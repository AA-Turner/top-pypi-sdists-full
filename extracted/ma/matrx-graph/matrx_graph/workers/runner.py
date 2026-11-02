"""Worker loop — claim jobs, dispatch the Scheduler, update wf_run.

Usage (entry point)::

    # In aidream — with AppContext, DefinitionStore, etc. wired:
    from matrx_graph.workers import WorkerRunner
    runner = WorkerRunner(app_context_factory=build_app_context)
    await runner.run_forever()

The runner is deliberately small. It depends on a host-app callable that
builds an ``AppContext`` for each job (because AppContext carries auth +
emitter, which worker instances don't have by default). The host decides:

- whether the worker has a null emitter (no streaming back to a client)
- whether the worker runs under a service account
- how to resolve the Definition for a given run_id (typically via
  DefinitionStore)

This module defines the loop; ``aidream/api/workflow_worker.py`` will
provide the concrete factory + Scheduler wiring when we turn it on.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable
from contextlib import AbstractContextManager, nullcontext
from typing import TYPE_CHECKING, Any

from matrx_utils import capture_error

from matrx_graph.workers import job_lease
from matrx_graph.workers.capability import (
    JobNeedsCapability,
    mark_run_awaiting_capability,
    worker_capabilities,
)
from matrx_graph.workers.queue import (
    _worker_id,
    defer_for_capability,
    enqueue_claimed,
    Job,
    JobHandedBack,
    claim_one,
    classify_failure,
    complete,
    fail,
    hand_back,
    reap_expired_leases,
    renew_lease,
    superseded_by,
)

log = logging.getLogger("matrx_graph.workers.runner")

if TYPE_CHECKING:
    from matrx_connect.context.app_context import AppContext


JobRunner = Callable[[Job, "AppContext"], Awaitable[None]]
AppContextFactory = Callable[[Job], Awaitable["AppContext"]]


class WorkerRunner:
    """Async worker loop with BOUNDED PARALLELISM.

    Configured with a ``job_runner`` that knows how to execute a claimed
    Job (typically: load the Definition, compile, instantiate Scheduler,
    call run/resume, write back run status). The runner handles queue
    plumbing — startup reconciliation, claim, lease renewal while the job executes (every
    lease/3 seconds, so ``reap_expired_leases`` only ever fires on a
    genuinely dead worker), retain terminal audit state on success, classify
    failures, and retry only transient failures.

    ``max_concurrent`` jobs execute at once, each as its OWN asyncio task with
    its own lease renewer. The claim loop keeps claiming while slots are free
    and only waits ``poll_interval`` when the queue is empty; when every slot
    is busy it waits for a slot instead of for the clock.

    Why this is not an optimization: the loop was strictly serial
    (claim → await → claim), so ONE slow job blocked EVERY other workflow on
    the platform behind it. Measured 2026-09-17: five concurrent Cloud Browser
    activations (each a workflow job that waits on container readiness) became
    a 5.5-second-per-run ladder, and at the 50-run fleet ceiling that is a
    ~4.5-minute tail during which nothing else in the queue moves.

    Per-job isolation is structural: each job runs in a task created from the
    claim loop's context, so ``contextvars`` a job sets (an AppContext, an
    ORM connection) are that task's own and CANNOT reach a sibling job or
    outlive the job in the loop. Under the old serial ``await`` they could —
    a job that installed an ambient AppContext left it installed in the loop.

    ``max_concurrent`` defaults to 1: a host that has not thought about the
    bound keeps exactly the behavior it had. Ours is a knob
    (``workflow_worker.max_concurrent_jobs``), never a constant.
    """

    def __init__(
        self,
        *,
        job_runner: JobRunner,
        app_context_factory: AppContextFactory,
        poll_interval_seconds: float = 1.0,
        visibility_timeout_seconds: int = 600,
        max_concurrent: int = 1,
        stop_grace_seconds: float = 60.0,
        capabilities: Callable[[], list[str]] | None = worker_capabilities,
    ) -> None:
        if max_concurrent < 1:
            raise ValueError(
                f"WorkerRunner max_concurrent must be >= 1; got {max_concurrent}. "
                "A worker that may run zero jobs is a stopped worker, not a "
                "configured one."
            )
        self._run_job = job_runner
        self._app_factory = app_context_factory
        self._poll_interval = poll_interval_seconds
        self._visibility_timeout = visibility_timeout_seconds
        self._max_concurrent = max_concurrent
        self._stop_grace = stop_grace_seconds
        # The node types this worker can run, read at every claim (the
        # registry is process state; a late registration counts). None turns
        # the capability filter off — every job is claimable, as before.
        self._capabilities = capabilities
        self._stop_event = asyncio.Event()
        self._in_flight: set[asyncio.Task[None]] = set()
        # The slot semaphore run_forever drives — shared with start_claimed so a job this
        # process starts directly counts against the same max_concurrent.
        self._slots: asyncio.Semaphore | None = None

    def stop(self) -> None:
        self._stop_event.set()

    @property
    def in_flight_count(self) -> int:
        return len(self._in_flight)

    async def _sleep_or_stop(self, seconds: float) -> None:
        try:
            await asyncio.wait_for(self._stop_event.wait(), timeout=seconds)
        except TimeoutError:
            pass

    async def _acquire_slot(self, slots: asyncio.Semaphore) -> bool:
        """Hold a slot, or report that the runner is stopping.

        Returns True with the semaphore HELD; False when ``stop()`` fired
        first (and nothing is held). A slot won in the same tick as the stop
        is handed straight back — never leaked.
        """
        acquire = asyncio.ensure_future(slots.acquire())
        stopping = asyncio.ensure_future(self._stop_event.wait())
        try:
            await asyncio.wait({acquire, stopping}, return_when=asyncio.FIRST_COMPLETED)
        finally:
            stopping.cancel()
        if acquire.done():
            return not acquire.cancelled()
        acquire.cancel()
        try:
            await acquire
        except asyncio.CancelledError:
            return False
        slots.release()
        return False

    async def run_forever(self) -> None:
        # Lifecycle-triggered recovery: reclaim expired leases before this
        # process asks for new work. The host's recurring sweep remains a
        # backstop for workers that die after startup.
        try:
            reaped = await reap_expired_leases()
            if reaped:
                log.warning(
                    "workflow worker startup reconciled %d expired lease(s)",
                    reaped,
                )
        except Exception as exc:  # noqa: BLE001 — recovery alarm, never silent boot death
            log.exception("workflow worker startup lease reconciliation failed")
            await capture_error(exc, kind="workflow_lease_reconciliation_failed")
        slots = asyncio.Semaphore(self._max_concurrent)
        self._slots = slots
        global _active_runner
        _active_runner = self
        try:
            while not self._stop_event.is_set():
                if not await self._acquire_slot(slots):
                    break
                try:
                    job = await claim_one(
                        visibility_timeout_seconds=self._visibility_timeout,
                        capabilities=self._capabilities() if self._capabilities else None,
                    )
                except asyncio.CancelledError:
                    slots.release()
                    raise
                except Exception as exc:  # noqa: BLE001 — a claim outage must not kill the worker
                    slots.release()
                    log.exception("workflow worker job claim failed; retrying")
                    try:
                        await capture_error(exc, kind="workflow_job_claim_failed")
                    except Exception:  # noqa: BLE001 — observability cannot defeat recovery
                        log.exception("workflow worker job-claim error capture failed")
                    await self._sleep_or_stop(self._poll_interval)
                    continue
                if job is None:
                    slots.release()
                    await self._sleep_or_stop(self._poll_interval)
                    continue
                task = asyncio.create_task(
                    self._process_in_slot(job, slots),
                    name=f"workflow_job_{job.job_id[:8]}",
                )
                self._in_flight.add(task)
                task.add_done_callback(self._in_flight.discard)
        finally:
            if _active_runner is self:
                _active_runner = None
            self._slots = None
            await self._drain_in_flight()

    async def start_claimed(
        self,
        *,
        run_id: str,
        inputs: dict[str, Any],
        max_steps: int,
        context: Callable[[], AbstractContextManager[Any]] | None = None,
    ) -> bool:
        """Start a fresh run's first leg in THIS process, keeping the queue's guarantees
        (lane 11 round 5): the same slot semaphore as claimed jobs (``max_concurrent``), a
        durable ``workflow.job`` row leased to this worker before the work starts, the same
        lease renewal and settlement (``_process``). ``context`` is entered around the task's
        creation, so the task — and only it — carries what it sets (ContextVars).

        Returns False, starting nothing, when this runner is stopping or has no slot free within
        one poll interval; the caller then queues the job normally.
        """
        slots = self._slots
        if slots is None or self._stop_event.is_set():
            return False
        # The claim loop holds a slot for the instant of each poll, so "free" means free
        # within one poll interval (plus a second); longer than that, the worker is busy.
        try:
            await asyncio.wait_for(slots.acquire(), timeout=self._poll_interval + 1.0)
        except TimeoutError:
            return False
        try:
            job = await enqueue_claimed(
                run_id=run_id,
                kind="start",
                inputs=inputs,
                max_steps=max_steps,
                visibility_timeout_seconds=self._visibility_timeout,
            )
        except BaseException:
            slots.release()
            raise
        with context() if context is not None else nullcontext():
            task = asyncio.create_task(
                self._process_in_slot(job, slots), name=f"workflow_job_{job.job_id[:8]}"
            )
        self._in_flight.add(task)
        task.add_done_callback(self._in_flight.discard)
        return True

    async def _process_in_slot(self, job: Job, slots: asyncio.Semaphore) -> None:
        """One job's task: run it, then hand the slot back — always.

        ``_process`` already swallows every ``Exception`` and settles the
        queue row itself, so the only escapes here are ``CancelledError``
        (drain) and a genuine bug in the settlement path; both are announced
        rather than lost in a task nobody awaits.
        """
        try:
            await self._process(job)
        except asyncio.CancelledError:
            raise
        except BaseException as exc:  # noqa: BLE001 — a job task must never die silently
            log.exception(
                "workflow worker job task %s escaped its own error handling",
                job.job_id,
            )
            try:
                await capture_error(
                    exc,
                    kind="workflow_job_task_escaped",
                    context={"job_id": job.job_id},
                )
            except Exception:  # noqa: BLE001 — observability cannot defeat recovery
                log.exception("workflow worker job-task error capture failed")
        finally:
            slots.release()

    async def _drain_in_flight(self) -> None:
        """Graceful stop: no new claims, then wait out the jobs already
        running for a BOUNDED grace, then cancel what is left.

        A canceled job is not lost: ``_process`` fails it retryable and the
        host's terminal-write path parks the run as resumable, exactly as it
        did when a serial worker was killed mid-job.
        """
        pending = {task for task in self._in_flight if not task.done()}
        if not pending:
            return
        log.info(
            "workflow worker draining %d in-flight job(s) with a %.0fs grace",
            len(pending),
            self._stop_grace,
        )
        _done, still_running = await asyncio.wait(pending, timeout=self._stop_grace)
        if not still_running:
            return
        log.error(
            "workflow worker drain grace (%.0fs) expired with %d job(s) still "
            "running — canceling them; each fails retryable and its run "
            "resumes from its last checkpoint",
            self._stop_grace,
            len(still_running),
        )
        for task in still_running:
            task.cancel()
        await asyncio.gather(*still_running, return_exceptions=True)

    async def _process(self, job: Job) -> None:
        # The lease this copy holds, published to the work (``job_lease.check`` before each item) and marked lost by
        # the renewal the moment the queue says the job is no longer ours (lane K1, 2026-10-21).
        lease = job_lease.JobLease(
            job_id=job.job_id,
            run_id=job.run_id,
            claimed_by=job.claimed_by,
            look_every=max(self._visibility_timeout // 3, 10) / 10,
            owner=asyncio.current_task(),
            visibility_timeout=self._visibility_timeout,
            # the job's attempt: every re-claim bumps it, so a later copy's fencing token is always greater (K1b, B5)
            generation=float(job.attempt or 0),
        )
        renewer = asyncio.create_task(
            self._renew_loop(job.job_id, claimed_by=job.claimed_by, lease=lease, owner=asyncio.current_task())
        )
        try:
            if await settle_if_superseded(job):
                return
            app = await self._app_factory(job)
            with job_lease.holding(lease):
                await self._run_job(job, app)
            lease.settling = True  # a renewal answering "not ours" after this settles is not a loss (K1b, M1)
            await complete(job.job_id, claimed_by=job.claimed_by)
        except JobNeedsCapability as need:
            await hand_back_for_capability(job, need)
        except JobHandedBack as handed:
            lease.settling = True
            await settle_handed_back(job, handed)
        except asyncio.CancelledError as exc:
            if lease.lost:
                # A copy whose lease was reaped stops here and settles NOTHING: the job row and the run belong to the
                # copy that holds the job now (its fail() would be fenced anyway; this keeps the log honest).
                log.warning("job %s: this copy stopped after losing its lease (%s); the current holder owns the run",
                            job.job_id[:8], lease.why)
                raise
            try:
                await asyncio.shield(
                    fail(
                        job.job_id,
                        error={"type": "CancelledError", "message": "worker canceled"},
                        retryable=True,
                        attempt=job.attempt,
                        max_attempts=job.max_attempts,
                        claimed_by=job.claimed_by,
                    )
                )
            except Exception as finalize_exc:  # noqa: BLE001
                await capture_error(
                    finalize_exc,
                    kind="workflow_job_cancellation_finalize_failed",
                    context={"job_id": job.job_id},
                )
            await capture_error(
                exc,
                kind="workflow_job_cancelled",
                context={"job_id": job.job_id},
            )
            raise
        except Exception as e:  # noqa: BLE001 — worker must never raise
            disposition = classify_failure(e)
            try:
                await fail(
                    job.job_id,
                    error={
                        "type": type(e).__name__,
                        "message": str(e),
                        "classification_reason": disposition.reason,
                        "status_code": disposition.status_code,
                    },
                    retryable=disposition.retryable,
                    attempt=job.attempt,
                    max_attempts=job.max_attempts,
                    claimed_by=job.claimed_by,
                )
            except Exception as persist_exc:  # noqa: BLE001 — lease reaper is the backstop
                log.exception(
                    "failed to persist %s queue disposition for job %s; "
                    "leaving the claim for lease reconciliation",
                    disposition.failure_class,
                    job.job_id,
                )
                await capture_error(
                    persist_exc,
                    kind="workflow_job_failure_persistence_failed",
                    context={"job_id": job.job_id},
                )
            # Re-raising would kill the worker process. We log via the host
            # app's logging config — stdlib print is a last resort here.
            import traceback as _tb

            _tb.print_exc()
            await capture_error(
                e,
                kind="workflow_job_failed",
                context={"job_id": job.job_id, "failure_class": disposition.failure_class},
            )
        finally:
            renewer.cancel()
            try:
                await renewer
            except asyncio.CancelledError:
                pass

    async def _renew_loop(
        self,
        job_id: str,
        *,
        claimed_by: str | None,
        lease: job_lease.JobLease | None = None,
        owner: asyncio.Task[Any] | None = None,
    ) -> None:
        # Lease/3 keeps two renewal misses of headroom before expiry; the
        # reaper adds its own grace on top, so only a dead worker is reaped.
        interval = max(self._visibility_timeout // 3, 10)
        while True:
            await asyncio.sleep(interval)
            try:
                still_ours = await renew_lease(
                    job_id,
                    visibility_timeout_seconds=self._visibility_timeout,
                    claimed_by=claimed_by,
                )
            except Exception as exc:  # noqa: BLE001 — a DB blip must not kill the job
                log.warning(
                    "lease renewal for job %s failed (transient?) — will retry",
                    job_id,
                    exc_info=True,
                )
                await capture_error(
                    exc,
                    kind="workflow_lease_renewal_failed",
                    context={"job_id": job_id},
                )
                continue
            if not still_ours:
                # Reaped (a false "dead" after a database outage looks exactly like this) or settled elsewhere.
                # Arman, 2026-10-21: a copy that loses its job lease STOPS ITSELF. Finishing "anyway" (the old rule)
                # left two copies of one run alive: the old one, hung on a store call, kept its organization import
                # slot and the restarted copy waited on itself (run 8749d414). Another copy may own the run now, so
                # this one stops: the lease is marked lost (many-item work checks it before each item), the job
                # task is cancelled, and the host skips its terminal write.
                # Lane K1b, B1: when the reaper only DEAD-LETTERED the job (a false "dead" on its last attempt), no
                # other copy can ever own the run, so this copy takes the job back and finishes it (stopping would
                # strand the run: nothing would ever write its terminal status).
                if lease is not None:
                    if lease.settling:
                        return
                    if await lease.not_ours("the queue reaped or settled the job"):
                        continue
                log.error(
                    "job %s lease is no longer ours (reaped or deleted) — "
                    "this copy stops; the current holder owns the run",
                    job_id,
                )
                if owner is not None and not owner.done():
                    owner.cancel()
                return


async def hand_back_for_capability(job: Job, need: JobNeedsCapability) -> None:
    """The job's graph needs node types this worker lacks: give the job back
    (no attempt spent, never failed) and say on the run what it waits for."""
    log.warning(
        "job %s (run %s) needs node type(s) %s this worker does not have — "
        "leaving it for a server that supports them",
        job.job_id[:8],
        job.run_id[:8],
        ", ".join(need.missing),
    )
    try:
        await defer_for_capability(
            job.job_id, required_node_types=need.required, claimed_by=job.claimed_by
        )
        await mark_run_awaiting_capability(job.run_id, missing=need.missing, worker_id=_worker_id())
    except Exception as exc:  # noqa: BLE001 — the lease reaper is the backstop
        log.exception("could not hand job %s back for a capable worker", job.job_id)
        await capture_error(
            exc,
            kind="workflow_job_capability_handback_failed",
            context={"job_id": job.job_id, "missing": need.missing},
        )


async def settle_if_superseded(job: Job) -> bool:
    """A job a NEWER job for its run replaced never drives the run: it is retained as
    dead-letter ``superseded`` and True is returned. Never raises — an unreadable check
    runs the job as before (the run's status CAS still guards it)."""
    try:
        newer = await superseded_by(job)
    except Exception:  # noqa: BLE001 — the check must never strand a job
        log.warning("could not check whether job %s is superseded; running it", job.job_id[:8], exc_info=True)
        return False
    if newer is None:
        return False
    log.warning(
        "job %s (run %s) was replaced by newer job %s for the same run; not running it",
        job.job_id[:8],
        job.run_id[:8],
        newer[:8],
    )
    try:
        await fail(
            job.job_id,
            error={"type": "superseded", "message": f"replaced by newer job {newer}", "superseded_by": newer},
            retryable=False,
            claimed_by=job.claimed_by,
        )
    except Exception as exc:  # noqa: BLE001 — the reaper is the backstop; the run is untouched
        await capture_error(exc, kind="workflow_job_superseded_settle_failed", context={"job_id": job.job_id})
    return True


async def settle_handed_back(job: Job, handed: JobHandedBack) -> None:
    """The host parked the run resumable while its process drained: the SAME job row
    becomes the continuation another worker claims. Shielded — this runs on a task
    the drain is cancelling."""
    try:
        moved = await asyncio.shield(
            hand_back(
                job.job_id,
                claimed_by=job.claimed_by,
                kind=handed.kind,
                checkpoint_id=handed.checkpoint_id,
                resume_value=handed.resume_value,
                reason=handed.reason,
                attempt=job.attempt,
            )
        )
        if moved:
            log.warning(
                "job %s (run %s) handed back as %s from %s (%s)",
                job.job_id[:8],
                job.run_id[:8],
                handed.kind,
                (handed.checkpoint_id or "its inputs")[:8],
                handed.reason,
            )
    except BaseException as exc:  # noqa: BLE001 — the lease reaper releases a job left claimed
        log.exception("could not hand job %s back", job.job_id)
        await capture_error(exc, kind="workflow_job_handback_failed", context={"job_id": job.job_id})


async def run_single_job(runner: JobRunner, app_factory: AppContextFactory) -> bool:
    """Convenience: claim + run ONE job (or return False if queue empty).

    Useful for tests and for request-scoped "drain queue inline" patterns.
    Capability-aware like the long-running loop.
    """
    job = await claim_one(capabilities=worker_capabilities())
    if job is None:
        return False
    try:
        if await settle_if_superseded(job):
            return True
        app = await app_factory(job)
        await runner(job, app)
        await complete(job.job_id, claimed_by=job.claimed_by)
    except JobNeedsCapability as need:
        await hand_back_for_capability(job, need)
    except JobHandedBack as handed:
        await settle_handed_back(job, handed)
    except Exception as e:  # noqa: BLE001
        disposition = classify_failure(e)
        try:
            await fail(
                job.job_id,
                error={
                    "type": type(e).__name__,
                    "message": str(e),
                    "classification_reason": disposition.reason,
                    "status_code": disposition.status_code,
                },
                retryable=disposition.retryable,
                attempt=job.attempt,
                max_attempts=job.max_attempts,
                claimed_by=job.claimed_by,
            )
        except Exception as persist_exc:  # noqa: BLE001 — preserve the original job failure
            log.exception(
                "failed to persist %s queue disposition for single job %s; "
                "leaving the claim for lease reconciliation",
                disposition.failure_class,
                job.job_id,
            )
            await capture_error(
                persist_exc,
                kind="workflow_job_failure_persistence_failed",
                context={"job_id": job.job_id},
            )
        raise
    return True


_ = Any  # placeholder — keeps import tidy for callers that wildcard this module


#: The runner driving this process's queue, while it runs (one per worker process).
_active_runner: WorkerRunner | None = None


def active_runner() -> WorkerRunner | None:
    """The WorkerRunner of THIS process, or None when none is running here."""
    return _active_runner

