"""
Type annotations for invoicing service type definitions.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_invoicing/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from types_aiobotocore_invoicing.type_defs import BatchGetInvoiceProfileRequestTypeDef

    data: BatchGetInvoiceProfileRequestTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Union

from .literals import InvoiceTypeType, ListInvoiceSummariesResourceTypeType

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import list as List
    from collections.abc import Sequence
else:
    from typing import Dict, List, Sequence
if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AmountBreakdownTypeDef",
    "BatchGetInvoiceProfileRequestTypeDef",
    "BatchGetInvoiceProfileResponseTypeDef",
    "BillingPeriodTypeDef",
    "CreateInvoiceUnitRequestTypeDef",
    "CreateInvoiceUnitResponseTypeDef",
    "CurrencyExchangeDetailsTypeDef",
    "DateIntervalTypeDef",
    "DeleteInvoiceUnitRequestTypeDef",
    "DeleteInvoiceUnitResponseTypeDef",
    "DiscountsBreakdownAmountTypeDef",
    "DiscountsBreakdownTypeDef",
    "EntityTypeDef",
    "FeesBreakdownAmountTypeDef",
    "FeesBreakdownTypeDef",
    "FiltersTypeDef",
    "GetInvoiceUnitRequestTypeDef",
    "GetInvoiceUnitResponseTypeDef",
    "InvoiceCurrencyAmountTypeDef",
    "InvoiceProfileTypeDef",
    "InvoiceSummariesFilterTypeDef",
    "InvoiceSummariesSelectorTypeDef",
    "InvoiceSummaryTypeDef",
    "InvoiceUnitRuleOutputTypeDef",
    "InvoiceUnitRuleTypeDef",
    "InvoiceUnitRuleUnionTypeDef",
    "InvoiceUnitTypeDef",
    "ListInvoiceSummariesRequestPaginateTypeDef",
    "ListInvoiceSummariesRequestTypeDef",
    "ListInvoiceSummariesResponseTypeDef",
    "ListInvoiceUnitsRequestPaginateTypeDef",
    "ListInvoiceUnitsRequestTypeDef",
    "ListInvoiceUnitsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ReceiverAddressTypeDef",
    "ResourceTagTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestTypeDef",
    "TaxesBreakdownAmountTypeDef",
    "TaxesBreakdownTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateInvoiceUnitRequestTypeDef",
    "UpdateInvoiceUnitResponseTypeDef",
)


class BatchGetInvoiceProfileRequestTypeDef(TypedDict):
    AccountIds: Sequence[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class BillingPeriodTypeDef(TypedDict):
    Month: int
    Year: int


class ResourceTagTypeDef(TypedDict):
    Key: str
    Value: str


class CurrencyExchangeDetailsTypeDef(TypedDict):
    SourceCurrencyCode: NotRequired[str]
    TargetCurrencyCode: NotRequired[str]
    Rate: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class DeleteInvoiceUnitRequestTypeDef(TypedDict):
    InvoiceUnitArn: str


class DiscountsBreakdownAmountTypeDef(TypedDict):
    Description: NotRequired[str]
    Amount: NotRequired[str]
    Rate: NotRequired[str]


class EntityTypeDef(TypedDict):
    InvoicingEntity: NotRequired[str]


class FeesBreakdownAmountTypeDef(TypedDict):
    Description: NotRequired[str]
    Amount: NotRequired[str]
    Rate: NotRequired[str]


class FiltersTypeDef(TypedDict):
    Names: NotRequired[Sequence[str]]
    InvoiceReceivers: NotRequired[Sequence[str]]
    Accounts: NotRequired[Sequence[str]]


class InvoiceUnitRuleOutputTypeDef(TypedDict):
    LinkedAccounts: NotRequired[List[str]]


class ReceiverAddressTypeDef(TypedDict):
    AddressLine1: NotRequired[str]
    AddressLine2: NotRequired[str]
    AddressLine3: NotRequired[str]
    DistrictOrCounty: NotRequired[str]
    City: NotRequired[str]
    StateOrRegion: NotRequired[str]
    CountryCode: NotRequired[str]
    CompanyName: NotRequired[str]
    PostalCode: NotRequired[str]


class InvoiceSummariesSelectorTypeDef(TypedDict):
    ResourceType: ListInvoiceSummariesResourceTypeType
    Value: str


class InvoiceUnitRuleTypeDef(TypedDict):
    LinkedAccounts: NotRequired[Sequence[str]]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListTagsForResourceRequestTypeDef(TypedDict):
    ResourceArn: str


class TaxesBreakdownAmountTypeDef(TypedDict):
    Description: NotRequired[str]
    Amount: NotRequired[str]
    Rate: NotRequired[str]


class UntagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    ResourceTagKeys: Sequence[str]


class CreateInvoiceUnitResponseTypeDef(TypedDict):
    InvoiceUnitArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteInvoiceUnitResponseTypeDef(TypedDict):
    InvoiceUnitArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateInvoiceUnitResponseTypeDef(TypedDict):
    InvoiceUnitArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    ResourceTags: List[ResourceTagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    ResourceTags: Sequence[ResourceTagTypeDef]


class DateIntervalTypeDef(TypedDict):
    StartDate: TimestampTypeDef
    EndDate: TimestampTypeDef


class GetInvoiceUnitRequestTypeDef(TypedDict):
    InvoiceUnitArn: str
    AsOf: NotRequired[TimestampTypeDef]


class DiscountsBreakdownTypeDef(TypedDict):
    Breakdown: NotRequired[List[DiscountsBreakdownAmountTypeDef]]
    TotalAmount: NotRequired[str]


class FeesBreakdownTypeDef(TypedDict):
    Breakdown: NotRequired[List[FeesBreakdownAmountTypeDef]]
    TotalAmount: NotRequired[str]


class ListInvoiceUnitsRequestTypeDef(TypedDict):
    Filters: NotRequired[FiltersTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    AsOf: NotRequired[TimestampTypeDef]


class GetInvoiceUnitResponseTypeDef(TypedDict):
    InvoiceUnitArn: str
    InvoiceReceiver: str
    Name: str
    Description: str
    TaxInheritanceDisabled: bool
    Rule: InvoiceUnitRuleOutputTypeDef
    LastModified: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class InvoiceUnitTypeDef(TypedDict):
    InvoiceUnitArn: NotRequired[str]
    InvoiceReceiver: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    TaxInheritanceDisabled: NotRequired[bool]
    Rule: NotRequired[InvoiceUnitRuleOutputTypeDef]
    LastModified: NotRequired[datetime]


class InvoiceProfileTypeDef(TypedDict):
    AccountId: NotRequired[str]
    ReceiverName: NotRequired[str]
    ReceiverAddress: NotRequired[ReceiverAddressTypeDef]
    ReceiverEmail: NotRequired[str]
    Issuer: NotRequired[str]
    TaxRegistrationNumber: NotRequired[str]


InvoiceUnitRuleUnionTypeDef = Union[InvoiceUnitRuleTypeDef, InvoiceUnitRuleOutputTypeDef]


class ListInvoiceUnitsRequestPaginateTypeDef(TypedDict):
    Filters: NotRequired[FiltersTypeDef]
    AsOf: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class TaxesBreakdownTypeDef(TypedDict):
    Breakdown: NotRequired[List[TaxesBreakdownAmountTypeDef]]
    TotalAmount: NotRequired[str]


class InvoiceSummariesFilterTypeDef(TypedDict):
    TimeInterval: NotRequired[DateIntervalTypeDef]
    BillingPeriod: NotRequired[BillingPeriodTypeDef]
    InvoicingEntity: NotRequired[str]


class ListInvoiceUnitsResponseTypeDef(TypedDict):
    InvoiceUnits: List[InvoiceUnitTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class BatchGetInvoiceProfileResponseTypeDef(TypedDict):
    Profiles: List[InvoiceProfileTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateInvoiceUnitRequestTypeDef(TypedDict):
    Name: str
    InvoiceReceiver: str
    Rule: InvoiceUnitRuleUnionTypeDef
    Description: NotRequired[str]
    TaxInheritanceDisabled: NotRequired[bool]
    ResourceTags: NotRequired[Sequence[ResourceTagTypeDef]]


class UpdateInvoiceUnitRequestTypeDef(TypedDict):
    InvoiceUnitArn: str
    Description: NotRequired[str]
    TaxInheritanceDisabled: NotRequired[bool]
    Rule: NotRequired[InvoiceUnitRuleUnionTypeDef]


class AmountBreakdownTypeDef(TypedDict):
    SubTotalAmount: NotRequired[str]
    Discounts: NotRequired[DiscountsBreakdownTypeDef]
    Taxes: NotRequired[TaxesBreakdownTypeDef]
    Fees: NotRequired[FeesBreakdownTypeDef]


class ListInvoiceSummariesRequestPaginateTypeDef(TypedDict):
    Selector: InvoiceSummariesSelectorTypeDef
    Filter: NotRequired[InvoiceSummariesFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListInvoiceSummariesRequestTypeDef(TypedDict):
    Selector: InvoiceSummariesSelectorTypeDef
    Filter: NotRequired[InvoiceSummariesFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class InvoiceCurrencyAmountTypeDef(TypedDict):
    TotalAmount: NotRequired[str]
    TotalAmountBeforeTax: NotRequired[str]
    CurrencyCode: NotRequired[str]
    AmountBreakdown: NotRequired[AmountBreakdownTypeDef]
    CurrencyExchangeDetails: NotRequired[CurrencyExchangeDetailsTypeDef]


class InvoiceSummaryTypeDef(TypedDict):
    AccountId: NotRequired[str]
    InvoiceId: NotRequired[str]
    IssuedDate: NotRequired[datetime]
    DueDate: NotRequired[datetime]
    Entity: NotRequired[EntityTypeDef]
    BillingPeriod: NotRequired[BillingPeriodTypeDef]
    InvoiceType: NotRequired[InvoiceTypeType]
    OriginalInvoiceId: NotRequired[str]
    PurchaseOrderNumber: NotRequired[str]
    BaseCurrencyAmount: NotRequired[InvoiceCurrencyAmountTypeDef]
    TaxCurrencyAmount: NotRequired[InvoiceCurrencyAmountTypeDef]
    PaymentCurrencyAmount: NotRequired[InvoiceCurrencyAmountTypeDef]


class ListInvoiceSummariesResponseTypeDef(TypedDict):
    InvoiceSummaries: List[InvoiceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
