"""SO-101 home pose and torque release for `dreamscale robots so101 home|release`.

Mirrors the YAM commands. `home --set` records a rest pose with the motors limp;
`home` moves there slowly and releases torque only once it arrives. A cancelled or
failed home leaves the motors holding, and `release` ends that hold after the
operator supports the arm.
"""

from __future__ import annotations

import json
import math
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

from dreamscale import errors
from dreamscale.config import load_config, save_config
from dreamscale.constants import EXEC_HZ, JOINT_NAMES
from dreamscale.motion.safety import clamp_step

# Every joint moves toward home at this speed, independently: a joint with farther to
# go simply takes longer. Paced against a fixed tick schedule, so bus latency slows
# homing down but never speeds a joint past it.
HOME_SPEED_DEG_S = 15.0
HOME_STEP_DEG = HOME_SPEED_DEG_S / EXEC_HZ
HOME_SETTLE_S = 1.0
HOME_TOLERANCE_DEG = 8.0
# A joint this far behind its setpoint is blocked (a wound wrist cable, an obstacle) or
# has cut its own torque; homing stops and holds instead of pushing into it.
HOME_LAG_LIMIT_DEG = 20.0
# The wrist_roll encoder wraps once per turn: one physical seam that position control
# cannot cross, so a target just past it is reached by turning the long way round,
# into the wrist cable. lerobot calibrates wrist_roll over the whole turn (seam at
# +/-180 degrees); calibrations that record its range (LeLab) shift the seam to where
# the encoder wraps relative to that range's midpoint.
WRIST_ROLL = JOINT_NAMES.index("wrist_roll")
WRIST_SEAM_MARGIN_DEG = 30.0
_ENCODER_MAX = 4095  # STS3215: 12-bit position


def _default_robot_factory() -> Any:
    from dreamscale.hardware.lerobot_so101 import create_so101
    from dreamscale.optional import require_so101_extra

    require_so101_extra()
    config = load_config()
    if config.robot_port is None:
        raise errors.catalog("robot_port_not_found", port="(none configured)")
    return create_so101(port=config.robot_port,
                        calibration_path=config.calibration_path,
                        include_camera=False)  # homing needs no camera


def run_set_home(*, robot_factory: Callable[[], Any] = _default_robot_factory,
                 input_fn: Callable[[str], str] = input,
                 print_fn: Callable[[str], None] = print) -> list[float] | None:
    """Record the pose the operator moves the limp arm to as home."""
    print_fn("Motors go limp so you can pose the arm by hand.")
    if not _confirm("Support the arm, then Enter · Ctrl+C to cancel: ", input_fn):
        return None
    robot = _open(robot_factory, bus_only=False, retry_command=f"{errors.COMMAND_HOME} --set")
    try:
        _require_calibrated(robot)
        robot.release_torque()
        print_fn("✓ Motor torque released")
        if not _confirm(
            "Pose the arm where it can rest with motors off, then Enter · Ctrl+C to cancel: ",
            input_fn,
        ):
            return None
        pose = [float(value) for value in robot.read_joint_positions()]
    finally:
        robot.disconnect()
    if not _valid_pose(pose):
        raise errors.catalog("so101_home_not_set",
                             detail=f"the arm reported an unusable pose: {pose}")
    config = load_config()
    wrist = pose[WRIST_ROLL]
    seam = _wrist_seam_deg(config.calibration_path)
    if min(seam - wrist, wrist - (seam - 360.0)) < WRIST_SEAM_MARGIN_DEG:
        raise errors.catalog(
            "so101_home_not_set",
            detail=(f"wrist_roll is at {wrist:+.0f}°, near its encoder seam "
                    f"({seam:+.0f}° = {seam - 360:+.0f}°); turn the wrist at least "
                    f"{WRIST_SEAM_MARGIN_DEG:.0f}° away from it, toward its middle"),
        )
    config.home_position = pose
    path = save_config(config)
    print_fn(f"✓ Home saved to {path}")
    return pose


def run_home(*, robot_factory: Callable[[], Any] = _default_robot_factory,
             input_fn: Callable[[str], str] = input,
             print_fn: Callable[[str], None] = print,
             sleep_fn: Callable[[float], None] = time.sleep) -> bool:
    """Move to the saved home pose, then release torque. True once home and limp."""
    home = load_config().home_position
    if home is None:
        raise errors.catalog("so101_home_not_set")
    if not _valid_pose(home):
        raise errors.catalog("so101_home_not_set",
                             detail="the saved home pose is invalid; record it again")
    home = [float(value) for value in home]
    print_fn("The arm moves to its home pose, then motors go limp. Clear the workspace.")
    if not _confirm("Enter to home · Ctrl+C to cancel: ", input_fn):
        return False
    robot = _open(robot_factory, bus_only=False, retry_command=errors.COMMAND_HOME)
    moved = released = False
    try:
        _require_calibrated(robot)
        wrist = robot.read_joint_positions()[WRIST_ROLL]
        if _crosses_wrist_seam(wrist, home):
            raise errors.catalog(
                "so101_wrist_seam",
                detail=(f"wrist_roll reads {wrist:+.0f}° and home is "
                        f"{home[WRIST_ROLL]:+.0f}°, on opposite sides of its encoder seam"),
            )
        print_fn("Homing… Ctrl+C to stop.")
        moved = True
        _move_to(robot, home, sleep_fn)
        name, off = max(
            zip(JOINT_NAMES, (abs(a - b) for a, b in
                              zip(robot.read_joint_positions(), home, strict=True)),
                strict=True),
            key=lambda pair: pair[1],
        )
        if off > HOME_TOLERANCE_DEG:
            raise errors.catalog("so101_home_not_reached",
                                 detail=f"{name} is {off:.0f}° from home")
        print_fn("✓ Home")
        robot.disconnect()
        released = True
        print_fn("✓ Motor torque released")
        return True
    except KeyboardInterrupt:
        print_fn("Stopped. The arm is holding its pose; support it, then run: "
                 f"{errors.COMMAND_RELEASE}")
        return False
    finally:
        if not released:
            # Never drop an arm mid-move: once motion starts, only `release` ends the hold.
            robot.disconnect(release_torque=not moved)


def run_release(*, robot_factory: Callable[[], Any] = _default_robot_factory,
                input_fn: Callable[[str], str] = input,
                print_fn: Callable[[str], None] = print) -> bool:
    """Release motor torque after the operator supports the arm."""
    print_fn("Support the arm. This releases motor torque.")
    if not _confirm("Enter to release · Ctrl+C to cancel: ", input_fn):
        return False
    robot = _open(robot_factory, bus_only=True, retry_command=errors.COMMAND_RELEASE)
    try:
        robot.release_torque()
    finally:
        robot.disconnect()
    print_fn("✓ Motor torque released")
    return True


def _move_to(robot: Any, home: list[float], sleep_fn: Callable[[float], None], *,
             clock: Callable[[], float] = time.monotonic) -> None:
    """Ramp every joint to `home` at HOME_SPEED_DEG_S, then hold it there to settle."""
    period = 1.0 / EXEC_HZ
    deadline = clock()

    def tick() -> None:
        # One HOME_STEP_DEG per period. A late tick resets the schedule instead of
        # catching up, which would send steps faster than the speed.
        nonlocal deadline
        deadline += period
        wait = deadline - clock()
        if wait > 0:
            sleep_fn(wait)
        else:
            deadline -= wait

    setpoint = [float(value) for value in robot.read_joint_positions()]
    while max(abs(target - value) for value, target in zip(setpoint, home, strict=True)) > 1e-6:
        measured = [float(value) for value in robot.read_joint_positions()]
        joint, lag = max(
            enumerate(abs(m - s) for m, s in zip(measured, setpoint, strict=True)),
            key=lambda pair: pair[1],
        )
        if lag > HOME_LAG_LIMIT_DEG:
            robot.send_joint_targets(measured)  # hold where it stopped, not where it was told
            raise errors.catalog(
                "so101_home_not_reached",
                detail=(f"{JOINT_NAMES[joint]} stopped following at {measured[joint]:+.0f}° "
                        f"({lag:.0f}° behind); something is blocking it or it cut its torque"),
            )
        setpoint = clamp_step(setpoint, home, HOME_STEP_DEG)
        robot.send_joint_targets(setpoint)
        tick()
    for _ in range(round(HOME_SETTLE_S * EXEC_HZ)):
        robot.send_joint_targets(home)
        tick()


def _open(robot_factory: Callable[[], Any], *, bus_only: bool, retry_command: str) -> Any:
    robot = robot_factory()
    port = load_config().robot_port or "the configured port"
    try:
        if bus_only:
            robot.connect_bus()
        else:
            robot.connect()
    except (ConnectionError, OSError) as exc:
        if _permission_denied(exc):
            raise errors.catalog("serial_permission_denied", port=port,
                                 retry_command=retry_command) from exc
        raise errors.catalog("robot_port_not_found", port=port) from exc
    return robot


def _permission_denied(exc: BaseException | None) -> bool:
    # lerobot wraps pyserial's "[Errno 13] Permission denied" in a ConnectionError.
    while exc is not None:
        if isinstance(exc, PermissionError) or "Permission denied" in str(exc):
            return True
        exc = exc.__cause__ or exc.__context__
    return False


def _require_calibrated(robot: Any) -> None:
    if not robot.is_calibrated():
        raise errors.catalog("calibration_mismatch",
                             detail="the arm's motors do not match the saved calibration")


def _crosses_wrist_seam(wrist: float, home: list[float]) -> bool:
    # Readings never wrap, so more than half a turn apart means the short way crosses
    # the seam, whatever the calibration.
    return abs(wrist - home[WRIST_ROLL]) > 180.0


def _seam_safe_home(robot: Any, home: list[float]) -> tuple[list[float], bool]:
    """Home, keeping wrist_roll where it is when reaching it would cross the seam.

    The second value says whether the wrist was left in place.
    """
    wrist = float(robot.read_joint_positions()[WRIST_ROLL])
    if not _crosses_wrist_seam(wrist, home):
        return home, False
    target = list(home)
    target[WRIST_ROLL] = wrist
    return target, True


def _wrist_seam_deg(calibration_path: str) -> float:
    """The positive side of wrist_roll's encoder seam, in calibrated degrees.

    lerobot maps raw position to (raw - mid) * 360 / 4095, mid being the calibrated
    range's midpoint, so the wrap at raw 4095|0 reads this and this minus 360.
    """
    try:
        wrist = json.loads(Path(calibration_path).expanduser().read_text())["wrist_roll"]
        mid = (float(wrist["range_min"]) + float(wrist["range_max"])) / 2
    except (OSError, ValueError, KeyError, TypeError):
        mid = _ENCODER_MAX / 2  # lerobot's own full-turn calibration
    return (_ENCODER_MAX - mid) * 360.0 / _ENCODER_MAX


def _confirm(prompt: str, input_fn: Callable[[str], str]) -> bool:
    try:
        while input_fn(prompt).strip():
            pass
    except (EOFError, KeyboardInterrupt):
        return False
    return True


def _valid_pose(pose: Any) -> bool:
    return (
        isinstance(pose, list)
        and len(pose) == len(JOINT_NAMES)
        and all(isinstance(value, int | float) and math.isfinite(value) for value in pose)
    )
