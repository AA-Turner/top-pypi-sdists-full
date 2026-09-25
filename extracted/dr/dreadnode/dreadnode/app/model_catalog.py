"""Centralized model catalog for the Dreadnode SDK.

Maps model IDs to display names, resolves friendly names to canonical
litellm IDs, and infers providers from model strings.  No TUI / Rich
dependencies — safe to import from CLI, server, or library code.
"""

import asyncio
import hashlib
import os
import typing as t
from time import monotonic

from loguru import logger

# ---------------------------------------------------------------------------
# Provider inference
# ---------------------------------------------------------------------------

# Reasoning-capable provider families beyond the original three. Following the
# consensus across other harnesses (goose, pi, opencode, hermes, aider — ENG-7388
# research): a model gets a reasoning/effort toggle if it's reasoning-CAPABLE,
# regardless of whether it surfaces readable chain-of-thought. Whether text
# actually shows is emergent — the SDK captures reasoning_content/thinking_blocks
# when present (litellm_.py) and nothing renders when the provider hides its CoT
# (openai, xai/grok, deepseek). This mirrors gpt-5.x, which already gets a toggle
# despite hiding its CoT. Genuinely non-reasoning families (llama, mistral) stay
# unmapped so no misleading toggle appears.
_KNOWN_PROVIDERS = {
    "anthropic",
    "openai",
    "google",
    "groq",
    "openrouter",
    "zhipuai",  # glm — surfaces readable reasoning_content
    "moonshot",  # kimi — surfaces readable reasoning_content
    "qwen",  # surfaces readable reasoning_content
    "nvidia",  # nemotron — surfaces readable reasoning_content
    "deepseek",  # reasoning-capable; CoT hidden through the proxy
    "xai",  # grok — reasoning-capable; CoT hidden through the proxy
}

_BARE_MODEL_PROVIDERS: list[tuple[str, str]] = [
    ("claude-", "anthropic"),
    ("gemini-", "google"),
    ("gpt-", "openai"),
    ("o1-", "openai"),
    ("o3-", "openai"),
    ("o4-", "openai"),
    ("glm-", "zhipuai"),
    ("kimi-", "moonshot"),
    ("qwen", "qwen"),
    ("nemotron-", "nvidia"),
    ("deepseek-", "deepseek"),
    ("grok-", "xai"),
]

_DN_PREFIX_PROVIDERS: list[tuple[str, str]] = [
    ("dn/claude-", "anthropic"),
    ("dn/gpt-", "openai"),
    ("dn/gemini-", "google"),
    ("dn/o1-", "openai"),
    ("dn/o3-", "openai"),
    ("dn/o4-", "openai"),
    ("dn/openrouter/", "openrouter"),
    ("dn/glm-", "zhipuai"),
    ("dn/kimi-", "moonshot"),
    ("dn/qwen", "qwen"),
    ("dn/nemotron-", "nvidia"),
    ("dn/deepseek-", "deepseek"),
    ("dn/grok-", "xai"),
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


# ---------------------------------------------------------------------------
# Model info resolution
# ---------------------------------------------------------------------------

# Successful tables are shared across callers; credentials are fingerprinted so
# rotation bypasses both old metadata and failed-request cooldowns.
_GatewayKey = tuple[str, str]
_gateway_info: dict[_GatewayKey, dict[str, dict[str, t.Any]]] = {}
_gateway_retry_at: dict[_GatewayKey, float] = {}
_gateway_loads: dict[tuple[asyncio.AbstractEventLoop, _GatewayKey], asyncio.Task[None]] = {}
_GATEWAY_RETRY_SECONDS = 30.0


def _gateway_config(api_base: str | None, api_key: str | None) -> tuple[str, str | None]:
    from dreadnode.generators.proxy import DREADNODE_LLM_API_KEY_ENV, DREADNODE_LLM_BASE_ENV

    base = api_base or os.environ.get(DREADNODE_LLM_BASE_ENV, "").strip()
    key = api_key or os.environ.get(DREADNODE_LLM_API_KEY_ENV, "").strip() or None
    return base.rstrip("/"), key


def _gateway_cache_key(api_base: str, api_key: str | None) -> _GatewayKey:
    return api_base.rstrip("/"), hashlib.sha256((api_key or "").encode()).hexdigest()


async def _fetch_gateway_info(api_base: str, api_key: str | None) -> None:
    import httpx

    from dreadnode.core.tls import create_platform_ssl_context

    key = _gateway_cache_key(api_base, api_key)
    started = monotonic()
    try:
        ssl_context = await asyncio.to_thread(create_platform_ssl_context)
        async with httpx.AsyncClient(verify=ssl_context, timeout=10) as client:
            response = await client.get(
                api_base + "/model/info",
                headers={"Authorization": f"Bearer {api_key}"} if api_key else {},
            )
            response.raise_for_status()
            table: dict[str, dict[str, t.Any]] = {}
            for entry in response.json()["data"]:
                name = entry.get("model_name")
                info = entry.get("model_info")
                if isinstance(name, str) and isinstance(info, dict):
                    table[name] = info
    except Exception:
        _gateway_retry_at[key] = monotonic() + _GATEWAY_RETRY_SECONDS
        logger.debug(
            "Gateway model info unavailable at '{}' after {:.2f}s",
            api_base,
            monotonic() - started,
        )
    else:
        _gateway_info[key] = table
        _gateway_retry_at.pop(key, None)
        logger.debug(
            "Gateway model info loaded from '{}' in {:.2f}s ({} models)",
            api_base,
            monotonic() - started,
            len(table),
        )


async def load_gateway_model_info(
    *, api_base: str | None = None, api_key: str | None = None
) -> None:
    """Populate metadata without blocking the event loop; retry failures after 30s.

    Concurrent callers on an event loop share a request. Cancelling a caller
    leaves the shared request running for the remaining consumers.
    """
    api_base, api_key = _gateway_config(api_base, api_key)
    if not api_base:
        return
    key = _gateway_cache_key(api_base, api_key)
    if key in _gateway_info or monotonic() < _gateway_retry_at.get(key, 0):
        return
    pending_key = (asyncio.get_running_loop(), key)
    task = _gateway_loads.get(pending_key)
    if task is None:
        task = asyncio.create_task(_fetch_gateway_info(api_base, api_key))
        _gateway_loads[pending_key] = task
        task.add_done_callback(lambda _: _gateway_loads.pop(pending_key, None))
    await asyncio.shield(task)


def resolve_model_info(
    model: str,
    *,
    api_base: str | None = None,
    api_key: str | None = None,
) -> dict[str, t.Any]:
    """Everything we know about a model id *we* use, as a litellm model-info dict.

    Our chat models are Dreadnode aliases (``dn/claude-sonnet-5``) that only the
    gateway can resolve — it owns the mapping to the real deployment, and that
    mapping is not guessable: ``dn/glm-5.2`` routes to ``openrouter/z-ai/glm-5.1``
    and ``dn/grok-4-20-reasoning`` to ``xai/grok-4.3``. litellm's client-side
    table is keyed by public model names and cannot know any of them.

    Callers used to strip segments off the alias until something matched. For a
    provider prefix that is mostly harmless — ``anthropic/claude-sonnet-4-5``
    is not in litellm's table but ``claude-sonnet-4-5`` is, and it is the same
    model — so that fallback stays. For ``dn/`` it is not: the alias is opaque,
    and stripping it lands on whatever public model happens to share the name.
    ``dn/deepseek-v4-flash`` resolved to public ``deepseek-v4-flash``, priced
    132% high; ``dn/deepseek-v4-pro`` 24% low (ENG-8431). So a ``dn/`` model is
    the gateway's to answer or nobody's.

    ``api_base``/``api_key`` default to the platform proxy the process is
    already configured for, so a caller holding nothing but a model string
    can read cached gateway metadata. This function never fetches metadata;
    async consumers should await ``load_gateway_model_info`` first.

    Returns ``{}`` when nothing knows the model. Callers must treat that as
    "unknown" rather than as a value — an honest gap is recoverable, a
    confidently wrong number is not.
    """
    api_base, api_key = _gateway_config(api_base, api_key)
    if api_base:
        info = _gateway_info.get(_gateway_cache_key(api_base, api_key), {}).get(model)
        if info:
            return info

    try:
        import litellm
    except Exception:
        return {}

    info = litellm.model_cost.get(model)
    if info:
        return dict(info)

    # A `dn/` alias that the gateway could not answer is unknown, full stop.
    if model.startswith("dn/"):
        return {}

    # Provider prefixes: litellm's table is patchy about carrying them, so fall
    # back to the bare name the way every caller used to do for itself.
    lookup = model
    while "/" in lookup:
        lookup = lookup.split("/", 1)[1]
        info = litellm.model_cost.get(lookup)
        if info:
            return dict(info)

    return {}
