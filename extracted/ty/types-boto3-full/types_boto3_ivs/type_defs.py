"""
Type annotations for ivs service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ivs/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_ivs.type_defs import MediaTailorPlaybackConfigurationTypeDef

    data: MediaTailorPlaybackConfigurationTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    ChannelLatencyModeType,
    ChannelTypeType,
    ContainerFormatType,
    MultitrackMaximumResolutionType,
    MultitrackPolicyType,
    RecordingConfigurationStateType,
    RecordingModeType,
    RenditionConfigurationRenditionSelectionType,
    RenditionConfigurationRenditionType,
    StreamHealthType,
    StreamStateType,
    ThumbnailConfigurationResolutionType,
    ThumbnailConfigurationStorageType,
    TranscodePresetType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AdConfigurationSummaryTypeDef",
    "AdConfigurationTypeDef",
    "AudioConfigurationTypeDef",
    "BatchErrorTypeDef",
    "BatchGetChannelRequestTypeDef",
    "BatchGetChannelResponseTypeDef",
    "BatchGetStreamKeyRequestTypeDef",
    "BatchGetStreamKeyResponseTypeDef",
    "BatchStartViewerSessionRevocationErrorTypeDef",
    "BatchStartViewerSessionRevocationRequestTypeDef",
    "BatchStartViewerSessionRevocationResponseTypeDef",
    "BatchStartViewerSessionRevocationViewerSessionTypeDef",
    "ChannelSummaryTypeDef",
    "ChannelTypeDef",
    "CreateAdConfigurationRequestTypeDef",
    "CreateAdConfigurationResponseTypeDef",
    "CreateChannelRequestTypeDef",
    "CreateChannelResponseTypeDef",
    "CreatePlaybackRestrictionPolicyRequestTypeDef",
    "CreatePlaybackRestrictionPolicyResponseTypeDef",
    "CreateRecordingConfigurationRequestTypeDef",
    "CreateRecordingConfigurationResponseTypeDef",
    "CreateStreamKeyRequestTypeDef",
    "CreateStreamKeyResponseTypeDef",
    "DeleteAdConfigurationRequestTypeDef",
    "DeleteChannelRequestTypeDef",
    "DeletePlaybackKeyPairRequestTypeDef",
    "DeletePlaybackRestrictionPolicyRequestTypeDef",
    "DeleteRecordingConfigurationRequestTypeDef",
    "DeleteStreamKeyRequestTypeDef",
    "DestinationConfigurationTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetAdConfigurationRequestTypeDef",
    "GetAdConfigurationResponseTypeDef",
    "GetChannelRequestTypeDef",
    "GetChannelResponseTypeDef",
    "GetPlaybackKeyPairRequestTypeDef",
    "GetPlaybackKeyPairResponseTypeDef",
    "GetPlaybackRestrictionPolicyRequestTypeDef",
    "GetPlaybackRestrictionPolicyResponseTypeDef",
    "GetRecordingConfigurationRequestTypeDef",
    "GetRecordingConfigurationResponseTypeDef",
    "GetStreamKeyRequestTypeDef",
    "GetStreamKeyResponseTypeDef",
    "GetStreamRequestTypeDef",
    "GetStreamResponseTypeDef",
    "GetStreamSessionRequestTypeDef",
    "GetStreamSessionResponseTypeDef",
    "ImportPlaybackKeyPairRequestTypeDef",
    "ImportPlaybackKeyPairResponseTypeDef",
    "IngestConfigurationTypeDef",
    "IngestConfigurationsTypeDef",
    "InsertAdBreakRequestTypeDef",
    "InsertAdBreakResponseTypeDef",
    "ListAdConfigurationsRequestPaginateTypeDef",
    "ListAdConfigurationsRequestTypeDef",
    "ListAdConfigurationsResponseTypeDef",
    "ListChannelsRequestPaginateTypeDef",
    "ListChannelsRequestTypeDef",
    "ListChannelsResponseTypeDef",
    "ListPlaybackKeyPairsRequestPaginateTypeDef",
    "ListPlaybackKeyPairsRequestTypeDef",
    "ListPlaybackKeyPairsResponseTypeDef",
    "ListPlaybackRestrictionPoliciesRequestTypeDef",
    "ListPlaybackRestrictionPoliciesResponseTypeDef",
    "ListRecordingConfigurationsRequestPaginateTypeDef",
    "ListRecordingConfigurationsRequestTypeDef",
    "ListRecordingConfigurationsResponseTypeDef",
    "ListStreamKeysRequestPaginateTypeDef",
    "ListStreamKeysRequestTypeDef",
    "ListStreamKeysResponseTypeDef",
    "ListStreamSessionsRequestTypeDef",
    "ListStreamSessionsResponseTypeDef",
    "ListStreamsRequestPaginateTypeDef",
    "ListStreamsRequestTypeDef",
    "ListStreamsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MediaTailorPlaybackConfigurationTypeDef",
    "MultitrackInputConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "PlaybackKeyPairSummaryTypeDef",
    "PlaybackKeyPairTypeDef",
    "PlaybackRestrictionPolicySummaryTypeDef",
    "PlaybackRestrictionPolicyTypeDef",
    "PutMetadataRequestTypeDef",
    "RecordingConfigurationSummaryTypeDef",
    "RecordingConfigurationTypeDef",
    "RenditionConfigurationOutputTypeDef",
    "RenditionConfigurationTypeDef",
    "RenditionConfigurationUnionTypeDef",
    "ResponseMetadataTypeDef",
    "S3DestinationConfigurationTypeDef",
    "SrtTypeDef",
    "StartViewerSessionRevocationRequestTypeDef",
    "StopStreamRequestTypeDef",
    "StreamEventTypeDef",
    "StreamFiltersTypeDef",
    "StreamKeySummaryTypeDef",
    "StreamKeyTypeDef",
    "StreamSessionSummaryTypeDef",
    "StreamSessionTypeDef",
    "StreamSummaryTypeDef",
    "StreamTypeDef",
    "TagResourceRequestTypeDef",
    "ThumbnailConfigurationOutputTypeDef",
    "ThumbnailConfigurationTypeDef",
    "ThumbnailConfigurationUnionTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateChannelRequestTypeDef",
    "UpdateChannelResponseTypeDef",
    "UpdatePlaybackRestrictionPolicyRequestTypeDef",
    "UpdatePlaybackRestrictionPolicyResponseTypeDef",
    "VideoConfigurationTypeDef",
)


class MediaTailorPlaybackConfigurationTypeDef(TypedDict):
    playbackConfigurationArn: NotRequired[str]


class AudioConfigurationTypeDef(TypedDict):
    codec: NotRequired[str]
    targetBitrate: NotRequired[int]
    sampleRate: NotRequired[int]
    channels: NotRequired[int]
    track: NotRequired[str]


class BatchErrorTypeDef(TypedDict):
    arn: NotRequired[str]
    code: NotRequired[str]
    message: NotRequired[str]


class BatchGetChannelRequestTypeDef(TypedDict):
    arns: Sequence[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class BatchGetStreamKeyRequestTypeDef(TypedDict):
    arns: Sequence[str]


class StreamKeyTypeDef(TypedDict):
    arn: NotRequired[str]
    value: NotRequired[str]
    channelArn: NotRequired[str]
    tags: NotRequired[dict[str, str]]


class BatchStartViewerSessionRevocationErrorTypeDef(TypedDict):
    channelArn: str
    viewerId: str
    code: NotRequired[str]
    message: NotRequired[str]


class BatchStartViewerSessionRevocationViewerSessionTypeDef(TypedDict):
    channelArn: str
    viewerId: str
    viewerSessionVersionsLessThanOrEqualTo: NotRequired[int]


ChannelSummaryTypeDef = TypedDict(
    "ChannelSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "latencyMode": NotRequired[ChannelLatencyModeType],
        "authorized": NotRequired[bool],
        "recordingConfigurationArn": NotRequired[str],
        "tags": NotRequired[dict[str, str]],
        "insecureIngest": NotRequired[bool],
        "type": NotRequired[ChannelTypeType],
        "preset": NotRequired[TranscodePresetType],
        "playbackRestrictionPolicyArn": NotRequired[str],
        "adConfigurationArn": NotRequired[str],
    },
)


class MultitrackInputConfigurationTypeDef(TypedDict):
    enabled: NotRequired[bool]
    policy: NotRequired[MultitrackPolicyType]
    maximumResolution: NotRequired[MultitrackMaximumResolutionType]


class SrtTypeDef(TypedDict):
    endpoint: NotRequired[str]
    passphrase: NotRequired[str]


class CreatePlaybackRestrictionPolicyRequestTypeDef(TypedDict):
    allowedCountries: NotRequired[Sequence[str]]
    allowedOrigins: NotRequired[Sequence[str]]
    enableStrictOriginEnforcement: NotRequired[bool]
    name: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class PlaybackRestrictionPolicyTypeDef(TypedDict):
    arn: str
    allowedCountries: list[str]
    allowedOrigins: list[str]
    enableStrictOriginEnforcement: NotRequired[bool]
    name: NotRequired[str]
    tags: NotRequired[dict[str, str]]


class CreateStreamKeyRequestTypeDef(TypedDict):
    channelArn: str
    tags: NotRequired[Mapping[str, str]]


class DeleteAdConfigurationRequestTypeDef(TypedDict):
    arn: str


class DeleteChannelRequestTypeDef(TypedDict):
    arn: str


class DeletePlaybackKeyPairRequestTypeDef(TypedDict):
    arn: str


class DeletePlaybackRestrictionPolicyRequestTypeDef(TypedDict):
    arn: str


class DeleteRecordingConfigurationRequestTypeDef(TypedDict):
    arn: str


class DeleteStreamKeyRequestTypeDef(TypedDict):
    arn: str


class S3DestinationConfigurationTypeDef(TypedDict):
    bucketName: str


class GetAdConfigurationRequestTypeDef(TypedDict):
    arn: str


class GetChannelRequestTypeDef(TypedDict):
    arn: str


class GetPlaybackKeyPairRequestTypeDef(TypedDict):
    arn: str


class PlaybackKeyPairTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    fingerprint: NotRequired[str]
    tags: NotRequired[dict[str, str]]


class GetPlaybackRestrictionPolicyRequestTypeDef(TypedDict):
    arn: str


class GetRecordingConfigurationRequestTypeDef(TypedDict):
    arn: str


class GetStreamKeyRequestTypeDef(TypedDict):
    arn: str


class GetStreamRequestTypeDef(TypedDict):
    channelArn: str


class StreamTypeDef(TypedDict):
    channelArn: NotRequired[str]
    streamId: NotRequired[str]
    playbackUrl: NotRequired[str]
    startTime: NotRequired[datetime]
    state: NotRequired[StreamStateType]
    health: NotRequired[StreamHealthType]
    viewerCount: NotRequired[int]


class GetStreamSessionRequestTypeDef(TypedDict):
    channelArn: str
    streamId: NotRequired[str]


class ImportPlaybackKeyPairRequestTypeDef(TypedDict):
    publicKeyMaterial: str
    name: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class VideoConfigurationTypeDef(TypedDict):
    avcProfile: NotRequired[str]
    avcLevel: NotRequired[str]
    codec: NotRequired[str]
    encoder: NotRequired[str]
    targetBitrate: NotRequired[int]
    targetFramerate: NotRequired[int]
    videoHeight: NotRequired[int]
    videoWidth: NotRequired[int]
    level: NotRequired[str]
    track: NotRequired[str]
    profile: NotRequired[str]


class InsertAdBreakRequestTypeDef(TypedDict):
    channelArn: str
    durationSeconds: int


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListAdConfigurationsRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListChannelsRequestTypeDef(TypedDict):
    filterByName: NotRequired[str]
    filterByRecordingConfigurationArn: NotRequired[str]
    filterByPlaybackRestrictionPolicyArn: NotRequired[str]
    filterByAdConfigurationArn: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListPlaybackKeyPairsRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class PlaybackKeyPairSummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    tags: NotRequired[dict[str, str]]


class ListPlaybackRestrictionPoliciesRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class PlaybackRestrictionPolicySummaryTypeDef(TypedDict):
    arn: str
    allowedCountries: list[str]
    allowedOrigins: list[str]
    enableStrictOriginEnforcement: NotRequired[bool]
    name: NotRequired[str]
    tags: NotRequired[dict[str, str]]


class ListRecordingConfigurationsRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListStreamKeysRequestTypeDef(TypedDict):
    channelArn: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class StreamKeySummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    channelArn: NotRequired[str]
    tags: NotRequired[dict[str, str]]


class ListStreamSessionsRequestTypeDef(TypedDict):
    channelArn: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class StreamSessionSummaryTypeDef(TypedDict):
    streamId: NotRequired[str]
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]
    hasErrorEvent: NotRequired[bool]


class StreamFiltersTypeDef(TypedDict):
    health: NotRequired[StreamHealthType]


class StreamSummaryTypeDef(TypedDict):
    channelArn: NotRequired[str]
    streamId: NotRequired[str]
    state: NotRequired[StreamStateType]
    health: NotRequired[StreamHealthType]
    viewerCount: NotRequired[int]
    startTime: NotRequired[datetime]


class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str


class PutMetadataRequestTypeDef(TypedDict):
    channelArn: str
    metadata: str


class RenditionConfigurationOutputTypeDef(TypedDict):
    renditionSelection: NotRequired[RenditionConfigurationRenditionSelectionType]
    renditions: NotRequired[list[RenditionConfigurationRenditionType]]


class ThumbnailConfigurationOutputTypeDef(TypedDict):
    recordingMode: NotRequired[RecordingModeType]
    targetIntervalSeconds: NotRequired[int]
    resolution: NotRequired[ThumbnailConfigurationResolutionType]
    storage: NotRequired[list[ThumbnailConfigurationStorageType]]


class RenditionConfigurationTypeDef(TypedDict):
    renditionSelection: NotRequired[RenditionConfigurationRenditionSelectionType]
    renditions: NotRequired[Sequence[RenditionConfigurationRenditionType]]


class StartViewerSessionRevocationRequestTypeDef(TypedDict):
    channelArn: str
    viewerId: str
    viewerSessionVersionsLessThanOrEqualTo: NotRequired[int]


class StopStreamRequestTypeDef(TypedDict):
    channelArn: str


StreamEventTypeDef = TypedDict(
    "StreamEventTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[str],
        "eventTime": NotRequired[datetime],
        "code": NotRequired[str],
    },
)


class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class ThumbnailConfigurationTypeDef(TypedDict):
    recordingMode: NotRequired[RecordingModeType]
    targetIntervalSeconds: NotRequired[int]
    resolution: NotRequired[ThumbnailConfigurationResolutionType]
    storage: NotRequired[Sequence[ThumbnailConfigurationStorageType]]


class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdatePlaybackRestrictionPolicyRequestTypeDef(TypedDict):
    arn: str
    allowedCountries: NotRequired[Sequence[str]]
    allowedOrigins: NotRequired[Sequence[str]]
    enableStrictOriginEnforcement: NotRequired[bool]
    name: NotRequired[str]


class AdConfigurationSummaryTypeDef(TypedDict):
    arn: str
    mediaTailorPlaybackConfigurations: list[MediaTailorPlaybackConfigurationTypeDef]
    name: NotRequired[str]
    tags: NotRequired[dict[str, str]]


class AdConfigurationTypeDef(TypedDict):
    arn: str
    mediaTailorPlaybackConfigurations: list[MediaTailorPlaybackConfigurationTypeDef]
    name: NotRequired[str]
    tags: NotRequired[dict[str, str]]


class CreateAdConfigurationRequestTypeDef(TypedDict):
    mediaTailorPlaybackConfigurations: Sequence[MediaTailorPlaybackConfigurationTypeDef]
    name: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class InsertAdBreakResponseTypeDef(TypedDict):
    adBreakId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchGetStreamKeyResponseTypeDef(TypedDict):
    accessControlAllowOrigin: str
    accessControlExposeHeaders: str
    cacheControl: str
    contentSecurityPolicy: str
    strictTransportSecurity: str
    xContentTypeOptions: str
    xFrameOptions: str
    streamKeys: list[StreamKeyTypeDef]
    errors: list[BatchErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateStreamKeyResponseTypeDef(TypedDict):
    streamKey: StreamKeyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetStreamKeyResponseTypeDef(TypedDict):
    streamKey: StreamKeyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class BatchStartViewerSessionRevocationResponseTypeDef(TypedDict):
    accessControlAllowOrigin: str
    accessControlExposeHeaders: str
    cacheControl: str
    contentSecurityPolicy: str
    strictTransportSecurity: str
    xContentTypeOptions: str
    xFrameOptions: str
    errors: list[BatchStartViewerSessionRevocationErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchStartViewerSessionRevocationRequestTypeDef(TypedDict):
    viewerSessions: Sequence[BatchStartViewerSessionRevocationViewerSessionTypeDef]


class ListChannelsResponseTypeDef(TypedDict):
    channels: list[ChannelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


CreateChannelRequestTypeDef = TypedDict(
    "CreateChannelRequestTypeDef",
    {
        "name": NotRequired[str],
        "latencyMode": NotRequired[ChannelLatencyModeType],
        "type": NotRequired[ChannelTypeType],
        "authorized": NotRequired[bool],
        "recordingConfigurationArn": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
        "insecureIngest": NotRequired[bool],
        "preset": NotRequired[TranscodePresetType],
        "playbackRestrictionPolicyArn": NotRequired[str],
        "multitrackInputConfiguration": NotRequired[MultitrackInputConfigurationTypeDef],
        "containerFormat": NotRequired[ContainerFormatType],
        "adConfigurationArn": NotRequired[str],
    },
)
UpdateChannelRequestTypeDef = TypedDict(
    "UpdateChannelRequestTypeDef",
    {
        "arn": str,
        "name": NotRequired[str],
        "latencyMode": NotRequired[ChannelLatencyModeType],
        "type": NotRequired[ChannelTypeType],
        "authorized": NotRequired[bool],
        "recordingConfigurationArn": NotRequired[str],
        "insecureIngest": NotRequired[bool],
        "preset": NotRequired[TranscodePresetType],
        "playbackRestrictionPolicyArn": NotRequired[str],
        "multitrackInputConfiguration": NotRequired[MultitrackInputConfigurationTypeDef],
        "containerFormat": NotRequired[ContainerFormatType],
        "adConfigurationArn": NotRequired[str],
    },
)
ChannelTypeDef = TypedDict(
    "ChannelTypeDef",
    {
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "latencyMode": NotRequired[ChannelLatencyModeType],
        "type": NotRequired[ChannelTypeType],
        "recordingConfigurationArn": NotRequired[str],
        "ingestEndpoint": NotRequired[str],
        "playbackUrl": NotRequired[str],
        "authorized": NotRequired[bool],
        "tags": NotRequired[dict[str, str]],
        "insecureIngest": NotRequired[bool],
        "preset": NotRequired[TranscodePresetType],
        "srt": NotRequired[SrtTypeDef],
        "playbackRestrictionPolicyArn": NotRequired[str],
        "multitrackInputConfiguration": NotRequired[MultitrackInputConfigurationTypeDef],
        "containerFormat": NotRequired[ContainerFormatType],
        "adConfigurationArn": NotRequired[str],
    },
)


class CreatePlaybackRestrictionPolicyResponseTypeDef(TypedDict):
    playbackRestrictionPolicy: PlaybackRestrictionPolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetPlaybackRestrictionPolicyResponseTypeDef(TypedDict):
    playbackRestrictionPolicy: PlaybackRestrictionPolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePlaybackRestrictionPolicyResponseTypeDef(TypedDict):
    playbackRestrictionPolicy: PlaybackRestrictionPolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DestinationConfigurationTypeDef(TypedDict):
    s3: NotRequired[S3DestinationConfigurationTypeDef]


class GetPlaybackKeyPairResponseTypeDef(TypedDict):
    keyPair: PlaybackKeyPairTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ImportPlaybackKeyPairResponseTypeDef(TypedDict):
    keyPair: PlaybackKeyPairTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetStreamResponseTypeDef(TypedDict):
    stream: StreamTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class IngestConfigurationTypeDef(TypedDict):
    video: NotRequired[VideoConfigurationTypeDef]
    audio: NotRequired[AudioConfigurationTypeDef]


class IngestConfigurationsTypeDef(TypedDict):
    videoConfigurations: list[VideoConfigurationTypeDef]
    audioConfigurations: list[AudioConfigurationTypeDef]


class ListAdConfigurationsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListChannelsRequestPaginateTypeDef(TypedDict):
    filterByName: NotRequired[str]
    filterByRecordingConfigurationArn: NotRequired[str]
    filterByPlaybackRestrictionPolicyArn: NotRequired[str]
    filterByAdConfigurationArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPlaybackKeyPairsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRecordingConfigurationsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListStreamKeysRequestPaginateTypeDef(TypedDict):
    channelArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPlaybackKeyPairsResponseTypeDef(TypedDict):
    keyPairs: list[PlaybackKeyPairSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListPlaybackRestrictionPoliciesResponseTypeDef(TypedDict):
    playbackRestrictionPolicies: list[PlaybackRestrictionPolicySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListStreamKeysResponseTypeDef(TypedDict):
    streamKeys: list[StreamKeySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListStreamSessionsResponseTypeDef(TypedDict):
    streamSessions: list[StreamSessionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListStreamsRequestPaginateTypeDef(TypedDict):
    filterBy: NotRequired[StreamFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListStreamsRequestTypeDef(TypedDict):
    filterBy: NotRequired[StreamFiltersTypeDef]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListStreamsResponseTypeDef(TypedDict):
    streams: list[StreamSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


RenditionConfigurationUnionTypeDef = Union[
    RenditionConfigurationTypeDef, RenditionConfigurationOutputTypeDef
]
ThumbnailConfigurationUnionTypeDef = Union[
    ThumbnailConfigurationTypeDef, ThumbnailConfigurationOutputTypeDef
]


class ListAdConfigurationsResponseTypeDef(TypedDict):
    adConfigurations: list[AdConfigurationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateAdConfigurationResponseTypeDef(TypedDict):
    adConfiguration: AdConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetAdConfigurationResponseTypeDef(TypedDict):
    adConfiguration: AdConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class BatchGetChannelResponseTypeDef(TypedDict):
    accessControlAllowOrigin: str
    accessControlExposeHeaders: str
    cacheControl: str
    contentSecurityPolicy: str
    strictTransportSecurity: str
    xContentTypeOptions: str
    xFrameOptions: str
    channels: list[ChannelTypeDef]
    errors: list[BatchErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateChannelResponseTypeDef(TypedDict):
    channel: ChannelTypeDef
    streamKey: StreamKeyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetChannelResponseTypeDef(TypedDict):
    channel: ChannelTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateChannelResponseTypeDef(TypedDict):
    channel: ChannelTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RecordingConfigurationSummaryTypeDef(TypedDict):
    arn: str
    destinationConfiguration: DestinationConfigurationTypeDef
    state: RecordingConfigurationStateType
    name: NotRequired[str]
    tags: NotRequired[dict[str, str]]


class RecordingConfigurationTypeDef(TypedDict):
    arn: str
    destinationConfiguration: DestinationConfigurationTypeDef
    state: RecordingConfigurationStateType
    name: NotRequired[str]
    tags: NotRequired[dict[str, str]]
    thumbnailConfiguration: NotRequired[ThumbnailConfigurationOutputTypeDef]
    recordingReconnectWindowSeconds: NotRequired[int]
    renditionConfiguration: NotRequired[RenditionConfigurationOutputTypeDef]


class CreateRecordingConfigurationRequestTypeDef(TypedDict):
    destinationConfiguration: DestinationConfigurationTypeDef
    name: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    thumbnailConfiguration: NotRequired[ThumbnailConfigurationUnionTypeDef]
    recordingReconnectWindowSeconds: NotRequired[int]
    renditionConfiguration: NotRequired[RenditionConfigurationUnionTypeDef]


class ListRecordingConfigurationsResponseTypeDef(TypedDict):
    recordingConfigurations: list[RecordingConfigurationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateRecordingConfigurationResponseTypeDef(TypedDict):
    recordingConfiguration: RecordingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetRecordingConfigurationResponseTypeDef(TypedDict):
    recordingConfiguration: RecordingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StreamSessionTypeDef(TypedDict):
    streamId: NotRequired[str]
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]
    channel: NotRequired[ChannelTypeDef]
    ingestConfiguration: NotRequired[IngestConfigurationTypeDef]
    ingestConfigurations: NotRequired[IngestConfigurationsTypeDef]
    recordingConfiguration: NotRequired[RecordingConfigurationTypeDef]
    truncatedEvents: NotRequired[list[StreamEventTypeDef]]


class GetStreamSessionResponseTypeDef(TypedDict):
    streamSession: StreamSessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
