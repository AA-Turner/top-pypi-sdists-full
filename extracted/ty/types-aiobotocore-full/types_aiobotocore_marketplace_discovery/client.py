"""
Type annotations for marketplace-discovery service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_marketplace_discovery.client import MarketplaceDiscoveryClient

    session = get_session()
    async with session.create_client("marketplace-discovery") as client:
        client: MarketplaceDiscoveryClient
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
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
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("MarketplaceDiscoveryClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class MarketplaceDiscoveryClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery.html#MarketplaceDiscovery.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MarketplaceDiscoveryClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery.html#MarketplaceDiscovery.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/client/#generate_presigned_url)
        """

    async def get_listing(
        self, **kwargs: Unpack[GetListingInputTypeDef]
    ) -> GetListingOutputTypeDef:
        """
        Provides details about a listing, such as descriptions, badges, categories,
        pricing model summaries, reviews, and associated products and offers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/get_listing.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/client/#get_listing)
        """

    async def get_offer(self, **kwargs: Unpack[GetOfferInputTypeDef]) -> GetOfferOutputTypeDef:
        """
        Provides details about an offer, such as the pricing model, seller of record,
        availability dates, badges, and associated products.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/get_offer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/client/#get_offer)
        """

    async def get_offer_set(
        self, **kwargs: Unpack[GetOfferSetInputTypeDef]
    ) -> GetOfferSetOutputTypeDef:
        """
        Provides details about an offer set, which is a bundle of offers across
        multiple products.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/get_offer_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/client/#get_offer_set)
        """

    async def get_offer_terms(
        self, **kwargs: Unpack[GetOfferTermsInputTypeDef]
    ) -> GetOfferTermsOutputTypeDef:
        """
        Returns the terms attached to an offer, such as pricing terms (usage-based,
        contract, BYOL, free trial), legal terms, payment schedules, validity terms,
        support terms, and renewal terms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/get_offer_terms.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/client/#get_offer_terms)
        """

    async def get_product(
        self, **kwargs: Unpack[GetProductInputTypeDef]
    ) -> GetProductOutputTypeDef:
        """
        Provides details about a product, such as descriptions, highlights, categories,
        fulfillment option summaries, promotional media, and seller engagement options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/get_product.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/client/#get_product)
        """

    async def list_fulfillment_options(
        self, **kwargs: Unpack[ListFulfillmentOptionsInputTypeDef]
    ) -> ListFulfillmentOptionsOutputTypeDef:
        """
        Returns the fulfillment options available for a product, including deployment
        details such as version information, operating systems, usage instructions, and
        release notes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/list_fulfillment_options.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/client/#list_fulfillment_options)
        """

    async def list_purchase_options(
        self, **kwargs: Unpack[ListPurchaseOptionsInputTypeDef]
    ) -> ListPurchaseOptionsOutputTypeDef:
        """
        Returns the purchase options (offers and offer sets) available to the buyer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/list_purchase_options.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/client/#list_purchase_options)
        """

    async def search_facets(
        self, **kwargs: Unpack[SearchFacetsInputTypeDef]
    ) -> SearchFacetsOutputTypeDef:
        """
        Returns available facet values for filtering listings, such as categories,
        pricing models, fulfillment option types, publishers, and customer ratings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/search_facets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/client/#search_facets)
        """

    async def search_listings(
        self, **kwargs: Unpack[SearchListingsInputTypeDef]
    ) -> SearchListingsOutputTypeDef:
        """
        Returns a list of product listings based on search criteria and filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/search_listings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/client/#search_listings)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_offer_terms"]
    ) -> GetOfferTermsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_fulfillment_options"]
    ) -> ListFulfillmentOptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_purchase_options"]
    ) -> ListPurchaseOptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_facets"]
    ) -> SearchFacetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_listings"]
    ) -> SearchListingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery.html#MarketplaceDiscovery.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-discovery.html#MarketplaceDiscovery.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_discovery/client/)
        """
