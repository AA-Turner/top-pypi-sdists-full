"""Probe staff asked this machine to update now (research-os control/071).

The server answers any authenticated request from a machine that has an open
request with `X-Probe-Update-Requested: <requested at, unix seconds>`. Whichever
of our clients gets that answer leaves `update-requested` in the state folder
(`probe._shared.device_mark`); the next `probe` command reads it
(`probe.cli.main._remote_update_notice`) and hands an update to this machine's
own updater, under every rule that updater already has.

Stdlib only; never raises (`device_mark`).
"""

from __future__ import annotations

from probe._shared.device_mark import FRESH_S, WRITE_EVERY_S, Mark

#: The server's `app/client_version/update_requests.py::UPDATE_REQUESTED_HEADER`.
HEADER = "X-Probe-Update-Requested"
#: The mark, beside `autoupdate.json`.
FILENAME = "update-requested"

MARK = Mark(HEADER, FILENAME)
note = MARK.note
fresh = MARK.fresh
clear = MARK.clear
_reset_for_tests = MARK.reset_for_tests

__all__ = ["FILENAME", "FRESH_S", "HEADER", "MARK", "WRITE_EVERY_S", "clear", "fresh", "note"]
