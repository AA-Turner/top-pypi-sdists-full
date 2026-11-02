"""Tests for the find_latest_operation_receipt_key symbol."""

from __future__ import annotations

import json

import pytest

from agentic_devtools.cli.ci.supervision_control import HoldReceipt, SupervisionControl
from agentic_devtools.cli.ci.supervision_control_command import (
    OPERATION_RECEIPT_MARKER,
    find_latest_operation_receipt_key,
    hold_receipt_to_json,
)


def _receipt(key: str, operation: str, receipt: dict[str, object]) -> str:
    return f"{OPERATION_RECEIPT_MARKER}\n" + json.dumps(
        {"idempotency_key": key, "operation": operation, "receipt": receipt}
    )


def test_find_latest_operation_receipt_key_returns_latest_matching_operation() -> None:
    control = SupervisionControl()
    first = hold_receipt_to_json(HoldReceipt("run-1", (), {"loop.yml": False}))
    latest = hold_receipt_to_json(HoldReceipt("run-2", (), {"loop.yml": False}))

    assert (
        find_latest_operation_receipt_key(
            control,
            [_receipt("run-1:hold", "hold", first), _receipt("run-2:hold", "hold", latest)],
            "hold",
        )
        == "run-2:hold"
    )


def test_find_latest_operation_receipt_key_ignores_other_operations() -> None:
    assert (
        find_latest_operation_receipt_key(
            SupervisionControl(), ["unrelated", _receipt("key", "checkpoint", {})], "hold"
        )
        is None
    )


@pytest.mark.parametrize(
    ("body", "message"),
    [
        (f"{OPERATION_RECEIPT_MARKER}\nnot-json", "JSON is invalid"),
        (f"{OPERATION_RECEIPT_MARKER}\n[]", "must be an object"),
        (_receipt("", "hold", {}), "is malformed"),
        (_receipt("run-1:hold", "hold", {"previous_states": "invalid"}), "is malformed"),
    ],
)
def test_find_latest_operation_receipt_key_rejects_malformed_matching_receipt(body: str, message: str) -> None:
    with pytest.raises(RuntimeError, match=message):
        find_latest_operation_receipt_key(
            SupervisionControl(),
            [body],
            "hold",
        )
