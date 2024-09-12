
ip="$1"
username=$2
password=$3
params=$#

usage() 
{
echo "Usage: config-fetch.sh  <device_ip> <username> <password>"
echo "Example: ./config-fetch.sh 192.168.99.49 root admin"
echo ""
}

if [ $params -lt 3 ]; then
  usage
  exit 1
fi

cookie="./tachyon-$ip.cookie"

echo "Logging into API for $ip"

# Get auth token 
curl -c $cookie -H "Content-type: application/json" -X POST -d '{"username": "'$2'", "password": "'$3'"}' http://$ip/cgi.lua/apiv1/login

echo ""

# Fetch token from cookie

token=$(cat $cookie | grep token | awk '{print $7}')

echo "Fetching config for $ip and saving to ./$ip-config.json"

curl -H "Cookie: api_token=$token" "http://$ip/cgi.lua/apiv1/config" -o "$ip-config.json"

rm $cookie
