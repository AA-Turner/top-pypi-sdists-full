"""A send with no swaps has no hidden value on the wire, so its captured payload is kept. Dropping it
stored `{}` in chat.request_snapshot for every ordinary run, and the request checks of the variable-rule
cases (PB-02, PB-04, PB-05A) came back undecided (final after-run, 2026-10-22, run f5848859)."""

from matrx_ai.config.picklist_runtime import redact_wire_payload, set_wire_swaps


def test_payload_is_kept_when_nothing_was_swapped():
    set_wire_swaps({})
    assert redact_wire_payload({"system": "Rider on file: []"}) == {"system": "Rider on file: []"}


def test_no_payload_stays_no_payload():
    set_wire_swaps({})
    assert redact_wire_payload(None) is None
