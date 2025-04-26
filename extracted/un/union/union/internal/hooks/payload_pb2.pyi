from flyteidl.event import cloudevents_pb2 as _cloudevents_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    UNSPECIFIED: _ClassVar[EventType]
    WORKFLOW_EXECUTION: _ClassVar[EventType]
    NODE_EXECUTION: _ClassVar[EventType]
    TASK_EXECUTION: _ClassVar[EventType]
UNSPECIFIED: EventType
WORKFLOW_EXECUTION: EventType
NODE_EXECUTION: EventType
TASK_EXECUTION: EventType

class EventFilters(_message.Message):
    __slots__ = ["event_types"]
    EVENT_TYPES_FIELD_NUMBER: _ClassVar[int]
    event_types: _containers.RepeatedScalarFieldContainer[EventType]
    def __init__(self, event_types: _Optional[_Iterable[_Union[EventType, str]]] = ...) -> None: ...

class StreamEventsRequest(_message.Message):
    __slots__ = ["filters"]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    filters: EventFilters
    def __init__(self, filters: _Optional[_Union[EventFilters, _Mapping]] = ...) -> None: ...

class StreamEventsResponse(_message.Message):
    __slots__ = ["workflow_execution", "node_execution", "task_execution", "id"]
    WORKFLOW_EXECUTION_FIELD_NUMBER: _ClassVar[int]
    NODE_EXECUTION_FIELD_NUMBER: _ClassVar[int]
    TASK_EXECUTION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    workflow_execution: _cloudevents_pb2.CloudEventWorkflowExecution
    node_execution: _cloudevents_pb2.CloudEventNodeExecution
    task_execution: _cloudevents_pb2.CloudEventTaskExecution
    id: str
    def __init__(self, workflow_execution: _Optional[_Union[_cloudevents_pb2.CloudEventWorkflowExecution, _Mapping]] = ..., node_execution: _Optional[_Union[_cloudevents_pb2.CloudEventNodeExecution, _Mapping]] = ..., task_execution: _Optional[_Union[_cloudevents_pb2.CloudEventTaskExecution, _Mapping]] = ..., id: _Optional[str] = ...) -> None: ...

class AcknowledgeEventRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class AcknowledgeEventResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
