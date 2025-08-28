from chalk._gen.chalk.arrow.v1 import arrow_pb2 as _arrow_pb2
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

class TensorSpec(_message.Message):
    __slots__ = ("dtype", "shape")
    DTYPE_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    dtype: _arrow_pb2.ArrowType
    shape: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self, dtype: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ..., shape: _Optional[_Iterable[int]] = ...
    ) -> None: ...

class TabularSpec(_message.Message):
    __slots__ = ("dtype", "name")
    DTYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    dtype: _arrow_pb2.ArrowType
    name: str
    def __init__(
        self, dtype: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ..., name: _Optional[str] = ...
    ) -> None: ...

class TensorSchema(_message.Message):
    __slots__ = ("tensors",)
    TENSORS_FIELD_NUMBER: _ClassVar[int]
    tensors: _containers.RepeatedCompositeFieldContainer[TensorSpec]
    def __init__(self, tensors: _Optional[_Iterable[_Union[TensorSpec, _Mapping]]] = ...) -> None: ...

class TabularSchema(_message.Message):
    __slots__ = ("columns",)
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    columns: _containers.RepeatedCompositeFieldContainer[TabularSpec]
    def __init__(self, columns: _Optional[_Iterable[_Union[TabularSpec, _Mapping]]] = ...) -> None: ...

class ModelSchema(_message.Message):
    __slots__ = ("tensor", "tabular")
    TENSOR_FIELD_NUMBER: _ClassVar[int]
    TABULAR_FIELD_NUMBER: _ClassVar[int]
    tensor: TensorSchema
    tabular: TabularSchema
    def __init__(
        self,
        tensor: _Optional[_Union[TensorSchema, _Mapping]] = ...,
        tabular: _Optional[_Union[TabularSchema, _Mapping]] = ...,
    ) -> None: ...

class ModelSignature(_message.Message):
    __slots__ = ("inputs", "outputs")
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    inputs: ModelSchema
    outputs: ModelSchema
    def __init__(
        self,
        inputs: _Optional[_Union[ModelSchema, _Mapping]] = ...,
        outputs: _Optional[_Union[ModelSchema, _Mapping]] = ...,
    ) -> None: ...

class ModelArtifactSpec(_message.Message):
    __slots__ = ("model_files", "additional_files", "model_type", "model_encoding", "model_signature")
    MODEL_FILES_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_FILES_FIELD_NUMBER: _ClassVar[int]
    MODEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    MODEL_ENCODING_FIELD_NUMBER: _ClassVar[int]
    MODEL_SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    model_files: _containers.RepeatedScalarFieldContainer[str]
    additional_files: _containers.RepeatedScalarFieldContainer[str]
    model_type: str
    model_encoding: str
    model_signature: ModelSignature
    def __init__(
        self,
        model_files: _Optional[_Iterable[str]] = ...,
        additional_files: _Optional[_Iterable[str]] = ...,
        model_type: _Optional[str] = ...,
        model_encoding: _Optional[str] = ...,
        model_signature: _Optional[_Union[ModelSignature, _Mapping]] = ...,
    ) -> None: ...
