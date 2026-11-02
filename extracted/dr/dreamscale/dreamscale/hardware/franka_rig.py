"""The Franka rig: one arm, one gripper and the cameras a model's roles need.

Actions are 8 values: seven absolute joint positions in radians, then the gripper from 0
(open) to 1 (closed). Every command passes the shared JointRig limits before franky's
own 1 kHz velocity, acceleration and jerk limits.
"""

from __future__ import annotations

import asyncio
import time

import numpy as np

from dreamscale import franka
from dreamscale.hardware.rig import MeasuredState

from .camera_sources import CameraError, CameraReaders, lagging_latest, wait_for_frames
from .franka_arm import FrankaArmError, FrankyArm
from .franka_config import FrankaConfig
from .franka_gripper import make_gripper
from .joint_rig import JointRig

ARM = "arm"
# Joints within this many radians of home are already home.
HOME_TOLERANCE = 0.02
# Home needs the arm to settle this close, once franky's move returns.
HOME_SETTLED = 0.05
GRIPPER_LIMITS = np.array([[0.0, 1.0]])


class FrankaRigError(FrankaArmError):
    """The rig refused a command or could not confirm its hold."""


class FrankaTaskStopped(FrankaRigError):
    """Intentional dispatch cancellation; healthy hardware can serve another task."""


class FrankaRig(JointRig):
    """policy.run callbacks for one Franka; explicit attended open is the motor boundary.

    roles are the camera roles this run uses, in wire order. chunk_size is the model's,
    carried on every observation.
    """

    groups = (ARM,)
    value_labels = (*(f"joint {i}" for i in range(1, 8)), "gripper")
    value_units = ("rad",) * 7 + ("normalized",)
    control_period_s = 1 / 15
    fault_error = FrankaRigError
    stopped_error = FrankaTaskStopped
    limits_name = "arm's joint limits"
    action_description = "seven joint positions in radians, then the gripper from 0 to 1"
    hold_unconfirmed = "Homing hold unconfirmed. Use the E-stop."

    def __init__(
        self,
        config: FrankaConfig,
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
        if "exterior_1" not in roles or "wrist" not in roles or not set(roles) <= set(config.roles):
            raise ValueError("Roles must include exterior_1 and wrist, each mapped in the rig.")
        if any(not np.isfinite(v) or v <= 0
               for v in (max_state_age_s, max_camera_age_s, camera_ready_timeout_s)):
            raise ValueError("Freshness limits must be positive finite seconds.")
        self.roles, self.chunk_size = tuple(roles), chunk_size
        self.readers_factory = readers_factory
        arm = config.arm
        self.arm_factory = arm_factory or (lambda: FrankyArm(arm.host, arm.model))
        self.gripper_factory = gripper_factory or (
            lambda: make_gripper(config.gripper.type, arm.host)
        )
        self.max_state_age_s, self.max_camera_age_s = max_state_age_s, max_camera_age_s
        self.camera_ready_timeout_s = camera_ready_timeout_s
        self.arm = self.gripper = self.readers = None

    # -- lifecycle ---------------------------------------------------------------------

    def open(self, *, attended=False, cameras=True):
        if not attended:
            raise FrankaRigError(
                "Attended consent required: connecting takes control of the arm."
            )
        if self.arm is not None or self.readers is not None:
            raise FrankaRigError("Rig already connected.")
        try:
            self.faulted, self.held_on_close = False, {}
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
                raise FrankaRigError("Could not confirm the arm is holding still.")
            return self
        except BaseException:
            self.close()
            raise

    def close(self):
        self.block_dispatch()
        errors = []
        with self._lock:
            # Idle and error-free at disconnect means the robot keeps holding its pose.
            holding = False
            if self.arm is not None and not self.faulted:
                try:
                    state = self.arm.snapshot()
                    holding = state.errors is None and state.mode == "Idle"
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
            self.held_on_close = {ARM: holding and not errors}
            if self.readers is not None:
                try:
                    self.readers.close()
                except BaseException as exc:
                    errors.append(f"cameras: {exc}")
                self.readers = None
        if errors:
            raise FrankaRigError("Disconnect unconfirmed; keep E-stop ready. " + "; ".join(errors))

    # -- reads -------------------------------------------------------------------------

    def _camera_ids(self):
        return {role: self.config.roles[role] for role in self.roles}

    def _state(self):
        if self.arm is None or self.gripper is None:
            raise FrankaRigError("Connect the rig before running.")
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
                raise CameraError(f"{role.replace('_', ' ').title()} camera: {exc}") from exc
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
            "home_pose": list(config.home),
        }

    def latest_frames(self):
        return {role: frame.rgb for role, frame in self._frames().items()}

    def observe(self, ctx=None):
        with self._lock:
            (state, gripper), frames = self._state(), self._frames()
            return franka.observation(
                exterior_frame=frames["exterior_1"].rgb,
                second_exterior_frame=(
                    frames["exterior_2"].rgb if "exterior_2" in frames else None
                ),
                wrist_frame=frames["wrist"].rgb,
                joint_positions=state.position.tolist(),
                gripper=gripper,
                actions_remaining=getattr(ctx, "actions_remaining", 0),
                chunk_size=self.chunk_size,
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
        return np.array([self.max_joint_velocity] * 7 + [np.inf])

    def _tracking(self, group):
        if self.max_joint_step is None:
            return None
        return np.array([self.max_joint_step] * 7 + [np.inf])

    def _send(self, targets):
        target = targets[ARM]
        sent = np.asarray(self.arm.follow(target[:7]), dtype=float)
        self.gripper.command(float(target[7]))
        return {ARM: np.array([*sent, target[7]])}

    def _hold(self):
        return {ARM: self.arm is not None and bool(self.arm.hold())}

    async def _home(self):
        """Move slowly to the home pose. Already within HOME_TOLERANCE, nothing moves."""
        home = np.asarray(self.config.home, dtype=float)
        self.validate_action([*home, 0.0], check_step=False)
        state, _ = self._state()
        offset = float(np.max(np.abs(state.position - home)))
        if offset <= HOME_TOLERANCE:
            return offset
        self._homing = True
        self.enable_dispatch()
        self.gripper.command(0.0)
        await asyncio.to_thread(self.arm.move_to, home)
        state, _ = self._state()
        offset = float(np.max(np.abs(state.position - home)))
        if offset > HOME_SETTLED:
            raise FrankaRigError(
                f"Homing ended {offset:.4f} rad from home. Check for an obstruction."
            )
        return offset
