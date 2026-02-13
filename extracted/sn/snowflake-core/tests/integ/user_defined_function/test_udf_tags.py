from typing import Optional

import pytest

from snowflake.core import CreateMode
from snowflake.core.tag import TagResource, TagValue
from snowflake.core.user_defined_function import (
    ReturnDataType,
    SQLFunction,
    UserDefinedFunction,
    UserDefinedFunctionCollection,
)

from ..base_tag_tests import BaseTagTests
from ..utils import random_string


class TestUserDefinedFunctionTags(BaseTagTests):
    @pytest.fixture(autouse=True)
    def setup(self, user_defined_functions: UserDefinedFunctionCollection):
        self.user_defined_functions = user_defined_functions
        udf_name = random_string(6, "udf_for_tag_tests_")
        udf = UserDefinedFunction(
            name=udf_name,
            arguments=[],
            return_type=ReturnDataType(datatype="VARCHAR"),
            language_config=SQLFunction(),
            body="SELECT 'test'",
        )
        self.udf_res = user_defined_functions.create(udf, mode=CreateMode.if_not_exists)
        try:
            yield
        finally:
            self.udf_res.drop(if_exists=True)

    @property
    def resource_level_name(self) -> str:
        return "FUNCTION"

    def set_tags(
        self, tags: dict[TagResource, TagValue], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.user_defined_functions[
            self._normalize_resource_name(resource_name) or self.udf_res.name_with_args
        ].set_tags(tags, if_exists)

    def unset_tags(
        self, tag_resources: set[TagResource], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.user_defined_functions[
            self._normalize_resource_name(resource_name) or self.udf_res.name_with_args
        ].unset_tags(tag_resources, if_exists)

    def get_tags(
        self, with_lineage: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> dict[TagResource, TagValue]:
        return self.user_defined_functions[
            self._normalize_resource_name(resource_name) or self.udf_res.name_with_args
        ].get_tags(with_lineage)

    @staticmethod
    def _normalize_resource_name(name: str | None) -> str | None:
        return f"{name}()" if name and not name.endswith(")") else name
