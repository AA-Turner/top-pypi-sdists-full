#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

"""Integration tests for :meth:`~snowflake.core.task.Task.fetch_task_dependents`."""

from __future__ import annotations

from collections.abc import Set

from snowflake.core.schema import SchemaResource
from snowflake.core.task import Task, TaskResource


def test_fetch_task_dependents_basic(temp_schema: SchemaResource):
    schema = temp_schema
    task_a = schema.tasks.create(Task("A", "SELECT 1"))
    task_b = schema.tasks.create(Task("B", "SELECT 2", predecessors=[task_a.name]))
    task_c = schema.tasks.create(Task("C", "SELECT 3", predecessors=[task_a.name]))
    task_d = schema.tasks.create(Task("D", "SELECT 4", predecessors=[task_b.name, task_c.name]))

    def check_fetch_task_dependents(task: TaskResource, expected: Set[str], recursive: bool):
        expected |= {task.name}  # The result always includes the task itself
        assert {t.name for t in task.fetch_task_dependents(recursive=recursive)} == expected

    check_fetch_task_dependents(task_a, {task_b.name, task_c.name}, False)
    check_fetch_task_dependents(task_a, {task_b.name, task_c.name, task_d.name}, True)
    check_fetch_task_dependents(task_b, {task_d.name}, False)
    check_fetch_task_dependents(task_b, {task_d.name}, True)
    check_fetch_task_dependents(task_c, {task_d.name}, False)
    check_fetch_task_dependents(task_c, {task_d.name}, True)
    check_fetch_task_dependents(task_d, frozenset(), False)
    check_fetch_task_dependents(task_d, frozenset(), True)
