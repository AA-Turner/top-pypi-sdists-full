"""
Type annotations for network-security-manager service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_network_security_manager/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_network_security_manager.type_defs import AccountSetOutputTypeDef

    data: AccountSetOutputTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Union

from .literals import (
    AdminAccountStatusType,
    EntityStatusFilterType,
    EntityStatusType,
    ExistingCustomerWebACLResolutionType,
    IpAddressTypeType,
    PolicyFirewallTypeType,
    ResourceTypeType,
    RuleTypeType,
    SchemeType,
    ScopeResourceTypeType,
    ServiceResourceTypeType,
    SynchronizationStatusType,
    WAFConfigDataTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AccountFilterOutputTypeDef",
    "AccountFilterTypeDef",
    "AccountReferenceTypeDef",
    "AccountSetOutputTypeDef",
    "AccountSetTypeDef",
    "AdminAccountDetailsTypeDef",
    "AdminAccountSummaryTypeDef",
    "AdminFirewallTypeScopeOutputTypeDef",
    "AdminFirewallTypeScopeTypeDef",
    "AdminFirewallTypeScopeUnionTypeDef",
    "AdminScopeFilterInputTypeDef",
    "AdminScopeFilterTypeDef",
    "AdminScopeInputTypeDef",
    "AdminScopeSelectionInputTypeDef",
    "AdminScopeSelectionTypeDef",
    "AdminScopeTypeDef",
    "AlbConfigurationTypeDef",
    "AssociatedPolicyTypeDef",
    "AssociatedRuleTypeDef",
    "AssociatedScopeTypeDef",
    "AssociatedTemplateOrRuleTypeDef",
    "ConfigurationIssueTypeDef",
    "CreateDeploymentInputTypeDef",
    "CreateDeploymentOutputTypeDef",
    "CreateDeploymentSnapshotInputTypeDef",
    "CreateDeploymentSnapshotOutputTypeDef",
    "CreatePolicyInputTypeDef",
    "CreatePolicyOutputTypeDef",
    "CreatePolicySnapshotInputTypeDef",
    "CreatePolicySnapshotOutputTypeDef",
    "CreateRuleInputTypeDef",
    "CreateRuleOutputTypeDef",
    "CreateRuleSnapshotInputTypeDef",
    "CreateRuleSnapshotOutputTypeDef",
    "CreateScopeInputTypeDef",
    "CreateScopeOutputTypeDef",
    "CreateScopeSnapshotInputTypeDef",
    "CreateScopeSnapshotOutputTypeDef",
    "CreateTemplateInputTypeDef",
    "CreateTemplateOutputTypeDef",
    "CreateTemplateSnapshotInputTypeDef",
    "CreateTemplateSnapshotOutputTypeDef",
    "DeleteAdminAccountRequestTypeDef",
    "DeleteDeploymentInputTypeDef",
    "DeletePolicyInputTypeDef",
    "DeleteRuleInputTypeDef",
    "DeleteScopeInputTypeDef",
    "DeleteTemplateInputTypeDef",
    "DeploymentConfigurationTypeDef",
    "DeploymentCoverageEntryTypeDef",
    "DeploymentSummaryTypeDef",
    "DeploymentWarningEntryTypeDef",
    "EmptyResponseMetadataTypeDef",
    "FirewallSyncReasonTypeDef",
    "GenerateRuleConfigurationRequestTypeDef",
    "GenerateRuleConfigurationResponseTypeDef",
    "GetAdminAccountRequestTypeDef",
    "GetAdminAccountResponseTypeDef",
    "GetDeploymentInputTypeDef",
    "GetDeploymentOutputTypeDef",
    "GetPolicyInputTypeDef",
    "GetPolicyOutputTypeDef",
    "GetRuleInputTypeDef",
    "GetRuleOutputTypeDef",
    "GetScopeInputTypeDef",
    "GetScopeOutputTypeDef",
    "GetTemplateInputTypeDef",
    "GetTemplateOutputTypeDef",
    "InvalidFirewallReasonsTypeDef",
    "ListAdminAccountsRequestPaginateTypeDef",
    "ListAdminAccountsRequestTypeDef",
    "ListAdminAccountsResponseTypeDef",
    "ListAggregateResourceSynchronizationStatusesInputPaginateTypeDef",
    "ListAggregateResourceSynchronizationStatusesInputTypeDef",
    "ListAggregateResourceSynchronizationStatusesOutputTypeDef",
    "ListDeploymentSnapshotsInputPaginateTypeDef",
    "ListDeploymentSnapshotsInputTypeDef",
    "ListDeploymentSnapshotsOutputTypeDef",
    "ListDeploymentsInputPaginateTypeDef",
    "ListDeploymentsInputTypeDef",
    "ListDeploymentsOutputTypeDef",
    "ListPoliciesInputPaginateTypeDef",
    "ListPoliciesInputTypeDef",
    "ListPoliciesOutputTypeDef",
    "ListPolicySnapshotsInputPaginateTypeDef",
    "ListPolicySnapshotsInputTypeDef",
    "ListPolicySnapshotsOutputTypeDef",
    "ListResourceAssociationsInputPaginateTypeDef",
    "ListResourceAssociationsInputTypeDef",
    "ListResourceAssociationsOutputTypeDef",
    "ListResourceSynchronizationStatusesInputPaginateTypeDef",
    "ListResourceSynchronizationStatusesInputTypeDef",
    "ListResourceSynchronizationStatusesOutputTypeDef",
    "ListRuleSnapshotsInputPaginateTypeDef",
    "ListRuleSnapshotsInputTypeDef",
    "ListRuleSnapshotsOutputTypeDef",
    "ListRulesInputPaginateTypeDef",
    "ListRulesInputTypeDef",
    "ListRulesOutputTypeDef",
    "ListScopeSnapshotsInputPaginateTypeDef",
    "ListScopeSnapshotsInputTypeDef",
    "ListScopeSnapshotsOutputTypeDef",
    "ListScopesInputPaginateTypeDef",
    "ListScopesInputTypeDef",
    "ListScopesOutputTypeDef",
    "ListTagsForResourceInputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "ListTemplateSnapshotsInputPaginateTypeDef",
    "ListTemplateSnapshotsInputTypeDef",
    "ListTemplateSnapshotsOutputTypeDef",
    "ListTemplatesInputPaginateTypeDef",
    "ListTemplatesInputTypeDef",
    "ListTemplatesOutputTypeDef",
    "NotVisibleMarkerTypeDef",
    "OrganizationalUnitReferenceTypeDef",
    "OutOfSyncReasonsViewTypeDef",
    "PaginatorConfigTypeDef",
    "PolicyConfigurationTypeDef",
    "PolicyReferenceTypeDef",
    "PolicySummaryTypeDef",
    "PutAdminAccountRequestTypeDef",
    "PutAdminAccountResponseTypeDef",
    "RemediationIssueDetailsTypeDef",
    "RemediationIssuesViewTypeDef",
    "ResourceAssociationTypeDef",
    "ResourceCriteriaOutputTypeDef",
    "ResourceCriteriaTypeDef",
    "ResourceLogicalExpressionOutputTypeDef",
    "ResourceLogicalExpressionTypeDef",
    "ResourceScopeOutputTypeDef",
    "ResourceScopeTypeDef",
    "ResourceSetOutputTypeDef",
    "ResourceSetTypeDef",
    "ResourceSynchronizationStatusSummaryTypeDef",
    "ResponseMetadataTypeDef",
    "RuleReferenceTypeDef",
    "RuleSummaryTypeDef",
    "ScopeConfigurationOutputTypeDef",
    "ScopeConfigurationTypeDef",
    "ScopeConfigurationUnionTypeDef",
    "ScopeReferenceTypeDef",
    "ScopeSummaryTypeDef",
    "TagResourceInputTypeDef",
    "TemplateOrRuleReferenceTypeDef",
    "TemplateSummaryTypeDef",
    "UntagResourceInputTypeDef",
    "UpdateDeploymentInputTypeDef",
    "UpdateDeploymentOutputTypeDef",
    "UpdatePolicyInputTypeDef",
    "UpdatePolicyOutputTypeDef",
    "UpdateRuleInputTypeDef",
    "UpdateRuleOutputTypeDef",
    "UpdateScopeInputTypeDef",
    "UpdateScopeOutputTypeDef",
    "UpdateTemplateInputTypeDef",
    "UpdateTemplateOutputTypeDef",
    "WafConfigTypeDef",
)


class AccountSetOutputTypeDef(TypedDict):
    accountIds: NotRequired[list[str]]
    organizationalUnits: NotRequired[list[str]]


class AccountSetTypeDef(TypedDict):
    accountIds: NotRequired[Sequence[str]]
    organizationalUnits: NotRequired[Sequence[str]]


class AccountReferenceTypeDef(TypedDict):
    accountId: str
    name: NotRequired[str]
    email: NotRequired[str]


class AdminAccountSummaryTypeDef(TypedDict):
    accountId: str
    priority: NotRequired[int]
    name: NotRequired[str]
    email: NotRequired[str]


class AdminFirewallTypeScopeOutputTypeDef(TypedDict):
    allFirewallTypesEnabled: NotRequired[bool]
    firewallTypes: NotRequired[list[PolicyFirewallTypeType]]


class AdminFirewallTypeScopeTypeDef(TypedDict):
    allFirewallTypesEnabled: NotRequired[bool]
    firewallTypes: NotRequired[Sequence[PolicyFirewallTypeType]]


class AdminScopeSelectionInputTypeDef(TypedDict):
    accounts: NotRequired[Sequence[str]]
    organizationalUnits: NotRequired[Sequence[str]]


class OrganizationalUnitReferenceTypeDef(TypedDict):
    ouId: str
    name: NotRequired[str]


class AlbConfigurationTypeDef(TypedDict):
    scheme: NotRequired[SchemeType]
    ipAddressType: NotRequired[IpAddressTypeType]


class AssociatedPolicyTypeDef(TypedDict):
    policyArn: str


class AssociatedRuleTypeDef(TypedDict):
    ruleArn: str


class AssociatedScopeTypeDef(TypedDict):
    scopeArn: str


class AssociatedTemplateOrRuleTypeDef(TypedDict):
    templateArn: NotRequired[str]
    ruleArn: NotRequired[str]


class ConfigurationIssueTypeDef(TypedDict):
    configurationName: NotRequired[str]
    expectedValue: NotRequired[str]
    actualValue: NotRequired[str]


class DeploymentConfigurationTypeDef(TypedDict):
    enableCrossAccountVisibility: bool


class PolicyReferenceTypeDef(TypedDict):
    policyIdentifier: str


class ScopeReferenceTypeDef(TypedDict):
    scopeIdentifier: str


class DeploymentCoverageEntryTypeDef(TypedDict):
    firewallType: PolicyFirewallTypeType
    policyArns: list[str]
    inScopeResourceTypes: list[ScopeResourceTypeType]


class DeploymentWarningEntryTypeDef(TypedDict):
    code: str
    policyArn: str
    message: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CreateDeploymentSnapshotInputTypeDef(TypedDict):
    deploymentIdentifier: str
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class TemplateOrRuleReferenceTypeDef(TypedDict):
    templateIdentifier: NotRequired[str]
    ruleIdentifier: NotRequired[str]


class CreatePolicySnapshotInputTypeDef(TypedDict):
    policyIdentifier: str
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class CreateRuleInputTypeDef(TypedDict):
    ruleName: str
    firewallType: Literal["WAF"]
    ruleType: RuleTypeType
    configuration: Mapping[str, Any]
    clientToken: NotRequired[str]
    ruleDescription: NotRequired[str]
    isPublished: NotRequired[bool]
    tags: NotRequired[Mapping[str, str]]


class CreateRuleSnapshotInputTypeDef(TypedDict):
    ruleIdentifier: str
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class CreateScopeSnapshotInputTypeDef(TypedDict):
    scopeIdentifier: str
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class RuleReferenceTypeDef(TypedDict):
    ruleIdentifier: str


class CreateTemplateSnapshotInputTypeDef(TypedDict):
    templateIdentifier: str
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class DeleteAdminAccountRequestTypeDef(TypedDict):
    accountId: str


class DeleteDeploymentInputTypeDef(TypedDict):
    deploymentIdentifier: str


class DeletePolicyInputTypeDef(TypedDict):
    policyIdentifier: str


class DeleteRuleInputTypeDef(TypedDict):
    ruleIdentifier: str


class DeleteScopeInputTypeDef(TypedDict):
    scopeIdentifier: str


class DeleteTemplateInputTypeDef(TypedDict):
    templateIdentifier: str


class DeploymentSummaryTypeDef(TypedDict):
    deploymentId: str
    deploymentArn: str
    deploymentName: NotRequired[str]
    status: NotRequired[EntityStatusType]
    version: NotRequired[str]
    hasPublishedVersion: NotRequired[bool]
    updatedAt: NotRequired[datetime]


class GenerateRuleConfigurationRequestTypeDef(TypedDict):
    prompt: str
    ruleFirewallType: Literal["WAF"]
    ruleType: RuleTypeType
    wafConfigDataType: NotRequired[WAFConfigDataTypeType]
    currentConfiguration: NotRequired[str]
    clientToken: NotRequired[str]


class GetAdminAccountRequestTypeDef(TypedDict):
    accountId: str


class GetDeploymentInputTypeDef(TypedDict):
    deploymentIdentifier: str


class GetPolicyInputTypeDef(TypedDict):
    policyIdentifier: str


class GetRuleInputTypeDef(TypedDict):
    ruleIdentifier: str


class GetScopeInputTypeDef(TypedDict):
    scopeIdentifier: str


class GetTemplateInputTypeDef(TypedDict):
    templateIdentifier: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListAdminAccountsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListAggregateResourceSynchronizationStatusesInputTypeDef(TypedDict):
    synchronizationStatus: NotRequired[SynchronizationStatusType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListDeploymentSnapshotsInputTypeDef(TypedDict):
    deploymentIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListDeploymentsInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    status: NotRequired[EntityStatusFilterType]


class ListPoliciesInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    status: NotRequired[EntityStatusFilterType]


class PolicySummaryTypeDef(TypedDict):
    policyId: str
    policyArn: str
    policyName: NotRequired[str]
    status: NotRequired[EntityStatusType]
    version: NotRequired[str]
    hasPublishedVersion: NotRequired[bool]
    firewallType: NotRequired[PolicyFirewallTypeType]
    priority: NotRequired[int]
    updatedAt: NotRequired[datetime]


class ListPolicySnapshotsInputTypeDef(TypedDict):
    policyIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListResourceAssociationsInputTypeDef(TypedDict):
    resourceIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ResourceAssociationTypeDef(TypedDict):
    arn: str
    resourceType: ServiceResourceTypeType


class ListResourceSynchronizationStatusesInputTypeDef(TypedDict):
    deploymentIdentifier: str
    synchronizationStatus: NotRequired[SynchronizationStatusType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListRuleSnapshotsInputTypeDef(TypedDict):
    ruleIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class RuleSummaryTypeDef(TypedDict):
    ruleId: str
    ruleArn: str
    ruleName: str
    firewallType: NotRequired[Literal["WAF"]]
    ruleType: NotRequired[RuleTypeType]
    status: NotRequired[EntityStatusType]
    version: NotRequired[str]
    hasPublishedVersion: NotRequired[bool]
    updatedAt: NotRequired[datetime]


class ListRulesInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    status: NotRequired[EntityStatusFilterType]


class ListScopeSnapshotsInputTypeDef(TypedDict):
    scopeIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ScopeSummaryTypeDef(TypedDict):
    scopeId: str
    scopeArn: str
    scopeName: NotRequired[str]
    status: NotRequired[EntityStatusType]
    version: NotRequired[str]
    hasPublishedVersion: NotRequired[bool]
    updatedAt: NotRequired[datetime]


class ListScopesInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    status: NotRequired[EntityStatusFilterType]


class ListTagsForResourceInputTypeDef(TypedDict):
    resourceArn: str


class ListTemplateSnapshotsInputTypeDef(TypedDict):
    templateIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class TemplateSummaryTypeDef(TypedDict):
    templateId: str
    templateArn: str
    templateName: str
    status: NotRequired[EntityStatusType]
    version: NotRequired[str]
    hasPublishedVersion: NotRequired[bool]
    firewallType: NotRequired[Literal["WAF"]]
    updatedAt: NotRequired[datetime]


class ListTemplatesInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    status: NotRequired[EntityStatusFilterType]


class NotVisibleMarkerTypeDef(TypedDict):
    reason: str


class WafConfigTypeDef(TypedDict):
    existingCustomerWebACLResolution: ExistingCustomerWebACLResolutionType
    conflictResolution: Literal["MERGE_WHERE_APPLICABLE"]


class RemediationIssueDetailsTypeDef(TypedDict):
    issueType: NotRequired[str]
    message: NotRequired[str]
    correctiveAction: NotRequired[str]


class TagResourceInputTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceInputTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateRuleInputTypeDef(TypedDict):
    ruleIdentifier: str
    updateToken: str
    isPublished: bool
    ruleType: NotRequired[RuleTypeType]
    ruleDescription: NotRequired[str]
    configuration: NotRequired[Mapping[str, Any]]
    clientToken: NotRequired[str]


class AccountFilterOutputTypeDef(TypedDict):
    includeAll: NotRequired[dict[str, Any]]
    include: NotRequired[AccountSetOutputTypeDef]
    exclude: NotRequired[AccountSetOutputTypeDef]


class AccountFilterTypeDef(TypedDict):
    includeAll: NotRequired[Mapping[str, Any]]
    include: NotRequired[AccountSetTypeDef]
    exclude: NotRequired[AccountSetTypeDef]


AdminFirewallTypeScopeUnionTypeDef = Union[
    AdminFirewallTypeScopeTypeDef, AdminFirewallTypeScopeOutputTypeDef
]


class AdminScopeFilterInputTypeDef(TypedDict):
    includeAll: NotRequired[Mapping[str, Any]]
    includeOnly: NotRequired[AdminScopeSelectionInputTypeDef]
    excludeOnly: NotRequired[AdminScopeSelectionInputTypeDef]


class AdminScopeSelectionTypeDef(TypedDict):
    accounts: NotRequired[list[AccountReferenceTypeDef]]
    organizationalUnits: NotRequired[list[OrganizationalUnitReferenceTypeDef]]


class ResourceCriteriaOutputTypeDef(TypedDict):
    tags: NotRequired[dict[str, str]]
    albConfig: NotRequired[AlbConfigurationTypeDef]


class ResourceCriteriaTypeDef(TypedDict):
    tags: NotRequired[Mapping[str, str]]
    albConfig: NotRequired[AlbConfigurationTypeDef]


class InvalidFirewallReasonsTypeDef(TypedDict):
    incorrectSingleValueConfigurations: NotRequired[list[ConfigurationIssueTypeDef]]
    missingAppendableConfigurationValues: NotRequired[list[ConfigurationIssueTypeDef]]
    unexpectedAppendableConfigurationValues: NotRequired[list[ConfigurationIssueTypeDef]]
    incorrectAppendableConfigurationOrder: NotRequired[list[ConfigurationIssueTypeDef]]
    missingMergeableConfigurationValues: NotRequired[list[ConfigurationIssueTypeDef]]
    unexpectedMergeableConfigurationValues: NotRequired[list[ConfigurationIssueTypeDef]]


class CreateDeploymentInputTypeDef(TypedDict):
    deploymentName: str
    deploymentConfiguration: DeploymentConfigurationTypeDef
    associatedPolicyList: Sequence[PolicyReferenceTypeDef]
    associatedScopeList: Sequence[ScopeReferenceTypeDef]
    clientToken: NotRequired[str]
    deploymentDescription: NotRequired[str]
    isPublished: NotRequired[bool]
    tags: NotRequired[Mapping[str, str]]


class UpdateDeploymentInputTypeDef(TypedDict):
    deploymentIdentifier: str
    updateToken: str
    isPublished: bool
    deploymentDescription: NotRequired[str]
    deploymentConfiguration: NotRequired[DeploymentConfigurationTypeDef]
    associatedPolicyList: NotRequired[Sequence[PolicyReferenceTypeDef]]
    associatedScopeList: NotRequired[Sequence[ScopeReferenceTypeDef]]
    clientToken: NotRequired[str]


class CreateDeploymentOutputTypeDef(TypedDict):
    deploymentId: str
    deploymentArn: str
    deploymentName: str
    deploymentDescription: str
    status: EntityStatusType
    deploymentConfiguration: DeploymentConfigurationTypeDef
    associatedPolicyList: list[AssociatedPolicyTypeDef]
    associatedScopeList: list[AssociatedScopeTypeDef]
    version: str
    updateToken: str
    isSnapshot: bool
    hasPublishedVersion: bool
    deploymentCoverage: list[DeploymentCoverageEntryTypeDef]
    warnings: list[DeploymentWarningEntryTypeDef]
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDeploymentSnapshotOutputTypeDef(TypedDict):
    deploymentId: str
    deploymentArn: str
    deploymentName: str
    deploymentDescription: str
    status: EntityStatusType
    deploymentConfiguration: DeploymentConfigurationTypeDef
    associatedPolicyList: list[AssociatedPolicyTypeDef]
    associatedScopeList: list[AssociatedScopeTypeDef]
    version: str
    updateToken: str
    isSnapshot: bool
    hasPublishedVersion: bool
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRuleOutputTypeDef(TypedDict):
    ruleId: str
    ruleArn: str
    ruleName: str
    firewallType: Literal["WAF"]
    ruleType: RuleTypeType
    ruleDescription: str
    configuration: dict[str, Any]
    status: EntityStatusType
    version: str
    updateToken: str
    isSnapshot: bool
    hasPublishedVersion: bool
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRuleSnapshotOutputTypeDef(TypedDict):
    ruleId: str
    ruleArn: str
    ruleName: str
    firewallType: Literal["WAF"]
    ruleType: RuleTypeType
    ruleDescription: str
    configuration: dict[str, Any]
    status: EntityStatusType
    version: str
    updateToken: str
    isSnapshot: bool
    hasPublishedVersion: bool
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTemplateOutputTypeDef(TypedDict):
    templateId: str
    templateArn: str
    templateName: str
    templateDescription: str
    status: EntityStatusType
    version: str
    associatedRuleList: list[AssociatedRuleTypeDef]
    updateToken: str
    isSnapshot: bool
    hasPublishedVersion: bool
    firewallType: Literal["WAF"]
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTemplateSnapshotOutputTypeDef(TypedDict):
    templateId: str
    templateArn: str
    templateName: str
    templateDescription: str
    status: EntityStatusType
    version: str
    associatedRuleList: list[AssociatedRuleTypeDef]
    updateToken: str
    isSnapshot: bool
    hasPublishedVersion: bool
    firewallType: Literal["WAF"]
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GenerateRuleConfigurationResponseTypeDef(TypedDict):
    configuration: str
    description: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetDeploymentOutputTypeDef(TypedDict):
    deploymentId: str
    deploymentArn: str
    deploymentName: str
    deploymentDescription: str
    status: EntityStatusType
    deploymentConfiguration: DeploymentConfigurationTypeDef
    associatedPolicyList: list[AssociatedPolicyTypeDef]
    associatedScopeList: list[AssociatedScopeTypeDef]
    version: str
    updateToken: str
    isSnapshot: bool
    hasPublishedVersion: bool
    updatedAt: datetime
    deploymentCoverage: list[DeploymentCoverageEntryTypeDef]
    warnings: list[DeploymentWarningEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetRuleOutputTypeDef(TypedDict):
    ruleId: str
    ruleArn: str
    ruleName: str
    firewallType: Literal["WAF"]
    ruleType: RuleTypeType
    ruleDescription: str
    configuration: dict[str, Any]
    status: EntityStatusType
    version: str
    updateToken: str
    isSnapshot: bool
    hasPublishedVersion: bool
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GetTemplateOutputTypeDef(TypedDict):
    templateId: str
    templateArn: str
    templateName: str
    templateDescription: str
    status: EntityStatusType
    version: str
    associatedRuleList: list[AssociatedRuleTypeDef]
    updateToken: str
    isSnapshot: bool
    hasPublishedVersion: bool
    firewallType: Literal["WAF"]
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class ListAdminAccountsResponseTypeDef(TypedDict):
    adminAccounts: list[AdminAccountSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTagsForResourceOutputTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDeploymentOutputTypeDef(TypedDict):
    deploymentId: str
    deploymentArn: str
    deploymentName: str
    deploymentDescription: str
    status: EntityStatusType
    deploymentConfiguration: DeploymentConfigurationTypeDef
    associatedPolicyList: list[AssociatedPolicyTypeDef]
    associatedScopeList: list[AssociatedScopeTypeDef]
    version: str
    updateToken: str
    isSnapshot: bool
    hasPublishedVersion: bool
    deploymentCoverage: list[DeploymentCoverageEntryTypeDef]
    warnings: list[DeploymentWarningEntryTypeDef]
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRuleOutputTypeDef(TypedDict):
    ruleId: str
    ruleArn: str
    ruleName: str
    firewallType: Literal["WAF"]
    ruleType: RuleTypeType
    ruleDescription: str
    configuration: dict[str, Any]
    status: EntityStatusType
    version: str
    updateToken: str
    isSnapshot: bool
    hasPublishedVersion: bool
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTemplateOutputTypeDef(TypedDict):
    templateId: str
    templateArn: str
    templateName: str
    templateDescription: str
    status: EntityStatusType
    version: str
    associatedRuleList: list[AssociatedRuleTypeDef]
    updateToken: str
    isSnapshot: bool
    hasPublishedVersion: bool
    firewallType: Literal["WAF"]
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTemplateInputTypeDef(TypedDict):
    templateName: str
    associatedRuleList: Sequence[RuleReferenceTypeDef]
    firewallType: Literal["WAF"]
    clientToken: NotRequired[str]
    templateDescription: NotRequired[str]
    isPublished: NotRequired[bool]
    tags: NotRequired[Mapping[str, str]]


class UpdateTemplateInputTypeDef(TypedDict):
    templateIdentifier: str
    updateToken: str
    isPublished: bool
    templateDescription: NotRequired[str]
    associatedRuleList: NotRequired[Sequence[RuleReferenceTypeDef]]
    clientToken: NotRequired[str]


class ListDeploymentSnapshotsOutputTypeDef(TypedDict):
    snapshots: list[DeploymentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListDeploymentsOutputTypeDef(TypedDict):
    deployments: list[DeploymentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListAdminAccountsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAggregateResourceSynchronizationStatusesInputPaginateTypeDef(TypedDict):
    synchronizationStatus: NotRequired[SynchronizationStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDeploymentSnapshotsInputPaginateTypeDef(TypedDict):
    deploymentIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDeploymentsInputPaginateTypeDef(TypedDict):
    status: NotRequired[EntityStatusFilterType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPoliciesInputPaginateTypeDef(TypedDict):
    status: NotRequired[EntityStatusFilterType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPolicySnapshotsInputPaginateTypeDef(TypedDict):
    policyIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResourceAssociationsInputPaginateTypeDef(TypedDict):
    resourceIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResourceSynchronizationStatusesInputPaginateTypeDef(TypedDict):
    deploymentIdentifier: str
    synchronizationStatus: NotRequired[SynchronizationStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRuleSnapshotsInputPaginateTypeDef(TypedDict):
    ruleIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRulesInputPaginateTypeDef(TypedDict):
    status: NotRequired[EntityStatusFilterType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListScopeSnapshotsInputPaginateTypeDef(TypedDict):
    scopeIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListScopesInputPaginateTypeDef(TypedDict):
    status: NotRequired[EntityStatusFilterType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTemplateSnapshotsInputPaginateTypeDef(TypedDict):
    templateIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTemplatesInputPaginateTypeDef(TypedDict):
    status: NotRequired[EntityStatusFilterType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPoliciesOutputTypeDef(TypedDict):
    policies: list[PolicySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListPolicySnapshotsOutputTypeDef(TypedDict):
    snapshots: list[PolicySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListResourceAssociationsOutputTypeDef(TypedDict):
    resourceAssociations: list[ResourceAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListRuleSnapshotsOutputTypeDef(TypedDict):
    snapshots: list[RuleSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListRulesOutputTypeDef(TypedDict):
    rules: list[RuleSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListScopeSnapshotsOutputTypeDef(TypedDict):
    snapshots: list[ScopeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListScopesOutputTypeDef(TypedDict):
    scopes: list[ScopeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTemplateSnapshotsOutputTypeDef(TypedDict):
    snapshots: list[TemplateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTemplatesOutputTypeDef(TypedDict):
    templates: list[TemplateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class PolicyConfigurationTypeDef(TypedDict):
    remediationEnabled: bool
    resourcesCleanUp: bool
    wafConfig: NotRequired[WafConfigTypeDef]


class RemediationIssuesViewTypeDef(TypedDict):
    issues: NotRequired[dict[PolicyFirewallTypeType, RemediationIssueDetailsTypeDef]]
    notVisible: NotRequired[NotVisibleMarkerTypeDef]


class AdminScopeInputTypeDef(TypedDict):
    scopeFilter: NotRequired[AdminScopeFilterInputTypeDef]
    firewallTypeScope: NotRequired[AdminFirewallTypeScopeUnionTypeDef]


class AdminScopeFilterTypeDef(TypedDict):
    includeAll: NotRequired[dict[str, Any]]
    includeOnly: NotRequired[AdminScopeSelectionTypeDef]
    excludeOnly: NotRequired[AdminScopeSelectionTypeDef]


ResourceLogicalExpressionOutputTypeDef = TypedDict(
    "ResourceLogicalExpressionOutputTypeDef",
    {
        "criteria": NotRequired[ResourceCriteriaOutputTypeDef],
        "and": NotRequired[list[dict[str, Any]]],
        "or": NotRequired[list[dict[str, Any]]],
        "not": NotRequired[dict[str, Any]],
    },
)
ResourceLogicalExpressionTypeDef = TypedDict(
    "ResourceLogicalExpressionTypeDef",
    {
        "criteria": NotRequired[ResourceCriteriaTypeDef],
        "and": NotRequired[Sequence[Mapping[str, Any]]],
        "or": NotRequired[Sequence[Mapping[str, Any]]],
        "not": NotRequired[Mapping[str, Any]],
    },
)


class FirewallSyncReasonTypeDef(TypedDict):
    missingFirewall: NotRequired[str]
    invalidFirewall: NotRequired[InvalidFirewallReasonsTypeDef]


class CreatePolicyInputTypeDef(TypedDict):
    policyName: str
    priority: int
    firewallType: PolicyFirewallTypeType
    policyConfiguration: PolicyConfigurationTypeDef
    clientToken: NotRequired[str]
    policyDescription: NotRequired[str]
    associatedTemplateAndRuleList: NotRequired[Sequence[TemplateOrRuleReferenceTypeDef]]
    isPublished: NotRequired[bool]
    tags: NotRequired[Mapping[str, str]]


class CreatePolicyOutputTypeDef(TypedDict):
    policyId: str
    policyArn: str
    policyName: str
    policyDescription: str
    status: EntityStatusType
    priority: int
    associatedTemplateAndRuleList: list[AssociatedTemplateOrRuleTypeDef]
    version: str
    updateToken: str
    isSnapshot: bool
    hasPublishedVersion: bool
    firewallType: PolicyFirewallTypeType
    policyConfiguration: PolicyConfigurationTypeDef
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePolicySnapshotOutputTypeDef(TypedDict):
    policyId: str
    policyArn: str
    policyName: str
    policyDescription: str
    status: EntityStatusType
    priority: int
    associatedTemplateAndRuleList: list[AssociatedTemplateOrRuleTypeDef]
    version: str
    updateToken: str
    isSnapshot: bool
    hasPublishedVersion: bool
    firewallType: PolicyFirewallTypeType
    policyConfiguration: PolicyConfigurationTypeDef
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GetPolicyOutputTypeDef(TypedDict):
    policyId: str
    policyArn: str
    policyName: str
    policyDescription: str
    status: EntityStatusType
    priority: int
    associatedTemplateAndRuleList: list[AssociatedTemplateOrRuleTypeDef]
    version: str
    updateToken: str
    isSnapshot: bool
    hasPublishedVersion: bool
    firewallType: PolicyFirewallTypeType
    policyConfiguration: PolicyConfigurationTypeDef
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePolicyInputTypeDef(TypedDict):
    policyIdentifier: str
    updateToken: str
    isPublished: bool
    policyDescription: NotRequired[str]
    priority: NotRequired[int]
    associatedTemplateAndRuleList: NotRequired[Sequence[TemplateOrRuleReferenceTypeDef]]
    policyConfiguration: NotRequired[PolicyConfigurationTypeDef]
    clientToken: NotRequired[str]


class UpdatePolicyOutputTypeDef(TypedDict):
    policyId: str
    policyArn: str
    policyName: str
    policyDescription: str
    status: EntityStatusType
    priority: int
    associatedTemplateAndRuleList: list[AssociatedTemplateOrRuleTypeDef]
    version: str
    updateToken: str
    isSnapshot: bool
    hasPublishedVersion: bool
    firewallType: PolicyFirewallTypeType
    policyConfiguration: PolicyConfigurationTypeDef
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class PutAdminAccountRequestTypeDef(TypedDict):
    accountId: str
    priority: int
    adminScope: NotRequired[AdminScopeInputTypeDef]


class AdminScopeTypeDef(TypedDict):
    scopeFilter: NotRequired[AdminScopeFilterTypeDef]
    firewallTypeScope: NotRequired[AdminFirewallTypeScopeOutputTypeDef]


class ResourceSetOutputTypeDef(TypedDict):
    explicitArns: NotRequired[list[str]]
    expression: NotRequired[ResourceLogicalExpressionOutputTypeDef]


class ResourceSetTypeDef(TypedDict):
    explicitArns: NotRequired[Sequence[str]]
    expression: NotRequired[ResourceLogicalExpressionTypeDef]


class OutOfSyncReasonsViewTypeDef(TypedDict):
    reasons: NotRequired[dict[PolicyFirewallTypeType, FirewallSyncReasonTypeDef]]
    notVisible: NotRequired[NotVisibleMarkerTypeDef]


class AdminAccountDetailsTypeDef(TypedDict):
    adminAccount: str
    priority: int
    adminScope: NotRequired[AdminScopeTypeDef]
    status: NotRequired[AdminAccountStatusType]


class ResourceScopeOutputTypeDef(TypedDict):
    includeAll: NotRequired[bool]
    include: NotRequired[ResourceSetOutputTypeDef]
    exclude: NotRequired[ResourceSetOutputTypeDef]


class ResourceScopeTypeDef(TypedDict):
    includeAll: NotRequired[bool]
    include: NotRequired[ResourceSetTypeDef]
    exclude: NotRequired[ResourceSetTypeDef]


class ResourceSynchronizationStatusSummaryTypeDef(TypedDict):
    synchronizationStatus: SynchronizationStatusType
    accountId: str
    resourceArn: str
    updatedAt: datetime
    deploymentArn: NotRequired[str]
    resourceType: NotRequired[ResourceTypeType]
    outOfSyncReasons: NotRequired[OutOfSyncReasonsViewTypeDef]
    remediationIssues: NotRequired[RemediationIssuesViewTypeDef]
    evaluatedAt: NotRequired[datetime]


class GetAdminAccountResponseTypeDef(TypedDict):
    adminAccountDetails: AdminAccountDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PutAdminAccountResponseTypeDef(TypedDict):
    adminAccountDetails: AdminAccountDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ScopeConfigurationOutputTypeDef(TypedDict):
    resourceScopes: dict[ScopeResourceTypeType, ResourceScopeOutputTypeDef]
    accountFilter: NotRequired[AccountFilterOutputTypeDef]


class ScopeConfigurationTypeDef(TypedDict):
    resourceScopes: Mapping[ScopeResourceTypeType, ResourceScopeTypeDef]
    accountFilter: NotRequired[AccountFilterTypeDef]


class ListAggregateResourceSynchronizationStatusesOutputTypeDef(TypedDict):
    resourceSynchronizationStatuses: list[ResourceSynchronizationStatusSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListResourceSynchronizationStatusesOutputTypeDef(TypedDict):
    resourceSynchronizationStatuses: list[ResourceSynchronizationStatusSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateScopeOutputTypeDef(TypedDict):
    scopeId: str
    scopeArn: str
    scopeName: str
    scopeDescription: str
    scopeConfiguration: ScopeConfigurationOutputTypeDef
    status: EntityStatusType
    version: str
    updateToken: str
    isSnapshot: bool
    hasPublishedVersion: bool
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CreateScopeSnapshotOutputTypeDef(TypedDict):
    scopeId: str
    scopeArn: str
    scopeName: str
    scopeDescription: str
    scopeConfiguration: ScopeConfigurationOutputTypeDef
    status: EntityStatusType
    version: str
    updateToken: str
    isSnapshot: bool
    hasPublishedVersion: bool
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GetScopeOutputTypeDef(TypedDict):
    scopeId: str
    scopeArn: str
    scopeName: str
    scopeDescription: str
    scopeConfiguration: ScopeConfigurationOutputTypeDef
    status: EntityStatusType
    version: str
    updateToken: str
    isSnapshot: bool
    hasPublishedVersion: bool
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateScopeOutputTypeDef(TypedDict):
    scopeId: str
    scopeArn: str
    scopeName: str
    scopeDescription: str
    scopeConfiguration: ScopeConfigurationOutputTypeDef
    status: EntityStatusType
    version: str
    updateToken: str
    isSnapshot: bool
    hasPublishedVersion: bool
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


ScopeConfigurationUnionTypeDef = Union[ScopeConfigurationTypeDef, ScopeConfigurationOutputTypeDef]


class CreateScopeInputTypeDef(TypedDict):
    scopeName: str
    scopeConfiguration: ScopeConfigurationUnionTypeDef
    clientToken: NotRequired[str]
    scopeDescription: NotRequired[str]
    isPublished: NotRequired[bool]
    tags: NotRequired[Mapping[str, str]]


class UpdateScopeInputTypeDef(TypedDict):
    scopeIdentifier: str
    updateToken: str
    isPublished: bool
    scopeDescription: NotRequired[str]
    scopeConfiguration: NotRequired[ScopeConfigurationUnionTypeDef]
    clientToken: NotRequired[str]
