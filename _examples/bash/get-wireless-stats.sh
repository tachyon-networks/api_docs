#!/bin/bash

ip=$1
username=$2
pass=$3

[ -z "$ip" ] && echo "Missing IP address" && 
	echo "Usage: ./get-wireless.stats <device_ip> (username) (password)" &&
	echo "Default username and password will be used if not provided. " &&
	exit
[ -z "$username" ] && username="root"
[ -z "$pass" ] && pass="admin"

echo "Logging in...."
curl -c ./tachyon$ip.cookie -H "Content-type: application/json" -X POST -d "{\"username\": \"$username\", \"password\": \"$pass\"}" http://$ip/cgi.lua/apiv1/login
echo ""
token=$(cat tachyon$1.cookie | grep token | awk '{print $7}')

echo "Getting wireless stats:"
curl -H "Cookie: api_token=$token" http://$ip/cgi.lua/apiv1/stats?type=wireless
echo ""
echo ""
