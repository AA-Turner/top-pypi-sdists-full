"""Registry for framework rewind capabilities and span handle dispatch."""

from __future__ import annotations

from typing import Any

from aigie.rewind.protocol import (
    Corrective,
    RewindCapability,
    RewindHandle,
    RewindOutcome,
)
from aigie.rewind.store import SpanCheckpointStore


class RewindCoordinator:
    def __init__(self, store: SpanCheckpointStore | None = None) -> None:
        self._capabilities: dict[str, RewindCapability] = {}
        # Empty stores are falsy via __len__; preserve caller-injected stores.
        if store is not None:
            self._store = store
        else:
            self._store = SpanCheckpointStore(on_evict=self._dispatch_evict)

    def _dispatch_evict(self, handle: RewindHandle) -> None:
        """Run capability cleanup after the trace has no live handles."""
        if self._store.has_trace(handle.trace_id):
            return
        capability = self._capabilities.get(handle.framework)
        hook = getattr(capability, "on_evict", None)
        if hook is not None:
            hook(handle)

    def register(self, capability: RewindCapability) -> None:
        self._capabilities[capability.framework] = capability

    async def capture(
        self, framework: str, span_id: str, trace_id: str, context: Any
    ) -> RewindHandle | None:
        capability = self._capabilities.get(framework)
        if capability is None:
            return None
        handle = await capability.capture(span_id, trace_id, context)
        if handle is not None:
            self._store.put(trace_id, span_id, handle)
        return handle

    def record(self, trace_id: str, span_id: str, handle: RewindHandle) -> None:
        """Store a pre-built handle (sync path for callback-driven capture)."""
        self._store.put(trace_id, span_id, handle)

    async def rewind(
        self, trace_id: str, span_id: str, corrective: Corrective | None = None
    ) -> RewindOutcome:
        handle = self._store.get(trace_id, span_id)
        if handle is None:
            return RewindOutcome.not_found(span_id)
        capability = self._capabilities.get(handle.framework)
        if capability is None or not capability.supports(handle):
            return RewindOutcome.unsupported(span_id)
        try:
            return await capability.rewind(handle, corrective)
        except Exception as exc:
            return RewindOutcome.failed(str(exc), handle=handle)

    def evict_trace(self, trace_id: str) -> None:
        self._store.evict_trace(trace_id)
