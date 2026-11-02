"""
act (`/v1/act`) — the robotics surface: the `Policy` and its two calls (observe, act). This is the one endpoint with a
lifecycle (a kept-open connection), because a robot observes and acts continuously; the other surfaces (chat / decide)
are one-shot calls.

`connect()` lives at the package top level rather than here because it is the primary entry point
the whole SDK is organised around; it constructs a `Policy` from this package.
"""

from __future__ import annotations

from .policy import Policy
from .types import Ready
from .waits import Interrupted

__all__ = [
    "Policy",
    "Interrupted",
    "Ready",
]
