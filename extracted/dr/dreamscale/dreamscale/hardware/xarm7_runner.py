"""`dreamscale run xarm7`: the attended runner over two xArm 7s (experimental).

The arms run an organization's own deployments: fine-tunes on demonstrations recorded on
this rig (per arm seven joints and a gripper, a scene camera and one on each wrist), and
Hy-VLA deployments of the bimanual xArm 7 preset, whose end-effector pose chunks
``hy_vla_xarm7`` turns into joint targets. Everything else is dreamscale.attended.
"""

from __future__ import annotations

import importlib
from functools import partial

from dreamscale import deploy_bases, errors
from dreamscale.attended.lifecycle import safe_printer
from dreamscale.attended.runner import (
    AttendedTaskRunner,
    run_attended,
    task_instructions,
    validate_run_options,
)
from dreamscale.embodiments import XARM7
from dreamscale.policy.remote import aconnect
from dreamscale.policy.runtime.action_smoothing import resolve_action_smoothing

from .xarm7_config import ARMS, DEFAULT_CONFIG_PATH, load_config
from .xarm7_rig import XArm7Rig
from .xarm_arm import GRIPPER_LABELS

__all__ = ["XArm7TaskRunner", "preflight_lines", "run_xarm7"]


def _runs_on_xarm7(model, checkpoint) -> bool:
    """Deployments of the bases that run on this rig (DeployBase.robots: π0.5, LingBot-VLA 2.0
    and Hy-VLA)."""
    base = deploy_bases.of_model(model)
    return (base is not None and XARM7.name in base.robots and bool(checkpoint)
            and checkpoint != "base")


def _adapter_module(model):
    """The module of the end-effector adapter a base's deployments run through on this rig
    (DeployBase.robot_adapters: Hy-VLA's pose chunks), else None."""
    base = deploy_bases.of_model(model)
    path = base.robot_adapters.get(XARM7.name) if base is not None else None
    return importlib.import_module(path) if path is not None else None


def _refuse(model):
    return errors.DreamscaleError(errors.ErrorInfo(
        code="invalid_model",
        problem=f"{model} doesn't run on the xArm 7s",
        cause="the xArm 7s run your own deployments, fine-tuned on recordings from this rig",
        fix="pass one with --deployment <account>/<slug>; list them with "
        "`dreamscale deployments list`",
    ))


class XArm7TaskRunner(AttendedTaskRunner):
    """The attended runner for one xArm 7 rig connection; see AttendedTaskRunner."""

    def __init__(self, rig, *, model, connect=aconnect, end_effector_adapter=None, **options):
        if not _runs_on_xarm7(model, options.get("checkpoint")):
            raise _refuse(model)
        module = _adapter_module(model)
        if module is not None:
            # Pose chunks: FK for the state, blend + seeded IK to joints before the run loop.
            adapter = end_effector_adapter or module.ADAPTER()
            end_effector_adapter = adapter
            options["observe"] = options.get("observe") or (
                lambda ctx: adapter.observe(rig.observe(ctx), rig=rig)
            )
            # The session names the chunk; until it connects, the rig's 16 joints at 20 Hz.
            options.setdefault("execution_contract", adapter.provisional_contract())
        super().__init__(
            rig, embodiment=XARM7, model=model, connect=connect,
            end_effector_adapter=end_effector_adapter, **options,
        )

    @property
    def execution_contract(self):
        """An adapted run's (Hy-VLA's) is its bound session's (the deployment's chunk);
        otherwise the one this runner was made with."""
        bound = getattr(getattr(self, "policy", None), "execution_contract", None)
        if _adapter_module(self.model) is not None and bound is not None:
            return bound
        return self._execution_contract

    @execution_contract.setter
    def execution_contract(self, contract):
        self._execution_contract = contract

    def _require_instruction(self, instruction):
        # An adapted run (Hy-VLA's) moves the arm its label map names for the instruction:
        # refuse any other before anything moves.
        check = getattr(self.policy, "require_instruction", None)
        if _adapter_module(self.model) is not None and check is not None:
            check(instruction)

    async def start_compute(self, instruction):
        await super().start_compute(instruction)
        self._require_instruction(instruction)

    async def start_calibration(self, instruction):
        self._require_instruction(instruction)
        await super().start_calibration(instruction)

    async def _close_policy(self):
        module = _adapter_module(self.model)
        if module is not None and self.policy is not None:
            line = module.describe_failures(self.policy)
            if line is not None:
                self.print_fn(line)
        return await super()._close_policy()


def preflight_lines(config, roles) -> list[str]:
    cameras = ", ".join(
        f"{role}: {config.camera(role).backend} {config.camera(role).id}" for role in roles
    )
    arms = " · ".join(
        f"{name}: {config.arms[name].host}, {GRIPPER_LABELS[config.arms[name].gripper]}"
        for name in ARMS
    )
    return [
        f"Arms: {arms}",
        f"Cameras: {cameras}",
        "Both arms enable in trajectory mode at their current pose. Keep the E-stop in reach.",
    ]


def run_xarm7(
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
    max_joint_step=XARM7.max_joint_step,
    max_joint_velocity=XARM7.max_joint_velocity,
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
    rig_factory=XArm7Rig,
    hud_platform=None,
):
    print_fn = safe_printer(print_fn)
    instruction = task_instructions(instruction)
    if not _runs_on_xarm7(model, checkpoint):
        raise _refuse(model)
    contract, strategy = validate_run_options(
        model, label=XARM7.label, mode=mode, region=region, provider=provider, speed=speed,
        keep_warm=keep_warm, rtc=rtc, context=context, max_actions=max_actions,
        trace_dir=trace_dir, trace_images=trace_images, action_smoothing=action_smoothing,
        smoothing_new_weight=smoothing_new_weight,
        smoothing_correction_steps=smoothing_correction_steps,
        smoothing_reference_speed=smoothing_reference_speed,
    )
    resolve_action_smoothing(strategy, contract)
    config = load_config(config_path).validate(complete=True)
    roles = XARM7.roles_for(model, config.roles)
    hud_session = None
    if hud:
        from dreamscale.integrations.hud_recorder import HudJob

        hud_session = HudJob(
            model=model, robot=XARM7.label, name=hud_job, platform=hud_platform,
            print_fn=print_fn,
        )

    def preflight():
        for line in preflight_lines(config, roles):
            print_fn(line)

    def make_runner(rig, lifecycle):
        return XArm7TaskRunner(
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
            embodiment=XARM7,
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
