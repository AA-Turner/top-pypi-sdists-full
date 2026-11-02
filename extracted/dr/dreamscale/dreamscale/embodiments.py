"""What differs between the robots `dreamscale run` drives, as data.

The attended runner, the policy client and the motion limiter are shared; an
embodiment contributes this descriptor and a rig (dreamscale.hardware.rig.Rig).
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module

from dreamscale_transport import catalog

from dreamscale.constants import JOINT_NAMES, MODEL_DROID, MODEL_PI05_DROID


@dataclass(frozen=True)
class ModelCameras:
    """The camera roles one model reads: every required one, and optional ones if mapped."""

    required: tuple[str, ...]
    optional: tuple[str, ...] = ()


class RoleMismatch(ValueError):
    """The rig has no camera for a role the model can't run without."""


@dataclass(frozen=True)
class Embodiment:
    name: str                       # the CLI word: `dreamscale run <name>`
    label: str                      # how the operator reads it: "SO-101"
    joints: tuple[str, ...]         # action order labels, for recorders
    arms: tuple[str, ...]           # arm names, in action order
    arm_size: int                   # values per arm, gripper last
    unit: str                       # joint unit word: "degrees" or "radians"
    precision: int                  # decimals when printing joint values
    camera_roles: tuple[str, ...]   # observation frames, by role
    # cloud policies `dreamscale run <name>` supports: the catalog's (Client.robot), in order
    policy_models: tuple[str, ...]
    run_policy: str                 # "module:function" running attended policy tasks
    doctor: str                     # "module:function" checking its setup
    extras: str                     # "module:function" listing the extras it installs
    setup_command: str              # how to set the robot up
    max_joint_step: float | None    # default tracking envelope, joint units; None: none
    max_joint_velocity: float | None  # default speed cap, joint units/s; None: none
    run_llm: str | None = None      # "module:function" running a managed LLM task
    llm_profile: str | None = None  # "module:function" returning its LLM tool profile
    rig_config: bool = False        # takes --config (a rig file beside config.toml)
    gripper_precision: int = 4
    # Works, but stays out of `-h` until launch.
    hidden: bool = False
    # Listed, but labeled experimental everywhere it is offered; docs is its page.
    experimental: bool = False
    docs: str | None = None
    # What to do after a run leaves the arms holding; None: support them and release.
    held_hint: str | None = None
    # Models that read fewer than all camera_roles, as (model, ModelCameras) pairs.
    # Any other model needs every role.
    model_cameras: tuple[tuple[str, ModelCameras], ...] = ()

    def trace_layout(self, contract):
        """A contract describing this robot's joint layout, for recorder views, when the
        model's own rows declare none (velocity rows); None when they do. Execution and
        the recording's metadata keep the model's contract."""
        if contract.joint_groups:
            return None
        from dataclasses import replace

        size = self.arm_size
        groups = tuple(tuple(range(a * size, a * size + size - 1)) for a in range(len(self.arms)))
        return replace(
            contract,
            # A deployment base declares no width before its session: the robot's.
            action_dim=contract.action_dim or size * len(self.arms),
            action_space="absolute_joint_position",
            hold_behavior="current_position",
            joint_groups=groups,
            gripper_indices=tuple(a * size + size - 1 for a in range(len(self.arms))),
            joint_unit={"radians": "rad", "degrees": "deg"}[self.unit],
        )

    @property
    def deployment_models(self) -> tuple[str, ...]:
        """The models (deployment bases' ids) whose own deployments `dreamscale run <name>`
        runs on this rig (DeployBase.robots), in the family manifest's order."""
        from dreamscale_transport import families

        from dreamscale import deploy_bases

        return tuple(families.family(base.family).deploy.base
                     for base in deploy_bases.running_on(self.name))

    @property
    def recording_keys(self) -> tuple[str, ...]:
        """Its cameras as a LeRobot recording names them, in role order: the camera keys
        of a π0.5 deployment fine-tuned on that recording."""
        return tuple(f"observation.images.{role}" for role in self.camera_roles)

    def cameras_for(self, model: str) -> ModelCameras:
        return dict(self.model_cameras).get(model, ModelCameras(self.camera_roles))

    def roles_for(self, model: str, mapped) -> tuple[str, ...]:
        """The roles a run of model uses on a rig whose mapped roles are given, in
        camera_roles order. Raises RoleMismatch naming each missing required role."""
        from dreamscale.model_names import public_model

        spec, mapped = self.cameras_for(model), set(mapped)
        missing = [role for role in spec.required if role not in mapped]
        if missing:
            raise RoleMismatch(
                f"{public_model(model)} needs {_role_words(spec.required)} cameras; this rig "
                f"has no {_role_words(missing)} camera. Run {self.setup_command}."
            )
        wanted = {*spec.required, *(role for role in spec.optional if role in mapped)}
        return tuple(role for role in self.camera_roles if role in wanted)

    @property
    def display_label(self) -> str:
        """The label as menus and help show it: experimental robots say so."""
        return f"{self.label} (experimental)" if self.experimental else self.label

    def experimental_notice(self) -> str | None:
        """What a run or setup prints first on an experimental robot; None otherwise."""
        if not self.experimental:
            return None
        notice = (
            f"{self.label} support is experimental: expect rough edges, and keep the "
            "E-stop in reach."
        )
        return f"{notice} See {self.docs}" if self.docs else notice

    @property
    def release_command(self) -> str:
        return f"dreamscale robots {self.name} release"

    def held_message(self) -> str:
        """What the operator reads when a run disconnects with every arm holding."""
        arms = "arms" if len(self.arms) > 1 else "arm"
        hint = self.held_hint or (
            f"Keep robot power on; to release, support the {arms}, then run: "
            f"{self.release_command}"
        )
        return f"{arms.title()} holding position. {hint}"

    @staticmethod
    def load(path: str):
        """The object a "module:function" field names, imported on first use."""
        module, _, name = path.partition(":")
        return getattr(import_module(module), name)

    @property
    def joint_indices(self) -> tuple[int, ...]:
        """Action indices of arm joints, grippers excluded."""
        return tuple(
            arm * self.arm_size + i
            for arm in range(len(self.arms)) for i in range(self.arm_size - 1)
        )

    def preview_lines(self, actions, current) -> list[str]:
        """What one non-dispatched prediction asks of the arms."""
        largest = max(
            abs(float(action[index]) - float(current[index]))
            for action in actions for index in self.joint_indices
        )
        lines = [f"Prediction only: {len(actions)} actions; none dispatched."]
        first = actions[0]
        for arm, name in enumerate(self.arms):
            offset = arm * self.arm_size
            joints = tuple(
                round(float(v), self.precision)
                for v in first[offset : offset + self.arm_size - 1]
            )
            gripper = float(first[offset + self.arm_size - 1])
            lines.append(
                f"{name}: joints {joints} {self.unit}; gripper {gripper:.{self.gripper_precision}f}"
            )
        lines.append(
            "Largest requested joint change from current pose: "
            f"{largest:.{self.precision}f} {self.unit}."
        )
        return lines


SO101 = Embodiment(
    name="so101",
    label="SO-101",
    joints=JOINT_NAMES,
    arms=("Arm",),
    arm_size=6,
    unit="degrees",
    precision=1,
    camera_roles=("side", "wrist"),
    policy_models=catalog.robot_models("so101"),
    run_policy="dreamscale.so101_runner:run_so101",
    run_llm="dreamscale.agents.so101_cli:run_so101_llm",
    llm_profile="dreamscale.agents.so101:profile",
    doctor="dreamscale.doctor:run_so101_doctor",
    extras="dreamscale.extras:so101_extras",
    setup_command="dreamscale robots so101 setup",
    max_joint_step=45.0,
    max_joint_velocity=150.0,
    gripper_precision=1,
)

YAM = Embodiment(
    name="yam",
    label="YAM",
    joints=tuple(
        f"{side}_{name}"
        for side in ("left", "right")
        for name in (*(f"joint_{i}" for i in range(1, 7)), "gripper")
    ),
    arms=("Left", "Right"),
    arm_size=7,
    unit="radians",
    precision=4,
    camera_roles=("top", "left", "right"),
    # Joint-wire models plus calibrated end-effector models using the same physical rig.
    policy_models=catalog.robot_models("yam"),
    run_policy="dreamscale.hardware.yam_runner:run_yam",
    run_llm="dreamscale.agents.yam_cli:run_yam_llm",
    llm_profile="dreamscale.agents.yam:profile",
    doctor="dreamscale.hardware.yam_doctor:run_yam_doctor",
    extras="dreamscale.extras:yam_extras",
    setup_command="dreamscale robots yam setup",
    max_joint_step=0.15,
    max_joint_velocity=1.0,
    # The resident controller holds them until released, whatever runs next (Gabriel's arms
    # overheated holding a wire through a 25-minute cold start).
    held_hint="Keep robot power on; they hold until released, and a long hold under load heats "
    "the motors. To release, support the arms, then run: dreamscale robots yam release",
    rig_config=True,
)

FRANKA = Embodiment(
    name="franka",
    label="Franka",
    joints=(*(f"joint_{i}" for i in range(1, 8)), "gripper"),
    arms=("Arm",),
    arm_size=8,
    unit="radians",
    precision=4,
    camera_roles=("exterior_1", "exterior_2", "wrist"),
    # DROID-trained models; model_cameras names those that read fewer than three views.
    policy_models=catalog.robot_models("franka"),
    run_policy="dreamscale.hardware.franka_runner:run_franka",
    doctor="dreamscale.hardware.franka_doctor:run_franka_doctor",
    extras="dreamscale.extras:franka_extras",
    setup_command="dreamscale robots franka setup",
    # No caps of our own: DROID's impedance controller tracks the policy, inside the
    # arm's own joint limits.
    max_joint_step=None,
    max_joint_velocity=None,
    rig_config=True,
    gripper_precision=2,
    # Listed for DROID setups, but its supervised motion is still being validated on
    # hardware: every surface says experimental.
    experimental=True,
    docs="https://docs.dreamscalelabs.com/robots/franka",
    # The FR3 holds its pose on its own controller once FCI disconnects (verified).
    held_hint="It holds itself while the robot stays on; lock its joints in Desk when "
    "you're done.",
    model_cameras=(
        # openpi's DroidInputs read the first exterior view and the wrist only.
        (MODEL_PI05_DROID, ModelCameras(("exterior_1", "wrist"))),
        (MODEL_DROID, ModelCameras(("exterior_1", "wrist"), ("exterior_2",))),
    ),
)

UR = Embodiment(
    name="ur",
    label="Universal Robots",
    joints=(*(f"joint_{i}" for i in range(1, 7)), "gripper"),
    arms=("Arm",),
    arm_size=7,
    unit="radians",
    precision=4,
    # π0.5's UR5e layout: an over-the-shoulder scene camera and a wrist camera.
    camera_roles=("scene", "wrist"),
    # No shared models: it runs an organization's own π0.5 deployments (--deployment).
    policy_models=(),
    run_policy="dreamscale.hardware.ur_runner:run_ur",
    doctor="dreamscale.hardware.ur_doctor:run_ur_doctor",
    extras="dreamscale.extras:ur_extras",
    setup_command="dreamscale robots ur setup",
    max_joint_step=0.3,
    max_joint_velocity=1.0,
    rig_config=True,
    gripper_precision=2,
    # Any e-Series or UR Series arm (dreamscale.hardware.ur_arm.ARM_SPECS), validated on one
    # UR7e on PolyScope X only.
    experimental=True,
    docs="https://docs.dreamscalelabs.com/robots/ur",
    held_hint="It holds itself while powered; stop the pendant program when you're done.",
)

XARM7 = Embodiment(
    name="xarm7",
    label="xArm 7",
    joints=tuple(
        f"{arm}_{joint}" for arm in ("aft", "fore")
        for joint in (*(f"joint_{i}" for i in range(1, 8)), "gripper")
    ),
    # Two UFACTORY xArm 7s named for where they sit on the bench, aft first.
    arms=("Aft", "Fore"),
    arm_size=8,
    unit="radians",
    precision=4,
    # A scene camera above the bench, then the fore (left) and aft (right) wrists.
    camera_roles=("top", "left", "right"),
    # No shared models: it runs an organization's own deployments (--deployment).
    policy_models=(),
    run_policy="dreamscale.hardware.xarm7_runner:run_xarm7",
    doctor="dreamscale.hardware.xarm7_doctor:run_xarm7_doctor",
    extras="dreamscale.extras:xarm7_extras",
    setup_command="dreamscale robots xarm7 setup",
    # The controller plans at 0.5 rad/s; the same cap and a 0.2 rad lunge guard client-side.
    max_joint_step=0.2,
    max_joint_velocity=0.5,
    rig_config=True,
    gripper_precision=2,
    # Validated against xarm-python-sdk and a bench's settings; first hardware run pending.
    experimental=True,
    docs="https://docs.dreamscalelabs.com/robots/xarm7",
    held_hint="They hold their last target while enabled; disable them in UFACTORY Studio "
    "when you're done.",
)

EMBODIMENTS = {e.name: e for e in (SO101, YAM, FRANKA, UR, XARM7)}


def _role_words(roles) -> str:
    names = [role.replace("_", " ") for role in roles]
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]
