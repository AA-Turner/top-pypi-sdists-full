# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, TypeAlias, TypedDict

from ..._types import SequenceNotStr
from ..shared_params.chunk_extra_info_schema import ChunkExtraInfoSchema
from ..shared_params.string_extra_info_schema import StringExtraInfoSchema

__all__ = ["ArtifactSchemaGenerationParam", "ExpectedExtraInfo"]

ExpectedExtraInfo: TypeAlias = Union[ChunkExtraInfoSchema, StringExtraInfoSchema]


class ArtifactSchemaGenerationParam(TypedDict, total=False):
    artifact_ids_filter: Required[SequenceNotStr[str]]

    input: Required[str]

    expected_extra_info: ExpectedExtraInfo

    expected_output: str
