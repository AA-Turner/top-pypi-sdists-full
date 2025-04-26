from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor
FWV3: FrameworkVersion
FWV5: FrameworkVersion
FWV6: FrameworkVersion
UNSPECIFIED: FrameworkVersion

class FrameworkVersion(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
