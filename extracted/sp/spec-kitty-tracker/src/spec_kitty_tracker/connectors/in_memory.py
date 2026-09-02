"""In-memory connector for spec-kitty-tracker.

Test and reference implementation of TaskTrackerConnector. Not backed by
any external provider. Used for unit tests and reference flows.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from uuid import uuid4

from spec_kitty_tracker.capabilities import TrackerCapabilities
from spec_kitty_tracker.errors import ConnectorRequestError, IssueNotFoundError
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
from spec_kitty_tracker.patch_contract import reject_unknown_patch_keys

# TRK-M1-06: content fields compared to tell a genuine concurrent-writer
# create race (a different record already at this identity) apart from an
# idempotent retry of the *same* create (e.g. the first attempt's write
# landed but its response was lost). ``ref``/``created_at``/``updated_at``/
# ``raw`` are excluded -- they are bookkeeping the connector itself stamps,
# not content a caller asserts.
_CREATE_CONTENT_FIELDS = (
    "title",
    "body",
    "status",
    "issue_type",
    "priority",
    "assignees",
    "labels",
    "parent",
    "links",
    "custom_fields",
)


def _same_create_content(existing: CanonicalIssue, incoming: CanonicalIssue) -> bool:
    return all(
        getattr(existing, field_name) == getattr(incoming, field_name)
        for field_name in _CREATE_CONTENT_FIELDS
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
            supports_assignment=True,
            supports_terminal_transition=True,
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
        # A12 (TRK-M1-03): cursor is an offset into the stable, unfiltered,
        # identity-sorted list; updated_since is applied as a per-page
        # filter on top of that window. This keeps cursor position
        # meaningful across a restored checkpoint whose updated_since
        # differs from the one an earlier, crashed pull used (N11/N12) --
        # composing the two independently, rather than re-filtering the
        # whole list by updated_since before indexing by cursor, which
        # would shift what a given cursor offset points at.
        all_issues = sorted(self._issues.values(), key=lambda issue: issue.ref.identity)

        # TRK-M1-06: a checkpoint is caller-owned state persisted and
        # restored outside the engine (e.g. to disk); a corrupted cursor
        # (e.g. truncated/garbled bytes on restore) must fail closed as a
        # typed, recorded SyncFailure -- never an uncaught crash and never
        # silently coerced into a guessed start position.
        if cursor is not None:
            try:
                start = int(cursor)
            except ValueError as exc:
                raise ConnectorRequestError(
                    f"malformed cursor: {cursor!r}",
                    status_code=400,
                    provider=self.name,
                ) from exc
            # TRK-M1-06 (Renata handback, attempt 1): a cursor that parses
            # cleanly but is negative is semantically invalid, not merely
            # "start at 0" -- Python's negative-index slicing would
            # otherwise silently wrap to the tail of the identity-sorted
            # list instead of raising, dropping issues with no recorded
            # failure. Fail closed the same way the non-numeric case does.
            if start < 0:
                raise ConnectorRequestError(
                    f"malformed cursor: {cursor!r}",
                    status_code=400,
                    provider=self.name,
                )
        else:
            start = 0
        end = start + limit
        window = all_issues[start:end]
        if updated_since is not None:
            window = [
                issue
                for issue in window
                if issue.updated_at is not None and issue.updated_at >= updated_since
            ]

        next_cursor = str(end) if end < len(all_issues) else None
        return Page(items=[issue.clone() for issue in window], next_cursor=next_cursor)

    async def get_issue(self, ref: ExternalRef) -> CanonicalIssue:
        issue = self._issues.get(ref.identity)
        if issue is None:
            raise IssueNotFoundError(f"Issue not found: {ref.identity}")
        return issue.clone()

    async def create_issue(self, issue: CanonicalIssue) -> CanonicalIssue:
        # TRK-M1-06: create-if-absent, not upsert. Two independent writers
        # that both believe they are first to create the same identity
        # must not silently clobber one another -- and a caller retrying
        # its own create (its write landed but the response was lost) must
        # see that retry succeed idempotently rather than be denied as a
        # conflict.
        existing = self._issues.get(issue.ref.identity)
        if existing is not None:
            if _same_create_content(existing, issue):
                return existing.clone()
            raise ConnectorRequestError(
                f"issue already exists with different content: {issue.ref.identity}",
                status_code=409,
                provider=self.name,
            )
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
        reject_unknown_patch_keys(patch, provider=self.name)
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
