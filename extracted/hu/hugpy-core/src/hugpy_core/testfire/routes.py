"""testfire route registration under the abstract_flask ``register_categories``
convention.

The console's test-fire surface on ONE blueprint, ``testfire_bp``, built by
``get_bp``. Every view is a PURE function taking kwargs (never touches
``request``): the former path params ``<worker_id>`` / ``<job_id>`` arrive as
the same-named kwargs, and the JSON-body / query values arrive as their own
kwargs.

Domain logic is UNCHANGED and imported verbatim from ``testfire`` (job registry,
model selection, the firing engine, the history store); only the HTTP shell is
re-expressed here.
"""
from __future__ import annotations


from abstract_flask import get_bp, register_categories, spec

from hugpy_core.testfire import testfire
from hugpy_core.testfire.testfire import (
    DEFAULT_MAX_TOKENS,
    RESULT_RING,
    _JOBS,
    _REG_LOCK,
    _archived_keys,
    _blocked_keys,
    _cancel_request,
    _catalog,
    _get_worker,
    _history,
    _latest_job_for,
    _running_job_for,
    fire_one,
    logger,
    parse_start_body,
    select_text_gen_models,
    start_job,
)

testfire_bp, logger = get_bp("testfire_bp", __name__)


def _clamp(value, default, lo, hi):
    try:
        return max(lo, min(hi, int(value)))
    except (TypeError, ValueError):
        return default


# ── /fleet/workers/test-fire/start  (was POST /fleet/workers/<worker_id>/test-fire) ─
def start(worker_id=None, **body):
    worker = _get_worker(worker_id)
    if not worker:
        return {"ok": False, "error": "unknown worker"}
    try:
        opts = parse_start_body(body)
    except ValueError as exc:
        return {"ok": False, "error": str(exc)}
    running = _running_job_for(worker_id)
    if running is not None:
        return {"ok": False, "error": "test-fire already running on this worker",
                "job_id": running.job_id}
    listing = _catalog()
    selection_worker = {**worker,"models":list(listing),"models_local":[],"storage":{}} if opts["grade"] else worker
    selected, skipped = select_text_gen_models(selection_worker, listing,
                                               blocked=_blocked_keys(),
                                               archived=_archived_keys(), grade=opts["grade"])
    if not selected:
        return {"ok": False,
                "error": ("no models with an installed grading suite on this worker"
                          if opts["grade"] else "no text-generation models on this worker"),
                "skipped": skipped}
    job = start_job(worker_id, worker.get("name") or worker_id, selected,
                    rounds=opts["rounds"], concurrency=opts["concurrency"],
                    max_tokens=opts["max_tokens"], seed=opts["seed"], skipped=skipped,
                    grade=opts["grade"], chaos=opts["chaos"], storage_managed=opts["grade"])
    logger.info("test-fire %s: worker=%s models=%d rounds=%s concurrency=%d chaos=%s max_tokens=%d",
                job.job_id, job.worker_name, len(job.models), job.rounds or "∞",
                job.concurrency, job.chaos, job.max_tokens)
    return {"ok": True, "job_id": job.job_id, "worker_id": worker_id,
            "models": job.models, "skipped": skipped,
            "rounds": job.rounds, "concurrency": job.concurrency,
            "max_tokens": job.max_tokens, "grade": job.grade, "chaos": job.chaos,
            "total_planned": job.total_planned}


# ── /fleet/workers/test-fire/current  (was GET /fleet/workers/<worker_id>/test-fire
#    and .../test-fire/current) ────────────────────────────────────────────────
def current(worker_id=None, **_):
    job = _latest_job_for(worker_id)
    if job is None:
        return {"ok": False, "error": "no test-fire job for this worker"}
    return job.snapshot()


# ── /fleet/workers/test-fire/history  (was GET .../test-fire/history) ───────────
def history(worker_id=None, limit=50, **_):
    """Past runs for this worker, newest first (persisted)."""
    h = _history()
    limit = _clamp(limit, 50, 1, 500)
    runs = h.list_runs(worker_id, limit) if h else []
    live = _running_job_for(worker_id)
    for r in runs:
        r["live"] = bool(live and live.job_id == r["job_id"])
        r["state"] = ("running" if r["live"] else "interrupted" if not r.get("finished")
                      else (r.get("stop_reason") or "complete"))
    return {"worker_id": worker_id, "runs": runs, "stored": h is not None,
            "live_job_id": live.job_id if live else None}


# ── /fleet/workers/test-fire/analysis  (was GET .../test-fire/analysis) ─────────
def analysis(worker_id=None, runs=20, **_):
    """Per-model inference over the stored runs (test_fire_store.analyze)."""
    h = _history()
    if h is None:
        return {"error": "test-fire history disabled"}
    runs = _clamp(runs, 20, 1, 200)
    return h.analyze(worker_id, runs)


# ── /fleet/workers/test-fire/resume  (was POST .../test-fire/history/<job_id>/resume) ─
def resume(worker_id=None, job_id=None, **_):
    """Pick an unfinished stored run back up as a NEW job (resumed_from = the old
    one). Never automatic — the operator asks."""
    h = _history()
    run = h.get_run(job_id) if h else None
    if not run or run.get("worker_id") != worker_id:
        return {"ok": False, "error": f"no stored test-fire run {job_id!r} for this worker"}
    live = _running_job_for(worker_id)
    if live is not None:
        return {"ok": False, "error": "test-fire already running on this worker",
                "job_id": live.job_id}
    if live is None and run.get("finished") and (run.get("stop_reason") or "complete") == "complete":
        return {"ok": False, "error": "that run completed — nothing to resume"}
    plan = h.resume_plan(run, run.get("results") or [])
    if not plan:
        return {"ok": False, "error": "nothing left to run in that test fire"}
    job = start_job(worker_id, run.get("worker_name") or worker_id, list(run.get("models") or []),
                    rounds=plan["rounds"], concurrency=int(run.get("concurrency") or 1),
                    max_tokens=int(run.get("max_tokens") or DEFAULT_MAX_TOKENS),
                    skipped=run.get("skipped") or [], first_order=plan["first_order"],
                    resumed_from=job_id, call_fn=fire_one, grade=bool(run.get("grade", False)),
                    chaos=bool(run.get("chaos", False)), storage_managed=bool(run.get("grade", False)))
    logger.info("test-fire %s: RESUMES %s on %s — first %s, %d model(s) left in the round, rounds=%s",
                job.job_id, job_id, job.worker_name, plan["first_order"][0],
                len(plan["first_order"]), plan["rounds"] or "∞")
    return {"ok": True, "job_id": job.job_id, "resumed_from": job_id, **plan}


# ── /fleet/workers/test-fire/history-run  (was GET .../test-fire/history/<job_id>) ─
def history_run(worker_id=None, job_id=None, **_):
    h = _history()
    run = h.get_run(job_id) if h else None
    if not run or run.get("worker_id") != worker_id:
        return {"error": f"no stored test-fire run {job_id!r} for this worker"}
    return run


# ── /fleet/workers/test-fire/status  (was GET .../test-fire/<job_id>) ───────────
def status(worker_id=None, job_id=None, limit=None, **_):
    with _REG_LOCK:
        job = _JOBS.get(job_id)
    if job is None or job.worker_id != worker_id:
        return {"ok": False, "error": "unknown test-fire job"}
    lim = _clamp(limit if limit is not None else RESULT_RING, RESULT_RING, 1, RESULT_RING)
    return job.snapshot(limit=lim)


# ── /fleet/workers/test-fire/stop  (was POST .../test-fire/<job_id>/stop) ───────
def stop(worker_id=None, job_id=None, **_):
    with _REG_LOCK:
        job = _JOBS.get(job_id)
    if job is None or job.worker_id != worker_id:
        return {"ok": False, "error": "unknown test-fire job"}
    was_running = job.running
    job.request_stop("operator")
    with job._lock:
        in_flight = list(job.in_flight.keys())
    cancelled = [rid for rid in in_flight if _cancel_request(rid, "test-fire stop")]
    return {"ok": True, "job_id": job.job_id, "was_running": was_running,
            "in_flight": len(in_flight), "cancelled": cancelled}


# ── console worker-ID URLs ────────────────────────────────────────────────────
# The shipped console places the worker id (and job id) in the PATH and reads a
# BARE JSON body with a meaningful HTTP status (202 on start, 404/400/409/503 for
# the error cases). These views fold in the method-specific routes that used to
# live on ``testfire.test_fire_bp``, verbatim in logic; path params and the JSON
# body / query reach them as kwargs. Domain calls resolve through ``testfire`` so
# the job registry stays the single source (and is monkeypatchable in one place).
def _native(view, method, endpoint):
    return spec(view, method, response="native", endpoint=endpoint, strict_slashes=True)


def test_fire_start(worker_id=None, **body):
    """POST /fleet/workers/<worker_id>/test-fire: the console's start form (202
    with the job, bare). Body fields arrive as kwargs; JSON booleans keep their type."""
    worker = testfire._get_worker(worker_id)
    if not worker:
        return {"ok": False, "error": "unknown worker"}, 404
    try:
        opts = testfire.parse_start_body(body)
    except ValueError as exc:
        return {"ok": False, "error": str(exc)}, 400
    running = testfire._running_job_for(worker_id)
    if running is not None:
        return {"ok": False, "error": "test-fire already running on this worker",
                "job_id": running.job_id}, 409
    listing = testfire._catalog()
    selection_worker = {**worker,"models":list(listing),"models_local":[],"storage":{}} if opts["grade"] else worker
    selected, skipped = testfire.select_text_gen_models(selection_worker, listing,
                                                        blocked=testfire._blocked_keys(),
                                                        archived=testfire._archived_keys(), grade=opts["grade"])
    if not selected:
        return {"ok": False, "error": "no models with an installed grading suite on this worker" if opts["grade"] else "no text-generation models on this worker",
                "skipped": skipped}, 400
    job = testfire.start_job(worker_id, worker.get("name") or worker_id, selected,
                             rounds=opts["rounds"], concurrency=opts["concurrency"],
                             max_tokens=opts["max_tokens"], seed=opts["seed"], skipped=skipped,
                             grade=opts["grade"], chaos=opts["chaos"], storage_managed=opts["grade"])
    testfire.logger.info("test-fire %s: worker=%s models=%d rounds=%s concurrency=%d chaos=%s max_tokens=%d",
                         job.job_id, job.worker_name, len(job.models), job.rounds or "∞",
                         job.concurrency, getattr(job, "chaos", False), job.max_tokens)
    return {"ok": True, "job_id": job.job_id, "worker_id": worker_id,
            "models": job.models, "skipped": skipped,
            "rounds": job.rounds, "concurrency": job.concurrency,
            "max_tokens": job.max_tokens, "grade": job.grade,
            "chaos": job.chaos,
            "total_planned": job.total_planned}, 202


def test_fire_current(worker_id=None, **_):
    job = testfire._latest_job_for(worker_id)
    if job is None:
        return {"ok": False, "error": "no test-fire job for this worker"}, 404
    return job.snapshot()


def test_fire_history(worker_id=None, limit=50, **_):
    """Past runs for this worker, newest first (persisted). A run with no
    ``finished`` that is not live here was cut off (central restarted)."""
    h = testfire._history()
    limit = _clamp(limit, 50, 1, 500)
    runs = h.list_runs(worker_id, limit) if h else []
    live = testfire._running_job_for(worker_id)
    for r in runs:
        r["live"] = bool(live and live.job_id == r["job_id"])
        r["state"] = ("running" if r["live"] else "interrupted" if not r.get("finished")
                      else (r.get("stop_reason") or "complete"))
    return {"worker_id": worker_id, "runs": runs, "stored": h is not None,
            "live_job_id": live.job_id if live else None}


def test_fire_analysis(worker_id=None, runs=20, **_):
    """Per-model inference over the stored runs (test_fire_store.analyze)."""
    h = testfire._history()
    if h is None:
        return {"error": "test-fire history disabled"}, 503
    runs = _clamp(runs, 20, 1, 200)
    return h.analyze(worker_id, runs)


def test_fire_resume(worker_id=None, job_id=None, **_):
    """Pick an unfinished stored run back up as a NEW job (resumed_from = the
    old one): the interrupted model first, then the rest of its round, then
    the rounds still owed. Never automatic — the operator asks."""
    h = testfire._history()
    run = h.get_run(job_id) if h else None
    if not run or run.get("worker_id") != worker_id:
        return {"ok": False, "error": f"no stored test-fire run {job_id!r} for this worker"}, 404
    live = testfire._running_job_for(worker_id)
    if live is not None:
        return {"ok": False, "error": "test-fire already running on this worker",
                "job_id": live.job_id}, 409
    if live is None and run.get("finished") and (run.get("stop_reason") or "complete") == "complete":
        return {"ok": False, "error": "that run completed — nothing to resume"}, 409
    plan = h.resume_plan(run, run.get("results") or [])
    if not plan:
        return {"ok": False, "error": "nothing left to run in that test fire"}, 409
    job = testfire.start_job(worker_id, run.get("worker_name") or worker_id, list(run.get("models") or []),
                             rounds=plan["rounds"], concurrency=int(run.get("concurrency") or 1),
                             max_tokens=int(run.get("max_tokens") or testfire.DEFAULT_MAX_TOKENS),
                             skipped=run.get("skipped") or [], first_order=plan["first_order"],
                             resumed_from=job_id, call_fn=testfire.fire_one, grade=bool(run.get("grade", False)),
                             chaos=bool(run.get("chaos", False)), storage_managed=bool(run.get("grade", False)))
    testfire.logger.info("test-fire %s: RESUMES %s on %s — first %s, %d model(s) left in the round, rounds=%s",
                         job.job_id, job_id, job.worker_name, plan["first_order"][0],
                         len(plan["first_order"]), plan["rounds"] or "∞")
    return {"ok": True, "job_id": job.job_id, "resumed_from": job_id, **plan}, 202


def test_fire_history_run(worker_id=None, job_id=None, **_):
    h = testfire._history()
    run = h.get_run(job_id) if h else None
    if not run or run.get("worker_id") != worker_id:
        return {"error": f"no stored test-fire run {job_id!r} for this worker"}, 404
    return run


def test_fire_status(worker_id=None, job_id=None, limit=None, **_):
    with testfire._REG_LOCK:
        job = testfire._JOBS.get(job_id)
    if job is None or job.worker_id != worker_id:
        return {"ok": False, "error": "unknown test-fire job"}, 404
    lim = _clamp(limit if limit is not None else testfire.RESULT_RING, testfire.RESULT_RING, 1, testfire.RESULT_RING)
    return job.snapshot(limit=lim)


def test_fire_stop(worker_id=None, job_id=None, **_):
    with testfire._REG_LOCK:
        job = testfire._JOBS.get(job_id)
    if job is None or job.worker_id != worker_id:
        return {"ok": False, "error": "unknown test-fire job"}, 404
    was_running = job.running
    job.request_stop("operator")
    with job._lock:
        in_flight = list(job.in_flight.keys())
    cancelled = [rid for rid in in_flight if testfire._cancel_request(rid, "test-fire stop")]
    return {"ok": True, "job_id": job.job_id, "was_running": was_running,
            "in_flight": len(in_flight), "cancelled": cancelled}


ALL_CATEGORIES = {
    "fleet": {
        "workers": {
            "test-fire": {
                "start":       start,        # -> /fleet/workers/test-fire/start       (worker_id kwarg)  [was POST /fleet/workers/<worker_id>/test-fire]
                "current":     current,      # -> /fleet/workers/test-fire/current     (worker_id kwarg)  [was GET /test-fire and /test-fire/current]
                "history":     history,      # -> /fleet/workers/test-fire/history     (worker_id kwarg)
                "analysis":    analysis,     # -> /fleet/workers/test-fire/analysis    (worker_id kwarg)
                "resume":      resume,       # -> /fleet/workers/test-fire/resume      (worker_id+job_id kwargs)  [was POST .../history/<job_id>/resume]
                "history-run": history_run,  # -> /fleet/workers/test-fire/history-run (worker_id+job_id kwargs)  [was GET .../history/<job_id>]
                "status":      status,       # -> /fleet/workers/test-fire/status      (worker_id+job_id kwargs)  [was GET .../<job_id>]
                "stop":        stop,         # -> /fleet/workers/test-fire/stop        (worker_id+job_id kwargs)  [was POST .../<job_id>/stop]
            },
            # ── console path forms (worker/job id in the URL; bare body + status) ──
            "<worker_id>": {
                "test-fire": {
                    # GET /fleet/workers/<worker_id>/test-fire + .../current, POST = start
                    "": [
                        spec(test_fire_current, "GET", response="native", endpoint="test_fire_current",
                             strict_slashes=True,
                             rules=["/fleet/workers/<worker_id>/test-fire",
                                    "/fleet/workers/<worker_id>/test-fire/current"]),
                        spec(test_fire_start, "POST", response="native",
                             endpoint="test_fire_start", strict_slashes=True),
                    ],
                    "analysis": _native(test_fire_analysis, "GET", "test_fire_analysis"),
                    "history": {
                        "": _native(test_fire_history, "GET", "test_fire_history"),
                        "<job_id>": {
                            "": _native(test_fire_history_run, "GET", "test_fire_history_run"),
                            "resume": _native(test_fire_resume, "POST", "test_fire_resume"),
                        },
                    },
                    "<job_id>": {
                        "": _native(test_fire_status, "GET", "test_fire_status"),
                        "stop": _native(test_fire_stop, "POST", "test_fire_stop"),
                    },
                },
            },
        },
    },
}

register_categories(testfire_bp, ALL_CATEGORIES)
