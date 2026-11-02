"""Tests for the parse_quarantine_receipt symbol."""

from __future__ import annotations

import json

import pytest

from agentic_devtools.cli.ci.supervision_control import QuarantineReceipt
from agentic_devtools.cli.ci.supervision_control_command import parse_quarantine_receipt, quarantine_receipt_to_json


def test_parse_quarantine_receipt_round_trips() -> None:
    receipt = QuarantineReceipt("run-1", (7, 8), {7: "head-7", 8: "head-8"}, (7,))
    wire = json.loads(json.dumps(quarantine_receipt_to_json(receipt)))
    assert parse_quarantine_receipt(wire) == receipt


def test_parse_quarantine_receipt_defaults_ignore_added_when_absent_for_backward_compatibility() -> None:
    receipt = parse_quarantine_receipt({"run_id": "run-1", "changed": [7], "heads": {"7": "head-7"}})
    assert receipt.ignore_added == ()


@pytest.mark.parametrize(
    "raw",
    [
        "not-a-dict",
        {"run_id": " ", "changed": [], "heads": {}},
        {"run_id": "r1", "changed": "not-a-list", "heads": {}},
        {"run_id": "r1", "changed": [True], "heads": {}},
        {"run_id": "r1", "changed": [0], "heads": {"0": "head-0"}},
        {"run_id": "r1", "changed": [7, 7], "heads": {"7": "head-7"}},
        {"run_id": "r1", "changed": [7], "heads": "not-a-dict"},
        {"run_id": "r1", "changed": [7], "heads": {"x": "head"}},
        {"run_id": "r1", "changed": [7], "heads": {"0": "head-0"}},
        {"run_id": "r1", "changed": [7], "heads": {"07": "head-a", "7": "head-b"}},
        {"run_id": "r1", "changed": [7], "heads": {"7": ""}},
        {"run_id": "r1", "changed": [7], "heads": {"7": "head-7"}, "ignore_added": "not-a-list"},
        {"run_id": "r1", "changed": [7], "heads": {"7": "head-7"}, "ignore_added": [True]},
        {"run_id": "r1", "changed": [7], "heads": {"7": "head-7"}, "ignore_added": [0]},
        {"run_id": "r1", "changed": [7], "heads": {"7": "head-7"}, "ignore_added": [7, 7]},
        {"run_id": "r1", "changed": [7], "heads": {"7": "head-7"}, "ignore_added": [8]},
        {"run_id": "r1", "changed": [7, 8], "heads": {"7": "head-7"}, "ignore_added": [7]},
    ],
)
def test_parse_quarantine_receipt_rejects_malformed_payloads(raw: object) -> None:
    with pytest.raises(ValueError):
        parse_quarantine_receipt(raw)
