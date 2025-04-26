import abc
import typing
import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server
from ..... import google
from ..... import cosmos

class ServiceBase(abc.ABC):

    @abc.abstractmethod
    async def Config(self, stream: 'grpclib.server.Stream[cosmos.base.node.v1beta1.query_pb2.ConfigRequest, cosmos.base.node.v1beta1.query_pb2.ConfigResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/cosmos.base.node.v1beta1.Service/Config': grpclib.const.Handler(self.Config, grpclib.const.Cardinality.UNARY_UNARY, cosmos.base.node.v1beta1.query_pb2.ConfigRequest, cosmos.base.node.v1beta1.query_pb2.ConfigResponse)}

class ServiceStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Config = grpclib.client.UnaryUnaryMethod(channel, '/cosmos.base.node.v1beta1.Service/Config', cosmos.base.node.v1beta1.query_pb2.ConfigRequest, cosmos.base.node.v1beta1.query_pb2.ConfigResponse)