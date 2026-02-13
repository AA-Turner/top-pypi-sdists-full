from typing import Optional

import pytest

from snowflake.core import CreateMode
from snowflake.core.tag import TagResource, TagValue
from snowflake.core.view import View, ViewCollection, ViewColumn

from ..base_tag_tests import BaseTagTests
from ..utils import random_string


class TestViewTags(BaseTagTests):
    @pytest.fixture(autouse=True)
    def setup(self, views: ViewCollection):
        self.views = views
        view_name = random_string(6, "view_for_tag_tests_")
        view = View(
            name=view_name,
            columns=[ViewColumn(name="COL")],
            query="SELECT 1 AS COL1",
        )
        self.view_res = views.create(view, mode=CreateMode.if_not_exists)
        try:
            yield
        finally:
            self.view_res.drop(if_exists=True)

    @property
    def resource_level_name(self) -> str:
        return "TABLE"

    def set_tags(
        self, tags: dict[TagResource, TagValue], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.views[resource_name or self.view_res.name].set_tags(tags, if_exists)

    def unset_tags(
        self, tag_resources: set[TagResource], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.views[resource_name or self.view_res.name].unset_tags(tag_resources, if_exists)

    def get_tags(
        self, with_lineage: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> dict[TagResource, TagValue]:
        return self.views[resource_name or self.view_res.name].get_tags(with_lineage)
