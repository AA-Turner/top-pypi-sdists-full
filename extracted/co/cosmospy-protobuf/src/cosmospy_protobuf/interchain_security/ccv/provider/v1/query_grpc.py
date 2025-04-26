import abc
import typing
import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server
from ..... import google
from ..... import gogoproto
import google.protobuf.timestamp_pb2
from ..... import interchain_security

class QueryBase(abc.ABC):

    @abc.abstractmethod
    async def QueryConsumerGenesis(self, stream: 'grpclib.server.Stream[interchain_security.ccv.provider.v1.query_pb2.QueryConsumerGenesisRequest, interchain_security.ccv.provider.v1.query_pb2.QueryConsumerGenesisResponse]') -> None:
        pass

    @abc.abstractmethod
    async def QueryConsumerChains(self, stream: 'grpclib.server.Stream[interchain_security.ccv.provider.v1.query_pb2.QueryConsumerChainsRequest, interchain_security.ccv.provider.v1.query_pb2.QueryConsumerChainsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def QueryConsumerChainStarts(self, stream: 'grpclib.server.Stream[interchain_security.ccv.provider.v1.query_pb2.QueryConsumerChainStartProposalsRequest, interchain_security.ccv.provider.v1.query_pb2.QueryConsumerChainStartProposalsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def QueryConsumerChainStops(self, stream: 'grpclib.server.Stream[interchain_security.ccv.provider.v1.query_pb2.QueryConsumerChainStopProposalsRequest, interchain_security.ccv.provider.v1.query_pb2.QueryConsumerChainStopProposalsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def QueryValidatorConsumerAddr(self, stream: 'grpclib.server.Stream[interchain_security.ccv.provider.v1.query_pb2.QueryValidatorConsumerAddrRequest, interchain_security.ccv.provider.v1.query_pb2.QueryValidatorConsumerAddrResponse]') -> None:
        pass

    @abc.abstractmethod
    async def QueryValidatorProviderAddr(self, stream: 'grpclib.server.Stream[interchain_security.ccv.provider.v1.query_pb2.QueryValidatorProviderAddrRequest, interchain_security.ccv.provider.v1.query_pb2.QueryValidatorProviderAddrResponse]') -> None:
        pass

    @abc.abstractmethod
    async def QueryThrottleState(self, stream: 'grpclib.server.Stream[interchain_security.ccv.provider.v1.query_pb2.QueryThrottleStateRequest, interchain_security.ccv.provider.v1.query_pb2.QueryThrottleStateResponse]') -> None:
        pass

    @abc.abstractmethod
    async def QueryThrottledConsumerPacketData(self, stream: 'grpclib.server.Stream[interchain_security.ccv.provider.v1.query_pb2.QueryThrottledConsumerPacketDataRequest, interchain_security.ccv.provider.v1.query_pb2.QueryThrottledConsumerPacketDataResponse]') -> None:
        pass

    @abc.abstractmethod
    async def QueryRegisteredConsumerRewardDenoms(self, stream: 'grpclib.server.Stream[interchain_security.ccv.provider.v1.query_pb2.QueryRegisteredConsumerRewardDenomsRequest, interchain_security.ccv.provider.v1.query_pb2.QueryRegisteredConsumerRewardDenomsResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/interchain_security.ccv.provider.v1.Query/QueryConsumerGenesis': grpclib.const.Handler(self.QueryConsumerGenesis, grpclib.const.Cardinality.UNARY_UNARY, interchain_security.ccv.provider.v1.query_pb2.QueryConsumerGenesisRequest, interchain_security.ccv.provider.v1.query_pb2.QueryConsumerGenesisResponse), '/interchain_security.ccv.provider.v1.Query/QueryConsumerChains': grpclib.const.Handler(self.QueryConsumerChains, grpclib.const.Cardinality.UNARY_UNARY, interchain_security.ccv.provider.v1.query_pb2.QueryConsumerChainsRequest, interchain_security.ccv.provider.v1.query_pb2.QueryConsumerChainsResponse), '/interchain_security.ccv.provider.v1.Query/QueryConsumerChainStarts': grpclib.const.Handler(self.QueryConsumerChainStarts, grpclib.const.Cardinality.UNARY_UNARY, interchain_security.ccv.provider.v1.query_pb2.QueryConsumerChainStartProposalsRequest, interchain_security.ccv.provider.v1.query_pb2.QueryConsumerChainStartProposalsResponse), '/interchain_security.ccv.provider.v1.Query/QueryConsumerChainStops': grpclib.const.Handler(self.QueryConsumerChainStops, grpclib.const.Cardinality.UNARY_UNARY, interchain_security.ccv.provider.v1.query_pb2.QueryConsumerChainStopProposalsRequest, interchain_security.ccv.provider.v1.query_pb2.QueryConsumerChainStopProposalsResponse), '/interchain_security.ccv.provider.v1.Query/QueryValidatorConsumerAddr': grpclib.const.Handler(self.QueryValidatorConsumerAddr, grpclib.const.Cardinality.UNARY_UNARY, interchain_security.ccv.provider.v1.query_pb2.QueryValidatorConsumerAddrRequest, interchain_security.ccv.provider.v1.query_pb2.QueryValidatorConsumerAddrResponse), '/interchain_security.ccv.provider.v1.Query/QueryValidatorProviderAddr': grpclib.const.Handler(self.QueryValidatorProviderAddr, grpclib.const.Cardinality.UNARY_UNARY, interchain_security.ccv.provider.v1.query_pb2.QueryValidatorProviderAddrRequest, interchain_security.ccv.provider.v1.query_pb2.QueryValidatorProviderAddrResponse), '/interchain_security.ccv.provider.v1.Query/QueryThrottleState': grpclib.const.Handler(self.QueryThrottleState, grpclib.const.Cardinality.UNARY_UNARY, interchain_security.ccv.provider.v1.query_pb2.QueryThrottleStateRequest, interchain_security.ccv.provider.v1.query_pb2.QueryThrottleStateResponse), '/interchain_security.ccv.provider.v1.Query/QueryThrottledConsumerPacketData': grpclib.const.Handler(self.QueryThrottledConsumerPacketData, grpclib.const.Cardinality.UNARY_UNARY, interchain_security.ccv.provider.v1.query_pb2.QueryThrottledConsumerPacketDataRequest, interchain_security.ccv.provider.v1.query_pb2.QueryThrottledConsumerPacketDataResponse), '/interchain_security.ccv.provider.v1.Query/QueryRegisteredConsumerRewardDenoms': grpclib.const.Handler(self.QueryRegisteredConsumerRewardDenoms, grpclib.const.Cardinality.UNARY_UNARY, interchain_security.ccv.provider.v1.query_pb2.QueryRegisteredConsumerRewardDenomsRequest, interchain_security.ccv.provider.v1.query_pb2.QueryRegisteredConsumerRewardDenomsResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.QueryConsumerGenesis = grpclib.client.UnaryUnaryMethod(channel, '/interchain_security.ccv.provider.v1.Query/QueryConsumerGenesis', interchain_security.ccv.provider.v1.query_pb2.QueryConsumerGenesisRequest, interchain_security.ccv.provider.v1.query_pb2.QueryConsumerGenesisResponse)
        self.QueryConsumerChains = grpclib.client.UnaryUnaryMethod(channel, '/interchain_security.ccv.provider.v1.Query/QueryConsumerChains', interchain_security.ccv.provider.v1.query_pb2.QueryConsumerChainsRequest, interchain_security.ccv.provider.v1.query_pb2.QueryConsumerChainsResponse)
        self.QueryConsumerChainStarts = grpclib.client.UnaryUnaryMethod(channel, '/interchain_security.ccv.provider.v1.Query/QueryConsumerChainStarts', interchain_security.ccv.provider.v1.query_pb2.QueryConsumerChainStartProposalsRequest, interchain_security.ccv.provider.v1.query_pb2.QueryConsumerChainStartProposalsResponse)
        self.QueryConsumerChainStops = grpclib.client.UnaryUnaryMethod(channel, '/interchain_security.ccv.provider.v1.Query/QueryConsumerChainStops', interchain_security.ccv.provider.v1.query_pb2.QueryConsumerChainStopProposalsRequest, interchain_security.ccv.provider.v1.query_pb2.QueryConsumerChainStopProposalsResponse)
        self.QueryValidatorConsumerAddr = grpclib.client.UnaryUnaryMethod(channel, '/interchain_security.ccv.provider.v1.Query/QueryValidatorConsumerAddr', interchain_security.ccv.provider.v1.query_pb2.QueryValidatorConsumerAddrRequest, interchain_security.ccv.provider.v1.query_pb2.QueryValidatorConsumerAddrResponse)
        self.QueryValidatorProviderAddr = grpclib.client.UnaryUnaryMethod(channel, '/interchain_security.ccv.provider.v1.Query/QueryValidatorProviderAddr', interchain_security.ccv.provider.v1.query_pb2.QueryValidatorProviderAddrRequest, interchain_security.ccv.provider.v1.query_pb2.QueryValidatorProviderAddrResponse)
        self.QueryThrottleState = grpclib.client.UnaryUnaryMethod(channel, '/interchain_security.ccv.provider.v1.Query/QueryThrottleState', interchain_security.ccv.provider.v1.query_pb2.QueryThrottleStateRequest, interchain_security.ccv.provider.v1.query_pb2.QueryThrottleStateResponse)
        self.QueryThrottledConsumerPacketData = grpclib.client.UnaryUnaryMethod(channel, '/interchain_security.ccv.provider.v1.Query/QueryThrottledConsumerPacketData', interchain_security.ccv.provider.v1.query_pb2.QueryThrottledConsumerPacketDataRequest, interchain_security.ccv.provider.v1.query_pb2.QueryThrottledConsumerPacketDataResponse)
        self.QueryRegisteredConsumerRewardDenoms = grpclib.client.UnaryUnaryMethod(channel, '/interchain_security.ccv.provider.v1.Query/QueryRegisteredConsumerRewardDenoms', interchain_security.ccv.provider.v1.query_pb2.QueryRegisteredConsumerRewardDenomsRequest, interchain_security.ccv.provider.v1.query_pb2.QueryRegisteredConsumerRewardDenomsResponse)