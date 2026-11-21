"""
Main interface for apiportal service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_apiportal/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_apiportal import (
        APIPortalClient,
        Client,
        ListApiInventoryItemsPaginator,
        ListDiscoveryStatusesPaginator,
        ListManagedApiEventsPaginator,
        ListManagedApisPaginator,
        ListPortalsPaginator,
        ListProductApiPagesPaginator,
        ListProductPagesPaginator,
        ListProductsPaginator,
    )

    session = Session()
    client: APIPortalClient = session.client("apiportal")

    list_api_inventory_items_paginator: ListApiInventoryItemsPaginator = client.get_paginator("list_api_inventory_items")
    list_discovery_statuses_paginator: ListDiscoveryStatusesPaginator = client.get_paginator("list_discovery_statuses")
    list_managed_api_events_paginator: ListManagedApiEventsPaginator = client.get_paginator("list_managed_api_events")
    list_managed_apis_paginator: ListManagedApisPaginator = client.get_paginator("list_managed_apis")
    list_portals_paginator: ListPortalsPaginator = client.get_paginator("list_portals")
    list_product_api_pages_paginator: ListProductApiPagesPaginator = client.get_paginator("list_product_api_pages")
    list_product_pages_paginator: ListProductPagesPaginator = client.get_paginator("list_product_pages")
    list_products_paginator: ListProductsPaginator = client.get_paginator("list_products")
    ```
"""

from .client import APIPortalClient
from .paginator import (
    ListApiInventoryItemsPaginator,
    ListDiscoveryStatusesPaginator,
    ListManagedApiEventsPaginator,
    ListManagedApisPaginator,
    ListPortalsPaginator,
    ListProductApiPagesPaginator,
    ListProductPagesPaginator,
    ListProductsPaginator,
)

Client = APIPortalClient


__all__ = (
    "APIPortalClient",
    "Client",
    "ListApiInventoryItemsPaginator",
    "ListDiscoveryStatusesPaginator",
    "ListManagedApiEventsPaginator",
    "ListManagedApisPaginator",
    "ListPortalsPaginator",
    "ListProductApiPagesPaginator",
    "ListProductPagesPaginator",
    "ListProductsPaginator",
)
