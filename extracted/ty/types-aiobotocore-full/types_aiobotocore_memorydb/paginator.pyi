"""
Type annotations for memorydb service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_memorydb.client import MemoryDBClient
    from types_aiobotocore_memorydb.paginator import (
        DescribeACLsPaginator,
        DescribeClustersPaginator,
        DescribeEngineVersionsPaginator,
        DescribeEventsPaginator,
        DescribeMultiRegionClustersPaginator,
        DescribeParameterGroupsPaginator,
        DescribeParametersPaginator,
        DescribeReservedNodesOfferingsPaginator,
        DescribeReservedNodesPaginator,
        DescribeServiceUpdatesPaginator,
        DescribeSnapshotsPaginator,
        DescribeSubnetGroupsPaginator,
        DescribeUsersPaginator,
    )

    session = get_session()
    with session.create_client("memorydb") as client:
        client: MemoryDBClient

        describe_acls_paginator: DescribeACLsPaginator = client.get_paginator("describe_acls")
        describe_clusters_paginator: DescribeClustersPaginator = client.get_paginator("describe_clusters")
        describe_engine_versions_paginator: DescribeEngineVersionsPaginator = client.get_paginator("describe_engine_versions")
        describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
        describe_multi_region_clusters_paginator: DescribeMultiRegionClustersPaginator = client.get_paginator("describe_multi_region_clusters")
        describe_parameter_groups_paginator: DescribeParameterGroupsPaginator = client.get_paginator("describe_parameter_groups")
        describe_parameters_paginator: DescribeParametersPaginator = client.get_paginator("describe_parameters")
        describe_reserved_nodes_offerings_paginator: DescribeReservedNodesOfferingsPaginator = client.get_paginator("describe_reserved_nodes_offerings")
        describe_reserved_nodes_paginator: DescribeReservedNodesPaginator = client.get_paginator("describe_reserved_nodes")
        describe_service_updates_paginator: DescribeServiceUpdatesPaginator = client.get_paginator("describe_service_updates")
        describe_snapshots_paginator: DescribeSnapshotsPaginator = client.get_paginator("describe_snapshots")
        describe_subnet_groups_paginator: DescribeSubnetGroupsPaginator = client.get_paginator("describe_subnet_groups")
        describe_users_paginator: DescribeUsersPaginator = client.get_paginator("describe_users")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeACLsRequestPaginateTypeDef,
    DescribeACLsResponseTypeDef,
    DescribeClustersRequestPaginateTypeDef,
    DescribeClustersResponseTypeDef,
    DescribeEngineVersionsRequestPaginateTypeDef,
    DescribeEngineVersionsResponseTypeDef,
    DescribeEventsRequestPaginateTypeDef,
    DescribeEventsResponseTypeDef,
    DescribeMultiRegionClustersRequestPaginateTypeDef,
    DescribeMultiRegionClustersResponseTypeDef,
    DescribeParameterGroupsRequestPaginateTypeDef,
    DescribeParameterGroupsResponseTypeDef,
    DescribeParametersRequestPaginateTypeDef,
    DescribeParametersResponseTypeDef,
    DescribeReservedNodesOfferingsRequestPaginateTypeDef,
    DescribeReservedNodesOfferingsResponseTypeDef,
    DescribeReservedNodesRequestPaginateTypeDef,
    DescribeReservedNodesResponseTypeDef,
    DescribeServiceUpdatesRequestPaginateTypeDef,
    DescribeServiceUpdatesResponseTypeDef,
    DescribeSnapshotsRequestPaginateTypeDef,
    DescribeSnapshotsResponseTypeDef,
    DescribeSubnetGroupsRequestPaginateTypeDef,
    DescribeSubnetGroupsResponseTypeDef,
    DescribeUsersRequestPaginateTypeDef,
    DescribeUsersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeACLsPaginator",
    "DescribeClustersPaginator",
    "DescribeEngineVersionsPaginator",
    "DescribeEventsPaginator",
    "DescribeMultiRegionClustersPaginator",
    "DescribeParameterGroupsPaginator",
    "DescribeParametersPaginator",
    "DescribeReservedNodesOfferingsPaginator",
    "DescribeReservedNodesPaginator",
    "DescribeServiceUpdatesPaginator",
    "DescribeSnapshotsPaginator",
    "DescribeSubnetGroupsPaginator",
    "DescribeUsersPaginator",
)

if TYPE_CHECKING:
    _DescribeACLsPaginatorBase = AioPaginator[DescribeACLsResponseTypeDef]
else:
    _DescribeACLsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeACLsPaginator(_DescribeACLsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeACLs.html#MemoryDB.Paginator.DescribeACLs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describeaclspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeACLsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeACLsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeACLs.html#MemoryDB.Paginator.DescribeACLs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describeaclspaginator)
        """

if TYPE_CHECKING:
    _DescribeClustersPaginatorBase = AioPaginator[DescribeClustersResponseTypeDef]
else:
    _DescribeClustersPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeClustersPaginator(_DescribeClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeClusters.html#MemoryDB.Paginator.DescribeClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describeclusterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeClustersRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeClusters.html#MemoryDB.Paginator.DescribeClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describeclusterspaginator)
        """

if TYPE_CHECKING:
    _DescribeEngineVersionsPaginatorBase = AioPaginator[DescribeEngineVersionsResponseTypeDef]
else:
    _DescribeEngineVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeEngineVersionsPaginator(_DescribeEngineVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeEngineVersions.html#MemoryDB.Paginator.DescribeEngineVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describeengineversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEngineVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeEngineVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeEngineVersions.html#MemoryDB.Paginator.DescribeEngineVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describeengineversionspaginator)
        """

if TYPE_CHECKING:
    _DescribeEventsPaginatorBase = AioPaginator[DescribeEventsResponseTypeDef]
else:
    _DescribeEventsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeEventsPaginator(_DescribeEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeEvents.html#MemoryDB.Paginator.DescribeEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describeeventspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEventsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeEvents.html#MemoryDB.Paginator.DescribeEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describeeventspaginator)
        """

if TYPE_CHECKING:
    _DescribeMultiRegionClustersPaginatorBase = AioPaginator[
        DescribeMultiRegionClustersResponseTypeDef
    ]
else:
    _DescribeMultiRegionClustersPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeMultiRegionClustersPaginator(_DescribeMultiRegionClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeMultiRegionClusters.html#MemoryDB.Paginator.DescribeMultiRegionClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describemultiregionclusterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMultiRegionClustersRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeMultiRegionClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeMultiRegionClusters.html#MemoryDB.Paginator.DescribeMultiRegionClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describemultiregionclusterspaginator)
        """

if TYPE_CHECKING:
    _DescribeParameterGroupsPaginatorBase = AioPaginator[DescribeParameterGroupsResponseTypeDef]
else:
    _DescribeParameterGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeParameterGroupsPaginator(_DescribeParameterGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeParameterGroups.html#MemoryDB.Paginator.DescribeParameterGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describeparametergroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeParameterGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeParameterGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeParameterGroups.html#MemoryDB.Paginator.DescribeParameterGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describeparametergroupspaginator)
        """

if TYPE_CHECKING:
    _DescribeParametersPaginatorBase = AioPaginator[DescribeParametersResponseTypeDef]
else:
    _DescribeParametersPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeParametersPaginator(_DescribeParametersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeParameters.html#MemoryDB.Paginator.DescribeParameters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describeparameterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeParametersRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeParametersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeParameters.html#MemoryDB.Paginator.DescribeParameters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describeparameterspaginator)
        """

if TYPE_CHECKING:
    _DescribeReservedNodesOfferingsPaginatorBase = AioPaginator[
        DescribeReservedNodesOfferingsResponseTypeDef
    ]
else:
    _DescribeReservedNodesOfferingsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeReservedNodesOfferingsPaginator(_DescribeReservedNodesOfferingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeReservedNodesOfferings.html#MemoryDB.Paginator.DescribeReservedNodesOfferings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describereservednodesofferingspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReservedNodesOfferingsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeReservedNodesOfferingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeReservedNodesOfferings.html#MemoryDB.Paginator.DescribeReservedNodesOfferings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describereservednodesofferingspaginator)
        """

if TYPE_CHECKING:
    _DescribeReservedNodesPaginatorBase = AioPaginator[DescribeReservedNodesResponseTypeDef]
else:
    _DescribeReservedNodesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeReservedNodesPaginator(_DescribeReservedNodesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeReservedNodes.html#MemoryDB.Paginator.DescribeReservedNodes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describereservednodespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReservedNodesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeReservedNodesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeReservedNodes.html#MemoryDB.Paginator.DescribeReservedNodes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describereservednodespaginator)
        """

if TYPE_CHECKING:
    _DescribeServiceUpdatesPaginatorBase = AioPaginator[DescribeServiceUpdatesResponseTypeDef]
else:
    _DescribeServiceUpdatesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeServiceUpdatesPaginator(_DescribeServiceUpdatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeServiceUpdates.html#MemoryDB.Paginator.DescribeServiceUpdates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describeserviceupdatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeServiceUpdatesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeServiceUpdatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeServiceUpdates.html#MemoryDB.Paginator.DescribeServiceUpdates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describeserviceupdatespaginator)
        """

if TYPE_CHECKING:
    _DescribeSnapshotsPaginatorBase = AioPaginator[DescribeSnapshotsResponseTypeDef]
else:
    _DescribeSnapshotsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeSnapshotsPaginator(_DescribeSnapshotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeSnapshots.html#MemoryDB.Paginator.DescribeSnapshots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describesnapshotspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSnapshotsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeSnapshotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeSnapshots.html#MemoryDB.Paginator.DescribeSnapshots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describesnapshotspaginator)
        """

if TYPE_CHECKING:
    _DescribeSubnetGroupsPaginatorBase = AioPaginator[DescribeSubnetGroupsResponseTypeDef]
else:
    _DescribeSubnetGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeSubnetGroupsPaginator(_DescribeSubnetGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeSubnetGroups.html#MemoryDB.Paginator.DescribeSubnetGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describesubnetgroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSubnetGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeSubnetGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeSubnetGroups.html#MemoryDB.Paginator.DescribeSubnetGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describesubnetgroupspaginator)
        """

if TYPE_CHECKING:
    _DescribeUsersPaginatorBase = AioPaginator[DescribeUsersResponseTypeDef]
else:
    _DescribeUsersPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeUsersPaginator(_DescribeUsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeUsers.html#MemoryDB.Paginator.DescribeUsers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describeuserspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeUsersRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/paginator/DescribeUsers.html#MemoryDB.Paginator.DescribeUsers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/paginators/#describeuserspaginator)
        """
