import pytest

from agentic_devtools.cli.ci.pipeline.session_detector import _raw_task_is_active


@pytest.mark.parametrize(("task", "expected"), [({}, False), ({"state": "running"}, True), ({"status": []}, False)])
def test_active_status_requires_supported_string(task: dict, expected: bool) -> None:
    assert _raw_task_is_active(task) is expected
