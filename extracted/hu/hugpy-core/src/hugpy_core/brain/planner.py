"""Coalesced synchronization of wrapper-owned verdicts.

Core selects workers and retains operator settings. The wrapper owns all model
requirements, context ceilings, placement modes and current feasibility.
"""
from __future__ import annotations
import hashlib
import json
import logging
import os
import threading
import time
from typing import Optional
from hugpy_core.brain.wrapper_verdicts import refresh as refresh_worker

logger = logging.getLogger("hugpy_core.planner")
COALESCE_S = float(os.environ.get("HUGPY_PLAN_COALESCE_S", "5") or 5)
REFRESH_S = 60.0  # Keep Wrapper availability younger than pair_live's 120s expiry.
_lock = threading.Lock()
_last_hash = {}
_last_refresh = {}
_running = set()
_next_allowed = {}
_timer_pending = set()


def replan_all(reason=""):
    from hugpy_core.registry import registry
    workers = registry.all_workers()
    for worker in workers:
        invalidate(worker["id"])
    return sum(bool(maybe_refresh(w, immediate=True)) for w in workers)


def invalidate(worker_id: str) -> None:
    """Forget the last-planned inputs so the next heartbeat re-plans."""
    with _lock:
        _last_hash.pop(worker_id, None)


def replan(name_or_id: str) -> Optional[str]:
    """Re-plan one worker NOW from its last report + the DB facts — the event
    path (facts_listener: a measurement row landed in hugpy_wrapper). Verdicts
    follow the facts, not the next budget change."""
    from hugpy_core.registry import registry
    w = registry.lookup_worker(name_or_id)
    if not w:
        return None
    invalidate(w["id"])
    return maybe_refresh(w, immediate=True)


def _plan_gate(wid: str, h: str, immediate: bool, now: float) -> str:
    """Decide, under ``_lock``, what a refresh request becomes:
      ``"skip"``   inputs unchanged, a refresh is already running, or a deferred
                   drift re-plan is already scheduled;
      ``"run"``    re-plan now (marks the worker running, opens the next window);
      ``"defer"``  within the drift window — schedule ONE deferred re-plan at the
                   window's end (it re-reads the worker, carrying the latest state).
    Events (immediate=True) never defer: they run now and reset the window."""
    with _lock:
        if wid in _running or (_last_hash.get(wid) == h
                              and now - _last_refresh.get(wid, float('-inf')) < REFRESH_S):
            return "skip"
        if not immediate and now < _next_allowed.get(wid, 0.0):
            if wid in _timer_pending:
                return "skip"
            _timer_pending.add(wid)
            return "defer"
        _next_allowed[wid] = now + COALESCE_S
        _running.add(wid)
        return "run"


def _coalesced_fire(wid: str) -> None:
    """The deferred drift re-plan: re-read the worker's LATEST report and re-plan it
    (the window has elapsed, so the gate now runs it). Nothing is dropped — the plan
    always uses the newest reading."""
    from hugpy_core.registry import registry
    with _lock:
        _timer_pending.discard(wid)
    w = registry.lookup_worker(wid)
    if w:
        maybe_refresh(w, immediate=False)


def maybe_refresh(w: dict, immediate: bool = False) -> Optional[str]:
    """Kick a background refresh when this worker's planner inputs changed.

    Intake calls this on every telemetry reading. Although capacity estimates
    depend on inventory, the snapshot also carries Wrapper's current feasibility.
    Resource changes must refresh that snapshot through the coalescing gate.
    Refresh unchanged inputs periodically too: pair_live expires after 120s."""
    service = w.get("data_service") or {}
    inputs = {"wrapper_version": w.get("wrapper_version"),
              "store_id": service.get("store_id"),
              "schema_version": service.get("schema_version"),
              "models": w.get("models"), "models_local": w.get("models_local"),
              "central_models": sorted((w.get("models_central") or {}).keys()),
              "gpu_capacity": [(g.get("index"), g.get("memory_total"))
                               for g in w.get("gpus") or []],
              "ram_total": w.get("ram_total"),
              "available": {"ram": w.get("free_ram"), "swap": w.get("swap_free"),
                            "gpu": [(g.get("index"), g.get("memory_free"))
                                    for g in w.get("gpus") or []],
                            "allocations": w.get("allocations")}}
    h = hashlib.sha256(json.dumps(inputs, sort_keys=True, default=str).encode()).hexdigest()
    wid = w["id"]
    # An offline worker has no wrapper to plan against: its verdicts cannot change
    # until it reconnects, and reconnecting re-plans it (intake). Without this, every
    # unrelated event (another worker's GPU reading) retried it — a failed refresh
    # never records its inputs — so a dead box was dialled every coalesce window.
    if "last_seen" in w:
        from hugpy_core.registry import registry
        if not registry.is_online(w):
            return None
    gate = _plan_gate(wid, h, immediate, time.monotonic())
    if gate == "skip":
        return None
    if gate == "defer":
        delay = max(0.0, _next_allowed.get(wid, 0.0) - time.monotonic())
        threading.Timer(delay, _coalesced_fire, (wid,)).start()
        return None

    def run():
        try:
            res = refresh_worker(w)
            with _lock:
                _last_hash[wid] = h
                _last_refresh[wid] = time.monotonic()
            logger.info("planner: %s", res)
        except Exception:  # noqa: BLE001 — planning never breaks routing
            logger.exception("planner refresh failed for %s", w.get("name"))
        finally:
            with _lock:
                _running.discard(wid)

    threading.Thread(target=run, name=f"planner-{wid[:8]}", daemon=True).start()
    return h
