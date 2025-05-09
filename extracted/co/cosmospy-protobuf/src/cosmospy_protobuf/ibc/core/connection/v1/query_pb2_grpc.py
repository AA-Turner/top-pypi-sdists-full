"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from .....ibc.core.connection.v1 import query_pb2 as ibc_dot_core_dot_connection_dot_v1_dot_query__pb2

class QueryStub(object):
    """Query provides defines the gRPC querier service
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Connection = channel.unary_unary('/ibc.core.connection.v1.Query/Connection', request_serializer=ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryConnectionRequest.SerializeToString, response_deserializer=ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryConnectionResponse.FromString)
        self.Connections = channel.unary_unary('/ibc.core.connection.v1.Query/Connections', request_serializer=ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryConnectionsRequest.SerializeToString, response_deserializer=ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryConnectionsResponse.FromString)
        self.ClientConnections = channel.unary_unary('/ibc.core.connection.v1.Query/ClientConnections', request_serializer=ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryClientConnectionsRequest.SerializeToString, response_deserializer=ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryClientConnectionsResponse.FromString)
        self.ConnectionClientState = channel.unary_unary('/ibc.core.connection.v1.Query/ConnectionClientState', request_serializer=ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryConnectionClientStateRequest.SerializeToString, response_deserializer=ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryConnectionClientStateResponse.FromString)
        self.ConnectionConsensusState = channel.unary_unary('/ibc.core.connection.v1.Query/ConnectionConsensusState', request_serializer=ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryConnectionConsensusStateRequest.SerializeToString, response_deserializer=ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryConnectionConsensusStateResponse.FromString)

class QueryServicer(object):
    """Query provides defines the gRPC querier service
    """

    def Connection(self, request, context):
        """Connection queries an IBC connection end.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Connections(self, request, context):
        """Connections queries all the IBC connections of a chain.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClientConnections(self, request, context):
        """ClientConnections queries the connection paths associated with a client
        state.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ConnectionClientState(self, request, context):
        """ConnectionClientState queries the client state associated with the
        connection.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ConnectionConsensusState(self, request, context):
        """ConnectionConsensusState queries the consensus state associated with the
        connection.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_QueryServicer_to_server(servicer, server):
    rpc_method_handlers = {'Connection': grpc.unary_unary_rpc_method_handler(servicer.Connection, request_deserializer=ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryConnectionRequest.FromString, response_serializer=ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryConnectionResponse.SerializeToString), 'Connections': grpc.unary_unary_rpc_method_handler(servicer.Connections, request_deserializer=ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryConnectionsRequest.FromString, response_serializer=ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryConnectionsResponse.SerializeToString), 'ClientConnections': grpc.unary_unary_rpc_method_handler(servicer.ClientConnections, request_deserializer=ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryClientConnectionsRequest.FromString, response_serializer=ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryClientConnectionsResponse.SerializeToString), 'ConnectionClientState': grpc.unary_unary_rpc_method_handler(servicer.ConnectionClientState, request_deserializer=ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryConnectionClientStateRequest.FromString, response_serializer=ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryConnectionClientStateResponse.SerializeToString), 'ConnectionConsensusState': grpc.unary_unary_rpc_method_handler(servicer.ConnectionConsensusState, request_deserializer=ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryConnectionConsensusStateRequest.FromString, response_serializer=ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryConnectionConsensusStateResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('ibc.core.connection.v1.Query', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class Query(object):
    """Query provides defines the gRPC querier service
    """

    @staticmethod
    def Connection(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ibc.core.connection.v1.Query/Connection', ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryConnectionRequest.SerializeToString, ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryConnectionResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Connections(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ibc.core.connection.v1.Query/Connections', ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryConnectionsRequest.SerializeToString, ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryConnectionsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ClientConnections(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ibc.core.connection.v1.Query/ClientConnections', ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryClientConnectionsRequest.SerializeToString, ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryClientConnectionsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ConnectionClientState(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ibc.core.connection.v1.Query/ConnectionClientState', ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryConnectionClientStateRequest.SerializeToString, ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryConnectionClientStateResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ConnectionConsensusState(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ibc.core.connection.v1.Query/ConnectionConsensusState', ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryConnectionConsensusStateRequest.SerializeToString, ibc_dot_core_dot_connection_dot_v1_dot_query__pb2.QueryConnectionConsensusStateResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)