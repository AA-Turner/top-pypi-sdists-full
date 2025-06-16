"""
Type annotations for pcs service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_pcs.client import ParallelComputingServiceClient
    from types_aiobotocore_pcs.paginator import (
        ListClustersPaginator,
        ListComputeNodeGroupsPaginator,
        ListQueuesPaginator,
    )

    session = get_session()
    with session.create_client("pcs") as client:
        client: ParallelComputingServiceClient

        list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
        list_compute_node_groups_paginator: ListComputeNodeGroupsPaginator = client.get_paginator("list_compute_node_groups")
        list_queues_paginator: ListQueuesPaginator = client.get_paginator("list_queues")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListClustersRequestPaginateTypeDef,
    ListClustersResponseTypeDef,
    ListComputeNodeGroupsRequestPaginateTypeDef,
    ListComputeNodeGroupsResponseTypeDef,
    ListQueuesRequestPaginateTypeDef,
    ListQueuesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListClustersPaginator", "ListComputeNodeGroupsPaginator", "ListQueuesPaginator")

if TYPE_CHECKING:
    _ListClustersPaginatorBase = AioPaginator[ListClustersResponseTypeDef]
else:
    _ListClustersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListClustersPaginator(_ListClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/paginator/ListClusters.html#ParallelComputingService.Paginator.ListClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/paginators/#listclusterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListClustersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/paginator/ListClusters.html#ParallelComputingService.Paginator.ListClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/paginators/#listclusterspaginator)
        """

if TYPE_CHECKING:
    _ListComputeNodeGroupsPaginatorBase = AioPaginator[ListComputeNodeGroupsResponseTypeDef]
else:
    _ListComputeNodeGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListComputeNodeGroupsPaginator(_ListComputeNodeGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/paginator/ListComputeNodeGroups.html#ParallelComputingService.Paginator.ListComputeNodeGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/paginators/#listcomputenodegroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListComputeNodeGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListComputeNodeGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/paginator/ListComputeNodeGroups.html#ParallelComputingService.Paginator.ListComputeNodeGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/paginators/#listcomputenodegroupspaginator)
        """

if TYPE_CHECKING:
    _ListQueuesPaginatorBase = AioPaginator[ListQueuesResponseTypeDef]
else:
    _ListQueuesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListQueuesPaginator(_ListQueuesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/paginator/ListQueues.html#ParallelComputingService.Paginator.ListQueues)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/paginators/#listqueuespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListQueuesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/paginator/ListQueues.html#ParallelComputingService.Paginator.ListQueues.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/paginators/#listqueuespaginator)
        """
