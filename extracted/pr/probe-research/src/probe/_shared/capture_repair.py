"""Probe staff asked to repair this machine's session capture (research-os control/073).

A wizard bug could revoke a capture credential nobody turned off (a Settings
commit read a sign-in's pending lock as "capture off" and ran the full
turn-off; Anthrogen, 2026-10-26). Bringing it back used to need the person's
browser approval. Staff can now open a one-time repair for ONE device and its
agents, and the server answers that device's authenticated requests with
`X-Probe-Capture-Repair: <requested at, unix seconds>`. Whichever of our
clients gets that answer leaves `capture-repair-requested` in the state folder
(`probe._shared.device_mark`); the next `probe` command reads it
(`probe.cli.main._capture_repair_notice`), fetches the replacement credentials
(`POST /v1/client/capture-repair`, which closes nothing), writes them where the
wizard's sign-in would, and confirms per agent
(`POST /v1/client/capture-repair/applied`); the request closes once every agent
is settled.

Stdlib only; never raises (`device_mark`).
"""

from __future__ import annotations

from probe._shared.device_mark import FRESH_S, WRITE_EVERY_S, Mark

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
