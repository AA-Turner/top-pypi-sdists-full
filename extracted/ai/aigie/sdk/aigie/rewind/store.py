"""Bounded per-trace span_id -> RewindHandle store for live runs."""

from __future__ import annotations

import contextlib
from collections import OrderedDict
from collections.abc import Callable

from aigie.rewind.protocol import RewindHandle


class SpanCheckpointStore:
    """Bounded per-trace span_id -> RewindHandle store."""

    def __init__(
        self,
        max_per_trace: int = 64,
        max_traces: int = 256,
        *,
        on_evict: Callable[[RewindHandle], None] | None = None,
    ) -> None:
        if max_per_trace < 1:
            raise ValueError("max_per_trace must be >= 1")
        if max_traces < 1:
            raise ValueError("max_traces must be >= 1")
        self._max_per_trace = max_per_trace
        self._max_traces = max_traces
        self._on_evict = on_evict
        self._by_trace: OrderedDict[str, OrderedDict[str, RewindHandle]] = OrderedDict()

    def _evicted(self, handle: RewindHandle) -> None:
        if self._on_evict is None:
            return
        with contextlib.suppress(Exception):
            self._on_evict(handle)

    def put(self, trace_id: str, span_id: str, handle: RewindHandle) -> None:
        spans = self._by_trace.get(trace_id)
        if spans is None:
            spans = OrderedDict()
            self._by_trace[trace_id] = spans
        self._by_trace.move_to_end(trace_id)
        spans.pop(span_id, None)
        spans[span_id] = handle
        while len(spans) > self._max_per_trace:
            _, dropped = spans.popitem(last=False)
            self._evicted(dropped)
        while len(self._by_trace) > self._max_traces:
            _, dropped_spans = self._by_trace.popitem(last=False)
            for dropped in dropped_spans.values():
                self._evicted(dropped)

    def has_trace(self, trace_id: str) -> bool:
        return bool(self._by_trace.get(trace_id))

    def get(self, trace_id: str, span_id: str) -> RewindHandle | None:
        spans = self._by_trace.get(trace_id)
        return spans.get(span_id) if spans is not None else None

    def evict_trace(self, trace_id: str) -> None:
        spans = self._by_trace.pop(trace_id, None)
        if spans is not None:
            for dropped in spans.values():
                self._evicted(dropped)

    def __len__(self) -> int:
        return sum(len(spans) for spans in self._by_trace.values())
