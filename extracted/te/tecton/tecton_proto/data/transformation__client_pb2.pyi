from tecton_proto.args import transformation__client_pb2 as _transformation__client_pb2
from tecton_proto.args import user_defined_function__client_pb2 as _user_defined_function__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.data import fco_metadata__client_pb2 as _fco_metadata__client_pb2
from tecton_proto.validation import validator__client_pb2 as _validator__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Transformation(_message.Message):
    __slots__ = ["fco_metadata", "options", "transformation_id", "transformation_mode", "user_function", "validation_args"]
    class OptionsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    FCO_METADATA_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMATION_ID_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMATION_MODE_FIELD_NUMBER: _ClassVar[int]
    USER_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_ARGS_FIELD_NUMBER: _ClassVar[int]
    fco_metadata: _fco_metadata__client_pb2.FcoMetadata
    options: _containers.ScalarMap[str, str]
    transformation_id: _id__client_pb2.Id
    transformation_mode: _transformation__client_pb2.TransformationMode
    user_function: _user_defined_function__client_pb2.UserDefinedFunction
    validation_args: _validator__client_pb2.TransformationValidationArgs
    def __init__(self, transformation_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., fco_metadata: _Optional[_Union[_fco_metadata__client_pb2.FcoMetadata, _Mapping]] = ..., transformation_mode: _Optional[_Union[_transformation__client_pb2.TransformationMode, str]] = ..., user_function: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ..., validation_args: _Optional[_Union[_validator__client_pb2.TransformationValidationArgs, _Mapping]] = ..., options: _Optional[_Mapping[str, str]] = ...) -> None: ...
