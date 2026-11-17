"""dreamscale deployments — your fine-tunes on a base model, shaped to your robot and
deployed in a region (``dreamscale endpoints`` and ``dreamscale checkpoints`` are the older
names for the same commands).

`deployments create hf://owner/repo` builds a deployment from a Hugging Face fine-tune with
the embodiment it serves: a preset (`--preset bimanual_yam|so101`), the repo's own deployment
adapter (detected), or your own shapes (`--camera key=view`, `--image-size HxW`, `--chunk`,
`--hz`, ...), in `--region <id>` (a region from the server's list, e.g. us-west).
Dreamscale checks the architecture, builds the embodiment from the checkpoint's training stats
and runs it once on a server before it serves.
Run it with `dreamscale.connect("perceptron-isaac05", deployment="ckpt_…")`; a server starts
when a robot connects. Mirrors sessions_cmd.py: async inner + sync wrapper, client closed in
finally.

`--base pi0.5` deploys a π0.5 fine-tune (openpi or LeRobot) instead: a preset robot
(`--preset bimanual_yam|so101|arx5|blank`) or `--camera key=slot`, the checkpoint
(`--path checkpoints/55000`, default the latest), its geometry and its RTC method, each
detected from the repo where it can be and editable. Run it with
`dreamscale.connect("pi0.5", deployment="ckpt_…")`.
"""

from __future__ import annotations

import asyncio
import json
import re
import sys
import time
from collections.abc import Callable
from types import SimpleNamespace
from typing import Any

import httpx
from dreamscale_transport import families as manifest
from rich.text import Text

from dreamscale import deploy_bases, errors, local_checkpoint, tables
from dreamscale.config import load_config
from dreamscale.control import ControlPlaneClient
from dreamscale.deploy_bases import Base  # noqa: F401 - its CLI name
from dreamscale.integrations import hugging_face
from dreamscale.model_names import internal_model, is_account_ref, public_model
from dreamscale.policy.deployment import joint_actions

DEFAULT_MODEL = "perceptron-isaac05-yam"
# A deployment's slug (the control plane's rule): what a bare name must look like to be one.
_SLUG = re.compile(r"[a-z0-9][a-z0-9.-]{1,46}[a-z0-9]")
_DEPLOYMENT_ID = re.compile(r"ckpt_[0-9a-f]{24}")
BASE_MODEL = "perceptron-isaac05"
POLL_S = 5.0
PRESETS = ("bimanual_yam", "so101")
# A region id as the server names them (us-west, japan, …); the server says which are live.
_REGION_ID = re.compile(r"^[a-z][a-z0-9-]{0,30}[a-z0-9]$")
# Where control planes from before regions built every deployment.
DEFAULT_REGION = "us-west"
# `--region auto` (the default): the nearest region the base serves, measured from here.
AUTO_REGION = "auto"
ISAAC = "isaac0.5"
# Every name `--base` takes (aliases too), each base's presets and build steps, and its label:
# one per deployment base (deploy_bases).
_BASE_NAMES = deploy_bases.names()
BASES = {base.name: base.cli for base in deploy_bases.BASES}
BASE_LABELS = {base.name: base.label for base in deploy_bases.BASES}
# A deployment on a base this SDK doesn't know: listed and shown, never as another base's.
UNKNOWN_BASE = Base({"custom": "Custom"}, (
    ("Building", ("building", "resolving", "checking", "downloading", "validating", "sealing",
                  "built")),
    ("Testing on a server", ("qualifying", "ready", "failed")),
), None)
RTC_LABELS = {"off": "off", "test_time": "test-time", "trained": "trained"}
TEST_TIME_NOTE = "test-time RTC adds latency"
OPENPI_RTC_NOTE = (
    "openpi checkpoints don't record RTC training; choose Trained if you trained with "
    "train-time RTC"
)


def parse_base(value: str | None, *, allow_auto: bool = False) -> str:
    """`--base pi0.5` (or `auto`, for inspect); unlisted bases (``deploy_bases``) still
    parse. None: the default base."""
    name = (value or deploy_bases.default().name).strip().lower()
    if allow_auto and name == "auto":
        return "auto"
    if name not in _BASE_NAMES:
        offered = [*deploy_bases.listed(), *(["auto"] if allow_auto else [])]
        choices = f"{', '.join(offered[:-1])} or {offered[-1]}"
        raise ValueError(f"--base is {choices}, got {value!r}")
    return _BASE_NAMES[name]


def downloaded_base(repo: str, path: str | None = None) -> str | None:
    """The base of a folder `dreamscale train download` made (its dreamscale.json names it),
    so its deploy needs no `--base`: a deployment base by name, or the deployment base of the
    training base it names (π0.5 RTC YAM deploys on π0.5). None for a folder that names no
    base; ValueError for one naming a base this SDK doesn't know, never deployed as another."""
    from dreamscale.local_checkpoint import trained_base

    name = (trained_base(repo, path) or "").strip().lower()
    if not name:
        return None
    if name in _BASE_NAMES:
        return _BASE_NAMES[name]
    from dreamscale_transport import families, training_families

    if training_families.is_base(name):
        deploy = families.family(training_families.family_of(name).id).deploy
        if deploy is not None and deploy.public_id in _BASE_NAMES:
            return _BASE_NAMES[deploy.public_id]
    raise ValueError(
        f"this folder was trained on {name!r}, which this dreamscale doesn't deploy: upgrade "
        "dreamscale, or pass --base"
    )


def base_name_of(checkpoint: dict) -> str | None:
    """The base a deployment row runs on (a ``deploy_bases`` name); None for a base this SDK
    doesn't know (a newer control plane's), which is never treated as another base."""
    model = checkpoint.get("base_model") or checkpoint.get("model")
    for base in deploy_bases.BASES:
        if base.claims_model and model == base.name:
            return base.name
    claimed = deploy_bases.claiming(checkpoint)
    if claimed is not None:
        return claimed.name
    named = checkpoint.get("base_model")
    if named is None:
        return ISAAC  # rows from before bases were named are Isaac 0.5's
    return _BASE_NAMES.get(internal_model(str(named)).lower())


def deploy_base_of(checkpoint: dict) -> deploy_bases.DeployBase | None:
    """The base a deployment row runs on; None for one this SDK doesn't know."""
    return deploy_bases.named(base_name_of(checkpoint))


def base_label(checkpoint: dict) -> str:
    name = base_name_of(checkpoint)
    return BASE_LABELS[name] if name else str(checkpoint.get("base_model") or "unknown")


def base_of(checkpoint: dict) -> Base:
    name = base_name_of(checkpoint)
    return BASES[name] if name else UNKNOWN_BASE


def _client(client_factory: Callable[..., Any]):
    config = load_config()
    if not config.api_key:
        raise errors.catalog("not_configured")
    return client_factory(config.control_plane_url, config.api_key)


async def _call(client_factory: Callable[..., Any], method: str, *args, **kwargs) -> Any:
    client = _client(client_factory)
    try:
        return await getattr(client, method)(*args, **kwargs)
    finally:
        await client.close()


def _gb(size: Any) -> str:
    return "—" if not size else f"{size / 1e9:.1f} GB"


def build_steps_for(checkpoint: dict) -> tuple:
    """The build's steps: its base's, as the base that claims the row reads them (π0.5's
    openpi checkpoints skip the LeRobot validation)."""
    steps = base_of(checkpoint).build_steps
    claimed = deploy_bases.claiming(checkpoint)
    if claimed is not None and claimed.row_steps is not None:
        return claimed.row_steps(checkpoint, steps)
    return steps


def build_status(checkpoint: dict, *, now: float) -> tuple[str, str]:
    """The build's step as a label, and as a live line with its elapsed time."""
    base = base_of(checkpoint)
    steps = build_steps_for(checkpoint)
    progress = checkpoint.get("progress") or {}
    phase = progress.get("phase") or "building"
    created = checkpoint.get("created_at")
    elapsed = int(max(0.0, now - created)) if isinstance(created, int | float) else 0
    if phase == "queued":
        # Control planes with a build queue: a build past the organization's limit waits.
        label = "Queued · waiting for a build slot (starts when another build finishes)"
        return label, f"{label}: {elapsed}s elapsed"
    index = next((i for i, (_, phases) in enumerate(steps) if phase in phases), 0)
    label = f"Building · step {index + 1} of {len(steps)} · {steps[index][0]}"
    done, total = progress.get("bytes_done"), progress.get("bytes_total")
    if phase == "downloading" and total:
        label += f" · {done / 1e9:.1f} of {total / 1e9:.1f} GB" if done else f" · {_gb(total)}"
    typical = f" ({base.typical_build})" if base.typical_build else ""
    return label, f"{label}: {elapsed}s elapsed{typical}"


def _printer(
    print_fn: Callable[[str], None], *, header: bool = True,
) -> tuple[Callable[[str], None], bool]:
    """The live terminal printer for the default `print`; whether lines may repeat. Without
    ``header`` when the command has printed lines of its own already."""
    if print_fn is not print:
        return print_fn, False
    from dreamscale.terminal import make_progress_printer

    return make_progress_printer(show_header=header), sys.stdout.isatty()


def _close(printer: Callable[[str], None]) -> None:
    close = getattr(printer, "close", None)
    if close is not None:
        close()


def embodiment_line(embodiment: dict | None) -> str:
    if not embodiment:
        return "—"
    label = {"bimanual_yam": "Bimanual YAM", "so101": "SO-101"}.get(
        embodiment.get("preset"), "Custom"
    )
    cameras = embodiment.get("cameras") or []
    height, width = (embodiment.get("image_size") or [0, 0])[:2]
    width_out = embodiment.get("action_dim")
    out = f"{embodiment.get('executed_actions')} × {width_out}" if width_out else (
        f"{embodiment.get('executed_actions')} steps"
    )
    return (
        f"{label} · {len(cameras)} × {height}×{width} → {out} at "
        f"{embodiment.get('action_hz')} Hz · cameras "
        + ", ".join(f"{c.get('key')}={c.get('view')}" for c in cameras)
    )


def _hz(value: Any) -> str:
    return f"{value:g}" if isinstance(value, int | float) else str(value)


def _cameras_line(cameras: list[dict]) -> str:
    return ", ".join(f"{c.get('key')} → {c.get('slot')}" for c in cameras) or "—"


def non_joint_line(state_dim: Any, action_dim: Any) -> str | None:
    """One line for a π0.5 deployment whose actions aren't joint targets, else None."""
    widths = (state_dim, action_dim)
    if any(type(width) is not int for width in widths) or joint_actions(*widths):
        return None
    return (
        f"State {state_dim} → {action_dim} actions: they aren't joint targets, so this "
        "deployment runs from Python only (no `dreamscale run`), and pauses rather than "
        "holding in place while no action has arrived."
    )


def _widths(embodiment: dict) -> str:
    """`state 14`, or `state 8 → 7` where the actions aren't joint targets."""
    state, actions = embodiment.get("state_dim"), embodiment.get("action_dim")
    if non_joint_line(state, actions) is None:
        return f"state {state}"
    return f"state {state} → {actions}"


def rtc_line(method: str | None, max_delay: Any = None, *, note: bool = True) -> str:
    """`test-time (test-time RTC adds latency)`, `trained (max delay 15)` or `off`."""
    label = RTC_LABELS.get(method or "off", str(method))
    if method == "trained" and max_delay:
        return f"{label} (max delay {max_delay})"
    if method == "test_time" and note:
        return f"{label} ({TEST_TIME_NOTE})"
    return label


def prefix_rtc(checkpoint: dict, *, note: str | None = None) -> str:
    """`trained (prefix up to 4 of 7 actions)` or `off`; ``note`` follows "trained" (FLUX:
    `trained, experimental (…)`)."""
    if checkpoint.get("rtc_method") != "trained":
        return "off"
    label = f"trained, {note}" if note else "trained"
    rows, trained = checkpoint.get("rtc_prefix_rows"), checkpoint.get("trained_rtc_max_delay")
    if rows and trained:
        return f"{label} (prefix up to {rows} of {trained} actions)"
    return label


def robot_line(checkpoint: dict) -> str:
    base = deploy_base_of(checkpoint)
    if base is None:
        return f"{base_label(checkpoint)} (upgrade dreamscale to see its robot)"
    return base.robot_line(checkpoint)


def _ref(checkpoint: dict) -> str:
    """What to type for this deployment: <account>/<slug> (control planes before account
    slugs: its slug; before slugs: its id)."""
    return checkpoint.get("full_slug") or checkpoint.get("slug") or checkpoint["id"]


def _title(checkpoint: dict) -> str:
    """`acme/towel-fold`: its name (older control planes also send a display name)."""
    ref, name = _ref(checkpoint), checkpoint.get("name")
    return ref if name in (None, ref, checkpoint.get("slug")) else f"{ref}  {name}"


def _known_model(name: str) -> bool:
    """A name this SDK knows as a catalog model (never looked up as a deployment)."""
    from dreamscale.embodiments import EMBODIMENTS
    from dreamscale.model_names import PUBLIC_NAMES, resolve_llm_model
    from dreamscale.models_cmd import SHARED_BASE_MODELS, SHARED_MODELS
    from dreamscale.policy.exported_deployments import exported_base
    from dreamscale.policy.runtime.contract import has_runtime_contract

    internal = internal_model(name)
    return (
        internal.lower() in _BASE_NAMES or internal in PUBLIC_NAMES
        or resolve_llm_model(name) != name
        or has_runtime_contract(internal) or internal in SHARED_MODELS
        or internal in SHARED_BASE_MODELS
        or any(internal in robot.policy_models for robot in EMBODIMENTS.values())
        or exported_base(internal) is not None
    )


def is_deployment_ref(name: str) -> bool:
    """``<account>/<slug>`` or a ``ckpt_…`` id: a deployment, never a model."""
    return is_account_ref(name) or bool(_DEPLOYMENT_ID.fullmatch(name or ""))


def may_name_deployment(name: str) -> bool:
    """``<account>/<slug>``, a ``ckpt_…`` id, or a bare slug this SDK doesn't know as a model."""
    return is_deployment_ref(name) or (bool(_SLUG.fullmatch(name)) and not _known_model(name))


def is_own_deployment(name: str, *, client_factory: Callable[..., Any] | None = None) -> bool:
    """Whether a bare name this SDK doesn't know as a model is one of your deployments (when
    it can't tell, the session reports the name)."""
    if not may_name_deployment(name):
        return False
    try:
        asyncio.run(_call(client_factory or ControlPlaneClient, "get_checkpoint", name))
    except (errors.DreamscaleError, httpx.HTTPError):
        return False
    return True


async def resolve_run_ref(
    client: Any, model: str | None, deployment: str | None
) -> tuple[str | None, str | None]:
    """What a model name runs: ``(model, deployment)``. ``<account>/<slug>`` is that
    deployment, on the model it was built on; a bare name this SDK doesn't know as a model
    is your deployment of that slug when you have one, else the model it names."""
    if model is None or deployment is not None or not may_name_deployment(model):
        return model, deployment
    qualified = is_deployment_ref(model)
    try:
        row = await client.get_checkpoint(model)
    except errors.DreamscaleError:
        if qualified:
            raise
        return model, None  # not one of yours: the session reports an unknown model
    return run_base(row), model


def run_base(row: dict) -> str | None:
    """The model a deployment runs on: the runtime of the base that claims its row (π0.5's for
    a π0.5 build), else its base."""
    claimed = deploy_bases.claiming(row)
    base = (manifest.family(claimed.family).deploy.base if claimed is not None
            else internal_model(row.get("model") or ""))
    return base or None


def _id_line(checkpoint: dict) -> list[str]:
    return [f"  id:       {checkpoint['id']}"] if checkpoint.get("slug") else []


def _describe(checkpoint: dict) -> list[str]:
    base = deploy_base_of(checkpoint)
    if base is not None and base.describe is not None:
        return base.describe(checkpoint)
    source = checkpoint.get("source") or {}
    revision = source.get("resolved_revision") or source.get("revision") or "main"
    where = f"hf://{source.get('repo')}@{revision}"
    if source.get("kind") == "official":  # a family's own published checkpoint, by name
        name = str(source.get("repo") or "").removeprefix("official/")
        where = f"official {name} (files {str(revision)[:12]})"
    training = checkpoint.get("training") or {}
    if training.get("run_id"):  # a training run's checkpoint, as π0.5's describe names it
        step = training.get("step")
        where = f"training run {training['run_id']}" + (
            f" · step {step:,}" if isinstance(step, int) else "")
    lines = [
        f"{_title(checkpoint)}  ({checkpoint.get('base_model') or checkpoint['model']})",
        *_id_line(checkpoint),
        f"  robot:    {robot_line(checkpoint)}",
        f"  region:   {region_line(checkpoint)}",
        f"  status:   {checkpoint['status']}"
        + ("  [default]" if checkpoint.get("default") else ""),
        f"  source:   {where}",
        f"  size:     {_gb(checkpoint.get('size_bytes'))}",
    ]
    if checkpoint.get("keep_warm") is not None:
        lines.append(f"  warm:     {keep_warm_line(checkpoint)}")
    if base is not None and base.describe_rtc is not None and checkpoint.get("rtc_method"):
        lines.append(f"  rtc:      {base.describe_rtc(checkpoint)}")
    elif checkpoint.get("rtc_max_prefix_steps") is not None:
        lines.append(f"  rtc:      prefix up to {checkpoint['rtc_max_prefix_steps']} actions")
    error = checkpoint.get("error")
    if error:
        lines += [f"  error:    {error['code']}: {error['message']}", f"  fix:      {error['fix']}"]
    return lines


KEEP_WARM_VALUES = ("off", "10m", "30m", "1h", "2h", "6h", "12h", "always")
# Robots an autoscaling deployment may keep ready (the control plane's limit).
MAX_READY_ROBOTS = 64
_WARM_STATES = {
    "off": "no server held",
    "warming": "starting a warm server",
    "warm": "a server is warm, waiting for a robot",
    "in_use": "in use",
    "replacing": "replacing its server with a fresh one",
    "waiting_for_capacity": "waiting for a server in its region",
    "waiting_for_gpu": "waiting for a GPU",
    "failed": "could not keep a server warm",
}
# An autoscaling deployment's robots kept ready, by what its capacity is doing now (ready
# says nothing more).
_HELD_STATES = {
    "warm": None,
    "in_use": None,
    "warming": "starting",
    # Capacity waits read the same everywhere: "waiting for a GPU".
    "waiting_for_gpu": "waiting for a GPU",
    "off": "none running now",
}


def _robots(count: int) -> str:
    return f"{count} robot{'' if count == 1 else 's'}"


def autoscaling(checkpoint: dict) -> bool:
    """Its robots share capacity that scales by itself (control planes from 0.1.0a155 on)."""
    return checkpoint.get("autoscaling") is True


def robots_line(checkpoint: dict) -> str:
    """An autoscaling deployment's robots now: connected, connecting, or none."""
    warm = checkpoint.get("warm") or {}
    connected, queued = int(warm.get("robots") or 0), int(warm.get("queued") or 0)
    if connected and queued:
        return f"{_robots(connected)} connected, {queued} connecting"
    if connected:
        return f"{_robots(connected)} connected"
    if queued:
        return f"{_robots(queued)} connecting"
    return "none connected"


def not_served(checkpoint: dict) -> tuple[str, str] | None:
    """Why no robot can run this deployment, and what to do, or None. A units-only
    deployment (π0.5, FLUX, ABC-VLA, InternW0, …) its host doesn't serve reads warm.state
    `off` with why, whatever its keep-warm says: the host isn't open to the organization
    (`not_open`), or doesn't run in the deployment's region (`region_unavailable`)."""
    reason = (checkpoint.get("warm") or {}).get("reason")
    if reason == "not_open":
        return ("not open to your organization yet",
                "email team@dreamscalelabs.com to have it opened")
    if reason == "region_unavailable":
        region = region_of(checkpoint)
        partner = checkpoint.get("fallback_region")
        return (f"not served in {region} yet",
                f"create it again in {partner} (--region {partner})" if partner
                else "create it again in a served region")
    return None


def keep_warm_line(checkpoint: dict) -> str:
    """`always — a server is warm, waiting for a robot`, or `off`. Autoscaling deployments
    speak in robots kept ready: `always — 8 robots kept ready around the clock`, with what
    they are doing now when they aren't ready (`(starting)`, `(none running now)`). A
    deployment no robot can run leads with why (not_served)."""
    value = checkpoint.get("keep_warm") or "off"
    if (unserved := not_served(checkpoint)) is not None:
        why, fix = unserved
        return f"{value} — {why}, so nothing is kept ready or billed ({fix})"
    warm = checkpoint.get("warm") or {}
    state = warm.get("state")
    reason = {"no_credits": "out of credits"}.get(warm.get("reason"), warm.get("reason"))
    if autoscaling(checkpoint):
        if value == "off":
            return "off (capacity scales to zero when no robot is connected)"
        ready = int(checkpoint.get("keep_warm_robots") or warm.get("ready_robots") or 1)
        when = "around the clock" if value == "always" else f"for {value} after the last robot"
        # A state this SDK doesn't know yet is named as the control plane sends it.
        held = _HELD_STATES.get(state, state.replace("_", " ") if state else None)
        detail = ", ".join(part for part in (held, reason) if part)
        return f"{value} — {_robots(ready)} kept ready {when}" + (
            f" ({detail})" if detail else ""
        )
    if value == "off" and state in (None, "off"):
        return "off (the server stops when the session ends)"
    described = _WARM_STATES.get(state, state or "")
    return f"{value} — {described}" + (f" ({reason})" if reason else "")


def region_of(checkpoint: dict) -> str:
    # Control planes from before regions built every deployment in us-west.
    return checkpoint.get("region") or DEFAULT_REGION




def region_line(checkpoint: dict) -> str:
    """`us-west (us-east if it's full)`, `us-west only`, or the region alone from a control
    plane that predates region fallback. The partner is the server's (``fallback_region``)."""
    region = region_of(checkpoint)
    fallback = checkpoint.get("region_fallback")
    partner = checkpoint.get("fallback_region") or ("the next-closest region" if fallback else None)
    if not isinstance(fallback, bool) or partner is None:
        return region
    return f"{region} ({partner} if it's full)" if fallback else f"{region} only"


def list_region(checkpoint: dict) -> str:
    """The list's region: `us-west +east` (or `japan +india`) when a server may start in its
    fallback region (the server's ``fallback_region``)."""
    region = region_of(checkpoint)
    partner = checkpoint.get("fallback_region")
    if checkpoint.get("region_fallback") is True and partner:
        stem = region.split("-", 1)[0] + "-" if "-" in region else None
        return f"{region} +{partner.removeprefix(stem) if stem else partner}"
    return region


def parse_region(value: str | None) -> str:
    """`--region <id>`: where the deployment's sessions run, or `auto` (the default), the
    nearest region its base serves (``choose_region``). Any region id is sent as is; the
    server accepts the live ones (and their aliases) and names them when it refuses."""
    region = (value or AUTO_REGION).strip().lower()
    if region != AUTO_REGION and not _REGION_ID.match(region):
        raise ValueError(f"--region is a region id such as us-west, or auto, got {value!r}")
    return region


def _nearest_region(
    client_factory: Callable[..., Any], offered: list[str] | None, print_fn: Callable[[str], None]
) -> str | None:
    """`auto`: the region nearest this machine among ``offered`` (None: every live region),
    from the region record's probes (``GET /v1/regions``), measured in parallel for about a
    second, then decided by the control plane (``region_choice.nearest_region``). None when
    nothing decided it, which the control plane takes as its default region; silent when it
    doesn't list regions (a control plane from before them)."""
    from dreamscale.region_choice import nearest_region

    try:
        listed = asyncio.run(_call(client_factory, "list_regions"))
    except Exception:
        return None
    live = {
        r["id"]: r for r in (listed or {}).get("regions") or ()
        if isinstance(r, dict) and r.get("live") and isinstance(r.get("id"), str)
    }
    names = [r for r in (offered if offered is not None else live) if r in live]
    if not names:
        return None
    if len(names) == 1:
        chosen, how = names[0], "the only region it serves"
    else:
        candidates = [{"region": r, "url": live[r]["probe_url"]} for r in names
                      if live[r].get("probe_url")]
        nearest = nearest_region(
            candidates,
            ask=lambda measurements: asyncio.run(
                _call(client_factory, "resolve_region", measurements=measurements, offered=names)
            ),
            allowed=names,
        )
        chosen = nearest.region if nearest else None
        how = (
            f"nearest to {nearest.location}"
            if nearest and nearest.source == "location" and nearest.location
            else "nearest to this machine"
        )
    if chosen is None:
        print_fn("Region: the server's default (nothing measured from here; choose one with "
                 "--region).")
        return None
    print_fn(f"Region: {live[chosen].get('label') or chosen} ({how}; choose another with "
             "--region).")
    return chosen


def parse_cameras(values: list[str] | None) -> list[dict] | None:
    """`--camera key=view` (repeatable, in the order the robot sends them)."""
    if not values:
        return None
    cameras = []
    for value in values:
        key, sep, view = value.partition("=")
        if not sep or not key.strip() or not view.strip():
            raise ValueError(f"--camera takes key=view (e.g. wrist_cam=wrist), got {value!r}")
        cameras.append({"key": key.strip(), "view": view.strip()})
    return cameras


def parse_image_size(value: str | None) -> list[int] | None:
    """`--image-size HxW` (height first, as the model's image_hw)."""
    if not value:
        return None
    height, sep, width = value.lower().partition("x")
    if not sep or not height.isdigit() or not width.isdigit():
        raise ValueError(f"--image-size takes HEIGHTxWIDTH (e.g. 360x640), got {value!r}")
    return [int(height), int(width)]


def build_embodiment(
    *,
    preset: str | None,
    detected: dict | None,
    cameras: list[dict] | None = None,
    image_size: list[int] | None = None,
    action_dim: int | None = None,
    state_dim: int | None = None,
    chunk: int | None = None,
    hz: float | None = None,
    dataset: str | None = None,
    context: int | None = None,
) -> dict:
    """A preset or the repo's detected embodiment, with any flags on top (the control
    plane fills a preset's fields; editing any of them makes the embodiment custom)."""
    if preset not in (None, "custom", *PRESETS):
        raise ValueError(f"--preset is one of {', '.join(PRESETS)} or custom")
    base: dict = {"preset": preset} if preset in PRESETS else dict(detected or {})
    overrides = {
        "cameras": cameras, "image_size": image_size, "action_dim": action_dim,
        "state_dim": state_dim, "executed_actions": chunk, "action_hz": hz,
        "dataset": dataset, "n_obs_steps": context,
    }
    embodiment = {**base, **{k: v for k, v in overrides.items() if v is not None}}
    if dataset is not None and dataset != base.get("dataset"):
        # Another dataset has its own stats entries; the detected scope no longer applies.
        embodiment.pop("normalization_scope", None)
    if preset == "custom" or (preset not in PRESETS and embodiment):
        embodiment["preset"] = "custom"
    if not embodiment.get("preset") or (
        embodiment["preset"] == "custom"
        and not all(embodiment.get(k) for k in ("cameras", "image_size", "dataset"))
    ):
        raise ValueError(
            "name the robot: --preset bimanual_yam|so101, or a repo with a deployment "
            "adapter, or --camera key=view ... --image-size HxW --dataset NAME"
        )
    return embodiment


def detect_embodiment(
    *,
    repo: str,
    revision: str | None,
    hf_token: str | None,
    client_factory: Callable[..., Any] = ControlPlaneClient,
) -> dict | None:
    token = hugging_face.token(hf_token)
    _, found = _inspect_with_status(client_factory, repo, revision, token, print)
    return found.get("detected")


def _inspect_with_status(
    client_factory: Callable[..., Any],
    repo: str,
    revision: str | None,
    token: str | None,
    print_fn: Callable[[str], None],
    *,
    base: str = ISAAC,
    path: str | None = None,
) -> tuple[str, dict]:
    """Inspect, with a ticking line while the repo is read (a cold read takes a while).
    Returns the base the repo was read as, and what the server found."""
    printer, _ = _printer(print_fn)
    try:
        printer(
            f"Reading {repo}'s deployment adapter and training stats: 0s elapsed"
            if base == ISAAC
            else f"Reading {repo}'s checkpoint and training stats: 0s elapsed"
        )
        return asyncio.run(_inspect_as(client_factory, repo, revision, token, base, path))
    finally:
        if printer is not print_fn:
            _close(printer)


def _inspect_local(
    client_factory: Callable[..., Any],
    folder: local_checkpoint.LocalFolder,
    print_fn: Callable[[str], None],
    *,
    path: str | None = None,
    base: str | None = None,
) -> dict:
    """Detect on a local folder's listing (nothing is uploaded yet), as ``base`` (default: the
    default base, by the name its sessions open)."""
    body = local_checkpoint.listing(folder)
    if _local_archive(base):
        body["archives"] = local_checkpoint.archives(folder)
    printer, _ = _printer(print_fn)
    try:
        printer(f"Reading {folder.root}'s checkpoint: 0s elapsed")
        return asyncio.run(_call(
            client_factory, "inspect_endpoint_repo", None, model=base or _default_public_id(),
            local=body,
            **({"path": path} if path else {}),
        ))
    except errors.DreamscaleError as error:
        # An older control plane asks for a repo: it can't read a local folder.
        if error.code == "invalid_request" and "repo" in str(error):
            raise errors.catalog("local_folders_unavailable") from None
        raise
    finally:
        if printer is not print_fn:
            _close(printer)


def _upload_checkpoint(
    client_factory: Callable[..., Any],
    folder: local_checkpoint.LocalFolder,
    found: dict,
    print_fn: Callable[[str], None],
    *, base_model: str | None = None,
) -> str:
    """Upload the files Detect named (a re-run sends nothing new); the upload's id. An
    ABC-VLA checkpoint's are members of its ``.pt``, each sent as its own blob."""
    from dreamscale.train_cmd import upload_folder

    slices = {}
    if _local_archive(base_model):
        files, slices = local_checkpoint.upload_plan(folder, found)
    else:
        files = local_checkpoint.upload_files(folder, found)
    local = SimpleNamespace(
        root=folder.root, files=tuple(files), bytes=sum(size for _, size in files),
        slices=slices,
    )
    return upload_folder(client_factory, local, print_fn=print_fn, kind="checkpoint",
                         **({"base_model": base_model} if base_model is not None else {}))


def _may_be_another_base(error: errors.DreamscaleError) -> bool:
    """A π0.5 refusal that another base might read (not auth, credits or an outage)."""
    return not (
        isinstance(error, errors.AuthError | errors.CreditsError | errors.ServerError)
        or error.code in ("rate_limited", "deployments_unavailable")
    )


async def _inspect_as(
    client_factory: Callable[..., Any],
    repo: str,
    revision: str | None,
    token: str | None,
    base: str,
    path: str | None,
) -> tuple[str, dict]:
    client = _client(client_factory)
    try:
        if _detects_as_base(base):
            return base, await client.inspect_endpoint_repo(
                repo, revision=revision, hf_token=token, model=base,
                **({"path": path} if path is not None else {}),
            )
        if base == ISAAC:
            return ISAAC, await client.inspect_endpoint_repo(
                repo, revision=revision, hf_token=token
            )
        # Any other (auto too): the Detect of the base named, if it has one, else the
        # default base's.
        chosen = deploy_bases.named(base)
        if chosen is None or chosen.inspect is None:
            chosen = deploy_bases.default()
        return await chosen.inspect(client, repo, revision, token, base, path)
    finally:
        await client.close()


_FIELD_LABELS = {
    "preset": "preset",
    "cameras": "cameras",
    "state_dim": "state width",
    "action_dim": "action width",
    "action_horizon": "horizon",
    "executed_actions": "executed actions",
    "action_hz": "rate",
    "token_length": "prompt tokens",
    "state_in_prompt": "state in prompt",
    "delta_action_mask": "delta actions",
    "image_resize": "image resize",
    "trained_rtc_max_delay": "trained RTC delay",
    "asset_id": "robot unit conversion",
}


def _field_value(field: str, value: Any) -> str:
    if field == "cameras" and isinstance(value, list):
        return _cameras_line(value)
    if field == "action_hz" and isinstance(value, int | float):
        return f"{value:g} Hz"
    if field == "delta_action_mask":
        if not value:
            return "none (absolute actions)"
        return f"{sum(bool(v) for v in value)} of {len(value)} dimensions"
    if field == "normalization" and isinstance(value, dict):
        if value.get("kind") == "openpi":
            return f"openpi quantile statistics (asset {value.get('asset_id')})"
        modes = [
            f"{part} {(value.get(part) or {}).get('mode', '?')}" for part in ("state", "action")
        ]
        return "the checkpoint's own statistics: " + ", ".join(modes)
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, dict | list):
        return json.dumps(value, separators=(",", ":"))
    return str(value)


def _checkpoint_paths(found: dict) -> list[dict]:
    return [c for c in found.get("checkpoints") or [] if isinstance(c, dict)]


def latest_checkpoint(found: dict) -> str | None:
    """The newest checkpoint path in the repo (highest step), as the build's default."""
    checkpoints = _checkpoint_paths(found)
    if not checkpoints:
        return None
    newest = max(
        checkpoints, key=lambda c: c.get("step") if isinstance(c.get("step"), int) else -1
    )
    return newest.get("path")


def _rtc_autofill_lines(found: dict) -> list[str]:
    rtc = found.get("rtc") or {}
    method = rtc.get("method")
    if not method:
        return []
    source = f" ({rtc['source']})" if rtc.get("source") else ""
    lines = [f"RTC: {rtc_line(method, rtc.get('max_delay'), note=False)}{source}"]
    if method == "test_time":
        lines.append(f"  {TEST_TIME_NOTE[0].upper()}{TEST_TIME_NOTE[1:]}.")
        if found.get("format") == "openpi":
            lines.append(f"  {OPENPI_RTC_NOTE}.")
    return lines


def run_inspect(
    *,
    repo: str,
    revision: str | None = None,
    hf_token: str | None = None,
    json_output: bool = False,
    base: str = "auto",
    path: str | None = None,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
) -> dict:
    if _detects_as_base(base):
        folder = _local_source(repo, base)
        if folder:
            found = _inspect_local(client_factory, folder, print_fn, path=path, base=base)
        else:
            _, found = _inspect_with_status(
                client_factory, repo, revision, hugging_face.token(hf_token), print_fn,
                base=base, path=path,
            )
        if json_output:
            print_fn(json.dumps(found, indent=2, sort_keys=True))
        elif deploy_bases.named(base).found_lines is not None:
            for line in deploy_bases.named(base).found_lines(found):
                print_fn(line)
        else:
            print_fn(robot_line({"base_model": base, "embodiment": found.get("detected")}))
        return found
    if local_checkpoint.is_local_folder(repo):
        folder = local_checkpoint.scan(repo)
        found = _inspect_local(
            client_factory, folder, print_fn if not json_output else (lambda _: None), path=path
        )
        if json_output:
            print_fn(json.dumps(found, indent=2, sort_keys=True))
            return found
        print_fn(f"{folder.root}:")
        for line in deploy_bases.default().found_lines(found):
            print_fn(line)
        return found
    token = hugging_face.token(hf_token)
    if json_output:
        _, found = asyncio.run(_inspect_as(client_factory, repo, revision, token, base, path))
        print_fn(json.dumps(found, indent=2, sort_keys=True))
        return found
    read_as, found = _inspect_with_status(
        client_factory, repo, revision, token, print_fn, base=base, path=path
    )
    reader = deploy_bases.named(read_as)
    if reader is not None and reader.found_lines is not None:
        for line in reader.found_lines(found):
            print_fn(line)
        return found
    detected = found.get("detected")
    if detected:
        print_fn(f"Declared embodiment: {embodiment_line({**detected, 'preset': 'custom'})}")
        print_fn(f"  robot unit conversion: {detected.get('dataset')}")
    else:
        print_fn("The repo has no deployment adapter; pick a preset or give the shapes.")
    datasets = found.get("datasets") or []
    print_fn(
        f"{len(datasets)} robot unit conversions (normalization statistics, by dataset)"
        + (
            ": " + ", ".join(
                f"{d['dataset']} ({d['action_dim']} actions · {d['state_dim']} state)"
                for d in datasets[:8]
            )
            if datasets
            else ""
        )
    )
    return found


def run_add(
    *,
    repo: str | None,
    model: str = DEFAULT_MODEL,
    revision: str | None = None,
    name: str | None = None,
    hf_token: str | None = None,
    embodiment: dict | None = None,
    region: str | None = None,
    wait: bool = True,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
    sleep: Callable[[float], None] = time.sleep,
    shown: str | None = None,
    **pi05: Any,
) -> dict:
    """``pi05``: a π0.5 deployment's ``source_path``, ``rtc_method`` and ``rtc_max_delay``
    (a local folder's: ``upload_id`` and ``source_format`` instead of a repo, ``shown`` the
    folder)."""
    token = hugging_face.token(hf_token) if repo is not None else None
    if region == AUTO_REGION:
        region = _check_region(client_factory, model, model, region, print_fn=print_fn)
    checkpoint = asyncio.run(
        _call(
            client_factory,
            "add_checkpoint",
            model,
            repo,
            revision=revision,
            name=name,
            hf_token=token,
            embodiment=embodiment,
            **({"region": region} if region is not None else {}),
            **{key: value for key, value in pi05.items() if value is not None},
        )
    )
    print_fn(
        f"Building {_ref(checkpoint)} (deployment) from {shown or repo} for "
        f"{robot_line(checkpoint)} in {region_of(checkpoint)} "
        "(one-time build: download, convert, server check)."
    )
    return follow_build(
        checkpoint, wait=wait, client_factory=client_factory, print_fn=print_fn, sleep=sleep
    )


def follow_build(
    checkpoint: dict,
    *,
    wait: bool = True,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
    sleep: Callable[[float], None] = time.sleep,
) -> dict:
    """Follow a deployment's build to ready or failed on one live line, then describe it."""
    if not wait:
        return checkpoint
    printer, live = _printer(print_fn)
    last = None
    try:
        while checkpoint["status"] == "building":
            label, line = build_status(checkpoint, now=time.time())
            # A terminal redraws one ticking line; logs get a line per step (not per GB).
            step = label.split(" · ")[:3]
            if live or step != last:
                printer(line)
                last = step
            sleep(POLL_S)
            checkpoint = asyncio.run(_call(client_factory, "get_checkpoint", checkpoint["id"]))
    finally:
        if printer is not print_fn:
            _close(printer)
    if checkpoint["status"] == "ready":
        print_fn(f"✓ Ready: {_ref(checkpoint)} serves {robot_line(checkpoint)}.")
    for line in _describe(checkpoint):
        print_fn(line)
    return checkpoint


_RTC_NAMES = {"off": "off", "test-time": "test_time", "test_time": "test_time",
              "trained": "trained"}
# --delta-mask none: absolute actions, whatever the repo suggested.
CLEAR = "none"


def _invalid(problem: str, fix: str, cause: str = "the deployment's settings") -> Exception:
    return errors.DreamscaleError(
        errors.ErrorInfo(code="invalid_deployment", problem=problem, cause=cause, fix=fix)
    )


def parse_rtc(value: str | None) -> str | None:
    """`--rtc off|test-time|trained` as the API's method (off, test_time, trained)."""
    if value is None:
        return None
    method = _RTC_NAMES.get(value.strip().lower())
    if method is None:
        raise ValueError(f"--rtc is off, test-time or trained, got {value!r}")
    return method


def parse_delta_mask(value: str | None) -> list[bool] | str | None:
    """`--delta-mask 1,1,1,1,1,1,0,…` (1 = that action is relative to the state), or none."""
    if value is None:
        return None
    if value.strip().lower() == CLEAR:
        return CLEAR
    names = {"1": True, "true": True, "t": True, "0": False, "false": False, "f": False}
    try:
        return [names[part.strip().lower()] for part in value.split(",")]
    except KeyError:
        raise ValueError(
            f"--delta-mask takes one 1 or 0 per action dimension, comma separated, or none; "
            f"got {value!r}"
        ) from None


def _check_region(client_factory: Callable[..., Any], model: str, label: str, region: str,
                  *, print_fn: Callable[[str], None] = print) -> str | None:
    """The region to build in: one the control plane offers this base's deployments in (its
    ``bases`` list them; a control plane that names none builds in us-west only, as before),
    or for ``auto`` the nearest of those (``_nearest_region``; None: the server's default)."""
    if region == DEFAULT_REGION:
        return region
    offered = None
    try:
        listed = asyncio.run(_call(client_factory, "list_checkpoints", None))
    except Exception:
        if region == AUTO_REGION:
            return None  # the server's default; its create says what's wrong, if anything
        raise
    for base in listed.get("bases") or []:
        if isinstance(base, dict) and base.get("id") == model and base.get("regions"):
            offered = list(base["regions"])
    if region == AUTO_REGION:
        return _nearest_region(client_factory, offered, print_fn)
    regions = offered or [DEFAULT_REGION]
    if region not in regions:
        raise _invalid(
            f"{label} deployments can't run in {region} yet",
            f"create it in {' or '.join(regions)} with --region",
        )
    return region


def _default_public_id() -> str:
    """The name the default base's sessions (and Detect) open it by."""
    return manifest.family(deploy_bases.default().family).deploy.public_id


def _detects_as_base(name: str | None) -> bool:
    """Detect reads a repo as this base (``model=<name>``), never π0.5 or Isaac 0.5's guess."""
    base = deploy_bases.named(name)
    return base is not None and base.detects_as_base


def _local_archive(name: str | None) -> bool:
    """A single local checkpoint file is a source for this base, beside a folder."""
    base = deploy_bases.named(name)
    return base is not None and base.local_archive


def _local_source(repo: str, base: str) -> local_checkpoint.LocalFolder | None:
    """A local folder (or, for a base that takes one, a single checkpoint file), else None (a
    Hub repo)."""
    if local_checkpoint.is_local_folder(repo):
        return local_checkpoint.scan(repo)
    if _local_archive(base) and local_checkpoint.is_local_archive(repo):
        return local_checkpoint.scan_archive(repo)
    return None


def parse_feature_cameras(values: list[str] | None) -> list[dict] | None:
    """`--camera key=feature` (repeatable, in the checkpoint's camera order): the robot's
    camera name, and the checkpoint camera it fills."""
    if not values:
        return None
    cameras = []
    for value in values:
        key, sep, feature = value.partition("=")
        key, feature = key.strip(), feature.strip()
        if not sep or not key or not feature:
            raise ValueError(
                f"--camera takes key=feature, the robot's camera and the checkpoint camera it "
                f"fills (e.g. wrist_cam=left), got {value!r}"
            )
        cameras.append({"key": key, "feature": feature})
    return cameras


# `dreamscale run <robot>` and the π0.5 preset robot it drives.
RUNNER_PRESETS = {"yam": "bimanual_yam", "so101": "so101"}
# Robots `dreamscale run` drives with custom π0.5 deployments only: fine-tunes on a LeRobot
# recording of that robot, whose cameras keep the recording's names (Embodiment.recording_keys).
RECORDED_RUNNERS = frozenset({"ur", "xarm7", "openarm"})


def _recorded_on(
    embodiment: Any, cameras: tuple[str, ...], state_dim: Any, action_dim: Any
) -> bool:
    """A custom π0.5 deployment fine-tuned on a recording of this robot: its cameras and
    joint targets of its width (Embodiment.records)."""
    return (
        embodiment.name in RECORDED_RUNNERS
        and state_dim == action_dim
        and type(state_dim) is int
        and embodiment.records(cameras, state_dim)
    )


def deployment_model_for_robot(
    embodiment: Any,
    checkpoint_id: str,
    model: str | None,
    *,
    client_factory: Callable[..., Any] | None = None,
) -> str | None:
    """The model `dreamscale run <robot> --deployment ckpt_…` runs: ``pi05`` for a π0.5
    deployment of this robot, the caller's (or else the deployment's own) for Isaac 0.5,
    the base for an ABC-VLA or FLUX 3 Action deployment of this robot, and a clear error,
    naming the way to run it, for a deployment of another robot."""
    row = asyncio.run(
        _call(client_factory or ControlPlaneClient, "get_checkpoint", checkpoint_id)
    )
    base = deploy_base_of(row)
    if base is None or base.runner is None:
        raise _invalid(
            f"{checkpoint_id} is a {base_label(row)} deployment, which `dreamscale run` "
            "doesn't drive",
            f'run it from Python: dreamscale.connect(deployment="{checkpoint_id}")',
        )
    return base.runner(embodiment, checkpoint_id, row, model)


def parse_on_off(value: str) -> bool:
    """`on` or `off` (also true/false, yes/no)."""
    answer = value.strip().lower()
    if answer in ("on", "true", "yes"):
        return True
    if answer in ("off", "false", "no"):
        return False
    raise ValueError(f"use on or off, got {value!r}")


def run_fallback(
    *,
    checkpoint_id: str,
    on: bool,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
) -> dict:
    """Whether a deployment's server may start in the next-closest region when its own is
    full (its next server; no rebuild)."""
    row = asyncio.run(
        _call(client_factory, "set_deployment_region_fallback", checkpoint_id, on)
    )
    region = region_of(row)
    partner = row.get("fallback_region") or "the next-closest region"
    print_fn(
        f"{_ref(row)}: if {region} is full, its server starts in {partner} "
        "(each request then takes longer: it's farther from your robot)." if on else
        f"{_ref(row)}: its server only ever starts in {region}, and a robot waits there when "
        f"{region} is full."
    )
    print_fn(f"  region:   {region_line(row)}")
    return row


def run_rtc(
    *,
    checkpoint_id: str,
    method: str,
    max_delay: int | None = None,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
) -> dict:
    """Change a deployment's RTC method for its new sessions (no rebuild), as its base allows."""
    method = parse_rtc(method) or "off"
    row = asyncio.run(_call(client_factory, "get_checkpoint", checkpoint_id))
    base = deploy_base_of(row)
    if base is None or base.set_rtc is None:
        raise _invalid(
            f"{checkpoint_id} is a {base_label(row)} deployment, which has no RTC setting",
            base.rtc_refusal_fix if base is not None else "nothing to change: its base fixes RTC",
        )
    return base.set_rtc(row, checkpoint_id, method, max_delay, client_factory, print_fn)


def _set_prefix_rtc(row, checkpoint_id, method, prefix, client_factory, print_fn, *,
                    label, bound=None, describe=prefix_rtc,
                    untrained_fix="it runs RTC off") -> dict:
    """A base whose RTC is off, or trained with a prefix cap (``--max-delay``; by default the
    server's) within the prefixes its checkpoint was trained on (and ``bound``, the most a
    request carries). ``label`` names the base in refusals."""
    trained = row.get("trained_rtc_max_delay") or 0
    most = min(trained, bound) if bound else trained
    if method == "test_time":
        raise _invalid(f"{label} runs RTC off or trained", "use off or trained")
    if method == "trained" and not trained:
        raise _invalid(f"{checkpoint_id}'s checkpoint records no prefix training", untrained_fix)
    if method == "off" and prefix is not None:
        raise _invalid("--max-delay is trained RTC's prefix cap", "use it with trained")
    if prefix is not None and not 1 <= prefix <= most:
        raise _invalid(f"the prefix cap is 1-{most} actions (what the checkpoint was trained "
                       "on)", f"pass --max-delay 1-{most}")
    result = asyncio.run(
        _call(client_factory, "set_deployment_rtc", checkpoint_id, method, max_delay=prefix)
    )
    print_fn(
        f"{checkpoint_id}: RTC {describe({**row, **result})} for new sessions. An idle "
        "server is replaced now; one a robot is on when the robot disconnects."
    )
    return result


def run_list(
    *,
    model: str | None = None,
    json_output: bool = False,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
) -> dict:
    listed = asyncio.run(_call(client_factory, "list_checkpoints", model))
    if json_output:
        print_fn(json.dumps(listed, indent=2, sort_keys=True))
        return listed
    for line in list_lines(listed):
        print_fn(line)
    return listed


# A deployment's status as `deployments list` shows it: (label, tables kind).
_LIST_STATUSES = {"ready": ("Ready", "ok"), "building": ("Building", "active"),
                  "failed": ("Failed", "bad")}


def _list_robot(checkpoint: dict) -> Text:
    """The robot preset; a custom robot adds its widths (`Custom · state 8 → 7`)."""
    if base_name_of(checkpoint) is None:
        return tables.dim("upgrade dreamscale to see it")
    spec = checkpoint.get("embodiment") or {}
    label = base_of(checkpoint).presets.get(spec.get("preset"), "Custom")
    robot = Text(label)
    if label == "Custom" and spec.get("state_dim") is not None:
        robot.append(f" · {_widths(spec)}", style=tables.DIM)
    return robot


def _list_actions(checkpoint: dict) -> Text:
    """`20/30 @ 30 Hz`: actions executed of each chunk, at the action rate."""
    spec = checkpoint.get("embodiment") or {}
    executed, horizon, hz = (spec.get("executed_actions"), spec.get("action_horizon"),
                             spec.get("action_hz"))
    if not hz or not (executed or horizon):
        return tables.none()
    if executed and horizon and executed != horizon:
        return Text.assemble(str(executed), (f"/{horizon}", tables.DIM), f" @ {_hz(hz)} Hz")
    return Text(f"{horizon or executed} @ {_hz(hz)} Hz")


def _list_rtc(checkpoint: dict) -> Text:
    """off, trained or test-time (yellow: it adds latency); a dash where the base has none."""
    method = checkpoint.get("rtc_method")
    base = deploy_base_of(checkpoint)
    if not method or base is None or not base.shows_rtc:
        return tables.none()
    label = RTC_LABELS.get(method, str(method))
    return Text(label, style={"off": tables.DIM, "test_time": "yellow"}.get(method, ""))


def list_lines(listed: dict, *, color: bool | None = None, width: int | None = None) -> list[str]:
    checkpoints = listed.get("checkpoints") or []
    base_defaults = listed.get("base_default") or []
    if not checkpoints:
        return ["Deployments", "  None yet. Create one: dreamscale deployments create "
                "hf://owner/repo"]
    # One account (the usual case) is named once in the title; its bare names work anywhere.
    accounts = {c["full_slug"].split("/")[0] for c in checkpoints if c.get("full_slug")}
    one_account = len(accounts) == 1 and all(c.get("full_slug") for c in checkpoints)
    columns = [
        tables.Column("DEPLOYMENT", style="bold"),
        tables.Column("BASE", drop=3),
        tables.Column("ROBOT", drop=1),
        tables.Column("ACTIONS", drop=2),
        tables.Column("RTC", drop=4),
        tables.Column("REGION", drop=5, style=tables.DIM),
        tables.Column("STATUS"),
    ]
    rows = []
    for checkpoint in checkpoints:
        name = Text(checkpoint.get("slug") if one_account else _ref(checkpoint))
        if checkpoint.get("default"):
            name.append(" ★", style=f"not bold {tables.BRAND}")
        warm = checkpoint.get("keep_warm") or "off"
        label, kind = _LIST_STATUSES.get(checkpoint["status"],
                                          (str(checkpoint["status"]).capitalize(), "idle"))
        rows.append([
            name, base_label(checkpoint), _list_robot(checkpoint), _list_actions(checkpoint),
            _list_rtc(checkpoint), list_region(checkpoint),
            tables.status(label, kind, f"warm {warm}" if warm != "off" else ""),
        ])
    notes = ["Base weights are always available as ", tables.command("base")]
    if any(c.get("default") for c in checkpoints):
        notes += ["   ·   ", Text("★", style=tables.BRAND), " its model's default"]
    for base_model in base_defaults:
        notes.append(f"   ·   {public_model(base_model)} defaults to base")
    footer = [
        tables.hint(*notes),
        tables.hint("Details: ", tables.command("dreamscale deployments show <deployment>")),
    ]
    detail = f"{len(checkpoints)} in {next(iter(accounts))}" if one_account else \
        str(len(checkpoints))
    return tables.render("Deployments", detail, columns, rows, footer=footer, color=color,
                         width=width)


def run_show(
    *,
    checkpoint_id: str,
    json_output: bool = False,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
) -> dict:
    """A deployment's status, build progress or error; ``json_output`` prints it as the API
    answers it (``status``, and ``warm.state`` while it's kept warm), for a program to read."""
    checkpoint = asyncio.run(_call(client_factory, "get_checkpoint", checkpoint_id))
    if json_output:
        print_fn(json.dumps(checkpoint, indent=2, sort_keys=True))
        return checkpoint
    for line in _describe(checkpoint):
        print_fn(line)
    if checkpoint["status"] == "building":
        print_fn(build_status(checkpoint, now=time.time())[1])
    return checkpoint


async def _use(client_factory: Callable[..., Any], checkpoint: str, model: str | None) -> dict:
    client = _client(client_factory)
    try:
        if model is None:
            # A checkpoint belongs to one model; `base` without --model means the default model.
            model = (
                DEFAULT_MODEL
                if checkpoint == "base"
                else (await client.get_checkpoint(checkpoint))["model"]
            )
        return await client.set_default_checkpoint(model, checkpoint)
    finally:
        await client.close()


def run_use(
    *,
    checkpoint: str,
    model: str | None = None,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
) -> dict:
    result = asyncio.run(_use(client_factory, checkpoint, model))
    model = result.get("model", model)
    chosen = result["checkpoint"]
    print_fn(
        f"Saved {'the base weights' if chosen == 'base' else chosen} as the {public_model(model)} "
        "default. Sessions run a deployment only when they name it (--deployment ckpt_…)."
    )
    return result


def run_rename(
    *,
    checkpoint_id: str,
    slug: str,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
) -> dict:
    """A deployment's name is its slug: rename it (the old name keeps naming it until another
    deployment takes it)."""
    result = asyncio.run(
        _call(client_factory, "rename_deployment", checkpoint_id, slug=slug)
    )
    print_fn(f"Renamed {checkpoint_id} to {_ref(result) if result.get('id') else slug}.")
    if not checkpoint_id.startswith("ckpt_"):
        print_fn(f"{checkpoint_id} still names it until another deployment takes that name.")
    return result


def run_rm(
    *,
    checkpoint_id: str,
    yes: bool = False,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
    confirm_fn: Callable[..., bool] | None = None,
    interactive: bool | None = None,
) -> dict:
    """Delete a deployment for good, after one question (``yes``: without asking; with no
    terminal to ask in, only with ``yes``), as ``train rm`` does."""
    from dreamscale.train_cmd import _confirm_required, ask

    interactive = sys.stdin.isatty() if interactive is None else interactive
    if not yes:
        row = asyncio.run(_call(client_factory, "get_checkpoint", checkpoint_id))
        print_fn(
            f"{_ref(row)}: this can't be undone. Robots running it now are disconnected, and "
            "its name is free for another deployment."
        )
        if not interactive:
            raise _confirm_required("Deleting a deployment")
        if not (confirm_fn or ask)(f"Delete {_ref(row)} permanently?", default=False):
            print_fn("Not deleted.")
            return row
    result = asyncio.run(_call(client_factory, "delete_checkpoint", checkpoint_id))
    if "stopped" in result:
        print_fn(f"Deleted deployment {checkpoint_id} permanently; its running sessions ended.")
    else:  # an older control plane leaves its sessions running
        print_fn(f"Removed deployment {checkpoint_id}; running sessions keep it until they end.")
    return result


def run_keep_warm(
    *,
    checkpoint_id: str,
    keep_warm: str,
    take_over_from: str | None = None,
    robots: int | None = None,
    now: bool = False,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
    sleep: Callable[[float], None] = time.sleep,
) -> dict:
    if keep_warm not in KEEP_WARM_VALUES:
        raise ValueError(f"keep-warm must be one of {', '.join(KEEP_WARM_VALUES)}")
    if robots is not None and not 1 <= robots <= MAX_READY_ROBOTS:
        raise ValueError(f"--robots is 1 to {MAX_READY_ROBOTS}")
    if now and keep_warm == "off":
        raise ValueError("--now starts a server that keep-warm holds: use 10m … always")
    result = asyncio.run(
        _call(
            client_factory,
            "set_deployment_keep_warm",
            checkpoint_id,
            keep_warm,
            take_over_from=take_over_from,
            **({"robots": robots} if robots is not None else {}),
            **({"now": True} if now else {}),
        )
    )
    _keep_warm_lines(result, checkpoint_id, keep_warm, take_over_from, print_fn,
                     now=now and "warm_now" in result)
    if not now or not_served(result) is not None:  # nothing would ever start: don't wait
        return result
    if "warm_now" not in result:
        print_fn("  This control plane doesn't warm up ahead yet: the first robot to connect "
                 "starts it.")
        return result
    return follow_warm_up(result, client_factory=client_factory, print_fn=print_fn, sleep=sleep)


# What a deployment warming up now is doing, while the CLI waits (warm.state).
_WARMING_LINES = {
    "waiting_for_gpu": "Waiting for a GPU",
    "waiting_for_capacity": "Waiting for a server in its region",
}
_WARM_READY = ("warm", "in_use")
WARM_POLL_S = 2.0
# The CLI stops waiting after this long (the server keeps starting): a capacity wait can
# outlast any terminal.
WARM_WAIT_S = 15 * 60.0


def follow_warm_up(
    checkpoint: dict,
    *,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
    sleep: Callable[[float], None] = time.sleep,
    clock: Callable[[], float] = time.monotonic,
) -> dict:
    """Wait for a deployment warmed up now to be ready, on one live line. Ctrl-C stops the
    waiting, never the server. A failure, the request's window ending (timed on this
    computer's clock from the answer), or WARM_WAIT_S says so and stops waiting."""
    started = clock()
    request = checkpoint.get("warm_now") or {}
    window_s = (
        float(request["until"]) - float(request["requested_at"])
        if request.get("until") is not None and request.get("requested_at") is not None
        else None
    )
    limit_s = min(WARM_WAIT_S, window_s) if window_s is not None else WARM_WAIT_S
    printer, live = _printer(print_fn, header=False)  # after keep-warm's own lines
    last = None
    try:
        while (state := (checkpoint.get("warm") or {}).get("state")) not in _WARM_READY:
            waited = clock() - started
            if state == "failed" or waited >= limit_s:
                print_fn(f"Not ready after {int(waited)}s: {keep_warm_line(checkpoint)}.")
                print_fn(f"  It keeps trying. Check it with: dreamscale deployments show "
                         f"{_ref(checkpoint)}")
                return checkpoint
            line = _WARMING_LINES.get(state, "Starting")
            if live or line != last:
                printer(f"{line}… {int(waited)}s")
                last = line
            sleep(WARM_POLL_S)
            checkpoint = {
                **asyncio.run(_call(client_factory, "get_checkpoint", checkpoint["id"])),
                "warm_now": request,
            }
    except KeyboardInterrupt:
        print_fn(f"Stopped waiting; {_ref(checkpoint)} keeps starting. Check it with: "
                 f"dreamscale deployments show {_ref(checkpoint)}")
        return checkpoint
    finally:
        if printer is not print_fn:
            _close(printer)
    print_fn(f"✓ Ready in {int(clock() - started)}s: {_ref(checkpoint)} answers its first "
             "robot without a cold start.")
    return checkpoint


def _keep_warm_lines(
    result: dict, checkpoint_id: str, keep_warm: str, take_over_from: str | None,
    print_fn: Callable[[str], None], *, now: bool = False,
) -> None:
    if (unserved := not_served(result)) is not None:
        # Saved, but nothing runs (nor bills) until its host serves it: lead with why.
        why, fix = unserved
        print_fn(
            f"{checkpoint_id} is {why}: keep-warm {keep_warm} is saved, but nothing is kept "
            f"ready or billed and robots can't connect. {fix[:1].upper()}{fix[1:]}."
        )
        print_fn(f"  warm:     {keep_warm_line(result)}")
        return
    if autoscaling(result):
        # Robots, never servers: its capacity scales with the robots that connect.
        if keep_warm == "off":
            print_fn(
                f"{checkpoint_id}: nothing is kept ready; the first robot to connect starts it."
            )
        else:
            ready = _robots(int(result.get("keep_warm_robots") or 1))
            when = "around the clock" if keep_warm == "always" else (
                f"for {keep_warm} from now, and after the last robot leaves" if now
                else f"for {keep_warm} after the last robot leaves"
            )
            print_fn(
                f"{checkpoint_id} keeps {ready} ready {when}, billed as at least {ready} "
                "while kept warm."
            )
        print_fn(f"  warm:     {keep_warm_line(result)}")
        return
    if take_over_from:
        print_fn(
            f"{checkpoint_id} is starting a warm server; {take_over_from} turns off once it "
            "is warm."
        )
    elif keep_warm == "always":
        print_fn(
            f"{checkpoint_id} keeps one server ready around the clock, billed like server time. "
            "Turn it off with: dreamscale deployments keep-warm "
            f"{checkpoint_id} off"
        )
    elif keep_warm == "off":
        print_fn(f"{checkpoint_id}: the server now stops when the last session ends.")
    else:
        print_fn(f"{checkpoint_id}: the server stays up {keep_warm} after the last robot leaves.")
    print_fn(f"  warm:     {keep_warm_line(result)}")


def run_restart(
    *,
    checkpoint_id: str,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
) -> dict:
    """Stop the deployment's servers now; with Always on a fresh one starts at once."""
    result = asyncio.run(_call(client_factory, "restart_deployment", checkpoint_id))
    servers, in_use = _counts(result.get("restart"))
    if autoscaling(result):
        print_fn(f"Restarted {checkpoint_id}: robots reconnect on their next request.")
        if result.get("keep_warm") is not None:
            print_fn(f"  warm:     {keep_warm_line(result)}")
        return result
    if not servers:
        print_fn(f"Nothing is running on {checkpoint_id}; the next robot starts a server.")
    elif (result.get("keep_warm") or "off") == "always":
        print_fn(f"Restarted {checkpoint_id}: a fresh server is starting now.")
    else:
        print_fn(f"Stopped {checkpoint_id}'s server: the next robot starts a fresh one.")
    if in_use:
        print_fn("  The connected robot reconnects to a new server on its next request.")
    if result.get("keep_warm") is not None:
        print_fn(f"  warm:     {keep_warm_line(result)}")
    return result


def run_stop(
    *,
    checkpoint_id: str,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
) -> dict:
    """Stop the deployment's servers now and keep none warm (turns its keep-warm off)."""
    before = asyncio.run(_call(client_factory, "get_checkpoint", checkpoint_id))
    result = asyncio.run(_call(client_factory, "stop_deployment", checkpoint_id))
    servers, in_use = _counts(result.get("stopped"))
    turned_off = _keep_warm_turned_off(before, result)
    if autoscaling(result):
        print_fn(
            f"Stopped {checkpoint_id}: {_robots(servers)} disconnected; the next robot starts it."
            if servers
            else f"Nothing is connected to {checkpoint_id}."
        )
        if turned_off:
            print_fn(f"  {turned_off} is now off, so no robots are kept ready.")
        return result
    if not servers:
        print_fn(f"Nothing is running on {checkpoint_id}.")
    else:
        print_fn(f"Stopped {checkpoint_id}'s server: the next robot starts a fresh one.")
    if turned_off:
        print_fn(f"  {turned_off} is now off, so no server is kept warm.")
    if in_use:
        print_fn("  The connected robot reconnects to a new server on its next request.")
    return result


def _keep_warm_turned_off(before: dict, reply: dict) -> str | None:
    """The keep-warm `stop` turned off, read from the server's reply: "Always on",
    "Keep-warm (10m)", or None. A control plane from before stop turned a timed keep-warm off
    answers it unchanged: never claimed. Always on it has always turned off."""
    was = before.get("keep_warm") or "off"
    if was == "off":
        return None
    now = reply.get("keep_warm", "off" if was == "always" else was) or "off"
    if now != "off":
        return None
    return "Always on" if was == "always" else f"Keep-warm ({was})"


def _counts(reply: Any) -> tuple[int, int]:
    reply = reply if isinstance(reply, dict) else {}
    return int(reply.get("servers") or 0), int(reply.get("in_use") or 0)
