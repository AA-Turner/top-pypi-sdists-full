#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#
from contextlib import suppress

import pytest

from snowflake.core.exceptions import APIError, NotFoundError
from snowflake.core.task import Task

from ..utils import get_task_history, random_object_name


def test_execute_basic(tasks, session):
    task_name = random_object_name()
    try:
        task = tasks.create(Task(name=task_name, definition="select 1"))
        assert not get_task_history(session, task.name)
        task.execute()
        assert len(get_task_history(session, task.name)) == 1
        with pytest.raises(NotFoundError):
            tasks["not_exists"].execute()
    finally:
        with suppress(NotFoundError):
            tasks[task_name].drop()


def test_execute_retry_last(tasks, session):
    # This test will not retry a task successfully. Instead, it asserts that the retry failure error message
    # is expected.  This test makes sure the client side has sent the right request to the server.
    #
    # To test a retry from a failed task, it needs to wait some time for the task to fail.  It would be
    # time-consuming and flaky.
    task_name = random_object_name()
    try:
        task = tasks.create(Task(name=task_name, definition="select 1"))
        with pytest.raises(APIError) as exec_info:
            task.execute(retry_last=True)
        assert exec_info.value.status == 400
        assert exec_info.match("(?i)Cannot perform retry")
    finally:
        with suppress(NotFoundError):
            tasks[task_name].drop()
