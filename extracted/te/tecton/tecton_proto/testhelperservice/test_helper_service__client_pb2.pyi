from tecton_proto.auth import service__client_pb2 as _service__client_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class IngestionServerConfigRequest(_message.Message):
    __slots__ = ["absolute_filepath", "offline_log_filepath"]
    ABSOLUTE_FILEPATH_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_LOG_FILEPATH_FIELD_NUMBER: _ClassVar[int]
    absolute_filepath: str
    offline_log_filepath: str
    def __init__(self, absolute_filepath: _Optional[str] = ..., offline_log_filepath: _Optional[str] = ...) -> None: ...

class IngestionServerConfigResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class InitializeStoreRequest(_message.Message):
    __slots__ = ["feature_view_name", "workspace"]
    FEATURE_VIEW_NAME_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    feature_view_name: str
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., feature_view_name: _Optional[str] = ...) -> None: ...

class InitializeStoreResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
