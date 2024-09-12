ip="$1"
username=$2
password=$3
config_file=$4
params=$#

usage() 
{
echo "Usage: config-update.sh <device_ip> <username> <password> <config_file_json>"
echo "Example: ./config-update.sh 192.168.99.49 root admin ./config.json"
echo "NOTE: you can insert the dry_run parameter before the config json in order to do a dry run. Please see API docs."
}

if [ $params -lt 4 ]; then
  usage
  exit 1
fi

cookie="./tachyon-$ip.cookie"

echo "Logging into API for $ip"

# Get auth token 
curl -c $cookie -H "Content-type: application/json" -X POST -d '{"username": "'$2'", "password": "'$3'"}' http://$ip/cgi.lua/apiv1/login

echo ""

# Parse out cookie token
token=$(cat $cookie | grep token | awk '{print $7}')

echo "Updating config $ip to $config_file"

# Add  "dry_run": true if you want to do a dry run in your config file.  The resulting file will look like { "dry_run": true, "config": { .... } }
curl -H "Cookie: api_token=$token" -H "Content-Type: application/json"  -X POST "http://$ip/cgi.lua/apiv1/config" -d "@$config_file"

rm $cookie
