"""Cluster V2 API client.

Provides wrapper methods for the Cluster V2 gRPC service with proper error handling.
"""

from _qwak_proto.qwak.administration.cluster.v2.cluster_pb2 import (
    ClusterSpec,
)
from _qwak_proto.qwak.administration.cluster.v2.cluster_service_pb2 import (
    CreateClusterCreationRequestRequest,
    CreateClusterCreationRequestResponse,
    DeleteClusterRequest,
    DeleteClusterResponse,
    GetClusterRequest,
    GetClusterResponse,
    GetClusterStateRequest,
    GetClusterStateResponse,
    ListClustersRequest,
    ListClustersResponse,
    UpdateClusterConfigurationRequest,
    UpdateClusterConfigurationResponse,
)
from _qwak_proto.qwak.administration.cluster.v2.cluster_service_pb2_grpc import (
    ClusterServiceStub,
)
from dependency_injector.wiring import Provide
from qwak.inner.di_configuration import QwakContainer
from qwak.inner.tool.grpc.grpc_try_wrapping import grpc_try_catch_wrapper


class ClusterV2Client:
    """Client for interacting with the Cluster V2 API.

    This client wraps the gRPC stub and provides methods with proper error handling
    using the grpc_try_catch_wrapper decorator.
    """

    def __init__(self, grpc_channel=Provide[QwakContainer.core_grpc_channel]):
        self.__cluster_service = ClusterServiceStub(grpc_channel)

    @grpc_try_catch_wrapper("Failed to create cluster")
    def create_cluster(
        self, cluster_spec: ClusterSpec
    ) -> CreateClusterCreationRequestResponse:
        """Create a new cluster.

        Args:
            cluster_spec: The cluster specification.

        Returns:
            CreateClusterCreationRequestResponse with the request_id.
        """
        request = CreateClusterCreationRequestRequest(cluster_spec=cluster_spec)
        return self.__cluster_service.CreateClusterCreationRequest(request)

    @grpc_try_catch_wrapper("Failed to get cluster state for request {request_id}")
    def get_cluster_state(self, request_id: str) -> GetClusterStateResponse:
        """Get cluster state by request ID.

        Args:
            request_id: The request ID from create_cluster.

        Returns:
            GetClusterStateResponse with the cluster state.
        """
        request = GetClusterStateRequest(request_id=request_id)
        return self.__cluster_service.GetClusterState(request)

    @grpc_try_catch_wrapper("Failed to get cluster {cluster_id}")
    def get_cluster(self, cluster_id: str) -> GetClusterResponse:
        """Get cluster by ID.

        Args:
            cluster_id: The cluster ID.

        Returns:
            GetClusterResponse with the cluster state.
        """
        request = GetClusterRequest(cluster_id=cluster_id)
        return self.__cluster_service.GetCluster(request)

    @grpc_try_catch_wrapper("Failed to list clusters")
    def list_clusters(self) -> ListClustersResponse:
        """List all clusters.

        Returns:
            ListClustersResponse with list of clusters.
        """
        request = ListClustersRequest()
        return self.__cluster_service.ListClusters(request)

    @grpc_try_catch_wrapper("Failed to update cluster {cluster_id}")
    def update_cluster(
        self, cluster_id: str, cluster_spec: ClusterSpec
    ) -> UpdateClusterConfigurationResponse:
        """Update cluster configuration.

        Args:
            cluster_id: The cluster ID to update.
            cluster_spec: The updated cluster specification.

        Returns:
            UpdateClusterConfigurationResponse with the request_id.
        """
        request = UpdateClusterConfigurationRequest(
            cluster_id=cluster_id,
            cluster_spec=cluster_spec,
        )
        return self.__cluster_service.UpdateClusterConfiguration(request)

    @grpc_try_catch_wrapper("Failed to delete cluster {cluster_id}")
    def delete_cluster(self, cluster_id: str) -> DeleteClusterResponse:
        """Delete cluster by ID.

        Args:
            cluster_id: The cluster ID to delete.

        Returns:
            DeleteClusterResponse with the request_id.
        """
        request = DeleteClusterRequest(cluster_id=cluster_id)
        return self.__cluster_service.DeleteCluster(request)
