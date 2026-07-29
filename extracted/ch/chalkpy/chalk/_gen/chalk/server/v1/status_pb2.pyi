from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import struct_pb2 as _struct_pb2
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

class HealthCheckStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HEALTH_CHECK_STATUS_UNSPECIFIED: _ClassVar[HealthCheckStatus]
    HEALTH_CHECK_STATUS_OK: _ClassVar[HealthCheckStatus]
    HEALTH_CHECK_STATUS_FAILING: _ClassVar[HealthCheckStatus]
    HEALTH_CHECK_STATUS_NOT_CONFIGURED: _ClassVar[HealthCheckStatus]

class HealthCheckName(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HEALTH_CHECK_NAME_UNSPECIFIED: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_HTTP_ENGINE: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_SPILLING_CONFIG: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_GRPC_ENGINE: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_API_SERVER: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_KEDA_COMPONENTS: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_FUNCTION_QUEUE: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_CERTIFICATE_MANAGER: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_BRANCH_SERVER: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_GRPC_BRANCH_SERVER: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_STREAMING_SERVER: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_AWS_LOAD_BALANCER_CONTROLLER: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_PG_CRON: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_BACKGROUND_PERSISTENCE: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_BACKGROUND_PERSISTENCE_BUS_CONNECTIONS: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_LOGGING_CLIENT: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_FLUENT_BIT_METRICS: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_TELEMETRY_COLLECTORS: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_TELEMETRY_AGGREGATOR: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_CLICKHOUSE: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_METRICS_TIMESCALE_DB: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_METRICS_BACKUPS: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_AWS_METADATA_SERVER: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_CLOUD_ACCOUNT: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_CLOUD_NETWORKING: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_PUB_SUB: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_BASE_IMAGE_CONTAINER_REGISTRY: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_PUSH_CONTAINER_REGISTRY: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_SOURCE_BUCKET: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_DATASET_BUCKET: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_PLAN_STAGES_BUCKET: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_ETL_BUCKET: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_ARGO: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_KEDA: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_KARPENTER: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_KUBE_PERMISSIONS: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_ENVOY_PROXY: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_GATEWAY: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_GATEWAY_DNS: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_GATEWAY_ROUTABILITY: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_CNPG: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_METRICS_SERVER_CHART: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_KUBERNETES_METRICS: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_KUBERNETES_PROXY_ADDON: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_BILLING_SERVICE: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_OFFLINE_STORE_QUERY_VALUE_PERSISTENCE: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_EXTERNAL_DNS_CHART: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_OFFLINE_STORE: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_ONLINE_STORE: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_S3_CSI_DRIVER: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_CORE_DNS: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_VOLUME_SERVICE: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_VPC_CNI: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_EBS_CSI_DRIVER: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_VICTORIA_METRICS: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_COMPUTE_CONTAINER_REGISTRY: _ClassVar[HealthCheckName]
    HEALTH_CHECK_NAME_CHALK_MACHINE_TYPE_NODEPOOLS: _ClassVar[HealthCheckName]

HEALTH_CHECK_STATUS_UNSPECIFIED: HealthCheckStatus
HEALTH_CHECK_STATUS_OK: HealthCheckStatus
HEALTH_CHECK_STATUS_FAILING: HealthCheckStatus
HEALTH_CHECK_STATUS_NOT_CONFIGURED: HealthCheckStatus
HEALTH_CHECK_NAME_UNSPECIFIED: HealthCheckName
HEALTH_CHECK_NAME_HTTP_ENGINE: HealthCheckName
HEALTH_CHECK_NAME_SPILLING_CONFIG: HealthCheckName
HEALTH_CHECK_NAME_GRPC_ENGINE: HealthCheckName
HEALTH_CHECK_NAME_API_SERVER: HealthCheckName
HEALTH_CHECK_NAME_KEDA_COMPONENTS: HealthCheckName
HEALTH_CHECK_NAME_FUNCTION_QUEUE: HealthCheckName
HEALTH_CHECK_NAME_CERTIFICATE_MANAGER: HealthCheckName
HEALTH_CHECK_NAME_BRANCH_SERVER: HealthCheckName
HEALTH_CHECK_NAME_GRPC_BRANCH_SERVER: HealthCheckName
HEALTH_CHECK_NAME_STREAMING_SERVER: HealthCheckName
HEALTH_CHECK_NAME_AWS_LOAD_BALANCER_CONTROLLER: HealthCheckName
HEALTH_CHECK_NAME_PG_CRON: HealthCheckName
HEALTH_CHECK_NAME_BACKGROUND_PERSISTENCE: HealthCheckName
HEALTH_CHECK_NAME_BACKGROUND_PERSISTENCE_BUS_CONNECTIONS: HealthCheckName
HEALTH_CHECK_NAME_LOGGING_CLIENT: HealthCheckName
HEALTH_CHECK_NAME_FLUENT_BIT_METRICS: HealthCheckName
HEALTH_CHECK_NAME_TELEMETRY_COLLECTORS: HealthCheckName
HEALTH_CHECK_NAME_TELEMETRY_AGGREGATOR: HealthCheckName
HEALTH_CHECK_NAME_CLICKHOUSE: HealthCheckName
HEALTH_CHECK_NAME_METRICS_TIMESCALE_DB: HealthCheckName
HEALTH_CHECK_NAME_METRICS_BACKUPS: HealthCheckName
HEALTH_CHECK_NAME_AWS_METADATA_SERVER: HealthCheckName
HEALTH_CHECK_NAME_CLOUD_ACCOUNT: HealthCheckName
HEALTH_CHECK_NAME_CLOUD_NETWORKING: HealthCheckName
HEALTH_CHECK_NAME_PUB_SUB: HealthCheckName
HEALTH_CHECK_NAME_BASE_IMAGE_CONTAINER_REGISTRY: HealthCheckName
HEALTH_CHECK_NAME_PUSH_CONTAINER_REGISTRY: HealthCheckName
HEALTH_CHECK_NAME_SOURCE_BUCKET: HealthCheckName
HEALTH_CHECK_NAME_DATASET_BUCKET: HealthCheckName
HEALTH_CHECK_NAME_PLAN_STAGES_BUCKET: HealthCheckName
HEALTH_CHECK_NAME_ETL_BUCKET: HealthCheckName
HEALTH_CHECK_NAME_ARGO: HealthCheckName
HEALTH_CHECK_NAME_KEDA: HealthCheckName
HEALTH_CHECK_NAME_KARPENTER: HealthCheckName
HEALTH_CHECK_NAME_KUBE_PERMISSIONS: HealthCheckName
HEALTH_CHECK_NAME_ENVOY_PROXY: HealthCheckName
HEALTH_CHECK_NAME_GATEWAY: HealthCheckName
HEALTH_CHECK_NAME_GATEWAY_DNS: HealthCheckName
HEALTH_CHECK_NAME_GATEWAY_ROUTABILITY: HealthCheckName
HEALTH_CHECK_NAME_CNPG: HealthCheckName
HEALTH_CHECK_NAME_METRICS_SERVER_CHART: HealthCheckName
HEALTH_CHECK_NAME_KUBERNETES_METRICS: HealthCheckName
HEALTH_CHECK_NAME_KUBERNETES_PROXY_ADDON: HealthCheckName
HEALTH_CHECK_NAME_BILLING_SERVICE: HealthCheckName
HEALTH_CHECK_NAME_OFFLINE_STORE_QUERY_VALUE_PERSISTENCE: HealthCheckName
HEALTH_CHECK_NAME_EXTERNAL_DNS_CHART: HealthCheckName
HEALTH_CHECK_NAME_OFFLINE_STORE: HealthCheckName
HEALTH_CHECK_NAME_ONLINE_STORE: HealthCheckName
HEALTH_CHECK_NAME_S3_CSI_DRIVER: HealthCheckName
HEALTH_CHECK_NAME_CORE_DNS: HealthCheckName
HEALTH_CHECK_NAME_VOLUME_SERVICE: HealthCheckName
HEALTH_CHECK_NAME_VPC_CNI: HealthCheckName
HEALTH_CHECK_NAME_EBS_CSI_DRIVER: HealthCheckName
HEALTH_CHECK_NAME_VICTORIA_METRICS: HealthCheckName
HEALTH_CHECK_NAME_COMPUTE_CONTAINER_REGISTRY: HealthCheckName
HEALTH_CHECK_NAME_CHALK_MACHINE_TYPE_NODEPOOLS: HealthCheckName

class HealthCheck(_message.Message):
    __slots__ = ("name", "status", "message", "latency", "kube_data", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LATENCY_FIELD_NUMBER: _ClassVar[int]
    KUBE_DATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    name: str
    status: HealthCheckStatus
    message: str
    latency: _duration_pb2.Duration
    kube_data: _struct_pb2.Struct
    metadata: _containers.ScalarMap[str, str]
    def __init__(
        self,
        name: _Optional[str] = ...,
        status: _Optional[_Union[HealthCheckStatus, str]] = ...,
        message: _Optional[str] = ...,
        latency: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        kube_data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        metadata: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class HealthCheckFilters(_message.Message):
    __slots__ = ("name", "status")
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    name: _containers.RepeatedScalarFieldContainer[str]
    status: _containers.RepeatedScalarFieldContainer[HealthCheckStatus]
    def __init__(
        self, name: _Optional[_Iterable[str]] = ..., status: _Optional[_Iterable[_Union[HealthCheckStatus, str]]] = ...
    ) -> None: ...

class CheckHealthRequest(_message.Message):
    __slots__ = ("filters",)
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    filters: HealthCheckFilters
    def __init__(self, filters: _Optional[_Union[HealthCheckFilters, _Mapping]] = ...) -> None: ...

class CheckHealthResponse(_message.Message):
    __slots__ = ("checks",)
    CHECKS_FIELD_NUMBER: _ClassVar[int]
    checks: _containers.RepeatedCompositeFieldContainer[HealthCheck]
    def __init__(self, checks: _Optional[_Iterable[_Union[HealthCheck, _Mapping]]] = ...) -> None: ...

class GetHealthRequest(_message.Message):
    __slots__ = ("filters",)
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    filters: HealthCheckFilters
    def __init__(self, filters: _Optional[_Union[HealthCheckFilters, _Mapping]] = ...) -> None: ...

class GetHealthResponse(_message.Message):
    __slots__ = ("checks",)
    CHECKS_FIELD_NUMBER: _ClassVar[int]
    checks: _containers.RepeatedCompositeFieldContainer[HealthCheck]
    def __init__(self, checks: _Optional[_Iterable[_Union[HealthCheck, _Mapping]]] = ...) -> None: ...

class GetClusterMetricsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetClusterMetricsResponse(_message.Message):
    __slots__ = ("metrics",)
    METRICS_FIELD_NUMBER: _ClassVar[int]
    metrics: str
    def __init__(self, metrics: _Optional[str] = ...) -> None: ...
