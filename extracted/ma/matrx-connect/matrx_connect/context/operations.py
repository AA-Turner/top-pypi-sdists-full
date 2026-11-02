"""Operation lifecycle definitions for init/completion paired events.

Every operation with meaningful duration gets an init + completion pair
tied by operation type and a unique operation_id.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


Operation = Literal[
    "llm_request",
    "tool_execution",
    "user_request",
    "sub_agent",
    "persistence",
]

InitCompletionStatus = Literal["success", "failed", "cancelled"]


class InitPayload(BaseModel):
    model_config = {"extra": "forbid"}
    operation: Operation
    operation_id: str
    parent_operation_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class CompletionPayload(BaseModel):
    model_config = {"extra": "forbid"}
    operation: Operation
    operation_id: str
    status: InitCompletionStatus
    result: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Deeply typed sub-models for total_usage
# ---------------------------------------------------------------------------


class UsageTotals(BaseModel):
    model_config = {"extra": "forbid"}
    input_tokens: int = 0
    output_tokens: int = 0
    cached_input_tokens: int = 0
    total_tokens: int = 0
    total_requests: int = 0
    unique_models: int = 0
    total_cost: float | None = None
    known_cost_subtotal: float = 0.0
    provider_reported_requests: int = 0
    catalog_priced_requests: int = 0
    unknown_cost_requests: int = 0


class ModelUsageSummary(BaseModel):
    model_config = {"extra": "forbid"}
    input_tokens: int = 0
    output_tokens: int = 0
    cached_input_tokens: int = 0
    total_tokens: int = 0
    api: str = ""
    request_count: int = 0
    cost: float | None = 0.0


class AggregatedUsageResult(BaseModel):
    model_config = {"extra": "forbid"}
    by_model: dict[str, ModelUsageSummary] = Field(default_factory=dict)
    total: UsageTotals = Field(default_factory=UsageTotals)


# ---------------------------------------------------------------------------
# Deeply typed sub-models for timing_stats
# ---------------------------------------------------------------------------


class TimingStatsResult(BaseModel):
    model_config = {"extra": "forbid"}
    total_duration: float | None = None
    sum_duration: float | None = None
    api_duration: float | None = None
    tool_duration: float | None = None
    processing_duration: float | None = None
    iterations: int | None = None
    avg_iteration_duration: float | None = None
    # Seconds from request acceptance to the first text or reasoning chunk
    # emitted (time-to-first-token). Absent when no output reached the client.
    first_token_seconds: float | None = None


# ---------------------------------------------------------------------------
# Deeply typed sub-models for tool_call_stats
# ---------------------------------------------------------------------------


class ToolCallByTool(BaseModel):
    model_config = {"extra": "forbid"}
    count: int = 0
    success: int = 0
    error: int = 0


class ToolCallStatsResult(BaseModel):
    model_config = {"extra": "forbid"}
    total_tool_calls: int = 0
    iterations_with_tools: int = 0
    by_tool: dict[str, ToolCallByTool] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Per-operation result models
# ---------------------------------------------------------------------------


class LlmRequestResult(BaseModel):
    model_config = {"extra": "forbid"}
    tokens_in: int = 0
    tokens_out: int = 0
    duration_ms: int = 0
    finish_reason: str = ""
    model: str = ""


class ToolExecutionResult(BaseModel):
    model_config = {"extra": "forbid"}
    success: bool = True
    duration_ms: int = 0
    error: str | None = None


class UserRequestResult(BaseModel):
    model_config = {"extra": "forbid"}
    status: str = "complete"
    output: Any = None
    iterations: int | None = None
    total_usage: AggregatedUsageResult | None = None
    timing_stats: TimingStatsResult | None = None
    tool_call_stats: ToolCallStatsResult | None = None
    finish_reason: str | None = None
    metadata: dict[str, Any] | None = None


class SubAgentResult(BaseModel):
    model_config = {"extra": "forbid"}
    agent_name: str = ""
    success: bool = True
    error: str | None = None


class PersistenceResult(BaseModel):
    model_config = {"extra": "forbid"}
    records_written: int = 0
    duration_ms: int = 0


COMPLETION_RESULT_REGISTRY: dict[str, type[BaseModel]] = {
    "llm_request": LlmRequestResult,
    "tool_execution": ToolExecutionResult,
    "user_request": UserRequestResult,
    "sub_agent": SubAgentResult,
    "persistence": PersistenceResult,
}


# ---------------------------------------------------------------------------
# Typed CompletionEvent models — narrow CompletionPayload per operation
# ---------------------------------------------------------------------------


class LlmRequestCompletionEvent(CompletionPayload):
    operation: Literal["llm_request"]  # type: ignore[assignment]
    result: LlmRequestResult  # type: ignore[assignment]


class ToolExecutionCompletionEvent(CompletionPayload):
    operation: Literal["tool_execution"]  # type: ignore[assignment]
    result: ToolExecutionResult  # type: ignore[assignment]


class UserRequestCompletionEvent(CompletionPayload):
    operation: Literal["user_request"]  # type: ignore[assignment]
    result: UserRequestResult  # type: ignore[assignment]


class SubAgentCompletionEvent(CompletionPayload):
    operation: Literal["sub_agent"]  # type: ignore[assignment]
    result: SubAgentResult  # type: ignore[assignment]


class PersistenceCompletionEvent(CompletionPayload):
    operation: Literal["persistence"]  # type: ignore[assignment]
    result: PersistenceResult  # type: ignore[assignment]


COMPLETION_EVENT_REGISTRY: dict[str, type[CompletionPayload]] = {
    "llm_request":    LlmRequestCompletionEvent,
    "tool_execution": ToolExecutionCompletionEvent,
    "user_request":   UserRequestCompletionEvent,
    "sub_agent":      SubAgentCompletionEvent,
    "persistence":    PersistenceCompletionEvent,
}
