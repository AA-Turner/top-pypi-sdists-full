"""
Type annotations for rtbfabric service type definitions.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_aiobotocore_rtbfabric.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    ConnectivityTypeType,
    FilterTypeType,
    GatewayTypeType,
    LinkDirectionType,
    LinkStatusType,
    ProtocolType,
    RequesterGatewayStatusType,
    ResponderErrorMaskingActionType,
    ResponderErrorMaskingLoggingTypeType,
    ResponderGatewayStatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AcceptLinkRequestTypeDef",
    "AcceptLinkResponseTypeDef",
    "ActionTypeDef",
    "AutoScalingGroupsConfigurationOutputTypeDef",
    "AutoScalingGroupsConfigurationTypeDef",
    "CreateInboundExternalLinkRequestTypeDef",
    "CreateInboundExternalLinkResponseTypeDef",
    "CreateLinkRequestTypeDef",
    "CreateLinkResponseTypeDef",
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
    "DeleteOutboundExternalLinkRequestTypeDef",
    "DeleteOutboundExternalLinkResponseTypeDef",
    "DeleteRequesterGatewayRequestTypeDef",
    "DeleteRequesterGatewayResponseTypeDef",
    "DeleteResponderGatewayRequestTypeDef",
    "DeleteResponderGatewayResponseTypeDef",
    "EksEndpointsConfigurationTypeDef",
    "FilterCriterionOutputTypeDef",
    "FilterCriterionTypeDef",
    "FilterCriterionUnionTypeDef",
    "FilterOutputTypeDef",
    "FilterTypeDef",
    "FilterUnionTypeDef",
    "GetInboundExternalLinkRequestTypeDef",
    "GetInboundExternalLinkRequestWaitExtraTypeDef",
    "GetInboundExternalLinkRequestWaitTypeDef",
    "GetInboundExternalLinkResponseTypeDef",
    "GetLinkRequestTypeDef",
    "GetLinkRequestWaitExtraExtraTypeDef",
    "GetLinkRequestWaitExtraTypeDef",
    "GetLinkRequestWaitTypeDef",
    "GetLinkResponseTypeDef",
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
    "HeaderTagActionTypeDef",
    "HealthCheckConfigTypeDef",
    "LinkApplicationLogConfigurationTypeDef",
    "LinkApplicationLogSamplingTypeDef",
    "LinkAttributesOutputTypeDef",
    "LinkAttributesTypeDef",
    "LinkAttributesUnionTypeDef",
    "LinkLogSettingsTypeDef",
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
    "RateLimiterModuleParametersTypeDef",
    "RejectLinkRequestTypeDef",
    "RejectLinkResponseTypeDef",
    "ResponderErrorMaskingForHttpCodeOutputTypeDef",
    "ResponderErrorMaskingForHttpCodeTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestTypeDef",
    "TrustStoreConfigurationOutputTypeDef",
    "TrustStoreConfigurationTypeDef",
    "TrustStoreConfigurationUnionTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateLinkModuleFlowRequestTypeDef",
    "UpdateLinkModuleFlowResponseTypeDef",
    "UpdateLinkRequestTypeDef",
    "UpdateLinkResponseTypeDef",
    "UpdateRequesterGatewayRequestTypeDef",
    "UpdateRequesterGatewayResponseTypeDef",
    "UpdateResponderGatewayRequestTypeDef",
    "UpdateResponderGatewayResponseTypeDef",
    "WaiterConfigTypeDef",
)


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


class HealthCheckConfigTypeDef(TypedDict):
    port: int
    path: str
    protocol: NotRequired[ProtocolType]
    timeoutMs: NotRequired[int]
    intervalSeconds: NotRequired[int]
    statusCodeMatcher: NotRequired[str]
    healthyThresholdCount: NotRequired[int]
    unhealthyThresholdCount: NotRequired[int]


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


class DeleteOutboundExternalLinkRequestTypeDef(TypedDict):
    gatewayId: str
    linkId: str


class DeleteRequesterGatewayRequestTypeDef(TypedDict):
    gatewayId: str


class DeleteResponderGatewayRequestTypeDef(TypedDict):
    gatewayId: str


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


class GetInboundExternalLinkRequestTypeDef(TypedDict):
    gatewayId: str
    linkId: str


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class GetLinkRequestTypeDef(TypedDict):
    gatewayId: str
    linkId: str


class GetOutboundExternalLinkRequestTypeDef(TypedDict):
    gatewayId: str
    linkId: str


class GetRequesterGatewayRequestTypeDef(TypedDict):
    gatewayId: str


class GetResponderGatewayRequestTypeDef(TypedDict):
    gatewayId: str


class TrustStoreConfigurationOutputTypeDef(TypedDict):
    certificateAuthorityCertificates: list[str]


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


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


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


class ListenerConfigTypeDef(TypedDict):
    protocols: Sequence[ProtocolType]


class NoBidModuleParametersTypeDef(TypedDict):
    reason: NotRequired[str]
    reasonCode: NotRequired[int]
    passThroughPercentage: NotRequired[float]


class RateLimiterModuleParametersTypeDef(TypedDict):
    tps: NotRequired[float]


class RejectLinkRequestTypeDef(TypedDict):
    gatewayId: str
    linkId: str


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


class CreateInboundExternalLinkResponseTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    status: LinkStatusType
    domainName: str
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


class GetRequesterGatewayResponseTypeDef(TypedDict):
    status: RequesterGatewayStatusType
    domainName: str
    description: str
    createdAt: datetime
    updatedAt: datetime
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


class UpdateLinkModuleFlowResponseTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    status: LinkStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateLinkResponseTypeDef(TypedDict):
    linkId: str
    status: LinkStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRequesterGatewayResponseTypeDef(TypedDict):
    gatewayId: str
    status: RequesterGatewayStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateResponderGatewayResponseTypeDef(TypedDict):
    gatewayId: str
    status: ResponderGatewayStatusType
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


class CreateResponderGatewayResponseTypeDef(TypedDict):
    gatewayId: str
    status: ResponderGatewayStatusType
    listenerConfig: ListenerConfigOutputTypeDef
    externalInboundEndpoint: str
    ResponseMetadata: ResponseMetadataTypeDef


class FilterOutputTypeDef(TypedDict):
    criteria: list[FilterCriterionOutputTypeDef]


FilterCriterionUnionTypeDef = Union[FilterCriterionTypeDef, FilterCriterionOutputTypeDef]


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


class ListLinksRequestPaginateTypeDef(TypedDict):
    gatewayId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRequesterGatewaysRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResponderGatewaysRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListenerConfigUnionTypeDef = Union[ListenerConfigTypeDef, ListenerConfigOutputTypeDef]
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


class LinkLogSettingsTypeDef(TypedDict):
    applicationLogs: LinkApplicationLogConfigurationTypeDef


LinkAttributesUnionTypeDef = Union[LinkAttributesTypeDef, LinkAttributesOutputTypeDef]


class GetResponderGatewayResponseTypeDef(TypedDict):
    vpcId: str
    subnetIds: list[str]
    securityGroupIds: list[str]
    status: ResponderGatewayStatusType
    description: str
    createdAt: datetime
    updatedAt: datetime
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
    inboundLinksCount: int
    gatewayType: GatewayTypeType
    externalInboundEndpoint: str
    ResponseMetadata: ResponseMetadataTypeDef


ManagedEndpointConfigurationUnionTypeDef = Union[
    ManagedEndpointConfigurationTypeDef, ManagedEndpointConfigurationOutputTypeDef
]


class ModuleParametersOutputTypeDef(TypedDict):
    noBid: NotRequired[NoBidModuleParametersTypeDef]
    openRtbAttribute: NotRequired[OpenRtbAttributeModuleParametersOutputTypeDef]
    rateLimiter: NotRequired[RateLimiterModuleParametersTypeDef]


FilterUnionTypeDef = Union[FilterTypeDef, FilterOutputTypeDef]


class UpdateLinkRequestTypeDef(TypedDict):
    gatewayId: str
    linkId: str
    logSettings: NotRequired[LinkLogSettingsTypeDef]
    timeoutInMillis: NotRequired[int]


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
    linkId: str
    customerProvidedId: str
    ResponseMetadata: ResponseMetadataTypeDef


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
    linkId: str
    tags: dict[str, str]
    httpResponderAllowed: bool
    timeoutInMillis: int
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
    linkId: str
    ResponseMetadata: ResponseMetadataTypeDef


OpenRtbAttributeModuleParametersUnionTypeDef = Union[
    OpenRtbAttributeModuleParametersTypeDef, OpenRtbAttributeModuleParametersOutputTypeDef
]


class ListLinksResponseTypeDef(TypedDict):
    links: list[ListLinksResponseStructureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ModuleParametersTypeDef(TypedDict):
    noBid: NotRequired[NoBidModuleParametersTypeDef]
    openRtbAttribute: NotRequired[OpenRtbAttributeModuleParametersUnionTypeDef]
    rateLimiter: NotRequired[RateLimiterModuleParametersTypeDef]


ModuleParametersUnionTypeDef = Union[ModuleParametersTypeDef, ModuleParametersOutputTypeDef]


class ModuleConfigurationTypeDef(TypedDict):
    name: str
    version: NotRequired[str]
    dependsOn: NotRequired[Sequence[str]]
    moduleParameters: NotRequired[ModuleParametersUnionTypeDef]


ModuleConfigurationUnionTypeDef = Union[
    ModuleConfigurationTypeDef, ModuleConfigurationOutputTypeDef
]


class UpdateLinkModuleFlowRequestTypeDef(TypedDict):
    clientToken: str
    gatewayId: str
    linkId: str
    modules: Sequence[ModuleConfigurationUnionTypeDef]
