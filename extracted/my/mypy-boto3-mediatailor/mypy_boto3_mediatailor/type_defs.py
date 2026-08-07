"""
Type annotations for mediatailor service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_mediatailor.type_defs import SecretsManagerAccessTokenConfigurationTypeDef

    data: SecretsManagerAccessTokenConfigurationTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    AccessTypeType,
    AdMarkupTypeType,
    AdsInteractionExcludeEventTypeType,
    AdsInteractionPublishOptInEventTypeType,
    AlertCategoryType,
    ChannelStateType,
    CompressionMethodType,
    EventNameType,
    FillPolicyType,
    FunctionTypeType,
    InsertionModeType,
    ListPrefetchScheduleTypeType,
    LoggingStrategyType,
    ManifestServiceExcludeEventTypeType,
    ManifestServicePublishOptInEventTypeType,
    MessageTypeType,
    MethodType,
    MethodTypeType,
    ModeType,
    OriginManifestTypeType,
    PlaybackModeType,
    PrefetchScheduleTypeType,
    RelativePositionType,
    ScheduleEntryTypeType,
    StreamingMediaFileConditioningType,
    TierType,
    TrafficShapingTypeType,
    TypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AccessConfigurationTypeDef",
    "AdBreakOpportunityTypeDef",
    "AdBreakOutputTypeDef",
    "AdBreakTypeDef",
    "AdBreakUnionTypeDef",
    "AdConditioningConfigurationTypeDef",
    "AdDecisionServerConfigurationOutputTypeDef",
    "AdDecisionServerConfigurationTypeDef",
    "AdDecisionServerConfigurationUnionTypeDef",
    "AdMarkerPassthroughTypeDef",
    "AdsInteractionLogOutputTypeDef",
    "AdsInteractionLogTypeDef",
    "AdsInteractionLogUnionTypeDef",
    "AdsPersonalizationConcurrencyTypeDef",
    "AdsPersonalizationTimeoutsTypeDef",
    "AlertTypeDef",
    "AlternateMediaOutputTypeDef",
    "AlternateMediaTypeDef",
    "AlternateMediaUnionTypeDef",
    "AudienceMediaOutputTypeDef",
    "AudienceMediaTypeDef",
    "AudienceMediaUnionTypeDef",
    "AvailMatchingCriteriaTypeDef",
    "AvailSuppressionTypeDef",
    "BumperTypeDef",
    "CdnConfigurationTypeDef",
    "ChannelTypeDef",
    "ClipRangeTypeDef",
    "ConcurrentExecutorConfigurationOutputTypeDef",
    "ConcurrentExecutorConfigurationTypeDef",
    "ConcurrentExecutorConfigurationUnionTypeDef",
    "ConfigureLogsForChannelRequestTypeDef",
    "ConfigureLogsForChannelResponseTypeDef",
    "ConfigureLogsForPlaybackConfigurationRequestTypeDef",
    "ConfigureLogsForPlaybackConfigurationResponseTypeDef",
    "CreateChannelRequestTypeDef",
    "CreateChannelResponseTypeDef",
    "CreateLiveSourceRequestTypeDef",
    "CreateLiveSourceResponseTypeDef",
    "CreatePrefetchScheduleRequestTypeDef",
    "CreatePrefetchScheduleResponseTypeDef",
    "CreateProgramRequestTypeDef",
    "CreateProgramResponseTypeDef",
    "CreateSourceLocationRequestTypeDef",
    "CreateSourceLocationResponseTypeDef",
    "CreateVodSourceRequestTypeDef",
    "CreateVodSourceResponseTypeDef",
    "CustomOutputConfigurationOutputTypeDef",
    "CustomOutputConfigurationTypeDef",
    "CustomOutputConfigurationUnionTypeDef",
    "DashConfigurationForPutTypeDef",
    "DashConfigurationTypeDef",
    "DashPlaylistSettingsTypeDef",
    "DefaultSegmentDeliveryConfigurationTypeDef",
    "DeleteChannelPolicyRequestTypeDef",
    "DeleteChannelRequestTypeDef",
    "DeleteFunctionRequestTypeDef",
    "DeleteLiveSourceRequestTypeDef",
    "DeletePlaybackConfigurationRequestTypeDef",
    "DeletePrefetchScheduleRequestTypeDef",
    "DeleteProgramRequestTypeDef",
    "DeleteSourceLocationRequestTypeDef",
    "DeleteVodSourceRequestTypeDef",
    "DescribeChannelRequestTypeDef",
    "DescribeChannelResponseTypeDef",
    "DescribeLiveSourceRequestTypeDef",
    "DescribeLiveSourceResponseTypeDef",
    "DescribeProgramRequestTypeDef",
    "DescribeProgramResponseTypeDef",
    "DescribeSourceLocationRequestTypeDef",
    "DescribeSourceLocationResponseTypeDef",
    "DescribeVodSourceRequestTypeDef",
    "DescribeVodSourceResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "FunctionRefTypeDef",
    "FunctionTypeDef",
    "GetChannelPolicyRequestTypeDef",
    "GetChannelPolicyResponseTypeDef",
    "GetChannelScheduleRequestPaginateTypeDef",
    "GetChannelScheduleRequestTypeDef",
    "GetChannelScheduleResponseTypeDef",
    "GetFunctionRequestTypeDef",
    "GetFunctionResponseTypeDef",
    "GetPlaybackConfigurationRequestTypeDef",
    "GetPlaybackConfigurationResponseTypeDef",
    "GetPrefetchScheduleRequestTypeDef",
    "GetPrefetchScheduleResponseTypeDef",
    "HlsConfigurationTypeDef",
    "HlsPlaylistSettingsOutputTypeDef",
    "HlsPlaylistSettingsTypeDef",
    "HlsPlaylistSettingsUnionTypeDef",
    "HttpConfigurationTypeDef",
    "HttpPackageConfigurationTypeDef",
    "HttpRequestConfigurationOutputTypeDef",
    "HttpRequestConfigurationTypeDef",
    "HttpRequestConfigurationUnionTypeDef",
    "HttpRequestOutputTypeDef",
    "HttpRequestTypeDef",
    "KeyValuePairTypeDef",
    "ListAlertsRequestPaginateTypeDef",
    "ListAlertsRequestTypeDef",
    "ListAlertsResponseTypeDef",
    "ListChannelsRequestPaginateTypeDef",
    "ListChannelsRequestTypeDef",
    "ListChannelsResponseTypeDef",
    "ListFunctionsRequestPaginateTypeDef",
    "ListFunctionsRequestTypeDef",
    "ListFunctionsResponseTypeDef",
    "ListLiveSourcesRequestPaginateTypeDef",
    "ListLiveSourcesRequestTypeDef",
    "ListLiveSourcesResponseTypeDef",
    "ListPlaybackConfigurationsRequestPaginateTypeDef",
    "ListPlaybackConfigurationsRequestTypeDef",
    "ListPlaybackConfigurationsResponseTypeDef",
    "ListPrefetchSchedulesRequestPaginateTypeDef",
    "ListPrefetchSchedulesRequestTypeDef",
    "ListPrefetchSchedulesResponseTypeDef",
    "ListSourceLocationsRequestPaginateTypeDef",
    "ListSourceLocationsRequestTypeDef",
    "ListSourceLocationsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListVodSourcesRequestPaginateTypeDef",
    "ListVodSourcesRequestTypeDef",
    "ListVodSourcesResponseTypeDef",
    "LivePreRollConfigurationTypeDef",
    "LiveSourceTypeDef",
    "LogConfigurationForChannelTypeDef",
    "LogConfigurationTypeDef",
    "ManifestProcessingRulesTypeDef",
    "ManifestServiceInteractionLogOutputTypeDef",
    "ManifestServiceInteractionLogTypeDef",
    "ManifestServiceInteractionLogUnionTypeDef",
    "PaginatorConfigTypeDef",
    "PlaybackConfigurationTypeDef",
    "PrefetchConsumptionOutputTypeDef",
    "PrefetchConsumptionTypeDef",
    "PrefetchConsumptionUnionTypeDef",
    "PrefetchRetrievalOutputTypeDef",
    "PrefetchRetrievalTypeDef",
    "PrefetchRetrievalUnionTypeDef",
    "PrefetchScheduleTypeDef",
    "PutChannelPolicyRequestTypeDef",
    "PutFunctionRequestTypeDef",
    "PutFunctionResponseTypeDef",
    "PutPlaybackConfigurationRequestTypeDef",
    "PutPlaybackConfigurationResponseTypeDef",
    "RecurringConsumptionOutputTypeDef",
    "RecurringConsumptionTypeDef",
    "RecurringPrefetchConfigurationOutputTypeDef",
    "RecurringPrefetchConfigurationTypeDef",
    "RecurringPrefetchConfigurationUnionTypeDef",
    "RecurringRetrievalOutputTypeDef",
    "RecurringRetrievalTypeDef",
    "RequestOutputItemTypeDef",
    "ResponseMetadataTypeDef",
    "ResponseOutputItemTypeDef",
    "ScheduleAdBreakTypeDef",
    "ScheduleConfigurationTypeDef",
    "ScheduleEntryTypeDef",
    "SecretsManagerAccessTokenConfigurationTypeDef",
    "SegmentDeliveryConfigurationTypeDef",
    "SegmentationDescriptorTypeDef",
    "SequentialExecutorConfigurationOutputTypeDef",
    "SequentialExecutorConfigurationTypeDef",
    "SequentialExecutorConfigurationUnionTypeDef",
    "SlateSourceTypeDef",
    "SourceLocationTypeDef",
    "SpliceInsertMessageTypeDef",
    "StartChannelRequestTypeDef",
    "StopChannelRequestTypeDef",
    "TagResourceRequestTypeDef",
    "TimeShiftConfigurationTypeDef",
    "TimeSignalMessageOutputTypeDef",
    "TimeSignalMessageTypeDef",
    "TimeSignalMessageUnionTypeDef",
    "TimestampTypeDef",
    "TrafficShapingRetrievalWindowTypeDef",
    "TrafficShapingTpsConfigurationTypeDef",
    "TransitionTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateChannelRequestTypeDef",
    "UpdateChannelResponseTypeDef",
    "UpdateLiveSourceRequestTypeDef",
    "UpdateLiveSourceResponseTypeDef",
    "UpdateProgramRequestTypeDef",
    "UpdateProgramResponseTypeDef",
    "UpdateProgramScheduleConfigurationTypeDef",
    "UpdateProgramTransitionTypeDef",
    "UpdateSourceLocationRequestTypeDef",
    "UpdateSourceLocationResponseTypeDef",
    "UpdateVodSourceRequestTypeDef",
    "UpdateVodSourceResponseTypeDef",
    "VodSourceTypeDef",
)


class SecretsManagerAccessTokenConfigurationTypeDef(TypedDict):
    HeaderName: NotRequired[str]
    SecretArn: NotRequired[str]
    SecretStringKey: NotRequired[str]


class AdBreakOpportunityTypeDef(TypedDict):
    OffsetMillis: int


class KeyValuePairTypeDef(TypedDict):
    Key: str
    Value: str


class SlateSourceTypeDef(TypedDict):
    SourceLocationName: NotRequired[str]
    VodSourceName: NotRequired[str]


class SpliceInsertMessageTypeDef(TypedDict):
    AvailNum: NotRequired[int]
    AvailsExpected: NotRequired[int]
    SpliceEventId: NotRequired[int]
    UniqueProgramId: NotRequired[int]


class AdConditioningConfigurationTypeDef(TypedDict):
    StreamingMediaFileConditioning: StreamingMediaFileConditioningType


class HttpRequestOutputTypeDef(TypedDict):
    Method: NotRequired[MethodType]
    Body: NotRequired[str]
    Headers: NotRequired[dict[str, str]]
    CompressRequest: NotRequired[CompressionMethodType]


class HttpRequestTypeDef(TypedDict):
    Method: NotRequired[MethodType]
    Body: NotRequired[str]
    Headers: NotRequired[Mapping[str, str]]
    CompressRequest: NotRequired[CompressionMethodType]


class AdMarkerPassthroughTypeDef(TypedDict):
    Enabled: NotRequired[bool]


class AdsInteractionLogOutputTypeDef(TypedDict):
    PublishOptInEventTypes: NotRequired[list[AdsInteractionPublishOptInEventTypeType]]
    ExcludeEventTypes: NotRequired[list[AdsInteractionExcludeEventTypeType]]


class AdsInteractionLogTypeDef(TypedDict):
    PublishOptInEventTypes: NotRequired[Sequence[AdsInteractionPublishOptInEventTypeType]]
    ExcludeEventTypes: NotRequired[Sequence[AdsInteractionExcludeEventTypeType]]


class AdsPersonalizationConcurrencyTypeDef(TypedDict):
    MaxConcurrentAdsRequests: NotRequired[int]
    EnableVodVastParallelization: NotRequired[bool]


class AdsPersonalizationTimeoutsTypeDef(TypedDict):
    AdsRequestTimeoutMilliseconds: NotRequired[int]
    LiveMaximumAdsPersonalizationTimeMilliseconds: NotRequired[int]
    VodMaximumAdsPersonalizationTimeMilliseconds: NotRequired[int]
    PrefetchAdsRequestTimeoutMilliseconds: NotRequired[int]
    PrefetchMaximumAdsPersonalizationTimeMilliseconds: NotRequired[int]


class AlertTypeDef(TypedDict):
    AlertCode: str
    AlertMessage: str
    LastModifiedTime: datetime
    RelatedResourceArns: list[str]
    ResourceArn: str
    Category: NotRequired[AlertCategoryType]


class ClipRangeTypeDef(TypedDict):
    EndOffsetMillis: NotRequired[int]
    StartOffsetMillis: NotRequired[int]


class AvailMatchingCriteriaTypeDef(TypedDict):
    DynamicVariable: str
    Operator: Literal["EQUALS"]


class AvailSuppressionTypeDef(TypedDict):
    Mode: NotRequired[ModeType]
    Value: NotRequired[str]
    FillPolicy: NotRequired[FillPolicyType]


class BumperTypeDef(TypedDict):
    EndUrl: NotRequired[str]
    StartUrl: NotRequired[str]


class CdnConfigurationTypeDef(TypedDict):
    AdSegmentUrlPrefix: NotRequired[str]
    ContentSegmentUrlPrefix: NotRequired[str]


class LogConfigurationForChannelTypeDef(TypedDict):
    LogTypes: NotRequired[list[Literal["AS_RUN"]]]


class FunctionRefTypeDef(TypedDict):
    RunCondition: NotRequired[str]
    FunctionId: NotRequired[str]
    Alias: NotRequired[str]


class ConfigureLogsForChannelRequestTypeDef(TypedDict):
    ChannelName: str
    LogTypes: Sequence[Literal["AS_RUN"]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class ManifestServiceInteractionLogOutputTypeDef(TypedDict):
    PublishOptInEventTypes: NotRequired[list[ManifestServicePublishOptInEventTypeType]]
    ExcludeEventTypes: NotRequired[list[ManifestServiceExcludeEventTypeType]]


class TimeShiftConfigurationTypeDef(TypedDict):
    MaxTimeDelaySeconds: int


HttpPackageConfigurationTypeDef = TypedDict(
    "HttpPackageConfigurationTypeDef",
    {
        "Path": str,
        "SourceGroup": str,
        "Type": TypeType,
    },
)


class DefaultSegmentDeliveryConfigurationTypeDef(TypedDict):
    BaseUrl: NotRequired[str]


class HttpConfigurationTypeDef(TypedDict):
    BaseUrl: str


class SegmentDeliveryConfigurationTypeDef(TypedDict):
    BaseUrl: NotRequired[str]
    Name: NotRequired[str]


class CustomOutputConfigurationOutputTypeDef(TypedDict):
    Runtime: Literal["JSONATA"]
    Output: NotRequired[dict[str, str]]


class CustomOutputConfigurationTypeDef(TypedDict):
    Runtime: Literal["JSONATA"]
    Output: NotRequired[Mapping[str, str]]


class DashConfigurationForPutTypeDef(TypedDict):
    MpdLocation: NotRequired[str]
    OriginManifestType: NotRequired[OriginManifestTypeType]


class DashConfigurationTypeDef(TypedDict):
    ManifestEndpointPrefix: NotRequired[str]
    DualStackManifestEndpointPrefix: NotRequired[str]
    MpdLocation: NotRequired[str]
    OriginManifestType: NotRequired[OriginManifestTypeType]


class DashPlaylistSettingsTypeDef(TypedDict):
    ManifestWindowSeconds: NotRequired[int]
    MinBufferTimeSeconds: NotRequired[int]
    MinUpdatePeriodSeconds: NotRequired[int]
    SuggestedPresentationDelaySeconds: NotRequired[int]


class DeleteChannelPolicyRequestTypeDef(TypedDict):
    ChannelName: str


class DeleteChannelRequestTypeDef(TypedDict):
    ChannelName: str


class DeleteFunctionRequestTypeDef(TypedDict):
    FunctionId: str


class DeleteLiveSourceRequestTypeDef(TypedDict):
    LiveSourceName: str
    SourceLocationName: str


class DeletePlaybackConfigurationRequestTypeDef(TypedDict):
    Name: str


class DeletePrefetchScheduleRequestTypeDef(TypedDict):
    Name: str
    PlaybackConfigurationName: str


class DeleteProgramRequestTypeDef(TypedDict):
    ChannelName: str
    ProgramName: str


class DeleteSourceLocationRequestTypeDef(TypedDict):
    SourceLocationName: str


class DeleteVodSourceRequestTypeDef(TypedDict):
    SourceLocationName: str
    VodSourceName: str


class DescribeChannelRequestTypeDef(TypedDict):
    ChannelName: str


class DescribeLiveSourceRequestTypeDef(TypedDict):
    LiveSourceName: str
    SourceLocationName: str


class DescribeProgramRequestTypeDef(TypedDict):
    ChannelName: str
    ProgramName: str


class DescribeSourceLocationRequestTypeDef(TypedDict):
    SourceLocationName: str


class DescribeVodSourceRequestTypeDef(TypedDict):
    SourceLocationName: str
    VodSourceName: str


HttpRequestConfigurationOutputTypeDef = TypedDict(
    "HttpRequestConfigurationOutputTypeDef",
    {
        "Runtime": Literal["JSONATA"],
        "MethodType": MethodTypeType,
        "RequestTimeoutMilliseconds": int,
        "Url": str,
        "Output": NotRequired[dict[str, str]],
        "Body": NotRequired[str],
        "Headers": NotRequired[dict[str, str]],
    },
)


class GetChannelPolicyRequestTypeDef(TypedDict):
    ChannelName: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class GetChannelScheduleRequestTypeDef(TypedDict):
    ChannelName: str
    DurationMinutes: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Audience: NotRequired[str]


class GetFunctionRequestTypeDef(TypedDict):
    FunctionId: str


class GetPlaybackConfigurationRequestTypeDef(TypedDict):
    Name: str


class HlsConfigurationTypeDef(TypedDict):
    ManifestEndpointPrefix: NotRequired[str]
    DualStackManifestEndpointPrefix: NotRequired[str]


class LivePreRollConfigurationTypeDef(TypedDict):
    AdDecisionServerUrl: NotRequired[str]
    MaxDurationSeconds: NotRequired[int]


class GetPrefetchScheduleRequestTypeDef(TypedDict):
    Name: str
    PlaybackConfigurationName: str


class HlsPlaylistSettingsOutputTypeDef(TypedDict):
    ManifestWindowSeconds: NotRequired[int]
    AdMarkupType: NotRequired[list[AdMarkupTypeType]]


class HlsPlaylistSettingsTypeDef(TypedDict):
    ManifestWindowSeconds: NotRequired[int]
    AdMarkupType: NotRequired[Sequence[AdMarkupTypeType]]


HttpRequestConfigurationTypeDef = TypedDict(
    "HttpRequestConfigurationTypeDef",
    {
        "Runtime": Literal["JSONATA"],
        "MethodType": MethodTypeType,
        "RequestTimeoutMilliseconds": int,
        "Url": str,
        "Output": NotRequired[Mapping[str, str]],
        "Body": NotRequired[str],
        "Headers": NotRequired[Mapping[str, str]],
    },
)


class ListAlertsRequestTypeDef(TypedDict):
    ResourceArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListChannelsRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListFunctionsRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListLiveSourcesRequestTypeDef(TypedDict):
    SourceLocationName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListPlaybackConfigurationsRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListPrefetchSchedulesRequestTypeDef(TypedDict):
    PlaybackConfigurationName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ScheduleType: NotRequired[ListPrefetchScheduleTypeType]
    StreamId: NotRequired[str]


class ListSourceLocationsRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListTagsForResourceRequestTypeDef(TypedDict):
    ResourceArn: str


class ListVodSourcesRequestTypeDef(TypedDict):
    SourceLocationName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ManifestServiceInteractionLogTypeDef(TypedDict):
    PublishOptInEventTypes: NotRequired[Sequence[ManifestServicePublishOptInEventTypeType]]
    ExcludeEventTypes: NotRequired[Sequence[ManifestServiceExcludeEventTypeType]]


TimestampTypeDef = Union[datetime, str]


class TrafficShapingRetrievalWindowTypeDef(TypedDict):
    RetrievalWindowDurationSeconds: NotRequired[int]


class TrafficShapingTpsConfigurationTypeDef(TypedDict):
    PeakTps: NotRequired[int]
    PeakConcurrentUsers: NotRequired[int]


class PutChannelPolicyRequestTypeDef(TypedDict):
    ChannelName: str
    Policy: str


class ScheduleAdBreakTypeDef(TypedDict):
    ApproximateDurationSeconds: NotRequired[int]
    ApproximateStartTime: NotRequired[datetime]
    SourceLocationName: NotRequired[str]
    VodSourceName: NotRequired[str]


TransitionTypeDef = TypedDict(
    "TransitionTypeDef",
    {
        "RelativePosition": RelativePositionType,
        "Type": str,
        "DurationMillis": NotRequired[int],
        "RelativeProgram": NotRequired[str],
        "ScheduledStartTimeMillis": NotRequired[int],
    },
)


class SegmentationDescriptorTypeDef(TypedDict):
    SegmentationEventId: NotRequired[int]
    SegmentationUpidType: NotRequired[int]
    SegmentationUpid: NotRequired[str]
    SegmentationTypeId: NotRequired[int]
    SegmentNum: NotRequired[int]
    SegmentsExpected: NotRequired[int]
    SubSegmentNum: NotRequired[int]
    SubSegmentsExpected: NotRequired[int]


class StartChannelRequestTypeDef(TypedDict):
    ChannelName: str


class StopChannelRequestTypeDef(TypedDict):
    ChannelName: str


class TagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]


class UntagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class UpdateProgramTransitionTypeDef(TypedDict):
    ScheduledStartTimeMillis: NotRequired[int]
    DurationMillis: NotRequired[int]


class AccessConfigurationTypeDef(TypedDict):
    AccessType: NotRequired[AccessTypeType]
    SecretsManagerAccessTokenConfiguration: NotRequired[
        SecretsManagerAccessTokenConfigurationTypeDef
    ]


class AdDecisionServerConfigurationOutputTypeDef(TypedDict):
    HttpRequest: NotRequired[HttpRequestOutputTypeDef]


class AdDecisionServerConfigurationTypeDef(TypedDict):
    HttpRequest: NotRequired[HttpRequestTypeDef]


class ManifestProcessingRulesTypeDef(TypedDict):
    AdMarkerPassthrough: NotRequired[AdMarkerPassthroughTypeDef]


AdsInteractionLogUnionTypeDef = Union[AdsInteractionLogTypeDef, AdsInteractionLogOutputTypeDef]


class PrefetchConsumptionOutputTypeDef(TypedDict):
    EndTime: datetime
    AvailMatchingCriteria: NotRequired[list[AvailMatchingCriteriaTypeDef]]
    StartTime: NotRequired[datetime]


class RecurringConsumptionOutputTypeDef(TypedDict):
    RetrievedAdExpirationSeconds: NotRequired[int]
    AvailMatchingCriteria: NotRequired[list[AvailMatchingCriteriaTypeDef]]


class RecurringConsumptionTypeDef(TypedDict):
    RetrievedAdExpirationSeconds: NotRequired[int]
    AvailMatchingCriteria: NotRequired[Sequence[AvailMatchingCriteriaTypeDef]]


class ConcurrentExecutorConfigurationOutputTypeDef(TypedDict):
    Runtime: Literal["JSONATA"]
    Output: dict[str, str]
    FunctionList: list[FunctionRefTypeDef]
    TimeoutMilliseconds: int
    MaxConcurrency: int


class ConcurrentExecutorConfigurationTypeDef(TypedDict):
    Runtime: Literal["JSONATA"]
    Output: Mapping[str, str]
    FunctionList: Sequence[FunctionRefTypeDef]
    TimeoutMilliseconds: int
    MaxConcurrency: int


class SequentialExecutorConfigurationOutputTypeDef(TypedDict):
    Runtime: Literal["JSONATA"]
    FunctionList: list[FunctionRefTypeDef]
    TimeoutMilliseconds: int
    Output: NotRequired[dict[str, str]]


class SequentialExecutorConfigurationTypeDef(TypedDict):
    Runtime: Literal["JSONATA"]
    FunctionList: Sequence[FunctionRefTypeDef]
    TimeoutMilliseconds: int
    Output: NotRequired[Mapping[str, str]]


class ConfigureLogsForChannelResponseTypeDef(TypedDict):
    ChannelName: str
    LogTypes: list[Literal["AS_RUN"]]
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetChannelPolicyResponseTypeDef(TypedDict):
    Policy: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListAlertsResponseTypeDef(TypedDict):
    Items: list[AlertTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ConfigureLogsForPlaybackConfigurationResponseTypeDef(TypedDict):
    PercentEnabled: int
    PlaybackConfigurationName: str
    EnabledLoggingStrategies: list[LoggingStrategyType]
    AdsInteractionLog: AdsInteractionLogOutputTypeDef
    ManifestServiceInteractionLog: ManifestServiceInteractionLogOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class LogConfigurationTypeDef(TypedDict):
    PercentEnabled: int
    EnabledLoggingStrategies: list[LoggingStrategyType]
    AdsInteractionLog: NotRequired[AdsInteractionLogOutputTypeDef]
    ManifestServiceInteractionLog: NotRequired[ManifestServiceInteractionLogOutputTypeDef]


class CreateLiveSourceRequestTypeDef(TypedDict):
    HttpPackageConfigurations: Sequence[HttpPackageConfigurationTypeDef]
    LiveSourceName: str
    SourceLocationName: str
    Tags: NotRequired[Mapping[str, str]]


class CreateLiveSourceResponseTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    HttpPackageConfigurations: list[HttpPackageConfigurationTypeDef]
    LastModifiedTime: datetime
    LiveSourceName: str
    SourceLocationName: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateVodSourceRequestTypeDef(TypedDict):
    HttpPackageConfigurations: Sequence[HttpPackageConfigurationTypeDef]
    SourceLocationName: str
    VodSourceName: str
    Tags: NotRequired[Mapping[str, str]]


class CreateVodSourceResponseTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    HttpPackageConfigurations: list[HttpPackageConfigurationTypeDef]
    LastModifiedTime: datetime
    SourceLocationName: str
    Tags: dict[str, str]
    VodSourceName: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeLiveSourceResponseTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    HttpPackageConfigurations: list[HttpPackageConfigurationTypeDef]
    LastModifiedTime: datetime
    LiveSourceName: str
    SourceLocationName: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVodSourceResponseTypeDef(TypedDict):
    AdBreakOpportunities: list[AdBreakOpportunityTypeDef]
    Arn: str
    CreationTime: datetime
    HttpPackageConfigurations: list[HttpPackageConfigurationTypeDef]
    LastModifiedTime: datetime
    SourceLocationName: str
    Tags: dict[str, str]
    VodSourceName: str
    ResponseMetadata: ResponseMetadataTypeDef


class LiveSourceTypeDef(TypedDict):
    Arn: str
    HttpPackageConfigurations: list[HttpPackageConfigurationTypeDef]
    LiveSourceName: str
    SourceLocationName: str
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    Tags: NotRequired[dict[str, str]]


class UpdateLiveSourceRequestTypeDef(TypedDict):
    HttpPackageConfigurations: Sequence[HttpPackageConfigurationTypeDef]
    LiveSourceName: str
    SourceLocationName: str


class UpdateLiveSourceResponseTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    HttpPackageConfigurations: list[HttpPackageConfigurationTypeDef]
    LastModifiedTime: datetime
    LiveSourceName: str
    SourceLocationName: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateVodSourceRequestTypeDef(TypedDict):
    HttpPackageConfigurations: Sequence[HttpPackageConfigurationTypeDef]
    SourceLocationName: str
    VodSourceName: str


class UpdateVodSourceResponseTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    HttpPackageConfigurations: list[HttpPackageConfigurationTypeDef]
    LastModifiedTime: datetime
    SourceLocationName: str
    Tags: dict[str, str]
    VodSourceName: str
    ResponseMetadata: ResponseMetadataTypeDef


class VodSourceTypeDef(TypedDict):
    Arn: str
    HttpPackageConfigurations: list[HttpPackageConfigurationTypeDef]
    SourceLocationName: str
    VodSourceName: str
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    Tags: NotRequired[dict[str, str]]


CustomOutputConfigurationUnionTypeDef = Union[
    CustomOutputConfigurationTypeDef, CustomOutputConfigurationOutputTypeDef
]


class GetChannelScheduleRequestPaginateTypeDef(TypedDict):
    ChannelName: str
    DurationMinutes: NotRequired[str]
    Audience: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAlertsRequestPaginateTypeDef(TypedDict):
    ResourceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListChannelsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFunctionsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListLiveSourcesRequestPaginateTypeDef(TypedDict):
    SourceLocationName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPlaybackConfigurationsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPrefetchSchedulesRequestPaginateTypeDef(TypedDict):
    PlaybackConfigurationName: str
    ScheduleType: NotRequired[ListPrefetchScheduleTypeType]
    StreamId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSourceLocationsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListVodSourcesRequestPaginateTypeDef(TypedDict):
    SourceLocationName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ResponseOutputItemTypeDef(TypedDict):
    ManifestName: str
    PlaybackUrl: str
    SourceGroup: str
    DashPlaylistSettings: NotRequired[DashPlaylistSettingsTypeDef]
    HlsPlaylistSettings: NotRequired[HlsPlaylistSettingsOutputTypeDef]
    DualStackPlaybackUrl: NotRequired[str]


HlsPlaylistSettingsUnionTypeDef = Union[
    HlsPlaylistSettingsTypeDef, HlsPlaylistSettingsOutputTypeDef
]
HttpRequestConfigurationUnionTypeDef = Union[
    HttpRequestConfigurationTypeDef, HttpRequestConfigurationOutputTypeDef
]
ManifestServiceInteractionLogUnionTypeDef = Union[
    ManifestServiceInteractionLogTypeDef, ManifestServiceInteractionLogOutputTypeDef
]


class PrefetchConsumptionTypeDef(TypedDict):
    EndTime: TimestampTypeDef
    AvailMatchingCriteria: NotRequired[Sequence[AvailMatchingCriteriaTypeDef]]
    StartTime: NotRequired[TimestampTypeDef]


class PrefetchRetrievalOutputTypeDef(TypedDict):
    EndTime: datetime
    DynamicVariables: NotRequired[dict[str, str]]
    StartTime: NotRequired[datetime]
    TrafficShapingType: NotRequired[TrafficShapingTypeType]
    TrafficShapingRetrievalWindow: NotRequired[TrafficShapingRetrievalWindowTypeDef]
    TrafficShapingTpsConfiguration: NotRequired[TrafficShapingTpsConfigurationTypeDef]


class PrefetchRetrievalTypeDef(TypedDict):
    EndTime: TimestampTypeDef
    DynamicVariables: NotRequired[Mapping[str, str]]
    StartTime: NotRequired[TimestampTypeDef]
    TrafficShapingType: NotRequired[TrafficShapingTypeType]
    TrafficShapingRetrievalWindow: NotRequired[TrafficShapingRetrievalWindowTypeDef]
    TrafficShapingTpsConfiguration: NotRequired[TrafficShapingTpsConfigurationTypeDef]


class RecurringRetrievalOutputTypeDef(TypedDict):
    DynamicVariables: NotRequired[dict[str, str]]
    DelayAfterAvailEndSeconds: NotRequired[int]
    TrafficShapingType: NotRequired[TrafficShapingTypeType]
    TrafficShapingRetrievalWindow: NotRequired[TrafficShapingRetrievalWindowTypeDef]
    TrafficShapingTpsConfiguration: NotRequired[TrafficShapingTpsConfigurationTypeDef]


class RecurringRetrievalTypeDef(TypedDict):
    DynamicVariables: NotRequired[Mapping[str, str]]
    DelayAfterAvailEndSeconds: NotRequired[int]
    TrafficShapingType: NotRequired[TrafficShapingTypeType]
    TrafficShapingRetrievalWindow: NotRequired[TrafficShapingRetrievalWindowTypeDef]
    TrafficShapingTpsConfiguration: NotRequired[TrafficShapingTpsConfigurationTypeDef]


class ScheduleEntryTypeDef(TypedDict):
    Arn: str
    ChannelName: str
    ProgramName: str
    SourceLocationName: str
    ApproximateDurationSeconds: NotRequired[int]
    ApproximateStartTime: NotRequired[datetime]
    LiveSourceName: NotRequired[str]
    ScheduleAdBreaks: NotRequired[list[ScheduleAdBreakTypeDef]]
    ScheduleEntryType: NotRequired[ScheduleEntryTypeType]
    VodSourceName: NotRequired[str]
    Audiences: NotRequired[list[str]]


class ScheduleConfigurationTypeDef(TypedDict):
    Transition: TransitionTypeDef
    ClipRange: NotRequired[ClipRangeTypeDef]


class TimeSignalMessageOutputTypeDef(TypedDict):
    SegmentationDescriptors: NotRequired[list[SegmentationDescriptorTypeDef]]


class TimeSignalMessageTypeDef(TypedDict):
    SegmentationDescriptors: NotRequired[Sequence[SegmentationDescriptorTypeDef]]


class UpdateProgramScheduleConfigurationTypeDef(TypedDict):
    Transition: NotRequired[UpdateProgramTransitionTypeDef]
    ClipRange: NotRequired[ClipRangeTypeDef]


class CreateSourceLocationRequestTypeDef(TypedDict):
    HttpConfiguration: HttpConfigurationTypeDef
    SourceLocationName: str
    AccessConfiguration: NotRequired[AccessConfigurationTypeDef]
    DefaultSegmentDeliveryConfiguration: NotRequired[DefaultSegmentDeliveryConfigurationTypeDef]
    SegmentDeliveryConfigurations: NotRequired[Sequence[SegmentDeliveryConfigurationTypeDef]]
    Tags: NotRequired[Mapping[str, str]]


class CreateSourceLocationResponseTypeDef(TypedDict):
    AccessConfiguration: AccessConfigurationTypeDef
    Arn: str
    CreationTime: datetime
    DefaultSegmentDeliveryConfiguration: DefaultSegmentDeliveryConfigurationTypeDef
    HttpConfiguration: HttpConfigurationTypeDef
    LastModifiedTime: datetime
    SegmentDeliveryConfigurations: list[SegmentDeliveryConfigurationTypeDef]
    SourceLocationName: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeSourceLocationResponseTypeDef(TypedDict):
    AccessConfiguration: AccessConfigurationTypeDef
    Arn: str
    CreationTime: datetime
    DefaultSegmentDeliveryConfiguration: DefaultSegmentDeliveryConfigurationTypeDef
    HttpConfiguration: HttpConfigurationTypeDef
    LastModifiedTime: datetime
    SegmentDeliveryConfigurations: list[SegmentDeliveryConfigurationTypeDef]
    SourceLocationName: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class SourceLocationTypeDef(TypedDict):
    Arn: str
    HttpConfiguration: HttpConfigurationTypeDef
    SourceLocationName: str
    AccessConfiguration: NotRequired[AccessConfigurationTypeDef]
    CreationTime: NotRequired[datetime]
    DefaultSegmentDeliveryConfiguration: NotRequired[DefaultSegmentDeliveryConfigurationTypeDef]
    LastModifiedTime: NotRequired[datetime]
    SegmentDeliveryConfigurations: NotRequired[list[SegmentDeliveryConfigurationTypeDef]]
    Tags: NotRequired[dict[str, str]]


class UpdateSourceLocationRequestTypeDef(TypedDict):
    HttpConfiguration: HttpConfigurationTypeDef
    SourceLocationName: str
    AccessConfiguration: NotRequired[AccessConfigurationTypeDef]
    DefaultSegmentDeliveryConfiguration: NotRequired[DefaultSegmentDeliveryConfigurationTypeDef]
    SegmentDeliveryConfigurations: NotRequired[Sequence[SegmentDeliveryConfigurationTypeDef]]


class UpdateSourceLocationResponseTypeDef(TypedDict):
    AccessConfiguration: AccessConfigurationTypeDef
    Arn: str
    CreationTime: datetime
    DefaultSegmentDeliveryConfiguration: DefaultSegmentDeliveryConfigurationTypeDef
    HttpConfiguration: HttpConfigurationTypeDef
    LastModifiedTime: datetime
    SegmentDeliveryConfigurations: list[SegmentDeliveryConfigurationTypeDef]
    SourceLocationName: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


AdDecisionServerConfigurationUnionTypeDef = Union[
    AdDecisionServerConfigurationTypeDef, AdDecisionServerConfigurationOutputTypeDef
]
ConcurrentExecutorConfigurationUnionTypeDef = Union[
    ConcurrentExecutorConfigurationTypeDef, ConcurrentExecutorConfigurationOutputTypeDef
]


class FunctionTypeDef(TypedDict):
    FunctionId: str
    FunctionType: FunctionTypeType
    Description: NotRequired[str]
    HttpRequestConfiguration: NotRequired[HttpRequestConfigurationOutputTypeDef]
    CustomOutputConfiguration: NotRequired[CustomOutputConfigurationOutputTypeDef]
    ConcurrentExecutorConfiguration: NotRequired[ConcurrentExecutorConfigurationOutputTypeDef]
    SequentialExecutorConfiguration: NotRequired[SequentialExecutorConfigurationOutputTypeDef]
    Tags: NotRequired[dict[str, str]]
    Arn: NotRequired[str]


class GetFunctionResponseTypeDef(TypedDict):
    FunctionId: str
    FunctionType: FunctionTypeType
    Description: str
    HttpRequestConfiguration: HttpRequestConfigurationOutputTypeDef
    CustomOutputConfiguration: CustomOutputConfigurationOutputTypeDef
    ConcurrentExecutorConfiguration: ConcurrentExecutorConfigurationOutputTypeDef
    SequentialExecutorConfiguration: SequentialExecutorConfigurationOutputTypeDef
    Tags: dict[str, str]
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class PutFunctionResponseTypeDef(TypedDict):
    FunctionId: str
    FunctionType: FunctionTypeType
    Description: str
    HttpRequestConfiguration: HttpRequestConfigurationOutputTypeDef
    CustomOutputConfiguration: CustomOutputConfigurationOutputTypeDef
    ConcurrentExecutorConfiguration: ConcurrentExecutorConfigurationOutputTypeDef
    SequentialExecutorConfiguration: SequentialExecutorConfigurationOutputTypeDef
    Tags: dict[str, str]
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


SequentialExecutorConfigurationUnionTypeDef = Union[
    SequentialExecutorConfigurationTypeDef, SequentialExecutorConfigurationOutputTypeDef
]


class GetPlaybackConfigurationResponseTypeDef(TypedDict):
    AdDecisionServerUrl: str
    AvailSuppression: AvailSuppressionTypeDef
    Bumper: BumperTypeDef
    CdnConfiguration: CdnConfigurationTypeDef
    ConfigurationAliases: dict[str, dict[str, str]]
    DashConfiguration: DashConfigurationTypeDef
    HlsConfiguration: HlsConfigurationTypeDef
    InsertionMode: InsertionModeType
    LivePreRollConfiguration: LivePreRollConfigurationTypeDef
    LogConfiguration: LogConfigurationTypeDef
    ManifestProcessingRules: ManifestProcessingRulesTypeDef
    Name: str
    PersonalizationThresholdSeconds: int
    PlaybackConfigurationArn: str
    PlaybackEndpointPrefix: str
    DualStackPlaybackEndpointPrefix: str
    SessionInitializationEndpointPrefix: str
    DualStackSessionInitializationEndpointPrefix: str
    SlateAdUrl: str
    Tags: dict[str, str]
    TranscodeProfileName: str
    VideoContentSourceUrl: str
    AdConditioningConfiguration: AdConditioningConfigurationTypeDef
    AdDecisionServerConfiguration: AdDecisionServerConfigurationOutputTypeDef
    FunctionMapping: dict[EventNameType, str]
    AdsPersonalizationTimeouts: AdsPersonalizationTimeoutsTypeDef
    AdsPersonalizationConcurrency: AdsPersonalizationConcurrencyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PlaybackConfigurationTypeDef(TypedDict):
    AdDecisionServerUrl: NotRequired[str]
    AvailSuppression: NotRequired[AvailSuppressionTypeDef]
    Bumper: NotRequired[BumperTypeDef]
    CdnConfiguration: NotRequired[CdnConfigurationTypeDef]
    ConfigurationAliases: NotRequired[dict[str, dict[str, str]]]
    DashConfiguration: NotRequired[DashConfigurationTypeDef]
    HlsConfiguration: NotRequired[HlsConfigurationTypeDef]
    InsertionMode: NotRequired[InsertionModeType]
    LivePreRollConfiguration: NotRequired[LivePreRollConfigurationTypeDef]
    LogConfiguration: NotRequired[LogConfigurationTypeDef]
    ManifestProcessingRules: NotRequired[ManifestProcessingRulesTypeDef]
    Name: NotRequired[str]
    PersonalizationThresholdSeconds: NotRequired[int]
    PlaybackConfigurationArn: NotRequired[str]
    PlaybackEndpointPrefix: NotRequired[str]
    DualStackPlaybackEndpointPrefix: NotRequired[str]
    SessionInitializationEndpointPrefix: NotRequired[str]
    DualStackSessionInitializationEndpointPrefix: NotRequired[str]
    SlateAdUrl: NotRequired[str]
    Tags: NotRequired[dict[str, str]]
    TranscodeProfileName: NotRequired[str]
    VideoContentSourceUrl: NotRequired[str]
    AdConditioningConfiguration: NotRequired[AdConditioningConfigurationTypeDef]
    AdDecisionServerConfiguration: NotRequired[AdDecisionServerConfigurationOutputTypeDef]
    FunctionMapping: NotRequired[dict[EventNameType, str]]
    AdsPersonalizationTimeouts: NotRequired[AdsPersonalizationTimeoutsTypeDef]
    AdsPersonalizationConcurrency: NotRequired[AdsPersonalizationConcurrencyTypeDef]


class PutPlaybackConfigurationResponseTypeDef(TypedDict):
    AdDecisionServerUrl: str
    AvailSuppression: AvailSuppressionTypeDef
    Bumper: BumperTypeDef
    CdnConfiguration: CdnConfigurationTypeDef
    ConfigurationAliases: dict[str, dict[str, str]]
    DashConfiguration: DashConfigurationTypeDef
    HlsConfiguration: HlsConfigurationTypeDef
    InsertionMode: InsertionModeType
    LivePreRollConfiguration: LivePreRollConfigurationTypeDef
    LogConfiguration: LogConfigurationTypeDef
    ManifestProcessingRules: ManifestProcessingRulesTypeDef
    Name: str
    PersonalizationThresholdSeconds: int
    PlaybackConfigurationArn: str
    PlaybackEndpointPrefix: str
    DualStackPlaybackEndpointPrefix: str
    SessionInitializationEndpointPrefix: str
    DualStackSessionInitializationEndpointPrefix: str
    SlateAdUrl: str
    Tags: dict[str, str]
    TranscodeProfileName: str
    VideoContentSourceUrl: str
    AdConditioningConfiguration: AdConditioningConfigurationTypeDef
    AdDecisionServerConfiguration: AdDecisionServerConfigurationOutputTypeDef
    FunctionMapping: dict[EventNameType, str]
    AdsPersonalizationTimeouts: AdsPersonalizationTimeoutsTypeDef
    AdsPersonalizationConcurrency: AdsPersonalizationConcurrencyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListLiveSourcesResponseTypeDef(TypedDict):
    Items: list[LiveSourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListVodSourcesResponseTypeDef(TypedDict):
    Items: list[VodSourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ChannelTypeDef(TypedDict):
    Arn: str
    ChannelName: str
    ChannelState: str
    Outputs: list[ResponseOutputItemTypeDef]
    PlaybackMode: str
    Tier: str
    LogConfiguration: LogConfigurationForChannelTypeDef
    CreationTime: NotRequired[datetime]
    FillerSlate: NotRequired[SlateSourceTypeDef]
    LastModifiedTime: NotRequired[datetime]
    Tags: NotRequired[dict[str, str]]
    Audiences: NotRequired[list[str]]


class CreateChannelResponseTypeDef(TypedDict):
    Arn: str
    ChannelName: str
    ChannelState: ChannelStateType
    CreationTime: datetime
    FillerSlate: SlateSourceTypeDef
    LastModifiedTime: datetime
    Outputs: list[ResponseOutputItemTypeDef]
    PlaybackMode: str
    Tags: dict[str, str]
    Tier: str
    TimeShiftConfiguration: TimeShiftConfigurationTypeDef
    Audiences: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeChannelResponseTypeDef(TypedDict):
    Arn: str
    ChannelName: str
    ChannelState: ChannelStateType
    CreationTime: datetime
    FillerSlate: SlateSourceTypeDef
    LastModifiedTime: datetime
    Outputs: list[ResponseOutputItemTypeDef]
    PlaybackMode: str
    Tags: dict[str, str]
    Tier: str
    LogConfiguration: LogConfigurationForChannelTypeDef
    TimeShiftConfiguration: TimeShiftConfigurationTypeDef
    Audiences: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateChannelResponseTypeDef(TypedDict):
    Arn: str
    ChannelName: str
    ChannelState: ChannelStateType
    CreationTime: datetime
    FillerSlate: SlateSourceTypeDef
    LastModifiedTime: datetime
    Outputs: list[ResponseOutputItemTypeDef]
    PlaybackMode: str
    Tags: dict[str, str]
    Tier: str
    TimeShiftConfiguration: TimeShiftConfigurationTypeDef
    Audiences: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class RequestOutputItemTypeDef(TypedDict):
    ManifestName: str
    SourceGroup: str
    DashPlaylistSettings: NotRequired[DashPlaylistSettingsTypeDef]
    HlsPlaylistSettings: NotRequired[HlsPlaylistSettingsUnionTypeDef]


class ConfigureLogsForPlaybackConfigurationRequestTypeDef(TypedDict):
    PercentEnabled: int
    PlaybackConfigurationName: str
    EnabledLoggingStrategies: NotRequired[Sequence[LoggingStrategyType]]
    AdsInteractionLog: NotRequired[AdsInteractionLogUnionTypeDef]
    ManifestServiceInteractionLog: NotRequired[ManifestServiceInteractionLogUnionTypeDef]


PrefetchConsumptionUnionTypeDef = Union[
    PrefetchConsumptionTypeDef, PrefetchConsumptionOutputTypeDef
]
PrefetchRetrievalUnionTypeDef = Union[PrefetchRetrievalTypeDef, PrefetchRetrievalOutputTypeDef]


class RecurringPrefetchConfigurationOutputTypeDef(TypedDict):
    EndTime: datetime
    RecurringConsumption: RecurringConsumptionOutputTypeDef
    RecurringRetrieval: RecurringRetrievalOutputTypeDef
    StartTime: NotRequired[datetime]


class RecurringPrefetchConfigurationTypeDef(TypedDict):
    EndTime: TimestampTypeDef
    RecurringConsumption: RecurringConsumptionTypeDef
    RecurringRetrieval: RecurringRetrievalTypeDef
    StartTime: NotRequired[TimestampTypeDef]


class GetChannelScheduleResponseTypeDef(TypedDict):
    Items: list[ScheduleEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AdBreakOutputTypeDef(TypedDict):
    OffsetMillis: int
    MessageType: NotRequired[MessageTypeType]
    Slate: NotRequired[SlateSourceTypeDef]
    SpliceInsertMessage: NotRequired[SpliceInsertMessageTypeDef]
    TimeSignalMessage: NotRequired[TimeSignalMessageOutputTypeDef]
    AdBreakMetadata: NotRequired[list[KeyValuePairTypeDef]]


TimeSignalMessageUnionTypeDef = Union[TimeSignalMessageTypeDef, TimeSignalMessageOutputTypeDef]


class ListSourceLocationsResponseTypeDef(TypedDict):
    Items: list[SourceLocationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PutPlaybackConfigurationRequestTypeDef(TypedDict):
    Name: str
    AdDecisionServerUrl: NotRequired[str]
    AvailSuppression: NotRequired[AvailSuppressionTypeDef]
    Bumper: NotRequired[BumperTypeDef]
    CdnConfiguration: NotRequired[CdnConfigurationTypeDef]
    ConfigurationAliases: NotRequired[Mapping[str, Mapping[str, str]]]
    DashConfiguration: NotRequired[DashConfigurationForPutTypeDef]
    InsertionMode: NotRequired[InsertionModeType]
    LivePreRollConfiguration: NotRequired[LivePreRollConfigurationTypeDef]
    ManifestProcessingRules: NotRequired[ManifestProcessingRulesTypeDef]
    PersonalizationThresholdSeconds: NotRequired[int]
    SlateAdUrl: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    TranscodeProfileName: NotRequired[str]
    VideoContentSourceUrl: NotRequired[str]
    AdConditioningConfiguration: NotRequired[AdConditioningConfigurationTypeDef]
    AdDecisionServerConfiguration: NotRequired[AdDecisionServerConfigurationUnionTypeDef]
    FunctionMapping: NotRequired[Mapping[EventNameType, str]]
    AdsPersonalizationTimeouts: NotRequired[AdsPersonalizationTimeoutsTypeDef]
    AdsPersonalizationConcurrency: NotRequired[AdsPersonalizationConcurrencyTypeDef]


class ListFunctionsResponseTypeDef(TypedDict):
    Items: list[FunctionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PutFunctionRequestTypeDef(TypedDict):
    FunctionId: str
    FunctionType: FunctionTypeType
    Description: NotRequired[str]
    HttpRequestConfiguration: NotRequired[HttpRequestConfigurationUnionTypeDef]
    CustomOutputConfiguration: NotRequired[CustomOutputConfigurationUnionTypeDef]
    ConcurrentExecutorConfiguration: NotRequired[ConcurrentExecutorConfigurationUnionTypeDef]
    SequentialExecutorConfiguration: NotRequired[SequentialExecutorConfigurationUnionTypeDef]
    Tags: NotRequired[Mapping[str, str]]


class ListPlaybackConfigurationsResponseTypeDef(TypedDict):
    Items: list[PlaybackConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListChannelsResponseTypeDef(TypedDict):
    Items: list[ChannelTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateChannelRequestTypeDef(TypedDict):
    ChannelName: str
    Outputs: Sequence[RequestOutputItemTypeDef]
    PlaybackMode: PlaybackModeType
    FillerSlate: NotRequired[SlateSourceTypeDef]
    Tags: NotRequired[Mapping[str, str]]
    Tier: NotRequired[TierType]
    TimeShiftConfiguration: NotRequired[TimeShiftConfigurationTypeDef]
    Audiences: NotRequired[Sequence[str]]


class UpdateChannelRequestTypeDef(TypedDict):
    ChannelName: str
    Outputs: Sequence[RequestOutputItemTypeDef]
    FillerSlate: NotRequired[SlateSourceTypeDef]
    TimeShiftConfiguration: NotRequired[TimeShiftConfigurationTypeDef]
    Audiences: NotRequired[Sequence[str]]


class CreatePrefetchScheduleResponseTypeDef(TypedDict):
    Arn: str
    Consumption: PrefetchConsumptionOutputTypeDef
    Name: str
    PlaybackConfigurationName: str
    Retrieval: PrefetchRetrievalOutputTypeDef
    RecurringPrefetchConfiguration: RecurringPrefetchConfigurationOutputTypeDef
    ScheduleType: PrefetchScheduleTypeType
    StreamId: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetPrefetchScheduleResponseTypeDef(TypedDict):
    Arn: str
    Consumption: PrefetchConsumptionOutputTypeDef
    Name: str
    PlaybackConfigurationName: str
    Retrieval: PrefetchRetrievalOutputTypeDef
    ScheduleType: PrefetchScheduleTypeType
    RecurringPrefetchConfiguration: RecurringPrefetchConfigurationOutputTypeDef
    StreamId: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class PrefetchScheduleTypeDef(TypedDict):
    Arn: str
    Name: str
    PlaybackConfigurationName: str
    Consumption: NotRequired[PrefetchConsumptionOutputTypeDef]
    Retrieval: NotRequired[PrefetchRetrievalOutputTypeDef]
    ScheduleType: NotRequired[PrefetchScheduleTypeType]
    RecurringPrefetchConfiguration: NotRequired[RecurringPrefetchConfigurationOutputTypeDef]
    StreamId: NotRequired[str]
    Tags: NotRequired[dict[str, str]]


RecurringPrefetchConfigurationUnionTypeDef = Union[
    RecurringPrefetchConfigurationTypeDef, RecurringPrefetchConfigurationOutputTypeDef
]


class AlternateMediaOutputTypeDef(TypedDict):
    SourceLocationName: NotRequired[str]
    LiveSourceName: NotRequired[str]
    VodSourceName: NotRequired[str]
    ClipRange: NotRequired[ClipRangeTypeDef]
    ScheduledStartTimeMillis: NotRequired[int]
    AdBreaks: NotRequired[list[AdBreakOutputTypeDef]]
    DurationMillis: NotRequired[int]


class AdBreakTypeDef(TypedDict):
    OffsetMillis: int
    MessageType: NotRequired[MessageTypeType]
    Slate: NotRequired[SlateSourceTypeDef]
    SpliceInsertMessage: NotRequired[SpliceInsertMessageTypeDef]
    TimeSignalMessage: NotRequired[TimeSignalMessageUnionTypeDef]
    AdBreakMetadata: NotRequired[Sequence[KeyValuePairTypeDef]]


class ListPrefetchSchedulesResponseTypeDef(TypedDict):
    Items: list[PrefetchScheduleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreatePrefetchScheduleRequestTypeDef(TypedDict):
    Name: str
    PlaybackConfigurationName: str
    Consumption: NotRequired[PrefetchConsumptionUnionTypeDef]
    Retrieval: NotRequired[PrefetchRetrievalUnionTypeDef]
    RecurringPrefetchConfiguration: NotRequired[RecurringPrefetchConfigurationUnionTypeDef]
    ScheduleType: NotRequired[PrefetchScheduleTypeType]
    StreamId: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]


class AudienceMediaOutputTypeDef(TypedDict):
    Audience: NotRequired[str]
    AlternateMedia: NotRequired[list[AlternateMediaOutputTypeDef]]


AdBreakUnionTypeDef = Union[AdBreakTypeDef, AdBreakOutputTypeDef]


class CreateProgramResponseTypeDef(TypedDict):
    AdBreaks: list[AdBreakOutputTypeDef]
    Arn: str
    ChannelName: str
    CreationTime: datetime
    LiveSourceName: str
    ProgramName: str
    ScheduledStartTime: datetime
    SourceLocationName: str
    VodSourceName: str
    ClipRange: ClipRangeTypeDef
    DurationMillis: int
    AudienceMedia: list[AudienceMediaOutputTypeDef]
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeProgramResponseTypeDef(TypedDict):
    AdBreaks: list[AdBreakOutputTypeDef]
    Arn: str
    ChannelName: str
    CreationTime: datetime
    LiveSourceName: str
    ProgramName: str
    ScheduledStartTime: datetime
    SourceLocationName: str
    VodSourceName: str
    ClipRange: ClipRangeTypeDef
    DurationMillis: int
    AudienceMedia: list[AudienceMediaOutputTypeDef]
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateProgramResponseTypeDef(TypedDict):
    AdBreaks: list[AdBreakOutputTypeDef]
    Arn: str
    ChannelName: str
    CreationTime: datetime
    ProgramName: str
    SourceLocationName: str
    VodSourceName: str
    LiveSourceName: str
    ClipRange: ClipRangeTypeDef
    DurationMillis: int
    ScheduledStartTime: datetime
    AudienceMedia: list[AudienceMediaOutputTypeDef]
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class AlternateMediaTypeDef(TypedDict):
    SourceLocationName: NotRequired[str]
    LiveSourceName: NotRequired[str]
    VodSourceName: NotRequired[str]
    ClipRange: NotRequired[ClipRangeTypeDef]
    ScheduledStartTimeMillis: NotRequired[int]
    AdBreaks: NotRequired[Sequence[AdBreakUnionTypeDef]]
    DurationMillis: NotRequired[int]


AlternateMediaUnionTypeDef = Union[AlternateMediaTypeDef, AlternateMediaOutputTypeDef]


class AudienceMediaTypeDef(TypedDict):
    Audience: NotRequired[str]
    AlternateMedia: NotRequired[Sequence[AlternateMediaUnionTypeDef]]


AudienceMediaUnionTypeDef = Union[AudienceMediaTypeDef, AudienceMediaOutputTypeDef]


class CreateProgramRequestTypeDef(TypedDict):
    ChannelName: str
    ProgramName: str
    ScheduleConfiguration: ScheduleConfigurationTypeDef
    SourceLocationName: str
    AdBreaks: NotRequired[Sequence[AdBreakUnionTypeDef]]
    LiveSourceName: NotRequired[str]
    VodSourceName: NotRequired[str]
    AudienceMedia: NotRequired[Sequence[AudienceMediaUnionTypeDef]]
    Tags: NotRequired[Mapping[str, str]]


class UpdateProgramRequestTypeDef(TypedDict):
    ChannelName: str
    ProgramName: str
    ScheduleConfiguration: UpdateProgramScheduleConfigurationTypeDef
    AdBreaks: NotRequired[Sequence[AdBreakUnionTypeDef]]
    AudienceMedia: NotRequired[Sequence[AudienceMediaUnionTypeDef]]
