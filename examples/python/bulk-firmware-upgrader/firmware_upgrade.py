import requests
import argparse
import time
import socket
import json

# pip install requests
# python3 firmware_upgrade.py -u root -p admin -f https://tachyon-networks.com/fw/tna-30x-1.11.1-r53981-20230426-tn-110-prs-squashfs-sysupgrade.bin -i 192.168.101.172

# Define command line arguments
parser = argparse.ArgumentParser(description='Firmware upgrade utility script')
parser.add_argument('-u', '--username', type=str, required=True, help='Username for authentication')
parser.add_argument('-p', '--password', type=str, required=True, help='Password for authentication')
parser.add_argument('-f', '--firmware', type=str, required=True, help='Path to firmware upgrade file')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-i', '--ip', nargs='+', help='IP address of device(s) to be upgraded')
group.add_argument('-if', '--ip_file', type=str, help='File containing list of IP addresses, one per line')
args = parser.parse_args()

if args.ip_file:
    with open(args.ip_file, 'r') as f:
        ips = f.read().splitlines()
elif args.ip:
    ips = args.ip

def make_request(method=None, url=None, headers=None, json=None):
    """
    Makes a REST API request using the provided HTTP/HTTPS method, URL, headers, JSON data.

    Args:
        method (str): The HTTP/HTTPS method to use for the request (e.g., "GET", "POST", "PUT", etc.).
        url (str): The URL to send the request to.
        headers (dict, optional): A dictionary of headers to include in the request.
        json (dict, optional): A dictionary of JSON data to include in the request body.

    Returns:
        The response object returned by the requests library.
    """

    # Send the request and get the response object
    response = requests.request(method=method, url=url, headers=headers, json=data)

    # Return the response object
    return response

for ip in ips: # Iterate over all specified devices
    
    print(f"\nWill now attempt to upgrade device at {ip} ...")
    cgi_url = f'http://{ip}/cgi.lua/apiv1/'
    
    # Post login credentials to your device in order to authenticate using REST interface.
    url = cgi_url + 'login'
    data = {'username': args.username, 'password': args.password}
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    response = make_request(method='post', url=url, headers=headers, json=data)

    # Check success of authentication.
    if response.status_code == 200:
        print('Authentication successful!')
    else:
        print(response.content)
        exit(1)

    # Retrieve the authentication token.

    auth_token = response.cookies.get_dict().get('token')
    if not auth_token:
        print(response.content)
        exit(1)
    
    # Fetch firmware version from the device and check whether the versions aren't already the same.

    url = cgi_url + 'stats?type=system'
    headers = {'accept': 'application/json', 'Cookie': f'api_token={auth_token}'}
    response = make_request(method='get', url=url, headers=headers)

    # Check success of firmware version fetch.
    if response.status_code == 200:
        specified_firmware_name = args.firmware.split('/')[-1]            # User specified firmware version
        tokens = specified_firmware_name.split('-')
        try:
            fw_version = json.loads(response.content)['system']['fw_version'] # Existing device firmware version
            version_number = fw_version.split()[0]
            revision_number = fw_version.split()[2]
            if (version_number in tokens) and ('r'+revision_number in tokens):
                print(f"Device already has firmware version '{version_number} rev {revision_number}'.\n")
                continue
        except:  #v1.10.3 does not have firmware version in response.content
            version_number = '1.10.3'
            if version_number in tokens:
                print(f"Device already has firmware version '{version_number}'.\n")
                continue
    else:
        print(response.content)
        exit(1)
        
    # Download firmware using REST interface
    url = cgi_url + 'update'
    data = {'firmware_url': args.firmware}
    headers = {'accept': 'application/json', 'Content-Type': 'application/json', 'Cookie': f'api_token={auth_token}'}
    response = make_request(method='put',url=url, json=data, headers=headers)

    if response.status_code == 200:
        print(f"Firmware {args.firmware} started downloading.")
    else:
        print(response.content)
        exit(1)

    # Get firmware upgrade status after download
    headers = {'accept': 'application/json', 'Cookie': f'api_token={auth_token}'}
    response = make_request(method='get', url=url, headers=headers)

    if response.status_code != 200:
        print(response.content)
        exit(1)
    else:
        status = response.json()
        print(f"Firmware upgrade status: {status['status']}")
        
    # Perform firmware upgrade
    headers = {'accept': 'application/json', 'Content-Type': 'application/json', 'Cookie': f'api_token={auth_token}'}
    data = {'reset': False, 'force': False}
    print("Will now wait up to 5 minutes for firmware download to finish...")
    start_time = time.time()
    while time.time() - start_time < 300:
        response = make_request(method='post', url=url, json=data, headers=headers)
        if response.status_code == 200:
            print('Firmware was sucessfully downloaded! Device will be upgraded after reboot.')
            break
        time.sleep(2)

    if response.status_code != 200:
        print(response.content)
        exit(1)

    # Keep getting response status until firmware flashing is done
    headers = {'accept': 'application/json', 'Cookie': f'api_token={auth_token}'}
    print("Will now wait up to 5 minutes for firmware flashing to complete...")
    start_time = time.time()
    while status['status'] != 'COMPLETE' and time.time() - start_time < 300:
        response = make_request(method='get', url=url, headers=headers)
        status = response.json()
        print(f"Firmware upgrade status: {status['status']}")
        time.sleep(5)

    if status['status'] != 'COMPLETE':
        print(f"Firmware flashing failed.")
        exit(1)
        
    # Reboot system for firmware to be upgraded
    url = cgi_url + 'reboot'
    headers = {'accept': 'application/json', 'Cookie': f'api_token={auth_token}'}
    response = make_request(method='post', url=url, headers=headers)
    if response.status_code == 200:
        print(f"Device started rebooting! Waiting for it to finish...")
        time.sleep(10)  # wait for device to start rebooting
    else:
        print(response.content)
        exit(1)

    # Wait for reboot to finish
    start_time = time.time()
    successful_reboot = False
    print("Will now wait up to 5 minutes for device to reboot...")
    while time.time() - start_time < 300:
        try:
            s = socket.create_connection((ip, 80), timeout=1)  # create a socket connection to the IP address
            s.close()
            print("Reboot finished successfully!")
            successful_reboot = True
            break
        except OSError:
            time.sleep(10)  # wait for the specified time before trying again

    if not successful_reboot:
        print("Can no longer reach device after reboot start! Reboot failed.")
        exit(1)

    # Post login credentials to your device once again in order to authenticate (necessary after reboot).
    url = cgi_url + 'login'
    data = {'username': args.username, 'password': args.password}
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    response = make_request(method='post', url=url, headers=headers, json=data)

    # Check success of authentication.
    if response.status_code == 200:
        print('Authentication successful!')
    else:
        print(response.content)
        exit(1)

    # Retrieve the authentication token.

    auth_token = response.cookies.get_dict().get('token')
    if not auth_token:
        print(response.content)
        exit(1)
        
    # Fetch firmware version from the device.
    url = cgi_url + 'stats?type=system'
    headers = {'accept': 'application/json', 'Cookie': f'api_token={auth_token}'}
    response = make_request(method='get', url=url, headers=headers)

    # Check success of firmware version fetch.
    if response.status_code == 200:
        try:
            print("Updated firmware version: " + json.loads(response.content)['system']['fw_version'] + "\n") # Print device firmware version.
        except:
            print("Updated firmware version: " + "v1.10.3" + "\n") # Print device firmware version.
        
    else:
        print(response.content)
        exit(1)