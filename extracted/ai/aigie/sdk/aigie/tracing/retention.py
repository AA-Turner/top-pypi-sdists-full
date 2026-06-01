"""Zero-retention switch for the framework ABC.

A single ContextVar gates whether the L1 emission substrate sends spans to
the wire. The L2 lifecycle bridge gates trace creation on the same flag.
Both `no_retention()` (sync) and `no_retention_async()` (async) flip the var
on enter and restore it on exit, including on exception. ContextVar (not
thread-local) so asyncio task fan-out via copy_context() isolates suppressed
tasks from concurrent unsuppressed siblings.
"""

from __future__ import annotations

from contextlib import asynccontextmanager, contextmanager
from contextvars import ContextVar

import aigie.telemetry as _telemetry

_retention_suppressed: ContextVar[bool] = ContextVar("_aigie_retention_suppressed", default=False)

_meter = _telemetry.get_meter("aigie.tracing")
_scopes_entered = _meter.create_counter(
    "aigie.tracing.zero_retention.scopes_entered",
    description="Number of aigie.no_retention() scopes entered.",
)


def is_retention_suppressed() -> bool:
    """True when the current task is inside a no_retention scope."""
    return _retention_suppressed.get()


@contextmanager
def no_retention():
    """Suppress all span/trace emission for the duration of the scope.

    Aigie still runs in-process (drift detection, guardrails, remediation
    decisions); only persistence to the backend is skipped. Nested scopes
    are idempotent.
    """
    _scopes_entered.add(1)
    token = _retention_suppressed.set(True)
    try:
        yield
    finally:
        _retention_suppressed.reset(token)


@asynccontextmanager
async def no_retention_async():
    """Async counterpart of `no_retention()` for async-only call sites."""
    _scopes_entered.add(1)
    token = _retention_suppressed.set(True)
    try:
        yield
    finally:
        _retention_suppressed.reset(token)
