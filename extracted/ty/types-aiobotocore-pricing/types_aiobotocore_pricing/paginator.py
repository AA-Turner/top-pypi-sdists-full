"""
Type annotations for pricing service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_pricing.client import PricingClient
    from types_aiobotocore_pricing.paginator import (
        DescribeServicesPaginator,
        GetAttributeValuesPaginator,
        GetProductsPaginator,
        ListPriceListsPaginator,
    )

    session = get_session()
    with session.create_client("pricing") as client:
        client: PricingClient

        describe_services_paginator: DescribeServicesPaginator = client.get_paginator("describe_services")
        get_attribute_values_paginator: GetAttributeValuesPaginator = client.get_paginator("get_attribute_values")
        get_products_paginator: GetProductsPaginator = client.get_paginator("get_products")
        list_price_lists_paginator: ListPriceListsPaginator = client.get_paginator("list_price_lists")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeServicesRequestPaginateTypeDef,
    DescribeServicesResponseTypeDef,
    GetAttributeValuesRequestPaginateTypeDef,
    GetAttributeValuesResponseTypeDef,
    GetProductsRequestPaginateTypeDef,
    GetProductsResponseTypeDef,
    ListPriceListsRequestPaginateTypeDef,
    ListPriceListsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeServicesPaginator",
    "GetAttributeValuesPaginator",
    "GetProductsPaginator",
    "ListPriceListsPaginator",
)


if TYPE_CHECKING:
    _DescribeServicesPaginatorBase = AioPaginator[DescribeServicesResponseTypeDef]
else:
    _DescribeServicesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeServicesPaginator(_DescribeServicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing/paginator/DescribeServices.html#Pricing.Paginator.DescribeServices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing/paginators/#describeservicespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeServicesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeServicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing/paginator/DescribeServices.html#Pricing.Paginator.DescribeServices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing/paginators/#describeservicespaginator)
        """


if TYPE_CHECKING:
    _GetAttributeValuesPaginatorBase = AioPaginator[GetAttributeValuesResponseTypeDef]
else:
    _GetAttributeValuesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetAttributeValuesPaginator(_GetAttributeValuesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing/paginator/GetAttributeValues.html#Pricing.Paginator.GetAttributeValues)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing/paginators/#getattributevaluespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetAttributeValuesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetAttributeValuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing/paginator/GetAttributeValues.html#Pricing.Paginator.GetAttributeValues.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing/paginators/#getattributevaluespaginator)
        """


if TYPE_CHECKING:
    _GetProductsPaginatorBase = AioPaginator[GetProductsResponseTypeDef]
else:
    _GetProductsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetProductsPaginator(_GetProductsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing/paginator/GetProducts.html#Pricing.Paginator.GetProducts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing/paginators/#getproductspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetProductsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetProductsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing/paginator/GetProducts.html#Pricing.Paginator.GetProducts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing/paginators/#getproductspaginator)
        """


if TYPE_CHECKING:
    _ListPriceListsPaginatorBase = AioPaginator[ListPriceListsResponseTypeDef]
else:
    _ListPriceListsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPriceListsPaginator(_ListPriceListsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing/paginator/ListPriceLists.html#Pricing.Paginator.ListPriceLists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing/paginators/#listpricelistspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPriceListsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPriceListsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing/paginator/ListPriceLists.html#Pricing.Paginator.ListPriceLists.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing/paginators/#listpricelistspaginator)
        """
