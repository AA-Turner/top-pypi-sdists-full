# LIFTED from legacy hugpy (read-only reference):
#   _has_usable_gpu <- py/fleet/hugpy_fleet/src/hugpy_fleet/central/workers.py:1535 (verbatim)
#   _resident_on    <- workers.py:3843 (loaded_models term only; no allocation rows)
#   routing rank    <- workers.py:_routing_rank 4350 (terms ③ resident, ⑥ GPU, last_picked, id)
#   _requested_worker_name <- py/inference/hugpy_engine/src/hugpy_engine/resolvers/remote.py:929 (verbatim)
#   central demand pull <- legacy routing a call to a box that lacks the model;
#     the box pulls it in the call (agent.py _ensure_present, purpose="demand")
# DROPPED: catalog, allocation, tier, task, fit and GPU-placement gates — the
#   box's fitevict decides fit. Assignment and wildcard still gate routing.
"""Pick the worker for a model_key."""
from __future__ import annotations

import logging
import threading
from typing import Any, Dict, Optional

from hugpy_core.registry import registry
from hugpy_core.models.keys import model_key_forms, serveable_match


class NoWorker(Exception):
    """No online worker can serve the requested model (or the pinned one can't)."""
    status = 404


# ── test-fire sequestering (operator ruling 2026-11-16) ──────────────────────
# While a test fire runs on a worker, routing must not place any OTHER call on
# that worker. The test fire's own calls carry its job tag (request
# metadata.test_fire.job_id) and so pass; everything else is routed elsewhere,
# or fails fast naming the test fire. This is the test fire's ONE special
# behaviour — it owns no relay path, no leases, no call records of its own.
_SEQUESTERED: Dict[str, str] = {}      # worker_id -> the test-fire job_id holding it
_SEQ_LOCK = threading.Lock()


def sequester(worker_id: str, job_id: str) -> None:
    """Hold ``worker_id`` for the test-fire ``job_id`` — no other call is routed there."""
    if worker_id and job_id:
        with _SEQ_LOCK:
            _SEQUESTERED[worker_id] = job_id


def release(worker_id: str, job_id: str) -> None:
    """Release the hold if ``job_id`` still owns it (a newer job keeps its own)."""
    with _SEQ_LOCK:
        if _SEQUESTERED.get(worker_id) == job_id:
            _SEQUESTERED.pop(worker_id, None)


def sequestered_by(worker_id: str) -> Optional[str]:
    """The test-fire job holding ``worker_id`` right now, or None."""
    with _SEQ_LOCK:
        return _SEQUESTERED.get(worker_id)


def _current_test_fire_job() -> Optional[str]:
    """The test-fire job tagged on the call being routed
    (request_body.metadata.test_fire.job_id), or None for ordinary traffic."""
    try:
        from hugpy_core.calllog.call_record import current
        row = current()
        md = ((row or {}).get("request_body") or {}).get("metadata") or {}
        tf = md.get("test_fire") if isinstance(md, dict) else None
        return tf.get("job_id") if isinstance(tf, dict) else None
    except Exception:  # noqa: BLE001 — sequestering never crashes a route
        return None


def _central_has(model_key: str) -> bool:
    """Whether the central store (HUGPY_CENTRAL_MODELS_HOME) holds this model."""
    try:
        from hugpy_storage.transfer_api import central_model_dir
        return bool(central_model_dir(model_key))
    except Exception:  # noqa: BLE001 — 404/409 abort or no store: not on central
        return False


def _has_usable_gpu(worker: Dict[str, Any]) -> bool:
    """Whether the worker advertises a GPU with free VRAM (for efficiency ranking).

    Capability-honest, like vision routing: a worker whose llama.cpp build
    AFFIRMATIVELY reports it cannot offload (engine.supports_gpu_offload is
    False) ranks as GPU-less no matter what nvidia-smi shows — n_gpu_layers is
    silently ignored by a CPU-only wheel, so its "GPU" would never be used.
    Older agents that don't report the flag keep their GPU credit (no guessing).
    """
    if (worker.get("engine") or {}).get("supports_gpu_offload") is False:
        return False
    return any((g.get("memory_free") or 0) > 0 for g in (worker.get("gpus") or []))


def _resident_on(worker: Dict[str, Any], model_key: str, wanted: set) -> bool:
    """MEASURED-RESIDENT: this worker reports ``model_key`` loaded RIGHT NOW."""
    return not _unhealthy_slot_on(worker, model_key, wanted) and serveable_match(
        model_key, wanted, worker.get("loaded_models") or [])


def _unhealthy_slot_on(worker: Dict[str, Any], model_key: str, wanted: set) -> bool:
    """A reported slot failed health, even if loaded_models still lists it."""
    slots = [a for a in (worker.get("allocations") or [])
             if serveable_match(model_key, wanted, [a.get("model_key")])]
    return bool(slots) and not any(a.get("healthy") is True for a in slots) \
        and any(a.get("healthy") is False and not a.get("loading") for a in slots)


def _serves(worker: Dict[str, Any], model_key: str, wanted: set) -> bool:
    held = list(worker.get("loaded_models") or []) + list(worker.get("models_local") or []) \
        + list(worker.get("models") or [])
    return serveable_match(model_key, wanted, held)


def _routing_rank(worker: Dict[str, Any], model_key: str, wanted: set,
                  pairs: dict | None = None) -> tuple:
    # A cold central-drive pull should prefer the worker with the most usable
    # GPU room. A GPU advertised by a CPU-only engine cannot take that credit.
    gpu_room = max((int(g.get("memory_free") or 0) for g in (worker.get("gpus") or [])), default=0) \
        if _has_usable_gpu(worker) else 0
    return (
        1 if _unhealthy_slot_on(worker, model_key, wanted) else 0,
        0 if _resident_on(worker, model_key, wanted) else 1,
        0 if gpu_room else 1,
        -gpu_room,
        -int(worker.get("free_ram") or 0),
        worker.get("last_picked", 0),
        worker.get("id", ""),
    )


def _serving_now(model_key: str, wanted: set, pool: str, pair_blocked,
                 allowed: set[str]) -> Optional[Dict[str, Any]]:
    """The registered, online, unblocked worker whose front door reports
    ``model_key`` RESIDENT right now (hugpy_wrapper.residents: alive, healthy,
    not loading). None when nobody serves it — or the read fails — so the
    caller falls through to normal routing. residents.worker is the worker NAME."""
    try:
        from hugpy_core.web.console_routes import _ie
        rows = _ie("SELECT worker, key, busy, last_used FROM residents "
                   "WHERE alive AND healthy AND NOT loading ORDER BY busy, last_used DESC NULLS LAST")
    except Exception:  # noqa: BLE001 — the fast path never blocks a call
        return None
    from hugpy_core.relay.admission import is_blocked
    for name, key, _busy, _last in rows:
        if not serveable_match(model_key, wanted, [key]):
            continue
        w = registry.lookup_worker(name)
        if w is None or not registry.is_online(w):
            continue
        if (w.get("id") or "") not in allowed or \
                registry.effective_pool(w) != (pool or "") or is_blocked(w.get("id") or "") \
                or (w.get("id") or "") in pair_blocked:
            continue
        return w
    return None


def requested_worker_name(alloc) -> Optional[str]:
    """The per-request WORKER pin, riding the same ``alloc`` dict as the other
    triggers (operator ask 2026-07-29: "it'll need its worker allocation"):
    ``{"alloc": {"worker": "ae", ...}}``. Not in _REQUEST_ALLOC_KEYS on purpose
    — it steers ROUTING, never the spill wire."""
    a = alloc
    if isinstance(a, dict):
        w = a.get("worker")
        if isinstance(w, str) and w.strip():
            return w.strip()
    return None


def requested_worker_names(alloc) -> Optional[list[str]]:
    """An explicit routing subset; None is unrestricted and [] permits none."""
    if not isinstance(alloc, dict) or 'workers' not in alloc:
        return None
    names = alloc['workers']
    if not isinstance(names, list) or len(names) > 256 or any(
            not isinstance(name, str) or not name.strip() for name in names):
        exc = NoWorker('alloc.workers must be a list of up to 256 nonempty worker names or IDs')
        exc.status = 400
        raise exc
    return list(dict.fromkeys(name.strip() for name in names))


def _provided(model_key, candidates, rank=None):
    """A worker given the model from another host's central drive (registry/fleet_central.provide), or None."""
    from hugpy_core.registry import fleet_central
    try:
        return fleet_central.provide(model_key, candidates, rank)
    except fleet_central.CopyPending as exc:
        err = NoWorker(str(exc))
        err.status = 503
        raise err from None
    except (LookupError, RuntimeError) as exc:
        raise NoWorker(str(exc)) from None


def pick(model_key: str, pool: str = "", pin: Optional[str] = None,
         source: str = "routing", workers: Optional[list[str]] = None, copy: bool = True) -> Dict[str, Any]:
    """Serve a model through an assignment or an opted-in wildcard worker. ``copy``: when no eligible worker has
    it but a connected host's central drive does, copy it to the worker routing chooses and serve it there
    (operator 2026-11-15)."""
    selected = None if workers is None else set(workers)
    if selected == set():
        raise NoWorker('No workers selected for this request')
    def selected_worker(w):
        return selected is None or bool(selected.intersection((w.get('id'), w.get('name'))))
    wanted = model_key_forms(model_key)
    from hugpy_core.models.modeldb import routing_snapshot
    pairs, wildcards = routing_snapshot(model_key)

    def remember(w):
        # Existing assignments and already-resident models are safe to retain
        # immediately. A wildcard/cold route is only a candidate: its pair is
        # promoted after the worker proves a fit and completes the load.
        wid = w.get("id") or ""
        assigned, _pinned, excluded = pairs.get(wid, (False, False, False))
        if excluded:
            raise NoWorker(f"{model_key!r} was explicitly unassigned from worker {wid!r}")
        if assigned or _resident_on(w, model_key, wanted):
            from hugpy_core.models.modeldb import record_routed_allocation
            if not record_routed_allocation(model_key, wid, source):
                raise NoWorker(f"{model_key!r} was explicitly unassigned from worker {wid!r}")
        registry.stamp_picked(wid)
        return w

    def allowed(w):
        wid = w.get("id") or ""
        state = pairs.get(wid, (False, False, False))
        # Assignment grants the route now; pin only keeps that assignment over
        # a Core restart. Residency policy controls eviction independently.
        if state[0]:
            return True
        if state[2]:  # explicit operator unassign/exclusion
            return False
        return bool(wildcards.get(wid, True))

    if pin:
        w = registry.lookup_worker(pin)
        if w is None:
            raise NoWorker(f"requested worker {pin!r} is not registered")
        if not selected_worker(w):
            raise NoWorker(f"requested worker {pin!r} is outside the selected workers")
        if not registry.is_online(w):
            raise NoWorker(f"requested worker {pin!r} is offline")
        holder = sequestered_by(w.get("id") or "")
        if holder and holder != _current_test_fire_job():
            raise NoWorker(f"requested worker {pin!r} is sequestered by test fire {holder}")
        from hugpy_core.relay.admission import is_blocked
        if is_blocked(w.get("id") or ""):
            raise NoWorker(f"requested worker {pin!r} is blocked by the operator")
        from hugpy_core.models.modeldb import blocked_worker_ids
        if (w.get("id") or "") in blocked_worker_ids(model_key):
            raise NoWorker(f"{model_key!r} is blocked on worker {pin!r} by the operator")
        # A call explicitly targeted to this worker can establish a temporary
        # allocation even with wildcard off. An operator exclusion still wins.
        if pairs.get(w.get("id") or "", (False, False, False))[2]:
            raise NoWorker(f"{model_key!r} is unassigned from worker {pin!r}")
        # legacy demand path: a box that lacks the model is still routed the call
        # when central holds it — the box pulls it (agent._ensure_present)
        if not _serves(w, model_key, wanted) and not _central_has(model_key):
            if not (copy and _provided(model_key, [w])):
                raise NoWorker(f"requested worker {pin!r} does not have {model_key!r}")
    else:
        from hugpy_core.relay.admission import is_blocked
        from hugpy_core.models.modeldb import blocked_worker_ids
        pair_blocked = blocked_worker_ids(model_key)   # model × worker operator block
        # Existing allocations get first refusal. Wildcard can establish a new
        # temporary allocation when no allocated box is eligible or can serve.
        # Within each group, a healthy resident wins before any cold load.
        cur_job = _current_test_fire_job()
        candidates = [w for w in registry.all_workers()
                      if selected_worker(w) and registry.is_online(w) and registry.effective_pool(w) == (pool or "")
                      and not is_blocked(w.get("id") or "")
                      and (w.get("id") or "") not in pair_blocked and allowed(w)]
        # A worker held by a test fire takes no other traffic (only that job's
        # own tagged calls, which always pin, would be let through).
        sequestered = [w for w in candidates if sequestered_by(w.get("id") or "") not in (None, cur_job)]
        eligible = [w for w in candidates if sequestered_by(w.get("id") or "") in (None, cur_job)]
        allocated = [w for w in eligible if pairs.get(w.get("id") or "", (False, False, False))[0]]
        groups = [allocated, [w for w in eligible if w not in allocated]] if allocated else [eligible]
        w = None
        central_has = None
        for group in groups:
            if not group:
                continue
            w = _serving_now(model_key, wanted, pool, pair_blocked, {box["id"] for box in group})
            if w is not None:
                logging.getLogger(__name__).info("serving-first: %s is resident on %s; relaying there", model_key, w.get("name"))
                return remember(w)
            cands = [box for box in group if _serves(box, model_key, wanted)]
            if not cands:
                if central_has is None:
                    central_has = _central_has(model_key)
                if central_has:
                    cands = group  # central has it; the selected box pulls it
            if not cands and copy:
                # another host's central drive holds it: copied to the worker routing would choose, served there
                given = _provided(model_key, group, lambda box: _routing_rank(box, model_key, wanted, pairs))
                if given is not None:
                    w = given
                    break
            if not cands:
                # Wildcard means this worker is a valid route even when its
                # catalog has not seen the model yet. The worker's front door
                # performs the real fit/load check and reports any refusal.
                cands = [box for box in group if wildcards.get(box.get("id") or "", False)]
            if cands:
                w = min(cands, key=lambda box: _routing_rank(box, model_key, wanted, pairs))
                break
        if w is None:
            scope = 'selected ' if selected is not None else ''
            held = [(box.get("name") or box.get("id"), sequestered_by(box.get("id") or ""))
                    for box in sequestered if _serves(box, model_key, wanted)]
            if held:
                where = "; ".join(f"{name} is sequestered by test fire {job}" for name, job in held)
                raise NoWorker(f"Unknown model {model_key!r}: no eligible {scope}worker can serve it "
                               f"({where})")
            raise NoWorker(f"Unknown model {model_key!r}: no eligible {scope}worker can serve it")
    return remember(w)


def served_name(model_key: str, worker: Dict[str, Any]) -> str:
    """The name ``worker`` serves ``model_key`` under: what to put in the request sent to it.

    pick() credits a worker with a model by loose forms (a bare tail, case, the -GGUF
    equivalence), which is how a legacy short name or the engine's default finds its worker.
    The worker itself resolves only a unit (``repo::file``), a repo name or a variation, so the
    request must carry one of those. A name the worker advertises, or the repo of units it
    advertises, goes as it is (for a repo the worker chooses the unit). Anything else becomes
    the repo it stands for; among several, one with a unit loaded, then by name."""
    names = [name for field in ("loaded_models", "models", "models_local")
             for name in (worker.get(field) or []) if isinstance(name, str)]
    if not model_key or model_key in names:
        return model_key
    heads = {name.split("::", 1)[0] for name in names}
    if model_key in heads:
        return model_key
    wanted = model_key_forms(model_key)
    loaded = {name.split("::", 1)[0] for name in (worker.get("loaded_models") or []) if isinstance(name, str)}
    stands_for = sorted((head for head in heads if serveable_match(model_key, wanted, [head])),
                        key=lambda head: (head not in loaded, head))
    return stands_for[0] if stands_for else model_key


def confirm_routed_allocation(model_key: str, worker: Dict[str, Any], source: str = "routing") -> bool:
    """Record a cold/wildcard route only after its worker call succeeds."""
    from hugpy_core.models.modeldb import record_routed_allocation
    wid = (worker or {}).get("id") or ""
    return bool(wid and record_routed_allocation(model_key, wid, source))
