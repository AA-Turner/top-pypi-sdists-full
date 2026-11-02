"""Observability event dataclasses for LangGraph workflow execution.

Defines the shared event envelope and type-specific event payloads
for node executions, LLM calls, and tool calls.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ObservabilityEvent:
    """Shared envelope present on every observability event.

    Attributes:
        version: Schema version (currently 1).
        event_seq: Monotonic per-run sequence starting at 1.
        type: Event discriminator (``"node"``, ``"llm_call"``, ``"tool_call"``).
        run_id: UUID4 identifying the workflow run.
        timestamp: ISO-8601 UTC emission timestamp.
    """

    version: int
    event_seq: int
    type: str
    run_id: str
    timestamp: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dictionary suitable for JSON encoding."""
        return asdict(self)


@dataclass(frozen=True)
class NodeExecutionEvent(ObservabilityEvent):
    """Event emitted for each node execution.

    Attributes:
        node_name: LangGraph node identifier.
        status: ``"success"``, ``"failure"``, or ``"skipped"``.
        start_time: ISO-8601 UTC start timestamp.
        end_time: ISO-8601 UTC end timestamp.
        duration_ms: Wall-clock duration in milliseconds.
        input_summary: Redacted and truncated input data.
        output_summary: Redacted and truncated output data.
        error_class: Classification when status is failure.
        retryable: Whether the error is retryable.
        error_message: Human-readable error detail.
    """

    node_name: str = ""
    status: str = ""
    start_time: str = ""
    end_time: str = ""
    duration_ms: int = 0
    input_summary: Any = None
    output_summary: Any = None
    error_class: str | None = None
    retryable: bool | None = None
    error_message: str | None = None


@dataclass(frozen=True)
class LLMCallEvent(ObservabilityEvent):
    """Event emitted for each LLM provider call.

    Attributes:
        node_name: Owning node identifier.
        node_type: Provider/config context.
        model: Provider model identifier.
        input_tokens: Input token count (None when unavailable).
        output_tokens: Output token count (None when unavailable).
        latency_ms: End-to-end call latency in milliseconds.
        validation_result: Structured output validation outcome.
        estimated_cost_usd: Cost estimate (None for unpriced/missing tokens).
    """

    node_name: str = ""
    node_type: str = ""
    model: str = ""
    input_tokens: int | None = None
    output_tokens: int | None = None
    latency_ms: int = 0
    validation_result: str = ""
    estimated_cost_usd: float | None = None


@dataclass(frozen=True)
class ToolCallEvent(ObservabilityEvent):
    """Event emitted for each tool invocation.

    Attributes:
        node_name: Owning node identifier.
        tool_name: Tool registry name.
        input_params: Redacted and truncated input parameters.
        duration_ms: Wall-clock execution time in milliseconds.
        success: Whether the tool invocation succeeded.
        dry_run: Whether execution was skipped due to dry-run mode.
        mutating: Whether the tool performs side effects.
        tool_result_summary: Truncated result summary.
        error_class: ``"tool"`` when tool execution fails.
    """

    node_name: str = ""
    tool_name: str = ""
    input_params: Any = None
    duration_ms: float = 0.0
    success: bool = True
    dry_run: bool = False
    mutating: bool = False
    tool_result_summary: Any = None
    error_class: str | None = None
