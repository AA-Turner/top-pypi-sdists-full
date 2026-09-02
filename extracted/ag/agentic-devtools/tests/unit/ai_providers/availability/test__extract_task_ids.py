import pytest

from agentic_devtools.ai_providers.availability import _extract_task_ids
from agentic_devtools.ai_providers.errors import ProviderError


def test__extract_task_ids_accepts_supported_snapshot_shapes() -> None:
    assert _extract_task_ids({"tasks": [{"id": "task-1"}, {"id": "task-2"}]}) == {"task-1", "task-2"}
    assert _extract_task_ids({"task_ids": ["task-1"]}) == {"task-1"}
    assert _extract_task_ids({"id": "task-1"}) == {"task-1"}
    assert _extract_task_ids(["task-1", {"id": "task-2"}]) == {"task-1", "task-2"}
    assert _extract_task_ids({}) == set()


@pytest.mark.parametrize(
    ("payload", "error"),
    [
        ({"tasks": None}, "'tasks' key is present but null"),
        ({"tasks": "task-1"}, "'tasks' key must contain a list or mapping"),
        ({"task_ids": "task-1"}, "'task_ids' key must contain a non-string sequence"),
        ({"error": "unauthorized"}, "Snapshot mapping must contain"),
        (["task-1", "task-1"], "duplicate task id 'task-1'"),
    ],
)
def test__extract_task_ids_rejects_malformed_payloads(payload: object, error: str) -> None:
    with pytest.raises(ProviderError, match=error):
        _extract_task_ids(payload)


@pytest.mark.parametrize(
    ("payload", "error"),
    [
        ({"id": " "}, r"does not match \^"),
        ([" "], r"does not match \^"),
        ([{"id": " "}], r"does not match \^"),
        (" ", r"does not match \^"),
        ({"id": "task 1"}, r"does not match \^"),
        ({"id": "task/1"}, r"does not match \^"),
    ],
)
def test__extract_task_ids_rejects_task_ids_not_matching_pattern(payload: object, error: str) -> None:
    with pytest.raises(ProviderError, match=error):
        _extract_task_ids(payload)
