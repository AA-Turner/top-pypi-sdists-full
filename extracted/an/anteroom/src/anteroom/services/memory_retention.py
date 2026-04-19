"""Memory-artifact retention & eviction pipeline (#625).

Policy-driven eviction for memory artifacts, executed inside the
existing :class:`~anteroom.services.retention.RetentionWorker`. The
worker calls :func:`purge_memories` once per cycle when the
``MemoryRetentionConfig.enabled`` flag is true.

Design principles:

* **Default off**: ``enabled=False`` means zero memories are ever
  touched. Retention is explicit opt-in, matching the project's
  data-sovereignty posture.
* **Pin is load-bearing**: any memory with ``metadata.pinned == True`` is
  skipped unless ``respect_pins=False`` (escape hatch).
* **Pack-sourced memories are never evicted**: they would be re-installed
  on the next pack sync and churn the DB. Only artifacts with
  ``source == "local"`` are considered.
* **Dry-run never mutates**: :func:`purge_memories` with ``dry_run=True``
  returns the would-be-purged list and deliberately does NOT emit audit
  entries — preview must stay off the tamper chain.
* **Audit per purge**: when ``audit_writer`` is non-None, one
  ``memory.purge`` audit entry is emitted per actual deletion with
  FQN + reason + structural metadata. Content is never logged.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Literal

from .artifact_storage import delete_artifact, list_artifacts
from .artifacts import ArtifactType

if TYPE_CHECKING:
    from ..config import MemoryRetentionConfig
    from ..db import ThreadSafeConnection
    from .audit import AuditWriter

logger = logging.getLogger(__name__)


# Reason codes are stable strings consumers can pattern-match on.
PurgeReason = Literal["max_age", "idle", "status"]


@dataclass(frozen=True)
class PurgeItem:
    """Single memory considered for (or actually) purged, audit-safe."""

    fqn: str
    reason: PurgeReason
    age_days: int
    last_recalled_at: str | None
    recall_count: int
    status: str | None
    pinned: bool


@dataclass(frozen=True)
class PurgeResult:
    """Summary of a retention pass. ``items`` is the concrete list of
    memories matched (actually deleted in non-dry-run mode, would-be in
    dry-run mode). ``skipped_pinned_count`` counts memories that matched
    eligibility but survived because of the pin flag.

    ``purged_by`` is the reviewer identity that triggered the pass.
    ``None`` when the scheduled worker ran the pass (the worker has no
    reviewer session); set for HTTP/CLI-originated purges so the audit
    trail and the UI can distinguish an on-demand governed purge from a
    background run."""

    purged_count: int
    skipped_pinned_count: int
    items: list[PurgeItem] = field(default_factory=list)
    dry_run: bool = False
    purged_by: str | None = None


# ---------------------------------------------------------------------------
# Pure eligibility helpers
# ---------------------------------------------------------------------------


def _parse_iso(ts: str | None) -> datetime | None:
    """Parse an ISO-8601 timestamp (with or without trailing ``Z``)."""
    if not ts or not isinstance(ts, str):
        return None
    try:
        # datetime.fromisoformat handles both with and without Z since 3.11.
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


def _age_days(art: dict[str, Any], now: datetime) -> int:
    """Days since ``created_at``; 0 when the timestamp is unparseable."""
    created = _parse_iso(art.get("created_at"))
    if created is None:
        return 0
    delta = now - created
    return max(0, delta.days)


def _idle_days(art: dict[str, Any], now: datetime) -> int:
    """Days since ``metadata.last_recalled_at``, falling back to
    ``created_at`` when recall telemetry has not fired yet."""
    meta = art.get("metadata") or {}
    last = _parse_iso(meta.get("last_recalled_at"))
    if last is None:
        last = _parse_iso(art.get("created_at"))
    if last is None:
        return 0
    delta = now - last
    return max(0, delta.days)


def _expired_by_age(art: dict[str, Any], now: datetime, max_age_days: int | None) -> bool:
    """True when ``max_age_days`` is set and the memory is older than it."""
    if max_age_days is None or max_age_days <= 0:
        return False
    return _age_days(art, now) >= max_age_days


def _expired_by_idle(
    art: dict[str, Any],
    now: datetime,
    idle_days: int | None,
    min_age_days: int,
) -> bool:
    """True when ``idle_days`` is set, the memory has been idle longer
    than that, and the memory is older than the ``min_age_days`` grace
    floor (so freshly-approved memories aren't immediately evicted)."""
    if idle_days is None or idle_days <= 0:
        return False
    if _age_days(art, now) < max(0, min_age_days):
        return False
    return _idle_days(art, now) >= idle_days


def _eligible_by_status(art: dict[str, Any], purge_statuses: list[str]) -> bool:
    """True when the memory's status is in the configured ``purge_statuses``."""
    meta = art.get("metadata") or {}
    return meta.get("memory_status") in purge_statuses


def _is_pinned(art: dict[str, Any]) -> bool:
    """True when the memory's metadata carries ``pinned: True``."""
    meta = art.get("metadata") or {}
    return bool(meta.get("pinned"))


def _is_pack_sourced(art: dict[str, Any]) -> bool:
    """Non-local artifacts (e.g. pack-sourced) are skipped so they don't
    churn when the pack is re-synced. Matches the artifact source-layer
    convention — ``source == "local"`` is user-owned."""
    return art.get("source") != "local"


def _reason_for(
    art: dict[str, Any],
    policy: MemoryRetentionConfig,
    now: datetime,
) -> PurgeReason | None:
    """Return the first reason code that matches, or ``None`` when the
    memory should NOT be purged.

    Evaluation order is deterministic: max_age → idle → status. A memory
    can match multiple rules; the first one wins so audit logs have a
    single canonical reason.
    """
    if _expired_by_age(art, now, policy.max_age_days):
        return "max_age"
    if _expired_by_idle(art, now, policy.idle_days, policy.min_age_days):
        return "idle"
    if _eligible_by_status(art, policy.purge_statuses):
        return "status"
    return None


# ---------------------------------------------------------------------------
# Purge loop
# ---------------------------------------------------------------------------


def _item_for(art: dict[str, Any], reason: PurgeReason, now: datetime) -> PurgeItem:
    meta = art.get("metadata") or {}
    return PurgeItem(
        fqn=art["fqn"],
        reason=reason,
        age_days=_age_days(art, now),
        last_recalled_at=meta.get("last_recalled_at"),
        recall_count=int(meta.get("recall_count") or 0),
        status=meta.get("memory_status"),
        pinned=_is_pinned(art),
    )


def _emit_audit(
    audit_writer: AuditWriter | None,
    item: PurgeItem,
    reviewer_id: str | None,
) -> None:
    if audit_writer is None:
        return
    # Import lazily so tests that mock ``audit_writer`` don't require the
    # full audit stack to be importable.
    from .audit import AuditEntry

    entry = AuditEntry.create(
        event_type="memory.purge",
        # The scheduled worker has no reviewer session; an HTTP/CLI
        # on-demand purge does. user_id stays empty for the worker
        # (matching the existing audit convention) and carries the
        # reviewer identity on governed purges so the audit trail can
        # distinguish the two paths.
        user_id=reviewer_id or "",
        details={
            "fqn": item.fqn,
            "reason": item.reason,
            "age_days": item.age_days,
            "last_recalled_at": item.last_recalled_at,
            "recall_count": item.recall_count,
            "status": item.status,
            "pinned": item.pinned,
            "reviewer_id": reviewer_id,
            "triggered_by": "reviewer" if reviewer_id else "scheduler",
        },
    )
    try:
        audit_writer.emit(entry)
    except Exception:  # pragma: no cover — audit must never block retention
        logger.exception("Failed to emit audit entry for memory.purge")


def purge_memories(
    db: ThreadSafeConnection,
    policy: MemoryRetentionConfig,
    *,
    dry_run: bool = False,
    audit_writer: AuditWriter | None = None,
    reviewer_id: str | None = None,
) -> PurgeResult:
    """Evaluate the retention *policy* against all memory artifacts.

    When *dry_run* is True, no deletes happen and no audit entries are
    emitted — the caller gets a preview of what the worker would do on
    the next cycle.

    When *dry_run* is False, each purged item triggers one
    ``memory.purge`` audit entry (when *audit_writer* is non-None) and
    one ``delete_artifact`` call.

    *reviewer_id* identifies the principal that triggered an on-demand
    purge (HTTP ``/retention-purge`` or CLI ``memory retention
    purge``). It is stamped into each audit entry's ``user_id`` field
    and into ``details.reviewer_id`` and carried back on
    :class:`PurgeResult.purged_by` so the UI can show who ran the
    pass. When the scheduled worker calls this function,
    ``reviewer_id`` is left as ``None`` and audit entries record
    ``triggered_by="scheduler"``.

    Pinned memories are skipped when ``policy.respect_pins`` is True
    (the default). Non-local (e.g. pack-sourced) memories are always
    skipped regardless of policy to avoid churning the DB on pack sync.

    Returns a :class:`PurgeResult` describing what was (or would be)
    purged. Does not raise — individual delete failures are logged and
    counted via the ``skipped_pinned_count`` stream (pin) but never
    abort the pass.
    """
    if not policy.enabled:
        return PurgeResult(
            purged_count=0,
            skipped_pinned_count=0,
            items=[],
            dry_run=dry_run,
            purged_by=reviewer_id,
        )

    now = datetime.now(timezone.utc)
    candidates = list_artifacts(db, artifact_type=ArtifactType.MEMORY)

    items: list[PurgeItem] = []
    skipped_pinned = 0
    purged = 0

    for art in candidates:
        if _is_pack_sourced(art):
            continue
        reason = _reason_for(art, policy, now)
        if reason is None:
            continue
        if policy.respect_pins and _is_pinned(art):
            skipped_pinned += 1
            continue

        item = _item_for(art, reason, now)
        items.append(item)
        if dry_run:
            continue

        try:
            removed = delete_artifact(db, art["id"])
        except Exception:
            logger.exception("Failed to delete memory %s during retention", art.get("fqn"))
            continue
        if not removed:
            logger.warning("delete_artifact returned False for %s", art.get("fqn"))
            continue

        purged += 1
        _emit_audit(audit_writer, item, reviewer_id)

    return PurgeResult(
        purged_count=purged if not dry_run else len(items),
        skipped_pinned_count=skipped_pinned,
        items=items,
        dry_run=dry_run,
        purged_by=reviewer_id,
    )
