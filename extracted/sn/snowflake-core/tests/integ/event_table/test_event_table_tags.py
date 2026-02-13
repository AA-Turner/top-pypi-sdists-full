from typing import Optional

import pytest

from snowflake.core import CreateMode
from snowflake.core.event_table import EventTable, EventTableCollection
from snowflake.core.tag import TagResource, TagValue

from ..base_tag_tests import BaseTagTests
from ..utils import random_string


class TestEventTableTags(BaseTagTests):
    @pytest.fixture(autouse=True)
    def setup(self, event_tables: EventTableCollection):
        self.event_tables = event_tables
        event_table_name = random_string(6, "event_table_for_tag_tests_")
        self.event_table_res = event_tables.create(EventTable(name=event_table_name), mode=CreateMode.if_not_exists)
        try:
            yield
        finally:
            self.event_table_res.drop(if_exists=True)

    @property
    def resource_level_name(self) -> str:
        return "TABLE"

    def set_tags(
        self, tags: dict[TagResource, TagValue], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.event_tables[resource_name or self.event_table_res.name].set_tags(tags, if_exists)

    def unset_tags(
        self, tag_resources: set[TagResource], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.event_tables[resource_name or self.event_table_res.name].unset_tags(tag_resources, if_exists)

    def get_tags(
        self, with_lineage: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> dict[TagResource, TagValue]:
        return self.event_tables[resource_name or self.event_table_res.name].get_tags(with_lineage)
