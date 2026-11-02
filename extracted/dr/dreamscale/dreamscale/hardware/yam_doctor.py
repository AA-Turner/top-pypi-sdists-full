"""Read-only YAM readiness report: never constructs arms or creates sessions."""

from __future__ import annotations

import asyncio
import subprocess
import sys
from pathlib import Path

import typer
from dreamscale_transport.rho_checkpoints import RHO_YAM_BOX_MODEL_ID

from dreamscale.constants import MODEL_BIMANUAL_YAM
from dreamscale.control import ControlPlaneClient
from dreamscale.doctor import CheckResult, format_check, format_overall

from .camera_sources import CameraReaders
from .rig_doctor import camera_checks, check_camera_imports
from .yam_can import discover_can_interfaces, locate_arms
from .yam_cli_setup import can_label
from .yam_config import DEFAULT_CONFIG_PATH, load_config
from .yam_native import check_native_pin, native_driver_detail


async def inspect_yam(
    *,
    model=MODEL_BIMANUAL_YAM,
    config_path=DEFAULT_CONFIG_PATH,
    readers_factory=CameraReaders,
    discover_can=discover_can_interfaces,
    native_check=check_native_pin,
    camera_import_check=check_camera_imports,
    control_factory=ControlPlaneClient,
    auth_config=None,
    camera_ready_timeout_s=5.0,
):
    from dreamscale.attended.model_check import local_checks
    from dreamscale.embodiments import YAM
    from dreamscale.model_names import resolve_llm_model

    model = resolve_llm_model(model)
    results = local_checks(YAM, model)
    try:
        native_check()
        detail = native_driver_detail() if native_check is check_native_pin else "checked"
        # Import in an isolated bounded interpreter catches binary/OS dependencies;
        # importing get_yam_robot does not construct it.
        if native_check is check_native_pin:
            result = await asyncio.to_thread(
                subprocess.run,
                [sys.executable, "-c", "from i2rt.robots.get_robot import get_yam_robot"],
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
            if result.returncode:
                raise RuntimeError("Native import failed: " + result.stderr[-800:])
        results.append(CheckResult("native driver", "pass", f"qualified {detail}"))
    except Exception as exc:
        results.append(CheckResult("native driver", "fail", str(exc)))
    try:
        config = load_config(config_path).validate(complete=True)
        results.append(CheckResult("rig config", "pass", str(config_path)))
    except Exception as exc:
        results.append(
            CheckResult("rig config", "fail", f"{exc} Run dreamscale robots yam setup --cli")
        )
        config = None
    if model == RHO_YAM_BOX_MODEL_ID and config is not None:
        try:
            from .yam_runner import load_end_effector_adapter

            calibration = load_end_effector_adapter(
                model, Path(config_path).with_name("yam-ee.json"), config,
                kinematics_factory=lambda _arm: None,
            )
            results.append(CheckResult(
                "end-effector calibration", "pass", calibration.calibration_id,
            ))
        except Exception as exc:
            results.append(CheckResult("end-effector calibration", "fail", str(exc)))
    inventory = discover_can()
    results.append(
        CheckResult(
            "CAN inventory",
            "pass" if inventory.interfaces else "fail",
            inventory.hint or "Passive network configuration only.",
        )
    )
    if config is not None:
        buses = {i.name: i for i in inventory.interfaces}
        located, problems = locate_arms(config, inventory)
        for side, arm in located.arms.items():
            if side in problems:
                results.append(CheckResult(f"{side} CAN", "fail", problems[side]))
                continue
            bus = buses.get(arm.can_interface)
            ready = (
                bus is not None
                and bus.up
                and bus.bitrate == 1000000
                and bus.state == "ERROR-ACTIVE"
            )
            results.append(
                CheckResult(
                    f"{side} CAN",
                    "pass" if ready else "fail",
                    (can_label(bus) + " · expected up / ERROR-ACTIVE / 1000000 bit/s")
                    if bus
                    else f"{arm.can_interface} unavailable; reconnect/configure adapter",
                )
            )
            if bus and arm.adapter_id is None:
                results.append(CheckResult(
                    f"{side} adapter", "fail",
                    f"Not pinned: {arm.can_interface} can name the other arm after a reboot. "
                    "Run dreamscale robots yam setup and save.",
                ))
        try:
            roles = YAM.roles_for(model, config.roles)
        except ValueError as exc:
            results.append(CheckResult("model cameras", "fail", str(exc)))
        else:
            results += await asyncio.to_thread(
                camera_checks, config, roles, model=model, readers_factory=readers_factory,
                import_check=camera_import_check, ready_timeout_s=camera_ready_timeout_s,
            )
    from dreamscale.attended.model_check import cloud_checks

    results += await cloud_checks(
        YAM, model, auth_config=auth_config, control_factory=control_factory,
    )
    results.append(
        CheckResult(
            "physical validation",
            "skip",
            "Arm sides, motor control, gripper calibration and task quality are unvalidated. "
            "Confirm cabling/views in attended setup before connecting.",
        )
    )
    return results


def run_yam_doctor(*, config_path=DEFAULT_CONFIG_PATH, model=MODEL_BIMANUAL_YAM, print_fn=None):
    color = print_fn is None
    print_fn = print_fn or typer.echo
    results = asyncio.run(inspect_yam(config_path=config_path, model=model))
    for result in results:
        print_fn(format_check(result, color=color))
    print_fn("")
    print_fn(format_overall(results, label="YAM", color=color))
    if any(r.status == "fail" for r in results):
        raise RuntimeError(
            "YAM checks need attention. Correct the reported items and rerun dreamscale doctor yam."
        )
