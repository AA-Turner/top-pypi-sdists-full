"""Long-WAM deployments in the SDK: its base as the CLI and the policy runtime know it
(``dreamscale.deploy_bases`` loads it by the family manifest's id).

Scaffolded by scripts/new_model.py, unlisted (``listed_as=None``) until GA. Its deployments run
the robot preset its transport module declares (dreamscale_transport.long_wam_deploy), or a
custom robot a managed training run trained (its export names its cameras, widths and rate:
docs/plans/2026-11-14-long-wam-any-robot.md), so `deployments create`, its robot line, Detect's
lines and its RTC setting are the shared preset base's (deploy_bases/_preset.py), and its
sessions' contract is dreamscale.policy.long_wam_deployment. `dreamscale run yam --deployment`
drives the preset on the Bimanual YAM rig (the same cameras, joint radians and 0-1 grippers as
π0.5's and Flex-π's YAM deployments; the run loop keeps the tick history its window reads);
``dreamscale.connect("long-wam-yam", deployment=...)`` drives either from Python. A session paces
at its deployment's own rate (the export's); a create declares none (``declared_rates``).
"""

from __future__ import annotations

from dataclasses import dataclass

from dreamscale_transport import long_wam_deploy as C

from dreamscale.deploy_bases import Base, DeployBase, ExportedBase, cmd
from dreamscale.deploy_bases._preset import PresetUnits

NAME = "long-wam-yam"
# The rig `dreamscale run` drives its one preset on.
_YAM = "yam"
# Its preset and its build's steps, as `deployments create --wait` shows them.
CLI = Base({C.PRESET: C.PRESET_LABEL}, (
    ("Finding the export", ("building", "resolving", "checking")),
    ("Downloading", ("downloading",)),
    ("Saving", ("validating", "sealing", "built")),
    ("Testing on a server", ("qualifying", "ready", "failed")),
), None)


@dataclass(frozen=True)
class LongWamUnits(PresetUnits):
    """The preset base's hooks; a custom robot's rows name it by its cameras."""

    def robot_name(self, spec: dict) -> str:
        if spec.get("preset") == C.CUSTOM:
            keys = ", ".join(c.get("key", "?") for c in spec.get("cameras") or ())
            return f"custom robot ({keys})" if keys else "custom robot"
        return super().robot_name(spec)


UNITS = LongWamUnits(
    name=NAME, label=C.LONG_WAM_PUBLIC_NAME,
    source_format=C.LONG_WAM_SOURCE_FORMAT,
    preset=C.PRESET, preset_label=C.PRESET_LABEL, cameras=C.CAMERAS,
    state_dim=C.STATE_DIM, action_dim=C.ACTION_DIM, action_horizon=C.ACTION_HORIZON,
    action_hz=C.ACTION_HZ, action_space=C.ACTION_SPACE, joint_unit=C.JOINT_UNIT,
    gripper_unit=C.GRIPPER_UNIT, gripper_indices=C.GRIPPER_INDICES,
    default_executed=C.DEFAULT_EXECUTED,
    # `--hz`: its server refuses a declared rate (long_wam_deploy_base's embodiment fields), so
    # the SDK does too: a deployment's rate is its export's (a custom robot's run's), never a
    # create's. None once its server takes one, and the server's validation decides.
    declared_rates=(),
)
# `deployments create --base long-wam-yam`, without the CLI.
run_add_long_wam = UNITS.run_add


def _custom(row: dict) -> bool:
    return ((row or {}).get("embodiment") or {}).get("preset") == C.CUSTOM


def runner(embodiment, checkpoint_id, row, model):
    """The model `dreamscale run <robot> --deployment` runs: the base on `dreamscale run yam`;
    a clear error, naming how to run it, on any other robot (and for a custom robot, which no
    `dreamscale run` rig drives)."""
    if _custom(row):
        raise cmd._invalid(
            f"{checkpoint_id} is a Long-WAM deployment for a custom robot",
            f'drive it from Python: dreamscale.connect("{NAME}", deployment="{checkpoint_id}")',
            cause=f"`dreamscale run {embodiment.name}` drives {embodiment.label} only",
        )
    if embodiment.name == _YAM:
        return NAME
    raise cmd._invalid(
        f"{checkpoint_id} is a Long-WAM deployment for {C.PRESET_LABEL}, not {embodiment.label}",
        f"run it with `dreamscale run {_YAM} --deployment {checkpoint_id}`",
        cause=f"`dreamscale run {embodiment.name}` drives {embodiment.label} only",
    )


def run_command(deployment: dict) -> str:
    """How to run a deployment: `dreamscale run yam`; a custom robot's from Python."""
    if _custom(deployment):
        return f'dreamscale.connect("{NAME}", deployment="{deployment["id"]}")'
    return f"dreamscale run {_YAM} --deployment {deployment['id']}"

EXPORTED = ExportedBase(
    "Long-WAM",
    "dreamscale.policy.long_wam_deployment:LongWamSessionDeployment",
    "dreamscale.policy.long_wam_deployment:runtime_contract",
)
BASE = DeployBase(
    family="long_wam", name=NAME, label="Long-WAM", cli=CLI,
    exported=EXPORTED, runner=runner, run_command=run_command, robots=(_YAM,),
    # Its exports' model.pt is a torch archive: Detect reads it from the listing's spans
    # (``archives``), and the upload sends only the members a build reads.
    local_archive=True,
    **UNITS.hooks(),
)
