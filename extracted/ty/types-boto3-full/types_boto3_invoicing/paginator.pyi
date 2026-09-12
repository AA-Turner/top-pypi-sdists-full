"""
Type annotations for invoicing service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_invoicing/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_invoicing.client import InvoicingClient
    from types_boto3_invoicing.paginator import (
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

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListInvoiceSummariesRequestPaginateTypeDef,
    ListInvoiceSummariesResponseTypeDef,
    ListInvoiceUnitsRequestPaginateTypeDef,
    ListInvoiceUnitsResponseTypeDef,
    ListProcurementPortalPreferencesRequestPaginateTypeDef,
    ListProcurementPortalPreferencesResponseTypeDef,
    ListProcurementPortalsRequestPaginateTypeDef,
    ListProcurementPortalsResponseTypeDef,
    ListProcurementPortalSuppliersRequestPaginateTypeDef,
    ListProcurementPortalSuppliersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListInvoiceSummariesPaginator",
    "ListInvoiceUnitsPaginator",
    "ListProcurementPortalPreferencesPaginator",
    "ListProcurementPortalSuppliersPaginator",
    "ListProcurementPortalsPaginator",
)

if TYPE_CHECKING:
    _ListInvoiceSummariesPaginatorBase = Paginator[ListInvoiceSummariesResponseTypeDef]
else:
    _ListInvoiceSummariesPaginatorBase = Paginator  # type: ignore[assignment]

class ListInvoiceSummariesPaginator(_ListInvoiceSummariesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/invoicing/paginator/ListInvoiceSummaries.html#Invoicing.Paginator.ListInvoiceSummaries)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_invoicing/paginators/#listinvoicesummariespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInvoiceSummariesRequestPaginateTypeDef]
    ) -> PageIterator[ListInvoiceSummariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/invoicing/paginator/ListInvoiceSummaries.html#Invoicing.Paginator.ListInvoiceSummaries.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_invoicing/paginators/#listinvoicesummariespaginator)
        """

if TYPE_CHECKING:
    _ListInvoiceUnitsPaginatorBase = Paginator[ListInvoiceUnitsResponseTypeDef]
else:
    _ListInvoiceUnitsPaginatorBase = Paginator  # type: ignore[assignment]

class ListInvoiceUnitsPaginator(_ListInvoiceUnitsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/invoicing/paginator/ListInvoiceUnits.html#Invoicing.Paginator.ListInvoiceUnits)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_invoicing/paginators/#listinvoiceunitspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInvoiceUnitsRequestPaginateTypeDef]
    ) -> PageIterator[ListInvoiceUnitsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/invoicing/paginator/ListInvoiceUnits.html#Invoicing.Paginator.ListInvoiceUnits.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_invoicing/paginators/#listinvoiceunitspaginator)
        """

if TYPE_CHECKING:
    _ListProcurementPortalPreferencesPaginatorBase = Paginator[
        ListProcurementPortalPreferencesResponseTypeDef
    ]
else:
    _ListProcurementPortalPreferencesPaginatorBase = Paginator  # type: ignore[assignment]

class ListProcurementPortalPreferencesPaginator(_ListProcurementPortalPreferencesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/invoicing/paginator/ListProcurementPortalPreferences.html#Invoicing.Paginator.ListProcurementPortalPreferences)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_invoicing/paginators/#listprocurementportalpreferencespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProcurementPortalPreferencesRequestPaginateTypeDef]
    ) -> PageIterator[ListProcurementPortalPreferencesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/invoicing/paginator/ListProcurementPortalPreferences.html#Invoicing.Paginator.ListProcurementPortalPreferences.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_invoicing/paginators/#listprocurementportalpreferencespaginator)
        """

if TYPE_CHECKING:
    _ListProcurementPortalSuppliersPaginatorBase = Paginator[
        ListProcurementPortalSuppliersResponseTypeDef
    ]
else:
    _ListProcurementPortalSuppliersPaginatorBase = Paginator  # type: ignore[assignment]

class ListProcurementPortalSuppliersPaginator(_ListProcurementPortalSuppliersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/invoicing/paginator/ListProcurementPortalSuppliers.html#Invoicing.Paginator.ListProcurementPortalSuppliers)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_invoicing/paginators/#listprocurementportalsupplierspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProcurementPortalSuppliersRequestPaginateTypeDef]
    ) -> PageIterator[ListProcurementPortalSuppliersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/invoicing/paginator/ListProcurementPortalSuppliers.html#Invoicing.Paginator.ListProcurementPortalSuppliers.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_invoicing/paginators/#listprocurementportalsupplierspaginator)
        """

if TYPE_CHECKING:
    _ListProcurementPortalsPaginatorBase = Paginator[ListProcurementPortalsResponseTypeDef]
else:
    _ListProcurementPortalsPaginatorBase = Paginator  # type: ignore[assignment]

class ListProcurementPortalsPaginator(_ListProcurementPortalsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/invoicing/paginator/ListProcurementPortals.html#Invoicing.Paginator.ListProcurementPortals)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_invoicing/paginators/#listprocurementportalspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProcurementPortalsRequestPaginateTypeDef]
    ) -> PageIterator[ListProcurementPortalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/invoicing/paginator/ListProcurementPortals.html#Invoicing.Paginator.ListProcurementPortals.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_invoicing/paginators/#listprocurementportalspaginator)
        """
