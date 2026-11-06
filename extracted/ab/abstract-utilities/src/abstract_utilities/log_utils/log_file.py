from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys
import os
from .imports import LevelFilter, SafeFormatter
PACKAGE_NAME = "abstract_utilities"

# ─────────────────────────────────────────────────────────────
# Formatting
# ─────────────────────────────────────────────────────────────

LOG_FORMAT = (
    "[%(asctime)s] "
    "%(levelname)-8s "
    "%(name)s:%(lineno)d | "
    "%(message)s "
    "[target=%(target_file)s:%(target_line)s]"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class CallerAwareLogger(logging.Logger):
    """
    Logger that reports the first frame outside logging + abstract utilities.
    """

    def findCaller(self, stack_info=False, stacklevel=1):
        import inspect

        frame = inspect.currentframe().f_back  # ← critical fix

        while frame:
            code = frame.f_code
            filename = code.co_filename

            if not (
                "logging" in filename
                or "log_utils" in filename
                or "abstract_utilities" in filename
            ):
                return (
                    filename,
                    frame.f_lineno,
                    code.co_name,
                    None,
                )

            frame = frame.f_back

        return super().findCaller(stack_info, stacklevel)

# ─────────────────────────────────────────────────────────────
# Stack-aware logger
# ─────────────────────────────────────────────────────────────

class StackAwareLogger(logging.Logger):
    """
    Logger that automatically skips itself when reporting
    filename / line number.
    """

    _STACKLEVEL = 2

    def debug(self, msg, *args, **kwargs):
        kwargs.setdefault("stacklevel", self._STACKLEVEL)
        super().debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        kwargs.setdefault("stacklevel", self._STACKLEVEL)
        super().info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        kwargs.setdefault("stacklevel", self._STACKLEVEL)
        super().warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        kwargs.setdefault("stacklevel", self._STACKLEVEL)
        super().error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        kwargs.setdefault("stacklevel", self._STACKLEVEL)
        super().exception(msg, *args, **kwargs)


# Ensure our logger class is used globally (safe once)
logging.setLoggerClass(StackAwareLogger)


# ─────────────────────────────────────────────────────────────
# Logger factory — single implementation in abstract_essentials
# ─────────────────────────────────────────────────────────────
# get_logFile, the level helpers and the log directory used to be a second copy
# here (stdout console, import-time directory creation, `level` that only ever hid
# DEBUG, ignored re-calls). abstract_essentials owns the one implementation now;
# these names stay importable from abstract_utilities.
from .imports import (  # noqa: E402
    LOG_ROOT,
    get_logFile,
    get_log_dir,
    set_logger_level,
    is_logger_level_enabled,
    _level_filters,
)

__all__ = [
    "LOG_FORMAT", "DATE_FORMAT", "LOG_ROOT", "PACKAGE_NAME",
    "CallerAwareLogger", "StackAwareLogger",
    "get_logFile", "get_log_dir", "set_logger_level", "is_logger_level_enabled",
]
