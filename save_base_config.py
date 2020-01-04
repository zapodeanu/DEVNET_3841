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


import cli
from cli import cli, execute, configure

from config import FOLDER_NAME

import os
os.chdir(FOLDER_NAME)


# This code is needed to run after every change made to the configuration of the switch


# check if 'Config_Files' folder exists and creates one if it does not

if not os.path.exists('Config_Files'):
    os.makedirs('Config_Files')

    # add additional vty lines, two required for EEM
    configure('no ip http active-session-modules none ; line vty 0 15 ; length 0 ; transport input ssh ; exit')

    print('Created additional vty lines')

    f = open('vasi_config.txt', 'r')
    cli_commands = f.read()
    configure(cli_commands)
    f.close()

    print('Configured VASI interfaces, vrf R, Loopback111, and routing')


    f = open('monitor_route_applet.txt', 'r')
    cli_commands = f.read()
    configure(cli_commands)
    f.close()

    print('Configured EEM applet')


# save baseline running configuration

output = execute('show run')

filename = 'Config_Files/base-config'

f = open(filename, 'w')
f.write(output)
f.close()

execute('copy run start')

execute('send log End of save_base_config.py Application Run')
print('\nEnd of save_base_config.py Application Run')
