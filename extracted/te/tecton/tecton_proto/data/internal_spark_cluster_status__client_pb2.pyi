from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
INTERNAL_SPARK_CLUSTER_STATUS_CREATING_CLUSTER: InternalSparkClusterStatusEnum
INTERNAL_SPARK_CLUSTER_STATUS_HEALTHY: InternalSparkClusterStatusEnum
INTERNAL_SPARK_CLUSTER_STATUS_NOT_APPLICABLE: InternalSparkClusterStatusEnum
INTERNAL_SPARK_CLUSTER_STATUS_NO_CLUSTER: InternalSparkClusterStatusEnum
INTERNAL_SPARK_CLUSTER_STATUS_UNHEALTHY: InternalSparkClusterStatusEnum
INTERNAL_SPARK_CLUSTER_STATUS_UNSPECIFIED: InternalSparkClusterStatusEnum
INTERNAL_SPARK_CLUSTER_STATUS_WAITING_FOR_CLUSTER_TO_START: InternalSparkClusterStatusEnum

class InternalSparkClusterStatus(_message.Message):
    __slots__ = ["cluster_url", "error", "error_message", "status"]
    CLUSTER_URL_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    cluster_url: str
    error: bool
    error_message: str
    status: InternalSparkClusterStatusEnum
    def __init__(self, status: _Optional[_Union[InternalSparkClusterStatusEnum, str]] = ..., error: bool = ..., error_message: _Optional[str] = ..., cluster_url: _Optional[str] = ...) -> None: ...

class InternalSparkClusterStatusEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
