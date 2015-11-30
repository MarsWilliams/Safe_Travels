#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from abc import abstractmethod

from workflow.base_workflow import BaseWorkflow
from utils import command

logger = logging.getLogger(__name__)


class BaseETLWorkflow(BaseWorkflow):
    def __init__(self, table, start_date, end_date):
        super(BaseETLWorkflow, self).__init__()
        self.path_data = self.config.path.get('target_data', None)
        self.table = table
        self.start_date = start_date
        self.end_date = end_date
        self.file_name = None

    def process(self):
        try:
            self.extract()
            self.verify_extract()
            self.transform()
            self.verify_transform()
            self.load()
            self.verify_load()
        except Exception as e:
            logger.error(e)
            raise

    @abstractmethod
    def load(self):
        pass

    def verify_load(self):
        pass

    @abstractmethod
    def extract(self):
        pass

    def verify_extract(self):
        pass

    @abstractmethod
    def transform(self):
        pass

    def verify_transform(self):
        pass

    def setup(self):
        self.base_dir, self.file, raw_file, self.compressed_file = \
            self.get_file_path()
        command.create_directories(self.base_dir)

    def get_file_path(self, arg=None, *args):
        if self.file_name is None:
            raise Exception('Must be set file_name')
        extend_path = ''
        if arg:
            extend_path = '/' + '/'.join([arg] + list(args))

        base_dir = "{path_data}/{table}{extend_path}".format(path_data=self.path_data,
                                                             table=self.table,
                                                             extend_path=extend_path)
        raw_file = "{base_dir}/{file_name}.raw".format(base_dir=base_dir, file_name=self.file_name)
        file = "{base_dir}/{file_name}".format(base_dir=base_dir, file_name=self.file_name)
        compressed_file = "{base_dir}/{file_name}.gz".format(base_dir=base_dir,
                                                             file_name=self.file_name)
        return base_dir, file, raw_file, compressed_file
