"""
LlamaIndex session context management.

Provides trace context propagation using Python's contextvars,
enabling all operations in a session to share the same trace.
"""

import contextvars
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any


@dataclass
class LlamaIndexSessionContext:
    """
    Holds shared state across all handlers in a LlamaIndex session.

    This enables trace_id, query counts, and aggregated metrics
    to persist across multiple query engine invocations.
    """

    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_name: str = "LlamaIndex Session"
    total_queries: int = 0
    total_retrievals: int = 0
    total_synthesis_calls: int = 0
    total_llm_calls: int = 0
    total_embedding_calls: int = 0
    total_rerank_calls: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost: float = 0.0
    trace_created: bool = False
    current_query_span_id: str | None = None
    current_retrieval_span_id: str | None = None
    # Parent span tracking for proper hierarchy
    current_parent_span_id: str | None = None
    # Model tracking
    current_model: str | None = None
    models_used: dict[str, int] = field(default_factory=dict)
    # Retrieval tracking
    total_nodes_retrieved: int = 0
    total_nodes_after_rerank: int = 0
    # Index tracking
    indices_used: dict[str, int] = field(default_factory=dict)
    # Embedding tracking
    embedding_models_used: dict[str, int] = field(default_factory=dict)

    def increment_query(self) -> int:
        """Increment and return the new query count."""
        self.total_queries += 1
        return self.total_queries

    def increment_retrieval(self, nodes_retrieved: int = 0) -> int:
        """Increment retrieval count and track nodes."""
        self.total_retrievals += 1
        self.total_nodes_retrieved += nodes_retrieved
        return self.total_retrievals

    def increment_synthesis(self) -> int:
        """Increment and return the new synthesis call count."""
        self.total_synthesis_calls += 1
        return self.total_synthesis_calls

    def increment_llm_call(self) -> int:
        """Increment and return the new LLM call count."""
        self.total_llm_calls += 1
        return self.total_llm_calls

    def increment_embedding_call(self, model: str | None = None) -> int:
        """Increment embedding call count and track model."""
        self.total_embedding_calls += 1
        if model:
            self.embedding_models_used[model] = self.embedding_models_used.get(model, 0) + 1
        return self.total_embedding_calls

    def increment_rerank_call(self, nodes_after: int = 0) -> int:
        """Increment rerank count and track output nodes."""
        self.total_rerank_calls += 1
        self.total_nodes_after_rerank += nodes_after
        return self.total_rerank_calls

    def track_index(self, index_name: str) -> None:
        """Track index usage."""
        if index_name:
            self.indices_used[index_name] = self.indices_used.get(index_name, 0) + 1

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
            "total_queries": self.total_queries,
            "total_retrievals": self.total_retrievals,
            "total_synthesis_calls": self.total_synthesis_calls,
            "total_llm_calls": self.total_llm_calls,
            "total_embedding_calls": self.total_embedding_calls,
            "total_rerank_calls": self.total_rerank_calls,
            "total_nodes_retrieved": self.total_nodes_retrieved,
            "total_nodes_after_rerank": self.total_nodes_after_rerank,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "total_cost": self.total_cost,
            "models_used": self.models_used,
            "embedding_models_used": self.embedding_models_used,
            "indices_used": self.indices_used,
        }


# Session-level context variable
_current_session_context: contextvars.ContextVar[LlamaIndexSessionContext | None] = (
    contextvars.ContextVar("_current_llamaindex_session_context", default=None)
)


def get_session_context() -> LlamaIndexSessionContext | None:
    """
    Get the current session context.

    Returns:
        The current LlamaIndexSessionContext or None if not in a session.
    """
    return _current_session_context.get()


def set_session_context(context: LlamaIndexSessionContext | None) -> contextvars.Token:
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
    trace_name: str = "LlamaIndex Session",
    trace_id: str | None = None,
) -> LlamaIndexSessionContext:
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
    context = LlamaIndexSessionContext(
        trace_id=trace_id or str(uuid.uuid4()),
        trace_name=trace_name,
    )
    _current_session_context.set(context)
    return context


@contextmanager
def llamaindex_session(
    trace_name: str = "LlamaIndex Session",
    trace_id: str | None = None,
):
    """
    Context manager for explicit session scoping.

    Use this to explicitly define the boundaries of a session
    that should share a single trace.

    Example:
        with llamaindex_session("Document QA Session"):
            query_engine.query("What is the main topic?")
            query_engine.query("What are the key points?")
            # Both queries share the same trace

    Args:
        trace_name: Name for the trace.
        trace_id: Optional trace ID to use.

    Yields:
        The session context.
    """
    context = LlamaIndexSessionContext(
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
