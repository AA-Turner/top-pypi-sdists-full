"""OpenCV camera enumeration + preview capture. cv2 is isolated to this module
(and lerobot's own capture path)."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import numpy as np


@contextmanager
def _quiet_opencv(cv2) -> Iterator[None]:
    """Silence OpenCV's per-index `[ WARN ] can't open camera by index` noise.

    Probing indexes that are not cameras (V4L metadata nodes, codecs) is expected
    to fail; the setup flow reports what it found instead.
    """
    logging = getattr(getattr(cv2, "utils", None), "logging", None)
    if logging is None:
        yield
        return
    previous = logging.getLogLevel()
    logging.setLogLevel(logging.LOG_LEVEL_SILENT)
    try:
        yield
    finally:
        logging.setLogLevel(previous)


class OpenCVCameraProber:
    def list_cameras(self, max_index: int = 6) -> list[int]:
        import cv2

        available = []
        with _quiet_opencv(cv2):
            for index in range(max_index):
                cap = cv2.VideoCapture(index)
                if cap.isOpened():
                    available.append(index)
                cap.release()
        return available

    def capture_preview(self, index: int) -> np.ndarray | None:
        import cv2

        with _quiet_opencv(cv2):
            cap = cv2.VideoCapture(index)
            try:
                if not cap.isOpened():
                    return None
                ok, frame = cap.read()
                return frame if ok else None
            finally:
                cap.release()


def save_preview(frame: np.ndarray, path: Path) -> Path:
    import cv2

    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), frame)
    return path


class RigCameraProber:
    """Cameras by stable identity for setup and doctor, every platform and backend:
    one CameraSpec per physical camera (one_per_camera), previews through CameraReaders."""

    def __init__(self, saved=None, *, discover=None, readers_factory=None):
        self.saved = list(saved or [])
        self._discover, self._readers_factory = discover, readers_factory

    def list_cameras(self):
        from .camera_sources import discover_cameras, one_per_camera, usb_link_mbps

        found = (self._discover or discover_cameras)()
        present = {spec.physical_id for spec in found}
        return [  # connected cameras only; a saved one keeps its stream settings
            spec for spec in one_per_camera(self.saved, found, link_speed=usb_link_mbps)
            if spec.physical_id in present
        ]

    def capture_preview(self, spec) -> np.ndarray | None:
        """One BGR frame (for cv2.imwrite), or None when the camera won't stream."""
        from .camera_sources import CameraReaders, wait_for_frames

        readers = (self._readers_factory or CameraReaders)([spec])
        try:
            readers.open()
            frame = wait_for_frames(readers, [spec.id], timeout_s=8.0)[spec.id]
            return frame.rgb[:, :, ::-1].copy()
        except Exception:
            return None
        finally:
            try:
                readers.close()
            except Exception:
                pass
