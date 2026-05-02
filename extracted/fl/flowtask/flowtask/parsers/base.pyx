# cython: embedsignature=True, boundscheck=False, wraparound=False, initializedcheck=False
# Copyright (C) 2018-present Jesus Lara
#
"""
Parsing a Task File (abstract Method)
"""
cimport cython
import errno
from pathlib import PosixPath
from aiofile import async_open
from ..exceptions import TaskError, TaskParseError, TaskDefinition, TaskNotFound


cdef class TaskParser:
    # cdef public object filename

    def __init__(self, str file = None, str content = None):
        self.filename = file
        self.content = content
        if file:
            self.filename = PosixPath(file)

    def task_exists(self):
        return self.filename.exists()

    async def open_file(self):
        cdef str content
        try:
            async with async_open(self.filename, 'r') as fp:
                return await fp.read()
        except OSError as e:
            try:
                if e.errno == errno.EAGAIN:
                    with open(self.filename, 'r') as fp:
                        return fp.read()
            except Exception as ex:
                raise TaskNotFound(
                    f'Task {self.filename!s} IO Error: {ex!s}'
                )
        except IOError as e:
            raise TaskNotFound(
                f'Task File {self.filename!s} is not accessible: {e!s}'
            )
        except Exception as err:
            raise TaskError(
                f'Task File: {self.filename!s} with Error: {err!s}'
            )

    async def run(self):
        cdef str content
        content = None
        if self.filename:
            content = await self.open_file()
        else:
            content = self.content
        return await self.parse(content)

    async def parse(self, str content):
        pass
