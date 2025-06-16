"""
Type annotations for neptune service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_neptune.client import NeptuneClient
    from types_aiobotocore_neptune.paginator import (
        DescribeDBClusterEndpointsPaginator,
        DescribeDBClusterParameterGroupsPaginator,
        DescribeDBClusterParametersPaginator,
        DescribeDBClusterSnapshotsPaginator,
        DescribeDBClustersPaginator,
        DescribeDBEngineVersionsPaginator,
        DescribeDBInstancesPaginator,
        DescribeDBParameterGroupsPaginator,
        DescribeDBParametersPaginator,
        DescribeDBSubnetGroupsPaginator,
        DescribeEngineDefaultParametersPaginator,
        DescribeEventSubscriptionsPaginator,
        DescribeEventsPaginator,
        DescribeGlobalClustersPaginator,
        DescribeOrderableDBInstanceOptionsPaginator,
        DescribePendingMaintenanceActionsPaginator,
    )

    session = get_session()
    with session.create_client("neptune") as client:
        client: NeptuneClient

        describe_db_cluster_endpoints_paginator: DescribeDBClusterEndpointsPaginator = client.get_paginator("describe_db_cluster_endpoints")
        describe_db_cluster_parameter_groups_paginator: DescribeDBClusterParameterGroupsPaginator = client.get_paginator("describe_db_cluster_parameter_groups")
        describe_db_cluster_parameters_paginator: DescribeDBClusterParametersPaginator = client.get_paginator("describe_db_cluster_parameters")
        describe_db_cluster_snapshots_paginator: DescribeDBClusterSnapshotsPaginator = client.get_paginator("describe_db_cluster_snapshots")
        describe_db_clusters_paginator: DescribeDBClustersPaginator = client.get_paginator("describe_db_clusters")
        describe_db_engine_versions_paginator: DescribeDBEngineVersionsPaginator = client.get_paginator("describe_db_engine_versions")
        describe_db_instances_paginator: DescribeDBInstancesPaginator = client.get_paginator("describe_db_instances")
        describe_db_parameter_groups_paginator: DescribeDBParameterGroupsPaginator = client.get_paginator("describe_db_parameter_groups")
        describe_db_parameters_paginator: DescribeDBParametersPaginator = client.get_paginator("describe_db_parameters")
        describe_db_subnet_groups_paginator: DescribeDBSubnetGroupsPaginator = client.get_paginator("describe_db_subnet_groups")
        describe_engine_default_parameters_paginator: DescribeEngineDefaultParametersPaginator = client.get_paginator("describe_engine_default_parameters")
        describe_event_subscriptions_paginator: DescribeEventSubscriptionsPaginator = client.get_paginator("describe_event_subscriptions")
        describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
        describe_global_clusters_paginator: DescribeGlobalClustersPaginator = client.get_paginator("describe_global_clusters")
        describe_orderable_db_instance_options_paginator: DescribeOrderableDBInstanceOptionsPaginator = client.get_paginator("describe_orderable_db_instance_options")
        describe_pending_maintenance_actions_paginator: DescribePendingMaintenanceActionsPaginator = client.get_paginator("describe_pending_maintenance_actions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DBClusterEndpointMessageTypeDef,
    DBClusterMessageTypeDef,
    DBClusterParameterGroupDetailsTypeDef,
    DBClusterParameterGroupsMessageTypeDef,
    DBClusterSnapshotMessageTypeDef,
    DBEngineVersionMessageTypeDef,
    DBInstanceMessageTypeDef,
    DBParameterGroupDetailsTypeDef,
    DBParameterGroupsMessageTypeDef,
    DBSubnetGroupMessageTypeDef,
    DescribeDBClusterEndpointsMessagePaginateTypeDef,
    DescribeDBClusterParameterGroupsMessagePaginateTypeDef,
    DescribeDBClusterParametersMessagePaginateTypeDef,
    DescribeDBClustersMessagePaginateTypeDef,
    DescribeDBClusterSnapshotsMessagePaginateTypeDef,
    DescribeDBEngineVersionsMessagePaginateTypeDef,
    DescribeDBInstancesMessagePaginateTypeDef,
    DescribeDBParameterGroupsMessagePaginateTypeDef,
    DescribeDBParametersMessagePaginateTypeDef,
    DescribeDBSubnetGroupsMessagePaginateTypeDef,
    DescribeEngineDefaultParametersMessagePaginateTypeDef,
    DescribeEngineDefaultParametersResultTypeDef,
    DescribeEventsMessagePaginateTypeDef,
    DescribeEventSubscriptionsMessagePaginateTypeDef,
    DescribeGlobalClustersMessagePaginateTypeDef,
    DescribeOrderableDBInstanceOptionsMessagePaginateTypeDef,
    DescribePendingMaintenanceActionsMessagePaginateTypeDef,
    EventsMessageTypeDef,
    EventSubscriptionsMessageTypeDef,
    GlobalClustersMessageTypeDef,
    OrderableDBInstanceOptionsMessageTypeDef,
    PendingMaintenanceActionsMessageTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeDBClusterEndpointsPaginator",
    "DescribeDBClusterParameterGroupsPaginator",
    "DescribeDBClusterParametersPaginator",
    "DescribeDBClusterSnapshotsPaginator",
    "DescribeDBClustersPaginator",
    "DescribeDBEngineVersionsPaginator",
    "DescribeDBInstancesPaginator",
    "DescribeDBParameterGroupsPaginator",
    "DescribeDBParametersPaginator",
    "DescribeDBSubnetGroupsPaginator",
    "DescribeEngineDefaultParametersPaginator",
    "DescribeEventSubscriptionsPaginator",
    "DescribeEventsPaginator",
    "DescribeGlobalClustersPaginator",
    "DescribeOrderableDBInstanceOptionsPaginator",
    "DescribePendingMaintenanceActionsPaginator",
)

if TYPE_CHECKING:
    _DescribeDBClusterEndpointsPaginatorBase = AioPaginator[DBClusterEndpointMessageTypeDef]
else:
    _DescribeDBClusterEndpointsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeDBClusterEndpointsPaginator(_DescribeDBClusterEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeDBClusterEndpoints.html#Neptune.Paginator.DescribeDBClusterEndpoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describedbclusterendpointspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBClusterEndpointsMessagePaginateTypeDef]
    ) -> AioPageIterator[DBClusterEndpointMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeDBClusterEndpoints.html#Neptune.Paginator.DescribeDBClusterEndpoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describedbclusterendpointspaginator)
        """

if TYPE_CHECKING:
    _DescribeDBClusterParameterGroupsPaginatorBase = AioPaginator[
        DBClusterParameterGroupsMessageTypeDef
    ]
else:
    _DescribeDBClusterParameterGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeDBClusterParameterGroupsPaginator(_DescribeDBClusterParameterGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeDBClusterParameterGroups.html#Neptune.Paginator.DescribeDBClusterParameterGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describedbclusterparametergroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBClusterParameterGroupsMessagePaginateTypeDef]
    ) -> AioPageIterator[DBClusterParameterGroupsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeDBClusterParameterGroups.html#Neptune.Paginator.DescribeDBClusterParameterGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describedbclusterparametergroupspaginator)
        """

if TYPE_CHECKING:
    _DescribeDBClusterParametersPaginatorBase = AioPaginator[DBClusterParameterGroupDetailsTypeDef]
else:
    _DescribeDBClusterParametersPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeDBClusterParametersPaginator(_DescribeDBClusterParametersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeDBClusterParameters.html#Neptune.Paginator.DescribeDBClusterParameters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describedbclusterparameterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBClusterParametersMessagePaginateTypeDef]
    ) -> AioPageIterator[DBClusterParameterGroupDetailsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeDBClusterParameters.html#Neptune.Paginator.DescribeDBClusterParameters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describedbclusterparameterspaginator)
        """

if TYPE_CHECKING:
    _DescribeDBClusterSnapshotsPaginatorBase = AioPaginator[DBClusterSnapshotMessageTypeDef]
else:
    _DescribeDBClusterSnapshotsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeDBClusterSnapshotsPaginator(_DescribeDBClusterSnapshotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeDBClusterSnapshots.html#Neptune.Paginator.DescribeDBClusterSnapshots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describedbclustersnapshotspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBClusterSnapshotsMessagePaginateTypeDef]
    ) -> AioPageIterator[DBClusterSnapshotMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeDBClusterSnapshots.html#Neptune.Paginator.DescribeDBClusterSnapshots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describedbclustersnapshotspaginator)
        """

if TYPE_CHECKING:
    _DescribeDBClustersPaginatorBase = AioPaginator[DBClusterMessageTypeDef]
else:
    _DescribeDBClustersPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeDBClustersPaginator(_DescribeDBClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeDBClusters.html#Neptune.Paginator.DescribeDBClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describedbclusterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBClustersMessagePaginateTypeDef]
    ) -> AioPageIterator[DBClusterMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeDBClusters.html#Neptune.Paginator.DescribeDBClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describedbclusterspaginator)
        """

if TYPE_CHECKING:
    _DescribeDBEngineVersionsPaginatorBase = AioPaginator[DBEngineVersionMessageTypeDef]
else:
    _DescribeDBEngineVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeDBEngineVersionsPaginator(_DescribeDBEngineVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeDBEngineVersions.html#Neptune.Paginator.DescribeDBEngineVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describedbengineversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBEngineVersionsMessagePaginateTypeDef]
    ) -> AioPageIterator[DBEngineVersionMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeDBEngineVersions.html#Neptune.Paginator.DescribeDBEngineVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describedbengineversionspaginator)
        """

if TYPE_CHECKING:
    _DescribeDBInstancesPaginatorBase = AioPaginator[DBInstanceMessageTypeDef]
else:
    _DescribeDBInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeDBInstancesPaginator(_DescribeDBInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeDBInstances.html#Neptune.Paginator.DescribeDBInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describedbinstancespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBInstancesMessagePaginateTypeDef]
    ) -> AioPageIterator[DBInstanceMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeDBInstances.html#Neptune.Paginator.DescribeDBInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describedbinstancespaginator)
        """

if TYPE_CHECKING:
    _DescribeDBParameterGroupsPaginatorBase = AioPaginator[DBParameterGroupsMessageTypeDef]
else:
    _DescribeDBParameterGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeDBParameterGroupsPaginator(_DescribeDBParameterGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeDBParameterGroups.html#Neptune.Paginator.DescribeDBParameterGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describedbparametergroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBParameterGroupsMessagePaginateTypeDef]
    ) -> AioPageIterator[DBParameterGroupsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeDBParameterGroups.html#Neptune.Paginator.DescribeDBParameterGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describedbparametergroupspaginator)
        """

if TYPE_CHECKING:
    _DescribeDBParametersPaginatorBase = AioPaginator[DBParameterGroupDetailsTypeDef]
else:
    _DescribeDBParametersPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeDBParametersPaginator(_DescribeDBParametersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeDBParameters.html#Neptune.Paginator.DescribeDBParameters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describedbparameterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBParametersMessagePaginateTypeDef]
    ) -> AioPageIterator[DBParameterGroupDetailsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeDBParameters.html#Neptune.Paginator.DescribeDBParameters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describedbparameterspaginator)
        """

if TYPE_CHECKING:
    _DescribeDBSubnetGroupsPaginatorBase = AioPaginator[DBSubnetGroupMessageTypeDef]
else:
    _DescribeDBSubnetGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeDBSubnetGroupsPaginator(_DescribeDBSubnetGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeDBSubnetGroups.html#Neptune.Paginator.DescribeDBSubnetGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describedbsubnetgroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBSubnetGroupsMessagePaginateTypeDef]
    ) -> AioPageIterator[DBSubnetGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeDBSubnetGroups.html#Neptune.Paginator.DescribeDBSubnetGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describedbsubnetgroupspaginator)
        """

if TYPE_CHECKING:
    _DescribeEngineDefaultParametersPaginatorBase = AioPaginator[
        DescribeEngineDefaultParametersResultTypeDef
    ]
else:
    _DescribeEngineDefaultParametersPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeEngineDefaultParametersPaginator(_DescribeEngineDefaultParametersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeEngineDefaultParameters.html#Neptune.Paginator.DescribeEngineDefaultParameters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describeenginedefaultparameterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEngineDefaultParametersMessagePaginateTypeDef]
    ) -> AioPageIterator[DescribeEngineDefaultParametersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeEngineDefaultParameters.html#Neptune.Paginator.DescribeEngineDefaultParameters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describeenginedefaultparameterspaginator)
        """

if TYPE_CHECKING:
    _DescribeEventSubscriptionsPaginatorBase = AioPaginator[EventSubscriptionsMessageTypeDef]
else:
    _DescribeEventSubscriptionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeEventSubscriptionsPaginator(_DescribeEventSubscriptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeEventSubscriptions.html#Neptune.Paginator.DescribeEventSubscriptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describeeventsubscriptionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEventSubscriptionsMessagePaginateTypeDef]
    ) -> AioPageIterator[EventSubscriptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeEventSubscriptions.html#Neptune.Paginator.DescribeEventSubscriptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describeeventsubscriptionspaginator)
        """

if TYPE_CHECKING:
    _DescribeEventsPaginatorBase = AioPaginator[EventsMessageTypeDef]
else:
    _DescribeEventsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeEventsPaginator(_DescribeEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeEvents.html#Neptune.Paginator.DescribeEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describeeventspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEventsMessagePaginateTypeDef]
    ) -> AioPageIterator[EventsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeEvents.html#Neptune.Paginator.DescribeEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describeeventspaginator)
        """

if TYPE_CHECKING:
    _DescribeGlobalClustersPaginatorBase = AioPaginator[GlobalClustersMessageTypeDef]
else:
    _DescribeGlobalClustersPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeGlobalClustersPaginator(_DescribeGlobalClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeGlobalClusters.html#Neptune.Paginator.DescribeGlobalClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describeglobalclusterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeGlobalClustersMessagePaginateTypeDef]
    ) -> AioPageIterator[GlobalClustersMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeGlobalClusters.html#Neptune.Paginator.DescribeGlobalClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describeglobalclusterspaginator)
        """

if TYPE_CHECKING:
    _DescribeOrderableDBInstanceOptionsPaginatorBase = AioPaginator[
        OrderableDBInstanceOptionsMessageTypeDef
    ]
else:
    _DescribeOrderableDBInstanceOptionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeOrderableDBInstanceOptionsPaginator(_DescribeOrderableDBInstanceOptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeOrderableDBInstanceOptions.html#Neptune.Paginator.DescribeOrderableDBInstanceOptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describeorderabledbinstanceoptionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeOrderableDBInstanceOptionsMessagePaginateTypeDef]
    ) -> AioPageIterator[OrderableDBInstanceOptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribeOrderableDBInstanceOptions.html#Neptune.Paginator.DescribeOrderableDBInstanceOptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describeorderabledbinstanceoptionspaginator)
        """

if TYPE_CHECKING:
    _DescribePendingMaintenanceActionsPaginatorBase = AioPaginator[
        PendingMaintenanceActionsMessageTypeDef
    ]
else:
    _DescribePendingMaintenanceActionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribePendingMaintenanceActionsPaginator(_DescribePendingMaintenanceActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribePendingMaintenanceActions.html#Neptune.Paginator.DescribePendingMaintenanceActions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describependingmaintenanceactionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribePendingMaintenanceActionsMessagePaginateTypeDef]
    ) -> AioPageIterator[PendingMaintenanceActionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune/paginator/DescribePendingMaintenanceActions.html#Neptune.Paginator.DescribePendingMaintenanceActions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/paginators/#describependingmaintenanceactionspaginator)
        """
