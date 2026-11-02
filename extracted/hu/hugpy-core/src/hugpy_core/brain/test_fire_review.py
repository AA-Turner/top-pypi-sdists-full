"""Durable, deferred brain review of models that never served in a test fire."""
from __future__ import annotations

import logging
import threading
import time

from psycopg.types.json import Jsonb

from hugpy_core.help import help_store

logger = logging.getLogger(__name__)
KIND = "test-fire-review"
TRANSIENT_KINDS = {"fit_failure", "capacity", "worker_busy", "model_busy",
                   "requested_worker", "context_overflow"}
TRANSIENT_TEXT = ("does not fit", "won't fit", "cannot fit", "admission cap",
                  "insufficient memory", "not enough memory", "loading model",
                  "worker_busy", "model_busy")
_wake = threading.Event()
_started = False
_lock = threading.Lock()


def queue(job) -> int:
    """Persist one review per model with failed calls and no successful call."""
    failures = [(key, pm) for key, pm in job.snapshot()["summary"]["per_model"].items()
                if pm.get("failed") and not pm.get("ok") and pm.get("last_error")
                and not pm.get("last_interrupted")
                and pm.get("last_error_kind") not in TRANSIENT_KINDS
                and not any(marker in str(pm["last_error"]).lower() for marker in TRANSIENT_TEXT)]
    if not failures:
        job.brain_review = {"status": "none", "queued": 0, "reviewed": 0}
        return 0
    now = time.time()
    queued = 0
    covered = 0
    with help_store._db() as conn:
        for key, pm in failures:
            existing = conn.execute(
                "SELECT id FROM help_tickets WHERE kind=%s AND model_key=%s "
                "AND detail->>'job_id'=%s LIMIT 1", (KIND, key, job.job_id)).fetchone()
            if existing:
                continue
            # Resident load-error events already go through the brain. Keep their
            # ticket and avoid asking the same brain model again for this run.
            prior = conn.execute(
                "SELECT id FROM help_tickets WHERE kind='load-failure' AND status='pending' "
                "AND model_key=%s AND worker_name=%s "
                "AND (updated >= %s OR detail->>'error'=%s) LIMIT 1",
                (key, job.worker_name, job.started or job.created,
                 str(pm["last_error"])[:20000])).fetchone()
            if prior:
                covered += 1
                continue
            detail = {"job_id": job.job_id, "job_started": job.started or job.created,
                      "error": str(pm["last_error"])[:20000],
                      "error_kind": pm.get("last_error_kind"), "failed_calls": pm["failed"]}
            conn.execute("INSERT INTO help_tickets (kind,status,created,updated,model_key,"
                         "worker_id,worker_name,title,detail) VALUES (%s,'queued',%s,%s,%s,%s,%s,%s,%s)",
                         (KIND, now, now, key, job.worker_id, job.worker_name,
                          f"Brain review queued: {key} on {job.worker_name}", Jsonb(detail)))
            queued += 1
    job.brain_review = {"status": "queued" if queued else "covered", "queued": queued,
                        "reviewed": 0, "covered": covered}
    if queued:
        _wake.set()
    return queued


def _active(worker_id: str) -> bool:
    from hugpy_core.testfire import testfire
    job = testfire._running_job_for(worker_id)
    return bool(job and job.running)


def _update_live(job_id: str, *, reviewed: bool = False) -> None:
    from hugpy_core.testfire import testfire
    with testfire._REG_LOCK:
        job = testfire._JOBS.get(job_id)
    if job is None:
        return
    view = dict(job.brain_review)
    if reviewed:
        view["reviewed"] = view.get("reviewed", 0) + 1
    view["status"] = "done" if view.get("reviewed", 0) >= view.get("queued", 0) else "reviewing"
    job.brain_review = view


def drain() -> int:
    """Claim due reviews. A busy test worker is left queued for the next pass."""
    from hugpy_core.brain import brain
    now = time.time()
    with help_store._db() as conn:
        conn.execute("UPDATE help_tickets SET status='queued' WHERE kind=%s "
                     "AND status='reviewing' AND updated<%s", (KIND, now - 600))
        rows = conn.execute(
            "SELECT id, model_key, worker_id, worker_name, detail FROM help_tickets "
            "WHERE kind=%s AND status='queued' "
            "AND coalesce((detail->>'retry_after')::double precision,0)<=%s "
            "ORDER BY created LIMIT 100", (KIND, now)).fetchall()
    reviewed = 0
    for row in rows:
        if _active(row["worker_id"]):
            continue
        with help_store._db() as conn:
            claimed = conn.execute("UPDATE help_tickets SET status='reviewing',updated=%s "
                                   "WHERE id=%s AND status='queued' RETURNING id",
                                   (time.time(), row["id"])).fetchone()
        if not claimed:
            continue
        detail = dict(row["detail"] or {})
        try:
            with help_store._db() as conn:
                prior = conn.execute(
                    "SELECT id FROM help_tickets WHERE kind='load-failure' AND status='pending' "
                    "AND model_key=%s AND worker_name=%s "
                    "AND (updated >= %s OR detail->>'error'=%s) LIMIT 1",
                    (row["model_key"], row["worker_name"], detail["job_started"],
                     detail["error"])).fetchone()
            own_ticket = (detail.get("evaluation") or {}).get("ticket_id")
            if prior and prior["id"] != own_ticket:
                detail["covered_by_ticket"] = prior["id"]
                with help_store._db() as conn:
                    conn.execute("UPDATE help_tickets SET status='acted',detail=%s,updated=%s WHERE id=%s",
                                 (Jsonb(detail), time.time(), row["id"]))
                reviewed += 1
                _update_live(detail["job_id"], reviewed=True)
                continue
            verdict = brain.evaluate_and_file(detail["error"], worker=row["worker_name"],
                                              model_key=row["model_key"])
            completed = bool(verdict.get("ticket_id")) and not verdict.get("brain_error")
            detail.update(evaluation=verdict, retry_after=0 if completed else time.time() + 3600)
            with help_store._db() as conn:
                conn.execute("UPDATE help_tickets SET status=%s,detail=%s,updated=%s WHERE id=%s",
                             ("acted" if completed else "queued", Jsonb(detail), time.time(), row["id"]))
            if completed:
                reviewed += 1
                _update_live(detail["job_id"], reviewed=True)
        except Exception as exc:  # noqa: BLE001 — keep the work for a later retry
            logger.exception("test-fire brain review %s failed", row["id"])
            detail.update(review_error=str(exc)[:300], retry_after=time.time() + 3600)
            with help_store._db() as conn:
                conn.execute("UPDATE help_tickets SET status='queued',detail=%s,updated=%s WHERE id=%s",
                             (Jsonb(detail), time.time(), row["id"]))
    return reviewed


def _loop() -> None:
    while True:
        _wake.wait(60)
        _wake.clear()
        try:
            drain()
        except Exception:  # noqa: BLE001 — a DB outage must not kill the queue worker
            logger.exception("test-fire brain queue drain failed")


def ensure() -> None:
    global _started
    with _lock:
        if _started:
            return
        _started = True
    try:
        # A process can die after claiming a review; return only stale claims.
        with help_store._db() as conn:
            conn.execute("UPDATE help_tickets SET status='queued' WHERE kind=%s "
                         "AND status='reviewing' AND updated<%s", (KIND, time.time() - 600))
    except Exception:
        logger.exception("test-fire brain review recovery failed")
    threading.Thread(target=_loop, name="test-fire-brain-review", daemon=True).start()
    _wake.set()  # recover queued reviews after a Core restart
