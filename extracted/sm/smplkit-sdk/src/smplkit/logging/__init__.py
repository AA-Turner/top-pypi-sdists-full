"""Smpl Logging SDK module — wraps generated logging client.

``LoggingClient`` / ``AsyncLoggingClient`` are re-exported from the top-level
``smplkit`` package only (alongside ``ConfigClient`` / ``FlagsClient``), not
from here.
"""

from __future__ import annotations

from smplkit.logging.adapters.base import LoggingAdapter
from smplkit.logging.adapters.stdlib_logging import StdlibLoggingAdapter
from smplkit.logging.clients import (
    AsyncLoggersClient,
    AsyncLogGroupsClient,
    LoggersClient,
    LogGroupsClient,
)
from smplkit.logging.models import (
    AsyncSmplLogger,
    AsyncSmplLogGroup,
    LoggerEnvironment,
    SmplLogger,
    SmplLogGroup,
)
from smplkit.logging.sources import LoggerSource

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
