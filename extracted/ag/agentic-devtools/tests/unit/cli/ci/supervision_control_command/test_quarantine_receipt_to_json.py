"""Tests for the quarantine_receipt_to_json symbol."""

from __future__ import annotations

import json

from agentic_devtools.cli.ci.supervision_control import QuarantineReceipt
from agentic_devtools.cli.ci.supervision_control_command import (
    parse_quarantine_receipt,
    quarantine_receipt_to_json,
)


def test_quarantine_receipt_to_json_returns_round_trippable_json_shape() -> None:
    receipt = QuarantineReceipt("run-1", (7,), {7: "head-7"}, (7,))

    encoded = json.dumps(quarantine_receipt_to_json(receipt))

    assert parse_quarantine_receipt(json.loads(encoded)) == receipt
