"""Verne V0.5 deployments in the SDK: its base as the CLI and the policy runtime know it
(``dreamscale.deploy_bases`` loads it by the family manifest's id), unlisted (``listed_as=None``)
until GA. `deployments create`, its robot line, Detect's lines and its RTC setting are the
shared preset base's (deploy_bases/_preset.py); its sessions' contract is
dreamscale.policy.verne_v05_deployment. `dreamscale run yam` drives the bimanual YAM preset
(dreamscale.hardware.verne_v05_yam turns the rig's joints into poses and back); a custom robot
runs from Python (``dreamscale.connect("verne-v05-base", deployment=...)``).
"""

from __future__ import annotations

from dreamscale_transport import verne_v05_deploy as C

from dreamscale.deploy_bases import Base, DeployBase, ExportedBase, cmd
from dreamscale.deploy_bases._preset import PresetUnits

NAME = "verne-v05-base"
# Its preset and its build's steps, as `deployments create --wait` shows them.
CLI = Base({C.PRESET: C.PRESET_LABEL}, (
    ("Finding the export", ("building", "resolving", "checking")),
    ("Downloading", ("downloading",)),
    ("Saving", ("validating", "sealing", "built")),
    ("Testing on a server", ("qualifying", "ready", "failed")),
), None)
UNITS = PresetUnits(
    name=NAME, label=C.VERNE_V05_PUBLIC_NAME,
    source_format=C.VERNE_V05_SOURCE_FORMAT,
    preset=C.PRESET, preset_label=C.PRESET_LABEL, cameras=C.CAMERAS,
    state_dim=C.STATE_DIM, action_dim=C.ACTION_DIM, action_horizon=C.ACTION_HORIZON,
    action_hz=C.ACTION_HZ, action_space=C.ACTION_SPACE, joint_unit=C.JOINT_UNIT,
    gripper_unit=C.GRIPPER_UNIT, gripper_indices=C.GRIPPER_INDICES,
    rtc_contract=C.TRAINED_RTC_CONTRACT,
    max_trained_rtc_delay=C.MAX_TRAINED_RTC_DELAY,
    default_executed=C.DEFAULT_EXECUTED_ACTIONS,
    # A robot with Verne's cameras by role (camera_0 left wrist, camera_1 right wrist,
    # camera_2 head) under its own keys: `--preset custom --camera <key>=camera_N`.
    custom_cameras=tuple(feature for _, feature in C.CAMERAS),
    # `--hz`: its server refuses a declared rate (verne_v05_deploy_base's embodiment fields), so
    # the SDK does too; None once its server takes one, and the server's validation decides.
    declared_rates=(),
)
# `deployments create --base verne-v05-base`, without the CLI.
run_add_verne_v05 = UNITS.run_add

EXPORTED = ExportedBase(
    "Verne V0.5",
    "dreamscale.policy.verne_v05_deployment:VerneV05SessionDeployment",
    "dreamscale.policy.verne_v05_deployment:runtime_contract",
    # One vector of tool poses: a helper's joint-only state isn't it.
    state="refuse",
)
# The rig `dreamscale run` drives the YAM preset on (dreamscale.embodiments.YAM).
_YAM = "yam"


def runner(embodiment, checkpoint_id, row, model):
    """The model `dreamscale run <robot> --deployment` runs: the base on `dreamscale run yam`
    for the YAM preset; a clear error, naming how to run it, otherwise."""
    spec = row.get("embodiment") or {}
    if spec.get("preset") == C.PRESET and embodiment.name == _YAM:
        return NAME
    if spec.get("preset") == C.PRESET:
        raise cmd._invalid(
            f"{checkpoint_id} is a {C.VERNE_V05_PUBLIC_NAME} deployment for "
            f"{C.PRESET_LABEL}, which `dreamscale run {embodiment.name}` doesn't drive",
            f"run it with `dreamscale run {_YAM} --deployment {checkpoint_id}`",
            cause=f"`dreamscale run {embodiment.name}` drives {embodiment.label} only",
        )
    raise cmd._invalid(
        f"{checkpoint_id} is a {C.VERNE_V05_PUBLIC_NAME} deployment for a custom robot, which "
        "`dreamscale run` doesn't drive",
        f'drive it from Python: dreamscale.connect("{NAME}", deployment="{checkpoint_id}"), '
        "then policy.next_action(...) with your robot's tool poses",
        cause=f"`dreamscale run` drives {C.VERNE_V05_PUBLIC_NAME} deployments of the "
              f"{C.PRESET} preset only",
    )


def run_command(deployment: dict) -> str:
    """How to run a deployment: `dreamscale run yam` for the YAM preset, else Python."""
    if (deployment.get("embodiment") or {}).get("preset") == C.PRESET:
        return f"dreamscale run {_YAM} --deployment {deployment['id']}"
    return f'dreamscale.connect("{NAME}", deployment="{deployment["id"]}")'


BASE = DeployBase(
    family="verne_v05", name=NAME, label="Verne V0.5", cli=CLI,
    exported=EXPORTED, runner=runner, run_command=run_command,
    # The bimanual YAM preset's absolute tool poses, turned into joint targets.
    robots=(_YAM,), robot_adapters={_YAM: "dreamscale.hardware.verne_v05_yam"},
    # Verne's own RoboTwin and LIBERO checkpoints as catalog models on Dreamscale Labs'
    # deployments: a session carries its deployment's block (its robot's cameras and arms).
    catalog_exports={C.VERNE_V05_ROBOTWIN_MODEL: EXPORTED, C.VERNE_V05_LIBERO_MODEL: EXPORTED},
    **UNITS.hooks(),
)
