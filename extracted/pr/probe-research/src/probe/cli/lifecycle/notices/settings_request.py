"""Probe staff changed a setting on this machine: apply it and acknowledge."""

from __future__ import annotations

import contextlib
import os
from ....sdk.settings.settings import resolve
#: A staff settings change (research-os control/074) is fetched at most this often
#: per machine, under its own stamp (`_settings_request_notice`).
_SETTINGS_REQUEST_EVERY_S = 10 * 60
_SETTINGS_REQUEST_STAMP = "settings-request-ask"


def _settings_request_notice() -> None:
    """Probe staff changed a setting on this machine (research-os control/074): apply
    it once and report it (`probe.cli.lifecycle.remote_settings.apply_pending`). Never raises.

    Gates, cheapest first, like `_capture_repair_notice`: not a run-scoped command
    (`_UPDATE_HOT_PATH_COMMANDS`), not the service, daemon, MCP, update or the
    wizard (`_REMOTE_UPDATE_SKIP_COMMANDS`), not a read-only one
    (`_READ_ONLY_COMMANDS`); a fresh mark; not a command a Probe daemon runs (its
    key is refused); a signed-in API token that IS the config file's current
    context (`_repair_identity_is_the_files`: the change is about THIS machine's
    files, so it is fetched only as the account they belong to); one try per
    `_SETTINGS_REQUEST_EVERY_S` (`_claim_window`).

    A CHILD OF THE PROBE SERVICE APPLIES IT TOO, unlike the other two staff
    requests. On a machine with the service every hook-run `probe` (the team
    note's sync at each session start, Stop and end: `service/jobs/notesync.py`) is
    one, and a person who only uses coding agents may run no other: skipping them
    would leave the request undelivered for good. Applying needs nothing the
    service does not already allow its children: a locked config write, the
    switch's own session write, and `session.recording` asked over the socket.
    """
    command = _invoked_command()
    if (
        command in _UPDATE_HOT_PATH_COMMANDS
        or command in _REMOTE_UPDATE_SKIP_COMMANDS
        or command in _READ_ONLY_COMMANDS
    ):
        return
    try:
        from probe.foundation.remote_settings import preferences as settings_request

        if not settings_request.fresh():
            return
        from probe.sdk.agent_session import DAEMON_SESSION_ENV

        if os.environ.get(DAEMON_SESSION_ENV):
            return
        settings = resolve(base_url=_conn.base_url)
        if not settings.token or not _repair_identity_is_the_files(settings):
            return
        if not _claim_window(_SETTINGS_REQUEST_STAMP, _SETTINGS_REQUEST_EVERY_S):
            return
        from .. import remote_settings

        client = _new_client(base_url=_conn.base_url, spool_dir=_conn.spool_dir)
        try:
            remote_settings.apply_pending(client, base_url=settings.base_url)
        finally:
            with contextlib.suppress(Exception):
                client.close()
    except Exception:  # noqa: BLE001 -- the check never breaks the command it runs before
        pass
from probe.cli.connection import _conn, _new_client  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.lifecycle.lifecycle import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _READ_ONLY_COMMANDS,
    _REMOTE_UPDATE_SKIP_COMMANDS,
    _UPDATE_HOT_PATH_COMMANDS,
    _claim_window,
    _invoked_command,
    _repair_identity_is_the_files,
)
