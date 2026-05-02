# cython: language_level=3, embedsignature=True, boundscheck=False, wraparound=False, initializedcheck=False
# Copyright (C) 2018-present Jesus Lara
#
"""
Parsing a Task from a TOML file.
"""
import pytomlpp
from .base cimport TaskParser
from ..exceptions import TaskParseError

cdef class TOMLParser(TaskParser):
    async def parse(self, str content):
        try:
            return pytomlpp.loads(content)
        except Exception as err:
            raise TaskParseError(
                f'Task parsing Error on {self.filename!s} with Error: {err!s}.'
            )
