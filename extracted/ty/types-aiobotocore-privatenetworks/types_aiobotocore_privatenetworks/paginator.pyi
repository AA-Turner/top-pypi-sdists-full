"""
Type annotations for privatenetworks service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_privatenetworks.client import Private5GClient
    from types_aiobotocore_privatenetworks.paginator import (
        ListDeviceIdentifiersPaginator,
        ListNetworkResourcesPaginator,
        ListNetworkSitesPaginator,
        ListNetworksPaginator,
        ListOrdersPaginator,
    )

    session = get_session()
    with session.create_client("privatenetworks") as client:
        client: Private5GClient

        list_device_identifiers_paginator: ListDeviceIdentifiersPaginator = client.get_paginator("list_device_identifiers")
        list_network_resources_paginator: ListNetworkResourcesPaginator = client.get_paginator("list_network_resources")
        list_network_sites_paginator: ListNetworkSitesPaginator = client.get_paginator("list_network_sites")
        list_networks_paginator: ListNetworksPaginator = client.get_paginator("list_networks")
        list_orders_paginator: ListOrdersPaginator = client.get_paginator("list_orders")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListDeviceIdentifiersRequestPaginateTypeDef,
    ListDeviceIdentifiersResponseTypeDef,
    ListNetworkResourcesRequestPaginateTypeDef,
    ListNetworkResourcesResponseTypeDef,
    ListNetworkSitesRequestPaginateTypeDef,
    ListNetworkSitesResponseTypeDef,
    ListNetworksRequestPaginateTypeDef,
    ListNetworksResponseTypeDef,
    ListOrdersRequestPaginateTypeDef,
    ListOrdersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListDeviceIdentifiersPaginator",
    "ListNetworkResourcesPaginator",
    "ListNetworkSitesPaginator",
    "ListNetworksPaginator",
    "ListOrdersPaginator",
)

if TYPE_CHECKING:
    _ListDeviceIdentifiersPaginatorBase = AioPaginator[ListDeviceIdentifiersResponseTypeDef]
else:
    _ListDeviceIdentifiersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDeviceIdentifiersPaginator(_ListDeviceIdentifiersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListDeviceIdentifiers.html#Private5G.Paginator.ListDeviceIdentifiers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/paginators/#listdeviceidentifierspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeviceIdentifiersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDeviceIdentifiersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListDeviceIdentifiers.html#Private5G.Paginator.ListDeviceIdentifiers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/paginators/#listdeviceidentifierspaginator)
        """

if TYPE_CHECKING:
    _ListNetworkResourcesPaginatorBase = AioPaginator[ListNetworkResourcesResponseTypeDef]
else:
    _ListNetworkResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListNetworkResourcesPaginator(_ListNetworkResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListNetworkResources.html#Private5G.Paginator.ListNetworkResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/paginators/#listnetworkresourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkResourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNetworkResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListNetworkResources.html#Private5G.Paginator.ListNetworkResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/paginators/#listnetworkresourcespaginator)
        """

if TYPE_CHECKING:
    _ListNetworkSitesPaginatorBase = AioPaginator[ListNetworkSitesResponseTypeDef]
else:
    _ListNetworkSitesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListNetworkSitesPaginator(_ListNetworkSitesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListNetworkSites.html#Private5G.Paginator.ListNetworkSites)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/paginators/#listnetworksitespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkSitesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNetworkSitesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListNetworkSites.html#Private5G.Paginator.ListNetworkSites.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/paginators/#listnetworksitespaginator)
        """

if TYPE_CHECKING:
    _ListNetworksPaginatorBase = AioPaginator[ListNetworksResponseTypeDef]
else:
    _ListNetworksPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListNetworksPaginator(_ListNetworksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListNetworks.html#Private5G.Paginator.ListNetworks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/paginators/#listnetworkspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNetworksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListNetworks.html#Private5G.Paginator.ListNetworks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/paginators/#listnetworkspaginator)
        """

if TYPE_CHECKING:
    _ListOrdersPaginatorBase = AioPaginator[ListOrdersResponseTypeDef]
else:
    _ListOrdersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListOrdersPaginator(_ListOrdersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListOrders.html#Private5G.Paginator.ListOrders)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/paginators/#listorderspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOrdersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOrdersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks/paginator/ListOrders.html#Private5G.Paginator.ListOrders.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/paginators/#listorderspaginator)
        """
