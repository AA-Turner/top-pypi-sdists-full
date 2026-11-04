"""The console's remaining routes, served by hugpy_core itself (no fallback to
the hugpy_next central). Live values come from the DB / the registry at the
moment of the call; /llm/events pushes on every registry change."""
from __future__ import annotations

import json
import time
import urllib.request

from flask import Response, jsonify, request, stream_with_context

from abstract_flask import spec

from hugpy_core.registry import registry

from hugpy_core.calllog.calllog import query as _ie   # THE one reader of the wrapper call log
NOTE_FLAGS = ["broken", "trash", "archive", "unknown", "needs-env", "experimental", "keep"]


def worker_activity(worker: dict) -> list:
    """One host view of the worker's GPU: every process on its card from
    hugpy_wrapper.gpu_state (published by its fitevict front door the moment
    the card changes), joined to the front door's residents."""
    name = worker.get("name")
    cards = _ie("SELECT device, processes, hugpy_pids, probe_pids FROM gpu_state WHERE worker = %s", (name,))
    res = {int(pid): key for key, pid in _ie("SELECT key, pid FROM residents WHERE worker = %s AND pid IS NOT NULL", (name,))}
    rows = []
    for device, procs, ours, probes in cards:
        for pid_s, nbytes in sorted((procs or {}).items()):
            pid = int(pid_s)
            key = res.get(pid)
            kind = "hugpy" if key or pid in (ours or []) else ("probe" if pid in (probes or []) else "observed")
            rows.append({"kind": kind, "model_key": key, "service": "fitevict" if kind == "hugpy" else
                         ("llama.cpp dry run" if kind == "probe" else "gpu process"),
                         "pids": [pid], "gpu_indices": [device], "vram_bytes": int(nbytes),
                         "vram_mib": int(nbytes) // 1048576, "state": "running",
                         "evictable": kind == "hugpy", "immutable": kind == "observed",
                         "api_available": bool(key), "activity": {},
                         "note": ("Hugpy managed (fitevict)" if kind == "hugpy" else
                                  "transient sizing probe" if kind == "probe" else
                                  "GPU process observed; not managed by hugpy")})
    return rows


def _ts(v):
    if v is None:
        return None
    return v if isinstance(v, (int, float)) else v.timestamp()


def _key_forms(k: str) -> set:
    """The spellings one model id wears across the catalog and the call log:
    ``owner~X`` / ``owner/X`` / bare ``X`` (and lowercased). Used to match a
    catalog model_key to a call_log model_name without a '~' vs '/' miss."""
    k = (k or "").strip().rstrip("/")
    if not k:
        return set()
    out = {k, k.lower(), k.replace("~", "/"), k.replace("/", "~")}
    for sep in ("~", "/"):
        if sep in k:
            tail = k.split(sep)[-1]
            out |= {tail, tail.lower()}
    return {x for x in out if x}


_PLACEMENTS_CACHE: dict = {}   # worker_name -> (fetched_at, {model_name: alloc_mode})
_PLACEMENTS_TTL = 5.0          # seconds — one query per worker per request burst


def placements_by_worker(worker_name: str) -> dict:
    """{model_key: last ACTUAL decided alloc_mode} for this worker — the newest
    successful (http_status = 200) hugpy_wrapper.call_log_derived row per
    model_name (call_log_derived.worker is the worker NAME; model_name == the
    model_key). This is what the model was really placed as last time it served,
    shown as the Alloc control's secondary label. A model never served here
    simply doesn't appear. Cached per worker for a few seconds."""
    if not worker_name:
        return {}
    now = time.time()
    hit = _PLACEMENTS_CACHE.get(worker_name)
    if hit and (now - hit[0]) < _PLACEMENTS_TTL:
        return hit[1]
    try:
        from hugpy_core.calllog import calllog
        out = calllog.placements_by_worker(worker_name)
    except Exception:  # noqa: BLE001 — never block a worker list
        return {}
    _PLACEMENTS_CACHE[worker_name] = (now, out)
    return out


def calls_rows(limit: int = 300, since: "float | None" = None,
               intent: "str | None" = None) -> list:
    """The console's call list from hugpy_wrapper.call_log_derived (the wrapper's
    call log is the single source of truth, read through calllog.py); shaped like
    the legacy /llm/calls rows. ``intent`` filters on the call's own
    metadata.intent (intent.py)."""
    from hugpy_core.calllog import calllog
    out = []
    for d in calllog.calls(limit, since, intent):
        st = d["http_status"]
        status = "done" if st == 200 else ("failed" if st is not None else
                                           ("running" if d["responded_at"] is None else "done"))
        tot = (d["prompt_tokens"] or 0) + (d["completion_tokens"] or 0)
        out.append({
            "id": d["id"], "request_id": d["request_id"], "intent": d["intent"],
            "model": d["model_name"], "model_key": d["model_name"], "worker": d["worker"],
            "kind": d["task"], "route": d["endpoint"], "client": d["caller"],
            "peer": str(d["from_ip"]) if d["from_ip"] is not None else None,      # inet -> text
            "host": str(d["to_ip"]) if d["to_ip"] is not None else None, "transport": "http",
            "status": status, "processed_status": status if status != "running" else None,
            "error": d["error"], "tokens": d["completion_tokens"], "total_tokens": tot or None,
            "queued_ts": _ts(d["received_at"]), "started_ts": _ts(d["received_at"]),
            "processing_ts": _ts(d["forwarded_at"] or d["dispatched_at"]),
            "first_token_ts": _ts(d["inference_started_at"]),
            "ended_ts": _ts(d["responded_at"]), "processed_ts": _ts(d["responded_at"]),
            "locality": "warm" if d["was_resident"] else "cold",
            "alloc_mode": d["alloc_mode"], "ctx": d["context_length"], "plan_note": d["plan_note"],
            "load_s": float(d["load_s"]) if d["load_s"] is not None else None,
            "total_s": float(d["total_s"]) if d["total_s"] is not None else None,
            "tok_per_s": float(d["tok_per_s"]) if d["tok_per_s"] is not None else None,
        })
    return out


def throughput_by_model() -> dict:
    """The per-model tok/s rollup — computed by calllog.py (the one derived
    layer); core computes nothing itself."""
    from hugpy_core.calllog import calllog
    return calllog.throughput_by_model()


def model_metrics_rows(limit: int = 500, model: str = "", suite: str = "") -> list:
    """The metrics sheet: one row per model x quant x alloc_mode x worker. The
    SQL rollup (cold_load_s = the chain's central pull, hot_load_s = engine load,
    tok/s medians) is calllog.metrics_by_model; here we only merge the core-local
    grades onto each row."""
    from hugpy_core.calllog import calllog
    rows = calllog.metrics_by_model(limit, model)
    try:
        from hugpy_core.grading import grader
        gs = {(g["model_key"], g["suite"]): g for g in grader.summary(suite=suite or None)}
        for it in grader.latest(suite=suite or None):
            identity = (it["model_key"], it["suite"])
            if identity in gs:
                gs[identity].setdefault("items", []).append(it)
    except Exception:  # noqa: BLE001 — the sheet renders without grades
        gs = {}
    # each row's own throughput BLOCK (n_calls, n_rated, mean_tok_s Σ/Σ, reason)
    # from the call log — the Grader matrix reads row.throughput as a block; a
    # bare tok_per_s number rendered as "no calls recorded" on every cell
    try:
        cells = calllog.cell_index()
    except Exception:  # noqa: BLE001
        cells = {}
    def _tp(r):
        c = cells.get((r["model_name"], r.get("worker"), r.get("quant"), r.get("alloc_mode")))
        if c is None and r.get("n_samples"):
            c = {"n_calls": int(r["n_samples"]), "n_rated": 0, "mean_tok_s": r.get("tok_per_s_avg"),
                 "reason": calllog._cell_reason({"n_calls": int(r["n_samples"]), "n_rated": 0,
                                                 "mean_s_per_call": None})}
        return c
    return [{**_grade_cols(g), **r, "throughput": _tp(r),
             "upload_time_s": None, "media_bytes": None, "temperature": None}
            for r in rows
            for g in ([grade for (key, _), grade in gs.items() if key == r["model_name"]]
                      or ([] if suite else [None]))]


def _grade_cols(g: "dict | None") -> dict:
    if not g:
        return {"grade": None, "grade_suite": None, "grade_detail": None, "graded_at": None}
    from hugpy_core.grading import grader
    # grade on the console's 0..100 scale; detail = the per-item matrix + counts
    return {"grade": round(g["score"] * 100, 2), "grade_suite": g["suite"], "graded_at": g["last_graded"],
            "grade_detail": {**grader.matrix(g.get("items") or [], g["suite"]),
                             "passed": g["passed"], "graded": g["graded"], "of": g["of"], "depth": g["depth"]}}


def _sig(payload) -> str:
    """A feed's content for change detection — its own build stamp excluded."""
    if isinstance(payload, dict):
        payload = {k: v for k, v in payload.items() if k not in ("generated_at", "ts", "updated")}
    return json.dumps(payload, default=str, sort_keys=True)


_WORKER_LIVE_FIELDS = {"status", "last_seen", "cpu", "free_ram", "ram_free_bytes", "ram_used", "swap_total", "swap_free",
                       "vram_used", "loaded_models", "loading", "allocations",
                       "resources", "cards", "gpu_policy", "resources_sampled_at", "pid_registry", "storage", "storage_view", "link", "link_ts", "worker_state", "state_stale"}
_GPU_LIVE_FIELDS = {"memory_free", "memory_used", "memory_reserved",
                    "memory_usable", "gpu_state"}


def _feed_sig(name: str, payload) -> str:
    """Compare the large roster by structure; live readings use `liveness`."""
    if name != "workers" or not isinstance(payload, list):
        return _sig(payload)
    stable = []
    for worker in payload:
        if not isinstance(worker, dict):
            stable.append(worker)
            continue
        row = {k: v for k, v in worker.items() if k not in _WORKER_LIVE_FIELDS}
        if isinstance(row.get("gpus"), list):
            row["gpus"] = [{k: v for k, v in gpu.items() if k not in _GPU_LIVE_FIELDS}
                           if isinstance(gpu, dict) else gpu for gpu in row["gpus"]]
        stable.append(row)
    return _sig(stable)


def liveness_feed() -> list[dict]:
    """Small worker readings published on each registry change."""
    out = []
    from hugpy_core.web.resources import storage_view
    reports = registry.all_workers()
    for worker in reports:
        view = registry.public_view(worker)
        from hugpy_core.models.modeldb import worker_view_extras
        swap = worker_view_extras(view.get("id") or "")
        allocations = view.get("allocations") or []
        out.append({
            "id": view.get("id"), "name": view.get("name"),
            "status": view.get("status"), "last_seen": view.get("last_seen"),
            "cpu": view.get("cpu"), "free_ram": view.get("free_ram"), "ram_free_bytes": view.get("ram_free_bytes"),
            "swap_total": view.get("swap_total") if view.get("swap_total") is not None else swap.get("swap_total"),
            "swap_free": view.get("swap_free") if view.get("swap_free") is not None else swap.get("swap_free"),
            "storage": view.get("storage"), "storage_view": storage_view(worker, reports),
            "ram_total": view.get("ram_total"),
            "link": view.get("link"), "link_ts": view.get("link_ts"),
            "worker_state": view.get("worker_state"),
            "state_stale": view.get("state_stale"),
            "loaded_models": view.get("loaded_models") or [],
            "loading": view.get("loading") or [],
            "gpus": [{"index": g.get("index", i), "memory_free": g.get("memory_free")} for i, g in enumerate(view.get("gpus") or [])],
            "allocations": allocations, "pid_registry": view.get("pid_registry") or {},
            "cards": view.get("cards") or [], "gpu_policy": view.get("gpu_policy") or {},
            "resources_sampled_at": view.get("resources_sampled_at"),
            "moe_effective": {a["model_key"]: True for a in allocations
                              if isinstance(a, dict) and a.get("model_key") and a.get("n_cpu_moe")},
        })
    return out


def queue_feed():
    from hugpy_core.web.queue_view import queue_snapshot
    return queue_snapshot([registry.public_view(worker) for worker in registry.all_workers()])


def llm_queue(**kwargs):
    return jsonify(queue_feed())


def model_status_payload(rows=None) -> dict:
    """The Models table's status block (GET /llm/models/status)."""
    if rows is None:
        from hugpy_core.web.routes import catalog_rows
        rows = catalog_rows()
    try:
        tp = throughput_by_model()
    except Exception:  # noqa: BLE001 — status renders without metrics
        tp = {}
    # Match the catalog model_key to the call_log model_name tolerating the
    # owner~X / owner/X / bare-X spellings the two sides carry (operator: watch
    # '~' vs '/' keys), so a model WITH log rows is never shown "no calls
    # recorded" over a spelling mismatch. Exact key wins; else by tail.
    tp_index: dict = {}
    for key, blk in tp.items():
        for form in _key_forms(key):
            tp_index.setdefault(form, blk)

    def _tp(model_key):
        if model_key in tp:
            return tp[model_key]
        for form in _key_forms(model_key):
            if form in tp_index:
                return tp_index[form]
        return None

    try:
        from hugpy_core.models.modelrows import workers_by_model
        per_box = workers_by_model()        # the seed; actions then arrive on /llm/models/rows/stream
    except Exception:  # noqa: BLE001
        per_box = {}
    models = [{"model_key": r["model_key"], "framework": r.get("framework"), "status": r.get("status") or "known",
               "workers": per_box.get(r["model_key"], []),
               "blocked": False, "archived": {"marked": False, "at": None, "by": None, "reason": None},
               "admission": {"status": "unknown"}, "task": r.get("task"),
               "throughput": _tp(r["model_key"]),
               "throughput_cells": (_tp(r["model_key"]) or {}).get("cells", [])} for r in rows]
    return {"models": models, "count": len(models), "buckets": {}, "counts": {},
            "generated_at": time.time(), "live": True}


def _json(payload, status=200):
    """Wrap JSON-able data in a Response so register_route passes the custom
    status through (a returned (body, status) tuple would be re-wrapped)."""
    r = jsonify(payload)
    r.status_code = status
    return r


# ── console views, as pure functions (register_categories convention) ────────
# Input arrives as kwargs (JSON body / form / query, via get_request_datas);
# path params from the original rules are now kwargs. request is read only for
# host/headers (readiness) — never for body input.

def console_bootstrap(view=None, **kwargs):
    """Return the lightweight console shell payload; include the model catalog
    only for callers that explicitly request ``?view=full``."""
    from hugpy_core.relay.arms import CORE, arms
    from hugpy_core.brain.model_groups import all_groups
    from hugpy_core.help import help_store

    # The console shell and the arm-presence hook need only the small bootstrap
    # values. Building the model catalog reads up to 1,000 database rows, so
    # defer it until a catalog-backed UI surface asks for it explicitly. ``view``
    # arrives as a kwarg (query/body field, via the registrar).
    full = view == "full"
    catalog = None
    if full:
        from hugpy_core.web.routes import catalog_rows
        from hugpy_core.web.console_catalog import console_catalog_rows
        catalog = catalog_rows()
    try:
        from hugpy_core.brain import brain
        brain.ensure_brain_group()
    except Exception:  # the stored groups remain readable without the seed
        pass
    payload = {
        "core": CORE,
        "arms": arms(),
        "model_groups": all_groups(),
        "help_pending": help_store.pending_count(),
    }
    from hugpy_core.config.settings import read_policies
    policies = read_policies()
    payload["model_preferences"] = policies.get("model_preferences", {})
    payload["task_bindings"] = policies.get("task_bindings", {})
    if full:
        payload["models"] = console_catalog_rows(catalog)
        payload["model_status"] = model_status_payload(catalog)
    return jsonify(payload)


def console_schema(**kwargs):
    """The schema the console renders placement and knob controls from: placements
    as terms (key, label, definition, engines, category), the knob schema and the
    accepted legacy renames (hugpy_core.intake.schema). 404 when this Core's
    resources predate the placement terms; the console keeps its built-in list."""
    from hugpy_core.intake import schema
    try:
        return jsonify(schema.document())
    except ImportError as exc:
        return _json({"error": f"placement terms unavailable: {exc}"}, 404)


def installed_arms(**kwargs):
    """Which optional surfaces this install has (the console hides the rest)."""
    from hugpy_core.relay.arms import CORE, arms
    return jsonify({"core": CORE, "arms": arms()})


def central_provisioning(**kwargs):
    """Readiness indexed by canonical key and worker-reported Hub aliases."""
    from hugpy_core.registry import central_store
    rows = central_store.rows(include_missing=True)
    out = {}
    repo_counts = {}
    for row in rows:
        repo_counts[row.get("repo")] = repo_counts.get(row.get("repo"), 0) + 1
    for row in rows:
        gone = bool(row.get("missing"))
        value = {
            "state": "absent" if gone else "ready",
            "reason": f"central's model directory is gone: {row.get('dir')}" if gone else None}
        owner_repo = f"{row.get('owner')}/{row.get('repo')}" if row.get("owner") else None
        aliases = {row.get("model_key"), row.get("hub_id"), owner_repo,
                   owner_repo.replace("/", "~") if owner_repo else None}
        if repo_counts.get(row.get("repo")) == 1:
            aliases.add(row.get("repo"))
        for alias in aliases:
            if alias:
                out[alias] = value
    return jsonify(out)


def grading_suites(**kwargs):
    from hugpy_core.grading import grader
    return jsonify({"suites": [{"name": name, "tiers": len(grader.TIER_ORDER),
        "max": len(grader.curriculum(name)),
        "tasks": list(dict.fromkeys(row[0] for row in grader.curriculum(name))),
        "task": "text-generation" if name == grader.SUITE else grader.providers()[name]["suite"].grade_task}
        for name in grader.suite_names()]})


def llm_grades(**kwargs):
    """Grader rollups per model (score = passed / curriculum size, depth per
    category); ?model=<key> for one model plus its graded items."""
    from hugpy_core.grading import grader
    model = (kwargs.get("model") or "").strip() or None
    suite = (kwargs.get("suite") or "").strip() or None
    if suite and suite not in grader.suite_names():
        return _json({"error": "unknown grading suite"}, 400)
    out = {"suite": suite, "suites": grader.suite_names(), "models": grader.summary(model, suite)}
    if suite:
        out["of"] = len(grader.curriculum(suite))
    if model:
        out["items"] = grader.latest(model, suite)
    return jsonify(out)


def model_graded_calls(model=None, **kwargs):
    """The model's graded calls for the Grader tab: each latest verdict joined
    to its call_log row by request_id (the grade is a pointer; the call's
    numbers come from the call log). Never 500. ``model`` was the path param
    (/llm/models/<model>/metrics); it is now a kwarg."""
    from hugpy_core.grading import grader
    try:
        items = grader.latest(model)
        rids = [i["request_id"] for i in items if i["request_id"]]
        calls = {r[0]: r[1:] for r in _ie(
            "SELECT request_id, quantization, alloc_mode, tok_per_s, completion_tokens, worker"
            " FROM call_log_derived WHERE request_id = ANY(%s)", (rids,))} if rids else {}
        out = []
        for i in items:
            q, alloc, tok_s, toks, w = calls.get(i["request_id"]) or (None,) * 5
            out.append({**grader.item_def(i["category"], i["tier"], i["suite"]),
                        "task": f"{i['category']} ({i['tier']})", "grade_suite": i["suite"],
                        "grade": "PASS" if i["passed"] else "FAIL", "passed": i["passed"],
                        "output": i["answer"], "why": i["why"], "request_id": i["request_id"],
                        "worker": w or i["worker"], "quant": q or i["quant"], "alloc_mode": alloc,
                        "tok_s": float(tok_s) if tok_s is not None else None, "completion_tokens": toks,
                        "timestamp": i["at"], "model": model, "benchmark": True})
        # tok/s by worker over EVERY recorded call of the model (was a fixed []
        # — the Grader tab showed "no calls recorded" for every model)
        try:
            from hugpy_core.calllog import calllog
            averages = calllog.worker_totals(_key_forms(model) | {model})
        except Exception:  # noqa: BLE001
            averages = []
        return jsonify({"calls": out, "worker_averages": averages, "count": len(out)})
    except Exception as exc:  # noqa: BLE001
        return jsonify({"calls": [], "worker_averages": [], "count": 0, "error": str(exc)})


def model_metrics2(**kwargs):
    """The live metrics sheet, derived from the wrapper's call log. Never 500."""
    try:
        limit = max(1, min(int(kwargs.get("limit") or 500), 5000))
    except (TypeError, ValueError):
        limit = 500
    try:
        rows = model_metrics_rows(limit, (kwargs.get("model") or "").strip(),
                                  (kwargs.get("suite") or "").strip())
        return jsonify({"rows": rows, "count": len(rows), "generated_at": time.time()})
    except Exception as exc:  # noqa: BLE001
        return jsonify({"rows": [], "count": 0, "generated_at": time.time(), "error": str(exc)})


def llm_calls(**kwargs):
    """Who called what, when, and how it went — from the wrapper's call log."""
    try:
        limit = max(1, min(2000, int(kwargs.get("limit") or 300)))
    except (TypeError, ValueError):
        limit = 300
    try:
        since = float(kwargs["since"]) if kwargs.get("since") else None
    except (TypeError, ValueError):
        since = None
    intent = (kwargs.get("intent") or "").strip() or None
    rows = calls_rows(limit, since, intent)
    return jsonify({"calls": rows, "count": len(rows), "intent": intent,
                    "path": "hugpy_wrapper.call_log_derived"})


def llm_calls_raw(**kwargs):
    """Unmodified call_log records. No aliases, defaults or derived metrics."""
    from hugpy_core.brain.intent import SQL as INTENT
    try:
        limit = max(1, min(500, int(kwargs.get("limit") or 100)))
        before = int(kwargs["before"]) if kwargs.get("before") else None
    except (TypeError, ValueError):
        return _json({"error": "limit and before must be integers"}, 400)
    where, params = [], []
    for column in ("request_id", "model_name", "worker", "task", "call_state"):
        if kwargs.get(column):
            where.append(f"{column} = %s")
            params.append(kwargs[column])
    if kwargs.get("intent"):
        where.append(f"{INTENT} = %s")
        params.append(kwargs["intent"])
    if kwargs.get("parent_request_id"):
        where.append("request_params->>'parent_request_id' = %s")
        params.append(kwargs["parent_request_id"])
    load_kind = kwargs.get("load")
    if load_kind == "initial":
        where.append("weights_loaded_at >= received_at")
    elif load_kind == "reused":
        where.append("(request_params->>'reused_resident' = 'true' OR weights_loaded_at < received_at)")
    if kwargs.get("hop"):
        where.append("request_params->>'hop' = %s")
        params.append(kwargs["hop"])
    if before is not None:
        where.append("id < %s")
        params.append(before)
    clause = " WHERE " + " AND ".join(where) if where else ""
    # PostgreSQL serializes its own types: timestamps retain their precision,
    # JSON stays nested, and SQL NULL remains JSON null. Select the WHOLE row.
    records = _ie("SELECT id, to_jsonb(c)::text FROM call_log c" + clause +
                  " ORDER BY id DESC LIMIT %s", tuple(params + [limit + 1]))
    more = len(records) > limit
    records = records[:limit]
    columns = [r[0] for r in _ie("SELECT column_name FROM information_schema.columns "
                "WHERE table_schema='public' AND table_name='call_log' ORDER BY ordinal_position")]
    # Keep exact numeric JSON from the DB instead of converting through floats.
    body = '{"calls":[' + ','.join(r[1] for r in records) + '],"columns":' + json.dumps(columns)
    body += ',"count":' + str(len(records)) + ',"next_before":' + json.dumps(records[-1][0] if more else None)
    body += ',"path":"hugpy_wrapper.call_log"}'
    return Response(body, mimetype="application/json", headers={"Cache-Control": "no-store"})


def llm_call_intents(**kwargs):
    """Every intent on record with its call count (the filter's choices)."""
    from hugpy_core.brain.intent import SQL as INTENT
    rows = _ie(f"SELECT {INTENT} AS i, count(*), extract(epoch FROM max(received_at))"
               " FROM call_log_derived WHERE %s GROUP BY 1 ORDER BY 2 DESC", (True,))
    return jsonify({"intents": [{"intent": r[0], "calls": int(r[1]),
                                 "last_at": float(r[2]) if r[2] is not None else None}
                                for r in rows]})


def workers_activity(worker_id=None, **kwargs):
    """``worker_id`` was the path param (/fleet/workers/<worker_id>/activity); now a kwarg."""
    w = registry.lookup_worker(worker_id)
    if w is None:
        return _json({"ok": False, "error": f"no worker {worker_id!r}", "activity": []}, 404)
    try:
        return jsonify({"ok": True, "activity": worker_activity(w)})
    except Exception as exc:  # noqa: BLE001
        return _json({"ok": False, "error": f"{type(exc).__name__}: {exc}", "activity": []}, 503)


def workers_health(worker_id=None, **kwargs):
    """``worker_id`` was the path param (/fleet/workers/<worker_id>/health); now a kwarg."""
    w = registry.lookup_worker(worker_id)
    if w is None:
        return _json({"reachable": False, "error": f"no worker {worker_id!r}"}, 404)
    url = (w.get("url") or "").rstrip("/") + "/health"
    try:
        with urllib.request.urlopen(url, timeout=4) as r:
            return jsonify({"reachable": True, "url": url, "health": json.loads(r.read() or b"{}")})
    except Exception as exc:  # noqa: BLE001
        return jsonify({"reachable": False, "url": url, "error": f"{type(exc).__name__}: {exc}"})


def models_status(**kwargs):
    return jsonify(model_status_payload())


# The event stream's worker rows (operator 2026-10-27: /api/llm/events moved ~3 MB on every
# connect and on every worker change). The console reads only membership from
# models_central, a few marker fields from models_discovered and nothing from
# model_pair_settings, so the stream carries those slim; REST views keep the full rows.
_STREAM_MARKER_FIELDS = ("primary_task", "framework", "tasks", "moe_capable")


def _stream_marker(entry):
    hj = entry.get("hugpy_json") if isinstance(entry, dict) else None
    hj = hj if isinstance(hj, dict) else {}
    keep = {k: hj[k] for k in _STREAM_MARKER_FIELDS if k in hj}
    hub = hj.get("hub")
    if isinstance(hub, dict) and hub.get("pipeline_tag"):
        keep["hub"] = {"pipeline_tag": hub["pipeline_tag"]}
    return {"hugpy_json": keep}


def stream_worker(row: dict) -> dict:
    row = dict(row)
    row.pop("model_pair_settings", None)
    central = row.get("models_central")
    if isinstance(central, dict):
        row["models_central"] = {key: True for key in central}
    discovered = row.get("models_discovered")
    if isinstance(discovered, dict):
        row["models_discovered"] = {key: _stream_marker(entry) for key, entry in discovered.items()}
    return row


def llm_events(**kwargs):
    """SSE: the full snapshot on connect, then a fresh one the moment the
    registry changes (a worker registers or heartbeats) or the boxes' DB state
    changes (residents / call_log / gpu_state triggers, via live.py). No polling."""
    from hugpy_core.registry import live
    from hugpy_core.web.routes import snapshot_feeds
    live._ensure()

    def feeds_now() -> dict:
        feeds = dict(snapshot_feeds())
        feeds["workers"] = [stream_worker(w) for w in feeds.get("workers") or []]
        return feeds

    def gen():
        seen, cv = registry.version(), live.console_version()
        feeds = feeds_now()
        feeds["liveness"] = liveness_feed()
        gpu = live.gpu_feed()
        feeds["gpu_state"] = gpu
        feeds["activity"] = gpu.get("activity", {})
        feeds["call_log_version"] = cv
        # what this stream last sent per feed: a wake re-sends only the feeds
        # whose content changed (a heartbeat that moves nothing costs nothing)
        last = {name: _feed_sig(name, payload) for name, payload in feeds.items()}
        yield "event: snapshot\ndata: " + json.dumps({"ts": time.time(), "versions": {"workers": seen},
                                                      "feeds": feeds}, default=str) + "\n\n"
        started = quiet = time.time()
        while time.time() - started < 3600:
            v = registry.wait_change(seen, 15.0)
            ncv = live.console_version()
            # registry / residents / call_log changes rebuild the heavy feeds;
            # a card-only change (gpu_state) re-diffs just its own small feed
            candidates = feeds_now() if (v != seen or ncv != cv) else {}
            seen, cv = v, ncv
            candidates["liveness"] = liveness_feed()
            gpu = live.gpu_feed()
            candidates["gpu_state"] = gpu
            candidates["activity"] = gpu.get("activity", {})
            candidates["call_log_version"] = cv
            sent = False
            for name, payload in candidates.items():
                body = _feed_sig(name, payload)
                if last.get(name) == body:
                    continue
                last[name] = body
                sent = True
                yield "event: feed\ndata: " + json.dumps({"feed": name, "version": v, "updated": time.time(),
                                                          "payload": payload}, default=str) + "\n\n"
            if sent:
                quiet = time.time()
            elif time.time() - quiet >= 15:
                quiet = time.time()
                yield ": keepalive\n\n"
    return Response(stream_with_context(gen()), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


def readiness(**kwargs):
    """The console's landing / health probe: hugpy_core is up; serving and
    storage are read live (registry + the model drive)."""
    import os
    from hugpy_core.web.routes import catalog_rows
    root = os.environ.get("HUGPY_CORE_STORAGE_ROOT", "/mnt/16T_toshiba/llm_storage")
    st = os.statvfs(root) if os.path.isdir(root) else None
    online = [w for w in registry.all_workers() if registry.is_online(w)]
    serving = any((w.get("loaded_models") or []) for w in online)
    return jsonify({
        "central": {"auth_mode": "open", "version": "hugpy_core"},
        "connect": {"base_url": request.host_url.rstrip("/")},
        "console": {"configured": True, "url": None},
        "serving": {"any_serving": serving, "enabled": bool(online), "slots": [],
                    "workers_online": len(online)},
        "storage": {"exists": st is not None, "root": root,
                    "free_bytes": (st.f_bavail * st.f_frsize) if st else None,
                    "free_gb": round(st.f_bavail * st.f_frsize / 1e9, 1) if st else None,
                    "writable": os.access(root, os.W_OK), "model_count": len(catalog_rows())},
    })


# /llm/model-groups moved to model_groups.py (DB-backed, sql/019, 2026-10-06)

def models_notes(**kwargs):
    return jsonify({"flags": NOTE_FLAGS, "notes": {}})


def fleet_distribution(**kwargs):
    return jsonify({"env_override": False, "mode": "feasible", "source": "default", "stored": None})


def enroll_tokens(**kwargs):
    return jsonify([])


def session_lease(session_id=None, **kwargs):
    """``session_id`` was the path param (/llm/sessions/<session_id>/lease); now a kwarg."""
    return jsonify({"ok": True, "session_id": session_id, "state": kwargs.get("state") or "active",
                    "lease_fresh": True})


# category -> {route_name: callable}. /arms and /readiness are single-segment
# routes (no category/route_name split); the web_bp aggregator registers those
# two directly, so they are intentionally NOT listed here.
CONSOLE_CATEGORIES = {
    "console": {"bootstrap": console_bootstrap, "schema": console_schema},
    # Inference and call feeds stay under llm; worker observations join the
    # recursively merged fleet/workers tree below.
    "llm": {
        "queue": spec(llm_queue, "GET", response="native"),
        "central-provisioning": central_provisioning,
        "grades": llm_grades,
        "model-metrics2": model_metrics2,
        "calls": {"": llm_calls, "raw": llm_calls_raw, "intents": llm_call_intents},
        "events": llm_events,
        "enroll-tokens": enroll_tokens,
        "benchmark": {"suites": grading_suites},
        "models": {"metrics": model_graded_calls, "status": models_status},
        "fleet": {"distribution": fleet_distribution},
        "sessions": {"lease": session_lease},
    },
    # The query form (/fleet/workers/activity?worker_id=) and the path form
    # (/fleet/workers/<worker_id>/activity) are the SAME handler: the ``<worker_id>``
    # key is a path parameter that reaches ``workers_activity`` as the same-named
    # kwarg (merged with the body, URL identity winning), while the query form
    # feeds it from ?worker_id=. The path form answers BARE JSON (response=
    # "native") with a 404 for an unknown worker, exactly as the console reads it.
    "fleet": {"workers": {"activity": workers_activity, "health": workers_health,
                    "<worker_id>": {"activity": spec(workers_activity, "GET", response="native"),
                                    "health": spec(workers_health, "GET", response="native")}}},
    "models": {"notes": models_notes},
}
