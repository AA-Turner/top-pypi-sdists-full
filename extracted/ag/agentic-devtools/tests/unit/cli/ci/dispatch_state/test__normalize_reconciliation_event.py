import pytest

from agentic_devtools.cli.ci import dispatch_state as dispatch_state_module
from agentic_devtools.cli.ci.dispatch_state import DispatchIdentity, DispatchRecord, DispatchState

SHA = "a" * 40


def test_rejects_generic_reconciliation_when_operation_is_unknown(monkeypatch: pytest.MonkeyPatch) -> None:
    record = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1)).with_state(
        DispatchState.NEEDS_RECONCILIATION,
        reason="timeout",
        evidence={"operation": "marker", "pages": 1},
    )
    monkeypatch.setattr(dispatch_state_module, "_reconciliation_operation", lambda _record, _changes: None)

    with pytest.raises(ValueError):
        dispatch_state_module._normalize_reconciliation_event(record, "reconcile_unique", {})


def test_rejects_operation_specific_reconciliation_event_for_wrong_operation() -> None:
    marker_record = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1)).with_state(
        DispatchState.NEEDS_RECONCILIATION,
        reason="timeout",
        evidence={"operation": "marker"},
    )
    with pytest.raises(ValueError):
        dispatch_state_module._normalize_reconciliation_event(marker_record, "reconcile_task_miss", {})


def test_accepts_matching_operation_specific_reconciliation_event() -> None:
    task_record = (
        DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1))
        .with_state("reserved", marker_comment_id=4)
        .with_state(DispatchState.NEEDS_RECONCILIATION, reason="timeout", evidence={"operation": "task"})
    )

    assert dispatch_state_module._normalize_reconciliation_event(task_record, "reconcile_task_unique", {}) == (
        "reconcile_task_unique"
    )
