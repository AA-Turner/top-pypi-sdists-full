"""`dreamscale run yam`: the attended runner over the bimanual YAM rig.

YAM contributes its models, its calibrated end-effector bindings (Rho), the end-effector
adapters deployment bases declare for it (DeployBase.robot_adapters) and its CAN preflight;
everything else is dreamscale.attended.
"""

from __future__ import annotations

import importlib
from functools import partial
from pathlib import Path

from dreamscale_transport.rho_checkpoints import RHO_YAM_BOX_MODEL_ID

from dreamscale import deploy_bases, errors
from dreamscale.attended.lifecycle import safe_printer
from dreamscale.attended.runner import (
    AttendedTaskRunner,
    _close_quietly,
    interactive_tasks,
    run_attended,
    task_instructions,
    validate_run_options,
)
from dreamscale.constants import MODEL_BIMANUAL_YAM
from dreamscale.embodiments import YAM
from dreamscale.model_names import public_model
from dreamscale.policy.cartesian import PoseApproximation
from dreamscale.policy.deployment import runs_robot_deployments
from dreamscale.policy.flux3_deployment import FLUX3_BASE_MODEL
from dreamscale.policy.remote import aconnect
from dreamscale.policy.runtime.action_smoothing import resolve_action_smoothing
from dreamscale.policy.runtime.contract import runtime_contract_for_model
from dreamscale.yam import YamEndEffectorObservation

from .yam_can import discover_can_interfaces, resolve_arms
from .yam_cli_setup import can_label
from .yam_config import DEFAULT_CONFIG_PATH, load_config
from .yam_hold import watch_resident_holds
from .yam_native import YamHardwareError
from .yam_rig import YamRig

__all__ = [
    "HUD_JOINTS", "YAM_RUNNER_MODELS", "YamTaskRunner", "check_can", "interactive_tasks",
    "load_end_effector_adapter", "run_yam",
]

YAM_RUNNER_MODELS = YAM.policy_models
_END_EFFECTOR_BINDINGS = {
    RHO_YAM_BOX_MODEL_ID: {
        "coordinate_frame": RHO_YAM_BOX_MODEL_ID,
        "gripper_unit": "checkpoint",
        "observation_factory": YamEndEffectorObservation,
    },
}
_MANAGED_POSE_APPROXIMATION = PoseApproximation(None, None)
# Measured and commanded joint labels on HUD, in the 14-value wire order.
HUD_JOINTS = list(YAM.joints)


def _end_effector_binding(model):
    try:
        return _END_EFFECTOR_BINDINGS[model]
    except KeyError as exc:
        raise YamHardwareError("No YAM end-effector binding for the selected model.") from exc


def load_end_effector_adapter(
    model, path, config, *, kinematics_factory=None,
    pose_approximation=_MANAGED_POSE_APPROXIMATION,
):
    """Bind selected model semantics before any optional solver or motor loading."""
    from .yam_end_effector import YamEndEffectorAdapter, builtin_end_effector_profile

    binding = _end_effector_binding(model)
    options = dict(
        expected_model_id=model,
        expected_coordinate_frame=binding["coordinate_frame"],
        expected_gripper_unit=binding["gripper_unit"],
        observation_factory=binding["observation_factory"],
        pose_approximation=pose_approximation,
        **({"kinematics_factory": kinematics_factory} if kinematics_factory is not None else {}),
    )
    path = Path(path)
    try:
        path.lstat()
    except FileNotFoundError:
        return YamEndEffectorAdapter.from_profile(
            builtin_end_effector_profile(model, config), config, **options,
        )
    except OSError as exc:
        raise YamHardwareError(f"Cannot inspect YAM end-effector calibration at {path}.") from exc
    # An explicit file, directory or dangling link must never silently fall back.
    return YamEndEffectorAdapter.from_file(path, config, **options)


def _adapter_module(model):
    """The module of the end-effector adapter a base's deployments run through on this rig
    (DeployBase.robot_adapters: pose rows turned into joint targets), else None."""
    base = deploy_bases.of_model(model)
    path = base.robot_adapters.get(YAM.name) if base is not None else None
    return importlib.import_module(path) if path is not None else None


def _end_effector_execution_contract(model, adapter):
    binding = _end_effector_binding(model)
    adapter.require_policy(
        model, coordinate_frame=binding["coordinate_frame"], gripper_unit=binding["gripper_unit"],
    )
    return adapter.execution_contract(runtime_contract_for_model(model))


_safe_printer = safe_printer


class YamDeploymentObservation:
    """A YAM observation for a deployment that names its own cameras (FLUX 3 Action trained on
    bimanual YAM): the top, left and right frames under the deployment's keys, the fourteen
    joint values (six radians and the 0–1 gripper per arm, left then right) as its state.
    Anything else reads the YAM observation it wraps."""

    def __init__(self, observation, keys):
        self.observation, self.keys = observation, keys

    def __getattr__(self, name):
        return getattr(self.observation, name)

    @property
    def state(self):
        """Its state vector (the history window's measured ticks read it)."""
        o = self.observation
        return (*o.left_joint_positions, o.left_gripper, *o.right_joint_positions, o.right_gripper)

    def to_wire(self, *, session_id, observation_id, instruction):
        from dreamscale import robot

        o = self.observation
        return robot.observation(
            cameras={self.keys[role]: getattr(o, f"{role}_frame") for role in self.keys},
            state=self.state,
            actions_remaining=o.actions_remaining,
        ).to_wire(session_id=session_id, observation_id=observation_id, instruction=instruction)


def deployment_observe(rig, runner):
    """The rig's observations for the connected deployment's cameras (yam_camera_keys)."""
    from dreamscale.policy.flux3_deployment import yam_camera_keys

    def observe(ctx=None):
        deployment = getattr(runner().policy, "deployment", None)
        keys = yam_camera_keys(deployment)
        if keys is None:
            raise errors.DreamscaleError(errors.ErrorInfo(
                code="invalid_deployment",
                problem="this deployment isn't bimanual YAM joint targets from top, left and "
                "right cameras",
                cause="`dreamscale run yam` drives FLUX deployments trained on bimanual YAM "
                "recordings only",
                fix="drive it from Python: dreamscale.connect(...), then policy.next_action(...)",
            ))
        return YamDeploymentObservation(rig.observe(ctx), keys)

    return observe


def _runs_on_yam(model, checkpoint):
    # A π0.5, ABC-VLA or InternW0-Δ deployment built for bimanual YAM runs here too (the CLI
    # checks its robot; one whose actions aren't joint targets is refused: the CLI first,
    # else once connected). InternW0-Δ runs in sync mode (attended.runner.task_mode).
    return model in YAM_RUNNER_MODELS or (runs_robot_deployments(model) and bool(checkpoint))


def check_can(config, *, print_fn=print, discover_can=discover_can_interfaces):
    """Show each arm's CAN bus; refuse unless every bus is up, ERROR-ACTIVE at 1 Mbit/s."""
    print_fn(
        "Confirm top/left/right camera views and left/right CAN labels/cabling "
        "before connecting."
    )
    inventory = discover_can()
    buses = {bus.name: bus for bus in inventory.interfaces}
    ready = True
    for side, arm in config.arms.items():
        bus = buses.get(arm.can_interface)
        print_fn(
            f"{side.title()}: {arm.arm_type} · {arm.gripper_type} · "
            + (can_label(bus) if bus else f"{arm.can_interface} unavailable")
        )
        ready = (
            ready
            and bus is not None
            and bus.up
            and bus.bitrate == 1000000
            and bus.state == "ERROR-ACTIVE"
        )
    if not ready:
        raise YamHardwareError(
            "Configured CAN must be up, ERROR-ACTIVE at 1000000 bit/s. "
            "Check adapters/driver and operator bus configuration; run dreamscale doctor yam."
        )


class YamTaskRunner(AttendedTaskRunner):
    """The attended runner for one YAM rig connection; see AttendedTaskRunner."""

    def __init__(
        self, rig, *, model=MODEL_BIMANUAL_YAM, connect=aconnect, observe=None,
        end_effector_adapter=None, **options,
    ):
        if not _runs_on_yam(model, options.get("checkpoint")):
            raise ValueError(f"{public_model(model)} doesn't run on YAM. {errors.SEE_MODELS}")
        if model in _END_EFFECTOR_BINDINGS and end_effector_adapter is None:
            raise YamHardwareError("Rho-YAM requires a calibrated end-effector adapter.")
        contract = None
        module = _adapter_module(model)
        # A deployment base's adapter: its session names the chunk once it connects.
        self._adapted = module is not None
        if module is not None:
            adapter = end_effector_adapter or module.ADAPTER(rig.config)
            end_effector_adapter = adapter
            observe = observe or (lambda ctx: adapter.observe(rig.observe(ctx)))
            contract = adapter.provisional_contract()
        elif end_effector_adapter is not None:
            observation_factory = _end_effector_binding(model)["observation_factory"]
            observe = observe or (lambda ctx: end_effector_adapter.observe(
                rig.observe(ctx), observation_factory=observation_factory,
            ))
            contract = _end_effector_execution_contract(model, end_effector_adapter)
        super().__init__(
            rig, embodiment=YAM, model=model, connect=connect, observe=observe,
            end_effector_adapter=end_effector_adapter, execution_contract=contract, **options,
        )

    @property
    def execution_contract(self):
        """An adapted deployment run's is its bound session's (the deployment's rate and
        chunk); otherwise the one this runner was made with."""
        bound = getattr(getattr(self, "policy", None), "execution_contract", None)
        if getattr(self, "_adapted", False) and bound is not None:
            return bound
        return self._execution_contract

    @execution_contract.setter
    def execution_contract(self, contract):
        self._execution_contract = contract

    async def _connect_policy(self, on_progress):
        policy = await super()._connect_policy(on_progress)
        # A deployment the adapter can't run (another robot's) is refused before anything
        # moves, and its session closed.
        check = getattr(self.end_effector_adapter, "require_session", None)
        if self._adapted and check is not None:
            try:
                check(policy)
            except BaseException:
                await _close_quietly(policy)
                raise
        return policy


def _note_codec_frame_sizes(config) -> None:
    """Tell an opted-in robot's camera codec the frame sizes this rig will capture."""
    from dreamscale.camera_codec import note_rig_frame_sizes

    sizes = {}
    for role in config.ROLES:
        camera = config.camera(role)
        turned = camera.rotate in (90, 270)
        sizes[role] = (camera.height, camera.width) if turned else (camera.width, camera.height)
    note_rig_frame_sizes(sizes)


def run_yam(
    *,
    instruction=None,
    config_path=DEFAULT_CONFIG_PATH,
    model=MODEL_BIMANUAL_YAM,
    mode="async",
    max_actions=None,
    keep_warm=300,
    region="available",
    provider=None,
    speed=None,
    rtc="auto",
    checkpoint=None,
    context="auto",
    max_joint_step=0.15,
    max_joint_velocity=1.0,
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
    rig_factory=YamRig,
    discover_can=discover_can_interfaces,
    end_effector_adapter=None,
    hud_platform=None,
):
    print_fn = safe_printer(print_fn)
    instruction = task_instructions(instruction)
    if not _runs_on_yam(model, checkpoint):
        raise ValueError(f"{public_model(model)} doesn't run on YAM. {errors.SEE_MODELS}")
    contract, strategy = validate_run_options(
        model, label=YAM.label, mode=mode, region=region, provider=provider, speed=speed,
        keep_warm=keep_warm, rtc=rtc, context=context, max_actions=max_actions,
        trace_dir=trace_dir, trace_images=trace_images, action_smoothing=action_smoothing,
        smoothing_new_weight=smoothing_new_weight,
        smoothing_correction_steps=smoothing_correction_steps,
        smoothing_reference_speed=smoothing_reference_speed,
    )
    if model not in _END_EFFECTOR_BINDINGS:
        resolve_action_smoothing(strategy, contract)
    config = load_config(config_path).validate(complete=True)
    _note_codec_frame_sizes(config)
    module = _adapter_module(model)
    if model in _END_EFFECTOR_BINDINGS and end_effector_adapter is None:
        end_effector_adapter = load_end_effector_adapter(
            model, Path(config_path).with_name("yam-ee.json"), config,
        )
    elif module is not None and end_effector_adapter is None:
        # Its kinematics load (and refuse a rig they don't describe) before anything opens.
        end_effector_adapter = module.ADAPTER(config)
    if module is not None:
        contract = end_effector_adapter.provisional_contract()
    elif end_effector_adapter is not None:
        contract = _end_effector_execution_contract(model, end_effector_adapter)
    resolve_action_smoothing(strategy, contract)
    # Calibration binds to the saved names above; the rig connects on today's.
    config = resolve_arms(config, discover_can=discover_can)
    hud_session = None
    if hud:
        from dreamscale.integrations.hud_recorder import HudJob

        hud_session = HudJob(
            model=model, robot=YAM.label, name=hud_job, platform=hud_platform, print_fn=print_fn,
        )

    def preflight():
        check_can(config, print_fn=print_fn, discover_can=discover_can)

    def make_runner(rig, lifecycle):
        # A FLUX deployment names its own cameras: it takes the rig's frames under its keys
        # (π0.5, ABC-VLA and InternW0-Δ deployments of YAM read the YAM observation itself).
        names_cameras = model == FLUX3_BASE_MODEL
        runner = YamTaskRunner(
            rig,
            lifecycle=lifecycle,
            # While compute starts, arms an earlier run left holding are named, with how long.
            while_compute_starts=partial(watch_resident_holds, config.arms),
            **({"observe": deployment_observe(rig, lambda: runner)} if names_cameras else {}),
            # The preview and the task loop share this connection.
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
            end_effector_adapter=end_effector_adapter,
            trace_dir=trace_dir,
            trace_images=trace_images,
            hud=hud_session,
            recorder=recorder,
        )
        return runner

    try:
        run_attended(
            embodiment=YAM,
            preflight=preflight,
            make_rig=lambda: rig_factory(
                config, max_joint_step=max_joint_step, max_joint_velocity=max_joint_velocity,
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
