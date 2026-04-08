"""
Type annotations for acm service type definitions.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_aiobotocore_acm.type_defs import AcmCertificateMetadataFilterTypeDef

    data: AcmCertificateMetadataFilterTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import IO, Any, Union

from aiobotocore.response import StreamingBody

from .literals import (
    CertificateExportType,
    CertificateStatusType,
    CertificateTransparencyLoggingPreferenceType,
    CertificateTypeType,
    ComparisonOperatorType,
    DomainStatusType,
    ExtendedKeyUsageNameType,
    FailureReasonType,
    KeyAlgorithmType,
    KeyUsageNameType,
    RenewalEligibilityType,
    RenewalStatusType,
    RevocationReasonType,
    SearchCertificatesSortByType,
    SearchCertificatesSortOrderType,
    SortOrderType,
    ValidationMethodType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AcmCertificateMetadataFilterTypeDef",
    "AcmCertificateMetadataTypeDef",
    "AddTagsToCertificateRequestTypeDef",
    "BlobTypeDef",
    "CertificateDetailTypeDef",
    "CertificateFilterStatementPaginatorTypeDef",
    "CertificateFilterStatementTypeDef",
    "CertificateFilterTypeDef",
    "CertificateMetadataTypeDef",
    "CertificateOptionsTypeDef",
    "CertificateSearchResultTypeDef",
    "CertificateSummaryTypeDef",
    "CommonNameFilterTypeDef",
    "CustomAttributeTypeDef",
    "DeleteCertificateRequestTypeDef",
    "DescribeCertificateRequestTypeDef",
    "DescribeCertificateRequestWaitTypeDef",
    "DescribeCertificateResponseTypeDef",
    "DistinguishedNameTypeDef",
    "DnsNameFilterTypeDef",
    "DomainValidationOptionTypeDef",
    "DomainValidationTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ExpiryEventsConfigurationTypeDef",
    "ExportCertificateRequestTypeDef",
    "ExportCertificateResponseTypeDef",
    "ExtendedKeyUsageTypeDef",
    "FiltersTypeDef",
    "GeneralNameTypeDef",
    "GetAccountConfigurationResponseTypeDef",
    "GetCertificateRequestTypeDef",
    "GetCertificateResponseTypeDef",
    "HttpRedirectTypeDef",
    "ImportCertificateRequestTypeDef",
    "ImportCertificateResponseTypeDef",
    "KeyUsageTypeDef",
    "ListCertificatesRequestPaginateTypeDef",
    "ListCertificatesRequestTypeDef",
    "ListCertificatesResponseTypeDef",
    "ListTagsForCertificateRequestTypeDef",
    "ListTagsForCertificateResponseTypeDef",
    "OtherNameTypeDef",
    "PaginatorConfigTypeDef",
    "PutAccountConfigurationRequestTypeDef",
    "RemoveTagsFromCertificateRequestTypeDef",
    "RenewCertificateRequestTypeDef",
    "RenewalSummaryTypeDef",
    "RequestCertificateRequestTypeDef",
    "RequestCertificateResponseTypeDef",
    "ResendValidationEmailRequestTypeDef",
    "ResourceRecordTypeDef",
    "ResponseMetadataTypeDef",
    "RevokeCertificateRequestTypeDef",
    "RevokeCertificateResponseTypeDef",
    "SearchCertificatesRequestPaginateTypeDef",
    "SearchCertificatesRequestTypeDef",
    "SearchCertificatesResponseTypeDef",
    "SubjectAlternativeNameFilterTypeDef",
    "SubjectFilterTypeDef",
    "TagTypeDef",
    "TimestampRangeTypeDef",
    "TimestampTypeDef",
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
    },
)


class TagTypeDef(TypedDict):
    Key: str
    Value: NotRequired[str]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


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
    },
)


class CommonNameFilterTypeDef(TypedDict):
    Value: str
    ComparisonOperator: ComparisonOperatorType


class CustomAttributeTypeDef(TypedDict):
    ObjectIdentifier: NotRequired[str]
    Value: NotRequired[str]


class DeleteCertificateRequestTypeDef(TypedDict):
    CertificateArn: str


class DescribeCertificateRequestTypeDef(TypedDict):
    CertificateArn: str


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DnsNameFilterTypeDef(TypedDict):
    Value: str
    ComparisonOperator: ComparisonOperatorType


class DomainValidationOptionTypeDef(TypedDict):
    DomainName: str
    ValidationDomain: str


class HttpRedirectTypeDef(TypedDict):
    RedirectFrom: NotRequired[str]
    RedirectTo: NotRequired[str]


ResourceRecordTypeDef = TypedDict(
    "ResourceRecordTypeDef",
    {
        "Name": str,
        "Type": Literal["CNAME"],
        "Value": str,
    },
)


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


class GetCertificateRequestTypeDef(TypedDict):
    CertificateArn: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListTagsForCertificateRequestTypeDef(TypedDict):
    CertificateArn: str


class RenewCertificateRequestTypeDef(TypedDict):
    CertificateArn: str


class ResendValidationEmailRequestTypeDef(TypedDict):
    CertificateArn: str
    Domain: str
    ValidationDomain: str


class RevokeCertificateRequestTypeDef(TypedDict):
    CertificateArn: str
    RevocationReason: RevocationReasonType


TimestampTypeDef = Union[datetime, str]


class CertificateMetadataTypeDef(TypedDict):
    AcmCertificateMetadata: NotRequired[AcmCertificateMetadataTypeDef]


class AddTagsToCertificateRequestTypeDef(TypedDict):
    CertificateArn: str
    Tags: Sequence[TagTypeDef]


class RemoveTagsFromCertificateRequestTypeDef(TypedDict):
    CertificateArn: str
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


class UpdateCertificateOptionsRequestTypeDef(TypedDict):
    CertificateArn: str
    Options: CertificateOptionsTypeDef


class SubjectFilterTypeDef(TypedDict):
    CommonName: NotRequired[CommonNameFilterTypeDef]


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


class DescribeCertificateRequestWaitTypeDef(TypedDict):
    CertificateArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class ExportCertificateResponseTypeDef(TypedDict):
    Certificate: str
    CertificateChain: str
    PrivateKey: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetCertificateResponseTypeDef(TypedDict):
    Certificate: str
    CertificateChain: str
    ResponseMetadata: ResponseMetadataTypeDef


class ImportCertificateResponseTypeDef(TypedDict):
    CertificateArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListCertificatesResponseTypeDef(TypedDict):
    CertificateSummaryList: list[CertificateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForCertificateResponseTypeDef(TypedDict):
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class RequestCertificateResponseTypeDef(TypedDict):
    CertificateArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class RevokeCertificateResponseTypeDef(TypedDict):
    CertificateArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class SubjectAlternativeNameFilterTypeDef(TypedDict):
    DnsName: NotRequired[DnsNameFilterTypeDef]


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
    Includes: NotRequired[FiltersTypeDef]
    NextToken: NotRequired[str]
    MaxItems: NotRequired[int]
    SortBy: NotRequired[Literal["CREATED_AT"]]
    SortOrder: NotRequired[SortOrderType]


class ListCertificatesRequestPaginateTypeDef(TypedDict):
    CertificateStatuses: NotRequired[Sequence[CertificateStatusType]]
    Includes: NotRequired[FiltersTypeDef]
    SortBy: NotRequired[Literal["CREATED_AT"]]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class TimestampRangeTypeDef(TypedDict):
    Start: NotRequired[TimestampTypeDef]
    End: NotRequired[TimestampTypeDef]


class GeneralNameTypeDef(TypedDict):
    DirectoryName: NotRequired[DistinguishedNameTypeDef]
    DnsName: NotRequired[str]
    IpAddress: NotRequired[str]
    OtherName: NotRequired[OtherNameTypeDef]
    RegisteredId: NotRequired[str]
    Rfc822Name: NotRequired[str]
    UniformResourceIdentifier: NotRequired[str]


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
