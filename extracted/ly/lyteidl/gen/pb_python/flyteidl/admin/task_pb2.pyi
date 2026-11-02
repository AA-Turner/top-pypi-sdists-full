from flyteidl.core import identifier_pb2 as _identifier_pb2
from flyteidl.core import tasks_pb2 as _tasks_pb2
from flyteidl.core import compiler_pb2 as _compiler_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Task(_message.Message):
    __slots__ = ["closure", "id"]
    CLOSURE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    closure: TaskClosure
    id: _identifier_pb2.Identifier
    def __init__(self, id: _Optional[_Union[_identifier_pb2.Identifier, _Mapping]] = ..., closure: _Optional[_Union[TaskClosure, _Mapping]] = ...) -> None: ...

class TaskClosure(_message.Message):
    __slots__ = ["compiled_task", "created_at"]
    COMPILED_TASK_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    compiled_task: _compiler_pb2.CompiledTask
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, compiled_task: _Optional[_Union[_compiler_pb2.CompiledTask, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class TaskCreateRequest(_message.Message):
    __slots__ = ["id", "spec"]
    ID_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    id: _identifier_pb2.Identifier
    spec: TaskSpec
    def __init__(self, id: _Optional[_Union[_identifier_pb2.Identifier, _Mapping]] = ..., spec: _Optional[_Union[TaskSpec, _Mapping]] = ...) -> None: ...

class TaskCreateResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class TaskList(_message.Message):
    __slots__ = ["tasks", "token"]
    TASKS_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    tasks: _containers.RepeatedCompositeFieldContainer[Task]
    token: str
    def __init__(self, tasks: _Optional[_Iterable[_Union[Task, _Mapping]]] = ..., token: _Optional[str] = ...) -> None: ...

class TaskSpec(_message.Message):
    __slots__ = ["template"]
    TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    template: _tasks_pb2.TaskTemplate
    def __init__(self, template: _Optional[_Union[_tasks_pb2.TaskTemplate, _Mapping]] = ...) -> None: ...
