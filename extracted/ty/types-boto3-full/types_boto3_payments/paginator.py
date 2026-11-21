"""
Type annotations for payments service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_payments/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_payments.client import PaymentsClient
    from types_boto3_payments.paginator import (
        GetAccountBalancePaginator,
        ListFinancialRecordsPaginator,
        ListPaymentInstrumentsPaginator,
    )

    session = Session()
    client: PaymentsClient = session.client("payments")

    get_account_balance_paginator: GetAccountBalancePaginator = client.get_paginator("get_account_balance")
    list_financial_records_paginator: ListFinancialRecordsPaginator = client.get_paginator("list_financial_records")
    list_payment_instruments_paginator: ListPaymentInstrumentsPaginator = client.get_paginator("list_payment_instruments")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetAccountBalanceRequestPaginateTypeDef,
    GetAccountBalanceResponseTypeDef,
    ListFinancialRecordsRequestPaginateTypeDef,
    ListFinancialRecordsResponseTypeDef,
    ListPaymentInstrumentsRequestPaginateTypeDef,
    ListPaymentInstrumentsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetAccountBalancePaginator",
    "ListFinancialRecordsPaginator",
    "ListPaymentInstrumentsPaginator",
)


if TYPE_CHECKING:
    _GetAccountBalancePaginatorBase = Paginator[GetAccountBalanceResponseTypeDef]
else:
    _GetAccountBalancePaginatorBase = Paginator  # type: ignore[assignment]


class GetAccountBalancePaginator(_GetAccountBalancePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payments/paginator/GetAccountBalance.html#Payments.Paginator.GetAccountBalance)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_payments/paginators/#getaccountbalancepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetAccountBalanceRequestPaginateTypeDef]
    ) -> PageIterator[GetAccountBalanceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payments/paginator/GetAccountBalance.html#Payments.Paginator.GetAccountBalance.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_payments/paginators/#getaccountbalancepaginator)
        """


if TYPE_CHECKING:
    _ListFinancialRecordsPaginatorBase = Paginator[ListFinancialRecordsResponseTypeDef]
else:
    _ListFinancialRecordsPaginatorBase = Paginator  # type: ignore[assignment]


class ListFinancialRecordsPaginator(_ListFinancialRecordsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payments/paginator/ListFinancialRecords.html#Payments.Paginator.ListFinancialRecords)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_payments/paginators/#listfinancialrecordspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFinancialRecordsRequestPaginateTypeDef]
    ) -> PageIterator[ListFinancialRecordsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payments/paginator/ListFinancialRecords.html#Payments.Paginator.ListFinancialRecords.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_payments/paginators/#listfinancialrecordspaginator)
        """


if TYPE_CHECKING:
    _ListPaymentInstrumentsPaginatorBase = Paginator[ListPaymentInstrumentsResponseTypeDef]
else:
    _ListPaymentInstrumentsPaginatorBase = Paginator  # type: ignore[assignment]


class ListPaymentInstrumentsPaginator(_ListPaymentInstrumentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payments/paginator/ListPaymentInstruments.html#Payments.Paginator.ListPaymentInstruments)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_payments/paginators/#listpaymentinstrumentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPaymentInstrumentsRequestPaginateTypeDef]
    ) -> PageIterator[ListPaymentInstrumentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payments/paginator/ListPaymentInstruments.html#Payments.Paginator.ListPaymentInstruments.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_payments/paginators/#listpaymentinstrumentspaginator)
        """
