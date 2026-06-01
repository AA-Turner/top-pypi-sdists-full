"""
LangChain session context management.

Provides trace context propagation using Python's contextvars,
enabling all operations in a session to share the same trace.
"""

import contextvars
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any


@dataclass
class LangChainSessionContext:
    """
    Holds shared state across all callbacks in a LangChain session.

    This enables trace_id, run counts, and aggregated metrics
    to persist across multiple chain invocations.
    """

    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_name: str = "LangChain Session"
    total_runs: int = 0
    total_chain_runs: int = 0
    total_llm_runs: int = 0
    total_tool_runs: int = 0
    total_retriever_runs: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost: float = 0.0
    trace_created: bool = False
    current_chain_span_id: str | None = None
    current_llm_span_id: str | None = None
    # Parent span tracking for proper hierarchy
    current_parent_span_id: str | None = None
    # Model tracking
    models_used: dict[str, int] = field(default_factory=dict)

    def increment_run(self, run_type: str = "chain") -> int:
        """Increment and return the new run count."""
        self.total_runs += 1
        if run_type == "chain":
            self.total_chain_runs += 1
        elif run_type == "llm":
            self.total_llm_runs += 1
        elif run_type == "tool":
            self.total_tool_runs += 1
        elif run_type == "retriever":
            self.total_retriever_runs += 1
        return self.total_runs

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

    def get_summary(self) -> dict[str, Any]:
        """Get session summary."""
        return {
            "trace_id": self.trace_id,
            "trace_name": self.trace_name,
            "total_runs": self.total_runs,
            "total_chain_runs": self.total_chain_runs,
            "total_llm_runs": self.total_llm_runs,
            "total_tool_runs": self.total_tool_runs,
            "total_retriever_runs": self.total_retriever_runs,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "total_cost": self.total_cost,
            "models_used": self.models_used,
        }


# Session-level context variable
_current_session_context: contextvars.ContextVar[LangChainSessionContext | None] = (
    contextvars.ContextVar("_current_langchain_session_context", default=None)
)


def get_session_context() -> LangChainSessionContext | None:
    """
    Get the current session context.

    Returns:
        The current LangChainSessionContext or None if not in a session.
    """
    return _current_session_context.get()


def set_session_context(context: LangChainSessionContext | None) -> contextvars.Token:
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
    trace_name: str = "LangChain Session",
    trace_id: str | None = None,
) -> LangChainSessionContext:
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
    context = LangChainSessionContext(
        trace_id=trace_id or str(uuid.uuid4()),
        trace_name=trace_name,
    )
    _current_session_context.set(context)
    return context


@contextmanager
def langchain_session(
    trace_name: str = "LangChain Session",
    trace_id: str | None = None,
):
    """
    Context manager for explicit session scoping.

    Use this to explicitly define the boundaries of a session
    that should share a single trace.

    Example:
        with langchain_session("My Chain Session"):
            chain.invoke("First input")
            chain.invoke("Second input")
            # Both invocations share the same trace

    Args:
        trace_name: Name for the trace.
        trace_id: Optional trace ID to use.

    Yields:
        The session context.
    """
    context = LangChainSessionContext(
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
