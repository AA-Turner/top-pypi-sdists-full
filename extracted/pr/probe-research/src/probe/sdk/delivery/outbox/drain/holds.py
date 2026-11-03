"""ops held back on purpose: a run's close hold and the takeover holds a relaunch leaves, restored when it died."""

from __future__ import annotations
import json
import os
import time
from pathlib import Path

from .....foundation.os_backend import os_backend as oscompat
from .....foundation.durable.durable import (
    fsync_directory,
    write_text_atomic)


#: How long a run's close waits for the run's writes queued under another credential
#: (`drain`). Past it the close goes: a run left open forever over writes nothing here may
#: send is worse than a close landing first. Under the server's reaper window (900 s stale +
#: up to 120 s between sweeps), so a held close lands before the run can be marked crashed
#: (#2041 round 5).
CLOSE_HOLD_MAX_SECONDS = 600.0


def _close_hold_left(op: dict) -> float | None:
    """Seconds until ``op``'s close hold expires, or None when unknown."""
    from datetime import datetime, timezone

    try:
        queued = datetime.fromisoformat(str(op.get("enqueued_at") or ""))
    except ValueError:
        return None
    if queued.tzinfo is None:
        queued = queued.replace(tzinfo=timezone.utc)
    return CLOSE_HOLD_MAX_SECONDS - (datetime.now(timezone.utc) - queued).total_seconds()


def _close_hold_expired(op: dict) -> bool:
    from datetime import datetime, timezone

    try:
        queued = datetime.fromisoformat(str(op.get("enqueued_at") or ""))
    except ValueError:
        return True
    if queued.tzinfo is None:
        queued = queued.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - queued).total_seconds() > CLOSE_HOLD_MAX_SECONDS


def hold_abandoned(hold: dict, *, now: float | None = None) -> bool:
    """Whether the relaunch that set ``hold`` can no longer release it: its deadline passed or,
    on this host, its process is gone. A relaunch killed hard mid-barrier left the incumbent's
    close aside until another barrier ran on the same box (review of #2019)."""
    if float(hold.get("until") or 0) < (time.time() if now is None else now):
        return True
    try:
        import socket

        same_host = hold.get("host") == socket.gethostname()
    except OSError:
        same_host = False
    if not same_host:
        return False
    try:
        oscompat.probe_pid(int(hold.get("pid")))
    except ProcessLookupError:
        return True
    except (PermissionError, TypeError, ValueError, OverflowError):
        return False  # alive under another user, or unreadable: keep the hold
    return False


def restore_held_op(journal: "Journal", path: Path, op: dict) -> bool:
    """Put one held status op back in the queue at its original position (its file name keeps
    its enqueue order), as before the hold."""
    hold = op.pop(TAKEOVER_HOLD_KEY, None)
    if not isinstance(hold, dict):
        return False
    op["last_error"] = hold.get("last_error")
    if hold.get("blocking") is None:
        op.pop("blocking", None)
    else:
        op["blocking"] = hold["blocking"]
    write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
    os.replace(path, journal.ops_dir / path.name)
    fsync_directory(journal.ops_dir)
    fsync_directory(path.parent)
    return True


def restore_abandoned_holds(journal: "Journal") -> list[str]:
    """Put back every held status op whose relaunch died (`hold_abandoned`). One `stat` (the
    marker) when nothing is held, so every drain pass and new client runs it: the detached
    worker delivers an abandoned close within one pass instead of the reaper calling the run
    `crashed` first. The marker goes once nothing is held."""
    if not journal.holds_marker.exists():
        return []
    restored: list[str] = []
    still_held = False
    for path, op in journal.failed():
        hold = op.get(TAKEOVER_HOLD_KEY)
        if not isinstance(hold, dict):
            continue
        if not hold_abandoned(hold):
            still_held = True
            continue
        try:
            if restore_held_op(journal, path, op):
                restored.append(path.name)
        except OSError:
            still_held = True
    if not still_held:
        try:
            journal.holds_marker.unlink()
        except OSError:
            pass
    return restored
from probe.sdk.delivery.journal.journal import Journal  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import TAKEOVER_HOLD_KEY  # noqa: E402 -- pieces need each other; the front door loads this one first
