#!/usr/local/bin/python3
import subprocess, sys
import http.client, os
import pprint, json, time
from json import JSONDecodeError

# SET PARAMETERS HERE
DEVICE_IP = "192.168.99.48"     # Device IP address
DRY_RUN = False                 # If we want to perform a dry run instead of a real config push
USERNAME = "root"               # Device login username
PASSWORD = "admin"              # Device login password
HOSTNAME = "hostname-123"       # New hostname
VERBOSE_DEBUG = False           # Whether or not to show the output of the response

def login():
    print(f"Attempting to login with username {USERNAME} and password {PASSWORD} to IP {DEVICE_IP}\n")

    headers = { "Content-Type" : "application/json" }

    login_data = json.dumps({ "username" : USERNAME, "password": PASSWORD })

    connection = http.client.HTTPConnection(DEVICE_IP)

    connection.request("POST", "/cgi.lua/apiv1/login", login_data, headers=headers)

    response = connection.getresponse() 

    response_body = json.loads(response.read().decode())

    if VERBOSE_DEBUG: 
        print("Response from login: ")
        print(response_body)

    if ("error" in response_body):
        print("Error logging in: " + response_body["error"]["details"])
        exit()

    token = response_body['token']

    if VERBOSE_DEBUG: 
        print(f"Token is {token}")

    connection.close()
    return token


def logout(token):
    headers = {  "Cookie" : f"api_token={token}" }

    connection = http.client.HTTPConnection(DEVICE_IP)
    connection.request("DELETE", "/cgi.lua/apiv1/login", headers=headers)

    response = connection.getresponse().read()

    connection.close()

def fetch_config(token):
    print(f"Fetching config from device with token {token}\n")

    headers = {  
        "Content-Type" : "application/json",
        "Cookie" : f"api_token={token}" 
    }

    connection = http.client.HTTPConnection(DEVICE_IP)
    connection.request("GET", "/cgi.lua/apiv1/config", headers=headers)
    response = connection.getresponse()
    response_body = json.loads(response.read().decode())

    if VERBOSE_DEBUG:
        print(response_body)
        print("")

    connection.close()
    return response_body

def set_hostname(config, hostname):
    config["system"]["hostname"] = hostname
    return config

def change_hostname():
    token = login()

    # Fetch config
    response_body = fetch_config(token)

    if ("error" in response_body):
        print("Error fetching config: " + response_body["error"]["details"])
        exit()

    config = response_body["config"]

    connection = http.client.HTTPConnection(DEVICE_IP)

    ## Set hostname in config, can also change other fields here
    config = set_hostname(config, HOSTNAME)

    data = { "config" : config, "dry_run": DRY_RUN }

    # Get new JSON-encoded config
    str_data = json.dumps(data)

    headers = {  
        "Content-Type" : "application/json",
        "Cookie" : f"api_token={token}" ,
        "Content-Length" : len(str_data)
    }

    print(f"Pushing new config now, dry run is set to {DRY_RUN}.\n")

    connection.request("POST", "/cgi.lua/apiv1/config", str_data, headers=headers)

    response = connection.getresponse()

    if VERBOSE_DEBUG: 
        print(f"Response code is: {response.status}, reason: {response.reason}")

    response_body = response.read().decode()

    if VERBOSE_DEBUG: 
        print(response_body)
        print("")

    valid = True

    try:
        json_response = json.loads(response_body)
    except (JSONDecodeError, json.JSONDecodeError):
        valid = False

    if (not valid):
        print("Error: received invalid JSON response")

    if ("error" in json_response):
        print("Received config response error: "+ json_response["error"]["details"])
    elif response.status != 200:
        print("Received server error: " + response_body)
    else: 
        print(f"Config change response: {json_response['status_msg']}")
        print(f"\tIs reboot required? {json_response['response']['reboot_required']}")
        print(f"\tKeys changed: {json_response['response']['keys_changed']}")
        print(f"\tKeys added: {json_response['response']['keys_added']}")
        print(f"\tKeys removed: {json_response['response']['keys_removed']}")
        print(f"\tWarnings: {json_response['response']['warnings']}")

    connection.close()
    logout(token)

change_hostname()