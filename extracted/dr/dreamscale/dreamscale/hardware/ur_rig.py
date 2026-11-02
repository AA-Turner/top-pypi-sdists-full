"""The Universal Robots rig: one arm, a Robotiq gripper, and a scene and a wrist camera.

Actions are 7 values: six absolute joint positions in radians, then the gripper from 0
(open) to 1 (closed). Observations carry the cameras under the names a LeRobot dataset
recorded on this rig uses, so its π0.5 deployment reads them as trained.
"""

from __future__ import annotations

import asyncio
import time

import numpy as np

from dreamscale import robot
from dreamscale.embodiments import UR
from dreamscale.hardware.rig import MeasuredState

from .camera_sources import CameraError, CameraReaders, lagging_latest, wait_for_frames
from .joint_rig import JointRig
from .robotiq import RobotiqGripper
from .ur_arm import MOVE_POLL_S, URArm, URArmError, arm_spec, speed_scale
from .ur_config import URConfig

ARM = "arm"
# The wire name of each camera role: the LeRobot feature a recording on this rig uses.
CAMERA_KEYS = dict(zip(UR.camera_roles, UR.recording_keys, strict=True))
HOME_TOLERANCE = 0.02
HOME_SETTLED = 0.05
# A 2F-85 fully open reads about 3 of 255.
GRIPPER_OPEN = 0.05
GRIPPER_OPEN_TIMEOUT_S = 3.0
GRIPPER_LIMITS = np.array([[0.0, 1.0]])


class URRigError(URArmError):
    """The rig refused a command or could not confirm its hold."""


class URTaskStopped(URRigError):
    """Intentional dispatch cancellation; healthy hardware can serve another task."""


class NoGripper:
    def open(self):
        return self

    def state(self) -> float:
        return 0.0

    def command(self, value: float) -> None:
        pass

    def close(self) -> None:
        pass


def make_gripper(gripper_type: str, host: str):
    if gripper_type == "none":
        return NoGripper()
    return RobotiqGripper(host, folds=gripper_type == "robotiq_2f85")


class URRig(JointRig):
    """policy.run callbacks for one UR arm; explicit attended open is the motor boundary."""

    groups = (ARM,)
    value_labels = (*(f"joint {i}" for i in range(1, 7)), "gripper")
    value_units = ("rad",) * 6 + ("normalized",)
    control_period_s = 1 / 20
    fault_error = URRigError
    stopped_error = URTaskStopped
    limits_name = "arm's joint limits"
    action_description = "six joint positions in radians, then the gripper from 0 to 1"
    hold_unconfirmed = "Homing hold unconfirmed. Use the E-stop."

    def __init__(
        self,
        config: URConfig,
        *,
        roles: tuple[str, ...],
        chunk_size: int | None = None,
        readers_factory=CameraReaders,
        arm_factory=None,
        gripper_factory=None,
        max_joint_step=None,
        max_joint_velocity=None,
        max_state_age_s=0.25,
        max_camera_age_s=1.0,
        camera_ready_timeout_s=8.0,
    ):
        super().__init__(
            max_joint_step=max_joint_step, max_joint_velocity=max_joint_velocity,
            unit="radians",
        )
        self.config = config.validate(complete=True)
        # No roles: an arm-only rig (homing), which never opens cameras.
        if not set(roles) <= set(config.roles):
            raise ValueError("Each camera role must be mapped in the rig.")
        self.roles, self.chunk_size = tuple(roles), chunk_size
        self.readers_factory = readers_factory
        arm = config.arm
        # The caps are a UR7e's; a longer arm's shrink so its tool moves no faster.
        self.max_speed, self.scale = np.array(arm_spec(arm.model).max_speed), speed_scale(arm.model)
        self.arm_factory = arm_factory or (lambda: URArm(arm.host, arm.model, program=arm.program))
        self.gripper_factory = gripper_factory or (
            lambda: make_gripper(config.gripper.type, arm.host)
        )
        self.max_state_age_s, self.max_camera_age_s = max_state_age_s, max_camera_age_s
        self.camera_ready_timeout_s = camera_ready_timeout_s
        self.arm = self.gripper = self.readers = None

    # -- lifecycle ---------------------------------------------------------------------

    def open(self, *, attended=False, cameras=True):
        if not attended:
            raise URRigError("Attended consent required: connecting takes control of the arm.")
        if self.arm is not None or self.readers is not None:
            raise URRigError("Rig already connected.")
        try:
            self.faulted, self.held_on_close = False, {}
            if cameras and not self.roles:
                raise URRigError("This rig was made without cameras.")
            if cameras:
                self.readers = self.readers_factory(
                    [self.config.camera(role) for role in self.roles]
                )
                self.readers.open()
                wait_for_frames(
                    self.readers, self._camera_ids(), timeout_s=self.camera_ready_timeout_s,
                    max_age_s=self.max_camera_age_s,
                )
            self.arm = self.arm_factory().connect()
            self.gripper = self.gripper_factory().open()
            self.limits = {
                ARM: np.vstack([np.asarray(self.arm.limits, dtype=float), GRIPPER_LIMITS]),
            }
            if cameras:
                self.observe(None)
            else:
                self._state()
            self.stop()
            if not all(self.last_hold.values()):
                raise URRigError("Could not confirm the arm is holding still.")
            return self
        except BaseException:
            self.close()
            raise

    def close(self):
        self.block_dispatch()
        errors = []
        with self._lock:
            holding = False
            if self.arm is not None and not self.faulted:
                try:
                    state = self.arm.snapshot()
                    holding = state.safety_mode in (1, 2) and state.robot_mode == 7
                except Exception:
                    holding = False
            for name in ("gripper", "arm"):
                device = getattr(self, name)
                if device is None:
                    continue
                try:
                    device.close()
                except BaseException as exc:
                    errors.append(f"{name}: {exc}")
                setattr(self, name, None)
            # A powered UR keeps its pose with brakes released once the program stops.
            self.held_on_close = {ARM: holding and not errors}
            if self.readers is not None:
                try:
                    self.readers.close()
                except BaseException as exc:
                    errors.append(f"cameras: {exc}")
                self.readers = None
        if errors:
            raise URRigError("Disconnect unconfirmed; keep E-stop ready. " + "; ".join(errors))

    # -- reads -------------------------------------------------------------------------

    def _camera_ids(self):
        return {role: self.config.roles[role] for role in self.roles}

    def _state(self):
        if self.arm is None or self.gripper is None:
            raise URRigError("Connect the rig before running.")
        state = self.arm.snapshot().validate(self.max_state_age_s)
        gripper = min(1.0, max(0.0, float(self.gripper.state())))
        if self.on_state is not None:
            self.on_state(MeasuredState(
                position=(*state.position.tolist(), gripper),
                velocity=(*state.velocity.tolist(), 0.0),
                capture_unix_s=time.time(),
            ))
        return state, gripper

    def _frames(self):
        if self.readers is None:
            raise CameraError("Cameras disconnected.")
        frames = {}
        for role, camera_id in self._camera_ids().items():
            try:
                frames[role] = lagging_latest(
                    self.readers, camera_id, warn_age_s=self.max_camera_age_s,
                    on_lag=lambda age_s, role=role: self._camera_lag(role, age_s),
                )
            except CameraError as exc:
                raise CameraError(f"{role.title()} camera: {exc}") from exc
        return frames

    def metadata(self):
        config = self.config
        return {
            "arm": {"model": config.arm.model},
            "gripper": {"type": config.gripper.type},
            "cameras": {
                role: {"backend": c.backend, "width": c.width, "height": c.height, "fps": c.fps}
                for role in self.roles
                for c in (config.camera(role),)
            },
            "home_pose": list(config.home_pose) if config.home_pose is not None else None,
        }

    def latest_frames(self):
        return {role: frame.rgb for role, frame in self._frames().items()}

    def observe(self, ctx=None):
        with self._lock:
            (state, gripper), frames = self._state(), self._frames()
            return robot.observation(
                cameras={CAMERA_KEYS[role]: frames[role].rgb for role in self.roles},
                state=[*state.position.tolist(), gripper],
                actions_remaining=getattr(ctx, "actions_remaining", 0),
            )

    # -- JointRig hooks ----------------------------------------------------------------

    def _read(self):
        state, gripper = self._state()
        return {ARM: np.array([*state.position, gripper])}

    def _ready(self):
        if self._homing:
            self._state()
        else:
            self.observe(None)

    def _check_frames(self):
        self._frames()

    def _velocity_caps(self, group):
        if self.max_joint_velocity is None:
            return None
        return np.array([*np.minimum(self.max_joint_velocity * self.scale, self.max_speed), np.inf])

    def _tracking(self, group):
        if self.max_joint_step is None:
            return None
        return np.array([self.max_joint_step * self.scale] * 6 + [np.inf])

    def _send(self, targets):
        target = targets[ARM]
        sent = np.asarray(self.arm.follow(target[:6]), dtype=float)
        self.gripper.command(float(target[6]))
        return {ARM: np.array([*sent, target[6]])}

    def _hold(self):
        return {ARM: self.arm is not None and bool(self.arm.hold())}

    async def _open_gripper(self, sleep) -> None:
        self.gripper.command(0.0)
        deadline = time.monotonic() + GRIPPER_OPEN_TIMEOUT_S
        while self._state()[1] > GRIPPER_OPEN:
            if time.monotonic() > deadline:
                raise URRigError("The gripper didn't open. Check that nothing blocks it.")
            await sleep(MOVE_POLL_S)

    @property
    def has_home(self) -> bool:
        return self.config.home_pose is not None

    async def _home(self, *, sleep=asyncio.sleep):
        """Open the gripper and move slowly to the home pose. With no home pose nothing
        moves; already at home, only the gripper opens."""
        if self.config.home_pose is None:
            return None
        home = np.asarray(self.config.home_pose, dtype=float)
        self.validate_action([*home, 0.0], check_step=False)
        self._homing = True
        self.enable_dispatch()
        # Every run starts with the gripper open, even with the arm already home: activating
        # the 2F-85 at connect leaves its fingers closed.
        await self._open_gripper(sleep)
        state, _ = self._state()
        offset = float(np.max(np.abs(state.position - home)))
        if offset <= HOME_TOLERANCE:
            return offset
        self.arm.start_move(home)
        try:
            while self.arm.moving():
                await sleep(MOVE_POLL_S)
        except BaseException:
            # Ctrl+C, a cancelled task or a fault: decelerate rather than finish the move.
            self.arm.stop_move()
            raise
        state, _ = self._state()
        offset = float(np.max(np.abs(state.position - home)))
        if offset > HOME_SETTLED:
            raise URRigError(
                f"Homing ended {offset:.4f} rad from home. Check for an obstruction."
            )
        return offset
