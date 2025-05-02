"""
Type annotations for datasync service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_datasync.client import DataSyncClient
    from types_aiobotocore_datasync.paginator import (
        DescribeStorageSystemResourceMetricsPaginator,
        ListAgentsPaginator,
        ListDiscoveryJobsPaginator,
        ListLocationsPaginator,
        ListStorageSystemsPaginator,
        ListTagsForResourcePaginator,
        ListTaskExecutionsPaginator,
        ListTasksPaginator,
    )

    session = get_session()
    with session.create_client("datasync") as client:
        client: DataSyncClient

        describe_storage_system_resource_metrics_paginator: DescribeStorageSystemResourceMetricsPaginator = client.get_paginator("describe_storage_system_resource_metrics")
        list_agents_paginator: ListAgentsPaginator = client.get_paginator("list_agents")
        list_discovery_jobs_paginator: ListDiscoveryJobsPaginator = client.get_paginator("list_discovery_jobs")
        list_locations_paginator: ListLocationsPaginator = client.get_paginator("list_locations")
        list_storage_systems_paginator: ListStorageSystemsPaginator = client.get_paginator("list_storage_systems")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
        list_task_executions_paginator: ListTaskExecutionsPaginator = client.get_paginator("list_task_executions")
        list_tasks_paginator: ListTasksPaginator = client.get_paginator("list_tasks")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeStorageSystemResourceMetricsRequestPaginateTypeDef,
    DescribeStorageSystemResourceMetricsResponseTypeDef,
    ListAgentsRequestPaginateTypeDef,
    ListAgentsResponseTypeDef,
    ListDiscoveryJobsRequestPaginateTypeDef,
    ListDiscoveryJobsResponseTypeDef,
    ListLocationsRequestPaginateTypeDef,
    ListLocationsResponseTypeDef,
    ListStorageSystemsRequestPaginateTypeDef,
    ListStorageSystemsResponseTypeDef,
    ListTagsForResourceRequestPaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTaskExecutionsRequestPaginateTypeDef,
    ListTaskExecutionsResponseTypeDef,
    ListTasksRequestPaginateTypeDef,
    ListTasksResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeStorageSystemResourceMetricsPaginator",
    "ListAgentsPaginator",
    "ListDiscoveryJobsPaginator",
    "ListLocationsPaginator",
    "ListStorageSystemsPaginator",
    "ListTagsForResourcePaginator",
    "ListTaskExecutionsPaginator",
    "ListTasksPaginator",
)


if TYPE_CHECKING:
    _DescribeStorageSystemResourceMetricsPaginatorBase = AioPaginator[
        DescribeStorageSystemResourceMetricsResponseTypeDef
    ]
else:
    _DescribeStorageSystemResourceMetricsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeStorageSystemResourceMetricsPaginator(
    _DescribeStorageSystemResourceMetricsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/DescribeStorageSystemResourceMetrics.html#DataSync.Paginator.DescribeStorageSystemResourceMetrics)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/paginators/#describestoragesystemresourcemetricspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeStorageSystemResourceMetricsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeStorageSystemResourceMetricsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/DescribeStorageSystemResourceMetrics.html#DataSync.Paginator.DescribeStorageSystemResourceMetrics.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/paginators/#describestoragesystemresourcemetricspaginator)
        """


if TYPE_CHECKING:
    _ListAgentsPaginatorBase = AioPaginator[ListAgentsResponseTypeDef]
else:
    _ListAgentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAgentsPaginator(_ListAgentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListAgents.html#DataSync.Paginator.ListAgents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/paginators/#listagentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAgentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListAgents.html#DataSync.Paginator.ListAgents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/paginators/#listagentspaginator)
        """


if TYPE_CHECKING:
    _ListDiscoveryJobsPaginatorBase = AioPaginator[ListDiscoveryJobsResponseTypeDef]
else:
    _ListDiscoveryJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDiscoveryJobsPaginator(_ListDiscoveryJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListDiscoveryJobs.html#DataSync.Paginator.ListDiscoveryJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/paginators/#listdiscoveryjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDiscoveryJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDiscoveryJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListDiscoveryJobs.html#DataSync.Paginator.ListDiscoveryJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/paginators/#listdiscoveryjobspaginator)
        """


if TYPE_CHECKING:
    _ListLocationsPaginatorBase = AioPaginator[ListLocationsResponseTypeDef]
else:
    _ListLocationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListLocationsPaginator(_ListLocationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListLocations.html#DataSync.Paginator.ListLocations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/paginators/#listlocationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLocationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLocationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListLocations.html#DataSync.Paginator.ListLocations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/paginators/#listlocationspaginator)
        """


if TYPE_CHECKING:
    _ListStorageSystemsPaginatorBase = AioPaginator[ListStorageSystemsResponseTypeDef]
else:
    _ListStorageSystemsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListStorageSystemsPaginator(_ListStorageSystemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListStorageSystems.html#DataSync.Paginator.ListStorageSystems)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/paginators/#liststoragesystemspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStorageSystemsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListStorageSystemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListStorageSystems.html#DataSync.Paginator.ListStorageSystems.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/paginators/#liststoragesystemspaginator)
        """


if TYPE_CHECKING:
    _ListTagsForResourcePaginatorBase = AioPaginator[ListTagsForResourceResponseTypeDef]
else:
    _ListTagsForResourcePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTagsForResourcePaginator(_ListTagsForResourcePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListTagsForResource.html#DataSync.Paginator.ListTagsForResource)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/paginators/#listtagsforresourcepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsForResourceRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListTagsForResource.html#DataSync.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/paginators/#listtagsforresourcepaginator)
        """


if TYPE_CHECKING:
    _ListTaskExecutionsPaginatorBase = AioPaginator[ListTaskExecutionsResponseTypeDef]
else:
    _ListTaskExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTaskExecutionsPaginator(_ListTaskExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListTaskExecutions.html#DataSync.Paginator.ListTaskExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/paginators/#listtaskexecutionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTaskExecutionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTaskExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListTaskExecutions.html#DataSync.Paginator.ListTaskExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/paginators/#listtaskexecutionspaginator)
        """


if TYPE_CHECKING:
    _ListTasksPaginatorBase = AioPaginator[ListTasksResponseTypeDef]
else:
    _ListTasksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTasksPaginator(_ListTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListTasks.html#DataSync.Paginator.ListTasks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/paginators/#listtaskspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTasksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/paginator/ListTasks.html#DataSync.Paginator.ListTasks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/paginators/#listtaskspaginator)
        """
