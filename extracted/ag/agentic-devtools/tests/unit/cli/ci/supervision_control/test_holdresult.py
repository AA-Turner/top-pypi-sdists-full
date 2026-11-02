"""Tests for the HoldResult symbol."""

from __future__ import annotations

from agentic_devtools.cli.ci.supervision_control import HoldReceipt, HoldResult


def test_hold_result_retains_its_operation_receipt() -> None:
    receipt = HoldReceipt("run-1", ("loop.yml",), {"loop.yml": True})
    result = HoldResult("run-1:hold", receipt)

    assert result.receipt == receipt
