"""
Type annotations for docdb-elastic service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_docdb_elastic.client import DocDBElasticClient
    from types_aiobotocore_docdb_elastic.paginator import (
        ListClusterSnapshotsPaginator,
        ListClustersPaginator,
        ListPendingMaintenanceActionsPaginator,
    )

    session = get_session()
    with session.create_client("docdb-elastic") as client:
        client: DocDBElasticClient

        list_cluster_snapshots_paginator: ListClusterSnapshotsPaginator = client.get_paginator("list_cluster_snapshots")
        list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
        list_pending_maintenance_actions_paginator: ListPendingMaintenanceActionsPaginator = client.get_paginator("list_pending_maintenance_actions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListClustersInputPaginateTypeDef,
    ListClusterSnapshotsInputPaginateTypeDef,
    ListClusterSnapshotsOutputTypeDef,
    ListClustersOutputTypeDef,
    ListPendingMaintenanceActionsInputPaginateTypeDef,
    ListPendingMaintenanceActionsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListClusterSnapshotsPaginator",
    "ListClustersPaginator",
    "ListPendingMaintenanceActionsPaginator",
)

if TYPE_CHECKING:
    _ListClusterSnapshotsPaginatorBase = AioPaginator[ListClusterSnapshotsOutputTypeDef]
else:
    _ListClusterSnapshotsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListClusterSnapshotsPaginator(_ListClusterSnapshotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/paginator/ListClusterSnapshots.html#DocDBElastic.Paginator.ListClusterSnapshots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/paginators/#listclustersnapshotspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListClusterSnapshotsInputPaginateTypeDef]
    ) -> AioPageIterator[ListClusterSnapshotsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/paginator/ListClusterSnapshots.html#DocDBElastic.Paginator.ListClusterSnapshots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/paginators/#listclustersnapshotspaginator)
        """

if TYPE_CHECKING:
    _ListClustersPaginatorBase = AioPaginator[ListClustersOutputTypeDef]
else:
    _ListClustersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListClustersPaginator(_ListClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/paginator/ListClusters.html#DocDBElastic.Paginator.ListClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/paginators/#listclusterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListClustersInputPaginateTypeDef]
    ) -> AioPageIterator[ListClustersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/paginator/ListClusters.html#DocDBElastic.Paginator.ListClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/paginators/#listclusterspaginator)
        """

if TYPE_CHECKING:
    _ListPendingMaintenanceActionsPaginatorBase = AioPaginator[
        ListPendingMaintenanceActionsOutputTypeDef
    ]
else:
    _ListPendingMaintenanceActionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPendingMaintenanceActionsPaginator(_ListPendingMaintenanceActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/paginator/ListPendingMaintenanceActions.html#DocDBElastic.Paginator.ListPendingMaintenanceActions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/paginators/#listpendingmaintenanceactionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPendingMaintenanceActionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListPendingMaintenanceActionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/paginator/ListPendingMaintenanceActions.html#DocDBElastic.Paginator.ListPendingMaintenanceActions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/paginators/#listpendingmaintenanceactionspaginator)
        """
