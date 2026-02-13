from typing import Optional

import pytest

from snowflake.core.streamlit import Streamlit, StreamlitCollection
from snowflake.core.tag import TagResource, TagValue

from ..base_tag_tests import BaseTagTests
from ..utils import random_string


class TestStreamlitTags(BaseTagTests):
    @pytest.fixture(autouse=True)
    def setup(self, streamlits: StreamlitCollection, streamlit_stage_with_file, warehouse, streamlit_main_file):
        self.streamlits = streamlits
        name = random_string(6, "streamlit_for_tag_tests_")
        streamlit = Streamlit(
            name=name,
            query_warehouse=warehouse.name,
            source_location=f"@{streamlit_stage_with_file.name}",
            main_file=streamlit_main_file,
        )
        self.streamlit_res = streamlits.create(streamlit)
        try:
            yield
        finally:
            self.streamlit_res.drop(if_exists=True)

    @property
    def resource_level_name(self) -> str:
        return "STREAMLIT"

    def set_tags(
        self, tags: dict[TagResource, TagValue], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.streamlits[resource_name or self.streamlit_res.name].set_tags(tags, if_exists)

    def unset_tags(
        self, tag_resources: set[TagResource], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.streamlits[resource_name or self.streamlit_res.name].unset_tags(tag_resources, if_exists)

    def get_tags(
        self, with_lineage: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> dict[TagResource, TagValue]:
        return self.streamlits[resource_name or self.streamlit_res.name].get_tags(with_lineage)
