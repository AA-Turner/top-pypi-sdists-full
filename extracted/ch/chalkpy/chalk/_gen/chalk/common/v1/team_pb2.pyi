from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class TeamCreationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TEAM_CREATION_TYPE_UNSPECIFIED: _ClassVar[TeamCreationType]
    TEAM_CREATION_TYPE_CHALK_MANAGED: _ClassVar[TeamCreationType]
    TEAM_CREATION_TYPE_SELF_SERVICE: _ClassVar[TeamCreationType]

TEAM_CREATION_TYPE_UNSPECIFIED: TeamCreationType
TEAM_CREATION_TYPE_CHALK_MANAGED: TeamCreationType
TEAM_CREATION_TYPE_SELF_SERVICE: TeamCreationType
