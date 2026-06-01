"""
OpenAI Agents session context management.

Provides trace context propagation using Python's contextvars,
enabling all operations in a session to share the same trace.
"""

import contextvars
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any


@dataclass
class OpenAIAgentsSessionContext:
    """
    Holds shared state across all handlers in an OpenAI Agents session.

    This enables trace_id, workflow counts, and aggregated metrics
    to persist across multiple agent workflow runs.
    """

    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_name: str = "OpenAI Agents Session"
    total_workflows: int = 0
    total_agent_runs: int = 0
    total_generations: int = 0
    total_tool_calls: int = 0
    total_handoffs: int = 0
    total_guardrail_checks: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost: float = 0.0
    trace_created: bool = False
    current_workflow_span_id: str | None = None
    current_agent_span_id: str | None = None
    # Parent span tracking for proper hierarchy
    current_parent_span_id: str | None = None
    # Model tracking
    current_model: str | None = None
    models_used: dict[str, int] = field(default_factory=dict)
    # Agent tracking
    agents_used: dict[str, int] = field(default_factory=dict)
    # Tool tracking
    tools_used: dict[str, int] = field(default_factory=dict)
    # Handoff tracking
    handoffs_by_agent: dict[str, int] = field(default_factory=dict)
    # Guardrail tracking
    guardrail_blocks: int = 0
    guardrail_passes: int = 0

    def increment_workflow(self) -> int:
        """Increment and return the new workflow count."""
        self.total_workflows += 1
        return self.total_workflows

    def increment_agent_run(self, agent_name: str | None = None) -> int:
        """Increment agent run count and track agent."""
        self.total_agent_runs += 1
        if agent_name:
            self.agents_used[agent_name] = self.agents_used.get(agent_name, 0) + 1
        return self.total_agent_runs

    def increment_generation(self) -> int:
        """Increment and return the new generation count."""
        self.total_generations += 1
        return self.total_generations

    def increment_tool_call(self, tool_name: str | None = None) -> int:
        """Increment tool call count and track tool."""
        self.total_tool_calls += 1
        if tool_name:
            self.tools_used[tool_name] = self.tools_used.get(tool_name, 0) + 1
        return self.total_tool_calls

    def increment_handoff(self, from_agent: str | None = None) -> int:
        """Increment handoff count and track source agent."""
        self.total_handoffs += 1
        if from_agent:
            self.handoffs_by_agent[from_agent] = self.handoffs_by_agent.get(from_agent, 0) + 1
        return self.total_handoffs

    def increment_guardrail_check(self, blocked: bool = False) -> int:
        """Increment guardrail check count and track result."""
        self.total_guardrail_checks += 1
        if blocked:
            self.guardrail_blocks += 1
        else:
            self.guardrail_passes += 1
        return self.total_guardrail_checks

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
            "total_workflows": self.total_workflows,
            "total_agent_runs": self.total_agent_runs,
            "total_generations": self.total_generations,
            "total_tool_calls": self.total_tool_calls,
            "total_handoffs": self.total_handoffs,
            "total_guardrail_checks": self.total_guardrail_checks,
            "guardrail_block_rate": self.guardrail_blocks / max(self.total_guardrail_checks, 1),
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "total_cost": self.total_cost,
            "models_used": self.models_used,
            "agents_used": self.agents_used,
            "tools_used": self.tools_used,
            "handoffs_by_agent": self.handoffs_by_agent,
        }


# Session-level context variable
_current_session_context: contextvars.ContextVar[OpenAIAgentsSessionContext | None] = (
    contextvars.ContextVar("_current_openai_agents_session_context", default=None)
)


def get_session_context() -> OpenAIAgentsSessionContext | None:
    """
    Get the current session context.

    Returns:
        The current OpenAIAgentsSessionContext or None if not in a session.
    """
    return _current_session_context.get()


def set_session_context(context: OpenAIAgentsSessionContext | None) -> contextvars.Token:
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
    trace_name: str = "OpenAI Agents Session",
    trace_id: str | None = None,
) -> OpenAIAgentsSessionContext:
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
    context = OpenAIAgentsSessionContext(
        trace_id=trace_id or str(uuid.uuid4()),
        trace_name=trace_name,
    )
    _current_session_context.set(context)
    return context


@contextmanager
def openai_agents_session(
    trace_name: str = "OpenAI Agents Session",
    trace_id: str | None = None,
):
    """
    Context manager for explicit session scoping.

    Use this to explicitly define the boundaries of a session
    that should share a single trace.

    Example:
        with openai_agents_session("Customer Support Session"):
            Runner.run(triage_agent, "I need help")
            Runner.run(support_agent, "Follow-up question")
            # Both runs share the same trace

    Args:
        trace_name: Name for the trace.
        trace_id: Optional trace ID to use.

    Yields:
        The session context.
    """
    context = OpenAIAgentsSessionContext(
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
