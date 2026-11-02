"""LingBot-VLA 2.0 deployments in the SDK: upstream's trainer export on the bimanual xArm 7
(its cameras, widths and rate are fixed), RTC off or trained; `dreamscale run xarm7` drives
it."""

from __future__ import annotations

from typing import Any

from dreamscale_transport import lingbot_vla_deploy as C

from dreamscale.deploy_bases import Base, DeployBase, ExportedBase, cmd
from dreamscale.deploy_bases._preset import PresetUnits

NAME = "lingbot-vla-deployments"
# Its intake: read the export's configs, download its weights, cast them to bf16, then run
# them against upstream's sampler on a server.
CLI = Base({"bimanual_xarm7": "Bimanual xArm 7"}, (
    ("Finding the export", ("building", "resolving", "checking")),
    ("Downloading", ("downloading", "converting")),
    ("Saving", ("sealing", "built")),
    ("Testing on a server", ("qualifying", "ready", "failed")),
), None)


def lingbot_vla_found_lines(found: dict) -> list[str]:
    """What Detect read from a LingBot-VLA export: which one, its robot and its RTC."""
    checkpoint = found.get("checkpoint") or {}
    rtc = found.get("rtc") or {}
    trained = rtc.get("trained_max_delay") or 0
    gigabytes = (checkpoint.get("bf16_bytes") or 0) / 1e9
    return [
        f"Export: {checkpoint.get('path')} (update {checkpoint.get('step')}, "
        f"{gigabytes:.1f} GB in bf16)",
        "Robot: Bimanual xArm 7 (16 joint targets, aft first; cameras top, left, right; 20 Hz)",
        f"RTC: trained (prefix up to {trained})" if trained else "RTC: off (not trained)",
        *([f"Trained instructions: {len(found.get('prompts') or [])}"]
          if found.get("prompts") else []),
    ]


def _lingbot_vla_runner_model(embodiment: Any, checkpoint_id: str, row: dict) -> str:
    """A LingBot-VLA deployment `dreamscale run xarm7` drives: its bimanual xArm 7 preset
    (joint targets, 16 values aft first, cameras top/left/right by role)."""
    spec = row.get("embodiment") or {}
    if spec.get("preset") == "bimanual_xarm7" and embodiment.name == "xarm7":
        return NAME
    raise cmd._invalid(
        f"{checkpoint_id} is a LingBot-VLA deployment for the bimanual xArm 7, not "
        f"{embodiment.label}",
        f"run it with `dreamscale run xarm7 --deployment {checkpoint_id}`",
        cause=f"`dreamscale run {embodiment.name}` drives {embodiment.label} only",
    )


def runner(embodiment, checkpoint_id, row, model):
    return _lingbot_vla_runner_model(embodiment, checkpoint_id, row)


# Its deployments run the bimanual xArm 7 preset: create, the robot line and RTC are the shared
# preset base's, from its transport module's facts; Detect's lines are its own.
UNITS = PresetUnits(
    name=NAME, label="LingBot-VLA", source_format=C.LINGBOT_VLA_SOURCE_FORMAT,
    preset=C.XARM7_PRESET, preset_label=CLI.presets[C.XARM7_PRESET], cameras=C.XARM7_CAMERAS,
    state_dim=C.WIDTH, action_dim=C.WIDTH, action_horizon=C.HORIZON, action_hz=C.ACTION_HZ,
    action_space="absolute_joint_position", joint_unit="rad", gripper_unit="normalized_0_1",
    gripper_indices=C.GRIPPER_INDICES, rtc_contract=C.TRAINED_RTC_CONTRACT,
    max_trained_rtc_delay=C.MAX_TRAINED_RTC_DELAY, title="LingBot-VLA 2.0",
    robot="bimanual xArm 7", describe_found=lingbot_vla_found_lines,
)
run_add_lingbot_vla = UNITS.run_add
lingbot_vla_robot_line = UNITS.robot_line


EXPORTED = ExportedBase(
    "LingBot-VLA",
    "dreamscale.policy.lingbot_vla_deployment:LingbotVlaSessionDeployment",
    "dreamscale.policy.lingbot_vla_deployment:runtime_contract",
)
BASE = DeployBase(
    family="lingbot_vla", name=NAME, label="LingBot-VLA 2.0", cli=CLI,
    aliases=("lingbot-vla",), listed_as="lingbot-vla", runner=runner, exported=EXPORTED,
    robots=("xarm7",), **UNITS.hooks(),
)
