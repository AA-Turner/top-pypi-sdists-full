"""Provider-based variant registry for thinking/reasoning effort levels.

Maps (provider, effort_label) → provider-specific API params that get
passed through GenerateParams.extra → LiteLLM acompletion() kwargs.

Provider is inferred from the model string. The platform catalog's
"reasoning" capability gates which models actually support variants.
When catalog is unavailable, variants are offered optimistically —
LiteLLM's drop_params:true silently drops unsupported params.
"""

from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from rich.text import Text

from dreadnode.app.model_catalog import infer_provider

# ---------------------------------------------------------------------------
# Provider → effort → API params
# ---------------------------------------------------------------------------

_ANTHROPIC_VARIANTS: dict[str, dict[str, t.Any]] = {
    "low": {"reasoning_effort": "low"},
    "medium": {"reasoning_effort": "medium"},
    "high": {"reasoning_effort": "high"},
    "max": {"reasoning_effort": "max"},
}

_OPENAI_VARIANTS: dict[str, dict[str, t.Any]] = {
    "low": {"reasoning_effort": "low"},
    "medium": {"reasoning_effort": "medium"},
    "high": {"reasoning_effort": "high"},
}

_GOOGLE_VARIANTS: dict[str, dict[str, t.Any]] = {
    "high": {"thinking_config": {"include_thoughts": True, "thinking_budget": 16000}},
    "max": {"thinking_config": {"include_thoughts": True, "thinking_budget": 24576}},
}

_PROVIDER_VARIANTS: dict[str, dict[str, dict[str, t.Any]]] = {
    "anthropic": _ANTHROPIC_VARIANTS,
    "openai": _OPENAI_VARIANTS,
    "google": _GOOGLE_VARIANTS,
}

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def get_variants(
    model: str,
    *,
    reasoning: bool | None = None,
) -> dict[str, dict[str, t.Any]]:
    """Return available effort variants for a model.

    Args:
        model: Model identifier string (e.g. "anthropic/claude-opus-4-6")
        reasoning: Whether model supports reasoning (from platform catalog).
            True = yes, return provider variants.
            False = no, return empty dict.
            None = unknown (no catalog), optimistically return provider variants.
    """
    if reasoning is False:
        return {}

    provider = infer_provider(model)
    if provider is None:
        return {}

    return dict(_PROVIDER_VARIANTS.get(provider, {}))


# ---------------------------------------------------------------------------
# Sane defaults per provider
# ---------------------------------------------------------------------------

_PROVIDER_DEFAULT_EFFORT: dict[str, str] = {
    "anthropic": "medium",
    "openai": "medium",
    "google": "high",
}


def default_effort(model: str) -> str | None:
    """Return the default thinking effort level for a model, or None if unsupported."""
    provider = infer_provider(model)
    if provider is None:
        return None
    return _PROVIDER_DEFAULT_EFFORT.get(provider)


def cycle_variant(
    variants: dict[str, dict[str, t.Any]],
    current: str | None,
) -> str | None:
    """Advance to the next variant label, wrapping to None after last."""
    if not variants:
        return None
    keys = list(variants.keys())
    if current is None:
        return keys[0]
    try:
        idx = keys.index(current)
    except ValueError:
        return keys[0]
    next_idx = idx + 1
    if next_idx >= len(keys):
        return None
    return keys[next_idx]


# ---------------------------------------------------------------------------
# Token formatting & model context limits
# ---------------------------------------------------------------------------


_model_max_cache: dict[str, int | None] = {}


def get_model_max_input_tokens(model: str) -> int | None:
    """Look up the max input token limit for a model via litellm metadata.

    Returns None if the model is unknown. Results are cached per model string.
    """
    if model in _model_max_cache:
        return _model_max_cache[model]

    result: int | None = None
    try:
        import os

        # Env vars are the canonical way to suppress litellm noise —
        # same mechanism as _suppress_library_noise() in print_mode.py
        os.environ.setdefault("LITELLM_LOG", "ERROR")
        os.environ.setdefault("LITELLM_SUPPRESS_DEBUG_INFO", "1")

        import litellm

        # Strip dn/ proxy prefix for lookup
        lookup = model
        lookup = lookup.removeprefix("dn/")

        while lookup not in litellm.model_cost:
            if "/" not in lookup:
                break
            lookup = "/".join(lookup.split("/")[1:])

        if lookup in litellm.model_cost:
            info = litellm.model_cost[lookup]
            max_input = info.get("max_input_tokens") or info.get("max_tokens", 0)
            if max_input and max_input > 0:
                result = int(max_input)
    except Exception:  # noqa: S110
        pass

    _model_max_cache[model] = result
    return result


def _fmt_tokens(n: int) -> str:
    """Format a raw token count as a compact string (no suffix)."""
    if n < 1_000:
        return str(n)
    if n >= 999_500:
        m = n / 1_000_000
        formatted = f"{m:.1f}"
        formatted = formatted.removesuffix(".0")
        return f"{formatted}M"
    k = n / 1_000
    if k >= 100:
        return f"{k:.0f}k"
    # 1k-99.9k — one decimal, strip trailing .0
    formatted = f"{k:.1f}"
    formatted = formatted.removesuffix(".0")
    return f"{formatted}k"


def format_tokens(tokens: int, limit: int | None = None) -> str:
    """Format a token count for display, with optional context limit.

    Examples:
        format_tokens(834)              → "834 tok"
        format_tokens(1_200)            → "1.2k tok"
        format_tokens(53_422)           → "53.4k tok"
        format_tokens(200_000)          → "200k tok"
        format_tokens(53_422, 200_000)  → "53.4k/200k tok"
    """
    result = _fmt_tokens(tokens)
    if limit is not None and limit > 0:
        result += f"/{_fmt_tokens(limit)}"
    return f"{result} tok"


def render_tokens(tokens: int, limit: int | None = None) -> Text:
    """Build a styled Rich Text for token display.

    The current count brightens as usage approaches the limit,
    fading from muted → subtle → accent for a gentle visual cue:
      - <50%:  muted grey
      - 50-75%: lighter grey
      - >75%:  brand accent
    """
    from rich.text import Text

    from dreadnode.app.tui.theme import ACCENT, FG_FAINTEST, FG_MUTED, FG_SUBTLE

    count_style = FG_MUTED
    if limit is not None and limit > 0:
        ratio = tokens / limit
        if ratio >= 0.75:
            count_style = ACCENT
        elif ratio >= 0.5:
            count_style = FG_SUBTLE

    result = Text(no_wrap=True)
    result.append(_fmt_tokens(tokens), style=count_style)
    if limit is not None and limit > 0:
        result.append("/", style=FG_FAINTEST)
        result.append(_fmt_tokens(limit), style=FG_FAINTEST)
    result.append(" tok", style=FG_FAINTEST)
    return result
