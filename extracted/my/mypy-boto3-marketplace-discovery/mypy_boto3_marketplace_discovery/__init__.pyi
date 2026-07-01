"""
Main interface for marketplace-discovery service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_discovery/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_marketplace_discovery import (
        Client,
        GetOfferTermsPaginator,
        ListFulfillmentOptionsPaginator,
        ListPurchaseOptionsPaginator,
        MarketplaceDiscoveryClient,
        SearchFacetsPaginator,
        SearchListingsPaginator,
    )

    session = Session()
    client: MarketplaceDiscoveryClient = session.client("marketplace-discovery")

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
