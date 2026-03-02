"""LLM provider abstraction layer using OpenAI SDK."""

from .base import LLMProvider, LLMResponse, ToolCall
from .models import ChatModelSpec, ModelRegistry, ModelEntry, ProviderConfig
from .openai_provider import OpenAIProvider
from .factory import (
    get_provider,
    get_default_model,
    get_default_api_key,
    list_available_models,
    DEFAULT_MODEL,
    DEFAULT_API_KEY_ENV,
)

__all__ = [
    # Base
    "LLMProvider",
    "LLMResponse",
    "ToolCall",
    # Models
    "ChatModelSpec",
    "ModelRegistry",
    "ModelEntry",
    "ProviderConfig",
    # Providers
    "OpenAIProvider",
    # Factory
    "get_provider",
    "get_default_model",
    "get_default_api_key",
    "list_available_models",
    "DEFAULT_MODEL",
    "DEFAULT_API_KEY_ENV",
]
