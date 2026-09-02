"""
Type annotations for marketplace-agreement service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_marketplace_agreement.type_defs import AcceptAgreementCancellationRequestInputTypeDef

    data: AcceptAgreementCancellationRequestInputTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from datetime import datetime
from typing import Union

from .literals import (
    AgreementCancellationRequestReasonCodeType,
    AgreementCancellationRequestStatusType,
    AgreementEntitlementStatusReasonCodeType,
    AgreementEntitlementStatusType,
    AgreementStatusType,
    BillingAdjustmentErrorCodeType,
    BillingAdjustmentReasonCodeType,
    BillingAdjustmentStatusType,
    EndTimeBehaviorReasonCodeType,
    EndTimeBehaviorTypeType,
    IntentType,
    InvoiceTypeType,
    PaymentRequestApprovalStrategyType,
    PaymentRequestStatusType,
    SortOrderType,
    TaxEstimationType,
    TimingType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AcceptAgreementCancellationRequestInputTypeDef",
    "AcceptAgreementCancellationRequestOutputTypeDef",
    "AcceptAgreementPaymentRequestInputTypeDef",
    "AcceptAgreementPaymentRequestOutputTypeDef",
    "AcceptAgreementRequestInputTypeDef",
    "AcceptAgreementRequestOutputTypeDef",
    "AcceptedTermTypeDef",
    "AcceptorTypeDef",
    "AgreementCancellationRequestSummaryTypeDef",
    "AgreementEntitlementTypeDef",
    "AgreementInvoiceLineItemGroupSummaryTypeDef",
    "AgreementViewSummaryTypeDef",
    "BatchCreateBillingAdjustmentErrorTypeDef",
    "BatchCreateBillingAdjustmentItemTypeDef",
    "BatchCreateBillingAdjustmentRequestEntryTypeDef",
    "BatchCreateBillingAdjustmentRequestInputTypeDef",
    "BatchCreateBillingAdjustmentRequestOutputTypeDef",
    "BillingAdjustmentSummaryTypeDef",
    "ByolPricingTermTypeDef",
    "CancelAgreementCancellationRequestInputTypeDef",
    "CancelAgreementCancellationRequestOutputTypeDef",
    "CancelAgreementInputTypeDef",
    "CancelAgreementPaymentRequestInputTypeDef",
    "CancelAgreementPaymentRequestOutputTypeDef",
    "ChargeSummaryTypeDef",
    "ChargeTypeDef",
    "ConfigurableUpfrontPricingTermConfigurationOutputTypeDef",
    "ConfigurableUpfrontPricingTermConfigurationTypeDef",
    "ConfigurableUpfrontPricingTermConfigurationUnionTypeDef",
    "ConfigurableUpfrontPricingTermTypeDef",
    "ConfigurableUpfrontRateCardItemTypeDef",
    "ConstraintsTypeDef",
    "CreateAgreementRequestInputTypeDef",
    "CreateAgreementRequestOutputTypeDef",
    "DescribeAgreementInputTypeDef",
    "DescribeAgreementOutputTypeDef",
    "DimensionTypeDef",
    "DocumentItemTypeDef",
    "EndTimeBehaviorTypeDef",
    "EntitlementTypeDef",
    "EstimatedChargesTypeDef",
    "EstimatedTaxesTypeDef",
    "ExpectedChargeTypeDef",
    "FilterTypeDef",
    "FixedPercentageTypeDef",
    "FixedUpfrontPricingTermTypeDef",
    "FreeTrialPricingTermTypeDef",
    "GetAgreementCancellationRequestInputTypeDef",
    "GetAgreementCancellationRequestOutputTypeDef",
    "GetAgreementEntitlementsInputPaginateTypeDef",
    "GetAgreementEntitlementsInputTypeDef",
    "GetAgreementEntitlementsOutputTypeDef",
    "GetAgreementPaymentRequestInputTypeDef",
    "GetAgreementPaymentRequestOutputTypeDef",
    "GetAgreementTermsInputPaginateTypeDef",
    "GetAgreementTermsInputTypeDef",
    "GetAgreementTermsOutputTypeDef",
    "GetBillingAdjustmentRequestInputTypeDef",
    "GetBillingAdjustmentRequestOutputTypeDef",
    "GrantItemTypeDef",
    "InvoiceBillingPeriodTypeDef",
    "InvoicingEntityTypeDef",
    "ItemizedChargeTypeDef",
    "LegalTermTypeDef",
    "ListAgreementCancellationRequestsInputPaginateTypeDef",
    "ListAgreementCancellationRequestsInputTypeDef",
    "ListAgreementCancellationRequestsOutputTypeDef",
    "ListAgreementChargesInputPaginateTypeDef",
    "ListAgreementChargesInputTypeDef",
    "ListAgreementChargesOutputTypeDef",
    "ListAgreementInvoiceLineItemsInputPaginateTypeDef",
    "ListAgreementInvoiceLineItemsInputTypeDef",
    "ListAgreementInvoiceLineItemsOutputTypeDef",
    "ListAgreementPaymentRequestsInputPaginateTypeDef",
    "ListAgreementPaymentRequestsInputTypeDef",
    "ListAgreementPaymentRequestsOutputTypeDef",
    "ListBillingAdjustmentRequestsInputPaginateTypeDef",
    "ListBillingAdjustmentRequestsInputTypeDef",
    "ListBillingAdjustmentRequestsOutputTypeDef",
    "NetPaymentTermTypeDef",
    "PaginatorConfigTypeDef",
    "PaymentRequestSummaryTypeDef",
    "PaymentScheduleEntryTypeDef",
    "PaymentScheduleTermTemplateTypeDef",
    "PaymentScheduleTermTypeDef",
    "PercentageRangeTypeDef",
    "PriceIncreaseTypeDef",
    "PricingCurrencyAmountTypeDef",
    "ProposalSummaryTypeDef",
    "ProposerTypeDef",
    "PurchaseOrderTypeDef",
    "RateCardItemTypeDef",
    "RecurringPaymentTermTypeDef",
    "RejectAgreementCancellationRequestInputTypeDef",
    "RejectAgreementCancellationRequestOutputTypeDef",
    "RejectAgreementPaymentRequestInputTypeDef",
    "RejectAgreementPaymentRequestOutputTypeDef",
    "RenewalSummaryTypeDef",
    "RenewalTermConfigurationTypeDef",
    "RenewalTermTypeDef",
    "RequestedTermConfigurationTypeDef",
    "RequestedTermTypeDef",
    "ResourceTypeDef",
    "ResponseMetadataTypeDef",
    "ScheduleItemTypeDef",
    "SearchAgreementsInputPaginateTypeDef",
    "SearchAgreementsInputTypeDef",
    "SearchAgreementsOutputTypeDef",
    "SelectorTypeDef",
    "SendAgreementCancellationRequestInputTypeDef",
    "SendAgreementCancellationRequestOutputTypeDef",
    "SendAgreementPaymentRequestInputTypeDef",
    "SendAgreementPaymentRequestOutputTypeDef",
    "SortTypeDef",
    "SupportTermTypeDef",
    "TaxBreakdownItemTypeDef",
    "TaxConfigurationTypeDef",
    "TermTemplateTypeDef",
    "TimestampTypeDef",
    "UpdatePurchaseOrdersInputTypeDef",
    "UsageBasedPricingTermTypeDef",
    "UsageBasedRateCardItemTypeDef",
    "ValidityTermTypeDef",
    "VariablePaymentTermConfigurationTypeDef",
    "VariablePaymentTermTypeDef",
)


class AcceptAgreementCancellationRequestInputTypeDef(TypedDict):
    agreementId: str
    agreementCancellationRequestId: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AcceptAgreementPaymentRequestInputTypeDef(TypedDict):
    paymentRequestId: str
    agreementId: str
    purchaseOrderReference: NotRequired[str]


class PurchaseOrderTypeDef(TypedDict):
    chargeId: str
    chargeRevision: NotRequired[int]
    agreementId: NotRequired[str]
    purchaseOrderReference: NotRequired[str]


ByolPricingTermTypeDef = TypedDict(
    "ByolPricingTermTypeDef",
    {
        "type": NotRequired[str],
        "id": NotRequired[str],
    },
)
NetPaymentTermTypeDef = TypedDict(
    "NetPaymentTermTypeDef",
    {
        "type": NotRequired[str],
        "id": NotRequired[str],
        "paymentDuePeriod": NotRequired[str],
    },
)
RecurringPaymentTermTypeDef = TypedDict(
    "RecurringPaymentTermTypeDef",
    {
        "type": NotRequired[str],
        "id": NotRequired[str],
        "currencyCode": NotRequired[str],
        "billingPeriod": NotRequired[str],
        "price": NotRequired[str],
    },
)
SupportTermTypeDef = TypedDict(
    "SupportTermTypeDef",
    {
        "type": NotRequired[str],
        "id": NotRequired[str],
        "refundPolicy": NotRequired[str],
    },
)
ValidityTermTypeDef = TypedDict(
    "ValidityTermTypeDef",
    {
        "type": NotRequired[str],
        "id": NotRequired[str],
        "agreementDuration": NotRequired[str],
        "agreementStartDate": NotRequired[datetime],
        "agreementEndDate": NotRequired[datetime],
    },
)


class AcceptorTypeDef(TypedDict):
    accountId: NotRequired[str]


class AgreementCancellationRequestSummaryTypeDef(TypedDict):
    agreementCancellationRequestId: NotRequired[str]
    agreementId: NotRequired[str]
    status: NotRequired[AgreementCancellationRequestStatusType]
    reasonCode: NotRequired[AgreementCancellationRequestReasonCodeType]
    agreementType: NotRequired[str]
    catalog: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]


ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "id": NotRequired[str],
        "type": NotRequired[str],
    },
)


class InvoiceBillingPeriodTypeDef(TypedDict):
    month: int
    year: int


class InvoicingEntityTypeDef(TypedDict):
    legalName: NotRequired[str]
    branchName: NotRequired[str]


class PricingCurrencyAmountTypeDef(TypedDict):
    amount: NotRequired[str]
    maxAdjustmentAmount: NotRequired[str]
    currencyCode: NotRequired[str]


class EntitlementTypeDef(TypedDict):
    licenseArn: NotRequired[str]


class ProposerTypeDef(TypedDict):
    accountId: NotRequired[str]


class BatchCreateBillingAdjustmentErrorTypeDef(TypedDict):
    code: BillingAdjustmentErrorCodeType
    message: str
    clientToken: str


class BatchCreateBillingAdjustmentItemTypeDef(TypedDict):
    billingAdjustmentRequestId: str
    clientToken: str


class BatchCreateBillingAdjustmentRequestEntryTypeDef(TypedDict):
    agreementId: str
    originalInvoiceId: str
    adjustmentAmount: str
    currencyCode: str
    adjustmentReasonCode: BillingAdjustmentReasonCodeType
    clientToken: str
    description: NotRequired[str]


class BillingAdjustmentSummaryTypeDef(TypedDict):
    billingAdjustmentRequestId: str
    originalInvoiceId: str
    adjustmentAmount: str
    currencyCode: str
    status: BillingAdjustmentStatusType
    agreementId: str
    createdAt: datetime
    updatedAt: datetime
    agreementType: str
    catalog: str


class CancelAgreementCancellationRequestInputTypeDef(TypedDict):
    agreementId: str
    agreementCancellationRequestId: str
    cancellationReason: str


class CancelAgreementInputTypeDef(TypedDict):
    agreementId: str


class CancelAgreementPaymentRequestInputTypeDef(TypedDict):
    paymentRequestId: str
    agreementId: str


class ItemizedChargeTypeDef(TypedDict):
    dimensionKey: NotRequired[str]
    newQuantity: NotRequired[int]
    oldQuantity: NotRequired[int]
    chargeReference: NotRequired[str]
    incrementalChargeAmount: NotRequired[str]


ChargeTypeDef = TypedDict(
    "ChargeTypeDef",
    {
        "id": NotRequired[str],
        "revision": NotRequired[int],
        "agreementId": NotRequired[str],
        "agreementType": NotRequired[str],
        "purchaseOrderReference": NotRequired[str],
        "currencyCode": NotRequired[str],
        "amount": NotRequired[str],
        "time": NotRequired[datetime],
    },
)


class DimensionTypeDef(TypedDict):
    dimensionKey: str
    dimensionValue: int


class ConstraintsTypeDef(TypedDict):
    multipleDimensionSelection: NotRequired[str]
    quantityConfiguration: NotRequired[str]


class RateCardItemTypeDef(TypedDict):
    dimensionKey: NotRequired[str]
    price: NotRequired[str]


SelectorTypeDef = TypedDict(
    "SelectorTypeDef",
    {
        "type": NotRequired[str],
        "value": NotRequired[str],
    },
)


class TaxConfigurationTypeDef(TypedDict):
    taxEstimation: NotRequired[TaxEstimationType]


class DescribeAgreementInputTypeDef(TypedDict):
    agreementId: str


class EstimatedChargesTypeDef(TypedDict):
    currencyCode: NotRequired[str]
    agreementValue: NotRequired[str]


DocumentItemTypeDef = TypedDict(
    "DocumentItemTypeDef",
    {
        "type": NotRequired[str],
        "url": NotRequired[str],
        "version": NotRequired[str],
    },
)


class RenewalSummaryTypeDef(TypedDict):
    offerId: NotRequired[str]


TaxBreakdownItemTypeDef = TypedDict(
    "TaxBreakdownItemTypeDef",
    {
        "amount": NotRequired[str],
        "rate": NotRequired[str],
        "type": NotRequired[str],
    },
)


class FilterTypeDef(TypedDict):
    name: NotRequired[str]
    values: NotRequired[Sequence[str]]


class FixedPercentageTypeDef(TypedDict):
    value: NotRequired[str]


class GrantItemTypeDef(TypedDict):
    dimensionKey: NotRequired[str]
    maxQuantity: NotRequired[int]


class GetAgreementCancellationRequestInputTypeDef(TypedDict):
    agreementCancellationRequestId: str
    agreementId: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class GetAgreementEntitlementsInputTypeDef(TypedDict):
    agreementId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class GetAgreementPaymentRequestInputTypeDef(TypedDict):
    paymentRequestId: str
    agreementId: str


class GetAgreementTermsInputTypeDef(TypedDict):
    agreementId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class GetBillingAdjustmentRequestInputTypeDef(TypedDict):
    agreementId: str
    billingAdjustmentRequestId: str


class ListAgreementCancellationRequestsInputTypeDef(TypedDict):
    partyType: str
    agreementId: NotRequired[str]
    status: NotRequired[AgreementCancellationRequestStatusType]
    agreementType: NotRequired[str]
    catalog: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListAgreementChargesInputTypeDef(TypedDict):
    catalog: NotRequired[str]
    agreementId: NotRequired[str]
    agreementType: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class ListAgreementPaymentRequestsInputTypeDef(TypedDict):
    partyType: str
    agreementType: NotRequired[str]
    catalog: NotRequired[str]
    agreementId: NotRequired[str]
    status: NotRequired[PaymentRequestStatusType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class PaymentRequestSummaryTypeDef(TypedDict):
    paymentRequestId: NotRequired[str]
    agreementId: NotRequired[str]
    status: NotRequired[PaymentRequestStatusType]
    name: NotRequired[str]
    chargeId: NotRequired[str]
    chargeAmount: NotRequired[str]
    currencyCode: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]


class PaymentScheduleEntryTypeDef(TypedDict):
    chargeDateOffset: NotRequired[str]
    chargePercentage: NotRequired[str]
    dayOfMonth: NotRequired[int]


class ScheduleItemTypeDef(TypedDict):
    chargeDate: NotRequired[datetime]
    chargeAmount: NotRequired[str]


class PercentageRangeTypeDef(TypedDict):
    minValue: NotRequired[str]
    maxValue: NotRequired[str]
    defaultValue: NotRequired[str]


class RejectAgreementCancellationRequestInputTypeDef(TypedDict):
    agreementId: str
    agreementCancellationRequestId: str
    rejectionReason: str


class RejectAgreementPaymentRequestInputTypeDef(TypedDict):
    paymentRequestId: str
    agreementId: str
    rejectionReason: NotRequired[str]


class RenewalTermConfigurationTypeDef(TypedDict):
    enableAutoRenew: bool


class VariablePaymentTermConfigurationTypeDef(TypedDict):
    paymentRequestApprovalStrategy: PaymentRequestApprovalStrategyType
    expirationDuration: NotRequired[str]


class SortTypeDef(TypedDict):
    sortBy: NotRequired[str]
    sortOrder: NotRequired[SortOrderType]


class SendAgreementCancellationRequestInputTypeDef(TypedDict):
    agreementId: str
    reasonCode: AgreementCancellationRequestReasonCodeType
    clientToken: NotRequired[str]
    description: NotRequired[str]


class SendAgreementPaymentRequestInputTypeDef(TypedDict):
    agreementId: str
    termId: str
    name: str
    chargeAmount: str
    clientToken: NotRequired[str]
    description: NotRequired[str]


class AcceptAgreementCancellationRequestOutputTypeDef(TypedDict):
    agreementId: str
    agreementCancellationRequestId: str
    status: AgreementCancellationRequestStatusType
    reasonCode: AgreementCancellationRequestReasonCodeType
    description: str
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class AcceptAgreementPaymentRequestOutputTypeDef(TypedDict):
    paymentRequestId: str
    agreementId: str
    status: PaymentRequestStatusType
    name: str
    description: str
    chargeAmount: str
    currencyCode: str
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class AcceptAgreementRequestOutputTypeDef(TypedDict):
    agreementId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CancelAgreementCancellationRequestOutputTypeDef(TypedDict):
    agreementCancellationRequestId: str
    agreementId: str
    reasonCode: AgreementCancellationRequestReasonCodeType
    description: str
    status: AgreementCancellationRequestStatusType
    statusMessage: str
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CancelAgreementPaymentRequestOutputTypeDef(TypedDict):
    paymentRequestId: str
    agreementId: str
    status: PaymentRequestStatusType
    name: str
    description: str
    chargeAmount: str
    currencyCode: str
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GetAgreementCancellationRequestOutputTypeDef(TypedDict):
    agreementCancellationRequestId: str
    agreementId: str
    reasonCode: AgreementCancellationRequestReasonCodeType
    description: str
    status: AgreementCancellationRequestStatusType
    statusMessage: str
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GetAgreementPaymentRequestOutputTypeDef(TypedDict):
    paymentRequestId: str
    agreementId: str
    status: PaymentRequestStatusType
    statusMessage: str
    name: str
    description: str
    chargeId: str
    chargeAmount: str
    currencyCode: str
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GetBillingAdjustmentRequestOutputTypeDef(TypedDict):
    billingAdjustmentRequestId: str
    agreementId: str
    adjustmentReasonCode: BillingAdjustmentReasonCodeType
    description: str
    originalInvoiceId: str
    adjustmentAmount: str
    currencyCode: str
    status: BillingAdjustmentStatusType
    statusMessage: str
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class RejectAgreementCancellationRequestOutputTypeDef(TypedDict):
    agreementId: str
    agreementCancellationRequestId: str
    status: AgreementCancellationRequestStatusType
    statusMessage: str
    reasonCode: AgreementCancellationRequestReasonCodeType
    description: str
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class RejectAgreementPaymentRequestOutputTypeDef(TypedDict):
    paymentRequestId: str
    agreementId: str
    status: PaymentRequestStatusType
    statusMessage: str
    name: str
    description: str
    chargeAmount: str
    currencyCode: str
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class SendAgreementCancellationRequestOutputTypeDef(TypedDict):
    agreementId: str
    agreementCancellationRequestId: str
    status: AgreementCancellationRequestStatusType
    reasonCode: AgreementCancellationRequestReasonCodeType
    description: str
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class SendAgreementPaymentRequestOutputTypeDef(TypedDict):
    paymentRequestId: str
    agreementId: str
    status: PaymentRequestStatusType
    name: str
    description: str
    chargeAmount: str
    currencyCode: str
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class AcceptAgreementRequestInputTypeDef(TypedDict):
    agreementRequestId: str
    purchaseOrders: NotRequired[Sequence[PurchaseOrderTypeDef]]


class UpdatePurchaseOrdersInputTypeDef(TypedDict):
    purchaseOrders: Sequence[PurchaseOrderTypeDef]


class ListAgreementCancellationRequestsOutputTypeDef(TypedDict):
    items: list[AgreementCancellationRequestSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


AgreementEntitlementTypeDef = TypedDict(
    "AgreementEntitlementTypeDef",
    {
        "resource": NotRequired[ResourceTypeDef],
        "type": NotRequired[str],
        "registrationToken": NotRequired[str],
        "status": NotRequired[AgreementEntitlementStatusType],
        "statusReasonCode": NotRequired[AgreementEntitlementStatusReasonCodeType],
        "licenseArn": NotRequired[str],
    },
)


class ProposalSummaryTypeDef(TypedDict):
    resources: NotRequired[list[ResourceTypeDef]]
    offerId: NotRequired[str]
    offerSetId: NotRequired[str]


class AgreementInvoiceLineItemGroupSummaryTypeDef(TypedDict):
    agreementId: NotRequired[str]
    invoiceId: NotRequired[str]
    pricingCurrencyAmount: NotRequired[PricingCurrencyAmountTypeDef]
    invoiceBillingPeriod: NotRequired[InvoiceBillingPeriodTypeDef]
    issuedTime: NotRequired[datetime]
    invoiceType: NotRequired[InvoiceTypeType]
    invoicingEntity: NotRequired[InvoicingEntityTypeDef]


class BatchCreateBillingAdjustmentRequestOutputTypeDef(TypedDict):
    items: list[BatchCreateBillingAdjustmentItemTypeDef]
    errors: list[BatchCreateBillingAdjustmentErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchCreateBillingAdjustmentRequestInputTypeDef(TypedDict):
    billingAdjustmentRequestEntries: Sequence[BatchCreateBillingAdjustmentRequestEntryTypeDef]


class ListBillingAdjustmentRequestsOutputTypeDef(TypedDict):
    items: list[BillingAdjustmentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListAgreementChargesOutputTypeDef(TypedDict):
    items: list[ChargeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ConfigurableUpfrontPricingTermConfigurationOutputTypeDef(TypedDict):
    selectorValue: str
    dimensions: list[DimensionTypeDef]


class ConfigurableUpfrontPricingTermConfigurationTypeDef(TypedDict):
    selectorValue: str
    dimensions: Sequence[DimensionTypeDef]


class UsageBasedRateCardItemTypeDef(TypedDict):
    rateCard: NotRequired[list[RateCardItemTypeDef]]


class ConfigurableUpfrontRateCardItemTypeDef(TypedDict):
    selector: NotRequired[SelectorTypeDef]
    constraints: NotRequired[ConstraintsTypeDef]
    rateCard: NotRequired[list[RateCardItemTypeDef]]


LegalTermTypeDef = TypedDict(
    "LegalTermTypeDef",
    {
        "type": NotRequired[str],
        "id": NotRequired[str],
        "documents": NotRequired[list[DocumentItemTypeDef]],
    },
)
EndTimeBehaviorTypeDef = TypedDict(
    "EndTimeBehaviorTypeDef",
    {
        "type": EndTimeBehaviorTypeType,
        "reasonCode": NotRequired[EndTimeBehaviorReasonCodeType],
        "renewalSummary": NotRequired[RenewalSummaryTypeDef],
    },
)


class EstimatedTaxesTypeDef(TypedDict):
    breakdown: NotRequired[list[TaxBreakdownItemTypeDef]]
    totalAmount: NotRequired[str]


FixedUpfrontPricingTermTypeDef = TypedDict(
    "FixedUpfrontPricingTermTypeDef",
    {
        "type": NotRequired[str],
        "id": NotRequired[str],
        "currencyCode": NotRequired[str],
        "duration": NotRequired[str],
        "price": NotRequired[str],
        "grants": NotRequired[list[GrantItemTypeDef]],
    },
)
FreeTrialPricingTermTypeDef = TypedDict(
    "FreeTrialPricingTermTypeDef",
    {
        "type": NotRequired[str],
        "id": NotRequired[str],
        "duration": NotRequired[str],
        "grants": NotRequired[list[GrantItemTypeDef]],
    },
)


class GetAgreementEntitlementsInputPaginateTypeDef(TypedDict):
    agreementId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetAgreementTermsInputPaginateTypeDef(TypedDict):
    agreementId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAgreementCancellationRequestsInputPaginateTypeDef(TypedDict):
    partyType: str
    agreementId: NotRequired[str]
    status: NotRequired[AgreementCancellationRequestStatusType]
    agreementType: NotRequired[str]
    catalog: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAgreementChargesInputPaginateTypeDef(TypedDict):
    catalog: NotRequired[str]
    agreementId: NotRequired[str]
    agreementType: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAgreementPaymentRequestsInputPaginateTypeDef(TypedDict):
    partyType: str
    agreementType: NotRequired[str]
    catalog: NotRequired[str]
    agreementId: NotRequired[str]
    status: NotRequired[PaymentRequestStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAgreementInvoiceLineItemsInputPaginateTypeDef(TypedDict):
    agreementId: str
    groupBy: Literal["INVOICE_ID"]
    invoiceId: NotRequired[str]
    invoiceType: NotRequired[InvoiceTypeType]
    invoiceBillingPeriod: NotRequired[InvoiceBillingPeriodTypeDef]
    beforeIssuedTime: NotRequired[TimestampTypeDef]
    afterIssuedTime: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAgreementInvoiceLineItemsInputTypeDef(TypedDict):
    agreementId: str
    groupBy: Literal["INVOICE_ID"]
    invoiceId: NotRequired[str]
    invoiceType: NotRequired[InvoiceTypeType]
    invoiceBillingPeriod: NotRequired[InvoiceBillingPeriodTypeDef]
    beforeIssuedTime: NotRequired[TimestampTypeDef]
    afterIssuedTime: NotRequired[TimestampTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListBillingAdjustmentRequestsInputPaginateTypeDef(TypedDict):
    agreementId: NotRequired[str]
    status: NotRequired[BillingAdjustmentStatusType]
    createdAfter: NotRequired[TimestampTypeDef]
    createdBefore: NotRequired[TimestampTypeDef]
    catalog: NotRequired[str]
    agreementType: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBillingAdjustmentRequestsInputTypeDef(TypedDict):
    agreementId: NotRequired[str]
    status: NotRequired[BillingAdjustmentStatusType]
    createdAfter: NotRequired[TimestampTypeDef]
    createdBefore: NotRequired[TimestampTypeDef]
    maxResults: NotRequired[int]
    catalog: NotRequired[str]
    agreementType: NotRequired[str]
    nextToken: NotRequired[str]


class ListAgreementPaymentRequestsOutputTypeDef(TypedDict):
    items: list[PaymentRequestSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class PaymentScheduleTermTemplateTypeDef(TypedDict):
    schedule: NotRequired[list[PaymentScheduleEntryTypeDef]]


PaymentScheduleTermTypeDef = TypedDict(
    "PaymentScheduleTermTypeDef",
    {
        "type": NotRequired[str],
        "id": NotRequired[str],
        "currencyCode": NotRequired[str],
        "schedule": NotRequired[list[ScheduleItemTypeDef]],
    },
)


class PriceIncreaseTypeDef(TypedDict):
    fixedPercentage: NotRequired[FixedPercentageTypeDef]
    percentageRange: NotRequired[PercentageRangeTypeDef]


VariablePaymentTermTypeDef = TypedDict(
    "VariablePaymentTermTypeDef",
    {
        "type": NotRequired[str],
        "id": NotRequired[str],
        "currencyCode": NotRequired[str],
        "maxTotalChargeAmount": NotRequired[str],
        "configuration": NotRequired[VariablePaymentTermConfigurationTypeDef],
    },
)


class SearchAgreementsInputPaginateTypeDef(TypedDict):
    catalog: NotRequired[str]
    filters: NotRequired[Sequence[FilterTypeDef]]
    sort: NotRequired[SortTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchAgreementsInputTypeDef(TypedDict):
    catalog: NotRequired[str]
    filters: NotRequired[Sequence[FilterTypeDef]]
    sort: NotRequired[SortTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class GetAgreementEntitlementsOutputTypeDef(TypedDict):
    agreementEntitlements: list[AgreementEntitlementTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class AgreementViewSummaryTypeDef(TypedDict):
    agreementId: NotRequired[str]
    acceptanceTime: NotRequired[datetime]
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]
    lastUpdateTime: NotRequired[datetime]
    agreementType: NotRequired[str]
    acceptor: NotRequired[AcceptorTypeDef]
    proposer: NotRequired[ProposerTypeDef]
    proposalSummary: NotRequired[ProposalSummaryTypeDef]
    status: NotRequired[AgreementStatusType]
    entitlements: NotRequired[list[EntitlementTypeDef]]
    initialAgreementId: NotRequired[str]
    endTimeBehaviorType: NotRequired[EndTimeBehaviorTypeType]
    endTimeBehaviorReasonCode: NotRequired[EndTimeBehaviorReasonCodeType]


class ListAgreementInvoiceLineItemsOutputTypeDef(TypedDict):
    agreementInvoiceLineItemGroupSummaries: list[AgreementInvoiceLineItemGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


ConfigurableUpfrontPricingTermConfigurationUnionTypeDef = Union[
    ConfigurableUpfrontPricingTermConfigurationTypeDef,
    ConfigurableUpfrontPricingTermConfigurationOutputTypeDef,
]
UsageBasedPricingTermTypeDef = TypedDict(
    "UsageBasedPricingTermTypeDef",
    {
        "type": NotRequired[str],
        "id": NotRequired[str],
        "currencyCode": NotRequired[str],
        "rateCards": NotRequired[list[UsageBasedRateCardItemTypeDef]],
    },
)
ConfigurableUpfrontPricingTermTypeDef = TypedDict(
    "ConfigurableUpfrontPricingTermTypeDef",
    {
        "type": NotRequired[str],
        "id": NotRequired[str],
        "currencyCode": NotRequired[str],
        "rateCards": NotRequired[list[ConfigurableUpfrontRateCardItemTypeDef]],
        "configuration": NotRequired[ConfigurableUpfrontPricingTermConfigurationOutputTypeDef],
    },
)


class DescribeAgreementOutputTypeDef(TypedDict):
    agreementId: str
    acceptor: AcceptorTypeDef
    proposer: ProposerTypeDef
    startTime: datetime
    endTime: datetime
    acceptanceTime: datetime
    agreementType: str
    estimatedCharges: EstimatedChargesTypeDef
    proposalSummary: ProposalSummaryTypeDef
    status: AgreementStatusType
    initialAgreementId: str
    endTimeBehavior: EndTimeBehaviorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


ExpectedChargeTypeDef = TypedDict(
    "ExpectedChargeTypeDef",
    {
        "id": NotRequired[str],
        "time": NotRequired[datetime],
        "amount": NotRequired[str],
        "amountAfterTax": NotRequired[str],
        "timing": NotRequired[TimingType],
        "estimatedTaxes": NotRequired[EstimatedTaxesTypeDef],
    },
)


class TermTemplateTypeDef(TypedDict):
    paymentScheduleTermTemplate: NotRequired[PaymentScheduleTermTemplateTypeDef]


class SearchAgreementsOutputTypeDef(TypedDict):
    agreementViewSummaries: list[AgreementViewSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class RequestedTermConfigurationTypeDef(TypedDict):
    configurableUpfrontPricingTermConfiguration: NotRequired[
        ConfigurableUpfrontPricingTermConfigurationUnionTypeDef
    ]
    renewalTermConfiguration: NotRequired[RenewalTermConfigurationTypeDef]
    variablePaymentTermConfiguration: NotRequired[VariablePaymentTermConfigurationTypeDef]


class ChargeSummaryTypeDef(TypedDict):
    currencyCode: NotRequired[str]
    newAgreementValue: NotRequired[str]
    newAgreementValueAfterTax: NotRequired[str]
    expectedCharges: NotRequired[list[ExpectedChargeTypeDef]]
    estimatedTaxes: NotRequired[EstimatedTaxesTypeDef]
    itemizedCharges: NotRequired[list[ItemizedChargeTypeDef]]
    invoicingEntity: NotRequired[InvoicingEntityTypeDef]


RenewalTermTypeDef = TypedDict(
    "RenewalTermTypeDef",
    {
        "type": NotRequired[str],
        "id": NotRequired[str],
        "configuration": NotRequired[RenewalTermConfigurationTypeDef],
        "lockoutPeriod": NotRequired[str],
        "maxRenewals": NotRequired[int],
        "adjustmentDeadline": NotRequired[str],
        "priceIncrease": NotRequired[PriceIncreaseTypeDef],
        "termTemplates": NotRequired[list[TermTemplateTypeDef]],
    },
)
RequestedTermTypeDef = TypedDict(
    "RequestedTermTypeDef",
    {
        "id": str,
        "configuration": NotRequired[RequestedTermConfigurationTypeDef],
    },
)


class CreateAgreementRequestOutputTypeDef(TypedDict):
    agreementRequestId: str
    chargeSummary: ChargeSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AcceptedTermTypeDef(TypedDict):
    legalTerm: NotRequired[LegalTermTypeDef]
    supportTerm: NotRequired[SupportTermTypeDef]
    renewalTerm: NotRequired[RenewalTermTypeDef]
    usageBasedPricingTerm: NotRequired[UsageBasedPricingTermTypeDef]
    configurableUpfrontPricingTerm: NotRequired[ConfigurableUpfrontPricingTermTypeDef]
    byolPricingTerm: NotRequired[ByolPricingTermTypeDef]
    recurringPaymentTerm: NotRequired[RecurringPaymentTermTypeDef]
    validityTerm: NotRequired[ValidityTermTypeDef]
    paymentScheduleTerm: NotRequired[PaymentScheduleTermTypeDef]
    freeTrialPricingTerm: NotRequired[FreeTrialPricingTermTypeDef]
    fixedUpfrontPricingTerm: NotRequired[FixedUpfrontPricingTermTypeDef]
    variablePaymentTerm: NotRequired[VariablePaymentTermTypeDef]
    netPaymentTerm: NotRequired[NetPaymentTermTypeDef]


class CreateAgreementRequestInputTypeDef(TypedDict):
    intent: IntentType
    requestedTerms: Sequence[RequestedTermTypeDef]
    clientToken: NotRequired[str]
    sourceAgreementIdentifier: NotRequired[str]
    agreementProposalIdentifier: NotRequired[str]
    taxConfiguration: NotRequired[TaxConfigurationTypeDef]


class GetAgreementTermsOutputTypeDef(TypedDict):
    acceptedTerms: list[AcceptedTermTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
