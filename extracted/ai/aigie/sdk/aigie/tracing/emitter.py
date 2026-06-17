"""The single channel adapters use to publish typed tracing events.

`TracingSink` is the structural Protocol — separate from the concrete
`TraceEmitter` because future transports (in-memory sink for tests, an
OTel sink once the platform supports it) will implement the same
interface. Today there is exactly one concrete: `TraceEmitter` writes
to `aigie._buffer`.

The emitter is a thin boundary. It does no transformation — each method
calls `<event>.to_dict()` and pushes to the buffer. Adapters are
responsible for building the typed event with the right fields; the
emitter only ferries it to the wire.

Pre-send hooks: callers may register ``SpanHook`` callables via
:meth:`TraceEmitter.register_span_complete_hook`. Each hook receives the
dict payload that is about to hit the buffer for span-completion events
(both the typed ``emit_span_complete*`` path and the dict-shape
``emit(...)`` path used by LangGraph). Hooks may mutate the dict
in place. Hook exceptions are logged and swallowed so a buggy hook cannot
break tracing.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import TYPE_CHECKING, Protocol

from aigie.tracing.types import JUDGE_SKIP_STATUSES

if TYPE_CHECKING:
    from aigie.client import Aigie
    from aigie.tracing.types import (
        Span,
    )

logger = logging.getLogger(__name__)

SpanHook = Callable[[dict], None]


class TracingSink(Protocol):
    """Structural interface for tracing destinations.

    Each event type has an async method (used from native async paths)
    and a sync method (used from LangChain on_*_end callbacks, which
    are invoked from the framework's synchronous callback dispatcher).
    """

    async def emit_span_complete(self, span: Span) -> None: ...
    def emit_span_complete_sync(self, span: Span) -> None: ...


class TraceEmitter:
    """Concrete TracingSink that publishes events to `aigie._buffer`.

    Defensive: if the buffer is unavailable (client not initialized, or
    teardown in progress), emissions are silently dropped. The contract
    is fire-and-forget — adapters never await the platform's response.
    """

    def __init__(self, aigie: Aigie) -> None:
        self._aigie = aigie
        self._span_complete_hooks: list[SpanHook] = []

    def register_span_complete_hook(self, hook: SpanHook) -> None:
        """Register a callable invoked with each span-completion dict before emission."""
        self._span_complete_hooks.append(hook)

    def _run_span_complete_hooks(self, payload: dict) -> None:
        for hook in self._span_complete_hooks:
            try:
                hook(payload)
            except Exception:
                logger.exception("span_complete hook failed; continuing")

    def _try_fire_evaluate(self, payload: dict) -> bool:
        """Fire EvaluateSpan at emit time so the judge sees the span within
        ~1s of finalization instead of after the next buffer flush. Must run
        AFTER the span-complete hooks (KytteError enrichment). Returns whether
        the fire was scheduled — False leaves the dispatch-time fire in
        charge. Never raises into instrumentation code."""
        if payload.get("status") in JUDGE_SKIP_STATUSES:
            return False
        try:
            return self._aigie._try_fire_evaluate_span(payload) is True
        except Exception:
            logger.exception("emit-time EvaluateSpan hook failed; deferring to flush")
            return False

    # --- async ---------------------------------------------------------

    async def emit_span_complete(self, span: Span) -> None:
        buf = self._aigie._buffer
        if buf is None:
            return
        payload = span.to_dict()
        self._run_span_complete_hooks(payload)
        evaluated = self._try_fire_evaluate(payload)
        await buf.add(payload, evaluated=evaluated)

    # --- sync (for LangChain on_*_end callbacks) -----------------------

    def emit_span_complete_sync(self, span: Span) -> None:
        buf = self._aigie._buffer
        if buf is None:
            return
        payload = span.to_dict()
        self._run_span_complete_hooks(payload)
        evaluated = self._try_fire_evaluate(payload)
        buf.add_sync(payload, evaluated=evaluated)

    # --- raw dict pass-through ----------------------------------------
    # Used by callbacks that already produce the wire-shape dict (e.g.
    # AigieCallbackHandler's denormalized payload). Bridges typed-event
    # consumers and dict-producing callers without each reaching into
    # `aigie._buffer` directly.

    def emit(self, payload: dict) -> None:
        """Publish a finalized span payload (wire-shape dict) to the buffer.

        Runs the span-complete hooks and fires emit-time EvaluateSpan before
        buffering."""
        buf = self._aigie._buffer
        if buf is None:
            return
        self._run_span_complete_hooks(payload)
        evaluated = self._try_fire_evaluate(payload)
        buf.add_sync(payload, evaluated=evaluated)
