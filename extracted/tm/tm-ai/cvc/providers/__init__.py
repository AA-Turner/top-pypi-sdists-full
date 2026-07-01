"""CVC providers package — declarative provider profiles + helpers."""
from cvc.providers.base import (
    ProviderProfile,
    register_provider,
    get_provider,
    list_providers,
    all_profiles,
    AUTH_BEARER, AUTH_X_API_KEY, AUTH_OAUTH, AUTH_NONE,
    API_MODE_CHAT_COMPLETIONS, API_MODE_CODEX_RESPONSES,
    API_MODE_ANTHROPIC, API_MODE_GEMINI, API_MODE_OLLAMA,
)
from cvc.providers.normalize import normalize_model_for_provider, strip_provider_prefix

__all__ = [
    "ProviderProfile", "register_provider", "get_provider",
    "list_providers", "all_profiles",
    "AUTH_BEARER", "AUTH_X_API_KEY", "AUTH_OAUTH", "AUTH_NONE",
    "API_MODE_CHAT_COMPLETIONS", "API_MODE_CODEX_RESPONSES",
    "API_MODE_ANTHROPIC", "API_MODE_GEMINI", "API_MODE_OLLAMA",
    "normalize_model_for_provider", "strip_provider_prefix",
]
