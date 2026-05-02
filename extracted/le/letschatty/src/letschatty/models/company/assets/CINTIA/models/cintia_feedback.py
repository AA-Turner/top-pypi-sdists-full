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
    """

    correction_id: str
    suggested_response: list[dict[str, Any]] = Field(default_factory=list)
    status: CintiaCorrectionStatus = CintiaCorrectionStatus.SUGGESTED
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str
    reviewed_at: datetime | None = None
    reviewed_by: str | None = None
    rejection_reason: str | None = None
