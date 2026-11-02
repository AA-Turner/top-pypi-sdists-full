"""the import_job analytics events: enqueued, stalled, finished, with their shared props."""

from __future__ import annotations
import time
from datetime import datetime, timezone


# -- funnel ------------------------------------------------------------------
# The wizard's own `backfill.summary` fires when it HANDS WORK OFF to one of
# these workers, and reports `partial` with 0% coverage for everything still
# queued -- which is every onboarding import, every time. So "did the import
# this person approved actually finish?" is answerable only from here.
#
# Metadata only, same contract as the rest of client telemetry: counts,
# booleans, durations and enum outcomes. Never a label (it carries a folder
# name), never `error` (lane prose can embed a path), never a payload field.


def _telemetry():
    """The telemetry module, or None when this process cannot reach it.

    A worker runs from a PINNED source tree -- the copy of `probe/` that was on
    disk when its approval was made, so an upgrade mid-import cannot change the
    code replaying it -- and that tree carries only the modules the lanes need.
    An unconditional import here turned every detached worker into an immediate
    ImportError: the import did not merely go unreported, it stopped happening.
    Telemetry is allowed to be absent; it is never allowed to be load-bearing.
    """
    try:
        from probe import analytics as telemetry
    except Exception:
        return None
    return telemetry


def _context(job: dict | None = None):
    """This process's funnel handle, or None. Never raises.

    With a job, the APPROVING session replayed off its record; without one,
    whatever context this process already started.
    """
    telemetry = _telemetry()
    if telemetry is None:
        return None
    try:
        return telemetry.current() if job is None else telemetry.job_context(job.get("origin"))
    except Exception:
        return None


def _origin_stamp():
    telemetry = _telemetry()
    if telemetry is None:
        return None
    try:
        return telemetry.origin_stamp()
    except Exception:
        return None


def _job_props(job: dict) -> dict:
    """The shape every import_job event shares. Never raises."""
    from ..progress import counts

    props = {"kind": str(job.get("kind") or ""), "job_id": job.get("id"),
             "attempt": job.get("attempt")}
    try:
        done, total = counts(job)
        props["units_done"] = done
        props["units_total"] = total
        if total:
            props["coverage_pct"] = round(100.0 * min(done or 0, total) / total, 1)
    except Exception:
        pass
    return props


def _elapsed_seconds(job: dict) -> float | None:
    for field in ("started_at", "created_at"):
        try:
            started = datetime.fromisoformat(job[field].replace("Z", "+00:00"))
            if started.tzinfo is None:
                started = started.replace(tzinfo=timezone.utc)
            return round(max(0.0, time.time() - started.timestamp()), 1)
        except Exception:
            continue
    return None


def _emit_finished(job: dict, outcome, *, tel=None, **extra) -> None:
    try:
        tel = tel or _context(job)
        tel.emit(
            _telemetry().EVENT_IMPORT_JOB_FINISHED,
            outcome=str(outcome),
            duration_seconds=_elapsed_seconds(job),
            **_job_props(job),
            **extra,
        )
    except Exception:
        pass  # observability must never become observable


def _emit_enqueued(job: dict, *, resumed: bool) -> None:
    """The approval becoming durable work -- the funnel's join to the lane
    events, emitted in the APPROVING process so it carries that session."""
    try:
        _context().emit(
            _telemetry().EVENT_IMPORT_JOB_ENQUEUED,
            resumed=resumed,
            state=str(job.get("state") or ""),
            **_job_props(job),
        )
    except Exception:
        pass


def _emit_stalled(job: dict, reason, *, tel=None, **extra) -> None:
    try:
        tel = tel or _context(job)
        tel.emit(
            _telemetry().EVENT_IMPORT_JOB_STALLED,
            reason=str(reason),
            age_seconds=_elapsed_seconds(job),
            **_job_props(job),
            **extra,
        )
    except Exception:
        pass
