import pytest

from agentic_devtools.cli.github.single_finding_dispatch import SingleFindingDispatchResult


def test_dispatch_result_returns_accepted_task_and_session_identity():
    result = SingleFindingDispatchResult(
        outcome="accepted",
        reason="task accepted and persisted",
        expected_head="a" * 40,
        finding_id="b" * 64,
        attempt_id="attempt-1",
        task_id="task-1",
        session_id="session-1",
    )

    assert result.task_id == "task-1"
    assert result.session_id == "session-1"


@pytest.mark.parametrize(
    "updates",
    [
        {"outcome": "accepted", "task_id": None},
        {"outcome": "already_resolved", "task_id": "task-1"},
        {"outcome": "head_changed", "task_id": "task-1"},
        {"expected_head": None},
        {"finding_id": None},
        {"expected_head": "short"},
        {"finding_id": "short"},
        {"attempt_id": ""},
        {"session_id": "session-1"},
        {"reason": " "},
        {"outcome": "invalid"},
    ],
)
def test_dispatch_result_rejects_inconsistent_values(updates):
    values = {
        "outcome": "blocked",
        "reason": "blocked",
        "expected_head": "a" * 40,
        "finding_id": "b" * 64,
        "attempt_id": "attempt-1",
        "task_id": None,
        "session_id": None,
    }
    values.update(updates)

    with pytest.raises(ValueError):
        SingleFindingDispatchResult(**values)
