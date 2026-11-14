"""Each deployment base's own code in the SDK (DSL-353, docs/plans/2026-10-30-family-registries.md
§6.6): what the CLI calls it, its presets and build steps, how its rows read, which robot
`dreamscale run` drives it on, how its RTC is set, how `deployments create` adds one, what
Detect shows, and the contract its sessions export.

A base's module, ``dreamscale.deploy_bases.<family>`` (the family manifest's id), declares one
``DeployBase`` as ``BASE``; this registry loads one per family the manifest deploys, in its
order. The CLI (``checkpoints_cmd``, ``cli``) and the policy runtime ask the base and never
name it. A base's code reads the CLI's shared helpers through ``cmd`` and ``cli``, looked up
when called (so the CLI modules may import this registry, and a test's patch of them holds).
"""

from __future__ import annotations

import importlib
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any, Literal

from dreamscale_transport import families as manifest


class _Module:
    """A module looked up when first used."""

    def __init__(self, name: str) -> None:
        self._name = name

    def __getattr__(self, attr: str) -> Any:
        return getattr(importlib.import_module(self._name), attr)


cmd: Any = _Module("dreamscale.checkpoints_cmd")
cli: Any = _Module("dreamscale.cli")


@dataclass(frozen=True)
class Base:
    """What differs between the bases a deployment fine-tunes, for the CLI."""

    presets: dict[str, str]  # preset id -> label
    build_steps: tuple[tuple[str, tuple[str, ...]], ...]
    typical_build: str | None


@dataclass(frozen=True)
class ExportedBase:
    """``deployment``: ``module:Class`` whose ``from_json`` parses the session's deployment
    block. ``contract``: ``module:function(resolved_config, deployment)`` returning its
    RuntimeContract. ``label`` names the base in errors. ``pad_episode_start_commands``:
    before its first executed command, the command window starts at the measured state
    (FLUX's upstream initializes it so). ``state``: what is done with a state that isn't one
    plain vector: "send" it as it is (ABC-VLA's server reads helpers' states), "convert" a
    two-arm state to one vector (InternW0's server reads one vector), or "refuse" it before
    sending (FLUX's: a helper's joint layout isn't assumed to be the export's)."""

    label: str
    deployment: str
    contract: str
    pad_episode_start_commands: bool = False
    state: Literal["send", "convert", "refuse"] = "send"

    def parse(self, data: Any) -> Any:
        return _load(self.deployment).from_json(data)

    def runtime_contract(self, resolved: Any, deployment: Any) -> Any:
        return _load(self.contract)(resolved, deployment)


@dataclass(frozen=True)
class SessionBase:
    """A base whose sessions carry their deployment's robot while the session's resolved
    configuration carries the contract (π0.5's). ``deployment``: ``module:Class`` whose
    ``from_json`` parses the session's deployment block. ``contract``:
    ``module:function(resolved_config, deployment, chunk_size_override)`` returning its
    RuntimeContract. ``control_hz``: ``module:function(requested)``, the command rate a caller
    may ask for (None: the session's)."""

    deployment: str
    contract: str
    control_hz: str

    def parse(self, data: Any) -> Any:
        return _load(self.deployment).from_json(data)

    def runtime_contract(self, resolved: Any, deployment: Any,
                         chunk_size_override: int | None = None) -> Any:
        return _load(self.contract)(resolved, deployment, chunk_size_override)

    def resolve_control_hz(self, requested: Any) -> float | None:
        return _load(self.control_hz)(requested)


def _load(path: str) -> Callable[..., Any] | Any:
    module, name = path.split(":")
    return getattr(importlib.import_module(module), name)


@dataclass(frozen=True)
class DeployBase:
    """One deployment base, as the SDK runs it."""

    family: str  # its manifest id
    name: str  # what `--base` parses it to; for a units base, the model its deployments serve
    label: str
    cli: Base
    aliases: tuple[str, ...] = ()  # other names `--base` takes
    listed_as: str | None = None  # the name `--base`'s choices offer (None: unlisted)
    # The `--base` name a refusal tells the user to create one with (default: the listed one,
    # else its name).
    creates_as: str | None = None
    # A row serving its model is its, ahead of any reading as π0.5 (rows from before bases
    # were named carry only the model).
    claims_model: bool = False
    robot_line: Callable[[dict], str] | None = None
    # `deployments show`: its own lines (None: the shared ones, with ``describe_rtc`` as the
    # rtc line when the row has an RTC method).
    describe: Callable[[dict], list[str]] | None = None
    describe_rtc: Callable[[dict], str] | None = None
    shows_rtc: bool = False  # `deployments list` shows its RTC method
    # Its robot waits for each chunk and runs it from its first action: `dreamscale run`
    # drives it in sync mode.
    waits_for_each_chunk: bool = False
    # The model `dreamscale run <robot> --deployment` runs: ``(robot, checkpoint id, row,
    # --model)``, or an error naming how to run it (None: `dreamscale run` doesn't drive it).
    runner: Callable[[Any, str, dict, str | None], str | None] | None = None
    # `deployments rtc`: ``(row, checkpoint id, method, max delay, client factory, print)``
    # (None: no RTC setting; ``rtc_refusal_fix`` says what to do instead).
    set_rtc: Callable[..., dict] | None = None
    rtc_refusal_fix: str = "nothing to change: its base fixes RTC"
    # The engines its deployments choose between, the default first (the API's ``engine``:
    # what its units serve; `deployments create --engine`, `deployments engine`); every other
    # is experimental. Empty: one engine, no setting.
    engines: tuple[str, ...] = ()
    # Detect reads it as this base (``model=<name>``); what `deployments inspect` prints of it
    # (None: its robot line).
    detects_as_base: bool = False
    found_lines: Callable[[dict], list[str]] | None = None
    local_archive: bool = False  # a single local checkpoint file is a source, beside a folder
    # `deployments create --base <name>`: every option the command takes, as keywords.
    create: Callable[..., None] | None = None
    # `deployments create --base <name> --official <checkpoint>`: one of its family's own
    # published checkpoints by name (None: the base offers none).
    create_official: Callable[..., None] | None = None
    exported: ExportedBase | None = None
    # Catalog models its deployments serve, with the contract their sessions export.
    catalog_exports: Mapping[str, ExportedBase] = field(default_factory=dict)
    # The command that runs a trained deployment on its robot, where its base knows it (None:
    # the robot preset's, else Python).
    run_command: Callable[[dict], str | None] | None = None
    # `--base`'s default, and the base Detect reads a repo as first (``inspect``): one base.
    default: bool = False
    # A row naming its id (``base_model``, else ``model``) or one of its source formats (the
    # family manifest's) is its, after the bases that claim their model; ``row_steps``:
    # ``(row, build steps)`` -> the build steps of a row it claims.
    claims_rows: bool = False
    row_steps: Callable[[dict, tuple], tuple] | None = None
    # Detect when `--base` names it or is auto (and it doesn't detect as itself):
    # ``(client, repo, revision, token, base, path)`` -> (the base it read the repo as, found).
    inspect: Callable[..., Any] | None = None
    # What a caller sees of its sessions' contract before one opens (RuntimeContract's
    # arguments), keyed by its id; None: none of its own.
    preview_contract: Mapping[str, Any] | None = None
    # Its sessions' robot and contract (SessionBase), where neither is exported.
    session: SessionBase | None = None
    # The errors-catalog code a control plane that predates its deployments refuses its
    # sessions with (an unknown model, or a request naming it).
    unavailable: str | None = None
    # Its robot presets: preset id -> its robot's layout (policy.deployment.PresetLayout).
    robot_presets: Mapping[str, Any] = field(default_factory=dict)
    # Recorded rigs (`dreamscale run <robot>`, embodiments) that run its deployments, beyond
    # its presets' robots.
    robots: tuple[str, ...] = ()
    # robot -> the module of the end-effector adapter its deployments run through there: its
    # ``ADAPTER`` class and ``describe_failures(policy)``.
    robot_adapters: Mapping[str, str] = field(default_factory=dict)


def _load_bases() -> tuple[DeployBase, ...]:
    out = []
    for family in manifest.FAMILIES:
        if family.deploy is None:
            continue
        base = importlib.import_module(f"{__name__}.{family.id}").BASE
        if not isinstance(base, DeployBase) or base.family != family.id:
            raise RuntimeError(f"dreamscale.deploy_bases.{family.id}.BASE is not its DeployBase")
        out.append(base)
    aliases = [alias for base in out for alias in (base.name, *base.aliases)]
    if len(set(aliases)) != len(aliases):
        raise RuntimeError("two deployment bases share a name")
    if sum(base.default for base in out) != 1:
        raise RuntimeError("exactly one deployment base is the default (DeployBase.default)")
    return tuple(out)


_BASES: tuple[DeployBase, ...] | None = None


def bases() -> tuple[DeployBase, ...]:
    """Every deployment base, in the manifest's order (loaded when first asked: the policy
    runtime imports this package, and a base's module imports the runtime's)."""
    global _BASES
    if _BASES is None:
        _BASES = _load_bases()
    return _BASES


def __getattr__(name: str) -> Any:
    if name == "BASES":
        return bases()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def named(name: str | None) -> DeployBase | None:
    """The base a name (or an alias) is, else None."""
    return next((b for b in bases() if name in (b.name, *b.aliases)), None)


def default() -> DeployBase:
    """The base `--base` defaults to."""
    return next(base for base in bases() if base.default)


def of_model(model: str | None) -> DeployBase | None:
    """The base whose sessions a model name opens: its manifest id or public name (never a CLI
    alias), else None."""
    for base in bases():
        deploy = manifest.family(base.family).deploy
        if model in (deploy.base, deploy.public_id):
            return base
    return None


def claiming(row: dict) -> DeployBase | None:
    """The base that claims a deployment row by its id or source format (``claims_rows``)."""
    from dreamscale.model_names import internal_model

    model = row.get("base_model") or row.get("model") or ""
    for base in bases():
        deploy = manifest.family(base.family).deploy
        if base.claims_rows and (internal_model(str(model)) == deploy.base
                                 or row.get("source_format") in deploy.source_formats):
            return base
    return None


def running_on(robot: str) -> tuple[DeployBase, ...]:
    """The bases whose deployments a recorded rig runs (``robots``), in the manifest's order."""
    return tuple(base for base in bases() if robot in base.robots)


def robot_presets() -> dict[str, Any]:
    """Every robot preset a base declares: preset id -> its robot's layout."""
    return {preset: layout for base in bases() for preset, layout in base.robot_presets.items()}


def names() -> dict[str, str]:
    """Every name `--base` takes -> the base's name."""
    return {alias: base.name for base in bases() for alias in (base.name, *base.aliases)}


def listed() -> tuple[str, ...]:
    """The names `--base` offers, in the manifest's order."""
    return tuple(base.listed_as for base in bases() if base.listed_as)


def exported_bases() -> dict[str, ExportedBase]:
    """Every model whose sessions export their contract: the units bases and the catalog
    models their deployments serve."""
    out: dict[str, ExportedBase] = {}
    for base in bases():
        if base.exported is not None:
            out[base.name] = base.exported
    for base in bases():
        out.update(base.catalog_exports)
    return out
