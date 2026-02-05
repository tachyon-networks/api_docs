## General

This is a very simple command-line based firmware upgrade utility that will upgrade one unit at a time.

Notes:
* You must pass the firmware in the form of a URL.  If the version information isn't available in the URL path, then use the --force flag to bypass comparison checking.
* If the verison of the new firmware is older than the device's current firmware, then no firmware upgrade will be performed unless the --force flag is specified.

## Example: 

 $> ./firmware_upgrade.py  --ip 192.168.99.133 --username XXXXX --password XXXXX --url http://tachyon-networks.com/fw/tna-30x/1.12.3/tna-30x-1.12.3-r54999-20260204-tn-110-prs-squashfs-sysupgrade.bin


============================================================
FIRMWARE UPGRADE PROCESS
============================================================

Logging in to 192.168.99.133...
✓ Login successful
Fetching device information...
  Device model: n/a
  Current firmware (active bootbank):   1.12.3 rev 54970
  Alternate firmware (backup bootbank):	1.12.3 rev 54999

Version comparison:
  Current: 1.12.3-r54970
  New:     1.12.3-r54999
✓ Upgrade available - proceeding with upgrade

Sending firmware URL to device...
✓ Firmware download initiated
Waiting for state: FIRMWARE_DOWNLOAD
  Status: PENDING, State: FIRMWARE_DOWNLOAD
  Status: SUCCESS, State: FIRMWARE_DOWNLOAD
✓ FIRMWARE_DOWNLOAD completed successfully
Starting firmware flashing...
✓ Firmware flashing initiated
Waiting for state: FIRMWARE_FLASHING
  Status: IN_PROGRESS, State: FIRMWARE_FLASHING
  Status: IN_PROGRESS, State: FIRMWARE_FLASHING
  Status: COMPLETE, State: FIRMWARE_FLASHING
✓ FIRMWARE_FLASHING completed successfully
Rebooting device...
✓ Reboot initiated
Waiting for device to come back online...
✓ Device is back online
Verifying firmware upgrade...
Logging in to 192.168.99.133...
✓ Login successful
Fetching current firmware version...
  Device model: TNA-301
  Current firmware (active bootbank):	1.12.3 rev 54999
  Alternate firmware (backup bootbank):	1.12.3 rev 54999
✓ Upgrade complete. New firmware version: 1.12.3 rev 54999


## Example: with --force

$> ./firmware_upgrade.py  --ip 192.168.99.133 --username root --password admin1 --url http://tachyon-networks.com/fw/tna-30x/1.12.3/tna-30x-1.12.3-r54999-20260204-tn-110-prs-squashfs-sysupgrade.bin --force 


============================================================
FIRMWARE UPGRADE PROCESS
============================================================

Logging in to 192.168.99.133...
✓ Login successful
Fetching device information...
  Device model: n/a
  Current firmware (active bootbank):	1.12.3 rev 54999
  Alternate firmware (backup bootbank):	1.12.3 rev 54970
⚠ Force flag enabled - skipping version extraction and comparison

Sending firmware URL to device...
✓ Firmware download initiated
Waiting for state: FIRMWARE_DOWNLOAD
  Status: PENDING, State: FIRMWARE_DOWNLOAD
  Status: SUCCESS, State: FIRMWARE_DOWNLOAD
✓ FIRMWARE_DOWNLOAD completed successfully
Starting firmware flashing...
✓ Firmware flashing initiated
Waiting for state: FIRMWARE_FLASHING
  Status: IN_PROGRESS, State: FIRMWARE_FLASHING
  Status: IN_PROGRESS, State: FIRMWARE_FLASHING
  Status: COMPLETE, State: FIRMWARE_FLASHING
✓ FIRMWARE_FLASHING completed successfully
Rebooting device...
✓ Reboot initiated
Waiting for device to come back online...
✓ Device is back online
Logging in to 192.168.99.133...
✓ Login successful
Fetching device information...
  Device model: TNA-301
  Current firmware (active bootbank):	1.12.3 rev 54999
  Alternate firmware (backup bootbank):	1.12.3 rev 54999
✓ Upgrade complete. New firmware version: 1.12.3 rev 54999


