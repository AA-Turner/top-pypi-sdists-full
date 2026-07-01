# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .chunk_extra_info_schema import ChunkExtraInfoSchema
from .string_extra_info_schema import StringExtraInfoSchema

__all__ = ["ResultSchemaGeneration", "GenerationExtraInfo"]

GenerationExtraInfo: TypeAlias = Annotated[
    Union[ChunkExtraInfoSchema, StringExtraInfoSchema], PropertyInfo(discriminator="schema_type")
]


class ResultSchemaGeneration(BaseModel):
    generation_output: str

    generation_extra_info: Optional[GenerationExtraInfo] = None
