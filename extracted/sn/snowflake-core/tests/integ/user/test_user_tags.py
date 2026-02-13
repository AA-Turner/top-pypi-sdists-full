from typing import Optional

import pytest

from snowflake.core import CreateMode
from snowflake.core.tag import TagResource, TagValue
from snowflake.core.user import User, UserCollection

from ..base_tag_tests import BaseTagTests
from ..utils import random_string


@pytest.mark.snowpark
@pytest.mark.use_accountadmin
class TestUserTags(BaseTagTests):
    @pytest.fixture(autouse=True)
    def setup(self, users: UserCollection):
        self.users = users
        user_name = random_string(6, "user_for_tag_tests_")
        self.user_res = users.create(User(name=user_name), mode=CreateMode.if_not_exists)
        try:
            yield
        finally:
            self.user_res.drop(if_exists=True)

    @property
    def resource_level_name(self) -> str:
        return "USER"

    def set_tags(
        self, tags: dict[TagResource, TagValue], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.users[resource_name or self.user_res.name].set_tags(tags, if_exists)

    def unset_tags(
        self, tag_resources: set[TagResource], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.users[resource_name or self.user_res.name].unset_tags(tag_resources, if_exists)

    def get_tags(
        self, with_lineage: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> dict[TagResource, TagValue]:
        return self.users[resource_name or self.user_res.name].get_tags(with_lineage)
