"""TraceBatch: one request of an agent's raw trace spans (`POST /v1/runs/{run}/traces`), the
model the server and the client checker both validate with."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from ..compat import StrEnum

#: The trace client protocol version a client names in its `Probe-Client` header.
TRACE_PROTOCOL_VERSION = 1
#: `<language>/<protocol version>`, e.g. `typescript/1`: lets the server count refusals per client.
PROBE_CLIENT_HEADER = "Probe-Client"
#: Raw spans per request; past it the server answers 413 and the client splits parent-first.
MAX_TRACE_SPANS_PER_REQUEST = 1_000
#: Request body bytes; past it the server answers 413 and the client splits parent-first.
MAX_TRACE_BODY_BYTES = 4 * 1024 * 1024
#: The rollout attribute naming the source that wrote a trial; such trials get no LLM description.
TRACE_SOURCE_ATTRIBUTE = "trace_source"


class TraceSourceName(StrEnum):
    """The framework whose raw spans a batch carries."""

    #: Mastra's exported spans (`@mastra/observability`), sent as the exporter receives them.
    MASTRA = "mastra"
    #: Spans already shaped as rollout / turn / tool_call (`GenericTraceSpan`).
    GENERIC = "generic"


class TraceSpanType(StrEnum):
    """The span tree the trial page draws: a rollout holds turns, a turn holds tool calls."""

    ROLLOUT = "rollout"
    TURN = "turn"
    TOOL_CALL = "tool_call"


class TraceSpanStatus(StrEnum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class TraceBatch(BaseModel):
    """Raw spans of one or more traces. A trace is one agent call and becomes one trial."""

    source: TraceSourceName
    #: The framework's own version (e.g. `@mastra/core` 1.81.0), kept on the trial.
    source_version: str | None = Field(default=None, max_length=64)
    #: Spans as the source emits them; each source validates its own shape.
    spans: list[dict[str, Any]]


class TraceBatchResult(BaseModel):
    #: Spans written to the run's span tree (raw spans the tree does not keep are not counted).
    upserted: int
    #: The trials (rollout span ids) this batch wrote to, one per trace.
    trial_ids: list[UUID]
