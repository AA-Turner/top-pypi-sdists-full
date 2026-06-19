from qm.grpc.qm.pb import inc_qua_config_pb2 as _inc_qua_config_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TranspilationFormats(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    TRANSPILATION_FORMATS_UNSPECIFIED: _ClassVar[TranspilationFormats]
    TRANSPILATION_FORMATS_GATE_LEVEL_AST: _ClassVar[TranspilationFormats]
    TRANSPILATION_FORMATS_PULSE_LEVEL_AST_QOP3: _ClassVar[TranspilationFormats]
    TRANSPILATION_FORMATS_GATE_LEVEL_IR: _ClassVar[TranspilationFormats]
    TRANSPILATION_FORMATS_PULSE_LEVEL_IR: _ClassVar[TranspilationFormats]
    TRANSPILATION_FORMATS_QUAKE: _ClassVar[TranspilationFormats]
    TRANSPILATION_FORMATS_OPENQASM3: _ClassVar[TranspilationFormats]
TRANSPILATION_FORMATS_UNSPECIFIED: TranspilationFormats
TRANSPILATION_FORMATS_GATE_LEVEL_AST: TranspilationFormats
TRANSPILATION_FORMATS_PULSE_LEVEL_AST_QOP3: TranspilationFormats
TRANSPILATION_FORMATS_GATE_LEVEL_IR: TranspilationFormats
TRANSPILATION_FORMATS_PULSE_LEVEL_IR: TranspilationFormats
TRANSPILATION_FORMATS_QUAKE: TranspilationFormats
TRANSPILATION_FORMATS_OPENQASM3: TranspilationFormats

class TranspileRequest(_message.Message):
    __slots__ = ["input_program", "source", "destination", "repetitions"]
    INPUT_PROGRAM_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    REPETITIONS_FIELD_NUMBER: _ClassVar[int]
    input_program: bytes
    source: TranspilationFormats
    destination: TranspilationFormats
    repetitions: int
    def __init__(self, input_program: _Optional[bytes] = ..., source: _Optional[_Union[TranspilationFormats, str]] = ..., destination: _Optional[_Union[TranspilationFormats, str]] = ..., repetitions: _Optional[int] = ...) -> None: ...

class TranspileResponse(_message.Message):
    __slots__ = ["success", "error"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: TranspileSuccess
    error: TranspileError
    def __init__(self, success: _Optional[_Union[TranspileSuccess, _Mapping]] = ..., error: _Optional[_Union[TranspileError, _Mapping]] = ...) -> None: ...

class TranspileSuccess(_message.Message):
    __slots__ = ["output_program", "output_format", "output_config"]
    OUTPUT_PROGRAM_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FORMAT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_CONFIG_FIELD_NUMBER: _ClassVar[int]
    output_program: bytes
    output_format: TranspilationFormats
    output_config: bytes
    def __init__(self, output_program: _Optional[bytes] = ..., output_format: _Optional[_Union[TranspilationFormats, str]] = ..., output_config: _Optional[bytes] = ...) -> None: ...

class TranspileError(_message.Message):
    __slots__ = ["details"]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    details: str
    def __init__(self, details: _Optional[str] = ...) -> None: ...
