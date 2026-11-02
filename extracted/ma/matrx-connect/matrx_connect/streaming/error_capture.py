"""Injectable failure-capture hook for the streaming layer.

matrx-connect is Tier-1 and must not import matrx-orm. But the streaming
response wrapper is where request crashes and client-disconnect
cancellations surface — and those are exactly the failures the host wants
to persist into an organized, queryable record (the ``system_error``
table, captured via ``matrx_orm.record_error``).

So the host injects an async capture callable here at startup; the
streaming layer calls it on its crash / cancel branches. When nothing is
injected (standalone matrx-connect, tests), the calls are silent no-ops.

Wired from the host in ``aidream/package_integration.py``:

    from matrx_connect.streaming.error_capture import configure_error_capture
    from matrx_orm import record_error
    configure_error_capture(record_error)
"""

from __future__ import annotations

import asyncio
import logging
import os
from collections.abc import Awaitable, Callable
from typing import Any

logger = logging.getLogger("matrx_connect.streaming.error_capture")

# An async callable matching matrx_orm.record_error's keyword surface:
#   await fn(exc, *, kind, request_id, user_id, conversation_id, agent_id,
#            source_app, route, error_type, error_text, payload, context)
ErrorCaptureFn = Callable[..., Awaitable[None]]

_capture_fn: ErrorCaptureFn | None = None
_allow_in_tests = False


def configure_error_capture(
    fn: ErrorCaptureFn | None,
    *,
    allow_in_tests: bool = False,
) -> None:
    """Inject the host capture coroutine; live writes stay disabled under pytest."""
    global _allow_in_tests, _capture_fn
    _capture_fn = fn
    _allow_in_tests = allow_in_tests if fn is not None else False


def is_error_capture_configured() -> bool:
    return _capture_fn is not None


async def capture_error(exc: BaseException, *, kind: str, **fields: Any) -> None:
    """Best-effort capture. Never raises, never blocks the caller's exit path.

    Shielded so a cancellation that's already in flight (the common case —
    we're usually called FROM a cancel handler) can't interrupt the capture
    write mid-flight.
    """
    fn = _capture_fn
    if fn is None:
        return
    if "PYTEST_CURRENT_TEST" in os.environ and not _allow_in_tests:
        logger.warning(
            "system_error_capture_blocked_in_test",
            extra={"kind": kind},
        )
        return
    try:
        await asyncio.shield(fn(exc, kind=kind, **fields))
    except Exception as cap_exc:
        # The capture must never escalate. Worst case we lose this one record;
        # the stderr log below keeps it greppable.
        logger.error(
            "stream_error_capture_failed",
            extra={
                "kind": kind,
                "capture_error": f"{type(cap_exc).__name__}: {cap_exc}",
                "original_error": f"{type(exc).__name__}: {exc}",
            },
        )
