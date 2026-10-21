from chalk._gen.buf.validate import validate_pb2 as _validate_pb2
from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class QuotaResourceKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    QUOTA_RESOURCE_KIND_UNSPECIFIED: _ClassVar[QuotaResourceKind]
    QUOTA_RESOURCE_KIND_CPU_MILLICORES: _ClassVar[QuotaResourceKind]
    QUOTA_RESOURCE_KIND_MEMORY_BYTES: _ClassVar[QuotaResourceKind]
    QUOTA_RESOURCE_KIND_GPU_COUNT: _ClassVar[QuotaResourceKind]
    QUOTA_RESOURCE_KIND_GPU_FAMILY: _ClassVar[QuotaResourceKind]
    QUOTA_RESOURCE_KIND_SANDBOX_COUNT: _ClassVar[QuotaResourceKind]
    QUOTA_RESOURCE_KIND_SCALING_GROUP_COUNT: _ClassVar[QuotaResourceKind]
    QUOTA_RESOURCE_KIND_FUNCTION_COUNT: _ClassVar[QuotaResourceKind]
    QUOTA_RESOURCE_KIND_MODEL_DEPLOYMENT_COUNT: _ClassVar[QuotaResourceKind]
    QUOTA_RESOURCE_KIND_NOTEBOOK_COUNT: _ClassVar[QuotaResourceKind]

class QuotaWorkloadKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    QUOTA_WORKLOAD_KIND_UNSPECIFIED: _ClassVar[QuotaWorkloadKind]
    QUOTA_WORKLOAD_KIND_SANDBOX: _ClassVar[QuotaWorkloadKind]
    QUOTA_WORKLOAD_KIND_SCALING_GROUP: _ClassVar[QuotaWorkloadKind]
    QUOTA_WORKLOAD_KIND_FUNCTION: _ClassVar[QuotaWorkloadKind]
    QUOTA_WORKLOAD_KIND_MODEL_DEPLOYMENT: _ClassVar[QuotaWorkloadKind]
    QUOTA_WORKLOAD_KIND_NOTEBOOK: _ClassVar[QuotaWorkloadKind]

QUOTA_RESOURCE_KIND_UNSPECIFIED: QuotaResourceKind
QUOTA_RESOURCE_KIND_CPU_MILLICORES: QuotaResourceKind
QUOTA_RESOURCE_KIND_MEMORY_BYTES: QuotaResourceKind
QUOTA_RESOURCE_KIND_GPU_COUNT: QuotaResourceKind
QUOTA_RESOURCE_KIND_GPU_FAMILY: QuotaResourceKind
QUOTA_RESOURCE_KIND_SANDBOX_COUNT: QuotaResourceKind
QUOTA_RESOURCE_KIND_SCALING_GROUP_COUNT: QuotaResourceKind
QUOTA_RESOURCE_KIND_FUNCTION_COUNT: QuotaResourceKind
QUOTA_RESOURCE_KIND_MODEL_DEPLOYMENT_COUNT: QuotaResourceKind
QUOTA_RESOURCE_KIND_NOTEBOOK_COUNT: QuotaResourceKind
QUOTA_WORKLOAD_KIND_UNSPECIFIED: QuotaWorkloadKind
QUOTA_WORKLOAD_KIND_SANDBOX: QuotaWorkloadKind
QUOTA_WORKLOAD_KIND_SCALING_GROUP: QuotaWorkloadKind
QUOTA_WORKLOAD_KIND_FUNCTION: QuotaWorkloadKind
QUOTA_WORKLOAD_KIND_MODEL_DEPLOYMENT: QuotaWorkloadKind
QUOTA_WORKLOAD_KIND_NOTEBOOK: QuotaWorkloadKind

class QuotaResource(_message.Message):
    __slots__ = ("kind", "gpu_family")
    KIND_FIELD_NUMBER: _ClassVar[int]
    GPU_FAMILY_FIELD_NUMBER: _ClassVar[int]
    kind: QuotaResourceKind
    gpu_family: str
    def __init__(
        self, kind: _Optional[_Union[QuotaResourceKind, str]] = ..., gpu_family: _Optional[str] = ...
    ) -> None: ...

class QuotaLimit(_message.Message):
    __slots__ = ("value", "unlimited")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    UNLIMITED_FIELD_NUMBER: _ClassVar[int]
    value: int
    unlimited: bool
    def __init__(self, value: _Optional[int] = ..., unlimited: bool = ...) -> None: ...

class Quota(_message.Message):
    __slots__ = ("resource", "display_name", "limit", "usage", "available", "updated_at", "updated_by")
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_BY_FIELD_NUMBER: _ClassVar[int]
    resource: QuotaResource
    display_name: str
    limit: QuotaLimit
    usage: int
    available: int
    updated_at: _timestamp_pb2.Timestamp
    updated_by: str
    def __init__(
        self,
        resource: _Optional[_Union[QuotaResource, _Mapping]] = ...,
        display_name: _Optional[str] = ...,
        limit: _Optional[_Union[QuotaLimit, _Mapping]] = ...,
        usage: _Optional[int] = ...,
        available: _Optional[int] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_by: _Optional[str] = ...,
    ) -> None: ...

class ListQuotasRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListQuotasResponse(_message.Message):
    __slots__ = ("enabled", "quotas")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    QUOTAS_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    quotas: _containers.RepeatedCompositeFieldContainer[Quota]
    def __init__(self, enabled: bool = ..., quotas: _Optional[_Iterable[_Union[Quota, _Mapping]]] = ...) -> None: ...

class GetQuotaRequest(_message.Message):
    __slots__ = ("resource",)
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    resource: QuotaResource
    def __init__(self, resource: _Optional[_Union[QuotaResource, _Mapping]] = ...) -> None: ...

class GetQuotaResponse(_message.Message):
    __slots__ = ("enabled", "quota")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    QUOTA_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    quota: Quota
    def __init__(self, enabled: bool = ..., quota: _Optional[_Union[Quota, _Mapping]] = ...) -> None: ...

class SetQuotaRequest(_message.Message):
    __slots__ = ("resource", "limit")
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    resource: QuotaResource
    limit: QuotaLimit
    def __init__(
        self,
        resource: _Optional[_Union[QuotaResource, _Mapping]] = ...,
        limit: _Optional[_Union[QuotaLimit, _Mapping]] = ...,
    ) -> None: ...

class SetQuotaResponse(_message.Message):
    __slots__ = ("quota",)
    QUOTA_FIELD_NUMBER: _ClassVar[int]
    quota: Quota
    def __init__(self, quota: _Optional[_Union[Quota, _Mapping]] = ...) -> None: ...

class ClearQuotaRequest(_message.Message):
    __slots__ = ("resource",)
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    resource: QuotaResource
    def __init__(self, resource: _Optional[_Union[QuotaResource, _Mapping]] = ...) -> None: ...

class ClearQuotaResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RequestQuotaIncreaseRequest(_message.Message):
    __slots__ = ("resource", "requested_limit", "comment")
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_LIMIT_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    resource: QuotaResource
    requested_limit: QuotaLimit
    comment: str
    def __init__(
        self,
        resource: _Optional[_Union[QuotaResource, _Mapping]] = ...,
        requested_limit: _Optional[_Union[QuotaLimit, _Mapping]] = ...,
        comment: _Optional[str] = ...,
    ) -> None: ...

class RequestQuotaIncreaseResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
