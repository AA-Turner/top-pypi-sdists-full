from agentic_devtools.cli.ci.pipeline.session_detector import _raw_task_values


def test_reads_aliases_without_accepting_boolean_id() -> None:
    assert _raw_task_values({"state": "running", "id": True, "taskId": 42, "created_at": "now"}) == (
        "running",
        "42",
        "now",
        None,
    )


def test_missing_fields_remain_unknown() -> None:
    assert _raw_task_values({}) == (None, None, None, None)
