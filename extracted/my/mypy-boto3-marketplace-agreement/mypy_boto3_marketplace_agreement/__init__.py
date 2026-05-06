"""
Main interface for marketplace-agreement service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_marketplace_agreement import (
        AgreementServiceClient,
        Client,
        GetAgreementEntitlementsPaginator,
        GetAgreementTermsPaginator,
        ListAgreementCancellationRequestsPaginator,
        ListAgreementChargesPaginator,
        ListAgreementInvoiceLineItemsPaginator,
        ListAgreementPaymentRequestsPaginator,
        ListBillingAdjustmentRequestsPaginator,
        SearchAgreementsPaginator,
    )

    session = Session()
    client: AgreementServiceClient = session.client("marketplace-agreement")

    get_agreement_entitlements_paginator: GetAgreementEntitlementsPaginator = client.get_paginator("get_agreement_entitlements")
    get_agreement_terms_paginator: GetAgreementTermsPaginator = client.get_paginator("get_agreement_terms")
    list_agreement_cancellation_requests_paginator: ListAgreementCancellationRequestsPaginator = client.get_paginator("list_agreement_cancellation_requests")
    list_agreement_charges_paginator: ListAgreementChargesPaginator = client.get_paginator("list_agreement_charges")
    list_agreement_invoice_line_items_paginator: ListAgreementInvoiceLineItemsPaginator = client.get_paginator("list_agreement_invoice_line_items")
    list_agreement_payment_requests_paginator: ListAgreementPaymentRequestsPaginator = client.get_paginator("list_agreement_payment_requests")
    list_billing_adjustment_requests_paginator: ListBillingAdjustmentRequestsPaginator = client.get_paginator("list_billing_adjustment_requests")
    search_agreements_paginator: SearchAgreementsPaginator = client.get_paginator("search_agreements")
    ```
"""

from .client import AgreementServiceClient
from .paginator import (
    GetAgreementEntitlementsPaginator,
    GetAgreementTermsPaginator,
    ListAgreementCancellationRequestsPaginator,
    ListAgreementChargesPaginator,
    ListAgreementInvoiceLineItemsPaginator,
    ListAgreementPaymentRequestsPaginator,
    ListBillingAdjustmentRequestsPaginator,
    SearchAgreementsPaginator,
)

Client = AgreementServiceClient


__all__ = (
    "AgreementServiceClient",
    "Client",
    "GetAgreementEntitlementsPaginator",
    "GetAgreementTermsPaginator",
    "ListAgreementCancellationRequestsPaginator",
    "ListAgreementChargesPaginator",
    "ListAgreementInvoiceLineItemsPaginator",
    "ListAgreementPaymentRequestsPaginator",
    "ListBillingAdjustmentRequestsPaginator",
    "SearchAgreementsPaginator",
)
