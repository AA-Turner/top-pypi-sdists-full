"""
Type annotations for interconnect service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_interconnect/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_interconnect.client import InterconnectClient
    from types_boto3_interconnect.paginator import (
        ListAttachPointsPaginator,
        ListConnectionsPaginator,
        ListEnvironmentsPaginator,
    )

    session = Session()
    client: InterconnectClient = session.client("interconnect")

    list_attach_points_paginator: ListAttachPointsPaginator = client.get_paginator("list_attach_points")
    list_connections_paginator: ListConnectionsPaginator = client.get_paginator("list_connections")
    list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

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
    _ListAttachPointsPaginatorBase = Paginator[ListAttachPointsResponseTypeDef]
else:
    _ListAttachPointsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAttachPointsPaginator(_ListAttachPointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/interconnect/paginator/ListAttachPoints.html#Interconnect.Paginator.ListAttachPoints)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_interconnect/paginators/#listattachpointspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAttachPointsRequestPaginateTypeDef]
    ) -> PageIterator[ListAttachPointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/interconnect/paginator/ListAttachPoints.html#Interconnect.Paginator.ListAttachPoints.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_interconnect/paginators/#listattachpointspaginator)
        """

if TYPE_CHECKING:
    _ListConnectionsPaginatorBase = Paginator[ListConnectionsResponseTypeDef]
else:
    _ListConnectionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListConnectionsPaginator(_ListConnectionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/interconnect/paginator/ListConnections.html#Interconnect.Paginator.ListConnections)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_interconnect/paginators/#listconnectionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConnectionsRequestPaginateTypeDef]
    ) -> PageIterator[ListConnectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/interconnect/paginator/ListConnections.html#Interconnect.Paginator.ListConnections.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_interconnect/paginators/#listconnectionspaginator)
        """

if TYPE_CHECKING:
    _ListEnvironmentsPaginatorBase = Paginator[ListEnvironmentsResponseTypeDef]
else:
    _ListEnvironmentsPaginatorBase = Paginator  # type: ignore[assignment]

class ListEnvironmentsPaginator(_ListEnvironmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/interconnect/paginator/ListEnvironments.html#Interconnect.Paginator.ListEnvironments)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_interconnect/paginators/#listenvironmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentsRequestPaginateTypeDef]
    ) -> PageIterator[ListEnvironmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/interconnect/paginator/ListEnvironments.html#Interconnect.Paginator.ListEnvironments.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_interconnect/paginators/#listenvironmentspaginator)
        """
