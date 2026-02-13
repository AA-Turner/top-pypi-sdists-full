from typing import Optional

import pytest

from snowflake.core import CreateMode
from snowflake.core.role import Role, RoleCollection
from snowflake.core.tag import TagResource, TagValue

from ..base_tag_tests import BaseTagTests
from ..utils import random_string


@pytest.mark.use_accountadmin
class TestRoleTags(BaseTagTests):
    @pytest.fixture(autouse=True)
    def setup(self, roles: RoleCollection):
        self.roles = roles
        role_name = random_string(6, "role_for_tag_tests_")
        self.role_res = roles.create(Role(name=role_name), mode=CreateMode.if_not_exists)
        try:
            yield
        finally:
            self.role_res.drop(if_exists=True)

    @property
    def resource_level_name(self) -> str:
        return "ROLE"

    def set_tags(
        self, tags: dict[TagResource, TagValue], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.roles[resource_name or self.role_res.name].set_tags(tags, if_exists)

    def unset_tags(
        self, tag_resources: set[TagResource], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.roles[resource_name or self.role_res.name].unset_tags(tag_resources, if_exists)

    def get_tags(
        self, with_lineage: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> dict[TagResource, TagValue]:
        return self.roles[resource_name or self.role_res.name].get_tags(with_lineage)
