"""Centralized model catalog for the Dreadnode SDK.

Maps model IDs to display names, resolves friendly names to canonical
litellm IDs, and infers providers from model strings.  No TUI / Rich
dependencies — safe to import from CLI, server, or library code.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Provider inference
# ---------------------------------------------------------------------------

_KNOWN_PROVIDERS = {"anthropic", "openai", "google", "groq", "openrouter"}

_BARE_MODEL_PROVIDERS: list[tuple[str, str]] = [
    ("claude-", "anthropic"),
    ("gemini-", "google"),
    ("gpt-", "openai"),
    ("o1-", "openai"),
    ("o3-", "openai"),
    ("o4-", "openai"),
]

_DN_PREFIX_PROVIDERS: list[tuple[str, str]] = [
    ("dn/claude-", "anthropic"),
    ("dn/gpt-", "openai"),
    ("dn/gemini-", "google"),
    ("dn/o1-", "openai"),
    ("dn/o3-", "openai"),
    ("dn/o4-", "openai"),
    ("dn/openrouter/", "openrouter"),
]


def infer_provider(model: str) -> str | None:
    """Infer the LLM provider from a model identifier string.

    Handles formats: ``"provider/model"``, ``"dn/model"``, ``"model"`` (bare).
    """
    lower = model.lower()

    # Explicit provider/ prefix
    if "/" in lower and not lower.startswith("dn/"):
        provider = lower.split("/", 1)[0]
        # Normalize gemini → google
        if provider == "gemini":
            provider = "google"
        # Only return known providers
        if provider in _KNOWN_PROVIDERS:
            return provider
        return None

    # dn/ prefix (platform proxy)
    for prefix, provider in _DN_PREFIX_PROVIDERS:
        if lower.startswith(prefix):
            return provider

    # Bare model name
    for prefix, provider in _BARE_MODEL_PROVIDERS:
        if lower.startswith(prefix):
            return provider

    return None


# ---------------------------------------------------------------------------
# Display names: model ID substring → human-friendly short name
# ---------------------------------------------------------------------------

# Order: more specific patterns first so longest match wins naturally.
_MODEL_DISPLAY_NAMES: dict[str, str] = {
    # Anthropic — versioned (e.g. claude-opus-4-6) and base (e.g. claude-sonnet-4-20250514)
    "claude-opus-4-6": "Opus 4.6",
    "claude-sonnet-4-6": "Sonnet 4.6",
    "claude-opus-4-5": "Opus 4.5",
    "claude-sonnet-4-5": "Sonnet 4.5",
    "claude-haiku-4-5": "Haiku 4.5",
    "claude-haiku-3-5": "Haiku 3.5",
    "claude-sonnet-3-5": "Sonnet 3.5",
    "claude-opus-4": "Opus 4",
    "claude-sonnet-4": "Sonnet 4",
    "claude-haiku-4": "Haiku 4",
    # OpenAI
    "gpt-5.4-mini": "GPT-5.4 Mini",
    "gpt-5.4": "GPT-5.4",
    "gpt-5.3-codex": "GPT-5.3-Codex",
    "gpt-5.2-codex": "GPT-5.2-Codex",
    "gpt-5.2": "GPT-5.2",
    "gpt-5-nano": "GPT-5 Nano",
    "gpt-4.1-mini": "GPT-4.1 Mini",
    "gpt-4.1-nano": "GPT-4.1 Nano",
    "gpt-4.1": "GPT-4.1",
    "gpt-4o-mini": "GPT-4o Mini",
    "gpt-4o": "GPT-4o",
    "o3-mini": "o3 Mini",
    "o4-mini": "o4 Mini",
    "o3": "o3",
    # Google
    "gemini-3.1-pro": "Gemini 3.1 Pro",
    "gemini-3.1-flash-lite": "Gemini 3.1 Flash Lite",
    "gemini-2.5-pro": "Gemini 2.5 Pro",
    "gemini-2.5-flash": "Gemini 2.5 Flash",
    "gemini-2.0-flash": "Gemini 2.0 Flash",
    # OpenRouter
    "kimi-k2.6": "Kimi K2.6",
    "qwen3.6-plus": "Qwen3.6 Plus",
}

# Ordered list of common model IDs for friendly-name resolution.
KNOWN_MODELS: list[str] = [
    "anthropic/claude-opus-4-6",
    "anthropic/claude-sonnet-4-6",
    "openai/gpt-5.4",
    "openai/gpt-5.4-mini",
    "openai/gpt-5.3-codex",
    "openai/o3",
    "openai/o4-mini",
    "gemini/gemini-3.1-pro-preview",
    "gemini/gemini-3.1-flash-lite-preview",
    "openrouter/moonshotai/kimi-k2.6",
    "openrouter/qwen/qwen3.6-plus",
]


def strip_provider(model: str) -> str:
    """Strip provider prefix (e.g. ``'anthropic/'``, ``'dn/'``) from a model string."""
    if "/" in model:
        return model.split("/", 1)[1]
    return model


def display_name(model: str) -> str:
    """Return a short human-friendly display name for a model.

    Strips the provider prefix, then looks up the longest matching
    substring in ``_MODEL_DISPLAY_NAMES``.  Falls back to the
    stripped model ID when no match is found.
    """
    bare = strip_provider(model).lower()

    # Normalize both sides: dots ↔ dashes so "claude-opus-4.5" matches "claude-opus-4-5"
    bare_norm = bare.replace(".", "-")
    best_key: str | None = None
    best_len = 0
    for key in _MODEL_DISPLAY_NAMES:
        key_norm = key.replace(".", "-")
        if key_norm in bare_norm and len(key_norm) > best_len:
            best_key = key
            best_len = len(key_norm)

    if best_key is not None:
        return _MODEL_DISPLAY_NAMES[best_key]

    return strip_provider(model)


def display_name_with_effort(model: str, effort: str | None) -> str:
    """Return display name optionally suffixed with the effort level.

    Example: ``"Opus 4.6 (High)"`` when *effort* is ``"high"``.
    Returns plain ``display_name(model)`` when *effort* is None or empty.
    """
    name = display_name(model)
    if effort:
        return f"{name} ({effort.capitalize()})"
    return name


# ---------------------------------------------------------------------------
# Friendly name resolution: "Sonnet 4.6" → "anthropic/claude-sonnet-4-6"
# ---------------------------------------------------------------------------


def _build_friendly_map() -> dict[str, str]:
    result: dict[str, str] = {}
    for model_id in KNOWN_MODELS:
        bare = model_id.split("/", 1)[-1] if "/" in model_id else model_id
        result[bare.lower()] = model_id
    # KNOWN_MODELS is ordered newest-first, so the first match for a display
    # name substring maps to the latest version of that model family.
    for substr, friendly in _MODEL_DISPLAY_NAMES.items():
        for model_id in KNOWN_MODELS:
            if substr in model_id:
                result[friendly.lower()] = model_id
                break
    return result


_FRIENDLY_TO_ID: dict[str, str] = _build_friendly_map()


def resolve_model(raw: str) -> str:
    """Resolve a friendly model name to its canonical litellm ID.

    Accepts display names (``"Sonnet 4.6"``, ``"opus 4.6"``), bare model
    names (``"claude-opus-4-6"``), or full IDs (``"anthropic/claude-opus-4-6"``).
    Full IDs pass through unchanged; unknown names pass through as-is.
    """
    if "/" in raw:
        return raw
    key = raw.strip().lower()
    if key in _FRIENDLY_TO_ID:
        return _FRIENDLY_TO_ID[key]
    return raw
