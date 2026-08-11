from snowflake.core.task import OverlapPolicy, Task


def test_to_dict():
    task = Task(
        name="test_task",
        definition="select 1",
        success_integration="my_success",
        overlap_policy=OverlapPolicy.NO_OVERLAP,
        execute_as_user="task_user",
    )
    assert task.to_dict() == {
        "definition": "select 1",
        "name": "test_task",
        "success_integration": "my_success",
        "overlap_policy": OverlapPolicy.NO_OVERLAP,
        "execute_as_user": "task_user",
    }
