"""The pure logic of an AI-visibility panel — no DB, no HTTP, no LLM.

The engine that asks ChatGPT/Claude/Gemini/Perplexity a question and persists
the answer already exists and is not rebuilt (D12). This module owns what a
*panel* adds on top, all of it pure so it is trivially testable and identical on
the server and in a preview:

1. **What a question is** — :class:`PanelPrompt`, a buyer question plus the flat
   cell fields a design run stamps on it (set, lane eligibility, prompted state,
   band…). A hand-typed question with none of them is still valid and reads as
   ``transformation='human_written'`` — an *unclassified* question.
2. **Which questions run this wave** — :func:`select_prompts` is set-aware: the
   tracked set, tripwires, false-positive checks and the prompted set run EVERY
   wave; only the discovery set (and unclassified questions) rotates,
   oldest-measured first. A budget smaller than the fixed sets is a *partial
   wave* with its shortfall named, never a silent cut.
3. **In what order** — :func:`plan_wave` lays questions × lanes × repeats out in
   a seeded random order, so the order is reproducible from the recorded seed.
4. **What a wave costs before it runs** — :func:`estimate_panel_cost`, questions
   × eligible engines per lane × repeats, priced by the design module's T10
   (``ai_visibility_design.allocate_and_price``) from the org's measured history.

Metrics over the answers live in ``ai_visibility_design`` (T12); the pooled
"named in X%" trend that used to live here is gone — it pooled prompted and
unprompted questions and every engine into one denominator.

🚨 **NULL IS UNMEASURED, NEVER ZERO.** A question nothing has answered yet has no
rate. It does not have a rate of 0%.

``ai_visibility_design`` imports this module at load time, so this module only
imports it lazily (inside functions) — a top-level import would be circular.
"""

from __future__ import annotations

import random
import re
from collections.abc import Sequence
from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

#: What one prompt on one engine costs when we have no measured history for this
#: org yet. DataForSEO's AI-answer endpoints are billed per live request; this is
#: the conservative side of what our own runs have reported, and it is only ever
#: a FALLBACK — a measured average always wins. The live value is the platform knob
#: ``seo.ai_visibility.fallback_cost_per_call_usd``; this is its default.
FALLBACK_COST_PER_PROMPT_ENGINE = Decimal("0.02")

#: Default of the platform knob ``seo.ai_visibility.max_key_messages``.
MAX_KEY_MESSAGES = 20

#: The sets that run in EVERY wave (contract partition codes). Order = the order a
#: partial wave fills its budget in: the tracked set first, the prompted set last.
FIXED_PARTITIONS: tuple[str, ...] = ("core", "sentinel", "control", "aided")
#: The discovery set — the only classified set that rotates.
ROTATING_PARTITION = "rotating"
#: Lanes the DataForSEO runner can execute. The real-app and campaign lanes have
#: no API runner; a question eligible only for those is skipped with a notice.
RUNNABLE_LANES: tuple[str, ...] = ("retrieval", "closed_model")
#: How an unclassified (hand-typed) question reads.
LEGACY_TRANSFORMATION = "human_written"


def max_prompts_per_panel(tier: str | None, tiers: dict[str, Any] | None = None) -> int:
    """How many questions a panel of this tier may hold, from the T10 tier table.

    = (unprompted slots + matched control slots, upper bounds) × variants per
    slot (upper bound). An unknown or empty tier reads as ``diagnostic``.
    ``tiers`` is the ``tiers`` knob (``DesignKnobs.tiers``); None = the default table.
    """
    from .ai_visibility_design import TIERS

    table = tiers or TIERS
    spec = table.get(tier or "diagnostic") or table["diagnostic"]
    slots = spec.unaided_slots[1] + (spec.control_slots[1] if spec.control_slots else 0)
    return slots * spec.variants[1]


class PanelPrompt(BaseModel):
    """One buyer question, in the user's words or a design run's. Never inferred
    from a keyword.

    Every cell field is optional: a legacy hand-typed prompt (``key``, ``text``,
    ``intent`` only) stays valid and reads as an unclassified question
    (:attr:`is_classified` False, :attr:`effective_transformation`
    ``'human_written'``). Enum-valued fields are checked against the design
    module's ``ENUMS`` so the codes have one home.
    """

    model_config = ConfigDict(extra="forbid")

    key: str
    text: str = Field(min_length=3)
    #: Free text: "comparison", "how-to", "brand". Ordering/labelling only.
    intent: str | None = None
    # --- flat cell fields (BUILD-CONTRACT "Data"), all optional ---
    candidate_id: str | None = None
    canonical_cell_id: str | None = None
    proximity_band: str | None = None
    aided_status: str | None = None
    campaign_exposed: bool | None = None
    partition: str | None = None
    lane_eligibility: list[str] | None = None
    variant_role: str | None = None
    locale: str | None = None
    persona_id: str | None = None
    job_id: str | None = None
    evidence_grade: str | None = None
    transformation: str | None = None

    @field_validator(
        "proximity_band", "aided_status", "partition", "evidence_grade", "transformation"
    )
    @classmethod
    def _enum_code(cls, value: str | None, info: Any) -> str | None:
        if value is None:
            return None
        from .ai_visibility_design import ENUMS

        allowed = ENUMS.get(info.field_name)
        if allowed and value not in allowed:
            raise ValueError(f"{info.field_name} must be one of {sorted(allowed)}, got {value!r}")
        return value

    @field_validator("lane_eligibility")
    @classmethod
    def _lanes(cls, value: list[str] | None) -> list[str] | None:
        if value is None:
            return None
        from .ai_visibility_design import ENUMS

        bad = [lane for lane in value if lane not in ENUMS["lane"]]
        if bad:
            raise ValueError(f"lane_eligibility has unknown lanes {bad}")
        return list(dict.fromkeys(value))

    @property
    def is_classified(self) -> bool:
        """True once a design run placed this question in a cell and a set."""
        return bool(self.canonical_cell_id and self.partition)

    @property
    def effective_transformation(self) -> str:
        return self.transformation or LEGACY_TRANSFORMATION

    @property
    def slot_id(self) -> str:
        """The question's slot for metrics: its cell, else its own key."""
        return self.canonical_cell_id or f"unclassified:{self.key}"


class KeyMessage(BaseModel):
    """A thing we want assistants to be SAYING about us.

    Detection is deterministic term matching over the answer text — free,
    instant, and explainable to the person who wrote the message. An LLM judging
    "is this message present?" would cost money per answer to produce a verdict
    nobody could audit.
    """

    model_config = ConfigDict(extra="forbid")

    key: str
    label: str
    #: Any one of these appearing counts as present. Matched case-insensitively
    #: on word boundaries, so "no code" does not fire inside "no coder".
    terms: list[str] = Field(min_length=1)


def _term_pattern(term: str) -> re.Pattern[str]:
    return re.compile(rf"(?<!\w){re.escape(term.strip())}(?!\w)", re.IGNORECASE)


class MessagePresence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str
    label: str
    present: bool
    #: The exact terms that fired — the evidence, so a user can see WHY we said
    #: their message landed.
    matched_terms: list[str] = Field(default_factory=list)


def message_presence(answer_text: str, messages: list[KeyMessage]) -> list[MessagePresence]:
    """Which of our key messages this one answer actually carried."""
    text = answer_text or ""
    results: list[MessagePresence] = []
    for message in messages:
        matched = [
            term for term in message.terms if term.strip() and _term_pattern(term).search(text)
        ]
        results.append(
            MessagePresence(
                key=message.key,
                label=message.label,
                present=bool(matched),
                matched_terms=matched,
            )
        )
    return results


class PanelCostEstimate(BaseModel):
    """What one wave will cost, and how confident that number is."""

    model_config = ConfigDict(extra="forbid")

    prompts: int
    engines: int
    lanes: list[str] = Field(default_factory=list)
    repeats: int = 1
    #: Provider answer calls: Σ questions × eligible engines per lane × repeats.
    calls: int
    calls_by_lane: dict[str, int] = Field(default_factory=dict)
    calls_by_engine: dict[str, int] = Field(default_factory=dict)
    #: Decision-analyst calls, per the ``analyst_sampling`` knob.
    analyst_calls: int = 0
    cost_per_call_usd: Decimal
    answer_cost_usd: Decimal = Decimal(0)
    analyst_cost_usd: Decimal = Decimal(0)
    #: Answers + analyst — the number a person is agreeing to spend.
    estimated_cost_usd: Decimal
    #: True when the per-call price came from this org's own completed runs.
    #: False means the declared fallback — say so in the UI rather than
    #: presenting a guess as a measurement.
    measured: bool
    basis: str
    notices: list[str] = Field(default_factory=list)


def _eligible_lanes(prompt: PanelPrompt, lanes: Sequence[str]) -> list[str]:
    allowed = prompt.lane_eligibility
    return [lane for lane in dict.fromkeys(lanes) if allowed is None or lane in allowed]


def estimate_panel_cost(
    *,
    prompts: Sequence[PanelPrompt],
    engines: Sequence[str],
    lanes: Sequence[str] = ("retrieval",),
    repeats: int = 1,
    measured_cost_per_call: Decimal | None = None,
    analyst_sampling: str = "first_repeat",
    analyst_cost_per_call: Decimal | None = None,
    fallback_cost_per_call: Decimal = FALLBACK_COST_PER_PROMPT_ENGINE,
) -> PanelCostEstimate:
    """The price of ONE wave, lane- and repeat-aware — delegated to T10.

    Pricing is ``ai_visibility_design.allocate_and_price`` (Σ questions ×
    eligible engines per lane × repeats × the measured per-call cost, plus
    analyst calls per ``analyst_sampling``). T10 needs a set for every question;
    an unclassified question is priced as a discovery-set question, which only
    affects set allocation (ignored here), never the price.
    """
    from .ai_visibility_design import DesignKnobs, PricedCandidate, allocate_and_price

    engine_list = list(dict.fromkeys(engines))
    lane_list = [lane for lane in dict.fromkeys(lanes) if lane in RUNNABLE_LANES]
    repeats = max(1, int(repeats))
    notices: list[str] = []
    skipped_lanes = sorted(set(lanes) - set(RUNNABLE_LANES))
    if skipped_lanes:
        notices.append(f"lanes with no API runner are not priced or run: {skipped_lanes}")
    priced: list[PricedCandidate] = []
    for prompt in prompts:
        eligible = _eligible_lanes(prompt, lane_list)
        if not eligible:
            continue
        priced.append(
            PricedCandidate(
                candidate_id=prompt.candidate_id or prompt.key,
                partition=prompt.partition or ROTATING_PARTITION,  # type: ignore[arg-type]
                lane_eligibility=eligible,  # type: ignore[arg-type]
            )
        )
    knobs = DesignKnobs(
        engines=engine_list,
        lanes=lane_list or ["retrieval"],  # type: ignore[list-item]
        repeats_per_wave=repeats,
        analyst_sampling=analyst_sampling,  # type: ignore[arg-type]
        fallback_cost_per_call_usd=fallback_cost_per_call,
    )
    result = allocate_and_price(
        {},
        priced,
        knobs=knobs,
        measured_cost_per_call=measured_cost_per_call,
        analyst_cost_per_call=analyst_cost_per_call,
    ).price
    return PanelCostEstimate(
        prompts=len(prompts),
        engines=len(engine_list),
        lanes=lane_list,
        repeats=repeats,
        calls=result.calls,
        calls_by_lane=result.calls_by_lane,
        calls_by_engine=result.calls_by_engine,
        analyst_calls=result.analyst_calls,
        cost_per_call_usd=result.cost_per_call_usd,
        answer_cost_usd=result.answer_cost_usd,
        analyst_cost_usd=result.analyst_cost_usd,
        estimated_cost_usd=result.total_usd,
        measured=result.measured,
        basis=result.basis,
        notices=notices + list(result.notices),
    )


class PromptSchedule(BaseModel):
    model_config = ConfigDict(extra="forbid")

    running: list[PanelPrompt] = Field(default_factory=list)
    #: Not run this wave, in order. Reported out loud — a cap that silently
    #: drops prompts reads as "we measured everything" when it did not.
    deferred: list[PanelPrompt] = Field(default_factory=list)
    #: Questions in the every-wave sets (tracked, tripwire, false-positive
    #: check, prompted).
    fixed_total: int = 0
    #: True when the budget could not hold every every-wave question.
    partial: bool = False
    #: How many every-wave questions did not fit. 0 on a full wave.
    shortfall: int = 0
    #: One plain sentence naming the shortfall; None on a full wave.
    shortfall_detail: str | None = None


def _oldest_first(prompts: Sequence[PanelPrompt], seen: dict[str, datetime]) -> list[PanelPrompt]:
    return sorted(
        prompts,
        key=lambda p: (
            seen.get(p.key) is not None,
            seen.get(p.key) or datetime.min,
            p.key,
        ),
    )


def select_prompts(
    prompts: list[PanelPrompt],
    *,
    max_per_run: int,
    last_measured: dict[str, datetime] | None = None,
) -> PromptSchedule:
    """Which questions run this wave — set-aware.

    * The tracked set (``core``), tripwires (``sentinel``), false-positive checks
      (``control``) and the prompted set (``aided``) run EVERY wave.
    * Only the discovery set (``rotating``) — and unclassified hand-typed
      questions — rotate, never-measured first, then oldest-measured first, so a
      big panel covers itself over a few waves instead of leaving its tail dark.
    * A budget below the every-wave sets returns a PARTIAL wave: as many
      every-wave questions as fit (tracked first, oldest-measured first inside
      each set), with ``partial``/``shortfall``/``shortfall_detail`` saying so.
    """
    seen = last_measured or {}
    cap = max(0, max_per_run)
    fixed: list[PanelPrompt] = []
    for partition in FIXED_PARTITIONS:
        fixed.extend(_oldest_first([p for p in prompts if p.partition == partition], seen))
    rotating = _oldest_first([p for p in prompts if p.partition not in FIXED_PARTITIONS], seen)
    if len(fixed) > cap:
        shortfall = len(fixed) - cap
        return PromptSchedule(
            running=fixed[:cap],
            deferred=fixed[cap:] + rotating,
            fixed_total=len(fixed),
            partial=True,
            shortfall=shortfall,
            shortfall_detail=(
                f"This wave is partial: the budget of {cap} question(s) is below the "
                f"{len(fixed)} that must run every wave, so {shortfall} of them and all "
                f"{len(rotating)} discovery question(s) wait for the next wave."
            ),
        )
    room = cap - len(fixed)
    return PromptSchedule(
        running=fixed + rotating[:room],
        deferred=rotating[room:],
        fixed_total=len(fixed),
    )


class WaveCell(BaseModel):
    """One unit of a wave: a question on one lane, one repeat. Every engine in
    the panel answers it together (the engines run concurrently)."""

    model_config = ConfigDict(extra="forbid")

    prompt_key: str
    lane: str
    repeat_index: int
    #: Position in the seeded order (0-based).
    position: int


class WavePlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    order_seed: int
    cells: list[WaveCell] = Field(default_factory=list)
    #: Questions skipped because none of their eligible lanes can run here.
    skipped: list[str] = Field(default_factory=list)
    notices: list[str] = Field(default_factory=list)


def plan_wave(
    prompts: Sequence[PanelPrompt],
    *,
    lanes: Sequence[str],
    repeats: int,
    order_seed: int,
) -> WavePlan:
    """Questions × eligible lanes × repeats, shuffled by ``order_seed``.

    The same inputs and seed always give the same order, so a wave's order is
    reproducible from the seed recorded on its response rows.
    """
    runnable = [lane for lane in dict.fromkeys(lanes) if lane in RUNNABLE_LANES]
    notices: list[str] = []
    dropped = sorted(set(lanes) - set(RUNNABLE_LANES))
    if dropped:
        notices.append(f"lanes with no API runner were not run: {dropped}")
    units: list[tuple[str, str, int]] = []
    skipped: list[str] = []
    for prompt in prompts:
        eligible = _eligible_lanes(prompt, runnable)
        if not eligible:
            skipped.append(prompt.key)
            continue
        for lane in eligible:
            for repeat_index in range(max(1, int(repeats))):
                units.append((prompt.key, lane, repeat_index))
    if skipped:
        notices.append(
            f"{len(skipped)} question(s) are eligible for no lane this panel runs and were skipped"
        )
    units.sort()
    random.Random(order_seed).shuffle(units)
    return WavePlan(
        order_seed=order_seed,
        cells=[
            WaveCell(prompt_key=key, lane=lane, repeat_index=r, position=i)
            for i, (key, lane, r) in enumerate(units)
        ],
        skipped=skipped,
        notices=notices,
    )


__all__ = [
    "FALLBACK_COST_PER_PROMPT_ENGINE",
    "FIXED_PARTITIONS",
    "LEGACY_TRANSFORMATION",
    "MAX_KEY_MESSAGES",
    "ROTATING_PARTITION",
    "RUNNABLE_LANES",
    "KeyMessage",
    "MessagePresence",
    "PanelCostEstimate",
    "PanelPrompt",
    "PromptSchedule",
    "WaveCell",
    "WavePlan",
    "estimate_panel_cost",
    "max_prompts_per_panel",
    "message_presence",
    "plan_wave",
    "select_prompts",
]
