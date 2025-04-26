from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

AUDIT_LOG_METADATA_FIELD_NUMBER: _ClassVar[int]
DESCRIPTOR: _descriptor.FileDescriptor
OPTIONS_FIELD_NUMBER: _ClassVar[int]
TRANSFORM_LEGACY_ROLES: AuditLogTransform
TRANSFORM_REDACT_STRING: AuditLogTransform
TRANSFORM_UNSPECIFIED: AuditLogTransform
VISIBILITY_OMIT: Visibility
VISIBILITY_UNSPECIFIED: Visibility
VISIBILITY_VISIBLE: Visibility
audit_log_metadata: _descriptor.FieldDescriptor
options: _descriptor.FieldDescriptor

class AuditLogMetadata(_message.Message):
    __slots__ = ["customer_facing_event_name", "version", "write_to_audit_log"]
    CUSTOMER_FACING_EVENT_NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    WRITE_TO_AUDIT_LOG_FIELD_NUMBER: _ClassVar[int]
    customer_facing_event_name: str
    version: str
    write_to_audit_log: bool
    def __init__(self, write_to_audit_log: bool = ..., customer_facing_event_name: _Optional[str] = ..., version: _Optional[str] = ...) -> None: ...

class AuditLogOptions(_message.Message):
    __slots__ = ["transform", "visibility"]
    TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    transform: AuditLogTransform
    visibility: Visibility
    def __init__(self, visibility: _Optional[_Union[Visibility, str]] = ..., transform: _Optional[_Union[AuditLogTransform, str]] = ...) -> None: ...

class Visibility(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class AuditLogTransform(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
