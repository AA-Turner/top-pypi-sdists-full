"""`dreamscale run ur`: the attended runner over one Universal Robots rig (experimental).

A UR arm runs an organization's own π0.5 deployments: fine-tunes on demonstrations recorded
on this rig (6 joints and a gripper, a scene and a wrist camera). Everything else is
dreamscale.attended.
"""

from __future__ import annotations

from functools import partial

from dreamscale import errors
from dreamscale.attended.lifecycle import safe_printer
from dreamscale.attended.runner import (
    AttendedTaskRunner,
    run_attended,
    task_instructions,
    validate_run_options,
)
from dreamscale.embodiments import UR
from dreamscale.policy.remote import aconnect
from dreamscale.policy.runtime.action_smoothing import resolve_action_smoothing

from .ur_arm import arm_spec, speed_scale
from .ur_config import DEFAULT_CONFIG_PATH, GRIPPER_LABELS, load_config
from .ur_rig import URRig

__all__ = ["URTaskRunner", "preflight_lines", "run_ur"]


def _runs_on_ur(model, checkpoint) -> bool:
    """Deployments of the bases that run on this rig (DeployBase.robots)."""
    from dreamscale import deploy_bases

    base = deploy_bases.of_model(model)
    return (base is not None and UR.name in base.robots and bool(checkpoint)
            and checkpoint != "base")


def _refuse(model):
    return errors.DreamscaleError(errors.ErrorInfo(
        code="invalid_model",
        problem=f"{model} doesn't run on a UR arm",
        cause="a UR arm runs your own π0.5 deployments, fine-tuned on recordings from this rig",
        fix="pass one with --deployment <account>/<slug>; list them with "
        "`dreamscale deployments list`",
    ))


class URTaskRunner(AttendedTaskRunner):
    """The attended runner for one UR rig connection; see AttendedTaskRunner."""

    def __init__(self, rig, *, model, connect=aconnect, **options):
        if not _runs_on_ur(model, options.get("checkpoint")):
            raise _refuse(model)
        super().__init__(rig, embodiment=UR, model=model, connect=connect, **options)


def preflight_lines(config, roles) -> list[str]:
    arm = config.arm
    cameras = ", ".join(
        f"{role}: {config.camera(role).backend} {config.camera(role).id}" for role in roles
    )
    scale = speed_scale(arm.model)
    lines = [
        f"Arm: {arm_spec(arm.model).label} at {arm.host} · gripper: "
        f"{GRIPPER_LABELS[config.gripper.type]}",
        f"Cameras: {cameras}",
    ]
    if scale < 1:
        lines.append(f"Speed and tracking caps scaled to {scale:.0%} for this arm's reach.")
    return [
        *lines,
        f"The {arm.program} program starts from here in Remote control; in Local control "
        "press Play on the pendant when asked. Keep the E-stop in reach.",
    ]


def run_ur(
    *,
    model,
    instruction=None,
    config_path=DEFAULT_CONFIG_PATH,
    mode="async",
    max_actions=None,
    keep_warm=300,
    region="available",
    provider=None,
    speed=None,
    rtc="auto",
    checkpoint=None,
    context="auto",
    max_joint_step=UR.max_joint_step,
    max_joint_velocity=UR.max_joint_velocity,
    action_smoothing="auto",
    smoothing_new_weight=None,
    smoothing_correction_steps=None,
    smoothing_reference_speed=None,
    trace_dir=None,
    trace_images=False,
    hud=False,
    hud_job=None,
    recorder=None,
    steady_send=None,
    connect=None,
    input_fn=input,
    print_fn=print,
    rig_factory=URRig,
    hud_platform=None,
):
    if connect is None:
        connect = aconnect
    print_fn = safe_printer(print_fn)
    instruction = task_instructions(instruction)
    if not _runs_on_ur(model, checkpoint):
        raise _refuse(model)
    contract, strategy = validate_run_options(
        model, label=UR.label, mode=mode, region=region, provider=provider, speed=speed,
        keep_warm=keep_warm, rtc=rtc, context=context, max_actions=max_actions,
        trace_dir=trace_dir, trace_images=trace_images, action_smoothing=action_smoothing,
        smoothing_new_weight=smoothing_new_weight,
        smoothing_correction_steps=smoothing_correction_steps,
        smoothing_reference_speed=smoothing_reference_speed,
    )
    resolve_action_smoothing(strategy, contract)
    config = load_config(config_path).validate(complete=True)
    roles = UR.roles_for(model, config.roles)
    hud_session = None
    if hud:
        from dreamscale.integrations.hud_recorder import HudJob

        hud_session = HudJob(
            model=model, robot=UR.label, name=hud_job, platform=hud_platform,
            print_fn=print_fn,
        )

    def preflight():
        for line in preflight_lines(config, roles):
            print_fn(line)

    def make_runner(rig, lifecycle):
        return URTaskRunner(
            rig,
            lifecycle=lifecycle,
            connect=partial(connect, steady_send=steady_send)
            if steady_send is not None else connect,
            model=model,
            mode=mode,
            keep_warm=keep_warm,
            region=region,
            provider=provider,
            speed=speed,
            rtc=rtc,
            checkpoint=checkpoint,
            context=context,
            print_fn=print_fn,
            strategy=strategy,
            trace_dir=trace_dir,
            trace_images=trace_images,
            hud=hud_session,
            recorder=recorder,
        )

    try:
        run_attended(
            embodiment=UR,
            preflight=preflight,
            make_rig=lambda: rig_factory(
                config, roles=roles, chunk_size=contract.chunk_size,
                max_joint_step=max_joint_step, max_joint_velocity=max_joint_velocity,
            ),
            make_runner=make_runner,
            instruction=instruction,
            max_actions=max_actions,
            input_fn=input_fn,
            print_fn=print_fn,
        )
    finally:
        if hud_session is not None:
            hud_session.close()
        if recorder is not None:
            recorder.close()
