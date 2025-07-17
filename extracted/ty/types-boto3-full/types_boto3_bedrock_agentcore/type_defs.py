"""
Type annotations for bedrock-agentcore service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from types_boto3_bedrock_agentcore.type_defs import AccessDeniedExceptionTypeDef

    data: AccessDeniedExceptionTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import IO, Any, Union

from botocore.eventstream import EventStream
from botocore.response import StreamingBody

from .literals import (
    AutomationStreamStatusType,
    BrowserSessionStatusType,
    CodeInterpreterSessionStatusType,
    ContentBlockTypeType,
    Oauth2FlowTypeType,
    ProgrammingLanguageType,
    ResourceContentTypeType,
    RoleType,
    TaskStatusType,
    ToolNameType,
    ValidationExceptionReasonType,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import list as List
    from collections.abc import Mapping, Sequence
else:
    from typing import Dict, List, Mapping, Sequence
if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AccessDeniedExceptionTypeDef",
    "ActorSummaryTypeDef",
    "AutomationStreamTypeDef",
    "AutomationStreamUpdateTypeDef",
    "BlobTypeDef",
    "BranchFilterTypeDef",
    "BranchTypeDef",
    "BrowserSessionStreamTypeDef",
    "BrowserSessionSummaryTypeDef",
    "CodeInterpreterResultTypeDef",
    "CodeInterpreterSessionSummaryTypeDef",
    "CodeInterpreterStreamOutputTypeDef",
    "ConflictExceptionTypeDef",
    "ContentBlockTypeDef",
    "ContentTypeDef",
    "ConversationalTypeDef",
    "CreateEventInputTypeDef",
    "CreateEventOutputTypeDef",
    "DeleteEventInputTypeDef",
    "DeleteEventOutputTypeDef",
    "DeleteMemoryRecordInputTypeDef",
    "DeleteMemoryRecordOutputTypeDef",
    "EventTypeDef",
    "FilterInputTypeDef",
    "GetBrowserSessionRequestTypeDef",
    "GetBrowserSessionResponseTypeDef",
    "GetCodeInterpreterSessionRequestTypeDef",
    "GetCodeInterpreterSessionResponseTypeDef",
    "GetEventInputTypeDef",
    "GetEventOutputTypeDef",
    "GetMemoryRecordInputTypeDef",
    "GetMemoryRecordOutputTypeDef",
    "GetResourceApiKeyRequestTypeDef",
    "GetResourceApiKeyResponseTypeDef",
    "GetResourceOauth2TokenRequestTypeDef",
    "GetResourceOauth2TokenResponseTypeDef",
    "GetWorkloadAccessTokenForJWTRequestTypeDef",
    "GetWorkloadAccessTokenForJWTResponseTypeDef",
    "GetWorkloadAccessTokenForUserIdRequestTypeDef",
    "GetWorkloadAccessTokenForUserIdResponseTypeDef",
    "GetWorkloadAccessTokenRequestTypeDef",
    "GetWorkloadAccessTokenResponseTypeDef",
    "InputContentBlockTypeDef",
    "InternalServerExceptionTypeDef",
    "InvokeAgentRuntimeRequestTypeDef",
    "InvokeAgentRuntimeResponseTypeDef",
    "InvokeCodeInterpreterRequestTypeDef",
    "InvokeCodeInterpreterResponseTypeDef",
    "ListActorsInputPaginateTypeDef",
    "ListActorsInputTypeDef",
    "ListActorsOutputTypeDef",
    "ListBrowserSessionsRequestTypeDef",
    "ListBrowserSessionsResponseTypeDef",
    "ListCodeInterpreterSessionsRequestTypeDef",
    "ListCodeInterpreterSessionsResponseTypeDef",
    "ListEventsInputPaginateTypeDef",
    "ListEventsInputTypeDef",
    "ListEventsOutputTypeDef",
    "ListMemoryRecordsInputPaginateTypeDef",
    "ListMemoryRecordsInputTypeDef",
    "ListMemoryRecordsOutputTypeDef",
    "ListSessionsInputPaginateTypeDef",
    "ListSessionsInputTypeDef",
    "ListSessionsOutputTypeDef",
    "LiveViewStreamTypeDef",
    "MemoryContentTypeDef",
    "MemoryRecordSummaryTypeDef",
    "MemoryRecordTypeDef",
    "PaginatorConfigTypeDef",
    "PayloadTypeOutputTypeDef",
    "PayloadTypeTypeDef",
    "PayloadTypeUnionTypeDef",
    "ResourceContentTypeDef",
    "ResourceNotFoundExceptionTypeDef",
    "ResponseMetadataTypeDef",
    "RetrieveMemoryRecordsInputPaginateTypeDef",
    "RetrieveMemoryRecordsInputTypeDef",
    "RetrieveMemoryRecordsOutputTypeDef",
    "SearchCriteriaTypeDef",
    "ServiceQuotaExceededExceptionTypeDef",
    "SessionSummaryTypeDef",
    "StartBrowserSessionRequestTypeDef",
    "StartBrowserSessionResponseTypeDef",
    "StartCodeInterpreterSessionRequestTypeDef",
    "StartCodeInterpreterSessionResponseTypeDef",
    "StopBrowserSessionRequestTypeDef",
    "StopBrowserSessionResponseTypeDef",
    "StopCodeInterpreterSessionRequestTypeDef",
    "StopCodeInterpreterSessionResponseTypeDef",
    "StreamUpdateTypeDef",
    "ThrottlingExceptionTypeDef",
    "TimestampTypeDef",
    "ToolArgumentsTypeDef",
    "ToolResultStructuredContentTypeDef",
    "UpdateBrowserStreamRequestTypeDef",
    "UpdateBrowserStreamResponseTypeDef",
    "ValidationExceptionFieldTypeDef",
    "ValidationExceptionTypeDef",
    "ViewPortTypeDef",
)


class AccessDeniedExceptionTypeDef(TypedDict):
    message: NotRequired[str]


class ActorSummaryTypeDef(TypedDict):
    actorId: str


class AutomationStreamTypeDef(TypedDict):
    streamEndpoint: str
    streamStatus: AutomationStreamStatusType


class AutomationStreamUpdateTypeDef(TypedDict):
    streamStatus: NotRequired[AutomationStreamStatusType]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class BranchFilterTypeDef(TypedDict):
    name: str
    includeParentBranches: NotRequired[bool]


class BranchTypeDef(TypedDict):
    name: str
    rootEventId: NotRequired[str]


class LiveViewStreamTypeDef(TypedDict):
    streamEndpoint: NotRequired[str]


class BrowserSessionSummaryTypeDef(TypedDict):
    browserIdentifier: str
    sessionId: str
    status: BrowserSessionStatusType
    createdAt: datetime
    name: NotRequired[str]
    lastUpdatedAt: NotRequired[datetime]


class ToolResultStructuredContentTypeDef(TypedDict):
    taskId: NotRequired[str]
    taskStatus: NotRequired[TaskStatusType]
    stdout: NotRequired[str]
    stderr: NotRequired[str]
    exitCode: NotRequired[int]
    executionTime: NotRequired[float]


class CodeInterpreterSessionSummaryTypeDef(TypedDict):
    codeInterpreterIdentifier: str
    sessionId: str
    status: CodeInterpreterSessionStatusType
    createdAt: datetime
    name: NotRequired[str]
    lastUpdatedAt: NotRequired[datetime]


class ConflictExceptionTypeDef(TypedDict):
    message: NotRequired[str]


class InternalServerExceptionTypeDef(TypedDict):
    message: NotRequired[str]


class ResourceNotFoundExceptionTypeDef(TypedDict):
    message: NotRequired[str]


class ServiceQuotaExceededExceptionTypeDef(TypedDict):
    message: NotRequired[str]


class ThrottlingExceptionTypeDef(TypedDict):
    message: NotRequired[str]


ResourceContentTypeDef = TypedDict(
    "ResourceContentTypeDef",
    {
        "type": ResourceContentTypeType,
        "uri": NotRequired[str],
        "mimeType": NotRequired[str],
        "text": NotRequired[str],
        "blob": NotRequired[bytes],
    },
)


class ContentTypeDef(TypedDict):
    text: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DeleteEventInputTypeDef(TypedDict):
    memoryId: str
    sessionId: str
    eventId: str
    actorId: str


class DeleteMemoryRecordInputTypeDef(TypedDict):
    memoryId: str
    memoryRecordId: str


class GetBrowserSessionRequestTypeDef(TypedDict):
    browserIdentifier: str
    sessionId: str


class ViewPortTypeDef(TypedDict):
    width: int
    height: int


class GetCodeInterpreterSessionRequestTypeDef(TypedDict):
    codeInterpreterIdentifier: str
    sessionId: str


class GetEventInputTypeDef(TypedDict):
    memoryId: str
    sessionId: str
    actorId: str
    eventId: str


class GetMemoryRecordInputTypeDef(TypedDict):
    memoryId: str
    memoryRecordId: str


class GetResourceApiKeyRequestTypeDef(TypedDict):
    workloadIdentityToken: str
    resourceCredentialProviderName: str


class GetResourceOauth2TokenRequestTypeDef(TypedDict):
    workloadIdentityToken: str
    resourceCredentialProviderName: str
    scopes: Sequence[str]
    oauth2Flow: Oauth2FlowTypeType
    userId: NotRequired[str]
    resourceOauth2ReturnUrl: NotRequired[str]
    forceAuthentication: NotRequired[bool]
    customParameters: NotRequired[Mapping[str, str]]


class GetWorkloadAccessTokenForJWTRequestTypeDef(TypedDict):
    workloadName: str
    userToken: str


class GetWorkloadAccessTokenForUserIdRequestTypeDef(TypedDict):
    workloadName: str
    userId: str


class GetWorkloadAccessTokenRequestTypeDef(TypedDict):
    workloadName: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListActorsInputTypeDef(TypedDict):
    memoryId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListBrowserSessionsRequestTypeDef(TypedDict):
    browserIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    status: NotRequired[BrowserSessionStatusType]


class ListCodeInterpreterSessionsRequestTypeDef(TypedDict):
    codeInterpreterIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    status: NotRequired[CodeInterpreterSessionStatusType]


class ListMemoryRecordsInputTypeDef(TypedDict):
    memoryId: str
    namespace: str
    memoryStrategyId: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListSessionsInputTypeDef(TypedDict):
    memoryId: str
    actorId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class SessionSummaryTypeDef(TypedDict):
    sessionId: str
    actorId: str
    createdAt: datetime


class MemoryContentTypeDef(TypedDict):
    text: NotRequired[str]


class SearchCriteriaTypeDef(TypedDict):
    searchQuery: str
    memoryStrategyId: NotRequired[str]
    topK: NotRequired[int]


class StartCodeInterpreterSessionRequestTypeDef(TypedDict):
    codeInterpreterIdentifier: str
    name: NotRequired[str]
    sessionTimeoutSeconds: NotRequired[int]
    clientToken: NotRequired[str]


class StopBrowserSessionRequestTypeDef(TypedDict):
    browserIdentifier: str
    sessionId: str
    clientToken: NotRequired[str]


class StopCodeInterpreterSessionRequestTypeDef(TypedDict):
    codeInterpreterIdentifier: str
    sessionId: str
    clientToken: NotRequired[str]


class ValidationExceptionFieldTypeDef(TypedDict):
    name: str
    message: str


class StreamUpdateTypeDef(TypedDict):
    automationStreamUpdate: NotRequired[AutomationStreamUpdateTypeDef]


class InputContentBlockTypeDef(TypedDict):
    path: str
    text: NotRequired[str]
    blob: NotRequired[BlobTypeDef]


class InvokeAgentRuntimeRequestTypeDef(TypedDict):
    agentRuntimeArn: str
    payload: BlobTypeDef
    contentType: NotRequired[str]
    accept: NotRequired[str]
    mcpSessionId: NotRequired[str]
    runtimeSessionId: NotRequired[str]
    mcpProtocolVersion: NotRequired[str]
    runtimeUserId: NotRequired[str]
    traceId: NotRequired[str]
    traceParent: NotRequired[str]
    traceState: NotRequired[str]
    baggage: NotRequired[str]
    qualifier: NotRequired[str]


class FilterInputTypeDef(TypedDict):
    branch: NotRequired[BranchFilterTypeDef]


class BrowserSessionStreamTypeDef(TypedDict):
    automationStream: AutomationStreamTypeDef
    liveViewStream: NotRequired[LiveViewStreamTypeDef]


ContentBlockTypeDef = TypedDict(
    "ContentBlockTypeDef",
    {
        "type": ContentBlockTypeType,
        "text": NotRequired[str],
        "data": NotRequired[bytes],
        "mimeType": NotRequired[str],
        "uri": NotRequired[str],
        "name": NotRequired[str],
        "description": NotRequired[str],
        "size": NotRequired[int],
        "resource": NotRequired[ResourceContentTypeDef],
    },
)


class ConversationalTypeDef(TypedDict):
    content: ContentTypeDef
    role: RoleType


class DeleteEventOutputTypeDef(TypedDict):
    eventId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteMemoryRecordOutputTypeDef(TypedDict):
    memoryRecordId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetCodeInterpreterSessionResponseTypeDef(TypedDict):
    codeInterpreterIdentifier: str
    sessionId: str
    name: str
    createdAt: datetime
    sessionTimeoutSeconds: int
    status: CodeInterpreterSessionStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class GetResourceApiKeyResponseTypeDef(TypedDict):
    apiKey: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetResourceOauth2TokenResponseTypeDef(TypedDict):
    authorizationUrl: str
    accessToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetWorkloadAccessTokenForJWTResponseTypeDef(TypedDict):
    workloadAccessToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetWorkloadAccessTokenForUserIdResponseTypeDef(TypedDict):
    workloadAccessToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetWorkloadAccessTokenResponseTypeDef(TypedDict):
    workloadAccessToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class InvokeAgentRuntimeResponseTypeDef(TypedDict):
    runtimeSessionId: str
    mcpSessionId: str
    mcpProtocolVersion: str
    traceId: str
    traceParent: str
    traceState: str
    baggage: str
    contentType: str
    response: StreamingBody
    statusCode: int
    ResponseMetadata: ResponseMetadataTypeDef


class ListActorsOutputTypeDef(TypedDict):
    actorSummaries: List[ActorSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListBrowserSessionsResponseTypeDef(TypedDict):
    items: List[BrowserSessionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListCodeInterpreterSessionsResponseTypeDef(TypedDict):
    items: List[CodeInterpreterSessionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class StartCodeInterpreterSessionResponseTypeDef(TypedDict):
    codeInterpreterIdentifier: str
    sessionId: str
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class StopBrowserSessionResponseTypeDef(TypedDict):
    browserIdentifier: str
    sessionId: str
    lastUpdatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class StopCodeInterpreterSessionResponseTypeDef(TypedDict):
    codeInterpreterIdentifier: str
    sessionId: str
    lastUpdatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class StartBrowserSessionRequestTypeDef(TypedDict):
    browserIdentifier: str
    name: NotRequired[str]
    sessionTimeoutSeconds: NotRequired[int]
    viewPort: NotRequired[ViewPortTypeDef]
    clientToken: NotRequired[str]


class ListActorsInputPaginateTypeDef(TypedDict):
    memoryId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMemoryRecordsInputPaginateTypeDef(TypedDict):
    memoryId: str
    namespace: str
    memoryStrategyId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSessionsInputPaginateTypeDef(TypedDict):
    memoryId: str
    actorId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSessionsOutputTypeDef(TypedDict):
    sessionSummaries: List[SessionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class MemoryRecordSummaryTypeDef(TypedDict):
    memoryRecordId: str
    content: MemoryContentTypeDef
    memoryStrategyId: str
    namespaces: List[str]
    createdAt: datetime
    score: NotRequired[float]


class MemoryRecordTypeDef(TypedDict):
    memoryRecordId: str
    content: MemoryContentTypeDef
    memoryStrategyId: str
    namespaces: List[str]
    createdAt: datetime


class RetrieveMemoryRecordsInputPaginateTypeDef(TypedDict):
    memoryId: str
    namespace: str
    searchCriteria: SearchCriteriaTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class RetrieveMemoryRecordsInputTypeDef(TypedDict):
    memoryId: str
    namespace: str
    searchCriteria: SearchCriteriaTypeDef
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ValidationExceptionTypeDef(TypedDict):
    message: str
    reason: ValidationExceptionReasonType
    fieldList: NotRequired[List[ValidationExceptionFieldTypeDef]]


class UpdateBrowserStreamRequestTypeDef(TypedDict):
    browserIdentifier: str
    sessionId: str
    streamUpdate: StreamUpdateTypeDef
    clientToken: NotRequired[str]


class ToolArgumentsTypeDef(TypedDict):
    code: NotRequired[str]
    language: NotRequired[ProgrammingLanguageType]
    clearContext: NotRequired[bool]
    command: NotRequired[str]
    path: NotRequired[str]
    paths: NotRequired[Sequence[str]]
    content: NotRequired[Sequence[InputContentBlockTypeDef]]
    directoryPath: NotRequired[str]
    taskId: NotRequired[str]


ListEventsInputPaginateTypeDef = TypedDict(
    "ListEventsInputPaginateTypeDef",
    {
        "memoryId": str,
        "sessionId": str,
        "actorId": str,
        "includePayloads": NotRequired[bool],
        "filter": NotRequired[FilterInputTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListEventsInputTypeDef = TypedDict(
    "ListEventsInputTypeDef",
    {
        "memoryId": str,
        "sessionId": str,
        "actorId": str,
        "includePayloads": NotRequired[bool],
        "filter": NotRequired[FilterInputTypeDef],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)


class GetBrowserSessionResponseTypeDef(TypedDict):
    browserIdentifier: str
    sessionId: str
    name: str
    createdAt: datetime
    viewPort: ViewPortTypeDef
    sessionTimeoutSeconds: int
    status: BrowserSessionStatusType
    streams: BrowserSessionStreamTypeDef
    sessionReplayArtifact: str
    lastUpdatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class StartBrowserSessionResponseTypeDef(TypedDict):
    browserIdentifier: str
    sessionId: str
    createdAt: datetime
    streams: BrowserSessionStreamTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBrowserStreamResponseTypeDef(TypedDict):
    browserIdentifier: str
    sessionId: str
    streams: BrowserSessionStreamTypeDef
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CodeInterpreterResultTypeDef(TypedDict):
    content: List[ContentBlockTypeDef]
    structuredContent: NotRequired[ToolResultStructuredContentTypeDef]
    isError: NotRequired[bool]


class PayloadTypeOutputTypeDef(TypedDict):
    conversational: NotRequired[ConversationalTypeDef]
    blob: NotRequired[Dict[str, Any]]


class PayloadTypeTypeDef(TypedDict):
    conversational: NotRequired[ConversationalTypeDef]
    blob: NotRequired[Mapping[str, Any]]


class ListMemoryRecordsOutputTypeDef(TypedDict):
    memoryRecordSummaries: List[MemoryRecordSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class RetrieveMemoryRecordsOutputTypeDef(TypedDict):
    memoryRecordSummaries: List[MemoryRecordSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetMemoryRecordOutputTypeDef(TypedDict):
    memoryRecord: MemoryRecordTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class InvokeCodeInterpreterRequestTypeDef(TypedDict):
    codeInterpreterIdentifier: str
    name: ToolNameType
    sessionId: NotRequired[str]
    arguments: NotRequired[ToolArgumentsTypeDef]


class CodeInterpreterStreamOutputTypeDef(TypedDict):
    result: NotRequired[CodeInterpreterResultTypeDef]
    accessDeniedException: NotRequired[AccessDeniedExceptionTypeDef]
    conflictException: NotRequired[ConflictExceptionTypeDef]
    internalServerException: NotRequired[InternalServerExceptionTypeDef]
    resourceNotFoundException: NotRequired[ResourceNotFoundExceptionTypeDef]
    serviceQuotaExceededException: NotRequired[ServiceQuotaExceededExceptionTypeDef]
    throttlingException: NotRequired[ThrottlingExceptionTypeDef]
    validationException: NotRequired[ValidationExceptionTypeDef]


class EventTypeDef(TypedDict):
    memoryId: str
    actorId: str
    sessionId: str
    eventId: str
    eventTimestamp: datetime
    payload: List[PayloadTypeOutputTypeDef]
    branch: NotRequired[BranchTypeDef]


PayloadTypeUnionTypeDef = Union[PayloadTypeTypeDef, PayloadTypeOutputTypeDef]


class InvokeCodeInterpreterResponseTypeDef(TypedDict):
    sessionId: str
    stream: EventStream[CodeInterpreterStreamOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateEventOutputTypeDef(TypedDict):
    event: EventTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetEventOutputTypeDef(TypedDict):
    event: EventTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListEventsOutputTypeDef(TypedDict):
    events: List[EventTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateEventInputTypeDef(TypedDict):
    memoryId: str
    actorId: str
    eventTimestamp: TimestampTypeDef
    payload: Sequence[PayloadTypeUnionTypeDef]
    sessionId: NotRequired[str]
    branch: NotRequired[BranchTypeDef]
    clientToken: NotRequired[str]
