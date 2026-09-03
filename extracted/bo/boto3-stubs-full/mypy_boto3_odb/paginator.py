"""
Type annotations for odb service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_odb.client import OdbClient
    from mypy_boto3_odb.paginator import (
        ListAutonomousDatabaseBackupsPaginator,
        ListAutonomousDatabaseCharacterSetsPaginator,
        ListAutonomousDatabaseClonesPaginator,
        ListAutonomousDatabasePeersPaginator,
        ListAutonomousDatabaseVersionsPaginator,
        ListAutonomousDatabasesPaginator,
        ListAutonomousVirtualMachinesPaginator,
        ListCloudAutonomousVmClustersPaginator,
        ListCloudExadataInfrastructuresPaginator,
        ListCloudVmClustersPaginator,
        ListDbNodesPaginator,
        ListDbServersPaginator,
        ListDbSystemShapesPaginator,
        ListExadbVmClustersPaginator,
        ListExascaleDbStorageVaultsPaginator,
        ListFlexComponentsPaginator,
        ListGiMinorVersionsPaginator,
        ListGiVersionsPaginator,
        ListOdbNetworksPaginator,
        ListOdbPeeringConnectionsPaginator,
        ListSystemVersionsPaginator,
    )

    session = Session()
    client: OdbClient = session.client("odb")

    list_autonomous_database_backups_paginator: ListAutonomousDatabaseBackupsPaginator = client.get_paginator("list_autonomous_database_backups")
    list_autonomous_database_character_sets_paginator: ListAutonomousDatabaseCharacterSetsPaginator = client.get_paginator("list_autonomous_database_character_sets")
    list_autonomous_database_clones_paginator: ListAutonomousDatabaseClonesPaginator = client.get_paginator("list_autonomous_database_clones")
    list_autonomous_database_peers_paginator: ListAutonomousDatabasePeersPaginator = client.get_paginator("list_autonomous_database_peers")
    list_autonomous_database_versions_paginator: ListAutonomousDatabaseVersionsPaginator = client.get_paginator("list_autonomous_database_versions")
    list_autonomous_databases_paginator: ListAutonomousDatabasesPaginator = client.get_paginator("list_autonomous_databases")
    list_autonomous_virtual_machines_paginator: ListAutonomousVirtualMachinesPaginator = client.get_paginator("list_autonomous_virtual_machines")
    list_cloud_autonomous_vm_clusters_paginator: ListCloudAutonomousVmClustersPaginator = client.get_paginator("list_cloud_autonomous_vm_clusters")
    list_cloud_exadata_infrastructures_paginator: ListCloudExadataInfrastructuresPaginator = client.get_paginator("list_cloud_exadata_infrastructures")
    list_cloud_vm_clusters_paginator: ListCloudVmClustersPaginator = client.get_paginator("list_cloud_vm_clusters")
    list_db_nodes_paginator: ListDbNodesPaginator = client.get_paginator("list_db_nodes")
    list_db_servers_paginator: ListDbServersPaginator = client.get_paginator("list_db_servers")
    list_db_system_shapes_paginator: ListDbSystemShapesPaginator = client.get_paginator("list_db_system_shapes")
    list_exadb_vm_clusters_paginator: ListExadbVmClustersPaginator = client.get_paginator("list_exadb_vm_clusters")
    list_exascale_db_storage_vaults_paginator: ListExascaleDbStorageVaultsPaginator = client.get_paginator("list_exascale_db_storage_vaults")
    list_flex_components_paginator: ListFlexComponentsPaginator = client.get_paginator("list_flex_components")
    list_gi_minor_versions_paginator: ListGiMinorVersionsPaginator = client.get_paginator("list_gi_minor_versions")
    list_gi_versions_paginator: ListGiVersionsPaginator = client.get_paginator("list_gi_versions")
    list_odb_networks_paginator: ListOdbNetworksPaginator = client.get_paginator("list_odb_networks")
    list_odb_peering_connections_paginator: ListOdbPeeringConnectionsPaginator = client.get_paginator("list_odb_peering_connections")
    list_system_versions_paginator: ListSystemVersionsPaginator = client.get_paginator("list_system_versions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAutonomousDatabaseBackupsInputPaginateTypeDef,
    ListAutonomousDatabaseBackupsOutputTypeDef,
    ListAutonomousDatabaseCharacterSetsInputPaginateTypeDef,
    ListAutonomousDatabaseCharacterSetsOutputTypeDef,
    ListAutonomousDatabaseClonesInputPaginateTypeDef,
    ListAutonomousDatabaseClonesOutputTypeDef,
    ListAutonomousDatabasePeersInputPaginateTypeDef,
    ListAutonomousDatabasePeersOutputTypeDef,
    ListAutonomousDatabasesInputPaginateTypeDef,
    ListAutonomousDatabasesOutputTypeDef,
    ListAutonomousDatabaseVersionsInputPaginateTypeDef,
    ListAutonomousDatabaseVersionsOutputTypeDef,
    ListAutonomousVirtualMachinesInputPaginateTypeDef,
    ListAutonomousVirtualMachinesOutputTypeDef,
    ListCloudAutonomousVmClustersInputPaginateTypeDef,
    ListCloudAutonomousVmClustersOutputTypeDef,
    ListCloudExadataInfrastructuresInputPaginateTypeDef,
    ListCloudExadataInfrastructuresOutputTypeDef,
    ListCloudVmClustersInputPaginateTypeDef,
    ListCloudVmClustersOutputTypeDef,
    ListDbNodesInputPaginateTypeDef,
    ListDbNodesOutputTypeDef,
    ListDbServersInputPaginateTypeDef,
    ListDbServersOutputTypeDef,
    ListDbSystemShapesInputPaginateTypeDef,
    ListDbSystemShapesOutputTypeDef,
    ListExadbVmClustersInputPaginateTypeDef,
    ListExadbVmClustersOutputTypeDef,
    ListExascaleDbStorageVaultsInputPaginateTypeDef,
    ListExascaleDbStorageVaultsOutputTypeDef,
    ListFlexComponentsInputPaginateTypeDef,
    ListFlexComponentsOutputTypeDef,
    ListGiMinorVersionsInputPaginateTypeDef,
    ListGiMinorVersionsOutputTypeDef,
    ListGiVersionsInputPaginateTypeDef,
    ListGiVersionsOutputTypeDef,
    ListOdbNetworksInputPaginateTypeDef,
    ListOdbNetworksOutputTypeDef,
    ListOdbPeeringConnectionsInputPaginateTypeDef,
    ListOdbPeeringConnectionsOutputTypeDef,
    ListSystemVersionsInputPaginateTypeDef,
    ListSystemVersionsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAutonomousDatabaseBackupsPaginator",
    "ListAutonomousDatabaseCharacterSetsPaginator",
    "ListAutonomousDatabaseClonesPaginator",
    "ListAutonomousDatabasePeersPaginator",
    "ListAutonomousDatabaseVersionsPaginator",
    "ListAutonomousDatabasesPaginator",
    "ListAutonomousVirtualMachinesPaginator",
    "ListCloudAutonomousVmClustersPaginator",
    "ListCloudExadataInfrastructuresPaginator",
    "ListCloudVmClustersPaginator",
    "ListDbNodesPaginator",
    "ListDbServersPaginator",
    "ListDbSystemShapesPaginator",
    "ListExadbVmClustersPaginator",
    "ListExascaleDbStorageVaultsPaginator",
    "ListFlexComponentsPaginator",
    "ListGiMinorVersionsPaginator",
    "ListGiVersionsPaginator",
    "ListOdbNetworksPaginator",
    "ListOdbPeeringConnectionsPaginator",
    "ListSystemVersionsPaginator",
)


if TYPE_CHECKING:
    _ListAutonomousDatabaseBackupsPaginatorBase = Paginator[
        ListAutonomousDatabaseBackupsOutputTypeDef
    ]
else:
    _ListAutonomousDatabaseBackupsPaginatorBase = Paginator  # type: ignore[assignment]


class ListAutonomousDatabaseBackupsPaginator(_ListAutonomousDatabaseBackupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListAutonomousDatabaseBackups.html#Odb.Paginator.ListAutonomousDatabaseBackups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listautonomousdatabasebackupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAutonomousDatabaseBackupsInputPaginateTypeDef]
    ) -> PageIterator[ListAutonomousDatabaseBackupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListAutonomousDatabaseBackups.html#Odb.Paginator.ListAutonomousDatabaseBackups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listautonomousdatabasebackupspaginator)
        """


if TYPE_CHECKING:
    _ListAutonomousDatabaseCharacterSetsPaginatorBase = Paginator[
        ListAutonomousDatabaseCharacterSetsOutputTypeDef
    ]
else:
    _ListAutonomousDatabaseCharacterSetsPaginatorBase = Paginator  # type: ignore[assignment]


class ListAutonomousDatabaseCharacterSetsPaginator(
    _ListAutonomousDatabaseCharacterSetsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListAutonomousDatabaseCharacterSets.html#Odb.Paginator.ListAutonomousDatabaseCharacterSets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listautonomousdatabasecharactersetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAutonomousDatabaseCharacterSetsInputPaginateTypeDef]
    ) -> PageIterator[ListAutonomousDatabaseCharacterSetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListAutonomousDatabaseCharacterSets.html#Odb.Paginator.ListAutonomousDatabaseCharacterSets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listautonomousdatabasecharactersetspaginator)
        """


if TYPE_CHECKING:
    _ListAutonomousDatabaseClonesPaginatorBase = Paginator[
        ListAutonomousDatabaseClonesOutputTypeDef
    ]
else:
    _ListAutonomousDatabaseClonesPaginatorBase = Paginator  # type: ignore[assignment]


class ListAutonomousDatabaseClonesPaginator(_ListAutonomousDatabaseClonesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListAutonomousDatabaseClones.html#Odb.Paginator.ListAutonomousDatabaseClones)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listautonomousdatabaseclonespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAutonomousDatabaseClonesInputPaginateTypeDef]
    ) -> PageIterator[ListAutonomousDatabaseClonesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListAutonomousDatabaseClones.html#Odb.Paginator.ListAutonomousDatabaseClones.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listautonomousdatabaseclonespaginator)
        """


if TYPE_CHECKING:
    _ListAutonomousDatabasePeersPaginatorBase = Paginator[ListAutonomousDatabasePeersOutputTypeDef]
else:
    _ListAutonomousDatabasePeersPaginatorBase = Paginator  # type: ignore[assignment]


class ListAutonomousDatabasePeersPaginator(_ListAutonomousDatabasePeersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListAutonomousDatabasePeers.html#Odb.Paginator.ListAutonomousDatabasePeers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listautonomousdatabasepeerspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAutonomousDatabasePeersInputPaginateTypeDef]
    ) -> PageIterator[ListAutonomousDatabasePeersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListAutonomousDatabasePeers.html#Odb.Paginator.ListAutonomousDatabasePeers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listautonomousdatabasepeerspaginator)
        """


if TYPE_CHECKING:
    _ListAutonomousDatabaseVersionsPaginatorBase = Paginator[
        ListAutonomousDatabaseVersionsOutputTypeDef
    ]
else:
    _ListAutonomousDatabaseVersionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListAutonomousDatabaseVersionsPaginator(_ListAutonomousDatabaseVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListAutonomousDatabaseVersions.html#Odb.Paginator.ListAutonomousDatabaseVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listautonomousdatabaseversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAutonomousDatabaseVersionsInputPaginateTypeDef]
    ) -> PageIterator[ListAutonomousDatabaseVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListAutonomousDatabaseVersions.html#Odb.Paginator.ListAutonomousDatabaseVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listautonomousdatabaseversionspaginator)
        """


if TYPE_CHECKING:
    _ListAutonomousDatabasesPaginatorBase = Paginator[ListAutonomousDatabasesOutputTypeDef]
else:
    _ListAutonomousDatabasesPaginatorBase = Paginator  # type: ignore[assignment]


class ListAutonomousDatabasesPaginator(_ListAutonomousDatabasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListAutonomousDatabases.html#Odb.Paginator.ListAutonomousDatabases)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listautonomousdatabasespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAutonomousDatabasesInputPaginateTypeDef]
    ) -> PageIterator[ListAutonomousDatabasesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListAutonomousDatabases.html#Odb.Paginator.ListAutonomousDatabases.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listautonomousdatabasespaginator)
        """


if TYPE_CHECKING:
    _ListAutonomousVirtualMachinesPaginatorBase = Paginator[
        ListAutonomousVirtualMachinesOutputTypeDef
    ]
else:
    _ListAutonomousVirtualMachinesPaginatorBase = Paginator  # type: ignore[assignment]


class ListAutonomousVirtualMachinesPaginator(_ListAutonomousVirtualMachinesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListAutonomousVirtualMachines.html#Odb.Paginator.ListAutonomousVirtualMachines)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listautonomousvirtualmachinespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAutonomousVirtualMachinesInputPaginateTypeDef]
    ) -> PageIterator[ListAutonomousVirtualMachinesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListAutonomousVirtualMachines.html#Odb.Paginator.ListAutonomousVirtualMachines.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listautonomousvirtualmachinespaginator)
        """


if TYPE_CHECKING:
    _ListCloudAutonomousVmClustersPaginatorBase = Paginator[
        ListCloudAutonomousVmClustersOutputTypeDef
    ]
else:
    _ListCloudAutonomousVmClustersPaginatorBase = Paginator  # type: ignore[assignment]


class ListCloudAutonomousVmClustersPaginator(_ListCloudAutonomousVmClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListCloudAutonomousVmClusters.html#Odb.Paginator.ListCloudAutonomousVmClusters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listcloudautonomousvmclusterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCloudAutonomousVmClustersInputPaginateTypeDef]
    ) -> PageIterator[ListCloudAutonomousVmClustersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListCloudAutonomousVmClusters.html#Odb.Paginator.ListCloudAutonomousVmClusters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listcloudautonomousvmclusterspaginator)
        """


if TYPE_CHECKING:
    _ListCloudExadataInfrastructuresPaginatorBase = Paginator[
        ListCloudExadataInfrastructuresOutputTypeDef
    ]
else:
    _ListCloudExadataInfrastructuresPaginatorBase = Paginator  # type: ignore[assignment]


class ListCloudExadataInfrastructuresPaginator(_ListCloudExadataInfrastructuresPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListCloudExadataInfrastructures.html#Odb.Paginator.ListCloudExadataInfrastructures)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listcloudexadatainfrastructurespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCloudExadataInfrastructuresInputPaginateTypeDef]
    ) -> PageIterator[ListCloudExadataInfrastructuresOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListCloudExadataInfrastructures.html#Odb.Paginator.ListCloudExadataInfrastructures.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listcloudexadatainfrastructurespaginator)
        """


if TYPE_CHECKING:
    _ListCloudVmClustersPaginatorBase = Paginator[ListCloudVmClustersOutputTypeDef]
else:
    _ListCloudVmClustersPaginatorBase = Paginator  # type: ignore[assignment]


class ListCloudVmClustersPaginator(_ListCloudVmClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListCloudVmClusters.html#Odb.Paginator.ListCloudVmClusters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listcloudvmclusterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCloudVmClustersInputPaginateTypeDef]
    ) -> PageIterator[ListCloudVmClustersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListCloudVmClusters.html#Odb.Paginator.ListCloudVmClusters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listcloudvmclusterspaginator)
        """


if TYPE_CHECKING:
    _ListDbNodesPaginatorBase = Paginator[ListDbNodesOutputTypeDef]
else:
    _ListDbNodesPaginatorBase = Paginator  # type: ignore[assignment]


class ListDbNodesPaginator(_ListDbNodesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListDbNodes.html#Odb.Paginator.ListDbNodes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listdbnodespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDbNodesInputPaginateTypeDef]
    ) -> PageIterator[ListDbNodesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListDbNodes.html#Odb.Paginator.ListDbNodes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listdbnodespaginator)
        """


if TYPE_CHECKING:
    _ListDbServersPaginatorBase = Paginator[ListDbServersOutputTypeDef]
else:
    _ListDbServersPaginatorBase = Paginator  # type: ignore[assignment]


class ListDbServersPaginator(_ListDbServersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListDbServers.html#Odb.Paginator.ListDbServers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listdbserverspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDbServersInputPaginateTypeDef]
    ) -> PageIterator[ListDbServersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListDbServers.html#Odb.Paginator.ListDbServers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listdbserverspaginator)
        """


if TYPE_CHECKING:
    _ListDbSystemShapesPaginatorBase = Paginator[ListDbSystemShapesOutputTypeDef]
else:
    _ListDbSystemShapesPaginatorBase = Paginator  # type: ignore[assignment]


class ListDbSystemShapesPaginator(_ListDbSystemShapesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListDbSystemShapes.html#Odb.Paginator.ListDbSystemShapes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listdbsystemshapespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDbSystemShapesInputPaginateTypeDef]
    ) -> PageIterator[ListDbSystemShapesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListDbSystemShapes.html#Odb.Paginator.ListDbSystemShapes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listdbsystemshapespaginator)
        """


if TYPE_CHECKING:
    _ListExadbVmClustersPaginatorBase = Paginator[ListExadbVmClustersOutputTypeDef]
else:
    _ListExadbVmClustersPaginatorBase = Paginator  # type: ignore[assignment]


class ListExadbVmClustersPaginator(_ListExadbVmClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListExadbVmClusters.html#Odb.Paginator.ListExadbVmClusters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listexadbvmclusterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExadbVmClustersInputPaginateTypeDef]
    ) -> PageIterator[ListExadbVmClustersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListExadbVmClusters.html#Odb.Paginator.ListExadbVmClusters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listexadbvmclusterspaginator)
        """


if TYPE_CHECKING:
    _ListExascaleDbStorageVaultsPaginatorBase = Paginator[ListExascaleDbStorageVaultsOutputTypeDef]
else:
    _ListExascaleDbStorageVaultsPaginatorBase = Paginator  # type: ignore[assignment]


class ListExascaleDbStorageVaultsPaginator(_ListExascaleDbStorageVaultsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListExascaleDbStorageVaults.html#Odb.Paginator.ListExascaleDbStorageVaults)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listexascaledbstoragevaultspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExascaleDbStorageVaultsInputPaginateTypeDef]
    ) -> PageIterator[ListExascaleDbStorageVaultsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListExascaleDbStorageVaults.html#Odb.Paginator.ListExascaleDbStorageVaults.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listexascaledbstoragevaultspaginator)
        """


if TYPE_CHECKING:
    _ListFlexComponentsPaginatorBase = Paginator[ListFlexComponentsOutputTypeDef]
else:
    _ListFlexComponentsPaginatorBase = Paginator  # type: ignore[assignment]


class ListFlexComponentsPaginator(_ListFlexComponentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListFlexComponents.html#Odb.Paginator.ListFlexComponents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listflexcomponentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFlexComponentsInputPaginateTypeDef]
    ) -> PageIterator[ListFlexComponentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListFlexComponents.html#Odb.Paginator.ListFlexComponents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listflexcomponentspaginator)
        """


if TYPE_CHECKING:
    _ListGiMinorVersionsPaginatorBase = Paginator[ListGiMinorVersionsOutputTypeDef]
else:
    _ListGiMinorVersionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListGiMinorVersionsPaginator(_ListGiMinorVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListGiMinorVersions.html#Odb.Paginator.ListGiMinorVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listgiminorversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGiMinorVersionsInputPaginateTypeDef]
    ) -> PageIterator[ListGiMinorVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListGiMinorVersions.html#Odb.Paginator.ListGiMinorVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listgiminorversionspaginator)
        """


if TYPE_CHECKING:
    _ListGiVersionsPaginatorBase = Paginator[ListGiVersionsOutputTypeDef]
else:
    _ListGiVersionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListGiVersionsPaginator(_ListGiVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListGiVersions.html#Odb.Paginator.ListGiVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listgiversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGiVersionsInputPaginateTypeDef]
    ) -> PageIterator[ListGiVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListGiVersions.html#Odb.Paginator.ListGiVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listgiversionspaginator)
        """


if TYPE_CHECKING:
    _ListOdbNetworksPaginatorBase = Paginator[ListOdbNetworksOutputTypeDef]
else:
    _ListOdbNetworksPaginatorBase = Paginator  # type: ignore[assignment]


class ListOdbNetworksPaginator(_ListOdbNetworksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListOdbNetworks.html#Odb.Paginator.ListOdbNetworks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listodbnetworkspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOdbNetworksInputPaginateTypeDef]
    ) -> PageIterator[ListOdbNetworksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListOdbNetworks.html#Odb.Paginator.ListOdbNetworks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listodbnetworkspaginator)
        """


if TYPE_CHECKING:
    _ListOdbPeeringConnectionsPaginatorBase = Paginator[ListOdbPeeringConnectionsOutputTypeDef]
else:
    _ListOdbPeeringConnectionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListOdbPeeringConnectionsPaginator(_ListOdbPeeringConnectionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListOdbPeeringConnections.html#Odb.Paginator.ListOdbPeeringConnections)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listodbpeeringconnectionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOdbPeeringConnectionsInputPaginateTypeDef]
    ) -> PageIterator[ListOdbPeeringConnectionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListOdbPeeringConnections.html#Odb.Paginator.ListOdbPeeringConnections.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listodbpeeringconnectionspaginator)
        """


if TYPE_CHECKING:
    _ListSystemVersionsPaginatorBase = Paginator[ListSystemVersionsOutputTypeDef]
else:
    _ListSystemVersionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListSystemVersionsPaginator(_ListSystemVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListSystemVersions.html#Odb.Paginator.ListSystemVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listsystemversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSystemVersionsInputPaginateTypeDef]
    ) -> PageIterator[ListSystemVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListSystemVersions.html#Odb.Paginator.ListSystemVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_odb/paginators/#listsystemversionspaginator)
        """
