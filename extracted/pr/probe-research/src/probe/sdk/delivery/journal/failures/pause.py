"""pause and resume delivery with a marker file that expires, here or in a queue above."""

from __future__ import annotations
import json
import os
import time
from pathlib import Path
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
    """The pause marker in ``directory`` while in effect, else None: ``{"at", "until"}`` in UTC,
    ``until`` None holding until `probe outbox resume`.

    - An older CLI's marker (a bare timestamp from when a pause never ended, or anything not a
      JSON object) is over: an update releases what it held at once (Richard, 2026-10-26) and
      `lift_stale_pause` deletes it. A pause an older CLI still on the machine types later is
      over too, the price of that.
    - A JSON object holds until its `until` (None: until resume). One whose `until` is missing
      or unreadable (a newer release's shape) holds DEFAULT_PAUSE_HOURS from its `at`, else from
      when it was written: never ended early here.
    - One that cannot be read (permissions, I/O, a symlink, not a regular file) holds,
      `{"at": None, "until": None}`: unknown is paused, and only `resume` deletes it.

    Never raises: this runs on every append and before every CLI command (one open when none)."""
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
from probe.sdk.delivery.ops.ops import CREDENTIAL_NAMESPACE, DELIVERY_NAMESPACE  # noqa: E402 -- pieces need each other; the front door loads this one first
