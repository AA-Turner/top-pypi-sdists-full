"""Staff asked to change ONE setting on ONE device, once, only quieter (research-os control/074; v1: new-session default).

The `settings-requested` mark (`off`/`read`); the Probe service's chores child applies it via `probe.cli.lifecycle.remote_settings.apply_pending`; stdlib, never raises.
"""

from __future__ import annotations

from probe.foundation.remote_settings.remote_settings import FRESH_S, WRITE_EVERY_S, Mark

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
