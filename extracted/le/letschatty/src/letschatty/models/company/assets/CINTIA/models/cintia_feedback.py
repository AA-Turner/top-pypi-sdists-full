"""Feedback model for CINTIA executions."""

from datetime import datetime
from enum import IntEnum, StrEnum
from typing import Any

from pydantic import BaseModel, Field


class CintiaFeedbackRating(IntEnum):
    NEGATIVE = -1
    POSITIVE = 1


# Categorical reason vocabulary for negative feedback. Frontend renders Spanish
# labels; backend stores the codes. Add new codes via a deploy on both sides.
# Tagger-specific codes (``tagger_missed_required`` / ``tagger_added_extra``)
# are reused alongside the responder codes — the FE picks the right subset
# per cintia_type when rendering the reason picker.
NEGATIVE_FEEDBACK_REASON_CODES: frozenset[str] = frozenset(
    {
        "outdated_info",
        "wrong_info",
        "bad_format",
        "too_robotic",
        "too_long",
        "too_short",
        "wrong_tone",
        "off_topic",
        "hallucination",
        "missed_context",
        "wrong_language",
        "other",
        # Tagger-specific
        "tagger_missed_required",
        "tagger_added_extra",
    }
)


class CintiaFeedback(BaseModel):
    """Feedback on a CINTIA execution — rating, reason, comment, author, and optional output override.

    ``created_by`` is the raw user_id string from the JWT — no name/avatar
    snapshot. Frontend resolves display info via the existing users
    collection if it needs to render a chip.
    """

    rating: CintiaFeedbackRating | None = None
    reason_code: str | None = None
    comment: str | None = None
    decision_output_override: dict[str, Any] | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str | None = None


class CintiaCorrectionStatus(StrEnum):
    SUGGESTED = "suggested"
    APPROVED = "approved"
    REJECTED = "rejected"


class CintiaCorrection(BaseModel):
    """Agent-authored correction of a CINTIA execution's response.

    Last write wins — only the latest correction is stored on the execution.
    The `suggested_response` mirrors the responder's message-list shape so it
    can be replayed/used as a training signal later. Submissions from users
    with approver permissions land directly as APPROVED; others land as
    SUGGESTED and need to be reviewed.

    Two correction shapes are supported:
    - **Free-text**: human writes the messages directly in
      ``suggested_response`` (each item ``{type: "text", content: {body}}``
      or other supported message types).
    - **Fast-answer-backed**: human picks a business-approved FA by id; the
      cintia-reader resolves the FA body fresh on read and injects composed
      messages with ``context.response_id`` so the FE renders the FA badge
      per bubble. Optional ``pre_fast_answer_message`` /
      ``post_fast_answer_message`` wrap the FA body — same convention as
      pgp-implementator-responder-with-fast-answers' decision_output. When
      ``fast_answer_id`` is set, ``suggested_response`` may be empty (the
      reader composes the messages on the fly).

    ``chain_of_thought`` is the human's reasoning for why the original AI
    response was wrong — captured as a training signal alongside the
    corrected messages. Distinct from the AI's ``decision_output.output.
    chain_of_thought`` which represents the AI's (wrong) reasoning.
    """

    correction_id: str
    suggested_response: list[dict[str, Any]] = Field(default_factory=list)
    status: CintiaCorrectionStatus = CintiaCorrectionStatus.SUGGESTED
    chain_of_thought: str | None = None
    fast_answer_id: str | None = None
    pre_fast_answer_message: str | None = None
    post_fast_answer_message: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str
    reviewed_at: datetime | None = None
    reviewed_by: str | None = None
    rejection_reason: str | None = None
