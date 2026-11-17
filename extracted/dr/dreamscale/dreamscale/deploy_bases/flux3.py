"""FLUX 3 Action deployments in the SDK: a strict BF16 policy export whose robot shape and
sampler the export records, RTC off or trained (experimental); `dreamscale run so101`,
`dreamscale run yam` and `dreamscale run xarm7` drive its joint-target exports."""

from __future__ import annotations

import time
from typing import Any

from dreamscale.control import ControlPlaneClient
from dreamscale.deploy_bases import Base, DeployBase, ExportedBase, cli, cmd

NAME = "flux-3-action-base"
CLI = Base({"custom": "Custom"}, (
    ("Finding the export", ("building", "resolving", "checking")),
    ("Downloading", ("downloading",)),
    ("Checking weights", ("validating", "sealing", "built")),
    ("Testing on a server", ("qualifying", "ready", "failed")),
), None)


def flux3_robot_line(checkpoint: dict) -> str:
    # Before its build reads the export, a row holds only what its create sent: say
    # what's known ("FLUX 3 Action · model_defined"), never "state None · ? of ?".
    spec = checkpoint.get("embodiment") or {}
    parts = ["FLUX 3 Action"]
    if spec.get("state_dim") is not None:
        parts.append(cmd._widths(spec))
    if spec.get("action_horizon") is not None:
        parts.append(f"{spec.get('executed_actions', '?')} of {spec['action_horizon']} "
                     f"actions at {cmd._hz(spec.get('action_hz'))} Hz")
    parts.append(spec.get("action_space") or "model_defined")
    line = " · ".join(parts)
    # The build settles RTC (trained where the checkpoint trained it); before a build,
    # what Detect read from the checkpoint.
    if checkpoint.get("rtc_method") and checkpoint.get("status") != "building":
        line += f" · RTC {flux3_rtc(checkpoint)}"
    elif not checkpoint.get("rtc_method") and spec.get("trained_rtc_max_delay"):
        line += (f" · trained with RTC (up to {spec['trained_rtc_max_delay']} actions), "
                 "experimental")
    return line


def flux3_rtc(checkpoint: dict) -> str:
    """`trained, experimental (prefix up to 15 of 21 actions)` or `off`."""
    return cmd.prefix_rtc(checkpoint, note="experimental")


# `--preset bimanual_xarm7`: the export's 16 values are the xArm 7 rig's joint targets, aft
# first, seven radians and a 0–1 gripper per arm, which `dreamscale run xarm7` drives. The
# export's own shape and cameras still decide everything else (checked before any upload).
XARM7_PRESET = "bimanual_xarm7"
XARM7_UNITS = {"action_space": "absolute_joint_position", "joint_unit": "rad",
               "gripper_unit": "normalized"}


def _check_xarm7(found: dict) -> None:
    from dreamscale.policy.flux3_deployment import xarm7_camera_keys

    detected = found.get("detected") or {}
    if xarm7_camera_keys({**detected, **XARM7_UNITS}) is None:
        features = [str(c.get("feature")) for c in detected.get("cameras") or []]
        raise cmd._invalid(
            "this export isn't the bimanual xArm 7 layout",
            "deploy it without --preset, then drive it from Python",
            cause=f"--preset {XARM7_PRESET} needs 16 state and action values and the cameras "
            f"images.scene, images.wrist, images.right_wrist in that order; this export has "
            f"{detected.get('state_dim')} and {detected.get('action_dim')} values and "
            f"cameras {', '.join(features) or 'none'}",
        )


def run_add_flux3(*, repo: str, revision=None, name=None, hf_token=None, path=None,
                  region="auto", wait=True, keep_warm=None, slug=None, region_fallback=None,
                  preset=None, client_factory=ControlPlaneClient, print_fn=print,
                  sleep=time.sleep):
    """Inspect the exported contract, pin the resolved commit, and deploy its exact files.
    ``preset``: None (actions mean what the recording meant) or ``bimanual_xarm7``."""
    if preset not in (None, XARM7_PRESET):
        raise cmd._invalid(f"FLUX 3 Action has no preset {preset!r}",
                           f"omit --preset, or pass --preset {XARM7_PRESET}")
    region = cmd._check_region(client_factory, NAME, "FLUX 3 Action", region, print_fn=print_fn)
    folder = cmd.local_checkpoint.scan(repo) if cmd.local_checkpoint.is_local_folder(repo) else None
    if folder and (revision is not None or hf_token is not None):
        raise cmd._invalid(
            "a local folder has no Hub revision or token", "omit --revision and --hf-token"
        )
    token = cmd.hugging_face.token(hf_token) if folder is None else None
    if folder:
        found = cmd._inspect_local(client_factory, folder, print_fn, path=path, base=NAME)
    else:
        _, found = cmd._inspect_with_status(
            client_factory, repo, revision, token, print_fn, base=NAME, path=path,
        )
    if found.get("source_format") != "flux_action":
        raise cmd._invalid(
            "the server did not return a FLUX policy export", "update the SDK and retry"
        )
    if preset == XARM7_PRESET:
        _check_xarm7(found)
    source = found.get("request") or {}
    local = {}
    if folder:
        local = {
            "upload_id": cmd._upload_checkpoint(
                client_factory, folder, found, print_fn, base_model=NAME
            ),
            "source_format": "flux_action", "shown": str(folder.root),
        }
        repo, name = None, name or folder.label
    else:
        repo, revision = source["repo"], source["revision"]
    return cmd.run_add(
        repo=repo, model=NAME, revision=revision, name=name, hf_token=token,
        # The checkpoint owns geometry. Action meaning remains model-defined unless the
        # caller declares it: through the API, or as the xArm 7 rig's joints (--preset).
        embodiment={"preset": "custom", **(XARM7_UNITS if preset == XARM7_PRESET else {})},
        region=region, wait=wait,
        client_factory=client_factory, print_fn=print_fn, sleep=sleep,
        keep_warm=keep_warm, slug=slug, source_path=source.get("source_path", ""),
        # RTC is the export's: trained where it trained with committed prefixes, else off.
        rtc_method=None, region_fallback=region_fallback, **local,
    )


ROBOT_LABELS = {"so101": "SO-101", "yam": "bimanual YAM", "xarm7": "bimanual xArm 7"}


def flux3_robot(declared: Any) -> str | None:
    """The robot whose `dreamscale run` drives a FLUX deployment (a row's ``embodiment`` or a
    session's deployment): so101, yam or xarm7, else None."""
    from dreamscale.policy.flux3_deployment import (
        so101_camera_keys,
        xarm7_camera_keys,
        yam_camera_keys,
    )

    for robot, keys in (("so101", so101_camera_keys), ("yam", yam_camera_keys),
                        ("xarm7", xarm7_camera_keys)):
        if keys(declared) is not None:
            return robot
    return None


def _flux3_runner_model(embodiment: Any, checkpoint_id: str, row: dict) -> str:
    """A FLUX 3 Action deployment `dreamscale run <robot>` drives: joint targets of BFL's
    SO-101 layout on `dreamscale run so101`, of a bimanual YAM recording on `dreamscale run
    yam`, of a bimanual xArm 7 recording on `dreamscale run xarm7`; any other runs from
    Python, with the cameras and state its contract names."""
    from dreamscale.policy.flux3_deployment import XARM7_FEATURES, YAM_FEATURES

    declared = row.get("embodiment") or {}
    robot = flux3_robot(declared)
    if robot == embodiment.name:
        return NAME
    if robot is not None:
        label = ROBOT_LABELS[robot]
        raise cmd._invalid(
            f"{checkpoint_id} is a FLUX 3 Action deployment for {label}, not {embodiment.label}",
            f"run it with `dreamscale run {robot} --deployment {checkpoint_id}`",
            cause=f"`dreamscale run {embodiment.name}` drives {embodiment.label} only",
        )
    cameras = [str(c.get("key")) for c in declared.get("cameras") or []]
    width = declared.get("state_dim")
    training = row.get("training") or {}
    yam_shaped = (
        width == declared.get("action_dim") == 14
        and tuple(c.get("feature") for c in declared.get("cameras") or []) == YAM_FEATURES
    )
    if yam_shaped and declared.get("action_space") == "model_defined" and training.get("run_id"):
        # Deployed before FLUX runs on YAM declared their joints: the same checkpoint, deployed
        # again, runs on `dreamscale run yam` (when its recording names itself a YAM).
        step = training.get("step")
        raise cmd._invalid(
            f"{checkpoint_id} was deployed before `dreamscale run yam` drove FLUX deployments",
            f"deploy its checkpoint again: dreamscale train deploy {training['run_id']}"
            + (f" --step {step}" if step else "")
            + ", then run that deployment",
            cause="its deployment doesn't declare its actions as YAM joint targets",
        )
    xarm7_shaped = (
        width == declared.get("action_dim") == 16
        and tuple(c.get("feature") for c in declared.get("cameras") or []) == XARM7_FEATURES
    )
    if embodiment.name == "xarm7" and xarm7_shaped and (
        declared.get("action_space") == "model_defined"
    ):
        # The export's actions are what its recording meant until its deployment says they are
        # this rig's joints; deployed again with the preset, `dreamscale run xarm7` drives it.
        raise cmd._invalid(
            f"{checkpoint_id} doesn't declare its actions as xArm 7 joint targets",
            "deploy the export again with `dreamscale deployments create <folder> --base "
            f"{NAME} --preset {XARM7_PRESET}`, then run that deployment",
            cause="it was deployed without --preset, so its 16 values mean what its recording "
            "meant",
        )
    frames = ", ".join(f'"{key}": frame' for key in cameras)
    raise cmd._invalid(
        f"{checkpoint_id} is a FLUX 3 Action deployment `dreamscale run` doesn't drive",
        f'drive it from Python: dreamscale.connect("{NAME}", deployment="{checkpoint_id}"), '
        f"then policy.next_action(dreamscale.robot.observation(cameras={{{frames}}}, "
        f"state=[{width} values]), ...)",
        cause="`dreamscale run` drives FLUX deployments of SO-101, bimanual YAM or bimanual "
        "xArm 7 joint targets; this one's actions mean what its recording meant",
    )


def _create_flux3(*, repo, given, preset, camera, hz, path, executed, steps, joint_unit, rtc,
                  rtc_prefix, revision, name, hf_token, region, wait, keep_warm, slug,
                  region_fallback=None) -> None:
    unsupported = {key: value for key, value in given.items() if key != "path"}
    if camera or hz is not None or joint_unit is not None or any(
        value is not None for value in unsupported.values()
    ):
        raise cli.typer.BadParameter(
            "FLUX reads its robot shape and sampler from the policy export; "
            "omit robot, geometry and RTC flags."
        )
    if preset not in (None, XARM7_PRESET):
        raise cli.typer.BadParameter(
            f"FLUX reads its robot shape from the policy export; its only preset is "
            f"{XARM7_PRESET} (the export's actions are the xArm 7 rig's joints).",
            param_hint="'--preset'",
        )
    result: dict = {}
    cli._run(
        lambda **kwargs: result.update(run_add_flux3(**kwargs)),
        repo=repo, revision=revision, name=name, hf_token=hf_token,
        path=path, region=region or cmd.AUTO_REGION, wait=wait,
        keep_warm=keep_warm, slug=slug, region_fallback=region_fallback,
        **({"preset": preset} if preset is not None else {}),
    )
    if result.get("status") == "failed":
        raise cli.typer.Exit(code=1)


def run_command(deployment: dict) -> str | None:
    """A deployment of BFL's SO-101 layout, or of a bimanual YAM or xArm 7 recording: its
    robot's `dreamscale run`."""
    robot = flux3_robot(deployment.get("embodiment") or {})
    return f"dreamscale run {robot} --deployment {deployment['id']}" if robot else None


def runner(embodiment, checkpoint_id, row, model):
    return _flux3_runner_model(embodiment, checkpoint_id, row)


def set_rtc(row, checkpoint_id, method, max_delay, client_factory, print_fn) -> dict:
    return cmd._set_prefix_rtc(row, checkpoint_id, method, max_delay, client_factory, print_fn,
                               label="FLUX 3 Action", describe=flux3_rtc,
                               untrained_fix="it runs RTC off; train with `dreamscale train "
                               "--rtc` to use it")


EXPORTED = ExportedBase(
    "FLUX",
    "dreamscale.policy.flux3_deployment:Flux3SessionDeployment",
    "dreamscale.policy.flux3_deployment:runtime_contract",
    pad_episode_start_commands=True,
    state="refuse",
)
BASE = DeployBase(
    family="flux3", name=NAME, label="FLUX 3 Action", cli=CLI, listed_as=NAME,
    # Rows that carry only the model they serve are FLUX's.
    claims_model=True, robot_line=flux3_robot_line, describe_rtc=flux3_rtc, shows_rtc=True,
    runner=runner, set_rtc=set_rtc, detects_as_base=True, create=_create_flux3,
    exported=EXPORTED, run_command=run_command,
    # Its exports of bimanual xArm 7 recordings (--preset bimanual_xarm7); SO-101 and YAM
    # runs pick FLUX deployments by their own runner checks.
    robots=("xarm7",),
    robot_observe={"xarm7": "dreamscale.policy.flux3_deployment:xarm7_deployment_observe"},
)
