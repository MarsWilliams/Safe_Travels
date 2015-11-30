#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def remove_escape_characters(value):
    regex = re.compile(r'[\n\r\t]')
    return regex.sub('', value)
