"""Sequential whole-chunk execution; native controllers hold while inference waits."""

from __future__ import annotations

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np

from dreamscale.policy.run_loop import (
    _accepted_action,
    _act_done,
    _call_user_callback,
    _timing_event_from_result,
)
from dreamscale.policy.runtime.action_smoothing import validate_normalized_grippers
from dreamscale.policy.runtime.contract import resolve_runtime_contract
from dreamscale.policy.telemetry import RunTelemetryAccumulator, publish_run_summary
from dreamscale.policy.types import (
    ActionEvent,
    BufferEvent,
    ChunkEvent,
    DispatchEvent,
    MergeEvent,
    QueueMergeEvent,
    RequestEvent,
    RunContext,
    RunHooks,
    RunResult,
)


def validate_mode(mode, strategy):
    if mode not in ("async", "sync"):
        raise ValueError("mode must be async or sync")
    if mode == "sync" and (
        strategy.action_smoothing != "auto"
        or strategy.smoothing_new_weight is not None
        or strategy.smoothing_correction_steps is not None
        or strategy.smoothing_reference_speed is not None
    ):
        raise ValueError("Sync executes raw chunks; smoothing options require --mode async.")


async def run_sync(
    *, policy, instruction, observe, act, strategy, max_actions, hooks=None,
    execution_contract=None,
):
    """Execute qualified prefixes without prefetch or smoothing; runner owns cleanup."""
    if max_actions is not None and (type(max_actions) is not int or max_actions < 1):
        raise ValueError("max_actions must be a positive integer or None")
    contract = execution_contract or resolve_runtime_contract(
        model=policy.model,
        resolved_config=getattr(policy, "resolved_optimization_config", None),
        action_hz_override=strategy.action_hz,
        chunk_size_override=strategy.chunk_size,
        control_hz=getattr(policy, "action_hz", None),
        deployment=getattr(policy, "deployment", None),
    )
    if execution_contract is not None and (
        strategy.action_hz not in (None, contract.action_hz)
        or strategy.chunk_size not in (None, contract.chunk_size)
    ):
        raise ValueError("strategy must match the adapter's execution contract")
    execution_size = contract.execution_chunk_size
    # An episode history counts the robot's executed actions (InternW0-Δ): each request
    # carries the episode's first frames and those that many actions back. Sync observes
    # once per chunk, so that frame is a previous request's observation.
    history = getattr(policy, "observation_history", None)
    episode = history if callable(getattr(history, "executed", None)) else None
    if episode is not None:
        episode.clear()
    hooks = hooks or RunHooks()
    telemetry = RunTelemetryAccumulator()
    executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="attended-sync")
    started = time.monotonic()
    completed = attempts = calls = 0
    startup_wait_ms = 0.0
    failure = None
    prepared_owner = None
    reason = "action_limit"

    def emit(name, event):
        callback = getattr(hooks, name)
        if callback is not None:
            callback(event)

    def context(observation_id, remaining=0):
        return RunContext(completed, observation_id, remaining, False, time.monotonic() - started)

    try:
        if getattr(policy, "requires_task_preparation", False):
            owner = getattr(policy, "remote", policy)
            prepare_managed = getattr(owner, "_prepare_task", None)
            if callable(prepare_managed):
                await prepare_managed(instruction=instruction, managed=True)
                prepared_owner = owner
            else:
                await policy.prepare(instruction=instruction)
        while max_actions is None or completed < max_actions:
            observation = await _call_user_callback(observe, context(calls), executor=executor)
            submitted = time.monotonic_ns()
            emit("on_request", RequestEvent(submitted, completed, 0, observation))
            emit("on_buffer", BufferEvent(completed, 0, execution_size, "waiting", True))
            calls += 1
            request = observation
            if episode is not None:
                request = episode.window(observation)
                episode.push(observation)
            chunk = await policy.predict(
                request, instruction=instruction, timeout_s=strategy.timeout_s
            )
            received = time.monotonic_ns()
            # Validate the entire qualified prefix, including rows beyond a run limit.
            # A checkpoint may generate an unqualified tail which must never be queued.
            if len(chunk.actions) != contract.chunk_size:
                raise ValueError("Sync prediction must be a complete generated action chunk.")
            values = np.asarray(chunk.actions[:execution_size])
            if (
                values.shape != (execution_size, contract.action_dim)
                or values.dtype.kind not in "fiu"
                or not np.isfinite(values).all()
            ):
                raise ValueError("Sync prediction must be a complete finite action chunk.")
            if chunk.action_indices is not None and (
                len(chunk.action_indices) != contract.chunk_size
                or tuple(chunk.action_indices[:execution_size]) != tuple(range(execution_size))
            ):
                raise ValueError(
                    "Sync prediction must contain consecutive actions from index zero."
                )
            actions = tuple(tuple(float(v) for v in row) for row in values)
            for action in actions:
                validate_normalized_grippers(action, contract.normalized_gripper_indices)
            timing = _timing_event_from_result(chunk)
            telemetry.record(timing)
            emit("on_timing", timing)
            event = ChunkEvent(
                chunk.observation_id,
                chunk.chunk_id,
                completed,
                completed,
                actions,
                tuple(range(len(actions))),
            )
            emit("on_chunk", event)
            emit(
                "on_merge",
                MergeEvent(
                    chunk.observation_id,
                    chunk.chunk_id,
                    completed,
                    completed,
                    "none",
                    "none",
                    None,
                    None,
                    0,
                    0,
                    len(actions),
                    0,
                    0,
                    0.0,
                ),
            )
            emit(
                "on_queue_merge",
                QueueMergeEvent(
                    submitted,
                    received,
                    event,
                    (),
                    (),
                    tuple(enumerate(actions, completed)),
                ),
            )
            if completed == 0:
                startup_wait_ms = (time.monotonic() - started) * 1000
            for offset, action in enumerate(actions):
                if max_actions is not None and completed >= max_actions:
                    break
                remaining = len(actions) - offset - 1
                emit("on_action", ActionEvent(completed, False, remaining, action))
                dispatch_start = time.monotonic_ns()
                attempts += 1
                result = await _call_user_callback(
                    act,
                    action,
                    context(chunk.observation_id, remaining),
                    executor=executor,
                )
                accepted = _accepted_action(result, action)
                emit(
                    "on_dispatch",
                    DispatchEvent(
                        completed, False, action, accepted, dispatch_start, time.monotonic_ns()
                    ),
                )
                completed += 1
                if episode is not None:
                    episode.executed()
                emit(
                    "on_buffer",
                    BufferEvent(
                        completed,
                        remaining,
                        execution_size,
                        "ok" if remaining else "empty",
                        False,
                    ),
                )
                if _act_done(result):
                    reason = "act_callback"
                    break
                # Pace every command, including chunk boundaries; late callbacks never catch up.
                delay = max(
                    0.0, 1 / contract.action_hz - (time.monotonic_ns() - dispatch_start) / 1e9
                )
                await asyncio.sleep(delay if strategy.real_time else 0)
            if reason == "act_callback":
                break
    except BaseException as exc:
        failure = exc
        reason = (
            "interrupted"
            if isinstance(exc, (asyncio.CancelledError, KeyboardInterrupt))
            else "error"
        )
        raise
    finally:
        # Drain an in-progress bounded hardware callback before runner cleanup takes ownership.
        executor.shutdown(wait=True, cancel_futures=True)
        if prepared_owner is not None:
            prepared_owner._prepared_run_active = False
        summary = RunResult(
            actions=completed,
            policy_calls=calls,
            underruns=0,
            done=reason == "act_callback",
            elapsed_s=time.monotonic() - started,
            max_actions=max_actions,
            stop_reason=reason,
            timing=telemetry.summary(),
            model=policy.model,
            region=getattr(policy, "region", None),
            transport_mode=getattr(policy, "transport_mode", None),
            fallback_reason=getattr(policy, "fallback_reason", None),
            startup_wait_ms=startup_wait_ms,
            action_attempts=attempts,
            error_type=type(failure).__name__ if failure else None,
        )
        publish_run_summary(policy, hooks, summary, preserve_error=failure is not None)
    return summary
