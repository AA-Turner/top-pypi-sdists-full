"""A Probe staff request for THIS machine, heard on an answer header, left as a mark file for a later `probe` command.

research-os control/071, 073, 074. Stdlib only; never raises. Headers, why a file, the bounds: DESIGN.md.
"""

from __future__ import annotations

import json
import time
from collections.abc import Mapping
from pathlib import Path

#: One process rewrites a mark at most this often.
WRITE_EVERY_S = 5 * 60
#: A mark older than this is not acted on: the server stopped sending it.
FRESH_S = 30 * 60
#: A value longer than this is not a unix time.
_MAX_DIGITS = 12


class Mark:
    """One staff request's header and the mark file it leaves."""

    def __init__(self, header: str, filename: str) -> None:
        self.header = header
        self.filename = filename
        #: When this process last wrote the mark (monotonic seconds).
        self._last_write: float | None = None

    def note(self, headers: Mapping[str, str]) -> None:
        """Leave the mark when an answer's `headers` carry the request. Never raises."""
        try:
            raw = headers.get(self.header)
            if not raw:
                return
            now = time.monotonic()
            if self._last_write is not None and 0 <= now - self._last_write < WRITE_EVERY_S:
                return
            if not (raw.isascii() and raw.isdigit() and len(raw) <= _MAX_DIGITS):
                return
            self._last_write = now
            from probe.foundation.version_policy import version_policy

            version_policy.atomic_write_json(
                version_policy.state_dir() / self.filename,
                {"requested_at": int(raw), "seen_at": time.time()},
            )
        except Exception:  # noqa: BLE001 -- a mark may never fail the request it rode on
            pass

    def fresh(self, now: float | None = None, *, folder: Path | None = None) -> bool:
        """A mark seen within `FRESH_S`, in `folder` (another caller context's state folder: the
        Probe service's chores), else this process's. False when there is none. Never raises."""
        try:
            from probe.foundation.version_policy import version_policy

            data = json.loads(((folder or version_policy.state_dir()) / self.filename).read_text())
            seen = float(data["seen_at"])
        except Exception:  # noqa: BLE001 -- no mark, an unreadable or a malformed one
            return False
        age = (time.time() if now is None else now) - seen
        return 0 <= age < FRESH_S

    def clear(self) -> None:
        """The request was answered (or there is none): forget the mark. Never raises."""
        try:
            from probe.foundation.version_policy import version_policy

            (version_policy.state_dir() / self.filename).unlink(missing_ok=True)
        except Exception:  # noqa: BLE001
            pass
        # A header still in flight in this process must be able to mark again.
        self._last_write = None

    def reset_for_tests(self) -> None:
        self._last_write = None


def note_all(headers: Mapping[str, str]) -> None:
    """Leave the mark of every staff request an answer's `headers` carry: one
    lookup per request kind when none does. Never raises."""
    from probe.foundation.remote_settings import capture_repair, preferences as settings_request, update as update_request

    for mark in (update_request.MARK, capture_repair.MARK, settings_request.MARK):
        mark.note(headers)
