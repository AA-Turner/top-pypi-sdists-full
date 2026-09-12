"""
Main interface for invoicing service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_invoicing/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_invoicing import (
        Client,
        InvoicingClient,
        ListInvoiceSummariesPaginator,
        ListInvoiceUnitsPaginator,
        ListProcurementPortalPreferencesPaginator,
        ListProcurementPortalSuppliersPaginator,
        ListProcurementPortalsPaginator,
    )

    session = Session()
    client: InvoicingClient = session.client("invoicing")

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
