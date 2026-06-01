"""
DSPy session context management.

Provides trace context propagation using Python's contextvars,
enabling all operations in a session to share the same trace.
"""

import contextvars
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any


@dataclass
class DSPySessionContext:
    """
    Holds shared state across all handlers in a DSPy session.

    This enables trace_id, module counts, and aggregated metrics
    to persist across multiple program invocations.
    """

    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_name: str = "DSPy Session"
    total_module_calls: int = 0
    total_predictions: int = 0
    total_retrievals: int = 0
    total_reasoning_steps: int = 0
    total_optimizations: int = 0
    total_llm_calls: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost: float = 0.0
    trace_created: bool = False
    current_module_span_id: str | None = None
    current_prediction_span_id: str | None = None
    # Parent span tracking for proper hierarchy
    current_parent_span_id: str | None = None
    # Model tracking
    current_model: str | None = None
    models_used: dict[str, int] = field(default_factory=dict)
    # Module tracking
    modules_used: dict[str, int] = field(default_factory=dict)
    # Signature tracking
    signatures_used: dict[str, int] = field(default_factory=dict)
    # Optimization tracking
    optimization_iterations: int = 0
    best_score: float | None = None

    def increment_module_call(self, module_name: str | None = None) -> int:
        """Increment and return the new module call count."""
        self.total_module_calls += 1
        if module_name:
            self.modules_used[module_name] = self.modules_used.get(module_name, 0) + 1
        return self.total_module_calls

    def increment_prediction(self, signature: str | None = None) -> int:
        """Increment and return the new prediction count."""
        self.total_predictions += 1
        if signature:
            self.signatures_used[signature] = self.signatures_used.get(signature, 0) + 1
        return self.total_predictions

    def increment_retrieval(self) -> int:
        """Increment and return the new retrieval count."""
        self.total_retrievals += 1
        return self.total_retrievals

    def increment_reasoning_step(self) -> int:
        """Increment and return the new reasoning step count."""
        self.total_reasoning_steps += 1
        return self.total_reasoning_steps

    def increment_optimization(self, iterations: int = 1, score: float | None = None) -> int:
        """Increment optimization count and track progress."""
        self.total_optimizations += 1
        self.optimization_iterations += iterations
        if score is not None and (self.best_score is None or score > self.best_score):
            self.best_score = score
        return self.total_optimizations

    def increment_llm_call(self) -> int:
        """Increment and return the new LLM call count."""
        self.total_llm_calls += 1
        return self.total_llm_calls

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
            "total_module_calls": self.total_module_calls,
            "total_predictions": self.total_predictions,
            "total_retrievals": self.total_retrievals,
            "total_reasoning_steps": self.total_reasoning_steps,
            "total_optimizations": self.total_optimizations,
            "optimization_iterations": self.optimization_iterations,
            "best_score": self.best_score,
            "total_llm_calls": self.total_llm_calls,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "total_cost": self.total_cost,
            "models_used": self.models_used,
            "modules_used": self.modules_used,
            "signatures_used": self.signatures_used,
        }


# Session-level context variable
_current_session_context: contextvars.ContextVar[DSPySessionContext | None] = (
    contextvars.ContextVar("_current_dspy_session_context", default=None)
)


def get_session_context() -> DSPySessionContext | None:
    """
    Get the current session context.

    Returns:
        The current DSPySessionContext or None if not in a session.
    """
    return _current_session_context.get()


def set_session_context(context: DSPySessionContext | None) -> contextvars.Token:
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
    trace_name: str = "DSPy Session",
    trace_id: str | None = None,
) -> DSPySessionContext:
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
    context = DSPySessionContext(
        trace_id=trace_id or str(uuid.uuid4()),
        trace_name=trace_name,
    )
    _current_session_context.set(context)
    return context


@contextmanager
def dspy_session(
    trace_name: str = "DSPy Session",
    trace_id: str | None = None,
):
    """
    Context manager for explicit session scoping.

    Use this to explicitly define the boundaries of a session
    that should share a single trace.

    Example:
        with dspy_session("QA Pipeline Session"):
            qa = dspy.ChainOfThought("question -> answer")
            qa(question="What is AI?")
            qa(question="What is ML?")
            # Both invocations share the same trace

    Args:
        trace_name: Name for the trace.
        trace_id: Optional trace ID to use.

    Yields:
        The session context.
    """
    context = DSPySessionContext(
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
