from dataclasses import replace

import pytest

from agentic_devtools.cli.ci import dispatch_state as dispatch_state_module
from agentic_devtools.cli.ci.dispatch_state import DispatchIdentity, DispatchRecord, DispatchState

SHA = "a" * 40


def test_infers_marker_and_task_operations_from_record_shape() -> None:
    marker_record = DispatchRecord.new(DispatchIdentity("repo", 7, SHA, 1)).with_state(
        "needs_reconciliation",
        reason="timeout",
        evidence={"operation": "marker", "pages": 1},
    )
    task_record = (
        DispatchRecord.new(DispatchIdentity("repo", 7, "b" * 40, 1))
        .with_state("reserved", marker_comment_id=4)
        .with_state("needs_reconciliation", reason="timeout", evidence={"operation": "task", "pages": 1})
    )
    orphan_task = replace(marker_record, state=DispatchState.RESERVED, evidence={}, task_id="task-1")

    assert dispatch_state_module._reconciliation_operation(marker_record, {}) == "marker"
    assert dispatch_state_module._reconciliation_operation(task_record, {}) == "task"
    assert dispatch_state_module._reconciliation_operation(orphan_task, {}) is None
    assert dispatch_state_module._reconciliation_operation(orphan_task, {"evidence": {"operation": "other"}}) is None
    assert dispatch_state_module._reconciliation_operation(orphan_task, {"evidence": []}) is None
    assert dispatch_state_module._reconciliation_operation(marker_record, {"evidence": []}) == "marker"
    with pytest.raises(ValueError, match="persisted uncertain operation"):
        dispatch_state_module._reconciliation_operation(
            marker_record,
            {"evidence": {"operation": "other"}},
        )
