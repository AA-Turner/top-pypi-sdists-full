from buf.validate import validate_pb2 as _validate_pb2
from corvic_generated.algorithm.graph.v1 import graph_pb2 as _graph_pb2
from corvic_generated.embedding.v1 import models_pb2 as _models_pb2
from corvic_generated.status.v1 import event_pb2 as _event_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SpaceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SPACE_TYPE_UNSPECIFIED: _ClassVar[SpaceType]
    SPACE_TYPE_RELATIONAL: _ClassVar[SpaceType]
    SPACE_TYPE_SEMANTIC: _ClassVar[SpaceType]
    SPACE_TYPE_TABULAR: _ClassVar[SpaceType]
    SPACE_TYPE_IMAGE: _ClassVar[SpaceType]
SPACE_TYPE_UNSPECIFIED: SpaceType
SPACE_TYPE_RELATIONAL: SpaceType
SPACE_TYPE_SEMANTIC: SpaceType
SPACE_TYPE_TABULAR: SpaceType
SPACE_TYPE_IMAGE: SpaceType

class Parameters(_message.Message):
    __slots__ = ("feature_view_id", "column_embedding_parameters", "node2vec_parameters", "concat_string_and_embed", "concat_and_embed_parameters", "embed_and_concat_parameters", "embed_image_parameters")
    FEATURE_VIEW_ID_FIELD_NUMBER: _ClassVar[int]
    COLUMN_EMBEDDING_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    NODE2VEC_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    CONCAT_STRING_AND_EMBED_FIELD_NUMBER: _ClassVar[int]
    CONCAT_AND_EMBED_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    EMBED_AND_CONCAT_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    EMBED_IMAGE_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    feature_view_id: str
    column_embedding_parameters: _models_pb2.ColumnEmbeddingParameters
    node2vec_parameters: _graph_pb2.Node2VecParameters
    concat_string_and_embed: _models_pb2.ConcatStringAndEmbedParameters
    concat_and_embed_parameters: _models_pb2.ConcatAndEmbedParameters
    embed_and_concat_parameters: _models_pb2.EmbedAndConcatParameters
    embed_image_parameters: _models_pb2.EmbedImageParameters
    def __init__(self, feature_view_id: _Optional[str] = ..., column_embedding_parameters: _Optional[_Union[_models_pb2.ColumnEmbeddingParameters, _Mapping]] = ..., node2vec_parameters: _Optional[_Union[_graph_pb2.Node2VecParameters, _Mapping]] = ..., concat_string_and_embed: _Optional[_Union[_models_pb2.ConcatStringAndEmbedParameters, _Mapping]] = ..., concat_and_embed_parameters: _Optional[_Union[_models_pb2.ConcatAndEmbedParameters, _Mapping]] = ..., embed_and_concat_parameters: _Optional[_Union[_models_pb2.EmbedAndConcatParameters, _Mapping]] = ..., embed_image_parameters: _Optional[_Union[_models_pb2.EmbedImageParameters, _Mapping]] = ...) -> None: ...

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

class SpaceEntry(_message.Message):
    __slots__ = ("room_id", "space_id", "created_at", "name", "description", "params", "recent_events", "embedding_metrics", "space_type")
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    SPACE_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    RECENT_EVENTS_FIELD_NUMBER: _ClassVar[int]
    EMBEDDING_METRICS_FIELD_NUMBER: _ClassVar[int]
    SPACE_TYPE_FIELD_NUMBER: _ClassVar[int]
    room_id: str
    space_id: str
    created_at: _timestamp_pb2.Timestamp
    name: str
    description: str
    params: _containers.RepeatedCompositeFieldContainer[Parameters]
    recent_events: _containers.RepeatedCompositeFieldContainer[_event_pb2.Event]
    embedding_metrics: EmbeddingMetrics
    space_type: SpaceType
    def __init__(self, room_id: _Optional[str] = ..., space_id: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., params: _Optional[_Iterable[_Union[Parameters, _Mapping]]] = ..., recent_events: _Optional[_Iterable[_Union[_event_pb2.Event, _Mapping]]] = ..., embedding_metrics: _Optional[_Union[EmbeddingMetrics, _Mapping]] = ..., space_type: _Optional[_Union[SpaceType, str]] = ...) -> None: ...

class GetSpaceRequest(_message.Message):
    __slots__ = ("space_id",)
    SPACE_ID_FIELD_NUMBER: _ClassVar[int]
    space_id: str
    def __init__(self, space_id: _Optional[str] = ...) -> None: ...

class GetSpaceResponse(_message.Message):
    __slots__ = ("space_entry",)
    SPACE_ENTRY_FIELD_NUMBER: _ClassVar[int]
    space_entry: SpaceEntry
    def __init__(self, space_entry: _Optional[_Union[SpaceEntry, _Mapping]] = ...) -> None: ...

class ListSpacesRequest(_message.Message):
    __slots__ = ("room_id",)
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    room_id: str
    def __init__(self, room_id: _Optional[str] = ...) -> None: ...

class ListSpacesResponse(_message.Message):
    __slots__ = ("space_entries",)
    SPACE_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    space_entries: _containers.RepeatedCompositeFieldContainer[SpaceEntry]
    def __init__(self, space_entries: _Optional[_Iterable[_Union[SpaceEntry, _Mapping]]] = ...) -> None: ...

class CreateSpaceRequest(_message.Message):
    __slots__ = ("room_id", "description", "params")
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    room_id: str
    description: str
    params: _containers.RepeatedCompositeFieldContainer[Parameters]
    def __init__(self, room_id: _Optional[str] = ..., description: _Optional[str] = ..., params: _Optional[_Iterable[_Union[Parameters, _Mapping]]] = ...) -> None: ...

class CreateSpaceResponse(_message.Message):
    __slots__ = ("space_entry",)
    SPACE_ENTRY_FIELD_NUMBER: _ClassVar[int]
    space_entry: SpaceEntry
    def __init__(self, space_entry: _Optional[_Union[SpaceEntry, _Mapping]] = ...) -> None: ...

class DeleteSpaceRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteSpaceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetSpaceResultRequest(_message.Message):
    __slots__ = ("space_id",)
    SPACE_ID_FIELD_NUMBER: _ClassVar[int]
    space_id: str
    def __init__(self, space_id: _Optional[str] = ...) -> None: ...

class GetSpaceResultResponse(_message.Message):
    __slots__ = ("signed_url",)
    SIGNED_URL_FIELD_NUMBER: _ClassVar[int]
    signed_url: str
    def __init__(self, signed_url: _Optional[str] = ...) -> None: ...

class GetSpaceVisualizationRequest(_message.Message):
    __slots__ = ("space_id",)
    SPACE_ID_FIELD_NUMBER: _ClassVar[int]
    space_id: str
    def __init__(self, space_id: _Optional[str] = ...) -> None: ...

class EmbeddingRowData(_message.Message):
    __slots__ = ("node_id", "node_type", "embedding")
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    EMBEDDING_FIELD_NUMBER: _ClassVar[int]
    node_id: str
    node_type: str
    embedding: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, node_id: _Optional[str] = ..., node_type: _Optional[str] = ..., embedding: _Optional[_Iterable[float]] = ...) -> None: ...

class EmbeddingTableData(_message.Message):
    __slots__ = ("embedding_rows",)
    EMBEDDING_ROWS_FIELD_NUMBER: _ClassVar[int]
    embedding_rows: _containers.RepeatedCompositeFieldContainer[EmbeddingRowData]
    def __init__(self, embedding_rows: _Optional[_Iterable[_Union[EmbeddingRowData, _Mapping]]] = ...) -> None: ...

class GetSpaceVisualizationResponse(_message.Message):
    __slots__ = ("coordinates", "fraction_points_retrieved")
    COORDINATES_FIELD_NUMBER: _ClassVar[int]
    FRACTION_POINTS_RETRIEVED_FIELD_NUMBER: _ClassVar[int]
    coordinates: EmbeddingTableData
    fraction_points_retrieved: float
    def __init__(self, coordinates: _Optional[_Union[EmbeddingTableData, _Mapping]] = ..., fraction_points_retrieved: _Optional[float] = ...) -> None: ...

class SourceKey(_message.Message):
    __slots__ = ("source_id", "value")
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    source_id: str
    value: _struct_pb2.Value
    def __init__(self, source_id: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...

class VisualizationData(_message.Message):
    __slots__ = ("source_key", "point")
    SOURCE_KEY_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    source_key: SourceKey
    point: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, source_key: _Optional[_Union[SourceKey, _Mapping]] = ..., point: _Optional[_Iterable[float]] = ...) -> None: ...

class GetVisualizationRequest(_message.Message):
    __slots__ = ("space_id", "cursor", "num_points")
    SPACE_ID_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    NUM_POINTS_FIELD_NUMBER: _ClassVar[int]
    space_id: str
    cursor: str
    num_points: int
    def __init__(self, space_id: _Optional[str] = ..., cursor: _Optional[str] = ..., num_points: _Optional[int] = ...) -> None: ...

class GetVisualizationResponse(_message.Message):
    __slots__ = ("cursor", "data")
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    cursor: str
    data: _containers.RepeatedCompositeFieldContainer[VisualizationData]
    def __init__(self, cursor: _Optional[str] = ..., data: _Optional[_Iterable[_Union[VisualizationData, _Mapping]]] = ...) -> None: ...
