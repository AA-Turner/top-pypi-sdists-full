"""Durable timer wiring for ``flow.sleep`` / ``flow.wait_until``.

The node parks the run (INTERRUPTED, marker in the interrupt payload); THIS
module turns that park into a wake that survives anything: a ``workflow.job``
``resume`` row with ``visible_at = wake_at``. Postgres is the clock — the
always-on worker's ordinary claim poll fires the resume when the deadline
passes (``claim_one`` only sees rows whose ``visible_at`` has arrived), so no
new schedule, sweeper, or in-process timer exists.

Called from the ONE ``RunStore.apply_result`` INTERRUPTED branch, which every
execution lane (inline detached start/resume + queued worker) already funnels
through. Exactly-once posture:

* one park → one job row; the enqueue happens once, at park time;
* at wake, the host worker admits the job through
  ``RunStore.claim_for_resume(run_id, from_statuses=("interrupted",))`` — the
  same CAS the HTTP resume route uses, so a person resuming early ALWAYS wins
  and the late wake becomes a logged no-op;
* a worker killed mid-wake is recovered by the queue's lease reaper, and the
  replayed resume is idempotent through recorded outcomes — the same
  chaos-tested path every queued resume rides.

A failure to enqueue the wake is SCREAMED (the run would otherwise sleep
forever) but never raises: the park itself already happened, and the run
remains manually resumable from the studio like any interrupted run.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

log = logging.getLogger("matrx_graph.workers.sleep_wake")

# Import indirection: nodes.flow.sleep owns the marker (the node writes it);
# re-exported here so host code (worker admission) needs only the workers
# namespace.
from matrx_graph.nodes.flow.sleep import SLEEP_MARKER  # noqa: E402

__all__ = ["SLEEP_MARKER", "sleep_marker_of", "schedule_sleep_wake"]


def sleep_marker_of(interrupt: dict[str, Any] | None) -> dict[str, Any] | None:
    """The ``matrx_sleep`` block, from either interrupt shape.

    ``workflow.run.interrupt_payload`` carries the ``{"node_id": …,
    "payload": …}`` envelope; ``workflow.checkpoint.interrupt_payload`` is the
    node payload itself. Accept both — same posture as the decision sweeper.
    """
    if not isinstance(interrupt, dict):
        return None
    inner = interrupt.get("payload")
    payload = inner if isinstance(inner, dict) else interrupt
    marker = payload.get(SLEEP_MARKER)
    return marker if isinstance(marker, dict) else None


def _wake_at_of(marker: dict[str, Any]) -> datetime | None:
    raw = marker.get("wake_at")
    if not isinstance(raw, str) or not raw:
        return None
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


async def schedule_sleep_wake(
    run_id: str,
    interrupt: dict[str, Any] | None,
    *,
    last_checkpoint_id: str | None = None,
) -> str | None:
    """Enqueue the durable wake for a sleep park. Returns the job_id, or None
    when the interrupt is not a sleep (the overwhelmingly common case) or the
    wake could not be scheduled (screamed, never raised)."""
    marker = sleep_marker_of(interrupt)
    if marker is None:
        return None
    try:
        wake_at = _wake_at_of(marker)
        if wake_at is None:
            log.error(
                "[sleep-wake:%s] sleep marker has no parseable wake_at (%r) — "
                "NO wake scheduled; the run stays interrupted until someone "
                "resumes it manually.",
                run_id[:8],
                marker.get("wake_at"),
            )
            return None

        checkpoint_id = await _interrupt_checkpoint_id(run_id, last_checkpoint_id, interrupt)
        if checkpoint_id is None:
            log.error(
                "[sleep-wake:%s] no interrupt checkpoint found — cannot wake "
                "what cannot be resumed; the run stays interrupted until "
                "someone resumes it manually.",
                run_id[:8],
            )
            return None

        payload = interrupt.get("payload") if isinstance(interrupt, dict) else None
        payload = payload if isinstance(payload, dict) else (interrupt or {})
        resume_output = payload.get("resume_output")
        resume_value = resume_output if isinstance(resume_output, dict) else {}

        from matrx_graph.workers.queue import enqueue

        job_id = await enqueue(
            run_id=run_id,
            kind="resume",
            checkpoint_id=checkpoint_id,
            resume_value=resume_value,
            visible_at=wake_at,
        )
        log.info(
            "[sleep-wake:%s] wake scheduled: job=%s checkpoint=%s wake_at=%s",
            run_id[:8],
            job_id,
            checkpoint_id[:8],
            wake_at.isoformat(),
        )
        return job_id
    except Exception:  # noqa: BLE001 — the park already happened; scream, never raise
        log.exception(
            "[sleep-wake:%s] FAILED to schedule the wake job — the run will "
            "sleep past its deadline until resumed manually. Fix the queue "
            "and resume the run from the studio.",
            run_id[:8],
        )
        return None


async def _interrupt_checkpoint_id(
    run_id: str, last_checkpoint_id: str | None, interrupt: dict[str, Any] | None = None
) -> str | None:
    """The checkpoint the run parked on: the caller's pointer, else the one the
    interrupt itself names, else the newest interrupt checkpoint.

    A polling park (``re_execute``) re-runs the SAME node at the SAME step on
    every wake, so each park writes a new interrupt checkpoint with an equal
    ``step``; ordering by step alone picked the previous park, whose resume the
    run then refused as stale — the wake was spent and nothing re-parked
    (live 2026-10-25, knowledge buckets ``batch.wait_for_units``: the second
    wake went to the first park's checkpoint and the run slept forever)."""
    from matrx_graph.db._registry import get_model

    if last_checkpoint_id:
        return str(UUID(str(last_checkpoint_id)))
    named = interrupt.get("checkpoint_id") if isinstance(interrupt, dict) else None
    if isinstance(named, str) and named:
        return str(UUID(named))
    rows = await (
        get_model("WfCheckpoint")
        .filter(run_id=str(UUID(run_id)), deleted_at=None)
        .exclude(interrupt_payload=None)
        .order_by("-step", "-created_at")
        .limit(1)
        .values("id")
    )
    return str(rows[0]["id"]) if rows else None
