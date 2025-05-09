"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

from abc import (
    ABCMeta,
    abstractmethod,
)
from chalk._gen.chalk.server.v1.chart_pb2 import (
    ListChartsRequest,
    ListChartsResponse,
)
from grpc import (
    Channel,
    Server,
    ServicerContext,
    UnaryUnaryMultiCallable,
)

class ChartsServiceStub:
    def __init__(self, channel: Channel) -> None: ...
    ListCharts: UnaryUnaryMultiCallable[
        ListChartsRequest,
        ListChartsResponse,
    ]

class ChartsServiceServicer(metaclass=ABCMeta):
    @abstractmethod
    def ListCharts(
        self,
        request: ListChartsRequest,
        context: ServicerContext,
    ) -> ListChartsResponse: ...

def add_ChartsServiceServicer_to_server(servicer: ChartsServiceServicer, server: Server) -> None: ...
