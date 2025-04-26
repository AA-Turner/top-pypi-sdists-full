from snowflake.core.task import Task


def test_to_dict():
    task = Task(name="test_task", definition="select 1")
    assert task.to_dict() == {'definition': 'select 1', 'name': 'test_task'}
