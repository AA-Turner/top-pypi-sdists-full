#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

import json

from collections.abc import Generator
from datetime import timedelta

import pytest

from snowflake.connector import DictCursor
from snowflake.core.exceptions import NotFoundError

from ..utils import random_object_name


task_name1 = random_object_name()
task_name2 = random_object_name()
task_name3 = random_object_name()
task_name4 = random_object_name()


@pytest.fixture(scope="module", autouse=True)
def setup(tasks, connection) -> Generator[None, None, None]:
    with connection.cursor() as cur:
        warehouse_name: str = cur.execute("select current_warehouse();").fetchone()[0]
        create_task2 = (
            f"create or replace task {task_name2} "
            "ALLOW_OVERLAPPING_EXECUTION = true SUSPEND_TASK_AFTER_NUM_FAILURES = 10 "
            "TIMEZONE='America/Los_Angeles' SNOWPARK_REQUEST_TIMEOUT_IN_SECONDS = 100 QUERY_RESULT_FORMAT='ARROW'"
            "schedule = '10 minute' as select current_version()"
        )
        cur.execute(create_task2).fetchone()
        create_task3 = (
            f"create or replace task {task_name3} "
            "user_task_managed_initial_warehouse_size = 'xsmall' "
            "target_completion_interval = '5 MINUTE' "
            "serverless_task_min_statement_size = 'xsmall' "
            "serverless_task_max_statement_size = 'small' "
            "SCHEDULE = 'USING CRON 0 9-17 * * SUN America/Los_Angeles' as select current_version()"
        )
        cur.execute(create_task3).fetchone()
        create_task1 = (
            f"create or replace task {task_name1} "
            f"warehouse = {warehouse_name} "
            "comment = 'test_task' "
            f"after {task_name2}, {task_name3} "
            "as select current_version()"
        )
        cur.execute(create_task1).fetchone()
        create_task4 = (
            f"create or replace task {task_name4} "
            f"warehouse = {warehouse_name} "
            "comment = 'test_task' "
            f"finalize = {task_name2} "
            "as select current_version()"
        )
        cur.execute(create_task4).fetchone()
        yield
        drop_task1 = f"drop task if exists {task_name1}"
        cur.execute(drop_task1).fetchone()
        drop_task2 = f"drop task if exists {task_name2}"
        cur.execute(drop_task2).fetchone()
        drop_task3 = f"drop task if exists {task_name2}"
        cur.execute(drop_task3).fetchone()
        drop_task4 = f"drop task if exists {task_name4}"
        cur.execute(drop_task4).fetchone()


@pytest.mark.snowpark
def test_load_task_basic(tasks, session):
    from snowflake.snowpark._internal.utils import parse_table_name
    task = tasks[task_name1].fetch()
    result = session._conn._conn.cursor(DictCursor).execute(f"describe task {task_name1}")
    for res in result:
        assert res["created_on"] == task.created_on
        assert res["name"] == task.name
        assert task.name == task_name1.upper()
        assert task.id == res["id"]
        assert task.database_name == res["database_name"]
        assert task.schema_name == res["schema_name"]
        assert task.owner == res["owner"]
        assert task.definition == res["definition"]
        assert task.warehouse == res["warehouse"]
        assert task.comment == res["comment"]
        assert task.comment == "test_task"
        assert task.state == res["state"]
        assert task.condition == res["condition"]
        assert task.error_integration is None
        assert task.last_committed_on == res["last_committed_on"]
        assert task.last_suspended_on == res["last_suspended_on"]
        # check predecessors
        parent_ids: list[str] = sorted(map(lambda name: parse_table_name(name)[-1], task.predecessors))
        expected = sorted(
            [
                tasks[task_name2].fetch().name,
                tasks[task_name3].fetch().name,
            ]
        )
        assert expected == parent_ids


def test_finalize_support(tasks, session):
    for t in [task_name1, task_name2, task_name3, task_name4]:
        task = tasks[t].fetch()
        result = session._conn._conn.cursor(DictCursor).execute(f"describe as resource task {t}")
        for res in result:
            task_relations_result = json.loads(json.loads(res["As Resource"])["task_relations"])
            task_relations_fetch = json.loads(task.task_relations)
            assert task_relations_result == task_relations_fetch


def test_load_task_allow_overlapping_execution(tasks):
    task = tasks[task_name2].fetch()
    assert task.allow_overlapping_execution


def test_load_task_user_task_managed_initial_warehouse_size(tasks):
    task = tasks[task_name3]
    assert task.fetch().user_task_managed_initial_warehouse_size == "XSMALL"


@pytest.mark.min_sf_ver("9.4.0")
def test_load_task_target_completion_interval(tasks):
    task = tasks[task_name3]
    assert task.fetch().target_completion_interval == timedelta(minutes=5)


@pytest.mark.min_sf_ver("9.4.0")
def test_load_task_serverless_task_min_statement_size(tasks):
    task = tasks[task_name3]
    assert task.fetch().serverless_task_min_statement_size == "XSMALL"


@pytest.mark.min_sf_ver("9.4.0")
def test_load_task_serverless_task_max_statement_size(tasks):
    task = tasks[task_name3]
    assert task.fetch().serverless_task_max_statement_size == "SMALL"


def test_show_parameters(tasks):
    task = tasks[task_name2]
    task_payload = task.fetch()
    local_parameters = task_payload.session_parameters
    assert local_parameters["TIMEZONE"] == "America/Los_Angeles"
    assert local_parameters["SNOWPARK_REQUEST_TIMEOUT_IN_SECONDS"] == 100
    assert local_parameters["QUERY_RESULT_FORMAT"] == "ARROW"


def test_load_task_failure(tasks):
    # lazy, no error
    task = tasks["task_not_exists"]

    with pytest.raises(NotFoundError):
        task.fetch()


def test_load_task_schedule(tasks):
    task2 = tasks[task_name2].fetch()
    assert task2.schedule == timedelta(minutes=10)
    task3 = tasks[task_name3].fetch()
    assert task3.schedule.expr == "0 9-17 * * SUN"
    assert task3.schedule.timezone == "America/Los_Angeles"
