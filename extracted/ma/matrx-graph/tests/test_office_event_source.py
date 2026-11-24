"""The office arm of the ONE trigger home (office integration W11).

An office trigger is a kind='event' workflow.trigger whose event_source is ``source: 'office'``. It
validates by what it watches, and never as a table or store source (each arm's emitter selects on its own
keys). Before W11 an ``office`` source did not validate at all.
"""

from __future__ import annotations

from uuid import uuid4

import pytest
from pydantic import ValidationError

from matrx_graph.db.trigger_store import (
    OfficeEventSource,
    StoreEventSource,
    TableEventSource,
    event_source_json,
    validate_event_source,
)


def test_a_range_trigger_validates_into_the_office_arm() -> None:
    rid = str(uuid4())
    spec = validate_event_source({"source": "office", "event": "sheet.range_changed", "record_id": rid,
                                  "sheet": "Sales", "range": "B2:D20"})
    assert isinstance(spec, OfficeEventSource)
    assert not isinstance(spec, (TableEventSource, StoreEventSource))
    stored = event_source_json(spec)
    assert stored["source"] == "office" and stored["record_id"] == rid and stored["range"] == "B2:D20"
    assert stored["debounce_seconds"] is None  # unset = the office.trigger_debounce_seconds knob


@pytest.mark.parametrize(
    ("body", "said"),
    [
        ({"event": "sheet.range_changed"}, "needs the A1 range"),
        ({"event": "live_table.record_changed"}, "needs the live table tab"),
        ({"event": "document.saved", "range": "A1:B2"}, "watches the whole document"),
        ({"event": "sheet.range_changed", "range": "A1", "debounce_seconds": -1}, "greater than or equal"),
        ({"event": "sheet.range_changed", "range": "A1", "table": "x.y"}, "Extra inputs"),
    ],
)
def test_an_office_trigger_that_watches_nothing_is_refused(body: dict, said: str) -> None:
    with pytest.raises(ValidationError, match=said):
        validate_event_source({"source": "office", "record_id": str(uuid4()), **body})


def test_a_document_trigger_needs_only_the_document() -> None:
    spec = validate_event_source({"source": "office", "event": "document.saved", "record_id": str(uuid4()),
                                  "debounce_seconds": 5})
    assert isinstance(spec, OfficeEventSource) and spec.debounce_seconds == 5
