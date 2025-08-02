import time
import warnings

from contextlib import ExitStack
from datetime import timedelta

import pytest

from snowflake.core._common import CreateMode
from snowflake.core._internal.utils import normalize_name
from snowflake.core.exceptions import APIError
from snowflake.core.task import StoredProcedureCall
from snowflake.core.task.context import TaskContext
from snowflake.core.task.dagv1 import DAG, DAGOperation, DAGTask, DAGTaskBranch, _use_func_return_value
from snowflake.core.warehouse import Warehouse

from ...utils import get_task_history, random_object_name


def test_deploy_dag(schema):
    test_dag = random_object_name()
    with DAG(test_dag, schedule=timedelta(minutes=10)) as dag:
        task1 = DAGTask("task1", "select 1")
        task2 = DAGTask("task2", "select 2")
        task3 = DAGTask("task3", "select 3")
        task2 << task1 >> task3
    op = DAGOperation(schema)
    op.deploy(dag, mode=CreateMode.or_replace)
    try:
        fetched = schema.tasks[test_dag].fetch_task_dependents()
        fetched = sorted(fetched, key=lambda x: x.name.lower())
        assert len(fetched) == 4
        assert fetched[0].name.lower() == test_dag
        assert fetched[1].name.lower() == f"{test_dag}$task1"
        assert fetched[2].name.lower() == f"{test_dag}$task2"
        assert fetched[3].name.lower() == f"{test_dag}$task3"
    finally:
        op.drop(dag)


def test_deploy_dag_with_finalizer(schema):
    test_dag = random_object_name()
    with DAG(test_dag, schedule=timedelta(minutes=10)) as dag:
        task1 = DAGTask("task1", "select 1")
        task2 = DAGTask("task2", "select 2")
        DAGTask("task3", "select 3", is_finalizer=True)
        task2 << task1
    op = DAGOperation(schema)
    op.deploy(dag, mode=CreateMode.or_replace)
    try:
        fetched = schema.tasks[test_dag].fetch_task_dependents()
        assert len(fetched) == 4
        assert fetched[0].name.lower() == test_dag
        assert fetched[1].name.lower() == f"{test_dag}$task1"
    finally:
        op.drop(dag)


def test_deploy_dag_default_mode(schema):
    test_dag = random_object_name()
    with DAG(test_dag, schedule=timedelta(minutes=10)) as dag:
        task1 = DAGTask("task1", "select 1")
        task2 = DAGTask("task2", "select 2")
        task3 = DAGTask("task3", "select 3")
        task2 << task1 >> task3
    op = DAGOperation(schema)
    # Deploy with the default mode DeploymentMode.error_if_exists for coverage.
    op.deploy(dag)
    try:
        fetched = schema.tasks[test_dag].fetch_task_dependents()
        assert len(fetched) == 4
        assert fetched[0].name.lower() == test_dag
        assert fetched[1].name.lower() == f"{test_dag}$task1"
    finally:
        op.drop(dag)


@pytest.mark.usefixtures("backup_database_schema")
def test_deploy_dag_to_not_default_schema(root, database):
    database = database.name
    new_schema_name = random_object_name()
    test_dag = random_object_name()
    root.connection.execute_string(f"create schema {database}.{new_schema_name}")
    try:
        new_schema = root.databases[database].schemas[new_schema_name]
        with DAG(test_dag, schedule=timedelta(minutes=10)) as dag:
            task1 = DAGTask("task1", "select 1")
            task2 = DAGTask("task2", "select 2")
            task3 = DAGTask("task3", "select 3")
            task2 << task1 >> task3
        op = DAGOperation(new_schema)
        op.deploy(dag, mode=CreateMode.or_replace)
        fetched = new_schema.tasks[test_dag].fetch_task_dependents()
        assert len(fetched) == 4
        assert fetched[0].name.lower() == test_dag
        assert fetched[1].name.lower() == f"{test_dag}$task1"
        op.drop(dag)
    finally:
        root.connection.execute_string(f"drop schema if exists {new_schema_name}")


def test_deploy_dag_circle(schema):
    test_dag = random_object_name()
    with DAG(test_dag, schedule=timedelta(minutes=10)) as dag:
        task1 = DAGTask("task1", "select 1")
        task2 = DAGTask("task2", "select 2")
        task3 = DAGTask("task3", "select 3")
        task1 >> task2 >> task3 >> task1
    op = DAGOperation(schema)
    with pytest.raises(ValueError) as ex:
        op.deploy(dag, mode=CreateMode.or_replace)
    assert ex.match("There is a cycle in the task graph.")


def test_deploy_dag_5_layers(schema):
    test_dag = random_object_name()
    with DAG(test_dag, schedule=timedelta(minutes=10)) as dag:
        prev_task = DAGTask("task1", "select 1")
        for i in range(2, 6):
            task = DAGTask(f"task{i}", f"select {i}")
            prev_task >> task
            prev_task = task
    op = DAGOperation(schema)
    op.deploy(dag, mode=CreateMode.or_replace)
    try:
        fetched = schema.tasks[test_dag].fetch_task_dependents()
        assert len(fetched) == 6
        assert [x.name.lower() for x in fetched] == [test_dag, *[f"{test_dag}$task{i + 1}" for i in range(5)]]
    finally:
        op.drop(dag)


@pytest.mark.snowpark
@pytest.mark.usefixtures("anaconda_package_available")
def test_deploy_dag_definition_python(schema, db_parameters):
    from snowflake.snowpark import Session

    def foo(session: Session) -> None:
        session.sql("select 1").collect()

    test_stage = random_object_name()
    test_dag = random_object_name()
    schema._connection.execute_string(f"create or replace stage {test_stage}")
    try:
        with DAG(test_dag, schedule=timedelta(minutes=10)) as dag:
            task1 = DAGTask(
                "task1",
                StoredProcedureCall(foo, stage_location=test_stage, packages=["snowflake-snowpark-python"]),
                warehouse=db_parameters["warehouse"],
            )
            task2 = DAGTask("task2", "select 2")
            task1 >> task2
        op = DAGOperation(schema)
        op.deploy(dag, mode=CreateMode.or_replace)
        try:
            fetched = schema.tasks[task1.full_name].fetch()
            assert "foo" in fetched.definition
        finally:
            op.drop(dag)
    finally:
        schema._connection.execute_string(f"drop stage {test_stage}")


@pytest.mark.snowpark
@pytest.mark.usefixtures("anaconda_package_available")
def test_deploy_dag_python_function_directly(schema, db_parameters):
    from snowflake.snowpark import Session

    def foo0(session: Session) -> None:
        session.sql("select 'foo0'").collect()

    def foo1(session: Session) -> None:
        session.sql("select 'foo1'").collect()

    def foo2(session: Session) -> None:
        session.sql("select 'foo2'").collect()

    def foo3(session: Session) -> None:
        session.sql("select 'foo3'").collect()

    def foo4(session: Session) -> None:
        session.sql("select 'foo4'").collect()

    def foo5(session: Session) -> None:
        session.sql("select 'foo5'").collect()

    def foo6(session: Session) -> None:
        session.sql("select 'foo6'").collect()

    test_stage = random_object_name()
    test_dag = random_object_name()
    schema._connection.execute_string(f"create or replace stage {test_stage}")
    try:
        with DAG(
            test_dag,
            schedule=timedelta(minutes=10),
            stage_location=test_stage,
            warehouse=db_parameters["warehouse"],
            packages=["snowflake-snowpark-python"],
        ) as dag:
            task0 = DAGTask("foo0", foo0, is_serverless=True)
            task0 >> foo1 >> [foo3, foo4]
            task0 << foo2 << [foo5, foo6]

        op = DAGOperation(schema)
        op.deploy(dag, mode=CreateMode.or_replace)
        try:
            assert "foo0" in schema.tasks[task0.full_name].fetch().definition
            assert "foo1" in schema.tasks[f"{test_dag}$foo1"].fetch().definition
            assert "foo2" in schema.tasks[f"{test_dag}$foo2"].fetch().definition
            assert "foo2" in schema.tasks[f"{test_dag}$foo2"].fetch().definition
            assert "foo3" in schema.tasks[f"{test_dag}$foo3"].fetch().definition
            assert "foo4" in schema.tasks[f"{test_dag}$foo4"].fetch().definition
            assert "foo5" in schema.tasks[f"{test_dag}$foo5"].fetch().definition
            assert "foo6" in schema.tasks[f"{test_dag}$foo6"].fetch().definition
            dependents = schema.tasks[test_dag].fetch_task_dependents()
            assert dependents[0].name.upper() == test_dag.upper()
            # foo5 and foo6 are next to dependents[0].
            assert {dependents[1].name.upper(), dependents[2].name.upper()} == {
                f"{test_dag}$foo5".upper(),
                f"{test_dag}$foo6".upper(),
            }
            assert dependents[3].name.upper() == f"{test_dag}$foo2".upper()
            assert dependents[4].name.upper() == f"{test_dag}$foo0".upper()
            assert dependents[5].name.upper() == f"{test_dag}$foo1".upper()
            assert {dependents[6].name.upper(), dependents[7].name.upper()} == {
                f"{test_dag}$foo3".upper(),
                f"{test_dag}$foo4".upper(),
            }
        finally:
            op.drop(dag)
    finally:
        schema._connection.execute_string(f"drop stage {test_stage}")


@pytest.mark.snowpark
@pytest.mark.usefixtures("anaconda_package_available")
@pytest.mark.parametrize("reverse", [True, False])
def test_deploy_dag_with_branch(schema, db_parameters, reverse):
    from snowflake.snowpark import Session

    def task_handler(session: Session) -> None:
        pass  # do nothing

    def task_branch_handler(session: Session) -> None:
        tc = TaskContext(session)
        tc.set_return_value("task3")

    def task4_handler(session: Session) -> None:
        tc = TaskContext(session)
        tc.set_return_value("task4")

    test_stage = random_object_name()
    test_dag = random_object_name()
    schema._connection.execute_string(f"create or replace stage {test_stage}")
    try:
        with DAG(
            test_dag,
            schedule=timedelta(minutes=10),
            stage_location=test_stage,
            packages=["snowflake-snowpark-python"],
            warehouse=db_parameters["warehouse"],
        ) as dag:
            task1 = DAGTask("task1", task_handler, warehouse=db_parameters["warehouse"])
            task1_branch = DAGTaskBranch("task1_branch", task_branch_handler, warehouse=db_parameters["warehouse"])
            task2 = DAGTask("task2", task_handler, is_serverless=True)
            task3 = DAGTask("task3", task_handler, warehouse=db_parameters["warehouse"], condition="1=1")
            if not reverse:
                task1 >> task1_branch >> [task2, task3]
            else:
                task1_branch << task1
                task1_branch >> [task2, task3]
            task2_branch = DAGTaskBranch("task2_branch", task_branch_handler, warehouse=db_parameters["warehouse"])
            if not reverse:
                task2 >> task2_branch >> task4_handler
            else:
                DAGTask("task4_handler", task4_handler) << task2_branch << task2
        op = DAGOperation(schema)
        op.deploy(dag, mode=CreateMode.or_replace)
        try:
            dependents = schema.tasks[dag.name].fetch_task_dependents()
            task4 = dependents[-1]
            assert len(dependents) == 7
            assert (
                f"SYSTEM$GET_PREDECESSOR_RETURN_VALUE('{normalize_name(task1_branch.full_name)}') = '{task2.name}'"
                == task2.condition
            )
            assert (
                f"SYSTEM$GET_PREDECESSOR_RETURN_VALUE('{normalize_name(task1_branch.full_name)}') = "
                f"'{task3.name}' and 1=1" == task3.condition
            )
            assert (
                f"SYSTEM$GET_PREDECESSOR_RETURN_VALUE('{normalize_name(task2_branch.full_name)}') = 'task4_handler'"
                == task4.condition
            )
            assert task1_branch in task2.predecessors
            assert task1_branch in task3.predecessors
            fqal_task2_name = f"{schema.database.name}.{schema.name}.{task2_branch.full_name}".upper()
            assert fqal_task2_name in task4.predecessors or task2_branch.full_name.upper() in task4.predecessors
        finally:
            op.drop(dag)
    finally:
        schema._connection.execute_string(f"drop stage {test_stage}")


@pytest.mark.snowpark
@pytest.mark.usefixtures("anaconda_package_available")
def test_dag_use_function_return_value(schema, db_parameters):
    from snowflake.snowpark import Session

    test_stage = f"{schema.database.name}.{schema.name}.{random_object_name()}"
    test_dag = random_object_name()
    schema._connection.execute_string(f"create or replace stage {test_stage}")

    def task_handler(session: Session) -> str:
        return "task1_return_value"

    try:
        with DAG(
            test_dag,
            schedule=timedelta(minutes=10),
            stage_location=test_stage,
            packages=["snowflake-snowpark-python"],
            use_func_return_value=True,
        ) as dag:
            task1 = DAGTask("task1", task_handler, warehouse=db_parameters["warehouse"])
        op = DAGOperation(schema)
        op.deploy(dag, mode=CreateMode.or_replace)
        try:
            op.run(dag)
            # get the history
            time.sleep(1)
            time_count = 0
            time_limit = 120
            task_name = task1.full_name
            while True:
                result = get_task_history(schema.root.session, task_name)
                if len(result) == 0 or (state := result[0]["STATE"]) in ["SCHEDULED", "EXECUTING"]:
                    if time_count > time_limit:  # run for 2 min
                        raise ValueError(f"Running more than {time_limit} seconds. task: {task_name}, result: {result}")
                    time_count += 10
                    time.sleep(10)
                    continue
                elif state == "SUCCEEDED":
                    assert result[0]["RETURN_VALUE"] == "task1_return_value"
                    break
                else:
                    raise ValueError(f"unexpected state: {state}. {result}")
        finally:
            op.drop(dag)
    finally:
        schema._connection.execute_string(f"drop stage {test_stage}")


def test__use_func_return_value(session):
    from snowflake.snowpark import Session

    def foo(session: Session) -> str:
        return "abc"

    wrapped_foo = _use_func_return_value(foo)
    assert wrapped_foo(session) == "abc"


def test_drop_dag_not_exist(schema):
    test_dag = random_object_name()
    with DAG(test_dag, schedule=timedelta(minutes=10)) as dag:
        prev_task = DAGTask("task1", "select 1")
        for i in range(2, 6):
            task = DAGTask(f"task{i}", f"select {i}")
            task << prev_task
            prev_task = task
    op = DAGOperation(schema)
    op.drop(dag)


@pytest.mark.parametrize("drop_finalizer", [True, False])
def test_drop_dag_by_name(schema, drop_finalizer):
    test_dag = random_object_name()
    with DAG(test_dag, schedule=timedelta(minutes=10)) as dag:
        task = DAGTask("task1", "select 1")
        finalizer = DAGTask("finalizer", "select 2", is_finalizer=True)
        op = DAGOperation(schema)
        op.deploy(dag)
        op.drop(dag.name, drop_finalizer=drop_finalizer)  # expect no exception thrown
    task_list = [t.name for t in schema.tasks.iter()]
    assert task.full_name.upper() not in task_list
    if drop_finalizer:
        assert finalizer.full_name.upper() not in task_list
    else:
        assert finalizer.full_name.upper() in task_list


def test_drop_dag_without_remaining_task(schema):
    test_dag = random_object_name()
    with DAG(test_dag, schedule=timedelta(minutes=10)) as dag:
        task1 = DAGTask("task1", "select 1")
        task2 = DAGTask("task2", "select 2")
        task2 >> task1
    op = DAGOperation(schema)
    op.deploy(dag)
    op.run(dag)

    with DAG(test_dag, schedule=timedelta(minutes=10)) as dag:
        task1 = DAGTask("task3", "select 1")
        task2 = DAGTask("task2", "select 2")
        task2 >> task1
    op.deploy(dag, mode=CreateMode.or_replace)
    op.run(dag)
    task_list = [i.name for i in schema.tasks.iter()]
    assert "task1" not in task_list
    op.drop(dag)


def test_run_dag(schema):
    test_dag = random_object_name()
    with DAG(test_dag, schedule=timedelta(minutes=10)) as dag:
        task1 = DAGTask("task1", "select 1")
        task2 = DAGTask("task2", "select 2")
        task3 = DAGTask("task3", "select 3")
        task2 >> task1 << task3
    op = DAGOperation(schema)
    op.deploy(dag, mode=CreateMode.or_replace)
    try:
        current_run1 = op.get_current_dag_runs(dag)
        assert len(current_run1) == 1
        assert current_run1[0].state == "SCHEDULED"
        op.run(dag)
        current_run2 = op.get_current_dag_runs(dag)
        assert len(current_run2) == 1
        assert current_run2[0].scheduled_time < current_run1[0].scheduled_time
        op.get_complete_dag_runs(
            dag, error_only=False
        )  # TODO: There is a latency so no assertion now. Review this later.
    finally:
        op.drop(dag)


def test_run_retry_last(schema):
    # This test will not retry a task successfully. Instead, it asserts that retry failure error message is expected.
    # So this test makes sure the client side has sent the right request to the server.
    #
    # To test a retry from a failed task, it needs to wait some time for the task to fail.
    # It would be time-consuming and flaky.
    test_dag = random_object_name()
    with DAG(test_dag, schedule=timedelta(minutes=10)) as dag:
        DAGTask("task1", "select 1")
    op = DAGOperation(schema)
    op.deploy(dag, mode=CreateMode.or_replace)
    try:
        with pytest.raises(APIError) as exec_info:
            op.run(dag, retry_last=True)
        assert exec_info.value.status == 400
        assert exec_info.match("(?i)Cannot perform retry")
    finally:
        op.drop(dag)


def test_iter_dags(schema):
    random_name = random_object_name()
    test_dag1 = random_name + "a"
    test_dag2 = random_name + "b"
    with DAG(test_dag1, schedule=timedelta(minutes=10)) as dag1:
        task1 = DAGTask("task1", "select 1")
        task2 = DAGTask("task2", "select 2")
        task3 = DAGTask("task3", "select 3")
        task2 << task1 >> task3
    with DAG(test_dag2, schedule=timedelta(minutes=10)) as dag2:
        task4 = DAGTask("task4", "select 4")
        task5 = DAGTask("task5", "select 5")
        task6 = DAGTask("task6", "select 6")
        task5 << task4 >> task6
    op = DAGOperation(schema)
    try:
        op.deploy(dag1, mode=CreateMode.or_replace)
        try:
            op.deploy(dag2, mode=CreateMode.or_replace)
            fetched_dags = list(op.iter_dags(like=random_name + "%"))
            assert len(fetched_dags) == 2
            assert set(fetched_dags) == {test_dag1.upper(), test_dag2.upper()}
        finally:
            op.drop(dag2)
    finally:
        op.drop(dag1)


def test_dagtask_without_dag_context(schema):
    with pytest.raises(ValueError):
        DAGTask("task1", "select 1")


def test_get_task(schema):
    test_dag = random_object_name()
    with DAG(test_dag, schedule=timedelta(minutes=10)) as dag:
        task1 = DAGTask("task1", "select 1")  # noqa: F841
        task2 = DAGTask("task2", "select 2")
        assert dag.get_task("task2") == task2
        assert dag.get_task("notask") is None


def test_get_finalizer(schema):
    test_dag = random_object_name()
    with DAG(test_dag, schedule=timedelta(minutes=10)) as dag:
        task1 = DAGTask("task1", "select 1", is_finalizer=True)
        task2 = DAGTask("task2", "select 2")
        assert dag.get_task("task2") == task2
        assert dag.get_task("task1") == task1
        assert dag.get_finalizer_task() == task1
    with DAG(test_dag, schedule=timedelta(minutes=10)) as dag:
        task1 = DAGTask("task1", "select 1")
        assert dag.get_task("task1") == task1
        assert dag.get_finalizer_task() is None


def test_add_one_predecessor(schema):
    dag_name = random_object_name()
    with DAG(dag_name, schedule=timedelta(minutes=10)) as dag:
        task1 = DAGTask("task1", "select 1")
        task2 = DAGTask("task2", "select 2")
        task1.add_predecessors(task2)
        assert task1.predecessors == {task2}
        assert dag.get_task("task2") == task2
        assert dag.tasks == [task1, task2]


def test_add_task_list_to_predecessors(schema):
    dag_name = random_object_name()
    with DAG(dag_name, schedule=timedelta(minutes=10)) as dag:
        task1 = DAGTask("task1", "select 1")
        task2 = DAGTask("task2", "select 2")
        task3 = DAGTask("task3", "select 3")
        task1.add_predecessors([task2, task3])
        assert task1.predecessors == set([task2, task3])
        assert dag.get_task("task2") == task2
        assert dag.get_task("task3") == task3
        assert dag.tasks == [task1, task2, task3]


def test_add_task_list_to_predecessors_ignoring_duplicates(schema):
    dag_name = random_object_name()
    with DAG(dag_name, schedule=timedelta(minutes=10)) as dag:
        task1 = DAGTask("task1", "select 1")
        task2 = DAGTask("task2", "select 2")
        task3 = DAGTask("task3", "select 3")
        task1.add_predecessors([task2, task3])
        # Try to add the same list of tasks again; these duplicates will be ignored.
        task1.add_predecessors([task2, task3])
        assert task1.predecessors == set([task2, task3])
        assert dag.get_task("task2") == task2
        assert dag.get_task("task3") == task3
        assert dag.tasks == [task1, task2, task3]


def test_add_invalid_object_to_predecessors(schema):
    dag_name = random_object_name()
    with DAG(dag_name, schedule=timedelta(minutes=10)) as dag:
        task = DAGTask("task1", "select 1")
        # DAGs themselves are not iterable.
        with pytest.raises(TypeError):
            task.add_predecessors(dag)


def test_add_one_successor(schema):
    dag_name = random_object_name()
    with DAG(dag_name, schedule=timedelta(minutes=10)) as dag:
        task1 = DAGTask("task1", "select 1")
        task2 = DAGTask("task2", "select 2")
        task1.add_successors(task2)
        # Successors are not directly represented, but here task1 is a predecessor of task2.
        assert task2.predecessors == set([task1])
        assert dag.tasks == [task1, task2]


def test_add_task_list_to_successors(schema):
    dag_name = random_object_name()
    with DAG(dag_name, schedule=timedelta(minutes=10)) as dag:
        task1 = DAGTask("task1", "select 1")
        task2 = DAGTask("task2", "select 2")
        task3 = DAGTask("task3", "select 3")
        task1.add_successors([task2, task3])
        # As above, successors are not directly represented, but task1 is now a predecessor of both task2 and
        # task3.
        assert task2.predecessors == set([task1])
        assert task3.predecessors == set([task1])
        assert dag.tasks == [task1, task2, task3]


def test_add_invalid_object_to_successors(schema):
    dag_name = random_object_name()
    with DAG(dag_name, schedule=timedelta(minutes=10)) as dag:
        task = DAGTask("task1", "select 1")
        # DAGs themselves are not iterable.
        with pytest.raises(TypeError):
            task.add_successors(dag)


def test_illegal_move_task_to_different_dag(schema):
    dag1_name = random_object_name()
    dag2_name = random_object_name()
    with ExitStack() as dags:
        dags.enter_context(DAG(dag1_name, schedule=timedelta(minutes=10)))
        # dag1 is at the top of the DAG context stack so task1 automatically gets added to it.
        task1 = DAGTask("task1", "select 1")
        # Create dag2 and try to move task1 to it, which should fail.
        dag2 = dags.enter_context(DAG(dag2_name, schedule=timedelta(minutes=10)))
        with pytest.raises(ValueError):
            dag2.add_task(task1)


def test_dag_repr(schema):
    dag_name = random_object_name()
    with DAG(dag_name, schedule=timedelta(minutes=10)) as dag:
        assert repr(dag) == f"<DAG: {dag_name}>"


def test_dagtask_repr(schema):
    dag_name = random_object_name()
    with DAG(dag_name, schedule=timedelta(minutes=10)):
        task = DAGTask("task1", "select 1")
        assert repr(task) == "<DAGTask: task1>"


def test_dag_contains_by_dagtask(schema):
    dag_name = random_object_name()
    with DAG(dag_name, schedule=timedelta(minutes=10)) as dag:
        task = DAGTask("task1", "select 1")
        assert task in dag


def test_dag_contains_by_dag_name(schema):
    dag_name = random_object_name()
    with DAG(dag_name, schedule=timedelta(minutes=10)) as dag:
        task = DAGTask("task1", "select 1")  # noqa: F841
        assert "task1" in dag


def test_dag_contains_by_dag_name_finalizer(schema):
    dag_name = random_object_name()
    with DAG(dag_name, schedule=timedelta(minutes=10)) as dag:
        task = DAGTask("task1", "select 1", is_finalizer=True)  # noqa: F841
        assert "task1" in dag


def test_create_task_in_dag_without_warehouse(schema, warehouses, db_parameters):
    dag_name = random_object_name()
    dag = DAG(
        dag_name,
        schedule=timedelta(minutes=10),
        stage_location="fake_stage",
        warehouse=warehouses[db_parameters["warehouse"]].name,
    )
    with dag:
        task = DAGTask("task", "select 'task'")
    op = DAGOperation(schema)
    try:
        op.deploy(dag, mode=CreateMode.or_replace)
        op.run(dag)
        assert task.warehouse == warehouses[db_parameters["warehouse"]].name
    finally:
        op.drop(dag)


def test_create_task_in_dag_with_warehouse(schema, warehouses, db_parameters):
    dag_name = random_object_name()
    dag = DAG(
        dag_name,
        schedule=timedelta(minutes=10),
        stage_location="fake_stage",
        warehouse=warehouses[db_parameters["warehouse"]].name,
    )
    with dag:
        task = DAGTask("task", "select 'task'", warehouse=warehouses[db_parameters["warehouse"]].name)
    op = DAGOperation(schema)
    try:
        op.deploy(dag, mode=CreateMode.or_replace)
        op.run(dag)
        assert task.warehouse == warehouses[db_parameters["warehouse"]].name
    finally:
        op.drop(dag)


@pytest.mark.snowpark
def test_create_task_in_dag_with_different_warehouse(session, schema, warehouses, db_parameters):
    current_warehouse = session.get_current_warehouse()
    task_warehouse_name = f"SUB_TASK_WAREHOUSE_{random_object_name()}"
    warehouse = Warehouse(name=task_warehouse_name, warehouse_size="SMALL")
    warehouse_ref = None
    try:
        warehouse_ref = warehouses.create(warehouse, mode=CreateMode.or_replace)
        dag_name = random_object_name()
        dag = DAG(
            dag_name,
            schedule=timedelta(minutes=10),
            stage_location="fake_stage",
            warehouse=warehouses[db_parameters["warehouse"]].name,
        )
        with dag:
            task = DAGTask("task", "select 'task'", warehouse=task_warehouse_name)
        op = DAGOperation(schema)
        try:
            op.deploy(dag, mode=CreateMode.or_replace)
            op.run(dag)
            assert task.warehouse == task_warehouse_name
        finally:
            op.drop(dag)
    finally:
        warehouse_ref.drop()
        session.sql(f"USE WAREHOUSE {current_warehouse}").collect()


def test_create_serverless_task_in_dag_with_default_warehouse(schema, warehouses, db_parameters):
    dag_name = random_object_name()
    dag = DAG(
        dag_name,
        schedule=timedelta(minutes=10),
        stage_location="fake_stage",
        warehouse=warehouses[db_parameters["warehouse"]].name,
    )
    with dag:
        task = DAGTask("task", "select 'task'", is_serverless=True)
    op = DAGOperation(schema)
    try:
        op.deploy(dag, mode=CreateMode.or_replace)
        op.run(dag)
        assert task.warehouse is None
    finally:
        op.drop(dag)


def test_create_serverless_task_with_warehouse(schema, warehouses, db_parameters):
    dag_name = random_object_name()
    dag = DAG(
        dag_name,
        schedule=timedelta(minutes=10),
        stage_location="fake_stage",
        warehouse=warehouses[db_parameters["warehouse"]].name,
    )
    with pytest.raises(ValueError):
        with dag:
            _ = DAGTask(
                "task", "select 'task'", warehouse=warehouses[db_parameters["warehouse"]].name, is_serverless=True
            )


def test_create_task_without_warehouse_in_dag_without_warehouse(schema, warehouses, db_parameters):
    dag_name = random_object_name()
    dag = DAG(dag_name, schedule=timedelta(minutes=10), stage_location="fake_stage")
    with dag:
        task = DAGTask("task", "select 'task'", is_serverless=False)
    op = DAGOperation(schema)
    try:
        op.deploy(dag, mode=CreateMode.or_replace)
        op.run(dag)
        assert (
            task.warehouse is None
        )  # the task is created serverless anyway, as the DAG does not have warehouse either
    finally:
        op.drop(dag)


def test_create_dag_with_config(schema, database):
    dag_name = random_object_name()
    config = {"DB_NAME": database.name, "SCHEMA_NAME": schema.name}
    dag = DAG(dag_name, schedule=timedelta(days=1), config=config)
    with dag:
        op = DAGOperation(schema)
        try:
            op.deploy(dag, mode="orReplace")
            op.run(dag)
            dag_task_ref = schema.tasks[dag_name]
            dag_info = dag_task_ref.fetch()
            assert dag_info.config == config
        finally:
            op.drop(dag)


def test_create_dag_with_task_auto_retry_attempts(schema):
    dag_name = random_object_name()
    with DAG(dag_name, schedule=timedelta(days=1), task_auto_retry_attempts=1) as dag:
        op = DAGOperation(schema)
        try:
            op.deploy(dag, mode="orReplace")
            op.run(dag)
            dag_task_ref = schema.tasks[dag_name]
            dag_info = dag_task_ref.fetch()
            assert dag_info.task_auto_retry_attempts == 1
        finally:
            op.drop(dag)


# warnings are suppressed when we run tests in notebooks and stored procs
@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
def test_dag_with_user_task_managed_initial_warehouse_size_raises_deprecation_warning(schema):
    dag_name = random_object_name()
    with warnings.catch_warnings(record=True) as w:
        _ = DAG(dag_name, schedule=timedelta(days=1), user_task_managed_initial_warehouse_size="SMALL")
        assert len(w) == 1
        assert issubclass(w[-1].category, DeprecationWarning)
        assert "Providing user_task_managed_initial_warehouse_size for a dummy root Task is deprecated" in str(
            w[-1].message
        )


@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
def test_child_task_with_error_integration_raises_deprecation_warning(schema):
    dag_name = random_object_name()
    task_name = random_object_name()
    dag = DAG(dag_name, schedule=timedelta(days=1))
    with warnings.catch_warnings(record=True) as w:
        _ = DAGTask(task_name, "select 1", error_integration="non_existing_object", dag=dag)
        assert len(w) == 1
        assert issubclass(w[-1].category, DeprecationWarning)
        assert "error_integration cannot be specified for a child Task." in str(w[-1].message)


@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
def test_drop_with_drop_finalizer_as_false_raises_deprecation_warning(schema):
    with DAG("dag") as dag:
        with warnings.catch_warnings(record=True) as w:
            DAGTask("task", "select 1")
            op = DAGOperation(schema)
            op.deploy(dag)
            op.drop(dag, drop_finalizer=False)
            assert len(w) == 1
            assert issubclass(w[-1].category, DeprecationWarning)
            assert "Setting drop_finalizer to False is deprecated. " in str(w[-1].message)
