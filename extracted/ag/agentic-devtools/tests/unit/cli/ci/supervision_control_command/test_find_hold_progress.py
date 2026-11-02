"""Tests for the find_hold_progress symbol."""

from __future__ import annotations

import json

import pytest

from agentic_devtools.cli.ci.supervision_control import HoldReceipt, SupervisionControl
from agentic_devtools.cli.ci.supervision_control_command import (
    OPERATION_RECEIPT_MARKER,
    find_hold_progress,
    hold_receipt_to_json,
)


def _hold_record(
    receipt: HoldReceipt,
    *,
    disabled_workflows: list[str] | None = None,
    attempted_workflows: list[str] | None = None,
) -> str:
    record: dict[str, object] = {
        "idempotency_key": f"{receipt.run_id}:hold",
        "operation": "hold",
        "receipt": hold_receipt_to_json(receipt),
    }
    if disabled_workflows is not None:
        record["disabled_workflows"] = disabled_workflows
    if attempted_workflows is not None:
        record["attempted_workflows"] = attempted_workflows
    return f"{OPERATION_RECEIPT_MARKER}\n" + json.dumps(record)


def test_find_hold_progress_recovers_the_latest_cumulative_progress() -> None:
    receipt = HoldReceipt(
        "run-1",
        ("first.yml", "second.yml"),
        {"first.yml": True, "second.yml": True, "initially-disabled.yml": False},
    )
    bodies = [
        "unrelated",
        f"{OPERATION_RECEIPT_MARKER}\n"
        + json.dumps(
            {
                "idempotency_key": "another-run:hold",
                "operation": "hold",
                "receipt": hold_receipt_to_json(receipt),
            }
        ),
        _hold_record(receipt),
        _hold_record(receipt, disabled_workflows=["first.yml"]),
        _hold_record(receipt, disabled_workflows=["first.yml", "second.yml"]),
    ]

    assert find_hold_progress(SupervisionControl(), bodies, "run-1:hold", receipt) == (
        frozenset({"first.yml", "second.yml"}),
        frozenset({"first.yml", "second.yml"}),
    )


def test_find_hold_progress_recovers_pending_workflows_separately() -> None:
    receipt = HoldReceipt("run-1", ("first.yml", "second.yml"), {"first.yml": True, "second.yml": True})

    assert find_hold_progress(
        SupervisionControl(),
        [
            _hold_record(receipt),
            _hold_record(receipt, disabled_workflows=[], attempted_workflows=["first.yml"]),
        ],
        "run-1:hold",
        receipt,
    ) == (frozenset(), frozenset({"first.yml"}))


@pytest.mark.parametrize(
    "records",
    [
        None,
        ["first.yml", "first.yml"],
        ["unknown.yml"],
        ["first.yml", None],
    ],
)
def test_find_hold_progress_rejects_malformed_or_unowned_workflows(records: object) -> None:
    receipt = HoldReceipt("run-1", ("first.yml", "second.yml"), {"first.yml": True, "second.yml": True})
    record = json.loads(_hold_record(receipt).split("\n", 1)[1])
    record["disabled_workflows"] = records
    body = f"{OPERATION_RECEIPT_MARKER}\n" + json.dumps(record)

    with pytest.raises(RuntimeError, match="stored hold progress"):
        find_hold_progress(SupervisionControl(), [_hold_record(receipt), body], "run-1:hold", receipt)


def test_find_hold_progress_rejects_regressing_progress() -> None:
    receipt = HoldReceipt("run-1", ("first.yml", "second.yml"), {"first.yml": True, "second.yml": True})

    with pytest.raises(RuntimeError, match="stored hold progress is inconsistent"):
        find_hold_progress(
            SupervisionControl(),
            [
                _hold_record(receipt, disabled_workflows=["first.yml"]),
                _hold_record(receipt, disabled_workflows=[]),
            ],
            "run-1:hold",
            receipt,
        )


def test_find_hold_progress_requires_a_matching_durable_receipt() -> None:
    receipt = HoldReceipt("run-1", ("first.yml",), {"first.yml": True})

    with pytest.raises(RuntimeError, match="stored hold receipt"):
        find_hold_progress(SupervisionControl(), [], "run-1:hold", receipt)


@pytest.mark.parametrize(
    ("disabled", "attempted"),
    [
        ([], ["first.yml", None]),
        (["first.yml"], []),
        ([], ["unknown.yml"]),
    ],
)
def test_find_hold_progress_rejects_malformed_or_inconsistent_attempts(
    disabled: list[str], attempted: list[object] | None
) -> None:
    receipt = HoldReceipt("run-1", ("first.yml", "second.yml"), {"first.yml": True, "second.yml": True})
    record = json.loads(_hold_record(receipt, disabled_workflows=disabled).split("\n", 1)[1])
    record["attempted_workflows"] = attempted
    body = f"{OPERATION_RECEIPT_MARKER}\n" + json.dumps(record)

    with pytest.raises(RuntimeError, match="stored hold progress"):
        find_hold_progress(SupervisionControl(), [_hold_record(receipt), body], "run-1:hold", receipt)
