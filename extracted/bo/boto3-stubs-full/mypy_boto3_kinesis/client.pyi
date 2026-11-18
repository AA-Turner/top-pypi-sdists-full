"""
Type annotations for kinesis service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_kinesis.client import KinesisClient

    session = Session()
    client: KinesisClient = session.client("kinesis")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    DescribeStreamPaginator,
    ListChannelsPaginator,
    ListQueuesPaginator,
    ListShardsPaginator,
    ListStreamConsumersPaginator,
    ListStreamsPaginator,
)
from .type_defs import (
    AcknowledgeDeadLetterQueueRecordsInputTypeDef,
    AcknowledgeDeadLetterQueueRecordsOutputTypeDef,
    AcknowledgeQueueRecordsInputTypeDef,
    AcknowledgeQueueRecordsOutputTypeDef,
    AddTagsToStreamInputTypeDef,
    CreateChannelInputTypeDef,
    CreateChannelOutputTypeDef,
    CreateQueueInputTypeDef,
    CreateQueueOutputTypeDef,
    CreateStreamInputTypeDef,
    DecreaseStreamRetentionPeriodInputTypeDef,
    DeleteChannelInputTypeDef,
    DeleteQueueInputTypeDef,
    DeleteResourcePolicyInputTypeDef,
    DeleteStreamInputTypeDef,
    DeregisterStreamConsumerInputTypeDef,
    DescribeAccountSettingsOutputTypeDef,
    DescribeChannelInputTypeDef,
    DescribeChannelOutputTypeDef,
    DescribeLimitsOutputTypeDef,
    DescribeQueueInputTypeDef,
    DescribeQueueOutputTypeDef,
    DescribeStreamConsumerInputTypeDef,
    DescribeStreamConsumerOutputTypeDef,
    DescribeStreamInputTypeDef,
    DescribeStreamOutputTypeDef,
    DescribeStreamSummaryInputTypeDef,
    DescribeStreamSummaryOutputTypeDef,
    DisableEnhancedMonitoringInputTypeDef,
    EmptyResponseMetadataTypeDef,
    EnableEnhancedMonitoringInputTypeDef,
    EnhancedMonitoringOutputTypeDef,
    GetRecordsInputTypeDef,
    GetRecordsOutputTypeDef,
    GetResourcePolicyInputTypeDef,
    GetResourcePolicyOutputTypeDef,
    GetShardIteratorInputTypeDef,
    GetShardIteratorOutputTypeDef,
    IncreaseStreamRetentionPeriodInputTypeDef,
    ListChannelsInputTypeDef,
    ListChannelsOutputTypeDef,
    ListQueuesInputTypeDef,
    ListQueuesOutputTypeDef,
    ListShardsInputTypeDef,
    ListShardsOutputTypeDef,
    ListStreamConsumersInputTypeDef,
    ListStreamConsumersOutputTypeDef,
    ListStreamsInputTypeDef,
    ListStreamsOutputTypeDef,
    ListTagsForResourceInputTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListTagsForStreamInputTypeDef,
    ListTagsForStreamOutputTypeDef,
    MergeShardsInputTypeDef,
    PutRecordInputTypeDef,
    PutRecordOutputTypeDef,
    PutRecordsInputTypeDef,
    PutRecordsOutputTypeDef,
    PutResourcePolicyInputTypeDef,
    ReceiveDeadLetterQueueRecordsInputTypeDef,
    ReceiveDeadLetterQueueRecordsOutputTypeDef,
    ReceiveQueueRecordsInputTypeDef,
    ReceiveQueueRecordsOutputTypeDef,
    RegisterStreamConsumerInputTypeDef,
    RegisterStreamConsumerOutputTypeDef,
    RemoveTagsFromStreamInputTypeDef,
    RestoreDeadLetterQueueRecordsInputTypeDef,
    RestoreDeadLetterQueueRecordsOutputTypeDef,
    SplitShardInputTypeDef,
    StartStreamEncryptionInputTypeDef,
    StopStreamEncryptionInputTypeDef,
    SubscribeToShardInputTypeDef,
    SubscribeToShardOutputTypeDef,
    TagResourceInputTypeDef,
    UntagResourceInputTypeDef,
    UpdateAccountSettingsInputTypeDef,
    UpdateAccountSettingsOutputTypeDef,
    UpdateChannelInputTypeDef,
    UpdateChannelOutputTypeDef,
    UpdateDeadLetterQueueRecordsVisibilityInputTypeDef,
    UpdateDeadLetterQueueRecordsVisibilityOutputTypeDef,
    UpdateMaxRecordSizeInputTypeDef,
    UpdateQueueInputTypeDef,
    UpdateQueueOutputTypeDef,
    UpdateQueueRecordsVisibilityInputTypeDef,
    UpdateQueueRecordsVisibilityOutputTypeDef,
    UpdateShardCountInputTypeDef,
    UpdateShardCountOutputTypeDef,
    UpdateStreamModeInputTypeDef,
    UpdateStreamRecordDistributionStrategyInputTypeDef,
    UpdateStreamWarmThroughputInputTypeDef,
    UpdateStreamWarmThroughputOutputTypeDef,
)
from .waiter import ChannelActiveWaiter, StreamExistsWaiter, StreamNotExistsWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("KinesisClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    DryRunOperationException: type[BotocoreClientError]
    ExpiredIteratorException: type[BotocoreClientError]
    ExpiredNextTokenException: type[BotocoreClientError]
    InternalFailureException: type[BotocoreClientError]
    InvalidArgumentException: type[BotocoreClientError]
    KMSAccessDeniedException: type[BotocoreClientError]
    KMSDisabledException: type[BotocoreClientError]
    KMSInvalidStateException: type[BotocoreClientError]
    KMSNotFoundException: type[BotocoreClientError]
    KMSOptInRequired: type[BotocoreClientError]
    KMSThrottlingException: type[BotocoreClientError]
    LimitExceededException: type[BotocoreClientError]
    ProvisionedThroughputExceededException: type[BotocoreClientError]
    ResourceInUseException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class KinesisClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html#Kinesis.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KinesisClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html#Kinesis.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#generate_presigned_url)
        """

    def acknowledge_dead_letter_queue_records(
        self, **kwargs: Unpack[AcknowledgeDeadLetterQueueRecordsInputTypeDef]
    ) -> AcknowledgeDeadLetterQueueRecordsOutputTypeDef:
        """
        Acknowledges up to 10 dead-letter records in the specified queue, so the queue
        doesn't return them again.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/acknowledge_dead_letter_queue_records.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#acknowledge_dead_letter_queue_records)
        """

    def acknowledge_queue_records(
        self, **kwargs: Unpack[AcknowledgeQueueRecordsInputTypeDef]
    ) -> AcknowledgeQueueRecordsOutputTypeDef:
        """
        Acknowledges up to 10 records from the specified queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/acknowledge_queue_records.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#acknowledge_queue_records)
        """

    def add_tags_to_stream(
        self, **kwargs: Unpack[AddTagsToStreamInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or updates tags for the specified Kinesis data stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/add_tags_to_stream.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#add_tags_to_stream)
        """

    def create_channel(
        self, **kwargs: Unpack[CreateChannelInputTypeDef]
    ) -> CreateChannelOutputTypeDef:
        """
        Creates a channel that delivers records from a Kinesis data stream to a
        destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/create_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#create_channel)
        """

    def create_queue(self, **kwargs: Unpack[CreateQueueInputTypeDef]) -> CreateQueueOutputTypeDef:
        """
        Creates a queue on the specified data stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/create_queue.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#create_queue)
        """

    def create_stream(
        self, **kwargs: Unpack[CreateStreamInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a Kinesis data stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/create_stream.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#create_stream)
        """

    def decrease_stream_retention_period(
        self, **kwargs: Unpack[DecreaseStreamRetentionPeriodInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Decreases the Kinesis data stream's retention period, which is the length of
        time data records are accessible after they are added to the stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/decrease_stream_retention_period.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#decrease_stream_retention_period)
        """

    def delete_channel(
        self, **kwargs: Unpack[DeleteChannelInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/delete_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#delete_channel)
        """

    def delete_queue(
        self, **kwargs: Unpack[DeleteQueueInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/delete_queue.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#delete_queue)
        """

    def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a policy for the specified data stream, consumer, or queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/delete_resource_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#delete_resource_policy)
        """

    def delete_stream(
        self, **kwargs: Unpack[DeleteStreamInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a Kinesis data stream and all its shards and data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/delete_stream.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#delete_stream)
        """

    def deregister_stream_consumer(
        self, **kwargs: Unpack[DeregisterStreamConsumerInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        To deregister a consumer, provide its ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/deregister_stream_consumer.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#deregister_stream_consumer)
        """

    def describe_account_settings(self) -> DescribeAccountSettingsOutputTypeDef:
        """
        Describes the account-level settings for Amazon Kinesis Data Streams.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/describe_account_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#describe_account_settings)
        """

    def describe_channel(
        self, **kwargs: Unpack[DescribeChannelInputTypeDef]
    ) -> DescribeChannelOutputTypeDef:
        """
        Describes the specified channel, including its configuration and current status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/describe_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#describe_channel)
        """

    def describe_limits(self) -> DescribeLimitsOutputTypeDef:
        """
        Describes the shard limits and usage for the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/describe_limits.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#describe_limits)
        """

    def describe_queue(
        self, **kwargs: Unpack[DescribeQueueInputTypeDef]
    ) -> DescribeQueueOutputTypeDef:
        """
        Returns a description of the specified queue, including its status, the data
        stream it delivers records from, and its configuration attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/describe_queue.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#describe_queue)
        """

    def describe_stream(
        self, **kwargs: Unpack[DescribeStreamInputTypeDef]
    ) -> DescribeStreamOutputTypeDef:
        """
        Describes the specified Kinesis data stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/describe_stream.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#describe_stream)
        """

    def describe_stream_consumer(
        self, **kwargs: Unpack[DescribeStreamConsumerInputTypeDef]
    ) -> DescribeStreamConsumerOutputTypeDef:
        """
        To get the description of a registered consumer, provide the ARN of the
        consumer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/describe_stream_consumer.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#describe_stream_consumer)
        """

    def describe_stream_summary(
        self, **kwargs: Unpack[DescribeStreamSummaryInputTypeDef]
    ) -> DescribeStreamSummaryOutputTypeDef:
        """
        Provides a summarized description of the specified Kinesis data stream without
        the shard list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/describe_stream_summary.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#describe_stream_summary)
        """

    def disable_enhanced_monitoring(
        self, **kwargs: Unpack[DisableEnhancedMonitoringInputTypeDef]
    ) -> EnhancedMonitoringOutputTypeDef:
        """
        Disables enhanced monitoring.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/disable_enhanced_monitoring.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#disable_enhanced_monitoring)
        """

    def enable_enhanced_monitoring(
        self, **kwargs: Unpack[EnableEnhancedMonitoringInputTypeDef]
    ) -> EnhancedMonitoringOutputTypeDef:
        """
        Enables enhanced Kinesis data stream monitoring for shard-level metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/enable_enhanced_monitoring.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#enable_enhanced_monitoring)
        """

    def get_records(self, **kwargs: Unpack[GetRecordsInputTypeDef]) -> GetRecordsOutputTypeDef:
        """
        Gets data records from a Kinesis data stream's shard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/get_records.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#get_records)
        """

    def get_resource_policy(
        self, **kwargs: Unpack[GetResourcePolicyInputTypeDef]
    ) -> GetResourcePolicyOutputTypeDef:
        """
        Returns a policy attached to the specified data stream, consumer, or queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/get_resource_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#get_resource_policy)
        """

    def get_shard_iterator(
        self, **kwargs: Unpack[GetShardIteratorInputTypeDef]
    ) -> GetShardIteratorOutputTypeDef:
        """
        Gets an Amazon Kinesis shard iterator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/get_shard_iterator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#get_shard_iterator)
        """

    def increase_stream_retention_period(
        self, **kwargs: Unpack[IncreaseStreamRetentionPeriodInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Increases the Kinesis data stream's retention period, which is the length of
        time data records are accessible after they are added to the stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/increase_stream_retention_period.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#increase_stream_retention_period)
        """

    def list_channels(
        self, **kwargs: Unpack[ListChannelsInputTypeDef]
    ) -> ListChannelsOutputTypeDef:
        """
        Lists the channels in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/list_channels.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#list_channels)
        """

    def list_queues(self, **kwargs: Unpack[ListQueuesInputTypeDef]) -> ListQueuesOutputTypeDef:
        """
        Returns a summary of each queue in the Amazon Web Services account and Region
        used by the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/list_queues.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#list_queues)
        """

    def list_shards(self, **kwargs: Unpack[ListShardsInputTypeDef]) -> ListShardsOutputTypeDef:
        """
        Lists the shards in a stream and provides information about each shard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/list_shards.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#list_shards)
        """

    def list_stream_consumers(
        self, **kwargs: Unpack[ListStreamConsumersInputTypeDef]
    ) -> ListStreamConsumersOutputTypeDef:
        """
        Lists the consumers registered to receive data from a stream using enhanced
        fan-out, and provides information about each consumer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/list_stream_consumers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#list_stream_consumers)
        """

    def list_streams(self, **kwargs: Unpack[ListStreamsInputTypeDef]) -> ListStreamsOutputTypeDef:
        """
        Lists your Kinesis data streams.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/list_streams.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#list_streams)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        List all tags added to the specified Kinesis resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#list_tags_for_resource)
        """

    def list_tags_for_stream(
        self, **kwargs: Unpack[ListTagsForStreamInputTypeDef]
    ) -> ListTagsForStreamOutputTypeDef:
        """
        Lists the tags for the specified Kinesis data stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/list_tags_for_stream.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#list_tags_for_stream)
        """

    def merge_shards(
        self, **kwargs: Unpack[MergeShardsInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Merges two adjacent shards in a Kinesis data stream and combines them into a
        single shard to reduce the stream's capacity to ingest and transport data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/merge_shards.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#merge_shards)
        """

    def put_record(self, **kwargs: Unpack[PutRecordInputTypeDef]) -> PutRecordOutputTypeDef:
        """
        Writes a single data record into an Amazon Kinesis data stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/put_record.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#put_record)
        """

    def put_records(self, **kwargs: Unpack[PutRecordsInputTypeDef]) -> PutRecordsOutputTypeDef:
        """
        Writes multiple data records into a Kinesis data stream in a single call (also
        referred to as a <code>PutRecords</code> request).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/put_records.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#put_records)
        """

    def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches a resource-based policy to a data stream, a queue, or an enhanced
        fan-out consumer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/put_resource_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#put_resource_policy)
        """

    def receive_dead_letter_queue_records(
        self, **kwargs: Unpack[ReceiveDeadLetterQueueRecordsInputTypeDef]
    ) -> ReceiveDeadLetterQueueRecordsOutputTypeDef:
        """
        Receives up to 10 dead-letter records from the specified queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/receive_dead_letter_queue_records.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#receive_dead_letter_queue_records)
        """

    def receive_queue_records(
        self, **kwargs: Unpack[ReceiveQueueRecordsInputTypeDef]
    ) -> ReceiveQueueRecordsOutputTypeDef:
        """
        Receives up to 10 records from the specified queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/receive_queue_records.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#receive_queue_records)
        """

    def register_stream_consumer(
        self, **kwargs: Unpack[RegisterStreamConsumerInputTypeDef]
    ) -> RegisterStreamConsumerOutputTypeDef:
        """
        Registers a consumer with a Kinesis data stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/register_stream_consumer.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#register_stream_consumer)
        """

    def remove_tags_from_stream(
        self, **kwargs: Unpack[RemoveTagsFromStreamInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes tags from the specified Kinesis data stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/remove_tags_from_stream.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#remove_tags_from_stream)
        """

    def restore_dead_letter_queue_records(
        self, **kwargs: Unpack[RestoreDeadLetterQueueRecordsInputTypeDef]
    ) -> RestoreDeadLetterQueueRecordsOutputTypeDef:
        """
        Restores up to 10 dead-letter records in the specified queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/restore_dead_letter_queue_records.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#restore_dead_letter_queue_records)
        """

    def split_shard(self, **kwargs: Unpack[SplitShardInputTypeDef]) -> EmptyResponseMetadataTypeDef:
        """
        Splits a shard into two new shards in the Kinesis data stream, to increase the
        stream's capacity to ingest and transport data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/split_shard.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#split_shard)
        """

    def start_stream_encryption(
        self, **kwargs: Unpack[StartStreamEncryptionInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables or updates server-side encryption using an Amazon Web Services KMS key
        for a specified stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/start_stream_encryption.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#start_stream_encryption)
        """

    def stop_stream_encryption(
        self, **kwargs: Unpack[StopStreamEncryptionInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disables server-side encryption for a specified stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/stop_stream_encryption.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#stop_stream_encryption)
        """

    def subscribe_to_shard(
        self, **kwargs: Unpack[SubscribeToShardInputTypeDef]
    ) -> SubscribeToShardOutputTypeDef:
        """
        This operation establishes an HTTP/2 connection between the consumer you
        specify in the <code>ConsumerARN</code> parameter and the shard you specify in
        the <code>ShardId</code> parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/subscribe_to_shard.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#subscribe_to_shard)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or updates tags for the specified Kinesis resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes tags from the specified Kinesis resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#untag_resource)
        """

    def update_account_settings(
        self, **kwargs: Unpack[UpdateAccountSettingsInputTypeDef]
    ) -> UpdateAccountSettingsOutputTypeDef:
        """
        Updates the account-level settings for Amazon Kinesis Data Streams.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/update_account_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#update_account_settings)
        """

    def update_channel(
        self, **kwargs: Unpack[UpdateChannelInputTypeDef]
    ) -> UpdateChannelOutputTypeDef:
        """
        Updates the data freshness interval or the Amazon CloudWatch Logs configuration
        of an existing channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/update_channel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#update_channel)
        """

    def update_dead_letter_queue_records_visibility(
        self, **kwargs: Unpack[UpdateDeadLetterQueueRecordsVisibilityInputTypeDef]
    ) -> UpdateDeadLetterQueueRecordsVisibilityOutputTypeDef:
        """
        Changes the visibility timeout of up to 10 dead-letter records that you have
        received from the specified queue but not yet acknowledged.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/update_dead_letter_queue_records_visibility.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#update_dead_letter_queue_records_visibility)
        """

    def update_max_record_size(
        self, **kwargs: Unpack[UpdateMaxRecordSizeInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This allows you to update the <code>MaxRecordSize</code> of a single record
        that you can write to, and read from a stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/update_max_record_size.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#update_max_record_size)
        """

    def update_queue(self, **kwargs: Unpack[UpdateQueueInputTypeDef]) -> UpdateQueueOutputTypeDef:
        """
        Updates the configuration attributes of the specified queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/update_queue.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#update_queue)
        """

    def update_queue_records_visibility(
        self, **kwargs: Unpack[UpdateQueueRecordsVisibilityInputTypeDef]
    ) -> UpdateQueueRecordsVisibilityOutputTypeDef:
        """
        Changes the visibility timeout of up to 10 records that you have received from
        the specified queue but not yet acknowledged.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/update_queue_records_visibility.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#update_queue_records_visibility)
        """

    def update_shard_count(
        self, **kwargs: Unpack[UpdateShardCountInputTypeDef]
    ) -> UpdateShardCountOutputTypeDef:
        """
        Updates the shard count of the specified stream to the specified number of
        shards.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/update_shard_count.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#update_shard_count)
        """

    def update_stream_mode(
        self, **kwargs: Unpack[UpdateStreamModeInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the capacity mode of the data stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/update_stream_mode.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#update_stream_mode)
        """

    def update_stream_record_distribution_strategy(
        self, **kwargs: Unpack[UpdateStreamRecordDistributionStrategyInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the record distribution strategy for the specified Amazon Kinesis Data
        Streams on-demand data stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/update_stream_record_distribution_strategy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#update_stream_record_distribution_strategy)
        """

    def update_stream_warm_throughput(
        self, **kwargs: Unpack[UpdateStreamWarmThroughputInputTypeDef]
    ) -> UpdateStreamWarmThroughputOutputTypeDef:
        """
        Updates the warm throughput configuration for the specified Amazon Kinesis Data
        Streams on-demand data stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/update_stream_warm_throughput.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#update_stream_warm_throughput)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_stream"]
    ) -> DescribeStreamPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_channels"]
    ) -> ListChannelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_queues"]
    ) -> ListQueuesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_shards"]
    ) -> ListShardsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_stream_consumers"]
    ) -> ListStreamConsumersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_streams"]
    ) -> ListStreamsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["channel_active"]
    ) -> ChannelActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["stream_exists"]
    ) -> StreamExistsWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["stream_not_exists"]
    ) -> StreamNotExistsWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis/client/#get_waiter)
        """
