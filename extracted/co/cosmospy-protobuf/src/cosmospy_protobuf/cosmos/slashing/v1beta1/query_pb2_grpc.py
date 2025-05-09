"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from ....cosmos.slashing.v1beta1 import query_pb2 as cosmos_dot_slashing_dot_v1beta1_dot_query__pb2

class QueryStub(object):
    """Query provides defines the gRPC querier service
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Params = channel.unary_unary('/cosmos.slashing.v1beta1.Query/Params', request_serializer=cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QueryParamsRequest.SerializeToString, response_deserializer=cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QueryParamsResponse.FromString)
        self.SigningInfo = channel.unary_unary('/cosmos.slashing.v1beta1.Query/SigningInfo', request_serializer=cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QuerySigningInfoRequest.SerializeToString, response_deserializer=cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QuerySigningInfoResponse.FromString)
        self.SigningInfos = channel.unary_unary('/cosmos.slashing.v1beta1.Query/SigningInfos', request_serializer=cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QuerySigningInfosRequest.SerializeToString, response_deserializer=cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QuerySigningInfosResponse.FromString)

class QueryServicer(object):
    """Query provides defines the gRPC querier service
    """

    def Params(self, request, context):
        """Params queries the parameters of slashing module
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SigningInfo(self, request, context):
        """SigningInfo queries the signing info of given cons address
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SigningInfos(self, request, context):
        """SigningInfos queries signing info of all validators
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_QueryServicer_to_server(servicer, server):
    rpc_method_handlers = {'Params': grpc.unary_unary_rpc_method_handler(servicer.Params, request_deserializer=cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QueryParamsRequest.FromString, response_serializer=cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QueryParamsResponse.SerializeToString), 'SigningInfo': grpc.unary_unary_rpc_method_handler(servicer.SigningInfo, request_deserializer=cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QuerySigningInfoRequest.FromString, response_serializer=cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QuerySigningInfoResponse.SerializeToString), 'SigningInfos': grpc.unary_unary_rpc_method_handler(servicer.SigningInfos, request_deserializer=cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QuerySigningInfosRequest.FromString, response_serializer=cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QuerySigningInfosResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('cosmos.slashing.v1beta1.Query', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class Query(object):
    """Query provides defines the gRPC querier service
    """

    @staticmethod
    def Params(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cosmos.slashing.v1beta1.Query/Params', cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QueryParamsRequest.SerializeToString, cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QueryParamsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SigningInfo(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cosmos.slashing.v1beta1.Query/SigningInfo', cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QuerySigningInfoRequest.SerializeToString, cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QuerySigningInfoResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SigningInfos(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cosmos.slashing.v1beta1.Query/SigningInfos', cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QuerySigningInfosRequest.SerializeToString, cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QuerySigningInfosResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)