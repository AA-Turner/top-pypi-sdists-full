import typing

from contextlib import suppress
from datetime import timedelta

import pytest

from snowflake.core._internal.utils import normalize_name
from snowflake.core.task import Cron, StoredProcedureCall, Task

from ..utils import random_object_name


if typing.TYPE_CHECKING:
    pass



@pytest.mark.snowpark
@pytest.mark.min_sf_ver("9.4.0")
def test_create_or_alter(tasks, db_parameters):
    from snowflake.snowpark._internal.utils import parse_table_name
    task_name1 = random_object_name()
    task_name2 = random_object_name()
    try:
        task1 = tasks[task_name1]
        task1.create_or_alter(
            Task(
                name=task_name1,
                definition="select current_version()",
                schedule=timedelta(minutes=100),
                warehouse=db_parameters["warehouse"],
                allow_overlapping_execution=True,
                suspend_task_after_num_failures=100,
                config={"a": 1},
                # TODO: testing with error_integration requires setup of notification channel first.
                # error_integration=,
            ),
        )
        task1_data = task1.fetch()
        assert task1_data.name == task_name1.upper()
        assert task1_data.definition == "select current_version()"
        assert task1_data.schedule == timedelta(minutes=100)
        assert task1_data.allow_overlapping_execution is True
        assert task1_data.suspend_task_after_num_failures == 100
        assert task1_data.config == {"a": 1}
        task1_data.schedule = Cron("* * * * *", "America/Los_Angeles")
        task1_data.warehouse = None
        task1_data.allow_overlapping_execution = False
        task1_data.suspend_task_after_num_failures = 200
        task1.create_or_alter(task1_data)
        task1_data_again = tasks[task_name1].fetch()
        assert task1_data_again.schedule == Cron("* * * * *", "America/Los_Angeles")
        assert task1_data_again.allow_overlapping_execution is False
        assert task1_data_again.warehouse is None
        assert task1_data.suspend_task_after_num_failures == 200

        task2 = tasks[task_name2]
        task2.create_or_alter(
            Task(
                name=task_name2,
                definition="select current_version()",
                user_task_managed_initial_warehouse_size="XSMALL",
                target_completion_interval=timedelta(minutes=10),
                serverless_task_min_statement_size="XSMALL",
                serverless_task_max_statement_size="SMALL",
                user_task_timeout_ms=1000000,
                comment="abc",
                predecessors=[task1.name],
                condition="1=1",
                session_parameters={
                    "SNOWPARK_REQUEST_TIMEOUT_IN_SECONDS": 80000,
                    "SNOWPARK_LAZY_ANALYSIS": False,
                },
            )
        )
        task2_data = next((t for t in tasks.iter() if t.name == task_name2.upper()), None)
        assert task2_data.name == task_name2.upper()
        assert task2_data.definition == "select current_version()"
        assert task2_data.user_task_managed_initial_warehouse_size == "XSMALL"
        assert task2_data.target_completion_interval == timedelta(minutes=10)
        assert task2_data.serverless_task_min_statement_size == "XSMALL"
        assert task2_data.serverless_task_max_statement_size == "SMALL"
        assert task2_data.user_task_timeout_ms == 1000000
        assert task2_data.comment == "abc"
        assert task2_data.condition == "1=1"
        assert task2_data.session_parameters == {
            "SNOWPARK_REQUEST_TIMEOUT_IN_SECONDS": 80000,
            "SNOWPARK_LAZY_ANALYSIS": False,
        }
        assert [parse_table_name(x)[-1] for x in task2_data.predecessors] == [normalize_name(task_name1)]
        task2_data.definition = "select 3"
        task2_data.comment = "def"
        task2_data.condition = "2=2"
        task2_data.session_parameters = {
            "SNOWPARK_REQUEST_TIMEOUT_IN_SECONDS": 90000,
            "TIMEZONE": "America/New_York",
        }
        task2.create_or_alter(task2_data)
        task2_data_again = task2.fetch()
        assert task2_data_again.name == task_name2.upper()
        assert task2_data_again.definition == "select 3"
        assert task2_data_again.comment == "def"
        assert task2_data_again.condition == "2=2"
        assert task2_data_again.session_parameters == {
            "SNOWPARK_REQUEST_TIMEOUT_IN_SECONDS": 90000,
            "TIMEZONE": "America/New_York",
        }
        assert [parse_table_name(x)[-1] for x in task2_data_again.predecessors] == [normalize_name(task_name1)]

    finally:
        with suppress(Exception):
            tasks[task_name1].drop()
        with suppress(Exception):
            tasks[task_name2].drop()


def test_create_or_alter_config_and_schedule(tasks, db_parameters):
    task_name1 = random_object_name()
    try:
        task1 = tasks[task_name1]
        task1.create_or_alter(
            Task(
                name=task_name1, definition="select current_version()", schedule=timedelta(minutes=100), config={"a": 1}
            )
        )

        task1.create_or_alter(
            Task(
                name=task_name1,
                definition="select current_version()",
            )
        )
        fetched = task1.fetch()
        assert fetched.config == {}
        assert fetched.schedule is None

        task1.create_or_alter(
            Task(
                name=task_name1, definition="select current_version()", schedule=timedelta(minutes=101), config={"b": 1}
            )
        )
        fetched_again = task1.fetch()
        assert fetched_again.config == {"b": 1}
        assert fetched_again.schedule == timedelta(minutes=101)
        task1.create_or_alter(
            Task(
                name=task_name1,
                definition="select current_version()",
                schedule=Cron("0 0 10-20 * TUE,THU", "America/Los_Angeles"),
            )
        )
        fetched_3rd = task1.fetch()
        fetched_3rd.schedule = Cron("0 0 10-20 * TUE,THU", "America/Los_Angeles")
    finally:
        with suppress(Exception):
            tasks[task_name1].drop()


@pytest.mark.min_sf_ver("8.27.0")
def test_create_or_alter_finalizer(database, schema, tasks):
    task_name1 = random_object_name()
    task_name2 = random_object_name()
    task_name3 = random_object_name()
    try:
        task1 = tasks[task_name1]
        task1.create_or_alter(
            Task(name=task_name1, definition="select current_version()", schedule=timedelta(minutes=100))
        )

        task2 = tasks[task_name2]
        task2.create_or_alter(Task(name=task_name2, definition="select current_version()", finalize=task1.name))

        fetched = task2.fetch()
        fetched1 = task1.fetch()
        assert fetched.finalize == f"{fetched1.name}"

        task3 = tasks[task_name3]
        task3.create_or_alter(
            Task(
                name=task_name3, definition="select current_version()", schedule=timedelta(minutes=100), config={"a": 1}
            )
        )

        task2.create_or_alter(Task(name=task_name2, definition="select current_version()", finalize=task3.name))

        fetched_again = task2.fetch()
        fetched3 = task3.fetch()
        assert fetched_again.finalize == f"{fetched3.name}"
    finally:
        with suppress(Exception):
            tasks[task_name1].drop()
            tasks[task_name2].drop()
            tasks[task_name3].drop()


@pytest.mark.snowpark
@pytest.mark.usefixtures("anaconda_package_available")
def test_create_or_alter_definition_python(tasks, db_parameters):
    from snowflake.snowpark import Session
    def foo1(session: Session) -> None:
        session.sql("select 1").collect()

    def foo2(session: Session) -> None:
        session.sql("select 2").collect()

    test_stage = random_object_name()
    test_task = random_object_name()
    tasks._connection.execute_string(f"create or replace stage {test_stage}")
    try:
        task1 = Task(
            test_task,
            StoredProcedureCall(foo1, stage_location=test_stage, packages=["snowflake-snowpark-python"]),
            warehouse=db_parameters["warehouse"],
        )
        task_ref = tasks[test_task]
        task_ref.create_or_alter(task1)
        try:
            fetched = task_ref.fetch()
            assert "foo1" in fetched.definition
            fetched.definition = StoredProcedureCall(
                foo2, stage_location=test_stage, packages=["snowflake-snowpark-python"]
            )
            task_ref.create_or_alter(fetched)
            fetched_again = task_ref.fetch()
            assert "foo2" in fetched_again.definition
        finally:
            task_ref.drop()
    finally:
        tasks._connection.execute_string(f"drop stage {test_stage}")
