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
    ABTestExecutionStatusType,
    ABTestStatusType,
    AutomationStreamStatusType,
    BatchEvaluationStatusType,
    BlockchainChainIdType,
    BrowserActionStatusType,
    BrowserEnterprisePolicyTypeType,
    BrowserSessionStatusType,
    CloudWatchLogsFilterOperatorType,
    CodeInterpreterSessionStatusType,
    CommandExecutionStatusType,
    ContentBlockTypeType,
    CryptoWalletNetworkType,
    DescriptorTypeType,
    HarnessConversationRoleType,
    HarnessStopReasonType,
    HarnessToolTypeType,
    HarnessToolUseStatusType,
    HarnessToolUseTypeType,
    LanguageRuntimeType,
    MemoryRecordOperatorTypeType,
    MemoryRecordStatusType,
    MouseButtonType,
    Oauth2FlowTypeType,
    OAuthGrantTypeType,
    OperatorTypeType,
    PaymentHttpMethodTypeType,
    PaymentInstrumentStatusType,
    PaymentSessionStatusType,
    ProgrammingLanguageType,
    RecommendationStatusType,
    RecommendationTypeType,
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
    "ABTestEvaluationConfigOutputTypeDef",
    "ABTestEvaluationConfigTypeDef",
    "ABTestEvaluationConfigUnionTypeDef",
    "ABTestResultsTypeDef",
    "ABTestSummaryTypeDef",
    "AccessDeniedExceptionTypeDef",
    "ActorSummaryTypeDef",
    "AgentCardDefinitionTypeDef",
    "AgentSkillsDescriptorTypeDef",
    "AgentTracesConfigOutputTypeDef",
    "AgentTracesConfigTypeDef",
    "AmountTypeDef",
    "AutomationStreamTypeDef",
    "AutomationStreamUpdateTypeDef",
    "AvailableLimitsTypeDef",
    "BasicAuthTypeDef",
    "BatchCreateMemoryRecordsInputTypeDef",
    "BatchCreateMemoryRecordsOutputTypeDef",
    "BatchDeleteMemoryRecordsInputTypeDef",
    "BatchDeleteMemoryRecordsOutputTypeDef",
    "BatchEvaluationSummaryTypeDef",
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
    "CloudWatchFilterConfigOutputTypeDef",
    "CloudWatchFilterConfigTypeDef",
    "CloudWatchLogsFilterTypeDef",
    "CloudWatchLogsRuleOutputTypeDef",
    "CloudWatchLogsRuleTypeDef",
    "CloudWatchLogsSourceOutputTypeDef",
    "CloudWatchLogsSourceTypeDef",
    "CloudWatchLogsTraceConfigOutputTypeDef",
    "CloudWatchLogsTraceConfigTypeDef",
    "CloudWatchOutputConfigTypeDef",
    "CodeInterpreterResultTypeDef",
    "CodeInterpreterSessionSummaryTypeDef",
    "CodeInterpreterStreamOutputTypeDef",
    "CoinbaseCdpTokenRequestInputTypeDef",
    "CoinbaseCdpTokenResponseOutputTypeDef",
    "CompleteResourceTokenAuthRequestTypeDef",
    "ConfidenceIntervalTypeDef",
    "ConfigurationBundleRefTypeDef",
    "ConfigurationBundleToolEntryTypeDef",
    "ConflictExceptionTypeDef",
    "ContentBlockTypeDef",
    "ContentDeltaEventTypeDef",
    "ContentStopEventTypeDef",
    "ContentTypeDef",
    "ContextTypeDef",
    "ControlStatsTypeDef",
    "ConversationalTypeDef",
    "CreateABTestRequestTypeDef",
    "CreateABTestResponseTypeDef",
    "CreateEventInputTypeDef",
    "CreateEventOutputTypeDef",
    "CreatePaymentInstrumentRequestTypeDef",
    "CreatePaymentInstrumentResponseTypeDef",
    "CreatePaymentSessionRequestTypeDef",
    "CreatePaymentSessionResponseTypeDef",
    "CryptoX402PaymentInputTypeDef",
    "CryptoX402PaymentOutputTypeDef",
    "CustomDescriptorTypeDef",
    "DataSourceConfigOutputTypeDef",
    "DataSourceConfigTypeDef",
    "DataSourceConfigUnionTypeDef",
    "DeleteABTestRequestTypeDef",
    "DeleteABTestResponseTypeDef",
    "DeleteBatchEvaluationRequestTypeDef",
    "DeleteBatchEvaluationResponseTypeDef",
    "DeleteEventInputTypeDef",
    "DeleteEventOutputTypeDef",
    "DeleteMemoryRecordInputTypeDef",
    "DeleteMemoryRecordOutputTypeDef",
    "DeletePaymentInstrumentRequestTypeDef",
    "DeletePaymentInstrumentResponseTypeDef",
    "DeletePaymentSessionRequestTypeDef",
    "DeletePaymentSessionResponseTypeDef",
    "DeleteRecommendationRequestTypeDef",
    "DeleteRecommendationResponseTypeDef",
    "DescriptorsTypeDef",
    "EmbeddedCryptoWalletOutputTypeDef",
    "EmbeddedCryptoWalletTypeDef",
    "EvaluateRequestTypeDef",
    "EvaluateResponseTypeDef",
    "EvaluationContentTypeDef",
    "EvaluationExpectedTrajectoryTypeDef",
    "EvaluationInputTypeDef",
    "EvaluationJobResultsTypeDef",
    "EvaluationMetadataTypeDef",
    "EvaluationReferenceInputTypeDef",
    "EvaluationResultContentTypeDef",
    "EvaluationTargetTypeDef",
    "EvaluatorMetricTypeDef",
    "EvaluatorStatisticsTypeDef",
    "EvaluatorSummaryTypeDef",
    "EvaluatorTypeDef",
    "EventMetadataFilterExpressionTypeDef",
    "EventTypeDef",
    "ExternalProxyOutputTypeDef",
    "ExternalProxyTypeDef",
    "ExtractionJobFilterInputTypeDef",
    "ExtractionJobMessagesTypeDef",
    "ExtractionJobMetadataTypeDef",
    "ExtractionJobTypeDef",
    "FilterInputTypeDef",
    "FilterValueTypeDef",
    "GatewayFilterOutputTypeDef",
    "GatewayFilterTypeDef",
    "GatewayFilterUnionTypeDef",
    "GetABTestRequestTypeDef",
    "GetABTestResponseTypeDef",
    "GetAgentCardRequestTypeDef",
    "GetAgentCardResponseTypeDef",
    "GetBatchEvaluationRequestTypeDef",
    "GetBatchEvaluationResponseTypeDef",
    "GetBrowserSessionRequestTypeDef",
    "GetBrowserSessionResponseTypeDef",
    "GetCodeInterpreterSessionRequestTypeDef",
    "GetCodeInterpreterSessionResponseTypeDef",
    "GetEventInputTypeDef",
    "GetEventOutputTypeDef",
    "GetMemoryRecordInputTypeDef",
    "GetMemoryRecordOutputTypeDef",
    "GetPaymentInstrumentBalanceRequestTypeDef",
    "GetPaymentInstrumentBalanceResponseTypeDef",
    "GetPaymentInstrumentRequestTypeDef",
    "GetPaymentInstrumentResponseTypeDef",
    "GetPaymentSessionRequestTypeDef",
    "GetPaymentSessionResponseTypeDef",
    "GetRecommendationRequestTypeDef",
    "GetRecommendationResponseTypeDef",
    "GetResourceApiKeyRequestTypeDef",
    "GetResourceApiKeyResponseTypeDef",
    "GetResourceOauth2TokenRequestTypeDef",
    "GetResourceOauth2TokenResponseTypeDef",
    "GetResourcePaymentTokenRequestTypeDef",
    "GetResourcePaymentTokenResponseTypeDef",
    "GetWorkloadAccessTokenForJWTRequestTypeDef",
    "GetWorkloadAccessTokenForJWTResponseTypeDef",
    "GetWorkloadAccessTokenForUserIdRequestTypeDef",
    "GetWorkloadAccessTokenForUserIdResponseTypeDef",
    "GetWorkloadAccessTokenRequestTypeDef",
    "GetWorkloadAccessTokenResponseTypeDef",
    "GroundTruthSourceTypeDef",
    "GroundTruthTurnInputTypeDef",
    "GroundTruthTurnTypeDef",
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
    "InlineGroundTruthTypeDef",
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
    "LinkedAccountDeveloperJwtTypeDef",
    "LinkedAccountEmailTypeDef",
    "LinkedAccountOAuth2TypeDef",
    "LinkedAccountSmsTypeDef",
    "LinkedAccountTypeDef",
    "ListABTestsRequestPaginateTypeDef",
    "ListABTestsRequestTypeDef",
    "ListABTestsResponseTypeDef",
    "ListActorsInputPaginateTypeDef",
    "ListActorsInputTypeDef",
    "ListActorsOutputTypeDef",
    "ListBatchEvaluationsRequestPaginateTypeDef",
    "ListBatchEvaluationsRequestTypeDef",
    "ListBatchEvaluationsResponseTypeDef",
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
    "ListPaymentInstrumentsRequestPaginateTypeDef",
    "ListPaymentInstrumentsRequestTypeDef",
    "ListPaymentInstrumentsResponseTypeDef",
    "ListPaymentSessionsRequestPaginateTypeDef",
    "ListPaymentSessionsRequestTypeDef",
    "ListPaymentSessionsResponseTypeDef",
    "ListRecommendationsRequestPaginateTypeDef",
    "ListRecommendationsRequestTypeDef",
    "ListRecommendationsResponseTypeDef",
    "ListSessionsInputPaginateTypeDef",
    "ListSessionsInputTypeDef",
    "ListSessionsOutputTypeDef",
    "LiveViewStreamTypeDef",
    "McpDescriptorTypeDef",
    "MemoryContentTypeDef",
    "MemoryMetadataFilterExpressionTypeDef",
    "MemoryRecordCreateInputTypeDef",
    "MemoryRecordDeleteInputTypeDef",
    "MemoryRecordLeftExpressionTypeDef",
    "MemoryRecordMetadataValueOutputTypeDef",
    "MemoryRecordMetadataValueTypeDef",
    "MemoryRecordMetadataValueUnionTypeDef",
    "MemoryRecordOutputTypeDef",
    "MemoryRecordRightExpressionTypeDef",
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
    "OAuth2AuthenticationTypeDef",
    "OAuthCredentialProviderTypeDef",
    "OutputConfigTypeDef",
    "PaginatorConfigTypeDef",
    "PayloadTypeOutputTypeDef",
    "PayloadTypeTypeDef",
    "PayloadTypeUnionTypeDef",
    "PaymentInputTypeDef",
    "PaymentInstrumentDetailsOutputTypeDef",
    "PaymentInstrumentDetailsTypeDef",
    "PaymentInstrumentDetailsUnionTypeDef",
    "PaymentInstrumentSummaryTypeDef",
    "PaymentInstrumentTypeDef",
    "PaymentOutputTypeDef",
    "PaymentSessionSummaryTypeDef",
    "PaymentSessionTypeDef",
    "PaymentTokenRequestInputTypeDef",
    "PaymentTokenResponseOutputTypeDef",
    "PerVariantOnlineEvaluationConfigTypeDef",
    "ProcessPaymentRequestTypeDef",
    "ProcessPaymentResponseTypeDef",
    "ProxyBypassOutputTypeDef",
    "ProxyBypassTypeDef",
    "ProxyConfigurationOutputTypeDef",
    "ProxyConfigurationTypeDef",
    "ProxyConfigurationUnionTypeDef",
    "ProxyCredentialsTypeDef",
    "ProxyOutputTypeDef",
    "ProxyTypeDef",
    "RecommendationConfigOutputTypeDef",
    "RecommendationConfigTypeDef",
    "RecommendationConfigUnionTypeDef",
    "RecommendationEvaluationConfigOutputTypeDef",
    "RecommendationEvaluationConfigTypeDef",
    "RecommendationEvaluatorReferenceTypeDef",
    "RecommendationResultConfigurationBundleTypeDef",
    "RecommendationResultTypeDef",
    "RecommendationSummaryTypeDef",
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
    "SessionFilterConfigOutputTypeDef",
    "SessionFilterConfigTypeDef",
    "SessionFilterTypeDef",
    "SessionLimitsTypeDef",
    "SessionMetadataShapeTypeDef",
    "SessionSummaryTypeDef",
    "SkillDefinitionTypeDef",
    "SkillMdDefinitionTypeDef",
    "SpanContextTypeDef",
    "StartBatchEvaluationRequestTypeDef",
    "StartBatchEvaluationResponseTypeDef",
    "StartBrowserSessionRequestTypeDef",
    "StartBrowserSessionResponseTypeDef",
    "StartCodeInterpreterSessionRequestTypeDef",
    "StartCodeInterpreterSessionResponseTypeDef",
    "StartMemoryExtractionJobInputTypeDef",
    "StartMemoryExtractionJobOutputTypeDef",
    "StartRecommendationRequestTypeDef",
    "StartRecommendationResponseTypeDef",
    "StopBatchEvaluationRequestTypeDef",
    "StopBatchEvaluationResponseTypeDef",
    "StopBrowserSessionRequestTypeDef",
    "StopBrowserSessionResponseTypeDef",
    "StopCodeInterpreterSessionRequestTypeDef",
    "StopCodeInterpreterSessionResponseTypeDef",
    "StopRuntimeSessionRequestTypeDef",
    "StopRuntimeSessionResponseTypeDef",
    "StreamUpdateTypeDef",
    "StripePrivyTokenRequestInputTypeDef",
    "StripePrivyTokenResponseOutputTypeDef",
    "SystemPromptConfigTypeDef",
    "SystemPromptConfigurationBundleTypeDef",
    "SystemPromptRecommendationConfigOutputTypeDef",
    "SystemPromptRecommendationConfigTypeDef",
    "SystemPromptRecommendationResultTypeDef",
    "TargetRefTypeDef",
    "ThrottlingExceptionTypeDef",
    "TimestampTypeDef",
    "TokenBalanceTypeDef",
    "TokenUsageTypeDef",
    "ToolArgumentsTypeDef",
    "ToolDescriptionConfigTypeDef",
    "ToolDescriptionConfigurationBundleOutputTypeDef",
    "ToolDescriptionConfigurationBundleTypeDef",
    "ToolDescriptionInputTypeDef",
    "ToolDescriptionOutputTypeDef",
    "ToolDescriptionRecommendationConfigOutputTypeDef",
    "ToolDescriptionRecommendationConfigTypeDef",
    "ToolDescriptionRecommendationResultTypeDef",
    "ToolDescriptionSourceOutputTypeDef",
    "ToolDescriptionSourceTypeDef",
    "ToolDescriptionTextInputOutputTypeDef",
    "ToolDescriptionTextInputTypeDef",
    "ToolResultStructuredContentTypeDef",
    "ToolsDefinitionTypeDef",
    "UpdateABTestRequestTypeDef",
    "UpdateABTestResponseTypeDef",
    "UpdateBrowserStreamRequestTypeDef",
    "UpdateBrowserStreamResponseTypeDef",
    "UserIdentifierTypeDef",
    "ValidationExceptionFieldTypeDef",
    "ValidationExceptionTypeDef",
    "VariantConfigurationTypeDef",
    "VariantResultTypeDef",
    "VariantTypeDef",
    "ViewPortTypeDef",
)


class AgentCardDefinitionTypeDef(TypedDict):
    schemaVersion: NotRequired[str]
    inlineContent: NotRequired[str]


class PerVariantOnlineEvaluationConfigTypeDef(TypedDict):
    name: str
    onlineEvaluationConfigArn: str


class ABTestSummaryTypeDef(TypedDict):
    abTestId: str
    abTestArn: str
    name: str
    status: ABTestStatusType
    executionStatus: ABTestExecutionStatusType
    createdAt: datetime
    updatedAt: datetime
    description: NotRequired[str]
    gatewayArn: NotRequired[str]


class AccessDeniedExceptionTypeDef(TypedDict):
    message: NotRequired[str]


class ActorSummaryTypeDef(TypedDict):
    actorId: str


class SkillDefinitionTypeDef(TypedDict):
    schemaVersion: NotRequired[str]
    inlineContent: NotRequired[str]


class SkillMdDefinitionTypeDef(TypedDict):
    inlineContent: NotRequired[str]


class AmountTypeDef(TypedDict):
    value: str
    currency: Literal["USD"]


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


class EvaluatorTypeDef(TypedDict):
    evaluatorId: str


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


class SessionFilterConfigOutputTypeDef(TypedDict):
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]


class FilterValueTypeDef(TypedDict):
    stringValue: NotRequired[str]
    doubleValue: NotRequired[float]
    booleanValue: NotRequired[bool]


TimestampTypeDef = Union[datetime, str]


class CloudWatchOutputConfigTypeDef(TypedDict):
    logGroupName: str
    logStreamName: str


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


class CoinbaseCdpTokenRequestInputTypeDef(TypedDict):
    requestMethod: PaymentHttpMethodTypeType
    requestPath: str
    requestHost: NotRequired[str]
    includeWalletAuthToken: NotRequired[bool]
    requestBody: NotRequired[str]


class CoinbaseCdpTokenResponseOutputTypeDef(TypedDict):
    bearerToken: str
    walletAuthToken: NotRequired[str]


class UserIdentifierTypeDef(TypedDict):
    userToken: NotRequired[str]
    userId: NotRequired[str]


class ConfidenceIntervalTypeDef(TypedDict):
    lower: NotRequired[float]
    upper: NotRequired[float]


class ConfigurationBundleRefTypeDef(TypedDict):
    bundleArn: str
    bundleVersion: str


class ConfigurationBundleToolEntryTypeDef(TypedDict):
    toolName: str
    toolDescriptionJsonPath: str


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


class ControlStatsTypeDef(TypedDict):
    variantName: str
    sampleSize: int
    mean: float


class MetadataValueTypeDef(TypedDict):
    stringValue: NotRequired[str]


class CryptoX402PaymentInputTypeDef(TypedDict):
    version: str
    payload: Mapping[str, Any]


class CryptoX402PaymentOutputTypeDef(TypedDict):
    version: str
    payload: dict[str, Any]


class CustomDescriptorTypeDef(TypedDict):
    inlineContent: NotRequired[str]


class DeleteABTestRequestTypeDef(TypedDict):
    abTestId: str


class DeleteBatchEvaluationRequestTypeDef(TypedDict):
    batchEvaluationId: str


class DeleteEventInputTypeDef(TypedDict):
    memoryId: str
    sessionId: str
    eventId: str
    actorId: str


class DeleteMemoryRecordInputTypeDef(TypedDict):
    memoryId: str
    memoryRecordId: str


class DeletePaymentInstrumentRequestTypeDef(TypedDict):
    paymentManagerArn: str
    paymentConnectorId: str
    paymentInstrumentId: str
    userId: NotRequired[str]


class DeletePaymentSessionRequestTypeDef(TypedDict):
    paymentManagerArn: str
    paymentSessionId: str
    userId: NotRequired[str]


class DeleteRecommendationRequestTypeDef(TypedDict):
    recommendationId: str


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


class EvaluatorStatisticsTypeDef(TypedDict):
    averageScore: NotRequired[float]


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


class GatewayFilterOutputTypeDef(TypedDict):
    targetPaths: NotRequired[list[str]]


class GatewayFilterTypeDef(TypedDict):
    targetPaths: NotRequired[Sequence[str]]


class GetABTestRequestTypeDef(TypedDict):
    abTestId: str


class GetAgentCardRequestTypeDef(TypedDict):
    agentRuntimeArn: str
    runtimeSessionId: NotRequired[str]
    qualifier: NotRequired[str]


class GetBatchEvaluationRequestTypeDef(TypedDict):
    batchEvaluationId: str


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


class GetPaymentInstrumentBalanceRequestTypeDef(TypedDict):
    paymentManagerArn: str
    paymentConnectorId: str
    paymentInstrumentId: str
    chain: BlockchainChainIdType
    token: Literal["USDC"]
    userId: NotRequired[str]
    agentName: NotRequired[str]


class TokenBalanceTypeDef(TypedDict):
    amount: str
    decimals: int
    token: Literal["USDC"]
    network: CryptoWalletNetworkType
    chain: BlockchainChainIdType


class GetPaymentInstrumentRequestTypeDef(TypedDict):
    paymentManagerArn: str
    paymentInstrumentId: str
    userId: NotRequired[str]
    agentName: NotRequired[str]
    paymentConnectorId: NotRequired[str]


class GetPaymentSessionRequestTypeDef(TypedDict):
    paymentManagerArn: str
    paymentSessionId: str
    userId: NotRequired[str]
    agentName: NotRequired[str]


class GetRecommendationRequestTypeDef(TypedDict):
    recommendationId: str


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
    resources: NotRequired[Sequence[str]]
    audiences: NotRequired[Sequence[str]]


class GetWorkloadAccessTokenForJWTRequestTypeDef(TypedDict):
    workloadName: str
    userToken: str


class GetWorkloadAccessTokenForUserIdRequestTypeDef(TypedDict):
    workloadName: str
    userId: str


class GetWorkloadAccessTokenRequestTypeDef(TypedDict):
    workloadName: str


class GroundTruthTurnInputTypeDef(TypedDict):
    prompt: NotRequired[str]


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


class LinkedAccountDeveloperJwtTypeDef(TypedDict):
    kid: str
    sub: str


class LinkedAccountEmailTypeDef(TypedDict):
    emailAddress: str


class OAuth2AuthenticationTypeDef(TypedDict):
    sub: str
    emailAddress: NotRequired[str]
    name: NotRequired[str]
    username: NotRequired[str]


class LinkedAccountSmsTypeDef(TypedDict):
    phoneNumber: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListABTestsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListActorsInputTypeDef(TypedDict):
    memoryId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListBatchEvaluationsRequestTypeDef(TypedDict):
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


class ListPaymentInstrumentsRequestTypeDef(TypedDict):
    paymentManagerArn: str
    userId: NotRequired[str]
    agentName: NotRequired[str]
    paymentConnectorId: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class PaymentInstrumentSummaryTypeDef(TypedDict):
    paymentInstrumentId: str
    paymentManagerArn: str
    paymentConnectorId: str
    userId: str
    paymentInstrumentType: Literal["EMBEDDED_CRYPTO_WALLET"]
    status: PaymentInstrumentStatusType
    createdAt: datetime
    updatedAt: datetime


class ListPaymentSessionsRequestTypeDef(TypedDict):
    paymentManagerArn: str
    userId: NotRequired[str]
    agentName: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class PaymentSessionSummaryTypeDef(TypedDict):
    paymentSessionId: str
    paymentManagerArn: str
    userId: str
    expiryTimeInMinutes: int
    createdAt: datetime
    updatedAt: datetime


class ListRecommendationsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    statusFilter: NotRequired[RecommendationStatusType]


RecommendationSummaryTypeDef = TypedDict(
    "RecommendationSummaryTypeDef",
    {
        "recommendationId": str,
        "recommendationArn": str,
        "name": str,
        "type": RecommendationTypeType,
        "status": RecommendationStatusType,
        "createdAt": datetime,
        "updatedAt": datetime,
        "description": NotRequired[str],
    },
)


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


class MemoryRecordLeftExpressionTypeDef(TypedDict):
    metadataKey: NotRequired[str]


class MemoryRecordMetadataValueOutputTypeDef(TypedDict):
    stringValue: NotRequired[str]
    stringListValue: NotRequired[list[str]]
    numberValue: NotRequired[float]
    dateTimeValue: NotRequired[datetime]


class StripePrivyTokenRequestInputTypeDef(TypedDict):
    requestPath: str
    requestBody: str
    requestHost: NotRequired[str]
    includeAuthorizationSignature: NotRequired[bool]


class StripePrivyTokenResponseOutputTypeDef(TypedDict):
    appId: str
    basicAuthToken: str
    authorizationSignature: NotRequired[str]
    requestExpiry: NotRequired[int]


class ProxyBypassOutputTypeDef(TypedDict):
    domainPatterns: NotRequired[list[str]]


class ProxyBypassTypeDef(TypedDict):
    domainPatterns: NotRequired[Sequence[str]]


class RecommendationEvaluatorReferenceTypeDef(TypedDict):
    evaluatorArn: str


class RecommendationResultConfigurationBundleTypeDef(TypedDict):
    bundleArn: str
    versionId: str


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


class StopBatchEvaluationRequestTypeDef(TypedDict):
    batchEvaluationId: str


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


class SystemPromptConfigurationBundleTypeDef(TypedDict):
    bundleArn: str
    versionId: str
    systemPromptJsonPath: str


class TargetRefTypeDef(TypedDict):
    name: str


class ToolDescriptionConfigTypeDef(TypedDict):
    text: NotRequired[str]


class ToolDescriptionOutputTypeDef(TypedDict):
    toolName: str
    recommendedToolDescription: NotRequired[str]


class ValidationExceptionFieldTypeDef(TypedDict):
    name: str
    message: str


class A2aDescriptorTypeDef(TypedDict):
    agentCard: AgentCardDefinitionTypeDef


class ABTestEvaluationConfigOutputTypeDef(TypedDict):
    onlineEvaluationConfigArn: NotRequired[str]
    perVariantOnlineEvaluationConfig: NotRequired[list[PerVariantOnlineEvaluationConfigTypeDef]]


class ABTestEvaluationConfigTypeDef(TypedDict):
    onlineEvaluationConfigArn: NotRequired[str]
    perVariantOnlineEvaluationConfig: NotRequired[Sequence[PerVariantOnlineEvaluationConfigTypeDef]]


class AgentSkillsDescriptorTypeDef(TypedDict):
    skillMd: SkillMdDefinitionTypeDef
    skillDefinition: NotRequired[SkillDefinitionTypeDef]


class AvailableLimitsTypeDef(TypedDict):
    availableSpendAmount: NotRequired[AmountTypeDef]
    updatedAt: NotRequired[datetime]


class SessionLimitsTypeDef(TypedDict):
    maxSpendAmount: AmountTypeDef


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


class CreateABTestResponseTypeDef(TypedDict):
    abTestId: str
    abTestArn: str
    name: str
    status: ABTestStatusType
    executionStatus: ABTestExecutionStatusType
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteABTestResponseTypeDef(TypedDict):
    abTestId: str
    abTestArn: str
    status: ABTestStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteBatchEvaluationResponseTypeDef(TypedDict):
    batchEvaluationId: str
    batchEvaluationArn: str
    status: BatchEvaluationStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteEventOutputTypeDef(TypedDict):
    eventId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteMemoryRecordOutputTypeDef(TypedDict):
    memoryRecordId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeletePaymentInstrumentResponseTypeDef(TypedDict):
    status: PaymentInstrumentStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class DeletePaymentSessionResponseTypeDef(TypedDict):
    status: PaymentSessionStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteRecommendationResponseTypeDef(TypedDict):
    recommendationId: str
    status: RecommendationStatusType
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


class ListABTestsResponseTypeDef(TypedDict):
    abTests: list[ABTestSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


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


class StopBatchEvaluationResponseTypeDef(TypedDict):
    batchEvaluationId: str
    batchEvaluationArn: str
    status: BatchEvaluationStatusType
    description: str
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


class UpdateABTestResponseTypeDef(TypedDict):
    abTestId: str
    abTestArn: str
    status: ABTestStatusType
    executionStatus: ABTestExecutionStatusType
    updatedAt: datetime
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


class CloudWatchFilterConfigOutputTypeDef(TypedDict):
    sessionIds: NotRequired[list[str]]
    timeRange: NotRequired[SessionFilterConfigOutputTypeDef]


CloudWatchLogsFilterTypeDef = TypedDict(
    "CloudWatchLogsFilterTypeDef",
    {
        "key": str,
        "operator": CloudWatchLogsFilterOperatorType,
        "value": FilterValueTypeDef,
    },
)


class MemoryRecordMetadataValueTypeDef(TypedDict):
    stringValue: NotRequired[str]
    stringListValue: NotRequired[Sequence[str]]
    numberValue: NotRequired[float]
    dateTimeValue: NotRequired[TimestampTypeDef]


class SessionFilterConfigTypeDef(TypedDict):
    startTime: NotRequired[TimestampTypeDef]
    endTime: NotRequired[TimestampTypeDef]


class OutputConfigTypeDef(TypedDict):
    cloudWatchConfig: NotRequired[CloudWatchOutputConfigTypeDef]


class ListCodeInterpreterSessionsResponseTypeDef(TypedDict):
    items: list[CodeInterpreterSessionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CompleteResourceTokenAuthRequestTypeDef(TypedDict):
    userIdentifier: UserIdentifierTypeDef
    sessionUri: str


class VariantResultTypeDef(TypedDict):
    variantName: str
    sampleSize: int
    mean: float
    isSignificant: bool
    absoluteChange: NotRequired[float]
    percentChange: NotRequired[float]
    pValue: NotRequired[float]
    confidenceInterval: NotRequired[ConfidenceIntervalTypeDef]


class ToolDescriptionConfigurationBundleOutputTypeDef(TypedDict):
    bundleArn: str
    versionId: str
    tools: list[ConfigurationBundleToolEntryTypeDef]


class ToolDescriptionConfigurationBundleTypeDef(TypedDict):
    bundleArn: str
    versionId: str
    tools: Sequence[ConfigurationBundleToolEntryTypeDef]


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


class PaymentInputTypeDef(TypedDict):
    cryptoX402: NotRequired[CryptoX402PaymentInputTypeDef]


class PaymentOutputTypeDef(TypedDict):
    cryptoX402: NotRequired[CryptoX402PaymentOutputTypeDef]


class EvaluatorSummaryTypeDef(TypedDict):
    evaluatorId: NotRequired[str]
    statistics: NotRequired[EvaluatorStatisticsTypeDef]
    totalEvaluated: NotRequired[int]
    totalFailed: NotRequired[int]


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


GatewayFilterUnionTypeDef = Union[GatewayFilterTypeDef, GatewayFilterOutputTypeDef]


class GetPaymentInstrumentBalanceResponseTypeDef(TypedDict):
    paymentInstrumentId: str
    tokenBalance: TokenBalanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


GroundTruthTurnTypeDef = TypedDict(
    "GroundTruthTurnTypeDef",
    {
        "input": NotRequired[GroundTruthTurnInputTypeDef],
        "expectedResponse": NotRequired[EvaluationContentTypeDef],
    },
)


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


class LinkedAccountOAuth2TypeDef(TypedDict):
    google: NotRequired[OAuth2AuthenticationTypeDef]
    apple: NotRequired[OAuth2AuthenticationTypeDef]
    x: NotRequired[OAuth2AuthenticationTypeDef]
    telegram: NotRequired[OAuth2AuthenticationTypeDef]
    github: NotRequired[OAuth2AuthenticationTypeDef]


class ListABTestsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListActorsInputPaginateTypeDef(TypedDict):
    memoryId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBatchEvaluationsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListMemoryExtractionJobsInputPaginateTypeDef = TypedDict(
    "ListMemoryExtractionJobsInputPaginateTypeDef",
    {
        "memoryId": str,
        "filter": NotRequired[ExtractionJobFilterInputTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class ListPaymentInstrumentsRequestPaginateTypeDef(TypedDict):
    paymentManagerArn: str
    userId: NotRequired[str]
    agentName: NotRequired[str]
    paymentConnectorId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPaymentSessionsRequestPaginateTypeDef(TypedDict):
    paymentManagerArn: str
    userId: NotRequired[str]
    agentName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRecommendationsRequestPaginateTypeDef(TypedDict):
    statusFilter: NotRequired[RecommendationStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPaymentInstrumentsResponseTypeDef(TypedDict):
    paymentInstruments: list[PaymentInstrumentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListPaymentSessionsResponseTypeDef(TypedDict):
    paymentSessions: list[PaymentSessionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListRecommendationsResponseTypeDef(TypedDict):
    recommendationSummaries: list[RecommendationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


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


class MemoryRecordSummaryTypeDef(TypedDict):
    memoryRecordId: str
    content: MemoryContentTypeDef
    memoryStrategyId: str
    namespaces: list[str]
    createdAt: datetime
    score: NotRequired[float]
    metadata: NotRequired[dict[str, MemoryRecordMetadataValueOutputTypeDef]]


class MemoryRecordTypeDef(TypedDict):
    memoryRecordId: str
    content: MemoryContentTypeDef
    memoryStrategyId: str
    namespaces: list[str]
    createdAt: datetime
    metadata: NotRequired[dict[str, MemoryRecordMetadataValueOutputTypeDef]]


class PaymentTokenRequestInputTypeDef(TypedDict):
    coinbaseCdpTokenRequest: NotRequired[CoinbaseCdpTokenRequestInputTypeDef]
    stripePrivyTokenRequest: NotRequired[StripePrivyTokenRequestInputTypeDef]


class PaymentTokenResponseOutputTypeDef(TypedDict):
    coinbaseCdpTokenResponse: NotRequired[CoinbaseCdpTokenResponseOutputTypeDef]
    stripePrivyTokenResponse: NotRequired[StripePrivyTokenResponseOutputTypeDef]


class RecommendationEvaluationConfigOutputTypeDef(TypedDict):
    evaluators: list[RecommendationEvaluatorReferenceTypeDef]


class RecommendationEvaluationConfigTypeDef(TypedDict):
    evaluators: Sequence[RecommendationEvaluatorReferenceTypeDef]


class SystemPromptRecommendationResultTypeDef(TypedDict):
    recommendedSystemPrompt: NotRequired[str]
    configurationBundle: NotRequired[RecommendationResultConfigurationBundleTypeDef]
    errorCode: NotRequired[str]
    errorMessage: NotRequired[str]


class ResourceLocationTypeDef(TypedDict):
    s3: NotRequired[S3LocationTypeDef]


class SystemPromptConfigTypeDef(TypedDict):
    text: NotRequired[str]
    configurationBundle: NotRequired[SystemPromptConfigurationBundleTypeDef]


class VariantConfigurationTypeDef(TypedDict):
    configurationBundle: NotRequired[ConfigurationBundleRefTypeDef]
    target: NotRequired[TargetRefTypeDef]


class ToolDescriptionInputTypeDef(TypedDict):
    toolName: str
    toolDescription: ToolDescriptionConfigTypeDef


class ToolDescriptionRecommendationResultTypeDef(TypedDict):
    tools: NotRequired[list[ToolDescriptionOutputTypeDef]]
    configurationBundle: NotRequired[RecommendationResultConfigurationBundleTypeDef]
    errorCode: NotRequired[str]
    errorMessage: NotRequired[str]


class ValidationExceptionTypeDef(TypedDict):
    message: str
    reason: ValidationExceptionReasonType
    fieldList: NotRequired[list[ValidationExceptionFieldTypeDef]]


ABTestEvaluationConfigUnionTypeDef = Union[
    ABTestEvaluationConfigTypeDef, ABTestEvaluationConfigOutputTypeDef
]


class CreatePaymentSessionRequestTypeDef(TypedDict):
    paymentManagerArn: str
    expiryTimeInMinutes: int
    userId: NotRequired[str]
    agentName: NotRequired[str]
    limits: NotRequired[SessionLimitsTypeDef]
    clientToken: NotRequired[str]


class PaymentSessionTypeDef(TypedDict):
    paymentSessionId: str
    paymentManagerArn: str
    userId: str
    expiryTimeInMinutes: int
    createdAt: datetime
    updatedAt: datetime
    limits: NotRequired[SessionLimitsTypeDef]
    availableLimits: NotRequired[AvailableLimitsTypeDef]


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


class CloudWatchLogsSourceOutputTypeDef(TypedDict):
    serviceNames: list[str]
    logGroupNames: list[str]
    filterConfig: NotRequired[CloudWatchFilterConfigOutputTypeDef]


class CloudWatchLogsRuleOutputTypeDef(TypedDict):
    filters: NotRequired[list[CloudWatchLogsFilterTypeDef]]


class CloudWatchLogsRuleTypeDef(TypedDict):
    filters: NotRequired[Sequence[CloudWatchLogsFilterTypeDef]]


MemoryRecordMetadataValueUnionTypeDef = Union[
    MemoryRecordMetadataValueTypeDef, MemoryRecordMetadataValueOutputTypeDef
]


class CloudWatchFilterConfigTypeDef(TypedDict):
    sessionIds: NotRequired[Sequence[str]]
    timeRange: NotRequired[SessionFilterConfigTypeDef]


class StartBatchEvaluationResponseTypeDef(TypedDict):
    batchEvaluationId: str
    batchEvaluationArn: str
    batchEvaluationName: str
    evaluators: list[EvaluatorTypeDef]
    status: BatchEvaluationStatusType
    createdAt: datetime
    outputConfig: OutputConfigTypeDef
    description: str
    ResponseMetadata: ResponseMetadataTypeDef


class EvaluatorMetricTypeDef(TypedDict):
    evaluatorArn: str
    controlStats: ControlStatsTypeDef
    variantResults: list[VariantResultTypeDef]


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


class ProcessPaymentRequestTypeDef(TypedDict):
    paymentManagerArn: str
    paymentSessionId: str
    paymentInstrumentId: str
    paymentType: Literal["CRYPTO_X402"]
    paymentInput: PaymentInputTypeDef
    userId: NotRequired[str]
    agentName: NotRequired[str]
    clientToken: NotRequired[str]


class ProcessPaymentResponseTypeDef(TypedDict):
    processPaymentId: str
    paymentManagerArn: str
    paymentSessionId: str
    paymentInstrumentId: str
    paymentType: Literal["CRYPTO_X402"]
    status: Literal["PROOF_GENERATED"]
    paymentOutput: PaymentOutputTypeDef
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class EvaluationJobResultsTypeDef(TypedDict):
    numberOfSessionsCompleted: NotRequired[int]
    numberOfSessionsInProgress: NotRequired[int]
    numberOfSessionsFailed: NotRequired[int]
    totalNumberOfSessions: NotRequired[int]
    numberOfSessionsIgnored: NotRequired[int]
    evaluatorSummaries: NotRequired[list[EvaluatorSummaryTypeDef]]


class ExtractionJobMetadataTypeDef(TypedDict):
    jobID: str
    messages: ExtractionJobMessagesTypeDef
    status: NotRequired[Literal["FAILED"]]
    failureReason: NotRequired[str]
    strategyId: NotRequired[str]
    sessionId: NotRequired[str]
    actorId: NotRequired[str]


class InlineGroundTruthTypeDef(TypedDict):
    assertions: NotRequired[Sequence[EvaluationContentTypeDef]]
    expectedTrajectory: NotRequired[EvaluationExpectedTrajectoryTypeDef]
    turns: NotRequired[Sequence[GroundTruthTurnTypeDef]]


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


class LinkedAccountTypeDef(TypedDict):
    email: NotRequired[LinkedAccountEmailTypeDef]
    sms: NotRequired[LinkedAccountSmsTypeDef]
    developerJwt: NotRequired[LinkedAccountDeveloperJwtTypeDef]
    oAuth2: NotRequired[LinkedAccountOAuth2TypeDef]


class DescriptorsTypeDef(TypedDict):
    mcp: NotRequired[McpDescriptorTypeDef]
    a2a: NotRequired[A2aDescriptorTypeDef]
    custom: NotRequired[CustomDescriptorTypeDef]
    agentSkills: NotRequired[AgentSkillsDescriptorTypeDef]


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


class GetResourcePaymentTokenRequestTypeDef(TypedDict):
    workloadIdentityToken: str
    resourceCredentialProviderName: str
    paymentTokenRequest: PaymentTokenRequestInputTypeDef


class GetResourcePaymentTokenResponseTypeDef(TypedDict):
    paymentTokenResponse: PaymentTokenResponseOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


BrowserEnterprisePolicyTypeDef = TypedDict(
    "BrowserEnterprisePolicyTypeDef",
    {
        "location": ResourceLocationTypeDef,
        "type": NotRequired[BrowserEnterprisePolicyTypeType],
    },
)


class BrowserExtensionTypeDef(TypedDict):
    location: ResourceLocationTypeDef


class VariantTypeDef(TypedDict):
    name: str
    weight: int
    variantConfiguration: VariantConfigurationTypeDef


class ToolDescriptionTextInputOutputTypeDef(TypedDict):
    tools: list[ToolDescriptionInputTypeDef]


class ToolDescriptionTextInputTypeDef(TypedDict):
    tools: Sequence[ToolDescriptionInputTypeDef]


class RecommendationResultTypeDef(TypedDict):
    systemPromptRecommendationResult: NotRequired[SystemPromptRecommendationResultTypeDef]
    toolDescriptionRecommendationResult: NotRequired[ToolDescriptionRecommendationResultTypeDef]


class InvokeAgentRuntimeCommandStreamOutputTypeDef(TypedDict):
    chunk: NotRequired[ResponseChunkTypeDef]
    accessDeniedException: NotRequired[AccessDeniedExceptionTypeDef]
    internalServerException: NotRequired[InternalServerExceptionTypeDef]
    resourceNotFoundException: NotRequired[ResourceNotFoundExceptionTypeDef]
    serviceQuotaExceededException: NotRequired[ServiceQuotaExceededExceptionTypeDef]
    throttlingException: NotRequired[ThrottlingExceptionTypeDef]
    validationException: NotRequired[ValidationExceptionTypeDef]
    runtimeClientError: NotRequired[RuntimeClientErrorTypeDef]


class CreatePaymentSessionResponseTypeDef(TypedDict):
    paymentSession: PaymentSessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetPaymentSessionResponseTypeDef(TypedDict):
    paymentSession: PaymentSessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


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


class DataSourceConfigOutputTypeDef(TypedDict):
    cloudWatchLogs: NotRequired[CloudWatchLogsSourceOutputTypeDef]


class CloudWatchLogsTraceConfigOutputTypeDef(TypedDict):
    logGroupArns: list[str]
    serviceNames: list[str]
    startTime: datetime
    endTime: datetime
    rule: NotRequired[CloudWatchLogsRuleOutputTypeDef]


class CloudWatchLogsTraceConfigTypeDef(TypedDict):
    logGroupArns: Sequence[str]
    serviceNames: Sequence[str]
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    rule: NotRequired[CloudWatchLogsRuleTypeDef]


class MemoryRecordCreateInputTypeDef(TypedDict):
    requestIdentifier: str
    namespaces: Sequence[str]
    content: MemoryContentTypeDef
    timestamp: TimestampTypeDef
    memoryStrategyId: NotRequired[str]
    metadata: NotRequired[Mapping[str, MemoryRecordMetadataValueUnionTypeDef]]


class MemoryRecordRightExpressionTypeDef(TypedDict):
    metadataValue: NotRequired[MemoryRecordMetadataValueUnionTypeDef]


class MemoryRecordUpdateInputTypeDef(TypedDict):
    memoryRecordId: str
    timestamp: TimestampTypeDef
    content: NotRequired[MemoryContentTypeDef]
    namespaces: NotRequired[Sequence[str]]
    memoryStrategyId: NotRequired[str]
    metadata: NotRequired[Mapping[str, MemoryRecordMetadataValueUnionTypeDef]]


class CloudWatchLogsSourceTypeDef(TypedDict):
    serviceNames: Sequence[str]
    logGroupNames: Sequence[str]
    filterConfig: NotRequired[CloudWatchFilterConfigTypeDef]


class ABTestResultsTypeDef(TypedDict):
    evaluatorMetrics: list[EvaluatorMetricTypeDef]
    analysisTimestamp: NotRequired[datetime]


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


class BatchEvaluationSummaryTypeDef(TypedDict):
    batchEvaluationId: str
    batchEvaluationArn: str
    batchEvaluationName: str
    status: BatchEvaluationStatusType
    createdAt: datetime
    description: NotRequired[str]
    evaluators: NotRequired[list[EvaluatorTypeDef]]
    evaluationResults: NotRequired[EvaluationJobResultsTypeDef]
    errorDetails: NotRequired[list[str]]
    updatedAt: NotRequired[datetime]


class ListMemoryExtractionJobsOutputTypeDef(TypedDict):
    jobs: list[ExtractionJobMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GroundTruthSourceTypeDef(TypedDict):
    inline: NotRequired[InlineGroundTruthTypeDef]


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


class EmbeddedCryptoWalletOutputTypeDef(TypedDict):
    network: CryptoWalletNetworkType
    linkedAccounts: list[LinkedAccountTypeDef]
    walletAddress: NotRequired[str]
    redirectUrl: NotRequired[str]


class EmbeddedCryptoWalletTypeDef(TypedDict):
    network: CryptoWalletNetworkType
    linkedAccounts: Sequence[LinkedAccountTypeDef]
    walletAddress: NotRequired[str]
    redirectUrl: NotRequired[str]


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


class CreateABTestRequestTypeDef(TypedDict):
    name: str
    gatewayArn: str
    variants: Sequence[VariantTypeDef]
    evaluationConfig: ABTestEvaluationConfigUnionTypeDef
    roleArn: str
    description: NotRequired[str]
    gatewayFilter: NotRequired[GatewayFilterUnionTypeDef]
    enableOnCreate: NotRequired[bool]
    clientToken: NotRequired[str]


class UpdateABTestRequestTypeDef(TypedDict):
    abTestId: str
    clientToken: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]
    variants: NotRequired[Sequence[VariantTypeDef]]
    gatewayFilter: NotRequired[GatewayFilterUnionTypeDef]
    evaluationConfig: NotRequired[ABTestEvaluationConfigUnionTypeDef]
    roleArn: NotRequired[str]
    executionStatus: NotRequired[ABTestExecutionStatusType]


class ToolDescriptionSourceOutputTypeDef(TypedDict):
    toolDescriptionText: NotRequired[ToolDescriptionTextInputOutputTypeDef]
    configurationBundle: NotRequired[ToolDescriptionConfigurationBundleOutputTypeDef]


class ToolDescriptionSourceTypeDef(TypedDict):
    toolDescriptionText: NotRequired[ToolDescriptionTextInputTypeDef]
    configurationBundle: NotRequired[ToolDescriptionConfigurationBundleTypeDef]


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


class GetBatchEvaluationResponseTypeDef(TypedDict):
    batchEvaluationId: str
    batchEvaluationArn: str
    batchEvaluationName: str
    status: BatchEvaluationStatusType
    createdAt: datetime
    evaluators: list[EvaluatorTypeDef]
    dataSourceConfig: DataSourceConfigOutputTypeDef
    outputConfig: OutputConfigTypeDef
    evaluationResults: EvaluationJobResultsTypeDef
    errorDetails: list[str]
    description: str
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class AgentTracesConfigOutputTypeDef(TypedDict):
    sessionSpans: NotRequired[list[dict[str, Any]]]
    cloudwatchLogs: NotRequired[CloudWatchLogsTraceConfigOutputTypeDef]


class AgentTracesConfigTypeDef(TypedDict):
    sessionSpans: NotRequired[Sequence[Mapping[str, Any]]]
    cloudwatchLogs: NotRequired[CloudWatchLogsTraceConfigTypeDef]


class BatchCreateMemoryRecordsInputTypeDef(TypedDict):
    memoryId: str
    records: Sequence[MemoryRecordCreateInputTypeDef]
    clientToken: NotRequired[str]


MemoryMetadataFilterExpressionTypeDef = TypedDict(
    "MemoryMetadataFilterExpressionTypeDef",
    {
        "left": MemoryRecordLeftExpressionTypeDef,
        "operator": MemoryRecordOperatorTypeType,
        "right": NotRequired[MemoryRecordRightExpressionTypeDef],
    },
)


class BatchUpdateMemoryRecordsInputTypeDef(TypedDict):
    memoryId: str
    records: Sequence[MemoryRecordUpdateInputTypeDef]


class DataSourceConfigTypeDef(TypedDict):
    cloudWatchLogs: NotRequired[CloudWatchLogsSourceTypeDef]


class GetABTestResponseTypeDef(TypedDict):
    abTestId: str
    abTestArn: str
    name: str
    description: str
    status: ABTestStatusType
    executionStatus: ABTestExecutionStatusType
    gatewayArn: str
    variants: list[VariantTypeDef]
    gatewayFilter: GatewayFilterOutputTypeDef
    evaluationConfig: ABTestEvaluationConfigOutputTypeDef
    roleArn: str
    currentRunId: str
    errorDetails: list[str]
    startedAt: datetime
    stoppedAt: datetime
    maxDurationExpiresAt: datetime
    createdAt: datetime
    updatedAt: datetime
    results: ABTestResultsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


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


class ListBatchEvaluationsResponseTypeDef(TypedDict):
    batchEvaluations: list[BatchEvaluationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class SessionMetadataShapeTypeDef(TypedDict):
    sessionId: str
    testScenarioId: NotRequired[str]
    groundTruth: NotRequired[GroundTruthSourceTypeDef]
    metadata: NotRequired[Mapping[str, str]]


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


class PaymentInstrumentDetailsOutputTypeDef(TypedDict):
    embeddedCryptoWallet: NotRequired[EmbeddedCryptoWalletOutputTypeDef]


class PaymentInstrumentDetailsTypeDef(TypedDict):
    embeddedCryptoWallet: NotRequired[EmbeddedCryptoWalletTypeDef]


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


class SystemPromptRecommendationConfigOutputTypeDef(TypedDict):
    systemPrompt: SystemPromptConfigTypeDef
    agentTraces: AgentTracesConfigOutputTypeDef
    evaluationConfig: RecommendationEvaluationConfigOutputTypeDef


class ToolDescriptionRecommendationConfigOutputTypeDef(TypedDict):
    toolDescription: ToolDescriptionSourceOutputTypeDef
    agentTraces: AgentTracesConfigOutputTypeDef


class SystemPromptRecommendationConfigTypeDef(TypedDict):
    systemPrompt: SystemPromptConfigTypeDef
    agentTraces: AgentTracesConfigTypeDef
    evaluationConfig: RecommendationEvaluationConfigTypeDef


class ToolDescriptionRecommendationConfigTypeDef(TypedDict):
    toolDescription: ToolDescriptionSourceTypeDef
    agentTraces: AgentTracesConfigTypeDef


class ListMemoryRecordsInputPaginateTypeDef(TypedDict):
    memoryId: str
    namespace: NotRequired[str]
    namespacePath: NotRequired[str]
    memoryStrategyId: NotRequired[str]
    metadataFilters: NotRequired[Sequence[MemoryMetadataFilterExpressionTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMemoryRecordsInputTypeDef(TypedDict):
    memoryId: str
    namespace: NotRequired[str]
    namespacePath: NotRequired[str]
    memoryStrategyId: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    metadataFilters: NotRequired[Sequence[MemoryMetadataFilterExpressionTypeDef]]


class SearchCriteriaTypeDef(TypedDict):
    searchQuery: str
    memoryStrategyId: NotRequired[str]
    topK: NotRequired[int]
    metadataFilters: NotRequired[Sequence[MemoryMetadataFilterExpressionTypeDef]]


DataSourceConfigUnionTypeDef = Union[DataSourceConfigTypeDef, DataSourceConfigOutputTypeDef]


class EvaluationMetadataTypeDef(TypedDict):
    sessionMetadata: NotRequired[Sequence[SessionMetadataShapeTypeDef]]


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


class PaymentInstrumentTypeDef(TypedDict):
    paymentInstrumentId: str
    paymentManagerArn: str
    paymentConnectorId: str
    userId: str
    paymentInstrumentType: Literal["EMBEDDED_CRYPTO_WALLET"]
    paymentInstrumentDetails: PaymentInstrumentDetailsOutputTypeDef
    createdAt: datetime
    status: PaymentInstrumentStatusType
    updatedAt: datetime


PaymentInstrumentDetailsUnionTypeDef = Union[
    PaymentInstrumentDetailsTypeDef, PaymentInstrumentDetailsOutputTypeDef
]


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


class RecommendationConfigOutputTypeDef(TypedDict):
    systemPromptRecommendationConfig: NotRequired[SystemPromptRecommendationConfigOutputTypeDef]
    toolDescriptionRecommendationConfig: NotRequired[
        ToolDescriptionRecommendationConfigOutputTypeDef
    ]


class RecommendationConfigTypeDef(TypedDict):
    systemPromptRecommendationConfig: NotRequired[SystemPromptRecommendationConfigTypeDef]
    toolDescriptionRecommendationConfig: NotRequired[ToolDescriptionRecommendationConfigTypeDef]


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


class StartBatchEvaluationRequestTypeDef(TypedDict):
    batchEvaluationName: str
    dataSourceConfig: DataSourceConfigUnionTypeDef
    evaluators: NotRequired[Sequence[EvaluatorTypeDef]]
    clientToken: NotRequired[str]
    evaluationMetadata: NotRequired[EvaluationMetadataTypeDef]
    description: NotRequired[str]


class CreatePaymentInstrumentResponseTypeDef(TypedDict):
    paymentInstrument: PaymentInstrumentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetPaymentInstrumentResponseTypeDef(TypedDict):
    paymentInstrument: PaymentInstrumentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePaymentInstrumentRequestTypeDef(TypedDict):
    paymentManagerArn: str
    paymentConnectorId: str
    paymentInstrumentType: Literal["EMBEDDED_CRYPTO_WALLET"]
    paymentInstrumentDetails: PaymentInstrumentDetailsUnionTypeDef
    userId: NotRequired[str]
    agentName: NotRequired[str]
    clientToken: NotRequired[str]


GetRecommendationResponseTypeDef = TypedDict(
    "GetRecommendationResponseTypeDef",
    {
        "recommendationId": str,
        "recommendationArn": str,
        "name": str,
        "description": str,
        "type": RecommendationTypeType,
        "recommendationConfig": RecommendationConfigOutputTypeDef,
        "status": RecommendationStatusType,
        "createdAt": datetime,
        "updatedAt": datetime,
        "recommendationResult": RecommendationResultTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartRecommendationResponseTypeDef = TypedDict(
    "StartRecommendationResponseTypeDef",
    {
        "recommendationId": str,
        "recommendationArn": str,
        "name": str,
        "description": str,
        "type": RecommendationTypeType,
        "recommendationConfig": RecommendationConfigOutputTypeDef,
        "status": RecommendationStatusType,
        "createdAt": datetime,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RecommendationConfigUnionTypeDef = Union[
    RecommendationConfigTypeDef, RecommendationConfigOutputTypeDef
]
StartRecommendationRequestTypeDef = TypedDict(
    "StartRecommendationRequestTypeDef",
    {
        "name": str,
        "type": RecommendationTypeType,
        "recommendationConfig": RecommendationConfigUnionTypeDef,
        "description": NotRequired[str],
        "clientToken": NotRequired[str],
    },
)
