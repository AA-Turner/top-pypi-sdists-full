"""dreamscale.trainings — fine-tune a base model on your LeRobot dataset, on Dreamscale's GPUs.

    ds = dreamscale.datasets.upload("./my_dataset")
    run = dreamscale.trainings.create(dataset=ds, base=base, max_usd=250)  # no prompt
    run.wait()                                                      # a live status line
    deployment = run.deploy()  # dreamscale.connect("pi0.5", deployment=deployment["id"])

A dataset is one kept on Dreamscale (``towels``, ``towels@2``: see dreamscale.datasets) or a
Hugging Face repo (``hf://owner/name[@revision]``).
The price is exact and quoted before anything starts; ``max_usd`` is the most a call may
spend, and create refuses a quote above it. ``dreamscale train`` is the same flow with one
confirm. Starts are idempotent: the same dataset and settings, while a run of them is still
active, return that run instead of starting another.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import math
import os
import re
import sys
import time
import uuid
from collections.abc import Callable
from dataclasses import dataclass, replace
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

import httpx
from dreamscale_transport.training_data import split_columns

from dreamscale import errors
from dreamscale.config import dashboard_url, dreamscale_home, load_config
from dreamscale.control import ControlPlaneClient

POLL_S = 5.0
ACTIVE = ("queued", "preparing", "training")
COMMAND = "dreamscale train"
_HF_REPO = re.compile(r"[A-Za-z0-9][\w.-]*/[\w.-]+")
# hf://owner/name/folder: a dataset in a folder of the repo (the control plane splits it).
_HF_DATASET = re.compile(r"[A-Za-z0-9][\w.-]*/[\w.-]+(?:/[\w.+=@,()-]+)*")
_DATASET_NAME = re.compile(r"[a-z0-9][a-z0-9.-]{1,46}[a-z0-9]\Z|ds_[0-9a-f]{24}\Z")
_PHASES = {
    "queued": "Queued",
    "checking_data": "Checking data",
    "converting": "Converting data",
    "waiting_for_gpus": "Queued",  # a GPU slot to come free (robots first) or start
    "starting": "Starting training",
    "restoring": "Restoring the saved state",
}
_BARS = "▁▂▃▄▅▆▇█"
# Consecutive failed polls tolerated while following (about a minute).
_POLL_FAILURES = 12
_SUPPORT_FIX = "retry; if it keeps failing, email team@dreamscalelabs.com"


# --- the dataset ----------------------------------------------------------------------------


@dataclass(frozen=True)
class DatasetSource:
    # "dataset" (kept on Dreamscale), "huggingface", or "several" (Hugging Face datasets, ``parts``)
    kind: str
    label: str  # as the user named it
    repo: str | None = None
    revision: str | None = None
    parts: tuple[DatasetSource, ...] = ()
    name: str | None = None  # a dataset's name or id, without @N
    version: int | None = None  # a dataset's version: named by @N, or its latest once resolved
    dataset_id: str | None = None  # once resolved
    # owner/name with no hf://: one of your account's datasets if there is one, else Hugging Face.
    ambiguous: bool = False


def _not_a_dataset(value: str) -> errors.DreamscaleError:
    return errors.DreamscaleError(
        errors.ErrorInfo(
            code="dataset_not_found",
            problem=f"{value} doesn't name a dataset",
            cause="a dataset is one of yours (towels, towels@2) or on Hugging Face (owner/name)",
            fix="pass --dataset towels (dreamscale datasets list shows yours) or "
            "--dataset hf://owner/name (hf://owner/name/folder for one in a folder of the repo)",
        )
    )


def upload_first(value: str) -> errors.DreamscaleError:
    """A folder: it's uploaded first, then trained on by name."""
    name = dataset_name_for(Path(value).expanduser().resolve().name or "dataset")
    return errors.catalog("upload_dataset_first", folder=value, name=name)


def dataset_name_for(text: str) -> str:
    """A folder's or repo's name as a dataset's (``YAM_towels`` -> ``yam-towels``), as the control
    plane suggests it."""
    slug = re.sub(r"[^a-z0-9.]+", "-", text.lower())[:48].strip("-.")
    if len(slug) < 3 or slug in ("recent", "base", "default"):
        slug = f"{slug}-dataset"[:48].strip("-.")
    return slug


def parse_dataset(value: str) -> DatasetSource:
    """``hf://owner/name[/folder][@revision]`` is always Hugging Face; ``ds_…``, a bare
    ``name[@N]`` or ``<your account>/name[@N]`` is your dataset; any other ``owner/name`` stays
    Hugging Face; a path (``./x``, ``/x``, ``~/x``) is a folder to upload first."""
    text = value.strip()
    if text.startswith("hf://"):
        repo, _, revision = text.removeprefix("hf://").partition("@")
        if not _HF_DATASET.fullmatch(repo.rstrip("/")):
            raise _not_a_dataset(value)
        return DatasetSource(
            "huggingface", text, repo=repo.rstrip("/"), revision=revision or None
        )
    if text.startswith((".", "/", "~")):
        raise upload_first(text)
    head, at, tail = text.partition("@")
    if _DATASET_NAME.fullmatch(head):
        if at and not (tail.isdigit() and int(tail) > 0):
            raise _not_a_dataset(value)
        return DatasetSource("dataset", text, name=head, version=int(tail) if at else None)
    if _HF_REPO.fullmatch(head):
        return DatasetSource(
            "huggingface", f"hf://{text}", repo=head, revision=tail or None, ambiguous=True,
            name=head, version=int(tail) if tail.isdigit() and int(tail) > 0 else None,
        )
    raise _not_a_dataset(value)


def parse_datasets(values: list[str]) -> DatasetSource:
    """One dataset (``parse_dataset``), or several Hugging Face datasets trained together, each
    read as it is (nothing merged): they must match after the column mapping."""
    if len(values) == 1:
        return parse_dataset(values[0])
    parts = tuple(parse_dataset(value) for value in values)
    if any(part.kind != "huggingface" for part in parts):
        raise errors.DreamscaleError(
            errors.ErrorInfo(
                code="invalid_datasets",
                problem="several datasets train together from Hugging Face only",
                cause="a dataset kept on Dreamscale trains by itself, for now",
                fix="upload them as one dataset (a folder of datasets combines the ones inside), "
                "or name each as hf://owner/name",
            )
        )
    return DatasetSource("several", " + ".join(part.label for part in parts), parts=parts)


def resolve_source(source: DatasetSource, client_factory: Callable[..., Any]) -> DatasetSource:
    """A dataset's id and the version a run trains on (its latest unless pinned), and whether an
    ``owner/name`` is your account's dataset or Hugging Face's."""
    if source.kind != "dataset" and not source.ambiguous:
        return source
    try:
        found = call(client_factory, "get_dataset", source.name)
    except errors.DreamscaleError as error:
        if source.ambiguous and error.code in ("dataset_not_found", "datasets_unavailable"):
            return replace(source, ambiguous=False, name=None, version=None)
        raise
    number = source.version or found.get("latest_version")
    if number is None:
        raise errors.DreamscaleError(
            errors.ErrorInfo(
                code="dataset_empty",
                problem=f"dataset {found.get('full_name')} has no data yet",
                cause="a dataset has data once an upload or import of it finishes",
                fix=f"dreamscale datasets upload ./folder --name {found.get('name')}",
            )
        )
    return DatasetSource(
        "dataset", f"{found.get('full_name')} v{number}", name=found.get("full_name"),
        version=number, dataset_id=found.get("id"),
    )


def dataset_body(source: DatasetSource) -> dict[str, Any]:
    """The dataset as the API takes it."""
    if source.kind == "dataset":
        body: dict[str, Any] = {"kind": "dataset", "name": source.dataset_id or source.name}
        return {**body, "version": source.version} if source.version else body
    if source.kind == "huggingface":
        body = {"kind": "huggingface", "repo": source.repo}
        return {**body, "revision": source.revision} if source.revision else body
    return {"kind": "several", "datasets": [dataset_body(part) for part in source.parts]}


def default_name(source: DatasetSource) -> str:
    if source.kind == "huggingface":
        return str(source.repo).rsplit("/", 1)[-1][:80]
    if source.kind == "several":  # the first, and how many more
        return f"{default_name(source.parts[0])}-and-{len(source.parts) - 1}-more"[:80]
    return str(source.name or "dataset").rsplit("/", 1)[-1][:80]


IMAGE_PREFIX = "observation.images."
_SLOTS = ("base", "left_wrist", "right_wrist")


def parse_inputs(specs: list[str]) -> dict[str, dict[str, Any]]:
    """`--input urdf=robot.json`: each a name and a JSON file holding one object (the server
    checks what the base takes)."""
    out: dict[str, dict[str, Any]] = {}
    for spec in specs:
        name, _, path = spec.partition("=")
        name = name.strip()
        problem = None
        if not name or not path:
            problem = f"--input {spec} isn't NAME=FILE.json"
        else:
            try:
                value = json.loads(Path(path).expanduser().read_text())
            except (OSError, ValueError) as error:
                problem = f"--input {name}: {path} isn't a readable JSON file ({error})"
            else:
                if not isinstance(value, dict):
                    problem = f"--input {name}: {path} holds {type(value).__name__}, not an object"
        if problem is None and name in out:
            problem = f"--input {name} is given twice"
        if problem:
            raise errors.DreamscaleError(errors.ErrorInfo(
                code="invalid_input", problem=problem,
                cause="each --input names one input and a JSON file holding one object",
                fix="pass e.g. --input urdf=robot.json"))
        out[name] = value
    return out


def parse_mapping(
    state: str | None = None, action: str | None = None, cameras: list[str] | None = None,
    weight: str | None = None, loss_mask: str | None = None, ee_state: str | None = None,
    ee_action: str | None = None, ee_rotation: str | None = None,
) -> dict[str, Any] | None:
    """`--state a+b --action c --camera top=base`: the columns to train on (any part left out
    is the dataset's own). A state may keep some of a column's values by name:
    `--state 'observation.state[left_joint_0,left_gripper]'`. A camera may be named without its
    `observation.images.` prefix (the server resolves it against the dataset). `--sample-weight`
    and `--loss-mask` name one-value columns (the server checks them). `--ee-state` and
    `--ee-action` name the measured and commanded end-effector pose columns (each arm's xyz then
    its rotation, in `--ee-rotation`'s format), for a base that learns end-effector poses."""
    mapping: dict[str, Any] = {}
    for key, value in (("weight", weight), ("loss_mask", loss_mask),
                       ("ee_rotation", ee_rotation)):
        if value:
            mapping[key] = value.strip()
    for key, value in (("state", state), ("action", action), ("ee_state", ee_state),
                       ("ee_action", ee_action)):
        if value:
            mapping[key] = split_columns(value)
    picked = []
    for spec in cameras or []:
        feature, _, slot = spec.rpartition("=")
        if not feature or slot not in _SLOTS:
            raise errors.DreamscaleError(
                errors.ErrorInfo(
                    code="invalid_camera",
                    problem=f"--camera {spec} isn't camera=slot",
                    cause="each --camera names one recorded camera and its camera role",
                    fix=f"pass e.g. --camera top=base (slots: {', '.join(_SLOTS)})",
                )
            )
        picked.append({"feature": feature, "slot": slot})
    if picked:
        mapping["cameras"] = picked
    return mapping or None


def _short(name: str) -> str:
    return name.removeprefix(IMAGE_PREFIX)


def folder_lines(summary: dict, *, several: bool = False) -> list[str]:
    """`Combines 15 datasets in folders · skipped 3: no episodes (3)` for a repo or folder of
    recording sessions; `Trains on 2 datasets together: a/b (50 episodes) · …` for datasets
    named together (``several``); nothing for one dataset."""
    folders, skipped = summary.get("folders") or [], summary.get("skipped") or []
    if not folders:
        return []
    if several:
        counts = summary.get("folder_episodes") or []
        each = [
            f"{folder} ({counts[i]:,} episode{'s' if counts[i] != 1 else ''})"
            if i < len(counts) else folder
            for i, folder in enumerate(folders)
        ]
        return [f"Trains on {len(folders)} datasets together: {' · '.join(each)}"]
    lines = [f"Combines {len(folders)} dataset{'s' if len(folders) != 1 else ''} in folders"]
    if skipped:
        reasons: dict[str, int] = {}
        for entry in skipped:
            reasons[entry["reason"]] = reasons.get(entry["reason"], 0) + 1
        why = ", ".join(f"{reason} ({n})" for reason, n in reasons.items())
        lines.append(f"Skipped {len(skipped)}: {why}")
    return lines


def mapping_lines(summary: dict, picked: bool = False) -> list[str]:
    """`Trains on: state a+b (8) · action c (7) · cameras top → base, …` when the columns were
    picked or aren't LeRobot's standard ones, and the recorded cameras left out (the standard
    case says nothing)."""
    mapping = summary.get("mapping")
    if not isinstance(mapping, dict):
        return []
    unused = summary.get("unused_cameras") or []
    standard = mapping["state"] == ["observation.state"] and mapping["action"] == ["action"]
    if standard and not picked and not unused:
        return []
    cameras = ", ".join(
        f"{_short(c['feature'])} → {c['slot'].replace('_', ' ')}" for c in mapping["cameras"]
    )
    lines = [
        f"Trains on: state {'+'.join(mapping['state'])} ({summary.get('state_dim')}) · action "
        f"{'+'.join(mapping['action'])} ({summary.get('action_dim')}) · cameras {cameras}"
    ]
    if unused:
        lines.append(
            f"Not used: {', '.join(_short(c) for c in unused)} (choose the cameras to train on; "
            "choose with --camera name=slot)"
        )
    return lines


# Held-out evaluation is opt-in (--eval-fraction, 2026-10-27): off unless a run chooses it, and
# shown only for the runs that did. On robot data a held-out loss often rises while the policy
# keeps improving, so nothing picks or marks a checkpoint by it; what to say wherever it's
# chosen or shown (the dashboard says the same):
EVAL_CAVEAT = (
    "Held-out loss is a poor proxy for task success in diffusion and flow-matching policies "
    "like π0.5 and FLUX: it often rises while the policy keeps improving. Use it to spot a "
    "broken run, not to pick a checkpoint; try checkpoints on the robot."
)


def held_out_metric(run_or_quote: dict) -> tuple[str, str, str]:
    """What a run's held-out evaluation reports: (label, the checkpoints' field, the
    evaluation points' field): its contract's, else its base's family's (the training
    registry's ``held_out_metric``, ABC-VLA's ``action_error``), else the loss."""
    from dreamscale_transport import training_families

    contract = run_or_quote.get("contract") or {}
    if contract.get("eval_metric") == "action_error":
        return "held-out action error", "eval_action_error", "action_error"
    base = run_or_quote.get("base")
    metric = (training_families.family_of(base).held_out_metric
              if base in training_families.listed_bases() else None)
    if metric is not None:
        return f"held-out {metric.replace('_', ' ')}", f"eval_{metric}", metric
    return "held-out loss", "eval_loss", "loss"


def run_settings(
    *, base: str | None, steps: int | None, max_usd: Any, rtc: bool | None, name: str | None,
    learning_rate: float | None, prompt: str | None, hardware_check: bool, trim_idle: bool,
    mapping: dict[str, Any] | None = None, eval_fraction: float | None = None,
    base_step: int | None = None, normalization: str | None = None,
    batch_size: int | None = None, warmup_steps: int | None = None,
    lr_schedule: str | None = None, checkpoint_every: int | None = None,
    inputs: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """The create body's fields besides the dataset (only what was chosen). ``inputs``: the
    run's inputs beside its dataset that its base's family takes, by name (a JSON object each,
    sent inline)."""
    settings = {
        key: value
        for key, value in (
            ("learning_rate", learning_rate), ("prompt", prompt), ("normalization", normalization),
            ("batch_size", batch_size), ("warmup_steps", warmup_steps),
            ("lr_schedule", lr_schedule), ("checkpoint_every", checkpoint_every),
        )
        if value is not None
    }
    if not hardware_check:
        settings["hardware_check"] = False
    if not trim_idle:
        settings["trim_idle"] = False
    # RTC only when chosen: unset trains what the base does by default (experimental: off).
    body: dict[str, Any] = {} if rtc is None else {"rtc": rtc}
    for key, value in (
        ("base", base), ("base_step", base_step), ("steps", steps), ("max_usd", max_usd),
        ("name", name), ("eval_fraction", eval_fraction or None),
    ):
        if value is not None:
            body[key] = str(value) if key == "max_usd" else value
    if settings:
        body["settings"] = settings
    if mapping:
        body["mapping"] = mapping
    if inputs:
        body["inputs"] = inputs
    return body


def estimate_body(body: dict[str, Any]) -> dict[str, Any]:
    """What the estimate prices: the create body without its name, RTC and accepted price."""
    return {k: v for k, v in body.items() if k in ("dataset", "base", "base_step", "steps",
                                                     "max_usd", "hf_token", "mapping",
                                                     "eval_fraction", "settings", "inputs")}


# --- the control plane ----------------------------------------------------------------------


def run_page(run_id: str) -> str | None:
    """The run's page on the dashboard of the control plane the CLI talks to (None for one
    without a known dashboard)."""
    return dashboard_url(f"/dashboard/training/{run_id}", load_config().control_plane_url)


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


def call(client_factory: Callable[..., Any], method: str, *args, **kwargs) -> Any:
    return asyncio.run(_call(client_factory, method, *args, **kwargs))


def _offered_bases_text(client_factory: Callable[..., Any]) -> str:
    """The bases your organization can start from, as `pi0.5, a or b`; "" when unknown."""
    try:
        bases = call(client_factory, "training_bases")
    except errors.DreamscaleError:
        return ""
    if len(bases) < 2:
        return "".join(bases)
    return f"{', '.join(bases[:-1])} or {bases[-1]}"


def problem_error(problem: dict, cause: str) -> errors.DreamscaleError:
    """An estimate's problem ({code, message, fix}) as a Dreamscale error."""
    code = str(problem.get("code") or "cannot_start")
    if code == "training_credits_required":
        return errors.catalog(
            code, detail=str(problem.get("message") or ""), amount_fix=str(problem.get("fix") or "")
        )
    return errors.DreamscaleError(
        errors.ErrorInfo(
            code=code,
            problem=str(problem.get("message") or "this run can't start"),
            cause=cause,
            fix=str(problem.get("fix") or "retry"),
        )
    )


def check_estimate(estimate: dict, cause: str) -> None:
    if not estimate.get("can_start", True):
        problems = [p for p in estimate.get("problems") or [] if isinstance(p, dict)]
        raise problem_error(problems[0] if problems else {}, cause)


# Idempotency: one key per (dataset, settings), kept until a run of them is finished.
def fingerprint(source: DatasetSource, body: dict[str, Any]) -> str:
    if source.kind == "huggingface":
        identity: Any = [source.repo, source.revision]
    elif source.kind == "several":
        identity = [[part.repo, part.revision] for part in source.parts]
    else:  # a new upload followed by the same command starts a new run
        identity = [source.dataset_id or source.name, source.version]
    settings = {k: v for k, v in body.items() if k not in ("dataset", "hf_token", "accept_usd")}
    blob = json.dumps([identity, settings], sort_keys=True, default=str)
    return hashlib.sha256(blob.encode()).hexdigest()


def _starts_path() -> Path:
    return dreamscale_home() / "trainings" / "starts.json"


def _starts() -> dict[str, Any]:
    try:
        starts = json.loads(_starts_path().read_text())
    except (OSError, ValueError):
        return {}
    return starts if isinstance(starts, dict) else {}


def _save_start(key: str, entry: dict | None) -> None:
    starts = _starts()
    if entry is None:
        starts.pop(key, None)
    else:
        starts[key] = entry
    path = _starts_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(starts))
    os.replace(temporary, path)


# A stored start's run is gone (deleted, or another organization's): the control plane
# answers training_not_found; this SDK's own name for a bare 404 is training_run_not_found.
_RUN_GONE = ("training_not_found", "training_run_not_found")


def active_run(client_factory: Callable[..., Any], fp: str) -> dict | None:
    """The still-active run these dataset and settings started, if any. A stored run that
    finished or no longer exists is forgotten, so the command starts a new one."""
    entry = _starts().get(fp) or {}
    if not entry.get("run"):
        return None
    try:
        run = call(client_factory, "get_training", entry["run"])
    except errors.DreamscaleError as error:
        if error.code not in _RUN_GONE:
            raise
        run = None
    if run is not None and run.get("status") in ACTIVE:
        return run
    _save_start(fp, None)
    return None


def start_run(
    client_factory: Callable[..., Any],
    body: dict[str, Any],
    fp: str,
    *,
    sleep: Callable[[float], None] = time.sleep,
) -> dict[str, Any]:
    """POST the run with this fingerprint's key; a dropped answer is retried with the same
    key, so it can never start twice."""
    for fresh in (False, True):
        entry = _starts().get(fp) or {}
        reused = bool(entry.get("key")) and not fresh
        key = entry.get("key") if reused else f"cli_{uuid.uuid4().hex}"
        _save_start(fp, {"key": key, "run": None})
        for attempt in range(3):
            try:
                run = call(client_factory, "create_training", body, idempotency_key=key)
                break
            except (httpx.TransportError, errors.ServerError) as error:
                if attempt == 2:
                    raise errors.DreamscaleError(
                        errors.ErrorInfo(
                            code="training_start_unconfirmed",
                            problem="couldn't confirm the training run started",
                            cause=f"the request to Dreamscale failed ({error})",
                            fix="rerun the same command; it never starts a second run",
                        )
                    ) from None
                sleep(2.0)
        # A key whose earlier run already finished returns that run: start a new one.
        if reused and run.get("status") not in ACTIVE:
            continue
        _save_start(fp, {"key": key, "run": run["id"]})
        return run
    return run


def forget_start(fp: str) -> None:
    _save_start(fp, None)


# --- words ----------------------------------------------------------------------------------


def usd(value: Any) -> str:
    try:
        return f"${Decimal(str(value)):,.2f}"
    except ArithmeticError:
        return f"${value}"


def duration(seconds: Any) -> str:
    seconds = max(int(seconds or 0), 0)
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    if hours:
        return f"{hours} h {minutes:02d} m"
    if minutes:
        return f"{minutes} m {secs:02d} s" if minutes < 10 else f"{minutes} m"
    return f"{secs} s"


def hours(value: Any) -> str:
    value = float(value or 0)
    return f"{value:.1f} h" if value >= 1 else f"{max(round(value * 60), 1)} min"


def _samples(count: int) -> str:
    if count >= 1e6:
        return f"{count / 1e6:.1f}M"
    return f"{count / 1e3:.0f}k" if count >= 1e3 else str(count)


def size_text(count: int) -> str:
    return f"{count / 1e9:.1f} GB" if count >= 1e8 else f"{max(count / 1e6, 0.1):.1f} MB"


def base_name(base_id: str | None) -> str:
    """A training base's name (the training registry's; a quote's stored id, gr00t-n17, by the
    name its family lists, gr00t-n1.7), else the id as given."""
    from dreamscale_transport import training_families

    if base_id in training_families.listed_bases():
        return training_families.family_of(base_id).base_name(base_id)
    if training_families.is_base(base_id):
        family = training_families.family_of(base_id)
        stored = training_families.stored_base(base_id)
        for listed in family.listed_bases:
            if family.bases.get(listed) == stored:
                return family.base_name(listed)
    return str(base_id)


def _robot_presets() -> dict:
    """Every robot preset a deployment base declares (deploy_bases): id -> its layout."""
    from dreamscale import deploy_bases

    return deploy_bases.robot_presets()


def robot_label(summary: dict, preset: str | None) -> str:
    layout = _robot_presets().get(preset or "")
    return layout.label if layout else (summary.get("robot_type") or "Custom robot")


def dataset_line(summary: dict, preset: str | None) -> str:
    """`SO-101 · 2 cameras · 30 fps · 50 episodes · 25 min`."""
    cameras = len(summary.get("cameras") or [])
    return (
        f"{robot_label(summary, preset)} · {cameras} camera{'s' if cameras != 1 else ''} · "
        f"{float(summary.get('fps') or 0):g} fps · {int(summary.get('episodes') or 0):,} "
        f"episodes · {hours(summary.get('demo_hours'))}"
    )


def _counts(counts: dict) -> str:
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return ", ".join(f"{n} {label[:1].lower()}{label[1:]}" for label, n in ordered)


def check_line(check: dict) -> str:
    """`removed 3 of 50 episodes (2 missing frames, …); cut 4 short windows (…)`."""
    removed, total = int(check.get("removed") or 0), int(check.get("episodes") or 0)
    text = (
        f"removed {removed:,} of {total:,} episodes ({_counts(check.get('reasons') or {})})"
        if removed
        else f"all {total:,} episodes kept"
    )
    cuts = check.get("cut_windows") or {}
    if cuts:
        count = sum(cuts.values())
        text += f"; cut {count:,} short window{'s' if count != 1 else ''} ({_counts(cuts)})"
    weights = check.get("weights") or {}
    if weights:
        text += f"; sample weights {weights.get('min', 0):g}–{weights.get('max', 0):g}"
        if weights.get("zero"):
            text += f" ({int(weights['zero']):,} at 0, left out)"
    masked = check.get("masked") or {}
    if masked:
        text += f"; {float(masked.get('share') or 0):.0%} of frames masked from the loss"
    return text


def eta_text(quote: dict) -> str:
    """"~4 m to prepare + ~1 h 02 m to train" (FLUX: "+ ~6 m to encode video" between), or
    "~1 h 06 m" on quotes that don't say apart."""
    eta, prepare = quote.get("eta_seconds"), quote.get("prepare_seconds")
    if prepare is None:
        return f"~{duration(eta)}"
    encode = int(quote.get("encode_seconds") or 0)
    train = max(int(eta or 0) - int(prepare) - encode, 0)
    return (
        f"~{duration(prepare)} to prepare + "
        + (f"~{duration(encode)} to encode video + " if encode else "")
        + f"~{duration(train)} to train"
    )


def normalization_line(quote: dict) -> str | None:
    """Where the run's normalization comes from, when the quote says (training_recipes)."""
    source, base = quote.get("normalization"), base_name(quote.get("base"))
    robot = trained_on(quote.get("base"))
    if source == "base":
        return f"  Normalization: {base}'s own ({robot})" if robot else (
            f"  Normalization: {base}'s own")
    if source == "parent":
        return "  Normalization: the run it continues, unless your data has moved far from it"
    if source == "data" and robot:
        # a base trained on another robot: its weights, this dataset's normalization
        return f"  Starts from {base}'s weights ({robot}), normalized with your data"
    if source == "data":
        return "  Normalization: computed from your data"
    return None


def trained_on(base_id: str | None) -> str | None:
    """The robot a base was trained on, for a base trained on one robot (π0.5 RTC YAM)."""
    from dreamscale_transport import training_families

    layout = _robot_presets().get(training_families.trained_on(base_id) or "")
    return f"trained on {layout.label}" if layout else None


def _rtc_text(offer: Any, chosen: bool | None) -> str:
    """` · RTC on` or ` · RTC off` for the run quoted: what was chosen, else the base's
    default ("" for a base or quote without RTC)."""
    if not isinstance(offer, dict) or not offer.get("available"):
        return ""
    on = bool(offer.get("default")) if chosen is None else chosen
    label = offer.get("label") if on else None
    return f" · RTC {'on' if on else 'off'}" + (f" ({label})" if label else "")


def quote_lines(estimate: dict, demo_hours: Any, *, rtc: bool | None = None) -> list[str]:
    """``rtc``: what the run asked for (None: the base's default)."""
    quote = estimate.get("quote") or {}
    balance = estimate.get("balance_usd")
    lines = [
        f"Fine-tune {base_name(quote.get('base'))} on {hours(demo_hours)} of demos",
        f"  {int(quote.get('steps') or 0):,} steps · {_samples(int(quote.get('samples') or 0))}"
        f" samples{_rtc_text(quote.get('rtc'), rtc)} · "
        f"{eta_text(quote)} · {usd(quote.get('usd'))}"
        + (f" (balance {usd(balance)})" if balance is not None else ""),
    ]
    if quote.get("gpus") and quote.get("gpu_hours") is not None:
        # The run's shape and the price's units: batch, learning rate, H100s and GPU-hours.
        schedule = (quote.get("lr_schedule") or {}).get("kind")
        rate = quote.get("learning_rate")
        trains = f"  Batch {int(quote['batch_size'])}"
        if rate:
            trains += f" at {float(rate):.1e}".replace("e-0", "e-")
            trains += f" ({schedule})" if schedule else ""
            if quote.get("warmup_steps"):
                trains += f" after a {int(quote['warmup_steps']):,}-step warm-up"
        trains += f" · {int(quote['gpus'])}× H100 · {float(quote['gpu_hours']):,.1f} GPU-hours"
        if quote.get("usd_per_gpu_hour"):
            trains += f" at {usd(quote['usd_per_gpu_hour'])}"
        lines.append(trains)
    if quote.get("checkpoints") and quote.get("checkpoint_every"):
        lines.append(f"  {int(quote['checkpoints'])} checkpoints, every "
                     f"{int(quote['checkpoint_every']):,} steps")
    normalized = normalization_line(quote)
    if normalized:
        lines.append(normalized)
    held = quote.get("eval") or {}  # only a quote that held episodes out
    if held:
        lines += [
            f"  Holds out {float(held['fraction']):.0%} of episodes for evaluation: "
            f"{int(held.get('evaluations') or 0)} "
            f"{held_out_metric({**quote, 'contract': estimate.get('contract')})[0]} checks, "
            f"+{(float(held['overhead']) - 1) * 100:.1f}% (included above)",
            f"  {EVAL_CAVEAT}",
        ]
    return lines


def sparkline(values: list[float], width: int = 8) -> str:
    finite = [float(v) for v in values if isinstance(v, int | float) and math.isfinite(v)]
    if len(finite) < 2:
        return ""
    size = math.ceil(len(finite) / min(width, len(finite)))
    means = [sum(chunk) / len(chunk) for chunk in
             (finite[i:i + size] for i in range(0, len(finite), size))]
    low, high = min(means), max(means)
    span = (high - low) or 1.0
    return "".join(_BARS[round((v - low) / span * (len(_BARS) - 1))] for v in means)


def status_text(run: dict, *, elapsed: int | None = None) -> str:
    """The run's state now: `Training · step 412 of 5,063 · loss 0.031 ▇▅▃▂ · ~6 h 52 m left`."""
    status = run.get("status")
    if status == "stopped":
        return stopped_line(run)
    if status not in ACTIVE:
        return str(status)
    progress = run.get("progress") or {}
    phase = run.get("phase") or ("training" if progress.get("step") else None)
    if status == "queued":
        phase = "queued"
    elif status == "preparing" and phase not in ("checking_data", "converting"):
        phase = "checking_data"
    if phase in ("training", "saving"):
        step, total = int(progress.get("step") or 0), int(progress.get("total_steps") or 0)
        where = f"step {step:,} of {total:,}"
        if phase == "saving":
            return f"Saving · {where}"
        parts = [f"Training · {where}"]
        if isinstance(progress.get("loss"), int | float):
            losses = [m.get("loss") for m in run.get("metrics") or [] if isinstance(m, dict)]
            parts.append(f"loss {progress['loss']:.3g} {sparkline(losses)}".rstrip())
        label, field, _ = held_out_metric(run)
        if isinstance(progress.get(field), int | float):  # a run that held episodes out
            shown = "held-out" if field == "eval_loss" else label
            parts.append(f"{shown} {progress[field]:.3g}")
        if progress.get("eta_seconds") is not None:
            parts.append(f"~{duration(progress['eta_seconds'])} left")
        return " · ".join(parts)
    encoding = progress.get("encoding") if phase == "starting" else None
    if isinstance(encoding, dict) and encoding.get("total"):
        # FLUX encodes its video once before its first update (its quote's "to encode video")
        share = int(encoding.get("done") or 0) / int(encoding["total"])
        parts = [f"Encoding video · {share:.0%}"]
        if encoding.get("eta_seconds") is not None:
            parts.append(f"~{duration(encoding['eta_seconds'])} left")
        return " · ".join(parts)
    label = _PHASES.get(phase or "", _PHASES["starting"])
    if phase == "restoring":
        return _restoring_text(run, label)
    return label if elapsed is None else f"{label}: {elapsed}s elapsed"


def _restoring_text(run: dict, label: str, *, now: float | None = None) -> str:
    """A resumed run whose saved state is coming back: how long so far, and past 10 minutes,
    that it waits for the cloud to start the worker that restores it (it trains on its own
    after)."""
    since = _time((run.get("resume") or {}).get("restoring_since"))
    if since is None:
        return label
    waited = max(0.0, (time.time() if now is None else now) - since.timestamp())
    if waited < 120:
        return label
    text = f"{label} · {duration(waited)} so far"
    if waited >= 600:
        text += "; waiting for the cloud to start a worker for it, then it trains on its own"
    return text


def stopped_line(run: dict) -> str:
    """`Stopped at step 1,812 of 5,063 · resume by Nov 23` (or that it can't resume)."""
    resume = run.get("resume") or {}
    total = int((run.get("quote") or {}).get("steps") or 0)
    where = f"Stopped at step {int(resume.get('steps_done') or 0):,} of {total:,}"
    until = _time(resume.get("resumable_until"))
    if resume.get("can_resume") and until:
        return f"{where} · resume by {until:%b} {until.day}"
    return f"{where}; it can no longer resume (its checkpoints stay deployable)"


def _time(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def latest_checkpoint(run: dict) -> dict | None:
    checkpoints = [c for c in run.get("checkpoints") or [] if isinstance(c, dict)]
    return max(checkpoints, key=lambda c: int(c.get("step") or 0)) if checkpoints else None


def outcome_lines(run: dict) -> list[str]:
    """What a finished run did, what it cost, and what to do next."""
    cost, status, run_id = run.get("cost") or {}, run.get("status"), run.get("id")
    latest = latest_checkpoint(run)
    if status == "ready":
        started, finished = _time(run.get("started_at")), _time(run.get("finished_at"))
        took = (
            f" in {duration((finished - started).total_seconds())}"
            if started and finished else ""
        )
        step = f" · latest checkpoint step {int(latest['step']):,}" if latest else ""
        return [
            f"✓ Ready{took} · charged {usd(cost.get('charged_usd', 0))}{step}",
            f"Deploy it: {COMMAND} deploy {run_id}",
        ]
    if status == "failed":
        error = run.get("error") or {}
        refunded = Decimal(str(cost.get("refunded_usd") or 0))
        charged = Decimal(str(cost.get("charged_usd") or 0))
        money = (
            f"Charged {usd(charged)}; refunded {usd(refunded)}" if charged
            else f"Refunded {usd(refunded)}; you weren't charged" if refunded
            else "You weren't charged"
        )
        return [
            f"✗ {error.get('message') or 'Training failed'}",
            f"  cause: training run {run_id} failed ({error.get('code') or 'unknown'})",
            f"  fix:   {error.get('fix') or _SUPPORT_FIX}",
            f"{money}.",
        ]
    if status == "stopped":
        resume = run.get("resume") or {}
        lines = [
            f"{stopped_line(run)} · charged {usd(cost.get('charged_usd', 0))}"
            f" · refunded {usd(cost.get('refunded_usd', 0))}"
        ]
        if resume.get("can_resume"):
            lines.append(
                f"Resume it ({usd(resume.get('usd', 0))} for the remaining "
                f"{int(resume.get('steps_left') or 0):,} steps): {COMMAND} resume {run_id}"
            )
        if latest:
            lines.append(f"Deploy a saved checkpoint: {COMMAND} deploy {run_id}")
        return lines
    if status == "canceled":
        progress = run.get("progress") or {}
        lines = [
            f"Canceled at step {int(progress.get('step') or 0):,} of "
            f"{int(progress.get('total_steps') or (run.get('quote') or {}).get('steps') or 0):,}"
            f" · charged {usd(cost.get('charged_usd', 0))} · refunded "
            f"{usd(cost.get('refunded_usd', 0))}"
        ]
        if latest:
            lines.append(f"Deploy a saved checkpoint: {COMMAND} deploy {run_id}")
        return lines
    return []


def run_line(deployment: dict) -> str:
    """How to run a trained deployment: its robot's command, or Python for other robots."""
    from dreamscale import deploy_bases

    base = deploy_bases.named(deployment.get("model"))
    command = base.run_command(deployment) if base and base.run_command else None
    if command is not None:
        return command
    # Any other (a base without a command of its own, or one this SDK doesn't know): the
    # default base's answer.
    return deploy_bases.default().run_command(deployment)


# --- following a run ------------------------------------------------------------------------


def live_printer(print_fn: Callable[[str], None]) -> tuple[Callable[[str], None], bool]:
    """A redrawn status line on a terminal (default ``print``); whether lines may repeat."""
    if print_fn is not print:
        return print_fn, False
    from dreamscale.terminal import ProgressPrinter

    return ProgressPrinter(show_header=False), sys.stdout.isatty()


def close_printer(printer: Callable[[str], None], print_fn: Callable[[str], None]) -> None:
    close = getattr(printer, "close", None)
    if printer is not print_fn and close is not None:
        close()


def follow(
    run: dict,
    *,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
    sleep: Callable[[float], None] = time.sleep,
    clock: Callable[[], float] = time.monotonic,
) -> dict:
    """Poll the run until it finishes, with one live status line. Ctrl-C (KeyboardInterrupt)
    stops following; the run carries on."""
    printer, live = live_printer(print_fn)
    metrics = list(run.get("metrics") or [])
    seen: dict[str, float] = {}
    last, failures = None, 0
    try:
        while run.get("status") in ACTIVE:
            key = (run.get("status"), run.get("phase"))
            started = seen.setdefault(str(key), clock())
            run = {**run, "metrics": metrics}
            if live:
                printer(status_text(run, elapsed=int(clock() - started)))
            else:
                # Logs get a line per phase, and per tenth of training.
                progress = run.get("progress") or {}
                total = int(progress.get("total_steps") or 0)
                tenth = int(progress.get("step") or 0) * 10 // total if total else 0
                if (key, tenth) != last:
                    printer(status_text(run))
                    last = (key, tenth)
            sleep(POLL_S)
            since = max((int(m.get("step") or 0) for m in metrics), default=None)
            try:
                fresh = call(client_factory, "get_training", run["id"], since_step=since)
            except (httpx.TransportError, errors.ServerError):
                failures += 1
                if failures >= _POLL_FAILURES:
                    raise
                continue
            failures = 0
            metrics += [m for m in fresh.get("metrics") or [] if isinstance(m, dict)]
            run = fresh
    finally:
        close_printer(printer, print_fn)
    return {**run, "metrics": metrics}


# --- the SDK --------------------------------------------------------------------------------


class Training:
    """A training run (``tr_…``): its JSON in ``.data``, refreshed by ``refresh()``."""

    def __init__(self, data: dict, *, client_factory: Callable[..., Any] = ControlPlaneClient):
        self.data = data
        self._client_factory = client_factory

    @property
    def id(self) -> str:
        return self.data["id"]

    @property
    def status(self) -> str:
        return self.data["status"]

    @property
    def checkpoints(self) -> list[dict]:
        return list(self.data.get("checkpoints") or [])

    def __repr__(self) -> str:
        return f"Training({self.id!r}, status={self.status!r})"

    def refresh(self) -> Training:
        self.data = call(self._client_factory, "get_training", self.id)
        return self

    def wait(self, *, quiet: bool = False) -> Training:
        """Follow the run until it finishes (a live line unless ``quiet``). Raises the run's
        error if it failed."""
        self.data = follow(
            self.data, client_factory=self._client_factory,
            print_fn=(lambda _line: None) if quiet else print,
        )
        if self.status == "failed":
            error = self.data.get("error") or {}
            raise problem_error(error, f"training run {self.id} failed")
        return self

    def stop(self) -> Training:
        """Stop it where it is: you pay for the steps it completed, it saves a checkpoint, and
        ``resume()`` continues it within 30 days. Nothing is charged before training starts."""
        # /cancel: every control plane answers it (the one with Stop and Resume stops there).
        self.data = call(self._client_factory, "cancel_training", self.id)
        return self

    def cancel(self) -> Training:
        """The older name of ``stop()``."""
        return self.stop()

    def resume(self, *, max_usd: float | str | Decimal) -> Training:
        """Continue a stopped run for its remaining steps at its own rate: ``max_usd`` is the
        most the rest may cost, and the call refuses a price above it. Follow it with
        ``wait()``."""
        self.data = call(
            self._client_factory, "resume_training", self.id,
            accept_usd=str(Decimal(str(max_usd))), idempotency_key=f"sdk-resume-{uuid.uuid4()}",
        )
        return self

    def delete(self) -> None:
        """Delete it for good. One still going is canceled first: you pay for the steps it
        completed. Deployments made from its checkpoints keep running."""
        call(self._client_factory, "delete_training", self.id)

    def deploy(self, step: int | None = None, *, region: str | None = "auto") -> dict:
        """A Deployment of a checkpoint (1-based ``step``; default the latest). It validates
        on a GPU first; pass its ``model`` and ``id`` to ``dreamscale.connect``. ``region``: a
        region id such as ``"japan"``, or ``"auto"`` (the default), the nearest region its base
        serves, measured from here as ``dreamscale train deploy`` does (the server's default
        when nothing could be measured)."""
        from dreamscale.checkpoints_cmd import AUTO_REGION, _check_region, parse_region

        region = parse_region(region)
        if region == AUTO_REGION:
            base = self.data.get("base") or call(
                self._client_factory, "get_training", self.id
            ).get("base")
            region = (_check_region(self._client_factory, base, base, region,
                                    print_fn=lambda _: None)
                      if isinstance(base, str) else None)
        result = call(
            self._client_factory, "deploy_training", self.id, step=step, region=region
        )
        return result.get("deployment") or result


def get(run_id: str) -> Training:
    return Training(call(ControlPlaneClient, "get_training", run_id))


def create(
    *,
    dataset: Any,
    base: str,
    max_usd: float | str | Decimal,
    steps: int | None = None,
    rtc: bool | None = None,
    name: str | None = None,
    hf_token: str | None = None,
    eval_fraction: float | None = None,
    inputs: dict[str, dict[str, Any]] | None = None,
    mapping: dict[str, Any] | None = None,
    client_factory: Callable[..., Any] = ControlPlaneClient,
) -> Training:
    """Start a training run without a prompt: ``dataset`` is a ``Dataset``, ``"towels@2"``,
    ``"acme/towels"`` or ``"hf://…"``; ``max_usd`` is the most it may cost, and the call refuses a
    quote above it. Length is Auto unless ``steps`` is given. ``inputs``: what the base's family
    takes beside the dataset, by name (a JSON object each); ``mapping``: the columns to train on
    (``parse_mapping``'s); each sent only when given."""
    if not base:
        raise errors.catalog("base_required")
    pinned = getattr(dataset, "ref", None)
    source = resolve_source(
        parse_dataset(pinned if pinned is not None else os.fspath(dataset)), client_factory
    )
    limit = Decimal(str(max_usd))
    body = run_settings(
        base=base, steps=steps, max_usd=None, rtc=rtc, name=name or default_name(source),
        learning_rate=None, prompt=None, hardware_check=True, trim_idle=True,
        eval_fraction=eval_fraction, inputs=inputs, mapping=mapping,
    )
    fp = fingerprint(source, body)
    existing = active_run(client_factory, fp)
    if existing is not None:
        return Training(existing, client_factory=client_factory)
    token = hf_token or os.environ.get("HF_TOKEN") or None
    extra = {"hf_token": token} if token else {}
    dataset_json = dataset_body(source)
    estimate = call(client_factory, "estimate_training", estimate_body(
        {**body, **extra, "dataset": dataset_json}
    ))
    check_estimate(estimate, f"the estimate for {source.label}")
    quote = estimate.get("quote") or {}
    price = Decimal(str(quote.get("usd") or 0))
    if price > limit:
        # The most steps the limit buys, as the control plane prices them (a run's GPU-hours).
        within = call(client_factory, "estimate_training", estimate_body(
            {**{k: v for k, v in body.items() if k != "steps"}, **extra, "max_usd": str(limit),
             "dataset": dataset_json}
        ))
        fits = int((within.get("quote") or {}).get("steps") or 0)
        raise errors.DreamscaleError(
            errors.ErrorInfo(
                code="quote_over_limit",
                problem=f"this run costs {usd(price)}, more than max_usd={usd(limit)}",
                cause=f"{int(quote['steps']):,} steps of {int(quote['batch_size'])} samples",
                fix=f"raise max_usd, or pass steps={fits} (the most {usd(limit)} buys)"
                if fits else "raise max_usd",
            )
        )
    run = start_run(
        client_factory, {**body, **extra, "dataset": dataset_json, "accept_usd": str(limit)}, fp
    )
    return Training(run, client_factory=client_factory)


async def _upload(client_factory, root, files, progress=None, transport=None,
                  kind: str = "dataset", base_model: str | None = None,
                  slices=None) -> dict:
    from dreamscale import uploads

    client = _client(client_factory)
    try:
        return await uploads.upload(
            client, root, files, progress=progress, transport=transport, kind=kind,
            **({"base_model": base_model} if base_model is not None else {}),
            **({"slices": slices} if slices else {}),
        )
    finally:
        await client.close()
