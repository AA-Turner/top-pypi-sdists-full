"""Franka readiness report. Never moves the arm or the gripper, never creates a session."""

from __future__ import annotations

import asyncio
import json
import platform
import resource
import subprocess
import sys
from pathlib import Path

import typer
from dreamscale_transport import catalog

from dreamscale.control import ControlPlaneClient
from dreamscale.doctor import CheckResult, format_check, format_overall

from .camera_sources import CameraReaders
from .franka_arm import FCI_PROTOCOLS, install_hint, joint_limits
from .franka_config import DEFAULT_CONFIG_PATH, FrankaConfig, load_config
from .rig_doctor import camera_checks, check_camera_imports

SETUP = "dreamscale robots franka setup"


def realtime_checks(*, sys_root=Path("/"), rlimit=resource.getrlimit) -> list[CheckResult]:
    results = []
    if sys.platform != "linux" or platform.machine().lower() not in {"x86_64", "amd64"}:
        return [CheckResult(
            "host", "fail",
            "Franka control needs x86_64 Linux on the computer cabled to the control box.",
        )]
    realtime = sys_root / "sys/kernel/realtime"
    preempt_rt = realtime.exists() and realtime.read_text().strip() == "1"
    results.append(CheckResult(
        "real-time kernel", "pass" if preempt_rt else "fail",
        f"{platform.release()} (PREEMPT_RT)" if preempt_rt else
        f"{platform.release()} is not PREEMPT_RT. libfranka's 1 kHz loop needs a real-time "
        "kernel; see Franka's 'Setting up the real-time kernel'.",
    ))
    soft, _ = rlimit(resource.RLIMIT_RTPRIO)
    unlimited = getattr(resource, "RLIM_INFINITY", -1)
    ok = soft == unlimited or soft >= 80
    results.append(CheckResult(
        "real-time priority", "pass" if ok else "fail",
        f"rtprio limit {soft}" if ok else
        f"rtprio limit is {soft}. Add your user to a group with 'rtprio 99' and "
        "'memlock unlimited' in /etc/security/limits.d, then log in again.",
    ))
    return results


def probe_arm(host, *, run=subprocess.run, timeout_s=20.0) -> dict:
    """The read-only probe in a child process, so a native crash or hang stays there."""
    try:
        result = run(
            [sys.executable, "-m", "dreamscale.hardware.franka_probe", host, "--gripper"],
            capture_output=True, text=True, timeout=timeout_s, check=False,
        )
    except subprocess.TimeoutExpired:
        return {"status": "timeout"}
    for line in reversed(result.stdout.splitlines()):
        if line.startswith("{"):
            return json.loads(line)
    return {"status": "crashed", "detail": (result.stderr or result.stdout)[-600:]}


def arm_checks(config: FrankaConfig, probed: dict) -> list[CheckResult]:
    host = config.arm.host
    status = probed.get("status")
    if status == "missing":
        return [CheckResult("franky", "fail", "franky isn't installed. Run " + SETUP + ".")]
    build = probed.get("libfranka")
    franky = CheckResult(
        "franky", "pass",
        f"libfranka {build}, FCI protocol {FCI_PROTOCOLS.get(build, 'unknown')}",
    )
    if status == "unreachable":
        return [franky, CheckResult(
            "FCI connection", "fail",
            f"No answer from {host}. Check the cable to the control box, that the "
            "computer has an address on the robot's network, and that FCI is activated in Desk.",
        )]
    if status == "incompatible":
        server = probed.get("server")
        return [franky, CheckResult(
            "FCI connection", "fail",
            f"The robot speaks FCI protocol {server}, this franky build speaks "
            f"{probed.get('library')}. " + (install_hint(server) if server else ""),
        )]
    if status != "connected":
        return [franky, CheckResult(
            "FCI connection", "fail", f"Probe {status}: {probed.get('detail', '')}".strip(),
        )]
    results = [franky, CheckResult("FCI connection", "pass", f"{host}, read-only")]
    mode, errors = probed.get("mode"), probed.get("errors")
    if errors:
        results.append(CheckResult(
            "arm state", "fail",
            f"{errors}. Clear the cause, then run dreamscale robots franka recover.",
        ))
    elif mode != "Idle":
        from .franka_arm import _mode_help

        results.append(CheckResult("arm state", "fail", _mode_help(mode)))
    else:
        results.append(CheckResult("arm state", "pass", "Idle, no errors"))
    limits = joint_limits(config.arm.model)
    q = probed.get("q") or []
    outside = [
        f"joint {i + 1} {v:.3f}" for i, v in enumerate(q)
        if not limits[i, 0] <= v <= limits[i, 1]
    ]
    results.append(CheckResult(
        "joint limits", "fail" if outside else "pass",
        f"{', '.join(outside)} outside the {config.arm.model.upper()} command range; guide "
        "the arm inward in Desk." if outside else
        f"{config.arm.model.upper()} pose inside its command range",
    ))
    if config.gripper.type == "franka_hand":
        hand = probed.get("gripper") or {}
        if "error" in hand:
            results.append(CheckResult("gripper", "fail", f"Franka Hand: {hand['error']}"))
        elif not hand.get("max_width", 0) > 0:
            results.append(CheckResult(
                "gripper", "fail", "The Franka Hand has no measured width. Home it in Desk.",
            ))
        else:
            results.append(CheckResult(
                "gripper", "pass",
                f"Franka Hand {hand['width'] * 1000:.1f} of {hand['max_width'] * 1000:.1f} mm",
            ))
    elif config.gripper.type == "none":
        results.append(CheckResult("gripper", "skip", "No gripper configured"))
    else:
        results.append(CheckResult(
            "gripper", "fail", f"The {config.gripper.type} driver isn't available yet.",
        ))
    return results


async def inspect_franka(
    *,
    model,
    config_path=DEFAULT_CONFIG_PATH,
    probe=probe_arm,
    readers_factory=CameraReaders,
    camera_import_check=check_camera_imports,
    host_checks=realtime_checks,
    control_factory=ControlPlaneClient,
    auth_config=None,
):
    from dreamscale.attended.model_check import cloud_checks, local_checks
    from dreamscale.embodiments import FRANKA, RoleMismatch
    from dreamscale.model_names import resolve_llm_model

    model = resolve_llm_model(model)
    results = local_checks(FRANKA, model)
    results += host_checks()
    try:
        config = load_config(config_path).validate(complete=True)
        results.append(CheckResult("rig file", "pass", str(config_path)))
    except Exception as exc:
        results.append(CheckResult("rig file", "fail", f"{exc} Run {SETUP}."))
        config = None
    if config is not None:
        results += arm_checks(config, await asyncio.to_thread(probe, config.arm.host))
        try:
            roles = FRANKA.roles_for(model, config.roles) if model in FRANKA.policy_models else ()
        except RoleMismatch as exc:
            results.append(CheckResult("model cameras", "fail", str(exc)))
            roles = ()
        if roles:
            unused = sorted(set(config.roles) - set(roles))
            note = f"; {', '.join(unused)} not used by this model" if unused else ""
            results.append(CheckResult("model cameras", "pass", ", ".join(roles) + note))
            results += await asyncio.to_thread(
                camera_checks, config, roles, model=model, readers_factory=readers_factory,
                import_check=camera_import_check,
            )
    results += await cloud_checks(
        FRANKA, model, auth_config=auth_config, control_factory=control_factory,
    )
    results.append(CheckResult(
        "physical validation", "skip",
        "Doctor never moves the arm. Confirm each camera's view in setup before running.",
    ))
    return results


# The model `dreamscale doctor franka` checks when none is given (the catalog's).
DEFAULT_MODEL = next(entry.id for entry in catalog.CATALOG
                     if entry.client.robot == "franka" and entry.client.doctor_default)


def run_franka_doctor(*, config_path=DEFAULT_CONFIG_PATH, model=DEFAULT_MODEL, print_fn=None):
    color = print_fn is None
    print_fn = print_fn or typer.echo
    results = asyncio.run(inspect_franka(config_path=config_path, model=model))
    for result in results:
        print_fn(format_check(result, color=color))
    print_fn("")
    print_fn(format_overall(results, label="Franka", color=color))
    if any(r.status == "fail" for r in results):
        raise RuntimeError(
            "Franka checks need attention. Correct the reported items and rerun "
            "dreamscale doctor franka."
        )
