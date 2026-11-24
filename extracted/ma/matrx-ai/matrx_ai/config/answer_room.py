"""THINKING NEVER TAKES THE ANSWER'S ROOM — the reserved share of an output limit, for every provider.

Why this exists
---------------
Every thinking model we route to counts its thinking INSIDE the call's output limit (Anthropic
``max_tokens``, OpenAI ``max_output_tokens``, Gemini ``maxOutputTokens``, every OpenAI-compatible
``max_tokens``). At a modest limit a model can therefore think until the limit and leave the
visible answer starved or empty. Live 2026-11-04 (Claude Haiku 5.5, limit 1,500, effort low):
requests 9d19883a and ca6660d2 spent 1,247 and 1,467 of their 1,500 tokens thinking, and the
person got a cut-off story. The reasoning-off retry (``orchestrator/executor.py::
_turn_reasoning_off_for_retry``) only fires when NO text arrived, so a starved answer slipped by.

The rule
--------
A call that will think keeps ``reserve`` = ceil(share x the authored limit) tokens that thinking can
never take (``share`` is the knob ``agents.output_room.answer_reserve_share``):

* **The provider caps thinking with a number** (Anthropic budget-mode ``thinking.budget_tokens`` —
  Claude Haiku 4.5 / Sonnet 4.5; Gemini 2.5 ``thinking_budget``; a scalar
  ``thinking_config.thinking_budget``): the budget is lowered so ``limit - budget >= reserve``. When
  the provider's smallest budget cannot fit, the limit is raised to ``floor + reserve`` instead.
* **The provider has no separate cap** (adaptive Claude 4.6+ / 5.x incl. Haiku 5.5, Gemini 3
  ``thinking_level``, OpenAI / xAI / Groq / Cerebras / Moonshot / Together ``reasoning_effort``):
  the limit is raised to ``authored + reserve`` — thinking keeps the room it had, and the answer
  gets the reserve on top — within the model's real output maximum.

A call that does not think (no reasoning control on the offering, or reasoning off on the wire) is
never touched: a small prose limit there is the author's cost knob (law 6). Raising a ceiling is
free (tokens are billed when generated); the send boundary still bounds a raise by an open
per-call spend cap. Every change is announced by the caller (``send_boundary``).

What the call WILL carry is read from the catalog's own outbound pass
(``providers.outbound_params.preview_outbound_params``) — the same translation the provider call
runs — so this module never guesses a provider's shape from a model name.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

#: The knob: the share of the authored output limit thinking may never take.
ANSWER_RESERVE_FEATURE = "agents.output_room"
ANSWER_RESERVE_KEY = "answer_reserve_share"
#: KNOB MIRROR of platform.feature_knob agents.output_room.answer_reserve_share (seeded 2026-11-04).
ANSWER_RESERVE_SHARE_MIRROR = 0.5

#: Anthropic rejects budget_tokens below this (also ``translation_defaults``); a rule may declare
#: its own ``min_budget_tokens`` / ``min_thinking_budget``.
_DEFAULT_BUDGET_FLOOR = 1024


def answer_reserve_share() -> float:
    """The live knob value, clamped into 0..1 (0 switches the reserve off)."""
    from matrx_ai.knobs import package_knob_number

    return package_knob_number(  # KNOB MIRROR agents.output_room.answer_reserve_share
        ANSWER_RESERVE_FEATURE, ANSWER_RESERVE_KEY, ANSWER_RESERVE_SHARE_MIRROR, low=0.0, high=1.0
    )


@dataclass(frozen=True)
class ThinkingShape:
    """What thinking a call will carry on the wire."""

    thinks: bool
    #: The numeric thinking cap on the wire, or None (no cap sent).
    budget: int | None = None
    #: True when the provider accepts a numeric cap for this model (``config.thinking_budget``).
    cappable: bool = False
    #: The smallest budget the provider accepts.
    floor: int = _DEFAULT_BUDGET_FLOOR
    #: One phrase naming the shape, for the announcement.
    label: str = ""


@dataclass(frozen=True)
class AnswerRoom:
    """The decision: what to send instead of the authored values."""

    authored_max: int
    reserve: int
    sent_max: int
    sent_budget: int | None
    shape: ThinkingShape
    reason: str


def _lookup(params: dict[str, Any], dotted: str | None) -> Any:
    """``params[dotted]``, or the nested path, or the same inside ``extra_body``."""
    if not dotted:
        return None
    for container in (params, params.get("extra_body") if isinstance(params.get("extra_body"), dict) else None):
        if not isinstance(container, dict):
            continue
        if dotted in container:
            return container[dotted]
        node: Any = container
        for part in dotted.split("."):
            if not isinstance(node, dict) or part not in node:
                node = None
                break
            node = node[part]
        if node is not None:
            return node
    return None


def _live_rule(controls: Any, key: str) -> Any:
    rule = (getattr(controls, "rules", None) or {}).get(key)
    if rule is None or getattr(rule, "drop", None) is True or getattr(rule, "supported", True) is False:
        return None
    return rule


def _is_off(value: Any) -> bool:
    return value in ("none", "disabled", "false", False, 0) or (isinstance(value, dict) and value.get("enabled") is False)


def thinking_shape(params: dict[str, Any], controls: Any) -> ThinkingShape:
    """Classify the wire params a call will carry. Provider-agnostic: read off the offering's own
    reasoning rule (``reasoning_effort`` / ``thinking_budget`` / ``thinking_level``)."""
    rule = _live_rule(controls, "reasoning_effort")
    key = "reasoning_effort"
    if rule is None:
        for alt in ("thinking_budget", "thinking_level"):
            rule = _live_rule(controls, alt)
            if rule is not None:
                key = alt
                break
    if rule is None:
        return ThinkingShape(thinks=False, label="no reasoning control")
    processor = getattr(rule, "processor", None)
    cfg = dict(getattr(rule, "processor_config", None) or {})

    if processor == "anthropic_thinking":
        thinking = params.get("thinking") if isinstance(params.get("thinking"), dict) else {}
        kind = thinking.get("type")
        floor = int(cfg.get("min_budget_tokens") or _DEFAULT_BUDGET_FLOOR)
        if kind == "enabled" and isinstance(thinking.get("budget_tokens"), int):
            return ThinkingShape(True, int(thinking["budget_tokens"]), True, floor, "Anthropic budget_tokens")
        if kind == "adaptive":
            return ThinkingShape(True, label="Anthropic adaptive thinking (no separate budget)")
        if kind is None and (cfg.get("thinking_always_on") or cfg.get("thinks_by_default")):
            return ThinkingShape(True, label="Anthropic adaptive thinking by default (no separate budget)")
        return ThinkingShape(False, label="Anthropic thinking off")

    if processor == "google_thinking":
        fragment = params.get(cfg.get("target", "thinking_config"))
        fragment = fragment if isinstance(fragment, dict) else {}
        if cfg.get("mode") == "legacy":
            budget = fragment.get("thinking_budget")
            floor = int(cfg.get("min_thinking_budget") or 1)
            if budget == 0:
                return ThinkingShape(False, label="Gemini thinking_budget 0")
            if isinstance(budget, int) and budget > 0:
                return ThinkingShape(True, budget, True, floor, "Gemini thinking_budget")
            # Unset or -1: Gemini 2.5 thinks dynamically, uncapped — but a number is accepted.
            return ThinkingShape(True, None, True, floor, "Gemini dynamic thinking")
        return ThinkingShape(True, label="Gemini thinking_level (no separate budget)")

    if processor == "together_reasoning":
        switch = _lookup(params, getattr(rule, "provider_key", None))
        if _is_off(params.get("reasoning")) or params.get("reasoning_effort") == "none" or _is_off(switch):
            return ThinkingShape(False, label="reasoning disabled")
        return ThinkingShape(True, label="reasoning_effort (no separate budget)")

    # Scalar rule: read the value it lands on the wire.
    provider_key = getattr(rule, "provider_key", None) or key
    value = _lookup(params, provider_key)
    if key == "thinking_budget" or provider_key.endswith("thinking_budget"):
        if value == 0:
            return ThinkingShape(False, label="thinking_budget 0")
        floor = int(cfg.get("min_thinking_budget") or 1)
        return ThinkingShape(
            True, int(value) if isinstance(value, int) and value > 0 else None, True, floor, "thinking_budget"
        )
    if _is_off(value):
        return ThinkingShape(False, label=f"{provider_key} off")
    return ThinkingShape(True, label=f"{provider_key} (no separate budget)")


def plan_answer_room(
    *,
    authored_max: int,
    shape: ThinkingShape,
    share: float,
    model_max: int | None,
) -> AnswerRoom | None:
    """The decision for one call, or None when the answer already has its reserve."""
    if not shape.thinks or authored_max <= 0 or share <= 0:
        return None
    reserve = max(1, math.ceil(share * authored_max))
    ceiling = model_max if model_max and model_max > 0 else None

    def fit(tokens: int) -> int:
        return min(tokens, ceiling) if ceiling is not None else tokens

    if shape.cappable:
        if shape.budget is not None and authored_max - shape.budget >= reserve:
            return None
        budget = authored_max - reserve
        if budget >= shape.floor:
            return AnswerRoom(
                authored_max, reserve, authored_max, budget, shape,
                f"thinking budget {'capped at' if shape.budget is not None else 'set to'} {budget:,} "
                f"({shape.label}{f', was {shape.budget:,}' if shape.budget is not None else ', was dynamic'}) "
                f"so {reserve:,} of the {authored_max:,}-token limit stay for the answer",
            )
        sent = fit(shape.floor + reserve)
        budget = sent - reserve
        if budget < shape.floor or sent <= authored_max:
            return None  # the model's ceiling leaves no room for both; the retry is the last resort
        return AnswerRoom(
            authored_max, reserve, sent, budget, shape,
            f"output limit raised {authored_max:,} -> {sent:,} with the thinking budget at the provider's "
            f"minimum {budget:,} ({shape.label}) so {reserve:,} tokens stay for the answer",
        )

    sent = fit(authored_max + reserve)
    if sent <= authored_max:
        return None
    return AnswerRoom(
        authored_max, reserve, sent, None, shape,
        f"output limit raised {authored_max:,} -> {sent:,}: {shape.label} counts thinking inside the limit, "
        f"so {sent - authored_max:,} tokens were added for the answer",
    )


__all__ = [
    "ANSWER_RESERVE_FEATURE",
    "ANSWER_RESERVE_KEY",
    "ANSWER_RESERVE_SHARE_MIRROR",
    "AnswerRoom",
    "ThinkingShape",
    "answer_reserve_share",
    "plan_answer_room",
    "thinking_shape",
]
