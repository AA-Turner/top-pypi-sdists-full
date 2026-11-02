"""Tests for the build_quarantine_output symbol."""

from __future__ import annotations

from agentic_devtools.cli.ci.supervision_control import PRObservation, QuarantineReceipt, SupervisionControl
from agentic_devtools.cli.ci.supervision_control_command import build_quarantine_output, quarantine_receipt_to_json


def _observation(number: int, head: str, *labels: str) -> PRObservation:
    return PRObservation(number, head, frozenset(labels))


def test_build_quarantine_output_returns_complete_receipt_when_changed() -> None:
    control = SupervisionControl()
    observations = [_observation(7, "head-7")]

    outcome = build_quarantine_output(observations, {7: "head-7"}, "run-1", control)

    assert outcome["idempotent"] is False
    assert outcome["idempotency_key"].startswith("run-1:quarantine:")
    receipt = outcome["receipt"]
    assert isinstance(receipt, QuarantineReceipt)
    assert receipt.heads == {7: "head-7"}
    assert receipt.ignore_added == (7,)
    assert quarantine_receipt_to_json(receipt) == {
        "run_id": "run-1",
        "changed": [7],
        "heads": {7: "head-7"},
        "ignore_added": [7],
    }


def test_build_quarantine_output_does_not_record_ownership_for_pre_existing_ignore_label() -> None:
    control = SupervisionControl()
    observations = [_observation(7, "head-7", "ai-pr-loop-ignore")]

    outcome = build_quarantine_output(observations, {7: "head-7"}, "run-1", control)

    receipt = outcome["receipt"]
    assert receipt.changed == (7,)
    assert receipt.ignore_added == ()


def test_build_quarantine_output_synthesizes_receipt_when_idempotent() -> None:
    control = SupervisionControl()
    observations = [_observation(7, "head-7", "ai-pr-loop-ignore", "ai-pr-loop-supervised")]

    outcome = build_quarantine_output(observations, {7: "head-7"}, "run-1", control)

    assert outcome["idempotent"] is True
    assert outcome["idempotency_key"].startswith("run-1:quarantine:")
    receipt = outcome["receipt"]
    assert receipt.changed == ()
    assert receipt.heads == {7: "head-7"}
    assert receipt.ignore_added == ()
