"""
Type annotations for rtbfabric service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_rtbfabric.type_defs import ErrorDetailTypeDef

    data: ErrorDetailTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Union

from .literals import (
    CertificateAssociationStatusType,
    ClientRoutingPolicyType,
    ConfigurableActionType,
    ConnectivityTypeType,
    ErrorCodeType,
    FailureModeType,
    FilterTypeType,
    GatewayTypeType,
    LinkDirectionType,
    LinkStatusType,
    ModulePermissionType,
    ModuleVersionStatusType,
    ProtocolType,
    RequesterGatewayStatusType,
    ResponderErrorMaskingActionType,
    ResponderErrorMaskingLoggingTypeType,
    ResponderGatewayStatusType,
    RuleStatusType,
    SubscriptionStatusType,
    SubscriptionTypeType,
    UpdateStatusType,
    UpdateTypeType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AcceptLinkRequestTypeDef",
    "AcceptLinkResponseTypeDef",
    "ActionTypeDef",
    "AssociateCertificateRequestTypeDef",
    "AssociateCertificateResponseTypeDef",
    "AutoScalingGroupsConfigurationOutputTypeDef",
    "AutoScalingGroupsConfigurationTypeDef",
    "AvailableModuleSummaryTypeDef",
    "AvailableModuleVersionSummaryTypeDef",
    "CertificateAssociationSummaryTypeDef",
    "CreateInboundExternalLinkRequestTypeDef",
    "CreateInboundExternalLinkResponseTypeDef",
    "CreateLinkRequestTypeDef",
    "CreateLinkResponseTypeDef",
    "CreateLinkRoutingRuleRequestTypeDef",
    "CreateLinkRoutingRuleResponseTypeDef",
    "CreateOutboundExternalLinkRequestTypeDef",
    "CreateOutboundExternalLinkResponseTypeDef",
    "CreateRequesterGatewayRequestTypeDef",
    "CreateRequesterGatewayResponseTypeDef",
    "CreateResponderGatewayRequestTypeDef",
    "CreateResponderGatewayResponseTypeDef",
    "DeleteInboundExternalLinkRequestTypeDef",
    "DeleteInboundExternalLinkResponseTypeDef",
    "DeleteLinkRequestTypeDef",
    "DeleteLinkResponseTypeDef",
    "DeleteLinkRoutingRuleRequestTypeDef",
    "DeleteLinkRoutingRuleResponseTypeDef",
    "DeleteOutboundExternalLinkRequestTypeDef",
    "DeleteOutboundExternalLinkResponseTypeDef",
    "DeleteRequesterGatewayRequestTypeDef",
    "DeleteRequesterGatewayResponseTypeDef",
    "DeleteResponderGatewayRequestTypeDef",
    "DeleteResponderGatewayResponseTypeDef",
    "DisassociateCertificateRequestTypeDef",
    "DisassociateCertificateResponseTypeDef",
    "EksEndpointsConfigurationTypeDef",
    "ErrorDetailTypeDef",
    "FilterCriterionOutputTypeDef",
    "FilterCriterionTypeDef",
    "FilterCriterionUnionTypeDef",
    "FilterOutputTypeDef",
    "FilterTypeDef",
    "FilterUnionTypeDef",
    "FlowModuleOutputTypeDef",
    "FlowModuleTypeDef",
    "FlowModuleUnionTypeDef",
    "FlowOutputTypeDef",
    "FlowPhaseOutputTypeDef",
    "FlowPhaseTypeDef",
    "FlowPhaseUnionTypeDef",
    "FlowPipelineOutputTypeDef",
    "FlowPipelineTypeDef",
    "FlowPipelineUnionTypeDef",
    "FlowTypeDef",
    "FlowUnionTypeDef",
    "GetAvailableModuleRequestTypeDef",
    "GetAvailableModuleResponseTypeDef",
    "GetAvailableModuleVersionRequestTypeDef",
    "GetAvailableModuleVersionResponseTypeDef",
    "GetCertificateAssociationRequestTypeDef",
    "GetCertificateAssociationRequestWaitExtraTypeDef",
    "GetCertificateAssociationRequestWaitTypeDef",
    "GetCertificateAssociationResponseTypeDef",
    "GetInboundExternalLinkRequestTypeDef",
    "GetInboundExternalLinkRequestWaitExtraTypeDef",
    "GetInboundExternalLinkRequestWaitTypeDef",
    "GetInboundExternalLinkResponseTypeDef",
    "GetLinkRequestTypeDef",
    "GetLinkRequestWaitExtraExtraTypeDef",
    "GetLinkRequestWaitExtraTypeDef",
    "GetLinkRequestWaitTypeDef",
    "GetLinkResponseTypeDef",
    "GetLinkRoutingRuleRequestTypeDef",
    "GetLinkRoutingRuleRequestWaitExtraTypeDef",
    "GetLinkRoutingRuleRequestWaitTypeDef",
    "GetLinkRoutingRuleResponseTypeDef",
    "GetOutboundExternalLinkRequestTypeDef",
    "GetOutboundExternalLinkRequestWaitExtraTypeDef",
    "GetOutboundExternalLinkRequestWaitTypeDef",
    "GetOutboundExternalLinkResponseTypeDef",
    "GetRequesterGatewayRequestTypeDef",
    "GetRequesterGatewayRequestWaitExtraTypeDef",
    "GetRequesterGatewayRequestWaitTypeDef",
    "GetRequesterGatewayResponseTypeDef",
    "GetResponderGatewayRequestTypeDef",
    "GetResponderGatewayRequestWaitExtraTypeDef",
    "GetResponderGatewayRequestWaitTypeDef",
    "GetResponderGatewayResponseTypeDef",
    "GetUpdateRequestTypeDef",
    "GetUpdateResponseTypeDef",
    "HeaderTagActionTypeDef",
    "HealthCheckConfigTypeDef",
    "LinkApplicationLogConfigurationTypeDef",
    "LinkApplicationLogSamplingTypeDef",
    "LinkAttributesOutputTypeDef",
    "LinkAttributesTypeDef",
    "LinkAttributesUnionTypeDef",
    "LinkConfigParametersTypeDef",
    "LinkFlowParametersTypeDef",
    "LinkLogSettingsTypeDef",
    "LinkRoutingRuleSummaryTypeDef",
    "LinkTargetTypeDef",
    "ListAvailableModuleVersionsRequestPaginateTypeDef",
    "ListAvailableModuleVersionsRequestTypeDef",
    "ListAvailableModuleVersionsResponseTypeDef",
    "ListAvailableModulesRequestPaginateTypeDef",
    "ListAvailableModulesRequestTypeDef",
    "ListAvailableModulesResponseTypeDef",
    "ListCertificateAssociationsRequestPaginateTypeDef",
    "ListCertificateAssociationsRequestTypeDef",
    "ListCertificateAssociationsResponseTypeDef",
    "ListLinkRoutingRulesRequestPaginateTypeDef",
    "ListLinkRoutingRulesRequestTypeDef",
    "ListLinkRoutingRulesResponseTypeDef",
    "ListLinksRequestPaginateTypeDef",
    "ListLinksRequestTypeDef",
    "ListLinksResponseStructureTypeDef",
    "ListLinksResponseTypeDef",
    "ListRequesterGatewaysRequestPaginateTypeDef",
    "ListRequesterGatewaysRequestTypeDef",
    "ListRequesterGatewaysResponseTypeDef",
    "ListResponderGatewaysRequestPaginateTypeDef",
    "ListResponderGatewaysRequestTypeDef",
    "ListResponderGatewaysResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListUpdatesRequestPaginateTypeDef",
    "ListUpdatesRequestTypeDef",
    "ListUpdatesResponseTypeDef",
    "ListenerConfigOutputTypeDef",
    "ListenerConfigTypeDef",
    "ListenerConfigUnionTypeDef",
    "ManagedEndpointConfigurationOutputTypeDef",
    "ManagedEndpointConfigurationTypeDef",
    "ManagedEndpointConfigurationUnionTypeDef",
    "ModuleConfigurationOutputTypeDef",
    "ModuleConfigurationTypeDef",
    "ModuleConfigurationUnionTypeDef",
    "ModuleParametersOutputTypeDef",
    "ModuleParametersTypeDef",
    "ModuleParametersUnionTypeDef",
    "NoBidActionTypeDef",
    "NoBidModuleParametersTypeDef",
    "OpenRtbAttributeModuleParametersOutputTypeDef",
    "OpenRtbAttributeModuleParametersTypeDef",
    "OpenRtbAttributeModuleParametersUnionTypeDef",
    "PaginatorConfigTypeDef",
    "PhasedPipelineOutputTypeDef",
    "PhasedPipelineTypeDef",
    "PhasedPipelineUnionTypeDef",
    "PutLinkFlowsRequestTypeDef",
    "PutLinkFlowsResponseTypeDef",
    "QueryStringKeyValuePairTypeDef",
    "RateLimiterModuleParametersTypeDef",
    "RejectLinkRequestTypeDef",
    "RejectLinkResponseTypeDef",
    "ResponderErrorMaskingForHttpCodeOutputTypeDef",
    "ResponderErrorMaskingForHttpCodeTypeDef",
    "ResponderGatewayConfigParametersTypeDef",
    "ResponseMetadataTypeDef",
    "RoutingRuleParametersTypeDef",
    "RoutingRuleTargetTypeDef",
    "RuleConditionTypeDef",
    "SequentialPipelineOutputTypeDef",
    "SequentialPipelineTypeDef",
    "SequentialPipelineUnionTypeDef",
    "TagResourceRequestTypeDef",
    "TrustStoreConfigurationOutputTypeDef",
    "TrustStoreConfigurationTypeDef",
    "TrustStoreConfigurationUnionTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateLinkModuleFlowRequestTypeDef",
    "UpdateLinkModuleFlowResponseTypeDef",
    "UpdateLinkRequestTypeDef",
    "UpdateLinkResponseTypeDef",
    "UpdateLinkRoutingRuleRequestTypeDef",
    "UpdateLinkRoutingRuleResponseTypeDef",
    "UpdateParametersTypeDef",
    "UpdateRequesterGatewayRequestTypeDef",
    "UpdateRequesterGatewayResponseTypeDef",
    "UpdateResponderGatewayRequestTypeDef",
    "UpdateResponderGatewayResponseTypeDef",
    "UpdateSummaryTypeDef",
    "UpdateTargetTypeDef",
    "UpdateTypeDef",
    "WaiterConfigTypeDef",
)

class ErrorDetailTypeDef(TypedDict):
    code: ErrorCodeType
    message: str
    resourceIds: NotRequired[list[str]]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class HeaderTagActionTypeDef(TypedDict):
    name: str
    value: str

class NoBidActionTypeDef(TypedDict):
    noBidReasonCode: NotRequired[int]

class AssociateCertificateRequestTypeDef(TypedDict):
    gatewayId: str
    acmCertificateArn: str
    clientToken: str

class HealthCheckConfigTypeDef(TypedDict):
    port: int
    path: str
    protocol: NotRequired[ProtocolType]
    timeoutMs: NotRequired[int]
    intervalSeconds: NotRequired[int]
    statusCodeMatcher: NotRequired[str]
    healthyThresholdCount: NotRequired[int]
    unhealthyThresholdCount: NotRequired[int]

class AvailableModuleSummaryTypeDef(TypedDict):
    moduleId: str
    moduleArn: str
    moduleName: str
    subscriptionType: SubscriptionTypeType
    subscriptionStatus: SubscriptionStatusType
    marketplaceProductId: NotRequired[str]

class AvailableModuleVersionSummaryTypeDef(TypedDict):
    version: str
    moduleVersionArn: str
    status: ModuleVersionStatusType
    createdAt: datetime

class CertificateAssociationSummaryTypeDef(TypedDict):
    acmCertificateArn: str
    status: CertificateAssociationStatusType
    associatedAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class CreateRequesterGatewayRequestTypeDef(TypedDict):
    vpcId: str
    subnetIds: Sequence[str]
    securityGroupIds: Sequence[str]
    clientToken: str
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class ListenerConfigOutputTypeDef(TypedDict):
    protocols: list[ProtocolType]

class DeleteInboundExternalLinkRequestTypeDef(TypedDict):
    gatewayId: str
    linkId: str

class DeleteLinkRequestTypeDef(TypedDict):
    gatewayId: str
    linkId: str

class DeleteLinkRoutingRuleRequestTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    ruleId: str

class DeleteOutboundExternalLinkRequestTypeDef(TypedDict):
    gatewayId: str
    linkId: str

class DeleteRequesterGatewayRequestTypeDef(TypedDict):
    gatewayId: str

class DeleteResponderGatewayRequestTypeDef(TypedDict):
    gatewayId: str

class DisassociateCertificateRequestTypeDef(TypedDict):
    gatewayId: str
    acmCertificateArn: str

class EksEndpointsConfigurationTypeDef(TypedDict):
    endpointsResourceName: str
    endpointsResourceNamespace: str
    clusterApiServerEndpointUri: str
    clusterApiServerCaCertificateChain: str
    clusterName: str
    roleArn: str

class FilterCriterionOutputTypeDef(TypedDict):
    path: str
    values: list[str]

class FilterCriterionTypeDef(TypedDict):
    path: str
    values: Sequence[str]

class FlowModuleOutputTypeDef(TypedDict):
    name: str
    moduleVersionArn: str
    selectedActions: NotRequired[list[ConfigurableActionType]]
    failureMode: NotRequired[FailureModeType]
    activationPercentage: NotRequired[float]
    configurationValues: NotRequired[str]

class FlowModuleTypeDef(TypedDict):
    name: str
    moduleVersionArn: str
    selectedActions: NotRequired[Sequence[ConfigurableActionType]]
    failureMode: NotRequired[FailureModeType]
    activationPercentage: NotRequired[float]
    configurationValues: NotRequired[str]

class GetAvailableModuleRequestTypeDef(TypedDict):
    moduleId: str

class GetAvailableModuleVersionRequestTypeDef(TypedDict):
    moduleId: str
    version: str

class GetCertificateAssociationRequestTypeDef(TypedDict):
    gatewayId: str
    acmCertificateArn: str

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class GetInboundExternalLinkRequestTypeDef(TypedDict):
    gatewayId: str
    linkId: str

class GetLinkRequestTypeDef(TypedDict):
    gatewayId: str
    linkId: str

class GetLinkRoutingRuleRequestTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    ruleId: str

class GetOutboundExternalLinkRequestTypeDef(TypedDict):
    gatewayId: str
    linkId: str

class GetRequesterGatewayRequestTypeDef(TypedDict):
    gatewayId: str

class GetResponderGatewayRequestTypeDef(TypedDict):
    gatewayId: str

class TrustStoreConfigurationOutputTypeDef(TypedDict):
    certificateAuthorityCertificates: list[str]

class GetUpdateRequestTypeDef(TypedDict):
    gatewayId: str
    updateId: str

class LinkApplicationLogSamplingTypeDef(TypedDict):
    errorLog: float
    filterLog: float

class ResponderErrorMaskingForHttpCodeOutputTypeDef(TypedDict):
    httpCode: str
    action: ResponderErrorMaskingActionType
    loggingTypes: list[ResponderErrorMaskingLoggingTypeType]
    responseLoggingPercentage: NotRequired[float]

class ResponderErrorMaskingForHttpCodeTypeDef(TypedDict):
    httpCode: str
    action: ResponderErrorMaskingActionType
    loggingTypes: Sequence[ResponderErrorMaskingLoggingTypeType]
    responseLoggingPercentage: NotRequired[float]

class LinkTargetTypeDef(TypedDict):
    linkId: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAvailableModuleVersionsRequestTypeDef(TypedDict):
    moduleId: str
    status: NotRequired[ModuleVersionStatusType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListAvailableModulesRequestTypeDef(TypedDict):
    subscriptionType: NotRequired[SubscriptionTypeType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListCertificateAssociationsRequestTypeDef(TypedDict):
    gatewayId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListLinkRoutingRulesRequestTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListLinksRequestTypeDef(TypedDict):
    gatewayId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListRequesterGatewaysRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListResponderGatewaysRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str

ListUpdatesRequestTypeDef = TypedDict(
    "ListUpdatesRequestTypeDef",
    {
        "gatewayId": str,
        "linkId": NotRequired[str],
        "ruleId": NotRequired[str],
        "type": NotRequired[UpdateTypeType],
        "status": NotRequired[UpdateStatusType],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
UpdateSummaryTypeDef = TypedDict(
    "UpdateSummaryTypeDef",
    {
        "updateId": str,
        "type": UpdateTypeType,
        "status": UpdateStatusType,
        "createdAt": datetime,
    },
)

class ListenerConfigTypeDef(TypedDict):
    protocols: Sequence[ProtocolType]

class NoBidModuleParametersTypeDef(TypedDict):
    reason: NotRequired[str]
    reasonCode: NotRequired[int]
    passThroughPercentage: NotRequired[float]

class RateLimiterModuleParametersTypeDef(TypedDict):
    tps: NotRequired[float]

class QueryStringKeyValuePairTypeDef(TypedDict):
    key: str
    value: str

class RejectLinkRequestTypeDef(TypedDict):
    gatewayId: str
    linkId: str

class RoutingRuleTargetTypeDef(TypedDict):
    linkId: str
    ruleId: str

class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class TrustStoreConfigurationTypeDef(TypedDict):
    certificateAuthorityCertificates: Sequence[str]

class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateRequesterGatewayRequestTypeDef(TypedDict):
    clientToken: str
    gatewayId: str
    description: NotRequired[str]

class AssociateCertificateResponseTypeDef(TypedDict):
    gatewayId: str
    acmCertificateArn: str
    status: CertificateAssociationStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateInboundExternalLinkResponseTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    status: LinkStatusType
    domainName: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateLinkRoutingRuleResponseTypeDef(TypedDict):
    ruleId: str
    status: RuleStatusType
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateOutboundExternalLinkResponseTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    status: LinkStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRequesterGatewayResponseTypeDef(TypedDict):
    gatewayId: str
    domainName: str
    status: RequesterGatewayStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteInboundExternalLinkResponseTypeDef(TypedDict):
    linkId: str
    status: LinkStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteLinkResponseTypeDef(TypedDict):
    linkId: str
    status: LinkStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteLinkRoutingRuleResponseTypeDef(TypedDict):
    ruleId: str
    status: RuleStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteOutboundExternalLinkResponseTypeDef(TypedDict):
    linkId: str
    status: LinkStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteRequesterGatewayResponseTypeDef(TypedDict):
    gatewayId: str
    status: RequesterGatewayStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteResponderGatewayResponseTypeDef(TypedDict):
    gatewayId: str
    status: ResponderGatewayStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DisassociateCertificateResponseTypeDef(TypedDict):
    gatewayId: str
    acmCertificateArn: str
    status: CertificateAssociationStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class GetAvailableModuleResponseTypeDef(TypedDict):
    moduleId: str
    moduleArn: str
    moduleName: str
    description: str
    subscriptionType: SubscriptionTypeType
    subscriptionStatus: SubscriptionStatusType
    marketplaceProductId: str
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetAvailableModuleVersionResponseTypeDef(TypedDict):
    moduleId: str
    version: str
    moduleVersionArn: str
    status: ModuleVersionStatusType
    permissions: list[ModulePermissionType]
    configurableActions: list[ConfigurableActionType]
    configurationSchema: str
    releaseNotes: str
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetCertificateAssociationResponseTypeDef(TypedDict):
    gatewayId: str
    acmCertificateArn: str
    status: CertificateAssociationStatusType
    associatedAt: datetime
    updatedAt: datetime
    errorDetails: list[ErrorDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetRequesterGatewayResponseTypeDef(TypedDict):
    status: RequesterGatewayStatusType
    domainName: str
    description: str
    createdAt: datetime
    updatedAt: datetime
    errorDetails: list[ErrorDetailTypeDef]
    vpcId: str
    subnetIds: list[str]
    securityGroupIds: list[str]
    gatewayId: str
    tags: dict[str, str]
    activeLinksCount: int
    totalLinksCount: int
    ResponseMetadata: ResponseMetadataTypeDef

class ListRequesterGatewaysResponseTypeDef(TypedDict):
    gatewayIds: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListResponderGatewaysResponseTypeDef(TypedDict):
    gatewayIds: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class PutLinkFlowsResponseTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    status: LinkStatusType
    updateId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateLinkModuleFlowResponseTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    status: LinkStatusType
    updateId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateLinkResponseTypeDef(TypedDict):
    linkId: str
    status: LinkStatusType
    updateId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateLinkRoutingRuleResponseTypeDef(TypedDict):
    ruleId: str
    status: RuleStatusType
    updatedAt: datetime
    updateId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateRequesterGatewayResponseTypeDef(TypedDict):
    gatewayId: str
    status: RequesterGatewayStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateResponderGatewayResponseTypeDef(TypedDict):
    gatewayId: str
    status: ResponderGatewayStatusType
    clientRoutingPolicy: ClientRoutingPolicyType
    updateId: str
    ResponseMetadata: ResponseMetadataTypeDef

class ActionTypeDef(TypedDict):
    noBid: NotRequired[NoBidActionTypeDef]
    headerTag: NotRequired[HeaderTagActionTypeDef]

class AutoScalingGroupsConfigurationOutputTypeDef(TypedDict):
    autoScalingGroupNames: list[str]
    roleArn: str
    healthCheckConfig: NotRequired[HealthCheckConfigTypeDef]

class AutoScalingGroupsConfigurationTypeDef(TypedDict):
    autoScalingGroupNames: Sequence[str]
    roleArn: str
    healthCheckConfig: NotRequired[HealthCheckConfigTypeDef]

class ListAvailableModulesResponseTypeDef(TypedDict):
    modules: list[AvailableModuleSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAvailableModuleVersionsResponseTypeDef(TypedDict):
    moduleId: str
    versions: list[AvailableModuleVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListCertificateAssociationsResponseTypeDef(TypedDict):
    certificateAssociations: list[CertificateAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateResponderGatewayResponseTypeDef(TypedDict):
    gatewayId: str
    status: ResponderGatewayStatusType
    listenerConfig: ListenerConfigOutputTypeDef
    externalInboundEndpoint: str
    clientRoutingPolicy: ClientRoutingPolicyType
    ResponseMetadata: ResponseMetadataTypeDef

class FilterOutputTypeDef(TypedDict):
    criteria: list[FilterCriterionOutputTypeDef]

FilterCriterionUnionTypeDef = Union[FilterCriterionTypeDef, FilterCriterionOutputTypeDef]

class FlowPhaseOutputTypeDef(TypedDict):
    modules: list[FlowModuleOutputTypeDef]

class SequentialPipelineOutputTypeDef(TypedDict):
    modules: list[FlowModuleOutputTypeDef]

FlowModuleUnionTypeDef = Union[FlowModuleTypeDef, FlowModuleOutputTypeDef]

class SequentialPipelineTypeDef(TypedDict):
    modules: Sequence[FlowModuleTypeDef]

class GetCertificateAssociationRequestWaitExtraTypeDef(TypedDict):
    gatewayId: str
    acmCertificateArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetCertificateAssociationRequestWaitTypeDef(TypedDict):
    gatewayId: str
    acmCertificateArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetInboundExternalLinkRequestWaitExtraTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetInboundExternalLinkRequestWaitTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetLinkRequestWaitExtraExtraTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetLinkRequestWaitExtraTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetLinkRequestWaitTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetLinkRoutingRuleRequestWaitExtraTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    ruleId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetLinkRoutingRuleRequestWaitTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    ruleId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetOutboundExternalLinkRequestWaitExtraTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetOutboundExternalLinkRequestWaitTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetRequesterGatewayRequestWaitExtraTypeDef(TypedDict):
    gatewayId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetRequesterGatewayRequestWaitTypeDef(TypedDict):
    gatewayId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetResponderGatewayRequestWaitExtraTypeDef(TypedDict):
    gatewayId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetResponderGatewayRequestWaitTypeDef(TypedDict):
    gatewayId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class LinkApplicationLogConfigurationTypeDef(TypedDict):
    sampling: LinkApplicationLogSamplingTypeDef

class LinkAttributesOutputTypeDef(TypedDict):
    responderErrorMasking: NotRequired[list[ResponderErrorMaskingForHttpCodeOutputTypeDef]]
    customerProvidedId: NotRequired[str]

class LinkAttributesTypeDef(TypedDict):
    responderErrorMasking: NotRequired[Sequence[ResponderErrorMaskingForHttpCodeTypeDef]]
    customerProvidedId: NotRequired[str]

class ListAvailableModuleVersionsRequestPaginateTypeDef(TypedDict):
    moduleId: str
    status: NotRequired[ModuleVersionStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAvailableModulesRequestPaginateTypeDef(TypedDict):
    subscriptionType: NotRequired[SubscriptionTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCertificateAssociationsRequestPaginateTypeDef(TypedDict):
    gatewayId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListLinkRoutingRulesRequestPaginateTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListLinksRequestPaginateTypeDef(TypedDict):
    gatewayId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRequesterGatewaysRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListResponderGatewaysRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListUpdatesRequestPaginateTypeDef = TypedDict(
    "ListUpdatesRequestPaginateTypeDef",
    {
        "gatewayId": str,
        "linkId": NotRequired[str],
        "ruleId": NotRequired[str],
        "type": NotRequired[UpdateTypeType],
        "status": NotRequired[UpdateStatusType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListUpdatesResponseTypeDef(TypedDict):
    updates: list[UpdateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

ListenerConfigUnionTypeDef = Union[ListenerConfigTypeDef, ListenerConfigOutputTypeDef]

class RuleConditionTypeDef(TypedDict):
    hostHeader: NotRequired[str]
    hostHeaderWildcard: NotRequired[str]
    pathPrefix: NotRequired[str]
    pathExact: NotRequired[str]
    queryStringEquals: NotRequired[QueryStringKeyValuePairTypeDef]
    queryStringExists: NotRequired[str]

class UpdateTargetTypeDef(TypedDict):
    gateway: NotRequired[dict[str, Any]]
    link: NotRequired[LinkTargetTypeDef]
    routingRule: NotRequired[RoutingRuleTargetTypeDef]

TrustStoreConfigurationUnionTypeDef = Union[
    TrustStoreConfigurationTypeDef, TrustStoreConfigurationOutputTypeDef
]

class ManagedEndpointConfigurationOutputTypeDef(TypedDict):
    autoScalingGroups: NotRequired[AutoScalingGroupsConfigurationOutputTypeDef]
    eksEndpoints: NotRequired[EksEndpointsConfigurationTypeDef]

class ManagedEndpointConfigurationTypeDef(TypedDict):
    autoScalingGroups: NotRequired[AutoScalingGroupsConfigurationTypeDef]
    eksEndpoints: NotRequired[EksEndpointsConfigurationTypeDef]

class OpenRtbAttributeModuleParametersOutputTypeDef(TypedDict):
    filterType: FilterTypeType
    filterConfiguration: list[FilterOutputTypeDef]
    action: ActionTypeDef
    holdbackPercentage: float

class FilterTypeDef(TypedDict):
    criteria: Sequence[FilterCriterionUnionTypeDef]

class PhasedPipelineOutputTypeDef(TypedDict):
    phases: list[FlowPhaseOutputTypeDef]

class FlowPhaseTypeDef(TypedDict):
    modules: Sequence[FlowModuleUnionTypeDef]

SequentialPipelineUnionTypeDef = Union[SequentialPipelineTypeDef, SequentialPipelineOutputTypeDef]

class LinkLogSettingsTypeDef(TypedDict):
    applicationLogs: LinkApplicationLogConfigurationTypeDef

LinkAttributesUnionTypeDef = Union[LinkAttributesTypeDef, LinkAttributesOutputTypeDef]

class CreateLinkRoutingRuleRequestTypeDef(TypedDict):
    clientToken: str
    gatewayId: str
    linkId: str
    priority: int
    conditions: RuleConditionTypeDef
    tags: NotRequired[Mapping[str, str]]

class GetLinkRoutingRuleResponseTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    ruleId: str
    priority: int
    conditions: RuleConditionTypeDef
    status: RuleStatusType
    createdAt: datetime
    updatedAt: datetime
    tags: dict[str, str]
    errorDetails: list[ErrorDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class LinkRoutingRuleSummaryTypeDef(TypedDict):
    ruleId: str
    priority: int
    conditions: RuleConditionTypeDef
    status: RuleStatusType
    createdAt: datetime
    updatedAt: datetime
    errorDetails: NotRequired[list[ErrorDetailTypeDef]]

class RoutingRuleParametersTypeDef(TypedDict):
    priority: int
    conditions: RuleConditionTypeDef

class UpdateLinkRoutingRuleRequestTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    ruleId: str
    priority: int
    conditions: RuleConditionTypeDef
    clientToken: NotRequired[str]

class GetResponderGatewayResponseTypeDef(TypedDict):
    vpcId: str
    subnetIds: list[str]
    securityGroupIds: list[str]
    status: ResponderGatewayStatusType
    description: str
    createdAt: datetime
    updatedAt: datetime
    errorDetails: list[ErrorDetailTypeDef]
    domainName: str
    port: int
    protocol: ProtocolType
    listenerConfig: ListenerConfigOutputTypeDef
    trustStoreConfiguration: TrustStoreConfigurationOutputTypeDef
    managedEndpointConfiguration: ManagedEndpointConfigurationOutputTypeDef
    gatewayId: str
    tags: dict[str, str]
    activeLinksCount: int
    totalLinksCount: int
    linksRequestedCount: int
    gatewayType: GatewayTypeType
    externalInboundEndpoint: str
    clientRoutingPolicy: ClientRoutingPolicyType
    ResponseMetadata: ResponseMetadataTypeDef

class ResponderGatewayConfigParametersTypeDef(TypedDict):
    port: int
    protocol: ProtocolType
    description: NotRequired[str]
    clientRoutingPolicy: NotRequired[ClientRoutingPolicyType]
    domainName: NotRequired[str]
    listenerConfig: NotRequired[ListenerConfigOutputTypeDef]
    trustStoreConfiguration: NotRequired[TrustStoreConfigurationOutputTypeDef]
    managedEndpointConfiguration: NotRequired[ManagedEndpointConfigurationOutputTypeDef]

ManagedEndpointConfigurationUnionTypeDef = Union[
    ManagedEndpointConfigurationTypeDef, ManagedEndpointConfigurationOutputTypeDef
]

class ModuleParametersOutputTypeDef(TypedDict):
    noBid: NotRequired[NoBidModuleParametersTypeDef]
    openRtbAttribute: NotRequired[OpenRtbAttributeModuleParametersOutputTypeDef]
    rateLimiter: NotRequired[RateLimiterModuleParametersTypeDef]

FilterUnionTypeDef = Union[FilterTypeDef, FilterOutputTypeDef]

class FlowPipelineOutputTypeDef(TypedDict):
    sequential: NotRequired[SequentialPipelineOutputTypeDef]
    phased: NotRequired[PhasedPipelineOutputTypeDef]

FlowPhaseUnionTypeDef = Union[FlowPhaseTypeDef, FlowPhaseOutputTypeDef]

class LinkConfigParametersTypeDef(TypedDict):
    logSettings: NotRequired[LinkLogSettingsTypeDef]
    timeoutInMillis: NotRequired[int]

class UpdateLinkRequestTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    logSettings: NotRequired[LinkLogSettingsTypeDef]
    timeoutInMillis: NotRequired[int]
    clientToken: NotRequired[str]

class AcceptLinkRequestTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    logSettings: LinkLogSettingsTypeDef
    attributes: NotRequired[LinkAttributesUnionTypeDef]
    timeoutInMillis: NotRequired[int]

class CreateInboundExternalLinkRequestTypeDef(TypedDict):
    clientToken: str
    gatewayId: str
    logSettings: LinkLogSettingsTypeDef
    attributes: NotRequired[LinkAttributesUnionTypeDef]
    tags: NotRequired[Mapping[str, str]]

class CreateLinkRequestTypeDef(TypedDict):
    gatewayId: str
    peerGatewayId: str
    logSettings: LinkLogSettingsTypeDef
    attributes: NotRequired[LinkAttributesUnionTypeDef]
    httpResponderAllowed: NotRequired[bool]
    tags: NotRequired[Mapping[str, str]]
    timeoutInMillis: NotRequired[int]

class CreateOutboundExternalLinkRequestTypeDef(TypedDict):
    clientToken: str
    gatewayId: str
    publicEndpoint: str
    logSettings: LinkLogSettingsTypeDef
    attributes: NotRequired[LinkAttributesUnionTypeDef]
    tags: NotRequired[Mapping[str, str]]

class ListLinkRoutingRulesResponseTypeDef(TypedDict):
    rules: list[LinkRoutingRuleSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateResponderGatewayRequestTypeDef(TypedDict):
    vpcId: str
    subnetIds: Sequence[str]
    securityGroupIds: Sequence[str]
    port: int
    protocol: ProtocolType
    clientToken: str
    domainName: NotRequired[str]
    listenerConfig: NotRequired[ListenerConfigUnionTypeDef]
    trustStoreConfiguration: NotRequired[TrustStoreConfigurationUnionTypeDef]
    managedEndpointConfiguration: NotRequired[ManagedEndpointConfigurationUnionTypeDef]
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    gatewayType: NotRequired[GatewayTypeType]
    clientRoutingPolicy: NotRequired[ClientRoutingPolicyType]

class UpdateResponderGatewayRequestTypeDef(TypedDict):
    port: int
    protocol: ProtocolType
    clientToken: str
    gatewayId: str
    domainName: NotRequired[str]
    listenerConfig: NotRequired[ListenerConfigUnionTypeDef]
    trustStoreConfiguration: NotRequired[TrustStoreConfigurationUnionTypeDef]
    managedEndpointConfiguration: NotRequired[ManagedEndpointConfigurationUnionTypeDef]
    description: NotRequired[str]
    clientRoutingPolicy: NotRequired[ClientRoutingPolicyType]

class ModuleConfigurationOutputTypeDef(TypedDict):
    name: str
    version: NotRequired[str]
    dependsOn: NotRequired[list[str]]
    moduleParameters: NotRequired[ModuleParametersOutputTypeDef]

class OpenRtbAttributeModuleParametersTypeDef(TypedDict):
    filterType: FilterTypeType
    filterConfiguration: Sequence[FilterUnionTypeDef]
    action: ActionTypeDef
    holdbackPercentage: float

class FlowOutputTypeDef(TypedDict):
    name: str
    pipeline: FlowPipelineOutputTypeDef

class PhasedPipelineTypeDef(TypedDict):
    phases: Sequence[FlowPhaseUnionTypeDef]

class AcceptLinkResponseTypeDef(TypedDict):
    gatewayId: str
    peerGatewayId: str
    status: LinkStatusType
    createdAt: datetime
    updatedAt: datetime
    direction: LinkDirectionType
    flowModules: list[ModuleConfigurationOutputTypeDef]
    pendingFlowModules: list[ModuleConfigurationOutputTypeDef]
    attributes: LinkAttributesOutputTypeDef
    logSettings: LinkLogSettingsTypeDef
    connectivityType: ConnectivityTypeType
    errorDetails: list[ErrorDetailTypeDef]
    linkId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateLinkResponseTypeDef(TypedDict):
    gatewayId: str
    peerGatewayId: str
    status: LinkStatusType
    createdAt: datetime
    updatedAt: datetime
    direction: LinkDirectionType
    flowModules: list[ModuleConfigurationOutputTypeDef]
    pendingFlowModules: list[ModuleConfigurationOutputTypeDef]
    attributes: LinkAttributesOutputTypeDef
    logSettings: LinkLogSettingsTypeDef
    connectivityType: ConnectivityTypeType
    errorDetails: list[ErrorDetailTypeDef]
    linkId: str
    customerProvidedId: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListLinksResponseStructureTypeDef(TypedDict):
    gatewayId: str
    peerGatewayId: str
    status: LinkStatusType
    createdAt: datetime
    updatedAt: datetime
    linkId: str
    direction: NotRequired[LinkDirectionType]
    flowModules: NotRequired[list[ModuleConfigurationOutputTypeDef]]
    pendingFlowModules: NotRequired[list[ModuleConfigurationOutputTypeDef]]
    attributes: NotRequired[LinkAttributesOutputTypeDef]
    logSettings: NotRequired[LinkLogSettingsTypeDef]
    connectivityType: NotRequired[ConnectivityTypeType]
    errorDetails: NotRequired[list[ErrorDetailTypeDef]]
    tags: NotRequired[dict[str, str]]
    publicEndpoint: NotRequired[str]

class RejectLinkResponseTypeDef(TypedDict):
    gatewayId: str
    peerGatewayId: str
    status: LinkStatusType
    createdAt: datetime
    updatedAt: datetime
    direction: LinkDirectionType
    flowModules: list[ModuleConfigurationOutputTypeDef]
    pendingFlowModules: list[ModuleConfigurationOutputTypeDef]
    attributes: LinkAttributesOutputTypeDef
    logSettings: LinkLogSettingsTypeDef
    connectivityType: ConnectivityTypeType
    errorDetails: list[ErrorDetailTypeDef]
    linkId: str
    ResponseMetadata: ResponseMetadataTypeDef

OpenRtbAttributeModuleParametersUnionTypeDef = Union[
    OpenRtbAttributeModuleParametersTypeDef, OpenRtbAttributeModuleParametersOutputTypeDef
]

class GetInboundExternalLinkResponseTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    status: LinkStatusType
    domainName: str
    flowModules: list[ModuleConfigurationOutputTypeDef]
    pendingFlowModules: list[ModuleConfigurationOutputTypeDef]
    attributes: LinkAttributesOutputTypeDef
    createdAt: datetime
    updatedAt: datetime
    tags: dict[str, str]
    logSettings: LinkLogSettingsTypeDef
    connectivityType: ConnectivityTypeType
    errorDetails: list[ErrorDetailTypeDef]
    lockToken: str
    flows: list[FlowOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetLinkResponseTypeDef(TypedDict):
    gatewayId: str
    peerGatewayId: str
    status: LinkStatusType
    createdAt: datetime
    updatedAt: datetime
    direction: LinkDirectionType
    flowModules: list[ModuleConfigurationOutputTypeDef]
    pendingFlowModules: list[ModuleConfigurationOutputTypeDef]
    attributes: LinkAttributesOutputTypeDef
    logSettings: LinkLogSettingsTypeDef
    connectivityType: ConnectivityTypeType
    errorDetails: list[ErrorDetailTypeDef]
    linkId: str
    tags: dict[str, str]
    httpResponderAllowed: bool
    timeoutInMillis: int
    lockToken: str
    flows: list[FlowOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetOutboundExternalLinkResponseTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    status: LinkStatusType
    publicEndpoint: str
    flowModules: list[ModuleConfigurationOutputTypeDef]
    pendingFlowModules: list[ModuleConfigurationOutputTypeDef]
    attributes: LinkAttributesOutputTypeDef
    createdAt: datetime
    updatedAt: datetime
    tags: dict[str, str]
    logSettings: LinkLogSettingsTypeDef
    connectivityType: ConnectivityTypeType
    errorDetails: list[ErrorDetailTypeDef]
    lockToken: str
    flows: list[FlowOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class LinkFlowParametersTypeDef(TypedDict):
    modules: NotRequired[list[ModuleConfigurationOutputTypeDef]]
    flows: NotRequired[list[FlowOutputTypeDef]]

PhasedPipelineUnionTypeDef = Union[PhasedPipelineTypeDef, PhasedPipelineOutputTypeDef]

class ListLinksResponseTypeDef(TypedDict):
    links: list[ListLinksResponseStructureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ModuleParametersTypeDef(TypedDict):
    noBid: NotRequired[NoBidModuleParametersTypeDef]
    openRtbAttribute: NotRequired[OpenRtbAttributeModuleParametersUnionTypeDef]
    rateLimiter: NotRequired[RateLimiterModuleParametersTypeDef]

class UpdateParametersTypeDef(TypedDict):
    responderGatewayConfig: NotRequired[ResponderGatewayConfigParametersTypeDef]
    linkConfig: NotRequired[LinkConfigParametersTypeDef]
    linkFlow: NotRequired[LinkFlowParametersTypeDef]
    routingRule: NotRequired[RoutingRuleParametersTypeDef]

class FlowPipelineTypeDef(TypedDict):
    sequential: NotRequired[SequentialPipelineUnionTypeDef]
    phased: NotRequired[PhasedPipelineUnionTypeDef]

ModuleParametersUnionTypeDef = Union[ModuleParametersTypeDef, ModuleParametersOutputTypeDef]
UpdateTypeDef = TypedDict(
    "UpdateTypeDef",
    {
        "updateId": str,
        "type": UpdateTypeType,
        "status": UpdateStatusType,
        "target": UpdateTargetTypeDef,
        "createdAt": datetime,
        "parameters": NotRequired[UpdateParametersTypeDef],
        "errorDetails": NotRequired[list[ErrorDetailTypeDef]],
    },
)
FlowPipelineUnionTypeDef = Union[FlowPipelineTypeDef, FlowPipelineOutputTypeDef]

class ModuleConfigurationTypeDef(TypedDict):
    name: str
    version: NotRequired[str]
    dependsOn: NotRequired[Sequence[str]]
    moduleParameters: NotRequired[ModuleParametersUnionTypeDef]

class GetUpdateResponseTypeDef(TypedDict):
    update: UpdateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class FlowTypeDef(TypedDict):
    name: str
    pipeline: FlowPipelineUnionTypeDef

ModuleConfigurationUnionTypeDef = Union[
    ModuleConfigurationTypeDef, ModuleConfigurationOutputTypeDef
]
FlowUnionTypeDef = Union[FlowTypeDef, FlowOutputTypeDef]

class UpdateLinkModuleFlowRequestTypeDef(TypedDict):
    clientToken: str
    gatewayId: str
    linkId: str
    modules: Sequence[ModuleConfigurationUnionTypeDef]

class PutLinkFlowsRequestTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    lockToken: str
    flows: Sequence[FlowUnionTypeDef]
    clientToken: NotRequired[str]
