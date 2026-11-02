"""Tests for the completed operation receipt lookup."""

from __future__ import annotations

import json

import pytest

from agentic_devtools.cli.ci.supervision_control import SupervisionControl
from agentic_devtools.cli.ci.supervision_control_command import (
    OPERATION_RECEIPT_MARKER,
    find_completed_operation_receipt,
)


def _record(
    *,
    operation: str = "resume",
    completed: object = False,
    idempotency_key: str | None = None,
) -> str:
    if operation == "restore-prs":
        receipt: dict[str, object] = {"run_id": "run-1", "quarantine_key": "run-1:quarantine:key", "changed": [7]}
        key = idempotency_key or "run-1:quarantine:key:restore"
    else:
        receipt = {"run_id": "run-1", "hold_key": "run-1:hold", "states": {"workflow.yml": True}}
        key = idempotency_key or "run-1:resume"
    return f"{OPERATION_RECEIPT_MARKER}\n" + json.dumps(
        {
            "idempotency_key": key,
            "operation": operation,
            "receipt": receipt,
            "completed": completed,
        }
    )


def test_find_completed_operation_receipt_returns_only_published_completion() -> None:
    control = SupervisionControl()
    write_ahead = _record()
    completed = _record(completed=True)

    assert find_completed_operation_receipt(control, [], "resume", "run-1:resume") is None
    assert (
        find_completed_operation_receipt(control, ["unrelated comment", write_ahead], "resume", "run-1:resume") is None
    )
    assert find_completed_operation_receipt(control, [completed], "resume", "run-1:resume") == {
        "run_id": "run-1",
        "hold_key": "run-1:hold",
        "states": {"workflow.yml": True},
    }


def test_find_completed_operation_receipt_ignores_other_operations_and_keys() -> None:
    control = SupervisionControl()

    assert (
        find_completed_operation_receipt(
            control,
            [_record(operation="restore-prs", completed=True)],
            "resume",
            "run-1:resume",
        )
        is None
    )
    assert (
        find_completed_operation_receipt(
            control,
            [_record(completed=True, idempotency_key="other:resume")],
            "resume",
            "run-1:resume",
        )
        is None
    )


def test_find_completed_operation_receipt_rejects_invalid_completion_markers() -> None:
    control = SupervisionControl()

    with pytest.raises(ValueError, match="unsupported completion operation"):
        find_completed_operation_receipt(control, [], "quarantine", "run-1:quarantine")
    with pytest.raises(RuntimeError, match="completion marker is malformed"):
        find_completed_operation_receipt(control, [_record(completed="yes")], "resume", "run-1:resume")


def test_find_completed_operation_receipt_rejects_malformed_matching_receipt() -> None:
    control = SupervisionControl()
    malformed = f"{OPERATION_RECEIPT_MARKER}\n" + json.dumps(
        {
            "idempotency_key": "run-1:resume",
            "operation": "resume",
            "receipt": {"run_id": "run-1", "hold_key": "run-1:hold", "states": []},
            "completed": True,
        }
    )

    with pytest.raises(RuntimeError, match="stored resume receipt is malformed"):
        find_completed_operation_receipt(control, [malformed], "resume", "run-1:resume")
