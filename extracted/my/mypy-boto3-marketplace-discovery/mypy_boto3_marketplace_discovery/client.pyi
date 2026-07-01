"""
Type annotations for marketplace-discovery service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_discovery/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_marketplace_discovery.client import MarketplaceDiscoveryClient

    session = Session()
    client: MarketplaceDiscoveryClient = session.client("marketplace-discovery")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    GetOfferTermsPaginator,
    ListFulfillmentOptionsPaginator,
    ListPurchaseOptionsPaginator,
    SearchFacetsPaginator,
    SearchListingsPaginator,
)
from .type_defs import (
    GetListingInputTypeDef,
    GetListingOutputTypeDef,
    GetOfferInputTypeDef,
    GetOfferOutputTypeDef,
    GetOfferSetInputTypeDef,
    GetOfferSetOutputTypeDef,
    GetOfferTermsInputTypeDef,
    GetOfferTermsOutputTypeDef,
    GetProductInputTypeDef,
    GetProductOutputTypeDef,
    ListFulfillmentOptionsInputTypeDef,
    ListFulfillmentOptionsOutputTypeDef,
    ListPurchaseOptionsInputTypeDef,
    ListPurchaseOptionsOutputTypeDef,
    SearchFacetsInputTypeDef,
    SearchFacetsOutputTypeDef,
    SearchListingsInputTypeDef,
    SearchListingsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("MarketplaceDiscoveryClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class MarketplaceDiscoveryClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery.html#MarketplaceDiscovery.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_discovery/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MarketplaceDiscoveryClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery.html#MarketplaceDiscovery.Client)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_discovery/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/can_paginate.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_discovery/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/generate_presigned_url.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_discovery/client/#generate_presigned_url)
        """

    def get_listing(self, **kwargs: Unpack[GetListingInputTypeDef]) -> GetListingOutputTypeDef:
        """
        Provides details about a listing, such as descriptions, badges, categories,
        pricing model summaries, reviews, and associated products and offers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/get_listing.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_discovery/client/#get_listing)
        """

    def get_offer(self, **kwargs: Unpack[GetOfferInputTypeDef]) -> GetOfferOutputTypeDef:
        """
        Provides details about an offer, such as the pricing model, seller of record,
        availability dates, badges, and associated products.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/get_offer.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_discovery/client/#get_offer)
        """

    def get_offer_set(self, **kwargs: Unpack[GetOfferSetInputTypeDef]) -> GetOfferSetOutputTypeDef:
        """
        Provides details about an offer set, which is a bundle of offers across
        multiple products.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/get_offer_set.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_discovery/client/#get_offer_set)
        """

    def get_offer_terms(
        self, **kwargs: Unpack[GetOfferTermsInputTypeDef]
    ) -> GetOfferTermsOutputTypeDef:
        """
        Returns the terms attached to an offer, such as pricing terms (usage-based,
        contract, BYOL, free trial), legal terms, payment schedules, validity terms,
        support terms, and renewal terms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/get_offer_terms.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_discovery/client/#get_offer_terms)
        """

    def get_product(self, **kwargs: Unpack[GetProductInputTypeDef]) -> GetProductOutputTypeDef:
        """
        Provides details about a product, such as descriptions, highlights, categories,
        fulfillment option summaries, promotional media, and seller engagement options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/get_product.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_discovery/client/#get_product)
        """

    def list_fulfillment_options(
        self, **kwargs: Unpack[ListFulfillmentOptionsInputTypeDef]
    ) -> ListFulfillmentOptionsOutputTypeDef:
        """
        Returns the fulfillment options available for a product, including deployment
        details such as version information, operating systems, usage instructions, and
        release notes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/list_fulfillment_options.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_discovery/client/#list_fulfillment_options)
        """

    def list_purchase_options(
        self, **kwargs: Unpack[ListPurchaseOptionsInputTypeDef]
    ) -> ListPurchaseOptionsOutputTypeDef:
        """
        Returns the purchase options (offers and offer sets) available to the buyer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/list_purchase_options.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_discovery/client/#list_purchase_options)
        """

    def search_facets(
        self, **kwargs: Unpack[SearchFacetsInputTypeDef]
    ) -> SearchFacetsOutputTypeDef:
        """
        Returns available facet values for filtering listings, such as categories,
        pricing models, fulfillment option types, publishers, and customer ratings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/search_facets.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_discovery/client/#search_facets)
        """

    def search_listings(
        self, **kwargs: Unpack[SearchListingsInputTypeDef]
    ) -> SearchListingsOutputTypeDef:
        """
        Returns a list of product listings based on search criteria and filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/search_listings.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_discovery/client/#search_listings)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_offer_terms"]
    ) -> GetOfferTermsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_discovery/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_fulfillment_options"]
    ) -> ListFulfillmentOptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_discovery/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_purchase_options"]
    ) -> ListPurchaseOptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_discovery/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_facets"]
    ) -> SearchFacetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_discovery/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_listings"]
    ) -> SearchListingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_discovery/client/#get_paginator)
        """
