"""The UFACTORY xArm 7 driver over xarm-python-sdk, with its xArm Gripper.

Motion uses the controller's mode 6 (online joint trajectory planning): each target replaces
the last and the controller plans to it within a speed and acceleration cap, so the arm
moves smoothly at whatever rate a policy sends. These are the settings a bimanual xArm 7
bench has run its teleop and π0.5 policies with (0.5 rad/s, 2 rad/s²).

The gripper's reading is the URDF ``drive_joint`` angle, 0 rad open to 0.85 rad closed,
which is what recordings on these arms store as state. Its command is a close intent from 0
(open) to 1 (closed). By default the jaw moves to that fraction of its travel (``position``);
a rig file can instead close it at or past one half and open it below (``threshold``).
"""

from __future__ import annotations

import contextlib
import io
import math
import threading
import time
import warnings
from dataclasses import dataclass

import numpy as np

from dreamscale.hardware.rig import RigFault

JOINTS = 7
# UFACTORY's xArm 7 URDF joint limits, radians; commands stay LIMIT_MARGIN inside them.
JOINT_LOWER = (-2 * math.pi, -2.059, -2 * math.pi, -0.19198, -2 * math.pi, -1.69297, -2 * math.pi)
JOINT_UPPER = (2 * math.pi, 2.0944, 2 * math.pi, 3.927, 2 * math.pi, math.pi, 2 * math.pi)
LIMIT_MARGIN = 0.02
# Mode-6 planner caps while a policy drives, and for homing.
SPEED = 0.5  # rad/s
ACCELERATION = 2.0  # rad/s²
HOME_SPEED = 0.3
MOVE_POLL_S = 0.02
# Joint speed below which the arm counts as still, rad/s.
STILL = 0.01
HOLD_TIMEOUT_S = 2.0
# Controller modes and states (xarm-python-sdk set_mode / set_state).
MODE_ONLINE_JOINT = 6
STATE_READY = 0
STATES_OK = (1, 2)  # in motion, ready
STATE_TEXT = {3: "is paused", 4: "is stopped", 5: "is stopped", 6: "is decelerating to a stop"}

# The gripper: drive_joint radians against what the SDK reads.
GRIPPER_CLOSED_RAD = 0.85
G2_OPEN_MM = 84.0
G1_OPEN_PULSE = 850.0
G2_SPEED_MMPS = 100
G2_FORCE = 75  # % of the G2's current limit, about 40 N
G1_SPEED = 3000  # pulses/s
CLOSE_AT = 0.5
# How a close intent drives the jaw: to that fraction of its travel, or shut past CLOSE_AT.
GRIPPER_CONTROLS = ("position", "threshold")
# A position command smaller than this fraction of the jaw's travel isn't sent.
GRIPPER_DEADBAND = 0.025
GRIPPER_TYPES = ("g2", "g1", "none")
GRIPPER_LABELS = {"g2": "xArm Gripper G2", "g1": "xArm Gripper", "none": "None"}
# The gripper is read at most this often; reads are TCP round trips on the arm's link.
GRIPPER_READ_S = 0.03


class XArmError(RigFault):
    """The arm refused, faulted or could not be reached."""


def joint_limits() -> np.ndarray:
    """7 x 2 command limits with the safety margin applied."""
    return np.stack(
        [np.array(JOINT_LOWER) + LIMIT_MARGIN, np.array(JOINT_UPPER) - LIMIT_MARGIN], axis=1
    )


def _api_factory(host: str):
    # xarm-python-sdk prints its version, the controller's details and protocol changes on
    # stdout, and its blockly tools raise a SyntaxWarning on first import; none of it is ours.
    with contextlib.redirect_stdout(io.StringIO()), warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        from xarm.wrapper import XArmAPI

        return XArmAPI(host, is_radian=True)


@dataclass(frozen=True)
class ArmState:
    position: np.ndarray
    velocity: np.ndarray
    error_code: int
    warn_code: int
    mode: int
    state: int
    timestamp: float  # time.monotonic()

    def validate(self, max_age_s: float, *, control: bool = True) -> ArmState:
        if self.position.shape != (JOINTS,) or not np.isfinite(self.position).all():
            raise XArmError("Arm returned invalid joint positions.")
        if time.monotonic() - self.timestamp > max_age_s:
            raise XArmError("Arm state is stale. Check the Ethernet cable to the control box.")
        if self.error_code:
            raise XArmError(
                f"Arm reports error C{self.error_code}. Check the cause, then clear it in "
                "UFACTORY Studio."
            )
        if control and self.mode != MODE_ONLINE_JOINT:
            raise XArmError(f"Arm left trajectory mode (mode {self.mode}). Reconnect to resume.")
        if control and self.state not in STATES_OK:
            raise XArmError(
                f"Arm {STATE_TEXT.get(self.state, f'is in state {self.state}')}. Check the "
                "E-stop and UFACTORY Studio, then reconnect."
            )
        return self


class XArm:
    """One xArm 7 controller connection. Never moves until follow() or start_move()."""

    def __init__(self, host: str, *, api_factory=_api_factory, speed=SPEED,
                 acceleration=ACCELERATION):
        self.host = host
        self.limits = joint_limits()
        self.speed, self.acceleration = speed, acceleration
        self._api_factory = api_factory
        self.api = None
        self.control = False
        self._move_target = None
        self._lock = threading.Lock()

    def connect(self, *, control: bool = True) -> XArm:
        """State always; with control, enable motion in mode 6 at the current pose."""
        try:
            self.api = self._api_factory(self.host)
        except ImportError:
            raise
        except Exception as exc:
            raise XArmError(
                f"Can't reach the xArm controller at {self.host}. Check the Ethernet link and "
                "that this computer has an address on the arm's network."
            ) from exc
        if not getattr(self.api, "connected", False):
            self.api = None
            raise XArmError(
                f"Can't reach the xArm controller at {self.host}. Check the Ethernet link and "
                "that this computer has an address on the arm's network."
            )
        if control:
            try:
                state = self.snapshot()
                if state.error_code:
                    raise XArmError(
                        f"Arm reports error C{state.error_code}. Check the cause, then clear "
                        "it in UFACTORY Studio."
                    )
                api = self.api
                for code in (
                    api.motion_enable(enable=True),
                    api.set_mode(MODE_ONLINE_JOINT),
                    api.set_state(STATE_READY),
                ):
                    if code:
                        raise XArmError(f"The arm refused to enable motion (code {code}).")
                deadline = time.monotonic() + 3.0
                while api.mode != MODE_ONLINE_JOINT or api.state not in STATES_OK:
                    if time.monotonic() > deadline:
                        raise XArmError(
                            "The arm didn't enter trajectory mode. Check the E-stop and that "
                            "UFACTORY Studio isn't running a program."
                        )
                    time.sleep(0.05)
                self.control = True
            except BaseException:
                self.close()
                raise
        return self

    def _require(self):
        if self.api is None:
            raise XArmError("Arm is not connected.")
        return self.api

    def snapshot(self) -> ArmState:
        api = self._require()
        with self._lock:
            try:
                code, states = api.get_joint_states(is_radian=True)
                if code:
                    raise XArmError(f"Arm state unavailable (code {code}).")
                position = np.asarray(states[0][:JOINTS], dtype=float)
                velocity = np.asarray(states[1][:JOINTS], dtype=float)
                error, warn = int(api.error_code), int(api.warn_code)
                mode, state = int(api.mode), int(api.state)
            except XArmError:
                raise
            except Exception as exc:
                raise XArmError(f"Arm state unavailable: {exc}") from exc
        return ArmState(position, velocity, error, warn, mode, state, time.monotonic())

    def follow(self, target, *, speed=None) -> np.ndarray:
        """Plan toward target (mode 6 replaces any earlier target); returns the target sent."""
        api = self._require()
        if not self.control:
            raise XArmError("Arm is connected read-only.")
        target = np.asarray(target, dtype=float).reshape(JOINTS)
        with self._lock:
            code = api.set_servo_angle(
                angle=[float(v) for v in target], speed=speed or self.speed,
                mvacc=self.acceleration, wait=False, is_radian=True,
            )
        if code:
            raise XArmError(f"The arm refused a target (code {code}). Check UFACTORY Studio.")
        return target

    def start_move(self, target, *, speed=HOME_SPEED) -> None:
        self.follow(target, speed=speed)
        self._move_target = np.asarray(target, dtype=float)

    def moving(self, tolerance=0.01) -> bool:
        state = self.snapshot().validate(0.5)
        offset = float(np.max(np.abs(state.position - self._move_target)))
        return offset > tolerance or float(np.max(np.abs(state.velocity))) > STILL

    def stop_move(self) -> None:
        self.hold()

    def hold(self) -> bool:
        """Target the measured pose. True once the arm is still, enabled and fault-free."""
        if self.api is None or not self.control:
            return False
        try:
            self.follow(self.snapshot().position)
            deadline = time.monotonic() + HOLD_TIMEOUT_S
            while True:
                state = self.snapshot()
                if state.error_code or state.state not in STATES_OK:
                    return False
                if float(np.max(np.abs(state.velocity))) < STILL:
                    return True
                if time.monotonic() > deadline:
                    return False
                time.sleep(MOVE_POLL_S)
        except Exception:
            return False

    def close(self) -> None:
        api, self.api = self.api, None
        self.control = False
        if api is None:
            return
        try:
            api.disconnect()
        except Exception as exc:
            raise XArmError(f"Arm disconnect unconfirmed: {exc}") from exc


class XArmGripper:
    """The arm's xArm Gripper (G2 or G1): drive_joint radians in, close intent out."""

    def __init__(self, arm: XArm, kind: str = "g2", *, control: str = "position",
                 clock=time.monotonic):
        if kind not in GRIPPER_TYPES:
            raise ValueError(f"Gripper type must be one of {', '.join(GRIPPER_TYPES)}.")
        if control not in GRIPPER_CONTROLS:
            raise ValueError(f"Gripper control must be one of {', '.join(GRIPPER_CONTROLS)}.")
        self.arm, self.kind, self.control, self.clock = arm, kind, control, clock
        self.closed = None  # the last command as a closed fraction 0-1; None until the first
        self._read_at, self._reading = -math.inf, 0.0

    def open(self) -> XArmGripper:
        if self.kind == "g1":
            api = self.arm._require()
            for code in (api.set_gripper_mode(0), api.set_gripper_enable(True),
                         api.set_gripper_speed(G1_SPEED)):
                if code:
                    raise XArmError(f"The gripper refused to enable (code {code}).")
        if self.kind != "none":
            self.state()
        return self

    def state(self) -> float:
        """drive_joint radians: 0 open, 0.85 closed."""
        if self.kind == "none":
            return 0.0
        now = self.clock()
        if now - self._read_at < GRIPPER_READ_S:
            return self._reading
        api = self.arm._require()
        if self.kind == "g2":
            code, value = api.get_gripper_g2_position()
            opening = float(value) / G2_OPEN_MM
        else:
            code, value = api.get_gripper_position()
            opening = float(value) / G1_OPEN_PULSE
        if code:
            raise XArmError(f"Gripper reading unavailable (code {code}). Check its cable.")
        self._reading = min(GRIPPER_CLOSED_RAD, max(0.0, GRIPPER_CLOSED_RAD * (1.0 - opening)))
        self._read_at = now
        return self._reading

    def command(self, intent: float) -> None:
        """Move the jaw to the intent's fraction of its travel (threshold: shut at or past
        CLOSE_AT, open below it); only a change past the deadband is sent."""
        intent = min(1.0, max(0.0, float(intent)))
        if self.control == "threshold":
            closed = 1.0 if intent >= CLOSE_AT else 0.0
        else:
            closed = intent
        # Fully open and fully shut are always sent, so the jaw reaches its end.
        unchanged = self.closed is not None and (
            closed == self.closed
            or (abs(closed - self.closed) < GRIPPER_DEADBAND and 0.0 < closed < 1.0)
        )
        if self.kind == "none" or unchanged:
            return
        api = self.arm._require()
        if self.kind == "g2":
            code = api.set_gripper_g2_position(
                G2_OPEN_MM * (1.0 - closed), speed=G2_SPEED_MMPS, force=G2_FORCE, wait=False,
            )
        else:
            code = api.set_gripper_position(G1_OPEN_PULSE * (1.0 - closed), wait=False)
        if code:
            raise XArmError(f"The gripper refused a command (code {code}).")
        self.closed = closed

    def close(self) -> None:
        pass
