"""Shared local benchmark simulation with asynchronous cloud policy inference."""

from __future__ import annotations

import asyncio
import dataclasses
import inspect
import json
import sys
import time
from collections.abc import Awaitable, Callable
from contextlib import suppress
from dataclasses import dataclass, field
from functools import partial
from pathlib import Path
from typing import Any, Protocol

import numpy as np
from dreamscale_transport import catalog
from dreamscale_transport.images import prepare_policy_image

from dreamscale import errors, wire
from dreamscale.arm import (
    _compatible_diagnose_udp,
    _default_transport_connect,
    _LoopRunner,
    _pin_connect,
)
from dreamscale.config import load_config
from dreamscale.constants import (
    CAMERA_KEY_LIBERO_AGENT,
    CAMERA_KEY_LIBERO_WRIST,
    CHUNK_SIZE,
    HEARTBEAT_S,
    MODEL_DREAMZERO_DROID,
    MODEL_LIBERO,
)
from dreamscale.control import ControlPlaneClient
from dreamscale.dreamzero import DREAMZERO_REPLAN_STRIDE
from dreamscale.model_names import public_model
from dreamscale.motion.ensemble import EnsembleBuffer
from dreamscale.policy.lifecycle import (
    ModalTransportReports,
    PolicyConnection,
    _start_modal_quic,
    _validate_keep_warm,
)
from dreamscale.policy.runtime.action_buffer import ActionBuffer
from dreamscale.policy.runtime.action_smoothing import resolve_action_smoothing
from dreamscale.policy.runtime.contract import runtime_contract_for_model
from dreamscale.policy.types import RegionPreference, RunStrategy, TransportPreference
from dreamscale.region_probe import create_session_with_rtt_region_order
from dreamscale.sessions import Heartbeat, stop_session, wait_until_ready
from dreamscale.sim.benchmarks import BENCHMARK_LABELS
from dreamscale.sim.metrics import SimMetrics, SimMetricsTui, _fmt_ms
from dreamscale.sim.timing import (
    DEFAULT_SIM_MAX_STEPS,
    LIBERO_ACTION_HZ,
    RealtimePacer,
)
from dreamscale.transport_selection import (
    _report_transport_best_effort,
    connect_selected_transport,
)

PREVIEW_WINDOW_NAME = "Dreamscale LIBERO sim"
_preview_window_initialized = False
PENDING_POLICY_CANCEL_TIMEOUT_S = 1.0
ACTION_CHUNKS_CLOSE_TIMEOUT_S = 1.0
# How each catalog model runs in a simulator (its entry's ``client.sim``).
_SIMS = {entry.id: entry.client.sim for entry in catalog.CATALOG if entry.client.sim is not None}
SIM_MODELS = tuple(_SIMS)
# Execute each complete chunk, holding while the next request is in flight.
STATEFUL_MODELS = tuple(model for model, sim in _SIMS.items() if sim.stateful)


def _budgets_actions(model: str, count_holds: bool | None) -> bool:
    """Whether a step budget counts the policy's actions only: by default a stateful LIBERO
    model's does (LIBERO's own evaluation waits for each plan, so its task horizons count
    actions), and ``count_holds`` decides it otherwise."""
    if count_holds is not None:
        return model in STATEFUL_MODELS and not count_holds
    return model in STATEFUL_MODELS and "libero" in _SIMS[model].benchmarks
# Simulators that build their own policy observation and multi-camera preview.
NATIVE_OBSERVATION_MODELS = tuple(
    model for model, sim in _SIMS.items() if sim.native_observation
)
# Each observation's SDK wire builder, by the sim's ``observation``: the libero builder sizes
# its images (``image_size``), the end-effector one names the model, the others take the chunk.
_BUILDERS = {
    "libero": "build_libero_observation", "rldx_libero": "build_rldx_libero_observation",
    "libero_history": "build_libero_history_observation",
    "robocasa": "build_robocasa_observation",
    "robocasa_window": "build_robocasa_window_observation",
    "franka": "build_franka_observation",
    "rho_end_effector": "build_rho_end_effector_observation",
}
# A stateful episode's settings beyond the chunk, by native observation: what it holds while
# a request is in flight and what each request carries (RoboLab DROID also drains a pending
# request before the next).
_STATEFUL_SETTINGS = {
    "franka": {"hold_description": "current absolute joints and measured gripper",
               "feedback_description": "current DROID camera views and proprioception",
               "drain_pending": True},
    "rho_end_effector": {
        "hold_description": "measured end-effector poses and last gripper commands",
        "feedback_description": "current RoboEval camera views and end-effector poses"},
    # Long-WAM RoboCasa365's own evaluation is synchronous (upstream's SyncPolicy): the world
    # waits while a plan is computed, then every planned action runs.
    "robocasa_window": {"hold_description": "physics paused during inference (upstream_eval)",
                        "feedback_description": "each camera's last 2.4 s and the state",
                        "pause_for_inference": True},
}
# A model whose own evaluation is synchronous (Sim.pause_for_inference): physics waits for each
# chunk instead of holding in real time.
_PAUSED = {"hold_description": "physics paused during inference (upstream_eval)",
           "pause_for_inference": True}
# The live viewer's camera layout, by native observation.
_VIEWER_CAMERAS = {"robocasa": "left | right | wrist",
                   "robocasa_window": "left | right | wrist",
                   "rho_end_effector": "head | left wrist | right wrist"}
# RoboLab DROID requests carry three views at 15 Hz: they get twice the usual reply timeout.
_SLOW_OBSERVATIONS = frozenset({"franka"})


def stateful_settings(model) -> dict:
    """A native-observation model's stateful episode settings: its observation's hold and
    feedback, and paused physics when its own evaluation is synchronous."""
    return {**_STATEFUL_SETTINGS.get(_observation(model), {}),
            **(_PAUSED if _SIMS[model].pause_for_inference else {})}


def _observation(model) -> str | None:
    sim = _SIMS.get(model)
    return sim.observation if sim is not None else None


def _sim_contract(model):
    if model not in SIM_MODELS:
        raise ValueError(f"{public_model(model)} doesn't run in sim. {errors.SEE_MODELS}")
    return runtime_contract_for_model(model)


def _sim_builder(model):
    contract = _sim_contract(model)
    observation = _observation(model)
    builder = getattr(wire, _BUILDERS[observation])
    if observation == "rho_end_effector":
        return partial(builder, model=model)
    if observation == "libero":
        return partial(builder, image_size=_sim_image_size(model),
                       chunk_size=contract.chunk_size)
    return partial(builder, chunk_size=contract.chunk_size)


def _sim_image_size(model):
    sim = _SIMS.get(model)
    return sim.image_size if sim is not None else 224


class SimEnvProtocol(Protocol):
    task_description: str

    def reset(self) -> Any: ...
    def step(self, action: list[float]) -> tuple[Any, bool]: ...
    def agent_frame(self, obs: Any) -> Any: ...
    def wrist_frame(self, obs: Any) -> Any: ...
    def proprio(self, obs: Any) -> list[float]: ...
    def close(self) -> None: ...


@dataclass
class SimResult:
    steps: int = 0
    policy_calls: int = 0
    done: bool = False
    metrics: dict[str, Any] = field(default_factory=dict)


@dataclass
class SimPolicyProfile:
    request_id: int
    observation_id: int
    start_step: int
    obs_build_ms: float = 0.0
    transport_send_ms: float | None = None
    wait_for_chunk_ms: float | None = None
    send_to_chunk_ms: float | None = None
    chunk_ready_ns: int | None = field(default=None, repr=False)
    chunk_ready_to_accept_ms: float | None = None
    server_queue_ms: float | None = None
    server_inference_ms: float | None = None
    server_total_ms: float | None = None
    client_overhead_ms: float | None = None
    runner_local_blocking_ms_total: float = 0.0
    client_overhead_unattributed_ms: float | None = None
    completed: bool = False
    env_step_count: int = 0
    env_step_ms_total: float = 0.0
    env_step_ms_max: float = 0.0
    preview_frame_count: int = 0
    preview_frame_ms_total: float = 0.0
    preview_frame_ms_max: float = 0.0
    frame_callback_count: int = 0
    frame_callback_ms_total: float = 0.0
    frame_callback_ms_max: float = 0.0

    def note_env_step(self, elapsed_ms: float) -> None:
        self.env_step_count += 1
        self.env_step_ms_total += elapsed_ms
        self.env_step_ms_max = max(self.env_step_ms_max, elapsed_ms)

    def note_preview_frame(self, elapsed_ms: float) -> None:
        self.preview_frame_count += 1
        self.preview_frame_ms_total += elapsed_ms
        self.preview_frame_ms_max = max(self.preview_frame_ms_max, elapsed_ms)

    def note_frame_callback(self, elapsed_ms: float) -> None:
        self.frame_callback_count += 1
        self.frame_callback_ms_total += elapsed_ms
        self.frame_callback_ms_max = max(self.frame_callback_ms_max, elapsed_ms)

    def note_chunk_accepted(self, accepted_ns: int) -> None:
        if self.chunk_ready_ns is None:
            return
        self.chunk_ready_to_accept_ms = _elapsed_ms(self.chunk_ready_ns, accepted_ns)


async def run_sim_episode(*, transport: Any, session_id: str, env: SimEnvProtocol,
                          min_send_interval_s: float = 0.0,
                          max_steps: int = DEFAULT_SIM_MAX_STEPS,
                          replan_steps: int = CHUNK_SIZE,
                          observation_builder: Callable[..., Any] | None = None,
                          on_line: Callable[[str], None] = print,
                          chunk_timeout_s: float = 60.0,
                          clock: Callable[[], int] = time.monotonic_ns,
                          sleep: Callable[[float], Awaitable[object]] = asyncio.sleep,
                          on_frame: Callable[..., None] | None = None,
                          on_buffer: Callable[[dict[str, Any]], None] | None = None,
                          on_policy_timing: Callable[[dict[str, Any]], None]
                          | None = None,
                          frame_interval_steps: int = 1,
                          frame_when_policy_pending: bool = True,
                          policy_runner: Any | None = None,
                          real_time: bool = True,
                          action_hz: int = LIBERO_ACTION_HZ) -> SimResult:
    builder = observation_builder or wire.build_libero_observation
    result = SimResult()
    metrics = SimMetrics(
        max_steps=max_steps,
        action_hz=action_hz,
        action_dt_s=1.0 / action_hz,
        real_time_enabled=real_time,
    )
    result.metrics = metrics.snapshot()
    reset_start_ns = clock()
    obs = env.reset()
    env_reset_ms = _elapsed_ms(reset_start_ns, clock())
    policy_profiles: list[SimPolicyProfile] = []
    preview_build_ms_values: list[float] = []
    frame_callback_ms_values: list[float] = []
    frame_interval = max(1, int(frame_interval_steps))
    pending_chunk: tuple[asyncio.Task, int, int, SimPolicyProfile] | None = None
    pacer = RealtimePacer(action_hz=action_hz, clock=clock)
    frame_sequence = 0

    def active_profile() -> SimPolicyProfile | None:
        return pending_chunk[3] if pending_chunk is not None else None

    def emit_frame(current_obs: Any, step: int, *, force: bool = False) -> None:
        nonlocal frame_sequence
        if on_frame is not None:
            if step != 0 and not force and step % frame_interval != 0:
                return
            if (
                pending_chunk is not None
                and not force
                and not frame_when_policy_pending
            ):
                return
            profile = active_profile()
            frame_start_ns = clock()
            frame = _policy_preview_frame(env, current_obs)
            preview_ms = _elapsed_ms(frame_start_ns, clock())
            preview_build_ms_values.append(preview_ms)
            if profile is not None:
                profile.note_preview_frame(preview_ms)
            frame_sequence += 1
            metadata = {
                "frame_id": frame_sequence,
                "step": step,
                "server_frame_created_ms": time.time() * 1000.0,
                "preview_build_ms": preview_ms,
                "policy_pending": pending_chunk is not None,
                "_server_frame_created_monotonic_ns": time.monotonic_ns(),
            }
            callback_start_ns = clock()
            _call_frame_callback(on_frame, frame, step, metadata)
            callback_ms = _elapsed_ms(callback_start_ns, clock())
            frame_callback_ms_values.append(callback_ms)
            if profile is not None:
                profile.note_frame_callback(callback_ms)

    emit_frame(obs, 0)
    buffer = EnsembleBuffer()
    chunks = (
        transport.action_chunks().__aiter__()
        if policy_runner is None
        else policy_runner.run(_action_chunks(transport))
    )
    observation_id = 0

    def emit_buffer(step: int) -> None:
        if on_buffer is None:
            return
        snapshot = metrics.snapshot()
        action_buffer = snapshot["action_buffer"]
        on_buffer({
            "step": step,
            "remaining": action_buffer["remaining"],
            "capacity": action_buffer["capacity"],
            "health": action_buffer["health"],
        })

    # Shared endpoints: at most one request per 400 ms, measured send to send. A request
    # that is due inside the floor waits for a later step, which observes afresh.
    floor_ns = int(max(0.0, float(min_send_interval_s)) * 1_000_000_000)
    last_send_ns: int | None = None

    def floor_ready() -> bool:
        if not floor_ns or last_send_ns is None:
            return True
        return clock() - last_send_ns >= floor_ns

    def start_request(
        current_obs: Any,
        start_tick: int,
    ) -> tuple[asyncio.Task, int, int, SimPolicyProfile]:
        nonlocal observation_id, last_send_ns
        if floor_ns:
            last_send_ns = clock()
        sent_observation_id = observation_id
        observation_id += 1
        profile = SimPolicyProfile(
            request_id=sent_observation_id,
            observation_id=sent_observation_id,
            start_step=start_tick,
        )
        build_start_ns = clock()
        observation = _build_sim_observation(
            builder=builder,
            session_id=session_id,
            observation_id=sent_observation_id,
            env=env,
            obs=current_obs,
        )
        profile.obs_build_ms = _elapsed_ms(build_start_ns, clock())
        policy_profiles.append(profile)
        send_coro = _send_observation_and_next(
            transport=transport,
            chunks=chunks,
            observation=observation,
            observation_id=sent_observation_id,
            timeout_s=chunk_timeout_s,
            metrics=metrics,
            clock=clock,
            profile=profile,
        )
        task = (
            asyncio.create_task(send_coro)
            if policy_runner is None
            else asyncio.wrap_future(policy_runner.submit(send_coro))
        )
        return task, start_tick, sent_observation_id, profile

    def accept_chunk(chunk: Any, *, start_tick: int, tick: int,
                     sent_observation_id: int,
                     profile: SimPolicyProfile) -> None:
        profile.note_chunk_accepted(clock())
        _add_chunk_to_buffer(buffer=buffer, chunk=chunk, start_tick=start_tick,
                             chunk_size=replan_steps, now_ns=clock())
        metrics.note_buffer(buffer.actions_remaining(tick), capacity=replan_steps)
        emit_buffer(tick)
        policy_call = result.policy_calls + 1
        send_to_chunk_ms = metrics.rtt_ms[-1] if metrics.rtt_ms else 0.0
        _complete_policy_profile(profile=profile, chunk=chunk,
                                 send_to_chunk_ms=send_to_chunk_ms)
        if on_policy_timing is not None:
            on_policy_timing(_policy_timing_event(
                profile=profile,
                policy_call=policy_call,
                step=tick,
                sent_observation_id=sent_observation_id,
                action_hz=action_hz,
                chunk_size=replan_steps,
            ))
        result.policy_calls = policy_call
        metrics.policy_calls = policy_call

    try:
        pending_chunk = start_request(obs, start_tick=0)
        # First inference is startup work. Begin the action clock with a usable
        # buffer; subsequent requests still overlap real-time simulation.
        task, start_tick, sent_observation_id, profile = pending_chunk
        accept_chunk(await task, start_tick=start_tick, tick=0,
                     sent_observation_id=sent_observation_id, profile=profile)
        pending_chunk = None
        episode_start_ns = pacer.start(clock())
        metrics.start_episode(episode_start_ns)

        for _ in range(max_steps):
            if real_time:
                metrics.note_realtime_tick(
                    await pacer.wait_async(result.steps, sleep=sleep)
                )
                if pending_chunk is not None:
                    await asyncio.sleep(0)

            if pending_chunk is not None and pending_chunk[0].done():
                task, start_tick, sent_observation_id, profile = pending_chunk
                accept_chunk(task.result(), start_tick=start_tick, tick=result.steps,
                             sent_observation_id=sent_observation_id, profile=profile)
                pending_chunk = None

            now_ns = clock()
            action = buffer.consume(result.steps, now_ns)
            if action is None:
                metrics.note_action_underrun()
                if pending_chunk is None and floor_ready():
                    pending_chunk = start_request(obs, start_tick=result.steps)
                    await asyncio.sleep(0)
                if real_time:
                    action = _zero_sim_action(env)
                else:
                    task, start_tick, sent_observation_id, profile = pending_chunk
                    accept_chunk(await task, start_tick=start_tick, tick=result.steps,
                                 sent_observation_id=sent_observation_id, profile=profile)
                    pending_chunk = None
                    now_ns = clock()
                    action = buffer.consume(result.steps, now_ns)
                    if action is None:
                        raise RuntimeError("policy returned no action for the current sim step")

            step_start_ns = clock()
            obs, done = env.step(action)
            step_ms = _elapsed_ms(step_start_ns, clock())
            if pending_chunk is not None:
                pending_chunk[3].note_env_step(step_ms)
            result.steps += 1
            if pending_chunk is not None and pending_chunk[0].done():
                task, start_tick, sent_observation_id, profile = pending_chunk
                accept_chunk(task.result(), start_tick=start_tick, tick=result.steps,
                             sent_observation_id=sent_observation_id, profile=profile)
                pending_chunk = None
            emit_frame(obs, result.steps, force=done)
            remaining = buffer.actions_remaining(result.steps)
            metrics.note_step(steps=result.steps, buffer_remaining=remaining)
            emit_buffer(result.steps)
            if done:
                result.done = True
                break

            if (
                pending_chunk is None
                and remaining <= max(1, replan_steps // 2)
                and floor_ready()
            ):
                pending_chunk = start_request(obs, start_tick=result.steps)
                await asyncio.sleep(0)
            elif pending_chunk is not None:
                await asyncio.sleep(0)
        if real_time and result.steps > 0:
            await pacer.wait_async(result.steps, sleep=sleep)
    finally:
        if pending_chunk is not None:
            await _cancel_pending_policy_task(pending_chunk[0])
        await _close_action_chunks(chunks, policy_runner=policy_runner)
        finish_ns = clock()
        metrics.finish(
            steps=result.steps,
            policy_calls=result.policy_calls,
            done=result.done,
            now_ns=finish_ns,
        )
        result.metrics = metrics.snapshot(now_ns=finish_ns)
        result.metrics["profile"] = _profile_summary(
            policy_profiles,
            env_reset_ms=env_reset_ms,
            preview_build_ms_values=preview_build_ms_values,
            frame_callback_ms_values=frame_callback_ms_values,
            action_hz=action_hz,
            chunk_size=replan_steps,
        )
        result.metrics["profile"]["realtime"] = result.metrics["realtime"]
    return result


def _build_sim_observation(*, builder: Callable[..., Any], session_id: str,
                           observation_id: int, env: SimEnvProtocol, obs: Any) -> Any:
    inputs = getattr(env, "observation_inputs", None)
    if callable(inputs):
        return builder(session_id=session_id, observation_id=observation_id,
                       instruction=env.task_description, **inputs(obs))
    return builder(
        session_id=session_id,
        observation_id=observation_id,
        agent_frame=env.agent_frame(obs),
        wrist_frame=env.wrist_frame(obs),
        libero_state=env.proprio(obs),
        instruction=env.task_description,
    )


async def _action_chunks(transport: Any) -> Any:
    return transport.action_chunks().__aiter__()


async def _close_action_chunks(chunks: Any, *, policy_runner: Any | None) -> None:
    close = getattr(chunks, "aclose", None)
    if close is None:
        return
    async def close_safely() -> None:
        try:
            await close()
        except RuntimeError as exc:
            if "aclose(): asynchronous generator is already running" not in str(exc):
                raise

    if policy_runner is None:
        try:
            await asyncio.wait_for(close_safely(), timeout=ACTION_CHUNKS_CLOSE_TIMEOUT_S)
        except TimeoutError:
            return
        return
    close_future = asyncio.wrap_future(policy_runner.submit(close_safely()))
    try:
        await asyncio.wait_for(close_future, timeout=ACTION_CHUNKS_CLOSE_TIMEOUT_S)
    except TimeoutError:
        return


async def _cancel_pending_policy_task(task: Any) -> None:
    if task.done():
        return
    task.cancel()
    try:
        await asyncio.wait_for(
            asyncio.gather(task, return_exceptions=True),
            timeout=PENDING_POLICY_CANCEL_TIMEOUT_S,
        )
    except TimeoutError:
        return


def _add_chunk_to_buffer(*, buffer: EnsembleBuffer, chunk: Any, start_tick: int,
                         chunk_size: int, now_ns: int) -> None:
    buffer.add_chunk(
        chunk_id=chunk.chunk_id,
        observation_id=chunk.generated_from_observation_id,
        actions=wire.chunk_actions(chunk)[:chunk_size],
        current_tick=start_tick - 1,
        now_ns=now_ns,
    )


class AlignedChunkBuffer:
    """The SDK runtime's output blend for `dreamscale sim` (as in the browser sim).

    Each chunk is aligned to the step it was requested at, steps already executed are
    dropped, and overlapping steps average old and new at the runtime's output weight
    (0.3 old / 0.7 new): policy/runtime/action_buffer.ActionBuffer.merge_aligned_chunk.
    """

    def __init__(self, contract: Any) -> None:
        smoothing = resolve_action_smoothing(
            RunStrategy(action_hz=contract.action_hz, chunk_size=contract.chunk_size,
                        action_smoothing="output"),
            contract,
        )
        self.new_weight = smoothing.new_weight
        self.chunk_size = int(contract.chunk_size)
        self._buffer = ActionBuffer()
        self.stale_steps = 0

    def add(self, chunk: Any, *, start_tick: int) -> dict[str, Any]:
        """Merge a chunk generated from the observation taken before step `start_tick`."""
        actions = wire.chunk_actions(chunk)[: self.chunk_size]
        indices = wire.chunk_action_indices(chunk)[: len(actions)]
        diagnostics = self._buffer.merge_aligned_chunk(
            base_action_step=start_tick,
            actions=actions,
            action_indices=indices or None,
            new_weight=self.new_weight,
        )
        self.stale_steps += int(diagnostics["stale_steps"])
        return diagnostics

    def consume(self, tick: int) -> list[float] | None:
        """The action for step `tick`, or None (an underrun; the same tick may be retried).
        Steps before `tick` are dropped: a step the sim held through never runs late."""
        if tick < self._buffer.next_action_step:
            raise ValueError("sim steps must be consumed in order")
        self._buffer.advance_to(tick)
        action = self._buffer.consume()
        return None if action is None else list(action)

    def actions_remaining(self, tick: int) -> int:
        return self._buffer.actions_remaining(tick)


def _zero_sim_action(env=None) -> list[float]:
    hold = getattr(env, "hold_action", None)
    if callable(hold):
        return hold()
    from dreamscale.sim.runtime import LIBERO_DUMMY_ACTION

    return list(LIBERO_DUMMY_ACTION)


def _default_env_factory(*, task_suite: str, task_id: int, task_seed: int,
                         control_freq: int = LIBERO_ACTION_HZ, env_resolution: int = 256,
                         camera_history: bool | tuple[int, ...] = False) -> Any:
    """``camera_history``: True for RLDX-1's window, or the steps back of each frame."""
    from dreamscale.sim.runtime import HistoryLiberoSimEnv, LiberoSimEnv, ensure_sim_ready

    ensure_sim_ready()
    if not camera_history:
        return LiberoSimEnv.create_default(
            task_suite_name=task_suite, task_id=task_id, seed=task_seed,
            control_freq=control_freq, env_resolution=env_resolution)
    env = HistoryLiberoSimEnv.create_default(
        task_suite_name=task_suite,
        task_id=task_id,
        seed=task_seed,
        control_freq=control_freq,
        env_resolution=env_resolution,
    )
    if camera_history is not True:
        env.set_history_ticks(camera_history)
    return env


def connect_libero(*, client_factory: Callable[..., Any] = ControlPlaneClient,
                   transport_connect: Callable[..., Any] = _default_transport_connect,
                   env_factory: Callable[[], Any] | None = None,
                   preflight_fn: Callable[..., Any] | None = None,
                   allow_fallback: bool = True,
                   relay_connect: Callable[..., Any] | None = None,
                   on_line: Callable[[str], None] = print,
                   sleep: Callable[..., Any] = asyncio.sleep,
                   heartbeat_interval_s: float = HEARTBEAT_S,
                   view: bool = True,
                   verbose: bool = False,
                   render_frame: Callable[[Any], None] | None = None,
                   close_render: Callable[[], None] | None = None,
                   region: RegionPreference | None = None,
                   idle_timeout: int | None = None,
                   keep_warm: int = 0,
                   task_suite: str = "libero_spatial",
                   task_id: int = 0,
                   task_seed: int = 0,
                   transport: TransportPreference = "auto",
                   model: str = MODEL_LIBERO,
                   benchmark: str = "libero",
                   steady_send: bool | int | None = None) -> SimArm:
    """Internal connector for Dreamscale's built-in local LIBERO sim path.

    This is intentionally separate from the generic public `dreamscale.connect()`
    contract used by downstream user-owned environments.

    ``steady_send`` (experimental, undocumented): ``True`` spaces sends to a shared
    model at least 400 ms apart, an int is that spacing in milliseconds (50 to 2000),
    ``None``/``False`` (the default) leaves the episode loop exactly as it is.
    """
    from dreamscale.policy.remote import resolve_steady_send
    from dreamscale.sim.benchmarks import validate_selection

    keep_warm = _validate_keep_warm(keep_warm)
    resolve_steady_send(steady_send)  # a bad value fails here, before any compute opens
    task_id = validate_selection(benchmark, model, task_suite, task_id)
    contract = _sim_contract(model)
    config = load_config()
    if not config.api_key:
        raise errors.catalog("not_configured")
    if transport not in ("auto", "quic", "relay"):
        raise ValueError('transport must be "auto", "quic", or "relay"')
    if preflight_fn is None:
        from dreamscale_transport import diagnose_udp as preflight_fn
    preflight_fn = _compatible_diagnose_udp(preflight_fn)

    if benchmark == "roboeval" and env_factory is None:
        from dreamscale.sim.roboeval_runtime import RoboEvalSimEnv, ensure_roboeval_runtime

        python = ensure_roboeval_runtime(on_line=on_line)
        env_factory = partial(RoboEvalSimEnv, family=task_suite, variant=str(task_id),
                              seed=task_seed, python=python)

    if benchmark == "robocasa365" and env_factory is None:
        from dreamscale.sim.robocasa_runtime import RoboCasaSimEnv, ensure_robocasa_runtime

        python = ensure_robocasa_runtime(on_line=on_line)
        # Its arm control ("eef_delta", or DROID's absolute joints): the model's Sim.env_options.
        env_factory = partial(
            RoboCasaSimEnv, task=str(task_id), seed=task_seed, python=python,
            **_SIMS[model].env_options,
        )

    prepared_env = None
    if benchmark == "molmospaces" and env_factory is None:
        from dreamscale.sim.molmospaces_runtime import MolmoSpacesSimEnv

        # Asset/native failures must happen before opening a billable session.
        prepared_env = MolmoSpacesSimEnv(suite=task_suite, task_id=int(task_id), seed=task_seed)
        def env_factory():
            return prepared_env

    runner = _LoopRunner()
    client: Any | None = None
    created: Any | None = None
    env: Any | None = prepared_env
    heartbeat: Heartbeat | None = None
    try:
        client, created = runner.run(_create_session_async(
            config=config, client_factory=client_factory, on_line=on_line,
            verbose=verbose, region=region, idle_timeout=idle_timeout, model=model,
            keep_warm=keep_warm,
        ))
        heartbeat = runner.run(_start_heartbeat(
            client=client,
            session_id=created.session_id,
            interval_s=heartbeat_interval_s,
        ))
        label = BENCHMARK_LABELS[benchmark]
        on_line(f"Preparing the local {label}/MuJoCo environment…")
        # MuJoCo/robosuite can trap on macOS when constructed or destroyed
        # off the caller/main thread. Keep simulator lifecycle here; the
        # already-created cloud session still boots concurrently.
        if env_factory is None:
            env = _default_env_factory(
                task_suite=task_suite,
                task_id=task_id,
                task_seed=task_seed,
                **({"control_freq": int(contract.action_hz)}
                   if _SIMS[model].control_freq else {}),
                **_SIMS[model].env_options,
            )
        else:
            env = env_factory()
        on_line(f"[local] task: {env.task_description}")
        sim = runner.run(_finish_connect_async(
            runner=runner, client=client, created=created,
            transport_connect=transport_connect, env=env,
            preflight_fn=preflight_fn, allow_fallback=allow_fallback,
            transport_preference=transport,
            relay_connect=relay_connect, heartbeat=heartbeat,
            on_line=on_line, sleep=sleep, view=view,
            render_frame=render_frame, close_render=close_render,
            verbose=verbose, model=model, keep_warm=keep_warm, steady_send=steady_send,
        ))
        heartbeat = None
        env = None
        return sim
    except BaseException:
        cleanup_interrupt: BaseException | None = None

        def note_cleanup_interrupt(exc: BaseException) -> None:
            nonlocal cleanup_interrupt
            if not isinstance(exc, Exception) and cleanup_interrupt is None:
                cleanup_interrupt = exc

        try:
            if env is not None:
                try:
                    env.close()
                except BaseException as exc:
                    note_cleanup_interrupt(exc)
            if heartbeat is not None:
                try:
                    runner.run_cleanup(heartbeat.stop())
                except BaseException as exc:
                    note_cleanup_interrupt(exc)
            if client is not None:
                try:
                    runner.run_cleanup(_cleanup_created_session(client, created))
                except BaseException as exc:
                    note_cleanup_interrupt(exc)
        finally:
            runner.shutdown()
        if cleanup_interrupt is not None:
            raise cleanup_interrupt from None
        raise


async def _create_session_async(*, config, client_factory, on_line,
                                verbose: bool,
                                region: RegionPreference | None = None,
                                idle_timeout: int | None = None,
                                model: str = MODEL_LIBERO,
                                keep_warm: int = 0) -> tuple[Any, Any]:
    client = client_factory(config.control_plane_url, config.api_key)
    created: Any | None = None
    returned = False
    try:
        # Session FIRST — the GPU boots while sim assets install.
        created = await create_session_with_rtt_region_order(
            client,
            model, region=region or config.preferred_region or "nearest",
            idle_timeout=idle_timeout,
            keep_warm=keep_warm,
        )
        if verbose:
            on_line(f"[cloud] session: {created.session_id}")
        on_line("[cloud] session created; GPU worker boots in the background")
        returned = True
        return client, created
    finally:
        if not returned:
            if created is not None:
                await stop_session(client, created.session_id)
            await client.close()


async def _start_heartbeat(*, client: Any, session_id: str, interval_s: float) -> Heartbeat:
    heartbeat = Heartbeat(client, session_id, interval_s=interval_s)
    heartbeat.start()
    return heartbeat


async def _cleanup_created_session(client: Any, created: Any | None) -> None:
    try:
        if created is not None:
            await stop_session(client, created.session_id)
    finally:
        await client.close()


async def _finish_connect_async(*, runner, client, created, transport_connect,
                                env, preflight_fn, allow_fallback,
                                transport_preference, relay_connect, heartbeat,
                                on_line, sleep, view, render_frame, close_render,
                                verbose, model=MODEL_LIBERO, keep_warm=0,
                                steady_send: bool | int | None = None) -> SimArm:
    # The simulator is ready; now wait for the worker, preflight UDP, and pin QUIC.
    session = await wait_until_ready(client, created, on_progress=on_line, sleep=sleep)
    transport = quic_upgrade = transport_reports = None

    async def quic_connect(ready_session):
        return await _pin_connect(transport_connect, ready_session)

    async def relay_connect_for_session(ready_session):
        connect = relay_connect or getattr(client, "connect_relay", None)
        if connect is None:
            raise errors.catalog("relay_unavailable")
        return await connect(ready_session)

    if verbose:
        on_line(f"[cloud] endpoint: {session.worker_addr}:{session.port}")
    try:
        if session.data_plane is not None:
            if transport_preference != "auto":
                raise ValueError("session-scoped WebSocket compute requires transport='auto'")
            connect_data_plane = getattr(client, "connect_data_plane", None)
            if not callable(connect_data_plane):
                raise RuntimeError("control-plane client cannot connect the assigned data plane")
            transport = await connect_data_plane(session)
            transport.mode = "wss_tunnel"
            transport.fallback_reason = None
            transport.primary_preflight_status = None
            transport.diagnostic_preflight_status = None
            # Punched QUIC when the control plane and the worker offer it, as the SDK does
            # (policy.lifecycle): it reports the path now and at every switch.
            transport_reports = ModalTransportReports(
                getattr(client, "report_transport", None), session.session_id, on_line
            )
            quic_upgrade = await _start_modal_quic(session, transport, transport_reports)
        elif transport_preference == "relay":
            transport = await relay_connect_for_session(session)
            transport.mode = getattr(transport, "mode", "relay")
            transport.fallback_reason = None
            transport.primary_preflight_status = None
            transport.diagnostic_preflight_status = None
            await _report_transport_best_effort(
                getattr(client, "report_transport", None),
                session.session_id,
                transport_protocol="relay",
                fallback_used=False,
                fallback_reason=None,
                primary_preflight_status=None,
                diagnostic_preflight_status=None,
            )
        else:
            transport = await connect_selected_transport(
                session,
                diagnose_udp_fn=preflight_fn,
                quic_connect=quic_connect,
                relay_connect=relay_connect_for_session,
                allow_fallback=allow_fallback and transport_preference == "auto",
                on_line=on_line,
                notice_style="cli_transport",
                report_transport_fn=getattr(client, "report_transport", None),
            )
        chunks = transport.action_chunks().__aiter__()
        if view:
            if render_frame is None:
                native_render = getattr(env, "render_frame", None)
                render_frame = native_render if callable(native_render) else _render_preview_frame
                if not callable(native_render):
                    close_render = close_render or _close_preview
            cameras = (_VIEWER_CAMERAS.get(_observation(model), "agent | wrist")
                       if model in NATIVE_OBSERVATION_MODELS else "agent | wrist")
            on_line(f"Live viewer: local window ({cameras}) opens on episode start.")
        else:
            render_frame = None
            close_render = None
        return SimArm(runner=runner, client=client, session=session, transport=transport,
                      chunks=chunks, env=env, heartbeat=heartbeat, on_line=on_line,
                      render_frame=render_frame, close_render=close_render, model=model,
                      keep_warm=keep_warm, steady_send=steady_send,
                      quic_upgrade=quic_upgrade, transport_reports=transport_reports)
    except BaseException:
        if quic_upgrade is not None:
            quic_upgrade.cancel()
            await asyncio.gather(quic_upgrade, return_exceptions=True)
        if transport_reports is not None:
            await transport_reports.cancel()
        if transport is not None:
            with suppress(Exception):
                await transport.close()
        raise


async def _send_observation_and_next(*, transport: Any, chunks: Any,
                                     observation: Any, timeout_s: float,
                                     observation_id: int | None = None,
                                     metrics: SimMetrics | None = None,
                                     tui: SimMetricsTui | None = None,
                                     clock: Callable[[], int] = time.monotonic_ns,
                                     profile: SimPolicyProfile | None = None) -> Any:
    start_ns = clock()
    if observation_id is None:
        frame = getattr(observation, "frame", None)
        observation_id = getattr(frame, "observation_id", None)
    if metrics is not None and observation_id is not None:
        metrics.note_observation_sent(
            observation_id=int(observation_id),
            observation=observation,
            now_ns=start_ns,
        )
        if tui is not None:
            tui.render(metrics, force=True)
    send_start_ns = clock()
    await transport.send_observation(observation)
    send_end_ns = clock()
    if profile is not None:
        profile.transport_send_ms = _elapsed_ms(send_start_ns, send_end_ns)
    deadline_ns = start_ns + int(timeout_s * 1_000_000_000)
    chunk_task = asyncio.create_task(chunks.__anext__())
    try:
        while True:
            now_ns = clock()
            remaining_s = (deadline_ns - now_ns) / 1_000_000_000.0
            if remaining_s <= 0:
                chunk_task.cancel()
                raise TimeoutError()
            try:
                chunk = await asyncio.wait_for(
                    asyncio.shield(chunk_task),
                    timeout=min(0.1, remaining_s),
                )
                break
            except TimeoutError:
                if metrics is not None:
                    metrics.note_in_flight(clock())
                    if tui is not None:
                        tui.render(metrics)
    except BaseException:
        if not chunk_task.done():
            chunk_task.cancel()
            await asyncio.gather(chunk_task, return_exceptions=True)
        raise
    end_ns = clock()
    if profile is not None:
        profile.chunk_ready_ns = end_ns
        profile.wait_for_chunk_ms = _elapsed_ms(send_end_ns, end_ns)
    if metrics is not None:
        metrics.note_chunk_received(
            chunk=chunk,
            rtt_ms=(end_ns - start_ns) / 1_000_000.0,
            now_ns=end_ns,
            actions_added=len(wire.chunk_actions(chunk)),
        )
        if tui is not None:
            tui.render(metrics, force=True)
    return chunk


class _SimEpisode:
    """An episode the server keeps (a contract with ``episode_tick_steps``: Praxis-1) in a
    stateful sim. Steps count executed actions from the episode's first request; every executed
    step's frames go ahead (``history_frame``, keyed by the step), and each request names its
    step and carries the joints of every step executed since the last one (``state_history``,
    oldest first), its frames at the model's wire image."""

    def __init__(self, *, contract, env, send) -> None:
        self.contract = contract
        self.env = env
        self.send = send
        self.step = 0
        self.chunk = 0
        self.states: list[list[float]] = []

    def _inputs(self, obs: Any) -> dict:
        return self.env.observation_inputs(obs)

    @staticmethod
    def _state(inputs: dict) -> list[float]:
        return [*map(float, inputs["joint_positions"]), float(inputs["gripper"])]

    def executed(self, obs: Any, executed: int, more: bool) -> None:
        self.step = executed
        inputs = self._inputs(obs)
        if not more:
            return  # the next request carries this step's frames and state itself
        self.states.append(self._state(inputs))
        with wire.wire_image(self.contract.wire_image):
            frames = {camera_id: wire._camera_frame(camera_id, inputs[source])[1]
                      for camera_id, source in (
                          (wire.CAMERA_KEY_DROID_EXTERIOR_1, "exterior_frame"),
                          (wire.CAMERA_KEY_DROID_WRIST, "wrist_frame"))}
        self.send(executed, frames)

    def request(self, observation: Any, obs: Any) -> Any:
        from dreamscale_transport.messages import EpisodeRequestContext, RuntimeRequestContext

        update: dict[str, Any] = {"runtime_context": RuntimeRequestContext(
            episode=EpisodeRequestContext(step=self.step, chunk=self.chunk, seed=0))}
        if self.states:
            update["state_history"] = self.states
        self.chunk += 1
        self.states = [self._state(self._inputs(obs))]
        return dataclasses.replace(observation, frame=observation.frame.model_copy(update=update))


class SimArm:
    def __init__(self, *, runner, client, session, transport, chunks, env,
                 heartbeat, on_line, render_frame, close_render, model=MODEL_LIBERO,
                 keep_warm: int = 0, steady_send: bool | int | None = None,
                 quic_upgrade=None, transport_reports=None) -> None:
        self.model = model
        # A punched-QUIC upgrade still running after connect, and the reports that follow it.
        self._quic_upgrade = quic_upgrade
        self._transport_reports = transport_reports
        # Experimental opt-in send floor (see policy.remote.send_floor_s); off by default.
        self.steady_send = steady_send
        self._contract = _sim_contract(model)
        self._runner = runner
        self._client = client
        self._session = session
        self._transport = transport
        self._chunks = chunks
        self._env = env
        self._heartbeat = heartbeat
        self._on_line = on_line
        self._render_frame = render_frame
        self._close_render = close_render
        self._closed = False
        self._keep_warm = _validate_keep_warm(keep_warm)
        self.release_status: str | None = None
        self._next_observation_id = 0
        self._dreamzero_generation = -1
        self._send_window_ahead()

    def _send_window_ahead(self) -> None:
        """A model that sends its window ahead, on a server that takes history frames: each frame
        goes out once and requests name them. World-model LIBERO (``wm_libero.SENDS_AHEAD``)
        sends every frame as it is rendered; a model whose sim sets ``send_ahead_kept`` (a long
        sparse window) only the frames its next window names."""
        from dreamscale_transport.websocket_client import HISTORY_FRAMES_CAPABILITY
        from dreamscale_transport.wm_libero import SENDS_AHEAD

        send_ahead = getattr(self._env, "send_frames_ahead", None)
        kept = _SIMS[self.model].send_ahead_kept if self.model in _SIMS else None
        if ((self.model not in SENDS_AHEAD and kept is None) or send_ahead is None
                or HISTORY_FRAMES_CAPABILITY not in getattr(self._transport, "capabilities", ())):
            return

        def send(key: int, agent: Any, wrist: Any) -> bool:
            frames = {CAMERA_KEY_LIBERO_AGENT: wire.encode_jpeg(agent),
                      CAMERA_KEY_LIBERO_WRIST: wire.encode_jpeg(wrist)}
            # Submitted in order with the requests that name it, on the same ordered stream.
            sent = self._runner.submit(self._transport.send_history_frames(key, frames))
            sent.add_done_callback(lambda future: future.exception())  # a lost frame repeats
            return True

        if kept is not None:
            send_ahead(send, kept=kept)
        else:
            send_ahead(send)

    def do(self, max_steps: int = DEFAULT_SIM_MAX_STEPS, *, tui: bool = True,
           real_time: bool = True,
           sleep: Callable[[float], object] = time.sleep,
           on_frame: Callable[..., None] | None = None,
           on_buffer: Callable[[dict[str, Any]], None] | None = None,
           on_policy_timing: Callable[[dict[str, Any]], None] | None = None,
           count_holds: bool | None = None) -> SimResult:
        """``count_holds``: whether the ticks a stateful model holds while a request is in
        flight count toward ``max_steps``; by default they do except on LIBERO."""
        if self.model in STATEFUL_MODELS:
            return self._do_stateful(max_steps=max_steps,tui=tui,real_time=real_time,sleep=sleep,
                on_frame=on_frame,on_buffer=on_buffer,on_policy_timing=on_policy_timing,
                count_holds=not _budgets_actions(self.model, count_holds))
        result = SimResult()
        metrics = SimMetrics(
            max_steps=max_steps,
            action_hz=self._contract.action_hz,
            action_dt_s=1.0 / self._contract.action_hz,
            real_time_enabled=real_time,
        )
        result.metrics = metrics.snapshot()
        live_metrics = SimMetricsTui(enabled=tui)
        self._prepare_task()
        obs = self._env.reset()
        buffer = AlignedChunkBuffer(self._contract)
        observation_id = 0
        pending_chunk: tuple[Any, int, int, SimPolicyProfile] | None = None
        pacer = RealtimePacer(action_hz=self._contract.action_hz)
        frame_sequence = 0
        metrics.note_buffer(0, capacity=self._contract.chunk_size)
        live_metrics.render(metrics, force=True)

        def active_profile() -> SimPolicyProfile | None:
            return pending_chunk[3] if pending_chunk is not None else None

        def emit_frame(current_obs: Any, step: int) -> None:
            nonlocal frame_sequence
            if self._render_frame is None and on_frame is None:
                return
            profile = active_profile()
            frame_start_ns = time.monotonic_ns()
            frame = _policy_preview_frame(
                self._env, current_obs,
                image_size=_sim_image_size(self.model),
            )
            preview_ms = _elapsed_ms(frame_start_ns, time.monotonic_ns())
            if profile is not None:
                profile.note_preview_frame(preview_ms)
            if self._render_frame is not None:
                self._render_frame(frame)
            if on_frame is None:
                return
            frame_sequence += 1
            metadata = {
                "frame_id": frame_sequence,
                "step": step,
                "server_frame_created_ms": time.time() * 1000.0,
                "preview_build_ms": preview_ms,
                "policy_pending": pending_chunk is not None,
                "_server_frame_created_monotonic_ns": time.monotonic_ns(),
            }
            callback_start_ns = time.monotonic_ns()
            _call_frame_callback(on_frame, frame, step, metadata)
            callback_ms = _elapsed_ms(callback_start_ns, time.monotonic_ns())
            if profile is not None:
                profile.note_frame_callback(callback_ms)

        def emit_buffer(step: int) -> None:
            if on_buffer is None:
                return
            snapshot = metrics.snapshot()
            action_buffer = snapshot["action_buffer"]
            on_buffer({
                "step": step,
                "remaining": action_buffer["remaining"],
                "capacity": action_buffer["capacity"],
                "health": action_buffer["health"],
            })

        from dreamscale.policy.remote import send_floor_s

        # Real-time episodes space their requests like every other shared-endpoint
        # client; synchronous evaluation pauses physics per request and is unchanged.
        floor_ns = (
            int(send_floor_s(self.model, steady_send=self.steady_send) * 1_000_000_000)
            if real_time else 0
        )
        last_send_ns: int | None = None

        def floor_ready() -> bool:
            if not floor_ns or last_send_ns is None:
                return True
            return time.monotonic_ns() - last_send_ns >= floor_ns

        def start_request(current_obs: Any, start_tick: int):
            nonlocal observation_id, last_send_ns
            last_send_ns = time.monotonic_ns()
            sent_observation_id = observation_id
            observation_id += 1
            profile = SimPolicyProfile(
                request_id=sent_observation_id,
                observation_id=sent_observation_id,
                start_step=start_tick,
            )
            build_start_ns = time.monotonic_ns()
            observation = _build_sim_observation(
                builder=_sim_builder(self.model),
                session_id=self._session.session_id,
                observation_id=sent_observation_id,
                env=self._env,
                obs=current_obs,
            )
            profile.obs_build_ms = _elapsed_ms(build_start_ns, time.monotonic_ns())
            return self._runner.submit(_send_observation_and_next(
                transport=self._transport,
                chunks=self._chunks,
                observation=observation,
                observation_id=sent_observation_id,
                timeout_s=60.0,
                metrics=metrics,
                tui=live_metrics,
                profile=profile,
            )), start_tick, sent_observation_id, profile

        def accept_chunk(chunk: Any, *, start_tick: int, tick: int,
                         sent_observation_id: int,
                         profile: SimPolicyProfile) -> None:
            profile.note_chunk_accepted(time.monotonic_ns())
            buffer.add(chunk, start_tick=start_tick)
            metrics.note_buffer(buffer.actions_remaining(tick), capacity=self._contract.chunk_size)
            emit_buffer(tick)
            policy_call = result.policy_calls + 1
            send_to_chunk_ms = metrics.rtt_ms[-1] if metrics.rtt_ms else 0.0
            _complete_policy_profile(profile=profile, chunk=chunk,
                                     send_to_chunk_ms=send_to_chunk_ms)
            if on_policy_timing is not None:
                on_policy_timing(_policy_timing_event(
                    profile=profile,
                    policy_call=policy_call,
                    step=tick,
                    sent_observation_id=sent_observation_id,
                    action_hz=self._contract.action_hz,
                    chunk_size=self._contract.chunk_size,
                ))
            result.policy_calls = policy_call
            metrics.policy_calls = policy_call

        try:
            emit_frame(obs, 0)
            pending_chunk = start_request(obs, start_tick=0)
            future, start_tick, sent_observation_id, profile = pending_chunk
            accept_chunk(future.result(), start_tick=start_tick, tick=0,
                         sent_observation_id=sent_observation_id, profile=profile)
            pending_chunk = None
            episode_start_ns = pacer.start()
            metrics.start_episode(episode_start_ns)

            for _ in range(max_steps):
                if real_time:
                    metrics.note_realtime_tick(
                        pacer.wait(result.steps, sleep=sleep)
                    )
                    if pending_chunk is not None:
                        time.sleep(0)

                if pending_chunk is not None and pending_chunk[0].done():
                    future, start_tick, sent_observation_id, profile = pending_chunk
                    accept_chunk(future.result(), start_tick=start_tick, tick=result.steps,
                                 sent_observation_id=sent_observation_id, profile=profile)
                    pending_chunk = None

                action = buffer.consume(result.steps)
                if action is None:
                    metrics.note_action_underrun()
                    if pending_chunk is None and floor_ready():
                        pending_chunk = start_request(obs, start_tick=result.steps)
                    if real_time:
                        action = _zero_sim_action(self._env)
                    else:
                        future, start_tick, sent_observation_id, profile = pending_chunk
                        accept_chunk(future.result(), start_tick=start_tick, tick=result.steps,
                                     sent_observation_id=sent_observation_id, profile=profile)
                        pending_chunk = None
                        action = buffer.consume(result.steps)
                        if action is None:
                            raise RuntimeError(
                                "policy returned no action for the current sim step"
                            )

                step_start_ns = time.monotonic_ns()
                obs, done = self._env.step(action)
                step_ms = _elapsed_ms(step_start_ns, time.monotonic_ns())
                if pending_chunk is not None:
                    pending_chunk[3].note_env_step(step_ms)
                result.steps += 1
                if pending_chunk is not None:
                    time.sleep(0)
                if pending_chunk is not None and pending_chunk[0].done():
                    future, start_tick, sent_observation_id, profile = pending_chunk
                    accept_chunk(
                        future.result(),
                        start_tick=start_tick,
                        tick=result.steps,
                        sent_observation_id=sent_observation_id,
                        profile=profile,
                    )
                    pending_chunk = None
                emit_frame(obs, result.steps)
                remaining = buffer.actions_remaining(result.steps)
                metrics.note_step(steps=result.steps, buffer_remaining=remaining)
                emit_buffer(result.steps)
                live_metrics.render(metrics)
                if done:
                    result.done = True
                    break

                if (
                    pending_chunk is None
                    and remaining <= self._contract.chunk_size // 2
                    and floor_ready()
                ):
                    pending_chunk = start_request(obs, start_tick=result.steps)
                    time.sleep(0)
            if real_time and result.steps > 0:
                pacer.wait(result.steps, sleep=sleep)
            return result
        finally:
            if pending_chunk is not None and not pending_chunk[0].done():
                pending_chunk[0].cancel()
            finish_ns = time.monotonic_ns()
            metrics.finish(
                steps=result.steps,
                policy_calls=result.policy_calls,
                done=result.done,
                now_ns=finish_ns,
            )
            result.metrics = metrics.snapshot(now_ns=finish_ns)
            live_metrics.render(metrics, force=True)
            live_metrics.close()

    def _prepare_task(self):
        if "task_prepare_v1" not in getattr(self._transport, "capabilities", ()):
            return
        from dreamscale.terminal import compute_progress

        with compute_progress(self._on_line, ready_message="Task ready.") as progress:
            progress("Preparing task…: 0s elapsed")
            # A new Xiaomi instruction can compile a new attention shape (~148s
            # observed on H100). This happens outside the timed physics loop.
            kwargs = {"timeout_s": runtime_contract_for_model(self.model).task_prepare_timeout_s}
            self._runner.run(self._transport.prepare_task(self._env.task_description, **kwargs))

    def _do_stateful(
        self, *, max_steps, tui, real_time, sleep, on_frame, on_buffer, on_policy_timing,
        count_holds=True,
    ):
        from dreamscale.sim.stateful import run_stateful_episode

        result = SimResult()
        metrics = SimMetrics(
            max_steps=max_steps, action_hz=self._contract.action_hz,
            action_dt_s=1/self._contract.action_hz, real_time_enabled=real_time
        )
        live = SimMetricsTui(enabled=tui)
        self._prepare_task()
        execute = self._contract.execution_chunk_size
        longer_horizon = execute < self._contract.chunk_size
        dreamzero = self.model == MODEL_DREAMZERO_DROID
        if dreamzero:
            # Each episode is a new DreamZero cache generation that restarts at T1.
            self._dreamzero_generation += 1
        boundaries = 0
        episode = None
        if self._contract.episode_tick_steps and self.model in NATIVE_OBSERVATION_MODELS:
            def send_frames(key, frames):
                # Submitted in order with the requests that read them, on the same stream.
                sent = self._runner.submit(self._transport.send_history_frames(key, frames))
                sent.add_done_callback(lambda future: future.exception())  # repeats a neighbour

            episode = _SimEpisode(contract=self._contract, env=self._env, send=send_frames)

        def submit(frames):
            nonlocal boundaries
            observation_id = self._next_observation_id
            self._next_observation_id += 1
            profile = SimPolicyProfile(
                request_id=observation_id, observation_id=observation_id, start_step=result.steps
            )
            started = time.monotonic_ns()
            action_index = None
            if dreamzero:
                action_index = boundaries * DREAMZERO_REPLAN_STRIDE
                boundaries += 1
                observation = _dreamzero_observation(
                    env=self._env, obs=frames, session_id=self._session.session_id,
                    observation_id=observation_id, action_index=action_index,
                    cache_generation=self._dreamzero_generation,
                )
            elif episode is not None:
                with wire.wire_image(self._contract.wire_image):
                    observation = _build_sim_observation(builder=_sim_builder(self.model),
                        session_id=self._session.session_id, observation_id=observation_id,
                        env=self._env, obs=frames)
                observation = episode.request(observation, frames)
            elif self.model in NATIVE_OBSERVATION_MODELS:
                observation = _build_sim_observation(builder=_sim_builder(self.model),
                    session_id=self._session.session_id, observation_id=observation_id,
                    env=self._env, obs=frames)
            else:
                observation = wire.build_lingbot_observation(
                    session_id=self._session.session_id,
                    observation_id=observation_id,
                    frames=frames,
                    instruction=self._env.task_description,
                )
            profile.obs_build_ms = _elapsed_ms(started, time.monotonic_ns())
            future = self._runner.submit(
                _send_observation_and_next(
                    transport=self._transport,
                    chunks=self._chunks,
                    observation=observation,
                    observation_id=observation_id,
                    timeout_s=120 if _observation(self.model) in _SLOW_OBSERVATIONS else 60,
                    metrics=metrics,
                    tui=live,
                    profile=profile,
                )
            )

            class Pending:
                def done(inner):
                    return future.done()

                def cancel(inner):
                    return future.cancel()

                def result(inner):
                    chunk = future.result()
                    if (
                        chunk.session_id != self._session.session_id
                        or chunk.generated_from_observation_id != observation_id
                    ):
                        raise ValueError("Policy response does not match the pending observation")
                    profile.note_chunk_accepted(time.monotonic_ns())
                    _complete_policy_profile(
                        profile=profile, chunk=chunk, send_to_chunk_ms=metrics.rtt_ms[-1]
                    )
                    if on_policy_timing:
                        on_policy_timing(
                            _policy_timing_event(
                                profile=profile,
                                policy_call=result.policy_calls + 1,
                                step=result.steps,
                                sent_observation_id=observation_id,
                                action_hz=self._contract.action_hz,
                                chunk_size=len(chunk.actions),
                            )
                        )
                    if dreamzero:
                        return _dreamzero_boundary_actions(
                            chunk, action_index=action_index,
                            cache_generation=self._dreamzero_generation,
                        )
                    # A model generating a longer horizon than it executes (Rho, RLDX) replans
                    # after its executed prefix.
                    actions = wire.chunk_actions(chunk)
                    return actions[:execute] if longer_horizon else actions

            return Pending()

        def frame(obs, step, pending):
            if self._render_frame is None and on_frame is None:
                return
            if self.model in NATIVE_OBSERVATION_MODELS:
                preview = _policy_preview_frame(self._env, obs)
            else:
                preview = np.concatenate(
                    [self._env.agent_frame(obs)[::-1], self._env.wrist_frame(obs)[::-1]], axis=1
                )
            if self._render_frame:
                self._render_frame(preview)
            if on_frame:
                _call_frame_callback(
                    on_frame,
                    preview,
                    step,
                    {
                        "frame_id": step + 1,
                        "step": step,
                        "server_frame_created_ms": time.time() * 1000,
                        "policy_pending": pending,
                        "_server_frame_created_monotonic_ns": time.monotonic_ns(),
                    },
                )

        def buffer(step, remaining):
            if on_buffer:
                on_buffer({"step": step, **metrics.snapshot()["action_buffer"]})
            live.render(metrics)

        try:
            return run_stateful_episode(
                env=self._env,
                submit=submit,
                result=result,
                max_steps=max_steps,
                count_holds=count_holds,
                action_hz=self._contract.action_hz,
                real_time=real_time,
                sleep=sleep,
                on_frame=frame,
                on_buffer=buffer,
                metrics=metrics,
                on_executed=episode.executed if episode is not None else None,
                **({"action_dim": 8, "initial_chunk_size": DREAMZERO_REPLAN_STRIDE,
                    "chunk_size": DREAMZERO_REPLAN_STRIDE,
                    "request_input": lambda obs: obs, "hold_action": self._env.hold_action,
                    "hold_description": "physics paused during inference (upstream_eval)",
                    "feedback_description": (
                        "DROID camera views and proprioception every eight actions"
                    ),
                    "drain_pending": True, "pause_for_inference": True}
                   if dreamzero else
                   # A native observation: the model's own width, executing its executed
                   # prefix, with its observation's hold and feedback.
                   {"action_dim": self._contract.action_dim, "initial_chunk_size": execute,
                    "chunk_size": execute, "min_chunk_size": self._contract.fewest_chunk_rows,
                    "request_input": lambda obs: obs,
                    "hold_action": self._env.hold_action,
                    **stateful_settings(self.model)}
                   if self.model in NATIVE_OBSERVATION_MODELS else {}),
            )
        finally:
            live.render(metrics, force=True)
            live.close()

    def _render(self, obs: Any) -> None:
        if self._render_frame is None:
            return
        self._render_frame(_policy_preview_frame(self._env, obs))

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        try:
            self._runner.run_cleanup(self._close_async())
        finally:
            try:
                if self._close_render is not None:
                    self._close_render()
            finally:
                try:
                    self._env.close()
                finally:
                    self._runner.shutdown()

    async def _close_async(self) -> None:
        connection = PolicyConnection(
            client=self._client, session=self._session, transport=self._transport,
            heartbeat=self._heartbeat, transport_mode=getattr(self._transport, "mode", "quic"),
            keep_warm=self._keep_warm, quic_upgrade=self._quic_upgrade,
            transport_reports=self._transport_reports,
        )
        with suppress(Exception):
            await connection.close()
        self.release_status = connection.release_status

    def __enter__(self) -> SimArm:
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


def run_sim(*, max_steps: int = DEFAULT_SIM_MAX_STEPS, view: bool = True,
            verbose: bool = False,
            json_output: bool = False,
            tui: bool = True,
            real_time: bool = True,
            region: RegionPreference | None = None,
            model: str,
            benchmark: str = "libero",
            transport: TransportPreference = "auto",
            task_suite: str = "libero_spatial",
            task_id: int | str = 0,
            task_seed: int = 0,
            keep_warm: int = 0,
            output_root: Path | None = None,
            on_line: Callable[[str], None] = print,
            count_holds: bool | None = None,
            **kwargs) -> SimResult:
    """`dreamscale sim` entry point."""
    from dreamscale.sim.benchmarks import validate_selection

    keep_warm = _validate_keep_warm(keep_warm)
    task_id = validate_selection(benchmark, model, task_suite, task_id)
    contract = _sim_contract(model)
    live_tui = tui and not json_output and sys.stdout.isatty()
    _print_sim_run_card(max_steps=max_steps, view=view, tui=live_tui,
                        on_line=on_line, model=model, benchmark=benchmark,
                        actions=_budgets_actions(model, count_holds))
    if keep_warm:  # shared models never keep warm, so they say nothing about it
        on_line(f"keep warm: {keep_warm}s after run (billable)")
    recorder = None
    if output_root is not None:
        from dreamscale.sim.artifacts import SimArtifactRecorder

        video_writer = None
        if benchmark == "robocasa365":
            from dreamscale.sim.robocasa_runtime import write_sim_video

            video_writer = write_sim_video
        elif benchmark == "roboeval":
            from dreamscale.sim.roboeval_runtime import write_sim_video

            video_writer = write_sim_video
        recorder = SimArtifactRecorder(
            Path(output_root).expanduser().resolve(),
            fps=contract.action_hz,
            **({"video_writer": video_writer} if video_writer is not None else {}),
        )
        recorder.start()
    result: SimResult | None = None
    summary: dict[str, Any] | None = None
    sim = None
    try:
        sim = connect_libero(
            on_line=on_line,
            model=model,
            **({"benchmark": benchmark} if benchmark != "libero" else {}),
            view=view,
            verbose=verbose,
            region=region,
            transport=transport,
            task_suite=task_suite,
            task_id=task_id,
            task_seed=task_seed,
            keep_warm=keep_warm,
            **kwargs,
        )
        try:
            result = sim.do(
                max_steps=max_steps,
                tui=live_tui,
                real_time=real_time,
                on_frame=None if recorder is None else recorder.frame,
                on_buffer=None if recorder is None else recorder.buffer,
                on_policy_timing=None if recorder is None else recorder.policy_timing,
                count_holds=count_holds,
            )
            summary = {
                "benchmark": benchmark,
                "model": public_model(model),
                "task_suite": task_suite,
                "task_id": task_id,
                "done": result.done,
                "steps": result.steps,
                "policy_calls": result.policy_calls,
                "metrics": result.metrics,
            }
        finally:
            sim.close()
        if summary is not None:
            status = sim.release_status or "unknown"
            summary.update(session=status, keep_warm_s=keep_warm)
            summary["worker"] = {
                "parked": "warm_reserved", "parking": "warm_reservation_pending",
                "closed": "reservation_released",
            }.get(status, "release_unconfirmed")
        if recorder is not None:
            recorder.finish(summary=summary)
    except BaseException as exc:
        if recorder is not None:
            recorder.fail(exc, summary=summary)
        raise
    if result is None or summary is None:
        raise RuntimeError("sim finished without a result")
    verdict = "task complete" if result.done else "episode ended at step limit"
    on_line("")
    on_line(verdict)
    on_line(f"result: {'success condition reached' if result.done else 'not complete'}")
    on_line(f"steps: {result.steps}")
    on_line(f"policy calls: {result.policy_calls}")
    _print_sim_metrics_summary(result.metrics, on_line=on_line)
    on_line(f"session: {summary['session']}")
    if summary["session"] == "parked":
        on_line(f"compute: reserved for up to {keep_warm}s (billable)")
    elif summary["session"] == "parking":
        on_line(f"compute: keep-warm reservation pending (up to {keep_warm}s, billable)")
    elif summary["session"] == "closed":
        on_line("compute: released")
    else:
        on_line("compute: release unconfirmed; check dreamscale sessions list")
    if json_output:
        on_line(json.dumps(summary, sort_keys=True))
    return result


def _print_sim_run_card(*, max_steps: int, view: bool, tui: bool,
                        on_line: Callable[[str], None], model: str = MODEL_LIBERO,
                        benchmark: str = "libero", actions: bool = False) -> None:
    contract = _sim_contract(model)
    on_line("Dreamscale sim")
    label = BENCHMARK_LABELS[benchmark]
    on_line(f"mode: local {label}/MuJoCo physics + cloud {public_model(model)} policy")
    on_line(f"replay: off; {label} initial state only")
    on_line(f"viewer: {'on' if view else 'off'}")
    on_line(f"metrics: {'live terminal panel' if tui else 'summary only'}")
    on_line(
        f"action rate: {contract.action_hz:g} Hz; "
        f"chunk: {contract.horizon_s:.1f}s; "
        + ("replan: after full feedback; hold while inference is pending"
           if model in STATEFUL_MODELS
           else "replan: halfway")
    )
    on_line(f"max steps: {max_steps} policy actions; holds while inference is pending run "
            f"outside it" if actions else
            f"max steps: {max_steps} ({max_steps / contract.action_hz:.1f}s sim)")


def _print_sim_metrics_summary(metrics: dict[str, Any],
                               on_line: Callable[[str], None]) -> None:
    if not metrics:
        return
    rtt = metrics["rtt_ms"]
    inference = metrics["server_inference_ms"]
    buffer = metrics["action_buffer"]
    wait_ms_max = metrics.get("wait_ms_max")
    on_line(
        "rtt_ms send->chunk: "
        f"p50 {_fmt_ms(rtt['p50'])}, p95 {_fmt_ms(rtt['p95'])}, max {_fmt_ms(rtt['max'])}"
    )
    if inference["p50"] is not None:
        on_line(
            "worker inference_ms: "
            f"p50 {_fmt_ms(inference['p50'])}, p95 {_fmt_ms(inference['p95'])}"
        )
    on_line(
        "action buffer: "
        f"final {buffer['remaining']}/{buffer['capacity']} {buffer['health']}, "
        f"max wait {_fmt_ms(wait_ms_max)}"
    )
    realtime = metrics.get("realtime")
    if isinstance(realtime, dict):
        on_line(
            "real_time: "
            f"action {realtime['action_hz']} Hz, "
            f"sim {realtime['sim_time_s']:.1f}s, "
            f"wall {realtime['wall_time_s']:.1f}s, "
            f"factor {realtime['real_time_factor']:.2f}x, "
            f"deadline misses {realtime['deadline_miss_count']}, "
            f"underruns {realtime['action_underrun_count']}"
        )


def _dreamzero_observation(*, env: Any, obs: Any, session_id: str, observation_id: int,
                           action_index: int, cache_generation: int) -> Any:
    """Build the upstream_eval boundary observation for one replan epoch."""
    from dreamscale.dreamzero import observe

    observation = observe(
        **env.observation_inputs(obs), camera_capture_times_ns=(time.time_ns(),) * 3
    )
    return observation.to_wire_for_step(
        session_id=session_id,
        observation_id=observation_id,
        instruction=env.task_description,
        source_action_step=action_index - 1,
        next_action_step=action_index,
        control_tick=action_index,
        replan_epoch=action_index // DREAMZERO_REPLAN_STRIDE,
        cache_generation=cache_generation,
        sampling="upstream_eval",
    )


def _dreamzero_boundary_actions(chunk: Any, *, action_index: int,
                                cache_generation: int) -> list[tuple[float, ...]]:
    """Validate one upstream_eval reply; return the actions up to the next boundary."""
    from dreamscale.dreamzero import (
        DREAMZERO_DROID_LOOP_PROFILE,
        ChunkAlignment,
        _action,
        alignment_from_chunk,
    )

    expected = ChunkAlignment(
        source_action_step=action_index - 1,
        source_control_tick=action_index,
        replan_epoch=action_index // DREAMZERO_REPLAN_STRIDE,
        cache_generation=cache_generation,
    )
    if alignment_from_chunk(chunk) != expected:
        raise ValueError("DreamZero reply does not match its boundary observation")
    horizon = runtime_contract_for_model(MODEL_DREAMZERO_DROID).chunk_size
    if wire.chunk_action_indices(chunk) != list(range(horizon)):
        raise ValueError(f"DreamZero chunks must contain action indices 0 through {horizon - 1}")
    return [
        _action(values, DREAMZERO_DROID_LOOP_PROFILE)
        for values in wire.chunk_actions(chunk)[:DREAMZERO_REPLAN_STRIDE]
    ]


def _policy_preview_frame(env: SimEnvProtocol, obs: Any,
                          image_size: int = wire.LIBERO_POLICY_IMAGE_SIZE) -> np.ndarray:
    preview = getattr(env, "policy_preview_frame", None)
    if callable(preview):
        return preview(obs)
    agent = prepare_policy_image(env.agent_frame(obs), image_size)
    wrist = prepare_policy_image(env.wrist_frame(obs), image_size)
    return np.concatenate((agent, wrist), axis=1)


def _call_frame_callback(
    callback: Callable[..., None],
    frame: np.ndarray,
    step: int,
    metadata: dict[str, Any],
) -> None:
    if _frame_callback_accepts_metadata(callback):
        callback(frame, step, metadata)
        return
    callback(frame, step)


def _frame_callback_accepts_metadata(callback: Callable[..., None]) -> bool:
    try:
        parameters = inspect.signature(callback).parameters.values()
    except (TypeError, ValueError):
        return False
    positional = 0
    for parameter in parameters:
        if parameter.kind is inspect.Parameter.VAR_POSITIONAL:
            return True
        if parameter.kind in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        ):
            positional += 1
    return positional >= 3


def _elapsed_ms(start_ns: int, end_ns: int) -> float:
    return max(0.0, (end_ns - start_ns) / 1_000_000.0)


def _int_attr(obj: Any, name: str) -> int | None:
    value = getattr(obj, name, None)
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _duration_ms(start_ns: int | None, end_ns: int | None) -> float | None:
    if start_ns is None or end_ns is None or end_ns < start_ns:
        return None
    return (end_ns - start_ns) / 1_000_000.0


def _chunk_server_timings(chunk: Any) -> dict[str, float | None]:
    server_receive = _int_attr(chunk, "server_receive_time_ns")
    inference_start = _int_attr(chunk, "inference_start_time_ns")
    inference_end = _int_attr(chunk, "inference_end_time_ns")
    server_send = _int_attr(chunk, "server_send_time_ns")
    return {
        "server_queue_ms": _duration_ms(server_receive, inference_start),
        "server_inference_ms": _duration_ms(inference_start, inference_end),
        "server_total_ms": _duration_ms(server_receive, server_send),
    }


def _complete_policy_profile(*, profile: SimPolicyProfile, chunk: Any,
                             send_to_chunk_ms: float) -> None:
    server_timings = _chunk_server_timings(chunk)
    profile.completed = True
    profile.send_to_chunk_ms = send_to_chunk_ms
    profile.server_queue_ms = server_timings["server_queue_ms"]
    profile.server_inference_ms = server_timings["server_inference_ms"]
    profile.server_total_ms = server_timings["server_total_ms"]
    profile.runner_local_blocking_ms_total = (
        profile.env_step_ms_total
        + profile.preview_frame_ms_total
        + profile.frame_callback_ms_total
    )
    if profile.server_total_ms is not None:
        profile.client_overhead_ms = max(0.0, send_to_chunk_ms - profile.server_total_ms)
    if profile.client_overhead_ms is not None:
        known_client_overhead = (
            (profile.transport_send_ms or 0.0)
            + profile.runner_local_blocking_ms_total
        )
        profile.client_overhead_unattributed_ms = max(
            0.0,
            profile.client_overhead_ms - known_client_overhead,
        )


def _policy_timing_event(*, profile: SimPolicyProfile, policy_call: int,
                         step: int, sent_observation_id: int,
                         action_hz: int = LIBERO_ACTION_HZ,
                         chunk_size: int = CHUNK_SIZE) -> dict[str, Any]:
    return {
        "request_id": profile.request_id,
        "observation_id": sent_observation_id,
        "policy_call": policy_call,
        "step": step,
        "start_step": profile.start_step,
        "action_hz": action_hz,
        "action_dt_ms": 1000.0 / action_hz,
        "chunk_duration_s": chunk_size / action_hz,
        "replan_remaining": chunk_size // 2,
        "send_to_chunk_ms": profile.send_to_chunk_ms or 0.0,
        "server_queue_ms": profile.server_queue_ms,
        "server_inference_ms": profile.server_inference_ms,
        "server_total_ms": profile.server_total_ms,
        "client_overhead_ms": profile.client_overhead_ms,
        "client_overhead_unattributed_ms": profile.client_overhead_unattributed_ms,
        "transport_send_ms": profile.transport_send_ms,
        "wait_for_chunk_ms": profile.wait_for_chunk_ms,
        "chunk_ready_to_accept_ms": profile.chunk_ready_to_accept_ms,
        "obs_build_ms": profile.obs_build_ms,
        "policy_obs_build_ms": profile.obs_build_ms,
        "steps_during_request": profile.env_step_count,
        "env_step_count": profile.env_step_count,
        "env_step_ms_total": profile.env_step_ms_total,
        "env_step_ms_max": profile.env_step_ms_max,
        "runner_local_blocking_ms_total": profile.runner_local_blocking_ms_total,
        "preview_frame_count": profile.preview_frame_count,
        "preview_frame_ms_total": profile.preview_frame_ms_total,
        "preview_frame_ms_max": profile.preview_frame_ms_max,
        "preview_build_ms_total": profile.preview_frame_ms_total,
        "preview_build_ms_max": profile.preview_frame_ms_max,
        "frame_callback_count": profile.frame_callback_count,
        "frame_callback_ms_total": profile.frame_callback_ms_total,
        "frame_callback_ms_max": profile.frame_callback_ms_max,
    }


def _series(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {"last": None, "p50": None, "p95": None, "max": None}
    ordered = sorted(values)

    def percentile(percentile_value: float) -> float:
        index = round((percentile_value / 100.0) * (len(ordered) - 1))
        return ordered[min(len(ordered) - 1, max(0, index))]

    return {
        "last": values[-1],
        "p50": percentile(50.0),
        "p95": percentile(95.0),
        "max": max(values),
    }


def _profile_summary(
    profiles: list[SimPolicyProfile],
    *,
    env_reset_ms: float | None = None,
    preview_build_ms_values: list[float] | None = None,
    frame_callback_ms_values: list[float] | None = None,
    action_hz: int = LIBERO_ACTION_HZ,
    chunk_size: int = CHUNK_SIZE,
) -> dict[str, Any]:
    completed_profiles = [profile for profile in profiles if profile.completed]
    preview_build_ms_values = preview_build_ms_values or []
    frame_callback_ms_values = frame_callback_ms_values or []

    def values(attr: str, *, include_zero: bool = True) -> list[float]:
        output: list[float] = []
        for profile in completed_profiles:
            value = getattr(profile, attr)
            if value is None:
                continue
            numeric = float(value)
            if include_zero or numeric != 0.0:
                output.append(numeric)
        return output

    return {
        "policy_calls": len(completed_profiles),
        "action_hz": action_hz,
        "action_dt_ms": 1000.0 / action_hz,
        "chunk_duration_s": chunk_size / action_hz,
        "replan_remaining": max(1, chunk_size // 2),
        "env_reset_ms": env_reset_ms,
        "preview_frame_source_count": len(preview_build_ms_values),
        "preview_build_ms": _series(preview_build_ms_values),
        "frame_callback_ms": _series(frame_callback_ms_values),
        "send_to_chunk_ms": _series(values("send_to_chunk_ms")),
        "server_inference_ms": _series(values("server_inference_ms")),
        "server_total_ms": _series(values("server_total_ms")),
        "client_overhead_ms": _series(values("client_overhead_ms")),
        "client_overhead_unattributed_ms": _series(
            values("client_overhead_unattributed_ms")
        ),
        "transport_send_ms": _series(values("transport_send_ms")),
        "obs_build_ms": _series(values("obs_build_ms")),
        "policy_obs_build_ms": _series(values("obs_build_ms")),
        "wait_for_chunk_ms": _series(values("wait_for_chunk_ms")),
        "chunk_ready_to_accept_ms": _series(values("chunk_ready_to_accept_ms")),
        "steps_during_request": _series(values("env_step_count")),
        "env_step_ms_total": _series(values("env_step_ms_total")),
        "env_step_ms_max": _series(values("env_step_ms_max")),
        "runner_local_blocking_ms_total": _series(values("runner_local_blocking_ms_total")),
        "preview_frame_ms_total": _series(values("preview_frame_ms_total")),
        "preview_frame_ms_max": _series(values("preview_frame_ms_max")),
        "frame_callback_ms_total": _series(values("frame_callback_ms_total")),
        "frame_callback_ms_max": _series(values("frame_callback_ms_max")),
    }


def _render_preview_frame(frame: Any) -> None:
    import cv2

    _ensure_preview_window(cv2)
    cv2.imshow(PREVIEW_WINDOW_NAME, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    cv2.waitKey(1)


def _close_preview() -> None:
    global _preview_window_initialized
    import cv2

    try:
        cv2.destroyAllWindows()
    except cv2.error:
        pass
    finally:
        _preview_window_initialized = False


def _ensure_preview_window(cv2: Any) -> None:
    global _preview_window_initialized
    if _preview_window_initialized:
        return

    try:
        cv2.startWindowThread()
    except Exception:  # noqa: BLE001
        pass
    cv2.namedWindow(PREVIEW_WINDOW_NAME, cv2.WINDOW_AUTOSIZE)
    try:
        cv2.setWindowProperty(PREVIEW_WINDOW_NAME, cv2.WND_PROP_TOPMOST, 1)
    except Exception:  # noqa: BLE001
        pass
    _activate_preview_app()
    _preview_window_initialized = True


def _activate_preview_app() -> None:
    if sys.platform != "darwin":
        return
    try:
        import AppKit

        app = AppKit.NSRunningApplication.currentApplication()
        app.activateWithOptions_(AppKit.NSApplicationActivateIgnoringOtherApps)
    except Exception:  # noqa: BLE001
        pass
