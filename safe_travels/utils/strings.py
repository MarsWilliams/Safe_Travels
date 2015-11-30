#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import selenium


def remove_escape_characters(value=None):
    regex = re.compile(r'[\n\r\t]')
    return regex.sub('', value)


def parse_url(url=None):
    return selenium.selenium.urllib_parse.urlparse(url)


def build_url_from_parts(parts=None):
    return selenium.selenium.urllib_parse.urlunparse(parts)
