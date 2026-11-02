"""EVICTIONS feed: the console's Evictions tab + Models-tab eviction feed, read
from hugpy_wrapper.evictions (written by each box's fitevict evict-to-fit)
and pushed the moment a row lands or completes. The trigger in
sql/006_inference_engine_evictions_notify.sql (hugpy_wrapper DB) notifies 'evictions'; one LISTEN
thread re-reads the recent window and wakes every open stream. No polling.

Each row becomes the stage events the console's evictionFormat.js already
renders: ``evict.start`` and, once the process exited, ``evict.done``. A run
is the demanding call (``request_id``); its incoming model comes from the
call_log row with that request_id."""
from __future__ import annotations

import json
import threading
import time

from flask import Response, stream_with_context

from hugpy_core.calllog.calllog_db import dsn as _calllog_dsn
IE_DSN = _calllog_dsn()
WINDOW = 500
_cond = threading.Condition()
_state = {"version": 0, "events": []}
_started = [False]
_lock = threading.Lock()

_SQL = ("SELECT e.id, e.worker, e.key, e.engine, e.request_id, e.reason, e.process_bytes, "
        "e.free_before, e.free_after, e.freed_bytes, e.exit_s, e.release_s, "
        "extract(epoch from e.started_at)::float8, extract(epoch from coalesce(e.released_at, e.exited_at))::float8, "
        "c.model_name "
        "FROM evictions e LEFT JOIN call_log c ON c.request_id = e.request_id "
        "ORDER BY e.id DESC LIMIT %s")


def _events(rows) -> list:
    out = []
    for (rid, worker, key, engine, req, reason, pbytes, fbefore, fafter, freed,
         exit_s, release_s, started, ended, incoming) in reversed(rows):
        common = {"run_id": req or f"ev:{rid}", "worker_id": worker, "model_key": key,
                  "engine": engine, "reason": reason, "incoming_model": incoming,
                  "trigger": reason, "vram_bytes": pbytes}
        out.append({**common, "_id": f"{rid}:start", "stage": "evict.start", "ts": started,
                    "free_bytes": fbefore})
        if ended is not None:
            secs = release_s if release_s is not None else exit_s
            out.append({**common, "_id": f"{rid}:done", "stage": "evict.done", "ts": ended,
                        "freed_bytes": freed, "free_bytes": fafter,
                        "duration_ms": None if secs is None else secs * 1000.0})
    return out


def _read(c, limit: int = WINDOW) -> list:
    return _events(c.execute(_SQL, (limit,)).fetchall())


def _loop():
    import psycopg
    from hugpy_core.imports.functions import listen_channel
    while True:
        try:
            with psycopg.connect(IE_DSN, autocommit=True) as conn, psycopg.connect(IE_DSN, autocommit=True) as rc:
                listen_channel(conn, "evictions")
                while True:
                    evs = _read(rc)
                    with _cond:
                        _state["events"] = evs
                        _state["version"] += 1
                        _cond.notify_all()
                    list(conn.notifies(stop_after=1))
                    list(conn.notifies(timeout=0))      # coalesce a burst into one re-read
        except Exception as exc:  # noqa: BLE001
            print(f"[evictions] reconnect: {exc}")
            time.sleep(2)


def _ensure():
    with _lock:
        if not _started[0]:
            _started[0] = True
            threading.Thread(target=_loop, name="evictions-listen", daemon=True).start()


def evictions_stream():
    """SSE: a ready marker, the recent window, then each new/updated row's
    events the moment the trigger fires. Capped at an hour; the client re-attaches."""
    _ensure()

    def gen():
        sent: set = set()
        seen = -1
        yield "data: " + json.dumps({"stage": "stream.ready", "ts": time.time()}) + "\n\n"
        started = time.time()
        while time.time() - started < 3600:
            with _cond:
                if _state["version"] == seen:
                    _cond.wait(timeout=15)
                v, evs = _state["version"], _state["events"]
            if v == seen:
                yield ": keepalive\n\n"
                continue
            seen = v
            for ev in evs:
                if ev["_id"] in sent:
                    continue
                sent.add(ev["_id"])
                yield "data: " + json.dumps(ev, default=str) + "\n\n"
    return Response(stream_with_context(gen()), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


def evictions_list(limit=300):
    """The recent eviction window as console stage events (newest run last);
    ``limit`` rows (1..5000, default 300)."""
    import psycopg
    try:
        limit = max(1, min(int(limit or 300), 5000))
    except (TypeError, ValueError):
        limit = 300
    with psycopg.connect(IE_DSN, autocommit=True, connect_timeout=5) as conn:
        events = _read(conn, limit)
    return {"events": events, "count": len(events), "path": "hugpy_wrapper.evictions"}
