"""Settle crawl sessions whose run lease died long ago — `partial` / `lease_expired`.

The stale-session reaper (`WebCrawlRepository.fail_stale_sessions`) fails
orphaned sessions after 30 minutes without an `updated_at` bump, so the
crash-resume sweep can continue them. It skips soft-deleted rows, so a
session deleted while `running` stays `running` forever — e.g. d5aa4b34,
`running` since 2026-09-14 with its heartbeat stopped at 13:55 that day.

This sweep judges the RUN LEASE itself: no heartbeat for longer than
`LEASE_EXPIRED_AFTER` means no process owns the run, so it is settled to its
honest terminal state (`stats.stop_reason = "lease_expired"`) — far past the
window in which a crash-resume would still pick it up. It runs inside the
scraper server's existing stale-session reaper loop; it adds no schedule.

Every deployment's reaper acts on every session, whichever deployment ran it.
That is safe: a live run heartbeats its lease every 30 s
(`RUN_LEASE_HEARTBEAT_EVERY`), so only a run silent for 6 hours — 720 missed
heartbeats — is ever touched, and the settle is a compare-and-swap on the
lease and row version it read.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any

from matrx_utils import utcnow

from matrx_scraper.db.models_web import CrawlSession as WebCrawlSession

logger = logging.getLogger(__name__)

#: A run lease with no heartbeat for this long is dead (the live heartbeat beats
#: every 30 s; the crash-resume window is 30 min). CAPS constant.
LEASE_EXPIRED_AFTER = timedelta(hours=6)
LEASE_EXPIRED_STOP_REASON = "lease_expired"
#: A reaped lease's owner becomes this prefix + the old owner, so the old run's
#: lease-pinned writes (`metadata @> {run_lease: {owner: <token>}}`) match nothing.
REAPED_LEASE_OWNER_PREFIX = "reaped:"
_ACTIVE = ["queued", "running"]


def _parse_ts(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str) and value:
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None
    return None


def last_run_signal(session: Any) -> datetime | None:
    """When some process last showed it owned this run: the lease heartbeat
    (else its acquisition), else — for a session that never leased — `updated_at`."""
    lease = ((getattr(session, "metadata", None) or {}).get("run_lease")) or {}
    for key in ("heartbeat_at", "acquired_at"):
        ts = _parse_ts(lease.get(key))
        if ts is not None:
            return ts
    return _parse_ts(getattr(session, "updated_at", None))


def _settle_guard(session: Any) -> tuple[dict[str, Any], dict[str, Any]]:
    """The compare-and-swap filter on what was read (row version + lease owner
    and heartbeat), and the metadata to write with the lease owner replaced so
    the old run's lease-pinned writes match nothing."""
    metadata = dict(getattr(session, "metadata", None) or {})
    lease = dict(metadata.get("run_lease") or {})
    guard: dict[str, Any] = {"id": str(session.id), "status__in": _ACTIVE}
    version = getattr(session, "version", None)
    if version is not None:
        guard["version"] = version
    if lease.get("owner"):
        read = {"owner": lease["owner"]}
        if lease.get("heartbeat_at"):
            read["heartbeat_at"] = lease["heartbeat_at"]
        guard["metadata__json_contains"] = {"run_lease": read}
        metadata["run_lease"] = {
            **lease,
            "owner": f"{REAPED_LEASE_OWNER_PREFIX}{lease['owner']}",
            "reaped_at": utcnow().isoformat(),
        }
    return guard, metadata


async def _settle_expired(session: Any, *, now: datetime, signal: datetime) -> bool:
    """Settle one session whose run is gone and will not be resumed."""
    lease = ((getattr(session, "metadata", None) or {}).get("run_lease")) or {}
    ran = bool(lease) or getattr(session, "started_at", None) is not None
    stats = dict(getattr(session, "stats", None) or {})
    stats["stop_reason"] = LEASE_EXPIRED_STOP_REASON
    stats["termination"] = LEASE_EXPIRED_STOP_REASON
    guard, metadata = _settle_guard(session)
    result = await WebCrawlSession.update_where(
        guard,
        status="partial" if ran else "failed",
        finished_at=now,
        stats=stats,
        metadata=metadata,
        error=(
            f"Run lease expired: no heartbeat since {signal:%Y-%m-%d %H:%M} UTC."
            if ran
            else f"Never started: queued since {signal:%Y-%m-%d %H:%M} UTC with no worker."
        ),
    )
    return bool(result.rows_affected)


async def fail_dead_lease_sessions(*, now: datetime | None = None) -> list[str]:
    """Hand runs whose lease went silent to crash-resume — within minutes.

    A `running` session whose run lease has not beaten for
    `DEAD_RUN_LEASE_AFTER` (5 min = ten missed 30 s beats) has no live process.
    A live (not deleted) one is marked `failed` with the stale-session marker:
    exactly the handoff `resume_crashed_sessions` consumes, so the deployment
    that owned the run continues it under the ownership rules. A soft-deleted
    one is never resumed — it is settled `partial` / `lease_expired` now
    rather than by the 6-hour backstop. Leaseless sessions are left to the
    30-minute stale-session reaper (they have no heartbeat to judge). Every
    settle is a compare-and-swap on what was read. Returns the ids settled.
    """
    from matrx_scraper.web_crawl.persistence import (
        DEAD_RUN_LEASE_AFTER,
        STALE_SESSION_ERROR,
        run_lease_is_live,
    )

    now = now or utcnow()
    cutoff = now - DEAD_RUN_LEASE_AFTER
    candidates = await WebCrawlSession.filter(
        status="running", updated_at__lt=cutoff
    ).all(use_cache=False)
    settled: list[str] = []
    for session in candidates:
        lease = ((getattr(session, "metadata", None) or {}).get("run_lease")) or {}
        if not lease.get("owner") or run_lease_is_live(session, now=now):
            continue
        signal = last_run_signal(session) or cutoff
        if getattr(session, "deleted_at", None) is not None:
            if await _settle_expired(session, now=now, signal=signal):
                settled.append(str(session.id))
            continue
        guard, metadata = _settle_guard(session)
        result = await WebCrawlSession.update_where(
            guard,
            status="failed",
            finished_at=now,
            metadata=metadata,
            error=STALE_SESSION_ERROR,
        )
        if result.rows_affected:
            settled.append(str(session.id))
    if settled:
        logger.error(
            "run lease silent past %s: handed %s crawl session(s) to crash-resume / settled: %s",
            DEAD_RUN_LEASE_AFTER,
            len(settled),
            ", ".join(settled),
        )
    return settled


async def settle_lease_expired_sessions(*, now: datetime | None = None) -> list[str]:
    """The 6-hour backstop: settle every queued/running session (deleted or not)
    whose run lease has been silent past `LEASE_EXPIRED_AFTER`. Returns the
    settled ids.

    * The scan is filtered in SQL by `updated_at` (a heartbeat UPDATE bumps it
      through `_touch_row`, so a live lease always has a fresh row); the lease's
      own heartbeat is then checked per row.
    * Each settle is a compare-and-swap on what was read — the row `version`
      (bumped by every UPDATE) and the lease owner + heartbeat — so a run that
      heartbeats in the gap wins and is left alone.
    * The settle replaces the lease owner, so a zombie run's lease-pinned
      writes match nothing afterwards.
    * A session that ran settles `partial`; one that never ran (no lease, never
      started) settles `failed` — it did nothing. Both carry
      `stats.stop_reason = "lease_expired"`.
    """
    now = now or utcnow()
    cutoff = now - LEASE_EXPIRED_AFTER
    candidates = await WebCrawlSession.filter(
        status__in=_ACTIVE, updated_at__lt=cutoff
    ).all(use_cache=False)
    settled: list[str] = []
    for session in candidates:
        signal = last_run_signal(session)
        if signal is None or signal >= cutoff:
            continue
        if await _settle_expired(session, now=now, signal=signal):
            settled.append(str(session.id))
    if settled:
        logger.error(
            "settled %s crawl session(s) whose run lease expired: %s",
            len(settled),
            ", ".join(settled),
        )
    return settled


__all__ = [
    "fail_dead_lease_sessions",
    "LEASE_EXPIRED_AFTER",
    "LEASE_EXPIRED_STOP_REASON",
    "last_run_signal",
    "settle_lease_expired_sessions",
]
