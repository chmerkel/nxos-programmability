# Written for Python 3.x
# Designed to take in switch ip addresses and add/change a user account on a NXOS devices with NXAPI enabled


import requests
import json
import getpass
# import re

var_username = input("Please enter the username to authenticate to the switch(es) > ")
var_password = getpass.getpass("Please enter the password to authenticate to the switch(es) > ")
var_switches = input("Please enter the IP address(es) or DNS name(s) of the switch(es) separated by commas if needed > ")
list_switches = var_switches.split(",")
print("")
var_newuser = input("Plese enter the new username > ")

# Gather new password for new user and validate the passwords are the same
var_newpass = "1"
var_newpass1 = "2"
while not var_newpass == var_newpass1:
    var_newpass = getpass.getpass("Please enter the new password > ")
    var_newpass1 = getpass.getpass("Please confirm the password > ")

    if not var_newpass == var_newpass1:
        print("Passwords do not match")
    else:
        print("Passwords match")

for var_ip in list_switches:
    url = 'http://'+str(var_ip)+'/ins'

    myheaders = {'content-type': 'application/json-rpc'}
    payload = [
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "conf t",
                "version": 1
            },
            "id": 1
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "username "+str(var_newuser)+" password "+str(var_newpass)+" role network-admin",
                "version": 1
            },
            "id": 2
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "copy run start",
                "version": 1
            },
            "id": 3
        }
    ]
    response = requests.post(url, data=json.dumps(payload), headers=myheaders, auth=(var_username, var_password)).json()
    print("Completed switch: "+str(var_ip))
print("Done!")
