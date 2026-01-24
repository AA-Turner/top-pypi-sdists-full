"""
Type annotations for rtbfabric service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_rtbfabric.client import RTBFabricClient
    from types_aiobotocore_rtbfabric.paginator import (
        ListLinksPaginator,
        ListRequesterGatewaysPaginator,
        ListResponderGatewaysPaginator,
    )

    session = get_session()
    with session.create_client("rtbfabric") as client:
        client: RTBFabricClient

        list_links_paginator: ListLinksPaginator = client.get_paginator("list_links")
        list_requester_gateways_paginator: ListRequesterGatewaysPaginator = client.get_paginator("list_requester_gateways")
        list_responder_gateways_paginator: ListResponderGatewaysPaginator = client.get_paginator("list_responder_gateways")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListLinksRequestPaginateTypeDef,
    ListLinksResponseTypeDef,
    ListRequesterGatewaysRequestPaginateTypeDef,
    ListRequesterGatewaysResponseTypeDef,
    ListResponderGatewaysRequestPaginateTypeDef,
    ListResponderGatewaysResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListLinksPaginator", "ListRequesterGatewaysPaginator", "ListResponderGatewaysPaginator")

if TYPE_CHECKING:
    _ListLinksPaginatorBase = AioPaginator[ListLinksResponseTypeDef]
else:
    _ListLinksPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListLinksPaginator(_ListLinksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/paginator/ListLinks.html#RTBFabric.Paginator.ListLinks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/paginators/#listlinkspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLinksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLinksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/paginator/ListLinks.html#RTBFabric.Paginator.ListLinks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/paginators/#listlinkspaginator)
        """

if TYPE_CHECKING:
    _ListRequesterGatewaysPaginatorBase = AioPaginator[ListRequesterGatewaysResponseTypeDef]
else:
    _ListRequesterGatewaysPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRequesterGatewaysPaginator(_ListRequesterGatewaysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/paginator/ListRequesterGateways.html#RTBFabric.Paginator.ListRequesterGateways)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/paginators/#listrequestergatewayspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRequesterGatewaysRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRequesterGatewaysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/paginator/ListRequesterGateways.html#RTBFabric.Paginator.ListRequesterGateways.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/paginators/#listrequestergatewayspaginator)
        """

if TYPE_CHECKING:
    _ListResponderGatewaysPaginatorBase = AioPaginator[ListResponderGatewaysResponseTypeDef]
else:
    _ListResponderGatewaysPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListResponderGatewaysPaginator(_ListResponderGatewaysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/paginator/ListResponderGateways.html#RTBFabric.Paginator.ListResponderGateways)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/paginators/#listrespondergatewayspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResponderGatewaysRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResponderGatewaysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/paginator/ListResponderGateways.html#RTBFabric.Paginator.ListResponderGateways.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/paginators/#listrespondergatewayspaginator)
        """
