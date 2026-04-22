"""
Main interface for marketplace-discovery service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_marketplace_discovery import (
        Client,
        GetOfferTermsPaginator,
        ListFulfillmentOptionsPaginator,
        ListPurchaseOptionsPaginator,
        MarketplaceDiscoveryClient,
        SearchFacetsPaginator,
        SearchListingsPaginator,
    )

    session = get_session()
    async with session.create_client("marketplace-discovery") as client:
        client: MarketplaceDiscoveryClient
        ...


    get_offer_terms_paginator: GetOfferTermsPaginator = client.get_paginator("get_offer_terms")
    list_fulfillment_options_paginator: ListFulfillmentOptionsPaginator = client.get_paginator("list_fulfillment_options")
    list_purchase_options_paginator: ListPurchaseOptionsPaginator = client.get_paginator("list_purchase_options")
    search_facets_paginator: SearchFacetsPaginator = client.get_paginator("search_facets")
    search_listings_paginator: SearchListingsPaginator = client.get_paginator("search_listings")
    ```
"""

from .client import MarketplaceDiscoveryClient
from .paginator import (
    GetOfferTermsPaginator,
    ListFulfillmentOptionsPaginator,
    ListPurchaseOptionsPaginator,
    SearchFacetsPaginator,
    SearchListingsPaginator,
)

Client = MarketplaceDiscoveryClient


__all__ = (
    "Client",
    "GetOfferTermsPaginator",
    "ListFulfillmentOptionsPaginator",
    "ListPurchaseOptionsPaginator",
    "MarketplaceDiscoveryClient",
    "SearchFacetsPaginator",
    "SearchListingsPaginator",
)
