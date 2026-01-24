"""
Type annotations for network-firewall service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_network_firewall/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_network_firewall.type_defs import AttachmentTypeDef

    data: AttachmentTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    AttachmentStatusType,
    ConfigurationSyncStateType,
    EnabledAnalysisTypeType,
    EncryptionTypeType,
    FirewallStatusValueType,
    FlowOperationStatusType,
    FlowOperationTypeType,
    GeneratedRulesTypeType,
    IdentifiedTypeType,
    IPAddressTypeType,
    ListenerPropertyTypeType,
    LogDestinationTypeType,
    LogTypeType,
    PerObjectSyncStatusType,
    ProxyModifyStateType,
    ProxyRulePhaseActionType,
    ProxyStateType,
    ResourceManagedStatusType,
    ResourceManagedTypeType,
    ResourceStatusType,
    RevocationCheckActionType,
    RuleGroupRequestPhaseType,
    RuleGroupTypeType,
    RuleOrderType,
    StatefulActionType,
    StatefulRuleDirectionType,
    StatefulRuleProtocolType,
    StreamExceptionPolicyType,
    SubscriptionStatusType,
    SummaryRuleOptionType,
    TargetTypeType,
    TCPFlagType,
    TlsInterceptModeType,
    TransitGatewayAttachmentStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AZSyncStateTypeDef",
    "AcceptNetworkFirewallTransitGatewayAttachmentRequestTypeDef",
    "AcceptNetworkFirewallTransitGatewayAttachmentResponseTypeDef",
    "ActionDefinitionOutputTypeDef",
    "ActionDefinitionTypeDef",
    "AddressTypeDef",
    "AnalysisReportTypeDef",
    "AnalysisResultTypeDef",
    "AnalysisTypeReportResultTypeDef",
    "AssociateAvailabilityZonesRequestTypeDef",
    "AssociateAvailabilityZonesResponseTypeDef",
    "AssociateFirewallPolicyRequestTypeDef",
    "AssociateFirewallPolicyResponseTypeDef",
    "AssociateSubnetsRequestTypeDef",
    "AssociateSubnetsResponseTypeDef",
    "AttachRuleGroupsToProxyConfigurationRequestTypeDef",
    "AttachRuleGroupsToProxyConfigurationResponseTypeDef",
    "AttachmentTypeDef",
    "AvailabilityZoneMappingTypeDef",
    "AvailabilityZoneMetadataTypeDef",
    "CIDRSummaryTypeDef",
    "CapacityUsageSummaryTypeDef",
    "CheckCertificateRevocationStatusActionsTypeDef",
    "CreateFirewallPolicyRequestTypeDef",
    "CreateFirewallPolicyResponseTypeDef",
    "CreateFirewallRequestTypeDef",
    "CreateFirewallResponseTypeDef",
    "CreateProxyConfigurationRequestTypeDef",
    "CreateProxyConfigurationResponseTypeDef",
    "CreateProxyRequestTypeDef",
    "CreateProxyResponseTypeDef",
    "CreateProxyRuleGroupRequestTypeDef",
    "CreateProxyRuleGroupResponseTypeDef",
    "CreateProxyRuleTypeDef",
    "CreateProxyRulesByRequestPhaseTypeDef",
    "CreateProxyRulesRequestTypeDef",
    "CreateProxyRulesResponseTypeDef",
    "CreateRuleGroupRequestTypeDef",
    "CreateRuleGroupResponseTypeDef",
    "CreateTLSInspectionConfigurationRequestTypeDef",
    "CreateTLSInspectionConfigurationResponseTypeDef",
    "CreateVpcEndpointAssociationRequestTypeDef",
    "CreateVpcEndpointAssociationResponseTypeDef",
    "CustomActionOutputTypeDef",
    "CustomActionTypeDef",
    "DeleteFirewallPolicyRequestTypeDef",
    "DeleteFirewallPolicyResponseTypeDef",
    "DeleteFirewallRequestTypeDef",
    "DeleteFirewallResponseTypeDef",
    "DeleteNetworkFirewallTransitGatewayAttachmentRequestTypeDef",
    "DeleteNetworkFirewallTransitGatewayAttachmentResponseTypeDef",
    "DeleteProxyConfigurationRequestTypeDef",
    "DeleteProxyConfigurationResponseTypeDef",
    "DeleteProxyRequestTypeDef",
    "DeleteProxyResponseTypeDef",
    "DeleteProxyRuleGroupRequestTypeDef",
    "DeleteProxyRuleGroupResponseTypeDef",
    "DeleteProxyRulesRequestTypeDef",
    "DeleteProxyRulesResponseTypeDef",
    "DeleteResourcePolicyRequestTypeDef",
    "DeleteRuleGroupRequestTypeDef",
    "DeleteRuleGroupResponseTypeDef",
    "DeleteTLSInspectionConfigurationRequestTypeDef",
    "DeleteTLSInspectionConfigurationResponseTypeDef",
    "DeleteVpcEndpointAssociationRequestTypeDef",
    "DeleteVpcEndpointAssociationResponseTypeDef",
    "DescribeFirewallMetadataRequestTypeDef",
    "DescribeFirewallMetadataResponseTypeDef",
    "DescribeFirewallPolicyRequestTypeDef",
    "DescribeFirewallPolicyResponseTypeDef",
    "DescribeFirewallRequestTypeDef",
    "DescribeFirewallResponseTypeDef",
    "DescribeFlowOperationRequestTypeDef",
    "DescribeFlowOperationResponseTypeDef",
    "DescribeLoggingConfigurationRequestTypeDef",
    "DescribeLoggingConfigurationResponseTypeDef",
    "DescribeProxyConfigurationRequestTypeDef",
    "DescribeProxyConfigurationResponseTypeDef",
    "DescribeProxyRequestTypeDef",
    "DescribeProxyResourceTypeDef",
    "DescribeProxyResponseTypeDef",
    "DescribeProxyRuleGroupRequestTypeDef",
    "DescribeProxyRuleGroupResponseTypeDef",
    "DescribeProxyRuleRequestTypeDef",
    "DescribeProxyRuleResponseTypeDef",
    "DescribeResourcePolicyRequestTypeDef",
    "DescribeResourcePolicyResponseTypeDef",
    "DescribeRuleGroupMetadataRequestTypeDef",
    "DescribeRuleGroupMetadataResponseTypeDef",
    "DescribeRuleGroupRequestTypeDef",
    "DescribeRuleGroupResponseTypeDef",
    "DescribeRuleGroupSummaryRequestTypeDef",
    "DescribeRuleGroupSummaryResponseTypeDef",
    "DescribeTLSInspectionConfigurationRequestTypeDef",
    "DescribeTLSInspectionConfigurationResponseTypeDef",
    "DescribeVpcEndpointAssociationRequestTypeDef",
    "DescribeVpcEndpointAssociationResponseTypeDef",
    "DetachRuleGroupsFromProxyConfigurationRequestTypeDef",
    "DetachRuleGroupsFromProxyConfigurationResponseTypeDef",
    "DimensionTypeDef",
    "DisassociateAvailabilityZonesRequestTypeDef",
    "DisassociateAvailabilityZonesResponseTypeDef",
    "DisassociateSubnetsRequestTypeDef",
    "DisassociateSubnetsResponseTypeDef",
    "EncryptionConfigurationTypeDef",
    "FirewallMetadataTypeDef",
    "FirewallPolicyMetadataTypeDef",
    "FirewallPolicyOutputTypeDef",
    "FirewallPolicyResponseTypeDef",
    "FirewallPolicyTypeDef",
    "FirewallPolicyUnionTypeDef",
    "FirewallStatusTypeDef",
    "FirewallTypeDef",
    "FlowFilterOutputTypeDef",
    "FlowFilterTypeDef",
    "FlowFilterUnionTypeDef",
    "FlowOperationMetadataTypeDef",
    "FlowOperationTypeDef",
    "FlowTimeoutsTypeDef",
    "FlowTypeDef",
    "GetAnalysisReportResultsRequestPaginateTypeDef",
    "GetAnalysisReportResultsRequestTypeDef",
    "GetAnalysisReportResultsResponseTypeDef",
    "HeaderTypeDef",
    "HitsTypeDef",
    "IPSetMetadataTypeDef",
    "IPSetOutputTypeDef",
    "IPSetReferenceTypeDef",
    "IPSetTypeDef",
    "ListAnalysisReportsRequestPaginateTypeDef",
    "ListAnalysisReportsRequestTypeDef",
    "ListAnalysisReportsResponseTypeDef",
    "ListFirewallPoliciesRequestPaginateTypeDef",
    "ListFirewallPoliciesRequestTypeDef",
    "ListFirewallPoliciesResponseTypeDef",
    "ListFirewallsRequestPaginateTypeDef",
    "ListFirewallsRequestTypeDef",
    "ListFirewallsResponseTypeDef",
    "ListFlowOperationResultsRequestPaginateTypeDef",
    "ListFlowOperationResultsRequestTypeDef",
    "ListFlowOperationResultsResponseTypeDef",
    "ListFlowOperationsRequestPaginateTypeDef",
    "ListFlowOperationsRequestTypeDef",
    "ListFlowOperationsResponseTypeDef",
    "ListProxiesRequestPaginateTypeDef",
    "ListProxiesRequestTypeDef",
    "ListProxiesResponseTypeDef",
    "ListProxyConfigurationsRequestPaginateTypeDef",
    "ListProxyConfigurationsRequestTypeDef",
    "ListProxyConfigurationsResponseTypeDef",
    "ListProxyRuleGroupsRequestPaginateTypeDef",
    "ListProxyRuleGroupsRequestTypeDef",
    "ListProxyRuleGroupsResponseTypeDef",
    "ListRuleGroupsRequestPaginateTypeDef",
    "ListRuleGroupsRequestTypeDef",
    "ListRuleGroupsResponseTypeDef",
    "ListTLSInspectionConfigurationsRequestPaginateTypeDef",
    "ListTLSInspectionConfigurationsRequestTypeDef",
    "ListTLSInspectionConfigurationsResponseTypeDef",
    "ListTagsForResourceRequestPaginateTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListVpcEndpointAssociationsRequestPaginateTypeDef",
    "ListVpcEndpointAssociationsRequestTypeDef",
    "ListVpcEndpointAssociationsResponseTypeDef",
    "ListenerPropertyRequestTypeDef",
    "ListenerPropertyTypeDef",
    "LogDestinationConfigOutputTypeDef",
    "LogDestinationConfigTypeDef",
    "LoggingConfigurationOutputTypeDef",
    "LoggingConfigurationTypeDef",
    "LoggingConfigurationUnionTypeDef",
    "MatchAttributesOutputTypeDef",
    "MatchAttributesTypeDef",
    "PaginatorConfigTypeDef",
    "PerObjectStatusTypeDef",
    "PolicyVariablesOutputTypeDef",
    "PolicyVariablesTypeDef",
    "PortRangeTypeDef",
    "PortSetOutputTypeDef",
    "PortSetTypeDef",
    "ProxyConfigDefaultRulePhaseActionsRequestTypeDef",
    "ProxyConfigRuleGroupTypeDef",
    "ProxyConfigurationMetadataTypeDef",
    "ProxyConfigurationTypeDef",
    "ProxyMetadataTypeDef",
    "ProxyRuleConditionOutputTypeDef",
    "ProxyRuleConditionTypeDef",
    "ProxyRuleConditionUnionTypeDef",
    "ProxyRuleGroupAttachmentTypeDef",
    "ProxyRuleGroupMetadataTypeDef",
    "ProxyRuleGroupPriorityResultTypeDef",
    "ProxyRuleGroupPriorityTypeDef",
    "ProxyRuleGroupTypeDef",
    "ProxyRuleOutputTypeDef",
    "ProxyRulePriorityTypeDef",
    "ProxyRuleTypeDef",
    "ProxyRulesByRequestPhaseOutputTypeDef",
    "ProxyRulesByRequestPhaseTypeDef",
    "ProxyRulesByRequestPhaseUnionTypeDef",
    "ProxyTypeDef",
    "PublishMetricActionOutputTypeDef",
    "PublishMetricActionTypeDef",
    "PutResourcePolicyRequestTypeDef",
    "ReferenceSetsOutputTypeDef",
    "ReferenceSetsTypeDef",
    "RejectNetworkFirewallTransitGatewayAttachmentRequestTypeDef",
    "RejectNetworkFirewallTransitGatewayAttachmentResponseTypeDef",
    "ResponseMetadataTypeDef",
    "RuleDefinitionOutputTypeDef",
    "RuleDefinitionTypeDef",
    "RuleGroupMetadataTypeDef",
    "RuleGroupOutputTypeDef",
    "RuleGroupResponseTypeDef",
    "RuleGroupTypeDef",
    "RuleGroupUnionTypeDef",
    "RuleOptionOutputTypeDef",
    "RuleOptionTypeDef",
    "RuleSummaryTypeDef",
    "RuleVariablesOutputTypeDef",
    "RuleVariablesTypeDef",
    "RulesSourceListOutputTypeDef",
    "RulesSourceListTypeDef",
    "RulesSourceOutputTypeDef",
    "RulesSourceTypeDef",
    "ServerCertificateConfigurationOutputTypeDef",
    "ServerCertificateConfigurationTypeDef",
    "ServerCertificateScopeOutputTypeDef",
    "ServerCertificateScopeTypeDef",
    "ServerCertificateTypeDef",
    "SourceMetadataTypeDef",
    "StartAnalysisReportRequestTypeDef",
    "StartAnalysisReportResponseTypeDef",
    "StartFlowCaptureRequestTypeDef",
    "StartFlowCaptureResponseTypeDef",
    "StartFlowFlushRequestTypeDef",
    "StartFlowFlushResponseTypeDef",
    "StatefulEngineOptionsTypeDef",
    "StatefulRuleGroupOverrideTypeDef",
    "StatefulRuleGroupReferenceTypeDef",
    "StatefulRuleOptionsTypeDef",
    "StatefulRuleOutputTypeDef",
    "StatefulRuleTypeDef",
    "StatelessRuleGroupReferenceTypeDef",
    "StatelessRuleOutputTypeDef",
    "StatelessRuleTypeDef",
    "StatelessRulesAndCustomActionsOutputTypeDef",
    "StatelessRulesAndCustomActionsTypeDef",
    "SubnetMappingTypeDef",
    "SummaryConfigurationOutputTypeDef",
    "SummaryConfigurationTypeDef",
    "SummaryConfigurationUnionTypeDef",
    "SummaryTypeDef",
    "SyncStateTypeDef",
    "TCPFlagFieldOutputTypeDef",
    "TCPFlagFieldTypeDef",
    "TLSInspectionConfigurationMetadataTypeDef",
    "TLSInspectionConfigurationOutputTypeDef",
    "TLSInspectionConfigurationResponseTypeDef",
    "TLSInspectionConfigurationTypeDef",
    "TLSInspectionConfigurationUnionTypeDef",
    "TagResourceRequestTypeDef",
    "TagTypeDef",
    "TlsCertificateDataTypeDef",
    "TlsInterceptPropertiesRequestTypeDef",
    "TlsInterceptPropertiesTypeDef",
    "TransitGatewayAttachmentSyncStateTypeDef",
    "UniqueSourcesTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateAvailabilityZoneChangeProtectionRequestTypeDef",
    "UpdateAvailabilityZoneChangeProtectionResponseTypeDef",
    "UpdateFirewallAnalysisSettingsRequestTypeDef",
    "UpdateFirewallAnalysisSettingsResponseTypeDef",
    "UpdateFirewallDeleteProtectionRequestTypeDef",
    "UpdateFirewallDeleteProtectionResponseTypeDef",
    "UpdateFirewallDescriptionRequestTypeDef",
    "UpdateFirewallDescriptionResponseTypeDef",
    "UpdateFirewallEncryptionConfigurationRequestTypeDef",
    "UpdateFirewallEncryptionConfigurationResponseTypeDef",
    "UpdateFirewallPolicyChangeProtectionRequestTypeDef",
    "UpdateFirewallPolicyChangeProtectionResponseTypeDef",
    "UpdateFirewallPolicyRequestTypeDef",
    "UpdateFirewallPolicyResponseTypeDef",
    "UpdateLoggingConfigurationRequestTypeDef",
    "UpdateLoggingConfigurationResponseTypeDef",
    "UpdateProxyConfigurationRequestTypeDef",
    "UpdateProxyConfigurationResponseTypeDef",
    "UpdateProxyRequestTypeDef",
    "UpdateProxyResponseTypeDef",
    "UpdateProxyRuleGroupPrioritiesRequestTypeDef",
    "UpdateProxyRuleGroupPrioritiesResponseTypeDef",
    "UpdateProxyRulePrioritiesRequestTypeDef",
    "UpdateProxyRulePrioritiesResponseTypeDef",
    "UpdateProxyRuleRequestTypeDef",
    "UpdateProxyRuleResponseTypeDef",
    "UpdateRuleGroupRequestTypeDef",
    "UpdateRuleGroupResponseTypeDef",
    "UpdateSubnetChangeProtectionRequestTypeDef",
    "UpdateSubnetChangeProtectionResponseTypeDef",
    "UpdateTLSInspectionConfigurationRequestTypeDef",
    "UpdateTLSInspectionConfigurationResponseTypeDef",
    "VpcEndpointAssociationMetadataTypeDef",
    "VpcEndpointAssociationStatusTypeDef",
    "VpcEndpointAssociationTypeDef",
)


class AttachmentTypeDef(TypedDict):
    SubnetId: NotRequired[str]
    EndpointId: NotRequired[str]
    Status: NotRequired[AttachmentStatusType]
    StatusMessage: NotRequired[str]


class AcceptNetworkFirewallTransitGatewayAttachmentRequestTypeDef(TypedDict):
    TransitGatewayAttachmentId: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AddressTypeDef(TypedDict):
    AddressDefinition: str


class AnalysisReportTypeDef(TypedDict):
    AnalysisReportId: NotRequired[str]
    AnalysisType: NotRequired[EnabledAnalysisTypeType]
    ReportTime: NotRequired[datetime]
    Status: NotRequired[str]


class AnalysisResultTypeDef(TypedDict):
    IdentifiedRuleIds: NotRequired[list[str]]
    IdentifiedType: NotRequired[IdentifiedTypeType]
    AnalysisDetail: NotRequired[str]


class HitsTypeDef(TypedDict):
    Count: NotRequired[int]


class UniqueSourcesTypeDef(TypedDict):
    Count: NotRequired[int]


class AvailabilityZoneMappingTypeDef(TypedDict):
    AvailabilityZone: str


class AssociateFirewallPolicyRequestTypeDef(TypedDict):
    FirewallPolicyArn: str
    UpdateToken: NotRequired[str]
    FirewallArn: NotRequired[str]
    FirewallName: NotRequired[str]


class SubnetMappingTypeDef(TypedDict):
    SubnetId: str
    IPAddressType: NotRequired[IPAddressTypeType]


class ProxyRuleGroupAttachmentTypeDef(TypedDict):
    ProxyRuleGroupName: NotRequired[str]
    InsertPosition: NotRequired[int]


class AvailabilityZoneMetadataTypeDef(TypedDict):
    IPAddressType: NotRequired[IPAddressTypeType]


class IPSetMetadataTypeDef(TypedDict):
    ResolvedCIDRCount: NotRequired[int]


class CheckCertificateRevocationStatusActionsTypeDef(TypedDict):
    RevokedStatusAction: NotRequired[RevocationCheckActionType]
    UnknownStatusAction: NotRequired[RevocationCheckActionType]


EncryptionConfigurationTypeDef = TypedDict(
    "EncryptionConfigurationTypeDef",
    {
        "Type": EncryptionTypeType,
        "KeyId": NotRequired[str],
    },
)


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class ProxyConfigDefaultRulePhaseActionsRequestTypeDef(TypedDict):
    PreDNS: NotRequired[ProxyRulePhaseActionType]
    PreREQUEST: NotRequired[ProxyRulePhaseActionType]
    PostRESPONSE: NotRequired[ProxyRulePhaseActionType]


ListenerPropertyRequestTypeDef = TypedDict(
    "ListenerPropertyRequestTypeDef",
    {
        "Port": int,
        "Type": ListenerPropertyTypeType,
    },
)


class TlsInterceptPropertiesRequestTypeDef(TypedDict):
    PcaArn: NotRequired[str]
    TlsInterceptMode: NotRequired[TlsInterceptModeType]


class SourceMetadataTypeDef(TypedDict):
    SourceArn: NotRequired[str]
    SourceUpdateToken: NotRequired[str]


class DeleteFirewallPolicyRequestTypeDef(TypedDict):
    FirewallPolicyName: NotRequired[str]
    FirewallPolicyArn: NotRequired[str]


class DeleteFirewallRequestTypeDef(TypedDict):
    FirewallName: NotRequired[str]
    FirewallArn: NotRequired[str]


class DeleteNetworkFirewallTransitGatewayAttachmentRequestTypeDef(TypedDict):
    TransitGatewayAttachmentId: str


class DeleteProxyConfigurationRequestTypeDef(TypedDict):
    ProxyConfigurationName: NotRequired[str]
    ProxyConfigurationArn: NotRequired[str]


class DeleteProxyRequestTypeDef(TypedDict):
    NatGatewayId: str
    ProxyName: NotRequired[str]
    ProxyArn: NotRequired[str]


class DeleteProxyRuleGroupRequestTypeDef(TypedDict):
    ProxyRuleGroupName: NotRequired[str]
    ProxyRuleGroupArn: NotRequired[str]


class DeleteProxyRulesRequestTypeDef(TypedDict):
    Rules: Sequence[str]
    ProxyRuleGroupArn: NotRequired[str]
    ProxyRuleGroupName: NotRequired[str]


class DeleteResourcePolicyRequestTypeDef(TypedDict):
    ResourceArn: str


DeleteRuleGroupRequestTypeDef = TypedDict(
    "DeleteRuleGroupRequestTypeDef",
    {
        "RuleGroupName": NotRequired[str],
        "RuleGroupArn": NotRequired[str],
        "Type": NotRequired[RuleGroupTypeType],
    },
)


class DeleteTLSInspectionConfigurationRequestTypeDef(TypedDict):
    TLSInspectionConfigurationArn: NotRequired[str]
    TLSInspectionConfigurationName: NotRequired[str]


class DeleteVpcEndpointAssociationRequestTypeDef(TypedDict):
    VpcEndpointAssociationArn: str


class DescribeFirewallMetadataRequestTypeDef(TypedDict):
    FirewallArn: NotRequired[str]


class DescribeFirewallPolicyRequestTypeDef(TypedDict):
    FirewallPolicyName: NotRequired[str]
    FirewallPolicyArn: NotRequired[str]


class DescribeFirewallRequestTypeDef(TypedDict):
    FirewallName: NotRequired[str]
    FirewallArn: NotRequired[str]


class DescribeFlowOperationRequestTypeDef(TypedDict):
    FirewallArn: str
    FlowOperationId: str
    AvailabilityZone: NotRequired[str]
    VpcEndpointAssociationArn: NotRequired[str]
    VpcEndpointId: NotRequired[str]


class DescribeLoggingConfigurationRequestTypeDef(TypedDict):
    FirewallArn: NotRequired[str]
    FirewallName: NotRequired[str]


class DescribeProxyConfigurationRequestTypeDef(TypedDict):
    ProxyConfigurationName: NotRequired[str]
    ProxyConfigurationArn: NotRequired[str]


class DescribeProxyRequestTypeDef(TypedDict):
    ProxyName: NotRequired[str]
    ProxyArn: NotRequired[str]


ListenerPropertyTypeDef = TypedDict(
    "ListenerPropertyTypeDef",
    {
        "Port": NotRequired[int],
        "Type": NotRequired[ListenerPropertyTypeType],
    },
)


class TlsInterceptPropertiesTypeDef(TypedDict):
    PcaArn: NotRequired[str]
    TlsInterceptMode: NotRequired[TlsInterceptModeType]


class DescribeProxyRuleGroupRequestTypeDef(TypedDict):
    ProxyRuleGroupName: NotRequired[str]
    ProxyRuleGroupArn: NotRequired[str]


class DescribeProxyRuleRequestTypeDef(TypedDict):
    ProxyRuleName: str
    ProxyRuleGroupName: NotRequired[str]
    ProxyRuleGroupArn: NotRequired[str]


class DescribeResourcePolicyRequestTypeDef(TypedDict):
    ResourceArn: str


DescribeRuleGroupMetadataRequestTypeDef = TypedDict(
    "DescribeRuleGroupMetadataRequestTypeDef",
    {
        "RuleGroupName": NotRequired[str],
        "RuleGroupArn": NotRequired[str],
        "Type": NotRequired[RuleGroupTypeType],
    },
)


class StatefulRuleOptionsTypeDef(TypedDict):
    RuleOrder: NotRequired[RuleOrderType]


DescribeRuleGroupRequestTypeDef = TypedDict(
    "DescribeRuleGroupRequestTypeDef",
    {
        "RuleGroupName": NotRequired[str],
        "RuleGroupArn": NotRequired[str],
        "Type": NotRequired[RuleGroupTypeType],
        "AnalyzeRuleGroup": NotRequired[bool],
    },
)
DescribeRuleGroupSummaryRequestTypeDef = TypedDict(
    "DescribeRuleGroupSummaryRequestTypeDef",
    {
        "RuleGroupName": NotRequired[str],
        "RuleGroupArn": NotRequired[str],
        "Type": NotRequired[RuleGroupTypeType],
    },
)


class DescribeTLSInspectionConfigurationRequestTypeDef(TypedDict):
    TLSInspectionConfigurationArn: NotRequired[str]
    TLSInspectionConfigurationName: NotRequired[str]


class DescribeVpcEndpointAssociationRequestTypeDef(TypedDict):
    VpcEndpointAssociationArn: str


class DetachRuleGroupsFromProxyConfigurationRequestTypeDef(TypedDict):
    UpdateToken: str
    ProxyConfigurationName: NotRequired[str]
    ProxyConfigurationArn: NotRequired[str]
    RuleGroupNames: NotRequired[Sequence[str]]
    RuleGroupArns: NotRequired[Sequence[str]]


class DimensionTypeDef(TypedDict):
    Value: str


class DisassociateSubnetsRequestTypeDef(TypedDict):
    SubnetIds: Sequence[str]
    UpdateToken: NotRequired[str]
    FirewallArn: NotRequired[str]
    FirewallName: NotRequired[str]


class FirewallMetadataTypeDef(TypedDict):
    FirewallName: NotRequired[str]
    FirewallArn: NotRequired[str]
    TransitGatewayAttachmentId: NotRequired[str]


class FirewallPolicyMetadataTypeDef(TypedDict):
    Name: NotRequired[str]
    Arn: NotRequired[str]


class StatelessRuleGroupReferenceTypeDef(TypedDict):
    ResourceArn: str
    Priority: int


class TransitGatewayAttachmentSyncStateTypeDef(TypedDict):
    AttachmentId: NotRequired[str]
    TransitGatewayAttachmentStatus: NotRequired[TransitGatewayAttachmentStatusType]
    StatusMessage: NotRequired[str]


class FlowOperationMetadataTypeDef(TypedDict):
    FlowOperationId: NotRequired[str]
    FlowOperationType: NotRequired[FlowOperationTypeType]
    FlowRequestTimestamp: NotRequired[datetime]
    FlowOperationStatus: NotRequired[FlowOperationStatusType]


class FlowTimeoutsTypeDef(TypedDict):
    TcpIdleTimeoutSeconds: NotRequired[int]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class GetAnalysisReportResultsRequestTypeDef(TypedDict):
    AnalysisReportId: str
    FirewallName: NotRequired[str]
    FirewallArn: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


HeaderTypeDef = TypedDict(
    "HeaderTypeDef",
    {
        "Protocol": StatefulRuleProtocolType,
        "Source": str,
        "SourcePort": str,
        "Direction": StatefulRuleDirectionType,
        "Destination": str,
        "DestinationPort": str,
    },
)


class IPSetOutputTypeDef(TypedDict):
    Definition: list[str]


class IPSetReferenceTypeDef(TypedDict):
    ReferenceArn: NotRequired[str]


class IPSetTypeDef(TypedDict):
    Definition: Sequence[str]


class ListAnalysisReportsRequestTypeDef(TypedDict):
    FirewallName: NotRequired[str]
    FirewallArn: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListFirewallPoliciesRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListFirewallsRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    VpcIds: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]


class ListFlowOperationResultsRequestTypeDef(TypedDict):
    FirewallArn: str
    FlowOperationId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    AvailabilityZone: NotRequired[str]
    VpcEndpointId: NotRequired[str]
    VpcEndpointAssociationArn: NotRequired[str]


class ListFlowOperationsRequestTypeDef(TypedDict):
    FirewallArn: str
    AvailabilityZone: NotRequired[str]
    VpcEndpointAssociationArn: NotRequired[str]
    VpcEndpointId: NotRequired[str]
    FlowOperationType: NotRequired[FlowOperationTypeType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListProxiesRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ProxyMetadataTypeDef(TypedDict):
    Name: NotRequired[str]
    Arn: NotRequired[str]


class ListProxyConfigurationsRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ProxyConfigurationMetadataTypeDef(TypedDict):
    Name: NotRequired[str]
    Arn: NotRequired[str]


class ListProxyRuleGroupsRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ProxyRuleGroupMetadataTypeDef(TypedDict):
    Name: NotRequired[str]
    Arn: NotRequired[str]


ListRuleGroupsRequestTypeDef = TypedDict(
    "ListRuleGroupsRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "Scope": NotRequired[ResourceManagedStatusType],
        "ManagedType": NotRequired[ResourceManagedTypeType],
        "SubscriptionStatus": NotRequired[SubscriptionStatusType],
        "Type": NotRequired[RuleGroupTypeType],
    },
)


class RuleGroupMetadataTypeDef(TypedDict):
    Name: NotRequired[str]
    Arn: NotRequired[str]
    VendorName: NotRequired[str]


class ListTLSInspectionConfigurationsRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class TLSInspectionConfigurationMetadataTypeDef(TypedDict):
    Name: NotRequired[str]
    Arn: NotRequired[str]


class ListTagsForResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListVpcEndpointAssociationsRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    FirewallArn: NotRequired[str]


class VpcEndpointAssociationMetadataTypeDef(TypedDict):
    VpcEndpointAssociationArn: NotRequired[str]


class LogDestinationConfigOutputTypeDef(TypedDict):
    LogType: LogTypeType
    LogDestinationType: LogDestinationTypeType
    LogDestination: dict[str, str]


class LogDestinationConfigTypeDef(TypedDict):
    LogType: LogTypeType
    LogDestinationType: LogDestinationTypeType
    LogDestination: Mapping[str, str]


class PortRangeTypeDef(TypedDict):
    FromPort: int
    ToPort: int


class TCPFlagFieldOutputTypeDef(TypedDict):
    Flags: list[TCPFlagType]
    Masks: NotRequired[list[TCPFlagType]]


class TCPFlagFieldTypeDef(TypedDict):
    Flags: Sequence[TCPFlagType]
    Masks: NotRequired[Sequence[TCPFlagType]]


class PerObjectStatusTypeDef(TypedDict):
    SyncStatus: NotRequired[PerObjectSyncStatusType]
    UpdateToken: NotRequired[str]


class PortSetOutputTypeDef(TypedDict):
    Definition: NotRequired[list[str]]


class PortSetTypeDef(TypedDict):
    Definition: NotRequired[Sequence[str]]


ProxyConfigRuleGroupTypeDef = TypedDict(
    "ProxyConfigRuleGroupTypeDef",
    {
        "ProxyRuleGroupName": NotRequired[str],
        "ProxyRuleGroupArn": NotRequired[str],
        "Type": NotRequired[str],
        "Priority": NotRequired[int],
    },
)


class ProxyRuleConditionOutputTypeDef(TypedDict):
    ConditionOperator: NotRequired[str]
    ConditionKey: NotRequired[str]
    ConditionValues: NotRequired[list[str]]


class ProxyRuleConditionTypeDef(TypedDict):
    ConditionOperator: NotRequired[str]
    ConditionKey: NotRequired[str]
    ConditionValues: NotRequired[Sequence[str]]


class ProxyRuleGroupPriorityResultTypeDef(TypedDict):
    ProxyRuleGroupName: NotRequired[str]
    Priority: NotRequired[int]


class ProxyRuleGroupPriorityTypeDef(TypedDict):
    ProxyRuleGroupName: NotRequired[str]
    NewPosition: NotRequired[int]


class ProxyRulePriorityTypeDef(TypedDict):
    ProxyRuleName: NotRequired[str]
    NewPosition: NotRequired[int]


class PutResourcePolicyRequestTypeDef(TypedDict):
    ResourceArn: str
    Policy: str


class RejectNetworkFirewallTransitGatewayAttachmentRequestTypeDef(TypedDict):
    TransitGatewayAttachmentId: str


class SummaryConfigurationOutputTypeDef(TypedDict):
    RuleOptions: NotRequired[list[SummaryRuleOptionType]]


class RuleOptionOutputTypeDef(TypedDict):
    Keyword: str
    Settings: NotRequired[list[str]]


class RuleOptionTypeDef(TypedDict):
    Keyword: str
    Settings: NotRequired[Sequence[str]]


class RuleSummaryTypeDef(TypedDict):
    SID: NotRequired[str]
    Msg: NotRequired[str]
    Metadata: NotRequired[str]


class RulesSourceListOutputTypeDef(TypedDict):
    Targets: list[str]
    TargetTypes: list[TargetTypeType]
    GeneratedRulesType: GeneratedRulesTypeType


class RulesSourceListTypeDef(TypedDict):
    Targets: Sequence[str]
    TargetTypes: Sequence[TargetTypeType]
    GeneratedRulesType: GeneratedRulesTypeType


class ServerCertificateTypeDef(TypedDict):
    ResourceArn: NotRequired[str]


class StartAnalysisReportRequestTypeDef(TypedDict):
    AnalysisType: EnabledAnalysisTypeType
    FirewallName: NotRequired[str]
    FirewallArn: NotRequired[str]


class StatefulRuleGroupOverrideTypeDef(TypedDict):
    Action: NotRequired[Literal["DROP_TO_ALERT"]]


class SummaryConfigurationTypeDef(TypedDict):
    RuleOptions: NotRequired[Sequence[SummaryRuleOptionType]]


class TlsCertificateDataTypeDef(TypedDict):
    CertificateArn: NotRequired[str]
    CertificateSerial: NotRequired[str]
    Status: NotRequired[str]
    StatusMessage: NotRequired[str]


class UntagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class UpdateAvailabilityZoneChangeProtectionRequestTypeDef(TypedDict):
    AvailabilityZoneChangeProtection: bool
    UpdateToken: NotRequired[str]
    FirewallArn: NotRequired[str]
    FirewallName: NotRequired[str]


class UpdateFirewallAnalysisSettingsRequestTypeDef(TypedDict):
    EnabledAnalysisTypes: NotRequired[Sequence[EnabledAnalysisTypeType]]
    FirewallArn: NotRequired[str]
    FirewallName: NotRequired[str]
    UpdateToken: NotRequired[str]


class UpdateFirewallDeleteProtectionRequestTypeDef(TypedDict):
    DeleteProtection: bool
    UpdateToken: NotRequired[str]
    FirewallArn: NotRequired[str]
    FirewallName: NotRequired[str]


class UpdateFirewallDescriptionRequestTypeDef(TypedDict):
    UpdateToken: NotRequired[str]
    FirewallArn: NotRequired[str]
    FirewallName: NotRequired[str]
    Description: NotRequired[str]


class UpdateFirewallPolicyChangeProtectionRequestTypeDef(TypedDict):
    FirewallPolicyChangeProtection: bool
    UpdateToken: NotRequired[str]
    FirewallArn: NotRequired[str]
    FirewallName: NotRequired[str]


class UpdateSubnetChangeProtectionRequestTypeDef(TypedDict):
    SubnetChangeProtection: bool
    UpdateToken: NotRequired[str]
    FirewallArn: NotRequired[str]
    FirewallName: NotRequired[str]


class AZSyncStateTypeDef(TypedDict):
    Attachment: NotRequired[AttachmentTypeDef]


class AcceptNetworkFirewallTransitGatewayAttachmentResponseTypeDef(TypedDict):
    TransitGatewayAttachmentId: str
    TransitGatewayAttachmentStatus: TransitGatewayAttachmentStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateFirewallPolicyResponseTypeDef(TypedDict):
    FirewallArn: str
    FirewallName: str
    FirewallPolicyArn: str
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteNetworkFirewallTransitGatewayAttachmentResponseTypeDef(TypedDict):
    TransitGatewayAttachmentId: str
    TransitGatewayAttachmentStatus: TransitGatewayAttachmentStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteProxyConfigurationResponseTypeDef(TypedDict):
    ProxyConfigurationName: str
    ProxyConfigurationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteProxyResponseTypeDef(TypedDict):
    NatGatewayId: str
    ProxyName: str
    ProxyArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteProxyRuleGroupResponseTypeDef(TypedDict):
    ProxyRuleGroupName: str
    ProxyRuleGroupArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeResourcePolicyResponseTypeDef(TypedDict):
    Policy: str
    ResponseMetadata: ResponseMetadataTypeDef


class RejectNetworkFirewallTransitGatewayAttachmentResponseTypeDef(TypedDict):
    TransitGatewayAttachmentId: str
    TransitGatewayAttachmentStatus: TransitGatewayAttachmentStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class StartAnalysisReportResponseTypeDef(TypedDict):
    AnalysisReportId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartFlowCaptureResponseTypeDef(TypedDict):
    FirewallArn: str
    FlowOperationId: str
    FlowOperationStatus: FlowOperationStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class StartFlowFlushResponseTypeDef(TypedDict):
    FirewallArn: str
    FlowOperationId: str
    FlowOperationStatus: FlowOperationStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAvailabilityZoneChangeProtectionResponseTypeDef(TypedDict):
    UpdateToken: str
    FirewallArn: str
    FirewallName: str
    AvailabilityZoneChangeProtection: bool
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateFirewallAnalysisSettingsResponseTypeDef(TypedDict):
    EnabledAnalysisTypes: list[EnabledAnalysisTypeType]
    FirewallArn: str
    FirewallName: str
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateFirewallDeleteProtectionResponseTypeDef(TypedDict):
    FirewallArn: str
    FirewallName: str
    DeleteProtection: bool
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateFirewallDescriptionResponseTypeDef(TypedDict):
    FirewallArn: str
    FirewallName: str
    Description: str
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateFirewallPolicyChangeProtectionResponseTypeDef(TypedDict):
    UpdateToken: str
    FirewallArn: str
    FirewallName: str
    FirewallPolicyChangeProtection: bool
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSubnetChangeProtectionResponseTypeDef(TypedDict):
    UpdateToken: str
    FirewallArn: str
    FirewallName: str
    SubnetChangeProtection: bool
    ResponseMetadata: ResponseMetadataTypeDef


class FlowFilterOutputTypeDef(TypedDict):
    SourceAddress: NotRequired[AddressTypeDef]
    DestinationAddress: NotRequired[AddressTypeDef]
    SourcePort: NotRequired[str]
    DestinationPort: NotRequired[str]
    Protocols: NotRequired[list[str]]


class FlowFilterTypeDef(TypedDict):
    SourceAddress: NotRequired[AddressTypeDef]
    DestinationAddress: NotRequired[AddressTypeDef]
    SourcePort: NotRequired[str]
    DestinationPort: NotRequired[str]
    Protocols: NotRequired[Sequence[str]]


FlowTypeDef = TypedDict(
    "FlowTypeDef",
    {
        "SourceAddress": NotRequired[AddressTypeDef],
        "DestinationAddress": NotRequired[AddressTypeDef],
        "SourcePort": NotRequired[str],
        "DestinationPort": NotRequired[str],
        "Protocol": NotRequired[str],
        "Age": NotRequired[int],
        "PacketCount": NotRequired[int],
        "ByteCount": NotRequired[int],
    },
)


class ListAnalysisReportsResponseTypeDef(TypedDict):
    AnalysisReports: list[AnalysisReportTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


AnalysisTypeReportResultTypeDef = TypedDict(
    "AnalysisTypeReportResultTypeDef",
    {
        "Protocol": NotRequired[str],
        "FirstAccessed": NotRequired[datetime],
        "LastAccessed": NotRequired[datetime],
        "Domain": NotRequired[str],
        "Hits": NotRequired[HitsTypeDef],
        "UniqueSources": NotRequired[UniqueSourcesTypeDef],
    },
)


class AssociateAvailabilityZonesRequestTypeDef(TypedDict):
    AvailabilityZoneMappings: Sequence[AvailabilityZoneMappingTypeDef]
    UpdateToken: NotRequired[str]
    FirewallArn: NotRequired[str]
    FirewallName: NotRequired[str]


class AssociateAvailabilityZonesResponseTypeDef(TypedDict):
    FirewallArn: str
    FirewallName: str
    AvailabilityZoneMappings: list[AvailabilityZoneMappingTypeDef]
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateAvailabilityZonesRequestTypeDef(TypedDict):
    AvailabilityZoneMappings: Sequence[AvailabilityZoneMappingTypeDef]
    UpdateToken: NotRequired[str]
    FirewallArn: NotRequired[str]
    FirewallName: NotRequired[str]


class DisassociateAvailabilityZonesResponseTypeDef(TypedDict):
    FirewallArn: str
    FirewallName: str
    AvailabilityZoneMappings: list[AvailabilityZoneMappingTypeDef]
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateSubnetsRequestTypeDef(TypedDict):
    SubnetMappings: Sequence[SubnetMappingTypeDef]
    UpdateToken: NotRequired[str]
    FirewallArn: NotRequired[str]
    FirewallName: NotRequired[str]


class AssociateSubnetsResponseTypeDef(TypedDict):
    FirewallArn: str
    FirewallName: str
    SubnetMappings: list[SubnetMappingTypeDef]
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateSubnetsResponseTypeDef(TypedDict):
    FirewallArn: str
    FirewallName: str
    SubnetMappings: list[SubnetMappingTypeDef]
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class AttachRuleGroupsToProxyConfigurationRequestTypeDef(TypedDict):
    RuleGroups: Sequence[ProxyRuleGroupAttachmentTypeDef]
    UpdateToken: str
    ProxyConfigurationName: NotRequired[str]
    ProxyConfigurationArn: NotRequired[str]


class DescribeFirewallMetadataResponseTypeDef(TypedDict):
    FirewallArn: str
    FirewallPolicyArn: str
    Description: str
    Status: FirewallStatusValueType
    SupportedAvailabilityZones: dict[str, AvailabilityZoneMetadataTypeDef]
    TransitGatewayAttachmentId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CIDRSummaryTypeDef(TypedDict):
    AvailableCIDRCount: NotRequired[int]
    UtilizedCIDRCount: NotRequired[int]
    IPSetReferences: NotRequired[dict[str, IPSetMetadataTypeDef]]


class UpdateFirewallEncryptionConfigurationRequestTypeDef(TypedDict):
    UpdateToken: NotRequired[str]
    FirewallArn: NotRequired[str]
    FirewallName: NotRequired[str]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]


class UpdateFirewallEncryptionConfigurationResponseTypeDef(TypedDict):
    FirewallArn: str
    FirewallName: str
    UpdateToken: str
    EncryptionConfiguration: EncryptionConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFirewallRequestTypeDef(TypedDict):
    FirewallName: str
    FirewallPolicyArn: str
    VpcId: NotRequired[str]
    SubnetMappings: NotRequired[Sequence[SubnetMappingTypeDef]]
    DeleteProtection: NotRequired[bool]
    SubnetChangeProtection: NotRequired[bool]
    FirewallPolicyChangeProtection: NotRequired[bool]
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]
    EnabledAnalysisTypes: NotRequired[Sequence[EnabledAnalysisTypeType]]
    TransitGatewayId: NotRequired[str]
    AvailabilityZoneMappings: NotRequired[Sequence[AvailabilityZoneMappingTypeDef]]
    AvailabilityZoneChangeProtection: NotRequired[bool]


class CreateVpcEndpointAssociationRequestTypeDef(TypedDict):
    FirewallArn: str
    VpcId: str
    SubnetMapping: SubnetMappingTypeDef
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class FirewallPolicyResponseTypeDef(TypedDict):
    FirewallPolicyName: str
    FirewallPolicyArn: str
    FirewallPolicyId: str
    Description: NotRequired[str]
    FirewallPolicyStatus: NotRequired[ResourceStatusType]
    Tags: NotRequired[list[TagTypeDef]]
    ConsumedStatelessRuleCapacity: NotRequired[int]
    ConsumedStatefulRuleCapacity: NotRequired[int]
    NumberOfAssociations: NotRequired[int]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]
    LastModifiedTime: NotRequired[datetime]


class FirewallTypeDef(TypedDict):
    FirewallPolicyArn: str
    VpcId: str
    SubnetMappings: list[SubnetMappingTypeDef]
    FirewallId: str
    FirewallName: NotRequired[str]
    FirewallArn: NotRequired[str]
    DeleteProtection: NotRequired[bool]
    SubnetChangeProtection: NotRequired[bool]
    FirewallPolicyChangeProtection: NotRequired[bool]
    Description: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]
    NumberOfAssociations: NotRequired[int]
    EnabledAnalysisTypes: NotRequired[list[EnabledAnalysisTypeType]]
    TransitGatewayId: NotRequired[str]
    TransitGatewayOwnerAccountId: NotRequired[str]
    AvailabilityZoneMappings: NotRequired[list[AvailabilityZoneMappingTypeDef]]
    AvailabilityZoneChangeProtection: NotRequired[bool]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class TagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]


class VpcEndpointAssociationTypeDef(TypedDict):
    VpcEndpointAssociationArn: str
    FirewallArn: str
    VpcId: str
    SubnetMapping: SubnetMappingTypeDef
    VpcEndpointAssociationId: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


class CreateProxyConfigurationRequestTypeDef(TypedDict):
    ProxyConfigurationName: str
    DefaultRulePhaseActions: ProxyConfigDefaultRulePhaseActionsRequestTypeDef
    Description: NotRequired[str]
    RuleGroupNames: NotRequired[Sequence[str]]
    RuleGroupArns: NotRequired[Sequence[str]]
    Tags: NotRequired[Sequence[TagTypeDef]]


class UpdateProxyConfigurationRequestTypeDef(TypedDict):
    DefaultRulePhaseActions: ProxyConfigDefaultRulePhaseActionsRequestTypeDef
    UpdateToken: str
    ProxyConfigurationName: NotRequired[str]
    ProxyConfigurationArn: NotRequired[str]


class CreateProxyRequestTypeDef(TypedDict):
    ProxyName: str
    NatGatewayId: str
    TlsInterceptProperties: TlsInterceptPropertiesRequestTypeDef
    ProxyConfigurationName: NotRequired[str]
    ProxyConfigurationArn: NotRequired[str]
    ListenerProperties: NotRequired[Sequence[ListenerPropertyRequestTypeDef]]
    Tags: NotRequired[Sequence[TagTypeDef]]


class UpdateProxyRequestTypeDef(TypedDict):
    NatGatewayId: str
    UpdateToken: str
    ProxyName: NotRequired[str]
    ProxyArn: NotRequired[str]
    ListenerPropertiesToAdd: NotRequired[Sequence[ListenerPropertyRequestTypeDef]]
    ListenerPropertiesToRemove: NotRequired[Sequence[ListenerPropertyRequestTypeDef]]
    TlsInterceptProperties: NotRequired[TlsInterceptPropertiesRequestTypeDef]


class DescribeProxyResourceTypeDef(TypedDict):
    ProxyName: NotRequired[str]
    ProxyArn: NotRequired[str]
    ProxyConfigurationName: NotRequired[str]
    ProxyConfigurationArn: NotRequired[str]
    NatGatewayId: NotRequired[str]
    ProxyState: NotRequired[ProxyStateType]
    ProxyModifyState: NotRequired[ProxyModifyStateType]
    ListenerProperties: NotRequired[list[ListenerPropertyTypeDef]]
    TlsInterceptProperties: NotRequired[TlsInterceptPropertiesTypeDef]
    VpcEndpointServiceName: NotRequired[str]
    PrivateDNSName: NotRequired[str]
    CreateTime: NotRequired[datetime]
    DeleteTime: NotRequired[datetime]
    UpdateTime: NotRequired[datetime]
    FailureCode: NotRequired[str]
    FailureMessage: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


class ProxyTypeDef(TypedDict):
    CreateTime: NotRequired[datetime]
    DeleteTime: NotRequired[datetime]
    UpdateTime: NotRequired[datetime]
    FailureCode: NotRequired[str]
    FailureMessage: NotRequired[str]
    ProxyState: NotRequired[ProxyStateType]
    ProxyModifyState: NotRequired[ProxyModifyStateType]
    NatGatewayId: NotRequired[str]
    ProxyConfigurationName: NotRequired[str]
    ProxyConfigurationArn: NotRequired[str]
    ProxyName: NotRequired[str]
    ProxyArn: NotRequired[str]
    ListenerProperties: NotRequired[list[ListenerPropertyTypeDef]]
    TlsInterceptProperties: NotRequired[TlsInterceptPropertiesTypeDef]
    Tags: NotRequired[list[TagTypeDef]]


DescribeRuleGroupMetadataResponseTypeDef = TypedDict(
    "DescribeRuleGroupMetadataResponseTypeDef",
    {
        "RuleGroupArn": str,
        "RuleGroupName": str,
        "Description": str,
        "Type": RuleGroupTypeType,
        "Capacity": int,
        "StatefulRuleOptions": StatefulRuleOptionsTypeDef,
        "LastModifiedTime": datetime,
        "VendorName": str,
        "ProductId": str,
        "ListingName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class PublishMetricActionOutputTypeDef(TypedDict):
    Dimensions: list[DimensionTypeDef]


class PublishMetricActionTypeDef(TypedDict):
    Dimensions: Sequence[DimensionTypeDef]


class ListFirewallsResponseTypeDef(TypedDict):
    Firewalls: list[FirewallMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListFirewallPoliciesResponseTypeDef(TypedDict):
    FirewallPolicies: list[FirewallPolicyMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListFlowOperationsResponseTypeDef(TypedDict):
    FlowOperations: list[FlowOperationMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class StatefulEngineOptionsTypeDef(TypedDict):
    RuleOrder: NotRequired[RuleOrderType]
    StreamExceptionPolicy: NotRequired[StreamExceptionPolicyType]
    FlowTimeouts: NotRequired[FlowTimeoutsTypeDef]


class GetAnalysisReportResultsRequestPaginateTypeDef(TypedDict):
    AnalysisReportId: str
    FirewallName: NotRequired[str]
    FirewallArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAnalysisReportsRequestPaginateTypeDef(TypedDict):
    FirewallName: NotRequired[str]
    FirewallArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFirewallPoliciesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFirewallsRequestPaginateTypeDef(TypedDict):
    VpcIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFlowOperationResultsRequestPaginateTypeDef(TypedDict):
    FirewallArn: str
    FlowOperationId: str
    AvailabilityZone: NotRequired[str]
    VpcEndpointId: NotRequired[str]
    VpcEndpointAssociationArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFlowOperationsRequestPaginateTypeDef(TypedDict):
    FirewallArn: str
    AvailabilityZone: NotRequired[str]
    VpcEndpointAssociationArn: NotRequired[str]
    VpcEndpointId: NotRequired[str]
    FlowOperationType: NotRequired[FlowOperationTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProxiesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProxyConfigurationsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProxyRuleGroupsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListRuleGroupsRequestPaginateTypeDef = TypedDict(
    "ListRuleGroupsRequestPaginateTypeDef",
    {
        "Scope": NotRequired[ResourceManagedStatusType],
        "ManagedType": NotRequired[ResourceManagedTypeType],
        "SubscriptionStatus": NotRequired[SubscriptionStatusType],
        "Type": NotRequired[RuleGroupTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class ListTLSInspectionConfigurationsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTagsForResourceRequestPaginateTypeDef(TypedDict):
    ResourceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListVpcEndpointAssociationsRequestPaginateTypeDef(TypedDict):
    FirewallArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class PolicyVariablesOutputTypeDef(TypedDict):
    RuleVariables: NotRequired[dict[str, IPSetOutputTypeDef]]


class ReferenceSetsOutputTypeDef(TypedDict):
    IPSetReferences: NotRequired[dict[str, IPSetReferenceTypeDef]]


class ReferenceSetsTypeDef(TypedDict):
    IPSetReferences: NotRequired[Mapping[str, IPSetReferenceTypeDef]]


class PolicyVariablesTypeDef(TypedDict):
    RuleVariables: NotRequired[Mapping[str, IPSetTypeDef]]


class ListProxiesResponseTypeDef(TypedDict):
    Proxies: list[ProxyMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListProxyConfigurationsResponseTypeDef(TypedDict):
    ProxyConfigurations: list[ProxyConfigurationMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListProxyRuleGroupsResponseTypeDef(TypedDict):
    ProxyRuleGroups: list[ProxyRuleGroupMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListRuleGroupsResponseTypeDef(TypedDict):
    RuleGroups: list[RuleGroupMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTLSInspectionConfigurationsResponseTypeDef(TypedDict):
    TLSInspectionConfigurations: list[TLSInspectionConfigurationMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListVpcEndpointAssociationsResponseTypeDef(TypedDict):
    VpcEndpointAssociations: list[VpcEndpointAssociationMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class LoggingConfigurationOutputTypeDef(TypedDict):
    LogDestinationConfigs: list[LogDestinationConfigOutputTypeDef]


class LoggingConfigurationTypeDef(TypedDict):
    LogDestinationConfigs: Sequence[LogDestinationConfigTypeDef]


class ServerCertificateScopeOutputTypeDef(TypedDict):
    Sources: NotRequired[list[AddressTypeDef]]
    Destinations: NotRequired[list[AddressTypeDef]]
    SourcePorts: NotRequired[list[PortRangeTypeDef]]
    DestinationPorts: NotRequired[list[PortRangeTypeDef]]
    Protocols: NotRequired[list[int]]


class ServerCertificateScopeTypeDef(TypedDict):
    Sources: NotRequired[Sequence[AddressTypeDef]]
    Destinations: NotRequired[Sequence[AddressTypeDef]]
    SourcePorts: NotRequired[Sequence[PortRangeTypeDef]]
    DestinationPorts: NotRequired[Sequence[PortRangeTypeDef]]
    Protocols: NotRequired[Sequence[int]]


class MatchAttributesOutputTypeDef(TypedDict):
    Sources: NotRequired[list[AddressTypeDef]]
    Destinations: NotRequired[list[AddressTypeDef]]
    SourcePorts: NotRequired[list[PortRangeTypeDef]]
    DestinationPorts: NotRequired[list[PortRangeTypeDef]]
    Protocols: NotRequired[list[int]]
    TCPFlags: NotRequired[list[TCPFlagFieldOutputTypeDef]]


class MatchAttributesTypeDef(TypedDict):
    Sources: NotRequired[Sequence[AddressTypeDef]]
    Destinations: NotRequired[Sequence[AddressTypeDef]]
    SourcePorts: NotRequired[Sequence[PortRangeTypeDef]]
    DestinationPorts: NotRequired[Sequence[PortRangeTypeDef]]
    Protocols: NotRequired[Sequence[int]]
    TCPFlags: NotRequired[Sequence[TCPFlagFieldTypeDef]]


class SyncStateTypeDef(TypedDict):
    Attachment: NotRequired[AttachmentTypeDef]
    Config: NotRequired[dict[str, PerObjectStatusTypeDef]]


class RuleVariablesOutputTypeDef(TypedDict):
    IPSets: NotRequired[dict[str, IPSetOutputTypeDef]]
    PortSets: NotRequired[dict[str, PortSetOutputTypeDef]]


class RuleVariablesTypeDef(TypedDict):
    IPSets: NotRequired[Mapping[str, IPSetTypeDef]]
    PortSets: NotRequired[Mapping[str, PortSetTypeDef]]


class ProxyConfigurationTypeDef(TypedDict):
    ProxyConfigurationName: NotRequired[str]
    ProxyConfigurationArn: NotRequired[str]
    Description: NotRequired[str]
    CreateTime: NotRequired[datetime]
    DeleteTime: NotRequired[datetime]
    RuleGroups: NotRequired[list[ProxyConfigRuleGroupTypeDef]]
    DefaultRulePhaseActions: NotRequired[ProxyConfigDefaultRulePhaseActionsRequestTypeDef]
    Tags: NotRequired[list[TagTypeDef]]


class ProxyRuleOutputTypeDef(TypedDict):
    ProxyRuleName: NotRequired[str]
    Description: NotRequired[str]
    Action: NotRequired[ProxyRulePhaseActionType]
    Conditions: NotRequired[list[ProxyRuleConditionOutputTypeDef]]


ProxyRuleConditionUnionTypeDef = Union[ProxyRuleConditionTypeDef, ProxyRuleConditionOutputTypeDef]


class ProxyRuleTypeDef(TypedDict):
    ProxyRuleName: NotRequired[str]
    Description: NotRequired[str]
    Action: NotRequired[ProxyRulePhaseActionType]
    Conditions: NotRequired[Sequence[ProxyRuleConditionTypeDef]]


class UpdateProxyRuleGroupPrioritiesResponseTypeDef(TypedDict):
    ProxyRuleGroups: list[ProxyRuleGroupPriorityResultTypeDef]
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateProxyRuleGroupPrioritiesRequestTypeDef(TypedDict):
    RuleGroups: Sequence[ProxyRuleGroupPriorityTypeDef]
    UpdateToken: str
    ProxyConfigurationName: NotRequired[str]
    ProxyConfigurationArn: NotRequired[str]


class UpdateProxyRulePrioritiesRequestTypeDef(TypedDict):
    RuleGroupRequestPhase: RuleGroupRequestPhaseType
    Rules: Sequence[ProxyRulePriorityTypeDef]
    UpdateToken: str
    ProxyRuleGroupName: NotRequired[str]
    ProxyRuleGroupArn: NotRequired[str]


class UpdateProxyRulePrioritiesResponseTypeDef(TypedDict):
    ProxyRuleGroupName: str
    ProxyRuleGroupArn: str
    RuleGroupRequestPhase: RuleGroupRequestPhaseType
    Rules: list[ProxyRulePriorityTypeDef]
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef


RuleGroupResponseTypeDef = TypedDict(
    "RuleGroupResponseTypeDef",
    {
        "RuleGroupArn": str,
        "RuleGroupName": str,
        "RuleGroupId": str,
        "Description": NotRequired[str],
        "Type": NotRequired[RuleGroupTypeType],
        "Capacity": NotRequired[int],
        "RuleGroupStatus": NotRequired[ResourceStatusType],
        "Tags": NotRequired[list[TagTypeDef]],
        "ConsumedCapacity": NotRequired[int],
        "NumberOfAssociations": NotRequired[int],
        "EncryptionConfiguration": NotRequired[EncryptionConfigurationTypeDef],
        "SourceMetadata": NotRequired[SourceMetadataTypeDef],
        "SnsTopic": NotRequired[str],
        "LastModifiedTime": NotRequired[datetime],
        "AnalysisResults": NotRequired[list[AnalysisResultTypeDef]],
        "SummaryConfiguration": NotRequired[SummaryConfigurationOutputTypeDef],
    },
)


class StatefulRuleOutputTypeDef(TypedDict):
    Action: StatefulActionType
    Header: HeaderTypeDef
    RuleOptions: list[RuleOptionOutputTypeDef]


class StatefulRuleTypeDef(TypedDict):
    Action: StatefulActionType
    Header: HeaderTypeDef
    RuleOptions: Sequence[RuleOptionTypeDef]


class SummaryTypeDef(TypedDict):
    RuleSummaries: NotRequired[list[RuleSummaryTypeDef]]


class StatefulRuleGroupReferenceTypeDef(TypedDict):
    ResourceArn: str
    Priority: NotRequired[int]
    Override: NotRequired[StatefulRuleGroupOverrideTypeDef]
    DeepThreatInspection: NotRequired[bool]


SummaryConfigurationUnionTypeDef = Union[
    SummaryConfigurationTypeDef, SummaryConfigurationOutputTypeDef
]


class TLSInspectionConfigurationResponseTypeDef(TypedDict):
    TLSInspectionConfigurationArn: str
    TLSInspectionConfigurationName: str
    TLSInspectionConfigurationId: str
    TLSInspectionConfigurationStatus: NotRequired[ResourceStatusType]
    Description: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    LastModifiedTime: NotRequired[datetime]
    NumberOfAssociations: NotRequired[int]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]
    Certificates: NotRequired[list[TlsCertificateDataTypeDef]]
    CertificateAuthority: NotRequired[TlsCertificateDataTypeDef]


class VpcEndpointAssociationStatusTypeDef(TypedDict):
    Status: FirewallStatusValueType
    AssociationSyncState: NotRequired[dict[str, AZSyncStateTypeDef]]


class FlowOperationTypeDef(TypedDict):
    MinimumFlowAgeInSeconds: NotRequired[int]
    FlowFilters: NotRequired[list[FlowFilterOutputTypeDef]]


FlowFilterUnionTypeDef = Union[FlowFilterTypeDef, FlowFilterOutputTypeDef]


class ListFlowOperationResultsResponseTypeDef(TypedDict):
    FirewallArn: str
    AvailabilityZone: str
    VpcEndpointAssociationArn: str
    VpcEndpointId: str
    FlowOperationId: str
    FlowOperationStatus: FlowOperationStatusType
    StatusMessage: str
    FlowRequestTimestamp: datetime
    Flows: list[FlowTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetAnalysisReportResultsResponseTypeDef(TypedDict):
    Status: str
    StartTime: datetime
    EndTime: datetime
    ReportTime: datetime
    AnalysisType: EnabledAnalysisTypeType
    AnalysisReportResults: list[AnalysisTypeReportResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CapacityUsageSummaryTypeDef(TypedDict):
    CIDRs: NotRequired[CIDRSummaryTypeDef]


class CreateFirewallPolicyResponseTypeDef(TypedDict):
    UpdateToken: str
    FirewallPolicyResponse: FirewallPolicyResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteFirewallPolicyResponseTypeDef(TypedDict):
    FirewallPolicyResponse: FirewallPolicyResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateFirewallPolicyResponseTypeDef(TypedDict):
    UpdateToken: str
    FirewallPolicyResponse: FirewallPolicyResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeProxyResponseTypeDef(TypedDict):
    Proxy: DescribeProxyResourceTypeDef
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateProxyResponseTypeDef(TypedDict):
    Proxy: ProxyTypeDef
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateProxyResponseTypeDef(TypedDict):
    Proxy: ProxyTypeDef
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class ActionDefinitionOutputTypeDef(TypedDict):
    PublishMetricAction: NotRequired[PublishMetricActionOutputTypeDef]


class ActionDefinitionTypeDef(TypedDict):
    PublishMetricAction: NotRequired[PublishMetricActionTypeDef]


class DescribeLoggingConfigurationResponseTypeDef(TypedDict):
    FirewallArn: str
    LoggingConfiguration: LoggingConfigurationOutputTypeDef
    EnableMonitoringDashboard: bool
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateLoggingConfigurationResponseTypeDef(TypedDict):
    FirewallArn: str
    FirewallName: str
    LoggingConfiguration: LoggingConfigurationOutputTypeDef
    EnableMonitoringDashboard: bool
    ResponseMetadata: ResponseMetadataTypeDef


LoggingConfigurationUnionTypeDef = Union[
    LoggingConfigurationTypeDef, LoggingConfigurationOutputTypeDef
]


class ServerCertificateConfigurationOutputTypeDef(TypedDict):
    ServerCertificates: NotRequired[list[ServerCertificateTypeDef]]
    Scopes: NotRequired[list[ServerCertificateScopeOutputTypeDef]]
    CertificateAuthorityArn: NotRequired[str]
    CheckCertificateRevocationStatus: NotRequired[CheckCertificateRevocationStatusActionsTypeDef]


class ServerCertificateConfigurationTypeDef(TypedDict):
    ServerCertificates: NotRequired[Sequence[ServerCertificateTypeDef]]
    Scopes: NotRequired[Sequence[ServerCertificateScopeTypeDef]]
    CertificateAuthorityArn: NotRequired[str]
    CheckCertificateRevocationStatus: NotRequired[CheckCertificateRevocationStatusActionsTypeDef]


class RuleDefinitionOutputTypeDef(TypedDict):
    MatchAttributes: MatchAttributesOutputTypeDef
    Actions: list[str]


class RuleDefinitionTypeDef(TypedDict):
    MatchAttributes: MatchAttributesTypeDef
    Actions: Sequence[str]


class AttachRuleGroupsToProxyConfigurationResponseTypeDef(TypedDict):
    ProxyConfiguration: ProxyConfigurationTypeDef
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateProxyConfigurationResponseTypeDef(TypedDict):
    ProxyConfiguration: ProxyConfigurationTypeDef
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeProxyConfigurationResponseTypeDef(TypedDict):
    ProxyConfiguration: ProxyConfigurationTypeDef
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DetachRuleGroupsFromProxyConfigurationResponseTypeDef(TypedDict):
    ProxyConfiguration: ProxyConfigurationTypeDef
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateProxyConfigurationResponseTypeDef(TypedDict):
    ProxyConfiguration: ProxyConfigurationTypeDef
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeProxyRuleResponseTypeDef(TypedDict):
    ProxyRule: ProxyRuleOutputTypeDef
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class ProxyRulesByRequestPhaseOutputTypeDef(TypedDict):
    PreDNS: NotRequired[list[ProxyRuleOutputTypeDef]]
    PreREQUEST: NotRequired[list[ProxyRuleOutputTypeDef]]
    PostRESPONSE: NotRequired[list[ProxyRuleOutputTypeDef]]


class UpdateProxyRuleResponseTypeDef(TypedDict):
    ProxyRule: ProxyRuleOutputTypeDef
    RemovedConditions: list[ProxyRuleConditionOutputTypeDef]
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateProxyRuleTypeDef(TypedDict):
    ProxyRuleName: NotRequired[str]
    Description: NotRequired[str]
    Action: NotRequired[ProxyRulePhaseActionType]
    Conditions: NotRequired[Sequence[ProxyRuleConditionUnionTypeDef]]
    InsertPosition: NotRequired[int]


class UpdateProxyRuleRequestTypeDef(TypedDict):
    ProxyRuleName: str
    UpdateToken: str
    ProxyRuleGroupName: NotRequired[str]
    ProxyRuleGroupArn: NotRequired[str]
    Description: NotRequired[str]
    Action: NotRequired[ProxyRulePhaseActionType]
    AddConditions: NotRequired[Sequence[ProxyRuleConditionUnionTypeDef]]
    RemoveConditions: NotRequired[Sequence[ProxyRuleConditionUnionTypeDef]]


class ProxyRulesByRequestPhaseTypeDef(TypedDict):
    PreDNS: NotRequired[Sequence[ProxyRuleTypeDef]]
    PreREQUEST: NotRequired[Sequence[ProxyRuleTypeDef]]
    PostRESPONSE: NotRequired[Sequence[ProxyRuleTypeDef]]


class CreateRuleGroupResponseTypeDef(TypedDict):
    UpdateToken: str
    RuleGroupResponse: RuleGroupResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteRuleGroupResponseTypeDef(TypedDict):
    RuleGroupResponse: RuleGroupResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRuleGroupResponseTypeDef(TypedDict):
    UpdateToken: str
    RuleGroupResponse: RuleGroupResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeRuleGroupSummaryResponseTypeDef(TypedDict):
    RuleGroupName: str
    Description: str
    Summary: SummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTLSInspectionConfigurationResponseTypeDef(TypedDict):
    UpdateToken: str
    TLSInspectionConfigurationResponse: TLSInspectionConfigurationResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTLSInspectionConfigurationResponseTypeDef(TypedDict):
    TLSInspectionConfigurationResponse: TLSInspectionConfigurationResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTLSInspectionConfigurationResponseTypeDef(TypedDict):
    UpdateToken: str
    TLSInspectionConfigurationResponse: TLSInspectionConfigurationResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateVpcEndpointAssociationResponseTypeDef(TypedDict):
    VpcEndpointAssociation: VpcEndpointAssociationTypeDef
    VpcEndpointAssociationStatus: VpcEndpointAssociationStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteVpcEndpointAssociationResponseTypeDef(TypedDict):
    VpcEndpointAssociation: VpcEndpointAssociationTypeDef
    VpcEndpointAssociationStatus: VpcEndpointAssociationStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVpcEndpointAssociationResponseTypeDef(TypedDict):
    VpcEndpointAssociation: VpcEndpointAssociationTypeDef
    VpcEndpointAssociationStatus: VpcEndpointAssociationStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeFlowOperationResponseTypeDef(TypedDict):
    FirewallArn: str
    AvailabilityZone: str
    VpcEndpointAssociationArn: str
    VpcEndpointId: str
    FlowOperationId: str
    FlowOperationType: FlowOperationTypeType
    FlowOperationStatus: FlowOperationStatusType
    StatusMessage: str
    FlowRequestTimestamp: datetime
    FlowOperation: FlowOperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StartFlowCaptureRequestTypeDef(TypedDict):
    FirewallArn: str
    FlowFilters: Sequence[FlowFilterUnionTypeDef]
    AvailabilityZone: NotRequired[str]
    VpcEndpointAssociationArn: NotRequired[str]
    VpcEndpointId: NotRequired[str]
    MinimumFlowAgeInSeconds: NotRequired[int]


class StartFlowFlushRequestTypeDef(TypedDict):
    FirewallArn: str
    FlowFilters: Sequence[FlowFilterUnionTypeDef]
    AvailabilityZone: NotRequired[str]
    VpcEndpointAssociationArn: NotRequired[str]
    VpcEndpointId: NotRequired[str]
    MinimumFlowAgeInSeconds: NotRequired[int]


class FirewallStatusTypeDef(TypedDict):
    Status: FirewallStatusValueType
    ConfigurationSyncStateSummary: ConfigurationSyncStateType
    SyncStates: NotRequired[dict[str, SyncStateTypeDef]]
    CapacityUsageSummary: NotRequired[CapacityUsageSummaryTypeDef]
    TransitGatewayAttachmentSyncState: NotRequired[TransitGatewayAttachmentSyncStateTypeDef]


class CustomActionOutputTypeDef(TypedDict):
    ActionName: str
    ActionDefinition: ActionDefinitionOutputTypeDef


class CustomActionTypeDef(TypedDict):
    ActionName: str
    ActionDefinition: ActionDefinitionTypeDef


class UpdateLoggingConfigurationRequestTypeDef(TypedDict):
    FirewallArn: NotRequired[str]
    FirewallName: NotRequired[str]
    LoggingConfiguration: NotRequired[LoggingConfigurationUnionTypeDef]
    EnableMonitoringDashboard: NotRequired[bool]


class TLSInspectionConfigurationOutputTypeDef(TypedDict):
    ServerCertificateConfigurations: NotRequired[list[ServerCertificateConfigurationOutputTypeDef]]


class TLSInspectionConfigurationTypeDef(TypedDict):
    ServerCertificateConfigurations: NotRequired[Sequence[ServerCertificateConfigurationTypeDef]]


class StatelessRuleOutputTypeDef(TypedDict):
    RuleDefinition: RuleDefinitionOutputTypeDef
    Priority: int


class StatelessRuleTypeDef(TypedDict):
    RuleDefinition: RuleDefinitionTypeDef
    Priority: int


class ProxyRuleGroupTypeDef(TypedDict):
    ProxyRuleGroupName: NotRequired[str]
    ProxyRuleGroupArn: NotRequired[str]
    CreateTime: NotRequired[datetime]
    DeleteTime: NotRequired[datetime]
    Rules: NotRequired[ProxyRulesByRequestPhaseOutputTypeDef]
    Description: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


class CreateProxyRulesByRequestPhaseTypeDef(TypedDict):
    PreDNS: NotRequired[Sequence[CreateProxyRuleTypeDef]]
    PreREQUEST: NotRequired[Sequence[CreateProxyRuleTypeDef]]
    PostRESPONSE: NotRequired[Sequence[CreateProxyRuleTypeDef]]


ProxyRulesByRequestPhaseUnionTypeDef = Union[
    ProxyRulesByRequestPhaseTypeDef, ProxyRulesByRequestPhaseOutputTypeDef
]


class CreateFirewallResponseTypeDef(TypedDict):
    Firewall: FirewallTypeDef
    FirewallStatus: FirewallStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteFirewallResponseTypeDef(TypedDict):
    Firewall: FirewallTypeDef
    FirewallStatus: FirewallStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeFirewallResponseTypeDef(TypedDict):
    UpdateToken: str
    Firewall: FirewallTypeDef
    FirewallStatus: FirewallStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class FirewallPolicyOutputTypeDef(TypedDict):
    StatelessDefaultActions: list[str]
    StatelessFragmentDefaultActions: list[str]
    StatelessRuleGroupReferences: NotRequired[list[StatelessRuleGroupReferenceTypeDef]]
    StatelessCustomActions: NotRequired[list[CustomActionOutputTypeDef]]
    StatefulRuleGroupReferences: NotRequired[list[StatefulRuleGroupReferenceTypeDef]]
    StatefulDefaultActions: NotRequired[list[str]]
    StatefulEngineOptions: NotRequired[StatefulEngineOptionsTypeDef]
    TLSInspectionConfigurationArn: NotRequired[str]
    PolicyVariables: NotRequired[PolicyVariablesOutputTypeDef]
    EnableTLSSessionHolding: NotRequired[bool]


class FirewallPolicyTypeDef(TypedDict):
    StatelessDefaultActions: Sequence[str]
    StatelessFragmentDefaultActions: Sequence[str]
    StatelessRuleGroupReferences: NotRequired[Sequence[StatelessRuleGroupReferenceTypeDef]]
    StatelessCustomActions: NotRequired[Sequence[CustomActionTypeDef]]
    StatefulRuleGroupReferences: NotRequired[Sequence[StatefulRuleGroupReferenceTypeDef]]
    StatefulDefaultActions: NotRequired[Sequence[str]]
    StatefulEngineOptions: NotRequired[StatefulEngineOptionsTypeDef]
    TLSInspectionConfigurationArn: NotRequired[str]
    PolicyVariables: NotRequired[PolicyVariablesTypeDef]
    EnableTLSSessionHolding: NotRequired[bool]


class DescribeTLSInspectionConfigurationResponseTypeDef(TypedDict):
    UpdateToken: str
    TLSInspectionConfiguration: TLSInspectionConfigurationOutputTypeDef
    TLSInspectionConfigurationResponse: TLSInspectionConfigurationResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


TLSInspectionConfigurationUnionTypeDef = Union[
    TLSInspectionConfigurationTypeDef, TLSInspectionConfigurationOutputTypeDef
]


class StatelessRulesAndCustomActionsOutputTypeDef(TypedDict):
    StatelessRules: list[StatelessRuleOutputTypeDef]
    CustomActions: NotRequired[list[CustomActionOutputTypeDef]]


class StatelessRulesAndCustomActionsTypeDef(TypedDict):
    StatelessRules: Sequence[StatelessRuleTypeDef]
    CustomActions: NotRequired[Sequence[CustomActionTypeDef]]


class CreateProxyRuleGroupResponseTypeDef(TypedDict):
    ProxyRuleGroup: ProxyRuleGroupTypeDef
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateProxyRulesResponseTypeDef(TypedDict):
    ProxyRuleGroup: ProxyRuleGroupTypeDef
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteProxyRulesResponseTypeDef(TypedDict):
    ProxyRuleGroup: ProxyRuleGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeProxyRuleGroupResponseTypeDef(TypedDict):
    ProxyRuleGroup: ProxyRuleGroupTypeDef
    UpdateToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateProxyRulesRequestTypeDef(TypedDict):
    Rules: CreateProxyRulesByRequestPhaseTypeDef
    ProxyRuleGroupArn: NotRequired[str]
    ProxyRuleGroupName: NotRequired[str]


class CreateProxyRuleGroupRequestTypeDef(TypedDict):
    ProxyRuleGroupName: str
    Description: NotRequired[str]
    Rules: NotRequired[ProxyRulesByRequestPhaseUnionTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class DescribeFirewallPolicyResponseTypeDef(TypedDict):
    UpdateToken: str
    FirewallPolicyResponse: FirewallPolicyResponseTypeDef
    FirewallPolicy: FirewallPolicyOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


FirewallPolicyUnionTypeDef = Union[FirewallPolicyTypeDef, FirewallPolicyOutputTypeDef]


class CreateTLSInspectionConfigurationRequestTypeDef(TypedDict):
    TLSInspectionConfigurationName: str
    TLSInspectionConfiguration: TLSInspectionConfigurationUnionTypeDef
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]


class UpdateTLSInspectionConfigurationRequestTypeDef(TypedDict):
    TLSInspectionConfiguration: TLSInspectionConfigurationUnionTypeDef
    UpdateToken: str
    TLSInspectionConfigurationArn: NotRequired[str]
    TLSInspectionConfigurationName: NotRequired[str]
    Description: NotRequired[str]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]


class RulesSourceOutputTypeDef(TypedDict):
    RulesString: NotRequired[str]
    RulesSourceList: NotRequired[RulesSourceListOutputTypeDef]
    StatefulRules: NotRequired[list[StatefulRuleOutputTypeDef]]
    StatelessRulesAndCustomActions: NotRequired[StatelessRulesAndCustomActionsOutputTypeDef]


class RulesSourceTypeDef(TypedDict):
    RulesString: NotRequired[str]
    RulesSourceList: NotRequired[RulesSourceListTypeDef]
    StatefulRules: NotRequired[Sequence[StatefulRuleTypeDef]]
    StatelessRulesAndCustomActions: NotRequired[StatelessRulesAndCustomActionsTypeDef]


class CreateFirewallPolicyRequestTypeDef(TypedDict):
    FirewallPolicyName: str
    FirewallPolicy: FirewallPolicyUnionTypeDef
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    DryRun: NotRequired[bool]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]


class UpdateFirewallPolicyRequestTypeDef(TypedDict):
    UpdateToken: str
    FirewallPolicy: FirewallPolicyUnionTypeDef
    FirewallPolicyArn: NotRequired[str]
    FirewallPolicyName: NotRequired[str]
    Description: NotRequired[str]
    DryRun: NotRequired[bool]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]


class RuleGroupOutputTypeDef(TypedDict):
    RulesSource: RulesSourceOutputTypeDef
    RuleVariables: NotRequired[RuleVariablesOutputTypeDef]
    ReferenceSets: NotRequired[ReferenceSetsOutputTypeDef]
    StatefulRuleOptions: NotRequired[StatefulRuleOptionsTypeDef]


class RuleGroupTypeDef(TypedDict):
    RulesSource: RulesSourceTypeDef
    RuleVariables: NotRequired[RuleVariablesTypeDef]
    ReferenceSets: NotRequired[ReferenceSetsTypeDef]
    StatefulRuleOptions: NotRequired[StatefulRuleOptionsTypeDef]


class DescribeRuleGroupResponseTypeDef(TypedDict):
    UpdateToken: str
    RuleGroup: RuleGroupOutputTypeDef
    RuleGroupResponse: RuleGroupResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


RuleGroupUnionTypeDef = Union[RuleGroupTypeDef, RuleGroupOutputTypeDef]
CreateRuleGroupRequestTypeDef = TypedDict(
    "CreateRuleGroupRequestTypeDef",
    {
        "RuleGroupName": str,
        "Type": RuleGroupTypeType,
        "Capacity": int,
        "RuleGroup": NotRequired[RuleGroupUnionTypeDef],
        "Rules": NotRequired[str],
        "Description": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "DryRun": NotRequired[bool],
        "EncryptionConfiguration": NotRequired[EncryptionConfigurationTypeDef],
        "SourceMetadata": NotRequired[SourceMetadataTypeDef],
        "AnalyzeRuleGroup": NotRequired[bool],
        "SummaryConfiguration": NotRequired[SummaryConfigurationUnionTypeDef],
    },
)
UpdateRuleGroupRequestTypeDef = TypedDict(
    "UpdateRuleGroupRequestTypeDef",
    {
        "UpdateToken": str,
        "RuleGroupArn": NotRequired[str],
        "RuleGroupName": NotRequired[str],
        "RuleGroup": NotRequired[RuleGroupUnionTypeDef],
        "Rules": NotRequired[str],
        "Type": NotRequired[RuleGroupTypeType],
        "Description": NotRequired[str],
        "DryRun": NotRequired[bool],
        "EncryptionConfiguration": NotRequired[EncryptionConfigurationTypeDef],
        "SourceMetadata": NotRequired[SourceMetadataTypeDef],
        "AnalyzeRuleGroup": NotRequired[bool],
        "SummaryConfiguration": NotRequired[SummaryConfigurationUnionTypeDef],
    },
)
