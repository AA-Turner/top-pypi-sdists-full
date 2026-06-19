from qm.grpc.qm.pb import inc_qua_config_pb2 as _inc_qua_config_pb2
from qm.grpc.qm.pb import general_messages_pb2 as _general_messages_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OpenQuantumMachineRequest(_message.Message):
    __slots__ = ["config", "never", "always", "ifNeeded", "keep_dc_offsets_when_closing"]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    NEVER_FIELD_NUMBER: _ClassVar[int]
    ALWAYS_FIELD_NUMBER: _ClassVar[int]
    IFNEEDED_FIELD_NUMBER: _ClassVar[int]
    KEEP_DC_OFFSETS_WHEN_CLOSING_FIELD_NUMBER: _ClassVar[int]
    config: _inc_qua_config_pb2.QuaConfig
    never: bool
    always: bool
    ifNeeded: bool
    keep_dc_offsets_when_closing: bool
    def __init__(self, config: _Optional[_Union[_inc_qua_config_pb2.QuaConfig, _Mapping]] = ..., never: bool = ..., always: bool = ..., ifNeeded: bool = ..., keep_dc_offsets_when_closing: bool = ...) -> None: ...

class OpenQuantumMachineResponse(_message.Message):
    __slots__ = ["machineID", "success", "configValidationErrors", "physicalValidationErrors", "openQmWarnings"]
    MACHINEID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    CONFIGVALIDATIONERRORS_FIELD_NUMBER: _ClassVar[int]
    PHYSICALVALIDATIONERRORS_FIELD_NUMBER: _ClassVar[int]
    OPENQMWARNINGS_FIELD_NUMBER: _ClassVar[int]
    machineID: str
    success: bool
    configValidationErrors: _containers.RepeatedCompositeFieldContainer[ConfigValidationMessage]
    physicalValidationErrors: _containers.RepeatedCompositeFieldContainer[PhysicalValidationMessage]
    openQmWarnings: _containers.RepeatedCompositeFieldContainer[OpenQmWarning]
    def __init__(self, machineID: _Optional[str] = ..., success: bool = ..., configValidationErrors: _Optional[_Iterable[_Union[ConfigValidationMessage, _Mapping]]] = ..., physicalValidationErrors: _Optional[_Iterable[_Union[PhysicalValidationMessage, _Mapping]]] = ..., openQmWarnings: _Optional[_Iterable[_Union[OpenQmWarning, _Mapping]]] = ...) -> None: ...

class CloseQuantumMachineRequest(_message.Message):
    __slots__ = ["machineID"]
    MACHINEID_FIELD_NUMBER: _ClassVar[int]
    machineID: str
    def __init__(self, machineID: _Optional[str] = ...) -> None: ...

class CloseQuantumMachineResponse(_message.Message):
    __slots__ = ["success", "errors"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    errors: _containers.RepeatedCompositeFieldContainer[_general_messages_pb2.ErrorMessage]
    def __init__(self, success: bool = ..., errors: _Optional[_Iterable[_Union[_general_messages_pb2.ErrorMessage, _Mapping]]] = ...) -> None: ...

class GetQuantumMachineRequest(_message.Message):
    __slots__ = ["machineID"]
    MACHINEID_FIELD_NUMBER: _ClassVar[int]
    machineID: str
    def __init__(self, machineID: _Optional[str] = ...) -> None: ...

class GetQuantumMachineResponse(_message.Message):
    __slots__ = ["machineID", "config", "success", "errors"]
    MACHINEID_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    machineID: str
    config: _inc_qua_config_pb2.QuaConfig
    success: bool
    errors: _containers.RepeatedCompositeFieldContainer[_general_messages_pb2.ErrorMessage]
    def __init__(self, machineID: _Optional[str] = ..., config: _Optional[_Union[_inc_qua_config_pb2.QuaConfig, _Mapping]] = ..., success: bool = ..., errors: _Optional[_Iterable[_Union[_general_messages_pb2.ErrorMessage, _Mapping]]] = ...) -> None: ...

class GetRunningJobRequest(_message.Message):
    __slots__ = ["machineID"]
    MACHINEID_FIELD_NUMBER: _ClassVar[int]
    machineID: str
    def __init__(self, machineID: _Optional[str] = ...) -> None: ...

class GetRunningJobResponse(_message.Message):
    __slots__ = ["machineID", "jobId"]
    MACHINEID_FIELD_NUMBER: _ClassVar[int]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    machineID: str
    jobId: str
    def __init__(self, machineID: _Optional[str] = ..., jobId: _Optional[str] = ...) -> None: ...

class ListOpenQuantumMachinesResponse(_message.Message):
    __slots__ = ["machineIDs"]
    MACHINEIDS_FIELD_NUMBER: _ClassVar[int]
    machineIDs: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, machineIDs: _Optional[_Iterable[str]] = ...) -> None: ...

class CloseAllQuantumMachinesResponse(_message.Message):
    __slots__ = ["success", "errors"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    errors: _containers.RepeatedCompositeFieldContainer[_general_messages_pb2.ErrorMessage]
    def __init__(self, success: bool = ..., errors: _Optional[_Iterable[_Union[_general_messages_pb2.ErrorMessage, _Mapping]]] = ...) -> None: ...

class GetControllersResponse(_message.Message):
    __slots__ = ["controllers"]
    CONTROLLERS_FIELD_NUMBER: _ClassVar[int]
    controllers: _containers.RepeatedCompositeFieldContainer[Controller]
    def __init__(self, controllers: _Optional[_Iterable[_Union[Controller, _Mapping]]] = ...) -> None: ...

class Controller(_message.Message):
    __slots__ = ["name", "temperature"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    name: str
    temperature: float
    def __init__(self, name: _Optional[str] = ..., temperature: _Optional[float] = ...) -> None: ...

class ConfigValidationMessage(_message.Message):
    __slots__ = ["message", "group", "path", "level"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    message: str
    group: str
    path: str
    level: _general_messages_pb2.MessageLevel
    def __init__(self, message: _Optional[str] = ..., group: _Optional[str] = ..., path: _Optional[str] = ..., level: _Optional[_Union[_general_messages_pb2.MessageLevel, str]] = ...) -> None: ...

class PhysicalValidationMessage(_message.Message):
    __slots__ = ["message", "group", "path", "level"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    message: str
    group: str
    path: str
    level: _general_messages_pb2.MessageLevel
    def __init__(self, message: _Optional[str] = ..., group: _Optional[str] = ..., path: _Optional[str] = ..., level: _Optional[_Union[_general_messages_pb2.MessageLevel, str]] = ...) -> None: ...

class OpenQmWarning(_message.Message):
    __slots__ = ["code", "message"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: int
    message: str
    def __init__(self, code: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...
