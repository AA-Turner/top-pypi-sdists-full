from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class OperationKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OPERATION_KIND_UNSPECIFIED: _ClassVar[OperationKind]
    OPERATION_KIND_ONLINE_QUERY: _ClassVar[OperationKind]
    OPERATION_KIND_MIGRATION: _ClassVar[OperationKind]
    OPERATION_KIND_CRON: _ClassVar[OperationKind]
    OPERATION_KIND_STREAMING: _ClassVar[OperationKind]
    OPERATION_KIND_MIGRATION_SAMPLER: _ClassVar[OperationKind]
    OPERATION_KIND_WINDOWED_STREAMING: _ClassVar[OperationKind]
    OPERATION_KIND_OFFLINE_QUERY: _ClassVar[OperationKind]

OPERATION_KIND_UNSPECIFIED: OperationKind
OPERATION_KIND_ONLINE_QUERY: OperationKind
OPERATION_KIND_MIGRATION: OperationKind
OPERATION_KIND_CRON: OperationKind
OPERATION_KIND_STREAMING: OperationKind
OPERATION_KIND_MIGRATION_SAMPLER: OperationKind
OPERATION_KIND_WINDOWED_STREAMING: OperationKind
OPERATION_KIND_OFFLINE_QUERY: OperationKind
