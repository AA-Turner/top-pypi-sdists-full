"""Tests for the hold_receipt_to_json symbol."""

from __future__ import annotations

import json

from agentic_devtools.cli.ci.supervision_control import HoldReceipt
from agentic_devtools.cli.ci.supervision_control_command import hold_receipt_to_json, parse_hold_receipt


def test_hold_receipt_to_json_returns_round_trippable_json_shape() -> None:
    receipt = HoldReceipt("run-1", ("ai-pr-loop.yml",), {"ai-pr-loop.yml": True, "watchdog.yml": False})

    encoded = json.dumps(hold_receipt_to_json(receipt))

    assert parse_hold_receipt(json.loads(encoded)) == receipt
