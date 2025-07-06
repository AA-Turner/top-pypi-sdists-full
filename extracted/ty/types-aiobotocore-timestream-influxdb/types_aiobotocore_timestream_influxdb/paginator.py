"""
Type annotations for timestream-influxdb service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_timestream_influxdb.client import TimestreamInfluxDBClient
    from types_aiobotocore_timestream_influxdb.paginator import (
        ListDbClustersPaginator,
        ListDbInstancesForClusterPaginator,
        ListDbInstancesPaginator,
        ListDbParameterGroupsPaginator,
    )

    session = get_session()
    with session.create_client("timestream-influxdb") as client:
        client: TimestreamInfluxDBClient

        list_db_clusters_paginator: ListDbClustersPaginator = client.get_paginator("list_db_clusters")
        list_db_instances_for_cluster_paginator: ListDbInstancesForClusterPaginator = client.get_paginator("list_db_instances_for_cluster")
        list_db_instances_paginator: ListDbInstancesPaginator = client.get_paginator("list_db_instances")
        list_db_parameter_groups_paginator: ListDbParameterGroupsPaginator = client.get_paginator("list_db_parameter_groups")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListDbClustersInputPaginateTypeDef,
    ListDbClustersOutputTypeDef,
    ListDbInstancesForClusterInputPaginateTypeDef,
    ListDbInstancesForClusterOutputTypeDef,
    ListDbInstancesInputPaginateTypeDef,
    ListDbInstancesOutputTypeDef,
    ListDbParameterGroupsInputPaginateTypeDef,
    ListDbParameterGroupsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListDbClustersPaginator",
    "ListDbInstancesForClusterPaginator",
    "ListDbInstancesPaginator",
    "ListDbParameterGroupsPaginator",
)


if TYPE_CHECKING:
    _ListDbClustersPaginatorBase = AioPaginator[ListDbClustersOutputTypeDef]
else:
    _ListDbClustersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDbClustersPaginator(_ListDbClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/paginator/ListDbClusters.html#TimestreamInfluxDB.Paginator.ListDbClusters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/paginators/#listdbclusterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDbClustersInputPaginateTypeDef]
    ) -> AioPageIterator[ListDbClustersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/paginator/ListDbClusters.html#TimestreamInfluxDB.Paginator.ListDbClusters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/paginators/#listdbclusterspaginator)
        """


if TYPE_CHECKING:
    _ListDbInstancesForClusterPaginatorBase = AioPaginator[ListDbInstancesForClusterOutputTypeDef]
else:
    _ListDbInstancesForClusterPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDbInstancesForClusterPaginator(_ListDbInstancesForClusterPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/paginator/ListDbInstancesForCluster.html#TimestreamInfluxDB.Paginator.ListDbInstancesForCluster)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/paginators/#listdbinstancesforclusterpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDbInstancesForClusterInputPaginateTypeDef]
    ) -> AioPageIterator[ListDbInstancesForClusterOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/paginator/ListDbInstancesForCluster.html#TimestreamInfluxDB.Paginator.ListDbInstancesForCluster.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/paginators/#listdbinstancesforclusterpaginator)
        """


if TYPE_CHECKING:
    _ListDbInstancesPaginatorBase = AioPaginator[ListDbInstancesOutputTypeDef]
else:
    _ListDbInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDbInstancesPaginator(_ListDbInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/paginator/ListDbInstances.html#TimestreamInfluxDB.Paginator.ListDbInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/paginators/#listdbinstancespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDbInstancesInputPaginateTypeDef]
    ) -> AioPageIterator[ListDbInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/paginator/ListDbInstances.html#TimestreamInfluxDB.Paginator.ListDbInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/paginators/#listdbinstancespaginator)
        """


if TYPE_CHECKING:
    _ListDbParameterGroupsPaginatorBase = AioPaginator[ListDbParameterGroupsOutputTypeDef]
else:
    _ListDbParameterGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDbParameterGroupsPaginator(_ListDbParameterGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/paginator/ListDbParameterGroups.html#TimestreamInfluxDB.Paginator.ListDbParameterGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/paginators/#listdbparametergroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDbParameterGroupsInputPaginateTypeDef]
    ) -> AioPageIterator[ListDbParameterGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/paginator/ListDbParameterGroups.html#TimestreamInfluxDB.Paginator.ListDbParameterGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/paginators/#listdbparametergroupspaginator)
        """
