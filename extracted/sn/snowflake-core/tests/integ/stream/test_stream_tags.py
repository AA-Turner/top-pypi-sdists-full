from typing import Optional

import pytest

from snowflake.core import CreateMode
from snowflake.core.stream import Stream, StreamCollection, StreamSourceTable
from snowflake.core.table import TableResource
from snowflake.core.tag import TagResource, TagValue

from ..base_tag_tests import BaseTagTests
from ..utils import random_string


class TestStreamTags(BaseTagTests):
    @pytest.fixture(autouse=True)
    def setup(self, streams: StreamCollection, temp_table: TableResource):
        self.streams = streams
        stream_name = random_string(6, "stream_for_tag_tests_")
        stream = Stream(
            name=stream_name,
            stream_source=StreamSourceTable(name=temp_table.name),
        )
        self.stream_res = streams.create(stream, mode=CreateMode.if_not_exists)
        try:
            yield
        finally:
            self.stream_res.drop(if_exists=True)

    @property
    def resource_level_name(self) -> str:
        return "STREAM"

    def set_tags(
        self, tags: dict[TagResource, TagValue], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.streams[resource_name or self.stream_res.name].set_tags(tags, if_exists)

    def unset_tags(
        self, tag_resources: set[TagResource], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.streams[resource_name or self.stream_res.name].unset_tags(tag_resources, if_exists)

    def get_tags(
        self, with_lineage: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> dict[TagResource, TagValue]:
        return self.streams[resource_name or self.stream_res.name].get_tags(with_lineage)
