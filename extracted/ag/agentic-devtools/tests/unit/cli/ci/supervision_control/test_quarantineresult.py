"""Tests for the QuarantineResult symbol."""

from __future__ import annotations

from agentic_devtools.cli.ci.supervision_control import IGNORE_LABEL, QuarantineReceipt, QuarantineResult


def test_quarantine_result_retains_its_operation_receipt() -> None:
    receipt = QuarantineReceipt("run-1", (7,), {7: "head-7"}, (7,))
    result = QuarantineResult("run-1:quarantine:key", (7,), {7: frozenset({IGNORE_LABEL})}, receipt)

    assert result.receipt == receipt
    assert result.labels[7] == frozenset({IGNORE_LABEL})
