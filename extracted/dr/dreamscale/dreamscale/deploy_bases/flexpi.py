"""Flex-π deployments in the SDK: its base as the CLI and the policy runtime know it
(``dreamscale.deploy_bases`` loads it by the family manifest's id).

Scaffolded by scripts/new_model.py, unlisted (``listed_as=None``) until GA. Its deployments run
the one robot preset its transport module declares (dreamscale_transport.flexpi_deploy), so
`deployments create`, its robot line, Detect's lines and its RTC setting are the shared preset
base's (deploy_bases/_preset.py), and its sessions' contract is
dreamscale.policy.flexpi_deployment. `dreamscale run yam --deployment` drives it on the
Bimanual YAM rig (its one preset: the same cameras, joint radians and 0-1 grippers as π0.5's
and GR00T N1.7's YAM deployments; the run loop sends the last executed command as the
``action_history`` Flex-π anchors on); ``dreamscale.connect("flexpi", deployment=...)``
drives it from Python.
"""

from __future__ import annotations

from dreamscale_transport import flexpi_deploy as C

from dreamscale.deploy_bases import Base, DeployBase, ExportedBase, cmd
from dreamscale.deploy_bases._preset import PresetUnits

NAME = "flexpi"
# The rig `dreamscale run` drives its one preset on.
_YAM = "yam"
# Its preset and its build's steps, as `deployments create --wait` shows them.
CLI = Base({C.PRESET: C.PRESET_LABEL}, (
    ("Finding the export", ("building", "resolving", "checking")),
    ("Downloading", ("downloading",)),
    ("Saving", ("validating", "sealing", "built")),
    ("Testing on a server", ("qualifying", "ready", "failed")),
), None)
UNITS = PresetUnits(
    name=NAME, label=C.FLEXPI_PUBLIC_NAME,
    source_format=C.FLEXPI_SOURCE_FORMAT,
    preset=C.PRESET, preset_label=C.PRESET_LABEL, cameras=C.CAMERAS,
    state_dim=C.STATE_DIM, action_dim=C.ACTION_DIM, action_horizon=C.ACTION_HORIZON,
    action_hz=C.ACTION_HZ, action_space=C.ACTION_SPACE, joint_unit=C.JOINT_UNIT,
    gripper_unit=C.GRIPPER_UNIT, gripper_indices=C.GRIPPER_INDICES,
)
# `deployments create --base flexpi`, without the CLI.
run_add_flexpi = UNITS.run_add



def runner(embodiment, checkpoint_id, row, model):
    """The model `dreamscale run <robot> --deployment` runs: the base on `dreamscale run yam`;
    a clear error, naming how to run it, on any other robot."""
    if embodiment.name == _YAM:
        return NAME
    raise cmd._invalid(
        f"{checkpoint_id} is a Flex-π deployment for {C.PRESET_LABEL}, not {embodiment.label}",
        f"run it with `dreamscale run {_YAM} --deployment {checkpoint_id}`",
        cause=f"`dreamscale run {embodiment.name}` drives {embodiment.label} only",
    )


def run_command(deployment: dict) -> str:
    """How to run a deployment: `dreamscale run yam`."""
    return f"dreamscale run {_YAM} --deployment {deployment['id']}"


EXPORTED = ExportedBase(
    "Flex-π",
    "dreamscale.policy.flexpi_deployment:FlexpiSessionDeployment",
    "dreamscale.policy.flexpi_deployment:runtime_contract",
)
BASE = DeployBase(
    family="flexpi", name=NAME, label="Flex-π", cli=CLI,
    exported=EXPORTED, runner=runner, run_command=run_command, robots=(_YAM,),
    # Its runs' step_N.pt is a torch archive: Detect reads it from the listing's spans
    # (``archives``), and the upload sends only the members a build reads.
    local_archive=True,
    **UNITS.hooks(),
)
