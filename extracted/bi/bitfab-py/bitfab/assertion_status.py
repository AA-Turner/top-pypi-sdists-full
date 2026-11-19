from __future__ import annotations

from typing import Any, Literal, TypedDict


class JustificationSpan(TypedDict):
    """One span the justification rests on, with what that span shows."""

    spanId: str
    text: str


Justification = list[JustificationSpan]

AssertionStatus = Literal["draft", "confirmed", "rejected"]
"""An assertion's status. Only ``confirmed`` assertions are checked on replay."""

ApprovalState = Literal["pending", "approved", "rejected"]
"""Deprecated: use ``AssertionStatus``. ``pending`` is ``draft`` and ``approved`` is ``confirmed``."""


class Confirmer(TypedDict):
    """The person who confirmed or rejected an assertion."""

    id: str
    fullName: str | None
    email: str | None
    imageUrl: str | None


Approver = Confirmer
"""Deprecated: use ``Confirmer``."""

Assignee = Confirmer


class StatusFields(TypedDict):
    """Read-only on this client: only a person in Bitfab sets these.

    ``status`` is ``draft``, ``confirmed``, or ``rejected``. ``confirmedBy``
    and ``confirmedAt`` say who set it and when, and are None on a draft.
    ``approvalState``, ``approvedBy``, and ``approvedAt`` are deprecated:
    read ``status``, ``confirmedBy``, and ``confirmedAt``. ``approvalState``
    carries the old values (``pending``, ``approved``, ``rejected``).
    """

    status: AssertionStatus
    confirmedBy: Confirmer | None
    confirmedAt: str | None
    approvalState: ApprovalState
    approvedBy: Confirmer | None
    approvedAt: str | None


ApprovalFields = StatusFields
"""Deprecated: use ``StatusFields``."""

_LEGACY_BY_STATUS: dict[str, str] = {
    "draft": "pending",
    "confirmed": "approved",
    "rejected": "rejected",
}
_STATUS_BY_LEGACY: dict[str, str] = {
    legacy: status for status, legacy in _LEGACY_BY_STATUS.items()
}


def with_status_fields(row: dict[str, Any]) -> dict[str, Any]:
    row = dict(row)
    if "status" not in row and "approvalState" in row:
        row["status"] = _STATUS_BY_LEGACY.get(
            row["approvalState"], row["approvalState"]
        )
        row["confirmedBy"] = row.get("approvedBy")
        row["confirmedAt"] = row.get("approvedAt")
    if "status" in row:
        row["approvalState"] = _LEGACY_BY_STATUS.get(row["status"], row["status"])
        row["approvedBy"] = row.get("confirmedBy")
        row["approvedAt"] = row.get("confirmedAt")
    return row
