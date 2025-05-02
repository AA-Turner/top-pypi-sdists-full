"""
Type annotations for worklink service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_worklink/type_defs/)

Usage::

    ```python
    from types_aiobotocore_worklink.type_defs import AssociateDomainRequestRequestTypeDef

    data: AssociateDomainRequestRequestTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import DeviceStatusType, DomainStatusType, FleetStatusType

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AssociateDomainRequestRequestTypeDef",
    "AssociateWebsiteAuthorizationProviderRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "AssociateWebsiteCertificateAuthorityRequestRequestTypeDef",
    "CreateFleetRequestRequestTypeDef",
    "DeleteFleetRequestRequestTypeDef",
    "DescribeAuditStreamConfigurationRequestRequestTypeDef",
    "DescribeCompanyNetworkConfigurationRequestRequestTypeDef",
    "DescribeDevicePolicyConfigurationRequestRequestTypeDef",
    "DescribeDeviceRequestRequestTypeDef",
    "DescribeDomainRequestRequestTypeDef",
    "DescribeFleetMetadataRequestRequestTypeDef",
    "DescribeIdentityProviderConfigurationRequestRequestTypeDef",
    "DescribeWebsiteCertificateAuthorityRequestRequestTypeDef",
    "DeviceSummaryTypeDef",
    "DisassociateDomainRequestRequestTypeDef",
    "DisassociateWebsiteAuthorizationProviderRequestRequestTypeDef",
    "DisassociateWebsiteCertificateAuthorityRequestRequestTypeDef",
    "DomainSummaryTypeDef",
    "FleetSummaryTypeDef",
    "ListDevicesRequestRequestTypeDef",
    "ListDomainsRequestRequestTypeDef",
    "ListFleetsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListWebsiteAuthorizationProvidersRequestRequestTypeDef",
    "WebsiteAuthorizationProviderSummaryTypeDef",
    "ListWebsiteCertificateAuthoritiesRequestRequestTypeDef",
    "WebsiteCaSummaryTypeDef",
    "RestoreDomainAccessRequestRequestTypeDef",
    "RevokeDomainAccessRequestRequestTypeDef",
    "SignOutUserRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAuditStreamConfigurationRequestRequestTypeDef",
    "UpdateCompanyNetworkConfigurationRequestRequestTypeDef",
    "UpdateDevicePolicyConfigurationRequestRequestTypeDef",
    "UpdateDomainMetadataRequestRequestTypeDef",
    "UpdateFleetMetadataRequestRequestTypeDef",
    "UpdateIdentityProviderConfigurationRequestRequestTypeDef",
    "AssociateWebsiteAuthorizationProviderResponseTypeDef",
    "AssociateWebsiteCertificateAuthorityResponseTypeDef",
    "CreateFleetResponseTypeDef",
    "DescribeAuditStreamConfigurationResponseTypeDef",
    "DescribeCompanyNetworkConfigurationResponseTypeDef",
    "DescribeDevicePolicyConfigurationResponseTypeDef",
    "DescribeDeviceResponseTypeDef",
    "DescribeDomainResponseTypeDef",
    "DescribeFleetMetadataResponseTypeDef",
    "DescribeIdentityProviderConfigurationResponseTypeDef",
    "DescribeWebsiteCertificateAuthorityResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListDevicesResponseTypeDef",
    "ListDomainsResponseTypeDef",
    "ListFleetsResponseTypeDef",
    "ListWebsiteAuthorizationProvidersResponseTypeDef",
    "ListWebsiteCertificateAuthoritiesResponseTypeDef",
)

AssociateDomainRequestRequestTypeDef = TypedDict(
    "AssociateDomainRequestRequestTypeDef",
    {
        "FleetArn": str,
        "DomainName": str,
        "AcmCertificateArn": str,
        "DisplayName": NotRequired[str],
    },
)
AssociateWebsiteAuthorizationProviderRequestRequestTypeDef = TypedDict(
    "AssociateWebsiteAuthorizationProviderRequestRequestTypeDef",
    {
        "FleetArn": str,
        "AuthorizationProviderType": Literal["SAML"],
        "DomainName": NotRequired[str],
    },
)
ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
        "HostId": NotRequired[str],
    },
)
AssociateWebsiteCertificateAuthorityRequestRequestTypeDef = TypedDict(
    "AssociateWebsiteCertificateAuthorityRequestRequestTypeDef",
    {
        "FleetArn": str,
        "Certificate": str,
        "DisplayName": NotRequired[str],
    },
)
CreateFleetRequestRequestTypeDef = TypedDict(
    "CreateFleetRequestRequestTypeDef",
    {
        "FleetName": str,
        "DisplayName": NotRequired[str],
        "OptimizeForEndUserLocation": NotRequired[bool],
        "Tags": NotRequired[Mapping[str, str]],
    },
)
DeleteFleetRequestRequestTypeDef = TypedDict(
    "DeleteFleetRequestRequestTypeDef",
    {
        "FleetArn": str,
    },
)
DescribeAuditStreamConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeAuditStreamConfigurationRequestRequestTypeDef",
    {
        "FleetArn": str,
    },
)
DescribeCompanyNetworkConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeCompanyNetworkConfigurationRequestRequestTypeDef",
    {
        "FleetArn": str,
    },
)
DescribeDevicePolicyConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeDevicePolicyConfigurationRequestRequestTypeDef",
    {
        "FleetArn": str,
    },
)
DescribeDeviceRequestRequestTypeDef = TypedDict(
    "DescribeDeviceRequestRequestTypeDef",
    {
        "FleetArn": str,
        "DeviceId": str,
    },
)
DescribeDomainRequestRequestTypeDef = TypedDict(
    "DescribeDomainRequestRequestTypeDef",
    {
        "FleetArn": str,
        "DomainName": str,
    },
)
DescribeFleetMetadataRequestRequestTypeDef = TypedDict(
    "DescribeFleetMetadataRequestRequestTypeDef",
    {
        "FleetArn": str,
    },
)
DescribeIdentityProviderConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeIdentityProviderConfigurationRequestRequestTypeDef",
    {
        "FleetArn": str,
    },
)
DescribeWebsiteCertificateAuthorityRequestRequestTypeDef = TypedDict(
    "DescribeWebsiteCertificateAuthorityRequestRequestTypeDef",
    {
        "FleetArn": str,
        "WebsiteCaId": str,
    },
)
DeviceSummaryTypeDef = TypedDict(
    "DeviceSummaryTypeDef",
    {
        "DeviceId": NotRequired[str],
        "DeviceStatus": NotRequired[DeviceStatusType],
    },
)
DisassociateDomainRequestRequestTypeDef = TypedDict(
    "DisassociateDomainRequestRequestTypeDef",
    {
        "FleetArn": str,
        "DomainName": str,
    },
)
DisassociateWebsiteAuthorizationProviderRequestRequestTypeDef = TypedDict(
    "DisassociateWebsiteAuthorizationProviderRequestRequestTypeDef",
    {
        "FleetArn": str,
        "AuthorizationProviderId": str,
    },
)
DisassociateWebsiteCertificateAuthorityRequestRequestTypeDef = TypedDict(
    "DisassociateWebsiteCertificateAuthorityRequestRequestTypeDef",
    {
        "FleetArn": str,
        "WebsiteCaId": str,
    },
)
DomainSummaryTypeDef = TypedDict(
    "DomainSummaryTypeDef",
    {
        "DomainName": str,
        "CreatedTime": datetime,
        "DomainStatus": DomainStatusType,
        "DisplayName": NotRequired[str],
    },
)
FleetSummaryTypeDef = TypedDict(
    "FleetSummaryTypeDef",
    {
        "FleetArn": NotRequired[str],
        "CreatedTime": NotRequired[datetime],
        "LastUpdatedTime": NotRequired[datetime],
        "FleetName": NotRequired[str],
        "DisplayName": NotRequired[str],
        "CompanyCode": NotRequired[str],
        "FleetStatus": NotRequired[FleetStatusType],
        "Tags": NotRequired[Dict[str, str]],
    },
)
ListDevicesRequestRequestTypeDef = TypedDict(
    "ListDevicesRequestRequestTypeDef",
    {
        "FleetArn": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
ListDomainsRequestRequestTypeDef = TypedDict(
    "ListDomainsRequestRequestTypeDef",
    {
        "FleetArn": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
ListFleetsRequestRequestTypeDef = TypedDict(
    "ListFleetsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)
ListWebsiteAuthorizationProvidersRequestRequestTypeDef = TypedDict(
    "ListWebsiteAuthorizationProvidersRequestRequestTypeDef",
    {
        "FleetArn": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
WebsiteAuthorizationProviderSummaryTypeDef = TypedDict(
    "WebsiteAuthorizationProviderSummaryTypeDef",
    {
        "AuthorizationProviderType": Literal["SAML"],
        "AuthorizationProviderId": NotRequired[str],
        "DomainName": NotRequired[str],
        "CreatedTime": NotRequired[datetime],
    },
)
ListWebsiteCertificateAuthoritiesRequestRequestTypeDef = TypedDict(
    "ListWebsiteCertificateAuthoritiesRequestRequestTypeDef",
    {
        "FleetArn": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
WebsiteCaSummaryTypeDef = TypedDict(
    "WebsiteCaSummaryTypeDef",
    {
        "WebsiteCaId": NotRequired[str],
        "CreatedTime": NotRequired[datetime],
        "DisplayName": NotRequired[str],
    },
)
RestoreDomainAccessRequestRequestTypeDef = TypedDict(
    "RestoreDomainAccessRequestRequestTypeDef",
    {
        "FleetArn": str,
        "DomainName": str,
    },
)
RevokeDomainAccessRequestRequestTypeDef = TypedDict(
    "RevokeDomainAccessRequestRequestTypeDef",
    {
        "FleetArn": str,
        "DomainName": str,
    },
)
SignOutUserRequestRequestTypeDef = TypedDict(
    "SignOutUserRequestRequestTypeDef",
    {
        "FleetArn": str,
        "Username": str,
    },
)
TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)
UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)
UpdateAuditStreamConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateAuditStreamConfigurationRequestRequestTypeDef",
    {
        "FleetArn": str,
        "AuditStreamArn": NotRequired[str],
    },
)
UpdateCompanyNetworkConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateCompanyNetworkConfigurationRequestRequestTypeDef",
    {
        "FleetArn": str,
        "VpcId": str,
        "SubnetIds": Sequence[str],
        "SecurityGroupIds": Sequence[str],
    },
)
UpdateDevicePolicyConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateDevicePolicyConfigurationRequestRequestTypeDef",
    {
        "FleetArn": str,
        "DeviceCaCertificate": NotRequired[str],
    },
)
UpdateDomainMetadataRequestRequestTypeDef = TypedDict(
    "UpdateDomainMetadataRequestRequestTypeDef",
    {
        "FleetArn": str,
        "DomainName": str,
        "DisplayName": NotRequired[str],
    },
)
UpdateFleetMetadataRequestRequestTypeDef = TypedDict(
    "UpdateFleetMetadataRequestRequestTypeDef",
    {
        "FleetArn": str,
        "DisplayName": NotRequired[str],
        "OptimizeForEndUserLocation": NotRequired[bool],
    },
)
UpdateIdentityProviderConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateIdentityProviderConfigurationRequestRequestTypeDef",
    {
        "FleetArn": str,
        "IdentityProviderType": Literal["SAML"],
        "IdentityProviderSamlMetadata": NotRequired[str],
    },
)
AssociateWebsiteAuthorizationProviderResponseTypeDef = TypedDict(
    "AssociateWebsiteAuthorizationProviderResponseTypeDef",
    {
        "AuthorizationProviderId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
AssociateWebsiteCertificateAuthorityResponseTypeDef = TypedDict(
    "AssociateWebsiteCertificateAuthorityResponseTypeDef",
    {
        "WebsiteCaId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateFleetResponseTypeDef = TypedDict(
    "CreateFleetResponseTypeDef",
    {
        "FleetArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeAuditStreamConfigurationResponseTypeDef = TypedDict(
    "DescribeAuditStreamConfigurationResponseTypeDef",
    {
        "AuditStreamArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeCompanyNetworkConfigurationResponseTypeDef = TypedDict(
    "DescribeCompanyNetworkConfigurationResponseTypeDef",
    {
        "VpcId": str,
        "SubnetIds": List[str],
        "SecurityGroupIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeDevicePolicyConfigurationResponseTypeDef = TypedDict(
    "DescribeDevicePolicyConfigurationResponseTypeDef",
    {
        "DeviceCaCertificate": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeDeviceResponseTypeDef = TypedDict(
    "DescribeDeviceResponseTypeDef",
    {
        "Status": DeviceStatusType,
        "Model": str,
        "Manufacturer": str,
        "OperatingSystem": str,
        "OperatingSystemVersion": str,
        "PatchLevel": str,
        "FirstAccessedTime": datetime,
        "LastAccessedTime": datetime,
        "Username": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeDomainResponseTypeDef = TypedDict(
    "DescribeDomainResponseTypeDef",
    {
        "DomainName": str,
        "DisplayName": str,
        "CreatedTime": datetime,
        "DomainStatus": DomainStatusType,
        "AcmCertificateArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeFleetMetadataResponseTypeDef = TypedDict(
    "DescribeFleetMetadataResponseTypeDef",
    {
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "FleetName": str,
        "DisplayName": str,
        "OptimizeForEndUserLocation": bool,
        "CompanyCode": str,
        "FleetStatus": FleetStatusType,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeIdentityProviderConfigurationResponseTypeDef = TypedDict(
    "DescribeIdentityProviderConfigurationResponseTypeDef",
    {
        "IdentityProviderType": Literal["SAML"],
        "ServiceProviderSamlMetadata": str,
        "IdentityProviderSamlMetadata": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeWebsiteCertificateAuthorityResponseTypeDef = TypedDict(
    "DescribeWebsiteCertificateAuthorityResponseTypeDef",
    {
        "Certificate": str,
        "CreatedTime": datetime,
        "DisplayName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListDevicesResponseTypeDef = TypedDict(
    "ListDevicesResponseTypeDef",
    {
        "Devices": List[DeviceSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ListDomainsResponseTypeDef = TypedDict(
    "ListDomainsResponseTypeDef",
    {
        "Domains": List[DomainSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ListFleetsResponseTypeDef = TypedDict(
    "ListFleetsResponseTypeDef",
    {
        "FleetSummaryList": List[FleetSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ListWebsiteAuthorizationProvidersResponseTypeDef = TypedDict(
    "ListWebsiteAuthorizationProvidersResponseTypeDef",
    {
        "WebsiteAuthorizationProviders": List[WebsiteAuthorizationProviderSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ListWebsiteCertificateAuthoritiesResponseTypeDef = TypedDict(
    "ListWebsiteCertificateAuthoritiesResponseTypeDef",
    {
        "WebsiteCertificateAuthorities": List[WebsiteCaSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
