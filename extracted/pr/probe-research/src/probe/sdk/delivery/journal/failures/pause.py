"""pause and resume delivery with a marker file that expires, here or in a queue above."""

from __future__ import annotations

import json
import os
from pathlib import Path
import time

from probe.foundation.durable.durable import file_lock, write_text_atomic
#: How long `probe outbox pause` holds delivery unless told otherwise. A pause had no end:
#: nothing resumed it and every write the machine made afterwards (runs, files, metrics) queued
#: silently behind it (Tokenless, 2026-10-26: a pause typed right after an aborted import held
#: its 800 writes and everything after).
DEFAULT_PAUSE_HOURS = 24.0
#: The longest `probe outbox pause --hours` (a year); `--until-resume` is longer.
MAX_PAUSE_HOURS = 24.0 * 365
PAUSE_SCHEMA = "probe.outbox.pause/1"
#: A marker is a few dozen bytes; no more than this is ever read of one.
_PAUSE_MARKER_MAX = 4096


def _parse_when(value):
    from datetime import datetime, timezone

    try:
        when = datetime.fromisoformat(str(value or ""))
    except ValueError:
        return None
    return when if when.tzinfo else when.replace(tzinfo=timezone.utc)


def _pause_marker(directory: Path) -> dict | None:
    """The pause marker in ``directory`` while in effect (``{"at", "until"}`` UTC, ``until`` None until
    `probe outbox resume`), else None. An older CLI's marker is over; an unreadable one holds.
    Never raises."""
    import stat
    from datetime import datetime, timedelta, timezone

    unreadable = {"at": None, "until": None}
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    try:
        fd = os.open(directory / "paused", flags)
    except (FileNotFoundError, NotADirectoryError):
        return None
    except OSError:
        return unreadable
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_size > _PAUSE_MARKER_MAX:
            return unreadable
        raw = os.read(fd, _PAUSE_MARKER_MAX)
    except OSError:
        return unreadable
    finally:
        os.close(fd)
    try:
        record = json.loads(raw.decode("utf-8"))
    except ValueError:  # not UTF-8, or not JSON: an older CLI's bare timestamp
        return None
    if not isinstance(record, dict):
        return None
    try:
        at = _parse_when(record.get("at")) or datetime.fromtimestamp(info.st_mtime, timezone.utc)
        if "until" in record and record["until"] is None:
            until = None
        else:
            until = _parse_when(record.get("until")) or at + timedelta(hours=DEFAULT_PAUSE_HOURS)
            if until <= datetime.now(timezone.utc):
                return None
        return {
            "at": at.astimezone(timezone.utc).isoformat(),
            "until": until.astimezone(timezone.utc).isoformat() if until else None,
        }
    except (ValueError, OverflowError):  # a date past the calendar's end
        return unreadable


def _unlink_pause(path: Path) -> None:
    """Delete a pause marker. On Windows a reader's open handle blocks a delete for the moment
    it reads: retried, as `oscompat.replace` is."""
    give_up = time.monotonic() + 1.0
    while True:
        try:
            path.unlink(missing_ok=True)
            return
        except PermissionError:
            if os.name != "nt" or time.monotonic() >= give_up:
                raise
            time.sleep(0.01)


def _pause_in_effect(directory: Path) -> dict | None:
    """The pause holding ``directory``: its own, or one above it (`probe outbox pause` pauses
    the root and with it every namespace under it)."""
    path = directory
    while True:
        marker = _pause_marker(path)
        if marker is not None:
            return marker
        if path.name == DELIVERY_NAMESPACE:
            path = path.parent
        elif path.parent.name == CREDENTIAL_NAMESPACE:
            path = path.parent.parent
        else:
            return None


class PauseMixin:
    """Part of Journal: its methods run with `self` the Journal; fold_parts() copies them into Journal."""

    @property
    def paused(self) -> bool:
        """Paused here, or in any queue above this one (`probe outbox pause` pauses the root and
        every namespace under it), by a pause that has not run out (`DEFAULT_PAUSE_HOURS`)."""
        return _pause_in_effect(self.dir) is not None

    def pause(self, hours: float | None = DEFAULT_PAUSE_HOURS) -> dict:
        """Hold delivery for ``hours``, or until `resume` when None. Returns the marker. Written
        under the append lock, so `lift_stale_pause` never removes a pause written while it looked."""
        from datetime import datetime, timedelta, timezone

        self._ensure()
        at = datetime.now(timezone.utc)
        until = None if hours is None else (at + timedelta(hours=hours)).isoformat()
        marker = {"schema": PAUSE_SCHEMA, "at": at.isoformat(), "until": until}
        with file_lock(self.append_lock):
            write_text_atomic(self.paused_file, json.dumps(marker) + "\n", mode=0o600)
            self._write_status_locked()
        return marker

    def lift_stale_pause(self, *, wait: bool = True) -> bool:
        """Delete this queue's pause marker once it no longer holds: its end passed, or it is an
        older CLI's endless one. An older release reads only whether the marker EXISTS (an SDK
        pinned in a job's venv), so it stays paused until the file is gone. An older CLI's `pause`
        writes outside the append lock, so one typed in the microseconds between this check and
        the unlink is lost. ``wait`` False: when another process holds the append lock, lift
        nothing now (for a caller that must never hang on a stopped writer's lock: the Probe
        service). True when one was lifted."""
        if not os.path.lexists(self.paused_file) or _pause_marker(self.dir) is not None:
            return False
        lock = file_lock(self.append_lock) if wait else _try_lock(self.append_lock)
        with lock as held:
            if held is False:
                return False
            if not os.path.lexists(self.paused_file) or _pause_marker(self.dir) is not None:
                return False
            _unlink_pause(self.paused_file)
            self._write_status_locked()
        return True

    def resume(self) -> None:
        for child in self.namespaces()[1:]:
            child.resume()
        _unlink_pause(self.paused_file)
        if self.dir.exists():
            with file_lock(self.append_lock):
                self._write_status_locked()

from probe.sdk.delivery.ops.ops import CREDENTIAL_NAMESPACE, DELIVERY_NAMESPACE  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.item_locks import _try_lock  # noqa: E402 -- pieces need each other; the front door loads this one first
