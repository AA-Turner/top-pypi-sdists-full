"""Readiness checks every robot's doctor shares: camera imports, frames and USB links.

Each robot's doctor adds its own host and hardware probes; the camera checks are the
same per role on every robot, so a ZED on USB 2 fails the same way on YAM and Franka.
"""

from __future__ import annotations

import subprocess
import sys

from dreamscale.doctor import CheckResult

from .camera_sources import (
    USB3_MBPS,
    CameraReaders,
    camera_error_text,
    install_hint,
    usb_link_mbps,
    wait_for_frames,
)
from .rig_file import RigFile

__all__ = ["USB3_MBPS", "camera_checks", "check_camera_imports", "usb_link_mbps"]
USB_FIX = ("Use a USB 3 cable straight into a USB 3 port (with USB-C, try flipping the "
           "plug), then rerun setup.")


def check_camera_imports(config, *, run=subprocess.run):
    modules = sorted(
        {"uvc": "cv2", "zed": "cv2", "realsense": "pyrealsense2"}[s.backend]
        for s in config.cameras
        if s.backend != "custom"
    )
    for module in set(modules):
        try:
            result = run(
                [sys.executable, "-c", f"import {module}"],
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise RuntimeError(f"{module} import unavailable or timed out: {exc}") from exc
        if result.returncode:
            backend = "realsense" if module == "pyrealsense2" else "uvc"
            raise RuntimeError(
                f"{module} could not load. {install_hint(backend)} "
                "On Debian/Ubuntu install libusb-1.0-0 for RealSense; "
                "libgl1 and libglib2.0-0 for OpenCV. " + result.stderr[-800:]
            )


def stream_suits(spec, contract) -> bool:
    """A camera's configured stream covers what the model reads: the model's wire image
    and its control rate. Without a wire image the model reads full frames, so only a
    full-speed stream suits it."""
    wire = getattr(contract, "wire_image", None)
    if contract is None or wire is None:
        return False
    rate = float(getattr(contract, "action_hz", 0) or 0)
    return spec.width >= wire.width and spec.height >= wire.height and spec.fps >= rate


def _slow_link(spec, speed) -> bool:
    return speed is not None and speed < USB3_MBPS and spec.backend in {"zed", "realsense"}


def camera_checks(config, roles, *, model=None, readers_factory=None,
                  import_check=check_camera_imports, link_speed=usb_link_mbps,
                  ready_timeout_s=8.0) -> list:
    """One result per role: fresh frames at the configured mode, and the USB link.

    A camera on USB 2 still passes as a warning when its stream covers what the model
    reads (its contract's wire_image at its action_hz); otherwise, or when it streams
    nothing, it fails.
    """
    from dreamscale.model_names import public_model
    from dreamscale.policy.runtime.contract import (
        follows_server_contract,
        runtime_contract_for_model,
    )

    # A model this SDK has no contract for (an LLM, a newer model): no stream to size for.
    contract = (runtime_contract_for_model(model)
                if model and not follows_server_contract(model) else None)
    readers_factory = readers_factory or CameraReaders
    specs = {role: config.camera(role) for role in roles}
    speeds = {role: link_speed(spec) for role, spec in specs.items()}
    label = {role: f"{role.replace('_', ' ')} camera" for role in specs}
    try:
        import_check(RigFile(cameras=list(specs.values())))
    except Exception as exc:
        return [CheckResult("cameras", "fail", str(exc))]
    readers, results = None, []
    try:
        readers = readers_factory(list(specs.values()))
        readers.open()
        frames = wait_for_frames(
            readers, {role: spec.id for role, spec in specs.items()},
            timeout_s=ready_timeout_s, max_age_s=1.0,
        )
    except Exception as exc:
        for role, spec in specs.items():
            if _slow_link(spec, speeds[role]):
                results.append(CheckResult(label[role], "fail", (
                    f"{spec.backend} {spec.id} is linked at USB 2 ({speeds[role]} Mb/s) and "
                    f"can't stream {spec.width}x{spec.height} at {spec.fps} fps. " + USB_FIX
                )))
        results.append(CheckResult("cameras", "fail", camera_error_text(exc)))
        frames = None
    finally:
        if readers is not None:
            try:
                readers.close()
            except Exception as exc:
                results.append(CheckResult("camera cleanup", "fail", str(exc)))
    if frames is None:
        return results
    name = public_model(model) if model else "this model"
    for role, spec in specs.items():
        rgb = getattr(frames.get(spec.id), "rgb", None)
        size = f" {rgb.shape[1]}x{rgb.shape[0]}" if hasattr(rgb, "shape") else ""
        speed = speeds[role]
        stream = f"{spec.backend} {spec.id}: fresh{size} at {spec.fps} fps"
        if not _slow_link(spec, speed):
            link = f", USB {speed} Mb/s" if speed is not None else ""
            results.append(CheckResult(label[role], "pass", stream + link))
            continue
        wire = getattr(contract, "wire_image", None)
        need = (
            f"{wire.width}x{wire.height} at {contract.action_hz:g} Hz" if wire is not None
            else "full-resolution frames"
        )
        if stream_suits(spec, contract):
            results.append(CheckResult(label[role], "warn", (
                f"{stream} over USB 2 ({speed} Mb/s): enough for {name}, which reads {need}. "
                "For full resolution: " + USB_FIX[0].lower() + USB_FIX[1:]
            )))
        else:
            results.append(CheckResult(label[role], "fail", (
                f"{stream} over USB 2 ({speed} Mb/s) is not enough for {name}, which reads "
                f"{need}. " + USB_FIX
            )))
    return results
