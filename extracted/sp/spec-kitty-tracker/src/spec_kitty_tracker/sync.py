from __future__ import annotations

import dataclasses
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal

from spec_kitty_tracker.conflicts import ConflictRecord, ConflictStrategy, resolve_field
from spec_kitty_tracker.errors import (
    CapabilityNotSupportedError,
    ConnectorRequestError,
    FailureClass,
    SyncConflictError,
    TrackerContractError,
)
from spec_kitty_tracker.mission_sync import assert_no_forbidden_teamspace_legacy_keys
from spec_kitty_tracker.models import (
    CanonicalIssue,
    CanonicalStatus,
    ExternalRef,
    Page,
    SyncCheckpoint,
)
from spec_kitty_tracker.policy import CORE_ISSUE_FIELDS, OwnershipPolicy
from spec_kitty_tracker.protocols import LocalIssueStore, TaskTrackerConnector

# A11 (TRK-M1-03): terminal statuses that require the connector to honestly
# report supports_terminal_transition before the engine will patch them.
_TERMINAL_STATUSES = frozenset({CanonicalStatus.DONE, CanonicalStatus.CANCELED})

# Exceptions a per-issue push operation may raise that must not abort the
# rest of the run -- recorded as a SyncFailure instead (A11).
_NON_ABORTING_PUSH_EXCEPTIONS = (
    ConnectorRequestError,
    CapabilityNotSupportedError,
    TrackerContractError,
)

# TRK-M1-06: fields with an unambiguous "nothing asserted" value, used to
# detect an ownership violation on create -- title/body/status/issue_type
# are required (no meaningful empty state) and are deliberately excluded;
# creation authority for them is already governed by the existing
# local_can_write("title") gate above. Every other member of
# CORE_ISSUE_FIELDS is covered here (Renata handback, attempt 1: priority
# and parent were originally omitted despite sharing the same None empty
# default as the selection criterion names).
_CREATE_OWNERSHIP_EMPTY_DEFAULTS: dict[str, Any] = {
    "assignees": [],
    "labels": [],
    "links": [],
    "custom_fields": {},
    "priority": None,
    "parent": None,
}

SyncOperation = Literal[
    "pull_page",
    "create",
    "update",
    "link",
    "comment",
    "patch_field_denied",
]


@dataclass(slots=True)
class SyncStats:
    pulled_created: int = 0
    pulled_updated: int = 0
    pushed_created: int = 0
    pushed_updated: int = 0
    skipped: int = 0


@dataclass(frozen=True, slots=True)
class SyncFailure:
    """A10 (TRK-M1-03): a typed partial-failure record.

    Recorded instead of aborting the whole sync when one issue/page fails
    -- see A11 for the push/pull semantics that populate this.
    """

    issue_ref: ExternalRef | None
    operation: SyncOperation
    failure_class: FailureClass | None
    message: str
    retryable: bool

    def __str__(self) -> str:
        ref = self.issue_ref.identity if self.issue_ref is not None else "<none>"
        return f"{self.operation}[{ref}]: {self.message}"


@dataclass(slots=True)
class SyncResult:
    stats: SyncStats = field(default_factory=SyncStats)
    conflicts: list[ConflictRecord] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    # A10 (TRK-M1-03): typed partial-failure list. ``errors`` (existing
    # list[str]) is kept and populated with str(failure) for each entry --
    # a derived mirror for callers that have not migrated to ``failures``.
    failures: list[SyncFailure] = field(default_factory=list)


class SyncEngine:
    def __init__(
        self,
        *,
        connector: TaskTrackerConnector,
        store: LocalIssueStore,
        policy: OwnershipPolicy,
        strategy: ConflictStrategy = ConflictStrategy.NEWER_TIMESTAMP,
        strict_manual_review: bool = False,
        max_retry_attempts: int = 2,
    ) -> None:
        self.connector = connector
        self.store = store
        self.policy = policy
        self.strategy = strategy
        self.strict_manual_review = strict_manual_review
        self.max_retry_attempts = max_retry_attempts
        self._checkpoint = SyncCheckpoint()

    @property
    def checkpoint(self) -> SyncCheckpoint:
        return self._checkpoint

    def restore_checkpoint(self, checkpoint: SyncCheckpoint) -> None:
        """A12 (TRK-M1-03): publicly restore a persisted checkpoint so the
        next ``pull()`` resumes at ``checkpoint.cursor`` / filters by
        ``checkpoint.updated_since``, instead of a caller poking the
        private ``_checkpoint`` attribute."""
        self._checkpoint = checkpoint

    async def pull(
        self,
        *,
        limit: int = 100,
        filters: Mapping[str, Any] | None = None,
    ) -> SyncResult:
        result = SyncResult()
        # A12: resume at the currently restored checkpoint's cursor rather
        # than always starting from the beginning.
        cursor: str | None = self._checkpoint.cursor
        query_updated_since = self._checkpoint.updated_since
        max_updated_at = self._checkpoint.updated_since

        while True:
            try:
                page = await self._list_issues_with_retry(
                    updated_since=query_updated_since,
                    cursor=cursor,
                    limit=limit,
                    filters=filters,
                )
            except ConnectorRequestError as exc:
                # A11: a page failure stops the loop without advancing the
                # checkpoint past the last fully processed page.
                result.failures.append(
                    SyncFailure(
                        issue_ref=None,
                        operation="pull_page",
                        failure_class=exc.failure_class,
                        message=str(exc),
                        retryable=exc.is_retryable,
                    )
                )
                break

            for external_issue in self._dedupe_page_items(page.items):
                if external_issue.updated_at is not None and (
                    max_updated_at is None or external_issue.updated_at > max_updated_at
                ):
                    max_updated_at = external_issue.updated_at

                local_issue = await self.store.get_issue(external_issue.ref)
                if local_issue is None:
                    await self.store.upsert_issue(external_issue)
                    result.stats.pulled_created += 1
                    continue

                merged_issue, conflicts = self._merge_issues(
                    local_issue=local_issue,
                    external_issue=external_issue,
                )
                result.conflicts.extend(conflicts)
                await self.store.upsert_issue(merged_issue)
                if merged_issue != local_issue:
                    result.stats.pulled_updated += 1
                else:
                    result.stats.skipped += 1

            # A11/A12: advance the checkpoint after each page is fully
            # processed, so a later page's failure leaves the checkpoint at
            # exactly the last successfully processed page (cursor = the
            # provider cursor of the first unprocessed page; None when
            # complete).
            cursor = page.next_cursor
            self._checkpoint = SyncCheckpoint(cursor=cursor, updated_since=max_updated_at)
            if cursor is None:
                break

        result.errors = [str(failure) for failure in result.failures]
        self._enforce_conflict_policy(result.conflicts)
        return result

    async def _list_issues_with_retry(
        self,
        *,
        updated_since: datetime | None,
        cursor: str | None,
        limit: int,
        filters: Mapping[str, Any] | None,
    ) -> Page[CanonicalIssue]:
        attempt = 0
        while True:
            try:
                return await self.connector.list_issues(
                    updated_since=updated_since,
                    cursor=cursor,
                    limit=limit,
                    filters=filters,
                )
            except ConnectorRequestError as exc:
                if not exc.is_retryable or attempt >= self.max_retry_attempts:
                    raise
                attempt += 1

    @staticmethod
    def _dedupe_page_items(items: list[CanonicalIssue]) -> list[CanonicalIssue]:
        """N9: collapse duplicate items for the same issue within one page
        (duplicate/out-of-order delivery) to the one with the greatest
        ``updated_at``, so a duplicate never inflates sync stats."""
        by_identity: dict[str, CanonicalIssue] = {}
        order: list[str] = []
        for item in items:
            identity = item.ref.identity
            if identity not in by_identity:
                order.append(identity)
                by_identity[identity] = item
                continue
            existing = by_identity[identity]
            if item.updated_at is not None and (
                existing.updated_at is None or item.updated_at >= existing.updated_at
            ):
                by_identity[identity] = item
        return [by_identity[identity] for identity in order]

    async def push(
        self,
        *,
        limit: int = 200,
        filters: Mapping[str, Any] | None = None,
    ) -> SyncResult:
        result = SyncResult()
        remote_index = await self._collect_remote_index(limit=limit, filters=filters)
        local_issues = await self.store.list_issues(system=self.connector.name)
        capabilities = await self.connector.get_capabilities()

        for local_issue in local_issues:
            remote_issue = remote_index.get(local_issue.ref.identity)
            if remote_issue is None:
                if not self.policy.local_can_write("title"):
                    result.stats.skipped += 1
                    continue
                # TRK-M1-06: local must not originate a non-empty value for
                # a field it does not own, even when creating a brand-new
                # remote issue where there is no external value yet to
                # merge/resolve a conflict against -- ownership governs
                # authorship of a field's value, not only after-the-fact
                # conflict resolution.
                violated_field = self._ownership_violation_on_create(
                    policy=self.policy, issue=local_issue
                )
                if violated_field is not None:
                    result.failures.append(
                        SyncFailure(
                            issue_ref=local_issue.ref,
                            operation="create",
                            failure_class=None,
                            message=(
                                f"create denied: local does not own {violated_field!r} "
                                "and it is not empty"
                            ),
                            retryable=False,
                        )
                    )
                    continue
                # N2: a retired legacy key in custom_fields must never reach
                # create_issue -- reject before egress, not after.
                legacy_failure = self._legacy_key_failure(
                    issue_ref=local_issue.ref,
                    custom_fields=local_issue.custom_fields,
                    operation="create",
                )
                if legacy_failure is not None:
                    result.failures.append(legacy_failure)
                    continue
                # A11: a create failure is recorded, not fatal to the run.
                # TRK-M1-06: retried the same way update() already was --
                # a transient create failure (e.g. the write landed but
                # the response was lost) must get a bounded retry, not an
                # immediate, permanent give-up.
                try:
                    created = await self._create_issue_with_retry(local_issue)
                except _NON_ABORTING_PUSH_EXCEPTIONS as exc:
                    result.failures.append(
                        SyncFailure(
                            issue_ref=local_issue.ref,
                            operation="create",
                            failure_class=getattr(exc, "failure_class", None),
                            message=str(exc),
                            retryable=False,
                        )
                    )
                    continue
                await self.store.upsert_issue(created)
                result.stats.pushed_created += 1
                continue

            desired_remote, conflicts = self._merge_issues(
                local_issue=local_issue,
                external_issue=remote_issue,
            )
            result.conflicts.extend(conflicts)

            patch = self._build_patch(before=remote_issue, after=desired_remote)
            self._exclude_unsupported_fields(
                patch=patch,
                capabilities=capabilities,
                issue_ref=local_issue.ref,
                failures=result.failures,
            )
            if not patch:
                # TRK-M1-06: the merge may have resolved a genuine conflict
                # to a value the remote already holds (so there is nothing
                # left to push), but that resolution must still be
                # materialized in the LOCAL store -- otherwise local stays
                # permanently diverged from the resolution just computed,
                # and every subsequent push() re-discovers and re-reports
                # the identical conflict forever (an infinite conflict
                # loop for any caller that calls push() without an
                # interleaving pull()).
                if desired_remote != local_issue:
                    await self.store.upsert_issue(desired_remote)
                result.stats.skipped += 1
                continue

            # N2: a retired legacy key in the outgoing custom_fields patch
            # must never reach update_issue -- reject the whole patch
            # before egress, not after.
            if "custom_fields" in patch:
                legacy_failure = self._legacy_key_failure(
                    issue_ref=local_issue.ref,
                    custom_fields=patch["custom_fields"],
                    operation="update",
                )
                if legacy_failure is not None:
                    result.failures.append(legacy_failure)
                    continue

            # A11: an update failure is recorded for this issue only; the
            # rest of the run continues.
            try:
                updated_remote = await self._update_issue_with_retry(
                    ref=local_issue.ref,
                    patch=patch,
                    idempotency_key=self._idempotency_key(local_issue.ref),
                )
            except _NON_ABORTING_PUSH_EXCEPTIONS as exc:
                result.failures.append(
                    SyncFailure(
                        issue_ref=local_issue.ref,
                        operation="update",
                        failure_class=getattr(exc, "failure_class", None),
                        message=str(exc),
                        retryable=False,
                    )
                )
                continue

            merged_local, post_conflicts = self._merge_issues(
                local_issue=local_issue,
                external_issue=updated_remote,
            )
            result.conflicts.extend(post_conflicts)
            await self.store.upsert_issue(merged_local)
            result.stats.pushed_updated += 1

        result.errors = [str(failure) for failure in result.failures]
        self._enforce_conflict_policy(result.conflicts)
        return result

    @staticmethod
    def _ownership_violation_on_create(
        *,
        policy: OwnershipPolicy,
        issue: CanonicalIssue,
    ) -> str | None:
        """TRK-M1-06: the first field local does not own (per ``policy``)
        whose current value on ``issue`` is not the field's empty default
        -- ``None`` if every field local does not own is empty. Checked
        before a *new* remote issue is created, when there is no external
        value yet for the ownership-aware merge to resolve against."""
        for field_name, empty_value in _CREATE_OWNERSHIP_EMPTY_DEFAULTS.items():
            if policy.local_can_write(field_name):
                continue
            if getattr(issue, field_name) != empty_value:
                return field_name
        return None

    @staticmethod
    def _legacy_key_failure(
        *,
        issue_ref: ExternalRef,
        custom_fields: Mapping[str, Any],
        operation: SyncOperation,
    ) -> SyncFailure | None:
        """N2: reject a retired TeamSpace legacy key before it reaches
        create_issue/update_issue, returning a SyncFailure instead of
        raising -- the caller records it and moves on to the next issue."""
        try:
            assert_no_forbidden_teamspace_legacy_keys({"custom_fields": dict(custom_fields)})
        except ValueError as exc:
            return SyncFailure(
                issue_ref=issue_ref,
                operation=operation,
                failure_class=None,
                message=str(exc),
                retryable=False,
            )
        return None

    @staticmethod
    def _exclude_unsupported_fields(
        *,
        patch: dict[str, Any],
        capabilities: Any,
        issue_ref: ExternalRef,
        failures: list[SyncFailure],
    ) -> None:
        """A11: fields whose capability flag is False are excluded from the
        outgoing patch before it is sent, and recorded as
        ``patch_field_denied`` (non-retryable) rather than emitted for the
        connector to deny or silently drop."""
        if "assignees" in patch and not capabilities.supports_assignment:
            del patch["assignees"]
            failures.append(
                SyncFailure(
                    issue_ref=issue_ref,
                    operation="patch_field_denied",
                    failure_class=None,
                    message="assignees excluded: connector does not support assignment",
                    retryable=False,
                )
            )
        if (
            "status" in patch
            and patch["status"] in _TERMINAL_STATUSES
            and not capabilities.supports_terminal_transition
        ):
            del patch["status"]
            failures.append(
                SyncFailure(
                    issue_ref=issue_ref,
                    operation="patch_field_denied",
                    failure_class=None,
                    message="status excluded: connector does not support a terminal transition",
                    retryable=False,
                )
            )

    async def sync(
        self,
        *,
        pull_first: bool = True,
        limit: int = 100,
        filters: Mapping[str, Any] | None = None,
    ) -> SyncResult:
        pull_result = SyncResult()
        if pull_first:
            pull_result = await self.pull(limit=limit, filters=filters)

        push_result = await self.push(limit=max(limit, 100), filters=filters)

        return SyncResult(
            stats=SyncStats(
                pulled_created=pull_result.stats.pulled_created,
                pulled_updated=pull_result.stats.pulled_updated,
                pushed_created=push_result.stats.pushed_created,
                pushed_updated=push_result.stats.pushed_updated,
                skipped=pull_result.stats.skipped + push_result.stats.skipped,
            ),
            conflicts=pull_result.conflicts + push_result.conflicts,
            errors=pull_result.errors + push_result.errors,
            failures=pull_result.failures + push_result.failures,
        )

    async def _collect_remote_index(
        self,
        *,
        limit: int,
        filters: Mapping[str, Any] | None,
    ) -> dict[str, CanonicalIssue]:
        index: dict[str, CanonicalIssue] = {}
        cursor: str | None = None

        while True:
            page = await self.connector.list_issues(
                updated_since=None,
                cursor=cursor,
                limit=limit,
                filters=filters,
            )
            for issue in page.items:
                index[issue.ref.identity] = issue
            if page.next_cursor is None:
                break
            cursor = page.next_cursor

        return index

    def _merge_issues(
        self,
        *,
        local_issue: CanonicalIssue,
        external_issue: CanonicalIssue,
    ) -> tuple[CanonicalIssue, list[ConflictRecord]]:
        merged = local_issue.clone()
        conflicts: list[ConflictRecord] = []

        for field_name in CORE_ISSUE_FIELDS:
            owner = self.policy.owner_for(field_name)
            local_value = getattr(local_issue, field_name)
            external_value = getattr(external_issue, field_name)
            resolution = resolve_field(
                field_name=field_name,
                owner=owner,
                local_value=local_value,
                external_value=external_value,
                local_updated_at=local_issue.updated_at,
                external_updated_at=external_issue.updated_at,
                strategy=self.strategy,
            )
            setattr(merged, field_name, resolution.value)
            if resolution.conflict is not None:
                # A9 (TRK-M1-03): attribute the conflict to the issue it
                # was raised on.
                conflicts.append(
                    dataclasses.replace(resolution.conflict, issue_ref=local_issue.ref)
                )

        if merged.created_at is None:
            merged.created_at = external_issue.created_at or local_issue.created_at

        merged.updated_at = self._max_dt(local_issue.updated_at, external_issue.updated_at)
        merged.raw = external_issue.raw if external_issue.raw is not None else local_issue.raw
        return merged, conflicts

    @staticmethod
    def _build_patch(*, before: CanonicalIssue, after: CanonicalIssue) -> dict[str, Any]:
        patch: dict[str, Any] = {}
        for field_name in CORE_ISSUE_FIELDS:
            old = getattr(before, field_name)
            new = getattr(after, field_name)
            if old != new:
                patch[field_name] = new
        return patch

    @staticmethod
    def _idempotency_key(ref: ExternalRef) -> str:
        return f"sync:{ref.identity}"

    async def _create_issue_with_retry(self, issue: CanonicalIssue) -> CanonicalIssue:
        """TRK-M1-06: mirror of ``_update_issue_with_retry`` for the create
        path -- a transient ``ConnectorRequestError`` (e.g. the write
        landed but the response was lost) is retried up to
        ``max_retry_attempts`` times before it is surfaced to the caller
        as a permanent :class:`SyncFailure`. Relies on
        ``TaskTrackerConnector.create_issue`` being create-if-absent
        (idempotent for a retry of identical content) rather than a blind
        upsert -- see ``InMemoryConnector.create_issue``."""
        attempt = 0
        while True:
            try:
                return await self.connector.create_issue(issue)
            except ConnectorRequestError as exc:
                if not exc.is_retryable or attempt >= self.max_retry_attempts:
                    raise
                attempt += 1

    async def _update_issue_with_retry(
        self,
        *,
        ref: ExternalRef,
        patch: dict[str, Any],
        idempotency_key: str,
    ) -> CanonicalIssue:
        attempt = 0
        while True:
            try:
                return await self.connector.update_issue(
                    ref,
                    patch,
                    idempotency_key=idempotency_key,
                )
            except ConnectorRequestError as exc:
                if not exc.is_retryable or attempt >= self.max_retry_attempts:
                    raise
                attempt += 1

    def _enforce_conflict_policy(self, conflicts: list[ConflictRecord]) -> None:
        if not self.strict_manual_review:
            return
        if any(conflict.manual_review_required for conflict in conflicts):
            raise SyncConflictError(
                "Manual review conflicts detected while strict_manual_review is enabled"
            )

    @staticmethod
    def _max_dt(
        left: datetime | None,
        right: datetime | None,
    ) -> datetime | None:
        if left is None:
            return right
        if right is None:
            return left
        return max(left, right)
