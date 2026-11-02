"""π0.5 deployments in the SDK: openpi or LeRobot fine-tunes on a preset robot or the robot's
own cameras and shapes, RTC off, test-time or trained. The default base: `--base` defaults to it,
and Detect reads a repo as π0.5 first (an older control plane's answer, or a repo π0.5 can't
read, as Isaac 0.5's legacy path)."""

from __future__ import annotations

import asyncio
import time
from collections.abc import Callable
from typing import Any

from dreamscale_transport.pi05_deploy import (
    MAX_CAMERAS,
    MAX_HORIZON,
    MAX_HZ,
    MAX_TRAINED_RTC_DELAY,
    PI05_DEPLOY_SLOTS,
)

from dreamscale import errors
from dreamscale.control import ControlPlaneClient
from dreamscale.deploy_bases import Base, DeployBase, SessionBase, cli, cmd
from dreamscale.model_names import internal_model
from dreamscale.policy.deployment import joint_actions, non_joint_run_error
from dreamscale.policy.pi05_deployment import (
    PI05_PUBLIC_BASE,
    PRESET_LAYOUTS,
    PREVIEW_CONTRACT,
    robot_preset,
)

NAME = PI05_PUBLIC_BASE
# Its intake, in order: resolve the commit, check the checkpoint, download, convert (LeRobot
# weights; openpi is copied as is), seal, run it on a GPU, compare it with a reference.
BUILD_STEPS = (
    ("Finding the repo", ("building", "resolving")),
    ("Checking the checkpoint", ("checking",)),
    ("Downloading", ("downloading",)),
    ("Converting", ("converting",)),
    ("Saving", ("sealing", "built")),
    ("Testing on a server", ("qualifying",)),
    # LeRobot checkpoints only: the converted deployment against LeRobot's own policy.
    ("Validating", ("comparing", "ready", "failed")),
)
CLI = Base(
    {**{preset: layout.label for preset, layout in PRESET_LAYOUTS.items()}, "custom": "Custom"},
    BUILD_STEPS,
    None,
)


def row_steps(checkpoint: dict, steps: tuple) -> tuple:
    """openpi checkpoints run on openpi's own code, so they skip the LeRobot validation (their
    GPU test is the last step)."""
    if checkpoint.get("source_format") == "openpi":
        *head, (label, phases), _validating = steps
        return (*head, (label, (*phases, "ready", "failed")))
    return steps


# --preset blank: a π0.5 robot described entirely by flags (the API's "custom").
PI05_PRESET_CHOICES = (*PRESET_LAYOUTS, "blank")


def _pi05_rtc(checkpoint: dict, *, note: bool = True) -> str:
    return cmd.rtc_line(
        checkpoint.get("rtc_method"),
        checkpoint.get("trained_rtc_max_delay") or checkpoint.get("rtc_max_prefix_steps"),
        note=note,
    )


def pi05_robot_line(checkpoint: dict) -> str:
    """One line for a π0.5 deployment's robot: preset, state width, geometry, cameras, RTC."""
    embodiment = checkpoint.get("embodiment") or {}
    if not embodiment:
        return "—"
    label = CLI.presets.get(embodiment.get("preset"), "Custom")
    executed, horizon = embodiment.get("executed_actions"), embodiment.get("action_horizon")
    geometry = f"{executed} of {horizon}" if horizon else f"{executed}"
    return (
        f"{label} · {cmd._widths(embodiment)} · {geometry} actions at "
        f"{cmd._hz(embodiment.get('action_hz'))} Hz · cameras "
        f"{cmd._cameras_line(embodiment.get('cameras') or [])} · RTC {_pi05_rtc(checkpoint)}"
    )


def _describe_pi05(checkpoint: dict) -> list[str]:
    source = checkpoint.get("source") or {}
    revision = source.get("resolved_revision") or source.get("revision") or "main"
    embodiment = checkpoint.get("embodiment") or {}
    label = CLI.presets.get(embodiment.get("preset"), "Custom")
    executed, horizon = embodiment.get("executed_actions"), embodiment.get("action_horizon")
    geometry = f"executes {executed} of {horizon} actions" if horizon else (
        f"executes {executed} actions"
    )
    geometry += f" at {cmd._hz(embodiment.get('action_hz'))} Hz"
    if embodiment.get("token_length"):
        geometry += f" · prompt {embodiment['token_length']} tokens"
    if embodiment.get("state_in_prompt") is not None:
        geometry += ", state in prompt" if embodiment["state_in_prompt"] else ", no state"
    path = source.get("path")
    fmt = checkpoint.get("source_format")
    where = f"hf://{source.get('repo')}@{revision}" + (f" · {path}" if path else "")
    training = checkpoint.get("training") or {}
    if training.get("run_id"):
        step = training.get("step")
        where = f"training run {training['run_id']}" + (
            f" · step {step:,}" if isinstance(step, int) else ""
        )
    elif source.get("kind") == "upload":
        where = f"local folder (upload {source.get('repo')})" + (f" · {path}" if path else "")
    runs = cmd.non_joint_line(embodiment.get("state_dim"), embodiment.get("action_dim"))
    lines = [
        f"{cmd._title(checkpoint)}  (π0.5)",
        *cmd._id_line(checkpoint),
        f"  robot:    {label} · state {embodiment.get('state_dim')} → "
        f"{embodiment.get('action_dim')} actions",
        f"  cameras:  {cmd._cameras_line(embodiment.get('cameras') or [])}",
        f"  geometry: {geometry}",
        f"  rtc:      {_pi05_rtc(checkpoint)}",
        f"  region:   {cmd.region_line(checkpoint)}",
        *([f"  runs:     {runs}"] if runs else []),
        f"  status:   {checkpoint['status']}",
        f"  source:   {where}" + (f" ({fmt})" if fmt else ""),
        f"  size:     {cmd._gb(checkpoint.get('size_bytes'))}",
    ]
    validation = checkpoint.get("validation") or {}
    if validation.get("mean_std") is not None:
        lines.append(
            f"  validated: matches LeRobot · {validation['mean_std']:.3f} std average "
            f"difference (limit {validation.get('limit_std', 0.05):g})"
        )
    if cmd.autoscaling(checkpoint):
        lines.append(f"  robots:   {cmd.robots_line(checkpoint)} (scales automatically)")
    if checkpoint.get("keep_warm") is not None:
        lines.append(f"  warm:     {cmd.keep_warm_line(checkpoint)}")
    error = checkpoint.get("error")
    if error:
        lines += [f"  error:    {error['code']}: {error['message']}", f"  fix:      {error['fix']}"]
    return lines


def is_pi05_inspect(found: dict) -> bool:
    """A π0.5 inspect answer (an older control plane ignores `model` and reads Isaac)."""
    return found.get("format") in ("openpi", "lerobot") or "checkpoints" in found


def pi05_inspect_lines(found: dict) -> list[str]:
    """What a π0.5 repo holds: format, checkpoints, detected fields with their sources, RTC."""
    source = found.get("source") or {}
    revision = source.get("resolved_revision") or source.get("revision")
    where = f"hf://{source.get('repo')}" + (f"@{revision}" if revision else "") if source else ""
    if "upload" in found:  # a local folder (named by the caller)
        where = ""
    lines = [f"π0.5 checkpoint ({found.get('format') or 'unknown format'})"
             + (f" in {where}" if where else "")]
    checkpoints = cmd._checkpoint_paths(found)
    latest = cmd.latest_checkpoint(found)
    if checkpoints:
        lines.append("Checkpoints:")
        for checkpoint in checkpoints:
            notes = []
            if checkpoint.get("step") is not None:
                notes.append(f"step {checkpoint['step']}")
            if checkpoint.get("asset_ids"):
                notes.append("stats " + ", ".join(map(str, checkpoint["asset_ids"])))
            if checkpoint.get("path") == latest and len(checkpoints) > 1:
                notes.append("latest, the default")
            lines.append(
                f"  {checkpoint.get('path') or '.'}" + (f"  ({'; '.join(notes)})" if notes else "")
            )
    detected = found.get("detected") or {}
    provenance = found.get("provenance") or {}
    # A preset only Detect's default fills ("custom") says nothing about the robot: the
    # suggestion below does.
    detected = {
        field: value for field, value in detected.items()
        if not (field == "preset" and provenance.get(field) in (None, "default"))
    }
    if detected:
        lines.append("Detected (each editable at create):")
        width = max(len(cmd._FIELD_LABELS.get(field, field)) for field in detected)
        for field, value in detected.items():
            label = cmd._FIELD_LABELS.get(field, field)
            origin = provenance.get(field)
            lines.append(
                f"  {label:<{width}}  {cmd._field_value(field, value)}"
                + (f"  ({origin})" if origin else "")
            )
        line = cmd.non_joint_line(detected.get("state_dim"), detected.get("action_dim"))
        if line:
            lines.append(line)
        suggested = found.get("suggested_preset")
        if suggested in PRESET_LAYOUTS:
            lines.append(f"Robot: the {PRESET_LAYOUTS[suggested].label} preset fits "
                         f"(--preset {suggested}).")
    else:
        lines.append("Nothing detected; give the robot with --preset or --camera and --hz.")
    if "upload" in found:
        lines.append(f"Uploads at create: {cmd.local_checkpoint.describe(found)} (only what the "
                     "build reads)")
    return lines + cmd._rtc_autofill_lines(found)


# The embodiment fields a π0.5 create sends (the control plane's spec keys).
_PI05_GEOMETRY = (
    "action_horizon", "executed_actions", "token_length", "state_in_prompt", "delta_action_mask",
)


_PI05_DEFAULTS = {"action_horizon": 50, "token_length": 200, "state_in_prompt": True}


def parse_pi05_cameras(values: list[str] | None) -> list[dict] | None:
    """`--camera key=slot` (repeatable, in the order the robot sends them)."""
    if not values:
        return None
    cameras = []
    for value in values:
        key, sep, slot = value.partition("=")
        key, slot = key.strip(), slot.strip()
        if not sep or not key or slot not in PI05_DEPLOY_SLOTS:
            raise ValueError(
                f"--camera takes key=slot with slot {', '.join(PI05_DEPLOY_SLOTS)} "
                f"(e.g. wrist_cam=left_wrist), got {value!r}"
            )
        cameras.append({"key": key, "slot": slot})
    return cameras


def _preset_template(preset: str, server_preset: dict | None) -> dict:
    layout = PRESET_LAYOUTS[preset]
    template = {
        "cameras": [{"key": key, "slot": slot} for key, slot in layout.cameras],
        "state_dim": layout.action_dim,
        "action_dim": layout.action_dim,
        "action_hz": layout.action_hz,
    }
    return {**template, **(server_preset or {})}


def build_pi05_embodiment(
    *,
    preset: str | None,
    detected: dict | None,
    server_preset: dict | None = None,
    cameras: list[dict] | None = None,
    hz: float | None = None,
    horizon: int | None = None,
    executed: int | None = None,
    token_length: int | None = None,
    state_in_prompt: bool | None = None,
    delta_mask: list[bool] | str | None = None,
    detected_presets: dict | None = None,
    lerobot: bool = False,
) -> tuple[dict, dict]:
    """The embodiment a π0.5 create sends, and the robot it describes once the control plane
    fills the preset and openpi's defaults (for the summary). A preset fixes the robot's
    wire (cameras, widths, rate); the repo's detected fields fill the rest, and flags win."""
    if preset not in (None, *PI05_PRESET_CHOICES, "custom"):
        raise ValueError(f"--preset is one of {', '.join(PI05_PRESET_CHOICES)}")
    detected = detected or {}
    wire_preset = preset if preset in PRESET_LAYOUTS else None
    body: dict = {"preset": wire_preset or "custom"}
    template: dict = {}
    if wire_preset is not None:
        template = _preset_template(wire_preset, server_preset)
        label = PRESET_LAYOUTS[wire_preset].label
        state, actions = detected.get("state_dim"), detected.get("action_dim")
        if cmd.non_joint_line(state, actions):
            raise ValueError(
                f"this checkpoint's state is {state} wide and its actions {actions}: they "
                f"aren't joint targets, so it isn't the {label} preset's robot; use --preset "
                "blank with --camera key=slot … --hz"
            )
        width = actions or state
        if width and (width != template["action_dim"] or width != template["state_dim"]):
            raise ValueError(
                f"this checkpoint's actions are {width} wide, and the {label} preset's "
                f"{template['action_dim']}: pick the preset of the robot it was trained on, "
                "or --preset blank with --camera key=slot … --hz"
            )
        # A LeRobot checkpoint fixes its cameras: send the preset's names for them as Detect
        # matched them (the server's one rule), unless --camera names them.
        entry = (detected_presets or {}).get(wire_preset)
        if lerobot and isinstance(entry, dict) and not cameras:
            if entry.get("cameras"):
                body["cameras"] = [dict(camera) for camera in entry["cameras"]]
            else:
                found = ", ".join(
                    str(c.get("feature") or c.get("key"))
                    for c in detected.get("cameras") or [] if isinstance(c, dict)
                )
                raise ValueError(
                    f"this checkpoint's cameras ({found}) aren't the {label} preset's "
                    f"({', '.join(key for key, _ in PRESET_LAYOUTS[wire_preset].cameras)}): "
                    "name each with --camera key=slot (in the checkpoint's order), or "
                    "--preset blank"
                )
    else:
        detected_cameras = [
            {key: c[key] for key in ("key", "slot", "feature") if c.get(key) is not None}
            for c in detected.get("cameras") or [] if isinstance(c, dict)
        ]
        for field, value in (
            ("cameras", detected_cameras or None),
            ("state_dim", detected.get("state_dim")),
            ("action_dim", detected.get("action_dim")),
            ("action_hz", detected.get("action_hz")),
        ):
            if value is not None:
                body[field] = value
    for field in _PI05_GEOMETRY:
        if detected.get(field) is not None:
            body[field] = detected[field]
    flags = {
        "cameras": cameras, "action_hz": hz, "action_horizon": horizon,
        "executed_actions": executed, "token_length": token_length,
        "state_in_prompt": state_in_prompt,
        "delta_action_mask": None if delta_mask == cmd.CLEAR else delta_mask,
    }
    body.update({field: value for field, value in flags.items() if value is not None})
    if delta_mask == cmd.CLEAR:
        body.pop("delta_action_mask", None)
    view = {**_PI05_DEFAULTS, **template, **body}
    view.setdefault("executed_actions", view["action_horizon"])
    _check_pi05(view)
    return body, view


def _check_pi05(view: dict) -> None:
    cameras = view.get("cameras") or []
    if not cameras:
        raise ValueError(
            "name the robot: --preset bimanual_yam|so101|arx5, or --camera key=slot (one "
            "per camera, in the order your robot sends them) with --hz"
        )
    keys = [camera.get("key") for camera in cameras]
    slots = [camera.get("slot") for camera in cameras]
    if len(cameras) > MAX_CAMERAS or len(set(keys)) != len(keys) or len(set(slots)) != len(slots):
        raise ValueError(
            f"π0.5 takes 1 to {MAX_CAMERAS} cameras, each with its own key and its own slot"
        )
    rate = view.get("action_hz")
    if not isinstance(rate, int | float) or not 0 < rate <= MAX_HZ:
        raise ValueError(f"--hz is the rate the checkpoint was trained at, up to {MAX_HZ} Hz")
    horizon, executed = view["action_horizon"], view["executed_actions"]
    if not 1 <= horizon <= MAX_HORIZON:
        raise ValueError(f"--horizon is 1 to {MAX_HORIZON} actions")
    if not 1 <= executed <= horizon:
        raise ValueError(f"--executed is 1 to the horizon ({horizon}) actions")
    if not 32 <= view["token_length"] <= 512:
        raise ValueError("--token-length is 32 to 512 tokens")
    mask, width = view.get("delta_action_mask"), view.get("action_dim")
    if mask is not None and width and len(mask) != width:
        raise ValueError(f"--delta-mask needs one value per action dimension ({width})")
    state = view.get("state_dim")
    if mask and any(mask) and cmd.non_joint_line(state, width):
        raise ValueError(
            f"delta actions are relative to the joint state, and this checkpoint's state is "
            f"{state} wide and its actions {width}: pass --delta-mask none"
        )


async def pi05_base(client_factory: Callable[..., Any]) -> dict:
    """The control plane's π0.5 base descriptor, or a clear error where it has none."""
    listed = await cmd._call(client_factory, "list_checkpoints", None)
    for base in listed.get("bases") or []:
        if isinstance(base, dict) and internal_model(str(base.get("id"))) == "pi05":
            return base
    # No `bases` (an older control plane), or not offered to this organization.
    raise errors.catalog("pi05_deployments_unavailable")


def run_add_pi05(
    *,
    repo: str,
    revision: str | None = None,
    name: str | None = None,
    hf_token: str | None = None,
    preset: str | None = None,
    path: str | None = None,
    cameras: list[dict] | None = None,
    hz: float | None = None,
    horizon: int | None = None,
    executed: int | None = None,
    token_length: int | None = None,
    state_in_prompt: bool | None = None,
    delta_mask: list[bool] | str | None = None,
    rtc: str | None = None,
    rtc_max_delay: int | None = None,
    region: str = "auto",
    wait: bool = True,
    keep_warm: str | None = None,
    slug: str | None = None,
    region_fallback: bool | None = None,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
    sleep: Callable[[float], None] = time.sleep,
) -> dict:
    """Detect, then build a π0.5 deployment: every field auto-filled from the repo (or a
    local folder, which is then uploaded) where it can be, and any flag on top."""
    folder = cmd.local_checkpoint.scan(repo) if cmd.local_checkpoint.is_local_folder(repo) else None
    if folder is not None and (revision is not None or hf_token is not None):
        raise cmd._invalid(
            "--revision and --hf-token apply to Hugging Face repos", "drop them for a folder"
        )
    token = cmd.hugging_face.token(hf_token) if folder is None else None
    base = asyncio.run(pi05_base(client_factory))
    regions = base.get("regions")
    if region == cmd.AUTO_REGION:
        region = cmd._nearest_region(client_factory, list(regions) if regions else None,
                                     print_fn)
    elif regions and region not in regions:
        raise cmd._invalid(
            f"π0.5 deployments can't run in {region} yet",
            f"create it in {' or '.join(regions)} with --region",
        )
    if folder is not None:
        found = cmd._inspect_local(client_factory, folder, print_fn, path=path)
    else:
        _, found = cmd._inspect_with_status(
            client_factory, repo, revision, token, print_fn, base=NAME, path=path
        )
    paths = [c.get("path") for c in cmd._checkpoint_paths(found)]
    if path and paths and path not in paths:
        raise cmd._invalid(
            f"{path} is not a checkpoint in {repo}",
            "pass one of --path " + ", ".join(map(str, paths)),
        )
    # The folder a pasted huggingface.co link named, as the server read it (DSL-233).
    asked = found.get("request") or {}
    repo, revision = asked.get("repo") or repo, asked.get("revision") or revision
    source_path = path or asked.get("source_path") or cmd.latest_checkpoint(found)
    server_preset = next(
        (
            entry["embodiment"]
            for entry in base.get("presets") or []
            if isinstance(entry, dict) and entry.get("id") == preset
            and isinstance(entry.get("embodiment"), dict)
        ),
        None,
    )
    try:
        embodiment, view = build_pi05_embodiment(
            preset=preset, detected=found.get("detected"), server_preset=server_preset,
            detected_presets=found.get("presets"), lerobot=found.get("format") == "lerobot",
            cameras=cameras, hz=hz, horizon=horizon, executed=executed,
            token_length=token_length, state_in_prompt=state_in_prompt, delta_mask=delta_mask,
        )
    except ValueError as error:
        raise cmd._invalid(str(error), "rerun create with the flag named above") from None
    detected_rtc = found.get("rtc") or {}
    try:
        method = cmd.parse_rtc(rtc) or detected_rtc.get("method") or "test_time"
    except ValueError as error:
        raise cmd._invalid(str(error), "use --rtc off, test-time or trained") from None
    delay = rtc_max_delay
    if method == "trained" and delay is None:
        delay = detected_rtc.get("max_delay") or None
    if method == "trained" and not (
        isinstance(delay, int) and 1 <= delay <= MAX_TRAINED_RTC_DELAY
        and delay < view["action_horizon"]
    ):
        raise cmd._invalid(
            "trained RTC needs the maximum delay the checkpoint was trained with",
            f"add --rtc-max-delay N (1-{MAX_TRAINED_RTC_DELAY}), or use --rtc test-time",
        )
    if method != "trained" and rtc_max_delay is not None:
        raise cmd._invalid(
            "--rtc-max-delay is the trained RTC's delay", "add --rtc trained, or drop it"
        )
    label = CLI.presets.get(embodiment["preset"], "Custom")
    print_fn(
        f"π0.5 {(found.get('format') or '') + ' ' if found.get('format') else ''}"
        f"checkpoint {source_path or '.'} for {label}: "
        f"cameras {cmd._cameras_line(view['cameras'])} · "
        f"{cmd._widths({'state_dim': '?', **view})} · "
        f"{view['executed_actions']} of {view['action_horizon']} actions at "
        f"{cmd._hz(view['action_hz'])} Hz · RTC {cmd.rtc_line(method, delay)}"
    )
    line = cmd.non_joint_line(view.get("state_dim"), view.get("action_dim"))
    if line:
        print_fn(line)
    local: dict[str, Any] = {}
    if folder is not None:
        # Detect said which files the build reads (for this checkpoint): upload just those.
        local = {
            "upload_id": cmd._upload_checkpoint(client_factory, folder, found, print_fn),
            "source_format": found.get("format"),
            "shown": str(folder.root),
        }
        repo, name = None, name or folder.label
    return cmd.run_add(
        repo=repo,
        model=NAME,
        revision=revision,
        name=name,
        hf_token=token,
        embodiment=embodiment,
        region=region,
        wait=wait,
        client_factory=client_factory,
        print_fn=print_fn,
        sleep=sleep,
        keep_warm=keep_warm,
        slug=slug,
        source_path=source_path,
        rtc_method=method,
        rtc_max_delay=delay if method == "trained" else None,
        region_fallback=region_fallback,
        **local,
    )


def _pi05_runner_model(embodiment: Any, checkpoint_id: str, row: dict,
                       model: str | None) -> str:
    """A π0.5 deployment `dreamscale run <robot>` drives: ``pi05`` for one of this robot; an
    error naming the way to run it for another."""
    robot_embodiment = row.get("embodiment") or {}
    state_dim, action_dim = robot_embodiment.get("state_dim"), robot_embodiment.get("action_dim")
    if None not in (state_dim, action_dim) and not joint_actions(state_dim, action_dim):
        raise non_joint_run_error(checkpoint_id, state_dim, action_dim)
    cameras = tuple(c.get("key") for c in robot_embodiment.get("cameras") or [])
    robot = robot_preset(robot_embodiment.get("preset"), cameras, action_dim)
    preset = cmd.RUNNER_PRESETS.get(embodiment.name)
    if preset is not None and robot == preset:
        return "pi05"
    if robot is None and cmd._recorded_on(embodiment, cameras, state_dim, action_dim):
        return "pi05"
    if embodiment.name in cmd.RECORDED_RUNNERS:
        width = len(embodiment.arms) * embodiment.arm_size
        raise cmd._invalid(
            f"{checkpoint_id} wasn't fine-tuned on a {embodiment.label} recording",
            f"`dreamscale run {embodiment.name}` runs deployments with cameras "
            f"{', '.join(embodiment.recording_keys)} (in that order) and {width} joint values",
            cause=f"`dreamscale run {embodiment.name}` drives {embodiment.label} only",
        )
    layout = PRESET_LAYOUTS.get(robot or "")
    built_for = layout.label if layout is not None else "a custom robot"
    if layout is not None and layout.run_command:
        fix = f"run it with `{layout.run_command} --deployment {checkpoint_id}`"
    else:
        helper = layout.observe_helper if layout is not None else "dreamscale.robot.observation"
        fix = (
            f'drive it from Python: dreamscale.connect("pi0.5", deployment="{checkpoint_id}"), '
            f"with observations from {helper}(…)"
        )
    raise cmd._invalid(
        f"{checkpoint_id} is a π0.5 deployment for {built_for}, not {embodiment.label}",
        fix,
        cause=f"`dreamscale run {embodiment.name}` drives {embodiment.label} only",
    )


def _set_pi05_rtc(row, checkpoint_id, method, max_delay, client_factory, print_fn) -> dict:
    """π0.5: off, test-time, or trained with the maximum delay its checkpoint trained."""
    if "rtc_method" not in row:
        raise errors.catalog("pi05_deployments_unavailable")
    if method == "trained":
        max_delay = max_delay or row.get("trained_rtc_max_delay") or None
        if not isinstance(max_delay, int) or not 1 <= max_delay <= MAX_TRAINED_RTC_DELAY:
            raise cmd._invalid(
                "trained RTC needs the maximum delay the checkpoint was trained with",
                f"add --max-delay N (1-{MAX_TRAINED_RTC_DELAY})",
            )
    elif max_delay is not None:
        raise cmd._invalid("--max-delay is the trained RTC's delay", "use it with trained")
    result = asyncio.run(
        cmd._call(client_factory, "set_deployment_rtc", checkpoint_id, method, max_delay=max_delay)
    )
    print_fn(
        f"{checkpoint_id}: RTC {cmd.rtc_line(method, max_delay)} for new sessions. An idle server "
        "is replaced now; one a robot is on when the robot disconnects."
    )
    return result



async def inspect(client, repo: str, revision: str | None, token: str | None, base: str,
                  path: str | None) -> tuple[str, dict]:
    """Detect as π0.5 (`--base pi0.5`, or auto): a repo π0.5 can't read, or an older control
    plane's answer (it ignores ``model``), is read as Isaac 0.5's."""
    try:
        found = await client.inspect_endpoint_repo(
            repo, revision=revision, hf_token=token, model=NAME,
            **({"path": path} if path else {}),
        )
    except errors.DreamscaleError as error:
        if base == NAME and error.code == "invalid_request" and "model" in str(error):
            raise errors.catalog("pi05_deployments_unavailable") from None
        if base == NAME or not cmd._may_be_another_base(error):
            raise
        pi05_error = error
    else:
        if is_pi05_inspect(found):
            return NAME, found
        if base == NAME:
            raise errors.catalog("pi05_deployments_unavailable")
        # An older control plane read it as Isaac 0.5 (it ignores `model`).
        return cmd.ISAAC, found
    try:
        return cmd.ISAAC, await client.inspect_endpoint_repo(
            repo, revision=revision, hf_token=token
        )
    except errors.DreamscaleError:
        raise pi05_error from None


def create(*, repo, given, preset, camera, hz, path, executed, steps, joint_unit, rtc,
           rtc_prefix, revision, name, hf_token, region, wait, keep_warm, slug,
           region_fallback=None) -> None:
    """`deployments create --base pi0.5` (or with no --base): the flags only Isaac 0.5 takes,
    and the units bases' (--rtc-prefix, --steps, --joint-unit), are refused by name."""
    for flag, value in (("--rtc-prefix", rtc_prefix), ("--steps", steps),
                        ("--joint-unit", joint_unit)):
        if value is not None:
            raise cli.typer.BadParameter(f"{flag} doesn't apply to {BASE.label} deployments.",
                                         param_hint=f"'{flag}'")
    if keep_warm is not None and keep_warm not in cmd.KEEP_WARM_VALUES:
        raise cli.typer.BadParameter(
            f"use one of {', '.join(cmd.KEEP_WARM_VALUES)}", param_hint="'--keep-warm'"
        )
    for field in cli._ISAAC_ONLY:
        if given[field] is not None:
            raise cli.typer.BadParameter(
                f"{cli._flag(field)} applies to Isaac 0.5 deployments only.")
    try:
        region = cmd.parse_region(region)
        if preset is not None and preset not in (*PI05_PRESET_CHOICES, "custom"):
            raise ValueError(f"--preset is one of {', '.join(PI05_PRESET_CHOICES)} for π0.5")
        options = dict(
            cameras=parse_pi05_cameras(camera), delta_mask=cmd.parse_delta_mask(
                given["delta_mask"]),
            rtc=cmd.parse_rtc(rtc),
        )
    except ValueError as error:
        raise cli.typer.BadParameter(str(error)) from None
    result: dict = {}
    cli._run(
        lambda **kwargs: result.update(run_add_pi05(**kwargs)),
        repo=repo, revision=revision, name=name, hf_token=hf_token, preset=preset, path=path,
        hz=hz, horizon=given["horizon"], executed=executed, token_length=given["token_length"],
        state_in_prompt=False if given["no_state_in_prompt"] else None,
        rtc_max_delay=given["rtc_max_delay"], region=region,
        wait=wait, keep_warm=keep_warm, slug=slug, region_fallback=region_fallback, **options,
    )
    if result.get("status") == "failed":
        raise cli.typer.Exit(code=1)


def run_command(deployment: dict) -> str:
    """How to run a trained deployment: its preset robot's command, or Python."""
    embodiment = deployment.get("embodiment") or {}
    robot = robot_preset(
        embodiment.get("preset"),
        tuple(c.get("key") for c in embodiment.get("cameras") or []),
        embodiment.get("action_dim") or 0,
        embodiment.get("state_dim"),
    )
    layout = PRESET_LAYOUTS.get(robot or "")
    if layout is not None and layout.run_command:
        model = deployment.get("model") or "pi0.5"
        option = f" --model {model}" if model != "pi0.5" else ""
        return f"{layout.run_command}{option} --deployment {deployment['id']}"
    model = deployment.get("model") or "pi0.5"
    return f'dreamscale.connect("{model}", deployment="{deployment["id"]}")'


def robot_line(checkpoint: dict) -> str:
    return pi05_robot_line(checkpoint)


def describe(checkpoint: dict) -> list[str]:
    return _describe_pi05(checkpoint)


def runner(embodiment, checkpoint_id, row, model):
    return _pi05_runner_model(embodiment, checkpoint_id, row, model)


def set_rtc(row, checkpoint_id, method, max_delay, client_factory, print_fn) -> dict:
    return _set_pi05_rtc(row, checkpoint_id, method, max_delay, client_factory, print_fn)


BASE = DeployBase(
    family="pi05", name=NAME, label="π0.5", cli=CLI, aliases=("pi05",), listed_as=NAME,
    robot_line=robot_line, describe=describe, shows_rtc=True, runner=runner, set_rtc=set_rtc,
    found_lines=pi05_inspect_lines, create=create, run_command=run_command, default=True,
    claims_rows=True, row_steps=row_steps, inspect=inspect,
    preview_contract=PREVIEW_CONTRACT,
    session=SessionBase(
        "dreamscale.policy.pi05_deployment:SessionDeployment",
        "dreamscale.policy.pi05_deployment:runtime_contract",
        "dreamscale.policy.pi05_deployment:control_hz",
    ),
    unavailable="pi05_deployments_unavailable", robot_presets=PRESET_LAYOUTS,
    # Fine-tunes on a LeRobot recording of these rigs (their cameras keep the recording's
    # names).
    robots=("ur", "xarm7"),
)
