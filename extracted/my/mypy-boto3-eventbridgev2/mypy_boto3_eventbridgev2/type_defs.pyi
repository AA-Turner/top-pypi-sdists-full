"""
Type annotations for eventbridgev2 service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_eventbridgev2/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_eventbridgev2.type_defs import OnFailureConfigurationTypeDef

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
    ConnectivityStateType,
    EventSourceStateType,
    EventSourceTypeType,
    FilterScopeType,
    IncludePayloadType,
    InvocationTypeType,
    LogLevelType,
    MskAcksType,
    MskCompressionType,
    MskConnectivityType,
    OrderingTypeType,
    PointTypeType,
    ResumePositionType,
    StartingPositionType,
    SubscriberStateType,
    SuccessCodeType,
    TransformerTypeType,
    WebhookHmacAlgorithmType,
    WebhookHmacEncodingType,
    WebhookSecretEncodingType,
    WebhookSignedMessageCompositionType,
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
    "DescribeSubscriberRequestWaitTypeDef",
    "DescribeSubscriberResponseTypeDef",
    "EncryptionConfigurationTypeDef",
    "EventBusSummaryTypeDef",
    "EventBusV2ParametersOutputTypeDef",
    "EventBusV2ParametersTypeDef",
    "EventBusV2ParametersUnionTypeDef",
    "EventBusV2SystemMetadataTypeDef",
    "EventSourceConfigurationOutputTypeDef",
    "EventSourceConfigurationTypeDef",
    "EventSourceConfigurationUnionTypeDef",
    "EventSourceDetailsTypeDef",
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
    "MskDetailsTypeDef",
    "MskHeaderTypeDef",
    "MskParametersOutputTypeDef",
    "MskParametersTypeDef",
    "MskParametersUnionTypeDef",
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
    "RotateWebhookCredentialsRequestTypeDef",
    "RotateWebhookCredentialsResponseTypeDef",
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
    "SubscriberDetailsTypeDef",
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
    "WebhookAuthConfigurationTypeDef",
    "WebhookBasicHttpAuthConfigurationTypeDef",
    "WebhookCredentialTypeDef",
    "WebhookDeduplicationConfigurationTypeDef",
    "WebhookDetailsTypeDef",
    "WebhookEventsSourceConfigurationOutputTypeDef",
    "WebhookEventsSourceConfigurationTypeDef",
    "WebhookHmacAuthConfigurationTypeDef",
    "WebhookStaticTokenAuthConfigurationTypeDef",
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

class WebhookDetailsTypeDef(TypedDict):
    WebhookUrl: NotRequired[str]
    SecretArn: NotRequired[str]

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

class MskDetailsTypeDef(TypedDict):
    ConnectivityState: NotRequired[ConnectivityStateType]
    StateReason: NotRequired[str]
    VpcConnectionArn: NotRequired[str]

class MskHeaderTypeDef(TypedDict):
    Key: str
    Value: NotRequired[str]

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

class WebhookCredentialTypeDef(TypedDict):
    StaticTokenSecretValue: NotRequired[str]
    BasicHttpPassword: NotRequired[str]
    HmacSecretValue: NotRequired[str]

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

class WebhookBasicHttpAuthConfigurationTypeDef(TypedDict):
    Username: NotRequired[str]
    Password: NotRequired[str]

class WebhookHmacAuthConfigurationTypeDef(TypedDict):
    Algorithm: WebhookHmacAlgorithmType
    Encoding: WebhookHmacEncodingType
    SignatureHttpHeader: str
    SignedMessageComposition: WebhookSignedMessageCompositionType
    SignaturePrefix: NotRequired[str]
    Delimiter: NotRequired[str]
    TimestampHttpHeader: NotRequired[str]
    TimestampPrefix: NotRequired[str]
    TimestampToleranceInSeconds: NotRequired[int]
    MessageIdHttpHeader: NotRequired[str]
    SecretValue: NotRequired[str]
    SecretEncoding: NotRequired[WebhookSecretEncodingType]

class WebhookStaticTokenAuthConfigurationTypeDef(TypedDict):
    TokenHttpHeader: str
    SecretValue: NotRequired[str]

class WebhookDeduplicationConfigurationTypeDef(TypedDict):
    DeduplicationType: Literal["CONTENT_BASED"]

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

class RotateWebhookCredentialsResponseTypeDef(TypedDict):
    SecretArn: str
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

class DescribeEventBusRequestWaitExtraTypeDef(TypedDict):
    EventBusArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeEventBusRequestWaitTypeDef(TypedDict):
    EventBusArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeSubscriberRequestWaitTypeDef(TypedDict):
    SubscriberArn: str
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

class EventSourceDetailsTypeDef(TypedDict):
    WebhookDetails: NotRequired[WebhookDetailsTypeDef]

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

class SubscriberDetailsTypeDef(TypedDict):
    MskDetails: NotRequired[MskDetailsTypeDef]

class MskParametersOutputTypeDef(TypedDict):
    TopicName: str
    Connectivity: MskConnectivityType
    Compression: NotRequired[MskCompressionType]
    Acks: NotRequired[MskAcksType]
    PartitionKey: NotRequired[str]
    Headers: NotRequired[list[MskHeaderTypeDef]]
    ClientId: NotRequired[str]

class MskParametersTypeDef(TypedDict):
    TopicName: str
    Connectivity: MskConnectivityType
    Compression: NotRequired[MskCompressionType]
    Acks: NotRequired[MskAcksType]
    PartitionKey: NotRequired[str]
    Headers: NotRequired[Sequence[MskHeaderTypeDef]]
    ClientId: NotRequired[str]

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

class RotateWebhookCredentialsRequestTypeDef(TypedDict):
    EventSourceArn: str
    Credential: NotRequired[WebhookCredentialTypeDef]
    ClientToken: NotRequired[str]

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

class WebhookAuthConfigurationTypeDef(TypedDict):
    StaticTokenAuthConfiguration: NotRequired[WebhookStaticTokenAuthConfigurationTypeDef]
    BasicHttpAuthConfiguration: NotRequired[WebhookBasicHttpAuthConfigurationTypeDef]
    HmacAuthConfiguration: NotRequired[WebhookHmacAuthConfigurationTypeDef]

EventBusV2ParametersUnionTypeDef = Union[
    EventBusV2ParametersTypeDef, EventBusV2ParametersOutputTypeDef
]

class CreateEventSourceResponseTypeDef(TypedDict):
    EventSourceArn: str
    Name: str
    EventBusArn: str
    State: EventSourceStateType
    EventSourceDetails: EventSourceDetailsTypeDef
    CreationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

FilterConfigurationUnionTypeDef = Union[
    FilterConfigurationTypeDef, FilterConfigurationOutputTypeDef
]
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
        "SubscriberDetails": SubscriberDetailsTypeDef,
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
        "SubscriberDetails": SubscriberDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
MskParametersUnionTypeDef = Union[MskParametersTypeDef, MskParametersOutputTypeDef]
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
    MskParameters: NotRequired[MskParametersOutputTypeDef]

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
    MskParameters: NotRequired[MskParametersTypeDef]

SqsParametersUnionTypeDef = Union[SqsParametersTypeDef, SqsParametersOutputTypeDef]

class WebhookEventsSourceConfigurationOutputTypeDef(TypedDict):
    AuthConfiguration: WebhookAuthConfigurationTypeDef
    RoleArn: str
    KmsKeyIdentifier: NotRequired[str]
    MetadataHttpHeaders: NotRequired[list[str]]
    DeduplicationConfiguration: NotRequired[WebhookDeduplicationConfigurationTypeDef]
    LogConfiguration: NotRequired[LogConfigurationTypeDef]

class WebhookEventsSourceConfigurationTypeDef(TypedDict):
    AuthConfiguration: WebhookAuthConfigurationTypeDef
    RoleArn: str
    KmsKeyIdentifier: NotRequired[str]
    MetadataHttpHeaders: NotRequired[Sequence[str]]
    DeduplicationConfiguration: NotRequired[WebhookDeduplicationConfigurationTypeDef]
    LogConfiguration: NotRequired[LogConfigurationTypeDef]

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
        "SubscriberDetails": SubscriberDetailsTypeDef,
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
    MskParameters: NotRequired[MskParametersUnionTypeDef]

class EventSourceConfigurationOutputTypeDef(TypedDict):
    AwsServiceEventsConfiguration: NotRequired[AwsServiceEventsSourceConfigurationTypeDef]
    PartnerEventsConfiguration: NotRequired[PartnerEventsSourceConfigurationTypeDef]
    WebhookEventsConfiguration: NotRequired[WebhookEventsSourceConfigurationOutputTypeDef]

class EventSourceConfigurationTypeDef(TypedDict):
    AwsServiceEventsConfiguration: NotRequired[AwsServiceEventsSourceConfigurationTypeDef]
    PartnerEventsConfiguration: NotRequired[PartnerEventsSourceConfigurationTypeDef]
    WebhookEventsConfiguration: NotRequired[WebhookEventsSourceConfigurationTypeDef]

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

class DescribeEventSourceResponseTypeDef(TypedDict):
    EventSourceArn: str
    Name: str
    EventBusArn: str
    Configuration: EventSourceConfigurationOutputTypeDef
    Description: str
    State: EventSourceStateType
    Revoked: bool
    EventSourceDetails: EventSourceDetailsTypeDef
    CreationTime: datetime
    LastModifiedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

EventSourceConfigurationUnionTypeDef = Union[
    EventSourceConfigurationTypeDef, EventSourceConfigurationOutputTypeDef
]

class CreateEventSourceRequestTypeDef(TypedDict):
    Name: str
    EventBusArn: str
    Configuration: EventSourceConfigurationUnionTypeDef
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    ClientToken: NotRequired[str]

class UpdateEventSourceRequestTypeDef(TypedDict):
    EventSourceArn: str
    Configuration: NotRequired[EventSourceConfigurationUnionTypeDef]
    Description: NotRequired[str]
