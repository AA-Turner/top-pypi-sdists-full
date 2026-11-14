"""Flex-π deployments in the SDK: its base as the CLI and the policy runtime know it
(``dreamscale.deploy_bases`` loads it by the family manifest's id).

Scaffolded by scripts/new_model.py, unlisted (``listed_as=None``) until GA. Its deployments run
the robot preset its transport module declares (dreamscale_transport.flexpi_deploy) or a custom
robot (docs/plans/2026-11-14-flexpi-any-robot.md): its run's config.yaml gives its widths and the
views it filmed; the create names its cameras' keys for those views (`--preset custom --camera
<key>=<view>`), its rate (`--hz`, required: a run's config doesn't record it) and, for joint
targets, their unit (`--joint-unit`; otherwise the model defines the values). `deployments
create`, its robot line, Detect's lines and its RTC setting are the shared preset base's
(deploy_bases/_preset.py) with those additions, and its sessions' contract is
dreamscale.policy.flexpi_deployment. `dreamscale run yam --deployment` drives the preset on the
Bimanual YAM rig (the same cameras, joint radians and 0-1 grippers as π0.5's and GR00T N1.7's YAM
deployments; the run loop sends the last executed command as the ``action_history`` Flex-π
anchors on); ``dreamscale.connect("flexpi", deployment=...)`` drives either from Python, paced at
the deployment's own rate.
"""

from __future__ import annotations

from dataclasses import dataclass

from dreamscale_transport import flexpi_deploy as C

from dreamscale.deploy_bases import Base, DeployBase, ExportedBase, cli, cmd
from dreamscale.deploy_bases._preset import PresetUnits

NAME = "flexpi"
# The rig `dreamscale run` drives its one preset on.
_YAM = "yam"
# Its preset and its build's steps, as `deployments create --wait` shows them.
CLI = Base({C.PRESET: C.PRESET_LABEL}, (
    ("Finding the export", ("building", "resolving", "checking")),
    ("Downloading", ("downloading",)),
    ("Saving", ("validating", "sealing", "built")),
    ("Testing on a server", ("qualifying", "ready", "failed")),
), None)


@dataclass(frozen=True)
class FlexpiUnits(PresetUnits):
    """The preset base's hooks, plus a custom robot's create, rows and Detect lines."""

    def robot_name(self, spec: dict) -> str:
        if spec.get("preset") == C.CUSTOM:
            keys = ", ".join(c.get("key", "?") for c in spec.get("cameras") or ())
            return f"custom robot ({keys})" if keys else "custom robot"
        return super().robot_name(spec)

    def found_lines(self, found: dict) -> list[str]:
        """What Detect read: the export and its robot (the YAM preset, or a custom robot of the
        views its run filmed, whose rate the create declares)."""
        detected = found.get("detected") or {}
        if detected.get("preset") != C.CUSTOM:
            return super().found_lines(found)
        lines = super().found_lines(found)[:1]
        views = ", ".join(c.get("feature", "?") for c in detected.get("cameras") or ())
        lines.append(f"Robot: custom ({detected.get('state_dim')} state values, "
                     f"{detected.get('action_dim')} actions; views {views}; declare --hz)")
        return lines

    def create(self, *, repo, given, preset, camera, hz, path, executed, steps, joint_unit, rtc,
               rtc_prefix, revision, name, hf_token, region, wait, keep_warm, slug,
               region_fallback=None) -> None:
        """`deployments create --base flexpi`: the preset's (the shared base's), or a custom
        robot's (`--preset custom --camera <key>=<view> ... --hz <rate> [--joint-unit rad|deg]`).
        Either may say `--rtc off`, what Flex-π serves."""
        given = {key: value for key, value in given.items()
                 if not (key == "rtc" and value == "off")}
        if preset != C.CUSTOM:
            return super().create(
                repo=repo, given=given, preset=preset, camera=camera, hz=hz, path=path,
                executed=executed, steps=steps, joint_unit=joint_unit, rtc=rtc,
                rtc_prefix=rtc_prefix, revision=revision, name=name, hf_token=hf_token,
                region=region, wait=wait, keep_warm=keep_warm, slug=slug,
                region_fallback=region_fallback)
        unsupported = [key for key, value in given.items()
                       if value is not None and key not in ("path", "executed")]
        if steps is not None or rtc_prefix is not None or rtc not in (None, "off") or unsupported:
            raise cli.typer.BadParameter(
                "a custom Flex-π robot takes --camera, --hz, --joint-unit, --path and --executed")
        if hz is None:
            raise cli.typer.BadParameter(
                "a custom Flex-π robot declares the rate its run's data was recorded at: --hz "
                "<whole Hz> (its config doesn't record it)")
        if joint_unit not in (None, *C.JOINT_UNITS):
            raise cli.typer.BadParameter(f"--joint-unit is {' or '.join(C.JOINT_UNITS)}")
        robot = {"preset": C.CUSTOM, "cameras": _views(camera)}
        if joint_unit is not None:
            robot.update(action_space=C.ACTION_SPACE, joint_unit=joint_unit)
        result = {}
        cli._run(
            lambda **kwargs: result.update(self.run_add(**kwargs)),
            repo=repo, revision=revision, name=name, hf_token=hf_token, path=path,
            executed=executed, rtc=rtc, rtc_prefix=None, region=region or cmd.AUTO_REGION,
            wait=wait, keep_warm=keep_warm, slug=slug, region_fallback=region_fallback,
            robot=robot, hz=hz,
        )
        if result.get("status") == "failed":
            raise cli.typer.Exit(code=1)
        return None


def _views(camera) -> list[dict]:
    """`--camera key=view`, one per view the run filmed (Detect lists them; the server holds them
    to the run's)."""
    views = ", ".join(C.VIEWS)
    pairs = []
    for item in camera or ():
        key, sep, view = str(item).partition("=")
        if not sep or not C.safe_key(key) or view not in C.VIEWS:
            raise cli.typer.BadParameter(
                f"--camera takes key=view, the view one of {views} (got {item!r})")
        pairs.append({"key": key, "feature": view})
    if not pairs or len({p["key"] for p in pairs}) != len(pairs) or len(
            {p["feature"] for p in pairs}) != len(pairs):
        raise cli.typer.BadParameter(
            f"a custom Flex-π robot names each camera once: --camera key=view for each view its "
            f"run filmed ({views})")
    return pairs


UNITS = FlexpiUnits(
    name=NAME, label=C.FLEXPI_PUBLIC_NAME,
    source_format=C.FLEXPI_SOURCE_FORMAT,
    preset=C.PRESET, preset_label=C.PRESET_LABEL, cameras=C.CAMERAS,
    state_dim=C.STATE_DIM, action_dim=C.ACTION_DIM, action_horizon=C.ACTION_HORIZON,
    action_hz=C.ACTION_HZ, action_space=C.ACTION_SPACE, joint_unit=C.JOINT_UNIT,
    gripper_unit=C.GRIPPER_UNIT, gripper_indices=C.GRIPPER_INDICES,
    # `--hz`: any rate goes to the server (a custom robot must declare one; the YAM preset may),
    # whose validation decides (whole Hz, 1-100).
    declared_rates=None,
)
# `deployments create --base flexpi`, without the CLI.
run_add_flexpi = UNITS.run_add


def _custom(row: dict) -> bool:
    return ((row or {}).get("embodiment") or {}).get("preset") == C.CUSTOM


def runner(embodiment, checkpoint_id, row, model):
    """The model `dreamscale run <robot> --deployment` runs: the base on `dreamscale run yam`;
    a clear error, naming how to run it, on any other robot (and for a custom robot, which no
    `dreamscale run` rig drives)."""
    if _custom(row):
        raise cmd._invalid(
            f"{checkpoint_id} is a Flex-π deployment for a custom robot",
            f'drive it from Python: dreamscale.connect("{NAME}", deployment="{checkpoint_id}")',
            cause=f"`dreamscale run {embodiment.name}` drives {embodiment.label} only",
        )
    if embodiment.name == _YAM:
        return NAME
    raise cmd._invalid(
        f"{checkpoint_id} is a Flex-π deployment for {C.PRESET_LABEL}, not {embodiment.label}",
        f"run it with `dreamscale run {_YAM} --deployment {checkpoint_id}`",
        cause=f"`dreamscale run {embodiment.name}` drives {embodiment.label} only",
    )


def run_command(deployment: dict) -> str:
    """How to run a deployment: `dreamscale run yam`; a custom robot's from Python."""
    if _custom(deployment):
        return f'dreamscale.connect("{NAME}", deployment="{deployment["id"]}")'
    return f"dreamscale run {_YAM} --deployment {deployment['id']}"


EXPORTED = ExportedBase(
    "Flex-π",
    "dreamscale.policy.flexpi_deployment:FlexpiSessionDeployment",
    "dreamscale.policy.flexpi_deployment:runtime_contract",
)
BASE = DeployBase(
    family="flexpi", name=NAME, label="Flex-π", cli=CLI,
    exported=EXPORTED, runner=runner, run_command=run_command, robots=(_YAM,),
    # Its runs' step_N.pt is a torch archive: Detect reads it from the listing's spans
    # (``archives``), and the upload sends only the members a build reads.
    local_archive=True,
    **UNITS.hooks(),
)
