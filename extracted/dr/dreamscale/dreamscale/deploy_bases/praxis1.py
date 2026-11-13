"""Praxis-1 deployments in the SDK: its base as the CLI and the policy runtime know it
(``dreamscale.deploy_bases`` loads it by the family manifest's id).

Scaffolded by scripts/new_model.py --contract-from-checkpoint, unlisted (``listed_as=None``)
until GA. No robot is fixed: each checkpoint's export declares its cameras, widths, rate and
chunk, and a create names the custom preset. So its create (the CLI's `deployments create`
options, then Detect the export and create with what the robot names), its robot line (from the
checkpoint row's embodiment) and Detect's lines are its own: deploy_bases/internw0.py's
_create_internw0, internw0_robot_line and hy_vla.py's hy_vla_found_lines are working ones. Its
sessions' contract is dreamscale.policy.praxis1_deployment.

RTC (experimental) is the export's: trained where its training ran with committed prefixes (and
its build passed the RTC checks), else off; `deployments rtc` turns it off or caps the prefix in
whole 4-row action tokens.
"""

from __future__ import annotations

import time

from dreamscale_transport.praxis1_deploy import RTC_TOKEN_ROWS

from dreamscale.control import ControlPlaneClient
from dreamscale.deploy_bases import Base, DeployBase, ExportedBase, cli, cmd

NAME = "praxis-1-base"
SOURCE_FORMAT = "praxis1"
ROLES = ("base", "left_wrist", "right_wrist")
# The custom preset a create names, and its build's steps, as `deployments create --wait` shows
# them.
CLI = Base({"custom": "Custom"}, (
    ("Finding the export", ("building", "resolving", "checking")),
    ("Downloading", ("downloading",)),
    ("Saving", ("validating", "sealing", "built")),
    ("Testing on a server", ("qualifying", "ready", "failed")),
), None)


def praxis1_robot_line(checkpoint: dict) -> str:
    """`Praxis-1 · 14 joints · 3 cameras · 21 of 24 actions at 15 Hz`, from the checkpoint
    row's embodiment (what its export declared; before its build, only what its create
    sent)."""
    spec = checkpoint.get("embodiment") or {}
    parts = ["Praxis-1"]
    if spec.get("action_dim") is not None:
        parts.append(f"{spec['action_dim']} joints" if spec.get("action_space") ==
                     "absolute_joint_position" else f"{spec['action_dim']} values")
    if spec.get("cameras"):
        count = len(spec["cameras"])
        parts.append(f"{count} camera{'s' if count != 1 else ''}")
    if spec.get("action_horizon") is not None:
        parts.append(f"{spec.get('executed_actions')} of {spec['action_horizon']} actions at "
                     f"{cmd._hz(spec.get('action_hz'))} Hz")
    return " · ".join(parts)


def praxis1_found_lines(found: dict) -> list[str]:
    """What Detect read from a Praxis-1 export: its robot and its cameras."""
    detected = found.get("detected") or {}
    lines = ["Robot: " + praxis1_robot_line({"embodiment": detected})]
    cameras = detected.get("cameras") or []
    if cameras:
        lines.append("Cameras: " + ", ".join(f"{c.get('key')} ({c.get('role')})"
                                             for c in cameras))
    rtc = found.get("rtc") or {}
    trained = rtc.get("trained_max_delay") if rtc.get("method") == "trained" else None
    lines.append(f"RTC: trained, experimental (prefix up to {trained} actions)" if trained
                 else "RTC: off")
    lines += [f"Note: {warning}" for warning in found.get("warnings") or []]
    return lines


def praxis1_rtc(checkpoint: dict) -> str:
    """`trained, experimental (prefix up to 8 of 20 actions)` or `off`."""
    return cmd.prefix_rtc(checkpoint, note="experimental")


def set_rtc(row, checkpoint_id, method, max_delay, client_factory, print_fn) -> dict:
    """`deployments rtc`: off, or trained with a prefix cap in whole 4-row action tokens within
    what the checkpoint trained (the server checks it too)."""
    trained = row.get("trained_rtc_max_delay") or 0
    if method == "trained" and max_delay is not None and trained and (
        not RTC_TOKEN_ROWS <= max_delay <= trained or max_delay % RTC_TOKEN_ROWS
    ):
        caps = ", ".join(str(rows) for rows in range(RTC_TOKEN_ROWS, trained + 1,
                                                     RTC_TOKEN_ROWS))
        raise cmd._invalid(
            f"the prefix cap is whole action tokens of {RTC_TOKEN_ROWS} actions, at most "
            f"{trained} (what the checkpoint was trained on)",
            f"pass --max-delay {caps}, or omit it for {trained}",
        )
    return cmd._set_prefix_rtc(row, checkpoint_id, method, max_delay, client_factory, print_fn,
                               label="Praxis-1", describe=praxis1_rtc,
                               untrained_fix="it runs RTC off; train with `dreamscale train "
                               "--rtc` to use it")


def parse_role_cameras(values) -> list[dict] | None:
    """``--camera KEY=ROLE`` (repeatable): the robot's camera key for each role the export
    trained (base, left_wrist, right_wrist), in the export's order."""
    if not values:
        return None
    out = []
    for value in values:
        key, sep, role = str(value).partition("=")
        if not sep or not key or role not in ROLES:
            raise ValueError(f"--camera takes KEY=ROLE, the role one of {', '.join(ROLES)}")
        out.append({"key": key, "role": role})
    return out


def run_add_praxis1(*, repo: str, revision=None, name=None, hf_token=None, path=None,
                    executed=None, joint_unit=None, cameras=None, region="auto", wait=True,
                    keep_warm=None, slug=None, region_fallback=None, rtc_method=None,
                    client_factory=ControlPlaneClient, print_fn=print, sleep=time.sleep):
    """Read a Praxis-1 fine-tune's export (a Hub repo or a local folder), pin the resolved
    commit, and deploy it. The export owns its robot (cameras by role, widths, joint names,
    grippers, normalization); a create may name the robot's camera keys, run fewer actions
    per chunk and name its joint unit. RTC is the export's unless ``rtc_method`` says "off".
    (A managed training run deploys from its own page.)"""
    region = cmd._check_region(client_factory, NAME, "Praxis-1", region, print_fn=print_fn)
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
    if found.get("source_format") != SOURCE_FORMAT:
        raise cmd._invalid("the server did not read a Praxis-1 export",
                           "update the SDK and retry")
    embodiment: dict = {"preset": "custom"}
    if executed is not None:
        embodiment["executed_actions"] = executed
    if joint_unit is not None:
        embodiment["joint_unit"] = joint_unit
    if cameras:
        embodiment["cameras"] = cameras
    source = found.get("request") or {}
    local = {}
    if folder:
        local = {
            "upload_id": cmd._upload_checkpoint(
                client_factory, folder, found, print_fn, base_model=NAME
            ),
            "source_format": SOURCE_FORMAT, "shown": str(folder.root),
        }
        repo, name = None, name or folder.label
    else:
        repo, revision = source["repo"], source["revision"]
    return cmd.run_add(
        repo=repo, model=NAME, revision=revision, name=name, hf_token=token,
        embodiment=embodiment, region=region, wait=wait,
        client_factory=client_factory, print_fn=print_fn, sleep=sleep,
        keep_warm=keep_warm, slug=slug, source_path=source.get("source_path", ""),
        # None: trained where the export trained with committed prefixes, else off.
        rtc_method=rtc_method, region_fallback=region_fallback, **local,
    )


def _create_praxis1(
    *, repo, given, preset, camera, hz, path, executed, steps, joint_unit, rtc, rtc_prefix,
    revision, name, hf_token, region, wait, keep_warm, slug, region_fallback=None,
) -> None:
    """`deployments create --base praxis-1-base`: the export owns the robot and its RTC; the CLI
    passes only --path, --executed, --joint-unit, --camera KEY=ROLE and --rtc off."""
    unsupported = {key: value for key, value in given.items()
                   if key not in ("path", "executed")}
    if preset is not None or hz is not None or steps is not None or rtc_prefix is not None or (
        rtc not in (None, "off")
    ) or any(value is not None for value in unsupported.values()):
        raise cli.typer.BadParameter(
            "Praxis-1 reads its robot from the export; pass only --path, --executed, "
            "--joint-unit and --camera KEY=ROLE."
        )
    try:
        cameras = parse_role_cameras(camera)
    except ValueError as exc:
        raise cli.typer.BadParameter(str(exc), param_hint="'--camera'") from exc
    result = {}
    cli._run(
        lambda **kwargs: result.update(run_add_praxis1(**kwargs)),
        repo=repo, revision=revision, name=name, hf_token=hf_token, path=path,
        executed=executed, joint_unit=joint_unit, cameras=cameras,
        region=region or cmd.AUTO_REGION, wait=wait, keep_warm=keep_warm, slug=slug,
        region_fallback=region_fallback, rtc_method=rtc,
    )
    if result.get("status") == "failed":
        raise cli.typer.Exit(code=1)


EXPORTED = ExportedBase(
    "Praxis-1",
    "dreamscale.policy.praxis1_deployment:Praxis1SessionDeployment",
    "dreamscale.policy.praxis1_deployment:runtime_contract",
)
BASE = DeployBase(
    family="praxis1", name=NAME, label="Praxis-1", cli=CLI,
    exported=EXPORTED,
    robot_line=praxis1_robot_line, describe_rtc=praxis1_rtc, set_rtc=set_rtc,
    create=_create_praxis1,
    detects_as_base=True, found_lines=praxis1_found_lines,
)
