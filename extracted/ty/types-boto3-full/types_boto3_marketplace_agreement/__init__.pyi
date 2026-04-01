"""
Main interface for marketplace-agreement service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_marketplace_agreement import (
        AgreementServiceClient,
        Client,
        ListAgreementCancellationRequestsPaginator,
        ListAgreementInvoiceLineItemsPaginator,
        ListAgreementPaymentRequestsPaginator,
        ListBillingAdjustmentRequestsPaginator,
    )

    session = Session()
    client: AgreementServiceClient = session.client("marketplace-agreement")

    list_agreement_cancellation_requests_paginator: ListAgreementCancellationRequestsPaginator = client.get_paginator("list_agreement_cancellation_requests")
    list_agreement_invoice_line_items_paginator: ListAgreementInvoiceLineItemsPaginator = client.get_paginator("list_agreement_invoice_line_items")
    list_agreement_payment_requests_paginator: ListAgreementPaymentRequestsPaginator = client.get_paginator("list_agreement_payment_requests")
    list_billing_adjustment_requests_paginator: ListBillingAdjustmentRequestsPaginator = client.get_paginator("list_billing_adjustment_requests")
    ```
"""

from .client import AgreementServiceClient
from .paginator import (
    ListAgreementCancellationRequestsPaginator,
    ListAgreementInvoiceLineItemsPaginator,
    ListAgreementPaymentRequestsPaginator,
    ListBillingAdjustmentRequestsPaginator,
)

Client = AgreementServiceClient

__all__ = (
    "AgreementServiceClient",
    "Client",
    "ListAgreementCancellationRequestsPaginator",
    "ListAgreementInvoiceLineItemsPaginator",
    "ListAgreementPaymentRequestsPaginator",
    "ListBillingAdjustmentRequestsPaginator",
)
