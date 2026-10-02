"""THE CONTINUATION — a run the PROCESS lost continues; it is never failed for it.

A scheduled run can stop for three kinds of reason, and they deserve three
different verdicts:

* **The handler finished, or stopped itself** (a clean lease stop, an error it
  reported) — the normal verdict: ``success`` / ``failed`` by work done.
* **The runner stopped it** (the run ceiling, a lost lease) — ``runner.py``'s
  bounded verdict, progress preserved.
* **The process that held it went away** — a deploy's SIGTERM (``stop_scanner``
  cancels the run) or a hard kill nobody announced (the lease is orphaned and the
  next worker's sweep finds it). The work is not broken and the approval is not
  spent; only the host is gone. That run closes ``interrupted`` and a
  CONTINUATION is queued due now, on the same task, carrying what is left of the
  fire's run ceiling and the units already done.

This is the pattern the best durable-execution systems share: Temporal retries
an activity whose worker stopped heartbeating; Sidekiq pushes an in-flight job
back onto its queue on TERM; Celery with ``acks_late`` redelivers a task whose
worker died. Before 2026-09-14 this scheduler had none of it: the approved
keyword facet backfill (``sch_run e6daa2aa…``) committed 1,593 of its 4,000
approved keywords, lost its worker to a deploy at 05:32 UTC, and was stamped
``failed / lease expired`` at 05:40 with nothing to resume it — the other 2,407
simply did not happen that day.

The contract every task inherits
--------------------------------
* ``interrupted`` is a TERMINAL state that is neither success nor failure. It
  never reaches the failure sink, and the repeat guard skips it: a deploy is not
  evidence that a schedule is broken, and it is not evidence that it works.
* The continuation is an ordinary ``queued`` ``sch_run`` — the scanner's own
  queued-run pass claims it, exactly like "Run now". Its
  ``metadata.continuation`` marker names the run it continues, the fire's first
  run, its index, the units carried, and the seconds of run ceiling left; the
  runner sizes the continuation's lease deadline from that, so a fire never gets
  a fresh full ceiling by being interrupted.
* A handler resumes IDEMPOTENTLY because its durable state is the truth, not the
  run: a queue claim with a stale reclaim, a cursor, a daily ceiling read from
  what landed. The continuation re-derives "what is left" exactly as a fresh fire
  would.
* Continuations per fire are bounded by the knob
  ``scheduler.continuation.max_continuations_per_fire``. Exhausting it is a real
  ``failed`` run whose message names the knob — a fire that keeps losing its
  worker is not going to finish by itself, and a person has to hear it.
* A fire whose run ceiling is already spent is not continued; it closes with the
  runner's bounded verdict (work landed = not failed, the stop named).
"""

from __future__ import annotations

import json
import logging
import uuid
from datetime import UTC, datetime
from typing import Any

from . import queries
from ._ext import get_db_model, get_optional_ext, report_operational_failure
from .models import (
    RUN_CONTINUATION_KEY,
    RUN_INTERRUPTED_STATUS,
    RUN_STOPPED_EARLY_KEY,
    RUN_UNITS_DONE_KEY,
)

log = logging.getLogger("matrx_scheduler.continuation")

#: The knob that bounds continuations per fire.
CONTINUATION_KNOB_FEATURE = "scheduler.continuation"
CONTINUATION_KNOB_KEY = "max_continuations_per_fire"

#: KNOB MIRROR of platform.feature_knob "scheduler.continuation" "max_continuations_per_fire".
#: The package cannot read the host's knob registry, so a host wires the live row
#: through ``configure(continuation_limit=...)``; this is what a bare package
#: (or a host whose resolver fails, loudly) uses. Change the row AND this line
#: together.
MAX_CONTINUATIONS_PER_FIRE = 3

#: What ``interrupt_run`` returns.
VERDICT_CONTINUED = "continued"
VERDICT_EXHAUSTED = "exhausted"
VERDICT_CEILING_SPENT = "ceiling_spent"
VERDICT_LOST = "lost"


def _as_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, str):
        try:
            value = json.loads(value) if value.strip() else {}
        except ValueError:
            return {}
    return dict(value) if isinstance(value, dict) else {}


def continuation_marker(run_metadata: Any) -> dict[str, Any] | None:
    """The ``metadata.continuation`` marker of a run, or None for a first run."""
    marker = _as_dict(run_metadata).get(RUN_CONTINUATION_KEY)
    return dict(marker) if isinstance(marker, dict) else None


def _int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def run_ceiling_seconds(run_metadata: Any, max_runtime_seconds: int) -> int:
    """The run ceiling a claimed run executes under: the schedule's Max runtime,
    or — for a continuation — what is left of its fire's ceiling, whichever is
    smaller. Being interrupted never buys a fire more time than it was given."""
    ceiling = max(1, _int(max_runtime_seconds, 1))
    marker = continuation_marker(run_metadata)
    if marker is None:
        return ceiling
    remaining = _int(marker.get("remaining_runtime_seconds"))
    return max(1, min(ceiling, remaining)) if remaining > 0 else ceiling


async def continuation_limit() -> int:
    """Continuations allowed per fire: the host's knob, else the package mirror.
    A resolver that fails SCREAMS and falls back — an unreadable knob must never
    turn a deploy casualty back into a lost night."""
    resolver = get_optional_ext("continuation_limit")
    if resolver is None:
        return MAX_CONTINUATIONS_PER_FIRE
    try:
        return max(0, int(await resolver()))
    except Exception:  # noqa: BLE001 — fall back loudly, never break finalization
        log.exception(
            "[scheduler-continuation] the %s.%s knob would not resolve; using the package "
            "default %d so an interrupted run still continues. Repair the "
            "platform.feature_knob row.",
            CONTINUATION_KNOB_FEATURE,
            CONTINUATION_KNOB_KEY,
            MAX_CONTINUATIONS_PER_FIRE,
        )
        return MAX_CONTINUATIONS_PER_FIRE


async def interrupt_run(
    *,
    run_id: str,
    claim_token: str,
    reason: str,
    result_metadata: dict[str, Any] | None,
    max_runtime_seconds: int,
    now: datetime | None = None,
) -> str:
    """Close a run whose PROCESS went away, and continue it.

    Every write is gated by ``claim_token`` through ``queries.finalize_run`` (THE
    CHOKEPOINT), so a run another worker already owns — or one its handler
    already finalized — is left alone and nothing is queued (``"lost"``). The
    continuation is inserted only AFTER the interrupted row is terminal, because
    ``sch_run_unique_active_per_task`` allows one active run per task.

    Returns ``"continued"``, ``"exhausted"`` (the knob's cap was reached: closed
    ``failed``), ``"ceiling_spent"`` (nothing left to continue with: closed by the
    bounded verdict), or ``"lost"``.
    """
    now = now or datetime.now(UTC)
    SchRunModel = get_db_model("SchRun")
    rows = await (
        SchRunModel.filter(id=run_id, claim_token=claim_token)
        .limit(1)
        .values("task_id", "trigger_id", "user_id", "organization_id", "queue", "claimed_at", "metadata")
    )
    if not rows:
        return VERDICT_LOST
    row = rows[0]

    meta = _as_dict(result_metadata)
    units = max(0, _int(meta.get(RUN_UNITS_DONE_KEY)))
    meta[RUN_UNITS_DONE_KEY] = units

    marker = continuation_marker(row.get("metadata")) or {}
    index = max(0, _int(marker.get("index")))
    fire_run_id = str(marker.get("fire_run_id") or run_id)
    carried = max(0, _int(marker.get("carried_units_done")))
    ceiling = run_ceiling_seconds(row.get("metadata"), max_runtime_seconds)
    claimed_at = row.get("claimed_at")
    elapsed = (now - claimed_at).total_seconds() if isinstance(claimed_at, datetime) else 0.0
    remaining = int(ceiling - elapsed)
    next_index = index + 1

    if remaining <= 0:
        stop = (
            f"{reason}; the fire's run ceiling ({ceiling}s) is already spent, so there is "
            f"nothing left to continue, after committing {units} unit(s)"
        )
        meta[RUN_STOPPED_EARLY_KEY] = stop
        persisted = await queries.finalize_run(
            run_id,
            claim_token,
            status="success" if units > 0 else "failed",
            result_summary=f"units_done={units} STOPPED_EARLY: {stop}" if units > 0 else None,
            error_message=reason,
            result_metadata=meta,
        )
        return VERDICT_CEILING_SPENT if persisted else VERDICT_LOST

    limit = await continuation_limit()
    if next_index > limit:
        stop = (
            f"{reason}; this fire has now been interrupted {next_index} time(s) and "
            f"{CONTINUATION_KNOB_FEATURE}.{CONTINUATION_KNOB_KEY}={limit} is exhausted. A fire "
            "that keeps losing its worker will not finish by itself: find what keeps killing "
            "the worker, or raise the knob"
        )
        meta[RUN_STOPPED_EARLY_KEY] = f"{stop} (after committing {units} unit(s))"
        persisted = await queries.finalize_run(
            run_id,
            claim_token,
            status="failed",
            error_message=stop,
            result_metadata=meta,
        )
        if persisted:
            log.error("[scheduler-continuation-exhausted] run %s: %s", run_id, stop)
        return VERDICT_EXHAUSTED if persisted else VERDICT_LOST

    meta[RUN_STOPPED_EARLY_KEY] = (
        f"interrupted: {reason} after committing {units} unit(s); continuation "
        f"#{next_index} of {limit} queued with {remaining}s of the run ceiling left"
    )
    persisted = await queries.finalize_run(
        run_id,
        claim_token,
        status=RUN_INTERRUPTED_STATUS,
        result_summary=f"units_done={units} INTERRUPTED: {reason}",
        result_metadata=meta,
    )
    if not persisted:
        return VERDICT_LOST
    await _queue_continuation(
        row,
        run_id=run_id,
        marker={
            "of_run_id": run_id,
            "fire_run_id": fire_run_id,
            "index": next_index,
            "carried_units_done": carried + units,
            "remaining_runtime_seconds": remaining,
            "reason": reason[:500],
            "interrupted_at": now.isoformat(),
        },
        now=now,
    )
    return VERDICT_CONTINUED


async def _queue_continuation(
    row: dict[str, Any], *, run_id: str, marker: dict[str, Any], now: datetime
) -> str | None:
    SchRunModel = get_db_model("SchRun")
    task_id = str(row["task_id"])
    payload: dict[str, Any] = {
        "id": str(uuid.uuid4()),
        "task_id": task_id,
        "trigger_id": row.get("trigger_id"),
        "user_id": row["user_id"],
        "organization_id": row["organization_id"],
        "status": "queued",
        "surface": None,
        "queue": row.get("queue"),
        "due_at": now,
        "metadata": {
            "claim_protocol": queries.CLAIM_PROTOCOL,
            RUN_CONTINUATION_KEY: marker,
        },
    }
    try:
        await SchRunModel.create(**payload)
    except Exception as exc:  # noqa: BLE001 — classified below; never breaks shutdown
        msg = str(exc)
        if "23505" in msg or "sch_run_unique_active_per_task" in msg or "duplicate key" in msg.lower():
            log.warning(
                "[scheduler-continuation] run %s: task %s already has an active run, which "
                "carries the remaining work; no continuation queued",
                run_id,
                task_id,
            )
            return None
        log.exception(
            "[scheduler-continuation] run %s was closed interrupted but its continuation "
            "could NOT be queued; the remaining work waits for the next fire. Remedy: fix "
            "the insert error, then use Run now on the schedule.",
            run_id,
        )
        await report_operational_failure(
            exc,
            operation="queue_run_continuation",
            context={"run_id": run_id, "task_id": task_id},
        )
        return None
    log.warning(
        "[scheduler-continuation] run %s (task %s) interrupted: continuation #%s queued as "
        "run %s with %ss of the fire's run ceiling and %s unit(s) carried",
        run_id,
        task_id,
        marker["index"],
        payload["id"],
        marker["remaining_runtime_seconds"],
        marker["carried_units_done"],
    )
    return str(payload["id"])


__all__ = [
    "CONTINUATION_KNOB_FEATURE",
    "CONTINUATION_KNOB_KEY",
    "MAX_CONTINUATIONS_PER_FIRE",
    "VERDICT_CEILING_SPENT",
    "VERDICT_CONTINUED",
    "VERDICT_EXHAUSTED",
    "VERDICT_LOST",
    "continuation_limit",
    "continuation_marker",
    "interrupt_run",
    "run_ceiling_seconds",
]
