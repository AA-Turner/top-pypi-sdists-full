from qm.grpc.qm.grpc.v2 import common_types_pb2 as _common_types_pb2
from qm.grpc.qm.grpc.v2 import qmm_api_pb2 as _qmm_api_pb2
from qm.grpc.qm.pb import compiler_pb2 as _compiler_pb2
from qm.grpc.qm.pb import frontend_pb2 as _frontend_pb2
from qm.grpc.qm.pb import inc_qua_pb2 as _inc_qua_pb2
from qm.grpc.qm.pb import inc_qua_config_pb2 as _inc_qua_config_pb2
from qm.grpc.qm.pb import qm_manager_pb2 as _qm_manager_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QmServiceGetConfigRequest(_message.Message):
    __slots__ = ["quantum_machine_id"]
    QUANTUM_MACHINE_ID_FIELD_NUMBER: _ClassVar[int]
    quantum_machine_id: str
    def __init__(self, quantum_machine_id: _Optional[str] = ...) -> None: ...

class UpdateConfigRequest(_message.Message):
    __slots__ = ["quantum_machine_id", "config"]
    QUANTUM_MACHINE_ID_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    quantum_machine_id: str
    config: _inc_qua_config_pb2.QuaConfig
    def __init__(self, quantum_machine_id: _Optional[str] = ..., config: _Optional[_Union[_inc_qua_config_pb2.QuaConfig, _Mapping]] = ...) -> None: ...

class UpdateConfigResponse(_message.Message):
    __slots__ = ["success", "error"]
    class UpdateConfigResponseSuccess(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    class UpdateConfigResponseError(_message.Message):
        __slots__ = ["details", "config_validation_errors"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        CONFIG_VALIDATION_ERRORS_FIELD_NUMBER: _ClassVar[int]
        details: str
        config_validation_errors: _containers.RepeatedCompositeFieldContainer[_qm_manager_pb2.ConfigValidationMessage]
        def __init__(self, details: _Optional[str] = ..., config_validation_errors: _Optional[_Iterable[_Union[_qm_manager_pb2.ConfigValidationMessage, _Mapping]]] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: UpdateConfigResponse.UpdateConfigResponseSuccess
    error: UpdateConfigResponse.UpdateConfigResponseError
    def __init__(self, success: _Optional[_Union[UpdateConfigResponse.UpdateConfigResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[UpdateConfigResponse.UpdateConfigResponseError, _Mapping]] = ...) -> None: ...

class QmServiceCloseRequest(_message.Message):
    __slots__ = ["quantum_machine_id"]
    QUANTUM_MACHINE_ID_FIELD_NUMBER: _ClassVar[int]
    quantum_machine_id: str
    def __init__(self, quantum_machine_id: _Optional[str] = ...) -> None: ...

class QmServiceCloseResponse(_message.Message):
    __slots__ = ["success", "error"]
    class QmServiceCloseResponseSuccess(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    class QmServiceCloseResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: QmServiceCloseResponse.QmServiceCloseResponseSuccess
    error: QmServiceCloseResponse.QmServiceCloseResponseError
    def __init__(self, success: _Optional[_Union[QmServiceCloseResponse.QmServiceCloseResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[QmServiceCloseResponse.QmServiceCloseResponseError, _Mapping]] = ...) -> None: ...

class QmServiceSimulateRequest(_message.Message):
    __slots__ = ["quantum_machine_id", "high_level_program", "simulate", "controller_connections", "config"]
    QUANTUM_MACHINE_ID_FIELD_NUMBER: _ClassVar[int]
    HIGH_LEVEL_PROGRAM_FIELD_NUMBER: _ClassVar[int]
    SIMULATE_FIELD_NUMBER: _ClassVar[int]
    CONTROLLER_CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    quantum_machine_id: str
    high_level_program: _inc_qua_pb2.QuaProgram
    simulate: _frontend_pb2.ExecutionRequest.Simulate
    controller_connections: _containers.RepeatedCompositeFieldContainer[_frontend_pb2.InterOpxConnection]
    config: _inc_qua_config_pb2.QuaConfig
    def __init__(self, quantum_machine_id: _Optional[str] = ..., high_level_program: _Optional[_Union[_inc_qua_pb2.QuaProgram, _Mapping]] = ..., simulate: _Optional[_Union[_frontend_pb2.ExecutionRequest.Simulate, _Mapping]] = ..., controller_connections: _Optional[_Iterable[_Union[_frontend_pb2.InterOpxConnection, _Mapping]]] = ..., config: _Optional[_Union[_inc_qua_config_pb2.QuaConfig, _Mapping]] = ...) -> None: ...

class QmServiceSimulateResponse(_message.Message):
    __slots__ = ["success", "error"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: _qmm_api_pb2.SimulationSuccess
    error: _qmm_api_pb2.SimulationError
    def __init__(self, success: _Optional[_Union[_qmm_api_pb2.SimulationSuccess, _Mapping]] = ..., error: _Optional[_Union[_qmm_api_pb2.SimulationError, _Mapping]] = ...) -> None: ...

class QmServiceSimulateCompiledRequest(_message.Message):
    __slots__ = ["quantum_machine_id", "program_id", "simulate", "controller_connections"]
    QUANTUM_MACHINE_ID_FIELD_NUMBER: _ClassVar[int]
    PROGRAM_ID_FIELD_NUMBER: _ClassVar[int]
    SIMULATE_FIELD_NUMBER: _ClassVar[int]
    CONTROLLER_CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    quantum_machine_id: str
    program_id: str
    simulate: _frontend_pb2.ExecutionRequest.Simulate
    controller_connections: _containers.RepeatedCompositeFieldContainer[_frontend_pb2.InterOpxConnection]
    def __init__(self, quantum_machine_id: _Optional[str] = ..., program_id: _Optional[str] = ..., simulate: _Optional[_Union[_frontend_pb2.ExecutionRequest.Simulate, _Mapping]] = ..., controller_connections: _Optional[_Iterable[_Union[_frontend_pb2.InterOpxConnection, _Mapping]]] = ...) -> None: ...

class QmServiceSimulateCompiledResponse(_message.Message):
    __slots__ = ["success", "error"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: SimulateCompiledSuccess
    error: SimulateCompiledError
    def __init__(self, success: _Optional[_Union[SimulateCompiledSuccess, _Mapping]] = ..., error: _Optional[_Union[SimulateCompiledError, _Mapping]] = ...) -> None: ...

class SimulateCompiledSuccess(_message.Message):
    __slots__ = ["job_id"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class SimulateCompiledError(_message.Message):
    __slots__ = ["details"]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    details: str
    def __init__(self, details: _Optional[str] = ...) -> None: ...

class QmServiceJobsQueryParams(_message.Message):
    __slots__ = ["quantum_machine_id", "job_ids", "user_ids", "description", "status"]
    QUANTUM_MACHINE_ID_FIELD_NUMBER: _ClassVar[int]
    JOB_IDS_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    quantum_machine_id: str
    job_ids: _containers.RepeatedScalarFieldContainer[str]
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    description: str
    status: _containers.RepeatedScalarFieldContainer[_common_types_pb2.JobExecutionStatus]
    def __init__(self, quantum_machine_id: _Optional[str] = ..., job_ids: _Optional[_Iterable[str]] = ..., user_ids: _Optional[_Iterable[str]] = ..., description: _Optional[str] = ..., status: _Optional[_Iterable[_Union[_common_types_pb2.JobExecutionStatus, str]]] = ...) -> None: ...

class QmServiceGetJobsRequest(_message.Message):
    __slots__ = ["query"]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    query: _qmm_api_pb2.JobsQueryParams
    def __init__(self, query: _Optional[_Union[_qmm_api_pb2.JobsQueryParams, _Mapping]] = ...) -> None: ...

class RemoveJobsRequest(_message.Message):
    __slots__ = ["query"]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    query: _qmm_api_pb2.JobsQueryParams
    def __init__(self, query: _Optional[_Union[_qmm_api_pb2.JobsQueryParams, _Mapping]] = ...) -> None: ...

class RemoveJobsResponse(_message.Message):
    __slots__ = ["success", "error"]
    class RemoveJobsResponseSuccess(_message.Message):
        __slots__ = ["removed_job_ids"]
        REMOVED_JOB_IDS_FIELD_NUMBER: _ClassVar[int]
        removed_job_ids: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, removed_job_ids: _Optional[_Iterable[str]] = ...) -> None: ...
    class RemoveJobsResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: RemoveJobsResponse.RemoveJobsResponseSuccess
    error: RemoveJobsResponse.RemoveJobsResponseError
    def __init__(self, success: _Optional[_Union[RemoveJobsResponse.RemoveJobsResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[RemoveJobsResponse.RemoveJobsResponseError, _Mapping]] = ...) -> None: ...

class QmServiceGetConfigResponse(_message.Message):
    __slots__ = ["success", "error"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: GetConfigSuccess
    error: GetConfigError
    def __init__(self, success: _Optional[_Union[GetConfigSuccess, _Mapping]] = ..., error: _Optional[_Union[GetConfigError, _Mapping]] = ...) -> None: ...

class GetConfigSuccess(_message.Message):
    __slots__ = ["config"]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: _inc_qua_config_pb2.QuaConfig
    def __init__(self, config: _Optional[_Union[_inc_qua_config_pb2.QuaConfig, _Mapping]] = ...) -> None: ...

class GetConfigError(_message.Message):
    __slots__ = ["details"]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    details: str
    def __init__(self, details: _Optional[str] = ...) -> None: ...

class QmServiceCompileRequest(_message.Message):
    __slots__ = ["quantum_machine_id", "high_level_program", "config"]
    QUANTUM_MACHINE_ID_FIELD_NUMBER: _ClassVar[int]
    HIGH_LEVEL_PROGRAM_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    quantum_machine_id: str
    high_level_program: _inc_qua_pb2.QuaProgram
    config: _inc_qua_config_pb2.QuaConfig
    def __init__(self, quantum_machine_id: _Optional[str] = ..., high_level_program: _Optional[_Union[_inc_qua_pb2.QuaProgram, _Mapping]] = ..., config: _Optional[_Union[_inc_qua_config_pb2.QuaConfig, _Mapping]] = ...) -> None: ...

class CompileResponse(_message.Message):
    __slots__ = ["success", "error"]
    class CompilationSuccess(_message.Message):
        __slots__ = ["program_id", "messages"]
        PROGRAM_ID_FIELD_NUMBER: _ClassVar[int]
        MESSAGES_FIELD_NUMBER: _ClassVar[int]
        program_id: str
        messages: _containers.RepeatedCompositeFieldContainer[_compiler_pb2.CompilerMessage]
        def __init__(self, program_id: _Optional[str] = ..., messages: _Optional[_Iterable[_Union[_compiler_pb2.CompilerMessage, _Mapping]]] = ...) -> None: ...
    class CompilationError(_message.Message):
        __slots__ = ["details", "messages", "config_validation_errors"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        MESSAGES_FIELD_NUMBER: _ClassVar[int]
        CONFIG_VALIDATION_ERRORS_FIELD_NUMBER: _ClassVar[int]
        details: str
        messages: _containers.RepeatedCompositeFieldContainer[_compiler_pb2.CompilerMessage]
        config_validation_errors: _containers.RepeatedCompositeFieldContainer[_qm_manager_pb2.ConfigValidationMessage]
        def __init__(self, details: _Optional[str] = ..., messages: _Optional[_Iterable[_Union[_compiler_pb2.CompilerMessage, _Mapping]]] = ..., config_validation_errors: _Optional[_Iterable[_Union[_qm_manager_pb2.ConfigValidationMessage, _Mapping]]] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: CompileResponse.CompilationSuccess
    error: CompileResponse.CompilationError
    def __init__(self, success: _Optional[_Union[CompileResponse.CompilationSuccess, _Mapping]] = ..., error: _Optional[_Union[CompileResponse.CompilationError, _Mapping]] = ...) -> None: ...

class QmServiceAddToQueueRequest(_message.Message):
    __slots__ = ["quantum_machine_id", "high_level_program", "queue_position", "config"]
    QUANTUM_MACHINE_ID_FIELD_NUMBER: _ClassVar[int]
    HIGH_LEVEL_PROGRAM_FIELD_NUMBER: _ClassVar[int]
    QUEUE_POSITION_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    quantum_machine_id: str
    high_level_program: _inc_qua_pb2.QuaProgram
    queue_position: _frontend_pb2.QueuePosition
    config: _inc_qua_config_pb2.QuaConfig
    def __init__(self, quantum_machine_id: _Optional[str] = ..., high_level_program: _Optional[_Union[_inc_qua_pb2.QuaProgram, _Mapping]] = ..., queue_position: _Optional[_Union[_frontend_pb2.QueuePosition, _Mapping]] = ..., config: _Optional[_Union[_inc_qua_config_pb2.QuaConfig, _Mapping]] = ...) -> None: ...

class AddToQueueResponse(_message.Message):
    __slots__ = ["success", "error"]
    class AddToQueueResponseSuccess(_message.Message):
        __slots__ = ["job_id", "messages"]
        JOB_ID_FIELD_NUMBER: _ClassVar[int]
        MESSAGES_FIELD_NUMBER: _ClassVar[int]
        job_id: str
        messages: _containers.RepeatedCompositeFieldContainer[_compiler_pb2.CompilerMessage]
        def __init__(self, job_id: _Optional[str] = ..., messages: _Optional[_Iterable[_Union[_compiler_pb2.CompilerMessage, _Mapping]]] = ...) -> None: ...
    class AddToQueueResponseError(_message.Message):
        __slots__ = ["details", "messages", "config_validation_errors"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        MESSAGES_FIELD_NUMBER: _ClassVar[int]
        CONFIG_VALIDATION_ERRORS_FIELD_NUMBER: _ClassVar[int]
        details: str
        messages: _containers.RepeatedCompositeFieldContainer[_compiler_pb2.CompilerMessage]
        config_validation_errors: _containers.RepeatedCompositeFieldContainer[_qm_manager_pb2.ConfigValidationMessage]
        def __init__(self, details: _Optional[str] = ..., messages: _Optional[_Iterable[_Union[_compiler_pb2.CompilerMessage, _Mapping]]] = ..., config_validation_errors: _Optional[_Iterable[_Union[_qm_manager_pb2.ConfigValidationMessage, _Mapping]]] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: AddToQueueResponse.AddToQueueResponseSuccess
    error: AddToQueueResponse.AddToQueueResponseError
    def __init__(self, success: _Optional[_Union[AddToQueueResponse.AddToQueueResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[AddToQueueResponse.AddToQueueResponseError, _Mapping]] = ...) -> None: ...

class QmServiceAddCompiledToQueueRequest(_message.Message):
    __slots__ = ["quantum_machine_id", "program_id"]
    QUANTUM_MACHINE_ID_FIELD_NUMBER: _ClassVar[int]
    PROGRAM_ID_FIELD_NUMBER: _ClassVar[int]
    quantum_machine_id: str
    program_id: str
    def __init__(self, quantum_machine_id: _Optional[str] = ..., program_id: _Optional[str] = ...) -> None: ...

class AddCompiledToQueueResponse(_message.Message):
    __slots__ = ["success", "error"]
    class AddCompiledToQueueResponseSuccess(_message.Message):
        __slots__ = ["job_id"]
        JOB_ID_FIELD_NUMBER: _ClassVar[int]
        job_id: str
        def __init__(self, job_id: _Optional[str] = ...) -> None: ...
    class AddCompiledToQueueResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: AddCompiledToQueueResponse.AddCompiledToQueueResponseSuccess
    error: AddCompiledToQueueResponse.AddCompiledToQueueResponseError
    def __init__(self, success: _Optional[_Union[AddCompiledToQueueResponse.AddCompiledToQueueResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[AddCompiledToQueueResponse.AddCompiledToQueueResponseError, _Mapping]] = ...) -> None: ...

class QmServiceGetJobsResponse(_message.Message):
    __slots__ = ["success", "error"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: _qmm_api_pb2.GetJobsSuccess
    error: _qmm_api_pb2.GetJobsError
    def __init__(self, success: _Optional[_Union[_qmm_api_pb2.GetJobsSuccess, _Mapping]] = ..., error: _Optional[_Union[_qmm_api_pb2.GetJobsError, _Mapping]] = ...) -> None: ...

class ResetDigitalFiltersRequest(_message.Message):
    __slots__ = ["quantum_machine_id"]
    QUANTUM_MACHINE_ID_FIELD_NUMBER: _ClassVar[int]
    quantum_machine_id: str
    def __init__(self, quantum_machine_id: _Optional[str] = ...) -> None: ...

class ResetDigitalFiltersResponse(_message.Message):
    __slots__ = ["success", "error"]
    class ResetDigitalFiltersResponseSuccess(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    class ResetDigitalFiltersResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: ResetDigitalFiltersResponse.ResetDigitalFiltersResponseSuccess
    error: ResetDigitalFiltersResponse.ResetDigitalFiltersResponseError
    def __init__(self, success: _Optional[_Union[ResetDigitalFiltersResponse.ResetDigitalFiltersResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[ResetDigitalFiltersResponse.ResetDigitalFiltersResponseError, _Mapping]] = ...) -> None: ...
