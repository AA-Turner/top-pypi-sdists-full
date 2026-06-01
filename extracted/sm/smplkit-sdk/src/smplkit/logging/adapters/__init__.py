"""Pluggable logging framework adapters."""

from __future__ import annotations

from smplkit.logging.adapters.base import LoggingAdapter
from smplkit.logging.adapters.stdlib_logging import StdlibLoggingAdapter

__all__ = [
    "LoggingAdapter",
    "LoguruAdapter",
    "StdlibLoggingAdapter",
]


def __getattr__(name: str) -> object:
    # Lazy import LoguruAdapter so that importing the package doesn't
    # require loguru to be installed.
    if name == "LoguruAdapter":
        from smplkit.logging.adapters.loguru_adapter import LoguruAdapter

        return LoguruAdapter
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
