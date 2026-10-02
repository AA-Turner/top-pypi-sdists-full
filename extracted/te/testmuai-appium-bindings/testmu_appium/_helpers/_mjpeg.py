"""One JPEG frame off the uiautomator2 server's MJPEG broadcaster.

The `appium:mjpegServerPort` capability makes the Appium driver forward a host port
to the on-device MJPEG server, so a frame can be read straight off that socket
instead of paying a screencap round trip through the Appium node.

The forward is created on the host running the Appium server: 127.0.0.1 reaches it
for a local run target and reaches nothing for a cloud session, whose device host is
elsewhere. The stream is therefore probed, never assumed, and the first failed read
disables it for the rest of the session — a run that cannot reach the stream pays one
connect attempt, not one per capture. `reset()` clears that verdict at session start.
"""
import logging
import socket
import time
from typing import Optional

from testmu_appium import _config
from testmu_appium._helpers import _adapters

_log = logging.getLogger("testmu_appium")

#: Factor from device pixels to a served frame's own pixels, per screenshot source.
#: The uiautomator2 MJPEG server broadcasts frames at half the device resolution
#: (measured on the reference device); the Appium screencap is full resolution.
_ANDROID_SOURCE_DOWNSCALE = {
    _config.SOURCE_MJPEG: 0.5,
    _config.SOURCE_APPIUM: 1.0,
}


def _android_downscale(screenshot_source: str) -> float:
    return _ANDROID_SOURCE_DOWNSCALE[str(screenshot_source).lower()]


#: iOS works in POINTS end to end — Appium taps in points, get_window_size
#: reports points, and the vision window is asked for in points — so a frame's
#: extra resolution never enters a coordinate calculation and the factor in THAT
#: basis is 1.0 for either source. This is the true value in the basis the binding
#: uses, not a placeholder: a consumer that genuinely needs frame-pixel space must
#: derive the display scale from the driver, because it is per-device (2x or 3x)
#: and cannot be answered by a static table.
_IOS_SOURCE_DOWNSCALE = {
    _config.SOURCE_MJPEG: 1.0,
    _config.SOURCE_APPIUM: 1.0,
}


def _ios_downscale(screenshot_source: str) -> float:
    return _IOS_SOURCE_DOWNSCALE[str(screenshot_source).lower()]


_adapters.register("screenshot_scaling", {
    "android": {"downscale": _android_downscale},
    "ios": {"downscale": _ios_downscale},
})


def source_downscale(screenshot_source: str, *, platform: Optional[str] = None) -> float:
    """Factor from device pixels to the given screenshot source's frame pixels."""
    downscale = _adapters.adapter(
        "screenshot_scaling", "downscale", "screenshot scaling", platform=platform
    )
    return downscale(screenshot_source)

#: JPEG frame markers: a frame runs from SOI (ff d8) through EOI (ff d9).
_SOI = b"\xff\xd8"
_EOI = b"\xff\xd9"

_CHUNK = 65536

#: Connect + first-frame budget. A live broadcaster answers within one frame interval
#: (~100ms at its 10fps default).
_STREAM_TIMEOUT_S = 2.0

#: Once a whole frame is in hand, a read that blocks this long means nothing newer is
#: buffered — the reader has caught up with the broadcaster.
_DRAIN_TIMEOUT_S = 0.05

#: Session-scoped verdict, set by the first failed read and cleared by reset().
_unreachable = False


def reset() -> None:
    """Forget the reachability verdict so the next capture probes the stream again."""
    global _unreachable
    _unreachable = False


def source() -> str:
    """The configured screenshot source: "auto", "mjpeg" or "appium"."""
    return str(_config.get("screenshot_source") or _config.SOURCE_AUTO).lower()


def port() -> int:
    """The host port the MJPEG forward is expected on."""
    return int(_config.get("mjpeg_port") or _config._DEFAULT_MJPEG_PORT)


def wanted() -> bool:
    """Whether this session asks Appium for the MJPEG forward and may read it.

    "auto" claims the forward only for a local run target, where the Appium server
    shares a host with the test process and 127.0.0.1 reaches it; "mjpeg" claims it
    unconditionally, which is how a run with its own tunnel opts in.
    """
    configured = source()
    if configured == _config.SOURCE_APPIUM:
        return False
    return configured == _config.SOURCE_MJPEG or _config.run_target == "local"


def usable() -> bool:
    """Whether a capture should open the stream: wanted, and not already found dead."""
    return wanted() and not _unreachable


def mark_unreachable(error: BaseException) -> None:
    """Record that the stream failed, so no later capture in this session retries it."""
    global _unreachable
    _unreachable = True
    _log.info(
        "[perception] MJPEG stream on 127.0.0.1:%d unavailable (%s); "
        "the Appium screenshot serves the rest of this session", port(), error,
    )


def _complete_frames(buffered: bytes) -> tuple[Optional[bytes], bytes]:
    """Split every complete JPEG out of the buffer: (last complete frame, remainder).

    The remainder holds a partial frame, or one trailing byte when no frame has
    started, so a marker split across two reads is still found.
    """
    latest = None
    while True:
        start = buffered.find(_SOI)
        if start < 0:
            return latest, buffered[-1:]
        end = buffered.find(_EOI, start + len(_SOI))
        if end < 0:
            return latest, buffered[start:]
        latest = buffered[start:end + len(_EOI)]
        buffered = buffered[end + len(_EOI):]


def read_latest_frame() -> bytes:
    """Return the newest complete JPEG frame the stream currently holds.

    The broadcaster pushes ~10 frames a second, so the first frame off the socket can
    be a frame interval old while newer ones are already buffered behind it. The read
    drains what the socket has and keeps the LAST complete frame, stopping as soon as
    a read blocks (nothing newer buffered) or the stream ends.

    The frame is JPEG bytes, not PNG; the callers that base64 it do not care.

    Raises:
        OSError: The stream could not be opened.
        RuntimeError: The stream opened but produced no complete frame in time.
    """
    stream_port = port()
    deadline = time.monotonic() + _STREAM_TIMEOUT_S
    sock = socket.create_connection(("127.0.0.1", stream_port), timeout=_STREAM_TIMEOUT_S)
    latest: Optional[bytes] = None
    buffered = b""
    try:
        sock.sendall((
            f"GET / HTTP/1.1\r\n"
            f"Host: 127.0.0.1:{stream_port}\r\n"
            f"Accept: */*\r\n"
            f"Connection: close\r\n\r\n"
        ).encode())
        while time.monotonic() < deadline:
            try:
                chunk = sock.recv(_CHUNK)
            except OSError:
                # A blocked read once a frame is in hand is the drain's exit; a
                # broken one is a failure only when no frame was read at all.
                break
            if not chunk:
                break
            frame, buffered = _complete_frames(buffered + chunk)
            if frame is not None:
                latest = frame
                sock.settimeout(_DRAIN_TIMEOUT_S)
    finally:
        sock.close()

    if latest is None:
        raise RuntimeError(
            f"no complete MJPEG frame on 127.0.0.1:{stream_port} "
            f"within {_STREAM_TIMEOUT_S}s"
        )
    return latest
