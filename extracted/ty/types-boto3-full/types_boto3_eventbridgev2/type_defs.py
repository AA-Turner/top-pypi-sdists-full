"""
Type annotations for eventbridgev2 service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_eventbridgev2/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_eventbridgev2.type_defs import OnFailureConfigurationTypeDef

    data: OnFailureConfigurationTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import IO, Any, Union

from botocore.response import StreamingBody

from .literals import (
    BusStateType,
    EventSourceStateType,
    EventSourceTypeType,
    FilterScopeType,
    IncludePayloadType,
    InvocationTypeType,
    LogLevelType,
    OrderingTypeType,
    PointTypeType,
    ResumePositionType,
    StartingPositionType,
    SubscriberStateType,
    SuccessCodeType,
    TransformerTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AwsServiceEventsSourceConfigurationTypeDef",
    "BatchConfigurationTypeDef",
    "BlobTypeDef",
    "ConfluentPublicRegistryConfigurationTypeDef",
    "CreateEventBusRequestTypeDef",
    "CreateEventBusResponseTypeDef",
    "CreateEventSourceRequestTypeDef",
    "CreateEventSourceResponseTypeDef",
    "CreateSubscriberRequestTypeDef",
    "CreateSubscriberResponseTypeDef",
    "DeduplicationConfigurationTypeDef",
    "DeleteEventBusRequestTypeDef",
    "DeleteEventSourceRequestTypeDef",
    "DeleteResourcePolicyRequestTypeDef",
    "DeleteResourcePolicyResponseTypeDef",
    "DeleteSubscriberRequestTypeDef",
    "DescribeEventBusRequestTypeDef",
    "DescribeEventBusRequestWaitExtraTypeDef",
    "DescribeEventBusRequestWaitTypeDef",
    "DescribeEventBusResponseTypeDef",
    "DescribeEventSourceRequestTypeDef",
    "DescribeEventSourceResponseTypeDef",
    "DescribeSubscriberRequestTypeDef",
    "DescribeSubscriberResponseTypeDef",
    "EncryptionConfigurationTypeDef",
    "EventBusSummaryTypeDef",
    "EventBusV2ParametersOutputTypeDef",
    "EventBusV2ParametersTypeDef",
    "EventBusV2ParametersUnionTypeDef",
    "EventBusV2SystemMetadataTypeDef",
    "EventSourceConfigurationTypeDef",
    "EventSourceSummaryTypeDef",
    "FilterConfigurationOutputTypeDef",
    "FilterConfigurationTypeDef",
    "FilterConfigurationUnionTypeDef",
    "FilterTypeDef",
    "GetResourcePolicyRequestTypeDef",
    "GetResourcePolicyResponseTypeDef",
    "HttpParametersOutputTypeDef",
    "HttpParametersTypeDef",
    "HttpParametersUnionTypeDef",
    "InvokeConfigurationOutputTypeDef",
    "InvokeConfigurationTypeDef",
    "InvokeConfigurationUnionTypeDef",
    "JsonataConfigurationTypeDef",
    "KinesisParametersTypeDef",
    "LambdaParametersTypeDef",
    "ListEventBusesRequestPaginateTypeDef",
    "ListEventBusesRequestTypeDef",
    "ListEventBusesResponseTypeDef",
    "ListEventSourcesRequestPaginateTypeDef",
    "ListEventSourcesRequestTypeDef",
    "ListEventSourcesResponseTypeDef",
    "ListResourcePoliciesRequestPaginateTypeDef",
    "ListResourcePoliciesRequestTypeDef",
    "ListResourcePoliciesResponseTypeDef",
    "ListSubscribersRequestPaginateTypeDef",
    "ListSubscribersRequestTypeDef",
    "ListSubscribersResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LogConfigurationTypeDef",
    "OnFailureConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "PartnerEventsSourceConfigurationTypeDef",
    "PointInTimeConfigurationOutputTypeDef",
    "PointInTimeConfigurationTypeDef",
    "PointInTimeConfigurationUnionTypeDef",
    "PutEventsRequestEntryTypeDef",
    "PutEventsRequestTypeDef",
    "PutEventsResponseTypeDef",
    "PutEventsResultEntryTypeDef",
    "PutEventsSystemMetadataTypeDef",
    "PutRawEventsRequestEntryTypeDef",
    "PutRawEventsRequestTypeDef",
    "PutRawEventsResponseTypeDef",
    "PutRawEventsResultEntryTypeDef",
    "PutRawEventsSystemMetadataTypeDef",
    "PutResourcePolicyRequestTypeDef",
    "PutResourcePolicyResponseTypeDef",
    "ResourcePolicySummaryTypeDef",
    "ResponseMetadataTypeDef",
    "RetryPolicyTypeDef",
    "RevokeResourceRequestTypeDef",
    "RevokeResourceResponseTypeDef",
    "SchemaRegistryConfigurationTypeDef",
    "SnsMessageAttributeValueTypeDef",
    "SnsParametersOutputTypeDef",
    "SnsParametersTypeDef",
    "SnsParametersUnionTypeDef",
    "SqsMessageAttributeValueTypeDef",
    "SqsParametersOutputTypeDef",
    "SqsParametersTypeDef",
    "SqsParametersUnionTypeDef",
    "StepFunctionsParametersTypeDef",
    "StorageConfigurationOutputTypeDef",
    "StorageConfigurationTypeDef",
    "SubscriberSummaryTypeDef",
    "TagResourceRequestTypeDef",
    "TimestampTypeDef",
    "TransformerTypeDef",
    "UniversalTargetParametersTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateEventBusRequestTypeDef",
    "UpdateEventBusResponseTypeDef",
    "UpdateEventSourceRequestTypeDef",
    "UpdateEventSourceResponseTypeDef",
    "UpdateInvokeConfigurationTypeDef",
    "UpdateSubscriberRequestTypeDef",
    "UpdateSubscriberResponseTypeDef",
    "WaiterConfigTypeDef",
)


class OnFailureConfigurationTypeDef(TypedDict):
    Arn: NotRequired[str]


class BatchConfigurationTypeDef(TypedDict):
    MaxBatchSize: NotRequired[int]
    MaxBatchWindowInSeconds: NotRequired[int]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class ConfluentPublicRegistryConfigurationTypeDef(TypedDict):
    ConnectionArn: str


class EncryptionConfigurationTypeDef(TypedDict):
    KmsKeyIdentifier: NotRequired[str]


class StorageConfigurationTypeDef(TypedDict):
    RetentionPeriodInDays: NotRequired[int]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class StorageConfigurationOutputTypeDef(TypedDict):
    RetentionPeriodInDays: NotRequired[int]
    RetentionWindowStartTime: NotRequired[datetime]


class LogConfigurationTypeDef(TypedDict):
    Level: NotRequired[LogLevelType]
    IncludePayload: NotRequired[IncludePayloadType]


class RetryPolicyTypeDef(TypedDict):
    MaxRetryAttempts: NotRequired[int]
    MaxEventAgeInSeconds: NotRequired[int]
    RetryStrategy: NotRequired[Literal["ALL"]]


class PointInTimeConfigurationOutputTypeDef(TypedDict):
    PointType: PointTypeType
    StartingPoint: NotRequired[datetime]
    EndPoint: NotRequired[datetime]


class DeduplicationConfigurationTypeDef(TypedDict):
    DeduplicationType: Literal["CONTENT_BASED"]


class DeleteEventBusRequestTypeDef(TypedDict):
    EventBusArn: str


class DeleteEventSourceRequestTypeDef(TypedDict):
    EventSourceArn: str


class DeleteResourcePolicyRequestTypeDef(TypedDict):
    ResourceArn: str
    PolicyName: NotRequired[str]
    ExpectedRevisionId: NotRequired[str]


class DeleteSubscriberRequestTypeDef(TypedDict):
    SubscriberArn: str


class DescribeEventBusRequestTypeDef(TypedDict):
    EventBusArn: str


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class DescribeEventSourceRequestTypeDef(TypedDict):
    EventSourceArn: str


class DescribeSubscriberRequestTypeDef(TypedDict):
    SubscriberArn: str


class EventBusSummaryTypeDef(TypedDict):
    Name: NotRequired[str]
    EventBusArn: NotRequired[str]
    Description: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    State: NotRequired[BusStateType]
    StateReason: NotRequired[str]
    EventBusAccountId: NotRequired[str]


class EventBusV2SystemMetadataTypeDef(TypedDict):
    EventGroupId: NotRequired[str]
    DeduplicationId: NotRequired[str]


EventSourceSummaryTypeDef = TypedDict(
    "EventSourceSummaryTypeDef",
    {
        "EventSourceArn": NotRequired[str],
        "Name": NotRequired[str],
        "EventBusArn": NotRequired[str],
        "Type": NotRequired[EventSourceTypeType],
        "State": NotRequired[EventSourceStateType],
        "Revoked": NotRequired[bool],
        "CreationTime": NotRequired[datetime],
        "LastModifiedTime": NotRequired[datetime],
        "EventSourceAccountId": NotRequired[str],
    },
)


class FilterTypeDef(TypedDict):
    Pattern: str
    Scope: FilterScopeType


class GetResourcePolicyRequestTypeDef(TypedDict):
    ResourceArn: str
    PolicyName: NotRequired[str]


class HttpParametersOutputTypeDef(TypedDict):
    PathParameterValues: NotRequired[list[str]]
    HeaderParameters: NotRequired[dict[str, str]]
    QueryStringParameters: NotRequired[dict[str, str]]
    InvocationTimeoutSeconds: NotRequired[str]


class HttpParametersTypeDef(TypedDict):
    PathParameterValues: NotRequired[Sequence[str]]
    HeaderParameters: NotRequired[Mapping[str, str]]
    QueryStringParameters: NotRequired[Mapping[str, str]]
    InvocationTimeoutSeconds: NotRequired[str]


class KinesisParametersTypeDef(TypedDict):
    PartitionKey: NotRequired[str]
    ExplicitHashKey: NotRequired[str]


class LambdaParametersTypeDef(TypedDict):
    InvocationType: NotRequired[InvocationTypeType]
    Qualifier: NotRequired[str]
    DurableExecutionName: NotRequired[str]
    TenantId: NotRequired[str]
    InvocationTimeoutSeconds: NotRequired[str]


class StepFunctionsParametersTypeDef(TypedDict):
    InvocationType: NotRequired[InvocationTypeType]
    Name: NotRequired[str]
    TraceHeader: NotRequired[str]
    InvocationTimeoutSeconds: NotRequired[str]


class UniversalTargetParametersTypeDef(TypedDict):
    Input: str
    InvocationTimeoutSeconds: NotRequired[str]


class JsonataConfigurationTypeDef(TypedDict):
    Expression: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListEventBusesRequestTypeDef(TypedDict):
    NamePrefix: NotRequired[str]
    EventBusAccountId: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListEventSourcesRequestTypeDef(TypedDict):
    EventBusArn: NotRequired[str]
    NamePrefix: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListResourcePoliciesRequestTypeDef(TypedDict):
    ResourceArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ResourcePolicySummaryTypeDef(TypedDict):
    PolicyName: str
    RevisionId: str


class ListSubscribersRequestTypeDef(TypedDict):
    EventBusArn: NotRequired[str]
    NamePrefix: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


SubscriberSummaryTypeDef = TypedDict(
    "SubscriberSummaryTypeDef",
    {
        "SubscriberArn": NotRequired[str],
        "Name": NotRequired[str],
        "EventBusArn": NotRequired[str],
        "TargetArn": NotRequired[str],
        "Type": NotRequired[OrderingTypeType],
        "Revoked": NotRequired[bool],
        "State": NotRequired[SubscriberStateType],
        "CreationTime": NotRequired[datetime],
        "LastModifiedTime": NotRequired[datetime],
        "SubscriberAccountId": NotRequired[str],
    },
)


class ListTagsForResourceRequestTypeDef(TypedDict):
    ResourceArn: str


TimestampTypeDef = Union[datetime, str]


class PutEventsSystemMetadataTypeDef(TypedDict):
    EventGroupId: NotRequired[str]
    DeduplicationId: NotRequired[str]


class PutEventsResultEntryTypeDef(TypedDict):
    EventId: NotRequired[str]
    SequenceNumber: NotRequired[str]
    SuccessCode: NotRequired[SuccessCodeType]
    ErrorCode: NotRequired[str]
    ErrorMessage: NotRequired[str]


class PutRawEventsSystemMetadataTypeDef(TypedDict):
    ContentType: str
    DeduplicationId: NotRequired[str]
    EventGroupId: NotRequired[str]


class PutRawEventsResultEntryTypeDef(TypedDict):
    EventId: NotRequired[str]
    SequenceNumber: NotRequired[str]
    SuccessCode: NotRequired[SuccessCodeType]
    ErrorCode: NotRequired[str]
    ErrorMessage: NotRequired[str]


class PutResourcePolicyRequestTypeDef(TypedDict):
    ResourceArn: str
    PolicyDocument: str
    PolicyName: NotRequired[str]
    ExpectedRevisionId: NotRequired[str]


class RevokeResourceRequestTypeDef(TypedDict):
    Arn: str


class SnsMessageAttributeValueTypeDef(TypedDict):
    DataType: NotRequired[str]
    StringValue: NotRequired[str]
    BinaryValue: NotRequired[str]


class SqsMessageAttributeValueTypeDef(TypedDict):
    DataType: NotRequired[str]
    StringValue: NotRequired[str]
    BinaryValue: NotRequired[str]


class TagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]


class UntagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class AwsServiceEventsSourceConfigurationTypeDef(TypedDict):
    AwsService: str
    Pattern: NotRequired[str]
    OnFailureConfiguration: NotRequired[OnFailureConfigurationTypeDef]


class PartnerEventsSourceConfigurationTypeDef(TypedDict):
    PartnerEventSourceArn: str
    Pattern: NotRequired[str]
    PartnerBusKmsKeyIdentifier: NotRequired[str]
    OnFailureConfiguration: NotRequired[OnFailureConfigurationTypeDef]


class SchemaRegistryConfigurationTypeDef(TypedDict):
    RegistryUri: str
    ConfluentPublicRegistryConfiguration: NotRequired[ConfluentPublicRegistryConfigurationTypeDef]


class CreateEventBusRequestTypeDef(TypedDict):
    Name: str
    Description: NotRequired[str]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]
    StorageConfiguration: NotRequired[StorageConfigurationTypeDef]
    Tags: NotRequired[Mapping[str, str]]
    ClientToken: NotRequired[str]


class UpdateEventBusRequestTypeDef(TypedDict):
    EventBusArn: str
    Description: NotRequired[str]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]
    StorageConfiguration: NotRequired[StorageConfigurationTypeDef]


class CreateEventSourceResponseTypeDef(TypedDict):
    EventSourceArn: str
    Name: str
    EventBusArn: str
    State: EventSourceStateType
    CreationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteResourcePolicyResponseTypeDef(TypedDict):
    RevisionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetResourcePolicyResponseTypeDef(TypedDict):
    ResourceArn: str
    PolicyDocument: str
    PolicyName: str
    RevisionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class PutResourcePolicyResponseTypeDef(TypedDict):
    ResourceArn: str
    PolicyName: str
    RevisionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class RevokeResourceResponseTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateEventSourceResponseTypeDef(TypedDict):
    EventSourceArn: str
    Name: str
    EventBusArn: str
    State: EventSourceStateType
    LastModifiedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CreateEventBusResponseTypeDef(TypedDict):
    EventBusArn: str
    Name: str
    Description: str
    EncryptionConfiguration: EncryptionConfigurationTypeDef
    StorageConfiguration: StorageConfigurationOutputTypeDef
    State: BusStateType
    StateReason: str
    CreationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeEventBusResponseTypeDef(TypedDict):
    EventBusArn: str
    Name: str
    Description: str
    EncryptionConfiguration: EncryptionConfigurationTypeDef
    StorageConfiguration: StorageConfigurationOutputTypeDef
    CreationTime: datetime
    LastModifiedTime: datetime
    State: BusStateType
    StateReason: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateEventBusResponseTypeDef(TypedDict):
    EventBusArn: str
    Name: str
    Description: str
    EncryptionConfiguration: EncryptionConfigurationTypeDef
    StorageConfiguration: StorageConfigurationOutputTypeDef
    State: BusStateType
    StateReason: str
    LastModifiedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


CreateSubscriberResponseTypeDef = TypedDict(
    "CreateSubscriberResponseTypeDef",
    {
        "SubscriberArn": str,
        "Name": str,
        "EventBusArn": str,
        "Type": OrderingTypeType,
        "StartingPosition": StartingPositionType,
        "PointInTimeConfiguration": PointInTimeConfigurationOutputTypeDef,
        "State": SubscriberStateType,
        "CreationTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateSubscriberResponseTypeDef = TypedDict(
    "UpdateSubscriberResponseTypeDef",
    {
        "SubscriberArn": str,
        "Name": str,
        "EventBusArn": str,
        "Type": OrderingTypeType,
        "StartingPosition": StartingPositionType,
        "PointInTimeConfiguration": PointInTimeConfigurationOutputTypeDef,
        "State": SubscriberStateType,
        "LastModifiedTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class DescribeEventBusRequestWaitExtraTypeDef(TypedDict):
    EventBusArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeEventBusRequestWaitTypeDef(TypedDict):
    EventBusArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class ListEventBusesResponseTypeDef(TypedDict):
    EventBuses: list[EventBusSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class EventBusV2ParametersOutputTypeDef(TypedDict):
    Metadata: NotRequired[dict[str, str]]
    SystemMetadata: NotRequired[EventBusV2SystemMetadataTypeDef]
    DeduplicationConfiguration: NotRequired[DeduplicationConfigurationTypeDef]


class EventBusV2ParametersTypeDef(TypedDict):
    Metadata: NotRequired[Mapping[str, str]]
    SystemMetadata: NotRequired[EventBusV2SystemMetadataTypeDef]
    DeduplicationConfiguration: NotRequired[DeduplicationConfigurationTypeDef]


class ListEventSourcesResponseTypeDef(TypedDict):
    EventSources: list[EventSourceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class FilterConfigurationOutputTypeDef(TypedDict):
    Language: NotRequired[Literal["EVENT_BRIDGE_PATTERN"]]
    Filters: NotRequired[list[FilterTypeDef]]


class FilterConfigurationTypeDef(TypedDict):
    Language: NotRequired[Literal["EVENT_BRIDGE_PATTERN"]]
    Filters: NotRequired[Sequence[FilterTypeDef]]


HttpParametersUnionTypeDef = Union[HttpParametersTypeDef, HttpParametersOutputTypeDef]
TransformerTypeDef = TypedDict(
    "TransformerTypeDef",
    {
        "Type": NotRequired[TransformerTypeType],
        "JsonataConfiguration": NotRequired[JsonataConfigurationTypeDef],
    },
)


class ListEventBusesRequestPaginateTypeDef(TypedDict):
    NamePrefix: NotRequired[str]
    EventBusAccountId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEventSourcesRequestPaginateTypeDef(TypedDict):
    EventBusArn: NotRequired[str]
    NamePrefix: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResourcePoliciesRequestPaginateTypeDef(TypedDict):
    ResourceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSubscribersRequestPaginateTypeDef(TypedDict):
    EventBusArn: NotRequired[str]
    NamePrefix: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResourcePoliciesResponseTypeDef(TypedDict):
    PolicySummaries: list[ResourcePolicySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListSubscribersResponseTypeDef(TypedDict):
    Subscribers: list[SubscriberSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PointInTimeConfigurationTypeDef(TypedDict):
    PointType: PointTypeType
    StartingPoint: NotRequired[TimestampTypeDef]
    EndPoint: NotRequired[TimestampTypeDef]


class PutEventsRequestEntryTypeDef(TypedDict):
    Source: str
    DetailType: str
    Detail: NotRequired[str]
    Resources: NotRequired[Sequence[str]]
    Time: NotRequired[TimestampTypeDef]
    SystemMetadata: NotRequired[PutEventsSystemMetadataTypeDef]


class PutEventsResponseTypeDef(TypedDict):
    FailedEntryCount: int
    Entries: list[PutEventsResultEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class PutRawEventsRequestEntryTypeDef(TypedDict):
    Data: BlobTypeDef
    SystemMetadata: PutRawEventsSystemMetadataTypeDef
    Metadata: NotRequired[Mapping[str, str]]


class PutRawEventsResponseTypeDef(TypedDict):
    FailedEntryCount: int
    Entries: list[PutRawEventsResultEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class SnsParametersOutputTypeDef(TypedDict):
    MessageGroupId: NotRequired[str]
    MessageDeduplicationId: NotRequired[str]
    Subject: NotRequired[str]
    MessageStructure: NotRequired[str]
    MessageAttributes: NotRequired[dict[str, SnsMessageAttributeValueTypeDef]]


class SnsParametersTypeDef(TypedDict):
    MessageGroupId: NotRequired[str]
    MessageDeduplicationId: NotRequired[str]
    Subject: NotRequired[str]
    MessageStructure: NotRequired[str]
    MessageAttributes: NotRequired[Mapping[str, SnsMessageAttributeValueTypeDef]]


class SqsParametersOutputTypeDef(TypedDict):
    MessageGroupId: NotRequired[str]
    MessageDeduplicationId: NotRequired[str]
    DelaySeconds: NotRequired[str]
    MessageAttributes: NotRequired[dict[str, SqsMessageAttributeValueTypeDef]]
    MessageSystemAttributes: NotRequired[dict[str, SqsMessageAttributeValueTypeDef]]


class SqsParametersTypeDef(TypedDict):
    MessageGroupId: NotRequired[str]
    MessageDeduplicationId: NotRequired[str]
    DelaySeconds: NotRequired[str]
    MessageAttributes: NotRequired[Mapping[str, SqsMessageAttributeValueTypeDef]]
    MessageSystemAttributes: NotRequired[Mapping[str, SqsMessageAttributeValueTypeDef]]


class EventSourceConfigurationTypeDef(TypedDict):
    AwsServiceEventsConfiguration: NotRequired[AwsServiceEventsSourceConfigurationTypeDef]
    PartnerEventsConfiguration: NotRequired[PartnerEventsSourceConfigurationTypeDef]


EventBusV2ParametersUnionTypeDef = Union[
    EventBusV2ParametersTypeDef, EventBusV2ParametersOutputTypeDef
]
FilterConfigurationUnionTypeDef = Union[
    FilterConfigurationTypeDef, FilterConfigurationOutputTypeDef
]
PointInTimeConfigurationUnionTypeDef = Union[
    PointInTimeConfigurationTypeDef, PointInTimeConfigurationOutputTypeDef
]


class PutEventsRequestTypeDef(TypedDict):
    EventBusArn: str
    Entries: Sequence[PutEventsRequestEntryTypeDef]
    DeduplicationConfiguration: NotRequired[DeduplicationConfigurationTypeDef]


class PutRawEventsRequestTypeDef(TypedDict):
    EventBusArn: str
    Entries: Sequence[PutRawEventsRequestEntryTypeDef]
    SchemaRegistryConfiguration: NotRequired[SchemaRegistryConfigurationTypeDef]
    DeduplicationConfiguration: NotRequired[DeduplicationConfigurationTypeDef]


SnsParametersUnionTypeDef = Union[SnsParametersTypeDef, SnsParametersOutputTypeDef]


class InvokeConfigurationOutputTypeDef(TypedDict):
    RoleArn: str
    TargetArn: str
    LambdaParameters: NotRequired[LambdaParametersTypeDef]
    SqsParameters: NotRequired[SqsParametersOutputTypeDef]
    SnsParameters: NotRequired[SnsParametersOutputTypeDef]
    KinesisParameters: NotRequired[KinesisParametersTypeDef]
    StepFunctionsParameters: NotRequired[StepFunctionsParametersTypeDef]
    HttpParameters: NotRequired[HttpParametersOutputTypeDef]
    UniversalTargetParameters: NotRequired[UniversalTargetParametersTypeDef]
    EventBusV2Parameters: NotRequired[EventBusV2ParametersOutputTypeDef]


class InvokeConfigurationTypeDef(TypedDict):
    RoleArn: str
    TargetArn: str
    LambdaParameters: NotRequired[LambdaParametersTypeDef]
    SqsParameters: NotRequired[SqsParametersTypeDef]
    SnsParameters: NotRequired[SnsParametersTypeDef]
    KinesisParameters: NotRequired[KinesisParametersTypeDef]
    StepFunctionsParameters: NotRequired[StepFunctionsParametersTypeDef]
    HttpParameters: NotRequired[HttpParametersTypeDef]
    UniversalTargetParameters: NotRequired[UniversalTargetParametersTypeDef]
    EventBusV2Parameters: NotRequired[EventBusV2ParametersTypeDef]


SqsParametersUnionTypeDef = Union[SqsParametersTypeDef, SqsParametersOutputTypeDef]


class CreateEventSourceRequestTypeDef(TypedDict):
    Name: str
    EventBusArn: str
    Configuration: EventSourceConfigurationTypeDef
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    ClientToken: NotRequired[str]


class DescribeEventSourceResponseTypeDef(TypedDict):
    EventSourceArn: str
    Name: str
    EventBusArn: str
    Configuration: EventSourceConfigurationTypeDef
    Description: str
    State: EventSourceStateType
    Revoked: bool
    CreationTime: datetime
    LastModifiedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateEventSourceRequestTypeDef(TypedDict):
    EventSourceArn: str
    Configuration: NotRequired[EventSourceConfigurationTypeDef]
    Description: NotRequired[str]


DescribeSubscriberResponseTypeDef = TypedDict(
    "DescribeSubscriberResponseTypeDef",
    {
        "SubscriberArn": str,
        "Name": str,
        "EventBusArn": str,
        "InvokeConfiguration": InvokeConfigurationOutputTypeDef,
        "Description": str,
        "FilterConfiguration": FilterConfigurationOutputTypeDef,
        "Type": OrderingTypeType,
        "StartingPosition": StartingPositionType,
        "PointInTimeConfiguration": PointInTimeConfigurationOutputTypeDef,
        "BatchConfiguration": BatchConfigurationTypeDef,
        "Transformer": TransformerTypeDef,
        "RetryPolicy": RetryPolicyTypeDef,
        "OnFailureConfiguration": OnFailureConfigurationTypeDef,
        "LogConfiguration": LogConfigurationTypeDef,
        "State": SubscriberStateType,
        "Revoked": bool,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
InvokeConfigurationUnionTypeDef = Union[
    InvokeConfigurationTypeDef, InvokeConfigurationOutputTypeDef
]


class UpdateInvokeConfigurationTypeDef(TypedDict):
    RoleArn: str
    LambdaParameters: NotRequired[LambdaParametersTypeDef]
    SqsParameters: NotRequired[SqsParametersUnionTypeDef]
    SnsParameters: NotRequired[SnsParametersUnionTypeDef]
    KinesisParameters: NotRequired[KinesisParametersTypeDef]
    StepFunctionsParameters: NotRequired[StepFunctionsParametersTypeDef]
    HttpParameters: NotRequired[HttpParametersUnionTypeDef]
    UniversalTargetParameters: NotRequired[UniversalTargetParametersTypeDef]
    EventBusV2Parameters: NotRequired[EventBusV2ParametersUnionTypeDef]


CreateSubscriberRequestTypeDef = TypedDict(
    "CreateSubscriberRequestTypeDef",
    {
        "Name": str,
        "EventBusArn": str,
        "InvokeConfiguration": InvokeConfigurationUnionTypeDef,
        "Description": NotRequired[str],
        "FilterConfiguration": NotRequired[FilterConfigurationUnionTypeDef],
        "Type": NotRequired[OrderingTypeType],
        "StartingPosition": NotRequired[StartingPositionType],
        "PointInTimeConfiguration": NotRequired[PointInTimeConfigurationUnionTypeDef],
        "BatchConfiguration": NotRequired[BatchConfigurationTypeDef],
        "Transformer": NotRequired[TransformerTypeDef],
        "RetryPolicy": NotRequired[RetryPolicyTypeDef],
        "OnFailureConfiguration": NotRequired[OnFailureConfigurationTypeDef],
        "LogConfiguration": NotRequired[LogConfigurationTypeDef],
        "State": NotRequired[SubscriberStateType],
        "Tags": NotRequired[Mapping[str, str]],
        "ClientToken": NotRequired[str],
    },
)


class UpdateSubscriberRequestTypeDef(TypedDict):
    SubscriberArn: str
    Description: NotRequired[str]
    State: NotRequired[SubscriberStateType]
    ResumePosition: NotRequired[ResumePositionType]
    InvokeConfiguration: NotRequired[UpdateInvokeConfigurationTypeDef]
    FilterConfiguration: NotRequired[FilterConfigurationUnionTypeDef]
    BatchConfiguration: NotRequired[BatchConfigurationTypeDef]
    Transformer: NotRequired[TransformerTypeDef]
    RetryPolicy: NotRequired[RetryPolicyTypeDef]
    OnFailureConfiguration: NotRequired[OnFailureConfigurationTypeDef]
    LogConfiguration: NotRequired[LogConfigurationTypeDef]
