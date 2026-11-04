"""Flex-π deployments in the SDK: its base as the CLI and the policy runtime know it
(``dreamscale.deploy_bases`` loads it by the family manifest's id).

Scaffolded by scripts/new_model.py, unlisted (``listed_as=None``) until GA. Its deployments run
the one robot preset its transport module declares (dreamscale_transport.flexpi_deploy), so
`deployments create`, its robot line, Detect's lines and its RTC setting are the shared preset
base's (deploy_bases/_preset.py), and its sessions' contract is
dreamscale.policy.flexpi_deployment. It is driven from Python
(``dreamscale.connect("flexpi", deployment=...)``) until a `dreamscale run` robot is decided
for it (a ``runner`` and ``robots``, as deploy_bases/lingbot_vla.py's).
"""

from __future__ import annotations

from dreamscale_transport import flexpi_deploy as C

from dreamscale.deploy_bases import Base, DeployBase, ExportedBase
from dreamscale.deploy_bases._preset import PresetUnits

NAME = "flexpi"
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

EXPORTED = ExportedBase(
    "Flex-π",
    "dreamscale.policy.flexpi_deployment:FlexpiSessionDeployment",
    "dreamscale.policy.flexpi_deployment:runtime_contract",
)
BASE = DeployBase(
    family="flexpi", name=NAME, label="Flex-π", cli=CLI,
    exported=EXPORTED, **UNITS.hooks(),
)
