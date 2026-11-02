"""Cosmos 3 Nano Policy deployments in the SDK (DSL-350): a policy export of NVIDIA's DROID recipe
or one Dreamscale trained, RTC off. No robot is fixed here: Detect reads each export's robot (the
DROID preset, or its ``dreamscale.json``), and a create names the custom preset with, at most,
the robot's camera names and how many actions it runs per chunk. `dreamscale run franka` drives
a DROID-preset deployment; any other runs from Python. Unlisted until GA."""

from __future__ import annotations

import time
from typing import Any

from dreamscale.control import ControlPlaneClient
from dreamscale.deploy_bases import Base, DeployBase, ExportedBase, cli, cmd

NAME = "cosmos3-nano-policy"
LABEL = "Cosmos 3 Nano Policy"
FORMAT = "cosmos3_policy"
# The Franka's wire cameras, as a DROID-preset deployment names them (canvas order).
DROID_CAMERAS = ("wrist", "exterior_1", "exterior_2")
# The custom preset a create names (and the DROID preset a DROID-recipe export seals, as
# `deployments list` labels it), and its build's steps, as `deployments create --wait` shows them.
CLI = Base({"custom": "Custom", "droid": "Franka (DROID)"}, (
    ("Finding the export", ("building", "resolving", "checking")),
    ("Downloading", ("downloading",)),
    ("Checking weights", ("validating", "sealing", "built")),
    ("Testing on a server", ("qualifying", "ready", "failed")),
), None)


def cosmos3_robot_line(checkpoint: dict) -> str:
    """`Cosmos 3 Nano Policy · Franka (DROID) · 32 of 32 actions at 15 Hz`, from the checkpoint
    row's embodiment (what its export declared; before its build, what the create sent)."""
    spec = checkpoint.get("embodiment") or {}
    parts = [LABEL]
    if spec.get("preset") == "droid":
        parts.append("Franka (DROID)")
    elif spec.get("action_dim") is not None:
        cameras = len(spec.get("cameras") or ())
        state = spec.get("state_dim") or 0
        parts.append(f"{cameras} camera{'s' if cameras != 1 else ''}, "
                     f"{spec['action_dim']} values" + ("" if state else ", no state"))
    if spec.get("action_horizon") is not None:
        rate = f" at {spec['action_hz']} Hz" if spec.get("action_hz") else ""
        parts.append(f"{spec.get('executed_actions')} of {spec['action_horizon']} actions{rate}")
    if spec.get("action_space"):
        parts.append(spec["action_space"])
    return " · ".join(parts)


def cosmos3_found_lines(found: dict) -> list[str]:
    """What Detect read from a Cosmos 3 export: its contract, robot and sampler; RTC off."""
    detected = found.get("detected") or {}
    contract = detected.get("contract")
    source = ("NVIDIA's DROID recipe (the Franka preset)" if contract == "droid_preset"
              else "a Dreamscale training export (its dreamscale.json)"
              if contract == "dreamscale_training" else "unknown")
    lines = [f"Contract: {source}", "Robot: " + cosmos3_robot_line({"embodiment": detected})]
    cameras = detected.get("cameras") or []
    if cameras:
        lines.append("Cameras: " + ", ".join(
            f"{c.get('key')} ({c.get('feature')})" if c.get("key") != c.get("feature")
            else str(c.get("key")) for c in cameras))
    canvas = detected.get("canvas") or {}
    if canvas:
        lines.append(f"Frames: each camera letterboxed to {canvas.get('slot_width')}x"
                     f"{canvas.get('slot_height')}; send at least that size (smaller frames, "
                     "upscaled, change its actions)")
    sampler = detected.get("sampler") or {}
    if sampler:
        lines.append(f"Sampler: {sampler.get('steps')} steps, guidance {sampler.get('guidance')}")
    lines.append("RTC: off (Cosmos 3 has none)")
    lines += [f"Note: {warning}" for warning in found.get("warnings") or []]
    return lines


def run_add_cosmos3(*, repo: str, revision=None, name=None, hf_token=None, path=None,
                    executed=None, cameras=None, region="auto", wait=True, keep_warm=None,
                    slug=None, region_fallback=None, client_factory=ControlPlaneClient,
                    print_fn=print, sleep=time.sleep):
    """Read a Cosmos 3 policy export (a Hub repo or a local folder), pin the resolved commit, and
    deploy it. The export owns its robot; the robot names how many actions it runs per chunk
    (``executed``) and (``cameras``, ``{key, feature}`` in the checkpoint's order) the names its
    cameras send under."""
    region = cmd._check_region(client_factory, NAME, LABEL, region, print_fn=print_fn)
    folder = cmd._local_source(repo, NAME)
    if folder and (revision is not None or hf_token is not None):
        raise cmd._invalid("a local folder has no Hub revision or token",
                           "omit --revision and --hf-token")
    token = cmd.hugging_face.token(hf_token) if folder is None else None
    if folder:
        found = cmd._inspect_local(client_factory, folder, print_fn, path=path, base=NAME)
    else:
        _, found = cmd._inspect_with_status(
            client_factory, repo, revision, token, print_fn, base=NAME, path=path,
        )
    if found.get("source_format") != FORMAT:
        raise cmd._invalid("the server did not read a Cosmos 3 policy export",
                           "update the SDK and retry")
    for line in cosmos3_found_lines(found):
        print_fn(line)
    embodiment: dict = {"preset": "custom"}
    if executed is not None:
        embodiment["executed_actions"] = executed
    if cameras:
        embodiment["cameras"] = cameras
    source = found.get("request") or {}
    local = {}
    if folder:
        local = {
            "upload_id": cmd._upload_checkpoint(client_factory, folder, found, print_fn,
                                                base_model=NAME),
            "source_format": FORMAT, "shown": str(folder.root),
        }
        repo, name = None, name or folder.label
    else:
        repo, revision = source["repo"], source["revision"]
    return cmd.run_add(
        repo=repo, model=NAME, revision=revision, name=name, hf_token=token,
        embodiment=embodiment, region=region, wait=wait,
        client_factory=client_factory, print_fn=print_fn, sleep=sleep,
        keep_warm=keep_warm, slug=slug, source_path=source.get("source_path", ""),
        rtc_method="off", region_fallback=region_fallback, **local,
    )


def _create_cosmos3(
    *, repo, given, preset, camera, hz, path, executed, steps, joint_unit, rtc, rtc_prefix,
    revision, name, hf_token, region, wait, keep_warm, slug, region_fallback=None,
) -> None:
    """`deployments create --base cosmos3-nano-policy`: the export's robot, the robot's camera
    names and executed actions; nothing else may be set."""
    unsupported = {key: value for key, value in given.items() if key not in ("path", "executed")}
    if (preset not in (None, "custom") or hz is not None or steps is not None
            or joint_unit is not None or rtc_prefix is not None or rtc not in (None, "off")
            or any(value is not None for value in unsupported.values())):
        raise cli.typer.BadParameter(
            f"{LABEL} reads its robot, rate, chunk and sampler from the export, and runs RTC "
            "off; pass only --executed and --camera."
        )
    from dreamscale.checkpoints_cmd import parse_feature_cameras

    try:
        cameras = parse_feature_cameras(camera)
    except ValueError as exc:
        raise cli.typer.BadParameter(str(exc), param_hint="'--camera'") from exc
    result = {}
    cli._run(
        lambda **kwargs: result.update(run_add_cosmos3(**kwargs)),
        repo=repo, revision=revision, name=name, hf_token=hf_token, path=path,
        executed=executed, cameras=cameras, region=region or cmd.AUTO_REGION, wait=wait,
        keep_warm=keep_warm, slug=slug, region_fallback=region_fallback,
    )
    if result.get("status") == "failed":
        raise cli.typer.Exit(code=1)


def runner(embodiment: Any, checkpoint_id: str, row: dict, model: str) -> str:
    """The deployment `dreamscale run franka` drives: a DROID-preset one whose cameras keep the
    Franka's names. Any other runs from Python."""
    spec = row.get("embodiment") or {}
    keys = tuple(c.get("key") for c in spec.get("cameras") or [])
    fix = (f'drive it from Python: dreamscale.connect("{NAME}", deployment="{checkpoint_id}"), '
           "then policy.next_action(...)")
    if getattr(embodiment, "name", None) != "franka" or spec.get("preset") != "droid":
        raise cmd._invalid(
            f"{checkpoint_id} is a {LABEL} deployment; `dreamscale run` drives those on a "
            "Franka with the DROID preset only", fix)
    if keys != DROID_CAMERAS:
        raise cmd._invalid(
            f"{checkpoint_id}'s cameras are named {', '.join(map(str, keys))}; the Franka "
            f"sends {', '.join(DROID_CAMERAS)}",
            "deploy it again without --camera (the DROID preset names them as the Franka "
            "does)")
    return NAME


EXPORTED = ExportedBase(
    LABEL,
    "dreamscale.policy.cosmos3_deployment:Cosmos3SessionDeployment",
    "dreamscale.policy.cosmos3_deployment:runtime_contract",
)
BASE = DeployBase(
    family="cosmos3", name=NAME, label=LABEL, cli=CLI, aliases=("cosmos3-nano",),
    exported=EXPORTED,
    robot_line=cosmos3_robot_line,
    create=_create_cosmos3, runner=runner,
    detects_as_base=True, found_lines=cosmos3_found_lines,
)
