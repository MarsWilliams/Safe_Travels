#!/usr/bin/env python
# -*- coding: utf-8 -*-
CONFIG_STR = 'config'
CFG_FILE = 'path.conf'
MYSQL_CFG_FILE = 'mysql.conf'


def get_constants():
    constants = dict()
    constants['config_str'] = CONFIG_STR
    constants['config_file'] = CFG_FILE
    constants['mysql_config_file'] = MYSQL_CFG_FILE
    return constants


