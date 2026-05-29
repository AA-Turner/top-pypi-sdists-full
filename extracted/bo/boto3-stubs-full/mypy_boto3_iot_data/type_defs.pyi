"""
Type annotations for iot-data service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_iot_data.type_defs import BlobTypeDef

    data: BlobTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from typing import IO, Any, Union

from botocore.response import StreamingBody

from .literals import PayloadFormatIndicatorType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "BlobTypeDef",
    "DeleteConnectionRequestTypeDef",
    "DeleteThingShadowRequestTypeDef",
    "DeleteThingShadowResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetConnectionRequestTypeDef",
    "GetConnectionResponseTypeDef",
    "GetRetainedMessageRequestTypeDef",
    "GetRetainedMessageResponseTypeDef",
    "GetThingShadowRequestTypeDef",
    "GetThingShadowResponseTypeDef",
    "ListNamedShadowsForThingRequestTypeDef",
    "ListNamedShadowsForThingResponseTypeDef",
    "ListRetainedMessagesRequestPaginateTypeDef",
    "ListRetainedMessagesRequestTypeDef",
    "ListRetainedMessagesResponseTypeDef",
    "ListSubscriptionsRequestPaginateTypeDef",
    "ListSubscriptionsRequestTypeDef",
    "ListSubscriptionsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PublishRequestTypeDef",
    "ResponseMetadataTypeDef",
    "RetainedMessageSummaryTypeDef",
    "SendDirectMessageRequestTypeDef",
    "SendDirectMessageResponseTypeDef",
    "SubscriptionSummaryTypeDef",
    "UpdateThingShadowRequestTypeDef",
    "UpdateThingShadowResponseTypeDef",
)

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class DeleteConnectionRequestTypeDef(TypedDict):
    clientId: str
    cleanSession: NotRequired[bool]
    preventWillMessage: NotRequired[bool]

class DeleteThingShadowRequestTypeDef(TypedDict):
    thingName: str
    shadowName: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class GetConnectionRequestTypeDef(TypedDict):
    clientId: str
    includeSocketInformation: NotRequired[bool]

class GetRetainedMessageRequestTypeDef(TypedDict):
    topic: str

class GetThingShadowRequestTypeDef(TypedDict):
    thingName: str
    shadowName: NotRequired[str]

class ListNamedShadowsForThingRequestTypeDef(TypedDict):
    thingName: str
    nextToken: NotRequired[str]
    pageSize: NotRequired[int]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListRetainedMessagesRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class RetainedMessageSummaryTypeDef(TypedDict):
    topic: NotRequired[str]
    payloadSize: NotRequired[int]
    qos: NotRequired[int]
    lastModifiedTime: NotRequired[int]

class ListSubscriptionsRequestTypeDef(TypedDict):
    clientId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class SubscriptionSummaryTypeDef(TypedDict):
    topicFilter: str
    qos: int

class PublishRequestTypeDef(TypedDict):
    topic: str
    qos: NotRequired[int]
    retain: NotRequired[bool]
    payload: NotRequired[BlobTypeDef]
    userProperties: NotRequired[str]
    payloadFormatIndicator: NotRequired[PayloadFormatIndicatorType]
    contentType: NotRequired[str]
    responseTopic: NotRequired[str]
    correlationData: NotRequired[str]
    messageExpiry: NotRequired[int]

class SendDirectMessageRequestTypeDef(TypedDict):
    clientId: str
    topic: str
    contentType: NotRequired[str]
    responseTopic: NotRequired[str]
    confirmation: NotRequired[bool]
    timeout: NotRequired[int]
    payload: NotRequired[BlobTypeDef]
    userProperties: NotRequired[str]
    payloadFormatIndicator: NotRequired[PayloadFormatIndicatorType]
    correlationData: NotRequired[str]

class UpdateThingShadowRequestTypeDef(TypedDict):
    thingName: str
    payload: BlobTypeDef
    shadowName: NotRequired[str]

class DeleteThingShadowResponseTypeDef(TypedDict):
    payload: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetConnectionResponseTypeDef(TypedDict):
    connected: bool
    thingName: str
    cleanSession: bool
    sourceIp: str
    sourcePort: int
    targetIp: str
    targetPort: int
    keepAliveDuration: int
    connectedSince: int
    disconnectedSince: int
    disconnectReason: str
    sessionExpiry: int
    clientId: str
    vpcEndpointId: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetRetainedMessageResponseTypeDef(TypedDict):
    topic: str
    payload: bytes
    qos: int
    lastModifiedTime: int
    userProperties: bytes
    ResponseMetadata: ResponseMetadataTypeDef

class GetThingShadowResponseTypeDef(TypedDict):
    payload: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef

class ListNamedShadowsForThingResponseTypeDef(TypedDict):
    results: list[str]
    timestamp: int
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class SendDirectMessageResponseTypeDef(TypedDict):
    message: str
    traceId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateThingShadowResponseTypeDef(TypedDict):
    payload: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef

class ListRetainedMessagesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSubscriptionsRequestPaginateTypeDef(TypedDict):
    clientId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRetainedMessagesResponseTypeDef(TypedDict):
    retainedTopics: list[RetainedMessageSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSubscriptionsResponseTypeDef(TypedDict):
    subscriptions: list[SubscriptionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
