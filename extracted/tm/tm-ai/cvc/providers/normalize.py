"""Model normalization layer (upstream parity).

`normalize_model_for_provider(model, provider)` handles vendor prefixes,
hyphens vs dots, DeepSeek aliases, Copilot vs Anthropic naming, etc.

Examples:
    >>> normalize_model_for_provider("claude-sonnet-4.6", "anthropic")
    'claude-sonnet-4-6'
    >>> normalize_model_for_provider("claude-sonnet-4.6", "github")
    'claude-sonnet-4.6'
    >>> normalize_model_for_provider("deepseek-r1", "nvidia")
    'deepseek-ai/deepseek-r1'
    >>> normalize_model_for_provider("nemotron", "nvidia")
    'nvidia/nemotron-3-super-120b-instruct'
"""
from __future__ import annotations

import re
from typing import Optional

# ── Static alias maps per provider ────────────────────────────────────

# Anthropic native API uses HYPHENATED versions (claude-sonnet-4-6).
# Copilot/GitHub uses DOTTED versions (claude-sonnet-4.6).
_ANTHROPIC_ALIASES: dict[str, str] = {
    "claude-opus-4.6": "claude-opus-4-6",
    "claude-sonnet-4.6": "claude-sonnet-4-6",
    "claude-sonnet-4.5": "claude-sonnet-4-5",
    "claude-opus-4.5": "claude-opus-4-5",
    "claude-haiku-4.5": "claude-haiku-4-5",
    "opus": "claude-opus-4-6",
    "sonnet": "claude-sonnet-4-6",
    "haiku": "claude-haiku-4-5",
}

_COPILOT_ALIASES: dict[str, str] = {
    "claude-sonnet-4-6": "claude-sonnet-4.6",
    "claude-sonnet-4-5": "claude-sonnet-4.5",
    "claude-opus-4-6": "claude-opus-4.6",
    "claude-opus-4-5": "claude-opus-4.5",
    "claude-haiku-4-5": "claude-haiku-4.5",
    "sonnet": "claude-sonnet-4.6",
    "opus": "claude-opus-4.6",
    "haiku": "claude-haiku-4.5",
    "gpt-5": "gpt-5",
    "gpt-4o": "gpt-4o",
}

# NVIDIA NIM uses VENDOR/MODEL form (nvidia/nemotron-3-super-120b-instruct).
_NVIDIA_ALIASES: dict[str, str] = {
    "nemotron": "nvidia/nemotron-3-super-120b-instruct",
    "nemotron-3-super": "nvidia/nemotron-3-super-120b-instruct",
    "nemotron-super": "nvidia/nemotron-3-super-120b-instruct",
    "kimi-k2": "moonshotai/kimi-k2-instruct",
    "kimi": "moonshotai/kimi-k2-instruct",
    "minimax-m2": "minimaxai/minimax-m2",
    "minimax": "minimaxai/minimax-m2",
    "glm-5": "zai-org/glm-4.6",
    "glm": "zai-org/glm-4.6",
    "deepseek-r1": "deepseek-ai/deepseek-r1",
    "deepseek": "deepseek-ai/deepseek-r1",
}

_GOOGLE_ALIASES: dict[str, str] = {
    "gemini-3-pro": "gemini-3-pro-preview",
    "gemini-3-flash": "gemini-3-flash-preview",
    "gemini-3.1-pro": "gemini-3.1-pro-preview",
    "gemini-3": "gemini-3-flash-preview",
    "gemini-pro": "gemini-3-pro-preview",
    "gemini-flash": "gemini-3-flash-preview",
}

_PROVIDER_ALIASES: dict[str, dict[str, str]] = {
    "anthropic": _ANTHROPIC_ALIASES,
    "github": _COPILOT_ALIASES,
    "copilot": _COPILOT_ALIASES,
    "nvidia": _NVIDIA_ALIASES,
    "google": _GOOGLE_ALIASES,
    "vertex": _GOOGLE_ALIASES,
}


# ── Strip "{provider}/" prefix in fallback chain model spec ──────────

def strip_provider_prefix(model: str) -> tuple[Optional[str], str]:
    """Split 'copilot/claude-sonnet-4.6' → ('copilot', 'claude-sonnet-4.6')."""
    if "/" in model:
        head, tail = model.split("/", 1)
        # Only treat as provider prefix if head matches a known provider
        if head.lower() in {"copilot", "github", "anthropic", "openai", "google",
                             "nvidia", "minimax", "vertex", "ollama", "lmstudio",
                             "openrouter"}:
            return head.lower(), tail
    return None, model


# ── Main entry ────────────────────────────────────────────────────────

def normalize_model_for_provider(model: str, provider: str) -> str:
    """Normalize a model name for the target provider's expected format.

    Steps:
        1. Strip leading {known_provider}/ prefix (e.g. copilot/claude-sonnet-4.6 → claude-sonnet-4.6).
        2. Apply provider-specific alias map (lowercased lookup).
        3. For Anthropic: convert dotted versions → hyphenated.
        4. For NVIDIA: ensure vendor/ prefix is present (default vendor = nvidia/ for raw names).
        5. Return as-is if no rule matches.
    """
    if not model or not provider:
        return model

    provider = provider.lower()
    _, bare = strip_provider_prefix(model)
    candidate = bare.strip()

    # 1) Direct alias hit
    aliases = _PROVIDER_ALIASES.get(provider, {})
    lower = candidate.lower()
    if lower in aliases:
        return aliases[lower]

    # 2) Provider-specific transforms
    if provider == "anthropic":
        # claude-sonnet-4.6 → claude-sonnet-4-6  (anthropic native API)
        if candidate.startswith("claude-") and re.search(r"\d+\.\d+$", candidate):
            return re.sub(r"(\d+)\.(\d+)$", r"\1-\2", candidate)

    elif provider in ("github", "copilot"):
        # claude-sonnet-4-6 → claude-sonnet-4.6 (Copilot expects dotted)
        if candidate.startswith("claude-") and re.search(r"-\d+-\d+$", candidate):
            return re.sub(r"-(\d+)-(\d+)$", r"-\1.\2", candidate)

    elif provider == "nvidia":
        # If no vendor/ prefix and not already normalized, default to nvidia/
        if "/" not in candidate:
            return f"nvidia/{candidate}"

    elif provider in ("google", "vertex"):
        # gemini-3.1-pro → gemini-3.1-pro-preview if no -preview/-stable suffix
        if candidate.startswith("gemini-3") and not candidate.endswith(("-preview", "-stable")):
            return f"{candidate}-preview"

    return candidate


__all__ = [
    "normalize_model_for_provider",
    "strip_provider_prefix",
]
