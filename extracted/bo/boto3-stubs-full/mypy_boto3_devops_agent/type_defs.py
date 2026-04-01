"""
Type annotations for devops-agent service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_devops_agent.type_defs import AWSConfigurationTypeDef

    data: AWSConfigurationTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Union

from botocore.eventstream import EventStream

from .literals import (
    AuthFlowType,
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
    SchedulerStateType,
    ServiceType,
    TaskSortFieldType,
    TaskSortOrderType,
    TaskStatusType,
    TaskTypeType,
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
    "AllowVendedLogDeliveryForResourceInputTypeDef",
    "AllowVendedLogDeliveryForResourceOutputTypeDef",
    "AssistantMessageBlockTypeDef",
    "AssociateServiceInputTypeDef",
    "AssociateServiceOutputTypeDef",
    "AssociationTypeDef",
    "AzureConfigurationTypeDef",
    "AzureDevOpsConfigurationTypeDef",
    "ChatExecutionTypeDef",
    "CreateAgentSpaceInputTypeDef",
    "CreateAgentSpaceOutputTypeDef",
    "CreateBacklogTaskRequestTypeDef",
    "CreateBacklogTaskResponseTypeDef",
    "CreateChatRequestTypeDef",
    "CreateChatResponseTypeDef",
    "CreatePrivateConnectionInputTypeDef",
    "CreatePrivateConnectionOutputTypeDef",
    "DatadogAuthorizationConfigTypeDef",
    "DatadogServiceDetailsTypeDef",
    "DeleteAgentSpaceInputTypeDef",
    "DeletePrivateConnectionInputTypeDef",
    "DeletePrivateConnectionOutputTypeDef",
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
    "ListWebhooksInputTypeDef",
    "ListWebhooksOutputTypeDef",
    "MCPServerAPIKeyConfigTypeDef",
    "MCPServerAuthorizationConfigTypeDef",
    "MCPServerAuthorizationDiscoveryConfigTypeDef",
    "MCPServerBearerTokenConfigTypeDef",
    "MCPServerDetailsTypeDef",
    "MCPServerGrafanaConfigurationOutputTypeDef",
    "MCPServerGrafanaConfigurationTypeDef",
    "MCPServerNewRelicConfigurationTypeDef",
    "MCPServerOAuth3LOConfigTypeDef",
    "MCPServerOAuthClientCredentialsConfigTypeDef",
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
    "RegisteredNewRelicDetailsTypeDef",
    "RegisteredPagerDutyDetailsTypeDef",
    "RegisteredServiceNowDetailsTypeDef",
    "RegisteredServiceTypeDef",
    "RegisteredSlackServiceDetailsTypeDef",
    "ResponseMetadataTypeDef",
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
    "UntagResourceRequestTypeDef",
    "UpdateAgentSpaceInputTypeDef",
    "UpdateAgentSpaceOutputTypeDef",
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


class RegisteredNewRelicDetailsTypeDef(TypedDict):
    accountId: str
    region: NewRelicRegionType
    description: NotRequired[str]


class RegisteredPagerDutyDetailsTypeDef(TypedDict):
    scopes: list[str]


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


class AllowVendedLogDeliveryForResourceInputTypeDef(TypedDict):
    resourceArnBeingAuthorized: str
    deliverySourceArn: str
    logType: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AssistantMessageBlockTypeDef(TypedDict):
    text: NotRequired[str]
    toolUse: NotRequired[dict[str, Any]]


class GenericWebhookTypeDef(TypedDict):
    webhookUrl: NotRequired[str]
    webhookId: NotRequired[str]
    webhookType: NotRequired[WebhookTypeType]
    webhookSecret: NotRequired[str]
    apiKey: NotRequired[str]


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


class ReferenceInputTypeDef(TypedDict):
    system: str
    referenceId: str
    referenceUrl: str
    associationId: str
    title: NotRequired[str]


class CreateChatRequestTypeDef(TypedDict):
    agentSpaceId: str
    userId: str
    userType: NotRequired[UserTypeType]


class MCPServerAuthorizationDiscoveryConfigTypeDef(TypedDict):
    returnToEndpoint: str


class DeleteAgentSpaceInputTypeDef(TypedDict):
    agentSpaceId: str


class DeletePrivateConnectionInputTypeDef(TypedDict):
    name: str


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


class GitHubConfigurationTypeDef(TypedDict):
    repoName: str
    repoId: str
    owner: str
    ownerType: GithubRepoOwnerTypeType
    instanceIdentifier: NotRequired[str]


class GitLabConfigurationTypeDef(TypedDict):
    projectId: str
    projectPath: str
    instanceIdentifier: NotRequired[str]


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


class ListAssociationsInputTypeDef(TypedDict):
    agentSpaceId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    filterServiceTypes: NotRequired[str]


class ListChatsRequestTypeDef(TypedDict):
    agentSpaceId: str
    userId: str
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


class MCPServerGrafanaConfigurationOutputTypeDef(TypedDict):
    endpoint: str
    organizationId: NotRequired[str]
    tools: NotRequired[list[str]]


class MCPServerGrafanaConfigurationTypeDef(TypedDict):
    endpoint: str
    organizationId: NotRequired[str]
    tools: NotRequired[Sequence[str]]


class MCPServerNewRelicConfigurationTypeDef(TypedDict):
    accountId: str
    endpoint: str


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


class SendMessageContextTypeDef(TypedDict):
    currentPage: NotRequired[str]
    lastMessage: NotRequired[str]
    userActionResponse: NotRequired[str]


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


TimestampTypeDef = Union[datetime, str]


class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateAgentSpaceInputTypeDef(TypedDict):
    agentSpaceId: str
    name: NotRequired[str]
    description: NotRequired[str]
    locale: NotRequired[str]


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


class AdditionalServiceRegistrationStepTypeDef(TypedDict):
    oauth: NotRequired[OAuthAdditionalStepDetailsTypeDef]


class AllowVendedLogDeliveryForResourceOutputTypeDef(TypedDict):
    message: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAgentSpaceOutputTypeDef(TypedDict):
    agentSpace: AgentSpaceTypeDef
    tags: dict[str, str]
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


class ListAgentSpacesOutputTypeDef(TypedDict):
    agentSpaces: list[AgentSpaceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAgentSpaceOutputTypeDef(TypedDict):
    agentSpace: AgentSpaceTypeDef
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
    iam: IamAuthConfigurationTypeDef
    idc: IdcAuthConfigurationTypeDef
    idp: IdpAuthConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetOperatorAppOutputTypeDef(TypedDict):
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


class SendMessageContentBlockDeltaTypeDef(TypedDict):
    textDelta: NotRequired[SendMessageTextDeltaTypeDef]
    jsonDelta: NotRequired[SendMessageJsonDeltaTypeDef]


class SendMessageRequestTypeDef(TypedDict):
    agentSpaceId: str
    executionId: str
    content: str
    userId: str
    context: NotRequired[SendMessageContextTypeDef]


class SendMessageResponseCompletedEventTypeDef(TypedDict):
    responseId: NotRequired[str]
    usage: NotRequired[SendMessageUsageInfoTypeDef]
    sequenceNumber: NotRequired[int]


class ServiceNowServiceAuthorizationConfigTypeDef(TypedDict):
    oAuthClientCredentials: NotRequired[ServiceNowOAuthClientCredentialsConfigTypeDef]


class SlackTransmissionTargetTypeDef(TypedDict):
    opsOncallTarget: SlackChannelTypeDef
    opsSRETarget: NotRequired[SlackChannelTypeDef]


class TaskFilterTypeDef(TypedDict):
    createdAfter: NotRequired[TimestampTypeDef]
    createdBefore: NotRequired[TimestampTypeDef]
    priority: NotRequired[Sequence[PriorityType]]
    status: NotRequired[Sequence[TaskStatusType]]
    taskType: NotRequired[Sequence[TaskTypeType]]
    primaryTaskId: NotRequired[str]


class RegisteredServiceTypeDef(TypedDict):
    serviceId: str
    serviceType: ServiceType
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


class GetServiceOutputTypeDef(TypedDict):
    service: RegisteredServiceTypeDef
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ListServicesOutputTypeDef(TypedDict):
    services: list[RegisteredServiceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListPendingMessagesResponseTypeDef(TypedDict):
    agentSpaceId: str
    executionId: str
    messages: list[PendingMessageTypeDef]
    createdAt: datetime
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


class ServiceConfigurationOutputTypeDef(TypedDict):
    sourceAws: NotRequired[SourceAwsConfigurationTypeDef]
    aws: NotRequired[AWSConfigurationTypeDef]
    github: NotRequired[GitHubConfigurationTypeDef]
    slack: NotRequired[SlackConfigurationTypeDef]
    dynatrace: NotRequired[DynatraceConfigurationOutputTypeDef]
    servicenow: NotRequired[ServiceNowConfigurationOutputTypeDef]
    mcpservernewrelic: NotRequired[MCPServerNewRelicConfigurationTypeDef]
    gitlab: NotRequired[GitLabConfigurationTypeDef]
    eventChannel: NotRequired[dict[str, Any]]
    azure: NotRequired[AzureConfigurationTypeDef]
    azuredevops: NotRequired[AzureDevOpsConfigurationTypeDef]
    mcpservergrafana: NotRequired[MCPServerGrafanaConfigurationOutputTypeDef]
    pagerduty: NotRequired[PagerDutyConfigurationOutputTypeDef]


class ServiceConfigurationTypeDef(TypedDict):
    sourceAws: NotRequired[SourceAwsConfigurationTypeDef]
    aws: NotRequired[AWSConfigurationTypeDef]
    github: NotRequired[GitHubConfigurationTypeDef]
    slack: NotRequired[SlackConfigurationTypeDef]
    dynatrace: NotRequired[DynatraceConfigurationTypeDef]
    servicenow: NotRequired[ServiceNowConfigurationTypeDef]
    mcpservernewrelic: NotRequired[MCPServerNewRelicConfigurationTypeDef]
    gitlab: NotRequired[GitLabConfigurationTypeDef]
    eventChannel: NotRequired[Mapping[str, Any]]
    azure: NotRequired[AzureConfigurationTypeDef]
    azuredevops: NotRequired[AzureDevOpsConfigurationTypeDef]
    mcpservergrafana: NotRequired[MCPServerGrafanaConfigurationTypeDef]
    pagerduty: NotRequired[PagerDutyConfigurationTypeDef]


class SendMessageResponseTypeDef(TypedDict):
    events: EventStream[SendMessageEventsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterServiceInputTypeDef(TypedDict):
    service: PostRegisterServiceSupportedServiceType
    serviceDetails: ServiceDetailsTypeDef
    kmsKeyArn: NotRequired[str]
    privateConnectionName: NotRequired[str]
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


ServiceConfigurationUnionTypeDef = Union[
    ServiceConfigurationTypeDef, ServiceConfigurationOutputTypeDef
]


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


class UpdateAssociationInputTypeDef(TypedDict):
    agentSpaceId: str
    associationId: str
    configuration: ServiceConfigurationUnionTypeDef
