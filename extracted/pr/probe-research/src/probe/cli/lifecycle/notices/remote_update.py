"""Probe staff asked this machine to update now: hand the update to its updater."""

from __future__ import annotations
import os

#: Probe staff asked this machine to update now (research-os control/071): a
#: `probe` command that finds the mark (`probe.foundation.remote_settings.update`) hands an
#: update to the updater at most this often, while the server keeps asking.
_REMOTE_ASK_EVERY_S = 15 * 60
#: Its stamp, beside `autoupdate.json` (its own window: an every-command ask the
#: service answered `recent` must not hold a remote one back).
_REMOTE_ASK_STAMP = "remote-update-ask"


def _remote_update_notice() -> None:
    """Probe staff asked this machine to update now: hand an update to its own
    updater. Never raises, prints nothing.

    The server marks the machine (research-os control/071) and answers its
    authenticated requests with `X-Probe-Update-Requested`; whichever of our
    clients got that answer left the mark (`probe.foundation.remote_settings.update`). This
    runs before every command, so its gates are cheapest first and nearly every
    call ends at the second one, a missing file:

        command      not run-scoped (`_UPDATE_HOT_PATH_COMMANDS`: nothing is ever
                     started from inside a training loop), not `service`,
                     `daemon` or the wizard (`_REMOTE_UPDATE_SKIP_COMMANDS`)
        the mark     present and seen within `update_request.FRESH_S`
        not a child of the Probe service (`paths.SERVICE_CHILD_ENV`)
        auto-update  on: turning it off is the person's choice, and staff asking
                     never overrides it
        the window   one ask per `_REMOTE_ASK_EVERY_S` (`_claim_window`)

    Then the updater the machine already has, with its own rules:
    - the Probe service (POSIX): `update.check_now`, the every-command check's
      ask (`_ask_service_to_update`), but whether or not the cached manifest
      shows an update (the service fetches its own). A running cycle, its
      `recent` cooldown and every quiet and deferral rule stand; the next window
      asks again while the server keeps asking.
    - no service (Windows, an install with no service interpreter): the update
      lands in place, so nothing may be running from the CLI's files. Not from a
      command a Probe daemon runs (`PROBE_DAEMON_SESSION`), nor while a daemon
      worker holds its lock, and a live run lock records `run in flight` and stops
      here (for a day at most: `autoupdate.defer_for_run`), as the every-command
      check does; otherwise `version_refresh --apply-if-newer` (a fresh
      manifest, the update lock, the run lock again in the child), the
      session-start update. Every `probe` on a machine that only runs
      coding-agent hooks is off a terminal, which is how two customer machines
      sat two days behind (2026-10-24): no TTY gate here either.
    """
    command = _invoked_command()
    if command in _UPDATE_HOT_PATH_COMMANDS or command in _REMOTE_UPDATE_SKIP_COMMANDS:
        return
    try:
        from probe.foundation.remote_settings import update as update_request

        if not update_request.fresh():
            return
        from probe.foundation.service_api.paths import SERVICE_CHILD_ENV

        if os.environ.get(SERVICE_CHILD_ENV):
            return
        from probe.shared.updates import version_policy

        if not version_policy.autoupdate_enabled():
            return
        if not _claim_window(_REMOTE_ASK_STAMP, _REMOTE_ASK_EVERY_S):
            return
        if _service_owns_updates():
            _ask_service_to_update("cli")
            return
        from probe.sdk.agent_session import DAEMON_SESSION_ENV

        if os.environ.get(DAEMON_SESSION_ENV):
            return
        from probe.service.updater.quiet.workers import daemon_worker_running

        from probe.shared.updates import autoupdate
        from probe.foundation.durable import run_lock

        if daemon_worker_running():
            autoupdate.record_skip(autoupdate.SKIP_DAEMON_RECORDING)
            return
        live = run_lock.any_live()
        if live and autoupdate.defer_for_run():  # a day at most (C3)
            return
        if not live:
            autoupdate.clear_run_deferral()
        _spawn_update("--apply-if-newer")
    except Exception:  # noqa: BLE001 -- the check never breaks the command it runs before
        pass
from probe.cli.lifecycle.lifecycle import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _REMOTE_UPDATE_SKIP_COMMANDS,
    _UPDATE_HOT_PATH_COMMANDS,
    _claim_window,
    _invoked_command,
)
from probe.cli.lifecycle.update_spawn import _ask_service_to_update, _service_owns_updates, _spawn_update  # noqa: E402 -- pieces need each other; the front door loads this one first
