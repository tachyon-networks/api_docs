#!/usr/bin/env python3
"""
Firmware Upgrade Script
Upgrades device firmware only if the provided firmware is newer than the current version.
"""

import argparse
import re
import requests
import time
import sys
from typing import Optional, Tuple
from packaging import version


class FirmwareUpgrader:
    def __init__(self, ip_address: str, username: str, password: str, firmware_url: str, force: bool = False):
        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.firmware_url = firmware_url
        self.force = force
        self.base_url = f"http://{ip_address}/cgi.lua/apiv1"
        self.api_token = None
        self.session = requests.Session()

    def extract_version_from_url(self, url: str) -> Optional[Tuple[str, int]]:
        """Extract version and revision from firmware filename in URL.

        Example: tna-30x-1.12.3-r54999-20260204-tn-110-prs-squashfs-sysupgrade.bin
        Returns: ('1.12.3', 54999)
        """
        # Match pattern like: {prefix}-{version}-r{revision}
        pattern = r'tna-\w+-(\d+\.\d+\.\d+)-r(\d+)'
        match = re.search(pattern, url)
        if match:
            ver = match.group(1)
            rev = int(match.group(2))
            return (ver, rev)
        return None

    def extract_version_from_string(self, version_string: str) -> Optional[Tuple[str, int]]:
        """Extract version and revision from version string.

        Handles multiple formats:
        - "1.12.3-r54999"
        - "1.12.3 rev 54999"
        - "1.12.3 r54999"
        Returns: ('1.12.3', 54999) or ('1.12.3', 0) if no revision
        """
        # Match version with optional revision in various formats
        # Matches: 1.12.3-r54999, 1.12.3 rev 54999, 1.12.3 r54999, etc.
        pattern = r'(\d+\.\d+\.\d+)(?:[-\s]r(?:ev)?\s*(\d+))?'
        match = re.search(pattern, version_string)
        if match:
            ver = match.group(1)
            rev = int(match.group(2)) if match.group(2) else 0
            return (ver, rev)
        return None

    def compare_versions(self, current: Tuple[str, int], new: Tuple[str, int]) -> int:
        """Compare two version tuples (version, revision).

        Args:
            current: Tuple of (version_string, revision_number)
            new: Tuple of (version_string, revision_number)

        Returns:
            1 if new > current (upgrade available)
            0 if new == current (same version and revision)
            -1 if new < current (downgrade)
        """
        try:
            current_ver, current_rev = current
            new_ver, new_rev = new

            current_parsed = version.parse(current_ver)
            new_parsed = version.parse(new_ver)

            # First compare semantic versions
            if new_parsed > current_parsed:
                return 1
            elif new_parsed < current_parsed:
                return -1
            else:
                # Versions are equal, compare revisions
                if new_rev > current_rev:
                    return 1
                elif new_rev < current_rev:
                    return -1
                else:
                    return 0

        except Exception as e:
            print(f"Error comparing versions: {e}")
            return 0

    def login(self) -> bool:
        """Authenticate and extract API token from cookie.

        Note: Server sends cookie as 'token' but expects it back as 'api_token'.
        """
        url = f"{self.base_url}/login"
        payload = {
            "username": self.username,
            "password": self.password
        }

        try:
            print(f"Logging in to {self.ip_address}...")
            response = self.session.post(url, json=payload, timeout=10)
            response.raise_for_status()

            # Extract token from 'token' cookie (server sends it with this name)
            if 'token' in response.cookies:
                self.api_token = response.cookies['token']
                print("✓ Login successful")
                return True
            else:
                print("✗ Login failed: No token cookie received")
                return False

        except requests.exceptions.RequestException as e:
            print(f"✗ Login failed: {e}")
            return False

    def get_current_firmware(self, show_model: bool = True) -> Optional[str]:
        """Get current firmware version from system stats.

        Extracts version from the active bootbank and optionally displays model info.

        Args:
            show_model: If True, display the device model
        """
        url = f"{self.base_url}/stats"
        params = {"type": "system"}

        try:
            print("Fetching device information...")
            response = self.session.get(
                url,
                params=params,
                cookies={"api_token": self.api_token},
                timeout=10
            )
            response.raise_for_status()

            data = response.json()

            # Get model if available and requested
            if show_model:
                try:
                    model = data['system']['model']
                    print(f"  Device model: {model}")
                except (KeyError, TypeError):
                    pass

            # Try to get version from active bootbank first (most accurate)
            try:
                current_version = data['system']['bootbanks']['active']['version']
                backup_version = data['system']['bootbanks']['backup']['version']
                print(f"  Current firmware (active bootbank):\t{current_version}")
                print(f"  Alternate firmware (backup bootbank):\t{backup_version}")
                return current_version
            except (KeyError, TypeError):
                # Fallback to fw_version if bootbank structure not available
                try:
                    current_version = data['system']['fw_version']
                    print(f"  Current firmware: {current_version}")
                    return current_version
                except (KeyError, TypeError):
                    print(f"✗ Could not find version in response: {data}")
                    return None

        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to get device information: {e}")
            return None

    def put_firmware_url(self) -> bool:
        """Send firmware URL to device to start download."""
        url = f"{self.base_url}/update"
        payload = {"firmware_url": self.firmware_url}

        try:
            print(f"Sending firmware URL to device...")
            response = self.session.put(
                url,
                json=payload,
                cookies={"api_token": self.api_token},
                timeout=10
            )
            response.raise_for_status()
            print("✓ Firmware download initiated")
            return True

        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to send firmware URL: {e}")
            return False

    def poll_update_status(self, expected_state: str, timeout: int = 600) -> bool:
        """Poll /update endpoint until expected state is reached.

        Args:
            expected_state: The state to wait for (e.g., 'FIRMWARE_DOWNLOAD', 'FIRMWARE_FLASHING')
            timeout: Maximum time to wait in seconds
        """
        url = f"{self.base_url}/update"
        start_time = time.time()

        print(f"Waiting for state: {expected_state}")

        while time.time() - start_time < timeout:
            try:
                response = self.session.get(
                    url,
                    cookies={"api_token": self.api_token},
                    timeout=10
                )
                response.raise_for_status()
                data = response.json()

                current_state = data.get('state')
                status = data.get('status')

                print(f"  Status: {status}, State: {current_state}")

                # Check if we've reached the expected state with SUCCESS or COMPLETE
                if current_state == expected_state:
                    if status in ['SUCCESS', 'COMPLETE']:
                        print(f"✓ {expected_state} completed successfully")
                        return True
                    elif status == 'FAILED' or status == 'ERROR':
                        print(f"✗ {expected_state} failed")
                        return False

                # Check for error states
                if status in ['FAILED', 'ERROR']:
                    print(f"✗ Process failed with status: {status}")
                    return False

                time.sleep(5)  # Poll every 5 seconds

            except requests.exceptions.RequestException as e:
                print(f"Warning: Polling error: {e}")
                time.sleep(5)

        print(f"✗ Timeout waiting for {expected_state}")
        return False

    def start_flashing(self, reset: bool = False) -> bool:
        """Tell device to start flashing the downloaded firmware."""
        url = f"{self.base_url}/update"
        payload = {"reset": reset}

        try:
            print("Starting firmware flashing...")
            response = self.session.post(
                url,
                json=payload,
                cookies={"api_token": self.api_token},
                timeout=10
            )
            response.raise_for_status()
            print("✓ Firmware flashing initiated")
            return True

        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to start flashing: {e}")
            return False

    def reboot_device(self) -> bool:
        """Reboot the device to activate new firmware."""
        url = f"{self.base_url}/reboot"

        try:
            print("Rebooting device...")
            response = self.session.post(
                url,
                json={},
                cookies={"api_token": self.api_token},
                timeout=10
            )
            response.raise_for_status()
            print("✓ Reboot initiated")
            return True

        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to reboot: {e}")
            return False

    def wait_for_device(self, timeout: int = 300) -> bool:
        """Wait for device to come back online after reboot."""
        print("Waiting for device to come back online...")
        start_time = time.time()

        # Wait a bit for reboot to start
        time.sleep(30)

        while time.time() - start_time < timeout:
            try:
                response = requests.get(
                    f"http://{self.ip_address}",
                    timeout=5
                )
                if response.status_code:
                    print("✓ Device is back online")
                    return True
            except requests.exceptions.RequestException:
                pass

            time.sleep(10)

        print("✗ Device did not come back online within timeout")
        return False

    def verify_upgrade(self, expected_version: str) -> bool:
        """Verify that the upgrade was successful.

        Compares versions by parsing them into (version, revision) tuples
        to handle different format variations (e.g., "1.12.3-r54999" vs "1.12.3 rev 54999").
        """
        print("Verifying firmware upgrade...")

        # Login again after reboot
        if not self.login():
            return False

        # Get new firmware version
        current_version_string = self.get_current_firmware()

        if current_version_string:
            # Parse both versions into (version, revision) tuples for comparison
            expected_parsed = self.extract_version_from_string(expected_version)
            current_parsed = self.extract_version_from_string(current_version_string)

            if expected_parsed and current_parsed:
                expected_ver, expected_rev = expected_parsed
                current_ver, current_rev = current_parsed

                if expected_ver == current_ver and expected_rev == current_rev:
                    print(f"✓ Firmware upgrade successful! Version: {current_version_string}")
                    return True
                else:
                    print(f"✗ Version mismatch.")
                    print(f"  Expected: {expected_ver}-r{expected_rev}")
                    print(f"  Got:      {current_ver}-r{current_rev}")
                    return False
            else:
                # Fallback to string comparison if parsing fails
                if current_version_string == expected_version:
                    print(f"✓ Firmware upgrade successful! Version: {current_version_string}")
                    return True
                else:
                    print(f"✗ Version mismatch. Expected: {expected_version}, Got: {current_version_string}")
                    return False

        return False

    def upgrade(self) -> bool:
        """Execute the full firmware upgrade process."""
        print("\n" + "="*60)
        print("FIRMWARE UPGRADE PROCESS")
        print("="*60 + "\n")

        # Step 1: Login
        if not self.login():
            return False

        # Step 2: Get current firmware
        current_version_string = self.get_current_firmware()
        if not current_version_string:
            return False

        # Step 3: Version checking (skip if force flag is set)
        if self.force:
            print("⚠ Force flag enabled - skipping version extraction and comparison\n")
            # Set dummy values for later use
            new_ver, new_rev = None, None
        else:
            # Extract current version and revision
            current_version = self.extract_version_from_string(current_version_string)
            if not current_version:
                print(f"✗ Could not parse current version: {current_version_string}")
                return False

            # Extract new firmware version from URL
            new_version = self.extract_version_from_url(self.firmware_url)
            if not new_version:
                print("✗ Could not extract version from firmware URL")
                print("  If URL doesn't contain version info, use --force flag")
                return False

            current_ver, current_rev = current_version
            new_ver, new_rev = new_version

            print(f"\nVersion comparison:")
            print(f"  Current: {current_ver}-r{current_rev}")
            print(f"  New:     {new_ver}-r{new_rev}")

            # Compare versions
            comparison = self.compare_versions(current_version, new_version)

            if comparison == 1:
                print("✓ Upgrade available - proceeding with upgrade\n")
            elif comparison == 0:
                print("⚠ Firmware versions and revisions are the same - no upgrade needed")
                print("  Use --force to upgrade anyway")
                return True
            else:
                print("⚠ New firmware is older than current - skipping upgrade")
                print("  Use --force to downgrade anyway")
                return True

        # Step 6: Send firmware URL
        if not self.put_firmware_url():
            return False

        # Step 7: Wait for download to complete
        if not self.poll_update_status('FIRMWARE_DOWNLOAD', timeout=600):
            return False

        # Step 8: Start flashing
        if not self.start_flashing():
            return False

        # Step 9: Wait for flashing to complete
        if not self.poll_update_status('FIRMWARE_FLASHING', timeout=600):
            return False

        # Step 10: Reboot device
        if not self.reboot_device():
            return False

        # Step 11: Wait for device to come back
        if not self.wait_for_device():
            return False

        # Step 12: Verify upgrade
        if new_ver and new_rev is not None:
            # We know the expected version, verify it matches
            expected_version_string = f"{new_ver}-r{new_rev}"
            if not self.verify_upgrade(expected_version_string):
                return False
        else:
            # Force mode - just show the new version without verification
            if not self.login():
                return False
            new_firmware = self.get_current_firmware()
            if new_firmware:
                print(f"✓ Upgrade complete. New firmware version: {new_firmware}")
            else:
                print("⚠ Upgrade complete but could not fetch new firmware version")

        print("\n" + "="*60)
        print("FIRMWARE UPGRADE COMPLETED SUCCESSFULLY")
        print("="*60 + "\n")

        return True


def main():
    parser = argparse.ArgumentParser(
        description='Upgrade device firmware if newer version is available'
    )
    parser.add_argument('--ip', required=True, help='Device IP address')
    parser.add_argument('--username', required=True, help='Login username')
    parser.add_argument('--password', required=True, help='Login password')
    parser.add_argument('--url', required=True, help='Firmware download URL')
    parser.add_argument('--force', action='store_true',
                        help='Force upgrade even if new firmware is older or same version')

    args = parser.parse_args()

    upgrader = FirmwareUpgrader(
        ip_address=args.ip,
        username=args.username,
        password=args.password,
        firmware_url=args.url,
        force=args.force
    )

    try:
        success = upgrader.upgrade()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n✗ Upgrade interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
