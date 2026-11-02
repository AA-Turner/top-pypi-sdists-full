"""The Franka arm driver over franky, which runs libfranka's 1 kHz loop in C++.

Python only sets joint targets. They stream into a joint impedance controller with
DROID's own gains, so the arm tracks a policy's targets the way DROID's data was
collected. FR3 and Panda share this driver and differ only in joint limits and in the
libfranka build franky bundles.
"""

from __future__ import annotations

import re
import sys
import time
from dataclasses import dataclass
from importlib import metadata

import numpy as np

from dreamscale.hardware.rig import RigFault

# Joint position limits in radians, from Franka's datasheets.
ARM_LIMITS = {
    "fr3": (
        (-2.7437, -1.7837, -2.9007, -3.0421, -2.8065, 0.5445, -3.0159),
        (2.7437, 1.7837, 2.9007, -0.1518, 2.8065, 4.5169, 3.0159),
    ),
    "panda": (
        (-2.8973, -1.7628, -2.8973, -3.0718, -2.8973, -0.0175, -2.8973),
        (2.8973, 1.7628, 2.8973, -0.0698, 2.8973, 3.7525, 2.8973),
    ),
}
# Commands stay this far inside the datasheet limits, short of the robot's own reflex.
LIMIT_MARGIN = 0.05
# The FCI protocol version each franky 2.0.0 libfranka build speaks, measured against
# the robot's handshake. The default PyPI wheel bundles libfranka 0.21.2.
FRANKY_VERSION = "2.0.0"
DEFAULT_LIBFRANKA = "0.21.2"
FCI_PROTOCOLS = {
    "0.7.1": 3, "0.8.0": 4, "0.9.2": 5, "0.12.1": 6, "0.13.3": 7, "0.14.2": 8,
    "0.17.0": 9, "0.21.2": 10,
}
_WHEELS = "https://github.com/TimSchneider42/franky/releases/download/v{franky}/"
_VERSIONS = re.compile(r"server version:\s*(\d+),\s*library version:\s*(\d+)")
# Contact sensitivity: lower thresholds stop sooner on contact.
TORQUE_THRESHOLDS = (20.0, 20.0, 18.0, 18.0, 16.0, 14.0, 12.0)
FORCE_THRESHOLDS = (20.0, 20.0, 20.0, 25.0, 25.0, 25.0)
# DROID's FR3 controller (droid/config/fr3/franka_hardware.yaml): polymetis's hybrid
# joint/Cartesian impedance, the gains its data was collected with. Streaming a target
# every 1/15 s into one torque-level controller, not a new position motion each time,
# is also what keeps libfranka's motion-discontinuity reflex out of the way.
DROID_IMPEDANCE = {
    "stiffness": (40.0, 30.0, 50.0, 25.0, 35.0, 25.0, 10.0),
    "damping": (4.0, 6.0, 5.0, 5.0, 3.0, 2.0, 1.0),
    "cartesian_stiffness": (400.0, 400.0, 400.0, 15.0, 15.0, 15.0),
    "cartesian_damping": (37.0, 37.0, 37.0, 2.0, 2.0, 2.0),
}
# Homing is a separate, slow move to DROID's reset pose, outside any policy run.
HOME_DYNAMICS_FACTOR = 0.1


class FrankaArmError(RigFault):
    """The arm refused, faulted or could not be reached."""


class IncompatibleFirmware(FrankaArmError):
    def __init__(self, server: int, library: int):
        self.server, self.library = server, library
        super().__init__(
            f"This robot speaks FCI protocol {server}; the installed franky build speaks "
            f"{library}. {install_hint(server)}"
        )


def joint_limits(model: str) -> np.ndarray:
    """7 x 2 command limits with the safety margin applied."""
    lower, upper = ARM_LIMITS[model]
    return np.column_stack([np.asarray(lower) + LIMIT_MARGIN, np.asarray(upper) - LIMIT_MARGIN])


def installed_libfranka() -> str | None:
    """The libfranka inside the installed franky, from its local version label."""
    try:
        version = metadata.version("franky-control")
    except metadata.PackageNotFoundError:
        return None
    _, _, local = version.partition("+")
    return local.removeprefix("libfranka.") if local else DEFAULT_LIBFRANKA


def wheel_url(libfranka: str, *, python=None) -> str:
    major, minor = python or sys.version_info[:2]
    tag = f"cp{major}{minor}"
    local = "" if libfranka == DEFAULT_LIBFRANKA else f"+libfranka.{libfranka}"
    return (
        _WHEELS.format(franky=FRANKY_VERSION)
        + f"franky_control-{FRANKY_VERSION}{local}-{tag}-{tag}-manylinux_2_34_x86_64.whl"
    )


def install_hint(server: int) -> str:
    builds = [build for build, protocol in FCI_PROTOCOLS.items() if protocol == server]
    if not builds:
        return (
            f"No franky {FRANKY_VERSION} build speaks protocol {server}. Check the robot's "
            "system version in Desk against Franka's libfranka compatibility table."
        )
    from dreamscale.extras import _uv_tool

    url = wheel_url(builds[-1])
    install = (
        f"uv pip install --python {sys.executable} --reinstall '{url}'" if _uv_tool()
        else f"{sys.executable} -m pip install --force-reinstall --no-deps '{url}'"
    )
    return f"Install the libfranka {builds[-1]} build: {install}"


def parse_versions(message: str) -> tuple[int, int] | None:
    match = _VERSIONS.search(str(message))
    return (int(match[1]), int(match[2])) if match else None


@dataclass(frozen=True)
class ArmState:
    position: np.ndarray
    velocity: np.ndarray
    mode: str
    errors: str | None
    timestamp: float  # time.monotonic()

    def validate(self, max_age_s: float) -> ArmState:
        if self.position.shape != (7,) or not np.isfinite(self.position).all():
            raise FrankaArmError("Arm returned invalid joint positions.")
        if time.monotonic() - self.timestamp > max_age_s:
            raise FrankaArmError("Arm state is stale. Check the FCI cable.")
        if self.errors:
            raise FrankaArmError(
                f"Arm reports {self.errors}. Clear the cause, then run dreamscale robots "
                "franka recover."
            )
        if self.mode not in ("Idle", "Move"):
            raise FrankaArmError(_mode_help(self.mode))
        return self


def _mode_help(mode: str) -> str:
    return {
        "UserStopped": "Arm is user-stopped. Release the enabling device or E-stop.",
        "Reflex": "Arm stopped on a reflex. Clear the cause, then run dreamscale robots "
        "franka recover.",
        "Guiding": "Arm is in guiding mode. Release the pilot buttons.",
        "Other": "Arm joints are locked or FCI is off. In Desk, unlock the joints and "
        "activate FCI.",
        "AutomaticErrorRecovery": "Arm is recovering from an error. Wait, then retry.",
    }.get(mode, f"Arm is in mode {mode}; it must be Idle.")


def _errors_text(errors) -> str | None:
    """libfranka's active errors as text, or None. An empty Errors prints as []."""
    text = str(errors).strip()
    if not errors or not text or text in {"[]", "{}", "None"}:
        return None
    return text


class FrankyArm:
    """One FCI connection. Never moves until follow(), move_to() or hold() is called."""

    def __init__(self, host: str, model: str, *, franky=None, realtime: bool = True):
        if model not in ARM_LIMITS:
            raise ValueError(f"Unknown arm model {model}.")
        self.host, self.model = host, model
        self.limits = joint_limits(model)
        self.realtime = realtime
        self._tracker = None
        self._franky = franky
        self.robot = None
        self.holds_after_close = False

    @property
    def franky(self):
        if self._franky is None:
            import franky

            self._franky = franky
        return self._franky

    def connect(self) -> FrankyArm:
        fk = self.franky
        config = fk.RealtimeConfig.Enforce if self.realtime else fk.RealtimeConfig.Ignore
        try:
            robot = fk.Robot(self.host, realtime_config=config)
        except fk.IncompatibleVersionException as exc:
            versions = parse_versions(exc)
            if versions is None:
                raise FrankaArmError(str(exc)) from exc
            raise IncompatibleFirmware(*versions) from exc
        except fk.NetworkException as exc:
            raise FrankaArmError(
                f"Can't reach the arm's FCI at {self.host}. Check the cable to the control "
                "box and that FCI is activated in Desk."
            ) from exc
        robot.set_collision_behavior(list(TORQUE_THRESHOLDS), list(FORCE_THRESHOLDS))
        self.robot = robot
        return self

    def _require(self):
        if self.robot is None:
            raise FrankaArmError("Arm is not connected.")
        return self.robot

    def snapshot(self) -> ArmState:
        state = self._require().state
        return ArmState(
            position=np.asarray(state.q, dtype=float).reshape(7),
            velocity=np.asarray(state.dq, dtype=float).reshape(7),
            mode=getattr(state.robot_mode, "name", str(state.robot_mode)),
            errors=_errors_text(state.current_errors),
            timestamp=time.monotonic(),
        )

    def follow(self, target) -> np.ndarray:
        """Track target from wherever the arm is now; returns the target sent."""
        fk, robot = self.franky, self._require()
        target = np.asarray(target, dtype=float)
        try:
            if self._tracker is None or not _running(self._tracker):
                lower, upper = (np.asarray(v, dtype=float) for v in ARM_LIMITS[self.model])
                self._tracker = fk.JointImpedanceTracker(
                    robot, **{k: np.asarray(v) for k, v in DROID_IMPEDANCE.items()},
                    lower_joint_limits=lower, upper_joint_limits=upper,
                )
            self._tracker.set_target(target)
        except fk.Exception as exc:
            raise FrankaArmError(f"Arm refused the target: {exc}") from exc
        return target

    def move_to(self, target, *, dynamics_factor: float = HOME_DYNAMICS_FACTOR) -> None:
        """Blocking, slow move to target, for homing."""
        fk, robot = self.franky, self._require()
        motion = fk.JointMotion(
            fk.JointState(np.asarray(target, dtype=float)),
            relative_dynamics_factor=dynamics_factor,
        )
        try:
            robot.move(motion)
        except fk.Exception as exc:
            raise FrankaArmError(f"Homing stopped: {exc}") from exc

    def hold(self) -> bool:
        """Bring any running motion to a smooth stop. True once the arm is idle and clean.

        With no motion running, the robot's own controller holds its pose.
        """
        fk, robot = self.franky, self._require()
        try:
            self._stop_motion()
        except fk.Exception:
            return False
        state = self.snapshot()
        return not robot.is_in_control and state.errors is None and state.mode == "Idle"

    def _stop_motion(self, robot=None):
        """Bring whatever runs to rest, whichever kind of motion it is.

        libfranka stops a motion only with a stop of its own control type: a torque stop
        for the tracker, a joint stop for homing. Ours are known; anything else running
        on this connection gets the other kind when the first is refused.
        """
        robot = robot or self._require()
        fk = self.franky
        tracker, self._tracker = self._tracker, None
        if tracker is not None and _running(tracker):
            tracker.stop()
        elif robot.is_in_control:
            stops = [fk.JointStopMotion, getattr(fk, "TorqueStopMotion", None)]
            for stop in filter(None, stops):
                try:
                    robot.move(stop())
                    break
                except getattr(fk, "InvalidMotionTypeException", ()):
                    continue
        robot.join_motion(timeout=2.0)

    def recover(self) -> bool:
        return bool(self._require().recover_from_errors())

    def close(self) -> None:
        robot, self.robot = self.robot, None
        if robot is None:
            return
        fk = self.franky
        try:
            self._stop_motion(robot)
        except fk.Exception as exc:
            raise FrankaArmError(f"Arm stop on disconnect unconfirmed: {exc}") from exc


def _running(tracker) -> bool:
    running = tracker.is_running
    return bool(running() if callable(running) else running)
