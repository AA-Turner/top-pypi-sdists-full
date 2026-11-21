"""
Type annotations for marketplace-discovery service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_discovery/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_marketplace_discovery.type_defs import AmazonMachineImageEbsVolumeTypeDef

    data: AmazonMachineImageEbsVolumeTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from datetime import datetime

from .literals import (
    DeployedOnAwsStatusType,
    DimensionLabelTypeType,
    FulfillmentOptionTypeType,
    LegalDocumentTypeType,
    ListingAttributeTypeType,
    ListingBadgeTypeType,
    PricingModelTypeType,
    PricingUnitTypeType,
    PurchaseIndicatorTypeType,
    PurchaseOptionBadgeTypeType,
    PurchaseOptionFilterTypeType,
    PurchaseOptionTypeType,
    RateCardConstraintTypeType,
    ResourceContentTypeType,
    ResourceTypeType,
    ReviewSourceIdType,
    SaasQuickLaunchStatusType,
    SearchFacetTypeType,
    SearchFilterTypeType,
    SearchListingsSortByType,
    SearchListingsSortOrderType,
    SellerEngagementTypeType,
    SpecializationTypeType,
    TermTypeType,
    TrustCenterControlDomainType,
    TrustCenterDocumentAccessTypeType,
    TrustCenterProviderType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AmazonMachineImageEbsVolumeTypeDef",
    "AmazonMachineImageFulfillmentOptionTypeDef",
    "AmazonMachineImageOperatingSystemTypeDef",
    "AmazonMachineImageRecommendationTypeDef",
    "AmazonMachineImageSecurityGroupTypeDef",
    "ApiFulfillmentOptionTypeDef",
    "AwsSupportedServiceTypeDef",
    "ByolPricingTermTypeDef",
    "CaseStudiesSummaryTypeDef",
    "CaseStudyResourceTypeDef",
    "CaseStudyTypeDef",
    "CategoryTypeDef",
    "CloudFormationFulfillmentOptionTypeDef",
    "ConfigurableUpfrontPricingTermTypeDef",
    "ConfigurableUpfrontRateCardItemTypeDef",
    "ConstraintsTypeDef",
    "ContainerFulfillmentOptionTypeDef",
    "ContainerOperatingSystemTypeDef",
    "DataArtifactTypeDef",
    "DataExchangeFulfillmentOptionTypeDef",
    "DimensionLabelTypeDef",
    "DocumentItemTypeDef",
    "Ec2ImageBuilderComponentFulfillmentOptionTypeDef",
    "EksAddOnFulfillmentOptionTypeDef",
    "EksAddOnOperatingSystemTypeDef",
    "EngagementDatesTypeDef",
    "FixedPercentageTypeDef",
    "FixedUpfrontPricingTermTypeDef",
    "FreeTrialPricingTermTypeDef",
    "FulfillmentOptionSummaryTypeDef",
    "FulfillmentOptionTypeDef",
    "GetListingInputTypeDef",
    "GetListingOutputTypeDef",
    "GetOfferInputTypeDef",
    "GetOfferOutputTypeDef",
    "GetOfferSetInputTypeDef",
    "GetOfferSetOutputTypeDef",
    "GetOfferTermsInputPaginateTypeDef",
    "GetOfferTermsInputTypeDef",
    "GetOfferTermsOutputTypeDef",
    "GetProductInputTypeDef",
    "GetProductOutputTypeDef",
    "GrantItemTypeDef",
    "HelmFulfillmentOptionTypeDef",
    "HelmOperatingSystemTypeDef",
    "LegalTermTypeDef",
    "ListFulfillmentOptionsInputPaginateTypeDef",
    "ListFulfillmentOptionsInputTypeDef",
    "ListFulfillmentOptionsOutputTypeDef",
    "ListListingAttributesInputPaginateTypeDef",
    "ListListingAttributesInputTypeDef",
    "ListListingAttributesOutputTypeDef",
    "ListPurchaseOptionsInputPaginateTypeDef",
    "ListPurchaseOptionsInputTypeDef",
    "ListPurchaseOptionsOutputTypeDef",
    "ListingAssociatedEntityTypeDef",
    "ListingAttributeResultsTypeDef",
    "ListingBadgeTypeDef",
    "ListingFacetTypeDef",
    "ListingSummaryAssociatedEntityTypeDef",
    "ListingSummaryTypeDef",
    "NetPaymentTermTypeDef",
    "OfferAssociatedEntityTypeDef",
    "OfferInformationTypeDef",
    "OfferSetAssociatedEntityTypeDef",
    "OfferSetInformationTypeDef",
    "OfferTermTypeDef",
    "PaginatorConfigTypeDef",
    "PaymentScheduleEntryTypeDef",
    "PaymentScheduleTermTemplateTypeDef",
    "PaymentScheduleTermTypeDef",
    "PercentageRangeTypeDef",
    "PriceIncreaseTypeDef",
    "PricingModelTypeDef",
    "PricingUnitTypeDef",
    "ProductInformationTypeDef",
    "ProfessionalServicesFulfillmentOptionTypeDef",
    "PromotionalEmbeddedImageTypeDef",
    "PromotionalEmbeddedVideoTypeDef",
    "PromotionalMediaTypeDef",
    "PurchaseIndicatorTypeDef",
    "PurchaseOptionAssociatedEntityTypeDef",
    "PurchaseOptionBadgeTypeDef",
    "PurchaseOptionFilterTypeDef",
    "PurchaseOptionSummaryTypeDef",
    "RateCardItemTypeDef",
    "RecurringPaymentTermTypeDef",
    "RegionalPriceTypeDef",
    "RenewalTermTypeDef",
    "ResourceTypeDef",
    "ResponseMetadataTypeDef",
    "ReviewSourceSummaryTypeDef",
    "ReviewSummaryTypeDef",
    "SaasCloudFormationDeploymentTemplateTypeDef",
    "SaasDeploymentTemplateTypeDef",
    "SaasFulfillmentOptionTypeDef",
    "SageMakerAlgorithmFulfillmentOptionTypeDef",
    "SageMakerAlgorithmRecommendationTypeDef",
    "SageMakerModelFulfillmentOptionTypeDef",
    "SageMakerModelRecommendationTypeDef",
    "ScheduleItemTypeDef",
    "SearchFacetsInputPaginateTypeDef",
    "SearchFacetsInputTypeDef",
    "SearchFacetsOutputTypeDef",
    "SearchFilterTypeDef",
    "SearchListingsInputPaginateTypeDef",
    "SearchListingsInputTypeDef",
    "SearchListingsOutputTypeDef",
    "SelectorTypeDef",
    "SellerEngagementTypeDef",
    "SellerInformationTypeDef",
    "SpecializationCategoryTypeDef",
    "SpecializationDetailTypeDef",
    "SpecializationTypeDef",
    "SpecializationTypeDetailTypeDef",
    "SupportTermTypeDef",
    "TermTemplateTypeDef",
    "TrustCenterCertificationAttributeTypeDef",
    "TrustCenterCertificationSummaryTypeDef",
    "TrustCenterControlTypeDef",
    "TrustCenterDocumentAttributeTypeDef",
    "TrustCenterFaqAttributeTypeDef",
    "TrustCenterSourceSummaryTypeDef",
    "TrustCenterSourceTypeDef",
    "TrustCenterSummaryTypeDef",
    "TrustCenterUpdateAttributeTypeDef",
    "UsageBasedPricingTermTypeDef",
    "UsageBasedRateCardItemTypeDef",
    "UseCaseEntryTypeDef",
    "UseCaseInformationTypeDef",
    "UseCaseSummaryEntryTypeDef",
    "UseCaseSummaryTypeDef",
    "UseCaseTypeDef",
    "ValidityTermTypeDef",
    "VariablePaymentTermTypeDef",
)

class AmazonMachineImageEbsVolumeTypeDef(TypedDict):
    volumeTypes: list[str]
    iops: NotRequired[int]

class AmazonMachineImageOperatingSystemTypeDef(TypedDict):
    operatingSystemFamilyName: str
    operatingSystemName: str
    operatingSystemVersion: NotRequired[str]

class AmazonMachineImageSecurityGroupTypeDef(TypedDict):
    protocol: str
    fromPort: int
    toPort: int
    cidrIpAddresses: list[str]

class AwsSupportedServiceTypeDef(TypedDict):
    supportedServiceType: str
    displayName: str
    description: str

ByolPricingTermTypeDef = TypedDict(
    "ByolPricingTermTypeDef",
    {
        "id": str,
        "type": TermTypeType,
    },
)

class CaseStudiesSummaryTypeDef(TypedDict):
    caseStudyCount: int

class CaseStudyResourceTypeDef(TypedDict):
    contentType: ResourceContentTypeType
    value: str
    resourceType: Literal["CASE_STUDY_WEBSITE"]
    displayName: NotRequired[str]

class EngagementDatesTypeDef(TypedDict):
    startDate: datetime
    completionDate: NotRequired[datetime]

class CategoryTypeDef(TypedDict):
    categoryId: str
    displayName: str

class CloudFormationFulfillmentOptionTypeDef(TypedDict):
    fulfillmentOptionId: str
    fulfillmentOptionName: str
    fulfillmentOptionType: FulfillmentOptionTypeType
    fulfillmentOptionDisplayName: str
    fulfillmentOptionVersion: NotRequired[str]
    releaseNotes: NotRequired[str]
    usageInstructions: NotRequired[str]
    availableFromTime: NotRequired[datetime]
    architectureDiagramUrl: NotRequired[str]
    deploymentTemplateUrl: NotRequired[str]
    shortDescription: NotRequired[str]
    longDescription: NotRequired[str]

class ConstraintsTypeDef(TypedDict):
    multipleDimensionSelection: RateCardConstraintTypeType
    quantityConfiguration: RateCardConstraintTypeType

SelectorTypeDef = TypedDict(
    "SelectorTypeDef",
    {
        "type": Literal["Duration"],
        "value": str,
    },
)

class ContainerOperatingSystemTypeDef(TypedDict):
    operatingSystemFamilyName: str
    operatingSystemName: str

class DataArtifactTypeDef(TypedDict):
    resourceType: str
    dataClassification: str
    description: NotRequired[str]
    resourceArn: NotRequired[str]

class DimensionLabelTypeDef(TypedDict):
    labelType: DimensionLabelTypeType
    labelValue: str
    displayName: NotRequired[str]

DocumentItemTypeDef = TypedDict(
    "DocumentItemTypeDef",
    {
        "type": LegalDocumentTypeType,
        "url": str,
        "version": NotRequired[str],
    },
)

class EksAddOnOperatingSystemTypeDef(TypedDict):
    operatingSystemFamilyName: str
    operatingSystemName: str

class FixedPercentageTypeDef(TypedDict):
    percentageValue: str

class FulfillmentOptionSummaryTypeDef(TypedDict):
    fulfillmentOptionType: FulfillmentOptionTypeType
    displayName: str

class ProfessionalServicesFulfillmentOptionTypeDef(TypedDict):
    fulfillmentOptionId: str
    fulfillmentOptionType: FulfillmentOptionTypeType
    fulfillmentOptionDisplayName: str

class GetListingInputTypeDef(TypedDict):
    listingId: str
    locale: NotRequired[str]

class ListingBadgeTypeDef(TypedDict):
    displayName: str
    badgeType: ListingBadgeTypeType

class PricingModelTypeDef(TypedDict):
    pricingModelType: PricingModelTypeType
    displayName: str

class PricingUnitTypeDef(TypedDict):
    pricingUnitType: PricingUnitTypeType
    displayName: str

class PurchaseIndicatorTypeDef(TypedDict):
    indicatorType: PurchaseIndicatorTypeType

class ResourceTypeDef(TypedDict):
    resourceType: ResourceTypeType
    contentType: ResourceContentTypeType
    value: str
    displayName: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class SellerEngagementTypeDef(TypedDict):
    engagementType: SellerEngagementTypeType
    contentType: Literal["LINK"]
    value: str

class SellerInformationTypeDef(TypedDict):
    sellerProfileId: str
    displayName: str

class GetOfferInputTypeDef(TypedDict):
    offerId: str
    locale: NotRequired[str]

class PurchaseOptionBadgeTypeDef(TypedDict):
    displayName: str
    badgeType: PurchaseOptionBadgeTypeType

class GetOfferSetInputTypeDef(TypedDict):
    offerSetId: str
    locale: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class GetOfferTermsInputTypeDef(TypedDict):
    offerId: str
    locale: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class GetProductInputTypeDef(TypedDict):
    productId: str
    locale: NotRequired[str]

class HelmOperatingSystemTypeDef(TypedDict):
    operatingSystemFamilyName: str
    operatingSystemName: str

class ListFulfillmentOptionsInputTypeDef(TypedDict):
    productId: str
    locale: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListListingAttributesInputTypeDef(TypedDict):
    listingId: str
    attributeTypes: Sequence[ListingAttributeTypeType]
    locale: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class PurchaseOptionFilterTypeDef(TypedDict):
    filterType: PurchaseOptionFilterTypeType
    filterValues: Sequence[str]

class TrustCenterCertificationAttributeTypeDef(TypedDict):
    certificationType: str
    displayName: str
    logoUrl: str

class TrustCenterControlTypeDef(TypedDict):
    name: str
    domains: list[TrustCenterControlDomainType]
    description: NotRequired[str]

class TrustCenterDocumentAttributeTypeDef(TypedDict):
    contentType: ResourceContentTypeType
    value: str
    accessType: TrustCenterDocumentAccessTypeType
    displayName: NotRequired[str]
    subjectArea: NotRequired[str]

class TrustCenterFaqAttributeTypeDef(TypedDict):
    question: str
    answer: str
    subjectArea: NotRequired[str]

class TrustCenterSourceTypeDef(TypedDict):
    contentType: ResourceContentTypeType
    value: str
    provider: TrustCenterProviderType
    displayName: NotRequired[str]

class TrustCenterUpdateAttributeTypeDef(TypedDict):
    title: str
    description: str
    publishedTime: datetime

class ListingFacetTypeDef(TypedDict):
    value: str
    displayName: str
    count: int
    parent: NotRequired[str]

NetPaymentTermTypeDef = TypedDict(
    "NetPaymentTermTypeDef",
    {
        "id": str,
        "type": TermTypeType,
        "paymentDuePeriod": str,
    },
)
RecurringPaymentTermTypeDef = TypedDict(
    "RecurringPaymentTermTypeDef",
    {
        "id": str,
        "type": TermTypeType,
        "currencyCode": str,
        "billingPeriod": Literal["Monthly"],
        "price": str,
    },
)
SupportTermTypeDef = TypedDict(
    "SupportTermTypeDef",
    {
        "id": str,
        "type": TermTypeType,
        "refundPolicy": str,
    },
)
ValidityTermTypeDef = TypedDict(
    "ValidityTermTypeDef",
    {
        "id": str,
        "type": TermTypeType,
        "agreementDuration": NotRequired[str],
        "agreementEndDate": NotRequired[datetime],
        "agreementStartDate": NotRequired[datetime],
    },
)
VariablePaymentTermTypeDef = TypedDict(
    "VariablePaymentTermTypeDef",
    {
        "id": str,
        "type": TermTypeType,
        "currencyCode": str,
        "maxTotalChargeAmount": str,
    },
)

class PaymentScheduleEntryTypeDef(TypedDict):
    chargeDateOffset: str
    chargePercentage: str
    dayOfMonth: NotRequired[int]

class ScheduleItemTypeDef(TypedDict):
    chargeDate: datetime
    chargeAmount: str

class PercentageRangeTypeDef(TypedDict):
    minimumValue: str
    maximumValue: str
    defaultValue: str

class PromotionalEmbeddedImageTypeDef(TypedDict):
    title: str
    url: str
    description: NotRequired[str]

class PromotionalEmbeddedVideoTypeDef(TypedDict):
    title: str
    url: str
    preview: str
    thumbnail: str
    description: NotRequired[str]

class RegionalPriceTypeDef(TypedDict):
    region: str
    displayName: str
    price: str

class ReviewSourceSummaryTypeDef(TypedDict):
    sourceName: str
    sourceId: ReviewSourceIdType
    averageRating: str
    totalReviews: int
    sourceUrl: NotRequired[str]

class SaasCloudFormationDeploymentTemplateTypeDef(TypedDict):
    templateName: str
    defaultStackName: str
    templateUrl: str
    iamPolicy: str
    description: NotRequired[str]

class SageMakerAlgorithmRecommendationTypeDef(TypedDict):
    recommendedBatchTransformInstanceType: str
    recommendedTrainingInstanceType: str
    recommendedRealtimeInferenceInstanceType: NotRequired[str]

class SageMakerModelRecommendationTypeDef(TypedDict):
    recommendedBatchTransformInstanceType: str
    recommendedRealtimeInferenceInstanceType: NotRequired[str]

class SearchFilterTypeDef(TypedDict):
    filterType: SearchFilterTypeType
    filterValues: Sequence[str]

class SpecializationCategoryTypeDef(TypedDict):
    specializationCategoryId: str
    specializationCategoryName: str
    parentSpecializationId: str

class SpecializationTypeDetailTypeDef(TypedDict):
    specializationType: SpecializationTypeType
    displayName: str

class TrustCenterCertificationSummaryTypeDef(TypedDict):
    certificationType: str
    displayName: str
    logoUrl: str

class TrustCenterSourceSummaryTypeDef(TypedDict):
    contentType: ResourceContentTypeType
    value: str
    provider: TrustCenterProviderType
    displayName: NotRequired[str]

class UseCaseTypeDef(TypedDict):
    description: str
    displayName: str
    value: str

class UseCaseInformationTypeDef(TypedDict):
    displayName: str
    value: str

class AmazonMachineImageRecommendationTypeDef(TypedDict):
    instanceType: str
    securityGroups: NotRequired[list[AmazonMachineImageSecurityGroupTypeDef]]

class ApiFulfillmentOptionTypeDef(TypedDict):
    fulfillmentOptionId: str
    fulfillmentOptionType: FulfillmentOptionTypeType
    fulfillmentOptionDisplayName: str
    awsSupportedServices: list[AwsSupportedServiceTypeDef]
    usageInstructions: NotRequired[str]

class CaseStudyTypeDef(TypedDict):
    caseStudyId: str
    caseStudyName: str
    shortDescription: str
    engagementDates: NotRequired[EngagementDatesTypeDef]
    challenge: NotRequired[str]
    resolution: NotRequired[str]
    implementationApproach: NotRequired[str]
    outcome: NotRequired[str]
    resources: NotRequired[list[CaseStudyResourceTypeDef]]

class ContainerFulfillmentOptionTypeDef(TypedDict):
    fulfillmentOptionId: str
    fulfillmentOptionName: str
    fulfillmentOptionType: FulfillmentOptionTypeType
    fulfillmentOptionDisplayName: str
    fulfillmentOptionVersion: NotRequired[str]
    operatingSystems: NotRequired[list[ContainerOperatingSystemTypeDef]]
    awsSupportedServices: NotRequired[list[AwsSupportedServiceTypeDef]]
    releaseNotes: NotRequired[str]
    usageInstructions: NotRequired[str]

class Ec2ImageBuilderComponentFulfillmentOptionTypeDef(TypedDict):
    fulfillmentOptionId: str
    fulfillmentOptionName: str
    fulfillmentOptionType: FulfillmentOptionTypeType
    fulfillmentOptionDisplayName: str
    fulfillmentOptionVersion: NotRequired[str]
    operatingSystems: NotRequired[list[ContainerOperatingSystemTypeDef]]
    awsSupportedServices: NotRequired[list[AwsSupportedServiceTypeDef]]
    releaseNotes: NotRequired[str]
    usageInstructions: NotRequired[str]

class DataExchangeFulfillmentOptionTypeDef(TypedDict):
    fulfillmentOptionId: str
    fulfillmentOptionType: FulfillmentOptionTypeType
    fulfillmentOptionDisplayName: str
    dataArtifacts: NotRequired[list[DataArtifactTypeDef]]

class GrantItemTypeDef(TypedDict):
    dimensionKey: str
    displayName: str
    unit: str
    description: NotRequired[str]
    dimensionLabels: NotRequired[list[DimensionLabelTypeDef]]
    maxQuantity: NotRequired[int]

LegalTermTypeDef = TypedDict(
    "LegalTermTypeDef",
    {
        "id": str,
        "type": TermTypeType,
        "documents": list[DocumentItemTypeDef],
    },
)

class EksAddOnFulfillmentOptionTypeDef(TypedDict):
    fulfillmentOptionId: str
    fulfillmentOptionName: str
    fulfillmentOptionType: FulfillmentOptionTypeType
    fulfillmentOptionDisplayName: str
    fulfillmentOptionVersion: NotRequired[str]
    operatingSystems: NotRequired[list[EksAddOnOperatingSystemTypeDef]]
    releaseNotes: NotRequired[str]
    usageInstructions: NotRequired[str]
    awsSupportedServices: NotRequired[list[AwsSupportedServiceTypeDef]]

class OfferInformationTypeDef(TypedDict):
    offerId: str
    sellerOfRecord: SellerInformationTypeDef
    offerName: NotRequired[str]

class OfferSetInformationTypeDef(TypedDict):
    offerSetId: str
    sellerOfRecord: SellerInformationTypeDef

class ProductInformationTypeDef(TypedDict):
    productId: str
    productName: str
    manufacturer: SellerInformationTypeDef

class GetOfferTermsInputPaginateTypeDef(TypedDict):
    offerId: str
    locale: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListFulfillmentOptionsInputPaginateTypeDef(TypedDict):
    productId: str
    locale: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListListingAttributesInputPaginateTypeDef(TypedDict):
    listingId: str
    attributeTypes: Sequence[ListingAttributeTypeType]
    locale: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class HelmFulfillmentOptionTypeDef(TypedDict):
    fulfillmentOptionId: str
    fulfillmentOptionName: str
    fulfillmentOptionType: FulfillmentOptionTypeType
    fulfillmentOptionDisplayName: str
    fulfillmentOptionVersion: NotRequired[str]
    operatingSystems: NotRequired[list[HelmOperatingSystemTypeDef]]
    releaseNotes: NotRequired[str]
    awsSupportedServices: NotRequired[list[AwsSupportedServiceTypeDef]]
    usageInstructions: NotRequired[str]

class ListPurchaseOptionsInputPaginateTypeDef(TypedDict):
    locale: NotRequired[str]
    filters: NotRequired[Sequence[PurchaseOptionFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPurchaseOptionsInputTypeDef(TypedDict):
    locale: NotRequired[str]
    filters: NotRequired[Sequence[PurchaseOptionFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class SearchFacetsOutputTypeDef(TypedDict):
    totalResults: int
    listingFacets: dict[SearchFacetTypeType, list[ListingFacetTypeDef]]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class PaymentScheduleTermTemplateTypeDef(TypedDict):
    schedule: list[PaymentScheduleEntryTypeDef]

PaymentScheduleTermTypeDef = TypedDict(
    "PaymentScheduleTermTypeDef",
    {
        "id": str,
        "type": TermTypeType,
        "currencyCode": str,
        "schedule": list[ScheduleItemTypeDef],
    },
)

class PriceIncreaseTypeDef(TypedDict):
    fixedPercentage: NotRequired[FixedPercentageTypeDef]
    percentageRange: NotRequired[PercentageRangeTypeDef]

class PromotionalMediaTypeDef(TypedDict):
    embeddedImage: NotRequired[PromotionalEmbeddedImageTypeDef]
    embeddedVideo: NotRequired[PromotionalEmbeddedVideoTypeDef]

class RateCardItemTypeDef(TypedDict):
    dimensionKey: str
    displayName: str
    unit: str
    price: str
    regionalPrices: list[RegionalPriceTypeDef]
    description: NotRequired[str]
    dimensionLabels: NotRequired[list[DimensionLabelTypeDef]]

class ReviewSummaryTypeDef(TypedDict):
    reviewSourceSummaries: list[ReviewSourceSummaryTypeDef]

class SaasDeploymentTemplateTypeDef(TypedDict):
    cloudFormationDeploymentTemplate: NotRequired[SaasCloudFormationDeploymentTemplateTypeDef]

class SageMakerAlgorithmFulfillmentOptionTypeDef(TypedDict):
    fulfillmentOptionId: str
    fulfillmentOptionType: FulfillmentOptionTypeType
    fulfillmentOptionDisplayName: str
    fulfillmentOptionVersion: NotRequired[str]
    releaseNotes: NotRequired[str]
    usageInstructions: NotRequired[str]
    recommendation: NotRequired[SageMakerAlgorithmRecommendationTypeDef]

class SageMakerModelFulfillmentOptionTypeDef(TypedDict):
    fulfillmentOptionId: str
    fulfillmentOptionType: FulfillmentOptionTypeType
    fulfillmentOptionDisplayName: str
    fulfillmentOptionVersion: NotRequired[str]
    releaseNotes: NotRequired[str]
    usageInstructions: NotRequired[str]
    recommendation: NotRequired[SageMakerModelRecommendationTypeDef]
    supportedContentTypes: NotRequired[list[str]]
    supportedResponseMimeTypes: NotRequired[list[str]]

class SearchFacetsInputPaginateTypeDef(TypedDict):
    locale: NotRequired[str]
    searchText: NotRequired[str]
    filters: NotRequired[Sequence[SearchFilterTypeDef]]
    facetTypes: NotRequired[Sequence[SearchFacetTypeType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchFacetsInputTypeDef(TypedDict):
    locale: NotRequired[str]
    searchText: NotRequired[str]
    filters: NotRequired[Sequence[SearchFilterTypeDef]]
    facetTypes: NotRequired[Sequence[SearchFacetTypeType]]
    nextToken: NotRequired[str]

class SearchListingsInputPaginateTypeDef(TypedDict):
    locale: NotRequired[str]
    searchText: NotRequired[str]
    filters: NotRequired[Sequence[SearchFilterTypeDef]]
    sortBy: NotRequired[SearchListingsSortByType]
    sortOrder: NotRequired[SearchListingsSortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchListingsInputTypeDef(TypedDict):
    locale: NotRequired[str]
    searchText: NotRequired[str]
    filters: NotRequired[Sequence[SearchFilterTypeDef]]
    maxResults: NotRequired[int]
    sortBy: NotRequired[SearchListingsSortByType]
    sortOrder: NotRequired[SearchListingsSortOrderType]
    nextToken: NotRequired[str]

class SpecializationTypeDef(TypedDict):
    specializationId: str
    specializationName: str
    specializationTypes: list[SpecializationTypeDetailTypeDef]
    description: NotRequired[str]
    caseStudyIds: NotRequired[list[str]]

class TrustCenterSummaryTypeDef(TypedDict):
    sourceSummaries: list[TrustCenterSourceSummaryTypeDef]
    certificationSummaries: list[TrustCenterCertificationSummaryTypeDef]
    totalCertificationCount: int

class UseCaseEntryTypeDef(TypedDict):
    useCase: UseCaseTypeDef

class UseCaseSummaryEntryTypeDef(TypedDict):
    useCase: UseCaseInformationTypeDef

class AmazonMachineImageFulfillmentOptionTypeDef(TypedDict):
    fulfillmentOptionId: str
    fulfillmentOptionName: str
    fulfillmentOptionType: FulfillmentOptionTypeType
    fulfillmentOptionDisplayName: str
    operatingSystems: list[AmazonMachineImageOperatingSystemTypeDef]
    architecture: str
    fulfillmentOptionVersion: NotRequired[str]
    recommendation: NotRequired[AmazonMachineImageRecommendationTypeDef]
    releaseNotes: NotRequired[str]
    usageInstructions: NotRequired[str]
    availableFromTime: NotRequired[datetime]
    accessUrlTemplate: NotRequired[str]
    amiAlias: NotRequired[str]
    ebsVolume: NotRequired[AmazonMachineImageEbsVolumeTypeDef]
    shortDescription: NotRequired[str]

FixedUpfrontPricingTermTypeDef = TypedDict(
    "FixedUpfrontPricingTermTypeDef",
    {
        "id": str,
        "type": TermTypeType,
        "currencyCode": str,
        "price": str,
        "grants": list[GrantItemTypeDef],
        "duration": NotRequired[str],
    },
)
FreeTrialPricingTermTypeDef = TypedDict(
    "FreeTrialPricingTermTypeDef",
    {
        "id": str,
        "type": TermTypeType,
        "grants": list[GrantItemTypeDef],
        "duration": NotRequired[str],
    },
)

class ListingAssociatedEntityTypeDef(TypedDict):
    product: NotRequired[ProductInformationTypeDef]
    offer: NotRequired[OfferInformationTypeDef]

class ListingSummaryAssociatedEntityTypeDef(TypedDict):
    product: NotRequired[ProductInformationTypeDef]

class OfferAssociatedEntityTypeDef(TypedDict):
    product: ProductInformationTypeDef
    offerSet: NotRequired[OfferSetInformationTypeDef]

class OfferSetAssociatedEntityTypeDef(TypedDict):
    product: ProductInformationTypeDef
    offer: OfferInformationTypeDef

class PurchaseOptionAssociatedEntityTypeDef(TypedDict):
    product: ProductInformationTypeDef
    offer: OfferInformationTypeDef
    offerSet: NotRequired[OfferSetInformationTypeDef]

class TermTemplateTypeDef(TypedDict):
    paymentScheduleTermTemplate: NotRequired[PaymentScheduleTermTemplateTypeDef]

class GetProductOutputTypeDef(TypedDict):
    locale: str
    productId: str
    catalog: str
    productName: str
    manufacturer: SellerInformationTypeDef
    deployedOnAws: DeployedOnAwsStatusType
    shortDescription: str
    longDescription: str
    logoThumbnailUrl: str
    fulfillmentOptionSummaries: list[FulfillmentOptionSummaryTypeDef]
    categories: list[CategoryTypeDef]
    highlights: list[str]
    promotionalMedia: list[PromotionalMediaTypeDef]
    resources: list[ResourceTypeDef]
    sellerEngagements: list[SellerEngagementTypeDef]
    listingId: str
    purchaseIndicators: list[PurchaseIndicatorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ConfigurableUpfrontRateCardItemTypeDef(TypedDict):
    selector: SelectorTypeDef
    constraints: ConstraintsTypeDef
    rateCard: list[RateCardItemTypeDef]

class UsageBasedRateCardItemTypeDef(TypedDict):
    rateCard: list[RateCardItemTypeDef]

class SaasFulfillmentOptionTypeDef(TypedDict):
    fulfillmentOptionId: str
    fulfillmentOptionType: FulfillmentOptionTypeType
    fulfillmentOptionDisplayName: str
    quickLaunch: SaasQuickLaunchStatusType
    deploymentTemplates: list[SaasDeploymentTemplateTypeDef]
    fulfillmentUrl: NotRequired[str]
    usageInstructions: NotRequired[str]
    availableFromTime: NotRequired[datetime]
    launchUrl: NotRequired[str]

class SpecializationDetailTypeDef(TypedDict):
    specialization: NotRequired[SpecializationTypeDef]
    specializationCategory: NotRequired[SpecializationCategoryTypeDef]

class UseCaseSummaryTypeDef(TypedDict):
    useCases: list[UseCaseSummaryEntryTypeDef]

class GetListingOutputTypeDef(TypedDict):
    locale: str
    associatedEntities: list[ListingAssociatedEntityTypeDef]
    badges: list[ListingBadgeTypeDef]
    catalog: str
    categories: list[CategoryTypeDef]
    fulfillmentOptionSummaries: list[FulfillmentOptionSummaryTypeDef]
    highlights: list[str]
    integrationGuide: str
    listingId: str
    listingName: str
    logoThumbnailUrl: str
    longDescription: str
    pricingModels: list[PricingModelTypeDef]
    pricingUnits: list[PricingUnitTypeDef]
    promotionalMedia: list[PromotionalMediaTypeDef]
    publisher: SellerInformationTypeDef
    resources: list[ResourceTypeDef]
    reviewSummary: ReviewSummaryTypeDef
    sellerEngagements: list[SellerEngagementTypeDef]
    shortDescription: str
    useCases: list[UseCaseEntryTypeDef]
    purchaseIndicators: list[PurchaseIndicatorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetOfferOutputTypeDef(TypedDict):
    locale: str
    offerId: str
    catalog: str
    offerName: str
    expirationTime: datetime
    availableFromTime: datetime
    sellerOfRecord: SellerInformationTypeDef
    associatedEntities: list[OfferAssociatedEntityTypeDef]
    agreementProposalId: str
    replacementAgreementId: str
    pricingModel: PricingModelTypeDef
    badges: list[PurchaseOptionBadgeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetOfferSetOutputTypeDef(TypedDict):
    locale: str
    offerSetId: str
    catalog: str
    offerSetName: str
    availableFromTime: datetime
    expirationTime: datetime
    buyerNotes: str
    sellerOfRecord: SellerInformationTypeDef
    badges: list[PurchaseOptionBadgeTypeDef]
    associatedEntities: list[OfferSetAssociatedEntityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class PurchaseOptionSummaryTypeDef(TypedDict):
    purchaseOptionId: str
    catalog: str
    purchaseOptionType: PurchaseOptionTypeType
    sellerOfRecord: SellerInformationTypeDef
    associatedEntities: list[PurchaseOptionAssociatedEntityTypeDef]
    purchaseOptionName: NotRequired[str]
    availableFromTime: NotRequired[datetime]
    expirationTime: NotRequired[datetime]
    badges: NotRequired[list[PurchaseOptionBadgeTypeDef]]

RenewalTermTypeDef = TypedDict(
    "RenewalTermTypeDef",
    {
        "id": str,
        "type": TermTypeType,
        "maxRenewals": NotRequired[int],
        "lockoutPeriod": NotRequired[str],
        "adjustmentDeadline": NotRequired[str],
        "priceIncrease": NotRequired[PriceIncreaseTypeDef],
        "termTemplates": NotRequired[list[TermTemplateTypeDef]],
    },
)
ConfigurableUpfrontPricingTermTypeDef = TypedDict(
    "ConfigurableUpfrontPricingTermTypeDef",
    {
        "id": str,
        "type": TermTypeType,
        "currencyCode": str,
        "rateCards": NotRequired[list[ConfigurableUpfrontRateCardItemTypeDef]],
    },
)
UsageBasedPricingTermTypeDef = TypedDict(
    "UsageBasedPricingTermTypeDef",
    {
        "id": str,
        "type": TermTypeType,
        "currencyCode": str,
        "rateCards": list[UsageBasedRateCardItemTypeDef],
    },
)

class FulfillmentOptionTypeDef(TypedDict):
    amazonMachineImageFulfillmentOption: NotRequired[AmazonMachineImageFulfillmentOptionTypeDef]
    apiFulfillmentOption: NotRequired[ApiFulfillmentOptionTypeDef]
    cloudFormationFulfillmentOption: NotRequired[CloudFormationFulfillmentOptionTypeDef]
    containerFulfillmentOption: NotRequired[ContainerFulfillmentOptionTypeDef]
    helmFulfillmentOption: NotRequired[HelmFulfillmentOptionTypeDef]
    eksAddOnFulfillmentOption: NotRequired[EksAddOnFulfillmentOptionTypeDef]
    ec2ImageBuilderComponentFulfillmentOption: NotRequired[
        Ec2ImageBuilderComponentFulfillmentOptionTypeDef
    ]
    dataExchangeFulfillmentOption: NotRequired[DataExchangeFulfillmentOptionTypeDef]
    professionalServicesFulfillmentOption: NotRequired[ProfessionalServicesFulfillmentOptionTypeDef]
    saasFulfillmentOption: NotRequired[SaasFulfillmentOptionTypeDef]
    sageMakerAlgorithmFulfillmentOption: NotRequired[SageMakerAlgorithmFulfillmentOptionTypeDef]
    sageMakerModelFulfillmentOption: NotRequired[SageMakerModelFulfillmentOptionTypeDef]

class ListingAttributeResultsTypeDef(TypedDict):
    caseStudy: NotRequired[CaseStudyTypeDef]
    specializationDetail: NotRequired[SpecializationDetailTypeDef]
    trustCenterSource: NotRequired[TrustCenterSourceTypeDef]
    trustCenterCertification: NotRequired[TrustCenterCertificationAttributeTypeDef]
    trustCenterDocument: NotRequired[TrustCenterDocumentAttributeTypeDef]
    trustCenterControl: NotRequired[TrustCenterControlTypeDef]
    trustCenterFaq: NotRequired[TrustCenterFaqAttributeTypeDef]
    trustCenterUpdate: NotRequired[TrustCenterUpdateAttributeTypeDef]

class ListingSummaryTypeDef(TypedDict):
    listingId: str
    listingName: str
    publisher: SellerInformationTypeDef
    fulfillmentOptionSummaries: list[FulfillmentOptionSummaryTypeDef]
    catalog: str
    shortDescription: str
    logoThumbnailUrl: str
    categories: list[CategoryTypeDef]
    badges: list[ListingBadgeTypeDef]
    reviewSummary: ReviewSummaryTypeDef
    pricingModels: list[PricingModelTypeDef]
    pricingUnits: list[PricingUnitTypeDef]
    associatedEntities: list[ListingSummaryAssociatedEntityTypeDef]
    trustCenterSummary: NotRequired[TrustCenterSummaryTypeDef]
    caseStudiesSummary: NotRequired[CaseStudiesSummaryTypeDef]
    useCaseSummary: NotRequired[UseCaseSummaryTypeDef]
    sellerEngagements: NotRequired[list[SellerEngagementTypeDef]]

class ListPurchaseOptionsOutputTypeDef(TypedDict):
    purchaseOptions: list[PurchaseOptionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class OfferTermTypeDef(TypedDict):
    byolPricingTerm: NotRequired[ByolPricingTermTypeDef]
    configurableUpfrontPricingTerm: NotRequired[ConfigurableUpfrontPricingTermTypeDef]
    fixedUpfrontPricingTerm: NotRequired[FixedUpfrontPricingTermTypeDef]
    freeTrialPricingTerm: NotRequired[FreeTrialPricingTermTypeDef]
    legalTerm: NotRequired[LegalTermTypeDef]
    paymentScheduleTerm: NotRequired[PaymentScheduleTermTypeDef]
    recurringPaymentTerm: NotRequired[RecurringPaymentTermTypeDef]
    renewalTerm: NotRequired[RenewalTermTypeDef]
    supportTerm: NotRequired[SupportTermTypeDef]
    usageBasedPricingTerm: NotRequired[UsageBasedPricingTermTypeDef]
    validityTerm: NotRequired[ValidityTermTypeDef]
    variablePaymentTerm: NotRequired[VariablePaymentTermTypeDef]
    netPaymentTerm: NotRequired[NetPaymentTermTypeDef]

class ListFulfillmentOptionsOutputTypeDef(TypedDict):
    locale: str
    fulfillmentOptions: list[FulfillmentOptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListListingAttributesOutputTypeDef(TypedDict):
    locale: str
    listingAttributes: list[ListingAttributeResultsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class SearchListingsOutputTypeDef(TypedDict):
    totalResults: int
    listingSummaries: list[ListingSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetOfferTermsOutputTypeDef(TypedDict):
    locale: str
    offerTerms: list[OfferTermTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
