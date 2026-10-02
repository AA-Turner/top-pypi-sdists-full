"""
The scanner loop. Background asyncio task, ticks every N seconds:

  1. Sweep expired leases (failed; recurring triggers will re-enqueue).
  2. Find queued runs (from `Run now` manual fires) and claim them.
  3. Find scheduled tasks due now, claim, dispatch.

Designed so multiple host processes can run scanners against the same DB
without double-running: the partial unique index
`sch_run_unique_active_per_task` is the atomicity primitive — concurrent
claims raise unique-violation and lose the race cleanly.
"""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from matrx_utils import supervised_task

from . import queries
from ._ext import get_ext, has_ext, is_configured, report_operational_failure
from .next_due import compute_next_due_at
from .runner import run_claimed_task


log = logging.getLogger("matrx_scheduler.scanner")


@dataclass
class ScannerStatus:
    started_at: datetime | None = None
    last_tick_at: datetime | None = None
    last_tick_duration_ms: int | None = None
    last_tick_claimed: int = 0
    last_tick_expired_sweeps: int = 0
    last_tick_manual_claimed: int = 0
    running: bool = False
    error_message: str | None = None
    consecutive_errors: int = 0
    total_runs_dispatched: int = 0
    in_flight_count: int = 0
    #: Tasks that read enabled but have no enabled trigger — see
    #: ``queries.find_dark_tasks``. Swept hourly, not per tick. Carried on the
    #: status object so an ops surface can show the lie without a DB trip.
    dark_tasks: list[dict[str, Any]] = field(default_factory=list)
    dark_tasks_checked_at: datetime | None = None


# How often the dark-schedule sweep runs. Hourly, not per tick: a task that
# cannot fire has been unable to fire since someone last wrote the row, so
# detecting it a few minutes later costs nothing, while a per-tick scan of
# every enabled task would be pure waste at a 5s cadence.
DARK_TASK_SWEEP_SECONDS = 3600.0

_status: ScannerStatus = ScannerStatus()
_task: asyncio.Task[None] | None = None
_in_flight: set[asyncio.Task[None]] = set()


def status() -> ScannerStatus:
    _status.in_flight_count = len(_in_flight)
    return _status


def is_running() -> bool:
    return _status.running


def _dispatch_run(hydrated, run) -> None:
    """Spawn a run task and track it for clean shutdown."""
    coro = run_claimed_task(hydrated, run)
    task = asyncio.create_task(coro, name=f"sch_run-{run.id}")
    _in_flight.add(task)

    def _done(t: asyncio.Task[None]) -> None:
        _in_flight.discard(t)
        if t.cancelled():
            return
        exc = t.exception()
        if exc:
            log.exception(
                "in-flight run task crashed", exc_info=(type(exc), exc, exc.__traceback__)
            )
            supervised_task(
                report_operational_failure(
                    exc,
                    operation="in_flight_run_task",
                    context={"run_id": str(run.id), "task_id": str(hydrated.task.id)},
                ),
                kind="scheduler_failure_capture_task_failed",
                name="scheduler-failure-capture",
            )

    task.add_done_callback(_done)


async def _sweep_dark_tasks() -> None:
    """SCREAM about schedules that read enabled and can never fire.

    Throttled to ``DARK_TASK_SWEEP_SECONDS``. Never raises: an alarm is not
    allowed to stop the scanner that carries every scheduled run in the system.
    """
    now = datetime.now(timezone.utc)
    last = _status.dark_tasks_checked_at
    if last is not None and (now - last).total_seconds() < DARK_TASK_SWEEP_SECONDS:
        return
    try:
        dark = await queries.find_dark_tasks()
    except Exception:  # noqa: BLE001 — the alarm never breaks the loop
        log.exception("scanner: dark-schedule sweep failed; the guard is blind this hour")
        return
    _status.dark_tasks_checked_at = now
    _status.dark_tasks = dark
    for row in dark:
        log.error(
            "[scheduler-dark-schedule] sch_task %s (%r) is ENABLED but every one of its "
            "triggers is disabled — every surface reads 'enabled' while it fires NOTHING, "
            "forever. Either enable its trigger or disable the task; a half-enabled "
            "schedule is a lie, not a pause.",
            row["id"],
            row["title"],
        )


async def _tick() -> None:
    tick_started = time.perf_counter()
    _status.last_tick_at = datetime.now(timezone.utc)

    expired = await queries.sweep_expired_leases()
    _status.last_tick_expired_sweeps = expired

    await _sweep_dark_tasks()

    lease = int(get_ext("lease_seconds"))

    # Pass 1: manual queued runs (FE "Run now").
    manual_claimed = 0
    try:
        queued = await queries.find_queued_runs()
        for run, hydrated in queued:
            # Non-agent kinds (ping, tool) may have no agent_task; fall
            # back to the SchAgentTask default runtime (600s) for lease
            # sizing. The runner's kind dispatch enforces presence per
            # kind after claim.
            max_runtime = (
                hydrated.agent_task.max_runtime_seconds
                if hydrated.agent_task is not None
                else 600
            )
            promoted = await queries.claim_queued_run(run, lease, max_runtime)
            if promoted is None:
                continue
            manual_claimed += 1
            _status.total_runs_dispatched += 1
            _dispatch_run(hydrated, promoted)
    except Exception as exc:
        log.exception("scanner: queued-run pass failed")
        await report_operational_failure(exc, operation="queued_run_scan")
    _status.last_tick_manual_claimed = manual_claimed

    # Pass 2: scheduled tasks.
    scheduled_claimed = 0
    candidates = await queries.find_due_tasks()
    for hydrated in candidates:
        try:
            run = await queries.claim_task(
                hydrated.task, hydrated.trigger, hydrated.agent_task, lease
            )
            if run is None:
                continue
            scheduled_claimed += 1
            _status.total_runs_dispatched += 1

            # Advance next_due_at IMMEDIATELY on claim so the scanner doesn't
            # re-fetch this row on the next tick before the run finishes.
            # The runner's post-run advance is still authoritative — this is
            # a short-circuit to keep the scanner queue clean.
            if hydrated.trigger is not None and hydrated.trigger.type != "one-shot":
                next_at = compute_next_due_at(
                    hydrated.trigger.type, hydrated.trigger.config
                )
                if next_at is not None:
                    await queries.advance_trigger_next_due_at(
                        hydrated.trigger.id, next_at
                    )

            _dispatch_run(hydrated, run)
        except Exception as exc:
            log.exception(
                "scanner failed to dispatch task %s", hydrated.task.id
            )
            await report_operational_failure(
                exc,
                operation="scheduled_task_dispatch",
                context={"task_id": str(hydrated.task.id)},
            )

    _status.last_tick_claimed = scheduled_claimed
    _status.last_tick_duration_ms = int(
        (time.perf_counter() - tick_started) * 1000
    )
    _status.consecutive_errors = 0
    _status.error_message = None


async def _beat(*, alive: bool) -> None:
    """Tell the host the scanner is (or is no longer) alive. Never raises.

    🚨 A scanner that stops ticking inside a process that stays up and healthy
    is invisible without this: on 2026-09-15 every scheduled task on the
    platform stopped for 17+ minutes while the API served normally, and no
    surface could tell the difference between "the scheduler is dead" and "this
    instance was never the one running it". A heartbeat makes absence a fact
    anyone can read. A failure to beat must never take the loop down with it —
    losing observability is bad, losing the scheduler is worse.
    """
    if not has_ext("heartbeat"):
        return
    try:
        await get_ext("heartbeat")(
            alive=alive,
            status={
                "started_at": _status.started_at.isoformat() if _status.started_at else None,
                "last_tick_at": _status.last_tick_at.isoformat()
                if _status.last_tick_at
                else None,
                "last_tick_duration_ms": _status.last_tick_duration_ms,
                "last_tick_claimed": _status.last_tick_claimed,
                "total_runs_dispatched": _status.total_runs_dispatched,
                "consecutive_errors": _status.consecutive_errors,
                "error_message": _status.error_message,
            },
        )
    except Exception:  # noqa: BLE001
        log.exception("scanner heartbeat failed — the loop continues regardless")


async def run_forever() -> None:
    """Main scanner loop. Wrapped in asyncio.create_task by start_scanner."""
    if not is_configured():
        raise RuntimeError(
            "matrx-scheduler not configured. Call matrx_scheduler.configure() first."
        )

    interval = float(get_ext("scan_interval_seconds"))
    _status.started_at = datetime.now(timezone.utc)
    _status.running = True
    log.info(
        "matrx-scheduler scanner started — interval=%.1fs surface=%s",
        interval,
        get_ext("surface"),
    )

    await _beat(alive=True)

    try:
        while True:
            try:
                await _tick()
                await _beat(alive=True)
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                _status.consecutive_errors += 1
                _status.error_message = str(exc)[:200]
                log.exception("scanner tick failed (consecutive=%d)", _status.consecutive_errors)
                await report_operational_failure(
                    exc,
                    operation="scanner_tick",
                    context={"consecutive_errors": _status.consecutive_errors},
                )
                # Exponential backoff capped at 5 minutes.
                backoff = min(300.0, interval * (2 ** min(_status.consecutive_errors, 8)))
                await asyncio.sleep(backoff)
                continue
            await asyncio.sleep(interval)
    finally:
        _status.running = False
        # The loop is leaving — say so, whether this is an orderly shutdown or
        # the task dying under us. A stale heartbeat is the alarm's evidence.
        await _beat(alive=False)
        log.info("matrx-scheduler scanner stopped")


async def start_scanner() -> None:
    """Idempotent — spawns the scanner task once per process."""
    global _task
    if _task and not _task.done():
        return
    _task = asyncio.create_task(run_forever(), name="matrx-scheduler-scanner")


_drain: asyncio.Future[None] | None = None


async def stop_scanner(in_flight_timeout: float = 10.0, finalize_timeout: float = 10.0) -> None:
    """
    Graceful shutdown: stop claiming, give in-flight runs ``in_flight_timeout``
    to finish, then cancel the rest and give each ``finalize_timeout`` to write
    its interruption and queue its continuation (``runner.run_claimed_task``).

    ONE DRAIN, JOINED BY EVERY CALLER. A host may call this more than once (the
    worker's signal handler starts it; its teardown ``finally`` calls it again).
    Before 2026-09-14 the second call returned at once — ``_task`` was already
    cleared — so the host finished its teardown and the event loop closed while
    the first drain was still waiting, cancelling the very writes that preserve a
    run. Every call now awaits the same drain, shielded from its caller's own
    cancellation.
    """
    global _drain
    drain = _drain
    if drain is None or drain.done():
        drain = asyncio.ensure_future(_drain_scanner(in_flight_timeout, finalize_timeout))
        _drain = drain
    await asyncio.shield(drain)


async def _drain_scanner(in_flight_timeout: float, finalize_timeout: float) -> None:
    global _task
    if _task is not None:
        _task.cancel()
        try:
            await _task
        except asyncio.CancelledError:
            pass
        finally:
            _task = None

    if not _in_flight:
        return
    running = list(_in_flight)
    _done, pending = await asyncio.wait(running, timeout=in_flight_timeout)
    if pending:
        log.warning(
            "shutdown: %d in-flight run(s) still running after %.0fs; cancelling — each "
            "is closed `interrupted` and a continuation is queued for the next worker",
            len(pending),
            in_flight_timeout,
        )
        for t in pending:
            t.cancel()
        _finished, unfinished = await asyncio.wait(pending, timeout=finalize_timeout)
        if unfinished:
            log.error(
                "[scheduler-shutdown-finalize-timeout] %d run(s) did not write their "
                "interruption within %.0fs; the next worker's orphaned-lease sweep will "
                "close and continue them once their lease lapses",
                len(unfinished),
                finalize_timeout,
            )
    _in_flight.clear()
