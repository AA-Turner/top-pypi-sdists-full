#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

from contextlib import suppress
from datetime import timedelta

import pytest

from pydantic_core._pydantic_core import ValidationError

from snowflake.core import CreateMode
from snowflake.core.exceptions import APIError, ConflictError, NotFoundError

from ..utils import random_object_name


task_name1 = random_object_name()
task_name2 = random_object_name()
task_name3 = random_object_name()

pytestmark = pytest.mark.snowpark

def test_get_task(tasks):
    with pytest.raises(NotFoundError):
        tasks["abc"].fetch()


def test_create_task_session_parameter(tasks):
    from snowflake.core.task import Task
    query = "select current_version()"
    try:
        # single parameter
        parameters = {"SNOWPARK_REQUEST_TIMEOUT_IN_SECONDS": 80000}
        task = tasks.create(Task(name=task_name1, definition=query, session_parameters=parameters))
        fetched_task = task.fetch()
        assert fetched_task.session_parameters["SNOWPARK_REQUEST_TIMEOUT_IN_SECONDS"] == 80000
        # multiple parameters
        parameters = {
            "SNOWPARK_REQUEST_TIMEOUT_IN_SECONDS": 80000,
            "SNOWPARK_LAZY_ANALYSIS": False,
            "TIMEZONE": "America/New_York",
        }
        task = tasks.create(
            Task(name=task_name1, definition=query, session_parameters=parameters),
            mode=CreateMode.or_replace,
        )
        parameters = task.fetch().session_parameters
        assert parameters["SNOWPARK_REQUEST_TIMEOUT_IN_SECONDS"] == 80000
        assert parameters["SNOWPARK_LAZY_ANALYSIS"] is False
        assert parameters["TIMEZONE"] == "America/New_York"

        # unsupported value
        with pytest.raises(TypeError) as ex_info:
            tasks.create(
                Task(
                    name=task_name1,
                    definition=query,
                    session_parameters={"param": task},
                )
            )
        ex_info.match(
            "Task.session_parameters is a dict. The value of this dict must be one of str, int, float, or bool."
        )
    finally:
        with suppress(NotFoundError):
            tasks[task_name1].drop()


def test_create_task_overwrite(tasks):
    from snowflake.core.task import Task
    try:
        query = "select current_version()"
        task_info = tasks.create(Task(name=task_name1, definition=query)).fetch()
        assert task_name1 == task_info.name.lower()
        assert query in task_info.definition

        with pytest.raises(ConflictError) as ex_info:
            tasks.create(Task(name=task_name1, definition=query))
        assert ex_info.value.status == 409

        created_time = task_info.created_on
        # no error
        task = tasks.create(Task(name=task_name1, definition=query), mode="orreplace")
        # should be the new one
        new_info = task.fetch()
        assert created_time != new_info.created_on
        created_time = new_info.created_on
        tasks.create(Task(name=task_name1, definition=query), mode="ifnotexists")
        # should be the old one
        assert created_time == task.fetch().created_on

    finally:
        with suppress(NotFoundError):
            tasks[task_name1].drop()


def test_create_task_warehouse(tasks, db_parameters):
    from snowflake.core.task import Task
    try:
        task = tasks.create(
            Task(
                name=task_name1,
                definition="select current_version()",
                warehouse=db_parameters["warehouse"],
            ),
        )
        assert task.fetch().warehouse.lower() in db_parameters["warehouse"].lower()
    finally:
        with suppress(NotFoundError):
            tasks[task_name1].drop()


def test_create_task_warehouse_size(tasks):
    from snowflake.core.task import Task
    try:
        task = tasks.create(
            Task(
                name=task_name1,
                definition="select current_version()",
                user_task_managed_initial_warehouse_size="LARGE",
            ),
        )
        assert task.fetch().user_task_managed_initial_warehouse_size == "LARGE"
    finally:
        with suppress(NotFoundError):
            tasks[task_name1].drop()


@pytest.mark.min_sf_ver("9.4.0")
def test_create_task_target_completion_interval(tasks):
    from snowflake.core.task import Task
    try:
        task = tasks.create(
            Task(
                name=task_name1,
                definition="select current_version()",
                target_completion_interval=timedelta(hours=2),
            ),
        )
        assert task.fetch().target_completion_interval == timedelta(minutes=120)
    finally:
        with suppress(NotFoundError):
            tasks[task_name1].drop()


@pytest.mark.min_sf_ver("9.4.0")
def test_create_task_serverless_task_min_statement_size(tasks):
    from snowflake.core.task import Task
    try:
        task = tasks.create(
            Task(
                name=task_name1,
                definition="select current_version()",
                serverless_task_min_statement_size="MEDIUM",
            ),
        )
        assert task.fetch().serverless_task_min_statement_size == "MEDIUM"
    finally:
        with suppress(NotFoundError):
            tasks[task_name1].drop()


@pytest.mark.min_sf_ver("9.4.0")
def test_create_task_serverless_task_max_statement_size(tasks):
    from snowflake.core.task import Task
    try:
        task = tasks.create(
            Task(
                name=task_name1,
                definition="select current_version()",
                serverless_task_max_statement_size="XLARGE",
            ),
        )
        assert task.fetch().serverless_task_max_statement_size == "XLARGE"
    finally:
        with suppress(NotFoundError):
            tasks[task_name1].drop()


def test_create_task_schedule_cron(tasks):
    from snowflake.core.task import Cron, Task
    try:
        schedule = Cron("0 9-17 * * SUN", "America/Los_Angeles")
        task = tasks.create(
            Task(
                name=task_name1,
                definition="select current_version()",
                schedule=schedule,
            ),
        )
        assert task.fetch().schedule == schedule
    finally:
        with suppress(NotFoundError):
            tasks[task_name1].drop()


def test_create_task_schedule_timedelta(tasks):
    from snowflake.core.task import Task
    try:
        with pytest.raises(ValueError) as ex_info:
            tasks.create(
                Task(
                    name=task_name1,
                    definition="select current_version()",
                    schedule=timedelta(microseconds=1),
                ),
            )
        assert ex_info.match("The schedule time delta must be")

        with pytest.raises(ValueError) as ex_info:
            tasks.create(
                Task(
                    name=task_name1,
                    definition="select current_version()",
                    schedule=timedelta(weeks=2),
                )
            )
        assert ex_info.match("The schedule time delta must be")

        task = tasks.create(
            Task(
                name=task_name1,
                definition="select current_version()",
                schedule=timedelta(minutes=11),
            )
        )
        assert task.fetch().schedule.total_seconds() == 660

    finally:
        with suppress(NotFoundError):
            tasks[task_name1].drop()


def test_create_task_allow_overlapping_execution(tasks):
    from snowflake.core.task import Task
    try:
        task = tasks.create(
            Task(
                name=task_name1,
                definition="select current_version()",
                allow_overlapping_execution=True,
            ),
        ).fetch()
        assert task.allow_overlapping_execution
    finally:
        with suppress(NotFoundError):
            tasks[task_name1].drop()


@pytest.mark.parametrize("comment", ["test_comment", "test comment", "TEST*COMMENT", None])
def test_create_task_comment(tasks, comment):
    from snowflake.core.task import Task
    try:
        task = tasks.create(
            Task(
                name=task_name1,
                definition="select current_version()",
                comment=comment,
            )
        ).fetch()
        assert task.comment == (comment if comment else "")
    finally:
        with suppress(NotFoundError):
            tasks[task_name1].drop()


def test_create_task_user_task_timeout_ms(tasks):
    from snowflake.core.task import Task
    try:
        task = tasks.create(
            Task(
                name=task_name1,
                definition="select current_version()",
                user_task_timeout_ms=1234,
            ),
        )
        assert task.fetch().user_task_timeout_ms == 1234
    finally:
        with suppress(NotFoundError):
            tasks[task_name1].drop()


def test_create_task_suspend_task_after_num_failures(tasks):
    from snowflake.core.task import Task
    try:
        task = tasks.create(
            Task(
                name=task_name1,
                definition="select current_version()",
                suspend_task_after_num_failures=1234,
            )
        )
        assert task.fetch().suspend_task_after_num_failures == 1234
    finally:
        with suppress(NotFoundError):
            tasks[task_name1].drop()


def test_create_task_predecessors(tasks):
    from snowflake.core.task import Task
    from snowflake.snowpark._internal.utils import parse_table_name
    try:
        task_name1_with_special_char = '"a b"'
        task1 = tasks.create(
            Task(name=task_name1_with_special_char, definition="select current_version()"),
        )

        task2 = tasks.create(
            Task(name=task_name2, definition="select current_version()"),
        )

        task3 = tasks.create(
            Task(
                name=task_name3,
                definition="select current_version()",
                predecessors=[task1.name, task2.name],
            )
        )

        task3_predecessors = sorted(
            map(
                lambda fqn: parse_table_name(fqn)[-1],
                task3.fetch().predecessors,
            )
        )
        expected = sorted(
            [
                tasks[task_name2].fetch().name,
                tasks[task_name1_with_special_char].fetch().name,
            ]
        )
        assert expected == task3_predecessors
    finally:
        with suppress(Exception):
            tasks[task_name1_with_special_char].drop()
        with suppress(Exception):
            tasks[task_name2].drop()
        with suppress(Exception):
            tasks[task_name3].drop()


def test_create_task_condition(tasks):
    from snowflake.core.task import Task
    try:
        task = tasks.create(
            Task(
                name=task_name1,
                definition="select current_version()",
                condition="SYSTEM$STREAM_HAS_DATA('my_stream')",
            )
        ).fetch()
        assert task.condition == "SYSTEM$STREAM_HAS_DATA('my_stream')"
    finally:
        with suppress(NotFoundError):
            tasks[task_name1].drop()


@pytest.mark.usefixtures("my_integration_exists")
def test_create_task_error_integration(tasks):
    from snowflake.core.task import Task
    try:
        task = tasks.create(
            Task(
                name=task_name1,
                definition="select current_version()",
                error_integration="my_integration",
            )
        ).fetch()
        assert task.error_integration == "my_integration"
    finally:
        with suppress(NotFoundError):
            tasks[task_name1].drop()


# not enabled on jenkins for now, since task tests need some extra setup which is under construction
def test_create_task_task_auto_retry_attempts(tasks):
    from snowflake.core.task import Task
    test_cases = [None, 0, 1, -1, 31]
    try:
        for val in test_cases:
            params = {"name": task_name1, "definition": "select current_version()"}
            if val is not None:
                params["task_auto_retry_attempts"] = val
            try:
                task = tasks.create(Task(**params), mode=CreateMode.or_replace).fetch()
                if val is None:
                    assert task.task_auto_retry_attempts is None
                elif 0 <= val <= 30:
                    assert task.task_auto_retry_attempts == val
                else:
                    pytest.fail("task creation should fail. Valid value range is 0 - 30")
            except ValidationError:
                assert val < 0 or val > 30

        # test child task
        with pytest.raises(APIError) as error:
            tasks.create(
                Task(
                    name=task_name2,
                    definition="select current_version()",
                    predecessors=[task_name1],
                    task_auto_retry_attempts=1,
                )
            )
            assert error.status == 400
            assert "cannot set parameter task_auto_retry_attempts on non-root task" in error.body
    finally:
        with suppress(NotFoundError):
            tasks[task_name1].drop()
