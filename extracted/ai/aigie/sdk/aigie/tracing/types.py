"""Typed tracing events emitted by all framework adapters.

These dataclasses mirror the wire format the SDK currently pushes to the
platform via aigie._buffer.add(EventType.X, dict). When the platform
adopts OTel they will map onto OTel Span/Resource — keeping these typed
makes that mapping mechanical.

There are four event types corresponding to the four EventType values
used by the platform today:

    SpanCreate   -> EventType.SPAN_CREATE
    SpanComplete -> EventType.SPAN_UPDATE   (semantically: span finished)
    TraceCreate  -> EventType.TRACE_CREATE
    TraceUpdate  -> EventType.TRACE_UPDATE

Conventions:
- datetime fields render as ISO 8601 via datetime.isoformat().
- Enum fields render as their .value string.
- `TraceUpdate.to_dict()` strips optional fields that are None; the wire
  format omits them on minimal updates such as the pause emission.
- `SpanCreate.to_dict()` and `SpanComplete.to_dict()` keep every field
  even when nullable (`parent_id: null` for root spans is part of the
  wire contract). Only the three error fields on SpanComplete are
  stripped when absent — matching the captured baseline.
- `metadata` is a free-form dict the caller fills with framework-specific
  enrichment (langgraph_node, error_detection, etc.). Typed events
  deliberately do not bake those quirks into the schema.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class SpanStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    ERROR = "error"
    PAUSED = "paused"


class SpanType(str, Enum):
    WORKFLOW = "workflow"
    CHAIN = "chain"
    NODE = "node"
    LLM = "llm"
    TOOL = "tool"
    RETRIEVER = "retriever"


@dataclass
class SpanCreate:
    """Event published when a span begins. Maps to EventType.SPAN_CREATE."""

    id: str
    trace_id: str
    parent_id: str | None
    name: str
    type: SpanType
    input: Any
    start_time: datetime
    created_at: datetime
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "trace_id": self.trace_id,
            "parent_id": self.parent_id,
            "name": self.name,
            "type": self.type.value,
            "input": self.input,
            "metadata": dict(self.metadata),
            "start_time": self.start_time.isoformat(),
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class SpanComplete:
    """Event published when a span finishes. Maps to EventType.SPAN_UPDATE.

    The wire format calls this SPAN_UPDATE for legacy reasons; semantically
    it is the completion event (success or error). Carries final status,
    output, timing, and (when applicable) error fields. Error spans set
    `error`, `error_message`, and `error_type` side by side — that
    triplication mirrors what the platform consumes today.
    """

    id: str
    trace_id: str
    parent_id: str | None
    name: str
    type: SpanType
    status: SpanStatus
    start_time: datetime
    end_time: datetime
    input: Any
    output: Any
    duration_ns: int
    latency_seconds: float
    total_tokens: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    error_message: str | None = None
    error_type: str | None = None

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "id": self.id,
            "trace_id": self.trace_id,
            "name": self.name,
            "type": self.type.value,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "input": self.input,
            "output": self.output,
            "metadata": dict(self.metadata),
            "status": self.status.value,
            "duration_ns": self.duration_ns,
            "parent_id": self.parent_id,
            "latency_seconds": self.latency_seconds,
            "total_tokens": self.total_tokens,
        }
        if self.error is not None:
            out["error"] = self.error
        if self.error_message is not None:
            out["error_message"] = self.error_message
        if self.error_type is not None:
            out["error_type"] = self.error_type
        return out


@dataclass
class TraceCreate:
    """Event published when a trace begins. Maps to EventType.TRACE_CREATE."""

    id: str
    name: str
    status: SpanStatus
    metadata: dict[str, Any] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    spans: list[Any] = field(default_factory=list)
    environment: str = "default"

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.value,
            "metadata": dict(self.metadata),
            "tags": list(self.tags),
            "spans": list(self.spans),
            "environment": self.environment,
        }


@dataclass
class TraceUpdate:
    """Event published when a trace finishes. Maps to EventType.TRACE_UPDATE.

    Used for both success and failure outcomes. Optional fields are
    stripped from to_dict() when None to match the historical payload
    shape (e.g. the brief `{"id": ..., "status": "paused"}` update emitted
    on interrupt).
    """

    id: str
    status: SpanStatus
    end_time: datetime | None = None
    error: str | None = None
    error_message: str | None = None
    error_type: str | None = None
    execution_data: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"id": self.id, "status": self.status.value}
        if self.end_time is not None:
            out["end_time"] = self.end_time.isoformat()
        if self.error is not None:
            out["error"] = self.error
        if self.error_message is not None:
            out["error_message"] = self.error_message
        if self.error_type is not None:
            out["error_type"] = self.error_type
        if self.execution_data is not None:
            out["execution_data"] = self.execution_data
        if self.metadata:
            out["metadata"] = dict(self.metadata)
        return out
