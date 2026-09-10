from agentic_devtools.cli.ci.guards import ReconciliationResult


def test_supports_task_or_marker_identifiers() -> None:
    marker = ReconciliationResult("unique_match", marker_comment_id=17)
    task = ReconciliationResult("unique_match", task_id="task-1")

    assert marker.marker_comment_id == 17
    assert marker.task_id is None
    assert task.task_id == "task-1"
    assert task.marker_comment_id is None
