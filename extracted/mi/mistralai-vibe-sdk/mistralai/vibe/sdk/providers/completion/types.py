"""Completion domain: types and converters.

Handles the standardized interface for LLM completion calls.
Types only — no capability imports. Bridge functions live in patterns/completion/bridge.py.
"""

from typing import Any, Literal

from pydantic import BaseModel

from mistralai.vibe.sdk.providers.completion.messages import Message
from mistralai.vibe.sdk.providers.completion.usage import TokenUsage

# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

CompletionRequestKind = Literal["agent", "compaction"]

COMPLETION_REQUEST_KIND_AGENT: CompletionRequestKind = "agent"
COMPLETION_REQUEST_KIND_COMPACTION: CompletionRequestKind = "compaction"

AGENT_COMPACTION_SENTINEL_TYPE = "agent.compaction"
COMPLETION_USAGE_ANNOTATION = "usage"
COMPACTION_ANNOTATION = "compaction"


class AgentCompactionSentinelContent(BaseModel):
    """Content shape for an agent compaction ``StateEntry`` sentinel.

    Canonical history entry shape:
    ``StateEntryPayload(type="agent.compaction", content={"summary": "..."})``.

    The completion bridge uses this entry as the projection boundary and
    renders ``summary`` as a user message before entries recorded after the
    sentinel.
    """

    summary: str


class CompactionAnnotation(BaseModel):
    """Lifecycle metadata attached to a compaction sentinel under the
    ``COMPACTION_ANNOTATION`` key.
    """

    status: Literal["running", "completed", "failed"]
    threshold: int
    old_context_tokens: int
    new_context_tokens: int | None = None
    summary_length: int | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    error: str | None = None


class FunctionSpec(BaseModel):
    """Function specification within a tool definition."""

    name: str
    description: str
    parameters: dict[str, Any]


class ToolDefinition(BaseModel):
    """A tool definition in OpenAI/Mistral standard format."""

    type: str = "function"
    function: FunctionSpec


class CompletionRequest(BaseModel):
    """Standardized completion request.

    Contains everything needed to call any LLM API.
    The adapter maps this to its specific SDK types.
    """

    messages: list[Message]
    tools: list[ToolDefinition] | None = None
    metadata: dict[str, Any] | None = None
    request_kind: CompletionRequestKind = COMPLETION_REQUEST_KIND_AGENT


# ---------------------------------------------------------------------------
# Streaming chunk types
# ---------------------------------------------------------------------------


class ToolCallDelta(BaseModel):
    """A delta for a single tool call within a streaming chunk.

    Tool calls arrive incrementally: the first delta for a given index
    carries id and function_name; subsequent deltas carry argument fragments.
    The consumer accumulates arguments_delta strings and JSON-parses at the end.
    """

    index: int
    id: str | None = None
    function_name: str | None = None
    arguments_delta: str | None = None


class CompletionChunk(BaseModel):
    """Standardized streaming chunk from an LLM completion.

    Provider-independent: adapters for Mistral, OpenAI, and Anthropic
    all convert their native streaming format into this type.
    See documentation/streaming_api_comparison.md for the mapping.
    """

    content_delta: str | None = None
    thinking_delta: str | None = None
    tool_call_deltas: list[ToolCallDelta] | None = None
    finish_reason: str | None = None
    usage: TokenUsage | None = None


__all__ = [
    "AGENT_COMPACTION_SENTINEL_TYPE",
    "COMPACTION_ANNOTATION",
    "COMPLETION_REQUEST_KIND_AGENT",
    "COMPLETION_REQUEST_KIND_COMPACTION",
    "COMPLETION_USAGE_ANNOTATION",
    "AgentCompactionSentinelContent",
    "CompactionAnnotation",
    "CompletionChunk",
    "CompletionRequest",
    "CompletionRequestKind",
    "FunctionSpec",
    "ToolCallDelta",
    "ToolDefinition",
]
