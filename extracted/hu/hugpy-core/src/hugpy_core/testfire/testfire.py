# LIFTED from legacy hugpy (read-only reference):
#   py/services/hugpy_server/src/hugpy_server/app/routes/test_fire_routes.py
#   — selection, error classification, TestFireJob, run_job, _guarded_call,
#   _tok_per_s, the job registry, body parsing and every route: VERBATIM.
# SWAPPED: fire_one (the in-process /v1 intake -> hugpy_core pick + worker_stream,
#   pinned to the job's worker), _get_worker (registry), _catalog (routes.catalog_rows:
#   discovery + hugpy.json over the DB rows), _cancel_request (relay.worker_cancel).
# SWAPPED: persisted history = hugpy_core.test_fire_store (run metadata in
#   test_fire_runs, per-call results read from the call log).
# DROPPED: blocked/archived sets are empty.
"""Per-worker TEST FIRE: complete cumulative grading by default.

With grade=false, run the original random smoke-call rounds.

Operator ask (2026-09-29): "a test button where it starts to randomly call
every model on that worker which does text gen". One background job per worker
walks that worker's text-generation models in a fresh random order each round
and sends each one a tiny prompt through the NORMAL /v1 intake — the same
``_completion_kwargs`` + ``_v1_events`` path an OpenAI client (and the
fire_keys.py harness) hits — with the request pinned to the worker via the
existing ``alloc.worker`` steer, so placement resolves to that box or fails
naming why (never silently reroutes).

Routes (bare and under /api, like the rest of the worker surface):

    POST /fleet/workers/<id>/test-fire                    {rounds?, concurrency?, max_tokens?, seed?}
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
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
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
MAX_CONCURRENCY = 8
MAX_ROUNDS = 1000


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
                 rounds: int = 1, concurrency: int = 1,
                 max_tokens: int = DEFAULT_MAX_TOKENS, seed: Optional[int] = None,
                 skipped: Optional[list] = None, first_order: Optional[list] = None,
                 resumed_from: Optional[str] = None, grade: bool = True,
                 chaos: bool = False, storage_managed: bool = False):
        self.job_id = uuid.uuid4().hex[:12]
        self.storage_managed = bool(storage_managed and grade)
        self.storage = {}
        self.station_lease = None
        self.grade = bool(grade)   # complete the remaining cumulative curriculum
        self.grading = {}
        self.grading_planned = None
        self.worker_id = worker_id
        self.worker_name = worker_name
        self.model_tasks = {m["model_key"]: m.get("tasks", []) for m in models if isinstance(m, dict)}
        self.models = [m["model_key"] if isinstance(m, dict) else str(m) for m in models]
        self.rounds = int(rounds)            # 0 = until stopped
        self.concurrency = int(concurrency)
        self.chaos = bool(chaos)
        self.concurrency_current = 0 if self.chaos else self.concurrency
        self.concurrency_changes = 0
        self.concurrency_history = []
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

    def call_metadata(self):
        """The submitted run options travel on its calls, not a run side table."""
        from hugpy_core.brain.intent import GRADING, SMOKE_TEST
        return {"intent": GRADING if self.grade else SMOKE_TEST,
                "test_fire": {"job_id": self.job_id, "worker_id": self.worker_id, "models": self.models,
                "rounds": self.rounds, "concurrency": self.concurrency,
                "concurrency_current": self.concurrency_current,
                "max_tokens": self.max_tokens, "grade": self.grade,
                "chaos": self.chaos, "storage_managed": self.storage_managed,
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
            "concurrency": self.concurrency,
            "chaos": self.chaos,
            "concurrency_current": self.concurrency_current,
                "concurrency_changes": self.concurrency_changes,
            "concurrency_history": list(self.concurrency_history[-32:]),
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
            "storage": dict(self.storage), "storage_managed": self.storage_managed,
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
            _run_grading(job, call_fn)
            return
        if job.chaos:
            _run_chaos_smoke(job, call_fn, prompts, rng)
            return
        with ThreadPoolExecutor(max_workers=max(1, job.concurrency)) as pool:
            while not job.stop_requested():
                if job.rounds and job.round >= job.rounds:
                    break
                job.round += 1
                if job.round == 1 and job.first_order:
                    order = list(job.first_order)
                else:
                    order = list(job.models)
                    rng.shuffle(order)
                pending = []
                for key in order:
                    if job.stop_requested():
                        break
                    prompt, item = rng.choice(prompts), None
                    fut = pool.submit(_test_call, call_fn, key, prompt, job)
                    pending.append(fut)
                    # concurrency=1 degenerates to strictly sequential calls so
                    # a warm slot is never piled on (worker_busy contract).
                    if len(pending) >= max(1, job.concurrency):
                        pending.pop(0).result()
                for fut in pending:
                    fut.result()
    except Exception as exc:  # noqa: BLE001 — the loop must always finish
        logger.exception("test-fire %s: run loop failed", job.job_id)
        job.request_stop(f"loop error: {type(exc).__name__}: {exc}")
    finally:
        job.running = False
        job.finished = time.time()
        if job.stop_reason is None:
            job.stop_reason = "complete"
        _persist("save_run", job)
        if os.environ.get("HUGPY_TEST_FIRE_BRAIN", "1").strip().lower() not in ("0", "false", "off", "no"):
            try:
                from hugpy_core.brain import test_fire_review
                test_fire_review.queue(job)
            except Exception:  # noqa: BLE001 — review must not change the run result
                logger.exception("test-fire %s: queueing brain review failed", job.job_id)


def _run_grading(job: TestFireJob, call_fn) -> None:
    """Drain unfinished curriculum per model; preserve grades and stop on faults.

    Round limits belong to random smoke calls. Grading is complete only when
    the persistent curriculum has no unanswered items. A transport/store fault
    leaves the model incomplete for a later resume, without an endless retry.
    """
    from hugpy_core.grading import grader
    order = list(dict.fromkeys((job.first_order or []) + job.models))
    progress = {}
    catalog = _catalog() if any(not job.model_tasks.get(key) for key in order) else {}
    for key in order:
        if job.stop_requested():
            return
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

    if job.chaos and not job.storage_managed:
        _run_chaos_grading(job, order, progress, grader, call_fn)
        return

    def complete_model(key):
        state = job.grading[key]
        attempted = set()
        try:
            while not job.stop_requested():
                with grader.test_turn(key):
                    item = next((pending for suite in state["suites"]
                                 if (pending := grader.next_item(key, suite)) is not None), None)
                    if item is None:
                        state.update(status="complete", remaining=0)
                        return
                    identity = (item["suite"], item["category"], item["tier"])
                    if identity in attempted:
                        state.update(status="incomplete", error="Saved grade is not visible; resume to retry")
                        return
                    attempted.add(identity)
                    # a stop must prevent any FURTHER item from being dispatched; the
                    # in-flight item (if any) is marked stopped by _guarded_call.
                    if job.stop_requested():
                        state.update(status="interrupted")
                        return
                    state.update(status="grading", suite=item["suite"], category=item["category"], tier=item["tier"])
                    result = _guarded_call(call_fn, key, item["prompt"], job, item)
                verdict = result.get("grade") or {}
                if result.get("interrupted"):
                    state.update(status="interrupted",
                                 error=(verdict.get("why") or result.get("interrupted_why")
                                        or "interrupted by unload/cancel"))
                    return
                if verdict.get("passed") is None:
                    state.update(status="incomplete", error=result.get("grading_error") or
                                 result.get("error") or "No grade was recorded; resume to retry")
                    return
                state["graded_this_run"] += 1
                state["remaining"] = sum(len(grader.pending_items(key, suite)) for suite in state["suites"])
            state["status"] = "interrupted"
        except Exception as exc:
            logger.exception("test-fire %s: grading failed for %s", job.job_id, key)
            state.update(status="incomplete", error=f"{type(exc).__name__}: {exc}")

    if job.storage_managed:
        if not any(row["remaining"] for row in progress.values()):
            job.stop_reason = "complete"
            job.storage = {"phase":"not-needed","events":[],"errors":[]}
            return
        from .storage_cycle import StorageCycle
        cycle = StorageCycle(job)
        restored = False
        try:
            cycle.begin(progress)
            pending = [k for k in order if progress[k]['remaining'] > 0]
            while pending and not job.stop_requested():
                window = cycle.fill(pending)
                ready = window['ready']
                for key,why in window['errors'].items():
                    progress[key].update(status='incomplete',error=why)
                    pending.remove(key)
                if job.stop_requested():
                    break
                if not ready:
                    for key in pending:
                        progress[key].update(status='incomplete',error='No worker drive room remains after reclaiming completed models')
                    break
                if job.chaos:
                    _run_chaos_grading(job,ready,progress,grader,call_fn)
                else:
                    for key in ready:
                        if job.stop_requested():
                            break
                        complete_model(key)
                for key in ready:
                    if progress[key]['status'] == 'complete':
                        try:
                            cycle.complete(key)
                        except Exception as exc:
                            progress[key]['reap_note'] = str(exc)
                    pending.remove(key)
        finally:
            restored = cycle.restore()
        if not restored:
            job.stop_reason = 'snapshot restoration incomplete'
        elif not job.stop_requested():
            job.stop_reason = 'complete' if all(r['status'] == 'complete' for r in progress.values()) else 'grading incomplete'
        return

    with ThreadPoolExecutor(max_workers=max(1, job.concurrency)) as pool:
        pending = []
        for key in order:
            if job.stop_requested():
                break
            if job.grading[key]["remaining"] == 0:
                continue
            pending.append(pool.submit(complete_model, key))
            if len(pending) >= max(1, job.concurrency):
                pending.pop(0).result()
        for future in pending:
            future.result()
    if not job.stop_requested():
        job.stop_reason = ("complete" if all(row["status"] == "complete" for row in job.grading.values())
                           else "grading incomplete")


def _run_chaos_grading(job: TestFireJob, order: list, progress: dict, grader, call_fn) -> None:
    """Grade one item per scheduled model at a time, varying call concurrency."""
    attempted = {key: set() for key in order}

    def grade_one(key):
        state = progress[key]
        try:
            with grader.test_turn(key):
                item = next((pending for suite in state["suites"]
                             if (pending := grader.next_item(key, suite)) is not None), None)
                if item is None:
                    state.update(status="complete", remaining=0)
                    return key
                identity = (item["suite"], item["category"], item["tier"])
                if identity in attempted[key]:
                    state.update(status="incomplete", error="Saved grade is not visible; resume to retry")
                    return key
                attempted[key].add(identity)
                if job.stop_requested():
                    state.update(status="interrupted")
                    return key
                state.update(status="grading", suite=item["suite"], category=item["category"], tier=item["tier"])
                result = _guarded_call(call_fn, key, item["prompt"], job, item)
            verdict = result.get("grade") or {}
            if result.get("interrupted"):
                state.update(status="interrupted",
                             error=(verdict.get("why") or result.get("interrupted_why")
                                    or "interrupted by unload/cancel"))
                return key
            if verdict.get("passed") is None:
                state.update(status="incomplete", error=result.get("grading_error") or
                             result.get("error") or "No grade was recorded; resume to retry")
                return key
            state["graded_this_run"] += 1
            state["remaining"] = sum(len(grader.pending_items(key, suite)) for suite in state["suites"])
            state.update(status="pending" if state["remaining"] else "complete")
        except Exception as exc:
            logger.exception("test-fire %s: chaos grading failed for %s", job.job_id, key)
            state.update(status="incomplete", error=f"{type(exc).__name__}: {exc}")
        return key

    pending = deque(key for key in order if progress[key]["remaining"] > 0)
    if not pending:
        job.stop_reason = "complete"
        return
    with ThreadPoolExecutor(max_workers=max(1, job.concurrency)) as pool:
        active = {}
        rng = random.Random(job.seed)
        cap = _change_chaos_cap(job, rng)

        def dispatch():
            while pending and len(active) < cap and not job.stop_requested():
                key = pending.popleft()
                active[pool.submit(grade_one, key)] = key

        dispatch()
        while active:
            done, _ = wait(active, return_when=FIRST_COMPLETED)
            for future in done:
                active.pop(future, None)
                key = future.result()
                if job.stop_requested():
                    continue
                if progress[key]["status"] == "pending" and progress[key]["remaining"] > 0:
                    pending.append(key)
                cap = _change_chaos_cap(job, rng)
                dispatch()
    if job.stop_requested():
        for state in progress.values():
            if state["status"] == "grading":
                state["status"] = "interrupted"
        return
    job.stop_reason = ("complete" if all(row["status"] == "complete" for row in progress.values())
                       else "grading incomplete")


def _change_chaos_cap(job: TestFireJob, rng: random.Random) -> int:
    """Pick a new cap in [1, configured max], changing it at every transition."""
    maximum = max(1, int(job.concurrency))
    current = int(job.concurrency_current)
    if current < 1 or current > maximum:
        cap = rng.randint(1, maximum)
        with job._lock:
            job.concurrency_current = cap
            job.concurrency_changes += 1
            job.concurrency_history.append(cap)
            del job.concurrency_history[:-32]
        return cap
    choices = [cap for cap in range(1, maximum + 1) if cap != current]
    cap = rng.choice(choices) if choices else 1
    with job._lock:
        job.concurrency_current = cap
        job.concurrency_changes += 1
        job.concurrency_history.append(cap)
        del job.concurrency_history[:-32]
    return cap


def _run_chaos_smoke(job: TestFireJob, call_fn, prompts: tuple, rng: random.Random) -> None:
    """Run normal smoke rounds while changing the dispatch cap after each call."""
    max_workers = max(1, job.concurrency)
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        while not job.stop_requested():
            if job.rounds and job.round >= job.rounds:
                break
            job.round += 1
            if job.round == 1 and job.first_order:
                order = list(job.first_order)
            else:
                order = list(job.models)
                rng.shuffle(order)
            pending = deque((key, rng.choice(prompts)) for key in order)
            active = {}
            cap = _change_chaos_cap(job, rng)

            def dispatch():
                while pending and len(active) < cap and not job.stop_requested():
                    key, prompt = pending.popleft()
                    active[pool.submit(_test_call, call_fn, key, prompt, job)] = key

            dispatch()
            while active:
                done, _ = wait(active, return_when=FIRST_COMPLETED)
                completed = []
                for future in done:
                    active.pop(future, None)
                    future.result()
                    completed.append(future)
                if job.stop_requested():
                    continue
                for _ in completed:
                    cap = _change_chaos_cap(job, rng)
                    dispatch()


_ITEM: contextvars.ContextVar = contextvars.ContextVar("test_fire_item", default=None)


def _item_metadata() -> dict:
    """The curriculum item the current call asks, carried on the call itself
    (metadata.grade): its grade derives from the call log alone
    (grader.fill_from_call_log), with no test-fire job left to remember it."""
    item = _ITEM.get()
    return {"intent": "grading", "grade": {k: item[k] for k in ("suite", "category", "tier")}} if item else {}


def _test_call(call_fn, key, prompt, job) -> dict:
    """Any test advances one unfinished grade before falling back to smoke."""
    from hugpy_core.grading import grader
    tasks = job.model_tasks.get(key) or model_tasks(_catalog_row(_catalog(), key) or {})
    with grader.test_turn(key):
        if job.stop_requested():
            return {}
        item = next((it for suite in grader.suites_for_tasks(tasks)
                     if (it := grader.next_item(key, suite)) is not None), None)
        return _guarded_call(call_fn, key, item["prompt"] if item else prompt, job, item)


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


# ── the real call: hugpy_core's relay, pinned to the job's worker ───────────
def fire_one(model_key: str, prompt: str, max_tokens: int, job: TestFireJob) -> dict:
    """One tiny completion through hugpy_core's relay (pick with the job's worker
    as the pin, then the worker's /infer/stream), drained like the non-streaming
    route drains it. Result shape is legacy's."""
    from hugpy_core.relay.pick import NoWorker, pick
    from hugpy_core.relay.relay import WorkerHTTPError, worker_payload, worker_stream

    request_id = f"tf-{job.job_id}-{uuid.uuid4().hex[:8]}"
    job.mark_in_flight(request_id, model_key)
    started = time.time()
    text_parts: list = []
    error_message = None
    usage = None
    timings = None
    worker_seen = None
    execution_id = None
    finish_reason = None
    from hugpy_core.calllog.call_record import start, finish, write
    call_body = {"model_key": model_key, "request_id": request_id, "task": "text-generation",
                 "messages": [{"role": "user", "content": prompt}], "max_new_tokens": int(max_tokens),
                 "temperature": 0.0, "metadata": {**job.call_metadata(), **_item_metadata(),
                                                "parent_request_id": request_id}}
    call_row = start(call_body, "/infer/stream", request_id=request_id, caller="test-fire")
    try:
        w = pick(model_key, pin=job.worker_id, source=("test-fire:" + job.job_id if job.storage_managed else "test-fire"))
        worker_seen = w.get("name")
        wp = worker_payload(call_body, w)
        if job.station_lease:
            wp["_station_lease"] = job.station_lease
        call_row.update(forwarded_at=time.time(), worker=worker_seen)
        write(call_row)
        for ev in worker_stream(w, wp, timeout=600):
            execution_id = ev.get("execution_request_id") or execution_id
            t = ev.get("type")
            if t == "token":
                text_parts.append(ev.get("text") or "")
            elif t == "done":
                usage = ev.get("usage")
                timings = ev.get("timings")
                finish_reason = ev.get("finish_reason")
            elif t == "error":
                error_message = ev.get("message") or "error"
                finish_reason = ev.get("finish_reason") or finish_reason
    except (NoWorker, WorkerHTTPError) as exc:
        error_message = str(exc)
    except Exception as exc:  # noqa: BLE001 — a raised relay error is a result, not a crash
        error_message = f"{type(exc).__name__}: {exc}"
    latency = round(time.time() - started, 3)

    content = "".join(text_parts)
    if "[error:" in content and not error_message:
        error_message = content[:2000]
    tokens = usage.get("completion_tokens") if isinstance(usage, dict) else None
    # a thinking model can spend the whole (small) test budget reasoning: the
    # answer text is empty but the model GENERATED tokens — that is a pass
    # a call the box ended by cancel/unload/interrupt (relay maps the worker's
    # finish reason to 'cancelled') is not a completion: it is never a pass on
    # whatever partial text arrived before the cut.
    interrupted = finish_reason == "cancelled"
    ok = error_message is None and not interrupted and (bool(content.strip()) or bool(tokens))
    if interrupted and error_message is None:
        error_message = "interrupted by unload/cancel"
    if not ok and error_message is None:
        error_message = "empty completion (0 tokens generated)"

    tok_s = _tok_per_s(timings, tokens, latency)
    call_row["response_meta"] = {"execution_request_id": execution_id}
    finish(call_row, 200 if ok else 499 if interrupted else 502, error_message)

    return {
        "model_key": model_key,
        "request_id": execution_id or request_id,
        "execution_request_id": execution_id, "client_request_id": request_id,
        "prompt": prompt,
        "started": started,
        "latency_s": latency,
        "ok": ok,
        "interrupted": interrupted,
        "interrupted_why": "interrupted by unload/cancel" if interrupted else None,
        "status": "interrupted" if interrupted else "ok" if ok else "fail",
        "tokens": tokens,
        "tok_s": tok_s,
        "worker": worker_seen,
        "text": content[:20000],
        "content80": content[:80] if content else
                     (f"(reasoning only — {tokens} tokens of thinking hit the {int(max_tokens)}-token test limit)"
                      if ok else None),
        # answered = visible text; reasoning_only = a thinking model spent the
        # whole test budget reasoning (it works — it just did not reach an answer)
        "outcome": ("answered" if (ok and content.strip()) else "reasoning_only" if ok else "fail"),
        "error": None if ok else str(error_message)[:2000],
        "error_kind": None if ok else classify_error(error_message),
    }


def fire_media(model_key: str, item: dict, max_tokens: int, job: TestFireJob) -> dict:
    """Use the installed suite fixture and the platform's actual worker routes."""
    import json
    import urllib.request
    from hugpy_core.grading import grader
    from hugpy_core.relay.pick import pick
    from hugpy_core.relay.relay import worker_payload, worker_stream
    adapter = grader.providers()[item["suite"]]
    request_id = f"tf-{job.job_id}-{uuid.uuid4().hex[:8]}"
    job.mark_in_flight(request_id, model_key)
    started = time.time()
    worker_name = None
    execution_id = None
    from hugpy_core.calllog.call_record import start, finish, write
    call_row = start({"model": model_key, "metadata": {**job.call_metadata(), **_item_metadata()}}, "/test-fire/media",
                     request_id=request_id, caller="test-fire")
    try:
        worker = pick(model_key, pin=job.worker_id, source=("test-fire:" + job.job_id if job.storage_managed else "test-fire"))
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
            if job.station_lease:
                payload["_station_lease"] = job.station_lease
            for event in worker_stream(worker, payload, timeout=600):
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
            lease_headers = {"X-Hugpy-Station-Lease":job.station_lease} if job.station_lease else {}
            req = urllib.request.Request(worker["url"].rstrip("/") + route,
                data=json.dumps(params).encode(), method="POST",
                headers={**lease_headers,"Content-Type": "application/json", "X-Task": params["task"],
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
              concurrency=1, max_tokens=DEFAULT_MAX_TOKENS, seed=None,
              skipped=None, call_fn: Callable[..., dict] = fire_one,
              spawn: bool = True, first_order=None, resumed_from=None, grade=True,
              chaos=False, storage_managed=False) -> TestFireJob:
    """Create + register + (by default) spawn the run thread. ``spawn=False``
    leaves the job registered but not started (tests drive ``run_job``)."""
    job = TestFireJob(worker_id, worker_name, models, rounds=rounds,
                      concurrency=concurrency, max_tokens=max_tokens, seed=seed,
                      skipped=skipped, first_order=first_order, resumed_from=resumed_from,
                      grade=grade, chaos=chaos, storage_managed=storage_managed)
    _register(job)
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


def _cancel_request(request_id: str, reason: str) -> bool:
    try:
        from hugpy_core.registry import registry
        from hugpy_core.relay.relay import worker_cancel
        job_id = request_id.split("-")[1] if request_id.startswith("tf-") else None
        with _REG_LOCK:
            job = _JOBS.get(job_id) if job_id else None
        w = registry.lookup_worker(job.worker_id) if job else None
        if w is None:
            return False
        status, out = worker_cancel(w, request_id)
        return bool((out or {}).get("cancelled"))
    except Exception:  # noqa: BLE001 — best-effort; the loop still stops
        logger.debug("test-fire: cancel %s failed", request_id, exc_info=True)
        return False


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
    """{rounds, concurrency, max_tokens, seed, grade, chaos} with defaults + bounds."""
    body = body if isinstance(body, dict) else {}
    out = {
        "rounds": _int_field(body, "rounds", 1, 0, MAX_ROUNDS),
        "concurrency": _int_field(body, "concurrency", 1, 1, MAX_CONCURRENCY),
        "max_tokens": _int_field(body, "max_tokens", DEFAULT_MAX_TOKENS, 1, MAX_MAX_TOKENS),
        "seed": None,
        "grade": body.get("grade", True),
        "chaos": body.get("chaos", False),
    }
    if not isinstance(out["grade"], bool):
        raise ValueError("grade must be a boolean")
    if not isinstance(out["chaos"], bool):
        raise ValueError("chaos must be a boolean")
    if out["chaos"] and out["concurrency"] < 2:
        raise ValueError("chaos mode requires a concurrency cap of at least 2")
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

