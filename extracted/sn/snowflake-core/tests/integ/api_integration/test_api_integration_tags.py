from typing import Optional

import pytest

from snowflake.core import CreateMode
from snowflake.core.api_integration import ApiIntegration, ApiIntegrationCollection, GitHook
from snowflake.core.tag import TagResource, TagValue

from ..base_tag_tests import BaseTagTests
from ..utils import random_string


class TestApiIntegrationTags(BaseTagTests):
    @pytest.fixture(autouse=True)
    def setup(self, api_integrations: ApiIntegrationCollection):
        self.api_integrations = api_integrations
        integration_name = random_string(6, "api_integration_for_tag_tests_")
        integration = ApiIntegration(
            name=integration_name,
            api_hook=GitHook(allow_any_secret=True),
            api_allowed_prefixes=["https://github.com"],
            enabled=True,
        )
        self.integration_res = api_integrations.create(integration, mode=CreateMode.if_not_exists)
        try:
            yield
        finally:
            self.integration_res.drop(if_exists=True)

    @property
    def resource_level_name(self) -> str:
        return "INTEGRATION"

    def set_tags(
        self, tags: dict[TagResource, TagValue], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.api_integrations[resource_name or self.integration_res.name].set_tags(tags, if_exists)

    def unset_tags(
        self, tag_resources: set[TagResource], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.api_integrations[resource_name or self.integration_res.name].unset_tags(tag_resources, if_exists)

    def get_tags(
        self, with_lineage: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> dict[TagResource, TagValue]:
        return self.api_integrations[resource_name or self.integration_res.name].get_tags(with_lineage)
