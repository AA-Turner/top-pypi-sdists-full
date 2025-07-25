"""
Type annotations for odb service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_odb.client import OdbClient

    session = get_session()
    async with session.create_client("odb") as client:
        client: OdbClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
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
from .type_defs import (
    AcceptMarketplaceRegistrationInputTypeDef,
    CreateCloudAutonomousVmClusterInputTypeDef,
    CreateCloudAutonomousVmClusterOutputTypeDef,
    CreateCloudExadataInfrastructureInputTypeDef,
    CreateCloudExadataInfrastructureOutputTypeDef,
    CreateCloudVmClusterInputTypeDef,
    CreateCloudVmClusterOutputTypeDef,
    CreateOdbNetworkInputTypeDef,
    CreateOdbNetworkOutputTypeDef,
    CreateOdbPeeringConnectionInputTypeDef,
    CreateOdbPeeringConnectionOutputTypeDef,
    DeleteCloudAutonomousVmClusterInputTypeDef,
    DeleteCloudExadataInfrastructureInputTypeDef,
    DeleteCloudVmClusterInputTypeDef,
    DeleteOdbNetworkInputTypeDef,
    DeleteOdbPeeringConnectionInputTypeDef,
    GetCloudAutonomousVmClusterInputTypeDef,
    GetCloudAutonomousVmClusterOutputTypeDef,
    GetCloudExadataInfrastructureInputTypeDef,
    GetCloudExadataInfrastructureOutputTypeDef,
    GetCloudExadataInfrastructureUnallocatedResourcesInputTypeDef,
    GetCloudExadataInfrastructureUnallocatedResourcesOutputTypeDef,
    GetCloudVmClusterInputTypeDef,
    GetCloudVmClusterOutputTypeDef,
    GetDbNodeInputTypeDef,
    GetDbNodeOutputTypeDef,
    GetDbServerInputTypeDef,
    GetDbServerOutputTypeDef,
    GetOciOnboardingStatusOutputTypeDef,
    GetOdbNetworkInputTypeDef,
    GetOdbNetworkOutputTypeDef,
    GetOdbPeeringConnectionInputTypeDef,
    GetOdbPeeringConnectionOutputTypeDef,
    ListAutonomousVirtualMachinesInputTypeDef,
    ListAutonomousVirtualMachinesOutputTypeDef,
    ListCloudAutonomousVmClustersInputTypeDef,
    ListCloudAutonomousVmClustersOutputTypeDef,
    ListCloudExadataInfrastructuresInputTypeDef,
    ListCloudExadataInfrastructuresOutputTypeDef,
    ListCloudVmClustersInputTypeDef,
    ListCloudVmClustersOutputTypeDef,
    ListDbNodesInputTypeDef,
    ListDbNodesOutputTypeDef,
    ListDbServersInputTypeDef,
    ListDbServersOutputTypeDef,
    ListDbSystemShapesInputTypeDef,
    ListDbSystemShapesOutputTypeDef,
    ListGiVersionsInputTypeDef,
    ListGiVersionsOutputTypeDef,
    ListOdbNetworksInputTypeDef,
    ListOdbNetworksOutputTypeDef,
    ListOdbPeeringConnectionsInputTypeDef,
    ListOdbPeeringConnectionsOutputTypeDef,
    ListSystemVersionsInputTypeDef,
    ListSystemVersionsOutputTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RebootDbNodeInputTypeDef,
    RebootDbNodeOutputTypeDef,
    StartDbNodeInputTypeDef,
    StartDbNodeOutputTypeDef,
    StopDbNodeInputTypeDef,
    StopDbNodeOutputTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateCloudExadataInfrastructureInputTypeDef,
    UpdateCloudExadataInfrastructureOutputTypeDef,
    UpdateOdbNetworkInputTypeDef,
    UpdateOdbNetworkOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("OdbClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class OdbClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb.html#Odb.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        OdbClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb.html#Odb.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#generate_presigned_url)
        """

    async def accept_marketplace_registration(
        self, **kwargs: Unpack[AcceptMarketplaceRegistrationInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Registers the Amazon Web Services Marketplace token for your Amazon Web
        Services account to activate your Oracle Database@Amazon Web Services
        subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/accept_marketplace_registration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#accept_marketplace_registration)
        """

    async def create_cloud_autonomous_vm_cluster(
        self, **kwargs: Unpack[CreateCloudAutonomousVmClusterInputTypeDef]
    ) -> CreateCloudAutonomousVmClusterOutputTypeDef:
        """
        Creates a new Autonomous VM cluster in the specified Exadata infrastructure.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/create_cloud_autonomous_vm_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#create_cloud_autonomous_vm_cluster)
        """

    async def create_cloud_exadata_infrastructure(
        self, **kwargs: Unpack[CreateCloudExadataInfrastructureInputTypeDef]
    ) -> CreateCloudExadataInfrastructureOutputTypeDef:
        """
        Creates an Exadata infrastructure.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/create_cloud_exadata_infrastructure.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#create_cloud_exadata_infrastructure)
        """

    async def create_cloud_vm_cluster(
        self, **kwargs: Unpack[CreateCloudVmClusterInputTypeDef]
    ) -> CreateCloudVmClusterOutputTypeDef:
        """
        Creates a VM cluster on the specified Exadata infrastructure.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/create_cloud_vm_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#create_cloud_vm_cluster)
        """

    async def create_odb_network(
        self, **kwargs: Unpack[CreateOdbNetworkInputTypeDef]
    ) -> CreateOdbNetworkOutputTypeDef:
        """
        Creates an ODB network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/create_odb_network.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#create_odb_network)
        """

    async def create_odb_peering_connection(
        self, **kwargs: Unpack[CreateOdbPeeringConnectionInputTypeDef]
    ) -> CreateOdbPeeringConnectionOutputTypeDef:
        """
        Creates a peering connection between an ODB network and either another ODB
        network or a customer-owned VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/create_odb_peering_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#create_odb_peering_connection)
        """

    async def delete_cloud_autonomous_vm_cluster(
        self, **kwargs: Unpack[DeleteCloudAutonomousVmClusterInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an Autonomous VM cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/delete_cloud_autonomous_vm_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#delete_cloud_autonomous_vm_cluster)
        """

    async def delete_cloud_exadata_infrastructure(
        self, **kwargs: Unpack[DeleteCloudExadataInfrastructureInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified Exadata infrastructure.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/delete_cloud_exadata_infrastructure.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#delete_cloud_exadata_infrastructure)
        """

    async def delete_cloud_vm_cluster(
        self, **kwargs: Unpack[DeleteCloudVmClusterInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified VM cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/delete_cloud_vm_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#delete_cloud_vm_cluster)
        """

    async def delete_odb_network(
        self, **kwargs: Unpack[DeleteOdbNetworkInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified ODB network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/delete_odb_network.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#delete_odb_network)
        """

    async def delete_odb_peering_connection(
        self, **kwargs: Unpack[DeleteOdbPeeringConnectionInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an ODB peering connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/delete_odb_peering_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#delete_odb_peering_connection)
        """

    async def get_cloud_autonomous_vm_cluster(
        self, **kwargs: Unpack[GetCloudAutonomousVmClusterInputTypeDef]
    ) -> GetCloudAutonomousVmClusterOutputTypeDef:
        """
        Gets information about a specific Autonomous VM cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/get_cloud_autonomous_vm_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#get_cloud_autonomous_vm_cluster)
        """

    async def get_cloud_exadata_infrastructure(
        self, **kwargs: Unpack[GetCloudExadataInfrastructureInputTypeDef]
    ) -> GetCloudExadataInfrastructureOutputTypeDef:
        """
        Returns information about the specified Exadata infrastructure.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/get_cloud_exadata_infrastructure.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#get_cloud_exadata_infrastructure)
        """

    async def get_cloud_exadata_infrastructure_unallocated_resources(
        self, **kwargs: Unpack[GetCloudExadataInfrastructureUnallocatedResourcesInputTypeDef]
    ) -> GetCloudExadataInfrastructureUnallocatedResourcesOutputTypeDef:
        """
        Retrieves information about unallocated resources in a specified Cloud Exadata
        Infrastructure.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/get_cloud_exadata_infrastructure_unallocated_resources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#get_cloud_exadata_infrastructure_unallocated_resources)
        """

    async def get_cloud_vm_cluster(
        self, **kwargs: Unpack[GetCloudVmClusterInputTypeDef]
    ) -> GetCloudVmClusterOutputTypeDef:
        """
        Returns information about the specified VM cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/get_cloud_vm_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#get_cloud_vm_cluster)
        """

    async def get_db_node(self, **kwargs: Unpack[GetDbNodeInputTypeDef]) -> GetDbNodeOutputTypeDef:
        """
        Returns information about the specified DB node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/get_db_node.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#get_db_node)
        """

    async def get_db_server(
        self, **kwargs: Unpack[GetDbServerInputTypeDef]
    ) -> GetDbServerOutputTypeDef:
        """
        Returns information about the specified database server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/get_db_server.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#get_db_server)
        """

    async def get_oci_onboarding_status(self) -> GetOciOnboardingStatusOutputTypeDef:
        """
        Returns the tenancy activation link and onboarding status for your Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/get_oci_onboarding_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#get_oci_onboarding_status)
        """

    async def get_odb_network(
        self, **kwargs: Unpack[GetOdbNetworkInputTypeDef]
    ) -> GetOdbNetworkOutputTypeDef:
        """
        Returns information about the specified ODB network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/get_odb_network.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#get_odb_network)
        """

    async def get_odb_peering_connection(
        self, **kwargs: Unpack[GetOdbPeeringConnectionInputTypeDef]
    ) -> GetOdbPeeringConnectionOutputTypeDef:
        """
        Retrieves information about an ODB peering connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/get_odb_peering_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#get_odb_peering_connection)
        """

    async def initialize_service(self) -> Dict[str, Any]:
        """
        Initializes the ODB service for the first time in an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/initialize_service.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#initialize_service)
        """

    async def list_autonomous_virtual_machines(
        self, **kwargs: Unpack[ListAutonomousVirtualMachinesInputTypeDef]
    ) -> ListAutonomousVirtualMachinesOutputTypeDef:
        """
        Lists all Autonomous VMs in an Autonomous VM cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/list_autonomous_virtual_machines.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#list_autonomous_virtual_machines)
        """

    async def list_cloud_autonomous_vm_clusters(
        self, **kwargs: Unpack[ListCloudAutonomousVmClustersInputTypeDef]
    ) -> ListCloudAutonomousVmClustersOutputTypeDef:
        """
        Lists all Autonomous VM clusters in a specified Cloud Exadata infrastructure.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/list_cloud_autonomous_vm_clusters.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#list_cloud_autonomous_vm_clusters)
        """

    async def list_cloud_exadata_infrastructures(
        self, **kwargs: Unpack[ListCloudExadataInfrastructuresInputTypeDef]
    ) -> ListCloudExadataInfrastructuresOutputTypeDef:
        """
        Returns information about the Exadata infrastructures owned by your Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/list_cloud_exadata_infrastructures.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#list_cloud_exadata_infrastructures)
        """

    async def list_cloud_vm_clusters(
        self, **kwargs: Unpack[ListCloudVmClustersInputTypeDef]
    ) -> ListCloudVmClustersOutputTypeDef:
        """
        Returns information about the VM clusters owned by your Amazon Web Services
        account or only the ones on the specified Exadata infrastructure.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/list_cloud_vm_clusters.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#list_cloud_vm_clusters)
        """

    async def list_db_nodes(
        self, **kwargs: Unpack[ListDbNodesInputTypeDef]
    ) -> ListDbNodesOutputTypeDef:
        """
        Returns information about the DB nodes for the specified VM cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/list_db_nodes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#list_db_nodes)
        """

    async def list_db_servers(
        self, **kwargs: Unpack[ListDbServersInputTypeDef]
    ) -> ListDbServersOutputTypeDef:
        """
        Returns information about the database servers that belong to the specified
        Exadata infrastructure.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/list_db_servers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#list_db_servers)
        """

    async def list_db_system_shapes(
        self, **kwargs: Unpack[ListDbSystemShapesInputTypeDef]
    ) -> ListDbSystemShapesOutputTypeDef:
        """
        Returns information about the shapes that are available for an Exadata
        infrastructure.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/list_db_system_shapes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#list_db_system_shapes)
        """

    async def list_gi_versions(
        self, **kwargs: Unpack[ListGiVersionsInputTypeDef]
    ) -> ListGiVersionsOutputTypeDef:
        """
        Returns information about Oracle Grid Infrastructure (GI) software versions
        that are available for a VM cluster for the specified shape.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/list_gi_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#list_gi_versions)
        """

    async def list_odb_networks(
        self, **kwargs: Unpack[ListOdbNetworksInputTypeDef]
    ) -> ListOdbNetworksOutputTypeDef:
        """
        Returns information about the ODB networks owned by your Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/list_odb_networks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#list_odb_networks)
        """

    async def list_odb_peering_connections(
        self, **kwargs: Unpack[ListOdbPeeringConnectionsInputTypeDef]
    ) -> ListOdbPeeringConnectionsOutputTypeDef:
        """
        Lists all ODB peering connections or those associated with a specific ODB
        network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/list_odb_peering_connections.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#list_odb_peering_connections)
        """

    async def list_system_versions(
        self, **kwargs: Unpack[ListSystemVersionsInputTypeDef]
    ) -> ListSystemVersionsOutputTypeDef:
        """
        Returns information about the system versions that are available for a VM
        cluster for the specified <code>giVersion</code> and <code>shape</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/list_system_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#list_system_versions)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns information about the tags applied to this resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#list_tags_for_resource)
        """

    async def reboot_db_node(
        self, **kwargs: Unpack[RebootDbNodeInputTypeDef]
    ) -> RebootDbNodeOutputTypeDef:
        """
        Reboots the specified DB node in a VM cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/reboot_db_node.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#reboot_db_node)
        """

    async def start_db_node(
        self, **kwargs: Unpack[StartDbNodeInputTypeDef]
    ) -> StartDbNodeOutputTypeDef:
        """
        Starts the specified DB node in a VM cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/start_db_node.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#start_db_node)
        """

    async def stop_db_node(
        self, **kwargs: Unpack[StopDbNodeInputTypeDef]
    ) -> StopDbNodeOutputTypeDef:
        """
        Stops the specified DB node in a VM cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/stop_db_node.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#stop_db_node)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Applies tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#untag_resource)
        """

    async def update_cloud_exadata_infrastructure(
        self, **kwargs: Unpack[UpdateCloudExadataInfrastructureInputTypeDef]
    ) -> UpdateCloudExadataInfrastructureOutputTypeDef:
        """
        Updates the properties of an Exadata infrastructure resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/update_cloud_exadata_infrastructure.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#update_cloud_exadata_infrastructure)
        """

    async def update_odb_network(
        self, **kwargs: Unpack[UpdateOdbNetworkInputTypeDef]
    ) -> UpdateOdbNetworkOutputTypeDef:
        """
        Updates properties of a specified ODB network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/update_odb_network.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#update_odb_network)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_autonomous_virtual_machines"]
    ) -> ListAutonomousVirtualMachinesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_cloud_autonomous_vm_clusters"]
    ) -> ListCloudAutonomousVmClustersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_cloud_exadata_infrastructures"]
    ) -> ListCloudExadataInfrastructuresPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_cloud_vm_clusters"]
    ) -> ListCloudVmClustersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_db_nodes"]
    ) -> ListDbNodesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_db_servers"]
    ) -> ListDbServersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_db_system_shapes"]
    ) -> ListDbSystemShapesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_gi_versions"]
    ) -> ListGiVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_odb_networks"]
    ) -> ListOdbNetworksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_odb_peering_connections"]
    ) -> ListOdbPeeringConnectionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_system_versions"]
    ) -> ListSystemVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb.html#Odb.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/odb.html#Odb.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_odb/client/)
        """
