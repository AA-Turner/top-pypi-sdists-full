"""Framework-agnostic tracing primitives."""

from aigie.tracing.emitter import TraceEmitter, TracingSink
from aigie.tracing.recorder import SpanRecorder
from aigie.tracing.types import (
    SpanComplete,
    SpanCreate,
    SpanStatus,
    SpanType,
    TraceCreate,
    TraceUpdate,
)

__all__ = [
    "SpanComplete",
    "SpanCreate",
    "SpanRecorder",
    "SpanStatus",
    "SpanType",
    "TraceCreate",
    "TraceEmitter",
    "TraceUpdate",
    "TracingSink",
]
