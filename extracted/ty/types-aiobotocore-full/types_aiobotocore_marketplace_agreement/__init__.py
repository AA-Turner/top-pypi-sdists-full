"""
Main interface for marketplace-agreement service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_agreement/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_marketplace_agreement import (
        AgreementServiceClient,
        Client,
        ListAgreementCancellationRequestsPaginator,
        ListAgreementInvoiceLineItemsPaginator,
        ListAgreementPaymentRequestsPaginator,
        ListBillingAdjustmentRequestsPaginator,
    )

    session = get_session()
    async with session.create_client("marketplace-agreement") as client:
        client: AgreementServiceClient
        ...


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
