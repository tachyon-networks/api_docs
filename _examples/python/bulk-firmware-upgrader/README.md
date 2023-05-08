<div style="margin-bottom: 0.5em; margin-top: 1.5em;">

# TACHYON FIRMWARE UPGRADER v1.0

The Tachyon Firmware Upgrader is a Python script that automates the firmware upgrade process for `Tachyon` devices. The utility script uses the REST interface to authenticate, upload firmware and start the upgrade process.

This utility will work on all models, TNA-30x, TNS-100, etc...

## Prerequisites

- Python 3.x
- Virtual environment
- requests
- argparse

## Setup

```
sudo apt-get update
sudo apt install python3
sudo apt-get install python3 virtualenv
```

Then, simply run `source setup.sh`. This will start the virtual environment and install all the necessary dependencies for you.

```
tester@tester:~/firmware-upgrader$ source setup.sh
created virtual environment CPython3.8.10.final.0-64 in 78ms
  creator CPython3Posix(dest=/home/tester/firmware-upgrader/venv, clear=False, global=False)
  seeder FromAppData(download=False, pip=latest, setuptools=latest, wheel=latest, pkg_resources=latest, via=copy, app_data_dir=/home/tester/.local/share/virtualenv/seed-app-data/v1.0.1.debian.1)
  activators BashActivator,CShellActivator,FishActivator,PowerShellActivator,PythonActivator,XonshActivator
Requirement already satisfied: requests in ./venv/lib/python3.8/site-packages (from -r requirements.txt (line 1)) (2.29.0)
Requirement already satisfied: argparse in ./venv/lib/python3.8/site-packages (from -r requirements.txt (line 2)) (1.4.0)
Requirement already satisfied: charset-normalizer<4,>=2 in ./venv/lib/python3.8/site-packages (from requests->-r requirements.txt (line 1)) (3.1.0)
Requirement already satisfied: urllib3<1.27,>=1.21.1 in ./venv/lib/python3.8/site-packages (from requests->-r requirements.txt (line 1)) (1.26.15)
Requirement already satisfied: certifi>=2017.4.17 in ./venv/lib/python3.8/site-packages (from requests->-r requirements.txt (line 1)) (2022.12.7)
Requirement already satisfied: idna<4,>=2.5 in ./venv/lib/python3.8/site-packages (from requests->-r requirements.txt (line 1)) (3.4)
(venv) tester@tester:~/firmware-upgrader$
```

## Running

In order to successfully run the script, the user is expected to provide:

- Username (-u)
- Password (-p)
- Firmware Upgrade File (-f)
- List of device IPv4 addresses (-i/-if) (specify either `-i` or `-if`)

The list of IPs can either be passed directly in the command line using `-i`, or be stored in a seperate file with a different IPv4 address in each line, which can be passed using `-if`. 

For example: `-i 192.168.101.172` or `-if example_ipfile.txt`. At least one IPv4 address needs to be specified.

All of these parameters are mandatory, or the script will not work. Lets try running it:

`python3 firmware_upgrade.py -u root -p admin -f http://192.168.101.69:8000/tna-30x-1.11.0-r53948-rc2-20230213-tn-110-prs-squashfs-sysupgrade.bin -i 192.168.101.172`

```
Will now attempt to upgrade device at 192.168.101.172 ...
Authentication successful!
Device already has firmware version '1.11.0 r53948'.
```

First, the script makes a `login` request using the `REST API`.
The next step is to check the existing firmware version and revision number at the specified IPv4 address. If they both match, we are done.

***Note:*** For the older version `1.10.3`, the revision number is not stored, so it is not accounted for when checking already existing firmware. Therefore, the script will not allow you to upgrade to a different `v1.10.3` revision, if the device already has `v1.10.3` firmware. If this is a problem, first update the device to a different version, and then update with the `1.10.3` revision you specifically need.

Lets try running the same command with a different firmware:

`python3 firmware_upgrade.py -u root -p admin -f http://192.168.101.69:8000/tna-30x-1.11.1-r53981-20230426-tn-110-prs-squashfs-sysupgrade.bin -i 192.168.101.172`

```
Will now attempt to upgrade device at 192.168.101.172 ...
Authentication successful!
Firmware http://192.168.101.69:8000/tna-30x-1.11.1-r53981-20230426-tn-110-prs-squashfs-sysupgrade.bin started downloading.
Firmware upgrade status: PENDING
Will now wait up to 1 minute for firmware download to finish...
Firmware was sucessfully downloaded! Device will be upgraded after reboot.
Will now wait up to 1 minute for firmware flashing to complete...
Firmware upgrade status: IN_PROGRESS
Firmware upgrade status: IN_PROGRESS
Firmware upgrade status: IN_PROGRESS
Firmware upgrade status: COMPLETE
Device started rebooting! Waiting for it to finish...
Will now wait up to 1 minute for device to reboot...
Reboot finished successfully!
Authentication successful!
Updated firmware version: 1.11.1 rev 53981
```

After comparing the firmware version, the scripts starts downloading firmware at the user specified `HTTP/HTTPS` address.
After the download is finished, it then begins the firmware flashing process, and reboots after that is done.
This is necessary, as the `tachyon` device will only be upgraded after rebooting.
After rebooting, we login once again to double check that the firmware version is updated.

***Note:*** To upgrade multiple devices with the same firmware file, you only need to specify all the IPv4 addresses at the end, and each device will be updated one by one. For example:

`python3 firmware_upgrade.py -u root -p admin -f http://192.168.101.69:8000/tna-30x-1.11.1-r53981-20230426-tn-110-prs-squashfs-sysupgrade.bin -i 0.0.0.0 1.1.1.1 2.2.2.2`

***Note:*** The firmware file specified must be in a hosted `HTTP/HTTPS` server, or you will get the following error message: `"Invalid firmware URL, only http/https protocols are currently supported."`. Thus, there are two scenarios:

1) The script downloads the firmware directly from `https://tachyon-networks.com/fw/`. In this case, your device must have access to the Internet:

`python3 firmware_upgrade.py -u root -p admin -f https://tachyon-networks.com/fw/tna-30x-1.11.1-r53981-20230426-tn-110-prs-squashfs-sysupgrade.bin -i 0.0.0.0 1.1.1.1 2.2.2.2`

2) You can download the firmware and host a simple web server on your PC:

    1. Go to the `firmware_upgrader` directory.
    2. Download the firmware in the current directory. For example:  `wget https://tachyon-networks.com/fw/tna-30x-1.11.1-r53981-20230426-tn-110-prs-squashfs-sysupgrade.bin`
    3. Start a web server on your PC. For example: `python3 -m http.server 8000 --bind 192.168.101.69`. In this case, your device must have access to both the Internet and your PC. Make sure to host the server with an address accessible by the device.
    4. Copy the firmware download link from your hosted server, in this case, `http://192.168.101.69:8000/`, and run the script:

`python3 firmware_upgrade.py -u root -p admin -f http://192.168.101.69:8000/tna-30x-1.11.1-r53981-20230426-tn-110-prs-squashfs-sysupgrade.bin -i 0.0.0.0 1.1.1.1 2.2.2.2`

</div>