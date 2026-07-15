"""
cvc.core.world_model — From Data Model to World Model (Fable5 Phase 3).

The user_model V2 stores WHAT the soul knows (entities, values, facts,
events). This module adds HOW the owner thinks — the generating function
behind their decisions. The difference:

  Data model:  "What did the owner say about X?"
  World model: "What WOULD the owner say about Y, which they never
                mentioned, given everything about how they think?"

Three capabilities, per FABLE5_SPACE_ROBOTICS_COGNITIVE_INTELLIGENCE.md §3.1:

  1. ValuesHierarchy — ranked, conflict-aware ordering of ValueStatements.
     Not just "user values directness" and "user values loyalty" as flat
     facts, but which one WINS when they collide, learned from observed
     resolutions in the DAG.

  2. ReasoningStyle — inferred from the *shape* of past decisions:
     top-down vs bottom-up, data-anchored vs precedent-anchored,
     fast-and-revise vs slow-and-commit.

  3. Uncertainty map — where the world model is weak or self-contradictory.
     Flagged as research targets for the counterfactual self-test loop
     (cvc.operations.counterfactual), never silently resolved.

Invariants honored: append-only (hierarchy revisions supersede, never
delete), local-first (persists inside .cvc/), provider-agnostic (any
adapter). Corrections (cvc.core.correction) always outrank inference.
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger("cvc.world_model")


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class ValueConflict(BaseModel):
    """An observed moment where two values collided and one won.

    These are the gold-standard signal for ranking: a value hierarchy
    inferred from stated importance is weak; one inferred from observed
    resolutions ("deadline pressure vs code quality — owner chose to
    ship behind a flag") is strong.
    """

    conflict_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    value_a: str  # value_id or statement text of first value
    value_b: str  # value_id or statement text of second value
    winner: str  # which one won ("a" | "b" | "synthesis")
    situation: str = ""  # short description of the collision
    resolution: str = ""  # how the owner actually resolved it
    source_commits: list[str] = Field(default_factory=list)
    observed_at: float = Field(default_factory=time.time)
    confidence: float = 0.5


class ValuesHierarchy(BaseModel):
    """A ranked ordering of the owner's values, with conflict evidence.

    Append-only: each revision gets a new revision_id and carries
    `supersedes` pointing at the prior revision. Never rewrite history —
    the owner's values DO change over a lifetime, and the trajectory of
    that change is itself soul data (it's how children understand who
    their parent was at 30 vs at 60).
    """

    revision_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    created_at: float = Field(default_factory=time.time)
    supersedes: str | None = None

    # value_id (or statement) -> rank (1 = highest). Ties allowed.
    ranking: dict[str, int] = Field(default_factory=dict)

    # Observed collisions backing this ranking.
    conflicts: list[ValueConflict] = Field(default_factory=list)

    # Context-dependence: some values dominate at work but not in life.
    # Maps context ("work" | "family" | "health" | ...) to ranking overrides.
    context_overrides: dict[str, dict[str, int]] = Field(default_factory=dict)

    narrative: str = ""  # one paragraph: "when push comes to shove, this owner..."


class ReasoningStyle(BaseModel):
    """The shape of how the owner thinks, inferred from decision traces.

    Every axis is a float in [-1.0, +1.0] with 0.0 = no signal yet.
    Confidence per axis tracks how much evidence backs the estimate.
    """

    revision_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    created_at: float = Field(default_factory=time.time)
    supersedes: str | None = None

    # -1.0 = pure bottom-up (details first), +1.0 = pure top-down (vision first)
    top_down_vs_bottom_up: float = 0.0
    # -1.0 = anchors on precedent/experience, +1.0 = anchors on fresh data
    data_vs_precedent: float = 0.0
    # -1.0 = slow-and-commit, +1.0 = fast-and-revise
    fast_revise_vs_slow_commit: float = 0.0
    # -1.0 = risk-averse, +1.0 = risk-seeking
    risk_posture: float = 0.0
    # -1.0 = consensus-seeking, +1.0 = unilateral decider
    decision_autonomy: float = 0.0

    confidence: dict[str, float] = Field(default_factory=dict)  # axis -> 0..1
    evidence_commits: list[str] = Field(default_factory=list)
    narrative: str = ""  # "This owner decides fast, revises publicly, anchors on..."


class UncertaintyFlag(BaseModel):
    """A place where the world model knows it is weak or contradictory.

    These are research targets for the counterfactual self-test loop —
    the soul should probe them, not paper over them.
    """

    flag_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    kind: str = "low_evidence"  # low_evidence | contradiction | stale | untested_extrapolation
    description: str = ""
    related_values: list[str] = Field(default_factory=list)
    related_entities: list[str] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)
    resolved: bool = False
    resolved_by: str = ""  # correction_id / probe_id / commit hash that resolved it


class WorldModelState(BaseModel):
    """Top-level persisted world model. One file, append-only revisions inside."""

    values_hierarchy: ValuesHierarchy | None = None
    hierarchy_history: list[str] = Field(default_factory=list)  # revision_ids, oldest first
    reasoning_style: ReasoningStyle | None = None
    style_history: list[str] = Field(default_factory=list)
    uncertainty_flags: list[UncertaintyFlag] = Field(default_factory=list)
    last_updated: float = Field(default_factory=time.time)


# ---------------------------------------------------------------------------
# Reasoning prompts
# ---------------------------------------------------------------------------

HIERARCHY_PROMPT = """\
You are the world-model engine of a digital soul. Your job is NOT to list \
the owner's values — that already exists. Your job is to determine which \
values WIN when they collide, based on observed evidence.

## Current Values (flat, from the soul model)
{values_json}

## Current Hierarchy (may be empty on first run)
{hierarchy_json}

## Owner Corrections (ALWAYS trust over inference)
{corrections_block}

## Recent Decision Evidence (from cognitive commits)
{decision_evidence}

## Instructions
1. Look for COLLISIONS: moments where two values pulled in opposite
   directions and the owner picked one (or synthesized). Example: "wanted
   to ship fast (speed) but wrote tests first anyway (quality)" → quality
   outranks speed under deadline pressure.
2. Rank the values. Rank 1 = wins most collisions. Ties allowed.
3. Note CONTEXT OVERRIDES: a value may dominate at work but lose in
   family contexts.
4. Flag UNCERTAINTY honestly: if two values have never collided in the
   evidence, say so — do NOT invent a ranking for them.

Respond with ONLY valid JSON:
{{
  "ranking": {{"<value statement or id>": 1, "...": 2}},
  "conflicts": [
    {{"value_a": "...", "value_b": "...", "winner": "a|b|synthesis",
      "situation": "...", "resolution": "...", "confidence": 0.0}}
  ],
  "context_overrides": {{"work": {{"<value>": 1}}}},
  "uncertainty_flags": [
    {{"kind": "low_evidence|contradiction", "description": "..."}}
  ],
  "narrative": "One paragraph: when push comes to shove, this owner..."
}}
"""

STYLE_PROMPT = """\
You are the world-model engine of a digital soul. Analyze the SHAPE of \
the owner's decisions — not what they decided, but HOW they decided.

## Current Style Estimate
{style_json}

## Owner Corrections (ALWAYS trust over inference)
{corrections_block}

## Recent Decision Traces (from cognitive commits)
{decision_evidence}

## Axes (score -1.0 to +1.0, 0.0 = no signal)
- top_down_vs_bottom_up: -1 = details-first builder, +1 = vision-first architect
- data_vs_precedent: -1 = leans on experience/precedent, +1 = wants fresh data
- fast_revise_vs_slow_commit: -1 = deliberates then commits, +1 = ships then iterates
- risk_posture: -1 = risk-averse, +1 = risk-seeking
- decision_autonomy: -1 = consensus-seeking, +1 = decides alone

## Instructions
Update each axis ONLY where the evidence moves it. Track per-axis
confidence (0-1). Cite which observations drove each change.

Respond with ONLY valid JSON:
{{
  "axes": {{"top_down_vs_bottom_up": 0.0, "data_vs_precedent": 0.0,
            "fast_revise_vs_slow_commit": 0.0, "risk_posture": 0.0,
            "decision_autonomy": 0.0}},
  "confidence": {{"top_down_vs_bottom_up": 0.0}},
  "narrative": "One paragraph describing how this owner thinks and decides."
}}
"""


# ---------------------------------------------------------------------------
# Manager
# ---------------------------------------------------------------------------


class WorldModelManager:
    """Builds and persists the world model. Sits beside UserModelManager.

    Persistence: ``<cvc_root>/world_model.json`` (canonical latest) plus
    append-only revision log at ``<cvc_root>/world_model_revisions.jsonl``.
    """

    WORLD_MODEL_FILE = "world_model.json"
    REVISIONS_FILE = "world_model_revisions.jsonl"

    def __init__(self, cvc_root: Path) -> None:
        self.cvc_root = Path(cvc_root)
        self._state_path = self.cvc_root / self.WORLD_MODEL_FILE
        self._revisions_path = self.cvc_root / self.REVISIONS_FILE

    # -- persistence --------------------------------------------------------

    def load_state(self) -> WorldModelState:
        if self._state_path.exists():
            try:
                data = json.loads(self._state_path.read_text(encoding="utf-8"))
                return WorldModelState.model_validate(data)
            except Exception as e:  # noqa: BLE001
                logger.warning("world_model: failed to load state: %s", e)
        return WorldModelState()

    def save_state(self, state: WorldModelState) -> Path:
        state.last_updated = time.time()
        self._state_path.write_text(state.model_dump_json(indent=2), encoding="utf-8")
        return self._state_path

    def _append_revision(self, kind: str, payload: dict[str, Any]) -> None:
        """Append-only revision log — never rewritten (Invariant #3)."""
        try:
            line = json.dumps({"kind": kind, "at": time.time(), **payload})
            with self._revisions_path.open("a", encoding="utf-8") as fh:
                fh.write(line + "\n")
        except Exception as e:  # noqa: BLE001
            logger.debug("world_model: revision append failed (non-fatal): %s", e)

    # -- prompt building ----------------------------------------------------

    def build_hierarchy_prompt(
        self,
        values: list[dict[str, Any]],
        decision_evidence: str,
        corrections_block: str = "(none)",
    ) -> str:
        state = self.load_state()
        hierarchy_json = (
            state.values_hierarchy.model_dump_json(indent=2)
            if state.values_hierarchy
            else "{}"
        )
        return HIERARCHY_PROMPT.format(
            values_json=json.dumps(values, indent=2, default=str),
            hierarchy_json=hierarchy_json,
            corrections_block=corrections_block,
            decision_evidence=decision_evidence[:12000],
        )

    def build_style_prompt(
        self,
        decision_evidence: str,
        corrections_block: str = "(none)",
    ) -> str:
        state = self.load_state()
        style_json = (
            state.reasoning_style.model_dump_json(indent=2)
            if state.reasoning_style
            else "{}"
        )
        return STYLE_PROMPT.format(
            style_json=style_json,
            corrections_block=corrections_block,
            decision_evidence=decision_evidence[:12000],
        )

    # -- response parsing ----------------------------------------------------

    @staticmethod
    def _extract_json(text: str) -> dict[str, Any] | None:
        """Tolerant JSON extraction (mirrors dreaming.py's approach)."""
        text = text.strip()
        if text.startswith("```"):
            # strip code fences
            lines = text.splitlines()
            lines = [l for l in lines if not l.strip().startswith("```")]
            text = "\n".join(lines)
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return None
        try:
            return json.loads(text[start : end + 1], strict=False)
        except Exception:  # noqa: BLE001
            return None

    def apply_hierarchy_response(self, response_text: str) -> ValuesHierarchy | None:
        data = self._extract_json(response_text)
        if not data or not isinstance(data.get("ranking"), dict):
            logger.warning("world_model: hierarchy response unparseable")
            return None

        state = self.load_state()
        prior = state.values_hierarchy

        conflicts = []
        for c in data.get("conflicts", []) or []:
            try:
                conflicts.append(ValueConflict.model_validate(c))
            except Exception:  # noqa: BLE001
                continue

        hierarchy = ValuesHierarchy(
            supersedes=prior.revision_id if prior else None,
            ranking={str(k): int(v) for k, v in data["ranking"].items()},
            conflicts=conflicts,
            context_overrides={
                str(ctx): {str(k): int(v) for k, v in override.items()}
                for ctx, override in (data.get("context_overrides") or {}).items()
                if isinstance(override, dict)
            },
            narrative=str(data.get("narrative", "")),
        )

        for f in data.get("uncertainty_flags", []) or []:
            try:
                state.uncertainty_flags.append(UncertaintyFlag.model_validate(f))
            except Exception:  # noqa: BLE001
                continue

        state.values_hierarchy = hierarchy
        state.hierarchy_history.append(hierarchy.revision_id)
        self.save_state(state)
        self._append_revision("values_hierarchy", hierarchy.model_dump())
        logger.info(
            "world_model: hierarchy revision %s (%d values, %d conflicts)",
            hierarchy.revision_id,
            len(hierarchy.ranking),
            len(hierarchy.conflicts),
        )
        return hierarchy

    def apply_style_response(self, response_text: str) -> ReasoningStyle | None:
        data = self._extract_json(response_text)
        if not data or not isinstance(data.get("axes"), dict):
            logger.warning("world_model: style response unparseable")
            return None

        state = self.load_state()
        prior = state.reasoning_style
        axes = data["axes"]

        def _clamp(v: Any) -> float:
            try:
                return max(-1.0, min(1.0, float(v)))
            except Exception:  # noqa: BLE001
                return 0.0

        style = ReasoningStyle(
            supersedes=prior.revision_id if prior else None,
            top_down_vs_bottom_up=_clamp(axes.get("top_down_vs_bottom_up", 0.0)),
            data_vs_precedent=_clamp(axes.get("data_vs_precedent", 0.0)),
            fast_revise_vs_slow_commit=_clamp(axes.get("fast_revise_vs_slow_commit", 0.0)),
            risk_posture=_clamp(axes.get("risk_posture", 0.0)),
            decision_autonomy=_clamp(axes.get("decision_autonomy", 0.0)),
            confidence={
                str(k): max(0.0, min(1.0, float(v)))
                for k, v in (data.get("confidence") or {}).items()
            },
            narrative=str(data.get("narrative", "")),
        )

        state.reasoning_style = style
        state.style_history.append(style.revision_id)
        self.save_state(state)
        self._append_revision("reasoning_style", style.model_dump())
        logger.info("world_model: style revision %s", style.revision_id)
        return style

    # -- injection ------------------------------------------------------------

    def get_world_model_injection(self) -> str:
        """Compact block for system-prompt injection alongside soul narrative.

        This is what lets a brand-new brain answer 'what would the owner
        do here?' instead of only 'what did the owner say once?'.
        """
        state = self.load_state()
        parts: list[str] = []

        if state.values_hierarchy and state.values_hierarchy.narrative:
            parts.append(f"VALUES (when they collide): {state.values_hierarchy.narrative}")
            top = sorted(state.values_hierarchy.ranking.items(), key=lambda kv: kv[1])[:5]
            if top:
                ranked = " > ".join(k for k, _ in top)
                parts.append(f"Priority order: {ranked}")

        if state.reasoning_style and state.reasoning_style.narrative:
            parts.append(f"HOW THEY THINK: {state.reasoning_style.narrative}")

        unresolved = [f for f in state.uncertainty_flags if not f.resolved]
        if unresolved:
            parts.append(
                "KNOWN UNCERTAINTY (do not fake confidence here): "
                + "; ".join(f.description for f in unresolved[:3])
            )

        return "\n".join(parts)

    # -- unresolved flags for the counterfactual loop -------------------------

    def get_probe_targets(self, limit: int = 5) -> list[UncertaintyFlag]:
        state = self.load_state()
        return [f for f in state.uncertainty_flags if not f.resolved][:limit]

    def resolve_flag(self, flag_id: str, resolved_by: str) -> bool:
        state = self.load_state()
        for f in state.uncertainty_flags:
            if f.flag_id == flag_id and not f.resolved:
                f.resolved = True
                f.resolved_by = resolved_by
                self.save_state(state)
                self._append_revision(
                    "flag_resolved", {"flag_id": flag_id, "resolved_by": resolved_by}
                )
                return True
        return False
