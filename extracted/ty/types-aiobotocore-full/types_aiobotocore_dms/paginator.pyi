"""
Type annotations for dms service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_dms.client import DatabaseMigrationServiceClient
    from types_aiobotocore_dms.paginator import (
        DescribeCertificatesPaginator,
        DescribeConnectionsPaginator,
        DescribeDataMigrationsPaginator,
        DescribeEndpointTypesPaginator,
        DescribeEndpointsPaginator,
        DescribeEventSubscriptionsPaginator,
        DescribeEventsPaginator,
        DescribeOrderableReplicationInstancesPaginator,
        DescribeReplicationInstancesPaginator,
        DescribeReplicationSubnetGroupsPaginator,
        DescribeReplicationTaskAssessmentResultsPaginator,
        DescribeReplicationTasksPaginator,
        DescribeSchemasPaginator,
        DescribeTableStatisticsPaginator,
    )

    session = get_session()
    with session.create_client("dms") as client:
        client: DatabaseMigrationServiceClient

        describe_certificates_paginator: DescribeCertificatesPaginator = client.get_paginator("describe_certificates")
        describe_connections_paginator: DescribeConnectionsPaginator = client.get_paginator("describe_connections")
        describe_data_migrations_paginator: DescribeDataMigrationsPaginator = client.get_paginator("describe_data_migrations")
        describe_endpoint_types_paginator: DescribeEndpointTypesPaginator = client.get_paginator("describe_endpoint_types")
        describe_endpoints_paginator: DescribeEndpointsPaginator = client.get_paginator("describe_endpoints")
        describe_event_subscriptions_paginator: DescribeEventSubscriptionsPaginator = client.get_paginator("describe_event_subscriptions")
        describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
        describe_orderable_replication_instances_paginator: DescribeOrderableReplicationInstancesPaginator = client.get_paginator("describe_orderable_replication_instances")
        describe_replication_instances_paginator: DescribeReplicationInstancesPaginator = client.get_paginator("describe_replication_instances")
        describe_replication_subnet_groups_paginator: DescribeReplicationSubnetGroupsPaginator = client.get_paginator("describe_replication_subnet_groups")
        describe_replication_task_assessment_results_paginator: DescribeReplicationTaskAssessmentResultsPaginator = client.get_paginator("describe_replication_task_assessment_results")
        describe_replication_tasks_paginator: DescribeReplicationTasksPaginator = client.get_paginator("describe_replication_tasks")
        describe_schemas_paginator: DescribeSchemasPaginator = client.get_paginator("describe_schemas")
        describe_table_statistics_paginator: DescribeTableStatisticsPaginator = client.get_paginator("describe_table_statistics")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeCertificatesMessagePaginateTypeDef,
    DescribeCertificatesResponseTypeDef,
    DescribeConnectionsMessagePaginateTypeDef,
    DescribeConnectionsResponseTypeDef,
    DescribeDataMigrationsMessagePaginateTypeDef,
    DescribeDataMigrationsResponseTypeDef,
    DescribeEndpointsMessagePaginateTypeDef,
    DescribeEndpointsResponseTypeDef,
    DescribeEndpointTypesMessagePaginateTypeDef,
    DescribeEndpointTypesResponseTypeDef,
    DescribeEventsMessagePaginateTypeDef,
    DescribeEventsResponseTypeDef,
    DescribeEventSubscriptionsMessagePaginateTypeDef,
    DescribeEventSubscriptionsResponseTypeDef,
    DescribeOrderableReplicationInstancesMessagePaginateTypeDef,
    DescribeOrderableReplicationInstancesResponseTypeDef,
    DescribeReplicationInstancesMessagePaginateTypeDef,
    DescribeReplicationInstancesResponseTypeDef,
    DescribeReplicationSubnetGroupsMessagePaginateTypeDef,
    DescribeReplicationSubnetGroupsResponseTypeDef,
    DescribeReplicationTaskAssessmentResultsMessagePaginateTypeDef,
    DescribeReplicationTaskAssessmentResultsResponseTypeDef,
    DescribeReplicationTasksMessagePaginateTypeDef,
    DescribeReplicationTasksResponseTypeDef,
    DescribeSchemasMessagePaginateTypeDef,
    DescribeSchemasResponseTypeDef,
    DescribeTableStatisticsMessagePaginateTypeDef,
    DescribeTableStatisticsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeCertificatesPaginator",
    "DescribeConnectionsPaginator",
    "DescribeDataMigrationsPaginator",
    "DescribeEndpointTypesPaginator",
    "DescribeEndpointsPaginator",
    "DescribeEventSubscriptionsPaginator",
    "DescribeEventsPaginator",
    "DescribeOrderableReplicationInstancesPaginator",
    "DescribeReplicationInstancesPaginator",
    "DescribeReplicationSubnetGroupsPaginator",
    "DescribeReplicationTaskAssessmentResultsPaginator",
    "DescribeReplicationTasksPaginator",
    "DescribeSchemasPaginator",
    "DescribeTableStatisticsPaginator",
)

if TYPE_CHECKING:
    _DescribeCertificatesPaginatorBase = AioPaginator[DescribeCertificatesResponseTypeDef]
else:
    _DescribeCertificatesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeCertificatesPaginator(_DescribeCertificatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeCertificates.html#DatabaseMigrationService.Paginator.DescribeCertificates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describecertificatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeCertificatesMessagePaginateTypeDef]
    ) -> AioPageIterator[DescribeCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeCertificates.html#DatabaseMigrationService.Paginator.DescribeCertificates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describecertificatespaginator)
        """

if TYPE_CHECKING:
    _DescribeConnectionsPaginatorBase = AioPaginator[DescribeConnectionsResponseTypeDef]
else:
    _DescribeConnectionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeConnectionsPaginator(_DescribeConnectionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeConnections.html#DatabaseMigrationService.Paginator.DescribeConnections)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describeconnectionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeConnectionsMessagePaginateTypeDef]
    ) -> AioPageIterator[DescribeConnectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeConnections.html#DatabaseMigrationService.Paginator.DescribeConnections.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describeconnectionspaginator)
        """

if TYPE_CHECKING:
    _DescribeDataMigrationsPaginatorBase = AioPaginator[DescribeDataMigrationsResponseTypeDef]
else:
    _DescribeDataMigrationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeDataMigrationsPaginator(_DescribeDataMigrationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeDataMigrations.html#DatabaseMigrationService.Paginator.DescribeDataMigrations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describedatamigrationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDataMigrationsMessagePaginateTypeDef]
    ) -> AioPageIterator[DescribeDataMigrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeDataMigrations.html#DatabaseMigrationService.Paginator.DescribeDataMigrations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describedatamigrationspaginator)
        """

if TYPE_CHECKING:
    _DescribeEndpointTypesPaginatorBase = AioPaginator[DescribeEndpointTypesResponseTypeDef]
else:
    _DescribeEndpointTypesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeEndpointTypesPaginator(_DescribeEndpointTypesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeEndpointTypes.html#DatabaseMigrationService.Paginator.DescribeEndpointTypes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describeendpointtypespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEndpointTypesMessagePaginateTypeDef]
    ) -> AioPageIterator[DescribeEndpointTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeEndpointTypes.html#DatabaseMigrationService.Paginator.DescribeEndpointTypes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describeendpointtypespaginator)
        """

if TYPE_CHECKING:
    _DescribeEndpointsPaginatorBase = AioPaginator[DescribeEndpointsResponseTypeDef]
else:
    _DescribeEndpointsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeEndpointsPaginator(_DescribeEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeEndpoints.html#DatabaseMigrationService.Paginator.DescribeEndpoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describeendpointspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEndpointsMessagePaginateTypeDef]
    ) -> AioPageIterator[DescribeEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeEndpoints.html#DatabaseMigrationService.Paginator.DescribeEndpoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describeendpointspaginator)
        """

if TYPE_CHECKING:
    _DescribeEventSubscriptionsPaginatorBase = AioPaginator[
        DescribeEventSubscriptionsResponseTypeDef
    ]
else:
    _DescribeEventSubscriptionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeEventSubscriptionsPaginator(_DescribeEventSubscriptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeEventSubscriptions.html#DatabaseMigrationService.Paginator.DescribeEventSubscriptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describeeventsubscriptionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEventSubscriptionsMessagePaginateTypeDef]
    ) -> AioPageIterator[DescribeEventSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeEventSubscriptions.html#DatabaseMigrationService.Paginator.DescribeEventSubscriptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describeeventsubscriptionspaginator)
        """

if TYPE_CHECKING:
    _DescribeEventsPaginatorBase = AioPaginator[DescribeEventsResponseTypeDef]
else:
    _DescribeEventsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeEventsPaginator(_DescribeEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeEvents.html#DatabaseMigrationService.Paginator.DescribeEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describeeventspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEventsMessagePaginateTypeDef]
    ) -> AioPageIterator[DescribeEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeEvents.html#DatabaseMigrationService.Paginator.DescribeEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describeeventspaginator)
        """

if TYPE_CHECKING:
    _DescribeOrderableReplicationInstancesPaginatorBase = AioPaginator[
        DescribeOrderableReplicationInstancesResponseTypeDef
    ]
else:
    _DescribeOrderableReplicationInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeOrderableReplicationInstancesPaginator(
    _DescribeOrderableReplicationInstancesPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeOrderableReplicationInstances.html#DatabaseMigrationService.Paginator.DescribeOrderableReplicationInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describeorderablereplicationinstancespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeOrderableReplicationInstancesMessagePaginateTypeDef]
    ) -> AioPageIterator[DescribeOrderableReplicationInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeOrderableReplicationInstances.html#DatabaseMigrationService.Paginator.DescribeOrderableReplicationInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describeorderablereplicationinstancespaginator)
        """

if TYPE_CHECKING:
    _DescribeReplicationInstancesPaginatorBase = AioPaginator[
        DescribeReplicationInstancesResponseTypeDef
    ]
else:
    _DescribeReplicationInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeReplicationInstancesPaginator(_DescribeReplicationInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeReplicationInstances.html#DatabaseMigrationService.Paginator.DescribeReplicationInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describereplicationinstancespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReplicationInstancesMessagePaginateTypeDef]
    ) -> AioPageIterator[DescribeReplicationInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeReplicationInstances.html#DatabaseMigrationService.Paginator.DescribeReplicationInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describereplicationinstancespaginator)
        """

if TYPE_CHECKING:
    _DescribeReplicationSubnetGroupsPaginatorBase = AioPaginator[
        DescribeReplicationSubnetGroupsResponseTypeDef
    ]
else:
    _DescribeReplicationSubnetGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeReplicationSubnetGroupsPaginator(_DescribeReplicationSubnetGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeReplicationSubnetGroups.html#DatabaseMigrationService.Paginator.DescribeReplicationSubnetGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describereplicationsubnetgroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReplicationSubnetGroupsMessagePaginateTypeDef]
    ) -> AioPageIterator[DescribeReplicationSubnetGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeReplicationSubnetGroups.html#DatabaseMigrationService.Paginator.DescribeReplicationSubnetGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describereplicationsubnetgroupspaginator)
        """

if TYPE_CHECKING:
    _DescribeReplicationTaskAssessmentResultsPaginatorBase = AioPaginator[
        DescribeReplicationTaskAssessmentResultsResponseTypeDef
    ]
else:
    _DescribeReplicationTaskAssessmentResultsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeReplicationTaskAssessmentResultsPaginator(
    _DescribeReplicationTaskAssessmentResultsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeReplicationTaskAssessmentResults.html#DatabaseMigrationService.Paginator.DescribeReplicationTaskAssessmentResults)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describereplicationtaskassessmentresultspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReplicationTaskAssessmentResultsMessagePaginateTypeDef]
    ) -> AioPageIterator[DescribeReplicationTaskAssessmentResultsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeReplicationTaskAssessmentResults.html#DatabaseMigrationService.Paginator.DescribeReplicationTaskAssessmentResults.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describereplicationtaskassessmentresultspaginator)
        """

if TYPE_CHECKING:
    _DescribeReplicationTasksPaginatorBase = AioPaginator[DescribeReplicationTasksResponseTypeDef]
else:
    _DescribeReplicationTasksPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeReplicationTasksPaginator(_DescribeReplicationTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeReplicationTasks.html#DatabaseMigrationService.Paginator.DescribeReplicationTasks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describereplicationtaskspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReplicationTasksMessagePaginateTypeDef]
    ) -> AioPageIterator[DescribeReplicationTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeReplicationTasks.html#DatabaseMigrationService.Paginator.DescribeReplicationTasks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describereplicationtaskspaginator)
        """

if TYPE_CHECKING:
    _DescribeSchemasPaginatorBase = AioPaginator[DescribeSchemasResponseTypeDef]
else:
    _DescribeSchemasPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeSchemasPaginator(_DescribeSchemasPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeSchemas.html#DatabaseMigrationService.Paginator.DescribeSchemas)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describeschemaspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSchemasMessagePaginateTypeDef]
    ) -> AioPageIterator[DescribeSchemasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeSchemas.html#DatabaseMigrationService.Paginator.DescribeSchemas.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describeschemaspaginator)
        """

if TYPE_CHECKING:
    _DescribeTableStatisticsPaginatorBase = AioPaginator[DescribeTableStatisticsResponseTypeDef]
else:
    _DescribeTableStatisticsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeTableStatisticsPaginator(_DescribeTableStatisticsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeTableStatistics.html#DatabaseMigrationService.Paginator.DescribeTableStatistics)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describetablestatisticspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeTableStatisticsMessagePaginateTypeDef]
    ) -> AioPageIterator[DescribeTableStatisticsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/paginator/DescribeTableStatistics.html#DatabaseMigrationService.Paginator.DescribeTableStatistics.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/paginators/#describetablestatisticspaginator)
        """
