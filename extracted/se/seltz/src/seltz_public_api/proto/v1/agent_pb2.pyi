from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AgentRunStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AGENT_RUN_STATUS_UNSPECIFIED: _ClassVar[AgentRunStatus]
    AGENT_RUN_STATUS_PENDING: _ClassVar[AgentRunStatus]
    AGENT_RUN_STATUS_RUNNING: _ClassVar[AgentRunStatus]
    AGENT_RUN_STATUS_COMPLETED: _ClassVar[AgentRunStatus]
    AGENT_RUN_STATUS_FAILED: _ClassVar[AgentRunStatus]
    AGENT_RUN_STATUS_CANCELLED: _ClassVar[AgentRunStatus]

class AgentRunStopReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AGENT_RUN_STOP_REASON_UNSPECIFIED: _ClassVar[AgentRunStopReason]
    AGENT_RUN_STOP_REASON_FINISHED: _ClassVar[AgentRunStopReason]
    AGENT_RUN_STOP_REASON_BUDGET_REACHED: _ClassVar[AgentRunStopReason]
    AGENT_RUN_STOP_REASON_TIMEOUT: _ClassVar[AgentRunStopReason]
    AGENT_RUN_STOP_REASON_CANCELLED: _ClassVar[AgentRunStopReason]
    AGENT_RUN_STOP_REASON_INVALID_OUTPUT: _ClassVar[AgentRunStopReason]
    AGENT_RUN_STOP_REASON_INTERNAL_ERROR: _ClassVar[AgentRunStopReason]
AGENT_RUN_STATUS_UNSPECIFIED: AgentRunStatus
AGENT_RUN_STATUS_PENDING: AgentRunStatus
AGENT_RUN_STATUS_RUNNING: AgentRunStatus
AGENT_RUN_STATUS_COMPLETED: AgentRunStatus
AGENT_RUN_STATUS_FAILED: AgentRunStatus
AGENT_RUN_STATUS_CANCELLED: AgentRunStatus
AGENT_RUN_STOP_REASON_UNSPECIFIED: AgentRunStopReason
AGENT_RUN_STOP_REASON_FINISHED: AgentRunStopReason
AGENT_RUN_STOP_REASON_BUDGET_REACHED: AgentRunStopReason
AGENT_RUN_STOP_REASON_TIMEOUT: AgentRunStopReason
AGENT_RUN_STOP_REASON_CANCELLED: AgentRunStopReason
AGENT_RUN_STOP_REASON_INVALID_OUTPUT: AgentRunStopReason
AGENT_RUN_STOP_REASON_INTERNAL_ERROR: AgentRunStopReason

class CreateAgentRunRequest(_message.Message):
    __slots__ = ("query", "output_schema", "api_key")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    query: str
    output_schema: str
    api_key: str
    def __init__(self, query: _Optional[str] = ..., output_schema: _Optional[str] = ..., api_key: _Optional[str] = ...) -> None: ...

class CreateAgentRunResponse(_message.Message):
    __slots__ = ("run",)
    RUN_FIELD_NUMBER: _ClassVar[int]
    run: AgentRun
    def __init__(self, run: _Optional[_Union[AgentRun, _Mapping]] = ...) -> None: ...

class GetAgentRunRequest(_message.Message):
    __slots__ = ("run_id", "api_key")
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    run_id: str
    api_key: str
    def __init__(self, run_id: _Optional[str] = ..., api_key: _Optional[str] = ...) -> None: ...

class GetAgentRunResponse(_message.Message):
    __slots__ = ("run",)
    RUN_FIELD_NUMBER: _ClassVar[int]
    run: AgentRun
    def __init__(self, run: _Optional[_Union[AgentRun, _Mapping]] = ...) -> None: ...

class ListAgentRunsRequest(_message.Message):
    __slots__ = ("limit", "after", "api_key")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    AFTER_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    limit: int
    after: str
    api_key: str
    def __init__(self, limit: _Optional[int] = ..., after: _Optional[str] = ..., api_key: _Optional[str] = ...) -> None: ...

class ListAgentRunsResponse(_message.Message):
    __slots__ = ("runs", "next")
    RUNS_FIELD_NUMBER: _ClassVar[int]
    NEXT_FIELD_NUMBER: _ClassVar[int]
    runs: _containers.RepeatedCompositeFieldContainer[AgentRun]
    next: str
    def __init__(self, runs: _Optional[_Iterable[_Union[AgentRun, _Mapping]]] = ..., next: _Optional[str] = ...) -> None: ...

class CancelAgentRunRequest(_message.Message):
    __slots__ = ("run_id", "api_key")
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    run_id: str
    api_key: str
    def __init__(self, run_id: _Optional[str] = ..., api_key: _Optional[str] = ...) -> None: ...

class CancelAgentRunResponse(_message.Message):
    __slots__ = ("run",)
    RUN_FIELD_NUMBER: _ClassVar[int]
    run: AgentRun
    def __init__(self, run: _Optional[_Union[AgentRun, _Mapping]] = ...) -> None: ...

class AgentRun(_message.Message):
    __slots__ = ("id", "object", "status", "stop_reason", "created_at", "started_at", "completed_at", "request", "output")
    ID_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STOP_REASON_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    id: str
    object: str
    status: AgentRunStatus
    stop_reason: AgentRunStopReason
    created_at: str
    started_at: str
    completed_at: str
    request: AgentRunRequest
    output: AgentRunOutput
    def __init__(self, id: _Optional[str] = ..., object: _Optional[str] = ..., status: _Optional[_Union[AgentRunStatus, str]] = ..., stop_reason: _Optional[_Union[AgentRunStopReason, str]] = ..., created_at: _Optional[str] = ..., started_at: _Optional[str] = ..., completed_at: _Optional[str] = ..., request: _Optional[_Union[AgentRunRequest, _Mapping]] = ..., output: _Optional[_Union[AgentRunOutput, _Mapping]] = ...) -> None: ...

class AgentRunRequest(_message.Message):
    __slots__ = ("query", "output_schema")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    query: str
    output_schema: str
    def __init__(self, query: _Optional[str] = ..., output_schema: _Optional[str] = ...) -> None: ...

class AgentRunOutput(_message.Message):
    __slots__ = ("text", "structured", "sources", "grounding")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    STRUCTURED_FIELD_NUMBER: _ClassVar[int]
    SOURCES_FIELD_NUMBER: _ClassVar[int]
    GROUNDING_FIELD_NUMBER: _ClassVar[int]
    text: str
    structured: str
    sources: _containers.RepeatedCompositeFieldContainer[AgentRunSource]
    grounding: _containers.RepeatedCompositeFieldContainer[AgentRunGrounding]
    def __init__(self, text: _Optional[str] = ..., structured: _Optional[str] = ..., sources: _Optional[_Iterable[_Union[AgentRunSource, _Mapping]]] = ..., grounding: _Optional[_Iterable[_Union[AgentRunGrounding, _Mapping]]] = ...) -> None: ...

class AgentRunSource(_message.Message):
    __slots__ = ("url", "id")
    URL_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    url: str
    id: int
    def __init__(self, url: _Optional[str] = ..., id: _Optional[int] = ...) -> None: ...

class AgentRunGrounding(_message.Message):
    __slots__ = ("field", "citations")
    FIELD_FIELD_NUMBER: _ClassVar[int]
    CITATIONS_FIELD_NUMBER: _ClassVar[int]
    field: str
    citations: _containers.RepeatedCompositeFieldContainer[AgentRunCitation]
    def __init__(self, field: _Optional[str] = ..., citations: _Optional[_Iterable[_Union[AgentRunCitation, _Mapping]]] = ...) -> None: ...

class AgentRunCitation(_message.Message):
    __slots__ = ("url", "source_id")
    URL_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    url: str
    source_id: int
    def __init__(self, url: _Optional[str] = ..., source_id: _Optional[int] = ...) -> None: ...
