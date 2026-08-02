"""Completion provider module."""

from mistralai.vibe.sdk.providers.completion.adapters import (
    AnthropicCompletion,
    MistralCompletion,
    OpenAICompletion,
    OpenAIResponsesCompletion,
)
from mistralai.vibe.sdk.providers.completion.config import (
    AnthropicCompletionConfig,
    CompletionConfig,
    CompletionConfigBase,
    MistralCompletionConfig,
    OpenAICompletionConfig,
    OpenAIResponsesCompletionConfig,
    completion_config_from_obj,
    completion_from_config,
)
from mistralai.vibe.sdk.providers.completion.errors import (
    CompletionContextTooLargeError,
    is_context_too_large_error,
)
from mistralai.vibe.sdk.providers.completion.messages import FunctionCall, Message, ToolCall
from mistralai.vibe.sdk.providers.completion.port import CompletionModel
from mistralai.vibe.sdk.providers.completion.types import (
    AGENT_COMPACTION_SENTINEL_TYPE,
    COMPACTION_ANNOTATION,
    COMPLETION_REQUEST_KIND_AGENT,
    COMPLETION_REQUEST_KIND_COMPACTION,
    COMPLETION_USAGE_ANNOTATION,
    AgentCompactionSentinelContent,
    CompactionAnnotation,
    CompletionChunk,
    CompletionRequest,
    CompletionRequestKind,
    FunctionSpec,
    ToolCallDelta,
    ToolDefinition,
)
from mistralai.vibe.sdk.providers.completion.usage import TokenUsage

__all__ = [
    "AGENT_COMPACTION_SENTINEL_TYPE",
    "COMPACTION_ANNOTATION",
    "COMPLETION_REQUEST_KIND_AGENT",
    "COMPLETION_REQUEST_KIND_COMPACTION",
    "AnthropicCompletion",
    "AnthropicCompletionConfig",
    "AgentCompactionSentinelContent",
    "CompactionAnnotation",
    "COMPLETION_USAGE_ANNOTATION",
    "CompletionChunk",
    "CompletionRequestKind",
    "CompletionConfig",
    "CompletionConfigBase",
    "CompletionContextTooLargeError",
    "CompletionModel",
    "CompletionRequest",
    "FunctionCall",
    "FunctionSpec",
    "Message",
    "MistralCompletion",
    "MistralCompletionConfig",
    "OpenAICompletion",
    "OpenAICompletionConfig",
    "OpenAIResponsesCompletion",
    "OpenAIResponsesCompletionConfig",
    "TokenUsage",
    "ToolCall",
    "ToolCallDelta",
    "ToolDefinition",
    "completion_config_from_obj",
    "completion_from_config",
    "is_context_too_large_error",
]
