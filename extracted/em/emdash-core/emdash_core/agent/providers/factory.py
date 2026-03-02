"""Factory for creating LLM providers."""
import os
from typing import Union

from .base import LLMProvider
from .models import ModelRegistry, ModelEntry
from .openai_provider import OpenAIProvider


# ═══════════════════════════════════════════════════════════════════════════════
# Configuration - Single source of truth
# ═══════════════════════════════════════════════════════════════════════════════

def _get_default_model_name() -> str:
    """Get default model name from registry config."""
    return ModelRegistry.get().default_model


def _get_vision_model_name() -> str:
    """Get vision model name from registry config."""
    return ModelRegistry.get().vision_model


# Sentinel values — do NOT evaluate at import time because the ModelRegistry
# singleton may not have loaded the correct project config yet.
# All runtime resolution goes through _get_default_model_name() / get_provider().
DEFAULT_MODEL = ""
VISION_MODEL = ""

# Default API key environment variable (used by default model)
DEFAULT_API_KEY_ENV = "FIREWORKS_API_KEY"


# ═══════════════════════════════════════════════════════════════════════════════
# Factory functions
# ═══════════════════════════════════════════════════════════════════════════════

# Provider cache — OpenAI clients are thread-safe and expensive to create
# (httpx connection pool setup, TLS config). Reuse across sessions.
_provider_cache: dict[str, LLMProvider] = {}


def get_provider(model: Union[str, ModelEntry, None] = None) -> LLMProvider:
    """
    Get an LLM provider for the specified model.

    Uses OpenAI SDK with provider-specific base URLs.
    Providers are cached by model name to avoid recreating httpx clients.

    Args:
        model: ModelEntry, model name/alias, or None for default model.
            Examples:
                - "minimax", "kimi", "glm-4p7"
                - "fireworks:accounts/fireworks/models/minimax-m2p1"

    Returns:
        LLMProvider instance (may be shared across sessions)
    """
    if not model:
        model = _get_default_model_name()

    # Determine cache key
    cache_key = model.name if isinstance(model, ModelEntry) else model
    if cache_key in _provider_cache:
        return _provider_cache[cache_key]

    if isinstance(model, ModelEntry):
        provider = OpenAIProvider(model)
    else:
        # Try to look up in registry
        registry = ModelRegistry.get()
        entry = registry.get_model(model)
        if entry:
            provider = OpenAIProvider(entry)
        else:
            # Assume it's a raw model string
            provider = OpenAIProvider(model)

    _provider_cache[cache_key] = provider
    return provider


def get_default_model() -> ModelEntry:
    """Get the default model."""
    return ModelRegistry.get().get_default()


def get_default_api_key() -> str | None:
    """Get the default API key from environment."""
    return os.environ.get(DEFAULT_API_KEY_ENV)


def list_available_models() -> list[dict]:
    """List all available models."""
    return ModelRegistry.get().list_all()


def get_vision_provider() -> LLMProvider:
    """Get a vision-capable LLM provider.

    Uses EMDASH_VISION_MODEL env var or registry default.

    Returns:
        LLMProvider instance that supports vision
    """
    return get_provider(_get_vision_model_name())


def get_vision_model() -> str:
    """Get the configured vision model name.

    Returns:
        Vision model string from EMDASH_VISION_MODEL or registry default
    """
    return _get_vision_model_name()
