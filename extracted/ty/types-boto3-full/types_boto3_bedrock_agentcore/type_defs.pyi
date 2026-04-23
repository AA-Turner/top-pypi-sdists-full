"""
Type annotations for bedrock-agentcore service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_bedrock_agentcore.type_defs import AgentCardDefinitionTypeDef

    data: AgentCardDefinitionTypeDef = ...
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
    AutomationStreamStatusType,
    BrowserActionStatusType,
    BrowserEnterprisePolicyTypeType,
    BrowserSessionStatusType,
    CodeInterpreterSessionStatusType,
    CommandExecutionStatusType,
    ContentBlockTypeType,
    DescriptorTypeType,
    HarnessConversationRoleType,
    HarnessStopReasonType,
    HarnessToolTypeType,
    HarnessToolUseStatusType,
    HarnessToolUseTypeType,
    LanguageRuntimeType,
    MemoryRecordStatusType,
    MouseButtonType,
    Oauth2FlowTypeType,
    OAuthGrantTypeType,
    OperatorTypeType,
    ProgrammingLanguageType,
    RegistryRecordStatusType,
    ResourceContentTypeType,
    RoleType,
    SessionStatusType,
    TaskStatusType,
    ToolNameType,
    ValidationExceptionReasonType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "A2aDescriptorTypeDef",
    "AccessDeniedExceptionTypeDef",
    "ActorSummaryTypeDef",
    "AgentCardDefinitionTypeDef",
    "AgentSkillsDescriptorTypeDef",
    "AutomationStreamTypeDef",
    "AutomationStreamUpdateTypeDef",
    "BasicAuthTypeDef",
    "BatchCreateMemoryRecordsInputTypeDef",
    "BatchCreateMemoryRecordsOutputTypeDef",
    "BatchDeleteMemoryRecordsInputTypeDef",
    "BatchDeleteMemoryRecordsOutputTypeDef",
    "BatchUpdateMemoryRecordsInputTypeDef",
    "BatchUpdateMemoryRecordsOutputTypeDef",
    "BlobTypeDef",
    "BranchFilterTypeDef",
    "BranchTypeDef",
    "BrowserActionResultTypeDef",
    "BrowserActionTypeDef",
    "BrowserEnterprisePolicyTypeDef",
    "BrowserExtensionTypeDef",
    "BrowserProfileConfigurationTypeDef",
    "BrowserSessionStreamTypeDef",
    "BrowserSessionSummaryTypeDef",
    "CertificateLocationTypeDef",
    "CertificateTypeDef",
    "CodeInterpreterResultTypeDef",
    "CodeInterpreterSessionSummaryTypeDef",
    "CodeInterpreterStreamOutputTypeDef",
    "CompleteResourceTokenAuthRequestTypeDef",
    "ConflictExceptionTypeDef",
    "ContentBlockTypeDef",
    "ContentDeltaEventTypeDef",
    "ContentStopEventTypeDef",
    "ContentTypeDef",
    "ContextTypeDef",
    "ConversationalTypeDef",
    "CreateEventInputTypeDef",
    "CreateEventOutputTypeDef",
    "CustomDescriptorTypeDef",
    "DeleteEventInputTypeDef",
    "DeleteEventOutputTypeDef",
    "DeleteMemoryRecordInputTypeDef",
    "DeleteMemoryRecordOutputTypeDef",
    "DescriptorsTypeDef",
    "EvaluateRequestTypeDef",
    "EvaluateResponseTypeDef",
    "EvaluationContentTypeDef",
    "EvaluationExpectedTrajectoryTypeDef",
    "EvaluationInputTypeDef",
    "EvaluationReferenceInputTypeDef",
    "EvaluationResultContentTypeDef",
    "EvaluationTargetTypeDef",
    "EventMetadataFilterExpressionTypeDef",
    "EventTypeDef",
    "ExternalProxyOutputTypeDef",
    "ExternalProxyTypeDef",
    "ExtractionJobFilterInputTypeDef",
    "ExtractionJobMessagesTypeDef",
    "ExtractionJobMetadataTypeDef",
    "ExtractionJobTypeDef",
    "FilterInputTypeDef",
    "GetAgentCardRequestTypeDef",
    "GetAgentCardResponseTypeDef",
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
    "HarnessAgentCoreBrowserConfigTypeDef",
    "HarnessAgentCoreCodeInterpreterConfigTypeDef",
    "HarnessAgentCoreGatewayConfigTypeDef",
    "HarnessBedrockModelConfigTypeDef",
    "HarnessContentBlockDeltaEventTypeDef",
    "HarnessContentBlockDeltaTypeDef",
    "HarnessContentBlockStartEventTypeDef",
    "HarnessContentBlockStartTypeDef",
    "HarnessContentBlockStopEventTypeDef",
    "HarnessContentBlockTypeDef",
    "HarnessGatewayOutboundAuthTypeDef",
    "HarnessGeminiModelConfigTypeDef",
    "HarnessInlineFunctionConfigTypeDef",
    "HarnessMessageStartEventTypeDef",
    "HarnessMessageStopEventTypeDef",
    "HarnessMessageTypeDef",
    "HarnessMetadataEventTypeDef",
    "HarnessModelConfigurationTypeDef",
    "HarnessOpenAiModelConfigTypeDef",
    "HarnessReasoningContentBlockDeltaTypeDef",
    "HarnessReasoningContentBlockTypeDef",
    "HarnessReasoningTextBlockTypeDef",
    "HarnessRemoteMcpConfigTypeDef",
    "HarnessSkillTypeDef",
    "HarnessStreamMetricsTypeDef",
    "HarnessSystemContentBlockTypeDef",
    "HarnessTokenUsageTypeDef",
    "HarnessToolConfigurationTypeDef",
    "HarnessToolResultBlockDeltaTypeDef",
    "HarnessToolResultBlockStartTypeDef",
    "HarnessToolResultBlockTypeDef",
    "HarnessToolResultContentBlockTypeDef",
    "HarnessToolTypeDef",
    "HarnessToolUseBlockDeltaTypeDef",
    "HarnessToolUseBlockStartTypeDef",
    "HarnessToolUseBlockTypeDef",
    "InputContentBlockTypeDef",
    "InternalServerExceptionTypeDef",
    "InvokeAgentRuntimeCommandRequestBodyTypeDef",
    "InvokeAgentRuntimeCommandRequestTypeDef",
    "InvokeAgentRuntimeCommandResponseTypeDef",
    "InvokeAgentRuntimeCommandStreamOutputTypeDef",
    "InvokeAgentRuntimeRequestTypeDef",
    "InvokeAgentRuntimeResponseTypeDef",
    "InvokeBrowserRequestTypeDef",
    "InvokeBrowserResponseTypeDef",
    "InvokeCodeInterpreterRequestTypeDef",
    "InvokeCodeInterpreterResponseTypeDef",
    "InvokeHarnessRequestTypeDef",
    "InvokeHarnessResponseTypeDef",
    "InvokeHarnessStreamOutputTypeDef",
    "KeyPressArgumentsTypeDef",
    "KeyPressResultTypeDef",
    "KeyShortcutArgumentsTypeDef",
    "KeyShortcutResultTypeDef",
    "KeyTypeArgumentsTypeDef",
    "KeyTypeResultTypeDef",
    "LeftExpressionTypeDef",
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
    "ListMemoryExtractionJobsInputPaginateTypeDef",
    "ListMemoryExtractionJobsInputTypeDef",
    "ListMemoryExtractionJobsOutputTypeDef",
    "ListMemoryRecordsInputPaginateTypeDef",
    "ListMemoryRecordsInputTypeDef",
    "ListMemoryRecordsOutputTypeDef",
    "ListSessionsInputPaginateTypeDef",
    "ListSessionsInputTypeDef",
    "ListSessionsOutputTypeDef",
    "LiveViewStreamTypeDef",
    "McpDescriptorTypeDef",
    "MemoryContentTypeDef",
    "MemoryMetadataFilterExpressionTypeDef",
    "MemoryRecordCreateInputTypeDef",
    "MemoryRecordDeleteInputTypeDef",
    "MemoryRecordOutputTypeDef",
    "MemoryRecordSummaryTypeDef",
    "MemoryRecordTypeDef",
    "MemoryRecordUpdateInputTypeDef",
    "MessageMetadataTypeDef",
    "MetadataValueTypeDef",
    "MouseClickArgumentsTypeDef",
    "MouseClickResultTypeDef",
    "MouseDragArgumentsTypeDef",
    "MouseDragResultTypeDef",
    "MouseMoveArgumentsTypeDef",
    "MouseMoveResultTypeDef",
    "MouseScrollArgumentsTypeDef",
    "MouseScrollResultTypeDef",
    "OAuthCredentialProviderTypeDef",
    "PaginatorConfigTypeDef",
    "PayloadTypeOutputTypeDef",
    "PayloadTypeTypeDef",
    "PayloadTypeUnionTypeDef",
    "ProxyBypassOutputTypeDef",
    "ProxyBypassTypeDef",
    "ProxyConfigurationOutputTypeDef",
    "ProxyConfigurationTypeDef",
    "ProxyConfigurationUnionTypeDef",
    "ProxyCredentialsTypeDef",
    "ProxyOutputTypeDef",
    "ProxyTypeDef",
    "RegistryRecordSummaryTypeDef",
    "ResourceContentTypeDef",
    "ResourceLocationTypeDef",
    "ResourceNotFoundExceptionTypeDef",
    "ResponseChunkTypeDef",
    "ResponseMetadataTypeDef",
    "RetrieveMemoryRecordsInputPaginateTypeDef",
    "RetrieveMemoryRecordsInputTypeDef",
    "RetrieveMemoryRecordsOutputTypeDef",
    "RightExpressionTypeDef",
    "RuntimeClientErrorTypeDef",
    "S3LocationTypeDef",
    "SaveBrowserSessionProfileRequestTypeDef",
    "SaveBrowserSessionProfileResponseTypeDef",
    "ScreenshotArgumentsTypeDef",
    "ScreenshotResultTypeDef",
    "SearchCriteriaTypeDef",
    "SearchRegistryRecordsRequestTypeDef",
    "SearchRegistryRecordsResponseTypeDef",
    "SecretsManagerLocationTypeDef",
    "ServerDefinitionTypeDef",
    "ServiceQuotaExceededExceptionTypeDef",
    "SessionFilterTypeDef",
    "SessionSummaryTypeDef",
    "SkillDefinitionTypeDef",
    "SkillMdDefinitionTypeDef",
    "SpanContextTypeDef",
    "StartBrowserSessionRequestTypeDef",
    "StartBrowserSessionResponseTypeDef",
    "StartCodeInterpreterSessionRequestTypeDef",
    "StartCodeInterpreterSessionResponseTypeDef",
    "StartMemoryExtractionJobInputTypeDef",
    "StartMemoryExtractionJobOutputTypeDef",
    "StopBrowserSessionRequestTypeDef",
    "StopBrowserSessionResponseTypeDef",
    "StopCodeInterpreterSessionRequestTypeDef",
    "StopCodeInterpreterSessionResponseTypeDef",
    "StopRuntimeSessionRequestTypeDef",
    "StopRuntimeSessionResponseTypeDef",
    "StreamUpdateTypeDef",
    "ThrottlingExceptionTypeDef",
    "TimestampTypeDef",
    "TokenUsageTypeDef",
    "ToolArgumentsTypeDef",
    "ToolResultStructuredContentTypeDef",
    "ToolsDefinitionTypeDef",
    "UpdateBrowserStreamRequestTypeDef",
    "UpdateBrowserStreamResponseTypeDef",
    "UserIdentifierTypeDef",
    "ValidationExceptionFieldTypeDef",
    "ValidationExceptionTypeDef",
    "ViewPortTypeDef",
)

class AgentCardDefinitionTypeDef(TypedDict):
    schemaVersion: NotRequired[str]
    inlineContent: NotRequired[str]

class AccessDeniedExceptionTypeDef(TypedDict):
    message: NotRequired[str]

class ActorSummaryTypeDef(TypedDict):
    actorId: str

class SkillDefinitionTypeDef(TypedDict):
    schemaVersion: NotRequired[str]
    inlineContent: NotRequired[str]

class SkillMdDefinitionTypeDef(TypedDict):
    inlineContent: NotRequired[str]

class AutomationStreamTypeDef(TypedDict):
    streamEndpoint: str
    streamStatus: AutomationStreamStatusType

class AutomationStreamUpdateTypeDef(TypedDict):
    streamStatus: NotRequired[AutomationStreamStatusType]

class BasicAuthTypeDef(TypedDict):
    secretArn: str

class MemoryRecordOutputTypeDef(TypedDict):
    memoryRecordId: str
    status: MemoryRecordStatusType
    requestIdentifier: NotRequired[str]
    errorCode: NotRequired[int]
    errorMessage: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class MemoryRecordDeleteInputTypeDef(TypedDict):
    memoryRecordId: str

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class BranchFilterTypeDef(TypedDict):
    name: str
    includeParentBranches: NotRequired[bool]

class BranchTypeDef(TypedDict):
    name: str
    rootEventId: NotRequired[str]

class KeyPressResultTypeDef(TypedDict):
    status: BrowserActionStatusType
    error: NotRequired[str]

class KeyShortcutResultTypeDef(TypedDict):
    status: BrowserActionStatusType
    error: NotRequired[str]

class KeyTypeResultTypeDef(TypedDict):
    status: BrowserActionStatusType
    error: NotRequired[str]

class MouseClickResultTypeDef(TypedDict):
    status: BrowserActionStatusType
    error: NotRequired[str]

class MouseDragResultTypeDef(TypedDict):
    status: BrowserActionStatusType
    error: NotRequired[str]

class MouseMoveResultTypeDef(TypedDict):
    status: BrowserActionStatusType
    error: NotRequired[str]

class MouseScrollResultTypeDef(TypedDict):
    status: BrowserActionStatusType
    error: NotRequired[str]

class ScreenshotResultTypeDef(TypedDict):
    status: BrowserActionStatusType
    error: NotRequired[str]
    data: NotRequired[bytes]

class KeyPressArgumentsTypeDef(TypedDict):
    key: str
    presses: NotRequired[int]

class KeyShortcutArgumentsTypeDef(TypedDict):
    keys: Sequence[str]

class KeyTypeArgumentsTypeDef(TypedDict):
    text: str

class MouseClickArgumentsTypeDef(TypedDict):
    x: int
    y: int
    button: NotRequired[MouseButtonType]
    clickCount: NotRequired[int]

class MouseDragArgumentsTypeDef(TypedDict):
    endX: int
    endY: int
    startX: int
    startY: int
    button: NotRequired[MouseButtonType]

class MouseMoveArgumentsTypeDef(TypedDict):
    x: int
    y: int

class MouseScrollArgumentsTypeDef(TypedDict):
    x: int
    y: int
    deltaX: NotRequired[int]
    deltaY: NotRequired[int]

ScreenshotArgumentsTypeDef = TypedDict(
    "ScreenshotArgumentsTypeDef",
    {
        "format": NotRequired[Literal["PNG"]],
    },
)

class BrowserProfileConfigurationTypeDef(TypedDict):
    profileIdentifier: str

class LiveViewStreamTypeDef(TypedDict):
    streamEndpoint: NotRequired[str]

class BrowserSessionSummaryTypeDef(TypedDict):
    browserIdentifier: str
    sessionId: str
    status: BrowserSessionStatusType
    createdAt: datetime
    name: NotRequired[str]
    lastUpdatedAt: NotRequired[datetime]

class SecretsManagerLocationTypeDef(TypedDict):
    secretArn: str

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

class UserIdentifierTypeDef(TypedDict):
    userToken: NotRequired[str]
    userId: NotRequired[str]

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

class ContentDeltaEventTypeDef(TypedDict):
    stdout: NotRequired[str]
    stderr: NotRequired[str]

class ContentStopEventTypeDef(TypedDict):
    exitCode: int
    status: CommandExecutionStatusType

class ContentTypeDef(TypedDict):
    text: NotRequired[str]

class SpanContextTypeDef(TypedDict):
    sessionId: str
    traceId: NotRequired[str]
    spanId: NotRequired[str]

class MetadataValueTypeDef(TypedDict):
    stringValue: NotRequired[str]

TimestampTypeDef = Union[datetime, str]

class CustomDescriptorTypeDef(TypedDict):
    inlineContent: NotRequired[str]

class DeleteEventInputTypeDef(TypedDict):
    memoryId: str
    sessionId: str
    eventId: str
    actorId: str

class DeleteMemoryRecordInputTypeDef(TypedDict):
    memoryId: str
    memoryRecordId: str

class EvaluationInputTypeDef(TypedDict):
    sessionSpans: NotRequired[Sequence[Mapping[str, Any]]]

class EvaluationTargetTypeDef(TypedDict):
    spanIds: NotRequired[Sequence[str]]
    traceIds: NotRequired[Sequence[str]]

class EvaluationContentTypeDef(TypedDict):
    text: NotRequired[str]

class EvaluationExpectedTrajectoryTypeDef(TypedDict):
    toolNames: NotRequired[Sequence[str]]

class TokenUsageTypeDef(TypedDict):
    inputTokens: NotRequired[int]
    outputTokens: NotRequired[int]
    totalTokens: NotRequired[int]

class LeftExpressionTypeDef(TypedDict):
    metadataKey: NotRequired[str]

class ExtractionJobFilterInputTypeDef(TypedDict):
    strategyId: NotRequired[str]
    sessionId: NotRequired[str]
    actorId: NotRequired[str]
    status: NotRequired[Literal["FAILED"]]

class MessageMetadataTypeDef(TypedDict):
    eventId: str
    messageIndex: int

class ExtractionJobTypeDef(TypedDict):
    jobId: str

class GetAgentCardRequestTypeDef(TypedDict):
    agentRuntimeArn: str
    runtimeSessionId: NotRequired[str]
    qualifier: NotRequired[str]

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
    sessionUri: NotRequired[str]
    resourceOauth2ReturnUrl: NotRequired[str]
    forceAuthentication: NotRequired[bool]
    customParameters: NotRequired[Mapping[str, str]]
    customState: NotRequired[str]

class GetWorkloadAccessTokenForJWTRequestTypeDef(TypedDict):
    workloadName: str
    userToken: str

class GetWorkloadAccessTokenForUserIdRequestTypeDef(TypedDict):
    workloadName: str
    userId: str

class GetWorkloadAccessTokenRequestTypeDef(TypedDict):
    workloadName: str

class HarnessAgentCoreBrowserConfigTypeDef(TypedDict):
    browserArn: NotRequired[str]

class HarnessAgentCoreCodeInterpreterConfigTypeDef(TypedDict):
    codeInterpreterArn: NotRequired[str]

class HarnessBedrockModelConfigTypeDef(TypedDict):
    modelId: str
    maxTokens: NotRequired[int]
    temperature: NotRequired[float]
    topP: NotRequired[float]

class HarnessReasoningContentBlockDeltaTypeDef(TypedDict):
    text: NotRequired[str]
    redactedContent: NotRequired[bytes]
    signature: NotRequired[str]

class HarnessToolResultBlockDeltaTypeDef(TypedDict):
    text: NotRequired[str]
    json: NotRequired[dict[str, Any]]

HarnessToolUseBlockDeltaTypeDef = TypedDict(
    "HarnessToolUseBlockDeltaTypeDef",
    {
        "input": str,
    },
)

class HarnessToolResultBlockStartTypeDef(TypedDict):
    toolUseId: str
    status: NotRequired[HarnessToolUseStatusType]

HarnessToolUseBlockStartTypeDef = TypedDict(
    "HarnessToolUseBlockStartTypeDef",
    {
        "toolUseId": str,
        "name": str,
        "type": NotRequired[HarnessToolUseTypeType],
        "serverName": NotRequired[str],
    },
)

class HarnessContentBlockStopEventTypeDef(TypedDict):
    contentBlockIndex: int

HarnessToolUseBlockTypeDef = TypedDict(
    "HarnessToolUseBlockTypeDef",
    {
        "name": str,
        "toolUseId": str,
        "input": Mapping[str, Any],
        "type": NotRequired[HarnessToolUseTypeType],
        "serverName": NotRequired[str],
    },
)

class OAuthCredentialProviderTypeDef(TypedDict):
    providerArn: str
    scopes: Sequence[str]
    customParameters: NotRequired[Mapping[str, str]]
    grantType: NotRequired[OAuthGrantTypeType]
    defaultReturnUrl: NotRequired[str]

class HarnessGeminiModelConfigTypeDef(TypedDict):
    modelId: str
    apiKeyArn: str
    maxTokens: NotRequired[int]
    temperature: NotRequired[float]
    topP: NotRequired[float]
    topK: NotRequired[int]

class HarnessInlineFunctionConfigTypeDef(TypedDict):
    description: str
    inputSchema: Mapping[str, Any]

class HarnessMessageStartEventTypeDef(TypedDict):
    role: HarnessConversationRoleType

class HarnessMessageStopEventTypeDef(TypedDict):
    stopReason: HarnessStopReasonType

class HarnessStreamMetricsTypeDef(TypedDict):
    latencyMs: int

class HarnessTokenUsageTypeDef(TypedDict):
    inputTokens: int
    outputTokens: int
    totalTokens: int
    cacheReadInputTokens: NotRequired[int]
    cacheWriteInputTokens: NotRequired[int]

class HarnessOpenAiModelConfigTypeDef(TypedDict):
    modelId: str
    apiKeyArn: str
    maxTokens: NotRequired[int]
    temperature: NotRequired[float]
    topP: NotRequired[float]

class HarnessReasoningTextBlockTypeDef(TypedDict):
    text: str
    signature: NotRequired[str]

class HarnessRemoteMcpConfigTypeDef(TypedDict):
    url: str
    headers: NotRequired[Mapping[str, str]]

class HarnessSkillTypeDef(TypedDict):
    path: NotRequired[str]

class HarnessSystemContentBlockTypeDef(TypedDict):
    text: NotRequired[str]

class HarnessToolResultContentBlockTypeDef(TypedDict):
    text: NotRequired[str]
    json: NotRequired[Mapping[str, Any]]

class InvokeAgentRuntimeCommandRequestBodyTypeDef(TypedDict):
    command: str
    timeout: NotRequired[int]

class RuntimeClientErrorTypeDef(TypedDict):
    message: NotRequired[str]

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
    namespace: NotRequired[str]
    namespacePath: NotRequired[str]
    memoryStrategyId: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class SessionFilterTypeDef(TypedDict):
    eventFilter: NotRequired[Literal["HAS_EVENTS"]]

class SessionSummaryTypeDef(TypedDict):
    sessionId: str
    actorId: str
    createdAt: datetime

class ServerDefinitionTypeDef(TypedDict):
    schemaVersion: NotRequired[str]
    inlineContent: NotRequired[str]

class ToolsDefinitionTypeDef(TypedDict):
    protocolVersion: NotRequired[str]
    inlineContent: NotRequired[str]

class MemoryContentTypeDef(TypedDict):
    text: NotRequired[str]

class ProxyBypassOutputTypeDef(TypedDict):
    domainPatterns: NotRequired[list[str]]

class ProxyBypassTypeDef(TypedDict):
    domainPatterns: NotRequired[Sequence[str]]

class S3LocationTypeDef(TypedDict):
    bucket: str
    prefix: str
    versionId: NotRequired[str]

class SaveBrowserSessionProfileRequestTypeDef(TypedDict):
    profileIdentifier: str
    browserIdentifier: str
    sessionId: str
    traceId: NotRequired[str]
    traceParent: NotRequired[str]
    clientToken: NotRequired[str]

class SearchRegistryRecordsRequestTypeDef(TypedDict):
    searchQuery: str
    registryIds: Sequence[str]
    maxResults: NotRequired[int]
    filters: NotRequired[Mapping[str, Any]]

class StopBrowserSessionRequestTypeDef(TypedDict):
    browserIdentifier: str
    sessionId: str
    traceId: NotRequired[str]
    traceParent: NotRequired[str]
    clientToken: NotRequired[str]

class StopCodeInterpreterSessionRequestTypeDef(TypedDict):
    codeInterpreterIdentifier: str
    sessionId: str
    traceId: NotRequired[str]
    traceParent: NotRequired[str]
    clientToken: NotRequired[str]

class StopRuntimeSessionRequestTypeDef(TypedDict):
    runtimeSessionId: str
    agentRuntimeArn: str
    qualifier: NotRequired[str]
    clientToken: NotRequired[str]

class ValidationExceptionFieldTypeDef(TypedDict):
    name: str
    message: str

class A2aDescriptorTypeDef(TypedDict):
    agentCard: AgentCardDefinitionTypeDef

class AgentSkillsDescriptorTypeDef(TypedDict):
    skillMd: SkillMdDefinitionTypeDef
    skillDefinition: NotRequired[SkillDefinitionTypeDef]

class StreamUpdateTypeDef(TypedDict):
    automationStreamUpdate: NotRequired[AutomationStreamUpdateTypeDef]

class ProxyCredentialsTypeDef(TypedDict):
    basicAuth: NotRequired[BasicAuthTypeDef]

class BatchCreateMemoryRecordsOutputTypeDef(TypedDict):
    successfulRecords: list[MemoryRecordOutputTypeDef]
    failedRecords: list[MemoryRecordOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDeleteMemoryRecordsOutputTypeDef(TypedDict):
    successfulRecords: list[MemoryRecordOutputTypeDef]
    failedRecords: list[MemoryRecordOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchUpdateMemoryRecordsOutputTypeDef(TypedDict):
    successfulRecords: list[MemoryRecordOutputTypeDef]
    failedRecords: list[MemoryRecordOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteEventOutputTypeDef(TypedDict):
    eventId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteMemoryRecordOutputTypeDef(TypedDict):
    memoryRecordId: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetAgentCardResponseTypeDef(TypedDict):
    runtimeSessionId: str
    agentCard: dict[str, Any]
    statusCode: int
    ResponseMetadata: ResponseMetadataTypeDef

class GetResourceApiKeyResponseTypeDef(TypedDict):
    apiKey: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetResourceOauth2TokenResponseTypeDef(TypedDict):
    authorizationUrl: str
    accessToken: str
    sessionUri: str
    sessionStatus: SessionStatusType
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
    actorSummaries: list[ActorSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class SaveBrowserSessionProfileResponseTypeDef(TypedDict):
    profileIdentifier: str
    browserIdentifier: str
    sessionId: str
    lastUpdatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class StartCodeInterpreterSessionResponseTypeDef(TypedDict):
    codeInterpreterIdentifier: str
    sessionId: str
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class StartMemoryExtractionJobOutputTypeDef(TypedDict):
    jobId: str
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

class StopRuntimeSessionResponseTypeDef(TypedDict):
    runtimeSessionId: str
    statusCode: int
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDeleteMemoryRecordsInputTypeDef(TypedDict):
    memoryId: str
    records: Sequence[MemoryRecordDeleteInputTypeDef]

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
    accountId: NotRequired[str]

class BrowserActionResultTypeDef(TypedDict):
    mouseClick: NotRequired[MouseClickResultTypeDef]
    mouseMove: NotRequired[MouseMoveResultTypeDef]
    mouseDrag: NotRequired[MouseDragResultTypeDef]
    mouseScroll: NotRequired[MouseScrollResultTypeDef]
    keyType: NotRequired[KeyTypeResultTypeDef]
    keyPress: NotRequired[KeyPressResultTypeDef]
    keyShortcut: NotRequired[KeyShortcutResultTypeDef]
    screenshot: NotRequired[ScreenshotResultTypeDef]

class BrowserActionTypeDef(TypedDict):
    mouseClick: NotRequired[MouseClickArgumentsTypeDef]
    mouseMove: NotRequired[MouseMoveArgumentsTypeDef]
    mouseDrag: NotRequired[MouseDragArgumentsTypeDef]
    mouseScroll: NotRequired[MouseScrollArgumentsTypeDef]
    keyType: NotRequired[KeyTypeArgumentsTypeDef]
    keyPress: NotRequired[KeyPressArgumentsTypeDef]
    keyShortcut: NotRequired[KeyShortcutArgumentsTypeDef]
    screenshot: NotRequired[ScreenshotArgumentsTypeDef]

class BrowserSessionStreamTypeDef(TypedDict):
    automationStream: AutomationStreamTypeDef
    liveViewStream: NotRequired[LiveViewStreamTypeDef]

class ListBrowserSessionsResponseTypeDef(TypedDict):
    items: list[BrowserSessionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CertificateLocationTypeDef(TypedDict):
    secretsManager: NotRequired[SecretsManagerLocationTypeDef]

class ListCodeInterpreterSessionsResponseTypeDef(TypedDict):
    items: list[CodeInterpreterSessionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CompleteResourceTokenAuthRequestTypeDef(TypedDict):
    userIdentifier: UserIdentifierTypeDef
    sessionUri: str

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

class ResponseChunkTypeDef(TypedDict):
    contentStart: NotRequired[dict[str, Any]]
    contentDelta: NotRequired[ContentDeltaEventTypeDef]
    contentStop: NotRequired[ContentStopEventTypeDef]

class ConversationalTypeDef(TypedDict):
    content: ContentTypeDef
    role: RoleType

class ContextTypeDef(TypedDict):
    spanContext: NotRequired[SpanContextTypeDef]

class RightExpressionTypeDef(TypedDict):
    metadataValue: NotRequired[MetadataValueTypeDef]

ListMemoryExtractionJobsInputTypeDef = TypedDict(
    "ListMemoryExtractionJobsInputTypeDef",
    {
        "memoryId": str,
        "maxResults": NotRequired[int],
        "filter": NotRequired[ExtractionJobFilterInputTypeDef],
        "nextToken": NotRequired[str],
    },
)

class ExtractionJobMessagesTypeDef(TypedDict):
    messagesList: NotRequired[list[MessageMetadataTypeDef]]

class StartMemoryExtractionJobInputTypeDef(TypedDict):
    memoryId: str
    extractionJob: ExtractionJobTypeDef
    clientToken: NotRequired[str]

class HarnessContentBlockDeltaTypeDef(TypedDict):
    text: NotRequired[str]
    toolUse: NotRequired[HarnessToolUseBlockDeltaTypeDef]
    toolResult: NotRequired[list[HarnessToolResultBlockDeltaTypeDef]]
    reasoningContent: NotRequired[HarnessReasoningContentBlockDeltaTypeDef]

class HarnessContentBlockStartTypeDef(TypedDict):
    toolUse: NotRequired[HarnessToolUseBlockStartTypeDef]
    toolResult: NotRequired[HarnessToolResultBlockStartTypeDef]

class HarnessGatewayOutboundAuthTypeDef(TypedDict):
    awsIam: NotRequired[Mapping[str, Any]]
    none: NotRequired[Mapping[str, Any]]
    oauth: NotRequired[OAuthCredentialProviderTypeDef]

class HarnessMetadataEventTypeDef(TypedDict):
    usage: HarnessTokenUsageTypeDef
    metrics: HarnessStreamMetricsTypeDef

class HarnessModelConfigurationTypeDef(TypedDict):
    bedrockModelConfig: NotRequired[HarnessBedrockModelConfigTypeDef]
    openAiModelConfig: NotRequired[HarnessOpenAiModelConfigTypeDef]
    geminiModelConfig: NotRequired[HarnessGeminiModelConfigTypeDef]

class HarnessReasoningContentBlockTypeDef(TypedDict):
    reasoningText: NotRequired[HarnessReasoningTextBlockTypeDef]
    redactedContent: NotRequired[BlobTypeDef]

HarnessToolResultBlockTypeDef = TypedDict(
    "HarnessToolResultBlockTypeDef",
    {
        "toolUseId": str,
        "content": Sequence[HarnessToolResultContentBlockTypeDef],
        "status": NotRequired[HarnessToolUseStatusType],
        "type": NotRequired[HarnessToolUseTypeType],
    },
)

class InvokeAgentRuntimeCommandRequestTypeDef(TypedDict):
    agentRuntimeArn: str
    body: InvokeAgentRuntimeCommandRequestBodyTypeDef
    contentType: NotRequired[str]
    accept: NotRequired[str]
    runtimeSessionId: NotRequired[str]
    traceId: NotRequired[str]
    traceParent: NotRequired[str]
    traceState: NotRequired[str]
    baggage: NotRequired[str]
    qualifier: NotRequired[str]
    accountId: NotRequired[str]

class ListActorsInputPaginateTypeDef(TypedDict):
    memoryId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListMemoryExtractionJobsInputPaginateTypeDef = TypedDict(
    "ListMemoryExtractionJobsInputPaginateTypeDef",
    {
        "memoryId": str,
        "filter": NotRequired[ExtractionJobFilterInputTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListMemoryRecordsInputPaginateTypeDef(TypedDict):
    memoryId: str
    namespace: NotRequired[str]
    namespacePath: NotRequired[str]
    memoryStrategyId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListSessionsInputPaginateTypeDef = TypedDict(
    "ListSessionsInputPaginateTypeDef",
    {
        "memoryId": str,
        "actorId": str,
        "filter": NotRequired[SessionFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListSessionsInputTypeDef = TypedDict(
    "ListSessionsInputTypeDef",
    {
        "memoryId": str,
        "actorId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "filter": NotRequired[SessionFilterTypeDef],
    },
)

class ListSessionsOutputTypeDef(TypedDict):
    sessionSummaries: list[SessionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class McpDescriptorTypeDef(TypedDict):
    server: ServerDefinitionTypeDef
    tools: ToolsDefinitionTypeDef

class MemoryRecordCreateInputTypeDef(TypedDict):
    requestIdentifier: str
    namespaces: Sequence[str]
    content: MemoryContentTypeDef
    timestamp: TimestampTypeDef
    memoryStrategyId: NotRequired[str]

class MemoryRecordSummaryTypeDef(TypedDict):
    memoryRecordId: str
    content: MemoryContentTypeDef
    memoryStrategyId: str
    namespaces: list[str]
    createdAt: datetime
    score: NotRequired[float]
    metadata: NotRequired[dict[str, MetadataValueTypeDef]]

class MemoryRecordTypeDef(TypedDict):
    memoryRecordId: str
    content: MemoryContentTypeDef
    memoryStrategyId: str
    namespaces: list[str]
    createdAt: datetime
    metadata: NotRequired[dict[str, MetadataValueTypeDef]]

class MemoryRecordUpdateInputTypeDef(TypedDict):
    memoryRecordId: str
    timestamp: TimestampTypeDef
    content: NotRequired[MemoryContentTypeDef]
    namespaces: NotRequired[Sequence[str]]
    memoryStrategyId: NotRequired[str]

class ResourceLocationTypeDef(TypedDict):
    s3: NotRequired[S3LocationTypeDef]

class ValidationExceptionTypeDef(TypedDict):
    message: str
    reason: ValidationExceptionReasonType
    fieldList: NotRequired[list[ValidationExceptionFieldTypeDef]]

class UpdateBrowserStreamRequestTypeDef(TypedDict):
    browserIdentifier: str
    sessionId: str
    streamUpdate: StreamUpdateTypeDef
    clientToken: NotRequired[str]

class ExternalProxyOutputTypeDef(TypedDict):
    server: str
    port: int
    domainPatterns: NotRequired[list[str]]
    credentials: NotRequired[ProxyCredentialsTypeDef]

class ExternalProxyTypeDef(TypedDict):
    server: str
    port: int
    domainPatterns: NotRequired[Sequence[str]]
    credentials: NotRequired[ProxyCredentialsTypeDef]

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
    runtime: NotRequired[LanguageRuntimeType]

class InvokeBrowserResponseTypeDef(TypedDict):
    result: BrowserActionResultTypeDef
    sessionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class InvokeBrowserRequestTypeDef(TypedDict):
    browserIdentifier: str
    sessionId: str
    action: BrowserActionTypeDef

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

class CertificateTypeDef(TypedDict):
    location: CertificateLocationTypeDef

class CodeInterpreterResultTypeDef(TypedDict):
    content: list[ContentBlockTypeDef]
    structuredContent: NotRequired[ToolResultStructuredContentTypeDef]
    isError: NotRequired[bool]

class PayloadTypeOutputTypeDef(TypedDict):
    conversational: NotRequired[ConversationalTypeDef]
    blob: NotRequired[dict[str, Any]]

class PayloadTypeTypeDef(TypedDict):
    conversational: NotRequired[ConversationalTypeDef]
    blob: NotRequired[Mapping[str, Any]]

class EvaluationReferenceInputTypeDef(TypedDict):
    context: ContextTypeDef
    expectedResponse: NotRequired[EvaluationContentTypeDef]
    assertions: NotRequired[Sequence[EvaluationContentTypeDef]]
    expectedTrajectory: NotRequired[EvaluationExpectedTrajectoryTypeDef]

class EvaluationResultContentTypeDef(TypedDict):
    evaluatorArn: str
    evaluatorId: str
    evaluatorName: str
    context: ContextTypeDef
    explanation: NotRequired[str]
    value: NotRequired[float]
    label: NotRequired[str]
    tokenUsage: NotRequired[TokenUsageTypeDef]
    errorMessage: NotRequired[str]
    errorCode: NotRequired[str]
    ignoredReferenceInputFields: NotRequired[list[str]]

EventMetadataFilterExpressionTypeDef = TypedDict(
    "EventMetadataFilterExpressionTypeDef",
    {
        "left": LeftExpressionTypeDef,
        "operator": OperatorTypeType,
        "right": NotRequired[RightExpressionTypeDef],
    },
)
MemoryMetadataFilterExpressionTypeDef = TypedDict(
    "MemoryMetadataFilterExpressionTypeDef",
    {
        "left": LeftExpressionTypeDef,
        "operator": OperatorTypeType,
        "right": NotRequired[RightExpressionTypeDef],
    },
)

class ExtractionJobMetadataTypeDef(TypedDict):
    jobID: str
    messages: ExtractionJobMessagesTypeDef
    status: NotRequired[Literal["FAILED"]]
    failureReason: NotRequired[str]
    strategyId: NotRequired[str]
    sessionId: NotRequired[str]
    actorId: NotRequired[str]

class HarnessContentBlockDeltaEventTypeDef(TypedDict):
    contentBlockIndex: int
    delta: HarnessContentBlockDeltaTypeDef

class HarnessContentBlockStartEventTypeDef(TypedDict):
    contentBlockIndex: int
    start: HarnessContentBlockStartTypeDef

class HarnessAgentCoreGatewayConfigTypeDef(TypedDict):
    gatewayArn: str
    outboundAuth: NotRequired[HarnessGatewayOutboundAuthTypeDef]

class HarnessContentBlockTypeDef(TypedDict):
    text: NotRequired[str]
    toolUse: NotRequired[HarnessToolUseBlockTypeDef]
    toolResult: NotRequired[HarnessToolResultBlockTypeDef]
    reasoningContent: NotRequired[HarnessReasoningContentBlockTypeDef]

class DescriptorsTypeDef(TypedDict):
    mcp: NotRequired[McpDescriptorTypeDef]
    a2a: NotRequired[A2aDescriptorTypeDef]
    custom: NotRequired[CustomDescriptorTypeDef]
    agentSkills: NotRequired[AgentSkillsDescriptorTypeDef]

class BatchCreateMemoryRecordsInputTypeDef(TypedDict):
    memoryId: str
    records: Sequence[MemoryRecordCreateInputTypeDef]
    clientToken: NotRequired[str]

class ListMemoryRecordsOutputTypeDef(TypedDict):
    memoryRecordSummaries: list[MemoryRecordSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class RetrieveMemoryRecordsOutputTypeDef(TypedDict):
    memoryRecordSummaries: list[MemoryRecordSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetMemoryRecordOutputTypeDef(TypedDict):
    memoryRecord: MemoryRecordTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class BatchUpdateMemoryRecordsInputTypeDef(TypedDict):
    memoryId: str
    records: Sequence[MemoryRecordUpdateInputTypeDef]

BrowserEnterprisePolicyTypeDef = TypedDict(
    "BrowserEnterprisePolicyTypeDef",
    {
        "location": ResourceLocationTypeDef,
        "type": NotRequired[BrowserEnterprisePolicyTypeType],
    },
)

class BrowserExtensionTypeDef(TypedDict):
    location: ResourceLocationTypeDef

class InvokeAgentRuntimeCommandStreamOutputTypeDef(TypedDict):
    chunk: NotRequired[ResponseChunkTypeDef]
    accessDeniedException: NotRequired[AccessDeniedExceptionTypeDef]
    internalServerException: NotRequired[InternalServerExceptionTypeDef]
    resourceNotFoundException: NotRequired[ResourceNotFoundExceptionTypeDef]
    serviceQuotaExceededException: NotRequired[ServiceQuotaExceededExceptionTypeDef]
    throttlingException: NotRequired[ThrottlingExceptionTypeDef]
    validationException: NotRequired[ValidationExceptionTypeDef]
    runtimeClientError: NotRequired[RuntimeClientErrorTypeDef]

class ProxyOutputTypeDef(TypedDict):
    externalProxy: NotRequired[ExternalProxyOutputTypeDef]

class ProxyTypeDef(TypedDict):
    externalProxy: NotRequired[ExternalProxyTypeDef]

class InvokeCodeInterpreterRequestTypeDef(TypedDict):
    codeInterpreterIdentifier: str
    name: ToolNameType
    sessionId: NotRequired[str]
    traceId: NotRequired[str]
    traceParent: NotRequired[str]
    arguments: NotRequired[ToolArgumentsTypeDef]

class GetCodeInterpreterSessionResponseTypeDef(TypedDict):
    codeInterpreterIdentifier: str
    sessionId: str
    name: str
    createdAt: datetime
    sessionTimeoutSeconds: int
    status: CodeInterpreterSessionStatusType
    certificates: list[CertificateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class StartCodeInterpreterSessionRequestTypeDef(TypedDict):
    codeInterpreterIdentifier: str
    traceId: NotRequired[str]
    traceParent: NotRequired[str]
    name: NotRequired[str]
    sessionTimeoutSeconds: NotRequired[int]
    certificates: NotRequired[Sequence[CertificateTypeDef]]
    clientToken: NotRequired[str]

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
    payload: list[PayloadTypeOutputTypeDef]
    branch: NotRequired[BranchTypeDef]
    metadata: NotRequired[dict[str, MetadataValueTypeDef]]

PayloadTypeUnionTypeDef = Union[PayloadTypeTypeDef, PayloadTypeOutputTypeDef]

class EvaluateRequestTypeDef(TypedDict):
    evaluatorId: str
    evaluationInput: EvaluationInputTypeDef
    evaluationTarget: NotRequired[EvaluationTargetTypeDef]
    evaluationReferenceInputs: NotRequired[Sequence[EvaluationReferenceInputTypeDef]]

class EvaluateResponseTypeDef(TypedDict):
    evaluationResults: list[EvaluationResultContentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class FilterInputTypeDef(TypedDict):
    branch: NotRequired[BranchFilterTypeDef]
    eventMetadata: NotRequired[Sequence[EventMetadataFilterExpressionTypeDef]]

class SearchCriteriaTypeDef(TypedDict):
    searchQuery: str
    memoryStrategyId: NotRequired[str]
    topK: NotRequired[int]
    metadataFilters: NotRequired[Sequence[MemoryMetadataFilterExpressionTypeDef]]

class ListMemoryExtractionJobsOutputTypeDef(TypedDict):
    jobs: list[ExtractionJobMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class InvokeHarnessStreamOutputTypeDef(TypedDict):
    messageStart: NotRequired[HarnessMessageStartEventTypeDef]
    contentBlockStart: NotRequired[HarnessContentBlockStartEventTypeDef]
    contentBlockDelta: NotRequired[HarnessContentBlockDeltaEventTypeDef]
    contentBlockStop: NotRequired[HarnessContentBlockStopEventTypeDef]
    messageStop: NotRequired[HarnessMessageStopEventTypeDef]
    metadata: NotRequired[HarnessMetadataEventTypeDef]
    internalServerException: NotRequired[InternalServerExceptionTypeDef]
    validationException: NotRequired[ValidationExceptionTypeDef]
    runtimeClientError: NotRequired[RuntimeClientErrorTypeDef]

class HarnessToolConfigurationTypeDef(TypedDict):
    remoteMcp: NotRequired[HarnessRemoteMcpConfigTypeDef]
    agentCoreBrowser: NotRequired[HarnessAgentCoreBrowserConfigTypeDef]
    agentCoreGateway: NotRequired[HarnessAgentCoreGatewayConfigTypeDef]
    inlineFunction: NotRequired[HarnessInlineFunctionConfigTypeDef]
    agentCoreCodeInterpreter: NotRequired[HarnessAgentCoreCodeInterpreterConfigTypeDef]

class HarnessMessageTypeDef(TypedDict):
    role: HarnessConversationRoleType
    content: Sequence[HarnessContentBlockTypeDef]

class RegistryRecordSummaryTypeDef(TypedDict):
    registryArn: str
    recordArn: str
    recordId: str
    name: str
    descriptorType: DescriptorTypeType
    descriptors: DescriptorsTypeDef
    version: str
    status: RegistryRecordStatusType
    createdAt: datetime
    updatedAt: datetime
    description: NotRequired[str]

class InvokeAgentRuntimeCommandResponseTypeDef(TypedDict):
    runtimeSessionId: str
    traceId: str
    traceParent: str
    traceState: str
    baggage: str
    contentType: str
    statusCode: int
    stream: EventStream[InvokeAgentRuntimeCommandStreamOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ProxyConfigurationOutputTypeDef(TypedDict):
    proxies: list[ProxyOutputTypeDef]
    bypass: NotRequired[ProxyBypassOutputTypeDef]

class ProxyConfigurationTypeDef(TypedDict):
    proxies: Sequence[ProxyTypeDef]
    bypass: NotRequired[ProxyBypassTypeDef]

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
    events: list[EventTypeDef]
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
    metadata: NotRequired[Mapping[str, MetadataValueTypeDef]]

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

class RetrieveMemoryRecordsInputPaginateTypeDef(TypedDict):
    memoryId: str
    searchCriteria: SearchCriteriaTypeDef
    namespace: NotRequired[str]
    namespacePath: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class RetrieveMemoryRecordsInputTypeDef(TypedDict):
    memoryId: str
    searchCriteria: SearchCriteriaTypeDef
    namespace: NotRequired[str]
    namespacePath: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class InvokeHarnessResponseTypeDef(TypedDict):
    stream: EventStream[InvokeHarnessStreamOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

HarnessToolTypeDef = TypedDict(
    "HarnessToolTypeDef",
    {
        "type": HarnessToolTypeType,
        "name": NotRequired[str],
        "config": NotRequired[HarnessToolConfigurationTypeDef],
    },
)

class SearchRegistryRecordsResponseTypeDef(TypedDict):
    registryRecords: list[RegistryRecordSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetBrowserSessionResponseTypeDef(TypedDict):
    browserIdentifier: str
    sessionId: str
    name: str
    createdAt: datetime
    viewPort: ViewPortTypeDef
    extensions: list[BrowserExtensionTypeDef]
    enterprisePolicies: list[BrowserEnterprisePolicyTypeDef]
    profileConfiguration: BrowserProfileConfigurationTypeDef
    sessionTimeoutSeconds: int
    status: BrowserSessionStatusType
    streams: BrowserSessionStreamTypeDef
    proxyConfiguration: ProxyConfigurationOutputTypeDef
    certificates: list[CertificateTypeDef]
    sessionReplayArtifact: str
    lastUpdatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

ProxyConfigurationUnionTypeDef = Union[ProxyConfigurationTypeDef, ProxyConfigurationOutputTypeDef]

class InvokeHarnessRequestTypeDef(TypedDict):
    harnessArn: str
    runtimeSessionId: str
    messages: Sequence[HarnessMessageTypeDef]
    model: NotRequired[HarnessModelConfigurationTypeDef]
    systemPrompt: NotRequired[Sequence[HarnessSystemContentBlockTypeDef]]
    tools: NotRequired[Sequence[HarnessToolTypeDef]]
    skills: NotRequired[Sequence[HarnessSkillTypeDef]]
    allowedTools: NotRequired[Sequence[str]]
    maxIterations: NotRequired[int]
    maxTokens: NotRequired[int]
    timeoutSeconds: NotRequired[int]
    actorId: NotRequired[str]

class StartBrowserSessionRequestTypeDef(TypedDict):
    browserIdentifier: str
    traceId: NotRequired[str]
    traceParent: NotRequired[str]
    name: NotRequired[str]
    sessionTimeoutSeconds: NotRequired[int]
    viewPort: NotRequired[ViewPortTypeDef]
    extensions: NotRequired[Sequence[BrowserExtensionTypeDef]]
    profileConfiguration: NotRequired[BrowserProfileConfigurationTypeDef]
    proxyConfiguration: NotRequired[ProxyConfigurationUnionTypeDef]
    enterprisePolicies: NotRequired[Sequence[BrowserEnterprisePolicyTypeDef]]
    certificates: NotRequired[Sequence[CertificateTypeDef]]
    clientToken: NotRequired[str]
