"""Universal Robots readiness report. Never moves the arm or the gripper, never creates a
session."""

from __future__ import annotations

import asyncio
import socket

import typer

from dreamscale.doctor import CheckResult, format_check, format_overall

from . import robotiq
from .camera_sources import CameraReaders
from .rig_doctor import camera_checks, check_camera_imports
from .ur_arm import ROBOT_RUNNING, SAFETY_OK, URArm, URArmError, arm_spec, joint_limits
from .ur_config import DEFAULT_CONFIG_PATH, GRIPPER_LABELS, URConfig, load_config

SETUP = "dreamscale robots ur setup"


def probe_arm(host: str, model: str) -> dict:
    """RTDE state only: no control script, nothing moves."""
    arm = URArm(host, model)
    try:
        arm.connect(control=False)
    except ImportError as exc:
        return {"status": "missing", "detail": str(exc)}
    except URArmError as exc:
        return {"status": "unreachable", "detail": str(exc)}
    try:
        state = arm.snapshot()
        return {
            "status": "connected", "q": state.position.tolist(),
            "robot_mode": state.robot_mode, "safety_mode": state.safety_mode,
        }
    finally:
        arm.close()


def probe_gripper(host: str, *, connect=socket.create_connection) -> dict:
    """Status only: reading never activates or moves the gripper."""
    return robotiq.probe(host, connect=connect)


def arm_checks(config: URConfig, probed: dict) -> list[CheckResult]:
    host = config.arm.host
    status = probed.get("status")
    if status == "missing":
        return [CheckResult("ur_rtde", "fail", "ur_rtde isn't installed. Run " + SETUP + ".")]
    if status != "connected":
        return [CheckResult(
            "RTDE connection", "fail",
            f"No answer from {host}. Check the Ethernet link, that this computer has an "
            "address on the robot's network, and that RTDE is enabled under Settings > "
            "Security > Services.",
        )]
    results = [CheckResult(
        "RTDE connection", "pass", f"{arm_spec(config.arm.model).label} at {host}, read-only",
    )]
    safety, mode = probed.get("safety_mode"), probed.get("robot_mode")
    if safety not in SAFETY_OK:
        from .ur_arm import _safety_help

        results.append(CheckResult("arm state", "fail", _safety_help(safety)))
    elif mode != ROBOT_RUNNING:
        results.append(CheckResult(
            "arm state", "fail", "Arm brakes are engaged. Power it on and release the brakes "
            "on the pendant.",
        ))
    else:
        results.append(CheckResult("arm state", "pass", "powered, brakes released, no stop"))
    limits = joint_limits(config.arm.model)
    outside = [
        f"joint {i + 1} {v:.3f}" for i, v in enumerate(probed.get("q") or [])
        if not limits[i, 0] <= v <= limits[i, 1]
    ]
    results.append(CheckResult(
        "joint limits", "fail" if outside else "pass",
        f"{', '.join(outside)} outside the command range; unwind it on the pendant."
        if outside else "pose inside the command range",
    ))
    return results


def gripper_checks(config: URConfig, probed: dict) -> list[CheckResult]:
    if config.gripper.type == "none":
        return [CheckResult("gripper", "skip", "No gripper configured")]
    if "error" in probed:
        return [CheckResult("gripper", "fail", probed["error"])]
    if probed.get("FLT"):
        return [CheckResult("gripper", "fail", f"Robotiq reports fault {probed['FLT']}.")]
    active = probed.get("ACT") == 1 and probed.get("STA") == 3
    return [CheckResult(
        "gripper", "pass",
        f"{GRIPPER_LABELS[config.gripper.type]} "
        f"{'active' if active else 'not activated (a run activates it)'}, "
        f"position {probed.get('POS')}/255, via the {probed.get('via')}",
    )]


async def inspect_ur(
    *,
    config_path=DEFAULT_CONFIG_PATH,
    arm_probe=probe_arm,
    gripper_probe=probe_gripper,
    readers_factory=CameraReaders,
    camera_import_check=check_camera_imports,
):
    from dreamscale.embodiments import UR, RoleMismatch

    results = []
    try:
        config = load_config(config_path).validate(complete=True)
        results.append(CheckResult("rig file", "pass", str(config_path)))
    except Exception as exc:
        results.append(CheckResult("rig file", "fail", f"{exc} Run {SETUP}."))
        config = None
    if config is not None:
        arm = config.arm
        results += arm_checks(config, await asyncio.to_thread(arm_probe, arm.host, arm.model))
        if config.gripper.type != "none":
            results += gripper_checks(config, await asyncio.to_thread(gripper_probe, arm.host))
        else:
            results += gripper_checks(config, {})
        try:
            roles = UR.roles_for(UR.deployment_models[0], config.roles)
        except RoleMismatch as exc:
            results.append(CheckResult("cameras", "fail", str(exc)))
            roles = ()
        if roles:
            results += await asyncio.to_thread(
                camera_checks, config, roles, readers_factory=readers_factory,
                import_check=camera_import_check,
            )
    results.append(CheckResult(
        "physical validation", "skip",
        "Doctor never moves the arm. Confirm each camera's view in setup before running.",
    ))
    return results


def run_ur_doctor(*, config_path=DEFAULT_CONFIG_PATH, model=None, print_fn=None):
    color = print_fn is None
    print_fn = print_fn or typer.echo
    results = asyncio.run(inspect_ur(config_path=config_path))
    for result in results:
        print_fn(format_check(result, color=color))
    print_fn("")
    print_fn(format_overall(results, label="Universal Robots", color=color))
    if any(r.status == "fail" for r in results):
        raise RuntimeError(
            "Universal Robots checks need attention. Correct the reported items and rerun "
            "dreamscale doctor ur."
        )
