"""
Main interface for invoicing service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_invoicing/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_invoicing import (
        Client,
        InvoicingClient,
        ListInvoiceSummariesPaginator,
        ListInvoiceUnitsPaginator,
    )

    session = get_session()
    async with session.create_client("invoicing") as client:
        client: InvoicingClient
        ...


    list_invoice_summaries_paginator: ListInvoiceSummariesPaginator = client.get_paginator("list_invoice_summaries")
    list_invoice_units_paginator: ListInvoiceUnitsPaginator = client.get_paginator("list_invoice_units")
    ```
"""

from .client import InvoicingClient
from .paginator import ListInvoiceSummariesPaginator, ListInvoiceUnitsPaginator

Client = InvoicingClient


__all__ = (
    "Client",
    "InvoicingClient",
    "ListInvoiceSummariesPaginator",
    "ListInvoiceUnitsPaginator",
)
