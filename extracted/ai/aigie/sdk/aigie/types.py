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

# Error types - aligned with backend error inference (backend/src/api/v1/spans.py)
ErrorType = Literal[
    "timeout",  # Operation timed out
    "rate_limit",  # Rate limit exceeded (429)
    "network_error",  # Network/connection issues
    "authentication_error",  # Auth/permission issues
    "validation_error",  # Input validation failed
    "llm_error",  # LLM/model error
    "tool_error",  # Tool execution error
    "unknown",  # Unclassified error
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


# Cost tracking (Langfuse-compatible)
class CostDetails(TypedDict):
    """Cost breakdown for LLM spans."""

    input_cost: NotRequired[float]  # Cost for input tokens
    output_cost: NotRequired[float]  # Cost for output tokens
    total_cost: NotRequired[float]  # Total cost


# Usage details for extended token tracking (cache tokens, reasoning tokens, etc.)
class UsageDetails(TypedDict):
    """Extended usage details for LLM spans."""

    input: NotRequired[int]
    output: NotRequired[int]
    total: NotRequired[int]
    cache_read: NotRequired[int]  # Tokens read from cache
    cache_write: NotRequired[int]  # Tokens written to cache
    reasoning: NotRequired[int]  # Reasoning tokens (e.g., o1 models)


# Metadata and tags
Metadata = dict[str, Any]
Tags = list[str]


# API request/response types
class TraceCreateRequest(TypedDict):
    """Request payload for creating a trace."""

    id: NotRequired[str]  # Client-provided ID (optional)
    name: str
    status: NotRequired[TraceStatus]
    metadata: NotRequired[Metadata]
    tags: NotRequired[Tags]
    spans: NotRequired[list[dict[str, Any]]]
    # Langfuse-compatible fields
    input: NotRequired[Any]  # Trace input
    output: NotRequired[Any]  # Trace output
    user_id: NotRequired[str]  # User identifier
    session_id: NotRequired[str]  # Session identifier
    environment: NotRequired[str]  # Environment (default, staging, production)
    version: NotRequired[str]  # Version tag
    release: NotRequired[str]  # Release tag


class TraceUpdateRequest(TypedDict):
    """Request payload for updating a trace."""

    name: NotRequired[str]
    status: NotRequired[TraceStatus]
    error_message: NotRequired[str]
    error_type: NotRequired[str]
    metadata: NotRequired[Metadata]
    tags: NotRequired[Tags]
    spans: NotRequired[list[dict[str, Any]]]
    input: NotRequired[Any]
    output: NotRequired[Any]
    user_id: NotRequired[str]
    session_id: NotRequired[str]
    environment: NotRequired[str]
    version: NotRequired[str]
    release: NotRequired[str]


class SpanCreateRequest(TypedDict):
    """Request payload for creating a span."""

    id: NotRequired[str]  # Client-provided ID (optional)
    trace_id: str
    name: str
    type: SpanType
    parent_id: NotRequired[str]  # Parent span for hierarchy
    input: NotRequired[Any]
    output: NotRequired[Any]
    metadata: NotRequired[Metadata]
    tags: NotRequired[Tags]
    # Error tracking
    error: NotRequired[str]  # Error message (max 5000 chars)
    error_type: NotRequired[ErrorType]  # Error classification
    # Token/Cost tracking
    token_usage: NotRequired[TokenUsage]
    usage: NotRequired[TokenUsage]  # Langfuse-style
    usage_details: NotRequired[UsageDetails]
    cost_details: NotRequired[CostDetails]
    # LLM-specific fields
    model: NotRequired[str]  # Model name
    model_parameters: NotRequired[dict[str, Any]]  # temperature, top_p, etc.
    # Observation level
    level: NotRequired[ObservationLevel]
    status_message: NotRequired[str]
    version: NotRequired[str]


class SpanUpdateRequest(TypedDict):
    """Request payload for updating a span."""

    name: NotRequired[str]
    input: NotRequired[Any]
    output: NotRequired[Any]
    parent_id: NotRequired[str]
    status: NotRequired[SpanStatus]
    # Error tracking
    error: NotRequired[str]
    error_message: NotRequired[str]  # SDK alias for error
    error_type: NotRequired[ErrorType]
    # Token/Cost tracking
    model: NotRequired[str]
    model_parameters: NotRequired[dict[str, Any]]
    prompt_tokens: NotRequired[int]
    completion_tokens: NotRequired[int]
    total_tokens: NotRequired[int]
    input_cost: NotRequired[float]
    output_cost: NotRequired[float]
    total_cost: NotRequired[float]
    # Observation level
    level: NotRequired[ObservationLevel]
    status_message: NotRequired[str]
    version: NotRequired[str]
    metadata: NotRequired[Metadata]
    tags: NotRequired[Tags]


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
