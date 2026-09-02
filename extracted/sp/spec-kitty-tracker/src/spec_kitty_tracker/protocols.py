from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Protocol, runtime_checkable

from spec_kitty_tracker.capabilities import TrackerCapabilities
from spec_kitty_tracker.models import (
    CanonicalIssue,
    CanonicalLink,
    CanonicalStatus,
    ExternalRef,
    Page,
    SyncCheckpoint,
    TrackerEvent,
)

IssuePatch = Mapping[str, Any]


@runtime_checkable
class TaskTrackerConnector(Protocol):
    name: str

    async def get_capabilities(self) -> TrackerCapabilities: ...

    async def list_issues(
        self,
        *,
        updated_since: datetime | None,
        cursor: str | None,
        limit: int,
        filters: Mapping[str, Any] | None,
    ) -> Page[CanonicalIssue]: ...

    async def get_issue(self, ref: ExternalRef) -> CanonicalIssue: ...

    async def create_issue(self, issue: CanonicalIssue) -> CanonicalIssue: ...

    async def update_issue(
        self,
        ref: ExternalRef,
        patch: IssuePatch,
        *,
        idempotency_key: str | None,
    ) -> CanonicalIssue: ...

    async def transition_issue(
        self,
        ref: ExternalRef,
        target_status: CanonicalStatus,
    ) -> CanonicalIssue: ...

    async def upsert_link(self, ref: ExternalRef, link: CanonicalLink) -> None: ...

    async def add_comment(self, ref: ExternalRef, body: str) -> None: ...

    async def list_events(
        self,
        cursor: SyncCheckpoint | None,
        limit: int,
    ) -> tuple[list[TrackerEvent], SyncCheckpoint | None]: ...


@runtime_checkable
class LocalIssueStore(Protocol):
    async def list_issues(
        self,
        *,
        system: str | None = None,
    ) -> Sequence[CanonicalIssue]: ...

    async def get_issue(self, ref: ExternalRef) -> CanonicalIssue | None: ...

    async def upsert_issue(self, issue: CanonicalIssue) -> None: ...

    async def delete_issue(self, ref: ExternalRef) -> None: ...
