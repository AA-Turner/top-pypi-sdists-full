"""Smpl Logging SDK module — wraps generated logging client.

``LoggingClient`` / ``AsyncLoggingClient`` are re-exported from the top-level
``smplkit`` package only (alongside ``ConfigClient`` / ``FlagsClient``), not
from here.
"""

from __future__ import annotations

from smplkit.logging.clients import (
    AsyncLogGroupsClient,
    AsyncLoggersClient,
    LogGroupsClient,
    LoggersClient,
)
from smplkit.logging.sources import LoggerSource
from smplkit.logging.adapters.base import LoggingAdapter
from smplkit.logging.adapters.stdlib_logging import StdlibLoggingAdapter
from smplkit.logging.models import (
    AsyncSmplLogGroup,
    AsyncSmplLogger,
    LoggerEnvironment,
    SmplLogGroup,
    SmplLogger,
)

__all__ = [
    "AsyncLogGroupsClient",
    "AsyncLoggersClient",
    "AsyncSmplLogGroup",
    "AsyncSmplLogger",
    "LogGroupsClient",
    "LoggerEnvironment",
    "LoggerSource",
    "LoggersClient",
    "LoggingAdapter",
    "SmplLogGroup",
    "SmplLogger",
    "StdlibLoggingAdapter",
]
