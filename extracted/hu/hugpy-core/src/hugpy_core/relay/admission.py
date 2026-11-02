"""Worker admission (2026-10-04). In the new build, joining is gated by box
enrollment (toolserver tokens) and a worker's presence lock proves it is the
enrolled box — so a registered worker is "approved" by default. The operator can
still BLOCK a worker (never routed to) and ADMIT it back; the decision lives in
hugpy_core.worker_admission so it survives restarts. Reads are cached briefly."""
from __future__ import annotations
from hugpy_core.imports import functions as _F

import os
import threading
import time

DB = _F.core_dsn()
_TTL = 2.0
_lock = threading.Lock()
_cache = {"at": 0.0, "states": {}}


def _db():
    import psycopg
    return psycopg.connect(DB, autocommit=True, connect_timeout=5)


def states() -> dict:
    """{worker_id: 'approved'|'blocked'} for workers with an explicit decision."""
    with _lock:
        if time.time() - _cache["at"] < _TTL:
            return _cache["states"]
    try:
        with _db() as c:
            got = {r[0]: r[1] for r in c.execute("SELECT worker_id, state FROM worker_admission").fetchall()}
    except Exception:  # noqa: BLE001 — unreachable DB: nobody is blocked (fail open, like presence)
        got = {}
    with _lock:
        _cache.update(at=time.time(), states=got)
    return got


def state_of(worker_id: str) -> str:
    return states().get(worker_id, "approved")


def is_blocked(worker_id: str) -> bool:
    return state_of(worker_id) == "blocked"


def set_state(worker_id: str, state: str, by: str = "operator", note: str = "") -> str:
    with _db() as c:
        c.execute("INSERT INTO worker_admission (worker_id, state, by_who, note) VALUES (%s,%s,%s,%s)"
                  " ON CONFLICT (worker_id) DO UPDATE SET state=EXCLUDED.state, at=now(),"
                  " by_who=EXCLUDED.by_who, note=EXCLUDED.note", (worker_id, state, by, note or None))
    with _lock:
        _cache["at"] = 0.0
    return state
