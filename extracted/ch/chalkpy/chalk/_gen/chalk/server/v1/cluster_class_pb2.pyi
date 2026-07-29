from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class ClusterClass(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLUSTER_CLASS_UNSPECIFIED: _ClassVar[ClusterClass]
    CLUSTER_CLASS_HOSTED: _ClassVar[ClusterClass]
    CLUSTER_CLASS_SERVERLESS: _ClassVar[ClusterClass]

CLUSTER_CLASS_UNSPECIFIED: ClusterClass
CLUSTER_CLASS_HOSTED: ClusterClass
CLUSTER_CLASS_SERVERLESS: ClusterClass
