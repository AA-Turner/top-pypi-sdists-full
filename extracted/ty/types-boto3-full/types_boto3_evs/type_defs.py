"""
Type annotations for evs service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_evs/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_evs.type_defs import AssociateEipToVlanRequestTypeDef

    data: AssociateEipToVlanRequestTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    CheckResultType,
    CheckTypeType,
    ConnectorStateType,
    ConnectorTypeType,
    EntitlementStatusType,
    EnvironmentStateType,
    HostStateType,
    InstanceTypeType,
    VcfVersionType,
    VlanStateType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AssociateEipToVlanRequestTypeDef",
    "AssociateEipToVlanResponseTypeDef",
    "CheckTypeDef",
    "ConnectivityInfoOutputTypeDef",
    "ConnectivityInfoTypeDef",
    "ConnectivityInfoUnionTypeDef",
    "ConnectorCheckTypeDef",
    "ConnectorTypeDef",
    "CreateEntitlementRequestTypeDef",
    "CreateEntitlementResponseTypeDef",
    "CreateEnvironmentConnectorRequestTypeDef",
    "CreateEnvironmentConnectorResponseTypeDef",
    "CreateEnvironmentHostRequestTypeDef",
    "CreateEnvironmentHostResponseTypeDef",
    "CreateEnvironmentRequestTypeDef",
    "CreateEnvironmentResponseTypeDef",
    "DeleteEntitlementRequestTypeDef",
    "DeleteEntitlementResponseTypeDef",
    "DeleteEnvironmentConnectorRequestTypeDef",
    "DeleteEnvironmentConnectorResponseTypeDef",
    "DeleteEnvironmentHostRequestTypeDef",
    "DeleteEnvironmentHostResponseTypeDef",
    "DeleteEnvironmentRequestTypeDef",
    "DeleteEnvironmentResponseTypeDef",
    "DisassociateEipFromVlanRequestTypeDef",
    "DisassociateEipFromVlanResponseTypeDef",
    "EipAssociationTypeDef",
    "EnvironmentSummaryTypeDef",
    "EnvironmentTypeDef",
    "ErrorDetailTypeDef",
    "GetDepotUrlRequestTypeDef",
    "GetDepotUrlResponseTypeDef",
    "GetEnvironmentRequestTypeDef",
    "GetEnvironmentResponseTypeDef",
    "GetVersionsResponseTypeDef",
    "HostInfoForCreateTypeDef",
    "HostTypeDef",
    "InitialVlanInfoTypeDef",
    "InitialVlansTypeDef",
    "InstanceTypeEsxVersionsInfoTypeDef",
    "LicenseInfoTypeDef",
    "ListEnvironmentConnectorsRequestPaginateTypeDef",
    "ListEnvironmentConnectorsRequestTypeDef",
    "ListEnvironmentConnectorsResponseTypeDef",
    "ListEnvironmentHostsRequestPaginateTypeDef",
    "ListEnvironmentHostsRequestTypeDef",
    "ListEnvironmentHostsResponseTypeDef",
    "ListEnvironmentVlansRequestPaginateTypeDef",
    "ListEnvironmentVlansRequestTypeDef",
    "ListEnvironmentVlansResponseTypeDef",
    "ListEnvironmentsRequestPaginateTypeDef",
    "ListEnvironmentsRequestTypeDef",
    "ListEnvironmentsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListVmEntitlementsRequestPaginateTypeDef",
    "ListVmEntitlementsRequestTypeDef",
    "ListVmEntitlementsResponseTypeDef",
    "NetworkInterfaceTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "SecretTypeDef",
    "ServiceAccessSecurityGroupsOutputTypeDef",
    "ServiceAccessSecurityGroupsTypeDef",
    "ServiceAccessSecurityGroupsUnionTypeDef",
    "TagResourceRequestTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateEnvironmentConnectorRequestTypeDef",
    "UpdateEnvironmentConnectorResponseTypeDef",
    "VcfHostnamesTypeDef",
    "VcfVersionInfoTypeDef",
    "VlanTypeDef",
    "VmEntitlementTypeDef",
)


class AssociateEipToVlanRequestTypeDef(TypedDict):
    environmentId: str
    vlanName: str
    allocationId: str
    clientToken: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


CheckTypeDef = TypedDict(
    "CheckTypeDef",
    {
        "type": NotRequired[CheckTypeType],
        "id": NotRequired[str],
        "result": NotRequired[CheckResultType],
        "impairedSince": NotRequired[datetime],
    },
)


class ConnectivityInfoOutputTypeDef(TypedDict):
    privateRouteServerPeerings: list[str]


class ConnectivityInfoTypeDef(TypedDict):
    privateRouteServerPeerings: Sequence[str]


ConnectorCheckTypeDef = TypedDict(
    "ConnectorCheckTypeDef",
    {
        "type": NotRequired[CheckTypeType],
        "result": NotRequired[CheckResultType],
        "lastCheckAttempt": NotRequired[datetime],
        "impairedSince": NotRequired[datetime],
    },
)


class CreateEntitlementRequestTypeDef(TypedDict):
    environmentId: str
    connectorId: str
    entitlementType: Literal["WINDOWS_SERVER"]
    vmIds: Sequence[str]
    clientToken: NotRequired[str]


CreateEnvironmentConnectorRequestTypeDef = TypedDict(
    "CreateEnvironmentConnectorRequestTypeDef",
    {
        "environmentId": str,
        "type": ConnectorTypeType,
        "applianceFqdn": str,
        "secretIdentifier": str,
        "clientToken": NotRequired[str],
    },
)


class HostInfoForCreateTypeDef(TypedDict):
    hostName: str
    keyName: str
    instanceType: InstanceTypeType
    placementGroupId: NotRequired[str]
    dedicatedHostId: NotRequired[str]


class EnvironmentSummaryTypeDef(TypedDict):
    environmentId: NotRequired[str]
    environmentName: NotRequired[str]
    vcfVersion: NotRequired[VcfVersionType]
    environmentStatus: NotRequired[CheckResultType]
    environmentState: NotRequired[EnvironmentStateType]
    createdAt: NotRequired[datetime]
    modifiedAt: NotRequired[datetime]
    environmentArn: NotRequired[str]


class LicenseInfoTypeDef(TypedDict):
    solutionKey: str
    vsanKey: str


class VcfHostnamesTypeDef(TypedDict):
    vCenter: str
    nsx: str
    nsxManager1: str
    nsxManager2: str
    nsxManager3: str
    nsxEdge1: str
    nsxEdge2: str
    sddcManager: str
    cloudBuilder: str


class DeleteEntitlementRequestTypeDef(TypedDict):
    environmentId: str
    connectorId: str
    entitlementType: Literal["WINDOWS_SERVER"]
    vmIds: Sequence[str]
    clientToken: NotRequired[str]


class DeleteEnvironmentConnectorRequestTypeDef(TypedDict):
    environmentId: str
    connectorId: str
    clientToken: NotRequired[str]


class DeleteEnvironmentHostRequestTypeDef(TypedDict):
    environmentId: str
    hostName: str
    clientToken: NotRequired[str]


class DeleteEnvironmentRequestTypeDef(TypedDict):
    environmentId: str
    clientToken: NotRequired[str]


class DisassociateEipFromVlanRequestTypeDef(TypedDict):
    environmentId: str
    vlanName: str
    associationId: str
    clientToken: NotRequired[str]


class EipAssociationTypeDef(TypedDict):
    associationId: NotRequired[str]
    allocationId: NotRequired[str]
    ipAddress: NotRequired[str]


class SecretTypeDef(TypedDict):
    secretArn: NotRequired[str]


class ServiceAccessSecurityGroupsOutputTypeDef(TypedDict):
    securityGroups: NotRequired[list[str]]


class ErrorDetailTypeDef(TypedDict):
    errorCode: str
    errorMessage: str


class GetDepotUrlRequestTypeDef(TypedDict):
    environmentId: str
    rotate: NotRequired[bool]


class GetEnvironmentRequestTypeDef(TypedDict):
    environmentId: str


class InstanceTypeEsxVersionsInfoTypeDef(TypedDict):
    instanceType: InstanceTypeType
    esxVersions: list[str]


class VcfVersionInfoTypeDef(TypedDict):
    vcfVersion: VcfVersionType
    status: str
    defaultEsxVersion: str
    instanceTypes: list[InstanceTypeType]


class NetworkInterfaceTypeDef(TypedDict):
    networkInterfaceId: NotRequired[str]


class InitialVlanInfoTypeDef(TypedDict):
    cidr: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListEnvironmentConnectorsRequestTypeDef(TypedDict):
    environmentId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListEnvironmentHostsRequestTypeDef(TypedDict):
    environmentId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListEnvironmentVlansRequestTypeDef(TypedDict):
    environmentId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListEnvironmentsRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    state: NotRequired[Sequence[EnvironmentStateType]]


class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str


class ListVmEntitlementsRequestTypeDef(TypedDict):
    environmentId: str
    connectorId: str
    entitlementType: Literal["WINDOWS_SERVER"]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ServiceAccessSecurityGroupsTypeDef(TypedDict):
    securityGroups: NotRequired[Sequence[str]]


class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateEnvironmentConnectorRequestTypeDef(TypedDict):
    environmentId: str
    connectorId: str
    clientToken: NotRequired[str]
    applianceFqdn: NotRequired[str]
    secretIdentifier: NotRequired[str]


class GetDepotUrlResponseTypeDef(TypedDict):
    depotUrl: str
    token: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


ConnectivityInfoUnionTypeDef = Union[ConnectivityInfoTypeDef, ConnectivityInfoOutputTypeDef]
ConnectorTypeDef = TypedDict(
    "ConnectorTypeDef",
    {
        "environmentId": NotRequired[str],
        "connectorId": NotRequired[str],
        "type": NotRequired[ConnectorTypeType],
        "applianceFqdn": NotRequired[str],
        "secretArn": NotRequired[str],
        "state": NotRequired[ConnectorStateType],
        "stateDetails": NotRequired[str],
        "status": NotRequired[CheckResultType],
        "checks": NotRequired[list[ConnectorCheckTypeDef]],
        "createdAt": NotRequired[datetime],
        "modifiedAt": NotRequired[datetime],
    },
)


class CreateEnvironmentHostRequestTypeDef(TypedDict):
    environmentId: str
    host: HostInfoForCreateTypeDef
    clientToken: NotRequired[str]
    esxVersion: NotRequired[str]


class ListEnvironmentsResponseTypeDef(TypedDict):
    environmentSummaries: list[EnvironmentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class VlanTypeDef(TypedDict):
    vlanId: NotRequired[int]
    cidr: NotRequired[str]
    availabilityZone: NotRequired[str]
    functionName: NotRequired[str]
    subnetId: NotRequired[str]
    createdAt: NotRequired[datetime]
    modifiedAt: NotRequired[datetime]
    vlanState: NotRequired[VlanStateType]
    stateDetails: NotRequired[str]
    eipAssociations: NotRequired[list[EipAssociationTypeDef]]
    isPublic: NotRequired[bool]
    networkAclId: NotRequired[str]


class EnvironmentTypeDef(TypedDict):
    environmentId: NotRequired[str]
    environmentState: NotRequired[EnvironmentStateType]
    stateDetails: NotRequired[str]
    createdAt: NotRequired[datetime]
    modifiedAt: NotRequired[datetime]
    environmentArn: NotRequired[str]
    environmentName: NotRequired[str]
    vpcId: NotRequired[str]
    serviceAccessSubnetId: NotRequired[str]
    vcfVersion: NotRequired[VcfVersionType]
    termsAccepted: NotRequired[bool]
    licenseInfo: NotRequired[list[LicenseInfoTypeDef]]
    siteId: NotRequired[str]
    environmentStatus: NotRequired[CheckResultType]
    checks: NotRequired[list[CheckTypeDef]]
    connectivityInfo: NotRequired[ConnectivityInfoOutputTypeDef]
    vcfHostnames: NotRequired[VcfHostnamesTypeDef]
    kmsKeyId: NotRequired[str]
    serviceAccessSecurityGroups: NotRequired[ServiceAccessSecurityGroupsOutputTypeDef]
    credentials: NotRequired[list[SecretTypeDef]]


VmEntitlementTypeDef = TypedDict(
    "VmEntitlementTypeDef",
    {
        "vmId": NotRequired[str],
        "environmentId": NotRequired[str],
        "connectorId": NotRequired[str],
        "vmName": NotRequired[str],
        "type": NotRequired[Literal["WINDOWS_SERVER"]],
        "status": NotRequired[EntitlementStatusType],
        "lastSyncedAt": NotRequired[datetime],
        "startedAt": NotRequired[datetime],
        "stoppedAt": NotRequired[datetime],
        "errorDetail": NotRequired[ErrorDetailTypeDef],
    },
)


class GetVersionsResponseTypeDef(TypedDict):
    vcfVersions: list[VcfVersionInfoTypeDef]
    instanceTypeEsxVersions: list[InstanceTypeEsxVersionsInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class HostTypeDef(TypedDict):
    hostName: NotRequired[str]
    ipAddress: NotRequired[str]
    keyName: NotRequired[str]
    instanceType: NotRequired[InstanceTypeType]
    placementGroupId: NotRequired[str]
    dedicatedHostId: NotRequired[str]
    createdAt: NotRequired[datetime]
    modifiedAt: NotRequired[datetime]
    hostState: NotRequired[HostStateType]
    stateDetails: NotRequired[str]
    ec2InstanceId: NotRequired[str]
    networkInterfaces: NotRequired[list[NetworkInterfaceTypeDef]]


class InitialVlansTypeDef(TypedDict):
    vmkManagement: InitialVlanInfoTypeDef
    vmManagement: InitialVlanInfoTypeDef
    vMotion: InitialVlanInfoTypeDef
    vSan: InitialVlanInfoTypeDef
    vTep: InitialVlanInfoTypeDef
    edgeVTep: InitialVlanInfoTypeDef
    nsxUplink: InitialVlanInfoTypeDef
    hcx: InitialVlanInfoTypeDef
    expansionVlan1: InitialVlanInfoTypeDef
    expansionVlan2: InitialVlanInfoTypeDef
    isHcxPublic: NotRequired[bool]
    hcxNetworkAclId: NotRequired[str]


class ListEnvironmentConnectorsRequestPaginateTypeDef(TypedDict):
    environmentId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEnvironmentHostsRequestPaginateTypeDef(TypedDict):
    environmentId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEnvironmentVlansRequestPaginateTypeDef(TypedDict):
    environmentId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEnvironmentsRequestPaginateTypeDef(TypedDict):
    state: NotRequired[Sequence[EnvironmentStateType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListVmEntitlementsRequestPaginateTypeDef(TypedDict):
    environmentId: str
    connectorId: str
    entitlementType: Literal["WINDOWS_SERVER"]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ServiceAccessSecurityGroupsUnionTypeDef = Union[
    ServiceAccessSecurityGroupsTypeDef, ServiceAccessSecurityGroupsOutputTypeDef
]


class CreateEnvironmentConnectorResponseTypeDef(TypedDict):
    connector: ConnectorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteEnvironmentConnectorResponseTypeDef(TypedDict):
    connector: ConnectorTypeDef
    environmentSummary: EnvironmentSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListEnvironmentConnectorsResponseTypeDef(TypedDict):
    connectors: list[ConnectorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateEnvironmentConnectorResponseTypeDef(TypedDict):
    connector: ConnectorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateEipToVlanResponseTypeDef(TypedDict):
    vlan: VlanTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateEipFromVlanResponseTypeDef(TypedDict):
    vlan: VlanTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListEnvironmentVlansResponseTypeDef(TypedDict):
    environmentVlans: list[VlanTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateEnvironmentResponseTypeDef(TypedDict):
    environment: EnvironmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteEnvironmentResponseTypeDef(TypedDict):
    environment: EnvironmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetEnvironmentResponseTypeDef(TypedDict):
    environment: EnvironmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateEntitlementResponseTypeDef(TypedDict):
    entitlements: list[VmEntitlementTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteEntitlementResponseTypeDef(TypedDict):
    entitlements: list[VmEntitlementTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListVmEntitlementsResponseTypeDef(TypedDict):
    entitlements: list[VmEntitlementTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateEnvironmentHostResponseTypeDef(TypedDict):
    environmentSummary: EnvironmentSummaryTypeDef
    host: HostTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteEnvironmentHostResponseTypeDef(TypedDict):
    environmentSummary: EnvironmentSummaryTypeDef
    host: HostTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListEnvironmentHostsResponseTypeDef(TypedDict):
    environmentHosts: list[HostTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateEnvironmentRequestTypeDef(TypedDict):
    vpcId: str
    serviceAccessSubnetId: str
    vcfVersion: VcfVersionType
    termsAccepted: bool
    initialVlans: InitialVlansTypeDef
    clientToken: NotRequired[str]
    environmentName: NotRequired[str]
    kmsKeyId: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    serviceAccessSecurityGroups: NotRequired[ServiceAccessSecurityGroupsUnionTypeDef]
    connectivityInfo: NotRequired[ConnectivityInfoUnionTypeDef]
    licenseInfo: NotRequired[Sequence[LicenseInfoTypeDef]]
    hosts: NotRequired[Sequence[HostInfoForCreateTypeDef]]
    vcfHostnames: NotRequired[VcfHostnamesTypeDef]
    siteId: NotRequired[str]
