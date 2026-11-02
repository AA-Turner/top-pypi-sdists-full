"""MODEL ROWS: each model's per-box state for the console's Models table, read
from the wrapper's own rows in hugpy_wrapper — ``models`` (the file is on
that box's drive) and ``residents`` (a seat: loading / idle / busy / error).

GET /llm/models/status seeds every model's ``workers`` from one read; after that
only ACTIONS move it: the triggers in sql/007_inference_engine_model_rows_notify.sql (hugpy_wrapper DB)
notify 'model_rows' with the (worker, key) an action touched, one LISTEN thread
reads that pair and pushes it on /llm/models/rows/stream. No status search.

A knob change OR a planner re-plan is likewise an event (operator 2026-10-06:
"moe-tick is an event"): sql/014_model_workers_knob_notify.sql (hugpy_core DB)
NOTIFYs the SAME 'model_rows' channel when model_workers.user_settings/plan or a
model_worker_quants verdict changes. pg_notify is per-DB, so a second LISTEN
thread (_loop_core) reads the core DB and pushes a pair event enriched with
user_settings + plan + the verdict's auto variants (so the console SELECTS the
Alloc / Memory variant, never recomputes), plus the current serving chip so the
Models-table consumer stays a harmless re-add."""
from __future__ import annotations
from hugpy_core.imports import functions as _F

import collections
import json
import os
import threading
import time

from flask import Response, request, stream_with_context

from hugpy_core.registry import registry

from hugpy_core.calllog.calllog_db import dsn as _calllog_dsn
IE_DSN = _calllog_dsn()
# The pair knobs + verdicts live in the CORE DB (model_workers / model_worker_quants).
# A knob change NOTIFYs 'model_rows' there (sql/011_model_workers_knob_notify.sql);
# a second LISTEN loop reads it and pushes the pair, so a toggle reaches the UI
# without a refetch. pg_notify is per-DB, so this needs its own connection.
CORE_DSN = _F.core_dsn()
_PAIR_SQL = ("SELECT coalesce(m.worker, r.worker), coalesce(m.key, r.key), m.path IS NOT NULL, "
             "r.state, r.busy, r.loading, r.load_error, r.quant, r.n_gpu_layers, r.total_layers, r.ctx, "
             "coalesce(r.engine, m.engine) "
             "FROM worker_model_copies m FULL JOIN residents r ON r.worker = m.worker AND r.key = m.key")
_cond = threading.Condition()
_events: "collections.deque" = collections.deque(maxlen=500)   # (seq, event)
_seq = [0]
_started = [False]
_lock = threading.Lock()
_pending: dict = {}            # (model_key, worker) -> latest whole-row event
_pending_timers: dict = {}
_pending_lock = threading.Lock()
_COALESCE_S = 0.10


def _flush_pair(pair) -> None:
    with _pending_lock:
        ev = _pending.pop(pair, None)
        _pending_timers.pop(pair, None)
    if ev is None:
        return
    with _cond:
        _seq[0] += 1
        _events.append((_seq[0], ev))
        _cond.notify_all()


def _publish(ev: dict) -> None:
    """Collapse one DB trigger burst into the pair's latest complete row.

    A copy/resident change can immediately cause a plan and several quant rows
    to change. Those are one UI row transition, not N stream messages.
    """
    pair = (ev.get("model_key"), ev.get("worker_id") or ev.get("worker"))
    if not all(pair):
        return
    with _pending_lock:
        _pending[pair] = {**_pending.get(pair, {}), **ev}
        if pair in _pending_timers:
            return
        timer = threading.Timer(_COALESCE_S, _flush_pair, args=(pair,))
        timer.daemon = True
        _pending_timers[pair] = timer
        timer.start()


def _known_workers() -> "set | None":
    try:
        names = {w.get("name") for w in registry.all_workers()} - {None}
    except Exception:  # noqa: BLE001
        return None
    return names or None


def _chip(row) -> "tuple[str, str, dict]":
    """(model_key, worker, chip) in the console's workerChips vocabulary."""
    worker, key, on_drive, state, busy, loading, err, quant, ngl, layers, ctx, engine = row
    if state is None:
        st, detail = ("cold" if on_drive else "n/a"), ("on this box's drive" if on_drive else "")
    elif state == "error" or err:
        st, detail = "failed", err or "load failed"
    elif loading or state == "loading":
        st, detail = "loading", "loading"
    elif busy:
        st, detail = "answering", "answering a call"
    else:
        st, detail = "serving", "resident"
    if state is not None and state != "error":
        bits = [b for b in (engine, quant, f"ctx {ctx}" if ctx else None,
                            (f"gpu layers {'all' if ngl is not None and ngl < 0 else ngl}"
                             f"{'/' + str(layers) if layers else ''}") if ngl is not None else None) if b]
        detail = " · ".join([detail] + bits)
    return key, worker, {"worker": worker, "state": st, "base": st, "label": st, "detail": detail}


def workers_by_model() -> dict:
    """{model_key: [chip, ...]} for every registered box (one read: the seed)."""
    import psycopg
    known = _known_workers()
    out: dict = {}
    with psycopg.connect(IE_DSN, autocommit=True, connect_timeout=5) as c:
        for row in c.execute(_PAIR_SQL).fetchall():
            key, worker, chip = _chip(row)
            if known is not None and worker not in known:
                continue
            out.setdefault(key, []).append(chip)
    return out


def _pair(c, worker: str, key: str) -> "dict | None":
    row = c.execute(_PAIR_SQL + " WHERE coalesce(m.worker, r.worker) = %s AND coalesce(m.key, r.key) = %s",
                    (worker, key)).fetchone()
    return _chip(row)[2] if row else None


_VERDICT_SQL = ("SELECT file, auto, memory, moe_offered FROM model_worker_quants"
                " WHERE worker_id = %s AND model_key = %s ORDER BY file")


def _pair_event(core_c, wrap_c, worker_id: str, key: str) -> "dict | None":
    """One pair's whole UI row from the CORE DB (knobs + plan + verdicts), enriched
    with the box's current serving chip from the wrapper DB, so the console SELECTS
    the Alloc / Memory / verdict variant for the knob state and never recomputes.

    worker_id -> worker NAME: the Models-table consumer (patchChip) keys chips by
    name and re-adds ``chip`` under it, so carrying the current chip under the name
    keeps that consumer a harmless no-op; the Workers panel reads worker_id +
    user_settings + plan + verdicts. None when the pair row is gone."""
    row = core_c.execute("SELECT m.user_settings, p.plan, m.assigned, m.pinned, m.fits, m.source, m.env_profile FROM model_workers m LEFT JOIN model_pair_plans p USING(model_key,worker_id)"
                         " WHERE worker_id = %s AND model_key = %s", (worker_id, key)).fetchone()
    if row is None:
        return None
    us, plan = (row[0] or {}), (row[1] or {})
    verdicts = [{"file": f, "auto": a, "memory": m, "moe_offered": bool(mo)}
                for (f, a, m, mo) in core_c.execute(_VERDICT_SQL, (worker_id, key)).fetchall()]
    live_row = core_c.execute("SELECT file,mode,gpu_fit,ram_fit,gpu_bytes,ram_bytes,room_gpu,room_ram,"
                              "room_swap,why,source,computed_at FROM pair_live WHERE worker_id=%s AND model_key=%s",
                              (worker_id, key)).fetchone()
    live = dict(zip(("file", "mode", "gpu_fit", "ram_fit", "gpu_bytes", "ram_bytes", "room_gpu",
                     "room_ram", "room_swap", "why", "source", "computed_at"), live_row)) if live_row else None
    w = registry.lookup_worker(worker_id)
    name = (w or {}).get("name")
    chip = _pair(wrap_c, name, key) if name else None
    return {"model_key": key, "worker": name or worker_id, "worker_id": worker_id,
            "chip": chip, "user_settings": us, "effective_settings": _F.effective_pair_settings(us),
            "plan": plan, "assigned": row[2], "pinned": row[3], "fits": row[4],
            "source": row[5], "env_profile": row[6], "verdicts": verdicts, "live": live}


def _loop_core():
    """LISTEN 'model_rows' on the CORE DB (sql/014 triggers fire it on a knob or a
    planner re-plan). pg_notify is per-DB, so this is a separate connection from the
    wrapper loop; both feed the one SSE deque. One extra read connection prices the
    pair, one wrapper read connection reads the current chip."""
    import psycopg
    while True:
        try:
            with psycopg.connect(CORE_DSN, autocommit=True) as conn, \
                 psycopg.connect(CORE_DSN, autocommit=True) as cc, \
                 psycopg.connect(IE_DSN, autocommit=True) as rc:
                _F.listen_channel(conn, "model_rows")
                for n in conn.notifies():
                    try:
                        p = json.loads(n.payload)
                    except ValueError:
                        continue
                    if p.get("table") not in ("model_workers", "model_worker_quants", "pair_live"):
                        continue
                    worker_id, key = p.get("worker"), p.get("key")
                    if not worker_id or not key:
                        continue
                    if p.get("table") == "pair_live":
                        live_row = cc.execute("SELECT file,mode,gpu_fit,ram_fit,gpu_bytes,ram_bytes,room_gpu,"
                                              "room_ram,room_swap,why,source,computed_at FROM pair_live "
                                              "WHERE worker_id=%s AND model_key=%s", (worker_id, key)).fetchone()
                        if live_row:
                            live = dict(zip(("file", "mode", "gpu_fit", "ram_fit", "gpu_bytes", "ram_bytes",
                                             "room_gpu", "room_ram", "room_swap", "why", "source", "computed_at"), live_row))
                            _publish({"model_key": key, "worker_id": worker_id, "live": live,
                                      "action": "pair_live.update", "ts": time.time()})
                        continue
                    pe = _pair_event(cc, rc, worker_id, key)
                    if pe is None:
                        continue
                    known = _known_workers()
                    if known is not None and pe["worker"] not in known and worker_id not in known:
                        continue
                    ev = {**pe, "action": f"{p.get('table')}.{p.get('op', '').lower()}", "ts": time.time()}
                    _publish(ev)
                    if p.get("table") in ("model_workers", "model_worker_quants"):
                        from hugpy_core.brain import gpu_live
                        gpu_live.schedule(worker_id, pair_change=True)
        except Exception as exc:  # noqa: BLE001
            print(f"[model_rows] core reconnect: {exc}")
            time.sleep(2)


_resync_pending: set = set()
_resync_lock = threading.Lock()


def _resync_soon(worker: str) -> None:
    """A model landed on / left a box's drive (hugpy_wrapper.models): ask that
    box's worker to re-report now (it LISTENs on hugpy_worker_cfg, like after a
    core restart), so core's catalog and the engine registry follow without a
    manual nudge. A discovery burst (many rows) coalesces into one notify."""
    with _resync_lock:
        if worker in _resync_pending:
            return
        _resync_pending.add(worker)

    def fire():
        with _resync_lock:
            _resync_pending.discard(worker)
        try:
            registry.pg_notify("hugpy_worker_cfg", json.dumps({"resync": "models", "worker": worker}))
        except Exception as exc:  # noqa: BLE001
            print(f"[model_rows] resync notify failed: {exc}")
    threading.Timer(1.0, fire).start()


def _loop():
    import psycopg
    while True:
        try:
            with psycopg.connect(IE_DSN, autocommit=True) as conn, psycopg.connect(IE_DSN, autocommit=True) as rc:
                _F.listen_channel(conn, "model_rows")
                for n in conn.notifies():
                    try:
                        p = json.loads(n.payload)
                    except ValueError:
                        continue
                    if p.get("table") in ("model_workers", "model_worker_quants", "pair_live"):
                        continue        # core's own pair rows: _loop_core pushes them whole (one DB
                                        # holds both when the intake mirrors the box into core's DB)
                    worker, key = p.get("worker"), p.get("key")
                    if p.get("table") in ("models", "worker_model_copies") and worker:
                        _resync_soon(worker)        # the box's drive changed: its catalog must follow
                    known = _known_workers()
                    if not worker or not key or (known is not None and worker not in known):
                        continue
                    ev = {"model_key": key, "worker": worker, "chip": _pair(rc, worker, key),
                          "action": f"{p.get('table')}.{p.get('op', '').lower()}", "ts": time.time()}
                    _publish(ev)
        except Exception as exc:  # noqa: BLE001
            print(f"[model_rows] reconnect: {exc}")
            time.sleep(2)


def _ensure():
    with _lock:
        if not _started[0]:
            _started[0] = True
            threading.Thread(target=_loop, name="model-rows-listen", daemon=True).start()
            threading.Thread(target=_loop_core, name="model-rows-core-listen", daemon=True).start()




def model_rows_stream():
    """SSE: one event per action row ({model_key, worker, chip, action}); chip null =
    that box no longer holds the model at all. Capped at an hour; the client re-attaches
    and re-seeds from GET /llm/models/status."""
    _ensure()

    last_id = request.headers.get("Last-Event-ID", "").strip()

    def gen():
        with _cond:
            current = _seq[0]
            oldest = _events[0][0] if _events else current + 1
        try:
            requested = int(last_id) if last_id else None
        except ValueError:
            requested = None
        can_replay = requested is not None and oldest - 1 <= requested <= current
        sent = requested if can_replay else current
        reset = requested is not None and not can_replay
        yield "data: " + json.dumps({"stage": "stream.ready", "reset": reset,
                                     "ts": time.time()}) + "\n\n"
        started = time.time()
        while time.time() - started < 3600:
            with _cond:
                if _seq[0] == sent:
                    _cond.wait(timeout=15)
                fresh = [(s, ev) for s, ev in _events if s > sent]
                if fresh:
                    sent = fresh[-1][0]
            if not fresh:
                yield ": keepalive\n\n"
                continue
            for seq, ev in fresh:
                yield f"id: {seq}\ndata: " + json.dumps(ev, default=str) + "\n\n"
    return Response(stream_with_context(gen()), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})
