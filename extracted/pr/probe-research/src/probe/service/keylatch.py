"""The capture tap's 401 latch, written by the Probe service.

Every surface that says "the key was refused" reads one stamp: `last_401_at`
(and `last_401_token_sha256`, the refused credential's sha256) in the tap's
state db `meta` table -- the status line (`statusline_refresh._halted`),
`probe session status` and `probe doctor` (`capture_state._halted`), `tap
status`. Only the tap's old outbox drain still writes it; the journal path
every tap since 0.4.5 delivers through never does, so a refused key read as
"not recording" at best and the person was never told to reconnect (release
gate, 2026-10-25).

`install(tap)` wraps the loaded tap's `Wire._request` once: an answer of 401
from the Probe gateway (FastAPI's `{"detail": ...}`, never a proxy's page)
stamps the latch for that credential; a 2xx answer for the same credential
clears a stamp it left. A new credential (re-pairing) is never latched by an
old stamp, as `capture_state._halted` already compares the fingerprint.
Writes happen only when the state changes. Never raises into capture.

Stdlib only; imported when the service loads a tap.
"""

from __future__ import annotations

import hashlib
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any, Callable

STAMP = "last_401_at"
FINGERPRINT = "last_401_token_sha256"
_MARK = "_probe_keylatch"
#: What each (source, fingerprint) last stamped: True latched, False cleared.
_SEEN: dict[tuple[str, str], bool] = {}
_LOCK = threading.Lock()


def fingerprint(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def state_db(source: str) -> Path | None:
    """The tap's state db for `source`, as `capture_state._halted` finds it."""
    try:
        from probe.harness import get_registry

        capture = get_registry().get(source).capture
        return None if capture is None else Path(capture.state_dir()) / "state.db"
    except Exception:  # noqa: BLE001 -- an unknown source has no latch to write
        return None


def _gateway_refusal(code: object, body: object) -> bool:
    detail = body.get("detail") if isinstance(body, dict) else None
    gateway = isinstance(detail, list) or (isinstance(detail, str) and detail != "invalid error response")
    return code == 401 and gateway


def _write(db: Path, *, stamp: bool, fp: str) -> bool:
    """Stamp (or clear) the latch in `db`'s existing `meta` table. True when
    it was written. Never creates the db or the table: that is the tap's."""
    if not db.is_file():
        return False
    try:
        conn = sqlite3.connect(db, timeout=1.0)
    except sqlite3.Error:
        return False
    try:
        with conn:
            if stamp:
                at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                conn.execute("INSERT OR REPLACE INTO meta (k, v) VALUES (?, ?)", (STAMP, at))
                conn.execute("INSERT OR REPLACE INTO meta (k, v) VALUES (?, ?)", (FINGERPRINT, fp))
            else:
                row = conn.execute("SELECT v FROM meta WHERE k = ?", (FINGERPRINT,)).fetchone()
                if row is not None and row[0] != fp:
                    return False  # another credential's stamp: not ours to clear
                conn.execute("DELETE FROM meta WHERE k IN (?, ?)", (STAMP, FINGERPRINT))
        return True
    except sqlite3.Error:
        return False
    finally:
        conn.close()


def note(source: str, token: str, code: object, body: object, db: Path | None = None) -> None:
    """Record what the gateway answered a request made with `token`."""
    if not isinstance(source, str) or not isinstance(token, str) or not token:
        return
    if _gateway_refusal(code, body):
        latched = True
    elif isinstance(code, int) and 200 <= code < 300:
        latched = False
    else:
        return  # offline, 5xx, a proxy: says nothing about the key
    fp = fingerprint(token)
    key = (source, fp)
    with _LOCK:
        if _SEEN.get(key) is latched:
            return
    path = db if db is not None else state_db(source)
    if path is None:
        return
    if _write(path, stamp=latched, fp=fp) or not latched:
        with _LOCK:
            _SEEN[key] = latched


def install(tap: Any, log: Callable[[str], None] = lambda _m: None) -> bool:
    """Wrap the loaded tap's `Wire._request` (once). True when wrapped."""
    sj = getattr(tap, "session_journal", None) or getattr(tap, "sj", None)
    wire = getattr(sj, "Wire", None)
    request = getattr(wire, "_request", None)
    if wire is None or not callable(request):
        return False
    if getattr(request, _MARK, False):
        return True

    def _request(self: Any, *args: Any, **kwargs: Any) -> Any:
        answer = request(self, *args, **kwargs)
        try:
            code, body = answer
            note(getattr(self, "source", None), getattr(self, "token", None), code, body)
        except Exception:  # noqa: BLE001 -- never into capture
            pass
        return answer

    setattr(_request, _MARK, True)
    wire._request = _request
    log("key latch: a refused key is recorded where the status line and doctor read it")
    return True
