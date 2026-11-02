"""dreamscale doctor — setup checks (spec §8): Python, API key, calibration format
(lerobot v2.1↔v3.0), camera presence + static camera coach, dependency pins."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from importlib import metadata, resources
from pathlib import Path
from typing import Any

import numpy as np
import typer

from dreamscale import errors
from dreamscale.config import (
    DEFAULT_HOME,
    HOME_ENV,
    LEGACY_HOME,
    LEGACY_HOME_ENV,
    dreamscale_home,
    legacy_home_in_use,
    load_config,
)
from dreamscale.hardware.cameras import OpenCVCameraProber
from dreamscale.hardware.ports import probe_serial_port
from dreamscale.model_names import public_model

LEROBOT_PIN = "0.6.1"
GOLDEN_PATH_URL = "https://docs.dreamscalelabs.com/robots/so101"


@dataclass
class CheckResult:
    name: str
    status: str  # "pass" | "warn" | "fail" | "skip"
    detail: str = ""
    error: errors.DreamscaleError | None = None


def calibration_format(path: Path) -> str:
    """Classify a calibration file: missing | v2_legacy | v3 | invalid."""
    if not path.exists():
        return "missing"
    try:
        data = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return "invalid"
    if not isinstance(data, dict) or not data:
        return "invalid"
    if "motor_names" in data or "calib_mode" in data:
        return "v2_legacy"
    required = {"id", "drive_mode", "homing_offset", "range_min", "range_max"}
    if all(isinstance(value, dict) and required <= set(value) for value in data.values()):
        return "v3"
    if all(isinstance(value, list) for value in data.values()):
        return "v2_legacy"
    return "invalid"


def compose_coach_preview(frame: np.ndarray) -> Path:
    """Side-by-side: reference framing (left) vs the user's capture (right)."""
    from PIL import Image

    with resources.as_file(
        resources.files("dreamscale.assets") / "camera_reference.jpg"
    ) as ref_path:
        reference = Image.open(ref_path).convert("RGB")
    captured = Image.fromarray(frame[..., ::-1])  # OpenCV BGR → RGB
    height = 480

    def fit(image: Image.Image) -> Image.Image:
        return image.resize((max(1, int(image.width * height / image.height)), height))

    reference, captured = fit(reference), fit(captured)
    canvas = Image.new("RGB", (reference.width + captured.width, height), "white")
    canvas.paste(reference, (0, 0))
    canvas.paste(captured, (reference.width, 0))
    out = dreamscale_home() / "doctor_preview.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, quality=85)
    return out


def _open_viewer(path: Path) -> None:
    try:
        if sys.platform == "darwin":
            subprocess.Popen(["open", str(path)])
        elif sys.platform.startswith("linux"):
            subprocess.Popen(["xdg-open", str(path)])
    except OSError:
        pass  # headless box — the path is printed either way


def _check_python() -> CheckResult:
    version = f"{sys.version_info.major}.{sys.version_info.minor}"
    if (3, 11) <= sys.version_info[:2] < (3, 15):
        return CheckResult("python", "pass", version)
    return CheckResult(
        "python",
        "fail",
        f"{version} — dreamscale requires Python >=3.11,<3.15",
        error=errors.catalog(
            "python_version_unsupported",
            python_version=version,
        ),
    )


def _check_lerobot_pin() -> CheckResult:
    try:
        version = metadata.version("lerobot")
    except metadata.PackageNotFoundError:
        return CheckResult("lerobot pin", "fail", "lerobot not installed",
                           error=errors.catalog("so101_not_installed"))
    if version == LEROBOT_PIN:
        return CheckResult("lerobot pin", "pass", version)
    return CheckResult(
        "lerobot pin", "fail", f"{version} != {LEROBOT_PIN}",
        error=errors.catalog("dependency_pin_mismatch",
                             detail=f"lerobot {version} installed; dreamscale is tested "
                                    f"against {LEROBOT_PIN}"))


def _check_api_key(config) -> CheckResult:
    if config.api_key:
        source = getattr(config, "api_key_source", None)
        where = {"DREAMSCALE_API_KEY": " (from DREAMSCALE_API_KEY)", "login": " (from login)"}
        return CheckResult("api key", "pass", "configured" + where.get(source, ""))
    return CheckResult("api key", "fail", "missing", error=errors.catalog("not_configured"))


def _check_camera_codec(config) -> CheckResult:
    from dreamscale.camera_codec import check_device

    status, detail, fix = check_device(config.camera_codec)
    error = None
    if status == "fail":
        error = errors.DreamscaleError(errors.ErrorInfo(
            code="camera_codec_device", problem=f"camera codec device: {detail}",
            cause="the [camera_codec] device in config.toml is not ready", fix=fix or "",
        ))
    return CheckResult("camera codec", status, detail, error=error)


def _check_sim_extra() -> CheckResult:
    missing = [
        name for name in ("mujoco", "robosuite")
        if importlib.util.find_spec(name) is None
    ]
    if not missing:
        return CheckResult("sim dependencies", "pass", "MuJoCo + robosuite installed")
    return CheckResult(
        "sim dependencies",
        "fail",
        ", ".join(missing),
        error=errors.catalog("sim_not_installed"),
    )


def _check_robot_port(config, port_probe: Callable[[str], str]) -> CheckResult:
    if config.robot_port is None:
        return CheckResult("robot port", "fail", "not configured",
                           error=errors.catalog("robot_port_not_found",
                                                port="(none configured)"))
    outcome = port_probe(config.robot_port)
    if outcome == "ok":
        return CheckResult("robot port", "pass", config.robot_port)
    if outcome == "permission_denied":
        return CheckResult("robot port", "fail", config.robot_port,
                           error=errors.catalog("serial_permission_denied",
                                                port=config.robot_port))
    return CheckResult("robot port", "fail", config.robot_port,
                       error=errors.catalog("robot_port_not_found", port=config.robot_port))


def _check_calibration(config) -> CheckResult:
    path = Path(config.calibration_path).expanduser()
    fmt = calibration_format(path)
    if fmt == "v3":
        return CheckResult("calibration", "pass", str(path))
    details = {
        "missing": f"no calibration file at {path}",
        "v2_legacy": "v2.1-format calibration found — lerobot 0.6.1 needs the v3.0 format",
        "invalid": f"unreadable calibration file at {path}",
    }
    return CheckResult("calibration", "fail", fmt,
                       error=errors.catalog("calibration_mismatch", detail=details[fmt]))


def _camera_capture_failure(role: str, index: int, prober) -> CheckResult:
    if index in prober.list_cameras():
        return CheckResult("camera", "fail", f"{role} index {index}",
                           error=errors.catalog("camera_busy", index=index))
    return CheckResult("camera", "fail", f"{role} index {index}",
                       error=errors.catalog("camera_missing", index=index))


def _check_cameras(config, prober, interactive: bool, input_fn, print_fn,
                   open_viewer) -> CheckResult:
    if config.camera_index is None or config.wrist_camera_index is None:
        return CheckResult(
            "camera", "fail", "side and wrist not configured",
            error=errors.catalog("camera_pair_not_configured"),
        )
    side_index = int(config.camera_index)
    wrist_index = int(config.wrist_camera_index)
    if side_index == wrist_index:
        return CheckResult(
            "camera", "fail", f"side and wrist both index {side_index}",
            error=errors.catalog("camera_pair_not_configured"),
        )
    frame = prober.capture_preview(side_index)
    if frame is None:
        return _camera_capture_failure("side", side_index, prober)
    wrist_frame = prober.capture_preview(wrist_index)
    if wrist_frame is None:
        return _camera_capture_failure("wrist", wrist_index, prober)
    preview = compose_coach_preview(frame)
    detail = f"side index {side_index}; wrist index {wrist_index}; coach preview: {preview}"
    if interactive:
        print_fn(f"Coach preview saved to {preview} (left: reference, right: yours)")
        open_viewer(preview)
        answer = input_fn("Does your framing roughly match the reference "
                          "(side angle, whole arm in frame)? [y/N] ")
        if answer.strip().lower() != "y":
            return CheckResult(
                "camera", "fail",
                f"framing mismatch — placement guide: {GOLDEN_PATH_URL}",
                error=errors.catalog("camera_missing", index=side_index))
    return CheckResult("camera", "pass", detail)


def _hardware_checks(*, config, interactive, port_probe, prober, calibrate_runner,
                     input_fn, print_fn, open_viewer, model=None) -> list[CheckResult]:
    results = [
        _check_robot_port(config, port_probe),
        _check_calibration(config),
    ]
    if results[-1].status == "fail" and interactive:
        if input_fn(
            "Run dreamscale robots so101 calibrate now? [y/N] "
        ).strip().lower() == "y":
            runner = calibrate_runner if calibrate_runner is not None else _run_calibrate
            runner()
            results[-1] = _check_calibration(config)
    from dreamscale.hardware.rig_file import rig_file_path

    if rig_file_path("so101").exists():
        results += _check_rig_cameras(model, interactive, input_fn, print_fn, open_viewer)
    else:
        camera = _check_cameras(config, prober, interactive, input_fn, print_fn, open_viewer)
        if camera.status == "pass":
            camera = CheckResult(camera.name, "warn", camera.detail + "; cameras are saved "
                                 "by index, which can change: rerun dreamscale robots so101 "
                                 "setup to save them by identity")
        results.append(camera)
    return results


def _check_rig_cameras(model, interactive, input_fn, print_fn, open_viewer,
                       *, prober=None) -> list[CheckResult]:
    """The rig file's side and wrist cameras through the shared per-role checks, then
    the framing coach on the side view."""
    from dreamscale.embodiments import SO101
    from dreamscale.hardware.cameras import RigCameraProber
    from dreamscale.hardware.rig_doctor import camera_checks
    from dreamscale.hardware.so101_config import load_config as load_rig

    rig = load_rig()
    try:
        roles = SO101.roles_for(model or SO101.policy_models[0], rig.roles)
    except ValueError:
        return [CheckResult("camera", "fail", "side and wrist not configured",
                            error=errors.catalog("camera_pair_not_configured"))]
    results = camera_checks(rig, roles, model=model)
    if not interactive or any(r.status == "fail" for r in results):
        return results
    frame = (prober or RigCameraProber()).capture_preview(rig.camera("side"))
    if frame is None:
        return results
    preview = compose_coach_preview(frame)
    print_fn(f"Coach preview saved to {preview} (left: reference, right: yours)")
    open_viewer(preview)
    answer = input_fn("Does your framing roughly match the reference "
                      "(side angle, whole arm in frame)? [y/N] ")
    if answer.strip().lower() != "y":
        results.append(CheckResult(
            "camera framing", "fail", f"framing mismatch — placement guide: {GOLDEN_PATH_URL}",
        ))
    return results


_STATUS_MARKS = {
    "pass": ("✓", "green"), "warn": ("!", "yellow"), "fail": ("✗", "red"),
    "skip": ("·", "bright_black"),
}


def format_check(result: CheckResult, *, color: bool = False) -> str:
    icon, fg = _STATUS_MARKS[result.status]
    suffix = f": {result.detail}" if result.detail else ""
    if color:
        icon = typer.style(icon, fg=fg, bold=True)
        if result.status == "skip":
            return f"{icon} {typer.style(result.name + suffix, fg=fg)}"
    return f"{icon} {result.name}{suffix}"


def format_overall(results: list[CheckResult], *, label: str = "",
                   color: bool = False) -> str:
    """One-line verdict, e.g. '✗ Core checks failed (1 failed, 1 passed, 1 skipped)'."""
    counts = {status: sum(r.status == status for r in results) for status in _STATUS_MARKS}
    status = "fail" if counts["fail"] else "pass"
    tally = ", ".join(
        f"{counts[key]} {word}"
        for key, word in (
            ("fail", "failed"), ("warn", "warned"), ("pass", "passed"), ("skip", "skipped"),
        )
        if counts[key]
    )
    noun = f"{label} checks" if label else "checks"
    icon, fg = _STATUS_MARKS[status]
    # Capitalize a lowercase mode ("core"), never a product's own spelling ("xArm 7").
    noun = f"{noun[0].upper()}{noun[1:]}" if noun.islower() else noun
    line = f"{icon} {noun} {status}ed ({tally})"
    return typer.style(line, fg=fg, bold=True) if color else line


def _print_results(results: list[CheckResult], *, print_fn, color: bool) -> None:
    for result in results:
        print_fn(format_check(result, color=color))
        if result.error is not None:
            print_fn(result.error.render())


def run_doctor(*, mode: str = "core",
               interactive: bool = True,
               port_probe: Callable[[str], str] = probe_serial_port,
               prober: Any = None,
               calibrate_runner: Callable[[], None] | None = None,
               input_fn: Callable[[str], str] = input,
               print_fn: Callable[[str], None] | None = None,
    open_viewer: Callable[[Path], None] = _open_viewer,
               model: str | None = None) -> list[CheckResult]:
    # Color only the default terminal output; typer.echo drops it when piped.
    color = print_fn is None
    print_fn = print_fn or typer.echo
    mode = mode.lower()
    if mode == "hardware":
        mode = "so101"
    if mode not in {"core", "so101", "sim", "all"}:
        raise errors.DreamscaleError(errors.ErrorInfo(
            code="unknown_doctor_mode",
            problem=f"unknown doctor mode {mode!r}",
            cause="doctor expects one of: core, so101, sim, all",
            fix="choose the check set that matches what you are trying to run",
        ))
    config = load_config()
    prober = prober if prober is not None else OpenCVCameraProber()
    results: list[CheckResult] = [
        _check_python(),
        _check_api_key(config),
    ]
    if config.camera_codec.get("device"):  # only robots with a camera codec device
        results.append(_check_camera_codec(config))

    if mode in {"so101", "all"}:
        print_fn("Dreamscale doctor (SO-101 hardware)")
        results += [_check_lerobot_pin(), *_hardware_checks(
            config=config,
            model=model,
            interactive=interactive,
            port_probe=port_probe,
            prober=prober,
            calibrate_runner=calibrate_runner,
            input_fn=input_fn,
            print_fn=print_fn,
            open_viewer=open_viewer,
        )]

    if model is not None:
        import asyncio

        from dreamscale.attended.model_check import cloud_checks, local_checks
        from dreamscale.embodiments import SO101
        from dreamscale.model_names import resolve_llm_model

        model = resolve_llm_model(model)
        results += local_checks(SO101, model)
        results += asyncio.run(cloud_checks(SO101, model, auth_config=config))

    if mode in {"sim", "all"}:
        if mode == "all":
            print_fn("")
        print_fn("Dreamscale doctor (LIBERO sim)")
        results.append(_check_sim_extra())

    _print_results(results, print_fn=print_fn, color=color)
    if (
        not (os.environ.get(HOME_ENV) or os.environ.get(LEGACY_HOME_ENV))
        and legacy_home_in_use()
    ):
        print_fn(f"Using {LEGACY_HOME} from before the rename; new installs use {DEFAULT_HOME}.")

    all_passed = all(result.status != "fail" for result in results)
    label = {"so101": "hardware", "all": ""}.get(mode, mode)
    print_fn("")
    print_fn(format_overall(results, label=label, color=color))
    if not all_passed:
        rerun = f"dreamscale doctor {mode}" + (f" --model {public_model(model)}" if model else "")
        print_fn(f"Fix the failures above, then re-run: {rerun}")
    return results


def run_so101_doctor(*, model: str | None = None, **options) -> list[CheckResult]:
    """`dreamscale doctor so101 [--model M]`: hardware, then the model's cloud access."""
    return run_doctor(mode="so101", model=model, **options)


def _run_calibrate() -> None:
    from dreamscale.calibrate import run_calibrate

    run_calibrate()
