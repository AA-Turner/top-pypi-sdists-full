"""
Type annotations for route53domains service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_route53domains.client import Route53DomainsClient
    from types_aiobotocore_route53domains.paginator import (
        ListDomainsPaginator,
        ListOperationsPaginator,
        ListPricesPaginator,
        ViewBillingPaginator,
    )

    session = get_session()
    with session.create_client("route53domains") as client:
        client: Route53DomainsClient

        list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
        list_operations_paginator: ListOperationsPaginator = client.get_paginator("list_operations")
        list_prices_paginator: ListPricesPaginator = client.get_paginator("list_prices")
        view_billing_paginator: ViewBillingPaginator = client.get_paginator("view_billing")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListDomainsRequestPaginateTypeDef,
    ListDomainsResponseTypeDef,
    ListOperationsRequestPaginateTypeDef,
    ListOperationsResponseTypeDef,
    ListPricesRequestPaginateTypeDef,
    ListPricesResponseTypeDef,
    ViewBillingRequestPaginateTypeDef,
    ViewBillingResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListDomainsPaginator",
    "ListOperationsPaginator",
    "ListPricesPaginator",
    "ViewBillingPaginator",
)

if TYPE_CHECKING:
    _ListDomainsPaginatorBase = AioPaginator[ListDomainsResponseTypeDef]
else:
    _ListDomainsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDomainsPaginator(_ListDomainsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/paginator/ListDomains.html#Route53Domains.Paginator.ListDomains)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators/#listdomainspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDomainsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDomainsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/paginator/ListDomains.html#Route53Domains.Paginator.ListDomains.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators/#listdomainspaginator)
        """

if TYPE_CHECKING:
    _ListOperationsPaginatorBase = AioPaginator[ListOperationsResponseTypeDef]
else:
    _ListOperationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListOperationsPaginator(_ListOperationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/paginator/ListOperations.html#Route53Domains.Paginator.ListOperations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators/#listoperationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOperationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOperationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/paginator/ListOperations.html#Route53Domains.Paginator.ListOperations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators/#listoperationspaginator)
        """

if TYPE_CHECKING:
    _ListPricesPaginatorBase = AioPaginator[ListPricesResponseTypeDef]
else:
    _ListPricesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPricesPaginator(_ListPricesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/paginator/ListPrices.html#Route53Domains.Paginator.ListPrices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators/#listpricespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPricesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPricesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/paginator/ListPrices.html#Route53Domains.Paginator.ListPrices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators/#listpricespaginator)
        """

if TYPE_CHECKING:
    _ViewBillingPaginatorBase = AioPaginator[ViewBillingResponseTypeDef]
else:
    _ViewBillingPaginatorBase = AioPaginator  # type: ignore[assignment]

class ViewBillingPaginator(_ViewBillingPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/paginator/ViewBilling.html#Route53Domains.Paginator.ViewBilling)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators/#viewbillingpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ViewBillingRequestPaginateTypeDef]
    ) -> AioPageIterator[ViewBillingResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/paginator/ViewBilling.html#Route53Domains.Paginator.ViewBilling.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/paginators/#viewbillingpaginator)
        """
