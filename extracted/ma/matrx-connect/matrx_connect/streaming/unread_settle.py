"""Host-injected hook: a stream's run settled while NOBODY was reading it.

A detached stream keeps working after its reader leaves (a disconnect never
stops server work). When that work finishes — or fails — with no reader on the
wire, the person who started it has not seen the result. matrx-connect knows
WHEN that happens (the END frame was published with no primary reader and no
replay subscriber attached, and the run then settled ``completed`` or
``failed``); the host decides WHAT to do about it (aidream: tell the person
their chat reply is ready). Same seam shape as ``run_tracking`` and
``journal``.

Contract:

* Fires at most ONCE per stream (the emitter owns the claim), only for the
  outcomes ``completed`` and ``failed``. A ``cancelled`` run (the person
  stopped it) and an abandoned one (process shutdown) never fire.
* "Unread" is judged at the moment the END frame is published, so a reader
  that received END and then hung up never counts as absent. Readers on
  ANOTHER process (cross-replica rejoin through the host journal) are
  invisible here; a host that cares checks its own read marks.
* No hook installed (the default, and every package-only consumer): nothing
  happens.
* The hook's own failure is captured through ``capture_error`` (kind
  ``unread_settle_hook_failed``) and never reaches the stream or the run.
"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

from matrx_utils import vcprint

from matrx_connect.context.app_context import AppContext
from matrx_connect.streaming.error_capture import capture_error
from matrx_connect.streaming.run_tracking import STREAM_RUN_COMPLETED, STREAM_RUN_FAILED

#: The outcomes that announce. ``cancelled`` is the person's own Stop; an
#: abandoned run (shutdown) has no outcome at all.
UNREAD_SETTLE_OUTCOMES = frozenset({STREAM_RUN_COMPLETED, STREAM_RUN_FAILED})


@dataclass(frozen=True)
class RunSettledUnread:
    """What the host hook receives. Every identity field is READ from the
    context the stream ran under — carried, never rebuilt."""

    #: ``completed`` | ``failed``.
    outcome: str
    request_id: str | None
    user_id: str | None
    organization_id: str | None
    conversation_id: str | None
    #: The route's log label (never an identity — do not branch on it).
    debug_label: str
    #: The full context the stream ran under (store, system_run, source_app,
    #: source_feature, auth flags …) so the host decides what kind of run it was.
    context: AppContext
    #: The request's opaque host metadata (a read-only copy of ``context.metadata``).
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))


RunSettledUnreadHook = Callable[[RunSettledUnread], Awaitable[None]]

_hook: RunSettledUnreadHook | None = None


def configure_run_settled_unread(hook: RunSettledUnreadHook | None) -> None:
    """Install the host's hook once at startup; ``None`` removes it (no-op default)."""
    global _hook
    _hook = hook


def run_settled_unread_configured() -> bool:
    return _hook is not None


async def announce_run_settled_unread(
    emitter: Any,
    ctx: AppContext,
    outcome: str | None,
    debug_label: str,
) -> bool:
    """Call the host hook when this stream's run settled while unread.

    Returns True when the hook was called. Never raises (a cancel propagates).
    """
    hook = _hook
    if hook is None or outcome not in UNREAD_SETTLE_OUTCOMES:
        return False
    claim = getattr(emitter, "claim_unread_settle", None)
    if not callable(claim) or not claim():
        return False
    payload = RunSettledUnread(
        outcome=outcome,
        request_id=str(ctx.request_id) if ctx.request_id else None,
        user_id=str(ctx.user_id) if ctx.user_id else None,
        organization_id=str(ctx.organization_id) if ctx.organization_id else None,
        conversation_id=str(ctx.conversation_id) if ctx.conversation_id else None,
        debug_label=debug_label,
        context=ctx,
        metadata=MappingProxyType(dict(ctx.metadata or {})),
    )
    try:
        await hook(payload)
    except asyncio.CancelledError:
        raise
    except Exception as exc:  # noqa: BLE001 - the stream and its run never pay for the hook
        vcprint(
            f"[{debug_label}] unread-settle hook raised: {type(exc).__name__}: {exc}",
            color="red",
        )
        try:
            await capture_error(
                exc,
                kind="unread_settle_hook_failed",
                request_id=payload.request_id,
                user_id=payload.user_id,
                conversation_id=payload.conversation_id,
                route=debug_label,
                context={"outcome": outcome, "debug_label": debug_label},
            )
        except Exception:  # noqa: BLE001
            pass
    return True


__all__ = [
    "RunSettledUnread",
    "RunSettledUnreadHook",
    "UNREAD_SETTLE_OUTCOMES",
    "announce_run_settled_unread",
    "configure_run_settled_unread",
    "run_settled_unread_configured",
]
