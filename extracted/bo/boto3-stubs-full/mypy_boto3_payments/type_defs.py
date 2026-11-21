"""
Type annotations for payments service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payments/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_payments.type_defs import CurrencyAmountTypeDef

    data: CurrencyAmountTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from datetime import datetime
from typing import Union

from .literals import (
    BalanceTypeType,
    BankAccountTypeType,
    BatchErrorCodeType,
    CardBrandType,
    CardTypeType,
    DueStatusType,
    FinancialRecordStatusType,
    FinancialRecordTypeType,
    InvoiceFrequencyType,
    LineOfBusinessType,
    PaymentInstrumentStatusType,
    PaymentMethodType,
    SettlementStatusType,
    SortOrderType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AccountBalanceTypeDef",
    "BalancesTypeDef",
    "BatchGetFinancialRecordRequestTypeDef",
    "BatchGetFinancialRecordResponseTypeDef",
    "BillingPeriodTypeDef",
    "BusinessUnitTypeDef",
    "CardTypeDef",
    "CnBankRedirectTypeDef",
    "CreditMemoDetailsTypeDef",
    "CurrencyAmountTypeDef",
    "FinancialRecordDetailsTypeDef",
    "FinancialRecordErrorTypeDef",
    "FinancialRecordKeyTypeDef",
    "FinancialRecordSummaryTypeDef",
    "FinancialRecordTypeDef",
    "GetAccountBalanceRequestPaginateTypeDef",
    "GetAccountBalanceRequestTypeDef",
    "GetAccountBalanceResponseTypeDef",
    "GetFinancialRecordRequestTypeDef",
    "GetFinancialRecordResponseTypeDef",
    "GetPaymentInstrumentRequestTypeDef",
    "GetPaymentInstrumentResponseTypeDef",
    "InNetBankingTypeDef",
    "InvoiceDetailsTypeDef",
    "ListFinancialRecordsRequestPaginateTypeDef",
    "ListFinancialRecordsRequestTypeDef",
    "ListFinancialRecordsResponseTypeDef",
    "ListPaymentInstrumentsRequestPaginateTypeDef",
    "ListPaymentInstrumentsRequestTypeDef",
    "ListPaymentInstrumentsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PaymentInstrumentDetailsTypeDef",
    "PaymentInstrumentSummaryTypeDef",
    "PaymentInstrumentTypeDef",
    "ResponseMetadataTypeDef",
    "SepaBankAccountTypeDef",
    "TimestampTypeDef",
    "UkBacsBankAccountTypeDef",
    "UpiTypeDef",
    "UsAchBankAccountTypeDef",
)


class CurrencyAmountTypeDef(TypedDict):
    value: str
    currency: str


class FinancialRecordKeyTypeDef(TypedDict):
    identifier: NotRequired[str]
    invoiceIdentifier: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class BillingPeriodTypeDef(TypedDict):
    startDate: datetime
    endDate: datetime


class BusinessUnitTypeDef(TypedDict):
    merchantOfRecord: str
    lineOfBusiness: NotRequired[LineOfBusinessType]


class CardTypeDef(TypedDict):
    last4: str
    brand: NotRequired[CardBrandType]
    expirationMonth: NotRequired[int]
    expirationYear: NotRequired[int]
    cardType: NotRequired[CardTypeType]
    issuingBank: NotRequired[str]
    issuerCountry: NotRequired[str]


class CnBankRedirectTypeDef(TypedDict):
    bankCode: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class GetAccountBalanceRequestTypeDef(TypedDict):
    balanceType: BalanceTypeType
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class GetFinancialRecordRequestTypeDef(TypedDict):
    identifier: NotRequired[str]
    invoiceIdentifier: NotRequired[str]


class GetPaymentInstrumentRequestTypeDef(TypedDict):
    identifier: str


class InNetBankingTypeDef(TypedDict):
    bankCode: str
    bankName: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class ListPaymentInstrumentsRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


PaymentInstrumentSummaryTypeDef = TypedDict(
    "PaymentInstrumentSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "paymentMethod": PaymentMethodType,
        "status": PaymentInstrumentStatusType,
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
    },
)


class SepaBankAccountTypeDef(TypedDict):
    accountNumberTail: NotRequired[str]
    accountHolderName: NotRequired[str]
    bankName: NotRequired[str]
    accountType: NotRequired[BankAccountTypeType]


class UkBacsBankAccountTypeDef(TypedDict):
    accountNumberTail: NotRequired[str]
    accountHolderName: NotRequired[str]
    bankName: NotRequired[str]
    accountType: NotRequired[BankAccountTypeType]


class UpiTypeDef(TypedDict):
    appName: NotRequired[str]


class UsAchBankAccountTypeDef(TypedDict):
    accountNumberTail: NotRequired[str]
    accountHolderName: NotRequired[str]
    bankName: NotRequired[str]
    accountType: NotRequired[BankAccountTypeType]


class AccountBalanceTypeDef(TypedDict):
    amount: CurrencyAmountTypeDef
    merchantOfRecord: str


class BalancesTypeDef(TypedDict):
    outstanding: CurrencyAmountTypeDef
    processing: CurrencyAmountTypeDef
    settled: CurrencyAmountTypeDef
    canceled: CurrencyAmountTypeDef


class BatchGetFinancialRecordRequestTypeDef(TypedDict):
    keys: Sequence[FinancialRecordKeyTypeDef]


class FinancialRecordErrorTypeDef(TypedDict):
    key: FinancialRecordKeyTypeDef
    code: BatchErrorCodeType
    message: str


class CreditMemoDetailsTypeDef(TypedDict):
    invoiceId: str
    billingPeriod: BillingPeriodTypeDef


class InvoiceDetailsTypeDef(TypedDict):
    invoiceId: str
    billingPeriod: BillingPeriodTypeDef
    dueDate: datetime
    invoiceFrequency: InvoiceFrequencyType
    dueStatus: NotRequired[DueStatusType]
    paymentTerms: NotRequired[str]


class GetAccountBalanceRequestPaginateTypeDef(TypedDict):
    balanceType: BalanceTypeType
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPaymentInstrumentsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListFinancialRecordsRequestPaginateTypeDef = TypedDict(
    "ListFinancialRecordsRequestPaginateTypeDef",
    {
        "types": Sequence[FinancialRecordTypeType],
        "settlementStatuses": NotRequired[Sequence[SettlementStatusType]],
        "issuedAfter": NotRequired[TimestampTypeDef],
        "issuedBefore": NotRequired[TimestampTypeDef],
        "sortBy": NotRequired[Literal["ISSUED_AT"]],
        "sortOrder": NotRequired[SortOrderType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListFinancialRecordsRequestTypeDef = TypedDict(
    "ListFinancialRecordsRequestTypeDef",
    {
        "types": Sequence[FinancialRecordTypeType],
        "settlementStatuses": NotRequired[Sequence[SettlementStatusType]],
        "issuedAfter": NotRequired[TimestampTypeDef],
        "issuedBefore": NotRequired[TimestampTypeDef],
        "sortBy": NotRequired[Literal["ISSUED_AT"]],
        "sortOrder": NotRequired[SortOrderType],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)


class ListPaymentInstrumentsResponseTypeDef(TypedDict):
    paymentInstrumentSummaries: list[PaymentInstrumentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class PaymentInstrumentDetailsTypeDef(TypedDict):
    card: NotRequired[CardTypeDef]
    usAchBankAccount: NotRequired[UsAchBankAccountTypeDef]
    sepaBankAccount: NotRequired[SepaBankAccountTypeDef]
    ukBacsBankAccount: NotRequired[UkBacsBankAccountTypeDef]
    inNetBanking: NotRequired[InNetBankingTypeDef]
    cnBankRedirect: NotRequired[CnBankRedirectTypeDef]
    upi: NotRequired[UpiTypeDef]


class GetAccountBalanceResponseTypeDef(TypedDict):
    accountBalances: list[AccountBalanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


FinancialRecordSummaryTypeDef = TypedDict(
    "FinancialRecordSummaryTypeDef",
    {
        "id": str,
        "type": FinancialRecordTypeType,
        "businessUnit": BusinessUnitTypeDef,
        "amount": CurrencyAmountTypeDef,
        "balances": BalancesTypeDef,
        "settlementStatus": SettlementStatusType,
        "status": FinancialRecordStatusType,
        "issuedAt": datetime,
        "closedAt": NotRequired[datetime],
    },
)


class FinancialRecordDetailsTypeDef(TypedDict):
    invoiceDetails: NotRequired[InvoiceDetailsTypeDef]
    creditMemoDetails: NotRequired[CreditMemoDetailsTypeDef]


class PaymentInstrumentTypeDef(TypedDict):
    arn: str
    paymentMethod: PaymentMethodType
    status: PaymentInstrumentStatusType
    details: NotRequired[PaymentInstrumentDetailsTypeDef]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]


class ListFinancialRecordsResponseTypeDef(TypedDict):
    financialRecordSummaries: list[FinancialRecordSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


FinancialRecordTypeDef = TypedDict(
    "FinancialRecordTypeDef",
    {
        "id": str,
        "type": FinancialRecordTypeType,
        "businessUnit": BusinessUnitTypeDef,
        "amount": CurrencyAmountTypeDef,
        "balances": BalancesTypeDef,
        "settlementStatus": SettlementStatusType,
        "status": FinancialRecordStatusType,
        "issuedAt": datetime,
        "details": FinancialRecordDetailsTypeDef,
        "closedAt": NotRequired[datetime],
    },
)


class GetPaymentInstrumentResponseTypeDef(TypedDict):
    paymentInstrument: PaymentInstrumentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class BatchGetFinancialRecordResponseTypeDef(TypedDict):
    financialRecords: list[FinancialRecordTypeDef]
    errors: list[FinancialRecordErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetFinancialRecordResponseTypeDef(TypedDict):
    financialRecord: FinancialRecordTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
