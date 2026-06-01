"""
Context propagation system for automatic trace/span relationships.

This module provides automatic context propagation using Python's contextvars,
enabling seamless parent-child relationships without manual ID passing.
"""

import contextvars
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

# Context variables for thread-safe trace context propagation
_current_trace_context: contextvars.ContextVar[Optional["RunContext"]] = contextvars.ContextVar(
    "_current_trace_context", default=None
)

_current_span_context: contextvars.ContextVar[Optional["RunContext"]] = contextvars.ContextVar(
    "_current_span_context", default=None
)

# Global configuration context
_global_tags: contextvars.ContextVar[list[str] | None] = contextvars.ContextVar(
    "_global_tags", default=None
)

_global_metadata: contextvars.ContextVar[dict[str, Any] | None] = contextvars.ContextVar(
    "_global_metadata", default=None
)

_tracing_enabled: contextvars.ContextVar[bool] = contextvars.ContextVar(
    "_tracing_enabled", default=True
)

_project_name: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "_project_name", default=None
)


@dataclass
class RunContext:
    """
    Execution context for a trace or span.

    Contains all contextual information needed for nested execution tracking.
    """

    id: str
    name: str
    type: str  # "trace" or "span"
    span_type: str | None = None  # For spans: "llm", "tool", "agent", etc.
    parent_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    start_time: datetime | None = None

    # Additional context for features
    project_name: str | None = None
    environment: str | None = None
    user_id: str | None = None
    session_id: str | None = None

    # Plan adherence tracking
    expected_tools: list[str] = field(default_factory=list)
    actual_tools_called: list[str] = field(default_factory=list)

    @property
    def plan_adherence_score(self) -> float:
        """How closely tool usage matched the expected plan. 1.0 = perfect."""
        if not self.expected_tools:
            return 1.0
        matched = set(self.expected_tools) & set(self.actual_tools_called)
        return len(matched) / len(self.expected_tools)

    @property
    def unexpected_tools(self) -> list[str]:
        """Tools called that were NOT in the expected plan."""
        if not self.expected_tools:
            return []
        expected_set = set(self.expected_tools)
        return [t for t in self.actual_tools_called if t not in expected_set]

    @property
    def is_potential_stuck_loop(self) -> bool:
        """Detect if the same tool is called 3+ times consecutively."""
        if len(self.actual_tools_called) < 3:
            return False
        for i in range(len(self.actual_tools_called) - 2):
            if (
                self.actual_tools_called[i]
                == self.actual_tools_called[i + 1]
                == self.actual_tools_called[i + 2]
            ):
                return True
        return False

    def to_dict(self) -> dict[str, Any]:
        """Convert context to dictionary for API calls."""
        data = {
            "id": self.id,
            "name": self.name,
            "metadata": self.metadata,
            "tags": self.tags,
        }

        if self.parent_id:
            data["parent_id"] = self.parent_id
        if self.span_type:
            data["type"] = self.span_type
        if self.project_name:
            data["project_name"] = self.project_name
        if self.environment:
            data["environment"] = self.environment
        if self.user_id:
            data["user_id"] = self.user_id
        if self.session_id:
            data["session_id"] = self.session_id

        if self.expected_tools:
            data["expected_tools"] = self.expected_tools
        if self.actual_tools_called:
            data["actual_tools_called"] = self.actual_tools_called
            data["plan_adherence_score"] = self.plan_adherence_score
            data["unexpected_tools"] = self.unexpected_tools
            data["is_potential_stuck_loop"] = self.is_potential_stuck_loop

        return data


def get_current_trace_context() -> RunContext | None:
    """
    Get the current trace context from contextvar.

    Returns:
        Current trace context or None if no trace is active
    """
    return _current_trace_context.get()


def set_current_trace_context(context: RunContext | None) -> None:
    """
    Set the current trace context.

    Args:
        context: Trace context to set
    """
    _current_trace_context.set(context)

    # Also set process-level trace ID for OTel bridge (thread pool workers)
    try:
        from .auto_instrument.span_enricher import set_active_trace_id

        set_active_trace_id(context.id if context else None)
    except Exception:
        pass  # OTel bridge not available


def get_current_span_context() -> RunContext | None:
    """
    Get the current span context from contextvar.

    Returns:
        Current span context or None if no span is active
    """
    return _current_span_context.get()


def set_current_span_context(context: RunContext | None) -> None:
    """
    Set the current span context.

    Args:
        context: Span context to set
    """
    _current_span_context.set(context)


def get_parent_context() -> RunContext | None:
    """
    Get the parent context (span if available, otherwise trace).

    This determines what the parent_id should be for a new span.

    Returns:
        Parent context (span > trace > None)
    """
    span_ctx = get_current_span_context()
    if span_ctx:
        return span_ctx

    return get_current_trace_context()


def is_tracing_enabled() -> bool:
    """
    Check if tracing is enabled in current context.

    Returns:
        True if tracing is enabled, False otherwise
    """
    return _tracing_enabled.get()


def set_tracing_enabled(enabled: bool) -> None:
    """
    Enable or disable tracing in current context.

    Args:
        enabled: Whether tracing should be enabled
    """
    _tracing_enabled.set(enabled)


def get_global_tags() -> list[str]:
    """
    Get global tags for current context.

    Returns:
        List of global tags
    """
    return _global_tags.get() or []


def set_global_tags(tags: list[str]) -> None:
    """
    Set global tags for current context.

    Args:
        tags: List of tags to apply to all traces/spans
    """
    _global_tags.set(tags)


def add_global_tags(tags: list[str]) -> None:
    """
    Add tags to global tag list.

    Args:
        tags: Tags to add
    """
    current = get_global_tags()
    current.extend(tags)
    set_global_tags(current)


def get_global_metadata() -> dict[str, Any]:
    """
    Get global metadata for current context.

    Returns:
        Dictionary of global metadata
    """
    return _global_metadata.get() or {}


def set_global_metadata(metadata: dict[str, Any]) -> None:
    """
    Set global metadata for current context.

    Args:
        metadata: Metadata to apply to all traces/spans
    """
    _global_metadata.set(metadata)


def add_global_metadata(metadata: dict[str, Any]) -> None:
    """
    Add metadata to global metadata dict.

    Args:
        metadata: Metadata to add
    """
    current = get_global_metadata()
    current.update(metadata)
    set_global_metadata(current)


def get_project_name() -> str | None:
    """
    Get project name for current context.

    Returns:
        Project name or None
    """
    return _project_name.get()


def set_project_name(name: str | None) -> None:
    """
    Set project name for current context.

    Args:
        name: Project name
    """
    _project_name.set(name)


class tracing_context:
    """
    Context manager for setting tracing configuration.

    Usage:
        with tracing_context(
            enabled=True,
            tags=["production", "critical"],
            metadata={"version": "1.0.0"},
            project_name="customer-support"
        ):
            # All traces/spans created here will inherit these settings
            await my_agent.run()
    """

    def __init__(
        self,
        enabled: bool | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        project_name: str | None = None,
    ):
        """
        Initialize tracing context manager.

        Args:
            enabled: Whether to enable tracing
            tags: Tags to add to all traces/spans
            metadata: Metadata to add to all traces/spans
            project_name: Project name for grouping
        """
        self.enabled = enabled
        self.tags = tags or []
        self.metadata = metadata or {}
        self.project_name = project_name

        # Store previous values for restoration
        self._prev_enabled = None
        self._prev_tags = None
        self._prev_metadata = None
        self._prev_project = None

    def __enter__(self):
        """Enter context and set values."""
        # Save previous values
        self._prev_enabled = is_tracing_enabled()
        self._prev_tags = get_global_tags().copy()
        self._prev_metadata = get_global_metadata().copy()
        self._prev_project = get_project_name()

        # Set new values
        if self.enabled is not None:
            set_tracing_enabled(self.enabled)
        if self.tags:
            add_global_tags(self.tags)
        if self.metadata:
            add_global_metadata(self.metadata)
        if self.project_name:
            set_project_name(self.project_name)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context and restore previous values."""
        set_tracing_enabled(self._prev_enabled)
        set_global_tags(self._prev_tags)
        set_global_metadata(self._prev_metadata)
        set_project_name(self._prev_project)
        return False


def merge_tags(*tag_lists: list[str] | None) -> list[str]:
    """
    Merge multiple tag lists, removing duplicates while preserving order.

    Args:
        *tag_lists: Variable number of tag lists

    Returns:
        Merged list of unique tags
    """
    seen = set()
    result = []

    # Start with global tags
    for tag in get_global_tags():
        if tag not in seen:
            seen.add(tag)
            result.append(tag)

    # Add tags from provided lists
    for tag_list in tag_lists:
        if tag_list:
            for tag in tag_list:
                if tag not in seen:
                    seen.add(tag)
                    result.append(tag)

    return result


def merge_metadata(*metadata_dicts: dict[str, Any] | None) -> dict[str, Any]:
    """
    Merge multiple metadata dictionaries.

    Later dicts override earlier ones for conflicting keys.

    Args:
        *metadata_dicts: Variable number of metadata dicts

    Returns:
        Merged metadata dictionary
    """
    result = get_global_metadata().copy()

    for metadata_dict in metadata_dicts:
        if metadata_dict:
            result.update(metadata_dict)

    return result
