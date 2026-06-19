from google.protobuf import wrappers_pb2 as _wrappers_pb2
from qm.grpc.qm.pb import general_messages_pb2 as _general_messages_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetJobResultSchemaRequest(_message.Message):
    __slots__ = ["jobId"]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    def __init__(self, jobId: _Optional[str] = ...) -> None: ...

class GetJobResultSchemaResponse(_message.Message):
    __slots__ = ["items"]
    class Item(_message.Message):
        __slots__ = ["name", "simpleDType", "isSingle", "expectedCount", "shape"]
        NAME_FIELD_NUMBER: _ClassVar[int]
        SIMPLEDTYPE_FIELD_NUMBER: _ClassVar[int]
        ISSINGLE_FIELD_NUMBER: _ClassVar[int]
        EXPECTEDCOUNT_FIELD_NUMBER: _ClassVar[int]
        SHAPE_FIELD_NUMBER: _ClassVar[int]
        name: str
        simpleDType: str
        isSingle: bool
        expectedCount: int
        shape: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, name: _Optional[str] = ..., simpleDType: _Optional[str] = ..., isSingle: bool = ..., expectedCount: _Optional[int] = ..., shape: _Optional[_Iterable[int]] = ...) -> None: ...
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[GetJobResultSchemaResponse.Item]
    def __init__(self, items: _Optional[_Iterable[_Union[GetJobResultSchemaResponse.Item, _Mapping]]] = ...) -> None: ...

class GetJobStateRequest(_message.Message):
    __slots__ = ["jobId"]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    def __init__(self, jobId: _Optional[str] = ...) -> None: ...

class GetJobStateResponse(_message.Message):
    __slots__ = ["done", "closed", "hasDataloss"]
    DONE_FIELD_NUMBER: _ClassVar[int]
    CLOSED_FIELD_NUMBER: _ClassVar[int]
    HASDATALOSS_FIELD_NUMBER: _ClassVar[int]
    done: bool
    closed: bool
    hasDataloss: bool
    def __init__(self, done: bool = ..., closed: bool = ..., hasDataloss: bool = ...) -> None: ...

class GetJobNamedResultHeaderRequest(_message.Message):
    __slots__ = ["jobId", "outputName", "flatFormat"]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    OUTPUTNAME_FIELD_NUMBER: _ClassVar[int]
    FLATFORMAT_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    outputName: str
    flatFormat: bool
    def __init__(self, jobId: _Optional[str] = ..., outputName: _Optional[str] = ..., flatFormat: bool = ...) -> None: ...

class GetJobNamedResultHeaderResponse(_message.Message):
    __slots__ = ["isSingle", "countSoFar", "simpleDType", "done", "closed", "hasDataloss", "shape", "hasExecutionErrors"]
    ISSINGLE_FIELD_NUMBER: _ClassVar[int]
    COUNTSOFAR_FIELD_NUMBER: _ClassVar[int]
    SIMPLEDTYPE_FIELD_NUMBER: _ClassVar[int]
    DONE_FIELD_NUMBER: _ClassVar[int]
    CLOSED_FIELD_NUMBER: _ClassVar[int]
    HASDATALOSS_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    HASEXECUTIONERRORS_FIELD_NUMBER: _ClassVar[int]
    isSingle: bool
    countSoFar: int
    simpleDType: str
    done: bool
    closed: bool
    hasDataloss: bool
    shape: _containers.RepeatedScalarFieldContainer[int]
    hasExecutionErrors: _wrappers_pb2.BoolValue
    def __init__(self, isSingle: bool = ..., countSoFar: _Optional[int] = ..., simpleDType: _Optional[str] = ..., done: bool = ..., closed: bool = ..., hasDataloss: bool = ..., shape: _Optional[_Iterable[int]] = ..., hasExecutionErrors: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ...) -> None: ...

class GetJobNamedResultRequest(_message.Message):
    __slots__ = ["jobId", "outputName", "offset", "limit", "longOffset"]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    OUTPUTNAME_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    LONGOFFSET_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    outputName: str
    offset: int
    limit: int
    longOffset: _wrappers_pb2.Int64Value
    def __init__(self, jobId: _Optional[str] = ..., outputName: _Optional[str] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ..., longOffset: _Optional[_Union[_wrappers_pb2.Int64Value, _Mapping]] = ...) -> None: ...

class GetJobNamedResultResponse(_message.Message):
    __slots__ = ["countOfItems", "data"]
    COUNTOFITEMS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    countOfItems: int
    data: bytes
    def __init__(self, countOfItems: _Optional[int] = ..., data: _Optional[bytes] = ...) -> None: ...

class GetJobErrorsRequest(_message.Message):
    __slots__ = ["jobId"]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    def __init__(self, jobId: _Optional[str] = ...) -> None: ...

class GetJobErrorsResponse(_message.Message):
    __slots__ = ["errors", "jobId"]
    class ExecutionErrorSeverity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        ERROR: _ClassVar[GetJobErrorsResponse.ExecutionErrorSeverity]
        WARNING: _ClassVar[GetJobErrorsResponse.ExecutionErrorSeverity]
    ERROR: GetJobErrorsResponse.ExecutionErrorSeverity
    WARNING: GetJobErrorsResponse.ExecutionErrorSeverity
    class Error(_message.Message):
        __slots__ = ["errorCode", "errorSeverity", "message"]
        ERRORCODE_FIELD_NUMBER: _ClassVar[int]
        ERRORSEVERITY_FIELD_NUMBER: _ClassVar[int]
        MESSAGE_FIELD_NUMBER: _ClassVar[int]
        errorCode: int
        errorSeverity: GetJobErrorsResponse.ExecutionErrorSeverity
        message: str
        def __init__(self, errorCode: _Optional[int] = ..., errorSeverity: _Optional[_Union[GetJobErrorsResponse.ExecutionErrorSeverity, str]] = ..., message: _Optional[str] = ...) -> None: ...
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    errors: _containers.RepeatedCompositeFieldContainer[GetJobErrorsResponse.Error]
    jobId: str
    def __init__(self, errors: _Optional[_Iterable[_Union[GetJobErrorsResponse.Error, _Mapping]]] = ..., jobId: _Optional[str] = ...) -> None: ...

class PullAnalysedResultsRequest(_message.Message):
    __slots__ = ["jobFilePath", "metadata", "containsVersion"]
    JOBFILEPATH_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CONTAINSVERSION_FIELD_NUMBER: _ClassVar[int]
    jobFilePath: str
    metadata: str
    containsVersion: bool
    def __init__(self, jobFilePath: _Optional[str] = ..., metadata: _Optional[str] = ..., containsVersion: bool = ...) -> None: ...

class AnalysedResultsResponse(_message.Message):
    __slots__ = ["version", "icpResults", "streamResults", "errors"]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    ICPRESULTS_FIELD_NUMBER: _ClassVar[int]
    STREAMRESULTS_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    version: str
    icpResults: _containers.RepeatedCompositeFieldContainer[IcpResultData]
    streamResults: _containers.RepeatedCompositeFieldContainer[StreamResultData]
    errors: _containers.RepeatedCompositeFieldContainer[_general_messages_pb2.ErrorMessage]
    def __init__(self, version: _Optional[str] = ..., icpResults: _Optional[_Iterable[_Union[IcpResultData, _Mapping]]] = ..., streamResults: _Optional[_Iterable[_Union[StreamResultData, _Mapping]]] = ..., errors: _Optional[_Iterable[_Union[_general_messages_pb2.ErrorMessage, _Mapping]]] = ...) -> None: ...

class PullResultOutputRequest(_message.Message):
    __slots__ = ["jobId", "outputName"]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    OUTPUTNAME_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    outputName: str
    def __init__(self, jobId: _Optional[str] = ..., outputName: _Optional[str] = ...) -> None: ...

class PullResultOutputResponse(_message.Message):
    __slots__ = ["data", "header", "npz", "npy"]
    class Header(_message.Message):
        __slots__ = ["version", "outputName", "dataLoss", "errors", "single"]
        VERSION_FIELD_NUMBER: _ClassVar[int]
        OUTPUTNAME_FIELD_NUMBER: _ClassVar[int]
        DATALOSS_FIELD_NUMBER: _ClassVar[int]
        ERRORS_FIELD_NUMBER: _ClassVar[int]
        SINGLE_FIELD_NUMBER: _ClassVar[int]
        version: str
        outputName: str
        dataLoss: bool
        errors: _containers.RepeatedCompositeFieldContainer[_general_messages_pb2.ErrorMessage]
        single: bool
        def __init__(self, version: _Optional[str] = ..., outputName: _Optional[str] = ..., dataLoss: bool = ..., errors: _Optional[_Iterable[_Union[_general_messages_pb2.ErrorMessage, _Mapping]]] = ..., single: bool = ...) -> None: ...
    class Data(_message.Message):
        __slots__ = ["results"]
        RESULTS_FIELD_NUMBER: _ClassVar[int]
        results: _struct_pb2.Value
        def __init__(self, results: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    class Npz(_message.Message):
        __slots__ = ["npz"]
        NPZ_FIELD_NUMBER: _ClassVar[int]
        npz: bytes
        def __init__(self, npz: _Optional[bytes] = ...) -> None: ...
    class Npy(_message.Message):
        __slots__ = ["name", "npy", "count"]
        NAME_FIELD_NUMBER: _ClassVar[int]
        NPY_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        name: str
        npy: bytes
        count: int
        def __init__(self, name: _Optional[str] = ..., npy: _Optional[bytes] = ..., count: _Optional[int] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NPZ_FIELD_NUMBER: _ClassVar[int]
    NPY_FIELD_NUMBER: _ClassVar[int]
    data: PullResultOutputResponse.Data
    header: PullResultOutputResponse.Header
    npz: PullResultOutputResponse.Npz
    npy: PullResultOutputResponse.Npy
    def __init__(self, data: _Optional[_Union[PullResultOutputResponse.Data, _Mapping]] = ..., header: _Optional[_Union[PullResultOutputResponse.Header, _Mapping]] = ..., npz: _Optional[_Union[PullResultOutputResponse.Npz, _Mapping]] = ..., npy: _Optional[_Union[PullResultOutputResponse.Npy, _Mapping]] = ...) -> None: ...

class BinaryWrapper(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, data: _Optional[_Iterable[bytes]] = ...) -> None: ...

class PullFileResultRequest(_message.Message):
    __slots__ = ["jobId", "metadata", "asNpz"]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ASNPZ_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    metadata: str
    asNpz: bool
    def __init__(self, jobId: _Optional[str] = ..., metadata: _Optional[str] = ..., asNpz: bool = ...) -> None: ...

class FileResultResponse(_message.Message):
    __slots__ = ["jobId", "controllerName", "group", "npz", "version", "errors"]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    CONTROLLERNAME_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    NPZ_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    controllerName: str
    group: str
    npz: bytes
    version: str
    errors: _containers.RepeatedCompositeFieldContainer[_general_messages_pb2.ErrorMessage]
    def __init__(self, jobId: _Optional[str] = ..., controllerName: _Optional[str] = ..., group: _Optional[str] = ..., npz: _Optional[bytes] = ..., version: _Optional[str] = ..., errors: _Optional[_Iterable[_Union[_general_messages_pb2.ErrorMessage, _Mapping]]] = ...) -> None: ...

class PullSimulatorSamplesRequest(_message.Message):
    __slots__ = ["jobId", "includeAnalog", "includeDigital", "asNpz", "includeAllConnections"]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    INCLUDEANALOG_FIELD_NUMBER: _ClassVar[int]
    INCLUDEDIGITAL_FIELD_NUMBER: _ClassVar[int]
    ASNPZ_FIELD_NUMBER: _ClassVar[int]
    INCLUDEALLCONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    includeAnalog: bool
    includeDigital: bool
    asNpz: bool
    includeAllConnections: bool
    def __init__(self, jobId: _Optional[str] = ..., includeAnalog: bool = ..., includeDigital: bool = ..., asNpz: bool = ..., includeAllConnections: bool = ...) -> None: ...

class SimulatorSamplesResponse(_message.Message):
    __slots__ = ["jobId", "ok", "header", "data"]
    class Header(_message.Message):
        __slots__ = ["simpleDType", "countOfItems"]
        SIMPLEDTYPE_FIELD_NUMBER: _ClassVar[int]
        COUNTOFITEMS_FIELD_NUMBER: _ClassVar[int]
        simpleDType: str
        countOfItems: int
        def __init__(self, simpleDType: _Optional[str] = ..., countOfItems: _Optional[int] = ...) -> None: ...
    class Data(_message.Message):
        __slots__ = ["data"]
        DATA_FIELD_NUMBER: _ClassVar[int]
        data: bytes
        def __init__(self, data: _Optional[bytes] = ...) -> None: ...
    JOBID_FIELD_NUMBER: _ClassVar[int]
    OK_FIELD_NUMBER: _ClassVar[int]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    ok: bool
    header: SimulatorSamplesResponse.Header
    data: SimulatorSamplesResponse.Data
    def __init__(self, jobId: _Optional[str] = ..., ok: bool = ..., header: _Optional[_Union[SimulatorSamplesResponse.Header, _Mapping]] = ..., data: _Optional[_Union[SimulatorSamplesResponse.Data, _Mapping]] = ...) -> None: ...

class IcpResultData(_message.Message):
    __slots__ = ["name", "timestamp", "dataLoss", "intValue", "doubleValue", "booleanValue"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DATALOSS_FIELD_NUMBER: _ClassVar[int]
    INTVALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLEVALUE_FIELD_NUMBER: _ClassVar[int]
    BOOLEANVALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    timestamp: int
    dataLoss: bool
    intValue: int
    doubleValue: float
    booleanValue: bool
    def __init__(self, name: _Optional[str] = ..., timestamp: _Optional[int] = ..., dataLoss: bool = ..., intValue: _Optional[int] = ..., doubleValue: _Optional[float] = ..., booleanValue: bool = ...) -> None: ...

class StreamResultData(_message.Message):
    __slots__ = ["name", "timestamp", "dataLoss", "multipleSources", "dataSourceName", "data"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DATALOSS_FIELD_NUMBER: _ClassVar[int]
    MULTIPLESOURCES_FIELD_NUMBER: _ClassVar[int]
    DATASOURCENAME_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    name: str
    timestamp: int
    dataLoss: bool
    multipleSources: bool
    dataSourceName: str
    data: int
    def __init__(self, name: _Optional[str] = ..., timestamp: _Optional[int] = ..., dataLoss: bool = ..., multipleSources: bool = ..., dataSourceName: _Optional[str] = ..., data: _Optional[int] = ...) -> None: ...
