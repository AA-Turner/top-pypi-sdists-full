from typing import Optional

import pytest

from snowflake.core import CreateMode
from snowflake.core.database import Database, DatabaseCollection
from snowflake.core.tag import TagResource, TagValue

from ..base_tag_tests import BaseTagTests
from ..utils import random_string


class TestDatabaseTags(BaseTagTests):
    @pytest.fixture(autouse=True)
    def setup(self, databases: DatabaseCollection, backup_database_schema):
        self.databases = databases
        database_name = random_string(6, "database_for_tag_tests_")
        self.db_res = databases.create(Database(name=database_name), mode=CreateMode.if_not_exists)
        try:
            yield
        finally:
            self.db_res.drop(if_exists=True)

    @property
    def resource_level_name(self) -> str:
        return "DATABASE"

    def set_tags(
        self, tags: dict[TagResource, TagValue], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.databases[resource_name or self.db_res.name].set_tags(tags, if_exists)

    def unset_tags(
        self, tag_resources: set[TagResource], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.databases[resource_name or self.db_res.name].unset_tags(tag_resources, if_exists)

    def get_tags(
        self, with_lineage: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> dict[TagResource, TagValue]:
        return self.databases[resource_name or self.db_res.name].get_tags(with_lineage)
