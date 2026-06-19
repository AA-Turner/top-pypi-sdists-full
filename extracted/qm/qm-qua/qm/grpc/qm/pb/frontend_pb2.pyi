from qm.grpc.qm.pb import inc_qua_pb2 as _inc_qua_pb2
from qm.grpc.qm.pb import inc_qua_config_pb2 as _inc_qua_config_pb2
from qm.grpc.qm.pb import inc_qm_api_pb2 as _inc_qm_api_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from qm.grpc.qm.pb import compiler_pb2 as _compiler_pb2
from qm.grpc.qm.pb import job_results_pb2 as _job_results_pb2
from qm.grpc.qm.pb import qm_manager_pb2 as _qm_manager_pb2
from qm.grpc.qm.pb import general_messages_pb2 as _general_messages_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueuePosition(_message.Message):
    __slots__ = ["end", "start"]
    END_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    end: _empty_pb2.Empty
    start: _empty_pb2.Empty
    def __init__(self, end: _Optional[_Union[_empty_pb2.Empty, _Mapping]] = ..., start: _Optional[_Union[_empty_pb2.Empty, _Mapping]] = ...) -> None: ...

class AddToQueueRequest(_message.Message):
    __slots__ = ["quantumMachineId", "highLevelProgram", "queuePosition"]
    QUANTUMMACHINEID_FIELD_NUMBER: _ClassVar[int]
    HIGHLEVELPROGRAM_FIELD_NUMBER: _ClassVar[int]
    QUEUEPOSITION_FIELD_NUMBER: _ClassVar[int]
    quantumMachineId: str
    highLevelProgram: _inc_qua_pb2.QuaProgram
    queuePosition: QueuePosition
    def __init__(self, quantumMachineId: _Optional[str] = ..., highLevelProgram: _Optional[_Union[_inc_qua_pb2.QuaProgram, _Mapping]] = ..., queuePosition: _Optional[_Union[QueuePosition, _Mapping]] = ...) -> None: ...

class AddToQueueResponse(_message.Message):
    __slots__ = ["ok", "jobId", "messages"]
    OK_FIELD_NUMBER: _ClassVar[int]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    jobId: str
    messages: _containers.RepeatedCompositeFieldContainer[_compiler_pb2.CompilerMessage]
    def __init__(self, ok: bool = ..., jobId: _Optional[str] = ..., messages: _Optional[_Iterable[_Union[_compiler_pb2.CompilerMessage, _Mapping]]] = ...) -> None: ...

class WaveformOverride(_message.Message):
    __slots__ = ["samples"]
    SAMPLES_FIELD_NUMBER: _ClassVar[int]
    samples: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, samples: _Optional[_Iterable[float]] = ...) -> None: ...

class ExecutionOverrides(_message.Message):
    __slots__ = ["waveforms"]
    class WaveformsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: WaveformOverride
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[WaveformOverride, _Mapping]] = ...) -> None: ...
    WAVEFORMS_FIELD_NUMBER: _ClassVar[int]
    waveforms: _containers.MessageMap[str, WaveformOverride]
    def __init__(self, waveforms: _Optional[_Mapping[str, WaveformOverride]] = ...) -> None: ...

class AddCompiledToQueueRequest(_message.Message):
    __slots__ = ["quantumMachineId", "programId", "queuePosition", "executionOverrides"]
    QUANTUMMACHINEID_FIELD_NUMBER: _ClassVar[int]
    PROGRAMID_FIELD_NUMBER: _ClassVar[int]
    QUEUEPOSITION_FIELD_NUMBER: _ClassVar[int]
    EXECUTIONOVERRIDES_FIELD_NUMBER: _ClassVar[int]
    quantumMachineId: str
    programId: str
    queuePosition: QueuePosition
    executionOverrides: ExecutionOverrides
    def __init__(self, quantumMachineId: _Optional[str] = ..., programId: _Optional[str] = ..., queuePosition: _Optional[_Union[QueuePosition, _Mapping]] = ..., executionOverrides: _Optional[_Union[ExecutionOverrides, _Mapping]] = ...) -> None: ...

class AddCompiledToQueueResponse(_message.Message):
    __slots__ = ["ok", "jobId", "errors"]
    OK_FIELD_NUMBER: _ClassVar[int]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    jobId: str
    errors: _containers.RepeatedCompositeFieldContainer[_general_messages_pb2.ErrorMessage]
    def __init__(self, ok: bool = ..., jobId: _Optional[str] = ..., errors: _Optional[_Iterable[_Union[_general_messages_pb2.ErrorMessage, _Mapping]]] = ...) -> None: ...

class CompileRequest(_message.Message):
    __slots__ = ["quantumMachineId", "highLevelProgram"]
    QUANTUMMACHINEID_FIELD_NUMBER: _ClassVar[int]
    HIGHLEVELPROGRAM_FIELD_NUMBER: _ClassVar[int]
    quantumMachineId: str
    highLevelProgram: _inc_qua_pb2.QuaProgram
    def __init__(self, quantumMachineId: _Optional[str] = ..., highLevelProgram: _Optional[_Union[_inc_qua_pb2.QuaProgram, _Mapping]] = ...) -> None: ...

class CompileResponse(_message.Message):
    __slots__ = ["ok", "programId", "messages"]
    OK_FIELD_NUMBER: _ClassVar[int]
    PROGRAMID_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    programId: str
    messages: _containers.RepeatedCompositeFieldContainer[_compiler_pb2.CompilerMessage]
    def __init__(self, ok: bool = ..., programId: _Optional[str] = ..., messages: _Optional[_Iterable[_Union[_compiler_pb2.CompilerMessage, _Mapping]]] = ...) -> None: ...

class GetJobExecutionStatusRequest(_message.Message):
    __slots__ = ["quantumMachineId", "jobId"]
    QUANTUMMACHINEID_FIELD_NUMBER: _ClassVar[int]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    quantumMachineId: str
    jobId: str
    def __init__(self, quantumMachineId: _Optional[str] = ..., jobId: _Optional[str] = ...) -> None: ...

class GetJobExecutionStatusResponse(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: JobExecutionStatus
    def __init__(self, status: _Optional[_Union[JobExecutionStatus, _Mapping]] = ...) -> None: ...

class JobExecutionStatus(_message.Message):
    __slots__ = ["unknown", "pending", "running", "completed", "canceled", "loading", "error", "processing"]
    class Unknown(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    class Pending(_message.Message):
        __slots__ = ["positionInQueue", "timeAdded", "addedBy"]
        POSITIONINQUEUE_FIELD_NUMBER: _ClassVar[int]
        TIMEADDED_FIELD_NUMBER: _ClassVar[int]
        ADDEDBY_FIELD_NUMBER: _ClassVar[int]
        positionInQueue: int
        timeAdded: _timestamp_pb2.Timestamp
        addedBy: str
        def __init__(self, positionInQueue: _Optional[int] = ..., timeAdded: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., addedBy: _Optional[str] = ...) -> None: ...
    class Running(_message.Message):
        __slots__ = ["timeAdded", "addedBy", "timeStarted"]
        TIMEADDED_FIELD_NUMBER: _ClassVar[int]
        ADDEDBY_FIELD_NUMBER: _ClassVar[int]
        TIMESTARTED_FIELD_NUMBER: _ClassVar[int]
        timeAdded: _timestamp_pb2.Timestamp
        addedBy: str
        timeStarted: _timestamp_pb2.Timestamp
        def __init__(self, timeAdded: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., addedBy: _Optional[str] = ..., timeStarted: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
    class Completed(_message.Message):
        __slots__ = ["timeAdded", "addedBy", "timeStarted", "timeCompleted"]
        TIMEADDED_FIELD_NUMBER: _ClassVar[int]
        ADDEDBY_FIELD_NUMBER: _ClassVar[int]
        TIMESTARTED_FIELD_NUMBER: _ClassVar[int]
        TIMECOMPLETED_FIELD_NUMBER: _ClassVar[int]
        timeAdded: _timestamp_pb2.Timestamp
        addedBy: str
        timeStarted: _timestamp_pb2.Timestamp
        timeCompleted: _timestamp_pb2.Timestamp
        def __init__(self, timeAdded: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., addedBy: _Optional[str] = ..., timeStarted: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., timeCompleted: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
    class Canceled(_message.Message):
        __slots__ = ["timeAdded", "addedBy", "timeCanceled"]
        TIMEADDED_FIELD_NUMBER: _ClassVar[int]
        ADDEDBY_FIELD_NUMBER: _ClassVar[int]
        TIMECANCELED_FIELD_NUMBER: _ClassVar[int]
        timeAdded: _timestamp_pb2.Timestamp
        addedBy: str
        timeCanceled: _timestamp_pb2.Timestamp
        def __init__(self, timeAdded: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., addedBy: _Optional[str] = ..., timeCanceled: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
    class Loading(_message.Message):
        __slots__ = ["timeAdded", "addedBy"]
        TIMEADDED_FIELD_NUMBER: _ClassVar[int]
        ADDEDBY_FIELD_NUMBER: _ClassVar[int]
        timeAdded: _timestamp_pb2.Timestamp
        addedBy: str
        def __init__(self, timeAdded: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., addedBy: _Optional[str] = ...) -> None: ...
    class Error(_message.Message):
        __slots__ = ["errorMessages", "addedBy"]
        ERRORMESSAGES_FIELD_NUMBER: _ClassVar[int]
        ADDEDBY_FIELD_NUMBER: _ClassVar[int]
        errorMessages: _struct_pb2.ListValue
        addedBy: str
        def __init__(self, errorMessages: _Optional[_Union[_struct_pb2.ListValue, _Mapping]] = ..., addedBy: _Optional[str] = ...) -> None: ...
    class Processing(_message.Message):
        __slots__ = ["timeAdded", "addedBy", "timeStarted"]
        TIMEADDED_FIELD_NUMBER: _ClassVar[int]
        ADDEDBY_FIELD_NUMBER: _ClassVar[int]
        TIMESTARTED_FIELD_NUMBER: _ClassVar[int]
        timeAdded: _timestamp_pb2.Timestamp
        addedBy: str
        timeStarted: _timestamp_pb2.Timestamp
        def __init__(self, timeAdded: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., addedBy: _Optional[str] = ..., timeStarted: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
    UNKNOWN_FIELD_NUMBER: _ClassVar[int]
    PENDING_FIELD_NUMBER: _ClassVar[int]
    RUNNING_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    CANCELED_FIELD_NUMBER: _ClassVar[int]
    LOADING_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PROCESSING_FIELD_NUMBER: _ClassVar[int]
    unknown: JobExecutionStatus.Unknown
    pending: JobExecutionStatus.Pending
    running: JobExecutionStatus.Running
    completed: JobExecutionStatus.Completed
    canceled: JobExecutionStatus.Canceled
    loading: JobExecutionStatus.Loading
    error: JobExecutionStatus.Error
    processing: JobExecutionStatus.Processing
    def __init__(self, unknown: _Optional[_Union[JobExecutionStatus.Unknown, _Mapping]] = ..., pending: _Optional[_Union[JobExecutionStatus.Pending, _Mapping]] = ..., running: _Optional[_Union[JobExecutionStatus.Running, _Mapping]] = ..., completed: _Optional[_Union[JobExecutionStatus.Completed, _Mapping]] = ..., canceled: _Optional[_Union[JobExecutionStatus.Canceled, _Mapping]] = ..., loading: _Optional[_Union[JobExecutionStatus.Loading, _Mapping]] = ..., error: _Optional[_Union[JobExecutionStatus.Error, _Mapping]] = ..., processing: _Optional[_Union[JobExecutionStatus.Processing, _Mapping]] = ...) -> None: ...

class GetPendingJobsResponse(_message.Message):
    __slots__ = ["pendingJobs"]
    class PendingJobsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: JobExecutionStatus.Pending
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[JobExecutionStatus.Pending, _Mapping]] = ...) -> None: ...
    PENDINGJOBS_FIELD_NUMBER: _ClassVar[int]
    pendingJobs: _containers.MessageMap[str, JobExecutionStatus.Pending]
    def __init__(self, pendingJobs: _Optional[_Mapping[str, JobExecutionStatus.Pending]] = ...) -> None: ...

class JobQueryParams(_message.Message):
    __slots__ = ["quantumMachineId", "jobId", "userId", "position"]
    QUANTUMMACHINEID_FIELD_NUMBER: _ClassVar[int]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    quantumMachineId: str
    jobId: QueryValueMatcher
    userId: QueryValueMatcher
    position: _wrappers_pb2.UInt32Value
    def __init__(self, quantumMachineId: _Optional[str] = ..., jobId: _Optional[_Union[QueryValueMatcher, _Mapping]] = ..., userId: _Optional[_Union[QueryValueMatcher, _Mapping]] = ..., position: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ...) -> None: ...

class QueryValueMatcher(_message.Message):
    __slots__ = ["any", "value"]
    ANY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    any: bool
    value: str
    def __init__(self, any: bool = ..., value: _Optional[str] = ...) -> None: ...

class RemovePendingJobsResponse(_message.Message):
    __slots__ = ["numbersOfJobsRemoved"]
    NUMBERSOFJOBSREMOVED_FIELD_NUMBER: _ClassVar[int]
    numbersOfJobsRemoved: int
    def __init__(self, numbersOfJobsRemoved: _Optional[int] = ...) -> None: ...

class SimulationRequest(_message.Message):
    __slots__ = ["config", "highLevelProgram", "simulate", "controllerConnections"]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    HIGHLEVELPROGRAM_FIELD_NUMBER: _ClassVar[int]
    SIMULATE_FIELD_NUMBER: _ClassVar[int]
    CONTROLLERCONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    config: _inc_qua_config_pb2.QuaConfig
    highLevelProgram: _inc_qua_pb2.QuaProgram
    simulate: ExecutionRequest.Simulate
    controllerConnections: _containers.RepeatedCompositeFieldContainer[InterOpxConnection]
    def __init__(self, config: _Optional[_Union[_inc_qua_config_pb2.QuaConfig, _Mapping]] = ..., highLevelProgram: _Optional[_Union[_inc_qua_pb2.QuaProgram, _Mapping]] = ..., simulate: _Optional[_Union[ExecutionRequest.Simulate, _Mapping]] = ..., controllerConnections: _Optional[_Iterable[_Union[InterOpxConnection, _Mapping]]] = ...) -> None: ...

class InterOpxAddress(_message.Message):
    __slots__ = ["controller", "left"]
    CONTROLLER_FIELD_NUMBER: _ClassVar[int]
    LEFT_FIELD_NUMBER: _ClassVar[int]
    controller: str
    left: bool
    def __init__(self, controller: _Optional[str] = ..., left: bool = ...) -> None: ...

class InterOpxTarget(_message.Message):
    __slots__ = ["direct"]
    DIRECT_FIELD_NUMBER: _ClassVar[int]
    direct: InterOpxAddress
    def __init__(self, direct: _Optional[_Union[InterOpxAddress, _Mapping]] = ...) -> None: ...

class InterOpxChannel(_message.Message):
    __slots__ = ["controller", "channelNumber"]
    CONTROLLER_FIELD_NUMBER: _ClassVar[int]
    CHANNELNUMBER_FIELD_NUMBER: _ClassVar[int]
    controller: str
    channelNumber: int
    def __init__(self, controller: _Optional[str] = ..., channelNumber: _Optional[int] = ...) -> None: ...

class InterOpxConnection(_message.Message):
    __slots__ = ["source", "target", "addressToAddress", "channelToChannel"]
    class AddressToAddress(_message.Message):
        __slots__ = ["source", "target"]
        SOURCE_FIELD_NUMBER: _ClassVar[int]
        TARGET_FIELD_NUMBER: _ClassVar[int]
        source: InterOpxAddress
        target: InterOpxAddress
        def __init__(self, source: _Optional[_Union[InterOpxAddress, _Mapping]] = ..., target: _Optional[_Union[InterOpxAddress, _Mapping]] = ...) -> None: ...
    class ChannelToChannel(_message.Message):
        __slots__ = ["source", "target"]
        SOURCE_FIELD_NUMBER: _ClassVar[int]
        TARGET_FIELD_NUMBER: _ClassVar[int]
        source: InterOpxChannel
        target: InterOpxChannel
        def __init__(self, source: _Optional[_Union[InterOpxChannel, _Mapping]] = ..., target: _Optional[_Union[InterOpxChannel, _Mapping]] = ...) -> None: ...
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    ADDRESSTOADDRESS_FIELD_NUMBER: _ClassVar[int]
    CHANNELTOCHANNEL_FIELD_NUMBER: _ClassVar[int]
    source: InterOpxAddress
    target: InterOpxTarget
    addressToAddress: InterOpxConnection.AddressToAddress
    channelToChannel: InterOpxConnection.ChannelToChannel
    def __init__(self, source: _Optional[_Union[InterOpxAddress, _Mapping]] = ..., target: _Optional[_Union[InterOpxTarget, _Mapping]] = ..., addressToAddress: _Optional[_Union[InterOpxConnection.AddressToAddress, _Mapping]] = ..., channelToChannel: _Optional[_Union[InterOpxConnection.ChannelToChannel, _Mapping]] = ...) -> None: ...

class SimulationResponse(_message.Message):
    __slots__ = ["success", "jobId", "configValidationErrors", "physicalValidationErrors", "messages", "simulated"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    CONFIGVALIDATIONERRORS_FIELD_NUMBER: _ClassVar[int]
    PHYSICALVALIDATIONERRORS_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    SIMULATED_FIELD_NUMBER: _ClassVar[int]
    success: bool
    jobId: str
    configValidationErrors: _containers.RepeatedCompositeFieldContainer[_qm_manager_pb2.ConfigValidationMessage]
    physicalValidationErrors: _containers.RepeatedCompositeFieldContainer[_qm_manager_pb2.PhysicalValidationMessage]
    messages: _containers.RepeatedCompositeFieldContainer[_compiler_pb2.CompilerMessage]
    simulated: SimulatedResponsePart
    def __init__(self, success: bool = ..., jobId: _Optional[str] = ..., configValidationErrors: _Optional[_Iterable[_Union[_qm_manager_pb2.ConfigValidationMessage, _Mapping]]] = ..., physicalValidationErrors: _Optional[_Iterable[_Union[_qm_manager_pb2.PhysicalValidationMessage, _Mapping]]] = ..., messages: _Optional[_Iterable[_Union[_compiler_pb2.CompilerMessage, _Mapping]]] = ..., simulated: _Optional[_Union[SimulatedResponsePart, _Mapping]] = ...) -> None: ...

class IsJobRunningRequest(_message.Message):
    __slots__ = ["jobId"]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    def __init__(self, jobId: _Optional[str] = ...) -> None: ...

class IsJobRunningResponse(_message.Message):
    __slots__ = ["jobId", "isRunning"]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    ISRUNNING_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    isRunning: bool
    def __init__(self, jobId: _Optional[str] = ..., isRunning: bool = ...) -> None: ...

class IsJobAcquiringDataRequest(_message.Message):
    __slots__ = ["jobId"]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    def __init__(self, jobId: _Optional[str] = ...) -> None: ...

class IsJobAcquiringDataResponse(_message.Message):
    __slots__ = ["jobId", "acquiringStatus"]
    class AcquiringStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        ACQUIRE_STOPPED: _ClassVar[IsJobAcquiringDataResponse.AcquiringStatus]
        NO_DATA_TO_ACQUIRE: _ClassVar[IsJobAcquiringDataResponse.AcquiringStatus]
        HAS_DATA_TO_ACQUIRE: _ClassVar[IsJobAcquiringDataResponse.AcquiringStatus]
    ACQUIRE_STOPPED: IsJobAcquiringDataResponse.AcquiringStatus
    NO_DATA_TO_ACQUIRE: IsJobAcquiringDataResponse.AcquiringStatus
    HAS_DATA_TO_ACQUIRE: IsJobAcquiringDataResponse.AcquiringStatus
    JOBID_FIELD_NUMBER: _ClassVar[int]
    ACQUIRINGSTATUS_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    acquiringStatus: IsJobAcquiringDataResponse.AcquiringStatus
    def __init__(self, jobId: _Optional[str] = ..., acquiringStatus: _Optional[_Union[IsJobAcquiringDataResponse.AcquiringStatus, str]] = ...) -> None: ...

class QmDataRequest(_message.Message):
    __slots__ = ["io_value_Request"]
    IO_VALUE_REQUEST_FIELD_NUMBER: _ClassVar[int]
    io_value_Request: _containers.RepeatedCompositeFieldContainer[IOValueRequest]
    def __init__(self, io_value_Request: _Optional[_Iterable[_Union[IOValueRequest, _Mapping]]] = ...) -> None: ...

class QmDataResponse(_message.Message):
    __slots__ = ["io_value_response", "success", "errors"]
    class IOValueResponse(_message.Message):
        __slots__ = ["request", "values"]
        REQUEST_FIELD_NUMBER: _ClassVar[int]
        VALUES_FIELD_NUMBER: _ClassVar[int]
        request: IOValueRequest
        values: _compiler_pb2.QuaValues
        def __init__(self, request: _Optional[_Union[IOValueRequest, _Mapping]] = ..., values: _Optional[_Union[_compiler_pb2.QuaValues, _Mapping]] = ...) -> None: ...
    IO_VALUE_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    io_value_response: _containers.RepeatedCompositeFieldContainer[QmDataResponse.IOValueResponse]
    success: bool
    errors: _containers.RepeatedCompositeFieldContainer[_general_messages_pb2.ErrorMessage]
    def __init__(self, io_value_response: _Optional[_Iterable[_Union[QmDataResponse.IOValueResponse, _Mapping]]] = ..., success: bool = ..., errors: _Optional[_Iterable[_Union[_general_messages_pb2.ErrorMessage, _Mapping]]] = ...) -> None: ...

class IOValueRequest(_message.Message):
    __slots__ = ["pulser_number", "io_number", "jobId", "quantumMachineId"]
    PULSER_NUMBER_FIELD_NUMBER: _ClassVar[int]
    IO_NUMBER_FIELD_NUMBER: _ClassVar[int]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    QUANTUMMACHINEID_FIELD_NUMBER: _ClassVar[int]
    pulser_number: int
    io_number: int
    jobId: str
    quantumMachineId: str
    def __init__(self, pulser_number: _Optional[int] = ..., io_number: _Optional[int] = ..., jobId: _Optional[str] = ..., quantumMachineId: _Optional[str] = ...) -> None: ...

class ResumeRequest(_message.Message):
    __slots__ = ["jobId", "pulsersBitmap"]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    PULSERSBITMAP_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    pulsersBitmap: int
    def __init__(self, jobId: _Optional[str] = ..., pulsersBitmap: _Optional[int] = ...) -> None: ...

class ResumeResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class PausedStatusRequest(_message.Message):
    __slots__ = ["jobId"]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    def __init__(self, jobId: _Optional[str] = ...) -> None: ...

class PausedStatusResponse(_message.Message):
    __slots__ = ["pulsersBitmap", "ok", "isPaused"]
    PULSERSBITMAP_FIELD_NUMBER: _ClassVar[int]
    OK_FIELD_NUMBER: _ClassVar[int]
    ISPAUSED_FIELD_NUMBER: _ClassVar[int]
    pulsersBitmap: int
    ok: bool
    isPaused: bool
    def __init__(self, pulsersBitmap: _Optional[int] = ..., ok: bool = ..., isPaused: bool = ...) -> None: ...

class PullResultRequest(_message.Message):
    __slots__ = ["jobId"]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    def __init__(self, jobId: _Optional[str] = ...) -> None: ...

class PullAnalysedResultsRequest(_message.Message):
    __slots__ = ["jobId", "metadata"]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    metadata: str
    def __init__(self, jobId: _Optional[str] = ..., metadata: _Optional[str] = ...) -> None: ...

class PullResultResponse(_message.Message):
    __slots__ = ["data", "offset", "bytesLeft", "controllerName", "applicationNumber", "implementationName"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    BYTESLEFT_FIELD_NUMBER: _ClassVar[int]
    CONTROLLERNAME_FIELD_NUMBER: _ClassVar[int]
    APPLICATIONNUMBER_FIELD_NUMBER: _ClassVar[int]
    IMPLEMENTATIONNAME_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    offset: int
    bytesLeft: int
    controllerName: str
    applicationNumber: int
    implementationName: str
    def __init__(self, data: _Optional[bytes] = ..., offset: _Optional[int] = ..., bytesLeft: _Optional[int] = ..., controllerName: _Optional[str] = ..., applicationNumber: _Optional[int] = ..., implementationName: _Optional[str] = ...) -> None: ...

class HealthCheckResponse(_message.Message):
    __slots__ = ["message", "ok", "errorMessages", "warningMessages"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    OK_FIELD_NUMBER: _ClassVar[int]
    ERRORMESSAGES_FIELD_NUMBER: _ClassVar[int]
    WARNINGMESSAGES_FIELD_NUMBER: _ClassVar[int]
    message: _containers.RepeatedScalarFieldContainer[str]
    ok: bool
    errorMessages: _containers.RepeatedScalarFieldContainer[str]
    warningMessages: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, message: _Optional[_Iterable[str]] = ..., ok: bool = ..., errorMessages: _Optional[_Iterable[str]] = ..., warningMessages: _Optional[_Iterable[str]] = ...) -> None: ...

class ExecutionRequest(_message.Message):
    __slots__ = ["highLevelProgram", "lowLevelProgram", "streamDurationLimit", "streamDataLimit", "forceExecution", "simulate", "dryRun", "quantumMachineId"]
    class Simulate(_message.Message):
        __slots__ = ["duration", "simulateAnalogOutputs", "simulateDigitalOutputs", "includeAnalogSamples", "includeDigitalSamples", "includeAnalogWaveforms", "includeDigitalWaveforms", "simulationInterface", "extraProcessingTimeoutMs"]
        class SimulationInterface(_message.Message):
            __slots__ = ["none", "loopback", "raw"]
            # class None(_message.Message):
#                 __slots__ = []
#                 def __init__(self) -> None: ...
            class Loopback(_message.Message):
                __slots__ = ["connections", "latency", "noisePower"]
                class Connections(_message.Message):
                    __slots__ = ["fromController", "fromFem", "fromPort", "toController", "toFem", "toPort"]
                    FROMCONTROLLER_FIELD_NUMBER: _ClassVar[int]
                    FROMFEM_FIELD_NUMBER: _ClassVar[int]
                    FROMPORT_FIELD_NUMBER: _ClassVar[int]
                    TOCONTROLLER_FIELD_NUMBER: _ClassVar[int]
                    TOFEM_FIELD_NUMBER: _ClassVar[int]
                    TOPORT_FIELD_NUMBER: _ClassVar[int]
                    fromController: str
                    fromFem: int
                    fromPort: int
                    toController: str
                    toFem: int
                    toPort: int
                    def __init__(self, fromController: _Optional[str] = ..., fromFem: _Optional[int] = ..., fromPort: _Optional[int] = ..., toController: _Optional[str] = ..., toFem: _Optional[int] = ..., toPort: _Optional[int] = ...) -> None: ...
                CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
                LATENCY_FIELD_NUMBER: _ClassVar[int]
                NOISEPOWER_FIELD_NUMBER: _ClassVar[int]
                connections: _containers.RepeatedCompositeFieldContainer[ExecutionRequest.Simulate.SimulationInterface.Loopback.Connections]
                latency: int
                noisePower: float
                def __init__(self, connections: _Optional[_Iterable[_Union[ExecutionRequest.Simulate.SimulationInterface.Loopback.Connections, _Mapping]]] = ..., latency: _Optional[int] = ..., noisePower: _Optional[float] = ...) -> None: ...
            class RawInterface(_message.Message):
                __slots__ = ["connections", "noisePower"]
                class Connections(_message.Message):
                    __slots__ = ["fromController", "fromFem", "fromPort", "toSamples"]
                    FROMCONTROLLER_FIELD_NUMBER: _ClassVar[int]
                    FROMFEM_FIELD_NUMBER: _ClassVar[int]
                    FROMPORT_FIELD_NUMBER: _ClassVar[int]
                    TOSAMPLES_FIELD_NUMBER: _ClassVar[int]
                    fromController: str
                    fromFem: int
                    fromPort: int
                    toSamples: _containers.RepeatedScalarFieldContainer[float]
                    def __init__(self, fromController: _Optional[str] = ..., fromFem: _Optional[int] = ..., fromPort: _Optional[int] = ..., toSamples: _Optional[_Iterable[float]] = ...) -> None: ...
                CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
                NOISEPOWER_FIELD_NUMBER: _ClassVar[int]
                connections: _containers.RepeatedCompositeFieldContainer[ExecutionRequest.Simulate.SimulationInterface.RawInterface.Connections]
                noisePower: float
                def __init__(self, connections: _Optional[_Iterable[_Union[ExecutionRequest.Simulate.SimulationInterface.RawInterface.Connections, _Mapping]]] = ..., noisePower: _Optional[float] = ...) -> None: ...
            NONE_FIELD_NUMBER: _ClassVar[int]
            LOOPBACK_FIELD_NUMBER: _ClassVar[int]
            RAW_FIELD_NUMBER: _ClassVar[int]
            none: getattr(ExecutionRequest.Simulate.SimulationInterface, 'None')
            loopback: ExecutionRequest.Simulate.SimulationInterface.Loopback
            raw: ExecutionRequest.Simulate.SimulationInterface.RawInterface
            def __init__(self, none: _Optional[_Union[getattr(ExecutionRequest.Simulate.SimulationInterface, 'None'), _Mapping]] = ..., loopback: _Optional[_Union[ExecutionRequest.Simulate.SimulationInterface.Loopback, _Mapping]] = ..., raw: _Optional[_Union[ExecutionRequest.Simulate.SimulationInterface.RawInterface, _Mapping]] = ...) -> None: ...
        DURATION_FIELD_NUMBER: _ClassVar[int]
        SIMULATEANALOGOUTPUTS_FIELD_NUMBER: _ClassVar[int]
        SIMULATEDIGITALOUTPUTS_FIELD_NUMBER: _ClassVar[int]
        INCLUDEANALOGSAMPLES_FIELD_NUMBER: _ClassVar[int]
        INCLUDEDIGITALSAMPLES_FIELD_NUMBER: _ClassVar[int]
        INCLUDEANALOGWAVEFORMS_FIELD_NUMBER: _ClassVar[int]
        INCLUDEDIGITALWAVEFORMS_FIELD_NUMBER: _ClassVar[int]
        SIMULATIONINTERFACE_FIELD_NUMBER: _ClassVar[int]
        EXTRAPROCESSINGTIMEOUTMS_FIELD_NUMBER: _ClassVar[int]
        duration: int
        simulateAnalogOutputs: bool
        simulateDigitalOutputs: bool
        includeAnalogSamples: bool
        includeDigitalSamples: bool
        includeAnalogWaveforms: bool
        includeDigitalWaveforms: bool
        simulationInterface: ExecutionRequest.Simulate.SimulationInterface
        extraProcessingTimeoutMs: int
        def __init__(self, duration: _Optional[int] = ..., simulateAnalogOutputs: bool = ..., simulateDigitalOutputs: bool = ..., includeAnalogSamples: bool = ..., includeDigitalSamples: bool = ..., includeAnalogWaveforms: bool = ..., includeDigitalWaveforms: bool = ..., simulationInterface: _Optional[_Union[ExecutionRequest.Simulate.SimulationInterface, _Mapping]] = ..., extraProcessingTimeoutMs: _Optional[int] = ...) -> None: ...
    HIGHLEVELPROGRAM_FIELD_NUMBER: _ClassVar[int]
    LOWLEVELPROGRAM_FIELD_NUMBER: _ClassVar[int]
    STREAMDURATIONLIMIT_FIELD_NUMBER: _ClassVar[int]
    STREAMDATALIMIT_FIELD_NUMBER: _ClassVar[int]
    FORCEEXECUTION_FIELD_NUMBER: _ClassVar[int]
    SIMULATE_FIELD_NUMBER: _ClassVar[int]
    DRYRUN_FIELD_NUMBER: _ClassVar[int]
    QUANTUMMACHINEID_FIELD_NUMBER: _ClassVar[int]
    highLevelProgram: _inc_qua_pb2.QuaProgram
    lowLevelProgram: bytes
    streamDurationLimit: int
    streamDataLimit: int
    forceExecution: bool
    simulate: ExecutionRequest.Simulate
    dryRun: bool
    quantumMachineId: str
    def __init__(self, highLevelProgram: _Optional[_Union[_inc_qua_pb2.QuaProgram, _Mapping]] = ..., lowLevelProgram: _Optional[bytes] = ..., streamDurationLimit: _Optional[int] = ..., streamDataLimit: _Optional[int] = ..., forceExecution: bool = ..., simulate: _Optional[_Union[ExecutionRequest.Simulate, _Mapping]] = ..., dryRun: bool = ..., quantumMachineId: _Optional[str] = ...) -> None: ...

class ExecutionResponse(_message.Message):
    __slots__ = ["ok", "jobId", "messages", "metadata", "simulated", "config"]
    OK_FIELD_NUMBER: _ClassVar[int]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SIMULATED_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    jobId: str
    messages: _containers.RepeatedCompositeFieldContainer[_compiler_pb2.CompilerMessage]
    metadata: str
    simulated: SimulatedResponsePart
    config: _inc_qua_config_pb2.QuaConfig
    def __init__(self, ok: bool = ..., jobId: _Optional[str] = ..., messages: _Optional[_Iterable[_Union[_compiler_pb2.CompilerMessage, _Mapping]]] = ..., metadata: _Optional[str] = ..., simulated: _Optional[_Union[SimulatedResponsePart, _Mapping]] = ..., config: _Optional[_Union[_inc_qua_config_pb2.QuaConfig, _Mapping]] = ...) -> None: ...

class SimulatedResponsePart(_message.Message):
    __slots__ = ["analogOutputs", "digitalOutputs", "waveformReport", "errors"]
    ANALOGOUTPUTS_FIELD_NUMBER: _ClassVar[int]
    DIGITALOUTPUTS_FIELD_NUMBER: _ClassVar[int]
    WAVEFORMREPORT_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    analogOutputs: _struct_pb2.Struct
    digitalOutputs: _struct_pb2.Struct
    waveformReport: _struct_pb2.Struct
    errors: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, analogOutputs: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., digitalOutputs: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., waveformReport: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., errors: _Optional[_Iterable[str]] = ...) -> None: ...

class ResetDataProcessingRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ResetDataProcessingResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class HaltRequest(_message.Message):
    __slots__ = ["jobId"]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    def __init__(self, jobId: _Optional[str] = ...) -> None: ...

class HaltResponse(_message.Message):
    __slots__ = ["ok"]
    OK_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    def __init__(self, ok: bool = ...) -> None: ...

class PeekRequest(_message.Message):
    __slots__ = ["address", "controllerId"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    CONTROLLERID_FIELD_NUMBER: _ClassVar[int]
    address: int
    controllerId: str
    def __init__(self, address: _Optional[int] = ..., controllerId: _Optional[str] = ...) -> None: ...

class PeekResponse(_message.Message):
    __slots__ = ["value"]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: int
    def __init__(self, value: _Optional[int] = ...) -> None: ...

class PokeRequest(_message.Message):
    __slots__ = ["address", "value", "controllerId"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    CONTROLLERID_FIELD_NUMBER: _ClassVar[int]
    address: int
    value: int
    controllerId: str
    def __init__(self, address: _Optional[int] = ..., value: _Optional[int] = ..., controllerId: _Optional[str] = ...) -> None: ...

class PokeResponse(_message.Message):
    __slots__ = ["ok"]
    OK_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    def __init__(self, ok: bool = ...) -> None: ...

class GetSimulatedQuantumStateRequest(_message.Message):
    __slots__ = ["jobId"]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    def __init__(self, jobId: _Optional[str] = ...) -> None: ...

class GetSimulatedQuantumStateResponse(_message.Message):
    __slots__ = ["jobId", "ok", "state"]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    OK_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    ok: bool
    state: DensityMatrix
    def __init__(self, jobId: _Optional[str] = ..., ok: bool = ..., state: _Optional[_Union[DensityMatrix, _Mapping]] = ...) -> None: ...

class DensityMatrix(_message.Message):
    __slots__ = ["timeStamp", "data"]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    timeStamp: int
    data: _containers.RepeatedCompositeFieldContainer[ComplexNumber]
    def __init__(self, timeStamp: _Optional[int] = ..., data: _Optional[_Iterable[_Union[ComplexNumber, _Mapping]]] = ...) -> None: ...

class ComplexNumber(_message.Message):
    __slots__ = ["re", "im"]
    RE_FIELD_NUMBER: _ClassVar[int]
    IM_FIELD_NUMBER: _ClassVar[int]
    re: float
    im: float
    def __init__(self, re: _Optional[float] = ..., im: _Optional[float] = ...) -> None: ...

class PerformHalDebugCommandRequest(_message.Message):
    __slots__ = ["controllerName", "command"]
    CONTROLLERNAME_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    controllerName: str
    command: str
    def __init__(self, controllerName: _Optional[str] = ..., command: _Optional[str] = ...) -> None: ...

class PerformHalDebugCommandResponse(_message.Message):
    __slots__ = ["success", "response"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    response: str
    def __init__(self, success: bool = ..., response: _Optional[str] = ...) -> None: ...
