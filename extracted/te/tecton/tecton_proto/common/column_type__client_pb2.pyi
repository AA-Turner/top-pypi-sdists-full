from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

COLUMN_TYPE_BOOL: ColumnType
COLUMN_TYPE_DERIVE_FROM_DATA_TYPE: ColumnType
COLUMN_TYPE_DOUBLE: ColumnType
COLUMN_TYPE_DOUBLE_ARRAY: ColumnType
COLUMN_TYPE_FLOAT_ARRAY: ColumnType
COLUMN_TYPE_INT64: ColumnType
COLUMN_TYPE_INT64_ARRAY: ColumnType
COLUMN_TYPE_STRING: ColumnType
COLUMN_TYPE_STRING_ARRAY: ColumnType
COLUMN_TYPE_UNKNOWN: ColumnType
DESCRIPTOR: _descriptor.FileDescriptor

class ColumnType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
