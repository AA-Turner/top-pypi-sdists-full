from typing import Optional

import pytest

from snowflake.core import CreateMode
from snowflake.core.tag import TagResource, TagValue
from snowflake.core.task import Task, TaskCollection

from ..base_tag_tests import BaseTagTests
from ..utils import random_string


class TestTaskTags(BaseTagTests):
    @pytest.fixture(autouse=True)
    def setup(self, tasks: TaskCollection):
        self.tasks = tasks
        task_name = random_string(6, "task_for_tag_tests_")
        self.task_res = tasks.create(
            Task(name=task_name, definition="select current_version()"), mode=CreateMode.if_not_exists
        )
        try:
            yield
        finally:
            self.task_res.drop(if_exists=True)

    @property
    def resource_level_name(self) -> str:
        return "TASK"

    def set_tags(
        self, tags: dict[TagResource, TagValue], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.tasks[resource_name or self.task_res.name].set_tags(tags, if_exists)

    def unset_tags(
        self, tag_resources: set[TagResource], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.tasks[resource_name or self.task_res.name].unset_tags(tag_resources, if_exists)

    def get_tags(
        self, with_lineage: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> dict[TagResource, TagValue]:
        return self.tasks[resource_name or self.task_res.name].get_tags(with_lineage)
