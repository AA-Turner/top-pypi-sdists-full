# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Using logger.info/debug/someOtherLevel() is not supported in this module. In order to get the correct
frame info, we must skip over functions called in this module and in vendored structlog. If logging is attempted,
incorrect frame info will be displayed on the log message if used in this file.

Use print(...) instead
"""

from __future__ import annotations

import asyncio
from contextlib import suppress
import os
import pathlib
import io
import sys
from dataclasses import dataclass
from functools import partial
from typing import TextIO, cast

from contrast.agent import request_state
from contrast.utils.namespace import Namespace
from contrast_vendor import structlog
from contrast.utils.configuration_utils import get_hostname
from . import DEFAULT_PROGNAME
from contrast_vendor.filelock import FileLock, Timeout


class module(Namespace):
    file_handle: TextIO | None = None


@dataclass
class RotationConfig:
    backup_count: int
    max_bytes: int


class RotatingFile:
    """
    A file handler that rotates the log file when it reaches a certain size.

    Writes to instances of this class are not thread-safe. If calling write() from multiple threads,
    you must ensure that the writes are synchronized externally.
    """

    def __init__(self, file: TextIO, config: RotationConfig):
        if config.max_bytes <= 0:
            raise ValueError("max_bytes must be greater than 0")
        self._max_bytes = config.max_bytes
        if config.backup_count <= 0:
            raise ValueError("backup_count must be greater than 0")
        self._backup_count = config.backup_count
        self._file = file
        self._filename = file.name
        self._lock = FileLock(f".{self._filename}.lock")

    def write(self, message: str) -> int:
        """Write a message to the log file, performing rotation if needed."""
        self._rotate_if_needed(len(message))

        return self._file.write(message)

    # NOTE: flush() and close() are intentionally hardcoding the implementation
    # of __getattr__. This is critical for flush(), because structlog's WriteLogger
    # binds the flush method function to an internal attribute. If we don't introduce
    # this layer of indirection, then when we rotate the _file, structlog will attempt
    # to call flush() on the old file handle, which has already been closed.

    def flush(self):
        """Flush the log file."""
        self._file.flush()

    def close(self):
        """Close the log file."""
        self._file.close()

    def _reopen(self):
        """Reopen the log file."""
        self._file.close()
        self._file = open(self._filename, "a", encoding="utf-8")  # noqa: SIM115

    def _should_rollover(self, msg_size: int):
        """Check if the log file should be rotated."""
        file_size = self._file.tell()
        if file_size == 0:
            # If the file is empty, we either need to write to it or
            # discard the message. We can't rollover, because the new
            # file will be empty and we'd enter an infinitely loop.
            return False
        return file_size + msg_size > self._max_bytes

    def _rotate_if_needed(self, msg_size: int):
        """Check if the log file should be rotated and perform the rotation if needed."""
        # Refer to https://en.wikipedia.org/wiki/Double-checked_locking for background
        # on the pattern used here (and ways it can be broken).
        if not self._should_rollover(msg_size):
            return

        while True:
            with suppress(Timeout), self._lock.acquire(timeout=1):
                self._reopen()
                if self._should_rollover(msg_size):
                    self._do_rollover()
                return

    def _do_rollover(self):
        """Perform log file rotation."""
        # This implementation follows the Java and .NET agents decisions.
        # It's a little unconventional, but we want to keep the same behavior across languages
        # so that it's easier for our support team to troubleshoot issues from the logs.

        # Check if the highest backup slot is filled
        highest_backup = f"{self._filename}.{self._backup_count}"
        if not os.path.exists(highest_backup):
            # Not all slots are filled yet - find next available slot
            next_slot = 1
            while (
                os.path.exists(f"{self._filename}.{next_slot}")
                and next_slot < self._backup_count
            ):
                next_slot += 1

            os.rename(self._filename, f"{self._filename}.{next_slot}")
        else:
            # All slots filled - need to shift files
            # contrast.log.1 is the oldest, contrast.log.N is newest

            # Delete the oldest backup
            os.remove(f"{self._filename}.1")

            # Shift files down by one position (2→1, 3→2, etc.)
            for i in range(1, self._backup_count):
                src = f"{self._filename}.{i + 1}"
                dst = f"{self._filename}.{i}"
                if os.path.exists(src):
                    os.rename(src, dst)

            os.rename(self._filename, highest_backup)

        # Reopen the file
        self._reopen()

    def __getattr__(self, name: str):
        return getattr(self._file, name)


def add_hostname(logger, method_name, event_dict):
    event_dict["hostname"] = get_hostname()
    return event_dict


def add_request_id(logger, method_name, event_dict):
    event_dict["request_id"] = request_state.get_request_id()
    return event_dict


def rename_key(old_name, new_name):
    def key_renamer(logger, method_name, event_dict):
        value = event_dict.get(old_name)
        if value and not event_dict.get(new_name):
            event_dict[new_name] = value
            del event_dict[old_name]

        return event_dict

    return key_renamer


def add_progname(logger, method_name, event_dict, progname=DEFAULT_PROGNAME):
    """
    progname is the name of the process the agents uses in logs.
    The default value is Contrast Agent. progname will be used
    as the name of the logger as seen in the logs.
    """
    event_dict["name"] = progname

    return event_dict


def add_asyncio_info(logger, method_name, event_dict):
    try:
        if (current_task := asyncio.current_task()) is not None:
            # If no name has been explicitly assigned to the Task, the default asyncio Task implementation
            # generates a default name during instantiation.
            event_dict["asyncio_task_name"] = current_task.get_name()
            current_coro = current_task.get_coro()
            event_dict["asyncio_coro_name"] = current_coro.__qualname__
            event_dict["asyncio_task_id"] = id(current_task)
    except Exception:
        # This can happen when there is no running event loop
        pass

    return event_dict


def _log_level_to_int(level: str) -> int:
    level_to_int = {
        "DEBUG": 10,
        "TRACE": 10,
        "INFO": 20,
        "WARNING": 30,
        "ERROR": 40,
        "CRITICAL": 50,
    }

    level = level.upper()
    if level == "TRACE":
        sys.stderr.write(
            "Contrast Python Agent: TRACE logging is equivalent to DEBUG\n"
        )

    return level_to_int.get(level, level_to_int["INFO"])


def _close_handler():
    handle = module.file_handle
    if handle not in (sys.stderr, sys.stdout, None):
        module.file_handle = None
        handle.close()


def _set_handler(filename: TextIO | str, rotation_config: RotationConfig | None = None):
    if isinstance(filename, str):
        try:
            path = pathlib.Path(filename).parent.resolve()
            os.makedirs(path, exist_ok=True)
            module.file_handle = open(filename, "a", encoding="utf-8")  # noqa: SIM115
            if rotation_config:
                module.file_handle = cast(
                    TextIO, RotatingFile(module.file_handle, rotation_config)
                )

        except Exception as e:
            sys.stderr.write(f"Failed to create log file {filename} - {e}\n")
            module.file_handle = sys.stderr
    elif isinstance(filename, io.TextIOBase):
        module.file_handle = filename
    else:
        raise TypeError(
            "log_file must be a string path to a file or an open TextIOBase object",
            type(filename).__name__,
        )

    return module.file_handle


def init_structlog(
    log_level_name: str,
    log_file: TextIO | str,
    progname: str,
    *,
    # NOTE: We should only enable logger caching if its configuration is finalized. If
    # it's possible for the logging config to change in the future, do not cache it.
    cache_logger: bool = False,
    rotation_config: RotationConfig | None = None,
) -> None:
    """
    Initial configuration for structlog. This can still be modified by subsequent calls
    to structlog.configure.
    """
    log_level = _log_level_to_int(log_level_name)

    _close_handler()
    file_handle = _set_handler(log_file, rotation_config)

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso", key="time"),
            structlog.processors.add_log_level,
            rename_key("event", "msg"),
            structlog.processors.CallsiteParameterAdder(
                [
                    structlog.processors.CallsiteParameter.PROCESS,
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                    structlog.processors.CallsiteParameter.THREAD,
                    structlog.processors.CallsiteParameter.THREAD_NAME,
                ],
                additional_ignores=[
                    "contrast_vendor.structlog",
                    "contrast.utils.decorators",
                ],
            ),
            rename_key("process", "pid"),
            add_request_id,
            add_asyncio_info,
            add_hostname,
            partial(add_progname, progname=progname),
            structlog.processors.format_exc_info,
            structlog.processors.StackInfoRenderer(
                additional_ignores=[
                    "contrast_vendor.structlog",
                    "contrast.utils.decorators",
                ]
            ),
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.WriteLoggerFactory(file_handle),
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        cache_logger_on_first_use=cache_logger,
    )
