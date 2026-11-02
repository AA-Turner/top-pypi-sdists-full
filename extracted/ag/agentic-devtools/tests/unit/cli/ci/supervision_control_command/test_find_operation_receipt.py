"""Tests for the find_operation_receipt symbol."""

from __future__ import annotations

import json

import pytest

from agentic_devtools.cli.ci.supervision_control import HoldReceipt, QuarantineReceipt, SupervisionControl
from agentic_devtools.cli.ci.supervision_control_command import (
    OPERATION_RECEIPT_MARKER,
    find_operation_receipt,
    hold_receipt_to_json,
    quarantine_receipt_to_json,
)


def test_find_operation_receipt_recovers_quarantine_and_hold_receipts() -> None:
    control = SupervisionControl()
    quarantine = QuarantineReceipt("run-1", (7,), {7: "head-7"}, (7,))
    hold = HoldReceipt("run-2", ("loop.yml",), {"loop.yml": True})
    ensure_labels = {
        "labels_created": ["ai-pr-loop-ignore"],
        "labels_reused": ["ai-pr-loop-supervised"],
        "control_issue": 42,
        "control_issue_created": False,
    }
    restore = {"run_id": "run-1", "quarantine_key": "q-key", "changed": [7]}
    resume = {"run_id": "run-2", "hold_key": "h-key", "states": {"loop.yml": True}}
    comments = [
        f"{OPERATION_RECEIPT_MARKER}\n"
        + json.dumps(
            {
                "idempotency_key": "q-key",
                "operation": "quarantine",
                "receipt": quarantine_receipt_to_json(quarantine),
            }
        ),
        f"{OPERATION_RECEIPT_MARKER}\n"
        + json.dumps(
            {
                "idempotency_key": "h-key",
                "operation": "hold",
                "receipt": hold_receipt_to_json(hold),
            }
        ),
        f"{OPERATION_RECEIPT_MARKER}\n"
        + json.dumps(
            {
                "idempotency_key": "ensure-key",
                "operation": "ensure-labels",
                "receipt": ensure_labels,
            }
        ),
        f"{OPERATION_RECEIPT_MARKER}\n"
        + json.dumps(
            {
                "idempotency_key": "restore-key",
                "operation": "restore-prs",
                "receipt": restore,
            }
        ),
        f"{OPERATION_RECEIPT_MARKER}\n"
        + json.dumps(
            {
                "idempotency_key": "resume-key",
                "operation": "resume",
                "receipt": resume,
            }
        ),
    ]

    assert find_operation_receipt(control, comments, "quarantine", "q-key") == quarantine
    assert find_operation_receipt(control, comments, "hold", "h-key") == hold
    assert find_operation_receipt(control, comments, "ensure-labels", "ensure-key") == ensure_labels
    assert find_operation_receipt(control, comments, "restore-prs", "restore-key") == restore
    assert find_operation_receipt(control, comments, "resume", "resume-key") == resume
    assert find_operation_receipt(control, ["unrelated"], "hold", "missing") is None


@pytest.mark.parametrize(
    "body",
    [
        f"{OPERATION_RECEIPT_MARKER}\nnot-json",
        f"{OPERATION_RECEIPT_MARKER}\n[]",
        f"{OPERATION_RECEIPT_MARKER}\n{{}}",
    ],
)
def test_find_operation_receipt_fails_closed_on_malformed_records(body: str) -> None:
    with pytest.raises(RuntimeError, match="stored operation receipt"):
        find_operation_receipt(SupervisionControl(), [body], "hold", "key")


def test_find_operation_receipt_rejects_key_reuse_and_conflicting_records() -> None:
    control = SupervisionControl()
    first = HoldReceipt("run-1", ("loop.yml",), {"loop.yml": True})
    second = HoldReceipt("run-1", (), {"loop.yml": False})

    def comment(receipt: HoldReceipt, operation: str = "hold") -> str:
        return f"{OPERATION_RECEIPT_MARKER}\n" + json.dumps(
            {
                "idempotency_key": "key",
                "operation": operation,
                "receipt": hold_receipt_to_json(receipt),
            }
        )

    with pytest.raises(RuntimeError, match="different operation"):
        find_operation_receipt(control, [comment(first)], "quarantine", "key")
    with pytest.raises(RuntimeError, match="conflicting durable receipts"):
        find_operation_receipt(control, [comment(first), comment(second)], "hold", "key")
    with pytest.raises(ValueError, match="unsupported durable receipt operation"):
        find_operation_receipt(control, [comment(first, "checkpoint")], "checkpoint", "key")


@pytest.mark.parametrize(
    ("operation", "receipt"),
    [
        (
            "ensure-labels",
            {"labels_created": [], "labels_reused": [], "control_issue": 42, "control_issue_created": False},
        ),
        ("restore-prs", {"run_id": "run-1", "quarantine_key": "q-key", "changed": [True]}),
        ("resume", {"run_id": "run-1", "hold_key": "h-key", "states": {"loop.yml": 1}}),
    ],
)
def test_find_operation_receipt_rejects_malformed_mutation_receipts(
    operation: str,
    receipt: dict[str, object],
) -> None:
    body = f"{OPERATION_RECEIPT_MARKER}\n" + json.dumps(
        {"idempotency_key": "key", "operation": operation, "receipt": receipt}
    )

    with pytest.raises(RuntimeError, match="receipt is malformed"):
        find_operation_receipt(SupervisionControl(), [body], operation, "key")
