"""the every-command version check: nudge from the cached manifest, decide whether an update is owed now, and an extension harness's session-start upkeep (owed package update or pin)."""

from __future__ import annotations
import os
import sys

import typer

from .... import __version__
from probe.cli.lifecycle.update_spawn import (
    _SERVICE_ASK_EVERY_S,
    _hand_update_to_service,
    _service_owns_updates,
    _spawn_autoupdate,
    _spawn_session_start_update,
    _spawn_version_refresh,
)


#: Where the CLI's own updater runs (no Probe service), a command off a terminal
#: starts it at most this often (C3): the every-command ask's window, under a
#: stamp of its own beside `autoupdate.json` (`_claim_window`).
_CLI_UPDATE_EVERY_S = _SERVICE_ASK_EVERY_S
_CLI_UPDATE_STAMP = "cli-update-ask"


def _version_notice() -> None:
    """The every-command version check: nudge from cache, refresh in background.

    Same contract as _outbox_notice below -- cheap reads, no network, never
    raises -- because it runs before every command including `probe log` inside
    training loops.

    THE GATE ORDER IS LOAD-BEARING, cheapest and most-likely-to-exit first:

        enabled?          one small read (`version_policy.autoupdate_state`): on
                          for the managed CLI unless turned off, opt-in for any
                          other install, which touches exactly one file and stops
        cache fresh?      one ~150-byte read; this is where ~99.9% of calls
                          exit, which is what makes the trigger free in a loop
        (spawn refresher) detached; this process NEVER fetches inline. A 3s
                          timeout on the hot path would put a periodic stall
                          inside training loops, attributed to anything but us.
                          Not for the wizard (`_WIZARD_COMMANDS`): its own one
                          server call carries the manifest
        update available? pure comparison, no I/O
        denylisted?       frozenset membership
        run in flight?    the only O(N) check: it scans a directory and probes
                          locks. Never reached unless an upgrade would otherwise
                          be applied right now. A day at most (`defer_for_run`)
        off a terminal?   once per `_CLI_UPDATE_EVERY_S` (`_claim_window`); a
                          terminal's command starts it every time, as before

    A skip at the denylist or a run is RECORDED, so `probe doctor` can tell a box
    that is correctly deferring from an auto-updater that has silently died.
    There was a TTY gate before the denylist, refusing (and recording `not an
    interactive terminal`) for every command off a terminal; it went (C3),
    except on Windows, where a child cannot detach from its caller.

    WHERE THE PROBE SERVICE IS THE UPDATER (POSIX, `_service_owns_updates`) the
    last three gates are not this command's: they guard an update THIS process
    would start in place, and here it only asks the service, which applies an
    update beside the running version or on a quiet machine and records its own
    deferral when it waits. So the CLI hands the update over
    (`_hand_update_to_service`) and records nothing. Applying the old gates
    there refused nothing real and said the wrong thing: every hook and daemon
    `probe` recorded "not an interactive terminal" (293 times in three hours on
    one laptop, 2026-10-23, the SessionStart hook's own `probe service
    check-now` among them), each one overwriting the service's real reason in
    `last_skip`, which is what the server's update report carries.
    """
    try:
        from probe.shared.updates import version_policy

        if not version_policy.autoupdate_enabled():
            return

        manifest, fetched_at, ok = version_policy.read_cache()
        if (
            not version_policy.cache_is_fresh(fetched_at, ok)
            and _invoked_command() not in _WIZARD_COMMANDS
        ):
            _spawn_version_refresh()

        from ...install import updater

        latest = isinstance(manifest, dict) and updater.cli_update_available(manifest, __version__)
        if not latest:
            # Cold cache or CLI current: nothing to apply, except a pi package
            # update that failed, which pi's session start retries.
            _retry_owed_pi_update()
            return

        from probe.shared.updates import autoupdate

        typer.echo(
            f"probe {__version__} -> {latest} available (`probe wizard --action update`)",
            err=True,
        )

        if _service_owns_updates():
            if _extension_session_start():
                _spawn_session_start_update()
            else:
                _hand_update_to_service(_invoked_command())
            return
        # The CLI's own updater (Windows, an install with no service
        # interpreter): these gates guard the in-place update it would start.
        if not hasattr(os, "fork") and not sys.stdout.isatty():
            # Windows only (out of C3's scope): a child of a command off a
            # terminal there cannot detach from its caller (pi's session start
            # included, `_extension_session_start`), so it is refused as before.
            autoupdate.record_skip(autoupdate.SKIP_NOT_A_TTY, available=latest)
            return
        # The two skips below can also be pi's session start; the record says
        # which, for the server's update report (`update_report`).
        if _invoked_command() in _UPDATE_HOT_PATH_COMMANDS:
            autoupdate.record_skip(
                autoupdate.SKIP_HOT_PATH_COMMAND, available=latest, trigger=_update_trigger()
            )
            return

        from probe.foundation.durable import run_lock

        # A live run holds the update off for a day at most, as the Probe
        # service's does (C3): `defer_for_run` records the skip and the hold;
        # a check that finds none ends the hold. (A Probe daemon's command, or
        # a daemon worker recording, holds every spawn off: `_spawn_update`.)
        live = run_lock.any_live()
        if live and autoupdate.defer_for_run(available=latest, trigger=_update_trigger()):
            return
        if not live:
            autoupdate.clear_run_deferral()

        from probe.sdk.agent_session import DAEMON_SESSION_ENV

        if os.environ.get(DAEMON_SESSION_ENV):
            return  # never from a Probe daemon's command (`_spawn_update`): its window stays unclaimed
        if _extension_session_start():
            _spawn_session_start_update()
        elif sys.stdout.isatty() or _claim_window(_CLI_UPDATE_STAMP, _CLI_UPDATE_EVERY_S):
            # No terminal is no reason to wait (C3): the update is detached and
            # waits for this command to exit. It used to be refused here, and a
            # machine whose only `probe` calls come from hooks or an agent's
            # shell never updated (an Anthrogen pod sat on 0.283.0). Off a
            # terminal, once per window: those callers run `probe` dozens of
            # times an hour.
            _spawn_autoupdate(available=latest)
    except Exception:  # noqa: BLE001 -- a version check must never break a command
        pass


def _update_trigger():
    """`Trigger.SESSION_START` for an extension harness's session start, else
    `Trigger.CLI` (`autoupdate.Trigger`: stdlib-only, cheap on this path).

    Cheapest test first: this runs on the every-command path, and only an
    extension harness's `probe session initialize`, which always names its
    harness in PROBE_AGENT, can be a session start -- so a `probe log` never
    loads the harness registry to find out it is not one."""
    from probe.shared.updates.autoupdate import Trigger

    if not os.environ.get("PROBE_AGENT") or _invoked_command() != "session":
        return Trigger.CLI
    return Trigger.SESSION_START if _extension_session_start() else Trigger.CLI


def _retry_owed_pi_update() -> None:
    """pi's session start, with a pi package update still owed because the last
    one failed (`autoupdate.pi_update_due`): try it again now. No run check: it
    touches pi's package, never the CLI a run imports from."""
    from probe.shared.harness.harnesses.pi.session_pin import _ensure_pi_pin
    if not _extension_session_start():
        return
    from probe.shared.updates import autoupdate

    if autoupdate.pi_update_due():
        _spawn_session_start_update()
        return
    _ensure_pi_pin()


def _extension_session_start() -> bool:
    """`probe session initialize` from an extension-family harness (pi): that
    harness's session start, the moment Claude Code's SessionStart hook updates
    from (`hooks/version_check.py`). pi has no hook, and every `probe` call its
    extension makes is off a terminal, so the TTY gate refused all of them and
    pi never auto-updated at all (2026-10-02). The update is detached and waits
    for this command to exit, exactly as it does from a terminal."""
    import sys as _sys

    from probe.foundation.harness_registry import FAMILY_EXTENSION, get_registry

    if not hasattr(os, "fork"):
        # Windows: the update cannot detach, so it would run inline and wait
        # for this command to exit -- past the extension's 5 s budget for it.
        return False
    harness = get_registry().find(os.environ.get("PROBE_AGENT"))
    argv = _sys.argv[1:]
    return (
        harness is not None
        and harness.family == FAMILY_EXTENSION
        and _invoked_command() == "session"
        and "initialize" in argv
    )
from probe.cli.lifecycle.lifecycle import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _UPDATE_HOT_PATH_COMMANDS,
    _WIZARD_COMMANDS,
    _claim_window,
    _invoked_command,
)
