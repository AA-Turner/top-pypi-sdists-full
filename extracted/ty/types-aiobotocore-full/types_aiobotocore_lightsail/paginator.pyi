"""
Type annotations for lightsail service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_lightsail.client import LightsailClient
    from types_aiobotocore_lightsail.paginator import (
        GetActiveNamesPaginator,
        GetBlueprintsPaginator,
        GetBundlesPaginator,
        GetCloudFormationStackRecordsPaginator,
        GetDiskSnapshotsPaginator,
        GetDisksPaginator,
        GetDomainsPaginator,
        GetExportSnapshotRecordsPaginator,
        GetInstanceSnapshotsPaginator,
        GetInstancesPaginator,
        GetKeyPairsPaginator,
        GetLoadBalancersPaginator,
        GetOperationsPaginator,
        GetRelationalDatabaseBlueprintsPaginator,
        GetRelationalDatabaseBundlesPaginator,
        GetRelationalDatabaseEventsPaginator,
        GetRelationalDatabaseParametersPaginator,
        GetRelationalDatabaseSnapshotsPaginator,
        GetRelationalDatabasesPaginator,
        GetStaticIpsPaginator,
    )

    session = get_session()
    with session.create_client("lightsail") as client:
        client: LightsailClient

        get_active_names_paginator: GetActiveNamesPaginator = client.get_paginator("get_active_names")
        get_blueprints_paginator: GetBlueprintsPaginator = client.get_paginator("get_blueprints")
        get_bundles_paginator: GetBundlesPaginator = client.get_paginator("get_bundles")
        get_cloud_formation_stack_records_paginator: GetCloudFormationStackRecordsPaginator = client.get_paginator("get_cloud_formation_stack_records")
        get_disk_snapshots_paginator: GetDiskSnapshotsPaginator = client.get_paginator("get_disk_snapshots")
        get_disks_paginator: GetDisksPaginator = client.get_paginator("get_disks")
        get_domains_paginator: GetDomainsPaginator = client.get_paginator("get_domains")
        get_export_snapshot_records_paginator: GetExportSnapshotRecordsPaginator = client.get_paginator("get_export_snapshot_records")
        get_instance_snapshots_paginator: GetInstanceSnapshotsPaginator = client.get_paginator("get_instance_snapshots")
        get_instances_paginator: GetInstancesPaginator = client.get_paginator("get_instances")
        get_key_pairs_paginator: GetKeyPairsPaginator = client.get_paginator("get_key_pairs")
        get_load_balancers_paginator: GetLoadBalancersPaginator = client.get_paginator("get_load_balancers")
        get_operations_paginator: GetOperationsPaginator = client.get_paginator("get_operations")
        get_relational_database_blueprints_paginator: GetRelationalDatabaseBlueprintsPaginator = client.get_paginator("get_relational_database_blueprints")
        get_relational_database_bundles_paginator: GetRelationalDatabaseBundlesPaginator = client.get_paginator("get_relational_database_bundles")
        get_relational_database_events_paginator: GetRelationalDatabaseEventsPaginator = client.get_paginator("get_relational_database_events")
        get_relational_database_parameters_paginator: GetRelationalDatabaseParametersPaginator = client.get_paginator("get_relational_database_parameters")
        get_relational_database_snapshots_paginator: GetRelationalDatabaseSnapshotsPaginator = client.get_paginator("get_relational_database_snapshots")
        get_relational_databases_paginator: GetRelationalDatabasesPaginator = client.get_paginator("get_relational_databases")
        get_static_ips_paginator: GetStaticIpsPaginator = client.get_paginator("get_static_ips")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetActiveNamesRequestPaginateTypeDef,
    GetActiveNamesResultTypeDef,
    GetBlueprintsRequestPaginateTypeDef,
    GetBlueprintsResultTypeDef,
    GetBundlesRequestPaginateTypeDef,
    GetBundlesResultTypeDef,
    GetCloudFormationStackRecordsRequestPaginateTypeDef,
    GetCloudFormationStackRecordsResultTypeDef,
    GetDiskSnapshotsRequestPaginateTypeDef,
    GetDiskSnapshotsResultTypeDef,
    GetDisksRequestPaginateTypeDef,
    GetDisksResultTypeDef,
    GetDomainsRequestPaginateTypeDef,
    GetDomainsResultTypeDef,
    GetExportSnapshotRecordsRequestPaginateTypeDef,
    GetExportSnapshotRecordsResultTypeDef,
    GetInstanceSnapshotsRequestPaginateTypeDef,
    GetInstanceSnapshotsResultTypeDef,
    GetInstancesRequestPaginateTypeDef,
    GetInstancesResultTypeDef,
    GetKeyPairsRequestPaginateTypeDef,
    GetKeyPairsResultTypeDef,
    GetLoadBalancersRequestPaginateTypeDef,
    GetLoadBalancersResultTypeDef,
    GetOperationsRequestPaginateTypeDef,
    GetOperationsResultTypeDef,
    GetRelationalDatabaseBlueprintsRequestPaginateTypeDef,
    GetRelationalDatabaseBlueprintsResultTypeDef,
    GetRelationalDatabaseBundlesRequestPaginateTypeDef,
    GetRelationalDatabaseBundlesResultTypeDef,
    GetRelationalDatabaseEventsRequestPaginateTypeDef,
    GetRelationalDatabaseEventsResultTypeDef,
    GetRelationalDatabaseParametersRequestPaginateTypeDef,
    GetRelationalDatabaseParametersResultTypeDef,
    GetRelationalDatabaseSnapshotsRequestPaginateTypeDef,
    GetRelationalDatabaseSnapshotsResultTypeDef,
    GetRelationalDatabasesRequestPaginateTypeDef,
    GetRelationalDatabasesResultTypeDef,
    GetStaticIpsRequestPaginateTypeDef,
    GetStaticIpsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetActiveNamesPaginator",
    "GetBlueprintsPaginator",
    "GetBundlesPaginator",
    "GetCloudFormationStackRecordsPaginator",
    "GetDiskSnapshotsPaginator",
    "GetDisksPaginator",
    "GetDomainsPaginator",
    "GetExportSnapshotRecordsPaginator",
    "GetInstanceSnapshotsPaginator",
    "GetInstancesPaginator",
    "GetKeyPairsPaginator",
    "GetLoadBalancersPaginator",
    "GetOperationsPaginator",
    "GetRelationalDatabaseBlueprintsPaginator",
    "GetRelationalDatabaseBundlesPaginator",
    "GetRelationalDatabaseEventsPaginator",
    "GetRelationalDatabaseParametersPaginator",
    "GetRelationalDatabaseSnapshotsPaginator",
    "GetRelationalDatabasesPaginator",
    "GetStaticIpsPaginator",
)

if TYPE_CHECKING:
    _GetActiveNamesPaginatorBase = AioPaginator[GetActiveNamesResultTypeDef]
else:
    _GetActiveNamesPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetActiveNamesPaginator(_GetActiveNamesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetActiveNames.html#Lightsail.Paginator.GetActiveNames)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getactivenamespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetActiveNamesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetActiveNamesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetActiveNames.html#Lightsail.Paginator.GetActiveNames.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getactivenamespaginator)
        """

if TYPE_CHECKING:
    _GetBlueprintsPaginatorBase = AioPaginator[GetBlueprintsResultTypeDef]
else:
    _GetBlueprintsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetBlueprintsPaginator(_GetBlueprintsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetBlueprints.html#Lightsail.Paginator.GetBlueprints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getblueprintspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetBlueprintsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetBlueprintsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetBlueprints.html#Lightsail.Paginator.GetBlueprints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getblueprintspaginator)
        """

if TYPE_CHECKING:
    _GetBundlesPaginatorBase = AioPaginator[GetBundlesResultTypeDef]
else:
    _GetBundlesPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetBundlesPaginator(_GetBundlesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetBundles.html#Lightsail.Paginator.GetBundles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getbundlespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetBundlesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetBundlesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetBundles.html#Lightsail.Paginator.GetBundles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getbundlespaginator)
        """

if TYPE_CHECKING:
    _GetCloudFormationStackRecordsPaginatorBase = AioPaginator[
        GetCloudFormationStackRecordsResultTypeDef
    ]
else:
    _GetCloudFormationStackRecordsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetCloudFormationStackRecordsPaginator(_GetCloudFormationStackRecordsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetCloudFormationStackRecords.html#Lightsail.Paginator.GetCloudFormationStackRecords)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getcloudformationstackrecordspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetCloudFormationStackRecordsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetCloudFormationStackRecordsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetCloudFormationStackRecords.html#Lightsail.Paginator.GetCloudFormationStackRecords.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getcloudformationstackrecordspaginator)
        """

if TYPE_CHECKING:
    _GetDiskSnapshotsPaginatorBase = AioPaginator[GetDiskSnapshotsResultTypeDef]
else:
    _GetDiskSnapshotsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetDiskSnapshotsPaginator(_GetDiskSnapshotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetDiskSnapshots.html#Lightsail.Paginator.GetDiskSnapshots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getdisksnapshotspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetDiskSnapshotsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetDiskSnapshotsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetDiskSnapshots.html#Lightsail.Paginator.GetDiskSnapshots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getdisksnapshotspaginator)
        """

if TYPE_CHECKING:
    _GetDisksPaginatorBase = AioPaginator[GetDisksResultTypeDef]
else:
    _GetDisksPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetDisksPaginator(_GetDisksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetDisks.html#Lightsail.Paginator.GetDisks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getdiskspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetDisksRequestPaginateTypeDef]
    ) -> AioPageIterator[GetDisksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetDisks.html#Lightsail.Paginator.GetDisks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getdiskspaginator)
        """

if TYPE_CHECKING:
    _GetDomainsPaginatorBase = AioPaginator[GetDomainsResultTypeDef]
else:
    _GetDomainsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetDomainsPaginator(_GetDomainsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetDomains.html#Lightsail.Paginator.GetDomains)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getdomainspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetDomainsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetDomainsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetDomains.html#Lightsail.Paginator.GetDomains.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getdomainspaginator)
        """

if TYPE_CHECKING:
    _GetExportSnapshotRecordsPaginatorBase = AioPaginator[GetExportSnapshotRecordsResultTypeDef]
else:
    _GetExportSnapshotRecordsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetExportSnapshotRecordsPaginator(_GetExportSnapshotRecordsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetExportSnapshotRecords.html#Lightsail.Paginator.GetExportSnapshotRecords)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getexportsnapshotrecordspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetExportSnapshotRecordsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetExportSnapshotRecordsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetExportSnapshotRecords.html#Lightsail.Paginator.GetExportSnapshotRecords.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getexportsnapshotrecordspaginator)
        """

if TYPE_CHECKING:
    _GetInstanceSnapshotsPaginatorBase = AioPaginator[GetInstanceSnapshotsResultTypeDef]
else:
    _GetInstanceSnapshotsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetInstanceSnapshotsPaginator(_GetInstanceSnapshotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetInstanceSnapshots.html#Lightsail.Paginator.GetInstanceSnapshots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getinstancesnapshotspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetInstanceSnapshotsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetInstanceSnapshotsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetInstanceSnapshots.html#Lightsail.Paginator.GetInstanceSnapshots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getinstancesnapshotspaginator)
        """

if TYPE_CHECKING:
    _GetInstancesPaginatorBase = AioPaginator[GetInstancesResultTypeDef]
else:
    _GetInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetInstancesPaginator(_GetInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetInstances.html#Lightsail.Paginator.GetInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getinstancespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetInstancesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetInstancesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetInstances.html#Lightsail.Paginator.GetInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getinstancespaginator)
        """

if TYPE_CHECKING:
    _GetKeyPairsPaginatorBase = AioPaginator[GetKeyPairsResultTypeDef]
else:
    _GetKeyPairsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetKeyPairsPaginator(_GetKeyPairsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetKeyPairs.html#Lightsail.Paginator.GetKeyPairs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getkeypairspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetKeyPairsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetKeyPairsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetKeyPairs.html#Lightsail.Paginator.GetKeyPairs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getkeypairspaginator)
        """

if TYPE_CHECKING:
    _GetLoadBalancersPaginatorBase = AioPaginator[GetLoadBalancersResultTypeDef]
else:
    _GetLoadBalancersPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetLoadBalancersPaginator(_GetLoadBalancersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetLoadBalancers.html#Lightsail.Paginator.GetLoadBalancers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getloadbalancerspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetLoadBalancersRequestPaginateTypeDef]
    ) -> AioPageIterator[GetLoadBalancersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetLoadBalancers.html#Lightsail.Paginator.GetLoadBalancers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getloadbalancerspaginator)
        """

if TYPE_CHECKING:
    _GetOperationsPaginatorBase = AioPaginator[GetOperationsResultTypeDef]
else:
    _GetOperationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetOperationsPaginator(_GetOperationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetOperations.html#Lightsail.Paginator.GetOperations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getoperationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetOperationsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetOperationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetOperations.html#Lightsail.Paginator.GetOperations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getoperationspaginator)
        """

if TYPE_CHECKING:
    _GetRelationalDatabaseBlueprintsPaginatorBase = AioPaginator[
        GetRelationalDatabaseBlueprintsResultTypeDef
    ]
else:
    _GetRelationalDatabaseBlueprintsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetRelationalDatabaseBlueprintsPaginator(_GetRelationalDatabaseBlueprintsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetRelationalDatabaseBlueprints.html#Lightsail.Paginator.GetRelationalDatabaseBlueprints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabaseblueprintspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetRelationalDatabaseBlueprintsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetRelationalDatabaseBlueprintsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetRelationalDatabaseBlueprints.html#Lightsail.Paginator.GetRelationalDatabaseBlueprints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabaseblueprintspaginator)
        """

if TYPE_CHECKING:
    _GetRelationalDatabaseBundlesPaginatorBase = AioPaginator[
        GetRelationalDatabaseBundlesResultTypeDef
    ]
else:
    _GetRelationalDatabaseBundlesPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetRelationalDatabaseBundlesPaginator(_GetRelationalDatabaseBundlesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetRelationalDatabaseBundles.html#Lightsail.Paginator.GetRelationalDatabaseBundles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabasebundlespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetRelationalDatabaseBundlesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetRelationalDatabaseBundlesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetRelationalDatabaseBundles.html#Lightsail.Paginator.GetRelationalDatabaseBundles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabasebundlespaginator)
        """

if TYPE_CHECKING:
    _GetRelationalDatabaseEventsPaginatorBase = AioPaginator[
        GetRelationalDatabaseEventsResultTypeDef
    ]
else:
    _GetRelationalDatabaseEventsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetRelationalDatabaseEventsPaginator(_GetRelationalDatabaseEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetRelationalDatabaseEvents.html#Lightsail.Paginator.GetRelationalDatabaseEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabaseeventspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetRelationalDatabaseEventsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetRelationalDatabaseEventsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetRelationalDatabaseEvents.html#Lightsail.Paginator.GetRelationalDatabaseEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabaseeventspaginator)
        """

if TYPE_CHECKING:
    _GetRelationalDatabaseParametersPaginatorBase = AioPaginator[
        GetRelationalDatabaseParametersResultTypeDef
    ]
else:
    _GetRelationalDatabaseParametersPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetRelationalDatabaseParametersPaginator(_GetRelationalDatabaseParametersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetRelationalDatabaseParameters.html#Lightsail.Paginator.GetRelationalDatabaseParameters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabaseparameterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetRelationalDatabaseParametersRequestPaginateTypeDef]
    ) -> AioPageIterator[GetRelationalDatabaseParametersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetRelationalDatabaseParameters.html#Lightsail.Paginator.GetRelationalDatabaseParameters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabaseparameterspaginator)
        """

if TYPE_CHECKING:
    _GetRelationalDatabaseSnapshotsPaginatorBase = AioPaginator[
        GetRelationalDatabaseSnapshotsResultTypeDef
    ]
else:
    _GetRelationalDatabaseSnapshotsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetRelationalDatabaseSnapshotsPaginator(_GetRelationalDatabaseSnapshotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetRelationalDatabaseSnapshots.html#Lightsail.Paginator.GetRelationalDatabaseSnapshots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabasesnapshotspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetRelationalDatabaseSnapshotsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetRelationalDatabaseSnapshotsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetRelationalDatabaseSnapshots.html#Lightsail.Paginator.GetRelationalDatabaseSnapshots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabasesnapshotspaginator)
        """

if TYPE_CHECKING:
    _GetRelationalDatabasesPaginatorBase = AioPaginator[GetRelationalDatabasesResultTypeDef]
else:
    _GetRelationalDatabasesPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetRelationalDatabasesPaginator(_GetRelationalDatabasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetRelationalDatabases.html#Lightsail.Paginator.GetRelationalDatabases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabasespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetRelationalDatabasesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetRelationalDatabasesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetRelationalDatabases.html#Lightsail.Paginator.GetRelationalDatabases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabasespaginator)
        """

if TYPE_CHECKING:
    _GetStaticIpsPaginatorBase = AioPaginator[GetStaticIpsResultTypeDef]
else:
    _GetStaticIpsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetStaticIpsPaginator(_GetStaticIpsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetStaticIps.html#Lightsail.Paginator.GetStaticIps)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getstaticipspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetStaticIpsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetStaticIpsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetStaticIps.html#Lightsail.Paginator.GetStaticIps.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getstaticipspaginator)
        """
