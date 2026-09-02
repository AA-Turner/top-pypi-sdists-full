"""ONE provider-independent pass: UnifiedConfig-shaped object -> canonical settings.

Extracts only the keys the caller actually set. Provider vocabulary/renames are
NOT applied here — that is ``CompiledControlsMap.outbound``'s job. This module
is the SOLE owner of the ``disable_reasoning`` / ``thinking_budget``
normalization (inherited byte-identical from the retired
ThinkingConfig.from_settings / to_openai_reasoning; the chat param golden in
packages/matrx-ai/tests/fixtures/chat_param_golden freezes the behaviour).
"""

from __future__ import annotations

from typing import Any


def _effort_from_budget(tokens: int) -> str:
    # The unified budget->effort tiers (OpenAI thresholds; frozen by the golden).
    if tokens < 1:
        return "none"
    if tokens < 2000:
        return "low"
    if tokens < 10000:
        return "medium"
    if tokens < 20000:
        return "high"
    return "xhigh"


def canonical_settings_from_config(config: Any) -> dict[str, Any]:
    out: dict[str, Any] = {}

    reasoning_effort = getattr(config, "reasoning_effort", None)
    disable_reasoning = getattr(config, "disable_reasoning", None)
    thinking_budget = getattr(config, "thinking_budget", None)

    # HOUSE SEMANTICS (platform law, ai_041):
    #   "auto" == UNSET. The caller declined to set the key; the provider payload
    #   omits it and whatever default applies (a DB rule ``default``, a processor's
    #   unset path, or the provider's own default) applies — identical to never
    #   sending the key. Normalized HERE, the one canonical pass, so every scalar
    #   rule, default, and processor sees auto and unset as the same thing.
    #   (processors._explicit_effort is the second, independent layer.)
    #   "none" == an explicit "send nothing": never collapsed into a concrete
    #   reasoning level; providers with a native OFF switch use it (documented
    #   per-family in the processors / DB rules).
    if reasoning_effort == "auto":
        reasoning_effort = None

    # The canonical disable_reasoning normalization:
    #   disable_reasoning=True            -> "none" (overrides everything)
    #   explicit reasoning_effort         -> as given ("auto" normalized to unset above)
    #   disable_reasoning=False, no effort -> "medium" ("reasoning ON, pick sensible level")
    #   thinking_budget, no effort        -> budget-derived tier
    if disable_reasoning is True:
        out["reasoning_effort"] = "none"
    elif reasoning_effort is not None:
        out["reasoning_effort"] = reasoning_effort
    elif disable_reasoning is False:
        out["reasoning_effort"] = "medium"
    elif thinking_budget is not None:
        out["reasoning_effort"] = _effort_from_budget(int(thinking_budget))
        # Metadata, never sent (outbound skips "_" keys): the effort tier above
        # uses the OpenAI thresholds. Processors that mirror a provider's OWN
        # budget arithmetic (anthropic/google) must treat it as unset and read
        # the raw thinking_budget ride-along instead.
        out["_reasoning_effort_derived"] = True

    reasoning_summary = getattr(config, "reasoning_summary", None)
    if reasoning_summary is not None:
        out["reasoning_summary"] = reasoning_summary

    # verbosity (gpt-5.x text.verbosity) rides only where an api/offering rule
    # declares it — the declared-keys gate drops it loudly everywhere else.
    for key in ("temperature", "top_p", "top_k", "max_output_tokens", "seed", "verbosity"):
        value = getattr(config, key, None)
        if value is not None:
            out[key] = value

    stop_sequences = getattr(config, "stop_sequences", None)
    if stop_sequences:
        out["stop_sequences"] = list(stop_sequences)

    response_format = getattr(config, "response_format", None)
    if response_format is not None:
        out["response_format"] = response_format

    for key in ("language", "timestamp_granularities"):
        value = getattr(config, key, None)
        if value is not None:
            out[key] = value

    # Raw budget rides along for services whose controls consume it directly
    # (e.g. Anthropic budget_tokens); the effort tier above is the portable form.
    if thinking_budget is not None:
        out["thinking_budget"] = int(thinking_budget)

    # Legacy thinking-cluster ride-alongs the processors consume (adaptive
    # thinking_level fallback, google include_thoughts, cerebras clear_thinking).
    # include_thoughts=False is meaningful — carry explicit booleans, not truthy.
    thinking_level = getattr(config, "thinking_level", None)
    if thinking_level is not None:
        out["thinking_level"] = thinking_level
    include_thoughts = getattr(config, "include_thoughts", None)
    if include_thoughts is not None:
        out["include_thoughts"] = include_thoughts
    clear_thinking = getattr(config, "clear_thinking", None)
    if clear_thinking is not None:
        out["clear_thinking"] = clear_thinking

    _add_media_settings(config, out)

    return out


# ── media-generation cluster (B2-media) ─────────────────────────────────────
# UnifiedConfig canonical field -> ai.setting key. Values pass through as-is;
# the per-family DB rules (ai.api.rules / ai.offering.override) own the
# provider vocabulary. Two normalizations happen HERE because they define the
# canonical vocabulary itself (the ai.setting enums are lowercase):
#   * resolution is lowercased ("1K" -> "1k", "720P" -> "720p")
#   * output_format is lowercased (every legacy media translator lowercased it)
# ``render_quality`` lands under the canonical key "quality" (the ai.setting
# dictionary key); "count" is always present on UnifiedConfig (default 1) but
# only emitted when it differs from the default OR is explicitly meaningful —
# media rules always re-derive the provider count via the media_count
# processor, which treats an unset count exactly like count=1.

_MEDIA_PASSTHROUGH_KEYS = (
    "aspect_ratio",
    "width",
    "height",
    "duration_seconds",
    "fps",
    "steps",
    "guidance_scale",
    "encode_quality",
    "negative_prompt",
    "background",
    "output_compression",
    "moderation",
    "input_fidelity",
    "partial_images",
    "style",
    "disable_safety_checker",
    "generate_audio",
    "enhance_prompt",
)


def _add_media_settings(config: Any, out: dict[str, Any]) -> None:
    for key in _MEDIA_PASSTHROUGH_KEYS:
        value = getattr(config, key, None)
        if value is not None:
            out[key] = value

    # count defaults to 1 on UnifiedConfig and every legacy media translator
    # collapses count<=1 (and unset) to exactly 1 — so only a count that ASKS
    # for more than one asset is canonical signal. Emitting the default would
    # leak "count" into every non-media family the moment those flip.
    count = getattr(config, "count", None)
    if count is not None and int(count) > 1:
        out["count"] = int(count)

    render_quality = getattr(config, "render_quality", None)
    if render_quality is not None:
        out["quality"] = render_quality

    resolution = getattr(config, "resolution", None)
    if isinstance(resolution, str) and resolution:
        out["resolution"] = resolution.lower()

    output_format = getattr(config, "output_format", None)
    if isinstance(output_format, str) and output_format:
        out["output_format"] = output_format.lower()


__all__ = ["canonical_settings_from_config"]
