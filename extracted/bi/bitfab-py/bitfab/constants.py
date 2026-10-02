"""Constants for the Bitfab SDK."""

from __future__ import annotations

from contextvars import ContextVar
from importlib.metadata import PackageNotFoundError, version
from typing import Any

# Default service URL for Bitfab API
DEFAULT_SERVICE_URL = "https://bitfab.ai"

# Get SDK version from installed package metadata
try:
    __version__ = version("bitfab-py")
except PackageNotFoundError:
    __version__ = "unknown"

_replay_context: ContextVar[dict[str, Any] | None] = ContextVar(
    "bitfab_replay_context", default=None
)

# Set by ``Bitfab.seed_trace`` for the duration of the one call it records:
# carries the trace id the call's root span adopts, and tells the span
# decorators to record even when capture is off.
_seed_context: ContextVar[dict[str, Any] | None] = ContextVar(
    "bitfab_seed_context", default=None
)

# Set by thread_propagation's dispatch wrapper for the duration of a carried
# callable: identifies the thread that called submit()/start(), so spans
# created on the worker can record where the work was handed off.
_submit_origin: ContextVar[dict[str, Any] | None] = ContextVar(
    "bitfab_submit_origin", default=None
)
