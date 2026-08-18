"""Completion provider module."""

from importlib import import_module
from typing import TYPE_CHECKING, Any

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
    "OllamaCompletion",
    "OllamaCompletionConfig",
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

if TYPE_CHECKING:
    from mistralai.vibe.sdk.providers.completion.adapters import (
        AnthropicCompletion,
        MistralCompletion,
        OllamaCompletion,
        OpenAICompletion,
        OpenAIResponsesCompletion,
    )
    from mistralai.vibe.sdk.providers.completion.config import (
        AnthropicCompletionConfig,
        CompletionConfig,
        CompletionConfigBase,
        MistralCompletionConfig,
        OllamaCompletionConfig,
        OpenAICompletionConfig,
        OpenAIResponsesCompletionConfig,
        completion_config_from_obj,
        completion_from_config,
    )
    from mistralai.vibe.sdk.providers.completion.errors import (
        CompletionContextTooLargeError,
        is_context_too_large_error,
    )
    from mistralai.vibe.sdk.providers.completion.messages import (
        FunctionCall,
        Message,
        ToolCall,
    )
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

_LAZY_EXPORTS = {
    "AnthropicCompletion": "mistralai.vibe.sdk.providers.completion.adapters",
    "MistralCompletion": "mistralai.vibe.sdk.providers.completion.adapters",
    "OllamaCompletion": "mistralai.vibe.sdk.providers.completion.adapters",
    "OpenAICompletion": "mistralai.vibe.sdk.providers.completion.adapters",
    "OpenAIResponsesCompletion": "mistralai.vibe.sdk.providers.completion.adapters",
    "AnthropicCompletionConfig": "mistralai.vibe.sdk.providers.completion.config",
    "CompletionConfig": "mistralai.vibe.sdk.providers.completion.config",
    "CompletionConfigBase": "mistralai.vibe.sdk.providers.completion.config",
    "MistralCompletionConfig": "mistralai.vibe.sdk.providers.completion.config",
    "OllamaCompletionConfig": "mistralai.vibe.sdk.providers.completion.config",
    "OpenAICompletionConfig": "mistralai.vibe.sdk.providers.completion.config",
    "OpenAIResponsesCompletionConfig": "mistralai.vibe.sdk.providers.completion.config",
    "completion_config_from_obj": "mistralai.vibe.sdk.providers.completion.config",
    "completion_from_config": "mistralai.vibe.sdk.providers.completion.config",
    "CompletionContextTooLargeError": "mistralai.vibe.sdk.providers.completion.errors",
    "is_context_too_large_error": "mistralai.vibe.sdk.providers.completion.errors",
    "FunctionCall": "mistralai.vibe.sdk.providers.completion.messages",
    "Message": "mistralai.vibe.sdk.providers.completion.messages",
    "ToolCall": "mistralai.vibe.sdk.providers.completion.messages",
    "CompletionModel": "mistralai.vibe.sdk.providers.completion.port",
    "AGENT_COMPACTION_SENTINEL_TYPE": "mistralai.vibe.sdk.providers.completion.types",
    "COMPACTION_ANNOTATION": "mistralai.vibe.sdk.providers.completion.types",
    "COMPLETION_REQUEST_KIND_AGENT": "mistralai.vibe.sdk.providers.completion.types",
    "COMPLETION_REQUEST_KIND_COMPACTION": "mistralai.vibe.sdk.providers.completion.types",
    "COMPLETION_USAGE_ANNOTATION": "mistralai.vibe.sdk.providers.completion.types",
    "AgentCompactionSentinelContent": "mistralai.vibe.sdk.providers.completion.types",
    "CompactionAnnotation": "mistralai.vibe.sdk.providers.completion.types",
    "CompletionChunk": "mistralai.vibe.sdk.providers.completion.types",
    "CompletionRequest": "mistralai.vibe.sdk.providers.completion.types",
    "CompletionRequestKind": "mistralai.vibe.sdk.providers.completion.types",
    "FunctionSpec": "mistralai.vibe.sdk.providers.completion.types",
    "ToolCallDelta": "mistralai.vibe.sdk.providers.completion.types",
    "ToolDefinition": "mistralai.vibe.sdk.providers.completion.types",
    "TokenUsage": "mistralai.vibe.sdk.providers.completion.usage",
}


def __getattr__(name: str) -> Any:
    if name not in _LAZY_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    value = getattr(import_module(_LAZY_EXPORTS[name]), name)
    globals()[name] = value
    return value
