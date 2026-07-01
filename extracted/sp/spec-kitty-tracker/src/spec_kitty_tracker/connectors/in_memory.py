"""In-memory connector for spec-kitty-tracker.

Test and reference implementation of TaskTrackerConnector. Not backed by
any external provider. Used for unit tests and reference flows.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from uuid import uuid4

from spec_kitty_tracker.capabilities import TrackerCapabilities
from spec_kitty_tracker.errors import IssueNotFoundError
from spec_kitty_tracker.models import (
    CanonicalIssue,
    CanonicalLink,
    CanonicalStatus,
    ExternalRef,
    Page,
    SyncCheckpoint,
    TrackerEvent,
    TrackerEventType,
    utcnow,
)


class InMemoryConnector:
    def __init__(self, *, name: str, workspace: str) -> None:
        self.name = name
        self.workspace = workspace
        self._issues: dict[str, CanonicalIssue] = {}
        self._events: list[TrackerEvent] = []

    async def get_capabilities(self) -> TrackerCapabilities:
        return TrackerCapabilities(
            supports_webhooks=False,
            supports_comments=True,
            supports_hierarchy=True,
            supports_dependencies=True,
            supports_custom_fields=True,
            supports_multi_assignee=True,
            supports_sprints_or_cycles=True,
            supports_bulk_read=True,
            supports_bulk_write=True,
            supports_delete=True,
        )

    async def list_issues(
        self,
        *,
        updated_since: Any,
        cursor: str | None,
        limit: int,
        filters: Mapping[str, Any] | None,
    ) -> Page[CanonicalIssue]:
        del filters
        issues = sorted(self._issues.values(), key=lambda issue: issue.ref.identity)
        if updated_since is not None:
            issues = [
                issue
                for issue in issues
                if issue.updated_at is not None and issue.updated_at >= updated_since
            ]

        start = int(cursor) if cursor is not None else 0
        end = start + limit
        sliced = issues[start:end]
        next_cursor = str(end) if end < len(issues) else None
        return Page(items=[issue.clone() for issue in sliced], next_cursor=next_cursor)

    async def get_issue(self, ref: ExternalRef) -> CanonicalIssue:
        issue = self._issues.get(ref.identity)
        if issue is None:
            raise IssueNotFoundError(f"Issue not found: {ref.identity}")
        return issue.clone()

    async def create_issue(self, issue: CanonicalIssue) -> CanonicalIssue:
        created = issue.clone()
        now = utcnow()
        created.created_at = created.created_at or now
        created.updated_at = now
        self._issues[created.ref.identity] = created
        self._append_event(TrackerEventType.CREATED, created.ref, {"title": created.title})
        return created.clone()

    async def update_issue(
        self,
        ref: ExternalRef,
        patch: Mapping[str, Any],
        *,
        idempotency_key: str | None,
    ) -> CanonicalIssue:
        del idempotency_key
        existing = self._issues.get(ref.identity)
        if existing is None:
            raise IssueNotFoundError(f"Issue not found: {ref.identity}")

        updated = existing.clone()
        for key, value in patch.items():
            if not hasattr(updated, key):
                continue
            setattr(updated, key, value)
        updated.updated_at = utcnow()
        self._issues[ref.identity] = updated
        self._append_event(TrackerEventType.UPDATED, ref, {"patch": dict(patch)})
        return updated.clone()

    async def transition_issue(
        self,
        ref: ExternalRef,
        target_status: CanonicalStatus,
    ) -> CanonicalIssue:
        updated = await self.update_issue(
            ref,
            {"status": target_status},
            idempotency_key=f"transition:{ref.identity}:{target_status}",
        )
        self._append_event(
            TrackerEventType.TRANSITIONED,
            ref,
            {"status": target_status.value},
        )
        return updated

    async def upsert_link(self, ref: ExternalRef, link: CanonicalLink) -> None:
        existing = self._issues.get(ref.identity)
        if existing is None:
            raise IssueNotFoundError(f"Issue not found: {ref.identity}")

        updated = existing.clone()
        if link not in updated.links:
            updated.links.append(link)
            updated.updated_at = utcnow()
            self._issues[ref.identity] = updated
        self._append_event(
            TrackerEventType.LINK_UPSERTED,
            ref,
            {"type": link.type.value, "target": link.target.identity},
        )

    async def add_comment(self, ref: ExternalRef, body: str) -> None:
        issue = self._issues.get(ref.identity)
        if issue is None:
            raise IssueNotFoundError(f"Issue not found: {ref.identity}")
        comments = issue.custom_fields.setdefault("comments", [])
        if not isinstance(comments, list):
            comments = []
            issue.custom_fields["comments"] = comments
        comments.append(body)
        issue.updated_at = utcnow()
        self._append_event(TrackerEventType.COMMENT_ADDED, ref, {"body": body})

    async def list_events(
        self,
        cursor: SyncCheckpoint | None,
        limit: int,
    ) -> tuple[list[TrackerEvent], SyncCheckpoint | None]:
        start = 0
        if cursor is not None and cursor.cursor is not None:
            start = int(cursor.cursor)
        end = start + limit
        events = self._events[start:end]
        next_cursor = str(end) if end < len(self._events) else None
        return events, SyncCheckpoint(cursor=next_cursor)

    def _append_event(
        self,
        event_type: TrackerEventType,
        ref: ExternalRef,
        payload: dict[str, Any],
    ) -> None:
        self._events.append(
            TrackerEvent(
                event_id=str(uuid4()),
                event_type=event_type,
                issue_ref=ref,
                timestamp=utcnow(),
                payload=payload,
            )
        )
