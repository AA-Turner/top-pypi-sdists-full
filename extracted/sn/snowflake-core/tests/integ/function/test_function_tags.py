from typing import Optional

import pytest

from snowflake.core.function import FunctionCollection
from snowflake.core.tag import TagResource, TagValue

from ..base_tag_tests import BaseTagTests
from ..utils import random_string
from .utils import create_service_function


pytestmark = [pytest.mark.skip_gov]


class TestFunctionTags(BaseTagTests):
    @pytest.fixture(autouse=True)
    def setup(self, temp_service_for_function, functions: FunctionCollection):
        self.functions = functions
        function_name = random_string(6, "function_for_tag_tests_")
        function_name_with_args = f"{function_name}(REAL)"
        self.function_res = create_service_function(
            function_name,
            ["REAL"],
            "REAL",
            "ep1",
            temp_service_for_function.name,
            functions,
        )
        self.function_name_with_args = function_name_with_args
        try:
            yield
        finally:
            functions[self.function_name_with_args].drop()

    @property
    def resource_level_name(self) -> str:
        return "FUNCTION"

    def set_tags(
        self, tags: dict[TagResource, TagValue], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.functions[self._normalize_resource_name(resource_name) or self.function_name_with_args].set_tags(
            tags, if_exists
        )

    def unset_tags(
        self, tag_resources: set[TagResource], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.functions[self._normalize_resource_name(resource_name) or self.function_name_with_args].unset_tags(
            tag_resources, if_exists
        )

    def get_tags(
        self, with_lineage: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> dict[TagResource, TagValue]:
        return self.functions[self._normalize_resource_name(resource_name) or self.function_name_with_args].get_tags(
            with_lineage
        )

    @staticmethod
    def _normalize_resource_name(name: str | None) -> str | None:
        return f"{name}()" if name and not name.endswith(")") else name
