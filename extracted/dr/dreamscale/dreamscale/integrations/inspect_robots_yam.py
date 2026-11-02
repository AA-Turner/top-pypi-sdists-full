"""A Dreamscale-configured YAM rig as an Inspect Robots embodiment: `--embodiment dreamscale_yam`.

The rig is the one `dreamscale robots yam setup` configured and `dreamscale run yam`
drives, with the same attended lifecycle: the CAN check and an Enter to start before
motors arm, homing before each trial, a measured-pose hold while the operator grades,
and a return home then a powered hold on exit. Every step goes through the rig's own
joint limits, tracking envelope and speed caps, paced at the models' 30 Hz.

    inspect-robots run --policy dreamscale -P model=pi0.5-bimanualyam \\
        --embodiment dreamscale_yam "fold the towel"
"""

from __future__ import annotations

import asyncio
import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

import numpy as np
from inspect_robots.embodiment import SELF_PACED, EmbodimentInfo
from inspect_robots.errors import EmbodimentFault
from inspect_robots.scene import Scene
from inspect_robots.spaces import (
    ActionSemantics,
    Box,
    CameraSpec,
    ObservationSpace,
    StateField,
    StateSpec,
)
from inspect_robots.types import Action, Observation, StepResult

from dreamscale.attended.lifecycle import AttendedLifecycle
from dreamscale.embodiments import YAM
from dreamscale.integrations.inspect_robots_policy import DEFAULT_CAMERAS, DIM_LABELS, STATE_KEY

NAME = "dreamscale_yam"
CONTROL_HZ = 30.0
# Nominal shape for the declaration; the rig's configured cameras set the real one.
_CAMERA_HEIGHT, _CAMERA_WIDTH = 360, 640
_START_PROMPT = "Enter to start · Ctrl+C to cancel: "
# Joint limits are known only once the arm drivers connect, after Inspect reads this
# declaration. Declare an envelope no YAM joint reaches (radians, grippers 0-1) and
# let the rig enforce each arm's driver-reported limits.
_GRIPPERS = (6, 13)
_LOW = np.array([0.0 if i in _GRIPPERS else -2 * np.pi for i in range(14)])
_HIGH = np.array([1.0 if i in _GRIPPERS else 2 * np.pi for i in range(14)])


def _rig_factory(config, *, max_joint_step, max_joint_velocity):
    from dreamscale.hardware.yam_rig import YamRig

    return YamRig(config, max_joint_step=max_joint_step, max_joint_velocity=max_joint_velocity)


def _load_config(path):
    from dreamscale.hardware.yam_can import resolve_arms
    from dreamscale.hardware.yam_config import load_config

    return resolve_arms(load_config(path).validate(complete=True))


def _preflight(config, print_fn):
    from dreamscale.hardware.yam_runner import check_can

    check_can(config, print_fn=print_fn)


class DreamscaleYam:
    """The bimanual YAM rig behind the Inspect Robots `Embodiment` contract.

    Nothing touches the hardware until the first trial: then the CAN check runs, the
    operator confirms, and the rig connects. Joint limits come from the arm drivers,
    so the declared bounds are a loose envelope and the rig enforces the real ones.
    """

    def __init__(
        self,
        config: str | Path | None = None,
        *,
        max_joint_step: float = YAM.max_joint_step,
        max_joint_velocity: float = YAM.max_joint_velocity,
        rig_factory: Callable[..., Any] = _rig_factory,
        load_config: Callable[[Any], Any] = _load_config,
        preflight: Callable[[Any, Callable[[str], None]], None] = _preflight,
        input_fn: Callable[[str], str] = input,
    ) -> None:
        if config is None:
            from dreamscale.hardware.yam_config import DEFAULT_CONFIG_PATH

            config = DEFAULT_CONFIG_PATH
        self.config_path = Path(config).expanduser()
        self.max_joint_step = float(max_joint_step)
        self.max_joint_velocity = float(max_joint_velocity)
        self._rig_factory = rig_factory
        self._load_config = load_config
        self._preflight = preflight
        self._input = input_fn
        self._session: Any | None = None
        self.rig: Any | None = None
        self.lifecycle: AttendedLifecycle | None = None
        self._dispatching = False
        self._homed = False
        self._next_tick: float | None = None
        self._period = 1.0 / CONTROL_HZ
        self.info = EmbodimentInfo(
            name=NAME,
            action_space=Box(
                shape=(14,),
                low=_LOW,
                high=_HIGH,
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
                    for name in DEFAULT_CAMERAS
                ),
                state_keys=frozenset({STATE_KEY}),
                state=StateSpec(
                    fields=(StateField(key=STATE_KEY, shape=(14,), unit="rad+normalized"),),
                ),
            ),
            control_hz=CONTROL_HZ,
            capabilities=frozenset({SELF_PACED}),
            docs="Dreamscale-configured bimanual YAM (dreamscale robots yam setup).",
        )

    def connect_operator_session(self, session: Any) -> None:
        """Inspect owns the terminal from here: write and prompt through its session."""
        self._session = session

    def _emit(self, message: str) -> None:
        try:
            if self._session is not None:
                self._session.write_line(message)
            else:
                print(message, file=sys.stderr, flush=True)
        except Exception:
            # Output failure must never bypass physical cleanup.
            pass

    def _confirm(self) -> None:
        self._emit("Arms will move. Clear the workspace; keep E-stop ready.")
        if self._session is not None:
            self._session.gate(_START_PROMPT, hint="the arms start moving after Enter")
            return
        try:
            choice = self._input(_START_PROMPT).strip().lower()
        except EOFError as exc:
            raise EmbodimentFault("no operator confirmation: stdin is closed") from exc
        if choice in {"cancel", "exit"}:
            raise KeyboardInterrupt

    def _connect(self) -> None:
        config = self._load_config(self.config_path)
        self._preflight(config, self._emit)
        self._confirm()
        rig = self._rig_factory(
            config, max_joint_step=self.max_joint_step,
            max_joint_velocity=self.max_joint_velocity,
        )
        lifecycle = AttendedLifecycle(rig, print_fn=self._emit, ready=False, arms="arms")
        self._emit("Connecting robot…")
        rig.open(attended=True)
        lifecycle.opened()
        self.rig, self.lifecycle = rig, lifecycle

    def _hold(self) -> dict[str, bool]:
        """Block dispatch and hold the measured pose; refuse to continue unconfirmed."""
        assert self.lifecycle is not None
        self._dispatching = False
        holds = self.lifecycle.stop_and_hold()
        if not holds or not all(holds.values()):
            raise EmbodimentFault("measured-pose hold unconfirmed; use the hardware E-stop")
        return holds

    def reset(self, scene: Scene, *, seed: int | None = None) -> Observation:
        if self.rig is None:
            self._connect()
        assert self.rig is not None and self.lifecycle is not None
        if self._dispatching:
            self._hold()
        if self.rig.faulted:
            raise EmbodimentFault("the rig faulted; reconnect it before another trial")
        if self._homed:
            if not asyncio.run(self.lifecycle.return_home()):
                raise EmbodimentFault("could not return home; check the arms, then rerun")
        else:
            asyncio.run(self.lifecycle.startup_home())
            self._homed = True
        self.lifecycle.task_started()
        self.rig.enable_dispatch()
        self._dispatching = True
        self._next_tick = None
        return self._observe()

    def step(self, action: Action) -> StepResult:
        if self.rig is None or not self._dispatching:
            raise EmbodimentFault("reset() must start a trial before step()")
        now = time.monotonic()
        if self._next_tick is not None and now < self._next_tick:
            time.sleep(self._next_tick - now)
        # Late ticks restart the schedule rather than bursting to catch up.
        self._next_tick = max(self._next_tick or now, time.monotonic()) + self._period
        result = self.rig.act(tuple(float(v) for v in np.asarray(action.data).reshape(-1)))
        accepted = getattr(result, "accepted_action", None)
        info = {} if accepted is None else {"accepted_action": list(accepted)}
        return StepResult(observation=self._observe(), info=info)

    def observe_parked(self) -> None:
        """Before grading: hold where the trial ended, as `dreamscale run yam` does."""
        if self._dispatching:
            self._hold()
        return None

    def close(self) -> None:
        """Hold, return home, then disconnect leaving the arms in a powered hold."""
        rig, lifecycle = self.rig, self.lifecycle
        if rig is None or lifecycle is None:
            return
        try:
            if self._dispatching:
                self._hold()
            asyncio.run(lifecycle.return_home())
        finally:
            self.rig = self.lifecycle = None
            self._emit("Disconnecting local hardware…")
            lifecycle.close()
            held = getattr(rig, "held_on_close", {})
            if held and all(held.values()):
                self._emit(YAM.held_message())
            else:
                self._emit("Disconnected.")

    def _observe(self) -> Observation:
        assert self.rig is not None
        observation = self.rig.observe()
        frames = (observation.top_frame, observation.left_frame, observation.right_frame)
        captures = observation.camera_capture_times_ns
        return Observation(
            images=dict(zip(DEFAULT_CAMERAS, frames, strict=True)),
            state={STATE_KEY: np.asarray(observation.hold_action, dtype=np.float64)},
            image_times=(
                {} if captures is None
                else {name: ns / 1e9 for name, ns in zip(DEFAULT_CAMERAS, captures, strict=True)}
            ),
            state_time=time.time(),
        )
