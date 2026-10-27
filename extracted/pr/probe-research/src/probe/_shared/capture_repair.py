"""Probe staff asked to repair this machine's session capture (research-os control/073).

A wizard bug could revoke a capture credential nobody turned off (a Settings
commit read a sign-in's pending lock as "capture off" and ran the full
turn-off; Anthrogen, 2026-10-26). Bringing it back used to need the person's
browser approval. Staff can now open a one-time repair for ONE device and its
agents, and the server answers that device's authenticated requests with
`X-Probe-Capture-Repair: <requested at, unix seconds>`. Whichever of our
clients gets that answer calls `note()`, which leaves `capture-repair-requested`
in the state folder; the next `probe` command reads it
(`probe.cli.main._capture_repair_notice`), fetches the replacement credentials
(`POST /v1/client/capture-repair`, which closes nothing), writes them where the
wizard's sign-in would, and confirms per agent
(`POST /v1/client/capture-repair/applied`); the request closes once every agent
is settled.

The same shape as `probe._shared.update_request`, for the same reasons: the
request that carries the header is often not a `probe` command, and a process
that saw the header once must not keep acting after the server stops sending
it. Bounded both ways, stdlib only, `probe.version_policy` loaded only once a
header arrives, never raises.
"""

from __future__ import annotations

import json
import time
from collections.abc import Mapping

#: The server's `app/client_version/capture_repairs.py::CAPTURE_REPAIR_HEADER`.
HEADER = "X-Probe-Capture-Repair"
#: The mark, beside `update-requested`.
FILENAME = "capture-repair-requested"
#: One process rewrites the mark at most this often.
WRITE_EVERY_S = 5 * 60
#: A mark older than this is not acted on: the server stopped sending it.
FRESH_S = 30 * 60
#: A value longer than this is not a unix time.
_MAX_DIGITS = 12

#: When this process last wrote the mark (monotonic seconds).
_last_write: float | None = None


def note(headers: Mapping[str, str]) -> None:
    """Leave the mark when an answer's `headers` carry the request. Never raises."""
    global _last_write
    try:
        raw = headers.get(HEADER)
        if not raw:
            return
        now = time.monotonic()
        if _last_write is not None and 0 <= now - _last_write < WRITE_EVERY_S:
            return
        if not (raw.isascii() and raw.isdigit() and len(raw) <= _MAX_DIGITS):
            return
        _last_write = now
        from probe import version_policy

        version_policy.atomic_write_json(
            version_policy.state_dir() / FILENAME,
            {"requested_at": int(raw), "seen_at": time.time()},
        )
    except Exception:  # noqa: BLE001 -- a mark may never fail the request it rode on
        pass


def fresh(now: float | None = None) -> bool:
    """A mark seen within `FRESH_S`. False when there is none. Never raises."""
    try:
        from probe import version_policy

        data = json.loads((version_policy.state_dir() / FILENAME).read_text())
        seen = float(data["seen_at"])
    except Exception:  # noqa: BLE001 -- no mark, an unreadable or a malformed one
        return False
    age = (time.time() if now is None else now) - seen
    return 0 <= age < FRESH_S


def clear() -> None:
    """The request was answered (or there is none): forget the mark. Never raises."""
    global _last_write
    try:
        from probe import version_policy

        (version_policy.state_dir() / FILENAME).unlink(missing_ok=True)
    except Exception:  # noqa: BLE001
        pass
    # A header still in flight in this process must be able to mark again.
    _last_write = None


def _reset_for_tests() -> None:
    global _last_write
    _last_write = None
