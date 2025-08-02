import pb.v1alpha1.application_auth_connection_service_pb2_grpc as auth_service_grpc
import pb.v1alpha1.application_auth_connection_service_pb2 as auth_service_pb2

from va.store.orby.orby_client import get_orby_client


def get_connection(connection_id: str):
    orby_client = get_orby_client()
    auth_stub = auth_service_grpc.ApplicationAuthConnectionServiceStub(
        orby_client._grpc_channel
    )
    request = auth_service_pb2.GetConnectionRequest(id=connection_id)
    response = orby_client.call_grpc_channel(auth_stub.GetConnection, request)
    return response.connection
