#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""

Copyright (c) 2019 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

__author__ = "Gabriel Zapodeanu TME, ENB"
__email__ = "gzapodea@cisco.com"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2019 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"


import json
import requests
import utils
import service_now_apis
import config
import netconf_restconf
import config_diff
import dnac_apis
import cli
import argparse
import time
import os
import os.path


from requests.auth import HTTPBasicAuth

from config import SNOW_DEV
from config import IOS_XE_PASS, IOS_XE_USER
from config import DNAC_URL, DNAC_USER, DNAC_PASS
from config import FOLDER_NAME
from config import DNAC_PROJECT, DNAC_CLI_TEMPLATE, FOLDER_NAME

from cli import cli, execute, configure

parser = argparse.ArgumentParser()
parser.description = 'The monitored route the application will alert on'
parser.add_argument('route')
args = parser.parse_args()
monitored_route = args.route


DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)


execute('send log "monitor_route.py" Application Run started')
print(str('\n\n"monitor_route.py" Application Run started'))

# retrieve the ios xe device management ip address, Gi0/0, not the VPG IP address
ios_xe_host_ip = execute('sh run int gi1 | in ip address').split(' ')[3]

# retrieve the device hostname using RESTCONF
device_hostname = netconf_restconf.get_restconf_hostname(ios_xe_host_ip, IOS_XE_USER, IOS_XE_PASS)
print(str('\nThe device hostname: ' + device_hostname))

# create a new Service Now incident
description = 'Monitored route: ' + monitored_route + ' Lost, device hostname: ' + device_hostname

comment = 'The device with the name: ' + device_hostname + ' has detected the loss of a critical route'
comment += '\n\nThe route: ' + monitored_route + ' - is missing from the routing table'

snow_incident = service_now_apis.create_incident(description, comment, SNOW_DEV, 1)

# The following commands to be use when Cisco DNA Center is available

# get DNA C AUth JWT token
dnac_token = dnac_apis.get_dnac_jwt_token(DNAC_AUTH)

# get device details
epoch_time = utils.get_epoch_current_time()
device_details = dnac_apis.get_device_health(device_hostname, epoch_time, dnac_token)
device_sn = device_details['serialNumber']
device_management_ip = device_details['managementIpAddr']
device_family = device_details['platformId']
device_os_info = device_details['osType'] + ',  ' + device_details['softwareVersion']
device_health = device_details['overallHealth']
device_location = device_details['location']

comment = ''
comment += "\nDevice management IP address: " + device_management_ip
comment += "\n\nDevice location: " + device_location
comment += "\nDevice family: " + device_family
comment += "\nDevice OS info: " + device_os_info
comment += '\nDevice S/N: ' + device_sn
comment += "\nDevice Health: " + str(device_health) + "/10"

print(comment)

service_now_apis.update_incident(snow_incident, comment, SNOW_DEV)

# download the troubleshooting CLI commands from Cisco DNA Center

cli_template_info = dnac_apis.get_template_name_info(DNAC_CLI_TEMPLATE, DNAC_PROJECT, dnac_token)
cli_template = cli_template_info['templateContent']
print(str('\nThe troubleshooting commands downloaded from Cisco DNA Center are:\n' + cli_template))
cli_commands_list = cli_template.split('\n')

# execute each command, send log to device logging, print to console, update ServiceNow incident
for command in cli_commands_list:
    comment = str('Exec command downloaded from Cisco DNA Center, ' + DNAC_PROJECT + '/' + DNAC_CLI_TEMPLATE + ' :  ' + command)
    # print to Python console, log to host device, and update ServiceNow
    print(comment)
    execute('send log ' + comment)

    # send the command to device using Python CLI
    output_message = comment + '\n\n' + execute(str(command))
    service_now_apis.update_incident(snow_incident, output_message, SNOW_DEV)
    time.sleep(2)

# identify if config changes from baseline and by who

temp_run_config_filename = FOLDER_NAME + 'temp_run_config.txt'
device_run_config = execute('show running-config')

# save the running config to a temp file

f_temp = open(temp_run_config_filename, 'w')
f_temp.write(device_run_config)
f_temp.seek(0)  # reset the file pointer to 0
f_temp.close()

baseline_filename = FOLDER_NAME + str(device_hostname) + '_baseline.txt'

# check if device has an existing baseline configuration file
# if yes, run the diff function
# if not, save the device configuration as the baseline

if os.path.isfile(baseline_filename):
    diff = config_diff.compare_configs(baseline_filename, temp_run_config_filename)
    updated_comment = ''
    if diff != '':
        # there are configurations changes
        # find the users that made configuration changes
        with open(temp_run_config_filename, 'r') as f:
            user_info = 'User info no available'
            for line in f:
                if 'Last configuration change' in line:
                    user_info = line

        updated_comment = '\nThere are configuration changes \n' + diff + '\n\n' + user_info
        execute('send log Configurations changes found')
    else:
        # there are no configurations changes
        updated_comment = '\nThere are no configuration changes'
        execute('send log There are no configuration changes')

    # update ServiceNow incident
    print(updated_comment)

    service_now_apis.update_incident(snow_incident, updated_comment, SNOW_DEV)

else:
    # no config baseline found
    print('No baseline config found, saved new baseline config')
    execute('send log No baseline config found, saved new baseline config')

execute('send log End of "monitor_route.py" Application Run')
print(str('\n\nEnd of "monitor_route.py" Application Run'))
