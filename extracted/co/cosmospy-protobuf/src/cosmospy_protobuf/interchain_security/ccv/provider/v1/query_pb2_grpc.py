"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from .....interchain_security.ccv.provider.v1 import query_pb2 as interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2

class QueryStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.QueryConsumerGenesis = channel.unary_unary('/interchain_security.ccv.provider.v1.Query/QueryConsumerGenesis', request_serializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryConsumerGenesisRequest.SerializeToString, response_deserializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryConsumerGenesisResponse.FromString)
        self.QueryConsumerChains = channel.unary_unary('/interchain_security.ccv.provider.v1.Query/QueryConsumerChains', request_serializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryConsumerChainsRequest.SerializeToString, response_deserializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryConsumerChainsResponse.FromString)
        self.QueryConsumerChainStarts = channel.unary_unary('/interchain_security.ccv.provider.v1.Query/QueryConsumerChainStarts', request_serializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryConsumerChainStartProposalsRequest.SerializeToString, response_deserializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryConsumerChainStartProposalsResponse.FromString)
        self.QueryConsumerChainStops = channel.unary_unary('/interchain_security.ccv.provider.v1.Query/QueryConsumerChainStops', request_serializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryConsumerChainStopProposalsRequest.SerializeToString, response_deserializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryConsumerChainStopProposalsResponse.FromString)
        self.QueryValidatorConsumerAddr = channel.unary_unary('/interchain_security.ccv.provider.v1.Query/QueryValidatorConsumerAddr', request_serializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryValidatorConsumerAddrRequest.SerializeToString, response_deserializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryValidatorConsumerAddrResponse.FromString)
        self.QueryValidatorProviderAddr = channel.unary_unary('/interchain_security.ccv.provider.v1.Query/QueryValidatorProviderAddr', request_serializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryValidatorProviderAddrRequest.SerializeToString, response_deserializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryValidatorProviderAddrResponse.FromString)
        self.QueryThrottleState = channel.unary_unary('/interchain_security.ccv.provider.v1.Query/QueryThrottleState', request_serializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryThrottleStateRequest.SerializeToString, response_deserializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryThrottleStateResponse.FromString)
        self.QueryThrottledConsumerPacketData = channel.unary_unary('/interchain_security.ccv.provider.v1.Query/QueryThrottledConsumerPacketData', request_serializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryThrottledConsumerPacketDataRequest.SerializeToString, response_deserializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryThrottledConsumerPacketDataResponse.FromString)
        self.QueryRegisteredConsumerRewardDenoms = channel.unary_unary('/interchain_security.ccv.provider.v1.Query/QueryRegisteredConsumerRewardDenoms', request_serializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryRegisteredConsumerRewardDenomsRequest.SerializeToString, response_deserializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryRegisteredConsumerRewardDenomsResponse.FromString)

class QueryServicer(object):
    """Missing associated documentation comment in .proto file."""

    def QueryConsumerGenesis(self, request, context):
        """ConsumerGenesis queries the genesis state needed to start a consumer chain
        whose proposal has been accepted
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryConsumerChains(self, request, context):
        """ConsumerChains queries active consumer chains supported by the provider
        chain
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryConsumerChainStarts(self, request, context):
        """QueryConsumerChainStarts queries consumer chain start proposals.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryConsumerChainStops(self, request, context):
        """QueryConsumerChainStops queries consumer chain stop proposals.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryValidatorConsumerAddr(self, request, context):
        """QueryValidatorConsumerAddr queries the address
        assigned by a validator for a consumer chain.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryValidatorProviderAddr(self, request, context):
        """QueryProviderAddr returns the provider chain validator
        given a consumer chain validator address
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryThrottleState(self, request, context):
        """QueryThrottleState returns the main on-chain state relevant to currently throttled slash packets 
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryThrottledConsumerPacketData(self, request, context):
        """QueryThrottledConsumerPacketData returns a list of pending packet data instances
        (slash packet and vsc matured) for a single consumer chain
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryRegisteredConsumerRewardDenoms(self, request, context):
        """QueryRegisteredConsumerRewardDenoms returns a list of consumer reward denoms that are registered
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_QueryServicer_to_server(servicer, server):
    rpc_method_handlers = {'QueryConsumerGenesis': grpc.unary_unary_rpc_method_handler(servicer.QueryConsumerGenesis, request_deserializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryConsumerGenesisRequest.FromString, response_serializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryConsumerGenesisResponse.SerializeToString), 'QueryConsumerChains': grpc.unary_unary_rpc_method_handler(servicer.QueryConsumerChains, request_deserializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryConsumerChainsRequest.FromString, response_serializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryConsumerChainsResponse.SerializeToString), 'QueryConsumerChainStarts': grpc.unary_unary_rpc_method_handler(servicer.QueryConsumerChainStarts, request_deserializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryConsumerChainStartProposalsRequest.FromString, response_serializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryConsumerChainStartProposalsResponse.SerializeToString), 'QueryConsumerChainStops': grpc.unary_unary_rpc_method_handler(servicer.QueryConsumerChainStops, request_deserializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryConsumerChainStopProposalsRequest.FromString, response_serializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryConsumerChainStopProposalsResponse.SerializeToString), 'QueryValidatorConsumerAddr': grpc.unary_unary_rpc_method_handler(servicer.QueryValidatorConsumerAddr, request_deserializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryValidatorConsumerAddrRequest.FromString, response_serializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryValidatorConsumerAddrResponse.SerializeToString), 'QueryValidatorProviderAddr': grpc.unary_unary_rpc_method_handler(servicer.QueryValidatorProviderAddr, request_deserializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryValidatorProviderAddrRequest.FromString, response_serializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryValidatorProviderAddrResponse.SerializeToString), 'QueryThrottleState': grpc.unary_unary_rpc_method_handler(servicer.QueryThrottleState, request_deserializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryThrottleStateRequest.FromString, response_serializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryThrottleStateResponse.SerializeToString), 'QueryThrottledConsumerPacketData': grpc.unary_unary_rpc_method_handler(servicer.QueryThrottledConsumerPacketData, request_deserializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryThrottledConsumerPacketDataRequest.FromString, response_serializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryThrottledConsumerPacketDataResponse.SerializeToString), 'QueryRegisteredConsumerRewardDenoms': grpc.unary_unary_rpc_method_handler(servicer.QueryRegisteredConsumerRewardDenoms, request_deserializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryRegisteredConsumerRewardDenomsRequest.FromString, response_serializer=interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryRegisteredConsumerRewardDenomsResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('interchain_security.ccv.provider.v1.Query', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class Query(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def QueryConsumerGenesis(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/interchain_security.ccv.provider.v1.Query/QueryConsumerGenesis', interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryConsumerGenesisRequest.SerializeToString, interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryConsumerGenesisResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryConsumerChains(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/interchain_security.ccv.provider.v1.Query/QueryConsumerChains', interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryConsumerChainsRequest.SerializeToString, interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryConsumerChainsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryConsumerChainStarts(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/interchain_security.ccv.provider.v1.Query/QueryConsumerChainStarts', interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryConsumerChainStartProposalsRequest.SerializeToString, interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryConsumerChainStartProposalsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryConsumerChainStops(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/interchain_security.ccv.provider.v1.Query/QueryConsumerChainStops', interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryConsumerChainStopProposalsRequest.SerializeToString, interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryConsumerChainStopProposalsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryValidatorConsumerAddr(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/interchain_security.ccv.provider.v1.Query/QueryValidatorConsumerAddr', interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryValidatorConsumerAddrRequest.SerializeToString, interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryValidatorConsumerAddrResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryValidatorProviderAddr(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/interchain_security.ccv.provider.v1.Query/QueryValidatorProviderAddr', interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryValidatorProviderAddrRequest.SerializeToString, interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryValidatorProviderAddrResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryThrottleState(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/interchain_security.ccv.provider.v1.Query/QueryThrottleState', interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryThrottleStateRequest.SerializeToString, interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryThrottleStateResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryThrottledConsumerPacketData(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/interchain_security.ccv.provider.v1.Query/QueryThrottledConsumerPacketData', interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryThrottledConsumerPacketDataRequest.SerializeToString, interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryThrottledConsumerPacketDataResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryRegisteredConsumerRewardDenoms(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/interchain_security.ccv.provider.v1.Query/QueryRegisteredConsumerRewardDenoms', interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryRegisteredConsumerRewardDenomsRequest.SerializeToString, interchain__security_dot_ccv_dot_provider_dot_v1_dot_query__pb2.QueryRegisteredConsumerRewardDenomsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)