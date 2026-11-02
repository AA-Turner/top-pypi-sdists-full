"""each agent's plugin pass, one thread each, and the versions it left."""

from __future__ import annotations

import dataclasses
import time
from dataclasses import dataclass, field
# `update_report` is imported HERE, at the top, for the same reason updater.py
# imports its whole call graph eagerly (H8): it runs after `uv tool upgrade` has
# replaced the installed tree, when a first import would read the new files.
from probe.cli.wizard.apply import root_skills
from probe.cli.install import updater
from probe.shared.harness import plugins as plugin_cli


def _plugin_passes(
    sources, *, include_plugin: bool, prelude: "_Prelude"
) -> "dict[str, _AgentPass | BaseException]":
    """`_plugin_pass` for every source at once, one thread each (each in a copy
    of this context): each source's pass, or what it raised, or
    `ComponentOverdue` once it has run `component_deadline()` (plan A3). A
    thread that cannot start runs its pass here instead."""
    components: dict[str, _Component] = {}
    started: list[_Component] = []
    found: dict = {}
    # From before the first start: a signal while they start stops what did.
    with _stopped_with_the_update(started):
        for source in sources:

            def body(source=source):
                try:
                    return _plugin_pass(source, include_plugin=include_plugin, prelude=prelude)
                finally:
                    _finished(source)

            components[source] = _start(source, body)
            started.append(components[source])
        deadline = time.monotonic() + component_deadline()
        for source, component in components.items():
            found[source] = _outcome_by(component, deadline, _plugins_of(source))
            if isinstance(found[source], ComponentOverdue):
                _finished(source)  # the bar moves on
    return found


def _plugins_of(source: str) -> str:
    """"Codex's plugin update": a component's name, from the registry."""
    return f"{_agent_label(source) or source}'s plugin update"


@dataclass
class _AgentPass:
    """One coding agent's own plugin update (`_plugin_pass`): what it ran and
    what it printed. Built from the agent's source alone, so several agents'
    passes can run at once (`perform_updates`)."""

    source: str
    lines: list[str]
    pres: "updater.PluginResult | None" = None
    plugins_moved: bool = False
    restart_needed: bool = False
    tap_behind: str = ""
    nothing_installed: bool = False
    #: `UpdateOutcome.summary`, `.problems` and `.actions`.
    summary: str = ""
    problems: list[str] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)


def _plugin_pass(source: str, *, include_plugin: bool, prelude: _Prelude) -> _AgentPass:
    """One agent's marketplace plugins brought up to the manifest (`_AgentPass`).
    Reads nothing of the agent but `source`: no `agent_source()`, no
    process-wide state, so passes for different agents may run at once."""
    lines: list[str] = []
    plugin_target, tap_target = prelude.plugin_target, prelude.tap_target
    is_plugins_moved = False
    is_restart_needed = False
    pres: updater.PluginResult | None = None
    tap_behind = ""
    # None of Probe's plugins in this agent, before or after: nothing to update,
    # which is not a failure (`updater.nothing_installed`, the report's rule too).
    is_nothing_installed = False
    summary = ""
    problems: list[str] = []
    actions: list[str] = []
    if include_plugin:
        # pi has no marketplace plugin: for it `pres` stays None, same bucket as
        # `include_plugin=False`.
        if source != "pi":
            codex = source == "codex"
            kimi = source == plugin_cli.KIMI
            lines.append("Codex plugins:" if codex else "Kimi Code plugins:" if kimi else "Claude Code plugins:")
            pres = (
                updater.update_codex_plugins()
                if codex
                else updater.update_kimi_plugins()
                if kimi
                else updater.update_plugin(plugin_target)
            )
            lines.append(f"  {pres.message}")
            if pres.attempted:
                # Claude Code reads Probe's skills from its own skills folder
                # (copies of the installed plugin's) and re-reads it when it
                # changes: refreshing it now is what gives every open session
                # the new plugin's skill text on its next skill call, instead of
                # whenever a session next starts. A harness that reads the
                # plugin's own folder (Codex, Kimi) has none: a no-op there.
                skills = root_skills.refresh(source)
                lines.extend(f"  {line}" for line in skills)
                problems.extend(line for line in skills if _reports_failure(line))
            # The sessions still running a tap from before this update: the
            # machine reports the oldest live tap, so a current install beside
            # one of them still reads as the old version until it restarts.
            if pres.attempted and pres.tap_after:
                pres = dataclasses.replace(
                    pres, tap_running_stale=updater.stale_tap_daemons(source, pres.tap_after)
                )
            # "No restart needed" only where it is true (Claude Code or Codex,
            # a user-scope install, a tap with the hand-back, every old session
            # movable): everywhere else the restart line, as before.
            pres = dataclasses.replace(pres, follows=updater.follows_without_restart(source, pres))
            # THE TAP'S OWN LINE, so all three versions are on screen (the CLI's
            # is above). It is a separate plugin, and "updated the plugin" said
            # nothing about it while it sat a version behind.
            if pres.attempted:
                tap_line, behind = updater.tap_verdict(pres, tap_target)
                lines.append(f"  {tap_line}")
                tap_behind = tap_line if behind else ""
            if pres.confirmed and (pres.changed or updater.tap_changed(pres)):
                is_plugins_moved = pres.follows
                is_restart_needed = not pres.follows
            is_nothing_installed = updater.nothing_installed(pres, source)
            # A machine that cannot run git would fail these the same way; the
            # failure printed above already says what to run first. Nor when
            # there was nothing to update: those commands would fail the same.
            plugin_failed = not pres.confirmed and not is_nothing_installed
            if plugin_failed:
                problems.append(pres.message)
            elif tap_behind:
                problems.append(tap_behind.strip())
            elif pres.attempted and not pres.follows and (stale := updater.running_stale_note(pres)):
                # Installed and current, but sessions still run an older tap:
                # something to do, not a failure.
                actions.append(stale)
            if (plugin_failed or tap_behind) and not pres.git_blocked:
                agent = "Codex" if codex else "Kimi Code" if kimi else "Claude Code"
                manual = (
                    updater.manual_codex_plugin_commands()
                    if codex
                    else updater.manual_kimi_plugin_commands()
                    if kimi
                    else updater.manual_plugin_commands()
                )
                # Followed once updated by hand only with the tap it would get.
                follows = updater.follows_without_restart(
                    source, pres, tap_after=tap_target or pres.tap_after, predicting=True
                )
                heading = (
                    f"update them manually ({agent} needs no restart):" if follows
                    else f"update them manually, then restart {agent}:"
                )
                lines.append(f"  {heading}")
                lines.extend(f"    {line}" for line in manual.split("\n"))
                problems += [heading[0].upper() + heading[1:], *(f"  {line}" for line in manual.split("\n"))]
            if pres.confirmed and not is_nothing_installed:
                summary = _versions_summary(pres)
    return _AgentPass(
        source=source, lines=lines, pres=pres, plugins_moved=is_plugins_moved,
        restart_needed=is_restart_needed, tap_behind=tap_behind, nothing_installed=is_nothing_installed,
        summary=summary, problems=problems, actions=actions,
    )


def _reports_failure(line: str) -> bool:
    from probe.cli import wizard as wizard

    return wizard.reports_failure(line.strip())


def _versions_summary(pres: "updater.PluginResult") -> str:
    """"plugin 0.180.0 (updated), tap 0.10.23": where a confirmed pass left
    the plugins. Claude Code's `after` is the plugin's version; Codex's and
    Kimi Code's name each plugin (`name=version, ...`)."""
    named = dict(part.split("=", 1) for part in (pres.after or "").split(", ") if "=" in part)
    plugin = next((v for n, v in named.items() if n != "probe-research-tap"), None) if named else pres.after
    parts = []
    if plugin:
        parts.append(f"plugin {plugin}{' (updated)' if pres.changed else ''}")
    if pres.tap_after:
        parts.append(f"tap {pres.tap_after}{' (updated)' if updater.tap_changed(pres) else ''}")
    return ", ".join(parts)
from probe.cli.install.upgrade.components import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    ComponentOverdue,
    _Component,
    _outcome_by,
    _start,
    _stopped_with_the_update,
    component_deadline,
)
from probe.cli.install.upgrade.finish import _agent_label  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.upgrade.prelude import _Prelude  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.upgrade.upgrade import _finished  # noqa: E402 -- pieces need each other; the front door loads this one first
