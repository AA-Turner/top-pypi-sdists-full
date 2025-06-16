"""
Type annotations for docdb service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_docdb.client import DocDBClient
    from types_aiobotocore_docdb.paginator import (
        DescribeCertificatesPaginator,
        DescribeDBClusterParameterGroupsPaginator,
        DescribeDBClusterParametersPaginator,
        DescribeDBClusterSnapshotsPaginator,
        DescribeDBClustersPaginator,
        DescribeDBEngineVersionsPaginator,
        DescribeDBInstancesPaginator,
        DescribeDBSubnetGroupsPaginator,
        DescribeEventSubscriptionsPaginator,
        DescribeEventsPaginator,
        DescribeGlobalClustersPaginator,
        DescribeOrderableDBInstanceOptionsPaginator,
        DescribePendingMaintenanceActionsPaginator,
    )

    session = get_session()
    with session.create_client("docdb") as client:
        client: DocDBClient

        describe_certificates_paginator: DescribeCertificatesPaginator = client.get_paginator("describe_certificates")
        describe_db_cluster_parameter_groups_paginator: DescribeDBClusterParameterGroupsPaginator = client.get_paginator("describe_db_cluster_parameter_groups")
        describe_db_cluster_parameters_paginator: DescribeDBClusterParametersPaginator = client.get_paginator("describe_db_cluster_parameters")
        describe_db_cluster_snapshots_paginator: DescribeDBClusterSnapshotsPaginator = client.get_paginator("describe_db_cluster_snapshots")
        describe_db_clusters_paginator: DescribeDBClustersPaginator = client.get_paginator("describe_db_clusters")
        describe_db_engine_versions_paginator: DescribeDBEngineVersionsPaginator = client.get_paginator("describe_db_engine_versions")
        describe_db_instances_paginator: DescribeDBInstancesPaginator = client.get_paginator("describe_db_instances")
        describe_db_subnet_groups_paginator: DescribeDBSubnetGroupsPaginator = client.get_paginator("describe_db_subnet_groups")
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
    CertificateMessageTypeDef,
    DBClusterMessageTypeDef,
    DBClusterParameterGroupDetailsTypeDef,
    DBClusterParameterGroupsMessageTypeDef,
    DBClusterSnapshotMessageTypeDef,
    DBEngineVersionMessageTypeDef,
    DBInstanceMessageTypeDef,
    DBSubnetGroupMessageTypeDef,
    DescribeCertificatesMessagePaginateTypeDef,
    DescribeDBClusterParameterGroupsMessagePaginateTypeDef,
    DescribeDBClusterParametersMessagePaginateTypeDef,
    DescribeDBClustersMessagePaginateTypeDef,
    DescribeDBClusterSnapshotsMessagePaginateTypeDef,
    DescribeDBEngineVersionsMessagePaginateTypeDef,
    DescribeDBInstancesMessagePaginateTypeDef,
    DescribeDBSubnetGroupsMessagePaginateTypeDef,
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
    "DescribeCertificatesPaginator",
    "DescribeDBClusterParameterGroupsPaginator",
    "DescribeDBClusterParametersPaginator",
    "DescribeDBClusterSnapshotsPaginator",
    "DescribeDBClustersPaginator",
    "DescribeDBEngineVersionsPaginator",
    "DescribeDBInstancesPaginator",
    "DescribeDBSubnetGroupsPaginator",
    "DescribeEventSubscriptionsPaginator",
    "DescribeEventsPaginator",
    "DescribeGlobalClustersPaginator",
    "DescribeOrderableDBInstanceOptionsPaginator",
    "DescribePendingMaintenanceActionsPaginator",
)


if TYPE_CHECKING:
    _DescribeCertificatesPaginatorBase = AioPaginator[CertificateMessageTypeDef]
else:
    _DescribeCertificatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeCertificatesPaginator(_DescribeCertificatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeCertificates.html#DocDB.Paginator.DescribeCertificates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describecertificatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeCertificatesMessagePaginateTypeDef]
    ) -> AioPageIterator[CertificateMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeCertificates.html#DocDB.Paginator.DescribeCertificates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describecertificatespaginator)
        """


if TYPE_CHECKING:
    _DescribeDBClusterParameterGroupsPaginatorBase = AioPaginator[
        DBClusterParameterGroupsMessageTypeDef
    ]
else:
    _DescribeDBClusterParameterGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBClusterParameterGroupsPaginator(_DescribeDBClusterParameterGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBClusterParameterGroups.html#DocDB.Paginator.DescribeDBClusterParameterGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbclusterparametergroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBClusterParameterGroupsMessagePaginateTypeDef]
    ) -> AioPageIterator[DBClusterParameterGroupsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBClusterParameterGroups.html#DocDB.Paginator.DescribeDBClusterParameterGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbclusterparametergroupspaginator)
        """


if TYPE_CHECKING:
    _DescribeDBClusterParametersPaginatorBase = AioPaginator[DBClusterParameterGroupDetailsTypeDef]
else:
    _DescribeDBClusterParametersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBClusterParametersPaginator(_DescribeDBClusterParametersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBClusterParameters.html#DocDB.Paginator.DescribeDBClusterParameters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbclusterparameterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBClusterParametersMessagePaginateTypeDef]
    ) -> AioPageIterator[DBClusterParameterGroupDetailsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBClusterParameters.html#DocDB.Paginator.DescribeDBClusterParameters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbclusterparameterspaginator)
        """


if TYPE_CHECKING:
    _DescribeDBClusterSnapshotsPaginatorBase = AioPaginator[DBClusterSnapshotMessageTypeDef]
else:
    _DescribeDBClusterSnapshotsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBClusterSnapshotsPaginator(_DescribeDBClusterSnapshotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBClusterSnapshots.html#DocDB.Paginator.DescribeDBClusterSnapshots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbclustersnapshotspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBClusterSnapshotsMessagePaginateTypeDef]
    ) -> AioPageIterator[DBClusterSnapshotMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBClusterSnapshots.html#DocDB.Paginator.DescribeDBClusterSnapshots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbclustersnapshotspaginator)
        """


if TYPE_CHECKING:
    _DescribeDBClustersPaginatorBase = AioPaginator[DBClusterMessageTypeDef]
else:
    _DescribeDBClustersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBClustersPaginator(_DescribeDBClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBClusters.html#DocDB.Paginator.DescribeDBClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbclusterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBClustersMessagePaginateTypeDef]
    ) -> AioPageIterator[DBClusterMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBClusters.html#DocDB.Paginator.DescribeDBClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbclusterspaginator)
        """


if TYPE_CHECKING:
    _DescribeDBEngineVersionsPaginatorBase = AioPaginator[DBEngineVersionMessageTypeDef]
else:
    _DescribeDBEngineVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBEngineVersionsPaginator(_DescribeDBEngineVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBEngineVersions.html#DocDB.Paginator.DescribeDBEngineVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbengineversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBEngineVersionsMessagePaginateTypeDef]
    ) -> AioPageIterator[DBEngineVersionMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBEngineVersions.html#DocDB.Paginator.DescribeDBEngineVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbengineversionspaginator)
        """


if TYPE_CHECKING:
    _DescribeDBInstancesPaginatorBase = AioPaginator[DBInstanceMessageTypeDef]
else:
    _DescribeDBInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBInstancesPaginator(_DescribeDBInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBInstances.html#DocDB.Paginator.DescribeDBInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbinstancespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBInstancesMessagePaginateTypeDef]
    ) -> AioPageIterator[DBInstanceMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBInstances.html#DocDB.Paginator.DescribeDBInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbinstancespaginator)
        """


if TYPE_CHECKING:
    _DescribeDBSubnetGroupsPaginatorBase = AioPaginator[DBSubnetGroupMessageTypeDef]
else:
    _DescribeDBSubnetGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBSubnetGroupsPaginator(_DescribeDBSubnetGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBSubnetGroups.html#DocDB.Paginator.DescribeDBSubnetGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbsubnetgroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBSubnetGroupsMessagePaginateTypeDef]
    ) -> AioPageIterator[DBSubnetGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBSubnetGroups.html#DocDB.Paginator.DescribeDBSubnetGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbsubnetgroupspaginator)
        """


if TYPE_CHECKING:
    _DescribeEventSubscriptionsPaginatorBase = AioPaginator[EventSubscriptionsMessageTypeDef]
else:
    _DescribeEventSubscriptionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeEventSubscriptionsPaginator(_DescribeEventSubscriptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeEventSubscriptions.html#DocDB.Paginator.DescribeEventSubscriptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describeeventsubscriptionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEventSubscriptionsMessagePaginateTypeDef]
    ) -> AioPageIterator[EventSubscriptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeEventSubscriptions.html#DocDB.Paginator.DescribeEventSubscriptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describeeventsubscriptionspaginator)
        """


if TYPE_CHECKING:
    _DescribeEventsPaginatorBase = AioPaginator[EventsMessageTypeDef]
else:
    _DescribeEventsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeEventsPaginator(_DescribeEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeEvents.html#DocDB.Paginator.DescribeEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describeeventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEventsMessagePaginateTypeDef]
    ) -> AioPageIterator[EventsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeEvents.html#DocDB.Paginator.DescribeEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describeeventspaginator)
        """


if TYPE_CHECKING:
    _DescribeGlobalClustersPaginatorBase = AioPaginator[GlobalClustersMessageTypeDef]
else:
    _DescribeGlobalClustersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeGlobalClustersPaginator(_DescribeGlobalClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeGlobalClusters.html#DocDB.Paginator.DescribeGlobalClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describeglobalclusterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeGlobalClustersMessagePaginateTypeDef]
    ) -> AioPageIterator[GlobalClustersMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeGlobalClusters.html#DocDB.Paginator.DescribeGlobalClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describeglobalclusterspaginator)
        """


if TYPE_CHECKING:
    _DescribeOrderableDBInstanceOptionsPaginatorBase = AioPaginator[
        OrderableDBInstanceOptionsMessageTypeDef
    ]
else:
    _DescribeOrderableDBInstanceOptionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeOrderableDBInstanceOptionsPaginator(_DescribeOrderableDBInstanceOptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeOrderableDBInstanceOptions.html#DocDB.Paginator.DescribeOrderableDBInstanceOptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describeorderabledbinstanceoptionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeOrderableDBInstanceOptionsMessagePaginateTypeDef]
    ) -> AioPageIterator[OrderableDBInstanceOptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeOrderableDBInstanceOptions.html#DocDB.Paginator.DescribeOrderableDBInstanceOptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describeorderabledbinstanceoptionspaginator)
        """


if TYPE_CHECKING:
    _DescribePendingMaintenanceActionsPaginatorBase = AioPaginator[
        PendingMaintenanceActionsMessageTypeDef
    ]
else:
    _DescribePendingMaintenanceActionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribePendingMaintenanceActionsPaginator(_DescribePendingMaintenanceActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribePendingMaintenanceActions.html#DocDB.Paginator.DescribePendingMaintenanceActions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describependingmaintenanceactionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribePendingMaintenanceActionsMessagePaginateTypeDef]
    ) -> AioPageIterator[PendingMaintenanceActionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribePendingMaintenanceActions.html#DocDB.Paginator.DescribePendingMaintenanceActions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describependingmaintenanceactionspaginator)
        """
