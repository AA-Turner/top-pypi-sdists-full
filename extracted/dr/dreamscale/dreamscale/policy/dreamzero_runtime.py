from __future__ import annotations

import asyncio
import sys
import time
from collections import deque
from collections.abc import Sequence
from dataclasses import dataclass, replace
from typing import Any

from dreamscale.dreamzero import (
    DREAMZERO_REPLAN_STRIDE,
    DreamZeroLoopProfile,
    LatestObservationSlot,
    SamplingMode,
    _max_action_revision,
    alignment_from_chunk,
    replace_aligned_chunk,
    resolve_dreamzero_sampling,
)
from dreamscale.policy.runtime.action_smoothing import (
    ResolvedActionSmoothing,
    resolve_action_smoothing,
    resolve_motion_smoothing,
)
from dreamscale.policy.runtime.adaptive_smoothing import resolve_adaptive_smoothing
from dreamscale.policy.runtime.contract import runtime_contract_for_model
from dreamscale.policy.runtime.result import result_from_chunk
from dreamscale.policy.types import (
    ActResult,
    ChunkEvent,
    MergeEvent,
    PolicyStepResult,
    PolicyTimingEvent,
    QueueMergeEvent,
    RequestEvent,
    RunHooks,
    RunStrategy,
    RuntimeStats,
)


@dataclass(frozen=True)
class _BufferedDreamZeroAction:
    action: tuple[float, ...]
    chunk_id: int | None
    source_observation_id: int
    source_control_tick: int
    source_capture_time_ns: int
    replan_epoch: int
    cache_generation: int


@dataclass(frozen=True)
class _SentObservation:
    start_ns: int
    send_start_ns: int
    send_end_ns: int
    source_capture_time_ns: int
    action_index: int


@dataclass(frozen=True)
class _AcceptedDreamZeroChunk:
    timing: PolicyTimingEvent
    chunk: ChunkEvent
    merge: MergeEvent
    queue: QueueMergeEvent | None


@dataclass(frozen=True)
class _PendingObservation:
    observation_id: int
    observation: object
    action_index: int
    enqueue_ns: int


class DreamZeroEpisodeController:
    """Own one DreamZero episode while an external caller owns the action clock."""

    def __init__(
        self,
        *,
        policy: Any,
        instruction: str,
        sampling: SamplingMode,
        commit_prefix_steps: int,
        profile: DreamZeroLoopProfile,
        strategy: RunStrategy | None = None,
        hooks: RunHooks | None = None,
    ) -> None:
        self.policy = policy
        self.instruction = instruction
        self.sampling = sampling
        self.commit_prefix_steps = commit_prefix_steps
        self.profile = profile
        self.hooks = hooks or RunHooks()
        # The session's contract, not the model's: the caller may have chosen a
        # different control_hz at connect, which stretches the chunk's horizon
        # without changing which actions are executed.
        session_contract = getattr(policy, "_runtime_contract", None)
        self._contract = session_contract or runtime_contract_for_model(profile.model_id)
        self._smoothing: ResolvedActionSmoothing | None = None
        if self._contract.joint_groups and sampling != "upstream_eval":
            self._smoothing = resolve_action_smoothing(strategy or RunStrategy(), self._contract)

        self._buffer: dict[int, _BufferedDreamZeroAction] = {}
        self._executed_history: deque[tuple[float, ...]] = deque(maxlen=2)
        self._sent: dict[int, _SentObservation] = {}
        self._accepted_events: list[_AcceptedDreamZeroChunk] = []
        self._slot: LatestObservationSlot[_PendingObservation] = LatestObservationSlot()
        self._state_changed = asyncio.Condition()
        self._next_action_index = 0
        self._latest_hold: tuple[float, ...] | None = None
        self._hold_latch: tuple[float, ...] | None = None
        self._raw_buffer: dict[int, tuple[float, ...]] = {}
        self._handover_end_step: int | None = None
        self._last_requested: tuple[float, ...] | None = None
        self._feedback_changed = False
        self._latest_received_epoch = -1
        self._latest_received_observation_id: int | None = None
        self._sender_task: asyncio.Task[None] | None = None
        self._receiver_task: asyncio.Task[None] | None = None
        self._closed = False

        self._begun = False
        self._cache_generation = -1
        self._latest_observation_id: int | None = None
        self._receiver: Any | None = None
        self._background_error: BaseException | None = None
        self._failure_surfaced = False

    @property
    def cache_generation(self) -> int:
        return self._cache_generation

    @property
    def sender_running(self) -> bool:
        return self._sender_task is not None and not self._sender_task.done()

    @property
    def receiver_running(self) -> bool:
        return self._receiver_task is not None and not self._receiver_task.done()

    async def begin(self) -> None:
        if self._begun:
            raise RuntimeError("DreamZero episode controller has already begun")
        if self._closed:
            raise RuntimeError("DreamZero episode controller is closed")
        if self.sampling not in ("upstream_eval", "async_8", "async_latest"):
            raise ValueError("sampling must be upstream_eval, async_8, or async_latest")
        resolve_dreamzero_sampling(self.profile.model_id, self.sampling)
        if self.commit_prefix_steps not in (1, 2):
            raise ValueError("commit_prefix_steps must be 1 or 2")
        if self.policy.model != self.profile.model_id:
            raise ValueError(
                f"DreamZero loop profile {self.profile.model_id} does not match {self.policy.model}"
            )

        self._begun = True
        self._cache_generation = int(getattr(self.policy, "_dreamzero_generation", -1)) + 1
        self.policy._dreamzero_generation = self._cache_generation
        if not hasattr(self.policy, "_observation_id"):
            self.policy._observation_id = 0
        transport = self.policy._connection.transport
        self._receiver = transport.action_chunks().__aiter__()
        self._sender_task = asyncio.create_task(
            self._run_sender(),
            name="dreamscale-dreamzero-sender",
        )
        self._receiver_task = asyncio.create_task(
            self._run_receiver(),
            name="dreamscale-dreamzero-receiver",
        )

    async def submit_observation(self, observation: object, action_index: int) -> int:
        async with self._state_changed:
            self._require_active_locked()
            self._raise_if_failed_locked()
            if self.sampling == "upstream_eval" and action_index % DREAMZERO_REPLAN_STRIDE != 0:
                raise ValueError("upstream_eval submits observations only at boundaries")
            self._record_observation_locked(observation, action_index)
            if self.sampling == "upstream_eval":
                self._discard_buffer_from(action_index)
            observation_id = int(self.policy._observation_id)
            self.policy._observation_id = observation_id + 1
            self._latest_observation_id = observation_id
            pending = _PendingObservation(
                observation_id=observation_id,
                observation=observation,
                action_index=action_index,
                enqueue_ns=time.monotonic_ns(),
            )
            await self._slot.put(pending)
            return observation_id

    async def take_action(
        self,
        action_index: int,
        timeout_s: float,
        *,
        required_observation_id: int | None = None,
    ) -> PolicyStepResult:
        async with self._state_changed:
            self._require_active_locked()
            self._raise_if_failed_locked()
            if action_index != self._next_action_index:
                raise ValueError(
                    f"expected action_index {self._next_action_index}, got {action_index}"
                )

            if self.sampling == "upstream_eval" and action_index % DREAMZERO_REPLAN_STRIDE == 0:
                if required_observation_id is None:
                    raise ValueError("upstream_eval boundary requires a submitted observation")
                if required_observation_id != self._latest_observation_id:
                    raise ValueError(
                        "upstream_eval boundary observation is not the latest submission"
                    )
                try:
                    async with asyncio.timeout(timeout_s):
                        while self._latest_received_observation_id != required_observation_id:
                            self._raise_if_failed_locked()
                            await self._state_changed.wait()
                except TimeoutError as exc:
                    raise TimeoutError(
                        f"DreamZero returned no action chunk for observation "
                        f"{required_observation_id} within {timeout_s:g} s"
                    ) from exc
                self._raise_if_failed_locked()

            buffered = self._buffer.pop(action_index, None)
            if buffered is None:
                if self._latest_hold is None:
                    raise RuntimeError("DreamZero cannot hold before receiving an observation")
                if self._hold_latch is None:
                    self._hold_latch = self._latest_hold
                action = self._hold_latch
                stalled = True
                source_chunk_id = None
                source_observation_id = None
                source_control_tick = None
                source_capture_to_execution_ms = None
                replan_epoch = action_index // DREAMZERO_REPLAN_STRIDE
                cache_generation = self._cache_generation
                self._record_stats(underruns=1, hold_position_count=1)
            else:
                self._hold_latch = None
                action = buffered.action
                stalled = False
                source_chunk_id = buffered.chunk_id
                source_observation_id = buffered.source_observation_id
                source_control_tick = buffered.source_control_tick
                source_capture_to_execution_ms = max(
                    0.0,
                    (time.time_ns() - buffered.source_capture_time_ns) / 1_000_000,
                )
                replan_epoch = buffered.replan_epoch
                cache_generation = buffered.cache_generation
            self._executed_history.append(action)
            self._last_requested = action
            self._raw_buffer.pop(action_index, None)
            self._next_action_index += 1
            actions_remaining = self._contiguous_actions(self._next_action_index)
            accepted_events = tuple(self._accepted_events)
            self._accepted_events.clear()
            return PolicyStepResult(
                action=action,
                action_index=action_index,
                observation_id=self._latest_observation_id,
                stalled=stalled,
                actions_remaining=actions_remaining,
                source_chunk_id=source_chunk_id,
                source_observation_id=source_observation_id,
                source_control_tick=source_control_tick,
                source_capture_to_execution_ms=source_capture_to_execution_ms,
                replan_epoch=replan_epoch,
                cache_generation=cache_generation,
                timing_events=tuple(event.timing for event in accepted_events),
                chunk_events=tuple(event.chunk for event in accepted_events),
                merge_events=tuple(event.merge for event in accepted_events),
                queue_merge_events=tuple(
                    event.queue for event in accepted_events if event.queue is not None
                ),
            )

    async def record_act_result(
        self,
        requested_action: Sequence[float],
        result: ActResult | bool | None,
    ) -> None:
        requested = tuple(float(value) for value in requested_action)
        accepted = requested
        if isinstance(result, ActResult) and result.accepted_action is not None:
            if len(result.accepted_action) != len(requested):
                raise ValueError("accepted_action dimension must match the requested action")
            accepted = result.accepted_action
        async with self._state_changed:
            self._require_active_locked()
            self._raise_if_failed_locked()
            if not self._executed_history:
                raise RuntimeError("cannot record actuator feedback before an action")
            if self._last_requested != requested:
                raise RuntimeError("actuator feedback does not match the latest action")
            self._executed_history[-1] = accepted
            indices = self._contract.joint_indices or tuple(range(len(requested)))
            self._feedback_changed = self._feedback_changed or any(
                accepted[i] != requested[i] for i in indices
            )

    async def wait_for_initial_chunk(self, timeout_s: float) -> None:
        async with self._state_changed, asyncio.timeout(timeout_s):
            while 0 not in self._buffer:
                self._require_active_locked()
                self._raise_if_failed_locked()
                await self._state_changed.wait()

    async def seed_initial_position(self, action: Sequence[float]) -> None:
        from dreamscale.dreamzero import _action

        anchor = _action(action, self.profile)
        async with self._state_changed:
            if self._next_action_index != 0:
                raise RuntimeError("initial position must be seeded before dispatch")
            self._executed_history.clear()
            self._executed_history.append(anchor)
            if self._smoothing is None or not self._raw_buffer:
                return
            inputs = dict(
                next_action_step=0,
                action_steps=sorted(self._raw_buffer),
                new_actions=[self._raw_buffer[i] for i in sorted(self._raw_buffer)],
                existing_actions={},
                executed_history=(anchor,),
            )
            if self._smoothing.mode in {"motion_handover", "motion_speed"}:
                resolved = resolve_adaptive_smoothing(**inputs, smoothing=self._smoothing)
            else:
                resolved = resolve_motion_smoothing(
                    **inputs,
                    new_weight=self._smoothing.new_weight,
                    correction_steps=self._smoothing.correction_steps,
                    normalized_gripper_indices=self._smoothing.normalized_gripper_indices,
                )
            for step, target in resolved.actions.items():
                self._buffer[step] = replace(self._buffer[step], action=target)
            self._handover_end_step = (resolved.transition_steps or 0) - 1
            # The first merge event must describe the actual seeded queue.
            if self._accepted_events:
                event = self._accepted_events[-1]
                self._accepted_events[-1] = replace(
                    event,
                    merge=replace(
                        event.merge,
                        transition_steps=resolved.transition_steps,
                        arm_speed_rad_s=resolved.arm_speed_rad_s,
                        correction_gain=resolved.correction_gain,
                        correction_rate_ratio=resolved.correction_rate_ratio,
                        new_action_weight=(
                            resolved.effective_new_weight
                            if resolved.effective_new_weight is not None
                            else None
                            if self._smoothing.mode == "motion_handover"
                            else self._smoothing.new_weight
                        ),
                    ),
                    queue=replace(
                        event.queue,
                        after=tuple((i, v.action) for i, v in sorted(self._buffer.items())),
                    )
                    if event.queue is not None
                    else None,
                )

    async def latch_hold(self, action: Sequence[float]) -> tuple[float, ...]:
        from dreamscale.dreamzero import _action

        target = _action(action, self.profile)
        async with self._state_changed:
            self._hold_latch = target
            self._last_requested = target
            self._executed_history[-1] = target
        return target

    async def step(
        self,
        observation: object,
        action_index: int,
        timeout_s: float,
    ) -> PolicyStepResult:
        boundary = action_index % DREAMZERO_REPLAN_STRIDE == 0
        observation_id: int | None = None
        if self.sampling != "upstream_eval" or boundary:
            observation_id = await self.submit_observation(observation, action_index)
        else:
            async with self._state_changed:
                self._require_active_locked()
                self._raise_if_failed_locked()
                self._record_observation_locked(observation, action_index)
        result = await self.take_action(
            action_index,
            timeout_s,
            required_observation_id=(
                observation_id if self.sampling == "upstream_eval" and boundary else None
            ),
        )
        await asyncio.sleep(0)
        async with self._state_changed:
            self._raise_if_failed_locked()
        return result

    async def end(self) -> None:
        if self._closed:
            return
        caller_exception_active = sys.exc_info()[0] is not None
        async with self._state_changed:
            self._closed = True
            self._state_changed.notify_all()

        tasks = tuple(task for task in (self._sender_task, self._receiver_task) if task is not None)
        for task in tasks:
            task.cancel()
        results = await asyncio.gather(*tasks, return_exceptions=True)
        failure = self._background_error
        if failure is None:
            failure = next(
                (
                    result
                    for result in results
                    if isinstance(result, BaseException)
                    and not isinstance(result, asyncio.CancelledError)
                ),
                None,
            )

        close_receiver = getattr(self._receiver, "aclose", None)
        close_failure: BaseException | None = None
        if callable(close_receiver):
            try:
                await close_receiver()
            except BaseException as exc:
                close_failure = exc

        self._sender_task = None
        self._receiver_task = None
        self._receiver = None
        self._slot.clear()
        self._buffer.clear()
        self._raw_buffer.clear()
        self._executed_history.clear()
        self._sent.clear()
        self._accepted_events.clear()
        self._latest_hold = None
        self._hold_latch = None
        self._latest_observation_id = None
        self._latest_received_observation_id = None
        if failure is None:
            failure = close_failure
        if failure is not None and not self._failure_surfaced and not caller_exception_active:
            self._failure_surfaced = True
            raise failure

    async def _run_sender(self) -> None:
        await self._run_background("sender", self._sender_loop)

    async def _run_receiver(self) -> None:
        await self._run_background("receiver", self._receiver_loop)

    async def _sender_loop(self) -> None:
        while True:
            pending = await self._slot.get()
            wire_observation = pending.observation.to_wire_for_step(
                session_id=self.policy.session_id,
                observation_id=pending.observation_id,
                instruction=self.instruction,
                source_action_step=pending.action_index - 1,
                next_action_step=pending.action_index,
                control_tick=pending.action_index,
                replan_epoch=pending.action_index // DREAMZERO_REPLAN_STRIDE,
                cache_generation=self._cache_generation,
                sampling=self.sampling,
            )
            send_start_ns = time.monotonic_ns()
            if self.hooks.on_request is not None:
                self.hooks.on_request(
                    RequestEvent(
                        send_start_ns,
                        pending.action_index,
                        self._contiguous_actions(self._next_action_index),
                        pending.observation,
                    )
                )
            await self.policy._connection.transport.send_observation(wire_observation)
            send_end_ns = time.monotonic_ns()
            async with self._state_changed:
                self._sent[pending.observation_id] = _SentObservation(
                    start_ns=pending.enqueue_ns,
                    send_start_ns=send_start_ns,
                    send_end_ns=send_end_ns,
                    source_capture_time_ns=max(pending.observation.camera_capture_times_ns),
                    action_index=pending.action_index,
                )
                self._record_stats(requests_submitted=1)
                self._state_changed.notify_all()

    async def _receiver_loop(self) -> None:
        assert self._receiver is not None
        async for chunk in self._receiver:
            alignment = alignment_from_chunk(chunk)
            if alignment.cache_generation != self._cache_generation:
                self._record_stats(stale_chunks_dropped=1)
                continue
            indices = tuple(int(action.action_index) for action in chunk.actions)
            # Always the model's native horizon: the server emits at the
            # native rate regardless of what the caller executes at.
            action_horizon = runtime_contract_for_model(self.profile.model_id).chunk_size
            if indices != tuple(range(action_horizon)):
                raise ValueError(
                    f"DreamZero chunks must contain action indices 0 through {action_horizon - 1}"
                )
            observation_id = int(chunk.generated_from_observation_id)
            if self.sampling == "upstream_eval" and observation_id != self._latest_observation_id:
                raise RuntimeError(
                    "received upstream_eval action chunk for unexpected observation "
                    f"{observation_id}; expected {self._latest_observation_id}"
                )
            if (
                self.sampling == "upstream_eval"
                and observation_id == self._latest_received_observation_id
            ):
                raise RuntimeError(
                    "received duplicate upstream_eval action chunk for observation "
                    f"{observation_id}"
                )
            sent = await self._wait_for_sent_observation(observation_id)
            if self.sampling == "upstream_eval" and (
                alignment.source_action_step != sent.action_index - 1
                or alignment.source_control_tick != sent.action_index
                or alignment.replan_epoch != sent.action_index // DREAMZERO_REPLAN_STRIDE
            ):
                raise RuntimeError(
                    "received upstream_eval action chunk with unexpected source alignment"
                )
            result = result_from_chunk(
                observation_id=observation_id,
                chunk=chunk,
                start_ns=sent.start_ns,
                send_start_ns=sent.send_start_ns,
                send_end_ns=sent.send_end_ns,
                end_ns=time.monotonic_ns(),
                transport=self.policy._connection.transport,
            )
            async with self._state_changed:
                if self._closed:
                    continue
                accepted_action_index = self._next_action_index
                base_action_index = alignment.source_action_step + 1
                old_buffer = dict(self._buffer)
                before_raw = dict(self._raw_buffer)
                raw_buffer = {step: buffered.action for step, buffered in old_buffer.items()}
                replacement = replace_aligned_chunk(
                    raw_buffer,
                    next_action_step=self._next_action_index,
                    source_action_step=alignment.source_action_step,
                    actions=result.actions,
                    commit_prefix_steps=self.commit_prefix_steps,
                    profile=self.profile,
                    smoothing=self._smoothing,
                    executed_history=tuple(self._executed_history),
                )
                if not replacement.fully_stale:
                    preserve_before = max(
                        base_action_index,
                        self._next_action_index + self.commit_prefix_steps,
                    )
                    sources = {
                        base_action_index + i: action for i, action in enumerate(result.actions)
                    }
                    overlap = sources.keys() & before_raw.keys()
                    if self._smoothing is not None and self._smoothing.mode == "motion_handover":
                        unchanged = (
                            bool(overlap)
                            and self._handover_end_step is not None
                            and max(sources) >= self._handover_end_step
                            and not self._feedback_changed
                            and all(
                                before_raw[i][j] == sources[i][j]
                                for i in overlap
                                for j in self._contract.joint_indices
                            )
                        )
                        if unchanged:
                            for i in raw_buffer:
                                if i in old_buffer:
                                    raw_buffer[i] = tuple(
                                        sources[i][j]
                                        if i >= preserve_before
                                        and j in self._contract.gripper_indices
                                        else value
                                        for j, value in enumerate(old_buffer[i].action)
                                    )
                            replacement = replace(
                                replacement,
                                max_abs_position_revision=_max_action_revision(
                                    {i: v.action for i, v in old_buffer.items()}, raw_buffer
                                ),
                                transition_steps=max(
                                    0,
                                    self._handover_end_step - self._next_action_index + 1,
                                ),
                                correction_rate_ratio=None,
                            )
                        else:
                            first = base_action_index + (
                                replacement.first_executable_source_offset or 0
                            )
                            self._handover_end_step = (
                                first + (replacement.transition_steps or 0) - 1
                            )
                    self._feedback_changed = False
                    self._raw_buffer = {
                        i: before_raw[i] if i < preserve_before and i in before_raw else sources[i]
                        for i in raw_buffer
                        if i in before_raw or i in sources
                    }
                    self._buffer = {
                        step: (
                            old_buffer[step]
                            if step in old_buffer and step < preserve_before
                            else _BufferedDreamZeroAction(
                                action=action,
                                chunk_id=result.chunk_id,
                                source_observation_id=result.observation_id,
                                source_control_tick=alignment.source_control_tick,
                                source_capture_time_ns=sent.source_capture_time_ns,
                                replan_epoch=alignment.replan_epoch,
                                cache_generation=alignment.cache_generation,
                            )
                        )
                        for step, action in raw_buffer.items()
                    }
                timing = self._timing_event(result)
                chunk_event = ChunkEvent(
                    observation_id=result.observation_id,
                    chunk_id=result.chunk_id,
                    base_action_index=base_action_index,
                    accepted_action_index=accepted_action_index,
                    actions=(),
                    action_indices=result.action_indices,
                )
                merge = MergeEvent(
                    observation_id=result.observation_id,
                    chunk_id=result.chunk_id,
                    base_action_index=base_action_index,
                    accepted_action_index=self._next_action_index,
                    requested_mode=f"dreamzero_{self.sampling}",
                    resolved_mode=(
                        "fully_stale" if replacement.fully_stale else replacement.resolved_mode
                    ),
                    new_action_weight=replacement.new_action_weight,
                    correction_steps=replacement.correction_steps,
                    stale_steps=max(0, self._next_action_index - base_action_index),
                    overlap_steps=replacement.preserved_committed,
                    resolved_steps=replacement.replaced_steps,
                    rebase_offset_steps=0,
                    first_executable_source_offset=(replacement.first_executable_source_offset),
                    max_abs_position_revision=(replacement.max_abs_position_revision),
                    transition_steps=replacement.transition_steps,
                    arm_speed_rad_s=replacement.arm_speed_rad_s,
                    correction_gain=replacement.correction_gain,
                    correction_rate_ratio=replacement.correction_rate_ratio,
                )
                self._latest_received_epoch = max(
                    self._latest_received_epoch,
                    alignment.replan_epoch,
                )
                self._latest_received_observation_id = observation_id
                self._accepted_events.append(
                    _AcceptedDreamZeroChunk(
                        timing=timing,
                        chunk=chunk_event,
                        merge=merge,
                        queue=QueueMergeEvent(
                            sent.start_ns,
                            time.monotonic_ns(),
                            replace(chunk_event, actions=tuple(result.actions)),
                            tuple((i, v.action) for i, v in sorted(old_buffer.items())),
                            tuple(sorted(before_raw.items())),
                            tuple((i, v.action) for i, v in sorted(self._buffer.items())),
                        )
                        if self.hooks.on_queue_merge is not None
                        else None,
                    )
                )
                self._record_stats(chunks_received=1)
                self._state_changed.notify_all()

    async def _wait_for_sent_observation(self, observation_id: int) -> _SentObservation:
        async with self._state_changed:
            while observation_id not in self._sent:
                if self._closed:
                    raise asyncio.CancelledError
                if self._background_error is not None:
                    raise self._background_error
                await self._state_changed.wait()
            return self._sent[observation_id]

    async def _run_background(self, name: str, loop: Any) -> None:
        try:
            await loop()
            if not self._closed:
                raise RuntimeError(f"DreamZero {name} loop stopped unexpectedly")
        except asyncio.CancelledError:
            raise
        except BaseException as exc:
            async with self._state_changed:
                if self._background_error is None:
                    self._background_error = exc
                self._state_changed.notify_all()
            raise

    def _require_active_locked(self) -> None:
        if not self._begun:
            raise RuntimeError("DreamZero episode controller has not begun")
        if self._closed:
            raise RuntimeError("DreamZero episode controller is closed")

    def _raise_if_failed_locked(self) -> None:
        if self._background_error is not None:
            self._failure_surfaced = True
            raise self._background_error

    def _record_observation_locked(self, observation: object, action_index: int) -> None:
        if action_index != self._next_action_index and not (
            self.sampling != "upstream_eval"
            and self._next_action_index > 0
            and action_index == self._next_action_index - 1
        ):
            raise ValueError(f"expected action_index {self._next_action_index}, got {action_index}")
        if not isinstance(observation, self.profile.observation_type):
            raise TypeError(
                f"{self.profile.model_id} observation must be "
                f"{self.profile.observation_type.__name__}"
            )
        self._latest_hold = tuple(observation.hold_action)

    def _discard_buffer_from(self, action_index: int) -> None:
        for step in tuple(self._buffer):
            if step >= action_index:
                del self._buffer[step]

    def _contiguous_actions(self, start: int) -> int:
        count = 0
        while start + count in self._buffer:
            count += 1
        return count

    def _record_stats(self, **increments: int) -> None:
        stats = getattr(self.policy, "runtime_stats", None)
        if not isinstance(stats, RuntimeStats):
            return
        for name, increment in increments.items():
            setattr(stats, name, int(getattr(stats, name)) + int(increment))

    @staticmethod
    def _timing_event(result: Any) -> PolicyTimingEvent:
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
