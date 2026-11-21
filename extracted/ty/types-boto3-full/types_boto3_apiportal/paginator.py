"""
Type annotations for apiportal service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_apiportal/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_apiportal.client import APIPortalClient
    from types_boto3_apiportal.paginator import (
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

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListApiInventoryItemsRequestPaginateTypeDef,
    ListApiInventoryItemsResponseTypeDef,
    ListDiscoveryStatusesRequestPaginateTypeDef,
    ListDiscoveryStatusesResponseTypeDef,
    ListManagedApiEventsRequestPaginateTypeDef,
    ListManagedApiEventsResponseTypeDef,
    ListManagedApisRequestPaginateTypeDef,
    ListManagedApisResponseTypeDef,
    ListPortalsRequestPaginateTypeDef,
    ListPortalsResponseTypeDef,
    ListProductApiPagesRequestPaginateTypeDef,
    ListProductApiPagesResponseTypeDef,
    ListProductPagesRequestPaginateTypeDef,
    ListProductPagesResponseTypeDef,
    ListProductsRequestPaginateTypeDef,
    ListProductsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListApiInventoryItemsPaginator",
    "ListDiscoveryStatusesPaginator",
    "ListManagedApiEventsPaginator",
    "ListManagedApisPaginator",
    "ListPortalsPaginator",
    "ListProductApiPagesPaginator",
    "ListProductPagesPaginator",
    "ListProductsPaginator",
)


if TYPE_CHECKING:
    _ListApiInventoryItemsPaginatorBase = Paginator[ListApiInventoryItemsResponseTypeDef]
else:
    _ListApiInventoryItemsPaginatorBase = Paginator  # type: ignore[assignment]


class ListApiInventoryItemsPaginator(_ListApiInventoryItemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/paginator/ListApiInventoryItems.html#APIPortal.Paginator.ListApiInventoryItems)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_apiportal/paginators/#listapiinventoryitemspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApiInventoryItemsRequestPaginateTypeDef]
    ) -> PageIterator[ListApiInventoryItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/paginator/ListApiInventoryItems.html#APIPortal.Paginator.ListApiInventoryItems.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_apiportal/paginators/#listapiinventoryitemspaginator)
        """


if TYPE_CHECKING:
    _ListDiscoveryStatusesPaginatorBase = Paginator[ListDiscoveryStatusesResponseTypeDef]
else:
    _ListDiscoveryStatusesPaginatorBase = Paginator  # type: ignore[assignment]


class ListDiscoveryStatusesPaginator(_ListDiscoveryStatusesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/paginator/ListDiscoveryStatuses.html#APIPortal.Paginator.ListDiscoveryStatuses)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_apiportal/paginators/#listdiscoverystatusespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDiscoveryStatusesRequestPaginateTypeDef]
    ) -> PageIterator[ListDiscoveryStatusesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/paginator/ListDiscoveryStatuses.html#APIPortal.Paginator.ListDiscoveryStatuses.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_apiportal/paginators/#listdiscoverystatusespaginator)
        """


if TYPE_CHECKING:
    _ListManagedApiEventsPaginatorBase = Paginator[ListManagedApiEventsResponseTypeDef]
else:
    _ListManagedApiEventsPaginatorBase = Paginator  # type: ignore[assignment]


class ListManagedApiEventsPaginator(_ListManagedApiEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/paginator/ListManagedApiEvents.html#APIPortal.Paginator.ListManagedApiEvents)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_apiportal/paginators/#listmanagedapieventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListManagedApiEventsRequestPaginateTypeDef]
    ) -> PageIterator[ListManagedApiEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/paginator/ListManagedApiEvents.html#APIPortal.Paginator.ListManagedApiEvents.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_apiportal/paginators/#listmanagedapieventspaginator)
        """


if TYPE_CHECKING:
    _ListManagedApisPaginatorBase = Paginator[ListManagedApisResponseTypeDef]
else:
    _ListManagedApisPaginatorBase = Paginator  # type: ignore[assignment]


class ListManagedApisPaginator(_ListManagedApisPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/paginator/ListManagedApis.html#APIPortal.Paginator.ListManagedApis)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_apiportal/paginators/#listmanagedapispaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListManagedApisRequestPaginateTypeDef]
    ) -> PageIterator[ListManagedApisResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/paginator/ListManagedApis.html#APIPortal.Paginator.ListManagedApis.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_apiportal/paginators/#listmanagedapispaginator)
        """


if TYPE_CHECKING:
    _ListPortalsPaginatorBase = Paginator[ListPortalsResponseTypeDef]
else:
    _ListPortalsPaginatorBase = Paginator  # type: ignore[assignment]


class ListPortalsPaginator(_ListPortalsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/paginator/ListPortals.html#APIPortal.Paginator.ListPortals)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_apiportal/paginators/#listportalspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPortalsRequestPaginateTypeDef]
    ) -> PageIterator[ListPortalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/paginator/ListPortals.html#APIPortal.Paginator.ListPortals.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_apiportal/paginators/#listportalspaginator)
        """


if TYPE_CHECKING:
    _ListProductApiPagesPaginatorBase = Paginator[ListProductApiPagesResponseTypeDef]
else:
    _ListProductApiPagesPaginatorBase = Paginator  # type: ignore[assignment]


class ListProductApiPagesPaginator(_ListProductApiPagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/paginator/ListProductApiPages.html#APIPortal.Paginator.ListProductApiPages)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_apiportal/paginators/#listproductapipagespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProductApiPagesRequestPaginateTypeDef]
    ) -> PageIterator[ListProductApiPagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/paginator/ListProductApiPages.html#APIPortal.Paginator.ListProductApiPages.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_apiportal/paginators/#listproductapipagespaginator)
        """


if TYPE_CHECKING:
    _ListProductPagesPaginatorBase = Paginator[ListProductPagesResponseTypeDef]
else:
    _ListProductPagesPaginatorBase = Paginator  # type: ignore[assignment]


class ListProductPagesPaginator(_ListProductPagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/paginator/ListProductPages.html#APIPortal.Paginator.ListProductPages)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_apiportal/paginators/#listproductpagespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProductPagesRequestPaginateTypeDef]
    ) -> PageIterator[ListProductPagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/paginator/ListProductPages.html#APIPortal.Paginator.ListProductPages.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_apiportal/paginators/#listproductpagespaginator)
        """


if TYPE_CHECKING:
    _ListProductsPaginatorBase = Paginator[ListProductsResponseTypeDef]
else:
    _ListProductsPaginatorBase = Paginator  # type: ignore[assignment]


class ListProductsPaginator(_ListProductsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/paginator/ListProducts.html#APIPortal.Paginator.ListProducts)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_apiportal/paginators/#listproductspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProductsRequestPaginateTypeDef]
    ) -> PageIterator[ListProductsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apiportal/paginator/ListProducts.html#APIPortal.Paginator.ListProducts.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_apiportal/paginators/#listproductspaginator)
        """
