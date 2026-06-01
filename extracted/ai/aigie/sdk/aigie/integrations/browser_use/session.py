"""
Browser Use session context management.

Provides trace context propagation using Python's contextvars,
enabling all operations in a session to share the same trace.
"""

import contextvars
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any


@dataclass
class BrowserUseSessionContext:
    """
    Holds shared state across all handlers in a Browser Use session.

    This enables trace_id, action counts, and aggregated metrics
    to persist across multiple browser automation invocations.
    """

    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_name: str = "Browser Use Session"
    total_tasks: int = 0
    total_actions: int = 0
    total_navigation_actions: int = 0
    total_click_actions: int = 0
    total_input_actions: int = 0
    total_extract_actions: int = 0
    total_screenshots: int = 0
    total_llm_calls: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost: float = 0.0
    trace_created: bool = False
    current_task_span_id: str | None = None
    current_action_span_id: str | None = None
    # Parent span tracking for proper hierarchy
    current_parent_span_id: str | None = None
    # Model tracking
    current_model: str | None = None
    # Page tracking
    pages_visited: list[str] = field(default_factory=list)
    # Error tracking
    total_errors: int = 0
    total_retries: int = 0

    def increment_task(self) -> int:
        """Increment and return the new task count."""
        self.total_tasks += 1
        return self.total_tasks

    def increment_action(self, action_type: str = "generic") -> int:
        """Increment and return the new action count."""
        self.total_actions += 1
        if action_type == "navigation":
            self.total_navigation_actions += 1
        elif action_type == "click":
            self.total_click_actions += 1
        elif action_type == "input":
            self.total_input_actions += 1
        elif action_type == "extract":
            self.total_extract_actions += 1
        return self.total_actions

    def increment_screenshot(self) -> int:
        """Increment and return the new screenshot count."""
        self.total_screenshots += 1
        return self.total_screenshots

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

    def add_page_visited(self, url: str) -> None:
        """Track a page visit."""
        if url and url not in self.pages_visited:
            self.pages_visited.append(url)

    def increment_error(self) -> int:
        """Increment and return the new error count."""
        self.total_errors += 1
        return self.total_errors

    def increment_retry(self) -> int:
        """Increment and return the new retry count."""
        self.total_retries += 1
        return self.total_retries

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
            "total_tasks": self.total_tasks,
            "total_actions": self.total_actions,
            "action_breakdown": {
                "navigation": self.total_navigation_actions,
                "click": self.total_click_actions,
                "input": self.total_input_actions,
                "extract": self.total_extract_actions,
            },
            "total_screenshots": self.total_screenshots,
            "total_llm_calls": self.total_llm_calls,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "total_cost": self.total_cost,
            "pages_visited": len(self.pages_visited),
            "total_errors": self.total_errors,
            "total_retries": self.total_retries,
        }


# Session-level context variable
_current_session_context: contextvars.ContextVar[BrowserUseSessionContext | None] = (
    contextvars.ContextVar("_current_browser_use_session_context", default=None)
)


def get_session_context() -> BrowserUseSessionContext | None:
    """
    Get the current session context.

    Returns:
        The current BrowserUseSessionContext or None if not in a session.
    """
    return _current_session_context.get()


def set_session_context(context: BrowserUseSessionContext | None) -> contextvars.Token:
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
    trace_name: str = "Browser Use Session",
    trace_id: str | None = None,
) -> BrowserUseSessionContext:
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
    context = BrowserUseSessionContext(
        trace_id=trace_id or str(uuid.uuid4()),
        trace_name=trace_name,
    )
    _current_session_context.set(context)
    return context


@contextmanager
def browser_use_session(
    trace_name: str = "Browser Use Session",
    trace_id: str | None = None,
):
    """
    Context manager for explicit session scoping.

    Use this to explicitly define the boundaries of a session
    that should share a single trace.

    Example:
        with browser_use_session("Web Scraping Session"):
            agent.run("Go to example.com")
            agent.run("Click the login button")
            # Both invocations share the same trace

    Args:
        trace_name: Name for the trace.
        trace_id: Optional trace ID to use.

    Yields:
        The session context.
    """
    context = BrowserUseSessionContext(
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
