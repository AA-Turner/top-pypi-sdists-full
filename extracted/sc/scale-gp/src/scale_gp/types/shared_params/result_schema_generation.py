# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, TypeAlias, TypedDict

from .chunk_extra_info_schema import ChunkExtraInfoSchema
from .string_extra_info_schema import StringExtraInfoSchema

__all__ = ["ResultSchemaGeneration", "GenerationExtraInfo"]

GenerationExtraInfo: TypeAlias = Union[ChunkExtraInfoSchema, StringExtraInfoSchema]


class ResultSchemaGeneration(TypedDict, total=False):
    generation_output: Required[str]

    generation_extra_info: GenerationExtraInfo
