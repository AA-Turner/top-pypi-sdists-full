"""`dreamscale run so101`: the attended runner over one SO-101 arm.

Connect the arm, then for each instruction: home (when a home pose is saved),
preview one plan (nothing moves), run until Ctrl+C, hold, and return home. The arm
holds its pose when the command exits; `dreamscale robots so101 release` ends that.
SO-101 contributes its models, its rig and its setup check; everything else is
dreamscale.attended.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import partial
from typing import Any

from dreamscale import errors
from dreamscale.attended.lifecycle import safe_printer
from dreamscale.attended.runner import (
    AttendedTaskRunner,
    run_attended,
    task_instructions,
    validate_run_options,
)
from dreamscale.config import load_config
from dreamscale.embodiments import SO101
from dreamscale.hardware.so101_rig import (
    DEFAULT_MAX_JOINT_STEP,
    DEFAULT_MAX_JOINT_VELOCITY,
    So101Rig,
)
from dreamscale.model_names import public_model
from dreamscale.policy.deployment import runs_robot_deployments
from dreamscale.policy.exported_deployments import exported_base
from dreamscale.policy.remote import aconnect
from dreamscale.policy.runtime.action_smoothing import resolve_action_smoothing

SO101_RUN_MODELS = SO101.policy_models
COMMAND = "dreamscale run so101"


class DeploymentObservation:
    """An SO-101 observation for a deployment that names its own cameras (FLUX 3 Action): the
    side and wrist frames under the deployment's keys, the six joints as its state. Anything
    else reads the SO-101 observation it wraps."""

    def __init__(self, observation: Any, keys: tuple[str, str]) -> None:
        self.observation, self.keys = observation, keys

    def __getattr__(self, name: str) -> Any:
        return getattr(self.observation, name)

    @property
    def state(self) -> tuple[float, ...]:
        """Its state vector (the history window's measured ticks read it)."""
        return self.observation.joint_positions

    def to_wire(self, *, session_id: str, observation_id: int, instruction: str):
        from dreamscale import robot

        side, wrist = self.keys
        return robot.observation(
            cameras={side: self.observation.side_frame, wrist: self.observation.wrist_frame},
            state=self.observation.joint_positions,
            actions_remaining=self.observation.actions_remaining,
        ).to_wire(session_id=session_id, observation_id=observation_id, instruction=instruction)


def deployment_observe(rig: Any, runner: Callable[[], Any]) -> Callable[..., Any]:
    """The rig's observations for the connected deployment's cameras (so101_camera_keys)."""
    from dreamscale.policy.flux3_deployment import so101_camera_keys

    def observe(ctx=None):
        deployment = getattr(runner().policy, "deployment", None)
        # A deployment that names its SO-101 cameras itself (GR00T N1.7's preset), else FLUX's
        # BFL layout.
        keys = (deployment.so101_cameras if hasattr(deployment, "so101_cameras")
                else so101_camera_keys(deployment))
        if keys is None:
            raise errors.DreamscaleError(errors.ErrorInfo(
                code="invalid_deployment",
                problem="this deployment isn't SO-101 joint targets from scene and wrist cameras",
                cause=f"`{COMMAND}` drives SO-101 deployments in degrees only",
                fix="drive it from Python: dreamscale.connect(...), then policy.next_action(...)",
            ))
        return DeploymentObservation(rig.observe(ctx), keys)

    return observe


def _default_robot_factory() -> Any:
    """The SO-101 arm alone: its cameras come from the rig file (rig_cameras)."""
    from dreamscale.hardware.lerobot_so101 import create_so101
    from dreamscale.optional import require_so101_extra

    require_so101_extra()
    config = load_config()
    if config.robot_port is None:
        raise errors.catalog("so101_not_set_up")
    return create_so101(
        port=config.robot_port, calibration_path=config.calibration_path, include_camera=False,
    )


def rig_cameras(robot_factory):
    """The rig file's cameras for the stock robot; a custom robot_factory brings its own
    (capture_frames). Raises so101_not_set_up when side or wrist is unmapped."""
    if robot_factory is not _default_robot_factory:
        return None
    from dreamscale.hardware.so101_config import load_config as load_rig

    rig = load_rig()
    try:
        SO101.roles_for(SO101_RUN_MODELS[0], rig.roles)
    except ValueError as exc:
        raise errors.catalog("so101_not_set_up") from exc
    return rig


def so101_preflight(config, home, *, cameras=None, print_fn=print) -> None:
    """What every SO-101 run (policy or LLM) shows before the arm is armed."""
    if cameras is not None:
        views = ", ".join(f"{role} {cameras.camera(role).id}" for role in ("side", "wrist"))
    else:
        views = f"side {config.camera_index}, wrist {config.wrist_camera_index}"
    print_fn(
        f"Confirm the side and wrist camera views before connecting. Arm: SO-101 on "
        f"{config.robot_port or 'no configured port'}; cameras {views}."
    )
    if home is None:
        print_fn(
            "No home pose saved: the arm starts and ends each task where it is. "
            f"Save one with `{errors.COMMAND_HOME} --set`."
        )


def run_so101(
    *,
    model: str,
    instruction: str | list[str] | None = None,
    mode: str = "async",
    max_actions: int | None = None,
    keep_warm: int = 300,
    region: str = "available",
    provider: str | None = None,
    speed: str | None = None,
    rtc: str = "auto",
    checkpoint: str | None = None,
    context: str = "auto",
    max_joint_step: float = DEFAULT_MAX_JOINT_STEP,
    max_joint_velocity: float = DEFAULT_MAX_JOINT_VELOCITY,
    action_smoothing: str = "auto",
    smoothing_new_weight: float | None = None,
    smoothing_correction_steps: int | None = None,
    smoothing_reference_speed: float | None = None,
    trace_dir=None,
    trace_images: bool = False,
    hud: bool = False,
    hud_job: str | None = None,
    recorder: Any = None,
    connect: Callable[..., Any] = aconnect,
    steady_send: int | None = None,
    robot_factory: Callable[[], Any] = _default_robot_factory,
    input_fn: Callable[[str], str] = input,
    print_fn: Callable[[str], None] = print,
    hud_platform: Any = None,
    read_line: Callable[[str], Any] | None = None,
    rig_options: dict[str, Any] | None = None,
) -> None:
    print_fn = safe_printer(print_fn)
    instruction = task_instructions(instruction)
    if steady_send is not None:  # the preview and the task loop share this connection
        connect = partial(connect, steady_send=steady_send)
    # A π0.5 or FLUX 3 Action deployment built for SO-101 runs here too (the CLI checks its
    # robot; one whose actions aren't joint targets is refused: the CLI first, else once
    # connected).
    if model not in SO101_RUN_MODELS and not (runs_robot_deployments(model) and checkpoint):
        raise ValueError(f"{public_model(model)} doesn't run on SO-101. {errors.SEE_MODELS}")
    contract, strategy = validate_run_options(
        model, label=SO101.label, mode=mode, region=region, provider=provider, speed=speed,
        keep_warm=keep_warm, rtc=rtc, context=context, max_actions=max_actions,
        trace_dir=trace_dir, trace_images=trace_images, action_smoothing=action_smoothing,
        smoothing_new_weight=smoothing_new_weight,
        smoothing_correction_steps=smoothing_correction_steps,
        smoothing_reference_speed=smoothing_reference_speed,
    )
    resolve_action_smoothing(strategy, contract)
    from dreamscale.homing import _valid_pose

    config = load_config()
    home = [float(v) for v in config.home_position] if _valid_pose(
        config.home_position
    ) else None
    resolved = {}

    def cameras():
        # Read when the arm is about to be used, as the robot itself is.
        if "rig" not in resolved:
            resolved["rig"] = rig_cameras(robot_factory)
        return resolved["rig"]

    hud_session = None
    if hud:
        from dreamscale.integrations.hud_recorder import HudJob

        hud_session = HudJob(
            model=model, robot=SO101.label, name=hud_job, platform=hud_platform,
            print_fn=print_fn,
        )

    def preflight():
        so101_preflight(config, home, cameras=cameras(), print_fn=print_fn)

    def make_rig():
        return So101Rig(
            robot_factory,
            calibration_path=config.calibration_path,
            home=home,
            max_joint_step=max_joint_step,
            max_joint_velocity=max_joint_velocity,
            cameras={"side": config.camera_index, "wrist": config.wrist_camera_index},
            camera_config=cameras(),
            retry_command=COMMAND,
            print_fn=print_fn,
            **(rig_options or {}),
        )

    def make_runner(rig, lifecycle):
        # A deployment naming its own cameras (FLUX) takes the rig's frames under its keys.
        names_cameras = exported_base(model) is not None
        runner = AttendedTaskRunner(
            rig,
            embodiment=SO101,
            observe=deployment_observe(rig, lambda: runner) if names_cameras else None,
            lifecycle=lifecycle,
            model=model,
            connect=connect,
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
        return runner

    try:
        run_attended(
            embodiment=SO101,
            preflight=preflight,
            make_rig=make_rig,
            make_runner=make_runner,
            instruction=instruction,
            max_actions=max_actions,
            input_fn=input_fn,
            print_fn=print_fn,
            read_line=read_line,
        )
    finally:
        if hud_session is not None:
            hud_session.close()
        if recorder is not None:
            recorder.close()
