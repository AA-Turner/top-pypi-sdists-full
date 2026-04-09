"""
Type annotations for marketplace-discovery service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_discovery/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_marketplace_discovery.client import MarketplaceDiscoveryClient
    from types_boto3_marketplace_discovery.paginator import (
        GetOfferTermsPaginator,
        ListFulfillmentOptionsPaginator,
        ListPurchaseOptionsPaginator,
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

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

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
    _GetOfferTermsPaginatorBase = Paginator[GetOfferTermsOutputTypeDef]
else:
    _GetOfferTermsPaginatorBase = Paginator  # type: ignore[assignment]


class GetOfferTermsPaginator(_GetOfferTermsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/paginator/GetOfferTerms.html#MarketplaceDiscovery.Paginator.GetOfferTerms)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_discovery/paginators/#getoffertermspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetOfferTermsInputPaginateTypeDef]
    ) -> PageIterator[GetOfferTermsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/paginator/GetOfferTerms.html#MarketplaceDiscovery.Paginator.GetOfferTerms.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_discovery/paginators/#getoffertermspaginator)
        """


if TYPE_CHECKING:
    _ListFulfillmentOptionsPaginatorBase = Paginator[ListFulfillmentOptionsOutputTypeDef]
else:
    _ListFulfillmentOptionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListFulfillmentOptionsPaginator(_ListFulfillmentOptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/paginator/ListFulfillmentOptions.html#MarketplaceDiscovery.Paginator.ListFulfillmentOptions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_discovery/paginators/#listfulfillmentoptionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFulfillmentOptionsInputPaginateTypeDef]
    ) -> PageIterator[ListFulfillmentOptionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/paginator/ListFulfillmentOptions.html#MarketplaceDiscovery.Paginator.ListFulfillmentOptions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_discovery/paginators/#listfulfillmentoptionspaginator)
        """


if TYPE_CHECKING:
    _ListPurchaseOptionsPaginatorBase = Paginator[ListPurchaseOptionsOutputTypeDef]
else:
    _ListPurchaseOptionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListPurchaseOptionsPaginator(_ListPurchaseOptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/paginator/ListPurchaseOptions.html#MarketplaceDiscovery.Paginator.ListPurchaseOptions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_discovery/paginators/#listpurchaseoptionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPurchaseOptionsInputPaginateTypeDef]
    ) -> PageIterator[ListPurchaseOptionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/paginator/ListPurchaseOptions.html#MarketplaceDiscovery.Paginator.ListPurchaseOptions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_discovery/paginators/#listpurchaseoptionspaginator)
        """


if TYPE_CHECKING:
    _SearchFacetsPaginatorBase = Paginator[SearchFacetsOutputTypeDef]
else:
    _SearchFacetsPaginatorBase = Paginator  # type: ignore[assignment]


class SearchFacetsPaginator(_SearchFacetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/paginator/SearchFacets.html#MarketplaceDiscovery.Paginator.SearchFacets)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_discovery/paginators/#searchfacetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchFacetsInputPaginateTypeDef]
    ) -> PageIterator[SearchFacetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/paginator/SearchFacets.html#MarketplaceDiscovery.Paginator.SearchFacets.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_discovery/paginators/#searchfacetspaginator)
        """


if TYPE_CHECKING:
    _SearchListingsPaginatorBase = Paginator[SearchListingsOutputTypeDef]
else:
    _SearchListingsPaginatorBase = Paginator  # type: ignore[assignment]


class SearchListingsPaginator(_SearchListingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/paginator/SearchListings.html#MarketplaceDiscovery.Paginator.SearchListings)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_discovery/paginators/#searchlistingspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchListingsInputPaginateTypeDef]
    ) -> PageIterator[SearchListingsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/paginator/SearchListings.html#MarketplaceDiscovery.Paginator.SearchListings.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_discovery/paginators/#searchlistingspaginator)
        """
