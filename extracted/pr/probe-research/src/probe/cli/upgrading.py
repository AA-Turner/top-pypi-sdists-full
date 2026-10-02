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

import os
import time
from dataclasses import dataclass

from probe import __version__
from probe.cli import autoupdate, updater, versions
from probe.cli.capabilities import agent_source


@dataclass
class UpdateOutcome:
    lines: list[str]
    ok: bool
    restart_needed: bool


def perform_update(
    *,
    base_url: str,
    include_plugin: bool = True,
    force: bool = False,
    manifest: dict | None = None,
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
    """
    lines: list[str] = []

    # WAIT FOR THE PROCESS THAT SPAWNED US, if it named itself.
    #
    # Only the detached auto-update path sets this; the wizard's interactive
    # Update action has no parent to outlive and skips the wait. Replacing the
    # installed tree while the triggering command is still lazily importing from
    # it is how you get a ModuleNotFoundError out of a command that has worked
    # for a year (see autoupdate.wait_for_pid_exit).
    parent = os.environ.get(autoupdate.WAIT_FOR_PID_ENV)
    if parent:
        try:
            autoupdate.wait_for_pid_exit(int(parent))
        except (TypeError, ValueError):
            pass

    # THE RUN-LOCK CHECK IS UNCONDITIONAL, and deliberately outside the block
    # above. It used to sit inside it, which meant it only ran for spawns that
    # named a parent -- and the plugin's SessionStart hook does not: it runs
    # `probe wizard --action update --yes`, which lands here with no parent pid
    # and would have upgraded straight through a live training run. The hook is
    # the OLDEST caller of this function, so scoping the check to the new one
    # protected everything except the path that already existed.
    #
    # For the spawned path this is also a RE-check: the gate that allowed the
    # spawn ran before the wait, and a run started during it must not be
    # upgraded into by a decision made minutes earlier.
    if not force:
        try:
            from probe.cli import run_lock

            if run_lock.any_live():
                autoupdate.record_skip(autoupdate.SKIP_RUN_IN_FLIGHT)
                return UpdateOutcome(
                    lines=[
                        "a run is in flight on this machine; upgrade deferred "
                        "(`probe doctor` shows what is holding it)"
                    ],
                    ok=True,
                    restart_needed=False,
                )
        except Exception:  # noqa: BLE001 -- an unreadable lock must not strand the upgrade
            pass

    # A failed manifest fetch must never block the upgrade -- being unable to
    # ask "what is latest" is not a reason to refuse to move.
    if manifest is None:
        try:
            manifest = updater.fetch_latest(base_url)
        except Exception:  # noqa: BLE001
            manifest = {}
    plugin_target = updater.plugin_latest(manifest)
    tap_target = updater.tap_latest(manifest)
    cli_target = updater.cli_latest(manifest)

    install = updater.detect_install()
    lines.append(f"Probe Research CLI {__version__}  (installed via: {install.method})")

    res: updater.CliResult | None = None
    if install.method is updater.Method.EPHEMERAL:
        res = _update_persistent_copy(cli_target, lines)
    elif install.method in (
        updater.Method.EDITABLE,
        updater.Method.MANAGED,
        updater.Method.UNKNOWN,
    ):
        # Running a package-manager upgrade against a source checkout or a
        # lockfile-managed environment would trash someone's working tree.
        lines.append(
            f"  skipping auto-upgrade: "
            f"{updater.upgrade_cli(install, __version__, cli_target).message}"
        )
    else:
        res = updater.upgrade_cli(install, __version__, cli_target)
        lines.append(f"  {res.message}")
        if res.changed:
            versions.record_installed_cli(res.after)

    restart_needed = False
    pres: updater.PluginResult | None = None
    tap_behind = ""
    if include_plugin:
        source = agent_source()
        if source == "pi":
            # pi's extension is its own npm package, updated through `pi
            # install`/a `git pull`, not a marketplace this CLI can shell
            # out to (see wizard.INSTALLABLE_AGENT_SOURCES). The old
            # two-way ternary's silent `else` ran `claude plugin update`
            # against a pi-selected run whenever `claude` happened to be
            # on the same machine too -- updating a different agent's
            # plugins as a side effect of updating pi's. `pres` stays
            # None, same bucket as `include_plugin=False`: no plugin work
            # was attempted, not "attempted and nothing to update."
            lines.append("pi: not managed by this CLI — see `pi install` / a `git pull`")
        else:
            codex = source == "codex"
            lines.append("Codex plugins:" if codex else "Claude Code plugins:")
            pres = updater.update_codex_plugins() if codex else updater.update_plugin(plugin_target)
            lines.append(f"  {pres.message}")
            # THE TAP'S OWN LINE, so all three versions are on screen (the CLI's
            # is above). It is a separate plugin, and "updated the plugin" said
            # nothing about it while it sat a version behind.
            if pres.attempted:
                tap_line, behind = updater.tap_verdict(pres, tap_target)
                lines.append(f"  {tap_line}")
                tap_behind = tap_line if behind else ""
            if pres.confirmed and (pres.changed or updater.tap_changed(pres)):
                restart_needed = True
            # A machine that cannot run git would fail these the same way; the
            # failure printed above already says what to run first.
            if (not pres.confirmed or tap_behind) and not pres.git_blocked:
                agent = "Codex" if codex else "Claude Code"
                manual = (
                    updater.manual_codex_plugin_commands()
                    if codex
                    else updater.manual_plugin_commands()
                )
                lines.append(f"  update them manually, then restart {agent}:")
                lines.extend(f"    {line}" for line in manual.split("\n"))

    # `attempted` is what separates "the plugin update failed" from "there was no
    # Claude Code to update" -- a CLI-only user has no `claude` on PATH, and
    # recording that as a failure every session would train everyone to ignore
    # the one line that is supposed to mean something.
    #
    # A tap still behind the manifest after the run fails the plugin half too:
    # it is installed, `claude` was asked to move it, and it did not.
    plugin_ok = (True if pres is None else (pres.confirmed or not pres.attempted)) and not tap_behind
    if pres is not None and not pres.confirmed:
        plugin_detail = pres.message
    else:
        plugin_detail = tap_behind
    plugin_version = pres.after if pres is not None else None

    # The ONLY way a detached auto-update can report failure: it runs with no
    # terminal attached, so without this an updater that has been broken for a
    # month is indistinguishable from one that works. `probe doctor` prints it.
    # BOTH halves are recorded -- the plugin's outcome used to live only in
    # `lines`, which a detached run sends straight to /dev/null.
    autoupdate.record_attempt(
        autoupdate.Attempt(
            at=int(time.time()),
            # No `res` means the install method was one we refuse to auto-upgrade.
            # That is a deliberate skip, not a failure.
            ok=res.ok if res is not None else True,
            detail="" if res is None or res.ok else res.message,
            from_version=__version__,
            # A failure with no observed version records none: falling back to
            # the manifest's latest printed "FAILED ... still at CLI <latest>".
            to_version=(
                cli_target if res is None else res.after or (cli_target if res.ok else None)
            ),
            plugin_ok=plugin_ok,
            plugin_detail=plugin_detail,
            plugin_version=plugin_version,
        )
    )

    return UpdateOutcome(
        lines=lines,
        # Both halves, so `probe update`'s exit code means "the update worked",
        # not "the CLI half worked".
        ok=(res.ok if res is not None else True) and plugin_ok,
        restart_needed=restart_needed,
    )


def _update_persistent_copy(cli_target: str | None, lines: list[str]) -> updater.CliResult | None:
    """Bring the persistent install up to date from a temporary (npx/uvx) run.

    This environment is discarded on exit, so there is nothing here to upgrade:
    the persistent install is what matters. Each outcome is said outright. This
    used to print "upgrading your installed copy instead" and then nothing,
    because bootstrap has no message for "already current", which read as the
    upgrade having silently failed.

    None means nothing needed doing; otherwise the outcome to record.
    """
    from probe.cli import bootstrap

    boot = bootstrap.ensure_persistent_install()
    if boot.already_persistent:
        # Bootstrap proves only that the installed copy is at least THIS one, and
        # a uvx/pipx cache can serve a stale copy: compare with the latest too.
        installed = bootstrap.installed_version() or __version__
        if not updater.is_newer(cli_target, installed):
            lines.append(
                "  running from a temporary environment — your installed copy is "
                f"already {installed}, nothing to upgrade"
            )
            versions.record_installed_cli(installed)
            return None
        lines.append(
            "  running from a temporary environment — upgrading your installed copy "
            f"({installed} → {cli_target})"
        )
        boot = bootstrap.install_persistent(f"{bootstrap.INSTALL_SPEC}@latest")
    else:
        lines.append("  running from a temporary environment — installing a permanent copy")
    # Installer output, shown and (on failure) stored: scrubbed once for both.
    said = updater.clean_reason(boot.message) if boot.message else ""
    if said:
        lines.append(f"  {said}")
    if not boot.installed:
        # A failed install was recorded as a success: `probe doctor` said
        # "success -> CLI <latest>" and `probe update` exited 0.
        return updater.CliResult(True, False, False, __version__, None, said)
    after = bootstrap.installed_version()
    versions.record_installed_cli(after)
    if not after:
        message = "installed, but no `probe` could be found to confirm its version"
    elif updater.is_newer(cli_target, after):
        message = f"the installed copy is still {after} after installing {cli_target}"
    else:
        return updater.CliResult(True, True, True, __version__, after, "")
    # On screen too: "Installed `probe`" alone read as the upgrade landing.
    lines.append(f"  {message}")
    return updater.CliResult(True, False, True, __version__, after, message)
