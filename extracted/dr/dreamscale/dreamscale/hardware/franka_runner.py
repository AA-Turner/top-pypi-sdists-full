"""`dreamscale run franka`: the attended runner over one Franka rig.

Franka contributes its rig and the camera roles each model needs; everything else is
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
from dreamscale.embodiments import FRANKA
from dreamscale.model_names import public_model
from dreamscale.policy.deployment import runs_robot_deployments
from dreamscale.policy.remote import aconnect
from dreamscale.policy.runtime.action_smoothing import resolve_action_smoothing

from .franka_config import DEFAULT_CONFIG_PATH, load_config
from .franka_rig import FrankaRig

__all__ = ["FrankaTaskRunner", "preflight_lines", "run_franka"]


def _runs_on_franka(model, checkpoint):
    # A deployment built for the Franka runs here too (the CLI checks its robot: a Cosmos 3
    # DROID-preset deployment, deploy_bases.cosmos3.runner), as on YAM.
    return model in FRANKA.policy_models or (runs_robot_deployments(model) and bool(checkpoint))


class FrankaTaskRunner(AttendedTaskRunner):
    """The attended runner for one Franka rig connection; see AttendedTaskRunner."""

    def __init__(self, rig, *, model, connect=aconnect, **options):
        if not _runs_on_franka(model, options.get("checkpoint")):
            raise ValueError(f"{public_model(model)} doesn't run on Franka. {errors.SEE_MODELS}")
        super().__init__(rig, embodiment=FRANKA, model=model, connect=connect, **options)


def preflight_lines(config, roles) -> list[str]:
    arm = config.arm
    cameras = ", ".join(
        f"{role.replace('_', ' ')}: {config.camera(role).backend} {config.camera(role).id}"
        for role in roles
    )
    return [
        f"Arm: {arm.model.upper()} at {arm.host} · gripper: {config.gripper.type}",
        f"Cameras: {cameras}",
        "Confirm the arm is unlocked with FCI active in Desk, and each camera shows its view.",
    ]


def run_franka(
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
    max_joint_step=FRANKA.max_joint_step,
    max_joint_velocity=FRANKA.max_joint_velocity,
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
    input_fn=input,
    print_fn=print,
    rig_factory=FrankaRig,
    hud_platform=None,
):
    print_fn = safe_printer(print_fn)
    instruction = task_instructions(instruction)
    if not _runs_on_franka(model, checkpoint):
        raise ValueError(f"{public_model(model)} doesn't run on Franka. {errors.SEE_MODELS}")
    contract, strategy = validate_run_options(
        model, label=FRANKA.label, mode=mode, region=region, provider=provider, speed=speed,
        keep_warm=keep_warm, rtc=rtc, context=context, max_actions=max_actions,
        trace_dir=trace_dir, trace_images=trace_images, action_smoothing=action_smoothing,
        smoothing_new_weight=smoothing_new_weight,
        smoothing_correction_steps=smoothing_correction_steps,
        smoothing_reference_speed=smoothing_reference_speed,
    )
    resolve_action_smoothing(strategy, contract)
    config = load_config(config_path).validate(complete=True)
    roles = FRANKA.roles_for(model, config.roles)
    hud_session = None
    if hud:
        from dreamscale.integrations.hud_recorder import HudJob

        hud_session = HudJob(
            model=model, robot=FRANKA.label, name=hud_job, platform=hud_platform,
            print_fn=print_fn,
        )

    def preflight():
        for line in preflight_lines(config, roles):
            print_fn(line)

    def make_runner(rig, lifecycle):
        return FrankaTaskRunner(
            rig,
            lifecycle=lifecycle,
            **({"connect": partial(aconnect, steady_send=steady_send)}
               if steady_send is not None else {}),
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
            embodiment=FRANKA,
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


def recover_franka(*, config_path=DEFAULT_CONFIG_PATH, input_fn=input, print_fn=print,
                   arm_factory=None):
    """Clear a reflex or error after the operator has looked at why it happened."""
    from .franka_arm import FrankaArmError, FrankyArm

    config = load_config(config_path).validate(complete=True)
    arm = (arm_factory or (lambda: FrankyArm(config.arm.host, config.arm.model)))()
    print_fn("Recovery clears the arm's error so it can move again. Check what caused it "
             "first: contact, a limit, or a cable.")
    if input_fn("Enter to recover · Ctrl+C to cancel: ").strip():
        print_fn("Cancelled.")
        return
    arm.connect()
    try:
        if not arm.recover():
            raise FrankaArmError("Recovery failed. Check Desk for the arm's error.")
        state = arm.snapshot()
        print_fn(f"Recovered. Arm mode {state.mode}" + (f", errors {state.errors}"
                                                         if state.errors else ", no errors."))
    finally:
        arm.close()
