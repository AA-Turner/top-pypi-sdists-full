"""Probe staff asked to change a setting on this machine (research-os control/074).

Staff can set ONE setting on ONE device, once, and only toward quieter (v1: the
machine's default for new sessions, `off` or `read`). The server answers that
device's authenticated requests with `X-Probe-Settings-Requested: <requested at,
unix seconds>`. Whichever of our clients gets that answer leaves
`settings-requested` in the state folder (`probe._shared.device_mark`); a later
`probe` command, a Probe service child included, applies it
(`probe.cli.remote_settings.apply_pending`).

Stdlib only; never raises (`device_mark`).
"""

from __future__ import annotations

from probe._shared.device_mark import FRESH_S, WRITE_EVERY_S, Mark

#: The server's `app/client_version/settings_requests.py::SETTINGS_REQUEST_HEADER`.
HEADER = "X-Probe-Settings-Requested"
#: The mark, beside `capture-repair-requested`.
FILENAME = "settings-requested"

MARK = Mark(HEADER, FILENAME)
note = MARK.note
fresh = MARK.fresh
clear = MARK.clear
_reset_for_tests = MARK.reset_for_tests

__all__ = ["FILENAME", "FRESH_S", "HEADER", "MARK", "WRITE_EVERY_S", "clear", "fresh", "note"]
