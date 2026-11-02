"""Verdicts are events (operator 2026-10-06: "the entire system was to be db
centric, with event driven changes").

Every measurement table in hugpy_wrapper (gguf_projection, kv_structure,
cuda_context, tf_structure, tf_measure, call_log) fires NOTIFY 'facts'
{table, worker} from its facts_notify trigger. Until now nobody in core
listened: a pair's verdict was re-derived only when the worker's budgets or a
file signature changed, so measurements landed and the plan never moved.

One LISTEN thread: a notification for a worker re-plans that worker from the
DB facts (planner.replan -> the same sizing.decide the wrapper places with),
coalescing a burst (a dry-run fill writes several rows) into one plan.

A call_log notification is not a measurement, but it is the grader's event:
grades derive from the call log (grader.fill_from_call_log), so a call landing
schedules one fill once the call has settled — and one at start, for the
grading calls an earlier core process answered but never recorded.
"""
from __future__ import annotations

import logging
import threading
import time

logger = logging.getLogger("hugpy_core.facts_listener")

DEBOUNCE_S = 2.0
_lock = threading.Lock()
_started = [False]
_pending: dict = {}          # worker name -> last notify time
_calls = {"last": 0.0, "due": 0.0}   # last call_log notify, when the next grade fill runs


def _fill_grades() -> None:
    from hugpy_core.grading import grader
    try:
        n = grader.fill_from_call_log()
        if n:
            logger.info("grader: %d grade(s) filled from the call log", n)
    except Exception:  # noqa: BLE001 — a fill fault never stops the listener
        logger.exception("grader: fill from the call log failed")


def _loop() -> None:
    import json
    import psycopg
    from hugpy_core.brain import planner
    from hugpy_core.calllog.calllog_db import dsn
    from hugpy_core.grading.grader import FILL_SETTLE_S
    from hugpy_core.imports.functions import listen_channel
    _calls["due"] = time.time() + FILL_SETTLE_S
    while True:
        try:
            with psycopg.connect(dsn(), autocommit=True) as conn:
                chan = listen_channel(conn, "facts")
                logger.info("listening on '%s'", chan)
                while True:
                    for n in conn.notifies(timeout=DEBOUNCE_S):
                        try:
                            p = json.loads(n.payload or "{}") or {}
                        except ValueError:
                            p = {}
                        # call_log fires 'facts' on every call (history ctx); a
                        # verdict is a measurement question — re-plan on the
                        # measurement tables only, not per call
                        name = p.get("worker") if p.get("table") != "call_log" else None
                        if name:
                            with _lock:
                                _pending[name] = time.time()
                        elif p.get("table") == "call_log":
                            _calls["last"] = time.time()
                            _calls["due"] = _calls["due"] or _calls["last"] + FILL_SETTLE_S
                    now = time.time()
                    with _lock:
                        due = [w for w, t in _pending.items() if now - t >= DEBOUNCE_S]
                        for w in due:
                            _pending.pop(w, None)
                    for w in due:
                        planner.replan(w)
                    if _calls["due"] and now >= _calls["due"]:
                        # calls that landed inside this fill's settle window get the next one
                        _calls["due"] = _calls["last"] + FILL_SETTLE_S if _calls["last"] > now - FILL_SETTLE_S else 0.0
                        _fill_grades()
        except Exception as exc:  # noqa: BLE001
            logger.warning("facts listener reconnect: %s", exc)
            time.sleep(2)


def ensure() -> None:
    with _lock:
        if _started[0]:
            return
        _started[0] = True
    threading.Thread(target=_loop, name="facts-listen", daemon=True).start()
