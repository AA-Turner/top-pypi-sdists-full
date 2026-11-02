"""Durable fit-station experiments using only the worker's existing operator API.

One run per worker; a restart marks unfinished runs interrupted (never replays
loads). Browser navigation has no effect on a run. Worker leases still expire.
"""
from __future__ import annotations

import json
from contextlib import contextmanager
import psycopg
from psycopg.types.json import Jsonb
import threading
import time
import uuid

from . import station_tasks

_lock = threading.RLock()
_changed = threading.Condition(_lock)
_threads = {}
_boot = uuid.uuid4().hex
_last_changed = {}


@contextmanager
def _connect():
    from hugpy_core.imports.functions import core_dsn
    with psycopg.connect(core_dsn(), connect_timeout=5) as conn:
        yield conn


def _save(doc):
    if doc.get("state") != "running":
        if doc.get("current"):
            doc["last_step"] = doc.pop("current")
        doc["unprocessed_models"] = doc.get("transfer_queue") or doc.get("unprocessed_models") or []
        doc["transfer_queue"] = []
    doc["updated"] = time.time()
    with _connect() as conn:
        conn.execute("INSERT INTO station_runs(id,worker,updated,doc) VALUES (%s,%s,%s,%s) "
                     "ON CONFLICT(id) DO UPDATE SET worker=EXCLUDED.worker,updated=EXCLUDED.updated,doc=EXCLUDED.doc",
                     (doc["id"], doc["worker"], doc["updated"], Jsonb(doc)))
    with _changed:
        revision = _last_changed.get(doc["worker"], (0, None))[0] + 1
        _last_changed[doc["worker"]] = (revision, dict(doc))
        _changed.notify_all()


def events(worker):
    """Yield an initial snapshot, then only changes for this worker."""
    with _changed:
        snapshot = list_runs(worker)
        seen = _last_changed.get(worker, (0, None))[0]
    yield {"runs": snapshot}
    while True:
        with _changed:
            changed = _changed.wait_for(lambda: _last_changed.get(worker, (0, None))[0] != seen, timeout=15)
            latest = _last_changed.get(worker)
            if latest:
                seen = latest[0]
        if changed and latest:
            yield {"run": latest[1]}
        else:
            yield None


def list_runs(worker):
    with _lock, _connect() as conn:
        docs = [row[0] for row in conn.execute(
            "SELECT doc FROM station_runs WHERE worker=%s ORDER BY updated DESC LIMIT 30", (worker,))]
        for doc in docs:
            if doc["state"] == "running" and doc.get("boot") != _boot:
                doc.update(state="interrupted", error="Core restarted. Inspect worker actions before starting a new run.")
                _save(doc)
            if doc.get("state") != "running":
                if doc.get("current"):
                    doc["last_step"] = doc.pop("current")
                doc["unprocessed_models"] = doc.get("transfer_queue") or doc.get("unprocessed_models") or []
                doc["transfer_queue"] = []
        return docs


# Compatibility export for older integrations; the client belongs to the service layer.
from hugpy_core.registry.transport import request as _request


def _action(worker, kind, model, lease, knobs=None):
    params = {"lease_id": lease} if lease else {}
    if kind == "station-free":
        params.update(resource="all", model_key=model)
    if knobs is not None:
        params["knobs"] = knobs
    row = _request(worker, "/v1/operator/actions", {"action": kind, "model_key": model,
                    "params": params, "requested_by": "fit station experiment"})
    aid = row["id"]
    deadline = time.monotonic() + 1800
    while time.monotonic() < deadline:
        row = _request(worker, f"/v1/operator/actions/{aid}")
        if row.get("state") in ("done", "failed", "refused"):
            return row
        time.sleep(1)
    raise TimeoutError(f"Worker action {aid} is still running; inspect it before another test")


def sweep_knobs(resident, base):
    """GGUF expert-block sweep; Transformers supports only full expert split."""
    if not resident.get("is_moe"):
        raise ValueError("Loaded model has no structural MoE evidence")
    if resident.get("engine") not in ("gguf", "llama_cpp"):
        raise ValueError("Partial expert placement is unavailable for this engine; use the full MoE split load control")
    layers = int(resident.get("total_layers") or 0)
    if layers <= 0:
        raise ValueError("Loaded model did not report its block count")
    levels = sorted({0, layers, *(round(layers * fraction) for fraction in (.25, .5, .75))})
    return [{**base, "alloc_mode": "explicit", "bnb_4bit": False,
             "n_gpu_layers": -1, "moe": True, "n_cpu_moe": n} for n in levels]


def start(worker, body):
    kind = body.get("kind")
    items = body.get("models")
    lease = body.get("lease_id")
    if kind not in ("battery", "cliff", "bnb", "download", "methodical", "copy"):
        raise ValueError("Unknown run kind")
    if kind != "copy" and (not isinstance(lease, str) or not lease):
        raise ValueError("lease_id is required for tests")
    if not isinstance(items, list) or not 1 <= len(items) <= 500:
        raise ValueError("Select between 1 and 500 models")
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("key"), str) or not item["key"]:
            raise ValueError("Each model requires a key")
        if not isinstance(item.get("knobs", {}), dict):
            raise ValueError("knobs must be an object")
        if not isinstance(item.get("tasks", []), list) or not all(isinstance(t, str) for t in item.get("tasks", [])):
            raise ValueError("tasks must be a list of strings")
    if kind != "copy":
        current = _request(worker, "/v1/station").get("lease", {})
        if not current.get("active") or current.get("lease_id") != lease:
            raise ValueError("Reserve the worker before starting tests")
    with _lock:
        if kind in ("download", "methodical", "copy"):
            catalog = _request(worker, "/v1/models")
            available = {entry.get("id"): entry for entry in catalog.get("data", [])} if isinstance(catalog, dict) else {}
            local = [item for item in items if not available.get(item["key"], {}).get("staging_required", True)]
            cold = [item for item in items if item not in local]
            items = local + cold if kind == "methodical" else items
        else:
            cold = []
        active = next((d for d in _threads.values()
                       if d["worker"] == worker["name"] and d["state"] == "running"), None)
        if kind == "copy" and active and active["kind"] == "copy":
            existing = {item["key"] for item in active["models"]}
            added = [item for item in items if item["key"] not in existing]
            if len(active["models"]) + len(added) > 500:
                raise ValueError("Copy queue is full (500 models)")
            active["models"].extend(added)
            active["transfer_queue"].extend(item["key"] for item in added if item in cold)
            _save(active)
            return active.copy()
        if active or any(d["state"] == "interrupted" for d in list_runs(worker["name"])[:1]):
            raise ValueError("An active or interrupted run needs to finish or be acknowledged first")
        doc = {"id": uuid.uuid4().hex, "worker": worker["name"], "kind": kind, "state": "running",
               "boot": _boot, "created": time.time(), "results": [], "models": items, "cancel": False}
        if kind in ("download", "methodical", "copy"):
            doc["transfer_queue"] = [item["key"] for item in cold]
        _save(doc)
        thread = threading.Thread(target=_execute, args=(worker, lease, doc), daemon=True)
        _threads[doc["id"]] = doc
        thread.start()
        return doc.copy()


def cancel(worker, run_id):
    with _lock:
        doc = next((d for d in list_runs(worker) if d["id"] == run_id), None)
        if doc is None:
            raise ValueError("Run not found")
        if run_id in _threads:
            _threads[run_id]["cancel"] = True
            doc = _threads[run_id]
        elif doc["state"] == "interrupted":
            doc["state"] = "acknowledged"
        _save(doc)
        return doc


def _execute(worker, lease, doc):
    failures = []
    def progress(message):
        with _lock:
            doc["current"] = message
            _save(doc)

    def record(row):
        with _lock:
            doc["results"].append(row)
            _save(doc)

    def loaded(key, knobs, label):
        progress(f"{key}: {label}")
        began = time.monotonic()
        row = _action(worker, "station-load", key, lease, knobs)
        result = row.get("result") or {}
        resident = next((r for r in result.get("after", {}).get("residents", [])
                         if r.get("key") == key and r.get("healthy")), None)
        error = result.get("error")
        runtime_blocked = bool(error and any(term in json.dumps(error).lower() for term in ("importerror", "no module named", "profile not ready")))
        record({"model_key": key, "phase": label, "knobs": knobs, "ok": row.get("state") == "done" and bool(resident),
                "blocked": runtime_blocked, "error": error,
                "seconds": round(time.monotonic() - began, 3), "action": row, "resident": resident})
        return resident if row.get("state") == "done" else None

    def tasks(key, names, knobs, label):
        for task in names or ["unknown"]:
            if doc["cancel"]:
                break
            if task not in station_tasks.TASK_PATHS:
                record({"model_key": key, "phase": label, "task": task, "ok": False,
                        "blocked": True, "error": "No worker fixture/endpoint for this task"})
                continue
            try:
                progress(f"{key}: {label} · {task}")
                result, _ = station_tasks.run(worker, task, key, lease, knobs)
                record({**result, "phase": label, "knobs": knobs})
            except (OSError, ValueError) as exc:
                if isinstance(exc, TimeoutError):
                    raise
                record({"model_key": key, "phase": label, "task": task, "ok": False, "error": str(exc)})

    try:
        index = 0
        while True:
            # A copy request may append models while the current model is being
            # transferred. Check and close the queue under the same lock used
            # by start(), so a late request cannot be lost at the last item.
            with _lock:
                if doc["cancel"] or index >= len(doc["models"]):
                    doc["state"] = "cancelled" if doc["cancel"] else "failed" if failures else "done"
                    if failures:
                        doc["error"] = "; ".join(failures[:5])
                    break
                item = doc["models"][index]
                index += 1
            key, knobs = item["key"], dict(item.get("knobs", {}))
            names = list(dict.fromkeys(item.get("tasks", [])))
            if doc["kind"] in ("download", "methodical", "copy"):
                progress(f"{key}: verify or download")
                began = time.monotonic()
                stage = _action(worker, "copy-model" if doc["kind"] == "copy" else "station-stage", key, lease, knobs)
                record({"model_key": key, "phase": "download", "ok": stage.get("state") == "done",
                        "seconds": round(time.monotonic() - began, 3), "action": stage,
                        "error": (stage.get("result") or {}).get("error")})
                if stage.get("state") != "done":
                    failures.append(f"{key}: {(stage.get('result') or {}).get('error') or stage.get('state')}")
                if key in doc["transfer_queue"]:
                    doc["transfer_queue"].remove(key)
                    _save(doc)
                if doc["kind"] in ("download", "copy") or stage.get("state") != "done":
                    continue
                resident = loaded(key, knobs, "load")
                if resident:
                    try:
                        tasks(key, names, knobs, "task")
                    finally:
                        progress(f"{key}: free resident")
                        freed = _action(worker, "station-free", key, lease)
                        record({"model_key": key, "phase": "free", "ok": freed.get("state") == "done", "action": freed})
                continue
            if doc["kind"] == "battery":
                tasks(key, names, knobs, "task")
                continue
            if doc["kind"] == "bnb":
                knobs.update(bnb_4bit=True, alloc_mode="gpu-only", moe=False)
                resident = loaded(key, knobs, "4-bit load")
                if resident and resident.get("quant") == "dir-bnb4":
                    tasks(key, names, knobs, "4-bit task")
                else:
                    record({"model_key": key, "phase": "4-bit verification", "ok": False,
                            "error": "No healthy bitsandbytes resident was observed; inspect the exact load runtime/error"})
                continue
            # Start with all experts on CPU, to discover the actual loaded block count.
            baseline = {**knobs, "alloc_mode": "explicit", "moe": True, "n_gpu_layers": -1, "n_cpu_moe": 999, "bnb_4bit": False}
            resident = loaded(key, baseline, "MoE baseline")
            if not resident:
                continue
            try:
                points = sweep_knobs(resident, knobs)
            except ValueError as exc:
                record({"model_key": key, "phase": "sweep", "ok": False, "blocked": True, "error": str(exc)})
                continue
            for point in points:
                if doc["cancel"]:
                    break
                progress(f"{key}: unload before experts CPU {point['n_cpu_moe']}")
                freed = _action(worker, "station-free", key, lease)
                if freed.get("state") != "done":
                    raise RuntimeError("Could not unload the sweep model; inspect worker action")
                resident = loaded(key, point, f"experts CPU {point['n_cpu_moe']}")
                if resident:
                    if (resident.get("n_cpu_moe") or 0) != point["n_cpu_moe"] or resident.get("n_gpu_layers") != -1:
                        record({"model_key": key, "phase": "placement mismatch", "ok": False,
                                "knobs": point, "resident": resident, "error": "Actual placement differs from the sweep point"})
                    else:
                        tasks(key, names, point, f"experts CPU {point['n_cpu_moe']}")
    except Exception as exc:
        doc.update(state="failed", error=str(exc))
    finally:
        with _lock:
            doc["finished"] = time.time()
            _save(doc)
            _threads.pop(doc["id"], None)
