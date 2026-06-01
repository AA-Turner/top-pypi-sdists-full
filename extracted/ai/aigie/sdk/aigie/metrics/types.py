"""
Type definitions for metric context parameters.

Provides TypedDict classes for type-safe context validation.
"""

from typing import Any, TypedDict


class MetricContextBase(TypedDict, total=False):
    """Base context type for all metrics."""

    trace_id: str | None
    span_id: str | None
    function_name: str | None
    span_type: str | None
    timestamp: str | None
    api_url: str | None
    aigie_client: Any | None


class DriftContext(MetricContextBase, total=False):
    """Context type for drift detection metric."""

    baseline_context: str
    current_context: str
    drift_type: str  # "semantic", "structural", etc.
    baseline_trace_id: str | None
    similarity_score: float | None


class RecoveryContext(MetricContextBase, total=False):
    """Context type for recovery success metric."""

    original_error: str
    error: str | None  # Alternative to original_error
    error_type: str
    recovery_strategy: str
    recovery_success: bool
    recovery_duration_ms: int
    recovery_metadata: dict[str, Any] | None
    recovery_result: str | None


class CheckpointContext(MetricContextBase, total=False):
    """Context type for checkpoint validity metric."""

    checkpoint_id: str
    checkpoint_type: str
    state_snapshot: dict[str, Any]
    execution_path: list[Any]


class NestedAgentContext(MetricContextBase, total=False):
    """Context type for nested agent health metric."""

    nested_depth: int
    agent_hierarchy: dict[str, Any]
    nested_agents: list[dict[str, Any]]
    parent_agent_id: str | None
    agent_handoffs: list[Any] | None


class ProductionReliabilityContext(MetricContextBase, total=False):
    """Context type for production reliability composite metric."""

    drift: DriftContext | None
    recovery: RecoveryContext | None
    checkpoint: CheckpointContext | None
    nested: NestedAgentContext | None
