from buf.validate import validate_pb2 as _validate_pb2
from corvic_generated.algorithm.graph.v1 import graph_pb2 as _graph_pb2
from corvic_generated.embedding.v1 import models_pb2 as _models_pb2
from corvic_generated.status.v1 import event_pb2 as _event_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Parameters(_message.Message):
    __slots__ = ("space_id", "column_embedding_parameters", "node2vec_parameters")
    SPACE_ID_FIELD_NUMBER: _ClassVar[int]
    COLUMN_EMBEDDING_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    NODE2VEC_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    space_id: str
    column_embedding_parameters: _models_pb2.ColumnEmbeddingParameters
    node2vec_parameters: _graph_pb2.Node2VecParameters
    def __init__(self, space_id: _Optional[str] = ..., column_embedding_parameters: _Optional[_Union[_models_pb2.ColumnEmbeddingParameters, _Mapping]] = ..., node2vec_parameters: _Optional[_Union[_graph_pb2.Node2VecParameters, _Mapping]] = ...) -> None: ...

class Experiment(_message.Message):
    __slots__ = ("name", "description", "params")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    params: _containers.RepeatedCompositeFieldContainer[Parameters]
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., params: _Optional[_Iterable[_Union[Parameters, _Mapping]]] = ...) -> None: ...

class EmbeddingMetrics(_message.Message):
    __slots__ = ("ne_sum", "condition_number", "rcondition_number", "stable_rank")
    NE_SUM_FIELD_NUMBER: _ClassVar[int]
    CONDITION_NUMBER_FIELD_NUMBER: _ClassVar[int]
    RCONDITION_NUMBER_FIELD_NUMBER: _ClassVar[int]
    STABLE_RANK_FIELD_NUMBER: _ClassVar[int]
    ne_sum: float
    condition_number: float
    rcondition_number: float
    stable_rank: float
    def __init__(self, ne_sum: _Optional[float] = ..., condition_number: _Optional[float] = ..., rcondition_number: _Optional[float] = ..., stable_rank: _Optional[float] = ...) -> None: ...

class ExperimentEntry(_message.Message):
    __slots__ = ("room_id", "experiment_id", "created_at", "experiment", "recent_events", "embedding_metrics")
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    EXPERIMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    EXPERIMENT_FIELD_NUMBER: _ClassVar[int]
    RECENT_EVENTS_FIELD_NUMBER: _ClassVar[int]
    EMBEDDING_METRICS_FIELD_NUMBER: _ClassVar[int]
    room_id: str
    experiment_id: str
    created_at: _timestamp_pb2.Timestamp
    experiment: Experiment
    recent_events: _containers.RepeatedCompositeFieldContainer[_event_pb2.Event]
    embedding_metrics: EmbeddingMetrics
    def __init__(self, room_id: _Optional[str] = ..., experiment_id: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., experiment: _Optional[_Union[Experiment, _Mapping]] = ..., recent_events: _Optional[_Iterable[_Union[_event_pb2.Event, _Mapping]]] = ..., embedding_metrics: _Optional[_Union[EmbeddingMetrics, _Mapping]] = ...) -> None: ...

class GetExperimentRequest(_message.Message):
    __slots__ = ("experiment_id",)
    EXPERIMENT_ID_FIELD_NUMBER: _ClassVar[int]
    experiment_id: str
    def __init__(self, experiment_id: _Optional[str] = ...) -> None: ...

class GetExperimentResponse(_message.Message):
    __slots__ = ("experiment_entry",)
    EXPERIMENT_ENTRY_FIELD_NUMBER: _ClassVar[int]
    experiment_entry: ExperimentEntry
    def __init__(self, experiment_entry: _Optional[_Union[ExperimentEntry, _Mapping]] = ...) -> None: ...

class ListExperimentsRequest(_message.Message):
    __slots__ = ("room_id",)
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    room_id: str
    def __init__(self, room_id: _Optional[str] = ...) -> None: ...

class ListExperimentsResponse(_message.Message):
    __slots__ = ("experiment_entries",)
    EXPERIMENT_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    experiment_entries: _containers.RepeatedCompositeFieldContainer[ExperimentEntry]
    def __init__(self, experiment_entries: _Optional[_Iterable[_Union[ExperimentEntry, _Mapping]]] = ...) -> None: ...

class CreateExperimentRequest(_message.Message):
    __slots__ = ("room_id", "experiment", "description", "params")
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    EXPERIMENT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    room_id: str
    experiment: Experiment
    description: str
    params: _containers.RepeatedCompositeFieldContainer[Parameters]
    def __init__(self, room_id: _Optional[str] = ..., experiment: _Optional[_Union[Experiment, _Mapping]] = ..., description: _Optional[str] = ..., params: _Optional[_Iterable[_Union[Parameters, _Mapping]]] = ...) -> None: ...

class CreateExperimentResponse(_message.Message):
    __slots__ = ("experiment_entry",)
    EXPERIMENT_ENTRY_FIELD_NUMBER: _ClassVar[int]
    experiment_entry: ExperimentEntry
    def __init__(self, experiment_entry: _Optional[_Union[ExperimentEntry, _Mapping]] = ...) -> None: ...

class DeleteExperimentRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteExperimentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetExperimentResultRequest(_message.Message):
    __slots__ = ("experiment_id",)
    EXPERIMENT_ID_FIELD_NUMBER: _ClassVar[int]
    experiment_id: str
    def __init__(self, experiment_id: _Optional[str] = ...) -> None: ...

class GetExperimentResultResponse(_message.Message):
    __slots__ = ("signed_url",)
    SIGNED_URL_FIELD_NUMBER: _ClassVar[int]
    signed_url: str
    def __init__(self, signed_url: _Optional[str] = ...) -> None: ...

class GetExperimentVisualizationRequest(_message.Message):
    __slots__ = ("experiment_id",)
    EXPERIMENT_ID_FIELD_NUMBER: _ClassVar[int]
    experiment_id: str
    def __init__(self, experiment_id: _Optional[str] = ...) -> None: ...

class EmbeddingRowData(_message.Message):
    __slots__ = ("row_ids", "node_id", "node_type", "embedding")
    ROW_IDS_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    EMBEDDING_FIELD_NUMBER: _ClassVar[int]
    row_ids: _struct_pb2.Struct
    node_id: str
    node_type: str
    embedding: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, row_ids: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., node_id: _Optional[str] = ..., node_type: _Optional[str] = ..., embedding: _Optional[_Iterable[float]] = ...) -> None: ...

class EmbeddingTableData(_message.Message):
    __slots__ = ("embedding_rows",)
    EMBEDDING_ROWS_FIELD_NUMBER: _ClassVar[int]
    embedding_rows: _containers.RepeatedCompositeFieldContainer[EmbeddingRowData]
    def __init__(self, embedding_rows: _Optional[_Iterable[_Union[EmbeddingRowData, _Mapping]]] = ...) -> None: ...

class GetExperimentVisualizationResponse(_message.Message):
    __slots__ = ("coordinates", "fraction_points_retrieved")
    COORDINATES_FIELD_NUMBER: _ClassVar[int]
    FRACTION_POINTS_RETRIEVED_FIELD_NUMBER: _ClassVar[int]
    coordinates: EmbeddingTableData
    fraction_points_retrieved: float
    def __init__(self, coordinates: _Optional[_Union[EmbeddingTableData, _Mapping]] = ..., fraction_points_retrieved: _Optional[float] = ...) -> None: ...
