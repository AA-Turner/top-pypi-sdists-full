from typing import Optional

import pytest

from snowflake.core import CreateMode
from snowflake.core.alert import Alert, AlertCollection, MinutesSchedule
from snowflake.core.tag import TagResource, TagValue

from ..base_tag_tests import BaseTagTests
from ..utils import random_string


class TestAlertTags(BaseTagTests):
    @pytest.fixture(autouse=True)
    def setup(self, alerts: AlertCollection):
        self.alerts = alerts
        alert_name = random_string(6, "alert_for_tag_tests_")
        self.alert_res = alerts.create(
            Alert(
                name=alert_name,
                condition="SELECT 1",
                action="SELECT 2",
                schedule=MinutesSchedule(minutes=1),
            ),
            mode=CreateMode.if_not_exists,
        )
        try:
            yield
        finally:
            self.alert_res.drop(if_exists=True)

    @property
    def resource_level_name(self) -> str:
        return "ALERT"

    def set_tags(
        self, tags: dict[TagResource, TagValue], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.alerts[resource_name or self.alert_res.name].set_tags(tags, if_exists)

    def unset_tags(
        self, tag_resources: set[TagResource], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.alerts[resource_name or self.alert_res.name].unset_tags(tag_resources, if_exists)

    def get_tags(
        self, with_lineage: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> dict[TagResource, TagValue]:
        return self.alerts[resource_name or self.alert_res.name].get_tags(with_lineage)
