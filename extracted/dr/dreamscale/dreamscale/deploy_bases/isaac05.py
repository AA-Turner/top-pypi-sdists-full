"""Deploy Isaac 0.5 using a Hugging Face export in the base's layout (or a
managed training run's), on a robot preset (Bimanual YAM, SO-101) or a custom robot, with 1 or
3 context frames, its executed actions and RTC off or trained with a prefix cap, all sealed at
create; `dreamscale run yam` and `dreamscale run so101` drive the presets."""

from __future__ import annotations

import time
from dataclasses import replace
from typing import Any

from dreamscale.control import ControlPlaneClient
from dreamscale.deploy_bases import Base, DeployBase, ExportedBase, cli, cmd
from dreamscale.deploy_bases.isaac05_legacy import BASE as LEGACY

NAME = "isaac05-base"
PUBLIC = "isaac0.5"
# Its intake: read the export (as data), download it (71-143 GB), convert it to BF16, seal it,
# then run it against Perceptron's own sampler on a server.
CLI = Base({"bimanual_yam": "Bimanual YAM", "so101": "SO-101", "custom": "Custom"}, (
    ("Finding the export", ("building", "resolving", "checking")),
    ("Downloading", ("downloading",)),
    ("Converting", ("converting",)),
    ("Saving", ("validating", "sealing", "built")),
    ("Testing on a server", ("qualifying", "ready", "failed")),
), "usually about 15 min")
CONTEXT_FRAMES = (1, 3)
# The robots `dreamscale run <robot>` drives, by the preset each one is.
_RUNNERS = {"bimanual_yam": "yam", "so101": "so101"}


def isaac05_robot_line(checkpoint: dict) -> str:
    """One line for an Isaac 0.5 deployment: robot, widths, geometry, context and RTC. Before
    its build reads the export, a row holds only what its create sent."""
    spec = checkpoint.get("embodiment") or {}
    parts = ["Isaac 0.5"]
    if spec.get("preset"):
        parts.append(CLI.presets.get(spec["preset"], "Custom"))
    if spec.get("state_dim") is not None:
        parts.append(cmd._widths(spec))
    if spec.get("model_horizon") is not None:
        parts.append(f"{spec.get('executed_actions')} of {spec['model_horizon']} actions at "
                     f"{cmd._hz(spec.get('action_hz'))} Hz")
    if spec.get("n_obs_steps") is not None:
        frames = spec["n_obs_steps"]
        parts.append(f"{frames} frame{'s' if frames != 1 else ''} per camera")
    if checkpoint.get("rtc_method") and checkpoint.get("status") != "building":
        parts.append(f"RTC {cmd.prefix_rtc(checkpoint)}")
    elif not checkpoint.get("rtc_method") and spec.get("trained_rtc_max_delay"):
        parts.append(f"trained with RTC (up to {spec['trained_rtc_max_delay']} actions)")
    return " · ".join(parts)


def _describe_isaac05(checkpoint: dict) -> list[str]:
    source = checkpoint.get("source") or {}
    revision = source.get("resolved_revision") or source.get("revision") or "main"
    spec = checkpoint.get("embodiment") or {}
    where = f"hf://{source.get('repo')}@{revision}"
    if source.get("kind") == "training":
        where = f"training run {source.get('repo')}"
    cameras = ", ".join(f"{c.get('key')} → {c.get('view')}" for c in spec.get("cameras") or [])
    lines = [
        f"{cmd._title(checkpoint)}  (Isaac 0.5)",
        *cmd._id_line(checkpoint),
        f"  robot:    {isaac05_robot_line(checkpoint)}",
        *([f"  cameras:  {cameras}"] if cameras else []),
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


def _trained(found: dict) -> int:
    trained = (found.get("rtc") or {}).get("trained_max_delay")
    if trained is None:
        trained = (found.get("detected") or {}).get("trained_rtc_max_delay") or 0
    return int(trained)


def _suggested(found: dict) -> dict:
    """The custom robot the export's own deployment adapter proposes, in the create's terms."""
    suggested = dict(found.get("suggested") or {})
    if "dataset" in suggested:
        suggested["policy_state_dataset"] = suggested.pop("dataset")
    if "image_size" in suggested:
        suggested["image_hw"] = suggested.pop("image_size")
    return {key: value for key, value in suggested.items()
            if key in ("preset", "cameras", "policy_state_dataset", "image_hw", "robot_type",
                       "control_mode", "executed_actions", "action_hz")}


def isaac05_found_lines(found: dict) -> list[str]:
    """What Detect read from an Isaac 0.5 export: the presets it can run, the robot its adapter
    proposes, its statistics and its RTC."""
    presets = found.get("presets") or {}
    runs = [CLI.presets[preset] for preset in ("bimanual_yam", "so101") if presets.get(preset)]
    suggested = _suggested(found)
    trained = _trained(found)
    lines = [
        "Presets: " + (", ".join(runs) if runs else "none (its statistics cover neither)")
        + " (--preset), or a custom robot (--camera key=view ... --dataset NAME)",
    ]
    if suggested.get("cameras"):
        cameras = ", ".join(f"{c.get('key')}={c.get('view')}" for c in suggested["cameras"])
        lines.append(f"Its adapter proposes: --camera {cameras} --dataset "
                     f"{suggested.get('policy_state_dataset')}")
    lines.append("RTC: " + (f"trained with prefixes up to {trained} actions (default: trained, "
                            f"prefix up to {trained})" if trained
                            else "not recorded in the export (off)"))
    datasets = found.get("datasets") or []
    if datasets:
        lines.append("Robot unit conversions: " + ", ".join(
            f"{d['dataset']} ({d['action_dim']} actions · {d['state_dim']} state)"
            for d in datasets[:8]))
    lines += [f"Note: {warning}" for warning in found.get("warnings") or []]
    return lines


def run_add_isaac05(*, repo: str, revision=None, name=None, hf_token=None, preset=None,
                    cameras=None, dataset=None, hz=None, executed=None, context=None, rtc=None,
                    rtc_prefix=None, region="auto", wait=True, keep_warm=None, slug=None,
                    region_fallback=None, client_factory=ControlPlaneClient, print_fn=print,
                    sleep=time.sleep):
    """Read an Isaac 0.5 export on the Hub, pin the resolved commit, and deploy it on a robot:
    a preset (Bimanual YAM, SO-101) or a custom robot's cameras (key=view) and statistics'
    dataset. The deployment seals its context frames (1 or 3; default 3), the actions it
    executes per chunk (1-50; default 30) and its RTC (default: trained where the export
    trained it, with every prefix row it trained, else off)."""
    folder = cmd._local_source(repo, NAME)
    if folder and (revision or hf_token):
        raise cmd._invalid("a local folder has no Hub revision or token",
                           "omit --revision and --hf-token")
    region = cmd._check_region(client_factory, NAME, "Isaac 0.5", region, print_fn=print_fn)
    if preset not in (None, *CLI.presets):
        raise cmd._invalid("--preset is bimanual_yam, so101 or custom for Isaac 0.5",
                           "pass --preset bimanual_yam|so101, or --camera key=view ...")
    if rtc not in (None, "off", "trained", "test_time"):
        raise cmd._invalid("Isaac 0.5 runs RTC off, trained or test_time",
                           "use --rtc off, --rtc trained or --rtc test_time")
    if rtc_prefix is not None and rtc == "off":
        raise cmd._invalid("--rtc-prefix goes with RTC on", "omit --rtc-prefix, or --rtc off")
    if context is not None and context not in CONTEXT_FRAMES:
        raise cmd._invalid("--context is 1 or 3 frames per camera",
                           "pass --context 3 (the default) or --context 1")
    if executed is not None and not 1 <= executed <= 50:
        raise cmd._invalid("--executed is 1-50 actions per chunk", "pass --executed 30")
    token = None if folder else cmd.hugging_face.token(hf_token)
    if folder:
        found = cmd._inspect_local(client_factory, folder, print_fn, base=NAME)
    else:
        _, found = cmd._inspect_with_status(
            client_factory, repo, revision, token, print_fn, base=NAME,
        )
    if found.get("source_format") != "isaac05":
        raise cmd._invalid("the server did not read an Isaac 0.5 export",
                           "update the SDK and retry")
    for line in isaac05_found_lines(found):
        print_fn(line)
    trained = _trained(found)
    method = rtc or ("trained" if rtc_prefix is not None else None)
    if method == "trained" and not trained:
        raise cmd._invalid(
            "this export records no prefix training, so it can't run trained RTC",
            "omit --rtc (it runs RTC off)",
        )
    if method == "trained" and rtc_prefix is not None and not 1 <= rtc_prefix <= trained:
        raise cmd._invalid(f"the RTC prefix is 1-{trained} actions (what the export was trained "
                           "on)", f"pass --rtc-prefix 1-{trained}")
    presets = found.get("presets") or {}
    if preset in ("bimanual_yam", "so101") and not presets.get(preset):
        raise cmd._invalid(
            f"this export has no {CLI.presets[preset]} statistics to run that preset with",
            "fine-tune on the robot's own data, or pass --camera key=view ... --dataset NAME",
        )
    embodiment: dict = {}
    if cameras:
        embodiment.update(preset="custom", cameras=cameras)
    elif preset in ("bimanual_yam", "so101"):
        embodiment["preset"] = preset
    elif _suggested(found).get("cameras"):
        # The robot the export's own adapter declares (the flags below edit it).
        embodiment.update(_suggested(found), preset="custom")
    for key, value in (("policy_state_dataset", dataset),
                       ("action_hz", None if hz is None else float(hz)),
                       ("executed_actions", executed), ("n_obs_steps", context)):
        if value is not None:
            embodiment[key] = value
    if embodiment.get("preset") in (None, "custom") and not (
        embodiment.get("cameras") and embodiment.get("policy_state_dataset")
    ):
        raise cmd._invalid(
            "name the robot this export runs on",
            "pass --preset bimanual_yam|so101, or --camera key=view (repeated, in the order "
            "your robot sends them) and --dataset NAME (the statistics it was trained with)",
        )
    source = found.get("source") or found.get("request") or {}
    local = {}
    if folder:
        upload_id = cmd._upload_checkpoint(client_factory, folder, found, print_fn, base_model=NAME)
        local = {"upload_id": upload_id, "source_format": "isaac05", "shown": str(folder.root)}
        repo, name = None, name or folder.label
    else:
        repo, revision = source.get("repo", repo), source.get("revision", revision)
    return cmd.run_add(
        repo=repo, model=NAME, revision=revision,
        name=name, hf_token=token, embodiment=embodiment, region=region, wait=wait,
        client_factory=client_factory, print_fn=print_fn, sleep=sleep, keep_warm=keep_warm,
        slug=slug, source_path=source.get("path", source.get("source_path", "")), rtc_method=method,
        rtc_max_delay=rtc_prefix, region_fallback=region_fallback, **local,
    )


def _isaac05_runner_model(embodiment: Any, checkpoint_id: str, row: dict) -> str:
    """An Isaac 0.5 deployment `dreamscale run <robot>` drives: its preset's robot (Bimanual
    YAM on `dreamscale run yam`, SO-101 on `dreamscale run so101`); a custom robot runs from
    Python."""
    preset = (row.get("embodiment") or {}).get("preset")
    if preset in _RUNNERS and cmd.RUNNER_PRESETS.get(embodiment.name) == preset:
        return NAME
    built_for = CLI.presets.get(preset) if preset in _RUNNERS else "a custom robot"
    fix = (
        f"run it with `dreamscale run {_RUNNERS[preset]} --deployment {checkpoint_id}`"
        if preset in _RUNNERS
        else f'drive it from Python: dreamscale.connect("{PUBLIC}", '
        f'deployment="{checkpoint_id}"), then policy.next_action(...)'
    )
    raise cmd._invalid(
        f"{checkpoint_id} is an Isaac 0.5 deployment for {built_for}, not {embodiment.label}",
        fix, cause=f"`dreamscale run {embodiment.name}` drives {embodiment.label} only",
    )


def _create_isaac05(*, repo, given, preset, camera, hz, path, executed, steps, joint_unit, rtc,
                    rtc_prefix, revision, name, hf_token, region, wait, keep_warm, slug,
                    region_fallback=None) -> None:
    from dreamscale.checkpoints_cmd import KEEP_WARM_VALUES, parse_cameras, parse_region

    own = ("context", "dataset", "chunk", "executed", "rtc")
    unsupported = [key for key, value in given.items() if value is not None and key not in own]
    unsupported += [key for key, value in (("steps", steps), ("joint_unit", joint_unit))
                    if value is not None]
    if unsupported:
        raise cli.typer.BadParameter(
            f"{cli._flag(unsupported[0])} doesn't apply to Isaac 0.5: the export records its "
            "widths and statistics. Pass --preset or --camera and --dataset, --hz, --executed, "
            "--context, --rtc and --rtc-prefix."
        )
    if keep_warm is not None and keep_warm not in KEEP_WARM_VALUES:
        raise cli.typer.BadParameter(
            f"use one of {', '.join(KEEP_WARM_VALUES)}", param_hint="'--keep-warm'"
        )
    if given.get("chunk") is not None and executed is not None:
        raise cli.typer.BadParameter("--chunk is --executed's older name: pass one of them")
    try:
        region = parse_region(region)
        if rtc is not None and rtc.strip().lower() not in ("off", "trained", "test_time"):
            raise ValueError(f"--rtc is off, trained or test_time for Isaac 0.5, got {rtc!r}")
        cameras = parse_cameras(camera)
    except ValueError as error:
        raise cli.typer.BadParameter(str(error)) from None
    result: dict = {}
    cli._run(
        lambda **kwargs: result.update(run_add_isaac05(**kwargs)),
        repo=repo, revision=revision, name=name, hf_token=hf_token, preset=preset,
        cameras=cameras, dataset=given.get("dataset"), hz=hz,
        executed=executed if executed is not None else given.get("chunk"),
        context=given.get("context"), rtc=None if rtc is None else rtc.strip().lower(),
        rtc_prefix=rtc_prefix, region=region, wait=wait, keep_warm=keep_warm, slug=slug,
        region_fallback=region_fallback,
    )
    if result.get("status") == "failed":
        raise cli.typer.Exit(code=1)


def runner(embodiment, checkpoint_id, row, model):
    return _isaac05_runner_model(embodiment, checkpoint_id, row)


def set_rtc(row, checkpoint_id, method, max_delay, client_factory, print_fn) -> dict:
    return cmd._set_prefix_rtc(row, checkpoint_id, method, max_delay, client_factory, print_fn,
                               label="Isaac 0.5")


EXPORTED = ExportedBase(
    "Isaac 0.5",
    "dreamscale.policy.isaac05_deployment:Isaac05SessionDeployment",
    "dreamscale.policy.isaac05_deployment:runtime_contract",
)
# The catalog model runs in sync unless a run asks for async (its RTC is training-time).
CATALOG_EXPORTED = ExportedBase(
    "Isaac 0.5",
    "dreamscale.policy.isaac05_deployment:Isaac05SessionDeployment",
    "dreamscale.policy.isaac05_deployment:catalog_runtime_contract",
)
BASE = DeployBase(
    family="isaac05", name=NAME, label="Isaac 0.5", cli=CLI,
    aliases=(PUBLIC, "isaac05"), creates_as=PUBLIC,
    robot_line=isaac05_robot_line, describe=_describe_isaac05, shows_rtc=True, runner=runner,
    set_rtc=set_rtc, detects_as_base=True, found_lines=isaac05_found_lines,
    create=_create_isaac05, exported=EXPORTED,
    # Perceptron's Isaac-0.5-YAM, -SO100_101 and -LIBERO as catalog models on Dreamscale Labs'
    # deployments: a session carries its deployment's block, run in sync by default (each chunk
    # to its end; `--mode async` replans with a package's training-time RTC; DSL-457).
    catalog_exports={"isaac05-yam": CATALOG_EXPORTED, "isaac05-so101": CATALOG_EXPORTED,
                     "isaac05-libero": CATALOG_EXPORTED},
)

# The units adapter owns both historical CLI shorthands. Explicit
# endpoint and deployment IDs continue to select the original request shape.
LEGACY_BASES = (replace(LEGACY, aliases=()),)
