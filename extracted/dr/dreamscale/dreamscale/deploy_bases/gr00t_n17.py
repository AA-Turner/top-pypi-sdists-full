"""GR00T N1.7 deployments in the SDK: an Isaac-GR00T fine-tune (a `checkpoint-N/` folder, or a
Hub repo laid out that way) on the Bimanual YAM or SO-101 preset, or a custom robot whose
cameras, widths and horizon the checkpoint records (plan docs/plans/2026-11-02-gr00t-n17.md
§6.1). RTC is off.

``deployments create`` takes the robot Detect suggests unless ``--preset`` names another: an
SO-101 create names the unit its joints were trained in (``--joint-unit deg``, what `dreamscale
run so101` sends; any other unit is the robot's own deployment, driven from Python), and a
custom robot names its control rate (``--hz``) and, where the robot's names differ from the
checkpoint's, its cameras (``--camera key=feature``). `dreamscale run yam` and `dreamscale run
so101` drive the presets; its sessions' contract is dreamscale.policy.gr00t_n17_deployment.
Unlisted (``listed_as=None``) until GA; ``--base gr00t-n1.7`` names it.
"""

from __future__ import annotations

import time
from pathlib import Path

from dreamscale_transport import gr00t_n17_deploy as C

from dreamscale.deploy_bases import Base, DeployBase, ExportedBase, cli, cmd

NAME = C.GR00T_N17_BASE_MODEL
PUBLIC = "gr00t-n1.7"
LABEL = C.GR00T_N17_PUBLIC_NAME
# Its robots and its build's steps, as `deployments create --wait` shows them.
CLI = Base(dict(C.PRESET_LABELS), (
    ("Finding the export", ("building", "resolving", "checking")),
    ("Downloading", ("downloading",)),
    ("Saving", ("validating", "sealing", "built")),
    ("Testing on a server", ("qualifying", "ready", "failed")),
), None)
# The rig `dreamscale run <robot>` drives each preset on.
RUNNERS = {C.PRESET: "yam", C.SO101_PRESET: "so101"}
# The SO-101 units an SO-101 create may name: degrees run on `dreamscale run so101`; LeRobot's
# ±100 range is the robot's own deployment.
SO101_UNITS = ("deg", "range_m100_100")


def _robot(spec: dict) -> str:
    preset = spec.get("preset")
    if preset in (C.PRESET, C.SO101_PRESET):
        return C.PRESET_LABELS[preset]
    if spec.get("state_dim") is None:
        return "Custom robot"
    unit = f" ({spec['joint_unit']})" if spec.get("joint_unit") else ""
    return f"Custom robot · {cmd._widths(spec)}{unit}"


def gr00t_n17_robot_line(checkpoint: dict) -> str:
    """`GR00T N1.7 · SO-101 · 8 of 16 actions at 30 Hz`: before its build reads the export, what
    its create sent."""
    spec = checkpoint.get("embodiment") or {}
    parts = [LABEL, _robot(spec)]
    horizon = spec.get("action_horizon") or C.ACTION_HORIZON
    executed = spec.get("executed_actions") or horizon // 2
    rate = spec.get("action_hz") or (C.ACTION_HZ if spec.get("preset") in RUNNERS else None)
    parts.append(f"{executed} of {horizon} actions"
                 + (f" at {cmd._hz(rate)} Hz" if rate is not None else ""))
    return " · ".join(parts)


def _cameras(detected: dict) -> str:
    """A preset's cameras by the checkpoint's names; a custom robot's, each robot key that
    differs from the checkpoint camera it fills shown beside it."""
    preset = detected.get("preset") in RUNNERS
    return ", ".join(
        camera["feature"] if preset or camera["key"] == camera["feature"]
        else f"{camera['key']} → {camera['feature']}"
        for camera in detected.get("cameras") or [])


def gr00t_n17_found_lines(found: dict) -> list[str]:
    """What Detect read: which checkpoint, the robot it suggests, and what the create must
    still name."""
    checkpoint = found.get("checkpoint") or {}
    detected = found.get("detected") or {}
    step = checkpoint.get("step")
    where = checkpoint.get("path") or "the folder itself"
    gigabytes = (checkpoint.get("bf16_bytes") or 0) / 1e9
    keys = ", ".join(f"{key['key']} ({key['representation']})"
                     for key in checkpoint.get("action_keys") or [])
    facts = [f"step {step:,}"] if isinstance(step, int) else []
    facts += [f"{gigabytes:.1f} GB in bf16"] if gigabytes else []
    lines = [
        f"Export: {where}" + (f" ({', '.join(facts)})" if facts else ""),
        f"Robot: {_robot(detected)} (cameras {_cameras(detected)}; "
        f"{checkpoint.get('action_horizon') or '?'}-action chunk)",
        *([f"Actions: {keys}"] if keys else []),
        "RTC: off",
    ]
    return lines + [f"Note: {warning}" for warning in found.get("warnings") or []]


def gr00t_n17_embodiment(detected: dict, *, preset=None, cameras=None, hz=None,
                         joint_unit=None, executed=None) -> dict:
    """The robot a create declares (what the control plane's normalize takes): a preset, or a
    custom robot's cameras (default: the checkpoint's own names), rate and joint unit."""
    preset = preset or detected.get("preset") or "custom"
    if preset not in C.PRESETS:
        raise cmd._invalid(f"{LABEL} runs {', '.join(C.PRESETS)}",
                           f"use --preset {' or --preset '.join(C.PRESETS)}")
    if preset == C.PRESET:
        if cameras or hz is not None or joint_unit is not None:
            raise cmd._invalid(
                f"--preset {C.PRESET} fixes its cameras, rate and units",
                "omit --camera, --hz and --joint-unit, or declare your robot with --preset "
                "custom")
        embodiment: dict = {"preset": C.PRESET}
    elif preset == C.SO101_PRESET:
        if cameras or hz is not None:
            raise cmd._invalid(f"--preset {C.SO101_PRESET} fixes its cameras and rate",
                               "omit --camera and --hz, or declare your robot with --preset "
                               "custom")
        if joint_unit not in SO101_UNITS:
            raise cmd._invalid(
                "an SO-101 checkpoint names the unit its joints were trained in",
                "pass --joint-unit deg for current LeRobot degrees (what `dreamscale run "
                "so101` sends), or --joint-unit range_m100_100 for LeRobot's ±100 range",
                cause="the checkpoint's statistics can't tell the two apart")
        embodiment = {"preset": C.SO101_PRESET, "joint_unit": joint_unit}
    else:
        if hz is None:
            raise cmd._invalid(
                "a custom GR00T N1.7 robot names its control rate",
                "pass --hz, the rate its dataset was recorded at",
                cause="the checkpoint doesn't record it")
        cameras = cameras or [dict(camera) for camera in detected.get("cameras") or []]
        if not cameras:
            raise cmd._invalid("a custom robot names its cameras",
                               "pass --camera key=feature for each of the checkpoint's cameras")
        embodiment = {"preset": "custom", "cameras": cameras, "action_hz": hz}
        if joint_unit is not None:
            embodiment.update(action_space="absolute_joint_position", joint_unit=joint_unit)
    if executed is not None:
        embodiment["executed_actions"] = executed
    return embodiment


def run_add_gr00t_n17(*, repo: str, revision=None, name=None, hf_token=None, path=None,
                      preset=None, cameras=None, hz=None, joint_unit=None, executed=None,
                      rtc=None, rtc_prefix=None, region="auto", wait=True, keep_warm=None,
                      slug=None, region_fallback=None, client_factory=None, print_fn=print,
                      sleep=time.sleep):
    """Read a checkpoint folder (a Hub repo or a local folder), pin the resolved commit, and
    deploy it on the robot the create names (``gr00t_n17_embodiment``)."""
    if client_factory is None:
        from dreamscale.control import ControlPlaneClient

        client_factory = ControlPlaneClient
    if rtc not in (None, "off") or rtc_prefix is not None:
        raise cmd._invalid(f"{LABEL} runs RTC off", "omit --rtc and --rtc-prefix")
    region = cmd._check_region(client_factory, NAME, LABEL, region, print_fn=print_fn)
    folder = cmd._local_source(repo, NAME)
    if folder and (revision is not None or hf_token is not None):
        raise cmd._invalid("a local checkpoint has no Hub revision or token",
                           "omit --revision and --hf-token")
    token = cmd.hugging_face.token(hf_token) if folder is None else None
    if folder:
        found = cmd._inspect_local(client_factory, folder, print_fn, path=path, base=NAME)
    else:
        _, found = cmd._inspect_with_status(
            client_factory, repo, revision, token, print_fn, base=NAME, path=path,
        )
    if found.get("source_format") != C.GR00T_N17_SOURCE_FORMAT:
        raise cmd._invalid(f"the server did not read a {LABEL} checkpoint",
                           "update the SDK and retry")
    for line in gr00t_n17_found_lines(found):
        print_fn(line)
    embodiment = gr00t_n17_embodiment(
        found.get("detected") or {}, preset=preset, cameras=cameras, hz=hz,
        joint_unit=joint_unit, executed=executed,
    )
    source = found.get("request") or {}
    local = {}
    if folder:
        local = {
            "upload_id": cmd._upload_checkpoint(
                client_factory, folder, found, print_fn, base_model=NAME
            ),
            "source_format": C.GR00T_N17_SOURCE_FORMAT, "shown": str(Path(repo).expanduser()),
        }
        repo, name = None, name or folder.label
    else:
        repo, revision = source["repo"], source["revision"]
    return cmd.run_add(
        repo=repo, model=NAME, revision=revision, name=name, hf_token=token,
        embodiment=embodiment, region=region, wait=wait,
        client_factory=client_factory, print_fn=print_fn, sleep=sleep,
        keep_warm=keep_warm, slug=slug,
        source_path=source.get("source_path") or (found.get("source") or {}).get("path", ""),
        rtc_method="off", rtc_max_delay=None, region_fallback=region_fallback, **local,
    )


def _create(*, repo, given, preset, camera, hz, path, executed, steps, joint_unit, rtc,
            rtc_prefix, revision, name, hf_token, region, wait, keep_warm, slug,
            region_fallback=None) -> None:
    from dreamscale.checkpoints_cmd import parse_feature_cameras

    unsupported = [key for key, value in given.items()
                   if value is not None and key not in ("path", "executed", "rtc")]
    if steps is not None:
        unsupported.append("steps")
    if unsupported or rtc not in (None, "off") or rtc_prefix is not None:
        flag = cli._flag(unsupported[0]) if unsupported else "--rtc"
        raise cli.typer.BadParameter(
            f"{flag} doesn't apply to {LABEL}: the checkpoint records its widths, horizon and "
            "statistics, and it runs RTC off. Pass --preset, --joint-unit (SO-101 or a custom "
            "robot's joints), --camera and --hz (a custom robot), --executed and --path."
        )
    if preset is not None and preset not in C.PRESETS:
        raise cli.typer.BadParameter(f"--preset is {', '.join(C.PRESETS)} for {LABEL}")
    try:
        cameras = parse_feature_cameras(camera)
    except ValueError as error:
        raise cli.typer.BadParameter(str(error)) from None
    result: dict = {}
    cli._run(
        lambda **kwargs: result.update(run_add_gr00t_n17(**kwargs)),
        repo=repo, revision=revision, name=name, hf_token=hf_token, path=path, preset=preset,
        cameras=cameras, hz=hz, joint_unit=joint_unit, executed=executed,
        region=region or cmd.AUTO_REGION, wait=wait, keep_warm=keep_warm, slug=slug,
        region_fallback=region_fallback,
    )
    if result.get("status") == "failed":
        raise cli.typer.Exit(code=1)


# --- `dreamscale run` ----------------------------------------------------------------------------


def _runs_on(spec: dict) -> str | None:
    """The rig a deployment's preset runs on (its preset's cameras, widths and units), else
    None: a custom robot, or an SO-101 checkpoint in its own units, runs from Python."""
    robot = RUNNERS.get(spec.get("preset"))
    if robot == "so101" and spec.get("joint_unit", "deg") != "deg":
        return None
    return robot


def runner(embodiment, checkpoint_id, row, model):
    """The model `dreamscale run <robot> --deployment` runs: the base on its preset's rig; a
    clear error, naming how to run it, otherwise."""
    spec = row.get("embodiment") or {}
    robot = _runs_on(spec)
    if robot == embodiment.name:
        return NAME
    if robot is not None:
        raise cmd._invalid(
            f"{checkpoint_id} is a {LABEL} deployment for {C.PRESET_LABELS[spec['preset']]}, "
            f"not {embodiment.label}",
            f"run it with `dreamscale run {robot} --deployment {checkpoint_id}`",
            cause=f"`dreamscale run {embodiment.name}` drives {embodiment.label} only",
        )
    raise cmd._invalid(
        f"{checkpoint_id} is a {LABEL} deployment for a custom robot, which `dreamscale run` "
        "doesn't drive",
        f'drive it from Python: dreamscale.connect("{PUBLIC}", deployment="{checkpoint_id}"), '
        "then policy.next_action(dreamscale.robot.observation(cameras={...}, state=[...]), ...) "
        "with its cameras and state as `deployments show` lists them",
        cause=f"`dreamscale run` drives {LABEL} deployments of the Bimanual YAM and SO-101 "
        "(degrees) presets",
    )


def run_command(deployment: dict) -> str:
    """How to run a deployment: its preset's `dreamscale run`, else Python."""
    robot = _runs_on(deployment.get("embodiment") or {})
    if robot is not None:
        return f"dreamscale run {robot} --deployment {deployment['id']}"
    return f'dreamscale.connect("{PUBLIC}", deployment="{deployment["id"]}")'


EXPORTED = ExportedBase(
    LABEL,
    "dreamscale.policy.gr00t_n17_deployment:Gr00tN17SessionDeployment",
    "dreamscale.policy.gr00t_n17_deployment:runtime_contract",
)
BASE = DeployBase(
    family="gr00t_n17", name=NAME, label=LABEL, cli=CLI, aliases=(PUBLIC,), creates_as=PUBLIC,
    robot_line=gr00t_n17_robot_line, detects_as_base=True, found_lines=gr00t_n17_found_lines,
    create=_create, exported=EXPORTED, runner=runner, run_command=run_command,
    robots=tuple(RUNNERS.values()),
)
