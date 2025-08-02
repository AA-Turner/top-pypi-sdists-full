import typing

import pytest

from snowflake.core.exceptions import InvalidOperationError
from snowflake.core.task import StoredProcedureCall
from snowflake.core.task.dagv1 import DAG, DAGTask


if typing.TYPE_CHECKING:
    from snowflake.snowpark import Session


def foo1(session: "Session") -> str:
    return "abc"


def foo2(session: "Session") -> str:
    return "abc"


def foo3(session: "Session") -> str:
    return "abc"


def foo4(session: "Session") -> str:
    return "abc"


@pytest.mark.snowpark
def test__use_func_return_value_kicked_in():
    with DAG("dag1", stage_location="fake_stage", use_func_return_value=True):
        task1 = DAGTask("task1", foo1)

    with DAG("dag2", stage_location="fake_stage"):
        task2 = DAGTask("task2", foo2)

    with DAG("dag3", use_func_return_value=True):
        task3 = DAGTask("task3", StoredProcedureCall(foo3, stage_location="fake_stage"))

    with DAG("dag4"):
        task4 = DAGTask("task4", StoredProcedureCall(foo4, stage_location="fake_stage"))

    lower_task1 = task1._to_low_level_task()
    lower_task2 = task2._to_low_level_task()
    lower_task3 = task3._to_low_level_task()
    lower_task4 = task4._to_low_level_task()
    assert lower_task1.definition.func is not foo1
    assert lower_task2.definition.func is foo2
    assert lower_task3.definition.func is not foo3
    assert lower_task4.definition.func is foo4


def test_create_task_in_dag_without_warehouse():
    dag_warehouse = "DAG_FAKE_WAREHOUSE"
    with DAG("dag", stage_location="fake_stage", warehouse=dag_warehouse):
        task = DAGTask("task", "select 'task'")
    assert task.warehouse == dag_warehouse


def test_create_task_in_dag_with_warehouse():
    dag_warehouse = "DAG_FAKE_WAREHOUSE"
    task_warehouse = "TASK_FAKE_WAREHOUSE"
    with DAG("dag", stage_location="fake_stage", warehouse=dag_warehouse):
        task = DAGTask("task", "select 'task'", warehouse=task_warehouse)
    assert task.warehouse == task_warehouse


def test_skip_adding_predecessors_if_task_is_from_different_task_group(schema):
    with DAG("dag1"):
        task1 = DAGTask("task1", "select 1")
        task2 = DAGTask("task2", "select 2")

    with DAG("dag2"):
        task3 = DAGTask("task3", "select 3")

    with pytest.raises(InvalidOperationError) as err:
        task1.add_predecessors(task3)
    assert str(err.value) == f"Task {task3.name} belongs to a different task graph"
    assert task1.predecessors == set()

    with pytest.raises(InvalidOperationError) as err:
        task1.add_predecessors([task2, task3])
    assert str(err.value) == f"Task {task3.name} belongs to a different task graph"
    assert task1.predecessors == set()


def test_skip_adding_successors_if_task_is_from_different_task_group(schema):
    with DAG("dag1"):
        task1 = DAGTask("task1", "select 1")
        task2 = DAGTask("task2", "select 2")

    with DAG("dag2"):
        task3 = DAGTask("task3", "select 3")

    with pytest.raises(InvalidOperationError) as err:
        task1.add_successors(task3)
    assert str(err.value) == f"Task {task3.name} belongs to a different task graph"
    assert task3.predecessors == set()

    with pytest.raises(InvalidOperationError) as err:
        task1.add_successors([task2, task3])
    assert str(err.value) == f"Task {task3.name} belongs to a different task graph"
    assert task2.predecessors == set()
    assert task3.predecessors == set()


def test_add_predecessor_to_finalizer_and_vice_versa(schema):
    with DAG("dag"):
        task1 = DAGTask("task1", "select 1", is_finalizer=True)
        task2 = DAGTask("task2", "select 1")
        task3 = DAGTask("task3", "select 1")

        with pytest.raises(InvalidOperationError) as err:
            task1.add_predecessors(task2)
        assert str(err.value) == f"Finalizer task {task1.name} cannot have any predecessors"
        assert task1.predecessors == set()

        with pytest.raises(InvalidOperationError) as err:
            task2.add_predecessors([task3, task1])
        assert str(err.value) == f"Finalizer task {task1.name} cannot be predecessor of any task"
        assert task2.predecessors == set()

        with pytest.raises(InvalidOperationError) as err:
            task2 << task1
        assert str(err.value) == f"Finalizer task {task1.name} cannot be predecessor of any task"
        assert task2.predecessors == set()

        with pytest.raises(InvalidOperationError) as err:
            task1 << task2
        assert str(err.value) == f"Finalizer task {task1.name} cannot have any predecessors"
        assert task1.predecessors == set()


def test_add_successors_to_finalizer_and_vice_versa(schema):
    with DAG("dag"):
        task1 = DAGTask("task1", "select 1", is_finalizer=True)
        task2 = DAGTask("task2", "select 1")
        task3 = DAGTask("task3", "select 1")

        with pytest.raises(InvalidOperationError) as err:
            task1.add_successors(task2)
        assert str(err.value) == f"Finalizer task {task1.name} cannot have any successors"
        assert task2.predecessors == set()

        with pytest.raises(InvalidOperationError) as err:
            task2.add_successors(task1)
        assert str(err.value) == f"Finalizer task {task1.name} cannot have any predecessors"
        assert task1.predecessors == set()

        with pytest.raises(InvalidOperationError) as err:
            task2.add_successors([task3, task1])
        assert str(err.value) == f"Finalizer task {task1.name} cannot have any predecessors"
        assert task1.predecessors == set()
        assert task3.predecessors == set()

        # adding finalizer task1 as successor of task2
        with pytest.raises(InvalidOperationError) as err:
            task2 >> task1
        assert str(err.value) == f"Finalizer task {task1.name} cannot have any predecessors"
        assert task1.predecessors == set()

        # adding task2 as the successor of finalizer task1
        with pytest.raises(InvalidOperationError) as err:
            task1 >> task2
        assert str(err.value) == f"Finalizer task {task1.name} cannot have any successors"
        assert task2.predecessors == set()
