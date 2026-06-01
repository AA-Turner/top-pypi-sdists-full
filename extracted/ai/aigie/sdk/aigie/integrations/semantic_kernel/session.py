"""
Semantic Kernel session context management.

Provides trace context propagation using Python's contextvars,
enabling all operations in a session to share the same trace.
"""

import contextvars
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any


@dataclass
class SemanticKernelSessionContext:
    """
    Holds shared state across all handlers in a Semantic Kernel session.

    This enables trace_id, function counts, and aggregated metrics
    to persist across multiple kernel invocations.
    """

    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_name: str = "Semantic Kernel Session"
    total_invocations: int = 0
    total_function_calls: int = 0
    total_plugin_calls: int = 0
    total_planner_calls: int = 0
    total_llm_calls: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost: float = 0.0
    trace_created: bool = False
    current_invocation_span_id: str | None = None
    current_function_span_id: str | None = None
    # Parent span tracking for proper hierarchy
    current_parent_span_id: str | None = None
    # Model tracking
    current_model: str | None = None
    models_used: dict[str, int] = field(default_factory=dict)
    # Plugin/function tracking
    plugins_used: dict[str, int] = field(default_factory=dict)
    functions_used: dict[str, int] = field(default_factory=dict)
    # Plan tracking
    plans_executed: int = 0
    plan_steps_executed: int = 0

    def increment_invocation(self) -> int:
        """Increment and return the new invocation count."""
        self.total_invocations += 1
        return self.total_invocations

    def increment_function_call(self, function_name: str | None = None) -> int:
        """Increment and return the new function call count."""
        self.total_function_calls += 1
        if function_name:
            self.functions_used[function_name] = self.functions_used.get(function_name, 0) + 1
        return self.total_function_calls

    def increment_plugin_call(self, plugin_name: str | None = None) -> int:
        """Increment and return the new plugin call count."""
        self.total_plugin_calls += 1
        if plugin_name:
            self.plugins_used[plugin_name] = self.plugins_used.get(plugin_name, 0) + 1
        return self.total_plugin_calls

    def increment_planner_call(self) -> int:
        """Increment and return the new planner call count."""
        self.total_planner_calls += 1
        return self.total_planner_calls

    def increment_llm_call(self) -> int:
        """Increment and return the new LLM call count."""
        self.total_llm_calls += 1
        return self.total_llm_calls

    def increment_plan_executed(self, steps: int = 0) -> int:
        """Increment plan execution count and track steps."""
        self.plans_executed += 1
        self.plan_steps_executed += steps
        return self.plans_executed

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
            "total_invocations": self.total_invocations,
            "total_function_calls": self.total_function_calls,
            "total_plugin_calls": self.total_plugin_calls,
            "total_planner_calls": self.total_planner_calls,
            "total_llm_calls": self.total_llm_calls,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "total_cost": self.total_cost,
            "models_used": self.models_used,
            "plugins_used": self.plugins_used,
            "functions_used": self.functions_used,
            "plans_executed": self.plans_executed,
            "plan_steps_executed": self.plan_steps_executed,
        }


# Session-level context variable
_current_session_context: contextvars.ContextVar[SemanticKernelSessionContext | None] = (
    contextvars.ContextVar("_current_semantic_kernel_session_context", default=None)
)


def get_session_context() -> SemanticKernelSessionContext | None:
    """
    Get the current session context.

    Returns:
        The current SemanticKernelSessionContext or None if not in a session.
    """
    return _current_session_context.get()


def set_session_context(context: SemanticKernelSessionContext | None) -> contextvars.Token:
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
    trace_name: str = "Semantic Kernel Session",
    trace_id: str | None = None,
) -> SemanticKernelSessionContext:
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
    context = SemanticKernelSessionContext(
        trace_id=trace_id or str(uuid.uuid4()),
        trace_name=trace_name,
    )
    _current_session_context.set(context)
    return context


@contextmanager
def semantic_kernel_session(
    trace_name: str = "Semantic Kernel Session",
    trace_id: str | None = None,
):
    """
    Context manager for explicit session scoping.

    Use this to explicitly define the boundaries of a session
    that should share a single trace.

    Example:
        with semantic_kernel_session("AI Assistant Session"):
            kernel.invoke(plugin.function1, ...)
            kernel.invoke(plugin.function2, ...)
            # Both invocations share the same trace

    Args:
        trace_name: Name for the trace.
        trace_id: Optional trace ID to use.

    Yields:
        The session context.
    """
    context = SemanticKernelSessionContext(
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
