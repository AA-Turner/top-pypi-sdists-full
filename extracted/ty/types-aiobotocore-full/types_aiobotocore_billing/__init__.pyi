"""
Main interface for billing service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billing/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_billing import (
        BillingClient,
        Client,
        ListBillingViewsPaginator,
        ListSourceViewsForBillingViewPaginator,
    )

    session = get_session()
    async with session.create_client("billing") as client:
        client: BillingClient
        ...


    list_billing_views_paginator: ListBillingViewsPaginator = client.get_paginator("list_billing_views")
    list_source_views_for_billing_view_paginator: ListSourceViewsForBillingViewPaginator = client.get_paginator("list_source_views_for_billing_view")
    ```
"""

from .client import BillingClient
from .paginator import ListBillingViewsPaginator, ListSourceViewsForBillingViewPaginator

Client = BillingClient

__all__ = (
    "BillingClient",
    "Client",
    "ListBillingViewsPaginator",
    "ListSourceViewsForBillingViewPaginator",
)
