from __future__ import annotations

import asyncio
import contextvars
import dataclasses
import enum
import inspect
import math
import time
import types
from collections.abc import Awaitable, Callable, Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress
from dataclasses import replace
from itertools import count
from typing import Any, Literal, TypeVar

import numpy as np
from dreamscale_transport import (
    PROTOCOL_VERSION,
    EpisodeRequestContext,
    Observation,
    RtcRequestContext,
    RuntimeRequestContext,
)
from dreamscale_transport.images import WireImage
from dreamscale_transport.send_hints import SendHint, send_hint
from dreamscale_transport.websocket_client import (
    CONTEXT_CAPABILITY,
    HISTORY_FRAMES_CAPABILITY,
)

from dreamscale import errors, region_hint, wire
from dreamscale.model_names import internal_model, public_model
from dreamscale.policy.calibration_cache import (
    load_session_calibration,
    save_session_calibration,
)
from dreamscale.policy.config import (
    Acceleration,
    Calibration,
    OptimizationConfig,
    RequestedCalibration,
    RequestedControl,
    ResolvedOptimizationConfig,
    Rtc,
)
from dreamscale.policy.context import (
    EpisodeObservation,
    EpisodeTicks,
    ObservationHistory,
    TickHistory,
)
from dreamscale.policy.deployment import (
    check_observation,
    deployment_only_base,
    session_base,
    with_vector_state,
)
from dreamscale.policy.exported_deployments import exported_base
from dreamscale.policy.lifecycle import (
    DEFAULT_CONNECT_IDLE_TIMEOUT_S,
    _cleanup_connect_failure,
    _LoopRunner,
    open_policy_connection,
)
from dreamscale.policy.run_loop import (
    AsyncActionController,
    _accepted_action,
    _hold_position_action,
    _validate_hold_action,
    require_run_hold,
    run_policy_loop,
)
from dreamscale.policy.runtime.action_smoothing import resolve_action_smoothing
from dreamscale.policy.runtime.calibration import (
    NETWORK_CALIBRATION_TIME_BUDGET_S,
    NetworkCalibrationConfig,
    NetworkCalibrationProfile,
    NetworkCalibrationSample,
    build_network_calibration_profile,
)
from dreamscale.policy.runtime.contract import (
    RuntimeContract,
    follows_server_contract,
    resolve_control_hz,
    resolve_runtime_contract,
    runtime_contract_for_model,
)
from dreamscale.policy.runtime.result import (
    _data_plane_rtt_sample,
    _finite_ms,
    result_from_chunk,
)
from dreamscale.policy.runtime.rtc import (
    RtcConfig,
    RtcGeometryProfile,
    RtcProfileSet,
    build_rtc_context_for_queue,
    build_rtc_estimator_state_from_calibration,
    build_rtc_profile_set,
)
from dreamscale.policy.runtime.server_report import record_server_report
from dreamscale.policy.telemetry import RunTelemetryAccumulator, publish_run_summary
from dreamscale.policy.types import (
    ActionChunkResult,
    ActionEvent,
    ActResult,
    DispatchEvent,
    ObservationLike,
    PolicyStepResult,
    ProviderPreference,
    RegionPreference,
    RunContext,
    RunHooks,
    RunResult,
    RunStrategy,
    RuntimeStats,
    SpeedPreference,
    TransportMode,
    TransportPreference,
)
from dreamscale.terminal import (
    describe_runtime_summary,
    format_run_summary,
    make_progress_printer,
)

# Matches the CLI's --keep-warm default (DEFAULT_CLI_KEEP_WARM_S).
DEFAULT_PUBLIC_KEEP_WARM_S = 300

# Shared-endpoint models: at most one request per session every 400 ms, measured send
# to send (a slow answer never adds to it), with one request in flight per session.
MIN_SEND_INTERVAL_S = 0.4


# Send-phase hints (DSL-266): a shared endpoint may say when it wants the next request. A hint
# only ever delays a send past the floor, by at most the endpoint's slot spacing (capped at the
# floor and at 50 ms), or 25 ms when it sends none.
DEFAULT_PHASE_SPACING_S = 0.025
MAX_PHASE_SPACING_S = 0.05


def next_send_at(
    *, last_send_at: float, last_response_at: float | None, floor_s: float,
    hint: SendHint | None = None,
) -> float:
    """When the next request may go: ``max(last send + floor, last response)``; with a hint
    received at ``last_response_at``, its instant clamped into ``[that, that + spacing]``."""
    receipt = last_response_at or 0.0
    earliest = max(last_send_at + floor_s, receipt)
    if hint is None or last_response_at is None:
        return earliest
    if hint.phase_spacing_ms is not None:
        spacing_s = min(hint.phase_spacing_ms / 1000.0, floor_s, MAX_PHASE_SPACING_S)
    else:
        spacing_s = DEFAULT_PHASE_SPACING_S
    latest = max(last_send_at + floor_s + spacing_s, receipt)
    return min(max(receipt + hint.next_send_in_ms / 1000.0, earliest), latest)


_T = TypeVar("_T")


class SendFloorTimeout(TimeoutError):
    """The caller's budget ends before the next send is allowed. Never a lost link."""


def send_floor_s(
    model: str | None,
    *,
    deployment: str | None = None,
    steady_send: bool | int | None = None,
) -> float:
    """The minimum send-to-send interval: 0 unless ``steady_send`` is on and ``model`` is a
    shared endpoint (``True`` = 400 ms, an int = that many ms, 50–2000). Deployments and
    non-shared models never wait. Experimental and undocumented."""
    from dreamscale.model_names import internal_model
    from dreamscale.models_cmd import SHARED_MODELS

    floor_s = resolve_steady_send(steady_send)
    if not floor_s or model is None or deployment is not None:
        return 0.0
    shared = {internal_model(name) for name in SHARED_MODELS}
    return floor_s if internal_model(model) in shared else 0.0


def resolve_steady_send(steady_send: bool | int | None) -> float:
    """``None``/``False`` → 0; ``True`` → 0.4 s; an int → that many milliseconds."""
    if steady_send is None or steady_send is False:
        return 0.0
    if steady_send is True:
        return MIN_SEND_INTERVAL_S
    if isinstance(steady_send, bool) or not isinstance(steady_send, int):
        raise ValueError(
            "steady_send must be True (400 ms), an int in milliseconds (50 to 2000), "
            "or None/False"
        )
    if not 50 <= steady_send <= 2000:
        raise ValueError("steady_send must be between 50 and 2000 milliseconds")
    return steady_send / 1000.0


_MIN_CALIBRATION_SAMPLE_BUDGET_S = 0.25
_MAX_CALIBRATION_SAMPLE_BUDGET_S = 2.0
_CALIBRATION_OBSERVED_RTT_GUARD_RATIO = 0.75
# Allow image delivery and inference to finish before retrying over HTTPS.
# This is a result wait on an established QUIC connection, not a handshake timeout.
_AUTO_QUIC_RESULT_TIMEOUT_S = 10.0

# Keep the former private import available to existing SDK integrations while
# all runtime code uses the shared public conversion helper.
_result_from_chunk = result_from_chunk

# Perceptron Isaac 0.5 endpoints: tasks are prepared before the first observation.
ISAAC05_MODELS = frozenset({
    "perceptron-isaac05", "perceptron-isaac05-yam", "perceptron-isaac05-so101",
})
# Models whose observation window a session can switch (3 frames on, 1 frame off).
CONTEXT_MODELS = ISAAC05_MODELS
Context = Literal["auto", "on", "off"]


def _validate_context(model: str, context: str) -> str:
    if context not in ("auto", "on", "off"):
        raise ValueError('context must be "auto", "on" or "off"')
    if context != "auto" and model not in CONTEXT_MODELS:
        raise ValueError(
            f"{public_model(model)} has no observation context to switch; use context=\"auto\""
        )
    return context


class AsyncRemotePolicy:
    def __init__(
        self,
        *,
        model: str,
        connection: Any,
        control_hz: float | None = None,
        context: Context = "auto",
        deployment: str | None = None,
        steady_send: bool | int | None = None,
    ) -> None:
        self.model = model
        # Observation history for windowed policies: "auto" follows the checkpoint.
        self.context = _validate_context(model, context)
        self.observation_history: ObservationHistory | None = None
        self.session_id = connection.session.session_id
        self.region = connection.session.routed_region or connection.session.region
        self._target_key = connection.session.target_key
        # The server-confirmed hardware tier; "fast" only when the session echoed it.
        self.speed = getattr(connection.session, "speed", None) or "standard"
        self.resolved_optimization_config = connection.session.resolved_optimization_config
        # A base whose sessions carry their robot (π0.5's deployments): the robot the
        # deployment serves; every observation is checked against it before it is sent.
        session = session_base(model)
        self.deployment = (
            session.parse(getattr(connection.session, "deployment", None))
            if session is not None
            else None
        )
        exported = exported_base(model)
        if exported is not None:
            # The deployment block is the whole contract (exported_deployments).
            self.deployment = exported.parse(connection.session.deployment)
        self._runtime_contract = resolve_runtime_contract(
            model=model,
            resolved_config=self.resolved_optimization_config,
            control_hz=control_hz,
            deployment=self.deployment,
        )
        # A deployment says what its server consumes; a bad spec fails the session here.
        declared = getattr(connection.session, "deployment", None)
        declared = declared.get("wire_image") if isinstance(declared, Mapping) else None
        if declared is not None:
            self._runtime_contract = replace(
                self._runtime_contract, wire_image=WireImage.from_json(declared)
            )
        self.action_hz = self._runtime_contract.action_hz
        self.native_action_hz = self._runtime_contract.native_hz
        self.chunk_size = self._runtime_contract.chunk_size
        contract = self._runtime_contract
        capabilities = getattr(connection.transport, "capabilities", ())
        self.wire_image = (
            contract.legacy_wire_image
            if contract.legacy_wire_image is not None and CONTEXT_CAPABILITY not in capabilities
            else contract.wire_image
        )
        # Older frames at fixed offsets (FLUX 3 Action SO-101's t-7 snapshot), where the server
        # takes them; otherwise each request carries its current frames only.
        if contract.episode_tick_steps:
            # The server keeps the episode (Verne V0.5): every tick's frames go ahead.
            if HISTORY_FRAMES_CAPABILITY not in capabilities:
                raise ValueError("this deployment's server takes no history frames; it needs "
                                 "the episode's frames sent ahead")
            self.observation_history = EpisodeTicks(
                contract.episode_tick_steps, contract.execution_chunk_size,
                measured_steps=contract.measured_state_steps)
        elif contract.history_ticks:
            # Hy-VLA: the frames 25-5 executed ticks back travel in each request's strips; a
            # server without history frames would read a strip as one wide frame.
            if HISTORY_FRAMES_CAPABILITY not in capabilities:
                raise ValueError("this deployment's server takes no history frames; it needs "
                                 "the frames from earlier ticks of the episode")
            self.observation_history = TickHistory(contract.history_ticks,
                                                   start=contract.history_start)
        elif contract.history_anchor:
            if HISTORY_FRAMES_CAPABILITY not in capabilities:
                raise ValueError("this deployment's server takes no history frames; it needs "
                                 "the episode's first and recent frames")
            from dreamscale.policy.context import EpisodeHistory

            self.observation_history = EpisodeHistory(contract.history_offsets[0])
        elif (contract.history_offsets or contract.measured_state_steps) and (
            HISTORY_FRAMES_CAPABILITY in capabilities
        ):
            self.observation_history = ObservationHistory.at_offsets(
                contract.history_offsets, 1.0 / self.native_action_hz,
                state_steps=contract.measured_state_steps,
            )
        self.control = self.resolved_optimization_config.control
        self._connection = connection
        self._connection_timing_monotonic = dict(
            getattr(connection, "diagnostic_timing_monotonic", None) or {}
        )
        self._chunks = connection.transport.action_chunks().__aiter__()
        self._observation_id = 0
        self._predict_lock = asyncio.Lock()
        self._prepared_run_active = False
        self._pending_chunk: asyncio.Task[Any] | None = None
        self._background_tasks: set[asyncio.Task[Any]] = set()
        self.runtime_stats = RuntimeStats()
        self._calibration_profile: NetworkCalibrationProfile | None = None
        self._action_controller = AsyncActionController(policy=self)
        self._dreamzero_episode: Any | None = None
        self._dreamzero_run_task: asyncio.Task[Any] | None = None
        self._dreamzero_lifecycle_lock = asyncio.Lock()
        self._manual_instruction: str | None = None
        self._manual_action_index = 0
        self._closed = False
        self._cleanup_complete = False
        self._on_progress = getattr(connection, "on_progress", None)
        # Called with every exception a request raises (the facade reads a drop from it).
        self.on_request_failure: Callable[[BaseException], None] | None = None
        self._send_floor_s = send_floor_s(model, deployment=deployment, steady_send=steady_send)
        self._last_send_at: float | None = None
        self._last_response_at: float | None = None
        self._send_hint: SendHint | None = None  # from the response to the last send
        # This session's own thread for resizing and encoding camera frames (see _off_loop).
        self._encoder: ThreadPoolExecutor | None = None
        self._history_error: Exception | None = None
        self._calibration_announced = False
        self._ready_announced = self.resolved_optimization_config.calibration == "off"
        self._inference_announced = False
        self._summary_announced = False
        self._has_completed_run = False
        self.last_run_result: RunResult | None = None

    @property
    def runtime_contract(self) -> RuntimeContract:
        return self._runtime_contract

    @property
    def calibration_profile(self) -> NetworkCalibrationProfile | None:
        return self._calibration_profile

    @property
    def transport_mode(self) -> TransportMode | None:
        """The path inference takes now: a Modal session moves between punched QUIC and
        its WebSocket during the session."""
        return getattr(self._connection.transport, "mode", None) or self._connection.transport_mode

    @property
    def fallback_reason(self) -> str | None:
        return getattr(self._connection.transport, "fallback_reason", None)

    def camera_frame_sink(self) -> Any:
        """Where each new camera frame goes as it arrives when the session's camera codec codes
        frames on arrival (t16_latency_v1 LP): the transport's ``offer_frame``; else None. Asked
        again on every frame, so a reconnect's transport takes over."""
        transport = getattr(self._connection, "transport", None)
        if getattr(transport, "wants_frame_feed", False) is True:
            return transport.offer_frame
        return None

    @property
    def requires_task_preparation(self) -> bool:
        return (self.model in ISAAC05_MODELS
                or "task_prepare_v1" in getattr(self._connection.transport, "capabilities", ()))

    async def prepare(self, *, instruction: str, timeout_s: float | None = None) -> None:
        """Warm the task and reset its episode before capturing an observation.

        Managed run() calls this automatically. Raw predict() users call it before
        observing, including when repeating the same instruction in a new episode.
        """
        await self._prepare_task(instruction=instruction, timeout_s=timeout_s)

    async def _prepare_task(
        self, *, instruction: str, timeout_s: float | None = None, managed: bool = False,
    ) -> None:
        self._require_open()
        if not self.requires_task_preparation:
            raise ValueError("Worker does not advertise task preparation for this session")
        if not isinstance(instruction, str) or not instruction.strip():
            raise ValueError("instruction must be non-empty")
        async with self._predict_lock:
            self._require_open()
            if self._prepared_run_active:
                raise RuntimeError("Stop the active run before preparing another episode")
            prepare = getattr(self._connection.transport, "prepare_task", None)
            if prepare is None:
                raise RuntimeError("Task preparation unavailable; upgrade the worker and transport")
            await self._action_controller.close()
            self._action_controller = AsyncActionController(policy=self)
            self._manual_instruction = None
            self._manual_action_index = 0
            if self._pending_chunk is not None:
                self._pending_chunk.cancel()
                await asyncio.gather(self._pending_chunk, return_exceptions=True)
                self._pending_chunk = None
                # Cancelling __anext__ closes an async generator; use a new consumer.
                self._chunks = self._connection.transport.action_chunks().__aiter__()
            self._emit_progress("Preparing task…")
            # The session's contract where the server's is the whole contract (a model this
            # SDK doesn't know, or an exported deployment base); the model's own otherwise.
            own = (self._runtime_contract
                   if follows_server_contract(self.model) or exported_base(self.model)
                   else runtime_contract_for_model(self.model))
            await prepare(instruction.strip(), timeout_s=(
                own.task_prepare_timeout_s if timeout_s is None else timeout_s),
                **({"context": self.context} if self.context != "auto" else {}))
            self._require_open()
            frames = getattr(self._connection.transport, "context_frames", None) or 1
            if isinstance(self.observation_history, EpisodeTicks):
                # A prepared task starts a new episode on the server and here.
                self.observation_history.clear()
            else:
                # History frames at the checkpoint's own action period (Isaac: 1/30 s).
                self.observation_history = (
                    ObservationHistory(frames, 1.0 / self.native_action_hz)
                    if frames > 1 else None
                )
            self._prepared_run_active = managed
            self._emit_progress("Task ready.")

    async def push_history(self, observation: Any) -> None:
        """Keep a pre-request observation for the next request's history frames.

        Where the server accepts history frames, its frames are sent now, in the
        background and in order with later observations, so the request carries only
        its newest frame. A failed send only costs context: the server pads.
        """
        history = self.observation_history
        if history is None:
            return
        transport = self._connection.transport
        if (
            not history.sends_ahead
            or HISTORY_FRAMES_CAPABILITY not in getattr(transport, "capabilities", ())
        ):
            # Kept for the request's own strip (a sparse window only ever uses one of them).
            history.push(observation)
            return
        self._raise_history_error()
        send_key = getattr(history, "send_key", None)
        key = send_key() if send_key is not None else time.time_ns()
        if key is None:  # this step's frames stay local (an episode's non-tick step)
            history.push(observation)
            return

        def encode(snapshot: Any) -> dict[str, bytes]:
            with wire.wire_image(self.wire_image):
                return wire.encoded_frames(snapshot)

        try:
            snapshot = _detached(observation)
        except _NotDetached:
            encoded = asyncio.get_running_loop().create_future()
            encoded.set_result(encode(observation))  # raises here, as it always did
        else:
            # Queued on the session's encoder thread now, ahead of any later request's
            # frames (one thread, first in first out), so they reach the server first.
            encoded = self._hand_off(lambda: encode(snapshot))

        async def send() -> None:
            try:
                frames = await encoded
            except Exception as exc:  # the caller's frames: raised at its next call
                self._history_error = self._history_error or exc
                return
            with suppress(Exception):  # a failed send only costs context: the server pads
                await transport.send_history_frames(key, frames)

        task = asyncio.create_task(send())
        self._background_tasks.add(task)
        task.add_done_callback(self._background_tasks.discard)
        history.push(observation, key=key)

    async def episode_window(self, observation: Any, executed: Sequence[Any]) -> Any:
        """``predict(observation, past_observations=executed)`` on an episode the server keeps
        with measured states (Praxis-1): ``executed`` holds the observation each action was
        executed from since the previous ``predict()``, oldest first (its first is that call's
        own observation). Each later one's frames go ahead keyed by its step, as a run loop sends
        them; every one's state rides the request. ``[]`` starts a new episode here and on the
        server."""
        history = self.observation_history
        if not isinstance(history, EpisodeTicks) or not history.measured_steps:
            raise ValueError("episode_window serves an episode the server keeps with states")
        if not executed:
            history.clear()
            return history.window(observation)
        if not history.requested:
            raise errors.observation_error(
                "past_observations", f"{len(executed)} observations before the episode's first "
                "predict()",
                "the observation each action was executed from since the last predict(), "
                "oldest first: [] for an episode's first call",
            )
        history.replay_from_request()
        for index, seen in enumerate(executed):
            if index:
                history.executed()
                await self.push_history(seen)
            else:
                # The last request's own step: its frames are on the server already.
                history.push(seen)
        history.executed()
        return history.window(observation)

    async def predict(
        self,
        observation: ObservationLike,
        *,
        instruction: str,
        timeout_s: float = 60.0,
    ) -> ActionChunkResult:
        """Send one observation and return the raw action chunk."""
        return await self._predict_chunk(
            observation,
            instruction=instruction,
            timeout_s=timeout_s,
            actions_remaining=None,
            is_calibration=False,
            calibration_context=None,
            rtc_context=None,
        )

    async def next_action(
        self,
        observation: ObservationLike,
        *,
        instruction: str,
        timeout_s: float = 60.0,
    ) -> tuple[float, ...]:
        """Stateful manual-loop step returning one executable action."""
        if self.model in {"dreamzero-droid", "dreamzero-yam"}:
            self._require_no_dreamzero_run("next_action()")
            if self._manual_instruction != instruction or self._dreamzero_episode is None:
                await self.begin_episode(instruction=instruction)
                self._manual_instruction = instruction
                self._manual_action_index = 0
            result = await self.step(
                observation,
                action_index=self._manual_action_index,
                timeout_s=timeout_s,
            )
            self._manual_action_index += 1
            return result.action
        return await self._action_controller.next_action(
            observation,
            instruction=instruction,
            timeout_s=timeout_s,
        )

    async def begin_episode(
        self,
        *,
        instruction: str,
        strategy: RunStrategy | None = None,
    ) -> None:
        self._require_open()
        self._require_no_dreamzero_run("begin_episode()")
        async with self._dreamzero_lifecycle_lock:
            self._require_open()
            self._require_no_dreamzero_run("begin_episode()")
            _, first_error = await self._end_dreamzero_episode_locked()
            if first_error is not None:
                raise first_error
            await self._begin_dreamzero_episode_locked(
                instruction=instruction,
                strategy=strategy,
            )

    async def _begin_dreamzero_episode_locked(
        self,
        *,
        instruction: str,
        strategy: RunStrategy | None,
    ) -> None:
        from dreamscale.dreamzero import dreamzero_loop_profile
        from dreamscale.policy.dreamzero_runtime import DreamZeroEpisodeController

        profile = dreamzero_loop_profile(self.model)
        resolved = _validate_dreamzero_strategy(
            self.model, strategy or RunStrategy(), _session_contract(self)
        )
        assert resolved.dreamzero_sampling is not None
        controller = DreamZeroEpisodeController(
            policy=self,
            instruction=instruction,
            sampling=resolved.dreamzero_sampling,
            commit_prefix_steps=resolved.dreamzero_commit_prefix_steps,
            profile=profile,
            strategy=resolved,
        )
        await controller.begin()
        self._dreamzero_episode = controller

    async def step(
        self,
        observation: ObservationLike,
        *,
        action_index: int,
        timeout_s: float = 60.0,
    ) -> PolicyStepResult:
        self._require_no_dreamzero_run("step()")
        if self._dreamzero_episode is None:
            raise RuntimeError("step() requires begin_episode()")
        return await self._dreamzero_episode.step(
            observation,
            action_index=action_index,
            timeout_s=timeout_s,
        )

    async def end_episode(self) -> None:
        async with self._dreamzero_lifecycle_lock:
            run_task, first_error = await self._end_dreamzero_episode_locked()
        await self._cancel_dreamzero_run(run_task)
        if first_error is not None:
            raise first_error

    async def _end_dreamzero_episode_locked(
        self,
    ) -> tuple[asyncio.Task[Any] | None, BaseException | None]:
        episode, self._dreamzero_episode = self._dreamzero_episode, None
        run_task, self._dreamzero_run_task = self._dreamzero_run_task, None
        self._manual_instruction = None
        self._manual_action_index = 0
        first_error: BaseException | None = None
        if episode is not None:
            try:
                await episode.end()
            except BaseException as exc:
                first_error = exc
        return run_task, first_error

    async def _cancel_dreamzero_run(
        self,
        run_task: asyncio.Task[Any] | None,
    ) -> None:
        current_task = asyncio.current_task()
        if run_task is not None and run_task is not current_task and not run_task.done():
            run_task.cancel()
            await asyncio.gather(run_task, return_exceptions=True)

    async def _calibrate(
        self,
        observation: ObservationLike,
        *,
        instruction: str,
        timeout_s: float = 60.0,
    ) -> NetworkCalibrationProfile | None:
        if self._calibration_profile is not None:
            return self._calibration_profile
        mode = self.resolved_optimization_config.calibration
        if mode == "off":
            return None
        route = self._calibration_route(mode)
        reused = load_session_calibration(session_id=self.session_id, route=route)
        if reused is not None:
            self._calibration_profile = reused
            self._emit_progress(
                _calibration_completion_message(reused).replace(
                    "Calibration complete", "Calibration reused from this warm session", 1
                )
            )
            self._emit_ready_for_inference()
            return reused
        if not self._calibration_announced:
            self._emit_progress(f"Calibrating network timing ({mode})...")
            self._calibration_announced = True
        budget_s = NETWORK_CALIBRATION_TIME_BUDGET_S[mode]
        if budget_s <= 0.0:
            return None
        sample_limit = _calibration_sample_limit(mode)
        deadline = time.monotonic() + budget_s
        profile_deadline = (
            deadline - min(5.0, budget_s / 2.0)
            if mode == "rtc_graph"
            and self.resolved_optimization_config.rtc == "on"
            and self.resolved_optimization_config.rtc_contract == "calibrated_static"
            else deadline
        )
        samples: list[NetworkCalibrationSample] = []
        for sample_index in range(sample_limit):
            remaining_s = profile_deadline - time.monotonic()
            if not _has_budget_for_calibration_sample(samples, remaining_s):
                break
            try:
                result = await self._predict_chunk(
                    observation,
                    instruction=instruction,
                    timeout_s=min(timeout_s, remaining_s),
                    actions_remaining=0,
                    is_calibration=True,
                    calibration_context={
                        "mode": mode,
                        "sample_index": sample_index,
                        "sample_limit": sample_limit,
                    },
                    rtc_context=_calibration_rtc_context(
                        resolved_config=self.resolved_optimization_config,
                        contract=self._runtime_contract,
                        mode=mode,
                        sample_index=sample_index,
                    ),
                )
            except TimeoutError:
                break
            samples.append(
                NetworkCalibrationSample(
                    request_id=str(result.observation_id),
                    roundtrip_ms=result.timing.obs_to_action_ms,
                    server_ms=result.timing.server_total_ms,
                    timing_ms=_calibration_timing_ms(result),
                    action_dim=len(result.actions[0]) if result.actions else None,
                )
            )
        if not samples:
            self._emit_progress(_calibration_completion_message(None))
            self._emit_ready_for_inference()
            return None
        self.runtime_stats.calibration_samples += len(samples)
        self._calibration_profile = build_network_calibration_profile(
            samples,
            config=NetworkCalibrationConfig(mode=mode),
            chunk_size=self._runtime_contract.execution_chunk_size,
            control_hz=self._runtime_contract.action_hz,
        )
        if mode == "rtc_graph":
            await self._warm_rtc_graph_profiles(
                observation,
                instruction=instruction,
                timeout_s=timeout_s,
                deadline=deadline,
                profile=self._calibration_profile,
            )
        if getattr(self._connection, "keep_warm", 0):
            save_session_calibration(
                session_id=self.session_id, route=route, profile=self._calibration_profile
            )
        self._emit_progress(_calibration_completion_message(self._calibration_profile))
        self._emit_ready_for_inference()
        return self._calibration_profile

    def _calibration_route(self, mode: str) -> dict[str, str | None]:
        """What a reused profile must match: mode, runtime and data-plane transport."""
        transport = self.transport_mode
        return {
            "mode": mode,
            "target_key": self._target_key,
            "capability_fingerprint": self.resolved_optimization_config.capability_fingerprint,
            "transport": None if transport is None else str(transport),
            "fallback_reason": self.fallback_reason,
        }

    async def _warm_rtc_graph_profiles(
        self,
        observation: ObservationLike,
        *,
        instruction: str,
        timeout_s: float,
        deadline: float,
        profile: NetworkCalibrationProfile,
    ) -> None:
        contexts = _rtc_graph_warmup_contexts(
            resolved_config=self.resolved_optimization_config,
            contract=self._runtime_contract,
            profile=profile,
        )
        if not contexts:
            return
        for index, rtc_context in enumerate(contexts):
            remaining_s = deadline - time.monotonic()
            if remaining_s <= _MIN_CALIBRATION_SAMPLE_BUDGET_S:
                return
            try:
                await self._predict_chunk(
                    observation,
                    instruction=instruction,
                    timeout_s=min(timeout_s, remaining_s),
                    actions_remaining=0,
                    is_calibration=True,
                    calibration_context={
                        "mode": self.resolved_optimization_config.calibration,
                        "rtc_profile_warmup": True,
                        "rtc_profile": rtc_context.profile or "bootstrap",
                        "rtc_profile_warmup_index": index,
                    },
                    rtc_context=rtc_context,
                )
            except TimeoutError:
                return

    async def _predict_chunk_with_queue_depth(
        self,
        observation: ObservationLike,
        *,
        instruction: str,
        timeout_s: float,
        actions_remaining: int,
        next_action_step: int | None = None,
        threshold_steps: int | None = None,
        rtc_context: RtcRequestContext | None = None,
        action_history: Sequence[Sequence[float]] = (),
    ) -> ActionChunkResult:
        return await self._predict_chunk(
            observation,
            instruction=instruction,
            timeout_s=timeout_s,
            actions_remaining=actions_remaining,
            is_calibration=False,
            next_action_step=next_action_step,
            threshold_steps=threshold_steps,
            calibration_context=None,
            rtc_context=rtc_context,
            action_history=action_history,
        )

    async def _predict_chunk(
        self,
        observation: ObservationLike,
        *,
        instruction: str,
        timeout_s: float,
        actions_remaining: int | None,
        is_calibration: bool,
        calibration_context: dict[str, Any] | None,
        rtc_context: RtcRequestContext | None,
        next_action_step: int | None = None,
        threshold_steps: int | None = None,
        action_history: Sequence[Sequence[float]] = (),
    ) -> ActionChunkResult:
        try:
            result = await self._predict_chunk_locked(
                observation,
                instruction=instruction,
                timeout_s=timeout_s,
                actions_remaining=actions_remaining,
                is_calibration=is_calibration,
                calibration_context=calibration_context,
                rtc_context=rtc_context,
                next_action_step=next_action_step,
                threshold_steps=threshold_steps,
                action_history=action_history,
            )
        except asyncio.CancelledError:
            raise
        except BaseException as exc:
            if self.on_request_failure is not None:
                self.on_request_failure(exc)
            raise
        if not is_calibration:
            # Every answer of every path (predict, the run loops, sync) counted once.
            record_server_report(self, result)
        return result

    async def _predict_chunk_locked(
        self,
        observation: ObservationLike,
        *,
        instruction: str,
        timeout_s: float,
        actions_remaining: int | None,
        is_calibration: bool,
        calibration_context: dict[str, Any] | None,
        rtc_context: RtcRequestContext | None,
        next_action_step: int | None = None,
        threshold_steps: int | None = None,
        action_history: Sequence[Sequence[float]] = (),
    ) -> ActionChunkResult:
        async with self._predict_lock:
            observation = _prepared_for_session(observation, model=self.model)
            if not is_calibration:
                self._emit_ready_for_inference()
                if not self._inference_announced:
                    self._emit_progress("Inference started.")
                    self._inference_announced = True
            self._raise_history_error()
            episode = self.observation_history
            if isinstance(episode, EpisodeTicks):
                if not isinstance(observation, EpisodeObservation):
                    # predict(): the observation alone, after the chunks before it ran.
                    observation = episode.predict_window(observation)
                episode_context = EpisodeRequestContext(
                    step=observation.step, chunk=episode.take_chunk(observation.step),
                    seed=episode.seed)
            else:
                episode_context = None
            observation_id = self._observation_id
            self._observation_id += 1
            if self._send_floor_s:
                # The floor first: a held request is encoded when it may go, and one whose
                # budget the floor outlasts fails at once (SendFloorTimeout), unencoded.
                timeout_s = await self._wait_for_send_floor(timeout_s)
            # A camera-codec transport (hidden robot-test mode) codes the raw frames itself.
            codec_frames = getattr(self._connection.transport, "wants_raw_frames", False) is True
            def encode(snapshot: Any) -> Observation:
                with wire.wire_image(self.wire_image), wire.raw_frames(codec_frames):
                    return snapshot.to_wire(
                        session_id=self.session_id,
                        observation_id=observation_id,
                        instruction=instruction,
                    )

            wire_observation = await self._encode(observation, encode)
            exported = exported_base(self.model)
            if self.deployment is not None:
                check_observation(
                    wire_observation, self.deployment,
                    label=exported.label if exported is not None else "π0.5",
                    plain_state=exported is not None and exported.state == "refuse",
                )
                if exported is not None and exported.state == "convert":
                    wire_observation = with_vector_state(wire_observation)
            wire_observation = _with_capture_time(wire_observation, observation)
            older = getattr(observation, "older", None)
            if self._runtime_contract.measured_state_steps:
                samples = getattr(observation, "state_samples", None)
                if samples:
                    wire_observation = dataclasses.replace(
                        wire_observation,
                        frame=wire_observation.frame.model_copy(update={"state_history": [
                            [float(value) for value in previous.state] for previous in samples
                        ]}),
                    )
            if episode_context is not None:
                # The state one executed step before the request; with measured states
                # (Praxis-1), that of every step executed since the last request.
                if self._runtime_contract.measured_state_steps:
                    # The joints and grippers of each executed step, as the robot held them.
                    states = [_hold_vector(seen) for seen in getattr(observation, "executed", ())]
                else:
                    states = [observation.previous.state]
                if states:
                    wire_observation = dataclasses.replace(
                        wire_observation,
                        frame=wire_observation.frame.model_copy(update={"state_history": [
                            [float(value) for value in state] for state in states
                        ]}),
                    )
            if self._runtime_contract.state_history and older:
                # The states of the older frames, which the window carries as observations.
                wire_observation = dataclasses.replace(
                    wire_observation,
                    frame=wire_observation.frame.model_copy(update={"state_history": [
                        [float(value) for value in previous.state] for previous in older
                    ]}),
                )
            pad_commands = exported is not None and exported.pad_episode_start_commands
            if (not action_history and pad_commands
                    and getattr(observation, "state_samples", None)):
                # Episode-start commands have not executed yet: upstream initializes its
                # command window at the measured state, independently of past state ticks.
                action_history = [list(observation.state)] * self._runtime_contract.action_history
            if action_history and self._runtime_contract.action_history:
                history = [list(map(float, action)) for action in action_history]
                if pad_commands:
                    count = self._runtime_contract.action_history
                    history = [history[0]] * max(0, count - len(history)) + history
                wire_observation = dataclasses.replace(
                    wire_observation,
                    frame=wire_observation.frame.model_copy(
                        update={"action_history": history[-self._runtime_contract.action_history:]}
                    ),
                )
            express = getattr(self.deployment, "express_committed", None)
            if express is not None and rtc_context is not None and rtc_context.reference_actions:
                # Hy-VLA: committed pose rows read against this request's own state.
                rtc_context = rtc_context.model_copy(update={"reference_actions": express(
                    rtc_context.reference_actions,
                    list(getattr(wire_observation.frame.robot_state, "state", None) or ()),
                )})
            wire_observation = _with_runtime_context(
                wire_observation,
                resolved_config=self.resolved_optimization_config,
                runtime_contract=self._runtime_contract,
                preserve_existing_queue=self.model in {"dreamzero-droid", "dreamzero-yam"},
                actions_remaining=actions_remaining,
                next_action_step=next_action_step,
                threshold_steps=threshold_steps,
                calibration_context=calibration_context
                or _runtime_calibration_context(
                    mode=self.resolved_optimization_config.calibration,
                    profile=self._calibration_profile,
                ),
                rtc_context=rtc_context,
            )
            if episode_context is not None:
                frame = wire_observation.frame
                wire_observation = dataclasses.replace(wire_observation, frame=frame.model_copy(
                    update={"runtime_context": frame.runtime_context.model_copy(
                        update={"episode": episode_context})}))
            transport = self._connection.transport
            rtt_probe = self._start_data_plane_rtt_probe(transport)
            start_ns = time.monotonic_ns()
            send_start_ns = time.monotonic_ns()
            await self._connection.transport.send_observation(wire_observation)
            send_end_ns = time.monotonic_ns()
            if self._send_floor_s:
                self._last_send_at = time.monotonic()
                self._send_hint = None  # a hint applies only after its own response
            deadline = time.monotonic() + timeout_s
            first_wait_s = timeout_s
            probe_quic = (
                bool(getattr(self._connection, "allow_runtime_fallback", False))
                and self.transport_mode == "quic"
                and timeout_s > _AUTO_QUIC_RESULT_TIMEOUT_S
            )
            if probe_quic:
                first_wait_s = _AUTO_QUIC_RESULT_TIMEOUT_S
            try:
                chunk = await self._next_matching_chunk(
                    observation_id=observation_id,
                    timeout_s=first_wait_s,
                )
            except TimeoutError:
                if not probe_quic or not await self._fallback_to_relay():
                    remaining_s = deadline - time.monotonic()
                    if remaining_s <= 0.0:
                        raise
                    chunk = await self._next_matching_chunk(
                        observation_id=observation_id,
                        timeout_s=remaining_s,
                    )
                else:
                    transport = self._connection.transport
                    rtt_probe = self._start_data_plane_rtt_probe(transport)
                    send_start_ns = time.monotonic_ns()
                    await self._connection.transport.send_observation(wire_observation)
                    send_end_ns = time.monotonic_ns()
                    remaining_s = deadline - time.monotonic()
                    if remaining_s <= 0.0:
                        raise
                    chunk = await self._next_matching_chunk(
                        observation_id=observation_id,
                        timeout_s=remaining_s,
                    )
            end_ns = time.monotonic_ns()
            if self._send_floor_s:
                self._last_response_at = time.monotonic()
                self._send_hint = send_hint(getattr(chunk, "runtime_metadata", None))
            transport = self._connection.transport
            data_plane_rtt_ms = _data_plane_rtt_sample(transport, rtt_probe)
            result = result_from_chunk(
                observation_id=observation_id,
                chunk=chunk,
                start_ns=start_ns,
                send_start_ns=send_start_ns,
                send_end_ns=send_end_ns,
                end_ns=end_ns,
                transport=transport,
                data_plane_rtt_ms=data_plane_rtt_ms,
                capture_time_ns=wire_observation.frame.capture_time_ns,
                frame=wire_observation.frame,
            )
            return result

    async def _encode(self, observation: Any, encode: Callable[[Any], _T]) -> _T:
        """``encode(snapshot)`` on the session's encoder thread when the observation can be
        snapshotted (``_detached``); otherwise on the loop, as before this thread existed."""
        try:
            snapshot = _detached(observation)
        except _NotDetached:
            return encode(observation)
        return await self._off_loop(lambda: encode(snapshot))

    async def _off_loop(self, work: Callable[[], _T]) -> _T:
        """Run ``work`` (resizing and JPEG-encoding camera frames: tens of ms of CPU on a
        robot computer) on this session's own encoder thread, so the event loop, and the
        control ticks on it, keep running meanwhile."""
        return await self._hand_off(work)

    def _raise_history_error(self) -> None:
        """A history frame that couldn't be encoded off the loop fails the caller's next call
        with its error, as encoding it in ``push_history`` itself used to."""
        error, self._history_error = self._history_error, None
        if error is not None:
            raise error

    def _hand_off(self, work: Callable[[], _T]) -> asyncio.Future[_T]:
        """Queue ``work`` on this session's encoder thread now, at the call: one thread, so
        work runs one item at a time in the order it was handed over (history frames before
        the request that follows them). Never the loop's default executor, which belongs to
        the caller in the async API. After close it runs inline, as it used to."""
        loop = asyncio.get_running_loop()
        if self._closed:
            done: asyncio.Future[_T] = loop.create_future()
            try:
                done.set_result(work())
            except Exception as exc:
                done.set_exception(exc)
            return done
        if self._encoder is None:
            self._encoder = ThreadPoolExecutor(
                max_workers=1, thread_name_prefix=f"dreamscale-encode-{self.session_id}"
            )
        context = contextvars.copy_context()  # the caller's wire settings (wire.py)
        return loop.run_in_executor(self._encoder, context.run, work)

    def _next_send_at(self, *, hinted: bool = True) -> float:
        assert self._last_send_at is not None
        return next_send_at(
            last_send_at=self._last_send_at, last_response_at=self._last_response_at,
            floor_s=self._send_floor_s, hint=self._send_hint if hinted else None,
        )

    async def _wait_for_send_floor(self, timeout_s: float) -> float:
        """Hold this send until ``max(prev_send + floor, prev_response)``, or the endpoint's
        hinted instant within its spacing past that (``next_send_at``). The wait counts
        against the caller's budget; what is left of it is returned."""
        if not self._send_floor_s or self._last_send_at is None:
            return timeout_s
        now = time.monotonic()
        wait_s = self._next_send_at() - now
        if wait_s >= timeout_s and self._send_hint is not None:
            # A hint only ever delays a send; it is never why a call times out.
            wait_s = self._next_send_at(hinted=False) - now
        if wait_s <= 0.0:
            return timeout_s
        if wait_s >= timeout_s:
            raise SendFloorTimeout(
                f"the next request may be sent in {wait_s:.2f} s, after this call's "
                f"{timeout_s:.2f} s budget"
            )
        await asyncio.sleep(wait_s)
        return timeout_s - wait_s

    def send_ready_in(self) -> float:
        """Seconds until the next request may be sent (0 when it may go now). Loops that
        choose when to request use it to observe *after* the wait, so a request never
        carries a frame captured before the floor."""
        if not self._send_floor_s or self._last_send_at is None:
            return 0.0
        return max(0.0, self._next_send_at() - time.monotonic())

    def _start_data_plane_rtt_probe(
        self,
        transport: Any,
    ) -> asyncio.Task[float | None] | None:
        if getattr(transport, "mode", None) == "relay" or self.transport_mode == "relay":
            # The relay's RTT probe is a clock_probe frame; Modal direct servers accept
            # only observation_submit and end the session on anything else. Never on
            # the relay, whether chosen explicitly or reached by the runtime fallback.
            return None
        measure = getattr(transport, "measure_data_plane_rtt_ms", None)
        if not callable(measure) and getattr(transport, "mode", None) == "wss_tunnel":
            websocket = getattr(transport, "_ws", None)
            ping = getattr(websocket, "ping", None)
            if callable(ping):

                async def measure_websocket_ping() -> float:
                    started_ns = time.monotonic_ns()
                    pong_waiter = await ping()
                    await asyncio.wait_for(pong_waiter, timeout=1.0)
                    return (time.monotonic_ns() - started_ns) / 1_000_000.0

                measure = measure_websocket_ping
        if not callable(measure):
            return None

        async def measure_safely() -> float | None:
            with suppress(Exception):
                value = await measure()
                return _finite_ms(value)
            return None

        task = asyncio.create_task(measure_safely())
        self._background_tasks.add(task)
        task.add_done_callback(self._background_tasks.discard)
        return task

    async def _fallback_to_relay(self) -> bool:
        if not bool(getattr(self._connection, "allow_runtime_fallback", False)):
            return False
        connect_relay = getattr(self._connection.client, "connect_relay", None)
        if not callable(connect_relay):
            return False

        if self._pending_chunk is not None:
            self._pending_chunk.cancel()
            await asyncio.gather(self._pending_chunk, return_exceptions=True)
            self._pending_chunk = None

        previous = self._connection.transport
        with suppress(Exception):
            await previous.close()
        relay = await connect_relay(self._connection.session)
        relay.fallback_reason = "quic_result_timeout"
        relay.primary_preflight_status = getattr(previous, "primary_preflight_status", None)
        relay.diagnostic_preflight_status = getattr(previous, "diagnostic_preflight_status", None)
        self._connection.transport = relay
        self._connection.transport_mode = "relay"
        self._send_hint = None  # a new path: its next answer brings its own hint
        self._connection.allow_runtime_fallback = False
        self._chunks = relay.action_chunks().__aiter__()
        self._emit_progress(
            "QUIC connected but did not return inference data; using HTTPS fallback."
        )
        self._emit_progress("Motion may feel less responsive while using fallback.")
        report_task = asyncio.create_task(self._report_runtime_fallback(relay))
        self._background_tasks.add(report_task)
        report_task.add_done_callback(self._background_tasks.discard)
        return True

    async def _report_runtime_fallback(self, transport: Any) -> None:
        report_transport = getattr(self._connection.client, "report_transport", None)
        if not callable(report_transport):
            return
        with suppress(Exception):
            await asyncio.wait_for(
                report_transport(
                    self.session_id,
                    transport_protocol="relay",
                    fallback_used=True,
                    fallback_reason="quic_result_timeout",
                    primary_preflight_status=getattr(transport, "primary_preflight_status", None),
                    diagnostic_preflight_status=getattr(
                        transport, "diagnostic_preflight_status", None
                    ),
                ),
                timeout=2.0,
            )

    async def run(
        self,
        *,
        instruction: str,
        observe: Callable[[RunContext], ObservationLike | Awaitable[ObservationLike]],
        act: Callable[
            [Sequence[float], RunContext],
            ActResult | bool | None | Awaitable[ActResult | bool | None],
        ],
        read_hold_action: Callable[[RunContext], Sequence[float] | Awaitable[Sequence[float]]]
        | None = None,
        max_actions: int | None,
        strategy: RunStrategy | None = None,
        hooks: RunHooks | None = None,
    ) -> RunResult:
        if self.model in {"dreamzero-droid", "dreamzero-yam"}:
            from dreamscale.dreamzero import run_dreamzero_loop

            self._require_open()
            self._require_no_dreamzero_run("run()")
            dreamzero_strategy = _validate_dreamzero_strategy(
                self.model,
                strategy or RunStrategy(),
                _session_contract(self),
            )
            assert dreamzero_strategy.dreamzero_sampling is not None
            contract = _session_contract(self) or runtime_contract_for_model(self.model)
            managed_joints = (
                bool(contract.joint_groups)
                and dreamzero_strategy.dreamzero_sampling != "upstream_eval"
            )
            if read_hold_action is not None and not managed_joints:
                raise ValueError(
                    f"{public_model(self.model)} does not support read_hold_action for this "
                    "sampling mode"
                )
            if (
                not managed_joints
                and hooks is not None
                and any(getattr(hooks, name) is not None for name in hooks.__dataclass_fields__)
            ):
                raise ValueError(
                    f"{public_model(self.model)} RunHooks are not yet supported for this "
                    "sampling mode"
                )
            run_task = asyncio.current_task()
            assert run_task is not None
            async with self._dreamzero_lifecycle_lock:
                self._require_open()
                self._require_no_dreamzero_run("run()")
                _, first_error = await self._end_dreamzero_episode_locked()
                if first_error is not None:
                    raise first_error
                await self._begin_dreamzero_episode_locked(
                    instruction=instruction,
                    strategy=dreamzero_strategy,
                )
                controller = self._dreamzero_episode
                assert controller is not None
                self._dreamzero_run_task = run_task
                controller.hooks = hooks or RunHooks()
            try:
                result = await run_dreamzero_loop(
                    instruction=instruction,
                    policy=self,
                    observe=observe,
                    act=act,
                    max_actions=max_actions,
                    sampling=dreamzero_strategy.dreamzero_sampling,
                    commit_prefix_steps=dreamzero_strategy.dreamzero_commit_prefix_steps,
                    timeout_s=dreamzero_strategy.timeout_s,
                    profile=controller.profile,
                    controller=controller,
                    strategy=dreamzero_strategy,
                    hooks=hooks,
                    read_hold_action=read_hold_action,
                )
            finally:
                async with self._dreamzero_lifecycle_lock:
                    if self._dreamzero_run_task is run_task:
                        self._dreamzero_run_task = None
                    if self._dreamzero_episode is controller:
                        self._dreamzero_episode = None
                        await controller.end()
            return result
        prepare_task = getattr(
            self, "requires_task_preparation", self.model in ISAAC05_MODELS,
        )
        if prepare_task:
            await self._prepare_task(instruction=instruction, managed=True)
        try:
            result = await run_policy_loop(
                instruction=instruction,
                policy=self,
                observe=observe,
                act=act,
                read_hold_action=read_hold_action,
                max_actions=max_actions,
                strategy=strategy,
                hooks=hooks,
            )
            return result
        finally:
            if prepare_task:
                self._prepared_run_active = False

    async def _next_matching_chunk(self, *, observation_id: int, timeout_s: float) -> Any:
        deadline = time.monotonic() + timeout_s
        while True:
            remaining_s = deadline - time.monotonic()
            if remaining_s <= 0:
                raise TimeoutError
            chunk = await asyncio.wait_for(
                asyncio.shield(self._next_chunk_task()),
                timeout=remaining_s,
            )
            self._pending_chunk = None
            generated_from = getattr(chunk, "generated_from_observation_id", None)
            if generated_from == observation_id:
                return chunk
            if generated_from is not None and generated_from < observation_id:
                self.runtime_stats.stale_chunks_dropped += 1
                continue
            raise RuntimeError(
                "received action chunk for unexpected observation "
                f"{generated_from}; expected {observation_id}"
            )

    def _next_chunk_task(self) -> asyncio.Task[Any]:
        if self._pending_chunk is None:
            self._pending_chunk = asyncio.create_task(self._chunks.__anext__())
        return self._pending_chunk

    async def close(self) -> None:
        if self._cleanup_complete:
            return
        self._closed = True
        self._emit_runtime_summary()
        first_error: BaseException | None = None

        async def attempt(cleanup: Awaitable[Any]) -> None:
            nonlocal first_error
            try:
                await cleanup
            except BaseException as exc:
                if first_error is None:
                    first_error = exc

        await attempt(self.end_episode())
        await attempt(self._action_controller.close())
        if self._pending_chunk is not None:
            self._pending_chunk.cancel()
            await asyncio.gather(self._pending_chunk, return_exceptions=True)
            self._pending_chunk = None
        close_chunks = getattr(self._chunks, "aclose", None)
        if close_chunks is not None:
            with suppress(Exception):
                await close_chunks()
        if self._background_tasks:
            results = await asyncio.gather(
                *tuple(self._background_tasks),
                return_exceptions=True,
            )
            self._background_tasks.clear()
            for result in results:
                if (
                    isinstance(result, BaseException)
                    and not isinstance(result, asyncio.CancelledError)
                    and first_error is None
                ):
                    first_error = result
        if self._encoder is not None:
            # A frame still being encoded finishes on its own; nothing new is queued.
            self._encoder.shutdown(wait=False, cancel_futures=True)
        await attempt(self._connection.close())
        self._cleanup_complete = first_error is None
        if first_error is not None:
            raise first_error

    def _require_open(self) -> None:
        if self._closed:
            raise RuntimeError("policy is closed")

    def _require_no_dreamzero_run(self, operation: str) -> None:
        run_task = self._dreamzero_run_task
        if run_task is not None and not run_task.done():
            raise RuntimeError(f"{operation} is unavailable while run() is active")

    def _emit_progress(self, line: str) -> None:
        if callable(self._on_progress):
            self._on_progress(line)

    def _emit_ready_for_inference(self) -> None:
        if self._ready_announced:
            return
        self._emit_progress("Policy is ready for inference.")
        self._ready_announced = True

    def _emit_runtime_summary(self) -> None:
        if self._has_completed_run:
            return
        if self._summary_announced:
            return
        summary = describe_runtime_summary(
            transport_mode=self.transport_mode,
            runtime_stats=self.runtime_stats,
            calibration_profile=self._calibration_profile,
        )
        if summary is not None:
            self._emit_progress(f"Run summary: {summary}")
            self._summary_announced = True

    def _emit_run_summary(self, result: RunResult) -> None:
        for line in format_run_summary(result):
            self._emit_progress(line)
        self._has_completed_run = True

    async def __aenter__(self) -> AsyncRemotePolicy:
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        await self.close()


class RemotePolicy:
    def __init__(self, *, runner: _LoopRunner, async_policy: AsyncRemotePolicy) -> None:
        self.model = async_policy.model
        self.session_id = async_policy.session_id
        self.region = async_policy.region
        self._target_key = getattr(async_policy, "_target_key", None)
        self.speed = getattr(async_policy, "speed", "standard")
        self.action_hz = getattr(async_policy, "action_hz", None)
        self.native_action_hz = getattr(async_policy, "native_action_hz", None)
        self.chunk_size = getattr(async_policy, "chunk_size", None)
        self.runtime_contract = getattr(async_policy, "runtime_contract", None)
        self.deployment = getattr(async_policy, "deployment", None)
        self.resolved_optimization_config = getattr(
            async_policy,
            "resolved_optimization_config",
            None,
        )
        self.runtime_stats = getattr(async_policy, "runtime_stats", RuntimeStats())
        self._connection_timing_monotonic = dict(
            getattr(async_policy, "_connection_timing_monotonic", None) or {}
        )
        self._runner = runner
        self._async_policy = async_policy
        self._closed = False

    @property
    def calibration_profile(self) -> NetworkCalibrationProfile | None:
        return getattr(self._async_policy, "calibration_profile", None)

    @property
    def transport_mode(self) -> str | None:
        return getattr(self._async_policy, "transport_mode", None)

    @property
    def fallback_reason(self) -> str | None:
        return getattr(self._async_policy, "fallback_reason", None)

    def prepare(self, *, instruction: str, timeout_s: float | None = None) -> None:
        """Prepare the episode before acquiring the observation for predict()."""
        self._runner.run(self._async_policy.prepare(instruction=instruction, timeout_s=timeout_s))

    def predict(
        self,
        observation: ObservationLike,
        *,
        instruction: str,
        timeout_s: float = 60.0,
    ) -> ActionChunkResult:
        """Send one observation and return the raw action chunk."""
        return self._runner.run(
            self._async_policy.predict(
                observation,
                instruction=instruction,
                timeout_s=timeout_s,
            )
        )

    def next_action(
        self,
        observation: ObservationLike,
        *,
        instruction: str,
        timeout_s: float = 60.0,
    ) -> tuple[float, ...]:
        """Stateful manual-loop step returning one executable action."""
        return self._runner.run(
            self._async_policy.next_action(
                observation,
                instruction=instruction,
                timeout_s=timeout_s,
            )
        )

    def begin_episode(
        self,
        *,
        instruction: str,
        strategy: RunStrategy | None = None,
    ) -> None:
        self._runner.run(
            self._async_policy.begin_episode(
                instruction=instruction,
                strategy=strategy,
            )
        )

    def step(
        self,
        observation: ObservationLike,
        *,
        action_index: int,
        timeout_s: float = 60.0,
    ) -> PolicyStepResult:
        return self._runner.run(
            self._async_policy.step(
                observation,
                action_index=action_index,
                timeout_s=timeout_s,
            )
        )

    def end_episode(self) -> None:
        self._runner.run_cleanup(self._async_policy.end_episode())

    def run(
        self,
        *,
        instruction: str,
        observe: Callable[[RunContext], ObservationLike],
        act: Callable[[Sequence[float], RunContext], ActResult | bool | None],
        read_hold_action: Callable[[RunContext], Sequence[float]] | None = None,
        max_actions: int | None,
        strategy: RunStrategy | None = None,
        hooks: RunHooks | None = None,
    ) -> RunResult:
        return _sync_run(
            self,
            instruction=instruction,
            observe=observe,
            act=act,
            read_hold_action=read_hold_action,
            max_actions=max_actions,
            strategy=strategy,
            hooks=hooks,
        )

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        try:
            self._runner.run_cleanup(self._async_policy.close())
        finally:
            self._runner.shutdown()

    def __enter__(self) -> RemotePolicy:
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()


def _sync_run(
    policy: Any,
    *,
    instruction: str,
    observe: Callable[[RunContext], ObservationLike],
    act: Callable[[Sequence[float], RunContext], ActResult | bool | None],
    read_hold_action: Callable[[RunContext], Sequence[float]] | None = None,
    max_actions: int | None,
    strategy: RunStrategy | None = None,
    hooks: RunHooks | None = None,
) -> RunResult:
    """The synchronous managed loop, shared by ``RemotePolicy`` and the public ``Policy``:
    ``policy`` exposes ``_runner`` and ``_async_policy`` (the open session)."""
    async_policy = policy._async_policy
    if policy.model in {"dreamzero-droid", "dreamzero-yam"}:
        try:
            return policy._runner.run(
                async_policy.run(
                    instruction=instruction,
                    observe=observe,
                    act=act,
                    read_hold_action=read_hold_action,
                    max_actions=max_actions,
                    strategy=strategy,
                    hooks=hooks,
                )
            )
        finally:
            policy.last_run_result = getattr(async_policy, "last_run_result", None)
    prepare_task = getattr(
        async_policy, "requires_task_preparation", policy.model in ISAAC05_MODELS,
    )
    if prepare_task:
        policy._runner.run(async_policy._prepare_task(instruction=instruction, managed=True))
    try:
        return _run_sync_policy_loop(
            policy=policy,
            instruction=instruction,
            observe=observe,
            act=act,
            read_hold_action=read_hold_action,
            max_actions=max_actions,
            strategy=strategy,
            hooks=hooks,
        )
    finally:
        if prepare_task:
            async_policy._prepared_run_active = False


def _session_contract(policy: Any) -> RuntimeContract | None:
    """Return the contract the open session resolved, if there is one.

    Both policy classes are routinely stood up as lightweight stand-ins in
    tests, so this reads through rather than requiring the attribute: absent a
    session, the caller falls back to the model's own contract.
    """

    contract = getattr(policy, "_runtime_contract", None)
    if contract is None:
        contract = getattr(getattr(policy, "_async_policy", None), "_runtime_contract", None)
    return contract if isinstance(contract, RuntimeContract) else None


def _validate_dreamzero_strategy(
    model: str, strategy: RunStrategy, session_contract: RuntimeContract | None = None
) -> RunStrategy:
    from dreamscale.dreamzero import resolve_dreamzero_sampling

    # The session's contract, when the caller chose a control_hz at connect,
    # carries the decimated rate and chunk. Falling back to the model contract
    # keeps the gate meaningful for callers that never opened a session.
    contract = session_contract or runtime_contract_for_model(model)
    if strategy.action_hz not in (None, contract.action_hz):
        raise ValueError(f"{public_model(model)} action_hz is fixed at {contract.action_hz:g}")
    if strategy.chunk_size not in (None, contract.chunk_size):
        raise ValueError(f"{public_model(model)} chunk_size is fixed at {contract.chunk_size}")
    if strategy.replan_at_remaining is not None:
        raise ValueError(
            f"{public_model(model)} server owns temporal admission; "
            "replan_at_remaining is unsupported"
        )
    if strategy.underrun != "hold_position":
        raise ValueError(f"{public_model(model)} underruns must hold the observed position")
    if not strategy.real_time:
        raise ValueError(
            f"{public_model(model)} control is fixed to real-time {contract.action_hz:g} Hz"
        )
    sampling = resolve_dreamzero_sampling(model, strategy.dreamzero_sampling)
    if contract.joint_groups and sampling != "upstream_eval":
        smoothing = resolve_action_smoothing(strategy, contract)
        if smoothing.mode == "output":
            raise ValueError("stateful joint control requires motion smoothing")
    elif (
        strategy.action_smoothing != "auto"
        or strategy.smoothing_new_weight is not None
        or strategy.smoothing_correction_steps is not None
        or strategy.smoothing_reference_speed is not None
    ):
        raise ValueError(f"{public_model(model)} action smoothing is not supported for {sampling}")
    return replace(
        strategy,
        dreamzero_sampling=resolve_dreamzero_sampling(
            model,
            strategy.dreamzero_sampling,
        ),
    )


def _run_sync_policy_loop(
    *,
    policy: RemotePolicy,
    instruction: str,
    observe: Callable[[RunContext], ObservationLike],
    act: Callable[[Sequence[float], RunContext], ActResult | bool | None],
    read_hold_action: Callable[[RunContext], Sequence[float]] | None,
    max_actions: int | None,
    strategy: RunStrategy | None,
    hooks: RunHooks | None,
) -> RunResult:
    if max_actions is not None and (type(max_actions) is not int or max_actions < 1):
        raise ValueError("max_actions must be a positive integer or None")
    run_started = time.monotonic()
    # No strategy given: the policy's mode (connect(mode=), else the model's own: sync for
    # Praxis-1), as AsyncPolicy.run does.
    strategy = strategy or RunStrategy(mode=getattr(policy, "mode", None) or "async")
    hooks = hooks or RunHooks()
    contract = resolve_runtime_contract(
        model=policy.model,
        resolved_config=policy.resolved_optimization_config,
        action_hz_override=strategy.action_hz,
        chunk_size_override=strategy.chunk_size,
        deployment=getattr(policy, "deployment", None),
    )
    require_run_hold(contract)
    period_s = 1.0 / contract.action_hz
    started = time.monotonic()
    action_started = started
    chunks_start = policy.runtime_stats.chunks_received
    underruns_start = policy.runtime_stats.underruns
    telemetry = RunTelemetryAccumulator()
    completed_actions = action_attempts = startup_holds = execution_underruns = 0
    first_motion = False
    hold_latch = None
    stop_reason = "action_limit"
    failure = None
    measured_bootstrap = contract.measured_bootstrap
    startup_wait_ms = 0.0
    controller = AsyncActionController(
        policy=policy._async_policy,
        strategy=strategy,
        skip_calibration=False,
        hooks=hooks,
    )

    try:
        if strategy.real_time or measured_bootstrap:
            ctx = RunContext(
                action_index=0,
                observation_id=0,
                actions_remaining=controller.actions_remaining,
                stalled=False,
                elapsed_s=0.0,
            )
            observation = observe(ctx)
            _raise_if_awaitable(observation, "observe")
            policy._runner.run(
                controller.prepare(
                    observation,
                    instruction=instruction,
                    timeout_s=strategy.timeout_s,
                    wait_for_chunk=measured_bootstrap,
                )
            )
            if measured_bootstrap:
                if read_hold_action is not None:
                    anchor = read_hold_action(ctx)
                    _raise_if_awaitable(anchor, "read_hold_action")
                else:
                    anchor = _hold_position_action(
                        contract=contract,
                        observation=observation,
                        last_action=None,
                    )
                policy._runner.run(controller.seed_initial_position(anchor))
                startup_wait_ms = (time.monotonic() - run_started) * 1000.0
            started = action_started = time.monotonic()
        for action_index in (count() if max_actions is None else range(max_actions)):
            if strategy.real_time:
                delay = action_started + action_index * period_s - time.monotonic()
                if delay > 0:
                    time.sleep(delay)
            ctx = RunContext(
                action_index=action_index,
                observation_id=action_index,
                actions_remaining=controller.actions_remaining,
                stalled=False,
                elapsed_s=time.monotonic() - started,
            )
            # The frame is captured no earlier than this: the startup motion delay counts
            # to it, not to when the step reaches the loop thread (later on a busy host).
            observed_at = time.monotonic()
            observation = observe(ctx)
            _raise_if_awaitable(observation, "observe")
            step = policy._runner.run(
                controller.step(
                    observation,
                    instruction=instruction,
                    timeout_s=strategy.timeout_s,
                    action_index=action_index,
                    wait_for_chunk=not strategy.real_time,
                    observed_at=observed_at,
                )
            )
            resolved_action = step.action
            action_ctx = RunContext(
                action_index=action_index,
                observation_id=ctx.observation_id,
                actions_remaining=step.actions_remaining,
                stalled=step.stalled,
                elapsed_s=time.monotonic() - started,
            )
            if step.stalled:
                if first_motion:
                    execution_underruns += 1
                else:
                    startup_holds += 1
                if strategy.underrun != "repeat_last_action":
                    if hold_latch is None:
                        if controller.holds_last_command:
                            # The last command holds (RuntimeContract.hold_last_command).
                            hold_latch = step.action
                        elif (
                            read_hold_action is not None
                            and contract.hold_behavior == "current_position"
                        ):
                            fresh_action = read_hold_action(action_ctx)
                            _raise_if_awaitable(fresh_action, "read_hold_action")
                            hold_latch = _validate_hold_action(
                                fresh_action,
                                action_dim=contract.action_dim,
                            )
                        else:
                            hold_latch = step.action
                    resolved_action = hold_latch
                    policy._runner.run(
                        controller.record_act_result(
                            step.action,
                            ActResult(accepted_action=resolved_action),
                        )
                    )
            else:
                hold_latch = None
            if hooks.on_chunk is not None:
                for event in step.chunk_events:
                    hooks.on_chunk(event)
            if hooks.on_merge is not None:
                for event in step.merge_events:
                    hooks.on_merge(event)
            if hooks.on_queue_merge is not None:
                for event in step.queue_merge_events:
                    hooks.on_queue_merge(event)
            for event in step.timing_events:
                telemetry.record(event)
                if hooks.on_timing is not None:
                    hooks.on_timing(event)
            if hooks.on_action is not None:
                hooks.on_action(
                    ActionEvent(
                        action_index=action_index,
                        stalled=step.stalled,
                        actions_remaining=step.actions_remaining,
                        action=resolved_action,
                    )
                )
            dispatch_started_ns = time.monotonic_ns()
            if measured_bootstrap and strategy.real_time:
                action_started = max(
                    action_started,
                    time.monotonic() - action_index * period_s,
                )
            action_attempts += 1
            done = act(resolved_action, action_ctx)
            _raise_if_awaitable(done, "act")
            policy._runner.run(controller.record_act_result(resolved_action, done))
            completed_actions += 1
            first_motion = first_motion or not step.stalled
            if hooks.on_dispatch is not None:
                hooks.on_dispatch(
                    DispatchEvent(
                        action_index,
                        step.stalled,
                        resolved_action,
                        _accepted_action(done, resolved_action),
                        dispatch_started_ns,
                        time.monotonic_ns(),
                    )
                )
            if hooks.on_buffer is not None:
                for event in step.buffer_events:
                    hooks.on_buffer(event)
            if _sync_act_done(done):
                stop_reason = "act_callback"
                break
    except BaseException as exc:
        failure = exc
        stop_reason = (
            "interrupted"
            if isinstance(exc, (KeyboardInterrupt, asyncio.CancelledError))
            else "error"
        )
        raise
    finally:
        cleanup_error = None
        try:
            policy._runner.run_cleanup(controller.close())
        except BaseException as exc:
            cleanup_error = exc
        report_error = failure or cleanup_error
        if cleanup_error is not None and failure is None:
            stop_reason = "error"
        result = RunResult(
            actions=completed_actions,
            policy_calls=policy.runtime_stats.chunks_received - chunks_start,
            underruns=policy.runtime_stats.underruns - underruns_start,
            done=stop_reason == "act_callback",
            elapsed_s=time.monotonic() - run_started,
            max_actions=max_actions,
            stop_reason=stop_reason,
            timing=telemetry.summary(),
            model=policy.model,
            region=policy.region,
            transport_mode=policy.transport_mode,
            fallback_reason=policy.fallback_reason,
            startup_holds=startup_holds,
            execution_underruns=execution_underruns,
            startup_wait_ms=startup_wait_ms,
            action_attempts=action_attempts,
            error_type=type(report_error).__name__ if report_error else None,
            loop_cleanup_error_type=type(cleanup_error).__name__ if cleanup_error else None,
        )
        policy.last_run_result = result
        publish_run_summary(
            policy._async_policy,
            hooks,
            result,
            preserve_error=report_error is not None,
        )
        if cleanup_error is not None and failure is None:
            raise cleanup_error
    return result


def _sync_act_done(result: ActResult | bool | None) -> bool:
    if isinstance(result, ActResult):
        return result.done
    return bool(result)


def _raise_if_awaitable(value: Any, callback_name: str) -> None:
    if inspect.isawaitable(value):
        raise TypeError(
            f"policy.run() from dreamscale.connect() requires a synchronous "
            f"{callback_name} callback; use dreamscale.aconnect() inside async "
            "applications"
        )


def _prepared_for_session(observation: Any, *, model: str) -> Any:
    """A LIBERO observation built without ``model=`` takes the session's model here, at
    the one place every path sends from (predict, next_action, run, step, the CLI), so
    pi05-libero always gets 256 px frames and a 20-action chunk. A ``model=`` that names
    the connected model (by either name) passes; a different one raises.

    A generic ``dreamscale.robot`` observation on a catalog model with a robot helper of
    its own (the catalog's ``robot_helper``) raises here, before anything is sent: that
    model's wire wants its robot's typed state, and the server would only answer
    INVALID_OBSERVATION."""
    from dreamscale.libero import LiberoObservation, stamped_for_model
    from dreamscale.robot import RobotObservation

    if isinstance(observation, LiberoObservation):
        return stamped_for_model(observation, model)
    if isinstance(observation, RobotObservation):
        helper = _robot_helper(model)
        if helper is not None:
            raise errors.catalog("typed_observation_required", model=model, helper=helper)
    return observation


def _robot_helper(model: str) -> str | None:
    """The SDK robot helper a catalog model reads its observation from (``dreamscale.<it>``),
    None for a model without one (deployments, LeRobot checkpoints: ``dreamscale.robot``)."""
    from dreamscale_transport import catalog

    entry = catalog.entry(internal_model(model))
    return None if entry is None else entry.client.robot_helper


class _NotDetached(Exception):
    """An observation holds something ``_detached`` can't vouch for: encode it on the loop."""


_IMMUTABLE = (str, bytes, int, float, complex, bool, type(None), np.generic, enum.Enum)


def _detached(value: Any, depth: int = 0) -> Any:
    """``value`` with every numpy array it holds copied, so the encoder thread works on a
    private snapshot while the caller reuses its camera buffers for the next frame (a copy
    is a memcpy per frame). It vouches for everything it returns: arrays, immutable
    scalars, plain lists/tuples/dicts, named tuples, SimpleNamespaces, and dataclasses or
    observation objects (``to_wire``) built from those. Anything else raises
    ``_NotDetached``, and that observation is encoded on the loop as before."""
    if isinstance(value, np.ndarray):
        return value.copy()
    if isinstance(value, _IMMUTABLE):
        return value
    if depth > 6:
        raise _NotDetached(type(value).__name__)
    if type(value) in (tuple, list) or (
        isinstance(value, tuple) and getattr(value, "_make", None) is not None
    ):
        items = [_detached(item, depth + 1) for item in value]
        if all(new is old for new, old in zip(items, value, strict=True)):
            return value
        return type(value)(items) if type(value) in (tuple, list) else value._make(items)
    if type(value) is dict:
        copied = {key: _detached(item, depth + 1) for key, item in value.items()}
        return copied if any(copied[k] is not v for k, v in value.items()) else value
    if type(value) is types.SimpleNamespace:
        copied = {key: _detached(item, depth + 1) for key, item in vars(value).items()}
        changed = any(copied[k] is not v for k, v in vars(value).items())
        return types.SimpleNamespace(**copied) if changed else value
    state = getattr(value, "__dict__", None)
    if not isinstance(state, dict) or not (
        dataclasses.is_dataclass(value) or callable(getattr(type(value), "to_wire", None))
    ) or getattr(type(value), "__slots__", None):
        raise _NotDetached(type(value).__name__)
    copied = {key: _detached(item, depth + 1) for key, item in state.items()}
    if all(copied[key] is item for key, item in state.items()):
        return value
    # Built bare, not through copy.copy: a history window forwards unknown attributes to its
    # newest observation, which copy's protocol lookups would recurse through.
    try:
        clone = object.__new__(type(value))
    except TypeError as exc:  # a type that must be built through its own __new__
        raise _NotDetached(type(value).__name__) from exc
    clone.__dict__.update(copied)  # frozen dataclasses too: their fields live in __dict__
    return clone


def _hold_vector(observation: Any) -> Sequence[float]:
    """An observation's measured joints and grippers in the action layout, as the facade's
    measured hold reads them: ``hold_action``, else ``joint_positions``."""
    hold = getattr(observation, "hold_action", None)
    if hold is None:
        hold = getattr(observation, "joint_positions", None)
    if hold is None:
        raise ValueError("this observation has no measured joints to send")
    return hold


def _with_capture_time(wire_observation: Observation, observation: Any) -> Observation:
    """The caller's capture time (``capture_time_ns=`` on the observation helpers) replaces
    the moment the request was built: the server counts a late-bound prefix from it."""
    capture_time_ns = getattr(observation, "capture_time_ns", None)
    if capture_time_ns is None:
        return wire_observation
    return dataclasses.replace(
        wire_observation,
        frame=wire_observation.frame.model_copy(update={"capture_time_ns": int(capture_time_ns)}),
    )


def _with_runtime_context(
    observation: Observation,
    *,
    resolved_config: ResolvedOptimizationConfig,
    runtime_contract: RuntimeContract,
    preserve_existing_queue: bool = False,
    actions_remaining: int | None = None,
    next_action_step: int | None = None,
    threshold_steps: int | None = None,
    calibration_context: dict[str, Any] | None = None,
    rtc_context: RtcRequestContext | None = None,
) -> Observation:
    queue_depth = (
        observation.frame.actions_remaining if actions_remaining is None else int(actions_remaining)
    )
    frame = observation.frame.model_copy(update={"actions_remaining": queue_depth})
    existing = frame.runtime_context
    queue: dict[str, Any] = {
        "actions_remaining": queue_depth,
        "control": resolved_config.control,
        "action_hz": float(runtime_contract.action_hz),
        "chunk_size": int(runtime_contract.chunk_size),
        "action_horizon": int(runtime_contract.chunk_size),
        "execution_horizon": runtime_contract.execution_chunk_size,
    }
    if next_action_step is not None:
        queue["next_action_step"] = int(next_action_step)
    if threshold_steps is not None:
        queue["threshold_steps"] = int(threshold_steps)
    calibration = calibration_context or {}
    if existing is None:
        runtime_context = RuntimeRequestContext(
            version=PROTOCOL_VERSION,
            resolved_config=resolved_config.to_wire(),
            calibration=calibration,
            queue=queue,
            rtc=rtc_context,
        )
    else:
        merged_queue = existing.queue if preserve_existing_queue else {**existing.queue, **queue}
        runtime_context = existing.model_copy(
            update={
                "version": PROTOCOL_VERSION,
                "resolved_config": resolved_config.to_wire(),
                "calibration": {**existing.calibration, **calibration},
                "queue": merged_queue,
                "rtc": rtc_context,
            }
        )
    return Observation(
        frame=frame.model_copy(update={"runtime_context": runtime_context}),
        camera_payloads=observation.camera_payloads,
        chunk_size=int(runtime_contract.chunk_size),
        camera_refs=observation.camera_refs,
        observation_seq=observation.observation_seq,
        raw_camera_frames=observation.raw_camera_frames,
    )


def _calibration_timing_ms(result: ActionChunkResult) -> dict[str, float]:
    fields = {
        "transport_send": result.timing.transport_send_ms,
        "wait_for_chunk": result.timing.wait_for_chunk_ms,
        "server_queue": result.timing.server_queue_ms,
        "server_inference": result.timing.server_inference_ms,
        "server_total": result.timing.server_total_ms,
        "client_overhead": result.timing.client_overhead_ms,
        "quic_rtt": result.timing.quic_rtt_ms,
        "data_plane_rtt": result.timing.data_plane_rtt_ms,
        "worker_queue": result.timing.worker_queue_ms,
        "worker_preprocess": result.timing.worker_preprocess_ms,
        "worker_inference": result.timing.worker_inference_ms,
        "worker_postprocess": result.timing.worker_postprocess_ms,
    }
    return {key: float(value) for key, value in fields.items() if value is not None}


def _runtime_calibration_context(
    *,
    mode: Calibration,
    profile: NetworkCalibrationProfile | None,
) -> dict[str, Any]:
    if profile is None:
        return {}
    return {
        "mode": mode,
        "sample_count": profile.sample_count,
        "usable_sample_count": profile.usable_sample_count,
        "raw_sample_count": profile.raw_sample_count,
        "retained_sample_count": profile.retained_sample_count,
        "discarded_warmup_sample_count": profile.discarded_warmup_sample_count,
        "discarded_warmup_rtt_ms": profile.discarded_warmup_rtt_ms,
        "calibration_confidence": profile.calibration_confidence,
        "latency_health": profile.latency_health,
        "runtime_calibration_usage": profile.runtime_calibration_usage,
        "runtime_calibration_usage_label": profile.runtime_calibration_usage_label,
        "readiness": profile.readiness,
        "burst_class": profile.burst_class,
        "rtt_ms": dict(profile.rtt_ms),
        "latency_steps": dict(profile.latency_steps),
        "late_budget_steps": profile.late_budget_steps,
        "recommended_latency_steps": profile.recommended_latency_steps,
        "recommended_fixed_threshold_steps": profile.recommended_fixed_threshold_steps,
    }


def _calibration_sample_limit(calibration: Calibration) -> int:
    return {
        "off": 0,
        "fast": 16,
        "default": 64,
        "rtc_graph": 64,
        "extended": 256,
    }[calibration]


def _calibration_completion_message(
    profile: NetworkCalibrationProfile | None,
) -> str:
    if profile is None:
        return "Calibration complete: latency=unknown, confidence=none, not using calibration."
    return (
        f"Calibration complete: latency={profile.latency_health}, "
        f"confidence={profile.calibration_confidence}, "
        f"{profile.runtime_calibration_usage_label}."
    )


def _has_budget_for_calibration_sample(
    samples: Sequence[NetworkCalibrationSample],
    remaining_s: float,
) -> bool:
    if remaining_s <= 0.0:
        return False
    if not samples:
        return True
    observed_s = [
        float(sample.roundtrip_ms) / 1000.0
        for sample in samples
        if math.isfinite(float(sample.roundtrip_ms)) and float(sample.roundtrip_ms) > 0.0
    ]
    if not observed_s:
        return remaining_s >= _MIN_CALIBRATION_SAMPLE_BUDGET_S
    guard_s = max(observed_s) * _CALIBRATION_OBSERVED_RTT_GUARD_RATIO
    guard_s = max(_MIN_CALIBRATION_SAMPLE_BUDGET_S, guard_s)
    guard_s = min(_MAX_CALIBRATION_SAMPLE_BUDGET_S, guard_s)
    return remaining_s >= guard_s


def _calibration_rtc_context(
    *,
    resolved_config: ResolvedOptimizationConfig,
    contract: RuntimeContract,
    mode: Calibration,
    sample_index: int,
) -> RtcRequestContext | None:
    if (
        mode != "rtc_graph"
        or resolved_config.rtc != "on"
        or resolved_config.rtc_contract != "fixed_ratio_v1"
        or contract.action_dim is None
    ):
        return None
    profile_names = ("green", "yellow", "red")
    profile_name = profile_names[sample_index % len(profile_names)]
    return build_rtc_context_for_queue(
        config=RtcConfig(
            enabled=True,
            contract_id=resolved_config.rtc_contract or "calibrated_static",
        ),
        chunk_size=contract.chunk_size,
        action_dim=contract.action_dim,
        profile_name=profile_name,
        reference_actions=None,
    )


def _rtc_graph_warmup_contexts(
    *,
    resolved_config: ResolvedOptimizationConfig,
    contract: RuntimeContract,
    profile: NetworkCalibrationProfile,
) -> list[RtcRequestContext]:
    if (
        resolved_config.rtc != "on"
        or resolved_config.rtc_contract != "calibrated_static"
        or contract.action_dim is None
        or profile.runtime_calibration_usage != "normal"
    ):
        return []
    config = RtcConfig(enabled=True, contract_id="calibrated_static")
    profile_set = build_rtc_profile_set(
        config,
        build_rtc_estimator_state_from_calibration(
            profile,
            chunk_size=contract.chunk_size,
            action_hz=contract.action_hz,
            method_o_profile=_method_o_profile_name(resolved_config.control),
            control_mode=resolved_config.control,
        ),
    ).mark_static("network_calibration")
    contexts = [
        RtcRequestContext(
            enabled=True,
            inference_delay_steps=0,
            execution_horizon_steps=0,
            fixed_steps=0,
            modifiable_steps=0,
            new_actions=contract.chunk_size,
            prefix_attention_schedule=config.prefix_attention_schedule,
            max_guidance_weight=config.max_guidance_weight,
            reference_actions=None,
            reference_action_valid_steps=0,
            profile=None,
            contract_id=None,
        )
    ]
    seen_shapes: set[tuple[int, int, int]] = set()
    for rtc_profile in profile_set.profiles:
        shape_key = (
            int(rtc_profile.fixed_steps),
            int(rtc_profile.execution_horizon_steps),
            int(rtc_profile.new_actions),
        )
        if shape_key in seen_shapes:
            continue
        seen_shapes.add(shape_key)
        contexts.append(
            _rtc_warmup_context_for_profile(
                config=config,
                contract=contract,
                profile=rtc_profile,
                profile_set=profile_set,
            )
        )
    return contexts


def _rtc_warmup_context_for_profile(
    *,
    config: RtcConfig,
    contract: RuntimeContract,
    profile: RtcGeometryProfile,
    profile_set: RtcProfileSet,
) -> RtcRequestContext:
    action_dim = int(contract.action_dim or 0)
    reference_actions = (
        [[0.0 for _ in range(action_dim)] for _ in range(profile.execution_horizon_steps)]
        if profile.execution_horizon_steps > 0
        else None
    )
    return build_rtc_context_for_queue(
        config=config,
        chunk_size=contract.chunk_size,
        action_dim=contract.action_dim,
        profile_name=profile.name,
        reference_actions=reference_actions,
        profile_set=profile_set,
    )


def _method_o_profile_name(control: str) -> str:
    if control in {"prefer_freshness", "balanced", "prefer_robustness"}:
        return control
    return "balanced"


async def _aconnect(
    model: str,
    *,
    acceleration: Acceleration | None = "auto",
    control: RequestedControl | None = "auto",
    rtc: Rtc | None = "auto",
    calibration: RequestedCalibration | None = "auto",
    region: RegionPreference = "auto",
    provider: ProviderPreference | None = None,
    speed: SpeedPreference | None = None,
    idle_timeout: int = DEFAULT_CONNECT_IDLE_TIMEOUT_S,
    keep_warm: int = DEFAULT_PUBLIC_KEEP_WARM_S,
    startup_timeout: float | None = None,
    transport: TransportPreference = "auto",
    control_hz: int | None = None,
    deployment: str | None = None,
    checkpoint: str | None = None,
    endpoint: str | None = None,
    api_key: str | None = None,
    context: Context = "auto",
    on_progress: Callable[[str], None] | None = print,
    optimization_config: OptimizationConfig | None = None,
    steady_send: bool | int | None = None,
    **deps: Any,
) -> AsyncRemotePolicy:
    # A public name (pi0.5-bimanualyam) or the internal id; the SDK keys on the latter.
    model = internal_model(model)
    checkpoint = _resolve_deployment(
        deployment=deployment, endpoint=endpoint, checkpoint=checkpoint
    )
    if checkpoint is None:
        model, checkpoint = await _deployment_named(model, api_key, deps)
    only = deployment_only_base(model)
    if only is not None and checkpoint in (None, "base"):
        raise errors.catalog("deployment_required", base_label=only[0], base_flag=only[1])
    resolve_steady_send(steady_send)  # a bad value fails before compute is opened
    # Resolved before the session is opened so an unsupported rate fails fast
    # rather than after a cold start has already been paid for.
    resolved_control_hz = resolve_control_hz(model, control_hz)
    _validate_context(model, context)
    progress = _resolve_progress_callback(on_progress)
    resolved_config = optimization_config or OptimizationConfig(
        acceleration=acceleration,
        control=control,
        rtc=rtc,
        calibration=calibration,
    )
    # Whether another region is much closer than the deployment's: measured while the session
    # opens, said once it's ready, never waited for.
    hint = region_hint.start(checkpoint, api_key, deps.get("client_factory"))
    try:
        connection = await open_policy_connection(
            model=model,
            region=region,
            provider=provider,
            speed=speed,
            idle_timeout=idle_timeout,
            keep_warm=keep_warm,
            startup_timeout=startup_timeout,
            transport=transport,
            optimization_config=resolved_config,
            on_progress=progress,
            **({"checkpoint": checkpoint} if checkpoint is not None else {}),
            **({"api_key": api_key} if api_key is not None else {}),
            **deps,
        )
    except BaseException:
        region_hint.finish(hint, None)
        raise
    try:
        policy = AsyncRemotePolicy(
            model=model, connection=connection, control_hz=resolved_control_hz,
            context=context, deployment=checkpoint, steady_send=steady_send,
        )
        region_hint.finish(hint, progress)
        return policy
    except BaseException:
        region_hint.finish(hint, None)
        # The session is ready but this SDK can't run its contract: close it now rather
        # than leave it heartbeating (and billed) until the process exits.
        if not getattr(connection, "closed", False):
            connection.closed = True
            await _cleanup_connect_failure(
                client=getattr(connection, "client", None),
                session=getattr(connection, "session", None),
                transport=getattr(connection, "transport", None),
                heartbeat=getattr(connection, "heartbeat", None),
            )
        raise


async def aconnect(
    model: str,
    *,
    acceleration: Acceleration | None = "auto",
    control: RequestedControl | None = "auto",
    rtc: Rtc | None = "auto",
    calibration: RequestedCalibration | None = "auto",
    region: RegionPreference = "auto",
    region_fallback: bool | None = None,
    provider: ProviderPreference | None = None,
    speed: SpeedPreference | None = None,
    idle_timeout: int = DEFAULT_CONNECT_IDLE_TIMEOUT_S,
    keep_warm: int = DEFAULT_PUBLIC_KEEP_WARM_S,
    startup_timeout: float | None = None,
    transport: TransportPreference = "auto",
    control_hz: int | None = None,
    deployment: str | None = None,
    checkpoint: str | None = None,
    endpoint: str | None = None,
    api_key: str | None = None,
    context: Context = "auto",
    on_progress: Callable[[str], None] | None = print,
    steady_send: bool | int | None = None,
) -> AsyncRemotePolicy:
    return await _aconnect(
        model,
        acceleration=acceleration,
        control=control,
        rtc=rtc,
        calibration=calibration,
        region=region,
        **({"region_fallback": region_fallback} if region_fallback is not None else {}),
        provider=provider,
        speed=speed,
        idle_timeout=idle_timeout,
        keep_warm=keep_warm,
        startup_timeout=startup_timeout,
        transport=transport,
        control_hz=control_hz,
        deployment=deployment,
        checkpoint=checkpoint,
        endpoint=endpoint,
        api_key=api_key,
        context=context,
        on_progress=on_progress,
        steady_send=steady_send,
    )


def connect(
    model: str,
    *,
    acceleration: Acceleration | None = "auto",
    control: RequestedControl | None = "auto",
    rtc: Rtc | None = "auto",
    calibration: RequestedCalibration | None = "auto",
    region: RegionPreference = "auto",
    region_fallback: bool | None = None,
    provider: ProviderPreference | None = None,
    speed: SpeedPreference | None = None,
    idle_timeout: int = DEFAULT_CONNECT_IDLE_TIMEOUT_S,
    keep_warm: int = DEFAULT_PUBLIC_KEEP_WARM_S,
    startup_timeout: float | None = None,
    transport: TransportPreference = "auto",
    control_hz: int | None = None,
    deployment: str | None = None,
    checkpoint: str | None = None,
    endpoint: str | None = None,
    api_key: str | None = None,
    context: Context = "auto",
    on_progress: Callable[[str], None] | None = print,
    steady_send: bool | int | None = None,
) -> RemotePolicy:
    runner = _LoopRunner()
    try:
        async_policy = runner.run(
            aconnect(
                model,
                acceleration=acceleration,
                control=control,
                rtc=rtc,
                calibration=calibration,
                region=region,
                **({"region_fallback": region_fallback} if region_fallback is not None else {}),
                provider=provider,
                speed=speed,
                idle_timeout=idle_timeout,
                keep_warm=keep_warm,
                startup_timeout=startup_timeout,
                transport=transport,
                control_hz=control_hz,
                deployment=deployment,
                checkpoint=checkpoint,
                endpoint=endpoint,
                api_key=api_key,
                context=context,
                on_progress=on_progress,
                steady_send=steady_send,
            )
        )
    except BaseException:
        runner.shutdown()
        raise
    return RemotePolicy(runner=runner, async_policy=async_policy)


async def _deployment_named(
    model: str, api_key: str | None, deps: dict[str, Any]
) -> tuple[str, str | None]:
    """``connect("<account>/<slug>")`` (or its ``ckpt_…`` id, or a bare slug of yours) runs
    that deployment on the model it was built on, as ``connect(<base>, deployment=...)``
    does."""
    from dreamscale.checkpoints_cmd import (
        is_deployment_ref,
        may_name_deployment,
        resolve_run_ref,
    )
    from dreamscale.config import load_config
    from dreamscale.control import ControlPlaneClient

    if not may_name_deployment(model):
        return model, None
    config = load_config()
    key = (api_key.strip() if api_key is not None else config.api_key) or None
    if key is None:
        if is_deployment_ref(model):
            raise errors.catalog("not_configured")
        return model, None
    client = deps.get("client_factory", ControlPlaneClient)(config.control_plane_url, key)
    try:
        base, deployment = await resolve_run_ref(client, model, None)
    finally:
        await client.close()
    return base or model, deployment


def _resolve_deployment(
    *, deployment: str | None, endpoint: str | None, checkpoint: str | None
) -> str | None:
    """One deployment id (or "base") from `deployment=` and its older names `endpoint=` and
    `checkpoint=`; the same value under several names is fine, different ones are not."""
    given = {
        name: value
        for name, value in (
            ("deployment", deployment), ("endpoint", endpoint), ("checkpoint", checkpoint)
        )
        if value is not None
    }
    if len(set(given.values())) > 1:
        names = " and ".join(f"{name}={value!r}" for name, value in given.items())
        raise ValueError(
            f"{names} name different deployments; pass one, as deployment= "
            "(endpoint= and checkpoint= are its older names)"
        )
    return next(iter(given.values()), None)


def _resolve_progress_callback(
    on_progress: Callable[[str], None] | None,
) -> Callable[[str], None] | None:
    if on_progress is print:
        return make_progress_printer()
    return on_progress
