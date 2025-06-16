# Parts of this class are from the Scanpy equivalent, see license below

# BSD 3-Clause License

# Copyright (c) 2017 F. Alexander Wolf, P. Angerer, Theis Lab
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""Logging and Profiling."""

import logging

# import platform
import sys
from datetime import datetime, timedelta, timezone
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING, getLevelName
from typing import Optional

# sys.stdout inside jupyter doesn't have reconfigure
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="backslashreplace")  # type: ignore


HINT = 15
SAVE = 21
SUCCESS = 25
PRINT = 41  # always print
IMPORTANT = 31  # at warning level
IMPORTANT_HINT = 32  # at warning level
logging.addLevelName(HINT, "HINT")
logging.addLevelName(SAVE, "SAVE")
logging.addLevelName(SUCCESS, "SUCCESS")
logging.addLevelName(PRINT, "PRINT")
logging.addLevelName(IMPORTANT, "IMPORTANT")
logging.addLevelName(IMPORTANT_HINT, "IMPORTANT_HINT")


VERBOSITY_TO_LOGLEVEL = {
    0: "ERROR",  # 40
    1: "WARNING",  # 30
    2: "SUCCESS",  # 25
    3: "INFO",  # 20
    4: "HINT",  # 15
    5: "DEBUG",  # 10
}


LEVEL_TO_ICONS = {
    40: "✗",  # error
    32: "•",  # important hint
    31: "→",  # important
    30: "!",  # warning
    25: "✓",  # success
    21: "✓",  # save
    20: "•",  # info
    15: "•",  # hint
    10: "•",  # debug
}

# Add color codes
LEVEL_TO_COLORS = {
    40: "\033[91m",  # Red for error
    32: "\033[94m",  # Blue for important hint
    31: "\033[92m",  # Green for important
    30: "\033[93m",  # Yellow for warning
    25: "\033[92m",  # Green for success
    21: "\033[92m",  # Green for save
    20: "\033[94m",  # Blue for info
    15: "\033[96m",  # Cyan for hint
    10: "\033[90m",  # Grey for debug
}

RESET_COLOR = "\033[0m"


class RootLogger(logging.RootLogger):
    def __init__(self, level="INFO"):
        super().__init__(level)
        self.propagate = False
        self._verbosity: int = 1
        self.indent = ""
        RootLogger.manager = logging.Manager(self)

    def log(  # type: ignore
        self,
        level: int,
        msg: str,
        *,
        extra: Optional[dict] = None,
        time: datetime = None,
        deep: Optional[str] = None,
    ) -> datetime:
        """Log message with level and return current time.

        Args:
            level: Logging level.
            msg: Message to display.
            time: A time in the past. If this is passed, the time difference from then
                to now is appended to `msg` as ` (HH:MM:SS)`.
                If `msg` contains `{time_passed}`, the time difference is instead
                inserted at that position.
            deep: If the current verbosity is higher than the log function’s level,
                this gets displayed as well
            extra: Additional values you can specify in `msg` like `{time_passed}`.
        """
        now = datetime.now(timezone.utc)
        time_passed: timedelta = None if time is None else now - time  # type: ignore
        extra = {
            **(extra or {}),
            "deep": (
                deep
                if getLevelName(VERBOSITY_TO_LOGLEVEL[self._verbosity]) < level
                else None
            ),
            "time_passed": time_passed,
        }
        msg = f"{self.indent}{msg}"
        super().log(level, msg, extra=extra)
        return now

    def critical(self, msg, *, time=None, deep=None, extra=None) -> datetime:  # type: ignore
        return self.log(CRITICAL, msg, time=time, deep=deep, extra=extra)

    def error(self, msg, *, time=None, deep=None, extra=None) -> datetime:  # type: ignore
        return self.log(ERROR, msg, time=time, deep=deep, extra=extra)

    def warning(self, msg, *, time=None, deep=None, extra=None) -> datetime:  # type: ignore
        return self.log(WARNING, msg, time=time, deep=deep, extra=extra)

    def important(self, msg, *, time=None, deep=None, extra=None) -> datetime:  # type: ignore
        return self.log(IMPORTANT, msg, time=time, deep=deep, extra=extra)

    def important_hint(self, msg, *, time=None, deep=None, extra=None) -> datetime:  # type: ignore
        return self.log(IMPORTANT_HINT, msg, time=time, deep=deep, extra=extra)

    def success(self, msg, *, time=None, deep=None, extra=None) -> datetime:  # type: ignore
        return self.log(SUCCESS, msg, time=time, deep=deep, extra=extra)

    def info(self, msg, *, time=None, deep=None, extra=None) -> datetime:  # type: ignore
        return self.log(INFO, msg, time=time, deep=deep, extra=extra)

    def save(self, msg, *, time=None, deep=None, extra=None) -> datetime:  # type: ignore
        return self.log(SAVE, msg, time=time, deep=deep, extra=extra)

    def hint(self, msg, *, time=None, deep=None, extra=None) -> datetime:  # type: ignore
        return self.log(HINT, msg, time=time, deep=deep, extra=extra)

    def debug(self, msg, *, time=None, deep=None, extra=None) -> datetime:  # type: ignore
        return self.log(DEBUG, msg, time=time, deep=deep, extra=extra)

    def print(self, msg, *, time=None, deep=None, extra=None) -> datetime:  # type: ignore
        return self.log(PRINT, msg, time=time, deep=deep, extra=extra)

    # backward compat
    def download(self, msg, *, time=None, deep=None, extra=None) -> datetime:  # type: ignore
        return self.log(SAVE, msg, time=time, deep=deep, extra=extra)


class _LogFormatter(logging.Formatter):
    def __init__(
        self, fmt="{levelname}: {message}", datefmt="%Y-%m-%d %H:%M", style="{"
    ):
        super().__init__(fmt, datefmt, style)

    def base_format(self, record: logging.LogRecord):
        # if platform.system() == "Windows":
        #     return f"{record.levelname}:" + " {message}"
        # else:
        if LEVEL_TO_ICONS.get(record.levelno) is not None:
            color = LEVEL_TO_COLORS.get(record.levelno, "")
            icon = LEVEL_TO_ICONS[record.levelno]
            return f"{color}{icon}{RESET_COLOR}" + " {message}"
        else:
            return "{message}"

    def format(self, record: logging.LogRecord):
        format_orig = self._style._fmt
        self._style._fmt = self.base_format(record)
        if record.time_passed:  # type: ignore
            if "{time_passed}" in record.msg:
                record.msg = record.msg.replace(
                    "{time_passed}",
                    record.time_passed,  # type: ignore
                )
            else:
                self._style._fmt += " ({time_passed})"
        if record.deep:  # type: ignore
            record.msg = f"{record.msg}: {record.deep}"  # type: ignore
        result = logging.Formatter.format(self, record)
        self._style._fmt = format_orig
        return result


logger = RootLogger()


def set_handler(logger):
    h = logging.StreamHandler(stream=sys.stdout)
    h.setFormatter(_LogFormatter())
    h.setLevel(logger.level)
    if len(logger.handlers) == 1:
        logger.removeHandler(logger.handlers[0])
    elif len(logger.handlers) > 1:
        raise RuntimeError("Lamin's root logger somehow got more than one handler")
    logger.addHandler(h)


set_handler(logger)


def set_log_level(logger, level: int):
    logger.setLevel(level)
    (h,) = logger.handlers  # can only be 1
    h.setLevel(level)


# this also sets it for the handler
RootLogger.set_level = set_log_level  # type: ignore


def set_verbosity(logger, verbosity: int):
    if verbosity not in VERBOSITY_TO_LOGLEVEL:
        raise ValueError(
            f"verbosity needs to be one of {set(VERBOSITY_TO_LOGLEVEL.keys())}"
        )
    logger.set_level(VERBOSITY_TO_LOGLEVEL[verbosity])
    logger._verbosity = verbosity


RootLogger.set_verbosity = set_verbosity  # type: ignore


def mute(logger):
    """Context manager to mute logger."""

    class Muted:
        def __enter__(self):
            self.original_verbosity = logger._verbosity
            logger.set_verbosity(0)

        def __exit__(self, exc_type, exc_val, exc_tb):
            logger.set_verbosity(self.original_verbosity)

    return Muted()


RootLogger.mute = mute  # type: ignore
