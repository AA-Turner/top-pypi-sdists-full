from chalk._gen.chalk.arrow.v1 import arrow_pb2 as _arrow_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
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

class ModelType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MODEL_TYPE_UNSPECIFIED: _ClassVar[ModelType]
    MODEL_TYPE_PYTORCH: _ClassVar[ModelType]
    MODEL_TYPE_SKLEARN: _ClassVar[ModelType]
    MODEL_TYPE_TENSORFLOW: _ClassVar[ModelType]
    MODEL_TYPE_XGBOOST: _ClassVar[ModelType]
    MODEL_TYPE_LIGHTGBM: _ClassVar[ModelType]
    MODEL_TYPE_CATBOOST: _ClassVar[ModelType]
    MODEL_TYPE_ONNX: _ClassVar[ModelType]

class ModelEncoding(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MODEL_ENCODING_UNSPECIFIED: _ClassVar[ModelEncoding]
    MODEL_ENCODING_PICKLE: _ClassVar[ModelEncoding]
    MODEL_ENCODING_JOBLIB: _ClassVar[ModelEncoding]
    MODEL_ENCODING_JSON: _ClassVar[ModelEncoding]
    MODEL_ENCODING_TEXT: _ClassVar[ModelEncoding]
    MODEL_ENCODING_HDF5: _ClassVar[ModelEncoding]
    MODEL_ENCODING_PROTOBUF: _ClassVar[ModelEncoding]
    MODEL_ENCODING_CBM: _ClassVar[ModelEncoding]
    MODEL_ENCODING_SAFETENSORS: _ClassVar[ModelEncoding]

MODEL_TYPE_UNSPECIFIED: ModelType
MODEL_TYPE_PYTORCH: ModelType
MODEL_TYPE_SKLEARN: ModelType
MODEL_TYPE_TENSORFLOW: ModelType
MODEL_TYPE_XGBOOST: ModelType
MODEL_TYPE_LIGHTGBM: ModelType
MODEL_TYPE_CATBOOST: ModelType
MODEL_TYPE_ONNX: ModelType
MODEL_ENCODING_UNSPECIFIED: ModelEncoding
MODEL_ENCODING_PICKLE: ModelEncoding
MODEL_ENCODING_JOBLIB: ModelEncoding
MODEL_ENCODING_JSON: ModelEncoding
MODEL_ENCODING_TEXT: ModelEncoding
MODEL_ENCODING_HDF5: ModelEncoding
MODEL_ENCODING_PROTOBUF: ModelEncoding
MODEL_ENCODING_CBM: ModelEncoding
MODEL_ENCODING_SAFETENSORS: ModelEncoding

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

class ModelFile(_message.Message):
    __slots__ = ("name", "size_kb", "file_hash")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SIZE_KB_FIELD_NUMBER: _ClassVar[int]
    FILE_HASH_FIELD_NUMBER: _ClassVar[int]
    name: str
    size_kb: int
    file_hash: bytes
    def __init__(
        self, name: _Optional[str] = ..., size_kb: _Optional[int] = ..., file_hash: _Optional[bytes] = ...
    ) -> None: ...

class ModelArtifactSpec(_message.Message):
    __slots__ = (
        "model_files",
        "additional_files",
        "model_type",
        "model_encoding",
        "model_signature",
        "input_features",
        "output_features",
    )
    MODEL_FILES_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_FILES_FIELD_NUMBER: _ClassVar[int]
    MODEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    MODEL_ENCODING_FIELD_NUMBER: _ClassVar[int]
    MODEL_SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    INPUT_FEATURES_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FEATURES_FIELD_NUMBER: _ClassVar[int]
    model_files: _containers.RepeatedCompositeFieldContainer[ModelFile]
    additional_files: _containers.RepeatedCompositeFieldContainer[ModelFile]
    model_type: ModelType
    model_encoding: ModelEncoding
    model_signature: ModelSignature
    input_features: _containers.RepeatedScalarFieldContainer[str]
    output_features: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        model_files: _Optional[_Iterable[_Union[ModelFile, _Mapping]]] = ...,
        additional_files: _Optional[_Iterable[_Union[ModelFile, _Mapping]]] = ...,
        model_type: _Optional[_Union[ModelType, str]] = ...,
        model_encoding: _Optional[_Union[ModelEncoding, str]] = ...,
        model_signature: _Optional[_Union[ModelSignature, _Mapping]] = ...,
        input_features: _Optional[_Iterable[str]] = ...,
        output_features: _Optional[_Iterable[str]] = ...,
    ) -> None: ...
