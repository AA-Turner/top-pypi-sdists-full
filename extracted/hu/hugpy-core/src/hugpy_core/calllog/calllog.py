"""THE one reader of the wrapper call log (operator 2026-10-06, derivation-map-2026-10-06).

Doctrine: "every metric anywhere in hugpy is a pointer into hugpy_wrapper.call_log
resolved through ONE derived layer; core computes nothing itself." The derived
layer is owned by the hugpy_wrapper package (sql/009_call_chain.sql):

  * VIEW ``call_log_derived`` — raw call_log + per-row metrics (queue_s/load_s/…)
    + the CHAIN-RESOLVED execution block (parent_request_id, intent, test_fire_job,
    exec_request_id/is_exec, exec_worker/exec_quantization/exec_*, cold_load_s =
    the chain's central pull, plan_evict_s, hot_load_s, ttft_s, exec_tok_per_s,
    pull_*). A pointer to ANY hop yields that execution's full staged timing.
  * VIEW ``call_chain`` — the family of a request (root/parent/exec/hop).

This module is the ONLY place in hugpy_core that SELECTs from the wrapper. core
computes nothing itself: the SQL does the aggregation (a full scan of
call_log_derived is ~100 ms — keep queries bounded/indexed, and NEVER a per-row
recursive function inside a lateral, which stalled the console ~8 min, REVERT
Step 5). Python here only shapes JSON. grader.py, console_routes.py,
test_fire_store.py, benchmark_log.py, review.py, modeldb (activate outcome) and
envprofiles all read through this module — no second connection anywhere.

Shared mirrored call-log columns (names kept from hugpy_wrapper; the box measures
them and intake mirrors them into core's copy — documented here, the one reader,
so a consumer never guesses the meaning):

  box_id                     the source box's record id — every box numbers its
                             own rows from 1, so the mirror keys a row by
                             (worker, box_id) and keeps its own id sequence
  measured_vram_after_load   engine GPU allocation at the ready/reuse boundary
  process_bytes_after_call   engine GPU memory after the call
  non_expert_bytes           estimated GPU weight bytes incl. GPU-resident experts
  tok_bytes_gpu              weight bytes read per generated token, from GPU
  tok_bytes_ram              weight bytes read per generated token, from RAM
  free_vram_before           budgetable GPU headroom before the call
  free_vram_after            budgetable GPU headroom after the call
"""
from __future__ import annotations

from typing import Iterable, Optional

from hugpy_core.calllog.calllog_db import store as _store


# ── the single reader primitive ──────────────────────────────────────────────
def query(sql: str, params: tuple = ()) -> list:
    """Run one SELECT against the wrapper DB (hugpy_wrapper). The ONLY connection
    to the call log in core; every other module calls through here. Routed via
    abstract_database's bootstrap-free PgStateStore (verbatim ``%s``, tuples)."""
    return _store().sql(sql, params)


# ── pointer reads (request_id list / intent / test-fire job / chain) ──────────
def by_request_ids(ids: Iterable[str], columns: "list | None" = None) -> dict:
    """{request_id: row} from call_log_derived for the given ids. ``columns`` is
    a list of call_log_derived column names (row = {col: val}); None hands back
    the WHOLE derived row as a jsonb dict (PostgreSQL keeps exact numerics and
    nested JSON). A grade/benchmark pointer at ANY hop still resolves the
    execution's exec_* block this way."""
    ids = [i for i in (ids or []) if i]
    if not ids:
        return {}
    if columns is None:
        rows = query("SELECT request_id, to_jsonb(c) FROM call_log_derived c "
                     "WHERE request_id = ANY(%s)", (ids,))
        return {r[0]: r[1] for r in rows}
    cols = ", ".join(columns)
    rows = query(f"SELECT request_id, {cols} FROM call_log_derived "
                 "WHERE request_id = ANY(%s)", (ids,))
    return {r[0]: dict(zip(columns, r[1:])) for r in rows}


def by_intent(intent: str, since: "float | None" = None, limit: int = 500,
              columns: "list | None" = None) -> list:
    """call_log_derived rows whose own metadata.intent is ``intent`` (intent is a
    derived column — request_body.metadata.intent, back-read for pre-intent rows
    by intent.py), newest first, bounded. ``columns`` None = whole jsonb row."""
    where, params = ["intent = %s"], [intent]
    if since is not None:
        where.append("received_at > to_timestamp(%s)")
        params.append(since)
    clause = " AND ".join(where)
    if columns is None:
        rows = query(f"SELECT to_jsonb(c) FROM call_log_derived c WHERE {clause} "
                     "ORDER BY id DESC LIMIT %s", tuple(params + [limit]))
        return [r[0] for r in rows]
    cols = ", ".join(columns)
    rows = query(f"SELECT {cols} FROM call_log_derived WHERE {clause} "
                 "ORDER BY id DESC LIMIT %s", tuple(params + [limit]))
    return [dict(zip(columns, r)) for r in rows]


def by_test_fire_job(job_ids: Iterable[str], columns: "list | None" = None) -> list:
    """call_log_derived rows belonging to the given test-fire run(s) — the job id
    is the derived column test_fire_job (request_body.metadata.test_fire.job_id),
    oldest first. ``columns`` None = whole jsonb row."""
    job_ids = [j for j in (job_ids or []) if j]
    if not job_ids:
        return []
    if columns is None:
        rows = query("SELECT to_jsonb(c) FROM call_log_derived c "
                     "WHERE test_fire_job = ANY(%s) ORDER BY received_at", (job_ids,))
        return [r[0] for r in rows]
    cols = ", ".join(columns)
    rows = query(f"SELECT {cols} FROM call_log_derived WHERE test_fire_job = ANY(%s) "
                 "ORDER BY received_at", (job_ids,))
    return [dict(zip(columns, r)) for r in rows]


_CHAIN_COLS = ("request_id", "parent_request_id", "root_request_id", "exec_request_id",
               "hop", "task", "caller", "callee", "received_at", "responded_at", "http_status")


def chain(request_id: str) -> list:
    """The family of a request: every hop sharing its root (call_chain over the
    wrapper's call_root_id/call_exec_id), oldest first."""
    if not request_id:
        return []
    rows = query("SELECT request_id, parent_request_id, root_request_id, exec_request_id, "
                 "hop, task, caller, callee, extract(epoch FROM received_at), "
                 "extract(epoch FROM responded_at), http_status FROM call_chain "
                 "WHERE root_request_id = call_root_id(%s) ORDER BY received_at",
                 (request_id,))
    f = lambda v: float(v) if v is not None else None
    out = []
    for r in rows:
        d = dict(zip(_CHAIN_COLS, r))
        d["received_at"], d["responded_at"] = f(d["received_at"]), f(d["responded_at"])
        out.append(d)
    return out


def grading_executions(since_s: float, settle_s: float) -> list:
    """[(exec request_id, central request_id)] — the EXECUTION rows (hop
    'wrapper') of answered grading calls (the wrapper's stored ``intent``
    column, sql/014) that responded between ``since_s`` and ``settle_s`` seconds
    ago, oldest first. Pointers only: grader.fill_from_call_log looks up which
    have no grade before it reads any body."""
    return [(r[0], r[1]) for r in query(
        "SELECT request_id, request_body->'metadata'->>'central_request_id' FROM call_log "
        "WHERE intent = 'grading' AND request_params->>'hop' = 'wrapper' AND http_status = 200 "
        "AND responded_at > now() - make_interval(secs => %s) "
        "AND responded_at < now() - make_interval(secs => %s) ORDER BY id",
        (float(since_s), float(settle_s)))]


def grading_calls(ids: Iterable[str]) -> list:
    """What a grade is checked from, for the given execution rows: the model
    asked, the call's own metadata, the prompt (last message) and the reply."""
    ids = [i for i in (ids or []) if i]
    if not ids:
        return []
    cols = ("request_id", "model", "metadata", "prompt", "response_body", "responded_at")
    rows = query("SELECT request_id, coalesce(request_body->>'model', model_name), "
                 "request_body->'metadata', request_body->'messages'->-1->>'content', "
                 "response_body, extract(epoch FROM responded_at) "
                 "FROM call_log WHERE request_id = ANY(%s) ORDER BY id", (ids,))
    return [dict(zip(cols, r)) for r in rows]


def central_pulls(model_name: str, worker: str) -> "dict | None":
    """The latest central-pull hop for a (model, worker) — the drive-fetch call
    the box opens on /llm/central/pulls (task 'central-pull'). This is the
    AUTHORITATIVE activate OUTCOME (derivation-map AUDIT 5: not a local status):
    done when the pull responded 200, error with the real pull_error otherwise,
    in-flight while it has no responded_at. None when the box never pulled."""
    if not model_name or not worker:
        return None
    rows = query("SELECT request_id, http_status, error, call_state, "
                 "extract(epoch FROM received_at), extract(epoch FROM responded_at) "
                 "FROM call_log WHERE task = 'central-pull' AND model_name = %s AND worker = %s "
                 "ORDER BY received_at DESC LIMIT 1", (model_name, worker))
    if not rows:
        return None
    rid, status, error, call_state, received, responded = rows[0]
    state = ("pulling" if responded is None else
             "done" if status == 200 and not error else "error")
    return {"request_id": rid, "state": state, "error": error,
            "http_status": status, "call_state": call_state,
            "at": float(received) if received is not None else None,
            "finished_at": float(responded) if responded is not None else None}


# ── env-profile "▶ test": a call with metadata.intent 'env-test' ──────────────
# (derivation-map AUDIT 6: the env test IS a call, not a side table) — the core
# call row carries env_profile + worker_id in its metadata; the result is read
# back from the log, latest per (profile, worker).
def env_tests() -> dict:
    """{(profile_name, worker_id): {ok, model, task, route, status, error, at}} —
    the latest env-test call per (profile, box) from the call log."""
    rows = query(
        "SELECT DISTINCT ON (request_body->'metadata'->>'env_profile',"
        " request_body->'metadata'->>'worker_id')"
        " request_body->'metadata'->>'env_profile', request_body->'metadata'->>'worker_id',"
        " model_name, task, endpoint, http_status, error, extract(epoch FROM received_at)"
        " FROM call_log_derived WHERE intent = 'env-test'"
        " ORDER BY 1, 2, id DESC")
    out = {}
    for name, wid, model, task, route, status, error, at in rows:
        if not name or not wid:
            continue
        ok = status is not None and 200 <= status < 300 and not error
        out[(name, wid)] = {"ok": ok, "model": model, "task": task, "route": route,
                            "status": status, "error": None if ok else error,
                            "at": float(at) if at is not None else None}
    return out


# ── rollups (SQL does the aggregation; callers only shape JSON) ───────────────
# every execution row that was NOT a sizing fill. One block PER MODEL THAT HAS
# ANY such row — never null, never "no calls recorded" (that phrase is only for a
# model with zero rows, which simply never appears here). A rated row = tokens +
# a generation window (the tok/s denominator); a model whose task emits images /
# audio / video / embeddings has n_rated 0 by nature — then tok/s is n/a and the
# honest figure is the per-call wall time (operator 2026-10-06 acceptance).
# a sizing fill is not a call to rate: the G8 context probes (old rows: task
# 'g8-…'; newer rows: task text-generation, request_id 'g8-…', intent
# 'context-probe' — a full-ctx prefill asking 1 token, ~228 s each) were landing
# in the Grader's tok/s as an unstamped "runtime default" row
_RECORDED = ("is_exec AND coalesce(task, '') NOT LIKE 'g8-%%' AND coalesce(request_id, '') NOT LIKE 'g8-%%'"
             " AND coalesce(intent, '') <> 'context-probe' AND model_name IS NOT NULL")
_RATED = "completion_tokens > 0 AND tok_per_s > 0"
# Σ tokens / Σ seconds where each call's seconds are its own tok_per_s denominator
# (call-record contract: tokens_out / (response − call − cold − hot)).
_MEAN = (f"sum(completion_tokens) FILTER (WHERE {_RATED}) "
         f"/ nullif(sum(completion_tokens / tok_per_s) FILTER (WHERE {_RATED}), 0)")

# output kind + unit by model task (what "a call" produces) — governs whether
# tok/s even applies; the server names it so the UI never guesses.
_OUTPUT = {
    "text-generation": ("text", "tokens"), "text2text-generation": ("text", "tokens"),
    "image-text-to-text": ("text", "tokens"), "visual-question-answering": ("text", "tokens"),
    "image-to-text": ("text", "tokens"), "summarization": ("text", "tokens"),
    "keyword-extraction": ("text", "tokens"),
    "text-to-image": ("image", "images"), "image-to-image": ("image", "images"),
    "text-to-video": ("video", "clips"), "image-to-video": ("video", "clips"),
    "automatic-speech-recognition": ("audio", "transcripts"), "text-to-speech": ("audio", "clips"),
    "feature-extraction": ("embedding", "vectors"), "sentence-similarity": ("embedding", "vectors"),
    "embedding": ("embedding", "vectors"), "rerank": ("embedding", "vectors"),
}


def _throughput_reason(b: dict) -> str:
    """Human text for the model's throughput cell, from its own counts — never
    the false "no calls recorded" while rows exist."""
    fail = ""
    if b["n_failed"]:
        fail = f" · {b['n_failed']} failed"
        if b["last_http"]:
            fail += f" (last HTTP {b['last_http']}: {b['last_error']})"
    if b["n_rated"]:
        return f"{b['n_ok']} call(s) ok · {b['mean_tok_s']:.1f} tok/s over {b['n_rated']} rated{fail}"
    if b["n_ok"]:
        per = f" · mean {b['mean_s_per_call']:.1f} s/call" if b["mean_s_per_call"] is not None else ""
        return f"{b['n_ok']} call(s) ok · {b['output_kind']} output — tok/s n/a{per}{fail}"
    return f"{b['n_calls']} call(s){fail or ' · all failed'}"


def throughput_by_model() -> dict:
    """{model_name: block} for EVERY model with a recorded execution row. Block:
    n_calls / n_ok / n_failed / n_rated (rows with tokens + a window), mean_tok_s
    (null when nothing was rated), p50/p90/min/max (over rated rows),
    mean_s_per_call (wall time, the honest figure for image/audio/video/embedding),
    last_http / last_error / last_request_id, task + output_kind + output_unit,
    a human ``reason``, first_at/last_at, and per worker x quant x alloc cells.
    tok/s = Σ tokens / Σ generation seconds (load never folded in)."""
    out: dict = {}
    for r in query(f"""SELECT model_name, count(*),
                        count(*) FILTER (WHERE http_status = 200),
                        count(*) FILTER (WHERE http_status IS NOT NULL AND http_status <> 200),
                        count(*) FILTER (WHERE {_RATED}),
                        {_MEAN},
                        percentile_cont(0.5) WITHIN GROUP (ORDER BY tok_per_s),
                        percentile_cont(0.9) WITHIN GROUP (ORDER BY tok_per_s),
                        min(tok_per_s) FILTER (WHERE {_RATED}), max(tok_per_s) FILTER (WHERE {_RATED}),
                        avg(total_s) FILTER (WHERE http_status = 200 AND total_s > 0),
                        (array_agg(http_status ORDER BY received_at DESC) FILTER (WHERE http_status IS NOT NULL AND http_status <> 200))[1],
                        (array_agg(left(error, 160) ORDER BY received_at DESC) FILTER (WHERE http_status IS NOT NULL AND http_status <> 200))[1],
                        (array_agg(request_id ORDER BY received_at DESC))[1],
                        mode() WITHIN GROUP (ORDER BY task),
                        extract(epoch FROM min(received_at)), extract(epoch FROM max(received_at)),
                      (array_agg(request_id ORDER BY received_at DESC, id DESC) FILTER (WHERE cold_load_s > 0))[1],
                      (array_agg(request_id ORDER BY received_at DESC, id DESC) FILTER (WHERE hot_load_s > 0))[1],
                      extract(epoch FROM max(received_at) FILTER (WHERE cold_load_s > 0)),
                      extract(epoch FROM max(received_at) FILTER (WHERE hot_load_s > 0))
                   FROM call_log_derived WHERE {_RECORDED} GROUP BY model_name"""):
        f = lambda v: float(v) if v is not None else None
        kind, unit = _OUTPUT.get(r[14] or "", ("text", "tokens"))
        b = {"n_calls": int(r[1]), "n_ok": int(r[2]), "n_failed": int(r[3]), "n_rated": int(r[4]),
             "mean_tok_s": f(r[5]), "p50": f(r[6]), "p90": f(r[7]), "min": f(r[8]), "max": f(r[9]),
             "mean_s_per_call": f(r[10]), "last_http": r[11], "last_error": r[12], "last_request_id": r[13],
             "task": r[14], "output_kind": kind, "output_unit": unit,
             "first_at": f(r[15]), "last_at": f(r[16]), "cells": []}
        b["reason"] = _throughput_reason(b)
        out[r[0]] = b
    for r in query(f"""SELECT model_name, worker, quantization, alloc_mode,
                        count(*), count(*) FILTER (WHERE {_RATED}), {_MEAN},
                        avg(total_s) FILTER (WHERE http_status = 200 AND total_s > 0),
                        count(*) FILTER (WHERE http_status IS NOT NULL AND http_status <> 200),
                        (array_agg(left(error, 160) ORDER BY received_at DESC)
                           FILTER (WHERE http_status IS NOT NULL AND http_status <> 200))[1]
                   FROM call_log_derived WHERE {_RECORDED}
                   GROUP BY 1, 2, 3, 4 ORDER BY 1, 5 DESC"""):
        blk = out.get(r[0])
        if blk is not None:
            blk["cells"].append({"worker": r[1], "quant": r[2], "alloc_mode": r[3],
                                 "n_calls": int(r[4]), "n_rated": int(r[5]),
                                 "mean_tok_s": float(r[6]) if r[6] is not None else None,
                                 "mean_s_per_call": float(r[7]) if r[7] is not None else None,
                                 "n_failed": int(r[8] or 0), "last_error": r[9]})
    return out


_METRICS_COLS = ("model_name", "quant", "alloc_mode", "worker", "cold_load_s", "hot_load_s",
                 "tok_per_s", "tok_per_s_avg", "n_samples", "task", "updated_at")


def metrics_by_model(limit: int = 500, model: str = "") -> list:
    """One row per model x quant x alloc_mode x worker from call_log_derived
    EXECUTION rows (sql/009): cold_load_s = the chain's central pull (0 when the
    weights were on the drive), hot_load_s = engine load (0 when already
    resident); latest positive measurement per stage, with its source request
    pointer and time. A resident reuse never erases the last measured load."""
    where, params = [_RECORDED], []          # execution rows, sizing fills excluded (same rule as tok/s)
    if model:
        tail = model.split("~")[-1]
        where.append("(model_name = ANY(%s) OR model_name LIKE %s)")
        params += [list(dict.fromkeys([model, tail])), "%~" + tail]
    rows = query(f"""SELECT model_name, quantization, alloc_mode, worker,
                      (array_agg(cold_load_s ORDER BY received_at DESC, id DESC) FILTER (WHERE cold_load_s > 0))[1],
                      (array_agg(hot_load_s ORDER BY received_at DESC, id DESC) FILTER (WHERE hot_load_s > 0))[1],
                      sum(completion_tokens) FILTER (WHERE tok_per_s > 0) / nullif(sum(completion_tokens / tok_per_s) FILTER (WHERE tok_per_s > 0 AND completion_tokens > 0), 0),
                      avg(tok_per_s), count(*), mode() WITHIN GROUP (ORDER BY task),
                      extract(epoch FROM max(received_at)),
                      (array_agg(request_id ORDER BY received_at DESC, id DESC) FILTER (WHERE cold_load_s > 0))[1],
                      (array_agg(request_id ORDER BY received_at DESC, id DESC) FILTER (WHERE hot_load_s > 0))[1],
                      extract(epoch FROM max(received_at) FILTER (WHERE cold_load_s > 0)),
                      extract(epoch FROM max(received_at) FILTER (WHERE hot_load_s > 0))
                   FROM call_log_derived WHERE {' AND '.join(where)}
                   GROUP BY 1, 2, 3, 4 ORDER BY max(received_at) DESC LIMIT %s""", tuple(params + [limit]))
    f = lambda v: float(v) if v is not None else None
    out = []
    for r in rows:
        out.append({"model_name": r[0], "quant": r[1], "alloc_mode": r[2], "worker": r[3],
                    "cold_load_s": f(r[4]), "hot_load_s": f(r[5]), "tok_per_s": f(r[6]),
                    "tok_per_s_avg": f(r[7]), "n_samples": int(r[8]), "task": r[9],
                    "updated_at": f(r[10]), "cold_request_id": r[11], "hot_request_id": r[12],
                    "cold_measured_at": f(r[13]), "hot_measured_at": f(r[14])})
    return out


def placements_by_worker(worker_name: str) -> dict:
    """{model_key: last ACTUAL decided alloc_mode} for this worker — the newest
    successful (http_status = 200) call_log_derived row per model_name
    (call_log_derived.worker is the worker NAME; model_name == the model_key).
    What the model was really placed as last time it served."""
    if not worker_name:
        return {}
    rows = query("SELECT DISTINCT ON (model_name) model_name, alloc_mode "
                 "FROM call_log_derived WHERE worker = %s AND http_status = 200 "
                 "AND alloc_mode IS NOT NULL ORDER BY model_name, id DESC", (worker_name,))
    return {m: a for m, a in rows}


# ── the console's call list (raw rows; the route shapes them) ─────────────────
CALL_COLS = ("id", "request_id", "model_name", "worker", "task", "caller", "from_ip", "to_ip",
             "endpoint", "http_status", "error", "prompt_tokens", "completion_tokens",
             "received_at", "dispatched_at", "forwarded_at", "inference_started_at",
             "responded_at", "alloc_mode", "context_length", "plan_note", "was_resident",
             "load_s", "total_s", "tok_per_s", "vram_prediction_error")


def calls(limit: int = 300, since: Optional[float] = None, intent: Optional[str] = None) -> list:
    """call_log_derived rows for the console's call list, newest first (CALL_COLS
    + the derived intent column). ``intent`` filters on the call's own
    metadata.intent (intent.py)."""
    from hugpy_core.brain.intent import SQL as INTENT
    where, params = [], []
    if since is not None:
        where.append("received_at > to_timestamp(%s)")
        params.append(since)
    if intent:
        where.append(f"{INTENT} = %s")
        params.append(intent)
    rows = query(f"SELECT {', '.join(CALL_COLS)}, {INTENT} FROM call_log_derived "
                 f"{'WHERE ' + ' AND '.join(where) if where else ''} "
                 "ORDER BY id DESC LIMIT %s", tuple(params + [limit]))
    cols = CALL_COLS + ("intent",)
    return [dict(zip(cols, r)) for r in rows]


def _cell_reason(c: dict) -> str:
    """The throughput text for one cell / worker total, from its own counts."""
    nf = int(c.get("n_failed") or 0)
    fail = (f" · {nf} failed (last: {c['last_error']})" if nf and c.get("last_error")
            else f" · {nf} failed" if nf else "")
    if c.get("n_rated"):
        return f"{c['mean_tok_s']:.1f} tok/s over {c['n_rated']} rated of {c['n_calls']} call(s){fail}"
    if c.get("n_calls") and nf >= c["n_calls"]:
        return f"{c['n_calls']} call(s), all failed — last: {c.get('last_error') or 'no error text'}"
    if c.get("n_calls"):
        per = f" · mean {c['mean_s_per_call']:.1f} s/call" if c.get("mean_s_per_call") is not None else ""
        return f"{c['n_calls']} call(s), none with tokens and a generation window — tok/s n/a{per}{fail}"
    return "no calls recorded"


def worker_totals(model_names) -> list:
    """Per worker, EVERY recorded execution row of the model (any quant / alloc,
    stamped or not): n_calls, n_rated, mean_tok_s = Σ tokens / Σ generation
    seconds, mean s/call — the Grader tab's 'tok/s by worker' (worker_averages)."""
    names = sorted({n for n in (model_names or []) if n})
    if not names:
        return []
    out = []
    for r in query(f"""SELECT worker, count(*), count(*) FILTER (WHERE {_RATED}), {_MEAN},
                        avg(total_s) FILTER (WHERE http_status = 200 AND total_s > 0),
                        count(*) FILTER (WHERE http_status IS NOT NULL AND http_status <> 200),
                        (array_agg(left(error, 160) ORDER BY received_at DESC)
                           FILTER (WHERE http_status IS NOT NULL AND http_status <> 200))[1]
                   FROM call_log_derived WHERE {_RECORDED} AND model_name = ANY(%s)
                   GROUP BY 1 ORDER BY 2 DESC""", (names,)):
        c = {"worker": r[0], "n_calls": int(r[1]), "n_rated": int(r[2]),
             "mean_tok_s": float(r[3]) if r[3] is not None else None,
             "mean_s_per_call": float(r[4]) if r[4] is not None else None,
             "n_failed": int(r[5] or 0), "last_error": r[6]}
        c["reason"] = _cell_reason(c)
        out.append(c)
    return out


def cell_index() -> dict:
    """{(model_name, worker, quant, alloc_mode): throughput block} over every
    recorded call — the Grader matrix's per-row 'tok/s (avg of calls)'."""
    idx = {}
    for name, blk in throughput_by_model().items():
        for c in blk.get("cells") or []:
            cc = {**c, "reason": _cell_reason(c), "task": blk.get("task")}
            idx[(name, c.get("worker"), c.get("quant"), c.get("alloc_mode"))] = cc
    return idx
