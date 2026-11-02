"""The bimanual xArm 7 rig: two arms (aft, fore) with xArm Grippers, a scene camera and a
camera on each wrist.

Actions are 16 values, aft arm first: seven absolute joint positions in radians, then the
gripper's close intent from 0 (open) to 1 (closed), which moves the jaw to that fraction of
its travel (or, with the arm's ``gripper_control`` set to ``threshold``, shuts it from 0.5).
Observations carry the same layout with each gripper's drive_joint angle in radians (0 open,
0.85 closed), the state recordings on these arms store, and the cameras under the names
their deployments read.

A gripper's held value is its last command, never its reading: a gripper closed on a bottle
reads part-open, and holding at that reading would let the bottle go.
"""

from __future__ import annotations

import asyncio
import time

import numpy as np

from dreamscale import robot
from dreamscale.embodiments import XARM7
from dreamscale.hardware.rig import MeasuredState

from .camera_sources import CameraError, CameraReaders, lagging_latest, wait_for_frames
from .joint_rig import JointRig
from .xarm7_config import ARMS, XArm7Config
from .xarm_arm import JOINTS, MOVE_POLL_S, XArm, XArmError, XArmGripper

CAMERA_KEYS = dict(zip(XARM7.camera_roles, XARM7.recording_keys, strict=True))
GRIPPER_LIMITS = np.array([[0.0, 1.0]])
HOME_TOLERANCE = 0.02
HOME_SETTLED = 0.05
# A gripper reading past this many radians from open counts as closed when nothing has been
# commanded yet (a run that starts holding something keeps holding it).
CLOSED_READING = 0.1
GRIPPER_OPEN_TIMEOUT_S = 3.0
GRIPPER_OPEN = 0.05


class XArm7RigError(XArmError):
    """The rig refused a command or could not confirm its hold."""


class XArm7TaskStopped(XArm7RigError):
    """Intentional dispatch cancellation; healthy hardware can serve another task."""


class XArm7Rig(JointRig):
    """policy.run callbacks for two xArm 7s; explicit attended open is the motor boundary."""

    groups = ARMS
    value_labels = (*(f"joint {i}" for i in range(1, JOINTS + 1)), "gripper")
    value_units = ("rad",) * JOINTS + ("intent",)
    control_period_s = 1 / 20
    fault_error = XArm7RigError
    stopped_error = XArm7TaskStopped
    limits_name = "arm's joint limits"
    action_description = (
        "per arm (aft, then fore) seven joint positions in radians, then the gripper from 0 to 1"
    )
    hold_unconfirmed = "Homing hold unconfirmed. Use the E-stop."

    def __init__(
        self,
        config: XArm7Config,
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
        if not set(roles) <= set(config.roles):
            raise ValueError("Each camera role must be mapped in the rig.")
        self.roles, self.chunk_size = tuple(roles), chunk_size
        self.readers_factory = readers_factory
        self.arm_factory = arm_factory or (lambda name: XArm(config.arms[name].host))
        self.gripper_factory = gripper_factory or (
            lambda name, arm: XArmGripper(
                arm, config.arms[name].gripper, control=config.arms[name].gripper_control
            )
        )
        self.max_state_age_s, self.max_camera_age_s = max_state_age_s, max_camera_age_s
        self.camera_ready_timeout_s = camera_ready_timeout_s
        self.arms, self.grippers, self.readers = {}, {}, None
        self.intent = {}

    # -- lifecycle ---------------------------------------------------------------------

    def open(self, *, attended=False, cameras=True):
        if not attended:
            raise XArm7RigError("Attended consent required: connecting takes control of the arms.")
        if self.arms or self.readers is not None:
            raise XArm7RigError("Rig already connected.")
        try:
            self.faulted, self.held_on_close = False, {}
            if cameras and not self.roles:
                raise XArm7RigError("This rig was made without cameras.")
            if cameras:
                self.readers = self.readers_factory(
                    [self.config.camera(role) for role in self.roles]
                )
                self.readers.open()
                wait_for_frames(
                    self.readers, self._camera_ids(), timeout_s=self.camera_ready_timeout_s,
                    max_age_s=self.max_camera_age_s,
                )
            for name in ARMS:
                self.arms[name] = self.arm_factory(name).connect()
                self.grippers[name] = self.gripper_factory(name, self.arms[name]).open()
            self.limits = {
                name: np.vstack([np.asarray(self.arms[name].limits, dtype=float), GRIPPER_LIMITS])
                for name in ARMS
            }
            self.intent = {
                name: 1.0 if self.grippers[name].state() > CLOSED_READING else 0.0
                for name in ARMS
            }
            if cameras:
                self.observe(None)
            else:
                self._state()
            self.stop()
            if not all(self.last_hold.values()):
                raise XArm7RigError("Could not confirm the arms are holding still.")
            return self
        except BaseException:
            self.close()
            raise

    def close(self):
        self.block_dispatch()
        errors = []
        with self._lock:
            held = {}
            for name in ARMS:
                arm = self.arms.get(name)
                holding = False
                if arm is not None and not self.faulted:
                    try:
                        state = arm.snapshot()
                        holding = not state.error_code and state.state in (1, 2)
                    except Exception:
                        holding = False
                for label, device in ((f"{name} gripper", self.grippers.get(name)),
                                      (f"{name} arm", arm)):
                    if device is None:
                        continue
                    try:
                        device.close()
                    except BaseException as exc:
                        errors.append(f"{label}: {exc}")
                # An enabled xArm keeps its last target after the connection ends.
                held[name] = holding and not errors
            self.arms, self.grippers = {}, {}
            self.held_on_close = held
            if self.readers is not None:
                try:
                    self.readers.close()
                except BaseException as exc:
                    errors.append(f"cameras: {exc}")
                self.readers = None
        if errors:
            raise XArm7RigError("Disconnect unconfirmed; keep E-stop ready. " + "; ".join(errors))

    # -- reads -------------------------------------------------------------------------

    def _camera_ids(self):
        return {role: self.config.roles[role] for role in self.roles}

    def _state(self):
        """Per arm, the validated arm state and the gripper's drive_joint radians."""
        if set(self.arms) != set(ARMS):
            raise XArm7RigError("Connect the rig before running.")
        states = {
            name: (
                self.arms[name].snapshot().validate(self.max_state_age_s),
                float(self.grippers[name].state()),
            )
            for name in ARMS
        }
        if self.on_state is not None:
            self.on_state(MeasuredState(
                position=tuple(v for name in ARMS
                               for v in (*states[name][0].position.tolist(), states[name][1])),
                velocity=tuple(v for name in ARMS
                               for v in (*states[name][0].velocity.tolist(), 0.0)),
                capture_unix_s=time.time(),
            ))
        return states

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
            "arms": {
                name: {"gripper": config.arms[name].gripper,
                       "gripper_control": config.arms[name].gripper_control}
                for name in ARMS
            },
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
            states, frames = self._state(), self._frames()
            return robot.observation(
                cameras={CAMERA_KEYS[role]: frames[role].rgb for role in self.roles},
                state=[v for name in ARMS
                       for v in (*states[name][0].position.tolist(), states[name][1])],
                actions_remaining=getattr(ctx, "actions_remaining", 0),
            )

    # -- JointRig hooks ----------------------------------------------------------------

    def _read(self):
        states = self._state()
        return {
            name: np.array([*states[name][0].position, self.intent[name]]) for name in ARMS
        }

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
        return np.array([float(self.max_joint_velocity)] * JOINTS + [np.inf])

    def _tracking(self, group):
        if self.max_joint_step is None:
            return None
        return np.array([float(self.max_joint_step)] * JOINTS + [np.inf])

    def _send(self, targets):
        applied = {}
        for name in ARMS:
            target = targets[name]
            sent = np.asarray(self.arms[name].follow(target[:JOINTS]), dtype=float)
            self.grippers[name].command(float(target[JOINTS]))
            self.intent[name] = float(target[JOINTS])
            applied[name] = np.array([*sent, target[JOINTS]])
        return applied

    def _hold(self):
        return {name: name in self.arms and bool(self.arms[name].hold()) for name in ARMS}

    @property
    def has_home(self) -> bool:
        return self.config.home_pose is not None

    async def _open_grippers(self, sleep) -> None:
        for name in ARMS:
            self.grippers[name].command(0.0)
            self.intent[name] = 0.0
        deadline = time.monotonic() + GRIPPER_OPEN_TIMEOUT_S
        while any(self.grippers[name].state() > GRIPPER_OPEN for name in ARMS
                  if self.config.arms[name].gripper != "none"):
            if time.monotonic() > deadline:
                raise XArm7RigError("A gripper didn't open. Check that nothing blocks it.")
            await sleep(MOVE_POLL_S)

    async def _home(self, *, sleep=asyncio.sleep):
        """Open the grippers and move both arms slowly to the home pose. With no home pose
        nothing moves; already at home, only the grippers open."""
        if self.config.home_pose is None:
            return None
        home = np.asarray(self.config.home_pose, dtype=float)
        poses = {name: home[i * JOINTS:(i + 1) * JOINTS] for i, name in enumerate(ARMS)}
        self.validate_action(
            [v for name in ARMS for v in (*poses[name], 0.0)], check_step=False,
        )
        self._homing = True
        self.enable_dispatch()
        await self._open_grippers(sleep)
        states = self._state()
        offset = max(float(np.max(np.abs(states[n][0].position - poses[n]))) for n in ARMS)
        if offset <= HOME_TOLERANCE:
            return offset
        for name in ARMS:
            self.arms[name].start_move(poses[name])
        try:
            while any(self.arms[name].moving() for name in ARMS):
                await sleep(MOVE_POLL_S)
        except BaseException:
            for name in ARMS:
                self.arms[name].stop_move()
            raise
        states = self._state()
        offset = max(float(np.max(np.abs(states[n][0].position - poses[n]))) for n in ARMS)
        if offset > HOME_SETTLED:
            raise XArm7RigError(
                f"Homing ended {offset:.4f} rad from home. Check for an obstruction."
            )
        return offset
