"""The OpenARM rig: one or two Anvil OpenARM 2.0 arms on a Devbox, driven through Anvil's
control stack.

Actions and observations carry the model's own layout (the rig file's): the arms in its
order, each arm's seven joint positions in radians with its gripper's opening in metres
before or after them. The rig turns that into the order the stack's controllers take.

The stack holds each arm at its last target, so a stop commands the measured pose once (a
target left leading a blocked arm would keep pushing it) and then sends nothing. The stack
enforces almost no limits on what a program commands: every target here is held inside the
joints' own limits, a step envelope around the measured pose and a speed cap before it is
sent, and an arm that reads outside those limits is refused.
"""

from __future__ import annotations

import asyncio
import time

import numpy as np

from dreamscale import robot
from dreamscale.hardware.rig import MeasuredState, RigFault

from .camera_sources import CameraError, lagging_latest, wait_for_frames
from .joint_rig import JointRig
from .openarm_config import JOINTS, OpenArmConfig
from .openarm_stack import (
    GRIPPER_RANGE,
    START_STACK,
    AnvilStack,
    controller_name,
)

HOME_TOLERANCE = 0.02
# Homing moves no faster than this, whatever the run's speed cap.
HOME_VELOCITY = 0.2
HOME_TIMEOUT_S = 60.0
# A joint resting on its stop reads just outside the limits (they keep a margin); one further
# out than this means the stack's description doesn't match the arm.
OUTSIDE_TOLERANCE = 0.05


class OpenArmRigError(RigFault):
    """The rig refused a command or could not confirm its hold."""


class OpenArmTaskStopped(OpenArmRigError):
    """Intentional dispatch cancellation; healthy hardware can serve another task."""


class OpenArmRig(JointRig):
    """policy.run callbacks for an OpenARM; explicit attended open is the motor boundary."""

    control_period_s = 1 / 30
    fault_error = OpenArmRigError
    stopped_error = OpenArmTaskStopped
    limits_name = "arm's joint limits"
    hold_unconfirmed = "Homing hold unconfirmed. Use the E-stop."

    def __init__(
        self,
        config: OpenArmConfig,
        *,
        roles: tuple[str, ...] | None = None,
        chunk_size: int | None = None,
        stack_factory=AnvilStack,
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
        roles = tuple(config.cameras if roles is None else roles)
        if not set(roles) <= set(config.cameras):
            raise ValueError("Each camera must be one the rig file names.")
        self.roles, self.chunk_size = roles, chunk_size
        self.groups = tuple(config.arms)
        joints = tuple(f"joint {i}" for i in range(1, JOINTS + 1))
        self._gripper_first = config.gripper == "first"
        self._gripper = 0 if self._gripper_first else JOINTS
        if self._gripper_first:
            self.value_labels, self.value_units = ("gripper", *joints), ("m",) + ("rad",) * JOINTS
        else:
            self.value_labels, self.value_units = (*joints, "gripper"), ("rad",) * JOINTS + ("m",)
        place = "before" if self._gripper_first else "after"
        self.action_description = (
            f"per arm ({', then '.join(self.groups)}) seven joint positions in radians, with "
            f"the gripper's opening in metres {place} them"
        )
        self.stack_factory = stack_factory
        self.max_state_age_s, self.max_camera_age_s = max_state_age_s, max_camera_age_s
        self.camera_ready_timeout_s = camera_ready_timeout_s
        self.stack = None
        # Each gripper's last command: what it holds, whatever it reads (closed on an object,
        # it reads part-open).
        self.intent = {}
        # Arms commanded since their last hold: their target may lead the measured pose.
        self._leading = set()

    # -- layout ------------------------------------------------------------------------

    def send_cameras_as(self, keys):
        """Send the cameras in a deployment's own order (it takes them in no other): the
        same cameras, as its ``observation.images.<camera>`` keys list them."""
        roles = tuple(key.removeprefix("observation.images.") for key in keys)
        if set(roles) != set(self.roles) or len(roles) != len(self.roles):
            raise ValueError("A deployment's cameras must be the rig's own.")
        with self._lock:
            self.roles = roles

    def _to_model(self, values):
        """The stack's order (joints, then gripper) to the model's."""
        values = np.asarray(values, dtype=float)
        return np.roll(values, 1, axis=0) if self._gripper_first else values.copy()

    def _to_stack(self, values):
        values = np.asarray(values, dtype=float)
        return np.roll(values, -1, axis=0) if self._gripper_first else values.copy()

    def _joint_values(self, value):
        """An array with value at each joint and inf at the gripper, in the model's order."""
        values = np.full(JOINTS + 1, float(value))
        values[self._gripper] = np.inf
        return values

    # -- lifecycle ---------------------------------------------------------------------

    def open(self, *, attended=False, cameras=True):
        if not attended:
            raise OpenArmRigError(
                "Attended consent required: connecting takes control of the arms."
            )
        if self.stack is not None:
            raise OpenArmRigError("Rig already connected.")
        try:
            self.faulted, self.held_on_close, self.intent = False, {}, {}
            self._leading = set()
            if cameras and not self.roles:
                raise OpenArmRigError("This rig was made without cameras.")
            self.stack = self.stack_factory(self.config.url)
            self.stack.open(cameras=self.roles if cameras else (), command=self.groups)
            self._require_controllers()
            self.limits = {
                arm: self._to_model(self.stack.limits(arm)) for arm in self.groups
            }
            self.stack.wait_for_arms(self.groups, max_age_s=self.max_state_age_s)
            self._require_inside_limits(self._state())
            if cameras:
                wait_for_frames(
                    self.stack, {role: role for role in self.roles},
                    timeout_s=self.camera_ready_timeout_s, max_age_s=self.max_camera_age_s,
                )
                self.observe(None)
            self.stop()
            if not all(self.last_hold.values()):
                raise OpenArmRigError("Could not confirm the arms are holding still.")
            return self
        except BaseException:
            self.close()
            raise

    def _require_controllers(self):
        """Refuse a stack that would ignore joint commands (leader-follower control) or that
        runs something other than the forward position controllers."""
        states = self.stack.controllers()
        for arm in self.groups:
            name = controller_name(arm)
            if states.get(name) != "active":
                state = states.get(name)
                raise OpenArmRigError(
                    f"The {arm} arm isn't taking joint commands: {name} is "
                    f"{state if state else 'not running'}. {START_STACK}"
                )

    def _require_inside_limits(self, measured):
        """Refuse an arm that reads outside the limits the stack describes: the first target
        would be the nearest limit, a jump no step envelope covers."""
        for arm in self.groups:
            low, high = self.limits[arm][:, 0], self.limits[arm][:, 1]
            for i, value in enumerate(measured[arm]):
                if i != self._gripper and not (
                    low[i] - OUTSIDE_TOLERANCE <= value <= high[i] + OUTSIDE_TOLERANCE
                ):
                    raise OpenArmRigError(
                        f"The {arm} arm's {self.value_labels[i]} reads {value:.3f} rad, outside "
                        f"the limits the stack describes ({low[i]:.3f} to {high[i]:.3f}). "
                        "Bring it inside, or check the stack's description matches this arm."
                    )

    def close(self):
        self.block_dispatch()
        error = None
        with self._lock:
            stack, self.stack = self.stack, None
            held = {}
            if stack is not None:
                for arm in self.groups:
                    try:
                        stack.arm_state(arm, self.max_state_age_s)
                        # The stack keeps holding its last target once we disconnect.
                        held[arm] = not self.faulted
                    except Exception:
                        held[arm] = False
                try:
                    stack.close()
                except BaseException as exc:
                    error = exc
            self.held_on_close = held
        if error is not None:
            raise OpenArmRigError(f"Disconnect unconfirmed; keep E-stop ready. {error}")

    # -- reads -------------------------------------------------------------------------

    def _state(self):
        """Per arm, the measured joints and gripper in the model's order."""
        if self.stack is None:
            raise OpenArmRigError("Connect the rig before running.")
        states = {arm: self.stack.arm_state(arm, self.max_state_age_s) for arm in self.groups}
        if self.on_state is not None:
            self.on_state(MeasuredState(
                position=tuple(
                    v for arm in self.groups for v in self._to_model(states[arm].position)
                ),
                velocity=tuple(
                    v for arm in self.groups for v in self._to_model(states[arm].velocity)
                ),
                capture_unix_s=time.time(),
            ))
        return {arm: self._to_model(states[arm].position) for arm in self.groups}

    def _frames(self):
        if self.stack is None:
            raise CameraError("Cameras disconnected.")
        frames = {}
        for role in self.roles:
            try:
                frames[role] = lagging_latest(
                    self.stack, role, warn_age_s=self.max_camera_age_s,
                    on_lag=lambda age_s, role=role: self._camera_lag(role, age_s),
                )
            except CameraError as exc:
                raise CameraError(f"{role} camera: {exc}") from exc
        return frames

    def metadata(self):
        config = self.config
        return {
            "arms": list(config.arms),
            "gripper": config.gripper,
            "cameras": list(self.roles),
            "home_pose": list(config.home_pose) if config.home_pose is not None else None,
        }

    def latest_frames(self):
        return {role: frame.rgb for role, frame in self._frames().items()}

    def observe(self, ctx=None):
        with self._lock:
            states, frames = self._state(), self._frames()
            return robot.observation(
                cameras={f"observation.images.{role}": frames[role].rgb for role in self.roles},
                state=[v for arm in self.groups for v in states[arm]],
                actions_remaining=getattr(ctx, "actions_remaining", 0),
            )

    # -- JointRig hooks ----------------------------------------------------------------

    def _read(self):
        measured = self._state()
        for arm, values in measured.items():
            values[self._gripper] = self.intent.get(
                arm, float(np.clip(values[self._gripper], *GRIPPER_RANGE))
            )
        return measured

    def _ready(self):
        self._require_inside_limits(self._state())
        if not self._homing:
            self.observe(None)

    def _check_frames(self):
        self._frames()

    def _velocity_caps(self, group):
        cap = self.max_joint_velocity
        if self._homing:
            cap = HOME_VELOCITY if cap is None else min(float(cap), HOME_VELOCITY)
        return None if cap is None else self._joint_values(cap)

    def _tracking(self, group):
        return None if self.max_joint_step is None else self._joint_values(self.max_joint_step)

    def _send(self, targets):
        applied = {}
        for arm in self.groups:
            target = np.asarray(targets[arm], dtype=float)
            self._leading.add(arm)
            self.stack.command(arm, self._to_stack(target))
            self.intent[arm] = float(target[self._gripper])
            applied[arm] = target.copy()
        return applied

    def _hold(self):
        """Hold each arm where it reads. An arm commanded since its last hold gets its measured
        joints as one last target (its gripper keeps its last command), so a target that led
        a blocked arm stops pushing; an arm not commanded is already held by the stack, and
        nothing is sent. Confirmed while its joint states keep arriving."""
        holds = {}
        for arm in self.groups:
            try:
                state = self.stack.arm_state(arm, self.max_state_age_s)
                if arm in self._leading:
                    target = self._to_model(state.position)
                    target[self._gripper] = self.intent[arm]
                    target = np.clip(target, *self.limits[arm].T)
                    self.stack.command(arm, self._to_stack(target))
                    self._leading.discard(arm)
                holds[arm] = True
            except Exception:
                holds[arm] = False
        return holds

    @property
    def has_home(self) -> bool:
        return self.config.home_pose is not None

    async def _home(self, *, sleep=asyncio.sleep):
        """Move every arm slowly to the home pose; each gripper is held at the opening it
        reads (or its last command). With no home pose nothing moves."""
        if self.config.home_pose is None:
            return None
        home = np.asarray(self.config.home_pose, dtype=float)
        poses = {arm: home[i * JOINTS:(i + 1) * JOINTS] for i, arm in enumerate(self.groups)}

        def offset(measured):
            return max(
                float(np.max(np.abs(self._to_stack(measured[arm])[:JOINTS] - poses[arm])))
                for arm in self.groups
            )

        def target(measured):
            values = []
            for arm in self.groups:
                gripper = self._to_stack(measured[arm])[JOINTS]
                values += self._to_model([*poses[arm], gripper]).tolist()
            return values

        self._homing = True
        self.validate_action(target(self._read()), check_step=False)
        self.enable_dispatch()
        deadline = time.monotonic() + HOME_TIMEOUT_S
        while True:
            measured = self._read()
            away = offset(measured)
            if away <= HOME_TOLERANCE:
                return away
            if time.monotonic() > deadline:
                raise OpenArmRigError(
                    f"Homing ended {away:.4f} rad from home. Check for an obstruction."
                )
            self.act(target(measured))
            await sleep(self.control_period_s)
