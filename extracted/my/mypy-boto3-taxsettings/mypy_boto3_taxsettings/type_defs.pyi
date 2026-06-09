"""
Type annotations for taxsettings service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_taxsettings/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_taxsettings.type_defs import TaxInheritanceDetailsTypeDef

    data: TaxInheritanceDetailsTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from datetime import datetime
from typing import IO, Any, Union

from botocore.response import StreamingBody

from .literals import (
    AddressRoleTypeType,
    ChileDocumentTypeType,
    CustomerTypeType,
    EntityExemptionAccountStatusType,
    HeritageStatusType,
    IndonesiaTaxRegistrationNumberTypeType,
    IndustriesType,
    IsraelCustomerTypeType,
    IsraelDealerTypeType,
    MalaysiaServiceTaxCodeType,
    PersonTypeType,
    PolandTaxRegistrationNumberTypeType,
    RegistrationTypeType,
    SaudiArabiaTaxRegistrationNumberTypeType,
    SectorType,
    TaxRegistrationNumberTypeType,
    TaxRegistrationStatusType,
    TaxRegistrationTypeType,
    UkraineTrnTypeType,
    UzbekistanTaxRegistrationNumberTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AccountDetailsTypeDef",
    "AccountMetaDataTypeDef",
    "AdditionalInfoRequestTypeDef",
    "AdditionalInfoResponseTypeDef",
    "AddressTypeDef",
    "AuthorityTypeDef",
    "BatchDeleteTaxRegistrationErrorTypeDef",
    "BatchDeleteTaxRegistrationRequestTypeDef",
    "BatchDeleteTaxRegistrationResponseTypeDef",
    "BatchGetTaxExemptionsRequestTypeDef",
    "BatchGetTaxExemptionsResponseTypeDef",
    "BatchPutTaxRegistrationErrorTypeDef",
    "BatchPutTaxRegistrationRequestTypeDef",
    "BatchPutTaxRegistrationResponseTypeDef",
    "BelgiumAdditionalInfoTypeDef",
    "BlobTypeDef",
    "BrazilAdditionalInfoTypeDef",
    "CanadaAdditionalInfoTypeDef",
    "ChileAdditionalInfoTypeDef",
    "DeleteSupplementalTaxRegistrationRequestTypeDef",
    "DeleteTaxRegistrationRequestTypeDef",
    "DestinationS3LocationTypeDef",
    "EgyptAdditionalInfoTypeDef",
    "EstoniaAdditionalInfoTypeDef",
    "ExemptionCertificateTypeDef",
    "FranceAdditionalInfoTypeDef",
    "GeorgiaAdditionalInfoTypeDef",
    "GetTaxExemptionTypesResponseTypeDef",
    "GetTaxInheritanceResponseTypeDef",
    "GetTaxRegistrationDocumentRequestTypeDef",
    "GetTaxRegistrationDocumentResponseTypeDef",
    "GetTaxRegistrationRequestTypeDef",
    "GetTaxRegistrationResponseTypeDef",
    "GreeceAdditionalInfoTypeDef",
    "IndiaAdditionalInfoTypeDef",
    "IndonesiaAdditionalInfoTypeDef",
    "IsraelAdditionalInfoTypeDef",
    "ItalyAdditionalInfoTypeDef",
    "JurisdictionTypeDef",
    "KenyaAdditionalInfoTypeDef",
    "ListSupplementalTaxRegistrationsRequestPaginateTypeDef",
    "ListSupplementalTaxRegistrationsRequestTypeDef",
    "ListSupplementalTaxRegistrationsResponseTypeDef",
    "ListTaxExemptionsRequestPaginateTypeDef",
    "ListTaxExemptionsRequestTypeDef",
    "ListTaxExemptionsResponseTypeDef",
    "ListTaxRegistrationsRequestPaginateTypeDef",
    "ListTaxRegistrationsRequestTypeDef",
    "ListTaxRegistrationsResponseTypeDef",
    "MalaysiaAdditionalInfoOutputTypeDef",
    "MalaysiaAdditionalInfoTypeDef",
    "MalaysiaAdditionalInfoUnionTypeDef",
    "PaginatorConfigTypeDef",
    "PhilippinesAdditionalInfoTypeDef",
    "PolandAdditionalInfoTypeDef",
    "PutSupplementalTaxRegistrationRequestTypeDef",
    "PutSupplementalTaxRegistrationResponseTypeDef",
    "PutTaxExemptionRequestTypeDef",
    "PutTaxExemptionResponseTypeDef",
    "PutTaxInheritanceRequestTypeDef",
    "PutTaxRegistrationRequestTypeDef",
    "PutTaxRegistrationResponseTypeDef",
    "ResponseMetadataTypeDef",
    "RomaniaAdditionalInfoTypeDef",
    "SaudiArabiaAdditionalInfoTypeDef",
    "SourceS3LocationTypeDef",
    "SouthKoreaAdditionalInfoTypeDef",
    "SpainAdditionalInfoTypeDef",
    "SupplementalTaxRegistrationEntryTypeDef",
    "SupplementalTaxRegistrationTypeDef",
    "TaxDocumentMetadataTypeDef",
    "TaxExemptionDetailsTypeDef",
    "TaxExemptionTypeDef",
    "TaxExemptionTypeTypeDef",
    "TaxInheritanceDetailsTypeDef",
    "TaxRegistrationDocFileTypeDef",
    "TaxRegistrationDocumentTypeDef",
    "TaxRegistrationEntryTypeDef",
    "TaxRegistrationTypeDef",
    "TaxRegistrationWithJurisdictionTypeDef",
    "TurkeyAdditionalInfoTypeDef",
    "UkraineAdditionalInfoTypeDef",
    "UzbekistanAdditionalInfoTypeDef",
    "VerificationDetailsTypeDef",
    "VietnamAdditionalInfoTypeDef",
)

class TaxInheritanceDetailsTypeDef(TypedDict):
    parentEntityId: NotRequired[str]
    inheritanceObtainedReason: NotRequired[str]

class AddressTypeDef(TypedDict):
    postalCode: str
    countryCode: str
    addressLine1: NotRequired[str]
    addressLine2: NotRequired[str]
    addressLine3: NotRequired[str]
    districtOrCounty: NotRequired[str]
    city: NotRequired[str]
    stateOrRegion: NotRequired[str]

class JurisdictionTypeDef(TypedDict):
    countryCode: str
    stateOrRegion: NotRequired[str]

class BelgiumAdditionalInfoTypeDef(TypedDict):
    peppolId: NotRequired[str]
    isMercuriusBoxEnabled: NotRequired[bool]

class CanadaAdditionalInfoTypeDef(TypedDict):
    provincialSalesTaxId: NotRequired[str]
    canadaQuebecSalesTaxNumber: NotRequired[str]
    canadaRetailSalesTaxNumber: NotRequired[str]
    isResellerAccount: NotRequired[bool]

class ChileAdditionalInfoTypeDef(TypedDict):
    documentType: NotRequired[ChileDocumentTypeType]
    businessActivity: NotRequired[str]

class EgyptAdditionalInfoTypeDef(TypedDict):
    uniqueIdentificationNumber: NotRequired[str]
    uniqueIdentificationNumberExpirationDate: NotRequired[str]

class EstoniaAdditionalInfoTypeDef(TypedDict):
    registryCommercialCode: str

class FranceAdditionalInfoTypeDef(TypedDict):
    sirenNumber: str

class GeorgiaAdditionalInfoTypeDef(TypedDict):
    personType: PersonTypeType

class GreeceAdditionalInfoTypeDef(TypedDict):
    contractingAuthorityCode: NotRequired[str]

class IndonesiaAdditionalInfoTypeDef(TypedDict):
    taxRegistrationNumberType: NotRequired[IndonesiaTaxRegistrationNumberTypeType]
    ppnExceptionDesignationCode: NotRequired[str]
    decisionNumber: NotRequired[str]

class IsraelAdditionalInfoTypeDef(TypedDict):
    dealerType: IsraelDealerTypeType
    customerType: IsraelCustomerTypeType

class ItalyAdditionalInfoTypeDef(TypedDict):
    sdiAccountId: NotRequired[str]
    cigNumber: NotRequired[str]
    cupNumber: NotRequired[str]
    taxCode: NotRequired[str]
    customerType: NotRequired[CustomerTypeType]

class KenyaAdditionalInfoTypeDef(TypedDict):
    personType: PersonTypeType

class PhilippinesAdditionalInfoTypeDef(TypedDict):
    isVatRegistered: NotRequired[bool]

class PolandAdditionalInfoTypeDef(TypedDict):
    individualRegistrationNumber: NotRequired[str]
    isGroupVatEnabled: NotRequired[bool]
    taxRegistrationNumberType: NotRequired[PolandTaxRegistrationNumberTypeType]

class RomaniaAdditionalInfoTypeDef(TypedDict):
    taxRegistrationNumberType: TaxRegistrationNumberTypeType

class SaudiArabiaAdditionalInfoTypeDef(TypedDict):
    taxRegistrationNumberType: NotRequired[SaudiArabiaTaxRegistrationNumberTypeType]

class SouthKoreaAdditionalInfoTypeDef(TypedDict):
    businessRepresentativeName: str
    lineOfBusiness: str
    itemOfBusiness: str

class SpainAdditionalInfoTypeDef(TypedDict):
    registrationType: RegistrationTypeType

class TurkeyAdditionalInfoTypeDef(TypedDict):
    taxOffice: NotRequired[str]
    kepEmailId: NotRequired[str]
    secondaryTaxId: NotRequired[str]
    industries: NotRequired[IndustriesType]

class UkraineAdditionalInfoTypeDef(TypedDict):
    ukraineTrnType: UkraineTrnTypeType

class UzbekistanAdditionalInfoTypeDef(TypedDict):
    taxRegistrationNumberType: NotRequired[UzbekistanTaxRegistrationNumberTypeType]
    vatRegistrationNumber: NotRequired[str]

class VietnamAdditionalInfoTypeDef(TypedDict):
    enterpriseIdentificationNumber: NotRequired[str]
    electronicTransactionCodeNumber: NotRequired[str]
    paymentVoucherNumber: NotRequired[str]
    paymentVoucherNumberDate: NotRequired[str]

class BrazilAdditionalInfoTypeDef(TypedDict):
    ccmCode: NotRequired[str]
    legalNatureCode: NotRequired[str]

class IndiaAdditionalInfoTypeDef(TypedDict):
    pan: NotRequired[str]

class MalaysiaAdditionalInfoOutputTypeDef(TypedDict):
    serviceTaxCodes: NotRequired[list[MalaysiaServiceTaxCodeType]]
    taxInformationNumber: NotRequired[str]
    businessRegistrationNumber: NotRequired[str]

class AuthorityTypeDef(TypedDict):
    country: str
    state: NotRequired[str]

class BatchDeleteTaxRegistrationErrorTypeDef(TypedDict):
    accountId: str
    message: str
    code: NotRequired[str]

class BatchDeleteTaxRegistrationRequestTypeDef(TypedDict):
    accountIds: Sequence[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class BatchGetTaxExemptionsRequestTypeDef(TypedDict):
    accountIds: Sequence[str]

class BatchPutTaxRegistrationErrorTypeDef(TypedDict):
    accountId: str
    message: str
    code: NotRequired[str]

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class DeleteSupplementalTaxRegistrationRequestTypeDef(TypedDict):
    authorityId: str

class DeleteTaxRegistrationRequestTypeDef(TypedDict):
    accountId: NotRequired[str]

class DestinationS3LocationTypeDef(TypedDict):
    bucket: str
    prefix: NotRequired[str]

class TaxDocumentMetadataTypeDef(TypedDict):
    taxDocumentAccessToken: str
    taxDocumentName: str

class GetTaxRegistrationRequestTypeDef(TypedDict):
    accountId: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListSupplementalTaxRegistrationsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListTaxExemptionsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListTaxRegistrationsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class MalaysiaAdditionalInfoTypeDef(TypedDict):
    serviceTaxCodes: NotRequired[Sequence[MalaysiaServiceTaxCodeType]]
    taxInformationNumber: NotRequired[str]
    businessRegistrationNumber: NotRequired[str]

class PutTaxInheritanceRequestTypeDef(TypedDict):
    heritageStatus: NotRequired[HeritageStatusType]

class SourceS3LocationTypeDef(TypedDict):
    bucket: str
    key: str

class SupplementalTaxRegistrationEntryTypeDef(TypedDict):
    registrationId: str
    registrationType: Literal["VAT"]
    legalName: str
    address: AddressTypeDef

class SupplementalTaxRegistrationTypeDef(TypedDict):
    registrationId: str
    registrationType: Literal["VAT"]
    legalName: str
    address: AddressTypeDef
    authorityId: str
    status: TaxRegistrationStatusType

class AccountMetaDataTypeDef(TypedDict):
    accountName: NotRequired[str]
    seller: NotRequired[str]
    address: NotRequired[AddressTypeDef]
    addressType: NotRequired[AddressRoleTypeType]
    addressRoleMap: NotRequired[dict[AddressRoleTypeType, JurisdictionTypeDef]]

class AdditionalInfoResponseTypeDef(TypedDict):
    malaysiaAdditionalInfo: NotRequired[MalaysiaAdditionalInfoOutputTypeDef]
    israelAdditionalInfo: NotRequired[IsraelAdditionalInfoTypeDef]
    estoniaAdditionalInfo: NotRequired[EstoniaAdditionalInfoTypeDef]
    canadaAdditionalInfo: NotRequired[CanadaAdditionalInfoTypeDef]
    brazilAdditionalInfo: NotRequired[BrazilAdditionalInfoTypeDef]
    spainAdditionalInfo: NotRequired[SpainAdditionalInfoTypeDef]
    kenyaAdditionalInfo: NotRequired[KenyaAdditionalInfoTypeDef]
    southKoreaAdditionalInfo: NotRequired[SouthKoreaAdditionalInfoTypeDef]
    turkeyAdditionalInfo: NotRequired[TurkeyAdditionalInfoTypeDef]
    georgiaAdditionalInfo: NotRequired[GeorgiaAdditionalInfoTypeDef]
    italyAdditionalInfo: NotRequired[ItalyAdditionalInfoTypeDef]
    romaniaAdditionalInfo: NotRequired[RomaniaAdditionalInfoTypeDef]
    ukraineAdditionalInfo: NotRequired[UkraineAdditionalInfoTypeDef]
    polandAdditionalInfo: NotRequired[PolandAdditionalInfoTypeDef]
    saudiArabiaAdditionalInfo: NotRequired[SaudiArabiaAdditionalInfoTypeDef]
    indiaAdditionalInfo: NotRequired[IndiaAdditionalInfoTypeDef]
    indonesiaAdditionalInfo: NotRequired[IndonesiaAdditionalInfoTypeDef]
    vietnamAdditionalInfo: NotRequired[VietnamAdditionalInfoTypeDef]
    egyptAdditionalInfo: NotRequired[EgyptAdditionalInfoTypeDef]
    greeceAdditionalInfo: NotRequired[GreeceAdditionalInfoTypeDef]
    uzbekistanAdditionalInfo: NotRequired[UzbekistanAdditionalInfoTypeDef]
    philippinesAdditionalInfo: NotRequired[PhilippinesAdditionalInfoTypeDef]
    belgiumAdditionalInfo: NotRequired[BelgiumAdditionalInfoTypeDef]
    chileAdditionalInfo: NotRequired[ChileAdditionalInfoTypeDef]
    franceAdditionalInfo: NotRequired[FranceAdditionalInfoTypeDef]

class TaxExemptionTypeTypeDef(TypedDict):
    displayName: NotRequired[str]
    description: NotRequired[str]
    applicableJurisdictions: NotRequired[list[AuthorityTypeDef]]

class BatchDeleteTaxRegistrationResponseTypeDef(TypedDict):
    errors: list[BatchDeleteTaxRegistrationErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetTaxInheritanceResponseTypeDef(TypedDict):
    heritageStatus: HeritageStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class GetTaxRegistrationDocumentResponseTypeDef(TypedDict):
    destinationFilePath: str
    presignedS3Url: str
    ResponseMetadata: ResponseMetadataTypeDef

class PutSupplementalTaxRegistrationResponseTypeDef(TypedDict):
    authorityId: str
    status: TaxRegistrationStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class PutTaxExemptionResponseTypeDef(TypedDict):
    caseId: str
    ResponseMetadata: ResponseMetadataTypeDef

class PutTaxRegistrationResponseTypeDef(TypedDict):
    status: TaxRegistrationStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class BatchPutTaxRegistrationResponseTypeDef(TypedDict):
    status: TaxRegistrationStatusType
    errors: list[BatchPutTaxRegistrationErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ExemptionCertificateTypeDef(TypedDict):
    documentName: str
    documentFile: BlobTypeDef

class TaxRegistrationDocFileTypeDef(TypedDict):
    fileName: str
    fileContent: BlobTypeDef

class GetTaxRegistrationDocumentRequestTypeDef(TypedDict):
    taxDocumentMetadata: TaxDocumentMetadataTypeDef
    destinationS3Location: NotRequired[DestinationS3LocationTypeDef]

class ListSupplementalTaxRegistrationsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTaxExemptionsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTaxRegistrationsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

MalaysiaAdditionalInfoUnionTypeDef = Union[
    MalaysiaAdditionalInfoTypeDef, MalaysiaAdditionalInfoOutputTypeDef
]

class PutSupplementalTaxRegistrationRequestTypeDef(TypedDict):
    taxRegistrationEntry: SupplementalTaxRegistrationEntryTypeDef

class ListSupplementalTaxRegistrationsResponseTypeDef(TypedDict):
    taxRegistrations: list[SupplementalTaxRegistrationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class TaxRegistrationTypeDef(TypedDict):
    registrationId: str
    registrationType: TaxRegistrationTypeType
    legalName: str
    status: TaxRegistrationStatusType
    legalAddress: AddressTypeDef
    sector: NotRequired[SectorType]
    taxDocumentMetadatas: NotRequired[list[TaxDocumentMetadataTypeDef]]
    certifiedEmailId: NotRequired[str]
    additionalTaxInformation: NotRequired[AdditionalInfoResponseTypeDef]

class TaxRegistrationWithJurisdictionTypeDef(TypedDict):
    registrationId: str
    registrationType: TaxRegistrationTypeType
    legalName: str
    status: TaxRegistrationStatusType
    jurisdiction: JurisdictionTypeDef
    sector: NotRequired[SectorType]
    taxDocumentMetadatas: NotRequired[list[TaxDocumentMetadataTypeDef]]
    certifiedEmailId: NotRequired[str]
    additionalTaxInformation: NotRequired[AdditionalInfoResponseTypeDef]

class GetTaxExemptionTypesResponseTypeDef(TypedDict):
    taxExemptionTypes: list[TaxExemptionTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TaxExemptionTypeDef(TypedDict):
    authority: AuthorityTypeDef
    taxExemptionType: TaxExemptionTypeTypeDef
    effectiveDate: NotRequired[datetime]
    expirationDate: NotRequired[datetime]
    systemEffectiveDate: NotRequired[datetime]
    status: NotRequired[EntityExemptionAccountStatusType]

class PutTaxExemptionRequestTypeDef(TypedDict):
    accountIds: Sequence[str]
    authority: AuthorityTypeDef
    exemptionType: str
    exemptionCertificate: ExemptionCertificateTypeDef

class TaxRegistrationDocumentTypeDef(TypedDict):
    s3Location: NotRequired[SourceS3LocationTypeDef]
    file: NotRequired[TaxRegistrationDocFileTypeDef]

class AdditionalInfoRequestTypeDef(TypedDict):
    malaysiaAdditionalInfo: NotRequired[MalaysiaAdditionalInfoUnionTypeDef]
    israelAdditionalInfo: NotRequired[IsraelAdditionalInfoTypeDef]
    estoniaAdditionalInfo: NotRequired[EstoniaAdditionalInfoTypeDef]
    canadaAdditionalInfo: NotRequired[CanadaAdditionalInfoTypeDef]
    spainAdditionalInfo: NotRequired[SpainAdditionalInfoTypeDef]
    kenyaAdditionalInfo: NotRequired[KenyaAdditionalInfoTypeDef]
    southKoreaAdditionalInfo: NotRequired[SouthKoreaAdditionalInfoTypeDef]
    turkeyAdditionalInfo: NotRequired[TurkeyAdditionalInfoTypeDef]
    georgiaAdditionalInfo: NotRequired[GeorgiaAdditionalInfoTypeDef]
    italyAdditionalInfo: NotRequired[ItalyAdditionalInfoTypeDef]
    romaniaAdditionalInfo: NotRequired[RomaniaAdditionalInfoTypeDef]
    ukraineAdditionalInfo: NotRequired[UkraineAdditionalInfoTypeDef]
    polandAdditionalInfo: NotRequired[PolandAdditionalInfoTypeDef]
    saudiArabiaAdditionalInfo: NotRequired[SaudiArabiaAdditionalInfoTypeDef]
    indonesiaAdditionalInfo: NotRequired[IndonesiaAdditionalInfoTypeDef]
    vietnamAdditionalInfo: NotRequired[VietnamAdditionalInfoTypeDef]
    egyptAdditionalInfo: NotRequired[EgyptAdditionalInfoTypeDef]
    greeceAdditionalInfo: NotRequired[GreeceAdditionalInfoTypeDef]
    uzbekistanAdditionalInfo: NotRequired[UzbekistanAdditionalInfoTypeDef]
    philippinesAdditionalInfo: NotRequired[PhilippinesAdditionalInfoTypeDef]
    belgiumAdditionalInfo: NotRequired[BelgiumAdditionalInfoTypeDef]
    chileAdditionalInfo: NotRequired[ChileAdditionalInfoTypeDef]
    franceAdditionalInfo: NotRequired[FranceAdditionalInfoTypeDef]

class GetTaxRegistrationResponseTypeDef(TypedDict):
    taxRegistration: TaxRegistrationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class AccountDetailsTypeDef(TypedDict):
    accountId: NotRequired[str]
    taxRegistration: NotRequired[TaxRegistrationWithJurisdictionTypeDef]
    taxInheritanceDetails: NotRequired[TaxInheritanceDetailsTypeDef]
    accountMetaData: NotRequired[AccountMetaDataTypeDef]

class TaxExemptionDetailsTypeDef(TypedDict):
    taxExemptions: NotRequired[list[TaxExemptionTypeDef]]
    heritageObtainedDetails: NotRequired[bool]
    heritageObtainedParentEntity: NotRequired[str]
    heritageObtainedReason: NotRequired[str]

class VerificationDetailsTypeDef(TypedDict):
    dateOfBirth: NotRequired[str]
    taxRegistrationDocuments: NotRequired[Sequence[TaxRegistrationDocumentTypeDef]]

class ListTaxRegistrationsResponseTypeDef(TypedDict):
    accountDetails: list[AccountDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class BatchGetTaxExemptionsResponseTypeDef(TypedDict):
    taxExemptionDetailsMap: dict[str, TaxExemptionDetailsTypeDef]
    failedAccounts: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListTaxExemptionsResponseTypeDef(TypedDict):
    taxExemptionDetailsMap: dict[str, TaxExemptionDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class TaxRegistrationEntryTypeDef(TypedDict):
    registrationId: str
    registrationType: TaxRegistrationTypeType
    legalName: NotRequired[str]
    legalAddress: NotRequired[AddressTypeDef]
    sector: NotRequired[SectorType]
    additionalTaxInformation: NotRequired[AdditionalInfoRequestTypeDef]
    verificationDetails: NotRequired[VerificationDetailsTypeDef]
    certifiedEmailId: NotRequired[str]

class BatchPutTaxRegistrationRequestTypeDef(TypedDict):
    accountIds: Sequence[str]
    taxRegistrationEntry: TaxRegistrationEntryTypeDef

class PutTaxRegistrationRequestTypeDef(TypedDict):
    taxRegistrationEntry: TaxRegistrationEntryTypeDef
    accountId: NotRequired[str]
