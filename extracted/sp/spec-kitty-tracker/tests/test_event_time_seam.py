"""A15: event/time seam (REQ-05).

TrackerEvent.timestamp is provider occurrence time; Tracker takes no
dependency on spec_kitty_events and emits no spec_kitty_events envelope
(no-import half is covered by test_no_forbidden_imports.py::
test_tracker_source_imports_no_forbidden_module — spec_kitty_events is in
the forbidden set). The tracker_sync_pushed_at vs updated_at
disambiguation is covered by test_tracker_egress_time.py.

This file pins the remaining A15 obligations owned by TRK-M1-02:

- local connectors that cannot observe a real event stream say so
  honestly by returning an empty page (([], None)), rather than
  fabricating one — BeadsConnector.list_events and FPConnector.list_events
  both stay ([], None) (draft A15: "honest absence, not a fake stream");
- no event-stream capability flag is added to TrackerCapabilities (draft
  D18/A15: "no event-stream flag is added — list_events returning an
  empty page is the negotiated signal").
"""

from __future__ import annotations

import dataclasses

import pytest

from spec_kitty_tracker.capabilities import TrackerCapabilities
from spec_kitty_tracker.connectors.beads import BeadsConnector
from spec_kitty_tracker.connectors.fp import FPConnector


@pytest.mark.asyncio
async def test_beads_connector_list_events_is_honest_empty_absence() -> None:
    connector = BeadsConnector()
    events, cursor = await connector.list_events(cursor=None, limit=50)
    assert events == []
    assert cursor is None


@pytest.mark.asyncio
async def test_fp_connector_list_events_is_honest_empty_absence() -> None:
    connector = FPConnector()
    events, cursor = await connector.list_events(cursor=None, limit=50)
    assert events == []
    assert cursor is None


def test_no_event_stream_capability_flag_exists() -> None:
    field_names = {f.name for f in dataclasses.fields(TrackerCapabilities)}
    event_stream_like = {name for name in field_names if "event" in name.lower()}
    assert event_stream_like == set(), (
        f"Unexpected event-stream capability flag(s) {sorted(event_stream_like)}: "
        "A15/D18 keep list_events()'s empty page as the sole negotiated signal "
        "for 'this connector cannot observe an event stream', not a flag."
    )
