import pytest

from agentic_devtools.ai_providers.availability import _validate_task_id
from agentic_devtools.ai_providers.errors import ProviderError


@pytest.mark.parametrize("task_id", ["task-1", "task_1", "Task123", "a", "A_B-C"])
def test__validate_task_id_accepts_ids_matching_task_id_pattern(task_id: str) -> None:
    _validate_task_id(task_id, "task id")


@pytest.mark.parametrize("task_id", ["", " ", "task 1", "task/1", "task.1", "task:1", "task@1", "task-1\n"])
def test__validate_task_id_rejects_ids_not_matching_task_id_pattern(task_id: str) -> None:
    with pytest.raises(ProviderError, match=r"does not match \^\[A-Za-z0-9_-\]\+\$"):
        _validate_task_id(task_id, "task id")
