from typing import Optional

import pytest

from snowflake.core import CreateMode
from snowflake.core.procedure import Procedure, ProcedureCollection, ReturnDataType, SQLFunction
from snowflake.core.tag import TagResource, TagValue

from ..base_tag_tests import BaseTagTests
from ..utils import random_string


class TestProcedureTags(BaseTagTests):
    @pytest.fixture(autouse=True)
    def setup(self, procedures: ProcedureCollection):
        self.procedures = procedures
        procedure_name = random_string(6, "procedure_for_tag_tests_")
        procedure = Procedure(
            name=procedure_name,
            arguments=[],
            return_type=ReturnDataType(datatype="VARCHAR"),
            language_config=SQLFunction(),
            body="BEGIN RETURN 'test'; END",
        )
        self.procedure_res = procedures.create(procedure, mode=CreateMode.if_not_exists)
        try:
            yield
        finally:
            self.procedure_res.drop(if_exists=True)

    @property
    def resource_level_name(self) -> str:
        return "PROCEDURE"

    def set_tags(
        self, tags: dict[TagResource, TagValue], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.procedures[self._normalize_resource_name(resource_name) or self.procedure_res.name_with_args].set_tags(
            tags, if_exists
        )

    def unset_tags(
        self, tag_resources: set[TagResource], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.procedures[self._normalize_resource_name(resource_name) or self.procedure_res.name_with_args].unset_tags(
            tag_resources, if_exists
        )

    def get_tags(
        self, with_lineage: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> dict[TagResource, TagValue]:
        return self.procedures[
            self._normalize_resource_name(resource_name) or self.procedure_res.name_with_args
        ].get_tags(with_lineage)

    @staticmethod
    def _normalize_resource_name(name: str | None) -> str | None:
        return f"{name}()" if name and not name.endswith(")") else name
