"""Agent traces: the request a client in any language sends to record its agent calls."""

from .spans import MAX_TRACE_ID_CHARS, MAX_TRACE_NAME_CHARS, GenericTraceSpan, MastraSpan
from .traces import (
    MAX_TRACE_BODY_BYTES,
    MAX_TRACE_SPANS_PER_REQUEST,
    PROBE_CLIENT_HEADER,
    TRACE_PROTOCOL_VERSION,
    TRACE_SOURCE_ATTRIBUTE,
    TraceBatch,
    TraceBatchResult,
    TraceSourceName,
    TraceSpanStatus,
    TraceSpanType,
)

__all__ = [
    "MAX_TRACE_BODY_BYTES",
    "MAX_TRACE_ID_CHARS",
    "MAX_TRACE_NAME_CHARS",
    "MAX_TRACE_SPANS_PER_REQUEST",
    "PROBE_CLIENT_HEADER",
    "TRACE_PROTOCOL_VERSION",
    "TRACE_SOURCE_ATTRIBUTE",
    "GenericTraceSpan",
    "MastraSpan",
    "TraceBatch",
    "TraceBatchResult",
    "TraceSourceName",
    "TraceSpanStatus",
    "TraceSpanType",
]
