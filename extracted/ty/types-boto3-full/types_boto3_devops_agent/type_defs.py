"""
Type annotations for devops-agent service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devops_agent/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_devops_agent.type_defs import AWSConfigurationTypeDef

    data: AWSConfigurationTypeDef = ...
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
    ApprovalActionTypeType,
    ApprovalStatusType,
    AuthFlowType,
    CapabilityTypeType,
    ExecutionStatusType,
    GithubRepoOwnerTypeType,
    GitLabTokenTypeType,
    GoalStatusType,
    GoalTypeType,
    IpAddressTypeType,
    MCPServerAuthorizationMethodType,
    NewRelicRegionType,
    OrderTypeType,
    PostRegisterServiceSupportedServiceType,
    PriorityType,
    PrivateConnectionStatusType,
    PrivateConnectionTypeType,
    RecommendationPriorityType,
    RecommendationStatusType,
    RemoteAgentAuthorizationMethodType,
    ResourceConfigDnsResolutionType,
    SchedulerStateType,
    ServiceType,
    TaskSortFieldType,
    TaskSortOrderType,
    TaskStatusType,
    TaskTypeType,
    ToolClassificationType,
    UserTypeType,
    ValidationStatusType,
    WebhookTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AWSConfigurationTypeDef",
    "AdditionalServiceDetailsTypeDef",
    "AdditionalServiceRegistrationStepTypeDef",
    "AgentSpaceTypeDef",
    "ApprovalActionTypeDef",
    "ApprovalPatternTypeDef",
    "AssetContentTypeDef",
    "AssetFileBodyOutputTypeDef",
    "AssetFileBodyTypeDef",
    "AssetFileBodyUnionTypeDef",
    "AssetFileContentTypeDef",
    "AssetFileSummaryTypeDef",
    "AssetFileTypeDef",
    "AssetSourceUrlContentTypeDef",
    "AssetTypeDef",
    "AssetTypeSummaryTypeDef",
    "AssetVersionMetadataTypeDef",
    "AssetZipContentOutputTypeDef",
    "AssetZipContentTypeDef",
    "AssetZipContentUnionTypeDef",
    "AssistantMessageBlockTypeDef",
    "AssociateServiceInputTypeDef",
    "AssociateServiceOutputTypeDef",
    "AssociationTypeDef",
    "AzureConfigurationTypeDef",
    "AzureDevOpsConfigurationTypeDef",
    "BlobTypeDef",
    "CapabilityConfigurationTypeDef",
    "ChatExecutionTypeDef",
    "CreateAgentSpaceInputTypeDef",
    "CreateAgentSpaceOutputTypeDef",
    "CreateAssetFileRequestTypeDef",
    "CreateAssetFileResponseTypeDef",
    "CreateAssetRequestTypeDef",
    "CreateAssetResponseTypeDef",
    "CreateBacklogTaskRequestTypeDef",
    "CreateBacklogTaskResponseTypeDef",
    "CreateChatRequestTypeDef",
    "CreateChatResponseTypeDef",
    "CreatePrivateConnectionInputTypeDef",
    "CreatePrivateConnectionOutputTypeDef",
    "CreateTriggerRequestTypeDef",
    "CreateTriggerResponseTypeDef",
    "DatadogAuthorizationConfigTypeDef",
    "DatadogServiceDetailsTypeDef",
    "DeleteAgentSpaceInputTypeDef",
    "DeleteAssetFileRequestTypeDef",
    "DeleteAssetRequestTypeDef",
    "DeletePrivateConnectionInputTypeDef",
    "DeletePrivateConnectionOutputTypeDef",
    "DeleteTriggerRequestTypeDef",
    "DeregisterServiceInputTypeDef",
    "DescribePrivateConnectionInputTypeDef",
    "DescribePrivateConnectionOutputTypeDef",
    "DisableOperatorAppInputTypeDef",
    "DisassociateServiceInputTypeDef",
    "DynatraceConfigurationOutputTypeDef",
    "DynatraceConfigurationTypeDef",
    "DynatraceOAuthClientCredentialsConfigTypeDef",
    "DynatraceServiceAuthorizationConfigTypeDef",
    "DynatraceServiceDetailsTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnableOperatorAppInputTypeDef",
    "EnableOperatorAppOutputTypeDef",
    "EventChannelDetailsTypeDef",
    "ExecutionTypeDef",
    "GenericWebhookTypeDef",
    "GetAccountUsageOutputTypeDef",
    "GetAgentSpaceInputTypeDef",
    "GetAgentSpaceOutputTypeDef",
    "GetAssetContentRequestTypeDef",
    "GetAssetContentResponseTypeDef",
    "GetAssetFileRequestTypeDef",
    "GetAssetFileResponseTypeDef",
    "GetAssetRequestTypeDef",
    "GetAssetResponseTypeDef",
    "GetAssociationInputTypeDef",
    "GetAssociationOutputTypeDef",
    "GetBacklogTaskRequestTypeDef",
    "GetBacklogTaskResponseTypeDef",
    "GetOperatorAppInputTypeDef",
    "GetOperatorAppOutputTypeDef",
    "GetRecommendationRequestTypeDef",
    "GetRecommendationResponseTypeDef",
    "GetServiceInputTypeDef",
    "GetServiceOutputTypeDef",
    "GetTriggerRequestTypeDef",
    "GetTriggerResponseTypeDef",
    "GitHubConfigurationTypeDef",
    "GitLabConfigurationTypeDef",
    "GitLabDetailsTypeDef",
    "GoalContentTypeDef",
    "GoalScheduleInputTypeDef",
    "GoalScheduleTypeDef",
    "GoalTypeDef",
    "GrafanaServiceDetailsTypeDef",
    "IamAuthConfigurationTypeDef",
    "IdcAuthConfigurationTypeDef",
    "IdpAuthConfigurationTypeDef",
    "JournalRecordTypeDef",
    "ListAgentSpacesInputPaginateTypeDef",
    "ListAgentSpacesInputTypeDef",
    "ListAgentSpacesOutputTypeDef",
    "ListAssetFilesRequestPaginateTypeDef",
    "ListAssetFilesRequestTypeDef",
    "ListAssetFilesResponseTypeDef",
    "ListAssetTypesRequestPaginateTypeDef",
    "ListAssetTypesRequestTypeDef",
    "ListAssetTypesResponseTypeDef",
    "ListAssetVersionsRequestPaginateTypeDef",
    "ListAssetVersionsRequestTypeDef",
    "ListAssetVersionsResponseTypeDef",
    "ListAssetsRequestPaginateTypeDef",
    "ListAssetsRequestTypeDef",
    "ListAssetsResponseTypeDef",
    "ListAssociationsInputPaginateTypeDef",
    "ListAssociationsInputTypeDef",
    "ListAssociationsOutputTypeDef",
    "ListBacklogTasksRequestPaginateTypeDef",
    "ListBacklogTasksRequestTypeDef",
    "ListBacklogTasksResponseTypeDef",
    "ListChatsRequestTypeDef",
    "ListChatsResponseTypeDef",
    "ListExecutionsRequestPaginateTypeDef",
    "ListExecutionsRequestTypeDef",
    "ListExecutionsResponseTypeDef",
    "ListGoalsRequestPaginateTypeDef",
    "ListGoalsRequestTypeDef",
    "ListGoalsResponseTypeDef",
    "ListJournalRecordsRequestPaginateTypeDef",
    "ListJournalRecordsRequestTypeDef",
    "ListJournalRecordsResponseTypeDef",
    "ListPendingMessagesRequestTypeDef",
    "ListPendingMessagesResponseTypeDef",
    "ListPrivateConnectionsOutputTypeDef",
    "ListRecommendationsRequestTypeDef",
    "ListRecommendationsResponseTypeDef",
    "ListServicesInputPaginateTypeDef",
    "ListServicesInputTypeDef",
    "ListServicesOutputTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTriggersRequestPaginateTypeDef",
    "ListTriggersRequestTypeDef",
    "ListTriggersResponseTypeDef",
    "ListWebhooksInputTypeDef",
    "ListWebhooksOutputTypeDef",
    "MCPServerAPIKeyConfigTypeDef",
    "MCPServerAuthorizationConfigTypeDef",
    "MCPServerAuthorizationDiscoveryConfigTypeDef",
    "MCPServerBearerTokenConfigTypeDef",
    "MCPServerConfigurationOutputTypeDef",
    "MCPServerConfigurationTypeDef",
    "MCPServerDatadogConfigurationOutputTypeDef",
    "MCPServerDatadogConfigurationTypeDef",
    "MCPServerDetailsTypeDef",
    "MCPServerGrafanaConfigurationOutputTypeDef",
    "MCPServerGrafanaConfigurationTypeDef",
    "MCPServerNewRelicConfigurationTypeDef",
    "MCPServerOAuth3LOConfigTypeDef",
    "MCPServerOAuthClientCredentialsConfigTypeDef",
    "MCPServerSigV4AuthorizationConfigTypeDef",
    "MCPServerSigV4ConfigurationOutputTypeDef",
    "MCPServerSigV4ConfigurationTypeDef",
    "MCPServerSigV4ServiceDetailsTypeDef",
    "MCPToolDetailTypeDef",
    "MessageTypeDef",
    "NewRelicApiKeyConfigTypeDef",
    "NewRelicServiceAuthorizationConfigTypeDef",
    "NewRelicServiceDetailsTypeDef",
    "OAuthAdditionalStepDetailsTypeDef",
    "PagerDutyAuthorizationConfigTypeDef",
    "PagerDutyConfigurationOutputTypeDef",
    "PagerDutyConfigurationTypeDef",
    "PagerDutyDetailsTypeDef",
    "PagerDutyOAuthClientCredentialsConfigTypeDef",
    "PaginatorConfigTypeDef",
    "PendingMessageTypeDef",
    "PrivateConnectionModeTypeDef",
    "PrivateConnectionSummaryTypeDef",
    "RecommendationContentTypeDef",
    "RecommendationTypeDef",
    "ReferenceInputTypeDef",
    "ReferenceOutputTypeDef",
    "RegisterServiceInputTypeDef",
    "RegisterServiceOutputTypeDef",
    "RegisteredAzureDevOpsServiceDetailsTypeDef",
    "RegisteredAzureIdentityDetailsOutputTypeDef",
    "RegisteredAzureIdentityDetailsTypeDef",
    "RegisteredAzureIdentityDetailsUnionTypeDef",
    "RegisteredGitLabServiceDetailsTypeDef",
    "RegisteredGithubServiceDetailsTypeDef",
    "RegisteredGrafanaServerDetailsTypeDef",
    "RegisteredMCPServerDetailsTypeDef",
    "RegisteredMCPServerSigV4DetailsTypeDef",
    "RegisteredNewRelicDetailsTypeDef",
    "RegisteredPagerDutyDetailsTypeDef",
    "RegisteredRemoteAgentDetailsTypeDef",
    "RegisteredRemoteAgentSigV4DetailsTypeDef",
    "RegisteredServiceNowDetailsTypeDef",
    "RegisteredServiceTypeDef",
    "RegisteredSlackServiceDetailsTypeDef",
    "RemoteAgentAPIKeyConfigTypeDef",
    "RemoteAgentAuthorizationConfigTypeDef",
    "RemoteAgentBearerTokenConfigTypeDef",
    "RemoteAgentOAuthClientCredentialsConfigTypeDef",
    "RemoteAgentServiceDetailsTypeDef",
    "RemoteAgentSigV4AuthorizationConfigTypeDef",
    "RemoteAgentSigV4ServiceDetailsTypeDef",
    "ResponseMetadataTypeDef",
    "ScheduleConditionTypeDef",
    "SelfManagedInputTypeDef",
    "SendMessageContentBlockDeltaEventTypeDef",
    "SendMessageContentBlockDeltaTypeDef",
    "SendMessageContentBlockStartEventTypeDef",
    "SendMessageContentBlockStopEventTypeDef",
    "SendMessageContextTypeDef",
    "SendMessageEventsTypeDef",
    "SendMessageJsonDeltaTypeDef",
    "SendMessageRequestTypeDef",
    "SendMessageResponseCompletedEventTypeDef",
    "SendMessageResponseCreatedEventTypeDef",
    "SendMessageResponseFailedEventTypeDef",
    "SendMessageResponseInProgressEventTypeDef",
    "SendMessageResponseTypeDef",
    "SendMessageSummaryEventTypeDef",
    "SendMessageTextDeltaTypeDef",
    "SendMessageUsageInfoTypeDef",
    "ServiceConfigurationOutputTypeDef",
    "ServiceConfigurationTypeDef",
    "ServiceConfigurationUnionTypeDef",
    "ServiceDetailsTypeDef",
    "ServiceManagedInputTypeDef",
    "ServiceNowConfigurationOutputTypeDef",
    "ServiceNowConfigurationTypeDef",
    "ServiceNowOAuthClientCredentialsConfigTypeDef",
    "ServiceNowServiceAuthorizationConfigTypeDef",
    "ServiceNowServiceDetailsTypeDef",
    "SlackChannelTypeDef",
    "SlackConfigurationTypeDef",
    "SlackTransmissionTargetTypeDef",
    "SourceAwsConfigurationTypeDef",
    "TagResourceRequestTypeDef",
    "TaskFilterTypeDef",
    "TaskTypeDef",
    "TimestampTypeDef",
    "TriggerConditionTypeDef",
    "TriggerTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateAgentSpaceInputTypeDef",
    "UpdateAgentSpaceOutputTypeDef",
    "UpdateApprovalActionRequestTypeDef",
    "UpdateApprovalActionResponseTypeDef",
    "UpdateAssetFileRequestTypeDef",
    "UpdateAssetFileResponseTypeDef",
    "UpdateAssetRequestTypeDef",
    "UpdateAssetResponseTypeDef",
    "UpdateAssociationInputTypeDef",
    "UpdateAssociationOutputTypeDef",
    "UpdateBacklogTaskRequestTypeDef",
    "UpdateBacklogTaskResponseTypeDef",
    "UpdateGoalRequestTypeDef",
    "UpdateGoalResponseTypeDef",
    "UpdateOperatorAppIdpConfigInputTypeDef",
    "UpdateOperatorAppIdpConfigOutputTypeDef",
    "UpdatePrivateConnectionCertificateInputTypeDef",
    "UpdatePrivateConnectionCertificateOutputTypeDef",
    "UpdateRecommendationRequestTypeDef",
    "UpdateRecommendationResponseTypeDef",
    "UpdateTriggerRequestTypeDef",
    "UpdateTriggerResponseTypeDef",
    "UsageMetricTypeDef",
    "UserMessageBlockTypeDef",
    "UserReferenceTypeDef",
    "ValidateAwsAssociationsInputTypeDef",
    "WebhookTypeDef",
)


class AWSConfigurationTypeDef(TypedDict):
    assumableRoleArn: str
    accountId: str
    accountType: Literal["monitor"]
    agentElevatedRoleArn: NotRequired[str]
    agentElevatedRoleArnStatus: NotRequired[ValidationStatusType]


class RegisteredAzureDevOpsServiceDetailsTypeDef(TypedDict):
    organizationName: str


class RegisteredAzureIdentityDetailsOutputTypeDef(TypedDict):
    tenantId: str
    clientId: str
    webIdentityRoleArn: str
    webIdentityTokenAudiences: list[str]


class RegisteredGitLabServiceDetailsTypeDef(TypedDict):
    targetUrl: str
    tokenType: GitLabTokenTypeType
    groupId: NotRequired[str]


class RegisteredGithubServiceDetailsTypeDef(TypedDict):
    owner: str
    ownerType: GithubRepoOwnerTypeType
    targetUrl: NotRequired[str]


class RegisteredGrafanaServerDetailsTypeDef(TypedDict):
    endpoint: str
    authorizationMethod: MCPServerAuthorizationMethodType


class RegisteredMCPServerDetailsTypeDef(TypedDict):
    name: str
    endpoint: str
    authorizationMethod: MCPServerAuthorizationMethodType
    description: NotRequired[str]
    apiKeyHeader: NotRequired[str]


class RegisteredMCPServerSigV4DetailsTypeDef(TypedDict):
    name: str
    endpoint: str
    region: str
    service: str
    roleArn: str
    description: NotRequired[str]
    mcpRoleArn: NotRequired[str]
    customHeaders: NotRequired[dict[str, str]]


class RegisteredNewRelicDetailsTypeDef(TypedDict):
    accountId: str
    region: NewRelicRegionType
    description: NotRequired[str]


class RegisteredPagerDutyDetailsTypeDef(TypedDict):
    scopes: list[str]


class RegisteredRemoteAgentDetailsTypeDef(TypedDict):
    name: str
    endpoint: str
    authorizationMethod: RemoteAgentAuthorizationMethodType
    description: NotRequired[str]
    apiKeyHeader: NotRequired[str]


class RegisteredRemoteAgentSigV4DetailsTypeDef(TypedDict):
    name: str
    endpoint: str
    region: str
    service: str
    description: NotRequired[str]
    roleArn: NotRequired[str]


class RegisteredServiceNowDetailsTypeDef(TypedDict):
    instanceUrl: NotRequired[str]


class RegisteredSlackServiceDetailsTypeDef(TypedDict):
    teamId: str
    teamName: str


class OAuthAdditionalStepDetailsTypeDef(TypedDict):
    authorizationUrl: str


class AgentSpaceTypeDef(TypedDict):
    name: str
    createdAt: datetime
    updatedAt: datetime
    agentSpaceId: str
    description: NotRequired[str]
    locale: NotRequired[str]
    kmsKeyArn: NotRequired[str]
    preferences: NotRequired[dict[Literal["elevatedActionsEnabled"], bool]]


class ApprovalActionTypeDef(TypedDict):
    toolUseId: NotRequired[str]
    interruptId: NotRequired[str]
    approvalId: NotRequired[str]
    buttonText: NotRequired[str]
    action: NotRequired[ApprovalActionTypeType]


class ApprovalPatternTypeDef(TypedDict):
    tool: str
    argumentPins: Mapping[str, str]


class AssetSourceUrlContentTypeDef(TypedDict):
    url: str


AssetFileBodyOutputTypeDef = TypedDict(
    "AssetFileBodyOutputTypeDef",
    {
        "bytes": NotRequired[bytes],
        "text": NotRequired[str],
    },
)
BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class AssetFileSummaryTypeDef(TypedDict):
    path: str
    version: int
    createdAt: datetime
    updatedAt: datetime
    metadata: NotRequired[dict[str, Any]]


class AssetTypeDef(TypedDict):
    assetId: str
    assetType: str
    metadata: dict[str, Any]
    version: int
    createdAt: datetime
    updatedAt: datetime


class AssetTypeSummaryTypeDef(TypedDict):
    assetType: str
    description: str


class AssetVersionMetadataTypeDef(TypedDict):
    version: int
    createdAt: datetime
    updatedAt: datetime


class AssetZipContentOutputTypeDef(TypedDict):
    zipFile: bytes


class AssistantMessageBlockTypeDef(TypedDict):
    text: NotRequired[str]
    toolUse: NotRequired[dict[str, Any]]


class CapabilityConfigurationTypeDef(TypedDict):
    enabled: NotRequired[bool]


class GenericWebhookTypeDef(TypedDict):
    webhookUrl: NotRequired[str]
    webhookId: NotRequired[str]
    webhookType: NotRequired[WebhookTypeType]
    webhookSecret: NotRequired[str]
    apiKey: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AzureConfigurationTypeDef(TypedDict):
    subscriptionId: str


class AzureDevOpsConfigurationTypeDef(TypedDict):
    organizationName: str
    projectId: str
    projectName: str


class ChatExecutionTypeDef(TypedDict):
    executionId: str
    createdAt: datetime
    updatedAt: NotRequired[datetime]
    summary: NotRequired[str]


class CreateAgentSpaceInputTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    locale: NotRequired[str]
    kmsKeyArn: NotRequired[str]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    preferences: NotRequired[Mapping[Literal["elevatedActionsEnabled"], bool]]


class ReferenceInputTypeDef(TypedDict):
    system: str
    referenceId: str
    referenceUrl: str
    associationId: str
    title: NotRequired[str]


class CreateChatRequestTypeDef(TypedDict):
    agentSpaceId: str
    userId: NotRequired[str]
    userType: NotRequired[UserTypeType]


class MCPServerAuthorizationDiscoveryConfigTypeDef(TypedDict):
    returnToEndpoint: str


class DeleteAgentSpaceInputTypeDef(TypedDict):
    agentSpaceId: str


class DeleteAssetFileRequestTypeDef(TypedDict):
    agentSpaceId: str
    assetId: str
    path: str


class DeleteAssetRequestTypeDef(TypedDict):
    agentSpaceId: str
    assetId: str


class DeletePrivateConnectionInputTypeDef(TypedDict):
    name: str


class DeleteTriggerRequestTypeDef(TypedDict):
    agentSpaceId: str
    triggerId: str


class DeregisterServiceInputTypeDef(TypedDict):
    serviceId: str


class DescribePrivateConnectionInputTypeDef(TypedDict):
    name: str


class DisableOperatorAppInputTypeDef(TypedDict):
    agentSpaceId: str
    authFlow: NotRequired[AuthFlowType]


class DisassociateServiceInputTypeDef(TypedDict):
    agentSpaceId: str
    associationId: str


class DynatraceConfigurationOutputTypeDef(TypedDict):
    envId: str
    resources: NotRequired[list[str]]


class DynatraceConfigurationTypeDef(TypedDict):
    envId: str
    resources: NotRequired[Sequence[str]]


class DynatraceOAuthClientCredentialsConfigTypeDef(TypedDict):
    clientId: str
    clientSecret: str
    clientName: NotRequired[str]
    exchangeParameters: NotRequired[Mapping[str, str]]


class EnableOperatorAppInputTypeDef(TypedDict):
    agentSpaceId: str
    authFlow: AuthFlowType
    operatorAppRoleArn: str
    idcInstanceArn: NotRequired[str]
    issuerUrl: NotRequired[str]
    idpClientId: NotRequired[str]
    idpClientSecret: NotRequired[str]
    provider: NotRequired[str]


class IamAuthConfigurationTypeDef(TypedDict):
    operatorAppRoleArn: str
    createdAt: datetime
    updatedAt: NotRequired[datetime]


class IdcAuthConfigurationTypeDef(TypedDict):
    operatorAppRoleArn: str
    idcInstanceArn: str
    createdAt: datetime
    idcApplicationArn: NotRequired[str]
    updatedAt: NotRequired[datetime]


class IdpAuthConfigurationTypeDef(TypedDict):
    issuerUrl: str
    clientId: str
    operatorAppRoleArn: str
    provider: str
    createdAt: datetime
    updatedAt: NotRequired[datetime]


EventChannelDetailsTypeDef = TypedDict(
    "EventChannelDetailsTypeDef",
    {
        "type": NotRequired[Literal["webhook"]],
    },
)


class ExecutionTypeDef(TypedDict):
    agentSpaceId: str
    executionId: str
    agentSubTask: str
    createdAt: datetime
    updatedAt: datetime
    executionStatus: ExecutionStatusType
    parentExecutionId: NotRequired[str]
    agentType: NotRequired[str]
    uid: NotRequired[str]


class UsageMetricTypeDef(TypedDict):
    limit: int
    usage: float


class GetAgentSpaceInputTypeDef(TypedDict):
    agentSpaceId: str


class GetAssetContentRequestTypeDef(TypedDict):
    agentSpaceId: str
    assetId: str
    assetVersion: NotRequired[int]


class GetAssetFileRequestTypeDef(TypedDict):
    agentSpaceId: str
    assetId: str
    path: str
    assetVersion: NotRequired[int]


class GetAssetRequestTypeDef(TypedDict):
    agentSpaceId: str
    assetId: str
    assetVersion: NotRequired[int]


class GetAssociationInputTypeDef(TypedDict):
    agentSpaceId: str
    associationId: str


class GetBacklogTaskRequestTypeDef(TypedDict):
    agentSpaceId: str
    taskId: str


class GetOperatorAppInputTypeDef(TypedDict):
    agentSpaceId: str


class GetRecommendationRequestTypeDef(TypedDict):
    agentSpaceId: str
    recommendationId: str
    recommendationVersion: NotRequired[int]


class GetServiceInputTypeDef(TypedDict):
    serviceId: str


class GetTriggerRequestTypeDef(TypedDict):
    agentSpaceId: str
    triggerId: str


class GitHubConfigurationTypeDef(TypedDict):
    repoName: str
    repoId: str
    owner: str
    ownerType: GithubRepoOwnerTypeType
    instanceIdentifier: NotRequired[str]
    runtimeRoleArn: NotRequired[str]


class GitLabConfigurationTypeDef(TypedDict):
    projectId: str
    projectPath: str
    instanceIdentifier: NotRequired[str]
    runtimeRoleArn: NotRequired[str]


class GitLabDetailsTypeDef(TypedDict):
    targetUrl: str
    tokenType: GitLabTokenTypeType
    tokenValue: str
    groupId: NotRequired[str]


class GoalContentTypeDef(TypedDict):
    description: str
    objectives: str


class GoalScheduleInputTypeDef(TypedDict):
    state: SchedulerStateType


class GoalScheduleTypeDef(TypedDict):
    state: SchedulerStateType
    expression: NotRequired[str]


class UserReferenceTypeDef(TypedDict):
    userId: str
    userType: UserTypeType


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListAgentSpacesInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListAssetFilesRequestTypeDef(TypedDict):
    agentSpaceId: str
    assetId: str
    assetVersion: NotRequired[int]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListAssetTypesRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListAssetVersionsRequestTypeDef(TypedDict):
    agentSpaceId: str
    assetId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class ListAssociationsInputTypeDef(TypedDict):
    agentSpaceId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    filterServiceTypes: NotRequired[str]


class ListChatsRequestTypeDef(TypedDict):
    agentSpaceId: str
    userId: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListExecutionsRequestTypeDef(TypedDict):
    agentSpaceId: str
    taskId: str
    limit: NotRequired[int]
    nextToken: NotRequired[str]


class ListGoalsRequestTypeDef(TypedDict):
    agentSpaceId: str
    status: NotRequired[GoalStatusType]
    goalType: NotRequired[GoalTypeType]
    limit: NotRequired[int]
    nextToken: NotRequired[str]


class ListJournalRecordsRequestTypeDef(TypedDict):
    agentSpaceId: str
    executionId: str
    limit: NotRequired[int]
    nextToken: NotRequired[str]
    recordType: NotRequired[str]
    order: NotRequired[OrderTypeType]


class ListPendingMessagesRequestTypeDef(TypedDict):
    agentSpaceId: str
    executionId: str


PrivateConnectionSummaryTypeDef = TypedDict(
    "PrivateConnectionSummaryTypeDef",
    {
        "name": str,
        "type": PrivateConnectionTypeType,
        "status": PrivateConnectionStatusType,
        "resourceGatewayId": NotRequired[str],
        "hostAddress": NotRequired[str],
        "vpcId": NotRequired[str],
        "resourceConfigurationId": NotRequired[str],
        "certificateExpiryTime": NotRequired[datetime],
        "dnsResolution": NotRequired[ResourceConfigDnsResolutionType],
        "failureMessage": NotRequired[str],
    },
)


class ListRecommendationsRequestTypeDef(TypedDict):
    agentSpaceId: str
    taskId: NotRequired[str]
    goalId: NotRequired[str]
    status: NotRequired[RecommendationStatusType]
    priority: NotRequired[RecommendationPriorityType]
    limit: NotRequired[int]
    nextToken: NotRequired[str]


class ListServicesInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    filterServiceType: NotRequired[ServiceType]


class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str


class ListTriggersRequestTypeDef(TypedDict):
    agentSpaceId: str
    status: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListWebhooksInputTypeDef(TypedDict):
    agentSpaceId: str
    associationId: str


class WebhookTypeDef(TypedDict):
    webhookUrl: str
    webhookId: str
    webhookType: NotRequired[WebhookTypeType]


class MCPServerAPIKeyConfigTypeDef(TypedDict):
    apiKeyName: str
    apiKeyValue: str
    apiKeyHeader: str


class MCPServerBearerTokenConfigTypeDef(TypedDict):
    tokenName: str
    tokenValue: str
    authorizationHeader: NotRequired[str]


class MCPServerOAuth3LOConfigTypeDef(TypedDict):
    clientId: str
    returnToEndpoint: str
    authorizationUrl: str
    exchangeUrl: str
    clientName: NotRequired[str]
    exchangeParameters: NotRequired[Mapping[str, str]]
    clientSecret: NotRequired[str]
    supportCodeChallenge: NotRequired[bool]
    scopes: NotRequired[Sequence[str]]


class MCPServerOAuthClientCredentialsConfigTypeDef(TypedDict):
    clientId: str
    clientSecret: str
    exchangeUrl: str
    clientName: NotRequired[str]
    exchangeParameters: NotRequired[Mapping[str, str]]
    scopes: NotRequired[Sequence[str]]


class MCPToolDetailTypeDef(TypedDict):
    name: str
    toolClassification: NotRequired[ToolClassificationType]


class MCPServerNewRelicConfigurationTypeDef(TypedDict):
    accountId: str
    endpoint: str


class MCPServerSigV4AuthorizationConfigTypeDef(TypedDict):
    region: str
    service: str
    roleArn: NotRequired[str]
    mcpRoleArn: NotRequired[str]
    customHeaders: NotRequired[Mapping[str, str]]


class UserMessageBlockTypeDef(TypedDict):
    text: NotRequired[str]
    toolResult: NotRequired[dict[str, Any]]


class NewRelicApiKeyConfigTypeDef(TypedDict):
    apiKey: str
    accountId: str
    region: NewRelicRegionType
    applicationIds: NotRequired[Sequence[str]]
    entityGuids: NotRequired[Sequence[str]]
    alertPolicyIds: NotRequired[Sequence[str]]


class PagerDutyOAuthClientCredentialsConfigTypeDef(TypedDict):
    clientId: str
    clientSecret: str
    clientName: NotRequired[str]
    exchangeParameters: NotRequired[Mapping[str, str]]


class PagerDutyConfigurationOutputTypeDef(TypedDict):
    services: list[str]
    customerEmail: str


class PagerDutyConfigurationTypeDef(TypedDict):
    services: Sequence[str]
    customerEmail: str


class SelfManagedInputTypeDef(TypedDict):
    resourceConfigurationId: str
    certificate: NotRequired[str]


class ServiceManagedInputTypeDef(TypedDict):
    hostAddress: str
    vpcId: str
    subnetIds: Sequence[str]
    securityGroupIds: NotRequired[Sequence[str]]
    ipAddressType: NotRequired[IpAddressTypeType]
    ipv4AddressesPerEni: NotRequired[int]
    portRanges: NotRequired[Sequence[str]]
    certificate: NotRequired[str]
    dnsResolution: NotRequired[ResourceConfigDnsResolutionType]


class RecommendationContentTypeDef(TypedDict):
    summary: str
    spec: NotRequired[str]


class ReferenceOutputTypeDef(TypedDict):
    system: str
    referenceId: str
    referenceUrl: str
    associationId: str
    title: NotRequired[str]


class RegisteredAzureIdentityDetailsTypeDef(TypedDict):
    tenantId: str
    clientId: str
    webIdentityRoleArn: str
    webIdentityTokenAudiences: Sequence[str]


class RemoteAgentAPIKeyConfigTypeDef(TypedDict):
    apiKeyName: str
    apiKeyValue: str
    apiKeyHeader: str


class RemoteAgentBearerTokenConfigTypeDef(TypedDict):
    tokenName: str
    tokenValue: str
    authorizationHeader: NotRequired[str]


class RemoteAgentOAuthClientCredentialsConfigTypeDef(TypedDict):
    clientId: str
    clientSecret: str
    exchangeUrl: str
    clientName: NotRequired[str]
    exchangeParameters: NotRequired[Mapping[str, str]]
    scopes: NotRequired[Sequence[str]]


class RemoteAgentSigV4AuthorizationConfigTypeDef(TypedDict):
    region: str
    service: str
    roleArn: NotRequired[str]


class ScheduleConditionTypeDef(TypedDict):
    expression: str


class SendMessageJsonDeltaTypeDef(TypedDict):
    partialJson: NotRequired[str]


class SendMessageTextDeltaTypeDef(TypedDict):
    text: NotRequired[str]


SendMessageContentBlockStartEventTypeDef = TypedDict(
    "SendMessageContentBlockStartEventTypeDef",
    {
        "index": NotRequired[int],
        "type": NotRequired[str],
        "id": NotRequired[str],
        "parentId": NotRequired[str],
        "sequenceNumber": NotRequired[int],
    },
)
SendMessageContentBlockStopEventTypeDef = TypedDict(
    "SendMessageContentBlockStopEventTypeDef",
    {
        "index": NotRequired[int],
        "type": NotRequired[str],
        "text": NotRequired[str],
        "last": NotRequired[bool],
        "sequenceNumber": NotRequired[int],
    },
)


class SendMessageResponseCreatedEventTypeDef(TypedDict):
    responseId: NotRequired[str]
    sequenceNumber: NotRequired[int]


class SendMessageResponseFailedEventTypeDef(TypedDict):
    responseId: NotRequired[str]
    errorCode: NotRequired[str]
    errorMessage: NotRequired[str]
    sequenceNumber: NotRequired[int]


class SendMessageResponseInProgressEventTypeDef(TypedDict):
    responseId: NotRequired[str]
    sequenceNumber: NotRequired[int]


class SendMessageSummaryEventTypeDef(TypedDict):
    content: NotRequired[str]
    sequenceNumber: NotRequired[int]


class SendMessageUsageInfoTypeDef(TypedDict):
    inputTokens: NotRequired[int]
    outputTokens: NotRequired[int]
    totalTokens: NotRequired[int]


class ServiceNowConfigurationOutputTypeDef(TypedDict):
    instanceId: NotRequired[str]
    authScopes: NotRequired[list[str]]


class SourceAwsConfigurationTypeDef(TypedDict):
    accountId: str
    accountType: Literal["source"]
    assumableRoleArn: str
    externalId: NotRequired[str]
    agentElevatedRoleArn: NotRequired[str]
    agentElevatedRoleArnStatus: NotRequired[ValidationStatusType]


class ServiceNowConfigurationTypeDef(TypedDict):
    instanceId: NotRequired[str]
    authScopes: NotRequired[Sequence[str]]


class ServiceNowOAuthClientCredentialsConfigTypeDef(TypedDict):
    clientId: str
    clientSecret: str
    clientName: NotRequired[str]
    exchangeParameters: NotRequired[Mapping[str, str]]


class SlackChannelTypeDef(TypedDict):
    channelId: str
    channelName: NotRequired[str]


class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateAgentSpaceInputTypeDef(TypedDict):
    agentSpaceId: str
    name: NotRequired[str]
    description: NotRequired[str]
    locale: NotRequired[str]
    preferences: NotRequired[Mapping[Literal["elevatedActionsEnabled"], bool]]


class UpdateBacklogTaskRequestTypeDef(TypedDict):
    agentSpaceId: str
    taskId: str
    taskStatus: NotRequired[TaskStatusType]
    clientToken: NotRequired[str]


class UpdateOperatorAppIdpConfigInputTypeDef(TypedDict):
    agentSpaceId: str
    idpClientSecret: NotRequired[str]


class UpdatePrivateConnectionCertificateInputTypeDef(TypedDict):
    name: str
    certificate: str


class UpdateRecommendationRequestTypeDef(TypedDict):
    agentSpaceId: str
    recommendationId: str
    status: NotRequired[RecommendationStatusType]
    additionalContext: NotRequired[str]
    clientToken: NotRequired[str]


class UpdateTriggerRequestTypeDef(TypedDict):
    agentSpaceId: str
    triggerId: str
    status: NotRequired[str]
    clientToken: NotRequired[str]


class ValidateAwsAssociationsInputTypeDef(TypedDict):
    agentSpaceId: str


class AdditionalServiceDetailsTypeDef(TypedDict):
    github: NotRequired[RegisteredGithubServiceDetailsTypeDef]
    slack: NotRequired[RegisteredSlackServiceDetailsTypeDef]
    mcpserverdatadog: NotRequired[RegisteredMCPServerDetailsTypeDef]
    mcpserver: NotRequired[RegisteredMCPServerDetailsTypeDef]
    servicenow: NotRequired[RegisteredServiceNowDetailsTypeDef]
    gitlab: NotRequired[RegisteredGitLabServiceDetailsTypeDef]
    mcpserversplunk: NotRequired[RegisteredMCPServerDetailsTypeDef]
    mcpservernewrelic: NotRequired[RegisteredNewRelicDetailsTypeDef]
    azuredevops: NotRequired[RegisteredAzureDevOpsServiceDetailsTypeDef]
    azureidentity: NotRequired[RegisteredAzureIdentityDetailsOutputTypeDef]
    mcpservergrafana: NotRequired[RegisteredGrafanaServerDetailsTypeDef]
    pagerduty: NotRequired[RegisteredPagerDutyDetailsTypeDef]
    mcpserversigv4: NotRequired[RegisteredMCPServerSigV4DetailsTypeDef]
    remoteagent: NotRequired[RegisteredRemoteAgentDetailsTypeDef]
    remoteagentsigv4: NotRequired[RegisteredRemoteAgentSigV4DetailsTypeDef]


class AdditionalServiceRegistrationStepTypeDef(TypedDict):
    oauth: NotRequired[OAuthAdditionalStepDetailsTypeDef]


class SendMessageContextTypeDef(TypedDict):
    currentPage: NotRequired[str]
    lastMessage: NotRequired[str]
    userActionResponse: NotRequired[str]
    approvalAction: NotRequired[ApprovalActionTypeDef]


class UpdateApprovalActionRequestTypeDef(TypedDict):
    agentSpaceId: str
    approvalId: str
    action: ApprovalActionTypeType
    finalPattern: NotRequired[ApprovalPatternTypeDef]
    reason: NotRequired[str]
    ttlSeconds: NotRequired[int]
    singleUse: NotRequired[bool]


class AssetFileTypeDef(TypedDict):
    path: str
    content: AssetFileBodyOutputTypeDef
    version: int
    createdAt: datetime
    updatedAt: datetime
    metadata: NotRequired[dict[str, Any]]


AssetFileBodyTypeDef = TypedDict(
    "AssetFileBodyTypeDef",
    {
        "bytes": NotRequired[BlobTypeDef],
        "text": NotRequired[str],
    },
)


class AssetZipContentTypeDef(TypedDict):
    zipFile: BlobTypeDef


class CreateAgentSpaceOutputTypeDef(TypedDict):
    agentSpace: AgentSpaceTypeDef
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAssetResponseTypeDef(TypedDict):
    asset: AssetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateChatResponseTypeDef(TypedDict):
    executionId: str
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


CreatePrivateConnectionOutputTypeDef = TypedDict(
    "CreatePrivateConnectionOutputTypeDef",
    {
        "name": str,
        "type": PrivateConnectionTypeType,
        "resourceGatewayId": str,
        "hostAddress": str,
        "vpcId": str,
        "resourceConfigurationId": str,
        "status": PrivateConnectionStatusType,
        "certificateExpiryTime": datetime,
        "dnsResolution": ResourceConfigDnsResolutionType,
        "failureMessage": str,
        "tags": dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class DeletePrivateConnectionOutputTypeDef(TypedDict):
    name: str
    status: PrivateConnectionStatusType
    ResponseMetadata: ResponseMetadataTypeDef


DescribePrivateConnectionOutputTypeDef = TypedDict(
    "DescribePrivateConnectionOutputTypeDef",
    {
        "name": str,
        "type": PrivateConnectionTypeType,
        "resourceGatewayId": str,
        "hostAddress": str,
        "vpcId": str,
        "resourceConfigurationId": str,
        "status": PrivateConnectionStatusType,
        "certificateExpiryTime": datetime,
        "dnsResolution": ResourceConfigDnsResolutionType,
        "failureMessage": str,
        "tags": dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetAgentSpaceOutputTypeDef(TypedDict):
    agentSpace: AgentSpaceTypeDef
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetAssetContentResponseTypeDef(TypedDict):
    content: AssetZipContentOutputTypeDef
    version: int
    ResponseMetadata: ResponseMetadataTypeDef


class GetAssetResponseTypeDef(TypedDict):
    asset: AssetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListAgentSpacesOutputTypeDef(TypedDict):
    agentSpaces: list[AgentSpaceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListAssetFilesResponseTypeDef(TypedDict):
    items: list[AssetFileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListAssetTypesResponseTypeDef(TypedDict):
    items: list[AssetTypeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListAssetVersionsResponseTypeDef(TypedDict):
    items: list[AssetVersionMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListAssetsResponseTypeDef(TypedDict):
    items: list[AssetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAgentSpaceOutputTypeDef(TypedDict):
    agentSpace: AgentSpaceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateApprovalActionResponseTypeDef(TypedDict):
    approvalId: str
    status: ApprovalStatusType
    expiresAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAssetResponseTypeDef(TypedDict):
    asset: AssetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


UpdatePrivateConnectionCertificateOutputTypeDef = TypedDict(
    "UpdatePrivateConnectionCertificateOutputTypeDef",
    {
        "name": str,
        "type": PrivateConnectionTypeType,
        "resourceGatewayId": str,
        "hostAddress": str,
        "vpcId": str,
        "resourceConfigurationId": str,
        "status": PrivateConnectionStatusType,
        "certificateExpiryTime": datetime,
        "dnsResolution": ResourceConfigDnsResolutionType,
        "failureMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class ListChatsResponseTypeDef(TypedDict):
    executions: list[ChatExecutionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateBacklogTaskRequestTypeDef(TypedDict):
    agentSpaceId: str
    taskType: TaskTypeType
    title: str
    priority: PriorityType
    reference: NotRequired[ReferenceInputTypeDef]
    description: NotRequired[str]
    clientToken: NotRequired[str]


class DatadogAuthorizationConfigTypeDef(TypedDict):
    authorizationDiscovery: NotRequired[MCPServerAuthorizationDiscoveryConfigTypeDef]


class DynatraceServiceAuthorizationConfigTypeDef(TypedDict):
    oAuthClientCredentials: NotRequired[DynatraceOAuthClientCredentialsConfigTypeDef]


class EnableOperatorAppOutputTypeDef(TypedDict):
    agentSpaceId: str
    operatorAppUrl: str
    iam: IamAuthConfigurationTypeDef
    idc: IdcAuthConfigurationTypeDef
    idp: IdpAuthConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetOperatorAppOutputTypeDef(TypedDict):
    operatorAppUrl: str
    iam: IamAuthConfigurationTypeDef
    idc: IdcAuthConfigurationTypeDef
    idp: IdpAuthConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateOperatorAppIdpConfigOutputTypeDef(TypedDict):
    agentSpaceId: str
    idp: IdpAuthConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListExecutionsResponseTypeDef(TypedDict):
    executions: list[ExecutionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetAccountUsageOutputTypeDef(TypedDict):
    monthlyAccountInvestigationHours: UsageMetricTypeDef
    monthlyAccountEvaluationHours: UsageMetricTypeDef
    monthlyAccountSystemLearningHours: UsageMetricTypeDef
    monthlyAccountOnDemandHours: UsageMetricTypeDef
    usagePeriodStartTime: datetime
    usagePeriodEndTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateGoalRequestTypeDef(TypedDict):
    agentSpaceId: str
    goalId: str
    evaluationSchedule: NotRequired[GoalScheduleInputTypeDef]
    clientToken: NotRequired[str]


class GoalTypeDef(TypedDict):
    agentSpaceArn: str
    goalId: str
    title: str
    content: GoalContentTypeDef
    status: GoalStatusType
    goalType: GoalTypeType
    createdAt: datetime
    updatedAt: datetime
    version: int
    lastEvaluatedAt: NotRequired[datetime]
    lastTaskId: NotRequired[str]
    lastSuccessfulTaskId: NotRequired[str]
    evaluationSchedule: NotRequired[GoalScheduleTypeDef]


class JournalRecordTypeDef(TypedDict):
    agentSpaceId: str
    executionId: str
    recordId: str
    content: dict[str, Any]
    createdAt: datetime
    recordType: str
    userReference: NotRequired[UserReferenceTypeDef]


class ListAgentSpacesInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAssetFilesRequestPaginateTypeDef(TypedDict):
    agentSpaceId: str
    assetId: str
    assetVersion: NotRequired[int]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAssetTypesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAssetVersionsRequestPaginateTypeDef(TypedDict):
    agentSpaceId: str
    assetId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAssociationsInputPaginateTypeDef(TypedDict):
    agentSpaceId: str
    filterServiceTypes: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListExecutionsRequestPaginateTypeDef(TypedDict):
    agentSpaceId: str
    taskId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGoalsRequestPaginateTypeDef(TypedDict):
    agentSpaceId: str
    status: NotRequired[GoalStatusType]
    goalType: NotRequired[GoalTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListJournalRecordsRequestPaginateTypeDef(TypedDict):
    agentSpaceId: str
    executionId: str
    recordType: NotRequired[str]
    order: NotRequired[OrderTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListServicesInputPaginateTypeDef(TypedDict):
    filterServiceType: NotRequired[ServiceType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTriggersRequestPaginateTypeDef(TypedDict):
    agentSpaceId: str
    status: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAssetsRequestPaginateTypeDef(TypedDict):
    agentSpaceId: str
    assetType: NotRequired[str]
    updatedAfter: NotRequired[TimestampTypeDef]
    updatedBefore: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAssetsRequestTypeDef(TypedDict):
    agentSpaceId: str
    assetType: NotRequired[str]
    updatedAfter: NotRequired[TimestampTypeDef]
    updatedBefore: NotRequired[TimestampTypeDef]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class TaskFilterTypeDef(TypedDict):
    createdAfter: NotRequired[TimestampTypeDef]
    createdBefore: NotRequired[TimestampTypeDef]
    priority: NotRequired[Sequence[PriorityType]]
    status: NotRequired[Sequence[TaskStatusType]]
    taskType: NotRequired[Sequence[TaskTypeType]]
    primaryTaskId: NotRequired[str]


class ListPrivateConnectionsOutputTypeDef(TypedDict):
    privateConnections: list[PrivateConnectionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListWebhooksOutputTypeDef(TypedDict):
    webhooks: list[WebhookTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class MCPServerAuthorizationConfigTypeDef(TypedDict):
    oAuthClientCredentials: NotRequired[MCPServerOAuthClientCredentialsConfigTypeDef]
    oAuth3LO: NotRequired[MCPServerOAuth3LOConfigTypeDef]
    apiKey: NotRequired[MCPServerAPIKeyConfigTypeDef]
    bearerToken: NotRequired[MCPServerBearerTokenConfigTypeDef]
    authorizationDiscovery: NotRequired[MCPServerAuthorizationDiscoveryConfigTypeDef]


class MCPServerConfigurationOutputTypeDef(TypedDict):
    tools: list[str]
    toolDetails: NotRequired[list[MCPToolDetailTypeDef]]


class MCPServerConfigurationTypeDef(TypedDict):
    tools: Sequence[str]
    toolDetails: NotRequired[Sequence[MCPToolDetailTypeDef]]


class MCPServerDatadogConfigurationOutputTypeDef(TypedDict):
    enabledElevatedTools: NotRequired[list[MCPToolDetailTypeDef]]


class MCPServerDatadogConfigurationTypeDef(TypedDict):
    enabledElevatedTools: NotRequired[Sequence[MCPToolDetailTypeDef]]


class MCPServerGrafanaConfigurationOutputTypeDef(TypedDict):
    endpoint: str
    organizationId: NotRequired[str]
    tools: NotRequired[list[str]]
    enabledElevatedTools: NotRequired[list[MCPToolDetailTypeDef]]


class MCPServerGrafanaConfigurationTypeDef(TypedDict):
    endpoint: str
    organizationId: NotRequired[str]
    tools: NotRequired[Sequence[str]]
    enabledElevatedTools: NotRequired[Sequence[MCPToolDetailTypeDef]]


class MCPServerSigV4ConfigurationOutputTypeDef(TypedDict):
    tools: list[str]
    toolDetails: NotRequired[list[MCPToolDetailTypeDef]]


class MCPServerSigV4ConfigurationTypeDef(TypedDict):
    tools: Sequence[str]
    toolDetails: NotRequired[Sequence[MCPToolDetailTypeDef]]


class MCPServerSigV4ServiceDetailsTypeDef(TypedDict):
    name: str
    endpoint: str
    authorizationConfig: MCPServerSigV4AuthorizationConfigTypeDef
    description: NotRequired[str]


class MessageTypeDef(TypedDict):
    userMessage: NotRequired[list[UserMessageBlockTypeDef]]
    assistantMessage: NotRequired[list[AssistantMessageBlockTypeDef]]


class NewRelicServiceAuthorizationConfigTypeDef(TypedDict):
    apiKey: NotRequired[NewRelicApiKeyConfigTypeDef]


class PagerDutyAuthorizationConfigTypeDef(TypedDict):
    oAuthClientCredentials: NotRequired[PagerDutyOAuthClientCredentialsConfigTypeDef]


class PrivateConnectionModeTypeDef(TypedDict):
    serviceManaged: NotRequired[ServiceManagedInputTypeDef]
    selfManaged: NotRequired[SelfManagedInputTypeDef]


class RecommendationTypeDef(TypedDict):
    agentSpaceArn: str
    recommendationId: str
    taskId: str
    title: str
    content: RecommendationContentTypeDef
    status: RecommendationStatusType
    priority: RecommendationPriorityType
    createdAt: datetime
    updatedAt: datetime
    version: int
    goalId: NotRequired[str]
    goalVersion: NotRequired[int]
    additionalContext: NotRequired[str]
    rankPosition: NotRequired[int]
    rankedAt: NotRequired[datetime]


class TaskTypeDef(TypedDict):
    agentSpaceId: str
    taskId: str
    title: str
    taskType: TaskTypeType
    priority: PriorityType
    status: TaskStatusType
    createdAt: datetime
    updatedAt: datetime
    version: int
    executionId: NotRequired[str]
    description: NotRequired[str]
    reference: NotRequired[ReferenceOutputTypeDef]
    supportMetadata: NotRequired[dict[str, Any]]
    metadata: NotRequired[dict[str, Any]]
    primaryTaskId: NotRequired[str]
    statusReason: NotRequired[str]
    hasLinkedTasks: NotRequired[bool]


RegisteredAzureIdentityDetailsUnionTypeDef = Union[
    RegisteredAzureIdentityDetailsTypeDef, RegisteredAzureIdentityDetailsOutputTypeDef
]


class RemoteAgentAuthorizationConfigTypeDef(TypedDict):
    apiKey: NotRequired[RemoteAgentAPIKeyConfigTypeDef]
    oAuthClientCredentials: NotRequired[RemoteAgentOAuthClientCredentialsConfigTypeDef]
    bearerToken: NotRequired[RemoteAgentBearerTokenConfigTypeDef]


class RemoteAgentSigV4ServiceDetailsTypeDef(TypedDict):
    name: str
    endpoint: str
    authorizationConfig: RemoteAgentSigV4AuthorizationConfigTypeDef
    description: NotRequired[str]


class TriggerConditionTypeDef(TypedDict):
    schedule: NotRequired[ScheduleConditionTypeDef]


class SendMessageContentBlockDeltaTypeDef(TypedDict):
    textDelta: NotRequired[SendMessageTextDeltaTypeDef]
    jsonDelta: NotRequired[SendMessageJsonDeltaTypeDef]


class SendMessageResponseCompletedEventTypeDef(TypedDict):
    responseId: NotRequired[str]
    usage: NotRequired[SendMessageUsageInfoTypeDef]
    sequenceNumber: NotRequired[int]


class ServiceNowServiceAuthorizationConfigTypeDef(TypedDict):
    oAuthClientCredentials: NotRequired[ServiceNowOAuthClientCredentialsConfigTypeDef]


class SlackTransmissionTargetTypeDef(TypedDict):
    opsOncallTarget: SlackChannelTypeDef
    opsSRETarget: NotRequired[SlackChannelTypeDef]


class RegisteredServiceTypeDef(TypedDict):
    serviceId: str
    serviceType: ServiceType
    createdAt: datetime
    updatedAt: datetime
    name: NotRequired[str]
    accessibleResources: NotRequired[list[dict[str, Any]]]
    additionalServiceDetails: NotRequired[AdditionalServiceDetailsTypeDef]
    kmsKeyArn: NotRequired[str]
    privateConnectionName: NotRequired[str]


class RegisterServiceOutputTypeDef(TypedDict):
    serviceId: str
    additionalStep: AdditionalServiceRegistrationStepTypeDef
    kmsKeyArn: str
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class SendMessageRequestTypeDef(TypedDict):
    agentSpaceId: str
    executionId: str
    content: str
    context: NotRequired[SendMessageContextTypeDef]
    userId: NotRequired[str]
    assetIds: NotRequired[Sequence[str]]
    modelTier: NotRequired[str]


class CreateAssetFileResponseTypeDef(TypedDict):
    file: AssetFileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetAssetFileResponseTypeDef(TypedDict):
    file: AssetFileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAssetFileResponseTypeDef(TypedDict):
    file: AssetFileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


AssetFileBodyUnionTypeDef = Union[AssetFileBodyTypeDef, AssetFileBodyOutputTypeDef]
AssetZipContentUnionTypeDef = Union[AssetZipContentTypeDef, AssetZipContentOutputTypeDef]


class DatadogServiceDetailsTypeDef(TypedDict):
    name: str
    endpoint: str
    authorizationConfig: DatadogAuthorizationConfigTypeDef
    description: NotRequired[str]


class DynatraceServiceDetailsTypeDef(TypedDict):
    accountUrn: str
    authorizationConfig: NotRequired[DynatraceServiceAuthorizationConfigTypeDef]


class ListGoalsResponseTypeDef(TypedDict):
    goals: list[GoalTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateGoalResponseTypeDef(TypedDict):
    goal: GoalTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListJournalRecordsResponseTypeDef(TypedDict):
    records: list[JournalRecordTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


ListBacklogTasksRequestPaginateTypeDef = TypedDict(
    "ListBacklogTasksRequestPaginateTypeDef",
    {
        "agentSpaceId": str,
        "filter": NotRequired[TaskFilterTypeDef],
        "sortField": NotRequired[TaskSortFieldType],
        "order": NotRequired[TaskSortOrderType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListBacklogTasksRequestTypeDef = TypedDict(
    "ListBacklogTasksRequestTypeDef",
    {
        "agentSpaceId": str,
        "filter": NotRequired[TaskFilterTypeDef],
        "limit": NotRequired[int],
        "nextToken": NotRequired[str],
        "sortField": NotRequired[TaskSortFieldType],
        "order": NotRequired[TaskSortOrderType],
    },
)


class GrafanaServiceDetailsTypeDef(TypedDict):
    name: str
    endpoint: str
    authorizationConfig: MCPServerAuthorizationConfigTypeDef
    description: NotRequired[str]


class MCPServerDetailsTypeDef(TypedDict):
    name: str
    endpoint: str
    authorizationConfig: MCPServerAuthorizationConfigTypeDef
    description: NotRequired[str]


class PendingMessageTypeDef(TypedDict):
    messageId: str
    message: MessageTypeDef


class NewRelicServiceDetailsTypeDef(TypedDict):
    authorizationConfig: NewRelicServiceAuthorizationConfigTypeDef


class PagerDutyDetailsTypeDef(TypedDict):
    scopes: Sequence[str]
    authorizationConfig: PagerDutyAuthorizationConfigTypeDef


class CreatePrivateConnectionInputTypeDef(TypedDict):
    name: str
    mode: PrivateConnectionModeTypeDef
    tags: NotRequired[Mapping[str, str]]


class GetRecommendationResponseTypeDef(TypedDict):
    recommendation: RecommendationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListRecommendationsResponseTypeDef(TypedDict):
    recommendations: list[RecommendationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateRecommendationResponseTypeDef(TypedDict):
    recommendation: RecommendationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateBacklogTaskResponseTypeDef(TypedDict):
    task: TaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetBacklogTaskResponseTypeDef(TypedDict):
    task: TaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListBacklogTasksResponseTypeDef(TypedDict):
    tasks: list[TaskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateBacklogTaskResponseTypeDef(TypedDict):
    task: TaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RemoteAgentServiceDetailsTypeDef(TypedDict):
    name: str
    endpoint: str
    authorizationConfig: RemoteAgentAuthorizationConfigTypeDef
    description: NotRequired[str]


CreateTriggerRequestTypeDef = TypedDict(
    "CreateTriggerRequestTypeDef",
    {
        "agentSpaceId": str,
        "type": str,
        "condition": TriggerConditionTypeDef,
        "action": Mapping[str, Any],
        "status": NotRequired[str],
        "clientToken": NotRequired[str],
    },
)
TriggerTypeDef = TypedDict(
    "TriggerTypeDef",
    {
        "triggerId": str,
        "agentSpaceId": str,
        "type": str,
        "condition": TriggerConditionTypeDef,
        "action": dict[str, Any],
        "status": str,
        "createdAt": datetime,
        "updatedAt": datetime,
    },
)


class SendMessageContentBlockDeltaEventTypeDef(TypedDict):
    index: NotRequired[int]
    delta: NotRequired[SendMessageContentBlockDeltaTypeDef]
    sequenceNumber: NotRequired[int]


class ServiceNowServiceDetailsTypeDef(TypedDict):
    instanceUrl: str
    authorizationConfig: NotRequired[ServiceNowServiceAuthorizationConfigTypeDef]


class SlackConfigurationTypeDef(TypedDict):
    workspaceId: str
    workspaceName: str
    transmissionTarget: SlackTransmissionTargetTypeDef


class GetServiceOutputTypeDef(TypedDict):
    service: RegisteredServiceTypeDef
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ListServicesOutputTypeDef(TypedDict):
    services: list[RegisteredServiceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class AssetFileContentTypeDef(TypedDict):
    path: str
    body: AssetFileBodyUnionTypeDef
    metadata: NotRequired[Mapping[str, Any]]


class CreateAssetFileRequestTypeDef(TypedDict):
    agentSpaceId: str
    assetId: str
    path: str
    content: AssetFileBodyUnionTypeDef
    metadata: NotRequired[Mapping[str, Any]]
    clientToken: NotRequired[str]


class UpdateAssetFileRequestTypeDef(TypedDict):
    agentSpaceId: str
    assetId: str
    path: str
    content: NotRequired[AssetFileBodyUnionTypeDef]
    metadata: NotRequired[Mapping[str, Any]]
    clientToken: NotRequired[str]


class ListPendingMessagesResponseTypeDef(TypedDict):
    agentSpaceId: str
    executionId: str
    messages: list[PendingMessageTypeDef]
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTriggerResponseTypeDef(TypedDict):
    trigger: TriggerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetTriggerResponseTypeDef(TypedDict):
    trigger: TriggerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListTriggersResponseTypeDef(TypedDict):
    items: list[TriggerTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateTriggerResponseTypeDef(TypedDict):
    trigger: TriggerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SendMessageEventsTypeDef(TypedDict):
    responseCreated: NotRequired[SendMessageResponseCreatedEventTypeDef]
    responseInProgress: NotRequired[SendMessageResponseInProgressEventTypeDef]
    responseCompleted: NotRequired[SendMessageResponseCompletedEventTypeDef]
    responseFailed: NotRequired[SendMessageResponseFailedEventTypeDef]
    summary: NotRequired[SendMessageSummaryEventTypeDef]
    heartbeat: NotRequired[dict[str, Any]]
    contentBlockStart: NotRequired[SendMessageContentBlockStartEventTypeDef]
    contentBlockDelta: NotRequired[SendMessageContentBlockDeltaEventTypeDef]
    contentBlockStop: NotRequired[SendMessageContentBlockStopEventTypeDef]


class ServiceDetailsTypeDef(TypedDict):
    dynatrace: NotRequired[DynatraceServiceDetailsTypeDef]
    servicenow: NotRequired[ServiceNowServiceDetailsTypeDef]
    mcpserverdatadog: NotRequired[DatadogServiceDetailsTypeDef]
    mcpserver: NotRequired[MCPServerDetailsTypeDef]
    gitlab: NotRequired[GitLabDetailsTypeDef]
    mcpserversplunk: NotRequired[MCPServerDetailsTypeDef]
    mcpservernewrelic: NotRequired[NewRelicServiceDetailsTypeDef]
    eventChannel: NotRequired[EventChannelDetailsTypeDef]
    mcpservergrafana: NotRequired[GrafanaServiceDetailsTypeDef]
    pagerduty: NotRequired[PagerDutyDetailsTypeDef]
    azureidentity: NotRequired[RegisteredAzureIdentityDetailsUnionTypeDef]
    mcpserversigv4: NotRequired[MCPServerSigV4ServiceDetailsTypeDef]
    remoteagent: NotRequired[RemoteAgentServiceDetailsTypeDef]
    remoteagentsigv4: NotRequired[RemoteAgentSigV4ServiceDetailsTypeDef]


class ServiceConfigurationOutputTypeDef(TypedDict):
    sourceAws: NotRequired[SourceAwsConfigurationTypeDef]
    aws: NotRequired[AWSConfigurationTypeDef]
    github: NotRequired[GitHubConfigurationTypeDef]
    slack: NotRequired[SlackConfigurationTypeDef]
    dynatrace: NotRequired[DynatraceConfigurationOutputTypeDef]
    servicenow: NotRequired[ServiceNowConfigurationOutputTypeDef]
    mcpservernewrelic: NotRequired[MCPServerNewRelicConfigurationTypeDef]
    mcpserverdatadog: NotRequired[MCPServerDatadogConfigurationOutputTypeDef]
    mcpserver: NotRequired[MCPServerConfigurationOutputTypeDef]
    gitlab: NotRequired[GitLabConfigurationTypeDef]
    mcpserversplunk: NotRequired[dict[str, Any]]
    eventChannel: NotRequired[dict[str, Any]]
    azure: NotRequired[AzureConfigurationTypeDef]
    azuredevops: NotRequired[AzureDevOpsConfigurationTypeDef]
    mcpservergrafana: NotRequired[MCPServerGrafanaConfigurationOutputTypeDef]
    pagerduty: NotRequired[PagerDutyConfigurationOutputTypeDef]
    mcpserversigv4: NotRequired[MCPServerSigV4ConfigurationOutputTypeDef]
    remoteagent: NotRequired[dict[str, Any]]
    remoteagentsigv4: NotRequired[dict[str, Any]]


class ServiceConfigurationTypeDef(TypedDict):
    sourceAws: NotRequired[SourceAwsConfigurationTypeDef]
    aws: NotRequired[AWSConfigurationTypeDef]
    github: NotRequired[GitHubConfigurationTypeDef]
    slack: NotRequired[SlackConfigurationTypeDef]
    dynatrace: NotRequired[DynatraceConfigurationTypeDef]
    servicenow: NotRequired[ServiceNowConfigurationTypeDef]
    mcpservernewrelic: NotRequired[MCPServerNewRelicConfigurationTypeDef]
    mcpserverdatadog: NotRequired[MCPServerDatadogConfigurationTypeDef]
    mcpserver: NotRequired[MCPServerConfigurationTypeDef]
    gitlab: NotRequired[GitLabConfigurationTypeDef]
    mcpserversplunk: NotRequired[Mapping[str, Any]]
    eventChannel: NotRequired[Mapping[str, Any]]
    azure: NotRequired[AzureConfigurationTypeDef]
    azuredevops: NotRequired[AzureDevOpsConfigurationTypeDef]
    mcpservergrafana: NotRequired[MCPServerGrafanaConfigurationTypeDef]
    pagerduty: NotRequired[PagerDutyConfigurationTypeDef]
    mcpserversigv4: NotRequired[MCPServerSigV4ConfigurationTypeDef]
    remoteagent: NotRequired[Mapping[str, Any]]
    remoteagentsigv4: NotRequired[Mapping[str, Any]]


AssetContentTypeDef = TypedDict(
    "AssetContentTypeDef",
    {
        "file": NotRequired[AssetFileContentTypeDef],
        "zip": NotRequired[AssetZipContentUnionTypeDef],
        "sourceUrl": NotRequired[AssetSourceUrlContentTypeDef],
    },
)


class SendMessageResponseTypeDef(TypedDict):
    events: EventStream[SendMessageEventsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterServiceInputTypeDef(TypedDict):
    service: PostRegisterServiceSupportedServiceType
    serviceDetails: ServiceDetailsTypeDef
    kmsKeyArn: NotRequired[str]
    privateConnectionName: NotRequired[str]
    targetUrlPrivateConnectionName: NotRequired[str]
    exchangeUrlPrivateConnectionName: NotRequired[str]
    name: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class AssociationTypeDef(TypedDict):
    agentSpaceId: str
    createdAt: datetime
    updatedAt: datetime
    associationId: str
    serviceId: str
    configuration: ServiceConfigurationOutputTypeDef
    status: NotRequired[ValidationStatusType]
    capabilities: NotRequired[dict[CapabilityTypeType, CapabilityConfigurationTypeDef]]


ServiceConfigurationUnionTypeDef = Union[
    ServiceConfigurationTypeDef, ServiceConfigurationOutputTypeDef
]


class CreateAssetRequestTypeDef(TypedDict):
    agentSpaceId: str
    assetType: str
    content: AssetContentTypeDef
    metadata: NotRequired[Mapping[str, Any]]
    clientToken: NotRequired[str]


class UpdateAssetRequestTypeDef(TypedDict):
    agentSpaceId: str
    assetId: str
    metadata: NotRequired[Mapping[str, Any]]
    content: NotRequired[AssetContentTypeDef]
    clientToken: NotRequired[str]


class AssociateServiceOutputTypeDef(TypedDict):
    association: AssociationTypeDef
    webhook: GenericWebhookTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetAssociationOutputTypeDef(TypedDict):
    association: AssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListAssociationsOutputTypeDef(TypedDict):
    associations: list[AssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateAssociationOutputTypeDef(TypedDict):
    association: AssociationTypeDef
    webhook: GenericWebhookTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateServiceInputTypeDef(TypedDict):
    agentSpaceId: str
    serviceId: str
    configuration: ServiceConfigurationUnionTypeDef
    capabilities: NotRequired[Mapping[CapabilityTypeType, CapabilityConfigurationTypeDef]]


class UpdateAssociationInputTypeDef(TypedDict):
    agentSpaceId: str
    associationId: str
    configuration: ServiceConfigurationUnionTypeDef
    capabilities: NotRequired[Mapping[CapabilityTypeType, CapabilityConfigurationTypeDef]]
