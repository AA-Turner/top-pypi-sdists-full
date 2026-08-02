"""Shared message types in OpenAI/Mistral standard format.

These types are the lingua franca for LLM API communication.
Used by both completion and tool execution domains.
"""

from typing import Literal

from pydantic import BaseModel


class FunctionCall(BaseModel):
    """A function call within a tool call."""

    name: str
    arguments: str  # JSON-encoded string, matching OpenAI/Mistral convention


class ToolCall(BaseModel):
    """A tool call within an assistant message."""

    id: str
    type: Literal["function"] = "function"
    function: FunctionCall


class Message(BaseModel):
    """A message in OpenAI/Mistral standard format.

    This is the universal message type that all adapters understand.
    """

    role: Literal["system", "user", "assistant", "tool"]
    content: str | None = None
    tool_calls: list[ToolCall] | None = None
    tool_call_id: str | None = None


__all__ = ["FunctionCall", "Message", "ToolCall"]
