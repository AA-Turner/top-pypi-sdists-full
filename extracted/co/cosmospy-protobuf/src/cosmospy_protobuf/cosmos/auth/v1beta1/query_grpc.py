import abc
import typing
import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server
from .... import cosmos
from .... import gogoproto
import google.protobuf.any_pb2
from .... import google
from .... import cosmos_proto

class QueryBase(abc.ABC):

    @abc.abstractmethod
    async def Accounts(self, stream: 'grpclib.server.Stream[cosmos.auth.v1beta1.query_pb2.QueryAccountsRequest, cosmos.auth.v1beta1.query_pb2.QueryAccountsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Account(self, stream: 'grpclib.server.Stream[cosmos.auth.v1beta1.query_pb2.QueryAccountRequest, cosmos.auth.v1beta1.query_pb2.QueryAccountResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Params(self, stream: 'grpclib.server.Stream[cosmos.auth.v1beta1.query_pb2.QueryParamsRequest, cosmos.auth.v1beta1.query_pb2.QueryParamsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def ModuleAccountByName(self, stream: 'grpclib.server.Stream[cosmos.auth.v1beta1.query_pb2.QueryModuleAccountByNameRequest, cosmos.auth.v1beta1.query_pb2.QueryModuleAccountByNameResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/cosmos.auth.v1beta1.Query/Accounts': grpclib.const.Handler(self.Accounts, grpclib.const.Cardinality.UNARY_UNARY, cosmos.auth.v1beta1.query_pb2.QueryAccountsRequest, cosmos.auth.v1beta1.query_pb2.QueryAccountsResponse), '/cosmos.auth.v1beta1.Query/Account': grpclib.const.Handler(self.Account, grpclib.const.Cardinality.UNARY_UNARY, cosmos.auth.v1beta1.query_pb2.QueryAccountRequest, cosmos.auth.v1beta1.query_pb2.QueryAccountResponse), '/cosmos.auth.v1beta1.Query/Params': grpclib.const.Handler(self.Params, grpclib.const.Cardinality.UNARY_UNARY, cosmos.auth.v1beta1.query_pb2.QueryParamsRequest, cosmos.auth.v1beta1.query_pb2.QueryParamsResponse), '/cosmos.auth.v1beta1.Query/ModuleAccountByName': grpclib.const.Handler(self.ModuleAccountByName, grpclib.const.Cardinality.UNARY_UNARY, cosmos.auth.v1beta1.query_pb2.QueryModuleAccountByNameRequest, cosmos.auth.v1beta1.query_pb2.QueryModuleAccountByNameResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Accounts = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.auth.v1beta1.Query/Accounts', cosmos.auth.v1beta1.query_pb2.QueryAccountsRequest, cosmos.auth.v1beta1.query_pb2.QueryAccountsResponse)
        self.Account = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.auth.v1beta1.Query/Account', cosmos.auth.v1beta1.query_pb2.QueryAccountRequest, cosmos.auth.v1beta1.query_pb2.QueryAccountResponse)
        self.Params = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.auth.v1beta1.Query/Params', cosmos.auth.v1beta1.query_pb2.QueryParamsRequest, cosmos.auth.v1beta1.query_pb2.QueryParamsResponse)
        self.ModuleAccountByName = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.auth.v1beta1.Query/ModuleAccountByName', cosmos.auth.v1beta1.query_pb2.QueryModuleAccountByNameRequest, cosmos.auth.v1beta1.query_pb2.QueryModuleAccountByNameResponse)