from typing import Optional

import pytest

from snowflake.core.notification_integration import NotificationEmail, NotificationIntegration
from snowflake.core.tag import TagResource, TagValue

from ..base_tag_tests import BaseTagTests
from ..utils import random_string


pytestmark = [
    pytest.mark.internal_only,
    pytest.mark.use_accountadmin,
]


class TestNotificationIntegrationTags(BaseTagTests):
    @pytest.fixture(autouse=True)
    def setup(self, notification_integrations, set_internal_params):
        self.notification_integrations = notification_integrations
        integration_name = random_string(6, "notification_integration_for_tag_tests_")
        integration = NotificationIntegration(
            name=integration_name,
            notification_hook=NotificationEmail(
                allowed_recipients=["test1@snowflake.com", "test2@snowflake.com"],
                default_recipients=["test1@snowflake.com"],
                default_subject="test default subject",
            ),
            enabled=True,
        )
        with set_internal_params({"ENABLE_LIMIT_RECIPIENTS_TO_SENDING_ACCOUNT": False}):
            self.integration_res = notification_integrations.create(integration)
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
        self.notification_integrations[resource_name or self.integration_res.name].set_tags(tags, if_exists)

    def unset_tags(
        self, tag_resources: set[TagResource], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.notification_integrations[resource_name or self.integration_res.name].unset_tags(tag_resources, if_exists)

    def get_tags(
        self, with_lineage: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> dict[TagResource, TagValue]:
        return self.notification_integrations[resource_name or self.integration_res.name].get_tags(with_lineage)
