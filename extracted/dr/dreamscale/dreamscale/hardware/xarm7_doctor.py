"""xArm 7 readiness report. Never enables or moves the arms or the grippers, never creates a
session."""

from __future__ import annotations

import asyncio

import typer

from dreamscale.doctor import CheckResult, format_check, format_overall

from .camera_sources import CameraReaders
from .rig_doctor import camera_checks, check_camera_imports
from .xarm7_config import ARMS, DEFAULT_CONFIG_PATH, XArm7Config, load_config
from .xarm_arm import GRIPPER_LABELS, STATE_TEXT, STATES_OK, XArm, XArmError, XArmGripper

# Controller states a run starts from as they are: stopped is how an idle, released arm sits.
STATES_STOPPED = (4, 5)

SETUP = "dreamscale robots xarm7 setup"


def probe_arm(host: str, gripper: str) -> dict:
    """State only: motion is never enabled, nothing moves."""
    arm = XArm(host)
    try:
        arm.connect(control=False)
    except ImportError as exc:
        return {"status": "missing", "detail": str(exc)}
    except XArmError as exc:
        return {"status": "unreachable", "detail": str(exc)}
    try:
        state = arm.snapshot()
        probed = {
            "status": "connected", "q": state.position.tolist(), "error_code": state.error_code,
            "warn_code": state.warn_code, "mode": state.mode, "state": state.state,
        }
        if gripper != "none":
            try:
                probed["gripper_rad"] = XArmGripper(arm, gripper).state()
            except XArmError as exc:
                probed["gripper_error"] = str(exc)
        return probed
    finally:
        arm.close()


def arm_checks(config: XArm7Config, name: str, probed: dict) -> list[CheckResult]:
    arm = config.arms[name]
    label = f"{name} arm"
    status = probed.get("status")
    if status == "missing":
        return [CheckResult(
            "xarm-python-sdk", "fail", "xarm-python-sdk isn't installed. Run " + SETUP + "."
        )]
    if status != "connected":
        return [CheckResult(
            label, "fail",
            f"No answer from {arm.host}. Check the Ethernet link and that this computer has an "
            "address on the arm's network.",
        )]
    results = [CheckResult(label, "pass", f"xArm 7 at {arm.host}, read-only")]
    if probed.get("error_code"):
        results.append(CheckResult(
            f"{name} state", "fail",
            f"Error C{probed['error_code']}. Check the cause, then clear it in UFACTORY Studio.",
        ))
    elif probed.get("state") in STATES_STOPPED:
        results.append(CheckResult(
            f"{name} state", "pass", "no error, stopped; a run enables it at its current pose",
        ))
    elif probed.get("state") not in STATES_OK:
        what = STATE_TEXT.get(probed.get("state"), f"is in state {probed.get('state')}")
        results.append(CheckResult(
            f"{name} state", "warn",
            f"Arm {what}. Stop or resume it in UFACTORY Studio before a run.",
        ))
    else:
        results.append(CheckResult(f"{name} state", "pass", "no error, ready"))
    if arm.gripper == "none":
        results.append(CheckResult(f"{name} gripper", "skip", "No gripper configured"))
    elif "gripper_error" in probed:
        results.append(CheckResult(f"{name} gripper", "fail", probed["gripper_error"]))
    else:
        results.append(CheckResult(
            f"{name} gripper", "pass",
            f"{GRIPPER_LABELS[arm.gripper]} at {probed.get('gripper_rad', 0.0):.2f} rad "
            "(0 open, 0.85 closed)",
        ))
    return results


async def inspect_xarm7(
    *,
    config_path=DEFAULT_CONFIG_PATH,
    arm_probe=probe_arm,
    readers_factory=CameraReaders,
    camera_import_check=check_camera_imports,
    model=None,
    control_factory=None,
    auth_config=None,
):
    from dreamscale.embodiments import XARM7, RoleMismatch

    results = []
    try:
        config = load_config(config_path).validate(complete=True)
        results.append(CheckResult("rig file", "pass", str(config_path)))
    except Exception as exc:
        results.append(CheckResult("rig file", "fail", f"{exc} Run {SETUP}."))
        config = None
    if config is not None:
        for name in ARMS:
            arm = config.arms[name]
            results += arm_checks(
                config, name, await asyncio.to_thread(arm_probe, arm.host, arm.gripper)
            )
        try:
            roles = XARM7.roles_for(XARM7.deployment_models[0], config.roles)
        except RoleMismatch as exc:
            results.append(CheckResult("cameras", "fail", str(exc)))
            roles = ()
        if roles:
            results += await asyncio.to_thread(
                camera_checks, config, roles, readers_factory=readers_factory,
                import_check=camera_import_check,
            )
            square = [role for role in roles
                      if (c := config.camera(role)).width * 9 != c.height * 16]
            if square:
                results.append(CheckResult(
                    "camera shape", "warn",
                    f"{', '.join(square)} not 16:9; models trained on 1280x720 recordings see "
                    "a different crop. Choose a 16:9 size in setup.",
                ))
    if model is not None:
        from dreamscale.attended.model_check import deployment_checks
        from dreamscale.control import ControlPlaneClient

        from .xarm7_runner import _runs_on_xarm7

        results += await deployment_checks(
            XARM7, model, _runs_on_xarm7, auth_config=auth_config,
            control_factory=control_factory or ControlPlaneClient,
        )
    results.append(CheckResult(
        "physical validation", "skip",
        "Doctor never moves the arms. Confirm each camera's view in setup before running.",
    ))
    return results


def run_xarm7_doctor(*, config_path=DEFAULT_CONFIG_PATH, model=None, print_fn=None):
    color = print_fn is None
    print_fn = print_fn or typer.echo
    results = asyncio.run(inspect_xarm7(config_path=config_path, model=model))
    for result in results:
        print_fn(format_check(result, color=color))
    print_fn("")
    print_fn(format_overall(results, label="xArm 7", color=color))
    if any(r.status == "fail" for r in results):
        raise RuntimeError(
            "xArm 7 checks need attention. Correct the reported items and rerun "
            "dreamscale doctor xarm7."
        )
