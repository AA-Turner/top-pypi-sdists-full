from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Mapping

from spec_kitty_tracker.conflicts import ConflictRecord, ConflictStrategy, resolve_field
from spec_kitty_tracker.errors import ConnectorRequestError, SyncConflictError
from spec_kitty_tracker.models import CanonicalIssue, ExternalRef, SyncCheckpoint
from spec_kitty_tracker.policy import CORE_ISSUE_FIELDS, OwnershipPolicy
from spec_kitty_tracker.protocols import LocalIssueStore, TaskTrackerConnector


@dataclass(slots=True)
class SyncStats:
    pulled_created: int = 0
    pulled_updated: int = 0
    pushed_created: int = 0
    pushed_updated: int = 0
    skipped: int = 0


@dataclass(slots=True)
class SyncResult:
    stats: SyncStats = field(default_factory=SyncStats)
    conflicts: list[ConflictRecord] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


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

    async def pull(
        self,
        *,
        limit: int = 100,
        filters: Mapping[str, Any] | None = None,
    ) -> SyncResult:
        result = SyncResult()
        cursor: str | None = None
        max_updated_at = self._checkpoint.updated_since

        while True:
            page = await self.connector.list_issues(
                updated_since=self._checkpoint.updated_since,
                cursor=cursor,
                limit=limit,
                filters=filters,
            )
            for external_issue in page.items:
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

            if page.next_cursor is None:
                break
            cursor = page.next_cursor

        self._checkpoint = SyncCheckpoint(cursor=cursor, updated_since=max_updated_at)
        self._enforce_conflict_policy(result.conflicts)
        return result

    async def push(
        self,
        *,
        limit: int = 200,
        filters: Mapping[str, Any] | None = None,
    ) -> SyncResult:
        result = SyncResult()
        remote_index = await self._collect_remote_index(limit=limit, filters=filters)
        local_issues = await self.store.list_issues(system=self.connector.name)

        for local_issue in local_issues:
            remote_issue = remote_index.get(local_issue.ref.identity)
            if remote_issue is None:
                if not self.policy.local_can_write("title"):
                    result.stats.skipped += 1
                    continue
                created = await self.connector.create_issue(local_issue)
                await self.store.upsert_issue(created)
                result.stats.pushed_created += 1
                continue

            desired_remote, conflicts = self._merge_issues(
                local_issue=local_issue,
                external_issue=remote_issue,
            )
            result.conflicts.extend(conflicts)

            patch = self._build_patch(before=remote_issue, after=desired_remote)
            if not patch:
                result.stats.skipped += 1
                continue

            updated_remote = await self._update_issue_with_retry(
                ref=local_issue.ref,
                patch=patch,
                idempotency_key=self._idempotency_key(local_issue.ref),
            )
            merged_local, post_conflicts = self._merge_issues(
                local_issue=local_issue,
                external_issue=updated_remote,
            )
            result.conflicts.extend(post_conflicts)
            await self.store.upsert_issue(merged_local)
            result.stats.pushed_updated += 1

        self._enforce_conflict_policy(result.conflicts)
        return result

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
                conflicts.append(resolution.conflict)

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
