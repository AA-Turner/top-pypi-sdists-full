"""Performing an update, as a function the wizard can call.

This was the body of a top-level `probe update` command. It moved here because
the wizard's Update action used to print "Run: probe update" and exit — which
is absurd. The wizard's whole job is to DO the thing; bouncing the user back to
a shell to type a command themselves is the failure it exists to remove.

There is still a hidden `probe update` bound to this, because the plugin's
SessionStart hook spawns it and plugins update on the USER's schedule, not
ours. Deleting the command outright would silently break auto-update on every
machine whose plugin has not been refreshed yet.
"""

from __future__ import annotations
import contextvars
from collections.abc import Callable, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field
from probe.foundation.compat.compat import StrEnum
from probe.shared.updates import update_report
from probe.cli.wizard.state.agent_identity import agent_source
from probe.foundation.harness_registry import get_registry


class UpdatePart(StrEnum):
    """The parts of an Update a progress hook (`reporting_progress`) hears
    finish, besides each agent's own plugins (named by its source)."""

    CLI = "cli"
    PI_PACKAGE = "pi_package"


_progress: contextvars.ContextVar[Callable[[str], None] | None] = contextvars.ContextVar(
    "probe_update_progress", default=None
)


@contextmanager
def reporting_progress(hook: Callable[[str], None]):
    """In this block, `hook(part)` hears each part of an Update finish (an
    `UpdatePart`, or an agent's source once its plugins are through), from
    whichever thread ran it: the wizard's bar. Never fails the update."""
    token = _progress.set(hook)
    try:
        yield
    finally:
        _progress.reset(token)


def _finished(part: str) -> None:
    hook = _progress.get()
    if hook is None:
        return
    try:
        hook(part)
    except Exception:  # noqa: BLE001 - a progress bar must never fail an update
        pass


@dataclass
class UpdateOutcome:
    lines: list[str]
    ok: bool
    #: The plugin or the tap moved and open sessions cannot follow it by
    #: themselves (`updater.follows_without_restart`: a Kimi Code session that
    #: loaded an older manifest or started before its hooks handed over, a
    #: project-scope install, a tap before the hand-back, a session on
    #: protocol 1, one still on its own tap watch): they need a restart, as before.
    restart_needed: bool
    #: The plugin or the tap moved and open sessions follow it: an open
    #: session runs the installed plugin's hooks from its next event
    #: (`hooks/dispatch.py hand_over`), its skill copies are refreshed here,
    #: and the Probe service moves the rest (the status line, the managed
    #: block, its recorders' tap) after its update cycle.
    plugins_moved: bool = False
    #: For the wizard's final screen (`setup.RunSummary`): a few words on where
    #: this agent's plugins ended ("plugin 0.180.0, tap 0.10.23")...
    summary: str = ""
    #: ...what needs attention about them (a failure and the commands to run
    #: by hand), and what needs attention about the run itself (the CLI's
    #: upgrade, pi's package: failures and what open sessions must do), the
    #: same on every agent's answer.
    problems: list[str] = field(default_factory=list)
    run_notes: list[str] = field(default_factory=list)
    #: What the person still has to do with it, though it worked: open
    #: sessions to /reload or restart. Never counts as a failure.
    actions: list[str] = field(default_factory=list)
    #: The run's own such steps: pi's /reload, from an Update of any agents.
    run_actions: list[str] = field(default_factory=list)
    #: The CLI's version line: "Probe CLI 0.324.0", "(updated from 0.323.1)".
    cli: str = ""
    #: A live run held the update off: nothing was updated (`lines` says why).
    deferred: bool = False


#: What `probe update` and the wizard's Update say when the plugins moved and
#: open sessions follow.
PICKED_UP = "No restart needed: open sessions pick up the new plugin at their next prompt."


def after_update_line(outcome: "UpdateOutcome", agent: str, source: str | None = None) -> str | None:
    """The line `probe update` and the wizard's Update end with: no restart
    where open sessions follow, the restart line where they cannot, else none.
    An agent that reloads its plugins in place (`reloads_plugins`: Kimi Code's
    and pi's /reload) is told that first: cheaper than a restart."""
    if getattr(outcome, "plugins_moved", False):
        return PICKED_UP
    if getattr(outcome, "restart_needed", False):
        if source and reloads_plugins(source):
            return f"Run /reload in {agent} (or restart it) to apply the plugin update."
        return f"Restart {agent} to apply the plugin update."
    return None


def reloads_plugins(source: str) -> bool:
    """Does this agent re-read Probe's plugin or package in place with /reload
    (a manifest kept from its start: `loaded_records`; an extension: pi)?"""
    from probe.foundation.harness_registry.harness_registry import CAPABILITY_LOADED_RECORDS, FAMILY_EXTENSION

    harness = get_registry().find(source)
    return harness is not None and (harness.can(CAPABILITY_LOADED_RECORDS) or harness.family == FAMILY_EXTENSION)


def perform_update(
    *,
    base_url: str,
    include_plugin: bool = True,
    force: bool = False,
    manifest: dict | None = None,
    trigger: update_report.Trigger | None = None,
) -> UpdateOutcome:
    """Upgrade the CLI and (optionally) the plugins, and record the attempt.

    There is no confirmation hook. Both callers -- the wizard's Update action
    and the plugin's SessionStart hook -- have already been told to update by
    the time they get here, and the one that has a terminal must not stop to
    ask a second time.

    ``force`` skips the run-lock check. Reserved for a human who has explicitly
    asked to upgrade now and can see what is running; nothing automatic sets it.

    ``manifest`` is for a caller that ALREADY fetched one. The run-end path
    (version_refresh's apply-if-newer mode) has to compare before it decides to
    call us at all, and without this it would fetch twice -- once to decide, once
    here to pick a target. Two fetches are not just wasteful: a release landing
    between them means comparing against one version and upgrading toward
    another. Omit it and we fetch, exactly as before.

    ``trigger`` is what asked for this run, for the server's update report
    (`update_report`); omitted, the spawner's `PROBE_AUTOUPDATE_TRIGGER`, else
    a person. It changes nothing about the update itself.

    Raises `wizard_lock.Busy`, having changed nothing and recorded the skip,
    while another Probe setup holds the device.
    """
    trigger = trigger or update_report.trigger_from_env(update_report.Trigger.MANUAL)

    with _update_turn(manifest, trigger):
        return _perform_update(
            base_url=base_url, include_plugin=include_plugin, force=force, manifest=manifest, trigger=trigger
        )


def perform_updates(
    sources: "Sequence[str]",
    *,
    base_url: str,
    include_plugin: bool = True,
    force: bool = False,
    manifest: dict | None = None,
    trigger: update_report.Trigger | None = None,
) -> "dict[str, UpdateOutcome]":
    """`perform_update` for several coding agents at once, by source, in order.

    The CLI's upgrade, the manifest and pi's package run ONCE (`_Prelude`):
    one pass per agent used to repeat all three, `pi update` included. Each
    agent's own plugins (`_plugin_pass`: its marketplace fetch, `plugin update`,
    its skills) then move on threads of their own, at the same time, and each
    pass is recorded and reported in `sources` order, as one after another
    were. The CLI's and pi's lines go to the first agent's answer (pi's to
    pi's own, when it is one of them); a deferral (a live run) answers for all.

    One agent's pass that raises, or runs past `component_deadline()`, fails
    that agent's answer alone (plan A3, I7): recorded and reported as the
    failure it is, while the CLI's step and every other pass finish and report.
    """
    trigger = trigger or update_report.trigger_from_env(update_report.Trigger.MANUAL)
    with _update_turn(manifest, trigger):
        prelude = _update_prelude(
            base_url=base_url, include_plugin=include_plugin, force=force, manifest=manifest, trigger=trigger
        )
        if prelude.deferred is not None:
            return {source: prelude.deferred for source in sources}
        passes = _plugin_passes(sources, include_plugin=include_plugin, prelude=prelude)
        package_harness = _package_harness()
        pi_home = package_harness if package_harness in sources else sources[0] if sources else None
        # What failed the whole run, on every agent's answer: each pass's
        # `ok` carries it, and `--json` sends each agent's lines as its reason.
        result, pi_update = prelude.res, prelude.pi_update
        cli_failure = [f"  {result.message}"] if result is not None and not result.ok else []
        pi_failure = [f"  pi package: {pi_update.detail}"] if pi_update is not None and not pi_update.ok else []
        outcomes: dict[str, UpdateOutcome] = {}
        for index, source in enumerate(sources):
            agent = passes[source]
            lines = [*prelude.lines] if index == 0 else [*cli_failure]
            lines.extend(pi_update.lines if pi_update is not None and source == pi_home else pi_failure)
            if isinstance(agent, BaseException):
                outcomes[source] = _crashed_pass(
                    source, agent, lines, prelude=prelude, base_url=base_url, trigger=trigger
                )
                continue
            outcomes[source] = _finish_pass(
                agent, [*lines, *agent.lines],
                prelude=prelude, include_plugin=include_plugin, base_url=base_url, trigger=trigger,
            )
        _refresh_lifeboat(prelude)
        return outcomes


def _perform_update(
    *,
    base_url: str,
    include_plugin: bool,
    force: bool,
    manifest: dict | None,
    trigger: update_report.Trigger,
) -> UpdateOutcome:
    """`perform_update` once its spawner has exited and the wizard lock is held."""
    prelude = _update_prelude(
        base_url=base_url, include_plugin=include_plugin, force=force, manifest=manifest, trigger=trigger
    )
    if prelude.deferred is not None:
        return prelude.deferred
    if prelude.pi_update is not None:
        prelude.lines.extend(prelude.pi_update.lines)
    source = agent_source()
    agent = _plugin_passes([source], include_plugin=include_plugin, prelude=prelude)[source]
    if isinstance(agent, BaseException):
        outcome = _crashed_pass(source, agent, [*prelude.lines], prelude=prelude, base_url=base_url, trigger=trigger)
    else:
        outcome = _finish_pass(
            agent, [*prelude.lines, *agent.lines],
            prelude=prelude, include_plugin=include_plugin, base_url=base_url, trigger=trigger,
        )
    _refresh_lifeboat(prelude)
    return outcome
from probe.cli.install.upgrade.finish import _crashed_pass, _finish_pass  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.upgrade.package_step import _package_harness, package_harness  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.upgrade.plugin_pass import _plugin_passes  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.upgrade.prelude import _refresh_lifeboat, _update_prelude  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.upgrade.turn import _update_turn  # noqa: E402 -- pieces need each other; the front door loads this one first
