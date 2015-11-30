#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import pymysql

from connector.connector import BaseConnector
from utils import command

logger = logging.getLogger(__name__)


class MySQLConnector(BaseConnector):
    def __init__(self,
                 host=None,
                 port=None,
                 user=None,
                 password=None,
                 db=None,
                 ):
        super(MySQLConnector, self).__init__()

        self.host = host if host else self.config.mysql.get('host', None)
        self.port = port if port else self.config.mysql.get('port', None)
        self.user = user if user else self.config.mysql.get('user', None)
        self.password = password if password else self.config.mysql.get('password', None)
        self.database = db if db else self.config.mysql.get('db', None)

    def connect(self):
        if self.connection:
            return

        self.connection = pymysql.connect(host=self.host,
                                          port=int(self.port) if self.port else 0,
                                          db=self.database,
                                          user=self.user,
                                          passwd=self.password,
                                          charset='utf8',
                                          autocommit=True)

    def get_columns(self, table):
        query = "desc {table};".format(table=table)
        success, rows, columns = self.execute(query)
        columns = dict()
        for row in rows:
            columns[row[0].lower()] = row
        return columns

    def dump_using_command_tool(self, query, cmds=None, path=None):
        cmd = "echo '{query}' | mysql -h {host} -B --column_names=0 -u{user} -p{password} " \
              "{database} | {cmds} >> {path}" \
            .format(host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    query=query,
                    cmds=cmds,
                    path=path)
        command.run(cmd)

    def set_index(self, table=None, column=None):
        query = 'ALTER TABLE {table} ' \
                'ADD INDEX ({column});'.format(table=table,
                                               column=column)
        success, rows, columns = self.execute(query)
        return success

    def truncate_table(self, table=None):
        query = 'TRUNCATE TABLE {table};'.format(table=table)
        success, rows, columns = self.execute(query)
        return success

    def safe_execute(self, query=None):
        self.execute('START TRANSACTION;')
        try:
            self.execute(query)
            self.execute('COMMIT;')
            return True, 'load successful'
        except Exception as error:
            self.execute('ROLLBACK;')
            return False, error

    def alter_table(self, table=None, staging=None):
        alter_query = 'DROP TABLE IF EXISTS {table};' \
                      'ALTER TABLE {staging} ' \
                      'RENAME TO {table};'
        success, message = self.safe_execute(query=alter_query)
        return success, message