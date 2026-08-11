"""
Type annotations for elementalinference service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_elementalinference.type_defs import AspectRatioTypeDef

    data: AspectRatioTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    DataSourceSportType,
    DictionaryLanguageType,
    DictionaryStatusType,
    FeedStatusType,
    OutputStatusType,
    ProfanityFilterModeType,
    TranscriptionLanguageType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AspectRatioTypeDef",
    "AssociateFeedRequestTypeDef",
    "AssociateFeedResponseTypeDef",
    "ClippingConfigTypeDef",
    "CompetitorTypeDef",
    "CreateDictionaryRequestTypeDef",
    "CreateDictionaryResponseTypeDef",
    "CreateFeedRequestTypeDef",
    "CreateFeedResponseTypeDef",
    "CreateOutputTypeDef",
    "CroppingConfigOutputTypeDef",
    "CroppingConfigTypeDef",
    "CroppingConfigUnionTypeDef",
    "DataSourceConfigurationTypeDef",
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
    "FixtureSummaryTypeDef",
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
    "SearchFilterTypeDef",
    "SearchFixturesRequestPaginateTypeDef",
    "SearchFixturesRequestTypeDef",
    "SearchFixturesResponseTypeDef",
    "SubtitlingConfigTypeDef",
    "TagResourceRequestTypeDef",
    "TemplateGroupOutputTypeDef",
    "TemplateGroupTypeDef",
    "TemplateGroupUnionTypeDef",
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


class DataSourceConfigurationTypeDef(TypedDict):
    fixtureId: str


class CompetitorTypeDef(TypedDict):
    name: NotRequired[str]
    isHome: NotRequired[bool]


class CreateDictionaryRequestTypeDef(TypedDict):
    name: str
    language: DictionaryLanguageType
    entries: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class FeedAssociationTypeDef(TypedDict):
    associatedResourceName: str


class TemplateGroupOutputTypeDef(TypedDict):
    name: str
    templateUris: list[str]


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


class SearchFilterTypeDef(TypedDict):
    name: Literal["COMPETITOR"]
    values: Sequence[str]


class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class TemplateGroupTypeDef(TypedDict):
    name: str
    templateUris: Sequence[str]


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


class ClippingConfigTypeDef(TypedDict):
    callbackMetadata: NotRequired[str]
    dataSourceConfiguration: NotRequired[DataSourceConfigurationTypeDef]


class FixtureSummaryTypeDef(TypedDict):
    fixtureId: str
    name: str
    status: str
    competitors: list[CompetitorTypeDef]
    fixtureGroup: NotRequired[str]
    scheduledStart: NotRequired[datetime]


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


class CroppingConfigOutputTypeDef(TypedDict):
    templateGroups: NotRequired[list[TemplateGroupOutputTypeDef]]


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


class SearchFixturesRequestPaginateTypeDef(TypedDict):
    sport: DataSourceSportType
    startDate: str
    endDate: NotRequired[str]
    filters: NotRequired[Sequence[SearchFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchFixturesRequestTypeDef(TypedDict):
    sport: DataSourceSportType
    startDate: str
    endDate: NotRequired[str]
    filters: NotRequired[Sequence[SearchFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


TemplateGroupUnionTypeDef = Union[TemplateGroupTypeDef, TemplateGroupOutputTypeDef]


class SearchFixturesResponseTypeDef(TypedDict):
    fixtures: list[FixtureSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListFeedsResponseTypeDef(TypedDict):
    feeds: list[FeedSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class OutputConfigOutputTypeDef(TypedDict):
    cropping: NotRequired[CroppingConfigOutputTypeDef]
    clipping: NotRequired[ClippingConfigTypeDef]
    subtitling: NotRequired[SubtitlingConfigTypeDef]


class CroppingConfigTypeDef(TypedDict):
    templateGroups: NotRequired[Sequence[TemplateGroupUnionTypeDef]]


class GetOutputTypeDef(TypedDict):
    name: str
    outputConfig: OutputConfigOutputTypeDef
    status: OutputStatusType
    description: NotRequired[str]
    fromAssociation: NotRequired[bool]


CroppingConfigUnionTypeDef = Union[CroppingConfigTypeDef, CroppingConfigOutputTypeDef]
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


class OutputConfigTypeDef(TypedDict):
    cropping: NotRequired[CroppingConfigUnionTypeDef]
    clipping: NotRequired[ClippingConfigTypeDef]
    subtitling: NotRequired[SubtitlingConfigTypeDef]


OutputConfigUnionTypeDef = Union[OutputConfigTypeDef, OutputConfigOutputTypeDef]


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
    accessRoleArn: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


UpdateFeedRequestTypeDef = TypedDict(
    "UpdateFeedRequestTypeDef",
    {
        "name": str,
        "id": str,
        "outputs": Sequence[UpdateOutputTypeDef],
        "accessRoleArn": NotRequired[str],
    },
)
