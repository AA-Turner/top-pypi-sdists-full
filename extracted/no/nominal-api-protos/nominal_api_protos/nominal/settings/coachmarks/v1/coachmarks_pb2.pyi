import datetime

from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from nominal_api_protos.nominal.gen.v1 import alias_pb2 as _alias_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CoachmarkDismissal(_message.Message):
    __slots__ = ("user_rid", "coachmark_id", "app_version", "dismissed_at", "step_index")
    USER_RID_FIELD_NUMBER: _ClassVar[int]
    COACHMARK_ID_FIELD_NUMBER: _ClassVar[int]
    APP_VERSION_FIELD_NUMBER: _ClassVar[int]
    DISMISSED_AT_FIELD_NUMBER: _ClassVar[int]
    STEP_INDEX_FIELD_NUMBER: _ClassVar[int]
    user_rid: str
    coachmark_id: str
    app_version: str
    dismissed_at: _timestamp_pb2.Timestamp
    step_index: int
    def __init__(self, user_rid: _Optional[str] = ..., coachmark_id: _Optional[str] = ..., app_version: _Optional[str] = ..., dismissed_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., step_index: _Optional[int] = ...) -> None: ...

class DismissCoachmarkRequest(_message.Message):
    __slots__ = ("coachmark_id", "app_version", "step_index")
    COACHMARK_ID_FIELD_NUMBER: _ClassVar[int]
    APP_VERSION_FIELD_NUMBER: _ClassVar[int]
    STEP_INDEX_FIELD_NUMBER: _ClassVar[int]
    coachmark_id: str
    app_version: str
    step_index: int
    def __init__(self, coachmark_id: _Optional[str] = ..., app_version: _Optional[str] = ..., step_index: _Optional[int] = ...) -> None: ...

class DismissCoachmarkResponse(_message.Message):
    __slots__ = ("dismissal",)
    DISMISSAL_FIELD_NUMBER: _ClassVar[int]
    dismissal: CoachmarkDismissal
    def __init__(self, dismissal: _Optional[_Union[CoachmarkDismissal, _Mapping]] = ...) -> None: ...

class ListCoachmarkDismissalsRequest(_message.Message):
    __slots__ = ("coachmark_ids",)
    COACHMARK_IDS_FIELD_NUMBER: _ClassVar[int]
    coachmark_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, coachmark_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ListCoachmarkDismissalsResponse(_message.Message):
    __slots__ = ("dismissals",)
    class DismissalsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: CoachmarkDismissal
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[CoachmarkDismissal, _Mapping]] = ...) -> None: ...
    DISMISSALS_FIELD_NUMBER: _ClassVar[int]
    dismissals: _containers.MessageMap[str, CoachmarkDismissal]
    def __init__(self, dismissals: _Optional[_Mapping[str, CoachmarkDismissal]] = ...) -> None: ...

class GetCoachmarkDismissalRequest(_message.Message):
    __slots__ = ("coachmark_id",)
    COACHMARK_ID_FIELD_NUMBER: _ClassVar[int]
    coachmark_id: str
    def __init__(self, coachmark_id: _Optional[str] = ...) -> None: ...

class GetCoachmarkDismissalResponse(_message.Message):
    __slots__ = ("dismissal",)
    DISMISSAL_FIELD_NUMBER: _ClassVar[int]
    dismissal: CoachmarkDismissal
    def __init__(self, dismissal: _Optional[_Union[CoachmarkDismissal, _Mapping]] = ...) -> None: ...

class DeleteCoachmarkDismissalRequest(_message.Message):
    __slots__ = ("coachmark_id",)
    COACHMARK_ID_FIELD_NUMBER: _ClassVar[int]
    coachmark_id: str
    def __init__(self, coachmark_id: _Optional[str] = ...) -> None: ...

class DeleteCoachmarkDismissalResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
