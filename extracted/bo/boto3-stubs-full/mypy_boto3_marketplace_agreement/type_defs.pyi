"""
Type annotations for marketplace-agreement service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_marketplace_agreement.type_defs import ByolPricingTermTypeDef

    data: ByolPricingTermTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from datetime import datetime

from .literals import AgreementStatusType, PaymentRequestApprovalStrategyType, SortOrderType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AcceptedTermTypeDef",
    "AcceptorTypeDef",
    "AgreementViewSummaryTypeDef",
    "ByolPricingTermTypeDef",
    "ConfigurableUpfrontPricingTermConfigurationTypeDef",
    "ConfigurableUpfrontPricingTermTypeDef",
    "ConfigurableUpfrontRateCardItemTypeDef",
    "ConstraintsTypeDef",
    "DescribeAgreementInputTypeDef",
    "DescribeAgreementOutputTypeDef",
    "DimensionTypeDef",
    "DocumentItemTypeDef",
    "EstimatedChargesTypeDef",
    "FilterTypeDef",
    "FixedUpfrontPricingTermTypeDef",
    "FreeTrialPricingTermTypeDef",
    "GetAgreementTermsInputTypeDef",
    "GetAgreementTermsOutputTypeDef",
    "GrantItemTypeDef",
    "LegalTermTypeDef",
    "PaymentScheduleTermTypeDef",
    "ProposalSummaryTypeDef",
    "ProposerTypeDef",
    "RateCardItemTypeDef",
    "RecurringPaymentTermTypeDef",
    "RenewalTermConfigurationTypeDef",
    "RenewalTermTypeDef",
    "ResourceTypeDef",
    "ResponseMetadataTypeDef",
    "ScheduleItemTypeDef",
    "SearchAgreementsInputTypeDef",
    "SearchAgreementsOutputTypeDef",
    "SelectorTypeDef",
    "SortTypeDef",
    "SupportTermTypeDef",
    "UsageBasedPricingTermTypeDef",
    "UsageBasedRateCardItemTypeDef",
    "ValidityTermTypeDef",
    "VariablePaymentTermConfigurationTypeDef",
    "VariablePaymentTermTypeDef",
)

ByolPricingTermTypeDef = TypedDict(
    "ByolPricingTermTypeDef",
    {
        "type": NotRequired[str],
    },
)
RecurringPaymentTermTypeDef = TypedDict(
    "RecurringPaymentTermTypeDef",
    {
        "type": NotRequired[str],
        "currencyCode": NotRequired[str],
        "billingPeriod": NotRequired[str],
        "price": NotRequired[str],
    },
)
SupportTermTypeDef = TypedDict(
    "SupportTermTypeDef",
    {
        "type": NotRequired[str],
        "refundPolicy": NotRequired[str],
    },
)
ValidityTermTypeDef = TypedDict(
    "ValidityTermTypeDef",
    {
        "type": NotRequired[str],
        "agreementDuration": NotRequired[str],
        "agreementStartDate": NotRequired[datetime],
        "agreementEndDate": NotRequired[datetime],
    },
)

class AcceptorTypeDef(TypedDict):
    accountId: NotRequired[str]

class ProposerTypeDef(TypedDict):
    accountId: NotRequired[str]

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

class DescribeAgreementInputTypeDef(TypedDict):
    agreementId: str

class EstimatedChargesTypeDef(TypedDict):
    currencyCode: NotRequired[str]
    agreementValue: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

DocumentItemTypeDef = TypedDict(
    "DocumentItemTypeDef",
    {
        "type": NotRequired[str],
        "url": NotRequired[str],
        "version": NotRequired[str],
    },
)

class FilterTypeDef(TypedDict):
    name: NotRequired[str]
    values: NotRequired[Sequence[str]]

class GrantItemTypeDef(TypedDict):
    dimensionKey: NotRequired[str]
    maxQuantity: NotRequired[int]

class GetAgreementTermsInputTypeDef(TypedDict):
    agreementId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ScheduleItemTypeDef(TypedDict):
    chargeDate: NotRequired[datetime]
    chargeAmount: NotRequired[str]

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "id": NotRequired[str],
        "type": NotRequired[str],
    },
)

class RenewalTermConfigurationTypeDef(TypedDict):
    enableAutoRenew: bool

class SortTypeDef(TypedDict):
    sortBy: NotRequired[str]
    sortOrder: NotRequired[SortOrderType]

class VariablePaymentTermConfigurationTypeDef(TypedDict):
    paymentRequestApprovalStrategy: PaymentRequestApprovalStrategyType
    expirationDuration: NotRequired[str]

class ConfigurableUpfrontPricingTermConfigurationTypeDef(TypedDict):
    selectorValue: str
    dimensions: list[DimensionTypeDef]

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
        "documents": NotRequired[list[DocumentItemTypeDef]],
    },
)
FixedUpfrontPricingTermTypeDef = TypedDict(
    "FixedUpfrontPricingTermTypeDef",
    {
        "type": NotRequired[str],
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
        "duration": NotRequired[str],
        "grants": NotRequired[list[GrantItemTypeDef]],
    },
)
PaymentScheduleTermTypeDef = TypedDict(
    "PaymentScheduleTermTypeDef",
    {
        "type": NotRequired[str],
        "currencyCode": NotRequired[str],
        "schedule": NotRequired[list[ScheduleItemTypeDef]],
    },
)

class ProposalSummaryTypeDef(TypedDict):
    resources: NotRequired[list[ResourceTypeDef]]
    offerId: NotRequired[str]
    offerSetId: NotRequired[str]

RenewalTermTypeDef = TypedDict(
    "RenewalTermTypeDef",
    {
        "type": NotRequired[str],
        "configuration": NotRequired[RenewalTermConfigurationTypeDef],
    },
)

class SearchAgreementsInputTypeDef(TypedDict):
    catalog: NotRequired[str]
    filters: NotRequired[Sequence[FilterTypeDef]]
    sort: NotRequired[SortTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

VariablePaymentTermTypeDef = TypedDict(
    "VariablePaymentTermTypeDef",
    {
        "type": NotRequired[str],
        "currencyCode": NotRequired[str],
        "maxTotalChargeAmount": NotRequired[str],
        "configuration": NotRequired[VariablePaymentTermConfigurationTypeDef],
    },
)
UsageBasedPricingTermTypeDef = TypedDict(
    "UsageBasedPricingTermTypeDef",
    {
        "type": NotRequired[str],
        "currencyCode": NotRequired[str],
        "rateCards": NotRequired[list[UsageBasedRateCardItemTypeDef]],
    },
)
ConfigurableUpfrontPricingTermTypeDef = TypedDict(
    "ConfigurableUpfrontPricingTermTypeDef",
    {
        "type": NotRequired[str],
        "currencyCode": NotRequired[str],
        "rateCards": NotRequired[list[ConfigurableUpfrontRateCardItemTypeDef]],
        "configuration": NotRequired[ConfigurableUpfrontPricingTermConfigurationTypeDef],
    },
)

class AgreementViewSummaryTypeDef(TypedDict):
    agreementId: NotRequired[str]
    acceptanceTime: NotRequired[datetime]
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]
    agreementType: NotRequired[str]
    acceptor: NotRequired[AcceptorTypeDef]
    proposer: NotRequired[ProposerTypeDef]
    proposalSummary: NotRequired[ProposalSummaryTypeDef]
    status: NotRequired[AgreementStatusType]

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

class SearchAgreementsOutputTypeDef(TypedDict):
    agreementViewSummaries: list[AgreementViewSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetAgreementTermsOutputTypeDef(TypedDict):
    acceptedTerms: list[AcceptedTermTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
