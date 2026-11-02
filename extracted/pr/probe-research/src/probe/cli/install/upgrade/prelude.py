"""the once-per-run half: run-lock check, the CLI step (or left alone), the lifeboat refresh, the persistent copy."""

from __future__ import annotations
import contextlib
import os
from dataclasses import dataclass

from probe import __version__
# `update_report` is imported HERE, at the top, for the same reason updater.py
# imports its whole call graph eagerly (H8): it runs after `uv tool upgrade` has
# replaced the installed tree, when a first import would read the new files.
from probe.shared.updates import autoupdate
from probe.cli.install import updater
from probe.shared.updates import (
    update_report,
    updates as versions)
from probe.core import events as json_events


def cli_left_alone(version: str) -> "updater.CliResult":
    """The CLI step when the Probe service asked for plugins only (SKIP_CLI_ENV):
    nothing ran, and the CLI is where it should be (a success, never a failure
    in `probe doctor` or the update report)."""
    return updater.CliResult(
        ran=False, ok=True, changed=False, before=version, after=version,
        message=f"CLI {version} current; left as it is while daemon workers run",
    )


def _refresh_lifeboat(prelude: _Prelude) -> None:
    """The CLI's step ended ok (current, or moved): the lifeboat and its
    env.json as this release has them (plan fool-proof-updates B4), on every
    path an update takes -- the service's child, a session start's own update
    where no service runs (a pod), `probe update`, a run's end -- with the
    keeper's guards (`keeper.refresh_lifeboat`). A plugin that failed changes
    nothing of it. Never raises."""
    if prelude.deferred is not None or (prelude.res is not None and not prelude.res.ok):
        return
    try:
        from probe.service import keeper

        keeper.refresh_lifeboat()
    except Exception:  # noqa: BLE001 -- the update itself is done
        pass


@dataclass
class _Prelude:
    """What an Update does ONCE, whatever the agents: the run-lock check, the
    manifest, the CLI's own upgrade and pi's package (`_update_pi_package`,
    moved whatever agent runs it). `deferred` is the whole answer when a live
    run holds the upgrade off."""

    lines: list[str]
    res: "updater.CliResult | None" = None
    refused: str = ""
    plugin_target: str | None = None
    tap_target: str | None = None
    cli_target: str | None = None
    pi_update: "_PiUpdate | None" = None
    deferred: "UpdateOutcome | None" = None


def _update_prelude(
    *,
    base_url: str,
    include_plugin: bool,
    force: bool,
    manifest: dict | None,
    trigger: update_report.Trigger,
) -> _Prelude:
    """The once-per-run half of `_perform_update` (`_Prelude`)."""
    lines: list[str] = []
    # Loaded before the CLI's step can replace the files they come from (an
    # in-place upgrade): the lifeboat's refresh at the end runs this code.
    with contextlib.suppress(Exception):
        from probe.service import keeper  # noqa: F401
        from probe.service.updater import lifeboat  # noqa: F401

    # THE RUN-LOCK CHECK IS UNCONDITIONAL, and deliberately outside the wait in
    # `perform_update`. It used to sit inside it, which meant it only ran for
    # spawns that named a parent -- and the plugin's SessionStart hook does not: it runs
    # `probe wizard --action update --yes`, which lands here with no parent pid
    # and would have upgraded straight through a live training run. The hook is
    # the OLDEST caller of this function, so scoping the check to the new one
    # protected everything except the path that already existed.
    #
    # For the spawned path this is also a RE-check: the gate that allowed the
    # spawn ran before the wait, and a run started during it must not be
    # upgraded into by a decision made minutes earlier.
    # The Probe service decided to update past a live run (24 h of deferral,
    # plan D33) and says so: that decision stands here too.
    # Nor when it must update beside the running version (plan D6): a run keeps
    # its own files then, and the service let it go on for that reason.
    # Without a service the same day applies (C3, `autoupdate.defer_for_run`):
    # a run held this update off for 24 h without a break, so it goes on.
    from probe.foundation.service_api.vocabularies import DeferReason  # loaded already, by `updater`

    is_deferred = False
    if (
        not force
        and not forced_past(DeferReason.RUN_IN_FLIGHT)
        and os.environ.get(updater.REQUIRE_SIDE_BY_SIDE_ENV) != "1"
    ):
        try:
            from probe.foundation.durable import run_lock

            if run_lock.any_live() and autoupdate.defer_for_run(trigger=trigger.value):
                # Not a training loop: this is the updater, so the skip it just
                # recorded can go to the server now.
                update_report.flush(base_url)
                is_deferred = True
        except Exception:  # noqa: BLE001 -- an unreadable lock must not strand the upgrade
            pass
    if is_deferred:
        # Deferred, Probe's hooks in Codex are still approved (#3617): Codex
        # rewrites its copies of Probe's plugins by itself, and a day's deferral
        # left Codex unrecorded that long. Outside the check above, whose
        # handler would go on with the upgrade.
        return _Prelude(lines=[], deferred=UpdateOutcome(
            lines=[
                "a run is in flight on this machine; upgrade deferred "
                "(`probe doctor` shows what is holding it)" + updater.approve_codex_hooks_note()
            ],
            ok=True,
            restart_needed=False,
            deferred=True,
        ))

    # A failed manifest fetch must never block the upgrade -- being unable to
    # ask "what is latest" is not a reason to refuse to move.
    json_events.step(json_events.Step.UPDATE_MANIFEST, json_events.Status.STARTED)
    if manifest is None:
        try:
            manifest = updater.fetch_latest(base_url)
        except Exception:  # noqa: BLE001
            manifest = {}
    plugin_target = updater.plugin_latest(manifest)
    tap_target = updater.tap_latest(manifest)
    cli_target = updater.cli_latest(manifest)
    json_events.step(json_events.Step.UPDATE_MANIFEST, json_events.Status.DONE)

    if include_plugin:
        # The pi step runs AFTER the CLI upgrade below has replaced the files
        # it would lazily import, so import them now, from this version.
        # (`probe.foundation.harness_registry` is imported at the top: `_agent_label` needs it.)
        from probe.shared.harness.harnesses import pi as pi_config  # noqa: F401
        from probe.sdk import session_marker  # noqa: F401
        # The plugin steps reach each agent's integration (and Kimi's and Codex's config) lazily.
        from probe.shared.harness.harness import get_integrations
        from probe.shared.harness.harnesses.codex import config as _codex_config  # noqa: F401
        from probe.shared.harness.harnesses.kimi_code import config as _kimi_config  # noqa: F401

        get_integrations()

    json_events.step(json_events.Step.UPDATE_CLI, json_events.Status.STARTED)
    install = updater.detect_install()
    lines.append(f"Probe Research CLI {__version__}  (installed via: {install.method})")
    from probe.cli.install import capy_retire

    lines.extend(f"  {line}" for line in capy_retire.retire())

    result: updater.CliResult | None = None
    refused = ""
    if install.method is updater.Method.EPHEMERAL:
        result = _update_persistent_copy(cli_target, lines)
    elif install.method in (
        updater.Method.EDITABLE,
        updater.Method.MANAGED,
        updater.Method.UNKNOWN,
    ):
        # Running a package-manager upgrade against a source checkout or a
        # lockfile-managed environment would trash someone's working tree.
        refused = updater.upgrade_cli(install, __version__, cli_target).message
        lines.append(f"  skipping auto-upgrade: {refused}")
    else:
        if os.environ.get(SKIP_CLI_ENV) == "1":
            # The CLI half is done already: this release took the update over
            # from a hand-off and switched to itself (`probe.core.adopt`), or
            # the Probe service updates the plugins only (the CLI is current
            # and daemon workers run from its env, left as it is: plan D7).
            from probe.core import adopt

            result = adopt.cli_result(__version__) or cli_left_alone(__version__)
        else:
            try:
                with _service_stopped_on_windows(install) as stopped:
                    if stopped:
                        result = updater.upgrade_cli(install, __version__, cli_target)
                    else:
                        result = updater.CliResult(
                            ran=False, ok=False, changed=False, before=__version__, after=__version__,
                            message="CLI upgrade waits: the Probe service did not stop, and Windows cannot "
                                    "replace the files it holds (the next update tries again)",
                        )
            except Exception as exc:  # noqa: BLE001 -- its own failure, never the components' (plan A3)
                result = updater.CliResult(
                    ran=True, ok=False, changed=False, before=__version__, after=__version__,
                    message=f"the CLI upgrade stopped: {type(exc).__name__}: {updater.clean_reason(str(exc))}",
                )
        lines.append(f"  {result.message}")
        if result.changed:
            versions.record_installed_cli(result.after)

    json_events.step(
        json_events.Step.UPDATE_CLI,
        json_events.Status.DONE if result is None or result.ok else json_events.Status.FAILED,
    )
    _finished(UpdatePart.CLI)
    json_events.step(json_events.Step.UPDATE_INTEGRATIONS, json_events.Status.STARTED)
    pi_update: _PiUpdate | None = None
    if include_plugin:
        # pi's Probe package is updated whatever agent runs this: an Update from
        # a plain terminal (claude_code by default) or Claude Code's auto-update
        # used to skip it, so pi stayed on whatever package it was installed
        # with (2026-10-02: a 0.2.x package under a 0.206 CLI, so pi never
        # switched to the daemon). Its own `pi update <source>`, never a
        # marketplace. Once per run, however many agents it updates. In a
        # boundary and a deadline of its own (plan A3): pi failing or hanging
        # fails pi's step alone.
        pi_update = _bounded_pi_update()
    _finished(UpdatePart.PI_PACKAGE)
    return _Prelude(
        lines=lines, res=result, refused=refused, plugin_target=plugin_target, tap_target=tap_target,
        cli_target=cli_target, pi_update=pi_update,
    )
from probe.cli.install.updater.cli_installs.ephemeral import _update_persistent_copy  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.upgrade.package_step import _bounded_pi_update  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.upgrade.turn import SKIP_CLI_ENV, _service_stopped_on_windows, forced_past  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.upgrade.upgrade import UpdateOutcome, UpdatePart, _finished  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.harness.harnesses.pi.package_upgrade import _PiUpdate  # noqa: E402 -- pieces need each other; the front door loads this one first
