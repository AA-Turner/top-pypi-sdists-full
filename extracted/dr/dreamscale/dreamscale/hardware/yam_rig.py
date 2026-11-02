"""Persistent local YAM cameras and arms, independent of cloud task lifetime."""

from __future__ import annotations

import asyncio
import math
from concurrent.futures import ThreadPoolExecutor

import numpy as np

from dreamscale import yam
from dreamscale.constants import (
    CAMERA_KEY_BIMANUAL_YAM_LEFT,
    CAMERA_KEY_BIMANUAL_YAM_RIGHT,
    CAMERA_KEY_BIMANUAL_YAM_TOP,
)
from dreamscale.hardware.rig import MeasuredState

from .camera_sources import CameraError, CameraReaders, lagging_latest, wait_for_frames
from .joint_rig import JointRig
from .yam_config import DEFAULT_HOME_POSE, ROLES, YamConfig
from .yam_hold import PersistentArm
from .yam_native import YamHardwareError, _validate_limits

# Joints within this many radians (grippers within this normalized travel)
# are already home: less than one 30 Hz ramp tick at the default 1 rad/s.
HOME_TOLERANCE = 0.02
# Shortest ramp, so small moves take time proportional to their distance.
MIN_HOME_RAMP_S = 0.3


def _measured_hold_target(position, limits):
    # Callers validate freshness, controller health and finite raw feedback.
    # Range excursions do not invalidate the observation: bound only the
    # outgoing hold/home reference, never the encoder readings themselves.
    return np.clip(position, limits[:, 0], limits[:, 1])


class YamTaskStopped(YamHardwareError):
    """Intentional dispatch cancellation; healthy hardware can serve another task."""


SIDES = ("left", "right")


class YamRig(JointRig):
    """Callbacks for policy.run; explicit attended open is the motor boundary.

    task_limits optionally narrows per-side hardware joint limits (7 x 2).
    max_joint_step optionally caps target-to-measured joint error in radians.
    Neither is inferred from another robot's task or deployment.
    """

    groups = SIDES
    value_labels = (*(f"joint {i}" for i in range(1, 7)), "gripper")
    value_units = ("rad",) * 6 + ("normalized",)
    control_period_s = 1 / 30
    fault_error = YamHardwareError
    stopped_error = YamTaskStopped
    limits_name = "configured hardware/task limits"
    action_description = "left six radians + gripper, then right"
    hold_unconfirmed = "Homing hold unconfirmed. Use the hardware E-stop."

    def __init__(
        self,
        config: YamConfig,
        *,
        readers_factory=CameraReaders,
        arm_factory=PersistentArm,
        task_limits=None,
        max_joint_step=None,
        max_joint_velocity=None,
        max_state_age_s=0.25,
        max_camera_age_s=1.0,
        camera_ready_timeout_s=5.0,
    ):
        super().__init__(
            max_joint_step=max_joint_step, max_joint_velocity=max_joint_velocity,
            unit="radians",
        )
        self.config = config.validate(complete=True)
        self.readers_factory, self.arm_factory = readers_factory, arm_factory
        self.task_limits = task_limits or {}
        if not set(self.task_limits) <= {"left", "right"}:
            raise ValueError("Task limits must name left or right.")
        if any(
            not np.isfinite(v) or v <= 0
            for v in (max_state_age_s, max_camera_age_s, camera_ready_timeout_s)
        ):
            raise ValueError("Freshness limits must be positive finite seconds.")
        self.max_state_age_s, self.max_camera_age_s = max_state_age_s, max_camera_age_s
        self.camera_ready_timeout_s = camera_ready_timeout_s
        self.arms = {}
        self.readers = None

    def open(self, *, attended=False, cameras=True):
        if not attended:
            raise YamHardwareError(
                "Attended consent required: connecting sends motor traffic and calibrates grippers."
            )
        if self.arms or self.readers is not None:
            raise YamHardwareError("Rig already connected.")
        try:
            self.faulted = False
            self.held_on_close = {}
            if cameras:
                self.readers = self.readers_factory(
                    [s for s in self.config.cameras if s.id in self.config.roles.values()]
                )
                self.readers.open()
                wait_for_frames(
                    self.readers,
                    self.config.roles,
                    timeout_s=self.camera_ready_timeout_s,
                    max_age_s=self.max_camera_age_s,
                )
            def connect_arm(side):
                arm = self.arm_factory(self.config.arms[side])
                # Register inside the worker so exception/interrupt cleanup also
                # owns a controller whose peer failed before it returned.
                with self._lock:
                    self.arms[side] = arm

            # Each independent CAN controller calibrates its own gripper. Wait
            # for both bounded constructors before validating or unwinding.
            with ThreadPoolExecutor(max_workers=2, thread_name_prefix="yam-connect") as pool:
                connections = [pool.submit(connect_arm, side) for side in ("left", "right")]
                for connection in connections:
                    connection.result()
            self.arms = {side: self.arms[side] for side in ("left", "right")}
            for side, arm in self.arms.items():
                limits = np.asarray(arm.limits).copy()
                _validate_limits(limits)
                if side in self.task_limits:
                    task = np.asarray(self.task_limits[side], dtype=float)
                    _validate_limits(task)
                    if (task[:, 0] < limits[:, 0]).any() or (task[:, 1] > limits[:, 1]).any():
                        raise YamHardwareError("Task limits must stay inside the hardware profile.")
                    limits = task.copy()
                self.limits[side] = limits
            if cameras:
                self.observe(None)
            else:
                self._states()
            self.stop()
            if not all(self.last_hold.values()):
                raise YamHardwareError("Could not establish both measured-pose holds.")
            return self
        except BaseException:
            self.close()
            raise

    def _states(self):
        if set(self.arms) != {"left", "right"}:
            raise YamHardwareError("Connect both arms before running.")
        states = {s: a.snapshot().validate(self.max_state_age_s) for s, a in self.arms.items()}
        if self.on_state is not None:
            self.on_state(MeasuredState(
                position=tuple(v for side in ("left", "right") for v in states[side].position),
                velocity=tuple(v for side in ("left", "right") for v in states[side].velocity),
                capture_unix_s=min(state.timestamp for state in states.values()),
            ))
        return states

    def _frames(self):
        if self.readers is None:
            raise CameraError("Cameras disconnected.")
        frames = {}
        for role in ROLES:
            try:
                frames[role] = lagging_latest(
                    self.readers, self.config.roles[role], warn_age_s=self.max_camera_age_s,
                    on_lag=lambda age_s, role=role: self._camera_lag(role, age_s),
                )
            except CameraError as exc:
                raise CameraError(f"{role.title()} camera: {exc}") from exc
        return frames

    def metadata(self):
        config = self.config
        return {
            "cameras": {
                role: {"backend": c.backend, "width": c.width, "height": c.height, "fps": c.fps}
                for role, camera_id in config.roles.items()
                for c in config.cameras if c.id == camera_id
            },
            "arms": {
                side: {"arm_type": arm.arm_type, "gripper_type": arm.gripper_type}
                for side, arm in config.arms.items()
            },
            "home_pose": list(config.home_pose) if config.home_pose is not None else None,
        }

    def latest_frames(self):
        """Latest RGB frame per role, without reading arm state; for recorders."""
        return {role: frame.rgb for role, frame in self._frames().items()}

    def camera_feed(self):
        """Each camera's latest RGBFrame by its observation camera key, for a camera codec that
        codes frames as they arrive (codec_feed.CameraFeed). No lag reports: observe() makes them.
        """
        readers = self.readers
        if readers is None:
            return {}
        keys = {"top": CAMERA_KEY_BIMANUAL_YAM_TOP, "left": CAMERA_KEY_BIMANUAL_YAM_LEFT,
                "right": CAMERA_KEY_BIMANUAL_YAM_RIGHT}
        return {keys[role]: readers.latest(self.config.roles[role]) for role in ROLES}

    def observe(self, ctx=None):
        with self._lock:
            states, frames = self._states(), self._frames()
            values = {f"{s}_joint_positions": v.position[:6] for s, v in states.items()}
            values.update({f"{s}_joint_velocities": v.velocity[:6] for s, v in states.items()})
            values.update({f"{s}_gripper": v.position[6] for s, v in states.items()})
            return yam.observation(
                **values,
                **{f"{r}_frame": frames[r].rgb for r in ROLES},
                camera_capture_times_ns=tuple(frames[r].timestamp_ns for r in ROLES),
                actions_remaining=getattr(ctx, "actions_remaining", 0),
            )

    # -- JointRig hooks ------------------------------------------------------------------

    def _read(self):
        return {side: state.position for side, state in self._states().items()}

    def _ready(self):
        if self._homing:
            # Attended, configured home uses encoder feedback, not images.
            self._states()
        else:
            self.observe(None)

    def _check_frames(self):
        self._frames()

    def _hold_limits(self, side):
        return self.arms[side].limits

    def _velocity_caps(self, side):
        if self.max_joint_velocity is None:
            return None
        return np.array([self.max_joint_velocity] * 6 + [1.0])

    def _tracking(self, side):
        if self.max_joint_step is None:
            return None
        return np.array([self.max_joint_step] * 6 + [np.inf])

    def _allowance(self, side):
        if self._homing:
            # home() owns pacing and sleeps after EVERY command. Its first
            # waypoint has one tick's budget; pauses never add extra budget.
            return np.array([min(1.0, self.max_joint_velocity or 1.0)] * 6 + [1.0]) / 30
        return super()._allowance(side)

    def _send(self, targets):
        applied = {}
        for side in SIDES:
            if not self._dispatch.is_set():
                raise YamTaskStopped("Task stopped before dispatch.")
            applied[side] = np.asarray(self.arms[side].command(targets[side]), dtype=float)
        return applied

    def _hold(self):
        holds = {}
        for side, arm in self.arms.items():
            try:
                state = arm.snapshot().validate(self.max_state_age_s)
                target = _measured_hold_target(state.position, arm.limits)
                applied = np.asarray(arm.command(target), dtype=float)
                if applied.shape != (7,) or not np.array_equal(applied, target):
                    raise YamHardwareError("Driver changed the measured hold target.")
                arm.snapshot().validate(self.max_state_age_s)
                holds[side] = True
            except Exception:
                holds[side] = False
        return holds

    async def _home(self, *, sleep=asyncio.sleep):
        """Ramp to the rig home, validate fresh feedback, then hold.

        Reuses both-arm dispatch validation and retains raw encoder feedback.
        Stale/invalid feedback still stops. No catch-up burst or collision checking.
        Returns the largest measured arm offset in radians. Like the default
        inspect-robots YAM path, completion does not require precision settling.
        Arms already within HOME_TOLERANCE skip the ramp and hold where measured.
        """
        start = np.asarray(self.read_hold_action(), dtype=float)
        target = np.asarray(self.config.home_pose or DEFAULT_HOME_POSE, dtype=float)
        self.validate_action(target, check_step=False)
        arm_indices = (*range(6), *range(7, 13))
        travel = np.abs(target - start)
        # Lower user caps lengthen the nominal ramp. Projection can pause
        # its progress further when measured motion falls behind.
        joint_speed = min(1.0, self.max_joint_velocity or 1.0)
        duration = max(
            MIN_HOME_RAMP_S,
            1.875 * max(travel[list(arm_indices)]) / joint_speed,
            1.875 * max(travel[[6, 13]]),
        )
        steps = math.ceil(duration * 30)
        self._homing = True
        self.enable_dispatch()
        # Compare raw feedback, not the clipped start: an encoder outside a
        # limit that home sits on is not home. Never exceed the completion cap.
        states = self._states()
        measured = np.concatenate([states[s].position for s in ("left", "right")])
        error = np.abs(measured - target)
        offset = float(np.max(error[list(arm_indices)]))
        if offset <= min(HOME_TOLERANCE, self.max_joint_step or HOME_TOLERANCE) and (
            np.max(error[[6, 13]]) <= HOME_TOLERANCE
        ):
            return offset  # finally confirms the measured-pose hold
        step = 1
        # Bound a stalled homing operation rather than reporting home or
        # waiting indefinitely. Healthy lag may extend the nominal ramp.
        for _ in range(max(450, 3 * steps)):
            u = step / steps
            blend = u * u * u * (10 - 15 * u + 6 * u * u)
            waypoint = target if step == steps else start + blend * (target - start)
            applied = np.asarray(self.act(waypoint).accepted_action)
            # Sleep after every dispatch; a late callback never causes
            # compressed catch-up commands.
            await sleep(1 / 30)
            states = self._states()
            measured = np.concatenate([states[s].position for s in ("left", "right")])
            offset = float(np.max(np.abs(measured - target)[list(arm_indices)]))
            if np.array_equal(applied, waypoint):
                if step < steps:
                    step += 1
                elif self.max_joint_step is None or offset <= self.max_joint_step:
                    return offset
            # Repeat a capped waypoint until it is sent in full, instead
            # of advancing the ramp into a growing tracking error.
        raise YamHardwareError(
            f"Homing timed out before reaching home; largest joint offset {offset:.4f} rad. "
            "Check for an obstruction or an arm that is not following commands."
        )

    def close(self):
        self.block_dispatch()
        errors = []
        with self._lock:
            for side, arm in list(self.arms.items()):
                try:
                    arm.close()
                    self.held_on_close[side] = bool(getattr(arm, "holds_after_close", False))
                except BaseException as exc:
                    self.held_on_close[side] = False
                    errors.append(f"{side}: {exc}")
            self.arms.clear()
            if self.readers is not None:
                try:
                    self.readers.close()
                except BaseException as exc:
                    errors.append(f"cameras: {exc}")
                self.readers = None
        if errors:
            raise YamHardwareError(
                "Arm hold or disconnect unconfirmed; check hardware E-stop. " + "; ".join(errors)
            )
