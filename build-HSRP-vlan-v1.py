# Base is the output from Cisco NXAPI python tool.  From there it was modified to as seen.

import requests
import json
import getpass

var_sw_user = input("Enter your username > ")
var_sw_pass = getpass.getpass("Enter your password > ")
var_sw1_ip = input("Enter IP address of switch 1 > ")
var_sw2_ip = input("Enter IP address of switch 2 > ")
var_vlan_id = input("Enter VLAN ID - This should not overlap with any other VLAN IDs. > ")
var_temp_ip = input("Enter the HSRP virtual IP address with subnet mask ie:1.2.3.4/24 > ")

# IP address with mask is split to reuse the netmask for other IP addresses
var_hsrp_ip, var_subnet_mask = var_temp_ip.split('/', 1)

# HSRP IP is assumed to be .1 and the SVI IP addresses are 2 and 3.
# The SVI ip addresses are stored as lists so the last octet can be calculated which makes it easy to modify for .254 gateway instances
list_svi_ip1 = var_hsrp_ip.split(".", 4)
list_svi_ip2 = var_hsrp_ip.split(".", 4)
list_svi_ip1[3] = int(list_svi_ip1[3])+1
list_svi_ip2[3] = int(list_svi_ip2[3])+2

# Verifies input before pushing to switches
print("Switch IP addresses are:")
print(str(var_sw1_ip)+" and "+str(var_sw2_ip))
print("VLAN ID is: "+str(var_vlan_id))
print("The HSRP IP configuration will be:")
print("Standby IP:"+str(var_hsrp_ip))
print("SVI IP 1:"+str('.'.join(map(str, list_svi_ip1))))
print("SVI IP 2:"+str('.'.join(map(str, list_svi_ip2))))
print("")
user_yn = input("Is this correct? (y/n)")

# Push configuration to both switches.  First switch is assumed to be STP root and second switch is STP secondary for priority
if user_yn == "y":
    myheaders = {'content-type': 'application/json-rpc'}
    url = "http://"+var_sw1_ip+"/ins"

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
                "cmd": "feature interface-vlan",
                "version": 1
            },
            "id": 2
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "vlan "+str(var_vlan_id),
                "version": 1
            },
            "id": 3
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "spanning-tree vlan "+str(var_vlan_id)+" root primary",
                "version": 1
            },
            "id": 4
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "interface vlan "+str(var_vlan_id),
                "version": 1
            },
            "id": 5
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "no shutdown",
                "version": 1
            },
            "id": 6
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "ip address "+str('.'.join(map(str, list_svi_ip1)))+"/"+str(var_subnet_mask),
                "version": 1
            },
            "id": 7
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "hsrp version 2",
                "version": 1
            },
            "id": 8
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "hsrp "+str(var_vlan_id),
                "version": 1
            },
            "id": 9
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "preempt delay minimum 300",
                "version": 1
            },
            "id": 10
         },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "priority 110",
                "version": 1
            },
            "id": 11
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "ip "+str(var_hsrp_ip),
                "version": 1
            },
            "id": 12
        },
    ]

    response = requests.post(url, data=json.dumps(payload), headers=myheaders, auth=(var_sw_user, password)).json()

    myheaders = {'content-type': 'application/json-rpc'}
    url = "http://"+var_sw2_ip+"/ins"

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
                "cmd": "feature interface-vlan",
                "version": 1
            },
            "id": 2
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "vlan " + str(var_vlan_id),
                "version": 1
            },
            "id": 3
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "spanning-tree vlan " + str(var_vlan_id) + " root secondary",
                "version": 1
            },
            "id": 4
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "interface vlan " + str(var_vlan_id),
                "version": 1
            },
            "id": 5
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "no shutdown",
                "version": 1
            },
            "id": 6
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "ip address " + str('.'.join(map(str, list_svi_ip2))) + "/" + str(var_subnet_mask),
                "version": 1
            },
            "id": 7
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "hsrp version 2",
                "version": 1
            },
            "id": 8
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "hsrp " + str(var_vlan_id),
                "version": 1
            },
            "id": 9
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "preempt",
                "version": 1
            },
            "id": 11
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "ip " + str(var_hsrp_ip),
                "version": 1
            },
            "id": 12
        }
    ]

    response = requests.post(url, data=json.dumps(payload), headers=myheaders, auth=(var_sw_user, password)).json()

    print("Success!")

# Save configurations to switch.  Assumes CLI alias wrmem for copy run start
    var_save_yn = input("Would you like to save the configuration? (y/n) > ")

    if var_save_yn == "y":
        myheaders = {'content-type': 'application/json-rpc'}
        url = "http://"+var_sw1_ip+"/ins"
        payload = [
            {
                "jsonrpc": "2.0",
                "method": "cli",
                "params": {
                    "cmd": "wrmem",
                    "version": 1
                },
                "id": 1
            },
        ]
        
        response = requests.post(url, data=json.dumps(payload), headers=myheaders, auth=(var_sw_user, password)).json()

        url = "http://"+var_sw2_ip+"/ins"

        payload = [
            {
                "jsonrpc": "2.0",
                "method": "cli",
                "params": {
                    "cmd": "wrmem",
                    "version": 1
                },
                "id": 1
            },
        ]

        response = requests.post(url, data=json.dumps(payload), headers=myheaders, auth=(var_sw_user, password)).json()
        print("Goodbye")
    else:
        print("Configuration not saved!")
else:
    print("Goodbye")
