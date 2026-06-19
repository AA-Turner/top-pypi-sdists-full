from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from qm.grpc.qm.grpc.v2 import qm_api_pb2 as _qm_api_pb2
from qm.grpc.qm.grpc.v2 import common_types_pb2 as _common_types_pb2
from qm.grpc.qm.pb import inc_qm_api_pb2 as _inc_qm_api_pb2
from qm.grpc.qm.pb import job_manager_pb2 as _job_manager_pb2
from qm.grpc.qm.pb import job_results_pb2 as _job_results_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetMatrixCorrectionResponse(_message.Message):
    __slots__ = ["success", "error"]
    class SetMatrixCorrectionResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    class SetMatrixCorrectionResponseSuccess(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: SetMatrixCorrectionResponse.SetMatrixCorrectionResponseSuccess
    error: SetMatrixCorrectionResponse.SetMatrixCorrectionResponseError
    def __init__(self, success: _Optional[_Union[SetMatrixCorrectionResponse.SetMatrixCorrectionResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[SetMatrixCorrectionResponse.SetMatrixCorrectionResponseError, _Mapping]] = ...) -> None: ...

class SetIntermediateFrequencyResponse(_message.Message):
    __slots__ = ["success", "error"]
    class SetIntermediateFrequencyResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    class SetIntermediateFrequencyResponseSuccess(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: SetIntermediateFrequencyResponse.SetIntermediateFrequencyResponseSuccess
    error: SetIntermediateFrequencyResponse.SetIntermediateFrequencyResponseError
    def __init__(self, success: _Optional[_Union[SetIntermediateFrequencyResponse.SetIntermediateFrequencyResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[SetIntermediateFrequencyResponse.SetIntermediateFrequencyResponseError, _Mapping]] = ...) -> None: ...

class SetDigitalDelayResponse(_message.Message):
    __slots__ = ["success", "error"]
    class SetDigitalDelayResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    class SetDigitalDelayResponseSuccess(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: SetDigitalDelayResponse.SetDigitalDelayResponseSuccess
    error: SetDigitalDelayResponse.SetDigitalDelayResponseError
    def __init__(self, success: _Optional[_Union[SetDigitalDelayResponse.SetDigitalDelayResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[SetDigitalDelayResponse.SetDigitalDelayResponseError, _Mapping]] = ...) -> None: ...

class SetDigitalBufferResponse(_message.Message):
    __slots__ = ["success", "error"]
    class SetDigitalBufferResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    class SetDigitalBufferResponseSuccess(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: SetDigitalBufferResponse.SetDigitalBufferResponseSuccess
    error: SetDigitalBufferResponse.SetDigitalBufferResponseError
    def __init__(self, success: _Optional[_Union[SetDigitalBufferResponse.SetDigitalBufferResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[SetDigitalBufferResponse.SetDigitalBufferResponseError, _Mapping]] = ...) -> None: ...

class SetInputDcOffsetResponse(_message.Message):
    __slots__ = ["success", "error"]
    class SetInputDcOffsetResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    class SetInputDcOffsetResponseSuccess(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: SetInputDcOffsetResponse.SetInputDcOffsetResponseSuccess
    error: SetInputDcOffsetResponse.SetInputDcOffsetResponseError
    def __init__(self, success: _Optional[_Union[SetInputDcOffsetResponse.SetInputDcOffsetResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[SetInputDcOffsetResponse.SetInputDcOffsetResponseError, _Mapping]] = ...) -> None: ...

class SetOutputDcOffsetResponse(_message.Message):
    __slots__ = ["success", "error"]
    class SetOutputDcOffsetResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    class SetOutputDcOffsetResponseSuccess(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: SetOutputDcOffsetResponse.SetOutputDcOffsetResponseSuccess
    error: SetOutputDcOffsetResponse.SetOutputDcOffsetResponseError
    def __init__(self, success: _Optional[_Union[SetOutputDcOffsetResponse.SetOutputDcOffsetResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[SetOutputDcOffsetResponse.SetOutputDcOffsetResponseError, _Mapping]] = ...) -> None: ...

class SetIoValuesResponse(_message.Message):
    __slots__ = ["success", "error"]
    class SetIoValuesResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    class SetIoValuesResponseSuccess(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: SetIoValuesResponse.SetIoValuesResponseSuccess
    error: SetIoValuesResponse.SetIoValuesResponseError
    def __init__(self, success: _Optional[_Union[SetIoValuesResponse.SetIoValuesResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[SetIoValuesResponse.SetIoValuesResponseError, _Mapping]] = ...) -> None: ...

class SetIoValuesRequest(_message.Message):
    __slots__ = ["job_id", "io1", "io2"]
    class IOValueSetData(_message.Message):
        __slots__ = ["int_value", "double_value", "boolean_value"]
        INT_VALUE_FIELD_NUMBER: _ClassVar[int]
        DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
        BOOLEAN_VALUE_FIELD_NUMBER: _ClassVar[int]
        int_value: int
        double_value: float
        boolean_value: bool
        def __init__(self, int_value: _Optional[int] = ..., double_value: _Optional[float] = ..., boolean_value: bool = ...) -> None: ...
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    IO1_FIELD_NUMBER: _ClassVar[int]
    IO2_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    io1: SetIoValuesRequest.IOValueSetData
    io2: SetIoValuesRequest.IOValueSetData
    def __init__(self, job_id: _Optional[str] = ..., io1: _Optional[_Union[SetIoValuesRequest.IOValueSetData, _Mapping]] = ..., io2: _Optional[_Union[SetIoValuesRequest.IOValueSetData, _Mapping]] = ...) -> None: ...

class GetIoValuesRequest(_message.Message):
    __slots__ = ["job_id"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class IOValuesData(_message.Message):
    __slots__ = ["int_value", "double_value", "boolean_value"]
    INT_VALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
    BOOLEAN_VALUE_FIELD_NUMBER: _ClassVar[int]
    int_value: int
    double_value: float
    boolean_value: bool
    def __init__(self, int_value: _Optional[int] = ..., double_value: _Optional[float] = ..., boolean_value: bool = ...) -> None: ...

class GetIoValuesResponse(_message.Message):
    __slots__ = ["success", "error"]
    class GetIoValuesResponseSuccess(_message.Message):
        __slots__ = ["io1", "io2"]
        class IOValuesData(_message.Message):
            __slots__ = ["int_value", "double_value", "boolean_value"]
            INT_VALUE_FIELD_NUMBER: _ClassVar[int]
            DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
            BOOLEAN_VALUE_FIELD_NUMBER: _ClassVar[int]
            int_value: int
            double_value: float
            boolean_value: bool
            def __init__(self, int_value: _Optional[int] = ..., double_value: _Optional[float] = ..., boolean_value: bool = ...) -> None: ...
        IO1_FIELD_NUMBER: _ClassVar[int]
        IO2_FIELD_NUMBER: _ClassVar[int]
        io1: GetIoValuesResponse.GetIoValuesResponseSuccess.IOValuesData
        io2: GetIoValuesResponse.GetIoValuesResponseSuccess.IOValuesData
        def __init__(self, io1: _Optional[_Union[GetIoValuesResponse.GetIoValuesResponseSuccess.IOValuesData, _Mapping]] = ..., io2: _Optional[_Union[GetIoValuesResponse.GetIoValuesResponseSuccess.IOValuesData, _Mapping]] = ...) -> None: ...
    class GetIoValuesResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: GetIoValuesResponse.GetIoValuesResponseSuccess
    error: GetIoValuesResponse.GetIoValuesResponseError
    def __init__(self, success: _Optional[_Union[GetIoValuesResponse.GetIoValuesResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[GetIoValuesResponse.GetIoValuesResponseError, _Mapping]] = ...) -> None: ...

class JobServiceIsPausedRequest(_message.Message):
    __slots__ = ["job_id"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class IsPausedResponse(_message.Message):
    __slots__ = ["error", "success"]
    class IsPausedResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    class IsPausedResponseSuccess(_message.Message):
        __slots__ = ["is_paused"]
        IS_PAUSED_FIELD_NUMBER: _ClassVar[int]
        is_paused: bool
        def __init__(self, is_paused: bool = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    error: IsPausedResponse.IsPausedResponseError
    success: IsPausedResponse.IsPausedResponseSuccess
    def __init__(self, error: _Optional[_Union[IsPausedResponse.IsPausedResponseError, _Mapping]] = ..., success: _Optional[_Union[IsPausedResponse.IsPausedResponseSuccess, _Mapping]] = ...) -> None: ...

class JobServiceGetConfigRequest(_message.Message):
    __slots__ = ["job_id"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class JobServiceGetJobStatusRequest(_message.Message):
    __slots__ = ["job_id"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class ResumeRequest(_message.Message):
    __slots__ = ["job_id"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class ResumeResponse(_message.Message):
    __slots__ = ["success", "error"]
    class ResumeResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    class ResumeResponseSuccess(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: ResumeResponse.ResumeResponseSuccess
    error: ResumeResponse.ResumeResponseError
    def __init__(self, success: _Optional[_Union[ResumeResponse.ResumeResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[ResumeResponse.ResumeResponseError, _Mapping]] = ...) -> None: ...

class SetMatrixCorrectionRequest(_message.Message):
    __slots__ = ["job_id", "qe", "correction"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    QE_FIELD_NUMBER: _ClassVar[int]
    CORRECTION_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    qe: str
    correction: _inc_qm_api_pb2.Matrix
    def __init__(self, job_id: _Optional[str] = ..., qe: _Optional[str] = ..., correction: _Optional[_Union[_inc_qm_api_pb2.Matrix, _Mapping]] = ...) -> None: ...

class SetIntermediateFrequencyRequest(_message.Message):
    __slots__ = ["job_id", "qe", "frequency"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    QE_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    qe: str
    frequency: float
    def __init__(self, job_id: _Optional[str] = ..., qe: _Optional[str] = ..., frequency: _Optional[float] = ...) -> None: ...

class SetDigitalDelayRequest(_message.Message):
    __slots__ = ["job_id", "qe", "port", "delay"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    QE_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    DELAY_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    qe: str
    port: str
    delay: int
    def __init__(self, job_id: _Optional[str] = ..., qe: _Optional[str] = ..., port: _Optional[str] = ..., delay: _Optional[int] = ...) -> None: ...

class SetDigitalBufferRequest(_message.Message):
    __slots__ = ["job_id", "qe", "port", "buffer"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    QE_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    BUFFER_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    qe: str
    port: str
    buffer: int
    def __init__(self, job_id: _Optional[str] = ..., qe: _Optional[str] = ..., port: _Optional[str] = ..., buffer: _Optional[int] = ...) -> None: ...

class SetInputDcOffsetRequest(_message.Message):
    __slots__ = ["job_id", "qe", "port", "offset"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    QE_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    qe: str
    port: str
    offset: float
    def __init__(self, job_id: _Optional[str] = ..., qe: _Optional[str] = ..., port: _Optional[str] = ..., offset: _Optional[float] = ...) -> None: ...

class SetOutputDcOffsetRequest(_message.Message):
    __slots__ = ["job_id", "qe", "mix_inputs", "single_input"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    QE_FIELD_NUMBER: _ClassVar[int]
    MIX_INPUTS_FIELD_NUMBER: _ClassVar[int]
    SINGLE_INPUT_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    qe: str
    mix_inputs: MixInputsDcOffset
    single_input: SingleInputDcOffset
    def __init__(self, job_id: _Optional[str] = ..., qe: _Optional[str] = ..., mix_inputs: _Optional[_Union[MixInputsDcOffset, _Mapping]] = ..., single_input: _Optional[_Union[SingleInputDcOffset, _Mapping]] = ...) -> None: ...

class GetMatrixCorrectionRequest(_message.Message):
    __slots__ = ["job_id", "qe"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    QE_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    qe: str
    def __init__(self, job_id: _Optional[str] = ..., qe: _Optional[str] = ...) -> None: ...

class GetMatrixCorrectionError(_message.Message):
    __slots__ = ["details"]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    details: str
    def __init__(self, details: _Optional[str] = ...) -> None: ...

class GetMatrixCorrectionResponse(_message.Message):
    __slots__ = ["error", "success"]
    class GetMatrixCorrectionResponseSuccess(_message.Message):
        __slots__ = ["correction"]
        CORRECTION_FIELD_NUMBER: _ClassVar[int]
        correction: _inc_qm_api_pb2.Matrix
        def __init__(self, correction: _Optional[_Union[_inc_qm_api_pb2.Matrix, _Mapping]] = ...) -> None: ...
    class GetMatrixCorrectionResponseError(_message.Message):
        __slots__ = ["error"]
        ERROR_FIELD_NUMBER: _ClassVar[int]
        error: GetMatrixCorrectionError
        def __init__(self, error: _Optional[_Union[GetMatrixCorrectionError, _Mapping]] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    error: GetMatrixCorrectionResponse.GetMatrixCorrectionResponseError
    success: GetMatrixCorrectionResponse.GetMatrixCorrectionResponseSuccess
    def __init__(self, error: _Optional[_Union[GetMatrixCorrectionResponse.GetMatrixCorrectionResponseError, _Mapping]] = ..., success: _Optional[_Union[GetMatrixCorrectionResponse.GetMatrixCorrectionResponseSuccess, _Mapping]] = ...) -> None: ...

class GetIntermediateFrequencyRequest(_message.Message):
    __slots__ = ["job_id", "qe"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    QE_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    qe: str
    def __init__(self, job_id: _Optional[str] = ..., qe: _Optional[str] = ...) -> None: ...

class GetIntermediateFrequencyResponse(_message.Message):
    __slots__ = ["error", "success"]
    class GetIntermediateFrequencyResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    class GetIntermediateFrequencyResponseSuccess(_message.Message):
        __slots__ = ["frequency"]
        FREQUENCY_FIELD_NUMBER: _ClassVar[int]
        frequency: float
        def __init__(self, frequency: _Optional[float] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    error: GetIntermediateFrequencyResponse.GetIntermediateFrequencyResponseError
    success: GetIntermediateFrequencyResponse.GetIntermediateFrequencyResponseSuccess
    def __init__(self, error: _Optional[_Union[GetIntermediateFrequencyResponse.GetIntermediateFrequencyResponseError, _Mapping]] = ..., success: _Optional[_Union[GetIntermediateFrequencyResponse.GetIntermediateFrequencyResponseSuccess, _Mapping]] = ...) -> None: ...

class GetDigitalDelayRequest(_message.Message):
    __slots__ = ["job_id", "qe", "port"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    QE_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    qe: str
    port: str
    def __init__(self, job_id: _Optional[str] = ..., qe: _Optional[str] = ..., port: _Optional[str] = ...) -> None: ...

class GetDigitalDelayResponse(_message.Message):
    __slots__ = ["success", "error"]
    class GetDigitalDelayResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    class GetDigitalDelayResponseSuccess(_message.Message):
        __slots__ = ["delay"]
        DELAY_FIELD_NUMBER: _ClassVar[int]
        delay: int
        def __init__(self, delay: _Optional[int] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: GetDigitalDelayResponse.GetDigitalDelayResponseSuccess
    error: GetDigitalDelayResponse.GetDigitalDelayResponseError
    def __init__(self, success: _Optional[_Union[GetDigitalDelayResponse.GetDigitalDelayResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[GetDigitalDelayResponse.GetDigitalDelayResponseError, _Mapping]] = ...) -> None: ...

class GetDigitalBufferRequest(_message.Message):
    __slots__ = ["job_id", "qe", "port"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    QE_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    qe: str
    port: str
    def __init__(self, job_id: _Optional[str] = ..., qe: _Optional[str] = ..., port: _Optional[str] = ...) -> None: ...

class GetDigitalBufferResponse(_message.Message):
    __slots__ = ["success", "error"]
    class GetDigitalBufferResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    class GetDigitalBufferResponseSuccess(_message.Message):
        __slots__ = ["buffer"]
        BUFFER_FIELD_NUMBER: _ClassVar[int]
        buffer: int
        def __init__(self, buffer: _Optional[int] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: GetDigitalBufferResponse.GetDigitalBufferResponseSuccess
    error: GetDigitalBufferResponse.GetDigitalBufferResponseError
    def __init__(self, success: _Optional[_Union[GetDigitalBufferResponse.GetDigitalBufferResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[GetDigitalBufferResponse.GetDigitalBufferResponseError, _Mapping]] = ...) -> None: ...

class GetInputDcOffsetRequest(_message.Message):
    __slots__ = ["job_id", "qe", "port"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    QE_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    qe: str
    port: str
    def __init__(self, job_id: _Optional[str] = ..., qe: _Optional[str] = ..., port: _Optional[str] = ...) -> None: ...

class GetInputDcOffsetError(_message.Message):
    __slots__ = ["details"]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    details: str
    def __init__(self, details: _Optional[str] = ...) -> None: ...

class GetInputDcOffsetSuccess(_message.Message):
    __slots__ = ["offset"]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    offset: float
    def __init__(self, offset: _Optional[float] = ...) -> None: ...

class GetInputDcOffsetResponse(_message.Message):
    __slots__ = ["success", "error"]
    class GetInputDcOffsetResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    class GetInputDcOffsetResponseSuccess(_message.Message):
        __slots__ = ["offset"]
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        offset: float
        def __init__(self, offset: _Optional[float] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: GetInputDcOffsetResponse.GetInputDcOffsetResponseSuccess
    error: GetInputDcOffsetResponse.GetInputDcOffsetResponseError
    def __init__(self, success: _Optional[_Union[GetInputDcOffsetResponse.GetInputDcOffsetResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[GetInputDcOffsetResponse.GetInputDcOffsetResponseError, _Mapping]] = ...) -> None: ...

class GetOutputDcOffsetRequest(_message.Message):
    __slots__ = ["job_id", "qe"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    QE_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    qe: str
    def __init__(self, job_id: _Optional[str] = ..., qe: _Optional[str] = ...) -> None: ...

class GetOutputDcOffsetResponse(_message.Message):
    __slots__ = ["success", "error"]
    class GetOutputDcOffsetResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    class GetOutputDcOffsetResponseSuccess(_message.Message):
        __slots__ = ["mix_inputs", "single_input"]
        MIX_INPUTS_FIELD_NUMBER: _ClassVar[int]
        SINGLE_INPUT_FIELD_NUMBER: _ClassVar[int]
        mix_inputs: MixInputsDcOffset
        single_input: SingleInputDcOffset
        def __init__(self, mix_inputs: _Optional[_Union[MixInputsDcOffset, _Mapping]] = ..., single_input: _Optional[_Union[SingleInputDcOffset, _Mapping]] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: GetOutputDcOffsetResponse.GetOutputDcOffsetResponseSuccess
    error: GetOutputDcOffsetResponse.GetOutputDcOffsetResponseError
    def __init__(self, success: _Optional[_Union[GetOutputDcOffsetResponse.GetOutputDcOffsetResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[GetOutputDcOffsetResponse.GetOutputDcOffsetResponseError, _Mapping]] = ...) -> None: ...

class MixInputsDcOffset(_message.Message):
    __slots__ = ["I", "Q"]
    I_FIELD_NUMBER: _ClassVar[int]
    Q_FIELD_NUMBER: _ClassVar[int]
    I: float
    Q: float
    def __init__(self, I: _Optional[float] = ..., Q: _Optional[float] = ...) -> None: ...

class SingleInputDcOffset(_message.Message):
    __slots__ = ["offset"]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    offset: float
    def __init__(self, offset: _Optional[float] = ...) -> None: ...

class JobServiceGetConfigResponse(_message.Message):
    __slots__ = ["success", "error"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: _qm_api_pb2.GetConfigSuccess
    error: _qm_api_pb2.GetConfigError
    def __init__(self, success: _Optional[_Union[_qm_api_pb2.GetConfigSuccess, _Mapping]] = ..., error: _Optional[_Union[_qm_api_pb2.GetConfigError, _Mapping]] = ...) -> None: ...

class JobServiceGetJobStatusResponse(_message.Message):
    __slots__ = ["success", "error"]
    class JobServiceGetJobStatusResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    class JobServiceGetJobStatusResponseSuccess(_message.Message):
        __slots__ = ["status"]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        status: _common_types_pb2.JobExecutionStatus
        def __init__(self, status: _Optional[_Union[_common_types_pb2.JobExecutionStatus, str]] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: JobServiceGetJobStatusResponse.JobServiceGetJobStatusResponseSuccess
    error: JobServiceGetJobStatusResponse.JobServiceGetJobStatusResponseError
    def __init__(self, success: _Optional[_Union[JobServiceGetJobStatusResponse.JobServiceGetJobStatusResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[JobServiceGetJobStatusResponse.JobServiceGetJobStatusResponseError, _Mapping]] = ...) -> None: ...

class JobServicePushToInputStreamRequest(_message.Message):
    __slots__ = ["job_id", "stream_name", "int_stream_data", "fixed_stream_data", "bool_stream_data"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    STREAM_NAME_FIELD_NUMBER: _ClassVar[int]
    INT_STREAM_DATA_FIELD_NUMBER: _ClassVar[int]
    FIXED_STREAM_DATA_FIELD_NUMBER: _ClassVar[int]
    BOOL_STREAM_DATA_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    stream_name: str
    int_stream_data: _job_manager_pb2.IntStreamData
    fixed_stream_data: _job_manager_pb2.FixedStreamData
    bool_stream_data: _job_manager_pb2.BoolStreamData
    def __init__(self, job_id: _Optional[str] = ..., stream_name: _Optional[str] = ..., int_stream_data: _Optional[_Union[_job_manager_pb2.IntStreamData, _Mapping]] = ..., fixed_stream_data: _Optional[_Union[_job_manager_pb2.FixedStreamData, _Mapping]] = ..., bool_stream_data: _Optional[_Union[_job_manager_pb2.BoolStreamData, _Mapping]] = ...) -> None: ...

class PushToInputStreamResponse(_message.Message):
    __slots__ = ["success", "error"]
    class PushToInputStreamResponseSuccess(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    class PushToInputStreamResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: PushToInputStreamResponse.PushToInputStreamResponseSuccess
    error: PushToInputStreamResponse.PushToInputStreamResponseError
    def __init__(self, success: _Optional[_Union[PushToInputStreamResponse.PushToInputStreamResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[PushToInputStreamResponse.PushToInputStreamResponseError, _Mapping]] = ...) -> None: ...

class GetJobResultSchemaRequest(_message.Message):
    __slots__ = ["job_id"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class GetJobResultSchemaResponse(_message.Message):
    __slots__ = ["success", "error"]
    class GetJobResultSchemaResponseSuccess(_message.Message):
        __slots__ = ["items"]
        class Item(_message.Message):
            __slots__ = ["name", "simple_dtype", "is_single", "expected_count", "shape"]
            NAME_FIELD_NUMBER: _ClassVar[int]
            SIMPLE_DTYPE_FIELD_NUMBER: _ClassVar[int]
            IS_SINGLE_FIELD_NUMBER: _ClassVar[int]
            EXPECTED_COUNT_FIELD_NUMBER: _ClassVar[int]
            SHAPE_FIELD_NUMBER: _ClassVar[int]
            name: str
            simple_dtype: str
            is_single: bool
            expected_count: int
            shape: _containers.RepeatedScalarFieldContainer[int]
            def __init__(self, name: _Optional[str] = ..., simple_dtype: _Optional[str] = ..., is_single: bool = ..., expected_count: _Optional[int] = ..., shape: _Optional[_Iterable[int]] = ...) -> None: ...
        ITEMS_FIELD_NUMBER: _ClassVar[int]
        items: _containers.RepeatedCompositeFieldContainer[GetJobResultSchemaResponse.GetJobResultSchemaResponseSuccess.Item]
        def __init__(self, items: _Optional[_Iterable[_Union[GetJobResultSchemaResponse.GetJobResultSchemaResponseSuccess.Item, _Mapping]]] = ...) -> None: ...
    class GetJobResultSchemaResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: GetJobResultSchemaResponse.GetJobResultSchemaResponseSuccess
    error: GetJobResultSchemaResponse.GetJobResultSchemaResponseError
    def __init__(self, success: _Optional[_Union[GetJobResultSchemaResponse.GetJobResultSchemaResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[GetJobResultSchemaResponse.GetJobResultSchemaResponseError, _Mapping]] = ...) -> None: ...

class GetJobNamedResultHeaderRequest(_message.Message):
    __slots__ = ["job_id", "output_name", "flat_format"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_NAME_FIELD_NUMBER: _ClassVar[int]
    FLAT_FORMAT_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    output_name: str
    flat_format: bool
    def __init__(self, job_id: _Optional[str] = ..., output_name: _Optional[str] = ..., flat_format: bool = ...) -> None: ...

class GetJobNamedResultsHeadersRequest(_message.Message):
    __slots__ = ["job_id", "outputs"]
    class Output(_message.Message):
        __slots__ = ["output_name", "flat_format"]
        OUTPUT_NAME_FIELD_NUMBER: _ClassVar[int]
        FLAT_FORMAT_FIELD_NUMBER: _ClassVar[int]
        output_name: str
        flat_format: bool
        def __init__(self, output_name: _Optional[str] = ..., flat_format: bool = ...) -> None: ...
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    outputs: _containers.RepeatedCompositeFieldContainer[GetJobNamedResultsHeadersRequest.Output]
    def __init__(self, job_id: _Optional[str] = ..., outputs: _Optional[_Iterable[_Union[GetJobNamedResultsHeadersRequest.Output, _Mapping]]] = ...) -> None: ...

class GetJobNamedResultsHeadersResponse(_message.Message):
    __slots__ = ["success", "error"]
    class GetJobNamedResultsHeadersResponseSuccess(_message.Message):
        __slots__ = ["headers"]
        class OutputHeader(_message.Message):
            __slots__ = ["count_so_far", "has_data_loss", "output_name", "simple_dtype", "shape"]
            COUNT_SO_FAR_FIELD_NUMBER: _ClassVar[int]
            HAS_DATA_LOSS_FIELD_NUMBER: _ClassVar[int]
            OUTPUT_NAME_FIELD_NUMBER: _ClassVar[int]
            SIMPLE_DTYPE_FIELD_NUMBER: _ClassVar[int]
            SHAPE_FIELD_NUMBER: _ClassVar[int]
            count_so_far: int
            has_data_loss: bool
            output_name: str
            simple_dtype: str
            shape: _containers.RepeatedScalarFieldContainer[int]
            def __init__(self, count_so_far: _Optional[int] = ..., has_data_loss: bool = ..., output_name: _Optional[str] = ..., simple_dtype: _Optional[str] = ..., shape: _Optional[_Iterable[int]] = ...) -> None: ...
        HEADERS_FIELD_NUMBER: _ClassVar[int]
        headers: _containers.RepeatedCompositeFieldContainer[GetJobNamedResultsHeadersResponse.GetJobNamedResultsHeadersResponseSuccess.OutputHeader]
        def __init__(self, headers: _Optional[_Iterable[_Union[GetJobNamedResultsHeadersResponse.GetJobNamedResultsHeadersResponseSuccess.OutputHeader, _Mapping]]] = ...) -> None: ...
    class GetJobNamedResultsHeadersResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: GetJobNamedResultsHeadersResponse.GetJobNamedResultsHeadersResponseSuccess
    error: GetJobNamedResultsHeadersResponse.GetJobNamedResultsHeadersResponseError
    def __init__(self, success: _Optional[_Union[GetJobNamedResultsHeadersResponse.GetJobNamedResultsHeadersResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[GetJobNamedResultsHeadersResponse.GetJobNamedResultsHeadersResponseError, _Mapping]] = ...) -> None: ...

class GetJobNamedResultHeaderResponse(_message.Message):
    __slots__ = ["success", "error"]
    class GetJobNamedResultHeaderResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    class GetJobNamedResultHeaderResponseSuccess(_message.Message):
        __slots__ = ["is_single", "count_so_far", "simple_dtype", "has_data_loss", "shape", "output_name"]
        IS_SINGLE_FIELD_NUMBER: _ClassVar[int]
        COUNT_SO_FAR_FIELD_NUMBER: _ClassVar[int]
        SIMPLE_DTYPE_FIELD_NUMBER: _ClassVar[int]
        HAS_DATA_LOSS_FIELD_NUMBER: _ClassVar[int]
        SHAPE_FIELD_NUMBER: _ClassVar[int]
        OUTPUT_NAME_FIELD_NUMBER: _ClassVar[int]
        is_single: bool
        count_so_far: int
        simple_dtype: str
        has_data_loss: bool
        shape: _containers.RepeatedScalarFieldContainer[int]
        output_name: str
        def __init__(self, is_single: bool = ..., count_so_far: _Optional[int] = ..., simple_dtype: _Optional[str] = ..., has_data_loss: bool = ..., shape: _Optional[_Iterable[int]] = ..., output_name: _Optional[str] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: GetJobNamedResultHeaderResponse.GetJobNamedResultHeaderResponseSuccess
    error: GetJobNamedResultHeaderResponse.GetJobNamedResultHeaderResponseError
    def __init__(self, success: _Optional[_Union[GetJobNamedResultHeaderResponse.GetJobNamedResultHeaderResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[GetJobNamedResultHeaderResponse.GetJobNamedResultHeaderResponseError, _Mapping]] = ...) -> None: ...

class GetNamedResultsRequest(_message.Message):
    __slots__ = ["job_id", "outputs"]
    class Output(_message.Message):
        __slots__ = ["output_name", "range"]
        OUTPUT_NAME_FIELD_NUMBER: _ClassVar[int]
        RANGE_FIELD_NUMBER: _ClassVar[int]
        output_name: str
        range: _common_types_pb2.Range
        def __init__(self, output_name: _Optional[str] = ..., range: _Optional[_Union[_common_types_pb2.Range, _Mapping]] = ...) -> None: ...
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    outputs: _containers.RepeatedCompositeFieldContainer[GetNamedResultsRequest.Output]
    def __init__(self, job_id: _Optional[str] = ..., outputs: _Optional[_Iterable[_Union[GetNamedResultsRequest.Output, _Mapping]]] = ...) -> None: ...

class GetNamedResultRequest(_message.Message):
    __slots__ = ["job_id", "output_name", "limit", "long_offset"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_NAME_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    LONG_OFFSET_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    output_name: str
    limit: int
    long_offset: _wrappers_pb2.Int64Value
    def __init__(self, job_id: _Optional[str] = ..., output_name: _Optional[str] = ..., limit: _Optional[int] = ..., long_offset: _Optional[_Union[_wrappers_pb2.Int64Value, _Mapping]] = ...) -> None: ...

class GetNamedResultResponse(_message.Message):
    __slots__ = ["success", "error"]
    class GetNamedResultResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    class GetNamedResultResponseSuccess(_message.Message):
        __slots__ = ["count_of_items", "data", "data_chunk", "data_summary", "output_name"]
        class DataChunk(_message.Message):
            __slots__ = ["data"]
            DATA_FIELD_NUMBER: _ClassVar[int]
            data: bytes
            def __init__(self, data: _Optional[bytes] = ...) -> None: ...
        class DataSummary(_message.Message):
            __slots__ = ["count"]
            COUNT_FIELD_NUMBER: _ClassVar[int]
            count: int
            def __init__(self, count: _Optional[int] = ...) -> None: ...
        COUNT_OF_ITEMS_FIELD_NUMBER: _ClassVar[int]
        DATA_FIELD_NUMBER: _ClassVar[int]
        DATA_CHUNK_FIELD_NUMBER: _ClassVar[int]
        DATA_SUMMARY_FIELD_NUMBER: _ClassVar[int]
        OUTPUT_NAME_FIELD_NUMBER: _ClassVar[int]
        count_of_items: int
        data: bytes
        data_chunk: GetNamedResultResponse.GetNamedResultResponseSuccess.DataChunk
        data_summary: GetNamedResultResponse.GetNamedResultResponseSuccess.DataSummary
        output_name: str
        def __init__(self, count_of_items: _Optional[int] = ..., data: _Optional[bytes] = ..., data_chunk: _Optional[_Union[GetNamedResultResponse.GetNamedResultResponseSuccess.DataChunk, _Mapping]] = ..., data_summary: _Optional[_Union[GetNamedResultResponse.GetNamedResultResponseSuccess.DataSummary, _Mapping]] = ..., output_name: _Optional[str] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: GetNamedResultResponse.GetNamedResultResponseSuccess
    error: GetNamedResultResponse.GetNamedResultResponseError
    def __init__(self, success: _Optional[_Union[GetNamedResultResponse.GetNamedResultResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[GetNamedResultResponse.GetNamedResultResponseError, _Mapping]] = ...) -> None: ...

class GetJobErrorsRequest(_message.Message):
    __slots__ = ["job_id"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class GetJobErrorsResponse(_message.Message):
    __slots__ = ["success", "error"]
    class GetJobErrorsResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    class GetJobErrorsResponseSuccess(_message.Message):
        __slots__ = ["errors"]
        class ExecutionErrorSeverity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
            ERROR: _ClassVar[GetJobErrorsResponse.GetJobErrorsResponseSuccess.ExecutionErrorSeverity]
            WARNING: _ClassVar[GetJobErrorsResponse.GetJobErrorsResponseSuccess.ExecutionErrorSeverity]
        ERROR: GetJobErrorsResponse.GetJobErrorsResponseSuccess.ExecutionErrorSeverity
        WARNING: GetJobErrorsResponse.GetJobErrorsResponseSuccess.ExecutionErrorSeverity
        class Error(_message.Message):
            __slots__ = ["errorCode", "errorSeverity", "message"]
            ERRORCODE_FIELD_NUMBER: _ClassVar[int]
            ERRORSEVERITY_FIELD_NUMBER: _ClassVar[int]
            MESSAGE_FIELD_NUMBER: _ClassVar[int]
            errorCode: int
            errorSeverity: GetJobErrorsResponse.GetJobErrorsResponseSuccess.ExecutionErrorSeverity
            message: str
            def __init__(self, errorCode: _Optional[int] = ..., errorSeverity: _Optional[_Union[GetJobErrorsResponse.GetJobErrorsResponseSuccess.ExecutionErrorSeverity, str]] = ..., message: _Optional[str] = ...) -> None: ...
        ERRORS_FIELD_NUMBER: _ClassVar[int]
        errors: _containers.RepeatedCompositeFieldContainer[GetJobErrorsResponse.GetJobErrorsResponseSuccess.Error]
        def __init__(self, errors: _Optional[_Iterable[_Union[GetJobErrorsResponse.GetJobErrorsResponseSuccess.Error, _Mapping]]] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: GetJobErrorsResponse.GetJobErrorsResponseSuccess
    error: GetJobErrorsResponse.GetJobErrorsResponseError
    def __init__(self, success: _Optional[_Union[GetJobErrorsResponse.GetJobErrorsResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[GetJobErrorsResponse.GetJobErrorsResponseError, _Mapping]] = ...) -> None: ...

class CancelRequest(_message.Message):
    __slots__ = ["job_id"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class CancelResponse(_message.Message):
    __slots__ = ["success", "error"]
    class CancelJobError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    class CancelJobSuccess(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: CancelResponse.CancelJobSuccess
    error: CancelResponse.CancelJobError
    def __init__(self, success: _Optional[_Union[CancelResponse.CancelJobSuccess, _Mapping]] = ..., error: _Optional[_Union[CancelResponse.CancelJobError, _Mapping]] = ...) -> None: ...

class GetJobResultStateRequest(_message.Message):
    __slots__ = ["job_id"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class GetJobResultStateResponse(_message.Message):
    __slots__ = ["success", "error"]
    class GetJobResultStateResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    class GetJobResultStateResponseSuccess(_message.Message):
        __slots__ = ["done", "closed", "has_dataloss"]
        DONE_FIELD_NUMBER: _ClassVar[int]
        CLOSED_FIELD_NUMBER: _ClassVar[int]
        HAS_DATALOSS_FIELD_NUMBER: _ClassVar[int]
        done: bool
        closed: bool
        has_dataloss: bool
        def __init__(self, done: bool = ..., closed: bool = ..., has_dataloss: bool = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: GetJobResultStateResponse.GetJobResultStateResponseSuccess
    error: GetJobResultStateResponse.GetJobResultStateResponseError
    def __init__(self, success: _Optional[_Union[GetJobResultStateResponse.GetJobResultStateResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[GetJobResultStateResponse.GetJobResultStateResponseError, _Mapping]] = ...) -> None: ...

class PullSamplesRequest(_message.Message):
    __slots__ = ["job_id", "include_analog", "include_digital"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ANALOG_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DIGITAL_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    include_analog: bool
    include_digital: bool
    def __init__(self, job_id: _Optional[str] = ..., include_analog: bool = ..., include_digital: bool = ...) -> None: ...

class PullSamplesResponse(_message.Message):
    __slots__ = ["success", "error"]
    class PullSamplesResponseError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    class PullSamplesResponseSuccess(_message.Message):
        __slots__ = ["controller", "fem_id", "port_id", "mode", "double_data", "boolean_data"]
        class Mode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
            ANALOG: _ClassVar[PullSamplesResponse.PullSamplesResponseSuccess.Mode]
            DIGITAL: _ClassVar[PullSamplesResponse.PullSamplesResponseSuccess.Mode]
        ANALOG: PullSamplesResponse.PullSamplesResponseSuccess.Mode
        DIGITAL: PullSamplesResponse.PullSamplesResponseSuccess.Mode
        class doubleData(_message.Message):
            __slots__ = ["mw", "lf"]
            MW_FIELD_NUMBER: _ClassVar[int]
            LF_FIELD_NUMBER: _ClassVar[int]
            mw: PullSamplesResponse.PullSamplesResponseSuccess.mw
            lf: PullSamplesResponse.PullSamplesResponseSuccess.lf
            def __init__(self, mw: _Optional[_Union[PullSamplesResponse.PullSamplesResponseSuccess.mw, _Mapping]] = ..., lf: _Optional[_Union[PullSamplesResponse.PullSamplesResponseSuccess.lf, _Mapping]] = ...) -> None: ...
        class mw(_message.Message):
            __slots__ = ["ducId", "I", "Q"]
            DUCID_FIELD_NUMBER: _ClassVar[int]
            I_FIELD_NUMBER: _ClassVar[int]
            Q_FIELD_NUMBER: _ClassVar[int]
            ducId: int
            I: _containers.RepeatedScalarFieldContainer[float]
            Q: _containers.RepeatedScalarFieldContainer[float]
            def __init__(self, ducId: _Optional[int] = ..., I: _Optional[_Iterable[float]] = ..., Q: _Optional[_Iterable[float]] = ...) -> None: ...
        class lf(_message.Message):
            __slots__ = ["items"]
            ITEMS_FIELD_NUMBER: _ClassVar[int]
            items: _containers.RepeatedScalarFieldContainer[float]
            def __init__(self, items: _Optional[_Iterable[float]] = ...) -> None: ...
        class booleanData(_message.Message):
            __slots__ = ["data"]
            class Data(_message.Message):
                __slots__ = ["item"]
                ITEM_FIELD_NUMBER: _ClassVar[int]
                item: _containers.RepeatedScalarFieldContainer[bool]
                def __init__(self, item: _Optional[_Iterable[bool]] = ...) -> None: ...
            DATA_FIELD_NUMBER: _ClassVar[int]
            data: _containers.RepeatedCompositeFieldContainer[PullSamplesResponse.PullSamplesResponseSuccess.booleanData.Data]
            def __init__(self, data: _Optional[_Iterable[_Union[PullSamplesResponse.PullSamplesResponseSuccess.booleanData.Data, _Mapping]]] = ...) -> None: ...
        CONTROLLER_FIELD_NUMBER: _ClassVar[int]
        FEM_ID_FIELD_NUMBER: _ClassVar[int]
        PORT_ID_FIELD_NUMBER: _ClassVar[int]
        MODE_FIELD_NUMBER: _ClassVar[int]
        DOUBLE_DATA_FIELD_NUMBER: _ClassVar[int]
        BOOLEAN_DATA_FIELD_NUMBER: _ClassVar[int]
        controller: str
        fem_id: int
        port_id: int
        mode: PullSamplesResponse.PullSamplesResponseSuccess.Mode
        double_data: PullSamplesResponse.PullSamplesResponseSuccess.doubleData
        boolean_data: PullSamplesResponse.PullSamplesResponseSuccess.booleanData
        def __init__(self, controller: _Optional[str] = ..., fem_id: _Optional[int] = ..., port_id: _Optional[int] = ..., mode: _Optional[_Union[PullSamplesResponse.PullSamplesResponseSuccess.Mode, str]] = ..., double_data: _Optional[_Union[PullSamplesResponse.PullSamplesResponseSuccess.doubleData, _Mapping]] = ..., boolean_data: _Optional[_Union[PullSamplesResponse.PullSamplesResponseSuccess.booleanData, _Mapping]] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: PullSamplesResponse.PullSamplesResponseSuccess
    error: PullSamplesResponse.PullSamplesResponseError
    def __init__(self, success: _Optional[_Union[PullSamplesResponse.PullSamplesResponseSuccess, _Mapping]] = ..., error: _Optional[_Union[PullSamplesResponse.PullSamplesResponseError, _Mapping]] = ...) -> None: ...

class SetOscillatorFrequencyRequest(_message.Message):
    __slots__ = ["job_id", "qe", "new_frequency_hz", "update_component"]
    class UpdateComponentSelection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        both: _ClassVar[SetOscillatorFrequencyRequest.UpdateComponentSelection]
        upconverter: _ClassVar[SetOscillatorFrequencyRequest.UpdateComponentSelection]
        downconverter: _ClassVar[SetOscillatorFrequencyRequest.UpdateComponentSelection]
    both: SetOscillatorFrequencyRequest.UpdateComponentSelection
    upconverter: SetOscillatorFrequencyRequest.UpdateComponentSelection
    downconverter: SetOscillatorFrequencyRequest.UpdateComponentSelection
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    QE_FIELD_NUMBER: _ClassVar[int]
    NEW_FREQUENCY_HZ_FIELD_NUMBER: _ClassVar[int]
    UPDATE_COMPONENT_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    qe: str
    new_frequency_hz: float
    update_component: SetOscillatorFrequencyRequest.UpdateComponentSelection
    def __init__(self, job_id: _Optional[str] = ..., qe: _Optional[str] = ..., new_frequency_hz: _Optional[float] = ..., update_component: _Optional[_Union[SetOscillatorFrequencyRequest.UpdateComponentSelection, str]] = ...) -> None: ...

class SetOscillatorFrequencyResponse(_message.Message):
    __slots__ = ["success", "error"]
    class ChangeOscillatorFrequencyError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    class ChangeOscillatorFrequencySuccess(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: SetOscillatorFrequencyResponse.ChangeOscillatorFrequencySuccess
    error: SetOscillatorFrequencyResponse.ChangeOscillatorFrequencyError
    def __init__(self, success: _Optional[_Union[SetOscillatorFrequencyResponse.ChangeOscillatorFrequencySuccess, _Mapping]] = ..., error: _Optional[_Union[SetOscillatorFrequencyResponse.ChangeOscillatorFrequencyError, _Mapping]] = ...) -> None: ...

class GetWaveformReportRequest(_message.Message):
    __slots__ = ["job_id"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class GetWaveformReportResponse(_message.Message):
    __slots__ = ["success", "error"]
    class GetWaveformReportSuccess(_message.Message):
        __slots__ = ["waveformReport"]
        WAVEFORMREPORT_FIELD_NUMBER: _ClassVar[int]
        waveformReport: _struct_pb2.Struct
        def __init__(self, waveformReport: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
    class GetWaveformReportError(_message.Message):
        __slots__ = ["details"]
        DETAILS_FIELD_NUMBER: _ClassVar[int]
        details: str
        def __init__(self, details: _Optional[str] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: GetWaveformReportResponse.GetWaveformReportSuccess
    error: GetWaveformReportResponse.GetWaveformReportError
    def __init__(self, success: _Optional[_Union[GetWaveformReportResponse.GetWaveformReportSuccess, _Mapping]] = ..., error: _Optional[_Union[GetWaveformReportResponse.GetWaveformReportError, _Mapping]] = ...) -> None: ...
