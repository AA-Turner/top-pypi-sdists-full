"""
Type annotations for acm service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_acm.type_defs import AcmCertificateMetadataFilterTypeDef

    data: AcmCertificateMetadataFilterTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import IO, Any, Union

from botocore.response import StreamingBody

from .literals import (
    AcmeAccountStatusType,
    AcmeContactType,
    AcmeDomainValidationFailureReasonType,
    AcmeDomainValidationStatusType,
    AcmeEndpointStatusType,
    CertificateExportType,
    CertificateKeyPairOriginType,
    CertificateStatusType,
    CertificateTransparencyLoggingPreferenceType,
    CertificateTypeType,
    ComparisonOperatorType,
    DomainScopeOptionType,
    DomainStatusType,
    ExtendedKeyUsageNameType,
    FailureReasonType,
    KeyAlgorithmType,
    KeyUsageNameType,
    PublicKeyAlgorithmType,
    RenewalEligibilityType,
    RenewalStatusType,
    RevocationReasonType,
    SearchCertificatesSortByType,
    SearchCertificatesSortOrderType,
    SortOrderType,
    TimeTypeType,
    ValidationMethodType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AcmCertificateMetadataFilterTypeDef",
    "AcmCertificateMetadataTypeDef",
    "AcmeAccountSummaryTypeDef",
    "AcmeAccountTypeDef",
    "AcmeDomainValidationSummaryTypeDef",
    "AcmeDomainValidationTypeDef",
    "AcmeEndpointSummaryTypeDef",
    "AcmeEndpointTypeDef",
    "AcmeExternalAccountBindingSummaryTypeDef",
    "AcmeExternalAccountBindingTypeDef",
    "AddTagsToCertificateRequestTypeDef",
    "BlobTypeDef",
    "CertificateAuthorityOutputTypeDef",
    "CertificateAuthorityTypeDef",
    "CertificateAuthorityUnionTypeDef",
    "CertificateDetailTypeDef",
    "CertificateFilterStatementPaginatorTypeDef",
    "CertificateFilterStatementTypeDef",
    "CertificateFilterTypeDef",
    "CertificateMetadataTypeDef",
    "CertificateOptionsTypeDef",
    "CertificateSearchResultTypeDef",
    "CertificateSummaryTypeDef",
    "CommonNameFilterTypeDef",
    "CreateAcmeDomainValidationRequestTypeDef",
    "CreateAcmeDomainValidationResponseTypeDef",
    "CreateAcmeEndpointRequestTypeDef",
    "CreateAcmeEndpointResponseTypeDef",
    "CreateAcmeExternalAccountBindingRequestTypeDef",
    "CreateAcmeExternalAccountBindingResponseTypeDef",
    "CustomAttributeTypeDef",
    "DeleteAcmeDomainValidationRequestTypeDef",
    "DeleteAcmeEndpointRequestTypeDef",
    "DeleteAcmeExternalAccountBindingRequestTypeDef",
    "DeleteCertificateRequestTypeDef",
    "DescribeAcmeAccountRequestTypeDef",
    "DescribeAcmeAccountResponseTypeDef",
    "DescribeAcmeDomainValidationRequestTypeDef",
    "DescribeAcmeDomainValidationRequestWaitExtraTypeDef",
    "DescribeAcmeDomainValidationRequestWaitTypeDef",
    "DescribeAcmeDomainValidationResponseTypeDef",
    "DescribeAcmeEndpointRequestTypeDef",
    "DescribeAcmeEndpointRequestWaitExtraTypeDef",
    "DescribeAcmeEndpointRequestWaitTypeDef",
    "DescribeAcmeEndpointResponseTypeDef",
    "DescribeAcmeExternalAccountBindingRequestTypeDef",
    "DescribeAcmeExternalAccountBindingResponseTypeDef",
    "DescribeCertificateRequestTypeDef",
    "DescribeCertificateRequestWaitTypeDef",
    "DescribeCertificateResponseTypeDef",
    "DistinguishedNameTypeDef",
    "DnsNameFilterTypeDef",
    "DnsPrevalidationDetailsTypeDef",
    "DnsPrevalidationOptionsTypeDef",
    "DomainScopeTypeDef",
    "DomainValidationOptionTypeDef",
    "DomainValidationTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ExpirationTypeDef",
    "ExpiryEventsConfigurationTypeDef",
    "ExportCertificateRequestTypeDef",
    "ExportCertificateResponseTypeDef",
    "ExtendedKeyUsageTypeDef",
    "FailureDetailsTypeDef",
    "FiltersTypeDef",
    "GeneralNameTypeDef",
    "GetAccountConfigurationResponseTypeDef",
    "GetAcmeExternalAccountBindingCredentialsRequestTypeDef",
    "GetAcmeExternalAccountBindingCredentialsResponseTypeDef",
    "GetCertificateRequestTypeDef",
    "GetCertificateResponseTypeDef",
    "HttpRedirectTypeDef",
    "ImportCertificateRequestTypeDef",
    "ImportCertificateResponseTypeDef",
    "KeyUsageTypeDef",
    "ListAcmeAccountsRequestPaginateTypeDef",
    "ListAcmeAccountsRequestTypeDef",
    "ListAcmeAccountsResponseTypeDef",
    "ListAcmeDomainValidationsRequestPaginateTypeDef",
    "ListAcmeDomainValidationsRequestTypeDef",
    "ListAcmeDomainValidationsResponseTypeDef",
    "ListAcmeEndpointsRequestPaginateTypeDef",
    "ListAcmeEndpointsRequestTypeDef",
    "ListAcmeEndpointsResponseTypeDef",
    "ListAcmeExternalAccountBindingsRequestPaginateTypeDef",
    "ListAcmeExternalAccountBindingsRequestTypeDef",
    "ListAcmeExternalAccountBindingsResponseTypeDef",
    "ListCertificatesRequestPaginateTypeDef",
    "ListCertificatesRequestTypeDef",
    "ListCertificatesResponseTypeDef",
    "ListTagsForCertificateRequestTypeDef",
    "ListTagsForCertificateResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "OtherNameTypeDef",
    "PaginatorConfigTypeDef",
    "PrevalidationDetailsTypeDef",
    "PrevalidationOptionsTypeDef",
    "PublicCertificateAuthorityOutputTypeDef",
    "PublicCertificateAuthorityTypeDef",
    "PutAccountConfigurationRequestTypeDef",
    "RemoveTagsFromCertificateRequestTypeDef",
    "RenewCertificateRequestTypeDef",
    "RenewalSummaryTypeDef",
    "RequestCertificateRequestTypeDef",
    "RequestCertificateResponseTypeDef",
    "ResendValidationEmailRequestTypeDef",
    "ResourceRecordTypeDef",
    "ResponseMetadataTypeDef",
    "RevokeAcmeAccountRequestTypeDef",
    "RevokeAcmeExternalAccountBindingRequestTypeDef",
    "RevokeCertificateRequestTypeDef",
    "RevokeCertificateResponseTypeDef",
    "SearchCertificatesRequestPaginateTypeDef",
    "SearchCertificatesRequestTypeDef",
    "SearchCertificatesResponseTypeDef",
    "SubjectAlternativeNameFilterTypeDef",
    "SubjectFilterTypeDef",
    "TagResourceRequestTypeDef",
    "TagTypeDef",
    "TimestampRangeTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateAcmeDomainValidationRequestTypeDef",
    "UpdateAcmeEndpointRequestTypeDef",
    "UpdateCertificateOptionsRequestTypeDef",
    "WaiterConfigTypeDef",
    "X509AttributeFilterTypeDef",
    "X509AttributesTypeDef",
)

AcmCertificateMetadataFilterTypeDef = TypedDict(
    "AcmCertificateMetadataFilterTypeDef",
    {
        "Status": NotRequired[CertificateStatusType],
        "RenewalStatus": NotRequired[RenewalStatusType],
        "Type": NotRequired[CertificateTypeType],
        "InUse": NotRequired[bool],
        "Exported": NotRequired[bool],
        "ExportOption": NotRequired[CertificateExportType],
        "ManagedBy": NotRequired[Literal["CLOUDFRONT"]],
        "ValidationMethod": NotRequired[ValidationMethodType],
        "CertificateKeyPairOrigin": NotRequired[CertificateKeyPairOriginType],
        "AcmeEndpointArn": NotRequired[str],
        "AcmeAccountId": NotRequired[str],
    },
)
AcmCertificateMetadataTypeDef = TypedDict(
    "AcmCertificateMetadataTypeDef",
    {
        "CreatedAt": NotRequired[datetime],
        "Exported": NotRequired[bool],
        "ImportedAt": NotRequired[datetime],
        "InUse": NotRequired[bool],
        "IssuedAt": NotRequired[datetime],
        "RenewalEligibility": NotRequired[RenewalEligibilityType],
        "RevokedAt": NotRequired[datetime],
        "Status": NotRequired[CertificateStatusType],
        "RenewalStatus": NotRequired[RenewalStatusType],
        "Type": NotRequired[CertificateTypeType],
        "ExportOption": NotRequired[CertificateExportType],
        "ManagedBy": NotRequired[Literal["CLOUDFRONT"]],
        "ValidationMethod": NotRequired[ValidationMethodType],
        "CertificateKeyPairOrigin": NotRequired[CertificateKeyPairOriginType],
        "AcmeEndpointArn": NotRequired[str],
        "AcmeAccountId": NotRequired[str],
    },
)

class AcmeAccountSummaryTypeDef(TypedDict):
    AccountUrl: NotRequired[str]
    PublicKeyThumbprint: NotRequired[str]
    Status: NotRequired[AcmeAccountStatusType]
    CreatedAt: NotRequired[datetime]
    AcmeExternalAccountBindingArn: NotRequired[str]
    Contacts: NotRequired[list[str]]

class AcmeAccountTypeDef(TypedDict):
    AccountUrl: NotRequired[str]
    PublicKeyThumbprint: NotRequired[str]
    Status: NotRequired[AcmeAccountStatusType]
    CreatedAt: NotRequired[datetime]
    AcmeExternalAccountBindingArn: NotRequired[str]
    Contacts: NotRequired[list[str]]

class FailureDetailsTypeDef(TypedDict):
    Reason: NotRequired[AcmeDomainValidationFailureReasonType]
    Message: NotRequired[str]

class TagTypeDef(TypedDict):
    Key: str
    Value: NotRequired[str]

class AcmeExternalAccountBindingSummaryTypeDef(TypedDict):
    AcmeExternalAccountBindingArn: NotRequired[str]
    AcmeEndpointArn: NotRequired[str]
    RoleArn: NotRequired[str]
    ExpiresAt: NotRequired[datetime]
    RevokedAt: NotRequired[datetime]
    LastUsedAt: NotRequired[datetime]
    CreatedAt: NotRequired[datetime]
    UpdatedAt: NotRequired[datetime]

class AcmeExternalAccountBindingTypeDef(TypedDict):
    AcmeExternalAccountBindingArn: NotRequired[str]
    AcmeEndpointArn: NotRequired[str]
    RoleArn: NotRequired[str]
    ExpiresAt: NotRequired[datetime]
    RevokedAt: NotRequired[datetime]
    LastUsedAt: NotRequired[datetime]
    CreatedAt: NotRequired[datetime]
    UpdatedAt: NotRequired[datetime]

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class PublicCertificateAuthorityOutputTypeDef(TypedDict):
    AllowedKeyAlgorithms: NotRequired[list[PublicKeyAlgorithmType]]

class PublicCertificateAuthorityTypeDef(TypedDict):
    AllowedKeyAlgorithms: NotRequired[Sequence[PublicKeyAlgorithmType]]

class CertificateOptionsTypeDef(TypedDict):
    CertificateTransparencyLoggingPreference: NotRequired[
        CertificateTransparencyLoggingPreferenceType
    ]
    Export: NotRequired[CertificateExportType]

class ExtendedKeyUsageTypeDef(TypedDict):
    Name: NotRequired[ExtendedKeyUsageNameType]
    OID: NotRequired[str]

class KeyUsageTypeDef(TypedDict):
    Name: NotRequired[KeyUsageNameType]

CertificateSummaryTypeDef = TypedDict(
    "CertificateSummaryTypeDef",
    {
        "CertificateArn": NotRequired[str],
        "DomainName": NotRequired[str],
        "SubjectAlternativeNameSummaries": NotRequired[list[str]],
        "HasAdditionalSubjectAlternativeNames": NotRequired[bool],
        "Status": NotRequired[CertificateStatusType],
        "Type": NotRequired[CertificateTypeType],
        "KeyAlgorithm": NotRequired[KeyAlgorithmType],
        "KeyUsages": NotRequired[list[KeyUsageNameType]],
        "ExtendedKeyUsages": NotRequired[list[ExtendedKeyUsageNameType]],
        "ExportOption": NotRequired[CertificateExportType],
        "InUse": NotRequired[bool],
        "Exported": NotRequired[bool],
        "RenewalEligibility": NotRequired[RenewalEligibilityType],
        "NotBefore": NotRequired[datetime],
        "NotAfter": NotRequired[datetime],
        "CreatedAt": NotRequired[datetime],
        "IssuedAt": NotRequired[datetime],
        "ImportedAt": NotRequired[datetime],
        "RevokedAt": NotRequired[datetime],
        "ManagedBy": NotRequired[Literal["CLOUDFRONT"]],
        "CertificateKeyPairOrigin": NotRequired[CertificateKeyPairOriginType],
    },
)

class CommonNameFilterTypeDef(TypedDict):
    Value: str
    ComparisonOperator: ComparisonOperatorType

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

ExpirationTypeDef = TypedDict(
    "ExpirationTypeDef",
    {
        "Value": int,
        "Type": TimeTypeType,
    },
)

class CustomAttributeTypeDef(TypedDict):
    ObjectIdentifier: NotRequired[str]
    Value: NotRequired[str]

class DeleteAcmeDomainValidationRequestTypeDef(TypedDict):
    AcmeDomainValidationArn: str

class DeleteAcmeEndpointRequestTypeDef(TypedDict):
    AcmeEndpointArn: str

class DeleteAcmeExternalAccountBindingRequestTypeDef(TypedDict):
    AcmeExternalAccountBindingArn: str

class DeleteCertificateRequestTypeDef(TypedDict):
    CertificateArn: str

class DescribeAcmeAccountRequestTypeDef(TypedDict):
    AcmeEndpointArn: str
    AccountUrl: str

class DescribeAcmeDomainValidationRequestTypeDef(TypedDict):
    AcmeDomainValidationArn: str

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class DescribeAcmeEndpointRequestTypeDef(TypedDict):
    AcmeEndpointArn: str

class DescribeAcmeExternalAccountBindingRequestTypeDef(TypedDict):
    AcmeExternalAccountBindingArn: str

class DescribeCertificateRequestTypeDef(TypedDict):
    CertificateArn: str

class DnsNameFilterTypeDef(TypedDict):
    Value: str
    ComparisonOperator: ComparisonOperatorType

class DomainScopeTypeDef(TypedDict):
    ExactDomain: NotRequired[DomainScopeOptionType]
    Subdomains: NotRequired[DomainScopeOptionType]
    Wildcards: NotRequired[DomainScopeOptionType]

ResourceRecordTypeDef = TypedDict(
    "ResourceRecordTypeDef",
    {
        "Name": str,
        "Type": Literal["CNAME"],
        "Value": str,
    },
)

class DomainValidationOptionTypeDef(TypedDict):
    DomainName: str
    ValidationDomain: str

class HttpRedirectTypeDef(TypedDict):
    RedirectFrom: NotRequired[str]
    RedirectTo: NotRequired[str]

class ExpiryEventsConfigurationTypeDef(TypedDict):
    DaysBeforeExpiry: NotRequired[int]

class FiltersTypeDef(TypedDict):
    extendedKeyUsage: NotRequired[Sequence[ExtendedKeyUsageNameType]]
    keyUsage: NotRequired[Sequence[KeyUsageNameType]]
    keyTypes: NotRequired[Sequence[KeyAlgorithmType]]
    exportOption: NotRequired[CertificateExportType]
    managedBy: NotRequired[Literal["CLOUDFRONT"]]

class OtherNameTypeDef(TypedDict):
    ObjectIdentifier: NotRequired[str]
    Value: NotRequired[str]

class GetAcmeExternalAccountBindingCredentialsRequestTypeDef(TypedDict):
    AcmeExternalAccountBindingArn: str

class GetCertificateRequestTypeDef(TypedDict):
    CertificateArn: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAcmeAccountsRequestTypeDef(TypedDict):
    AcmeEndpointArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListAcmeDomainValidationsRequestTypeDef(TypedDict):
    AcmeEndpointArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListAcmeEndpointsRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListAcmeExternalAccountBindingsRequestTypeDef(TypedDict):
    AcmeEndpointArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListTagsForCertificateRequestTypeDef(TypedDict):
    CertificateArn: str

class ListTagsForResourceRequestTypeDef(TypedDict):
    ResourceArn: str

class RenewCertificateRequestTypeDef(TypedDict):
    CertificateArn: str

class ResendValidationEmailRequestTypeDef(TypedDict):
    CertificateArn: str
    Domain: str
    ValidationDomain: str

class RevokeAcmeAccountRequestTypeDef(TypedDict):
    AcmeEndpointArn: str
    AccountUrl: str

class RevokeAcmeExternalAccountBindingRequestTypeDef(TypedDict):
    AcmeExternalAccountBindingArn: str

class RevokeCertificateRequestTypeDef(TypedDict):
    CertificateArn: str
    RevocationReason: RevocationReasonType

TimestampTypeDef = Union[datetime, str]

class UntagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class CertificateMetadataTypeDef(TypedDict):
    AcmCertificateMetadata: NotRequired[AcmCertificateMetadataTypeDef]

class AddTagsToCertificateRequestTypeDef(TypedDict):
    CertificateArn: str
    Tags: Sequence[TagTypeDef]

class RemoveTagsFromCertificateRequestTypeDef(TypedDict):
    CertificateArn: str
    Tags: Sequence[TagTypeDef]

class TagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]

class ExportCertificateRequestTypeDef(TypedDict):
    CertificateArn: str
    Passphrase: BlobTypeDef

class ImportCertificateRequestTypeDef(TypedDict):
    Certificate: BlobTypeDef
    PrivateKey: BlobTypeDef
    CertificateArn: NotRequired[str]
    CertificateChain: NotRequired[BlobTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]

class CertificateAuthorityOutputTypeDef(TypedDict):
    PublicCertificateAuthority: NotRequired[PublicCertificateAuthorityOutputTypeDef]

class CertificateAuthorityTypeDef(TypedDict):
    PublicCertificateAuthority: NotRequired[PublicCertificateAuthorityTypeDef]

class UpdateCertificateOptionsRequestTypeDef(TypedDict):
    CertificateArn: str
    Options: CertificateOptionsTypeDef

class SubjectFilterTypeDef(TypedDict):
    CommonName: NotRequired[CommonNameFilterTypeDef]

class CreateAcmeDomainValidationResponseTypeDef(TypedDict):
    AcmeDomainValidationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAcmeEndpointResponseTypeDef(TypedDict):
    AcmeEndpointArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAcmeExternalAccountBindingResponseTypeDef(TypedDict):
    ExternalAccountBinding: AcmeExternalAccountBindingTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAcmeAccountResponseTypeDef(TypedDict):
    AcmeAccount: AcmeAccountTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAcmeExternalAccountBindingResponseTypeDef(TypedDict):
    ExternalAccountBinding: AcmeExternalAccountBindingTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class ExportCertificateResponseTypeDef(TypedDict):
    Certificate: str
    CertificateChain: str
    PrivateKey: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetAcmeExternalAccountBindingCredentialsResponseTypeDef(TypedDict):
    KeyId: str
    MacKey: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetCertificateResponseTypeDef(TypedDict):
    Certificate: str
    CertificateChain: str
    ResponseMetadata: ResponseMetadataTypeDef

class ImportCertificateResponseTypeDef(TypedDict):
    CertificateArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListAcmeAccountsResponseTypeDef(TypedDict):
    AcmeAccounts: list[AcmeAccountSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListAcmeExternalAccountBindingsResponseTypeDef(TypedDict):
    ExternalAccountBindings: list[AcmeExternalAccountBindingSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListCertificatesResponseTypeDef(TypedDict):
    CertificateSummaryList: list[CertificateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTagsForCertificateResponseTypeDef(TypedDict):
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class RequestCertificateResponseTypeDef(TypedDict):
    CertificateArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class RevokeCertificateResponseTypeDef(TypedDict):
    CertificateArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAcmeExternalAccountBindingRequestTypeDef(TypedDict):
    AcmeEndpointArn: str
    RoleArn: str
    IdempotencyToken: NotRequired[str]
    Expiration: NotRequired[ExpirationTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]

class DistinguishedNameTypeDef(TypedDict):
    CommonName: NotRequired[str]
    DomainComponents: NotRequired[list[str]]
    Country: NotRequired[str]
    CustomAttributes: NotRequired[list[CustomAttributeTypeDef]]
    DistinguishedNameQualifier: NotRequired[str]
    GenerationQualifier: NotRequired[str]
    GivenName: NotRequired[str]
    Initials: NotRequired[str]
    Locality: NotRequired[str]
    Organization: NotRequired[str]
    OrganizationalUnit: NotRequired[str]
    Pseudonym: NotRequired[str]
    SerialNumber: NotRequired[str]
    State: NotRequired[str]
    Surname: NotRequired[str]
    Title: NotRequired[str]

class DescribeAcmeDomainValidationRequestWaitExtraTypeDef(TypedDict):
    AcmeDomainValidationArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeAcmeDomainValidationRequestWaitTypeDef(TypedDict):
    AcmeDomainValidationArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeAcmeEndpointRequestWaitExtraTypeDef(TypedDict):
    AcmeEndpointArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeAcmeEndpointRequestWaitTypeDef(TypedDict):
    AcmeEndpointArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeCertificateRequestWaitTypeDef(TypedDict):
    CertificateArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class SubjectAlternativeNameFilterTypeDef(TypedDict):
    DnsName: NotRequired[DnsNameFilterTypeDef]

class DnsPrevalidationOptionsTypeDef(TypedDict):
    DomainScope: NotRequired[DomainScopeTypeDef]
    HostedZoneId: NotRequired[str]

class DnsPrevalidationDetailsTypeDef(TypedDict):
    DomainScope: NotRequired[DomainScopeTypeDef]
    HostedZoneId: NotRequired[str]
    ResourceRecord: NotRequired[ResourceRecordTypeDef]

class RequestCertificateRequestTypeDef(TypedDict):
    DomainName: str
    ValidationMethod: NotRequired[ValidationMethodType]
    SubjectAlternativeNames: NotRequired[Sequence[str]]
    IdempotencyToken: NotRequired[str]
    DomainValidationOptions: NotRequired[Sequence[DomainValidationOptionTypeDef]]
    Options: NotRequired[CertificateOptionsTypeDef]
    CertificateAuthorityArn: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    KeyAlgorithm: NotRequired[KeyAlgorithmType]
    ManagedBy: NotRequired[Literal["CLOUDFRONT"]]

class DomainValidationTypeDef(TypedDict):
    DomainName: str
    ValidationEmails: NotRequired[list[str]]
    ValidationDomain: NotRequired[str]
    ValidationStatus: NotRequired[DomainStatusType]
    ResourceRecord: NotRequired[ResourceRecordTypeDef]
    HttpRedirect: NotRequired[HttpRedirectTypeDef]
    ValidationMethod: NotRequired[ValidationMethodType]

class GetAccountConfigurationResponseTypeDef(TypedDict):
    ExpiryEvents: ExpiryEventsConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutAccountConfigurationRequestTypeDef(TypedDict):
    IdempotencyToken: str
    ExpiryEvents: NotRequired[ExpiryEventsConfigurationTypeDef]

class ListCertificatesRequestTypeDef(TypedDict):
    CertificateStatuses: NotRequired[Sequence[CertificateStatusType]]
    CertificateKeyPairOrigins: NotRequired[Sequence[CertificateKeyPairOriginType]]
    Includes: NotRequired[FiltersTypeDef]
    NextToken: NotRequired[str]
    MaxItems: NotRequired[int]
    SortBy: NotRequired[Literal["CREATED_AT"]]
    SortOrder: NotRequired[SortOrderType]

class ListAcmeAccountsRequestPaginateTypeDef(TypedDict):
    AcmeEndpointArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAcmeDomainValidationsRequestPaginateTypeDef(TypedDict):
    AcmeEndpointArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAcmeEndpointsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAcmeExternalAccountBindingsRequestPaginateTypeDef(TypedDict):
    AcmeEndpointArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCertificatesRequestPaginateTypeDef(TypedDict):
    CertificateStatuses: NotRequired[Sequence[CertificateStatusType]]
    CertificateKeyPairOrigins: NotRequired[Sequence[CertificateKeyPairOriginType]]
    Includes: NotRequired[FiltersTypeDef]
    SortBy: NotRequired[Literal["CREATED_AT"]]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class TimestampRangeTypeDef(TypedDict):
    Start: NotRequired[TimestampTypeDef]
    End: NotRequired[TimestampTypeDef]

class AcmeEndpointSummaryTypeDef(TypedDict):
    AcmeEndpointArn: NotRequired[str]
    EndpointUrl: NotRequired[str]
    Status: NotRequired[AcmeEndpointStatusType]
    FailureReason: NotRequired[str]
    AuthorizationBehavior: NotRequired[Literal["PRE_APPROVED"]]
    Contact: NotRequired[AcmeContactType]
    CertificateAuthority: NotRequired[CertificateAuthorityOutputTypeDef]
    CertificateTags: NotRequired[list[TagTypeDef]]
    CreatedAt: NotRequired[datetime]
    UpdatedAt: NotRequired[datetime]

class AcmeEndpointTypeDef(TypedDict):
    AcmeEndpointArn: NotRequired[str]
    EndpointUrl: NotRequired[str]
    Status: NotRequired[AcmeEndpointStatusType]
    FailureReason: NotRequired[str]
    AuthorizationBehavior: NotRequired[Literal["PRE_APPROVED"]]
    Contact: NotRequired[AcmeContactType]
    CertificateAuthority: NotRequired[CertificateAuthorityOutputTypeDef]
    CertificateTags: NotRequired[list[TagTypeDef]]
    CreatedAt: NotRequired[datetime]
    UpdatedAt: NotRequired[datetime]

CertificateAuthorityUnionTypeDef = Union[
    CertificateAuthorityTypeDef, CertificateAuthorityOutputTypeDef
]

class GeneralNameTypeDef(TypedDict):
    DirectoryName: NotRequired[DistinguishedNameTypeDef]
    DnsName: NotRequired[str]
    IpAddress: NotRequired[str]
    OtherName: NotRequired[OtherNameTypeDef]
    RegisteredId: NotRequired[str]
    Rfc822Name: NotRequired[str]
    UniformResourceIdentifier: NotRequired[str]

class PrevalidationOptionsTypeDef(TypedDict):
    DnsPrevalidation: NotRequired[DnsPrevalidationOptionsTypeDef]

class PrevalidationDetailsTypeDef(TypedDict):
    DnsPrevalidation: NotRequired[DnsPrevalidationDetailsTypeDef]

class RenewalSummaryTypeDef(TypedDict):
    RenewalStatus: RenewalStatusType
    DomainValidationOptions: list[DomainValidationTypeDef]
    UpdatedAt: datetime
    RenewalStatusReason: NotRequired[FailureReasonType]

class X509AttributeFilterTypeDef(TypedDict):
    Subject: NotRequired[SubjectFilterTypeDef]
    SubjectAlternativeName: NotRequired[SubjectAlternativeNameFilterTypeDef]
    ExtendedKeyUsage: NotRequired[ExtendedKeyUsageNameType]
    KeyUsage: NotRequired[KeyUsageNameType]
    KeyAlgorithm: NotRequired[KeyAlgorithmType]
    SerialNumber: NotRequired[str]
    NotAfter: NotRequired[TimestampRangeTypeDef]
    NotBefore: NotRequired[TimestampRangeTypeDef]

class ListAcmeEndpointsResponseTypeDef(TypedDict):
    AcmeEndpoints: list[AcmeEndpointSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeAcmeEndpointResponseTypeDef(TypedDict):
    AcmeEndpoint: AcmeEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAcmeEndpointRequestTypeDef(TypedDict):
    AuthorizationBehavior: Literal["PRE_APPROVED"]
    CertificateAuthority: CertificateAuthorityUnionTypeDef
    IdempotencyToken: NotRequired[str]
    Contact: NotRequired[AcmeContactType]
    Tags: NotRequired[Sequence[TagTypeDef]]
    CertificateTags: NotRequired[Sequence[TagTypeDef]]

class UpdateAcmeEndpointRequestTypeDef(TypedDict):
    AcmeEndpointArn: str
    AuthorizationBehavior: NotRequired[Literal["PRE_APPROVED"]]
    Contact: NotRequired[AcmeContactType]
    CertificateAuthority: NotRequired[CertificateAuthorityUnionTypeDef]

class X509AttributesTypeDef(TypedDict):
    Issuer: NotRequired[DistinguishedNameTypeDef]
    Subject: NotRequired[DistinguishedNameTypeDef]
    SubjectAlternativeNames: NotRequired[list[GeneralNameTypeDef]]
    ExtendedKeyUsages: NotRequired[list[ExtendedKeyUsageNameType]]
    KeyAlgorithm: NotRequired[KeyAlgorithmType]
    KeyUsages: NotRequired[list[KeyUsageNameType]]
    SerialNumber: NotRequired[str]
    NotAfter: NotRequired[datetime]
    NotBefore: NotRequired[datetime]

class CreateAcmeDomainValidationRequestTypeDef(TypedDict):
    AcmeEndpointArn: str
    DomainName: str
    PrevalidationOptions: PrevalidationOptionsTypeDef
    IdempotencyToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class UpdateAcmeDomainValidationRequestTypeDef(TypedDict):
    AcmeDomainValidationArn: str
    PrevalidationOptions: NotRequired[PrevalidationOptionsTypeDef]

class AcmeDomainValidationSummaryTypeDef(TypedDict):
    AcmeDomainValidationArn: NotRequired[str]
    AcmeEndpointArn: NotRequired[str]
    DomainName: NotRequired[str]
    PrevalidationType: NotRequired[Literal["DNS_PREVALIDATION"]]
    PrevalidationDetails: NotRequired[PrevalidationDetailsTypeDef]
    Status: NotRequired[AcmeDomainValidationStatusType]
    FailureDetails: NotRequired[FailureDetailsTypeDef]
    CreatedAt: NotRequired[datetime]
    UpdatedAt: NotRequired[datetime]

class AcmeDomainValidationTypeDef(TypedDict):
    AcmeDomainValidationArn: NotRequired[str]
    AcmeEndpointArn: NotRequired[str]
    DomainName: NotRequired[str]
    PrevalidationType: NotRequired[Literal["DNS_PREVALIDATION"]]
    PrevalidationDetails: NotRequired[PrevalidationDetailsTypeDef]
    Status: NotRequired[AcmeDomainValidationStatusType]
    FailureDetails: NotRequired[FailureDetailsTypeDef]
    CreatedAt: NotRequired[datetime]
    UpdatedAt: NotRequired[datetime]

CertificateDetailTypeDef = TypedDict(
    "CertificateDetailTypeDef",
    {
        "CertificateArn": NotRequired[str],
        "DomainName": NotRequired[str],
        "SubjectAlternativeNames": NotRequired[list[str]],
        "ManagedBy": NotRequired[Literal["CLOUDFRONT"]],
        "DomainValidationOptions": NotRequired[list[DomainValidationTypeDef]],
        "Serial": NotRequired[str],
        "Subject": NotRequired[str],
        "Issuer": NotRequired[str],
        "CreatedAt": NotRequired[datetime],
        "IssuedAt": NotRequired[datetime],
        "ImportedAt": NotRequired[datetime],
        "Status": NotRequired[CertificateStatusType],
        "RevokedAt": NotRequired[datetime],
        "RevocationReason": NotRequired[RevocationReasonType],
        "NotBefore": NotRequired[datetime],
        "NotAfter": NotRequired[datetime],
        "KeyAlgorithm": NotRequired[KeyAlgorithmType],
        "SignatureAlgorithm": NotRequired[str],
        "InUseBy": NotRequired[list[str]],
        "FailureReason": NotRequired[FailureReasonType],
        "Type": NotRequired[CertificateTypeType],
        "RenewalSummary": NotRequired[RenewalSummaryTypeDef],
        "KeyUsages": NotRequired[list[KeyUsageTypeDef]],
        "ExtendedKeyUsages": NotRequired[list[ExtendedKeyUsageTypeDef]],
        "CertificateAuthorityArn": NotRequired[str],
        "RenewalEligibility": NotRequired[RenewalEligibilityType],
        "Options": NotRequired[CertificateOptionsTypeDef],
        "CertificateKeyPairOrigin": NotRequired[CertificateKeyPairOriginType],
        "AcmeEndpointArn": NotRequired[str],
        "AcmeAccountId": NotRequired[str],
    },
)

class CertificateFilterTypeDef(TypedDict):
    CertificateArn: NotRequired[str]
    X509AttributeFilter: NotRequired[X509AttributeFilterTypeDef]
    AcmCertificateMetadataFilter: NotRequired[AcmCertificateMetadataFilterTypeDef]

class CertificateSearchResultTypeDef(TypedDict):
    CertificateArn: NotRequired[str]
    X509Attributes: NotRequired[X509AttributesTypeDef]
    CertificateMetadata: NotRequired[CertificateMetadataTypeDef]

class ListAcmeDomainValidationsResponseTypeDef(TypedDict):
    AcmeDomainValidations: list[AcmeDomainValidationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeAcmeDomainValidationResponseTypeDef(TypedDict):
    AcmeDomainValidation: AcmeDomainValidationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeCertificateResponseTypeDef(TypedDict):
    Certificate: CertificateDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CertificateFilterStatementPaginatorTypeDef(TypedDict):
    And: NotRequired[Sequence[Mapping[str, Any]]]
    Or: NotRequired[Sequence[Mapping[str, Any]]]
    Not: NotRequired[Mapping[str, Any]]
    Filter: NotRequired[CertificateFilterTypeDef]

class CertificateFilterStatementTypeDef(TypedDict):
    And: NotRequired[Sequence[Mapping[str, Any]]]
    Or: NotRequired[Sequence[Mapping[str, Any]]]
    Not: NotRequired[Mapping[str, Any]]
    Filter: NotRequired[CertificateFilterTypeDef]

class SearchCertificatesResponseTypeDef(TypedDict):
    Results: list[CertificateSearchResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class SearchCertificatesRequestPaginateTypeDef(TypedDict):
    FilterStatement: NotRequired[CertificateFilterStatementPaginatorTypeDef]
    SortBy: NotRequired[SearchCertificatesSortByType]
    SortOrder: NotRequired[SearchCertificatesSortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchCertificatesRequestTypeDef(TypedDict):
    FilterStatement: NotRequired[CertificateFilterStatementTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    SortBy: NotRequired[SearchCertificatesSortByType]
    SortOrder: NotRequired[SearchCertificatesSortOrderType]
