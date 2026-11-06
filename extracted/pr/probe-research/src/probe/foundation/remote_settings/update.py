"""Staff asked this machine to update now (research-os control/071): the `update-requested` mark.

Acted on by the Probe service's timer (`probe.service.chores`) through its updater. Stdlib only; never raises.
"""

from __future__ import annotations

from probe.foundation.remote_settings.remote_settings import FRESH_S, WRITE_EVERY_S, Mark

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
