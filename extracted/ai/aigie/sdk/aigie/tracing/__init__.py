"""Framework-agnostic tracing primitives."""

from aigie.tracing.emitter import TraceEmitter, TracingSink
from aigie.tracing.types import (
    Span,
    SpanStatus,
    SpanType,
)

__all__ = [
    "Span",
    "SpanStatus",
    "SpanType",
    "TraceEmitter",
    "TracingSink",
]
