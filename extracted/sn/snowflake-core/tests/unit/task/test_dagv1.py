import itertools
import typing

import pytest

from snowflake.core.exceptions import InvalidOperationError
from snowflake.core.task import OverlapPolicy, StoredProcedureCall
from snowflake.core.task.dagv1 import DAG, DAGRun, DAGTask


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


def _make_dagrun(**kwargs) -> DAGRun:
    run = DAGRun()
    run.run_id = kwargs.get("run_id", 42)
    run.dag_name = kwargs.get("dag_name", "MY_DAG")
    run.database_name = kwargs.get("database_name", "DB")
    run.schema_name = kwargs.get("schema_name", "PUBLIC")
    run.state = kwargs.get("state", "SUCCEEDED")
    run.first_error_task_name = kwargs.get("first_error_task_name", None)
    run.first_error_code = kwargs.get("first_error_code", None)
    run.first_error_message = kwargs.get("first_error_message", None)
    run.scheduled_time = kwargs.get("scheduled_time", None)
    run.query_start_time = kwargs.get("query_start_time", None)
    run.next_scheduled_time = kwargs.get("next_scheduled_time", None)
    run.graph_version = kwargs.get("graph_version", 1)
    return run


def test_repr_html_contains_field_values():
    run = _make_dagrun(run_id=99, dag_name="TEST_DAG", state="FAILED", graph_version=3)
    html = run._repr_html_()
    assert "99" in html
    assert "TEST_DAG" in html
    assert "FAILED" in html
    assert "3" in html


def test_repr_html_escapes_xss_in_error_message():
    payload = '<img src=x onerror="alert(1)">'
    run = _make_dagrun(first_error_message=payload)
    html = run._repr_html_()
    assert "<img" not in html
    assert "&lt;img" in html


def test_repr_html_escapes_special_chars_in_dag_name():
    run = _make_dagrun(dag_name="A&B<C>D")
    html = run._repr_html_()
    assert "A&B<C>D" not in html
    assert "A&amp;B&lt;C&gt;D" in html


def test_repr_html_none_fields_render_as_none_string():
    run = _make_dagrun(
        first_error_task_name=None,
        first_error_code=None,
        first_error_message=None,
        scheduled_time=None,
        query_start_time=None,
        next_scheduled_time=None,
    )
    html = run._repr_html_()
    assert html.count(">None<") == 6


def test_repr_html_returns_table():
    run = _make_dagrun()
    html = run._repr_html_()
    assert html.strip().startswith("<table")
    assert "</table>" in html


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


def test_dag_condition_passed_to_low_level_task(schema):
    with DAG("dag", condition="SYSTEM$STREAM_HAS_DATA('s')") as dag:
        pass
    task = dag._to_low_level_task()
    assert task.condition == "SYSTEM$STREAM_HAS_DATA('s')"


class TestDAGOverlapPolicyBehavior:
    @pytest.mark.parametrize("overlap_policy", itertools.chain(OverlapPolicy, (None,)))
    def test_valid_constructions_with_overlap_policy(self, overlap_policy: OverlapPolicy | None):
        dag = DAG("test_dag", overlap_policy=overlap_policy)
        assert dag.overlap_policy is overlap_policy
        assert dag.allow_overlapping_execution is (
            overlap_policy._equivalent_allow_overlapping_execution_value() if overlap_policy is not None else None
        )
        rest_model = dag._to_low_level_task()._to_rest_model()
        assert rest_model.overlap_policy == (str(overlap_policy) if overlap_policy is not None else None)
        assert rest_model.allow_overlapping_execution is None

    @pytest.mark.parametrize("allow_overlapping_execution", (None, False, True))
    def test_valid_constructions_with_allow_overlapping_execution(self, allow_overlapping_execution: bool | None):
        dag = DAG("test_dag", allow_overlapping_execution=allow_overlapping_execution)
        assert dag.overlap_policy is OverlapPolicy._from_allow_overlapping_execution(allow_overlapping_execution)
        assert dag.allow_overlapping_execution is allow_overlapping_execution
        rest_model = dag._to_low_level_task()._to_rest_model()
        assert rest_model.overlap_policy is None
        assert rest_model.allow_overlapping_execution is allow_overlapping_execution

    @pytest.mark.parametrize(
        "overlap_policy,allow_overlapping_execution",
        (
            (OverlapPolicy.NO_OVERLAP, True),
            (OverlapPolicy.ALLOW_CHILD_OVERLAP, False),
            (OverlapPolicy.ALLOW_ALL_OVERLAP, False),
            (OverlapPolicy.ALLOW_ALL_OVERLAP, True),
        ),
    )
    def test_invalid_constructions(
        self, overlap_policy: OverlapPolicy | None, allow_overlapping_execution: bool | None
    ):
        with pytest.raises(ValueError):
            DAG(
                "test_dag",
                overlap_policy=overlap_policy,
                allow_overlapping_execution=allow_overlapping_execution,
            )

    def test_setters_switch_low_level_task_projection(self):
        dag = DAG("test_dag", overlap_policy=OverlapPolicy.NO_OVERLAP)
        rest = dag._to_low_level_task()._to_rest_model()
        assert (rest.overlap_policy, rest.allow_overlapping_execution) == (
            str(OverlapPolicy.NO_OVERLAP),
            None,
        )

        dag.allow_overlapping_execution = True
        assert dag.overlap_policy is OverlapPolicy.ALLOW_CHILD_OVERLAP
        rest = dag._to_low_level_task()._to_rest_model()
        assert (rest.overlap_policy, rest.allow_overlapping_execution) == (None, True)

        dag.overlap_policy = OverlapPolicy.ALLOW_ALL_OVERLAP
        rest = dag._to_low_level_task()._to_rest_model()
        assert (rest.overlap_policy, rest.allow_overlapping_execution) == (
            str(OverlapPolicy.ALLOW_ALL_OVERLAP),
            None,
        )
