"""Probe staff asked this machine to update now (research-os control/071).

The server answers any authenticated request from a machine that has an open
request with `X-Probe-Update-Requested: <requested at, unix seconds>`. Whichever
of our clients gets that answer calls `note()`, which leaves `update-requested`
in the state folder; the next `probe` command reads it
(`probe.cli.main._remote_update_notice`) and hands an update to this machine's
own updater, under every rule that updater already has.

WHY A FILE AND NOT A CALLBACK. The request that carries the header is often not
a `probe` command: the manifest refresher's update-report flush, the Probe
service's own reports, an SDK run. The process that acts is the next `probe`
command, where the update gates already live, and a long-lived process that saw
the header once cannot keep a pending request from being retried.

BOUNDED BOTH WAYS. No header: one lookup, nothing else (a training loop calls
this on every request). A header: at most one write per `WRITE_EVERY_S` per
process. The mark says when it was last seen, and the CLI acts only on a FRESH
one (`FRESH_S`), so once the server stops sending it (the request was answered,
canceled or expired) the CLI stops asking within that.

Stdlib only, and `probe.version_policy` is loaded only once a header arrives:
the SDK transport imports this module, and `import probe` in a training script
must not pay for the state-folder code. Never raises.
"""

from __future__ import annotations

import json
import time
from collections.abc import Mapping

#: The server's `app/client_version/update_requests.py::UPDATE_REQUESTED_HEADER`.
HEADER = "X-Probe-Update-Requested"
#: The mark, beside `autoupdate.json`.
FILENAME = "update-requested"
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


def _reset_for_tests() -> None:
    global _last_write
    _last_write = None
