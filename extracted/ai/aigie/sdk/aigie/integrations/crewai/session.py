"""
CrewAI session context management.

Provides trace context propagation using Python's contextvars,
enabling all operations in a session to share the same trace.
"""

import contextvars
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any


@dataclass
class CrewAISessionContext:
    """
    Holds shared state across all handlers in a CrewAI session.

    This enables trace_id, task counts, and aggregated metrics
    to persist across multiple crew kickoffs.
    """

    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_name: str = "CrewAI Session"
    total_crew_runs: int = 0
    total_tasks: int = 0
    total_steps: int = 0
    total_llm_calls: int = 0
    total_tool_calls: int = 0
    total_delegations: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost: float = 0.0
    trace_created: bool = False
    current_crew_span_id: str | None = None
    current_task_span_id: str | None = None
    # Parent span tracking for proper hierarchy
    current_parent_span_id: str | None = None
    # Model tracking
    current_model: str | None = None
    models_used: dict[str, int] = field(default_factory=dict)
    # Agent tracking
    agents_used: dict[str, int] = field(default_factory=dict)
    # Task tracking
    tasks_completed: int = 0
    tasks_failed: int = 0
    # Tool tracking
    tools_used: dict[str, int] = field(default_factory=dict)

    def increment_crew_run(self) -> int:
        """Increment and return the new crew run count."""
        self.total_crew_runs += 1
        return self.total_crew_runs

    def increment_task(self, completed: bool = True) -> int:
        """Increment and return the new task count."""
        self.total_tasks += 1
        if completed:
            self.tasks_completed += 1
        else:
            self.tasks_failed += 1
        return self.total_tasks

    def increment_step(self) -> int:
        """Increment and return the new step count."""
        self.total_steps += 1
        return self.total_steps

    def increment_llm_call(self) -> int:
        """Increment and return the new LLM call count."""
        self.total_llm_calls += 1
        return self.total_llm_calls

    def increment_tool_call(self, tool_name: str | None = None) -> int:
        """Increment and return the new tool call count."""
        self.total_tool_calls += 1
        if tool_name:
            self.tools_used[tool_name] = self.tools_used.get(tool_name, 0) + 1
        return self.total_tool_calls

    def increment_delegation(self) -> int:
        """Increment and return the new delegation count."""
        self.total_delegations += 1
        return self.total_delegations

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

    def track_agent(self, agent_name: str) -> None:
        """Track agent participation."""
        if agent_name:
            self.agents_used[agent_name] = self.agents_used.get(agent_name, 0) + 1

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
            "total_crew_runs": self.total_crew_runs,
            "total_tasks": self.total_tasks,
            "tasks_completed": self.tasks_completed,
            "tasks_failed": self.tasks_failed,
            "task_success_rate": self.tasks_completed / max(self.total_tasks, 1),
            "total_steps": self.total_steps,
            "total_llm_calls": self.total_llm_calls,
            "total_tool_calls": self.total_tool_calls,
            "total_delegations": self.total_delegations,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "total_cost": self.total_cost,
            "models_used": self.models_used,
            "agents_used": self.agents_used,
            "tools_used": self.tools_used,
        }


# Session-level context variable
_current_session_context: contextvars.ContextVar[CrewAISessionContext | None] = (
    contextvars.ContextVar("_current_crewai_session_context", default=None)
)


def get_session_context() -> CrewAISessionContext | None:
    """
    Get the current session context.

    Returns:
        The current CrewAISessionContext or None if not in a session.
    """
    return _current_session_context.get()


def set_session_context(context: CrewAISessionContext | None) -> contextvars.Token:
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
    trace_name: str = "CrewAI Session",
    trace_id: str | None = None,
) -> CrewAISessionContext:
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
    context = CrewAISessionContext(
        trace_id=trace_id or str(uuid.uuid4()),
        trace_name=trace_name,
    )
    _current_session_context.set(context)
    return context


@contextmanager
def crewai_session(
    trace_name: str = "CrewAI Session",
    trace_id: str | None = None,
):
    """
    Context manager for explicit session scoping.

    Use this to explicitly define the boundaries of a session
    that should share a single trace.

    Example:
        with crewai_session("Research Crew Session"):
            crew.kickoff(inputs={"topic": "AI"})
            crew.kickoff(inputs={"topic": "ML"})
            # Both kickoffs share the same trace

    Args:
        trace_name: Name for the trace.
        trace_id: Optional trace ID to use.

    Yields:
        The session context.
    """
    context = CrewAISessionContext(
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
