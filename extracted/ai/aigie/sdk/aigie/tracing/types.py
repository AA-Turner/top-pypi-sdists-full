"""The single immutable span event emitted by all framework adapters.

`Span` mirrors the wire format the SDK pushes to the platform via
aigie._buffer.add(dict). The SDK emits exactly one finalized span event
per span (no create/update split, no separate trace events). When the
platform adopts OTel this maps onto an OTel Span — keeping it typed makes
that mapping mechanical.

Conventions:
- datetime fields render as ISO 8601 via datetime.isoformat().
- Enum fields render as their .value string.
- `Span.to_dict()` keeps every field even when nullable (`parent_id: null`
  for root spans is part of the wire contract). Only the three error
  fields are stripped when absent — matching the captured baseline.
- `metadata` is a free-form dict the caller fills with framework-specific
  enrichment (langgraph_node, error_detection, etc.). The typed event
  deliberately does not bake those quirks into the schema.
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
    INTERRUPTED = "interrupted"


# Span outcomes that must never reach the judge: a paused span re-emits
# finalized (same span_id) on resume/close, an interrupted span never
# completed, and a cancelled one carries only the chunks the caller read
# before walking away — judging any of them would score an incomplete span.
# "cancelled" is a wire status the provider wrappers emit; it has no member
# here yet, which is part of the enum/Literal split tracked separately.
JUDGE_SKIP_STATUSES: frozenset[str] = frozenset(
    {SpanStatus.PAUSED.value, SpanStatus.INTERRUPTED.value, "cancelled"}
)


class SpanType(str, Enum):
    WORKFLOW = "workflow"
    CHAIN = "chain"
    NODE = "node"
    LLM = "llm"
    TOOL = "tool"
    RETRIEVER = "retriever"


@dataclass
class Span:
    """The single finalized span event the SDK emits per span.

    Semantically the completion event (success or error): carries final
    status, output, timing, and (when applicable) error fields. Error spans
    set `error`, `error_message`, and `error_type` side by side — that
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
