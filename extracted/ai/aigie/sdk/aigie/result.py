"""
AgentResult - Structured result objects for agent execution.

Provides typed, structured results from agent runs including:
- Validated output data
- Usage information (tokens, cost)
- Conversation history
- Helper methods for continuation

Example:
    ```python
    result = await agent.run("What is AI?", deps=my_deps)

    # Access typed data
    print(result.data.answer)

    # Check usage
    print(f"Cost: ${result.usage.cost_usd:.4f}")

    # Continue conversation
    new_result = await agent.run(
        "Tell me more",
        message_history=result.all_messages()
    )
    ```
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Generic, TypeVar

from aigie.run_context import Message

# Type variable for result data
T = TypeVar("T")


@dataclass
class UsageInfo:
    """
    Token usage and cost information for an agent run.

    Tracks token counts from the LLM API and calculates
    estimated costs based on model pricing.

    Attributes:
        request_tokens: Number of input/prompt tokens
        response_tokens: Number of output/completion tokens
        total_tokens: Total tokens used (request + response)
        cost_usd: Estimated cost in USD
        cache_read_tokens: Tokens read from cache (if applicable)
        cache_creation_tokens: Tokens used to create cache
        model: The model used for the request

    Example:
        ```python
        usage = result.usage
        print(f"Tokens: {usage.total_tokens}")
        print(f"Cost: ${usage.cost_usd:.4f}")
        ```
    """

    request_tokens: int = 0
    response_tokens: int = 0
    total_tokens: int = 0
    cost_usd: float = 0.0
    cache_read_tokens: int = 0
    cache_creation_tokens: int = 0
    model: str | None = None

    def __add__(self, other: UsageInfo) -> UsageInfo:
        """Combine usage from multiple requests."""
        return UsageInfo(
            request_tokens=self.request_tokens + other.request_tokens,
            response_tokens=self.response_tokens + other.response_tokens,
            total_tokens=self.total_tokens + other.total_tokens,
            cost_usd=self.cost_usd + other.cost_usd,
            cache_read_tokens=self.cache_read_tokens + other.cache_read_tokens,
            cache_creation_tokens=self.cache_creation_tokens + other.cache_creation_tokens,
            model=self.model or other.model,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "request_tokens": self.request_tokens,
            "response_tokens": self.response_tokens,
            "total_tokens": self.total_tokens,
            "cost_usd": self.cost_usd,
            "cache_read_tokens": self.cache_read_tokens,
            "cache_creation_tokens": self.cache_creation_tokens,
            "model": self.model,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UsageInfo:
        """Create from dictionary."""
        return cls(
            request_tokens=data.get("request_tokens", 0),
            response_tokens=data.get("response_tokens", 0),
            total_tokens=data.get("total_tokens", 0),
            cost_usd=data.get("cost_usd", 0.0),
            cache_read_tokens=data.get("cache_read_tokens", 0),
            cache_creation_tokens=data.get("cache_creation_tokens", 0),
            model=data.get("model"),
        )


@dataclass
class AgentResult(Generic[T]):
    """
    Structured result from an agent execution.

    Contains the validated output data, usage information,
    and conversation history for continuation.

    Attributes:
        data: The validated output (typed as T)
        usage: Token usage and cost information
        messages: Complete conversation history
        model: The model used for generation
        trace_id: Trace ID for observability
        duration_ms: Execution duration in milliseconds
        tool_calls: Number of tool calls made
        retries: Number of retries attempted
        metadata: Additional metadata from the run

    Example:
        ```python
        result = await agent.run("Analyze this data", deps=deps)

        # Access typed data
        analysis = result.data

        # Check performance
        print(f"Duration: {result.duration_ms}ms")
        print(f"Tool calls: {result.tool_calls}")

        # Continue conversation
        followup = await agent.run(
            "Explain more about point 3",
            message_history=result.all_messages()
        )
        ```
    """

    data: T
    usage: UsageInfo = field(default_factory=UsageInfo)
    messages: list[Message] = field(default_factory=list)
    model: str | None = None
    trace_id: str | None = None
    duration_ms: float = 0.0
    tool_calls: int = 0
    retries: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def all_messages(self) -> list[Message]:
        """
        Get all messages from the conversation.

        Returns:
            Complete list of messages.
        """
        return list(self.messages)

    def all_messages_dict(self) -> list[dict[str, Any]]:
        """
        Get all messages as dictionaries for API calls.

        Returns:
            Messages formatted for LLM APIs.
        """
        return [msg.to_dict() for msg in self.messages]

    def with_tool_return_content(
        self, content: str, tool_call_id: str | None = None
    ) -> list[Message]:
        """
        Modify the last tool return for conversation continuation.

        Useful for correcting or adjusting tool outputs before
        continuing the conversation.

        Args:
            content: New content for the tool return
            tool_call_id: Optional specific tool call ID to modify

        Returns:
            Modified message list for continuation.

        Example:
            ```python
            # Modify tool output for retry
            modified = result.with_tool_return_content(
                "Please try a different approach"
            )
            new_result = await agent.run(
                "Continue",
                message_history=modified
            )
            ```
        """
        messages = [msg for msg in self.messages]

        # Find the tool return to modify
        for i in range(len(messages) - 1, -1, -1):
            msg = messages[i]
            if msg.role == "tool":
                if tool_call_id is None or msg.tool_call_id == tool_call_id:
                    messages[i] = Message(
                        role="tool",
                        content=content,
                        tool_call_id=msg.tool_call_id,
                        name=msg.name,
                        timestamp=msg.timestamp,
                        metadata=msg.metadata,
                    )
                    break

        return messages

    def to_dict(self) -> dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "data": self.data
            if isinstance(self.data, (dict, str, int, float, bool, list))
            else str(self.data),
            "usage": self.usage.to_dict(),
            "messages": [msg.to_dict() for msg in self.messages],
            "model": self.model,
            "trace_id": self.trace_id,
            "duration_ms": self.duration_ms,
            "tool_calls": self.tool_calls,
            "retries": self.retries,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class StreamedRunResult(Generic[T]):
    """
    Result from a streaming agent run.

    Wraps the final result after streaming completes,
    providing the same interface as AgentResult plus
    streaming-specific metadata.

    Attributes:
        data: The validated output (typed as T)
        usage: Token usage and cost information
        messages: Complete conversation history
        chunks_count: Number of streamed chunks
        ttft_ms: Time to first token in milliseconds
    """

    data: T
    usage: UsageInfo = field(default_factory=UsageInfo)
    messages: list[Message] = field(default_factory=list)
    model: str | None = None
    trace_id: str | None = None
    duration_ms: float = 0.0
    chunks_count: int = 0
    ttft_ms: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_agent_result(self) -> AgentResult[T]:
        """Convert to standard AgentResult."""
        return AgentResult(
            data=self.data,
            usage=self.usage,
            messages=self.messages,
            model=self.model,
            trace_id=self.trace_id,
            duration_ms=self.duration_ms,
            metadata={
                **self.metadata,
                "chunks_count": self.chunks_count,
                "ttft_ms": self.ttft_ms,
            },
        )


class UnifiedError(Exception):
    """
    Unified error type for agent execution.

    Wraps various error types with consistent metadata
    for better error handling and debugging.

    Attributes:
        message: Human-readable error message
        error_type: Category of error
        original_error: The underlying exception
        trace_id: Trace ID for debugging
        tool_name: Name of the tool that failed (if applicable)
        retry_count: Number of retries attempted
    """

    def __init__(
        self,
        message: str,
        error_type: str = "agent_error",
        original_error: Exception | None = None,
        trace_id: str | None = None,
        tool_name: str | None = None,
        retry_count: int = 0,
    ):
        self.message = message
        self.error_type = error_type
        self.original_error = original_error
        self.trace_id = trace_id
        self.tool_name = tool_name
        self.retry_count = retry_count
        super().__init__(message)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for logging/tracing."""
        return {
            "message": self.message,
            "error_type": self.error_type,
            "original_error": str(self.original_error) if self.original_error else None,
            "trace_id": self.trace_id,
            "tool_name": self.tool_name,
            "retry_count": self.retry_count,
        }


__all__ = [
    "AgentResult",
    "StreamedRunResult",
    "T",
    "UnifiedError",
    "UsageInfo",
]
