"""Strict DreamZero observations with synchronous eval and model-native async control."""

from __future__ import annotations

import asyncio
import inspect
import math
import time
from collections.abc import Awaitable, Callable, MutableMapping, Sequence
from dataclasses import dataclass
from typing import Generic, TypeVar

import numpy as np
from PIL import Image

from dreamscale import wire
from dreamscale.model_names import public_model
from dreamscale.policy.runtime.action_smoothing import (
    ResolvedActionSmoothing,
    resolve_motion_smoothing,
)
from dreamscale.policy.runtime.adaptive_smoothing import resolve_adaptive_smoothing
from dreamscale.policy.runtime.contract import runtime_contract_for_model
from dreamscale.policy.telemetry import RunTelemetryAccumulator, publish_run_summary
from dreamscale.policy.types import (
    ActionEvent,
    ActResult,
    BufferEvent,
    DispatchEvent,
    RunContext,
    RunHooks,
    RunResult,
    RunStrategy,
    SamplingMode,
)

DREAMZERO_IMAGE_HEIGHT = 180
DREAMZERO_IMAGE_WIDTH = 320
DREAMZERO_ACTION_HZ = 15.0
DREAMZERO_ACTION_HORIZON = 24
DREAMZERO_REPLAN_STRIDE = 8
DREAMZERO_MAX_CAMERA_SKEW_NS = 50_000_000

Action = tuple[float, ...]
T = TypeVar("T")


@dataclass(frozen=True)
class DreamZeroObservation:
    exterior_frame: np.ndarray
    second_exterior_frame: np.ndarray
    wrist_frame: np.ndarray
    camera_capture_times_ns: tuple[int, int, int]
    joint_positions: tuple[float, ...]
    gripper: float

    @property
    def hold_action(self) -> Action:
        return (*self.joint_positions, self.gripper)

    def to_wire(
        self,
        *,
        session_id: str,
        observation_id: int,
        instruction: str,
    ):
        return self.to_wire_for_step(
            session_id=session_id,
            observation_id=observation_id,
            instruction=instruction,
            source_action_step=-1,
            next_action_step=0,
            control_tick=0,
            replan_epoch=0,
            cache_generation=0,
            sampling="async_8",
        )

    def to_wire_for_step(
        self,
        *,
        session_id: str,
        observation_id: int,
        instruction: str,
        source_action_step: int,
        next_action_step: int,
        control_tick: int,
        replan_epoch: int,
        cache_generation: int,
        sampling: SamplingMode,
    ):
        sampling = resolve_dreamzero_sampling("dreamzero-droid", sampling)
        return wire.build_dreamzero_observation(
            session_id=session_id,
            observation_id=observation_id,
            exterior_frame=self.exterior_frame,
            second_exterior_frame=self.second_exterior_frame,
            wrist_frame=self.wrist_frame,
            camera_capture_times_ns=self.camera_capture_times_ns,
            joint_positions=list(self.joint_positions),
            gripper=self.gripper,
            instruction=instruction,
            source_action_step=source_action_step,
            next_action_step=next_action_step,
            control_tick=control_tick,
            replan_epoch=replan_epoch,
            cache_generation=cache_generation,
            sampling=sampling,
        )


@dataclass(frozen=True)
class DreamZeroLoopProfile:
    model_id: str
    observation_type: type
    action_dim: int
    gripper_indices: tuple[int, ...]
    threshold_grippers: bool
    control_hz: float = DREAMZERO_ACTION_HZ


DREAMZERO_DROID_LOOP_PROFILE = DreamZeroLoopProfile(
    model_id="dreamzero-droid",
    observation_type=DreamZeroObservation,
    action_dim=8,
    gripper_indices=(7,),
    threshold_grippers=True,
)


def dreamzero_loop_profile(model: str) -> DreamZeroLoopProfile:
    if model == DREAMZERO_DROID_LOOP_PROFILE.model_id:
        return DREAMZERO_DROID_LOOP_PROFILE
    if model == "dreamzero-yam":
        from dreamscale.dreamzero_yam import DREAMZERO_YAM_LOOP_PROFILE

        return DREAMZERO_YAM_LOOP_PROFILE
    raise ValueError(f"unsupported DreamZero model: {public_model(model)}")


def resolve_dreamzero_sampling(
    model: str,
    sampling: SamplingMode | None,
) -> SamplingMode:
    if model not in {"dreamzero-droid", "dreamzero-yam"}:
        raise ValueError(f"unsupported DreamZero model: {public_model(model)}")
    if sampling is None:
        return "async_latest" if model == "dreamzero-yam" else "async_8"
    if sampling not in ("upstream_eval", "async_8", "async_latest"):
        raise ValueError(f"unknown DreamZero sampling mode: {sampling!r}")
    if sampling == "async_latest" and model != "dreamzero-yam":
        raise ValueError("async_latest is supported only for dreamzero-yam")
    return sampling


@dataclass(frozen=True)
class ChunkAlignment:
    source_action_step: int
    source_control_tick: int
    replan_epoch: int
    cache_generation: int


@dataclass(frozen=True)
class ChunkReplacement:
    fully_stale: bool
    preserved_committed: int = 0
    replaced_steps: int = 0
    resolved_mode: str = "commit_prefix_replace"
    new_action_weight: float | None = None
    correction_steps: int | None = None
    first_executable_source_offset: int | None = None
    max_abs_position_revision: float = 0.0
    transition_steps: int | None = None
    arm_speed_rad_s: float | None = None
    correction_gain: float | None = None
    correction_rate_ratio: float | None = None


class LatestObservationSlot(Generic[T]):
    def __init__(self) -> None:
        self._queue: asyncio.Queue[T] = asyncio.Queue(maxsize=1)
        self.replaced = 0

    async def put(self, item: T) -> None:
        if self._queue.full():
            self._queue.get_nowait()
            self.replaced += 1
        self._queue.put_nowait(item)

    async def get(self) -> T:
        return await self._queue.get()

    def clear(self) -> None:
        while not self._queue.empty():
            self._queue.get_nowait()


def resize_with_pad(
    frame: np.ndarray,
    *,
    height: int = DREAMZERO_IMAGE_HEIGHT,
    width: int = DREAMZERO_IMAGE_WIDTH,
) -> np.ndarray:
    """OpenPI-faithful aspect-preserving resize into a zero RGB canvas."""
    image = _validate_frame(frame, "frame")
    current_height, current_width = image.shape[:2]
    ratio = max(current_width / width, current_height / height)
    resized_height = int(current_height / ratio)
    resized_width = int(current_width / ratio)
    resized = np.asarray(
        Image.fromarray(image).resize(
            (resized_width, resized_height),
            resample=Image.Resampling.BILINEAR,
        )
    )
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    top = (height - resized_height) // 2
    left = (width - resized_width) // 2
    canvas[top : top + resized_height, left : left + resized_width] = resized
    return canvas


def observation(
    *,
    exterior_frame: np.ndarray,
    second_exterior_frame: np.ndarray,
    wrist_frame: np.ndarray,
    camera_capture_times_ns: Sequence[int],
    joint_positions: Sequence[float],
    gripper: float,
) -> DreamZeroObservation:
    timestamps = tuple(camera_capture_times_ns)
    if len(timestamps) != 3 or any(
        isinstance(value, bool) or not isinstance(value, int) or value < 0 for value in timestamps
    ):
        raise ValueError("camera_capture_times_ns must contain exactly 3 nonnegative integers")
    if max(timestamps) - min(timestamps) > DREAMZERO_MAX_CAMERA_SKEW_NS:
        raise ValueError("camera skew exceeds the 50 ms DreamZero-DROID limit")
    joints = tuple(joint_positions)
    if (
        len(joints) != 7
        or any(isinstance(value, (bool, np.bool_)) for value in joints)
        or any(not math.isfinite(float(value)) for value in joints)
    ):
        raise ValueError("joint_positions must contain exactly 7 finite radians")
    if isinstance(gripper, (bool, np.bool_)) or not math.isfinite(float(gripper)):
        raise ValueError("gripper must be finite and numeric")
    normalized_gripper = float(gripper)
    if not 0.0 <= normalized_gripper <= 1.0:
        raise ValueError("gripper must be between 0 and 1")
    return DreamZeroObservation(
        exterior_frame=resize_with_pad(exterior_frame),
        second_exterior_frame=resize_with_pad(second_exterior_frame),
        wrist_frame=resize_with_pad(wrist_frame),
        camera_capture_times_ns=(int(timestamps[0]), int(timestamps[1]), int(timestamps[2])),
        joint_positions=tuple(float(value) for value in joints),
        gripper=normalized_gripper,
    )


def alignment_from_chunk(chunk) -> ChunkAlignment:
    runtime_metadata = getattr(chunk, "runtime_metadata", None)
    queue = getattr(runtime_metadata, "queue", None)
    if not isinstance(queue, dict):
        raise ValueError("DreamZero chunk is missing source_action_step alignment")
    required = (
        "source_action_step",
        "source_control_tick",
        "replan_epoch",
        "cache_generation",
    )
    missing = [name for name in required if not isinstance(queue.get(name), int)]
    if missing:
        raise ValueError(f"DreamZero chunk is missing {', '.join(missing)} alignment")
    return ChunkAlignment(
        source_action_step=int(queue["source_action_step"]),
        source_control_tick=int(queue["source_control_tick"]),
        replan_epoch=int(queue["replan_epoch"]),
        cache_generation=int(queue["cache_generation"]),
    )


def replace_aligned_chunk(
    buffer: MutableMapping[int, Action],
    *,
    next_action_step: int,
    source_action_step: int,
    actions: Sequence[Sequence[float]],
    commit_prefix_steps: int = 2,
    profile: DreamZeroLoopProfile = DREAMZERO_DROID_LOOP_PROFILE,
    smoothing: ResolvedActionSmoothing | None = None,
    executed_history: Sequence[Sequence[float]] = (),
) -> ChunkReplacement:
    if commit_prefix_steps not in (1, 2):
        raise ValueError("commit_prefix_steps must be 1 or 2")
    if smoothing is not None and smoothing.mode == "output":
        raise ValueError("DreamZero aligned replacement requires joint motion smoothing")
    base = int(source_action_step) + 1
    last = base + len(actions) - 1
    if not actions or last < next_action_step:
        return ChunkReplacement(
            fully_stale=True,
            resolved_mode=(smoothing.mode if smoothing is not None else "commit_prefix_replace"),
            new_action_weight=(smoothing.new_weight if smoothing is not None else None),
            correction_steps=(smoothing.correction_steps if smoothing is not None else None),
        )
    normalized = [_action(action, profile) for action in actions]
    before = dict(buffer)
    committed_until = next_action_step + commit_prefix_steps
    replace_from = max(base, committed_until)
    for step in tuple(buffer):
        if step >= replace_from:
            del buffer[step]
    preserved = 0
    replaced = 0
    first_replaced_step: int | None = None
    resolution = None
    for offset, action in enumerate(normalized):
        step = base + offset
        if step < next_action_step:
            continue
        if step < committed_until and step in buffer:
            preserved += 1
            continue
        buffer[step] = action
        replaced += 1
        if first_replaced_step is None:
            first_replaced_step = step

    if smoothing is not None and (before or executed_history):
        # An unanchored initial chunk has no previous trajectory to reconcile.
        # Keep it exact; a prefix copied from this same new chunk is not old
        # coverage and must not create artificial damping of its own tail.
        if smoothing.correction_steps is None:
            raise AssertionError("motion smoothing requires correction steps")
        # A commit prefix is only committed when those steps already existed in
        # the buffer. If latency aged out the start of the first chunk, its first
        # executable targets are new: join them from the actions the actuator
        # actually held instead of exempting them from motion smoothing.
        motion_from = first_replaced_step if first_replaced_step is not None else replace_from
        if motion_from == base and not executed_history:
            # A future-sourced chunk has no incoming predecessor for offset 0.
            # Keep that aligned target direct and begin with the first delta.
            motion_from += 1
        if motion_from <= last:
            existing_for_motion = dict(before)
            existing_for_motion.update(
                {step: action for step, action in buffer.items() if step < motion_from}
            )
            source_steps = [base + offset for offset in range(len(normalized))]
            inputs = dict(
                next_action_step=motion_from,
                action_steps=source_steps,
                new_actions=normalized,
                existing_actions=existing_for_motion,
                executed_history=(
                    (existing_for_motion[motion_from - 1],)
                    if motion_from - 1 in existing_for_motion
                    else executed_history
                ),
            )
            if smoothing.mode in {"motion_handover", "motion_speed"}:
                resolution = resolve_adaptive_smoothing(**inputs, smoothing=smoothing)
            else:
                resolution = resolve_motion_smoothing(
                    **inputs,
                    new_weight=smoothing.new_weight,
                    correction_steps=smoothing.correction_steps,
                    normalized_gripper_indices=smoothing.normalized_gripper_indices,
                )
            buffer.update(resolution.actions)
    return ChunkReplacement(
        fully_stale=False,
        preserved_committed=preserved,
        replaced_steps=replaced,
        resolved_mode=(smoothing.mode if smoothing is not None else "commit_prefix_replace"),
        new_action_weight=(
            resolution.effective_new_weight
            if resolution is not None and resolution.effective_new_weight is not None
            else smoothing.new_weight
            if smoothing is not None and smoothing.mode != "motion_handover"
            else None
        ),
        correction_steps=(smoothing.correction_steps if smoothing is not None else None),
        first_executable_source_offset=(
            None if first_replaced_step is None else first_replaced_step - base
        ),
        max_abs_position_revision=_max_action_revision(before, buffer),
        transition_steps=resolution.transition_steps if resolution is not None else None,
        arm_speed_rad_s=resolution.arm_speed_rad_s if resolution is not None else None,
        correction_gain=resolution.correction_gain if resolution is not None else None,
        correction_rate_ratio=resolution.correction_rate_ratio if resolution is not None else None,
    )


def _max_action_revision(
    before: MutableMapping[int, Action],
    after: MutableMapping[int, Action],
) -> float:
    maximum = 0.0
    for step in before.keys() & after.keys():
        maximum = max(
            maximum,
            max(
                (abs(old - new) for old, new in zip(before[step], after[step], strict=True)),
                default=0.0,
            ),
        )
    return maximum


async def run_dreamzero_loop(
    *,
    policy,
    instruction: str,
    observe: Callable[[RunContext], object | Awaitable[object]],
    act: Callable[
        [Sequence[float], RunContext],
        ActResult | bool | None | Awaitable[ActResult | bool | None],
    ],
    max_actions: int,
    sampling: SamplingMode | None = None,
    commit_prefix_steps: int = 2,
    timeout_s: float = 60.0,
    profile: DreamZeroLoopProfile | None = None,
    controller=None,
    strategy: RunStrategy | None = None,
    hooks: RunHooks | None = None,
    read_hold_action=None,
) -> RunResult:
    """Drive a DreamZero episode with synchronous or asynchronous capture."""
    if max_actions < 0:
        raise ValueError("max_actions must be nonnegative")
    profile = profile or dreamzero_loop_profile(str(policy.model))
    if policy.model != profile.model_id:
        raise ValueError(f"DreamZero loop profile {profile.model_id} does not match {policy.model}")
    sampling = resolve_dreamzero_sampling(profile.model_id, sampling)

    owns_controller = controller is None
    if owns_controller:
        from dreamscale.policy.dreamzero_runtime import DreamZeroEpisodeController

        controller = DreamZeroEpisodeController(
            policy=policy,
            instruction=instruction,
            sampling=sampling,
            commit_prefix_steps=commit_prefix_steps,
            profile=profile,
            strategy=strategy,
            hooks=hooks,
        )
        await controller.begin()
    assert controller is not None
    try:
        return await _drive_dreamzero_loop(
            controller=controller,
            policy=policy,
            observe=observe,
            act=act,
            max_actions=max_actions,
            timeout_s=timeout_s,
            profile=profile,
            hooks=hooks or RunHooks(),
            read_hold_action=read_hold_action,
        )
    finally:
        if owns_controller:
            await controller.end()


async def _drive_dreamzero_loop(
    *,
    controller,
    policy,
    observe: Callable[[RunContext], object | Awaitable[object]],
    act: Callable[
        [Sequence[float], RunContext],
        ActResult | bool | None | Awaitable[ActResult | bool | None],
    ],
    max_actions: int,
    timeout_s: float,
    profile: DreamZeroLoopProfile,
    hooks: RunHooks,
    read_hold_action=None,
) -> RunResult:
    if controller.sampling == "upstream_eval":
        if read_hold_action is not None or any(
            getattr(hooks, field) is not None for field in hooks.__dataclass_fields__
        ):
            raise ValueError("upstream_eval does not support managed holds or RunHooks")
        result = await _drive_upstream_eval_loop(
            controller=controller,
            policy=policy,
            observe=observe,
            act=act,
            max_actions=max_actions,
            timeout_s=timeout_s,
            profile=profile,
        )
        publish_run_summary(policy, hooks, result)
        return result
    return await _drive_async_dreamzero_loop(
        controller=controller,
        policy=policy,
        observe=observe,
        act=act,
        max_actions=max_actions,
        timeout_s=timeout_s,
        profile=profile,
        hooks=hooks,
        read_hold_action=read_hold_action,
    )


async def _drive_upstream_eval_loop(
    *,
    controller,
    policy,
    observe: Callable[[RunContext], object | Awaitable[object]],
    act: Callable[
        [Sequence[float], RunContext],
        ActResult | bool | None | Awaitable[ActResult | bool | None],
    ],
    max_actions: int,
    timeout_s: float,
    profile: DreamZeroLoopProfile,
) -> RunResult:
    period_s = 1.0 / DREAMZERO_ACTION_HZ
    started = time.monotonic()
    next_action_deadline = started
    actions_executed = 0
    latest_actions_remaining = 0
    latest_stalled = False
    policy_calls = 0
    underruns = 0
    done = False

    for action_index in range(max_actions):
        await _sleep_until(next_action_deadline)
        if action_index % DREAMZERO_REPLAN_STRIDE == 0:
            observation_context = RunContext(
                action_index=action_index,
                observation_id=action_index,
                actions_remaining=latest_actions_remaining,
                stalled=latest_stalled,
                elapsed_s=time.monotonic() - started,
            )
            observation = await _call(observe, observation_context)
            if not isinstance(observation, profile.observation_type):
                raise TypeError(
                    f"{profile.model_id} observe callback must return "
                    f"{profile.observation_type.__name__}"
                )
            observation_id = await controller.submit_observation(
                observation,
                action_index=action_index,
            )
            step_result = await controller.take_action(
                action_index=action_index,
                timeout_s=timeout_s,
                required_observation_id=observation_id,
            )
            next_action_deadline = time.monotonic()
        else:
            step_result = await controller.take_action(
                action_index=action_index,
                timeout_s=timeout_s,
            )

        policy_calls += len(step_result.chunk_events)
        underruns += int(step_result.stalled)
        latest_actions_remaining = step_result.actions_remaining
        latest_stalled = step_result.stalled
        action_context = RunContext(
            action_index=action_index,
            observation_id=action_index,
            actions_remaining=step_result.actions_remaining,
            stalled=step_result.stalled,
            elapsed_s=time.monotonic() - started,
        )
        result = await _call(act, step_result.action, action_context)
        record_act_result = getattr(controller, "record_act_result", None)
        if callable(record_act_result):
            await record_act_result(step_result.action, result)
        actions_executed = action_index + 1
        next_action_deadline = max(
            next_action_deadline + period_s,
            time.monotonic(),
        )
        if result is True or (isinstance(result, ActResult) and result.done):
            done = True
            break

    return RunResult(
        actions=actions_executed,
        policy_calls=policy_calls,
        underruns=underruns,
        done=done,
        elapsed_s=time.monotonic() - started,
        max_actions=max_actions,
        stop_reason="act_callback" if done else "action_limit",
        model=getattr(policy, "model", None),
        region=getattr(policy, "region", None),
        transport_mode=getattr(policy, "transport_mode", None),
    )


async def _drive_async_dreamzero_loop(
    *,
    controller,
    policy,
    observe,
    act,
    max_actions: int,
    timeout_s: float,
    profile: DreamZeroLoopProfile,
    hooks: RunHooks,
    read_hold_action=None,
) -> RunResult:
    from concurrent.futures import ThreadPoolExecutor
    from dataclasses import replace

    from dreamscale.policy.run_loop import (
        _accepted_action,
        _buffer_health,
        _call_user_callback,
        _validate_startup_observation,
    )

    contract = getattr(controller, "_contract", None) or runtime_contract_for_model(
        profile.model_id
    )
    period_s = 1.0 / contract.action_hz
    bootstrap = contract.measured_bootstrap
    started = time.monotonic()
    stop, first_observation, first_dispatch = asyncio.Event(), asyncio.Event(), asyncio.Event()
    current_action_index = latest_actions_remaining = 0
    latest_stalled = False
    latest_observation = None
    first_dispatch_at = first_dispatch_unix_ns = None
    policy_calls = underruns = completed = attempts = startup_holds = execution_underruns = 0
    startup_wait_ms = 0.0
    hold_latch = None
    telemetry = RunTelemetryAccumulator()
    stop_reason, failure = "action_limit", None
    # Capture and dispatch must not block the transport event loop or each other.
    executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="dreamscale-stateful-callback")

    async def call(callback, *args):
        return await _call_user_callback(callback, *args, executor=executor)

    async def capture_loop():
        nonlocal latest_observation
        tick, next_capture_deadline = 0, time.monotonic()
        while not stop.is_set():
            if bootstrap and tick == 1:
                await first_dispatch.wait()
                await _sleep_until(first_dispatch_at + contract.startup_motion_delay_s)
            else:
                await _sleep_until(next_capture_deadline)
            capture_started = time.monotonic()
            step = current_action_index
            ctx = RunContext(
                step, tick, latest_actions_remaining, latest_stalled, time.monotonic() - started
            )
            observation = await call(observe, ctx)
            if not isinstance(observation, profile.observation_type):
                raise TypeError(
                    f"{profile.model_id} observe callback must return "
                    f"{profile.observation_type.__name__}"
                )
            if bootstrap and tick == 1:
                _validate_startup_observation(observation, first_dispatch_unix_ns)
            latest_observation = observation
            # Capture can span several dispatches. Associate it with the current
            # control index, while preserving its actual camera capture times.
            await controller.submit_observation(observation, action_index=current_action_index)
            first_observation.set()
            tick += 1
            next_capture_deadline = max(
                next_capture_deadline + period_s, capture_started + period_s
            )

    def raise_if_capture_stopped():
        if not capture_task.done():
            return
        if not capture_task.cancelled() and capture_task.exception() is not None:
            raise capture_task.exception()
        raise RuntimeError("DreamZero capture loop stopped unexpectedly")

    async def wait_while_capturing(awaitable):
        waiter = asyncio.create_task(awaitable)
        try:
            completed_tasks, _ = await asyncio.wait(
                {waiter, capture_task},
                return_when=asyncio.FIRST_COMPLETED,
            )
            if capture_task in completed_tasks:
                raise_if_capture_stopped()
            return await waiter
        finally:
            if not waiter.done():
                waiter.cancel()
                await asyncio.gather(waiter, return_exceptions=True)

    capture_task = asyncio.create_task(capture_loop(), name="dreamscale-dreamzero-capture")
    try:
        if max_actions:
            await wait_while_capturing(first_observation.wait())
            if bootstrap:
                await wait_while_capturing(controller.wait_for_initial_chunk(timeout_s))
                ctx = RunContext(0, 0, 0, True, time.monotonic() - started)
                anchor = (
                    await call(read_hold_action, ctx)
                    if read_hold_action is not None
                    else latest_observation.hold_action
                )
                await controller.seed_initial_position(anchor)
                startup_wait_ms = (time.monotonic() - started) * 1000
        next_action_deadline = time.monotonic()
        for action_index in range(max_actions):
            await _sleep_until(next_action_deadline)
            raise_if_capture_stopped()
            step = await wait_while_capturing(controller.take_action(action_index, timeout_s))
            policy_calls += len(step.chunk_events)
            underruns += int(step.stalled)
            latest_actions_remaining, latest_stalled = step.actions_remaining, step.stalled
            ctx = RunContext(
                action_index,
                step.observation_id or 0,
                step.actions_remaining,
                step.stalled,
                time.monotonic() - started,
            )
            if step.stalled:
                if first_dispatch.is_set():
                    execution_underruns += 1
                else:
                    startup_holds += 1
                if hold_latch is None:
                    hold_latch = (
                        await call(read_hold_action, ctx)
                        if read_hold_action is not None
                        else latest_observation.hold_action
                    )
                step = replace(step, action=await controller.latch_hold(hold_latch))
            else:
                hold_latch = None
            for event in step.timing_events:
                telemetry.record(event)
            for name, events in (
                ("on_chunk", step.chunk_events),
                ("on_merge", step.merge_events),
                ("on_timing", step.timing_events),
                ("on_queue_merge", step.queue_merge_events),
            ):
                callback = getattr(hooks, name)
                if callback is not None:
                    for event in events:
                        callback(event)
            if hooks.on_action is not None:
                hooks.on_action(
                    ActionEvent(action_index, step.stalled, step.actions_remaining, step.action)
                )
            dispatch_clock, dispatch_started = time.monotonic(), time.monotonic_ns()
            current_action_index = action_index + 1
            attempts += 1
            result = await call(act, step.action, ctx)
            accepted = _accepted_action(result, step.action)
            record = getattr(controller, "record_act_result", None)
            if callable(record):
                await record(step.action, result)
            completed += 1
            if not step.stalled and not first_dispatch.is_set():
                first_dispatch_at, first_dispatch_unix_ns = time.monotonic(), time.time_ns()
                first_dispatch.set()
            if hooks.on_dispatch is not None:
                hooks.on_dispatch(
                    DispatchEvent(
                        action_index,
                        step.stalled,
                        step.action,
                        accepted,
                        dispatch_started,
                        time.monotonic_ns(),
                    )
                )
            if hooks.on_buffer is not None:
                hooks.on_buffer(
                    BufferEvent(
                        action_index,
                        step.actions_remaining,
                        contract.chunk_size,
                        _buffer_health(
                            remaining=step.actions_remaining,
                            capacity=contract.chunk_size,
                            in_flight=True,
                        ),
                        True,
                    )
                )
            next_action_deadline = max(next_action_deadline + period_s, dispatch_clock + period_s)
            if result is True or (isinstance(result, ActResult) and result.done):
                stop_reason = "act_callback"
                break
    except BaseException as exc:
        failure = exc
        stop_reason = (
            "interrupted"
            if isinstance(exc, (asyncio.CancelledError, KeyboardInterrupt))
            else "error"
        )
        raise
    finally:
        stop.set()
        capture_task.cancel()
        cleanup_error = None
        try:
            outcomes = await asyncio.gather(capture_task, return_exceptions=True)
            cleanup_error = next(
                (
                    e
                    for e in outcomes
                    if isinstance(e, BaseException) and not isinstance(e, asyncio.CancelledError)
                ),
                None,
            )
        finally:
            executor.shutdown(wait=True, cancel_futures=True)
        report_error = failure or cleanup_error
        if cleanup_error is not None and failure is None:
            stop_reason = "error"
        summary = RunResult(
            actions=completed,
            policy_calls=policy_calls,
            underruns=underruns,
            done=stop_reason == "act_callback",
            elapsed_s=time.monotonic() - started,
            max_actions=max_actions,
            stop_reason=stop_reason,
            timing=telemetry.summary(),
            model=getattr(policy, "model", None),
            region=getattr(policy, "region", None),
            transport_mode=getattr(policy, "transport_mode", None),
            startup_wait_ms=startup_wait_ms,
            startup_holds=startup_holds,
            execution_underruns=execution_underruns,
            action_attempts=attempts,
            error_type=type(report_error).__name__ if report_error else None,
            loop_cleanup_error_type=type(cleanup_error).__name__ if cleanup_error else None,
        )
        publish_run_summary(policy, hooks, summary, preserve_error=report_error is not None)
        if cleanup_error is not None and failure is None:
            raise cleanup_error
    return summary


def _validate_frame(frame: np.ndarray, name: str) -> np.ndarray:
    if not isinstance(frame, np.ndarray):
        raise TypeError(f"{name} must be a numpy array")
    if frame.dtype != np.uint8 or frame.ndim != 3 or frame.shape[2] != 3:
        raise ValueError(f"{name} must be an HxWx3 uint8 RGB array")
    if frame.shape[0] < 1 or frame.shape[1] < 1:
        raise ValueError(f"{name} must have nonzero dimensions")
    return frame


def _action(values: Sequence[float], profile: DreamZeroLoopProfile) -> Action:
    if len(values) != profile.action_dim:
        raise ValueError(
            f"{profile.model_id} actions must have exactly {profile.action_dim} values"
        )
    action = tuple(float(value) for value in values)
    if any(not math.isfinite(value) for value in action):
        raise ValueError(f"{profile.model_id} actions must be finite")
    if not profile.threshold_grippers:
        return action
    if any(not 0.0 <= action[index] <= 1.0 for index in profile.gripper_indices):
        raise ValueError(f"{profile.model_id} gripper actions must be between 0 and 1")
    mutable = list(action)
    for index in profile.gripper_indices:
        mutable[index] = 1.0 if mutable[index] > 0.5 else 0.0
    return tuple(mutable)


async def _call(callback, *args):
    result = callback(*args)
    if inspect.isawaitable(result):
        return await result
    return result


async def _sleep_until(target: float) -> None:
    delay = target - time.monotonic()
    if delay > 0:
        await asyncio.sleep(delay)


# The earlier name, kept working (the same function).
observe = observation
