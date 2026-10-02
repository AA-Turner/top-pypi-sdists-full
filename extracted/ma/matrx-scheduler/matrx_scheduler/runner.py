"""
Runs a claimed task: drives the host's agent_runner, writes results back,
handles heartbeat conversation continuity, and recomputes next_due_at for
recurring triggers.

All writes to the run row are gated by `claim_token` -- if our lease has
lapsed and another claimer took over, the writes silently no-op (rowcount=0)
and we bail without corrupting the new claimer's state.

Kind dispatch (Phase 4):
The scanner no longer filters on ``kind`` (see queries.find_due_tasks).
``run_claimed_task`` dispatches by kind:

  - ``agent``  -- existing path: invoke host's ``agent_runner``.
  - ``tool``   -- requires a host-supplied ``tool_runner`` callable.
                  Without one, the run finalizes ``failed`` with a
                  clear error_message so the FE shows it.
  - ``ping``   -- minimal handler returning ``success=True`` and a
                  fixed summary. Useful for end-to-end claim/run/
                  finalize verification.
  - anything else -- fails cleanly with ``unsupported kind=...``.

To register a tool_runner, call ``matrx_scheduler.configure(...,
tool_runner=callable)`` at host startup. The callable receives a
ToolRunInput and returns an AgentRunResult (same shape -- it's the
generic "ran something, here's the result" envelope).
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
from datetime import UTC, datetime
from typing import Any

from . import queries
from ._ext import get_ext, report_operational_failure
from .backlog import BacklogRearmOutcome, BacklogRearmRequest, finalize_and_rearm_backlog
from .continuation import VERDICT_LOST, interrupt_run, run_ceiling_seconds
from .lease import RunLease, bind_run_lease, heartbeat_until_stopped, unbind_run_lease
from .models import (
    RUN_STOPPED_EARLY_KEY,
    RUN_UNITS_DONE_KEY,
    AgentRunInput,
    AgentRunResult,
    BacklogRearmResult,
    HydratedTask,
    SchRun,
    ToolRunInput,
)
from .next_due import compute_next_due_at
from .repeat_guard import suspend_schedule_now


log = logging.getLogger("matrx_scheduler.runner")



def variables_for_run(
    task_variables: dict[str, Any] | None, run_metadata: dict[str, Any] | None
) -> dict[str, Any]:
    """The agent's variables for ONE run: the task's own, plus `event` when the
    run was enqueued by an event trigger (scheduler.sch_match_event writes the
    spine row under sch_run.metadata.event). A task variable literally named
    `event` is kept when the run carries none; when both exist the run's event
    wins, because it is the reason this run exists."""
    base: dict[str, Any] = dict(task_variables or {})
    event = (run_metadata or {}).get("event")
    if isinstance(event, dict) and event:
        base["event"] = event
    return base

async def _interrupt_cancelled_run(
    run: SchRun, task: Any, claim_token: str, lease: RunLease, *, reason: str
) -> str:
    """Terminal write for a run whose WORKER is going away: closed
    ``interrupted`` with everything the handler reported, and a continuation
    queued (``continuation.interrupt_run``). A run that is no longer ours still
    ran — the task row says so."""
    verdict = await interrupt_run(
        run_id=run.id,
        claim_token=claim_token,
        reason=reason,
        result_metadata=lease.snapshot_metadata(),
        max_runtime_seconds=lease.max_runtime_seconds,
    )
    if verdict == VERDICT_LOST:
        await queries.update_last_run_at(task.id)
    return verdict


async def run_claimed_task(hydrated: HydratedTask, run: SchRun) -> None:
    """
    Drive a single run end-to-end. The caller has already won the claim race
    and stored a sch_run row with status='claimed' and a claim_token.

    All status-writing calls are gated by run.claim_token; if our lease
    expired mid-flight (the sweep marked it failed and another claimer took
    over), the writes return False and we exit without overwriting the new
    state.

    THE LEASE (``lease.py``). The kind-specific handler runs in a child task
    beside a heartbeat that renews ``claim_expires_at`` every third of the
    lease while the handler is alive, and stops it at the schedule's
    ``max_runtime_seconds`` (the hard deadline). The handler reaches the same
    ``RunLease`` through ``current_run_lease()`` to stop cleanly before the
    deadline and to write progress (``units_done``) onto the row as it goes.
    Whatever it reported is preserved on EVERY terminal path — normal return,
    deadline cancel, lost lease, worker shutdown — so the repeat guard's
    work-done test is never blind to work that landed.

    SHUTDOWN IS AN INTERRUPTION, NOT A VERDICT. A cancellation of this task only
    ever comes from outside the runner — ``stop_scanner`` on a deploy's SIGTERM,
    or the event loop closing — because the runner's own stops (deadline, lost
    lease) return instead of raising. So a ``CancelledError`` here closes the run
    ``interrupted`` with its progress and queues a continuation
    (``continuation.py``); the shielded write is lease-gated, so a cancel landing
    after the handler already finalized is a benign no-op and queues nothing.
    A continuation runs under what is left of its fire's run ceiling.
    """
    task = hydrated.task
    agent_task = hydrated.agent_task
    trigger = hydrated.trigger
    claim_token = run.claim_token or ""

    if not claim_token:
        log.error("run %s missing claim_token; refusing to drive", run.id)
        return

    lease = RunLease(
        run_id=run.id,
        task_id=task.id,
        claim_token=claim_token,
        lease_seconds=int(get_ext("lease_seconds")),
        max_runtime_seconds=run_ceiling_seconds(
            run.metadata,
            agent_task.max_runtime_seconds if agent_task is not None else 600,
        ),
        claimed_at=run.claimed_at,
        renew=queries.renew_run_lease,
        record_progress=queries.record_run_progress,
    )
    token = bind_run_lease(lease)
    try:
        await _run_claimed_task_inner(
            hydrated, run, task, agent_task, trigger, claim_token, lease
        )
    except asyncio.CancelledError:
        reason = "the worker shut down mid-run (runner cancelled before completion)"
        try:
            await asyncio.shield(
                _interrupt_cancelled_run(run, task, claim_token, lease, reason=reason)
            )
        except Exception as exc:
            # Lease-expiry sweep is the backstop if even the shielded
            # write fails. Don't block the cancel propagation.
            log.exception("run %s: shielded finalize-on-cancel failed", run.id)
            await report_operational_failure(
                exc,
                operation="finalize_cancelled_run",
                context={"run_id": str(run.id), "task_id": str(task.id)},
            )
        raise
    finally:
        unbind_run_lease(token)


async def _finalize_stopped_run(
    run: SchRun, task: Any, claim_token: str, lease: RunLease, *, reason: str
) -> bool:
    """Terminal write for a run the RUNNER stopped (deadline, lost lease,
    shutdown cancel) — never the handler's own return. The verdict follows
    the bounded-work rule the handlers themselves use: work landed means the
    run is not failed, and the stop is named in the summary and the metadata;
    nothing landed means failed with the reason as the error. Progress the
    handler reported through the lease is carried either way."""
    units = lease.units_done
    stop = f"{reason} after committing {units} unit(s)"
    metadata = lease.snapshot_metadata(stopped_early=stop)
    if units > 0:
        persisted = await queries.finalize_run(
            run.id,
            claim_token,
            status="success",
            result_summary=f"units_done={units} STOPPED_EARLY: {stop}",
            error_message=reason,
            result_metadata=metadata,
        )
    else:
        persisted = await queries.finalize_run(
            run.id,
            claim_token,
            status="failed",
            error_message=reason,
            result_metadata=metadata,
        )
    if not persisted:
        # The row is no longer ours (the sweep expired it, or another claimer
        # took over). The task still RAN; say so on the task row.
        await queries.update_last_run_at(task.id)
    return persisted


async def _run_claimed_task_inner(
    hydrated: HydratedTask,
    run: SchRun,
    task: Any,
    agent_task: Any,
    trigger: Any,
    claim_token: str,
    lease: RunLease,
) -> None:
    # 1. Mark running, lease-gated.
    if not await queries.mark_run_running(run.id, claim_token):
        log.warning("run %s lost lease before mark_running; aborting", run.id)
        return

    # 2. Dispatch by kind, supervised by the lease heartbeat. Each branch
    #    produces an AgentRunResult or finalizes the run + returns early.
    result = await _dispatch_under_lease(hydrated, run, task, claim_token, lease)
    if result is None:
        # Already finalized (by the kind dispatch, or by the lease supervisor).
        # A one-shot is still spent: before 2026-09-28 this return skipped the
        # roll-forward, so a failed one-shot kept a due trigger — re-claimed on
        # the next tick while its task was enabled, and reading "due, never
        # fired" forever once something had switched the task off.
        await _settle_one_shot(task, trigger, run)
        return

    # Defensive: ensure whichever runner returned the right shape.
    if not isinstance(result, AgentRunResult):
        log.error(
            "kind=%s runner returned non-AgentRunResult: %s",
            task.kind,
            type(result).__name__,
        )
        await queries.finalize_run(
            run.id,
            claim_token,
            status="failed",
            error_message=f"kind={task.kind} runner returned unexpected shape",
        )
        await _settle_one_shot(task, trigger, run)
        return

    if isinstance(result, BacklogRearmResult):
        await _finalize_backlog_result(run, task, claim_token, lease, result)
        return

    # 3. Heartbeat conversation continuity — conditional update wins the race.
    # Non-agent kinds (ping/tool) have agent_task=None; they never have a
    # persistent_conversation_id to bind, so skip the heartbeat dance.
    if (
        trigger is not None
        and trigger.type == "heartbeat"
        and result.conversation_id
        and agent_task is not None
        and not agent_task.persistent_conversation_id
    ):
        canonical = await queries.set_persistent_conversation(task.id, result.conversation_id)
        # If we lost the race, use the canonical conversation id for output_ref.
        if canonical and canonical != result.conversation_id:
            result = result.model_copy(update={"conversation_id": canonical})

    # 4. Finalize, lease-gated.
    output_ref = (
        {"kind": "conversation", "id": result.conversation_id} if result.conversation_id else None
    )
    # THE WORK-DONE CONTRACT. `units_done` and `stopped_early` are stamped on
    # EVERY terminal write, under reserved keys the handler's own metadata can
    # never shadow, so the ledger row itself says how much landed and why the
    # run stopped -- the repeat guard reads exactly these keys back. A handler
    # that never sets them reports 0, which is honest: "unmeasured" is not
    # "did work". Progress the handler reported through the lease mid-run is
    # the floor: a handler that reported 600 units in flight and then returned
    # a result that forgot to count them still lands as 600. An error a handler
    # chose to report is persisted even on a successful (partial) run: the
    # runner is not the place information gets thrown away.
    result_metadata: dict[str, Any] = dict(result.metadata or {})
    units_done = max(0, int(result.units_done or 0), lease.units_done)
    for key, value in (
        (RUN_UNITS_DONE_KEY, units_done),
        (RUN_STOPPED_EARLY_KEY, result.stopped_early),
    ):
        if key in result_metadata and result_metadata[key] != value:
            log.warning(
                "run %s: handler metadata carried %r=%r; the reserved contract value %r wins",
                run.id,
                key,
                result_metadata[key],
                value,
            )
        result_metadata[key] = value
    persisted = await queries.finalize_run(
        run.id,
        claim_token,
        # A lease-reported unit is work: a run that says "skipped" but landed
        # units mid-flight is a success (terminal_status reads units_done).
        status=result.model_copy(update={"units_done": units_done}).terminal_status(),
        result_summary=result.result_summary,
        error_message=result.error_message,
        output_ref=output_ref,
        result_metadata=result_metadata,
    )
    if not persisted:
        # The task ran — every unit the handler committed is real — even though
        # the ledger row moved on without us. Stamp the task, then stand down
        # from the trigger: whoever owns the row now owns the roll-forward.
        log.warning(
            "run %s lost lease before finalize (%d unit(s) committed); the task's "
            "last_run_at is stamped, the trigger is not advanced here",
            run.id,
            units_done,
        )
        await queries.update_last_run_at(task.id)
        return

    # 5. Roll the trigger forward.
    if trigger is not None:
        if trigger.type == "one-shot":
            await _settle_one_shot(task, trigger, run)
        else:
            now = datetime.now(UTC)
            next_at = compute_next_due_at(trigger.type, trigger.config, now=now)
            await queries.advance_trigger_next_due_at(trigger.id, next_at)


async def _settle_one_shot(task: Any, trigger: Any, run: SchRun) -> None:
    """A one-shot fires ONCE, whatever its run's verdict.

    Every terminal path of a one-shot's fire lands here: the task is switched
    off and the trigger records that it fired. A success or skip is spent
    (``next_due_at`` cleared). A failed verdict keeps the trigger's instant, so
    the deliberate human re-enable that follows a repair retries it once — and
    the failure itself was already made loud by the repeat guard's one-shot
    ceiling, which suspended the task with its reason and told its owner.

    A run that is not terminal (``interrupted`` — a continuation carries the
    fire) is left alone; the continuation settles it.
    """
    if trigger is None or trigger.type != "one-shot":
        return
    status = await queries.read_run_status(run.id)
    if status is None or status in {"queued", "claimed", "running", "interrupted"}:
        return
    await queries.disable_task(task.id)
    if status in queries.FAILED_RUN_STATUSES:
        await queries.mark_trigger_fired(trigger.id)
    else:
        await queries.advance_trigger_next_due_at(trigger.id, None)


async def _finalize_backlog_result(
    run: SchRun,
    task: Any,
    claim_token: str,
    lease: RunLease,
    result: BacklogRearmResult,
) -> BacklogRearmOutcome:
    """Atomically finish one bounded batch and queue its next on-demand run.

    The persistence primitive re-reads and locks every authority-bearing row.
    The persistence primitive also stamps the task's completion time in its
    transaction. A successful return therefore needs no post-commit reporting
    step with a crash gap or duplicate-retry ambiguity.
    """
    result_metadata: dict[str, Any] = dict(result.metadata or {})
    units_done = max(0, int(result.units_done or 0), lease.units_done)
    result_metadata[RUN_UNITS_DONE_KEY] = units_done
    result_metadata[RUN_STOPPED_EARLY_KEY] = result.stopped_early
    output_ref = (
        {"kind": "conversation", "id": result.conversation_id}
        if result.conversation_id
        else None
    )
    outcome = await finalize_and_rearm_backlog(
        BacklogRearmRequest(
            task_id=str(task.id),
            user_id=str(task.user_id),
            organization_id=str(task.organization_id),
            predecessor_run_id=str(run.id),
            claim_token=claim_token,
            recovery_key=result.recovery_key,
            due_at=result.rearm_at,
            result_summary=result.result_summary,
            error_message=result.error_message,
            output_ref=output_ref,
            result_metadata=result_metadata,
        )
    )
    if outcome.status in {"rearmed", "already_rearmed"}:
        return outcome

    await report_operational_failure(
        RuntimeError(
            f"backlog rearm refused with status={outcome.status}: "
            f"{outcome.reason or 'no reason supplied'}"
        ),
        operation="finalize_and_rearm_backlog",
        context={
            "run_id": str(run.id),
            "task_id": str(task.id),
            "status": outcome.status,
        },
    )
    return outcome


async def _dispatch_under_lease(
    hydrated: HydratedTask, run: SchRun, task: Any, claim_token: str, lease: RunLease
) -> AgentRunResult | None:
    """Run the kind dispatch in a child task beside the lease heartbeat.

    Whichever finishes first decides:

    * the handler returns -> the heartbeat is cancelled and the result flows
      to the normal finalize;
    * the heartbeat stops (``"deadline"`` -- max_runtime_seconds reached, or
      ``"lost"`` -- the row is no longer ours) -> the handler is CANCELLED and
      the run is finalized with the progress it reported. Before 2026-09-13
      an expired run's handler was left running as a zombie: real spend, real
      writes, and a final report nobody could persist.

    A cancellation of THIS task (worker shutdown) cancels both children and
    propagates; ``run_claimed_task`` finalizes with progress preserved.
    """
    handler = asyncio.create_task(
        _dispatch_by_kind(hydrated, run, claim_token), name=f"sch_run-handler-{run.id}"
    )
    heartbeat = asyncio.create_task(
        heartbeat_until_stopped(lease), name=f"sch_run-heartbeat-{run.id}"
    )
    try:
        done, _pending = await asyncio.wait(
            {handler, heartbeat}, return_when=asyncio.FIRST_COMPLETED
        )
    except asyncio.CancelledError:
        heartbeat.cancel()
        handler.cancel()
        # Give the handler its own cancel handling (the host's spine settle
        # etc.) before propagating ours; a second cancel arriving here is
        # re-raised by the bare ``raise`` below regardless.
        with contextlib.suppress(BaseException):
            await handler
        raise

    if handler in done:
        heartbeat.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await heartbeat
        return handler.result()

    # The heartbeat stopped first: the handler must not outlive its lease.
    stop = heartbeat.result()
    handler.cancel()
    try:
        await handler
    except asyncio.CancelledError:
        current = asyncio.current_task()
        if current is not None and current.cancelling():
            raise  # that was OUR cancellation, not the child's
    except Exception:  # noqa: BLE001 -- the handler's own error while being cancelled
        log.exception("run %s: handler raised while being stopped for %s", run.id, stop)

    if stop == "deadline":
        reason = (
            f"run ceiling reached: max_runtime_seconds={lease.max_runtime_seconds} elapsed; "
            "the handler was stopped. Raise the schedule's Max runtime if the approved "
            "budget needs more time"
        )
        log.error(
            "[scheduler-run-ceiling] run %s (task %s) hit max_runtime_seconds=%d with %d "
            "unit(s) committed; handler cancelled, progress preserved",
            run.id,
            task.id,
            lease.max_runtime_seconds,
            lease.units_done,
        )
    else:
        reason = f"lease lost mid-run: {lease.lost_reason or 'another worker owns this run'}"
        log.error(
            "[scheduler-lease-lost] run %s (task %s) lost its lease mid-run with %d unit(s) "
            "committed; handler cancelled so it does not zombie on",
            run.id,
            task.id,
            lease.units_done,
        )
    await _finalize_stopped_run(run, task, claim_token, lease, reason=reason)
    return None


# ── Kind dispatch ──────────────────────────────────────────────────────────


async def _dispatch_by_kind(
    hydrated: HydratedTask, run: SchRun, claim_token: str
) -> AgentRunResult | None:
    """
    Route a claimed task to the right runner based on ``task.kind``.

    Returns the runner's AgentRunResult on success, or ``None`` if the
    function finalized the run itself (e.g. no runner configured, raised
    exception, unsupported kind). Callers should treat ``None`` as "stop;
    everything already written".
    """
    task = hydrated.task
    kind = task.kind
    surface = get_ext("surface")

    if kind == "agent":
        return await _run_agent_kind(hydrated, run, claim_token)

    if kind == "tool":
        return await _run_tool_kind(hydrated, run, claim_token, surface)

    if kind == "ping":
        # Minimal end-to-end verification handler. Echoes basic metadata
        # so the FE shows the round-trip worked. No external calls.
        log.info(
            "ping handler responding for run=%s task=%s surface=%s",
            run.id,
            task.id,
            surface,
        )
        return AgentRunResult(
            success=True,
            result_summary=(f"pong from surface={surface} kind=ping task={task.id}"),
            metadata={
                "handled_by": "matrx-scheduler",
                "kind": "ping",
                "surface": surface,
                "task_id": task.id,
                "run_id": run.id,
            },
        )

    # Unknown kind -- finalize and bail. Don't raise; the scanner loop
    # would catch it but it's clearer in the run row.
    log.warning(
        "unsupported kind=%r on task=%s; finalizing run %s as failed",
        kind,
        task.id,
        run.id,
    )
    await queries.finalize_run(
        run.id,
        claim_token,
        status="failed",
        error_message=f"unsupported kind={kind!r}",
    )
    return None


async def _run_agent_kind(
    hydrated: HydratedTask, run: SchRun, claim_token: str
) -> AgentRunResult | None:
    """Original kind='agent' path: invoke host's agent_runner."""
    task = hydrated.task
    agent_task = hydrated.agent_task

    if agent_task is None or not (
        (agent_task.agent_id or "").strip() or (agent_task.mandate_key or "").strip()
    ):
        # Legacy/direct-DB rows can bypass the API's creation and enablement
        # validation. This is an invalid configuration, not a crashing host:
        # pause it at the package boundary before it can repeatedly dispatch
        # or enter the host's system-error repair queue. The pause is a
        # RECORDED suspension with an escalation, never a bare enabled=false:
        # a bare flip left the "learn" schedule off for 12 days with no alarm
        # anywhere (2026-09-16).
        reason = (
            "has no sch_agent_task row"
            if agent_task is None
            else "has neither agent_id nor mandate_key"
        )
        error_message = (
            f"kind='agent' task {task.id} {reason}; schedule was paused. "
            "Choose an agent or Mandate before enabling it again."
        )
        await suspend_schedule_now(
            task.id,
            run.id,
            error_message=error_message,
            reason=(
                "This schedule was paused on its first run because it has no agent or "
                "Mandate to run, so it can never succeed. Choose an agent or Mandate, "
                "then re-enable it."
            ),
        )
        await queries.finalize_run(
            run.id,
            claim_token,
            status="failed",
            error_message=error_message,
        )
        return None

    agent_runner = get_ext("agent_runner", required=False)
    if not agent_runner:
        await queries.finalize_run(
            run.id,
            claim_token,
            status="failed",
            error_message="agent_runner not configured in host",
        )
        return None

    agent_input = AgentRunInput(
        task_id=task.id,
        run_id=run.id,
        user_id=task.user_id,
        organization_id=task.organization_id,
        agent_id=agent_task.agent_id,
        mandate_key=agent_task.mandate_key,
        prompt=agent_task.prompt,
        variables=variables_for_run(agent_task.variables, run.metadata),
        persistent_conversation_id=agent_task.persistent_conversation_id,
        max_runtime_seconds=agent_task.max_runtime_seconds,
    )

    try:
        return await agent_runner(agent_input)
    except Exception as exc:
        log.exception("agent_runner raised for run %s", run.id)
        await queries.finalize_run(
            run.id, claim_token, status="failed", error_message=str(exc)[:2000]
        )
        return None


async def _run_tool_kind(
    hydrated: HydratedTask, run: SchRun, claim_token: str, surface: str
) -> AgentRunResult | None:
    """kind='tool' path: invoke host's tool_runner if registered, else fail clean."""
    task = hydrated.task
    agent_task = hydrated.agent_task

    if agent_task is None:
        # kind='tool' reuses sch_agent_task as the carrier (variables.tool_name
        # + variables.args + max_runtime_seconds) until a dedicated
        # sch_tool_task ships. A missing row means there's nothing to dispatch.
        await queries.finalize_run(
            run.id,
            claim_token,
            status="failed",
            error_message=(
                f"kind='tool' task {task.id} has no sch_agent_task row "
                f"(tool args live in variables.tool_name + variables.args); "
                "cannot dispatch"
            ),
        )
        return None

    tool_runner = get_ext("tool_runner", required=False)
    if not tool_runner:
        # Wake-hint receivers (matrx-extend, matrx-local) are expected to
        # register their own tool_runner. aidream itself usually doesn't
        # claim tool-kind tasks -- they're routed via wake hints to the
        # surface that owns the capability.
        await queries.finalize_run(
            run.id,
            claim_token,
            status="failed",
            error_message=(
                f"kind='tool' has no tool_runner registered on this host "
                f"(surface={surface}). Wire one via matrx_scheduler."
                f"configure(..., tool_runner=...) at startup."
            ),
        )
        return None

    # Tool args are conventionally stashed in agent_task.variables for now
    # (we reuse the existing child table until a sch_tool_task lands).
    tool_input = ToolRunInput(
        user_id=task.user_id,
        tool_name=agent_task.variables.get("tool_name", ""),
        args=agent_task.variables.get("args", {}),
        max_runtime_seconds=agent_task.max_runtime_seconds,
        task_id=task.id,
        run_id=run.id,
    )

    if not tool_input.tool_name:
        await queries.finalize_run(
            run.id,
            claim_token,
            status="failed",
            error_message=("kind='tool' missing tool_name in agent_task.variables.tool_name"),
        )
        return None

    try:
        return await tool_runner(tool_input)
    except Exception as exc:
        log.exception("tool_runner raised for run %s", run.id)
        await queries.finalize_run(
            run.id, claim_token, status="failed", error_message=str(exc)[:2000]
        )
        return None
