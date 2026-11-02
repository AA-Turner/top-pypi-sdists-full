from __future__ import annotations
from datetime import datetime
from enum import StrEnum
from typing import List, Optional

from pydantic import BaseModel, Field

from ...utils.types.identifier import StrObjectId


class InferredAttributionStatus(StrEnum):
    """Lifecycle of the estimation on a contact point."""
    WEIGHTED = "weighted"     # split across candidates; no human decision yet
    CONFIRMED = "confirmed"   # a human picked a concrete ad (or a graduated template did)
    REJECTED = "rejected"     # a human said "none of these"


class MetaBacking(StrEnum):
    """What Meta's conversation receipt said about this chat. Absent ≠ unattributed:
    PENDING means the receipt never arrived (we may not have replied); UNATTRIBUTED
    means the receipt arrived and did NOT attribute the conversation to an ad — which
    is 'Meta couldn't track it', not 'it was not an ad' (web-surface clicks and
    deferred sends break the receipt the same way they break the referral)."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    UNATTRIBUTED = "unattributed"


class InferredBasis(StrEnum):
    """Evidence backing the attribution, accumulated in order of arrival."""
    TEMPLATE = "template"
    REFERRAL_CONVERSION = "referral_conversion"
    HUMAN = "human"


class AdCandidate(BaseModel):
    """One candidate ad for a template match, with its share at the time the chat arrived."""
    source_id: StrObjectId
    ad_id: str = Field(default="")
    weight: float = Field(ge=0.0, le=1.0)
    n: int = Field(default=0, description="labeled chats observed for this ad in the window")


class InferredAttribution(BaseModel):
    """Estimation layer of a contact point's origin. The hard attribution stays in
    ``source_id``/``source_checker_method``; this sub-document carries the candidates,
    their FROZEN weights (computed once, when the chat arrived — never recomputed), the
    evidence (``basis``/``meta_backing``), and the audit trail to reverse any move
    (``previous_source_id``) or dedupe Meta's receipt (``conversation_id``)."""
    status: InferredAttributionStatus = Field(default=InferredAttributionStatus.WEIGHTED)
    basis: List[InferredBasis] = Field(default_factory=list)
    meta_backing: MetaBacking = Field(default=MetaBacking.PENDING)
    candidates: List[AdCandidate] = Field(default_factory=list)
    window_days: int = Field(default=30)
    computed_at: Optional[datetime] = Field(default=None)
    conversation_id: Optional[str] = Field(default=None)
    template_hash: Optional[str] = Field(default=None)
    previous_source_id: Optional[StrObjectId] = Field(default=None)
    decided_by: Optional[StrObjectId] = Field(default=None)
    decided_at: Optional[datetime] = Field(default=None)
