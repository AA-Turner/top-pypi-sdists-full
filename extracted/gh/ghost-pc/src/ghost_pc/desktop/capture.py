"""Screen capture using BetterCam (DXGI Desktop Duplication API).

BetterCam returns numpy arrays. We encode to JPEG with PyTurboJPEG
for fast, SIMD-accelerated compression.
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray

# Lazy imports — these are Windows-only
_camera = None
_jpeg = None
_last_frame: NDArray[np.uint8] | None = None


def _get_camera():
    """Lazy-init BetterCam. Fails gracefully on non-Windows."""
    global _camera
    if _camera is not None:
        return _camera

    if sys.platform != "win32":
        raise RuntimeError("Screen capture requires Windows (DXGI Desktop Duplication)")

    import bettercam

    # BGRA is DXGI's native format — avoids cv2 dependency for color conversion.
    # We pass pixel_format=TJPF_BGRA to TurboJPEG instead.
    _camera = bettercam.create(output_color="BGRA")
    return _camera


def _get_jpeg():
    """Lazy-init TurboJPEG encoder."""
    global _jpeg
    if _jpeg is not None:
        return _jpeg

    from turbojpeg import TurboJPEG

    # In a PyInstaller bundle, the DLL is next to the exe (sys._MEIPASS for
    # onefile, or the exe's directory for onedir).  TurboJPEG() won't find it
    # automatically, so we pass the path explicitly.
    lib_path = None
    if getattr(sys, "frozen", False):
        import os

        base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
        for name in ("turbojpeg.dll", "libturbojpeg.dll", "libturbojpeg.so", "libturbojpeg.dylib"):
            candidate = os.path.join(base, name)
            if os.path.isfile(candidate):
                lib_path = candidate
                break

    _jpeg = TurboJPEG(lib_path) if lib_path else TurboJPEG()
    return _jpeg


def grab_screenshot() -> NDArray[np.uint8] | None:
    """Capture full screen as a BGRA numpy array.

    Returns the cached frame if the screen hasn't changed since last grab.
    Shape: (height, width, 4), dtype: uint8, color: BGRA
    """
    global _last_frame
    camera = _get_camera()
    frame = camera.grab()
    if frame is not None:
        _last_frame = frame
        return frame
    return _last_frame


def grab_screenshot_region(
    left: int, top: int, right: int, bottom: int
) -> NDArray[np.uint8] | None:
    """Capture a screen region. Coordinates: (left, top, right, bottom)."""
    camera = _get_camera()
    return camera.grab(region=(left, top, right, bottom))


def screenshot_to_jpeg(frame: NDArray[np.uint8], quality: int = 70) -> bytes:
    """Encode a BGRA numpy frame to JPEG bytes.

    Args:
        frame: BGRA numpy array from BetterCam, shape (H, W, 4)
        quality: JPEG quality 1-100 (70 is good balance for screenshots)

    Returns:
        JPEG bytes ready to send over network or to Gemini API
    """
    from turbojpeg import TJPF_BGRA

    jpeg = _get_jpeg()
    result = jpeg.encode(frame, quality=quality, pixel_format=TJPF_BGRA)
    if isinstance(result, tuple):
        return result[0] or b""
    return result or b""


def grab_and_encode(quality: int = 70) -> bytes | None:
    """Capture screen and return JPEG bytes in one step.

    Returns None if screen hasn't changed.
    """
    frame = grab_screenshot()
    if frame is None:
        return None
    return screenshot_to_jpeg(frame, quality=quality)


def get_screen_dimensions() -> tuple[int, int]:
    """Get primary screen resolution (width, height)."""
    if sys.platform != "win32":
        return (1920, 1080)  # Fallback for dev

    import ctypes

    user32 = ctypes.windll.user32
    return (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
