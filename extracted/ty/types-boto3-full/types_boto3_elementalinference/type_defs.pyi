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
from typing import Any, Union

from .literals import (
    ContextTypeType,
    DataSourceSportType,
    DictionaryLanguageType,
    DictionaryStatusType,
    EventBridgeDeliveryModeType,
    ExtendedAnalysisModeType,
    FeedStatusType,
    FrameSamplingModeType,
    FunctionStatusType,
    OutputStatusType,
    ProfanityFilterModeType,
    ScheduleActionErrorCodeType,
    ScheduleActionStatusType,
    SummaryGenerationModeType,
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
    "BedrockFunctionTargetTypeDef",
    "ChooseOneQuestionOutputTypeDef",
    "ChooseOneQuestionTypeDef",
    "ChooseOneQuestionUnionTypeDef",
    "ClippingConfigTypeDef",
    "ClippingSettingsTypeDef",
    "CompetitorTypeDef",
    "ContextualMetadataConfigTypeDef",
    "ContextualMetadataSettingsTypeDef",
    "CreateDictionaryRequestTypeDef",
    "CreateDictionaryResponseTypeDef",
    "CreateFeedRequestTypeDef",
    "CreateFeedResponseTypeDef",
    "CreateFunctionRequestTypeDef",
    "CreateFunctionResponseTypeDef",
    "CreateOutputTypeDef",
    "CreateQuestionSetRequestTypeDef",
    "CreateQuestionSetResponseTypeDef",
    "CreateQuestionSetVersionRequestTypeDef",
    "CreateQuestionSetVersionResponseTypeDef",
    "CreateScheduleActionRequestTypeDef",
    "CreateScheduleActionResponseTypeDef",
    "CroppingConfigOutputTypeDef",
    "CroppingConfigTypeDef",
    "CroppingConfigUnionTypeDef",
    "CustomQuestionsConfigTypeDef",
    "DataSourceConfigurationTypeDef",
    "DeleteDictionaryRequestTypeDef",
    "DeleteDictionaryResponseTypeDef",
    "DeleteFeedPolicyRequestTypeDef",
    "DeleteFeedRequestTypeDef",
    "DeleteFeedResponseTypeDef",
    "DeleteFunctionRequestTypeDef",
    "DeleteFunctionResponseTypeDef",
    "DeleteQuestionSetRequestTypeDef",
    "DeleteQuestionSetResponseTypeDef",
    "DeleteQuestionSetVersionRequestTypeDef",
    "DeleteScheduleActionRequestTypeDef",
    "DeleteScheduleActionResponseTypeDef",
    "DictionarySummaryTypeDef",
    "DisassociateFeedRequestTypeDef",
    "DisassociateFeedResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ExportDictionaryEntriesRequestTypeDef",
    "ExportDictionaryEntriesResponseTypeDef",
    "FeedAssociationTypeDef",
    "FeedSummaryTypeDef",
    "FixedIntervalTriggerTypeDef",
    "FixedModeScheduleActionStartSettingsOutputTypeDef",
    "FixedModeScheduleActionStartSettingsTypeDef",
    "FixtureSummaryTypeDef",
    "FrameSamplingStrategyTypeDef",
    "FrameSettingsTypeDef",
    "FrameSizeTypeDef",
    "FunctionConfigOutputTypeDef",
    "FunctionConfigTypeDef",
    "FunctionConfigUnionTypeDef",
    "FunctionSummaryTypeDef",
    "FunctionTargetOutputTypeDef",
    "FunctionTargetTypeDef",
    "FunctionTargetUnionTypeDef",
    "GetDictionaryRequestTypeDef",
    "GetDictionaryResponseTypeDef",
    "GetFeedPolicyRequestTypeDef",
    "GetFeedPolicyResponseTypeDef",
    "GetFeedRequestTypeDef",
    "GetFeedRequestWaitTypeDef",
    "GetFeedResponseTypeDef",
    "GetFixtureRequestTypeDef",
    "GetFixtureResponseTypeDef",
    "GetFunctionRequestTypeDef",
    "GetFunctionResponseTypeDef",
    "GetOutputTypeDef",
    "GetQuestionSetRequestTypeDef",
    "GetQuestionSetResponseTypeDef",
    "ListDictionariesRequestPaginateTypeDef",
    "ListDictionariesRequestTypeDef",
    "ListDictionariesResponseTypeDef",
    "ListFeedsRequestPaginateTypeDef",
    "ListFeedsRequestTypeDef",
    "ListFeedsResponseTypeDef",
    "ListFunctionsRequestPaginateTypeDef",
    "ListFunctionsRequestTypeDef",
    "ListFunctionsResponseTypeDef",
    "ListQuestionSetVersionsRequestPaginateTypeDef",
    "ListQuestionSetVersionsRequestTypeDef",
    "ListQuestionSetVersionsResponseTypeDef",
    "ListQuestionSetsRequestPaginateTypeDef",
    "ListQuestionSetsRequestTypeDef",
    "ListQuestionSetsResponseTypeDef",
    "ListScheduleActionsRequestPaginateTypeDef",
    "ListScheduleActionsRequestTypeDef",
    "ListScheduleActionsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "OutputConfigOutputTypeDef",
    "OutputConfigTypeDef",
    "OutputConfigUnionTypeDef",
    "PaginatorConfigTypeDef",
    "PutFeedPolicyRequestTypeDef",
    "QuestionOptionTypeDef",
    "QuestionSetReferenceTypeDef",
    "QuestionSetSummaryTypeDef",
    "QuestionSetVersionSummaryTypeDef",
    "RemoveClippingDataSourceConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "ScheduleActionErrorTypeDef",
    "ScheduleActionOperationTypeDef",
    "ScheduleActionStartConfigurationOutputTypeDef",
    "ScheduleActionStartConfigurationTypeDef",
    "ScheduleActionStartConfigurationUnionTypeDef",
    "ScheduleActionTypeDef",
    "SearchFilterTypeDef",
    "SearchFixturesRequestPaginateTypeDef",
    "SearchFixturesRequestTypeDef",
    "SearchFixturesResponseTypeDef",
    "SubtitlingConfigTypeDef",
    "SubtitlingSettingsTypeDef",
    "TagResourceRequestTypeDef",
    "TemplateGroupOutputTypeDef",
    "TemplateGroupTypeDef",
    "TemplateGroupUnionTypeDef",
    "TimestampTypeDef",
    "TriggerOutputTypeDef",
    "TriggerTypeDef",
    "TriggerUnionTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateClippingDataSourceConfigurationTypeDef",
    "UpdateDictionaryRequestTypeDef",
    "UpdateDictionaryResponseTypeDef",
    "UpdateFeedRequestTypeDef",
    "UpdateFeedResponseTypeDef",
    "UpdateFunctionRequestTypeDef",
    "UpdateFunctionResponseTypeDef",
    "UpdateOutputStatusTypeDef",
    "UpdateOutputTypeDef",
    "UpdateQuestionSetRequestTypeDef",
    "UpdateQuestionSetResponseTypeDef",
    "WaiterConfigTypeDef",
    "YesNoPerOptionQuestionOutputTypeDef",
    "YesNoPerOptionQuestionTypeDef",
    "YesNoPerOptionQuestionUnionTypeDef",
    "YesNoQuestionTypeDef",
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

class BedrockFunctionTargetTypeDef(TypedDict):
    api: Literal["INVOKE_MODEL"]
    model: str

class QuestionOptionTypeDef(TypedDict):
    name: str
    text: str

class DataSourceConfigurationTypeDef(TypedDict):
    fixtureId: str

class ClippingSettingsTypeDef(TypedDict):
    outputName: str

class CompetitorTypeDef(TypedDict):
    name: NotRequired[str]
    isHome: NotRequired[bool]

class ContextualMetadataSettingsTypeDef(TypedDict):
    outputName: str

class CreateDictionaryRequestTypeDef(TypedDict):
    name: str
    language: DictionaryLanguageType
    entries: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class FeedAssociationTypeDef(TypedDict):
    associatedResourceName: str

class YesNoQuestionTypeDef(TypedDict):
    name: str
    question: str

CreateQuestionSetVersionRequestTypeDef = TypedDict(
    "CreateQuestionSetVersionRequestTypeDef",
    {
        "id": str,
        "sha256": NotRequired[str],
        "description": NotRequired[str],
    },
)

class ScheduleActionErrorTypeDef(TypedDict):
    errorCode: ScheduleActionErrorCodeType
    errorMessage: str

class TemplateGroupOutputTypeDef(TypedDict):
    name: str
    templateUris: list[str]

class QuestionSetReferenceTypeDef(TypedDict):
    questionSetId: str
    version: str

DeleteDictionaryRequestTypeDef = TypedDict(
    "DeleteDictionaryRequestTypeDef",
    {
        "id": str,
    },
)
DeleteFeedPolicyRequestTypeDef = TypedDict(
    "DeleteFeedPolicyRequestTypeDef",
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
DeleteFunctionRequestTypeDef = TypedDict(
    "DeleteFunctionRequestTypeDef",
    {
        "id": str,
    },
)
DeleteQuestionSetRequestTypeDef = TypedDict(
    "DeleteQuestionSetRequestTypeDef",
    {
        "id": str,
    },
)
DeleteQuestionSetVersionRequestTypeDef = TypedDict(
    "DeleteQuestionSetVersionRequestTypeDef",
    {
        "id": str,
        "questionSetVersion": str,
    },
)
DeleteScheduleActionRequestTypeDef = TypedDict(
    "DeleteScheduleActionRequestTypeDef",
    {
        "id": str,
        "actionName": str,
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

class FixedIntervalTriggerTypeDef(TypedDict):
    intervalSeconds: int

class FixedModeScheduleActionStartSettingsOutputTypeDef(TypedDict):
    scheduledAt: datetime

TimestampTypeDef = Union[datetime, str]

class FrameSamplingStrategyTypeDef(TypedDict):
    mode: FrameSamplingModeType
    count: NotRequired[int]

class FrameSizeTypeDef(TypedDict):
    widthPixels: int
    heightPixels: int

class SubtitlingSettingsTypeDef(TypedDict):
    outputName: str

GetDictionaryRequestTypeDef = TypedDict(
    "GetDictionaryRequestTypeDef",
    {
        "id": str,
    },
)
GetFeedPolicyRequestTypeDef = TypedDict(
    "GetFeedPolicyRequestTypeDef",
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

class GetFixtureRequestTypeDef(TypedDict):
    fixtureId: str

GetFunctionRequestTypeDef = TypedDict(
    "GetFunctionRequestTypeDef",
    {
        "id": str,
    },
)
GetQuestionSetRequestTypeDef = TypedDict(
    "GetQuestionSetRequestTypeDef",
    {
        "id": str,
        "questionSetVersion": NotRequired[str],
    },
)

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

class ListFunctionsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

ListQuestionSetVersionsRequestTypeDef = TypedDict(
    "ListQuestionSetVersionsRequestTypeDef",
    {
        "id": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

class QuestionSetVersionSummaryTypeDef(TypedDict):
    version: str
    sha256: str
    lastModifiedAt: datetime
    description: NotRequired[str]

class ListQuestionSetsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

QuestionSetSummaryTypeDef = TypedDict(
    "QuestionSetSummaryTypeDef",
    {
        "arn": str,
        "id": str,
        "name": str,
        "latestVersion": NotRequired[str],
    },
)
ListScheduleActionsRequestTypeDef = TypedDict(
    "ListScheduleActionsRequestTypeDef",
    {
        "id": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str

PutFeedPolicyRequestTypeDef = TypedDict(
    "PutFeedPolicyRequestTypeDef",
    {
        "id": str,
        "policy": str,
    },
)

class RemoveClippingDataSourceConfigurationTypeDef(TypedDict):
    outputName: str

class UpdateOutputStatusTypeDef(TypedDict):
    outputName: str
    status: OutputStatusType

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
DeleteFunctionResponseTypeDef = TypedDict(
    "DeleteFunctionResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "status": FunctionStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteQuestionSetResponseTypeDef = TypedDict(
    "DeleteQuestionSetResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class DeleteScheduleActionResponseTypeDef(TypedDict):
    actionName: str
    ResponseMetadata: ResponseMetadataTypeDef

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

class GetFeedPolicyResponseTypeDef(TypedDict):
    policy: str
    ResponseMetadata: ResponseMetadataTypeDef

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

class FunctionTargetOutputTypeDef(TypedDict):
    bedrock: NotRequired[BedrockFunctionTargetTypeDef]
    passthrough: NotRequired[dict[str, Any]]

class FunctionTargetTypeDef(TypedDict):
    bedrock: NotRequired[BedrockFunctionTargetTypeDef]
    passthrough: NotRequired[Mapping[str, Any]]

class ChooseOneQuestionOutputTypeDef(TypedDict):
    name: str
    question: str
    options: list[QuestionOptionTypeDef]

class ChooseOneQuestionTypeDef(TypedDict):
    name: str
    question: str
    options: Sequence[QuestionOptionTypeDef]

class YesNoPerOptionQuestionOutputTypeDef(TypedDict):
    name: str
    question: str
    options: list[QuestionOptionTypeDef]

class YesNoPerOptionQuestionTypeDef(TypedDict):
    name: str
    question: str
    options: Sequence[QuestionOptionTypeDef]

class ClippingConfigTypeDef(TypedDict):
    callbackMetadata: NotRequired[str]
    dataSourceConfiguration: NotRequired[DataSourceConfigurationTypeDef]

class UpdateClippingDataSourceConfigurationTypeDef(TypedDict):
    outputName: str
    dataSourceConfiguration: DataSourceConfigurationTypeDef

class FixtureSummaryTypeDef(TypedDict):
    fixtureId: str
    name: str
    status: str
    competitors: list[CompetitorTypeDef]
    fixtureGroup: NotRequired[str]
    scheduledStart: NotRequired[datetime]

class GetFixtureResponseTypeDef(TypedDict):
    fixtureId: str
    name: str
    fixtureGroup: str
    scheduledStart: datetime
    status: str
    competitors: list[CompetitorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

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

class CustomQuestionsConfigTypeDef(TypedDict):
    shot: NotRequired[QuestionSetReferenceTypeDef]
    scene: NotRequired[QuestionSetReferenceTypeDef]

class ListDictionariesResponseTypeDef(TypedDict):
    dictionaries: list[DictionarySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class TriggerOutputTypeDef(TypedDict):
    fixedInterval: NotRequired[FixedIntervalTriggerTypeDef]
    perShot: NotRequired[dict[str, Any]]
    perScene: NotRequired[dict[str, Any]]
    perClip: NotRequired[dict[str, Any]]

class TriggerTypeDef(TypedDict):
    fixedInterval: NotRequired[FixedIntervalTriggerTypeDef]
    perShot: NotRequired[Mapping[str, Any]]
    perScene: NotRequired[Mapping[str, Any]]
    perClip: NotRequired[Mapping[str, Any]]

class ScheduleActionStartConfigurationOutputTypeDef(TypedDict):
    fixedModeScheduleActionStartSettings: NotRequired[
        FixedModeScheduleActionStartSettingsOutputTypeDef
    ]

class FixedModeScheduleActionStartSettingsTypeDef(TypedDict):
    scheduledAt: TimestampTypeDef

class FrameSettingsTypeDef(TypedDict):
    frameSampling: FrameSamplingStrategyTypeDef
    frameSize: NotRequired[FrameSizeTypeDef]

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

class ListFunctionsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListQuestionSetVersionsRequestPaginateTypeDef = TypedDict(
    "ListQuestionSetVersionsRequestPaginateTypeDef",
    {
        "id": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListQuestionSetsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListScheduleActionsRequestPaginateTypeDef = TypedDict(
    "ListScheduleActionsRequestPaginateTypeDef",
    {
        "id": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListQuestionSetVersionsResponseTypeDef(TypedDict):
    versions: list[QuestionSetVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListQuestionSetsResponseTypeDef(TypedDict):
    questionSets: list[QuestionSetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

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
CreateFunctionResponseTypeDef = TypedDict(
    "CreateFunctionResponseTypeDef",
    {
        "name": str,
        "target": FunctionTargetOutputTypeDef,
        "requestExpression": str,
        "responseExpression": str,
        "description": str,
        "eventBridgeDelivery": EventBridgeDeliveryModeType,
        "arn": str,
        "id": str,
        "status": FunctionStatusType,
        "references": list[str],
        "contextTypes": list[ContextTypeType],
        "tags": dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
FunctionSummaryTypeDef = TypedDict(
    "FunctionSummaryTypeDef",
    {
        "arn": str,
        "id": str,
        "name": str,
        "status": FunctionStatusType,
        "description": NotRequired[str],
        "target": NotRequired[FunctionTargetOutputTypeDef],
        "contextTypes": NotRequired[list[ContextTypeType]],
    },
)
GetFunctionResponseTypeDef = TypedDict(
    "GetFunctionResponseTypeDef",
    {
        "name": str,
        "target": FunctionTargetOutputTypeDef,
        "requestExpression": str,
        "responseExpression": str,
        "description": str,
        "eventBridgeDelivery": EventBridgeDeliveryModeType,
        "arn": str,
        "id": str,
        "status": FunctionStatusType,
        "references": list[str],
        "contextTypes": list[ContextTypeType],
        "tags": dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateFunctionResponseTypeDef = TypedDict(
    "UpdateFunctionResponseTypeDef",
    {
        "name": str,
        "target": FunctionTargetOutputTypeDef,
        "requestExpression": str,
        "responseExpression": str,
        "description": str,
        "eventBridgeDelivery": EventBridgeDeliveryModeType,
        "arn": str,
        "id": str,
        "status": FunctionStatusType,
        "references": list[str],
        "contextTypes": list[ContextTypeType],
        "tags": dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
FunctionTargetUnionTypeDef = Union[FunctionTargetTypeDef, FunctionTargetOutputTypeDef]
ChooseOneQuestionUnionTypeDef = Union[ChooseOneQuestionTypeDef, ChooseOneQuestionOutputTypeDef]
CreateQuestionSetResponseTypeDef = TypedDict(
    "CreateQuestionSetResponseTypeDef",
    {
        "yesNo": list[YesNoQuestionTypeDef],
        "yesNoPerOption": list[YesNoPerOptionQuestionOutputTypeDef],
        "chooseOne": list[ChooseOneQuestionOutputTypeDef],
        "arn": str,
        "id": str,
        "name": str,
        "version": str,
        "description": str,
        "latestVersion": str,
        "sha256": str,
        "references": list[str],
        "tags": dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateQuestionSetVersionResponseTypeDef = TypedDict(
    "CreateQuestionSetVersionResponseTypeDef",
    {
        "yesNo": list[YesNoQuestionTypeDef],
        "yesNoPerOption": list[YesNoPerOptionQuestionOutputTypeDef],
        "chooseOne": list[ChooseOneQuestionOutputTypeDef],
        "arn": str,
        "id": str,
        "name": str,
        "version": str,
        "description": str,
        "latestVersion": str,
        "sha256": str,
        "references": list[str],
        "tags": dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetQuestionSetResponseTypeDef = TypedDict(
    "GetQuestionSetResponseTypeDef",
    {
        "yesNo": list[YesNoQuestionTypeDef],
        "yesNoPerOption": list[YesNoPerOptionQuestionOutputTypeDef],
        "chooseOne": list[ChooseOneQuestionOutputTypeDef],
        "arn": str,
        "id": str,
        "name": str,
        "version": str,
        "description": str,
        "latestVersion": str,
        "sha256": str,
        "references": list[str],
        "tags": dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateQuestionSetResponseTypeDef = TypedDict(
    "UpdateQuestionSetResponseTypeDef",
    {
        "yesNo": list[YesNoQuestionTypeDef],
        "yesNoPerOption": list[YesNoPerOptionQuestionOutputTypeDef],
        "chooseOne": list[ChooseOneQuestionOutputTypeDef],
        "arn": str,
        "id": str,
        "name": str,
        "version": str,
        "description": str,
        "latestVersion": str,
        "sha256": str,
        "references": list[str],
        "tags": dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
YesNoPerOptionQuestionUnionTypeDef = Union[
    YesNoPerOptionQuestionTypeDef, YesNoPerOptionQuestionOutputTypeDef
]

class ScheduleActionOperationTypeDef(TypedDict):
    updateOutputStatus: NotRequired[UpdateOutputStatusTypeDef]
    updateClippingDataSourceConfiguration: NotRequired[UpdateClippingDataSourceConfigurationTypeDef]
    removeClippingDataSourceConfiguration: NotRequired[RemoveClippingDataSourceConfigurationTypeDef]

class SearchFixturesResponseTypeDef(TypedDict):
    fixtures: list[FixtureSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListFeedsResponseTypeDef(TypedDict):
    feeds: list[FeedSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ContextualMetadataConfigTypeDef(TypedDict):
    summaryGeneration: NotRequired[SummaryGenerationModeType]
    extendedAnalysis: NotRequired[ExtendedAnalysisModeType]
    customQuestions: NotRequired[CustomQuestionsConfigTypeDef]

TriggerUnionTypeDef = Union[TriggerTypeDef, TriggerOutputTypeDef]

class ScheduleActionStartConfigurationTypeDef(TypedDict):
    fixedModeScheduleActionStartSettings: NotRequired[FixedModeScheduleActionStartSettingsTypeDef]

class FunctionConfigOutputTypeDef(TypedDict):
    functionArn: str
    trigger: TriggerOutputTypeDef
    frameSettings: NotRequired[FrameSettingsTypeDef]
    subtitlingSettings: NotRequired[SubtitlingSettingsTypeDef]
    contextualMetadataSettings: NotRequired[ContextualMetadataSettingsTypeDef]
    clippingSettings: NotRequired[ClippingSettingsTypeDef]

class CroppingConfigTypeDef(TypedDict):
    templateGroups: NotRequired[Sequence[TemplateGroupUnionTypeDef]]

class ListFunctionsResponseTypeDef(TypedDict):
    functions: list[FunctionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateFunctionRequestTypeDef(TypedDict):
    name: str
    target: FunctionTargetUnionTypeDef
    requestExpression: str
    responseExpression: NotRequired[str]
    description: NotRequired[str]
    eventBridgeDelivery: NotRequired[EventBridgeDeliveryModeType]
    tags: NotRequired[Mapping[str, str]]

UpdateFunctionRequestTypeDef = TypedDict(
    "UpdateFunctionRequestTypeDef",
    {
        "id": str,
        "name": NotRequired[str],
        "target": NotRequired[FunctionTargetUnionTypeDef],
        "requestExpression": NotRequired[str],
        "responseExpression": NotRequired[str],
        "description": NotRequired[str],
        "eventBridgeDelivery": NotRequired[EventBridgeDeliveryModeType],
    },
)

class CreateQuestionSetRequestTypeDef(TypedDict):
    name: str
    yesNo: NotRequired[Sequence[YesNoQuestionTypeDef]]
    yesNoPerOption: NotRequired[Sequence[YesNoPerOptionQuestionUnionTypeDef]]
    chooseOne: NotRequired[Sequence[ChooseOneQuestionUnionTypeDef]]
    tags: NotRequired[Mapping[str, str]]

UpdateQuestionSetRequestTypeDef = TypedDict(
    "UpdateQuestionSetRequestTypeDef",
    {
        "id": str,
        "yesNo": NotRequired[Sequence[YesNoQuestionTypeDef]],
        "yesNoPerOption": NotRequired[Sequence[YesNoPerOptionQuestionUnionTypeDef]],
        "chooseOne": NotRequired[Sequence[ChooseOneQuestionUnionTypeDef]],
        "name": NotRequired[str],
    },
)

class CreateScheduleActionResponseTypeDef(TypedDict):
    actionName: str
    startConfiguration: ScheduleActionStartConfigurationOutputTypeDef
    operations: list[ScheduleActionOperationTypeDef]
    status: ScheduleActionStatusType
    error: ScheduleActionErrorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ScheduleActionTypeDef(TypedDict):
    actionName: str
    startConfiguration: ScheduleActionStartConfigurationOutputTypeDef
    operations: list[ScheduleActionOperationTypeDef]
    status: ScheduleActionStatusType
    error: NotRequired[ScheduleActionErrorTypeDef]

class FunctionConfigTypeDef(TypedDict):
    functionArn: str
    trigger: TriggerUnionTypeDef
    frameSettings: NotRequired[FrameSettingsTypeDef]
    subtitlingSettings: NotRequired[SubtitlingSettingsTypeDef]
    contextualMetadataSettings: NotRequired[ContextualMetadataSettingsTypeDef]
    clippingSettings: NotRequired[ClippingSettingsTypeDef]

ScheduleActionStartConfigurationUnionTypeDef = Union[
    ScheduleActionStartConfigurationTypeDef, ScheduleActionStartConfigurationOutputTypeDef
]

class OutputConfigOutputTypeDef(TypedDict):
    cropping: NotRequired[CroppingConfigOutputTypeDef]
    clipping: NotRequired[ClippingConfigTypeDef]
    subtitling: NotRequired[SubtitlingConfigTypeDef]
    contextualMetadata: NotRequired[ContextualMetadataConfigTypeDef]
    function: NotRequired[FunctionConfigOutputTypeDef]

CroppingConfigUnionTypeDef = Union[CroppingConfigTypeDef, CroppingConfigOutputTypeDef]

class ListScheduleActionsResponseTypeDef(TypedDict):
    scheduleActions: list[ScheduleActionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

FunctionConfigUnionTypeDef = Union[FunctionConfigTypeDef, FunctionConfigOutputTypeDef]
CreateScheduleActionRequestTypeDef = TypedDict(
    "CreateScheduleActionRequestTypeDef",
    {
        "id": str,
        "actionName": str,
        "startConfiguration": ScheduleActionStartConfigurationUnionTypeDef,
        "operations": Sequence[ScheduleActionOperationTypeDef],
    },
)

class GetOutputTypeDef(TypedDict):
    name: str
    outputConfig: OutputConfigOutputTypeDef
    status: OutputStatusType
    description: NotRequired[str]
    fromAssociation: NotRequired[bool]

class OutputConfigTypeDef(TypedDict):
    cropping: NotRequired[CroppingConfigUnionTypeDef]
    clipping: NotRequired[ClippingConfigTypeDef]
    subtitling: NotRequired[SubtitlingConfigTypeDef]
    contextualMetadata: NotRequired[ContextualMetadataConfigTypeDef]
    function: NotRequired[FunctionConfigUnionTypeDef]

CreateFeedResponseTypeDef = TypedDict(
    "CreateFeedResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "id": str,
        "dataEndpoints": list[str],
        "outputs": list[GetOutputTypeDef],
        "accessRoleArn": str,
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
        "accessRoleArn": str,
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
        "accessRoleArn": str,
        "status": FeedStatusType,
        "association": FeedAssociationTypeDef,
        "tags": dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
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
