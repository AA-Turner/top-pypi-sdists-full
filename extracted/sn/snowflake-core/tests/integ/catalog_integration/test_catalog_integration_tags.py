from typing import Optional

import pytest

from snowflake.core import CreateMode
from snowflake.core.catalog_integration import CatalogIntegration, CatalogIntegrationCollection, ObjectStore
from snowflake.core.tag import TagResource, TagValue

from ..base_tag_tests import BaseTagTests
from ..utils import random_string


pytestmark = [
    pytest.mark.internal_only,
    pytest.mark.usefixtures("setup_credentials_fixture"),
]


class TestCatalogIntegrationTags(BaseTagTests):
    @pytest.fixture(autouse=True)
    def setup(self, catalog_integrations: CatalogIntegrationCollection):
        self.catalog_integrations = catalog_integrations
        integration_name = random_string(6, "catalog_integration_for_tag_tests_")
        integration = CatalogIntegration(
            name=integration_name,
            catalog=ObjectStore(),
            table_format="ICEBERG",
            enabled=True,
        )
        self.integration_res = catalog_integrations.create(integration, mode=CreateMode.if_not_exists)
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
        self.catalog_integrations[resource_name or self.integration_res.name].set_tags(tags, if_exists)

    def unset_tags(
        self, tag_resources: set[TagResource], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.catalog_integrations[resource_name or self.integration_res.name].unset_tags(tag_resources, if_exists)

    def get_tags(
        self, with_lineage: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> dict[TagResource, TagValue]:
        return self.catalog_integrations[resource_name or self.integration_res.name].get_tags(with_lineage)
