"""The `data` of the kinds the live core emits itself: the two control events, `entity.*` and `access.changed`.

The producers' kinds are typed beside: `samples.py` (`samples.*`), `runs.py` (`run.*`), `documents.py` (notes and
summary pages); `kinds.py` names each kind's model.
"""

from __future__ import annotations

import json
from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator, BaseModel, Field

from ..compat import StrEnum

#: An `entity.*` notice's summary: a few scalar facts of the audit row, never another entity's id or free text.
MAX_SUMMARY_BYTES = 1024
MAX_EVENT_TYPE_CHARS = 64

Scalar = str | int | float | bool | None


def check_summary(value: dict[str, Scalar]) -> dict[str, Scalar]:
    if len(json.dumps(value, separators=(",", ":"), ensure_ascii=False).encode("utf-8")) > MAX_SUMMARY_BYTES:
        raise ValueError("an entity summary is over 1 KiB")
    return value


Summary = Annotated[dict[str, Scalar], AfterValidator(check_summary)]


class ResyncReason(StrEnum):
    """Why a stream says "re-read state": events after the client's cursor can no longer all be sent.

    A client treats a reason it does not know like any other: re-read, then follow on.
    """

    CURSOR_EXPIRED = "cursor_expired"  # an event after the cursor was published over 24 h ago
    CURSOR_UNKNOWN = "cursor_unknown"  # the cursor is past the head (another server's, or made up)
    TOO_SLOW = "too_slow"  # still behind after a replay from the table


class ResyncData(BaseModel):
    """`resync`: re-read whatever you follow through the read routes, then carry on from this event's `seq`."""

    reason: ResyncReason


class LaggedData(BaseModel):
    """`lagged`: the stream fell over 1,000 events behind; it now replays from the table, then goes live again."""

    #: Published events between what was delivered and the head, when it fell back.
    behind: int = Field(ge=0)


class EntityData(BaseModel):
    """`entity.<audit type>`: the audit log's row (`record_event`) as a notice. Read the subject's route for more."""

    #: The audit `EventType` (`run.status_changed`); the kind repeats it after `entity.`.
    event_type: str = Field(min_length=1, max_length=MAX_EVENT_TYPE_CHARS)
    #: The audit `EventSubject` (`run`, `project`, `team`, ...).
    subject_type: str | None = Field(default=None, max_length=MAX_EVENT_TYPE_CHARS)
    subject_id: UUID | None = None
    summary: Summary = Field(default_factory=dict)


class AccessTarget(StrEnum):
    """What changed who may read what. Streams re-resolve what they may deliver on every one."""

    PROJECT = "project"  # a project's access settings (refs.project names it)
    WORKSPACE = "workspace"  # a workspace's access settings (no ids: a team event)
    MEMBER = "member"  # a member's role, or an access group's members (no ids: a team event)


class AccessChangedData(BaseModel):
    """`access.changed`."""

    target: AccessTarget
