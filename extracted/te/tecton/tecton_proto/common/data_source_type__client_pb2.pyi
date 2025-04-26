from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

BATCH: DataSourceType
DESCRIPTOR: _descriptor.FileDescriptor
PUSH_NO_BATCH: DataSourceType
PUSH_WITH_BATCH: DataSourceType
STREAM_WITH_BATCH: DataSourceType
UNKNOWN: DataSourceType

class DataSourceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
