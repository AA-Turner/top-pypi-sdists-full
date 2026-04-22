"""
Type annotations for interconnect service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_interconnect/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_interconnect.client import InterconnectClient
    from types_aiobotocore_interconnect.paginator import (
        ListAttachPointsPaginator,
        ListConnectionsPaginator,
        ListEnvironmentsPaginator,
    )

    session = get_session()
    with session.create_client("interconnect") as client:
        client: InterconnectClient

        list_attach_points_paginator: ListAttachPointsPaginator = client.get_paginator("list_attach_points")
        list_connections_paginator: ListConnectionsPaginator = client.get_paginator("list_connections")
        list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAttachPointsRequestPaginateTypeDef,
    ListAttachPointsResponseTypeDef,
    ListConnectionsRequestPaginateTypeDef,
    ListConnectionsResponseTypeDef,
    ListEnvironmentsRequestPaginateTypeDef,
    ListEnvironmentsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListAttachPointsPaginator", "ListConnectionsPaginator", "ListEnvironmentsPaginator")


if TYPE_CHECKING:
    _ListAttachPointsPaginatorBase = AioPaginator[ListAttachPointsResponseTypeDef]
else:
    _ListAttachPointsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAttachPointsPaginator(_ListAttachPointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/interconnect/paginator/ListAttachPoints.html#Interconnect.Paginator.ListAttachPoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_interconnect/paginators/#listattachpointspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAttachPointsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAttachPointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/interconnect/paginator/ListAttachPoints.html#Interconnect.Paginator.ListAttachPoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_interconnect/paginators/#listattachpointspaginator)
        """


if TYPE_CHECKING:
    _ListConnectionsPaginatorBase = AioPaginator[ListConnectionsResponseTypeDef]
else:
    _ListConnectionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListConnectionsPaginator(_ListConnectionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/interconnect/paginator/ListConnections.html#Interconnect.Paginator.ListConnections)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_interconnect/paginators/#listconnectionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConnectionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListConnectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/interconnect/paginator/ListConnections.html#Interconnect.Paginator.ListConnections.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_interconnect/paginators/#listconnectionspaginator)
        """


if TYPE_CHECKING:
    _ListEnvironmentsPaginatorBase = AioPaginator[ListEnvironmentsResponseTypeDef]
else:
    _ListEnvironmentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEnvironmentsPaginator(_ListEnvironmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/interconnect/paginator/ListEnvironments.html#Interconnect.Paginator.ListEnvironments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_interconnect/paginators/#listenvironmentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEnvironmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/interconnect/paginator/ListEnvironments.html#Interconnect.Paginator.ListEnvironments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_interconnect/paginators/#listenvironmentspaginator)
        """
