"""InternW0-Δ deployments in the SDK (DSL-284): an upstream training run's export, RTC off;
`dreamscale run yam` drives a run on the Bimanual YAM wire."""

from __future__ import annotations

import time
from typing import Any

from dreamscale.control import ControlPlaneClient
from dreamscale.deploy_bases import Base, DeployBase, ExportedBase, cli, cmd

NAME = "internw0-delta-base"
CLI = Base({"custom": "Custom"}, (
    ("Finding the run", ("building", "resolving", "checking")),
    ("Downloading", ("downloading",)),
    ("Checking weights", ("validating", "sealing", "built")),
    ("Testing on a server", ("qualifying", "ready", "failed")),
), None)


def internw0_robot_line(checkpoint: dict) -> str:
    # Before its build reads the run, a row holds only what its create sent.
    spec = checkpoint.get("embodiment") or {}
    parts = ["InternW0-Δ"]
    if spec.get("state_dim") is not None:
        parts.append(cmd._widths(spec))
    rate = f"at {cmd._hz(spec.get('action_hz'))} Hz" if spec.get("action_hz") else ""
    if spec.get("action_horizon") is not None:
        rate = f"{spec.get('executed_actions')} of {spec['action_horizon']} actions {rate}"
    if rate:
        parts.append(rate.strip())
    parts.append(spec.get("action_space") or "model_defined")
    return " · ".join(parts)


def run_add_internw0(*, repo: str, revision=None, name=None, hf_token=None, path=None,
                     hz=None, executed=None, joint_unit=None, cameras=None, region="auto",
                     wait=True, keep_warm=None, slug=None, region_fallback=None,
                     client_factory=ControlPlaneClient, print_fn=print, sleep=time.sleep):
    """Inspect an InternW0-Δ training run, pin the resolved commit, and deploy it. The run
    owns its cameras, widths and canvas; the robot names its rate (when the run records
    none), how many actions it runs per request, (``joint_unit``) that its actions are joint
    positions, and (``cameras``, ``{key, feature}`` in the run's order) the names its cameras
    send under, where they differ from the run's."""
    region = cmd._check_region(client_factory, NAME, "InternW0-Δ", region, print_fn=print_fn)
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
    if found.get("source_format") != "internw0_run":
        raise cmd._invalid("the server did not read an InternW0 training run",
                       "update the SDK and retry")
    if "action_hz" in (found.get("missing") or ()) and hz is None:
        raise cmd._invalid("the run records no action rate",
                       "pass --hz with the rate your robot runs at")
    embodiment: dict = {"preset": "custom"}
    if hz is not None:
        embodiment["action_hz"] = float(hz)
    if executed is not None:
        embodiment["executed_actions"] = executed
    if joint_unit is not None:
        embodiment.update(action_space="absolute_joint_position", joint_unit=joint_unit)
    if cameras:
        embodiment["cameras"] = cameras
    source = found.get("request") or {}
    local = {}
    if folder:
        local = {
            "upload_id": cmd._upload_checkpoint(
                client_factory, folder, found, print_fn, base_model=NAME
            ),
            "source_format": "internw0_run", "shown": str(folder.root),
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


def _internw0_runner_model(embodiment: Any, checkpoint_id: str, row: dict) -> str:
    """An InternW0-Δ deployment `dreamscale run yam` drives: a run on the Bimanual YAM wire
    (cameras observation.images.top, left, right; 14 joint positions in radians). Any other
    runs from Python."""
    spec = row.get("embodiment") or {}
    cameras = tuple(c.get("key") for c in spec.get("cameras") or [])
    width = len(embodiment.arms) * embodiment.arm_size
    joints = (
        spec.get("state_dim") == spec.get("action_dim") == width
        and spec.get("action_space") == "absolute_joint_position"
        and spec.get("joint_unit") in ("rad", "radians")
    )
    wire = tuple(embodiment.recording_keys)
    if cmd.RUNNER_PRESETS.get(embodiment.name) == "bimanual_yam" and joints and cameras == wire:
        return NAME
    fix = (
        f'drive it from Python: dreamscale.connect("{NAME}", '
        f'deployment="{checkpoint_id}"), then policy.next_action(...)'
    )
    if cmd.RUNNER_PRESETS.get(embodiment.name) != "bimanual_yam":
        raise cmd._invalid(
            f"{checkpoint_id} is an InternW0-Δ deployment; `dreamscale run` drives those on "
            "Bimanual YAM only", fix,
        )
    if joints and len(cameras) == len(wire):
        # The run's cameras under other names: name them as the YAM sends them.
        features = [c.get("feature") for c in spec.get("cameras") or []]
        mapping = " ".join(
            f"--camera {key}={feature}" for key, feature in zip(wire, features, strict=True)
        )
        raise cmd._invalid(
            f"{checkpoint_id}'s cameras are named {', '.join(cameras)}; the YAM sends "
            f"{', '.join(wire)}",
            f"deploy the run again with {mapping} (in the run's camera order)",
            cause="an InternW0-Δ deployment's camera names are the robot's, set when it's created",
        )
    raise cmd._invalid(
        f"{checkpoint_id} is an InternW0-Δ deployment for a custom robot, not {embodiment.label}",
        fix,
        cause=(
            f"`dreamscale run {embodiment.name}` drives runs with cameras "
            f"{', '.join(wire)} (in that order) and {width} joint positions in radians"
        ),
    )



def _create_internw0(*, repo, given, preset, camera, hz, path, executed, steps, joint_unit, rtc,
                     rtc_prefix, revision, name, hf_token, region, wait, keep_warm, slug,
                     region_fallback=None) -> None:
    unsupported = {key: value for key, value in given.items()
                   if key not in ("path", "executed")}
    if preset is not None or rtc_prefix is not None or steps is not None or any(
        value is not None for value in unsupported.values()
    ):
        raise cli.typer.BadParameter(
            "InternW0-Δ reads its cameras, widths and canvas from the run; pass only "
            "--hz, --executed, --joint-unit and --camera."
        )
    from dreamscale.checkpoints_cmd import parse_feature_cameras

    try:
        cameras = parse_feature_cameras(camera)
    except ValueError as exc:
        raise cli.typer.BadParameter(str(exc), param_hint="'--camera'") from exc
    result = {}
    cli._run(
        lambda **kwargs: result.update(run_add_internw0(**kwargs)),
        repo=repo, revision=revision, name=name, hf_token=hf_token,
        path=path, hz=hz, executed=executed, joint_unit=joint_unit, cameras=cameras,
        region=region or cmd.AUTO_REGION, wait=wait, keep_warm=keep_warm, slug=slug,
        region_fallback=region_fallback,
    )
    if result.get("status") == "failed":
        raise cli.typer.Exit(code=1)


def runner(embodiment, checkpoint_id, row, model):
    return _internw0_runner_model(embodiment, checkpoint_id, row)


EXPORTED = ExportedBase(
    "InternW0",
    "dreamscale.policy.internw0_deployment:InternW0SessionDeployment",
    "dreamscale.policy.internw0_deployment:runtime_contract",
    state="convert",
)
BASE = DeployBase(
    family="internw0", name=NAME, label="InternW0-Δ", cli=CLI, aliases=("internw0",),
    # Rows that carry only the model they serve are InternW0-Δ's.
    claims_model=True, robot_line=internw0_robot_line, runner=runner, detects_as_base=True,
    # The robot waits for each chunk (upstream's sync loop).
    waits_for_each_chunk=True,
    create=_create_internw0, exported=EXPORTED,
)
