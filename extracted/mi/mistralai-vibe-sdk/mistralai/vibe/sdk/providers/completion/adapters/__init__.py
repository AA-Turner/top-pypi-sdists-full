"""Completion adapters — concrete implementations of CompletionModel."""

from mistralai.vibe.sdk.providers.completion.adapters.anthropic import AnthropicCompletion
from mistralai.vibe.sdk.providers.completion.adapters.mistral import MistralCompletion
from mistralai.vibe.sdk.providers.completion.adapters.openai import OpenAICompletion
from mistralai.vibe.sdk.providers.completion.adapters.openai_responses import (
    OpenAIResponsesCompletion,
)

__all__ = [
    "AnthropicCompletion",
    "MistralCompletion",
    "OpenAICompletion",
    "OpenAIResponsesCompletion",
]
