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

import dataclasses
import os
import time
from collections.abc import Callable
from contextlib import contextmanager
from dataclasses import dataclass

from probe import __version__
# `update_report` is imported HERE, at the top, for the same reason updater.py
# imports its whole call graph eagerly (H8): it runs after `uv tool upgrade` has
# replaced the installed tree, when a first import would read the new files.
from probe.cli import autoupdate, plugin_cli, update_report, updater, versions
from probe.cli.capabilities import agent_source
from probe.harness import get_registry


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
    """
    lines: list[str] = []
    trigger = trigger or update_report.trigger_from_env(update_report.Trigger.MANUAL)

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
                autoupdate.record_skip(autoupdate.SKIP_RUN_IN_FLIGHT, trigger=trigger.value)
                # Not a training loop: this is the updater, so the skip it just
                # recorded can go to the server now.
                update_report.flush(base_url)
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

    if include_plugin:
        # The pi step runs AFTER the CLI upgrade below has replaced the files
        # it would lazily import, so import them now, from this version.
        # (`probe.harness` is imported at the top: `_agent_label` needs it.)
        from probe.cli import pi_config  # noqa: F401
        from probe.sdk import session_marker  # noqa: F401

    install = updater.detect_install()
    lines.append(f"Probe Research CLI {__version__}  (installed via: {install.method})")

    res: updater.CliResult | None = None
    refused = ""
    if install.method is updater.Method.EPHEMERAL:
        res = _update_persistent_copy(cli_target, lines)
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
        res = updater.upgrade_cli(install, __version__, cli_target)
        lines.append(f"  {res.message}")
        if res.changed:
            versions.record_installed_cli(res.after)

    restart_needed = False
    pres: updater.PluginResult | None = None
    pi_update: _PiUpdate | None = None
    tap_behind = ""
    source = agent_source()
    if include_plugin:
        # pi's Probe package is updated whatever agent runs this: an Update from
        # a plain terminal (claude_code by default) or Claude Code's auto-update
        # used to skip it, so pi stayed on whatever package it was installed
        # with (2026-10-02: a 0.2.x package under a 0.206 CLI, so pi never
        # switched to the daemon). Its own `pi update <source>`, never a
        # marketplace.
        pi_update = _update_pi_package()
        lines.extend(pi_update.lines)
        # pi has no marketplace plugin, and a cloud agent (Capy) no plugin at
        # all (its app updates itself): for them `pres` stays None, same bucket
        # as `include_plugin=False`.
        from probe.cli import cloud_agents

        if cloud_agents.is_cloud(source):
            lines.append(f"{cloud_agents.module(source).label()}: no Probe plugin to update; its app updates itself.")
        elif source != "pi":
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
            # The sessions still running a tap from before this update: the
            # machine reports the oldest live tap, so a current install beside
            # one of them still reads as the old version until it restarts.
            if pres.attempted and pres.tap_after:
                pres = dataclasses.replace(
                    pres, tap_running_stale=updater.stale_tap_daemons(source, pres.tap_after)
                )
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
                agent = "Codex" if codex else "Kimi Code" if kimi else "Claude Code"
                manual = (
                    updater.manual_codex_plugin_commands()
                    if codex
                    else updater.manual_kimi_plugin_commands()
                    if kimi
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
        # Sessions on an older tap are not a failure, but `probe doctor` is
        # where a person looks, so the local record says it too.
        plugin_detail = tap_behind or (updater.running_stale_note(pres) if pres else "")
    # pi's package is the plugin half for pi: an attempted update that failed
    # fails it, or a detached run (pi's session start) would report success.
    if pi_update is not None and not pi_update.ok:
        plugin_ok = False
        plugin_detail = "; ".join(part for part in (plugin_detail, pi_update.detail) if part)
    plugin_version = pres.after if pres is not None else None

    # The ONLY way a detached auto-update can report failure: it runs with no
    # terminal attached, so without this an updater that has been broken for a
    # month is indistinguishable from one that works. `probe doctor` prints it.
    # BOTH halves are recorded -- the plugin's outcome used to live only in
    # `lines`, which a detached run sends straight to /dev/null.
    attempted_at = int(time.time())
    autoupdate.record_attempt(
        autoupdate.Attempt(
            at=attempted_at,
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
        ),
        agent=_agent_label(source),
    )
    ok = (res.ok if res is not None else True) and plugin_ok

    # The same outcome, to the server, per component -- the local record above
    # is read by `probe doctor` on THIS machine only. Best-effort and bounded;
    # see update_report.
    _report_attempt(
        lambda: update_report.attempt_report(
            trigger=trigger,
            ok=ok,
            at=attempted_at,
            source=source,
            cli=update_report.cli_component(
                res, current=__version__, target=cli_target, refused=refused
            ),
            # No marketplace plugin ran (`pres`) although plugins were asked
            # for: pi, whose package IS its plugin half.
            plugin=(
                update_report.pi_component(pi_update, target=plugin_target)
                if include_plugin and pres is None
                else update_report.plugin_component(pres, target=plugin_target, source=source)
            ),
            tap=update_report.tap_component(pres, target=tap_target),
            legacy_ids=pres.legacy_ids if pres is not None else (),
        ),
        base_url=base_url,
    )

    return UpdateOutcome(
        lines=lines,
        # Both halves, so `probe update`'s exit code means "the update worked",
        # not "the CLI half worked".
        ok=ok,
        restart_needed=restart_needed,
    )


def _agent_label(source: str | None) -> str | None:
    """The coding agent a pass ran for, as `probe doctor` names it."""
    try:
        return get_registry().get(source).label if source else None
    except Exception:  # noqa: BLE001 - only a label
        return source


def _report_attempt(build: Callable[[], dict], *, base_url: str | None = None) -> None:
    """Build the server's update report and send it. NEVER RAISES.

    By the time this runs the update is over and recorded locally (`probe
    doctor` reads that record). A bug in building or sending the report may
    cost the report; it must never turn a finished update into a traceback."""
    try:
        update_report.submit_attempt(build(), base_url=base_url)
    except Exception:  # noqa: BLE001 - see docstring
        pass


@dataclass(frozen=True)
class _PiUpdate:
    """What the pi step did: its lines, and whether an ATTEMPTED update failed
    (skipped -- not installed, another update holding the lock -- is not a
    failure)."""

    lines: list[str]
    ok: bool = True
    detail: str = ""
    #: `pi update` actually ran (a skip did not).
    ran: bool = False
    #: For the server's update report only: which of the returns below this
    #: is, and the package versions either side of it.
    code: update_report.PiStep | None = None
    before: str | None = None
    after: str | None = None


def _package_harness() -> str | None:
    """The extension-family harness whose package `_update_pi_package` moves
    (pi's), from the registry rather than by name."""
    from probe.harness import FAMILY_EXTENSION, get_registry

    return next(
        (h.id for h in get_registry().installable() if h.family == FAMILY_EXTENSION), None
    )


@contextmanager
def _pi_update_lock():
    """One `pi update` at a time on this machine: two runs on one clone (two
    Claude Code windows' auto-updates and a pi start) race git and npm. Yields
    whether this run holds it; without `fcntl` (Windows) it always does."""
    try:
        import fcntl
    except ImportError:
        yield True
        return
    from probe.sdk import session_marker

    try:
        path = session_marker.state_dir() / "pi-update.lock"
        path.parent.mkdir(parents=True, exist_ok=True)
        handle = open(path, "a+")  # noqa: SIM115 - held across the yield
    except OSError:
        # A lock that cannot be opened is never worth failing the update over.
        yield True
        return
    with handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            yield False
            return
        try:
            yield True
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def _update_pi_package() -> _PiUpdate:
    """`pi update` for Probe's pi package when pi has it installed; nothing
    otherwise. Says the versions it moved between, or how to do it by hand.

    It runs while pi does, as pi's own `pi update` does. It used to wait until
    no pi process was left, and a researcher running pi agents around the
    clock never got the package at all (strand-ai, 2026-10-15). A running pi
    keeps the extension and capture watcher it loaded: in real pi 1.0.0, with
    the package's `node_modules` deleted and then `pi update`d from 0.4.0 to
    0.5.0 under it, turns, `/probe-status`, `/probe-mcp-login` and the watcher
    process carried on, `/new` started a session, and `/reload` loaded 0.5.0
    (a running session's capture watcher keeps its old code until pi restarts).
    Killed mid-`npm install`, the orphaned npm still finished `node_modules`.
    Only a pi STARTED during the second or two in which `pi update` has removed
    `node_modules` fails to load the package, and exits 1."""
    from probe.cli import pi_config

    directory = pi_config.installed_package_dir()
    if directory is None or not directory.is_dir():
        autoupdate.mark_pi_update_pending(False)
        return _PiUpdate([], code=update_report.PiStep.NOT_INSTALLED)
    with _pi_update_lock() as held:
        if not held:
            return _PiUpdate(
                ["pi package:", "  another update is updating it now"],
                code=update_report.PiStep.LOCKED,
            )
        before = pi_config.installed_package_version()
        # Owed until it is known to have worked: an updater killed mid-update
        # (it removes and reinstalls `node_modules`) is retried, not forgotten.
        autoupdate.mark_pi_update_pending(True)
        result = pi_config.update_package()
        after = pi_config.installed_package_version()

    def shown(version) -> str:
        return ".".join(str(part) for part in version) if version else "unknown"

    versions_seen = {
        "before": shown(before) if before else None,
        "after": shown(after) if after else None,
    }
    if not result.ok and not getattr(result, "reachable", True):
        # pi itself is gone (uninstalled, its settings still naming us): nothing
        # to update with, which is not an update that failed.
        autoupdate.mark_pi_update_pending(False)
        return _PiUpdate(
            ["pi package:", f"  not updated: {result.detail}"],
            code=update_report.PiStep.UNREACHABLE,
            **versions_seen,
        )
    # A failure stays owed, so pi's next session start tries again.
    autoupdate.mark_pi_update_pending(not result.ok)
    if not result.ok:
        return _PiUpdate(
            ["pi package:", f"  ! not updated ({result.detail}); run `pi update {pi_config.MIRROR_GIT_SOURCE}`"],
            ok=False,
            detail=f"pi package not updated: {result.detail}",
            ran=True,
            code=update_report.PiStep.FAILED,
            **versions_seen,
        )
    if before != after:
        # One line: the attempt record (`update_owed_pi_package`) and the update
        # report read the last line as what happened.
        return _PiUpdate(
            ["pi package:", f"  updated {shown(before)} → {shown(after)} (open pi sessions pick it up when restarted)"],
            ran=True, code=update_report.PiStep.UPDATED, **versions_seen,
        )
    return _PiUpdate(
        ["pi package:", f"  already {shown(after)}"],
        ran=True, code=update_report.PiStep.CURRENT, **versions_seen,
    )


def update_owed_pi_package() -> None:
    """Run ONLY the pi step, for a pi package update that failed
    (`autoupdate.PI_UPDATE_PENDING_FILENAME`) while the CLI itself is current.
    The caller holds the update lock. Records the attempt only when `pi update`
    ran: a skip is not news, and overwriting `last_attempt` with it would hide
    the real one."""
    step = _update_pi_package()
    if not step.ran:
        return
    attempted_at = int(time.time())
    autoupdate.record_attempt(
        autoupdate.Attempt(
            at=attempted_at,
            ok=True,
            from_version=__version__,
            plugin_ok=step.ok,
            plugin_detail=step.detail or f"pi package {step.lines[-1].strip()}",
        )
    )
    # Only pi's step ran: no CLI or tap half to report. pi's session start or a
    # run's end asked for it; the spawner's TRIGGER_ENV says which.
    _report_attempt(
        lambda: update_report.attempt_report(
            trigger=update_report.trigger_from_env(update_report.Trigger.SESSION_START),
            ok=step.ok,
            at=attempted_at,
            source=_package_harness(),
            cli=None,
            plugin=update_report.pi_component(step, target=None),
            tap=None,
        )
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

    boot = bootstrap.ensure_persistent_install(target=cli_target)
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
