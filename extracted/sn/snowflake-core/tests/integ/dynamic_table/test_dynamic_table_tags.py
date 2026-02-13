from typing import Optional

import pytest

from snowflake.core import CreateMode
from snowflake.core.dynamic_table import (
    DownstreamLag,
    DynamicTable,
    DynamicTableCollection,
    DynamicTableColumn,
)
from snowflake.core.table import TableResource
from snowflake.core.tag import TagResource, TagValue
from snowflake.core.warehouse import WarehouseResource

from ..base_tag_tests import BaseTagTests
from ..utils import random_string


class TestDynamicTableTags(BaseTagTests):
    @pytest.fixture(autouse=True)
    def setup(self, dynamic_tables: DynamicTableCollection, warehouse: WarehouseResource, temp_table: TableResource):
        self.dynamic_tables = dynamic_tables
        dynamic_table_name = random_string(6, "dynamic_table_for_tag_tests_")
        dynamic_table = DynamicTable(
            name=dynamic_table_name,
            warehouse=warehouse.name,
            target_lag=DownstreamLag(),
            columns=[DynamicTableColumn(name="c1"), DynamicTableColumn(name="c2")],
            query=f"SELECT * FROM {temp_table.name}",
        )
        self.dynamic_table_res = dynamic_tables.create(dynamic_table, mode=CreateMode.if_not_exists)
        try:
            yield
        finally:
            self.dynamic_table_res.drop(if_exists=True)

    @property
    def resource_level_name(self) -> str:
        return "TABLE"

    def set_tags(
        self, tags: dict[TagResource, TagValue], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.dynamic_tables[resource_name or self.dynamic_table_res.name].set_tags(tags, if_exists)

    def unset_tags(
        self, tag_resources: set[TagResource], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.dynamic_tables[resource_name or self.dynamic_table_res.name].unset_tags(tag_resources, if_exists)

    def get_tags(
        self, with_lineage: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> dict[TagResource, TagValue]:
        return self.dynamic_tables[resource_name or self.dynamic_table_res.name].get_tags(with_lineage)
