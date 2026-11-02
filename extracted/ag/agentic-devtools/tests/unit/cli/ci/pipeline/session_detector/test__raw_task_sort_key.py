from agentic_devtools.cli.ci.pipeline.session_detector import _raw_task_sort_key


def test_creation_time_precedes_update_time() -> None:
    assert _raw_task_sort_key((2, {"createdAt": "a", "updatedAt": "z"})) == ("a", -2)


def test_missing_timestamp_keeps_stable_order() -> None:
    assert _raw_task_sort_key((0, {})) == ("", 0)
