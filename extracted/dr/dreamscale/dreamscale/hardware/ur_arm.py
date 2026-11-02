"""The Universal Robots arm driver over ur_rtde: RTDE for state, External Control for motion.

PolyScope X takes motion from another computer only through UR's External Control URCapX:
a pendant program whose External Control node runs the script ur_rtde serves. Python
streams joint targets into servoj from its own 125 Hz thread, moving linearly from the
last commanded pose to each new target over the interval between targets, so the arm
moves smoothly at whatever rate a policy sends.
"""

from __future__ import annotations

import math
import threading
import time
from dataclasses import dataclass

import numpy as np

from dreamscale.hardware.rig import RigFault
from dreamscale.hardware.ur_robot_api import RobotAPI, RobotAPIError

# Commands stay this far inside each joint's range.
LIMIT_MARGIN = 0.05
SERVO_PERIOD_S = 1 / 125
# servoj smoothing: lookahead in [0.03, 0.2] s and a proportional gain in [100, 2000].
LOOKAHEAD_S = 0.1
GAIN = 300
# A new target is reached over the interval since the previous one, within these bounds.
MIN_STEP_S = 0.02
MAX_STEP_S = 0.25
# Homing: a slow joint move outside any policy run.
HOME_SPEED = 0.3  # rad/s on a UR7e, less on a longer arm (speed_scale)
HOME_ACCELERATION = 0.5  # rad/s²
STOP_DECELERATION = 2.0  # rad/s²
MOVE_POLL_S = 0.02
MOVE_STATE_AGE_S = 0.25
MOVE_REPORT_S = 0.2
# The pendant program holding the External Control node, played remotely in Remote control.
DEFAULT_PROGRAM = "dreamscale"
# How long a connection waits for the operator to press Play on the External Control program.
CONTROL_TIMEOUT_S = 180.0

# RTDE robot_mode and safety_mode values.
ROBOT_RUNNING = 7
_ROBOT_MODES = {
    -1: "has no controller", 0: "is disconnected", 1: "is waiting for safety confirmation",
    2: "is booting", 3: "is powered off", 4: "is powered on with brakes engaged",
    5: "is idle with brakes engaged", 6: "is in backdrive", 8: "is updating firmware",
}
SAFETY_OK = (1, 2)  # normal, reduced
_SAFETY_MODES = {
    3: "is protective-stopped", 4: "is in safety recovery", 5: "is safeguard-stopped",
    6: "is emergency-stopped (system)", 7: "is emergency-stopped", 8: "reports a safety "
    "violation", 9: "reports a safety fault", 12: "is safeguard-stopped (automatic mode)",
    13: "is stopped by the three-position enabling device",
}


DH_ALPHA = (math.pi / 2, 0.0, 0.0, math.pi / 2, -math.pi / 2, 0.0)


@dataclass(frozen=True)
class ArmModel:
    """What differs between UR models for this driver: kinematics, for describing a pose,
    and joint speeds. Every joint turns ±360° except the elbow, which the upper arm stops
    at ±180°; a UR3e's wrist 3 turns endlessly, but commands stay within ±360° anyway."""

    label: str
    dh_d: tuple[float, ...]  # standard DH, metres (UR's published values)
    dh_a: tuple[float, ...]
    max_speed: tuple[float, ...]  # each joint's top speed, rad/s

    @property
    def lever(self) -> float:
        """Shoulder to wrist, metres: how far a shoulder turn swings the tool."""
        return abs(self.dh_a[1]) + abs(self.dh_a[2])


def _speeds(*degrees_per_s) -> tuple[float, ...]:
    return tuple(math.radians(v) for v in degrees_per_s)


_E_SMALL = _speeds(180, 180, 180, 180, 180, 180)
_E_LARGE = _speeds(120, 120, 180, 180, 180, 180)
_UR_SERIES = _speeds(180, 180, 240, 300, 300, 300)
_UR_HEAVY = _speeds(120, 120, 150, 210, 210, 210)
_UR5E = ((0.1625, 0.0, 0.0, 0.1333, 0.0997, 0.0996), (0.0, -0.425, -0.3922, 0.0, 0.0, 0.0))
_UR10E_D = (0.1807, 0.0, 0.0, 0.17415, 0.11985, 0.11655)
_UR15_D = (0.2186, 0.0, 0.0, 0.1824, 0.1361, 0.1434)
_UR20_D = (0.2363, 0.0, 0.0, 0.201, 0.1593, 0.1543)
# UR's e-Series and UR Series arms, from Universal_Robots_ROS2_Description. A UR7e is a UR5e
# and a UR12e a UR10e, each with more payload.
ARM_SPECS = {
    "ur3e": ArmModel(
        "UR3e", (0.15185, 0.0, 0.0, 0.13105, 0.08535, 0.0921),
        (0.0, -0.24355, -0.2132, 0.0, 0.0, 0.0), _speeds(180, 180, 180, 360, 360, 360),
    ),
    "ur5e": ArmModel("UR5e", *_UR5E, _E_SMALL),
    "ur7e": ArmModel("UR7e", *_UR5E, _E_SMALL),
    "ur10e": ArmModel("UR10e", _UR10E_D, (0.0, -0.6127, -0.57155, 0.0, 0.0, 0.0), _E_LARGE),
    "ur12e": ArmModel("UR12e", _UR10E_D, (0.0, -0.6127, -0.57155, 0.0, 0.0, 0.0), _E_LARGE),
    "ur16e": ArmModel("UR16e", _UR10E_D, (0.0, -0.4784, -0.36, 0.0, 0.0, 0.0), _E_LARGE),
    "ur8long": ArmModel("UR8 Long", _UR15_D, (0.0, -0.8989, -0.7149, 0.0, 0.0, 0.0), _UR_SERIES),
    "ur15": ArmModel("UR15", _UR15_D, (0.0, -0.6475, -0.5164, 0.0, 0.0, 0.0), _UR_SERIES),
    "ur18": ArmModel("UR18", _UR15_D, (0.0, -0.475, -0.3389, 0.0, 0.0, 0.0), _UR_SERIES),
    "ur20": ArmModel("UR20", _UR20_D, (0.0, -0.862, -0.7287, 0.0, 0.0, 0.0), _UR_HEAVY),
    "ur30": ArmModel("UR30", _UR20_D, (0.0, -0.637, -0.5037, 0.0, 0.0, 0.0), _UR_HEAVY),
}
ARM_MODELS = tuple(ARM_SPECS)
# Speed and tracking caps were validated on a UR7e; on a longer arm they shrink so the tool
# moves no faster than it would there.
REFERENCE_MODEL = "ur7e"
_JOINT_RANGE = np.array([2 * math.pi, 2 * math.pi, math.pi, 2 * math.pi, 2 * math.pi, 2 * math.pi])


def arm_spec(model: str) -> ArmModel:
    try:
        return ARM_SPECS[model]
    except KeyError:
        raise ValueError(
            f"Unknown arm model {model}. Supported: {', '.join(ARM_MODELS)}."
        ) from None


def speed_scale(model: str) -> float:
    """At most 1: the reference arm's shoulder-to-wrist length over this arm's."""
    return min(1.0, ARM_SPECS[REFERENCE_MODEL].lever / arm_spec(model).lever)


def flange_pose(q, model: str = REFERENCE_MODEL) -> np.ndarray:
    """4x4 base-to-flange transform for joints q (radians), within a millimetre or so."""
    spec = arm_spec(model)
    T = np.eye(4)
    for theta, d, a, alpha in zip(q, spec.dh_d, spec.dh_a, DH_ALPHA, strict=True):
        ct, st, ca, sa = math.cos(theta), math.sin(theta), math.cos(alpha), math.sin(alpha)
        T = T @ np.array([
            [ct, -st * ca, st * sa, a * ct],
            [st, ct * ca, -ct * sa, a * st],
            [0.0, sa, ca, d],
            [0.0, 0.0, 0.0, 1.0],
        ])
    return T


class URArmError(RigFault):
    """The arm refused, faulted or could not be reached."""


def joint_limits(model: str) -> np.ndarray:
    """6 x 2 command limits with the safety margin applied."""
    arm_spec(model)
    bound = _JOINT_RANGE - LIMIT_MARGIN
    return np.stack([-bound, bound], axis=1)


@dataclass(frozen=True)
class ArmState:
    position: np.ndarray
    velocity: np.ndarray
    robot_mode: int
    safety_mode: int
    timestamp: float  # time.monotonic()

    def validate(self, max_age_s: float) -> ArmState:
        if self.position.shape != (6,) or not np.isfinite(self.position).all():
            raise URArmError("Arm returned invalid joint positions.")
        if time.monotonic() - self.timestamp > max_age_s:
            raise URArmError("Arm state is stale. Check the Ethernet cable to the control box.")
        if self.safety_mode not in SAFETY_OK:
            raise URArmError(_safety_help(self.safety_mode))
        if self.robot_mode != ROBOT_RUNNING:
            raise URArmError(
                f"Arm {_ROBOT_MODES.get(self.robot_mode, f'is in mode {self.robot_mode}')}. "
                "Power it on and release the brakes on the pendant."
            )
        return self


def _safety_help(mode: int) -> str:
    what = _SAFETY_MODES.get(mode, f"is in safety mode {mode}")
    return f"Arm {what}. Clear the cause, then unlock it on the pendant."


class URArm:
    """One RTDE connection, plus motion once connected with control. Never moves until
    follow(), move_to() is called."""

    def __init__(
        self, host: str, model: str, *, program: str = DEFAULT_PROGRAM, rtde=None,
        robot_api=RobotAPI, control_timeout_s=CONTROL_TIMEOUT_S,
    ):
        self.host, self.model, self.program = host, model, program
        self._robot_api = robot_api
        self.started_program = False
        self.limits = joint_limits(model)
        self.speed_scale = speed_scale(model)
        self.control_timeout_s = control_timeout_s
        self._rtde = rtde
        self.receive = self.control = None
        self._servo = None
        self._move_started = 0.0

    @property
    def rtde(self):
        """The (rtde_receive, rtde_control) modules, imported on first use."""
        if self._rtde is None:
            import rtde_control
            import rtde_receive

            self._rtde = (rtde_receive, rtde_control)
        return self._rtde

    def connect(self, *, control: bool = True) -> URArm:
        """RTDE state always; with control, wait for the pendant's External Control program."""
        rtde_receive, rtde_control = self.rtde
        try:
            self.receive = rtde_receive.RTDEReceiveInterface(self.host)
        except Exception as exc:
            raise URArmError(
                f"Can't reach the arm's RTDE at {self.host}. Check the Ethernet link, and "
                "that RTDE is enabled under Settings > Security > Services on the pendant."
            ) from exc
        if control:
            interface = rtde_control.RTDEControlInterface
            # External Control: ur_rtde serves its script on 50002 for the pendant's node to
            # fetch. (FLAG_UPLOAD_SCRIPT would upload it over port 30003 instead, which
            # PolyScope X won't run outside remote control.) NO_WAIT returns at once, so the
            # wait for Play is ours, not ur_rtde's fixed 60 s.
            flags = interface.FLAG_USE_EXT_UR_CAP | interface.FLAG_NO_WAIT
            try:
                self.control = interface(self.host, -1.0, flags)
            except Exception as exc:
                self.close()
                raise URArmError(f"Couldn't start External Control: {exc}") from exc
            if not self.control.isProgramRunning():
                try:
                    self._play_remotely()
                except BaseException:
                    self.close()
                    raise
            deadline = time.monotonic() + self.control_timeout_s
            while not self.control.isProgramRunning():
                if time.monotonic() > deadline:
                    self.close()
                    raise URArmError(
                        "The arm didn't take control. On the pendant, press Play on the "
                        f"{self.program} program (its External Control node points at this "
                        "computer), or switch the pendant to Remote control so this computer "
                        "can."
                    )
                time.sleep(0.05)
        return self

    def _play_remotely(self) -> None:
        """In Remote control, load and play the External Control program ourselves."""
        api = self._robot_api(self.host)
        if not api.remote_control():
            return  # Local control (or no Robot API): the operator presses Play.
        try:
            if api.loaded_program() != self.program:
                api.load(self.program)
            state = api.program_state()
            if state != "STOPPED":
                raise URArmError(
                    f"The {self.program} program is {state.lower()} but isn't running this "
                    "computer's script. Stop it on the pendant, then try again."
                )
            api.play()
        except RobotAPIError as exc:
            # PolyScope X validates the External Control node's cached copy of our script;
            # a stale copy makes the whole program invalid for remote play.
            hint = (
                " In Local control, press Update program on its External Control node while "
                "this computer waits for Play, then switch back to Remote."
                if "not valid" in str(exc) else ""
            )
            raise URArmError(
                f"Couldn't start the {self.program} program remotely: {exc}.{hint}"
            ) from exc
        self.started_program = True

    def snapshot(self) -> ArmState:
        receive = self._require_receive()
        try:
            position = np.asarray(receive.getActualQ(), dtype=float).reshape(6)
            velocity = np.asarray(receive.getActualQd(), dtype=float).reshape(6)
            robot_mode, safety_mode = int(receive.getRobotMode()), int(receive.getSafetyMode())
        except Exception as exc:
            raise URArmError(f"Arm state unavailable: {exc}") from exc
        return ArmState(position, velocity, robot_mode, safety_mode, time.monotonic())

    def follow(self, target) -> np.ndarray:
        """Track target from the last commanded pose; returns the target sent."""
        control = self._require_control()
        target = np.asarray(target, dtype=float).reshape(6)
        if self._servo is None or not self._servo.alive:
            if self._servo is not None and self._servo.error is not None:
                raise URArmError(f"Arm stopped following: {self._servo.error}")
            self._servo = _ServoThread(control, self.snapshot().position)
            self._servo.start()
        self._servo.set_target(target)
        return target

    def start_move(self, target, *, speed=None, acceleration=HOME_ACCELERATION) -> None:
        """Begin a slow joint move to target, for homing; moving() reports when it ends."""
        control = self._require_control()
        speed = HOME_SPEED * self.speed_scale if speed is None else speed
        self._stop_servo(control)
        # Asynchronous, so the caller can stop it part way: a blocking moveJ can't be
        # interrupted from Python.
        if not control.moveJ([float(v) for v in target], speed, acceleration, True):
            raise URArmError("The arm refused the move. Check the pendant for a protective stop.")
        self._move_started = time.monotonic()

    def moving(self) -> bool:
        """True while a start_move() runs; raises if the arm faults meanwhile."""
        control = self._require_control()
        self.snapshot().validate(MOVE_STATE_AGE_S)
        if control.getAsyncOperationProgressEx().isAsyncOperationRunning():
            return True
        # The script may report the move a moment after accepting it.
        return time.monotonic() - self._move_started < MOVE_REPORT_S

    def stop_move(self) -> None:
        """Decelerate out of a start_move()."""
        control = self._require_control()
        if control.isProgramRunning():
            control.stopJ(STOP_DECELERATION)

    def move_to(self, target, *, speed=None, acceleration=HOME_ACCELERATION) -> None:
        """Blocking slow joint move to target; any interruption stops the arm."""
        self.start_move(target, speed=speed, acceleration=acceleration)
        try:
            while self.moving():
                time.sleep(MOVE_POLL_S)
        except BaseException:
            self.stop_move()
            raise

    def hold(self) -> bool:
        """Stop any streaming motion. True once the arm is still, powered and safe."""
        if self.control is None:
            return False
        try:
            self._stop_servo(self.control)
            state = self.snapshot()
        except Exception:
            return False
        return state.safety_mode in SAFETY_OK and state.robot_mode == ROBOT_RUNNING and bool(
            np.max(np.abs(state.velocity)) < 0.01
        )

    def _stop_servo(self, control) -> None:
        servo, self._servo = self._servo, None
        if servo is not None:
            servo.stop()
        control.servoStop(STOP_DECELERATION)
        deadline = time.monotonic() + 2.0
        while time.monotonic() < deadline:
            if np.max(np.abs(self.snapshot().velocity)) < 0.01:
                return
            time.sleep(0.01)

    def _require_receive(self):
        if self.receive is None:
            raise URArmError("Arm is not connected.")
        return self.receive

    def _require_control(self):
        if self.control is None:
            raise URArmError("Arm is connected read-only.")
        return self.control

    def close(self) -> None:
        errors = []
        control, self.control = self.control, None
        if control is not None:
            try:
                if self._servo is not None:
                    self._servo.stop()
                    self._servo = None
                # Commands wait on the robot's script; with none running they'd never return.
                if control.isProgramRunning():
                    control.servoStop(STOP_DECELERATION)
                    control.stopScript()
                control.disconnect()
            except Exception as exc:
                errors.append(str(exc))
            if self.started_program:
                self.started_program = False
                try:  # ending our script ends the program; make sure it isn't left playing
                    api = self._robot_api(self.host)
                    if api.program_state() != "STOPPED":
                        api.stop()
                except Exception as exc:
                    errors.append(f"program stop: {exc}")
        receive, self.receive = self.receive, None
        if receive is not None:
            try:
                receive.disconnect()
            except Exception as exc:
                errors.append(str(exc))
        if errors:
            raise URArmError("Arm stop on disconnect unconfirmed: " + "; ".join(errors))


class _ServoThread:
    """servoj at 125 Hz toward the latest target, linear from the last commanded pose."""

    def __init__(self, control, start):
        self.control = control
        self.commanded = np.asarray(start, dtype=float)
        self._from = self.commanded.copy()
        self._to = self.commanded.copy()
        self._began = self._last_target = time.monotonic()
        self._duration = MAX_STEP_S
        self._lock = threading.Lock()
        self._running = False
        self._thread = None
        self.error = None

    @property
    def alive(self) -> bool:
        return self._running and self.error is None

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._loop, name="ur-servo", daemon=True)
        self._thread.start()

    def set_target(self, target):
        now = time.monotonic()
        with self._lock:
            self._from, self._to = self.commanded.copy(), np.asarray(target, dtype=float)
            self._duration = min(MAX_STEP_S, max(MIN_STEP_S, now - self._last_target))
            self._began = self._last_target = now

    def _loop(self):
        control = self.control
        while self._running:
            started = control.initPeriod()
            with self._lock:
                fraction = min(1.0, (time.monotonic() - self._began) / self._duration)
                self.commanded = self._from + fraction * (self._to - self._from)
                q = self.commanded.tolist()
            try:
                if not control.servoJ(q, 0.0, 0.0, SERVO_PERIOD_S, LOOKAHEAD_S, GAIN):
                    self.error = "the robot program stopped (check the pendant)"
                    self._running = False
                    return
            except Exception as exc:
                self.error = str(exc)
                self._running = False
                return
            control.waitPeriod(started)

    def stop(self):
        self._running = False
        if self._thread is not None and self._thread is not threading.current_thread():
            self._thread.join(timeout=1.0)
