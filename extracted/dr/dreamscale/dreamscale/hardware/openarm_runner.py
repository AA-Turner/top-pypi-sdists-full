"""`dreamscale run openarm`: the attended runner over an Anvil OpenARM (experimental).

The arms run an organization's own π0.5 deployments: fine-tunes on demonstrations recorded
on this cell through Anvil's control stack (per arm seven joints and a gripper, and up to
three of its cameras). Everything else is dreamscale.attended.
"""

from __future__ import annotations

from functools import partial

from dreamscale import deploy_bases, errors
from dreamscale.attended.lifecycle import safe_printer
from dreamscale.attended.runner import (
    AttendedTaskRunner,
    _close_quietly,
    run_attended,
    task_instructions,
    validate_run_options,
)
from dreamscale.embodiments import OPENARM
from dreamscale.policy.remote import aconnect
from dreamscale.policy.runtime.action_smoothing import resolve_action_smoothing

from .openarm_config import DEFAULT_CONFIG_PATH, SETUP, embodiment_for, load_config
from .openarm_rig import OpenArmRig

__all__ = ["OpenArmTaskRunner", "preflight_lines", "run_openarm"]


def _runs_on_openarm(model, checkpoint) -> bool:
    """Deployments of the bases that run on this rig (DeployBase.robots: π0.5)."""
    base = deploy_bases.of_model(model)
    return (base is not None and OPENARM.name in base.robots and bool(checkpoint)
            and checkpoint != "base")


def _refuse(model):
    return errors.DreamscaleError(errors.ErrorInfo(
        code="invalid_model",
        problem=f"{model} doesn't run on the OpenARM",
        cause="the OpenARM runs your own deployments, fine-tuned on recordings from this rig",
        fix="pass one with --deployment <account>/<slug>; list them with "
        "`dreamscale deployments list`",
    ))


def layout_mismatch(config, deployment, ref):
    """The error for a deployment whose recording isn't laid out as the rig file says: other
    cameras, or another number of arms. None when they agree (or the session doesn't say)."""
    cameras = getattr(deployment, "camera_keys", None)
    width = getattr(deployment, "action_dim", None)
    if cameras is None or width is None:
        return None
    rig_cameras = {f"observation.images.{camera}" for camera in config.cameras}
    if set(cameras) == rig_cameras and width == config.width:
        return None
    names = ", ".join(key.rpartition(".")[2] for key in cameras)
    return errors.DreamscaleError(errors.ErrorInfo(
        code="invalid_deployment",
        problem=f"{ref} doesn't match this rig's file",
        cause=f"it reads cameras {names} and {width} joint values; the rig file names "
        f"{', '.join(config.cameras)} and {config.width} values "
        f"({' and '.join(config.arms)} arm)",
        fix=f"run {SETUP} and choose the arms and cameras the deployment was recorded with",
    ))


class OpenArmTaskRunner(AttendedTaskRunner):
    """The attended runner for one OpenARM rig connection; see AttendedTaskRunner."""

    def __init__(self, rig, *, model, config, connect=aconnect, **options):
        if not _runs_on_openarm(model, options.get("checkpoint")):
            raise _refuse(model)
        self.config = config
        super().__init__(
            rig, embodiment=embodiment_for(config), model=model, connect=connect, **options,
        )

    async def _connect_policy(self, on_progress):
        policy = await super()._connect_policy(on_progress)
        # Before anything moves: the deployment's own layout against the rig file's.
        mismatch = layout_mismatch(
            self.config, getattr(policy, "deployment", None), self.checkpoint,
        )
        if mismatch is not None:
            await _close_quietly(policy)
            raise mismatch
        keys = getattr(getattr(policy, "deployment", None), "camera_keys", None)
        if keys is not None:
            # A deployment takes its cameras in its own order, whatever the cell's.
            self.rig.send_cameras_as(keys)
        return policy


def preflight_lines(config) -> list[str]:
    place = "before" if config.gripper == "first" else "after"
    return [
        f"Arms: {', '.join(config.arms)} through Anvil's control stack at {config.url}",
        f"Layout: each arm's gripper {place} its seven joints",
        f"Cameras: {', '.join(config.cameras)}",
        "The arms follow the model from their current pose. Keep the E-stop in reach.",
    ]


def run_openarm(
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
    max_joint_step=OPENARM.max_joint_step,
    max_joint_velocity=OPENARM.max_joint_velocity,
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
    rig_factory=OpenArmRig,
    hud_platform=None,
):
    if connect is None:
        connect = aconnect
    print_fn = safe_printer(print_fn)
    instruction = task_instructions(instruction)
    if not _runs_on_openarm(model, checkpoint):
        raise _refuse(model)
    contract, strategy = validate_run_options(
        model, label=OPENARM.label, mode=mode, region=region, provider=provider, speed=speed,
        keep_warm=keep_warm, rtc=rtc, context=context, max_actions=max_actions,
        trace_dir=trace_dir, trace_images=trace_images, action_smoothing=action_smoothing,
        smoothing_new_weight=smoothing_new_weight,
        smoothing_correction_steps=smoothing_correction_steps,
        smoothing_reference_speed=smoothing_reference_speed,
    )
    resolve_action_smoothing(strategy, contract)
    config = load_config(config_path).validate(complete=True)
    embodiment = embodiment_for(config)
    hud_session = None
    if hud:
        from dreamscale.integrations.hud_recorder import HudJob

        hud_session = HudJob(
            model=model, robot=OPENARM.label, name=hud_job, platform=hud_platform,
            print_fn=print_fn,
        )

    def preflight():
        for line in preflight_lines(config):
            print_fn(line)

    def make_runner(rig, lifecycle):
        return OpenArmTaskRunner(
            rig,
            config=config,
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
            embodiment=embodiment,
            preflight=preflight,
            make_rig=lambda: rig_factory(
                config, chunk_size=contract.chunk_size,
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
