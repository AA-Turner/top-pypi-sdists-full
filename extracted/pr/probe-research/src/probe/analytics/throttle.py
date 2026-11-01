"""decide when a repeat report is due (file-stamp throttle) and whether an outbox is stuck."""

from __future__ import annotations
import os
from datetime import datetime, timezone
from probe.foundation.compat.compat import fromisoformat


# Outbox: the drainer reports what delivery did; a stuck queue has no drainer, so the banner does.
# Metadata only: `last_error` is free text, so only its exception TYPE goes. DESIGN.md.

#: Rate-limit stamp, in the journal dir so it is per-outbox and dies with it.
_STUCK_STAMP = "telemetry-stuck.stamp"
#: Stuck is a level every `probe` command re-sees: 6 h caps a loop shelling out thousands of
#: times at 4 reports a day, and bounds how long a newly wedged queue stays unseen.
STUCK_REPORT_INTERVAL_S = 6 * 3600.0
#: Seconds: held writes (for a credential nothing here can send) this old make a queue stuck;
#: they wait for that credential, which for a revoked one is never.
STUCK_HELD_S = 3600.0


def _error_kind(last_error: str | None) -> str | None:
    """The exception TYPE from a journal `last_error`, or None.

    `last_error` is `_redact(f"{type(exc).__name__}: {exc}")`; only the class name is
    metadata, and anything that is not a bare identifier is dropped, never guessed at.
    """
    if not isinstance(last_error, str):
        return None
    head = last_error.split(":", 1)[0].strip()
    return head if head.isidentifier() else None


def _age_hours(stamp: str | None) -> float | None:
    """Whole-ish hours since an ISO stamp; None when it will not parse."""
    if not stamp or not isinstance(stamp, str):
        return None
    try:
        parsed = fromisoformat(stamp)
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    delta = (datetime.now(timezone.utc) - parsed).total_seconds()
    return round(max(delta, 0.0) / 3600.0, 2)


def report_due(spool_dir: str | None, key: str, *, interval_s: float) -> bool:
    """Whether a report keyed on `key` is due, claiming the window when it is.

    A stamp FILE, not a counter: a loop running `probe log` per step is N fresh processes.
    O_CREAT|O_EXCL picks one winner; an expired stamp is claimed by a utime bump. An
    unwritable dir or ``spool_dir`` None answers False, else every command would report.
    The caller resolves ``spool_dir`` (unset `--spool-dir`: the journal's `default_dir()`).
    Why: DESIGN.md (report_due).
    """
    if not spool_dir:
        return False
    path = os.path.join(os.path.expanduser(spool_dir), f"telemetry-{_safe_key(key)}.stamp")
    try:
        # Never-reported: an atomic create decides the single winner.
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        os.close(fd)
        return True
    except FileExistsError:
        pass
    except OSError:
        return False
    try:
        if datetime.now(timezone.utc).timestamp() - os.stat(path).st_mtime < interval_s:
            return False
        os.utime(path, None)  # claim the new window
    except OSError:
        return False
    return True


def _safe_key(key: str) -> str:
    """A stamp-filename-safe form of a report key. The keys are hand-written
    literals, so this only has to stop a typo from escaping the directory."""
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in key)[:64]


def stuck_report_due(spool_dir: str | None, *, interval_s: float = STUCK_REPORT_INTERVAL_S) -> bool:
    """The stuck-report throttle. See :func:`report_due`."""
    return report_due(spool_dir, "stuck", interval_s=interval_s)


def stuck_status(status: dict, *, auth_blocked_since: str | None) -> bool:
    """Whether this queue is STUCK, as opposed to merely carrying old scars.

    Not the banner's condition: dead letters are permanent, so counting them made a
    drained queue report every 6 h forever (DESIGN.md (stuck_status)); their count only
    rides the event. Stuck is: blocked on credentials, paused with work pending, or one
    queue's oldest held write STUCK_HELD_S old (`blocked_oldest_pending`, judged per
    queue by `Journal.read_status`, a run close waiting on its data left out).
    ``auth_blocked_since`` is the caller's `journal.auth_blocked_since(status)`.
    """
    if auth_blocked_since:
        return True
    if bool(status.get("pending")) and bool(status.get("paused")):
        return True
    blocked_hours = _age_hours(status.get("blocked_oldest_pending"))
    return blocked_hours is not None and blocked_hours * 3600 >= STUCK_HELD_S
