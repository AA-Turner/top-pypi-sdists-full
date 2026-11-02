"""Headless fakes for tests (and the doctor's --fake mode is built on these)."""

from __future__ import annotations

import numpy as np

from dreamscale.constants import CAMERA_KEY_SO101_SIDE, CAMERA_KEY_SO101_WRIST


class FakeRobot:
    def __init__(self, positions: list[float] | None = None, calibrated: bool = True,
                 frame: np.ndarray | None = None,
                 wrist_frame: np.ndarray | None = None) -> None:
        self._positions = list(positions or [0.0] * 6)
        self._calibrated = calibrated
        self._frame = frame if frame is not None else np.zeros((480, 640, 3), dtype=np.uint8)
        self._wrist_frame = (
            wrist_frame if wrist_frame is not None else np.zeros((480, 640, 3), dtype=np.uint8)
        )
        self.sent: list[list[float]] = []
        self.connected = False
        self.torque = False
        self.calibrate_calls = 0

    def connect(self) -> None:
        self.connected = True
        self.torque = True

    def connect_bus(self) -> None:
        self.connected = True

    def disconnect(self, *, release_torque: bool = True) -> None:
        self.connected = False
        if release_torque:
            self.torque = False

    def release_torque(self) -> None:
        self.torque = False

    def is_calibrated(self) -> bool:
        return self._calibrated

    def read_joint_positions(self) -> list[float]:
        return list(self._positions)

    def capture_frame(self) -> np.ndarray:
        return self._frame

    def capture_frames(self) -> dict[str, np.ndarray]:
        return {
            CAMERA_KEY_SO101_SIDE: self._frame,
            CAMERA_KEY_SO101_WRIST: self._wrist_frame,
        }

    def send_joint_targets(self, targets: list[float]) -> None:
        self.sent.append(list(targets))
        self._positions = list(targets)

    def calibrate(self) -> None:
        self.calibrate_calls += 1
        self._calibrated = True


class FakeCameraProber:
    def __init__(self, available: set[int] | None = None) -> None:
        self._available = available if available is not None else {0}

    def list_cameras(self, max_index: int = 6) -> list[int]:
        return sorted(i for i in self._available if i < max_index)

    def capture_preview(self, index: int) -> np.ndarray | None:
        if index not in self._available:
            return None
        return np.full((480, 640, 3), 127, dtype=np.uint8)


class FakeRigCameraProber:
    """RigCameraProber's shape over custom CameraSpecs "cam0", "cam1", ..."""

    def __init__(self, available: set[int] | None = None) -> None:
        from dreamscale.hardware.camera_sources import CameraSpec

        self.specs = [
            CameraSpec(f"cam{i}", "custom", f"usb:fake:{i}", f"cam{i}")
            for i in sorted(available if available is not None else {0})
        ]

    def list_cameras(self):
        return list(self.specs)

    def capture_preview(self, spec) -> np.ndarray | None:
        if spec not in self.specs:
            return None
        return np.full((480, 640, 3), 127, dtype=np.uint8)
