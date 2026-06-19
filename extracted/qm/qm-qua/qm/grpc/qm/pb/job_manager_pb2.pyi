from qm.grpc.qm.pb import errors_pb2 as _errors_pb2
from qm.grpc.qm.pb import general_messages_pb2 as _general_messages_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetElementCorrectionRequest(_message.Message):
    __slots__ = ["jobId", "qeName", "correction"]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    QENAME_FIELD_NUMBER: _ClassVar[int]
    CORRECTION_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    qeName: str
    correction: _general_messages_pb2.Matrix
    def __init__(self, jobId: _Optional[str] = ..., qeName: _Optional[str] = ..., correction: _Optional[_Union[_general_messages_pb2.Matrix, _Mapping]] = ...) -> None: ...

class GetElementCorrectionResponse(_message.Message):
    __slots__ = ["jobManagerResponseHeader", "correction"]
    JOBMANAGERRESPONSEHEADER_FIELD_NUMBER: _ClassVar[int]
    CORRECTION_FIELD_NUMBER: _ClassVar[int]
    jobManagerResponseHeader: JobManagerResponseHeader
    correction: _general_messages_pb2.Matrix
    def __init__(self, jobManagerResponseHeader: _Optional[_Union[JobManagerResponseHeader, _Mapping]] = ..., correction: _Optional[_Union[_general_messages_pb2.Matrix, _Mapping]] = ...) -> None: ...

class SetElementCorrectionRequest(_message.Message):
    __slots__ = ["jobId", "qeName", "correction"]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    QENAME_FIELD_NUMBER: _ClassVar[int]
    CORRECTION_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    qeName: str
    correction: _general_messages_pb2.Matrix
    def __init__(self, jobId: _Optional[str] = ..., qeName: _Optional[str] = ..., correction: _Optional[_Union[_general_messages_pb2.Matrix, _Mapping]] = ...) -> None: ...

class SetElementCorrectionResponse(_message.Message):
    __slots__ = ["jobManagerResponseHeader", "correction"]
    JOBMANAGERRESPONSEHEADER_FIELD_NUMBER: _ClassVar[int]
    CORRECTION_FIELD_NUMBER: _ClassVar[int]
    jobManagerResponseHeader: JobManagerResponseHeader
    correction: _general_messages_pb2.Matrix
    def __init__(self, jobManagerResponseHeader: _Optional[_Union[JobManagerResponseHeader, _Mapping]] = ..., correction: _Optional[_Union[_general_messages_pb2.Matrix, _Mapping]] = ...) -> None: ...

class JobManagerResponseHeader(_message.Message):
    __slots__ = ["success", "jobId", "jobManagerErrorType", "jobErrorDetails"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    JOBMANAGERERRORTYPE_FIELD_NUMBER: _ClassVar[int]
    JOBERRORDETAILS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    jobId: str
    jobManagerErrorType: _errors_pb2.JobManagerErrorTypes
    jobErrorDetails: JobErrorDetails
    def __init__(self, success: bool = ..., jobId: _Optional[str] = ..., jobManagerErrorType: _Optional[_Union[_errors_pb2.JobManagerErrorTypes, str]] = ..., jobErrorDetails: _Optional[_Union[JobErrorDetails, _Mapping]] = ...) -> None: ...

class JobErrorDetails(_message.Message):
    __slots__ = ["jobOperationSpecificErrorType", "configQueryErrorType", "message"]
    JOBOPERATIONSPECIFICERRORTYPE_FIELD_NUMBER: _ClassVar[int]
    CONFIGQUERYERRORTYPE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    jobOperationSpecificErrorType: _errors_pb2.JobOperationSpecificErrorTypes
    configQueryErrorType: _errors_pb2.ConfigQueryErrorTypes
    message: str
    def __init__(self, jobOperationSpecificErrorType: _Optional[_Union[_errors_pb2.JobOperationSpecificErrorTypes, str]] = ..., configQueryErrorType: _Optional[_Union[_errors_pb2.ConfigQueryErrorTypes, str]] = ..., message: _Optional[str] = ...) -> None: ...

class JobOperationSpecificError(_message.Message):
    __slots__ = ["type", "message"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    type: _errors_pb2.JobOperationSpecificErrorTypes
    message: str
    def __init__(self, type: _Optional[_Union[_errors_pb2.JobOperationSpecificErrorTypes, str]] = ..., message: _Optional[str] = ...) -> None: ...

class InsertInputStreamRequest(_message.Message):
    __slots__ = ["jobId", "streamName", "intStreamData", "fixedStreamData", "boolStreamData"]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    STREAMNAME_FIELD_NUMBER: _ClassVar[int]
    INTSTREAMDATA_FIELD_NUMBER: _ClassVar[int]
    FIXEDSTREAMDATA_FIELD_NUMBER: _ClassVar[int]
    BOOLSTREAMDATA_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    streamName: str
    intStreamData: IntStreamData
    fixedStreamData: FixedStreamData
    boolStreamData: BoolStreamData
    def __init__(self, jobId: _Optional[str] = ..., streamName: _Optional[str] = ..., intStreamData: _Optional[_Union[IntStreamData, _Mapping]] = ..., fixedStreamData: _Optional[_Union[FixedStreamData, _Mapping]] = ..., boolStreamData: _Optional[_Union[BoolStreamData, _Mapping]] = ...) -> None: ...

class ChangeOscillatorFrequencyRequest(_message.Message):
    __slots__ = ["jobId", "elementName", "newFrequencyHz", "updateComponent"]
    class UpdateComponentSelection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        both: _ClassVar[ChangeOscillatorFrequencyRequest.UpdateComponentSelection]
        upconverter: _ClassVar[ChangeOscillatorFrequencyRequest.UpdateComponentSelection]
        downconverter: _ClassVar[ChangeOscillatorFrequencyRequest.UpdateComponentSelection]
    both: ChangeOscillatorFrequencyRequest.UpdateComponentSelection
    upconverter: ChangeOscillatorFrequencyRequest.UpdateComponentSelection
    downconverter: ChangeOscillatorFrequencyRequest.UpdateComponentSelection
    JOBID_FIELD_NUMBER: _ClassVar[int]
    ELEMENTNAME_FIELD_NUMBER: _ClassVar[int]
    NEWFREQUENCYHZ_FIELD_NUMBER: _ClassVar[int]
    UPDATECOMPONENT_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    elementName: str
    newFrequencyHz: float
    updateComponent: ChangeOscillatorFrequencyRequest.UpdateComponentSelection
    def __init__(self, jobId: _Optional[str] = ..., elementName: _Optional[str] = ..., newFrequencyHz: _Optional[float] = ..., updateComponent: _Optional[_Union[ChangeOscillatorFrequencyRequest.UpdateComponentSelection, str]] = ...) -> None: ...

class ChangeOscillatorFrequencyResponse(_message.Message):
    __slots__ = ["jobManagerResponseHeader"]
    JOBMANAGERRESPONSEHEADER_FIELD_NUMBER: _ClassVar[int]
    jobManagerResponseHeader: JobManagerResponseHeader
    def __init__(self, jobManagerResponseHeader: _Optional[_Union[JobManagerResponseHeader, _Mapping]] = ...) -> None: ...

class IntStreamData(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, data: _Optional[_Iterable[int]] = ...) -> None: ...

class FixedStreamData(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, data: _Optional[_Iterable[float]] = ...) -> None: ...

class BoolStreamData(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedScalarFieldContainer[bool]
    def __init__(self, data: _Optional[_Iterable[bool]] = ...) -> None: ...

class InsertInputStreamResponse(_message.Message):
    __slots__ = ["jobManagerResponseHeader"]
    JOBMANAGERRESPONSEHEADER_FIELD_NUMBER: _ClassVar[int]
    jobManagerResponseHeader: JobManagerResponseHeader
    def __init__(self, jobManagerResponseHeader: _Optional[_Union[JobManagerResponseHeader, _Mapping]] = ...) -> None: ...
