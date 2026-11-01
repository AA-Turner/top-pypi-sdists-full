"""Everything Probe does differently per coding agent, behind one interface: HarnessIntegration.
An agent's integration is harnesses/<id>/<id>.py, found by its harness_registry id: a new agent is a row and a folder."""

from __future__ import annotations

import importlib
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING, Any, Protocol

from probe.foundation.harness_registry import get_registry

if TYPE_CHECKING:
    from probe.shared.harness.session_log import Adapter


@dataclass(frozen=True)
class PluginCli:
    """An agent's plugin command line: its binary and its verbs for Probe's plugin lifecycle."""

    #: The executable on PATH.
    binary: str
    #: Probe's lifecycle verbs in the agent's own spelling: refresh, install, uninstall, list.
    verbs: Mapping[str, Any] = field(default_factory=dict)
    #: Runs a plugin command its own way, `(args, timeout) -> Result`; None runs `binary` from PATH.
    run: Callable[..., Any] | None = None
    #: The agent keeps its plugin list in a file Probe edits instead (Kimi Code): the module with
    #: list_plugins / refresh / install_plugin / uninstall_plugin. Its commands are then refused.
    plugin_list: Callable[[], ModuleType] | None = None
    #: Why a plugin command is refused here (only with `plugin_list`).
    no_command: str | None = None
    #: Where the agent keeps its clone of the marketplace `name` (it need not exist); None: no clone.
    checkout: Callable[[str], Path] | None = None


class HarnessIntegration(Protocol):
    """One coding agent's integration, by facet (composition, no base class); a facet it lacks is None."""

    #: Its harness_registry id, which its folder is named after.
    harness_id: str
    #: Spellings that name it besides the registry's id, aliases and route (the daemon's capture side).
    extra_names: tuple[str, ...]
    #: Its plugin command line, or None (pi: a settings entry, never a marketplace CLI).
    plugin_cli: PluginCli | None
    #: The team-note audit runs inline, never in a background subagent (its sandbox reaps those).
    should_audit_inline: bool
    #: Its installed-plugins ledger names the tap's installed version.
    has_plugin_ledger: bool

    @property
    def session_log(self) -> type[Adapter] | None:
        """The daemon's reader of its session log, or None: no daemon there."""
        ...


_loaded: dict[str, HarnessIntegration | None] = {}


def _load(harness_id: str) -> HarnessIntegration | None:
    """The integration in harnesses/<id>/<id>.py, or None when that folder does not exist."""
    if harness_id not in _loaded:
        name = f"{__package__}.harnesses.{harness_id}.{harness_id}"
        try:
            module = importlib.import_module(name)
        except ModuleNotFoundError as exc:
            if exc.name not in (name, name.rpartition(".")[0]):
                raise  # the module exists and an import inside it failed
            return None  # no folder for this row (not cached: a later look tries again)
        _loaded[harness_id] = getattr(module, "INTEGRATION", None)
    return _loaded[harness_id]


def get_integrations() -> tuple[HarnessIntegration, ...]:
    """Every registry row's integration, in registry order (rows with no folder here are left out)."""
    found = (_load(harness.id) for harness in get_registry().all())
    return tuple(integration for integration in found if integration is not None)


def get_integration(harness_id: str | None) -> HarnessIntegration | None:
    """The integration of an exact registry id, else None (never a default, never an alias)."""
    if harness_id not in get_registry().ids():
        return None
    return _load(harness_id)


def find_integration(name: str | None) -> HarnessIntegration | None:
    """The integration an id, alias, route or extra spelling names (case and surrounding space ignored)."""
    wanted = (name or "").strip().lower()
    if not wanted:
        return None
    harnesses = get_registry().all()
    for harness in harnesses:  # the registry's spellings first: loads only the integration they name
        if wanted in (*harness.names, harness.route):
            return _load(harness.id)
    for harness in harnesses:
        integration = _load(harness.id)
        if integration is not None and wanted in integration.extra_names:
            return integration
    return None
