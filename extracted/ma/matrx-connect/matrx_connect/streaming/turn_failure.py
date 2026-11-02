"""Injectable turn-failure persister for the streaming layer.

A TURN THAT DIES MUST LEAVE A TRACE THE USER CAN STILL SEE TOMORROW.

The streaming wrapper already emits an honest terminal error on the wire when
the work task crashes. The wire is not durable: reload the page and it is gone.
On 2026-09-12 a stream task died mid-build and the conversation simply ended —
the last persisted row was a tool_result, and nothing after it said why. The
request row still read ``status=completed`` because the crash happened after the
previous iteration finalized and before the orchestrator could reach any
failure path of its own.

THE COMPONENT THAT CATCHES THE CRASH IS THE ONE THAT TERMINALIZES THE TURN.
That is this seam. matrx-connect is Tier-1 and must never learn the chat schema,
so the host injects an async persister exactly the way it injects
``capture_error``; the crash branch calls it with the same honest text it puts
on the wire. When nothing is injected (standalone matrx-connect, tests), the
call is a silent no-op.

Wired from matrx-ai in ``matrx_ai.configure()``:

    from matrx_connect.streaming.turn_failure import configure_turn_failure_persister
    from matrx_ai.db.turn_failure import persist_stream_turn_failure
    configure_turn_failure_persister(persist_stream_turn_failure)
"""

from __future__ import annotations

import asyncio
import logging
import os
from collections.abc import Awaitable, Callable
from typing import Any

logger = logging.getLogger("matrx_connect.streaming.turn_failure")

# An async callable persisting ONE failed assistant row plus the request's
# terminal status. Returns True when something durable landed.
#   await fn(*, conversation_id, request_id, user_id, error_type, message,
#            user_message, route)
TurnFailurePersistFn = Callable[..., Awaitable[bool]]

_persist_fn: TurnFailurePersistFn | None = None
_allow_in_tests = False


def configure_turn_failure_persister(
    fn: TurnFailurePersistFn | None,
    *,
    allow_in_tests: bool = False,
) -> None:
    """Inject the host persister; live writes stay disabled under pytest."""
    global _allow_in_tests, _persist_fn
    _persist_fn = fn
    _allow_in_tests = allow_in_tests if fn is not None else False


def is_turn_failure_persister_configured() -> bool:
    return _persist_fn is not None


async def persist_turn_failure(
    *,
    conversation_id: str | None,
    request_id: str | None,
    user_id: str | None,
    error_type: str,
    message: str,
    user_message: str,
    route: str,
    **extra: Any,
) -> bool:
    """Best-effort durable trace of a dead turn. NEVER raises.

    Shielded, because we are called from a crash path that may itself be racing
    a cancellation — the whole point is that this write survives the thing that
    killed the turn.

    Returns True when the host reports something durable landed. A False (or a
    raise from the host) SCREAMS ONCE and leaves the wire message as the only
    surviving notice: that is the one acceptable residue when the database is
    unreachable at the exact moment we need it, and it is loud so nobody mistakes
    it for a turn that merely ended.
    """
    fn = _persist_fn
    if fn is None:
        return False
    if not conversation_id:
        # Nothing to attach the row to. A conversation-less stream (a utility
        # route, a tool probe) has no transcript that could lie about it.
        return False
    if "PYTEST_CURRENT_TEST" in os.environ and not _allow_in_tests:
        logger.warning("turn_failure_persist_blocked_in_test", extra={"route": route})
        return False
    try:
        persisted = await asyncio.shield(
            fn(
                conversation_id=conversation_id,
                request_id=request_id,
                user_id=user_id,
                error_type=error_type,
                message=message,
                user_message=user_message,
                route=route,
                **extra,
            )
        )
    except Exception as exc:  # noqa: BLE001 - the trace must never escalate
        logger.error(
            "turn_failure_persist_failed",
            extra={
                "route": route,
                "request_id": request_id,
                "conversation_id": conversation_id,
                "persist_error": f"{type(exc).__name__}: {exc}",
                "original_error_type": error_type,
                "remedy": (
                    "The user saw the error live but it is NOT in their history: "
                    "the database was unreachable while terminalizing a dead turn. "
                    "Check pool saturation / write latency."
                ),
            },
        )
        return False
    if not persisted:
        logger.error(
            "turn_failure_not_persisted",
            extra={
                "route": route,
                "request_id": request_id,
                "conversation_id": conversation_id,
                "original_error_type": error_type,
                "remedy": (
                    "A dead turn left no durable trace; the wire message is the "
                    "only notice the user ever got. It vanishes on reload."
                ),
            },
        )
    return bool(persisted)
