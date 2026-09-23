"""
Type annotations for cloudwatchomni service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatchomni/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_cloudwatchomni.type_defs import AccessGrantPrincipalAttributeTypeDef

    data: AccessGrantPrincipalAttributeTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Union

from .literals import (
    AccessGrantPermissionType,
    AccessGrantPrincipalTypeType,
    AccessGrantTypeType,
    AccessProfileTypeType,
    AlertSortFieldType,
    AlertSortOrderType,
    AlertStateType,
    AssumeStatusType,
    AuthTypeType,
    ComparatorType,
    EdgeTypeType,
    EncryptionStrategyType,
    IdentityProviderType,
    IntegrationStatusType,
    IntegrationTypeType,
    NodeCategoryType,
    NodeTypeType,
    NotificationStatusType,
    NotificationTargetTypeType,
    OrganizationGrantPrincipalTypeType,
    PrincipalTypeType,
    QueryLanguageType,
    QueryStatusType,
    ScopeType,
    SignalType,
    SignalTypeType,
    SourceType,
    SpaceStatusType,
    TelemetryTypeType,
    ThresholdModeType,
    ViewTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AccessGrantPrincipalAttributeTypeDef",
    "AccessGrantPrincipalOutputTypeDef",
    "AccessGrantPrincipalTypeDef",
    "AccessGrantPrincipalUnionTypeDef",
    "AccessGrantSummaryTypeDef",
    "AccessGrantTypeDef",
    "AccessProfileSummaryTypeDef",
    "AccessProfileTypeDef",
    "AlertConditionTypeDef",
    "AlertEvaluationTypeDef",
    "AlertFilterCriteriaTypeDef",
    "AlertRuleQueryTypeDef",
    "AlertStateDataTypeDef",
    "AlertStateInfoTypeDef",
    "AlertSummaryTypeDef",
    "AlertTypeDef",
    "ApiKeyCredentialTypeDef",
    "AwsCredentialsTypeDef",
    "ContributorSummaryTypeDef",
    "CreateAccessGrantInputTypeDef",
    "CreateAccessGrantOutputTypeDef",
    "CreateAccessProfileInputTypeDef",
    "CreateAccessProfileOutputTypeDef",
    "CreateAlertInputTypeDef",
    "CreateAlertOutputTypeDef",
    "CreateDomainAccessGrantForOrganizationInputTypeDef",
    "CreateDomainAccessGrantForOrganizationOutputTypeDef",
    "CreateDomainForOrganizationInputTypeDef",
    "CreateDomainForOrganizationOutputTypeDef",
    "CreateDomainInputTypeDef",
    "CreateDomainOutputTypeDef",
    "CreateIntegrationInputTypeDef",
    "CreateIntegrationOutputTypeDef",
    "CreateOmniDashboardInputTypeDef",
    "CreateOmniDashboardOutputTypeDef",
    "CreateOneTimeDeepLinkCodeInputTypeDef",
    "CreateOneTimeDeepLinkCodeOutputTypeDef",
    "CreateSpaceInputTypeDef",
    "CreateSpaceOutputTypeDef",
    "CreateViewRequestTypeDef",
    "CreateViewResponseTypeDef",
    "DeleteAccessGrantInputTypeDef",
    "DeleteAccessProfileInputTypeDef",
    "DeleteAlertInputTypeDef",
    "DeleteDomainAccessGrantForOrganizationInputTypeDef",
    "DeleteDomainForOrganizationInputTypeDef",
    "DeleteDomainInputTypeDef",
    "DeleteIntegrationInputTypeDef",
    "DeleteOmniDashboardInputTypeDef",
    "DeleteSpaceInputTypeDef",
    "DeleteViewRequestTypeDef",
    "DomainSummaryTypeDef",
    "DomainTypeDef",
    "EdgeFiltersTypeDef",
    "EdgePropertiesTypeDef",
    "EdgeTrafficStatsTypeDef",
    "EdgeTypeDef",
    "EncryptionConfigurationTypeDef",
    "FieldPaginatorTypeDef",
    "FieldTypeDef",
    "GetAccessGrantInputTypeDef",
    "GetAccessGrantOutputTypeDef",
    "GetAccessProfileInputTypeDef",
    "GetAccessProfileOutputTypeDef",
    "GetAlertInputTypeDef",
    "GetAlertOutputTypeDef",
    "GetContextGraphInputPaginateTypeDef",
    "GetContextGraphInputTypeDef",
    "GetContextGraphOutputTypeDef",
    "GetDomainAccessGrantForOrganizationInputTypeDef",
    "GetDomainAccessGrantForOrganizationOutputTypeDef",
    "GetDomainForOrganizationInputTypeDef",
    "GetDomainForOrganizationOutputTypeDef",
    "GetDomainInputTypeDef",
    "GetDomainOutputTypeDef",
    "GetIntegrationInputTypeDef",
    "GetIntegrationOutputTypeDef",
    "GetIntelligenceConfigurationOutputTypeDef",
    "GetOmniDashboardInputTypeDef",
    "GetOmniDashboardOutputTypeDef",
    "GetSpaceCredentialsForOrganizationInputTypeDef",
    "GetSpaceCredentialsForOrganizationOutputTypeDef",
    "GetSpaceInputTypeDef",
    "GetSpaceOutputTypeDef",
    "GetTelemetryQueryResultsRequestPaginateTypeDef",
    "GetTelemetryQueryResultsRequestTypeDef",
    "GetTelemetryQueryResultsResponseTypeDef",
    "GetViewRequestTypeDef",
    "GetViewResponseTypeDef",
    "IdentityCenterConfigurationTypeDef",
    "IdentityProviderConfigurationTypeDef",
    "IntegrationCredentialTypeDef",
    "IntegrationIdentifierTypeDef",
    "IntegrationTypeDef",
    "KeyFilterTypeDef",
    "ListAccessGrantsInputPaginateTypeDef",
    "ListAccessGrantsInputTypeDef",
    "ListAccessGrantsOutputTypeDef",
    "ListAccessProfilesInputPaginateTypeDef",
    "ListAccessProfilesInputTypeDef",
    "ListAccessProfilesOutputTypeDef",
    "ListAlertsInputPaginateTypeDef",
    "ListAlertsInputTypeDef",
    "ListAlertsOutputTypeDef",
    "ListDomainAccessGrantsForOrganizationInputPaginateTypeDef",
    "ListDomainAccessGrantsForOrganizationInputTypeDef",
    "ListDomainAccessGrantsForOrganizationOutputTypeDef",
    "ListDomainsInputPaginateTypeDef",
    "ListDomainsInputTypeDef",
    "ListDomainsOutputTypeDef",
    "ListIntegrationsInputPaginateTypeDef",
    "ListIntegrationsInputTypeDef",
    "ListIntegrationsOutputTypeDef",
    "ListOmniDashboardsInputPaginateTypeDef",
    "ListOmniDashboardsInputTypeDef",
    "ListOmniDashboardsOutputTypeDef",
    "ListSpacesForOrganizationInputPaginateTypeDef",
    "ListSpacesForOrganizationInputTypeDef",
    "ListSpacesForOrganizationOutputTypeDef",
    "ListSpacesInputPaginateTypeDef",
    "ListSpacesInputTypeDef",
    "ListSpacesOutputTypeDef",
    "ListTelemetryFieldsRequestPaginateTypeDef",
    "ListTelemetryFieldsRequestTypeDef",
    "ListTelemetryFieldsResponsePaginatorTypeDef",
    "ListTelemetryFieldsResponseTypeDef",
    "ListTelemetryQuerySessionsRequestPaginateTypeDef",
    "ListTelemetryQuerySessionsRequestTypeDef",
    "ListTelemetryQuerySessionsResponseTypeDef",
    "ListViewsRequestPaginateTypeDef",
    "ListViewsRequestTypeDef",
    "ListViewsResponseTypeDef",
    "LogMetadataTypeDef",
    "MetadataTypeDef",
    "MetricMetadataTypeDef",
    "MetricSemanticsTypeDef",
    "NoDataTypeDef",
    "NodeFiltersTypeDef",
    "NodePropertiesTypeDef",
    "NodeSemanticsTypeDef",
    "NodeTypeDef",
    "NotificationRuleOutputTypeDef",
    "NotificationRuleTypeDef",
    "NotificationRuleUnionTypeDef",
    "NotificationTargetOutputTypeDef",
    "NotificationTargetTypeDef",
    "NotificationTargetUnionTypeDef",
    "NotificationTriggerOutputTypeDef",
    "NotificationTriggerTypeDef",
    "NotificationTriggerUnionTypeDef",
    "OAuthClientCredentialTypeDef",
    "OAuthCodeCredentialTypeDef",
    "OmniDashboardSummaryTypeDef",
    "OmniDashboardTypeDef",
    "OrganizationAccessGrantPrincipalOutputTypeDef",
    "OrganizationAccessGrantPrincipalTypeDef",
    "OrganizationAccessGrantPrincipalUnionTypeDef",
    "OrganizationAccessGrantSummaryTypeDef",
    "OrganizationAccessGrantTypeDef",
    "OrganizationDomainTypeDef",
    "PaginatorConfigTypeDef",
    "PartialResultsTypeDef",
    "PrincipalSearchResultTypeDef",
    "PutIntelligenceConfigurationInputTypeDef",
    "PutIntelligenceConfigurationOutputTypeDef",
    "QueryStatisticsTypeDef",
    "ResourceScopeOutputTypeDef",
    "ResourceScopeTypeDef",
    "ResourceScopeUnionTypeDef",
    "ResponseMetadataTypeDef",
    "RowScopeOutputTypeDef",
    "RowScopeTypeDef",
    "RowScopeUnionTypeDef",
    "RuleTypeDef",
    "ScopedActionsOutputTypeDef",
    "ScopedActionsTypeDef",
    "ScopedActionsUnionTypeDef",
    "SearchPrincipalsInputPaginateTypeDef",
    "SearchPrincipalsInputTypeDef",
    "SearchPrincipalsOutputTypeDef",
    "SessionSummaryTypeDef",
    "SpaceCredentialRequestContextTypeDef",
    "SpaceSummaryTypeDef",
    "SpaceTypeDef",
    "StartTelemetryQueryRequestTypeDef",
    "StartTelemetryQueryResponseTypeDef",
    "StartTelemetryQuerySessionRequestTypeDef",
    "StartTelemetryQuerySessionResponseTypeDef",
    "StopTelemetryQueryRequestTypeDef",
    "StopTelemetryQuerySessionRequestTypeDef",
    "TelemetryRuleTypeDef",
    "TimestampTypeDef",
    "TraceMetadataTypeDef",
    "UpdateAccessProfileInputTypeDef",
    "UpdateAccessProfileOutputTypeDef",
    "UpdateAlertInputTypeDef",
    "UpdateDomainForOrganizationInputTypeDef",
    "UpdateDomainForOrganizationOutputTypeDef",
    "UpdateDomainInputTypeDef",
    "UpdateDomainOutputTypeDef",
    "UpdateIntegrationInputTypeDef",
    "UpdateIntegrationOutputTypeDef",
    "UpdateOmniDashboardInputTypeDef",
    "UpdateOmniDashboardOutputTypeDef",
    "UpdateSpaceInputTypeDef",
    "UpdateSpaceOutputTypeDef",
    "UpdateViewRequestTypeDef",
    "UpdateViewResponseTypeDef",
    "ViewSummaryTypeDef",
)


class AccessGrantPrincipalAttributeTypeDef(TypedDict):
    key: str
    value: str


class AccessProfileSummaryTypeDef(TypedDict):
    profileId: str
    arn: str
    name: str
    description: NotRequired[str]
    profileType: NotRequired[AccessProfileTypeType]


class AccessProfileTypeDef(TypedDict):
    profileId: str
    spaceId: str
    arn: str
    name: str
    createdAt: datetime
    updatedAt: datetime
    description: NotRequired[str]
    assumeStatus: NotRequired[AssumeStatusType]
    profileType: NotRequired[AccessProfileTypeType]


class AlertConditionTypeDef(TypedDict):
    thresholdMode: NotRequired[ThresholdModeType]
    thresholdField: NotRequired[str]
    comparator: NotRequired[ComparatorType]
    warningThreshold: NotRequired[float]
    criticalThreshold: NotRequired[float]


class AlertEvaluationTypeDef(TypedDict):
    intervalSeconds: int
    pendingDurationSeconds: NotRequired[int]
    recoveryDurationSeconds: NotRequired[int]


class AlertFilterCriteriaTypeDef(TypedDict):
    names: NotRequired[Sequence[str]]
    namePrefix: NotRequired[str]
    ids: NotRequired[Sequence[str]]
    stateValue: NotRequired[Sequence[AlertStateType]]
    notificationsEnabled: NotRequired[bool]


class AlertRuleQueryTypeDef(TypedDict):
    language: QueryLanguageType
    expression: str


class AlertStateDataTypeDef(TypedDict):
    thresholdBreached: NotRequired[float]


class ContributorSummaryTypeDef(TypedDict):
    warningCount: NotRequired[int]
    criticalCount: NotRequired[int]


class ApiKeyCredentialTypeDef(TypedDict):
    apiKeyValue: str


class AwsCredentialsTypeDef(TypedDict):
    accessKeyId: str
    secretAccessKey: str
    sessionToken: str
    expiration: datetime


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CreateAccessProfileInputTypeDef(TypedDict):
    spaceId: str
    name: str
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]


class IntegrationTypeDef(TypedDict):
    integrationId: str
    integrationType: IntegrationTypeType
    name: str
    status: IntegrationStatusType
    integrationArn: NotRequired[str]
    authType: NotRequired[AuthTypeType]
    credentialArn: NotRequired[str]
    roleArn: NotRequired[str]
    integrationAttributes: NotRequired[dict[str, str]]
    authorizationUrl: NotRequired[str]
    errorMessage: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]
    scope: NotRequired[ScopeType]


class CreateOmniDashboardInputTypeDef(TypedDict):
    spaceId: str
    name: str
    body: str
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]


class OmniDashboardTypeDef(TypedDict):
    dashboardId: str
    arn: str
    name: str
    body: str
    createdBy: str
    createdAt: datetime
    updatedAt: datetime
    description: NotRequired[str]
    tags: NotRequired[dict[str, str]]


class CreateOneTimeDeepLinkCodeInputTypeDef(TypedDict):
    domainId: str
    ttlSeconds: NotRequired[int]
    redirectUrl: NotRequired[str]


class EncryptionConfigurationTypeDef(TypedDict):
    encryptionStrategy: EncryptionStrategyType
    kmsKeyArn: NotRequired[str]


class CreateViewRequestTypeDef(TypedDict):
    name: str
    definition: str
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]


class DeleteAccessGrantInputTypeDef(TypedDict):
    grantId: str


class DeleteAccessProfileInputTypeDef(TypedDict):
    spaceId: str
    profileId: str


class DeleteAlertInputTypeDef(TypedDict):
    spaceId: str
    alertId: str


class DeleteDomainAccessGrantForOrganizationInputTypeDef(TypedDict):
    grantId: str


class DeleteDomainForOrganizationInputTypeDef(TypedDict):
    domainId: str


class DeleteDomainInputTypeDef(TypedDict):
    domainId: str


class IntegrationIdentifierTypeDef(TypedDict):
    integrationId: NotRequired[str]
    integrationArn: NotRequired[str]
    integrationName: NotRequired[str]


class DeleteOmniDashboardInputTypeDef(TypedDict):
    spaceId: str
    dashboardId: str


class DeleteSpaceInputTypeDef(TypedDict):
    spaceId: str


class DeleteViewRequestTypeDef(TypedDict):
    name: str


class DomainSummaryTypeDef(TypedDict):
    domainId: str
    createdAt: datetime
    updatedAt: datetime
    status: Literal["ACTIVE"]
    domainArn: NotRequired[str]
    name: NotRequired[str]
    identityCenterInstanceArn: NotRequired[str]
    region: NotRequired[str]


class KeyFilterTypeDef(TypedDict):
    key: str
    values: NotRequired[Sequence[str]]


EdgeTrafficStatsTypeDef = TypedDict(
    "EdgeTrafficStatsTypeDef",
    {
        "bytes": NotRequired[int],
        "packets": NotRequired[int],
        "flows": NotRequired[int],
        "sentBytes": NotRequired[int],
        "receivedBytes": NotRequired[int],
    },
)


class FieldPaginatorTypeDef(TypedDict):
    name: str
    children: NotRequired[list[dict[str, Any]]]


class FieldTypeDef(TypedDict):
    name: str
    children: NotRequired[list[dict[str, Any]]]


class GetAccessGrantInputTypeDef(TypedDict):
    grantId: str


class GetAccessProfileInputTypeDef(TypedDict):
    spaceId: str
    profileId: str


class GetAlertInputTypeDef(TypedDict):
    spaceId: str
    alertId: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class GetDomainAccessGrantForOrganizationInputTypeDef(TypedDict):
    grantId: str


class GetDomainForOrganizationInputTypeDef(TypedDict):
    domainId: str


class GetDomainInputTypeDef(TypedDict):
    domainId: str


class GetOmniDashboardInputTypeDef(TypedDict):
    spaceId: str
    dashboardId: str


class SpaceCredentialRequestContextTypeDef(TypedDict):
    spaceId: NotRequired[str]
    domainId: NotRequired[str]
    targetAccountId: NotRequired[str]


class GetSpaceInputTypeDef(TypedDict):
    spaceId: str


class GetTelemetryQueryResultsRequestTypeDef(TypedDict):
    queryId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class GetViewRequestTypeDef(TypedDict):
    name: str


class IdentityCenterConfigurationTypeDef(TypedDict):
    identityCenterInstanceArn: NotRequired[str]


class OAuthClientCredentialTypeDef(TypedDict):
    clientId: str
    clientSecret: str
    providerId: NotRequired[str]


class OAuthCodeCredentialTypeDef(TypedDict):
    authCode: str


class ListAccessGrantsInputTypeDef(TypedDict):
    domainId: NotRequired[str]
    spaceId: NotRequired[str]
    principalId: NotRequired[str]
    principalType: NotRequired[AccessGrantPrincipalTypeType]
    permission: NotRequired[AccessGrantPermissionType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListAccessProfilesInputTypeDef(TypedDict):
    spaceId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListDomainAccessGrantsForOrganizationInputTypeDef(TypedDict):
    domainId: NotRequired[str]
    principalId: NotRequired[str]
    principalType: NotRequired[OrganizationGrantPrincipalTypeType]
    permission: NotRequired[Literal["ADMIN"]]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListDomainsInputTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListIntegrationsInputTypeDef(TypedDict):
    integrationType: NotRequired[IntegrationTypeType]
    status: NotRequired[IntegrationStatusType]
    name: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListOmniDashboardsInputTypeDef(TypedDict):
    spaceId: str
    namePrefix: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class OmniDashboardSummaryTypeDef(TypedDict):
    dashboardId: str
    arn: str
    name: str
    createdBy: str
    createdAt: datetime
    updatedAt: datetime
    description: NotRequired[str]
    tags: NotRequired[dict[str, str]]


class ListSpacesForOrganizationInputTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class SpaceSummaryTypeDef(TypedDict):
    spaceId: str
    name: str
    spaceArn: str
    region: str
    ownerAccountId: str
    status: SpaceStatusType
    createdAt: datetime
    updatedAt: datetime
    domainArn: NotRequired[str]
    statusReason: NotRequired[str]


class ListSpacesInputTypeDef(TypedDict):
    domainId: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListTelemetryQuerySessionsRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class SessionSummaryTypeDef(TypedDict):
    sessionId: str
    createdAt: NotRequired[datetime]
    lastActivityAt: NotRequired[datetime]
    sessionName: NotRequired[str]


ListViewsRequestTypeDef = TypedDict(
    "ListViewsRequestTypeDef",
    {
        "type": NotRequired[ViewTypeType],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ViewSummaryTypeDef = TypedDict(
    "ViewSummaryTypeDef",
    {
        "name": str,
        "type": ViewTypeType,
        "createdAt": datetime,
        "updatedAt": datetime,
        "description": NotRequired[str],
    },
)


class LogMetadataTypeDef(TypedDict):
    attributes: NotRequired[dict[str, str]]


class NodeSemanticsTypeDef(TypedDict):
    purpose: NotRequired[str]
    language: NotRequired[str]
    framework: NotRequired[str]
    kind: NotRequired[str]
    repository: NotRequired[str]


class TraceMetadataTypeDef(TypedDict):
    attributes: NotRequired[dict[str, str]]


class MetricSemanticsTypeDef(TypedDict):
    description: NotRequired[str]
    unit: NotRequired[str]


class NoDataTypeDef(TypedDict):
    treatAs: AlertStateType


class NodePropertiesTypeDef(TypedDict):
    region: NotRequired[str]
    cloudProvider: NotRequired[str]
    sourceAccountId: NotRequired[str]
    namespace: NotRequired[str]
    category: NotRequired[NodeCategoryType]
    stage: NotRequired[str]


NotificationTargetOutputTypeDef = TypedDict(
    "NotificationTargetOutputTypeDef",
    {
        "type": NotificationTargetTypeType,
        "arn": str,
        "metadata": NotRequired[dict[str, str]],
    },
)


class NotificationTriggerOutputTypeDef(TypedDict):
    stateValues: NotRequired[list[AlertStateType]]


NotificationTargetTypeDef = TypedDict(
    "NotificationTargetTypeDef",
    {
        "type": NotificationTargetTypeType,
        "arn": str,
        "metadata": NotRequired[Mapping[str, str]],
    },
)


class NotificationTriggerTypeDef(TypedDict):
    stateValues: NotRequired[Sequence[AlertStateType]]


class PartialResultsTypeDef(TypedDict):
    partialResultsDetected: NotRequired[bool]


class PrincipalSearchResultTypeDef(TypedDict):
    principalId: str
    principalType: PrincipalTypeType
    displayName: str
    userName: NotRequired[str]
    description: NotRequired[str]


class PutIntelligenceConfigurationInputTypeDef(TypedDict):
    kmsKeyArn: NotRequired[str]
    removeKmsKey: NotRequired[bool]
    clientToken: NotRequired[str]


RowScopeOutputTypeDef = TypedDict(
    "RowScopeOutputTypeDef",
    {
        "field": str,
        "operator": Literal["IN"],
        "values": list[str],
    },
)
RowScopeTypeDef = TypedDict(
    "RowScopeTypeDef",
    {
        "field": str,
        "operator": Literal["IN"],
        "values": Sequence[str],
    },
)


class SearchPrincipalsInputTypeDef(TypedDict):
    domainId: str
    searchQuery: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class StartTelemetryQueryRequestTypeDef(TypedDict):
    queryString: str
    sessionId: str


class StartTelemetryQuerySessionRequestTypeDef(TypedDict):
    sessionName: NotRequired[str]


class StopTelemetryQueryRequestTypeDef(TypedDict):
    queryId: str


class StopTelemetryQuerySessionRequestTypeDef(TypedDict):
    sessionId: str


class UpdateAccessProfileInputTypeDef(TypedDict):
    spaceId: str
    profileId: str
    name: NotRequired[str]
    description: NotRequired[str]


class UpdateOmniDashboardInputTypeDef(TypedDict):
    spaceId: str
    dashboardId: str
    body: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]


class UpdateViewRequestTypeDef(TypedDict):
    name: str
    definition: NotRequired[str]
    description: NotRequired[str]


class AccessGrantPrincipalOutputTypeDef(TypedDict):
    principalType: AccessGrantPrincipalTypeType
    principalId: NotRequired[str]
    principalAttributes: NotRequired[list[AccessGrantPrincipalAttributeTypeDef]]


class AccessGrantPrincipalTypeDef(TypedDict):
    principalType: AccessGrantPrincipalTypeType
    principalId: NotRequired[str]
    principalAttributes: NotRequired[Sequence[AccessGrantPrincipalAttributeTypeDef]]


class OrganizationAccessGrantPrincipalOutputTypeDef(TypedDict):
    principalType: OrganizationGrantPrincipalTypeType
    principalId: NotRequired[str]
    principalAttributes: NotRequired[list[AccessGrantPrincipalAttributeTypeDef]]


class OrganizationAccessGrantPrincipalTypeDef(TypedDict):
    principalType: OrganizationGrantPrincipalTypeType
    principalId: NotRequired[str]
    principalAttributes: NotRequired[Sequence[AccessGrantPrincipalAttributeTypeDef]]


class ListAlertsInputTypeDef(TypedDict):
    spaceId: str
    filterCriteria: NotRequired[AlertFilterCriteriaTypeDef]
    sortBy: NotRequired[AlertSortFieldType]
    sortOrder: NotRequired[AlertSortOrderType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class AlertStateInfoTypeDef(TypedDict):
    value: AlertStateType
    transitionedAt: NotRequired[datetime]
    contributorSummary: NotRequired[ContributorSummaryTypeDef]
    data: NotRequired[AlertStateDataTypeDef]


class CreateAccessProfileOutputTypeDef(TypedDict):
    accessProfile: AccessProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateOneTimeDeepLinkCodeOutputTypeDef(TypedDict):
    code: str
    deepLinkUrl: str
    expiresAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


CreateViewResponseTypeDef = TypedDict(
    "CreateViewResponseTypeDef",
    {
        "name": str,
        "type": ViewTypeType,
        "description": str,
        "definition": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class GetAccessProfileOutputTypeDef(TypedDict):
    accessProfile: AccessProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetIntelligenceConfigurationOutputTypeDef(TypedDict):
    accountId: str
    kmsKeyArn: str
    updatedAt: datetime
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GetSpaceCredentialsForOrganizationOutputTypeDef(TypedDict):
    credentials: AwsCredentialsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


GetViewResponseTypeDef = TypedDict(
    "GetViewResponseTypeDef",
    {
        "name": str,
        "type": ViewTypeType,
        "description": str,
        "definition": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class ListAccessProfilesOutputTypeDef(TypedDict):
    items: list[AccessProfileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class PutIntelligenceConfigurationOutputTypeDef(TypedDict):
    accountId: str
    kmsKeyArn: str
    updatedAt: datetime
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class StartTelemetryQueryResponseTypeDef(TypedDict):
    queryId: str
    sessionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartTelemetryQuerySessionResponseTypeDef(TypedDict):
    sessionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAccessProfileOutputTypeDef(TypedDict):
    accessProfile: AccessProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


UpdateViewResponseTypeDef = TypedDict(
    "UpdateViewResponseTypeDef",
    {
        "name": str,
        "type": ViewTypeType,
        "description": str,
        "definition": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class CreateIntegrationOutputTypeDef(TypedDict):
    integration: IntegrationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetIntegrationOutputTypeDef(TypedDict):
    integration: IntegrationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListIntegrationsOutputTypeDef(TypedDict):
    items: list[IntegrationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateIntegrationOutputTypeDef(TypedDict):
    integration: IntegrationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateOmniDashboardOutputTypeDef(TypedDict):
    omniDashboard: OmniDashboardTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetOmniDashboardOutputTypeDef(TypedDict):
    omniDashboard: OmniDashboardTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateOmniDashboardOutputTypeDef(TypedDict):
    omniDashboard: OmniDashboardTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSpaceInputTypeDef(TypedDict):
    name: str
    domainId: str
    dataAccessRoleArn: str
    agentCoreEvaluationRoleArn: NotRequired[str]
    encryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]


class SpaceTypeDef(TypedDict):
    spaceId: str
    name: str
    spaceArn: str
    region: str
    ownerAccountId: str
    dataAccessRoleArn: str
    createdAt: datetime
    updatedAt: datetime
    status: SpaceStatusType
    domainArn: NotRequired[str]
    agentCoreEvaluationRoleArn: NotRequired[str]
    statusReason: NotRequired[str]
    encryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]


class UpdateSpaceInputTypeDef(TypedDict):
    spaceId: str
    name: NotRequired[str]
    encryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]


class DeleteIntegrationInputTypeDef(TypedDict):
    identifier: IntegrationIdentifierTypeDef


class GetIntegrationInputTypeDef(TypedDict):
    identifier: IntegrationIdentifierTypeDef


class ListDomainsOutputTypeDef(TypedDict):
    items: list[DomainSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


EdgeFiltersTypeDef = TypedDict(
    "EdgeFiltersTypeDef",
    {
        "edgeId": NotRequired[str],
        "from": NotRequired[str],
        "to": NotRequired[str],
        "edgeType": NotRequired[EdgeTypeType],
        "operations": NotRequired[Sequence[str]],
        "telemetryAttributes": NotRequired[Sequence[KeyFilterTypeDef]],
        "sources": NotRequired[Sequence[SourceType]],
    },
)


class NodeFiltersTypeDef(TypedDict):
    nodeId: NotRequired[str]
    nodeType: NotRequired[NodeTypeType]
    name: NotRequired[str]
    tags: NotRequired[Sequence[KeyFilterTypeDef]]
    telemetryAttributes: NotRequired[Sequence[KeyFilterTypeDef]]
    region: NotRequired[Sequence[str]]
    cloudProvider: NotRequired[Sequence[str]]
    sourceAccountId: NotRequired[Sequence[str]]
    namespace: NotRequired[Sequence[str]]
    category: NotRequired[Sequence[NodeCategoryType]]
    stage: NotRequired[Sequence[str]]
    sources: NotRequired[Sequence[SourceType]]


class EdgePropertiesTypeDef(TypedDict):
    protocol: NotRequired[str]
    sourcePort: NotRequired[str]
    destinationPort: NotRequired[str]
    blocked: NotRequired[bool]
    errorCode: NotRequired[str]
    httpStatusCode: NotRequired[str]
    httpMethod: NotRequired[str]
    serviceInitiated: NotRequired[bool]
    trafficStats: NotRequired[EdgeTrafficStatsTypeDef]


class ListTelemetryFieldsResponsePaginatorTypeDef(TypedDict):
    fields: list[FieldPaginatorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTelemetryFieldsResponseTypeDef(TypedDict):
    fields: list[FieldTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetTelemetryQueryResultsRequestPaginateTypeDef(TypedDict):
    queryId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAccessGrantsInputPaginateTypeDef(TypedDict):
    domainId: NotRequired[str]
    spaceId: NotRequired[str]
    principalId: NotRequired[str]
    principalType: NotRequired[AccessGrantPrincipalTypeType]
    permission: NotRequired[AccessGrantPermissionType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAccessProfilesInputPaginateTypeDef(TypedDict):
    spaceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAlertsInputPaginateTypeDef(TypedDict):
    spaceId: str
    filterCriteria: NotRequired[AlertFilterCriteriaTypeDef]
    sortBy: NotRequired[AlertSortFieldType]
    sortOrder: NotRequired[AlertSortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDomainAccessGrantsForOrganizationInputPaginateTypeDef(TypedDict):
    domainId: NotRequired[str]
    principalId: NotRequired[str]
    principalType: NotRequired[OrganizationGrantPrincipalTypeType]
    permission: NotRequired[Literal["ADMIN"]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDomainsInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListIntegrationsInputPaginateTypeDef(TypedDict):
    integrationType: NotRequired[IntegrationTypeType]
    status: NotRequired[IntegrationStatusType]
    name: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListOmniDashboardsInputPaginateTypeDef(TypedDict):
    spaceId: str
    namePrefix: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSpacesForOrganizationInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSpacesInputPaginateTypeDef(TypedDict):
    domainId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTelemetryQuerySessionsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListViewsRequestPaginateTypeDef = TypedDict(
    "ListViewsRequestPaginateTypeDef",
    {
        "type": NotRequired[ViewTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class SearchPrincipalsInputPaginateTypeDef(TypedDict):
    domainId: str
    searchQuery: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTelemetryFieldsRequestPaginateTypeDef(TypedDict):
    dataSetName: str
    telemetryType: NotRequired[TelemetryTypeType]
    startTime: NotRequired[TimestampTypeDef]
    endTime: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTelemetryFieldsRequestTypeDef(TypedDict):
    dataSetName: str
    telemetryType: NotRequired[TelemetryTypeType]
    startTime: NotRequired[TimestampTypeDef]
    endTime: NotRequired[TimestampTypeDef]
    nextToken: NotRequired[str]


class GetSpaceCredentialsForOrganizationInputTypeDef(TypedDict):
    context: SpaceCredentialRequestContextTypeDef
    credentialType: Literal["SPACE_OPERATION"]


class IdentityProviderConfigurationTypeDef(TypedDict):
    identityCenterConfiguration: NotRequired[IdentityCenterConfigurationTypeDef]


class IntegrationCredentialTypeDef(TypedDict):
    oauthCodeCredential: NotRequired[OAuthCodeCredentialTypeDef]
    oauthClientCredential: NotRequired[OAuthClientCredentialTypeDef]
    apiKeyCredential: NotRequired[ApiKeyCredentialTypeDef]


class ListOmniDashboardsOutputTypeDef(TypedDict):
    items: list[OmniDashboardSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListSpacesForOrganizationOutputTypeDef(TypedDict):
    items: list[SpaceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListSpacesOutputTypeDef(TypedDict):
    items: list[SpaceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTelemetryQuerySessionsResponseTypeDef(TypedDict):
    sessions: list[SessionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListViewsResponseTypeDef(TypedDict):
    items: list[ViewSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class MetricMetadataTypeDef(TypedDict):
    name: NotRequired[str]
    namespace: NotRequired[str]
    preferredStat: NotRequired[str]
    metricType: NotRequired[str]
    attributes: NotRequired[dict[str, str]]
    semantics: NotRequired[MetricSemanticsTypeDef]


class TelemetryRuleTypeDef(TypedDict):
    query: NotRequired[AlertRuleQueryTypeDef]
    condition: NotRequired[AlertConditionTypeDef]
    evaluation: NotRequired[AlertEvaluationTypeDef]
    noData: NotRequired[NoDataTypeDef]


class NotificationRuleOutputTypeDef(TypedDict):
    trigger: NotificationTriggerOutputTypeDef
    target: NotificationTargetOutputTypeDef


NotificationTargetUnionTypeDef = Union[NotificationTargetTypeDef, NotificationTargetOutputTypeDef]
NotificationTriggerUnionTypeDef = Union[
    NotificationTriggerTypeDef, NotificationTriggerOutputTypeDef
]


class QueryStatisticsTypeDef(TypedDict):
    bytesScanned: NotRequired[float]
    percentComplete: NotRequired[int]
    recordsScanned: NotRequired[int]
    recordsMatched: NotRequired[int]
    partialResults: NotRequired[PartialResultsTypeDef]


class SearchPrincipalsOutputTypeDef(TypedDict):
    results: list[PrincipalSearchResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ResourceScopeOutputTypeDef(TypedDict):
    resourceType: str
    resourceArns: NotRequired[list[str]]
    tags: NotRequired[dict[str, str]]
    signalTypes: NotRequired[list[SignalTypeType]]
    rowScopeGroups: NotRequired[list[list[RowScopeOutputTypeDef]]]


RowScopeUnionTypeDef = Union[RowScopeTypeDef, RowScopeOutputTypeDef]


class AccessGrantSummaryTypeDef(TypedDict):
    grantId: str
    grantArn: str
    domainId: str
    principal: AccessGrantPrincipalOutputTypeDef
    permission: AccessGrantPermissionType
    grantType: AccessGrantTypeType
    spaceId: str
    name: NotRequired[str]


AccessGrantPrincipalUnionTypeDef = Union[
    AccessGrantPrincipalTypeDef, AccessGrantPrincipalOutputTypeDef
]


class OrganizationAccessGrantSummaryTypeDef(TypedDict):
    grantId: str
    grantArn: str
    domainId: str
    principal: OrganizationAccessGrantPrincipalOutputTypeDef
    permission: Literal["ADMIN"]
    grantType: AccessGrantTypeType
    createdAt: datetime
    updatedAt: datetime
    name: NotRequired[str]


class OrganizationAccessGrantTypeDef(TypedDict):
    grantId: str
    grantArn: str
    domainId: str
    principal: OrganizationAccessGrantPrincipalOutputTypeDef
    permission: Literal["ADMIN"]
    grantType: AccessGrantTypeType
    createdBy: str
    createdAt: datetime
    updatedAt: datetime
    name: NotRequired[str]


OrganizationAccessGrantPrincipalUnionTypeDef = Union[
    OrganizationAccessGrantPrincipalTypeDef, OrganizationAccessGrantPrincipalOutputTypeDef
]


class AlertSummaryTypeDef(TypedDict):
    name: str
    state: AlertStateInfoTypeDef
    createdAt: datetime
    updatedAt: datetime
    alertArn: str
    alertId: NotRequired[str]
    spaceId: NotRequired[str]
    profileId: NotRequired[str]
    notificationStatus: NotRequired[NotificationStatusType]


class CreateSpaceOutputTypeDef(TypedDict):
    space: SpaceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetSpaceOutputTypeDef(TypedDict):
    space: SpaceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSpaceOutputTypeDef(TypedDict):
    space: SpaceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetContextGraphInputPaginateTypeDef(TypedDict):
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    nodeFilters: NotRequired[NodeFiltersTypeDef]
    edgeFilters: NotRequired[EdgeFiltersTypeDef]
    depth: NotRequired[int]
    maxEdgesPerNode: NotRequired[int]
    includeMetadata: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetContextGraphInputTypeDef(TypedDict):
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    nodeFilters: NotRequired[NodeFiltersTypeDef]
    edgeFilters: NotRequired[EdgeFiltersTypeDef]
    depth: NotRequired[int]
    maxResults: NotRequired[int]
    maxEdgesPerNode: NotRequired[int]
    includeMetadata: NotRequired[bool]
    nextToken: NotRequired[str]


class CreateDomainForOrganizationInputTypeDef(TypedDict):
    name: str
    identityProviders: Sequence[IdentityProviderType]
    domainAccessRoleArn: str
    identityProviderConfiguration: NotRequired[IdentityProviderConfigurationTypeDef]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]


class CreateDomainInputTypeDef(TypedDict):
    name: str
    identityProviders: Sequence[IdentityProviderType]
    identityProviderConfiguration: NotRequired[IdentityProviderConfigurationTypeDef]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]


class DomainTypeDef(TypedDict):
    domainId: str
    domainArn: str
    identityProviders: list[IdentityProviderType]
    domainEndpointUrl: str
    region: str
    createdAt: datetime
    updatedAt: datetime
    status: Literal["ACTIVE"]
    name: NotRequired[str]
    identityProviderConfiguration: NotRequired[IdentityProviderConfigurationTypeDef]
    customEndpointUrls: NotRequired[list[str]]
    identityCenterApplicationArn: NotRequired[str]


class OrganizationDomainTypeDef(TypedDict):
    domainId: str
    domainArn: str
    domainEndpointUrl: str
    organizationId: str
    ownerAccountId: str
    identityProviders: list[IdentityProviderType]
    region: str
    status: Literal["ACTIVE"]
    createdAt: datetime
    updatedAt: datetime
    name: NotRequired[str]
    customEndpointUrls: NotRequired[list[str]]
    identityProviderConfiguration: NotRequired[IdentityProviderConfigurationTypeDef]
    identityCenterApplicationArn: NotRequired[str]
    domainAccessRoleArn: NotRequired[str]


class UpdateDomainForOrganizationInputTypeDef(TypedDict):
    domainId: str
    name: NotRequired[str]
    identityProviders: NotRequired[Sequence[IdentityProviderType]]
    identityProviderConfiguration: NotRequired[IdentityProviderConfigurationTypeDef]


class UpdateDomainInputTypeDef(TypedDict):
    domainId: str
    name: NotRequired[str]
    identityProviders: NotRequired[Sequence[IdentityProviderType]]
    identityProviderConfiguration: NotRequired[IdentityProviderConfigurationTypeDef]


class CreateIntegrationInputTypeDef(TypedDict):
    integrationType: IntegrationTypeType
    name: str
    credential: NotRequired[IntegrationCredentialTypeDef]
    integrationAttributes: NotRequired[Mapping[str, str]]
    roleArn: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]


class UpdateIntegrationInputTypeDef(TypedDict):
    identifier: IntegrationIdentifierTypeDef
    credential: NotRequired[IntegrationCredentialTypeDef]
    integrationAttributes: NotRequired[Mapping[str, str]]
    roleArn: NotRequired[str]


class MetadataTypeDef(TypedDict):
    metrics: NotRequired[list[MetricMetadataTypeDef]]
    semantics: NotRequired[NodeSemanticsTypeDef]
    logs: NotRequired[list[LogMetadataTypeDef]]
    traces: NotRequired[list[TraceMetadataTypeDef]]


class RuleTypeDef(TypedDict):
    telemetryRule: NotRequired[TelemetryRuleTypeDef]


class NotificationRuleTypeDef(TypedDict):
    trigger: NotificationTriggerUnionTypeDef
    target: NotificationTargetUnionTypeDef


class GetTelemetryQueryResultsResponseTypeDef(TypedDict):
    status: QueryStatusType
    rows: list[dict[str, str]]
    statistics: QueryStatisticsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ScopedActionsOutputTypeDef(TypedDict):
    actions: list[str]
    resources: NotRequired[list[ResourceScopeOutputTypeDef]]
    contextConditions: NotRequired[dict[str, list[str]]]


class ResourceScopeTypeDef(TypedDict):
    resourceType: str
    resourceArns: NotRequired[Sequence[str]]
    tags: NotRequired[Mapping[str, str]]
    signalTypes: NotRequired[Sequence[SignalTypeType]]
    rowScopeGroups: NotRequired[Sequence[Sequence[RowScopeUnionTypeDef]]]


class ListAccessGrantsOutputTypeDef(TypedDict):
    items: list[AccessGrantSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListDomainAccessGrantsForOrganizationOutputTypeDef(TypedDict):
    items: list[OrganizationAccessGrantSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateDomainAccessGrantForOrganizationOutputTypeDef(TypedDict):
    accessGrant: OrganizationAccessGrantTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetDomainAccessGrantForOrganizationOutputTypeDef(TypedDict):
    accessGrant: OrganizationAccessGrantTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDomainAccessGrantForOrganizationInputTypeDef(TypedDict):
    domainId: str
    name: str
    principal: OrganizationAccessGrantPrincipalUnionTypeDef
    permission: Literal["ADMIN"]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]


class ListAlertsOutputTypeDef(TypedDict):
    items: list[AlertSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateDomainOutputTypeDef(TypedDict):
    domain: DomainTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetDomainOutputTypeDef(TypedDict):
    domain: DomainTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDomainOutputTypeDef(TypedDict):
    domain: DomainTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDomainForOrganizationOutputTypeDef(TypedDict):
    organizationDomain: OrganizationDomainTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetDomainForOrganizationOutputTypeDef(TypedDict):
    organizationDomain: OrganizationDomainTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDomainForOrganizationOutputTypeDef(TypedDict):
    organizationDomain: OrganizationDomainTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


EdgeTypeDef = TypedDict(
    "EdgeTypeDef",
    {
        "edgeId": NotRequired[str],
        "from": NotRequired[str],
        "to": NotRequired[str],
        "edgeType": NotRequired[EdgeTypeType],
        "operations": NotRequired[list[str]],
        "edgeProperties": NotRequired[EdgePropertiesTypeDef],
        "telemetryAttributes": NotRequired[dict[str, str]],
        "signalTypes": NotRequired[list[SignalType]],
        "sources": NotRequired[list[SourceType]],
        "metadata": NotRequired[MetadataTypeDef],
        "firstObservedAt": NotRequired[datetime],
        "lastObservedAt": NotRequired[datetime],
    },
)


class AlertTypeDef(TypedDict):
    name: str
    accountId: str
    rule: RuleTypeDef
    createdAt: datetime
    updatedAt: datetime
    alertArn: str
    alertId: NotRequired[str]
    description: NotRequired[str]
    spaceId: NotRequired[str]
    profileId: NotRequired[str]
    notificationStatus: NotRequired[NotificationStatusType]
    state: NotRequired[AlertStateInfoTypeDef]
    notificationRules: NotRequired[list[NotificationRuleOutputTypeDef]]


NotificationRuleUnionTypeDef = Union[NotificationRuleTypeDef, NotificationRuleOutputTypeDef]


class AccessGrantTypeDef(TypedDict):
    grantId: str
    grantArn: str
    accountId: str
    domainId: str
    principal: AccessGrantPrincipalOutputTypeDef
    permission: AccessGrantPermissionType
    grantType: AccessGrantTypeType
    createdBy: str
    createdAt: datetime
    updatedAt: datetime
    spaceId: str
    name: NotRequired[str]
    scopedActions: NotRequired[list[ScopedActionsOutputTypeDef]]


ResourceScopeUnionTypeDef = Union[ResourceScopeTypeDef, ResourceScopeOutputTypeDef]


class NodeTypeDef(TypedDict):
    nodeId: NotRequired[str]
    nodeType: NotRequired[NodeTypeType]
    name: NotRequired[str]
    alternateNames: NotRequired[list[str]]
    tags: NotRequired[dict[str, str]]
    nodeProperties: NotRequired[NodePropertiesTypeDef]
    telemetryAttributes: NotRequired[dict[str, str]]
    operationDetails: NotRequired[dict[str, list[dict[str, str]]]]
    signalTypes: NotRequired[list[SignalType]]
    sources: NotRequired[list[SourceType]]
    metadata: NotRequired[MetadataTypeDef]
    firstObservedAt: NotRequired[datetime]
    lastObservedAt: NotRequired[datetime]
    edges: NotRequired[list[EdgeTypeDef]]


class CreateAlertOutputTypeDef(TypedDict):
    alertArn: str
    alert: AlertTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetAlertOutputTypeDef(TypedDict):
    alert: AlertTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAlertInputTypeDef(TypedDict):
    spaceId: str
    profileId: str
    name: str
    rule: RuleTypeDef
    description: NotRequired[str]
    notificationsEnabled: NotRequired[bool]
    tags: NotRequired[Mapping[str, str]]
    notificationRules: NotRequired[Sequence[NotificationRuleUnionTypeDef]]
    clientToken: NotRequired[str]


class UpdateAlertInputTypeDef(TypedDict):
    spaceId: str
    alertId: str
    profileId: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]
    rule: NotRequired[RuleTypeDef]
    notificationsEnabled: NotRequired[bool]
    notificationRules: NotRequired[Sequence[NotificationRuleUnionTypeDef]]


class CreateAccessGrantOutputTypeDef(TypedDict):
    accessGrant: AccessGrantTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetAccessGrantOutputTypeDef(TypedDict):
    accessGrant: AccessGrantTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ScopedActionsTypeDef(TypedDict):
    actions: Sequence[str]
    resources: NotRequired[Sequence[ResourceScopeUnionTypeDef]]
    contextConditions: NotRequired[Mapping[str, Sequence[str]]]


class GetContextGraphOutputTypeDef(TypedDict):
    nodes: list[NodeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


ScopedActionsUnionTypeDef = Union[ScopedActionsTypeDef, ScopedActionsOutputTypeDef]


class CreateAccessGrantInputTypeDef(TypedDict):
    domainId: str
    spaceId: str
    name: str
    principal: AccessGrantPrincipalUnionTypeDef
    permission: AccessGrantPermissionType
    scopedActions: NotRequired[Sequence[ScopedActionsUnionTypeDef]]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]
