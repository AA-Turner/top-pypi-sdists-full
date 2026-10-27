"""
Type annotations for billing service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_billing.type_defs import TimestampTypeDef

    data: TimestampTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from datetime import datetime
from typing import Union

from .literals import (
    ApplicationTypeType,
    AssociationStatusType,
    BillingDomainType,
    BillingFeatureType,
    BillingViewStatusReasonType,
    BillingViewStatusType,
    BillingViewTypeType,
    ContractTypeType,
    CreditSharingTypeType,
    CreditStatusType,
    InvestmentAttestationStatusType,
    InvestmentTypeType,
    MultiplierTypeType,
    PreferenceValueType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "ActiveTimeRangeTypeDef",
    "AdditionalChargeTypeDef",
    "AdditionalRecipientTypeDef",
    "AmountTypeDef",
    "ApproverDetailsTypeDef",
    "AssociateContractRequestTypeDef",
    "AssociateSourceViewsRequestTypeDef",
    "AssociateSourceViewsResponseTypeDef",
    "AttestationDetailsTypeDef",
    "AttestationQuantityTypeDef",
    "AttestationValueTypeDef",
    "BillingFeatureFilterTypeDef",
    "BillingPeriodTypeDef",
    "BillingPreferenceForKeyTypeDef",
    "BillingPreferenceSummaryTypeDef",
    "BillingViewElementTypeDef",
    "BillingViewHealthStatusTypeDef",
    "BillingViewListElementTypeDef",
    "BillingViewSegmentTimeRangeOutputTypeDef",
    "BillingViewSegmentTimeRangeTypeDef",
    "BillingViewSegmentTimeRangeUnionTypeDef",
    "BillingViewSegmentsListElementTypeDef",
    "BusinessSupportAccountChargeTypeDef",
    "BusinessSupportDiscountTypeDef",
    "BusinessSupportServiceSpendTypeDef",
    "BusinessSupportSubscriptionContractTypeDef",
    "BusinessSupportTierChargeTypeDef",
    "CancelContractualInvestmentAttestationRequestTypeDef",
    "ChargeAccountTypeDef",
    "ContractAccountTypeDef",
    "ContractDetailsTypeDef",
    "ContractSummaryTypeDef",
    "CostCategoryValuesOutputTypeDef",
    "CostCategoryValuesTypeDef",
    "CreateBillingViewRequestTypeDef",
    "CreateBillingViewResponseTypeDef",
    "CreateContractualInvestmentAttestationRequestTypeDef",
    "CreateContractualInvestmentAttestationResponseTypeDef",
    "CreditAllocationHistoryEntryTypeDef",
    "CreditDataTypeDef",
    "DeleteBillingViewRequestTypeDef",
    "DeleteBillingViewResponseTypeDef",
    "DimensionValuesOutputTypeDef",
    "DimensionValuesTypeDef",
    "DisassociateContractRequestTypeDef",
    "DisassociateSourceViewsRequestTypeDef",
    "DisassociateSourceViewsResponseTypeDef",
    "EnterpriseSupportTimePeriodTypeDef",
    "ExpressionOutputTypeDef",
    "ExpressionTypeDef",
    "ExpressionUnionTypeDef",
    "GetBillingPreferencesRequestTypeDef",
    "GetBillingPreferencesResponseTypeDef",
    "GetBillingViewRequestTypeDef",
    "GetBillingViewResponseTypeDef",
    "GetContractInformationRequestTypeDef",
    "GetContractInformationResponseTypeDef",
    "GetCreditAllocationHistoryRequestPaginateTypeDef",
    "GetCreditAllocationHistoryRequestTypeDef",
    "GetCreditAllocationHistoryResponseTypeDef",
    "GetCreditsRequestTypeDef",
    "GetCreditsResponseTypeDef",
    "GetEnterpriseSupportChargeSummaryRequestTypeDef",
    "GetEnterpriseSupportChargeSummaryResponseTypeDef",
    "GetEnterpriseSupportContractDetailsRequestTypeDef",
    "GetEnterpriseSupportContractDetailsResponseTypeDef",
    "GetResourcePolicyRequestTypeDef",
    "GetResourcePolicyResponseTypeDef",
    "IntervalTypeDef",
    "InvestmentAttestationTypeDef",
    "InvestmentDistributionTypeDef",
    "InvestmentMultiplierTypeDef",
    "InvestmentRestrictionTypeDef",
    "InvestmentSummaryTypeDef",
    "InvestmentTypeDef",
    "LegalEntityTypeDef",
    "LinkedAccountChargeTypeDef",
    "ListBillingViewSegmentsRequestPaginateTypeDef",
    "ListBillingViewSegmentsRequestTypeDef",
    "ListBillingViewSegmentsResponseTypeDef",
    "ListBillingViewsRequestPaginateTypeDef",
    "ListBillingViewsRequestTypeDef",
    "ListBillingViewsResponseTypeDef",
    "ListBusinessSupportAccountChargesRequestPaginateTypeDef",
    "ListBusinessSupportAccountChargesRequestTypeDef",
    "ListBusinessSupportAccountChargesResponseTypeDef",
    "ListBusinessSupportSubscriptionHistoryRequestPaginateTypeDef",
    "ListBusinessSupportSubscriptionHistoryRequestTypeDef",
    "ListBusinessSupportSubscriptionHistoryResponseTypeDef",
    "ListContractsRequestPaginateTypeDef",
    "ListContractsRequestTypeDef",
    "ListContractsResponseTypeDef",
    "ListContractualInvestmentAttestationsRequestPaginateTypeDef",
    "ListContractualInvestmentAttestationsRequestTypeDef",
    "ListContractualInvestmentAttestationsResponseTypeDef",
    "ListContractualInvestmentSummariesRequestPaginateTypeDef",
    "ListContractualInvestmentSummariesRequestTypeDef",
    "ListContractualInvestmentSummariesResponseTypeDef",
    "ListContractualInvestmentsRequestPaginateTypeDef",
    "ListContractualInvestmentsRequestTypeDef",
    "ListContractualInvestmentsResponseTypeDef",
    "ListEnterpriseSupportLinkedAccountChargesRequestPaginateTypeDef",
    "ListEnterpriseSupportLinkedAccountChargesRequestTypeDef",
    "ListEnterpriseSupportLinkedAccountChargesResponseTypeDef",
    "ListSourceViewsForBillingViewRequestPaginateTypeDef",
    "ListSourceViewsForBillingViewRequestTypeDef",
    "ListSourceViewsForBillingViewResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MilestoneBasedInvestmentTypeDef",
    "OutcomeBasedInvestmentTypeDef",
    "PaginatorConfigTypeDef",
    "PricingPlanTierTypeDef",
    "PricingPlanTypeDef",
    "PrivatePricingAddendumTypeDef",
    "RedeemCreditsRequestTypeDef",
    "ResourceTagTypeDef",
    "ResponseMetadataTypeDef",
    "ServiceLevelAccountUsageTypeDef",
    "StringSearchTypeDef",
    "TagResourceRequestTypeDef",
    "TagValuesOutputTypeDef",
    "TagValuesTypeDef",
    "TimeRangeOutputTypeDef",
    "TimeRangeTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateBillingPreferencesRequestTypeDef",
    "UpdateBillingViewRequestTypeDef",
    "UpdateBillingViewResponseTypeDef",
)

TimestampTypeDef = Union[datetime, str]


class AdditionalChargeTypeDef(TypedDict):
    description: str
    amount: NotRequired[str]
    chargeType: NotRequired[str]


class AdditionalRecipientTypeDef(TypedDict):
    email: str


class AmountTypeDef(TypedDict):
    currencyCode: str
    currencyAmount: str


class ApproverDetailsTypeDef(TypedDict):
    name: str
    title: str
    email: str


class AssociateContractRequestTypeDef(TypedDict):
    contractArn: str
    contractDocumentId: str


class AssociateSourceViewsRequestTypeDef(TypedDict):
    arn: str
    sourceViews: Sequence[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AttestationQuantityTypeDef(TypedDict):
    attestationVolume: str
    attestationUnit: str


class BillingFeatureFilterTypeDef(TypedDict):
    name: NotRequired[Literal["PREFERENCE_KEY"]]
    value: NotRequired[Sequence[str]]


class BillingPeriodTypeDef(TypedDict):
    year: int
    month: int


class BillingPreferenceForKeyTypeDef(TypedDict):
    key: str
    value: PreferenceValueType


class BillingViewHealthStatusTypeDef(TypedDict):
    statusCode: NotRequired[BillingViewStatusType]
    statusReasons: NotRequired[list[BillingViewStatusReasonType]]


class BillingViewSegmentTimeRangeOutputTypeDef(TypedDict):
    beginDateInclusive: NotRequired[datetime]
    endDateExclusive: NotRequired[datetime]


class BusinessSupportDiscountTypeDef(TypedDict):
    discountAmount: NotRequired[str]
    discountPercentage: NotRequired[str]
    discountType: NotRequired[str]
    discountSource: NotRequired[str]


class BusinessSupportServiceSpendTypeDef(TypedDict):
    contributingService: str
    itemType: str
    chargeAmount: str
    currency: str
    description: NotRequired[str]


class BusinessSupportTierChargeTypeDef(TypedDict):
    tierDescription: str
    tierRate: str
    usageSlice: str
    tierCharge: str
    chargePeriodStartDate: NotRequired[datetime]
    chargePeriodEndDate: NotRequired[datetime]


class BusinessSupportSubscriptionContractTypeDef(TypedDict):
    accountId: str
    planName: str
    contractStartDate: datetime
    contractEndDate: datetime


class CancelContractualInvestmentAttestationRequestTypeDef(TypedDict):
    attestationId: str
    contractArn: str
    reason: str


class ChargeAccountTypeDef(TypedDict):
    accountId: str
    chargePercentage: str


class ContractAccountTypeDef(TypedDict):
    accountId: str
    isGdn: bool


class IntervalTypeDef(TypedDict):
    startDateInclusive: datetime
    endDateInclusive: datetime


class CostCategoryValuesOutputTypeDef(TypedDict):
    key: str
    values: list[str]


class CostCategoryValuesTypeDef(TypedDict):
    key: str
    values: Sequence[str]


class ResourceTagTypeDef(TypedDict):
    key: str
    value: NotRequired[str]


class DeleteBillingViewRequestTypeDef(TypedDict):
    arn: str
    force: NotRequired[bool]


class DimensionValuesOutputTypeDef(TypedDict):
    key: Literal["LINKED_ACCOUNT"]
    values: list[str]


class DimensionValuesTypeDef(TypedDict):
    key: Literal["LINKED_ACCOUNT"]
    values: Sequence[str]


class DisassociateContractRequestTypeDef(TypedDict):
    contractArn: str


class DisassociateSourceViewsRequestTypeDef(TypedDict):
    arn: str
    sourceViews: Sequence[str]


class EnterpriseSupportTimePeriodTypeDef(TypedDict):
    beginDate: datetime
    endDate: NotRequired[datetime]


class TagValuesOutputTypeDef(TypedDict):
    key: str
    values: list[str]


class TimeRangeOutputTypeDef(TypedDict):
    beginDateInclusive: NotRequired[datetime]
    endDateInclusive: NotRequired[datetime]


class TagValuesTypeDef(TypedDict):
    key: str
    values: Sequence[str]


class GetBillingViewRequestTypeDef(TypedDict):
    arn: str


class GetContractInformationRequestTypeDef(TypedDict):
    contractArn: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class GetEnterpriseSupportChargeSummaryRequestTypeDef(TypedDict):
    billingMonth: str


class GetEnterpriseSupportContractDetailsRequestTypeDef(TypedDict):
    billingMonth: str


class GetResourcePolicyRequestTypeDef(TypedDict):
    resourceArn: str


class InvestmentMultiplierTypeDef(TypedDict):
    value: str
    investmentAttestationInputUnit: str
    multiplierType: MultiplierTypeType


class LegalEntityTypeDef(TypedDict):
    legalEntityName: str


class ServiceLevelAccountUsageTypeDef(TypedDict):
    serviceCode: NotRequired[str]
    totalSupportEligibleSpend: NotRequired[str]


class StringSearchTypeDef(TypedDict):
    searchOption: Literal["STARTS_WITH"]
    searchValue: str


class ListBusinessSupportAccountChargesRequestTypeDef(TypedDict):
    billingMonth: str
    accountId: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListContractsRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListContractualInvestmentAttestationsRequestTypeDef(TypedDict):
    contractArn: str
    investmentSummaryId: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListContractualInvestmentSummariesRequestTypeDef(TypedDict):
    contractArn: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListContractualInvestmentsRequestTypeDef(TypedDict):
    contractArn: str
    investmentSummaryId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListEnterpriseSupportLinkedAccountChargesRequestTypeDef(TypedDict):
    billingMonth: str
    accountId: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListSourceViewsForBillingViewRequestTypeDef(TypedDict):
    arn: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str


class PricingPlanTierTypeDef(TypedDict):
    tierMinimum: str
    baseCharge: str
    additionalPercentageOfAggregateCharges: str
    aggregateChargesAdjustment: str
    incremental: bool
    tierMaximum: NotRequired[str]
    increment: NotRequired[str]
    incrementCharge: NotRequired[str]


class RedeemCreditsRequestTypeDef(TypedDict):
    promoCode: str


class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    resourceTagKeys: Sequence[str]


class ActiveTimeRangeTypeDef(TypedDict):
    activeAfterInclusive: TimestampTypeDef
    activeBeforeInclusive: TimestampTypeDef


class BillingViewSegmentTimeRangeTypeDef(TypedDict):
    beginDateInclusive: NotRequired[TimestampTypeDef]
    endDateExclusive: NotRequired[TimestampTypeDef]


class GetCreditAllocationHistoryRequestTypeDef(TypedDict):
    accountId: str
    startDate: TimestampTypeDef
    endDate: TimestampTypeDef
    creditId: NotRequired[int]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class GetCreditsRequestTypeDef(TypedDict):
    accountId: str
    startDate: TimestampTypeDef
    endDate: NotRequired[TimestampTypeDef]
    payerAccountFlag: NotRequired[bool]


class ListBusinessSupportSubscriptionHistoryRequestTypeDef(TypedDict):
    billingMonth: NotRequired[str]
    accountId: NotRequired[str]
    startDate: NotRequired[TimestampTypeDef]
    endDate: NotRequired[TimestampTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class TimeRangeTypeDef(TypedDict):
    beginDateInclusive: NotRequired[TimestampTypeDef]
    endDateInclusive: NotRequired[TimestampTypeDef]


class CreditAllocationHistoryEntryTypeDef(TypedDict):
    creditId: str
    creditAmount: AmountTypeDef
    accountId: str
    appliedServiceName: str
    billingMonth: str
    isEstimatedBill: bool
    description: NotRequired[str]


class CreditDataTypeDef(TypedDict):
    creditId: str
    accountId: str
    creditType: str
    initialAmount: AmountTypeDef
    remainingAmount: AmountTypeDef
    description: str
    startDate: datetime
    estimatedAmount: NotRequired[AmountTypeDef]
    applicableProductNames: NotRequired[list[str]]
    endDate: NotRequired[datetime]
    exhaustDate: NotRequired[datetime]
    applicationType: NotRequired[ApplicationTypeType]
    shareableAccounts: NotRequired[list[str]]
    accountHasCreditSharingEnabled: NotRequired[bool]
    creditConsoleVisibility: NotRequired[str]
    creditSharingType: NotRequired[CreditSharingTypeType]
    costCategoryArn: NotRequired[str]
    ruleName: NotRequired[str]
    creditStatus: NotRequired[CreditStatusType]
    purchaseTypeApplications: NotRequired[list[str]]


class InvestmentDistributionTypeDef(TypedDict):
    accountId: str
    investmentAmount: AmountTypeDef


class InvestmentRestrictionTypeDef(TypedDict):
    amount: AmountTypeDef


class InvestmentSummaryTypeDef(TypedDict):
    investmentSummaryId: str
    investmentName: str
    investmentType: InvestmentTypeType
    maxAllowedInvestmentDisbursementValue: NotRequired[AmountTypeDef]


class MilestoneBasedInvestmentTypeDef(TypedDict):
    investmentId: str
    investmentValue: AmountTypeDef
    investmentDisbursedAt: datetime


class AssociateSourceViewsResponseTypeDef(TypedDict):
    arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateBillingViewResponseTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CreateContractualInvestmentAttestationResponseTypeDef(TypedDict):
    attestationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteBillingViewResponseTypeDef(TypedDict):
    arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateSourceViewsResponseTypeDef(TypedDict):
    arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetResourcePolicyResponseTypeDef(TypedDict):
    resourceArn: str
    policy: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListSourceViewsForBillingViewResponseTypeDef(TypedDict):
    sourceViews: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateBillingViewResponseTypeDef(TypedDict):
    arn: str
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class AttestationValueTypeDef(TypedDict):
    attestationAmount: NotRequired[AmountTypeDef]
    attestationQuantities: NotRequired[Sequence[AttestationQuantityTypeDef]]


class GetBillingPreferencesRequestTypeDef(TypedDict):
    features: Sequence[BillingFeatureType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    filters: NotRequired[Sequence[BillingFeatureFilterTypeDef]]


class BillingPreferenceSummaryTypeDef(TypedDict):
    feature: BillingFeatureType
    key: str
    value: PreferenceValueType
    accountName: NotRequired[str]
    accountId: NotRequired[str]
    billingPeriod: NotRequired[BillingPeriodTypeDef]


class UpdateBillingPreferencesRequestTypeDef(TypedDict):
    feature: BillingFeatureType
    billingPreferencesPerKey: Sequence[BillingPreferenceForKeyTypeDef]


class BillingViewListElementTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]
    ownerAccountId: NotRequired[str]
    sourceAccountId: NotRequired[str]
    billingViewType: NotRequired[BillingViewTypeType]
    healthStatus: NotRequired[BillingViewHealthStatusTypeDef]


class BillingViewSegmentsListElementTypeDef(TypedDict):
    domain: NotRequired[BillingDomainType]
    timeRange: NotRequired[BillingViewSegmentTimeRangeOutputTypeDef]
    billingTransferAccountId: NotRequired[str]
    managementAccountId: NotRequired[str]
    billingGroupPrimaryAccountId: NotRequired[str]


class BusinessSupportAccountChargeTypeDef(TypedDict):
    accountId: str
    supportPlanName: str
    totalCharge: str
    totalUsageBasis: str
    tierCharges: NotRequired[list[BusinessSupportTierChargeTypeDef]]
    supportDiscount: NotRequired[BusinessSupportDiscountTypeDef]
    supportEligibleSpendByService: NotRequired[list[BusinessSupportServiceSpendTypeDef]]


class ListBusinessSupportSubscriptionHistoryResponseTypeDef(TypedDict):
    subscriptionContracts: list[BusinessSupportSubscriptionContractTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ContractSummaryTypeDef(TypedDict):
    contractArn: str
    contractTerm: IntervalTypeDef
    associationStatus: AssociationStatusType
    contractType: NotRequired[ContractTypeType]
    lastUpdatedAt: NotRequired[datetime]


class ListTagsForResourceResponseTypeDef(TypedDict):
    resourceTags: list[ResourceTagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    resourceTags: Sequence[ResourceTagTypeDef]


class ExpressionOutputTypeDef(TypedDict):
    dimensions: NotRequired[DimensionValuesOutputTypeDef]
    tags: NotRequired[TagValuesOutputTypeDef]
    costCategories: NotRequired[CostCategoryValuesOutputTypeDef]
    timeRange: NotRequired[TimeRangeOutputTypeDef]


class GetCreditAllocationHistoryRequestPaginateTypeDef(TypedDict):
    accountId: str
    startDate: TimestampTypeDef
    endDate: TimestampTypeDef
    creditId: NotRequired[int]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBusinessSupportAccountChargesRequestPaginateTypeDef(TypedDict):
    billingMonth: str
    accountId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBusinessSupportSubscriptionHistoryRequestPaginateTypeDef(TypedDict):
    billingMonth: NotRequired[str]
    accountId: NotRequired[str]
    startDate: NotRequired[TimestampTypeDef]
    endDate: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListContractsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListContractualInvestmentAttestationsRequestPaginateTypeDef(TypedDict):
    contractArn: str
    investmentSummaryId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListContractualInvestmentSummariesRequestPaginateTypeDef(TypedDict):
    contractArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListContractualInvestmentsRequestPaginateTypeDef(TypedDict):
    contractArn: str
    investmentSummaryId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEnterpriseSupportLinkedAccountChargesRequestPaginateTypeDef(TypedDict):
    billingMonth: str
    accountId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSourceViewsForBillingViewRequestPaginateTypeDef(TypedDict):
    arn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class PrivatePricingAddendumTypeDef(TypedDict):
    contractArn: str
    contractTerm: IntervalTypeDef
    eligiblePayerAccounts: list[str]
    investmentAccounts: list[str]
    legalEntities: list[LegalEntityTypeDef]
    contractRestrictions: NotRequired[list[Literal["ATTESTATION_SELF_SERVICE_BLOCKED"]]]


class LinkedAccountChargeTypeDef(TypedDict):
    accountId: str
    payerAccountId: str
    billableSeconds: int
    totalSeconds: int
    totalSupportEligibleSpend: str
    proratedTotalSupportEligibleSpend: str
    accountType: NotRequired[str]
    linkedTimePeriods: NotRequired[list[EnterpriseSupportTimePeriodTypeDef]]
    subscriptionTimePeriods: NotRequired[list[EnterpriseSupportTimePeriodTypeDef]]
    totalSupportEligibleReservedInstanceSpend: NotRequired[str]
    totalSupportEligibleSavingsPlanSpend: NotRequired[str]
    supportEligibleSpendByService: NotRequired[list[ServiceLevelAccountUsageTypeDef]]


class PricingPlanTypeDef(TypedDict):
    tiers: list[PricingPlanTierTypeDef]
    pricingPlanId: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]
    startDate: NotRequired[datetime]
    endDate: NotRequired[datetime]
    planDiscountPercent: NotRequired[str]
    discountAppliesToMinimumCharge: NotRequired[bool]
    minimumCharge: NotRequired[str]
    tiered: NotRequired[str]


class ListBillingViewsRequestPaginateTypeDef(TypedDict):
    activeTimeRange: NotRequired[ActiveTimeRangeTypeDef]
    arns: NotRequired[Sequence[str]]
    billingViewTypes: NotRequired[Sequence[BillingViewTypeType]]
    names: NotRequired[Sequence[StringSearchTypeDef]]
    ownerAccountId: NotRequired[str]
    sourceAccountId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBillingViewsRequestTypeDef(TypedDict):
    activeTimeRange: NotRequired[ActiveTimeRangeTypeDef]
    arns: NotRequired[Sequence[str]]
    billingViewTypes: NotRequired[Sequence[BillingViewTypeType]]
    names: NotRequired[Sequence[StringSearchTypeDef]]
    ownerAccountId: NotRequired[str]
    sourceAccountId: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


BillingViewSegmentTimeRangeUnionTypeDef = Union[
    BillingViewSegmentTimeRangeTypeDef, BillingViewSegmentTimeRangeOutputTypeDef
]


class ExpressionTypeDef(TypedDict):
    dimensions: NotRequired[DimensionValuesTypeDef]
    tags: NotRequired[TagValuesTypeDef]
    costCategories: NotRequired[CostCategoryValuesTypeDef]
    timeRange: NotRequired[TimeRangeTypeDef]


class GetCreditAllocationHistoryResponseTypeDef(TypedDict):
    creditAllocationHistoryList: list[CreditAllocationHistoryEntryTypeDef]
    partialResults: bool
    failedMonths: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


GetCreditsResponseTypeDef = TypedDict(
    "GetCreditsResponseTypeDef",
    {
        "credits": list[CreditDataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class InvestmentAttestationTypeDef(TypedDict):
    attestationId: str
    investmentName: str
    outcomeDescription: str
    investmentSummaryId: str
    investmentId: str
    attestedAt: datetime
    updatedAt: datetime
    attestationStatus: InvestmentAttestationStatusType
    investmentDisbursedAt: NotRequired[datetime]
    attestedValue: NotRequired[AmountTypeDef]
    investmentDistributions: NotRequired[list[InvestmentDistributionTypeDef]]
    rejectionReasons: NotRequired[list[str]]
    isCancellable: NotRequired[bool]


class OutcomeBasedInvestmentTypeDef(TypedDict):
    investmentId: str
    outcomeDescription: str
    attestationWindow: IntervalTypeDef
    disbursedValue: AmountTypeDef
    investmentRestrictions: NotRequired[list[InvestmentRestrictionTypeDef]]
    investmentMultipliers: NotRequired[list[InvestmentMultiplierTypeDef]]


class ListContractualInvestmentSummariesResponseTypeDef(TypedDict):
    items: list[InvestmentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class AttestationDetailsTypeDef(TypedDict):
    attestationValue: AttestationValueTypeDef
    investmentDistributions: NotRequired[Sequence[InvestmentDistributionTypeDef]]


class GetBillingPreferencesResponseTypeDef(TypedDict):
    billingPreferences: list[BillingPreferenceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListBillingViewsResponseTypeDef(TypedDict):
    billingViews: list[BillingViewListElementTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListBillingViewSegmentsResponseTypeDef(TypedDict):
    items: list[BillingViewSegmentsListElementTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListBusinessSupportAccountChargesResponseTypeDef(TypedDict):
    billingMonth: str
    isEstimated: bool
    totalSupportCharge: str
    totalSupportEligibleSpend: str
    accountCount: int
    accountCharges: list[BusinessSupportAccountChargeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListContractsResponseTypeDef(TypedDict):
    items: list[ContractSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class BillingViewElementTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]
    billingViewType: NotRequired[BillingViewTypeType]
    ownerAccountId: NotRequired[str]
    sourceAccountId: NotRequired[str]
    dataFilterExpression: NotRequired[ExpressionOutputTypeDef]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]
    derivedViewCount: NotRequired[int]
    sourceViewCount: NotRequired[int]
    viewDefinitionLastUpdatedAt: NotRequired[datetime]
    healthStatus: NotRequired[BillingViewHealthStatusTypeDef]


class ContractDetailsTypeDef(TypedDict):
    privatePricingAddendum: NotRequired[PrivatePricingAddendumTypeDef]


class ListEnterpriseSupportLinkedAccountChargesResponseTypeDef(TypedDict):
    linkedAccount: list[LinkedAccountChargeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetEnterpriseSupportChargeSummaryResponseTypeDef(TypedDict):
    payerAccountId: str
    billingMonth: str
    billingPeriodStartDate: datetime
    billingPeriodEndDate: datetime
    isEstimated: bool
    billDate: datetime
    supportCharge: str
    totalSupportCharge: str
    supportDiscount: str
    totalSupportEligibleSpend: str
    totalSupportEligibleUsageSpend: str
    totalSupportEligibleReservedInstanceSpend: str
    totalSupportEligibleSavingsPlanSpend: str
    supportChargePercentage: str
    supportEffectivePricingPlan: PricingPlanTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetEnterpriseSupportContractDetailsResponseTypeDef(TypedDict):
    isContractActive: bool
    supportAllocationMethod: str
    supportReservedInstanceAmortizationStartDate: datetime
    supportReservedInstanceTreatmentMethod: str
    supportSavingsPlansAmortizationStartDate: datetime
    supportSavingsPlansTreatmentMethod: str
    supportProrateStartDate: datetime
    contractPayerAccountIds: list[ContractAccountTypeDef]
    chargedPayerAccountIds: list[ChargeAccountTypeDef]
    additionalSupportCharge: list[AdditionalChargeTypeDef]
    additionalSupportEligibleUsageSpend: list[AdditionalChargeTypeDef]
    pricingPlans: list[PricingPlanTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListBillingViewSegmentsRequestPaginateTypeDef(TypedDict):
    timeRange: NotRequired[BillingViewSegmentTimeRangeUnionTypeDef]
    arn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBillingViewSegmentsRequestTypeDef(TypedDict):
    timeRange: NotRequired[BillingViewSegmentTimeRangeUnionTypeDef]
    arn: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


ExpressionUnionTypeDef = Union[ExpressionTypeDef, ExpressionOutputTypeDef]


class ListContractualInvestmentAttestationsResponseTypeDef(TypedDict):
    items: list[InvestmentAttestationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class InvestmentTypeDef(TypedDict):
    milestoneBasedInvestment: NotRequired[MilestoneBasedInvestmentTypeDef]
    outcomeBasedInvestment: NotRequired[OutcomeBasedInvestmentTypeDef]


class CreateContractualInvestmentAttestationRequestTypeDef(TypedDict):
    contractArn: str
    investmentSummaryId: str
    investmentId: str
    contractDocumentId: str
    approverDetails: ApproverDetailsTypeDef
    attestationDetails: AttestationDetailsTypeDef
    investmentDisbursedAt: NotRequired[TimestampTypeDef]
    additionalRecipients: NotRequired[Sequence[AdditionalRecipientTypeDef]]
    clientToken: NotRequired[str]


class GetBillingViewResponseTypeDef(TypedDict):
    billingView: BillingViewElementTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetContractInformationResponseTypeDef(TypedDict):
    contract: ContractDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateBillingViewRequestTypeDef(TypedDict):
    name: str
    sourceViews: Sequence[str]
    description: NotRequired[str]
    dataFilterExpression: NotRequired[ExpressionUnionTypeDef]
    clientToken: NotRequired[str]
    resourceTags: NotRequired[Sequence[ResourceTagTypeDef]]


class UpdateBillingViewRequestTypeDef(TypedDict):
    arn: str
    name: NotRequired[str]
    description: NotRequired[str]
    dataFilterExpression: NotRequired[ExpressionUnionTypeDef]


class ListContractualInvestmentsResponseTypeDef(TypedDict):
    items: list[InvestmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
