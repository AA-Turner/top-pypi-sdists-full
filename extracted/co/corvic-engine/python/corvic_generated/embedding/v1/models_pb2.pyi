from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Model(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MODEL_UNSPECIFIED: _ClassVar[Model]
    MODEL_SENTENCE_TRANSFORMER: _ClassVar[Model]
    MODEL_OPENAI_TEXT_EMBEDDING_3_SMALL: _ClassVar[Model]
    MODEL_OPENAI_TEXT_EMBEDDING_3_LARGE: _ClassVar[Model]
    MODEL_GCP_TEXT_EMBEDDING_004: _ClassVar[Model]
    MODEL_CUSTOM: _ClassVar[Model]

class ImageModel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    IMAGE_MODEL_UNSPECIFIED: _ClassVar[ImageModel]
    IMAGE_MODEL_CLIP: _ClassVar[ImageModel]
    IMAGE_MODEL_CUSTOM: _ClassVar[ImageModel]
MODEL_UNSPECIFIED: Model
MODEL_SENTENCE_TRANSFORMER: Model
MODEL_OPENAI_TEXT_EMBEDDING_3_SMALL: Model
MODEL_OPENAI_TEXT_EMBEDDING_3_LARGE: Model
MODEL_GCP_TEXT_EMBEDDING_004: Model
MODEL_CUSTOM: Model
IMAGE_MODEL_UNSPECIFIED: ImageModel
IMAGE_MODEL_CLIP: ImageModel
IMAGE_MODEL_CUSTOM: ImageModel

class Parameters(_message.Message):
    __slots__ = ("model", "ndim")
    MODEL_FIELD_NUMBER: _ClassVar[int]
    NDIM_FIELD_NUMBER: _ClassVar[int]
    model: Model
    ndim: int
    def __init__(self, model: _Optional[_Union[Model, str]] = ..., ndim: _Optional[int] = ...) -> None: ...

class ColumnEmbeddingParameters(_message.Message):
    __slots__ = ("column_parameters",)
    class ColumnParametersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Parameters
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Parameters, _Mapping]] = ...) -> None: ...
    COLUMN_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    column_parameters: _containers.MessageMap[str, Parameters]
    def __init__(self, column_parameters: _Optional[_Mapping[str, Parameters]] = ...) -> None: ...

class ConcatStringAndEmbedParameters(_message.Message):
    __slots__ = ("column_names", "model_parameters")
    COLUMN_NAMES_FIELD_NUMBER: _ClassVar[int]
    MODEL_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    column_names: _containers.RepeatedScalarFieldContainer[str]
    model_parameters: Parameters
    def __init__(self, column_names: _Optional[_Iterable[str]] = ..., model_parameters: _Optional[_Union[Parameters, _Mapping]] = ...) -> None: ...

class ConcatAndEmbedParameters(_message.Message):
    __slots__ = ("column_names", "model_parameters")
    COLUMN_NAMES_FIELD_NUMBER: _ClassVar[int]
    MODEL_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    column_names: _containers.RepeatedScalarFieldContainer[str]
    model_parameters: Parameters
    def __init__(self, column_names: _Optional[_Iterable[str]] = ..., model_parameters: _Optional[_Union[Parameters, _Mapping]] = ...) -> None: ...

class EmbedAndConcatParameters(_message.Message):
    __slots__ = ("ndim",)
    NDIM_FIELD_NUMBER: _ClassVar[int]
    ndim: int
    def __init__(self, ndim: _Optional[int] = ...) -> None: ...

class ImageModelParameters(_message.Message):
    __slots__ = ("model", "ndim")
    MODEL_FIELD_NUMBER: _ClassVar[int]
    NDIM_FIELD_NUMBER: _ClassVar[int]
    model: ImageModel
    ndim: int
    def __init__(self, model: _Optional[_Union[ImageModel, str]] = ..., ndim: _Optional[int] = ...) -> None: ...

class EmbedImageParameters(_message.Message):
    __slots__ = ("column_name", "model_parameters")
    COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    MODEL_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    column_name: str
    model_parameters: ImageModelParameters
    def __init__(self, column_name: _Optional[str] = ..., model_parameters: _Optional[_Union[ImageModelParameters, _Mapping]] = ...) -> None: ...
