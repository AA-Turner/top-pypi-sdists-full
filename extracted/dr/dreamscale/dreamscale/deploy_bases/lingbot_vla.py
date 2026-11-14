"""LingBot-VLA 2.0 deployments in the SDK: upstream's trainer export on the bimanual xArm 7
(Rodeo's export: its cameras and widths are fixed) or on a custom robot its export's record
declares (`--preset custom`: its widths, views and chunk are the record's; the create may name
its camera keys by role, its units and, where the record names none, its rate). RTC off or
trained; `dreamscale run xarm7` drives the preset."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from dreamscale_transport import lingbot_vla_deploy as C

from dreamscale.deploy_bases import Base, DeployBase, ExportedBase, cli, cmd
from dreamscale.deploy_bases._preset import PresetUnits

NAME = "lingbot-vla-deployments"
# Its intake: read the export's configs, download its weights, cast them to bf16, then run
# them against upstream's sampler on a server.
CLI = Base({"bimanual_xarm7": "Bimanual xArm 7", "custom": "Custom"}, (
    ("Finding the export", ("building", "resolving", "checking")),
    ("Downloading", ("downloading", "converting")),
    ("Saving", ("sealing", "built")),
    ("Testing on a server", ("qualifying", "ready", "failed")),
), None)


def _robot_line(detected: dict) -> str:
    """Detect's robot: Rodeo's xArm 7, or the custom robot the export's record declares."""
    if detected.get("preset") != C.CUSTOM_PRESET:
        return ("Robot: Bimanual xArm 7 (16 joint targets, aft first; cameras top, left, right; "
                "20 Hz)")
    values = (f"{detected.get('action_dim')} joint targets"
              if detected.get("action_space") == "absolute_joint_position"
              else f"{detected.get('action_dim')} values")
    cameras = ", ".join(c.get("role", "?") for c in detected.get("cameras") or ())
    hz = detected.get("action_hz")
    rate = f"{cmd._hz(hz)} Hz" if hz else "rate not recorded: pass --hz"
    return (f"Robot: custom, from its record ({values}; cameras {cameras}; "
            f"{detected.get('action_horizon')}-action chunks; {rate})")


def lingbot_vla_found_lines(found: dict) -> list[str]:
    """What Detect read from a LingBot-VLA export: which one, its robot and its RTC."""
    checkpoint = found.get("checkpoint") or {}
    rtc = found.get("rtc") or {}
    trained = rtc.get("trained_max_delay") or 0
    gigabytes = (checkpoint.get("bf16_bytes") or 0) / 1e9
    return [
        f"Export: {checkpoint.get('path')} (update {checkpoint.get('step')}, "
        f"{gigabytes:.1f} GB in bf16)",
        _robot_line(found.get("detected") or {}),
        f"RTC: trained (prefix up to {trained})" if trained else "RTC: off (not trained)",
        *([f"Trained instructions: {len(found.get('prompts') or [])}"]
          if found.get("prompts") else []),
    ]


def _robot_from_found(found: dict, robot: dict | None, hz: float | None) -> dict:
    """The robot a create runs: the one it named, else the one Detect read (a custom robot's
    export names it; Rodeo's is the xArm 7). A custom robot needs a rate: its record's or the
    create's (`--hz`), refused here when neither names one, never assumed."""
    detected = found.get("detected") or {}
    if robot is None:
        robot = {"preset": C.CUSTOM_PRESET if detected.get("preset") == C.CUSTOM_PRESET
                 else C.XARM7_PRESET}
    if robot.get("preset") == C.CUSTOM_PRESET and hz is None and (
            detected.get("preset") == C.CUSTOM_PRESET and detected.get("action_hz") is None):
        raise cmd._invalid("this export records no control rate, and none was declared",
                           "pass --hz <the rate its training data was recorded at>")
    return dict(robot)


def _lingbot_vla_runner_model(embodiment: Any, checkpoint_id: str, row: dict) -> str:
    """A LingBot-VLA deployment `dreamscale run xarm7` drives: its bimanual xArm 7 preset
    (joint targets, 16 values aft first, cameras top/left/right by role)."""
    spec = row.get("embodiment") or {}
    if spec.get("preset") == "bimanual_xarm7" and embodiment.name == "xarm7":
        return NAME
    if spec.get("preset") == "custom":
        raise cmd._invalid(
            f"{checkpoint_id} is a LingBot-VLA deployment for a custom robot; "
            "`dreamscale run` drives the robots it knows",
            f'drive it from Python: dreamscale.connect("{C.LINGBOT_VLA_ALIAS}", '
            f'deployment="{checkpoint_id}")',
            cause=f"`dreamscale run {embodiment.name}` drives {embodiment.label} only",
        )
    raise cmd._invalid(
        f"{checkpoint_id} is a LingBot-VLA deployment for the bimanual xArm 7, not "
        f"{embodiment.label}",
        f"run it with `dreamscale run xarm7 --deployment {checkpoint_id}`",
        cause=f"`dreamscale run {embodiment.name}` drives {embodiment.label} only",
    )


def runner(embodiment, checkpoint_id, row, model):
    return _lingbot_vla_runner_model(embodiment, checkpoint_id, row)


@dataclass(frozen=True)
class LingbotUnits(PresetUnits):
    """The shared preset base, plus a custom robot from its export's record."""

    def robot_name(self, spec: dict) -> str:
        if spec.get("preset") == C.CUSTOM_PRESET:
            keys = ", ".join(c.get("key", "?") for c in spec.get("cameras") or ())
            return f"custom robot ({keys})" if keys else "custom robot"
        return self.preset_label

    def robot_line(self, checkpoint: dict) -> str:
        """The preset's line, or a custom robot's: its record's chunk and rate."""
        spec = checkpoint.get("embodiment") or {}
        if spec.get("preset") != C.CUSTOM_PRESET:
            return super().robot_line(checkpoint)
        horizon = spec.get("action_horizon")
        parts = [self.title or self.label, self.robot_name(spec),
                 f"{spec.get('executed_actions') or horizon} of {horizon} actions at "
                 f"{cmd._hz(spec.get('action_hz'))} Hz"]
        if checkpoint.get("rtc_method") and checkpoint.get("status") != "building":
            parts.append(f"RTC {cmd.prefix_rtc(checkpoint)}")
        return " · ".join(parts)

    def create(self, *, repo, given, preset, camera, hz, path, executed, steps, joint_unit, rtc,
               rtc_prefix, revision, name, hf_token, region, wait, keep_warm, slug,
               region_fallback=None) -> None:
        """`deployments create --base lingbot-vla`: the xArm 7 preset as the shared base takes
        it, or `--preset custom` (the export's record names the robot; `--camera key=role`
        renames its cameras, `--joint-unit` names its units, `--hz` its rate where the record
        names none)."""
        if preset != C.CUSTOM_PRESET:
            return super().create(
                repo=repo, given=given, preset=preset, camera=camera, hz=hz, path=path,
                executed=executed, steps=steps, joint_unit=joint_unit, rtc=rtc,
                rtc_prefix=rtc_prefix, revision=revision, name=name, hf_token=hf_token,
                region=region, wait=wait, keep_warm=keep_warm, slug=slug,
                region_fallback=region_fallback)
        unsupported = [key for key, value in given.items()
                       if value is not None and key not in ("path", "executed", "rtc")]
        if steps is not None or unsupported:
            raise cli.typer.BadParameter(
                "a custom LingBot-VLA robot is its export's record; pass only --camera "
                "key=role, --joint-unit, --hz, --path, --executed, --rtc and --rtc-prefix.")
        robot: dict = {"preset": C.CUSTOM_PRESET}
        if camera:
            robot["cameras"] = _role_cameras(camera)
        if joint_unit is not None:
            robot["joint_unit"] = joint_unit
        result = {}
        cli._run(
            lambda **kwargs: result.update(self.run_add(**kwargs)),
            repo=repo, revision=revision, name=name, hf_token=hf_token, path=path,
            executed=executed, rtc=rtc, rtc_prefix=rtc_prefix, region=region or cmd.AUTO_REGION,
            wait=wait, keep_warm=keep_warm, slug=slug, region_fallback=region_fallback,
            robot=robot, hz=hz,
        )
        if result.get("status") == "failed":
            raise cli.typer.Exit(code=1)


def _role_cameras(camera) -> list[dict]:
    """`--camera key=role`: the key the robot sends each of its export's views under."""
    pairs = []
    for item in camera:
        key, sep, role = str(item).partition("=")
        if not sep or not key or role not in C.ROLES:
            raise cli.typer.BadParameter(
                f"--camera takes key=role, the role one of {', '.join(C.ROLES)} (got {item!r})")
        pairs.append({"key": key, "role": role})
    if len({p["key"] for p in pairs}) != len(pairs) or len({p["role"] for p in pairs}) != len(
            pairs):
        raise cli.typer.BadParameter("--camera names each key and role once")
    return pairs


# Its deployments run the bimanual xArm 7 preset or a custom robot: create, the robot line and
# RTC are the shared preset base's, from its transport module's facts, with the custom robot's
# create; Detect's lines are its own.
UNITS = LingbotUnits(
    name=NAME, label="LingBot-VLA", source_format=C.LINGBOT_VLA_SOURCE_FORMAT,
    preset=C.XARM7_PRESET, preset_label=CLI.presets[C.XARM7_PRESET], cameras=C.XARM7_CAMERAS,
    state_dim=C.WIDTH, action_dim=C.WIDTH, action_horizon=C.HORIZON, action_hz=C.ACTION_HZ,
    action_space="absolute_joint_position", joint_unit="rad", gripper_unit="normalized_0_1",
    gripper_indices=C.GRIPPER_INDICES, rtc_contract=C.TRAINED_RTC_CONTRACT,
    max_trained_rtc_delay=C.MAX_TRAINED_RTC_DELAY, title="LingBot-VLA 2.0",
    robot="bimanual xArm 7", describe_found=lingbot_vla_found_lines,
    # `--hz`: its server takes any declared rate and decides (a custom robot's where its record
    # names none; the xArm 7's must be its 20 Hz). The session paces at its record's rate.
    declared_rates=None,
    robot_from_found=_robot_from_found,
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
