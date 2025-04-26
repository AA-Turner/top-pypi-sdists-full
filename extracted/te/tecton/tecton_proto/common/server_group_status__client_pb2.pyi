from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor
SERVER_GROUP_STATUS_CREATING: ServerGroupStatus
SERVER_GROUP_STATUS_DELETING: ServerGroupStatus
SERVER_GROUP_STATUS_ERROR: ServerGroupStatus
SERVER_GROUP_STATUS_PENDING: ServerGroupStatus
SERVER_GROUP_STATUS_READY: ServerGroupStatus
SERVER_GROUP_STATUS_UNSPECIFIED: ServerGroupStatus
SERVER_GROUP_STATUS_UPDATING: ServerGroupStatus

class ServerGroupStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
