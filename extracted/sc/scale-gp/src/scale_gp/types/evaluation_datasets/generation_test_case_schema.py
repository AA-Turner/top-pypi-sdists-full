# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from ..shared.chunk_extra_info_schema import ChunkExtraInfoSchema
from ..shared.string_extra_info_schema import StringExtraInfoSchema

__all__ = ["GenerationTestCaseSchema", "ExpectedExtraInfo"]

ExpectedExtraInfo: TypeAlias = Annotated[
    Union[ChunkExtraInfoSchema, StringExtraInfoSchema], PropertyInfo(discriminator="schema_type")
]


class GenerationTestCaseSchema(BaseModel):
    input: str

    expected_extra_info: Optional[ExpectedExtraInfo] = None

    expected_output: Optional[str] = None
