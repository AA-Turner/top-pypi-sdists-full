"""Tests for the parse_hold_receipt symbol."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.supervision_control import HoldReceipt
from agentic_devtools.cli.ci.supervision_control_command import hold_receipt_to_json, parse_hold_receipt


def test_parse_hold_receipt_round_trips() -> None:
    receipt = HoldReceipt("run-1", ("loop.yml",), {"loop.yml": True, "watchdog.yml": False})
    assert parse_hold_receipt(hold_receipt_to_json(receipt)) == receipt


@pytest.mark.parametrize(
    "raw",
    [
        "not-a-dict",
        {"run_id": " ", "changed_workflows": [], "previous_states": {}},
        {"run_id": "r1", "changed_workflows": "not-a-list", "previous_states": {}},
        {"run_id": "r1", "changed_workflows": [""], "previous_states": {}},
        {"run_id": "r1", "changed_workflows": [], "previous_states": "not-a-dict"},
        {"run_id": "r1", "changed_workflows": [], "previous_states": {"loop.yml": "yes"}},
    ],
)
def test_parse_hold_receipt_rejects_malformed_payloads(raw: object) -> None:
    with pytest.raises(ValueError):
        parse_hold_receipt(raw)
