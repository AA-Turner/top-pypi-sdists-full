"""
Type annotations for payments service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payments/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_payments.client import PaymentsClient

    session = Session()
    client: PaymentsClient = session.client("payments")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    GetAccountBalancePaginator,
    ListFinancialRecordsPaginator,
    ListPaymentInstrumentsPaginator,
)
from .type_defs import (
    BatchGetFinancialRecordRequestTypeDef,
    BatchGetFinancialRecordResponseTypeDef,
    GetAccountBalanceRequestTypeDef,
    GetAccountBalanceResponseTypeDef,
    GetFinancialRecordRequestTypeDef,
    GetFinancialRecordResponseTypeDef,
    GetPaymentInstrumentRequestTypeDef,
    GetPaymentInstrumentResponseTypeDef,
    ListFinancialRecordsRequestTypeDef,
    ListFinancialRecordsResponseTypeDef,
    ListPaymentInstrumentsRequestTypeDef,
    ListPaymentInstrumentsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("PaymentsClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class PaymentsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payments.html#Payments.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payments/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PaymentsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payments.html#Payments.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payments/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payments/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payments/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payments/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payments/client/#generate_presigned_url)
        """

    def batch_get_financial_record(
        self, **kwargs: Unpack[BatchGetFinancialRecordRequestTypeDef]
    ) -> BatchGetFinancialRecordResponseTypeDef:
        """
        Retrieves up to 100 financial records in one request, including the details
        that are specific to each record's type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payments/client/batch_get_financial_record.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payments/client/#batch_get_financial_record)
        """

    def get_account_balance(
        self, **kwargs: Unpack[GetAccountBalanceRequestTypeDef]
    ) -> GetAccountBalanceResponseTypeDef:
        """
        Retrieves one balance of your account, selected by balance type, as one amount
        for each merchant of record and currency.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payments/client/get_account_balance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payments/client/#get_account_balance)
        """

    def get_financial_record(
        self, **kwargs: Unpack[GetFinancialRecordRequestTypeDef]
    ) -> GetFinancialRecordResponseTypeDef:
        """
        Retrieves a single financial record, including the details that are specific to
        its type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payments/client/get_financial_record.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payments/client/#get_financial_record)
        """

    def get_payment_instrument(
        self, **kwargs: Unpack[GetPaymentInstrumentRequestTypeDef]
    ) -> GetPaymentInstrumentResponseTypeDef:
        """
        Retrieves a payment instrument on your account, including the details that are
        specific to its payment method, such as a card's last four digits.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payments/client/get_payment_instrument.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payments/client/#get_payment_instrument)
        """

    def list_financial_records(
        self, **kwargs: Unpack[ListFinancialRecordsRequestTypeDef]
    ) -> ListFinancialRecordsResponseTypeDef:
        """
        Lists the financial records on your account, with the newest first by default.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payments/client/list_financial_records.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payments/client/#list_financial_records)
        """

    def list_payment_instruments(
        self, **kwargs: Unpack[ListPaymentInstrumentsRequestTypeDef]
    ) -> ListPaymentInstrumentsResponseTypeDef:
        """
        Lists the payment instruments on your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payments/client/list_payment_instruments.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payments/client/#list_payment_instruments)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_account_balance"]
    ) -> GetAccountBalancePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payments/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payments/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_financial_records"]
    ) -> ListFinancialRecordsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payments/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payments/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_payment_instruments"]
    ) -> ListPaymentInstrumentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payments/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payments/client/#get_paginator)
        """
