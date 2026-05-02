from corvic_generated.status.v1 import event_pb2 as _event_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RunQuickModeRequest(_message.Message):
    __slots__ = ("source_ids",)
    SOURCE_IDS_FIELD_NUMBER: _ClassVar[int]
    source_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, source_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class RunQuickModeResponse(_message.Message):
    __slots__ = ("run_token",)
    RUN_TOKEN_FIELD_NUMBER: _ClassVar[int]
    run_token: str
    def __init__(self, run_token: _Optional[str] = ...) -> None: ...

class GetRunStatusRequest(_message.Message):
    __slots__ = ("run_token",)
    RUN_TOKEN_FIELD_NUMBER: _ClassVar[int]
    run_token: str
    def __init__(self, run_token: _Optional[str] = ...) -> None: ...

class CreatedObjects(_message.Message):
    __slots__ = ("feature_view_ids", "space_ids", "agent_ids")
    FEATURE_VIEW_IDS_FIELD_NUMBER: _ClassVar[int]
    SPACE_IDS_FIELD_NUMBER: _ClassVar[int]
    AGENT_IDS_FIELD_NUMBER: _ClassVar[int]
    feature_view_ids: _containers.RepeatedScalarFieldContainer[str]
    space_ids: _containers.RepeatedScalarFieldContainer[str]
    agent_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, feature_view_ids: _Optional[_Iterable[str]] = ..., space_ids: _Optional[_Iterable[str]] = ..., agent_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class GetRunStatusResponse(_message.Message):
    __slots__ = ("created_objects", "recent_events")
    CREATED_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    RECENT_EVENTS_FIELD_NUMBER: _ClassVar[int]
    created_objects: CreatedObjects
    recent_events: _containers.RepeatedCompositeFieldContainer[_event_pb2.Event]
    def __init__(self, created_objects: _Optional[_Union[CreatedObjects, _Mapping]] = ..., recent_events: _Optional[_Iterable[_Union[_event_pb2.Event, _Mapping]]] = ...) -> None: ...
