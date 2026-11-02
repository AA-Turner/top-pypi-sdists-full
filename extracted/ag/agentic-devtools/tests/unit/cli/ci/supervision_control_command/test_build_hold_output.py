"""Tests for the build_hold_output symbol."""

from __future__ import annotations

from agentic_devtools.cli.ci.supervision_control import HoldReceipt, SupervisionControl
from agentic_devtools.cli.ci.supervision_control_command import build_hold_output, hold_receipt_to_json


def test_build_hold_output_returns_complete_receipt_when_changed() -> None:
    control = SupervisionControl()

    outcome = build_hold_output({"loop.yml": True}, "run-2", control)

    assert outcome["idempotent"] is False
    assert outcome["idempotency_key"] == "run-2:hold"
    receipt = outcome["receipt"]
    assert isinstance(receipt, HoldReceipt)
    assert hold_receipt_to_json(receipt) == {
        "run_id": "run-2",
        "changed_workflows": ["loop.yml"],
        "previous_states": {"loop.yml": True},
    }


def test_build_hold_output_synthesizes_receipt_when_idempotent() -> None:
    control = SupervisionControl()

    outcome = build_hold_output({"loop.yml": False}, "run-2", control)

    assert outcome["idempotent"] is True
    assert outcome["idempotency_key"] == "run-2:hold"
    receipt = outcome["receipt"]
    assert receipt.changed_workflows == ()
    assert receipt.previous_states == {"loop.yml": False}
