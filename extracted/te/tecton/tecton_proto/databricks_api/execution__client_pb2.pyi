from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CommandsExecuteRequest(_message.Message):
    __slots__ = ["clusterId", "command", "contextId", "language"]
    CLUSTERID_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    CONTEXTID_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    clusterId: str
    command: str
    contextId: str
    language: str
    def __init__(self, language: _Optional[str] = ..., clusterId: _Optional[str] = ..., contextId: _Optional[str] = ..., command: _Optional[str] = ...) -> None: ...

class CommandsExecuteResponse(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class CommandsStatusRequest(_message.Message):
    __slots__ = ["clusterId", "commandId", "contextId"]
    CLUSTERID_FIELD_NUMBER: _ClassVar[int]
    COMMANDID_FIELD_NUMBER: _ClassVar[int]
    CONTEXTID_FIELD_NUMBER: _ClassVar[int]
    clusterId: str
    commandId: str
    contextId: str
    def __init__(self, clusterId: _Optional[str] = ..., contextId: _Optional[str] = ..., commandId: _Optional[str] = ...) -> None: ...

class CommandsStatusResponse(_message.Message):
    __slots__ = ["results", "status"]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    results: Results
    status: str
    def __init__(self, results: _Optional[_Union[Results, _Mapping]] = ..., status: _Optional[str] = ...) -> None: ...

class ContextDestroyRequest(_message.Message):
    __slots__ = ["clusterId", "contextId"]
    CLUSTERID_FIELD_NUMBER: _ClassVar[int]
    CONTEXTID_FIELD_NUMBER: _ClassVar[int]
    clusterId: str
    contextId: str
    def __init__(self, clusterId: _Optional[str] = ..., contextId: _Optional[str] = ...) -> None: ...

class ContextDestroyResponse(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ContextStatusRequest(_message.Message):
    __slots__ = ["clusterId", "contextId"]
    CLUSTERID_FIELD_NUMBER: _ClassVar[int]
    CONTEXTID_FIELD_NUMBER: _ClassVar[int]
    clusterId: str
    contextId: str
    def __init__(self, clusterId: _Optional[str] = ..., contextId: _Optional[str] = ...) -> None: ...

class ContextStatusResponse(_message.Message):
    __slots__ = ["error", "id", "status"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    error: str
    id: str
    status: str
    def __init__(self, id: _Optional[str] = ..., status: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...

class ContextsCreateRequest(_message.Message):
    __slots__ = ["clusterId", "language"]
    CLUSTERID_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    clusterId: str
    language: str
    def __init__(self, language: _Optional[str] = ..., clusterId: _Optional[str] = ...) -> None: ...

class ContextsCreateResponse(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class Results(_message.Message):
    __slots__ = ["cause", "data", "resultType"]
    CAUSE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    RESULTTYPE_FIELD_NUMBER: _ClassVar[int]
    cause: str
    data: str
    resultType: str
    def __init__(self, data: _Optional[str] = ..., resultType: _Optional[str] = ..., cause: _Optional[str] = ...) -> None: ...
