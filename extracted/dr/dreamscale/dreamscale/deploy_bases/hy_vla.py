"""Hy-VLA deployments in the SDK: an upstream ``save_pretrained`` export, the bimanual xArm 7
preset or a custom robot, end-effector pose rows, RTC off or trained; `dreamscale run xarm7`
drives the preset."""

from __future__ import annotations

import time
from typing import Any

from dreamscale_transport.hy_vla_deploy import MAX_HZ, MIN_HZ, normalize_rate

from dreamscale.control import ControlPlaneClient
from dreamscale.deploy_bases import Base, DeployBase, ExportedBase, cli, cmd

NAME = "hy-vla"
# Its intake: read the export (as data), download it, seal it, then run it against upstream
# on a server. Its preset is detected from the export.
CLI = Base({"bimanual_xarm7": "Bimanual xArm 7", "custom": "Custom"}, (
    ("Finding the export", ("building", "resolving", "checking")),
    ("Downloading", ("downloading",)),
    ("Saving", ("validating", "sealing", "built")),
    ("Testing on a server", ("qualifying", "ready", "failed")),
), None)
# The rates a create may declare (`--hz`, sent as its robot's ``action_hz``), as
# ``PresetUnits.declared_rates`` reads: None, any of MIN_HZ-MAX_HZ (the export's recorded rate,
# where Detect read one: ``run_add_hy_vla`` refuses another before anything is uploaded).
DECLARED_RATES: tuple[float, ...] | None = None


def takes_rate(hz: Any) -> bool:
    """Whether a create may declare ``hz`` (``DECLARED_RATES``)."""
    return DECLARED_RATES is None or (
        isinstance(hz, int | float) and not isinstance(hz, bool) and float(hz) in DECLARED_RATES)


def hy_vla_robot_line(checkpoint: dict) -> str:
    """One line for a Hy-VLA deployment: robot, geometry, rate and RTC. Before its build reads
    the export, a row holds only what its create sent."""
    spec = checkpoint.get("embodiment") or {}
    parts = ["Hy-VLA"]
    if spec.get("preset"):
        parts.append(CLI.presets.get(spec["preset"], "Custom"))
    if spec.get("state_dim") is not None:
        parts.append(f"pose state {spec['state_dim']}")
    if spec.get("action_horizon") is not None:
        rate = spec.get("action_hz")
        parts.append(f"{spec.get('executed_actions')} of {spec['action_horizon']} actions "
                     + (f"at {cmd._hz(rate)} Hz" if rate is not None else "(rate not recorded)"))
    if checkpoint.get("rtc_method") and checkpoint.get("status") != "building":
        parts.append(f"RTC {cmd.prefix_rtc(checkpoint)}")
    elif not checkpoint.get("rtc_method") and spec.get("trained_rtc_max_delay"):
        parts.append(f"trained with RTC (up to {spec['trained_rtc_max_delay']} actions)")
    return " · ".join(parts)


def _describe_hy_vla(checkpoint: dict) -> list[str]:
    source = checkpoint.get("source") or {}
    revision = source.get("resolved_revision") or source.get("revision") or "main"
    spec = checkpoint.get("embodiment") or {}
    where = f"hf://{source.get('repo')}@{revision}"
    if source.get("kind") == "upload":
        where = f"local export (upload {source.get('repo')})"
    cameras = ", ".join(f"{c.get('key')} → {c.get('feature')}" for c in spec.get("cameras") or [])
    lines = [
        f"{cmd._title(checkpoint)}  (Hy-VLA)",
        *cmd._id_line(checkpoint),
        f"  robot:    {hy_vla_robot_line(checkpoint)}",
        *([f"  arms:     {', '.join(spec['arms'])}"] if spec.get("arms") else []),
        *([f"  cameras:  {cameras}"] if cameras else []),
        "  actions:  end-effector poses (relative, then absolute, per arm)",
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


def hy_vla_found_lines(found: dict) -> list[str]:
    """What Detect read from a Hy-VLA export: its robot and its RTC."""
    detected = found.get("detected") or {}
    trained = (found.get("rtc") or {}).get("trained_max_delay")
    if trained is None:
        trained = detected.get("trained_rtc_max_delay") or 0
    lines = [
        "Robot: " + hy_vla_robot_line({"embodiment": detected}),
        "RTC: " + (f"trained with prefixes up to {trained} actions (default: trained, "
                   f"prefix up to {trained})" if trained
                   else "not recorded in the export (off)"),
    ]
    lines += [f"Note: {warning}" for warning in found.get("warnings") or []]
    return lines


def run_add_hy_vla(*, repo: str, revision=None, name=None, hf_token=None, path=None,
                   rtc=None, rtc_prefix=None, region="auto", wait=True, keep_warm=None,
                   slug=None, region_fallback=None, client_factory=ControlPlaneClient,
                   print_fn=print, sleep=time.sleep, hz=None):
    """Read a Hy-VLA export (a Hub repo or a local folder), pin the resolved commit, and
    deploy it. The export owns its robot (the bimanual xArm 7 preset is detected), cameras,
    arms, widths and statistics; the create names its RTC (default: trained where the export
    trained it, with every prefix row it trained, else off) and, with ``hz``, the rate its
    training data ran at (sent as ``action_hz``: needed where the export records none). A rate
    outside MIN_HZ-MAX_HZ, or other than the one the export records, is refused here, before
    anything is uploaded."""
    if hz is not None:
        try:
            hz = normalize_rate(hz)
        except ValueError:
            raise cmd._invalid(
                f"--hz is the rate the checkpoint's training data ran at, {MIN_HZ}-{MAX_HZ} Hz",
                "pass --hz 20, say") from None
        if not takes_rate(hz):
            raise cmd._invalid(f"Hy-VLA doesn't take --hz {hz:g}", "omit the rate (--hz)")
    region = cmd._check_region(client_factory, NAME, "Hy-VLA", region, print_fn=print_fn)
    if rtc not in (None, "off", "trained"):
        raise cmd._invalid("Hy-VLA runs RTC off or trained", "use --rtc off or --rtc trained")
    if rtc_prefix is not None and rtc == "off":
        raise cmd._invalid("--rtc-prefix goes with trained RTC", "omit --rtc-prefix, or --rtc off")
    folder = cmd._local_source(repo, NAME)
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
    if found.get("source_format") != "hy_vla":
        raise cmd._invalid("the server did not read a Hy-VLA export", "update the SDK and retry")
    recorded = (found.get("detected") or {}).get("action_hz")
    if recorded is None and hz is None:
        raise cmd._invalid(
            "this export records no control rate, and Hy-VLA never assumes one",
            "pass --hz with the rate its training data ran at",
        )
    if recorded is not None and hz is not None and hz != recorded:
        raise cmd._invalid(
            f"this export records {cmd._hz(recorded)} Hz, and --hz {cmd._hz(hz)} contradicts it",
            f"omit --hz (the export's {cmd._hz(recorded)} Hz applies), or pass "
            f"--hz {cmd._hz(recorded)}",
        )
    for line in hy_vla_found_lines(found):
        if hz is not None and line.startswith("Robot: "):
            # Detect reads the export; the rate is the create's declaration.
            spec = {**(found.get("detected") or {}), "action_hz": hz}
            line = f"Robot: {hy_vla_robot_line({'embodiment': spec})} (rate declared)"
        print_fn(line)
    trained = (found.get("rtc") or {}).get("trained_max_delay")
    if trained is None:
        trained = (found.get("detected") or {}).get("trained_rtc_max_delay") or 0
    method = rtc or ("trained" if rtc_prefix is not None else None)
    if method == "trained" and not trained:
        raise cmd._invalid(
            "this export records no prefix training, so it can't run trained RTC",
            "omit --rtc (it runs RTC off)",
        )
    if rtc_prefix is not None and not 1 <= rtc_prefix <= trained:
        raise cmd._invalid(f"the RTC prefix is 1-{trained} actions (what the export was trained "
                       "on)", f"pass --rtc-prefix 1-{trained}")
    source = found.get("request") or {}
    local = {}
    if folder:
        local = {
            "upload_id": cmd._upload_checkpoint(
                client_factory, folder, found, print_fn, base_model=NAME
            ),
            "source_format": "hy_vla", "shown": str(folder.root),
        }
        repo, name = None, name or folder.label
    else:
        repo, revision = source["repo"], source["revision"]
    return cmd.run_add(
        repo=repo, model=NAME, revision=revision, name=name, hf_token=token,
        # The export owns the robot; the server detects its preset. A declared rate goes as
        # the server takes it (a whole one an integer, as the deployment records it).
        embodiment={} if hz is None else {"action_hz": hz},
        region=region, wait=wait,
        client_factory=client_factory, print_fn=print_fn, sleep=sleep,
        keep_warm=keep_warm, slug=slug, source_path=source.get("source_path", ""),
        rtc_method=method, rtc_max_delay=rtc_prefix, region_fallback=region_fallback, **local,
    )


def _hy_vla_runner_model(embodiment: Any, checkpoint_id: str, row: dict) -> str:
    """A Hy-VLA deployment `dreamscale run <robot>` drives: robots whose kinematics turn its
    pose rows into joint targets, the bimanual xArm 7 preset on `dreamscale run xarm7`
    (hardware.hy_vla_xarm7); every other robot runs it from Python."""
    spec = row.get("embodiment") or {}
    if spec.get("preset") == "bimanual_xarm7" and embodiment.name == "xarm7":
        return NAME
    built_for = (CLI.presets.get(spec.get("preset") or "", "a custom robot")
                 if spec.get("preset") != "custom" else "a custom robot")
    fix = (
        f"run it with `dreamscale run xarm7 --deployment {checkpoint_id}`"
        if spec.get("preset") == "bimanual_xarm7"
        else f'drive it from Python: dreamscale.connect("{NAME}", '
        f'deployment="{checkpoint_id}"), then policy.next_action(...) with a 20-value pose '
        "state; turn its pose rows into joint targets on your robot"
    )
    raise cmd._invalid(
        f"{checkpoint_id} is a Hy-VLA deployment for {built_for}, which `dreamscale run "
        f"{embodiment.name}` doesn't drive",
        fix,
        cause=f"`dreamscale run {embodiment.name}` drives {embodiment.label} only",
    )



def _create_hy_vla(*, repo, given, preset, camera, hz, path, executed, steps, joint_unit, rtc,
                   rtc_prefix, revision, name, hf_token, region, wait, keep_warm, slug,
                   region_fallback=None) -> None:
    from dreamscale.checkpoints_cmd import KEEP_WARM_VALUES, parse_region

    unsupported = [key for key, value in given.items()
                   if value is not None and key not in ("path", "rtc")]
    unsupported += [key for key, value in (
        ("preset", preset), ("camera", camera or None), ("steps", steps),
        ("joint_unit", joint_unit),
    ) if value is not None]
    if unsupported:
        raise cli.typer.BadParameter(
            f"{cli._flag(unsupported[0])} doesn't apply to Hy-VLA: the export records its robot, "
            "cameras and statistics. Pass only --rtc, --rtc-prefix and --hz (the rate its "
            "training data ran at, where the export records none)."
        )
    if keep_warm is not None and keep_warm not in KEEP_WARM_VALUES:
        raise cli.typer.BadParameter(
            f"use one of {', '.join(KEEP_WARM_VALUES)}", param_hint="'--keep-warm'"
        )
    try:
        region = parse_region(region)
        if rtc is not None and rtc.strip().lower() not in ("off", "trained"):
            raise ValueError(f"--rtc is off or trained for Hy-VLA, got {rtc!r}")
    except ValueError as error:
        raise cli.typer.BadParameter(str(error)) from None
    result: dict = {}
    cli._run(
        lambda **kwargs: result.update(run_add_hy_vla(**kwargs)),
        repo=repo, revision=revision, name=name, hf_token=hf_token, path=path,
        rtc=None if rtc is None else rtc.strip().lower(), rtc_prefix=rtc_prefix,
        region=region, wait=wait, keep_warm=keep_warm, slug=slug, region_fallback=region_fallback,
        hz=hz,
    )
    if result.get("status") == "failed":
        raise cli.typer.Exit(code=1)


def runner(embodiment, checkpoint_id, row, model):
    return _hy_vla_runner_model(embodiment, checkpoint_id, row)


def set_rtc(row, checkpoint_id, method, max_delay, client_factory, print_fn) -> dict:
    return cmd._set_prefix_rtc(row, checkpoint_id, method, max_delay, client_factory, print_fn,
                               label="Hy-VLA", untrained_fix="it runs RTC off")


EXPORTED = ExportedBase(
    "Hy-VLA",
    "dreamscale.policy.hy_vla_deployment:HyVlaSessionDeployment",
    "dreamscale.policy.hy_vla_deployment:runtime_contract",
    # Pose rows from a 20-value pose state: a joint state is never the export's.
    state="refuse",
)
BASE = DeployBase(
    family="hy_vla", name=NAME, label="Hy-VLA", cli=CLI, listed_as="hy-vla",
    robot_line=hy_vla_robot_line, describe=_describe_hy_vla, shows_rtc=True, runner=runner,
    set_rtc=set_rtc, detects_as_base=True, found_lines=hy_vla_found_lines,
    create=_create_hy_vla, exported=EXPORTED,
    # The bimanual xArm 7 preset's end-effector pose chunks, turned into joint targets.
    robots=("xarm7",), robot_adapters={"xarm7": "dreamscale.hardware.hy_vla_xarm7"},
)
