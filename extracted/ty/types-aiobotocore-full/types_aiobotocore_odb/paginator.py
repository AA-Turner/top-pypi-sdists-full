"""
Type annotations for odb service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_odb.client import OdbClient
    from types_aiobotocore_odb.paginator import (
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

    session = get_session()
    with session.create_client("odb") as client:
        client: OdbClient

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

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
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
)


if TYPE_CHECKING:
    _ListAutonomousVirtualMachinesPaginatorBase = AioPaginator[
        ListAutonomousVirtualMachinesOutputTypeDef
    ]
else:
    _ListAutonomousVirtualMachinesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAutonomousVirtualMachinesPaginator(_ListAutonomousVirtualMachinesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListAutonomousVirtualMachines.html#Odb.Paginator.ListAutonomousVirtualMachines)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/paginators/#listautonomousvirtualmachinespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAutonomousVirtualMachinesInputPaginateTypeDef]
    ) -> AioPageIterator[ListAutonomousVirtualMachinesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListAutonomousVirtualMachines.html#Odb.Paginator.ListAutonomousVirtualMachines.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/paginators/#listautonomousvirtualmachinespaginator)
        """


if TYPE_CHECKING:
    _ListCloudAutonomousVmClustersPaginatorBase = AioPaginator[
        ListCloudAutonomousVmClustersOutputTypeDef
    ]
else:
    _ListCloudAutonomousVmClustersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCloudAutonomousVmClustersPaginator(_ListCloudAutonomousVmClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListCloudAutonomousVmClusters.html#Odb.Paginator.ListCloudAutonomousVmClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/paginators/#listcloudautonomousvmclusterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCloudAutonomousVmClustersInputPaginateTypeDef]
    ) -> AioPageIterator[ListCloudAutonomousVmClustersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListCloudAutonomousVmClusters.html#Odb.Paginator.ListCloudAutonomousVmClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/paginators/#listcloudautonomousvmclusterspaginator)
        """


if TYPE_CHECKING:
    _ListCloudExadataInfrastructuresPaginatorBase = AioPaginator[
        ListCloudExadataInfrastructuresOutputTypeDef
    ]
else:
    _ListCloudExadataInfrastructuresPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCloudExadataInfrastructuresPaginator(_ListCloudExadataInfrastructuresPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListCloudExadataInfrastructures.html#Odb.Paginator.ListCloudExadataInfrastructures)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/paginators/#listcloudexadatainfrastructurespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCloudExadataInfrastructuresInputPaginateTypeDef]
    ) -> AioPageIterator[ListCloudExadataInfrastructuresOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListCloudExadataInfrastructures.html#Odb.Paginator.ListCloudExadataInfrastructures.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/paginators/#listcloudexadatainfrastructurespaginator)
        """


if TYPE_CHECKING:
    _ListCloudVmClustersPaginatorBase = AioPaginator[ListCloudVmClustersOutputTypeDef]
else:
    _ListCloudVmClustersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCloudVmClustersPaginator(_ListCloudVmClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListCloudVmClusters.html#Odb.Paginator.ListCloudVmClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/paginators/#listcloudvmclusterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCloudVmClustersInputPaginateTypeDef]
    ) -> AioPageIterator[ListCloudVmClustersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListCloudVmClusters.html#Odb.Paginator.ListCloudVmClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/paginators/#listcloudvmclusterspaginator)
        """


if TYPE_CHECKING:
    _ListDbNodesPaginatorBase = AioPaginator[ListDbNodesOutputTypeDef]
else:
    _ListDbNodesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDbNodesPaginator(_ListDbNodesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListDbNodes.html#Odb.Paginator.ListDbNodes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/paginators/#listdbnodespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDbNodesInputPaginateTypeDef]
    ) -> AioPageIterator[ListDbNodesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListDbNodes.html#Odb.Paginator.ListDbNodes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/paginators/#listdbnodespaginator)
        """


if TYPE_CHECKING:
    _ListDbServersPaginatorBase = AioPaginator[ListDbServersOutputTypeDef]
else:
    _ListDbServersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDbServersPaginator(_ListDbServersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListDbServers.html#Odb.Paginator.ListDbServers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/paginators/#listdbserverspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDbServersInputPaginateTypeDef]
    ) -> AioPageIterator[ListDbServersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListDbServers.html#Odb.Paginator.ListDbServers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/paginators/#listdbserverspaginator)
        """


if TYPE_CHECKING:
    _ListDbSystemShapesPaginatorBase = AioPaginator[ListDbSystemShapesOutputTypeDef]
else:
    _ListDbSystemShapesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDbSystemShapesPaginator(_ListDbSystemShapesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListDbSystemShapes.html#Odb.Paginator.ListDbSystemShapes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/paginators/#listdbsystemshapespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDbSystemShapesInputPaginateTypeDef]
    ) -> AioPageIterator[ListDbSystemShapesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListDbSystemShapes.html#Odb.Paginator.ListDbSystemShapes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/paginators/#listdbsystemshapespaginator)
        """


if TYPE_CHECKING:
    _ListGiVersionsPaginatorBase = AioPaginator[ListGiVersionsOutputTypeDef]
else:
    _ListGiVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListGiVersionsPaginator(_ListGiVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListGiVersions.html#Odb.Paginator.ListGiVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/paginators/#listgiversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGiVersionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListGiVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListGiVersions.html#Odb.Paginator.ListGiVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/paginators/#listgiversionspaginator)
        """


if TYPE_CHECKING:
    _ListOdbNetworksPaginatorBase = AioPaginator[ListOdbNetworksOutputTypeDef]
else:
    _ListOdbNetworksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListOdbNetworksPaginator(_ListOdbNetworksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListOdbNetworks.html#Odb.Paginator.ListOdbNetworks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/paginators/#listodbnetworkspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOdbNetworksInputPaginateTypeDef]
    ) -> AioPageIterator[ListOdbNetworksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListOdbNetworks.html#Odb.Paginator.ListOdbNetworks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/paginators/#listodbnetworkspaginator)
        """


if TYPE_CHECKING:
    _ListOdbPeeringConnectionsPaginatorBase = AioPaginator[ListOdbPeeringConnectionsOutputTypeDef]
else:
    _ListOdbPeeringConnectionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListOdbPeeringConnectionsPaginator(_ListOdbPeeringConnectionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListOdbPeeringConnections.html#Odb.Paginator.ListOdbPeeringConnections)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/paginators/#listodbpeeringconnectionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOdbPeeringConnectionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListOdbPeeringConnectionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListOdbPeeringConnections.html#Odb.Paginator.ListOdbPeeringConnections.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/paginators/#listodbpeeringconnectionspaginator)
        """


if TYPE_CHECKING:
    _ListSystemVersionsPaginatorBase = AioPaginator[ListSystemVersionsOutputTypeDef]
else:
    _ListSystemVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSystemVersionsPaginator(_ListSystemVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListSystemVersions.html#Odb.Paginator.ListSystemVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/paginators/#listsystemversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSystemVersionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListSystemVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/paginator/ListSystemVersions.html#Odb.Paginator.ListSystemVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/paginators/#listsystemversionspaginator)
        """
