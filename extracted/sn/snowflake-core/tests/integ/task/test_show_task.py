#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

import copy
import json

from collections.abc import Iterable, Iterator
from datetime import timedelta

import pytest

from snowflake.core import CreateMode
from snowflake.core.schema import Schema
from snowflake.core.task import Cron, Task, TaskCollection

from ..utils import random_object_name


task_name1 = random_object_name()
task_name2 = random_object_name()
task_name3 = random_object_name()
task_name4 = random_object_name()
name_list = [task_name1, task_name2, task_name3, task_name4]


@pytest.fixture(scope="module")
def tasks(db_parameters, database) -> Iterator[TaskCollection]:
    warehouse_name = db_parameters["warehouse"]
    schema = database.schemas.create(Schema(name=(random_object_name())))
    tasks = [
        Task(
            name=task_name2,
            definition="select current_version()",
            suspend_task_after_num_failures=10,
            schedule=timedelta(minutes=10),
            allow_overlapping_execution=True,
        ),
        Task(
            name=task_name3,
            definition="select current_version()",
            user_task_managed_initial_warehouse_size="xsmall",
            target_completion_interval=timedelta(minutes=5),
            serverless_task_min_statement_size="xsmall",
            serverless_task_max_statement_size="small",
            schedule=Cron("0 9-17 * * SUN", "America/Los_Angeles"),
        ),
        Task(
            name=task_name1,
            definition="select current_version()",
            warehouse=warehouse_name,
            comment="test_task",
            predecessors=[task_name2, task_name3],
        ),
        Task(
            name=task_name4,
            definition="select current_version()",
            warehouse=warehouse_name,
            comment="test_task",
            finalize=task_name2,
        ),
    ]
    task_collection = schema.tasks
    for task in tasks:
        task_collection.create(task, mode=CreateMode.or_replace)
    try:
        yield task_collection
    finally:
        schema.drop()


def test_basic(tasks):
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
def test_finalize_support(tasks):
    database = tasks.database
    schema = tasks.schema
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
def test_serverless_attributes(tasks):
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


def test_limit_from(tasks):
    result = tasks.iter()
    assert len(list(result)) >= 4

    result = tasks.iter(limit=3)
    assert len(list(result)) == 3

    lex_order_names = copy.deepcopy(name_list)
    lex_order_names.sort()
    # use the second last task_name as 'from_name'
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
