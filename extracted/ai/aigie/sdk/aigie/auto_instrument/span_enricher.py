"""Thread-keyed active trace/span context for the OTel bridge.

The infra-enrichment subsystem (OTel span capture → trace-metadata events)
was removed with the single-immutable-span migration: its only sink was a
``TRACE_UPDATE`` that the transport already dropped. What remains here is the
small thread-context API that framework callbacks use to record the active
Aigie trace/span id for the current thread.
"""

from __future__ import annotations

import threading

# Thread-keyed context for frameworks that dispatch to thread pools. Keyed by
# thread id so concurrent agents in different threads don't collide.
_thread_traces: dict[int, str] = {}  # thread_id -> trace_id
_thread_spans: dict[int, str] = {}  # thread_id -> span_id
_thread_ctx_lock = threading.Lock()


def set_active_trace_id(trace_id: str | None, span_id: str | None = None) -> None:
    """Set the trace/span ids for the current thread.

    Thread-keyed: concurrent agents in different threads won't collide.
    Called by framework auto-instruments when a trace starts.
    """
    tid = threading.get_ident()
    with _thread_ctx_lock:
        if trace_id:
            _thread_traces[tid] = trace_id
        else:
            _thread_traces.pop(tid, None)
        if span_id:
            _thread_spans[tid] = span_id
        else:
            _thread_spans.pop(tid, None)


def set_active_span_id(span_id: str | None) -> None:
    """Update the current span id for the current thread."""
    tid = threading.get_ident()
    with _thread_ctx_lock:
        if span_id:
            _thread_spans[tid] = span_id
        else:
            _thread_spans.pop(tid, None)
