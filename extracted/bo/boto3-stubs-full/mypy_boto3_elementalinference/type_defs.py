"""
Type annotations for elementalinference service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_elementalinference.type_defs import AspectRatioTypeDef

    data: AspectRatioTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from typing import Any, Union

from .literals import (
    DictionaryLanguageType,
    DictionaryStatusType,
    FeedStatusType,
    OutputStatusType,
    ProfanityFilterModeType,
    TranscriptionLanguageType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AspectRatioTypeDef",
    "AssociateFeedRequestTypeDef",
    "AssociateFeedResponseTypeDef",
    "ClippingConfigTypeDef",
    "CreateDictionaryRequestTypeDef",
    "CreateDictionaryResponseTypeDef",
    "CreateFeedRequestTypeDef",
    "CreateFeedResponseTypeDef",
    "CreateOutputTypeDef",
    "DeleteDictionaryRequestTypeDef",
    "DeleteDictionaryResponseTypeDef",
    "DeleteFeedRequestTypeDef",
    "DeleteFeedResponseTypeDef",
    "DictionarySummaryTypeDef",
    "DisassociateFeedRequestTypeDef",
    "DisassociateFeedResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ExportDictionaryEntriesRequestTypeDef",
    "ExportDictionaryEntriesResponseTypeDef",
    "FeedAssociationTypeDef",
    "FeedSummaryTypeDef",
    "GetDictionaryRequestTypeDef",
    "GetDictionaryResponseTypeDef",
    "GetFeedRequestTypeDef",
    "GetFeedRequestWaitTypeDef",
    "GetFeedResponseTypeDef",
    "GetOutputTypeDef",
    "ListDictionariesRequestPaginateTypeDef",
    "ListDictionariesRequestTypeDef",
    "ListDictionariesResponseTypeDef",
    "ListFeedsRequestPaginateTypeDef",
    "ListFeedsRequestTypeDef",
    "ListFeedsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "OutputConfigOutputTypeDef",
    "OutputConfigTypeDef",
    "OutputConfigUnionTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "SubtitlingConfigTypeDef",
    "TagResourceRequestTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateDictionaryRequestTypeDef",
    "UpdateDictionaryResponseTypeDef",
    "UpdateFeedRequestTypeDef",
    "UpdateFeedResponseTypeDef",
    "UpdateOutputTypeDef",
    "WaiterConfigTypeDef",
)


class AspectRatioTypeDef(TypedDict):
    width: int
    height: int


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class ClippingConfigTypeDef(TypedDict):
    callbackMetadata: NotRequired[str]


class CreateDictionaryRequestTypeDef(TypedDict):
    name: str
    language: DictionaryLanguageType
    entries: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class FeedAssociationTypeDef(TypedDict):
    associatedResourceName: str


DeleteDictionaryRequestTypeDef = TypedDict(
    "DeleteDictionaryRequestTypeDef",
    {
        "id": str,
    },
)
DeleteFeedRequestTypeDef = TypedDict(
    "DeleteFeedRequestTypeDef",
    {
        "id": str,
    },
)
DictionarySummaryTypeDef = TypedDict(
    "DictionarySummaryTypeDef",
    {
        "arn": str,
        "id": str,
        "name": str,
        "language": DictionaryLanguageType,
        "status": DictionaryStatusType,
    },
)
DisassociateFeedRequestTypeDef = TypedDict(
    "DisassociateFeedRequestTypeDef",
    {
        "id": str,
        "associatedResourceName": str,
        "dryRun": NotRequired[bool],
    },
)
ExportDictionaryEntriesRequestTypeDef = TypedDict(
    "ExportDictionaryEntriesRequestTypeDef",
    {
        "id": str,
    },
)
GetDictionaryRequestTypeDef = TypedDict(
    "GetDictionaryRequestTypeDef",
    {
        "id": str,
    },
)
GetFeedRequestTypeDef = TypedDict(
    "GetFeedRequestTypeDef",
    {
        "id": str,
    },
)


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListDictionariesRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListFeedsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str


class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


UpdateDictionaryRequestTypeDef = TypedDict(
    "UpdateDictionaryRequestTypeDef",
    {
        "id": str,
        "name": NotRequired[str],
        "language": NotRequired[DictionaryLanguageType],
        "entries": NotRequired[str],
    },
)


class SubtitlingConfigTypeDef(TypedDict):
    language: TranscriptionLanguageType
    aspectRatio: NotRequired[AspectRatioTypeDef]
    dictionary: NotRequired[str]
    profanityFilter: NotRequired[ProfanityFilterModeType]


AssociateFeedResponseTypeDef = TypedDict(
    "AssociateFeedResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateDictionaryResponseTypeDef = TypedDict(
    "CreateDictionaryResponseTypeDef",
    {
        "name": str,
        "arn": str,
        "id": str,
        "language": DictionaryLanguageType,
        "status": DictionaryStatusType,
        "references": list[str],
        "tags": dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteDictionaryResponseTypeDef = TypedDict(
    "DeleteDictionaryResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "status": DictionaryStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteFeedResponseTypeDef = TypedDict(
    "DeleteFeedResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "status": FeedStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DisassociateFeedResponseTypeDef = TypedDict(
    "DisassociateFeedResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class ExportDictionaryEntriesResponseTypeDef(TypedDict):
    entries: str
    ResponseMetadata: ResponseMetadataTypeDef


GetDictionaryResponseTypeDef = TypedDict(
    "GetDictionaryResponseTypeDef",
    {
        "name": str,
        "arn": str,
        "id": str,
        "language": DictionaryLanguageType,
        "status": DictionaryStatusType,
        "references": list[str],
        "tags": dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


UpdateDictionaryResponseTypeDef = TypedDict(
    "UpdateDictionaryResponseTypeDef",
    {
        "name": str,
        "arn": str,
        "id": str,
        "language": DictionaryLanguageType,
        "status": DictionaryStatusType,
        "references": list[str],
        "tags": dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
FeedSummaryTypeDef = TypedDict(
    "FeedSummaryTypeDef",
    {
        "arn": str,
        "id": str,
        "name": str,
        "status": FeedStatusType,
        "association": NotRequired[FeedAssociationTypeDef],
    },
)


class ListDictionariesResponseTypeDef(TypedDict):
    dictionaries: list[DictionarySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


GetFeedRequestWaitTypeDef = TypedDict(
    "GetFeedRequestWaitTypeDef",
    {
        "id": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)


class ListDictionariesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFeedsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class OutputConfigOutputTypeDef(TypedDict):
    cropping: NotRequired[dict[str, Any]]
    clipping: NotRequired[ClippingConfigTypeDef]
    subtitling: NotRequired[SubtitlingConfigTypeDef]


class OutputConfigTypeDef(TypedDict):
    cropping: NotRequired[Mapping[str, Any]]
    clipping: NotRequired[ClippingConfigTypeDef]
    subtitling: NotRequired[SubtitlingConfigTypeDef]


class ListFeedsResponseTypeDef(TypedDict):
    feeds: list[FeedSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetOutputTypeDef(TypedDict):
    name: str
    outputConfig: OutputConfigOutputTypeDef
    status: OutputStatusType
    description: NotRequired[str]
    fromAssociation: NotRequired[bool]


OutputConfigUnionTypeDef = Union[OutputConfigTypeDef, OutputConfigOutputTypeDef]
CreateFeedResponseTypeDef = TypedDict(
    "CreateFeedResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "id": str,
        "dataEndpoints": list[str],
        "outputs": list[GetOutputTypeDef],
        "status": FeedStatusType,
        "association": FeedAssociationTypeDef,
        "tags": dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetFeedResponseTypeDef = TypedDict(
    "GetFeedResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "id": str,
        "dataEndpoints": list[str],
        "outputs": list[GetOutputTypeDef],
        "status": FeedStatusType,
        "association": FeedAssociationTypeDef,
        "tags": dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateFeedResponseTypeDef = TypedDict(
    "UpdateFeedResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "id": str,
        "dataEndpoints": list[str],
        "outputs": list[GetOutputTypeDef],
        "status": FeedStatusType,
        "association": FeedAssociationTypeDef,
        "tags": dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class CreateOutputTypeDef(TypedDict):
    name: str
    outputConfig: OutputConfigUnionTypeDef
    status: OutputStatusType
    description: NotRequired[str]


class UpdateOutputTypeDef(TypedDict):
    name: str
    outputConfig: OutputConfigUnionTypeDef
    status: OutputStatusType
    description: NotRequired[str]
    fromAssociation: NotRequired[bool]


AssociateFeedRequestTypeDef = TypedDict(
    "AssociateFeedRequestTypeDef",
    {
        "id": str,
        "associatedResourceName": str,
        "outputs": Sequence[CreateOutputTypeDef],
        "dryRun": NotRequired[bool],
    },
)


class CreateFeedRequestTypeDef(TypedDict):
    name: str
    outputs: Sequence[CreateOutputTypeDef]
    tags: NotRequired[Mapping[str, str]]


UpdateFeedRequestTypeDef = TypedDict(
    "UpdateFeedRequestTypeDef",
    {
        "name": str,
        "id": str,
        "outputs": Sequence[UpdateOutputTypeDef],
    },
)
