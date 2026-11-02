# LIFTED from legacy hugpy (read-only references):
#   py/services/hugpy_server/src/hugpy_server/app/routes/review_routes.py
#   py/services/hugpy_server/src/hugpy_server/app/routes/metrics_routes.py
#   py/packages/hugpy_curation/src/hugpy_curation/review/fleet_grading.py
#
# LIFTED VERBATIM (shape-preserving):
#   - the transient benchmark state dict and lock,
#     _benchmark_run_summary / benchmark_runs / benchmark_run_get, _benchmark_public,
#     benchmark_status/run/judge/cancel/events routes and their JSON shapes;
#   - _benchmark_failure_summary (pure);
#   - the fleet_grading RESULT row and CALL row shapes (status/complete, grade
#     "score/max", detail{category:{tier,max,history[]}}, call grade PASS/FAIL/ERROR,
#     prompt/expected/expected_answer/actual/why) the Metrics workbook reads;
#   - the /llm/benchmark/suites registry entry shape and /llm/compute-actions row shape.
#
# SWAPPED (the integration points — the new build has none of the legacy infra):
#   - the run loop: legacy delegated to a hugpy-agent on :7002 via
#     fleet_grading.run_capacity_benchmark + a loopback Client. Core runs the plan
#     ITSELF over core's own pick() + relay.worker_stream, pinned per worker, with
#     grader.py's deterministic text suite (grader.CURRICULUM / check). No HTTP
#     loopback to any central.
#   - persistence: legacy wrote model_metrics / model_calls in the retired `hugpy`
#     Postgres DB. Here the grade goes to hugpy_core's `grades` table (grader.record,
#     the pointer into hugpy_wrapper.call_log.request_id) and the call itself is
#     logged by the wrapper's call_log on the normal relay path — the single source
#     of truth. The legacy _persist_benchmark_* / _ColdStore / cold-split columns and
#     the cross-process resume/owner election are DROPPED (core is one process).
#   - benchmark history is the core request row, with execution call pointers.
#   - suite registry: derived from grader.TASKS_TIERED (the only suite core has);
#     the vision + imagegen suites are listed UNAVAILABLE with a reason (no vision
#     chat path wired, no image backend — ComfyUI retired).
#   - compute-actions: derived from hugpy_wrapper.resource_log (action='load',
#     phase='failed') + call_log (http_status<>200, error LIKE 'load failed%').
#   - judge (LLM-as-judge): legacy called agents on a retired VM/:7002. Core routes
#     a judge through its own pick+relay only when HUGPY_CORE_JUDGE_MODEL is set;
#     unset (the default) = judge disabled, said so with a clear status (never a
#     legacy URL). The deterministic checkers are authoritative.
#
# DROPPED (feature paths that depend on forced downloads/placement, which hugpy_core
# must never do — reported with a clear JSON error, never HTML, never a 500):
#   - the review DISCOVERY pipeline (HF search -> screen -> download weights ->
#     smoke-load -> judge) and its criteria/dossier/radar/ingest store. Core does not
#     fetch weights or force placement, so /llm/review/{screen,run,criteria PUT} answer
#     501 with the reason; /llm/review/{status,runs,results,criteria GET} answer their
#     empty shape; /llm/review/dossier answers 404 with the reason.
"""The console's Grader + Metrics benchmark surface, served by hugpy_core.

The Fleet capacity test is REAL here: it grades every selected (model, worker)
through core's own placement (pick) + relay, with grader.py's deterministic
checkers, writing one `grades` row per item and logging each call to the
wrapper's call_log. The model-discovery REVIEW pipeline (download + smoke) is a
hugpy responsibility that forces no downloads in core, so it is reported
unavailable rather than faked.
"""
from __future__ import annotations

import json
import logging
import os
import re
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed


from hugpy_core.grading import grader

logger = logging.getLogger("hugpy_core.grading.review")

JUDGE_MODEL = (os.environ.get("HUGPY_CORE_JUDGE_MODEL") or "").strip() or None

# ── benchmark state (lifted shape) ───────────────────────────────────────────
_BENCHMARK = {"status": "idle", "events": [], "results": [], "calls": [],
              "summary": {},
              "plan": {"rows": [], "total": 0, "runnable": 0},
              "progress": {"completed": 0, "total": 0, "percent": 0}}
_BENCHMARK_LOCK = threading.RLock()
_BENCHMARK_ACTIVE = ("running", "resuming", "judging")
_PROCESS_STARTED = time.time()


def _benchmark_save() -> None:
    """Update core's own call; execution facts remain behind call pointers."""
    from hugpy_core.grading import benchmark_log
    from hugpy_core.calllog import call_record
    row = _BENCHMARK.get("_call_row")
    if row is None:
        return
    row["response_body"] = benchmark_log.compact(_benchmark_public())
    status = _BENCHMARK.get("status")
    if status in _BENCHMARK_ACTIVE:
        call_record.write(row)
    else:
        error = _BENCHMARK.get("error")
        call_record.finish(row, 499 if status == "cancelled" else
                           500 if status == "interrupted" else 422 if error else 200,
                           json.dumps(error) if isinstance(error, dict) else error)


def _benchmark_updated(now=None) -> None:
    _BENCHMARK["updated"] = now or time.time()
    _benchmark_save()


def _benchmark_public() -> dict:
    with _BENCHMARK_LOCK:
        row = {k: v for k, v in _BENCHMARK.items() if k not in {"thread", "control"} and not k.startswith("_")}
        row["events"] = list(row.get("events", []))     # whole; never a tail
        row["results"] = list(row.get("results", []))
        return row


def _benchmark_run_summary(row: dict) -> dict:
    err = row.get("error")
    return {"run_id": row.get("run_id"), "request_id": row.get("request_id"), "status": row.get("status"), "started": row.get("started"),
            "finished": row.get("finished"), "updated": row.get("updated"), "models": row.get("models") or [],
            "workers": row.get("workers") or [], "results": len(row.get("results") or []),
            "calls": len(row.get("calls") or []),
            "error": err.get("headline") if isinstance(err, dict) else err}


def benchmark_runs():
    """Benchmark history projected from core call records."""
    from hugpy_core.grading.benchmark_log import runs
    try:
        return {"runs": [_benchmark_run_summary(r) for r in runs()],
                "source": "call_log", "errors": []}
    except Exception as exc:
        return {"runs": [], "source": "call_log", "error": str(exc)}, 503


def benchmark_run_get(run_id=None):
    """One benchmark run by id (the ``<run_id>`` of /llm/benchmark/runs/<run_id>)."""
    from hugpy_core.grading.benchmark_log import runs
    if not re.fullmatch(r"[0-9a-f]{6,32}", run_id or ""):
        return {"error": f"run id {run_id!r} is not a hex run id"}, 400
    try:
        rows = runs(run_id=run_id)
        if rows:
            return rows[0]
        return {"error": f"no call-log record for benchmark {run_id}"}, 404
    except Exception as exc:
        return {"error": str(exc)}, 503


def benchmark_status():
    """Current capacity benchmark, including live per-config results. A run whose
    thread died with a stale heartbeat is marked interrupted (core is one process;
    there is no cross-process resume to elect)."""
    with _BENCHMARK_LOCK:
        if not _BENCHMARK.get("run_id"):
            from hugpy_core.grading.benchmark_log import runs
            try:
                saved = runs(limit=1)
                if saved:
                    _BENCHMARK.update(saved[0])
            except Exception:
                logger.exception("Could not restore benchmark from call_log")
        th = _BENCHMARK.get("thread")
        alive = th is not None and th.is_alive()
        if (_BENCHMARK.get("status") in _BENCHMARK_ACTIVE and not alive
                and time.time() - float(_BENCHMARK.get("heartbeat") or 0) > 45):
            _BENCHMARK.update(status="interrupted", finished=time.time(),
                              error="benchmark thread ended without finishing (heartbeat expired)")
            _benchmark_updated()
    return _benchmark_public()


def benchmark_events(tail=None):
    """Every event of the current/last run, whole (the status read is already
    whole here too, but the panel fetches this to be sure). ?tail=N for the last N."""
    with _BENCHMARK_LOCK:
        events = list(_BENCHMARK.get("events") or [])
        run_id = _BENCHMARK.get("run_id")
    total = len(events)
    try:
        n = int(tail) if tail not in (None, "") else 0
    except (TypeError, ValueError):
        n = 0
    return {"run_id": run_id, "events": events[-n:] if n > 0 else events, "count": total}


def benchmark_run(models=None, workers=None, tokens=128, measure_cold_load=False,
                  executor="hugpy-central", concurrency=8, supervisor_model=None, review_interval_s=None):
    """Start the capacity test: grade the selected models on the selected workers
    through core's own placement. Body: models[], workers[], tokens, measure_cold_load.
    202 with the run state, or 409 with the active run if one is in flight."""
    try:
        tokens = max(8, min(2048, int(tokens if tokens not in (None, "") else 128)))
        concurrency = max(1, min(32, int(concurrency)))
        review_interval_s = max(10, min(3600, float(review_interval_s or os.environ.get("HUGPY_GRADER_REVIEW_INTERVAL_S") or 60)))
    except (TypeError, ValueError):
        return {"error": "tokens/concurrency must be integers and review_interval_s a number"}, 400
    if supervisor_model is not None and (not isinstance(supervisor_model,str) or not supervisor_model.strip()):
        return {"error":"supervisor_model must be a nonempty model key"},400
    params = {"tokens": tokens, "concurrency": concurrency,
              "supervisor_model": supervisor_model, "review_interval_s": review_interval_s,
              "models": [str(v) for v in (models or []) if v],
              "workers": [str(v) for v in (workers or []) if v],
              "measure_cold_load": bool(measure_cold_load)}
    with _BENCHMARK_LOCK:
        if _BENCHMARK.get("status") in _BENCHMARK_ACTIVE:
            return _benchmark_public(), 409
        from flask import g
        from hugpy_core.calllog.call_record import current
        call_row = current()
        run_id = uuid.uuid4().hex[:12]
        call_row["request_body"].setdefault("metadata", {})["benchmark"] = {"run_id": run_id}
        g.call_async = True
        _BENCHMARK.clear()
        _BENCHMARK.update({"run_id": run_id, "request_id": call_row["request_id"],
                           "_call_row": call_row, "status": "running", "executor": executor,
                           "started": time.time(), "finished": None, "tokens": tokens,
                           "heartbeat": time.time(), "params": params,
                           "models": list(params["models"]), "workers": list(params["workers"]),
                           "events": [], "results": [], "calls": [], "summary": {},
                           "plan": {"rows": [], "total": 0, "runnable": 0},
                           "progress": {"completed": 0, "total": 0, "percent": 0}, "report": None})
        _benchmark_updated()
    _start_benchmark_thread(run_id, params)
    return _benchmark_public(), 202


def benchmark_judge():
    """PHASE 2 (LLM-as-judge) for the collected run. In hugpy_core the deterministic
    checkers are authoritative; a brain judge runs only when HUGPY_CORE_JUDGE_MODEL
    is set (it never routes to a legacy URL). Unset = disabled, said so (409)."""
    with _BENCHMARK_LOCK:
        status = _BENCHMARK.get("status")
        run_id = _BENCHMARK.get("run_id")
        results = [r for r in (_BENCHMARK.get("results") or []) if isinstance(r, dict)]
    if status in _BENCHMARK_ACTIVE:
        return ({"status": status, "run_id": run_id,
                        "reason": f"run is {status}; judging is already scheduled"}, 409)
    if not run_id or not results:
        return ({"status": status, "run_id": run_id,
                        "reason": "no collected run to judge"}, 409)
    if not JUDGE_MODEL:
        return ({"status": status, "run_id": run_id,
                        "reason": ("LLM-as-judge is disabled in hugpy_core (the deterministic "
                                   "checkers are authoritative); set HUGPY_CORE_JUDGE_MODEL to a "
                                   "fleet model key to enable it")}, 409)
    return ({"status": status, "run_id": run_id,
                    "reason": (f"judge model {JUDGE_MODEL!r} is configured but the core judge pass "
                               "is not yet wired; the deterministic grade stands")}, 409)


def benchmark_cancel(scope="execution", worker_id=None, model=None, quant=None, call=None):
    """Cancel the whole execution (scope execution) — the only scope core runs.
    Sets the control flag the run loop checks between items."""
    scope = scope or "execution"
    if scope not in {"call", "quant", "model", "worker", "execution"}:
        return {"error": "scope must be call, quant, model, worker, or execution"}, 400
    target = {k: v for k, v in (("worker_id", worker_id), ("model", model), ("quant", quant), ("call", call)) if v}
    with _BENCHMARK_LOCK:
        control = _BENCHMARK.get("control")
        if _BENCHMARK.get("status") not in _BENCHMARK_ACTIVE or control is None:
            return {"status": "not_running"}, 409
        control.set()
        _BENCHMARK.update(cancel_requested=True, cancelled_at=time.time())
        _BENCHMARK.setdefault("events", []).append(
            {"at": time.time(), "kind": "cancel", "message": "cancelled %s" % scope, "scope": scope,
             "target": target})
        _benchmark_updated()
        cancel_lanes = _BENCHMARK.get("_cancel_lanes")
    if cancel_lanes: cancel_lanes()
    return _benchmark_public()


# ── the capacity run (SWAP: core's own pick + relay, grader's text suite) ─────
def _bench_call(model_key: str, worker_name: str, prompt: str, max_tokens: int, run_id: str,
                item: "dict | None" = None) -> dict:
    """One grading call through core's placement, pinned to ``worker_name``. The
    same path a client hits (pick -> worker_stream); the wrapper logs it to
    call_log under ``request_id``. Returns the reply text, timings and the id."""
    from hugpy_core.relay.pick import NoWorker, pick
    from hugpy_core.relay.relay import WorkerHTTPError, worker_payload, worker_stream
    request_id = f"bench-{run_id}-{uuid.uuid4().hex[:8]}"
    from .supervisor import current
    supervised = current()
    if supervised: supervised.begin_call(request_id)
    started = time.time()
    text_parts, error_message, usage, timings, worker_seen = [], None, None, None, None
    execution_id = None
    from hugpy_core.calllog.call_record import start, finish, write
    body = {"model_key": model_key, "request_id": request_id, "task": "text-generation",
            "messages": [{"role": "user", "content": prompt}], "max_new_tokens": int(max_tokens),
            "temperature": 0.0, "metadata": {"intent": "grading", "benchmark": {"run_id": run_id},
                                           "parent_request_id": request_id}}
    if item:    # the item asked rides the call: its grade derives from the call log alone
        body["metadata"]["grade"] = {k: item[k] for k in ("suite", "category", "tier")}
    row = start(body, "/infer/stream", request_id=request_id,
                parent=_BENCHMARK.get("request_id"), caller="benchmark")
    row["worker"] = worker_name
    try:
        w = pick(model_key, pin=worker_name, source="grading")
        worker_seen = w.get("name")
        wp = worker_payload(body, w)
        row.update(worker=worker_seen, forwarded_at=time.time())
        write(row)
        for ev in worker_stream(w, wp, timeout=600):
            execution_id = ev.get("execution_request_id") or execution_id
            t = ev.get("type")
            if t == "token":
                if supervised: supervised.token()
                text_parts.append(ev.get("text") or "")
            elif t == "done":
                usage, timings = ev.get("usage"), ev.get("timings")
            elif t == "error":
                error_message = ev.get("message") or "error"
    except (NoWorker, WorkerHTTPError) as exc:
        error_message = str(exc)
    except Exception as exc:  # noqa: BLE001 — a relay error is a result, not a crash
        error_message = f"{type(exc).__name__}: {exc}"
    elapsed = round(time.time() - started, 4)
    content = "".join(text_parts)
    if "[error:" in content and not error_message:
        error_message = content[:2000]
    comp = usage.get("completion_tokens") if isinstance(usage, dict) else None
    prompt_toks = usage.get("prompt_tokens") if isinstance(usage, dict) else None
    tok_s = None
    if isinstance(timings, dict):
        call = timings.get("call") if isinstance(timings.get("call"), dict) else None
        for cand in ((call or {}).get("tok_per_s"), timings.get("predicted_per_second")):
            if cand is not None:
                try:
                    tok_s = round(float(cand), 2); break
                except (TypeError, ValueError):
                    pass
    if not error_message and not execution_id:
        error_message = "No execution call-log pointer returned"
    row["response_meta"] = {"execution_request_id": execution_id}
    finish(row, 502 if error_message else 200, error_message,
           {"text": content, "usage": usage})
    if supervised: supervised.end_call(error_message)
    return {"core_request_id": request_id, "request_id": execution_id or request_id, "worker": worker_seen, "text": content,
            "error": str(error_message)[:2000] if error_message else None, "elapsed_s": elapsed,
            "tok_s": tok_s, "ctx_in": prompt_toks, "ctx_out": comp}


def _eligible(w: dict) -> bool:
    return (w.get("status") == "online" and not w.get("unreachable")
            and w.get("admission") == "approved" and w.get("serve_mode") != "off")


def _bench_workers(requested: list) -> list:
    """The selected eligible workers, in the UI shape (same eligibility predicate
    the Grader's worker checklist uses)."""
    from hugpy_core.registry import registry
    from hugpy_core.web.routes import gpu_process_map, ui_worker
    gp = gpu_process_map()
    workers = registry.all_workers()
    rows = [ui_worker(w, gp, workers) for w in workers]
    rows = [r for r in rows if _eligible(r)]
    if requested:
        want = set(requested)
        rows = [r for r in rows if r.get("id") in want or r.get("name") in want]
    return rows


def _bench_models(requested: list) -> list:
    """The selected text-gen catalog rows (what online workers discovered)."""
    from hugpy_core.web.routes import catalog_rows
    text = {"text-generation", "text2text-generation"}
    rows = []
    for r in catalog_rows():
        tasks = set(r.get("tasks") or [])
        if r.get("primary_task"):
            tasks.add(r["primary_task"])
        if r.get("task"):
            tasks.add(r["task"])
        if tasks & text:
            rows.append(r)
    if requested:
        want = set(requested)
        rows = [r for r in rows if r.get("model_key") in want]
    return rows


def _failure_summary(results, plan, params, started_at=None) -> dict:
    """Why a run produced no completed allocation, from its own rows (lifted)."""
    by_class = {}
    for r in results:
        cls = r.get("failure_class") or r.get("status") or "unknown"
        entry = by_class.setdefault(cls, {"count": 0, "models": [], "first_reason": None})
        entry["count"] += 1
        if r.get("model") and r["model"] not in entry["models"]:
            entry["models"].append(r["model"])
        if entry["first_reason"] is None:
            entry["first_reason"] = r.get("reason") or r.get("error") or r.get("constraint_reason")
    planned, runnable = plan.get("total", 0), plan.get("runnable", 0)
    requested = (params or {}).get("models") or []
    if not results and not planned:
        headline = (f"nothing was graded: {len(requested) or 'all'} model(s) requested, 0 lanes planned "
                    f"(no eligible worker had a selected model)")
    elif not results:
        headline = f"nothing was graded: {planned} lane(s) planned, {runnable} runnable, 0 rows recorded"
    else:
        parts = ", ".join(f"{v['count']} {k}" for k, v in by_class.items())
        headline = f"0 of {len(results)} allocation(s) completed: {parts}"
    elapsed = round(time.time() - started_at, 1) if isinstance(started_at, (int, float)) else None
    if elapsed is not None:
        headline += f" — {elapsed} s spent"
    return {"headline": headline, "planned": planned, "runnable": runnable,
            "requested_models": requested, "elapsed_s": elapsed, "failure_classes": by_class}


def _start_benchmark_thread(run_id: str, params: dict):
    control = threading.Event()
    with _BENCHMARK_LOCK:
        _BENCHMARK["control"] = control

    def report(kind, value):
        with _BENCHMARK_LOCK:
            if _BENCHMARK.get("run_id") != run_id:
                return
            _BENCHMARK["heartbeat"] = time.time()
            if kind == "result" and isinstance(value, dict):
                _BENCHMARK.setdefault("results", []).append(value)
            elif kind == "call" and isinstance(value, dict):
                _BENCHMARK.setdefault("calls", []).append(value)
            elif kind in {"plan", "progress", "summary"} and isinstance(value, dict):
                _BENCHMARK[kind] = value
                if kind == "plan":
                    _BENCHMARK.setdefault("progress", {})["total"] = value.get("runnable", 0)
            else:
                _BENCHMARK.setdefault("events", []).append(
                    {"at": time.time(), "kind": kind, "value": value,
                     "message": value if isinstance(value, str) else None})
            _benchmark_updated()

    def work():
        status, error = "failed", "benchmark did not run"
        try:
            workers = _bench_workers(params.get("workers") or [])
            models = _bench_models(params.get("models") or [])
            tokens = params.get("tokens") or 128
            suite = grader.SUITE
            # Plan: one lane per (model, worker). Only workers that actually serve
            # the model make a runnable lane (core never forces a download).
            from hugpy_core.relay.pick import _serves  # noqa: WPS437 — same serve predicate as pick()
            from hugpy_core.relay.pick import model_key_forms, _central_has
            plan_rows, lanes = [], []
            for m in models:
                mk = m["model_key"]
                wanted = model_key_forms(mk)
                quant = m.get("quant") or "runtime default"
                for w in workers:
                    from hugpy_core.registry import registry
                    raw = registry.lookup_worker(w.get("id") or w.get("name"))
                    runnable = bool(raw and (_serves(raw, mk, wanted) or _central_has(mk)))
                    row = {"worker": w.get("name"), "worker_id": w.get("id"), "model": mk,
                           "quant": quant, "config": "standard", "alloc_mode": "auto",
                           "runnable": runnable, "grade_suite": suite,
                           "status": "N/A" if runnable else "hardware_constraint_failed",
                           "constraint_reason": None if runnable else (
                               f"worker {w.get('name')} does not have {mk} on disk and no central source is available"),
                           "disk_bytes": m.get("size_bytes"), "grade": "N/A", "tok_s": "N/A"}
                    plan_rows.append(row)
                    if runnable:
                        lanes.append((m, w, quant))
            total = sum(1 for r in plan_rows if r["runnable"])
            report("plan", {"total": len(plan_rows), "runnable": total,
                            "workers": len({r["worker_id"] for r in plan_rows}), "rows": plan_rows})
            # Non-runnable lanes are recorded immediately as constrained results,
            # and each is handed to the brain for a determination (operator
            # 2026-10-06): where the model is, and the pull/reroute that fixes it.
            for r in plan_rows:
                if not r["runnable"]:
                    try:
                        from hugpy_core.brain import brain
                        r["brain"] = brain.constraint_and_file(r["model"], r["worker"], r["constraint_reason"])
                    except Exception as exc:  # noqa: BLE001 — the determination never fails the run
                        logger.warning("brain allocation evaluation failed: %s", exc)
                    report("result", {**r, "matrix": True, "ok": False, "detail": {}})
            from . import lifecycle, supervisor
            supervision = supervisor.Supervisor(run_id,report,params.get('supervisor_model'),params.get('review_interval_s'))

            def execute_lane(m,w,quant,state):
                mk, wname = m["model_key"], w.get("name")
                base = {"worker": wname, "worker_id": w.get("id"), "model": mk, "quant": quant,
                        "config": "standard", "alloc_mode": "auto", "grade_suite": suite,
                        "grade_task": "text-generation"}
                detail, calls, speeds = {}, [], []
                hard_error = None
                for cat, tiers in grader.TASKS_TIERED.items():
                    if control.is_set() or state.stop.is_set() or hard_error:
                        break
                    history = []
                    for tier, prompt, checker in tiers:
                        if control.is_set() or state.stop.is_set() or hard_error:
                            break
                        item = {"suite": suite, "category": cat, "tier": tier,
                                "prompt": prompt + grader.NO_THINK}
                        for attempt in range(2):
                            generation=supervision.generation(state)
                            res = _bench_call(mk, wname, item["prompt"], tokens, run_id, item)
                            err = res.get("error")
                            if not err:
                                break
                            if lifecycle.capacity_error(err):
                                if not attempt and supervision.wait_capacity(state,control,generation):
                                    continue
                                break
                            verdict = supervision.review(state)
                            fatal = any(term in str(err).lower() for term in
                                        ('load failed', 'conversion of the weights', 'unsupported', 'out of memory'))
                            if fatal or attempt or state.stop.is_set() or control.is_set() or not verdict or verdict['decision'] != 'continue':
                                break
                        if err:
                            passed, answer, why = None, None, f"call failed: {err}"
                        else:
                            passed, answer, why = grader.check(item, res.get("text") or "")
                        try:
                            grader.record(mk, item, worker=res.get("worker") or wname, quant=quant,
                                           request_id=res.get("request_id"), passed=passed,
                                           answer=answer, why=why, source="benchmark")
                        except Exception:  # noqa: BLE001 — a grade-write fault never fails the run
                            logger.exception("benchmark grade write failed for %s/%s", mk, cat)
                        expected = getattr(checker, "rule", None)
                        expected_answer = getattr(checker, "answer", None)
                        if res.get("tok_s"):
                            speeds.append(res["tok_s"])
                        item_row = {"tier": tier, "pass": bool(passed), "check_pass": bool(passed),
                                    "format": (bool(passed) if not err else None), "revised": False,
                                    "prompt": prompt, "expected": expected,
                                    "expected_answer": expected_answer, "actual": answer,
                                    **({"why": why} if why else {})}
                        history.append(item_row)
                        call = {**base, "task": f"{cat} ({tier})", "timestamp": time.time(),
                                "elapsed_s": res.get("elapsed_s"), "tok_s": res.get("tok_s") or "N/A",
                                "tok_s_avg": res.get("tok_s") or "N/A", "ctx_in": res.get("ctx_in"),
                                "ctx_out": res.get("ctx_out"), "caller": "orchestrator",
                                "output": res.get("text"),
                                "grade": "ERROR" if err else "PASS" if passed else "FAIL",
                                "passed": bool(passed), "error": err or "N/A", "check_pass": bool(passed),
                                "prompt": prompt, "expected": expected, "expected_answer": expected_answer,
                                "actual": answer, "request_id": res.get("request_id"),
                                "core_request_id": res.get("core_request_id"),
                                **({"why": why} if why else {})}
                        calls.append(call)
                        report("call", call)
                        if err and hard_error is None:
                            hard_error = err
                    detail[cat] = {"tier": sum(1 for x in history if x["pass"]), "max": 3,
                                   "format": sum(1 for x in history if x.get("format") is True),
                                   "revised": 0, "history": history}
                if state.reason and not hard_error: hard_error = state.reason
                answered = [c for c in calls if c.get("grade") in ("PASS", "FAIL")]
                if not answered:
                    first = hard_error or "no graded call was made"
                    result = {**base, "matrix": True, "ok": False, "status": "failed",
                              "failure_class": "error", "grade": "N/A", "tok_s": "N/A", "detail": {},
                              "error": first, "reason": (f"no item answered ({len(calls)} call(s)); "
                                                         f"first error: {first}"), "finished": time.time()}
                    return result
                depths = {k: v["tier"] for k, v in detail.items()}
                score, maximum = sum(depths.values()), len(grader.CURRICULUM)
                speed = round(sum(speeds) / len(speeds), 2) if speeds else None
                result = {**base, "matrix": True, "ok": True, "status": "complete",
                          "grade": f"{score}/{maximum}", "score": score, "max": maximum, "detail": detail,
                          "task_best": max(depths, key=depths.get), "task_worst": min(depths, key=depths.get),
                          "cold_s": None, "cold_measured": False, "hot_load_s": None,
                          "tok_s": speed or "N/A", "tok_s_avg": speed or "N/A",
                          "metrics_complete": speed is not None, "error": "N/A", "finished": time.time(),
                          "judge": {"status": "unavailable",
                                    "reason": ("LLM-as-judge disabled in hugpy_core; the deterministic "
                                               "checkers are authoritative")}}
                if hard_error or state.stop.is_set() or control.is_set():
                    result.update(ok=False,status="failed" if not control.is_set() else "cancelled",
                                  failure_class="error",error=hard_error or state.reason or "grading cancelled")
                return result

            def run_lane(m,w,quant):
                state=supervisor.Lane(supervision,m['model_key'],w)
                token=supervisor._CURRENT.set(state)
                supervision.add(state)
                with supervision.lock: active=[lane.snapshot() for lane in supervision.lanes]
                report('progress',{'completed':completed,'total':total,'percent':round(100*completed/max(1,total),2),'active_lanes':active})
                base={'worker':w.get('name'),'worker_id':w.get('id'),'model':m['model_key'],
                      'quant':quant,'config':'standard','alloc_mode':'auto','grade_suite':suite}
                try:
                    if control.is_set():return
                    with lifecycle.lane(run_id,m,w,control,report) as endpoint:
                        state.endpoint=endpoint
                        result=execute_lane(m,w,quant,state)
                except Exception as exc:
                    result={**base,'matrix':True,'ok':False,'status':'failed','failure_class':'error',
                            'error':str(exc),'reason':str(exc),'grade':'N/A','detail':{},'finished':time.time()}
                finally:
                    supervision.remove(state)
                    supervisor._CURRENT.reset(token)
                report('result',result)

            completed=0
            with _BENCHMARK_LOCK:_BENCHMARK["_cancel_lanes"]=supervision.cancel
            supervision.start()
            try:
                # This bounds HTTP/thread fanout, not model fit. Every load goes
                # through the existing worker admission and eviction mechanisms.
                with ThreadPoolExecutor(max_workers=max(1,min(len(lanes),int(params.get('concurrency') or 8)))) as pool:
                    futures=[pool.submit(run_lane,*args) for args in lanes]
                    for future in as_completed(futures):
                        future.result()
                        completed+=1
                        with supervision.lock: active=[lane.snapshot() for lane in supervision.lanes]
                        report('progress',{'completed':completed,'total':total,
                                           'percent':round(100*completed/max(1,total),2),'active_lanes':active})
            finally:
                supervision.close()
                with _BENCHMARK_LOCK:_BENCHMARK.pop("_cancel_lanes",None)
            report("progress", {"completed": completed, "total": total,
                                "percent": round(100 * completed / max(1, total), 2)})
            with _BENCHMARK_LOCK:
                all_results = [r for r in _BENCHMARK.get("results", []) if isinstance(r, dict)]
                plan = dict(_BENCHMARK.get("plan") or {})
                started_at = _BENCHMARK.get("started")
            report("summary", {"execution": {"configurations": len(all_results)},
                               "workers": [w.get("name") for w in workers],
                               "models": [m["model_key"] for m in models],
                               "failures": sum(1 for r in all_results if r.get("failure_class"))})
            if control.is_set():
                status, error = "cancelled", None
            elif any(r.get("status") == "complete" for r in all_results):
                status, error = "complete", None
            else:
                status, error = "failed", _failure_summary(all_results, plan, params, started_at)
        except Exception as exc:  # noqa: BLE001 — a background failure stays visible
            logger.exception("capacity benchmark failed")
            status, error = "failed", f"{type(exc).__name__}: {exc}"
        with _BENCHMARK_LOCK:
            if _BENCHMARK.get("run_id") == run_id:
                _BENCHMARK.update(status=status, error=error, finished=time.time())
                _benchmark_updated()

    thread = threading.Thread(target=work, name=f"benchmark-{run_id}", daemon=True)
    with _BENCHMARK_LOCK:
        _BENCHMARK["thread"] = thread
    thread.start()
    return thread


# ── grading-suite registry (SWAP: derived from grader.TASKS_TIERED) ───────────
def suite_registry() -> list:
    items = {}
    for cat, tiers in grader.TASKS_TIERED.items():
        items[cat] = [{"tier": t[0], "prompt": t[1], "expected": getattr(t[2], "rule", None),
                       "expected_answer": getattr(t[2], "answer", None)} for t in tiers]
    text = {"name": grader.SUITE, "task": "text-generation",
            "serves_tasks": ["text-generation", "text2text-generation"], "tiers": 3, "legacy": False,
            "tasks": list(grader.TASKS_TIERED), "items": items, "max": len(grader.CURRICULUM),
            "available": True}
    vision = {"name": "hugpy-vision-v1", "task": "image-text-to-text", "serves_tasks": [], "tiers": 0,
              "legacy": False, "tasks": [], "items": {}, "max": None, "available": False,
              "error": ("vision grading is not wired in hugpy_core yet: it needs image content sent "
                        "through the chat path to a vision model, which has not been lifted")}
    imagegen = {"name": "hugpy-imagegen-v1", "task": "text-to-image", "serves_tasks": [], "tiers": 0,
                "legacy": False, "tasks": [], "items": {}, "max": None, "available": False,
                "error": ("no image backend in hugpy_core: ComfyUI is retired; text-to-image will be a "
                          "cinema-package module")}
    return [text, vision, imagegen]


def benchmark_suites():
    """Every grading suite: name, task, ordered tasks, tiers, max, and per item the
    prompt + expected answer. The console derives matrix columns + score denominators
    from this, never from constants."""
    try:
        return {"suites": suite_registry(), "generated_at": time.time()}
    except Exception as exc:  # noqa: BLE001
        return {"suites": [], "error": str(exc), "generated_at": time.time()}


# ── compute-actions (SWAP: derived from hugpy_wrapper load telemetry) ──────
def _ie(sql: str, params: tuple = ()) -> list:
    # resource_log + call_log read only through calllog.py (the one reader)
    from hugpy_core.calllog.calllog import query
    return query(sql, params)


def compute_actions(limit: int, model: str, worker: str) -> list:
    """Load failures a model's header reads: one row per failed load, newest first,
    from resource_log (action='load', phase='failed') and call_log (http_status<>200,
    error LIKE 'load failed%'). Shape matches the legacy compute-action rows."""
    rows = []
    mw = "%" + model.split("~")[-1] + "%" if model else None
    rl_where, rl_params = ["action = 'load'", "phase = 'failed'"], []
    if model:
        rl_where.append("(item ILIKE %s OR for_item ILIKE %s)")
        rl_params += [mw, mw]
    if worker:
        rl_where.append("worker = %s")
        rl_params.append(worker)
    for r in _ie(f"SELECT id, extract(epoch FROM at), worker, item, note, request_id FROM resource_log "
                 f"WHERE {' AND '.join(rl_where)} ORDER BY at DESC LIMIT %s", tuple(rl_params + [limit])):
        rows.append({"id": int(r[0]), "at": float(r[1]) if r[1] is not None else None,
                     "ts": float(r[1]) if r[1] is not None else None, "worker": r[2], "action": "load",
                     "outcome": "fail", "model": r[3], "model_name": r[3],
                     "error": r[4], "reason": r[4], "detail": {"message": r[4]} if r[4] else {},
                     "request_id": r[5], "source": "resource_log"})
    cl_where, cl_params = ["http_status IS NOT NULL", "http_status <> 200", "error ILIKE 'load failed%%'"], []
    if model:
        cl_where.append("model_name ILIKE %s")
        cl_params.append(mw)
    if worker:
        cl_where.append("worker = %s")
        cl_params.append(worker)
    for r in _ie(f"SELECT id, extract(epoch FROM received_at), worker, model_name, error, request_id "
                 f"FROM call_log WHERE {' AND '.join(cl_where)} ORDER BY id DESC LIMIT %s",
                 tuple(cl_params + [limit])):
        rows.append({"id": int(r[0]), "at": float(r[1]) if r[1] is not None else None,
                     "ts": float(r[1]) if r[1] is not None else None, "worker": r[2], "action": "load",
                     "outcome": "fail", "model": r[3], "model_name": r[3],
                     "error": r[4], "reason": r[4], "detail": {"message": r[4]} if r[4] else {},
                     "request_id": r[5], "source": "call_log"})
    rows.sort(key=lambda x: x.get("ts") or 0, reverse=True)
    return rows[:limit]


def compute_actions_log(limit=200, model=None, worker=None):
    """A model's load failures, newest first, bounded. Member-readable; never 500
    (empty list + error on a store fault)."""
    try:
        limit = max(1, min(5000, int(limit or 200)))
    except (TypeError, ValueError):
        limit = 200
    model = str(model or "").strip()
    worker = str(worker or "").strip()
    try:
        rows = compute_actions(limit, model, worker)
        return {"actions": rows, "count": len(rows)}
    except Exception as exc:  # noqa: BLE001 — a read surface must not 500
        logger.warning("GET /llm/compute-actions failed: %s", exc, exc_info=True)
        return {"actions": [], "count": 0, "error": str(exc)}


# ── review DISCOVERY pipeline (DROPPED: forces downloads/placement) ───────────
_REVIEW_WHY = ("the model-discovery review pipeline (Hugging Face search, weight "
               "download, smoke-load) is not part of hugpy_core: core never forces a "
               "download or placement. Use the Fleet capacity test to grade models "
               "that online workers already serve.")


def review_status():
    """No API-started discovery runs exist in core; the criteria list is empty."""
    return {"criteria": [], "note": _REVIEW_WHY}


def review_criteria_list():
    return []


def review_criteria_get(name=None):
    return {"name": name, "error": _REVIEW_WHY}, 404


def review_criteria_put(name=None, **_body):
    return {"name": name, "error": _REVIEW_WHY}, 501


def review_screen(**_body):
    return {"error": _REVIEW_WHY}, 501


def review_run(**_body):
    return {"status": "error", "error": _REVIEW_WHY}, 501


def review_runs():
    return []


def review_results():
    return []


def review_dossiers(criteria=None):
    if not criteria:
        return {"error": "criteria is required"}, 400
    return {"criteria": criteria, "dossiers": [], "note": _REVIEW_WHY}


def review_dossier(criteria=None, hub_id=None):
    if not criteria or not hub_id:
        return {"error": "criteria and hub_id are required"}, 400
    return {"error": f"no dossier for {hub_id} under criteria {criteria!r}: {_REVIEW_WHY}"}, 404


def review_radar(criteria=None):
    if not criteria:
        return {"error": "criteria is required"}, 400
    return {"criteria": criteria, "hits": [], "detail": _REVIEW_WHY}


def review_ingest(**_body):
    return {"error": _REVIEW_WHY}, 501


__all__ = ["suite_registry", "compute_actions", "benchmark_runs", "benchmark_run_get", "benchmark_status",
           "benchmark_events", "benchmark_run", "benchmark_judge", "benchmark_cancel", "benchmark_suites",
           "compute_actions_log", "review_status", "review_criteria_list", "review_criteria_get",
           "review_criteria_put", "review_screen", "review_run", "review_runs", "review_results",
           "review_dossiers", "review_dossier", "review_radar", "review_ingest"]
