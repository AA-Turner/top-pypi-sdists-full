"""LeRobot 0.6.1 SO-101 adapter — the ONLY module that imports lerobot symbols,
so a lerobot API change is contained here (master/spec §8 isolation requirement).
"""

from __future__ import annotations

import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

import numpy as np

from dreamscale import errors
from dreamscale.constants import (
    CAMERA_KEY_SO101,
    CAMERA_KEY_SO101_SIDE,
    CAMERA_KEY_SO101_WRIST,
    JOINT_NAMES,
    OBS_FRAME_HEIGHT,
    OBS_FRAME_WIDTH,
)

# Measured on an SO-101: healthy servos drift 0 counts in the 300 ms after torque comes
# on with goal == present; a latched wrist_roll moved 42 counts in the first 100 ms.
RUNAWAY_COUNTS = 20
RUNAWAY_CHECK_S = 0.1
_POSITION_MODE, _VELOCITY_MODE = 0, 1  # lerobot OperatingMode.POSITION / VELOCITY
# SOFollower.configure()'s gripper protection: half torque and current, 25% when overloaded.
_GRIPPER_LIMITS = {"Max_Torque_Limit": 500, "Protection_Current": 250, "Overload_Torque": 25}


def build_follower_config(*, port: str, calibration_path: str,
                          side_camera_index: int | None = None,
                          wrist_camera_index: int | None = None,
                          include_camera: bool = True,
                          camera_index: int | None = None) -> Any:
    from lerobot.cameras.opencv import OpenCVCameraConfig
    from lerobot.robots.so_follower import SO101FollowerConfig

    calibration = Path(calibration_path).expanduser()
    if side_camera_index is None:
        side_camera_index = camera_index
    cameras = {}
    if include_camera:
        if side_camera_index is None or wrist_camera_index is None:
            raise ValueError("side_camera_index and wrist_camera_index are required")
        cameras[CAMERA_KEY_SO101_SIDE] = OpenCVCameraConfig(
            index_or_path=side_camera_index,
            width=OBS_FRAME_WIDTH,
            height=OBS_FRAME_HEIGHT,
            fps=30,
        )
        cameras[CAMERA_KEY_SO101_WRIST] = OpenCVCameraConfig(
            index_or_path=wrist_camera_index,
            width=OBS_FRAME_WIDTH,
            height=OBS_FRAME_HEIGHT,
            fps=30,
        )
    return SO101FollowerConfig(
        port=port,
        id=calibration.stem,                 # so101 → calibration file so101.json
        calibration_dir=calibration.parent,  # <home>/calibration
        use_degrees=True,                    # absolute joint pose, degrees (epic contract)
        cameras=cameras,
    )


def create_so101(*, port: str, calibration_path: str,
                 side_camera_index: int | None = None,
                 wrist_camera_index: int | None = None,
                 include_camera: bool = True,
                 camera_index: int | None = None) -> LeRobotSO101:
    from lerobot.robots.so_follower import SO101Follower

    config = build_follower_config(
        port=port,
        calibration_path=calibration_path,
        side_camera_index=side_camera_index,
        wrist_camera_index=wrist_camera_index,
        include_camera=include_camera,
        camera_index=camera_index,
    )
    return LeRobotSO101(follower=SO101Follower(config))


class LeRobotSO101:
    """RobotInterface implementation over lerobot's SO101Follower."""

    joint_names = JOINT_NAMES

    def __init__(self, follower: Any) -> None:
        self._follower = follower

    def connect(self) -> None:
        # SO101Follower.connect(calibrate=False), except that connecting never moves the
        # arm. Each servo drives at full speed to the Goal_Position an earlier session
        # left (release keeps it), so the goals first aim at where the arm is now. An arm
        # still holding with lerobot's settings (`run so101` exits holding) keeps holding:
        # configure() would cut torque to rewrite them, the arm would sag, and torque-on
        # would snap it back. Calibration stays with doctor/calibrate; connect never
        # blocks on lerobot's interactive prompt.
        bus = self._follower.bus
        bus.connect()
        present = bus.sync_read("Present_Position", normalize=False)
        bus.sync_write("Goal_Position", present, normalize=False)
        for camera in self._follower.cameras.values():
            camera.connect()
        if not self._holding_configured():
            self._configure()
        self._recover_runaway_servos()

    def _settings(self) -> dict[str, int]:
        config = self._follower.config
        return {
            "Operating_Mode": _POSITION_MODE,
            "P_Coefficient": config.position_p_coefficient,
            "I_Coefficient": config.position_i_coefficient,
            "D_Coefficient": config.position_d_coefficient,
        }

    def _holding_configured(self) -> bool:
        """Every servo holds torque with the settings configure() would write."""
        bus = self._follower.bus
        try:
            expected = {**self._settings(), "Torque_Enable": 1, "Return_Delay_Time": 0,
                        "Acceleration": 254}
            for register, value in expected.items():
                if any(v != value for v in bus.sync_read(register, normalize=False).values()):
                    return False
            if any(bus.read(register, "gripper", normalize=False) != value
                   for register, value in _GRIPPER_LIMITS.items()):
                return False
            return not any(bus.read("Phase", motor, normalize=False) & 0x10
                           for motor in bus.motors)
        except Exception:  # noqa: BLE001 - an unreadable setting means configure it.
            return False

    def _configure(self) -> None:
        """lerobot's SOFollower.configure(), aiming each goal at the measured pose before
        torque returns, so a joint that sagged while limp holds where it settled."""
        bus = self._follower.bus
        bus.disable_torque()
        try:
            bus.configure_motors()
            for motor in bus.motors:
                for register, value in self._settings().items():
                    bus.write(register, motor, value)
            for register, value in _GRIPPER_LIMITS.items():
                bus.write(register, "gripper", value)
        finally:
            here = bus.sync_read("Present_Position", normalize=False)
            bus.sync_write("Goal_Position", here, normalize=False)
            bus.enable_torque()

    def _recover_runaway_servos(self, sleep: Callable[[float], None] = time.sleep) -> None:
        """Catch a servo whose position control drives away from its goal.

        A Feetech STS3215 can latch a state in which position mode pushes toward one
        end of its travel whatever the goal: an SO-101 wrist_roll, given goal ==
        present, ran into its stopper at full load until it overloaded. Velocity mode
        still drove it both ways, and switching it to velocity mode and back cleared
        the latch. A healthy servo does not move at all when torque comes on with goal
        == present, so a joint that has already moved RUNAWAY_COUNTS is latched.
        """
        bus = self._follower.bus
        for attempt in range(2):
            goals = bus.sync_read("Goal_Position", normalize=False)
            sleep(RUNAWAY_CHECK_S)
            present = bus.sync_read("Present_Position", normalize=False)
            runaway = [m for m in goals if abs(present[m] - goals[m]) > RUNAWAY_COUNTS]
            if not runaway:
                return
            for motor in runaway:
                bus.disable_torque(motor)  # also unlocks EEPROM for the mode writes
                if attempt:
                    continue  # still latched after a reset: leave it limp
                bus.write("Operating_Mode", motor, _VELOCITY_MODE)
                sleep(RUNAWAY_CHECK_S)
                bus.write("Operating_Mode", motor, _POSITION_MODE)
                here = bus.read("Present_Position", motor, normalize=False)
                bus.write("Goal_Position", motor, here, normalize=False)
                bus.enable_torque(motor)
        raise errors.catalog("so101_servo_runaway", detail=", ".join(runaway))

    def connect_bus(self) -> None:
        # Serial bus only: skips configure(), which re-enables torque on exit.
        self._follower.bus.connect()

    def disconnect(self, *, release_torque: bool = True) -> None:
        if release_torque:
            self._follower.disconnect()  # lerobot disables torque on disconnect
            return
        # Leave the motors holding their last goal; `robots so101 release` ends it.
        self._follower.bus.disconnect(disable_torque=False)
        for camera in self._follower.cameras.values():
            camera.disconnect()

    def release_torque(self) -> None:
        self._follower.bus.disable_torque()

    def is_calibrated(self) -> bool:
        return bool(self._follower.is_calibrated)

    def read_joint_positions(self) -> list[float]:
        positions = self._follower.bus.sync_read("Present_Position")
        return [float(positions[name]) for name in self.joint_names]

    def capture_frame(self) -> np.ndarray:
        camera = self._follower.cameras[CAMERA_KEY_SO101]
        return camera.read_latest(max_age_ms=500)

    def capture_frames(self) -> dict[str, np.ndarray]:
        return {
            CAMERA_KEY_SO101_SIDE: self._follower.cameras[
                CAMERA_KEY_SO101_SIDE
            ].read_latest(max_age_ms=500),
            CAMERA_KEY_SO101_WRIST: self._follower.cameras[
                CAMERA_KEY_SO101_WRIST
            ].read_latest(max_age_ms=500),
        }

    def send_joint_targets(self, targets: list[float]) -> None:
        # strict: a dim mismatch must refuse, never silently drop joint commands.
        action = {
            f"{name}.pos": float(value)
            for name, value in zip(self.joint_names, targets, strict=True)
        }
        self._follower.send_action(action)

    def calibrate(self) -> None:
        self._follower.calibrate()
