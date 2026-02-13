from typing import Optional

import pytest

from snowflake.core import CreateMode
from snowflake.core.database_role import DatabaseRole, DatabaseRoleCollection
from snowflake.core.tag import TagResource, TagValue

from ..base_tag_tests import BaseTagTests
from ..utils import random_string


class TestDatabaseRoleTags(BaseTagTests):
    @pytest.fixture(autouse=True)
    def setup(self, database_roles: DatabaseRoleCollection):
        self.database_roles = database_roles
        db_role_name = random_string(6, "database_role_for_tag_tests_")
        self.database_role_res = database_roles.create(DatabaseRole(name=db_role_name), mode=CreateMode.if_not_exists)
        try:
            yield
        finally:
            self.database_role_res.drop(if_exists=True)

    @property
    def resource_level_name(self) -> str:
        return "DATABASE_ROLE"

    def set_tags(
        self, tags: dict[TagResource, TagValue], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.database_roles[resource_name or self.database_role_res.name].set_tags(tags, if_exists)

    def unset_tags(
        self, tag_resources: set[TagResource], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.database_roles[resource_name or self.database_role_res.name].unset_tags(tag_resources, if_exists)

    def get_tags(
        self, with_lineage: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> dict[TagResource, TagValue]:
        return self.database_roles[resource_name or self.database_role_res.name].get_tags(with_lineage)
