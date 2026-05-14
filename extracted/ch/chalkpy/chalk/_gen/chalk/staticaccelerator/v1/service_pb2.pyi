from chalk._gen.chalk.artifacts.v1 import export_pb2 as _export_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HealthCheckRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class HealthCheckResponse(_message.Message):
    __slots__ = ("status", "service")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    status: str
    service: str
    def __init__(self, status: _Optional[str] = ..., service: _Optional[str] = ...) -> None: ...

class GetStaticConversionDiagnosticsRequest(_message.Message):
    __slots__ = ("export", "render_failed_proofs")
    EXPORT_FIELD_NUMBER: _ClassVar[int]
    RENDER_FAILED_PROOFS_FIELD_NUMBER: _ClassVar[int]
    export: _export_pb2.Export
    render_failed_proofs: bool
    def __init__(
        self, export: _Optional[_Union[_export_pb2.Export, _Mapping]] = ..., render_failed_proofs: bool = ...
    ) -> None: ...
