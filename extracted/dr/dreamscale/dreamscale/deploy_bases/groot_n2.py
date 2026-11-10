"""GR00T N2 deployments in the SDK: an Isaac-GR00T N2 checkpoint (a `checkpoint-N/` folder, or a
Hub repo laid out that way) deployed for one of its embodiments, on the Bimanual YAM preset or a
custom robot whose cameras, widths, history and horizon the checkpoint records (plan
docs/plans/2026-11-08-groot-n2-deployments-and-catalog.md). RTC is off.

``deployments create`` names the embodiment with ``--dataset <tag>`` (the export's
``statistics.json`` key, as π0.5's ``--dataset`` names its normalization) when the export carries
several, and takes the robot Detect suggests unless ``--preset`` names another; every robot names
its control rate (``--hz``: the export doesn't record it) and a custom robot, where its names
differ from the checkpoint's, its cameras (``--camera key=feature``). `dreamscale run yam` drives
the YAM preset; its sessions' contract is dreamscale.policy.groot_n2_deployment. Unlisted
(``listed_as=None``): the family is hidden.
"""

from __future__ import annotations

import time
from pathlib import Path

from dreamscale_transport import groot_n2_deploy as C

from dreamscale.deploy_bases import Base, DeployBase, ExportedBase, cli, cmd

NAME = C.GROOT_N2_BASE_MODEL
LABEL = C.GROOT_N2_PUBLIC_NAME
# Its robots and its build's steps, as `deployments create --wait` shows them.
CLI = Base(dict(C.PRESET_LABELS), (
    ("Finding the export", ("building", "resolving", "checking")),
    ("Downloading", ("downloading",)),
    ("Saving", ("validating", "sealing", "built")),
    ("Testing on a server", ("qualifying", "ready", "failed")),
), None)
# The rig `dreamscale run <robot>` drives each preset on.
RUNNERS = {C.YAM_PRESET: "yam"}


def _robot(spec: dict) -> str:
    preset = spec.get("preset")
    if preset in RUNNERS:
        return C.PRESET_LABELS[preset]
    if spec.get("state_dim") is None:
        return "Custom robot"
    unit = f" ({spec['joint_unit']})" if spec.get("joint_unit") else ""
    return f"Custom robot · {cmd._widths(spec)}{unit}"


def groot_n2_robot_line(checkpoint: dict) -> str:
    """`GR00T N2 · Bimanual YAM · xdof_… · 8 of 48 actions at 30 Hz`: before its build reads
    the export, what its create sent."""
    spec = checkpoint.get("embodiment") or {}
    parts = [LABEL, _robot(spec)]
    if spec.get("embodiment_tag"):
        parts.append(spec["embodiment_tag"])
    horizon = spec.get("action_horizon")
    executed = spec.get("executed_actions") or 8
    rate = spec.get("action_hz")
    parts.append((f"{executed} of {horizon} actions" if horizon else f"{executed} actions")
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


def groot_n2_found_lines(found: dict) -> list[str]:
    """What Detect read: which checkpoint and variant, its embodiments, the robot it suggests,
    and what the create must still name."""
    checkpoint = found.get("checkpoint") or {}
    detected = found.get("detected") or {}
    step = checkpoint.get("step")
    where = checkpoint.get("path") or "the folder itself"
    gigabytes = (checkpoint.get("bf16_bytes") or 0) / 1e9
    facts = [f"step {step:,}"] if isinstance(step, int) else []
    facts += [checkpoint["variant"].capitalize()] if checkpoint.get("variant") else []
    facts += [f"{gigabytes:.1f} GB in bf16"] if gigabytes else []
    tags = checkpoint.get("embodiments") or []
    lines = [f"Export: {where}" + (f" ({', '.join(facts)})" if facts else "")]
    if len(tags) > 1:
        lines.append(f"Embodiments: {', '.join(tags)} (name one with --dataset)")
    if detected.get("embodiment_tag"):
        keys = ", ".join(f"{key['key']} ({key['representation']})"
                         for key in detected.get("action_keys") or [])
        lines += [
            f"Embodiment: {detected['embodiment_tag']}",
            f"Robot: {_robot(detected)} (cameras {_cameras(detected)}; "
            f"{detected.get('action_horizon') or '?'}-action chunk, "
            f"{len(detected.get('history_offsets') or []) + 1} frames per camera)",
            *([f"Actions: {keys}"] if keys else []),
        ]
    lines.append("RTC: off")
    return lines + [f"Note: {warning}" for warning in found.get("warnings") or []]


def groot_n2_embodiment(found: dict, *, tag=None, preset=None, cameras=None, hz=None,
                        joint_unit=None, executed=None) -> dict:
    """The robot a create declares (what the control plane's normalize takes): the embodiment
    tag (the export's only one unless named), a preset or a custom robot's cameras (default:
    the checkpoint's own names), its rate and joint unit."""
    checkpoint = found.get("checkpoint") or {}
    detected = found.get("detected") or {}
    tags = list(checkpoint.get("embodiments") or [])
    if tag is None:
        if len(tags) != 1:
            raise cmd._invalid(
                f"this {LABEL} checkpoint carries {len(tags)} embodiments",
                f"name the one to deploy with --dataset ({', '.join(tags) or 'see Detect'})",
                cause="one deployment serves one embodiment")
        tag = tags[0]
    elif tags and tag not in tags:
        raise cmd._invalid(f"{tag} isn't one of this checkpoint's embodiments",
                           f"pass --dataset with one of {', '.join(tags)}")
    if hz is None:
        raise cmd._invalid(f"a {LABEL} deployment names its control rate",
                           "pass --hz, the rate its dataset was recorded at",
                           cause="the checkpoint doesn't record it")
    suggested = detected.get("preset") if detected.get("embodiment_tag") == tag else None
    preset = preset or suggested or "custom"
    if preset not in C.PRESETS:
        raise cmd._invalid(f"{LABEL} runs {', '.join(C.PRESETS)}",
                           f"use --preset {' or --preset '.join(C.PRESETS)}")
    embodiment: dict = {"embodiment_tag": tag, "action_hz": hz}
    if preset == C.YAM_PRESET:
        if cameras or joint_unit is not None:
            raise cmd._invalid(
                f"--preset {C.YAM_PRESET} fixes its cameras and units",
                "omit --camera and --joint-unit, or declare your robot with --preset custom")
        embodiment["preset"] = C.YAM_PRESET
    else:
        if not cameras and detected.get("embodiment_tag") == tag:
            cameras = [dict(camera) for camera in detected.get("cameras") or []]
        if not cameras:
            raise cmd._invalid("a custom robot names its cameras",
                               "pass --camera key=feature for each of the embodiment's cameras")
        embodiment.update(preset="custom", cameras=cameras)
        if joint_unit is not None:
            embodiment.update(action_space="absolute_joint_position", joint_unit=joint_unit)
    if executed is not None:
        embodiment["executed_actions"] = executed
    return embodiment


def run_add_groot_n2(*, repo: str, revision=None, name=None, hf_token=None, path=None, tag=None,
                     preset=None, cameras=None, hz=None, joint_unit=None, executed=None,
                     rtc=None, rtc_prefix=None, region="auto", wait=True, keep_warm=None,
                     slug=None, region_fallback=None, client_factory=None, print_fn=print,
                     sleep=time.sleep):
    """Read a checkpoint folder (a Hub repo or a local folder), pin the resolved commit, and
    deploy one of its embodiments on the robot the create names (``groot_n2_embodiment``)."""
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
    if found.get("source_format") != C.GROOT_N2_SOURCE_FORMAT:
        raise cmd._invalid(f"the server did not read a {LABEL} checkpoint",
                           "update the SDK and retry")
    for line in groot_n2_found_lines(found):
        print_fn(line)
    embodiment = groot_n2_embodiment(
        found, tag=tag, preset=preset, cameras=cameras, hz=hz, joint_unit=joint_unit,
        executed=executed,
    )
    source = found.get("request") or {}
    local = {}
    if folder:
        local = {
            "upload_id": cmd._upload_checkpoint(
                client_factory, folder, found, print_fn, base_model=NAME
            ),
            "source_format": C.GROOT_N2_SOURCE_FORMAT, "shown": str(Path(repo).expanduser()),
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


def _create_groot_n2(
    *, repo, given, preset, camera, hz, path, executed, steps, joint_unit, rtc, rtc_prefix,
    revision, name, hf_token, region, wait, keep_warm, slug, region_fallback=None,
) -> None:
    """`deployments create --base groot-n2`, every option the CLI passes (cli.py's
    `deployments create`): refuse the ones its robot doesn't take, Detect the export, then
    create for the embodiment and robot the options name."""
    from dreamscale.checkpoints_cmd import parse_feature_cameras

    unsupported = [key for key, value in given.items()
                   if value is not None and key not in ("path", "executed", "rtc", "dataset")]
    if steps is not None:
        unsupported.append("steps")
    if unsupported or rtc not in (None, "off") or rtc_prefix is not None:
        flag = cli._flag(unsupported[0]) if unsupported else "--rtc"
        raise cli.typer.BadParameter(
            f"{flag} doesn't apply to {LABEL}: the checkpoint records its widths, horizon, "
            "history and statistics, and it runs RTC off. Pass --dataset (the embodiment), "
            "--preset, --hz, --camera and --joint-unit (a custom robot), --executed and --path."
        )
    if preset is not None and preset not in C.PRESETS:
        raise cli.typer.BadParameter(f"--preset is {', '.join(C.PRESETS)} for {LABEL}")
    try:
        cameras = parse_feature_cameras(camera)
    except ValueError as error:
        raise cli.typer.BadParameter(str(error)) from None
    result: dict = {}
    cli._run(
        lambda **kwargs: result.update(run_add_groot_n2(**kwargs)),
        repo=repo, revision=revision, name=name, hf_token=hf_token, path=path,
        tag=given.get("dataset"), preset=preset, cameras=cameras, hz=hz, joint_unit=joint_unit,
        executed=executed, region=region or cmd.AUTO_REGION, wait=wait, keep_warm=keep_warm,
        slug=slug, region_fallback=region_fallback,
    )
    if result.get("status") == "failed":
        raise cli.typer.Exit(code=1)


# --- `dreamscale run` ----------------------------------------------------------------------------


def runner(embodiment, checkpoint_id, row, model):
    """The model `dreamscale run <robot> --deployment` runs: the base on its preset's rig; a
    clear error, naming how to run it, otherwise."""
    spec = row.get("embodiment") or {}
    robot = RUNNERS.get(spec.get("preset"))
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
        f'drive it from Python: dreamscale.connect("{NAME}", deployment="{checkpoint_id}"), '
        "then policy.next_action(dreamscale.robot.observation(cameras={...}, state=[...]), ...) "
        "with its cameras and state as `deployments show` lists them",
        cause=f"`dreamscale run` drives {LABEL} deployments of the Bimanual YAM preset",
    )


def run_command(deployment: dict) -> str:
    """How to run a deployment: its preset's `dreamscale run`, else Python."""
    robot = RUNNERS.get((deployment.get("embodiment") or {}).get("preset"))
    if robot is not None:
        return f"dreamscale run {robot} --deployment {deployment['id']}"
    return f'dreamscale.connect("{NAME}", deployment="{deployment["id"]}")'


EXPORTED = ExportedBase(
    LABEL,
    "dreamscale.policy.groot_n2_deployment:GrootN2SessionDeployment",
    "dreamscale.policy.groot_n2_deployment:runtime_contract",
)
BASE = DeployBase(
    family="groot_n2", name=NAME, label=LABEL, cli=CLI,
    exported=EXPORTED,
    robot_line=groot_n2_robot_line,
    create=_create_groot_n2,
    detects_as_base=True, found_lines=groot_n2_found_lines,
    runner=runner, run_command=run_command, robots=tuple(RUNNERS.values()),
    # GR00T N2 on the Bimanual YAM as hidden catalog models (2B and 14B) on Dreamscale Labs'
    # deployments: a session carries its deployment's block (the YAM preset's cameras and arms).
    catalog_exports={C.GROOT_N2_YAM_MODEL: EXPORTED, C.GROOT_N2_YAM_14B_MODEL: EXPORTED},
)
