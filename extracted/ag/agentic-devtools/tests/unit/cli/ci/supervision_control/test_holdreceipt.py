"""Tests for the HoldReceipt symbol."""

from __future__ import annotations

from agentic_devtools.cli.ci.supervision_control import HoldReceipt


def test_hold_receipt_retains_its_original_states() -> None:
    receipt = HoldReceipt("run-1", ("loop.yml",), {"loop.yml": True})

    assert receipt.previous_states == {"loop.yml": True}
