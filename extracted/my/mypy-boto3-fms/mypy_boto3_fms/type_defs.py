"""
Type annotations for fms service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fms/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_fms.type_defs import AccountScopeOutputTypeDef

    data: AccountScopeOutputTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    AccountRoleStatusType,
    CustomerPolicyScopeIdTypeType,
    CustomerPolicyStatusType,
    DependentServiceNameType,
    DestinationTypeType,
    EntryTypeType,
    EntryViolationReasonType,
    FailedItemReasonType,
    FirewallDeploymentModelType,
    MarketplaceSubscriptionOnboardingStatusType,
    NetworkAclRuleActionType,
    OrganizationStatusType,
    PolicyComplianceStatusTypeType,
    RemediationActionTypeType,
    ResourceSetStatusType,
    ResourceTagLogicalOperatorType,
    RuleOrderType,
    SecurityServiceTypeType,
    StreamExceptionPolicyType,
    TargetTypeType,
    ThirdPartyFirewallAssociationStatusType,
    ThirdPartyFirewallType,
    ViolationReasonType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AccountScopeOutputTypeDef",
    "AccountScopeTypeDef",
    "ActionTargetTypeDef",
    "AdminAccountSummaryTypeDef",
    "AdminScopeOutputTypeDef",
    "AdminScopeTypeDef",
    "AdminScopeUnionTypeDef",
    "AppTypeDef",
    "AppsListDataOutputTypeDef",
    "AppsListDataSummaryTypeDef",
    "AppsListDataTypeDef",
    "AppsListDataUnionTypeDef",
    "AssociateAdminAccountRequestTypeDef",
    "AssociateThirdPartyFirewallRequestTypeDef",
    "AssociateThirdPartyFirewallResponseTypeDef",
    "AwsEc2InstanceViolationTypeDef",
    "AwsEc2NetworkInterfaceViolationTypeDef",
    "AwsVPCSecurityGroupViolationTypeDef",
    "BatchAssociateResourceRequestTypeDef",
    "BatchAssociateResourceResponseTypeDef",
    "BatchDisassociateResourceRequestTypeDef",
    "BatchDisassociateResourceResponseTypeDef",
    "ComplianceViolatorTypeDef",
    "CreateNetworkAclActionTypeDef",
    "CreateNetworkAclEntriesActionTypeDef",
    "DeleteAppsListRequestTypeDef",
    "DeleteNetworkAclEntriesActionTypeDef",
    "DeletePolicyRequestTypeDef",
    "DeleteProtocolsListRequestTypeDef",
    "DeleteResourceSetRequestTypeDef",
    "DisassociateThirdPartyFirewallRequestTypeDef",
    "DisassociateThirdPartyFirewallResponseTypeDef",
    "DiscoveredResourceTypeDef",
    "DnsDuplicateRuleGroupViolationTypeDef",
    "DnsRuleGroupLimitExceededViolationTypeDef",
    "DnsRuleGroupPriorityConflictViolationTypeDef",
    "EC2AssociateRouteTableActionTypeDef",
    "EC2CopyRouteTableActionTypeDef",
    "EC2CreateRouteActionTypeDef",
    "EC2CreateRouteTableActionTypeDef",
    "EC2DeleteRouteActionTypeDef",
    "EC2ReplaceRouteActionTypeDef",
    "EC2ReplaceRouteTableAssociationActionTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EntryDescriptionTypeDef",
    "EntryViolationTypeDef",
    "EvaluationResultTypeDef",
    "ExpectedRouteTypeDef",
    "FMSPolicyUpdateFirewallCreationConfigActionTypeDef",
    "FailedItemTypeDef",
    "FirewallSubnetIsOutOfScopeViolationTypeDef",
    "FirewallSubnetMissingVPCEndpointViolationTypeDef",
    "GetAdminAccountResponseTypeDef",
    "GetAdminScopeRequestTypeDef",
    "GetAdminScopeResponseTypeDef",
    "GetAppsListRequestTypeDef",
    "GetAppsListResponseTypeDef",
    "GetComplianceDetailRequestTypeDef",
    "GetComplianceDetailResponseTypeDef",
    "GetNotificationChannelResponseTypeDef",
    "GetPolicyRequestTypeDef",
    "GetPolicyResponseTypeDef",
    "GetProtectionStatusRequestTypeDef",
    "GetProtectionStatusResponseTypeDef",
    "GetProtocolsListRequestTypeDef",
    "GetProtocolsListResponseTypeDef",
    "GetResourceSetRequestTypeDef",
    "GetResourceSetResponseTypeDef",
    "GetThirdPartyFirewallAssociationStatusRequestTypeDef",
    "GetThirdPartyFirewallAssociationStatusResponseTypeDef",
    "GetViolationDetailsRequestTypeDef",
    "GetViolationDetailsResponseTypeDef",
    "InvalidNetworkAclEntriesViolationTypeDef",
    "ListAdminAccountsForOrganizationRequestPaginateTypeDef",
    "ListAdminAccountsForOrganizationRequestTypeDef",
    "ListAdminAccountsForOrganizationResponseTypeDef",
    "ListAdminsManagingAccountRequestPaginateTypeDef",
    "ListAdminsManagingAccountRequestTypeDef",
    "ListAdminsManagingAccountResponseTypeDef",
    "ListAppsListsRequestPaginateTypeDef",
    "ListAppsListsRequestTypeDef",
    "ListAppsListsResponseTypeDef",
    "ListComplianceStatusRequestPaginateTypeDef",
    "ListComplianceStatusRequestTypeDef",
    "ListComplianceStatusResponseTypeDef",
    "ListDiscoveredResourcesRequestTypeDef",
    "ListDiscoveredResourcesResponseTypeDef",
    "ListMemberAccountsRequestPaginateTypeDef",
    "ListMemberAccountsRequestTypeDef",
    "ListMemberAccountsResponseTypeDef",
    "ListPoliciesRequestPaginateTypeDef",
    "ListPoliciesRequestTypeDef",
    "ListPoliciesResponseTypeDef",
    "ListProtocolsListsRequestPaginateTypeDef",
    "ListProtocolsListsRequestTypeDef",
    "ListProtocolsListsResponseTypeDef",
    "ListResourceSetResourcesRequestTypeDef",
    "ListResourceSetResourcesResponseTypeDef",
    "ListResourceSetsRequestTypeDef",
    "ListResourceSetsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListThirdPartyFirewallFirewallPoliciesRequestPaginateTypeDef",
    "ListThirdPartyFirewallFirewallPoliciesRequestTypeDef",
    "ListThirdPartyFirewallFirewallPoliciesResponseTypeDef",
    "NetworkAclCommonPolicyOutputTypeDef",
    "NetworkAclCommonPolicyTypeDef",
    "NetworkAclEntrySetOutputTypeDef",
    "NetworkAclEntrySetTypeDef",
    "NetworkAclEntryTypeDef",
    "NetworkAclIcmpTypeCodeTypeDef",
    "NetworkAclPortRangeTypeDef",
    "NetworkFirewallBlackHoleRouteDetectedViolationTypeDef",
    "NetworkFirewallInternetTrafficNotInspectedViolationTypeDef",
    "NetworkFirewallInvalidRouteConfigurationViolationTypeDef",
    "NetworkFirewallMissingExpectedRTViolationTypeDef",
    "NetworkFirewallMissingExpectedRoutesViolationTypeDef",
    "NetworkFirewallMissingFirewallViolationTypeDef",
    "NetworkFirewallMissingSubnetViolationTypeDef",
    "NetworkFirewallPolicyDescriptionTypeDef",
    "NetworkFirewallPolicyModifiedViolationTypeDef",
    "NetworkFirewallPolicyTypeDef",
    "NetworkFirewallStatefulRuleGroupOverrideTypeDef",
    "NetworkFirewallUnexpectedFirewallRoutesViolationTypeDef",
    "NetworkFirewallUnexpectedGatewayRoutesViolationTypeDef",
    "OrganizationalUnitScopeOutputTypeDef",
    "OrganizationalUnitScopeTypeDef",
    "PaginatorConfigTypeDef",
    "PartialMatchTypeDef",
    "PolicyComplianceDetailTypeDef",
    "PolicyComplianceStatusTypeDef",
    "PolicyOptionOutputTypeDef",
    "PolicyOptionTypeDef",
    "PolicyOutputTypeDef",
    "PolicySummaryTypeDef",
    "PolicyTypeDef",
    "PolicyTypeScopeOutputTypeDef",
    "PolicyTypeScopeTypeDef",
    "PolicyUnionTypeDef",
    "PossibleRemediationActionTypeDef",
    "PossibleRemediationActionsTypeDef",
    "ProtocolsListDataOutputTypeDef",
    "ProtocolsListDataSummaryTypeDef",
    "ProtocolsListDataTypeDef",
    "ProtocolsListDataUnionTypeDef",
    "PutAdminAccountRequestTypeDef",
    "PutAppsListRequestTypeDef",
    "PutAppsListResponseTypeDef",
    "PutNotificationChannelRequestTypeDef",
    "PutPolicyRequestTypeDef",
    "PutPolicyResponseTypeDef",
    "PutProtocolsListRequestTypeDef",
    "PutProtocolsListResponseTypeDef",
    "PutResourceSetRequestTypeDef",
    "PutResourceSetResponseTypeDef",
    "RegionScopeOutputTypeDef",
    "RegionScopeTypeDef",
    "RemediationActionTypeDef",
    "RemediationActionWithOrderTypeDef",
    "ReplaceNetworkAclAssociationActionTypeDef",
    "ResourceSetOutputTypeDef",
    "ResourceSetSummaryTypeDef",
    "ResourceSetTypeDef",
    "ResourceSetUnionTypeDef",
    "ResourceTagTypeDef",
    "ResourceTypeDef",
    "ResourceViolationTypeDef",
    "ResponseMetadataTypeDef",
    "RouteHasOutOfScopeEndpointViolationTypeDef",
    "RouteTypeDef",
    "SecurityGroupRemediationActionTypeDef",
    "SecurityGroupRuleDescriptionTypeDef",
    "SecurityServicePolicyDataOutputTypeDef",
    "SecurityServicePolicyDataTypeDef",
    "StatefulEngineOptionsTypeDef",
    "StatefulRuleGroupTypeDef",
    "StatelessRuleGroupTypeDef",
    "TagResourceRequestTypeDef",
    "TagTypeDef",
    "ThirdPartyFirewallFirewallPolicyTypeDef",
    "ThirdPartyFirewallMissingExpectedRouteTableViolationTypeDef",
    "ThirdPartyFirewallMissingFirewallViolationTypeDef",
    "ThirdPartyFirewallMissingSubnetViolationTypeDef",
    "ThirdPartyFirewallPolicyTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestTypeDef",
    "ViolationDetailTypeDef",
    "WebACLHasIncompatibleConfigurationViolationTypeDef",
    "WebACLHasOutOfScopeResourcesViolationTypeDef",
)


class AccountScopeOutputTypeDef(TypedDict):
    Accounts: NotRequired[list[str]]
    AllAccountsEnabled: NotRequired[bool]
    ExcludeSpecifiedAccounts: NotRequired[bool]


class AccountScopeTypeDef(TypedDict):
    Accounts: NotRequired[Sequence[str]]
    AllAccountsEnabled: NotRequired[bool]
    ExcludeSpecifiedAccounts: NotRequired[bool]


class ActionTargetTypeDef(TypedDict):
    ResourceId: NotRequired[str]
    Description: NotRequired[str]


class AdminAccountSummaryTypeDef(TypedDict):
    AdminAccount: NotRequired[str]
    DefaultAdmin: NotRequired[bool]
    Status: NotRequired[OrganizationStatusType]


class OrganizationalUnitScopeOutputTypeDef(TypedDict):
    OrganizationalUnits: NotRequired[list[str]]
    AllOrganizationalUnitsEnabled: NotRequired[bool]
    ExcludeSpecifiedOrganizationalUnits: NotRequired[bool]


class PolicyTypeScopeOutputTypeDef(TypedDict):
    PolicyTypes: NotRequired[list[SecurityServiceTypeType]]
    AllPolicyTypesEnabled: NotRequired[bool]


class RegionScopeOutputTypeDef(TypedDict):
    Regions: NotRequired[list[str]]
    AllRegionsEnabled: NotRequired[bool]


class OrganizationalUnitScopeTypeDef(TypedDict):
    OrganizationalUnits: NotRequired[Sequence[str]]
    AllOrganizationalUnitsEnabled: NotRequired[bool]
    ExcludeSpecifiedOrganizationalUnits: NotRequired[bool]


class PolicyTypeScopeTypeDef(TypedDict):
    PolicyTypes: NotRequired[Sequence[SecurityServiceTypeType]]
    AllPolicyTypesEnabled: NotRequired[bool]


class RegionScopeTypeDef(TypedDict):
    Regions: NotRequired[Sequence[str]]
    AllRegionsEnabled: NotRequired[bool]


AppTypeDef = TypedDict(
    "AppTypeDef",
    {
        "AppName": str,
        "Protocol": str,
        "Port": int,
    },
)
TimestampTypeDef = Union[datetime, str]


class AssociateAdminAccountRequestTypeDef(TypedDict):
    AdminAccount: str


class AssociateThirdPartyFirewallRequestTypeDef(TypedDict):
    ThirdPartyFirewall: ThirdPartyFirewallType


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AwsEc2NetworkInterfaceViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    ViolatingSecurityGroups: NotRequired[list[str]]


class PartialMatchTypeDef(TypedDict):
    Reference: NotRequired[str]
    TargetViolationReasons: NotRequired[list[str]]


class BatchAssociateResourceRequestTypeDef(TypedDict):
    ResourceSetIdentifier: str
    Items: Sequence[str]


class FailedItemTypeDef(TypedDict):
    URI: NotRequired[str]
    Reason: NotRequired[FailedItemReasonType]


class BatchDisassociateResourceRequestTypeDef(TypedDict):
    ResourceSetIdentifier: str
    Items: Sequence[str]


class ComplianceViolatorTypeDef(TypedDict):
    ResourceId: NotRequired[str]
    ViolationReason: NotRequired[ViolationReasonType]
    ResourceType: NotRequired[str]
    Metadata: NotRequired[dict[str, str]]


class DeleteAppsListRequestTypeDef(TypedDict):
    ListId: str


class DeletePolicyRequestTypeDef(TypedDict):
    PolicyId: str
    DeleteAllPolicyResources: NotRequired[bool]


class DeleteProtocolsListRequestTypeDef(TypedDict):
    ListId: str


class DeleteResourceSetRequestTypeDef(TypedDict):
    Identifier: str


class DisassociateThirdPartyFirewallRequestTypeDef(TypedDict):
    ThirdPartyFirewall: ThirdPartyFirewallType


DiscoveredResourceTypeDef = TypedDict(
    "DiscoveredResourceTypeDef",
    {
        "URI": NotRequired[str],
        "AccountId": NotRequired[str],
        "Type": NotRequired[str],
        "Name": NotRequired[str],
    },
)


class DnsDuplicateRuleGroupViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    ViolationTargetDescription: NotRequired[str]


class DnsRuleGroupLimitExceededViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    ViolationTargetDescription: NotRequired[str]
    NumberOfRuleGroupsAlreadyAssociated: NotRequired[int]


class DnsRuleGroupPriorityConflictViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    ViolationTargetDescription: NotRequired[str]
    ConflictingPriority: NotRequired[int]
    ConflictingPolicyId: NotRequired[str]
    UnavailablePriorities: NotRequired[list[int]]


class EvaluationResultTypeDef(TypedDict):
    ComplianceStatus: NotRequired[PolicyComplianceStatusTypeType]
    ViolatorCount: NotRequired[int]
    EvaluationLimitExceeded: NotRequired[bool]


class ExpectedRouteTypeDef(TypedDict):
    IpV4Cidr: NotRequired[str]
    PrefixListId: NotRequired[str]
    IpV6Cidr: NotRequired[str]
    ContributingSubnets: NotRequired[list[str]]
    AllowedTargets: NotRequired[list[str]]
    RouteTableId: NotRequired[str]


class FMSPolicyUpdateFirewallCreationConfigActionTypeDef(TypedDict):
    Description: NotRequired[str]
    FirewallCreationConfig: NotRequired[str]


class FirewallSubnetIsOutOfScopeViolationTypeDef(TypedDict):
    FirewallSubnetId: NotRequired[str]
    VpcId: NotRequired[str]
    SubnetAvailabilityZone: NotRequired[str]
    SubnetAvailabilityZoneId: NotRequired[str]
    VpcEndpointId: NotRequired[str]


class FirewallSubnetMissingVPCEndpointViolationTypeDef(TypedDict):
    FirewallSubnetId: NotRequired[str]
    VpcId: NotRequired[str]
    SubnetAvailabilityZone: NotRequired[str]
    SubnetAvailabilityZoneId: NotRequired[str]


class GetAdminScopeRequestTypeDef(TypedDict):
    AdminAccount: str


class GetAppsListRequestTypeDef(TypedDict):
    ListId: str
    DefaultList: NotRequired[bool]


class GetComplianceDetailRequestTypeDef(TypedDict):
    PolicyId: str
    MemberAccount: str


class GetPolicyRequestTypeDef(TypedDict):
    PolicyId: str


class GetProtocolsListRequestTypeDef(TypedDict):
    ListId: str
    DefaultList: NotRequired[bool]


class ProtocolsListDataOutputTypeDef(TypedDict):
    ListName: str
    ProtocolsList: list[str]
    ListId: NotRequired[str]
    ListUpdateToken: NotRequired[str]
    CreateTime: NotRequired[datetime]
    LastUpdateTime: NotRequired[datetime]
    PreviousProtocolsList: NotRequired[dict[str, list[str]]]


class GetResourceSetRequestTypeDef(TypedDict):
    Identifier: str


class ResourceSetOutputTypeDef(TypedDict):
    Name: str
    ResourceTypeList: list[str]
    Id: NotRequired[str]
    Description: NotRequired[str]
    UpdateToken: NotRequired[str]
    LastUpdateTime: NotRequired[datetime]
    ResourceSetStatus: NotRequired[ResourceSetStatusType]


class GetThirdPartyFirewallAssociationStatusRequestTypeDef(TypedDict):
    ThirdPartyFirewall: ThirdPartyFirewallType


class GetViolationDetailsRequestTypeDef(TypedDict):
    PolicyId: str
    MemberAccount: str
    ResourceId: str
    ResourceType: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListAdminAccountsForOrganizationRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListAdminsManagingAccountRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListAppsListsRequestTypeDef(TypedDict):
    MaxResults: int
    DefaultLists: NotRequired[bool]
    NextToken: NotRequired[str]


class ListComplianceStatusRequestTypeDef(TypedDict):
    PolicyId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListDiscoveredResourcesRequestTypeDef(TypedDict):
    MemberAccountIds: Sequence[str]
    ResourceType: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListMemberAccountsRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListPoliciesRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class PolicySummaryTypeDef(TypedDict):
    PolicyArn: NotRequired[str]
    PolicyId: NotRequired[str]
    PolicyName: NotRequired[str]
    ResourceType: NotRequired[str]
    SecurityServiceType: NotRequired[SecurityServiceTypeType]
    RemediationEnabled: NotRequired[bool]
    DeleteUnusedFMManagedResources: NotRequired[bool]
    PolicyStatus: NotRequired[CustomerPolicyStatusType]


class ListProtocolsListsRequestTypeDef(TypedDict):
    MaxResults: int
    DefaultLists: NotRequired[bool]
    NextToken: NotRequired[str]


class ProtocolsListDataSummaryTypeDef(TypedDict):
    ListArn: NotRequired[str]
    ListId: NotRequired[str]
    ListName: NotRequired[str]
    ProtocolsList: NotRequired[list[str]]


class ListResourceSetResourcesRequestTypeDef(TypedDict):
    Identifier: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ResourceTypeDef(TypedDict):
    URI: str
    AccountId: NotRequired[str]


class ListResourceSetsRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ResourceSetSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    LastUpdateTime: NotRequired[datetime]
    ResourceSetStatus: NotRequired[ResourceSetStatusType]


class ListTagsForResourceRequestTypeDef(TypedDict):
    ResourceArn: str


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class ListThirdPartyFirewallFirewallPoliciesRequestTypeDef(TypedDict):
    ThirdPartyFirewall: ThirdPartyFirewallType
    MaxResults: int
    NextToken: NotRequired[str]


class ThirdPartyFirewallFirewallPolicyTypeDef(TypedDict):
    FirewallPolicyId: NotRequired[str]
    FirewallPolicyName: NotRequired[str]


NetworkAclIcmpTypeCodeTypeDef = TypedDict(
    "NetworkAclIcmpTypeCodeTypeDef",
    {
        "Code": NotRequired[int],
        "Type": NotRequired[int],
    },
)


class NetworkAclPortRangeTypeDef(TypedDict):
    From: NotRequired[int]
    To: NotRequired[int]


class RouteTypeDef(TypedDict):
    DestinationType: NotRequired[DestinationTypeType]
    TargetType: NotRequired[TargetTypeType]
    Destination: NotRequired[str]
    Target: NotRequired[str]


class NetworkFirewallMissingExpectedRTViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    VPC: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    CurrentRouteTable: NotRequired[str]
    ExpectedRouteTable: NotRequired[str]


class NetworkFirewallMissingFirewallViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    VPC: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    TargetViolationReason: NotRequired[str]


class NetworkFirewallMissingSubnetViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    VPC: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    TargetViolationReason: NotRequired[str]


class StatefulEngineOptionsTypeDef(TypedDict):
    RuleOrder: NotRequired[RuleOrderType]
    StreamExceptionPolicy: NotRequired[StreamExceptionPolicyType]


class StatelessRuleGroupTypeDef(TypedDict):
    RuleGroupName: NotRequired[str]
    ResourceId: NotRequired[str]
    Priority: NotRequired[int]


class NetworkFirewallPolicyTypeDef(TypedDict):
    FirewallDeploymentModel: NotRequired[FirewallDeploymentModelType]


class NetworkFirewallStatefulRuleGroupOverrideTypeDef(TypedDict):
    Action: NotRequired[Literal["DROP_TO_ALERT"]]


class ThirdPartyFirewallPolicyTypeDef(TypedDict):
    FirewallDeploymentModel: NotRequired[FirewallDeploymentModelType]


class ResourceTagTypeDef(TypedDict):
    Key: str
    Value: NotRequired[str]


class PutNotificationChannelRequestTypeDef(TypedDict):
    SnsTopicArn: str
    SnsRoleName: str


class ThirdPartyFirewallMissingExpectedRouteTableViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    VPC: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    CurrentRouteTable: NotRequired[str]
    ExpectedRouteTable: NotRequired[str]


class ThirdPartyFirewallMissingFirewallViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    VPC: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    TargetViolationReason: NotRequired[str]


class ThirdPartyFirewallMissingSubnetViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    VPC: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    TargetViolationReason: NotRequired[str]


class WebACLHasIncompatibleConfigurationViolationTypeDef(TypedDict):
    WebACLArn: NotRequired[str]
    Description: NotRequired[str]


class WebACLHasOutOfScopeResourcesViolationTypeDef(TypedDict):
    WebACLArn: NotRequired[str]
    OutOfScopeResourceList: NotRequired[list[str]]


SecurityGroupRuleDescriptionTypeDef = TypedDict(
    "SecurityGroupRuleDescriptionTypeDef",
    {
        "IPV4Range": NotRequired[str],
        "IPV6Range": NotRequired[str],
        "PrefixListId": NotRequired[str],
        "Protocol": NotRequired[str],
        "FromPort": NotRequired[int],
        "ToPort": NotRequired[int],
    },
)


class UntagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class CreateNetworkAclActionTypeDef(TypedDict):
    Description: NotRequired[str]
    Vpc: NotRequired[ActionTargetTypeDef]
    FMSCanRemediate: NotRequired[bool]


class EC2AssociateRouteTableActionTypeDef(TypedDict):
    RouteTableId: ActionTargetTypeDef
    Description: NotRequired[str]
    SubnetId: NotRequired[ActionTargetTypeDef]
    GatewayId: NotRequired[ActionTargetTypeDef]


class EC2CopyRouteTableActionTypeDef(TypedDict):
    VpcId: ActionTargetTypeDef
    RouteTableId: ActionTargetTypeDef
    Description: NotRequired[str]


class EC2CreateRouteActionTypeDef(TypedDict):
    RouteTableId: ActionTargetTypeDef
    Description: NotRequired[str]
    DestinationCidrBlock: NotRequired[str]
    DestinationPrefixListId: NotRequired[str]
    DestinationIpv6CidrBlock: NotRequired[str]
    VpcEndpointId: NotRequired[ActionTargetTypeDef]
    GatewayId: NotRequired[ActionTargetTypeDef]


class EC2CreateRouteTableActionTypeDef(TypedDict):
    VpcId: ActionTargetTypeDef
    Description: NotRequired[str]


class EC2DeleteRouteActionTypeDef(TypedDict):
    RouteTableId: ActionTargetTypeDef
    Description: NotRequired[str]
    DestinationCidrBlock: NotRequired[str]
    DestinationPrefixListId: NotRequired[str]
    DestinationIpv6CidrBlock: NotRequired[str]


class EC2ReplaceRouteActionTypeDef(TypedDict):
    RouteTableId: ActionTargetTypeDef
    Description: NotRequired[str]
    DestinationCidrBlock: NotRequired[str]
    DestinationPrefixListId: NotRequired[str]
    DestinationIpv6CidrBlock: NotRequired[str]
    GatewayId: NotRequired[ActionTargetTypeDef]


class EC2ReplaceRouteTableAssociationActionTypeDef(TypedDict):
    AssociationId: ActionTargetTypeDef
    RouteTableId: ActionTargetTypeDef
    Description: NotRequired[str]


class ReplaceNetworkAclAssociationActionTypeDef(TypedDict):
    Description: NotRequired[str]
    AssociationId: NotRequired[ActionTargetTypeDef]
    NetworkAclId: NotRequired[ActionTargetTypeDef]
    FMSCanRemediate: NotRequired[bool]


class AdminScopeOutputTypeDef(TypedDict):
    AccountScope: NotRequired[AccountScopeOutputTypeDef]
    OrganizationalUnitScope: NotRequired[OrganizationalUnitScopeOutputTypeDef]
    RegionScope: NotRequired[RegionScopeOutputTypeDef]
    PolicyTypeScope: NotRequired[PolicyTypeScopeOutputTypeDef]


class AdminScopeTypeDef(TypedDict):
    AccountScope: NotRequired[AccountScopeTypeDef]
    OrganizationalUnitScope: NotRequired[OrganizationalUnitScopeTypeDef]
    RegionScope: NotRequired[RegionScopeTypeDef]
    PolicyTypeScope: NotRequired[PolicyTypeScopeTypeDef]


class AppsListDataOutputTypeDef(TypedDict):
    ListName: str
    AppsList: list[AppTypeDef]
    ListId: NotRequired[str]
    ListUpdateToken: NotRequired[str]
    CreateTime: NotRequired[datetime]
    LastUpdateTime: NotRequired[datetime]
    PreviousAppsList: NotRequired[dict[str, list[AppTypeDef]]]


class AppsListDataSummaryTypeDef(TypedDict):
    ListArn: NotRequired[str]
    ListId: NotRequired[str]
    ListName: NotRequired[str]
    AppsList: NotRequired[list[AppTypeDef]]


class AppsListDataTypeDef(TypedDict):
    ListName: str
    AppsList: Sequence[AppTypeDef]
    ListId: NotRequired[str]
    ListUpdateToken: NotRequired[str]
    CreateTime: NotRequired[TimestampTypeDef]
    LastUpdateTime: NotRequired[TimestampTypeDef]
    PreviousAppsList: NotRequired[Mapping[str, Sequence[AppTypeDef]]]


class GetProtectionStatusRequestTypeDef(TypedDict):
    PolicyId: str
    MemberAccountId: NotRequired[str]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ProtocolsListDataTypeDef(TypedDict):
    ListName: str
    ProtocolsList: Sequence[str]
    ListId: NotRequired[str]
    ListUpdateToken: NotRequired[str]
    CreateTime: NotRequired[TimestampTypeDef]
    LastUpdateTime: NotRequired[TimestampTypeDef]
    PreviousProtocolsList: NotRequired[Mapping[str, Sequence[str]]]


class ResourceSetTypeDef(TypedDict):
    Name: str
    ResourceTypeList: Sequence[str]
    Id: NotRequired[str]
    Description: NotRequired[str]
    UpdateToken: NotRequired[str]
    LastUpdateTime: NotRequired[TimestampTypeDef]
    ResourceSetStatus: NotRequired[ResourceSetStatusType]


class AssociateThirdPartyFirewallResponseTypeDef(TypedDict):
    ThirdPartyFirewallStatus: ThirdPartyFirewallAssociationStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateThirdPartyFirewallResponseTypeDef(TypedDict):
    ThirdPartyFirewallStatus: ThirdPartyFirewallAssociationStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetAdminAccountResponseTypeDef(TypedDict):
    AdminAccount: str
    RoleStatus: AccountRoleStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class GetNotificationChannelResponseTypeDef(TypedDict):
    SnsTopicArn: str
    SnsRoleName: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetProtectionStatusResponseTypeDef(TypedDict):
    AdminAccountId: str
    ServiceType: SecurityServiceTypeType
    Data: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetThirdPartyFirewallAssociationStatusResponseTypeDef(TypedDict):
    ThirdPartyFirewallStatus: ThirdPartyFirewallAssociationStatusType
    MarketplaceOnboardingStatus: MarketplaceSubscriptionOnboardingStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class ListAdminAccountsForOrganizationResponseTypeDef(TypedDict):
    AdminAccounts: list[AdminAccountSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListAdminsManagingAccountResponseTypeDef(TypedDict):
    AdminAccounts: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListMemberAccountsResponseTypeDef(TypedDict):
    MemberAccounts: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AwsEc2InstanceViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    AwsEc2NetworkInterfaceViolations: NotRequired[list[AwsEc2NetworkInterfaceViolationTypeDef]]


class BatchAssociateResourceResponseTypeDef(TypedDict):
    ResourceSetIdentifier: str
    FailedItems: list[FailedItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchDisassociateResourceResponseTypeDef(TypedDict):
    ResourceSetIdentifier: str
    FailedItems: list[FailedItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class PolicyComplianceDetailTypeDef(TypedDict):
    PolicyOwner: NotRequired[str]
    PolicyId: NotRequired[str]
    MemberAccount: NotRequired[str]
    Violators: NotRequired[list[ComplianceViolatorTypeDef]]
    EvaluationLimitExceeded: NotRequired[bool]
    ExpiredAt: NotRequired[datetime]
    IssueInfoMap: NotRequired[dict[DependentServiceNameType, str]]


class ListDiscoveredResourcesResponseTypeDef(TypedDict):
    Items: list[DiscoveredResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PolicyComplianceStatusTypeDef(TypedDict):
    PolicyOwner: NotRequired[str]
    PolicyId: NotRequired[str]
    PolicyName: NotRequired[str]
    MemberAccount: NotRequired[str]
    EvaluationResults: NotRequired[list[EvaluationResultTypeDef]]
    LastUpdated: NotRequired[datetime]
    IssueInfoMap: NotRequired[dict[DependentServiceNameType, str]]


class NetworkFirewallMissingExpectedRoutesViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    ExpectedRoutes: NotRequired[list[ExpectedRouteTypeDef]]
    VpcId: NotRequired[str]


class GetProtocolsListResponseTypeDef(TypedDict):
    ProtocolsList: ProtocolsListDataOutputTypeDef
    ProtocolsListArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class PutProtocolsListResponseTypeDef(TypedDict):
    ProtocolsList: ProtocolsListDataOutputTypeDef
    ProtocolsListArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetResourceSetResponseTypeDef(TypedDict):
    ResourceSet: ResourceSetOutputTypeDef
    ResourceSetArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class PutResourceSetResponseTypeDef(TypedDict):
    ResourceSet: ResourceSetOutputTypeDef
    ResourceSetArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListAdminAccountsForOrganizationRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAdminsManagingAccountRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAppsListsRequestPaginateTypeDef(TypedDict):
    DefaultLists: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListComplianceStatusRequestPaginateTypeDef(TypedDict):
    PolicyId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMemberAccountsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPoliciesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProtocolsListsRequestPaginateTypeDef(TypedDict):
    DefaultLists: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListThirdPartyFirewallFirewallPoliciesRequestPaginateTypeDef(TypedDict):
    ThirdPartyFirewall: ThirdPartyFirewallType
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPoliciesResponseTypeDef(TypedDict):
    PolicyList: list[PolicySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListProtocolsListsResponseTypeDef(TypedDict):
    ProtocolsLists: list[ProtocolsListDataSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListResourceSetResourcesResponseTypeDef(TypedDict):
    Items: list[ResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListResourceSetsResponseTypeDef(TypedDict):
    ResourceSets: list[ResourceSetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    TagList: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    TagList: Sequence[TagTypeDef]


class ListThirdPartyFirewallFirewallPoliciesResponseTypeDef(TypedDict):
    ThirdPartyFirewallFirewallPolicies: list[ThirdPartyFirewallFirewallPolicyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


NetworkAclEntryTypeDef = TypedDict(
    "NetworkAclEntryTypeDef",
    {
        "Protocol": str,
        "RuleAction": NetworkAclRuleActionType,
        "Egress": bool,
        "IcmpTypeCode": NotRequired[NetworkAclIcmpTypeCodeTypeDef],
        "PortRange": NotRequired[NetworkAclPortRangeTypeDef],
        "CidrBlock": NotRequired[str],
        "Ipv6CidrBlock": NotRequired[str],
    },
)


class NetworkFirewallBlackHoleRouteDetectedViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    RouteTableId: NotRequired[str]
    VpcId: NotRequired[str]
    ViolatingRoutes: NotRequired[list[RouteTypeDef]]


class NetworkFirewallInternetTrafficNotInspectedViolationTypeDef(TypedDict):
    SubnetId: NotRequired[str]
    SubnetAvailabilityZone: NotRequired[str]
    RouteTableId: NotRequired[str]
    ViolatingRoutes: NotRequired[list[RouteTypeDef]]
    IsRouteTableUsedInDifferentAZ: NotRequired[bool]
    CurrentFirewallSubnetRouteTable: NotRequired[str]
    ExpectedFirewallEndpoint: NotRequired[str]
    FirewallSubnetId: NotRequired[str]
    ExpectedFirewallSubnetRoutes: NotRequired[list[ExpectedRouteTypeDef]]
    ActualFirewallSubnetRoutes: NotRequired[list[RouteTypeDef]]
    InternetGatewayId: NotRequired[str]
    CurrentInternetGatewayRouteTable: NotRequired[str]
    ExpectedInternetGatewayRoutes: NotRequired[list[ExpectedRouteTypeDef]]
    ActualInternetGatewayRoutes: NotRequired[list[RouteTypeDef]]
    VpcId: NotRequired[str]


class NetworkFirewallInvalidRouteConfigurationViolationTypeDef(TypedDict):
    AffectedSubnets: NotRequired[list[str]]
    RouteTableId: NotRequired[str]
    IsRouteTableUsedInDifferentAZ: NotRequired[bool]
    ViolatingRoute: NotRequired[RouteTypeDef]
    CurrentFirewallSubnetRouteTable: NotRequired[str]
    ExpectedFirewallEndpoint: NotRequired[str]
    ActualFirewallEndpoint: NotRequired[str]
    ExpectedFirewallSubnetId: NotRequired[str]
    ActualFirewallSubnetId: NotRequired[str]
    ExpectedFirewallSubnetRoutes: NotRequired[list[ExpectedRouteTypeDef]]
    ActualFirewallSubnetRoutes: NotRequired[list[RouteTypeDef]]
    InternetGatewayId: NotRequired[str]
    CurrentInternetGatewayRouteTable: NotRequired[str]
    ExpectedInternetGatewayRoutes: NotRequired[list[ExpectedRouteTypeDef]]
    ActualInternetGatewayRoutes: NotRequired[list[RouteTypeDef]]
    VpcId: NotRequired[str]


class NetworkFirewallUnexpectedFirewallRoutesViolationTypeDef(TypedDict):
    FirewallSubnetId: NotRequired[str]
    ViolatingRoutes: NotRequired[list[RouteTypeDef]]
    RouteTableId: NotRequired[str]
    FirewallEndpoint: NotRequired[str]
    VpcId: NotRequired[str]


class NetworkFirewallUnexpectedGatewayRoutesViolationTypeDef(TypedDict):
    GatewayId: NotRequired[str]
    ViolatingRoutes: NotRequired[list[RouteTypeDef]]
    RouteTableId: NotRequired[str]
    VpcId: NotRequired[str]


class RouteHasOutOfScopeEndpointViolationTypeDef(TypedDict):
    SubnetId: NotRequired[str]
    VpcId: NotRequired[str]
    RouteTableId: NotRequired[str]
    ViolatingRoutes: NotRequired[list[RouteTypeDef]]
    SubnetAvailabilityZone: NotRequired[str]
    SubnetAvailabilityZoneId: NotRequired[str]
    CurrentFirewallSubnetRouteTable: NotRequired[str]
    FirewallSubnetId: NotRequired[str]
    FirewallSubnetRoutes: NotRequired[list[RouteTypeDef]]
    InternetGatewayId: NotRequired[str]
    CurrentInternetGatewayRouteTable: NotRequired[str]
    InternetGatewayRoutes: NotRequired[list[RouteTypeDef]]


class StatefulRuleGroupTypeDef(TypedDict):
    RuleGroupName: NotRequired[str]
    ResourceId: NotRequired[str]
    Priority: NotRequired[int]
    Override: NotRequired[NetworkFirewallStatefulRuleGroupOverrideTypeDef]


class SecurityGroupRemediationActionTypeDef(TypedDict):
    RemediationActionType: NotRequired[RemediationActionTypeType]
    Description: NotRequired[str]
    RemediationResult: NotRequired[SecurityGroupRuleDescriptionTypeDef]
    IsDefaultAction: NotRequired[bool]


class GetAdminScopeResponseTypeDef(TypedDict):
    AdminScope: AdminScopeOutputTypeDef
    Status: OrganizationStatusType
    ResponseMetadata: ResponseMetadataTypeDef


AdminScopeUnionTypeDef = Union[AdminScopeTypeDef, AdminScopeOutputTypeDef]


class GetAppsListResponseTypeDef(TypedDict):
    AppsList: AppsListDataOutputTypeDef
    AppsListArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class PutAppsListResponseTypeDef(TypedDict):
    AppsList: AppsListDataOutputTypeDef
    AppsListArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListAppsListsResponseTypeDef(TypedDict):
    AppsLists: list[AppsListDataSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


AppsListDataUnionTypeDef = Union[AppsListDataTypeDef, AppsListDataOutputTypeDef]
ProtocolsListDataUnionTypeDef = Union[ProtocolsListDataTypeDef, ProtocolsListDataOutputTypeDef]
ResourceSetUnionTypeDef = Union[ResourceSetTypeDef, ResourceSetOutputTypeDef]


class GetComplianceDetailResponseTypeDef(TypedDict):
    PolicyComplianceDetail: PolicyComplianceDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListComplianceStatusResponseTypeDef(TypedDict):
    PolicyComplianceStatusList: list[PolicyComplianceStatusTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class EntryDescriptionTypeDef(TypedDict):
    EntryDetail: NotRequired[NetworkAclEntryTypeDef]
    EntryRuleNumber: NotRequired[int]
    EntryType: NotRequired[EntryTypeType]


class NetworkAclEntrySetOutputTypeDef(TypedDict):
    ForceRemediateForFirstEntries: bool
    ForceRemediateForLastEntries: bool
    FirstEntries: NotRequired[list[NetworkAclEntryTypeDef]]
    LastEntries: NotRequired[list[NetworkAclEntryTypeDef]]


class NetworkAclEntrySetTypeDef(TypedDict):
    ForceRemediateForFirstEntries: bool
    ForceRemediateForLastEntries: bool
    FirstEntries: NotRequired[Sequence[NetworkAclEntryTypeDef]]
    LastEntries: NotRequired[Sequence[NetworkAclEntryTypeDef]]


class NetworkFirewallPolicyDescriptionTypeDef(TypedDict):
    StatelessRuleGroups: NotRequired[list[StatelessRuleGroupTypeDef]]
    StatelessDefaultActions: NotRequired[list[str]]
    StatelessFragmentDefaultActions: NotRequired[list[str]]
    StatelessCustomActions: NotRequired[list[str]]
    StatefulRuleGroups: NotRequired[list[StatefulRuleGroupTypeDef]]
    StatefulDefaultActions: NotRequired[list[str]]
    StatefulEngineOptions: NotRequired[StatefulEngineOptionsTypeDef]


class AwsVPCSecurityGroupViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    ViolationTargetDescription: NotRequired[str]
    PartialMatches: NotRequired[list[PartialMatchTypeDef]]
    PossibleSecurityGroupRemediationActions: NotRequired[
        list[SecurityGroupRemediationActionTypeDef]
    ]


class PutAdminAccountRequestTypeDef(TypedDict):
    AdminAccount: str
    AdminScope: NotRequired[AdminScopeUnionTypeDef]


class PutAppsListRequestTypeDef(TypedDict):
    AppsList: AppsListDataUnionTypeDef
    TagList: NotRequired[Sequence[TagTypeDef]]


class PutProtocolsListRequestTypeDef(TypedDict):
    ProtocolsList: ProtocolsListDataUnionTypeDef
    TagList: NotRequired[Sequence[TagTypeDef]]


class PutResourceSetRequestTypeDef(TypedDict):
    ResourceSet: ResourceSetUnionTypeDef
    TagList: NotRequired[Sequence[TagTypeDef]]


class CreateNetworkAclEntriesActionTypeDef(TypedDict):
    Description: NotRequired[str]
    NetworkAclId: NotRequired[ActionTargetTypeDef]
    NetworkAclEntriesToBeCreated: NotRequired[list[EntryDescriptionTypeDef]]
    FMSCanRemediate: NotRequired[bool]


class DeleteNetworkAclEntriesActionTypeDef(TypedDict):
    Description: NotRequired[str]
    NetworkAclId: NotRequired[ActionTargetTypeDef]
    NetworkAclEntriesToBeDeleted: NotRequired[list[EntryDescriptionTypeDef]]
    FMSCanRemediate: NotRequired[bool]


class EntryViolationTypeDef(TypedDict):
    ExpectedEntry: NotRequired[EntryDescriptionTypeDef]
    ExpectedEvaluationOrder: NotRequired[str]
    ActualEvaluationOrder: NotRequired[str]
    EntryAtExpectedEvaluationOrder: NotRequired[EntryDescriptionTypeDef]
    EntriesWithConflicts: NotRequired[list[EntryDescriptionTypeDef]]
    EntryViolationReasons: NotRequired[list[EntryViolationReasonType]]


class NetworkAclCommonPolicyOutputTypeDef(TypedDict):
    NetworkAclEntrySet: NetworkAclEntrySetOutputTypeDef


class NetworkAclCommonPolicyTypeDef(TypedDict):
    NetworkAclEntrySet: NetworkAclEntrySetTypeDef


class NetworkFirewallPolicyModifiedViolationTypeDef(TypedDict):
    ViolationTarget: NotRequired[str]
    CurrentPolicyDescription: NotRequired[NetworkFirewallPolicyDescriptionTypeDef]
    ExpectedPolicyDescription: NotRequired[NetworkFirewallPolicyDescriptionTypeDef]


class RemediationActionTypeDef(TypedDict):
    Description: NotRequired[str]
    EC2CreateRouteAction: NotRequired[EC2CreateRouteActionTypeDef]
    EC2ReplaceRouteAction: NotRequired[EC2ReplaceRouteActionTypeDef]
    EC2DeleteRouteAction: NotRequired[EC2DeleteRouteActionTypeDef]
    EC2CopyRouteTableAction: NotRequired[EC2CopyRouteTableActionTypeDef]
    EC2ReplaceRouteTableAssociationAction: NotRequired[EC2ReplaceRouteTableAssociationActionTypeDef]
    EC2AssociateRouteTableAction: NotRequired[EC2AssociateRouteTableActionTypeDef]
    EC2CreateRouteTableAction: NotRequired[EC2CreateRouteTableActionTypeDef]
    FMSPolicyUpdateFirewallCreationConfigAction: NotRequired[
        FMSPolicyUpdateFirewallCreationConfigActionTypeDef
    ]
    CreateNetworkAclAction: NotRequired[CreateNetworkAclActionTypeDef]
    ReplaceNetworkAclAssociationAction: NotRequired[ReplaceNetworkAclAssociationActionTypeDef]
    CreateNetworkAclEntriesAction: NotRequired[CreateNetworkAclEntriesActionTypeDef]
    DeleteNetworkAclEntriesAction: NotRequired[DeleteNetworkAclEntriesActionTypeDef]


class InvalidNetworkAclEntriesViolationTypeDef(TypedDict):
    Vpc: NotRequired[str]
    Subnet: NotRequired[str]
    SubnetAvailabilityZone: NotRequired[str]
    CurrentAssociatedNetworkAcl: NotRequired[str]
    EntryViolations: NotRequired[list[EntryViolationTypeDef]]


class PolicyOptionOutputTypeDef(TypedDict):
    NetworkFirewallPolicy: NotRequired[NetworkFirewallPolicyTypeDef]
    ThirdPartyFirewallPolicy: NotRequired[ThirdPartyFirewallPolicyTypeDef]
    NetworkAclCommonPolicy: NotRequired[NetworkAclCommonPolicyOutputTypeDef]


class PolicyOptionTypeDef(TypedDict):
    NetworkFirewallPolicy: NotRequired[NetworkFirewallPolicyTypeDef]
    ThirdPartyFirewallPolicy: NotRequired[ThirdPartyFirewallPolicyTypeDef]
    NetworkAclCommonPolicy: NotRequired[NetworkAclCommonPolicyTypeDef]


class RemediationActionWithOrderTypeDef(TypedDict):
    RemediationAction: NotRequired[RemediationActionTypeDef]
    Order: NotRequired[int]


SecurityServicePolicyDataOutputTypeDef = TypedDict(
    "SecurityServicePolicyDataOutputTypeDef",
    {
        "Type": SecurityServiceTypeType,
        "ManagedServiceData": NotRequired[str],
        "PolicyOption": NotRequired[PolicyOptionOutputTypeDef],
    },
)
SecurityServicePolicyDataTypeDef = TypedDict(
    "SecurityServicePolicyDataTypeDef",
    {
        "Type": SecurityServiceTypeType,
        "ManagedServiceData": NotRequired[str],
        "PolicyOption": NotRequired[PolicyOptionTypeDef],
    },
)


class PossibleRemediationActionTypeDef(TypedDict):
    OrderedRemediationActions: list[RemediationActionWithOrderTypeDef]
    Description: NotRequired[str]
    IsDefaultAction: NotRequired[bool]


class PolicyOutputTypeDef(TypedDict):
    PolicyName: str
    SecurityServicePolicyData: SecurityServicePolicyDataOutputTypeDef
    ResourceType: str
    ExcludeResourceTags: bool
    RemediationEnabled: bool
    PolicyId: NotRequired[str]
    PolicyUpdateToken: NotRequired[str]
    ResourceTypeList: NotRequired[list[str]]
    ResourceTags: NotRequired[list[ResourceTagTypeDef]]
    DeleteUnusedFMManagedResources: NotRequired[bool]
    IncludeMap: NotRequired[dict[CustomerPolicyScopeIdTypeType, list[str]]]
    ExcludeMap: NotRequired[dict[CustomerPolicyScopeIdTypeType, list[str]]]
    ResourceSetIds: NotRequired[list[str]]
    PolicyDescription: NotRequired[str]
    PolicyStatus: NotRequired[CustomerPolicyStatusType]
    ResourceTagLogicalOperator: NotRequired[ResourceTagLogicalOperatorType]


class PolicyTypeDef(TypedDict):
    PolicyName: str
    SecurityServicePolicyData: SecurityServicePolicyDataTypeDef
    ResourceType: str
    ExcludeResourceTags: bool
    RemediationEnabled: bool
    PolicyId: NotRequired[str]
    PolicyUpdateToken: NotRequired[str]
    ResourceTypeList: NotRequired[Sequence[str]]
    ResourceTags: NotRequired[Sequence[ResourceTagTypeDef]]
    DeleteUnusedFMManagedResources: NotRequired[bool]
    IncludeMap: NotRequired[Mapping[CustomerPolicyScopeIdTypeType, Sequence[str]]]
    ExcludeMap: NotRequired[Mapping[CustomerPolicyScopeIdTypeType, Sequence[str]]]
    ResourceSetIds: NotRequired[Sequence[str]]
    PolicyDescription: NotRequired[str]
    PolicyStatus: NotRequired[CustomerPolicyStatusType]
    ResourceTagLogicalOperator: NotRequired[ResourceTagLogicalOperatorType]


class PossibleRemediationActionsTypeDef(TypedDict):
    Description: NotRequired[str]
    Actions: NotRequired[list[PossibleRemediationActionTypeDef]]


class GetPolicyResponseTypeDef(TypedDict):
    Policy: PolicyOutputTypeDef
    PolicyArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class PutPolicyResponseTypeDef(TypedDict):
    Policy: PolicyOutputTypeDef
    PolicyArn: str
    ResponseMetadata: ResponseMetadataTypeDef


PolicyUnionTypeDef = Union[PolicyTypeDef, PolicyOutputTypeDef]


class ResourceViolationTypeDef(TypedDict):
    AwsVPCSecurityGroupViolation: NotRequired[AwsVPCSecurityGroupViolationTypeDef]
    AwsEc2NetworkInterfaceViolation: NotRequired[AwsEc2NetworkInterfaceViolationTypeDef]
    AwsEc2InstanceViolation: NotRequired[AwsEc2InstanceViolationTypeDef]
    NetworkFirewallMissingFirewallViolation: NotRequired[
        NetworkFirewallMissingFirewallViolationTypeDef
    ]
    NetworkFirewallMissingSubnetViolation: NotRequired[NetworkFirewallMissingSubnetViolationTypeDef]
    NetworkFirewallMissingExpectedRTViolation: NotRequired[
        NetworkFirewallMissingExpectedRTViolationTypeDef
    ]
    NetworkFirewallPolicyModifiedViolation: NotRequired[
        NetworkFirewallPolicyModifiedViolationTypeDef
    ]
    NetworkFirewallInternetTrafficNotInspectedViolation: NotRequired[
        NetworkFirewallInternetTrafficNotInspectedViolationTypeDef
    ]
    NetworkFirewallInvalidRouteConfigurationViolation: NotRequired[
        NetworkFirewallInvalidRouteConfigurationViolationTypeDef
    ]
    NetworkFirewallBlackHoleRouteDetectedViolation: NotRequired[
        NetworkFirewallBlackHoleRouteDetectedViolationTypeDef
    ]
    NetworkFirewallUnexpectedFirewallRoutesViolation: NotRequired[
        NetworkFirewallUnexpectedFirewallRoutesViolationTypeDef
    ]
    NetworkFirewallUnexpectedGatewayRoutesViolation: NotRequired[
        NetworkFirewallUnexpectedGatewayRoutesViolationTypeDef
    ]
    NetworkFirewallMissingExpectedRoutesViolation: NotRequired[
        NetworkFirewallMissingExpectedRoutesViolationTypeDef
    ]
    DnsRuleGroupPriorityConflictViolation: NotRequired[DnsRuleGroupPriorityConflictViolationTypeDef]
    DnsDuplicateRuleGroupViolation: NotRequired[DnsDuplicateRuleGroupViolationTypeDef]
    DnsRuleGroupLimitExceededViolation: NotRequired[DnsRuleGroupLimitExceededViolationTypeDef]
    FirewallSubnetIsOutOfScopeViolation: NotRequired[FirewallSubnetIsOutOfScopeViolationTypeDef]
    RouteHasOutOfScopeEndpointViolation: NotRequired[RouteHasOutOfScopeEndpointViolationTypeDef]
    ThirdPartyFirewallMissingFirewallViolation: NotRequired[
        ThirdPartyFirewallMissingFirewallViolationTypeDef
    ]
    ThirdPartyFirewallMissingSubnetViolation: NotRequired[
        ThirdPartyFirewallMissingSubnetViolationTypeDef
    ]
    ThirdPartyFirewallMissingExpectedRouteTableViolation: NotRequired[
        ThirdPartyFirewallMissingExpectedRouteTableViolationTypeDef
    ]
    FirewallSubnetMissingVPCEndpointViolation: NotRequired[
        FirewallSubnetMissingVPCEndpointViolationTypeDef
    ]
    InvalidNetworkAclEntriesViolation: NotRequired[InvalidNetworkAclEntriesViolationTypeDef]
    PossibleRemediationActions: NotRequired[PossibleRemediationActionsTypeDef]
    WebACLHasIncompatibleConfigurationViolation: NotRequired[
        WebACLHasIncompatibleConfigurationViolationTypeDef
    ]
    WebACLHasOutOfScopeResourcesViolation: NotRequired[WebACLHasOutOfScopeResourcesViolationTypeDef]


class PutPolicyRequestTypeDef(TypedDict):
    Policy: PolicyUnionTypeDef
    TagList: NotRequired[Sequence[TagTypeDef]]


class ViolationDetailTypeDef(TypedDict):
    PolicyId: str
    MemberAccount: str
    ResourceId: str
    ResourceType: str
    ResourceViolations: list[ResourceViolationTypeDef]
    ResourceTags: NotRequired[list[TagTypeDef]]
    ResourceDescription: NotRequired[str]


class GetViolationDetailsResponseTypeDef(TypedDict):
    ViolationDetail: ViolationDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
