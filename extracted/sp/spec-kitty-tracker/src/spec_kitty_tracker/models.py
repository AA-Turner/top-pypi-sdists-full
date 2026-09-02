from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any, Generic, TypeVar


class CanonicalStatus(StrEnum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    BLOCKED = "blocked"
    DONE = "done"
    CANCELED = "canceled"


class CanonicalIssueType(StrEnum):
    EPIC = "epic"
    STORY = "story"
    TASK = "task"
    BUG = "bug"
    CHORE = "chore"
    SUBTASK = "subtask"


class LinkType(StrEnum):
    BLOCKS = "blocks"
    BLOCKED_BY = "blocked_by"
    RELATES_TO = "relates_to"
    DUPLICATES = "duplicates"
    PARENT_OF = "parent_of"
    CHILD_OF = "child_of"


class TrackerEventType(StrEnum):
    CREATED = "created"
    UPDATED = "updated"
    TRANSITIONED = "transitioned"
    COMMENT_ADDED = "comment_added"
    LINK_UPSERTED = "link_upserted"


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True, slots=True)
class ExternalRef:
    system: str
    workspace: str
    id: str
    key: str | None = None
    url: str | None = None

    def __post_init__(self) -> None:
        if not self.system.strip():
            raise ValueError("ExternalRef.system must not be empty")
        if not self.workspace.strip():
            raise ValueError("ExternalRef.workspace must not be empty")
        if not self.id.strip():
            raise ValueError("ExternalRef.id must not be empty")

    @property
    def identity(self) -> str:
        return f"{self.system}:{self.workspace}:{self.id}"


@dataclass(frozen=True, slots=True)
class CanonicalLink:
    type: LinkType
    target: ExternalRef


@dataclass(slots=True)
class CanonicalIssue:
    ref: ExternalRef
    title: str
    body: str | None
    status: CanonicalStatus
    issue_type: CanonicalIssueType
    priority: int | None = None
    assignees: list[str] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    parent: ExternalRef | None = None
    links: list[CanonicalLink] = field(default_factory=list)
    custom_fields: dict[str, Any] = field(default_factory=dict)
    created_at: datetime | None = None
    updated_at: datetime | None = None
    raw: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("CanonicalIssue.title must not be empty")
        if self.priority is not None and not (0 <= self.priority <= 4):
            raise ValueError("CanonicalIssue.priority must be in range 0..4")

    def clone(self) -> CanonicalIssue:
        return replace(
            self,
            assignees=list(self.assignees),
            labels=list(self.labels),
            links=list(self.links),
            custom_fields=dict(self.custom_fields),
            raw=dict(self.raw) if self.raw is not None else None,
        )


@dataclass(frozen=True, slots=True)
class TrackerEvent:
    event_id: str
    event_type: TrackerEventType
    issue_ref: ExternalRef
    timestamp: datetime
    payload: dict[str, Any]


T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class Page(Generic[T]):
    items: list[T]
    next_cursor: str | None = None


@dataclass(frozen=True, slots=True)
class SyncCheckpoint:
    cursor: str | None = None
    updated_since: datetime | None = None
