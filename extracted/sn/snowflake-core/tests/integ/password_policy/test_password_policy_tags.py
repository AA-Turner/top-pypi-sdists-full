from typing import Optional

import pytest

from snowflake.core import CreateMode
from snowflake.core.password_policy import PasswordPolicy, PasswordPolicyCollection
from snowflake.core.tag import TagResource, TagValue

from ..base_tag_tests import BaseTagTests
from ..utils import random_string


class TestPasswordPolicyTags(BaseTagTests):
    @pytest.fixture(autouse=True)
    def setup(self, password_policies: PasswordPolicyCollection):
        self.password_policies = password_policies
        policy_name = random_string(6, "password_policy_for_tag_tests_")
        policy = PasswordPolicy(
            name=policy_name,
            password_min_length=8,
            password_max_length=256,
        )
        self.policy_res = password_policies.create(policy, mode=CreateMode.if_not_exists)
        try:
            yield
        finally:
            self.policy_res.drop(if_exists=True)

    @property
    def resource_level_name(self) -> str:
        return "POLICY"

    def set_tags(
        self, tags: dict[TagResource, TagValue], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.password_policies[resource_name or self.policy_res.name].set_tags(tags, if_exists)

    def unset_tags(
        self, tag_resources: set[TagResource], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.password_policies[resource_name or self.policy_res.name].unset_tags(tag_resources, if_exists)

    def get_tags(
        self, with_lineage: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> dict[TagResource, TagValue]:
        return self.password_policies[resource_name or self.policy_res.name].get_tags(with_lineage)
