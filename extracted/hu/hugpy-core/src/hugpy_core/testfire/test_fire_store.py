# LIFTED from legacy hugpy (read-only reference):
#   py/services/hugpy_server/src/hugpy_server/app/test_fire_store.py
#   — thresholds, resume_plan, _median, verdict_for, analyze: VERBATIM.
# SWAPPED: storage. test_fire_results is gone — a run's per-call results ARE its
#   call-log rows (hugpy_wrapper.call_log_derived, task 'test-fire:<job_id>'),
#   read at request time. Run options travel in each call request; no run table.
"""Test-fire HISTORY: a worker's past test fires, viewable after central restarts.

Fail-open everywhere: no DB / a DB error means the run still happens, it just
is not listed."""
from __future__ import annotations

import json
import logging
import statistics
from typing import Optional

log = logging.getLogger(__name__)

# verdict thresholds (analyze)
HEALTHY_RATE = 0.95          # success rate at/above which a model is healthy
FAILING_STREAK = 3           # this many latest calls all failed -> failing
REGRESS_TOK_S = 0.70         # latest run's median tok/s below 70% of baseline -> regressed
REGRESS_LATENCY = 1.50       # ... or median latency above 150% of baseline
MIN_BASELINE = 3             # ok calls needed before a baseline is drawn

def _ie(sql: str, params: tuple = ()) -> list:
    # the wrapper call log is read only through calllog.py (the one reader)
    from hugpy_core.calllog.calllog import query
    return query(sql, params)


def _worker_name(worker_id: str) -> Optional[str]:
    from hugpy_core.registry import registry
    w = registry.lookup_worker(worker_id)
    return (w or {}).get("name")


# ── writes (called by the job) ───────────────────────────────────────────────
def save_run(job) -> bool:
    """Compatibility hook: run history is derived from the calls themselves."""
    return True


def save_result(job, result: dict) -> bool:
    """The call log is the sole execution record."""
    return True


# New rows carry the run ID in metadata; the task prefix is read only for old rows.
_JOB = "coalesce(request_body->'metadata'->'test_fire'->>'job_id', CASE WHEN task LIKE 'test-fire:%%' THEN substr(task, 11) END)"
# Each attempt contributes its execution row, or its last failed relay if no
# execution was reached. Never count the core/worker/wrapper chain three times.
_LEAF = "NOT EXISTS (SELECT 1 FROM call_log child WHERE child.request_params->>'parent_request_id' = call_log_derived.request_id AND child.request_body->'metadata'->'test_fire' IS NOT NULL)"

# ── reads ────────────────────────────────────────────────────────────────────
def _results(job_ids: list) -> list:
    """The runs' calls from the call log, oldest first, in the legacy result shape."""
    if not job_ids:
        return []
    from hugpy_core.testfire.testfire import classify_error
    rows = _ie(f"SELECT {_JOB}, request_id, model_name, worker, extract(epoch FROM received_at),"
               " http_status, error, total_s, completion_tokens, tok_per_s,"
               " coalesce(request_body->'messages'->-1->>'content', request_body->>'prompt'),"
               " left(response_body->'choices'->0->'message'->>'content', 80)"
               f" FROM call_log_derived WHERE {_JOB} = ANY(%s) AND {_LEAF} ORDER BY received_at",
               (job_ids,))
    grades = {}
    request_ids = [row[1] for row in rows if row[1]]
    if request_ids:
        try:
            from hugpy_core.grading import grader
            with grader._db() as conn:
                grades = {rid: {"passed": passed, "category": category, "tier": tier,
                                "why": why}
                          for rid, passed, category, tier, why in conn.execute(
                              "SELECT request_id, passed, category, tier, why FROM grades "
                              "WHERE request_id = ANY(%s)", (request_ids,))}
        except Exception:  # noqa: BLE001 — history still works when grades are unavailable
            log.exception("test-fire history: grade lookup failed")
    f = lambda v: float(v) if v is not None else None
    out = []
    for job, rid, model, worker, at, status, err, total, toks, tps, prompt, content in rows:
        ok = status == 200 and not err
        error = None if ok else (err or f"HTTP {status}")
        out.append({"job_id": job, "request_id": rid, "model_key": model, "started": f(at), "ok": ok,
                    "latency_s": f(total), "tokens": toks, "tok_s": f(tps), "error": error,
                    "error_kind": classify_error(error) if error else None, "served_by": worker,
                    "content80": content, "prompt": prompt, "grade": grades.get(rid)})
    return out


def _derived_runs(worker_name: Optional[str], job_ids: Optional[list] = None, limit: int = 50) -> dict:
    """Group call-log rows; the submitted run options ride the calls' metadata."""
    where, params = [f"{_JOB} IS NOT NULL", _LEAF], []
    if job_ids is not None:
        where.append(f"{_JOB} = ANY(%s)")
        params.append(job_ids)
    if worker_name:
        where.append("worker = %s")
        params.append(worker_name)
    rows = _ie(f"SELECT {_JOB}, min(worker), extract(epoch FROM min(received_at)),"
               f" extract(epoch FROM max(coalesce(responded_at, received_at))),"
               f" array_agg(DISTINCT model_name), count(*) FILTER (WHERE http_status = 200 AND error IS NULL),"
               f" count(*) FILTER (WHERE NOT (http_status = 200 AND error IS NULL) OR http_status IS NULL),"
               f" (array_agg(request_body->'metadata'->'test_fire' ORDER BY received_at DESC))[1]"
               f" FROM call_log_derived WHERE {' AND '.join(where)}"
               f" GROUP BY {_JOB} ORDER BY min(received_at) DESC LIMIT %s", tuple(params + [int(limit)]))
    out = {}
    for row in rows:
        opts = row[7] if isinstance(row[7], dict) else {}
        total = int(row[5]) + int(row[6])
        models = opts.get("models") or sorted(m for m in row[4] or [] if m)
        grade = bool(opts.get("grade"))
        complete = False
        if grade:
            from hugpy_core.grading import grader
            from hugpy_core.testfire import testfire
            catalog = testfire._catalog()
            complete = all(
                (suites := grader.suites_for_tasks(testfire.model_tasks(testfire._catalog_row(catalog, key) or {})))
                and all(not grader.pending_items(key, suite) for suite in suites) for key in models)
        elif opts.get("rounds"):
            complete = total >= int(opts["rounds"]) * len(models)
        out[row[0]] = {**opts, "job_id": row[0], "worker_name": row[1], "source": "call_log",
                       "created": float(row[2]), "started": float(row[2]),
                       "finished": float(row[3]) if complete else None,
                       "models": models, "ok": int(row[5]), "failed": int(row[6]),
                       "stop_reason": "complete" if complete else "incomplete",
                       "grade": grade}
    return out


def list_runs(worker_id: str, limit: int = 50) -> list:
    name = _worker_name(worker_id)
    if not name:
        return []
    return [dict(row, worker_id=worker_id) for row in _derived_runs(name, limit=limit).values()]


def get_run(job_id: str) -> Optional[dict]:
    run = _derived_runs(None, job_ids=[job_id]).get(job_id)
    if run is None:
        return None
    if not run.get("worker_id"):
        from hugpy_core.registry import registry
        run["worker_id"] = (registry.lookup_worker(run.get("worker_name") or "") or {}).get("id")
    return dict(run, results=_results([job_id]))


def resume_plan(run: dict, results: list) -> Optional[dict]:
    """PURE: how to pick an unfinished run back up (operator 2026-10-02: "a
    resume option that starts with the last model that was run if incomplete —
    start that model's run over and proceed"). Returns ``{first_order,
    rounds}`` — the rest of the interrupted round, the in-flight model first,
    then the rounds still owed (0 = until stopped) — or None when nothing is
    left. Assumes the round-robin order run_job uses (every model once per round)."""
    models = list(run.get("models") or [])
    if not models:
        return None
    if run.get("grade"):
        current = run.get("current_model")
        order = ([current] if current in models else []) + [m for m in models if m != current]
        return {"first_order": order, "rounds": 1, "interrupted_model": current,
                "completed_rounds": 0}
    n = len(models)
    done = len(results or [])
    rounds = int(run.get("rounds") or 0)
    full = done // n
    if rounds and full >= rounds:
        return None
    in_round = [r.get("model_key") for r in (results or [])[full * n:]]
    remaining = [m for m in models if m not in in_round]
    cur = run.get("current_model")
    if cur in remaining:
        remaining = [cur] + [m for m in remaining if m != cur]
    if not remaining:
        return None
    return {"first_order": remaining, "rounds": (0 if not rounds else rounds - full),
            "interrupted_model": cur, "completed_rounds": full}


def _pair_results(worker_id: str, limit_runs: int) -> "tuple[list, list]":
    runs = list_runs(worker_id, limit_runs)
    return runs, _results([r["job_id"] for r in runs])


def _median(xs):
    xs = [float(x) for x in xs if x is not None]
    return round(statistics.median(xs), 3) if xs else None


def verdict_for(calls: list, latest_job: Optional[str]) -> dict:
    """PURE: the per-model inference over its stored calls (oldest first).

    baseline = medians over the ok calls BEFORE the latest run (MIN_BASELINE
    needed); latest = medians over the latest run's ok calls. Verdict order:
    untested -> failing (last FAILING_STREAK all failed) -> regressed (latest
    slower than baseline past the thresholds) -> flaky (success < HEALTHY_RATE)
    -> healthy."""
    n = len(calls)
    oks = [c for c in calls if c.get("ok")]
    kinds: dict = {}
    for c in calls:
        if not c.get("ok"):
            k = c.get("error_kind") or "error"
            kinds[k] = kinds.get(k, 0) + 1
    prior_ok = [c for c in oks if c.get("job_id") != latest_job]
    latest_ok = [c for c in oks if c.get("job_id") == latest_job]
    base = None
    if len(prior_ok) >= MIN_BASELINE:
        base = {"latency_s": _median(c.get("latency_s") for c in prior_ok),
                "tok_s": _median(c.get("tok_s") for c in prior_ok), "samples": len(prior_ok)}
    latest = None
    if latest_ok:
        latest = {"latency_s": _median(c.get("latency_s") for c in latest_ok),
                  "tok_s": _median(c.get("tok_s") for c in latest_ok), "samples": len(latest_ok)}
    rate = (len(oks) / n) if n else None
    out = {"calls": n, "ok": len(oks), "failed": n - len(oks),
           "success_rate": (round(rate, 3) if rate is not None else None),
           "error_kinds": kinds, "baseline": base, "latest": latest,
           "last_ok_at": (oks[-1].get("started") if oks else None), "why": None}
    if not n:
        out.update(verdict="untested", why="no stored calls")
        return out
    tail = calls[-FAILING_STREAK:]
    if len(tail) >= min(FAILING_STREAK, n) and all(not c.get("ok") for c in tail):
        out.update(verdict="failing", why=f"last {len(tail)} call(s) failed"
                   + (f" ({max(kinds, key=kinds.get)})" if kinds else ""))
        return out
    if base and latest:
        slow_tok = (base["tok_s"] and latest["tok_s"] is not None
                    and latest["tok_s"] < base["tok_s"] * REGRESS_TOK_S)
        slow_lat = (base["latency_s"] and latest["latency_s"] is not None
                    and latest["latency_s"] > base["latency_s"] * REGRESS_LATENCY)
        if slow_tok or slow_lat:
            parts = []
            if slow_tok:
                parts.append(f"tok/s {latest['tok_s']} vs baseline {base['tok_s']}")
            if slow_lat:
                parts.append(f"latency {latest['latency_s']}s vs baseline {base['latency_s']}s")
            out.update(verdict="regressed", why="; ".join(parts))
            return out
    if rate is not None and rate < HEALTHY_RATE:
        out.update(verdict="flaky", why=f"{round(rate * 100)}% ok over {n} call(s)")
        return out
    out.update(verdict="healthy", why=f"{round((rate or 0) * 100)}% ok over {n} call(s)")
    return out


def analyze(worker_id: str, limit_runs: int = 20) -> dict:
    """Per-model inference over the worker's last ``limit_runs`` stored runs."""
    runs, results = _pair_results(worker_id, limit_runs)
    latest_job = runs[0]["job_id"] if runs else None
    by_model: dict = {}
    for r in results:
        by_model.setdefault(r["model_key"], []).append(r)
    models = {mk: verdict_for(calls, latest_job) for mk, calls in sorted(by_model.items())}
    counts: dict = {}
    for v in models.values():
        counts[v["verdict"]] = counts.get(v["verdict"], 0) + 1
    return {"worker_id": worker_id, "runs": len(runs), "latest_job": latest_job,
            "models": models, "verdicts": counts,
            "thresholds": {"healthy_rate": HEALTHY_RATE, "failing_streak": FAILING_STREAK,
                           "regress_tok_s": REGRESS_TOK_S, "regress_latency": REGRESS_LATENCY,
                           "min_baseline": MIN_BASELINE}}
