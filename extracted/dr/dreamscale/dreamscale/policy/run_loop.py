from __future__ import annotations

import asyncio
import inspect
import time
from collections import deque
from collections.abc import Awaitable, Callable, Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from functools import partial
from itertools import count
from math import ceil, isfinite
from numbers import Real
from typing import Any

from dreamscale import errors
from dreamscale.model_names import public_model
from dreamscale.policy.config import ResolvedOptimizationConfig
from dreamscale.policy.runtime.action_buffer import ActionBuffer
from dreamscale.policy.runtime.action_smoothing import (
    ResolvedActionSmoothing,
    resolve_action_smoothing,
)
from dreamscale.policy.runtime.contract import RuntimeContract, resolve_runtime_contract
from dreamscale.policy.runtime.control import (
    METHOD_O_PROFILES,
    EagerRefillQueueConfig,
    MethodOConfig,
    MethodOController,
    control_config_for_name,
)
from dreamscale.policy.runtime.rtc import (
    DYNAMIC_FULL_HORIZON_RTC_CONTRACT_ID,
    LATE_BOUND_PREFIX_RTC_CONTRACT_ID,
    RtcConfig,
    RtcDelayEstimator,
    RtcProfileSet,
    build_late_bound_prefix_rtc_request,
    build_rtc_context_for_queue,
    build_rtc_estimator_state_from_calibration,
    build_rtc_profile_set,
    late_bound_prefix_rows,
    select_static_rtc_profile_name,
)
from dreamscale.policy.telemetry import RunTelemetryAccumulator, publish_run_summary
from dreamscale.policy.types import (
    ActionChunkResult,
    ActionEvent,
    ActResult,
    BufferEvent,
    ChunkEvent,
    DispatchEvent,
    MergeEvent,
    PolicyStepResult,
    PolicyTimingEvent,
    QueueMergeEvent,
    RequestEvent,
    RunContext,
    RunHooks,
    RunResult,
    RunStrategy,
    RuntimeStats,
)

# run() refuses a contract whose actions have no hold.
NO_HOLD_RUN_MESSAGE = (
    "this deployment's actions aren't joint targets, so run() can't hold the robot while "
    "it waits for one; drive it with policy.next_action(...) or policy.predict(...)"
)


WAIT_RUN_MESSAGE = (
    "this deployment waits for each chunk and runs it from its first action, so run() "
    "can't command every tick while one is computed; drive it with policy.next_action(...) "
    "(which waits for the chunk) or policy.predict(...)"
)


def require_run_hold(contract: RuntimeContract) -> None:
    """run() commands an action every tick, holding when none has arrived. A π0.5
    deployment acting in its model's own space has no hold, and a contract that waits for
    each chunk (InternW0-Δ) must not have its plan advanced by the wait: they run with
    next_action (which waits for the real action) or predict, never run()."""
    if contract.action_space == "model_defined":
        raise ValueError(NO_HOLD_RUN_MESSAGE)
    if contract.hold_behavior == "wait":
        raise ValueError(WAIT_RUN_MESSAGE)


async def run_policy_loop(
    *,
    instruction: str,
    policy: Any,
    observe: Callable[[RunContext], Any | Awaitable[Any]],
    act: Callable[
        [Sequence[float], RunContext],
        ActResult | bool | None | Awaitable[ActResult | bool | None],
    ],
    read_hold_action: Callable[
        [RunContext], Sequence[float] | Awaitable[Sequence[float]]
    ]
    | None = None,
    max_actions: int | None,
    strategy: RunStrategy | None = None,
    hooks: RunHooks | None = None,
    execution_contract: RuntimeContract | None = None,
) -> RunResult:
    if max_actions is not None and (type(max_actions) is not int or max_actions < 1):
        raise ValueError("max_actions must be a positive integer or None")
    run_started = time.monotonic()
    strategy = strategy or RunStrategy()
    hooks = hooks or RunHooks()
    contract = execution_contract or resolve_runtime_contract(
        model=getattr(policy, "model", None),
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
    require_run_hold(contract)
    action_smoothing = resolve_action_smoothing(strategy, contract)
    chunk_size = contract.execution_chunk_size
    period_s = 1.0 / contract.action_hz
    started = run_started
    action_started = started
    action_queue = ActionBuffer(next_action_step=0)
    planner = _ReplanPlanner(
        control=getattr(policy, "control", "adaptive"),
        control_hz=contract.action_hz,
        chunk_size=chunk_size,
        action_dim=contract.action_dim,
        explicit_threshold=strategy.replan_at_remaining,
        resolved_config=getattr(policy, "resolved_optimization_config", None),
        action_smoothing=action_smoothing,
        late_bound_rows=late_bound_prefix_rows(getattr(policy, "deployment", None)),
        min_replan_steps=contract.min_replan_steps,
    )
    pending: _PendingRequest | None = None
    last_action: tuple[float, ...] | None = None
    last_observation: Any | None = None
    calibrated = False
    policy_calls = 0
    underruns = 0
    observation_id = 0
    executed_history: deque[tuple[float, ...]] = deque(maxlen=2)
    # Accepted actions of recent ticks, for checkpoints that condition on them.
    action_history: deque[tuple[float, ...]] = deque(maxlen=contract.action_history)
    accepted_events: list[_AcceptedChunkEvents] = []
    telemetry = RunTelemetryAccumulator()
    completed_actions = action_attempts = startup_holds = execution_underruns = 0
    first_dispatch_at: float | None = None
    first_dispatch_unix_ns: int | None = None
    hold_latch: tuple[float, ...] | None = None
    # Since when the robot has held (stalled steps), for measured history windows.
    held_since: float | None = None
    startup_wait_ms = 0.0
    stop_reason = "action_limit"
    failure: BaseException | None = None
    # YAM's first prediction is made while stationary. Keep its complete
    # horizon, then give motion 100 ms before capturing observation two.
    measured_bootstrap = contract.measured_bootstrap
    startup_delay_s = contract.startup_motion_delay_s if strategy.real_time else 0.0
    callback_executor = ThreadPoolExecutor(
        max_workers=1,
        thread_name_prefix="dreamscale-run-callback",
    )
    # Windowed sessions: observations of the ticks before each request (history frames):
    # Isaac context the last two ticks, FLUX 3 Action SO-101 the tick 7 before (DSL-182).
    history = getattr(policy, "observation_history", None)
    if history is not None:
        history.clear()

    async def observe_for_history(action_index: int) -> None:
        """Observe on the ticks before a planned request, for its history frames. A measured
        window (FLUX deployments) takes every tick: a request may start before the planned
        one, and its window must still find each tick measured."""
        remaining = action_queue.actions_remaining(action_index)
        if history.state_steps or any(
            planner.should_replan(remaining - step) for step in history.observe_steps
        ):
            push = getattr(policy, "push_history", None) or history.push
            await _maybe_await(push(await _call_user_callback(
                observe,
                RunContext(
                    action_index=action_index,
                    observation_id=observation_id,
                    actions_remaining=remaining,
                    stalled=False,
                    elapsed_s=time.monotonic() - started,
                ),
                executor=callback_executor,
            )))

    async def start_request(action_index: int) -> _PendingRequest:
        nonlocal calibrated, last_observation, observation_id
        actions_remaining = action_queue.actions_remaining(action_index)
        ctx = RunContext(
            action_index=action_index,
            observation_id=observation_id,
            actions_remaining=actions_remaining,
            stalled=False,
            elapsed_s=time.monotonic() - started,
        )
        observation_id += 1
        observation = await _call_user_callback(
            observe,
            ctx,
            executor=callback_executor,
        )
        request_observation = observation
        if history is not None:
            if held_since is not None:
                # The robot has held since then: measured windows repeat its held tick.
                history.hold(held_since, time.monotonic())
            request_observation = history.window(observation)
            history.push(observation)
        if measured_bootstrap and policy_calls == 1 and first_dispatch_unix_ns is not None:
            _validate_startup_observation(observation, first_dispatch_unix_ns)
        last_observation = observation
        if not calibrated:
            profile = await _maybe_calibrate_policy(
                policy=policy,
                observation=observation,
                instruction=instruction,
                timeout_s=strategy.timeout_s,
            )
            if profile is not None:
                planner.seed_calibration(profile)
            calibrated = True
        rtc_context = planner.build_rtc_context(action_queue)
        submitted_at_ns = time.monotonic_ns()
        if hooks.on_request is not None:
            hooks.on_request(RequestEvent(
                submitted_at_ns, action_index, actions_remaining, observation,
            ))
        task = _create_predict_task(
            policy=policy,
            observation=request_observation,
            instruction=instruction,
            timeout_s=strategy.timeout_s,
            actions_remaining=actions_remaining,
            base_action_index=action_index,
            planner=planner,
            rtc_context=rtc_context,
            action_history=tuple(action_history),
        )
        return _PendingRequest(
            base_action_index=action_index,
            actions_remaining_at_submit=actions_remaining,
            task=task,
            rtc_context=rtc_context,
            submitted_at_ns=submitted_at_ns,
        )

    def can_replan() -> bool:
        if not startup_delay_s or policy_calls > 1:
            return True
        if first_dispatch_at is None:
            return False
        return time.monotonic() - first_dispatch_at >= startup_delay_s

    def accept(
        request: _PendingRequest,
        result: ActionChunkResult,
    ) -> _AcceptedChunkEvents:
        nonlocal policy_calls
        elapsed_request_steps = ceil(
            max(0, time.monotonic_ns() - request.submitted_at_ns)
            * contract.action_hz
            / 1_000_000_000.0
        )
        merge_telemetry = planner.record_merge_delay(
            action_queue=action_queue,
            base_action_index=request.base_action_index,
            actions_remaining_at_submit=request.actions_remaining_at_submit,
            rtc_context=request.rtc_context,
            elapsed_request_steps=elapsed_request_steps,
        )
        _record_rtc_merge_stats(policy, merge_telemetry)
        accepted_action_index = action_queue.next_action_step
        chunk_event = _chunk_event_from_result(
            result=result,
            base_action_index=request.base_action_index,
            accepted_action_index=accepted_action_index,
            chunk_size=chunk_size,
        )
        before = action_queue.snapshot() if hooks.on_queue_merge else ()
        before_raw = action_queue.snapshot(raw=True) if hooks.on_queue_merge else ()
        merge_diagnostics = planner.accept_chunk(
            action_queue=action_queue,
            base_action_index=request.base_action_index,
            result=result,
            executed_history=tuple(executed_history),
        )
        merge_event = _merge_event_from_diagnostics(
            result=result,
            base_action_index=request.base_action_index,
            accepted_action_index=accepted_action_index,
            diagnostics=merge_diagnostics,
        )
        _record_rtc_reference_stats(
            policy,
            rtc_context=request.rtc_context,
            result=result,
        )
        policy_calls += 1
        _record_stats(policy, chunks_received=1)
        planner.record_result(
            result,
            actions_remaining_at_submit=request.actions_remaining_at_submit,
        )
        timing_event = _timing_event_from_result(result)
        telemetry.record(timing_event)
        return _AcceptedChunkEvents(
            timing=timing_event,
            chunk=chunk_event,
            merge=merge_event,
            queue=QueueMergeEvent(
                request.submitted_at_ns, time.monotonic_ns(), chunk_event,
                before, before_raw, action_queue.snapshot(),
            ) if hooks.on_queue_merge else None,
        )

    async def finish_ready_request() -> None:
        nonlocal pending
        if pending is not None and pending.task.done():
            accepted_events.append(accept(pending, pending.task.result()))
            pending = None

    def emit_accepted_events() -> None:
        events = tuple(accepted_events)
        accepted_events.clear()
        for event in events:
            if hooks.on_chunk is not None:
                hooks.on_chunk(event.chunk)
            if hooks.on_merge is not None:
                hooks.on_merge(event.merge)
            if hooks.on_timing is not None:
                hooks.on_timing(event.timing)
            if hooks.on_queue_merge is not None and event.queue is not None:
                hooks.on_queue_merge(event.queue)

    def emit_buffer(action_index: int, *, remaining_at: int | None = None) -> None:
        if hooks.on_buffer is None:
            return
        remaining = action_queue.actions_remaining(
            action_index if remaining_at is None else remaining_at
        )
        in_flight = pending is not None
        hooks.on_buffer(
            BufferEvent(
                action_index=action_index,
                remaining=remaining,
                capacity=chunk_size,
                health=_buffer_health(
                    remaining=remaining,
                    capacity=chunk_size,
                    in_flight=in_flight,
                ),
                in_flight=in_flight,
            )
        )

    try:
        pending = await start_request(0)
        started = action_started = time.monotonic()
        if not strategy.real_time or measured_bootstrap:
            stale_first_chunks = 0
            while True:
                first_result = await pending.task
                if (
                    measured_bootstrap
                    and contract.hold_behavior == "current_position"
                    and not executed_history
                ):
                    if read_hold_action is not None:
                        anchor = await _call_user_callback(
                            read_hold_action,
                            RunContext(0, 0, 0, True, time.monotonic() - started),
                            executor=callback_executor,
                        )
                    else:
                        anchor = _hold_position_action(
                            contract=contract, observation=last_observation, last_action=None,
                        )
                    if contract.action_dim is not None:
                        anchor = _validate_hold_action(anchor, action_dim=contract.action_dim)
                    executed_history.append(tuple(anchor))
                submitted_at_ns = pending.submitted_at_ns
                accepted_events.append(accept(pending, first_result))
                pending = None
                if measured_bootstrap and not action_queue.actions_remaining():
                    # The chunk indexed every action past step 0 (an engine fault): not a
                    # reason to abort a run that has not moved yet. Ask again; three in a
                    # row mean the model cannot start at the current step.
                    stale_first_chunks += 1
                    _record_stats(policy, stale_chunks_dropped=1)
                    if stale_first_chunks >= STALE_FIRST_CHUNKS_BEFORE_RAISE:
                        raise StaleFirstChunkError(
                            elapsed_s=max(0.0, time.monotonic_ns() - submitted_at_ns) / 1e9,
                            horizon_s=contract.horizon_s,
                            model=getattr(policy, "model", None),
                        )
                    # Nothing of the rejected chunk may blend into the real plan.
                    action_queue = ActionBuffer(next_action_step=action_queue.next_action_step)
                    ready_in = _send_ready_in(policy)
                    if ready_in > 0.0:
                        await asyncio.sleep(ready_in)  # observe after the floor, not before
                    pending = await start_request(action_queue.next_action_step)
                    continue
                break
            action_started = time.monotonic()
            startup_wait_ms = (action_started - run_started) * 1000.0

        for action_index in (count() if max_actions is None else range(max_actions)):
            if strategy.real_time:
                await _sleep_until(action_started + (action_index * period_s))
            await finish_ready_request()
            if (
                planner.eager_refill
                and (max_actions is None or action_index + 1 < max_actions)
                and pending is None
                and action_queue.actions_remaining(action_index) > 0
                and can_replan()
                and _send_ready_in(policy) <= 0.0
            ):
                pending = await start_request(action_index)
            stalled = False
            action = action_queue.consume()
            if action is None:
                underruns += 1
                _record_stats(policy, underruns=1)
                stalled = True
                if first_dispatch_at is None:
                    startup_holds += 1
                else:
                    execution_underruns += 1
                if held_since is None:
                    held_since = time.monotonic()
                if pending is None and can_replan() and _send_ready_in(policy) <= 0.0:
                    pending = await start_request(action_index)
                action_queue.advance_to(action_index + 1)
                ctx = RunContext(
                    action_index=action_index,
                    observation_id=max(0, observation_id - 1),
                    actions_remaining=action_queue.actions_remaining(
                        action_index + 1
                    ),
                    stalled=True,
                    elapsed_s=time.monotonic() - started,
                )
                if (
                    strategy.underrun == "repeat_last_action"
                    and last_action is not None
                ):
                    action = last_action
                elif (
                    read_hold_action is not None
                    and contract.hold_behavior == "current_position"
                    and strategy.underrun != "repeat_last_action"
                ):
                    if hold_latch is None:
                        hold_action = await _call_user_callback(
                            read_hold_action, ctx, executor=callback_executor,
                        )
                        hold_latch = _validate_hold_action(
                            hold_action, action_dim=contract.action_dim,
                        )
                    action = hold_latch
                else:
                    if hold_latch is None:
                        hold_latch = _hold_position_action(
                            contract=contract, observation=last_observation,
                            last_action=last_action,
                        )
                    action = hold_latch
                if not (
                    strategy.underrun == "repeat_last_action"
                    and last_action is not None
                ):
                    _record_stats(policy, hold_position_count=1)
                emit_buffer(action_index)
            else:
                hold_latch = None
                ctx = RunContext(
                    action_index=action_index,
                    observation_id=max(0, observation_id - 1),
                    actions_remaining=action_queue.actions_remaining(
                        action_index + 1
                    ),
                    stalled=False,
                    elapsed_s=time.monotonic() - started,
                )
            requested_action = tuple(float(value) for value in action)
            emit_accepted_events()
            if hooks.on_action is not None:
                hooks.on_action(
                    ActionEvent(
                        action_index=action_index,
                        stalled=stalled,
                        actions_remaining=action_queue.actions_remaining(
                            action_index + 1
                        ),
                        action=requested_action,
                    )
                )
            dispatch_started_ns = time.monotonic_ns()
            if measured_bootstrap and strategy.real_time:
                # A slow observation/driver must not cause a burst of
                # overdue commands on successive loop iterations.
                action_started = max(
                    action_started, time.monotonic() - action_index * period_s,
                )
            action_attempts += 1
            act_result = await _call_user_callback(
                act,
                requested_action,
                ctx,
                executor=callback_executor,
            )
            last_action = _accepted_action(act_result, requested_action)
            executed_history.append(last_action)
            action_history.append(last_action)
            completed_actions += 1
            if not stalled:
                _count_executed(history)
                if history is not None and held_since is not None:
                    history.hold(held_since, time.monotonic())
                held_since = None
            if not stalled and first_dispatch_at is None:
                first_dispatch_at = time.monotonic()
                first_dispatch_unix_ns = time.time_ns()
                if history is not None:
                    # Before the first action the robot held its starting state: measured
                    # windows pad those ticks like episode-start ticks (as next_action does).
                    history.begin_motion()
            if hooks.on_dispatch is not None:
                hooks.on_dispatch(DispatchEvent(
                    action_index, stalled, requested_action, last_action,
                    dispatch_started_ns, time.monotonic_ns(),
                ))
            done = _act_done(act_result)
            emit_buffer(action_index, remaining_at=action_index + 1)
            if done:
                stop_reason = "act_callback"
                break
            if (
                (max_actions is None or action_index + 1 < max_actions)
                and pending is None
                and can_replan()
                and planner.should_replan(
                    action_queue.actions_remaining(action_index + 1)
                )
                and _send_ready_in(policy) <= 0.0
            ):
                pending = await start_request(action_index + 1)
            elif (
                history is not None
                and (max_actions is None or action_index + 1 < max_actions)
                # A sparse window's frame may precede a request that starts the moment the
                # one in flight returns, so it keeps observing while a request is pending.
                and (pending is None or history.sparse)
                and can_replan()
            ):
                await observe_for_history(action_index + 1)
            if not strategy.real_time:
                await asyncio.sleep(0)
        emit_accepted_events()
    except BaseException as exc:
        failure = exc
        stop_reason = (
            "interrupted" if isinstance(exc, (asyncio.CancelledError, KeyboardInterrupt))
            else "error"
        )
        raise
    finally:
        cleanup_error = None
        try:
            if pending is not None and not pending.task.done():
                pending.task.cancel()
                await asyncio.gather(pending.task, return_exceptions=True)
        except BaseException as exc:
            cleanup_error = exc
        try:
            callback_executor.shutdown(wait=True, cancel_futures=True)
        except BaseException as exc:
            cleanup_error = cleanup_error or exc
        report_error = failure or cleanup_error
        if cleanup_error is not None and failure is None:
            stop_reason = "error"
        result = RunResult(
            actions=completed_actions, policy_calls=policy_calls, underruns=underruns,
            done=stop_reason == "act_callback", elapsed_s=time.monotonic() - run_started,
            max_actions=max_actions, stop_reason=stop_reason, timing=telemetry.summary(),
            model=getattr(policy, "model", None), region=getattr(policy, "region", None),
            transport_mode=getattr(policy, "transport_mode", None),
            fallback_reason=getattr(policy, "fallback_reason", None),
            startup_wait_ms=startup_wait_ms, startup_holds=startup_holds,
            execution_underruns=execution_underruns, action_attempts=action_attempts,
            error_type=type(report_error).__name__ if report_error else None,
            loop_cleanup_error_type=type(cleanup_error).__name__ if cleanup_error else None,
        )
        publish_run_summary(policy, hooks, result, preserve_error=report_error is not None)
        if cleanup_error is not None and failure is None:
            raise cleanup_error
    return result


async def _call_user_callback(
    callback: Callable[..., Any],
    *args: Any,
    executor: ThreadPoolExecutor,
) -> Any:
    if inspect.iscoroutinefunction(callback):
        return await callback(*args)
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(executor, partial(callback, *args))
    return await _maybe_await(result)


async def _maybe_await(value: Any) -> Any:
    if inspect.isawaitable(value):
        return await value
    return value


def _act_done(result: ActResult | bool | None) -> bool:
    if isinstance(result, ActResult):
        return result.done
    return bool(result)


def _accepted_action(
    result: ActResult | bool | None,
    requested_action: tuple[float, ...],
) -> tuple[float, ...]:
    if not isinstance(result, ActResult) or result.accepted_action is None:
        return requested_action
    if len(result.accepted_action) != len(requested_action):
        raise ValueError("accepted_action dimension must match the requested action")
    return result.accepted_action


async def _sleep_until(target: float) -> None:
    delay = target - time.monotonic()
    if delay > 0:
        await asyncio.sleep(delay)


def _validate_startup_observation(observation: Any, motion_started_unix_ns: int) -> None:
    """Use camera timestamps when supplied; never submit a pre-motion frame twice."""
    stamps = getattr(observation, "camera_capture_times_ns", None)
    if stamps is not None and any(
        type(stamp) is not int or stamp <= motion_started_unix_ns
        for stamp in stamps
    ):
        raise ValueError(
            "YAM startup requires camera frames captured after motion began; "
            "check camera frame rate and Unix capture timestamps"
        )


def _hold_position_action(
    *,
    contract: RuntimeContract,
    observation: Any | None,
    last_action: tuple[float, ...] | None,
) -> tuple[float, ...]:
    if contract.hold_behavior == "current_position":
        hold_action = getattr(observation, "hold_action", None)
        if hold_action is not None:
            return tuple(float(value) for value in hold_action)
        state = getattr(observation, "state", None)
        if contract.hold_indices and state is not None:
            # The measured pose in the action layout (RuntimeContract.hold_indices).
            return tuple(0.0 if index < 0 else float(state[index])
                         for index in contract.hold_indices)
        joint_positions = getattr(observation, "joint_positions", None)
        if joint_positions is not None:
            return tuple(float(value) for value in joint_positions)
    dim = contract.action_dim
    if dim is None and last_action is not None:
        dim = len(last_action)
    hold = [0.0] * max(1, int(dim or 1))
    if contract.hold_behavior == "zero_velocity_last_gripper":
        # Velocity rows hold still at zero; the gripper keeps its last commanded
        # position (else the measured one), so a hold never drops a grasped object.
        measured = getattr(observation, "gripper", None)
        for index in contract.gripper_indices:
            if last_action is not None and index < len(last_action):
                hold[index] = float(last_action[index])
            elif measured is not None and index < len(hold):
                hold[index] = float(measured)
    return tuple(hold)


def _count_executed(history: Any) -> None:
    """Histories that count the robot's executed actions (InternW0's episode ticks)."""
    executed = getattr(history, "executed", None)
    if executed is not None:
        executed()


def _validate_hold_action(
    action: Sequence[float],
    *,
    action_dim: int | None,
) -> tuple[float, ...]:
    if action_dim is None:
        raise ValueError(
            "read_hold_action requires a runtime contract with a known action_dim"
        )
    message = (
        f"read_hold_action must return exactly {action_dim} finite numeric values"
    )
    if isinstance(action, (str, bytes, Mapping)):
        raise ValueError(message)
    try:
        raw = tuple(action)
    except (TypeError, ValueError, OverflowError):
        raise ValueError(message) from None
    if len(raw) != action_dim or any(
        isinstance(value, bool) or not isinstance(value, Real) for value in raw
    ):
        raise ValueError(message)
    try:
        converted = tuple(float(value) for value in raw)
    except (TypeError, ValueError, OverflowError):
        raise ValueError(message) from None
    if any(not isfinite(value) for value in converted):
        raise ValueError(message)
    return converted


async def _maybe_calibrate_policy(
    *,
    policy: Any,
    observation: Any,
    instruction: str,
    timeout_s: float,
) -> Any | None:
    calibrate = getattr(policy, "_calibrate", None)
    if calibrate is None:
        return None
    return await _maybe_await(
        calibrate(observation, instruction=instruction, timeout_s=timeout_s)
    )


def _create_predict_task(
    *,
    policy: Any,
    observation: Any,
    instruction: str,
    timeout_s: float,
    actions_remaining: int,
    base_action_index: int,
    planner: _ReplanPlanner,
    rtc_context: Any | None,
    action_history: Sequence[Sequence[float]] = (),
) -> asyncio.Task[ActionChunkResult]:
    if rtc_context is not None and getattr(rtc_context, "enabled", False):
        _record_stats(policy, rtc_requests=1)
    predictor = getattr(policy, "_predict_chunk_with_queue_depth", None)
    if predictor is not None:
        task = predictor(
            observation,
            instruction=instruction,
            timeout_s=timeout_s,
            actions_remaining=actions_remaining,
            next_action_step=base_action_index,
            threshold_steps=planner.threshold_steps,
            rtc_context=rtc_context,
            **({"action_history": action_history} if action_history else {}),
        )
    else:
        task = policy.predict(
            observation,
            instruction=instruction,
            timeout_s=timeout_s,
        )
    _record_stats(policy, requests_submitted=1)
    created = asyncio.create_task(task)
    # A request dropped on a reconnect or close fails with its connection; whoever awaits it
    # still sees the error, and an abandoned one never prints "exception was never retrieved".
    created.add_done_callback(_retrieve)
    return created


def _retrieve(task: asyncio.Task) -> None:
    if not task.cancelled():
        task.exception()


def _send_ready_in(policy: Any) -> float:
    ready_in = getattr(policy, "send_ready_in", None)
    return float(ready_in()) if callable(ready_in) else 0.0


def _record_stats(policy: Any, **increments: int) -> None:
    stats = getattr(policy, "runtime_stats", None)
    if not isinstance(stats, RuntimeStats):
        return
    for name, increment in increments.items():
        if hasattr(stats, name):
            setattr(stats, name, int(getattr(stats, name)) + int(increment))


def _record_rtc_merge_stats(
    policy: Any,
    telemetry: dict[str, int | bool | None] | None,
) -> None:
    if telemetry is None:
        return
    increments = {
        "rtc_hold_or_starvation_gap_steps": int(
            telemetry.get("hold_or_starvation_gap_steps") or 0
        ),
    }
    if bool(telemetry.get("recorded")):
        increments.update(
            {
                "rtc_eligible_delay_samples": 1,
                "rtc_merge_delay_steps": int(
                    telemetry.get("merge_delay_steps") or 0
                ),
                "rtc_overcoverage_steps": int(
                    telemetry.get("overcoverage_steps") or 0
                ),
                "rtc_undercoverage_steps": int(
                    telemetry.get("undercoverage_steps") or 0
                ),
            }
        )
    _record_stats(policy, **increments)


def _record_rtc_reference_stats(
    policy: Any,
    *,
    rtc_context: Any | None,
    result: ActionChunkResult,
) -> None:
    if rtc_context is None or not getattr(rtc_context, "enabled", False):
        return
    reference_actions = _reference_actions_from_result(result)
    if reference_actions is None or len(reference_actions) == 0:
        return
    _record_stats(
        policy,
        rtc_reference_chunks=1,
        rtc_reference_actions=len(reference_actions),
    )


def _buffer_health(
    *,
    remaining: int,
    capacity: int,
    in_flight: bool,
) -> str:
    if remaining <= 0:
        return "empty"
    if in_flight:
        return "waiting"
    if remaining <= max(1, capacity // 4):
        return "low"
    return "ok"


class _ReplanPlanner:
    def __init__(
        self,
        *,
        control: str,
        control_hz: float,
        chunk_size: int,
        action_dim: int | None,
        explicit_threshold: int | None,
        resolved_config: ResolvedOptimizationConfig | None,
        action_smoothing: ResolvedActionSmoothing,
        late_bound_rows: int | None = None,
        min_replan_steps: int = 0,
    ) -> None:
        self._control_hz = control_hz
        # The most rows left at a replan: a fresh chunk minus the contract's minimum interval.
        self._max_threshold = chunk_size - min_replan_steps if min_replan_steps else None
        # The deployment's own cap on committed rows (late-bound prefix), if it declares one.
        self._late_bound_rows = late_bound_rows
        self._chunk_size = chunk_size
        self._action_dim = action_dim
        self._explicit_threshold = explicit_threshold
        self._resolved_config = resolved_config
        self._action_smoothing = action_smoothing
        self._rtc_enabled = _config_rtc_enabled(resolved_config)
        self._rtc_config = _rtc_config_from_resolved(resolved_config)
        self._rtc_profile_set: RtcProfileSet | None = None
        self._last_rtc_merge_telemetry: dict[str, int | bool | None] | None = None
        # Late-bound prefix RTC: the last accepted chunk and its wall-clock receipt.
        self._last_chunk_receipt: tuple[int, int] | None = None
        try:
            self._control_config = control_config_for_name(control)
        except ValueError:
            self._control_config = control_config_for_name("adaptive")
        self._method_o = (
            MethodOController(
                chunk_size=chunk_size,
                control_hz=control_hz,
                config=self._control_config,
            )
            if isinstance(self._control_config, MethodOConfig)
            else None
        )
        self._rtc_delay_estimator = (
            RtcDelayEstimator(
                chunk_size=chunk_size,
                action_hz=control_hz,
                control_mode=control,
            )
            if self._rtc_config is not None
            and self._rtc_config.contract_id
            == DYNAMIC_FULL_HORIZON_RTC_CONTRACT_ID
            else None
        )

    @property
    def replan_at_remaining(self) -> int:
        if self._explicit_threshold is not None:
            return int(self._explicit_threshold)
        if self._method_o is not None:
            threshold = self._method_o.threshold_steps
        else:
            threshold = max(1, ceil(self._chunk_size / 2))
        if self._max_threshold is not None:
            threshold = max(1, min(threshold, self._max_threshold))
        return threshold

    @property
    def threshold_steps(self) -> int | None:
        if self.eager_refill:
            return None
        return self.replan_at_remaining

    @property
    def eager_refill(self) -> bool:
        return (
            self._explicit_threshold is None
            and isinstance(self._control_config, EagerRefillQueueConfig)
        )

    def seed_calibration(self, profile: Any) -> None:
        usage = getattr(profile, "runtime_calibration_usage", "normal")
        if usage == "not_used":
            return
        if self._rtc_delay_estimator is not None:
            self._rtc_delay_estimator.seed_calibration(profile)
        if self._method_o is not None:
            self._method_o.seed_calibration(
                profile,
                mode="light" if usage == "light" else "normal",
            )
        if (
            usage == "normal"
            and self._rtc_config is not None
            and _is_calibrated_static_rtc(self._rtc_config)
        ):
            method_profile = (
                self._control_config.profile
                if isinstance(self._control_config, MethodOConfig)
                else "balanced"
            )
            state = build_rtc_estimator_state_from_calibration(
                profile,
                chunk_size=self._chunk_size,
                action_hz=self._control_hz,
                method_o_profile=method_profile,
                control_mode=(
                    method_profile
                    if method_profile in METHOD_O_PROFILES
                    else "adaptive"
                ),
            )
            self._rtc_profile_set = build_rtc_profile_set(
                self._rtc_config,
                state,
            ).mark_static("network_calibration")

    def should_replan(self, actions_remaining: int) -> bool:
        if self.eager_refill:
            return False
        return int(actions_remaining) <= self.replan_at_remaining

    def build_rtc_context(
        self, action_queue: ActionBuffer, from_step: int | None = None
    ) -> Any | None:
        if not self._rtc_enabled or self._rtc_config is None:
            return None
        decision = self._method_o.last_decision if self._method_o is not None else None
        classification = None if decision is None else decision.classification
        profile_name = select_static_rtc_profile_name(classification)
        reference_actions = action_queue.peek_rtc_reference_actions(
            max_steps=self._chunk_size, from_step=from_step
        )
        if self._rtc_config.contract_id == LATE_BOUND_PREFIX_RTC_CONTRACT_ID:
            previous = self._last_chunk_receipt
            return build_late_bound_prefix_rtc_request(
                reference_actions=reference_actions or (),
                previous_chunk_id=None if previous is None else previous[0],
                previous_chunk_receipt_unix_ns=None if previous is None else previous[1],
                client_send_unix_ns=time.time_ns(),
                max_rows=self._late_bound_rows,
            )
        if self._rtc_delay_estimator is not None:
            context = build_rtc_context_for_queue(
                config=self._rtc_config,
                chunk_size=self._chunk_size,
                action_dim=(
                    self._resolved_config.action_dim
                    if self._resolved_config is not None
                    and self._resolved_config.action_dim is not None
                    else self._action_dim
                ),
                profile_name=profile_name,
                reference_actions=reference_actions,
                estimator_state=self._rtc_delay_estimator.state(),
                estimator_source=self._rtc_delay_estimator.source,
                estimator_sample_count=self._rtc_delay_estimator.sample_count,
            )
            if self._last_rtc_merge_telemetry is None:
                return context
            return context.model_copy(
                update={
                    "telemetry": {
                        **context.telemetry,
                        "previous_merge": dict(self._last_rtc_merge_telemetry),
                    }
                }
            )
        return build_rtc_context_for_queue(
            config=self._rtc_config,
            chunk_size=self._chunk_size,
            action_dim=(
                self._resolved_config.action_dim
                if self._resolved_config is not None
                and self._resolved_config.action_dim is not None
                else self._action_dim
            ),
            profile_name=profile_name,
            reference_actions=reference_actions,
            profile_set=self._rtc_profile_set,
            desired_execution_horizon_steps=(
                None if decision is None else decision.threshold_steps
            ),
        )

    def record_merge_delay(
        self,
        *,
        action_queue: ActionBuffer,
        base_action_index: int,
        actions_remaining_at_submit: int,
        rtc_context: Any | None,
        elapsed_request_steps: int,
    ) -> dict[str, int | bool | None] | None:
        if self._rtc_delay_estimator is None or rtc_context is None:
            return None
        merge_delay_steps = max(
            0,
            int(action_queue.next_action_step) - int(base_action_index),
        )
        eligible = int(actions_remaining_at_submit) > 0
        recorded = self._rtc_delay_estimator.record(
            merge_delay_steps,
            eligible=eligible,
        )
        valid_steps = max(
            0,
            int(getattr(rtc_context, "reference_action_valid_steps", 0) or 0),
        )
        execution_horizon = max(
            0,
            int(getattr(rtc_context, "execution_horizon_steps", 0) or 0),
        )
        effective_horizon = min(valid_steps, execution_horizon)
        overcoverage = (
            max(0, effective_horizon - merge_delay_steps) if eligible else None
        )
        undercoverage = (
            max(0, merge_delay_steps - effective_horizon) if eligible else None
        )
        telemetry: dict[str, int | bool | None] = {
            "merge_delay_steps": merge_delay_steps,
            "eligible": eligible,
            "recorded": recorded,
            "effective_guided_horizon_steps": effective_horizon,
            "overcoverage_steps": overcoverage,
            "undercoverage_steps": undercoverage,
            "hold_or_starvation_gap_steps": max(
                0,
                int(elapsed_request_steps) - merge_delay_steps,
            ),
        }
        self._last_rtc_merge_telemetry = dict(telemetry)
        return telemetry

    def accept_chunk(
        self,
        *,
        action_queue: ActionBuffer,
        base_action_index: int,
        result: ActionChunkResult,
        executed_history: Sequence[Sequence[float]] = (),
    ) -> dict[str, int | float | str | None]:
        if result.chunk_id is not None:
            self._last_chunk_receipt = (int(result.chunk_id), time.time_ns())
        actions = result.actions[: self._chunk_size]
        action_indices = (
            None
            if result.action_indices is None
            else result.action_indices[: len(actions)]
        )
        action_dimensions = {len(action) for action in actions}
        if len(action_dimensions) > 1:
            raise ValueError("action dimensions must be consistent within a chunk")
        if (
            self._action_dim is not None
            and action_dimensions
            and action_dimensions != {self._action_dim}
        ):
            actual_dimension = next(iter(action_dimensions))
            raise ValueError(
                "action dimensions must match the runtime contract: "
                f"expected {self._action_dim}, got {actual_dimension}"
            )
        if self._rtc_enabled:
            diagnostics = action_queue.replace_aligned_chunk(
                base_action_step=base_action_index,
                actions=actions,
                action_indices=action_indices,
                rtc_reference_actions=_reference_actions_from_result(result),
            )
            return {
                **diagnostics,
                "requested_mode": self._action_smoothing.requested_mode,
                "resolved_mode": "rtc",
                "new_action_weight": None,
                "correction_steps": None,
                "stale_steps": 0,
                "overlap_steps": int(diagnostics.get("replaced_steps", 0)),
                "resolved_steps": len(actions),
                "first_executable_source_offset": None,
                "max_abs_position_revision": 0.0,
            }
        return action_queue.merge_smoothed_chunk(
            base_action_step=base_action_index,
            actions=actions,
            action_indices=action_indices,
            smoothing=self._action_smoothing,
            executed_history=executed_history,
        )

    def record_result(
        self,
        result: ActionChunkResult,
        *,
        actions_remaining_at_submit: int,
    ) -> None:
        if self._explicit_threshold is not None or self._method_o is None:
            return
        roundtrip_ms = max(0.0, float(result.timing.obs_to_action_ms))
        self._method_o.record_roundtrip_result(
            roundtrip_ms=roundtrip_ms,
            request_actions_remaining=actions_remaining_at_submit,
            usable_for_slack=True,
        )

# On a new instruction, the request in flight for the old one is dropped only when the plan
# left covers this many round trips (the slowest of the last few): the server still finishes
# the dropped inference before the new one, so the fresh chunk takes about two.
SWITCH_DROP_ROUND_TRIPS = 3.0
ROUND_TRIPS_KEPT = 5


@dataclass(frozen=True)
class _PendingRequest:
    base_action_index: int
    actions_remaining_at_submit: int
    task: asyncio.Task[ActionChunkResult]
    rtc_context: Any | None
    submitted_at_ns: int


@dataclass(frozen=True)
class _AcceptedChunkEvents:
    timing: PolicyTimingEvent
    chunk: ChunkEvent
    merge: MergeEvent
    queue: QueueMergeEvent | None = None


class StaleFirstChunkError(errors.DreamscaleError, ValueError):
    """Chunks keep arriving with every action already past the robot's step, before the
    first model action was ever dispatched. A ``dreamscale.Error`` (code
    ``first_chunk_misaligned``, with a fix) so the CLI renders a recovery line; also a
    ``ValueError`` for older handlers."""

    def __init__(self, *, elapsed_s: float, horizon_s: float, model: str | None = None) -> None:
        name = public_model(model) if model else "the model"
        super().__init__(
            errors.ErrorInfo(
                code="first_chunk_misaligned",
                problem=f"{name} returned a first chunk that does not start at the current step",
                cause=f"the last {STALE_FIRST_CHUNKS_BEFORE_RAISE} chunks indexed their actions "
                f"past the robot's step ({elapsed_s * 1000:.0f} ms round trip, "
                f"{horizon_s:.1f} s chunk)",
                fix="check `dreamscale models list`; if it keeps happening for this model, email "
                "team@dreamscalelabs.com with the session id",
            )
        )
        self.elapsed_s = elapsed_s
        self.horizon_s = horizon_s


# Consecutive fully stale chunks before the first dispatch that raise StaleFirstChunkError.
STALE_FIRST_CHUNKS_BEFORE_RAISE = 3


class AsyncActionController:
    def __init__(
        self,
        *,
        policy: Any,
        strategy: RunStrategy | None = None,
        skip_calibration: bool = False,
        hooks: RunHooks | None = None,
        anchor_first_chunk: bool = False,
    ) -> None:
        self._policy = policy
        self._strategy = strategy or RunStrategy()
        self._skip_calibration = bool(skip_calibration)
        # The public next_action path only: held ticks before the first dispatch do not
        # consume plan steps, and a fully stale first chunk is a stall, not an error. The
        # managed run loops (CLI) wait for their first chunk and keep their behaviour.
        self._anchor_first_chunk = bool(anchor_first_chunk)
        self._hooks = hooks or RunHooks()
        self._contract = resolve_runtime_contract(
            model=getattr(policy, "model", None),
            resolved_config=getattr(policy, "resolved_optimization_config", None),
            action_hz_override=self._strategy.action_hz,
            chunk_size_override=self._strategy.chunk_size,
            deployment=getattr(policy, "deployment", None),
        )
        action_smoothing = resolve_action_smoothing(self._strategy, self._contract)
        self._chunk_size = self._contract.execution_chunk_size
        self._action_queue = ActionBuffer(next_action_step=0)
        self._planner = _ReplanPlanner(
            control=getattr(policy, "control", "adaptive"),
            control_hz=self._contract.action_hz,
            chunk_size=self._chunk_size,
            action_dim=self._contract.action_dim,
            explicit_threshold=self._strategy.replan_at_remaining,
            resolved_config=getattr(policy, "resolved_optimization_config", None),
            action_smoothing=action_smoothing,
            late_bound_rows=late_bound_prefix_rows(getattr(policy, "deployment", None)),
            min_replan_steps=self._contract.min_replan_steps,
        )
        self._pending: _PendingRequest | None = None
        # Whether this controller has stepped or prepared yet: its first one starts a new
        # server-kept episode if raw ``predict()`` calls already used the policy's.
        self._episode_begun = False
        self._active_instruction: str | None = None
        # A new instruction whose first request hasn't gone out yet (it goes on the next tick
        # a request can), and when the plan was last stepped.
        self._instruction_switched = False
        self._last_step_at: float | None = None
        # Recent chunks' round trips (request sent to chunk merged), seconds.
        self._round_trips_s: deque[float] = deque(maxlen=ROUND_TRIPS_KEPT)
        # A request sent ahead of the first step (prefetch), and when its chunk landed.
        self._ahead: _PendingRequest | None = None
        self._ahead_landed_at: float | None = None
        self._latest_observation: Any | None = None
        # The step the latest observation was captured at: a request sent after that step's
        # action is consumed still starts there (its row 0 is the action played at capture).
        self._latest_observation_step: int | None = None
        self._latest_instruction: str | None = None
        self._last_observation: Any | None = None
        self._last_action: tuple[float, ...] | None = None
        self._executed_history: deque[tuple[float, ...]] = deque(maxlen=2)
        # Actions executed on recent ticks, for checkpoints that condition on them. The
        # snapshot taken with each observation ends on the tick before its capture.
        self._action_history: deque[tuple[float, ...]] | None = (
            deque(maxlen=self._contract.action_history) if self._contract.action_history else None
        )
        self._latest_action_history: tuple[tuple[float, ...], ...] = ()
        self._measured_bootstrap = self._contract.measured_bootstrap
        self._startup_delay_s = (
            self._contract.startup_motion_delay_s if self._strategy.real_time else 0.0
        )
        self._first_dispatch_at: float | None = None
        self._first_dispatch_unix_ns: int | None = None
        self._first_dispatch_confirmed = False
        # Since when the robot has held (stalled steps, however the caller waited).
        self._held_since: float | None = None
        self._latest_observed_at = 0.0
        self._requests_started = 0
        self._last_stalled = False
        self._hold_latch: tuple[float, ...] | None = None
        self._calibrated = False
        self._stale_first_chunks = 0
        self._lock = asyncio.Lock()

    @property
    def actions_remaining(self) -> int:
        return self._action_queue.actions_remaining()

    @property
    def in_flight(self) -> bool:
        return self._pending is not None

    @property
    def dispatched(self) -> bool:
        """A model action has been returned (the plan is being executed)."""
        return self._first_dispatch_at is not None

    @property
    def awaiting_chunk(self) -> bool:
        """A request has been sent and the server has not answered yet (a finished
        request waiting to be merged on the next step does not count)."""
        return self._pending is not None and not self._pending.task.done()

    def _begin_episode(self, history: Any) -> None:
        """The controller's first step or prepare: an episode the server keeps (EpisodeTicks)
        that raw ``predict()`` calls already drove starts afresh (step 0, chunk 0), so the
        loop's first request is a new episode on the server rather than a step back in the
        one the predicts left (which the server refuses; the SDK then reconnected)."""
        if self._episode_begun:
            return
        self._episode_begun = True
        if history is not None and getattr(history, "requested", False) and hasattr(
            history, "take_chunk"
        ):
            history.clear()

    async def next_action(
        self,
        observation: Any,
        *,
        instruction: str,
        timeout_s: float,
    ) -> tuple[float, ...]:
        step = await self.step(
            observation,
            instruction=instruction,
            timeout_s=timeout_s,
        )
        return step.action

    async def prepare(
        self,
        observation: Any,
        *,
        instruction: str,
        timeout_s: float,
        wait_for_chunk: bool = False,
        ahead: bool = False,
    ) -> None:
        """Take this observation and send its request now, before stepping. ``ahead``: a
        prefetch, whose chunk is dropped on the first step if it waited too long there
        (see _drop_aged_prefetch)."""
        async with self._lock:
            await self._set_active_instruction(instruction)
            if self._plan_is_stale():
                # Prepared ahead of stepping (prefetch, a run's start): nothing queued from
                # before is still the robot's plan.
                await self._flush_plan()
            self._latest_observation = observation
            self._latest_observation_step = self._action_queue.next_action_step
            self._latest_observed_at = time.monotonic()
            self._latest_instruction = instruction
            self._last_observation = observation
            if self._action_history is not None:
                self._latest_action_history = tuple(self._action_history)
            history = getattr(self._policy, "observation_history", None)
            self._begin_episode(history)
            if history is not None:
                # Every step is one control tick: the windowed request reads them back.
                # Keep the tick even when its window fails, so later windows can heal.
                self._record_hold()
                try:
                    self._latest_observation = history.window(observation)
                finally:
                    await self._push_history(history, observation)
            await self._maybe_calibrate(instruction=instruction, timeout_s=timeout_s)
            await self._finish_ready_request()
            if self._pending is None:
                self._start_request(instruction=instruction, timeout_s=timeout_s)
            if ahead and self._pending is not None:
                self._track_ahead(self._pending)
            if wait_for_chunk and self._pending is not None:
                await asyncio.wait_for(asyncio.shield(self._pending.task), timeout_s)

    async def seed_initial_position(self, action: Sequence[float]) -> None:
        async with self._lock:
            if self._executed_history:
                raise RuntimeError("initial position must precede execution")
            self._executed_history.append(
                _validate_hold_action(action, action_dim=self._contract.action_dim)
            )

    async def step(
        self,
        observation: Any,
        *,
        instruction: str,
        timeout_s: float,
        action_index: int | None = None,
        wait_for_chunk: bool = True,
        observed_at: float | None = None,
    ) -> PolicyStepResult:
        """``observed_at``: a monotonic time no later than the observation's capture (when
        the caller started observing); by default, when it reaches this step."""
        async with self._lock:
            accepted_events: list[_AcceptedChunkEvents] = []
            await self._set_active_instruction(instruction)
            self._drop_aged_prefetch()
            self._last_step_at = time.monotonic()
            self._latest_observation = observation
            self._latest_observation_step = self._action_queue.next_action_step
            self._latest_observed_at = time.monotonic() if observed_at is None else observed_at
            self._latest_instruction = instruction
            self._last_observation = observation
            if self._action_history is not None:
                self._latest_action_history = tuple(self._action_history)
            history = getattr(self._policy, "observation_history", None)
            self._begin_episode(history)
            if history is not None:
                # Every step is one control tick: the windowed request reads them back.
                # Keep the tick even when its window fails, so later windows can heal.
                self._record_hold()
                try:
                    self._latest_observation = history.window(observation)
                finally:
                    await self._push_history(history, observation)
            await self._maybe_calibrate(instruction=instruction, timeout_s=timeout_s)
            if self._pending is not None and not self._pending.task.done():
                # The sync facade can otherwise poll repeatedly ahead of ready
                # transport callbacks when user callbacks consume the full cadence.
                await asyncio.sleep(0)
                await asyncio.sleep(0)
            accepted_events.extend(await self._finish_ready_request())
            self._submit_before_consume_if_needed(
                instruction=instruction,
                timeout_s=timeout_s,
            )

            action = self._action_queue.consume()
            if action is not None:
                resolved = tuple(float(value) for value in action)
                self._record_action(resolved)
                self._submit_after_consume_if_needed(
                    instruction=instruction,
                    timeout_s=timeout_s,
                )
                return self._step_result(
                    action=resolved,
                    stalled=False,
                    action_index=action_index,
                    accepted_events=accepted_events,
                )

            if self._pending is None:
                self._start_request(instruction=instruction, timeout_s=timeout_s)
            if self._pending is None:
                return self._underrun_step(
                    action_index=action_index,
                    accepted_events=accepted_events,
                )
            if not wait_for_chunk:
                return self._underrun_step(
                    action_index=action_index,
                    accepted_events=accepted_events,
                )
            waited_from = time.monotonic()
            try:
                result = await asyncio.wait_for(
                    asyncio.shield(self._pending.task),
                    timeout=timeout_s,
                )
            except TimeoutError:
                return self._underrun_step(
                    action_index=action_index,
                    accepted_events=accepted_events,
                )
            finally:
                if history is not None:
                    history.hold(waited_from, time.monotonic())
            accepted = self._accept_pending(result)
            if accepted is not None:
                accepted_events.append(accepted)
            self._submit_before_consume_if_needed(
                instruction=instruction,
                timeout_s=timeout_s,
            )
            action = self._action_queue.consume()
            if action is None:
                return self._underrun_step(
                    action_index=action_index,
                    accepted_events=accepted_events,
                )
            resolved = tuple(float(value) for value in action)
            self._record_action(resolved)
            self._submit_after_consume_if_needed(
                instruction=instruction,
                timeout_s=timeout_s,
            )
            return self._step_result(
                action=resolved,
                stalled=False,
                action_index=action_index,
                accepted_events=accepted_events,
            )

    async def record_act_result(
        self,
        requested_action: Sequence[float],
        result: ActResult | bool | None,
    ) -> None:
        requested = tuple(float(value) for value in requested_action)
        accepted = _accepted_action(result, requested)
        async with self._lock:
            if not self._executed_history:
                raise RuntimeError("cannot record actuator feedback before an action")
            if self._executed_history[-1] != requested:
                raise RuntimeError("actuator feedback does not match the latest action")
            self._executed_history[-1] = accepted
            if self._action_history:
                self._action_history[-1] = accepted
            self._last_action = accepted
            if not self._last_stalled and not self._first_dispatch_confirmed:
                self._first_dispatch_at = time.monotonic()
                self._first_dispatch_unix_ns = time.time_ns()
                self._first_dispatch_confirmed = True

    async def close(self) -> None:
        if self._pending is not None and not self._pending.task.done():
            self._pending.task.cancel()
            await asyncio.gather(self._pending.task, return_exceptions=True)
        self._pending = None

    def forget_request(self) -> None:
        """Drop a request that failed with a server answer, so the next step sends a new
        one instead of re-raising the same failure."""
        pending, self._pending = self._pending, None
        if pending is not None and not pending.task.done():
            pending.task.cancel()

    def skip(self, steps: int) -> None:
        """Drop the next ``steps`` queued actions: a late caller never catches up.

        Only once a chunk is being executed. Before the first dispatch there is nothing
        to be late against: held ticks must not consume the plan that has not arrived.
        """
        if steps > 0 and (self._first_dispatch_at is not None or not self._anchor_first_chunk):
            self._action_queue.advance_to(self._action_queue.next_action_step + int(steps))

    def buffer_event(self, action_index: int) -> BufferEvent:
        remaining = self._action_queue.actions_remaining()
        return BufferEvent(
            action_index=action_index,
            remaining=remaining,
            capacity=self._chunk_size,
            health=_buffer_health(
                remaining=remaining,
                capacity=self._chunk_size,
                in_flight=self.in_flight,
            ),
            in_flight=self.in_flight,
        )

    async def _finish_ready_request(self) -> list[_AcceptedChunkEvents]:
        if self._pending is not None and self._pending.task.done():
            try:
                result = self._pending.task.result()
            except TimeoutError:
                self._pending = None
                return []
            accepted = self._accept_pending(result)
            return [] if accepted is None else [accepted]
        return []

    def _accept_pending(self, result: ActionChunkResult) -> _AcceptedChunkEvents | None:
        if self._pending is None:
            return None
        request = self._pending
        self._pending = None
        self._round_trips_s.append(max(0.0, time.monotonic_ns() - request.submitted_at_ns) / 1e9)
        if self._measured_bootstrap and not self._executed_history:
            anchor = _hold_position_action(
                contract=self._contract, observation=self._last_observation, last_action=None,
            )
            self._executed_history.append(
                _validate_hold_action(anchor, action_dim=self._contract.action_dim)
            )
        elapsed_request_steps = ceil(
            max(0, time.monotonic_ns() - request.submitted_at_ns)
            * self._contract.action_hz
            / 1_000_000_000.0
        )
        merge_telemetry = self._planner.record_merge_delay(
            action_queue=self._action_queue,
            base_action_index=request.base_action_index,
            actions_remaining_at_submit=request.actions_remaining_at_submit,
            rtc_context=request.rtc_context,
            elapsed_request_steps=elapsed_request_steps,
        )
        _record_rtc_merge_stats(self._policy, merge_telemetry)
        accepted_action_index = self._action_queue.next_action_step
        chunk_event = _chunk_event_from_result(
            result=result,
            base_action_index=request.base_action_index,
            accepted_action_index=accepted_action_index,
            chunk_size=self._chunk_size,
        )
        before = self._action_queue.snapshot() if self._hooks.on_queue_merge else ()
        before_raw = self._action_queue.snapshot(raw=True) if self._hooks.on_queue_merge else ()
        merge_diagnostics = self._planner.accept_chunk(
            action_queue=self._action_queue,
            base_action_index=request.base_action_index,
            result=result,
            executed_history=tuple(self._executed_history),
        )
        if (
            (self._anchor_first_chunk or self._measured_bootstrap)
            and self._first_dispatch_at is None
            and not self.actions_remaining
        ):
            # Every action of this chunk already went by (a first chunk slower than the
            # chunk itself, or an engine indexing from a later step). Not an error for
            # the robot loop: hold and request again with the measured latency. Three in
            # a row mean the round trip cannot keep up with this model. Other un-anchored
            # contracts (SO-101 through the sync loop) keep their a107 behaviour: the
            # stale actions are simply never reached.
            self._stale_first_chunks += 1
            _record_stats(self._policy, stale_chunks_dropped=1)
            # Nothing of the rejected chunk may ever execute: the fresh request is
            # anchored at the current step, on an empty queue.
            self._action_queue = ActionBuffer(
                next_action_step=self._action_queue.next_action_step
            )
            if self._stale_first_chunks >= STALE_FIRST_CHUNKS_BEFORE_RAISE:
                raise StaleFirstChunkError(
                    elapsed_s=max(0.0, time.monotonic_ns() - request.submitted_at_ns) / 1e9,
                    horizon_s=self._contract.horizon_s,
                    model=getattr(self._policy, "model", None),
                )
            # The request did not start the plan: YAM's startup gate (one request until
            # the first dispatch plus the motion delay) must let the next one through.
            self._requests_started = max(0, self._requests_started - 1)
            return None
        self._stale_first_chunks = 0
        merge_event = _merge_event_from_diagnostics(
            result=result,
            base_action_index=request.base_action_index,
            accepted_action_index=accepted_action_index,
            diagnostics=merge_diagnostics,
        )
        _record_rtc_reference_stats(
            self._policy,
            rtc_context=request.rtc_context,
            result=result,
        )
        _record_stats(self._policy, chunks_received=1)
        self._planner.record_result(
            result,
            actions_remaining_at_submit=request.actions_remaining_at_submit,
        )
        return _AcceptedChunkEvents(
            timing=_timing_event_from_result(result),
            chunk=chunk_event,
            merge=merge_event,
            queue=QueueMergeEvent(
                request.submitted_at_ns, time.monotonic_ns(), chunk_event,
                before, before_raw, self._action_queue.snapshot(),
            ) if self._hooks.on_queue_merge else None,
        )

    def _submit_before_consume_if_needed(
        self,
        *,
        instruction: str,
        timeout_s: float,
    ) -> None:
        if self._pending is None and self._instruction_switched:
            # A new instruction's first request goes out as soon as nothing is in flight.
            self._start_request(instruction=instruction, timeout_s=timeout_s)
            return
        if not self._planner.eager_refill:
            return
        if self._pending is None and self._action_queue.actions_remaining() > 0:
            self._start_request(instruction=instruction, timeout_s=timeout_s)

    def _submit_after_consume_if_needed(
        self,
        *,
        instruction: str,
        timeout_s: float,
    ) -> None:
        if self._pending is not None:
            return
        if self._instruction_switched or self._planner.should_replan(
            self._action_queue.actions_remaining()
        ):
            self._start_request(instruction=instruction, timeout_s=timeout_s)

    def _start_request(self, *, instruction: str, timeout_s: float) -> None:
        if self._latest_observation is None:
            return
        if _send_ready_in(self._policy) > 0.0:
            # The send floor has not passed: don't freeze this observation into a
            # request now; a later tick starts it with a fresher one.
            return
        if self._startup_delay_s and self._requests_started == 1:
            if self._first_dispatch_at is None or (
                self._latest_observed_at < self._first_dispatch_at + self._startup_delay_s
            ):
                return
            _validate_startup_observation(
                self._latest_observation, self._first_dispatch_unix_ns,
            )
        resolved_instruction = (
            self._latest_instruction
            if self._latest_instruction is not None
            else instruction
        )
        actions_remaining = self._action_queue.actions_remaining()
        # A model that reads its executed actions (FLUX 3 Action) plans from its observation's
        # step: row 0 is the action played at capture, just after the history it was sent, even
        # when the request goes out after that step's action is consumed (as run() bases a
        # request on its observation's step). Its committed rows start there too. Other models
        # keep placing row 0 at the next step.
        base = self._action_queue.next_action_step
        if self._latest_observation_step is not None and self._contract.action_history:
            base = min(base, self._latest_observation_step)
        rtc_context = self._planner.build_rtc_context(self._action_queue, from_step=base)
        submitted_at_ns = time.monotonic_ns()
        if self._hooks.on_request is not None:
            self._hooks.on_request(RequestEvent(
                submitted_at_ns, base, actions_remaining, self._latest_observation,
            ))
        self._pending = _PendingRequest(
            base_action_index=base,
            actions_remaining_at_submit=actions_remaining,
            task=_create_predict_task(
                policy=self._policy,
                observation=self._latest_observation,
                instruction=resolved_instruction,
                timeout_s=max(float(timeout_s), float(self._strategy.timeout_s)),
                actions_remaining=actions_remaining,
                base_action_index=base,
                planner=self._planner,
                rtc_context=rtc_context,
                action_history=self._latest_action_history,
            ),
            rtc_context=rtc_context,
            submitted_at_ns=submitted_at_ns,
        )
        self._requests_started += 1
        self._instruction_switched = False
        self._latest_observation = None
        self._latest_observation_step = None
        self._latest_instruction = None

    async def _set_active_instruction(self, instruction: str) -> None:
        """A new instruction takes effect at the next chunk. While the plan is being executed,
        the robot keeps executing it (no flush, no hold) and the next request carries the
        new instruction. A request still in flight for the old one is dropped when the plan
        left covers SWITCH_DROP_ROUND_TRIPS of the slowest recent round trip (the server
        finishes the dropped inference first) and no send floor holds the next request back,
        so the new instruction acts about one round trip after the switch; otherwise it lands
        (it is the robot's next plan) and the new request follows on that tick: up to about
        two round trips. (After a drop the new chunk's RTC prefix is sized for its own round
        trip; a merge that comes later blends as any late chunk does.) A plan no longer being
        executed (see _plan_is_stale) starts over, as before."""
        if self._active_instruction == instruction:
            return
        previous, self._active_instruction = self._active_instruction, instruction
        if previous is None:
            return
        if self._plan_is_stale():
            await self._flush_plan()
            return
        self._instruction_switched = True
        pending = self._pending
        if (
            pending is None or pending.task.done() or not self._round_trips_s
            or _send_ready_in(self._policy) > 0.0  # a shared model's spacing: it would wait
        ):
            return
        plan_s = self.actions_remaining / self._contract.action_hz
        if plan_s >= SWITCH_DROP_ROUND_TRIPS * max(self._round_trips_s):
            # Counted once, by the transport, when its late reply is discarded.
            pending.task.cancel()
            await asyncio.gather(pending.task, return_exceptions=True)
            self._pending = None

    def _track_ahead(self, request: _PendingRequest) -> None:
        self._ahead, self._ahead_landed_at = request, None

        def landed(_task: asyncio.Task[Any]) -> None:
            if self._ahead is request:
                self._ahead_landed_at = time.monotonic()

        request.task.add_done_callback(landed)

    def _drop_aged_prefetch(self) -> None:
        """A chunk requested ahead (prefetch) that then waited unmerged for longer than its
        own round trip (at least two ticks) was planned from a pose the robot has since left,
        another policy driving it meanwhile: drop it, so this step requests again from its
        own observation rather than replay it."""
        ahead, self._ahead = self._ahead, None
        if ahead is None or ahead is not self._pending or not ahead.task.done():
            return
        landed = self._ahead_landed_at
        if landed is None:
            return
        round_trip_s = max(0.0, landed - ahead.submitted_at_ns / 1e9)
        if time.monotonic() - landed <= max(2.0 / self._contract.action_hz, round_trip_s):
            return
        if not ahead.task.cancelled():
            ahead.task.exception()  # retrieved: a failure there is moot now
        self._pending = None
        self._requests_started = max(0, self._requests_started - 1)
        _record_stats(self._policy, stale_chunks_dropped=1)

    def _plan_is_stale(self) -> bool:
        """No step since the queued plan would have run out (at least two control ticks):
        it was planned for a robot state that has gone by."""
        if self._last_step_at is None:
            return True
        horizon_s = max(2, self.actions_remaining) / self._contract.action_hz
        return time.monotonic() - self._last_step_at > horizon_s

    async def _flush_plan(self) -> None:
        if self._pending is not None:
            if not self._pending.task.done():
                self._pending.task.cancel()
                await asyncio.gather(self._pending.task, return_exceptions=True)
            self._pending = None
        self._action_queue = ActionBuffer(
            next_action_step=self._action_queue.next_action_step
        )
        self._latest_observation = None
        self._latest_observation_step = None
        self._latest_instruction = None
        self._last_action = None
        self._executed_history.clear()
        self._first_dispatch_at = None
        self._first_dispatch_unix_ns = None
        self._first_dispatch_confirmed = False
        self._requests_started = 0
        self._hold_latch = None
        self._instruction_switched = False
        self._held_since = None
        if self._action_history is not None:
            self._action_history.clear()
        self._latest_action_history = ()
        self._ahead = None
        self._round_trips_s.clear()

    async def _maybe_calibrate(self, *, instruction: str, timeout_s: float) -> None:
        if self._skip_calibration:
            self._calibrated = True
            return
        if self._calibrated or self._last_observation is None:
            return
        profile = await _maybe_calibrate_policy(
            policy=self._policy,
            observation=self._last_observation,
            instruction=instruction,
            timeout_s=timeout_s,
        )
        if profile is not None:
            self._planner.seed_calibration(profile)
        self._calibrated = True

    def _underrun_step(
        self,
        *,
        action_index: int | None,
        accepted_events: list[_AcceptedChunkEvents],
    ) -> PolicyStepResult:
        action = self._handle_underrun()
        self._record_action(action, stalled=True)
        if self._first_dispatch_at is None and (
            self._anchor_first_chunk or self._measured_bootstrap
        ):
            # A startup hold (next_action before the first chunk, or a real-time tick
            # while a rejected bootstrap chunk is re-requested): the plan has not started,
            # so the tick does not consume a step of it and the chunk lands at this step.
            return self._step_result(
                action=action,
                stalled=True,
                action_index=action_index,
                accepted_events=accepted_events,
            )
        next_step = (
            self._action_queue.next_action_step + 1
            if action_index is None
            else int(action_index) + 1
        )
        self._action_queue.advance_to(next_step)
        return self._step_result(
            action=action,
            stalled=True,
            action_index=action_index,
            accepted_events=accepted_events,
        )

    def _handle_underrun(self) -> tuple[float, ...]:
        _record_stats(self._policy, underruns=1)
        if (
            self._strategy.underrun == "repeat_last_action"
            and self._last_action is not None
        ):
            return self._last_action
        _record_stats(self._policy, hold_position_count=1)
        if self._hold_latch is None:
            self._hold_latch = _hold_position_action(
                contract=self._contract,
                observation=self._last_observation,
                last_action=self._last_action,
            )
        return self._hold_latch

    async def _push_history(self, history: Any, observation: Any) -> None:
        """Keep this step's observation; an episode the server keeps (EpisodeTicks) also
        sends its tick frames ahead, as the managed run loop does."""
        push = getattr(self._policy, "push_history", None)
        if getattr(history, "pushes_ahead_in_steps", False) and push is not None:
            await _maybe_await(push(observation))
        else:
            history.push(observation)

    def _record_hold(self) -> None:
        """The robot has held since its first stalled step; measured history windows
        repeat its last tick for that interval, whichever layer waited for the chunk."""
        history = getattr(self._policy, "observation_history", None)
        if history is not None and self._held_since is not None:
            history.hold(self._held_since, time.monotonic())

    def _record_action(self, action: tuple[float, ...], *, stalled: bool = False) -> None:
        self._last_stalled = stalled
        if stalled:
            if self._held_since is None:
                self._held_since = time.monotonic()
        else:
            self._record_hold()
            self._held_since = None
            self._hold_latch = None
            _count_executed(getattr(self._policy, "observation_history", None))
            # Manual step()/next_action() callers own dispatch. Their first
            # returned command is the best available boundary; managed run()
            # replaces it with the actual actuator callback completion time.
            if self._first_dispatch_at is None:
                self._first_dispatch_at = time.monotonic()
                self._first_dispatch_unix_ns = time.time_ns()
                history = getattr(self._policy, "observation_history", None)
                if history is not None:
                    history.begin_motion()
        self._last_action = action
        self._executed_history.append(action)
        if self._action_history is not None:
            self._action_history.append(action)

    def _step_result(
        self,
        *,
        action: tuple[float, ...],
        stalled: bool,
        action_index: int | None,
        accepted_events: list[_AcceptedChunkEvents],
    ) -> PolicyStepResult:
        resolved_index = (
            self._action_queue.next_action_step - 1
            if action_index is None
            else int(action_index)
        )
        buffer_event = self.buffer_event(resolved_index)
        return PolicyStepResult(
            action=action,
            action_index=resolved_index,
            observation_id=None,
            stalled=stalled,
            actions_remaining=buffer_event.remaining,
            timing_events=tuple(event.timing for event in accepted_events),
            buffer_events=(buffer_event,),
            chunk_events=tuple(event.chunk for event in accepted_events),
            merge_events=tuple(event.merge for event in accepted_events),
            queue_merge_events=tuple(
                event.queue for event in accepted_events if event.queue is not None
            ),
        )


def _optional_int(value: object) -> int | None:
    return None if value is None else int(value)


def _chunk_event_from_result(
    *,
    result: ActionChunkResult,
    base_action_index: int,
    accepted_action_index: int,
    chunk_size: int,
) -> ChunkEvent:
    accepted_actions = result.actions[:chunk_size]
    accepted_action_indices = (
        None
        if result.action_indices is None
        else result.action_indices[: len(accepted_actions)]
    )
    return ChunkEvent(
        observation_id=result.observation_id,
        chunk_id=result.chunk_id,
        base_action_index=base_action_index,
        accepted_action_index=accepted_action_index,
        actions=accepted_actions,
        action_indices=accepted_action_indices,
    )


def _merge_event_from_diagnostics(
    *,
    result: ActionChunkResult,
    base_action_index: int,
    accepted_action_index: int,
    diagnostics: dict[str, int | float | str | None],
) -> MergeEvent:
    return MergeEvent(
        observation_id=result.observation_id,
        chunk_id=result.chunk_id,
        base_action_index=base_action_index,
        accepted_action_index=accepted_action_index,
        requested_mode=str(diagnostics["requested_mode"]),
        resolved_mode=str(diagnostics["resolved_mode"]),
        new_action_weight=(
            None
            if diagnostics.get("new_action_weight") is None
            else float(diagnostics["new_action_weight"])
        ),
        correction_steps=_optional_int(diagnostics.get("correction_steps")),
        stale_steps=int(diagnostics.get("stale_steps", 0) or 0),
        overlap_steps=int(diagnostics.get("overlap_steps", 0) or 0),
        resolved_steps=int(diagnostics.get("resolved_steps", 0) or 0),
        rebase_offset_steps=int(diagnostics.get("rebase_offset_steps", 0) or 0),
        first_executable_source_offset=_optional_int(
            diagnostics.get("first_executable_source_offset")
        ),
        max_abs_position_revision=float(
            diagnostics.get("max_abs_position_revision", 0.0) or 0.0
        ),
        transition_steps=_optional_int(diagnostics.get("transition_steps")),
        arm_speed_rad_s=diagnostics.get("arm_speed_rad_s"),
        correction_gain=diagnostics.get("correction_gain"),
        correction_rate_ratio=diagnostics.get("correction_rate_ratio"),
    )


def _config_rtc_enabled(config: Any | None) -> bool:
    if isinstance(config, ResolvedOptimizationConfig):
        return config.rtc == "on"
    return getattr(config, "rtc", None) == "on"


def _rtc_config_from_resolved(config: Any | None) -> RtcConfig | None:
    if not _config_rtc_enabled(config):
        return None
    contract_id = getattr(config, "rtc_contract", None)
    if isinstance(config, dict):
        contract_id = config.get("rtc_contract")
    return RtcConfig(
        enabled=True,
        contract_id=None if contract_id is None else str(contract_id),
    )


def _is_calibrated_static_rtc(config: RtcConfig) -> bool:
    return (config.contract_id or "calibrated_static") == "calibrated_static"


def _reference_actions_from_result(
    result: ActionChunkResult,
) -> Sequence[Sequence[float]] | None:
    metadata = getattr(result.raw_chunk, "runtime_metadata", None)
    if metadata is None:
        return None
    reference_actions = getattr(metadata, "reference_actions", None)
    if reference_actions is None and isinstance(metadata, dict):
        reference_actions = metadata.get("reference_actions")
    return reference_actions


def _timing_event_from_result(result: ActionChunkResult) -> PolicyTimingEvent:
    return PolicyTimingEvent(
        observation_id=result.observation_id,
        chunk_id=result.chunk_id,
        obs_to_action_ms=result.timing.obs_to_action_ms,
        server_queue_ms=result.timing.server_queue_ms,
        server_inference_ms=result.timing.server_inference_ms,
        server_total_ms=result.timing.server_total_ms,
        client_overhead_ms=result.timing.client_overhead_ms,
        transport_send_ms=result.timing.transport_send_ms,
        wait_for_chunk_ms=result.timing.wait_for_chunk_ms,
        quic_rtt_ms=result.timing.quic_rtt_ms,
        transport_mode=result.transport_mode,
        data_plane_rtt_ms=result.timing.data_plane_rtt_ms,
        worker_queue_ms=result.timing.worker_queue_ms,
        worker_preprocess_ms=result.timing.worker_preprocess_ms,
        worker_inference_ms=result.timing.worker_inference_ms,
        worker_postprocess_ms=result.timing.worker_postprocess_ms,
    )
