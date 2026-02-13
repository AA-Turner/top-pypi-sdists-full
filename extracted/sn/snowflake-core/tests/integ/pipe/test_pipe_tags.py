from typing import Optional

import pytest

from snowflake.core import CreateMode
from snowflake.core.pipe import Pipe, PipeCollection
from snowflake.core.stage import StageResource
from snowflake.core.table import TableResource
from snowflake.core.tag import TagResource, TagValue

from ..base_tag_tests import BaseTagTests
from ..utils import random_string


class TestPipeTags(BaseTagTests):
    @pytest.fixture(autouse=True)
    def setup(self, pipes: PipeCollection, temp_table: TableResource, temp_stage: StageResource):
        self.pipes = pipes
        pipe_name = random_string(6, "pipe_for_tag_tests_")
        pipe = Pipe(
            name=pipe_name,
            copy_statement=f"COPY into {temp_table.name} from @{temp_stage.name}",
        )
        self.pipe_res = pipes.create(pipe, mode=CreateMode.if_not_exists)
        try:
            yield
        finally:
            self.pipe_res.drop(if_exists=True)

    @property
    def resource_level_name(self) -> str:
        return "PIPE"

    def set_tags(
        self, tags: dict[TagResource, TagValue], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.pipes[resource_name or self.pipe_res.name].set_tags(tags, if_exists)

    def unset_tags(
        self, tag_resources: set[TagResource], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.pipes[resource_name or self.pipe_res.name].unset_tags(tag_resources, if_exists)

    def get_tags(
        self, with_lineage: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> dict[TagResource, TagValue]:
        return self.pipes[resource_name or self.pipe_res.name].get_tags(with_lineage)
