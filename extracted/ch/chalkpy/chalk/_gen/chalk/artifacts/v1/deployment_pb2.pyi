from chalk._gen.chalk.artifacts.v1 import cdc_pb2 as _cdc_pb2
from chalk._gen.chalk.artifacts.v1 import chart_pb2 as _chart_pb2
from chalk._gen.chalk.artifacts.v1 import cron_query_pb2 as _cron_query_pb2
from chalk._gen.chalk.artifacts.v1 import export_pb2 as _export_pb2
from chalk._gen.chalk.graph.v1 import graph_pb2 as _graph_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class DeploymentArtifacts(_message.Message):
    __slots__ = ("graph", "crons", "charts", "cdc_sources", "config", "chalkpy")
    GRAPH_FIELD_NUMBER: _ClassVar[int]
    CRONS_FIELD_NUMBER: _ClassVar[int]
    CHARTS_FIELD_NUMBER: _ClassVar[int]
    CDC_SOURCES_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    CHALKPY_FIELD_NUMBER: _ClassVar[int]
    graph: _graph_pb2.Graph
    crons: _containers.RepeatedCompositeFieldContainer[_cron_query_pb2.CronQuery]
    charts: _containers.RepeatedCompositeFieldContainer[_chart_pb2.Chart]
    cdc_sources: _containers.RepeatedCompositeFieldContainer[_cdc_pb2.CDCSource]
    config: _export_pb2.ProjectSettings
    chalkpy: _export_pb2.ChalkpyInfo
    def __init__(
        self,
        graph: _Optional[_Union[_graph_pb2.Graph, _Mapping]] = ...,
        crons: _Optional[_Iterable[_Union[_cron_query_pb2.CronQuery, _Mapping]]] = ...,
        charts: _Optional[_Iterable[_Union[_chart_pb2.Chart, _Mapping]]] = ...,
        cdc_sources: _Optional[_Iterable[_Union[_cdc_pb2.CDCSource, _Mapping]]] = ...,
        config: _Optional[_Union[_export_pb2.ProjectSettings, _Mapping]] = ...,
        chalkpy: _Optional[_Union[_export_pb2.ChalkpyInfo, _Mapping]] = ...,
    ) -> None: ...
