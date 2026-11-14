"""Xiaomi-Robotics-1 deployments in the SDK: a run folder upstream's ``xr1/`` trainer wrote (or a
Dreamscale training export), on the bimanual YAM preset or a custom robot, absolute end-effector
rows, RTC off or trained (dreamscale_transport.xr1_deploy is the contract).

Listed since GA (0138). Its checkpoints don't record their robot, so a create
declares it: ``--preset bimanual_yam`` (the default), or a custom robot's arms, cameras (by view,
with the crop each trained with), waist, mobile base, end-effector frame and units, as the
control plane's ``normalize_xr1_embodiment`` takes them. Its sessions' contract is
dreamscale.policy.xr1_deployment. `dreamscale run yam --deployment` drives a deployment of the
bimanual YAM preset (``robots``, ``robot_adapters``: dreamscale.hardware.xr1_yam turns the rig's
joints into its end-effector state and its pose rows into joint targets); a custom robot's runs
from Python: ``dreamscale.connect("xiaomi-robotics-1", deployment=...)``.

``run_add_xr1`` is `deployments create --base xiaomi-robotics-1` without the CLI. The CLI's
create command passes the options every base shares as keywords; XR-1's own (``--arm``,
``--ee-frame``, ``--gripper-unit``, ``--waist``, ``--mobile-base``) arrive in its ``given``
(``ARM``, ``EE_FRAME``, ``GRIPPER_UNIT``, ``WAIST``, ``MOBILE_BASE``), where every other base
refuses them by name.
"""

from __future__ import annotations

import time
from pathlib import Path

from dreamscale_transport import xr1_deploy as C

from dreamscale.deploy_bases import Base, DeployBase, ExportedBase, cli, cmd

NAME = C.XR1_BASE_MODEL
LABEL = C.XR1_PUBLIC_NAME
# Its presets and its build's steps, as `deployments create --wait` shows them.
CLI = Base({C.PRESET: C.PRESET_LABEL, "custom": "Custom"}, (
    ("Finding the export", ("building", "resolving", "checking")),
    ("Downloading", ("downloading",)),
    ("Saving", ("validating", "sealing", "built")),
    ("Testing on a server", ("qualifying", "ready", "failed")),
), None)
# The `given` keys of XR-1's own create options.
ARM, EE_FRAME, GRIPPER_UNIT, WAIST, MOBILE_BASE = (
    "arm", "ee_frame", "gripper_unit", "waist", "mobile_base")
_OWN = (ARM, EE_FRAME, GRIPPER_UNIT, WAIST, MOBILE_BASE)
_ROBOT_FLAGS = "--arm, --camera, --ee-frame, --joint-unit, --gripper-unit"


# --- rows ---------------------------------------------------------------------------------------


def xr1_robot_line(checkpoint: dict) -> str:
    """One line for a Xiaomi-Robotics-1 deployment: robot, widths, geometry, rate and RTC.
    Before its build reads the checkpoint, a row holds only what its create sent."""
    spec = checkpoint.get("embodiment") or {}
    parts = [LABEL]
    if spec.get("preset"):
        parts.append(CLI.presets.get(spec["preset"], "Custom"))
    if spec.get("state_dim") is not None:
        parts.append(cmd._widths(spec))
    if spec.get("action_horizon") is not None:
        parts.append(f"{spec.get('executed_actions')} of {spec['action_horizon']} actions at "
                     f"{cmd._hz(spec.get('action_hz'))} Hz"
                     + (f" (each answer returns all {spec['action_horizon']})"
                        if spec.get("full_chunk") else ""))
    if checkpoint.get("rtc_method") and checkpoint.get("status") != "building":
        parts.append(f"RTC {cmd.prefix_rtc(checkpoint)}")
    elif not checkpoint.get("rtc_method") and spec.get("trained_rtc_max_delay"):
        parts.append(f"trained with RTC (up to {spec['trained_rtc_max_delay']} actions)")
    return " · ".join(parts)


def _arms_line(spec: dict) -> str | None:
    arms = [f"{arm.get('side')} ({arm.get('joints')} joints)" for arm in spec.get("arms") or []]
    if not arms:
        return None
    return ", ".join(arms + ["waist"] * bool(spec.get("waist"))
                     + ["mobile base"] * bool(spec.get("base") or spec.get("base_components")))


def _base_components(spec: dict) -> list[str]:
    return [str(c) for c in spec.get("base_components") or []]


def _camera(camera: dict) -> str:
    crop = camera.get("crop")
    return f"{camera.get('key')} → {camera.get('view')}" + (
        f" (crop {', '.join(map(str, crop))})" if crop else "")


def _describe_xr1(checkpoint: dict) -> list[str]:
    source = checkpoint.get("source") or {}
    revision = source.get("resolved_revision") or source.get("revision") or "main"
    spec = checkpoint.get("embodiment") or {}
    where = f"hf://{source.get('repo')}@{revision}"
    if source.get("kind") == "upload":
        where = f"local run folder (upload {source.get('repo')})"
    if source.get("path"):
        where += f" · {source['path']}"
    arms = _arms_line(spec)
    cameras = ", ".join(_camera(camera) for camera in spec.get("cameras") or [])
    base = _base_components(spec)
    frame = ([f"  frame:    {spec['ee_frame']} · joints {spec.get('joint_unit')} · gripper "
              f"{spec.get('gripper_unit')}"] if spec.get("ee_frame") and spec.get("arms")
             else [])
    actions = ("absolute end-effector poses (xyz, 6D rotation, gripper per arm); the robot "
               "holds its measured pose between chunks")
    vector = spec.get("vector") or {}
    if vector:
        hold = ("holds its measured values" if vector.get("hold", "measured") == "measured"
                else "holds zeros")
        actions = (f"{vector.get('action')} values, absolute, in your data's order and units "
                   f"(from a state of {vector.get('state')}); between chunks the robot {hold}")
    elif base and not spec.get("arms"):
        actions = (f"the mobile base's {', '.join(base)}, absolute, in your data's units; "
                   "between chunks the base holds still (zero velocity)")
    elif base:
        actions += f"; then the mobile base's {', '.join(base)} (still between chunks)"
    lines = [
        f"{cmd._title(checkpoint)}  ({LABEL})",
        *cmd._id_line(checkpoint),
        f"  robot:    {xr1_robot_line(checkpoint)}",
        *([f"  arms:     {arms}"] if arms else []),
        *([f"  base:     mobile base ({', '.join(base)})"] if base else []),
        *([f"  cameras:  {cameras}"] if cameras else []),
        *frame,
        f"  actions:  {actions}",
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
    return trained


def xr1_found_lines(found: dict) -> list[str]:
    """What Detect read from a run folder: its checkpoint, its robot (the declared one, which
    the checkpoint doesn't record) and its RTC."""
    checkpoint = found.get("checkpoint") or {}
    step = checkpoint.get("step")
    detected = found.get("detected") or {}
    trained = _trained(found)
    lines = []
    if checkpoint.get("path"):
        lines.append(f"Checkpoint: {checkpoint['path']}"
                     + (f" (step {step:,})" if isinstance(step, int) else ""))
    lines += [
        "Robot: " + (xr1_robot_line({"embodiment": detected}) if detected.get("preset") else
                     f"declared at create (--preset {C.PRESET}, or a custom robot's "
                     f"{_ROBOT_FLAGS}); the checkpoint doesn't record it"),
        "RTC: " + (f"trained with prefixes up to {trained} actions (default: trained, prefix "
                   f"up to {trained})" if trained else "trained without prefixes (off)"),
    ]
    lines += [f"Note: {warning}" for warning in found.get("warnings") or []]
    return lines


# --- `deployments create` -----------------------------------------------------------------------


def parse_arms(values: list[str] | None) -> list[dict] | None:
    """`--arm side:joints` (repeatable, left before right), e.g. left:7."""
    if not values:
        return None
    arms = []
    for value in values:
        side, sep, joints = value.partition(":")
        side, joints = side.strip(), joints.strip()
        if not sep or side not in C.SIDES or not joints.isdigit():
            raise ValueError(f"--arm takes side:joints (left or right, and its joint count, "
                             f"e.g. left:7), got {value!r}")
        arms.append({"side": side, "joints": int(joints)})
    return arms


def parse_cameras(values: list[str] | None) -> list[dict] | None:
    """`--camera key=view[:top,left,height,width]` (repeatable): the robot's camera key, the
    view it fills (ego, left_wrist, right_wrist) and the crop it trained with, if any."""
    if not values:
        return None
    cameras = []
    for value in values:
        key, sep, rest = value.partition("=")
        view, colon, crop = rest.partition(":")
        key, view = key.strip(), view.strip()
        box = [part.strip() for part in crop.split(",")] if colon else None
        if (not sep or not key or view not in C.VIEWS
                or (box is not None and (len(box) != 4 or not all(p.isdigit() for p in box)))):
            raise ValueError(
                f"--camera takes key=view or key=view:top,left,height,width (view one of "
                f"{', '.join(C.VIEWS)}; the crop in capture pixels), got {value!r}"
            )
        cameras.append({"key": key, "view": view,
                        "crop": None if box is None else [int(p) for p in box]})
    return cameras


def xr1_embodiment(*, preset=None, cameras=None, arms=None, waist=None, base=None,
                   ee_frame=None, joint_unit=None, gripper_unit=None, executed=None,
                   hz=None) -> dict:
    """The embodiment a create sends (what the control plane's ``normalize_xr1_embodiment``
    takes): the preset, or a custom robot's arms, cameras, waist, mobile base, frame and units;
    plus the executed rows per chunk and the control rate. Checked here with the transport
    contract's own models, so a robot it can't serve fails before anything is read."""
    robot = {"cameras": cameras, "arms": arms, "ee_frame": ee_frame, "joint_unit": joint_unit,
             "gripper_unit": gripper_unit, "waist": waist or None, "base": base or None}
    given = [key for key, value in robot.items() if value is not None]
    if preset not in (None, *C.PRESETS):
        raise cmd._invalid(f"{LABEL} runs preset {C.PRESET} or a custom robot",
                           f"use --preset {C.PRESET} or --preset custom")
    if preset == C.PRESET and given:
        raise cmd._invalid(
            f"--preset {C.PRESET} fixes its cameras, arms, frame and units",
            f"omit {_flag(given[0])}, or declare your robot with --preset custom",
        )
    if preset == C.PRESET or (preset is None and not given):
        embodiment: dict = {"preset": C.PRESET}
    else:
        missing = [key for key in ("arms", "cameras", "ee_frame", "joint_unit", "gripper_unit")
                   if robot[key] is None]
        if missing:
            raise cmd._invalid(
                f"a custom {LABEL} robot declares its arms, cameras, end-effector frame and "
                "units", f"pass {', '.join(_flag(key) for key in missing)} "
                f"(or --preset {C.PRESET})",
            )
        try:
            parsed_arms = [C.Xr1Arm.model_validate(arm) for arm in arms]
            parsed_cameras = [C.Xr1Camera.model_validate(
                {**camera, "crop": None if camera.get("crop") is None else tuple(camera["crop"])}
            ) for camera in cameras]
        except (AttributeError, TypeError, ValueError) as error:
            raise cmd._invalid(f"invalid {LABEL} robot: {_message(error)}",
                               f"fix {_ROBOT_FLAGS}") from None
        sides = [arm.side for arm in parsed_arms]
        if len(set(sides)) != len(sides) or sides != [s for s in C.SIDES if s in sides]:
            raise cmd._invalid("arms are 1-2 distinct sides, left before right",
                               "pass --arm left:N before --arm right:N")
        views = [camera.view for camera in parsed_cameras]
        if (len(set(views)) != len(views) or views != [v for v in C.VIEWS if v in views]
                or len({camera.key for camera in parsed_cameras}) != len(views)):
            raise cmd._invalid(
                "cameras are 1-3 distinct robot keys, each filling a distinct view",
                f"pass --camera in the order {', '.join(C.VIEWS)}",
            )
        if not C._FRAME_ID.fullmatch(ee_frame):
            raise cmd._invalid("--ee-frame names the frame your end-effector poses are in",
                               "use a short id (letters, digits, . _ : / -)")
        if joint_unit not in C.JOINT_UNITS:
            raise cmd._invalid(f"--joint-unit is one of {', '.join(C.JOINT_UNITS)}",
                               "use --joint-unit rad or deg")
        if gripper_unit not in C.GRIPPER_UNITS:
            raise cmd._invalid(f"--gripper-unit is one of {', '.join(C.GRIPPER_UNITS)}",
                               "use the unit your gripper's data was recorded in")
        embodiment = {
            "preset": "custom",
            "cameras": [camera.model_dump(mode="json") for camera in parsed_cameras],
            "arms": [arm.model_dump(mode="json") for arm in parsed_arms],
            "waist": bool(waist), "base": bool(base), "ee_frame": ee_frame,
            "joint_unit": joint_unit, "gripper_unit": gripper_unit,
        }
    if executed is not None:
        # The checkpoint's chunk bounds it (30 rows, or its run's): the server checks that.
        if type(executed) is not int or not 1 <= executed <= C.MAX_ACTION_HORIZON:
            raise cmd._invalid(f"--executed is 1-{C.MAX_ACTION_HORIZON} actions per chunk, "
                               "within the checkpoint's chunk",
                               f"pass --executed 1-{C.ACTION_HORIZON} (a 30-row checkpoint)")
        embodiment["executed_actions"] = executed
    if hz is not None:
        if isinstance(hz, bool) or not isinstance(hz, int | float) or not 0 < hz <= 100:
            raise cmd._invalid("--hz is the rate the data was recorded at (0-100)",
                               "pass --hz 30, say")
        embodiment["action_hz"] = float(hz)
    return embodiment


def run_add_xr1(*, repo: str, revision=None, name=None, hf_token=None, path=None,
                preset=None, cameras=None, arms=None, waist=None, base=None, ee_frame=None,
                joint_unit=None, gripper_unit=None, executed=None, hz=None, rtc=None,
                rtc_prefix=None, region="auto", wait=True, keep_warm=None, slug=None,
                region_fallback=None, client_factory=None, print_fn=print, sleep=time.sleep):
    """Read a run folder (a Hub repo or a local folder), pin the resolved commit, and deploy it
    on the robot the create declares (``xr1_embodiment``). RTC: trained where the checkpoint
    trained with prefixes (with every prefix row it trained, or ``rtc_prefix``), else off."""
    if client_factory is None:
        from dreamscale.control import ControlPlaneClient

        client_factory = ControlPlaneClient
    embodiment = xr1_embodiment(
        preset=preset, cameras=cameras, arms=arms, waist=waist, base=base, ee_frame=ee_frame,
        joint_unit=joint_unit, gripper_unit=gripper_unit, executed=executed, hz=hz,
    )
    if rtc not in (None, *C.RTC_METHODS):
        raise cmd._invalid(f"{LABEL} runs RTC off or trained", "use --rtc off or --rtc trained")
    if rtc_prefix is not None and rtc == "off":
        raise cmd._invalid("--rtc-prefix goes with trained RTC", "omit --rtc-prefix, or --rtc off")
    region = cmd._check_region(client_factory, NAME, LABEL, region, print_fn=print_fn)
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
    if found.get("source_format") != C.XR1_SOURCE_FORMAT:
        raise cmd._invalid(f"the server did not read a {LABEL} run folder",
                           "update the SDK and retry")
    for line in xr1_found_lines(found):
        print_fn(line)
    trained = _trained(found)
    method = rtc or ("trained" if rtc_prefix is not None else None)
    if method == "trained" and not trained:
        raise cmd._invalid(
            "this checkpoint trained without prefixes, so it can't run trained RTC",
            "omit --rtc (it runs RTC off)",
        )
    if rtc_prefix is not None and not 1 <= rtc_prefix <= trained:
        raise cmd._invalid(f"the RTC prefix is 1-{trained} actions (what the checkpoint was "
                           "trained on)", f"pass --rtc-prefix 1-{trained}")
    source = found.get("request") or {}
    local = {}
    if folder:
        local = {
            "upload_id": cmd._upload_checkpoint(
                client_factory, folder, found, print_fn, base_model=NAME
            ),
            "source_format": C.XR1_SOURCE_FORMAT, "shown": str(Path(repo).expanduser()),
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


def _create_xr1(*, repo, given, preset, camera, hz, path, executed, steps, joint_unit, rtc,
                rtc_prefix, revision, name, hf_token, region, wait, keep_warm, slug,
                region_fallback=None) -> None:
    from dreamscale.checkpoints_cmd import KEEP_WARM_VALUES, parse_region

    unsupported = [key for key, value in given.items()
                   if value is not None and key not in ("path", "executed", "rtc", *_OWN)]
    if steps is not None:
        unsupported.append("steps")
    if unsupported:
        raise cli.typer.BadParameter(
            f"{cli._flag(unsupported[0])} doesn't apply to {LABEL}: the checkpoint records its "
            f"widths, horizon and statistics. Pass --preset {C.PRESET}, or a custom robot's "
            f"{_ROBOT_FLAGS}, --waist and --mobile-base; and --executed, --hz, --path, --rtc "
            "and --rtc-prefix."
        )
    if keep_warm is not None and keep_warm not in KEEP_WARM_VALUES:
        raise cli.typer.BadParameter(
            f"use one of {', '.join(KEEP_WARM_VALUES)}", param_hint="'--keep-warm'"
        )
    try:
        region = parse_region(region)
        if preset is not None and preset not in CLI.presets:
            raise ValueError(f"--preset is {C.PRESET} or custom for {LABEL}")
        if rtc is not None and rtc.strip().lower() not in C.RTC_METHODS:
            raise ValueError(f"--rtc is off or trained for {LABEL}, got {rtc!r}")
        cameras = parse_cameras(camera)
        arms = parse_arms(given.get(ARM))
    except ValueError as error:
        raise cli.typer.BadParameter(str(error)) from None
    result: dict = {}
    cli._run(
        lambda **kwargs: result.update(run_add_xr1(**kwargs)),
        repo=repo, revision=revision, name=name, hf_token=hf_token, path=path, preset=preset,
        cameras=cameras, arms=arms, waist=given.get(WAIST), base=given.get(MOBILE_BASE),
        ee_frame=given.get(EE_FRAME), joint_unit=joint_unit,
        gripper_unit=given.get(GRIPPER_UNIT), executed=executed, hz=hz,
        rtc=None if rtc is None else rtc.strip().lower(), rtc_prefix=rtc_prefix,
        region=region, wait=wait, keep_warm=keep_warm, slug=slug, region_fallback=region_fallback,
    )
    if result.get("status") == "failed":
        raise cli.typer.Exit(code=1)


def _flag(key: str) -> str:
    return {"arms": "--arm", "cameras": "--camera", "base": "--mobile-base"}.get(
        key, "--" + key.replace("_", "-"))


def _message(error: ValueError) -> str:
    errors = getattr(error, "errors", None)
    if callable(errors):
        return str(errors()[0].get("msg"))
    return str(error)


# --- `dreamscale run` ----------------------------------------------------------------------------

# The rig `dreamscale run` drives the YAM preset on (dreamscale.embodiments.YAM).
_YAM = "yam"


def _runs_on_yam(spec: dict) -> bool:
    """A deployment of the bimanual YAM preset, its poses in YAM's end-effector frame."""
    return spec.get("preset") == C.PRESET and spec.get("ee_frame", C.YAM_EE_FRAME) == C.YAM_EE_FRAME


def runner(embodiment, checkpoint_id, row, model):
    """The model `dreamscale run <robot> --deployment` runs: the base on `dreamscale run yam`
    for the YAM preset (dreamscale.hardware.xr1_yam); a clear error, naming how to run it,
    otherwise: a custom robot has no runner and runs from Python."""
    spec = row.get("embodiment") or {}
    if _runs_on_yam(spec) and embodiment.name == _YAM:
        return NAME
    if _runs_on_yam(spec):
        raise cmd._invalid(
            f"{checkpoint_id} is a {LABEL} deployment for {C.PRESET_LABEL}, which `dreamscale "
            f"run {embodiment.name}` doesn't drive",
            f"run it with `dreamscale run {_YAM} --deployment {checkpoint_id}`",
            cause=f"`dreamscale run {embodiment.name}` drives {embodiment.label} only",
        )
    raise cmd._invalid(
        f"{checkpoint_id} is a {LABEL} deployment for a custom robot, which `dreamscale run` "
        "doesn't drive",
        f'drive it from Python: dreamscale.connect("{NAME}", deployment="{checkpoint_id}"), '
        "then policy.next_action(...) with your robot's state "
        "(dreamscale.policy.xr1_deployment.robot_state); turn its end-effector targets into "
        "joint targets on your robot",
        cause=f"`dreamscale run` drives {LABEL} deployments of the {C.PRESET} preset only",
    )


def run_command(deployment: dict) -> str:
    """How to run a deployment: `dreamscale run yam` for the YAM preset, else Python."""
    if _runs_on_yam(deployment.get("embodiment") or {}):
        return f"dreamscale run {_YAM} --deployment {deployment['id']}"
    return f'dreamscale.connect("{NAME}", deployment="{deployment["id"]}")'


# --- `deployments rtc` --------------------------------------------------------------------------


def set_rtc(row, checkpoint_id, method, max_delay, client_factory, print_fn) -> dict:
    return cmd._set_prefix_rtc(row, checkpoint_id, method, max_delay, client_factory, print_fn,
                               label=LABEL, bound=C.MAX_TRAINED_RTC_DELAY,
                               untrained_fix="it runs RTC off")


EXPORTED = ExportedBase(
    LABEL,
    "dreamscale.policy.xr1_deployment:Xr1SessionDeployment",
    "dreamscale.policy.xr1_deployment:runtime_contract",
    # One plain vector of joints and end-effector poses: a helper's joint-only state isn't it.
    state="refuse",
)
BASE = DeployBase(
    family="xr1", name=NAME, label=LABEL, cli=CLI, aliases=("xr1",), listed_as=NAME,
    robot_line=xr1_robot_line, describe=_describe_xr1, shows_rtc=True, set_rtc=set_rtc,
    detects_as_base=True, found_lines=xr1_found_lines, create=_create_xr1, exported=EXPORTED,
    # A run folder's model states are torch archives: Detect reads their data.pkl from the
    # listing's spans, and the upload sends only the members a build reads (a lone .pt has no
    # config.yaml, so the intake refuses it with its fix).
    local_archive=True,
    runner=runner, run_command=run_command,
    # The bimanual YAM preset's absolute end-effector rows, turned into joint targets.
    robots=(_YAM,), robot_adapters={_YAM: "dreamscale.hardware.xr1_yam"},
)
