"""
Main interface for payments service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_payments/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_payments import (
        Client,
        GetAccountBalancePaginator,
        ListFinancialRecordsPaginator,
        ListPaymentInstrumentsPaginator,
        PaymentsClient,
    )

    session = Session()
    client: PaymentsClient = session.client("payments")

    get_account_balance_paginator: GetAccountBalancePaginator = client.get_paginator("get_account_balance")
    list_financial_records_paginator: ListFinancialRecordsPaginator = client.get_paginator("list_financial_records")
    list_payment_instruments_paginator: ListPaymentInstrumentsPaginator = client.get_paginator("list_payment_instruments")
    ```
"""

from .client import PaymentsClient
from .paginator import (
    GetAccountBalancePaginator,
    ListFinancialRecordsPaginator,
    ListPaymentInstrumentsPaginator,
)

Client = PaymentsClient

__all__ = (
    "Client",
    "GetAccountBalancePaginator",
    "ListFinancialRecordsPaginator",
    "ListPaymentInstrumentsPaginator",
    "PaymentsClient",
)
