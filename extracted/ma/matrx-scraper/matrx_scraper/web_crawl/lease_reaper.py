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


async def settle_lease_expired_sessions(*, now: datetime | None = None) -> list[str]:
    """Settle every queued/running session (deleted or not) whose run lease
    has been silent past `LEASE_EXPIRED_AFTER`. Returns the settled ids.

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
        metadata = dict(getattr(session, "metadata", None) or {})
        lease = dict(metadata.get("run_lease") or {})
        ran = bool(lease) or getattr(session, "started_at", None) is not None
        stats = dict(getattr(session, "stats", None) or {})
        stats["stop_reason"] = LEASE_EXPIRED_STOP_REASON
        stats["termination"] = LEASE_EXPIRED_STOP_REASON
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
                "reaped_at": now.isoformat(),
            }
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
        if result.rows_affected:
            settled.append(str(session.id))
    if settled:
        logger.error(
            "settled %s crawl session(s) whose run lease expired: %s",
            len(settled),
            ", ".join(settled),
        )
    return settled


__all__ = [
    "LEASE_EXPIRED_AFTER",
    "LEASE_EXPIRED_STOP_REASON",
    "last_run_signal",
    "settle_lease_expired_sessions",
]
