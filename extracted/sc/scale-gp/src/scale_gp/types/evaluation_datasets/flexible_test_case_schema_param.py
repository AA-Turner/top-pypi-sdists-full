# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .flexible_message_param import FlexibleMessageParam
from ..shared_params.flexible_chunk import FlexibleChunk
from ..shared_params.chunk_extra_info_schema import ChunkExtraInfoSchema
from ..shared_params.string_extra_info_schema import StringExtraInfoSchema

__all__ = [
    "FlexibleTestCaseSchemaParam",
    "InputAdditionalObjectInputAdditionalObjectItem",
    "InputAdditionalObjectInputAdditionalObjectItemExternalFile",
    "InputAdditionalObjectInputAdditionalObjectItemInternalFile",
    "ExpectedExtraInfo",
    "ExpectedOutputAdditionalObjectExpectedOutputAdditionalObjectItem",
    "ExpectedOutputAdditionalObjectExpectedOutputAdditionalObjectItemExternalFile",
    "ExpectedOutputAdditionalObjectExpectedOutputAdditionalObjectItemInternalFile",
]


class InputAdditionalObjectInputAdditionalObjectItemExternalFile(TypedDict, total=False):
    file_type: Required[Literal["image", "pdf"]]

    uri: Required[str]


class InputAdditionalObjectInputAdditionalObjectItemInternalFile(TypedDict, total=False):
    file_id: Required[str]

    file_type: Required[Literal["image", "pdf"]]


InputAdditionalObjectInputAdditionalObjectItem: TypeAlias = Union[
    str,
    float,
    Iterable[FlexibleChunk],
    Iterable[FlexibleMessageParam],
    Iterable[object],
    Dict[str, object],
    InputAdditionalObjectInputAdditionalObjectItemExternalFile,
    InputAdditionalObjectInputAdditionalObjectItemInternalFile,
]

ExpectedExtraInfo: TypeAlias = Union[ChunkExtraInfoSchema, StringExtraInfoSchema]


class ExpectedOutputAdditionalObjectExpectedOutputAdditionalObjectItemExternalFile(TypedDict, total=False):
    file_type: Required[Literal["image", "pdf"]]

    uri: Required[str]


class ExpectedOutputAdditionalObjectExpectedOutputAdditionalObjectItemInternalFile(TypedDict, total=False):
    file_id: Required[str]

    file_type: Required[Literal["image", "pdf"]]


ExpectedOutputAdditionalObjectExpectedOutputAdditionalObjectItem: TypeAlias = Union[
    str,
    float,
    Iterable[FlexibleChunk],
    Iterable[FlexibleMessageParam],
    Iterable[object],
    Dict[str, object],
    ExpectedOutputAdditionalObjectExpectedOutputAdditionalObjectItemExternalFile,
    ExpectedOutputAdditionalObjectExpectedOutputAdditionalObjectItemInternalFile,
]


class FlexibleTestCaseSchemaParam(TypedDict, total=False):
    input: Required[Union[str, Dict[str, Optional[InputAdditionalObjectInputAdditionalObjectItem]]]]

    expected_extra_info: ExpectedExtraInfo

    expected_output: Union[str, Dict[str, Optional[ExpectedOutputAdditionalObjectExpectedOutputAdditionalObjectItem]]]
