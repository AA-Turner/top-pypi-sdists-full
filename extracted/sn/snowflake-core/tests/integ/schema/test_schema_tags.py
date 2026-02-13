from typing import Optional

import pytest

from snowflake.core import CreateMode
from snowflake.core.schema import Schema, SchemaCollection
from snowflake.core.tag import TagResource, TagValue

from ..base_tag_tests import BaseTagTests
from ..utils import random_string


class TestSchemaTags(BaseTagTests):
    @pytest.fixture(autouse=True)
    def setup(self, schemas: SchemaCollection, backup_database_schema):
        self.schemas = schemas
        schema_name = random_string(6, "schema_for_tag_tests_")
        self.schema_res = schemas.create(Schema(name=schema_name), mode=CreateMode.if_not_exists)
        try:
            yield
        finally:
            self.schema_res.drop(if_exists=True)

    @property
    def resource_level_name(self) -> str:
        return "SCHEMA"

    def set_tags(
        self, tags: dict[TagResource, TagValue], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.schemas[resource_name or self.schema_res.name].set_tags(tags, if_exists)

    def unset_tags(
        self, tag_resources: set[TagResource], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.schemas[resource_name or self.schema_res.name].unset_tags(tag_resources, if_exists)

    def get_tags(
        self, with_lineage: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> dict[TagResource, TagValue]:
        return self.schemas[resource_name or self.schema_res.name].get_tags(with_lineage)
