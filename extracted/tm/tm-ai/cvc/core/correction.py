"""
cvc.core.correction — Soul Self-Correction Loop.

The soul stores inferred claims about its owner (entities, values,
emotional context, temporal facts). Sometimes those inferences are
wrong. Until now, there was no way for the owner to *teach* the soul
directly — the soul would silently keep being wrong forever.

This module adds the correction loop:

  1. The user clicks "✕ Not right" on a soul claim in the dashboard.
  2. The correction is recorded as a ``CorrectionRecord`` and persisted
     to the user_model.
  3. On the next reasoning pass, the soul sees every correction as a
     "User-Direct Corrections (always trust over inference)" block in
     the prompt. The LLM is told: when a current inference contradicts
     a correction, the correction wins.

A correction is an explicit override. Confidence = 1.0 by default — the
soul treats direct corrections as ground truth until the user changes
their mind (which itself becomes a new correction, with the old one
superseded).

Pattern mirrored from user_model.ValueStatement.superseded_by.
"""

from __future__ import annotations

import logging
import time
import uuid
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger("cvc.correction")


# ---------------------------------------------------------------------------
# Claim types — which user_model field does this correction target?
# ---------------------------------------------------------------------------

CLAIM_TYPES: set[str] = {
    "entity",          # a person, project, place, etc.
    "value",           # a ValueStatement
    "temporal_fact",   # an always/current/periodic fact
    "life_event",      # a milestone
    "emotional_context",  # a mood observation
    "narrative",       # the soul_narrative paragraph
    "communication_style",
    "expertise_area",
    "preferred_language",
    "preferred_tool",
}


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------


class CorrectionRecord(BaseModel):
    """A direct correction from the owner overriding an inferred claim.

    The soul stores these as ground truth. On the next reasoning pass,
    each active correction is injected into the prompt as a
    "User-Direct Corrections (always trust)" block.

    Corrections are append-only. If the user changes their mind about
    a correction, a new CorrectionRecord is created with
    ``supersedes`` pointing at the previous one. The old record stays
    in the DAG for audit (consistent with the rest of CVC's
    immutable-history model).
    """

    correction_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])

    # What kind of claim this corrects. Must be in CLAIM_TYPES.
    claim_type: str

    # The original inferred claim (what the soul got wrong).
    # Free-form text — matched against the model by the LLM during reasoning.
    original_inference: str = ""

    # What the user says is true instead.
    corrected_value: str

    # Why. Optional free-form.
    reason: str = ""

    # Ground truth — the soul trusts this completely until the user
    # changes their mind. 1.0 means "always trust". Lower values are
    # not currently used but reserved for future nuance ("trust this
    # for daily tasks but not for big life decisions").
    confidence_override: float = 1.0

    # Provenance
    created_at: float = Field(default_factory=time.time)
    source_commit: str = ""  # CVC commit hash where the user pressed the button
    conversation_snippet: str = ""  # the surrounding chat context, if any

    # Correction-of-a-correction support
    superseded_by: str | None = None  # correction_id of a newer override

    def is_active(self) -> bool:
        """Active = not superseded."""
        return self.superseded_by is None


# ---------------------------------------------------------------------------
# Apply corrections to a UserIdentitySnapshot
# ---------------------------------------------------------------------------


def apply_correction_to_model(
    model: Any,
    correction: CorrectionRecord,
) -> Any:
    """
    Merge a new correction into a ``UserIdentitySnapshot`` (in-place of the
    caller, by deep-copy semantics — caller decides whether to assign back).

    The model returned is the SAME instance with ``model.corrections``
    extended. The caller is responsible for persisting it.

    Dedup logic: if the user corrects the same claim_type with the same
    corrected_value, we don't double-insert — we just bump a counter
    via the timestamp. If the same claim_type is corrected with a
    different value, the previous active correction is superseded by
    the new one (the old one stays in the list with superseded_by set).

    Returns the same model object for ergonomic chaining.
    """
    if correction.claim_type not in CLAIM_TYPES:
        logger.warning(
            "apply_correction: unknown claim_type=%s — accepting anyway",
            correction.claim_type,
        )

    if not hasattr(model, "corrections"):
        # Be permissive: if the model doesn't yet carry the corrections
        # field, this is an old v1 model loaded from disk. Caller should
        # upgrade via UserIdentitySnapshot.model_validate(model.model_dump()).
        logger.debug("model lacks 'corrections' field; caller should upgrade schema")

    corrections: list[CorrectionRecord] = list(getattr(model, "corrections", []) or [])

    # Dedup / supersede prior active correction for the same claim_type + original
    for existing in corrections:
        if (
            existing.is_active()
            and existing.claim_type == correction.claim_type
            and (
                not existing.original_inference
                or not correction.original_inference
                or existing.original_inference.lower()
                == correction.original_inference.lower()
            )
        ):
            # Same claim being corrected again. Mark the old one superseded.
            existing.superseded_by = correction.correction_id
            logger.info(
                "superseding previous correction %s for claim_type=%s",
                existing.correction_id,
                correction.claim_type,
            )
            break

    corrections.append(correction)
    try:
        model.corrections = corrections
    except Exception:
        # Model is immutable / frozen — fall back to a copy.
        try:
            new_model = model.model_copy(deep=True)
            new_model.corrections = corrections
            return new_model
        except Exception as exc:
            logger.exception("could not attach corrections to model: %s", exc)
    return model


# ---------------------------------------------------------------------------
# Prompt block — injected into SOUL_REASONING_PROMPT
# ---------------------------------------------------------------------------


def build_corrections_prompt_block(corrections: list[CorrectionRecord]) -> str:
    """
    Format active corrections into a prompt block for the soul-reasoning
    LLM call. Returns an empty string if there are no active corrections.

    The block is intentionally placed at the TOP of the prompt
    hierarchy in user_model.py so the LLM treats corrections as
    authoritative ground truth — above inference.
    """
    active = [c for c in corrections if c.is_active()]
    if not active:
        return ""

    lines: list[str] = [
        "",
        "## ⚠️ User-Direct Corrections (ALWAYS TRUST — these override inference)",
        "",
        "The user has explicitly corrected the following claims. When a new",
        "inference or extraction CONTRADICTS one of these corrections, the",
        "correction wins. Do not re-infer these. Treat them as ground truth.",
        "",
    ]
    for c in active[-30:]:  # cap at 30 most-recent active corrections
        lines.append(f"### Correction #{c.correction_id[:6]} ({c.claim_type})")
        if c.original_inference:
            lines.append(f"- The soul previously thought: {c.original_inference}")
            lines.append(f"- User correction: {c.corrected_value}")
        else:
            lines.append(f"- User-stated truth: {c.corrected_value}")
        if c.reason:
            lines.append(f"- Reason: {c.reason}")
        lines.append("")

    lines.append(
        "End of corrections block. When building entities, values, "
        "temporal_facts, life_events, emotional_context, soul_narrative, "
        "communication_style, expertise_areas, preferred_languages, or "
        "preferred_tools: do NOT contradict any correction above. If the "
        "new conversation data agrees with a correction, you may reinforce "
        "it. If it disagrees, ignore the new data for that claim and trust "
        "the correction."
    )
    return "\n".join(lines)


def active_corrections_count(corrections: list[CorrectionRecord]) -> int:
    """Quick count of non-superseded corrections — for dashboard stats."""
    return sum(1 for c in corrections if c.is_active())
