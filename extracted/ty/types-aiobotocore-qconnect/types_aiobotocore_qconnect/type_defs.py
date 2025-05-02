"""
Type annotations for qconnect service type definitions.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from types_aiobotocore_qconnect.type_defs import AIAgentConfigurationDataTypeDef

    data: AIAgentConfigurationDataTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Any, Union

from .literals import (
    AIAgentTypeType,
    AIPromptAPIFormatType,
    AIPromptTypeType,
    AssistantCapabilityTypeType,
    AssistantStatusType,
    ChannelSubtypeType,
    ChunkingStrategyType,
    ContentStatusType,
    ConversationStatusReasonType,
    ConversationStatusType,
    GuardrailContentFilterTypeType,
    GuardrailContextualGroundingFilterTypeType,
    GuardrailFilterStrengthType,
    GuardrailPiiEntityTypeType,
    GuardrailSensitiveInformationActionType,
    ImportJobStatusType,
    KnowledgeBaseSearchTypeType,
    KnowledgeBaseStatusType,
    KnowledgeBaseTypeType,
    MessageTemplateAttributeTypeType,
    MessageTemplateFilterOperatorType,
    MessageTemplateQueryOperatorType,
    OrderType,
    OriginType,
    ParticipantType,
    PriorityType,
    QueryResultTypeType,
    QuickResponseFilterOperatorType,
    QuickResponseQueryOperatorType,
    QuickResponseStatusType,
    RecommendationSourceTypeType,
    RecommendationTriggerTypeType,
    RecommendationTypeType,
    ReferenceTypeType,
    RelevanceLevelType,
    RelevanceType,
    StatusType,
    SyncStatusType,
    TargetTypeType,
    VisibilityStatusType,
    WebScopeTypeType,
)

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
    "AIAgentConfigurationDataTypeDef",
    "AIAgentConfigurationOutputTypeDef",
    "AIAgentConfigurationTypeDef",
    "AIAgentConfigurationUnionTypeDef",
    "AIAgentDataTypeDef",
    "AIAgentSummaryTypeDef",
    "AIAgentVersionSummaryTypeDef",
    "AIGuardrailContentPolicyConfigOutputTypeDef",
    "AIGuardrailContentPolicyConfigTypeDef",
    "AIGuardrailContentPolicyConfigUnionTypeDef",
    "AIGuardrailContextualGroundingPolicyConfigOutputTypeDef",
    "AIGuardrailContextualGroundingPolicyConfigTypeDef",
    "AIGuardrailContextualGroundingPolicyConfigUnionTypeDef",
    "AIGuardrailDataTypeDef",
    "AIGuardrailSensitiveInformationPolicyConfigOutputTypeDef",
    "AIGuardrailSensitiveInformationPolicyConfigTypeDef",
    "AIGuardrailSensitiveInformationPolicyConfigUnionTypeDef",
    "AIGuardrailSummaryTypeDef",
    "AIGuardrailTopicPolicyConfigOutputTypeDef",
    "AIGuardrailTopicPolicyConfigTypeDef",
    "AIGuardrailTopicPolicyConfigUnionTypeDef",
    "AIGuardrailVersionSummaryTypeDef",
    "AIGuardrailWordPolicyConfigOutputTypeDef",
    "AIGuardrailWordPolicyConfigTypeDef",
    "AIGuardrailWordPolicyConfigUnionTypeDef",
    "AIPromptDataTypeDef",
    "AIPromptSummaryTypeDef",
    "AIPromptTemplateConfigurationTypeDef",
    "AIPromptVersionSummaryTypeDef",
    "ActivateMessageTemplateRequestTypeDef",
    "ActivateMessageTemplateResponseTypeDef",
    "AgentAttributesTypeDef",
    "AmazonConnectGuideAssociationDataTypeDef",
    "AnswerRecommendationAIAgentConfigurationOutputTypeDef",
    "AnswerRecommendationAIAgentConfigurationTypeDef",
    "AppIntegrationsConfigurationOutputTypeDef",
    "AppIntegrationsConfigurationTypeDef",
    "AssistantAssociationDataTypeDef",
    "AssistantAssociationInputDataTypeDef",
    "AssistantAssociationOutputDataTypeDef",
    "AssistantAssociationSummaryTypeDef",
    "AssistantCapabilityConfigurationTypeDef",
    "AssistantDataTypeDef",
    "AssistantIntegrationConfigurationTypeDef",
    "AssistantSummaryTypeDef",
    "AssociationConfigurationDataOutputTypeDef",
    "AssociationConfigurationDataTypeDef",
    "AssociationConfigurationOutputTypeDef",
    "AssociationConfigurationTypeDef",
    "BedrockFoundationModelConfigurationForParsingTypeDef",
    "ChunkingConfigurationOutputTypeDef",
    "ChunkingConfigurationTypeDef",
    "CitationSpanTypeDef",
    "ConfigurationTypeDef",
    "ConnectConfigurationTypeDef",
    "ContentAssociationContentsTypeDef",
    "ContentAssociationDataTypeDef",
    "ContentAssociationSummaryTypeDef",
    "ContentDataDetailsTypeDef",
    "ContentDataTypeDef",
    "ContentFeedbackDataTypeDef",
    "ContentReferenceTypeDef",
    "ContentSummaryTypeDef",
    "ConversationContextTypeDef",
    "ConversationStateTypeDef",
    "CreateAIAgentRequestTypeDef",
    "CreateAIAgentResponseTypeDef",
    "CreateAIAgentVersionRequestTypeDef",
    "CreateAIAgentVersionResponseTypeDef",
    "CreateAIGuardrailRequestTypeDef",
    "CreateAIGuardrailResponseTypeDef",
    "CreateAIGuardrailVersionRequestTypeDef",
    "CreateAIGuardrailVersionResponseTypeDef",
    "CreateAIPromptRequestTypeDef",
    "CreateAIPromptResponseTypeDef",
    "CreateAIPromptVersionRequestTypeDef",
    "CreateAIPromptVersionResponseTypeDef",
    "CreateAssistantAssociationRequestTypeDef",
    "CreateAssistantAssociationResponseTypeDef",
    "CreateAssistantRequestTypeDef",
    "CreateAssistantResponseTypeDef",
    "CreateContentAssociationRequestTypeDef",
    "CreateContentAssociationResponseTypeDef",
    "CreateContentRequestTypeDef",
    "CreateContentResponseTypeDef",
    "CreateKnowledgeBaseRequestTypeDef",
    "CreateKnowledgeBaseResponseTypeDef",
    "CreateMessageTemplateAttachmentRequestTypeDef",
    "CreateMessageTemplateAttachmentResponseTypeDef",
    "CreateMessageTemplateRequestTypeDef",
    "CreateMessageTemplateResponseTypeDef",
    "CreateMessageTemplateVersionRequestTypeDef",
    "CreateMessageTemplateVersionResponseTypeDef",
    "CreateQuickResponseRequestTypeDef",
    "CreateQuickResponseResponseTypeDef",
    "CreateSessionRequestTypeDef",
    "CreateSessionResponseTypeDef",
    "CustomerProfileAttributesOutputTypeDef",
    "CustomerProfileAttributesTypeDef",
    "DataDetailsPaginatorTypeDef",
    "DataDetailsTypeDef",
    "DataReferenceTypeDef",
    "DataSummaryPaginatorTypeDef",
    "DataSummaryTypeDef",
    "DeactivateMessageTemplateRequestTypeDef",
    "DeactivateMessageTemplateResponseTypeDef",
    "DeleteAIAgentRequestTypeDef",
    "DeleteAIAgentVersionRequestTypeDef",
    "DeleteAIGuardrailRequestTypeDef",
    "DeleteAIGuardrailVersionRequestTypeDef",
    "DeleteAIPromptRequestTypeDef",
    "DeleteAIPromptVersionRequestTypeDef",
    "DeleteAssistantAssociationRequestTypeDef",
    "DeleteAssistantRequestTypeDef",
    "DeleteContentAssociationRequestTypeDef",
    "DeleteContentRequestTypeDef",
    "DeleteImportJobRequestTypeDef",
    "DeleteKnowledgeBaseRequestTypeDef",
    "DeleteMessageTemplateAttachmentRequestTypeDef",
    "DeleteMessageTemplateRequestTypeDef",
    "DeleteQuickResponseRequestTypeDef",
    "DocumentTextTypeDef",
    "DocumentTypeDef",
    "EmailHeaderTypeDef",
    "EmailMessageTemplateContentBodyTypeDef",
    "EmailMessageTemplateContentOutputTypeDef",
    "EmailMessageTemplateContentTypeDef",
    "ExtendedMessageTemplateDataTypeDef",
    "ExternalSourceConfigurationTypeDef",
    "FilterTypeDef",
    "FixedSizeChunkingConfigurationTypeDef",
    "GenerativeContentFeedbackDataTypeDef",
    "GenerativeDataDetailsPaginatorTypeDef",
    "GenerativeDataDetailsTypeDef",
    "GenerativeReferenceTypeDef",
    "GetAIAgentRequestTypeDef",
    "GetAIAgentResponseTypeDef",
    "GetAIGuardrailRequestTypeDef",
    "GetAIGuardrailResponseTypeDef",
    "GetAIPromptRequestTypeDef",
    "GetAIPromptResponseTypeDef",
    "GetAssistantAssociationRequestTypeDef",
    "GetAssistantAssociationResponseTypeDef",
    "GetAssistantRequestTypeDef",
    "GetAssistantResponseTypeDef",
    "GetContentAssociationRequestTypeDef",
    "GetContentAssociationResponseTypeDef",
    "GetContentRequestTypeDef",
    "GetContentResponseTypeDef",
    "GetContentSummaryRequestTypeDef",
    "GetContentSummaryResponseTypeDef",
    "GetImportJobRequestTypeDef",
    "GetImportJobResponseTypeDef",
    "GetKnowledgeBaseRequestTypeDef",
    "GetKnowledgeBaseResponseTypeDef",
    "GetMessageTemplateRequestTypeDef",
    "GetMessageTemplateResponseTypeDef",
    "GetNextMessageRequestTypeDef",
    "GetNextMessageResponseTypeDef",
    "GetQuickResponseRequestTypeDef",
    "GetQuickResponseResponseTypeDef",
    "GetRecommendationsRequestTypeDef",
    "GetRecommendationsResponseTypeDef",
    "GetSessionRequestTypeDef",
    "GetSessionResponseTypeDef",
    "GroupingConfigurationOutputTypeDef",
    "GroupingConfigurationTypeDef",
    "GroupingConfigurationUnionTypeDef",
    "GuardrailContentFilterConfigTypeDef",
    "GuardrailContextualGroundingFilterConfigTypeDef",
    "GuardrailManagedWordsConfigTypeDef",
    "GuardrailPiiEntityConfigTypeDef",
    "GuardrailRegexConfigTypeDef",
    "GuardrailTopicConfigOutputTypeDef",
    "GuardrailTopicConfigTypeDef",
    "GuardrailWordConfigTypeDef",
    "HierarchicalChunkingConfigurationOutputTypeDef",
    "HierarchicalChunkingConfigurationTypeDef",
    "HierarchicalChunkingLevelConfigurationTypeDef",
    "HighlightTypeDef",
    "ImportJobDataTypeDef",
    "ImportJobSummaryTypeDef",
    "IntentDetectedDataDetailsTypeDef",
    "IntentInputDataTypeDef",
    "KnowledgeBaseAssociationConfigurationDataOutputTypeDef",
    "KnowledgeBaseAssociationConfigurationDataTypeDef",
    "KnowledgeBaseAssociationDataTypeDef",
    "KnowledgeBaseDataTypeDef",
    "KnowledgeBaseSummaryTypeDef",
    "ListAIAgentVersionsRequestPaginateTypeDef",
    "ListAIAgentVersionsRequestTypeDef",
    "ListAIAgentVersionsResponseTypeDef",
    "ListAIAgentsRequestPaginateTypeDef",
    "ListAIAgentsRequestTypeDef",
    "ListAIAgentsResponseTypeDef",
    "ListAIGuardrailVersionsRequestPaginateTypeDef",
    "ListAIGuardrailVersionsRequestTypeDef",
    "ListAIGuardrailVersionsResponseTypeDef",
    "ListAIGuardrailsRequestPaginateTypeDef",
    "ListAIGuardrailsRequestTypeDef",
    "ListAIGuardrailsResponseTypeDef",
    "ListAIPromptVersionsRequestPaginateTypeDef",
    "ListAIPromptVersionsRequestTypeDef",
    "ListAIPromptVersionsResponseTypeDef",
    "ListAIPromptsRequestPaginateTypeDef",
    "ListAIPromptsRequestTypeDef",
    "ListAIPromptsResponseTypeDef",
    "ListAssistantAssociationsRequestPaginateTypeDef",
    "ListAssistantAssociationsRequestTypeDef",
    "ListAssistantAssociationsResponseTypeDef",
    "ListAssistantsRequestPaginateTypeDef",
    "ListAssistantsRequestTypeDef",
    "ListAssistantsResponseTypeDef",
    "ListContentAssociationsRequestPaginateTypeDef",
    "ListContentAssociationsRequestTypeDef",
    "ListContentAssociationsResponseTypeDef",
    "ListContentsRequestPaginateTypeDef",
    "ListContentsRequestTypeDef",
    "ListContentsResponseTypeDef",
    "ListImportJobsRequestPaginateTypeDef",
    "ListImportJobsRequestTypeDef",
    "ListImportJobsResponseTypeDef",
    "ListKnowledgeBasesRequestPaginateTypeDef",
    "ListKnowledgeBasesRequestTypeDef",
    "ListKnowledgeBasesResponseTypeDef",
    "ListMessageTemplateVersionsRequestPaginateTypeDef",
    "ListMessageTemplateVersionsRequestTypeDef",
    "ListMessageTemplateVersionsResponseTypeDef",
    "ListMessageTemplatesRequestPaginateTypeDef",
    "ListMessageTemplatesRequestTypeDef",
    "ListMessageTemplatesResponseTypeDef",
    "ListMessagesRequestPaginateTypeDef",
    "ListMessagesRequestTypeDef",
    "ListMessagesResponseTypeDef",
    "ListQuickResponsesRequestPaginateTypeDef",
    "ListQuickResponsesRequestTypeDef",
    "ListQuickResponsesResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ManagedSourceConfigurationOutputTypeDef",
    "ManagedSourceConfigurationTypeDef",
    "ManualSearchAIAgentConfigurationOutputTypeDef",
    "ManualSearchAIAgentConfigurationTypeDef",
    "MessageDataTypeDef",
    "MessageInputTypeDef",
    "MessageOutputTypeDef",
    "MessageTemplateAttachmentTypeDef",
    "MessageTemplateAttributesOutputTypeDef",
    "MessageTemplateAttributesTypeDef",
    "MessageTemplateAttributesUnionTypeDef",
    "MessageTemplateBodyContentProviderTypeDef",
    "MessageTemplateContentProviderOutputTypeDef",
    "MessageTemplateContentProviderTypeDef",
    "MessageTemplateContentProviderUnionTypeDef",
    "MessageTemplateDataTypeDef",
    "MessageTemplateFilterFieldTypeDef",
    "MessageTemplateOrderFieldTypeDef",
    "MessageTemplateQueryFieldTypeDef",
    "MessageTemplateSearchExpressionTypeDef",
    "MessageTemplateSearchResultDataTypeDef",
    "MessageTemplateSummaryTypeDef",
    "MessageTemplateVersionSummaryTypeDef",
    "NotifyRecommendationsReceivedErrorTypeDef",
    "NotifyRecommendationsReceivedRequestTypeDef",
    "NotifyRecommendationsReceivedResponseTypeDef",
    "OrConditionOutputTypeDef",
    "OrConditionTypeDef",
    "PaginatorConfigTypeDef",
    "ParsingConfigurationTypeDef",
    "ParsingPromptTypeDef",
    "PutFeedbackRequestTypeDef",
    "PutFeedbackResponseTypeDef",
    "QueryAssistantRequestPaginateTypeDef",
    "QueryAssistantRequestTypeDef",
    "QueryAssistantResponsePaginatorTypeDef",
    "QueryAssistantResponseTypeDef",
    "QueryConditionItemTypeDef",
    "QueryConditionTypeDef",
    "QueryInputDataTypeDef",
    "QueryRecommendationTriggerDataTypeDef",
    "QueryTextInputDataTypeDef",
    "QuickResponseContentProviderTypeDef",
    "QuickResponseContentsTypeDef",
    "QuickResponseDataProviderTypeDef",
    "QuickResponseDataTypeDef",
    "QuickResponseFilterFieldTypeDef",
    "QuickResponseOrderFieldTypeDef",
    "QuickResponseQueryFieldTypeDef",
    "QuickResponseSearchExpressionTypeDef",
    "QuickResponseSearchResultDataTypeDef",
    "QuickResponseSummaryTypeDef",
    "RankingDataTypeDef",
    "RecommendationDataTypeDef",
    "RecommendationTriggerDataTypeDef",
    "RecommendationTriggerTypeDef",
    "RemoveAssistantAIAgentRequestTypeDef",
    "RemoveKnowledgeBaseTemplateUriRequestTypeDef",
    "RenderMessageTemplateRequestTypeDef",
    "RenderMessageTemplateResponseTypeDef",
    "RenderingConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "ResultDataPaginatorTypeDef",
    "ResultDataTypeDef",
    "RuntimeSessionDataTypeDef",
    "RuntimeSessionDataValueTypeDef",
    "SMSMessageTemplateContentBodyTypeDef",
    "SMSMessageTemplateContentTypeDef",
    "SearchContentRequestPaginateTypeDef",
    "SearchContentRequestTypeDef",
    "SearchContentResponseTypeDef",
    "SearchExpressionTypeDef",
    "SearchMessageTemplatesRequestPaginateTypeDef",
    "SearchMessageTemplatesRequestTypeDef",
    "SearchMessageTemplatesResponseTypeDef",
    "SearchQuickResponsesRequestPaginateTypeDef",
    "SearchQuickResponsesRequestTypeDef",
    "SearchQuickResponsesResponseTypeDef",
    "SearchSessionsRequestPaginateTypeDef",
    "SearchSessionsRequestTypeDef",
    "SearchSessionsResponseTypeDef",
    "SeedUrlTypeDef",
    "SelfServiceAIAgentConfigurationOutputTypeDef",
    "SelfServiceAIAgentConfigurationTypeDef",
    "SelfServiceConversationHistoryTypeDef",
    "SemanticChunkingConfigurationTypeDef",
    "SendMessageRequestTypeDef",
    "SendMessageResponseTypeDef",
    "ServerSideEncryptionConfigurationTypeDef",
    "SessionDataTypeDef",
    "SessionIntegrationConfigurationTypeDef",
    "SessionSummaryTypeDef",
    "SourceConfigurationOutputTypeDef",
    "SourceConfigurationTypeDef",
    "SourceConfigurationUnionTypeDef",
    "SourceContentDataDetailsTypeDef",
    "StartContentUploadRequestTypeDef",
    "StartContentUploadResponseTypeDef",
    "StartImportJobRequestTypeDef",
    "StartImportJobResponseTypeDef",
    "SystemAttributesTypeDef",
    "SystemEndpointAttributesTypeDef",
    "TagConditionTypeDef",
    "TagFilterOutputTypeDef",
    "TagFilterTypeDef",
    "TagFilterUnionTypeDef",
    "TagResourceRequestTypeDef",
    "TextDataTypeDef",
    "TextFullAIPromptEditTemplateConfigurationTypeDef",
    "TextMessageTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateAIAgentRequestTypeDef",
    "UpdateAIAgentResponseTypeDef",
    "UpdateAIGuardrailRequestTypeDef",
    "UpdateAIGuardrailResponseTypeDef",
    "UpdateAIPromptRequestTypeDef",
    "UpdateAIPromptResponseTypeDef",
    "UpdateAssistantAIAgentRequestTypeDef",
    "UpdateAssistantAIAgentResponseTypeDef",
    "UpdateContentRequestTypeDef",
    "UpdateContentResponseTypeDef",
    "UpdateKnowledgeBaseTemplateUriRequestTypeDef",
    "UpdateKnowledgeBaseTemplateUriResponseTypeDef",
    "UpdateMessageTemplateMetadataRequestTypeDef",
    "UpdateMessageTemplateMetadataResponseTypeDef",
    "UpdateMessageTemplateRequestTypeDef",
    "UpdateMessageTemplateResponseTypeDef",
    "UpdateQuickResponseRequestTypeDef",
    "UpdateQuickResponseResponseTypeDef",
    "UpdateSessionDataRequestTypeDef",
    "UpdateSessionDataResponseTypeDef",
    "UpdateSessionRequestTypeDef",
    "UpdateSessionResponseTypeDef",
    "UrlConfigurationOutputTypeDef",
    "UrlConfigurationTypeDef",
    "VectorIngestionConfigurationOutputTypeDef",
    "VectorIngestionConfigurationTypeDef",
    "VectorIngestionConfigurationUnionTypeDef",
    "WebCrawlerConfigurationOutputTypeDef",
    "WebCrawlerConfigurationTypeDef",
    "WebCrawlerLimitsTypeDef",
)


class AIAgentConfigurationDataTypeDef(TypedDict):
    aiAgentId: str


GuardrailContentFilterConfigTypeDef = TypedDict(
    "GuardrailContentFilterConfigTypeDef",
    {
        "inputStrength": GuardrailFilterStrengthType,
        "outputStrength": GuardrailFilterStrengthType,
        "type": GuardrailContentFilterTypeType,
    },
)
GuardrailContextualGroundingFilterConfigTypeDef = TypedDict(
    "GuardrailContextualGroundingFilterConfigTypeDef",
    {
        "threshold": float,
        "type": GuardrailContextualGroundingFilterTypeType,
    },
)
GuardrailPiiEntityConfigTypeDef = TypedDict(
    "GuardrailPiiEntityConfigTypeDef",
    {
        "action": GuardrailSensitiveInformationActionType,
        "type": GuardrailPiiEntityTypeType,
    },
)


class GuardrailRegexConfigTypeDef(TypedDict):
    action: GuardrailSensitiveInformationActionType
    name: str
    pattern: str
    description: NotRequired[str]


class AIGuardrailSummaryTypeDef(TypedDict):
    aiGuardrailArn: str
    aiGuardrailId: str
    assistantArn: str
    assistantId: str
    name: str
    visibilityStatus: VisibilityStatusType
    description: NotRequired[str]
    modifiedTime: NotRequired[datetime]
    status: NotRequired[StatusType]
    tags: NotRequired[Dict[str, str]]


GuardrailTopicConfigOutputTypeDef = TypedDict(
    "GuardrailTopicConfigOutputTypeDef",
    {
        "definition": str,
        "name": str,
        "type": Literal["DENY"],
        "examples": NotRequired[List[str]],
    },
)
GuardrailTopicConfigTypeDef = TypedDict(
    "GuardrailTopicConfigTypeDef",
    {
        "definition": str,
        "name": str,
        "type": Literal["DENY"],
        "examples": NotRequired[Sequence[str]],
    },
)
GuardrailManagedWordsConfigTypeDef = TypedDict(
    "GuardrailManagedWordsConfigTypeDef",
    {
        "type": Literal["PROFANITY"],
    },
)


class GuardrailWordConfigTypeDef(TypedDict):
    text: str


AIPromptSummaryTypeDef = TypedDict(
    "AIPromptSummaryTypeDef",
    {
        "aiPromptArn": str,
        "aiPromptId": str,
        "apiFormat": AIPromptAPIFormatType,
        "assistantArn": str,
        "assistantId": str,
        "modelId": str,
        "name": str,
        "templateType": Literal["TEXT"],
        "type": AIPromptTypeType,
        "visibilityStatus": VisibilityStatusType,
        "description": NotRequired[str],
        "modifiedTime": NotRequired[datetime],
        "origin": NotRequired[OriginType],
        "status": NotRequired[StatusType],
        "tags": NotRequired[Dict[str, str]],
    },
)


class TextFullAIPromptEditTemplateConfigurationTypeDef(TypedDict):
    text: str


class ActivateMessageTemplateRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    messageTemplateId: str
    versionNumber: int


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AgentAttributesTypeDef(TypedDict):
    firstName: NotRequired[str]
    lastName: NotRequired[str]


class AmazonConnectGuideAssociationDataTypeDef(TypedDict):
    flowId: NotRequired[str]


class AppIntegrationsConfigurationOutputTypeDef(TypedDict):
    appIntegrationArn: str
    objectFields: NotRequired[List[str]]


class AppIntegrationsConfigurationTypeDef(TypedDict):
    appIntegrationArn: str
    objectFields: NotRequired[Sequence[str]]


class AssistantAssociationInputDataTypeDef(TypedDict):
    knowledgeBaseId: NotRequired[str]


class KnowledgeBaseAssociationDataTypeDef(TypedDict):
    knowledgeBaseArn: NotRequired[str]
    knowledgeBaseId: NotRequired[str]


AssistantCapabilityConfigurationTypeDef = TypedDict(
    "AssistantCapabilityConfigurationTypeDef",
    {
        "type": NotRequired[AssistantCapabilityTypeType],
    },
)


class AssistantIntegrationConfigurationTypeDef(TypedDict):
    topicIntegrationArn: NotRequired[str]


class ServerSideEncryptionConfigurationTypeDef(TypedDict):
    kmsKeyId: NotRequired[str]


class ParsingPromptTypeDef(TypedDict):
    parsingPromptText: str


class FixedSizeChunkingConfigurationTypeDef(TypedDict):
    maxTokens: int
    overlapPercentage: int


class SemanticChunkingConfigurationTypeDef(TypedDict):
    breakpointPercentileThreshold: int
    bufferSize: int
    maxTokens: int


class CitationSpanTypeDef(TypedDict):
    beginOffsetInclusive: NotRequired[int]
    endOffsetExclusive: NotRequired[int]


class ConnectConfigurationTypeDef(TypedDict):
    instanceId: NotRequired[str]


class RankingDataTypeDef(TypedDict):
    relevanceLevel: NotRequired[RelevanceLevelType]
    relevanceScore: NotRequired[float]


class ContentDataTypeDef(TypedDict):
    contentArn: str
    contentId: str
    contentType: str
    knowledgeBaseArn: str
    knowledgeBaseId: str
    metadata: Dict[str, str]
    name: str
    revisionId: str
    status: ContentStatusType
    title: str
    url: str
    urlExpiry: datetime
    linkOutUri: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class GenerativeContentFeedbackDataTypeDef(TypedDict):
    relevance: RelevanceType


class ContentReferenceTypeDef(TypedDict):
    contentArn: NotRequired[str]
    contentId: NotRequired[str]
    knowledgeBaseArn: NotRequired[str]
    knowledgeBaseId: NotRequired[str]
    referenceType: NotRequired[ReferenceTypeType]
    sourceURL: NotRequired[str]


class ContentSummaryTypeDef(TypedDict):
    contentArn: str
    contentId: str
    contentType: str
    knowledgeBaseArn: str
    knowledgeBaseId: str
    metadata: Dict[str, str]
    name: str
    revisionId: str
    status: ContentStatusType
    title: str
    tags: NotRequired[Dict[str, str]]


class SelfServiceConversationHistoryTypeDef(TypedDict):
    turnNumber: int
    botResponse: NotRequired[str]
    inputTranscript: NotRequired[str]


class ConversationStateTypeDef(TypedDict):
    status: ConversationStatusType
    reason: NotRequired[ConversationStatusReasonType]


TimestampTypeDef = Union[datetime, str]


class CreateContentRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    name: str
    uploadId: str
    clientToken: NotRequired[str]
    metadata: NotRequired[Mapping[str, str]]
    overrideLinkOutUri: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    title: NotRequired[str]


class RenderingConfigurationTypeDef(TypedDict):
    templateUri: NotRequired[str]


class CreateMessageTemplateAttachmentRequestTypeDef(TypedDict):
    body: str
    contentDisposition: Literal["ATTACHMENT"]
    knowledgeBaseId: str
    messageTemplateId: str
    name: str
    clientToken: NotRequired[str]


class MessageTemplateAttachmentTypeDef(TypedDict):
    attachmentId: str
    contentDisposition: Literal["ATTACHMENT"]
    name: str
    uploadedTime: datetime
    url: str
    urlExpiry: datetime


class CreateMessageTemplateVersionRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    messageTemplateId: str
    messageTemplateContentSha256: NotRequired[str]


class QuickResponseDataProviderTypeDef(TypedDict):
    content: NotRequired[str]


class CustomerProfileAttributesOutputTypeDef(TypedDict):
    accountNumber: NotRequired[str]
    additionalInformation: NotRequired[str]
    address1: NotRequired[str]
    address2: NotRequired[str]
    address3: NotRequired[str]
    address4: NotRequired[str]
    billingAddress1: NotRequired[str]
    billingAddress2: NotRequired[str]
    billingAddress3: NotRequired[str]
    billingAddress4: NotRequired[str]
    billingCity: NotRequired[str]
    billingCountry: NotRequired[str]
    billingCounty: NotRequired[str]
    billingPostalCode: NotRequired[str]
    billingProvince: NotRequired[str]
    billingState: NotRequired[str]
    birthDate: NotRequired[str]
    businessEmailAddress: NotRequired[str]
    businessName: NotRequired[str]
    businessPhoneNumber: NotRequired[str]
    city: NotRequired[str]
    country: NotRequired[str]
    county: NotRequired[str]
    custom: NotRequired[Dict[str, str]]
    emailAddress: NotRequired[str]
    firstName: NotRequired[str]
    gender: NotRequired[str]
    homePhoneNumber: NotRequired[str]
    lastName: NotRequired[str]
    mailingAddress1: NotRequired[str]
    mailingAddress2: NotRequired[str]
    mailingAddress3: NotRequired[str]
    mailingAddress4: NotRequired[str]
    mailingCity: NotRequired[str]
    mailingCountry: NotRequired[str]
    mailingCounty: NotRequired[str]
    mailingPostalCode: NotRequired[str]
    mailingProvince: NotRequired[str]
    mailingState: NotRequired[str]
    middleName: NotRequired[str]
    mobilePhoneNumber: NotRequired[str]
    partyType: NotRequired[str]
    phoneNumber: NotRequired[str]
    postalCode: NotRequired[str]
    profileARN: NotRequired[str]
    profileId: NotRequired[str]
    province: NotRequired[str]
    shippingAddress1: NotRequired[str]
    shippingAddress2: NotRequired[str]
    shippingAddress3: NotRequired[str]
    shippingAddress4: NotRequired[str]
    shippingCity: NotRequired[str]
    shippingCountry: NotRequired[str]
    shippingCounty: NotRequired[str]
    shippingPostalCode: NotRequired[str]
    shippingProvince: NotRequired[str]
    shippingState: NotRequired[str]
    state: NotRequired[str]


class CustomerProfileAttributesTypeDef(TypedDict):
    accountNumber: NotRequired[str]
    additionalInformation: NotRequired[str]
    address1: NotRequired[str]
    address2: NotRequired[str]
    address3: NotRequired[str]
    address4: NotRequired[str]
    billingAddress1: NotRequired[str]
    billingAddress2: NotRequired[str]
    billingAddress3: NotRequired[str]
    billingAddress4: NotRequired[str]
    billingCity: NotRequired[str]
    billingCountry: NotRequired[str]
    billingCounty: NotRequired[str]
    billingPostalCode: NotRequired[str]
    billingProvince: NotRequired[str]
    billingState: NotRequired[str]
    birthDate: NotRequired[str]
    businessEmailAddress: NotRequired[str]
    businessName: NotRequired[str]
    businessPhoneNumber: NotRequired[str]
    city: NotRequired[str]
    country: NotRequired[str]
    county: NotRequired[str]
    custom: NotRequired[Mapping[str, str]]
    emailAddress: NotRequired[str]
    firstName: NotRequired[str]
    gender: NotRequired[str]
    homePhoneNumber: NotRequired[str]
    lastName: NotRequired[str]
    mailingAddress1: NotRequired[str]
    mailingAddress2: NotRequired[str]
    mailingAddress3: NotRequired[str]
    mailingAddress4: NotRequired[str]
    mailingCity: NotRequired[str]
    mailingCountry: NotRequired[str]
    mailingCounty: NotRequired[str]
    mailingPostalCode: NotRequired[str]
    mailingProvince: NotRequired[str]
    mailingState: NotRequired[str]
    middleName: NotRequired[str]
    mobilePhoneNumber: NotRequired[str]
    partyType: NotRequired[str]
    phoneNumber: NotRequired[str]
    postalCode: NotRequired[str]
    profileARN: NotRequired[str]
    profileId: NotRequired[str]
    province: NotRequired[str]
    shippingAddress1: NotRequired[str]
    shippingAddress2: NotRequired[str]
    shippingAddress3: NotRequired[str]
    shippingAddress4: NotRequired[str]
    shippingCity: NotRequired[str]
    shippingCountry: NotRequired[str]
    shippingCounty: NotRequired[str]
    shippingPostalCode: NotRequired[str]
    shippingProvince: NotRequired[str]
    shippingState: NotRequired[str]
    state: NotRequired[str]


class IntentDetectedDataDetailsTypeDef(TypedDict):
    intent: str
    intentId: str


class GenerativeReferenceTypeDef(TypedDict):
    generationId: NotRequired[str]
    modelId: NotRequired[str]


class DeactivateMessageTemplateRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    messageTemplateId: str
    versionNumber: int


class DeleteAIAgentRequestTypeDef(TypedDict):
    aiAgentId: str
    assistantId: str


class DeleteAIAgentVersionRequestTypeDef(TypedDict):
    aiAgentId: str
    assistantId: str
    versionNumber: int


class DeleteAIGuardrailRequestTypeDef(TypedDict):
    aiGuardrailId: str
    assistantId: str


class DeleteAIGuardrailVersionRequestTypeDef(TypedDict):
    aiGuardrailId: str
    assistantId: str
    versionNumber: int


class DeleteAIPromptRequestTypeDef(TypedDict):
    aiPromptId: str
    assistantId: str


class DeleteAIPromptVersionRequestTypeDef(TypedDict):
    aiPromptId: str
    assistantId: str
    versionNumber: int


class DeleteAssistantAssociationRequestTypeDef(TypedDict):
    assistantAssociationId: str
    assistantId: str


class DeleteAssistantRequestTypeDef(TypedDict):
    assistantId: str


class DeleteContentAssociationRequestTypeDef(TypedDict):
    contentAssociationId: str
    contentId: str
    knowledgeBaseId: str


class DeleteContentRequestTypeDef(TypedDict):
    contentId: str
    knowledgeBaseId: str


class DeleteImportJobRequestTypeDef(TypedDict):
    importJobId: str
    knowledgeBaseId: str


class DeleteKnowledgeBaseRequestTypeDef(TypedDict):
    knowledgeBaseId: str


class DeleteMessageTemplateAttachmentRequestTypeDef(TypedDict):
    attachmentId: str
    knowledgeBaseId: str
    messageTemplateId: str


class DeleteMessageTemplateRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    messageTemplateId: str


class DeleteQuickResponseRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    quickResponseId: str


class HighlightTypeDef(TypedDict):
    beginOffsetInclusive: NotRequired[int]
    endOffsetExclusive: NotRequired[int]


class EmailHeaderTypeDef(TypedDict):
    name: NotRequired[str]
    value: NotRequired[str]


class MessageTemplateBodyContentProviderTypeDef(TypedDict):
    content: NotRequired[str]


class GroupingConfigurationOutputTypeDef(TypedDict):
    criteria: NotRequired[str]
    values: NotRequired[List[str]]


FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "field": Literal["NAME"],
        "operator": Literal["EQUALS"],
        "value": str,
    },
)


class GetAIAgentRequestTypeDef(TypedDict):
    aiAgentId: str
    assistantId: str


class GetAIGuardrailRequestTypeDef(TypedDict):
    aiGuardrailId: str
    assistantId: str


class GetAIPromptRequestTypeDef(TypedDict):
    aiPromptId: str
    assistantId: str


class GetAssistantAssociationRequestTypeDef(TypedDict):
    assistantAssociationId: str
    assistantId: str


class GetAssistantRequestTypeDef(TypedDict):
    assistantId: str


class GetContentAssociationRequestTypeDef(TypedDict):
    contentAssociationId: str
    contentId: str
    knowledgeBaseId: str


class GetContentRequestTypeDef(TypedDict):
    contentId: str
    knowledgeBaseId: str


class GetContentSummaryRequestTypeDef(TypedDict):
    contentId: str
    knowledgeBaseId: str


class GetImportJobRequestTypeDef(TypedDict):
    importJobId: str
    knowledgeBaseId: str


class GetKnowledgeBaseRequestTypeDef(TypedDict):
    knowledgeBaseId: str


class GetMessageTemplateRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    messageTemplateId: str


class GetNextMessageRequestTypeDef(TypedDict):
    assistantId: str
    nextMessageToken: str
    sessionId: str


class GetQuickResponseRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    quickResponseId: str


class GetRecommendationsRequestTypeDef(TypedDict):
    assistantId: str
    sessionId: str
    maxResults: NotRequired[int]
    waitTimeSeconds: NotRequired[int]


class GetSessionRequestTypeDef(TypedDict):
    assistantId: str
    sessionId: str


class GroupingConfigurationTypeDef(TypedDict):
    criteria: NotRequired[str]
    values: NotRequired[Sequence[str]]


class HierarchicalChunkingLevelConfigurationTypeDef(TypedDict):
    maxTokens: int


class IntentInputDataTypeDef(TypedDict):
    intentId: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListAIAgentVersionsRequestTypeDef(TypedDict):
    aiAgentId: str
    assistantId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    origin: NotRequired[OriginType]


class ListAIAgentsRequestTypeDef(TypedDict):
    assistantId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    origin: NotRequired[OriginType]


class ListAIGuardrailVersionsRequestTypeDef(TypedDict):
    aiGuardrailId: str
    assistantId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListAIGuardrailsRequestTypeDef(TypedDict):
    assistantId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListAIPromptVersionsRequestTypeDef(TypedDict):
    aiPromptId: str
    assistantId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    origin: NotRequired[OriginType]


class ListAIPromptsRequestTypeDef(TypedDict):
    assistantId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    origin: NotRequired[OriginType]


class ListAssistantAssociationsRequestTypeDef(TypedDict):
    assistantId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListAssistantsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListContentAssociationsRequestTypeDef(TypedDict):
    contentId: str
    knowledgeBaseId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListContentsRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListImportJobsRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListKnowledgeBasesRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListMessageTemplateVersionsRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    messageTemplateId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class MessageTemplateVersionSummaryTypeDef(TypedDict):
    channelSubtype: ChannelSubtypeType
    isActive: bool
    knowledgeBaseArn: str
    knowledgeBaseId: str
    messageTemplateArn: str
    messageTemplateId: str
    name: str
    versionNumber: int


class ListMessageTemplatesRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class MessageTemplateSummaryTypeDef(TypedDict):
    channelSubtype: ChannelSubtypeType
    createdTime: datetime
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedBy: str
    lastModifiedTime: datetime
    messageTemplateArn: str
    messageTemplateId: str
    name: str
    activeVersionNumber: NotRequired[int]
    description: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class ListMessagesRequestTypeDef(TypedDict):
    assistantId: str
    sessionId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListQuickResponsesRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class QuickResponseSummaryTypeDef(TypedDict):
    contentType: str
    createdTime: datetime
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedTime: datetime
    name: str
    quickResponseArn: str
    quickResponseId: str
    status: QuickResponseStatusType
    channels: NotRequired[List[str]]
    description: NotRequired[str]
    isActive: NotRequired[bool]
    lastModifiedBy: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str


class TextMessageTypeDef(TypedDict):
    value: NotRequired[str]


MessageTemplateFilterFieldTypeDef = TypedDict(
    "MessageTemplateFilterFieldTypeDef",
    {
        "name": str,
        "operator": MessageTemplateFilterOperatorType,
        "includeNoExistence": NotRequired[bool],
        "values": NotRequired[Sequence[str]],
    },
)


class MessageTemplateOrderFieldTypeDef(TypedDict):
    name: str
    order: NotRequired[OrderType]


MessageTemplateQueryFieldTypeDef = TypedDict(
    "MessageTemplateQueryFieldTypeDef",
    {
        "name": str,
        "operator": MessageTemplateQueryOperatorType,
        "values": Sequence[str],
        "allowFuzziness": NotRequired[bool],
        "priority": NotRequired[PriorityType],
    },
)


class NotifyRecommendationsReceivedErrorTypeDef(TypedDict):
    message: NotRequired[str]
    recommendationId: NotRequired[str]


class NotifyRecommendationsReceivedRequestTypeDef(TypedDict):
    assistantId: str
    recommendationIds: Sequence[str]
    sessionId: str


class TagConditionTypeDef(TypedDict):
    key: str
    value: NotRequired[str]


class QueryConditionItemTypeDef(TypedDict):
    comparator: Literal["EQUALS"]
    field: Literal["RESULT_TYPE"]
    value: str


class QueryTextInputDataTypeDef(TypedDict):
    text: str


class QueryRecommendationTriggerDataTypeDef(TypedDict):
    text: NotRequired[str]


class QuickResponseContentProviderTypeDef(TypedDict):
    content: NotRequired[str]


QuickResponseFilterFieldTypeDef = TypedDict(
    "QuickResponseFilterFieldTypeDef",
    {
        "name": str,
        "operator": QuickResponseFilterOperatorType,
        "includeNoExistence": NotRequired[bool],
        "values": NotRequired[Sequence[str]],
    },
)


class QuickResponseOrderFieldTypeDef(TypedDict):
    name: str
    order: NotRequired[OrderType]


QuickResponseQueryFieldTypeDef = TypedDict(
    "QuickResponseQueryFieldTypeDef",
    {
        "name": str,
        "operator": QuickResponseQueryOperatorType,
        "values": Sequence[str],
        "allowFuzziness": NotRequired[bool],
        "priority": NotRequired[PriorityType],
    },
)


class RemoveAssistantAIAgentRequestTypeDef(TypedDict):
    aiAgentType: AIAgentTypeType
    assistantId: str


class RemoveKnowledgeBaseTemplateUriRequestTypeDef(TypedDict):
    knowledgeBaseId: str


class RuntimeSessionDataValueTypeDef(TypedDict):
    stringValue: NotRequired[str]


class SessionSummaryTypeDef(TypedDict):
    assistantArn: str
    assistantId: str
    sessionArn: str
    sessionId: str


class SeedUrlTypeDef(TypedDict):
    url: NotRequired[str]


class SessionIntegrationConfigurationTypeDef(TypedDict):
    topicIntegrationArn: NotRequired[str]


class StartContentUploadRequestTypeDef(TypedDict):
    contentType: str
    knowledgeBaseId: str
    presignedUrlTimeToLive: NotRequired[int]


class SystemEndpointAttributesTypeDef(TypedDict):
    address: NotRequired[str]


class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateContentRequestTypeDef(TypedDict):
    contentId: str
    knowledgeBaseId: str
    metadata: NotRequired[Mapping[str, str]]
    overrideLinkOutUri: NotRequired[str]
    removeOverrideLinkOutUri: NotRequired[bool]
    revisionId: NotRequired[str]
    title: NotRequired[str]
    uploadId: NotRequired[str]


class UpdateKnowledgeBaseTemplateUriRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    templateUri: str


class WebCrawlerLimitsTypeDef(TypedDict):
    rateLimit: NotRequired[int]


class UpdateAssistantAIAgentRequestTypeDef(TypedDict):
    aiAgentType: AIAgentTypeType
    assistantId: str
    configuration: AIAgentConfigurationDataTypeDef


class AIGuardrailContentPolicyConfigOutputTypeDef(TypedDict):
    filtersConfig: List[GuardrailContentFilterConfigTypeDef]


class AIGuardrailContentPolicyConfigTypeDef(TypedDict):
    filtersConfig: Sequence[GuardrailContentFilterConfigTypeDef]


class AIGuardrailContextualGroundingPolicyConfigOutputTypeDef(TypedDict):
    filtersConfig: List[GuardrailContextualGroundingFilterConfigTypeDef]


class AIGuardrailContextualGroundingPolicyConfigTypeDef(TypedDict):
    filtersConfig: Sequence[GuardrailContextualGroundingFilterConfigTypeDef]


class AIGuardrailSensitiveInformationPolicyConfigOutputTypeDef(TypedDict):
    piiEntitiesConfig: NotRequired[List[GuardrailPiiEntityConfigTypeDef]]
    regexesConfig: NotRequired[List[GuardrailRegexConfigTypeDef]]


class AIGuardrailSensitiveInformationPolicyConfigTypeDef(TypedDict):
    piiEntitiesConfig: NotRequired[Sequence[GuardrailPiiEntityConfigTypeDef]]
    regexesConfig: NotRequired[Sequence[GuardrailRegexConfigTypeDef]]


class AIGuardrailVersionSummaryTypeDef(TypedDict):
    aiGuardrailSummary: NotRequired[AIGuardrailSummaryTypeDef]
    versionNumber: NotRequired[int]


class AIGuardrailTopicPolicyConfigOutputTypeDef(TypedDict):
    topicsConfig: List[GuardrailTopicConfigOutputTypeDef]


class AIGuardrailTopicPolicyConfigTypeDef(TypedDict):
    topicsConfig: Sequence[GuardrailTopicConfigTypeDef]


class AIGuardrailWordPolicyConfigOutputTypeDef(TypedDict):
    managedWordListsConfig: NotRequired[List[GuardrailManagedWordsConfigTypeDef]]
    wordsConfig: NotRequired[List[GuardrailWordConfigTypeDef]]


class AIGuardrailWordPolicyConfigTypeDef(TypedDict):
    managedWordListsConfig: NotRequired[Sequence[GuardrailManagedWordsConfigTypeDef]]
    wordsConfig: NotRequired[Sequence[GuardrailWordConfigTypeDef]]


class AIPromptVersionSummaryTypeDef(TypedDict):
    aiPromptSummary: NotRequired[AIPromptSummaryTypeDef]
    versionNumber: NotRequired[int]


class AIPromptTemplateConfigurationTypeDef(TypedDict):
    textFullAIPromptEditTemplateConfiguration: NotRequired[
        TextFullAIPromptEditTemplateConfigurationTypeDef
    ]


class ActivateMessageTemplateResponseTypeDef(TypedDict):
    messageTemplateArn: str
    messageTemplateId: str
    versionNumber: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeactivateMessageTemplateResponseTypeDef(TypedDict):
    messageTemplateArn: str
    messageTemplateId: str
    versionNumber: int
    ResponseMetadata: ResponseMetadataTypeDef


class ListAIGuardrailsResponseTypeDef(TypedDict):
    aiGuardrailSummaries: List[AIGuardrailSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListAIPromptsResponseTypeDef(TypedDict):
    aiPromptSummaries: List[AIPromptSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class SendMessageResponseTypeDef(TypedDict):
    nextMessageToken: str
    requestMessageId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartContentUploadResponseTypeDef(TypedDict):
    headersToInclude: Dict[str, str]
    uploadId: str
    url: str
    urlExpiry: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class ContentAssociationContentsTypeDef(TypedDict):
    amazonConnectGuideAssociation: NotRequired[AmazonConnectGuideAssociationDataTypeDef]


class CreateAssistantAssociationRequestTypeDef(TypedDict):
    assistantId: str
    association: AssistantAssociationInputDataTypeDef
    associationType: Literal["KNOWLEDGE_BASE"]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class AssistantAssociationOutputDataTypeDef(TypedDict):
    knowledgeBaseAssociation: NotRequired[KnowledgeBaseAssociationDataTypeDef]


AssistantDataTypeDef = TypedDict(
    "AssistantDataTypeDef",
    {
        "assistantArn": str,
        "assistantId": str,
        "name": str,
        "status": AssistantStatusType,
        "type": Literal["AGENT"],
        "aiAgentConfiguration": NotRequired[Dict[AIAgentTypeType, AIAgentConfigurationDataTypeDef]],
        "capabilityConfiguration": NotRequired[AssistantCapabilityConfigurationTypeDef],
        "description": NotRequired[str],
        "integrationConfiguration": NotRequired[AssistantIntegrationConfigurationTypeDef],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "tags": NotRequired[Dict[str, str]],
    },
)
AssistantSummaryTypeDef = TypedDict(
    "AssistantSummaryTypeDef",
    {
        "assistantArn": str,
        "assistantId": str,
        "name": str,
        "status": AssistantStatusType,
        "type": Literal["AGENT"],
        "aiAgentConfiguration": NotRequired[Dict[AIAgentTypeType, AIAgentConfigurationDataTypeDef]],
        "capabilityConfiguration": NotRequired[AssistantCapabilityConfigurationTypeDef],
        "description": NotRequired[str],
        "integrationConfiguration": NotRequired[AssistantIntegrationConfigurationTypeDef],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "tags": NotRequired[Dict[str, str]],
    },
)
CreateAssistantRequestTypeDef = TypedDict(
    "CreateAssistantRequestTypeDef",
    {
        "name": str,
        "type": Literal["AGENT"],
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "tags": NotRequired[Mapping[str, str]],
    },
)


class BedrockFoundationModelConfigurationForParsingTypeDef(TypedDict):
    modelArn: str
    parsingPrompt: NotRequired[ParsingPromptTypeDef]


class ConfigurationTypeDef(TypedDict):
    connectConfiguration: NotRequired[ConnectConfigurationTypeDef]


class GenerativeDataDetailsPaginatorTypeDef(TypedDict):
    completion: str
    rankingData: RankingDataTypeDef
    references: List[Dict[str, Any]]


class GenerativeDataDetailsTypeDef(TypedDict):
    completion: str
    rankingData: RankingDataTypeDef
    references: List[Dict[str, Any]]


class CreateContentResponseTypeDef(TypedDict):
    content: ContentDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetContentResponseTypeDef(TypedDict):
    content: ContentDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateContentResponseTypeDef(TypedDict):
    content: ContentDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ContentFeedbackDataTypeDef(TypedDict):
    generativeContentFeedbackData: NotRequired[GenerativeContentFeedbackDataTypeDef]


class GetContentSummaryResponseTypeDef(TypedDict):
    contentSummary: ContentSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListContentsResponseTypeDef(TypedDict):
    contentSummaries: List[ContentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class SearchContentResponseTypeDef(TypedDict):
    contentSummaries: List[ContentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ConversationContextTypeDef(TypedDict):
    selfServiceConversationHistory: Sequence[SelfServiceConversationHistoryTypeDef]


class CreateAIAgentVersionRequestTypeDef(TypedDict):
    aiAgentId: str
    assistantId: str
    clientToken: NotRequired[str]
    modifiedTime: NotRequired[TimestampTypeDef]


class CreateAIGuardrailVersionRequestTypeDef(TypedDict):
    aiGuardrailId: str
    assistantId: str
    clientToken: NotRequired[str]
    modifiedTime: NotRequired[TimestampTypeDef]


class CreateAIPromptVersionRequestTypeDef(TypedDict):
    aiPromptId: str
    assistantId: str
    clientToken: NotRequired[str]
    modifiedTime: NotRequired[TimestampTypeDef]


class CreateMessageTemplateAttachmentResponseTypeDef(TypedDict):
    attachment: MessageTemplateAttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DataReferenceTypeDef(TypedDict):
    contentReference: NotRequired[ContentReferenceTypeDef]
    generativeReference: NotRequired[GenerativeReferenceTypeDef]


class DocumentTextTypeDef(TypedDict):
    highlights: NotRequired[List[HighlightTypeDef]]
    text: NotRequired[str]


class EmailMessageTemplateContentBodyTypeDef(TypedDict):
    html: NotRequired[MessageTemplateBodyContentProviderTypeDef]
    plainText: NotRequired[MessageTemplateBodyContentProviderTypeDef]


class SMSMessageTemplateContentBodyTypeDef(TypedDict):
    plainText: NotRequired[MessageTemplateBodyContentProviderTypeDef]


class MessageTemplateSearchResultDataTypeDef(TypedDict):
    channelSubtype: ChannelSubtypeType
    createdTime: datetime
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedBy: str
    lastModifiedTime: datetime
    messageTemplateArn: str
    messageTemplateId: str
    name: str
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationOutputTypeDef]
    isActive: NotRequired[bool]
    language: NotRequired[str]
    tags: NotRequired[Dict[str, str]]
    versionNumber: NotRequired[int]


class SearchExpressionTypeDef(TypedDict):
    filters: Sequence[FilterTypeDef]


GroupingConfigurationUnionTypeDef = Union[
    GroupingConfigurationTypeDef, GroupingConfigurationOutputTypeDef
]


class HierarchicalChunkingConfigurationOutputTypeDef(TypedDict):
    levelConfigurations: List[HierarchicalChunkingLevelConfigurationTypeDef]
    overlapTokens: int


class HierarchicalChunkingConfigurationTypeDef(TypedDict):
    levelConfigurations: Sequence[HierarchicalChunkingLevelConfigurationTypeDef]
    overlapTokens: int


class ListAIAgentVersionsRequestPaginateTypeDef(TypedDict):
    aiAgentId: str
    assistantId: str
    origin: NotRequired[OriginType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAIAgentsRequestPaginateTypeDef(TypedDict):
    assistantId: str
    origin: NotRequired[OriginType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAIGuardrailVersionsRequestPaginateTypeDef(TypedDict):
    aiGuardrailId: str
    assistantId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAIGuardrailsRequestPaginateTypeDef(TypedDict):
    assistantId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAIPromptVersionsRequestPaginateTypeDef(TypedDict):
    aiPromptId: str
    assistantId: str
    origin: NotRequired[OriginType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAIPromptsRequestPaginateTypeDef(TypedDict):
    assistantId: str
    origin: NotRequired[OriginType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAssistantAssociationsRequestPaginateTypeDef(TypedDict):
    assistantId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAssistantsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListContentAssociationsRequestPaginateTypeDef(TypedDict):
    contentId: str
    knowledgeBaseId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListContentsRequestPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListImportJobsRequestPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListKnowledgeBasesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMessageTemplateVersionsRequestPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    messageTemplateId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMessageTemplatesRequestPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMessagesRequestPaginateTypeDef(TypedDict):
    assistantId: str
    sessionId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListQuickResponsesRequestPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMessageTemplateVersionsResponseTypeDef(TypedDict):
    messageTemplateVersionSummaries: List[MessageTemplateVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListMessageTemplatesResponseTypeDef(TypedDict):
    messageTemplateSummaries: List[MessageTemplateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListQuickResponsesResponseTypeDef(TypedDict):
    quickResponseSummaries: List[QuickResponseSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class MessageDataTypeDef(TypedDict):
    text: NotRequired[TextMessageTypeDef]


class MessageTemplateSearchExpressionTypeDef(TypedDict):
    filters: NotRequired[Sequence[MessageTemplateFilterFieldTypeDef]]
    orderOnField: NotRequired[MessageTemplateOrderFieldTypeDef]
    queries: NotRequired[Sequence[MessageTemplateQueryFieldTypeDef]]


class NotifyRecommendationsReceivedResponseTypeDef(TypedDict):
    errors: List[NotifyRecommendationsReceivedErrorTypeDef]
    recommendationIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class OrConditionOutputTypeDef(TypedDict):
    andConditions: NotRequired[List[TagConditionTypeDef]]
    tagCondition: NotRequired[TagConditionTypeDef]


class OrConditionTypeDef(TypedDict):
    andConditions: NotRequired[Sequence[TagConditionTypeDef]]
    tagCondition: NotRequired[TagConditionTypeDef]


class QueryConditionTypeDef(TypedDict):
    single: NotRequired[QueryConditionItemTypeDef]


class QueryInputDataTypeDef(TypedDict):
    intentInputData: NotRequired[IntentInputDataTypeDef]
    queryTextInputData: NotRequired[QueryTextInputDataTypeDef]


class RecommendationTriggerDataTypeDef(TypedDict):
    query: NotRequired[QueryRecommendationTriggerDataTypeDef]


class QuickResponseContentsTypeDef(TypedDict):
    markdown: NotRequired[QuickResponseContentProviderTypeDef]
    plainText: NotRequired[QuickResponseContentProviderTypeDef]


class QuickResponseSearchExpressionTypeDef(TypedDict):
    filters: NotRequired[Sequence[QuickResponseFilterFieldTypeDef]]
    orderOnField: NotRequired[QuickResponseOrderFieldTypeDef]
    queries: NotRequired[Sequence[QuickResponseQueryFieldTypeDef]]


class RuntimeSessionDataTypeDef(TypedDict):
    key: str
    value: RuntimeSessionDataValueTypeDef


class SearchSessionsResponseTypeDef(TypedDict):
    sessionSummaries: List[SessionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UrlConfigurationOutputTypeDef(TypedDict):
    seedUrls: NotRequired[List[SeedUrlTypeDef]]


class UrlConfigurationTypeDef(TypedDict):
    seedUrls: NotRequired[Sequence[SeedUrlTypeDef]]


class SystemAttributesTypeDef(TypedDict):
    customerEndpoint: NotRequired[SystemEndpointAttributesTypeDef]
    name: NotRequired[str]
    systemEndpoint: NotRequired[SystemEndpointAttributesTypeDef]


AIGuardrailContentPolicyConfigUnionTypeDef = Union[
    AIGuardrailContentPolicyConfigTypeDef, AIGuardrailContentPolicyConfigOutputTypeDef
]
AIGuardrailContextualGroundingPolicyConfigUnionTypeDef = Union[
    AIGuardrailContextualGroundingPolicyConfigTypeDef,
    AIGuardrailContextualGroundingPolicyConfigOutputTypeDef,
]
AIGuardrailSensitiveInformationPolicyConfigUnionTypeDef = Union[
    AIGuardrailSensitiveInformationPolicyConfigTypeDef,
    AIGuardrailSensitiveInformationPolicyConfigOutputTypeDef,
]


class ListAIGuardrailVersionsResponseTypeDef(TypedDict):
    aiGuardrailVersionSummaries: List[AIGuardrailVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


AIGuardrailTopicPolicyConfigUnionTypeDef = Union[
    AIGuardrailTopicPolicyConfigTypeDef, AIGuardrailTopicPolicyConfigOutputTypeDef
]


class AIGuardrailDataTypeDef(TypedDict):
    aiGuardrailArn: str
    aiGuardrailId: str
    assistantArn: str
    assistantId: str
    blockedInputMessaging: str
    blockedOutputsMessaging: str
    name: str
    visibilityStatus: VisibilityStatusType
    contentPolicyConfig: NotRequired[AIGuardrailContentPolicyConfigOutputTypeDef]
    contextualGroundingPolicyConfig: NotRequired[
        AIGuardrailContextualGroundingPolicyConfigOutputTypeDef
    ]
    description: NotRequired[str]
    modifiedTime: NotRequired[datetime]
    sensitiveInformationPolicyConfig: NotRequired[
        AIGuardrailSensitiveInformationPolicyConfigOutputTypeDef
    ]
    status: NotRequired[StatusType]
    tags: NotRequired[Dict[str, str]]
    topicPolicyConfig: NotRequired[AIGuardrailTopicPolicyConfigOutputTypeDef]
    wordPolicyConfig: NotRequired[AIGuardrailWordPolicyConfigOutputTypeDef]


AIGuardrailWordPolicyConfigUnionTypeDef = Union[
    AIGuardrailWordPolicyConfigTypeDef, AIGuardrailWordPolicyConfigOutputTypeDef
]


class ListAIPromptVersionsResponseTypeDef(TypedDict):
    aiPromptVersionSummaries: List[AIPromptVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


AIPromptDataTypeDef = TypedDict(
    "AIPromptDataTypeDef",
    {
        "aiPromptArn": str,
        "aiPromptId": str,
        "apiFormat": AIPromptAPIFormatType,
        "assistantArn": str,
        "assistantId": str,
        "modelId": str,
        "name": str,
        "templateConfiguration": AIPromptTemplateConfigurationTypeDef,
        "templateType": Literal["TEXT"],
        "type": AIPromptTypeType,
        "visibilityStatus": VisibilityStatusType,
        "description": NotRequired[str],
        "modifiedTime": NotRequired[datetime],
        "origin": NotRequired[OriginType],
        "status": NotRequired[StatusType],
        "tags": NotRequired[Dict[str, str]],
    },
)
CreateAIPromptRequestTypeDef = TypedDict(
    "CreateAIPromptRequestTypeDef",
    {
        "apiFormat": AIPromptAPIFormatType,
        "assistantId": str,
        "modelId": str,
        "name": str,
        "templateConfiguration": AIPromptTemplateConfigurationTypeDef,
        "templateType": Literal["TEXT"],
        "type": AIPromptTypeType,
        "visibilityStatus": VisibilityStatusType,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)


class UpdateAIPromptRequestTypeDef(TypedDict):
    aiPromptId: str
    assistantId: str
    visibilityStatus: VisibilityStatusType
    clientToken: NotRequired[str]
    description: NotRequired[str]
    templateConfiguration: NotRequired[AIPromptTemplateConfigurationTypeDef]


class ContentAssociationDataTypeDef(TypedDict):
    associationData: ContentAssociationContentsTypeDef
    associationType: Literal["AMAZON_CONNECT_GUIDE"]
    contentArn: str
    contentAssociationArn: str
    contentAssociationId: str
    contentId: str
    knowledgeBaseArn: str
    knowledgeBaseId: str
    tags: NotRequired[Dict[str, str]]


class ContentAssociationSummaryTypeDef(TypedDict):
    associationData: ContentAssociationContentsTypeDef
    associationType: Literal["AMAZON_CONNECT_GUIDE"]
    contentArn: str
    contentAssociationArn: str
    contentAssociationId: str
    contentId: str
    knowledgeBaseArn: str
    knowledgeBaseId: str
    tags: NotRequired[Dict[str, str]]


class CreateContentAssociationRequestTypeDef(TypedDict):
    association: ContentAssociationContentsTypeDef
    associationType: Literal["AMAZON_CONNECT_GUIDE"]
    contentId: str
    knowledgeBaseId: str
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class AssistantAssociationDataTypeDef(TypedDict):
    assistantArn: str
    assistantAssociationArn: str
    assistantAssociationId: str
    assistantId: str
    associationData: AssistantAssociationOutputDataTypeDef
    associationType: Literal["KNOWLEDGE_BASE"]
    tags: NotRequired[Dict[str, str]]


class AssistantAssociationSummaryTypeDef(TypedDict):
    assistantArn: str
    assistantAssociationArn: str
    assistantAssociationId: str
    assistantId: str
    associationData: AssistantAssociationOutputDataTypeDef
    associationType: Literal["KNOWLEDGE_BASE"]
    tags: NotRequired[Dict[str, str]]


class CreateAssistantResponseTypeDef(TypedDict):
    assistant: AssistantDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetAssistantResponseTypeDef(TypedDict):
    assistant: AssistantDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAssistantAIAgentResponseTypeDef(TypedDict):
    assistant: AssistantDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListAssistantsResponseTypeDef(TypedDict):
    assistantSummaries: List[AssistantSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ParsingConfigurationTypeDef(TypedDict):
    parsingStrategy: Literal["BEDROCK_FOUNDATION_MODEL"]
    bedrockFoundationModelConfiguration: NotRequired[
        BedrockFoundationModelConfigurationForParsingTypeDef
    ]


class ExternalSourceConfigurationTypeDef(TypedDict):
    configuration: ConfigurationTypeDef
    source: Literal["AMAZON_CONNECT"]


class PutFeedbackRequestTypeDef(TypedDict):
    assistantId: str
    contentFeedback: ContentFeedbackDataTypeDef
    targetId: str
    targetType: TargetTypeType


class PutFeedbackResponseTypeDef(TypedDict):
    assistantArn: str
    assistantId: str
    contentFeedback: ContentFeedbackDataTypeDef
    targetId: str
    targetType: TargetTypeType
    ResponseMetadata: ResponseMetadataTypeDef


class DocumentTypeDef(TypedDict):
    contentReference: ContentReferenceTypeDef
    excerpt: NotRequired[DocumentTextTypeDef]
    title: NotRequired[DocumentTextTypeDef]


class TextDataTypeDef(TypedDict):
    excerpt: NotRequired[DocumentTextTypeDef]
    title: NotRequired[DocumentTextTypeDef]


class EmailMessageTemplateContentOutputTypeDef(TypedDict):
    body: NotRequired[EmailMessageTemplateContentBodyTypeDef]
    headers: NotRequired[List[EmailHeaderTypeDef]]
    subject: NotRequired[str]


class EmailMessageTemplateContentTypeDef(TypedDict):
    body: NotRequired[EmailMessageTemplateContentBodyTypeDef]
    headers: NotRequired[Sequence[EmailHeaderTypeDef]]
    subject: NotRequired[str]


class SMSMessageTemplateContentTypeDef(TypedDict):
    body: NotRequired[SMSMessageTemplateContentBodyTypeDef]


class SearchMessageTemplatesResponseTypeDef(TypedDict):
    results: List[MessageTemplateSearchResultDataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class SearchContentRequestPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    searchExpression: SearchExpressionTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchContentRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    searchExpression: SearchExpressionTypeDef
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class SearchSessionsRequestPaginateTypeDef(TypedDict):
    assistantId: str
    searchExpression: SearchExpressionTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchSessionsRequestTypeDef(TypedDict):
    assistantId: str
    searchExpression: SearchExpressionTypeDef
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class CreateQuickResponseRequestTypeDef(TypedDict):
    content: QuickResponseDataProviderTypeDef
    knowledgeBaseId: str
    name: str
    channels: NotRequired[Sequence[str]]
    clientToken: NotRequired[str]
    contentType: NotRequired[str]
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationUnionTypeDef]
    isActive: NotRequired[bool]
    language: NotRequired[str]
    shortcutKey: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class UpdateMessageTemplateMetadataRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    messageTemplateId: str
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationUnionTypeDef]
    name: NotRequired[str]


class UpdateQuickResponseRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    quickResponseId: str
    channels: NotRequired[Sequence[str]]
    content: NotRequired[QuickResponseDataProviderTypeDef]
    contentType: NotRequired[str]
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationUnionTypeDef]
    isActive: NotRequired[bool]
    language: NotRequired[str]
    name: NotRequired[str]
    removeDescription: NotRequired[bool]
    removeGroupingConfiguration: NotRequired[bool]
    removeShortcutKey: NotRequired[bool]
    shortcutKey: NotRequired[str]


class ChunkingConfigurationOutputTypeDef(TypedDict):
    chunkingStrategy: ChunkingStrategyType
    fixedSizeChunkingConfiguration: NotRequired[FixedSizeChunkingConfigurationTypeDef]
    hierarchicalChunkingConfiguration: NotRequired[HierarchicalChunkingConfigurationOutputTypeDef]
    semanticChunkingConfiguration: NotRequired[SemanticChunkingConfigurationTypeDef]


class ChunkingConfigurationTypeDef(TypedDict):
    chunkingStrategy: ChunkingStrategyType
    fixedSizeChunkingConfiguration: NotRequired[FixedSizeChunkingConfigurationTypeDef]
    hierarchicalChunkingConfiguration: NotRequired[HierarchicalChunkingConfigurationTypeDef]
    semanticChunkingConfiguration: NotRequired[SemanticChunkingConfigurationTypeDef]


class MessageInputTypeDef(TypedDict):
    value: MessageDataTypeDef


class MessageOutputTypeDef(TypedDict):
    messageId: str
    participant: ParticipantType
    timestamp: datetime
    value: MessageDataTypeDef


class SearchMessageTemplatesRequestPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    searchExpression: MessageTemplateSearchExpressionTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchMessageTemplatesRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    searchExpression: MessageTemplateSearchExpressionTypeDef
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class TagFilterOutputTypeDef(TypedDict):
    andConditions: NotRequired[List[TagConditionTypeDef]]
    orConditions: NotRequired[List[OrConditionOutputTypeDef]]
    tagCondition: NotRequired[TagConditionTypeDef]


class TagFilterTypeDef(TypedDict):
    andConditions: NotRequired[Sequence[TagConditionTypeDef]]
    orConditions: NotRequired[Sequence[OrConditionTypeDef]]
    tagCondition: NotRequired[TagConditionTypeDef]


class QueryAssistantRequestPaginateTypeDef(TypedDict):
    assistantId: str
    overrideKnowledgeBaseSearchType: NotRequired[KnowledgeBaseSearchTypeType]
    queryCondition: NotRequired[Sequence[QueryConditionTypeDef]]
    queryInputData: NotRequired[QueryInputDataTypeDef]
    queryText: NotRequired[str]
    sessionId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class QueryAssistantRequestTypeDef(TypedDict):
    assistantId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    overrideKnowledgeBaseSearchType: NotRequired[KnowledgeBaseSearchTypeType]
    queryCondition: NotRequired[Sequence[QueryConditionTypeDef]]
    queryInputData: NotRequired[QueryInputDataTypeDef]
    queryText: NotRequired[str]
    sessionId: NotRequired[str]


RecommendationTriggerTypeDef = TypedDict(
    "RecommendationTriggerTypeDef",
    {
        "data": RecommendationTriggerDataTypeDef,
        "id": str,
        "recommendationIds": List[str],
        "source": RecommendationSourceTypeType,
        "type": RecommendationTriggerTypeType,
    },
)


class QuickResponseDataTypeDef(TypedDict):
    contentType: str
    createdTime: datetime
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedTime: datetime
    name: str
    quickResponseArn: str
    quickResponseId: str
    status: QuickResponseStatusType
    channels: NotRequired[List[str]]
    contents: NotRequired[QuickResponseContentsTypeDef]
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationOutputTypeDef]
    isActive: NotRequired[bool]
    language: NotRequired[str]
    lastModifiedBy: NotRequired[str]
    shortcutKey: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class QuickResponseSearchResultDataTypeDef(TypedDict):
    contentType: str
    contents: QuickResponseContentsTypeDef
    createdTime: datetime
    isActive: bool
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedTime: datetime
    name: str
    quickResponseArn: str
    quickResponseId: str
    status: QuickResponseStatusType
    attributesInterpolated: NotRequired[List[str]]
    attributesNotInterpolated: NotRequired[List[str]]
    channels: NotRequired[List[str]]
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationOutputTypeDef]
    language: NotRequired[str]
    lastModifiedBy: NotRequired[str]
    shortcutKey: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class SearchQuickResponsesRequestPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    searchExpression: QuickResponseSearchExpressionTypeDef
    attributes: NotRequired[Mapping[str, str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchQuickResponsesRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    searchExpression: QuickResponseSearchExpressionTypeDef
    attributes: NotRequired[Mapping[str, str]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class UpdateSessionDataRequestTypeDef(TypedDict):
    assistantId: str
    data: Sequence[RuntimeSessionDataTypeDef]
    sessionId: str
    namespace: NotRequired[Literal["Custom"]]


class UpdateSessionDataResponseTypeDef(TypedDict):
    data: List[RuntimeSessionDataTypeDef]
    namespace: Literal["Custom"]
    sessionArn: str
    sessionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class WebCrawlerConfigurationOutputTypeDef(TypedDict):
    urlConfiguration: UrlConfigurationOutputTypeDef
    crawlerLimits: NotRequired[WebCrawlerLimitsTypeDef]
    exclusionFilters: NotRequired[List[str]]
    inclusionFilters: NotRequired[List[str]]
    scope: NotRequired[WebScopeTypeType]


class WebCrawlerConfigurationTypeDef(TypedDict):
    urlConfiguration: UrlConfigurationTypeDef
    crawlerLimits: NotRequired[WebCrawlerLimitsTypeDef]
    exclusionFilters: NotRequired[Sequence[str]]
    inclusionFilters: NotRequired[Sequence[str]]
    scope: NotRequired[WebScopeTypeType]


class MessageTemplateAttributesOutputTypeDef(TypedDict):
    agentAttributes: NotRequired[AgentAttributesTypeDef]
    customAttributes: NotRequired[Dict[str, str]]
    customerProfileAttributes: NotRequired[CustomerProfileAttributesOutputTypeDef]
    systemAttributes: NotRequired[SystemAttributesTypeDef]


class MessageTemplateAttributesTypeDef(TypedDict):
    agentAttributes: NotRequired[AgentAttributesTypeDef]
    customAttributes: NotRequired[Mapping[str, str]]
    customerProfileAttributes: NotRequired[CustomerProfileAttributesTypeDef]
    systemAttributes: NotRequired[SystemAttributesTypeDef]


class CreateAIGuardrailResponseTypeDef(TypedDict):
    aiGuardrail: AIGuardrailDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAIGuardrailVersionResponseTypeDef(TypedDict):
    aiGuardrail: AIGuardrailDataTypeDef
    versionNumber: int
    ResponseMetadata: ResponseMetadataTypeDef


class GetAIGuardrailResponseTypeDef(TypedDict):
    aiGuardrail: AIGuardrailDataTypeDef
    versionNumber: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAIGuardrailResponseTypeDef(TypedDict):
    aiGuardrail: AIGuardrailDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAIGuardrailRequestTypeDef(TypedDict):
    assistantId: str
    blockedInputMessaging: str
    blockedOutputsMessaging: str
    name: str
    visibilityStatus: VisibilityStatusType
    clientToken: NotRequired[str]
    contentPolicyConfig: NotRequired[AIGuardrailContentPolicyConfigUnionTypeDef]
    contextualGroundingPolicyConfig: NotRequired[
        AIGuardrailContextualGroundingPolicyConfigUnionTypeDef
    ]
    description: NotRequired[str]
    sensitiveInformationPolicyConfig: NotRequired[
        AIGuardrailSensitiveInformationPolicyConfigUnionTypeDef
    ]
    tags: NotRequired[Mapping[str, str]]
    topicPolicyConfig: NotRequired[AIGuardrailTopicPolicyConfigUnionTypeDef]
    wordPolicyConfig: NotRequired[AIGuardrailWordPolicyConfigUnionTypeDef]


class UpdateAIGuardrailRequestTypeDef(TypedDict):
    aiGuardrailId: str
    assistantId: str
    blockedInputMessaging: str
    blockedOutputsMessaging: str
    visibilityStatus: VisibilityStatusType
    clientToken: NotRequired[str]
    contentPolicyConfig: NotRequired[AIGuardrailContentPolicyConfigUnionTypeDef]
    contextualGroundingPolicyConfig: NotRequired[
        AIGuardrailContextualGroundingPolicyConfigUnionTypeDef
    ]
    description: NotRequired[str]
    sensitiveInformationPolicyConfig: NotRequired[
        AIGuardrailSensitiveInformationPolicyConfigUnionTypeDef
    ]
    topicPolicyConfig: NotRequired[AIGuardrailTopicPolicyConfigUnionTypeDef]
    wordPolicyConfig: NotRequired[AIGuardrailWordPolicyConfigUnionTypeDef]


class CreateAIPromptResponseTypeDef(TypedDict):
    aiPrompt: AIPromptDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAIPromptVersionResponseTypeDef(TypedDict):
    aiPrompt: AIPromptDataTypeDef
    versionNumber: int
    ResponseMetadata: ResponseMetadataTypeDef


class GetAIPromptResponseTypeDef(TypedDict):
    aiPrompt: AIPromptDataTypeDef
    versionNumber: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAIPromptResponseTypeDef(TypedDict):
    aiPrompt: AIPromptDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateContentAssociationResponseTypeDef(TypedDict):
    contentAssociation: ContentAssociationDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetContentAssociationResponseTypeDef(TypedDict):
    contentAssociation: ContentAssociationDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListContentAssociationsResponseTypeDef(TypedDict):
    contentAssociationSummaries: List[ContentAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateAssistantAssociationResponseTypeDef(TypedDict):
    assistantAssociation: AssistantAssociationDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetAssistantAssociationResponseTypeDef(TypedDict):
    assistantAssociation: AssistantAssociationDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListAssistantAssociationsResponseTypeDef(TypedDict):
    assistantAssociationSummaries: List[AssistantAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ImportJobDataTypeDef(TypedDict):
    createdTime: datetime
    importJobId: str
    importJobType: Literal["QUICK_RESPONSES"]
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedTime: datetime
    status: ImportJobStatusType
    uploadId: str
    url: str
    urlExpiry: datetime
    externalSourceConfiguration: NotRequired[ExternalSourceConfigurationTypeDef]
    failedRecordReport: NotRequired[str]
    metadata: NotRequired[Dict[str, str]]


class ImportJobSummaryTypeDef(TypedDict):
    createdTime: datetime
    importJobId: str
    importJobType: Literal["QUICK_RESPONSES"]
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedTime: datetime
    status: ImportJobStatusType
    uploadId: str
    externalSourceConfiguration: NotRequired[ExternalSourceConfigurationTypeDef]
    metadata: NotRequired[Dict[str, str]]


class StartImportJobRequestTypeDef(TypedDict):
    importJobType: Literal["QUICK_RESPONSES"]
    knowledgeBaseId: str
    uploadId: str
    clientToken: NotRequired[str]
    externalSourceConfiguration: NotRequired[ExternalSourceConfigurationTypeDef]
    metadata: NotRequired[Mapping[str, str]]


class ContentDataDetailsTypeDef(TypedDict):
    rankingData: RankingDataTypeDef
    textData: TextDataTypeDef


SourceContentDataDetailsTypeDef = TypedDict(
    "SourceContentDataDetailsTypeDef",
    {
        "id": str,
        "rankingData": RankingDataTypeDef,
        "textData": TextDataTypeDef,
        "type": Literal["KNOWLEDGE_CONTENT"],
        "citationSpan": NotRequired[CitationSpanTypeDef],
    },
)


class MessageTemplateContentProviderOutputTypeDef(TypedDict):
    email: NotRequired[EmailMessageTemplateContentOutputTypeDef]
    sms: NotRequired[SMSMessageTemplateContentTypeDef]


class MessageTemplateContentProviderTypeDef(TypedDict):
    email: NotRequired[EmailMessageTemplateContentTypeDef]
    sms: NotRequired[SMSMessageTemplateContentTypeDef]


class VectorIngestionConfigurationOutputTypeDef(TypedDict):
    chunkingConfiguration: NotRequired[ChunkingConfigurationOutputTypeDef]
    parsingConfiguration: NotRequired[ParsingConfigurationTypeDef]


class VectorIngestionConfigurationTypeDef(TypedDict):
    chunkingConfiguration: NotRequired[ChunkingConfigurationTypeDef]
    parsingConfiguration: NotRequired[ParsingConfigurationTypeDef]


SendMessageRequestTypeDef = TypedDict(
    "SendMessageRequestTypeDef",
    {
        "assistantId": str,
        "message": MessageInputTypeDef,
        "sessionId": str,
        "type": Literal["TEXT"],
        "clientToken": NotRequired[str],
        "conversationContext": NotRequired[ConversationContextTypeDef],
    },
)
GetNextMessageResponseTypeDef = TypedDict(
    "GetNextMessageResponseTypeDef",
    {
        "conversationSessionData": List[RuntimeSessionDataTypeDef],
        "conversationState": ConversationStateTypeDef,
        "nextMessageToken": str,
        "requestMessageId": str,
        "response": MessageOutputTypeDef,
        "type": Literal["TEXT"],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class ListMessagesResponseTypeDef(TypedDict):
    messages: List[MessageOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class KnowledgeBaseAssociationConfigurationDataOutputTypeDef(TypedDict):
    contentTagFilter: NotRequired[TagFilterOutputTypeDef]
    maxResults: NotRequired[int]
    overrideKnowledgeBaseSearchType: NotRequired[KnowledgeBaseSearchTypeType]


class SessionDataTypeDef(TypedDict):
    name: str
    sessionArn: str
    sessionId: str
    aiAgentConfiguration: NotRequired[Dict[AIAgentTypeType, AIAgentConfigurationDataTypeDef]]
    description: NotRequired[str]
    integrationConfiguration: NotRequired[SessionIntegrationConfigurationTypeDef]
    tagFilter: NotRequired[TagFilterOutputTypeDef]
    tags: NotRequired[Dict[str, str]]


class KnowledgeBaseAssociationConfigurationDataTypeDef(TypedDict):
    contentTagFilter: NotRequired[TagFilterTypeDef]
    maxResults: NotRequired[int]
    overrideKnowledgeBaseSearchType: NotRequired[KnowledgeBaseSearchTypeType]


TagFilterUnionTypeDef = Union[TagFilterTypeDef, TagFilterOutputTypeDef]


class CreateQuickResponseResponseTypeDef(TypedDict):
    quickResponse: QuickResponseDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetQuickResponseResponseTypeDef(TypedDict):
    quickResponse: QuickResponseDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateQuickResponseResponseTypeDef(TypedDict):
    quickResponse: QuickResponseDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SearchQuickResponsesResponseTypeDef(TypedDict):
    results: List[QuickResponseSearchResultDataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ManagedSourceConfigurationOutputTypeDef(TypedDict):
    webCrawlerConfiguration: NotRequired[WebCrawlerConfigurationOutputTypeDef]


class ManagedSourceConfigurationTypeDef(TypedDict):
    webCrawlerConfiguration: NotRequired[WebCrawlerConfigurationTypeDef]


MessageTemplateAttributesUnionTypeDef = Union[
    MessageTemplateAttributesTypeDef, MessageTemplateAttributesOutputTypeDef
]


class GetImportJobResponseTypeDef(TypedDict):
    importJob: ImportJobDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StartImportJobResponseTypeDef(TypedDict):
    importJob: ImportJobDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListImportJobsResponseTypeDef(TypedDict):
    importJobSummaries: List[ImportJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DataDetailsPaginatorTypeDef(TypedDict):
    contentData: NotRequired[ContentDataDetailsTypeDef]
    generativeData: NotRequired[GenerativeDataDetailsPaginatorTypeDef]
    intentDetectedData: NotRequired[IntentDetectedDataDetailsTypeDef]
    sourceContentData: NotRequired[SourceContentDataDetailsTypeDef]


class DataDetailsTypeDef(TypedDict):
    contentData: NotRequired[ContentDataDetailsTypeDef]
    generativeData: NotRequired[GenerativeDataDetailsTypeDef]
    intentDetectedData: NotRequired[IntentDetectedDataDetailsTypeDef]
    sourceContentData: NotRequired[SourceContentDataDetailsTypeDef]


class ExtendedMessageTemplateDataTypeDef(TypedDict):
    channelSubtype: ChannelSubtypeType
    content: MessageTemplateContentProviderOutputTypeDef
    createdTime: datetime
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedBy: str
    lastModifiedTime: datetime
    messageTemplateArn: str
    messageTemplateContentSha256: str
    messageTemplateId: str
    name: str
    attachments: NotRequired[List[MessageTemplateAttachmentTypeDef]]
    attributeTypes: NotRequired[List[MessageTemplateAttributeTypeType]]
    defaultAttributes: NotRequired[MessageTemplateAttributesOutputTypeDef]
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationOutputTypeDef]
    isActive: NotRequired[bool]
    language: NotRequired[str]
    tags: NotRequired[Dict[str, str]]
    versionNumber: NotRequired[int]


class MessageTemplateDataTypeDef(TypedDict):
    channelSubtype: ChannelSubtypeType
    content: MessageTemplateContentProviderOutputTypeDef
    createdTime: datetime
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedBy: str
    lastModifiedTime: datetime
    messageTemplateArn: str
    messageTemplateContentSha256: str
    messageTemplateId: str
    name: str
    attributeTypes: NotRequired[List[MessageTemplateAttributeTypeType]]
    defaultAttributes: NotRequired[MessageTemplateAttributesOutputTypeDef]
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationOutputTypeDef]
    language: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class RenderMessageTemplateResponseTypeDef(TypedDict):
    attachments: List[MessageTemplateAttachmentTypeDef]
    attributesNotInterpolated: List[str]
    content: MessageTemplateContentProviderOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


MessageTemplateContentProviderUnionTypeDef = Union[
    MessageTemplateContentProviderTypeDef, MessageTemplateContentProviderOutputTypeDef
]
VectorIngestionConfigurationUnionTypeDef = Union[
    VectorIngestionConfigurationTypeDef, VectorIngestionConfigurationOutputTypeDef
]


class AssociationConfigurationDataOutputTypeDef(TypedDict):
    knowledgeBaseAssociationConfigurationData: NotRequired[
        KnowledgeBaseAssociationConfigurationDataOutputTypeDef
    ]


class CreateSessionResponseTypeDef(TypedDict):
    session: SessionDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetSessionResponseTypeDef(TypedDict):
    session: SessionDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSessionResponseTypeDef(TypedDict):
    session: SessionDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AssociationConfigurationDataTypeDef(TypedDict):
    knowledgeBaseAssociationConfigurationData: NotRequired[
        KnowledgeBaseAssociationConfigurationDataTypeDef
    ]


class CreateSessionRequestTypeDef(TypedDict):
    assistantId: str
    name: str
    aiAgentConfiguration: NotRequired[Mapping[AIAgentTypeType, AIAgentConfigurationDataTypeDef]]
    clientToken: NotRequired[str]
    description: NotRequired[str]
    tagFilter: NotRequired[TagFilterUnionTypeDef]
    tags: NotRequired[Mapping[str, str]]


class UpdateSessionRequestTypeDef(TypedDict):
    assistantId: str
    sessionId: str
    aiAgentConfiguration: NotRequired[Mapping[AIAgentTypeType, AIAgentConfigurationDataTypeDef]]
    description: NotRequired[str]
    tagFilter: NotRequired[TagFilterUnionTypeDef]


class SourceConfigurationOutputTypeDef(TypedDict):
    appIntegrations: NotRequired[AppIntegrationsConfigurationOutputTypeDef]
    managedSourceConfiguration: NotRequired[ManagedSourceConfigurationOutputTypeDef]


class SourceConfigurationTypeDef(TypedDict):
    appIntegrations: NotRequired[AppIntegrationsConfigurationTypeDef]
    managedSourceConfiguration: NotRequired[ManagedSourceConfigurationTypeDef]


class RenderMessageTemplateRequestTypeDef(TypedDict):
    attributes: MessageTemplateAttributesUnionTypeDef
    knowledgeBaseId: str
    messageTemplateId: str


class DataSummaryPaginatorTypeDef(TypedDict):
    details: DataDetailsPaginatorTypeDef
    reference: DataReferenceTypeDef


class DataSummaryTypeDef(TypedDict):
    details: DataDetailsTypeDef
    reference: DataReferenceTypeDef


class CreateMessageTemplateVersionResponseTypeDef(TypedDict):
    messageTemplate: ExtendedMessageTemplateDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetMessageTemplateResponseTypeDef(TypedDict):
    messageTemplate: ExtendedMessageTemplateDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateMessageTemplateResponseTypeDef(TypedDict):
    messageTemplate: MessageTemplateDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMessageTemplateMetadataResponseTypeDef(TypedDict):
    messageTemplate: MessageTemplateDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMessageTemplateResponseTypeDef(TypedDict):
    messageTemplate: MessageTemplateDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateMessageTemplateRequestTypeDef(TypedDict):
    channelSubtype: ChannelSubtypeType
    content: MessageTemplateContentProviderUnionTypeDef
    knowledgeBaseId: str
    name: str
    clientToken: NotRequired[str]
    defaultAttributes: NotRequired[MessageTemplateAttributesUnionTypeDef]
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationUnionTypeDef]
    language: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class UpdateMessageTemplateRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    messageTemplateId: str
    content: NotRequired[MessageTemplateContentProviderUnionTypeDef]
    defaultAttributes: NotRequired[MessageTemplateAttributesUnionTypeDef]
    language: NotRequired[str]


class AssociationConfigurationOutputTypeDef(TypedDict):
    associationConfigurationData: NotRequired[AssociationConfigurationDataOutputTypeDef]
    associationId: NotRequired[str]
    associationType: NotRequired[Literal["KNOWLEDGE_BASE"]]


class AssociationConfigurationTypeDef(TypedDict):
    associationConfigurationData: NotRequired[AssociationConfigurationDataTypeDef]
    associationId: NotRequired[str]
    associationType: NotRequired[Literal["KNOWLEDGE_BASE"]]


class KnowledgeBaseDataTypeDef(TypedDict):
    knowledgeBaseArn: str
    knowledgeBaseId: str
    knowledgeBaseType: KnowledgeBaseTypeType
    name: str
    status: KnowledgeBaseStatusType
    description: NotRequired[str]
    ingestionFailureReasons: NotRequired[List[str]]
    ingestionStatus: NotRequired[SyncStatusType]
    lastContentModificationTime: NotRequired[datetime]
    renderingConfiguration: NotRequired[RenderingConfigurationTypeDef]
    serverSideEncryptionConfiguration: NotRequired[ServerSideEncryptionConfigurationTypeDef]
    sourceConfiguration: NotRequired[SourceConfigurationOutputTypeDef]
    tags: NotRequired[Dict[str, str]]
    vectorIngestionConfiguration: NotRequired[VectorIngestionConfigurationOutputTypeDef]


class KnowledgeBaseSummaryTypeDef(TypedDict):
    knowledgeBaseArn: str
    knowledgeBaseId: str
    knowledgeBaseType: KnowledgeBaseTypeType
    name: str
    status: KnowledgeBaseStatusType
    description: NotRequired[str]
    renderingConfiguration: NotRequired[RenderingConfigurationTypeDef]
    serverSideEncryptionConfiguration: NotRequired[ServerSideEncryptionConfigurationTypeDef]
    sourceConfiguration: NotRequired[SourceConfigurationOutputTypeDef]
    tags: NotRequired[Dict[str, str]]
    vectorIngestionConfiguration: NotRequired[VectorIngestionConfigurationOutputTypeDef]


SourceConfigurationUnionTypeDef = Union[
    SourceConfigurationTypeDef, SourceConfigurationOutputTypeDef
]
ResultDataPaginatorTypeDef = TypedDict(
    "ResultDataPaginatorTypeDef",
    {
        "resultId": str,
        "data": NotRequired[DataSummaryPaginatorTypeDef],
        "document": NotRequired[DocumentTypeDef],
        "relevanceScore": NotRequired[float],
        "type": NotRequired[QueryResultTypeType],
    },
)
RecommendationDataTypeDef = TypedDict(
    "RecommendationDataTypeDef",
    {
        "recommendationId": str,
        "data": NotRequired[DataSummaryTypeDef],
        "document": NotRequired[DocumentTypeDef],
        "relevanceLevel": NotRequired[RelevanceLevelType],
        "relevanceScore": NotRequired[float],
        "type": NotRequired[RecommendationTypeType],
    },
)
ResultDataTypeDef = TypedDict(
    "ResultDataTypeDef",
    {
        "resultId": str,
        "data": NotRequired[DataSummaryTypeDef],
        "document": NotRequired[DocumentTypeDef],
        "relevanceScore": NotRequired[float],
        "type": NotRequired[QueryResultTypeType],
    },
)


class AnswerRecommendationAIAgentConfigurationOutputTypeDef(TypedDict):
    answerGenerationAIGuardrailId: NotRequired[str]
    answerGenerationAIPromptId: NotRequired[str]
    associationConfigurations: NotRequired[List[AssociationConfigurationOutputTypeDef]]
    intentLabelingGenerationAIPromptId: NotRequired[str]
    locale: NotRequired[str]
    queryReformulationAIPromptId: NotRequired[str]


class ManualSearchAIAgentConfigurationOutputTypeDef(TypedDict):
    answerGenerationAIGuardrailId: NotRequired[str]
    answerGenerationAIPromptId: NotRequired[str]
    associationConfigurations: NotRequired[List[AssociationConfigurationOutputTypeDef]]
    locale: NotRequired[str]


class SelfServiceAIAgentConfigurationOutputTypeDef(TypedDict):
    associationConfigurations: NotRequired[List[AssociationConfigurationOutputTypeDef]]
    selfServiceAIGuardrailId: NotRequired[str]
    selfServiceAnswerGenerationAIPromptId: NotRequired[str]
    selfServicePreProcessingAIPromptId: NotRequired[str]


class AnswerRecommendationAIAgentConfigurationTypeDef(TypedDict):
    answerGenerationAIGuardrailId: NotRequired[str]
    answerGenerationAIPromptId: NotRequired[str]
    associationConfigurations: NotRequired[Sequence[AssociationConfigurationTypeDef]]
    intentLabelingGenerationAIPromptId: NotRequired[str]
    locale: NotRequired[str]
    queryReformulationAIPromptId: NotRequired[str]


class ManualSearchAIAgentConfigurationTypeDef(TypedDict):
    answerGenerationAIGuardrailId: NotRequired[str]
    answerGenerationAIPromptId: NotRequired[str]
    associationConfigurations: NotRequired[Sequence[AssociationConfigurationTypeDef]]
    locale: NotRequired[str]


class SelfServiceAIAgentConfigurationTypeDef(TypedDict):
    associationConfigurations: NotRequired[Sequence[AssociationConfigurationTypeDef]]
    selfServiceAIGuardrailId: NotRequired[str]
    selfServiceAnswerGenerationAIPromptId: NotRequired[str]
    selfServicePreProcessingAIPromptId: NotRequired[str]


class CreateKnowledgeBaseResponseTypeDef(TypedDict):
    knowledgeBase: KnowledgeBaseDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetKnowledgeBaseResponseTypeDef(TypedDict):
    knowledgeBase: KnowledgeBaseDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateKnowledgeBaseTemplateUriResponseTypeDef(TypedDict):
    knowledgeBase: KnowledgeBaseDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListKnowledgeBasesResponseTypeDef(TypedDict):
    knowledgeBaseSummaries: List[KnowledgeBaseSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateKnowledgeBaseRequestTypeDef(TypedDict):
    knowledgeBaseType: KnowledgeBaseTypeType
    name: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    renderingConfiguration: NotRequired[RenderingConfigurationTypeDef]
    serverSideEncryptionConfiguration: NotRequired[ServerSideEncryptionConfigurationTypeDef]
    sourceConfiguration: NotRequired[SourceConfigurationUnionTypeDef]
    tags: NotRequired[Mapping[str, str]]
    vectorIngestionConfiguration: NotRequired[VectorIngestionConfigurationUnionTypeDef]


class QueryAssistantResponsePaginatorTypeDef(TypedDict):
    results: List[ResultDataPaginatorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetRecommendationsResponseTypeDef(TypedDict):
    recommendations: List[RecommendationDataTypeDef]
    triggers: List[RecommendationTriggerTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class QueryAssistantResponseTypeDef(TypedDict):
    results: List[ResultDataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class AIAgentConfigurationOutputTypeDef(TypedDict):
    answerRecommendationAIAgentConfiguration: NotRequired[
        AnswerRecommendationAIAgentConfigurationOutputTypeDef
    ]
    manualSearchAIAgentConfiguration: NotRequired[ManualSearchAIAgentConfigurationOutputTypeDef]
    selfServiceAIAgentConfiguration: NotRequired[SelfServiceAIAgentConfigurationOutputTypeDef]


class AIAgentConfigurationTypeDef(TypedDict):
    answerRecommendationAIAgentConfiguration: NotRequired[
        AnswerRecommendationAIAgentConfigurationTypeDef
    ]
    manualSearchAIAgentConfiguration: NotRequired[ManualSearchAIAgentConfigurationTypeDef]
    selfServiceAIAgentConfiguration: NotRequired[SelfServiceAIAgentConfigurationTypeDef]


AIAgentDataTypeDef = TypedDict(
    "AIAgentDataTypeDef",
    {
        "aiAgentArn": str,
        "aiAgentId": str,
        "assistantArn": str,
        "assistantId": str,
        "configuration": AIAgentConfigurationOutputTypeDef,
        "name": str,
        "type": AIAgentTypeType,
        "visibilityStatus": VisibilityStatusType,
        "description": NotRequired[str],
        "modifiedTime": NotRequired[datetime],
        "origin": NotRequired[OriginType],
        "status": NotRequired[StatusType],
        "tags": NotRequired[Dict[str, str]],
    },
)
AIAgentSummaryTypeDef = TypedDict(
    "AIAgentSummaryTypeDef",
    {
        "aiAgentArn": str,
        "aiAgentId": str,
        "assistantArn": str,
        "assistantId": str,
        "name": str,
        "type": AIAgentTypeType,
        "visibilityStatus": VisibilityStatusType,
        "configuration": NotRequired[AIAgentConfigurationOutputTypeDef],
        "description": NotRequired[str],
        "modifiedTime": NotRequired[datetime],
        "origin": NotRequired[OriginType],
        "status": NotRequired[StatusType],
        "tags": NotRequired[Dict[str, str]],
    },
)
AIAgentConfigurationUnionTypeDef = Union[
    AIAgentConfigurationTypeDef, AIAgentConfigurationOutputTypeDef
]


class CreateAIAgentResponseTypeDef(TypedDict):
    aiAgent: AIAgentDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAIAgentVersionResponseTypeDef(TypedDict):
    aiAgent: AIAgentDataTypeDef
    versionNumber: int
    ResponseMetadata: ResponseMetadataTypeDef


class GetAIAgentResponseTypeDef(TypedDict):
    aiAgent: AIAgentDataTypeDef
    versionNumber: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAIAgentResponseTypeDef(TypedDict):
    aiAgent: AIAgentDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AIAgentVersionSummaryTypeDef(TypedDict):
    aiAgentSummary: NotRequired[AIAgentSummaryTypeDef]
    versionNumber: NotRequired[int]


class ListAIAgentsResponseTypeDef(TypedDict):
    aiAgentSummaries: List[AIAgentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


CreateAIAgentRequestTypeDef = TypedDict(
    "CreateAIAgentRequestTypeDef",
    {
        "assistantId": str,
        "configuration": AIAgentConfigurationUnionTypeDef,
        "name": str,
        "type": AIAgentTypeType,
        "visibilityStatus": VisibilityStatusType,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)


class UpdateAIAgentRequestTypeDef(TypedDict):
    aiAgentId: str
    assistantId: str
    visibilityStatus: VisibilityStatusType
    clientToken: NotRequired[str]
    configuration: NotRequired[AIAgentConfigurationUnionTypeDef]
    description: NotRequired[str]


class ListAIAgentVersionsResponseTypeDef(TypedDict):
    aiAgentVersionSummaries: List[AIAgentVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
