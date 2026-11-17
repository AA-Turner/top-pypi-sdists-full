"""
Type annotations for opensearchmemory service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opensearchmemory/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_opensearchmemory.type_defs import BatchGetEventErrorTypeDef

    data: BatchGetEventErrorTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Union

from .literals import (
    BatchGetEventErrorCodeType,
    BlobContentTypeType,
    MemorySortFieldType,
    MemoryStrategyTypeType,
    MemoryTypeType,
    MessageRoleType,
    MetadataModeType,
    SortOrderType,
    SpaceStatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "BatchGetEventErrorTypeDef",
    "BatchGetEventInputTypeDef",
    "BatchGetEventOutputTypeDef",
    "BlobPayloadTypeDef",
    "BlobSourceTypeDef",
    "ConversationalPayloadOutputTypeDef",
    "ConversationalPayloadTypeDef",
    "CreateEventInputTypeDef",
    "CreateEventOutputTypeDef",
    "CreateMemoryDetailTypeDef",
    "CreateMemoryInputTypeDef",
    "CreateMemoryOutputTypeDef",
    "CreateSpaceRequestTypeDef",
    "CreateSpaceResponseTypeDef",
    "DeleteEventInputTypeDef",
    "DeleteEventOutputTypeDef",
    "DeleteMemoryInputTypeDef",
    "DeleteMemoryOutputTypeDef",
    "DeleteSpaceRequestTypeDef",
    "DeleteSpaceResponseTypeDef",
    "EncryptionConfigurationTypeDef",
    "EventDetailTypeDef",
    "EventPayloadOutputTypeDef",
    "EventPayloadTypeDef",
    "EventPayloadUnionTypeDef",
    "EventSearchSummaryTypeDef",
    "EventSummaryTypeDef",
    "EventTypeDef",
    "GetEventInputTypeDef",
    "GetEventOutputTypeDef",
    "GetMemoryInputTypeDef",
    "GetMemoryOutputTypeDef",
    "GetSpaceRequestTypeDef",
    "GetSpaceRequestWaitExtraTypeDef",
    "GetSpaceRequestWaitTypeDef",
    "GetSpaceResponseTypeDef",
    "ListEventsInputPaginateTypeDef",
    "ListEventsInputTypeDef",
    "ListEventsOutputTypeDef",
    "ListMemoriesInputPaginateTypeDef",
    "ListMemoriesInputTypeDef",
    "ListMemoriesOutputTypeDef",
    "ListSpacesRequestPaginateTypeDef",
    "ListSpacesRequestTypeDef",
    "ListSpacesResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MemoryListSummaryTypeDef",
    "MemorySearchSummaryTypeDef",
    "MemoryStrategyConfigurationTypeDef",
    "MemoryStrategyTypeDef",
    "MemoryTypeDef",
    "MessageContentTypeDef",
    "MessageTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "S3LocationTypeDef",
    "SearchEventsInputPaginateTypeDef",
    "SearchEventsInputTypeDef",
    "SearchEventsOutputTypeDef",
    "SearchMemoriesInputPaginateTypeDef",
    "SearchMemoriesInputTypeDef",
    "SearchMemoriesOutputTypeDef",
    "SpaceSummaryTypeDef",
    "StrategySelectorTypeDef",
    "StructuredDataPayloadOutputTypeDef",
    "StructuredDataPayloadTypeDef",
    "StructuredDataSourceOutputTypeDef",
    "StructuredDataSourceTypeDef",
    "SystemMetadataTypeDef",
    "TagResourceRequestTypeDef",
    "TagTypeDef",
    "TimestampTypeDef",
    "UnifiedConversationalObjectOutputTypeDef",
    "UnifiedConversationalObjectTypeDef",
    "UnifiedConversationalOutputTypeDef",
    "UnifiedConversationalSourceOutputTypeDef",
    "UnifiedConversationalSourceTypeDef",
    "UnifiedConversationalTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateMemoryInputTypeDef",
    "UpdateMemoryOutputTypeDef",
    "UpdateSpaceRequestTypeDef",
    "UpdateSpaceResponseTypeDef",
    "WaiterConfigTypeDef",
)


class BatchGetEventErrorTypeDef(TypedDict):
    eventId: str
    errorCode: BatchGetEventErrorCodeType
    message: str


class BatchGetEventInputTypeDef(TypedDict):
    spaceId: str
    eventIds: Sequence[str]
    actorId: NotRequired[str]
    sessionId: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class S3LocationTypeDef(TypedDict):
    uri: str


TimestampTypeDef = Union[datetime, str]


class EventDetailTypeDef(TypedDict):
    eventId: str
    spaceId: str
    actorId: str
    sessionId: str
    eventTimestamp: datetime


class CreateMemoryDetailTypeDef(TypedDict):
    memoryId: str
    spaceId: str
    name: str
    actorId: str
    sessionId: str


class CreateMemoryInputTypeDef(TypedDict):
    spaceId: str
    name: str
    content: str
    actorId: str
    sessionId: NotRequired[str]
    metadata: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]


class EncryptionConfigurationTypeDef(TypedDict):
    kmsKeyArn: NotRequired[str]


class TagTypeDef(TypedDict):
    key: str
    value: str


class DeleteEventInputTypeDef(TypedDict):
    spaceId: str
    eventId: str
    actorId: NotRequired[str]
    sessionId: NotRequired[str]


class DeleteMemoryInputTypeDef(TypedDict):
    spaceId: str
    memoryId: str
    actorId: NotRequired[str]
    strategyName: NotRequired[str]


class DeleteSpaceRequestTypeDef(TypedDict):
    spaceId: str


class SystemMetadataTypeDef(TypedDict):
    actorId: NotRequired[str]
    sessionId: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]


class EventSummaryTypeDef(TypedDict):
    eventId: str
    eventTimestamp: datetime
    metadata: NotRequired[dict[str, str]]


class GetEventInputTypeDef(TypedDict):
    spaceId: str
    eventId: str
    actorId: NotRequired[str]
    sessionId: NotRequired[str]


class GetMemoryInputTypeDef(TypedDict):
    spaceId: str
    memoryId: str
    actorId: NotRequired[str]
    strategyName: NotRequired[str]


class GetSpaceRequestTypeDef(TypedDict):
    spaceId: str


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class StrategySelectorTypeDef(TypedDict):
    memoryType: MemoryTypeType
    memoryStrategyNames: NotRequired[Sequence[str]]


class ListSpacesRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class SpaceSummaryTypeDef(TypedDict):
    spaceId: str
    arn: str
    name: str
    status: SpaceStatusType
    createdAt: datetime


class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str


class MemoryStrategyConfigurationTypeDef(TypedDict):
    extractionPrompt: NotRequired[str]
    extractEveryNMessages: NotRequired[int]
    extractEveryNTokens: NotRequired[int]
    idleTimeoutSeconds: NotRequired[int]
    extractionSeedTopK: NotRequired[int]
    extractionSeedRecentN: NotRequired[int]
    consolidationEnabled: NotRequired[bool]


class MessageContentTypeDef(TypedDict):
    text: str


class SearchEventsInputTypeDef(TypedDict):
    spaceId: str
    actorId: str
    query: Mapping[str, Any]
    sessionIds: NotRequired[Sequence[str]]
    sort: NotRequired[Mapping[str, Any]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class StructuredDataSourceOutputTypeDef(TypedDict):
    json: NotRequired[dict[str, Any]]


class StructuredDataSourceTypeDef(TypedDict):
    json: NotRequired[Mapping[str, Any]]


class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateMemoryInputTypeDef(TypedDict):
    spaceId: str
    memoryId: str
    content: NotRequired[str]
    metadata: NotRequired[Mapping[str, str]]
    metadataMode: NotRequired[MetadataModeType]
    actorId: NotRequired[str]
    strategyName: NotRequired[str]


class CreateSpaceResponseTypeDef(TypedDict):
    spaceId: str
    arn: str
    name: str
    status: SpaceStatusType
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteEventOutputTypeDef(TypedDict):
    eventId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteMemoryOutputTypeDef(TypedDict):
    memoryId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteSpaceResponseTypeDef(TypedDict):
    spaceId: str
    status: SpaceStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSpaceResponseTypeDef(TypedDict):
    spaceId: str
    status: SpaceStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class BlobSourceTypeDef(TypedDict):
    s3Location: NotRequired[S3LocationTypeDef]


class ListEventsInputTypeDef(TypedDict):
    spaceId: str
    actorId: str
    sessionId: str
    eventTimestampBefore: NotRequired[TimestampTypeDef]
    eventTimestampAfter: NotRequired[TimestampTypeDef]
    sortOrder: NotRequired[SortOrderType]
    metadataFilters: NotRequired[Mapping[str, str]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class CreateEventOutputTypeDef(TypedDict):
    event: EventDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateMemoryOutputTypeDef(TypedDict):
    memory: CreateMemoryDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Sequence[TagTypeDef]


class EventSearchSummaryTypeDef(TypedDict):
    eventId: str
    score: NotRequired[float]
    systemMetadata: NotRequired[SystemMetadataTypeDef]
    metadata: NotRequired[dict[str, str]]
    matchedContent: NotRequired[str]


class MemoryListSummaryTypeDef(TypedDict):
    memoryId: str
    memoryType: MemoryTypeType
    systemMetadata: SystemMetadataTypeDef
    strategyName: NotRequired[str]
    metadata: NotRequired[dict[str, str]]


class MemorySearchSummaryTypeDef(TypedDict):
    memoryId: str
    memoryType: NotRequired[MemoryTypeType]
    strategyName: NotRequired[str]
    content: NotRequired[str]
    score: NotRequired[float]
    systemMetadata: NotRequired[SystemMetadataTypeDef]
    metadata: NotRequired[dict[str, str]]
    sourceEventIds: NotRequired[list[str]]


class MemoryTypeDef(TypedDict):
    memoryId: str
    memoryType: MemoryTypeType
    content: str
    systemMetadata: SystemMetadataTypeDef
    strategyName: NotRequired[str]
    metadata: NotRequired[dict[str, str]]


class ListEventsOutputTypeDef(TypedDict):
    events: list[EventSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetSpaceRequestWaitExtraTypeDef(TypedDict):
    spaceId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetSpaceRequestWaitTypeDef(TypedDict):
    spaceId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class ListEventsInputPaginateTypeDef(TypedDict):
    spaceId: str
    actorId: str
    sessionId: str
    eventTimestampBefore: NotRequired[TimestampTypeDef]
    eventTimestampAfter: NotRequired[TimestampTypeDef]
    sortOrder: NotRequired[SortOrderType]
    metadataFilters: NotRequired[Mapping[str, str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSpacesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchEventsInputPaginateTypeDef(TypedDict):
    spaceId: str
    actorId: str
    query: Mapping[str, Any]
    sessionIds: NotRequired[Sequence[str]]
    sort: NotRequired[Mapping[str, Any]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMemoriesInputPaginateTypeDef(TypedDict):
    spaceId: str
    memoryStrategies: NotRequired[Sequence[StrategySelectorTypeDef]]
    actorIds: NotRequired[Sequence[str]]
    sessionIds: NotRequired[Sequence[str]]
    sortBy: NotRequired[MemorySortFieldType]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMemoriesInputTypeDef(TypedDict):
    spaceId: str
    memoryStrategies: NotRequired[Sequence[StrategySelectorTypeDef]]
    actorIds: NotRequired[Sequence[str]]
    sessionIds: NotRequired[Sequence[str]]
    sortBy: NotRequired[MemorySortFieldType]
    sortOrder: NotRequired[SortOrderType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class SearchMemoriesInputPaginateTypeDef(TypedDict):
    spaceId: str
    actorId: str
    query: Mapping[str, Any]
    memoryStrategies: NotRequired[Sequence[StrategySelectorTypeDef]]
    sort: NotRequired[Mapping[str, Any]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchMemoriesInputTypeDef(TypedDict):
    spaceId: str
    actorId: str
    query: Mapping[str, Any]
    memoryStrategies: NotRequired[Sequence[StrategySelectorTypeDef]]
    sort: NotRequired[Mapping[str, Any]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListSpacesResponseTypeDef(TypedDict):
    spaces: list[SpaceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


MemoryStrategyTypeDef = TypedDict(
    "MemoryStrategyTypeDef",
    {
        "type": MemoryStrategyTypeType,
        "name": NotRequired[str],
        "description": NotRequired[str],
        "configuration": NotRequired[MemoryStrategyConfigurationTypeDef],
    },
)


class MessageTypeDef(TypedDict):
    role: MessageRoleType
    content: MessageContentTypeDef


class StructuredDataPayloadOutputTypeDef(TypedDict):
    source: StructuredDataSourceOutputTypeDef


class StructuredDataPayloadTypeDef(TypedDict):
    source: StructuredDataSourceTypeDef


class BlobPayloadTypeDef(TypedDict):
    contentType: BlobContentTypeType
    source: BlobSourceTypeDef


class SearchEventsOutputTypeDef(TypedDict):
    events: list[EventSearchSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListMemoriesOutputTypeDef(TypedDict):
    memories: list[MemoryListSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class SearchMemoriesOutputTypeDef(TypedDict):
    memories: list[MemorySearchSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetMemoryOutputTypeDef(TypedDict):
    memory: MemoryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMemoryOutputTypeDef(TypedDict):
    memory: MemoryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSpaceRequestTypeDef(TypedDict):
    name: str
    memoryStrategies: NotRequired[Sequence[MemoryStrategyTypeDef]]
    eventExpiryDays: NotRequired[int]
    memoryExpiryDays: NotRequired[int]
    extractionModelId: NotRequired[str]
    encryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]
    clientToken: NotRequired[str]


class GetSpaceResponseTypeDef(TypedDict):
    spaceId: str
    arn: str
    name: str
    status: SpaceStatusType
    statusReason: str
    createdAt: datetime
    memoryStrategies: list[MemoryStrategyTypeDef]
    eventExpiryDays: int
    memoryExpiryDays: int
    extractionModelId: str
    encryptionConfiguration: EncryptionConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSpaceRequestTypeDef(TypedDict):
    spaceId: str
    memoryStrategies: NotRequired[Sequence[MemoryStrategyTypeDef]]
    eventExpiryDays: NotRequired[int]
    memoryExpiryDays: NotRequired[int]
    extractionModelId: NotRequired[str]


class UnifiedConversationalObjectOutputTypeDef(TypedDict):
    messages: list[MessageTypeDef]


class UnifiedConversationalObjectTypeDef(TypedDict):
    messages: Sequence[MessageTypeDef]


UnifiedConversationalSourceOutputTypeDef = TypedDict(
    "UnifiedConversationalSourceOutputTypeDef",
    {
        "object": NotRequired[UnifiedConversationalObjectOutputTypeDef],
    },
)
UnifiedConversationalSourceTypeDef = TypedDict(
    "UnifiedConversationalSourceTypeDef",
    {
        "object": NotRequired[UnifiedConversationalObjectTypeDef],
    },
)


class UnifiedConversationalOutputTypeDef(TypedDict):
    source: UnifiedConversationalSourceOutputTypeDef


class UnifiedConversationalTypeDef(TypedDict):
    source: UnifiedConversationalSourceTypeDef


class ConversationalPayloadOutputTypeDef(TypedDict):
    unified: NotRequired[UnifiedConversationalOutputTypeDef]


class ConversationalPayloadTypeDef(TypedDict):
    unified: NotRequired[UnifiedConversationalTypeDef]


class EventPayloadOutputTypeDef(TypedDict):
    conversational: NotRequired[ConversationalPayloadOutputTypeDef]
    structuredData: NotRequired[StructuredDataPayloadOutputTypeDef]
    blob: NotRequired[BlobPayloadTypeDef]


class EventPayloadTypeDef(TypedDict):
    conversational: NotRequired[ConversationalPayloadTypeDef]
    structuredData: NotRequired[StructuredDataPayloadTypeDef]
    blob: NotRequired[BlobPayloadTypeDef]


class EventTypeDef(TypedDict):
    eventId: str
    spaceId: str
    actorId: str
    sessionId: str
    payload: EventPayloadOutputTypeDef
    eventTimestamp: datetime
    metadata: NotRequired[dict[str, str]]


EventPayloadUnionTypeDef = Union[EventPayloadTypeDef, EventPayloadOutputTypeDef]


class BatchGetEventOutputTypeDef(TypedDict):
    events: list[EventTypeDef]
    errors: list[BatchGetEventErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetEventOutputTypeDef(TypedDict):
    event: EventTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateEventInputTypeDef(TypedDict):
    spaceId: str
    actorId: str
    payload: EventPayloadUnionTypeDef
    sessionId: NotRequired[str]
    eventTimestamp: NotRequired[TimestampTypeDef]
    metadata: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]
    infer: NotRequired[bool]
