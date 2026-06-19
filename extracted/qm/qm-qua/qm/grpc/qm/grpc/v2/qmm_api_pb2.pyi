from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from qm.grpc.qm.grpc.v2 import common_types_pb2 as _common_types_pb2
from qm.grpc.qm.pb import compiler_pb2 as _compiler_pb2
from qm.grpc.qm.pb import frontend_pb2 as _frontend_pb2
from qm.grpc.qm.pb import inc_qua_pb2 as _inc_qua_pb2
from qm.grpc.qm.pb import inc_qua_config_pb2 as _inc_qua_config_pb2
from qm.grpc.qm.pb import qm_manager_pb2 as _qm_manager_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetVersionRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class QmmServiceResetDataProcessingRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class QmmServiceGetQuantumMachineRequest(_message.Message):
    __slots__ = ["machine_id"]
    MACHINE_ID_FIELD_NUMBER: _ClassVar[int]
    machine_id: str
    def __init__(self, machine_id: _Optional[str] = ...) -> None: ...

class QmmServiceCloseQuantumMachineRequest(_message.Message):
    __slots__ = ["machine_id"]
    MACHINE_ID_FIELD_NUMBER: _ClassVar[int]
    machine_id: str
    def __init__(self, machine_id: _Optional[str] = ...) -> None: ...

class HealthCheckRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class HealthCheckResponse(_message.Message):
    __slots__ = ["success", "error"]
    class HealthCheckResponseSuccess(_message.Message):
        __slots__ = ["ok", "components", "details"]
        class ComponentsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: HealthCheckResponse.HealthCheckResponseSuccess
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[HealthCheckResponse.HealthCheckResponseSuccess, _Mapping]] = ...) -> None: ...
        class DetailsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: _any_pb2.Any
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...
        OK_FIELD_NUMBER: _ClassVar[int]
        COMPONENTS_FIELD_NUMBER: _ClassVar[int]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        ok: bool
        components: _containers.MessageMap[str, HealthCheckResponse.HealthCheckResponseSuccess]
        details: _containers.MessageMap[str, _any_pb2.Any]
        def __init__(self, ok: bool = ..., components: _Optional[_Mapping[str, HealthCheckResponse.HealthCheckResponseSuccess]] = ..., details: _Optional[_Mapping[str, _any_pb2.Any]] = ...) -> None: ...
    class HealthCheckResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: HealthCheckResponse.HealthCheckResponseSuccess
    error: HealthCheckResponse.HealthCheckResponseError
    def __init__(self, success: _Optional[_Union[HealthCheckResponse.HealthCheckResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[HealthCheckResponse.HealthCheckResponseError, _Mapping]] = ...) -> None: ...

class OpenQuantumMachineRequest(_message.Message):
    __slots__ = ["config", "close_mode"]
    class CloseMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        CLOSE_MODE_UNSPECIFIED: _ClassVar[OpenQuantumMachineRequest.CloseMode]
        CLOSE_MODE_IF_NEEDED: _ClassVar[OpenQuantumMachineRequest.CloseMode]
        CLOSE_MODE_ALL: _ClassVar[OpenQuantumMachineRequest.CloseMode]
    CLOSE_MODE_UNSPECIFIED: OpenQuantumMachineRequest.CloseMode
    CLOSE_MODE_IF_NEEDED: OpenQuantumMachineRequest.CloseMode
    CLOSE_MODE_ALL: OpenQuantumMachineRequest.CloseMode
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    CLOSE_MODE_FIELD_NUMBER: _ClassVar[int]
    config: _inc_qua_config_pb2.QuaConfig
    close_mode: OpenQuantumMachineRequest.CloseMode
    def __init__(self, config: _Optional[_Union[_inc_qua_config_pb2.QuaConfig, _Mapping]] = ..., close_mode: _Optional[_Union[OpenQuantumMachineRequest.CloseMode, str]] = ...) -> None: ...

class OpenQuantumMachineResponse(_message.Message):
    __slots__ = ["success", "error"]
    class OpenQuantumMachineResponseSuccess(_message.Message):
        __slots__ = ["quantum_machine_id", "open_qm_warnings"]
        QUANTUM_MACHINE_ID_FIELD_NUMBER: _ClassVar[int]
        OPEN_QM_WARNINGS_FIELD_NUMBER: _ClassVar[int]
        quantum_machine_id: str
        open_qm_warnings: _containers.RepeatedCompositeFieldContainer[_qm_manager_pb2.OpenQmWarning]
        def __init__(self, quantum_machine_id: _Optional[str] = ..., open_qm_warnings: _Optional[_Iterable[_Union[_qm_manager_pb2.OpenQmWarning, _Mapping]]] = ...) -> None: ...
    class OpenQuantumMachineResponseError(_message.Message):
        __slots__ = ["config_validation_errors", "physical_validation_errors"]
        CONFIG_VALIDATION_ERRORS_FIELD_NUMBER: _ClassVar[int]
        PHYSICAL_VALIDATION_ERRORS_FIELD_NUMBER: _ClassVar[int]
        config_validation_errors: _containers.RepeatedCompositeFieldContainer[_qm_manager_pb2.ConfigValidationMessage]
        physical_validation_errors: _containers.RepeatedCompositeFieldContainer[_qm_manager_pb2.PhysicalValidationMessage]
        def __init__(self, config_validation_errors: _Optional[_Iterable[_Union[_qm_manager_pb2.ConfigValidationMessage, _Mapping]]] = ..., physical_validation_errors: _Optional[_Iterable[_Union[_qm_manager_pb2.PhysicalValidationMessage, _Mapping]]] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: OpenQuantumMachineResponse.OpenQuantumMachineResponseSuccess
    error: OpenQuantumMachineResponse.OpenQuantumMachineResponseError
    def __init__(self, success: _Optional[_Union[OpenQuantumMachineResponse.OpenQuantumMachineResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[OpenQuantumMachineResponse.OpenQuantumMachineResponseError, _Mapping]] = ...) -> None: ...

class GetQuantumMachineResponse(_message.Message):
    __slots__ = ["success", "error"]
    class GetQuantumMachineResponseSuccess(_message.Message):
        __slots__ = ["machine_id", "config"]
        MACHINE_ID_FIELD_NUMBER: _ClassVar[int]
        CONFIG_FIELD_NUMBER: _ClassVar[int]
        machine_id: str
        config: _inc_qua_config_pb2.QuaConfig
        def __init__(self, machine_id: _Optional[str] = ..., config: _Optional[_Union[_inc_qua_config_pb2.QuaConfig, _Mapping]] = ...) -> None: ...
    class GetQuantumMachineResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: GetQuantumMachineResponse.GetQuantumMachineResponseSuccess
    error: GetQuantumMachineResponse.GetQuantumMachineResponseError
    def __init__(self, success: _Optional[_Union[GetQuantumMachineResponse.GetQuantumMachineResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[GetQuantumMachineResponse.GetQuantumMachineResponseError, _Mapping]] = ...) -> None: ...

class GetControllersRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListOpenQuantumMachinesRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListOpenQuantumMachinesResponse(_message.Message):
    __slots__ = ["success", "error"]
    class ListOpenQuantumMachinesResponseSuccess(_message.Message):
        __slots__ = ["machine_ids"]
        MACHINE_IDS_FIELD_NUMBER: _ClassVar[int]
        machine_ids: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, machine_ids: _Optional[_Iterable[str]] = ...) -> None: ...
    class ListOpenQuantumMachinesResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: ListOpenQuantumMachinesResponse.ListOpenQuantumMachinesResponseSuccess
    error: ListOpenQuantumMachinesResponse.ListOpenQuantumMachinesResponseError
    def __init__(self, success: _Optional[_Union[ListOpenQuantumMachinesResponse.ListOpenQuantumMachinesResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[ListOpenQuantumMachinesResponse.ListOpenQuantumMachinesResponseError, _Mapping]] = ...) -> None: ...

class CloseAllQuantumMachinesRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class JobsQueryParams(_message.Message):
    __slots__ = ["quantum_machine_ids", "job_ids", "user_ids", "description", "status"]
    QUANTUM_MACHINE_IDS_FIELD_NUMBER: _ClassVar[int]
    JOB_IDS_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    quantum_machine_ids: _containers.RepeatedScalarFieldContainer[str]
    job_ids: _containers.RepeatedScalarFieldContainer[str]
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    description: str
    status: _containers.RepeatedScalarFieldContainer[_common_types_pb2.JobExecutionStatus]
    def __init__(self, quantum_machine_ids: _Optional[_Iterable[str]] = ..., job_ids: _Optional[_Iterable[str]] = ..., user_ids: _Optional[_Iterable[str]] = ..., description: _Optional[str] = ..., status: _Optional[_Iterable[_Union[_common_types_pb2.JobExecutionStatus, str]]] = ...) -> None: ...

class JobResponseData(_message.Message):
    __slots__ = ["job_id", "description", "status", "metadata", "is_simulation"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    IS_SIMULATION_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    description: str
    status: _common_types_pb2.JobExecutionStatus
    metadata: JobMetadata
    is_simulation: bool
    def __init__(self, job_id: _Optional[str] = ..., description: _Optional[str] = ..., status: _Optional[_Union[_common_types_pb2.JobExecutionStatus, str]] = ..., metadata: _Optional[_Union[JobMetadata, _Mapping]] = ..., is_simulation: bool = ...) -> None: ...

class JobMetadata(_message.Message):
    __slots__ = ["created_at", "started_at", "last_status_updated_at"]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    LAST_STATUS_UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    created_at: _timestamp_pb2.Timestamp
    started_at: _timestamp_pb2.Timestamp
    last_status_updated_at: _timestamp_pb2.Timestamp
    def __init__(self, created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., started_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., last_status_updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GetJobsRequest(_message.Message):
    __slots__ = ["query"]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    query: JobsQueryParams
    def __init__(self, query: _Optional[_Union[JobsQueryParams, _Mapping]] = ...) -> None: ...

class GetJobsResponse(_message.Message):
    __slots__ = ["success", "error"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: GetJobsSuccess
    error: GetJobsError
    def __init__(self, success: _Optional[_Union[GetJobsSuccess, _Mapping]] = ..., error: _Optional[_Union[GetJobsError, _Mapping]] = ...) -> None: ...

class GetJobsError(_message.Message):
    __slots__ = ["details"]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    details: str
    def __init__(self, details: _Optional[str] = ...) -> None: ...

class GetJobsSuccess(_message.Message):
    __slots__ = ["jobs"]
    JOBS_FIELD_NUMBER: _ClassVar[int]
    jobs: _containers.RepeatedCompositeFieldContainer[JobResponseData]
    def __init__(self, jobs: _Optional[_Iterable[_Union[JobResponseData, _Mapping]]] = ...) -> None: ...

class GetControllersResponse(_message.Message):
    __slots__ = ["success", "error"]
    class FemType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        FEM_TYPE_UNSPECIFIED: _ClassVar[GetControllersResponse.FemType]
        FEM_TYPE_LF: _ClassVar[GetControllersResponse.FemType]
        FEM_TYPE_MW: _ClassVar[GetControllersResponse.FemType]
    FEM_TYPE_UNSPECIFIED: GetControllersResponse.FemType
    FEM_TYPE_LF: GetControllersResponse.FemType
    FEM_TYPE_MW: GetControllersResponse.FemType
    class ControllerType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        CONTROLLER_TYPE_UNSPECIFIED: _ClassVar[GetControllersResponse.ControllerType]
        CONTROLLER_TYPE_OPX_1000: _ClassVar[GetControllersResponse.ControllerType]
    CONTROLLER_TYPE_UNSPECIFIED: GetControllersResponse.ControllerType
    CONTROLLER_TYPE_OPX_1000: GetControllersResponse.ControllerType
    class GetControllersResponseSuccess(_message.Message):
        __slots__ = ["control_devices"]
        class ControlDevicesEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: GetControllersResponse.Controller
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[GetControllersResponse.Controller, _Mapping]] = ...) -> None: ...
        CONTROL_DEVICES_FIELD_NUMBER: _ClassVar[int]
        control_devices: _containers.MessageMap[str, GetControllersResponse.Controller]
        def __init__(self, control_devices: _Optional[_Mapping[str, GetControllersResponse.Controller]] = ...) -> None: ...
    class GetControllersResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    class Controller(_message.Message):
        __slots__ = ["hostname", "controller_type", "fems", "temperatures"]
        class FemsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: int
            value: GetControllersResponse.Fem
            def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[GetControllersResponse.Fem, _Mapping]] = ...) -> None: ...
        class TemperaturesEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: float
            def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
        HOSTNAME_FIELD_NUMBER: _ClassVar[int]
        CONTROLLER_TYPE_FIELD_NUMBER: _ClassVar[int]
        FEMS_FIELD_NUMBER: _ClassVar[int]
        TEMPERATURES_FIELD_NUMBER: _ClassVar[int]
        hostname: str
        controller_type: GetControllersResponse.ControllerType
        fems: _containers.MessageMap[int, GetControllersResponse.Fem]
        temperatures: _containers.ScalarMap[str, float]
        def __init__(self, hostname: _Optional[str] = ..., controller_type: _Optional[_Union[GetControllersResponse.ControllerType, str]] = ..., fems: _Optional[_Mapping[int, GetControllersResponse.Fem]] = ..., temperatures: _Optional[_Mapping[str, float]] = ...) -> None: ...
    class Fem(_message.Message):
        __slots__ = ["type"]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        type: GetControllersResponse.FemType
        def __init__(self, type: _Optional[_Union[GetControllersResponse.FemType, str]] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: GetControllersResponse.GetControllersResponseSuccess
    error: GetControllersResponse.GetControllersResponseError
    def __init__(self, success: _Optional[_Union[GetControllersResponse.GetControllersResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[GetControllersResponse.GetControllersResponseError, _Mapping]] = ...) -> None: ...

class GetVersionResponse(_message.Message):
    __slots__ = ["success", "error"]
    class GetVersionResponseSuccess(_message.Message):
        __slots__ = ["gateway", "controllers"]
        class ControllersEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
        GATEWAY_FIELD_NUMBER: _ClassVar[int]
        CONTROLLERS_FIELD_NUMBER: _ClassVar[int]
        gateway: str
        controllers: _containers.ScalarMap[str, str]
        def __init__(self, gateway: _Optional[str] = ..., controllers: _Optional[_Mapping[str, str]] = ...) -> None: ...
    class GetVersionResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: GetVersionResponse.GetVersionResponseSuccess
    error: GetVersionResponse.GetVersionResponseError
    def __init__(self, success: _Optional[_Union[GetVersionResponse.GetVersionResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[GetVersionResponse.GetVersionResponseError, _Mapping]] = ...) -> None: ...

class QmmServiceSimulateRequest(_message.Message):
    __slots__ = ["config", "high_level_program", "simulate", "controller_connections"]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    HIGH_LEVEL_PROGRAM_FIELD_NUMBER: _ClassVar[int]
    SIMULATE_FIELD_NUMBER: _ClassVar[int]
    CONTROLLER_CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    config: _inc_qua_config_pb2.QuaConfig
    high_level_program: _inc_qua_pb2.QuaProgram
    simulate: _frontend_pb2.ExecutionRequest.Simulate
    controller_connections: _containers.RepeatedCompositeFieldContainer[_frontend_pb2.InterOpxConnection]
    def __init__(self, config: _Optional[_Union[_inc_qua_config_pb2.QuaConfig, _Mapping]] = ..., high_level_program: _Optional[_Union[_inc_qua_pb2.QuaProgram, _Mapping]] = ..., simulate: _Optional[_Union[_frontend_pb2.ExecutionRequest.Simulate, _Mapping]] = ..., controller_connections: _Optional[_Iterable[_Union[_frontend_pb2.InterOpxConnection, _Mapping]]] = ...) -> None: ...

class QmmServiceSimulateResponse(_message.Message):
    __slots__ = ["success", "error"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: SimulationSuccess
    error: SimulationError
    def __init__(self, success: _Optional[_Union[SimulationSuccess, _Mapping]] = ..., error: _Optional[_Union[SimulationError, _Mapping]] = ...) -> None: ...

class SimulationSuccess(_message.Message):
    __slots__ = ["job_id", "messages", "simulated"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    SIMULATED_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    messages: _containers.RepeatedCompositeFieldContainer[_compiler_pb2.CompilerMessage]
    simulated: _frontend_pb2.SimulatedResponsePart
    def __init__(self, job_id: _Optional[str] = ..., messages: _Optional[_Iterable[_Union[_compiler_pb2.CompilerMessage, _Mapping]]] = ..., simulated: _Optional[_Union[_frontend_pb2.SimulatedResponsePart, _Mapping]] = ...) -> None: ...

class SimulationError(_message.Message):
    __slots__ = ["details", "config_validation_errors", "physical_validation_errors", "messages"]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_VALIDATION_ERRORS_FIELD_NUMBER: _ClassVar[int]
    PHYSICAL_VALIDATION_ERRORS_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    details: str
    config_validation_errors: _containers.RepeatedCompositeFieldContainer[_qm_manager_pb2.ConfigValidationMessage]
    physical_validation_errors: _containers.RepeatedCompositeFieldContainer[_qm_manager_pb2.PhysicalValidationMessage]
    messages: _containers.RepeatedCompositeFieldContainer[_compiler_pb2.CompilerMessage]
    def __init__(self, details: _Optional[str] = ..., config_validation_errors: _Optional[_Iterable[_Union[_qm_manager_pb2.ConfigValidationMessage, _Mapping]]] = ..., physical_validation_errors: _Optional[_Iterable[_Union[_qm_manager_pb2.PhysicalValidationMessage, _Mapping]]] = ..., messages: _Optional[_Iterable[_Union[_compiler_pb2.CompilerMessage, _Mapping]]] = ...) -> None: ...

class ResetDataProcessingResponse(_message.Message):
    __slots__ = ["success", "error"]
    class ResetDataProcessingResponseSuccess(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    class ResetDataProcessingResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: ResetDataProcessingResponse.ResetDataProcessingResponseSuccess
    error: ResetDataProcessingResponse.ResetDataProcessingResponseError
    def __init__(self, success: _Optional[_Union[ResetDataProcessingResponse.ResetDataProcessingResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[ResetDataProcessingResponse.ResetDataProcessingResponseError, _Mapping]] = ...) -> None: ...

class CloseQuantumMachineResponse(_message.Message):
    __slots__ = ["success", "error"]
    class CloseQuantumMachineResponseSuccess(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    class CloseQuantumMachineResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: CloseQuantumMachineResponse.CloseQuantumMachineResponseSuccess
    error: CloseQuantumMachineResponse.CloseQuantumMachineResponseError
    def __init__(self, success: _Optional[_Union[CloseQuantumMachineResponse.CloseQuantumMachineResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[CloseQuantumMachineResponse.CloseQuantumMachineResponseError, _Mapping]] = ...) -> None: ...

class CloseAllQuantumMachinesResponse(_message.Message):
    __slots__ = ["success", "error"]
    class CloseAllQuantumMachinesResponseSuccess(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    class CloseAllQuantumMachinesResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: CloseAllQuantumMachinesResponse.CloseAllQuantumMachinesResponseSuccess
    error: CloseAllQuantumMachinesResponse.CloseAllQuantumMachinesResponseError
    def __init__(self, success: _Optional[_Union[CloseAllQuantumMachinesResponse.CloseAllQuantumMachinesResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[CloseAllQuantumMachinesResponse.CloseAllQuantumMachinesResponseError, _Mapping]] = ...) -> None: ...

class ClearAllJobResultsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ClearAllJobResultsResponse(_message.Message):
    __slots__ = ["success", "error"]
    class ClearAllJobResultsResponseSuccess(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    class ClearAllJobResultsResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: ClearAllJobResultsResponse.ClearAllJobResultsResponseSuccess
    error: ClearAllJobResultsResponse.ClearAllJobResultsResponseError
    def __init__(self, success: _Optional[_Union[ClearAllJobResultsResponse.ClearAllJobResultsResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[ClearAllJobResultsResponse.ClearAllJobResultsResponseError, _Mapping]] = ...) -> None: ...
