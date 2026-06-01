"""Smpl Logging SDK module — wraps generated logging client."""

from __future__ import annotations

from smplkit.logging._sources import LoggerSource
from smplkit.logging.adapters.base import LoggingAdapter
from smplkit.logging.adapters.stdlib_logging import StdlibLoggingAdapter
from smplkit.logging.client import (
    AsyncLoggingClient,
    LoggingClient,
)
from smplkit.logging.models import (
    AsyncSmplLogGroup,
    AsyncSmplLogger,
    SmplLogGroup,
    SmplLogger,
)

__all__ = [
    "AsyncLoggingClient",
    "AsyncSmplLogGroup",
    "AsyncSmplLogger",
    "LoggerSource",
    "LoggingAdapter",
    "LoggingClient",
    "SmplLogGroup",
    "SmplLogger",
    "StdlibLoggingAdapter",
]
