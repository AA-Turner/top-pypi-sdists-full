"""Registered param processors — the ControlRule ``processor`` escape hatch.

A processor is a PURE function over (canonical config, assembled provider
params, context) — no DB access, no api_class reads. It runs in outbound's
SECOND pass, after every scalar rule (const/value_map/clamp/rename/default),
so it can see and mutate the fully assembled provider params. Run order across
processors: ``processor_config["order"]`` (default 100), tie-broken by key.

The built-ins below are the exact (now sole) owners of the irreducible
thinking arithmetic ported from the retired ThinkingConfig; the chat param
golden (tests/fixtures/chat_param_golden) freezes their behaviour.

TRANSLATION TABLES ARE DATA (settings-translation C5, CONTRACTS.md K6). No
table lives here: a processor reads its numbers/maps from ITS rule —
``rule.from_number`` (number -> scale), ``rule.to_number`` (scale -> number),
``rule.processor_config[...]`` (maps / thresholds) — and falls back to the
declared defaults in ``catalog/translation_defaults.py`` (today's behaviour)
when the rule carries none.

Converted-sibling note: ``CompiledControlsMap.bridge_numbers`` (the
target-aware outbound seam) converts a raw thinking_budget into a
reasoning_effort when the caller set no effort, and records it in
``canonical["_converted"]`` ({target_key: source_key}). A processor owning the
raw number must treat a converted effort as UNSET (``_explicit_effort``) and
translate the raw budget through its own numbers.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from matrx_utils import vcprint

from matrx_ai.catalog import translation_defaults as D
from matrx_ai.catalog.models import Adjustment, ControlRule

# The house enum values (ai_041): "auto" = leave the key unset (the provider
# default applies), "none" = send nothing. They are POSTURES, not degrees —
# see ProcessorContext.reconcile_supported for why that distinction is
# load-bearing.
_HOUSE_VALUES = D.HOUSE_VALUES


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
    # The model's real output maximum (CompiledControlsMap.output_maximum) — a
    # processor that WRITES the output ceiling must never write above it.
    output_maximum: int | None = None
    # THE RULE this processor is attached to — the source of its translation
    # tables (from_number / to_number / processor_config). None only for a
    # context built by hand outside outbound; then the declared defaults apply.
    rule: ControlRule | None = None
    # K6 ``accepts`` — the capability list, when the rule declares one. Unlike
    # ``supported_values`` (accepts, else ui_values — the Gemini-3 contract
    # since 2026-08-17), this is EMPTY unless the rule declares ``accepts``,
    # so processors that never enforced ui_values keep not enforcing them.
    accepts: frozenset[str] = frozenset()

    def cap_output(self, value: int) -> int:
        return min(value, self.output_maximum) if self.output_maximum else value

    # ── the rule's tables, else the declared defaults ────────────────────────
    def from_number(self, number: float, default: list[dict[str, Any]]) -> Any:
        """number -> scale through the rule's ``from_number`` (else ``default``)."""
        steps = self.rule.from_number if self.rule is not None and self.rule.from_number else default
        return D.step_lookup(steps, number)

    def to_number_table(self, default: dict[str, int]) -> dict[str, int]:
        """scale -> number table: the rule's ``to_number`` (else ``default``)."""
        if self.rule is not None and self.rule.to_number:
            return self.rule.to_number
        return default

    def table(self, name: str, default: Any) -> Any:
        """A map/threshold from ``processor_config[name]`` (else ``default``)."""
        value = self.config.get(name)
        return default if value is None else value

    def reconcile_accepted(self, value: str | None) -> str | None:
        """K6 ``accepts`` on a processor's OUTPUT: like ``reconcile_supported``
        but only when the rule declares ``accepts`` (seed semantics — a rule with
        ui_values and no accepts behaves exactly as before)."""
        if value is None or not self.accepts:
            return value
        saved = self.supported_values
        self.supported_values = self.accepts
        try:
            return self.reconcile_supported(value)
        finally:
            self.supported_values = saved

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
                provenance="computed",  # K9: the nearest metric decided
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
    # An effort CONVERTED from the raw budget (bridge_numbers) must NOT drive
    # provider-specific effort maps — the processor translates the raw budget
    # through its own numbers (the rule's from_number / to_number).
    if "reasoning_effort" in (canonical.get("_converted") or {}):
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
#   effort_ceiling: str | None (adaptive only — ai_047; order = translation_defaults)
#   consumes / order: engine keys (see controls.py)
#
# Reads canonical: reasoning_effort (+_converted), thinking_budget,
# thinking_level, include_thoughts, reasoning_summary, max_output_tokens.
# Writes params: thinking, output_config.effort (adaptive), max_tokens.

# Re-exported for importers of the historical names; the values live in
# translation_defaults (declared defaults, overridable per rule).
ANTHROPIC_MIN_BUDGET_TOKENS = D.ANTHROPIC_MIN_BUDGET_TOKENS
GOOGLE_THINKING_BUDGET_FIELD_MAX = D.GOOGLE_THINKING_BUDGET_FIELD_MAX
# LAST RESORT ONLY — the offering's own `default_max_tokens` is the answer, and
# it must BE the model's real `ai.model_definition.max_tokens` (2026-09-11: all
# eleven Anthropic offerings declared 32,768 while Opus 5 / Sonnet 5 could do
# 128,000). Never raise it to chase a new model. Guard:
# `python scripts/check_output_ceiling_defaults.py` (`--self-test`).
ANTHROPIC_DEFAULT_MAX_TOKENS = D.ANTHROPIC_DEFAULT_MAX_TOKENS

# Tables (each overridable by the rule — see translation_defaults):
#   budget mode   effort -> budget_tokens        rule.to_number
#   adaptive mode effort -> output_config.effort processor_config["effort_map"]
#                 budget -> effort               rule.from_number
#                 thinking_level -> effort       processor_config["thinking_level_map"]
# ai_045: "xhigh"/"max" pass through natively on adaptive; product gating of the
# expensive tiers is the offering's ui_values + ``effort_ceiling`` (ai_047).
# "auto" never reaches a table (house auto == unset, ai_041); "none" (explicit
# off) is handled before any table is consulted.


def _apply_effort_ceiling(
    effort_level: str, ctx: ProcessorContext
) -> str:
    ceiling = ctx.config.get("effort_ceiling")
    if ceiling is None:
        return effort_level
    order: tuple[str, ...] = tuple(ctx.table("effort_order", D.ANTHROPIC_ADAPTIVE_EFFORT_ORDER))
    if ceiling not in order:
        vcprint(
            f"anthropic_thinking processor_config.effort_ceiling={ceiling!r} is not a "
            f"valid adaptive effort tier {order}.\n"
            f"  Fix the ai.offering override / ai.api.rules row for key '{ctx.key}'.",
            title="🚨 AI CATALOG INVALID EFFORT CEILING",
            color="red",
        )
        raise ValueError(
            f"anthropic_thinking: invalid processor_config effort_ceiling {ceiling!r} "
            f"(expected one of {order})"
        )
    if effort_level not in order:
        return effort_level
    if order.index(effort_level) <= order.index(ceiling):
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


def effort_lookup(table: dict[str, Any], effort: str, unknown: Any = None) -> Any:
    """``table[effort]``; an effort ABOVE the table's top lands on the TOP entry.

    Live 2026-10-04: the Gemini 2.5 effort->budget table stops at ``xhigh``, so
    ``max`` fell to the 1,024 "unknown effort" budget — maximum effort became
    minimal thinking (and Anthropic budget mode sent no thinking at all). The
    model's real ceiling belongs in the table's top (or the cell's to_number /
    clamp); ``unknown`` is only for a value that is not on the scale."""
    if effort in table:
        return table[effort]
    if effort in D.EFFORT_SCALE:
        ranked = [k for k in table if k in D.EFFORT_SCALE]
        if ranked:
            top = max(ranked, key=D.EFFORT_SCALE.index)
            if D.EFFORT_SCALE.index(effort) > D.EFFORT_SCALE.index(top):
                return table[top]
    return unknown


def _unset_output_default(ctx: ProcessorContext) -> int:
    """The output cap sent when the caller declared none: the MODEL'S REAL MAXIMUM
    (``ctx.output_maximum``, ai.model_definition.max_tokens) whenever it is known.
    A cell's ``default_max_tokens`` is a fallback only — an api- or profile-layer
    cell cannot know each member model's room (live 2026-10-04: the anthropic_chat
    api cell said 32768 and Claude Haiku 4.5 / Sonnet 4.5 were capped at half
    their 64,000). Guard: scripts/check_output_ceiling_defaults.py (the wire)."""
    if ctx.output_maximum:
        return int(ctx.output_maximum)
    return int(ctx.config.get("default_max_tokens", ANTHROPIC_DEFAULT_MAX_TOKENS))


def _anthropic_budget_thinking(
    canonical: dict[str, Any], params: dict[str, Any], ctx: ProcessorContext
) -> dict[str, Any]:
    default_max = _unset_output_default(ctx)
    current_max = _current_max_tokens(canonical, params)
    min_budget = int(ctx.table("min_budget_tokens", D.ANTHROPIC_MIN_BUDGET_TOKENS))
    headroom = int(ctx.table("max_tokens_headroom", D.ANTHROPIC_MAX_TOKENS_HEADROOM))

    # Budget resolution — thinking_budget WINS over effort (legacy contract).
    thinking_budget: int | None = None
    if canonical.get("thinking_budget") is not None:
        thinking_budget = int(canonical["thinking_budget"])
    else:
        effort = _explicit_effort(canonical)
        if effort:
            thinking_budget = effort_lookup(ctx.to_number_table(D.ANTHROPIC_EFFORT_TO_BUDGET), effort)

    if not thinking_budget:  # None or 0 — no thinking; translator max_tokens fallback
        params["max_tokens"] = ctx.cap_output(current_max if current_max is not None else default_max)
        return params

    if thinking_budget < min_budget:
        # Anthropic hard-rejects budget_tokens < 1024 — raise to the floor, never drop.
        ctx.adjustments.append(
            Adjustment(
                key="thinking_budget",
                action="clamped",
                canonical_value=thinking_budget,
                sent_value=min_budget,
                reason=(
                    f"Anthropic requires thinking.budget_tokens >= {min_budget}; "
                    f"raised {thinking_budget} to the minimum"
                ),
            )
        )
        thinking_budget = min_budget

    # Anthropic requires max_tokens > thinking.budget_tokens.
    if current_max is None:
        validated_max = max(thinking_budget + headroom, default_max)
    elif current_max <= thinking_budget:
        # Chair ruling R-a (2026-10-04): a translation never DEFEATS what the person
        # explicitly set. Their output cap is honoured; the THINKING yields to fit
        # under it (live e7c78e54: effort max + cap 50 was sent max_tokens 26624).
        # Anthropic needs budget >= min_budget and max_tokens > budget, and the
        # answer needs room (R-b: an empty answer is a failure) — so the budget
        # shrinks to leave ``headroom`` visible tokens, and when even the floor
        # budget cannot fit, thinking is switched off (the nearest honest
        # equivalent). Silent: a conversion is the system working.
        cap = ctx.cap_output(current_max)
        fitted = cap - headroom
        if fitted >= min_budget:
            ctx.adjustments.append(
                Adjustment(
                    key="thinking_budget",
                    action="clamped",
                    canonical_value=thinking_budget,
                    sent_value=fitted,
                    provenance="computed",
                    reason=(
                        f"thinking budget {thinking_budget} fitted to {fitted} so the "
                        f"requested output cap {cap} still leaves room for the answer"
                    ),
                )
            )
            params["thinking"] = {"type": "enabled", "budget_tokens": fitted}
            params["max_tokens"] = cap
            return params
        ctx.adjustments.append(
            Adjustment(
                key="thinking_budget",
                action="omitted",
                canonical_value=thinking_budget,
                sent_value=None,
                provenance="computed",
                reason=(
                    f"the requested output cap {cap} is below the smallest thinking budget "
                    f"Anthropic accepts ({min_budget}); thinking switched off to honour the cap"
                ),
            )
        )
        params.pop("thinking", None)
        params["max_tokens"] = cap
        return params
    else:
        validated_max = current_max

    # The model's real maximum outranks "max_tokens > budget": raising max_tokens
    # past it is a provider 400, so the BUDGET yields instead (it must stay below
    # max_tokens and at or above Anthropic's floor).
    capped_max = ctx.cap_output(validated_max)
    if capped_max != validated_max:
        validated_max = capped_max
        if thinking_budget >= validated_max:
            fitted = max(min_budget, validated_max - headroom)
            ctx.adjustments.append(
                Adjustment(
                    key="thinking_budget",
                    action="clamped",
                    canonical_value=thinking_budget,
                    sent_value=fitted,
                    provenance="computed",  # K9: fitted to the model's maximum
                    reason=(
                        f"thinking.budget_tokens {thinking_budget} must stay below max_tokens, "
                        f"which this model caps at {validated_max}; budget fitted to {fitted}"
                    ),
                )
            )
            thinking_budget = fitted

    params["thinking"] = {"type": "enabled", "budget_tokens": thinking_budget}
    params["max_tokens"] = validated_max
    return params


def _always_on_thinking_floor(
    params: dict[str, Any],
    ctx: ProcessorContext,
    *,
    effort_level: str | None,
    key: str,
    requested: Any,
) -> dict[str, Any]:
    """processor_config.thinking_always_on: the NEAREST honest equivalent of "off".

    Claude Opus 5.5 and Fable 5.1 (and Mythos 5 / 5.1) reject
    ``thinking: {"type": "disabled"}`` and have no way to switch reasoning off.
    Omitting the block is not "off" either — it runs the model's DEFAULT effort
    (medium on Opus 5.5), i.e. more thinking than the caller asked for. Per THE
    EQUIVALENCE LAW (nearest is the default), the closest thing to "no thinking"
    that the model accepts is adaptive thinking at the lowest effort with nothing
    displayed. If the caller also named an effort (e.g. include_thoughts=False with
    reasoning_effort="high") that effort is kept — they asked for depth, just not
    to see it. This is a CONVERSION (``mapped``): logged on the server, silent to
    the client, like every other conversion.
    """
    effort = _apply_effort_ceiling(
        effort_level or ctx.table("always_on_floor_effort", D.ANTHROPIC_ALWAYS_ON_FLOOR_EFFORT), ctx
    )
    ctx.adjustments.append(
        Adjustment(
            key=key,
            action="mapped",
            canonical_value=requested,
            sent_value={"thinking": "adaptive", "effort": effort, "display": "omitted"},
            reason=(
                "this model's thinking is always on and cannot be disabled "
                "(thinking.type='disabled' is rejected); sent the nearest equivalent: "
                f"adaptive thinking at effort '{effort}' with display omitted"
            ),
        )
    )
    params["thinking"] = {"type": "adaptive", "display": "omitted"}
    existing = params.get("output_config")
    if isinstance(existing, dict):
        existing["effort"] = effort
    else:
        params["output_config"] = {"effort": effort}
    return params


def _anthropic_adaptive_thinking(
    canonical: dict[str, Any], params: dict[str, Any], ctx: ProcessorContext
) -> dict[str, Any]:
    default_max = _unset_output_default(ctx)
    current_max = _current_max_tokens(canonical, params)
    # Adaptive thinking has no budget_tokens constraint — max_tokens is the
    # caller's value, translator-defaulted when unset (thinking or not).
    params["max_tokens"] = ctx.cap_output(current_max if current_max is not None else default_max)

    effort_level: str | None = None
    thinking_off = False
    # processor_config.thinking_always_on — the model rejects thinking.type
    # "disabled" (Opus 5.5, Fable 5.1, Mythos 5 / 5.1). Every "off" signal below
    # then converts to the nearest accepted equivalent instead of omitting the
    # block (which would silently run the model's DEFAULT, deeper, effort).
    always_on = bool(ctx.config.get("thinking_always_on"))

    # Priority 1: reasoning_effort ("none" is an explicit off switch).
    explicit = _explicit_effort(canonical)
    if explicit is not None:
        if explicit == "none":
            if always_on:
                return _always_on_thinking_floor(
                    params, ctx, effort_level=None, key="reasoning_effort", requested="none"
                )
            return params
        effort_level = ctx.table("effort_map", D.ANTHROPIC_ADAPTIVE_EFFORT).get(explicit)

    # Priority 2: thinking_budget token ranges (adaptive tiers via the rule's
    # from_number, NOT the budget map). A budget <= 0 is OFF.
    if effort_level is None and canonical.get("thinking_budget") is not None:
        budget = int(canonical["thinking_budget"])
        if budget <= 0:
            thinking_off = True
        else:
            effort_level = ctx.from_number(budget, D.ANTHROPIC_ADAPTIVE_FROM_NUMBER)

    # Priority 3: thinking_level named levels.
    if effort_level is None and not thinking_off and canonical.get("thinking_level") is not None:
        effort_level = ctx.table("thinking_level_map", D.ANTHROPIC_ADAPTIVE_THINKING_LEVEL).get(
            canonical["thinking_level"]
        )

    # VISIBILITY IS NEVER DEPTH (settings-translation C7b). include_thoughts=False
    # and reasoning_summary="never" HIDE the thoughts; they never turn thinking
    # off and never change its effort. Before C7b include_thoughts=False dropped
    # the thinking block (or, always-on, floored the effort to "low").
    hide = canonical.get("include_thoughts") is False or canonical.get("reasoning_summary") == "never"
    if thinking_off:
        if always_on:
            return _always_on_thinking_floor(
                params,
                ctx,
                effort_level=None,
                key="thinking_budget",
                requested=canonical.get("thinking_budget"),
            )
        return params
    if effort_level is None:
        # No depth asked for. A model that thinks anyway (always-on, or
        # processor_config.thinks_by_default — Opus 5 / Sonnet 5, probed) is
        # told to hide its thoughts at ITS OWN default effort; any other model
        # is not thinking, so there is nothing to hide and nothing is sent.
        if hide and (always_on or ctx.config.get("thinks_by_default")):
            params["thinking"] = {"type": "adaptive", "display": "omitted"}
        return params

    # ai_047: engine-side ceiling — the second gate behind ui_values.
    effort_level = _apply_effort_ceiling(effort_level, ctx)
    # K6 accepts on the processor's output (only when the rule declares it).
    effort_level = ctx.reconcile_accepted(effort_level)
    if effort_level is None:
        return params

    # Always send display explicitly so the whole adaptive class streams
    # thinking unless the caller hid it (include_thoughts=False /
    # reasoning_summary="never").
    display = "omitted" if hide else "summarized"
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

    # ai_076 — THE WIRE CONTAINER IS CATALOG DATA. anthropic SDK 1.x dropped the
    # sampling kwargs from messages.create/stream while the Messages API still
    # accepts them on the non-adaptive models, so the api rule declares
    # processor_config.wire_container="extra_body" and the three keys are
    # emitted nested there (same bytes on the wire). Absent → top-level, and
    # the shared SDK-drift guard (providers/sdk_drift.py) is the loud backstop.
    container = ctx.config.get("wire_container")
    if container:
        wire = params.get(container)
        if not isinstance(wire, dict):
            wire = {}
            params[container] = wire
    else:
        wire = params

    if temperature is not None:
        wire["temperature"] = temperature
    if top_p is not None:
        wire["top_p"] = top_p
    if top_k is not None:
        wire["top_k"] = top_k

    if "thinking" not in params:
        return _prune_empty_container(params, container)

    required_temp = ctx.table("thinking_temperature", D.ANTHROPIC_THINKING_TEMPERATURE)
    min_top_p = ctx.table("thinking_min_top_p", D.ANTHROPIC_THINKING_MIN_TOP_P)
    sent_temp = wire.get("temperature")
    if sent_temp is not None and sent_temp != required_temp:
        wire.pop("temperature")
        ctx.adjustments.append(
            Adjustment(
                key="temperature",
                action="dropped",
                canonical_value=sent_temp,
                sent_value=None,
                reason=f"Anthropic extended thinking requires temperature={required_temp} — dropped",
            )
        )
    if "top_k" in wire:
        dropped_top_k = wire.pop("top_k")
        ctx.adjustments.append(
            Adjustment(
                key="top_k",
                action="dropped",
                canonical_value=dropped_top_k,
                sent_value=None,
                reason="Anthropic extended thinking accepts no top_k — dropped",
            )
        )
    sent_top_p = wire.get("top_p")
    if sent_top_p is not None and sent_top_p < min_top_p:
        wire.pop("top_p")
        ctx.adjustments.append(
            Adjustment(
                key="top_p",
                action="dropped",
                canonical_value=sent_top_p,
                sent_value=None,
                reason=f"Anthropic extended thinking only accepts top_p in [{min_top_p}, 1] — dropped",
            )
        )
    return _prune_empty_container(params, container)


def _prune_empty_container(params: dict[str, Any], container: str | None) -> dict[str, Any]:
    """Never send an empty ``extra_body: {}`` — it is noise on the wire and in
    every request snapshot/golden."""
    if container and isinstance(params.get(container), dict) and not params[container]:
        params.pop(container)
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

# Tables (each overridable by the rule — see translation_defaults):
#   legacy   effort -> thinking_budget        rule.to_number (unknown effort ->
#                                             processor_config["unknown_effort_budget"])
#   gemini_3 effort -> thinking_level         processor_config["level_map"] (else
#                                             the family's default table)
#            thinking_budget -> level         rule.from_number
#            reasoning_summary -> include     processor_config["summary_to_include"]
# House values (ai_041): "auto" never reaches a table (fragment stays empty, the
# provider default applies); "none" sends nothing (no level, no budget).
# Non-native gemini_3 tiers (pro medium -> low, xhigh -> high) are TRANSLATION
# compat; the UI never offers them (ui_values).


@register_processor("google_thinking")
def google_thinking(
    canonical: dict[str, Any], params: dict[str, Any], ctx: ProcessorContext
) -> dict[str, Any]:
    mode = ctx.config.get("mode")
    target = ctx.config.get("target", "thinking_config")
    if mode == "legacy":
        fragment = _google_thinking_legacy_fragment(canonical, ctx)
        # A budget authored for a bigger model converts instead of 400ing. The
        # ceiling is the model's THINKING-BUDGET ceiling — never its output
        # maximum (live 2026-10-04, da318b6f: 2.5 Pro's 100,000 was clamped to
        # its 64,000 OUTPUT max and Google refused it; the budget range is
        # per model — boundary-probed 2026-10-04: 2.5 Pro 128..32768, 2.5 Flash
        # 0..24576, 2.5 Flash-Lite 512..24576). The per-model ceiling is the
        # cell's processor_config.max_thinking_budget; undeclared, only the
        # field's own range applies (the safety net repairs from Google's
        # stated range and files the missing cell).
        ceiling = _google_budget_ceiling(ctx)
        budget = fragment.get("thinking_budget")
        if isinstance(budget, int) and budget > ceiling:
            ctx.adjustments.append(
                Adjustment(
                    key="thinking_budget",
                    action="clamped",
                    canonical_value=budget,
                    sent_value=ceiling,
                    reason=f"thinking_budget {budget} clamped to this model's maximum {ceiling}",
                )
            )
            fragment["thinking_budget"] = ceiling
        # ...and a budget BELOW the model's floor clamps UP to it (record ae16d0f2:
        # "The thinking budget 50 is invalid. Please choose a value between 128 and
        # 32768" — 2.5 Pro). The floor is the cell's processor_config.min_thinking_budget.
        floor = ctx.config.get("min_thinking_budget")
        if floor is not None and isinstance(budget, int) and 0 < budget < int(floor):
            ctx.adjustments.append(
                Adjustment(
                    key="thinking_budget",
                    action="clamped",
                    canonical_value=budget,
                    sent_value=int(floor),
                    reason=f"thinking_budget {budget} raised to this model's minimum {int(floor)}",
                )
            )
            fragment["thinking_budget"] = int(floor)
        params[target] = fragment
        return params
    if mode == "gemini_3":
        params[target] = _google_thinking_3_fragment(
            canonical, ctx.config.get("family", D.GOOGLE_3_DEFAULT_FAMILY), ctx
        )
        return params
    raise ValueError(
        f"google_thinking: processor_config mode must be 'legacy' or 'gemini_3', got {mode!r}"
    )


def _google_budget_ceiling(ctx: ProcessorContext) -> int:
    """The model's thinking-budget ceiling: the declared one, else the field's range."""
    return int(ctx.config.get("max_thinking_budget") or D.GOOGLE_THINKING_BUDGET_FIELD_MAX)


def _google_thinking_legacy_fragment(
    canonical: dict[str, Any], ctx: ProcessorContext
) -> dict[str, Any]:
    fragment: dict[str, Any] = {}
    include_thoughts = canonical.get("include_thoughts")
    if include_thoughts is not None:
        fragment["include_thoughts"] = include_thoughts

    thinking_budget: int | None = None
    if canonical.get("thinking_budget") is not None:
        thinking_budget = int(canonical["thinking_budget"])
    else:
        effort = _explicit_effort(canonical)
        if effort:
            thinking_budget = effort_lookup(
                ctx.to_number_table(D.GOOGLE_LEGACY_EFFORT_TO_BUDGET),
                effort,
                ctx.table("unknown_effort_budget", D.GOOGLE_LEGACY_UNKNOWN_EFFORT_BUDGET),
            )
            # MAX effort is the model's real top budget when its ceiling is
            # declared (V2 battery 3e: 2.5 Pro max sent 24,576; its top is 32,768).
            declared = ctx.config.get("max_thinking_budget")
            if effort == D.EFFORT_SCALE[-1] and declared and "max" not in ctx.to_number_table({}):
                thinking_budget = int(declared)

    if thinking_budget is not None and thinking_budget > 0:
        fragment["thinking_budget"] = thinking_budget
    elif include_thoughts is False:
        # Hiding the thoughts is VISIBILITY, not depth: an explicit budget or effort the
        # caller set is kept above; only with none does the hidden-thoughts budget apply.
        fragment["thinking_budget"] = ctx.table(
            "hidden_thoughts_budget", D.GOOGLE_LEGACY_HIDDEN_THOUGHTS_BUDGET
        )
    return fragment


def _google_thinking_3_fragment(
    canonical: dict[str, Any], family: str, ctx: ProcessorContext
) -> dict[str, Any]:
    fragment: dict[str, Any] = {}
    thinking_level: str | None = None
    include_thoughts: bool | None = None

    effort = _explicit_effort(canonical)
    if effort:
        default_map = D.GOOGLE_3_EFFORT_TO_LEVEL.get(
            family, D.GOOGLE_3_EFFORT_TO_LEVEL[D.GOOGLE_3_DEFAULT_FAMILY]
        )
        thinking_level = effort_lookup(ctx.table("level_map", default_map), effort)

    reasoning_summary = canonical.get("reasoning_summary")
    if reasoning_summary:
        include_thoughts = ctx.table(
            "summary_to_include", D.GOOGLE_3_SUMMARY_TO_INCLUDE
        ).get(reasoning_summary)

    # House "none" (ai_041): send nothing — no thinking_level, and the raw
    # thinking_budget fallback must not resurrect one.
    if effort != "none" and thinking_level is None and canonical.get("thinking_budget") is not None:
        thinking_level = ctx.from_number(int(canonical["thinking_budget"]), D.GOOGLE_3_FROM_NUMBER)

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
# Together/Z.AI reasoning. NOT SET SENDS NOTHING (settings-translation law: an
# unset key carries a value only when a cell DECLARES it, with a why — here
# ``processor_config.default_effort``). The old hidden "high" for unset (V2
# verifier, live 6f26a08b) is gone: a live probe 2026-10-04 (Kimi-K3 on
# Together, "17*23") answered with the field omitted at the same reasoning
# depth as "high" (23-25 vs 29-48 reasoning tokens), so omission is neither
# refused nor the costly "max" the old comment assumed. "none" (which
# canonicalize also produces from disable_reasoning=True)
# instead disables reasoning via the nested reasoning.enabled=false switch —
# a DIFFERENT provider key, which is why this is a processor and not a scalar
# value_map rule (a value_map can only land values on ONE provider_key).
#
# Reads canonical: reasoning_effort (+_converted; a budget-converted
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
    if effort is None:
        # NOT SET: only a cell-declared default rides (processor_config.default_effort).
        sent = ctx.config.get("default_effort")
    else:
        # A set effort short of an explicit deep ask maps to "high".
        sent = ctx.table("effort_map", D.TOGETHER_EFFORT_MAP).get(
            effort, ctx.table("set_effort_fallback", D.TOGETHER_SET_EFFORT_FALLBACK)
        )
    sent = ctx.reconcile_accepted(sent)  # K6 accepts (only when declared)
    if sent is not None:
        params["reasoning_effort"] = sent
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

# The aspect -> (w, h) table, anchor edge and rounding multiple are declared
# defaults (translation_defaults.MEDIA_*); processor_config["aspect_table"] /
# ["anchor_edge"] / ["dimension_multiple"] override them per rule.


def _anchored_wh(a: int, b: int, ctx: ProcessorContext | None) -> tuple[int, int]:
    edge = int(ctx.table("anchor_edge", D.MEDIA_ANCHOR_SHORT_EDGE)) if ctx else D.MEDIA_ANCHOR_SHORT_EDGE
    multiple = (
        int(ctx.table("dimension_multiple", D.MEDIA_DIMENSION_MULTIPLE))
        if ctx
        else D.MEDIA_DIMENSION_MULTIPLE
    )
    if a >= b:
        return (round(edge * a / b / multiple) * multiple, edge)
    return (edge, round(edge * b / a / multiple) * multiple)


def _derive_wh_table(
    canonical: dict[str, Any], ctx: ProcessorContext | None = None
) -> tuple[int | None, int | None]:
    """Port of _media_dims.derive_wh: explicit width+height wins, else the
    aspect table, else parse "A:B" anchored on the short edge (rounded to the
    multiple), else (None, None)."""
    width, height = canonical.get("width"), canonical.get("height")
    if width and height:
        return int(width), int(height)
    aspect = canonical.get("aspect_ratio")
    if aspect:
        table = ctx.table("aspect_table", D.MEDIA_ASPECT_TO_WH) if ctx else D.MEDIA_ASPECT_TO_WH
        wh = table.get(aspect)
        if wh:
            return (int(wh[0]), int(wh[1]))
        try:
            a, b = (int(x) for x in str(aspect).split(":", 1))
            return _anchored_wh(a, b, ctx)
        except (ValueError, TypeError):
            return (None, None)
    return (None, None)


def _derive_wh_anchor1024(
    canonical: dict[str, Any], ctx: ProcessorContext | None = None
) -> tuple[int, int]:
    """Port of TogetherImageGeneration._derive_wh: NO table — every ratio is
    computed off the anchor short edge; unparseable/missing ratios fall back to
    the declared fallback ratio (1:1)."""
    fa, fb = D.MEDIA_ANCHOR_FALLBACK_RATIO
    aspect = canonical.get("aspect_ratio") or f"{fa}:{fb}"
    try:
        a, b = (int(x) for x in str(aspect).split(":", 1))
    except (ValueError, TypeError):
        a, b = fa, fb
    return _anchored_wh(a, b, ctx)


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
        width, height = _derive_wh_table(canonical, ctx)
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
            width, height = _derive_wh_anchor1024(canonical, ctx)
        else:
            width, height = _derive_wh_table(canonical, ctx)
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
        # NOT SET means not set: no shape asked for → no size (Sora's own default).
        asked = [canonical.get("aspect_ratio"), canonical.get("resolution")]
        if not any(asked) and not (canonical.get("width") or canonical.get("height")):
            return params
        width, height = _derive_wh_table(canonical, ctx)
        if width and height:
            params[target] = f"{width}x{height}"
            return params
        default_resolution = ctx.table("default_resolution", D.SORA_DEFAULT_RESOLUTION)
        aspect = canonical.get("aspect_ratio") or ctx.table("default_aspect", D.SORA_DEFAULT_ASPECT)
        resolution = (canonical.get("resolution") or default_resolution).lower()
        landscape = aspect in ctx.table("landscape_aspects", D.SORA_LANDSCAPE_ASPECTS)
        sizes = ctx.table("sizes", D.SORA_SIZES)
        pair = sizes.get(resolution) or sizes[default_resolution]
        params[target] = pair[0] if landscape else pair[1]
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
    if raw is None:
        # NOT SET means not set: only a DECLARED default is sent for an empty count.
        raw = ctx.config.get("default")
        if raw is None:
            return params
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
    params["moderation"] = canonical.get("moderation") or ctx.config.get(
        "default", D.OPENAI_IMAGE_DEFAULT_MODERATION
    )
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
    params["safety_tolerance"] = (
        ctx.table("with_image_input", D.FLUX_SAFETY_TOLERANCE_WITH_IMAGE_INPUT)
        if (ctx.extra or {}).get("has_image_input")
        else ctx.table("default", ctx.table("tolerance", D.FLUX_SAFETY_TOLERANCE))
    )
    return params


@register_processor("xai_image_resolution")
def xai_image_resolution(
    canonical: dict[str, Any], params: dict[str, Any], ctx: ProcessorContext
) -> dict[str, Any]:
    """xai-sdk resolution: "1k"/"2k" pass; else width>=2048 -> "2k", any other
    width -> "1k", nothing -> omitted. Port of xai_image_api._build_kwargs."""
    resolution = canonical.get("resolution")
    if resolution in ctx.table("native_resolutions", D.XAI_NATIVE_RESOLUTIONS):
        params["resolution"] = resolution
        return params
    width = canonical.get("width")
    if width and int(width) >= int(ctx.table("width_threshold", D.XAI_WIDTH_THRESHOLD)):
        params["resolution"] = ctx.table("high_resolution", D.XAI_HIGH_RESOLUTION)
    elif width:
        params["resolution"] = ctx.table("low_resolution", D.XAI_LOW_RESOLUTION)
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
        mapped = ctx.table("resolution_map", D.IMAGEN_RESOLUTION_TO_SIZE).get(resolution)
        if mapped:
            params["image_size"] = mapped
            return params
    width = canonical.get("width")
    if width:
        try:
            params["image_size"] = (
                ctx.table("high_size", D.IMAGEN_HIGH_SIZE)
                if int(width) >= int(ctx.table("width_threshold", D.IMAGEN_WIDTH_THRESHOLD))
                else ctx.table("low_size", D.IMAGEN_LOW_SIZE)
            )
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
