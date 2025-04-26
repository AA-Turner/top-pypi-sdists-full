import abc
import typing
import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server
from .... import google
from .... import cosmos
from .... import gogoproto
from .... import tendermint

class ServiceBase(abc.ABC):

    @abc.abstractmethod
    async def Simulate(self, stream: 'grpclib.server.Stream[cosmos.tx.v1beta1.service_pb2.SimulateRequest, cosmos.tx.v1beta1.service_pb2.SimulateResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetTx(self, stream: 'grpclib.server.Stream[cosmos.tx.v1beta1.service_pb2.GetTxRequest, cosmos.tx.v1beta1.service_pb2.GetTxResponse]') -> None:
        pass

    @abc.abstractmethod
    async def BroadcastTx(self, stream: 'grpclib.server.Stream[cosmos.tx.v1beta1.service_pb2.BroadcastTxRequest, cosmos.tx.v1beta1.service_pb2.BroadcastTxResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetTxsEvent(self, stream: 'grpclib.server.Stream[cosmos.tx.v1beta1.service_pb2.GetTxsEventRequest, cosmos.tx.v1beta1.service_pb2.GetTxsEventResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetBlockWithTxs(self, stream: 'grpclib.server.Stream[cosmos.tx.v1beta1.service_pb2.GetBlockWithTxsRequest, cosmos.tx.v1beta1.service_pb2.GetBlockWithTxsResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/cosmos.tx.v1beta1.Service/Simulate': grpclib.const.Handler(self.Simulate, grpclib.const.Cardinality.UNARY_UNARY, cosmos.tx.v1beta1.service_pb2.SimulateRequest, cosmos.tx.v1beta1.service_pb2.SimulateResponse), '/cosmos.tx.v1beta1.Service/GetTx': grpclib.const.Handler(self.GetTx, grpclib.const.Cardinality.UNARY_UNARY, cosmos.tx.v1beta1.service_pb2.GetTxRequest, cosmos.tx.v1beta1.service_pb2.GetTxResponse), '/cosmos.tx.v1beta1.Service/BroadcastTx': grpclib.const.Handler(self.BroadcastTx, grpclib.const.Cardinality.UNARY_UNARY, cosmos.tx.v1beta1.service_pb2.BroadcastTxRequest, cosmos.tx.v1beta1.service_pb2.BroadcastTxResponse), '/cosmos.tx.v1beta1.Service/GetTxsEvent': grpclib.const.Handler(self.GetTxsEvent, grpclib.const.Cardinality.UNARY_UNARY, cosmos.tx.v1beta1.service_pb2.GetTxsEventRequest, cosmos.tx.v1beta1.service_pb2.GetTxsEventResponse), '/cosmos.tx.v1beta1.Service/GetBlockWithTxs': grpclib.const.Handler(self.GetBlockWithTxs, grpclib.const.Cardinality.UNARY_UNARY, cosmos.tx.v1beta1.service_pb2.GetBlockWithTxsRequest, cosmos.tx.v1beta1.service_pb2.GetBlockWithTxsResponse)}

class ServiceStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Simulate = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.tx.v1beta1.Service/Simulate', cosmos.tx.v1beta1.service_pb2.SimulateRequest, cosmos.tx.v1beta1.service_pb2.SimulateResponse)
        self.GetTx = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.tx.v1beta1.Service/GetTx', cosmos.tx.v1beta1.service_pb2.GetTxRequest, cosmos.tx.v1beta1.service_pb2.GetTxResponse)
        self.BroadcastTx = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.tx.v1beta1.Service/BroadcastTx', cosmos.tx.v1beta1.service_pb2.BroadcastTxRequest, cosmos.tx.v1beta1.service_pb2.BroadcastTxResponse)
        self.GetTxsEvent = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.tx.v1beta1.Service/GetTxsEvent', cosmos.tx.v1beta1.service_pb2.GetTxsEventRequest, cosmos.tx.v1beta1.service_pb2.GetTxsEventResponse)
        self.GetBlockWithTxs = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.tx.v1beta1.Service/GetBlockWithTxs', cosmos.tx.v1beta1.service_pb2.GetBlockWithTxsRequest, cosmos.tx.v1beta1.service_pb2.GetBlockWithTxsResponse)