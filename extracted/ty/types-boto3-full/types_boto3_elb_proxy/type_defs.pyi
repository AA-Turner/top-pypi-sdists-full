"""
Type annotations for elb-proxy service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_elb_proxy.type_defs import AssociateCertificateRequestTypeDef

    data: AssociateCertificateRequestTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import IO, Any, Union

from botocore.response import StreamingBody

from .literals import (
    CertificateAssociationStatusCodeType,
    ProxyIpv4AddressabilityType,
    ProxyIpv6AddressabilityType,
    ProxyStatusCodeType,
    ProxyUpdatePropagationStatusType,
    ProxyUpdateValidationStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AssociateCertificateRequestTypeDef",
    "AssociateCertificateResponseTypeDef",
    "AttributeDetailsTypeDef",
    "AttributeTypeDef",
    "BlobTypeDef",
    "CertificateAssociationStatusReasonTypeDef",
    "CertificateAssociationStatusTypeDef",
    "CertificateAssociationTypeDef",
    "ConfigurationArchiveTypeDef",
    "ConfigurationFileTypeDef",
    "ConfigurationMetadataTypeDef",
    "CreateProxyRequestTypeDef",
    "CreateProxyResponseTypeDef",
    "DeleteProxyRequestTypeDef",
    "DeleteProxyResponseTypeDef",
    "DisassociateCertificateRequestTypeDef",
    "DisassociateCertificateResponseTypeDef",
    "GetProxyAttributesRequestTypeDef",
    "GetProxyAttributesResponseTypeDef",
    "GetProxyConfigurationContentsRequestTypeDef",
    "GetProxyConfigurationContentsResponseTypeDef",
    "GetProxyRequestTypeDef",
    "GetProxyRequestWaitExtraTypeDef",
    "GetProxyRequestWaitTypeDef",
    "GetProxyResponseTypeDef",
    "GetProxyUpdateRequestTypeDef",
    "GetProxyUpdateRequestWaitTypeDef",
    "GetProxyUpdateResponseTypeDef",
    "ListCertificateAssociationsRequestPaginateTypeDef",
    "ListCertificateAssociationsRequestTypeDef",
    "ListCertificateAssociationsResponseTypeDef",
    "ListProxiesRequestPaginateTypeDef",
    "ListProxiesRequestTypeDef",
    "ListProxiesResponseTypeDef",
    "ListProxyUpdatesRequestPaginateTypeDef",
    "ListProxyUpdatesRequestTypeDef",
    "ListProxyUpdatesResponseTypeDef",
    "ListProxyVersionsRequestPaginateTypeDef",
    "ListProxyVersionsRequestTypeDef",
    "ListProxyVersionsResponseTypeDef",
    "ListTagsForResourceInputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "PaginatorConfigTypeDef",
    "ProxyConfigurationTypeDef",
    "ProxyConfigurationUpdateDetailsTypeDef",
    "ProxyIpAddressingConfigurationTypeDef",
    "ProxyIpConfigurationTypeDef",
    "ProxyNetworkConfigurationTypeDef",
    "ProxyNetworkUserConfigurationTypeDef",
    "ProxyStatusReasonTypeDef",
    "ProxyStatusTypeDef",
    "ProxySummaryTypeDef",
    "ProxyUpdateDetailsTypeDef",
    "ProxyUpdateStateTypeDef",
    "ProxyUpdateSummaryTypeDef",
    "ProxyVersionSummaryTypeDef",
    "ProxyVpcConfigurationTypeDef",
    "ProxyVpcUserConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "SecurityGroupDetailsTypeDef",
    "SubnetAndZoneTypeDef",
    "SubnetDetailsTypeDef",
    "TagResourceInputTypeDef",
    "UntagResourceInputTypeDef",
    "UpdateProxyAttributesRequestTypeDef",
    "UpdateProxyAttributesResponseTypeDef",
    "UpdateProxyConfigurationRequestTypeDef",
    "UpdateProxyConfigurationResponseTypeDef",
    "UpdateProxyNetworkConfigurationRequestTypeDef",
    "UpdateProxyNetworkConfigurationResponseTypeDef",
    "UpdateProxyVpcConfigurationTypeDef",
    "WaiterConfigTypeDef",
)

class AssociateCertificateRequestTypeDef(TypedDict):
    proxyIdentifier: str
    certificateIdentifier: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class AttributeDetailsTypeDef(TypedDict):
    key: str
    value: str
    defaultValue: NotRequired[str]

class AttributeTypeDef(TypedDict):
    key: str
    value: str

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class CertificateAssociationStatusReasonTypeDef(TypedDict):
    code: str
    message: NotRequired[str]

class ConfigurationMetadataTypeDef(TypedDict):
    configFileHash: NotRequired[str]
    configArchiveHash: NotRequired[str]
    configFileLastUpdatedAt: NotRequired[datetime]
    configArchiveLastUpdatedAt: NotRequired[datetime]

class DeleteProxyRequestTypeDef(TypedDict):
    proxyIdentifier: str

class DisassociateCertificateRequestTypeDef(TypedDict):
    proxyIdentifier: str
    certificateIdentifier: str

class GetProxyAttributesRequestTypeDef(TypedDict):
    proxyIdentifier: str

class GetProxyConfigurationContentsRequestTypeDef(TypedDict):
    proxyIdentifier: str
    includeConfigFile: NotRequired[bool]
    includeConfigArchive: NotRequired[bool]

class GetProxyRequestTypeDef(TypedDict):
    proxyIdentifier: str

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class GetProxyUpdateRequestTypeDef(TypedDict):
    proxyIdentifier: str
    updateIdentifier: str

class ProxyUpdateStateTypeDef(TypedDict):
    validationStatus: ProxyUpdateValidationStatusType
    propagationStatus: ProxyUpdatePropagationStatusType
    reasons: NotRequired[list[str]]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListCertificateAssociationsRequestTypeDef(TypedDict):
    proxyIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListProxiesRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListProxyUpdatesRequestTypeDef(TypedDict):
    proxyIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

ProxyUpdateSummaryTypeDef = TypedDict(
    "ProxyUpdateSummaryTypeDef",
    {
        "updateId": str,
        "type": Literal["update-proxy-configuration"],
        "validationStatus": ProxyUpdateValidationStatusType,
        "propagationStatus": ProxyUpdatePropagationStatusType,
        "submittedAt": datetime,
        "validatedAt": NotRequired[datetime],
        "completedAt": NotRequired[datetime],
    },
)
ListProxyVersionsRequestTypeDef = TypedDict(
    "ListProxyVersionsRequestTypeDef",
    {
        "type": Literal["envoy"],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ProxyVersionSummaryTypeDef = TypedDict(
    "ProxyVersionSummaryTypeDef",
    {
        "type": Literal["envoy"],
        "version": str,
    },
)

class ListTagsForResourceInputTypeDef(TypedDict):
    resourceArn: str

class ProxyIpAddressingConfigurationTypeDef(TypedDict):
    ipv4Addressability: ProxyIpv4AddressabilityType
    ipv6Addressability: ProxyIpv6AddressabilityType

class ProxyStatusReasonTypeDef(TypedDict):
    code: str
    target: NotRequired[str]
    message: NotRequired[str]

class SecurityGroupDetailsTypeDef(TypedDict):
    securityGroupId: str

class SubnetAndZoneTypeDef(TypedDict):
    subnetId: str
    zoneId: str
    zoneName: NotRequired[str]

class SubnetDetailsTypeDef(TypedDict):
    subnetId: str

class TagResourceInputTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceInputTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class ListTagsForResourceOutputTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetProxyAttributesResponseTypeDef(TypedDict):
    attributes: list[AttributeDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateProxyAttributesResponseTypeDef(TypedDict):
    attributes: list[AttributeDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateProxyAttributesRequestTypeDef(TypedDict):
    proxyIdentifier: str
    attributes: Sequence[AttributeTypeDef]

class ConfigurationArchiveTypeDef(TypedDict):
    configurationBytes: BlobTypeDef

class ConfigurationFileTypeDef(TypedDict):
    configurationBytes: BlobTypeDef

class CertificateAssociationStatusTypeDef(TypedDict):
    code: CertificateAssociationStatusCodeType
    reasons: list[CertificateAssociationStatusReasonTypeDef]

class GetProxyConfigurationContentsResponseTypeDef(TypedDict):
    configurationFileContents: bytes
    configurationArchiveContents: bytes
    configurationMetadata: ConfigurationMetadataTypeDef
    customerKmsKeyArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class ProxyConfigurationUpdateDetailsTypeDef(TypedDict):
    newConfigurationMetadata: NotRequired[ConfigurationMetadataTypeDef]

class UpdateProxyConfigurationResponseTypeDef(TypedDict):
    configurationMetadata: ConfigurationMetadataTypeDef
    updateId: str
    customerKmsKeyArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetProxyRequestWaitExtraTypeDef(TypedDict):
    proxyIdentifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetProxyRequestWaitTypeDef(TypedDict):
    proxyIdentifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetProxyUpdateRequestWaitTypeDef(TypedDict):
    proxyIdentifier: str
    updateIdentifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class ListCertificateAssociationsRequestPaginateTypeDef(TypedDict):
    proxyIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProxiesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProxyUpdatesRequestPaginateTypeDef(TypedDict):
    proxyIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListProxyVersionsRequestPaginateTypeDef = TypedDict(
    "ListProxyVersionsRequestPaginateTypeDef",
    {
        "type": Literal["envoy"],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListProxyUpdatesResponseTypeDef(TypedDict):
    items: list[ProxyUpdateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListProxyVersionsResponseTypeDef(TypedDict):
    items: list[ProxyVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ProxyIpConfigurationTypeDef(TypedDict):
    ipAddressingConfiguration: ProxyIpAddressingConfigurationTypeDef

class ProxyStatusTypeDef(TypedDict):
    code: ProxyStatusCodeType
    reasons: list[ProxyStatusReasonTypeDef]

class ProxyVpcConfigurationTypeDef(TypedDict):
    availabilityZones: list[SubnetAndZoneTypeDef]
    securityGroups: list[SecurityGroupDetailsTypeDef]
    vpcId: NotRequired[str]

class ProxyVpcUserConfigurationTypeDef(TypedDict):
    subnets: Sequence[SubnetDetailsTypeDef]
    securityGroups: Sequence[SecurityGroupDetailsTypeDef]

class UpdateProxyVpcConfigurationTypeDef(TypedDict):
    subnets: NotRequired[Sequence[SubnetDetailsTypeDef]]
    securityGroups: NotRequired[Sequence[SecurityGroupDetailsTypeDef]]

class ProxyConfigurationTypeDef(TypedDict):
    configurationFile: NotRequired[ConfigurationFileTypeDef]
    configurationArchive: NotRequired[ConfigurationArchiveTypeDef]

class UpdateProxyConfigurationRequestTypeDef(TypedDict):
    proxyIdentifier: str
    configurationFile: NotRequired[ConfigurationFileTypeDef]
    configurationArchive: NotRequired[ConfigurationArchiveTypeDef]
    resetConfigurationArchive: NotRequired[bool]
    customerKmsKeyArn: NotRequired[str]
    resetCustomerKmsKeyArn: NotRequired[bool]

class CertificateAssociationTypeDef(TypedDict):
    certificateArn: str
    status: CertificateAssociationStatusTypeDef
    createdAt: NotRequired[datetime]

class ProxyUpdateDetailsTypeDef(TypedDict):
    configuration: NotRequired[ProxyConfigurationUpdateDetailsTypeDef]

class DeleteProxyResponseTypeDef(TypedDict):
    arn: str
    name: str
    status: ProxyStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

ProxySummaryTypeDef = TypedDict(
    "ProxySummaryTypeDef",
    {
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "type": NotRequired[Literal["envoy"]],
        "dnsName": NotRequired[str],
        "vpcId": NotRequired[str],
        "status": NotRequired[ProxyStatusTypeDef],
        "createdAt": NotRequired[datetime],
    },
)

class ProxyNetworkConfigurationTypeDef(TypedDict):
    ipConfiguration: ProxyIpConfigurationTypeDef
    vpcConfiguration: ProxyVpcConfigurationTypeDef

class ProxyNetworkUserConfigurationTypeDef(TypedDict):
    ipConfiguration: ProxyIpConfigurationTypeDef
    vpcConfiguration: ProxyVpcUserConfigurationTypeDef

class UpdateProxyNetworkConfigurationRequestTypeDef(TypedDict):
    proxyIdentifier: str
    vpcConfiguration: UpdateProxyVpcConfigurationTypeDef

class AssociateCertificateResponseTypeDef(TypedDict):
    certificateAssociation: CertificateAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DisassociateCertificateResponseTypeDef(TypedDict):
    certificateAssociation: CertificateAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListCertificateAssociationsResponseTypeDef(TypedDict):
    items: list[CertificateAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetProxyUpdateResponseTypeDef(TypedDict):
    proxyArn: str
    updateId: str
    state: ProxyUpdateStateTypeDef
    details: ProxyUpdateDetailsTypeDef
    submittedAt: datetime
    validatedAt: datetime
    completedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ListProxiesResponseTypeDef(TypedDict):
    items: list[ProxySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

CreateProxyResponseTypeDef = TypedDict(
    "CreateProxyResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "type": Literal["envoy"],
        "proxyVersion": str,
        "dnsName": str,
        "roleArn": str,
        "networkConfiguration": ProxyNetworkConfigurationTypeDef,
        "status": ProxyStatusTypeDef,
        "configurationMetadata": ConfigurationMetadataTypeDef,
        "createdAt": datetime,
        "customerKmsKeyArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetProxyResponseTypeDef = TypedDict(
    "GetProxyResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "type": Literal["envoy"],
        "proxyVersion": str,
        "dnsName": str,
        "roleArn": str,
        "networkConfiguration": ProxyNetworkConfigurationTypeDef,
        "status": ProxyStatusTypeDef,
        "configurationMetadata": ConfigurationMetadataTypeDef,
        "createdAt": datetime,
        "customerKmsKeyArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateProxyNetworkConfigurationResponseTypeDef = TypedDict(
    "UpdateProxyNetworkConfigurationResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "type": Literal["envoy"],
        "proxyVersion": str,
        "dnsName": str,
        "roleArn": str,
        "networkConfiguration": ProxyNetworkConfigurationTypeDef,
        "status": ProxyStatusTypeDef,
        "configurationMetadata": ConfigurationMetadataTypeDef,
        "createdAt": datetime,
        "customerKmsKeyArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateProxyRequestTypeDef = TypedDict(
    "CreateProxyRequestTypeDef",
    {
        "name": str,
        "type": Literal["envoy"],
        "proxyVersion": str,
        "roleArn": str,
        "configuration": ProxyConfigurationTypeDef,
        "networkConfiguration": ProxyNetworkUserConfigurationTypeDef,
        "attributes": NotRequired[Sequence[AttributeTypeDef]],
        "customerKmsKeyArn": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
        "clientToken": NotRequired[str],
    },
)
