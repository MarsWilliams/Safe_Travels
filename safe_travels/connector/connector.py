#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import re
import time
from abc import ABCMeta, abstractmethod

from config.config import Config

logger = logging.getLogger(__name__)


class BaseConnector(metaclass=ABCMeta):
    config = Config()

    def __init__(self):
        self.host = None
        self.port = None
        self.user = None
        self.password = None
        self.database = None
        self.connection = None
        self.cursor = None

    def __exit__(self):
        self.disconnect()

    @abstractmethod
    def connect(self):
        pass

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute(self, query=None):
        success = True
        start_time = time.time()
        try:
            self.connect()
            cursor = self.connection.cursor()
            query = query.encode("ASCII", 'ignore')
            cursor.execute(query)
            columns = cursor.description if cursor.description else None
        except Exception as e:
            logger.error(query, e)
            raise e
        rows = list()
        try:
            for row in cursor:
                rows.append(row)
        except Exception as e:
            if not re.search('no results to fetch', str(e)):
                logger.error(e)
                raise e
        finally:
            cursor.close()
        elapsed_time = time.time() - start_time
        logger.debug("[elapsed_time: {elapsed_time}]"
                     " {query}".format(elapsed_time=elapsed_time,
                                       query=query))
        return success, rows, columns

    def execute_update(self, query):
        success, rows, columns = self.execute(query)
        return rows

    def execute_query(self, query):
        success, rows, columns = self.execute(query)
        return rows

    def get_max_value(self, table=None, id=None):
        if not table or not id:
            return -1
        query = "SELECT MAX({id}) FROM {table}".format(id=id, table=table)
        success, rows, columns = self.execute(query)
        try:
            value = rows[0][0]
        except Exception as e:
            logger.error(e)
            value = -1
        return value

    def get_count(self, table=None, id=None, condition=None):
        if not table:
            return -1
        condition = "WHERE {condition}".format(condition=condition) if condition else ''
        query = "SELECT COUNT({id}) FROM {table} {condition}".format(id=id if id else 1,
                                                                     table=table,
                                                                     condition=condition)
        success, rows, columns = self.execute(query=query)
        try:
            value = int(rows[0][0])
        except Exception as e:
            logger.error(e)
            value = -1
        return value
