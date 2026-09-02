"""
Type annotations for kinesis service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kinesis/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_kinesis.type_defs import AddTagsToStreamInputTypeDef

    data: AddTagsToStreamInputTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import IO, Any, Union

from botocore.eventstream import EventStream
from botocore.response import StreamingBody

from .literals import (
    ChannelDestinationTypeType,
    ChannelStatusType,
    ConsumerStatusType,
    EncryptionTypeType,
    MetricsNameType,
    MinimumThroughputBillingCommitmentInputStatusType,
    MinimumThroughputBillingCommitmentOutputStatusType,
    RecordFormatTypeType,
    S3CompressionTypeType,
    S3StorageClassType,
    S3TablesCompressionTypeType,
    ShardFilterTypeType,
    ShardIteratorTypeType,
    StreamModeType,
    StreamStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AddTagsToStreamInputTypeDef",
    "BlobTypeDef",
    "ChannelDescriptionTypeDef",
    "ChannelEncryptionConfigurationTypeDef",
    "ChannelLoggingConfigurationTypeDef",
    "ChannelLoggingUpdateInputTypeDef",
    "ChannelStreamConfigurationTypeDef",
    "ChannelStreamDescriptionTypeDef",
    "ChannelStreamIdentifierTypeDef",
    "ChannelSummaryTypeDef",
    "ChildShardTypeDef",
    "CloudWatchLogsTypeDef",
    "CloudWatchLogsUpdateInputTypeDef",
    "ConsumerDescriptionTypeDef",
    "ConsumerTypeDef",
    "CreateChannelInputTypeDef",
    "CreateChannelOutputTypeDef",
    "CreateStreamInputTypeDef",
    "DeadLetterQueueS3ConfigurationTypeDef",
    "DecreaseStreamRetentionPeriodInputTypeDef",
    "DeleteChannelInputTypeDef",
    "DeleteResourcePolicyInputTypeDef",
    "DeleteStreamInputTypeDef",
    "DeregisterStreamConsumerInputTypeDef",
    "DescribeAccountSettingsOutputTypeDef",
    "DescribeChannelInputTypeDef",
    "DescribeChannelInputWaitTypeDef",
    "DescribeChannelOutputTypeDef",
    "DescribeLimitsOutputTypeDef",
    "DescribeStreamConsumerInputTypeDef",
    "DescribeStreamConsumerOutputTypeDef",
    "DescribeStreamInputPaginateTypeDef",
    "DescribeStreamInputTypeDef",
    "DescribeStreamInputWaitExtraTypeDef",
    "DescribeStreamInputWaitTypeDef",
    "DescribeStreamOutputTypeDef",
    "DescribeStreamSummaryInputTypeDef",
    "DescribeStreamSummaryOutputTypeDef",
    "DisableEnhancedMonitoringInputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnableEnhancedMonitoringInputTypeDef",
    "EnhancedMetricsTypeDef",
    "EnhancedMonitoringOutputTypeDef",
    "GetRecordsInputTypeDef",
    "GetRecordsOutputTypeDef",
    "GetResourcePolicyInputTypeDef",
    "GetResourcePolicyOutputTypeDef",
    "GetShardIteratorInputTypeDef",
    "GetShardIteratorOutputTypeDef",
    "HashKeyRangeTypeDef",
    "IncreaseStreamRetentionPeriodInputTypeDef",
    "InternalFailureExceptionTypeDef",
    "KMSAccessDeniedExceptionTypeDef",
    "KMSDisabledExceptionTypeDef",
    "KMSInvalidStateExceptionTypeDef",
    "KMSNotFoundExceptionTypeDef",
    "KMSOptInRequiredTypeDef",
    "KMSThrottlingExceptionTypeDef",
    "ListChannelsInputPaginateTypeDef",
    "ListChannelsInputTypeDef",
    "ListChannelsOutputTypeDef",
    "ListShardsInputPaginateTypeDef",
    "ListShardsInputTypeDef",
    "ListShardsOutputTypeDef",
    "ListStreamConsumersInputPaginateTypeDef",
    "ListStreamConsumersInputTypeDef",
    "ListStreamConsumersOutputTypeDef",
    "ListStreamsInputPaginateTypeDef",
    "ListStreamsInputTypeDef",
    "ListStreamsOutputTypeDef",
    "ListTagsForResourceInputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "ListTagsForStreamInputTypeDef",
    "ListTagsForStreamOutputTypeDef",
    "MergeShardsInputTypeDef",
    "MinimumThroughputBillingCommitmentInputTypeDef",
    "MinimumThroughputBillingCommitmentOutputTypeDef",
    "PaginatorConfigTypeDef",
    "PartitionFieldTypeDef",
    "PartitionSpecOutputTypeDef",
    "PartitionSpecTypeDef",
    "PartitionSpecUnionTypeDef",
    "PutRecordInputTypeDef",
    "PutRecordOutputTypeDef",
    "PutRecordsInputTypeDef",
    "PutRecordsOutputTypeDef",
    "PutRecordsRequestEntryTypeDef",
    "PutRecordsResultEntryTypeDef",
    "PutResourcePolicyInputTypeDef",
    "RecordConfigurationTypeDef",
    "RecordTypeDef",
    "RegisterStreamConsumerInputTypeDef",
    "RegisterStreamConsumerOutputTypeDef",
    "RemoveTagsFromStreamInputTypeDef",
    "ResourceInUseExceptionTypeDef",
    "ResourceNotFoundExceptionTypeDef",
    "ResponseMetadataTypeDef",
    "S3DestinationConfigurationTypeDef",
    "S3DestinationDescriptionTypeDef",
    "S3DestinationUpdateInputTypeDef",
    "S3StorageConfigurationTypeDef",
    "S3TablesConfigurationOutputTypeDef",
    "S3TablesConfigurationTypeDef",
    "S3TablesConfigurationUnionTypeDef",
    "S3TablesDestinationConfigurationTypeDef",
    "S3TablesDestinationDescriptionTypeDef",
    "S3TablesDestinationUpdateInputTypeDef",
    "SequenceNumberRangeTypeDef",
    "ShardFilterTypeDef",
    "ShardTypeDef",
    "SplitShardInputTypeDef",
    "StartStreamEncryptionInputTypeDef",
    "StartingPositionTypeDef",
    "StopStreamEncryptionInputTypeDef",
    "StreamDescriptionSummaryTypeDef",
    "StreamDescriptionTypeDef",
    "StreamFilterTypeDef",
    "StreamModeDetailsTypeDef",
    "StreamSummaryTypeDef",
    "SubscribeToShardEventStreamTypeDef",
    "SubscribeToShardEventTypeDef",
    "SubscribeToShardInputTypeDef",
    "SubscribeToShardOutputTypeDef",
    "TagResourceInputTypeDef",
    "TagTypeDef",
    "TimestampTypeDef",
    "UntagResourceInputTypeDef",
    "UpdateAccountSettingsInputTypeDef",
    "UpdateAccountSettingsOutputTypeDef",
    "UpdateChannelInputTypeDef",
    "UpdateChannelOutputTypeDef",
    "UpdateMaxRecordSizeInputTypeDef",
    "UpdateShardCountInputTypeDef",
    "UpdateShardCountOutputTypeDef",
    "UpdateStreamModeInputTypeDef",
    "UpdateStreamWarmThroughputInputTypeDef",
    "UpdateStreamWarmThroughputOutputTypeDef",
    "WaiterConfigTypeDef",
    "WarmThroughputObjectTypeDef",
)

class AddTagsToStreamInputTypeDef(TypedDict):
    Tags: Mapping[str, str]
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]
    StreamId: NotRequired[str]

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class ChannelEncryptionConfigurationTypeDef(TypedDict):
    EncryptionType: Literal["KMS"]
    KeyId: str

class CloudWatchLogsTypeDef(TypedDict):
    Enabled: bool
    LogGroupName: NotRequired[str]
    LogStreamName: NotRequired[str]

class CloudWatchLogsUpdateInputTypeDef(TypedDict):
    Enabled: bool
    LogGroupName: NotRequired[str]
    LogStreamName: NotRequired[str]

class RecordConfigurationTypeDef(TypedDict):
    RecordFormatType: RecordFormatTypeType
    GSRSchemaARN: NotRequired[str]

class ChannelStreamIdentifierTypeDef(TypedDict):
    StreamARN: str
    StreamCreationTimestamp: datetime

class HashKeyRangeTypeDef(TypedDict):
    StartingHashKey: str
    EndingHashKey: str

class ConsumerDescriptionTypeDef(TypedDict):
    ConsumerName: str
    ConsumerARN: str
    ConsumerStatus: ConsumerStatusType
    ConsumerCreationTimestamp: datetime
    StreamARN: str

class ConsumerTypeDef(TypedDict):
    ConsumerName: str
    ConsumerARN: str
    ConsumerStatus: ConsumerStatusType
    ConsumerCreationTimestamp: datetime

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class StreamModeDetailsTypeDef(TypedDict):
    StreamMode: StreamModeType

class DeadLetterQueueS3ConfigurationTypeDef(TypedDict):
    BucketARN: str
    ExpectedBucketOwner: str
    ErrorOutputPrefix: NotRequired[str]

class DecreaseStreamRetentionPeriodInputTypeDef(TypedDict):
    RetentionPeriodHours: int
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]
    StreamId: NotRequired[str]

class DeleteChannelInputTypeDef(TypedDict):
    ChannelARN: str

class DeleteResourcePolicyInputTypeDef(TypedDict):
    ResourceARN: str
    StreamId: NotRequired[str]

class DeleteStreamInputTypeDef(TypedDict):
    StreamName: NotRequired[str]
    EnforceConsumerDeletion: NotRequired[bool]
    StreamARN: NotRequired[str]
    StreamId: NotRequired[str]

class DeregisterStreamConsumerInputTypeDef(TypedDict):
    StreamARN: NotRequired[str]
    ConsumerName: NotRequired[str]
    ConsumerARN: NotRequired[str]
    StreamId: NotRequired[str]

class MinimumThroughputBillingCommitmentOutputTypeDef(TypedDict):
    Status: MinimumThroughputBillingCommitmentOutputStatusType
    StartedAt: NotRequired[datetime]
    EndedAt: NotRequired[datetime]
    EarliestAllowedEndAt: NotRequired[datetime]

class DescribeChannelInputTypeDef(TypedDict):
    ChannelARN: str

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class DescribeStreamConsumerInputTypeDef(TypedDict):
    StreamARN: NotRequired[str]
    ConsumerName: NotRequired[str]
    ConsumerARN: NotRequired[str]
    StreamId: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class DescribeStreamInputTypeDef(TypedDict):
    StreamName: NotRequired[str]
    Limit: NotRequired[int]
    ExclusiveStartShardId: NotRequired[str]
    StreamARN: NotRequired[str]
    StreamId: NotRequired[str]

class DescribeStreamSummaryInputTypeDef(TypedDict):
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]
    StreamId: NotRequired[str]

class DisableEnhancedMonitoringInputTypeDef(TypedDict):
    ShardLevelMetrics: Sequence[MetricsNameType]
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]
    StreamId: NotRequired[str]

class EnableEnhancedMonitoringInputTypeDef(TypedDict):
    ShardLevelMetrics: Sequence[MetricsNameType]
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]
    StreamId: NotRequired[str]

class EnhancedMetricsTypeDef(TypedDict):
    ShardLevelMetrics: NotRequired[list[MetricsNameType]]

class GetRecordsInputTypeDef(TypedDict):
    ShardIterator: str
    Limit: NotRequired[int]
    StreamARN: NotRequired[str]
    StreamId: NotRequired[str]
    DryRun: NotRequired[bool]

class RecordTypeDef(TypedDict):
    SequenceNumber: str
    Data: bytes
    PartitionKey: str
    ApproximateArrivalTimestamp: NotRequired[datetime]
    EncryptionType: NotRequired[EncryptionTypeType]

class GetResourcePolicyInputTypeDef(TypedDict):
    ResourceARN: str
    StreamId: NotRequired[str]

TimestampTypeDef = Union[datetime, str]

class IncreaseStreamRetentionPeriodInputTypeDef(TypedDict):
    RetentionPeriodHours: int
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]
    StreamId: NotRequired[str]

class InternalFailureExceptionTypeDef(TypedDict):
    message: NotRequired[str]

class KMSAccessDeniedExceptionTypeDef(TypedDict):
    message: NotRequired[str]

class KMSDisabledExceptionTypeDef(TypedDict):
    message: NotRequired[str]

class KMSInvalidStateExceptionTypeDef(TypedDict):
    message: NotRequired[str]

class KMSNotFoundExceptionTypeDef(TypedDict):
    message: NotRequired[str]

class KMSOptInRequiredTypeDef(TypedDict):
    message: NotRequired[str]

class KMSThrottlingExceptionTypeDef(TypedDict):
    message: NotRequired[str]

class ListStreamsInputTypeDef(TypedDict):
    Limit: NotRequired[int]
    ExclusiveStartStreamName: NotRequired[str]
    NextToken: NotRequired[str]

class ListTagsForResourceInputTypeDef(TypedDict):
    ResourceARN: str
    StreamId: NotRequired[str]

class TagTypeDef(TypedDict):
    Key: str
    Value: NotRequired[str]

class ListTagsForStreamInputTypeDef(TypedDict):
    StreamName: NotRequired[str]
    ExclusiveStartTagKey: NotRequired[str]
    Limit: NotRequired[int]
    StreamARN: NotRequired[str]
    StreamId: NotRequired[str]

class MergeShardsInputTypeDef(TypedDict):
    ShardToMerge: str
    AdjacentShardToMerge: str
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]
    StreamId: NotRequired[str]

class MinimumThroughputBillingCommitmentInputTypeDef(TypedDict):
    Status: MinimumThroughputBillingCommitmentInputStatusType

class PartitionFieldTypeDef(TypedDict):
    Transform: Literal["TIME_HOUR"]
    SourceName: str

class PutRecordsResultEntryTypeDef(TypedDict):
    SequenceNumber: NotRequired[str]
    ShardId: NotRequired[str]
    ErrorCode: NotRequired[str]
    ErrorMessage: NotRequired[str]

class PutResourcePolicyInputTypeDef(TypedDict):
    ResourceARN: str
    Policy: str
    StreamId: NotRequired[str]

class RegisterStreamConsumerInputTypeDef(TypedDict):
    StreamARN: str
    ConsumerName: str
    StreamId: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class RemoveTagsFromStreamInputTypeDef(TypedDict):
    TagKeys: Sequence[str]
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]
    StreamId: NotRequired[str]

class ResourceInUseExceptionTypeDef(TypedDict):
    message: NotRequired[str]

class ResourceNotFoundExceptionTypeDef(TypedDict):
    message: NotRequired[str]

class S3StorageConfigurationTypeDef(TypedDict):
    BucketARN: str
    ExpectedBucketOwner: str
    CompressionType: S3CompressionTypeType
    OutputKeyTemplate: NotRequired[str]
    StorageClass: NotRequired[S3StorageClassType]

class S3DestinationUpdateInputTypeDef(TypedDict):
    DataFreshnessInSeconds: int

class S3TablesDestinationUpdateInputTypeDef(TypedDict):
    DataFreshnessInSeconds: int

class SequenceNumberRangeTypeDef(TypedDict):
    StartingSequenceNumber: str
    EndingSequenceNumber: NotRequired[str]

class SplitShardInputTypeDef(TypedDict):
    ShardToSplit: str
    NewStartingHashKey: str
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]
    StreamId: NotRequired[str]

class StartStreamEncryptionInputTypeDef(TypedDict):
    EncryptionType: EncryptionTypeType
    KeyId: str
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]
    StreamId: NotRequired[str]

class StopStreamEncryptionInputTypeDef(TypedDict):
    EncryptionType: EncryptionTypeType
    KeyId: str
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]
    StreamId: NotRequired[str]

class WarmThroughputObjectTypeDef(TypedDict):
    TargetMiBps: NotRequired[int]
    CurrentMiBps: NotRequired[int]

class TagResourceInputTypeDef(TypedDict):
    Tags: Mapping[str, str]
    ResourceARN: str
    StreamId: NotRequired[str]

class UntagResourceInputTypeDef(TypedDict):
    TagKeys: Sequence[str]
    ResourceARN: str
    StreamId: NotRequired[str]

class UpdateMaxRecordSizeInputTypeDef(TypedDict):
    MaxRecordSizeInKiB: int
    StreamARN: NotRequired[str]
    StreamId: NotRequired[str]

class UpdateShardCountInputTypeDef(TypedDict):
    TargetShardCount: int
    ScalingType: Literal["UNIFORM_SCALING"]
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]
    StreamId: NotRequired[str]

class UpdateStreamWarmThroughputInputTypeDef(TypedDict):
    WarmThroughputMiBps: int
    StreamARN: NotRequired[str]
    StreamName: NotRequired[str]
    StreamId: NotRequired[str]

class PutRecordInputTypeDef(TypedDict):
    Data: BlobTypeDef
    PartitionKey: str
    StreamName: NotRequired[str]
    ExplicitHashKey: NotRequired[str]
    SequenceNumberForOrdering: NotRequired[str]
    StreamARN: NotRequired[str]
    StreamId: NotRequired[str]
    DryRun: NotRequired[bool]

class PutRecordsRequestEntryTypeDef(TypedDict):
    Data: BlobTypeDef
    PartitionKey: str
    ExplicitHashKey: NotRequired[str]

class ChannelLoggingConfigurationTypeDef(TypedDict):
    CloudWatchLogs: CloudWatchLogsTypeDef

class ChannelLoggingUpdateInputTypeDef(TypedDict):
    CloudWatchLogs: CloudWatchLogsUpdateInputTypeDef

class ChannelStreamConfigurationTypeDef(TypedDict):
    StreamARN: str
    RecordConfiguration: RecordConfigurationTypeDef

class ChannelStreamDescriptionTypeDef(TypedDict):
    StreamARN: str
    StreamCreationTimestamp: datetime
    RecordConfiguration: RecordConfigurationTypeDef

class ChannelSummaryTypeDef(TypedDict):
    ChannelName: str
    ChannelARN: str
    ChannelId: str
    ChannelStatus: ChannelStatusType
    ChannelCreationTimestamp: datetime
    ChannelDestinationType: ChannelDestinationTypeType
    Streams: list[ChannelStreamIdentifierTypeDef]
    ChannelStatusReason: NotRequired[str]

class ChildShardTypeDef(TypedDict):
    ShardId: str
    ParentShards: list[str]
    HashKeyRange: HashKeyRangeTypeDef

class DescribeLimitsOutputTypeDef(TypedDict):
    ShardLimit: int
    OpenShardCount: int
    OnDemandStreamCount: int
    OnDemandStreamCountLimit: int
    ChannelCount: int
    ChannelCountLimit: int
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeStreamConsumerOutputTypeDef(TypedDict):
    ConsumerDescription: ConsumerDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class EnhancedMonitoringOutputTypeDef(TypedDict):
    StreamName: str
    CurrentShardLevelMetrics: list[MetricsNameType]
    DesiredShardLevelMetrics: list[MetricsNameType]
    StreamARN: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetResourcePolicyOutputTypeDef(TypedDict):
    Policy: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetShardIteratorOutputTypeDef(TypedDict):
    ShardIterator: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListStreamConsumersOutputTypeDef(TypedDict):
    Consumers: list[ConsumerTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class PutRecordOutputTypeDef(TypedDict):
    ShardId: str
    SequenceNumber: str
    EncryptionType: EncryptionTypeType
    ResponseMetadata: ResponseMetadataTypeDef

class RegisterStreamConsumerOutputTypeDef(TypedDict):
    Consumer: ConsumerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateShardCountOutputTypeDef(TypedDict):
    StreamName: str
    CurrentShardCount: int
    TargetShardCount: int
    StreamARN: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateStreamInputTypeDef(TypedDict):
    StreamName: str
    ShardCount: NotRequired[int]
    StreamModeDetails: NotRequired[StreamModeDetailsTypeDef]
    Tags: NotRequired[Mapping[str, str]]
    WarmThroughputMiBps: NotRequired[int]
    MaxRecordSizeInKiB: NotRequired[int]

class StreamSummaryTypeDef(TypedDict):
    StreamName: str
    StreamARN: str
    StreamStatus: StreamStatusType
    StreamModeDetails: NotRequired[StreamModeDetailsTypeDef]
    StreamCreationTimestamp: NotRequired[datetime]

class UpdateStreamModeInputTypeDef(TypedDict):
    StreamARN: str
    StreamModeDetails: StreamModeDetailsTypeDef
    StreamId: NotRequired[str]
    WarmThroughputMiBps: NotRequired[int]

class DescribeAccountSettingsOutputTypeDef(TypedDict):
    MinimumThroughputBillingCommitment: MinimumThroughputBillingCommitmentOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAccountSettingsOutputTypeDef(TypedDict):
    MinimumThroughputBillingCommitment: MinimumThroughputBillingCommitmentOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeChannelInputWaitTypeDef(TypedDict):
    ChannelARN: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeStreamInputWaitExtraTypeDef(TypedDict):
    StreamName: NotRequired[str]
    Limit: NotRequired[int]
    ExclusiveStartShardId: NotRequired[str]
    StreamARN: NotRequired[str]
    StreamId: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeStreamInputWaitTypeDef(TypedDict):
    StreamName: NotRequired[str]
    Limit: NotRequired[int]
    ExclusiveStartShardId: NotRequired[str]
    StreamARN: NotRequired[str]
    StreamId: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeStreamInputPaginateTypeDef(TypedDict):
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]
    StreamId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListStreamsInputPaginateTypeDef(TypedDict):
    ExclusiveStartStreamName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetShardIteratorInputTypeDef(TypedDict):
    ShardId: str
    ShardIteratorType: ShardIteratorTypeType
    StreamName: NotRequired[str]
    StartingSequenceNumber: NotRequired[str]
    Timestamp: NotRequired[TimestampTypeDef]
    StreamARN: NotRequired[str]
    StreamId: NotRequired[str]
    DryRun: NotRequired[bool]

class ListStreamConsumersInputPaginateTypeDef(TypedDict):
    StreamARN: str
    StreamCreationTimestamp: NotRequired[TimestampTypeDef]
    StreamId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListStreamConsumersInputTypeDef(TypedDict):
    StreamARN: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    StreamCreationTimestamp: NotRequired[TimestampTypeDef]
    StreamId: NotRequired[str]

ShardFilterTypeDef = TypedDict(
    "ShardFilterTypeDef",
    {
        "Type": ShardFilterTypeType,
        "ShardId": NotRequired[str],
        "Timestamp": NotRequired[TimestampTypeDef],
    },
)
StartingPositionTypeDef = TypedDict(
    "StartingPositionTypeDef",
    {
        "Type": ShardIteratorTypeType,
        "SequenceNumber": NotRequired[str],
        "Timestamp": NotRequired[TimestampTypeDef],
    },
)

class StreamFilterTypeDef(TypedDict):
    StreamARN: str
    StreamCreationTimestamp: NotRequired[TimestampTypeDef]

class ListTagsForResourceOutputTypeDef(TypedDict):
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForStreamOutputTypeDef(TypedDict):
    Tags: list[TagTypeDef]
    HasMoreTags: bool
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAccountSettingsInputTypeDef(TypedDict):
    MinimumThroughputBillingCommitment: MinimumThroughputBillingCommitmentInputTypeDef

class PartitionSpecOutputTypeDef(TypedDict):
    PartitionFields: list[PartitionFieldTypeDef]

class PartitionSpecTypeDef(TypedDict):
    PartitionFields: Sequence[PartitionFieldTypeDef]

class PutRecordsOutputTypeDef(TypedDict):
    FailedRecordCount: int
    Records: list[PutRecordsResultEntryTypeDef]
    EncryptionType: EncryptionTypeType
    ResponseMetadata: ResponseMetadataTypeDef

class S3DestinationConfigurationTypeDef(TypedDict):
    StorageConfiguration: S3StorageConfigurationTypeDef
    DataFreshnessInSeconds: NotRequired[int]
    DeadLetterQueueS3Configuration: NotRequired[DeadLetterQueueS3ConfigurationTypeDef]

class S3DestinationDescriptionTypeDef(TypedDict):
    DataFreshnessInSeconds: int
    DeadLetterQueueS3Configuration: DeadLetterQueueS3ConfigurationTypeDef
    StorageConfiguration: S3StorageConfigurationTypeDef

class ShardTypeDef(TypedDict):
    ShardId: str
    HashKeyRange: HashKeyRangeTypeDef
    SequenceNumberRange: SequenceNumberRangeTypeDef
    ParentShardId: NotRequired[str]
    AdjacentParentShardId: NotRequired[str]

class StreamDescriptionSummaryTypeDef(TypedDict):
    StreamName: str
    StreamARN: str
    StreamStatus: StreamStatusType
    RetentionPeriodHours: int
    StreamCreationTimestamp: datetime
    EnhancedMonitoring: list[EnhancedMetricsTypeDef]
    OpenShardCount: int
    StreamId: NotRequired[str]
    StreamModeDetails: NotRequired[StreamModeDetailsTypeDef]
    EncryptionType: NotRequired[EncryptionTypeType]
    KeyId: NotRequired[str]
    ConsumerCount: NotRequired[int]
    WarmThroughput: NotRequired[WarmThroughputObjectTypeDef]
    MaxRecordSizeInKiB: NotRequired[int]
    ChannelCount: NotRequired[int]

class UpdateStreamWarmThroughputOutputTypeDef(TypedDict):
    StreamARN: str
    StreamName: str
    WarmThroughput: WarmThroughputObjectTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutRecordsInputTypeDef(TypedDict):
    Records: Sequence[PutRecordsRequestEntryTypeDef]
    StreamName: NotRequired[str]
    StreamARN: NotRequired[str]
    StreamId: NotRequired[str]
    DryRun: NotRequired[bool]

class UpdateChannelInputTypeDef(TypedDict):
    ChannelARN: str
    S3DestinationConfiguration: NotRequired[S3DestinationUpdateInputTypeDef]
    S3TablesDestinationConfiguration: NotRequired[S3TablesDestinationUpdateInputTypeDef]
    LoggingConfiguration: NotRequired[ChannelLoggingUpdateInputTypeDef]

class ListChannelsOutputTypeDef(TypedDict):
    ChannelSummaries: list[ChannelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetRecordsOutputTypeDef(TypedDict):
    Records: list[RecordTypeDef]
    NextShardIterator: str
    MillisBehindLatest: int
    ChildShards: list[ChildShardTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class SubscribeToShardEventTypeDef(TypedDict):
    Records: list[RecordTypeDef]
    ContinuationSequenceNumber: str
    MillisBehindLatest: int
    ChildShards: NotRequired[list[ChildShardTypeDef]]

class ListStreamsOutputTypeDef(TypedDict):
    StreamNames: list[str]
    HasMoreStreams: bool
    StreamSummaries: list[StreamSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListShardsInputPaginateTypeDef(TypedDict):
    StreamName: NotRequired[str]
    ExclusiveStartShardId: NotRequired[str]
    StreamCreationTimestamp: NotRequired[TimestampTypeDef]
    ShardFilter: NotRequired[ShardFilterTypeDef]
    StreamARN: NotRequired[str]
    StreamId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListShardsInputTypeDef(TypedDict):
    StreamName: NotRequired[str]
    NextToken: NotRequired[str]
    ExclusiveStartShardId: NotRequired[str]
    MaxResults: NotRequired[int]
    StreamCreationTimestamp: NotRequired[TimestampTypeDef]
    ShardFilter: NotRequired[ShardFilterTypeDef]
    StreamARN: NotRequired[str]
    StreamId: NotRequired[str]

class SubscribeToShardInputTypeDef(TypedDict):
    ConsumerARN: str
    ShardId: str
    StartingPosition: StartingPositionTypeDef
    StreamId: NotRequired[str]
    DryRun: NotRequired[bool]

class ListChannelsInputPaginateTypeDef(TypedDict):
    StreamFilter: NotRequired[Sequence[StreamFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListChannelsInputTypeDef(TypedDict):
    StreamFilter: NotRequired[Sequence[StreamFilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class S3TablesConfigurationOutputTypeDef(TypedDict):
    TableBucketARN: str
    Namespace: str
    TableName: str
    CompressionType: S3TablesCompressionTypeType
    PartitionSpec: NotRequired[PartitionSpecOutputTypeDef]

PartitionSpecUnionTypeDef = Union[PartitionSpecTypeDef, PartitionSpecOutputTypeDef]

class ListShardsOutputTypeDef(TypedDict):
    Shards: list[ShardTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class StreamDescriptionTypeDef(TypedDict):
    StreamName: str
    StreamARN: str
    StreamStatus: StreamStatusType
    Shards: list[ShardTypeDef]
    HasMoreShards: bool
    RetentionPeriodHours: int
    StreamCreationTimestamp: datetime
    EnhancedMonitoring: list[EnhancedMetricsTypeDef]
    StreamModeDetails: NotRequired[StreamModeDetailsTypeDef]
    EncryptionType: NotRequired[EncryptionTypeType]
    KeyId: NotRequired[str]

class DescribeStreamSummaryOutputTypeDef(TypedDict):
    StreamDescriptionSummary: StreamDescriptionSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class SubscribeToShardEventStreamTypeDef(TypedDict):
    SubscribeToShardEvent: SubscribeToShardEventTypeDef
    ResourceNotFoundException: NotRequired[ResourceNotFoundExceptionTypeDef]
    ResourceInUseException: NotRequired[ResourceInUseExceptionTypeDef]
    KMSDisabledException: NotRequired[KMSDisabledExceptionTypeDef]
    KMSInvalidStateException: NotRequired[KMSInvalidStateExceptionTypeDef]
    KMSAccessDeniedException: NotRequired[KMSAccessDeniedExceptionTypeDef]
    KMSNotFoundException: NotRequired[KMSNotFoundExceptionTypeDef]
    KMSOptInRequired: NotRequired[KMSOptInRequiredTypeDef]
    KMSThrottlingException: NotRequired[KMSThrottlingExceptionTypeDef]
    InternalFailureException: NotRequired[InternalFailureExceptionTypeDef]

class S3TablesDestinationDescriptionTypeDef(TypedDict):
    DataFreshnessInSeconds: int
    DeadLetterQueueS3Configuration: DeadLetterQueueS3ConfigurationTypeDef
    S3TablesConfigurationList: list[S3TablesConfigurationOutputTypeDef]

class S3TablesConfigurationTypeDef(TypedDict):
    TableBucketARN: str
    Namespace: str
    TableName: str
    CompressionType: S3TablesCompressionTypeType
    PartitionSpec: NotRequired[PartitionSpecUnionTypeDef]

class DescribeStreamOutputTypeDef(TypedDict):
    StreamDescription: StreamDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class SubscribeToShardOutputTypeDef(TypedDict):
    EventStream: EventStream[SubscribeToShardEventStreamTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ChannelDescriptionTypeDef(TypedDict):
    ChannelName: str
    ChannelARN: str
    ChannelId: str
    ChannelStatus: ChannelStatusType
    ChannelCreationTimestamp: datetime
    ServiceExecutionRoleARN: str
    StreamConfigurationList: list[ChannelStreamDescriptionTypeDef]
    LoggingConfiguration: ChannelLoggingConfigurationTypeDef
    ChannelStatusReason: NotRequired[str]
    S3DestinationConfiguration: NotRequired[S3DestinationDescriptionTypeDef]
    S3TablesDestinationConfiguration: NotRequired[S3TablesDestinationDescriptionTypeDef]
    EncryptionConfiguration: NotRequired[ChannelEncryptionConfigurationTypeDef]

S3TablesConfigurationUnionTypeDef = Union[
    S3TablesConfigurationTypeDef, S3TablesConfigurationOutputTypeDef
]

class CreateChannelOutputTypeDef(TypedDict):
    ChannelDescription: ChannelDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeChannelOutputTypeDef(TypedDict):
    ChannelDescription: ChannelDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateChannelOutputTypeDef(TypedDict):
    ChannelDescription: ChannelDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class S3TablesDestinationConfigurationTypeDef(TypedDict):
    DeadLetterQueueS3Configuration: DeadLetterQueueS3ConfigurationTypeDef
    S3TablesConfigurationList: Sequence[S3TablesConfigurationUnionTypeDef]
    DataFreshnessInSeconds: NotRequired[int]

class CreateChannelInputTypeDef(TypedDict):
    ChannelName: str
    ServiceExecutionRoleARN: str
    StreamConfigurationList: Sequence[ChannelStreamConfigurationTypeDef]
    S3DestinationConfiguration: NotRequired[S3DestinationConfigurationTypeDef]
    S3TablesDestinationConfiguration: NotRequired[S3TablesDestinationConfigurationTypeDef]
    EncryptionConfiguration: NotRequired[ChannelEncryptionConfigurationTypeDef]
    Tags: NotRequired[Mapping[str, str]]
    LoggingConfiguration: NotRequired[ChannelLoggingConfigurationTypeDef]
