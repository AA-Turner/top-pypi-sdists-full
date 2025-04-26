#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

import pytest

from snowflake.core.exceptions import NotFoundError

from ..utils import random_object_name


def test_drop_basic(tasks, root):
    tasks["dummy______task"].drop(if_exists=True)
    task_name = random_object_name()
    try:
        create_task = (
            f"create or replace task {task_name} "
            "ALLOW_OVERLAPPING_EXECUTION = true SUSPEND_TASK_AFTER_NUM_FAILURES = 10 "
            "schedule = '10 minute' as select current_version()"
        )
        root.connection.execute_string(create_task)
        tasks[task_name].drop()
        assert len(list(tasks.iter(like=task_name))) == 0
    finally:
        root.connection.execute_string(f"drop task if exists {task_name}")

    with pytest.raises(NotFoundError):
        tasks[random_object_name()].drop()

