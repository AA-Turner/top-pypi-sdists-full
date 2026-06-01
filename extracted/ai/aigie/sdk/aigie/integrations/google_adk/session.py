"""
Google ADK session context management.

Provides trace context propagation using Python's contextvars,
enabling all operations in a session to share the same trace.
"""

import contextvars
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field


@dataclass
class GoogleADKSessionContext:
    """
    Holds shared state across all handlers in a Google ADK session.

    This enables trace_id, turn numbers, and aggregated metrics
    to persist across multiple agent invocations within a Runner.
    """

    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_name: str = "Google ADK Session"
    total_agent_invocations: int = 0
    total_model_calls: int = 0
    total_tool_calls: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost: float = 0.0
    trace_created: bool = False
    current_invocation_span_id: str | None = None
    current_agent_span_id: str | None = None
    # Parent span tracking for proper hierarchy
    current_parent_span_id: str | None = None
    # Model tracking
    current_model: str | None = None

    def increment_agent_invocation(self) -> int:
        """Increment and return the new agent invocation count."""
        self.total_agent_invocations += 1
        return self.total_agent_invocations

    def increment_model_calls(self) -> int:
        """Increment and return the new model call count."""
        self.total_model_calls += 1
        return self.total_model_calls

    def increment_tool_calls(self) -> int:
        """Increment and return the new tool call count."""
        self.total_tool_calls += 1
        return self.total_tool_calls

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

    def mark_trace_created(self) -> None:
        """Mark that the trace has been created."""
        self.trace_created = True

    def set_current_parent(self, span_id: str | None) -> None:
        """Set the current parent span ID for hierarchical nesting."""
        self.current_parent_span_id = span_id

    def get_current_parent(self) -> str | None:
        """Get the current parent span ID for hierarchical nesting."""
        return self.current_parent_span_id

    def get_summary(self) -> dict:
        """Get session summary."""
        return {
            "trace_id": self.trace_id,
            "trace_name": self.trace_name,
            "total_agent_invocations": self.total_agent_invocations,
            "total_model_calls": self.total_model_calls,
            "total_tool_calls": self.total_tool_calls,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "total_cost": self.total_cost,
        }


# Session-level context variable
_current_session_context: contextvars.ContextVar[GoogleADKSessionContext | None] = (
    contextvars.ContextVar("_current_google_adk_session_context", default=None)
)


def get_session_context() -> GoogleADKSessionContext | None:
    """
    Get the current session context.

    Returns:
        The current GoogleADKSessionContext or None if not in a session.
    """
    return _current_session_context.get()


def set_session_context(context: GoogleADKSessionContext | None) -> contextvars.Token:
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
    trace_name: str = "Google ADK Session",
    trace_id: str | None = None,
) -> GoogleADKSessionContext:
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
    context = GoogleADKSessionContext(
        trace_id=trace_id or str(uuid.uuid4()),
        trace_name=trace_name,
    )
    _current_session_context.set(context)
    return context


@contextmanager
def google_adk_session(
    trace_name: str = "Google ADK Session",
    trace_id: str | None = None,
):
    """
    Context manager for explicit session scoping.

    Use this to explicitly define the boundaries of a session
    that should share a single trace.

    Example:
        with google_adk_session("My Agent Session"):
            async for event in runner.run_async(...):
                process(event)
            # Another run in the same session
            async for event in runner.run_async(...):
                process(event)
            # Both runs share the same trace

    Args:
        trace_name: Name for the trace.
        trace_id: Optional trace ID to use.

    Yields:
        The session context.
    """
    context = GoogleADKSessionContext(
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
