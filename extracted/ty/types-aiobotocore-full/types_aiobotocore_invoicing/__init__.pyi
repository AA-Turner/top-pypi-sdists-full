"""
Main interface for invoicing service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_invoicing/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_invoicing import (
        Client,
        InvoicingClient,
        ListInvoiceSummariesPaginator,
        ListInvoiceUnitsPaginator,
        ListProcurementPortalPreferencesPaginator,
        ListProcurementPortalSuppliersPaginator,
        ListProcurementPortalsPaginator,
    )

    session = get_session()
    async with session.create_client("invoicing") as client:
        client: InvoicingClient
        ...


    list_invoice_summaries_paginator: ListInvoiceSummariesPaginator = client.get_paginator("list_invoice_summaries")
    list_invoice_units_paginator: ListInvoiceUnitsPaginator = client.get_paginator("list_invoice_units")
    list_procurement_portal_preferences_paginator: ListProcurementPortalPreferencesPaginator = client.get_paginator("list_procurement_portal_preferences")
    list_procurement_portal_suppliers_paginator: ListProcurementPortalSuppliersPaginator = client.get_paginator("list_procurement_portal_suppliers")
    list_procurement_portals_paginator: ListProcurementPortalsPaginator = client.get_paginator("list_procurement_portals")
    ```
"""

from .client import InvoicingClient
from .paginator import (
    ListInvoiceSummariesPaginator,
    ListInvoiceUnitsPaginator,
    ListProcurementPortalPreferencesPaginator,
    ListProcurementPortalsPaginator,
    ListProcurementPortalSuppliersPaginator,
)

Client = InvoicingClient

__all__ = (
    "Client",
    "InvoicingClient",
    "ListInvoiceSummariesPaginator",
    "ListInvoiceUnitsPaginator",
    "ListProcurementPortalPreferencesPaginator",
    "ListProcurementPortalSuppliersPaginator",
    "ListProcurementPortalsPaginator",
)
