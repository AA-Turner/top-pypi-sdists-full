from __future__ import annotations

from typing import Literal, TypedDict


class JustificationSpan(TypedDict):
    """One span the justification rests on, with what that span shows."""

    spanId: str
    text: str


Justification = list[JustificationSpan]

ApprovalState = Literal["pending", "approved", "rejected"]


class Approver(TypedDict):
    id: str
    fullName: str | None
    email: str | None
    imageUrl: str | None


Assignee = Approver


class ApprovalFields(TypedDict):
    """Read-only on this client: only a person in Bitfab sets these."""

    approvalState: ApprovalState
    approvedBy: Approver | None
    approvedAt: str | None
