"""Policy-driven retention for disposable files in reserved temporary paths."""

from __future__ import annotations

import fnmatch
import logging
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime, timedelta
from time import monotonic
from typing import TYPE_CHECKING, Protocol

from matrx_orm import Q
from pydantic import BaseModel, ConfigDict, Field, field_validator

from .cloud_sync.db import _models, _vals
from .cloud_sync.purge_escape import purge_escaped

if TYPE_CHECKING:
    from .cloud_sync.sync_engine import SyncEngine

logger = logging.getLogger("matrx_files.retention")

DEFAULT_TEMPORARY_FILE_TTL = timedelta(hours=48)
VOICE_RECORDING_RETENTION_TTL = timedelta(days=30)
MEET_RECORDING_RETENTION_TTL = timedelta(days=30)


async def run_retention_purge_transaction[T](
    root_file_id: object, operation: Callable[[], Awaitable[T]]
) -> T:
    """Run a retention finalizer inside the package-owned purge transaction.

    Central lifecycle custody has a two-phase contract that the ordinary
    ``SyncEngine`` delete cannot express: it must lock and revalidate policy,
    prove the external object absent, and delete the database row without
    releasing those locks. This is the one public extension point for that
    finalizer. The package still owns the exact-root GUC and transaction; host
    code supplies only the work that must remain atomic inside it.
    """
    return await purge_escaped(root_file_id, operation)


class TemporaryFileRetentionPolicy(BaseModel):
    """Named, bounded retention policy for one reserved temporary namespace."""

    model_config = ConfigDict(frozen=True)

    name: str = Field(min_length=1, max_length=100, pattern=r"^[a-z][a-z0-9_-]*$")
    path_prefix: str
    filename_glob: str
    ttl: timedelta = DEFAULT_TEMPORARY_FILE_TTL
    batch_size: int = Field(default=100, ge=1, le=1_000)
    max_batches: int = Field(default=10, ge=1, le=1_000)
    dry_run: bool = True

    @field_validator("path_prefix")
    @classmethod
    def _validate_path_prefix(cls, value: str) -> str:
        if (
            not value.startswith(".matrx-tmp/")
            or not value.endswith("/")
            or ".." in value.split("/")
            or "\\" in value
        ):
            raise ValueError(
                "path_prefix must be a normalized directory below the reserved "
                "'.matrx-tmp/' namespace"
            )
        return value

    @field_validator("filename_glob")
    @classmethod
    def _validate_filename_glob(cls, value: str) -> str:
        if not value or "/" in value or "\\" in value or value in {"*", "**"}:
            raise ValueError("filename_glob must narrowly match basenames, not every file")
        return value

    @field_validator("ttl")
    @classmethod
    def _validate_ttl(cls, value: timedelta) -> timedelta:
        if value < timedelta(hours=1):
            raise ValueError("ttl must be at least one hour")
        return value

    def matches_path(self, file_path: str) -> bool:
        """Return whether one logical file path belongs to this policy.

        Write/finalize paths use this before inserting a disposable row so a
        retention declaration can never name a policy that will not actually
        find the file later. The janitor reuses the same predicate below.
        """
        if not file_path.startswith(self.path_prefix):
            return False
        relative = file_path.removeprefix(self.path_prefix)
        return "/" not in relative and fnmatch.fnmatchcase(relative, self.filename_glob)

    def matches(self, candidate: RetentionCandidate, *, cutoff: datetime) -> bool:
        if candidate.id == "" or candidate.storage_uri == "":
            return False
        if candidate.created_at >= cutoff:
            return False
        return self.matches_path(candidate.file_path)


class RetentionCandidate(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    file_path: str
    storage_uri: str
    created_at: datetime

    @field_validator("created_at")
    @classmethod
    def _normalize_created_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)


VOICE_RECORDING_RETENTION_POLICY = TemporaryFileRetentionPolicy(
    name="voice_recordings_30d",
    path_prefix=".matrx-tmp/voice-recordings/",
    filename_glob="recording_*",
    ttl=VOICE_RECORDING_RETENTION_TTL,
)

#: Meeting-room recordings written by a provider egress into our own bucket and
#: adopted through ``adopt_external_object``. Declaring the policy is what makes
#: a provider-written object adoptable at all — every external object must carry
#: a NAMED lifecycle in its custody evidence. Declaring it is NOT scheduling it:
#: this policy is deliberately not registered with the janitor and has no
#: scheduler seed, so nothing deletes a meeting recording today. Turning it on is
#: a data-lifecycle decision (one owner-approved registration + seed), never a
#: side effect of landing a file.
MEET_RECORDING_RETENTION_POLICY = TemporaryFileRetentionPolicy(
    name="meet_recordings_30d",
    path_prefix=".matrx-tmp/meet-recordings/",
    filename_glob="recording_*",
    ttl=MEET_RECORDING_RETENTION_TTL,
)


#: THE one list of declared retention policies, keyed by name. A caller that is
#: configured rather than coded (a workflow step) names a policy as text; it
#: resolves here to the exact object the janitor would use. Declaring a policy
#: here does NOT schedule deletion — see each policy's own note.
DECLARED_RETENTION_POLICIES: dict[str, TemporaryFileRetentionPolicy] = {
    policy.name: policy
    for policy in (VOICE_RECORDING_RETENTION_POLICY, MEET_RECORDING_RETENTION_POLICY)
}


def retention_policy_by_name(name: str) -> TemporaryFileRetentionPolicy:
    """The declared policy called ``name``; an unknown name is refused, naming the known ones."""
    policy = DECLARED_RETENTION_POLICIES.get(name)
    if policy is None:
        known = ", ".join(sorted(DECLARED_RETENTION_POLICIES))
        raise KeyError(f"No retention policy is declared as {name!r}. Declared policies: {known}.")
    return policy


class RetentionCursor(BaseModel):
    model_config = ConfigDict(frozen=True)

    created_at: datetime
    id: str


class TemporaryFileRetentionReport(BaseModel):
    policy_name: str
    dry_run: bool
    cutoff_utc: datetime
    ttl_seconds: int
    batch_size: int
    max_batches: int
    batches: int = 0
    scanned: int = 0
    eligible: int = 0
    would_delete: int = 0
    deleted: int = 0
    already_absent: int = 0
    revalidation_skipped: int = 0
    failed: int = 0
    scan_complete: bool = True
    duration_ms: int = 0
    error_samples: list[str] = Field(default_factory=list)


class TemporaryFileRetentionStore(Protocol):
    async def load_batch(
        self,
        policy: TemporaryFileRetentionPolicy,
        *,
        cutoff: datetime,
        cursor: RetentionCursor | None,
    ) -> list[RetentionCandidate]: ...

    async def load_current(self, file_id: str) -> RetentionCandidate | None: ...


class OrmTemporaryFileRetentionStore:
    async def load_batch(
        self,
        policy: TemporaryFileRetentionPolicy,
        *,
        cutoff: datetime,
        cursor: RetentionCursor | None,
    ) -> list[RetentionCandidate]:
        mf, _ = _models()
        query = mf.Files.filter(
            file_path__startswith=policy.path_prefix,
            created_at__lt=cutoff,
        )
        if cursor is not None:
            query = query.filter(
                Q(created_at__gt=cursor.created_at)
                | Q(created_at=cursor.created_at, id__gt=cursor.id)
            )
        rows = await (
            query.order_by("created_at", "id")
            .limit(policy.batch_size)
            .values("id", "file_path", "storage_uri", "created_at")
        )
        return [RetentionCandidate.model_validate(row) for row in _vals(rows)]

    async def load_current(self, file_id: str) -> RetentionCandidate | None:
        mf, _ = _models()
        rows = await (
            mf.Files.filter(id=file_id)
            .limit(1)
            .values("id", "file_path", "storage_uri", "created_at")
        )
        values = _vals(rows)
        return RetentionCandidate.model_validate(values[0]) if values else None


class TemporaryFileRetentionJanitor:
    """Execute registered temporary-file policies through the canonical purge path."""

    def __init__(
        self,
        sync_engine: SyncEngine,
        policies: list[TemporaryFileRetentionPolicy],
        *,
        store: TemporaryFileRetentionStore | None = None,
    ) -> None:
        if not policies:
            raise ValueError("at least one temporary-file retention policy is required")
        policy_map = {policy.name: policy for policy in policies}
        if len(policy_map) != len(policies):
            raise ValueError("temporary-file retention policy names must be unique")
        self._sync_engine = sync_engine
        self._policies = policy_map
        self._store = store or OrmTemporaryFileRetentionStore()

    async def run(
        self,
        policy_name: str,
        *,
        dry_run: bool | None = None,
        now: datetime | None = None,
    ) -> TemporaryFileRetentionReport:
        policy = self._policies.get(policy_name)
        if policy is None:
            raise KeyError(
                f"temporary-file retention policy {policy_name!r} is not registered; "
                f"known={sorted(self._policies)}"
            )
        effective_dry_run = policy.dry_run if dry_run is None else dry_run
        started = monotonic()
        current_time = now or datetime.now(UTC)
        if current_time.tzinfo is None:
            raise ValueError("now must be timezone-aware")
        cutoff = current_time.astimezone(UTC) - policy.ttl
        report = TemporaryFileRetentionReport(
            policy_name=policy.name,
            dry_run=effective_dry_run,
            cutoff_utc=cutoff,
            ttl_seconds=int(policy.ttl.total_seconds()),
            batch_size=policy.batch_size,
            max_batches=policy.max_batches,
        )
        cursor: RetentionCursor | None = None

        for batch_number in range(policy.max_batches):
            candidates = await self._store.load_batch(policy, cutoff=cutoff, cursor=cursor)
            if not candidates:
                break
            report.batches += 1
            report.scanned += len(candidates)
            last = candidates[-1]
            cursor = RetentionCursor(created_at=last.created_at, id=last.id)

            for candidate in candidates:
                if not policy.matches(candidate, cutoff=cutoff):
                    continue
                report.eligible += 1
                if effective_dry_run:
                    report.would_delete += 1
                    continue

                current = await self._store.load_current(candidate.id)
                if current is None:
                    report.already_absent += 1
                    continue
                if current != candidate or not policy.matches(current, cutoff=cutoff):
                    report.revalidation_skipped += 1
                    continue
                try:
                    await self._sync_engine.hard_delete_and_purge_async(
                        current.id,
                        current.storage_uri,
                    )
                    report.deleted += 1
                except Exception as exc:  # one failed object never blocks the batch
                    report.failed += 1
                    if len(report.error_samples) < 20:
                        report.error_samples.append(f"{current.id}: {type(exc).__name__}")
                    logger.exception(
                        "temporary_file_retention_delete_failed",
                        extra={
                            "retention_policy": policy.name,
                            "file_id": current.id,
                            "file_path": current.file_path,
                        },
                    )

            if len(candidates) < policy.batch_size:
                break
            if batch_number == policy.max_batches - 1:
                report.scan_complete = False

        report.duration_ms = round((monotonic() - started) * 1_000)
        logger.info(
            "temporary_file_retention_complete",
            extra={"retention_report": report.model_dump(mode="json")},
        )
        return report


__all__ = [
    "DECLARED_RETENTION_POLICIES",
    "DEFAULT_TEMPORARY_FILE_TTL",
    "MEET_RECORDING_RETENTION_POLICY",
    "MEET_RECORDING_RETENTION_TTL",
    "OrmTemporaryFileRetentionStore",
    "RetentionCandidate",
    "RetentionCursor",
    "TemporaryFileRetentionJanitor",
    "TemporaryFileRetentionPolicy",
    "TemporaryFileRetentionReport",
    "TemporaryFileRetentionStore",
    "VOICE_RECORDING_RETENTION_POLICY",
    "VOICE_RECORDING_RETENTION_TTL",
    "retention_policy_by_name",
]
