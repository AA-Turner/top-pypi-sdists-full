"""
Type annotations for invoicing service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_invoicing/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_invoicing.client import InvoicingClient
    from types_aiobotocore_invoicing.paginator import (
        ListInvoiceSummariesPaginator,
        ListInvoiceUnitsPaginator,
    )

    session = get_session()
    with session.create_client("invoicing") as client:
        client: InvoicingClient

        list_invoice_summaries_paginator: ListInvoiceSummariesPaginator = client.get_paginator("list_invoice_summaries")
        list_invoice_units_paginator: ListInvoiceUnitsPaginator = client.get_paginator("list_invoice_units")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListInvoiceSummariesRequestPaginateTypeDef,
    ListInvoiceSummariesResponseTypeDef,
    ListInvoiceUnitsRequestPaginateTypeDef,
    ListInvoiceUnitsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListInvoiceSummariesPaginator", "ListInvoiceUnitsPaginator")


if TYPE_CHECKING:
    _ListInvoiceSummariesPaginatorBase = AioPaginator[ListInvoiceSummariesResponseTypeDef]
else:
    _ListInvoiceSummariesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListInvoiceSummariesPaginator(_ListInvoiceSummariesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/invoicing/paginator/ListInvoiceSummaries.html#Invoicing.Paginator.ListInvoiceSummaries)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_invoicing/paginators/#listinvoicesummariespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInvoiceSummariesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInvoiceSummariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/invoicing/paginator/ListInvoiceSummaries.html#Invoicing.Paginator.ListInvoiceSummaries.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_invoicing/paginators/#listinvoicesummariespaginator)
        """


if TYPE_CHECKING:
    _ListInvoiceUnitsPaginatorBase = AioPaginator[ListInvoiceUnitsResponseTypeDef]
else:
    _ListInvoiceUnitsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListInvoiceUnitsPaginator(_ListInvoiceUnitsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/invoicing/paginator/ListInvoiceUnits.html#Invoicing.Paginator.ListInvoiceUnits)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_invoicing/paginators/#listinvoiceunitspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInvoiceUnitsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInvoiceUnitsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/invoicing/paginator/ListInvoiceUnits.html#Invoicing.Paginator.ListInvoiceUnits.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_invoicing/paginators/#listinvoiceunitspaginator)
        """
