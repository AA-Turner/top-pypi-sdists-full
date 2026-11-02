"""Timestamped RGB sources shared by camera setup and robot observation.

Custom sources implement RGBFrameSource: open/close own their resources, latest
is nonblocking, and each genuinely new frame carries its original wall-clock
acquisition time and monotonic acquisition time. Never re-stamp cached frames.
Native readers run in owned processes so blocked driver calls can be terminated.
"""

from __future__ import annotations

import importlib.util
import json
import multiprocessing as mp
import os
import platform
import queue
import re
import subprocess
import sys
import tempfile
import threading
import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Protocol

import numpy as np


class CameraError(RuntimeError):
    """Camera unavailable, stale, or incorrectly configured."""


_BUSY = ("Device or resource busy", "errno=16", "EBUSY")
CAMERA_BUSY = (
    "In use by another program. Stop whatever holds the camera (a recorder or teleop "
    "stack, for example), then rerun."
)


def camera_error_text(exc: BaseException) -> str:
    """A camera failure for the operator: a camera another process holds says so."""
    text = str(exc) or type(exc).__name__
    return CAMERA_BUSY if any(sign in text for sign in _BUSY) else text


class FrameUnavailable(CameraError):
    """An open source has not acquired its first frame yet; startup may retry."""


class FrameTimeout(CameraError):
    """A native read waited out its timeout without a frame; capture may recover."""


# A run treats a frame older than its freshness limit (1 s) as a lagging camera: it warns and
# keeps going. Only a frame older than this means the camera has stopped, which ends the task.
CAMERA_STOP_AGE_S = 5.0

# Consecutive timed-out native reads (1 s each for RealSense) that capture
# rides out before failing: a brief USB stall should not end the capture.
# Consumers still reject any frame older than their freshness limit meanwhile.
MAX_FRAME_TIMEOUTS = 3


@dataclass(frozen=True)
class RGBFrame:
    rgb: np.ndarray
    timestamp_ns: int
    monotonic_ns: int
    sequence: int

    def validate(self, max_age_s: float = 1.0) -> RGBFrame:
        if not isinstance(self.rgb, np.ndarray):
            raise CameraError("Camera must supply a NumPy RGB image.")
        if type(self.sequence) is not int or self.sequence < 0:
            raise CameraError("Camera must supply a nonnegative frame sequence number.")
        if (
            self.rgb.dtype != np.uint8
            or self.rgb.ndim != 3
            or self.rgb.shape[2] != 3
            or min(self.rgb.shape[:2]) == 0
        ):
            raise CameraError("Camera must supply a nonempty uint8 RGB image.")
        if (
            type(self.timestamp_ns) is not int
            or self.timestamp_ns <= 0
            or type(self.monotonic_ns) is not int
            or self.monotonic_ns <= 0
        ):
            raise CameraError("Camera must supply acquisition timestamps.")
        age = (time.monotonic_ns() - self.monotonic_ns) / 1e9
        if age < -0.1 or age > max_age_s:
            raise CameraError(
                "Camera frame is stale. Check its USB connection and restart cameras."
            )
        return self


def lagging_latest(readers, camera_id, *, warn_age_s, stop_age_s=CAMERA_STOP_AGE_S, on_lag=None):
    """A camera's latest frame during a run, tolerating lag: a frame older than ``warn_age_s``
    is still used and reported to ``on_lag(age_s)``; only one older than ``stop_age_s`` (or
    any other camera failure) raises ``CameraError``."""
    frame = readers.latest(camera_id, max_age_s=max(warn_age_s, stop_age_s))
    age_s = (time.monotonic_ns() - frame.monotonic_ns) / 1e9
    if age_s > warn_age_s and on_lag is not None:
        on_lag(age_s)
    return frame


class RGBFrameSource(Protocol):
    """Nonblocking latest raises FrameUnavailable only while awaiting first capture."""

    def open(self) -> None: ...
    def latest(self, max_age_s: float = 1.0) -> RGBFrame: ...
    def close(self) -> None: ...


@dataclass(frozen=True)
class CameraSpec:
    id: str
    backend: str
    physical_id: str
    device: str
    eye: str | None = None
    rotate: int = 0
    width: int = 640
    height: int = 480
    fps: int = 30

    def __post_init__(self):
        if self.backend not in {"uvc", "realsense", "zed", "custom"}:
            raise ValueError("Choose uvc, realsense, zed, or custom camera backend.")
        if not all(isinstance(v, str) and v for v in (self.id, self.physical_id, self.device)):
            raise ValueError("Camera identity, physical identity and device are required.")
        if self.rotate not in (0, 90, 180, 270):
            raise ValueError("Camera rotation must be 0, 90, 180, or 270 degrees.")
        if self.backend == "zed" and self.eye not in {"left", "right"}:
            raise ValueError(
                "ZED requires an explicit left or right eye of its side-by-side stream."
            )
        if self.backend != "zed" and self.eye is not None:
            raise ValueError("Eye selection is only supported for ZED side-by-side streams.")
        if any(type(v) is not int or v <= 0 for v in (self.width, self.height, self.fps)):
            raise ValueError("Camera width, height and fps must be positive integers.")
        if self.width > 4096 or self.height > 2160 or self.fps > 120:
            raise ValueError("Camera dimensions or frame rate exceed supported limits.")
        if self.backend in {"uvc", "zed"} and not self.device.startswith(
            ("/dev/v4l/by-id/", "/dev/v4l/by-path/", AVFOUNDATION)
        ):
            raise ValueError(
                "Save a stable camera identity (/dev/v4l/by-id or by-path on Linux, "
                "avfoundation:<unique id> on macOS), never an index or /dev/videoN."
            )


def transform_rgb(rgb: np.ndarray, spec: CameraSpec) -> np.ndarray:
    if spec.backend == "zed":
        # Configured width means one eye. Reject an ordinary mono stream.
        if rgb.shape[1] != spec.width * 2 or rgb.shape[0] != spec.height:
            raise CameraError("ZED must provide the configured side-by-side RGB dimensions.")
        start = 0 if spec.eye == "left" else spec.width
        rgb = rgb[:, start : start + spec.width]
    if spec.rotate:
        rgb = np.rot90(rgb, -(spec.rotate // 90))
    return np.ascontiguousarray(rgb)


def dependency_help(backend: str) -> str | None:
    module = {"uvc": "cv2", "zed": "cv2", "realsense": "pyrealsense2"}.get(backend)
    if module and importlib.util.find_spec(module) is None:
        return install_hint(backend)
    return None


def install_hint(backend: str) -> str:
    """How to get a camera backend's reader: setup installs it where it can."""
    from dreamscale.extras import realsense_installable

    if backend == "realsense" and not realsense_installable():
        return ("RealSense needs pyrealsense2, which only has wheels for x86_64 Linux "
                "and Windows on Python 3.13 or older, and for aarch64 Linux.")
    return "Camera support is not installed. Run: dreamscale robots yam setup"


# macOS cameras by AVFoundation unique ID. OpenCV's AVFoundation backend numbers the
# video devices by sorting their unique IDs (cap_avfoundation_mac.mm), so a saved ID
# resolves to today's index whatever order the cameras were plugged in.
AVFOUNDATION = "avfoundation:"


def avfoundation_ids(*, run=subprocess.run) -> list[str]:
    """Unique IDs of the Mac's cameras, from system_profiler, in OpenCV's index order."""
    try:
        result = run(["system_profiler", "SPCameraDataType", "-json"],
                     capture_output=True, text=True, timeout=20, check=False)
        cameras = json.loads(result.stdout or "{}").get("SPCameraDataType", [])
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return []
    ids = [c.get("spcamera_unique-id") for c in cameras if isinstance(c, dict)]
    return sorted(i for i in ids if isinstance(i, str) and i)


def discover_avfoundation(*, ids=None) -> list[CameraSpec]:
    ids = ids or avfoundation_ids
    return [
        CameraSpec(id=AVFOUNDATION + uid, backend="uvc", physical_id=AVFOUNDATION + uid,
                   device=AVFOUNDATION + uid)
        for uid in ids()
    ]


def avfoundation_index(device: str, *, ids=None) -> int:
    """Today's OpenCV index of a camera saved as avfoundation:<unique id>."""
    unique_id, known = device[len(AVFOUNDATION):], (ids or avfoundation_ids)()
    if unique_id not in known:
        raise CameraError("Camera is not connected. Plug it in, then rerun setup.")
    return known.index(unique_id)


def opencv_source(device: str, *, ids=None):
    """What cv2.VideoCapture opens for a saved device, and with which backend."""
    import cv2

    if device.startswith(AVFOUNDATION):
        return avfoundation_index(device, ids=ids), cv2.CAP_AVFOUNDATION
    return device, cv2.CAP_V4L2


def camera_for_index(index: int, *, v4l_root: Path = Path("/dev/v4l"),
                     ids=None) -> CameraSpec | None:
    """A stable identity for a legacy OpenCV camera index, or None when it can't be
    resolved (the camera is unplugged, or the platform has no stable identity)."""
    if sys.platform == "darwin":
        known = (ids or avfoundation_ids)()
        if 0 <= index < len(known):
            uid = AVFOUNDATION + known[index]
            return CameraSpec(id=uid, backend="uvc", physical_id=uid, device=uid)
        return None
    target = os.path.realpath(f"/dev/video{int(index)}")
    for directory in ("by-id", "by-path"):
        for path in sorted((v4l_root / directory).glob("*")):
            if os.path.realpath(path) == target:
                device = f"/dev/v4l/{directory}/{path.name}"
                return CameraSpec(id=device, backend="uvc",
                                  physical_id=usb_physical_id(str(path)), device=device)
    return None


def usb_physical_id(device: str) -> str:
    """Resolve V4L aliases to their parent USB serial or physical USB port."""
    node = Path(device).resolve().name
    sys_device = Path("/sys/class/video4linux") / node / "device"
    return _usb_parent_identity(sys_device) or f"v4l:{Path(device).resolve()}"


def _usb_parent_identity(sys_device: Path) -> str | None:
    for parent in (sys_device.resolve(), *sys_device.resolve().parents):
        if (parent / "idVendor").exists():
            vendor = (parent / "idVendor").read_text().strip()
            serial_path = parent / "serial"
            serial = serial_path.read_text().strip() if serial_path.exists() else ""
            return f"usb:{vendor}:{serial}" if serial else f"usb-port:{parent.name}"
    return None


# V4L2 ioctls (linux/videodev2.h): struct v4l2_capability is 104 bytes,
# struct v4l2_fmtdesc 64.
_VIDIOC_QUERYCAP = 0x80685600
_VIDIOC_ENUM_FMT = 0xC0405602
_V4L2_CAP_VIDEO_CAPTURE = 0x1
_V4L2_CAP_DEVICE_CAPS = 0x80000000
# Formats OpenCV decodes to color. Depth (Z16) and infrared (GREY, Y8, Y16...)
# streams, and metadata nodes with no capture formats, are not RGB cameras.
_COLOR_FOURCCS = {
    b"YUYV", b"UYVY", b"YVYU", b"MJPG", b"JPEG", b"RGB3", b"BGR3",
    b"NV12", b"NV21", b"YU12", b"YV12",
}


def v4l2_color_capture(device: str) -> bool | None:
    """Whether a V4L node captures a color format; None when it cannot be queried."""
    import fcntl
    import struct

    try:
        fd = os.open(device, os.O_RDONLY | os.O_NONBLOCK)
    except OSError:
        return None
    try:
        caps = bytearray(104)
        fcntl.ioctl(fd, _VIDIOC_QUERYCAP, caps)
        capabilities, device_caps = struct.unpack_from("<II", caps, 84)
        if capabilities & _V4L2_CAP_DEVICE_CAPS:
            capabilities = device_caps
        if not capabilities & _V4L2_CAP_VIDEO_CAPTURE:
            return False
        for index in range(64):
            desc = bytearray(64)
            struct.pack_into("<II", desc, 0, index, 1)  # V4L2_BUF_TYPE_VIDEO_CAPTURE
            try:
                fcntl.ioctl(fd, _VIDIOC_ENUM_FMT, desc)
            except OSError:
                return False
            if bytes(desc[44:48]) in _COLOR_FOURCCS:
                return True
        return False
    except OSError:
        return None
    finally:
        os.close(fd)


def discover_uvc(
    root: Path = Path("/dev/v4l"), *, color_capture=v4l2_color_capture
) -> list[CameraSpec]:
    found: dict[str, tuple[CameraSpec, bool | None]] = {}
    for directory in ("by-id", "by-path"):
        for path in sorted((root / directory).glob("*")):
            if not path.exists() or str(path.resolve()) in found:
                continue
            # by-id entries without a USB serial are port-bound, not serial-stable.
            physical = usb_physical_id(str(path))
            if directory == "by-id" and not physical.startswith("usb:"):
                continue
            # No USB parent: a system-on-chip codec or image processor (Raspberry Pi's
            # pisp_be, Jetson's), never a camera this backend can stream.
            if not physical.startswith(("usb:", "usb-port:")):
                continue
            found[str(path.resolve())] = (
                CameraSpec(id=str(path), backend="uvc", physical_id=physical, device=str(path)),
                color_capture(str(path)),
            )
    return color_nodes(list(found.values()))


def usb_cameras_present(usb_devices: Path = Path("/sys/bus/usb/devices")) -> frozenset:
    """(port, device address) of each USB device with a video interface.

    Cheap enough to poll, and unchanged while a camera streams: interfaces stay
    listed when RSUSB detaches the kernel driver. A camera that resets after a
    USB error comes back under a new address. Empty where there is no sysfs.
    """
    present = set()
    for interface in usb_devices.glob("*:*"):
        try:
            if (interface / "bInterfaceClass").read_text().strip() != "0e":
                continue
            device = interface.name.split(":")[0]
            present.add((device, (usb_devices / device / "devnum").read_text().strip()))
        except OSError:
            continue  # unplugged mid-read
    return frozenset(present)


def color_nodes(nodes: list[tuple[CameraSpec, bool | None]]) -> list[CameraSpec]:
    """Keep each camera's color nodes from (spec, streams color?) pairs.

    One camera exposes several nodes (RealSense: depth, infrared, color,
    metadata). Keep its confirmed color nodes, else the nodes that could not be
    queried; a camera with no color node at all keeps every node rather than
    disappearing.
    """
    groups: dict[str, list[tuple[CameraSpec, bool | None]]] = {}
    for spec, color in nodes:
        groups.setdefault(spec.physical_id, []).append((spec, color))
    result = []
    for group in groups.values():
        for wanted in (True, None, False):
            kept = [spec for spec, color in group if color is wanted]
            if kept:
                result.extend(kept)
                break
    return result


# Stereolabs' USB vendor. ZEDs stream both eyes side by side; DROID-style models and
# every rig here read the left eye at 720p.
STEREOLABS_VENDOR = "2b03"
ZED_LEFT_EYE = {"eye": "left", "width": 1280, "height": 720, "fps": 30}
# USB 3 (SuperSpeed) or faster.
USB3_MBPS = 5000
# The one ZED mode a USB 2 link carries: VGA per eye at 15 fps. A ZED Mini streams
# nothing on USB 2 (it shows no video device at all).
ZED_USB2_MODE = {"width": 672, "height": 376, "fps": 15}


def usb_link_mbps(spec, *, sys_root=Path("/")) -> int | None:
    """Negotiated USB speed of a camera, from sysfs; None when it can't be resolved.

    Every backend's physical_id names the USB device: usb:<vendor>:<serial> or
    usb-port:<sysfs name>.
    """
    devices = sys_root / "sys/bus/usb/devices"
    kind, _, rest = spec.physical_id.partition(":")
    try:
        if kind == "usb-port":
            return int(float((devices / rest / "speed").read_text().strip()))
        if kind == "usb":
            vendor, _, serial = rest.partition(":")
            for usb in devices.glob("*"):
                if (
                    (usb / "idVendor").exists() and (usb / "serial").exists()
                    and (usb / "idVendor").read_text().strip() == vendor
                    and (usb / "serial").read_text().strip() == serial
                ):
                    return int(float((usb / "speed").read_text().strip()))
    except (OSError, ValueError):
        return None
    return None


def fit_to_link(spec: CameraSpec, mbps: int | None) -> CameraSpec:
    """The stream a camera can deliver on its USB link: a ZED drops to VGA at 15 fps on
    USB 2. Unknown links, and other backends, keep their spec."""
    if spec.backend != "zed" or mbps is None:
        return spec
    if mbps >= USB3_MBPS:
        return replace(spec, width=ZED_LEFT_EYE["width"], height=ZED_LEFT_EYE["height"],
                       fps=ZED_LEFT_EYE["fps"])
    return replace(spec, **ZED_USB2_MODE)


def as_zed_eye(spec: CameraSpec) -> CameraSpec:
    """A Stereolabs UVC node as the ZED backend's left eye; anything else unchanged."""
    if spec.backend == "uvc" and spec.physical_id.startswith(f"usb:{STEREOLABS_VENDOR}:"):
        return replace(spec, backend="zed", **ZED_LEFT_EYE)
    return spec


def one_per_camera(saved: list[CameraSpec], found: list[CameraSpec], *,
                   link_speed=None) -> list[CameraSpec]:
    """One choice per physical camera, in discovery order, for every robot's setup.

    A saved camera keeps its stream and rotation. Otherwise RealSense SDK color
    beats its raw UVC nodes, a ZED reads as its left eye, then the first discovered
    node wins. Saved cameras that are not connected come last, so setup can say
    they are missing. With link_speed (usb_link_mbps), each connected ZED gets the
    mode its USB link can carry, saved or not.
    """
    found = [as_zed_eye(spec) for spec in found]
    rank = {"realsense": 0}
    chosen: dict[str, CameraSpec] = {}
    for spec in sorted(found, key=lambda s: rank.get(s.backend, 1)):
        chosen.setdefault(spec.physical_id, spec)
    order: dict[str, int] = {}
    for spec in found:
        order.setdefault(spec.physical_id, len(order))
    result = sorted(chosen.values(), key=lambda s: order[s.physical_id])
    saved_by_physical = {s.physical_id: s for s in saved}
    result = [saved_by_physical.pop(s.physical_id, s) for s in result]
    if link_speed is not None:
        result = [fit_to_link(spec, link_speed(spec)) for spec in result]
    return result + list(saved_by_physical.values())


# RSUSB builds of librealsense name a camera's port <bus>-<port path>-<device address>
# (1-2.2.3-13); V4L builds name a sysfs path instead.
_RSUSB_PORT = re.compile(r"(?P<device>\d+-\d+(?:\.\d+)*)-(?P<address>\d+)")


def _realsense_port_identity(
    port: str, usb_devices: Path = Path("/sys/bus/usb/devices")
) -> str | None:
    """USB identity behind a RealSense physical_port, from either SDK backend."""
    match = _RSUSB_PORT.fullmatch(port)
    if match is None:
        return _usb_parent_identity(Path(port))
    device = usb_devices / match["device"]
    try:
        # The port path alone could name whatever was plugged in after enumeration.
        if (device / "devnum").read_text().strip() != match["address"]:
            return None
    except OSError:
        return None
    return _usb_parent_identity(device)


def _lock_dir() -> Path:
    # Keep the pre-rename name: it interlocks with older installs on one machine.
    lock_dir = Path(tempfile.gettempdir()) / f"dropbear-cameras-{os.getuid()}"
    lock_dir.mkdir(mode=0o700, exist_ok=True)
    return lock_dir


def _rsusb() -> bool:
    """aarch64 Linux, where the realsense extra installs Dreamscale's RSUSB build."""
    return sys.platform == "linux" and platform.machine() == "aarch64"


def realsense_access_help(
    usb_devices: Path = Path("/sys/bus/usb/devices"), dev_usb: Path = Path("/dev/bus/usb")
) -> str | None:
    """How to let RSUSB open connected RealSense cameras this user cannot, if any.

    RSUSB opens cameras through /dev/bus/usb, which needs RealSense's udev rules.
    Without them it still lists the cameras, but opening one fails with "failed to
    set power state".
    """
    spec = importlib.util.find_spec("pyrealsense2") if _rsusb() else None
    if spec is None or not spec.submodule_search_locations:
        return None
    blocked = False
    for device in usb_devices.glob("*"):
        try:
            if (device / "idVendor").read_text().strip() != "8086":
                continue
            if "RealSense" not in (device / "product").read_text():
                continue
            bus, number = (int((device / key).read_text()) for key in ("busnum", "devnum"))
        except (OSError, ValueError):
            continue
        node = dev_usb / f"{bus:03d}" / f"{number:03d}"
        blocked = blocked or not os.access(node, os.R_OK | os.W_OK)
    if not blocked:
        return None
    rules = Path(spec.submodule_search_locations[0]) / "99-realsense-libusb.rules"
    if not rules.is_file():  # a build that does not ship them
        return (
            "RealSense cameras need USB access. Install RealSense's udev rules "
            "(config/99-realsense-libusb.rules in librealsense), then unplug and "
            "replug the cameras."
        )
    return (
        "RealSense cameras need USB access. Run: "
        f"sudo cp {rules} /etc/udev/rules.d/ && sudo udevadm control --reload-rules "
        "&& sudo udevadm trigger, then unplug and replug the cameras."
    )


def _realsense_start_lock():
    """Wait for, then hold, the machine-wide RealSense startup lock; None where unneeded.

    RSUSB has no cross-process device locking: enumerating or starting one camera
    while another process powers one up fails with "failed to set power state".
    Elsewhere cameras start together. Closing the returned file releases the
    lock, as does the process exiting.
    """
    if not _rsusb():
        return None
    import fcntl

    lock = (_lock_dir() / "realsense-start").open("a")
    fcntl.flock(lock, fcntl.LOCK_EX)
    return lock


# USB 2 carries roughly 35 MB/s in practice: one 640x480 RGB stream at 30 fps takes
# 28 MB/s, a 480x270 one 12 MB/s, so two wrist cameras can share a bus.
_USB2_COLOR_LIMIT = (480, 270)


def _realsense_color_profile(device, rs) -> dict:
    """Default color size for a camera: CameraSpec's own, or smaller on USB 2."""
    usb = rs.camera_info.usb_type_descriptor
    if not device.supports(usb) or not device.get_info(usb).startswith("2"):
        return {}
    sizes = set()
    for sensor in device.query_sensors():
        for profile in sensor.get_stream_profiles():
            if (
                profile.stream_type() == rs.stream.color
                and profile.format() == rs.format.rgb8
                and profile.fps() == 30
                and profile.is_video_stream_profile()
            ):
                video = profile.as_video_stream_profile()
                sizes.add((video.width(), video.height()))
    width_limit, height_limit = _USB2_COLOR_LIMIT
    fitting = [(w, h) for w, h in sizes if w <= width_limit and h <= height_limit]
    if not fitting:
        return {}
    width, height = max(fitting, key=lambda size: size[0] * size[1])
    return {"width": width, "height": height}


def _realsense_inventory():
    lock = _realsense_start_lock()
    try:
        return _enumerate_realsense()
    finally:
        if lock is not None:
            lock.close()


def _enumerate_realsense():
    import pyrealsense2 as rs

    result = []
    for device in rs.context().query_devices():
        serial = device.get_info(rs.camera_info.serial_number)
        aliases = {serial}
        asic = getattr(rs.camera_info, "asic_serial_number", None)
        if asic is not None and device.supports(asic):
            aliases.add(device.get_info(asic))
        physical = None
        if device.supports(rs.camera_info.physical_port):
            physical = _realsense_port_identity(device.get_info(rs.camera_info.physical_port))
        # On supported Linux hosts the USB parent resolves both SDK and UVC
        # aliases. If sysfs cannot establish that link, require manual identity
        # confirmation instead of inventing an independent SDK device identity.
        if physical is None:
            for usb in Path("/sys/bus/usb/devices").glob("*"):
                serial_path = usb / "serial"
                if serial_path.exists() and serial_path.read_text().strip() in aliases:
                    physical = _usb_parent_identity(usb)
                    break
        if physical is None:
            raise CameraError("Cannot resolve RealSense USB identity. Check Linux sysfs access.")
        spec = CameraSpec(
            "realsense:" + serial,
            "realsense",
            physical,
            serial,
            **_realsense_color_profile(device, rs),
        )
        result.append((spec, sorted(aliases)))
    return result


def _inventory_worker(output, inventory):
    try:
        output.put(("ok", inventory()))
    except Exception as exc:
        output.put(("error", str(exc)))


def realsense_inventory(*, timeout_s=15.0, inventory=_realsense_inventory):
    """Bounded metadata probe; closes its process before capture starts."""
    context = mp.get_context("spawn")
    output = context.Queue(maxsize=1)
    process = context.Process(target=_inventory_worker, args=(output, inventory), daemon=True)
    try:
        process.start()
        try:
            kind, value = output.get(timeout=timeout_s)
        except queue.Empty as exc:
            raise CameraError("RealSense discovery timed out. Check the USB connection.") from exc
        if kind == "error":
            raise CameraError(" ".join(text for text in (value, realsense_access_help()) if text))
        return value
    finally:
        if process.pid is not None:
            process.join(timeout=0.2)
            if process.is_alive():
                process.terminate()
                process.join(timeout=0.5)
            if process.is_alive():
                process.kill()
                process.join()
        output.close()


def discover_cameras(realsense: list | None = None) -> list[CameraSpec]:
    """USB and optional RealSense candidates; aliases share physical_id.

    realsense is a realsense_inventory() the caller already took, if any.
    """
    cameras = discover_avfoundation() if sys.platform == "darwin" else discover_uvc()
    if realsense is None and dependency_help("realsense") is None:
        realsense = realsense_inventory()
    cameras.extend(spec for spec, _ in realsense or [])
    return cameras


class _OpenCVReader:
    def __init__(self, spec: CameraSpec):
        import cv2

        self.spec = spec
        self.cap = cv2.VideoCapture(*opencv_source(spec.device))
        if not self.cap.isOpened():
            self.cap.release()
            raise CameraError(f"Cannot open {spec.device}. Check connection and video permissions.")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, spec.width * (2 if spec.backend == "zed" else 1))
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, spec.height)
        self.cap.set(cv2.CAP_PROP_FPS, spec.fps)
        self.sequence = 0

    def read(self):
        ok, bgr = self.cap.read()
        wall, mono = time.time_ns(), time.monotonic_ns()
        if not ok:
            raise CameraError("Camera disconnected. Reconnect it and restart cameras.")
        self.sequence += 1
        return RGBFrame(bgr[:, :, ::-1].copy(), wall, mono, self.sequence)

    def close(self):
        self.cap.release()


class _RealSenseReader:
    def __init__(self, spec: CameraSpec):
        import pyrealsense2 as rs

        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_device(spec.device)
        config.enable_stream(rs.stream.color, spec.width, spec.height, rs.format.rgb8, spec.fps)
        try:
            self.pipeline.start(config)
        except BaseException:
            try:
                self.pipeline.stop()
            except RuntimeError:
                pass
            raise

    def read(self):
        try:
            frames = self.pipeline.wait_for_frames(timeout_ms=1000)
        except RuntimeError as exc:
            # librealsense reports a wait timeout as a bare RuntimeError.
            raise FrameTimeout(str(exc)) from exc
        wall, mono = time.time_ns(), time.monotonic_ns()
        frame = frames.get_color_frame()
        if not frame:
            raise CameraError("RealSense color frame is missing. Check RGB stream support.")
        return RGBFrame(
            np.asanyarray(frame.get_data()).copy(), wall, mono, int(frame.get_frame_number())
        )

    def close(self):
        self.pipeline.stop()


def _native_reader(spec: CameraSpec):
    return _RealSenseReader(spec) if spec.backend == "realsense" else _OpenCVReader(spec)


def _capture_worker(spec, output, stop, factory, buffer, metadata, parent_pid):
    import fcntl
    import hashlib
    import signal
    import threading

    # Task cancellation belongs to the parent; capture persists between tasks.
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    def watch_parent():
        while True:
            if os.getppid() != parent_pid:
                # This also terminates a blocked native open/read. The device
                # lock is child-owned and stays held until this process exits.
                os._exit(1)
            time.sleep(0.2)

    threading.Thread(target=watch_parent, daemon=True).start()
    reader = None
    lock = None
    starting = None
    try:
        lock = (_lock_dir() / hashlib.sha256(spec.physical_id.encode()).hexdigest()).open("a")
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise CameraError("Camera is already in use by another Dreamscale reader.") from exc
        if spec.backend == "realsense":
            starting = _realsense_start_lock()
            if starting is not None:
                output.put(("starting", None))
        reader = factory(spec)
        output.put(("ready", None))
        previous = None
        timeouts = 0
        while not stop.is_set():
            try:
                frame = reader.read()
            except FrameTimeout as exc:
                timeouts += 1
                if timeouts < MAX_FRAME_TIMEOUTS:
                    continue
                raise CameraError(
                    f"No frames from {spec.device}. Check its USB cable and hub, "
                    "then restart cameras."
                ) from exc
            timeouts = 0
            if starting is not None:
                # Streaming: the next camera may power up now.
                starting.close()
                starting = None
            if frame.sequence == previous:
                continue
            frame.validate()
            rgb = transform_rgb(frame.rgb, spec)
            if rgb.size > len(buffer):
                raise CameraError("Camera returned more pixels than its configured dimensions.")
            # Only copying a complete frame holds this lock; native reads never
            # do. Consumers use a nonblocking acquire, including after crashes.
            if metadata.get_lock().acquire(timeout=0.1):
                try:
                    np.frombuffer(buffer, dtype=np.uint8)[: rgb.size] = rgb.reshape(-1)
                    metadata[:] = [
                        rgb.shape[0],
                        rgb.shape[1],
                        frame.timestamp_ns,
                        frame.monotonic_ns,
                        frame.sequence,
                        1,
                    ]
                    previous = frame.sequence
                finally:
                    metadata.get_lock().release()
    except BaseException as exc:
        try:
            output.put(("error", str(exc)[:1024]), timeout=0.2)
        except queue.Full:
            pass
    finally:
        try:
            if reader is not None:
                reader.close()
        finally:
            if starting is not None:
                starting.close()
            if lock is not None:
                lock.close()


class ProcessCameraSource:
    """Exclusive process-owned native camera; latest never waits for a driver.

    Native acquisition is host receive time, not a hardware exposure timestamp.
    RealSense frame numbers suppress repeated deliveries. UVC read() supplies a
    new capture; identical pixels are allowed (a stationary scene is still live).
    """

    def __init__(
        self,
        spec: CameraSpec,
        *,
        factory: Callable = _native_reader,
        open_timeout_s: float = 15.0,
        close_timeout_s: float = 1.0,
    ):
        self.spec, self.factory = spec, factory
        self.open_timeout_s, self.close_timeout_s = open_timeout_s, close_timeout_s
        self._process = None
        self._ready_deadline = self._close_deadline = None
        self._frame = None
        self._error = None

    def open(self):
        self.start()
        while not self.poll_ready(self.open_timeout_s):
            pass

    def start(self, *, inventory: Callable | None = None):
        """Check identity and spawn capture without waiting for the device.

        inventory optionally shares one RealSense enumeration across cameras.
        """
        if self._process is not None:
            raise CameraError("Camera already open.")
        if self.factory is _native_reader:
            help_text = dependency_help(self.spec.backend)
            if help_text:
                raise CameraError(help_text)
            if self.spec.device.startswith(AVFOUNDATION):
                pass  # opencv_source checks the Mac still lists this camera
            elif self.spec.backend in {"uvc", "zed"}:
                if not Path(self.spec.device).exists():
                    raise CameraError(f"Saved camera {self.spec.device} is missing; reconnect it.")
                if usb_physical_id(self.spec.device) != self.spec.physical_id:
                    raise CameraError("Camera identity changed. Visually confirm it in setup.")
            elif self.spec.backend == "realsense":
                matches = [
                    candidate
                    for candidate, aliases in (inventory or realsense_inventory)()
                    if self.spec.device in aliases
                ]
                if not matches:
                    raise CameraError(
                        " ".join(
                            text
                            for text in (
                                "Saved RealSense camera is missing. Reconnect it.",
                                realsense_access_help(),
                            )
                            if text
                        )
                    )
                if matches[0].physical_id != self.spec.physical_id:
                    raise CameraError("RealSense identity changed. Confirm it in setup.")
        self._frame, self._error = None, None
        context = mp.get_context("spawn")
        self._output = context.Queue(maxsize=2)
        self._stop = context.Event()
        self._buffer = context.RawArray("B", self.spec.width * self.spec.height * 3)
        self._metadata = context.Array("q", [0] * 6)
        self._process = context.Process(
            target=_capture_worker,
            args=(
                self.spec,
                self._output,
                self._stop,
                self.factory,
                self._buffer,
                self._metadata,
                os.getpid(),
            ),
            daemon=True,
        )
        self._ready_deadline = time.monotonic() + self.open_timeout_s
        try:
            self._process.start()
        except BaseException:
            self.close()
            raise

    def poll_ready(self, timeout_s: float = 0.0) -> bool:
        """Wait up to timeout_s for the started capture to own its device.

        Returns False while startup is pending; raises and closes on failure
        or once open_timeout_s has elapsed since start, or since the capture's
        turn came if it queued behind other RealSense cameras.
        """
        if self._process is None:
            raise CameraError("Camera is closed. Start cameras first.")
        if self._ready_deadline is None:
            return True
        remaining = self._ready_deadline - time.monotonic()
        try:
            try:
                kind, value = self._output.get(timeout=max(0.0, min(timeout_s, remaining)))
            except queue.Empty as exc:
                if remaining > timeout_s:
                    return False
                raise CameraError(
                    "Camera startup timed out. Check its connection and restart."
                ) from exc
            if kind == "error":
                raise CameraError(value)
        except BaseException:
            self.close()
            raise
        if kind == "starting":
            # Queued behind other RealSense cameras until now; time its own startup.
            self._ready_deadline = time.monotonic() + self.open_timeout_s
            return False
        self._ready_deadline = None
        return True

    def latest(self, max_age_s: float = 1.0) -> RGBFrame:
        if self._process is None:
            raise CameraError("Camera is closed. Start cameras first.")
        for _ in range(4):
            try:
                kind, value = self._output.get_nowait()
            except queue.Empty:
                break
            if kind == "error":
                self._error = value
        if self._error:
            raise CameraError(self._error)
        if not self._process.is_alive():
            raise CameraError("Camera capture stopped. Reconnect it and restart cameras.")
        if self._metadata.get_lock().acquire(block=False):
            try:
                height, width, wall, mono, sequence, valid = self._metadata[:]
                if valid and (self._frame is None or sequence != self._frame.sequence):
                    rgb = np.frombuffer(self._buffer, dtype=np.uint8)[: height * width * 3]
                    self._frame = RGBFrame(
                        rgb.reshape(height, width, 3).copy(), wall, mono, sequence
                    )
            finally:
                self._metadata.get_lock().release()
        if self._frame is None:
            raise FrameUnavailable("Waiting for the first camera frame.")
        return self._frame.validate(max_age_s)

    def begin_close(self):
        """Ask capture to stop now; close() then shares this graceful deadline."""
        if self._process is not None and self._close_deadline is None:
            self._stop.set()
            self._close_deadline = time.monotonic() + self.close_timeout_s

    def close(self):
        if self._process is not None:
            self.begin_close()
            if self._process.pid is not None:
                self._process.join(max(0.0, self._close_deadline - time.monotonic()))
                if self._process.is_alive():
                    self._process.terminate()
                    self._process.join(self.close_timeout_s)
                if self._process.is_alive():
                    self._process.kill()
                    self._process.join()
            self._output.close()
            self._process = None
        self._ready_deadline = self._close_deadline = None
        self._frame = None


class CameraReaders:
    """One owned source per physical camera, reusable across setup/inference."""

    def __init__(
        self,
        specs: list[CameraSpec],
        *,
        custom_sources=None,
        source_factory=None,
        realsense: list | None = None,
    ):
        """realsense is a recent realsense_inventory() to check RealSense cameras against."""
        if len({s.id for s in specs}) != len(specs):
            raise ValueError("Camera IDs must be unique.")
        if len({s.physical_id for s in specs}) != len(specs):
            raise ValueError("The same physical camera was selected more than once.")
        self.specs = {s.id: s for s in specs}
        self.sources = {}
        self._last_frames = {}
        # latest() may be called from more than one thread (the run loop, a HUD, a codec feed)
        self._latest_lock = threading.Lock()
        self.custom_sources = custom_sources or {}
        self.source_factory = source_factory or ProcessCameraSource
        self.realsense = realsense

    def open(self):
        if self.sources:
            raise CameraError("Cameras already open.")
        inventory = self.realsense

        def shared_inventory():
            # One RealSense enumeration serves every saved RealSense camera.
            nonlocal inventory
            if inventory is None:
                inventory = realsense_inventory()
            return inventory

        try:
            starting = []
            for spec in self.specs.values():
                source = (
                    self.custom_sources[spec.device]
                    if spec.backend == "custom"
                    else self.source_factory(spec)
                )
                self.sources[spec.id] = source
                if isinstance(source, ProcessCameraSource):
                    source.start(inventory=shared_inventory)
                    starting.append(source)
                else:
                    source.open()
            # Every capture process starts before any wait, so startup costs
            # the slowest camera rather than the sum. Each keeps its own
            # timeout, and polling all of them surfaces any failure at once.
            while starting:
                starting = [source for source in starting if not source.poll_ready()]
                if starting:
                    time.sleep(0.005)
        except BaseException:
            self.close()
            raise
        return self

    def latest(self, camera_id: str, max_age_s: float = 1.0) -> RGBFrame:
        with self._latest_lock:
            return self._latest(camera_id, max_age_s)

    def _latest(self, camera_id: str, max_age_s: float) -> RGBFrame:
        frame = self.sources[camera_id].latest(max_age_s).validate(max_age_s)
        previous = self._last_frames.get(camera_id)
        if previous is not None and previous.sequence == frame.sequence:
            return previous.validate(max_age_s)
        if previous is not None and frame.monotonic_ns < previous.monotonic_ns:
            raise CameraError("Camera acquisition time moved backwards. Restart cameras.")
        spec = self.specs[camera_id]
        if spec.backend == "custom":
            frame = RGBFrame(
                transform_rgb(frame.rgb, spec),
                frame.timestamp_ns,
                frame.monotonic_ns,
                frame.sequence,
            )
        self._last_frames[camera_id] = frame
        return frame

    def close(self):
        failures = []
        sources = list(self.sources.values())[::-1]
        for source in sources:
            # Signal every capture first so their bounded joins overlap.
            if isinstance(source, ProcessCameraSource):
                try:
                    source.begin_close()
                except Exception as exc:
                    failures.append(exc)
        for source in sources:
            try:
                source.close()
            except Exception as exc:
                failures.append(exc)
        self.sources.clear()
        self._last_frames.clear()
        if failures:
            raise CameraError(f"Camera cleanup failed: {failures[0]}")

    def __enter__(self):
        return self.open()

    def __exit__(self, *_):
        self.close()


def wait_for_frames(readers, camera_ids, *, timeout_s=5.0, max_age_s=1.0):
    """Wait for fresh frames from every mapped camera under one startup deadline.

    camera_ids is camera IDs, or a role -> camera ID mapping whose roles name
    the cameras in errors. Frames are keyed by camera ID either way.
    Sources keep the nonblocking latest() interface and original timestamps.
    Only FrameUnavailable is retried; stale frames, disconnection, invalid data
    and other source errors fail immediately. Check every source on each pass
    so a pending first camera cannot hide a terminal error in another camera.
    The caller owns open/close and must clean up if this function fails.
    """
    if any(not np.isfinite(value) or value <= 0 for value in (timeout_s, max_age_s)):
        raise ValueError("Camera readiness timeout and freshness must be positive finite seconds.")
    names = {}
    if isinstance(camera_ids, Mapping):
        names = {
            camera_id: f"{role.replace('_', ' ').title()} camera"
            for role, camera_id in camera_ids.items()
        }
        camera_ids = camera_ids.values()
    camera_ids = tuple(camera_ids)
    deadline = time.monotonic() + timeout_s
    while True:
        frames, pending = {}, []
        for camera_id in camera_ids:
            try:
                frames[camera_id] = readers.latest(camera_id, max_age_s=max_age_s)
            except FrameUnavailable:
                pending.append(camera_id)
            except CameraError as exc:
                if camera_id in names:
                    raise CameraError(f"{names[camera_id]}: {exc}") from exc
                raise
        if not pending:
            return frames
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise CameraError(
                "Timed out waiting for the first camera frame: "
                + ", ".join(names.get(camera_id, camera_id) for camera_id in pending)
                + ". Check acquisition/USB connections and restart cameras."
            )
        time.sleep(min(0.01, remaining))
