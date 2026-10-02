from __future__ import annotations

import threading
from collections import OrderedDict
from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass
class _State:
    span_ids: set[str] = field(default_factory=set)
    active: set[str] = field(default_factory=set)
    complete: Callable[[int], None] | None = None


class TraceCompletion:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._traces: dict[str, _State] = {}
        self._closed: OrderedDict[str, int] = OrderedDict()

    def start(self, trace_id: str, span_id: str) -> None:
        with self._lock:
            if trace_id in self._closed:
                return
            state = self._traces.setdefault(trace_id, _State())
            state.span_ids.add(span_id)
            state.active.add(span_id)

    def open(self, trace_id: str) -> None:
        with self._lock:
            if trace_id not in self._closed:
                self._traces.setdefault(trace_id, _State())

    def hold(self, trace_id: str, key: str) -> None:
        with self._lock:
            self._traces.setdefault(trace_id, _State()).active.add(key)

    def record(self, trace_id: str, span_id: str) -> None:
        with self._lock:
            if trace_id not in self._closed:
                self._traces.setdefault(trace_id, _State()).span_ids.add(span_id)

    def end(self, trace_id: str, span_id: str) -> None:
        with self._lock:
            state = self._traces.get(trace_id)
            if state is None:
                return
            state.active.discard(span_id)
            ready = self._drain(trace_id, state)
        if ready is not None:
            ready[0](ready[1])

    def abort(self, trace_id: str, span_id: str) -> bool:
        with self._lock:
            state = self._traces.get(trace_id)
            if state is None:
                return False
            state.active.discard(span_id)
            state.span_ids.discard(span_id)
            if not state.active and not state.span_ids and state.complete is None:
                del self._traces[trace_id]
                return True
            ready = self._drain(trace_id, state)
        if ready is not None:
            ready[0](ready[1])
        return True

    def close(
        self, trace_id: str, complete: Callable[[int], None], dropped: bool = False
    ) -> None:
        with self._lock:
            if trace_id in self._closed:
                ready = (complete, self._closed[trace_id])
            else:
                state = self._traces.get(trace_id)
                if state is None:
                    ready = None
                else:
                    state.complete = complete
                    if dropped:
                        state.active.clear()
                    ready = self._drain(trace_id, state)
        if ready is not None:
            ready[0](ready[1])

    def _drain(
        self, trace_id: str, state: _State
    ) -> tuple[Callable[[int], None], int] | None:
        if state.active or state.complete is None:
            return None
        del self._traces[trace_id]
        count = len(state.span_ids)
        self._closed[trace_id] = count
        if len(self._closed) > 1024:
            self._closed.popitem(last=False)
        return state.complete, count
