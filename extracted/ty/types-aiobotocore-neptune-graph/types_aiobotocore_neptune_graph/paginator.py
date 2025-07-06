"""
Type annotations for neptune-graph service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune_graph/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_neptune_graph.client import NeptuneGraphClient
    from types_aiobotocore_neptune_graph.paginator import (
        ListExportTasksPaginator,
        ListGraphSnapshotsPaginator,
        ListGraphsPaginator,
        ListImportTasksPaginator,
        ListPrivateGraphEndpointsPaginator,
    )

    session = get_session()
    with session.create_client("neptune-graph") as client:
        client: NeptuneGraphClient

        list_export_tasks_paginator: ListExportTasksPaginator = client.get_paginator("list_export_tasks")
        list_graph_snapshots_paginator: ListGraphSnapshotsPaginator = client.get_paginator("list_graph_snapshots")
        list_graphs_paginator: ListGraphsPaginator = client.get_paginator("list_graphs")
        list_import_tasks_paginator: ListImportTasksPaginator = client.get_paginator("list_import_tasks")
        list_private_graph_endpoints_paginator: ListPrivateGraphEndpointsPaginator = client.get_paginator("list_private_graph_endpoints")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListExportTasksInputPaginateTypeDef,
    ListExportTasksOutputTypeDef,
    ListGraphsInputPaginateTypeDef,
    ListGraphSnapshotsInputPaginateTypeDef,
    ListGraphSnapshotsOutputTypeDef,
    ListGraphsOutputTypeDef,
    ListImportTasksInputPaginateTypeDef,
    ListImportTasksOutputTypeDef,
    ListPrivateGraphEndpointsInputPaginateTypeDef,
    ListPrivateGraphEndpointsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListExportTasksPaginator",
    "ListGraphSnapshotsPaginator",
    "ListGraphsPaginator",
    "ListImportTasksPaginator",
    "ListPrivateGraphEndpointsPaginator",
)


if TYPE_CHECKING:
    _ListExportTasksPaginatorBase = AioPaginator[ListExportTasksOutputTypeDef]
else:
    _ListExportTasksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListExportTasksPaginator(_ListExportTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListExportTasks.html#NeptuneGraph.Paginator.ListExportTasks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune_graph/paginators/#listexporttaskspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExportTasksInputPaginateTypeDef]
    ) -> AioPageIterator[ListExportTasksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListExportTasks.html#NeptuneGraph.Paginator.ListExportTasks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune_graph/paginators/#listexporttaskspaginator)
        """


if TYPE_CHECKING:
    _ListGraphSnapshotsPaginatorBase = AioPaginator[ListGraphSnapshotsOutputTypeDef]
else:
    _ListGraphSnapshotsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListGraphSnapshotsPaginator(_ListGraphSnapshotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListGraphSnapshots.html#NeptuneGraph.Paginator.ListGraphSnapshots)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune_graph/paginators/#listgraphsnapshotspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGraphSnapshotsInputPaginateTypeDef]
    ) -> AioPageIterator[ListGraphSnapshotsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListGraphSnapshots.html#NeptuneGraph.Paginator.ListGraphSnapshots.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune_graph/paginators/#listgraphsnapshotspaginator)
        """


if TYPE_CHECKING:
    _ListGraphsPaginatorBase = AioPaginator[ListGraphsOutputTypeDef]
else:
    _ListGraphsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListGraphsPaginator(_ListGraphsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListGraphs.html#NeptuneGraph.Paginator.ListGraphs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune_graph/paginators/#listgraphspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGraphsInputPaginateTypeDef]
    ) -> AioPageIterator[ListGraphsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListGraphs.html#NeptuneGraph.Paginator.ListGraphs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune_graph/paginators/#listgraphspaginator)
        """


if TYPE_CHECKING:
    _ListImportTasksPaginatorBase = AioPaginator[ListImportTasksOutputTypeDef]
else:
    _ListImportTasksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListImportTasksPaginator(_ListImportTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListImportTasks.html#NeptuneGraph.Paginator.ListImportTasks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune_graph/paginators/#listimporttaskspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImportTasksInputPaginateTypeDef]
    ) -> AioPageIterator[ListImportTasksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListImportTasks.html#NeptuneGraph.Paginator.ListImportTasks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune_graph/paginators/#listimporttaskspaginator)
        """


if TYPE_CHECKING:
    _ListPrivateGraphEndpointsPaginatorBase = AioPaginator[ListPrivateGraphEndpointsOutputTypeDef]
else:
    _ListPrivateGraphEndpointsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPrivateGraphEndpointsPaginator(_ListPrivateGraphEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListPrivateGraphEndpoints.html#NeptuneGraph.Paginator.ListPrivateGraphEndpoints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune_graph/paginators/#listprivategraphendpointspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPrivateGraphEndpointsInputPaginateTypeDef]
    ) -> AioPageIterator[ListPrivateGraphEndpointsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune-graph/paginator/ListPrivateGraphEndpoints.html#NeptuneGraph.Paginator.ListPrivateGraphEndpoints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune_graph/paginators/#listprivategraphendpointspaginator)
        """
