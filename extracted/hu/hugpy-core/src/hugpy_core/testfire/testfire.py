# LIFTED from legacy hugpy (read-only reference):
#   py/services/hugpy_server/src/hugpy_server/app/routes/test_fire_routes.py
#   — selection, error classification, TestFireJob, run_job, _guarded_call,
#   _tok_per_s, the job registry, body parsing and every route: VERBATIM.
# REWORKED 2026-11-16 (operator ruling): fire_one is now an ordinary HTTP POST to
#   Core's OWN public /v1/chat/completions (self_base), pinned with the public
#   ``alloc.worker`` steer and tagged with the job; the result is READ BACK from
#   that call-log row. The test fire keeps NO call records, relay/stream path,
#   station lease, or storage cycle of its own.
# SWAPPED: _get_worker (registry), _catalog (routes.catalog_rows: discovery +
#   hugpy.json over the DB rows).
# SWAPPED: persisted history = hugpy_core.test_fire_store (per-call results read
#   from the call log).
# DROPPED: blocked/archived sets are empty.
"""Per-worker TEST FIRE: call a model and assess its call log — nothing else.

Operator ruling (2026-11-16, verbatim): "test fire should literally be calling a
model and assessing its calllog. it should not have any uniqueness to it other
than its sequestering of the worker during the test fire execution".

So a run has exactly ONE special behaviour: while it executes, Core's routing
sequesters its worker (relay.pick) — no OTHER call is placed there; other
traffic routes elsewhere or fails fast naming the test fire. Everything else is
the ordinary public surface:

  * each call is a plain HTTP POST to Core's own ``/v1/chat/completions``
    (``local_base()``, Core's loopback listener) with ``model``, ``messages``,
    ``max_tokens``, ``temperature``, pinned to the worker via the public
    ``alloc.worker`` steer and carrying the job tag (``metadata.test_fire.job_id``)
    so it passes the sequester. Core routes, serves and records it like any
    client's call.
  * assessment reads that call's OWN call-log row back (hugpy_core.calllog):
    status, error, latency, tokens, tok/s and the reply text. Grading
    (grader.check/record) checks the recorded reply and points the grade at the
    call-log row. The test fire computes none of these itself and keeps no side
    record.

The test fire makes NO concurrency decision (operator 2026-11-16: "all testfire
should have to do is make all calls in sequential order and the job should take
care of itself"): it submits EVERY planned call in list order, each on its own
thread, without waiting — the Wrapper's queue plans concurrency from the
resources. ``MAX_IN_FLIGHT`` is only a safety ceiling on open threads/
connections, never a pace.

With grade=false, run random smoke-call rounds (same public call, no grade).
Model selection, rounds, stop, the job registry and the call-log-backed history
are unchanged.

Routes (bare and under /api, like the rest of the worker surface):

    POST /fleet/workers/<id>/test-fire                    {rounds?, max_tokens?, seed?, grade?}
                                                        -> {job_id, ...}   409 if one is already running
    GET  /fleet/workers/<id>/test-fire                    the worker's current/last job (or 404)
    GET  /fleet/workers/<id>/test-fire/current            same (explicit alias; never read as a job id)
    GET  /fleet/workers/<id>/test-fire/<job_id>           {running, round, done_calls, total_planned,
                                                         results[], summary{ok, failed, per_model}}
    POST /fleet/workers/<id>/test-fire/<job_id>/stop      stop after in-flight calls finish
                                                        (in-flight jobs get the authoritative cancel)

Model SELECTION reads the catalog rows the console already renders
(``get_models_dict(dict_return=True)`` -> ``tasks`` / ``primary_task``): a
model is text-gen when it carries ``text-generation`` / ``text2text-generation``
— even alongside a vision task (a VL chat model answers a text prompt too);
rows whose tasks are ONLY non-text (embedding, image gen, ASR, ...) are not
targets. Operator-
blocked and archive-marked keys are skipped. The candidate set is the worker's
designations plus what it holds locally (``models``, ``models_local`` and the
storage rows), i.e. "that worker's models" as the row shows them.

Results are kept in memory only: a ring of the last ``RESULT_RING`` calls per
job plus per-model last status; finished jobs stay readable until
``MAX_FINISHED`` newer ones displace them.
"""
from __future__ import annotations

import contextvars
import os
import random
import threading
import time
import uuid
from collections import OrderedDict, deque
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Iterable, Optional

from abstract_flask import get_bp

# ``test_fire_bp`` is kept defined for ``hugpy_core.routes`` but registers no
# routes — the console's worker-ID test-fire URLs now live in ``routes.py``.
test_fire_bp, logger = get_bp("test_fire_bp", __name__)

# ── selection vocabulary ─────────────────────────────────────────────────────
TEXT_GEN_TASKS = frozenset({"text-generation", "text2text-generation"})
# Non-text task vocabulary (vision-language, image/video generation, audio,
# embeddings, rerank, parts). A row carrying ONLY these is not a target; a row
# that ALSO carries a TEXT_GEN_TASKS entry (e.g. a VL chat model) still is.
NON_TEXT_TASKS = frozenset({
    "image-text-to-text", "visual-question-answering", "image-to-text",
    "text-to-image", "image-to-image", "image-to-video", "text-to-video",
    "automatic-speech-recognition", "text-to-speech", "audio-classification",
    "feature-extraction", "sentence-similarity", "keyword-extraction",
    "embedding", "rerank", "reranking",
    "depth-estimation", "object-detection", "image-classification",
    "image-segmentation", "pipeline-component", "adapter", "needs-classification",
})

PROMPTS = (
    "Reply with one short sentence: what is 2+2?",
    "Name one primary color.",
    "Say hello in one word.",
    "What is the capital of France? Answer briefly.",
    "Finish this: the sky is",
    "Give a one-word synonym for 'fast'.",
    "Count from 1 to 3.",
    "What color is grass? One word.",
)

RESULT_RING = 200
MAX_FINISHED = 20
DEFAULT_MAX_TOKENS = 32
MAX_MAX_TOKENS = 512
MAX_ROUNDS = 1000
# Operator 2026-11-16: the test fire makes NO concurrency decision — it submits
# every planned call in list order and lets the Wrapper's queue plan concurrency
# from the resources. This bound only protects Core from an unbounded thread/
# connection burst (a huge curriculum); it is a safety ceiling, never a pace.
MAX_IN_FLIGHT = 1000
# CONNECT timeout only: an unreachable Core fails fast. There is deliberately NO
# read timeout — the Wrapper owns every call's outcome (serve it, or fail it with
# a reason: never fits, copy failed, engine died), and the test fire waits for
# that verdict however long the queue takes. A broken connection (Core/Wrapper
# restart) surfaces as an immediate error, recorded as a failed call.
CONNECT_TIMEOUT_S = 30


def model_tasks(row: dict) -> set:
    """The task vocabulary the harness/assortment use: ``tasks`` ∪ ``primary_task``."""
    tasks = set(t for t in (row.get("tasks") or []) if isinstance(t, str))
    pt = row.get("primary_task")
    if isinstance(pt, str) and pt:
        tasks.add(pt)
    return tasks


def is_text_gen(row: dict) -> bool:
    """Text-capable: carries ``text-generation`` / ``text2text-generation``.
    A ``['image-text-to-text', 'text-generation']`` VL row IS a target (it
    answers a text-only prompt); rows with only NON_TEXT_TASKS are not."""
    if not isinstance(row, dict):
        return False
    return bool(model_tasks(row) & TEXT_GEN_TASKS)


def worker_model_keys(worker: dict) -> list:
    """Ordered, de-duplicated candidate keys: designations + local files +
    storage rows — what the worker row lists as 'its' models."""
    seen: "OrderedDict[str, None]" = OrderedDict()
    for k in (worker.get("models") or []):
        if isinstance(k, str) and k:
            seen.setdefault(k, None)
    for k in (worker.get("models_local") or []):
        if isinstance(k, str) and k:
            seen.setdefault(k, None)
    storage = worker.get("storage") or {}
    for r in (storage.get("models") or []) if isinstance(storage, dict) else []:
        k = r.get("model_key") if isinstance(r, dict) else None
        if isinstance(k, str) and k:
            seen.setdefault(k, None)
    return list(seen.keys())


def _catalog_row(catalog: dict, key: str) -> Optional[dict]:
    """Registry lookup tolerant of the bare/qualified spellings (``owner~X`` vs
    ``X``) the worker roster carries; exact key first."""
    row = catalog.get(key)
    if isinstance(row, dict):
        return row
    tail = key.split("~", 1)[1] if "~" in key else None
    if tail and isinstance(catalog.get(tail), dict):
        return catalog[tail]
    for k, r in catalog.items():
        if isinstance(r, dict) and (r.get("model_key") == key or k.split("~", 1)[-1] == key):
            return r
    return None


def _key_forms(key: str) -> set:
    """Spellings one model id can wear across the catalog / a worker's store:
    ``owner/X`` (hub id), ``owner~X`` (qualified key), ``X`` (bare key)."""
    k = str(key or "").strip().rstrip("/")
    if not k:
        return set()
    forms = {k, k.lower()}
    for sep in ("/", "~"):
        if sep in k:
            owner, tail = k.split(sep, 1)
            forms |= {tail, tail.lower(), f"{owner}~{tail}", f"{owner}/{tail}",
                      f"{owner}~{tail}".lower(), f"{owner}/{tail}".lower()}
    return forms


def adapter_base_on_worker(base_model: Optional[str], worker: dict) -> bool:
    """True when the adapter's ``base_model`` (hub id) is among the keys this
    worker's store / designations carry, under any spelling."""
    want = _key_forms(base_model)
    if not want:
        return False
    for key in worker_model_keys(worker):
        if _key_forms(key) & want:
            return True
    return False


def unserveable_reason(row: dict) -> Optional[str]:
    """The catalog's own ``extra.serveable=False`` verdict (e.g. the engine's
    "PEFT adapter (base '…') — … NOT in this store" refusal), else None."""
    extra = row.get("extra")
    if isinstance(extra, dict) and extra.get("serveable") is False:
        return str(extra.get("unserveable_reason") or "marked unserveable")
    return None


def worker_blocked_reasons(worker_id: str) -> dict:
    """{model_key: reason} for pairs blocked on this worker — an operator block or
    the Wrapper's automatic-fit feasibility verdict (user_settings.auto_blocked,
    set by intake from the Wrapper's possible=false report). Fail-open: a read
    error never stops a run, it just leaves those pairs unskipped (routing's
    blocked_worker_ids still refuses them)."""
    try:
        from hugpy_core.models.modeldb import worker_blocked_reasons as _reasons
        return _reasons(worker_id)
    except Exception:  # noqa: BLE001
        logger.debug("test-fire: blocked-pair read failed for %s", worker_id, exc_info=True)
        return {}


def blocked_pair_reason(blocks: dict, model_key: str) -> Optional[str]:
    """The block reason for ``model_key`` among a worker's blocked pairs, tolerant
    of the owner~/owner/ /bare key spellings, or None when the pair is not blocked."""
    reason = blocks.get(model_key)
    if reason is not None:
        return reason
    from hugpy_core.models.keys import model_key_forms, serveable_match
    wanted = model_key_forms(model_key)
    for k, why in blocks.items():
        if serveable_match(model_key, wanted, [k]):
            return why
    return None


def worker_drive_models(worker: dict) -> dict:
    """{model key: its weights files} of the complete copies on the worker's own serving drives (its worker and
    immutable roots), from its storage survey. A run that calls only these never waits on a copy."""
    out = {}
    storage = worker.get("storage") or {}
    for r in (storage.get("models") or []) if isinstance(storage, dict) else []:
        if isinstance(r, dict) and r.get("role") in ("worker", "immutable") and r.get("complete") is not False \
                and isinstance(r.get("model_key"), str):
            out.setdefault(r["model_key"], set()).update(v for v in (r.get("variations") or []) if isinstance(v, str))
    return out


def on_worker_drive(key: str, on_drive: dict) -> bool:
    """Whether model `key` ("org/name" or "org/name::file") has its copy among `on_drive` (worker_drive_models)."""
    from fnmatch import fnmatch
    repo, _, variation = key.partition("::")
    files = on_drive.get(repo)
    if files is None:
        return False
    return not variation or variation == "*" or not files or variation in files or any(fnmatch(variation, f) for f in files)


def select_text_gen_models(worker: dict, catalog: dict,
                           blocked: Iterable[str] = (),
                           archived: Iterable[str] = (), grade: bool = False) -> tuple:
    """(selected, skipped) for one worker. ``selected`` rows are
    ``{model_key, framework, tasks}``; ``skipped`` rows carry a ``reason``.

    Rows that cannot load deterministically are skipped up front so the strip
    can say "skipped: base missing" instead of painting a red failure: the
    catalog's ``extra.serveable=False`` verdict, and a PEFT/LoRA adapter row
    (``base_model`` set) whose base is not in THIS worker's store."""
    blocked = set(blocked or ())
    archived = set(archived or ())
    selected, skipped = [], []
    for key in worker_model_keys(worker):
        if key in blocked:
            skipped.append({"model_key": key, "reason": "operator-blocked"})
            continue
        if key in archived:
            skipped.append({"model_key": key, "reason": "archive-marked"})
            continue
        row = _catalog_row(catalog, key)
        if row is None:
            skipped.append({"model_key": key, "reason": "not in catalog"})
            continue
        if row.get("blocked"):
            skipped.append({"model_key": key, "reason": "operator-blocked"})
            continue
        if grade:
            from hugpy_core.grading import grader
            eligible = bool(grader.suites_for_tasks(model_tasks(row)))
        else:
            eligible = is_text_gen(row)
        if not eligible:
            skipped.append({"model_key": key,
                            "reason": ("no installed grading suite: " if grade else "not text-gen: ") + (",".join(sorted(model_tasks(row))) or "no task")})
            continue
        why = unserveable_reason(row)
        if why:
            skipped.append({"model_key": key, "reason": "unserveable: " + why,
                            "kind": "base missing" if "PEFT adapter" in why else "unserveable"})
            continue
        base = row.get("base_model")
        if isinstance(base, str) and base.strip() and not adapter_base_on_worker(base, worker):
            skipped.append({"model_key": key, "kind": "base missing",
                            "reason": f"adapter base {base!r} is not in this worker's store"})
            continue
        selected.append({"model_key": key,
                         "framework": row.get("framework"),
                         "tasks": sorted(model_tasks(row) if grade else model_tasks(row) & TEXT_GEN_TASKS)})
    return selected, skipped


# ── error classification (mirrors the harness's structured_error markers) ────
_ERROR_KINDS = (
    ("LoadRefusal", "loadrefusal"),
    ("fit_failure", "fit_failure"),
    ("fit_failure", "does not fit"),
    ("worker_busy", "worker_busy"),
    ("model_busy", "model_busy"),
    ("requested_worker", "requested worker"),
    ("context_overflow", "context length"),
    ("capacity", "admission cap"),
    ("timeout", "timed out"),
    ("timeout", "timeout"),
)


def classify_error(message: Optional[str]) -> Optional[str]:
    if not message:
        return None
    low = str(message).lower()
    for kind, marker in _ERROR_KINDS:
        if marker in low:
            return kind
    return "error"


# ── history (2026-10-02): runs + results persisted, fail-open ────────────────
def _history():
    """The persistence module, or None when disabled (HUGPY_TEST_FIRE_HISTORY=0)."""
    if os.environ.get("HUGPY_TEST_FIRE_HISTORY", "1") == "0":
        return None
    from hugpy_core.testfire import test_fire_store
    return test_fire_store


def _persist(fn_name: str, *args) -> None:
    h = _history()
    if h is None:
        return
    try:
        getattr(h, fn_name)(*args)
    except Exception:  # noqa: BLE001 — history never breaks a run
        logger.debug("test-fire history %s failed", fn_name, exc_info=True)


# ── bookkeeping ──────────────────────────────────────────────────────────────
class TestFireJob:
    """In-memory state for one test-fire run (thread-safe snapshot/record)."""

    def __init__(self, worker_id: str, worker_name: str, models: list, *,
                 rounds: int = 1,
                 max_tokens: int = DEFAULT_MAX_TOKENS, seed: Optional[int] = None,
                 skipped: Optional[list] = None, first_order: Optional[list] = None,
                 resumed_from: Optional[str] = None, grade: bool = True):
        self.job_id = uuid.uuid4().hex[:12]
        self.grade = bool(grade)   # complete the remaining cumulative curriculum
        self.grading = {}
        self.grading_planned = None
        self.worker_id = worker_id
        self.worker_name = worker_name
        self.model_tasks = {m["model_key"]: m.get("tasks", []) for m in models if isinstance(m, dict)}
        self.models = [m["model_key"] if isinstance(m, dict) else str(m) for m in models]
        self.rounds = int(rounds)            # 0 = until stopped (smoke only)
        self.submitted = 0                   # calls sent so far (the job paces nothing)
        self.max_tokens = int(max_tokens)
        self.seed = seed
        self.skipped = list(skipped or [])
        # RESUME (2026-10-02): round 1 runs exactly this order (the rest of an
        # interrupted round, its in-flight model first); later rounds shuffle.
        self.first_order = [str(m) for m in (first_order or [])] or None
        self.resumed_from = resumed_from
        self.current_model: Optional[str] = None
        self.created = time.time()
        self.started: Optional[float] = None
        self.finished: Optional[float] = None
        self.running = False
        self.round = 0
        self.done_calls = 0
        self.ok = 0
        self.failed = 0
        self.brain_review = {"status": "waiting", "queued": 0, "reviewed": 0}
        self.stop_reason: Optional[str] = None
        self.results: deque = deque(maxlen=RESULT_RING)
        self.per_model: dict = {k: {"ok": 0, "failed": 0, "grade_passed": 0,
                                    "grade_failed": 0, "last_status": None,
                                    "last_error": None, "last_latency_s": None,
                                    "last_tok_s": None, "last_at": None}
                                for k in self.models}
        self.in_flight: dict = {}   # request_id -> model_key
        self._stop = threading.Event()
        self._lock = threading.Lock()
        self.thread: Optional[threading.Thread] = None
        # Open HTTP connections of in-flight calls, so a stop can shut them down
        # (the Wrapper then cancels the queued rows). Guarded by its own lock.
        self._conns: dict = {}      # client_request_id -> http.client connection
        self._cancelled: dict = {}  # client_request_id -> cancel reason
        self._cancelling = False
        self._conn_lock = threading.Lock()

    def call_metadata(self):
        """The submitted run options travel on its calls, not a run side table."""
        from hugpy_core.brain.intent import GRADING, SMOKE_TEST
        return {"intent": GRADING if self.grade else SMOKE_TEST,
                "test_fire": {"job_id": self.job_id, "worker_id": self.worker_id, "models": self.models,
                "rounds": self.rounds,
                "max_tokens": self.max_tokens, "grade": self.grade,
                "resumed_from": self.resumed_from}}

    # ----- control
    @property
    def total_planned(self) -> Optional[int]:
        if self.grade:
            return self.grading_planned
        if self.rounds == 0:
            return None
        if self.first_order:
            return len(self.first_order) + (self.rounds - 1) * len(self.models)
        return self.rounds * len(self.models)

    def stop_requested(self) -> bool:
        return self._stop.is_set()

    def request_stop(self, reason: str = "operator") -> None:
        with self._lock:
            if self.stop_reason is None:
                self.stop_reason = reason
        self._stop.set()

    # ----- in-flight cancellation (stop ends the queued calls, no read timeout)
    def register_conn(self, client_rid: str, conn) -> None:
        """A call's live HTTP connection. If the job is already cancelling, shut
        it down at once (this call was submitted just as stop arrived)."""
        with self._conn_lock:
            if self._cancelling:
                self._cancelled[client_rid] = self._cancelled.get(client_rid) or "test fire stopped"
                _shutdown_conn(conn)
                return
            self._conns[client_rid] = conn

    def unregister_conn(self, client_rid: str) -> None:
        with self._conn_lock:
            self._conns.pop(client_rid, None)

    def cancel_reason_for(self, client_rid: str) -> Optional[str]:
        with self._conn_lock:
            return self._cancelled.get(client_rid)

    def cancel_in_flight(self, reason: str = "test fire stopped") -> list:
        """Shut down every in-flight call's connection so the Wrapper cancels its
        queued row; mark each cancelled with ``reason``. Returns the cancelled
        calls (``{request_id, model_key}``). Late-starting calls self-cancel via
        ``register_conn``. The run ends on its own once these connections close."""
        with self._conn_lock:
            self._cancelling = True
            items = list(self._conns.items())
            for rid, _conn in items:
                self._cancelled[rid] = reason
            self._conns.clear()
        with self._lock:
            models = dict(self.in_flight)
        for _rid, conn in items:
            _shutdown_conn(conn)
        return [{"request_id": rid, "model_key": models.get(rid)} for rid, _conn in items]

    # ----- recording
    def mark_in_flight(self, request_id: Optional[str], model_key: str) -> None:
        if request_id:
            with self._lock:
                self.in_flight[request_id] = model_key
        self.current_model = model_key
        _persist("save_run", self)

    def record(self, result: dict) -> None:
        """Append one call result and fold it into the counters/per-model view."""
        key = result.get("model_key")
        rid = result.get("client_request_id") or result.get("request_id")
        with self._lock:
            if rid:
                self.in_flight.pop(rid, None)
            if self.current_model == key:
                self.current_model = None
            self.results.append(result)
            self.done_calls += 1
            pm = self.per_model.setdefault(key, {"ok": 0, "failed": 0,
                                                 "grade_passed": 0, "grade_failed": 0,
                                                 "last_status": None,
                                                 "last_error": None, "last_latency_s": None,
                                                 "last_tok_s": None, "last_at": None})
            if result.get("ok"):
                self.ok += 1
                pm["ok"] += 1
            else:
                self.failed += 1
                pm["failed"] += 1
            passed = (result.get("grade") or {}).get("passed")
            if passed is True:
                pm["grade_passed"] += 1
            elif passed is False:
                pm["grade_failed"] += 1
            pm["last_status"] = "ok" if result.get("ok") else "fail"
            pm["last_error"] = result.get("error")
            pm["last_error_kind"] = result.get("error_kind")
            pm["last_interrupted"] = bool(result.get("interrupted"))
            pm["last_latency_s"] = result.get("latency_s")
            pm["last_tok_s"] = result.get("tok_s")
            pm["last_at"] = result.get("started")
        _persist("save_result", self, result)
        _persist("save_run", self)

    def snapshot(self, limit: int = RESULT_RING) -> dict:
        with self._lock:
            results = list(self.results)[-limit:]
            per_model = {k: dict(v) for k, v in self.per_model.items()}
            in_flight = dict(self.in_flight)
        return {
            "job_id": self.job_id,
            "worker_id": self.worker_id,
            "worker": self.worker_name,
            "running": self.running,
            "round": self.round,
            "rounds": self.rounds,
            "submitted": self.submitted,
            "max_tokens": self.max_tokens,
            "seed": self.seed,
            "grade": self.grade,
            "grading": {key: dict(value) for key, value in self.grading.items()},
            "models": list(self.models),
            "skipped": list(self.skipped),
            "resumed_from": self.resumed_from,
            "done_calls": self.done_calls,
            "total_planned": self.total_planned,
            "in_flight": [{"request_id": r, "model_key": k} for r, k in in_flight.items()],
            "stop_requested": self.stop_requested(),
            "stop_reason": self.stop_reason,
            "created": self.created,
            "started": self.started,
            "finished": self.finished,
            "brain_review": dict(self.brain_review),
            "results": results,
            "summary": {"ok": self.ok, "failed": self.failed,
                        "total": self.done_calls, "per_model": per_model},
        }


# ── the run loop (pure: the call function is injected) ───────────────────────
def run_job(job: TestFireJob, call_fn: Callable[..., dict],
            prompts: tuple = PROMPTS) -> None:
    """Complete remaining grading, or run random smoke rounds when grade=false.

    ``call_fn``
    (model_key, prompt, max_tokens, job) -> result dict. Stops when the round
    budget is spent, on ``request_stop`` (after in-flight calls finish), or when
    there are no models."""
    rng = random.Random(job.seed)
    job.started = time.time()
    job.running = True
    _persist("save_run", job)
    try:
        if not job.models:
            job.request_stop("no eligible models")
            return
        if job.grade:
            _plan_grading(job)
        _submit_all(job, call_fn, prompts, rng)
        if job.grade:
            _finalize_grading(job)
        elif not job.stop_requested():
            job.stop_reason = "complete"
    except Exception as exc:  # noqa: BLE001 — the loop must always finish
        logger.exception("test-fire %s: run loop failed", job.job_id)
        job.request_stop(f"loop error: {type(exc).__name__}: {exc}")
    finally:
        job.running = False
        job.finished = time.time()
        if job.stop_reason is None:
            job.stop_reason = "complete"
        # release the worker's sequester — other traffic may be placed there again
        from hugpy_core.relay.pick import release
        release(job.worker_id, job.job_id)
        _persist("save_run", job)
        if os.environ.get("HUGPY_TEST_FIRE_BRAIN", "1").strip().lower() not in ("0", "false", "off", "no"):
            try:
                from hugpy_core.brain import test_fire_review
                test_fire_review.queue(job)
            except Exception:  # noqa: BLE001 — review must not change the run result
                logger.exception("test-fire %s: queueing brain review failed", job.job_id)


def _plan_grading(job: TestFireJob) -> None:
    """Record per-model remaining curriculum (the grading view the console reads)
    and the total planned call count, BEFORE any call is submitted."""
    from hugpy_core.grading import grader
    order = list(dict.fromkeys((job.first_order or []) + job.models))
    progress = {}
    catalog = _catalog() if any(not job.model_tasks.get(key) for key in order) else {}
    for key in order:
        tasks = job.model_tasks.get(key) or model_tasks(_catalog_row(catalog, key) or {})
        suites = grader.suites_for_tasks(tasks)
        remaining = [item for suite in suites for item in grader.pending_items(key, suite)]
        progress[key] = {"remaining": len(remaining), "graded_this_run": 0, "suites": suites,
                         "status": ("pending" if remaining else "complete") if suites else "incomplete"}
        if not suites:
            progress[key]["error"] = "No installed grading suite matches this model's current tasks"
    job.grading = progress
    job.grading_planned = sum(row["remaining"] for row in job.grading.values())
    _persist("save_run", job)


def _iter_calls(job: TestFireJob, prompts: tuple, rng: random.Random):
    """Yield the planned calls as ``(model_key, prompt, item)`` in submission
    order — the ONE thing the test fire decides. Grading drains every pending
    curriculum item, model by model, in curriculum order. Smoke walks each
    round's model order (round 1 = first_order when resuming, else shuffled;
    rounds=0 = until stopped). The caller submits each without waiting."""
    if job.grade:
        from hugpy_core.grading import grader
        for key in dict.fromkeys((job.first_order or []) + job.models):
            state = job.grading.get(key) or {}
            for suite in state.get("suites") or []:
                for item in grader.pending_items(key, suite):
                    if job.stop_requested():
                        return
                    yield key, item["prompt"], item
        return
    while not job.stop_requested():
        if job.rounds and job.round >= job.rounds:
            return
        job.round += 1
        order = list(job.first_order) if (job.round == 1 and job.first_order) else list(job.models)
        if not (job.round == 1 and job.first_order):
            rng.shuffle(order)
        for key in order:
            if job.stop_requested():
                return
            yield key, rng.choice(prompts), None


def _submit_all(job: TestFireJob, call_fn, prompts: tuple, rng: random.Random) -> None:
    """Submit EVERY planned call in list order, each on its own thread, WITHOUT
    waiting for earlier calls — the Wrapper's queue plans concurrency from the
    resources. The only bound is MAX_IN_FLIGHT, a safety ceiling (a semaphore
    caps outstanding submissions so a huge curriculum cannot open unbounded
    threads/connections); it never paces a run that fits under it. A stop halts
    submission; calls already sent finish or fail on their own."""
    gate = threading.Semaphore(MAX_IN_FLIGHT)
    futures = []
    with ThreadPoolExecutor(max_workers=MAX_IN_FLIGHT, thread_name_prefix=f"tf-{job.job_id}") as pool:
        def one(key, prompt, item):
            try:
                _guarded_call(call_fn, key, prompt, job, item)
            finally:
                gate.release()
        for key, prompt, item in _iter_calls(job, prompts, rng):
            if job.stop_requested():
                break
            gate.acquire()
            if job.stop_requested():
                gate.release()
                break
            with job._lock:
                job.submitted += 1
            futures.append(pool.submit(one, key, prompt, item))
        for fut in futures:
            fut.result()


def _finalize_grading(job: TestFireJob) -> None:
    """After every grading call has been assessed, recompute each model's
    remaining items and set its status + the run's stop_reason from the grades
    the call log now holds (a fault leaves a model incomplete, for resume)."""
    from hugpy_core.grading import grader
    for key, state in job.grading.items():
        if not state.get("suites"):
            continue
        try:
            state["remaining"] = sum(len(grader.pending_items(key, suite)) for suite in state["suites"])
        except Exception as exc:  # noqa: BLE001
            logger.exception("test-fire %s: grading recount failed for %s", job.job_id, key)
            state.update(status="incomplete", error=f"{type(exc).__name__}: {exc}")
            continue
        if job.stop_requested() and state["remaining"]:
            state["status"] = "interrupted"
        else:
            state["status"] = "complete" if state["remaining"] == 0 else "incomplete"
    if not job.stop_requested():
        job.stop_reason = ("complete" if all(s.get("status") == "complete" for s in job.grading.values())
                           else "grading incomplete")


_ITEM: contextvars.ContextVar = contextvars.ContextVar("test_fire_item", default=None)


def _item_metadata() -> dict:
    """The curriculum item the current call asks, carried on the call itself
    (metadata.grade): its grade derives from the call log alone
    (grader.fill_from_call_log), with no test-fire job left to remember it."""
    item = _ITEM.get()
    return {"intent": "grading", "grade": {k: item[k] for k in ("suite", "category", "tier")}} if item else {}


def _guarded_call(call_fn, key, prompt, job, item=None) -> dict:
    t0 = time.time()
    tokens = job.max_tokens
    if item:
        from hugpy_core.grading import grader
        tokens = max(job.max_tokens, grader.TOKENS)
    asked = _ITEM.set(item)
    try:
        if item and item["suite"] != grader.SUITE:
            res = fire_media(key, item, tokens, job)
        else:
            res = call_fn(key, prompt, tokens, job)
    except Exception as exc:  # noqa: BLE001
        res = {"ok": False, "error": f"{type(exc).__name__}: {exc}",
               "error_kind": classify_error(f"{exc}") or "exception"}
    finally:
        _ITEM.reset(asked)
    res = dict(res or {})
    res.setdefault("model_key", key)
    res.setdefault("prompt", prompt)
    res.setdefault("started", t0)
    res.setdefault("latency_s", round(time.time() - t0, 3))
    res.setdefault("ok", False)
    res.setdefault("round", job.round)
    if not res["ok"] and res.get("error_kind") is None:
        res["error_kind"] = classify_error(res.get("error"))
    # a stop that arrived while this call was in flight: the item is marked stopped,
    # never graded on whatever (partial) reply came back before the stop.
    if item and job.stop_requested() and not res.get("interrupted"):
        res["interrupted"] = True
        res["interrupted_why"] = "interrupted by operator stop"
    if item:
        _grade(key, item, res)
    res.pop("_grade_response", None)
    res.pop("text", None)        # the full reply lives in the call log, not the poll payload
    job.record(res)
    return res


def _grade(key: str, item: dict, res: dict) -> None:
    """Check the reply against the item and record the verdict (a pointer to the
    call by request_id). A failed CALL is recorded ungraded (passed NULL) and the
    item is asked again next run."""
    from hugpy_core.grading import grader
    try:
        if res.get("interrupted"):
            # a call cut short by an unload / cancel / stop is NOT a verdict: it is
            # recorded passed NULL so the item stays pending (resume re-asks it),
            # never a pass on a partial reply.
            passed, answer, why = None, None, res.get("interrupted_why") or "interrupted by unload/cancel"
        elif not res.get("ok") or res.get("error"):
            passed, answer, why = None, None, f"call failed: {res.get('error') or 'unsuccessful completion'}"
        else:
            passed, answer, why = grader.check(item, res.get("text") or "", res.get("_grade_response"))
        if passed is not None and not res.get("execution_request_id"):
            raise ValueError("No execution call-log pointer returned; item remains incomplete")
        if passed is not None:
            grader.record(key, item, request_id=res.get("request_id"), passed=passed,
                          why=None if passed else "Response did not satisfy the suite criterion")
        elif res.get("interrupted") and res.get("request_id"):
            # record the interruption as a NULL verdict with its reason when there is
            # a call to point at (idempotent per request_id); pending_items ignores
            # passed-NULL rows, so the item is re-asked on resume.
            grader.record(key, item, request_id=res.get("request_id"), passed=None, why=why)
        res["grade"] = {"suite": item["suite"], "category": item["category"], "tier": item["tier"],
                        "passed": passed, "why": why, "expected": item.get("expected")}
    except Exception:  # noqa: BLE001 — a grading fault never fails the call's result
        res["grading_error"] = "Grade could not be saved; this item remains incomplete"
        logger.exception("test-fire: grade record failed for %s", key)


# ── the call: Core's OWN public /v1/chat/completions, pinned + job-tagged ────
def _shutdown_conn(conn) -> None:
    """Break a blocked ``getresponse`` by shutting the socket down, then close it.
    The far side (Core -> Wrapper) sees the client disconnect and cancels the
    queued row."""
    try:
        sock = getattr(conn, "sock", None)
        if sock is not None:
            import socket as _socket
            sock.shutdown(_socket.SHUT_RDWR)
    except OSError:
        pass
    try:
        conn.close()
    except Exception:  # noqa: BLE001
        pass


def _post_chat(payload: dict, job=None, client_rid=None) -> tuple:
    """POST ``payload`` to this Core's own public ``/v1/chat/completions`` and
    return ``(http_status, core_request_id, body, transport_error)``. The server
    records the call like any client's; its row id rides back in
    ``X-Hugpy-Request-Id``. Overridable in place so tests supply a fake endpoint.

    CONNECT timeout only (``CONNECT_TIMEOUT_S``): an unreachable Core fails fast,
    but the read has NO timeout — a queued call waits for the Wrapper's verdict
    however long it takes. The socket timeout is cleared right after connect; a
    dropped connection then surfaces as an immediate error, recorded as a failure."""
    import http.client
    import json
    from urllib.parse import urlparse
    from hugpy_core.imports.functions import local_base
    # Core's OWN loopback listener, never the public proxy domain: an in-box call
    # with no bearer/cookie passes guest_access straight through (no auth, no
    # proxy timeout). See guest_access: a non-projected request falls through.
    u = urlparse(local_base().rstrip("/") + "/v1/chat/completions")
    conn_cls = http.client.HTTPSConnection if u.scheme == "https" else http.client.HTTPConnection
    conn = conn_cls(u.hostname, u.port, timeout=CONNECT_TIMEOUT_S)
    try:
        conn.connect()
        conn.sock.settimeout(None)   # read has no deadline: wait for the queue's verdict
        # Register the live connection with the job so a stop can shut this
        # socket down: the Wrapper then sees the client disconnect and cancels
        # the queued row (there is still no read timeout). register_conn closes
        # it at once if the job is already cancelling.
        if job is not None and client_rid is not None:
            job.register_conn(client_rid, conn)
        conn.request("POST", u.path, body=json.dumps(payload).encode("utf-8"),
                     headers={"Content-Type": "application/json"})
        resp = conn.getresponse()
        rid = resp.getheader("X-Hugpy-Request-Id")
        raw = resp.read().decode("utf-8", "replace")
        try:
            body = json.loads(raw or "{}")
        except ValueError:
            body = {"error": raw[:2000]}
        return resp.status, rid, body, None
    except Exception as exc:  # noqa: BLE001 — a transport failure (incl. a stop's socket shutdown) is a result, not a crash
        return None, None, None, f"{type(exc).__name__}: {exc}"
    finally:
        if job is not None and client_rid is not None:
            job.unregister_conn(client_rid)
        conn.close()


def fire_one(model_key: str, prompt: str, max_tokens: int, job: TestFireJob) -> dict:
    """One tiny completion through Core's OWN public /v1/chat/completions, pinned
    to the job's worker (the public ``alloc.worker`` steer) and tagged with the
    job so it passes the worker's sequester. Core routes, serves and RECORDS it
    like any client's call; the result is then read back from that call-log row."""
    client_rid = f"tf-{job.job_id}-{uuid.uuid4().hex[:8]}"
    job.mark_in_flight(client_rid, model_key)
    started = time.time()
    payload = {
        "model": model_key,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": int(max_tokens),
        "temperature": 0.0,
        "stream": False,
        "alloc": {"worker": job.worker_id},     # the same per-request worker steer any client uses
        "metadata": {**job.call_metadata(), **_item_metadata()},   # carries test_fire.job_id + the grade item
    }
    status, core_request_id, body, transport_error = _post_chat(payload, job, client_rid)
    return _assess_from_call_log(job, model_key, prompt, int(max_tokens), started,
                                 client_rid, core_request_id, status, body, transport_error)


def _assess_from_call_log(job, model_key, prompt, max_tokens, started, client_rid,
                          core_request_id, http_status, http_body, transport_error) -> dict:
    """Read this call's OWN call-log row back and shape the job's result from it:
    status, error, latency, tokens, tok/s and the reply text. The call log is the
    source; the HTTP body is used only when the row cannot be read."""
    from hugpy_core.grading import grader
    row = {}
    if core_request_id:
        try:
            from hugpy_core.calllog.calllog import by_request_ids
            row = by_request_ids([core_request_id]).get(core_request_id) or {}
        except Exception:  # noqa: BLE001 — fall back to the HTTP result
            logger.debug("test-fire: call-log read for %s failed", core_request_id, exc_info=True)
    response_body = row.get("response_body")
    if not isinstance(response_body, dict):
        response_body = http_body if isinstance(http_body, dict) else {}
    status = row.get("http_status") if row.get("http_status") is not None else http_status
    error_message = row.get("error") or transport_error
    if error_message is None and response_body.get("error"):
        error_message = str(response_body.get("error"))

    text = grader.reply_text(response_body) or ""
    usage = response_body.get("usage") if isinstance(response_body.get("usage"), dict) else None
    tokens = usage.get("completion_tokens") if usage else None
    timings = response_body.get("timings") if isinstance(response_body.get("timings"), dict) else None
    served = response_body.get("hugpy") if isinstance(response_body.get("hugpy"), dict) else {}
    execution_id = served.get("execution_request_id")
    worker_seen = row.get("worker") or served.get("worker")
    latency = row.get("total_s")
    latency = round(float(latency), 3) if latency is not None else round(time.time() - started, 3)

    choices = response_body.get("choices") if isinstance(response_body.get("choices"), list) else []
    finish_reason = choices[0].get("finish_reason") if choices and isinstance(choices[0], dict) else None
    # a thinking model can spend the whole (small) test budget reasoning: empty
    # answer text but tokens generated is a pass. A call the box ended by
    # cancel/unload (finish 'cancelled') is never a pass on partial text.
    interrupted = finish_reason == "cancelled"
    # A stop shut this call's socket down (the Wrapper cancels the queued row):
    # it is never a completion, and carries the stop reason, whatever the
    # transport error text was.
    cancel_reason = job.cancel_reason_for(client_rid)
    interrupted_why = None
    if cancel_reason:
        interrupted, error_message, interrupted_why = True, cancel_reason, cancel_reason
    elif interrupted:
        interrupted_why = "interrupted by unload/cancel"
    ok = (status == 200) and error_message is None and not interrupted and (bool(text.strip()) or bool(tokens))
    if interrupted and error_message is None:
        error_message = interrupted_why or "interrupted by unload/cancel"
    if not ok and error_message is None:
        error_message = (f"HTTP {status}" if status and status != 200
                         else "empty completion (0 tokens generated)")

    tok_s = _tok_per_s(timings, tokens, latency)
    return {
        "model_key": model_key,
        "request_id": execution_id or core_request_id or client_rid,
        "execution_request_id": execution_id, "client_request_id": client_rid,
        "prompt": prompt,
        "started": started,
        "latency_s": latency,
        "ok": ok,
        "interrupted": interrupted,
        "interrupted_why": interrupted_why,
        "status": "cancelled" if cancel_reason else "interrupted" if interrupted else "ok" if ok else "fail",
        "tokens": tokens,
        "tok_s": tok_s,
        "worker": worker_seen,
        "text": text[:20000],
        "content80": text[:80] if text else
                     (f"(reasoning only — {tokens} tokens of thinking hit the {int(max_tokens)}-token test limit)"
                      if ok else None),
        # answered = visible text; reasoning_only = a thinking model spent the
        # whole test budget reasoning (it works — it just did not reach an answer)
        "outcome": ("answered" if (ok and text.strip()) else "reasoning_only" if ok else "fail"),
        "error": None if ok else str(error_message)[:2000],
        "error_kind": None if ok else classify_error(error_message),
    }


def fire_media(model_key: str, item: dict, max_tokens: int, job: TestFireJob) -> dict:
    """Media grading item: the installed suite's worker-native request.

    Core has no public OpenAI route that carries a media grading adapter's
    worker-native ``/infer/stream`` / media request as-is, so (unlike fire_one)
    this still relays through hugpy_core directly, pinned + job-tagged. It binds
    its own call row so the pin passes the worker's sequester, and records that
    one row for the call-log assessment. See the module docstring: converting
    this to the public media surface is a grading-adapter change, reported."""
    import json
    import urllib.request
    from hugpy_core.grading import grader
    from hugpy_core.relay.pick import pick
    from hugpy_core.relay.relay import worker_payload, worker_stream
    from hugpy_core.calllog.call_record import bound_call, start, finish, write
    adapter = grader.providers()[item["suite"]]
    request_id = f"tf-{job.job_id}-{uuid.uuid4().hex[:8]}"
    job.mark_in_flight(request_id, model_key)
    started = time.time()
    worker_name = None
    execution_id = None
    call_row = start({"model": model_key, "metadata": {**job.call_metadata(), **_item_metadata()}}, "/test-fire/media",
                     request_id=request_id, caller="test-fire")
    try:
        # the job tag on this row lets the pin through the worker's sequester
        with bound_call(call_row):
            worker = pick(model_key, pin=job.worker_id, source="test-fire")
        worker_name = worker.get("name")
        route, params = adapter["request"](item["spec"], max_tokens)
        params.update(model=model_key, model_key=model_key, request_id=request_id,
                      task="image-to-text" if route == "/infer/stream" else "text-to-image",
                      metadata={**job.call_metadata(), **_item_metadata(), "parent_request_id": request_id})
        call_row.update(task=params["task"], request_body=params, endpoint=route,
                        worker=worker_name, forwarded_at=time.time())
        write(call_row)
        if route == "/infer/stream":
            chunks, error, usage = [], None, None
            payload = worker_payload(params, worker)
            for event in worker_stream(worker, payload):        # waits as long as the queue needs, like any call
                execution_id = event.get("execution_request_id") or execution_id
                if event.get("type") == "token":
                    chunks.append(event.get("text") or "")
                elif event.get("type") == "error":
                    error = event.get("message") or "Worker error"
                elif event.get("type") == "done":
                    usage = event.get("usage")
            if error:
                raise RuntimeError(error)
            payload = {"text": "".join(chunks), "usage": usage}
        else:
            req = urllib.request.Request(worker["url"].rstrip("/") + route,
                data=json.dumps(params).encode(), method="POST",
                headers={"Content-Type": "application/json", "X-Task": params["task"],
                         "X-Hugpy-Parent-Request-Id": request_id})
            with urllib.request.urlopen(req, timeout=1800) as response:
                payload = json.load(response)
                execution_id = response.headers.get("X-Hugpy-Execution-Request-Id") or (payload.get("hugpy") or {}).get("request_id")
            if payload.get("error") or payload.get("ok") is False:
                raise RuntimeError(str(payload.get("error") or "Media generation failed"))
        graded = adapter["response"](payload)
        text = str(graded.get("output") or "")
        call_row["response_meta"] = {"execution_request_id": execution_id}
        finish(call_row)
        return {"ok": True, "model_key": model_key, "worker": worker_name,
                "request_id": execution_id or request_id, "client_request_id": request_id,
                "execution_request_id": execution_id, "text": text, "content80": text[:80],
                "_grade_response": graded, "started": started, "latency_s": round(time.time()-started, 3)}
    except Exception as exc:
        finish(call_row, 502, f"{type(exc).__name__}: {exc}")
        return {"ok": False, "model_key": model_key, "worker": worker_name,
                "request_id": request_id, "error": f"{type(exc).__name__}: {exc}",
                "started": started, "latency_s": round(time.time()-started, 3)}


def _tok_per_s(timings, tokens, latency_s) -> Optional[float]:
    if isinstance(timings, dict):
        call = timings.get("call")
        if isinstance(call, dict) and call.get("tok_per_s") is not None:
            try:
                return round(float(call["tok_per_s"]), 2)
            except (TypeError, ValueError):
                pass
        if timings.get("predicted_per_second") is not None:
            try:
                return round(float(timings["predicted_per_second"]), 2)
            except (TypeError, ValueError):
                pass
    if tokens and latency_s and latency_s > 0:
        try:
            return round(float(tokens) / float(latency_s), 2)
        except (TypeError, ValueError):
            pass
    return None


# ── registry ─────────────────────────────────────────────────────────────────
_JOBS: "OrderedDict[str, TestFireJob]" = OrderedDict()
_BY_WORKER: dict = {}
_REG_LOCK = threading.Lock()


def _running_job_for(worker_id: str) -> Optional[TestFireJob]:
    with _REG_LOCK:
        jid = _BY_WORKER.get(worker_id)
        job = _JOBS.get(jid) if jid else None
    if job is not None and (job.running or (job.thread is not None and job.thread.is_alive())):
        return job
    return None


def _latest_job_for(worker_id: str) -> Optional[TestFireJob]:
    with _REG_LOCK:
        jid = _BY_WORKER.get(worker_id)
        return _JOBS.get(jid) if jid else None


def _register(job: TestFireJob) -> None:
    with _REG_LOCK:
        _JOBS[job.job_id] = job
        _BY_WORKER[job.worker_id] = job.job_id
        # Drop the oldest FINISHED jobs beyond the retention window.
        finished = [j for j in _JOBS.values() if not j.running and j.thread is not None
                    and not j.thread.is_alive()]
        while len(_JOBS) > MAX_FINISHED and finished:
            old = finished.pop(0)
            if _BY_WORKER.get(old.worker_id) == old.job_id and old.job_id != job.job_id:
                # keep the worker's pointer only while it points at a live job
                _BY_WORKER.pop(old.worker_id, None)
            _JOBS.pop(old.job_id, None)


def start_job(worker_id: str, worker_name: str, models: list, *, rounds=1,
              max_tokens=DEFAULT_MAX_TOKENS, seed=None,
              skipped=None, call_fn: Callable[..., dict] = fire_one,
              spawn: bool = True, first_order=None, resumed_from=None, grade=True) -> TestFireJob:
    """Create + register + (by default) spawn the run thread. ``spawn=False``
    leaves the job registered but not started (tests drive ``run_job``).

    Registration sequesters the worker in routing BEFORE the first call, so no
    other traffic slips in during the gap; ``run_job`` releases it when done."""
    job = TestFireJob(worker_id, worker_name, models, rounds=rounds,
                      max_tokens=max_tokens, seed=seed,
                      skipped=skipped, first_order=first_order, resumed_from=resumed_from,
                      grade=grade)
    _register(job)
    from hugpy_core.relay.pick import sequester
    sequester(worker_id, job.job_id)
    if spawn:
        job.running = True   # visible as running before the thread's first tick
        job.thread = threading.Thread(target=run_job, args=(job, call_fn),
                                      name=f"test-fire-{job.job_id}", daemon=True)
        job.thread.start()
    return job


def reset_registry() -> None:
    """Tests only."""
    with _REG_LOCK:
        _JOBS.clear()
        _BY_WORKER.clear()


# ── collaborators (module attrs so tests can fake them in place) ─────────────
def _get_worker(worker_id: str) -> Optional[dict]:
    from hugpy_core.registry import registry
    return registry.lookup_worker(worker_id)


def _catalog() -> dict:
    from hugpy_core.web.routes import catalog_rows
    return {r["model_key"]: r for r in catalog_rows()}


def _blocked_keys() -> set:
    return set()


def _archived_keys() -> set:
    return set()


# ── body validation ──────────────────────────────────────────────────────────
def _int_field(body: dict, name: str, default: int, lo: int, hi: int) -> int:
    v = body.get(name, default)
    if v is None:
        return default
    if isinstance(v, bool) or not isinstance(v, (int, float, str)):
        raise ValueError(f"{name} must be an integer")
    try:
        iv = int(v)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be an integer")
    if iv < lo or iv > hi:
        raise ValueError(f"{name} must be between {lo} and {hi}")
    return iv


def parse_start_body(body) -> dict:
    """{rounds, max_tokens, seed, grade, worker_drive_only} with defaults + bounds.
    The test fire makes NO concurrency decision (operator 2026-11-16: "all testfire
    should have to do is make all calls in sequential order and the job should take
    care of itself" — the Wrapper's queue plans concurrency). A run uses the models
    already on the worker's own drives, so no call waits on a copy."""
    body = body if isinstance(body, dict) else {}
    out = {
        "rounds": _int_field(body, "rounds", 1, 0, MAX_ROUNDS),
        "max_tokens": _int_field(body, "max_tokens", DEFAULT_MAX_TOKENS, 1, MAX_MAX_TOKENS),
        "seed": None,
        "grade": body.get("grade", True),
        "worker_drive_only": body.get("worker_drive_only", True),
    }
    if not isinstance(out["worker_drive_only"], bool):
        raise ValueError("worker_drive_only must be a boolean")
    if not isinstance(out["grade"], bool):
        raise ValueError("grade must be a boolean")
    if body.get("seed") is not None:
        out["seed"] = _int_field(body, "seed", 0, -(2 ** 31), 2 ** 31 - 1)
    return out


# The console's worker-ID test-fire URLs (POST /fleet/workers/<worker_id>/test-fire
# → 202, GET .../<job_id>, .../stop, …) now live in ``testfire/routes.py``'s
# category tree with their exact status codes, so there is ONE source for them.
# ``test_fire_bp`` is kept defined (``hugpy_core.routes`` still imports it) but
# registers no routes — an intentional no-op blueprint.

__all__ = [
    "test_fire_bp", "TEXT_GEN_TASKS", "NON_TEXT_TASKS", "PROMPTS",
    "is_text_gen", "model_tasks", "worker_model_keys", "select_text_gen_models",
    "adapter_base_on_worker", "unserveable_reason",
    "classify_error", "TestFireJob", "run_job", "fire_one", "start_job",
    "parse_start_body", "reset_registry",
]

