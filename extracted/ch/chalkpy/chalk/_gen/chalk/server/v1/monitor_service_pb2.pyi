from chalk._gen.chalk.artifacts.v1 import monitor_pb2 as _monitor_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import monitor_pb2 as _monitor_pb2_1
from google.protobuf import field_mask_pb2 as _field_mask_pb2
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

class GetMonitorRequest(_message.Message):
    __slots__ = ("monitor_id", "read_mask")
    MONITOR_ID_FIELD_NUMBER: _ClassVar[int]
    READ_MASK_FIELD_NUMBER: _ClassVar[int]
    monitor_id: str
    read_mask: _field_mask_pb2.FieldMask
    def __init__(
        self, monitor_id: _Optional[str] = ..., read_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...
    ) -> None: ...

class GetMonitorResponse(_message.Message):
    __slots__ = ("monitor", "has_active_incident")
    MONITOR_FIELD_NUMBER: _ClassVar[int]
    HAS_ACTIVE_INCIDENT_FIELD_NUMBER: _ClassVar[int]
    monitor: _monitor_pb2.Monitor
    has_active_incident: bool
    def __init__(
        self, monitor: _Optional[_Union[_monitor_pb2.Monitor, _Mapping]] = ..., has_active_incident: bool = ...
    ) -> None: ...

class GetMonitorEventsRequest(_message.Message):
    __slots__ = ("monitor_id",)
    MONITOR_ID_FIELD_NUMBER: _ClassVar[int]
    monitor_id: str
    def __init__(self, monitor_id: _Optional[str] = ...) -> None: ...

class GetMonitorEventsResponse(_message.Message):
    __slots__ = ("events",)
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[_monitor_pb2_1.MonitorEvent]
    def __init__(self, events: _Optional[_Iterable[_Union[_monitor_pb2_1.MonitorEvent, _Mapping]]] = ...) -> None: ...

class GetMonitorEvaluationRequest(_message.Message):
    __slots__ = ("monitor_id",)
    MONITOR_ID_FIELD_NUMBER: _ClassVar[int]
    monitor_id: str
    def __init__(self, monitor_id: _Optional[str] = ...) -> None: ...

class GetMonitorEvaluationResponse(_message.Message):
    __slots__ = ("evaluation",)
    EVALUATION_FIELD_NUMBER: _ClassVar[int]
    evaluation: _containers.RepeatedCompositeFieldContainer[_monitor_pb2_1.MonitorEvaluation]
    def __init__(
        self, evaluation: _Optional[_Iterable[_Union[_monitor_pb2_1.MonitorEvaluation, _Mapping]]] = ...
    ) -> None: ...

class CreateMonitorRequest(_message.Message):
    __slots__ = ("monitor",)
    MONITOR_FIELD_NUMBER: _ClassVar[int]
    monitor: _monitor_pb2.Monitor
    def __init__(self, monitor: _Optional[_Union[_monitor_pb2.Monitor, _Mapping]] = ...) -> None: ...

class CreateMonitorResponse(_message.Message):
    __slots__ = ("monitor",)
    MONITOR_FIELD_NUMBER: _ClassVar[int]
    monitor: _monitor_pb2.Monitor
    def __init__(self, monitor: _Optional[_Union[_monitor_pb2.Monitor, _Mapping]] = ...) -> None: ...

class UpdateMonitorRequest(_message.Message):
    __slots__ = ("monitor", "update_mask")
    MONITOR_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    monitor: _monitor_pb2.Monitor
    update_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        monitor: _Optional[_Union[_monitor_pb2.Monitor, _Mapping]] = ...,
        update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class UpdateMonitorResponse(_message.Message):
    __slots__ = ("monitor",)
    MONITOR_FIELD_NUMBER: _ClassVar[int]
    monitor: _monitor_pb2.Monitor
    def __init__(self, monitor: _Optional[_Union[_monitor_pb2.Monitor, _Mapping]] = ...) -> None: ...

class DeleteMonitorRequest(_message.Message):
    __slots__ = ("monitor_id",)
    MONITOR_ID_FIELD_NUMBER: _ClassVar[int]
    monitor_id: str
    def __init__(self, monitor_id: _Optional[str] = ...) -> None: ...

class DeleteMonitorResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListMonitorsRequest(_message.Message):
    __slots__ = ("limit", "cursor", "read_mask")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    READ_MASK_FIELD_NUMBER: _ClassVar[int]
    limit: int
    cursor: str
    read_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        limit: _Optional[int] = ...,
        cursor: _Optional[str] = ...,
        read_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class ListMonitorsResponse(_message.Message):
    __slots__ = ("monitors", "cursor", "monitor_has_active_incident")
    class MonitorHasActiveIncidentEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: bool
        def __init__(self, key: _Optional[str] = ..., value: bool = ...) -> None: ...

    MONITORS_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    MONITOR_HAS_ACTIVE_INCIDENT_FIELD_NUMBER: _ClassVar[int]
    monitors: _containers.RepeatedCompositeFieldContainer[_monitor_pb2.Monitor]
    cursor: str
    monitor_has_active_incident: _containers.ScalarMap[str, bool]
    def __init__(
        self,
        monitors: _Optional[_Iterable[_Union[_monitor_pb2.Monitor, _Mapping]]] = ...,
        cursor: _Optional[str] = ...,
        monitor_has_active_incident: _Optional[_Mapping[str, bool]] = ...,
    ) -> None: ...
