"""Staff asked to repair this machine's session capture (research-os control/073): the `capture-repair-requested` mark.

Acted on by `probe.cli.lifecycle.notices.capture_repair._capture_repair_notice`, run by the Probe service's timer (`probe.service.chores`). Stdlib only; never raises. Why (Anthrogen, 2026-10-26): DESIGN.md.
"""

from __future__ import annotations

from probe.foundation.remote_settings.remote_settings import FRESH_S, WRITE_EVERY_S, Mark

#: The server's `app/client_version/capture_repairs.py::CAPTURE_REPAIR_HEADER`.
HEADER = "X-Probe-Capture-Repair"
#: The mark, beside `update-requested`.
FILENAME = "capture-repair-requested"

MARK = Mark(HEADER, FILENAME)
note = MARK.note
fresh = MARK.fresh
clear = MARK.clear
_reset_for_tests = MARK.reset_for_tests

__all__ = ["FILENAME", "FRESH_S", "HEADER", "MARK", "WRITE_EVERY_S", "clear", "fresh", "note"]
