"""
Type annotations for ivschat service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ivschat/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from types_boto3_ivschat.type_defs import CloudWatchLogsDestinationConfigurationTypeDef

    data: CloudWatchLogsDestinationConfigurationTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from datetime import datetime

from .literals import ChatTokenCapabilityType, FallbackResultType, LoggingConfigurationStateType

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import list as List
    from collections.abc import Mapping, Sequence
else:
    from typing import Dict, List, Mapping, Sequence
if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "CloudWatchLogsDestinationConfigurationTypeDef",
    "CreateChatTokenRequestTypeDef",
    "CreateChatTokenResponseTypeDef",
    "CreateLoggingConfigurationRequestTypeDef",
    "CreateLoggingConfigurationResponseTypeDef",
    "CreateRoomRequestTypeDef",
    "CreateRoomResponseTypeDef",
    "DeleteLoggingConfigurationRequestTypeDef",
    "DeleteMessageRequestTypeDef",
    "DeleteMessageResponseTypeDef",
    "DeleteRoomRequestTypeDef",
    "DestinationConfigurationTypeDef",
    "DisconnectUserRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "FirehoseDestinationConfigurationTypeDef",
    "GetLoggingConfigurationRequestTypeDef",
    "GetLoggingConfigurationResponseTypeDef",
    "GetRoomRequestTypeDef",
    "GetRoomResponseTypeDef",
    "ListLoggingConfigurationsRequestTypeDef",
    "ListLoggingConfigurationsResponseTypeDef",
    "ListRoomsRequestTypeDef",
    "ListRoomsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LoggingConfigurationSummaryTypeDef",
    "MessageReviewHandlerTypeDef",
    "ResponseMetadataTypeDef",
    "RoomSummaryTypeDef",
    "S3DestinationConfigurationTypeDef",
    "SendEventRequestTypeDef",
    "SendEventResponseTypeDef",
    "TagResourceRequestTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateLoggingConfigurationRequestTypeDef",
    "UpdateLoggingConfigurationResponseTypeDef",
    "UpdateRoomRequestTypeDef",
    "UpdateRoomResponseTypeDef",
)


class CloudWatchLogsDestinationConfigurationTypeDef(TypedDict):
    logGroupName: str


class CreateChatTokenRequestTypeDef(TypedDict):
    roomIdentifier: str
    userId: str
    capabilities: NotRequired[Sequence[ChatTokenCapabilityType]]
    sessionDurationInMinutes: NotRequired[int]
    attributes: NotRequired[Mapping[str, str]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class MessageReviewHandlerTypeDef(TypedDict):
    uri: NotRequired[str]
    fallbackResult: NotRequired[FallbackResultType]


class DeleteLoggingConfigurationRequestTypeDef(TypedDict):
    identifier: str


DeleteMessageRequestTypeDef = TypedDict(
    "DeleteMessageRequestTypeDef",
    {
        "roomIdentifier": str,
        "id": str,
        "reason": NotRequired[str],
    },
)


class DeleteRoomRequestTypeDef(TypedDict):
    identifier: str


class FirehoseDestinationConfigurationTypeDef(TypedDict):
    deliveryStreamName: str


class S3DestinationConfigurationTypeDef(TypedDict):
    bucketName: str


class DisconnectUserRequestTypeDef(TypedDict):
    roomIdentifier: str
    userId: str
    reason: NotRequired[str]


class GetLoggingConfigurationRequestTypeDef(TypedDict):
    identifier: str


class GetRoomRequestTypeDef(TypedDict):
    identifier: str


class ListLoggingConfigurationsRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListRoomsRequestTypeDef(TypedDict):
    name: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    messageReviewHandlerUri: NotRequired[str]
    loggingConfigurationIdentifier: NotRequired[str]


class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str


class SendEventRequestTypeDef(TypedDict):
    roomIdentifier: str
    eventName: str
    attributes: NotRequired[Mapping[str, str]]


class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class CreateChatTokenResponseTypeDef(TypedDict):
    token: str
    tokenExpirationTime: datetime
    sessionExpirationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


DeleteMessageResponseTypeDef = TypedDict(
    "DeleteMessageResponseTypeDef",
    {
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


SendEventResponseTypeDef = TypedDict(
    "SendEventResponseTypeDef",
    {
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class CreateRoomRequestTypeDef(TypedDict):
    name: NotRequired[str]
    maximumMessageRatePerSecond: NotRequired[int]
    maximumMessageLength: NotRequired[int]
    messageReviewHandler: NotRequired[MessageReviewHandlerTypeDef]
    tags: NotRequired[Mapping[str, str]]
    loggingConfigurationIdentifiers: NotRequired[Sequence[str]]


CreateRoomResponseTypeDef = TypedDict(
    "CreateRoomResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "name": str,
        "createTime": datetime,
        "updateTime": datetime,
        "maximumMessageRatePerSecond": int,
        "maximumMessageLength": int,
        "messageReviewHandler": MessageReviewHandlerTypeDef,
        "tags": Dict[str, str],
        "loggingConfigurationIdentifiers": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetRoomResponseTypeDef = TypedDict(
    "GetRoomResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "name": str,
        "createTime": datetime,
        "updateTime": datetime,
        "maximumMessageRatePerSecond": int,
        "maximumMessageLength": int,
        "messageReviewHandler": MessageReviewHandlerTypeDef,
        "tags": Dict[str, str],
        "loggingConfigurationIdentifiers": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RoomSummaryTypeDef = TypedDict(
    "RoomSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "id": NotRequired[str],
        "name": NotRequired[str],
        "messageReviewHandler": NotRequired[MessageReviewHandlerTypeDef],
        "createTime": NotRequired[datetime],
        "updateTime": NotRequired[datetime],
        "tags": NotRequired[Dict[str, str]],
        "loggingConfigurationIdentifiers": NotRequired[List[str]],
    },
)


class UpdateRoomRequestTypeDef(TypedDict):
    identifier: str
    name: NotRequired[str]
    maximumMessageRatePerSecond: NotRequired[int]
    maximumMessageLength: NotRequired[int]
    messageReviewHandler: NotRequired[MessageReviewHandlerTypeDef]
    loggingConfigurationIdentifiers: NotRequired[Sequence[str]]


UpdateRoomResponseTypeDef = TypedDict(
    "UpdateRoomResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "name": str,
        "createTime": datetime,
        "updateTime": datetime,
        "maximumMessageRatePerSecond": int,
        "maximumMessageLength": int,
        "messageReviewHandler": MessageReviewHandlerTypeDef,
        "tags": Dict[str, str],
        "loggingConfigurationIdentifiers": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class DestinationConfigurationTypeDef(TypedDict):
    s3: NotRequired[S3DestinationConfigurationTypeDef]
    cloudWatchLogs: NotRequired[CloudWatchLogsDestinationConfigurationTypeDef]
    firehose: NotRequired[FirehoseDestinationConfigurationTypeDef]


class ListRoomsResponseTypeDef(TypedDict):
    rooms: List[RoomSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateLoggingConfigurationRequestTypeDef(TypedDict):
    destinationConfiguration: DestinationConfigurationTypeDef
    name: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


CreateLoggingConfigurationResponseTypeDef = TypedDict(
    "CreateLoggingConfigurationResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "createTime": datetime,
        "updateTime": datetime,
        "name": str,
        "destinationConfiguration": DestinationConfigurationTypeDef,
        "state": Literal["ACTIVE"],
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetLoggingConfigurationResponseTypeDef = TypedDict(
    "GetLoggingConfigurationResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "createTime": datetime,
        "updateTime": datetime,
        "name": str,
        "destinationConfiguration": DestinationConfigurationTypeDef,
        "state": LoggingConfigurationStateType,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
LoggingConfigurationSummaryTypeDef = TypedDict(
    "LoggingConfigurationSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "id": NotRequired[str],
        "createTime": NotRequired[datetime],
        "updateTime": NotRequired[datetime],
        "name": NotRequired[str],
        "destinationConfiguration": NotRequired[DestinationConfigurationTypeDef],
        "state": NotRequired[LoggingConfigurationStateType],
        "tags": NotRequired[Dict[str, str]],
    },
)


class UpdateLoggingConfigurationRequestTypeDef(TypedDict):
    identifier: str
    name: NotRequired[str]
    destinationConfiguration: NotRequired[DestinationConfigurationTypeDef]


UpdateLoggingConfigurationResponseTypeDef = TypedDict(
    "UpdateLoggingConfigurationResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "createTime": datetime,
        "updateTime": datetime,
        "name": str,
        "destinationConfiguration": DestinationConfigurationTypeDef,
        "state": Literal["ACTIVE"],
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class ListLoggingConfigurationsResponseTypeDef(TypedDict):
    loggingConfigurations: List[LoggingConfigurationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
