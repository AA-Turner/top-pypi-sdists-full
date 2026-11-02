"""Tests for the QuarantineReceipt symbol."""

from __future__ import annotations

from agentic_devtools.cli.ci.supervision_control import QuarantineReceipt


def test_quarantine_receipt_retains_its_ownership_fields() -> None:
    receipt = QuarantineReceipt("run-1", (7,), {7: "head-7"}, (7,))

    assert receipt.ignore_added == (7,)
    assert receipt.heads == {7: "head-7"}
