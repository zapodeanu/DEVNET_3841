#!/usr/bin/env python
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

import difflib

import urllib3
from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings

urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings


def compare_configs(cfg1, cfg2):
    """
    This function, using the unified diff function, will compare two config files and identify the changes.
    '+' or '-' will be prepended in front of the lines with changes
    :param cfg1: old configuration file path and filename
    :param cfg2: new configuration file path and filename
    :return: text with the configuration lines that changed. The return will include the configuration for the sections
    that include the changes
    """

    # open the old and new configuration files
    f1 = open(cfg1, 'r')
    old_cfg = f1.readlines()
    f1.close()

    f2 = open(cfg2, 'r')
    new_cfg = f2.readlines()
    f2.close()

    # compare the two specified config files {cfg1} and {cfg2}
    d = difflib.unified_diff(old_cfg, new_cfg, n=9)

    # create a diff_list that will include all the lines that changed
    # create a diff_output string that will collect the generator output from the unified_diff function
    diff_list = []
    diff_output = ''

    for line in d:
        diff_output += line
        if line.find('Current configuration') == -1:
            if line.find('Last configuration change') == -1:
                if (line.find('+++') == -1) and (line.find('---') == -1):
                    if (line.find('-!') == -1) and (line.find('+!') == -1):
                        if line.startswith('+'):
                            diff_list.append('\n' + line)
                        elif line.startswith('-'):
                            diff_list.append('\n' + line)

    # process the diff_output to select only the sections between '!' characters for the sections that changed,
    # replace the empty '+' or '-' lines with space
    diff_output = diff_output.replace('+!', '!')
    diff_output = diff_output.replace('-!', '!')
    diff_output_list = diff_output.split('!')

    all_changes = []

    for changes in diff_list:
        for config_changes in diff_output_list:
            if changes in config_changes:
                if config_changes not in all_changes:
                    all_changes.append(config_changes)

    # create a config_text string with all the sections that include changes
    config_text = ''
    for items in all_changes:
        config_text += items

    return config_text

