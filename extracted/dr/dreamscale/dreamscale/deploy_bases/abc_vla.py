"""ABC-VLA deployments in the SDK (DSL-286): an upstream checkpoint (a Hub repo, a local
folder or a single ``.pt`` file), its Bimanual YAM preset or a custom robot, RTC off or trained
with a prefix cap; `dreamscale run yam` drives the preset."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from dreamscale.control import ControlPlaneClient
from dreamscale.deploy_bases import Base, DeployBase, ExportedBase, cli, cmd

NAME = "abc-vla-base"
# Its intake: read the checkpoint (as data), download its model tensors, seal them, then
# run it against upstream on a server.
CLI = Base({"bimanual_yam": "Bimanual YAM", "custom": "Custom"}, (
    ("Finding the checkpoint", ("building", "resolving", "checking")),
    ("Downloading", ("downloading",)),
    ("Saving", ("sealing", "built")),
    ("Testing on a server", ("qualifying", "ready", "failed")),
), None)


def _actions(spec: dict) -> str:
    """`20 of 30 actions at 30 Hz`; a checkpoint that records no rate (a custom robot's, before
    its create names one) says so."""
    executed = f"{spec.get('executed_actions')} of {spec['action_horizon']} actions"
    rate = spec.get("action_hz")
    return f"{executed} at {cmd._hz(rate)} Hz" if rate is not None else (
        f"{executed}, rate not recorded")


def abc_vla_robot_line(checkpoint: dict) -> str:
    """One line for an ABC-VLA deployment: robot, widths, geometry, rate and RTC. Before its
    build reads the checkpoint, a row holds only what its create sent."""
    spec = checkpoint.get("embodiment") or {}
    parts = ["ABC-VLA"]
    if spec.get("preset"):
        parts.append(CLI.presets.get(spec["preset"], "Custom"))
    if spec.get("state_dim") is not None:
        parts.append(cmd._widths(spec))
    if spec.get("action_horizon") is not None:
        parts.append(_actions(spec))
    # The build settles RTC (the checkpoint's default unless the create named one).
    if checkpoint.get("rtc_method") and checkpoint.get("status") != "building":
        parts.append(f"RTC {cmd.prefix_rtc(checkpoint)}")
    return " · ".join(parts)


def _describe_abc_vla(checkpoint: dict) -> list[str]:
    source = checkpoint.get("source") or {}
    revision = source.get("resolved_revision") or source.get("revision") or "main"
    spec = checkpoint.get("embodiment") or {}
    path = source.get("path")
    where = f"hf://{source.get('repo')}@{revision}"
    if source.get("kind") == "upload":
        where = f"local checkpoint (upload {source.get('repo')})"
    where += f" · {path}" if path else ""
    cameras = ", ".join(f"{c.get('key')} → {c.get('feature')}" for c in spec.get("cameras") or [])
    geometry = f"executes {_actions(spec)}" if spec.get("action_horizon") is not None else ""
    if spec.get("denoising_steps"):
        geometry += f" · {spec['denoising_steps']} denoising steps"
    lines = [
        f"{cmd._title(checkpoint)}  (ABC-VLA)",
        *cmd._id_line(checkpoint),
        f"  robot:    {abc_vla_robot_line(checkpoint)}",
        *([f"  cameras:  {cameras}"] if cameras else []),
        *([f"  geometry: {geometry}"] if spec.get("action_horizon") else []),
        f"  actions:  {spec.get('action_space') or 'model_defined'}"
        + (f" ({spec['joint_unit']})" if spec.get("joint_unit") else ""),
        f"  rtc:      {cmd.prefix_rtc(checkpoint)}",
        f"  region:   {cmd.region_line(checkpoint)}",
        f"  status:   {checkpoint['status']}",
        f"  source:   {where}",
        f"  size:     {cmd._gb(checkpoint.get('size_bytes'))}",
    ]
    if cmd.autoscaling(checkpoint):
        lines.append(f"  robots:   {cmd.robots_line(checkpoint)} (scales automatically)")
    if checkpoint.get("keep_warm") is not None:
        lines.append(f"  warm:     {cmd.keep_warm_line(checkpoint)}")
    error = checkpoint.get("error")
    if error:
        lines += [f"  error:    {error['code']}: {error['message']}", f"  fix:      {error['fix']}"]
    return lines


def abc_vla_found_lines(found: dict) -> list[str]:
    """What Detect read from an ABC-VLA checkpoint: which one, its robot and its RTC."""
    chosen = found.get("checkpoint") or {}
    step = chosen.get("step")
    others = len(found.get("checkpoints") or []) - 1
    rtc = found.get("rtc") or {}
    trained = rtc.get("trained_max_delay") or 0
    detected = found.get("detected") or {}
    lines = [
        f"Checkpoint: {chosen.get('path')}" + (f" · step {step:,}" if isinstance(step, int)
                                               else "")
        + (f" (newest of {others + 1}; --path picks another)" if others > 0 else ""),
        "Robot: " + abc_vla_robot_line({"embodiment": {
            **detected, "action_horizon": (found.get("architecture") or {}).get(
                "dit", {}).get("chunk_length"),
        }}),
        "RTC: " + (f"trained with prefixes up to {trained} actions (default: trained, "
                   f"prefix up to {min(DEFAULT_ABC_VLA_PREFIX, trained)})" if trained
                   else "not recorded in the checkpoint (off)"),
    ]
    lines += [f"Note: {warning}" for warning in found.get("warnings") or []]
    return lines


# ABC-VLA's default trained-RTC prefix cap (the control plane's, within the trained bound).
DEFAULT_ABC_VLA_PREFIX = 4


def run_add_abc_vla(*, repo: str, revision=None, name=None, hf_token=None, path=None,
                    preset=None, cameras=None, hz=None, executed=None, steps=None,
                    joint_unit=None, rtc=None, rtc_prefix=None, region="auto", wait=True,
                    keep_warm=None, slug=None, region_fallback=None,
                    client_factory=ControlPlaneClient, print_fn=print, sleep=time.sleep):
    """Read an ABC-VLA checkpoint (a Hub repo, a local folder or a ``.pt`` file), pin the
    resolved commit, and deploy it. The checkpoint owns its widths, horizon and statistics;
    the robot names its preset (or its cameras), rate, executed actions and RTC."""
    region = cmd._check_region(client_factory, NAME, "ABC-VLA", region, print_fn=print_fn)
    if rtc not in (None, "off", "trained"):
        raise cmd._invalid("ABC-VLA runs RTC off or trained", "use --rtc off or --rtc trained")
    if rtc_prefix is not None and rtc == "off":
        raise cmd._invalid("--rtc-prefix goes with trained RTC", "omit --rtc-prefix, or --rtc off")
    folder = cmd._local_source(repo, NAME)
    if folder and (revision is not None or hf_token is not None):
        raise cmd._invalid(
            "a local checkpoint has no Hub revision or token", "omit --revision and --hf-token"
        )
    token = cmd.hugging_face.token(hf_token) if folder is None else None
    if folder:
        found = cmd._inspect_local(client_factory, folder, print_fn, path=path, base=NAME)
    else:
        _, found = cmd._inspect_with_status(
            client_factory, repo, revision, token, print_fn, base=NAME, path=path,
        )
    if found.get("source_format") != "abc_vla":
        raise cmd._invalid(
            "the server did not read an ABC-VLA checkpoint", "update the SDK and retry"
        )
    for line in abc_vla_found_lines(found):
        print_fn(line)
    trained = (found.get("rtc") or {}).get("trained_max_delay") or 0
    method = rtc or ("trained" if rtc_prefix is not None else None)
    if method == "trained" and not trained:
        raise cmd._invalid(
            "this checkpoint records no prefix training, so it can't run trained RTC",
            "omit --rtc (it runs RTC off)",
        )
    # A custom robot's rate: the one named, else the one its checkpoint records (a Dreamscale
    # training export's); with neither, the build would refuse it, so refuse before uploading.
    detected = found.get("detected") or {}
    robot = preset or ("custom" if cameras is not None else detected.get("preset"))
    if robot == "custom" and hz is None and detected.get("action_hz") is None:
        raise cmd._invalid(
            "a custom ABC-VLA robot names its control rate",
            "pass --hz, the rate its dataset was recorded at",
            cause="the checkpoint doesn't record it",
        )
    embodiment: dict = {}
    if preset is not None:
        embodiment["preset"] = preset
    if cameras is not None:
        embodiment.update(preset=preset or "custom", cameras=cameras)
    for key, value in (("action_hz", None if hz is None else float(hz)),
                       ("executed_actions", executed), ("denoising_steps", steps)):
        if value is not None:
            embodiment[key] = value
    if joint_unit is not None:
        embodiment.update(action_space="absolute_joint_position", joint_unit=joint_unit)
    source = found.get("request") or {}
    local = {}
    if folder:
        local = {
            "upload_id": cmd._upload_checkpoint(
                client_factory, folder, found, print_fn, base_model=NAME
            ),
            "source_format": "abc_vla", "shown": str(Path(repo).expanduser()),
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
        rtc_method=method, rtc_max_delay=rtc_prefix, region_fallback=region_fallback, **local,
    )


def _abc_vla_runner_model(embodiment: Any, checkpoint_id: str, row: dict) -> str:
    """An ABC-VLA deployment `dreamscale run <robot>` drives: its Bimanual YAM preset on
    `dreamscale run yam`; any other runs from Python."""
    spec = row.get("embodiment") or {}
    if spec.get("preset") == "bimanual_yam" and cmd.RUNNER_PRESETS.get(embodiment.name) == (
        "bimanual_yam"
    ):
        return NAME
    built_for = "Bimanual YAM" if spec.get("preset") == "bimanual_yam" else "a custom robot"
    fix = (
        f"run it with `dreamscale run yam --deployment {checkpoint_id}`"
        if built_for == "Bimanual YAM"
        else f'drive it from Python: dreamscale.connect("{NAME}", '
        f'deployment="{checkpoint_id}"), then policy.next_action(...)'
    )
    raise cmd._invalid(
        f"{checkpoint_id} is an ABC-VLA deployment for {built_for}, not {embodiment.label}",
        fix, cause=f"`dreamscale run {embodiment.name}` drives {embodiment.label} only",
    )



def _create_abc_vla(*, repo, given, preset, camera, hz, path, executed, steps, joint_unit, rtc,
                    rtc_prefix, revision, name, hf_token, region, wait, keep_warm, slug,
                    region_fallback=None) -> None:
    from dreamscale.checkpoints_cmd import KEEP_WARM_VALUES, parse_feature_cameras, parse_region

    unsupported = [key for key, value in given.items()
                   if value is not None and key not in ("path", "executed", "rtc")]
    if unsupported:
        raise cli.typer.BadParameter(
            f"{cli._flag(unsupported[0])} doesn't apply to ABC-VLA: the checkpoint records its "
            "widths, horizon and statistics. Pass --preset or --camera, --hz, --executed, "
            "--steps, --joint-unit, --rtc and --rtc-prefix."
        )
    if keep_warm is not None and keep_warm not in KEEP_WARM_VALUES:
        raise cli.typer.BadParameter(
            f"use one of {', '.join(KEEP_WARM_VALUES)}", param_hint="'--keep-warm'"
        )
    try:
        region = parse_region(region)
        if preset is not None and preset not in CLI.presets:
            raise ValueError("--preset is bimanual_yam or custom for ABC-VLA")
        if rtc is not None and rtc.strip().lower() not in ("off", "trained"):
            raise ValueError(f"--rtc is off or trained for ABC-VLA, got {rtc!r}")
        cameras = parse_feature_cameras(camera)
    except ValueError as error:
        raise cli.typer.BadParameter(str(error)) from None
    result: dict = {}
    cli._run(
        lambda **kwargs: result.update(run_add_abc_vla(**kwargs)),
        repo=repo, revision=revision, name=name, hf_token=hf_token, path=path, preset=preset,
        cameras=cameras, hz=hz, executed=executed, steps=steps, joint_unit=joint_unit,
        rtc=None if rtc is None else rtc.strip().lower(), rtc_prefix=rtc_prefix,
        region=region, wait=wait, keep_warm=keep_warm, slug=slug, region_fallback=region_fallback,
    )
    if result.get("status") == "failed":
        raise cli.typer.Exit(code=1)


def runner(embodiment, checkpoint_id, row, model):
    return _abc_vla_runner_model(embodiment, checkpoint_id, row)


def set_rtc(row, checkpoint_id, method, max_delay, client_factory, print_fn) -> dict:
    return cmd._set_prefix_rtc(row, checkpoint_id, method, max_delay, client_factory, print_fn,
                               label="ABC-VLA")


EXPORTED = ExportedBase(
    "ABC-VLA",
    "dreamscale.policy.abc_vla_deployment:AbcVlaSessionDeployment",
    "dreamscale.policy.abc_vla_deployment:runtime_contract",
)
BASE = DeployBase(
    family="abc_vla", name=NAME, label="ABC-VLA", cli=CLI, aliases=("abc-vla",),
    listed_as=NAME,
    robot_line=abc_vla_robot_line, describe=_describe_abc_vla, shows_rtc=True, runner=runner,
    set_rtc=set_rtc, detects_as_base=True, found_lines=abc_vla_found_lines,
    local_archive=True, create=_create_abc_vla, exported=EXPORTED,
    # The shared catalog model: the public checkpoint on Bimanual YAM, served by ABC-VLA
    # deployments, so its session carries the same deployment block.
    catalog_exports={"abc-vla-yam": EXPORTED},
)
