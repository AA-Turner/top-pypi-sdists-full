"""
Type definitions for Aigie SDK.

This module provides type hints and type aliases for better IDE support.
"""

from typing import Any, Literal

from typing_extensions import NotRequired, TypedDict

# Status types - aligned with backend (see backend/src/models/traces.py)
TraceStatus = Literal["success", "failure", "timeout", "cancelled"]
SpanStatus = Literal["success", "failure", "error"]

# Observation levels for spans (Langfuse-compatible)
ObservationLevel = Literal["DEBUG", "DEFAULT", "WARNING", "ERROR"]

# Span types - aligned with backend SpanType enum (backend/src/models/spans.py)
SpanType = Literal[
    # Standard operation types (OpenInference-aligned)
    "chain",  # Sequential chain of operations
    "llm",  # Large Language Model call
    "tool",  # Tool/function execution
    "agent",  # Agent operation
    "workflow",  # State machine/LangGraph workflow
    "retriever",  # Vector DB retrieval
    "retrieval",  # Alternative retrieval type
    "embedding",  # Embedding model call
    "reranker",  # Document reranking
    # Aigie-specific reliability types
    "drift_detection",  # Context drift detection
    "error_recovery",  # Error recovery attempt
    "checkpoint",  # State checkpoint
    "evaluator",  # Evaluation operation
    # Agent orchestration types
    "nested_agent",  # Nested agent call
    "agent_orchestrator",  # Agent orchestration
    # Agent observability types (Think-Act-Observe pattern)
    "reasoning",  # Agent reasoning/thinking phase
    "observation",  # Agent observation/evaluation phase
    "think",  # Alias for reasoning phase
    "act",  # Action execution phase
    "plan",  # Planning phase
    "goal",  # Goal tracking span
    "loop_detection",  # Loop detection check
    "cycle",  # Execution cycle span
    # Business/domain types
    "classification",  # Classification operation
    "validation",  # Validation check
    "escalation",  # Escalation event
    "business_event",  # Business domain event
    "guardrail",  # Safety guardrail check
    # Fallback
    "unknown",  # Unknown/unclassified span
]

# Failure categories for analysis (backend/src/models/enums.py)
FailureCategory = Literal[
    "timeout_error",
    "llm_error",
    "tool_error",
    "logic_error",
    "data_error",
    "network_error",
    "unknown",
]


# Token usage tracking (Langfuse-compatible)
class TokenUsage(TypedDict):
    """Token usage for LLM spans."""

    input: NotRequired[int]  # Prompt tokens
    output: NotRequired[int]  # Completion tokens
    total: NotRequired[int]  # Total tokens
    unit: NotRequired[str]  # Token unit (e.g., "TOKENS")


# Metadata and tags
Metadata = dict[str, Any]
Tags = list[str]

# JSON-compatible value. Buffered event payloads are JSON-serialized for
# offline storage, so they must stay within these types.
JsonValue = str | int | float | bool | None | list["JsonValue"] | dict[str, "JsonValue"]

# Payload of a buffered event (see aigie.buffer.BufferedEvent).
EventPayload = dict[str, JsonValue]


class OfflineStorageStats(TypedDict):
    """Statistics for the on-disk offline event store."""

    pending_files: int
    total_size_bytes: int
    storage_dir: str


class OfflineModeStats(TypedDict):
    """Offline-mode statistics reported by ``EventBuffer.get_offline_stats``."""

    enabled: bool
    is_offline: bool
    consecutive_failures: int
    offline_threshold: int
    storage: NotRequired[OfflineStorageStats]


# Response types
class TraceResponse(TypedDict):
    """Response from trace API."""

    id: str
    name: str
    status: TraceStatus
    metadata: Metadata
    tags: Tags
    start_time: NotRequired[str]
    end_time: NotRequired[str]
    duration_ns: NotRequired[int]
    created_at: NotRequired[str]
    updated_at: NotRequired[str]
    # Error info
    error_message: NotRequired[str]
    error_type: NotRequired[str]
    # Workflow flag
    has_workflow: NotRequired[bool]
    # Langfuse-compatible fields
    input: NotRequired[Any]
    output: NotRequired[Any]
    environment: NotRequired[str]
    release: NotRequired[str]
    version: NotRequired[str]
    session_id: NotRequired[str]
    user_id: NotRequired[str]
    bookmarked: NotRequired[bool]
    public: NotRequired[bool]
    # Calculated fields
    latency: NotRequired[float]  # Latency in seconds
    total_tokens: NotRequired[int]  # Total tokens across all spans
    total_cost: NotRequired[float]  # Total cost across all spans
    # Pre-aggregated fields (for efficient list views)
    agg_total_tokens: NotRequired[int]
    agg_prompt_tokens: NotRequired[int]
    agg_completion_tokens: NotRequired[int]
    agg_total_cost: NotRequired[float]
    agg_has_error: NotRequired[bool]
    agg_span_count: NotRequired[int]
    agg_error_count: NotRequired[int]
    agg_computed_status: NotRequired[str]
    agg_duration_ns: NotRequired[int]
    agg_end_time: NotRequired[str]


class SpanResponse(TypedDict):
    """Response from span API."""

    id: str
    trace_id: str
    name: str
    type: SpanType
    parent_id: NotRequired[str]
    input: NotRequired[Any]
    output: NotRequired[Any]
    metadata: Metadata
    tags: NotRequired[Tags]
    status: NotRequired[SpanStatus]
    start_time: NotRequired[str]
    end_time: NotRequired[str]
    duration_ns: NotRequired[int]
    created_at: NotRequired[str]
    # Error info
    error: NotRequired[str]
    error_type: NotRequired[str]
    # LLM-specific fields
    model: NotRequired[str]
    internal_model: NotRequired[str]
    internal_model_id: NotRequired[str]
    model_parameters: NotRequired[dict[str, Any]]
    # Token tracking
    prompt_tokens: NotRequired[int]
    completion_tokens: NotRequired[int]
    total_tokens: NotRequired[int]
    token_usage: NotRequired[TokenUsage]
    # Cost tracking
    input_cost: NotRequired[float]
    output_cost: NotRequired[float]
    total_cost: NotRequired[float]
    calculated_input_cost: NotRequired[float]
    calculated_output_cost: NotRequired[float]
    calculated_total_cost: NotRequired[float]
    # Timing
    completion_start_time: NotRequired[str]  # TTFT for streaming
    latency: NotRequired[float]  # Latency in seconds
    # Observation level
    level: NotRequired[ObservationLevel]
    status_message: NotRequired[str]
    version: NotRequired[str]
    unit: NotRequired[str]
    prompt_id: NotRequired[str]


# Configuration types
class RetryConfig(TypedDict):
    """Retry configuration."""

    max_retries: int
    base_delay: float
    max_delay: float
    exponential_base: float
    jitter: bool


class BufferConfig(TypedDict):
    """Buffer configuration."""

    max_size: int
    flush_interval: float
    enable_buffering: bool
