"""
Type annotations for elasticache service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_elasticache.client import ElastiCacheClient
    from types_aiobotocore_elasticache.paginator import (
        DescribeCacheClustersPaginator,
        DescribeCacheEngineVersionsPaginator,
        DescribeCacheParameterGroupsPaginator,
        DescribeCacheParametersPaginator,
        DescribeCacheSecurityGroupsPaginator,
        DescribeCacheSubnetGroupsPaginator,
        DescribeEngineDefaultParametersPaginator,
        DescribeEventsPaginator,
        DescribeGlobalReplicationGroupsPaginator,
        DescribeReplicationGroupsPaginator,
        DescribeReservedCacheNodesOfferingsPaginator,
        DescribeReservedCacheNodesPaginator,
        DescribeServerlessCacheSnapshotsPaginator,
        DescribeServerlessCachesPaginator,
        DescribeServiceUpdatesPaginator,
        DescribeSnapshotsPaginator,
        DescribeUpdateActionsPaginator,
        DescribeUserGroupsPaginator,
        DescribeUsersPaginator,
    )

    session = get_session()
    with session.create_client("elasticache") as client:
        client: ElastiCacheClient

        describe_cache_clusters_paginator: DescribeCacheClustersPaginator = client.get_paginator("describe_cache_clusters")
        describe_cache_engine_versions_paginator: DescribeCacheEngineVersionsPaginator = client.get_paginator("describe_cache_engine_versions")
        describe_cache_parameter_groups_paginator: DescribeCacheParameterGroupsPaginator = client.get_paginator("describe_cache_parameter_groups")
        describe_cache_parameters_paginator: DescribeCacheParametersPaginator = client.get_paginator("describe_cache_parameters")
        describe_cache_security_groups_paginator: DescribeCacheSecurityGroupsPaginator = client.get_paginator("describe_cache_security_groups")
        describe_cache_subnet_groups_paginator: DescribeCacheSubnetGroupsPaginator = client.get_paginator("describe_cache_subnet_groups")
        describe_engine_default_parameters_paginator: DescribeEngineDefaultParametersPaginator = client.get_paginator("describe_engine_default_parameters")
        describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
        describe_global_replication_groups_paginator: DescribeGlobalReplicationGroupsPaginator = client.get_paginator("describe_global_replication_groups")
        describe_replication_groups_paginator: DescribeReplicationGroupsPaginator = client.get_paginator("describe_replication_groups")
        describe_reserved_cache_nodes_offerings_paginator: DescribeReservedCacheNodesOfferingsPaginator = client.get_paginator("describe_reserved_cache_nodes_offerings")
        describe_reserved_cache_nodes_paginator: DescribeReservedCacheNodesPaginator = client.get_paginator("describe_reserved_cache_nodes")
        describe_serverless_cache_snapshots_paginator: DescribeServerlessCacheSnapshotsPaginator = client.get_paginator("describe_serverless_cache_snapshots")
        describe_serverless_caches_paginator: DescribeServerlessCachesPaginator = client.get_paginator("describe_serverless_caches")
        describe_service_updates_paginator: DescribeServiceUpdatesPaginator = client.get_paginator("describe_service_updates")
        describe_snapshots_paginator: DescribeSnapshotsPaginator = client.get_paginator("describe_snapshots")
        describe_update_actions_paginator: DescribeUpdateActionsPaginator = client.get_paginator("describe_update_actions")
        describe_user_groups_paginator: DescribeUserGroupsPaginator = client.get_paginator("describe_user_groups")
        describe_users_paginator: DescribeUsersPaginator = client.get_paginator("describe_users")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    CacheClusterMessageTypeDef,
    CacheEngineVersionMessageTypeDef,
    CacheParameterGroupDetailsTypeDef,
    CacheParameterGroupsMessageTypeDef,
    CacheSecurityGroupMessageTypeDef,
    CacheSubnetGroupMessageTypeDef,
    DescribeCacheClustersMessagePaginateTypeDef,
    DescribeCacheEngineVersionsMessagePaginateTypeDef,
    DescribeCacheParameterGroupsMessagePaginateTypeDef,
    DescribeCacheParametersMessagePaginateTypeDef,
    DescribeCacheSecurityGroupsMessagePaginateTypeDef,
    DescribeCacheSubnetGroupsMessagePaginateTypeDef,
    DescribeEngineDefaultParametersMessagePaginateTypeDef,
    DescribeEngineDefaultParametersResultTypeDef,
    DescribeEventsMessagePaginateTypeDef,
    DescribeGlobalReplicationGroupsMessagePaginateTypeDef,
    DescribeGlobalReplicationGroupsResultTypeDef,
    DescribeReplicationGroupsMessagePaginateTypeDef,
    DescribeReservedCacheNodesMessagePaginateTypeDef,
    DescribeReservedCacheNodesOfferingsMessagePaginateTypeDef,
    DescribeServerlessCacheSnapshotsRequestPaginateTypeDef,
    DescribeServerlessCacheSnapshotsResponseTypeDef,
    DescribeServerlessCachesRequestPaginateTypeDef,
    DescribeServerlessCachesResponseTypeDef,
    DescribeServiceUpdatesMessagePaginateTypeDef,
    DescribeSnapshotsListMessageTypeDef,
    DescribeSnapshotsMessagePaginateTypeDef,
    DescribeUpdateActionsMessagePaginateTypeDef,
    DescribeUserGroupsMessagePaginateTypeDef,
    DescribeUserGroupsResultTypeDef,
    DescribeUsersMessagePaginateTypeDef,
    DescribeUsersResultTypeDef,
    EventsMessageTypeDef,
    ReplicationGroupMessageTypeDef,
    ReservedCacheNodeMessageTypeDef,
    ReservedCacheNodesOfferingMessageTypeDef,
    ServiceUpdatesMessageTypeDef,
    UpdateActionsMessageTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeCacheClustersPaginator",
    "DescribeCacheEngineVersionsPaginator",
    "DescribeCacheParameterGroupsPaginator",
    "DescribeCacheParametersPaginator",
    "DescribeCacheSecurityGroupsPaginator",
    "DescribeCacheSubnetGroupsPaginator",
    "DescribeEngineDefaultParametersPaginator",
    "DescribeEventsPaginator",
    "DescribeGlobalReplicationGroupsPaginator",
    "DescribeReplicationGroupsPaginator",
    "DescribeReservedCacheNodesOfferingsPaginator",
    "DescribeReservedCacheNodesPaginator",
    "DescribeServerlessCacheSnapshotsPaginator",
    "DescribeServerlessCachesPaginator",
    "DescribeServiceUpdatesPaginator",
    "DescribeSnapshotsPaginator",
    "DescribeUpdateActionsPaginator",
    "DescribeUserGroupsPaginator",
    "DescribeUsersPaginator",
)


if TYPE_CHECKING:
    _DescribeCacheClustersPaginatorBase = AioPaginator[CacheClusterMessageTypeDef]
else:
    _DescribeCacheClustersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeCacheClustersPaginator(_DescribeCacheClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheClusters.html#ElastiCache.Paginator.DescribeCacheClusters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describecacheclusterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeCacheClustersMessagePaginateTypeDef]
    ) -> AioPageIterator[CacheClusterMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheClusters.html#ElastiCache.Paginator.DescribeCacheClusters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describecacheclusterspaginator)
        """


if TYPE_CHECKING:
    _DescribeCacheEngineVersionsPaginatorBase = AioPaginator[CacheEngineVersionMessageTypeDef]
else:
    _DescribeCacheEngineVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeCacheEngineVersionsPaginator(_DescribeCacheEngineVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheEngineVersions.html#ElastiCache.Paginator.DescribeCacheEngineVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describecacheengineversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeCacheEngineVersionsMessagePaginateTypeDef]
    ) -> AioPageIterator[CacheEngineVersionMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheEngineVersions.html#ElastiCache.Paginator.DescribeCacheEngineVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describecacheengineversionspaginator)
        """


if TYPE_CHECKING:
    _DescribeCacheParameterGroupsPaginatorBase = AioPaginator[CacheParameterGroupsMessageTypeDef]
else:
    _DescribeCacheParameterGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeCacheParameterGroupsPaginator(_DescribeCacheParameterGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheParameterGroups.html#ElastiCache.Paginator.DescribeCacheParameterGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describecacheparametergroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeCacheParameterGroupsMessagePaginateTypeDef]
    ) -> AioPageIterator[CacheParameterGroupsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheParameterGroups.html#ElastiCache.Paginator.DescribeCacheParameterGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describecacheparametergroupspaginator)
        """


if TYPE_CHECKING:
    _DescribeCacheParametersPaginatorBase = AioPaginator[CacheParameterGroupDetailsTypeDef]
else:
    _DescribeCacheParametersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeCacheParametersPaginator(_DescribeCacheParametersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheParameters.html#ElastiCache.Paginator.DescribeCacheParameters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describecacheparameterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeCacheParametersMessagePaginateTypeDef]
    ) -> AioPageIterator[CacheParameterGroupDetailsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheParameters.html#ElastiCache.Paginator.DescribeCacheParameters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describecacheparameterspaginator)
        """


if TYPE_CHECKING:
    _DescribeCacheSecurityGroupsPaginatorBase = AioPaginator[CacheSecurityGroupMessageTypeDef]
else:
    _DescribeCacheSecurityGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeCacheSecurityGroupsPaginator(_DescribeCacheSecurityGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheSecurityGroups.html#ElastiCache.Paginator.DescribeCacheSecurityGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describecachesecuritygroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeCacheSecurityGroupsMessagePaginateTypeDef]
    ) -> AioPageIterator[CacheSecurityGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheSecurityGroups.html#ElastiCache.Paginator.DescribeCacheSecurityGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describecachesecuritygroupspaginator)
        """


if TYPE_CHECKING:
    _DescribeCacheSubnetGroupsPaginatorBase = AioPaginator[CacheSubnetGroupMessageTypeDef]
else:
    _DescribeCacheSubnetGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeCacheSubnetGroupsPaginator(_DescribeCacheSubnetGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheSubnetGroups.html#ElastiCache.Paginator.DescribeCacheSubnetGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describecachesubnetgroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeCacheSubnetGroupsMessagePaginateTypeDef]
    ) -> AioPageIterator[CacheSubnetGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheSubnetGroups.html#ElastiCache.Paginator.DescribeCacheSubnetGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describecachesubnetgroupspaginator)
        """


if TYPE_CHECKING:
    _DescribeEngineDefaultParametersPaginatorBase = AioPaginator[
        DescribeEngineDefaultParametersResultTypeDef
    ]
else:
    _DescribeEngineDefaultParametersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeEngineDefaultParametersPaginator(_DescribeEngineDefaultParametersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeEngineDefaultParameters.html#ElastiCache.Paginator.DescribeEngineDefaultParameters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeenginedefaultparameterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEngineDefaultParametersMessagePaginateTypeDef]
    ) -> AioPageIterator[DescribeEngineDefaultParametersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeEngineDefaultParameters.html#ElastiCache.Paginator.DescribeEngineDefaultParameters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeenginedefaultparameterspaginator)
        """


if TYPE_CHECKING:
    _DescribeEventsPaginatorBase = AioPaginator[EventsMessageTypeDef]
else:
    _DescribeEventsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeEventsPaginator(_DescribeEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeEvents.html#ElastiCache.Paginator.DescribeEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeeventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEventsMessagePaginateTypeDef]
    ) -> AioPageIterator[EventsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeEvents.html#ElastiCache.Paginator.DescribeEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeeventspaginator)
        """


if TYPE_CHECKING:
    _DescribeGlobalReplicationGroupsPaginatorBase = AioPaginator[
        DescribeGlobalReplicationGroupsResultTypeDef
    ]
else:
    _DescribeGlobalReplicationGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeGlobalReplicationGroupsPaginator(_DescribeGlobalReplicationGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeGlobalReplicationGroups.html#ElastiCache.Paginator.DescribeGlobalReplicationGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeglobalreplicationgroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeGlobalReplicationGroupsMessagePaginateTypeDef]
    ) -> AioPageIterator[DescribeGlobalReplicationGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeGlobalReplicationGroups.html#ElastiCache.Paginator.DescribeGlobalReplicationGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeglobalreplicationgroupspaginator)
        """


if TYPE_CHECKING:
    _DescribeReplicationGroupsPaginatorBase = AioPaginator[ReplicationGroupMessageTypeDef]
else:
    _DescribeReplicationGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeReplicationGroupsPaginator(_DescribeReplicationGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeReplicationGroups.html#ElastiCache.Paginator.DescribeReplicationGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describereplicationgroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReplicationGroupsMessagePaginateTypeDef]
    ) -> AioPageIterator[ReplicationGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeReplicationGroups.html#ElastiCache.Paginator.DescribeReplicationGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describereplicationgroupspaginator)
        """


if TYPE_CHECKING:
    _DescribeReservedCacheNodesOfferingsPaginatorBase = AioPaginator[
        ReservedCacheNodesOfferingMessageTypeDef
    ]
else:
    _DescribeReservedCacheNodesOfferingsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeReservedCacheNodesOfferingsPaginator(
    _DescribeReservedCacheNodesOfferingsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeReservedCacheNodesOfferings.html#ElastiCache.Paginator.DescribeReservedCacheNodesOfferings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describereservedcachenodesofferingspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReservedCacheNodesOfferingsMessagePaginateTypeDef]
    ) -> AioPageIterator[ReservedCacheNodesOfferingMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeReservedCacheNodesOfferings.html#ElastiCache.Paginator.DescribeReservedCacheNodesOfferings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describereservedcachenodesofferingspaginator)
        """


if TYPE_CHECKING:
    _DescribeReservedCacheNodesPaginatorBase = AioPaginator[ReservedCacheNodeMessageTypeDef]
else:
    _DescribeReservedCacheNodesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeReservedCacheNodesPaginator(_DescribeReservedCacheNodesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeReservedCacheNodes.html#ElastiCache.Paginator.DescribeReservedCacheNodes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describereservedcachenodespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReservedCacheNodesMessagePaginateTypeDef]
    ) -> AioPageIterator[ReservedCacheNodeMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeReservedCacheNodes.html#ElastiCache.Paginator.DescribeReservedCacheNodes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describereservedcachenodespaginator)
        """


if TYPE_CHECKING:
    _DescribeServerlessCacheSnapshotsPaginatorBase = AioPaginator[
        DescribeServerlessCacheSnapshotsResponseTypeDef
    ]
else:
    _DescribeServerlessCacheSnapshotsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeServerlessCacheSnapshotsPaginator(_DescribeServerlessCacheSnapshotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeServerlessCacheSnapshots.html#ElastiCache.Paginator.DescribeServerlessCacheSnapshots)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeserverlesscachesnapshotspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeServerlessCacheSnapshotsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeServerlessCacheSnapshotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeServerlessCacheSnapshots.html#ElastiCache.Paginator.DescribeServerlessCacheSnapshots.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeserverlesscachesnapshotspaginator)
        """


if TYPE_CHECKING:
    _DescribeServerlessCachesPaginatorBase = AioPaginator[DescribeServerlessCachesResponseTypeDef]
else:
    _DescribeServerlessCachesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeServerlessCachesPaginator(_DescribeServerlessCachesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeServerlessCaches.html#ElastiCache.Paginator.DescribeServerlessCaches)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeserverlesscachespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeServerlessCachesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeServerlessCachesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeServerlessCaches.html#ElastiCache.Paginator.DescribeServerlessCaches.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeserverlesscachespaginator)
        """


if TYPE_CHECKING:
    _DescribeServiceUpdatesPaginatorBase = AioPaginator[ServiceUpdatesMessageTypeDef]
else:
    _DescribeServiceUpdatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeServiceUpdatesPaginator(_DescribeServiceUpdatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeServiceUpdates.html#ElastiCache.Paginator.DescribeServiceUpdates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeserviceupdatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeServiceUpdatesMessagePaginateTypeDef]
    ) -> AioPageIterator[ServiceUpdatesMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeServiceUpdates.html#ElastiCache.Paginator.DescribeServiceUpdates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeserviceupdatespaginator)
        """


if TYPE_CHECKING:
    _DescribeSnapshotsPaginatorBase = AioPaginator[DescribeSnapshotsListMessageTypeDef]
else:
    _DescribeSnapshotsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeSnapshotsPaginator(_DescribeSnapshotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeSnapshots.html#ElastiCache.Paginator.DescribeSnapshots)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describesnapshotspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSnapshotsMessagePaginateTypeDef]
    ) -> AioPageIterator[DescribeSnapshotsListMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeSnapshots.html#ElastiCache.Paginator.DescribeSnapshots.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describesnapshotspaginator)
        """


if TYPE_CHECKING:
    _DescribeUpdateActionsPaginatorBase = AioPaginator[UpdateActionsMessageTypeDef]
else:
    _DescribeUpdateActionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeUpdateActionsPaginator(_DescribeUpdateActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeUpdateActions.html#ElastiCache.Paginator.DescribeUpdateActions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeupdateactionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeUpdateActionsMessagePaginateTypeDef]
    ) -> AioPageIterator[UpdateActionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeUpdateActions.html#ElastiCache.Paginator.DescribeUpdateActions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeupdateactionspaginator)
        """


if TYPE_CHECKING:
    _DescribeUserGroupsPaginatorBase = AioPaginator[DescribeUserGroupsResultTypeDef]
else:
    _DescribeUserGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeUserGroupsPaginator(_DescribeUserGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeUserGroups.html#ElastiCache.Paginator.DescribeUserGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeusergroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeUserGroupsMessagePaginateTypeDef]
    ) -> AioPageIterator[DescribeUserGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeUserGroups.html#ElastiCache.Paginator.DescribeUserGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeusergroupspaginator)
        """


if TYPE_CHECKING:
    _DescribeUsersPaginatorBase = AioPaginator[DescribeUsersResultTypeDef]
else:
    _DescribeUsersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeUsersPaginator(_DescribeUsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeUsers.html#ElastiCache.Paginator.DescribeUsers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeuserspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeUsersMessagePaginateTypeDef]
    ) -> AioPageIterator[DescribeUsersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeUsers.html#ElastiCache.Paginator.DescribeUsers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeuserspaginator)
        """
