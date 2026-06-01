"""
LangGraph session context management.

Provides trace context propagation using Python's contextvars,
enabling all operations in a session to share the same trace.
"""

import contextvars
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any


@dataclass
class LangGraphSessionContext:
    """
    Holds shared state across all handlers in a LangGraph session.

    This enables trace_id, node execution counts, and aggregated metrics
    to persist across multiple graph invocations.
    """

    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_name: str = "LangGraph Session"
    total_graph_runs: int = 0
    total_node_executions: int = 0
    total_llm_calls: int = 0
    total_tool_calls: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost: float = 0.0
    trace_created: bool = False
    current_graph_span_id: str | None = None
    current_node_span_id: str | None = None
    # Parent span tracking for proper hierarchy
    current_parent_span_id: str | None = None
    # Node tracking
    nodes_executed: list[str] = field(default_factory=list)
    # Model tracking
    models_used: dict[str, int] = field(default_factory=dict)
    # State tracking
    state_versions: int = 0

    def increment_graph_run(self) -> int:
        """Increment and return the new graph run count."""
        self.total_graph_runs += 1
        return self.total_graph_runs

    def increment_node_execution(self, node_name: str) -> int:
        """Increment node execution count and track the node."""
        self.total_node_executions += 1
        self.nodes_executed.append(node_name)
        return self.total_node_executions

    def increment_llm_calls(self) -> int:
        """Increment and return the new LLM call count."""
        self.total_llm_calls += 1
        return self.total_llm_calls

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

    def track_model(self, model: str) -> None:
        """Track model usage."""
        if model:
            self.models_used[model] = self.models_used.get(model, 0) + 1

    def mark_trace_created(self) -> None:
        """Mark that the trace has been created."""
        self.trace_created = True

    def set_current_parent(self, span_id: str | None) -> None:
        """Set the current parent span ID for hierarchical nesting."""
        self.current_parent_span_id = span_id

    def get_current_parent(self) -> str | None:
        """Get the current parent span ID for hierarchical nesting."""
        return self.current_parent_span_id

    def increment_state_version(self) -> int:
        """Increment state version counter."""
        self.state_versions += 1
        return self.state_versions

    def get_summary(self) -> dict[str, Any]:
        """Get session summary."""
        return {
            "trace_id": self.trace_id,
            "trace_name": self.trace_name,
            "total_graph_runs": self.total_graph_runs,
            "total_node_executions": self.total_node_executions,
            "total_llm_calls": self.total_llm_calls,
            "total_tool_calls": self.total_tool_calls,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "total_cost": self.total_cost,
            "nodes_executed": self.nodes_executed,
            "unique_nodes": list(set(self.nodes_executed)),
            "models_used": self.models_used,
            "state_versions": self.state_versions,
        }


# Session-level context variable
_current_session_context: contextvars.ContextVar[LangGraphSessionContext | None] = (
    contextvars.ContextVar("_current_langgraph_session_context", default=None)
)


def get_session_context() -> LangGraphSessionContext | None:
    """
    Get the current session context.

    Returns:
        The current LangGraphSessionContext or None if not in a session.
    """
    return _current_session_context.get()


def set_session_context(context: LangGraphSessionContext | None) -> contextvars.Token:
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
    trace_name: str = "LangGraph Session",
    trace_id: str | None = None,
) -> LangGraphSessionContext:
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
    context = LangGraphSessionContext(
        trace_id=trace_id or str(uuid.uuid4()),
        trace_name=trace_name,
    )
    _current_session_context.set(context)
    return context


@contextmanager
def langgraph_session(
    trace_name: str = "LangGraph Session",
    trace_id: str | None = None,
):
    """
    Context manager for explicit session scoping.

    Use this to explicitly define the boundaries of a session
    that should share a single trace.

    Example:
        with langgraph_session("My Graph Session"):
            graph.invoke({"input": "First query"})
            graph.invoke({"input": "Second query"})
            # Both invocations share the same trace

    Args:
        trace_name: Name for the trace.
        trace_id: Optional trace ID to use.

    Yields:
        The session context.
    """
    context = LangGraphSessionContext(
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
