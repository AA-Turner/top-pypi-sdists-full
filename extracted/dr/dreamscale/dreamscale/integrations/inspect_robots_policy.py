"""Dreamscale models as an Inspect Robots policy: `--policy dreamscale`.

Inspect Robots owns the rollout: each `act()` returns the one action to execute on
this control tick, and the embodiment paces itself at the model's rate. Dreamscale's
action controller does the rest exactly as in `policy.run()`: it requests chunks
ahead of need, merges them, and holds position on an underrun.

    inspect-robots run --policy dreamscale -P model=molmoact2-bimanual-yam \\
        --embodiment yam_arms -E control_hz=30 "fold the towel"
"""

from __future__ import annotations

import atexit
import math
import threading
import time
from collections.abc import Callable, Mapping
from typing import Any

import numpy as np
from dreamscale_transport import catalog
from inspect_robots.policy import PolicyConfig, PolicyInfo
from inspect_robots.scene import Scene
from inspect_robots.spaces import (
    ActionSemantics,
    Box,
    CameraSpec,
    ObservationSpace,
    StateField,
    StateSpec,
)
from inspect_robots.types import Action, ActionChunk, Observation

from dreamscale import errors, yam
from dreamscale.constants import MODEL_BIMANUAL_YAM
from dreamscale.model_names import internal_model, public_model
from dreamscale.policy.run_loop import AsyncActionController, _hold_position_action
from dreamscale.policy.runtime.contract import runtime_contract_for_model
from dreamscale.policy.types import ActResult, RunStrategy

NAME = "dreamscale"
# Bimanual YAM models with 14-D absolute joint actions: left 6 joints + gripper, then right
# (the catalog's ``client.inspect_joint_view``, in the YAM robot's order).
YAM_JOINT_MODELS = tuple(
    model for model in catalog.robot_models("yam")
    if catalog.entry(model).client.inspect_joint_view
)
DEFAULT_CAMERAS = ("top_cam", "left_cam", "right_cam")
STATE_KEY = "joint_pos"
VELOCITY_KEY = "joint_vel"
DIM_LABELS = tuple(
    f"{side}_{part}"
    for side in ("left", "right")
    for part in (*(f"j{i}" for i in range(6)), "gripper")
)
# Nominal camera shape for the declaration only: compatibility checks camera names,
# and the session resizes frames to what its checkpoint was trained on.
_CAMERA_HEIGHT, _CAMERA_WIDTH = 360, 640


def _connect(model: str, **kwargs: Any) -> Any:
    # The raw session (no idle release or transparent reopen): the eval loop owns timing.
    from dreamscale.policy.remote import connect

    return connect(model, **kwargs)


class DreamscalePolicy:
    """A Dreamscale cloud model behind the Inspect Robots `Policy` contract.

    Construct-time options mirror `dreamscale run yam`. The cloud session starts on the
    first `reset()`, is reused across trials, and is released when the process exits;
    with `keep_warm` > 0 it stays reserved (and billed) that long for the next run.
    """

    def __init__(
        self,
        model: str = MODEL_BIMANUAL_YAM,
        *,
        region: str = "available",
        provider: str | None = None,
        speed: str | None = None,
        rtc: str = "auto",
        checkpoint: str | None = None,
        context: str = "auto",
        keep_warm: int = 300,
        cameras: tuple[str, ...] | list[str] | str = DEFAULT_CAMERAS,
        state_key: str = STATE_KEY,
        timeout_s: float = 60.0,
        connect: Callable[..., Any] = _connect,
    ) -> None:
        model = internal_model(model)
        if model not in YAM_JOINT_MODELS:
            raise ValueError(
                f"model {public_model(model)!r} is not available through Inspect Robots. "
                f"{errors.SEE_MODELS}"
            )
        if isinstance(cameras, str):
            cameras = tuple(name.strip() for name in cameras.split(",") if name.strip())
        cameras = tuple(cameras)
        if len(cameras) != 3:
            raise ValueError("cameras must name the top, left wrist and right wrist cameras")
        if type(keep_warm) is not int or not 0 <= keep_warm <= 3600:
            raise ValueError("keep_warm must be 0–3600 seconds")
        self.model = model
        self.contract = runtime_contract_for_model(model)
        self.cameras = cameras
        self.state_key = state_key
        self.timeout_s = float(timeout_s)
        self.keep_warm = keep_warm
        self._connect_kwargs: dict[str, Any] = {
            "region": region,
            "rtc": rtc,
            "keep_warm": keep_warm,
            "control_hz": int(self.contract.action_hz),
            "on_progress": self._on_progress,
            **({"provider": provider} if provider is not None else {}),
            **({"speed": speed} if speed is not None else {}),
            **({"checkpoint": checkpoint} if checkpoint is not None else {}),
            **({"context": context} if context != "auto" else {}),
        }
        self._connect_fn = connect
        self._printer: Any | None = None
        self._remote: Any | None = None
        self._episode: _Episode | None = None
        self._lock = threading.Lock()
        self._closed = False
        self.info = PolicyInfo(
            name=NAME,
            action_space=Box(
                shape=(14,),
                semantics=ActionSemantics(
                    control_mode="joint_pos",
                    rotation_repr="none",
                    gripper="continuous",
                    frame="base",
                    dim_labels=DIM_LABELS,
                ),
            ),
            observation_space=ObservationSpace(
                cameras=tuple(
                    CameraSpec(name=name, height=_CAMERA_HEIGHT, width=_CAMERA_WIDTH)
                    for name in cameras
                ),
                state_keys=frozenset({state_key}),
                state=StateSpec(
                    fields=(StateField(key=state_key, shape=(14,), unit="rad+normalized"),),
                ),
            ),
            control_hz=self.contract.action_hz,
            checkpoint=checkpoint or model,
        )
        # One action per act(): the action controller, not Inspect's, buffers chunks.
        self.config = PolicyConfig(action_horizon=1, replan_interval=1)
        # Inspect never closes a policy, so process exit is the normal release path.
        # Threading's exit hooks run while the network still works; atexit is the fallback.
        register = getattr(threading, "_register_atexit", None)
        if register is not None:
            try:
                register(self.close)
            except RuntimeError:
                pass
        atexit.register(self.close)

    @property
    def session_id(self) -> str | None:
        return None if self._remote is None else str(self._remote.session_id)

    def bind(self, embodiment_info: Any) -> None:
        """Refuse an embodiment stepping at another rate: every act() is one model tick."""
        hz = getattr(embodiment_info, "control_hz", None)
        if hz is None or not math.isclose(float(hz), self.contract.action_hz, abs_tol=1e-6):
            raise ValueError(
                f"{public_model(self.model)} runs at {self.contract.action_hz:g} Hz but the "
                f"embodiment steps at {hz} Hz; set the embodiment's rate to match (yam_arms: "
                f"-E control_hz={self.contract.action_hz:g})"
            )

    def reset(self, scene: Scene) -> None:
        instruction = (scene.instruction or "").strip()
        if not instruction:
            raise ValueError("the scene has no instruction for the model")
        with self._lock:
            self._end_episode()
            remote = self._ensure_connected()
            if getattr(remote._async_policy, "requires_task_preparation", False):
                remote.prepare(instruction=instruction)
            self._episode = _Episode(remote, instruction, self.contract, self.timeout_s)

    def act(self, observation: Observation) -> ActionChunk:
        started = time.perf_counter()
        with self._lock:
            episode = self._episode
            if episode is None:
                raise RuntimeError("reset() must start an episode before act()")
            converted = to_yam_observation(
                observation, cameras=self.cameras, state_key=self.state_key,
                actions_remaining=episode.actions_remaining,
            )
            action, stalled = episode.step(converted)
        return ActionChunk(
            actions=[Action(
                data=np.asarray(action, dtype=np.float64),
                meta={"dreamscale_hold": stalled},
            )],
            control_hz=self.contract.action_hz,
            inference_latency_s=time.perf_counter() - started,
        )

    def on_trial_end(self, record: Any, log_dir: str, run_id: str) -> None:
        with self._lock:
            summary = self._end_episode()
        if summary is not None:
            record.metadata[NAME] = summary

    def close(self) -> None:
        """End the episode and release the session (parked warm when keep_warm > 0)."""
        with self._lock:
            if self._closed:
                return
            self._closed = True
            try:
                self._end_episode()
            finally:
                remote, self._remote = self._remote, None
                try:
                    if remote is not None:
                        remote.close()
                        self._on_progress(
                            "Cloud task closed"
                            + (f"; reserved for {self.keep_warm}s." if self.keep_warm
                               else "; stopped.")
                        )
                finally:
                    printer, self._printer = self._printer, None
                    if printer is not None:
                        printer.close()

    def _ensure_connected(self) -> Any:
        if self._closed:
            raise RuntimeError("this policy is closed")
        if self._remote is None:
            if self._printer is None:
                from dreamscale.attended.output import ProgressPrinter

                # The same live compute progress as `dreamscale run yam`; details go to
                # ~/.dreamscale/logs/yam.
                self._printer = ProgressPrinter(robot="yam")
            self._remote = self._connect_fn(self.model, **self._connect_kwargs)
            # Inspect Robots owns the terminal while trials run: log only from here.
            self._printer.mute()
        return self._remote

    def _on_progress(self, message: str) -> None:
        printer = self._printer
        if printer is not None:
            printer(message)

    def _end_episode(self) -> dict[str, Any] | None:
        episode, self._episode = self._episode, None
        if episode is None:
            return None
        summary = episode.close()
        remote = self._remote
        return {
            **summary,
            "model": self.model,
            "session_id": None if remote is None else str(remote.session_id),
            "region": getattr(remote, "region", None),
            "transport_mode": getattr(remote, "transport_mode", None),
        }


class _Episode:
    """One trial's action controller, stepped once per control tick.

    The per-tick contract of `RemotePolicy.run()` in real time: never wait for a
    chunk mid-episode, hold the measured pose on an underrun, and record what was
    sent so action history and smoothing see the executed trajectory.
    """

    def __init__(self, remote: Any, instruction: str, contract: Any, timeout_s: float) -> None:
        self._remote = remote
        self._instruction = instruction
        self._contract = contract
        self._timeout_s = timeout_s
        self._controller = AsyncActionController(
            policy=remote._async_policy,
            strategy=RunStrategy(
                action_hz=contract.action_hz,
                chunk_size=contract.execution_chunk_size,
                timeout_s=timeout_s,
            ),
        )
        self._tick = 0
        self._hold: tuple[float, ...] | None = None
        self._chunks_start = remote.runtime_stats.chunks_received
        self._underruns_start = remote.runtime_stats.underruns
        self.startup_holds = self.execution_underruns = 0
        self._moving = False

    @property
    def actions_remaining(self) -> int:
        return self._controller.actions_remaining

    def _run(self, coro: Any) -> Any:
        return self._remote._runner.run(coro)

    def step(self, observation: Any) -> tuple[tuple[float, ...], bool]:
        if self._tick == 0:
            bootstrap = self._contract.measured_bootstrap
            self._run(self._controller.prepare(
                observation, instruction=self._instruction, timeout_s=self._timeout_s,
                wait_for_chunk=bootstrap,
            ))
            if bootstrap:
                anchor = _hold_position_action(
                    contract=self._contract, observation=observation, last_action=None,
                )
                self._run(self._controller.seed_initial_position(anchor))
        step = self._run(self._controller.step(
            observation, instruction=self._instruction, timeout_s=self._timeout_s,
            action_index=self._tick, wait_for_chunk=False,
        ))
        self._tick += 1
        action = step.action
        if step.stalled:
            if self._moving:
                self.execution_underruns += 1
            else:
                self.startup_holds += 1
            if self._hold is None:
                self._hold = step.action
            action = self._hold
            self._run(self._controller.record_act_result(
                step.action, ActResult(accepted_action=action),
            ))
        else:
            self._hold = None
            self._moving = True
        self._run(self._controller.record_act_result(action, None))
        return action, step.stalled

    def close(self) -> dict[str, Any]:
        self._remote._runner.run_cleanup(self._controller.close())
        stats = self._remote.runtime_stats
        return {
            "actions": self._tick,
            "policy_calls": stats.chunks_received - self._chunks_start,
            "underruns": stats.underruns - self._underruns_start,
            "startup_holds": self.startup_holds,
            "execution_underruns": self.execution_underruns,
        }


def to_yam_observation(
    observation: Observation,
    *,
    cameras: tuple[str, ...] = DEFAULT_CAMERAS,
    state_key: str = STATE_KEY,
    actions_remaining: int = 0,
) -> yam.YamObservation:
    """An Inspect Robots bimanual YAM observation as the SDK's typed YAM observation."""
    frames = []
    for name in cameras:
        frame = observation.images.get(name)
        if frame is None:
            raise ValueError(
                f"observation has no {name!r} camera; it provides {sorted(observation.images)}"
            )
        frames.append(np.ascontiguousarray(frame))
    state = observation.state.get(state_key)
    if state is None:
        raise ValueError(f"observation has no {state_key!r} state")
    joints = np.asarray(state, dtype=np.float64).reshape(-1)
    if joints.shape != (14,):
        raise ValueError(f"{state_key!r} must hold 14 values, got shape {joints.shape}")
    velocity = observation.state.get(VELOCITY_KEY)
    velocities = (
        np.zeros(14) if velocity is None else np.asarray(velocity, dtype=np.float64).reshape(-1)
    )
    if velocities.shape != (14,):
        velocities = np.zeros(14)
    # Grippers are normalized (1 = open); encoder noise can read a hair outside [0, 1].
    return yam.observation(
        top_frame=frames[0], left_frame=frames[1], right_frame=frames[2],
        left_joint_positions=joints[0:6], left_gripper=float(np.clip(joints[6], 0.0, 1.0)),
        right_joint_positions=joints[7:13], right_gripper=float(np.clip(joints[13], 0.0, 1.0)),
        left_joint_velocities=velocities[0:6], right_joint_velocities=velocities[7:13],
        actions_remaining=actions_remaining,
        camera_capture_times_ns=_capture_times_ns(observation.image_times, cameras),
    )


def _capture_times_ns(
    image_times: Mapping[str, float], cameras: tuple[str, ...]
) -> tuple[int, int, int] | None:
    """Capture stamps as Unix nanoseconds, when the embodiment supplies all three.

    Inspect Robots leaves the clock unspecified, so stamps that are not recent Unix
    seconds (a monotonic clock, say) are dropped rather than sent as stale captures.
    """
    try:
        seconds = [float(image_times[name]) for name in cameras]
    except (KeyError, TypeError, ValueError):
        return None
    now = time.time()
    if not all(math.isfinite(s) and abs(now - s) < 60.0 for s in seconds):
        return None
    return tuple(int(s * 1e9) for s in seconds)  # type: ignore[return-value]
