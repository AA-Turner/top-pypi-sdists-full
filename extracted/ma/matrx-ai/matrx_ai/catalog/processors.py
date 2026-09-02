"""Registered param processors — the ControlRule ``processor`` escape hatch.

A processor is a PURE function over (canonical config, assembled provider
params, context) — no DB access, no api_class reads. It runs in outbound's
SECOND pass, after every scalar rule (const/value_map/clamp/rename/default),
so it can see and mutate the fully assembled provider params. Run order across
processors: ``processor_config["order"]`` (default 100), tie-broken by key.

The built-ins below are the exact (now sole) owners of the irreducible
thinking arithmetic ported from the retired ThinkingConfig; the chat param
golden (tests/fixtures/chat_param_golden) freezes their behaviour.

Canonical-config note: ``canonicalize.canonical_settings_from_config`` emits
``_reasoning_effort_derived=True`` when reasoning_effort was derived from a raw
thinking_budget (no explicit effort). Processors that mirror ThinkingConfig's
per-provider budget arithmetic must treat a derived effort as UNSET (via
``_explicit_effort``) so the raw budget takes its legacy path — the derived
tier uses OpenAI's thresholds, not this provider's.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from matrx_utils import vcprint

from matrx_ai.catalog.models import Adjustment

# The house enum values (ai_041): "auto" = leave the key unset (the provider
# default applies), "none" = send nothing. They are POSTURES, not degrees —
# see ProcessorContext.reconcile_supported for why that distinction is
# load-bearing.
_HOUSE_VALUES = frozenset({"auto", "none"})


@dataclass
class ProcessorContext:
    key: str  # the canonical key the rule is attached to
    config: dict[str, Any]  # rule.processor_config (data for THIS rule)
    adjustments: list[Adjustment]  # append to voice every change, as scalar rules do
    extra: dict[str, Any] = field(default_factory=dict)  # caller-supplied rule context
    # THE OFFERING'S DECLARED VOCABULARY for `key` (rule.ui_values) and the
    # ai.setting canonical order. A processor's own maps are per-FAMILY
    # ("flash", "pro"); these two are per-MODEL, which is the only resolution
    # at which "does this model accept that value" is answerable.
    supported_values: frozenset[str] = frozenset()
    value_order: tuple[str, ...] = ()

    def reconcile_supported(self, value: str | None) -> str | None:
        """Force a processor's RESOLVED provider value into the offering's
        declared vocabulary. Returns the value to send (or None to send none).

        🚨 Why this exists (2026-08-17, FastFire graded nothing for a whole
        session). A processor's effort→level maps are keyed by model FAMILY,
        and a family is not a model: ``_GOOGLE_3_EFFORT_TO_LEVEL_FLASH`` maps
        ``minimal -> "minimal"``, which is true of gemini-3.5-flash and FALSE
        of gemini-3.7-flash. The offering for 3.7-flash declares
        ``ui_values=[auto,none,low,medium,high]`` — no ``minimal`` — and 38
        live agents stored ``reasoning_effort="minimal"``. Nothing compared the
        map's output to that declaration, so every call shipped
        ``thinking_level: MINIMAL`` and Google 400'd all of them: *"Thinking
        level MINIMAL is not supported for this model."*

        Posture (root CLAUDE.md — "a guard that CAN reconcile MUST reconcile"):
        there is exactly one thing an unsupported intensity can mean — the
        nearest one this model actually has — so this reconciles and SCREAMS.
        It never raises and never kills a request.

        It reconciles only among the INTENSITIES: "auto"/"none" are postures,
        never a substitute for a degree the caller asked for (snapping
        "minimal" onto "none" would silently turn "think a little" into "do not
        think" on a model whose floor is merely higher — measured on
        MiniMax-M3, which supports only high/xhigh). A value with no
        reconcilable neighbour is dropped so the provider default applies —
        the one thing never allowed is forwarding it."""
        if value is None or not self.supported_values:
            return value
        if value in self.supported_values or value in _HOUSE_VALUES:
            return value
        nearest = _nearest_in_order(
            value, self.value_order, self.supported_values - _HOUSE_VALUES
        )
        self.adjustments.append(
            Adjustment(
                key=self.key,
                action="unsupported_value",
                canonical_value=value,
                sent_value=nearest,
                expected=nearest is not None,
                reason=(
                    f"'{self.key}' resolved to {value!r}, which this offering does not "
                    f"support (supported: {sorted(self.supported_values)}) — "
                    + (
                        f"reconciled to {nearest!r}"
                        if nearest
                        else "dropped; the provider default applies"
                    )
                ),
            )
        )
        vcprint(
            f"The '{self.key}' rule resolved to {value!r}, which is outside this "
            f"offering's declared vocabulary {sorted(self.supported_values)}. "
            + (f"Reconciled to {nearest!r}. " if nearest else "Dropped. ")
            + "The provider was never sent the unsupported value. Fix the SOURCE: "
            "either the offering's ui_values (if the model really does accept it) "
            "or the processor map for this family.",
            title="⚠️ AI CATALOG UNSUPPORTED VALUE",
            color="yellow",
        )
        return nearest


def _nearest_in_order(
    value: str, order: tuple[str, ...], candidates: frozenset[str]
) -> str | None:
    # ONE equivalence law for the whole catalog — see catalog/equivalence.py.
    from matrx_ai.catalog.equivalence import nearest_equivalent

    return nearest_equivalent("reasoning_effort", value, candidates, order)


ProcessorFn = Callable[[dict[str, Any], dict[str, Any], ProcessorContext], dict[str, Any]]

_PROCESSORS: dict[str, ProcessorFn] = {}


class UnknownProcessorError(KeyError):
    pass


def register_processor(name: str) -> Callable[[ProcessorFn], ProcessorFn]:
    def decorator(fn: ProcessorFn) -> ProcessorFn:
        existing = _PROCESSORS.get(name)
        if existing is not None and existing is not fn:
            raise ValueError(
                f"processor '{name}' is already registered ({existing.__module__}."
                f"{existing.__qualname__}) — processor names are a global vocabulary"
            )
        _PROCESSORS[name] = fn
        return fn

    return decorator


def has_processor(name: str) -> bool:
    return name in _PROCESSORS


def get_processor(name: str) -> ProcessorFn:
    fn = _PROCESSORS.get(name)
    if fn is None:
        vcprint(
            f"ControlRule names processor '{name}' but no such processor is registered.\n"
            f"  Registered: {sorted(_PROCESSORS)}\n"
            f"  Fix the ai.api.rules / ai.offering.override row (or register the "
            f"processor via matrx_ai.catalog.processors.register_processor). "
            f"Rows naming unknown processors QUARANTINE at catalog load — reaching "
            f"this error means a compiled map was built outside the manager.",
            title="🚨 AI CATALOG UNKNOWN PROCESSOR",
            color="red",
        )
        raise UnknownProcessorError(
            f"unknown control-rule processor '{name}' (registered: {sorted(_PROCESSORS)})"
        )
    return fn


def _explicit_effort(canonical: dict[str, Any]) -> str | None:
    # A budget-derived effort must NOT drive provider-specific effort maps —
    # ThinkingConfig resolves the raw budget through per-provider thresholds.
    if canonical.get("_reasoning_effort_derived"):
        return None
    effort = canonical.get("reasoning_effort")
    # HOUSE SEMANTICS (ai_041): "auto" == UNSET, everywhere. canonicalize.py
    # already normalizes it away; this is the second, independent layer for
    # canonical dicts assembled outside that pass. A processor must never map
    # "auto" to a concrete provider value.
    if effort == "auto":
        return None
    return effort


# ── anthropic_thinking ───────────────────────────────────────────────────────
# Exact port of ThinkingConfig.to_anthropic_thinking (mode "budget", default)
# and to_anthropic_adaptive_thinking (mode "adaptive"), PLUS the translator's
# max_tokens fallback (Anthropic requires max_tokens on every request).
#
# processor_config:
#   mode: "budget" (default) | "adaptive"
#   default_max_tokens: int (default 32768 — the translator's permissive floor)
#   effort_ceiling: str | None (adaptive only — ai_047; see _ADAPTIVE_EFFORT_ORDER)
#   consumes / order: engine keys (see controls.py)
#
# Reads canonical: reasoning_effort (+_reasoning_effort_derived), thinking_budget,
# thinking_level, include_thoughts, reasoning_summary, max_output_tokens.
# Writes params: thinking, output_config.effort (adaptive), max_tokens.

ANTHROPIC_MIN_BUDGET_TOKENS = 1024
ANTHROPIC_DEFAULT_MAX_TOKENS = 32768

# ThinkingConfig.to_anthropic_thinking effort_to_budget, verbatim.
_ANTHROPIC_EFFORT_TO_BUDGET: dict[str, int] = {
    "none": 0,
    "minimal": 1024,  # Anthropic's hard minimum (it rejects < 1024)
    "low": 1024,
    "medium": 4096,
    "high": 8192,
    "xhigh": 24576,
}

# ThinkingConfig.to_anthropic_adaptive_thinking effort_mapping — MINUS the
# legacy "auto" -> "high" entry, retired by the house auto/none standard
# (ai_041): "auto" == unset (no thinking key sent; the provider default
# applies), never a concrete effort. "none" (explicit off) is handled before
# this map is consulted. Deliberate divergence from the pre-migration golden.
# ai_045: "xhigh" and "max" pass through natively — Anthropic's adaptive
# output_config.effort accepts low/medium/high/xhigh/max on every adaptive
# model (Opus 4.7+, Sonnet 5, Fable 5). The old "xhigh" -> "high" cap was a
# port from before the provider grew the deeper tiers; product-level gating
# of the expensive tiers lives in the offering rule's ui_values (the base
# listings stop at "high"; the premium "-max" listings expose xhigh/max).
_ANTHROPIC_ADAPTIVE_EFFORT: dict[str, str | None] = {
    "none": None,
    "minimal": "low",
    "low": "low",
    "medium": "medium",
    "high": "high",
    "xhigh": "xhigh",
    "max": "max",
}

# ai_047: the second, ENGINE-side gate on the expensive adaptive tiers. The
# offering's ui_values is a UI cap only — a raw API caller can send
# reasoning_effort="xhigh"/"max" straight at a BASE listing and (since ai_045's
# native pass-through) reach the provider at full depth. processor_config
# "effort_ceiling" clamps any resolved effort ABOVE the ceiling down to it,
# with a loud Adjustment so the deviation is visible in response metadata.
# Values at/below the ceiling pass through; auto/none semantics are untouched
# (they exit before this runs). The premium "-max" offerings set NO ceiling.
_ADAPTIVE_EFFORT_ORDER: tuple[str, ...] = ("low", "medium", "high", "xhigh", "max")


def _apply_effort_ceiling(
    effort_level: str, ctx: ProcessorContext
) -> str:
    ceiling = ctx.config.get("effort_ceiling")
    if ceiling is None:
        return effort_level
    if ceiling not in _ADAPTIVE_EFFORT_ORDER:
        vcprint(
            f"anthropic_thinking processor_config.effort_ceiling={ceiling!r} is not a "
            f"valid adaptive effort tier {_ADAPTIVE_EFFORT_ORDER}.\n"
            f"  Fix the ai.offering override / ai.api.rules row for key '{ctx.key}'.",
            title="🚨 AI CATALOG INVALID EFFORT CEILING",
            color="red",
        )
        raise ValueError(
            f"anthropic_thinking: invalid processor_config effort_ceiling {ceiling!r} "
            f"(expected one of {_ADAPTIVE_EFFORT_ORDER})"
        )
    if effort_level not in _ADAPTIVE_EFFORT_ORDER:
        return effort_level
    if _ADAPTIVE_EFFORT_ORDER.index(effort_level) <= _ADAPTIVE_EFFORT_ORDER.index(ceiling):
        return effort_level
    ctx.adjustments.append(
        Adjustment(
            key="reasoning_effort",
            action="effort_ceiling",
            canonical_value=effort_level,
            sent_value=ceiling,
            reason=(
                f"this offering caps adaptive reasoning effort at '{ceiling}' "
                f"(requested '{effort_level}'); the deeper tiers are gated behind "
                f"the premium Max listing"
            ),
        )
    )
    return ceiling


def _current_max_tokens(canonical: dict[str, Any], params: dict[str, Any]) -> int | None:
    # Post-scalar params are the truth (rename/clamp already applied); fall back
    # to the canonical value when no scalar rule landed max_tokens.
    if "max_tokens" in params:
        return params["max_tokens"]
    return canonical.get("max_output_tokens")


@register_processor("anthropic_thinking")
def anthropic_thinking(
    canonical: dict[str, Any], params: dict[str, Any], ctx: ProcessorContext
) -> dict[str, Any]:
    mode = ctx.config.get("mode", "budget")
    if mode == "adaptive":
        return _anthropic_adaptive_thinking(canonical, params, ctx)
    if mode != "budget":
        raise ValueError(f"anthropic_thinking: unknown processor_config mode {mode!r}")
    return _anthropic_budget_thinking(canonical, params, ctx)


def _anthropic_budget_thinking(
    canonical: dict[str, Any], params: dict[str, Any], ctx: ProcessorContext
) -> dict[str, Any]:
    default_max = ctx.config.get("default_max_tokens", ANTHROPIC_DEFAULT_MAX_TOKENS)
    current_max = _current_max_tokens(canonical, params)

    # Budget resolution — thinking_budget WINS over effort (legacy contract).
    thinking_budget: int | None = None
    if canonical.get("thinking_budget") is not None:
        thinking_budget = int(canonical["thinking_budget"])
    else:
        effort = _explicit_effort(canonical)
        if effort:
            thinking_budget = _ANTHROPIC_EFFORT_TO_BUDGET.get(effort)

    if not thinking_budget:  # None or 0 — no thinking; translator max_tokens fallback
        params["max_tokens"] = current_max if current_max is not None else default_max
        return params

    if thinking_budget < ANTHROPIC_MIN_BUDGET_TOKENS:
        # Anthropic hard-rejects budget_tokens < 1024 — raise to the floor, never drop.
        ctx.adjustments.append(
            Adjustment(
                key="thinking_budget",
                action="clamped",
                canonical_value=thinking_budget,
                sent_value=ANTHROPIC_MIN_BUDGET_TOKENS,
                reason=(
                    f"Anthropic requires thinking.budget_tokens >= {ANTHROPIC_MIN_BUDGET_TOKENS}; "
                    f"raised {thinking_budget} to the minimum"
                ),
            )
        )
        thinking_budget = ANTHROPIC_MIN_BUDGET_TOKENS

    # Anthropic requires max_tokens > thinking.budget_tokens.
    if current_max is None:
        validated_max = max(thinking_budget + 2048, default_max)
    elif current_max <= thinking_budget:
        validated_max = thinking_budget + 2048
        ctx.adjustments.append(
            Adjustment(
                key="max_output_tokens",
                action="clamped",
                canonical_value=current_max,
                sent_value=validated_max,
                reason=(
                    f"Anthropic requires max_tokens ({current_max}) > thinking.budget_tokens "
                    f"({thinking_budget}); adjusted max_tokens to {validated_max}"
                ),
            )
        )
    else:
        validated_max = current_max

    params["thinking"] = {"type": "enabled", "budget_tokens": thinking_budget}
    params["max_tokens"] = validated_max
    return params


def _anthropic_adaptive_thinking(
    canonical: dict[str, Any], params: dict[str, Any], ctx: ProcessorContext
) -> dict[str, Any]:
    default_max = ctx.config.get("default_max_tokens", ANTHROPIC_DEFAULT_MAX_TOKENS)
    current_max = _current_max_tokens(canonical, params)
    # Adaptive thinking has no budget_tokens constraint — max_tokens is the
    # caller's value, translator-defaulted when unset (thinking or not).
    params["max_tokens"] = current_max if current_max is not None else default_max

    effort_level: str | None = None
    thinking_off = False

    # Priority 1: reasoning_effort ("none" is an explicit off switch).
    explicit = _explicit_effort(canonical)
    if explicit is not None:
        if explicit == "none":
            return params
        effort_level = _ANTHROPIC_ADAPTIVE_EFFORT.get(explicit)

    # Priority 2: thinking_budget token ranges (adaptive tiers, NOT the budget map).
    if effort_level is None and canonical.get("thinking_budget") is not None:
        budget = int(canonical["thinking_budget"])
        if budget <= 0:
            thinking_off = True
        elif budget <= 1024:
            effort_level = "low"
        elif budget <= 8192:
            effort_level = "medium"
        else:
            effort_level = "high"

    # Priority 3: thinking_level named levels.
    if effort_level is None and not thinking_off and canonical.get("thinking_level") is not None:
        effort_level = {"minimal": "low", "low": "low", "medium": "medium", "high": "high"}.get(
            canonical["thinking_level"]
        )

    # Priority 4: include_thoughts=False disables thinking outright.
    if canonical.get("include_thoughts") is False:
        return params
    if thinking_off or effort_level is None:
        return params

    # ai_047: engine-side ceiling — the second gate behind ui_values.
    effort_level = _apply_effort_ceiling(effort_level, ctx)

    # Always send display explicitly so the whole adaptive class streams
    # thinking unless the caller opted out with reasoning_summary="never".
    display = "omitted" if canonical.get("reasoning_summary") == "never" else "summarized"
    params["thinking"] = {"type": "adaptive", "display": display}
    existing = params.get("output_config")
    if isinstance(existing, dict):
        existing["effort"] = effort_level
    else:
        params["output_config"] = {"effort": effort_level}
    return params


# ── anthropic_temp_topp_exclusion ────────────────────────────────────────────
# Port of the anthropic translator's sampling coupling (standard api_class):
#   1. temperature OR top_p, never both — temperature wins, top_p dropped.
#   2. when a thinking block is present, Anthropic 400s on temperature != 1,
#      on ANY top_k, and on top_p < 0.95 — drop the incompatible knobs loudly.
# Attach to "temperature" with processor_config consumes=["top_p","top_k"] and
# an order AFTER the thinking processor (it must see params["thinking"]).


@register_processor("anthropic_temp_topp_exclusion")
def anthropic_temp_topp_exclusion(
    canonical: dict[str, Any], params: dict[str, Any], ctx: ProcessorContext
) -> dict[str, Any]:
    temperature = canonical.get("temperature")
    top_p = canonical.get("top_p")
    top_k = canonical.get("top_k")

    if temperature is not None and top_p is not None:
        ctx.adjustments.append(
            Adjustment(
                key="top_p",
                action="dropped",
                canonical_value=top_p,
                sent_value=None,
                reason=(
                    f"Anthropic requires temperature OR top_p, not both — dropped "
                    f"top_p={top_p} and kept temperature={temperature}"
                ),
            )
        )
        top_p = None

    if temperature is not None:
        params["temperature"] = temperature
    if top_p is not None:
        params["top_p"] = top_p
    if top_k is not None:
        params["top_k"] = top_k

    if "thinking" not in params:
        return params

    sent_temp = params.get("temperature")
    if sent_temp is not None and sent_temp != 1:
        params.pop("temperature")
        ctx.adjustments.append(
            Adjustment(
                key="temperature",
                action="dropped",
                canonical_value=sent_temp,
                sent_value=None,
                reason="Anthropic extended thinking requires temperature=1 — dropped",
            )
        )
    if "top_k" in params:
        dropped_top_k = params.pop("top_k")
        ctx.adjustments.append(
            Adjustment(
                key="top_k",
                action="dropped",
                canonical_value=dropped_top_k,
                sent_value=None,
                reason="Anthropic extended thinking accepts no top_k — dropped",
            )
        )
    sent_top_p = params.get("top_p")
    if sent_top_p is not None and sent_top_p < 0.95:
        params.pop("top_p")
        ctx.adjustments.append(
            Adjustment(
                key="top_p",
                action="dropped",
                canonical_value=sent_top_p,
                sent_value=None,
                reason="Anthropic extended thinking only accepts top_p in [0.95, 1] — dropped",
            )
        )
    return params


# ── google_thinking ──────────────────────────────────────────────────────────
# Exact port of ThinkingConfig.to_google_thinking_legacy (mode "legacy") and
# to_google_thinking_3 (mode "gemini_3"). The translator always assigns the
# fragment (even {}) at generation_config.thinking_config — mirrored here.
#
# processor_config:
#   mode: "legacy" | "gemini_3" (REQUIRED — the two wire dialects share nothing)
#   family: "flash" | "pro" (gemini_3 only; default "pro" — mirrors the
#           translator's `"flash" in model_name` probe, per-offering data now)
#   target: provider key for the fragment (default "thinking_config")

# to_google_thinking_legacy effort_to_budget, verbatim (unknown -> 1024 via
# .get(effort, 1024)). "auto" never reaches this map (house auto == unset,
# normalized in canonicalize + _explicit_effort — ai_041): the fragment stays
# empty and the provider default applies (legacy sent budget 1024 for auto —
# deliberate divergence). "none" -> 0 -> the fragment omits thinking_budget
# entirely (send nothing), already standard-compliant.
_GOOGLE_LEGACY_EFFORT_TO_BUDGET: dict[str, int] = {
    "none": 0,
    "minimal": 512,
    "low": 1024,
    "medium": 4096,
    "high": 8192,
    "xhigh": 24576,
}

# to_google_thinking_3 maps — MINUS the legacy "auto"/"none" entries, retired
# by the house auto/none standard (ai_041): "auto" == unset (no thinking_level;
# the provider default applies) and "none" == send nothing (the legacy maps
# collapsed none to a concrete level — "minimal" on flash, "low" on pro — which
# is exactly the violation the standard outlaws). Deliberate divergences from
# the pre-migration golden. Non-native tiers (pro medium -> low, xhigh -> high)
# remain as TRANSLATION compat; the UI never offers them (ui_values).
_GOOGLE_3_EFFORT_TO_LEVEL_FLASH: dict[str, str | None] = {
    "minimal": "minimal",
    "low": "low",
    "medium": "medium",
    "high": "high",
    "xhigh": "high",
}
_GOOGLE_3_EFFORT_TO_LEVEL_PRO: dict[str, str | None] = {
    "minimal": "low",
    "low": "low",
    "medium": "low",
    "high": "high",
    "xhigh": "high",
}
_GOOGLE_3_SUMMARY_TO_INCLUDE: dict[str, bool | None] = {
    "concise": True,
    "always": True,
    "detailed": True,
    "never": False,
    "auto": None,
}


@register_processor("google_thinking")
def google_thinking(
    canonical: dict[str, Any], params: dict[str, Any], ctx: ProcessorContext
) -> dict[str, Any]:
    mode = ctx.config.get("mode")
    target = ctx.config.get("target", "thinking_config")
    if mode == "legacy":
        params[target] = _google_thinking_legacy_fragment(canonical)
        return params
    if mode == "gemini_3":
        params[target] = _google_thinking_3_fragment(
            canonical, ctx.config.get("family", "pro"), ctx
        )
        return params
    raise ValueError(
        f"google_thinking: processor_config mode must be 'legacy' or 'gemini_3', got {mode!r}"
    )


def _google_thinking_legacy_fragment(canonical: dict[str, Any]) -> dict[str, Any]:
    fragment: dict[str, Any] = {}
    include_thoughts = canonical.get("include_thoughts")
    if include_thoughts is False:
        fragment["include_thoughts"] = False
        fragment["thinking_budget"] = -1
        return fragment

    if include_thoughts is not None:
        fragment["include_thoughts"] = include_thoughts

    thinking_budget: int | None = None
    if canonical.get("thinking_budget") is not None:
        thinking_budget = int(canonical["thinking_budget"])
    else:
        effort = _explicit_effort(canonical)
        if effort:
            thinking_budget = _GOOGLE_LEGACY_EFFORT_TO_BUDGET.get(effort, 1024)

    if thinking_budget is not None and thinking_budget > 0:
        fragment["thinking_budget"] = thinking_budget
    return fragment


def _google_thinking_3_fragment(
    canonical: dict[str, Any], family: str, ctx: ProcessorContext
) -> dict[str, Any]:
    fragment: dict[str, Any] = {}
    thinking_level: str | None = None
    include_thoughts: bool | None = None

    effort = _explicit_effort(canonical)
    if effort:
        level_map = (
            _GOOGLE_3_EFFORT_TO_LEVEL_FLASH if family == "flash" else _GOOGLE_3_EFFORT_TO_LEVEL_PRO
        )
        thinking_level = level_map.get(effort)

    reasoning_summary = canonical.get("reasoning_summary")
    if reasoning_summary:
        include_thoughts = _GOOGLE_3_SUMMARY_TO_INCLUDE.get(reasoning_summary)

    # House "none" (ai_041): send nothing — no thinking_level, and the raw
    # thinking_budget fallback must not resurrect one.
    if effort != "none" and thinking_level is None and canonical.get("thinking_budget") is not None:
        budget = int(canonical["thinking_budget"])
        if budget <= 0:
            thinking_level = None
        elif budget <= 512:
            thinking_level = "minimal"
        elif budget <= 1024:
            thinking_level = "low"
        elif budget <= 4096:
            thinking_level = "medium"
        else:
            thinking_level = "high"

    if canonical.get("include_thoughts") is not None:
        include_thoughts = canonical["include_thoughts"]

    # The family maps above are per-FAMILY; whether THIS model accepts the level
    # they produced is per-MODEL, and only the offering knows it. Gemini 3.5
    # Flash takes "minimal", 3.7 Flash does not — same map, same family.
    thinking_level = ctx.reconcile_supported(thinking_level)

    if thinking_level is not None:
        fragment["thinking_level"] = thinking_level
    if include_thoughts is not None:
        fragment["include_thoughts"] = include_thoughts
    return fragment


# ── together_reasoning ───────────────────────────────────────────────────────
# Exact port of ThinkingConfig.to_together_reasoning_params. Together/Z.AI
# thinking models default to reasoning_effort="max" when the field is OMITTED —
# expensive and never our product default — so an explicit effort is ALWAYS
# sent. "none" (which canonicalize also produces from disable_reasoning=True)
# instead disables reasoning via the nested reasoning.enabled=false switch —
# a DIFFERENT provider key, which is why this is a processor and not a scalar
# value_map rule (a value_map can only land values on ONE provider_key).
#
# Reads canonical: reasoning_effort (+_reasoning_effort_derived; a budget-derived
# tier is treated as unset, mirroring from_settings which never derives effort
# from thinking_budget). Writes params: reasoning_effort OR reasoning.enabled.


@register_processor("together_reasoning")
def together_reasoning(
    canonical: dict[str, Any], params: dict[str, Any], ctx: ProcessorContext
) -> dict[str, Any]:
    effort = _explicit_effort(canonical)
    if effort == "none":
        # House-"none" reconciliation (ai_041): Together has a NATIVE off switch
        # (reasoning.enabled=false) and omission means reasoning_effort="max" —
        # so "send nothing" here is the explicit disable, never an effort level.
        params["reasoning"] = {"enabled": False}
        return params
    # Anything short of an explicit deep ask is "high" (OUR default, incl. unset).
    params["reasoning_effort"] = "max" if effort in ("xhigh", "max") else "high"
    return params


# ═════════════════════════════════════════════════════════════════════════════
# MEDIA processors (B2-media) — exact ports of the media translators' dimension
# / count / gating arithmetic (providers/_media_dims.py + the param blocks in
# providers/*/*_image_api.py, *_video_api.py, openai|google translators).
# Parity is held by tests/test_catalog_media_processors_parity.py and
# scripts/validate_media_parity.py.
#
# Context keys builders pass to ``outbound(..., context=...)``:
#   operation:        "generate" (default) | "edit" — openai image dual-endpoint
#   has_image_input:  bool — any start/reference image on the request (flux
#                     safety_tolerance caps at 2 when editing)
# ═════════════════════════════════════════════════════════════════════════════

# Verbatim port of providers/_media_dims.py::_ASPECT_TO_DEFAULT_WH.
_MEDIA_ASPECT_TO_WH: dict[str, tuple[int, int]] = {
    "1:1": (1024, 1024),
    "16:9": (1536, 1024),
    "9:16": (1024, 1536),
    "4:3": (1408, 1024),
    "3:4": (1024, 1408),
    "21:9": (1920, 832),
    "9:21": (832, 1920),
    "3:2": (1536, 1024),
    "2:3": (1024, 1536),
}


def _derive_wh_table(canonical: dict[str, Any]) -> tuple[int | None, int | None]:
    """Port of _media_dims.derive_wh: explicit width+height wins, else the
    aspect table, else parse "A:B" anchored on a 1024 short edge (16-multiples),
    else (None, None)."""
    width, height = canonical.get("width"), canonical.get("height")
    if width and height:
        return int(width), int(height)
    aspect = canonical.get("aspect_ratio")
    if aspect:
        wh = _MEDIA_ASPECT_TO_WH.get(aspect)
        if wh:
            return wh
        try:
            a, b = (int(x) for x in str(aspect).split(":", 1))
            if a >= b:
                return (round(1024 * a / b / 16) * 16, 1024)
            return (1024, round(1024 * b / a / 16) * 16)
        except (ValueError, TypeError):
            return (None, None)
    return (None, None)


def _derive_wh_anchor1024(canonical: dict[str, Any]) -> tuple[int, int]:
    """Port of TogetherImageGeneration._derive_wh: NO table — every ratio is
    computed off a 1024 short edge; unparseable/missing ratios fall back 1:1."""
    aspect = canonical.get("aspect_ratio") or "1:1"
    try:
        a, b = (int(x) for x in str(aspect).split(":", 1))
    except (ValueError, TypeError):
        a, b = 1, 1
    if a >= b:
        return (round(1024 * a / b / 16) * 16, 1024)
    return (1024, round(1024 * b / a / 16) * 16)


def _derive_aspect_ratio(canonical: dict[str, Any]) -> str | None:
    """Port of _media_dims.derive_aspect_ratio: explicit aspect_ratio, else
    gcd-reduced width:height, else None."""
    aspect = canonical.get("aspect_ratio")
    if aspect:
        return aspect
    width, height = canonical.get("width"), canonical.get("height")
    if width and height:
        from math import gcd

        g = gcd(int(width), int(height))
        return f"{int(width) // g}:{int(height) // g}"
    return None


@register_processor("media_dims")
def media_dims(
    canonical: dict[str, Any], params: dict[str, Any], ctx: ProcessorContext
) -> dict[str, Any]:
    """Dimension shaping — the one irreducible media arithmetic.

    processor_config:
      mode: REQUIRED —
        "size"         -> "WxH" string via the table derivation
                          (openai image, recraft, seedream)
        "wh"           -> width+height ints; arithmetic: "table" | "anchor1024"
                          (together image always sends both)
        "aspect_ratio" -> ratio string, optionally derived from width/height
                          (derive, default True), gated by ``allowed`` with
                          ``fallback`` (send fallback on miss/unset) or dropped
        "sora_size"    -> openai video: table size string, else the
                          aspect+resolution grid with 720p default
      target: provider key (defaults: size/"size", aspect_ratio/"aspect_ratio")
      default: (size mode) value sent when nothing derives
      default_operations: (size mode) only apply ``default`` when
                          ctx.extra["operation"] is in this list
      consumes: width/height/aspect_ratio(/resolution) per family
    """
    mode = ctx.config.get("mode")
    if mode == "size":
        target = ctx.config.get("target", "size")
        width, height = _derive_wh_table(canonical)
        if width and height:
            params[target] = f"{width}x{height}"
            return params
        default = ctx.config.get("default")
        if default is not None:
            operations = ctx.config.get("default_operations")
            operation = (ctx.extra or {}).get("operation", "generate")
            if operations is None or operation in operations:
                params[target] = default
        return params

    if mode == "wh":
        width, height = canonical.get("width"), canonical.get("height")
        if width and height:
            width, height = int(width), int(height)
        elif ctx.config.get("arithmetic", "table") == "anchor1024":
            width, height = _derive_wh_anchor1024(canonical)
        else:
            width, height = _derive_wh_table(canonical)
        if width and height:
            params["width"] = width
            params["height"] = height
        return params

    if mode == "aspect_ratio":
        target = ctx.config.get("target", "aspect_ratio")
        derive = ctx.config.get("derive", True)
        aspect = _derive_aspect_ratio(canonical) if derive else canonical.get("aspect_ratio")
        if aspect is None:
            # ``default`` fills an UNSET ratio before the gate (imagen "1:1",
            # google video "16:9", replicate gpt-image "1:1").
            aspect = ctx.config.get("default")
        allowed = ctx.config.get("allowed")
        if allowed is not None and aspect is not None and aspect not in allowed:
            # A SET-but-unsupported ratio takes ``fallback`` when configured
            # (imagen / google video), else it is dropped (replicate gpt-image
            # sends nothing on a gated miss).
            fallback = ctx.config.get("fallback")
            if fallback is not None:
                ctx.adjustments.append(
                    Adjustment(
                        key="aspect_ratio",
                        action="mapped",
                        canonical_value=aspect,
                        sent_value=fallback,
                        reason=(
                            f"aspect_ratio={aspect!r} is not supported here "
                            f"(allowed: {allowed}) — sent {fallback!r} instead"
                        ),
                    )
                )
            else:
                ctx.adjustments.append(
                    Adjustment(
                        key="aspect_ratio",
                        action="dropped",
                        canonical_value=aspect,
                        sent_value=None,
                        reason=(
                            f"aspect_ratio={aspect!r} is not supported here "
                            f"(allowed: {allowed}) — dropped"
                        ),
                    )
                )
            aspect = fallback
        if aspect is not None:
            params[target] = aspect
        return params

    if mode == "sora_size":
        target = ctx.config.get("target", "size")
        width, height = _derive_wh_table(canonical)
        if width and height:
            params[target] = f"{width}x{height}"
            return params
        aspect = canonical.get("aspect_ratio") or "16:9"
        resolution = (canonical.get("resolution") or "720p").lower()
        landscape = aspect in ("16:9", "21:9", "3:2", "4:3", "1:1")
        if resolution == "1080p":
            params[target] = "1920x1080" if landscape else "1080x1920"
        elif resolution == "1024p":
            params[target] = "1792x1024" if landscape else "1024x1792"
        else:
            params[target] = "1280x720" if landscape else "720x1280"
        return params

    raise ValueError(f"media_dims: unknown processor_config mode {mode!r}")


@register_processor("media_count")
def media_count(
    canonical: dict[str, Any], params: dict[str, Any], ctx: ProcessorContext
) -> dict[str, Any]:
    """Asset-count shaping: ``max(1, min(count or 1, max))`` under the
    provider's key. processor_config: target (REQUIRED), max (REQUIRED),
    omit_at_or_below (default 0 — replicate omits the field entirely at
    count<=1)."""
    target = ctx.config["target"]
    cap = int(ctx.config["max"])
    raw = canonical.get("count")
    n = max(1, min(int(raw or 1), cap))
    if raw is not None and int(raw) > cap:
        ctx.adjustments.append(
            Adjustment(
                key="count",
                action="clamped",
                canonical_value=int(raw),
                sent_value=n,
                reason=f"count={raw} clamped to the per-call maximum {cap}",
            )
        )
    if n <= int(ctx.config.get("omit_at_or_below", 0)):
        return params
    params[target] = n
    return params


@register_processor("media_cast")
def media_cast(
    canonical: dict[str, Any], params: dict[str, Any], ctx: ProcessorContext
) -> dict[str, Any]:
    """Typed rename with an int() base cast — for providers that take a
    canonical number in a different scalar type (Sora/Together ``seconds`` is a
    STRING; together-video guidance_scale is int()). processor_config:
    source (default: the rule key), target (default: source), to: "int" (default)
    | "str", max (optional pre-cast ceiling — sora extend's min(20, x))."""
    source = ctx.config.get("source", ctx.key)
    value = canonical.get(source)
    if value is None:
        return params
    value = int(value)
    ceiling = ctx.config.get("max")
    if ceiling is not None and value > int(ceiling):
        ctx.adjustments.append(
            Adjustment(
                key=source,
                action="clamped",
                canonical_value=value,
                sent_value=int(ceiling),
                reason=f"{source}={value} exceeds the per-call maximum {ceiling}",
            )
        )
        value = int(ceiling)
    if ctx.config.get("to", "int") == "str":
        value = str(value)
    params[ctx.config.get("target", source)] = value
    return params


@register_processor("openai_image_gen_only")
def openai_image_gen_only(
    canonical: dict[str, Any], params: dict[str, Any], ctx: ProcessorContext
) -> dict[str, Any]:
    """The two knobs images.generate() takes that images.edit() rejects —
    omitted entirely on operation="edit" (port of to_openai_image_generate vs
    to_openai_image_edit):

      * moderation — ALWAYS sent on generate (explicit value wins, else the
        least-restrictive ``default``, "low").
      * background — passthrough, EXCEPT "transparent" is silently stripped
        when processor_config["background_transparent_drop"] is true
        (gpt-image-2 rejects transparent).

    Attach to "moderation" with consumes=["background"].
    """
    if (ctx.extra or {}).get("operation", "generate") != "generate":
        return params
    params["moderation"] = canonical.get("moderation") or ctx.config.get("default", "low")
    background = canonical.get("background")
    if background is not None:
        if background == "transparent" and ctx.config.get("background_transparent_drop"):
            ctx.adjustments.append(
                Adjustment(
                    key="background",
                    action="dropped",
                    canonical_value=background,
                    sent_value=None,
                    reason="this model rejects background='transparent' — dropped",
                )
            )
        else:
            params["background"] = background
    return params


@register_processor("openai_partial_images")
def openai_partial_images(
    canonical: dict[str, Any], params: dict[str, Any], ctx: ProcessorContext
) -> dict[str, Any]:
    """partial_images > 0 opts into SSE partial streaming: send the count AND
    stream=True; otherwise send neither. Port of openai/translator.py:433."""
    count = canonical.get("partial_images")
    if count is not None and int(count) > 0:
        params["partial_images"] = int(count)
        params["stream"] = True
    return params


@register_processor("flux_safety_tolerance")
def flux_safety_tolerance(
    canonical: dict[str, Any], params: dict[str, Any], ctx: ProcessorContext
) -> dict[str, Any]:
    """Replicate FLUX.2: always push safety_tolerance to the most permissive
    value (5), except the BFL backend caps it at 2 whenever an input/reference
    image is present (400s above). Port of model_descriptors._flux_2_input."""
    params["safety_tolerance"] = 2 if (ctx.extra or {}).get("has_image_input") else 5
    return params


@register_processor("xai_image_resolution")
def xai_image_resolution(
    canonical: dict[str, Any], params: dict[str, Any], ctx: ProcessorContext
) -> dict[str, Any]:
    """xai-sdk resolution: "1k"/"2k" pass; else width>=2048 -> "2k", any other
    width -> "1k", nothing -> omitted. Port of xai_image_api._build_kwargs."""
    resolution = canonical.get("resolution")
    if resolution in ("1k", "2k"):
        params["resolution"] = resolution
        return params
    width = canonical.get("width")
    if width and int(width) >= 2048:
        params["resolution"] = "2k"
    elif width:
        params["resolution"] = "1k"
    return params


@register_processor("google_imagen_size")
def google_imagen_size(
    canonical: dict[str, Any], params: dict[str, Any], ctx: ProcessorContext
) -> dict[str, Any]:
    """Imagen image_size ("1K"/"2K"): resolution tier map first, else a width
    threshold (>=2048 -> 2K), else omitted. Port of GoogleTranslator._derive_image_size
    (canonical resolution is already lowercase)."""
    resolution = canonical.get("resolution")
    if resolution:
        mapped = {
            "1k": "1K",
            "2k": "2K",
            "720p": "1K",
            "1080p": "1K",
            "4k": "2K",
            "1080": "1K",
        }.get(resolution)
        if mapped:
            params["image_size"] = mapped
            return params
    width = canonical.get("width")
    if width:
        try:
            params["image_size"] = "2K" if int(width) >= 2048 else "1K"
        except (ValueError, TypeError):
            pass
    return params


__all__ = [
    "ANTHROPIC_DEFAULT_MAX_TOKENS",
    "ANTHROPIC_MIN_BUDGET_TOKENS",
    "ProcessorContext",
    "ProcessorFn",
    "UnknownProcessorError",
    "anthropic_temp_topp_exclusion",
    "anthropic_thinking",
    "flux_safety_tolerance",
    "get_processor",
    "google_imagen_size",
    "google_thinking",
    "has_processor",
    "media_cast",
    "media_count",
    "media_dims",
    "openai_image_gen_only",
    "openai_partial_images",
    "register_processor",
    "together_reasoning",
    "xai_image_resolution",
]
