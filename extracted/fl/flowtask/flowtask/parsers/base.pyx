# cython: embedsignature=True, boundscheck=False, wraparound=False, initializedcheck=False
# Copyright (C) 2018-present Jesus Lara
#
"""
Parsing a Task File (abstract Method)
"""
cimport cython
import errno
from pathlib import PosixPath
import aiofiles
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

    def _is_eagain(self, exc):
        """Return True when *exc* signals EAGAIN ('Resource temporarily
        unavailable'), regardless of the concrete exception class.

        Kept as defence-in-depth: a plain ``OSError`` carries ``errno`` set
        to EAGAIN, while native-AIO backends may surface it as a
        ``SystemError(11, ...)`` instead. Detect both shapes.
        """
        if getattr(exc, 'errno', None) == errno.EAGAIN:
            return True
        args = getattr(exc, 'args', ())
        return bool(args) and args[0] == errno.EAGAIN

    async def open_file(self):
        cdef str content
        try:
            # aiofiles delegates to a thread-pool executor (no native libaio
            # io_setup / fs.aio-max-nr budget), so it is immune to the EAGAIN
            # context-exhaustion seen under high Qworker concurrency.
            async with aiofiles.open(self.filename, 'r') as fp:
                return await fp.read()
        except (OSError, SystemError) as e:
            # EAGAIN: fall back to a plain blocking read so the task can
            # still be parsed.
            if self._is_eagain(e):
                try:
                    with open(self.filename, 'r') as fp:
                        return fp.read()
                except Exception as ex:
                    raise TaskNotFound(
                        f'Task {self.filename!s} IO Error: {ex!s}'
                    )
            raise TaskError(
                f'Task File: {self.filename!s} with Error: {e!s}'
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
