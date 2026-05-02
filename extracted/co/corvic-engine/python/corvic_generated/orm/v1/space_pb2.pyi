from corvic_generated.algorithm.graph.v1 import graph_pb2 as _graph_pb2
from corvic_generated.embedding.v1 import models_pb2 as _models_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SpaceParameters(_message.Message):
    __slots__ = ("column_embedding_parameters", "node2vec_parameters", "concat_and_embed_parameters", "embed_and_concat_parameters", "embed_image_parameters")
    COLUMN_EMBEDDING_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    NODE2VEC_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    CONCAT_AND_EMBED_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    EMBED_AND_CONCAT_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    EMBED_IMAGE_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    column_embedding_parameters: _models_pb2.ColumnEmbeddingParameters
    node2vec_parameters: _graph_pb2.Node2VecParameters
    concat_and_embed_parameters: _models_pb2.ConcatAndEmbedParameters
    embed_and_concat_parameters: _models_pb2.EmbedAndConcatParameters
    embed_image_parameters: _models_pb2.EmbedImageParameters
    def __init__(self, column_embedding_parameters: _Optional[_Union[_models_pb2.ColumnEmbeddingParameters, _Mapping]] = ..., node2vec_parameters: _Optional[_Union[_graph_pb2.Node2VecParameters, _Mapping]] = ..., concat_and_embed_parameters: _Optional[_Union[_models_pb2.ConcatAndEmbedParameters, _Mapping]] = ..., embed_and_concat_parameters: _Optional[_Union[_models_pb2.EmbedAndConcatParameters, _Mapping]] = ..., embed_image_parameters: _Optional[_Union[_models_pb2.EmbedImageParameters, _Mapping]] = ...) -> None: ...
