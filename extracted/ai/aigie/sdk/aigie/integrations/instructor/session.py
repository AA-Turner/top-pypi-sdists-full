"""
Instructor session context management.

Provides trace context propagation using Python's contextvars,
enabling all operations in a session to share the same trace.
"""

import contextvars
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any


@dataclass
class InstructorSessionContext:
    """
    Holds shared state across all handlers in an Instructor session.

    This enables trace_id, extraction counts, and aggregated metrics
    to persist across multiple structured extraction invocations.
    """

    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_name: str = "Instructor Session"
    total_extractions: int = 0
    total_completions: int = 0
    total_retries: int = 0
    total_validation_errors: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost: float = 0.0
    trace_created: bool = False
    current_extraction_span_id: str | None = None
    current_completion_span_id: str | None = None
    # Parent span tracking for proper hierarchy
    current_parent_span_id: str | None = None
    # Model tracking
    current_model: str | None = None
    models_used: dict[str, int] = field(default_factory=dict)
    # Schema tracking
    schemas_used: dict[str, int] = field(default_factory=dict)
    # Retry tracking per schema
    retries_by_schema: dict[str, int] = field(default_factory=dict)

    def increment_extraction(self, schema_name: str | None = None) -> int:
        """Increment and return the new extraction count."""
        self.total_extractions += 1
        if schema_name:
            self.schemas_used[schema_name] = self.schemas_used.get(schema_name, 0) + 1
        return self.total_extractions

    def increment_completion(self) -> int:
        """Increment and return the new completion count."""
        self.total_completions += 1
        return self.total_completions

    def increment_retry(self, schema_name: str | None = None) -> int:
        """Increment and return the new retry count."""
        self.total_retries += 1
        if schema_name:
            self.retries_by_schema[schema_name] = self.retries_by_schema.get(schema_name, 0) + 1
        return self.total_retries

    def increment_validation_error(self) -> int:
        """Increment and return the new validation error count."""
        self.total_validation_errors += 1
        return self.total_validation_errors

    def add_tokens(
        self,
        input_tokens: int = 0,
        output_tokens: int = 0,
    ) -> None:
        """Add token counts to the session totals."""
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens

    def add_cost(self, cost: float) -> None:
        """Add cost to the session total."""
        self.total_cost += cost

    def track_model(self, model: str) -> None:
        """Track model usage."""
        if model:
            self.models_used[model] = self.models_used.get(model, 0) + 1
            self.current_model = model

    def mark_trace_created(self) -> None:
        """Mark that the trace has been created."""
        self.trace_created = True

    def set_current_parent(self, span_id: str | None) -> None:
        """Set the current parent span ID for hierarchical nesting."""
        self.current_parent_span_id = span_id

    def get_current_parent(self) -> str | None:
        """Get the current parent span ID for hierarchical nesting."""
        return self.current_parent_span_id

    def get_summary(self) -> dict[str, Any]:
        """Get session summary."""
        return {
            "trace_id": self.trace_id,
            "trace_name": self.trace_name,
            "total_extractions": self.total_extractions,
            "total_completions": self.total_completions,
            "total_retries": self.total_retries,
            "total_validation_errors": self.total_validation_errors,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "total_cost": self.total_cost,
            "models_used": self.models_used,
            "schemas_used": self.schemas_used,
            "retries_by_schema": self.retries_by_schema,
            "retry_rate": self.total_retries / max(self.total_extractions, 1),
        }


# Session-level context variable
_current_session_context: contextvars.ContextVar[InstructorSessionContext | None] = (
    contextvars.ContextVar("_current_instructor_session_context", default=None)
)


def get_session_context() -> InstructorSessionContext | None:
    """
    Get the current session context.

    Returns:
        The current InstructorSessionContext or None if not in a session.
    """
    return _current_session_context.get()


def set_session_context(context: InstructorSessionContext | None) -> contextvars.Token:
    """
    Set the current session context.

    Args:
        context: The session context to set, or None to clear.

    Returns:
        Token that can be used to reset to the previous value.
    """
    return _current_session_context.set(context)


def reset_session_context(token: contextvars.Token) -> None:
    """
    Reset session context to a previous value.

    Args:
        token: Token from a previous set_session_context call.
    """
    _current_session_context.reset(token)


def get_or_create_session_context(
    trace_name: str = "Instructor Session",
    trace_id: str | None = None,
) -> InstructorSessionContext:
    """
    Get the existing session context or create a new one.

    This is the main entry point for session context management.
    If a session context exists, it returns that context (preserving
    the shared trace_id). Otherwise, it creates a new context.

    Args:
        trace_name: Name for the trace (only used if creating new).
        trace_id: Optional trace ID to use (only used if creating new).

    Returns:
        The session context (existing or newly created).
    """
    existing = _current_session_context.get()
    if existing is not None:
        return existing

    # Create new session context
    context = InstructorSessionContext(
        trace_id=trace_id or str(uuid.uuid4()),
        trace_name=trace_name,
    )
    _current_session_context.set(context)
    return context


@contextmanager
def instructor_session(
    trace_name: str = "Instructor Session",
    trace_id: str | None = None,
):
    """
    Context manager for explicit session scoping.

    Use this to explicitly define the boundaries of a session
    that should share a single trace.

    Example:
        with instructor_session("Data Extraction Session"):
            client.chat.completions.create(response_model=User, ...)
            client.chat.completions.create(response_model=Address, ...)
            # Both extractions share the same trace

    Args:
        trace_name: Name for the trace.
        trace_id: Optional trace ID to use.

    Yields:
        The session context.
    """
    context = InstructorSessionContext(
        trace_id=trace_id or str(uuid.uuid4()),
        trace_name=trace_name,
    )
    token = _current_session_context.set(context)
    try:
        yield context
    finally:
        _current_session_context.reset(token)


def clear_session_context() -> None:
    """
    Clear the current session context.

    This forces a new trace to be created on the next operation.
    """
    _current_session_context.set(None)
