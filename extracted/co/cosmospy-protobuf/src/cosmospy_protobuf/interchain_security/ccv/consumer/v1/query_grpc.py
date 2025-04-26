import abc
import typing
import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server
from ..... import gogoproto
from ..... import google
from ..... import interchain_security

class QueryBase(abc.ABC):

    @abc.abstractmethod
    async def QueryNextFeeDistribution(self, stream: 'grpclib.server.Stream[interchain_security.ccv.consumer.v1.query_pb2.QueryNextFeeDistributionEstimateRequest, interchain_security.ccv.consumer.v1.query_pb2.QueryNextFeeDistributionEstimateResponse]') -> None:
        pass

    @abc.abstractmethod
    async def QueryParams(self, stream: 'grpclib.server.Stream[interchain_security.ccv.consumer.v1.query_pb2.QueryParamsRequest, interchain_security.ccv.consumer.v1.query_pb2.QueryParamsResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/interchain_security.ccv.consumer.v1.Query/QueryNextFeeDistribution': grpclib.const.Handler(self.QueryNextFeeDistribution, grpclib.const.Cardinality.UNARY_UNARY, interchain_security.ccv.consumer.v1.query_pb2.QueryNextFeeDistributionEstimateRequest, interchain_security.ccv.consumer.v1.query_pb2.QueryNextFeeDistributionEstimateResponse), '/interchain_security.ccv.consumer.v1.Query/QueryParams': grpclib.const.Handler(self.QueryParams, grpclib.const.Cardinality.UNARY_UNARY, interchain_security.ccv.consumer.v1.query_pb2.QueryParamsRequest, interchain_security.ccv.consumer.v1.query_pb2.QueryParamsResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.QueryNextFeeDistribution = grpclib.client.UnaryUnaryMethod(channel, '/interchain_security.ccv.consumer.v1.Query/QueryNextFeeDistribution', interchain_security.ccv.consumer.v1.query_pb2.QueryNextFeeDistributionEstimateRequest, interchain_security.ccv.consumer.v1.query_pb2.QueryNextFeeDistributionEstimateResponse)
        self.QueryParams = grpclib.client.UnaryUnaryMethod(channel, '/interchain_security.ccv.consumer.v1.Query/QueryParams', interchain_security.ccv.consumer.v1.query_pb2.QueryParamsRequest, interchain_security.ccv.consumer.v1.query_pb2.QueryParamsResponse)