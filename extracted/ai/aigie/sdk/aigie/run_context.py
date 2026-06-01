"""
RunContext - Typed dependency injection for agent execution.

Provides type-safe access to dependencies and execution context
within agent tools using contextvars for async-safe propagation.

Example:
    ```python
    from aigie import Agent, RunContext

    class MyDeps:
        db: Database
        api_client: APIClient

    agent = Agent[MyDeps, str]('openai:gpt-4')

    @agent.tool
    async def search(ctx: RunContext[MyDeps], query: str) -> str:
        # Type-safe access to dependencies
        return await ctx.deps.db.search(query)
    ```
"""

from __future__ import annotations

import contextvars
from dataclasses import dataclass, field
from datetime import datetime
from typing import (
    Any,
    Generic,
    TypeVar,
)

# Type variable for dependencies (covariant for subtype compatibility)
DepsT = TypeVar("DepsT")


@dataclass
class Message:
    """Represents a message in the conversation history."""

    role: str  # 'system', 'user', 'assistant', 'tool'
    content: str
    name: str | None = None
    tool_call_id: str | None = None
    tool_calls: list[dict[str, Any]] | None = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for API calls."""
        result = {"role": self.role, "content": self.content}
        if self.name:
            result["name"] = self.name
        if self.tool_call_id:
            result["tool_call_id"] = self.tool_call_id
        if self.tool_calls:
            result["tool_calls"] = self.tool_calls
        return result


@dataclass
class RunContext(Generic[DepsT]):
    """
    Context for agent execution with typed dependencies.

    RunContext is passed to tool functions and provides:
    - Type-safe access to dependencies via `ctx.deps`
    - Access to the current model and messages
    - Helper methods for message management
    - Retry signaling capability

    The context is automatically propagated via contextvars, so nested
    tool calls have access to the same context without explicit passing.

    Attributes:
        deps: The typed dependencies passed to the agent
        model: The model identifier (e.g., 'openai:gpt-4')
        messages: The conversation history
        tool_call_id: ID of the current tool call (if in tool execution)
        trace_id: ID of the current trace for observability
        span_id: ID of the current span for observability
        retry_count: Number of retries attempted
        max_retries: Maximum retries allowed
        last_attempt: Whether this is the last retry attempt

    Example:
        ```python
        @agent.tool
        async def get_weather(ctx: RunContext[MyDeps], location: str) -> str:
            # Access typed dependencies
            weather = await ctx.deps.weather_api.get(location)

            # Check if last attempt for different behavior
            if ctx.last_attempt:
                return f"Weather data may be stale: {weather}"

            return weather
        ```
    """

    deps: DepsT
    model: str
    messages: list[Message] = field(default_factory=list)
    tool_call_id: str | None = None
    trace_id: str | None = None
    span_id: str | None = None
    retry_count: int = 0
    max_retries: int = 2
    metadata: dict[str, Any] = field(default_factory=dict)
    _message_index: int = 0  # Track where new messages start

    @property
    def last_attempt(self) -> bool:
        """Check if this is the last retry attempt."""
        return self.retry_count >= self.max_retries

    def all_messages(self) -> list[Message]:
        """
        Get all messages in the conversation history.

        Returns:
            Complete list of messages from conversation start.
        """
        return list(self.messages)

    def new_messages(self, after_index: int | None = None) -> list[Message]:
        """
        Get messages added after a specific point.

        Args:
            after_index: Index to start from. If None, uses internal tracker.

        Returns:
            List of messages added after the specified index.
        """
        index = after_index if after_index is not None else self._message_index
        return list(self.messages[index:])

    def add_message(self, message: Message) -> None:
        """Add a message to the conversation history."""
        self.messages.append(message)

    def add_user_message(self, content: str) -> None:
        """Add a user message to the conversation."""
        self.add_message(Message(role="user", content=content))

    def add_assistant_message(self, content: str) -> None:
        """Add an assistant message to the conversation."""
        self.add_message(Message(role="assistant", content=content))

    def add_tool_result(self, tool_call_id: str, content: str, name: str | None = None) -> None:
        """Add a tool result message to the conversation."""
        self.add_message(
            Message(
                role="tool",
                content=content,
                tool_call_id=tool_call_id,
                name=name,
            )
        )

    def mark_message_index(self) -> int:
        """
        Mark the current message index for later retrieval.

        Returns:
            The current message index.
        """
        self._message_index = len(self.messages)
        return self._message_index

    def get_messages_for_api(self) -> list[dict[str, Any]]:
        """Get messages formatted for LLM API calls."""
        return [msg.to_dict() for msg in self.messages]

    def with_retry(self) -> RunContext[DepsT]:
        """Create a new context for a retry attempt."""
        return RunContext(
            deps=self.deps,
            model=self.model,
            messages=self.messages.copy(),
            tool_call_id=self.tool_call_id,
            trace_id=self.trace_id,
            span_id=self.span_id,
            retry_count=self.retry_count + 1,
            max_retries=self.max_retries,
            metadata=self.metadata.copy(),
            _message_index=self._message_index,
        )


# ContextVar for async-safe context propagation
_current_context: contextvars.ContextVar[RunContext[Any] | None] = contextvars.ContextVar(
    "aigie_run_context", default=None
)


def get_current_context() -> RunContext[Any]:
    """
    Get the current RunContext from the async context.

    Returns:
        The active RunContext.

    Raises:
        RuntimeError: If no context is active.
    """
    ctx = _current_context.get()
    if ctx is None:
        raise RuntimeError(
            "No active RunContext. This function must be called within an agent run."
        )
    return ctx


def get_current_context_or_none() -> RunContext[Any] | None:
    """
    Get the current RunContext if one exists.

    Returns:
        The active RunContext or None.
    """
    return _current_context.get()


def set_current_context(ctx: RunContext[Any]) -> contextvars.Token:
    """
    Set the current RunContext.

    Args:
        ctx: The RunContext to set.

    Returns:
        A token for restoring the previous context.
    """
    return _current_context.set(ctx)


def reset_current_context(token: contextvars.Token) -> None:
    """
    Reset the context to its previous value.

    Args:
        token: The token from set_current_context.
    """
    _current_context.reset(token)


class run_context:
    """
    Context manager for setting the RunContext.

    Example:
        ```python
        ctx = RunContext(deps=my_deps, model='openai:gpt-4')

        async with run_context(ctx):
            # All nested calls can access ctx via get_current_context()
            result = await my_tool_function()
        ```
    """

    def __init__(self, ctx: RunContext[Any]):
        self.ctx = ctx
        self.token: contextvars.Token | None = None

    def __enter__(self) -> RunContext[Any]:
        self.token = set_current_context(self.ctx)
        return self.ctx

    def __exit__(self, *args: Any) -> None:
        if self.token is not None:
            reset_current_context(self.token)

    async def __aenter__(self) -> RunContext[Any]:
        self.token = set_current_context(self.ctx)
        return self.ctx

    async def __aexit__(self, *args: Any) -> None:
        if self.token is not None:
            reset_current_context(self.token)


class ModelRetry(Exception):
    """
    Signal to retry the model with feedback.

    Raise this from a tool or validator to trigger a retry with
    an error message that will be fed back to the model.

    Example:
        ```python
        @agent.tool
        async def validate_data(ctx: RunContext[Deps], data: str) -> str:
            if not is_valid(data):
                raise ModelRetry("Data format is invalid. Please use JSON format.")
            return process(data)
        ```
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


__all__ = [
    "DepsT",
    "Message",
    "ModelRetry",
    "RunContext",
    "get_current_context",
    "get_current_context_or_none",
    "reset_current_context",
    "run_context",
    "set_current_context",
]
