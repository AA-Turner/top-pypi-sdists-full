"""OpenARM readiness report. Only reads Anvil's control stack: never commands the arms, never
creates a session."""

from __future__ import annotations

import asyncio
import time

import typer

from dreamscale.doctor import CheckResult, format_check, format_overall

from .camera_sources import CameraError
from .openarm_config import DEFAULT_CONFIG_PATH, SETUP, OpenArmConfig, load_config
from .openarm_stack import (
    INFERENCE_CONFIG,
    JOINT_STATES,
    AnvilStack,
    StackError,
    camera_topic,
    command_topic,
    controller_name,
)

# How long the stack's topics are watched before their rates are read.
SAMPLE_S = 2.0
# A run observes at up to 30 Hz: slower joint states or frames than these make it late.
MIN_STATE_HZ = 30.0
MIN_CAMERA_HZ = 15.0
MAX_FRAME_GAP_S = 0.1
# rosbridge itself, which this program publishes commands through.
_BRIDGE_NODES = ("rosbridge",)


def probe_stack(config: OpenArmConfig, *, stack_factory=AnvilStack, sample_s=SAMPLE_S,
                sleep=time.sleep) -> dict:
    """What the stack reports, read-only: nothing is advertised or published."""
    stack = stack_factory(config.url)
    try:
        stack.open(cameras=config.cameras)
    except StackError as exc:
        return {"status": "unreachable", "detail": str(exc)}
    try:
        sleep(sample_s)
        probed = {
            "status": "connected",
            "arms_present": stack.arms_present(),
            "joints_seen": len(stack.joints_seen()),
            "state_rate": stack.rate(JOINT_STATES, sample_s),
            "controllers": stack.controllers(),
            "arms": {}, "cameras": {}, "publishers": {},
        }
        for arm in config.arms:
            entry = probed["arms"][arm] = {}
            try:
                entry["state"] = stack.arm_state(arm, max_age_s=1.0)
            except StackError as exc:
                entry["state_error"] = str(exc)
            try:
                entry["limits"] = stack.limits(arm)
            except StackError as exc:
                entry["limits_error"] = str(exc)
            probed["publishers"][arm] = stack.publishers(command_topic(arm))
        for camera in config.cameras:
            entry = probed["cameras"][camera] = {"rate": stack.rate(camera_topic(camera),
                                                                    sample_s)}
            try:
                entry["shape"] = stack.latest(camera, max_age_s=1.0).rgb.shape
            except CameraError as exc:
                entry["error"] = str(exc)
        return probed
    finally:
        stack.close()


def stack_checks(config: OpenArmConfig, probed: dict) -> list[CheckResult]:
    if probed.get("status") != "connected":
        return [CheckResult("control stack", "fail", probed.get("detail", "No answer."))]
    results = [CheckResult(
        "control stack", "pass",
        f"rosbridge at {config.url}, read-only; {probed['joints_seen']} joints reported",
    )]
    rate = probed.get("state_rate")
    if rate is None:
        results.append(CheckResult(
            "joint states", "fail", f"Nothing on {JOINT_STATES}. Check the stack is running.",
        ))
    else:
        results.append(CheckResult(
            "joint states", "pass" if rate[0] >= MIN_STATE_HZ else "warn",
            f"{rate[0]:.0f} Hz through the bridge"
            + ("" if rate[0] >= MIN_STATE_HZ else "; a run needs 30 Hz or more"),
        ))
    controllers = probed.get("controllers") or {}
    for arm in config.arms:
        entry = probed["arms"].get(arm, {})
        if "state_error" in entry:
            results.append(CheckResult(f"{arm} arm", "fail", entry["state_error"]))
            continue
        results.append(CheckResult(f"{arm} arm", "pass", "seven joints and a gripper reported"))
        name = controller_name(arm)
        state = controllers.get(name)
        if state == "active":
            results.append(CheckResult(f"{arm} control", "pass", f"{name} is active"))
        else:
            results.append(CheckResult(
                f"{arm} control", "fail",
                f"{name} is {state if state else 'not running'}, so joint commands would be "
                f"ignored. Start the stack with {INFERENCE_CONFIG}.",
            ))
        if "limits_error" in entry:
            results.append(CheckResult(f"{arm} limits", "fail", entry["limits_error"]))
        else:
            limits, position = entry["limits"], entry["state"].position
            outside = [
                f"joint {i + 1} at {position[i]:.3f} rad (limits {limits[i][0]:.3f} to "
                f"{limits[i][1]:.3f})"
                for i in range(len(limits) - 1)
                if not limits[i][0] <= position[i] <= limits[i][1]
            ]
            if outside:
                results.append(CheckResult(
                    f"{arm} limits", "warn",
                    f"{'; '.join(outside)}: outside the limits the stack describes. Check "
                    "the description matches this arm before a run.",
                ))
            else:
                results.append(CheckResult(
                    f"{arm} limits", "pass", "read from the stack's robot description",
                ))
        others = [
            node for node in probed["publishers"].get(arm) or []
            if not any(word in node for word in _BRIDGE_NODES)
        ]
        if others:
            results.append(CheckResult(
                f"{arm} commands", "warn",
                f"{', '.join(others)} also publishes this arm's targets. Stop it before a "
                "run, or the two will fight.",
            ))
    for camera in config.cameras:
        entry = probed["cameras"].get(camera, {})
        rate = entry.get("rate")
        if "error" in entry or rate is None:
            results.append(CheckResult(
                f"{camera} camera", "fail",
                entry.get("error") or f"No frames on {camera_topic(camera)}.",
            ))
            continue
        height, width = entry["shape"][:2]
        slow = rate[0] < MIN_CAMERA_HZ or rate[1] > MAX_FRAME_GAP_S
        results.append(CheckResult(
            f"{camera} camera", "warn" if slow else "pass",
            f"{width}x{height} at {rate[0]:.0f} fps through the bridge, 95% of frames "
            f"within {rate[1] * 1000:.0f} ms of the last"
            + ("; too slow for a 30 Hz run" if slow else ""),
        ))
    return results


async def inspect_openarm(
    *,
    config_path=DEFAULT_CONFIG_PATH,
    stack_probe=probe_stack,
    model=None,
    control_factory=None,
    auth_config=None,
):
    from dreamscale.embodiments import OPENARM

    results = []
    try:
        config = load_config(config_path).validate(complete=True)
        results.append(CheckResult("rig file", "pass", str(config_path)))
    except Exception as exc:
        hint = "" if SETUP in str(exc) else f" Run {SETUP}."
        results.append(CheckResult("rig file", "fail", f"{exc}{hint}"))
        config = None
    if config is not None:
        results += stack_checks(config, await asyncio.to_thread(stack_probe, config))
    if model is not None:
        from dreamscale.attended.model_check import deployment_checks
        from dreamscale.control import ControlPlaneClient

        from .openarm_runner import _runs_on_openarm

        results += await deployment_checks(
            OPENARM, model, _runs_on_openarm, auth_config=auth_config,
            control_factory=control_factory or ControlPlaneClient,
        )
    results.append(CheckResult(
        "physical validation", "skip",
        "Doctor never moves the arms. Check each camera's view in Anvil's web app before "
        "running.",
    ))
    return results


def run_openarm_doctor(*, config_path=DEFAULT_CONFIG_PATH, model=None, print_fn=None):
    color = print_fn is None
    print_fn = print_fn or typer.echo
    results = asyncio.run(inspect_openarm(config_path=config_path, model=model))
    for result in results:
        print_fn(format_check(result, color=color))
    print_fn("")
    print_fn(format_overall(results, label="OpenARM", color=color))
    if any(r.status == "fail" for r in results):
        raise RuntimeError(
            "OpenARM checks need attention. Correct the reported items and rerun "
            "dreamscale doctor openarm."
        )
