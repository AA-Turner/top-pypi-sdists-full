"""
Type annotations for rds service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_rds.client import RDSClient
    from types_aiobotocore_rds.paginator import (
        DescribeBlueGreenDeploymentsPaginator,
        DescribeCertificatesPaginator,
        DescribeDBClusterAutomatedBackupsPaginator,
        DescribeDBClusterBacktracksPaginator,
        DescribeDBClusterEndpointsPaginator,
        DescribeDBClusterParameterGroupsPaginator,
        DescribeDBClusterParametersPaginator,
        DescribeDBClusterSnapshotsPaginator,
        DescribeDBClustersPaginator,
        DescribeDBEngineVersionsPaginator,
        DescribeDBInstanceAutomatedBackupsPaginator,
        DescribeDBInstancesPaginator,
        DescribeDBLogFilesPaginator,
        DescribeDBMajorEngineVersionsPaginator,
        DescribeDBParameterGroupsPaginator,
        DescribeDBParametersPaginator,
        DescribeDBProxiesPaginator,
        DescribeDBProxyEndpointsPaginator,
        DescribeDBProxyTargetGroupsPaginator,
        DescribeDBProxyTargetsPaginator,
        DescribeDBRecommendationsPaginator,
        DescribeDBSecurityGroupsPaginator,
        DescribeDBSnapshotTenantDatabasesPaginator,
        DescribeDBSnapshotsPaginator,
        DescribeDBSubnetGroupsPaginator,
        DescribeEngineDefaultClusterParametersPaginator,
        DescribeEngineDefaultParametersPaginator,
        DescribeEventSubscriptionsPaginator,
        DescribeEventsPaginator,
        DescribeExportTasksPaginator,
        DescribeGlobalClustersPaginator,
        DescribeIntegrationsPaginator,
        DescribeOptionGroupOptionsPaginator,
        DescribeOptionGroupsPaginator,
        DescribeOrderableDBInstanceOptionsPaginator,
        DescribePendingMaintenanceActionsPaginator,
        DescribeReservedDBInstancesOfferingsPaginator,
        DescribeReservedDBInstancesPaginator,
        DescribeSourceRegionsPaginator,
        DescribeTenantDatabasesPaginator,
        DownloadDBLogFilePortionPaginator,
    )

    session = get_session()
    with session.create_client("rds") as client:
        client: RDSClient

        describe_blue_green_deployments_paginator: DescribeBlueGreenDeploymentsPaginator = client.get_paginator("describe_blue_green_deployments")
        describe_certificates_paginator: DescribeCertificatesPaginator = client.get_paginator("describe_certificates")
        describe_db_cluster_automated_backups_paginator: DescribeDBClusterAutomatedBackupsPaginator = client.get_paginator("describe_db_cluster_automated_backups")
        describe_db_cluster_backtracks_paginator: DescribeDBClusterBacktracksPaginator = client.get_paginator("describe_db_cluster_backtracks")
        describe_db_cluster_endpoints_paginator: DescribeDBClusterEndpointsPaginator = client.get_paginator("describe_db_cluster_endpoints")
        describe_db_cluster_parameter_groups_paginator: DescribeDBClusterParameterGroupsPaginator = client.get_paginator("describe_db_cluster_parameter_groups")
        describe_db_cluster_parameters_paginator: DescribeDBClusterParametersPaginator = client.get_paginator("describe_db_cluster_parameters")
        describe_db_cluster_snapshots_paginator: DescribeDBClusterSnapshotsPaginator = client.get_paginator("describe_db_cluster_snapshots")
        describe_db_clusters_paginator: DescribeDBClustersPaginator = client.get_paginator("describe_db_clusters")
        describe_db_engine_versions_paginator: DescribeDBEngineVersionsPaginator = client.get_paginator("describe_db_engine_versions")
        describe_db_instance_automated_backups_paginator: DescribeDBInstanceAutomatedBackupsPaginator = client.get_paginator("describe_db_instance_automated_backups")
        describe_db_instances_paginator: DescribeDBInstancesPaginator = client.get_paginator("describe_db_instances")
        describe_db_log_files_paginator: DescribeDBLogFilesPaginator = client.get_paginator("describe_db_log_files")
        describe_db_major_engine_versions_paginator: DescribeDBMajorEngineVersionsPaginator = client.get_paginator("describe_db_major_engine_versions")
        describe_db_parameter_groups_paginator: DescribeDBParameterGroupsPaginator = client.get_paginator("describe_db_parameter_groups")
        describe_db_parameters_paginator: DescribeDBParametersPaginator = client.get_paginator("describe_db_parameters")
        describe_db_proxies_paginator: DescribeDBProxiesPaginator = client.get_paginator("describe_db_proxies")
        describe_db_proxy_endpoints_paginator: DescribeDBProxyEndpointsPaginator = client.get_paginator("describe_db_proxy_endpoints")
        describe_db_proxy_target_groups_paginator: DescribeDBProxyTargetGroupsPaginator = client.get_paginator("describe_db_proxy_target_groups")
        describe_db_proxy_targets_paginator: DescribeDBProxyTargetsPaginator = client.get_paginator("describe_db_proxy_targets")
        describe_db_recommendations_paginator: DescribeDBRecommendationsPaginator = client.get_paginator("describe_db_recommendations")
        describe_db_security_groups_paginator: DescribeDBSecurityGroupsPaginator = client.get_paginator("describe_db_security_groups")
        describe_db_snapshot_tenant_databases_paginator: DescribeDBSnapshotTenantDatabasesPaginator = client.get_paginator("describe_db_snapshot_tenant_databases")
        describe_db_snapshots_paginator: DescribeDBSnapshotsPaginator = client.get_paginator("describe_db_snapshots")
        describe_db_subnet_groups_paginator: DescribeDBSubnetGroupsPaginator = client.get_paginator("describe_db_subnet_groups")
        describe_engine_default_cluster_parameters_paginator: DescribeEngineDefaultClusterParametersPaginator = client.get_paginator("describe_engine_default_cluster_parameters")
        describe_engine_default_parameters_paginator: DescribeEngineDefaultParametersPaginator = client.get_paginator("describe_engine_default_parameters")
        describe_event_subscriptions_paginator: DescribeEventSubscriptionsPaginator = client.get_paginator("describe_event_subscriptions")
        describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
        describe_export_tasks_paginator: DescribeExportTasksPaginator = client.get_paginator("describe_export_tasks")
        describe_global_clusters_paginator: DescribeGlobalClustersPaginator = client.get_paginator("describe_global_clusters")
        describe_integrations_paginator: DescribeIntegrationsPaginator = client.get_paginator("describe_integrations")
        describe_option_group_options_paginator: DescribeOptionGroupOptionsPaginator = client.get_paginator("describe_option_group_options")
        describe_option_groups_paginator: DescribeOptionGroupsPaginator = client.get_paginator("describe_option_groups")
        describe_orderable_db_instance_options_paginator: DescribeOrderableDBInstanceOptionsPaginator = client.get_paginator("describe_orderable_db_instance_options")
        describe_pending_maintenance_actions_paginator: DescribePendingMaintenanceActionsPaginator = client.get_paginator("describe_pending_maintenance_actions")
        describe_reserved_db_instances_offerings_paginator: DescribeReservedDBInstancesOfferingsPaginator = client.get_paginator("describe_reserved_db_instances_offerings")
        describe_reserved_db_instances_paginator: DescribeReservedDBInstancesPaginator = client.get_paginator("describe_reserved_db_instances")
        describe_source_regions_paginator: DescribeSourceRegionsPaginator = client.get_paginator("describe_source_regions")
        describe_tenant_databases_paginator: DescribeTenantDatabasesPaginator = client.get_paginator("describe_tenant_databases")
        download_db_log_file_portion_paginator: DownloadDBLogFilePortionPaginator = client.get_paginator("download_db_log_file_portion")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    CertificateMessageTypeDef,
    DBClusterAutomatedBackupMessageTypeDef,
    DBClusterBacktrackMessageTypeDef,
    DBClusterEndpointMessageTypeDef,
    DBClusterMessageTypeDef,
    DBClusterParameterGroupDetailsTypeDef,
    DBClusterParameterGroupsMessageTypeDef,
    DBClusterSnapshotMessageTypeDef,
    DBEngineVersionMessageTypeDef,
    DBInstanceAutomatedBackupMessageTypeDef,
    DBInstanceMessageTypeDef,
    DBParameterGroupDetailsTypeDef,
    DBParameterGroupsMessageTypeDef,
    DBRecommendationsMessageTypeDef,
    DBSecurityGroupMessageTypeDef,
    DBSnapshotMessageTypeDef,
    DBSnapshotTenantDatabasesMessageTypeDef,
    DBSubnetGroupMessageTypeDef,
    DescribeBlueGreenDeploymentsRequestPaginateTypeDef,
    DescribeBlueGreenDeploymentsResponseTypeDef,
    DescribeCertificatesMessagePaginateTypeDef,
    DescribeDBClusterAutomatedBackupsMessagePaginateTypeDef,
    DescribeDBClusterBacktracksMessagePaginateTypeDef,
    DescribeDBClusterEndpointsMessagePaginateTypeDef,
    DescribeDBClusterParameterGroupsMessagePaginateTypeDef,
    DescribeDBClusterParametersMessagePaginateTypeDef,
    DescribeDBClustersMessagePaginateTypeDef,
    DescribeDBClusterSnapshotsMessagePaginateTypeDef,
    DescribeDBEngineVersionsMessagePaginateTypeDef,
    DescribeDBInstanceAutomatedBackupsMessagePaginateTypeDef,
    DescribeDBInstancesMessagePaginateTypeDef,
    DescribeDBLogFilesMessagePaginateTypeDef,
    DescribeDBLogFilesResponseTypeDef,
    DescribeDBMajorEngineVersionsRequestPaginateTypeDef,
    DescribeDBMajorEngineVersionsResponseTypeDef,
    DescribeDBParameterGroupsMessagePaginateTypeDef,
    DescribeDBParametersMessagePaginateTypeDef,
    DescribeDBProxiesRequestPaginateTypeDef,
    DescribeDBProxiesResponseTypeDef,
    DescribeDBProxyEndpointsRequestPaginateTypeDef,
    DescribeDBProxyEndpointsResponseTypeDef,
    DescribeDBProxyTargetGroupsRequestPaginateTypeDef,
    DescribeDBProxyTargetGroupsResponseTypeDef,
    DescribeDBProxyTargetsRequestPaginateTypeDef,
    DescribeDBProxyTargetsResponseTypeDef,
    DescribeDBRecommendationsMessagePaginateTypeDef,
    DescribeDBSecurityGroupsMessagePaginateTypeDef,
    DescribeDBSnapshotsMessagePaginateTypeDef,
    DescribeDBSnapshotTenantDatabasesMessagePaginateTypeDef,
    DescribeDBSubnetGroupsMessagePaginateTypeDef,
    DescribeEngineDefaultClusterParametersMessagePaginateTypeDef,
    DescribeEngineDefaultClusterParametersResultTypeDef,
    DescribeEngineDefaultParametersMessagePaginateTypeDef,
    DescribeEngineDefaultParametersResultTypeDef,
    DescribeEventsMessagePaginateTypeDef,
    DescribeEventSubscriptionsMessagePaginateTypeDef,
    DescribeExportTasksMessagePaginateTypeDef,
    DescribeGlobalClustersMessagePaginateTypeDef,
    DescribeIntegrationsMessagePaginateTypeDef,
    DescribeIntegrationsResponseTypeDef,
    DescribeOptionGroupOptionsMessagePaginateTypeDef,
    DescribeOptionGroupsMessagePaginateTypeDef,
    DescribeOrderableDBInstanceOptionsMessagePaginateTypeDef,
    DescribePendingMaintenanceActionsMessagePaginateTypeDef,
    DescribeReservedDBInstancesMessagePaginateTypeDef,
    DescribeReservedDBInstancesOfferingsMessagePaginateTypeDef,
    DescribeSourceRegionsMessagePaginateTypeDef,
    DescribeTenantDatabasesMessagePaginateTypeDef,
    DownloadDBLogFilePortionDetailsTypeDef,
    DownloadDBLogFilePortionMessagePaginateTypeDef,
    EventsMessageTypeDef,
    EventSubscriptionsMessageTypeDef,
    ExportTasksMessageTypeDef,
    GlobalClustersMessageTypeDef,
    OptionGroupOptionsMessageTypeDef,
    OptionGroupsTypeDef,
    OrderableDBInstanceOptionsMessageTypeDef,
    PendingMaintenanceActionsMessageTypeDef,
    ReservedDBInstanceMessageTypeDef,
    ReservedDBInstancesOfferingMessageTypeDef,
    SourceRegionMessageTypeDef,
    TenantDatabasesMessageTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeBlueGreenDeploymentsPaginator",
    "DescribeCertificatesPaginator",
    "DescribeDBClusterAutomatedBackupsPaginator",
    "DescribeDBClusterBacktracksPaginator",
    "DescribeDBClusterEndpointsPaginator",
    "DescribeDBClusterParameterGroupsPaginator",
    "DescribeDBClusterParametersPaginator",
    "DescribeDBClusterSnapshotsPaginator",
    "DescribeDBClustersPaginator",
    "DescribeDBEngineVersionsPaginator",
    "DescribeDBInstanceAutomatedBackupsPaginator",
    "DescribeDBInstancesPaginator",
    "DescribeDBLogFilesPaginator",
    "DescribeDBMajorEngineVersionsPaginator",
    "DescribeDBParameterGroupsPaginator",
    "DescribeDBParametersPaginator",
    "DescribeDBProxiesPaginator",
    "DescribeDBProxyEndpointsPaginator",
    "DescribeDBProxyTargetGroupsPaginator",
    "DescribeDBProxyTargetsPaginator",
    "DescribeDBRecommendationsPaginator",
    "DescribeDBSecurityGroupsPaginator",
    "DescribeDBSnapshotTenantDatabasesPaginator",
    "DescribeDBSnapshotsPaginator",
    "DescribeDBSubnetGroupsPaginator",
    "DescribeEngineDefaultClusterParametersPaginator",
    "DescribeEngineDefaultParametersPaginator",
    "DescribeEventSubscriptionsPaginator",
    "DescribeEventsPaginator",
    "DescribeExportTasksPaginator",
    "DescribeGlobalClustersPaginator",
    "DescribeIntegrationsPaginator",
    "DescribeOptionGroupOptionsPaginator",
    "DescribeOptionGroupsPaginator",
    "DescribeOrderableDBInstanceOptionsPaginator",
    "DescribePendingMaintenanceActionsPaginator",
    "DescribeReservedDBInstancesOfferingsPaginator",
    "DescribeReservedDBInstancesPaginator",
    "DescribeSourceRegionsPaginator",
    "DescribeTenantDatabasesPaginator",
    "DownloadDBLogFilePortionPaginator",
)


if TYPE_CHECKING:
    _DescribeBlueGreenDeploymentsPaginatorBase = AioPaginator[
        DescribeBlueGreenDeploymentsResponseTypeDef
    ]
else:
    _DescribeBlueGreenDeploymentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeBlueGreenDeploymentsPaginator(_DescribeBlueGreenDeploymentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeBlueGreenDeployments.html#RDS.Paginator.DescribeBlueGreenDeployments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describebluegreendeploymentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeBlueGreenDeploymentsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeBlueGreenDeploymentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeBlueGreenDeployments.html#RDS.Paginator.DescribeBlueGreenDeployments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describebluegreendeploymentspaginator)
        """


if TYPE_CHECKING:
    _DescribeCertificatesPaginatorBase = AioPaginator[CertificateMessageTypeDef]
else:
    _DescribeCertificatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeCertificatesPaginator(_DescribeCertificatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeCertificates.html#RDS.Paginator.DescribeCertificates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describecertificatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeCertificatesMessagePaginateTypeDef]
    ) -> AioPageIterator[CertificateMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeCertificates.html#RDS.Paginator.DescribeCertificates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describecertificatespaginator)
        """


if TYPE_CHECKING:
    _DescribeDBClusterAutomatedBackupsPaginatorBase = AioPaginator[
        DBClusterAutomatedBackupMessageTypeDef
    ]
else:
    _DescribeDBClusterAutomatedBackupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBClusterAutomatedBackupsPaginator(_DescribeDBClusterAutomatedBackupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBClusterAutomatedBackups.html#RDS.Paginator.DescribeDBClusterAutomatedBackups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclusterautomatedbackupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBClusterAutomatedBackupsMessagePaginateTypeDef]
    ) -> AioPageIterator[DBClusterAutomatedBackupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBClusterAutomatedBackups.html#RDS.Paginator.DescribeDBClusterAutomatedBackups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclusterautomatedbackupspaginator)
        """


if TYPE_CHECKING:
    _DescribeDBClusterBacktracksPaginatorBase = AioPaginator[DBClusterBacktrackMessageTypeDef]
else:
    _DescribeDBClusterBacktracksPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBClusterBacktracksPaginator(_DescribeDBClusterBacktracksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBClusterBacktracks.html#RDS.Paginator.DescribeDBClusterBacktracks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclusterbacktrackspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBClusterBacktracksMessagePaginateTypeDef]
    ) -> AioPageIterator[DBClusterBacktrackMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBClusterBacktracks.html#RDS.Paginator.DescribeDBClusterBacktracks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclusterbacktrackspaginator)
        """


if TYPE_CHECKING:
    _DescribeDBClusterEndpointsPaginatorBase = AioPaginator[DBClusterEndpointMessageTypeDef]
else:
    _DescribeDBClusterEndpointsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBClusterEndpointsPaginator(_DescribeDBClusterEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBClusterEndpoints.html#RDS.Paginator.DescribeDBClusterEndpoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclusterendpointspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBClusterEndpointsMessagePaginateTypeDef]
    ) -> AioPageIterator[DBClusterEndpointMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBClusterEndpoints.html#RDS.Paginator.DescribeDBClusterEndpoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclusterendpointspaginator)
        """


if TYPE_CHECKING:
    _DescribeDBClusterParameterGroupsPaginatorBase = AioPaginator[
        DBClusterParameterGroupsMessageTypeDef
    ]
else:
    _DescribeDBClusterParameterGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBClusterParameterGroupsPaginator(_DescribeDBClusterParameterGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBClusterParameterGroups.html#RDS.Paginator.DescribeDBClusterParameterGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclusterparametergroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBClusterParameterGroupsMessagePaginateTypeDef]
    ) -> AioPageIterator[DBClusterParameterGroupsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBClusterParameterGroups.html#RDS.Paginator.DescribeDBClusterParameterGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclusterparametergroupspaginator)
        """


if TYPE_CHECKING:
    _DescribeDBClusterParametersPaginatorBase = AioPaginator[DBClusterParameterGroupDetailsTypeDef]
else:
    _DescribeDBClusterParametersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBClusterParametersPaginator(_DescribeDBClusterParametersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBClusterParameters.html#RDS.Paginator.DescribeDBClusterParameters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclusterparameterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBClusterParametersMessagePaginateTypeDef]
    ) -> AioPageIterator[DBClusterParameterGroupDetailsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBClusterParameters.html#RDS.Paginator.DescribeDBClusterParameters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclusterparameterspaginator)
        """


if TYPE_CHECKING:
    _DescribeDBClusterSnapshotsPaginatorBase = AioPaginator[DBClusterSnapshotMessageTypeDef]
else:
    _DescribeDBClusterSnapshotsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBClusterSnapshotsPaginator(_DescribeDBClusterSnapshotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBClusterSnapshots.html#RDS.Paginator.DescribeDBClusterSnapshots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclustersnapshotspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBClusterSnapshotsMessagePaginateTypeDef]
    ) -> AioPageIterator[DBClusterSnapshotMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBClusterSnapshots.html#RDS.Paginator.DescribeDBClusterSnapshots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclustersnapshotspaginator)
        """


if TYPE_CHECKING:
    _DescribeDBClustersPaginatorBase = AioPaginator[DBClusterMessageTypeDef]
else:
    _DescribeDBClustersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBClustersPaginator(_DescribeDBClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBClusters.html#RDS.Paginator.DescribeDBClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclusterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBClustersMessagePaginateTypeDef]
    ) -> AioPageIterator[DBClusterMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBClusters.html#RDS.Paginator.DescribeDBClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclusterspaginator)
        """


if TYPE_CHECKING:
    _DescribeDBEngineVersionsPaginatorBase = AioPaginator[DBEngineVersionMessageTypeDef]
else:
    _DescribeDBEngineVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBEngineVersionsPaginator(_DescribeDBEngineVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBEngineVersions.html#RDS.Paginator.DescribeDBEngineVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbengineversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBEngineVersionsMessagePaginateTypeDef]
    ) -> AioPageIterator[DBEngineVersionMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBEngineVersions.html#RDS.Paginator.DescribeDBEngineVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbengineversionspaginator)
        """


if TYPE_CHECKING:
    _DescribeDBInstanceAutomatedBackupsPaginatorBase = AioPaginator[
        DBInstanceAutomatedBackupMessageTypeDef
    ]
else:
    _DescribeDBInstanceAutomatedBackupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBInstanceAutomatedBackupsPaginator(_DescribeDBInstanceAutomatedBackupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBInstanceAutomatedBackups.html#RDS.Paginator.DescribeDBInstanceAutomatedBackups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbinstanceautomatedbackupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBInstanceAutomatedBackupsMessagePaginateTypeDef]
    ) -> AioPageIterator[DBInstanceAutomatedBackupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBInstanceAutomatedBackups.html#RDS.Paginator.DescribeDBInstanceAutomatedBackups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbinstanceautomatedbackupspaginator)
        """


if TYPE_CHECKING:
    _DescribeDBInstancesPaginatorBase = AioPaginator[DBInstanceMessageTypeDef]
else:
    _DescribeDBInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBInstancesPaginator(_DescribeDBInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBInstances.html#RDS.Paginator.DescribeDBInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbinstancespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBInstancesMessagePaginateTypeDef]
    ) -> AioPageIterator[DBInstanceMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBInstances.html#RDS.Paginator.DescribeDBInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbinstancespaginator)
        """


if TYPE_CHECKING:
    _DescribeDBLogFilesPaginatorBase = AioPaginator[DescribeDBLogFilesResponseTypeDef]
else:
    _DescribeDBLogFilesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBLogFilesPaginator(_DescribeDBLogFilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBLogFiles.html#RDS.Paginator.DescribeDBLogFiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedblogfilespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBLogFilesMessagePaginateTypeDef]
    ) -> AioPageIterator[DescribeDBLogFilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBLogFiles.html#RDS.Paginator.DescribeDBLogFiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedblogfilespaginator)
        """


if TYPE_CHECKING:
    _DescribeDBMajorEngineVersionsPaginatorBase = AioPaginator[
        DescribeDBMajorEngineVersionsResponseTypeDef
    ]
else:
    _DescribeDBMajorEngineVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBMajorEngineVersionsPaginator(_DescribeDBMajorEngineVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBMajorEngineVersions.html#RDS.Paginator.DescribeDBMajorEngineVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbmajorengineversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBMajorEngineVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeDBMajorEngineVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBMajorEngineVersions.html#RDS.Paginator.DescribeDBMajorEngineVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbmajorengineversionspaginator)
        """


if TYPE_CHECKING:
    _DescribeDBParameterGroupsPaginatorBase = AioPaginator[DBParameterGroupsMessageTypeDef]
else:
    _DescribeDBParameterGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBParameterGroupsPaginator(_DescribeDBParameterGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBParameterGroups.html#RDS.Paginator.DescribeDBParameterGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbparametergroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBParameterGroupsMessagePaginateTypeDef]
    ) -> AioPageIterator[DBParameterGroupsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBParameterGroups.html#RDS.Paginator.DescribeDBParameterGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbparametergroupspaginator)
        """


if TYPE_CHECKING:
    _DescribeDBParametersPaginatorBase = AioPaginator[DBParameterGroupDetailsTypeDef]
else:
    _DescribeDBParametersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBParametersPaginator(_DescribeDBParametersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBParameters.html#RDS.Paginator.DescribeDBParameters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbparameterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBParametersMessagePaginateTypeDef]
    ) -> AioPageIterator[DBParameterGroupDetailsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBParameters.html#RDS.Paginator.DescribeDBParameters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbparameterspaginator)
        """


if TYPE_CHECKING:
    _DescribeDBProxiesPaginatorBase = AioPaginator[DescribeDBProxiesResponseTypeDef]
else:
    _DescribeDBProxiesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBProxiesPaginator(_DescribeDBProxiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBProxies.html#RDS.Paginator.DescribeDBProxies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbproxiespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBProxiesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeDBProxiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBProxies.html#RDS.Paginator.DescribeDBProxies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbproxiespaginator)
        """


if TYPE_CHECKING:
    _DescribeDBProxyEndpointsPaginatorBase = AioPaginator[DescribeDBProxyEndpointsResponseTypeDef]
else:
    _DescribeDBProxyEndpointsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBProxyEndpointsPaginator(_DescribeDBProxyEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBProxyEndpoints.html#RDS.Paginator.DescribeDBProxyEndpoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbproxyendpointspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBProxyEndpointsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeDBProxyEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBProxyEndpoints.html#RDS.Paginator.DescribeDBProxyEndpoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbproxyendpointspaginator)
        """


if TYPE_CHECKING:
    _DescribeDBProxyTargetGroupsPaginatorBase = AioPaginator[
        DescribeDBProxyTargetGroupsResponseTypeDef
    ]
else:
    _DescribeDBProxyTargetGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBProxyTargetGroupsPaginator(_DescribeDBProxyTargetGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBProxyTargetGroups.html#RDS.Paginator.DescribeDBProxyTargetGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbproxytargetgroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBProxyTargetGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeDBProxyTargetGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBProxyTargetGroups.html#RDS.Paginator.DescribeDBProxyTargetGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbproxytargetgroupspaginator)
        """


if TYPE_CHECKING:
    _DescribeDBProxyTargetsPaginatorBase = AioPaginator[DescribeDBProxyTargetsResponseTypeDef]
else:
    _DescribeDBProxyTargetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBProxyTargetsPaginator(_DescribeDBProxyTargetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBProxyTargets.html#RDS.Paginator.DescribeDBProxyTargets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbproxytargetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBProxyTargetsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeDBProxyTargetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBProxyTargets.html#RDS.Paginator.DescribeDBProxyTargets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbproxytargetspaginator)
        """


if TYPE_CHECKING:
    _DescribeDBRecommendationsPaginatorBase = AioPaginator[DBRecommendationsMessageTypeDef]
else:
    _DescribeDBRecommendationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBRecommendationsPaginator(_DescribeDBRecommendationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBRecommendations.html#RDS.Paginator.DescribeDBRecommendations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbrecommendationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBRecommendationsMessagePaginateTypeDef]
    ) -> AioPageIterator[DBRecommendationsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBRecommendations.html#RDS.Paginator.DescribeDBRecommendations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbrecommendationspaginator)
        """


if TYPE_CHECKING:
    _DescribeDBSecurityGroupsPaginatorBase = AioPaginator[DBSecurityGroupMessageTypeDef]
else:
    _DescribeDBSecurityGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBSecurityGroupsPaginator(_DescribeDBSecurityGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBSecurityGroups.html#RDS.Paginator.DescribeDBSecurityGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbsecuritygroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBSecurityGroupsMessagePaginateTypeDef]
    ) -> AioPageIterator[DBSecurityGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBSecurityGroups.html#RDS.Paginator.DescribeDBSecurityGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbsecuritygroupspaginator)
        """


if TYPE_CHECKING:
    _DescribeDBSnapshotTenantDatabasesPaginatorBase = AioPaginator[
        DBSnapshotTenantDatabasesMessageTypeDef
    ]
else:
    _DescribeDBSnapshotTenantDatabasesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBSnapshotTenantDatabasesPaginator(_DescribeDBSnapshotTenantDatabasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBSnapshotTenantDatabases.html#RDS.Paginator.DescribeDBSnapshotTenantDatabases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbsnapshottenantdatabasespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBSnapshotTenantDatabasesMessagePaginateTypeDef]
    ) -> AioPageIterator[DBSnapshotTenantDatabasesMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBSnapshotTenantDatabases.html#RDS.Paginator.DescribeDBSnapshotTenantDatabases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbsnapshottenantdatabasespaginator)
        """


if TYPE_CHECKING:
    _DescribeDBSnapshotsPaginatorBase = AioPaginator[DBSnapshotMessageTypeDef]
else:
    _DescribeDBSnapshotsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBSnapshotsPaginator(_DescribeDBSnapshotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBSnapshots.html#RDS.Paginator.DescribeDBSnapshots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbsnapshotspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBSnapshotsMessagePaginateTypeDef]
    ) -> AioPageIterator[DBSnapshotMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBSnapshots.html#RDS.Paginator.DescribeDBSnapshots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbsnapshotspaginator)
        """


if TYPE_CHECKING:
    _DescribeDBSubnetGroupsPaginatorBase = AioPaginator[DBSubnetGroupMessageTypeDef]
else:
    _DescribeDBSubnetGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDBSubnetGroupsPaginator(_DescribeDBSubnetGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBSubnetGroups.html#RDS.Paginator.DescribeDBSubnetGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbsubnetgroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDBSubnetGroupsMessagePaginateTypeDef]
    ) -> AioPageIterator[DBSubnetGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeDBSubnetGroups.html#RDS.Paginator.DescribeDBSubnetGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbsubnetgroupspaginator)
        """


if TYPE_CHECKING:
    _DescribeEngineDefaultClusterParametersPaginatorBase = AioPaginator[
        DescribeEngineDefaultClusterParametersResultTypeDef
    ]
else:
    _DescribeEngineDefaultClusterParametersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeEngineDefaultClusterParametersPaginator(
    _DescribeEngineDefaultClusterParametersPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeEngineDefaultClusterParameters.html#RDS.Paginator.DescribeEngineDefaultClusterParameters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeenginedefaultclusterparameterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEngineDefaultClusterParametersMessagePaginateTypeDef]
    ) -> AioPageIterator[DescribeEngineDefaultClusterParametersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeEngineDefaultClusterParameters.html#RDS.Paginator.DescribeEngineDefaultClusterParameters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeenginedefaultclusterparameterspaginator)
        """


if TYPE_CHECKING:
    _DescribeEngineDefaultParametersPaginatorBase = AioPaginator[
        DescribeEngineDefaultParametersResultTypeDef
    ]
else:
    _DescribeEngineDefaultParametersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeEngineDefaultParametersPaginator(_DescribeEngineDefaultParametersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeEngineDefaultParameters.html#RDS.Paginator.DescribeEngineDefaultParameters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeenginedefaultparameterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEngineDefaultParametersMessagePaginateTypeDef]
    ) -> AioPageIterator[DescribeEngineDefaultParametersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeEngineDefaultParameters.html#RDS.Paginator.DescribeEngineDefaultParameters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeenginedefaultparameterspaginator)
        """


if TYPE_CHECKING:
    _DescribeEventSubscriptionsPaginatorBase = AioPaginator[EventSubscriptionsMessageTypeDef]
else:
    _DescribeEventSubscriptionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeEventSubscriptionsPaginator(_DescribeEventSubscriptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeEventSubscriptions.html#RDS.Paginator.DescribeEventSubscriptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeeventsubscriptionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEventSubscriptionsMessagePaginateTypeDef]
    ) -> AioPageIterator[EventSubscriptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeEventSubscriptions.html#RDS.Paginator.DescribeEventSubscriptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeeventsubscriptionspaginator)
        """


if TYPE_CHECKING:
    _DescribeEventsPaginatorBase = AioPaginator[EventsMessageTypeDef]
else:
    _DescribeEventsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeEventsPaginator(_DescribeEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeEvents.html#RDS.Paginator.DescribeEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeeventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEventsMessagePaginateTypeDef]
    ) -> AioPageIterator[EventsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeEvents.html#RDS.Paginator.DescribeEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeeventspaginator)
        """


if TYPE_CHECKING:
    _DescribeExportTasksPaginatorBase = AioPaginator[ExportTasksMessageTypeDef]
else:
    _DescribeExportTasksPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeExportTasksPaginator(_DescribeExportTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeExportTasks.html#RDS.Paginator.DescribeExportTasks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeexporttaskspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeExportTasksMessagePaginateTypeDef]
    ) -> AioPageIterator[ExportTasksMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeExportTasks.html#RDS.Paginator.DescribeExportTasks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeexporttaskspaginator)
        """


if TYPE_CHECKING:
    _DescribeGlobalClustersPaginatorBase = AioPaginator[GlobalClustersMessageTypeDef]
else:
    _DescribeGlobalClustersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeGlobalClustersPaginator(_DescribeGlobalClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeGlobalClusters.html#RDS.Paginator.DescribeGlobalClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeglobalclusterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeGlobalClustersMessagePaginateTypeDef]
    ) -> AioPageIterator[GlobalClustersMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeGlobalClusters.html#RDS.Paginator.DescribeGlobalClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeglobalclusterspaginator)
        """


if TYPE_CHECKING:
    _DescribeIntegrationsPaginatorBase = AioPaginator[DescribeIntegrationsResponseTypeDef]
else:
    _DescribeIntegrationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeIntegrationsPaginator(_DescribeIntegrationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeIntegrations.html#RDS.Paginator.DescribeIntegrations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeintegrationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeIntegrationsMessagePaginateTypeDef]
    ) -> AioPageIterator[DescribeIntegrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeIntegrations.html#RDS.Paginator.DescribeIntegrations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeintegrationspaginator)
        """


if TYPE_CHECKING:
    _DescribeOptionGroupOptionsPaginatorBase = AioPaginator[OptionGroupOptionsMessageTypeDef]
else:
    _DescribeOptionGroupOptionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeOptionGroupOptionsPaginator(_DescribeOptionGroupOptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeOptionGroupOptions.html#RDS.Paginator.DescribeOptionGroupOptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeoptiongroupoptionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeOptionGroupOptionsMessagePaginateTypeDef]
    ) -> AioPageIterator[OptionGroupOptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeOptionGroupOptions.html#RDS.Paginator.DescribeOptionGroupOptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeoptiongroupoptionspaginator)
        """


if TYPE_CHECKING:
    _DescribeOptionGroupsPaginatorBase = AioPaginator[OptionGroupsTypeDef]
else:
    _DescribeOptionGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeOptionGroupsPaginator(_DescribeOptionGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeOptionGroups.html#RDS.Paginator.DescribeOptionGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeoptiongroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeOptionGroupsMessagePaginateTypeDef]
    ) -> AioPageIterator[OptionGroupsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeOptionGroups.html#RDS.Paginator.DescribeOptionGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeoptiongroupspaginator)
        """


if TYPE_CHECKING:
    _DescribeOrderableDBInstanceOptionsPaginatorBase = AioPaginator[
        OrderableDBInstanceOptionsMessageTypeDef
    ]
else:
    _DescribeOrderableDBInstanceOptionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeOrderableDBInstanceOptionsPaginator(_DescribeOrderableDBInstanceOptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeOrderableDBInstanceOptions.html#RDS.Paginator.DescribeOrderableDBInstanceOptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeorderabledbinstanceoptionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeOrderableDBInstanceOptionsMessagePaginateTypeDef]
    ) -> AioPageIterator[OrderableDBInstanceOptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeOrderableDBInstanceOptions.html#RDS.Paginator.DescribeOrderableDBInstanceOptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeorderabledbinstanceoptionspaginator)
        """


if TYPE_CHECKING:
    _DescribePendingMaintenanceActionsPaginatorBase = AioPaginator[
        PendingMaintenanceActionsMessageTypeDef
    ]
else:
    _DescribePendingMaintenanceActionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribePendingMaintenanceActionsPaginator(_DescribePendingMaintenanceActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribePendingMaintenanceActions.html#RDS.Paginator.DescribePendingMaintenanceActions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describependingmaintenanceactionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribePendingMaintenanceActionsMessagePaginateTypeDef]
    ) -> AioPageIterator[PendingMaintenanceActionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribePendingMaintenanceActions.html#RDS.Paginator.DescribePendingMaintenanceActions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describependingmaintenanceactionspaginator)
        """


if TYPE_CHECKING:
    _DescribeReservedDBInstancesOfferingsPaginatorBase = AioPaginator[
        ReservedDBInstancesOfferingMessageTypeDef
    ]
else:
    _DescribeReservedDBInstancesOfferingsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeReservedDBInstancesOfferingsPaginator(
    _DescribeReservedDBInstancesOfferingsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeReservedDBInstancesOfferings.html#RDS.Paginator.DescribeReservedDBInstancesOfferings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describereserveddbinstancesofferingspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReservedDBInstancesOfferingsMessagePaginateTypeDef]
    ) -> AioPageIterator[ReservedDBInstancesOfferingMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeReservedDBInstancesOfferings.html#RDS.Paginator.DescribeReservedDBInstancesOfferings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describereserveddbinstancesofferingspaginator)
        """


if TYPE_CHECKING:
    _DescribeReservedDBInstancesPaginatorBase = AioPaginator[ReservedDBInstanceMessageTypeDef]
else:
    _DescribeReservedDBInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeReservedDBInstancesPaginator(_DescribeReservedDBInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeReservedDBInstances.html#RDS.Paginator.DescribeReservedDBInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describereserveddbinstancespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReservedDBInstancesMessagePaginateTypeDef]
    ) -> AioPageIterator[ReservedDBInstanceMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeReservedDBInstances.html#RDS.Paginator.DescribeReservedDBInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describereserveddbinstancespaginator)
        """


if TYPE_CHECKING:
    _DescribeSourceRegionsPaginatorBase = AioPaginator[SourceRegionMessageTypeDef]
else:
    _DescribeSourceRegionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeSourceRegionsPaginator(_DescribeSourceRegionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeSourceRegions.html#RDS.Paginator.DescribeSourceRegions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describesourceregionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSourceRegionsMessagePaginateTypeDef]
    ) -> AioPageIterator[SourceRegionMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeSourceRegions.html#RDS.Paginator.DescribeSourceRegions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describesourceregionspaginator)
        """


if TYPE_CHECKING:
    _DescribeTenantDatabasesPaginatorBase = AioPaginator[TenantDatabasesMessageTypeDef]
else:
    _DescribeTenantDatabasesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeTenantDatabasesPaginator(_DescribeTenantDatabasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeTenantDatabases.html#RDS.Paginator.DescribeTenantDatabases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describetenantdatabasespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeTenantDatabasesMessagePaginateTypeDef]
    ) -> AioPageIterator[TenantDatabasesMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DescribeTenantDatabases.html#RDS.Paginator.DescribeTenantDatabases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describetenantdatabasespaginator)
        """


if TYPE_CHECKING:
    _DownloadDBLogFilePortionPaginatorBase = AioPaginator[DownloadDBLogFilePortionDetailsTypeDef]
else:
    _DownloadDBLogFilePortionPaginatorBase = AioPaginator  # type: ignore[assignment]


class DownloadDBLogFilePortionPaginator(_DownloadDBLogFilePortionPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DownloadDBLogFilePortion.html#RDS.Paginator.DownloadDBLogFilePortion)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#downloaddblogfileportionpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DownloadDBLogFilePortionMessagePaginateTypeDef]
    ) -> AioPageIterator[DownloadDBLogFilePortionDetailsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/paginator/DownloadDBLogFilePortion.html#RDS.Paginator.DownloadDBLogFilePortion.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#downloaddblogfileportionpaginator)
        """
