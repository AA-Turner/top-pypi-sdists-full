# cython: language_level=3, embedsignature=True, boundscheck=False, wraparound=False, initializedcheck=False
# Copyright (C) 2018-present Jesus Lara
#
"""
Parsing a Task from a YAML file.
"""
import yaml
from .base cimport TaskParser
from ..exceptions import TaskParseError

cdef class YAMLParser(TaskParser):
    async def parse(self, str content):
        try:
            return yaml.load(content, Loader=yaml.FullLoader)
        except Exception as err:
            raise TaskParseError(
                f'Task parsing Error on {self.filename!s} with Error: {err!s}.'
            )
