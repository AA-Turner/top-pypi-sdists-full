"""The SO-101 arm and its side and wrist cameras as an attended rig.

Cameras come from the rig file (camera_config) through the shared CameraReaders, as on
YAM and Franka. A custom robot without a rig file brings its own (capture_frames).

Units are lerobot's: five joints in calibrated degrees, then the gripper in 0-100.
The Feetech servos hold whatever goal they were last given, so stop() writes the
measured pose as the goal, and close() leaves torque on: the arm keeps holding
until `dreamscale robots so101 release`.
"""

from __future__ import annotations

import asyncio
import json
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

import numpy as np

from dreamscale import so101
from dreamscale.constants import (
    CAMERA_KEY_SO101_SIDE,
    CAMERA_KEY_SO101_WRIST,
    EXEC_HZ,
    JOINT_NAMES,
)
from dreamscale.hardware.rig import MeasuredState, RigFault
from dreamscale.motion.safety import clamp_step

from .camera_sources import CameraError, CameraReaders, lagging_latest, wait_for_frames
from .joint_rig import JointRig

ARM = "arm"
GRIPPER = len(JOINT_NAMES) - 1
GRIPPER_RANGE = (0.0, 100.0)
_ENCODER_MAX = 4095  # STS3215: 12-bit position, lerobot's max_res
# Each command moves at most this fast from the previous one (5° per tick at 30 Hz)
# and never leads the measured pose by more than DEFAULT_MAX_JOINT_STEP, so a blocked
# joint cannot wind up. A tight limit against the measured pose instead stalls the
# P-only servos under gravity.
DEFAULT_MAX_JOINT_VELOCITY = 150.0
DEFAULT_MAX_JOINT_STEP = 45.0


class So101TaskStopped(RigFault):
    pass


def calibrated_limits(calibration_path) -> np.ndarray:
    """Command range per value, [low, high]: each joint's calibrated travel in lerobot
    degrees (whose zero is the middle of that travel), then the gripper's 0-100."""
    limits = np.array([[-180.0, 180.0]] * GRIPPER + [list(GRIPPER_RANGE)])
    try:
        calibration = json.loads(Path(calibration_path).expanduser().read_text())
    except (OSError, ValueError):
        return limits
    for index, name in enumerate(JOINT_NAMES[:GRIPPER]):
        try:
            low, high = float(calibration[name]["range_min"]), float(calibration[name]["range_max"])
        except (KeyError, TypeError, ValueError):
            continue
        if high > low:
            mid = (low + high) / 2
            limits[index] = [(low - mid) * 360 / _ENCODER_MAX, (high - mid) * 360 / _ENCODER_MAX]
    return limits


class So101Rig(JointRig):
    """Rig callbacks over a lerobot SO-101 follower; see dreamscale.hardware.rig.Rig."""

    groups = (ARM,)
    value_labels = tuple(JOINT_NAMES)
    value_units = ("deg",) * GRIPPER + ("of 100",)
    control_period_s = 1 / EXEC_HZ
    stopped_error = So101TaskStopped
    limits_name = "calibrated range"
    action_description = "five joints in degrees, then the gripper"
    hold_unconfirmed = "Homing hold unconfirmed. Support the arm and switch it off."

    def __init__(
        self,
        robot_factory: Callable[[], Any],
        *,
        calibration_path,
        home: list[float] | None = None,
        max_joint_step: float | None = DEFAULT_MAX_JOINT_STEP,
        max_joint_velocity: float | None = DEFAULT_MAX_JOINT_VELOCITY,
        cameras: dict[str, Any] | None = None,
        camera_config=None,
        camera_roles: tuple[str, ...] = ("side", "wrist"),
        gripper_range: tuple[float, float] | None = None,
        readers_factory=CameraReaders,
        max_camera_age_s: float = 1.0,
        camera_ready_timeout_s: float = 8.0,
        retry_command: str = "dreamscale run so101",
        print_fn: Callable[[str], None] = print,
        clock: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], Any] = asyncio.sleep,
    ):
        super().__init__(
            max_joint_step=max_joint_step, max_joint_velocity=max_joint_velocity,
            unit="degrees", clock=clock,
        )
        self.robot_factory = robot_factory
        self.calibration_path = calibration_path
        self.home_pose = None if home is None else [float(v) for v in home]
        self.cameras = cameras or {}
        self.camera_config = camera_config
        if camera_roles not in (("side",), ("side", "wrist")):
            raise ValueError("SO-101 camera roles are side, with an optional wrist")
        self.camera_roles, self.gripper_range = camera_roles, gripper_range
        self.readers_factory, self.readers = readers_factory, None
        self.max_camera_age_s = max_camera_age_s
        self.camera_ready_timeout_s = camera_ready_timeout_s
        self.retry_command = retry_command
        self.print_fn = print_fn
        self.sleep = sleep
        self.robot = None
        self.limits = {ARM: calibrated_limits(calibration_path)}

    @property
    def has_home(self) -> bool:
        return self.home_pose is not None

    def open(self, *, attended=False):
        if not attended:
            raise RigFault("Attended consent required: connecting enables motor torque.")
        if self.robot is not None:
            raise RigFault("Rig already connected.")
        from dreamscale.homing import _open, _require_calibrated

        self.faulted = False
        self.held_on_close = {}
        if self.camera_config is not None:
            roles = {role: self.camera_config.roles[role] for role in self.camera_roles}
            self.readers = self.readers_factory(
                [self.camera_config.camera(role) for role in roles]
            )
            try:
                self.readers.open()
                wait_for_frames(self.readers, roles, timeout_s=self.camera_ready_timeout_s,
                                max_age_s=self.max_camera_age_s)
            except BaseException:
                self._close_readers()
                raise
        try:
            self.robot = _open(self.robot_factory, bus_only=False,
                               retry_command=self.retry_command)
        except BaseException:
            self._close_readers()
            raise
        try:
            _require_calibrated(self.robot)
            self.observe(None)
            if not self.stop().get(ARM):
                raise RigFault("Could not establish the measured-pose hold.")
            return self
        except BaseException:
            self.close()
            raise

    def _measured(self) -> np.ndarray:
        if self.robot is None:
            raise RigFault("Connect the arm before running.")
        position = np.asarray(self.robot.read_joint_positions(), dtype=float)
        if position.shape != (len(JOINT_NAMES),) or not np.isfinite(position).all():
            raise RigFault(f"The arm reported an unusable pose: {position.tolist()}")
        if self.on_state is not None:
            self.on_state(MeasuredState(tuple(position.tolist()), None, time.time()))
        return position

    def latest_frames(self) -> dict[str, np.ndarray]:
        if self.readers is None:
            frames = self.robot.capture_frames()
            keys = {"side": CAMERA_KEY_SO101_SIDE, "wrist": CAMERA_KEY_SO101_WRIST}
            return {role: frames[keys[role]] for role in self.camera_roles}
        frames = {}
        for role in self.camera_roles:
            try:
                frames[role] = lagging_latest(
                    self.readers, self.camera_config.roles[role],
                    warn_age_s=self.max_camera_age_s,
                    on_lag=lambda age_s, role=role: self._camera_lag(role, age_s),
                ).rgb
            except CameraError as exc:
                raise CameraError(f"{role.title()} camera: {exc}") from exc
        return frames

    def _close_readers(self):
        readers, self.readers = self.readers, None
        if readers is not None:
            readers.close()

    def observe(self, ctx=None):
        frames = self.latest_frames()
        with self._lock:
            position = self._measured()
        return so101.observation(
            side_frame=frames["side"],
            wrist_frame=frames.get("wrist"),
            views=len(self.camera_roles),
            gripper_range=self.gripper_range,
            joint_positions=position.tolist(),
            actions_remaining=getattr(ctx, "actions_remaining", 0),
        )

    def metadata(self) -> dict[str, Any]:
        cameras = dict(self.cameras)
        if self.camera_config is not None:
            cameras = {
                role: {"backend": c.backend, "width": c.width, "height": c.height, "fps": c.fps}
                for role in self.camera_roles for c in (self.camera_config.camera(role),)
            }
        return {
            "cameras": cameras,
            "home_pose": self.home_pose,
            "limits": self.limits[ARM].tolist(),
            "max_joint_step_deg": self.max_joint_step,
            "max_joint_velocity_deg_s": self.max_joint_velocity,
        }

    # -- JointRig hooks ------------------------------------------------------------------

    def _read(self):
        return {ARM: self._measured()}

    def _check_frames(self):
        if self.readers is not None:
            self.latest_frames()  # do not drain a model queue once a camera has stopped

    def _send(self, targets):
        self.robot.send_joint_targets(targets[ARM].tolist())
        return {ARM: targets[ARM]}

    def _hold(self):
        """Hold where the arm is now: goal = measured."""
        try:
            limits = self.limits[ARM]
            hold = np.clip(self._measured(), limits[:, 0], limits[:, 1])
            self.robot.send_joint_targets(hold.tolist())
            return {ARM: True}
        except Exception:
            return {ARM: False}

    async def _home(self):
        """Ramp every joint to home at the homing speed, then hold there.

        Returns the largest measured joint offset from home, in degrees. Without a
        home pose the arm only holds where it is. Never crosses the wrist_roll seam:
        a wrist on the far side of it stays where it is.
        """
        from dreamscale.homing import (
            HOME_LAG_LIMIT_DEG,
            HOME_SETTLE_S,
            HOME_STEP_DEG,
            HOME_TOLERANCE_DEG,
            WRIST_ROLL,
            _crosses_wrist_seam,
        )

        with self._lock:
            start = self._measured()
        target = list(self.home_pose)
        if _crosses_wrist_seam(float(start[WRIST_ROLL]), target):
            target[WRIST_ROLL] = float(start[WRIST_ROLL])
            self.print_fn(
                "Leaving the wrist where it is: turning it home would cross its encoder "
                "seam. Turn it by hand once the motors are released."
            )
        target = self.validate_action(target, check_step=False, saturate=True)[ARM].tolist()
        self._homing = True
        self._dispatch.set()
        period = 1.0 / EXEC_HZ
        clock, sleep = self.clock, self.sleep
        deadline = clock()
        setpoint = start.tolist()
        settle = round(HOME_SETTLE_S * EXEC_HZ)
        while settle > 0:
            if not self._dispatch.is_set() or self.faulted:
                raise So101TaskStopped("Homing stopped.")
            with self._lock:
                measured = self._measured()
                lag = np.abs(measured - np.asarray(setpoint))
                joint = int(np.argmax(lag))
                if lag[joint] > HOME_LAG_LIMIT_DEG:
                    raise RigFault(
                        f"{JOINT_NAMES[joint]} stopped following at {measured[joint]:+.0f}° "
                        f"({lag[joint]:.0f}° behind); something is blocking it or it cut "
                        "its torque."
                    )
                if max(abs(t - s) for s, t in zip(setpoint, target, strict=True)) > 1e-6:
                    setpoint = clamp_step(setpoint, target, HOME_STEP_DEG)
                else:
                    settle -= 1
                self.robot.send_joint_targets(setpoint)
            # One step per period. A late tick resets the schedule instead of
            # catching up, which would send steps faster than the homing speed.
            deadline += period
            wait = deadline - clock()
            if wait > 0:
                await sleep(wait)
            else:
                deadline -= wait
                await sleep(0)
        with self._lock:
            offset = np.abs(self._measured() - np.asarray(target))
        joint = int(np.argmax(offset))
        if offset[joint] > HOME_TOLERANCE_DEG:
            raise RigFault(f"Home not reached: {JOINT_NAMES[joint]} is "
                           f"{offset[joint]:.0f}° from home.")
        return float(offset.max())

    def close(self):
        """Disconnect, leaving torque on so the arm keeps holding its last pose."""
        self.block_dispatch()
        with self._lock:
            self._close_readers()
            robot, self.robot = self.robot, None
            if robot is None:
                return
            held = False
            try:
                if not self.faulted:
                    hold = np.clip(
                        np.asarray(robot.read_joint_positions(), dtype=float),
                        self.limits[ARM][:, 0], self.limits[ARM][:, 1],
                    )
                    robot.send_joint_targets(hold.tolist())
                    held = True
            except Exception:
                held = False
            finally:
                try:
                    robot.disconnect(release_torque=False)
                except Exception as exc:
                    self.held_on_close = {ARM: False}
                    raise RigFault(f"Arm disconnect unconfirmed: {exc}") from exc
            self.held_on_close = {ARM: held}
