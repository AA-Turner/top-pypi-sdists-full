from contextlib import suppress

from snowflake.core.exceptions import NotFoundError

from ..utils import random_object_name


task_name1 = random_object_name()

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
        assert task.fetch().state == "suspended"
        task.suspend()
        assert task.fetch().state == "suspended"
        task.resume()
        assert task.fetch().state != "suspended"
        task.suspend()
        assert task.fetch().state == "suspended"
    finally:
        with suppress(NotFoundError):
            tasks[task_name1].drop()
