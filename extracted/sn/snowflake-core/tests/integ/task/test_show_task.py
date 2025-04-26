#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

import copy
import json

from collections.abc import Generator, Iterable

import pytest

from snowflake.core.task import Task

from ..utils import random_object_name


task_name1 = random_object_name()
task_name2 = random_object_name()
task_name3 = random_object_name()
task_name4 = random_object_name()
name_list = [task_name1, task_name2, task_name3, task_name4]


@pytest.fixture(scope="module", autouse=True)
def setup(connection) -> Generator[None, None, None]:
    with connection.cursor() as cur:
        warehouse_name: str = cur.execute("select current_warehouse();").fetchone()[0]
        create_task2 = (
            f"create or replace task {task_name2} "
            "ALLOW_OVERLAPPING_EXECUTION = true SUSPEND_TASK_AFTER_NUM_FAILURES = 10 "
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


def test_basic(tasks, database, schema):
    result = _info_list_to_dict(tasks.iter())
    for t in [task_name1, task_name2, task_name3, task_name4]:
        assert t.upper() in result
        res = result[t.upper()]
        task = tasks[t].fetch()
        assert res.created_on == task.created_on
        assert res.name == task.name
        assert task.id == res.id
        assert task.database_name == res.database_name
        assert task.schema_name == res.schema_name
        assert task.owner == res.owner
        assert task.definition == res.definition
        assert task.warehouse == res.warehouse
        assert task.comment == res.comment
        assert task.state == res.state
        assert task.condition == res.condition
        assert task.error_integration == res.error_integration
        assert task.last_committed_on == res.last_committed_on
        assert task.last_suspended_on == res.last_suspended_on


@pytest.mark.min_sf_ver("8.27.0")
def test_finalize_support(tasks, database, schema):
    result = _info_list_to_dict(tasks.iter())
    # assert finalize
    res = result[task_name4.upper()]
    assert res.finalize == f"{task_name2.upper()}"
    for t in [task_name1, task_name2, task_name3]:
        res = result[t.upper()]
        assert res.finalize is None

    # assert task relations
    res = result[task_name4.upper()]
    task_relations = json.loads(res.task_relations)
    assert task_relations["FinalizedRootTask"] == f"{database.name.upper()}.{schema.name.upper()}.{task_name2.upper()}"
    assert task_relations["Predecessors"] == []
    assert task_relations.get("FinalizerTask", None) is None

    res = result[task_name2.upper()]
    task_relations = json.loads(res.task_relations)
    assert task_relations["FinalizerTask"] == f"{database.name.upper()}.{schema.name.upper()}.{task_name4.upper()}"
    assert task_relations["Predecessors"] == []
    assert task_relations.get("FinalizedRootTask", None) is None

    res = result[task_name3.upper()]
    task_relations = json.loads(res.task_relations)
    assert task_relations.get("FinalizerTask", None) is None
    assert task_relations.get("FinalizedRootTask", None) is None
    assert task_relations["Predecessors"] == []

    res = result[task_name1.upper()]
    task_relations = json.loads(res.task_relations)
    assert task_relations.get("FinalizerTask", None) is None
    assert task_relations.get("FinalizedRootTask", None) is None
    assert set(task_relations["Predecessors"]) == set(
        [
            f"{database.name.upper()}.{schema.name.upper()}.{task_name2.upper()}",
            f"{database.name.upper()}.{schema.name.upper()}.{task_name3.upper()}",
        ]
    )


@pytest.mark.min_sf_ver("9.4.0")
def test_serverless_attributes(tasks, database, schema):
    result = _info_list_to_dict(tasks.iter())
    for t in [task_name1, task_name2, task_name3, task_name4]:
        assert t.upper() in result
        res = result[t.upper()]
        task = tasks[t].fetch()
        assert task.user_task_managed_initial_warehouse_size == res.user_task_managed_initial_warehouse_size
        assert task.target_completion_interval == res.target_completion_interval
        assert task.serverless_task_min_statement_size == res.serverless_task_min_statement_size
        assert task.serverless_task_max_statement_size == res.serverless_task_max_statement_size


def test_pattern(tasks):
    result = _info_list_to_dict(tasks.iter(like=task_name1))
    assert task_name1.upper() in result
    assert len(result) == 1
    result = _info_list_to_dict(tasks.iter(like=random_object_name()))
    assert len(result) == 0
    result = _info_list_to_dict(tasks.iter(like="test_object%"))
    assert task_name1.upper() in result
    assert task_name2.upper() in result
    assert task_name3.upper() in result


@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
def test_like(tasks):
    result = tasks.iter(like="")
    assert len(list(result)) == 0


@pytest.mark.flaky
def test_limit_from(tasks):
    result = tasks.iter()
    assert len(list(result)) >= 4

    result = tasks.iter(limit=3)
    assert len(list(result)) == 3

    lex_order_names = copy.deepcopy(name_list)
    lex_order_names.sort()
    # use the second last task_name as 'from_name'
    # TODO: SNOW-1944134 - this can return tasks created in the same schema by other test suites - use separate schema
    #  in each test suite
    result = _info_list_to_dict(tasks.iter(limit=3, from_name=lex_order_names[-2][:-1].upper()))
    assert len(result) >= 2
    assert lex_order_names[-2].upper() in result
    assert lex_order_names[-1].upper() in result

    # test case-sensitive
    result = _info_list_to_dict(tasks.iter(limit=3, from_name=lex_order_names[-2][:-1]))
    assert len(result) == 0


def _info_list_to_dict(info_list: Iterable[Task]) -> dict[str, Task]:
    result = {}
    for info in info_list:
        result[info.name] = info
    return result
