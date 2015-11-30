#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
from os import environ
from config.constants import get_constants


class Config(object):

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.get_config_files())
        dictionary = {}
        for section in self.config.sections():
            dictionary[section] = {}
            for option in self.config.options(section):
                dictionary[section][option] = self.config.get(section, option)
        self.__dict__ = dictionary

    def dict(self):
        return self.__dict__

    @staticmethod
    def get_config_files():
        if 'SAFE_TRAVELS_HOME' not in environ:
            raise Exception('You have to set SAFE_TRAVELS_HOME environment variable.')
        constants = get_constants()
        safe_travels_home = environ['SAFE_TRAVELS_HOME']
        conf_dir = 'conf/'
        config_file = safe_travels_home + conf_dir + constants['config_file']
        mysql_file = safe_travels_home + conf_dir + constants['mysql_config_file']
        config_files = [config_file, mysql_file]
        return config_files
