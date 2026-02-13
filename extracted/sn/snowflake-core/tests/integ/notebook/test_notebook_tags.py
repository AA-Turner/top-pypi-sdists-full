from typing import Optional

import pytest

from snowflake.core import CreateMode
from snowflake.core.notebook import Notebook, NotebookCollection
from snowflake.core.tag import TagResource, TagValue

from ..base_tag_tests import BaseTagTests
from ..utils import random_string


class TestNotebookTags(BaseTagTests):
    @pytest.fixture(autouse=True)
    def setup(self, notebooks: NotebookCollection):
        self.notebooks = notebooks
        notebook_name = random_string(6, "notebook_for_tag_tests_")
        notebook = Notebook(name=notebook_name)
        self.notebook_res = notebooks.create(notebook, mode=CreateMode.if_not_exists)
        try:
            yield
        finally:
            self.notebook_res.drop(if_exists=True)

    @property
    def resource_level_name(self) -> str:
        return "NOTEBOOK"

    def set_tags(
        self, tags: dict[TagResource, TagValue], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.notebooks[resource_name or self.notebook_res.name].set_tags(tags, if_exists)

    def unset_tags(
        self, tag_resources: set[TagResource], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.notebooks[resource_name or self.notebook_res.name].unset_tags(tag_resources, if_exists)

    def get_tags(
        self, with_lineage: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> dict[TagResource, TagValue]:
        return self.notebooks[resource_name or self.notebook_res.name].get_tags(with_lineage)
