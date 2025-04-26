#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

import time
import typing

import pytest

from snowflake.core.task import StoredProcedureCall, Task
from snowflake.core.task.context import TaskContext

from ..utils import get_task_history, random_object_name


if typing.TYPE_CHECKING:
    pass


task_name1 = random_object_name()
task_name2 = random_object_name()


PACKAGES = [
    # Clients do not need to use `atpublic`; it's a convenient decorator used in TaskContext so it needs to be
    # named in the stored procedure packages list.
    "atpublic",
    "snowflake-snowpark-python",
    "snowflake.core"
]


@pytest.mark.usefixtures("anaconda_package_available")
def test_create_task_from_python_function(tasks, session):
    from snowflake.snowpark import Session
    def f(session: Session, table_name: str) -> str:
        context = TaskContext(session)
        value = context.get_current_task_name()
        session.sql(f"insert into {table_name} values(1, '{value}')").collect()
        context.set_return_value(value)
        return session.sql("select 'snowflake'").collect()[0][0]

    def g(session: Session, table_name: str, predecessor_name: str) -> str:
        def assert_none(value: typing.Any):
            if value is not None:
                raise ValueError("assert_none error.")

        def assert_not_none(value: typing.Any):
            if value is None:
                raise ValueError("assert_not_none error.")

        context = TaskContext(session)
        value1 = context.get_predecessor_return_value()
        value2 = context.get_predecessor_return_value(predecessor_name)

        # When using python's own assert statement, _pytest was used but it's not available.
        # Don't know why this happens but the following works.
        assert_not_none(context.get_task_graph_config())
        assert_not_none(context.get_task_graph_config_property("a"))
        assert_not_none(context.get_current_task_name())
        assert_not_none(context.get_current_root_task_name())
        assert_not_none(context.get_current_task_short_name())
        assert_not_none(context.get_current_root_task_uuid())
        assert_not_none(context.get_current_task_graph_original_schedule())
        assert_not_none(context.get_current_task_graph_run_group_id())
        assert_none(context.get_last_successful_task_graph_run_group_id())
        assert_none(context.get_last_successful_task_graph_original_schedule())

        session.sql(f"insert into {table_name} values(2, '{value1}.{value2}')").collect()
        return ""

    stage_name = random_object_name()
    table_name = random_object_name()
    warehouse = session.get_current_warehouse()
    try:
        session.sql(f"create or replace stage {stage_name}").collect()
        session.sql(f"create or replace table {table_name} (id int, str varchar)").collect()

        # create t1
        t1 = Task(
            task_name1,
            StoredProcedureCall(
                f,
                args=[table_name],
                stage_location=stage_name,
                packages=PACKAGES,
            ),
            warehouse=warehouse,
            config={"a": 1},
        )
        with pytest.raises(ValueError) as ex_info:
            _ = t1.sql_definition
        assert "definition of this task can only be retrieved after creating the task" in str(ex_info)
        task1 = tasks.create(t1)
        assert "LANGUAGE PYTHON" in t1.sql_definition

        # create t2
        t2 = Task(
            task_name2,
            StoredProcedureCall(
                g,
                args=[table_name, task_name1.upper()],
                stage_location=stage_name,
                packages=PACKAGES,
            ),
            predecessors=[task1.name],
            warehouse=None,
        )
        with pytest.raises(ValueError) as ex_info:
            _ = t2.sql_definition
        assert "definition of this task can only be retrieved after creating the task" in str(ex_info)
        task2 = tasks.create(t2)
        assert "LANGUAGE PYTHON" in t2.sql_definition

        # resume and execute
        task2.resume()
        task1.execute()

        # get the history
        time.sleep(1)
        time_count = 0
        time_limit = 120
        task_name = task_name1
        while True:
            result = get_task_history(session, task_name)
            assert len(result) > 0
            state = result[0]["STATE"]
            if state in ["SCHEDULED", "EXECUTING"]:
                time.sleep(1)
                time_count += 1
                if time_count > time_limit:  # run for 2 min
                    pytest.xfail("Flaky test, fix trace by SNOW-1317265")
                    raise ValueError(f"Running more than {time_limit} seconds. task: {task_name}, result: {result}")
                continue
            elif state == "SUCCEEDED":
                assert result[0]["ERROR_CODE"] is None
                if task_name == task_name2:
                    break
                task_name = task_name2
            else:
                raise ValueError(f"unexpected state: {state}. {result}")

        result = session.table(table_name).sort("id").collect()
        assert len(result) == 2
        assert result[0][1].count(task_name1.upper()) == 1
        assert result[1][1].count(task_name1.upper()) == 2
    finally:
        session.sql(f"drop stage if exists {stage_name}").collect()
        session.sql(f"drop table if exists {table_name}").collect()
        session.sql(f"drop task if exists {task_name1}").collect()
        session.sql(f"drop task if exists {task_name2}").collect()

@pytest.mark.usefixtures("anaconda_package_available")
def test_create_task_from_python_stored_proc(tasks, session):
    from snowflake.snowpark import Session
    def f(session: Session, table_name: str) -> int:
        session.sql(f"insert into {table_name} values(1, 'abc')").collect()
        return 0

    def g(session: Session, table_name: str) -> float:
        session.sql(f"insert into {table_name} values(2, 'def')").collect()
        return 1.0

    stage_name = random_object_name()
    table_name = random_object_name()
    sp1_name = random_object_name()
    sp2_name = random_object_name()
    warehouse = session.get_current_warehouse()
    try:
        session.sql(f"create or replace stage {stage_name}").collect()
        session.sql(f"create or replace table {table_name} (id int, str varchar)").collect()

        sproc1 = session.sproc.register(
            f,
            stage_location=stage_name,
            packages=PACKAGES,
            name=sp1_name,
            replace=True,
            is_permanent=True,
        )
        sproc2 = session.sproc.register(
            g,
            stage_location=stage_name,
            packages=PACKAGES,
            name=sp2_name,
            replace=True,
            is_permanent=True,
        )
        # create t1
        t1 = Task(
            task_name1,
            StoredProcedureCall(
                sproc1,
                args=[table_name],
            ),
            warehouse=None,
        )
        with pytest.raises(ValueError) as ex_info:
            _ = t1.sql_definition
        assert "definition of this task can only be retrieved after creating the task" in str(ex_info)
        task1 = tasks.create(t1)
        assert "CALL" in t1.sql_definition

        # create t2
        t2 = Task(
            task_name2,
            StoredProcedureCall(
                sproc2,
                args=[table_name],
            ),
            predecessors=[task1.name],
            warehouse=warehouse,
        )
        with pytest.raises(ValueError) as ex_info:
            _ = t2.sql_definition
        assert "definition of this task can only be retrieved after creating the task" in str(ex_info)
        task2 = tasks.create(t2)
        assert "CALL" in t2.sql_definition

        # resume and execute
        task2.resume()
        task1.execute()

        # get the history
        time.sleep(1)
        time_count = 0
        time_limit = 120
        task_name = task_name1
        while True:
            result = get_task_history(session, task_name)
            assert len(result) > 0
            state = result[0]["STATE"]
            if state in ["SCHEDULED", "EXECUTING"]:
                time.sleep(1)
                time_count += 1
                if time_count > time_limit:  # run for 2 min
                    pytest.xfail("Flaky test, fix trace by SNOW-1317265")
                    raise ValueError(f"Running more than {time_limit} seconds. task: {task_name}, result: {result}")
                continue
            elif state == "SUCCEEDED":
                assert result[0]["ERROR_CODE"] is None
                if task_name == task_name2:
                    break
                task_name = task_name2
            else:
                raise ValueError(f"unexpected state: {state}")

        result = session.table(table_name).sort("id").collect()
        assert len(result) == 2
        assert result[0][1] == "abc"
        assert result[1][1] == "def"
    finally:
        session.sql(f"drop stage if exists {stage_name}").collect()
        session.sql(f"drop table if exists {table_name}").collect()
        session.sql(f"drop task if exists {task_name1}").collect()
        session.sql(f"drop task if exists {task_name2}").collect()
        session.sql(f"drop procedure if exists {sp1_name}(string)").collect()
        session.sql(f"drop procedure if exists {sp2_name}(string)").collect()


@pytest.mark.snowpark
def test_create_task_from_python_function_requires_stage_location(tasks):
    with pytest.raises(
        ValueError,
        match="stage_location has to be specified when func is a Python function",
    ):
        StoredProcedureCall(lambda: 1)


@pytest.mark.snowpark
def test_task_context(tasks, session):
    from snowflake.snowpark.exceptions import SnowparkSQLException
    # we are not able to test it in a real task, so just call functions here
    task_context = TaskContext(session)

    with pytest.raises(SnowparkSQLException, match="must be called from within a task"):
        task_context.set_return_value("1")

    with pytest.raises(SnowparkSQLException, match="must be called from within a task"):
        task_context.get_predecessor_return_value()

    with pytest.raises(ValueError):
        task_context.get_predecessor_return_value("invalid name")

    # this function can actually be called outside of a task...
    assert not task_context.get_current_task_name()
