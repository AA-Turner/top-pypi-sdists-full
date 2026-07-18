"""
Main interface for odb service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_odb import (
        Client,
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
        ListGiVersionsPaginator,
        ListOdbNetworksPaginator,
        ListOdbPeeringConnectionsPaginator,
        ListSystemVersionsPaginator,
        OdbClient,
    )

    session = get_session()
    async with session.create_client("odb") as client:
        client: OdbClient
        ...


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
    list_gi_versions_paginator: ListGiVersionsPaginator = client.get_paginator("list_gi_versions")
    list_odb_networks_paginator: ListOdbNetworksPaginator = client.get_paginator("list_odb_networks")
    list_odb_peering_connections_paginator: ListOdbPeeringConnectionsPaginator = client.get_paginator("list_odb_peering_connections")
    list_system_versions_paginator: ListSystemVersionsPaginator = client.get_paginator("list_system_versions")
    ```
"""

from .client import OdbClient
from .paginator import (
    ListAutonomousDatabaseBackupsPaginator,
    ListAutonomousDatabaseCharacterSetsPaginator,
    ListAutonomousDatabaseClonesPaginator,
    ListAutonomousDatabasePeersPaginator,
    ListAutonomousDatabasesPaginator,
    ListAutonomousDatabaseVersionsPaginator,
    ListAutonomousVirtualMachinesPaginator,
    ListCloudAutonomousVmClustersPaginator,
    ListCloudExadataInfrastructuresPaginator,
    ListCloudVmClustersPaginator,
    ListDbNodesPaginator,
    ListDbServersPaginator,
    ListDbSystemShapesPaginator,
    ListGiVersionsPaginator,
    ListOdbNetworksPaginator,
    ListOdbPeeringConnectionsPaginator,
    ListSystemVersionsPaginator,
)

Client = OdbClient

__all__ = (
    "Client",
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
    "ListGiVersionsPaginator",
    "ListOdbNetworksPaginator",
    "ListOdbPeeringConnectionsPaginator",
    "ListSystemVersionsPaginator",
    "OdbClient",
)
