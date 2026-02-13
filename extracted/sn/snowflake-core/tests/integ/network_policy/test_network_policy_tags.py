from typing import Optional

import pytest

from snowflake.core import CreateMode
from snowflake.core.network_policy import NetworkPolicy, NetworkPolicyCollection
from snowflake.core.tag import TagResource, TagValue

from ..base_tag_tests import BaseTagTests
from ..utils import random_string


pytestmark = [pytest.mark.use_accountadmin]


class TestNetworkPolicyTags(BaseTagTests):
    @pytest.fixture(autouse=True)
    def setup(self, network_policies: NetworkPolicyCollection):
        self.network_policies = network_policies
        policy_name = random_string(6, "network_policy_for_tag_tests_")
        policy = NetworkPolicy(
            name=policy_name,
            allowed_ip_list=["0.0.0.0/0"],
        )
        self.policy_res = network_policies.create(policy, mode=CreateMode.if_not_exists)
        try:
            yield
        finally:
            self.policy_res.drop(if_exists=True)

    @property
    def resource_level_name(self) -> str:
        return "NETWORK_POLICY"

    def set_tags(
        self, tags: dict[TagResource, TagValue], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.network_policies[resource_name or self.policy_res.name].set_tags(tags, if_exists)

    def unset_tags(
        self, tag_resources: set[TagResource], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.network_policies[resource_name or self.policy_res.name].unset_tags(tag_resources, if_exists)

    def get_tags(
        self, with_lineage: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> dict[TagResource, TagValue]:
        return self.network_policies[resource_name or self.policy_res.name].get_tags(with_lineage)
