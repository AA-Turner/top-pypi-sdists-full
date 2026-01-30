from typing import Optional

import grpc

from _qwak_proto.qwak.administration.cluster.v2.cluster_pb2 import (
    ClusterState,
)
from _qwak_proto.qwak.administration.cluster.v2.cluster_service_pb2 import (
    CreateClusterCreationRequestResponse,
    DeleteClusterResponse,
    GetClusterResponse,
    GetClusterStateResponse,
    ListClustersResponse,
    UpdateClusterConfigurationResponse,
)
from _qwak_proto.qwak.administration.cluster.v2.cluster_service_pb2_grpc import (
    ClusterServiceServicer,
)


class ClusterV2ServiceMock(ClusterServiceServicer):
    def __init__(self):
        super().__init__()
        self.__create_cluster_response: Optional[
            CreateClusterCreationRequestResponse
        ] = None
        self.__create_cluster_error: Optional[grpc.StatusCode] = None

        self.__get_cluster_state_response: Optional[GetClusterStateResponse] = None
        self.__get_cluster_state_error: Optional[grpc.StatusCode] = None

        self.__get_cluster_response: Optional[GetClusterResponse] = None
        self.__get_cluster_error: Optional[grpc.StatusCode] = None

        self.__list_clusters_response: Optional[ListClustersResponse] = None
        self.__list_clusters_error: Optional[grpc.StatusCode] = None

        self.__update_cluster_response: Optional[UpdateClusterConfigurationResponse] = (
            None
        )
        self.__update_cluster_error: Optional[grpc.StatusCode] = None

        self.__delete_cluster_response: Optional[DeleteClusterResponse] = None
        self.__delete_cluster_error: Optional[grpc.StatusCode] = None

    def given_create_cluster(
        self,
        response: Optional[CreateClusterCreationRequestResponse] = None,
        error_code: Optional[grpc.StatusCode] = None,
    ):
        self.__create_cluster_response = response
        self.__create_cluster_error = error_code

    def given_get_cluster_state(
        self,
        response: Optional[GetClusterStateResponse] = None,
        error_code: Optional[grpc.StatusCode] = None,
    ):
        self.__get_cluster_state_response = response
        self.__get_cluster_state_error = error_code

    def given_get_cluster(
        self,
        response: Optional[GetClusterResponse] = None,
        error_code: Optional[grpc.StatusCode] = None,
    ):
        self.__get_cluster_response = response
        self.__get_cluster_error = error_code

    def given_list_clusters(
        self,
        response: Optional[ListClustersResponse] = None,
        error_code: Optional[grpc.StatusCode] = None,
    ):
        self.__list_clusters_response = response
        self.__list_clusters_error = error_code

    def given_update_cluster(
        self,
        response: Optional[UpdateClusterConfigurationResponse] = None,
        error_code: Optional[grpc.StatusCode] = None,
    ):
        self.__update_cluster_response = response
        self.__update_cluster_error = error_code

    def given_delete_cluster(
        self,
        response: Optional[DeleteClusterResponse] = None,
        error_code: Optional[grpc.StatusCode] = None,
    ):
        self.__delete_cluster_response = response
        self.__delete_cluster_error = error_code

    def CreateClusterCreationRequest(self, request, context):
        if self.__create_cluster_error:
            context.set_code(self.__create_cluster_error)
            context.set_details("Failed to create cluster")
            return CreateClusterCreationRequestResponse()
        if self.__create_cluster_response:
            return self.__create_cluster_response
        return CreateClusterCreationRequestResponse(request_id="mock-request-id")

    def GetClusterState(self, request, context):
        if self.__get_cluster_state_error:
            context.set_code(self.__get_cluster_state_error)
            context.set_details("Failed to get cluster state")
            return GetClusterStateResponse()
        if self.__get_cluster_state_response:
            return self.__get_cluster_state_response
        return GetClusterStateResponse(cluster_state=ClusterState())

    def GetCluster(self, request, context):
        if self.__get_cluster_error:
            context.set_code(self.__get_cluster_error)
            context.set_details("Failed to get cluster")
            return GetClusterResponse()
        if self.__get_cluster_response:
            return self.__get_cluster_response
        return GetClusterResponse(cluster_state=ClusterState())

    def ListClusters(self, request, context):
        if self.__list_clusters_error:
            context.set_code(self.__list_clusters_error)
            context.set_details("Failed to list clusters")
            return ListClustersResponse()
        if self.__list_clusters_response:
            return self.__list_clusters_response
        return ListClustersResponse()

    def UpdateClusterConfiguration(self, request, context):
        if self.__update_cluster_error:
            context.set_code(self.__update_cluster_error)
            context.set_details("Failed to update cluster")
            return UpdateClusterConfigurationResponse()
        if self.__update_cluster_response:
            return self.__update_cluster_response
        return UpdateClusterConfigurationResponse(request_id="mock-request-id")

    def DeleteCluster(self, request, context):
        if self.__delete_cluster_error:
            context.set_code(self.__delete_cluster_error)
            context.set_details("Failed to delete cluster")
            return DeleteClusterResponse()
        if self.__delete_cluster_response:
            return self.__delete_cluster_response
        return DeleteClusterResponse(request_id="mock-request-id")
