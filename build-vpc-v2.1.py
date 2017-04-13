# Written for Python 3.x
# This script will connect to 2 switches and build a VPC Domain between them
# The basic VPC domain configuration will allow for building cross switch port-channels once completed.
# This requires management access on the switch, a user account with admin access, and NXAPI enabled on the switch

# Import section

import requests
import json
import getpass
import re

# User option to select which part to build VPC domain or VPC interfaces.

var_user_option = "0"
while not re.match("1|2", var_user_option):
    print("1) Build initial VPC Domain")
    print("2) Add Port-channel (VPC) to VPC switch pair")
    var_user_option = input("Select option > ")

    if not re.search("1|2", var_user_option):
        print("Please select an available option")
        print("")

# User input
var_user_yn = "a"
while var_user_yn != "y":

    # if var_user_yn == "n":
    #    var_sw_user = input("Enter your username for the switches ("+str(var_sw_user)+"> ")
    #    var_sw_pass = getpass.getpass("Enter your password > ")
    #    var_sw1_ip = input("Enter IP address of switch 1 > ")
    #    var_sw2_ip = input("Enter IP address of switch 2 > ")
    #    var_vpc_domain_id = input("Enter VPC Domain ID - This should not overlap with any other domain IDs > ")
    #    var_vpc_eth1 = input("Enter the first interface for the VPC Peerlink ie:x/y > ")
    #    var_vpc_eth2 = input("Enter the second interface for the VPC Peerlink ie:x/y > ")
    #    var_po_num = input("Enter the desired port-channel ID for the VPC Peerlink > ")
    var_sw_user = input("Enter your username for the switches > ")
    var_sw_pass = getpass.getpass("Enter your password > ")
    var_sw1_ip = input("Enter IP address of switch 1 > ")
    var_sw2_ip = input("Enter IP address of switch 2 > ")

    if var_user_option == "1":
        var_vpc_domain_id = input("Enter VPC Domain ID - This should not overlap with any other domain IDs > ")
        var_vpc_eth1 = input("Enter the first interface for the VPC Peerlink ie:x/y > ")
        var_vpc_eth2 = input("Enter the second interface for the VPC Peerlink ie:x/y > ")
        var_po_num = input("Enter the desired port-channel ID for the VPC Peerlink > ")

# Verify input to user

        print("Switch IP addresses are:")
        print(str(var_sw1_ip)+" and "+str(var_sw2_ip))
        print("VPC Domain ID is: "+str(var_vpc_domain_id))
        print("VPC Peerlink interfaces will be:")
        print("Eth"+str(var_vpc_eth1)+" and Eth"+str(var_vpc_eth2))
        print("These interfaces will use port-channel id: "+str(var_po_num))
        print("")

        var_user_yn = input("Is this correct? ie:y/n >")

    if var_user_option == "2":
        var_po_num = input("Enter the desired port-channel ID > ")
        var_num_ports = input("Enter the number of ports per switch in the port-channel (4 means an 8 port VPC) > ")
        print("")
        print("Select the port-channel mode access/trunk")
        print("1) Port-channel mode trunk")
        print("2) Port-channel mode trunk")
        var_pc_trunk = input("Port-channel mode > ")
        print("")
        print("Select the port-channel protocol")
        print("1) LACP")
        print("2) Mode On")
        var_pc_proto = input("Port-channel protocol > ")

        # port channel access or trunk
        # port channel vlans if trunk or all

# if input is correct push configuration to switches via NXAPI

if var_user_yn == "y":

    # Pushing configuration to switch 1

    myheaders = {'content-type': 'application/json-rpc'}
    url = "http://"+var_sw1_ip+"/ins"
    # var_sw_user = "admin"
    # var_sw_pass = "password"

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
                "cmd": "feature vpc",
                "version": 1
            },
            "id": 2
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "feature lacp",
                "version": 1
            },
            "id": 3
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "vpc domain "+str(var_vpc_domain_id),
                "version": 1
            },
            "id": 4
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "peer-switch",
                "version": 1
            },
            "id": 5},
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "role priority 100",
                "version": 1
            },
            "id": 6
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "peer-keepalive destination "+str(var_sw2_ip)+" source "+str(var_sw1_ip),
                "version": 1
            },
            "id": 7
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "role priority 100",
                "version": 1
            },
            "id": 8
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "interface e "+str(var_vpc_eth1)+",e"+str(var_vpc_eth2),
                "version": 1
            },
            "id": 9
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "switchport",
                "version": 1
            },
            "id": 10
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "switchport mode trunk",
                "version": 1
            },
            "id": 11
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "channel-group "+str(var_po_num)+" mode active",
                "version": 1
            },
            "id": 12
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "interface po"+str(var_po_num),
                "version": 1
            },
            "id": 13
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "vpc peer-link",
                "version": 1
            },
            "id": 14
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "wrmem",
                "version": 1
            },
            "id": 15
        },
    ]

    response = requests.post(url, data=json.dumps(payload), headers=myheaders, auth=(var_sw_user, var_sw_pass)).json()

    # Pushing Configuration to switch 2

    myheaders = {'content-type': 'application/json-rpc'}
    url = ("http://"+var_sw2_ip+"/ins")

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
                "cmd": "feature vpc",
                "version": 1
            },
            "id": 2
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "feature lacp",
                "version": 1
            },
            "id": 3
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "vpc domain " + str(var_vpc_domain_id),
                "version": 1
            },
            "id": 4
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "peer-switch",
                "version": 1
            },
            "id": 5
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "role priority 100",
                "version": 1
            },
            "id": 6
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "peer-keepalive destination " + str(var_sw1_ip) + " source " + str(var_sw2_ip),
                "version": 1
            },
            "id": 7
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "role priority 100",
                "version": 1
            },
            "id": 8
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "interface e " + str(var_vpc_eth1) + ",e" + str(var_vpc_eth2),
                "version": 1
            },
            "id": 9
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "switchport",
                "version": 1
            },
            "id": 10
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "switchport mode trunk",
                "version": 1
            },
            "id": 11
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "channel-group " + str(var_po_num) + " mode active",
                "version": 1
            },
            "id": 12
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "interface po" + str(var_po_num),
                "version": 1
            },
            "id": 13
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "vpc peer-link",
                "version": 1
            },
            "id": 14
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "wrmem",
                "version": 1
            },
            "id": 15
        },
    ]

    response = requests.post(url, data=json.dumps(payload), headers=myheaders, auth=(var_sw_user, var_sw_pass)).json()
else:
    print("Goodbye")
