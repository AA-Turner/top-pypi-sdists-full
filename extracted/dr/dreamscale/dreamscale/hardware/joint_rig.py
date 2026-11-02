"""The joint-command core every attended rig shares.

A rig's action is its arm groups' values concatenated, in group order ("left" then
"right" for YAM; one "arm" for SO-101 and Franka), each group's grippers included.
JointRig owns everything that must behave the same on every robot: the dispatch gate,
fault latching, limit and step validation, MotionLimiter projection, act/stop, and the
homing hold contract. A robot supplies reads, writes, holds and its homing motion.
"""

from __future__ import annotations

import asyncio
import threading
import time

import numpy as np

from dreamscale.hardware.rig import RigFault
from dreamscale.motion.limiter import LimitConflict, MotionLimiter
from dreamscale.policy.types import ActResult

from .camera_sources import CameraError


def _sentence(text: str) -> str:
    return text[:1].upper() + text[1:]


class RigTaskStopped(RigFault):
    """Intentional dispatch cancellation; healthy hardware can serve another task."""


class JointRig:
    """Shared dispatch, limits and hold contract; see dreamscale.hardware.rig.Rig.

    Subclasses set, before dispatch:
      groups: arm group names in action order
      limits: {group: (n, 2) command range}
      value_labels: per-group labels ("joint 1", ..., "gripper")
      value_units: per-group unit words for messages ("rad", "deg", "normalized")
    and implement _read(), _send(targets) and _hold(). Override _velocity_caps() and
    _tracking() for per-value limits (np.inf leaves a value free to lead, like a gripper
    closing on an object), _allowance() for paced motion, _ready() and _check_frames()
    for camera freshness, and _home() for the robot's homing motion.
    """

    groups: tuple[str, ...] = ("arm",)
    value_labels: tuple[str, ...] = ()
    value_units: tuple[str, ...] = ()
    # The longest tick a speed allowance spans, so a late callback never bursts.
    control_period_s: float = 1 / 30
    fault_error: type[RigFault] = RigFault
    stopped_error: type[RigFault] = RigTaskStopped
    limits_name = "configured joint limits"
    action_description = "joint targets"
    hold_unconfirmed = "Homing hold unconfirmed. Use the E-stop."

    def __init__(self, *, max_joint_step=None, max_joint_velocity=None, unit="joint units",
                 clock=None):
        for name, value in (("max_joint_step", max_joint_step),
                            ("max_joint_velocity", max_joint_velocity)):
            if value is not None and (
                isinstance(value, bool) or not np.isfinite(value) or value <= 0
            ):
                raise ValueError(f"{name} must be positive finite {unit}.")
        self.max_joint_step, self.max_joint_velocity = max_joint_step, max_joint_velocity
        # Looked up per call, so a patched time.monotonic drives every rig's clock.
        self.clock = clock or (lambda: time.monotonic())
        self.limits = {}
        self._lock = threading.RLock()
        self._dispatch = threading.Event()
        self._previous = None
        self._previous_time = None
        self._homing = False
        self.faulted = False
        self.last_hold = {}
        self.held_on_close = {}
        self.on_state = None
        # on_camera_lag(role, age_s): a camera's frame is older than the rig's freshness
        # limit but the camera still runs (the run warns and continues).
        self.on_camera_lag = None

    # -- robot hooks -----------------------------------------------------------------

    def _read(self) -> dict[str, np.ndarray]:
        """Fresh, validated measured positions per group, in action units."""
        raise NotImplementedError

    def _send(self, targets: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
        """Write validated targets; return what each group's driver applied."""
        raise NotImplementedError

    def _hold(self) -> dict[str, bool]:
        """Hold every group at its measured pose; True per confirmed group."""
        raise NotImplementedError

    async def _home(self, **options) -> float:
        raise NotImplementedError

    def _ready(self):
        """Before dispatch: whatever must be fresh (feedback, cameras)."""
        self._read()

    def _check_frames(self):
        """During dispatch: refuse to drain a model queue once a camera has stopped."""

    def _camera_lag(self, role, age_s):
        if self.on_camera_lag is not None:
            self.on_camera_lag(role, age_s)

    def _velocity_caps(self, group) -> np.ndarray | None:
        if self.max_joint_velocity is None:
            return None
        return np.full(len(self.limits[group]), float(self.max_joint_velocity))

    def _tracking(self, group) -> np.ndarray | None:
        if self.max_joint_step is None:
            return None
        return np.full(len(self.limits[group]), float(self.max_joint_step))

    def _allowance(self, group) -> np.ndarray | None:
        caps = self._velocity_caps(group)
        if caps is None:
            return None
        dt = min(self.control_period_s, max(0.0, self.clock() - self._previous_time))
        return caps * dt

    def _hold_limits(self, group) -> np.ndarray:
        return self.limits[group]

    # -- shared behaviour ----------------------------------------------------------------

    @property
    def has_home(self) -> bool:
        return True

    def _prefix(self, group) -> str:
        return f"{group.title()} " if len(self.groups) > 1 else ""

    def _split(self, values) -> dict[str, np.ndarray]:
        out, start = {}, 0
        for group in self.groups:
            size = len(self.limits[group])
            out[group] = np.asarray(values[start:start + size], dtype=float).copy()
            start += size
        return out

    @staticmethod
    def _join(values: dict[str, np.ndarray]) -> np.ndarray:
        return np.concatenate([np.asarray(v, dtype=float) for v in values.values()])

    def action_limits(self) -> dict[str, list]:
        return {group: np.asarray(limits).tolist() for group, limits in self.limits.items()}

    def read_hold_action(self, ctx=None) -> tuple[float, ...]:
        with self._lock:
            measured = self._read()
            return tuple(self._join({
                g: np.clip(measured[g], *self._hold_limits(g).T) for g in self.groups
            }).tolist())

    def validate_action(self, action, *, measured=None, check_step=True, saturate=False):
        """The action split per group, inside every group's limits; raises fault_error."""
        raw = np.asarray(action)
        target = np.asarray(action, dtype=float)
        size = sum(len(self.limits.get(g, ())) for g in self.groups)
        if set(self.limits) != set(self.groups):
            raise self.fault_error("Connect the arms before validating targets.")
        if raw.dtype.kind == "b" or target.shape != (size,) or not np.isfinite(target).all():
            raise self.fault_error(f"Expected {size} finite targets: {self.action_description}.")
        if check_step and self.max_joint_step is not None and measured is None:
            measured = self._read()
        targets = self._split(target)
        for group, value in targets.items():
            low, high = self.limits[group][:, 0], self.limits[group][:, 1]
            if saturate:
                value[:] = np.clip(value, low, high)
            invalid = np.flatnonzero((value < low) | (value > high))
            if invalid.size:
                details = "; ".join(
                    f"{self.value_labels[i]}: {value[i]:.6f} {self.value_units[i]} outside "
                    f"[{low[i]:.6f}, {high[i]:.6f}]" for i in invalid
                )
                raise self.fault_error(_sentence(
                    f"{self._prefix(group)}target exceeds the {self.limits_name}: {details}."
                ))
            if check_step and self.max_joint_step is not None:
                limiter = MotionLimiter(low, high, tracking=self._tracking(group))
                tracked = limiter.tracking_applies(measured[group])
                error = np.abs(value - measured[group])
                over = tracked & (error > self.max_joint_step)
                if over.any():
                    i = int(np.argmax(np.where(over, error, -1.0)))
                    unit = self.value_units[i]
                    raise self.fault_error(_sentence(
                        f"{self._prefix(group)}target exceeds max_joint_step: "
                        f"{self.value_labels[i]} target {value[i]:.6f} {unit}, measured "
                        f"{measured[group][i]:.6f} {unit}, difference {error[i]:.6f} {unit} "
                        f"exceeds {self.max_joint_step:.6f} {unit}."
                    ))
        return targets

    def _project(self, action, measured) -> dict[str, np.ndarray]:
        targets = self.validate_action(action, check_step=False, saturate=True)
        for group in self.groups:
            limiter = MotionLimiter(*self.limits[group].T, tracking=self._tracking(group))
            try:
                targets[group] = limiter.project(
                    targets[group], previous=self._previous[group],
                    measured=measured[group], allowance=self._allowance(group),
                )
            except LimitConflict as exc:
                raise self.fault_error(_sentence(
                    f"{self._prefix(group)}measured motion leaves no command satisfying both "
                    "position/tracking and velocity bounds. Stop and check the arm."
                )) from exc
        return targets

    def enable_dispatch(self):
        with self._lock:
            if self.faulted:
                raise self.fault_error("Rig faulted. Exit and reconnect before another task.")
            self._ready()
            hold = self._split(self.read_hold_action())
            self._previous = {g: np.clip(hold[g], *self.limits[g].T) for g in self.groups}
            self._previous_time = self.clock()
            self._dispatch.set()

    def block_dispatch(self):
        # Clear before waiting for an already-running callback to leave its lock.
        self._dispatch.clear()

    def act(self, action, ctx=None) -> ActResult:
        with self._lock:
            if not self._dispatch.is_set() or self.faulted:
                raise self.stopped_error("Task stopped; action rejected.")
            try:
                measured = self._read()
                if not self._homing:
                    self._check_frames()
                targets = self._project(action, measured)
                # Validate every group's projected target before any write.
                self.validate_action(self._join(targets), measured=measured)
                if not self._dispatch.is_set():
                    raise self.stopped_error("Task stopped before dispatch.")
                applied = self._send(targets)
                for group in self.groups:
                    value = np.asarray(applied[group], dtype=float)
                    if value.shape != targets[group].shape or not np.isfinite(value).all():
                        raise self.fault_error(f"{group} driver returned an invalid target.")
                    if not np.array_equal(value, targets[group]):
                        raise self.fault_error(f"{group} driver changed the validated target.")
                self._previous = {g: np.asarray(applied[g], dtype=float) for g in self.groups}
                self._previous_time = self.clock()
                return ActResult(accepted_action=tuple(self._join(self._previous).tolist()))
            except (self.stopped_error, CameraError):
                # A task boundary, or a camera failure, which doesn't invalidate healthy
                # motor feedback. stop() still latches a fault if a hold is unconfirmed.
                self.stop()
                raise
            except BaseException:
                self.faulted = True
                self.stop()
                raise

    def stop(self) -> dict[str, bool]:
        """Block dispatch and hold at the measured pose; latch a fault if unconfirmed."""
        self.block_dispatch()
        with self._lock:
            try:
                holds = dict(self._hold())
            except Exception:
                holds = {group: False for group in self.groups}
            self.last_hold = holds
            if not holds or not all(holds.values()):
                self.faulted = True
            return dict(holds)

    async def home(self, **options):
        """The robot's homing motion, then a confirmed hold. None without a home pose."""
        if not self.has_home:
            self.stop()
            return None
        failure = None
        try:
            return await self._home(**options)
        except BaseException as exc:
            failure = exc
            if not isinstance(exc, (asyncio.CancelledError, KeyboardInterrupt,
                                    self.stopped_error)):
                self.faulted = True
            raise
        finally:
            self._homing = False
            holds = self.stop()
            if failure is None and not all(holds.values()):
                raise self.fault_error(self.hold_unconfirmed)
