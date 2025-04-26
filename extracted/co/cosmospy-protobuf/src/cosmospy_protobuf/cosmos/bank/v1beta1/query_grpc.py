import abc
import typing
import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server
from .... import cosmos
from .... import gogoproto
from .... import google

class QueryBase(abc.ABC):

    @abc.abstractmethod
    async def Balance(self, stream: 'grpclib.server.Stream[cosmos.bank.v1beta1.query_pb2.QueryBalanceRequest, cosmos.bank.v1beta1.query_pb2.QueryBalanceResponse]') -> None:
        pass

    @abc.abstractmethod
    async def AllBalances(self, stream: 'grpclib.server.Stream[cosmos.bank.v1beta1.query_pb2.QueryAllBalancesRequest, cosmos.bank.v1beta1.query_pb2.QueryAllBalancesResponse]') -> None:
        pass

    @abc.abstractmethod
    async def SpendableBalances(self, stream: 'grpclib.server.Stream[cosmos.bank.v1beta1.query_pb2.QuerySpendableBalancesRequest, cosmos.bank.v1beta1.query_pb2.QuerySpendableBalancesResponse]') -> None:
        pass

    @abc.abstractmethod
    async def TotalSupply(self, stream: 'grpclib.server.Stream[cosmos.bank.v1beta1.query_pb2.QueryTotalSupplyRequest, cosmos.bank.v1beta1.query_pb2.QueryTotalSupplyResponse]') -> None:
        pass

    @abc.abstractmethod
    async def SupplyOf(self, stream: 'grpclib.server.Stream[cosmos.bank.v1beta1.query_pb2.QuerySupplyOfRequest, cosmos.bank.v1beta1.query_pb2.QuerySupplyOfResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Params(self, stream: 'grpclib.server.Stream[cosmos.bank.v1beta1.query_pb2.QueryParamsRequest, cosmos.bank.v1beta1.query_pb2.QueryParamsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def DenomMetadata(self, stream: 'grpclib.server.Stream[cosmos.bank.v1beta1.query_pb2.QueryDenomMetadataRequest, cosmos.bank.v1beta1.query_pb2.QueryDenomMetadataResponse]') -> None:
        pass

    @abc.abstractmethod
    async def DenomsMetadata(self, stream: 'grpclib.server.Stream[cosmos.bank.v1beta1.query_pb2.QueryDenomsMetadataRequest, cosmos.bank.v1beta1.query_pb2.QueryDenomsMetadataResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/cosmos.bank.v1beta1.Query/Balance': grpclib.const.Handler(self.Balance, grpclib.const.Cardinality.UNARY_UNARY, cosmos.bank.v1beta1.query_pb2.QueryBalanceRequest, cosmos.bank.v1beta1.query_pb2.QueryBalanceResponse), '/cosmos.bank.v1beta1.Query/AllBalances': grpclib.const.Handler(self.AllBalances, grpclib.const.Cardinality.UNARY_UNARY, cosmos.bank.v1beta1.query_pb2.QueryAllBalancesRequest, cosmos.bank.v1beta1.query_pb2.QueryAllBalancesResponse), '/cosmos.bank.v1beta1.Query/SpendableBalances': grpclib.const.Handler(self.SpendableBalances, grpclib.const.Cardinality.UNARY_UNARY, cosmos.bank.v1beta1.query_pb2.QuerySpendableBalancesRequest, cosmos.bank.v1beta1.query_pb2.QuerySpendableBalancesResponse), '/cosmos.bank.v1beta1.Query/TotalSupply': grpclib.const.Handler(self.TotalSupply, grpclib.const.Cardinality.UNARY_UNARY, cosmos.bank.v1beta1.query_pb2.QueryTotalSupplyRequest, cosmos.bank.v1beta1.query_pb2.QueryTotalSupplyResponse), '/cosmos.bank.v1beta1.Query/SupplyOf': grpclib.const.Handler(self.SupplyOf, grpclib.const.Cardinality.UNARY_UNARY, cosmos.bank.v1beta1.query_pb2.QuerySupplyOfRequest, cosmos.bank.v1beta1.query_pb2.QuerySupplyOfResponse), '/cosmos.bank.v1beta1.Query/Params': grpclib.const.Handler(self.Params, grpclib.const.Cardinality.UNARY_UNARY, cosmos.bank.v1beta1.query_pb2.QueryParamsRequest, cosmos.bank.v1beta1.query_pb2.QueryParamsResponse), '/cosmos.bank.v1beta1.Query/DenomMetadata': grpclib.const.Handler(self.DenomMetadata, grpclib.const.Cardinality.UNARY_UNARY, cosmos.bank.v1beta1.query_pb2.QueryDenomMetadataRequest, cosmos.bank.v1beta1.query_pb2.QueryDenomMetadataResponse), '/cosmos.bank.v1beta1.Query/DenomsMetadata': grpclib.const.Handler(self.DenomsMetadata, grpclib.const.Cardinality.UNARY_UNARY, cosmos.bank.v1beta1.query_pb2.QueryDenomsMetadataRequest, cosmos.bank.v1beta1.query_pb2.QueryDenomsMetadataResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Balance = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.bank.v1beta1.Query/Balance', cosmos.bank.v1beta1.query_pb2.QueryBalanceRequest, cosmos.bank.v1beta1.query_pb2.QueryBalanceResponse)
        self.AllBalances = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.bank.v1beta1.Query/AllBalances', cosmos.bank.v1beta1.query_pb2.QueryAllBalancesRequest, cosmos.bank.v1beta1.query_pb2.QueryAllBalancesResponse)
        self.SpendableBalances = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.bank.v1beta1.Query/SpendableBalances', cosmos.bank.v1beta1.query_pb2.QuerySpendableBalancesRequest, cosmos.bank.v1beta1.query_pb2.QuerySpendableBalancesResponse)
        self.TotalSupply = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.bank.v1beta1.Query/TotalSupply', cosmos.bank.v1beta1.query_pb2.QueryTotalSupplyRequest, cosmos.bank.v1beta1.query_pb2.QueryTotalSupplyResponse)
        self.SupplyOf = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.bank.v1beta1.Query/SupplyOf', cosmos.bank.v1beta1.query_pb2.QuerySupplyOfRequest, cosmos.bank.v1beta1.query_pb2.QuerySupplyOfResponse)
        self.Params = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.bank.v1beta1.Query/Params', cosmos.bank.v1beta1.query_pb2.QueryParamsRequest, cosmos.bank.v1beta1.query_pb2.QueryParamsResponse)
        self.DenomMetadata = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.bank.v1beta1.Query/DenomMetadata', cosmos.bank.v1beta1.query_pb2.QueryDenomMetadataRequest, cosmos.bank.v1beta1.query_pb2.QueryDenomMetadataResponse)
        self.DenomsMetadata = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.bank.v1beta1.Query/DenomsMetadata', cosmos.bank.v1beta1.query_pb2.QueryDenomsMetadataRequest, cosmos.bank.v1beta1.query_pb2.QueryDenomsMetadataResponse)