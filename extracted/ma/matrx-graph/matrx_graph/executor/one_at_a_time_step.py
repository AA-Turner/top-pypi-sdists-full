"""The scheduler's half of one at a time per key (``data.one_at_a_time``): take the turn, give it back.

Called from ``Scheduler._execute_invocation_body`` once per invocation (after ``node_started``,
before the executor's first attempt) and cleaned up by ``Scheduler._execute_invocation``:

* :func:`take_turn` — waits while another invocation holds this key's turn (saying so on the step
  and in the run log), then holds it, renewing the lease while the step works. It ends the wait
  WITHOUT the turn — setting ``slot.error`` (a :class:`TurnNotTaken`, never retried), so the step
  fails loudly instead of running unguarded — when:
    - the run is being CANCELLED (checked every poll; the run then ends cancelled);
    - the wait passes the ``workflow.one_at_a_time.max_wait_seconds`` knob (this also ends two runs
      waiting on each other in opposite order);
    - the turn is already held by this step's own caller chain (a ``subgraph.call`` child asking for
      the turn its parent step holds would wait forever) — ``engine.one_at_a_time_self_wait``.
  A PAUSE does not end the wait: like any working step, the run pauses when the step ends; the step
  says so. The max wait bounds it.
* :func:`end_turn` — always (``finally``): stops the renewer and gives the turn back. A turn whose
  claim was still being written when the step was cancelled is awaited first (the claim is shielded),
  so a cancel never leaves an orphan turn.

The turn does NOT survive a pause or a question (``control.human_input`` inside the held unit raises an
interrupt; the step ends and gives the turn back). On resume the step takes its turn again, waiting if
another run has it now. Holding a turn across a wait for a person could block every other run forever.

The store owns every compare-and-swap (``matrx_graph.once.acquire`` with ``bypass=True``: a turn
never reads or writes a result). See ``matrx_graph/one_at_a_time.py`` for the rules.
"""

from __future__ import annotations

import asyncio
import contextvars
import logging
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any, Literal

from matrx_graph.errors import ExecutionError
from matrx_graph.once import Claim, ClaimPosition, StepResultKey, Wait, acquire, get_step_result_store
from matrx_graph.one_at_a_time import turn_key, turn_step_type

if TYPE_CHECKING:
    from matrx_graph.executor.scheduler import Invocation, Scheduler

logger = logging.getLogger(__name__)

WAITING_LABEL = "engine.waiting_turn"
UNAVAILABLE_LABEL = "engine.one_at_a_time_unavailable"
SELF_WAIT_LABEL = "engine.one_at_a_time_self_wait"
LOST_TURN_LABEL = "engine.one_at_a_time_lost_turn"

#: The turns held by THIS task's caller chain (a step and every child run it awaits inline inherit
#: it). A key in here asked for again is a self-wait, never a wait.
_HELD_TURNS: contextvars.ContextVar[frozenset[StepResultKey]] = contextvars.ContextVar(
    "matrx_graph_one_at_a_time_held", default=frozenset()
)

TurnStopReason = Literal["cancelled", "max_wait", "self_wait"]


class TurnNotTaken(ExecutionError):
    """The step ended its wait without the turn. Never retried (``_NON_RETRYABLE_ERROR_TYPES``)."""

    def __init__(self, reason: TurnStopReason, message: str) -> None:
        super().__init__(message)
        self.reason = reason
        self.person_message = message
        self.node_error_details = {"one_at_a_time": reason}


@dataclass(slots=True)
class TurnSlot:
    """Per-invocation state, created by ``Scheduler._execute_invocation``."""

    decided: bool = False
    claim: Claim | None = None
    waited_for: str | None = None
    error: TurnNotTaken | None = None
    acquiring: asyncio.Task[Any] | None = None
    held_token: contextvars.Token[frozenset[StepResultKey]] | None = None


def waiting_says(holder_run_id: str | None, same_run: bool) -> str:
    """The one sentence a waiting step shows."""
    if same_run:
        return "Waiting its turn: another item of this run is working on the same thing. It starts when that finishes."
    who = f"run {holder_run_id[:8]}" if holder_run_id else "another run"
    return f"Waiting its turn: {who} is working on the same thing. It starts when that finishes."


async def _flag(scheduler: Scheduler, run_id: str, invocation: Invocation, *, step: int,
                attempt: int, label: str, message: str, payload: dict[str, Any] | None = None) -> None:
    await scheduler._raise_review(
        run_id, invocation, step=step, attempt=attempt, label=label, message=message,
        category="unexpected_path", payload=payload,
    )


def _scope_id(scheduler: Scheduler, scope: str, run_id: str, organization_id: str) -> str | None:
    if scope == "run":
        return run_id
    if scope == "organization":
        return organization_id
    return scheduler.definition_id or None


async def _say_waiting(scheduler: Scheduler, ctx: Any, run_id: str, invocation: Invocation, *,
                       step: int, attempt: int, holder: ClaimPosition | None) -> None:
    from matrx_graph import run_log

    same_run = holder is not None and holder.run_id == run_id
    message = waiting_says(holder.run_id if holder else None, same_run)
    if ctx is not None:
        await ctx.progress(message)
    try:
        await run_log.write_run_log(
            run_id=run_id, node_id=invocation.node_id, step=step, attempt=attempt,
            label=WAITING_LABEL, message=message, severity="info",
            payload={"holder_run_id": holder.run_id if holder else None,
                     "holder_step": holder.node_id if holder else None},
            organization_id=str(getattr(scheduler.app, "organization_id", "") or "") or None,
            user_id=str(getattr(scheduler.app, "user_id", "") or "") or None,
            occurrence_key=f"{invocation.node_id}:{invocation.dispatch_id}:{invocation.item_index}:{step}:waiting",
        )
    except Exception:  # noqa: BLE001 — saying so is best-effort; the log line below always lands
        logger.exception("[wf:%s node=%s] could not record the waiting line", run_id[:8], invocation.node_id)
    logger.info("[wf:%s node=%s] %s", run_id[:8], invocation.node_id, message)


async def _renew_forever(claim: Claim, lease_seconds: int, on_lost: Callable[[], Awaitable[None]]) -> None:
    store = get_step_result_store()
    interval = max(lease_seconds / 3.0, 0.05)
    while True:
        await asyncio.sleep(interval)
        try:
            ok = await store.renew(
                claim.key, token=claim.token,
                lease_until=datetime.now(UTC) + timedelta(seconds=lease_seconds),
            )
        except Exception:  # noqa: BLE001 — keep trying; the lease is the safety net
            logger.exception("[wf one-at-a-time] renewing the turn on %s failed", claim.key.step_type)
            continue
        if not ok:
            logger.error(
                "[wf one-at-a-time] LOST the turn on %s key %s — its lease ran out and another run "
                "took it. This step keeps working, so two may now overlap.",
                claim.key.step_type, claim.key.result_key[:12],
            )
            try:
                await on_lost()
            except Exception:  # noqa: BLE001 — the log line above already landed
                logger.exception("[wf one-at-a-time] could not flag the lost turn")
            return


async def _acquire_once(store: Any, key: StepResultKey, position: ClaimPosition, lease_seconds: int,
                        slot: TurnSlot, on_lost: Callable[[], Awaitable[None]]) -> Claim | Wait:
    """One acquire; a Claim is recorded on the slot and its renewer started in the SAME uncancellable
    unit (the caller shields this), so a cancel can never leave a claim nobody gives back."""
    decision = await acquire(store, key, digest="", position=position, lease_seconds=lease_seconds,
                             reuse_changed=False, bypass=True)
    if isinstance(decision, Claim):
        slot.claim = decision
        decision.renewer = asyncio.create_task(
            _renew_forever(decision, lease_seconds, on_lost), name=f"wf-turn-lease:{position.node_id}",
        )
        return decision
    assert isinstance(decision, Wait)  # bypass=True never returns a Hit
    return decision


async def take_turn(
    scheduler: Scheduler,
    slot: TurnSlot,
    *,
    run_id: str,
    step: int,
    attempt: int,
    invocation: Invocation,
    node: Any,
    ctx: Any,
    inputs: dict[str, Any],
) -> None:
    """Hold this key's turn before the step works (waiting for it if needed), or set ``slot.error``.
    A missing key part or a broken store runs the step without a turn and flags it."""
    from matrx_graph.knobs import once_knobs, one_at_a_time_knobs

    slot.decided = True
    policy = node.one_at_a_time
    organization_id = str(getattr(scheduler.app, "organization_id", "") or "")
    if not organization_id:
        await _flag(scheduler, run_id, invocation, step=step, attempt=attempt, label=UNAVAILABLE_LABEL,
                    message="One at a time could not apply: the run has no organization; the step ran")
        return
    scope_id = _scope_id(scheduler, policy.scope, run_id, organization_id)
    if not scope_id:
        await _flag(scheduler, run_id, invocation, step=step, attempt=attempt, label=UNAVAILABLE_LABEL,
                    message=f"One at a time could not apply: scope '{policy.scope}' has no id in this run; the step ran")
        return
    key_value, missing = turn_key(policy, inputs)
    if key_value is None:
        await _flag(scheduler, run_id, invocation, step=step, attempt=attempt, label=UNAVAILABLE_LABEL,
                    message=f"One at a time could not build a key: missing {', '.join(missing)}; the step ran",
                    payload={"missing": missing})
        return
    key = StepResultKey(
        organization_id=organization_id, scope=policy.scope, scope_id=str(scope_id),
        step_type=turn_step_type(policy, invocation.node_id), result_key=key_value,
    )
    if key in _HELD_TURNS.get():
        message = ("This step asks for a turn its own caller already holds (a sub-workflow inside the "
                   "step that holds it); it would wait forever, so it stopped. Give the inner step "
                   "another name, or take the turn on only one of them.")
        await _flag(scheduler, run_id, invocation, step=step, attempt=attempt, label=SELF_WAIT_LABEL,
                    message=message, payload={"turn": key.step_type})
        slot.error = TurnNotTaken("self_wait", message)
        return

    async def on_lost() -> None:
        await _flag(scheduler, run_id, invocation, step=step, attempt=attempt, label=LOST_TURN_LABEL,
                    message=("This step lost its turn while working (its lease ran out and another run "
                             "took it), so two runs may have worked on the same thing at once"),
                    payload={"turn": key.step_type})

    once = await once_knobs()
    max_wait = (await one_at_a_time_knobs()).max_wait_seconds
    store = get_step_result_store()
    position = ClaimPosition(run_id=run_id, node_id=invocation.node_id,
                             dispatch_id=invocation.dispatch_id, item_index=invocation.item_index)
    started = time.monotonic()
    said_pause = False
    while True:
        task = asyncio.ensure_future(_acquire_once(store, key, position, once.lease_seconds, slot, on_lost))
        slot.acquiring = task
        try:
            decision = await asyncio.shield(task)
        except asyncio.CancelledError:
            raise  # end_turn awaits the shielded task and gives back whatever it took
        except Exception as exc:  # noqa: BLE001 — the store is down: work rather than block the run
            logger.exception("[wf:%s node=%s] one at a time: the store failed", run_id[:8], invocation.node_id)
            await _flag(scheduler, run_id, invocation, step=step, attempt=attempt, label=UNAVAILABLE_LABEL,
                        message=f"One at a time could not reach its turns ({type(exc).__name__}); the step ran",
                        payload={"error": f"{type(exc).__name__}: {str(exc)[:300]}"})
            return
        finally:
            if task.done():
                slot.acquiring = None
        if isinstance(decision, Claim):
            slot.held_token = _HELD_TURNS.set(_HELD_TURNS.get() | {key})
            if slot.waited_for is not None and ctx is not None:
                await ctx.progress("Its turn: starting now.")
            return
        holder_run = decision.holder.run_id if decision.holder else None
        if slot.waited_for != (holder_run or "?"):
            slot.waited_for = holder_run or "?"
            await _say_waiting(scheduler, ctx, run_id, invocation, step=step, attempt=attempt,
                               holder=decision.holder)
        pause_now, cancel_now = await scheduler._poll_controls()
        if cancel_now:
            slot.error = TurnNotTaken("cancelled", "The run was cancelled while this step waited its turn.")
            return
        if pause_now and not said_pause and ctx is not None:
            said_pause = True
            await ctx.progress("Pause asked: the run pauses when this step ends (it is waiting its turn).")
        waited = time.monotonic() - started
        if waited >= max_wait:
            who = f"run {holder_run[:8]}" if holder_run else "another run"
            slot.error = TurnNotTaken(
                "max_wait",
                f"Waited {int(waited)} s for its turn behind {who} (the limit is {max_wait} s) and stopped "
                "without working. Retry once that run has finished.",
            )
            return
        try:
            await store.wait(key, float(min(once.wait_poll_seconds, max(max_wait - waited, 0.05))))
        except Exception as exc:  # noqa: BLE001
            await _flag(scheduler, run_id, invocation, step=step, attempt=attempt, label=UNAVAILABLE_LABEL,
                        message=f"One at a time could not wait for its turn ({type(exc).__name__}); the step ran",
                        payload={"error": f"{type(exc).__name__}: {str(exc)[:300]}"})
            return


async def end_turn(slot: TurnSlot) -> None:
    """Stop the renewer and give the turn back. Never raises."""
    pending, slot.acquiring = slot.acquiring, None
    if pending is not None and not pending.done():
        # Cancelled mid-claim: the shielded claim finishes, then is given back below.
        await asyncio.wait({pending})
    token, slot.held_token = slot.held_token, None
    if token is not None:
        try:
            _HELD_TURNS.reset(token)
        except ValueError:  # another context — nothing of ours to undo there
            pass
    claim, slot.claim = slot.claim, None
    if claim is None:
        return
    renewer, claim.renewer = claim.renewer, None
    if renewer is not None:
        renewer.cancel()
        await asyncio.wait({renewer})
    try:
        await get_step_result_store().release(claim.key, token=claim.token)
    except Exception:  # noqa: BLE001 — the lease runs out on its own
        logger.exception("[wf one-at-a-time] giving the turn back failed; its lease will run out")
