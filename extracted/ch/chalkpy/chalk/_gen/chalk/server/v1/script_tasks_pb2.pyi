from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.common.v1 import script_task_pb2 as _script_task_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class CreateScriptTaskRequest(_message.Message):
    __slots__ = ("request", "source_file")
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FILE_FIELD_NUMBER: _ClassVar[int]
    request: _script_task_pb2.ScriptTaskRequest
    source_file: bytes
    def __init__(
        self,
        request: _Optional[_Union[_script_task_pb2.ScriptTaskRequest, _Mapping]] = ...,
        source_file: _Optional[bytes] = ...,
    ) -> None: ...

class CreateScriptTaskResponse(_message.Message):
    __slots__ = ("task_id",)
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    def __init__(self, task_id: _Optional[str] = ...) -> None: ...

class ScriptTaskMeta(_message.Message):
    __slots__ = (
        "id",
        "status",
        "created_at",
        "completed_at",
        "branch_name",
        "raw_body_filename",
        "agent_id",
        "metadata",
        "kind",
        "deployment_id",
    )
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    RAW_BODY_FILENAME_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: _script_task_pb2.ScriptTaskStatus
    created_at: _timestamp_pb2.Timestamp
    completed_at: _timestamp_pb2.Timestamp
    branch_name: str
    raw_body_filename: str
    agent_id: str
    metadata: _containers.MessageMap[str, _struct_pb2.Value]
    kind: _script_task_pb2.ScriptTaskKind
    deployment_id: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        status: _Optional[_Union[_script_task_pb2.ScriptTaskStatus, str]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        completed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        branch_name: _Optional[str] = ...,
        raw_body_filename: _Optional[str] = ...,
        agent_id: _Optional[str] = ...,
        metadata: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
        kind: _Optional[_Union[_script_task_pb2.ScriptTaskKind, str]] = ...,
        deployment_id: _Optional[str] = ...,
    ) -> None: ...

class ListScriptTasksRequest(_message.Message):
    __slots__ = ("limit", "cursor", "filters", "start_time", "end_time")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    limit: int
    cursor: str
    filters: _containers.RepeatedCompositeFieldContainer[_script_task_pb2.ScriptTaskFilter]
    start_time: str
    end_time: str
    def __init__(
        self,
        limit: _Optional[int] = ...,
        cursor: _Optional[str] = ...,
        filters: _Optional[_Iterable[_Union[_script_task_pb2.ScriptTaskFilter, _Mapping]]] = ...,
        start_time: _Optional[str] = ...,
        end_time: _Optional[str] = ...,
    ) -> None: ...

class ListScriptTasksResponse(_message.Message):
    __slots__ = ("script_tasks", "next_cursor")
    SCRIPT_TASKS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    script_tasks: _containers.RepeatedCompositeFieldContainer[ScriptTaskMeta]
    next_cursor: str
    def __init__(
        self,
        script_tasks: _Optional[_Iterable[_Union[ScriptTaskMeta, _Mapping]]] = ...,
        next_cursor: _Optional[str] = ...,
    ) -> None: ...

class GetScriptTaskRequest(_message.Message):
    __slots__ = ("script_task_id",)
    SCRIPT_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    script_task_id: str
    def __init__(self, script_task_id: _Optional[str] = ...) -> None: ...

class GetScriptTaskResponse(_message.Message):
    __slots__ = ("script_task",)
    SCRIPT_TASK_FIELD_NUMBER: _ClassVar[int]
    script_task: ScriptTaskMeta
    def __init__(self, script_task: _Optional[_Union[ScriptTaskMeta, _Mapping]] = ...) -> None: ...

class GetScriptTaskSourceRequest(_message.Message):
    __slots__ = ("script_task_id",)
    SCRIPT_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    script_task_id: str
    def __init__(self, script_task_id: _Optional[str] = ...) -> None: ...

class GetScriptTaskSourceResponse(_message.Message):
    __slots__ = ("source_file_url", "inputs_file_url")
    SOURCE_FILE_URL_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FILE_URL_FIELD_NUMBER: _ClassVar[int]
    source_file_url: str
    inputs_file_url: str
    def __init__(self, source_file_url: _Optional[str] = ..., inputs_file_url: _Optional[str] = ...) -> None: ...

class CancelScriptTaskRequest(_message.Message):
    __slots__ = ("script_task_id",)
    SCRIPT_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    script_task_id: str
    def __init__(self, script_task_id: _Optional[str] = ...) -> None: ...

class CancelScriptTaskResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RerunScriptTaskRequest(_message.Message):
    __slots__ = ("script_task_id",)
    SCRIPT_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    script_task_id: str
    def __init__(self, script_task_id: _Optional[str] = ...) -> None: ...

class RerunScriptTaskResponse(_message.Message):
    __slots__ = ("new_script_task_id",)
    NEW_SCRIPT_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    new_script_task_id: str
    def __init__(self, new_script_task_id: _Optional[str] = ...) -> None: ...
