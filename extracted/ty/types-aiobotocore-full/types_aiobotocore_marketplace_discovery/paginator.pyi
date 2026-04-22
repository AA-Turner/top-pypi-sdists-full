"""
Type annotations for marketplace-discovery service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_marketplace_discovery.client import MarketplaceDiscoveryClient
    from types_aiobotocore_marketplace_discovery.paginator import (
        GetOfferTermsPaginator,
        ListFulfillmentOptionsPaginator,
        ListPurchaseOptionsPaginator,
        SearchFacetsPaginator,
        SearchListingsPaginator,
    )

    session = get_session()
    with session.create_client("marketplace-discovery") as client:
        client: MarketplaceDiscoveryClient

        get_offer_terms_paginator: GetOfferTermsPaginator = client.get_paginator("get_offer_terms")
        list_fulfillment_options_paginator: ListFulfillmentOptionsPaginator = client.get_paginator("list_fulfillment_options")
        list_purchase_options_paginator: ListPurchaseOptionsPaginator = client.get_paginator("list_purchase_options")
        search_facets_paginator: SearchFacetsPaginator = client.get_paginator("search_facets")
        search_listings_paginator: SearchListingsPaginator = client.get_paginator("search_listings")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetOfferTermsInputPaginateTypeDef,
    GetOfferTermsOutputTypeDef,
    ListFulfillmentOptionsInputPaginateTypeDef,
    ListFulfillmentOptionsOutputTypeDef,
    ListPurchaseOptionsInputPaginateTypeDef,
    ListPurchaseOptionsOutputTypeDef,
    SearchFacetsInputPaginateTypeDef,
    SearchFacetsOutputTypeDef,
    SearchListingsInputPaginateTypeDef,
    SearchListingsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetOfferTermsPaginator",
    "ListFulfillmentOptionsPaginator",
    "ListPurchaseOptionsPaginator",
    "SearchFacetsPaginator",
    "SearchListingsPaginator",
)

if TYPE_CHECKING:
    _GetOfferTermsPaginatorBase = AioPaginator[GetOfferTermsOutputTypeDef]
else:
    _GetOfferTermsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetOfferTermsPaginator(_GetOfferTermsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/paginator/GetOfferTerms.html#MarketplaceDiscovery.Paginator.GetOfferTerms)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/paginators/#getoffertermspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetOfferTermsInputPaginateTypeDef]
    ) -> AioPageIterator[GetOfferTermsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/paginator/GetOfferTerms.html#MarketplaceDiscovery.Paginator.GetOfferTerms.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/paginators/#getoffertermspaginator)
        """

if TYPE_CHECKING:
    _ListFulfillmentOptionsPaginatorBase = AioPaginator[ListFulfillmentOptionsOutputTypeDef]
else:
    _ListFulfillmentOptionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFulfillmentOptionsPaginator(_ListFulfillmentOptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/paginator/ListFulfillmentOptions.html#MarketplaceDiscovery.Paginator.ListFulfillmentOptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/paginators/#listfulfillmentoptionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFulfillmentOptionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListFulfillmentOptionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/paginator/ListFulfillmentOptions.html#MarketplaceDiscovery.Paginator.ListFulfillmentOptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/paginators/#listfulfillmentoptionspaginator)
        """

if TYPE_CHECKING:
    _ListPurchaseOptionsPaginatorBase = AioPaginator[ListPurchaseOptionsOutputTypeDef]
else:
    _ListPurchaseOptionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPurchaseOptionsPaginator(_ListPurchaseOptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/paginator/ListPurchaseOptions.html#MarketplaceDiscovery.Paginator.ListPurchaseOptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/paginators/#listpurchaseoptionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPurchaseOptionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListPurchaseOptionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/paginator/ListPurchaseOptions.html#MarketplaceDiscovery.Paginator.ListPurchaseOptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/paginators/#listpurchaseoptionspaginator)
        """

if TYPE_CHECKING:
    _SearchFacetsPaginatorBase = AioPaginator[SearchFacetsOutputTypeDef]
else:
    _SearchFacetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchFacetsPaginator(_SearchFacetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/paginator/SearchFacets.html#MarketplaceDiscovery.Paginator.SearchFacets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/paginators/#searchfacetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchFacetsInputPaginateTypeDef]
    ) -> AioPageIterator[SearchFacetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/paginator/SearchFacets.html#MarketplaceDiscovery.Paginator.SearchFacets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/paginators/#searchfacetspaginator)
        """

if TYPE_CHECKING:
    _SearchListingsPaginatorBase = AioPaginator[SearchListingsOutputTypeDef]
else:
    _SearchListingsPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchListingsPaginator(_SearchListingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/paginator/SearchListings.html#MarketplaceDiscovery.Paginator.SearchListings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/paginators/#searchlistingspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchListingsInputPaginateTypeDef]
    ) -> AioPageIterator[SearchListingsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/paginator/SearchListings.html#MarketplaceDiscovery.Paginator.SearchListings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/paginators/#searchlistingspaginator)
        """
