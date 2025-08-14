from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class SeriesDataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SERIES_DATA_TYPE_UNSPECIFIED: _ClassVar[SeriesDataType]
    DOUBLE: _ClassVar[SeriesDataType]
    STRING: _ClassVar[SeriesDataType]
    LOG: _ClassVar[SeriesDataType]
    INT: _ClassVar[SeriesDataType]
SERIES_DATA_TYPE_UNSPECIFIED: SeriesDataType
DOUBLE: SeriesDataType
STRING: SeriesDataType
LOG: SeriesDataType
INT: SeriesDataType
