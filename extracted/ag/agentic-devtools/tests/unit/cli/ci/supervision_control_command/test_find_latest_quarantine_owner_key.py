"""Tests for the find_latest_quarantine_owner_key symbol."""

from __future__ import annotations

import json

import pytest

from agentic_devtools.cli.ci import supervision_control_command
from agentic_devtools.cli.ci.supervision_control import QuarantineReceipt, SupervisionControl
from agentic_devtools.cli.ci.supervision_control_command import (
    OPERATION_RECEIPT_MARKER,
    find_latest_quarantine_owner_key,
    quarantine_receipt_to_json,
)


def _receipt(key: str, receipt: QuarantineReceipt, *, completed: bool = True) -> str:
    return f"{OPERATION_RECEIPT_MARKER}\n" + json.dumps(
        {
            "idempotency_key": key,
            "operation": "quarantine",
            "receipt": quarantine_receipt_to_json(receipt),
            "completed": completed,
        }
    )


def test_find_latest_quarantine_owner_key_is_scoped_to_owned_pr_heads() -> None:
    prior = QuarantineReceipt("run-a", (7, 8), {7: "head-7", 8: "head-8"}, (7, 8))
    no_op = QuarantineReceipt("run-b", (7,), {7: "head-7"}, ())
    other_pr = QuarantineReceipt("run-c", (8,), {8: "head-8"}, (8,))
    bodies = [
        _receipt("run-a:quarantine:7,8", prior),
        _receipt("run-b:quarantine:7", no_op),
        _receipt("run-c:quarantine:8", other_pr),
    ]

    assert find_latest_quarantine_owner_key(SupervisionControl(), bodies, 7, "head-7") == "run-a:quarantine:7,8"
    assert find_latest_quarantine_owner_key(SupervisionControl(), bodies, 8, "head-8") == "run-c:quarantine:8"
    assert find_latest_quarantine_owner_key(SupervisionControl(), bodies, 7, "head-new") is None


def test_find_latest_quarantine_owner_key_rejects_malformed_receipts() -> None:
    for body in (
        f"{OPERATION_RECEIPT_MARKER}\nnot-json",
        f"{OPERATION_RECEIPT_MARKER}\n[]",
        f"{OPERATION_RECEIPT_MARKER}\n" + json.dumps({"operation": "quarantine"}),
        f"{OPERATION_RECEIPT_MARKER}\n"
        + json.dumps({"idempotency_key": "key", "operation": "quarantine", "receipt": {}}),
    ):
        with pytest.raises(RuntimeError):
            find_latest_quarantine_owner_key(SupervisionControl(), [body], 7, "head-7")


def test_find_latest_quarantine_owner_key_skips_unrelated_comments_and_operations() -> None:
    checkpoint = f"{OPERATION_RECEIPT_MARKER}\n" + json.dumps(
        {"idempotency_key": "checkpoint-key", "operation": "checkpoint", "receipt": {}}
    )

    assert (
        find_latest_quarantine_owner_key(
            SupervisionControl(),
            ["ordinary comment", checkpoint],
            7,
            "head-7",
        )
        is None
    )


def test_find_latest_quarantine_owner_key_ignores_uncompleted_write_ahead_receipt() -> None:
    receipt = QuarantineReceipt("run-a", (7,), {7: "head-7"}, (7,))

    assert (
        find_latest_quarantine_owner_key(
            SupervisionControl(),
            [_receipt("run-a:quarantine:7", receipt, completed=False)],
            7,
            "head-7",
        )
        is None
    )


def test_find_latest_quarantine_owner_key_rejects_malformed_completion_marker() -> None:
    receipt = QuarantineReceipt("run-a", (7,), {7: "head-7"}, (7,))
    body = _receipt("run-a:quarantine:7", receipt).replace('"completed": true', '"completed": "true"')

    with pytest.raises(RuntimeError, match="completion marker is malformed"):
        find_latest_quarantine_owner_key(SupervisionControl(), [body], 7, "head-7")


def test_find_latest_quarantine_owner_key_rejects_unexpected_receipt_type(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    receipt = QuarantineReceipt("run-a", (7,), {7: "head-7"}, (7,))
    monkeypatch.setattr(supervision_control_command, "find_operation_receipt", lambda *_args: {})

    with pytest.raises(RuntimeError, match="malformed"):
        find_latest_quarantine_owner_key(
            SupervisionControl(),
            [_receipt("run-a:quarantine:7", receipt)],
            7,
            "head-7",
        )
