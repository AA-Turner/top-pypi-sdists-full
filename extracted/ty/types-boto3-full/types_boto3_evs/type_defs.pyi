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
    EnvironmentStateType,
    HostStateType,
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
    "CreateEnvironmentHostRequestTypeDef",
    "CreateEnvironmentHostResponseTypeDef",
    "CreateEnvironmentRequestTypeDef",
    "CreateEnvironmentResponseTypeDef",
    "DeleteEnvironmentHostRequestTypeDef",
    "DeleteEnvironmentHostResponseTypeDef",
    "DeleteEnvironmentRequestTypeDef",
    "DeleteEnvironmentResponseTypeDef",
    "DisassociateEipFromVlanRequestTypeDef",
    "DisassociateEipFromVlanResponseTypeDef",
    "EipAssociationTypeDef",
    "EnvironmentSummaryTypeDef",
    "EnvironmentTypeDef",
    "GetEnvironmentRequestTypeDef",
    "GetEnvironmentResponseTypeDef",
    "GetVersionsResponseTypeDef",
    "HostInfoForCreateTypeDef",
    "HostTypeDef",
    "InitialVlanInfoTypeDef",
    "InitialVlansTypeDef",
    "InstanceTypeEsxVersionsInfoTypeDef",
    "LicenseInfoTypeDef",
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
    "NetworkInterfaceTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "SecretTypeDef",
    "ServiceAccessSecurityGroupsOutputTypeDef",
    "ServiceAccessSecurityGroupsTypeDef",
    "ServiceAccessSecurityGroupsUnionTypeDef",
    "TagResourceRequestTypeDef",
    "UntagResourceRequestTypeDef",
    "VcfHostnamesTypeDef",
    "VcfVersionInfoTypeDef",
    "VlanTypeDef",
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
        "result": NotRequired[CheckResultType],
        "impairedSince": NotRequired[datetime],
    },
)

class ConnectivityInfoOutputTypeDef(TypedDict):
    privateRouteServerPeerings: list[str]

class ConnectivityInfoTypeDef(TypedDict):
    privateRouteServerPeerings: Sequence[str]

class HostInfoForCreateTypeDef(TypedDict):
    hostName: str
    keyName: str
    instanceType: Literal["i4i.metal"]
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

class GetEnvironmentRequestTypeDef(TypedDict):
    environmentId: str

class InstanceTypeEsxVersionsInfoTypeDef(TypedDict):
    instanceType: Literal["i4i.metal"]
    esxVersions: list[str]

class VcfVersionInfoTypeDef(TypedDict):
    vcfVersion: VcfVersionType
    status: str
    defaultEsxVersion: str
    instanceTypes: list[Literal["i4i.metal"]]

class NetworkInterfaceTypeDef(TypedDict):
    networkInterfaceId: NotRequired[str]

class InitialVlanInfoTypeDef(TypedDict):
    cidr: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

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

class ServiceAccessSecurityGroupsTypeDef(TypedDict):
    securityGroups: NotRequired[Sequence[str]]

class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

ConnectivityInfoUnionTypeDef = Union[ConnectivityInfoTypeDef, ConnectivityInfoOutputTypeDef]

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

class GetVersionsResponseTypeDef(TypedDict):
    vcfVersions: list[VcfVersionInfoTypeDef]
    instanceTypeEsxVersions: list[InstanceTypeEsxVersionsInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class HostTypeDef(TypedDict):
    hostName: NotRequired[str]
    ipAddress: NotRequired[str]
    keyName: NotRequired[str]
    instanceType: NotRequired[Literal["i4i.metal"]]
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

class ListEnvironmentHostsRequestPaginateTypeDef(TypedDict):
    environmentId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEnvironmentVlansRequestPaginateTypeDef(TypedDict):
    environmentId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEnvironmentsRequestPaginateTypeDef(TypedDict):
    state: NotRequired[Sequence[EnvironmentStateType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ServiceAccessSecurityGroupsUnionTypeDef = Union[
    ServiceAccessSecurityGroupsTypeDef, ServiceAccessSecurityGroupsOutputTypeDef
]

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
    licenseInfo: Sequence[LicenseInfoTypeDef]
    initialVlans: InitialVlansTypeDef
    hosts: Sequence[HostInfoForCreateTypeDef]
    connectivityInfo: ConnectivityInfoUnionTypeDef
    vcfHostnames: VcfHostnamesTypeDef
    siteId: str
    clientToken: NotRequired[str]
    environmentName: NotRequired[str]
    kmsKeyId: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    serviceAccessSecurityGroups: NotRequired[ServiceAccessSecurityGroupsUnionTypeDef]
