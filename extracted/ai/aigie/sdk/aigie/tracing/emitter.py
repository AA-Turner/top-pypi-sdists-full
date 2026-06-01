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

Pre-send hooks: callers may register ``SpanCompleteHook`` callables via
:meth:`TraceEmitter.register_span_complete_hook`. Each hook receives the
dict payload that is about to hit the buffer for span-completion events
(both the typed ``emit_span_complete*`` path and the dict-shape
``emit_raw_sync(SPAN_UPDATE, ...)`` path used by LangGraph). Hooks may
mutate the dict in place. Hook exceptions are logged and swallowed so a
buggy hook cannot break tracing.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import TYPE_CHECKING, Protocol

from aigie.buffer import EventType

if TYPE_CHECKING:
    from aigie.client import Aigie
    from aigie.tracing.types import (
        SpanComplete,
        SpanCreate,
        TraceCreate,
        TraceUpdate,
    )

logger = logging.getLogger(__name__)

SpanCompleteHook = Callable[[dict], None]


class TracingSink(Protocol):
    """Structural interface for tracing destinations.

    Each event type has an async method (used from native async paths)
    and a sync method (used from LangChain on_*_end callbacks, which
    are invoked from the framework's synchronous callback dispatcher).
    """

    async def emit_span_create(self, span: SpanCreate) -> None: ...
    async def emit_span_complete(self, span: SpanComplete) -> None: ...
    async def emit_trace_create(self, trace: TraceCreate) -> None: ...
    async def emit_trace_update(self, update: TraceUpdate) -> None: ...

    def emit_span_create_sync(self, span: SpanCreate) -> None: ...
    def emit_span_complete_sync(self, span: SpanComplete) -> None: ...
    def emit_trace_create_sync(self, trace: TraceCreate) -> None: ...
    def emit_trace_update_sync(self, update: TraceUpdate) -> None: ...


class TraceEmitter:
    """Concrete TracingSink that publishes events to `aigie._buffer`.

    Defensive: if the buffer is unavailable (client not initialized, or
    teardown in progress), emissions are silently dropped. The contract
    is fire-and-forget — adapters never await the platform's response.
    """

    def __init__(self, aigie: Aigie) -> None:
        self._aigie = aigie
        self._span_complete_hooks: list[SpanCompleteHook] = []

    def register_span_complete_hook(self, hook: SpanCompleteHook) -> None:
        """Register a callable invoked with each span-completion dict before emission."""
        self._span_complete_hooks.append(hook)

    def _run_span_complete_hooks(self, payload: dict) -> None:
        for hook in self._span_complete_hooks:
            try:
                hook(payload)
            except Exception:
                logger.exception("span_complete hook failed; continuing")

    # --- async ---------------------------------------------------------

    async def emit_span_create(self, span: SpanCreate) -> None:
        buf = self._aigie._buffer
        if buf is None:
            return
        await buf.add(EventType.SPAN_CREATE, span.to_dict())

    async def emit_span_complete(self, span: SpanComplete) -> None:
        buf = self._aigie._buffer
        if buf is None:
            return
        payload = span.to_dict()
        self._run_span_complete_hooks(payload)
        await buf.add(EventType.SPAN_UPDATE, payload)

    async def emit_trace_create(self, trace: TraceCreate) -> None:
        buf = self._aigie._buffer
        if buf is None:
            return
        await buf.add(EventType.TRACE_CREATE, trace.to_dict())

    async def emit_trace_update(self, update: TraceUpdate) -> None:
        buf = self._aigie._buffer
        if buf is None:
            return
        await buf.add(EventType.TRACE_UPDATE, update.to_dict())

    # --- sync (for LangChain on_*_end callbacks) -----------------------

    def emit_span_create_sync(self, span: SpanCreate) -> None:
        buf = self._aigie._buffer
        if buf is None:
            return
        buf.add_sync(EventType.SPAN_CREATE, span.to_dict())

    def emit_span_complete_sync(self, span: SpanComplete) -> None:
        buf = self._aigie._buffer
        if buf is None:
            return
        payload = span.to_dict()
        self._run_span_complete_hooks(payload)
        buf.add_sync(EventType.SPAN_UPDATE, payload)

    def emit_trace_create_sync(self, trace: TraceCreate) -> None:
        buf = self._aigie._buffer
        if buf is None:
            return
        buf.add_sync(EventType.TRACE_CREATE, trace.to_dict())

    def emit_trace_update_sync(self, update: TraceUpdate) -> None:
        buf = self._aigie._buffer
        if buf is None:
            return
        buf.add_sync(EventType.TRACE_UPDATE, update.to_dict())

    # --- raw dict pass-through ----------------------------------------
    # Used by callbacks that already produce the wire-shape dict (e.g.
    # AigieCallbackHandler's denormalized payload). Bridges typed-event
    # consumers and dict-producing callers without each reaching into
    # `aigie._buffer` directly.

    def emit_raw_sync(self, event_type: EventType, payload: dict) -> None:
        buf = self._aigie._buffer
        if buf is None:
            return
        if event_type == EventType.SPAN_UPDATE:
            self._run_span_complete_hooks(payload)
        buf.add_sync(event_type, payload)
