from chalk._gen.chalk.artifacts.v1 import export_pb2 as _export_pb2
from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.graph.v1 import graph_pb2 as _graph_pb2
from chalk._gen.chalk.lsp.v1 import lsp_pb2 as _lsp_pb2
from chalk._gen.chalk.nodepools.v1 import gke_pb2 as _gke_pb2
from chalk._gen.chalk.nodepools.v1 import karpenter_pb2 as _karpenter_pb2
from chalk._gen.chalk.server.v1 import deployment_pb2 as _deployment_pb2
from chalk._gen.chalk.server.v1 import environment_pb2 as _environment_pb2
from chalk._gen.chalk.server.v1 import graph_pb2 as _graph_pb2_1
from chalk._gen.chalk.server.v1 import log_pb2 as _log_pb2
from chalk._gen.chalk.usage.v1 import rate_pb2 as _rate_pb2
from chalk._gen.chalk.utils.v1 import field_change_pb2 as _field_change_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
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

class DeploymentBuildStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DEPLOYMENT_BUILD_STATUS_UNSPECIFIED: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_UNKNOWN: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_PENDING: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_QUEUED: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_WORKING: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_SUCCESS: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_FAILURE: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_INTERNAL_ERROR: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_TIMEOUT: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_CANCELLED: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_EXPIRED: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_BOOT_ERRORS: _ClassVar[DeploymentBuildStatus]

class CustomerVectorAggregatorStatsdProtocol(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CUSTOMER_VECTOR_AGGREGATOR_STATSD_PROTOCOL_UNSPECIFIED: _ClassVar[CustomerVectorAggregatorStatsdProtocol]
    CUSTOMER_VECTOR_AGGREGATOR_STATSD_PROTOCOL_UDP: _ClassVar[CustomerVectorAggregatorStatsdProtocol]
    CUSTOMER_VECTOR_AGGREGATOR_STATSD_PROTOCOL_TCP: _ClassVar[CustomerVectorAggregatorStatsdProtocol]

class TelemetryCollectorTolerationMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TELEMETRY_COLLECTOR_TOLERATION_MODE_UNSPECIFIED: _ClassVar[TelemetryCollectorTolerationMode]
    TELEMETRY_COLLECTOR_TOLERATION_MODE_NO_SCHEDULE_ALL: _ClassVar[TelemetryCollectorTolerationMode]
    TELEMETRY_COLLECTOR_TOLERATION_MODE_NO_SCHEDULE_ALL_EXCEPT_NO_NETWORK: _ClassVar[TelemetryCollectorTolerationMode]

class OtelCollectorImage(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OTEL_COLLECTOR_IMAGE_UNSPECIFIED: _ClassVar[OtelCollectorImage]
    OTEL_COLLECTOR_IMAGE_UPSTREAM_CONTRIB: _ClassVar[OtelCollectorImage]
    OTEL_COLLECTOR_IMAGE_CHALK_SHARED: _ClassVar[OtelCollectorImage]

class TelemetryRuntime(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TELEMETRY_RUNTIME_UNSPECIFIED: _ClassVar[TelemetryRuntime]
    TELEMETRY_RUNTIME_OTEL: _ClassVar[TelemetryRuntime]
    TELEMETRY_RUNTIME_VECTOR: _ClassVar[TelemetryRuntime]

class TelemetryPrometheusCollectionRuntime(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TELEMETRY_PROMETHEUS_COLLECTION_RUNTIME_UNSPECIFIED: _ClassVar[TelemetryPrometheusCollectionRuntime]
    TELEMETRY_PROMETHEUS_COLLECTION_RUNTIME_VECTOR_COLLECTOR: _ClassVar[TelemetryPrometheusCollectionRuntime]
    TELEMETRY_PROMETHEUS_COLLECTION_RUNTIME_VICTORIA_METRICS: _ClassVar[TelemetryPrometheusCollectionRuntime]

class MetricExportDestinationFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    METRIC_EXPORT_DESTINATION_FORMAT_UNSPECIFIED: _ClassVar[MetricExportDestinationFormat]
    METRIC_EXPORT_DESTINATION_FORMAT_PROMETHEUS_REMOTE_WRITE: _ClassVar[MetricExportDestinationFormat]
    METRIC_EXPORT_DESTINATION_FORMAT_STATSD: _ClassVar[MetricExportDestinationFormat]

class VectorClusterMetricsSinkMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VECTOR_CLUSTER_METRICS_SINK_MODE_UNSPECIFIED: _ClassVar[VectorClusterMetricsSinkMode]
    VECTOR_CLUSTER_METRICS_SINK_MODE_DISABLED: _ClassVar[VectorClusterMetricsSinkMode]
    VECTOR_CLUSTER_METRICS_SINK_MODE_SHADOW: _ClassVar[VectorClusterMetricsSinkMode]
    VECTOR_CLUSTER_METRICS_SINK_MODE_WRITE: _ClassVar[VectorClusterMetricsSinkMode]

class VectorClusterMetricsShadowOutput(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VECTOR_CLUSTER_METRICS_SHADOW_OUTPUT_UNSPECIFIED: _ClassVar[VectorClusterMetricsShadowOutput]
    VECTOR_CLUSTER_METRICS_SHADOW_OUTPUT_STDOUT: _ClassVar[VectorClusterMetricsShadowOutput]
    VECTOR_CLUSTER_METRICS_SHADOW_OUTPUT_TABLE: _ClassVar[VectorClusterMetricsShadowOutput]

class PerfettoTrigger(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PERFETTO_TRIGGER_UNSPECIFIED: _ClassVar[PerfettoTrigger]
    PERFETTO_TRIGGER_TIME_INTERVAL: _ClassVar[PerfettoTrigger]
    PERFETTO_TRIGGER_HTTP: _ClassVar[PerfettoTrigger]

class NetworkInspectorTrigger(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NETWORK_INSPECTOR_TRIGGER_UNSPECIFIED: _ClassVar[NetworkInspectorTrigger]
    NETWORK_INSPECTOR_TRIGGER_START_ON_LAUNCH: _ClassVar[NetworkInspectorTrigger]
    NETWORK_INSPECTOR_TRIGGER_HTTP: _ClassVar[NetworkInspectorTrigger]

class BranchScalingState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BRANCH_SCALING_STATE_UNSPECIFIED: _ClassVar[BranchScalingState]
    BRANCH_SCALING_STATE_SUCCESS: _ClassVar[BranchScalingState]
    BRANCH_SCALING_STATE_IN_PROGRESS: _ClassVar[BranchScalingState]

class BranchServerStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BRANCH_SERVER_STATUS_UNSPECIFIED: _ClassVar[BranchServerStatus]
    BRANCH_SERVER_STATUS_READY: _ClassVar[BranchServerStatus]
    BRANCH_SERVER_STATUS_STARTING: _ClassVar[BranchServerStatus]
    BRANCH_SERVER_STATUS_STOPPING: _ClassVar[BranchServerStatus]
    BRANCH_SERVER_STATUS_PAUSED: _ClassVar[BranchServerStatus]
    BRANCH_SERVER_STATUS_OFFLINE: _ClassVar[BranchServerStatus]
    BRANCH_SERVER_STATUS_DISABLED: _ClassVar[BranchServerStatus]
    BRANCH_SERVER_STATUS_NOT_CONFIGURED: _ClassVar[BranchServerStatus]
    BRANCH_SERVER_STATUS_ERROR_COMMUNICATING: _ClassVar[BranchServerStatus]

DEPLOYMENT_BUILD_STATUS_UNSPECIFIED: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_UNKNOWN: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_PENDING: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_QUEUED: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_WORKING: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_SUCCESS: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_FAILURE: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_INTERNAL_ERROR: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_TIMEOUT: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_CANCELLED: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_EXPIRED: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_BOOT_ERRORS: DeploymentBuildStatus
CUSTOMER_VECTOR_AGGREGATOR_STATSD_PROTOCOL_UNSPECIFIED: CustomerVectorAggregatorStatsdProtocol
CUSTOMER_VECTOR_AGGREGATOR_STATSD_PROTOCOL_UDP: CustomerVectorAggregatorStatsdProtocol
CUSTOMER_VECTOR_AGGREGATOR_STATSD_PROTOCOL_TCP: CustomerVectorAggregatorStatsdProtocol
TELEMETRY_COLLECTOR_TOLERATION_MODE_UNSPECIFIED: TelemetryCollectorTolerationMode
TELEMETRY_COLLECTOR_TOLERATION_MODE_NO_SCHEDULE_ALL: TelemetryCollectorTolerationMode
TELEMETRY_COLLECTOR_TOLERATION_MODE_NO_SCHEDULE_ALL_EXCEPT_NO_NETWORK: TelemetryCollectorTolerationMode
OTEL_COLLECTOR_IMAGE_UNSPECIFIED: OtelCollectorImage
OTEL_COLLECTOR_IMAGE_UPSTREAM_CONTRIB: OtelCollectorImage
OTEL_COLLECTOR_IMAGE_CHALK_SHARED: OtelCollectorImage
TELEMETRY_RUNTIME_UNSPECIFIED: TelemetryRuntime
TELEMETRY_RUNTIME_OTEL: TelemetryRuntime
TELEMETRY_RUNTIME_VECTOR: TelemetryRuntime
TELEMETRY_PROMETHEUS_COLLECTION_RUNTIME_UNSPECIFIED: TelemetryPrometheusCollectionRuntime
TELEMETRY_PROMETHEUS_COLLECTION_RUNTIME_VECTOR_COLLECTOR: TelemetryPrometheusCollectionRuntime
TELEMETRY_PROMETHEUS_COLLECTION_RUNTIME_VICTORIA_METRICS: TelemetryPrometheusCollectionRuntime
METRIC_EXPORT_DESTINATION_FORMAT_UNSPECIFIED: MetricExportDestinationFormat
METRIC_EXPORT_DESTINATION_FORMAT_PROMETHEUS_REMOTE_WRITE: MetricExportDestinationFormat
METRIC_EXPORT_DESTINATION_FORMAT_STATSD: MetricExportDestinationFormat
VECTOR_CLUSTER_METRICS_SINK_MODE_UNSPECIFIED: VectorClusterMetricsSinkMode
VECTOR_CLUSTER_METRICS_SINK_MODE_DISABLED: VectorClusterMetricsSinkMode
VECTOR_CLUSTER_METRICS_SINK_MODE_SHADOW: VectorClusterMetricsSinkMode
VECTOR_CLUSTER_METRICS_SINK_MODE_WRITE: VectorClusterMetricsSinkMode
VECTOR_CLUSTER_METRICS_SHADOW_OUTPUT_UNSPECIFIED: VectorClusterMetricsShadowOutput
VECTOR_CLUSTER_METRICS_SHADOW_OUTPUT_STDOUT: VectorClusterMetricsShadowOutput
VECTOR_CLUSTER_METRICS_SHADOW_OUTPUT_TABLE: VectorClusterMetricsShadowOutput
PERFETTO_TRIGGER_UNSPECIFIED: PerfettoTrigger
PERFETTO_TRIGGER_TIME_INTERVAL: PerfettoTrigger
PERFETTO_TRIGGER_HTTP: PerfettoTrigger
NETWORK_INSPECTOR_TRIGGER_UNSPECIFIED: NetworkInspectorTrigger
NETWORK_INSPECTOR_TRIGGER_START_ON_LAUNCH: NetworkInspectorTrigger
NETWORK_INSPECTOR_TRIGGER_HTTP: NetworkInspectorTrigger
BRANCH_SCALING_STATE_UNSPECIFIED: BranchScalingState
BRANCH_SCALING_STATE_SUCCESS: BranchScalingState
BRANCH_SCALING_STATE_IN_PROGRESS: BranchScalingState
BRANCH_SERVER_STATUS_UNSPECIFIED: BranchServerStatus
BRANCH_SERVER_STATUS_READY: BranchServerStatus
BRANCH_SERVER_STATUS_STARTING: BranchServerStatus
BRANCH_SERVER_STATUS_STOPPING: BranchServerStatus
BRANCH_SERVER_STATUS_PAUSED: BranchServerStatus
BRANCH_SERVER_STATUS_OFFLINE: BranchServerStatus
BRANCH_SERVER_STATUS_DISABLED: BranchServerStatus
BRANCH_SERVER_STATUS_NOT_CONFIGURED: BranchServerStatus
BRANCH_SERVER_STATUS_ERROR_COMMUNICATING: BranchServerStatus

class ActivateDeploymentTarget(_message.Message):
    __slots__ = ("service_kind", "resource_group_name")
    SERVICE_KIND_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    service_kind: str
    resource_group_name: str
    def __init__(self, service_kind: _Optional[str] = ..., resource_group_name: _Optional[str] = ...) -> None: ...

class ActivateDeploymentRequest(_message.Message):
    __slots__ = ("existing_deployment_id", "targets")
    EXISTING_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TARGETS_FIELD_NUMBER: _ClassVar[int]
    existing_deployment_id: str
    targets: _containers.RepeatedCompositeFieldContainer[ActivateDeploymentTarget]
    def __init__(
        self,
        existing_deployment_id: _Optional[str] = ...,
        targets: _Optional[_Iterable[_Union[ActivateDeploymentTarget, _Mapping]]] = ...,
    ) -> None: ...

class ActivateDeploymentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class IndexDeploymentRequest(_message.Message):
    __slots__ = (
        "existing_deployment_id",
        "dry_run",
        "shadow_force_venv_rebuild",
        "shadow_skip_handle_conversion_errors",
        "shadow",
        "shadow_run_id",
    )
    EXISTING_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    SHADOW_FORCE_VENV_REBUILD_FIELD_NUMBER: _ClassVar[int]
    SHADOW_SKIP_HANDLE_CONVERSION_ERRORS_FIELD_NUMBER: _ClassVar[int]
    SHADOW_FIELD_NUMBER: _ClassVar[int]
    SHADOW_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    existing_deployment_id: str
    dry_run: bool
    shadow_force_venv_rebuild: bool
    shadow_skip_handle_conversion_errors: bool
    shadow: bool
    shadow_run_id: str
    def __init__(
        self,
        existing_deployment_id: _Optional[str] = ...,
        dry_run: bool = ...,
        shadow_force_venv_rebuild: bool = ...,
        shadow_skip_handle_conversion_errors: bool = ...,
        shadow: bool = ...,
        shadow_run_id: _Optional[str] = ...,
    ) -> None: ...

class IndexDeploymentResponse(_message.Message):
    __slots__ = ("build_id",)
    BUILD_ID_FIELD_NUMBER: _ClassVar[int]
    build_id: str
    def __init__(self, build_id: _Optional[str] = ...) -> None: ...

class ValidateNamedQueriesRequest(_message.Message):
    __slots__ = ("existing_deployment_id", "shadow_run_id")
    EXISTING_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    SHADOW_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    existing_deployment_id: str
    shadow_run_id: str
    def __init__(self, existing_deployment_id: _Optional[str] = ..., shadow_run_id: _Optional[str] = ...) -> None: ...

class ValidateNamedQueriesResponse(_message.Message):
    __slots__ = ("job_id",)
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class RunPostIndexValidationRequest(_message.Message):
    __slots__ = ("existing_deployment_id", "shadow_run_id", "run_indexing", "validate_named_queries")
    EXISTING_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    SHADOW_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_INDEXING_FIELD_NUMBER: _ClassVar[int]
    VALIDATE_NAMED_QUERIES_FIELD_NUMBER: _ClassVar[int]
    existing_deployment_id: str
    shadow_run_id: str
    run_indexing: bool
    validate_named_queries: bool
    def __init__(
        self,
        existing_deployment_id: _Optional[str] = ...,
        shadow_run_id: _Optional[str] = ...,
        run_indexing: bool = ...,
        validate_named_queries: bool = ...,
    ) -> None: ...

class RunPostIndexValidationResponse(_message.Message):
    __slots__ = ("job_id",)
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class StartShadowBuildFromDeploymentRequest(_message.Message):
    __slots__ = (
        "existing_deployment_id",
        "force_venv_rebuild",
        "skip_handle_conversion_errors",
        "validate_named_queries_after_build",
    )
    EXISTING_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    FORCE_VENV_REBUILD_FIELD_NUMBER: _ClassVar[int]
    SKIP_HANDLE_CONVERSION_ERRORS_FIELD_NUMBER: _ClassVar[int]
    VALIDATE_NAMED_QUERIES_AFTER_BUILD_FIELD_NUMBER: _ClassVar[int]
    existing_deployment_id: str
    force_venv_rebuild: bool
    skip_handle_conversion_errors: bool
    validate_named_queries_after_build: bool
    def __init__(
        self,
        existing_deployment_id: _Optional[str] = ...,
        force_venv_rebuild: bool = ...,
        skip_handle_conversion_errors: bool = ...,
        validate_named_queries_after_build: bool = ...,
    ) -> None: ...

class StartShadowBuildFromDeploymentResponse(_message.Message):
    __slots__ = ("build_id",)
    BUILD_ID_FIELD_NUMBER: _ClassVar[int]
    build_id: str
    def __init__(self, build_id: _Optional[str] = ...) -> None: ...

class DeployKubeComponentsRequest(_message.Message):
    __slots__ = ("existing_deployment_id", "targets")
    EXISTING_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TARGETS_FIELD_NUMBER: _ClassVar[int]
    existing_deployment_id: str
    targets: _containers.RepeatedCompositeFieldContainer[ActivateDeploymentTarget]
    def __init__(
        self,
        existing_deployment_id: _Optional[str] = ...,
        targets: _Optional[_Iterable[_Union[ActivateDeploymentTarget, _Mapping]]] = ...,
    ) -> None: ...

class DeployKubeComponentsResponse(_message.Message):
    __slots__ = ("nonfatal_errors",)
    NONFATAL_ERRORS_FIELD_NUMBER: _ClassVar[int]
    nonfatal_errors: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, nonfatal_errors: _Optional[_Iterable[str]] = ...) -> None: ...

class RebuildDeploymentRequest(_message.Message):
    __slots__ = (
        "existing_deployment_id",
        "new_image_tag",
        "base_image_override",
        "enable_profiling",
        "build_profile",
        "force_rebuild_dockerfile",
        "branch_name",
        "platform_version",
    )
    EXISTING_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_IMAGE_TAG_FIELD_NUMBER: _ClassVar[int]
    BASE_IMAGE_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    ENABLE_PROFILING_FIELD_NUMBER: _ClassVar[int]
    BUILD_PROFILE_FIELD_NUMBER: _ClassVar[int]
    FORCE_REBUILD_DOCKERFILE_FIELD_NUMBER: _ClassVar[int]
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_VERSION_FIELD_NUMBER: _ClassVar[int]
    existing_deployment_id: str
    new_image_tag: str
    base_image_override: str
    enable_profiling: bool
    build_profile: _environment_pb2.DeploymentBuildProfile
    force_rebuild_dockerfile: bool
    branch_name: str
    platform_version: str
    def __init__(
        self,
        existing_deployment_id: _Optional[str] = ...,
        new_image_tag: _Optional[str] = ...,
        base_image_override: _Optional[str] = ...,
        enable_profiling: bool = ...,
        build_profile: _Optional[_Union[_environment_pb2.DeploymentBuildProfile, str]] = ...,
        force_rebuild_dockerfile: bool = ...,
        branch_name: _Optional[str] = ...,
        platform_version: _Optional[str] = ...,
    ) -> None: ...

class RebuildDeploymentResponse(_message.Message):
    __slots__ = ("build_id",)
    BUILD_ID_FIELD_NUMBER: _ClassVar[int]
    build_id: str
    def __init__(self, build_id: _Optional[str] = ...) -> None: ...

class RedeployDeploymentRequest(_message.Message):
    __slots__ = (
        "existing_deployment_id",
        "enable_profiling",
        "deployment_tags",
        "base_image_override",
        "override_graph",
        "build_profile",
        "graph_mutations",
        "customer_metadata",
        "display_description",
        "force_rebuild_dockerfile",
        "build_options",
        "platform_version",
    )
    class CustomerMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class BuildOptionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    EXISTING_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ENABLE_PROFILING_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_TAGS_FIELD_NUMBER: _ClassVar[int]
    BASE_IMAGE_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_GRAPH_FIELD_NUMBER: _ClassVar[int]
    BUILD_PROFILE_FIELD_NUMBER: _ClassVar[int]
    GRAPH_MUTATIONS_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_METADATA_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FORCE_REBUILD_DOCKERFILE_FIELD_NUMBER: _ClassVar[int]
    BUILD_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_VERSION_FIELD_NUMBER: _ClassVar[int]
    existing_deployment_id: str
    enable_profiling: bool
    deployment_tags: _containers.RepeatedScalarFieldContainer[str]
    base_image_override: str
    override_graph: _graph_pb2.Graph
    build_profile: _environment_pb2.DeploymentBuildProfile
    graph_mutations: _containers.RepeatedCompositeFieldContainer[_graph_pb2_1.GraphMutation]
    customer_metadata: _containers.ScalarMap[str, str]
    display_description: str
    force_rebuild_dockerfile: bool
    build_options: _containers.ScalarMap[str, str]
    platform_version: str
    def __init__(
        self,
        existing_deployment_id: _Optional[str] = ...,
        enable_profiling: bool = ...,
        deployment_tags: _Optional[_Iterable[str]] = ...,
        base_image_override: _Optional[str] = ...,
        override_graph: _Optional[_Union[_graph_pb2.Graph, _Mapping]] = ...,
        build_profile: _Optional[_Union[_environment_pb2.DeploymentBuildProfile, str]] = ...,
        graph_mutations: _Optional[_Iterable[_Union[_graph_pb2_1.GraphMutation, _Mapping]]] = ...,
        customer_metadata: _Optional[_Mapping[str, str]] = ...,
        display_description: _Optional[str] = ...,
        force_rebuild_dockerfile: bool = ...,
        build_options: _Optional[_Mapping[str, str]] = ...,
        platform_version: _Optional[str] = ...,
    ) -> None: ...

class RedeployDeploymentResponse(_message.Message):
    __slots__ = ("build_id", "deployment_id")
    BUILD_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    build_id: str
    deployment_id: str
    def __init__(self, build_id: _Optional[str] = ..., deployment_id: _Optional[str] = ...) -> None: ...

class UploadSourceRequest(_message.Message):
    __slots__ = (
        "deployment_id",
        "archive",
        "no_promote",
        "dependency_hash",
        "base_image_override",
        "use_grpc",
        "enable_profiling",
        "build_profile",
        "force_rebuild_dockerfile",
    )
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ARCHIVE_FIELD_NUMBER: _ClassVar[int]
    NO_PROMOTE_FIELD_NUMBER: _ClassVar[int]
    DEPENDENCY_HASH_FIELD_NUMBER: _ClassVar[int]
    BASE_IMAGE_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    USE_GRPC_FIELD_NUMBER: _ClassVar[int]
    ENABLE_PROFILING_FIELD_NUMBER: _ClassVar[int]
    BUILD_PROFILE_FIELD_NUMBER: _ClassVar[int]
    FORCE_REBUILD_DOCKERFILE_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    archive: bytes
    no_promote: bool
    dependency_hash: str
    base_image_override: str
    use_grpc: bool
    enable_profiling: bool
    build_profile: _environment_pb2.DeploymentBuildProfile
    force_rebuild_dockerfile: bool
    def __init__(
        self,
        deployment_id: _Optional[str] = ...,
        archive: _Optional[bytes] = ...,
        no_promote: bool = ...,
        dependency_hash: _Optional[str] = ...,
        base_image_override: _Optional[str] = ...,
        use_grpc: bool = ...,
        enable_profiling: bool = ...,
        build_profile: _Optional[_Union[_environment_pb2.DeploymentBuildProfile, str]] = ...,
        force_rebuild_dockerfile: bool = ...,
    ) -> None: ...

class UploadSourceResponse(_message.Message):
    __slots__ = ("status", "progress_url", "warnings")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_URL_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    status: str
    progress_url: str
    warnings: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        status: _Optional[str] = ...,
        progress_url: _Optional[str] = ...,
        warnings: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class PrepareDeploymentRequest(_message.Message):
    __slots__ = (
        "git_branch",
        "git_commit",
        "git_pr",
        "git_author",
        "git_tag",
        "branch",
        "requirements",
        "customer_deployment_tags",
        "project_settings",
        "customer_metadata",
        "display_description",
        "archive",
        "no_promote",
        "dependency_hash",
        "base_image_override",
        "use_grpc",
        "enable_profiling",
        "build_profile",
        "build_options",
    )
    class CustomerMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class BuildOptionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    GIT_BRANCH_FIELD_NUMBER: _ClassVar[int]
    GIT_COMMIT_FIELD_NUMBER: _ClassVar[int]
    GIT_PR_FIELD_NUMBER: _ClassVar[int]
    GIT_AUTHOR_FIELD_NUMBER: _ClassVar[int]
    GIT_TAG_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_DEPLOYMENT_TAGS_FIELD_NUMBER: _ClassVar[int]
    PROJECT_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_METADATA_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ARCHIVE_FIELD_NUMBER: _ClassVar[int]
    NO_PROMOTE_FIELD_NUMBER: _ClassVar[int]
    DEPENDENCY_HASH_FIELD_NUMBER: _ClassVar[int]
    BASE_IMAGE_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    USE_GRPC_FIELD_NUMBER: _ClassVar[int]
    ENABLE_PROFILING_FIELD_NUMBER: _ClassVar[int]
    BUILD_PROFILE_FIELD_NUMBER: _ClassVar[int]
    BUILD_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    git_branch: str
    git_commit: str
    git_pr: str
    git_author: str
    git_tag: str
    branch: str
    requirements: _containers.RepeatedCompositeFieldContainer[RequirementsFile]
    customer_deployment_tags: _containers.RepeatedScalarFieldContainer[str]
    project_settings: _export_pb2.ProjectSettings
    customer_metadata: _containers.ScalarMap[str, str]
    display_description: str
    archive: bytes
    no_promote: bool
    dependency_hash: str
    base_image_override: str
    use_grpc: bool
    enable_profiling: bool
    build_profile: _environment_pb2.DeploymentBuildProfile
    build_options: _containers.ScalarMap[str, str]
    def __init__(
        self,
        git_branch: _Optional[str] = ...,
        git_commit: _Optional[str] = ...,
        git_pr: _Optional[str] = ...,
        git_author: _Optional[str] = ...,
        git_tag: _Optional[str] = ...,
        branch: _Optional[str] = ...,
        requirements: _Optional[_Iterable[_Union[RequirementsFile, _Mapping]]] = ...,
        customer_deployment_tags: _Optional[_Iterable[str]] = ...,
        project_settings: _Optional[_Union[_export_pb2.ProjectSettings, _Mapping]] = ...,
        customer_metadata: _Optional[_Mapping[str, str]] = ...,
        display_description: _Optional[str] = ...,
        archive: _Optional[bytes] = ...,
        no_promote: bool = ...,
        dependency_hash: _Optional[str] = ...,
        base_image_override: _Optional[str] = ...,
        use_grpc: bool = ...,
        enable_profiling: bool = ...,
        build_profile: _Optional[_Union[_environment_pb2.DeploymentBuildProfile, str]] = ...,
        build_options: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class PrepareDeploymentResponse(_message.Message):
    __slots__ = ("deployment_id", "status", "progress_url")
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_URL_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    status: str
    progress_url: str
    def __init__(
        self, deployment_id: _Optional[str] = ..., status: _Optional[str] = ..., progress_url: _Optional[str] = ...
    ) -> None: ...

class LintSourceRequest(_message.Message):
    __slots__ = ("archive", "use_branch_server")
    ARCHIVE_FIELD_NUMBER: _ClassVar[int]
    USE_BRANCH_SERVER_FIELD_NUMBER: _ClassVar[int]
    archive: bytes
    use_branch_server: bool
    def __init__(self, archive: _Optional[bytes] = ..., use_branch_server: bool = ...) -> None: ...

class LintSourceResponse(_message.Message):
    __slots__ = ("graph", "lsp")
    GRAPH_FIELD_NUMBER: _ClassVar[int]
    LSP_FIELD_NUMBER: _ClassVar[int]
    graph: _graph_pb2.Graph
    lsp: _lsp_pb2.LSP
    def __init__(
        self,
        graph: _Optional[_Union[_graph_pb2.Graph, _Mapping]] = ...,
        lsp: _Optional[_Union[_lsp_pb2.LSP, _Mapping]] = ...,
    ) -> None: ...

class GetDeploymentStepsRequest(_message.Message):
    __slots__ = ("deployment_id",)
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    def __init__(self, deployment_id: _Optional[str] = ...) -> None: ...

class DeploymentBuildStep(_message.Message):
    __slots__ = ("id", "display_name", "status", "start_time", "end_time")
    ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    id: str
    display_name: str
    status: DeploymentBuildStatus
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        display_name: _Optional[str] = ...,
        status: _Optional[_Union[DeploymentBuildStatus, str]] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GetDeploymentStepsResponse(_message.Message):
    __slots__ = ("steps", "deployment", "perfetto_trace_url")
    STEPS_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    PERFETTO_TRACE_URL_FIELD_NUMBER: _ClassVar[int]
    steps: _containers.RepeatedCompositeFieldContainer[DeploymentBuildStep]
    deployment: _deployment_pb2.Deployment
    perfetto_trace_url: str
    def __init__(
        self,
        steps: _Optional[_Iterable[_Union[DeploymentBuildStep, _Mapping]]] = ...,
        deployment: _Optional[_Union[_deployment_pb2.Deployment, _Mapping]] = ...,
        perfetto_trace_url: _Optional[str] = ...,
    ) -> None: ...

class GetDeploymentLogsRequest(_message.Message):
    __slots__ = ("deployment_id",)
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    def __init__(self, deployment_id: _Optional[str] = ...) -> None: ...

class GetDeploymentLogsResponse(_message.Message):
    __slots__ = ("logs",)
    LOGS_FIELD_NUMBER: _ClassVar[int]
    logs: _containers.RepeatedCompositeFieldContainer[_log_pb2.LogEntry]
    def __init__(self, logs: _Optional[_Iterable[_Union[_log_pb2.LogEntry, _Mapping]]] = ...) -> None: ...

class GetDeploymentDependenciesRequest(_message.Message):
    __slots__ = ("deployment_id",)
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    def __init__(self, deployment_id: _Optional[str] = ...) -> None: ...

class GetDeploymentDependenciesResponse(_message.Message):
    __slots__ = (
        "runtime",
        "requirements_file",
        "requirements_contents",
        "platform_version",
        "profiling_mode",
        "desired_engine_base_image",
        "final_engine_image",
        "build_profile",
        "source_dependency_hash",
        "dependency_hash",
        "target_tag",
    )
    RUNTIME_FIELD_NUMBER: _ClassVar[int]
    REQUIREMENTS_FILE_FIELD_NUMBER: _ClassVar[int]
    REQUIREMENTS_CONTENTS_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_VERSION_FIELD_NUMBER: _ClassVar[int]
    PROFILING_MODE_FIELD_NUMBER: _ClassVar[int]
    DESIRED_ENGINE_BASE_IMAGE_FIELD_NUMBER: _ClassVar[int]
    FINAL_ENGINE_IMAGE_FIELD_NUMBER: _ClassVar[int]
    BUILD_PROFILE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_DEPENDENCY_HASH_FIELD_NUMBER: _ClassVar[int]
    DEPENDENCY_HASH_FIELD_NUMBER: _ClassVar[int]
    TARGET_TAG_FIELD_NUMBER: _ClassVar[int]
    runtime: str
    requirements_file: str
    requirements_contents: str
    platform_version: str
    profiling_mode: str
    desired_engine_base_image: str
    final_engine_image: str
    build_profile: _environment_pb2.DeploymentBuildProfile
    source_dependency_hash: str
    dependency_hash: str
    target_tag: str
    def __init__(
        self,
        runtime: _Optional[str] = ...,
        requirements_file: _Optional[str] = ...,
        requirements_contents: _Optional[str] = ...,
        platform_version: _Optional[str] = ...,
        profiling_mode: _Optional[str] = ...,
        desired_engine_base_image: _Optional[str] = ...,
        final_engine_image: _Optional[str] = ...,
        build_profile: _Optional[_Union[_environment_pb2.DeploymentBuildProfile, str]] = ...,
        source_dependency_hash: _Optional[str] = ...,
        dependency_hash: _Optional[str] = ...,
        target_tag: _Optional[str] = ...,
    ) -> None: ...

class ResolveEngineBaseImageRequest(_message.Message):
    __slots__ = ("environment_id",)
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    def __init__(self, environment_id: _Optional[str] = ...) -> None: ...

class ResolveEngineBaseImageResponse(_message.Message):
    __slots__ = (
        "default_base_image",
        "resolved_structured_tag",
        "final_base_image",
        "digest",
        "git_commit_sha",
        "resolve_flag_enabled",
    )
    DEFAULT_BASE_IMAGE_FIELD_NUMBER: _ClassVar[int]
    RESOLVED_STRUCTURED_TAG_FIELD_NUMBER: _ClassVar[int]
    FINAL_BASE_IMAGE_FIELD_NUMBER: _ClassVar[int]
    DIGEST_FIELD_NUMBER: _ClassVar[int]
    GIT_COMMIT_SHA_FIELD_NUMBER: _ClassVar[int]
    RESOLVE_FLAG_ENABLED_FIELD_NUMBER: _ClassVar[int]
    default_base_image: str
    resolved_structured_tag: str
    final_base_image: str
    digest: str
    git_commit_sha: str
    resolve_flag_enabled: bool
    def __init__(
        self,
        default_base_image: _Optional[str] = ...,
        resolved_structured_tag: _Optional[str] = ...,
        final_base_image: _Optional[str] = ...,
        digest: _Optional[str] = ...,
        git_commit_sha: _Optional[str] = ...,
        resolve_flag_enabled: bool = ...,
    ) -> None: ...

class GetClusterTimescaleDBRequest(_message.Message):
    __slots__ = ("environment_id", "cluster_timescale_id")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_TIMESCALE_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    cluster_timescale_id: str
    def __init__(self, environment_id: _Optional[str] = ..., cluster_timescale_id: _Optional[str] = ...) -> None: ...

class GetClusterTimescaleDBResponse(_message.Message):
    __slots__ = ("id", "specs_string", "created_at", "updated_at", "specs")
    ID_FIELD_NUMBER: _ClassVar[int]
    SPECS_STRING_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    SPECS_FIELD_NUMBER: _ClassVar[int]
    id: str
    specs_string: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    specs: ClusterTimescaleSpecs
    def __init__(
        self,
        id: _Optional[str] = ...,
        specs_string: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        specs: _Optional[_Union[ClusterTimescaleSpecs, _Mapping]] = ...,
    ) -> None: ...

class ListClusterTimescaleDBsRequest(_message.Message):
    __slots__ = ("cluster_id",)
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class ListClusterTimescaleDBsResponse(_message.Message):
    __slots__ = ("cluster_timescale_dbs",)
    CLUSTER_TIMESCALE_DBS_FIELD_NUMBER: _ClassVar[int]
    cluster_timescale_dbs: _containers.RepeatedCompositeFieldContainer[GetClusterTimescaleDBResponse]
    def __init__(
        self, cluster_timescale_dbs: _Optional[_Iterable[_Union[GetClusterTimescaleDBResponse, _Mapping]]] = ...
    ) -> None: ...

class GetClusterGatewayRequest(_message.Message):
    __slots__ = ("environment_id", "id")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    id: str
    def __init__(self, environment_id: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class GetClusterGatewayResponse(_message.Message):
    __slots__ = ("id", "specs_string", "created_at", "updated_at", "specs", "kube_cluster_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    SPECS_STRING_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    SPECS_FIELD_NUMBER: _ClassVar[int]
    KUBE_CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    specs_string: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    specs: EnvoyGatewaySpecs
    kube_cluster_id: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        specs_string: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        specs: _Optional[_Union[EnvoyGatewaySpecs, _Mapping]] = ...,
        kube_cluster_id: _Optional[str] = ...,
    ) -> None: ...

class ListClusterGatewaysRequest(_message.Message):
    __slots__ = ("cluster_id",)
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class ListClusterGatewaysResponse(_message.Message):
    __slots__ = ("gateways",)
    GATEWAYS_FIELD_NUMBER: _ClassVar[int]
    gateways: _containers.RepeatedCompositeFieldContainer[GetClusterGatewayResponse]
    def __init__(self, gateways: _Optional[_Iterable[_Union[GetClusterGatewayResponse, _Mapping]]] = ...) -> None: ...

class GetClusterGatewayDefaultRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetClusterGatewayDefaultResponse(_message.Message):
    __slots__ = ("specs",)
    SPECS_FIELD_NUMBER: _ClassVar[int]
    specs: EnvoyGatewaySpecs
    def __init__(self, specs: _Optional[_Union[EnvoyGatewaySpecs, _Mapping]] = ...) -> None: ...

class BackgroundPersistence(_message.Message):
    __slots__ = ("id", "kind", "specs_string", "created_at", "updated_at", "specs", "kube_cluster_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    SPECS_STRING_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    SPECS_FIELD_NUMBER: _ClassVar[int]
    KUBE_CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    kind: str
    specs_string: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    specs: BackgroundPersistenceDeploymentSpecs
    kube_cluster_id: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        kind: _Optional[str] = ...,
        specs_string: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        specs: _Optional[_Union[BackgroundPersistenceDeploymentSpecs, _Mapping]] = ...,
        kube_cluster_id: _Optional[str] = ...,
    ) -> None: ...

class GetClusterBackgroundPersistenceRequest(_message.Message):
    __slots__ = ("environment_id", "id")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    id: str
    def __init__(self, environment_id: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class GetClusterBackgroundPersistenceResponse(_message.Message):
    __slots__ = ("background_persistence",)
    BACKGROUND_PERSISTENCE_FIELD_NUMBER: _ClassVar[int]
    background_persistence: BackgroundPersistence
    def __init__(self, background_persistence: _Optional[_Union[BackgroundPersistence, _Mapping]] = ...) -> None: ...

class ListClusterBackgroundPersistenceDeploymentsRequest(_message.Message):
    __slots__ = ("cluster_id",)
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class ListClusterBackgroundPersistenceDeploymentsResponse(_message.Message):
    __slots__ = ("background_persistence_deployments",)
    BACKGROUND_PERSISTENCE_DEPLOYMENTS_FIELD_NUMBER: _ClassVar[int]
    background_persistence_deployments: _containers.RepeatedCompositeFieldContainer[BackgroundPersistence]
    def __init__(
        self, background_persistence_deployments: _Optional[_Iterable[_Union[BackgroundPersistence, _Mapping]]] = ...
    ) -> None: ...

class CreateClusterTimescaleDBRequest(_message.Message):
    __slots__ = ("environment_id", "environment_ids", "specs_string", "specs")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_IDS_FIELD_NUMBER: _ClassVar[int]
    SPECS_STRING_FIELD_NUMBER: _ClassVar[int]
    SPECS_FIELD_NUMBER: _ClassVar[int]
    environment_id: _containers.RepeatedScalarFieldContainer[str]
    environment_ids: _containers.RepeatedScalarFieldContainer[str]
    specs_string: str
    specs: ClusterTimescaleSpecs
    def __init__(
        self,
        environment_id: _Optional[_Iterable[str]] = ...,
        environment_ids: _Optional[_Iterable[str]] = ...,
        specs_string: _Optional[str] = ...,
        specs: _Optional[_Union[ClusterTimescaleSpecs, _Mapping]] = ...,
    ) -> None: ...

class DeleteClusterTimescaleDBRequest(_message.Message):
    __slots__ = ("cluster_timescale_id",)
    CLUSTER_TIMESCALE_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_timescale_id: str
    def __init__(self, cluster_timescale_id: _Optional[str] = ...) -> None: ...

class DeleteClusterTimescaleDBResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetClusterTimescaleDefaultRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetClusterTimescaleDefaultResponse(_message.Message):
    __slots__ = ("specs",)
    SPECS_FIELD_NUMBER: _ClassVar[int]
    specs: ClusterTimescaleSpecs
    def __init__(self, specs: _Optional[_Union[ClusterTimescaleSpecs, _Mapping]] = ...) -> None: ...

class KubeResourceConfig(_message.Message):
    __slots__ = ("cpu", "memory", "ephemeral_storage", "storage")
    CPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    EPHEMERAL_STORAGE_FIELD_NUMBER: _ClassVar[int]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    cpu: str
    memory: str
    ephemeral_storage: str
    storage: str
    def __init__(
        self,
        cpu: _Optional[str] = ...,
        memory: _Optional[str] = ...,
        ephemeral_storage: _Optional[str] = ...,
        storage: _Optional[str] = ...,
    ) -> None: ...

class KubePersistentVolumeClaim(_message.Message):
    __slots__ = ("storage", "storage_class_name")
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    STORAGE_CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    storage: str
    storage_class_name: str
    def __init__(self, storage: _Optional[str] = ..., storage_class_name: _Optional[str] = ...) -> None: ...

class ClusterTimescaleSpecs(_message.Message):
    __slots__ = (
        "timescale_image",
        "database_name",
        "database_replicas",
        "storage",
        "storage_class",
        "namespace",
        "request",
        "limit",
        "connection_pool_replicas",
        "connection_pool_max_connections",
        "connection_pool_size",
        "connection_pool_mode",
        "backup_bucket",
        "backup_iam_role_arn",
        "secret_name",
        "internal",
        "service_type",
        "postgres_parameters",
        "include_chalk_node_selector",
        "backup_gcp_service_account",
        "instance_type",
        "nodepool",
        "node_selector",
        "dns_hostname",
        "bootstrap_cloud_resources",
        "suspended",
        "ip_allowlist",
        "gateway_port",
        "gateway_id",
        "shared_preload_libraries",
        "require_infrastructure_nodepool",
        "pgbouncer_parameters",
    )
    class PostgresParametersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class NodeSelectorEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class PgbouncerParametersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    TIMESCALE_IMAGE_FIELD_NUMBER: _ClassVar[int]
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    DATABASE_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    STORAGE_CLASS_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_POOL_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_POOL_MAX_CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_POOL_SIZE_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_POOL_MODE_FIELD_NUMBER: _ClassVar[int]
    BACKUP_BUCKET_FIELD_NUMBER: _ClassVar[int]
    BACKUP_IAM_ROLE_ARN_FIELD_NUMBER: _ClassVar[int]
    SECRET_NAME_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_FIELD_NUMBER: _ClassVar[int]
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    POSTGRES_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_CHALK_NODE_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    BACKUP_GCP_SERVICE_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    NODE_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    DNS_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    BOOTSTRAP_CLOUD_RESOURCES_FIELD_NUMBER: _ClassVar[int]
    SUSPENDED_FIELD_NUMBER: _ClassVar[int]
    IP_ALLOWLIST_FIELD_NUMBER: _ClassVar[int]
    GATEWAY_PORT_FIELD_NUMBER: _ClassVar[int]
    GATEWAY_ID_FIELD_NUMBER: _ClassVar[int]
    SHARED_PRELOAD_LIBRARIES_FIELD_NUMBER: _ClassVar[int]
    REQUIRE_INFRASTRUCTURE_NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    PGBOUNCER_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    timescale_image: str
    database_name: str
    database_replicas: int
    storage: str
    storage_class: str
    namespace: str
    request: KubeResourceConfig
    limit: KubeResourceConfig
    connection_pool_replicas: int
    connection_pool_max_connections: str
    connection_pool_size: str
    connection_pool_mode: str
    backup_bucket: str
    backup_iam_role_arn: str
    secret_name: str
    internal: bool
    service_type: str
    postgres_parameters: _containers.ScalarMap[str, str]
    include_chalk_node_selector: bool
    backup_gcp_service_account: str
    instance_type: str
    nodepool: str
    node_selector: _containers.ScalarMap[str, str]
    dns_hostname: str
    bootstrap_cloud_resources: bool
    suspended: bool
    ip_allowlist: _containers.RepeatedScalarFieldContainer[str]
    gateway_port: int
    gateway_id: str
    shared_preload_libraries: _containers.RepeatedScalarFieldContainer[str]
    require_infrastructure_nodepool: bool
    pgbouncer_parameters: _containers.ScalarMap[str, str]
    def __init__(
        self,
        timescale_image: _Optional[str] = ...,
        database_name: _Optional[str] = ...,
        database_replicas: _Optional[int] = ...,
        storage: _Optional[str] = ...,
        storage_class: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        request: _Optional[_Union[KubeResourceConfig, _Mapping]] = ...,
        limit: _Optional[_Union[KubeResourceConfig, _Mapping]] = ...,
        connection_pool_replicas: _Optional[int] = ...,
        connection_pool_max_connections: _Optional[str] = ...,
        connection_pool_size: _Optional[str] = ...,
        connection_pool_mode: _Optional[str] = ...,
        backup_bucket: _Optional[str] = ...,
        backup_iam_role_arn: _Optional[str] = ...,
        secret_name: _Optional[str] = ...,
        internal: bool = ...,
        service_type: _Optional[str] = ...,
        postgres_parameters: _Optional[_Mapping[str, str]] = ...,
        include_chalk_node_selector: bool = ...,
        backup_gcp_service_account: _Optional[str] = ...,
        instance_type: _Optional[str] = ...,
        nodepool: _Optional[str] = ...,
        node_selector: _Optional[_Mapping[str, str]] = ...,
        dns_hostname: _Optional[str] = ...,
        bootstrap_cloud_resources: bool = ...,
        suspended: bool = ...,
        ip_allowlist: _Optional[_Iterable[str]] = ...,
        gateway_port: _Optional[int] = ...,
        gateway_id: _Optional[str] = ...,
        shared_preload_libraries: _Optional[_Iterable[str]] = ...,
        require_infrastructure_nodepool: bool = ...,
        pgbouncer_parameters: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class CreateClusterTimescaleDBResponse(_message.Message):
    __slots__ = ("cluster_timescale_id", "specs")
    CLUSTER_TIMESCALE_ID_FIELD_NUMBER: _ClassVar[int]
    SPECS_FIELD_NUMBER: _ClassVar[int]
    cluster_timescale_id: str
    specs: ClusterTimescaleSpecs
    def __init__(
        self,
        cluster_timescale_id: _Optional[str] = ...,
        specs: _Optional[_Union[ClusterTimescaleSpecs, _Mapping]] = ...,
    ) -> None: ...

class UpdateClusterTimescaleDBRequest(_message.Message):
    __slots__ = ("cluster_timescale_id", "specs", "update_mask")
    CLUSTER_TIMESCALE_ID_FIELD_NUMBER: _ClassVar[int]
    SPECS_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    cluster_timescale_id: str
    specs: ClusterTimescaleSpecs
    update_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        cluster_timescale_id: _Optional[str] = ...,
        specs: _Optional[_Union[ClusterTimescaleSpecs, _Mapping]] = ...,
        update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class UpdateClusterTimescaleDBResponse(_message.Message):
    __slots__ = ("cluster_timescale_id", "specs")
    CLUSTER_TIMESCALE_ID_FIELD_NUMBER: _ClassVar[int]
    SPECS_FIELD_NUMBER: _ClassVar[int]
    cluster_timescale_id: str
    specs: ClusterTimescaleSpecs
    def __init__(
        self,
        cluster_timescale_id: _Optional[str] = ...,
        specs: _Optional[_Union[ClusterTimescaleSpecs, _Mapping]] = ...,
    ) -> None: ...

class MigrateClusterTimescaleDBRequest(_message.Message):
    __slots__ = ("cluster_timescale_id", "migration_image", "environment_ids")
    CLUSTER_TIMESCALE_ID_FIELD_NUMBER: _ClassVar[int]
    MIGRATION_IMAGE_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_IDS_FIELD_NUMBER: _ClassVar[int]
    cluster_timescale_id: str
    migration_image: str
    environment_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        cluster_timescale_id: _Optional[str] = ...,
        migration_image: _Optional[str] = ...,
        environment_ids: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class MigrateClusterTimescaleDBResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CreateClusterGatewayRequest(_message.Message):
    __slots__ = ("environment_id", "environment_ids", "specs_string", "specs", "kube_cluster_id", "id")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_IDS_FIELD_NUMBER: _ClassVar[int]
    SPECS_STRING_FIELD_NUMBER: _ClassVar[int]
    SPECS_FIELD_NUMBER: _ClassVar[int]
    KUBE_CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: _containers.RepeatedScalarFieldContainer[str]
    environment_ids: _containers.RepeatedScalarFieldContainer[str]
    specs_string: str
    specs: EnvoyGatewaySpecs
    kube_cluster_id: str
    id: str
    def __init__(
        self,
        environment_id: _Optional[_Iterable[str]] = ...,
        environment_ids: _Optional[_Iterable[str]] = ...,
        specs_string: _Optional[str] = ...,
        specs: _Optional[_Union[EnvoyGatewaySpecs, _Mapping]] = ...,
        kube_cluster_id: _Optional[str] = ...,
        id: _Optional[str] = ...,
    ) -> None: ...

class EnvoyGatewaySpecs(_message.Message):
    __slots__ = (
        "namespace",
        "gateway_name",
        "gateway_class_name",
        "listeners",
        "config",
        "include_chalk_node_selector",
        "ip_allowlist",
        "tls_certificate",
        "service_annotations",
        "load_balancer_class",
        "cluster_gateway_id",
        "suspended",
        "routing",
        "container_ssh_port_count",
    )
    class ServiceAnnotationsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    GATEWAY_NAME_FIELD_NUMBER: _ClassVar[int]
    GATEWAY_CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    LISTENERS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_CHALK_NODE_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    IP_ALLOWLIST_FIELD_NUMBER: _ClassVar[int]
    TLS_CERTIFICATE_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    LOAD_BALANCER_CLASS_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_GATEWAY_ID_FIELD_NUMBER: _ClassVar[int]
    SUSPENDED_FIELD_NUMBER: _ClassVar[int]
    ROUTING_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_SSH_PORT_COUNT_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    gateway_name: str
    gateway_class_name: str
    listeners: _containers.RepeatedCompositeFieldContainer[EnvoyGatewayListener]
    config: GatewayProviderConfig
    include_chalk_node_selector: bool
    ip_allowlist: _containers.RepeatedScalarFieldContainer[str]
    tls_certificate: TLSCertificateConfig
    service_annotations: _containers.ScalarMap[str, str]
    load_balancer_class: str
    cluster_gateway_id: str
    suspended: bool
    routing: str
    container_ssh_port_count: int
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        gateway_name: _Optional[str] = ...,
        gateway_class_name: _Optional[str] = ...,
        listeners: _Optional[_Iterable[_Union[EnvoyGatewayListener, _Mapping]]] = ...,
        config: _Optional[_Union[GatewayProviderConfig, _Mapping]] = ...,
        include_chalk_node_selector: bool = ...,
        ip_allowlist: _Optional[_Iterable[str]] = ...,
        tls_certificate: _Optional[_Union[TLSCertificateConfig, _Mapping]] = ...,
        service_annotations: _Optional[_Mapping[str, str]] = ...,
        load_balancer_class: _Optional[str] = ...,
        cluster_gateway_id: _Optional[str] = ...,
        suspended: bool = ...,
        routing: _Optional[str] = ...,
        container_ssh_port_count: _Optional[int] = ...,
    ) -> None: ...

class EnvoyGatewayListener(_message.Message):
    __slots__ = ("port", "protocol", "name", "allowed_routes", "hostname")
    PORT_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_ROUTES_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    port: int
    protocol: str
    name: str
    allowed_routes: EnvoyGatewayAllowedRoutes
    hostname: str
    def __init__(
        self,
        port: _Optional[int] = ...,
        protocol: _Optional[str] = ...,
        name: _Optional[str] = ...,
        allowed_routes: _Optional[_Union[EnvoyGatewayAllowedRoutes, _Mapping]] = ...,
        hostname: _Optional[str] = ...,
    ) -> None: ...

class EnvoyGatewayAllowedRoutes(_message.Message):
    __slots__ = ("namespaces",)
    NAMESPACES_FIELD_NUMBER: _ClassVar[int]
    namespaces: EnvoyGatewayAllowedNamespaces
    def __init__(self, namespaces: _Optional[_Union[EnvoyGatewayAllowedNamespaces, _Mapping]] = ...) -> None: ...

class EnvoyGatewayAllowedNamespaces(_message.Message):
    __slots__ = ()
    FROM_FIELD_NUMBER: _ClassVar[int]
    def __init__(self, **kwargs) -> None: ...

class GatewayProviderConfig(_message.Message):
    __slots__ = ("envoy", "gcp")
    ENVOY_FIELD_NUMBER: _ClassVar[int]
    GCP_FIELD_NUMBER: _ClassVar[int]
    envoy: EnvoyGatewayProviderConfig
    gcp: GCPGatewayProviderConfig
    def __init__(
        self,
        envoy: _Optional[_Union[EnvoyGatewayProviderConfig, _Mapping]] = ...,
        gcp: _Optional[_Union[GCPGatewayProviderConfig, _Mapping]] = ...,
    ) -> None: ...

class EnvoyGatewayProviderConfig(_message.Message):
    __slots__ = (
        "timeout_duration",
        "dns_hostname",
        "replicas",
        "min_available",
        "letsencrypt_cluster_issuer",
        "additional_dns_names",
        "instance_type",
        "nodepool",
        "node_selector",
        "prevent_disruption",
        "allow_colocation_with_chalk_workloads",
        "require_infrastructure_nodepool",
    )
    class NodeSelectorEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    TIMEOUT_DURATION_FIELD_NUMBER: _ClassVar[int]
    DNS_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    MIN_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    LETSENCRYPT_CLUSTER_ISSUER_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_DNS_NAMES_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    NODE_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    PREVENT_DISRUPTION_FIELD_NUMBER: _ClassVar[int]
    ALLOW_COLOCATION_WITH_CHALK_WORKLOADS_FIELD_NUMBER: _ClassVar[int]
    REQUIRE_INFRASTRUCTURE_NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    timeout_duration: str
    dns_hostname: str
    replicas: int
    min_available: int
    letsencrypt_cluster_issuer: str
    additional_dns_names: _containers.RepeatedScalarFieldContainer[str]
    instance_type: str
    nodepool: str
    node_selector: _containers.ScalarMap[str, str]
    prevent_disruption: bool
    allow_colocation_with_chalk_workloads: bool
    require_infrastructure_nodepool: bool
    def __init__(
        self,
        timeout_duration: _Optional[str] = ...,
        dns_hostname: _Optional[str] = ...,
        replicas: _Optional[int] = ...,
        min_available: _Optional[int] = ...,
        letsencrypt_cluster_issuer: _Optional[str] = ...,
        additional_dns_names: _Optional[_Iterable[str]] = ...,
        instance_type: _Optional[str] = ...,
        nodepool: _Optional[str] = ...,
        node_selector: _Optional[_Mapping[str, str]] = ...,
        prevent_disruption: bool = ...,
        allow_colocation_with_chalk_workloads: bool = ...,
        require_infrastructure_nodepool: bool = ...,
    ) -> None: ...

class GCPGatewayProviderConfig(_message.Message):
    __slots__ = ("dns_hostname",)
    DNS_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    dns_hostname: str
    def __init__(self, dns_hostname: _Optional[str] = ...) -> None: ...

class TLSCertificateConfig(_message.Message):
    __slots__ = ("manual_certificate",)
    MANUAL_CERTIFICATE_FIELD_NUMBER: _ClassVar[int]
    manual_certificate: TLSManualCertificateRef
    def __init__(self, manual_certificate: _Optional[_Union[TLSManualCertificateRef, _Mapping]] = ...) -> None: ...

class TLSManualCertificateRef(_message.Message):
    __slots__ = ("secret_name", "secret_namespace")
    SECRET_NAME_FIELD_NUMBER: _ClassVar[int]
    SECRET_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    secret_name: str
    secret_namespace: str
    def __init__(self, secret_name: _Optional[str] = ..., secret_namespace: _Optional[str] = ...) -> None: ...

class CreateClusterGatewayResponse(_message.Message):
    __slots__ = ("id", "specs")
    ID_FIELD_NUMBER: _ClassVar[int]
    SPECS_FIELD_NUMBER: _ClassVar[int]
    id: str
    specs: EnvoyGatewaySpecs
    def __init__(
        self, id: _Optional[str] = ..., specs: _Optional[_Union[EnvoyGatewaySpecs, _Mapping]] = ...
    ) -> None: ...

class CreateClusterBackgroundPersistenceRequest(_message.Message):
    __slots__ = ("environment_ids", "specs_string", "specs", "kube_cluster_id", "id")
    ENVIRONMENT_IDS_FIELD_NUMBER: _ClassVar[int]
    SPECS_STRING_FIELD_NUMBER: _ClassVar[int]
    SPECS_FIELD_NUMBER: _ClassVar[int]
    KUBE_CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    environment_ids: _containers.RepeatedScalarFieldContainer[str]
    specs_string: str
    specs: BackgroundPersistenceDeploymentSpecs
    kube_cluster_id: str
    id: str
    def __init__(
        self,
        environment_ids: _Optional[_Iterable[str]] = ...,
        specs_string: _Optional[str] = ...,
        specs: _Optional[_Union[BackgroundPersistenceDeploymentSpecs, _Mapping]] = ...,
        kube_cluster_id: _Optional[str] = ...,
        id: _Optional[str] = ...,
    ) -> None: ...

class BackgroundPersistenceCommonSpecs(_message.Message):
    __slots__ = (
        "namespace",
        "bus_writer_image_go",
        "bus_writer_image_python",
        "bus_writer_image_bswl",
        "service_account_name",
        "bus_backend",
        "secret_client",
        "bigquery_parquet_upload_subscription_id",
        "bigquery_streaming_write_subscription_id",
        "bigquery_streaming_write_topic",
        "bigquery_upload_bucket",
        "bigquery_upload_topic",
        "google_cloud_project",
        "kafka_dlq_topic",
        "metrics_bus_subscription_id",
        "metrics_bus_topic_id",
        "operation_subscription_id",
        "query_log_result_topic",
        "query_log_subscription_id",
        "result_bus_metrics_subscription_id",
        "result_bus_offline_store_subscription_id",
        "result_bus_online_store_subscription_id",
        "result_bus_topic_id",
        "usage_bus_topic_id",
        "usage_events_subscription_id",
        "bq_upload_bucket",
        "bq_upload_topic",
        "include_chalk_node_selector",
        "bus_writer_image_rust",
        "use_aws_pool_for_google_adc",
    )
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    BUS_WRITER_IMAGE_GO_FIELD_NUMBER: _ClassVar[int]
    BUS_WRITER_IMAGE_PYTHON_FIELD_NUMBER: _ClassVar[int]
    BUS_WRITER_IMAGE_BSWL_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ACCOUNT_NAME_FIELD_NUMBER: _ClassVar[int]
    BUS_BACKEND_FIELD_NUMBER: _ClassVar[int]
    SECRET_CLIENT_FIELD_NUMBER: _ClassVar[int]
    BIGQUERY_PARQUET_UPLOAD_SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    BIGQUERY_STREAMING_WRITE_SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    BIGQUERY_STREAMING_WRITE_TOPIC_FIELD_NUMBER: _ClassVar[int]
    BIGQUERY_UPLOAD_BUCKET_FIELD_NUMBER: _ClassVar[int]
    BIGQUERY_UPLOAD_TOPIC_FIELD_NUMBER: _ClassVar[int]
    GOOGLE_CLOUD_PROJECT_FIELD_NUMBER: _ClassVar[int]
    KAFKA_DLQ_TOPIC_FIELD_NUMBER: _ClassVar[int]
    METRICS_BUS_SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    METRICS_BUS_TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATION_SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_LOG_RESULT_TOPIC_FIELD_NUMBER: _ClassVar[int]
    QUERY_LOG_SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_BUS_METRICS_SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_BUS_OFFLINE_STORE_SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_BUS_ONLINE_STORE_SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_BUS_TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    USAGE_BUS_TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    USAGE_EVENTS_SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    BQ_UPLOAD_BUCKET_FIELD_NUMBER: _ClassVar[int]
    BQ_UPLOAD_TOPIC_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_CHALK_NODE_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    BUS_WRITER_IMAGE_RUST_FIELD_NUMBER: _ClassVar[int]
    USE_AWS_POOL_FOR_GOOGLE_ADC_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    bus_writer_image_go: str
    bus_writer_image_python: str
    bus_writer_image_bswl: str
    service_account_name: str
    bus_backend: str
    secret_client: str
    bigquery_parquet_upload_subscription_id: str
    bigquery_streaming_write_subscription_id: str
    bigquery_streaming_write_topic: str
    bigquery_upload_bucket: str
    bigquery_upload_topic: str
    google_cloud_project: str
    kafka_dlq_topic: str
    metrics_bus_subscription_id: str
    metrics_bus_topic_id: str
    operation_subscription_id: str
    query_log_result_topic: str
    query_log_subscription_id: str
    result_bus_metrics_subscription_id: str
    result_bus_offline_store_subscription_id: str
    result_bus_online_store_subscription_id: str
    result_bus_topic_id: str
    usage_bus_topic_id: str
    usage_events_subscription_id: str
    bq_upload_bucket: str
    bq_upload_topic: str
    include_chalk_node_selector: bool
    bus_writer_image_rust: str
    use_aws_pool_for_google_adc: bool
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        bus_writer_image_go: _Optional[str] = ...,
        bus_writer_image_python: _Optional[str] = ...,
        bus_writer_image_bswl: _Optional[str] = ...,
        service_account_name: _Optional[str] = ...,
        bus_backend: _Optional[str] = ...,
        secret_client: _Optional[str] = ...,
        bigquery_parquet_upload_subscription_id: _Optional[str] = ...,
        bigquery_streaming_write_subscription_id: _Optional[str] = ...,
        bigquery_streaming_write_topic: _Optional[str] = ...,
        bigquery_upload_bucket: _Optional[str] = ...,
        bigquery_upload_topic: _Optional[str] = ...,
        google_cloud_project: _Optional[str] = ...,
        kafka_dlq_topic: _Optional[str] = ...,
        metrics_bus_subscription_id: _Optional[str] = ...,
        metrics_bus_topic_id: _Optional[str] = ...,
        operation_subscription_id: _Optional[str] = ...,
        query_log_result_topic: _Optional[str] = ...,
        query_log_subscription_id: _Optional[str] = ...,
        result_bus_metrics_subscription_id: _Optional[str] = ...,
        result_bus_offline_store_subscription_id: _Optional[str] = ...,
        result_bus_online_store_subscription_id: _Optional[str] = ...,
        result_bus_topic_id: _Optional[str] = ...,
        usage_bus_topic_id: _Optional[str] = ...,
        usage_events_subscription_id: _Optional[str] = ...,
        bq_upload_bucket: _Optional[str] = ...,
        bq_upload_topic: _Optional[str] = ...,
        include_chalk_node_selector: bool = ...,
        bus_writer_image_rust: _Optional[str] = ...,
        use_aws_pool_for_google_adc: bool = ...,
    ) -> None: ...

class BackgroundPersistenceWriterHpaSpecs(_message.Message):
    __slots__ = ("hpa_pubsub_subscription_id", "hpa_min_replicas", "hpa_max_replicas", "hpa_target_average_value")
    HPA_PUBSUB_SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    HPA_MIN_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    HPA_MAX_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    HPA_TARGET_AVERAGE_VALUE_FIELD_NUMBER: _ClassVar[int]
    hpa_pubsub_subscription_id: str
    hpa_min_replicas: int
    hpa_max_replicas: int
    hpa_target_average_value: int
    def __init__(
        self,
        hpa_pubsub_subscription_id: _Optional[str] = ...,
        hpa_min_replicas: _Optional[int] = ...,
        hpa_max_replicas: _Optional[int] = ...,
        hpa_target_average_value: _Optional[int] = ...,
    ) -> None: ...

class BackgroundPersistenceWriterSpecs(_message.Message):
    __slots__ = (
        "name",
        "image_override",
        "hpa_specs",
        "gke_spot",
        "load_writer_configmap",
        "version",
        "request",
        "limit",
        "bus_subscriber_type",
        "default_replica_count",
        "kafka_consumer_group_override",
        "max_batch_size",
        "message_processing_concurrency",
        "metadata_sql_ssl_ca_cert_secret",
        "metadata_sql_ssl_client_cert_secret",
        "metadata_sql_ssl_client_key_secret",
        "metadata_sql_uri_secret",
        "offline_store_inserter_db_type",
        "storage_cache_prefix",
        "usage_store_uri",
        "results_writer_skip_producing_feature_metrics",
        "query_table_write_drop_ratio",
        "instance_type",
        "nodepool",
        "node_selector",
        "additional_env_vars",
    )
    class NodeSelectorEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class AdditionalEnvVarsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    IMAGE_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    HPA_SPECS_FIELD_NUMBER: _ClassVar[int]
    GKE_SPOT_FIELD_NUMBER: _ClassVar[int]
    LOAD_WRITER_CONFIGMAP_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    BUS_SUBSCRIBER_TYPE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_REPLICA_COUNT_FIELD_NUMBER: _ClassVar[int]
    KAFKA_CONSUMER_GROUP_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    MAX_BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_PROCESSING_CONCURRENCY_FIELD_NUMBER: _ClassVar[int]
    METADATA_SQL_SSL_CA_CERT_SECRET_FIELD_NUMBER: _ClassVar[int]
    METADATA_SQL_SSL_CLIENT_CERT_SECRET_FIELD_NUMBER: _ClassVar[int]
    METADATA_SQL_SSL_CLIENT_KEY_SECRET_FIELD_NUMBER: _ClassVar[int]
    METADATA_SQL_URI_SECRET_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_STORE_INSERTER_DB_TYPE_FIELD_NUMBER: _ClassVar[int]
    STORAGE_CACHE_PREFIX_FIELD_NUMBER: _ClassVar[int]
    USAGE_STORE_URI_FIELD_NUMBER: _ClassVar[int]
    RESULTS_WRITER_SKIP_PRODUCING_FEATURE_METRICS_FIELD_NUMBER: _ClassVar[int]
    QUERY_TABLE_WRITE_DROP_RATIO_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    NODE_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_ENV_VARS_FIELD_NUMBER: _ClassVar[int]
    name: str
    image_override: str
    hpa_specs: BackgroundPersistenceWriterHpaSpecs
    gke_spot: bool
    load_writer_configmap: bool
    version: str
    request: KubeResourceConfig
    limit: KubeResourceConfig
    bus_subscriber_type: str
    default_replica_count: int
    kafka_consumer_group_override: str
    max_batch_size: int
    message_processing_concurrency: int
    metadata_sql_ssl_ca_cert_secret: str
    metadata_sql_ssl_client_cert_secret: str
    metadata_sql_ssl_client_key_secret: str
    metadata_sql_uri_secret: str
    offline_store_inserter_db_type: str
    storage_cache_prefix: str
    usage_store_uri: str
    results_writer_skip_producing_feature_metrics: bool
    query_table_write_drop_ratio: str
    instance_type: str
    nodepool: str
    node_selector: _containers.ScalarMap[str, str]
    additional_env_vars: _containers.ScalarMap[str, str]
    def __init__(
        self,
        name: _Optional[str] = ...,
        image_override: _Optional[str] = ...,
        hpa_specs: _Optional[_Union[BackgroundPersistenceWriterHpaSpecs, _Mapping]] = ...,
        gke_spot: bool = ...,
        load_writer_configmap: bool = ...,
        version: _Optional[str] = ...,
        request: _Optional[_Union[KubeResourceConfig, _Mapping]] = ...,
        limit: _Optional[_Union[KubeResourceConfig, _Mapping]] = ...,
        bus_subscriber_type: _Optional[str] = ...,
        default_replica_count: _Optional[int] = ...,
        kafka_consumer_group_override: _Optional[str] = ...,
        max_batch_size: _Optional[int] = ...,
        message_processing_concurrency: _Optional[int] = ...,
        metadata_sql_ssl_ca_cert_secret: _Optional[str] = ...,
        metadata_sql_ssl_client_cert_secret: _Optional[str] = ...,
        metadata_sql_ssl_client_key_secret: _Optional[str] = ...,
        metadata_sql_uri_secret: _Optional[str] = ...,
        offline_store_inserter_db_type: _Optional[str] = ...,
        storage_cache_prefix: _Optional[str] = ...,
        usage_store_uri: _Optional[str] = ...,
        results_writer_skip_producing_feature_metrics: bool = ...,
        query_table_write_drop_ratio: _Optional[str] = ...,
        instance_type: _Optional[str] = ...,
        nodepool: _Optional[str] = ...,
        node_selector: _Optional[_Mapping[str, str]] = ...,
        additional_env_vars: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class NodePodMetricsFilter(_message.Message):
    __slots__ = ("pod_label_regex", "namespace_regex", "node_selector")
    class NodeSelectorEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    POD_LABEL_REGEX_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_REGEX_FIELD_NUMBER: _ClassVar[int]
    NODE_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    pod_label_regex: str
    namespace_regex: str
    node_selector: _containers.ScalarMap[str, str]
    def __init__(
        self,
        pod_label_regex: _Optional[str] = ...,
        namespace_regex: _Optional[str] = ...,
        node_selector: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class ClusterManagerConfig(_message.Message):
    __slots__ = (
        "node_pod_metrics_filters",
        "node_pod_metrics_interval_secs",
        "record_node_pod_metrics",
        "record_gpu_metrics",
    )
    NODE_POD_METRICS_FILTERS_FIELD_NUMBER: _ClassVar[int]
    NODE_POD_METRICS_INTERVAL_SECS_FIELD_NUMBER: _ClassVar[int]
    RECORD_NODE_POD_METRICS_FIELD_NUMBER: _ClassVar[int]
    RECORD_GPU_METRICS_FIELD_NUMBER: _ClassVar[int]
    node_pod_metrics_filters: _containers.RepeatedCompositeFieldContainer[NodePodMetricsFilter]
    node_pod_metrics_interval_secs: int
    record_node_pod_metrics: bool
    record_gpu_metrics: bool
    def __init__(
        self,
        node_pod_metrics_filters: _Optional[_Iterable[_Union[NodePodMetricsFilter, _Mapping]]] = ...,
        node_pod_metrics_interval_secs: _Optional[int] = ...,
        record_node_pod_metrics: bool = ...,
        record_gpu_metrics: bool = ...,
    ) -> None: ...

class BackgroundPersistenceDeploymentSpecs(_message.Message):
    __slots__ = (
        "common_persistence_specs",
        "api_server_host",
        "kafka_sasl_secret",
        "metadata_provider",
        "kafka_bootstrap_servers",
        "kafka_security_protocol",
        "kafka_sasl_mechanism",
        "redis_is_clustered",
        "snowflake_storage_integration_name",
        "redis_lightning_supports_has_many",
        "insecure",
        "writers",
        "bootstrap_cloud_resources",
        "suspended",
        "observability_daemons",
        "cluster_manager_config",
        "autodiscover_key",
        "observability_daemon_scheduling",
    )
    COMMON_PERSISTENCE_SPECS_FIELD_NUMBER: _ClassVar[int]
    API_SERVER_HOST_FIELD_NUMBER: _ClassVar[int]
    KAFKA_SASL_SECRET_FIELD_NUMBER: _ClassVar[int]
    METADATA_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    KAFKA_BOOTSTRAP_SERVERS_FIELD_NUMBER: _ClassVar[int]
    KAFKA_SECURITY_PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    KAFKA_SASL_MECHANISM_FIELD_NUMBER: _ClassVar[int]
    REDIS_IS_CLUSTERED_FIELD_NUMBER: _ClassVar[int]
    SNOWFLAKE_STORAGE_INTEGRATION_NAME_FIELD_NUMBER: _ClassVar[int]
    REDIS_LIGHTNING_SUPPORTS_HAS_MANY_FIELD_NUMBER: _ClassVar[int]
    INSECURE_FIELD_NUMBER: _ClassVar[int]
    WRITERS_FIELD_NUMBER: _ClassVar[int]
    BOOTSTRAP_CLOUD_RESOURCES_FIELD_NUMBER: _ClassVar[int]
    SUSPENDED_FIELD_NUMBER: _ClassVar[int]
    OBSERVABILITY_DAEMONS_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_MANAGER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    AUTODISCOVER_KEY_FIELD_NUMBER: _ClassVar[int]
    OBSERVABILITY_DAEMON_SCHEDULING_FIELD_NUMBER: _ClassVar[int]
    common_persistence_specs: BackgroundPersistenceCommonSpecs
    api_server_host: str
    kafka_sasl_secret: str
    metadata_provider: str
    kafka_bootstrap_servers: str
    kafka_security_protocol: str
    kafka_sasl_mechanism: str
    redis_is_clustered: str
    snowflake_storage_integration_name: str
    redis_lightning_supports_has_many: bool
    insecure: bool
    writers: _containers.RepeatedCompositeFieldContainer[BackgroundPersistenceWriterSpecs]
    bootstrap_cloud_resources: bool
    suspended: bool
    observability_daemons: _containers.RepeatedCompositeFieldContainer[ObservabilityDaemonSpec]
    cluster_manager_config: ClusterManagerConfig
    autodiscover_key: str
    observability_daemon_scheduling: ObservabilityDaemonSchedulingSpec
    def __init__(
        self,
        common_persistence_specs: _Optional[_Union[BackgroundPersistenceCommonSpecs, _Mapping]] = ...,
        api_server_host: _Optional[str] = ...,
        kafka_sasl_secret: _Optional[str] = ...,
        metadata_provider: _Optional[str] = ...,
        kafka_bootstrap_servers: _Optional[str] = ...,
        kafka_security_protocol: _Optional[str] = ...,
        kafka_sasl_mechanism: _Optional[str] = ...,
        redis_is_clustered: _Optional[str] = ...,
        snowflake_storage_integration_name: _Optional[str] = ...,
        redis_lightning_supports_has_many: bool = ...,
        insecure: bool = ...,
        writers: _Optional[_Iterable[_Union[BackgroundPersistenceWriterSpecs, _Mapping]]] = ...,
        bootstrap_cloud_resources: bool = ...,
        suspended: bool = ...,
        observability_daemons: _Optional[_Iterable[_Union[ObservabilityDaemonSpec, _Mapping]]] = ...,
        cluster_manager_config: _Optional[_Union[ClusterManagerConfig, _Mapping]] = ...,
        autodiscover_key: _Optional[str] = ...,
        observability_daemon_scheduling: _Optional[_Union[ObservabilityDaemonSchedulingSpec, _Mapping]] = ...,
    ) -> None: ...

class CreateClusterBackgroundPersistenceResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class KubeNodeSelector(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class VectorAggregatorClickHouseSinkSpec(_message.Message):
    __slots__ = ("request_concurrency", "batch_max_events", "batch_max_bytes", "batch_timeout_secs")
    REQUEST_CONCURRENCY_FIELD_NUMBER: _ClassVar[int]
    BATCH_MAX_EVENTS_FIELD_NUMBER: _ClassVar[int]
    BATCH_MAX_BYTES_FIELD_NUMBER: _ClassVar[int]
    BATCH_TIMEOUT_SECS_FIELD_NUMBER: _ClassVar[int]
    request_concurrency: int
    batch_max_events: int
    batch_max_bytes: int
    batch_timeout_secs: int
    def __init__(
        self,
        request_concurrency: _Optional[int] = ...,
        batch_max_events: _Optional[int] = ...,
        batch_max_bytes: _Optional[int] = ...,
        batch_timeout_secs: _Optional[int] = ...,
    ) -> None: ...

class VectorAggregatorVictoriaMetricsSinkSpec(_message.Message):
    __slots__ = (
        "request_concurrency",
        "batch_max_events",
        "batch_max_bytes",
        "batch_timeout_secs",
        "request_timeout_secs",
        "request_retry_attempts",
        "buffer_max_size",
        "buffer_when_full",
        "acknowledgements_enabled",
        "batch_aggregate",
        "expire_metrics_secs",
        "healthcheck_enabled",
    )
    REQUEST_CONCURRENCY_FIELD_NUMBER: _ClassVar[int]
    BATCH_MAX_EVENTS_FIELD_NUMBER: _ClassVar[int]
    BATCH_MAX_BYTES_FIELD_NUMBER: _ClassVar[int]
    BATCH_TIMEOUT_SECS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_TIMEOUT_SECS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_RETRY_ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    BUFFER_MAX_SIZE_FIELD_NUMBER: _ClassVar[int]
    BUFFER_WHEN_FULL_FIELD_NUMBER: _ClassVar[int]
    ACKNOWLEDGEMENTS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    BATCH_AGGREGATE_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_METRICS_SECS_FIELD_NUMBER: _ClassVar[int]
    HEALTHCHECK_ENABLED_FIELD_NUMBER: _ClassVar[int]
    request_concurrency: int
    batch_max_events: int
    batch_max_bytes: int
    batch_timeout_secs: int
    request_timeout_secs: int
    request_retry_attempts: int
    buffer_max_size: int
    buffer_when_full: str
    acknowledgements_enabled: bool
    batch_aggregate: bool
    expire_metrics_secs: int
    healthcheck_enabled: bool
    def __init__(
        self,
        request_concurrency: _Optional[int] = ...,
        batch_max_events: _Optional[int] = ...,
        batch_max_bytes: _Optional[int] = ...,
        batch_timeout_secs: _Optional[int] = ...,
        request_timeout_secs: _Optional[int] = ...,
        request_retry_attempts: _Optional[int] = ...,
        buffer_max_size: _Optional[int] = ...,
        buffer_when_full: _Optional[str] = ...,
        acknowledgements_enabled: bool = ...,
        batch_aggregate: bool = ...,
        expire_metrics_secs: _Optional[int] = ...,
        healthcheck_enabled: bool = ...,
    ) -> None: ...

class VectorAggregatorChalkDatadogExportSpec(_message.Message):
    __slots__ = ("logs", "traces", "metrics", "metrics_sink")
    LOGS_FIELD_NUMBER: _ClassVar[int]
    TRACES_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    METRICS_SINK_FIELD_NUMBER: _ClassVar[int]
    logs: bool
    traces: bool
    metrics: bool
    metrics_sink: VectorAggregatorChalkDatadogMetricsSinkSpec
    def __init__(
        self,
        logs: bool = ...,
        traces: bool = ...,
        metrics: bool = ...,
        metrics_sink: _Optional[_Union[VectorAggregatorChalkDatadogMetricsSinkSpec, _Mapping]] = ...,
    ) -> None: ...

class VectorAggregatorChalkDatadogMetricsSinkSpec(_message.Message):
    __slots__ = (
        "request_concurrency",
        "batch_max_events",
        "batch_max_bytes",
        "batch_timeout_secs",
        "request_timeout_secs",
        "buffer_max_size",
        "buffer_when_full",
    )
    REQUEST_CONCURRENCY_FIELD_NUMBER: _ClassVar[int]
    BATCH_MAX_EVENTS_FIELD_NUMBER: _ClassVar[int]
    BATCH_MAX_BYTES_FIELD_NUMBER: _ClassVar[int]
    BATCH_TIMEOUT_SECS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_TIMEOUT_SECS_FIELD_NUMBER: _ClassVar[int]
    BUFFER_MAX_SIZE_FIELD_NUMBER: _ClassVar[int]
    BUFFER_WHEN_FULL_FIELD_NUMBER: _ClassVar[int]
    request_concurrency: int
    batch_max_events: int
    batch_max_bytes: int
    batch_timeout_secs: int
    request_timeout_secs: int
    buffer_max_size: int
    buffer_when_full: str
    def __init__(
        self,
        request_concurrency: _Optional[int] = ...,
        batch_max_events: _Optional[int] = ...,
        batch_max_bytes: _Optional[int] = ...,
        batch_timeout_secs: _Optional[int] = ...,
        request_timeout_secs: _Optional[int] = ...,
        buffer_max_size: _Optional[int] = ...,
        buffer_when_full: _Optional[str] = ...,
    ) -> None: ...

class VectorAggregatorMetricAggregationSpec(_message.Message):
    __slots__ = ("enabled", "interval_ms", "mode")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_MS_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    interval_ms: int
    mode: str
    def __init__(self, enabled: bool = ..., interval_ms: _Optional[int] = ..., mode: _Optional[str] = ...) -> None: ...

class VectorCollectorMetricAggregationSpec(_message.Message):
    __slots__ = ("enabled", "interval_ms", "mode")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_MS_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    interval_ms: int
    mode: str
    def __init__(self, enabled: bool = ..., interval_ms: _Optional[int] = ..., mode: _Optional[str] = ...) -> None: ...

class CustomerVectorAggregatorDatadogSignalExportSpec(_message.Message):
    __slots__ = ("enabled", "remap_vrl")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    REMAP_VRL_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    remap_vrl: str
    def __init__(self, enabled: bool = ..., remap_vrl: _Optional[str] = ...) -> None: ...

class CustomerVectorAggregatorDatadogMetricsSinkSpec(_message.Message):
    __slots__ = (
        "request_concurrency",
        "batch_max_events",
        "batch_max_bytes",
        "batch_timeout_secs",
        "request_timeout_secs",
        "buffer_max_size",
        "buffer_when_full",
    )
    REQUEST_CONCURRENCY_FIELD_NUMBER: _ClassVar[int]
    BATCH_MAX_EVENTS_FIELD_NUMBER: _ClassVar[int]
    BATCH_MAX_BYTES_FIELD_NUMBER: _ClassVar[int]
    BATCH_TIMEOUT_SECS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_TIMEOUT_SECS_FIELD_NUMBER: _ClassVar[int]
    BUFFER_MAX_SIZE_FIELD_NUMBER: _ClassVar[int]
    BUFFER_WHEN_FULL_FIELD_NUMBER: _ClassVar[int]
    request_concurrency: int
    batch_max_events: int
    batch_max_bytes: int
    batch_timeout_secs: int
    request_timeout_secs: int
    buffer_max_size: int
    buffer_when_full: str
    def __init__(
        self,
        request_concurrency: _Optional[int] = ...,
        batch_max_events: _Optional[int] = ...,
        batch_max_bytes: _Optional[int] = ...,
        batch_timeout_secs: _Optional[int] = ...,
        request_timeout_secs: _Optional[int] = ...,
        buffer_max_size: _Optional[int] = ...,
        buffer_when_full: _Optional[str] = ...,
    ) -> None: ...

class CustomerVectorAggregatorDatadogExportConfig(_message.Message):
    __slots__ = ("api_key", "api_key_secret_arn", "api_host", "logs", "traces", "metrics", "metrics_sink")
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    API_KEY_SECRET_ARN_FIELD_NUMBER: _ClassVar[int]
    API_HOST_FIELD_NUMBER: _ClassVar[int]
    LOGS_FIELD_NUMBER: _ClassVar[int]
    TRACES_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    METRICS_SINK_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    api_key_secret_arn: str
    api_host: str
    logs: CustomerVectorAggregatorDatadogSignalExportSpec
    traces: CustomerVectorAggregatorDatadogSignalExportSpec
    metrics: CustomerVectorAggregatorDatadogSignalExportSpec
    metrics_sink: CustomerVectorAggregatorDatadogMetricsSinkSpec
    def __init__(
        self,
        api_key: _Optional[str] = ...,
        api_key_secret_arn: _Optional[str] = ...,
        api_host: _Optional[str] = ...,
        logs: _Optional[_Union[CustomerVectorAggregatorDatadogSignalExportSpec, _Mapping]] = ...,
        traces: _Optional[_Union[CustomerVectorAggregatorDatadogSignalExportSpec, _Mapping]] = ...,
        metrics: _Optional[_Union[CustomerVectorAggregatorDatadogSignalExportSpec, _Mapping]] = ...,
        metrics_sink: _Optional[_Union[CustomerVectorAggregatorDatadogMetricsSinkSpec, _Mapping]] = ...,
    ) -> None: ...

class CustomerVectorAggregatorStatsdMetricsSinkSpec(_message.Message):
    __slots__ = ("batch_max_events", "batch_timeout_secs", "buffer_max_size", "buffer_when_full")
    BATCH_MAX_EVENTS_FIELD_NUMBER: _ClassVar[int]
    BATCH_TIMEOUT_SECS_FIELD_NUMBER: _ClassVar[int]
    BUFFER_MAX_SIZE_FIELD_NUMBER: _ClassVar[int]
    BUFFER_WHEN_FULL_FIELD_NUMBER: _ClassVar[int]
    batch_max_events: int
    batch_timeout_secs: int
    buffer_max_size: int
    buffer_when_full: str
    def __init__(
        self,
        batch_max_events: _Optional[int] = ...,
        batch_timeout_secs: _Optional[int] = ...,
        buffer_max_size: _Optional[int] = ...,
        buffer_when_full: _Optional[str] = ...,
    ) -> None: ...

class CustomerVectorAggregatorStatsdExportConfig(_message.Message):
    __slots__ = ("enabled", "host", "port", "protocol", "metrics_sink", "remap_vrl")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    METRICS_SINK_FIELD_NUMBER: _ClassVar[int]
    REMAP_VRL_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    host: str
    port: int
    protocol: CustomerVectorAggregatorStatsdProtocol
    metrics_sink: CustomerVectorAggregatorStatsdMetricsSinkSpec
    remap_vrl: str
    def __init__(
        self,
        enabled: bool = ...,
        host: _Optional[str] = ...,
        port: _Optional[int] = ...,
        protocol: _Optional[_Union[CustomerVectorAggregatorStatsdProtocol, str]] = ...,
        metrics_sink: _Optional[_Union[CustomerVectorAggregatorStatsdMetricsSinkSpec, _Mapping]] = ...,
        remap_vrl: _Optional[str] = ...,
    ) -> None: ...

class CustomerVectorAggregatorConfig(_message.Message):
    __slots__ = (
        "datadog_export",
        "replicas",
        "statsd_export",
        "logs_remap_vrl",
        "metrics_remap_vrl",
        "traces_remap_vrl",
    )
    DATADOG_EXPORT_FIELD_NUMBER: _ClassVar[int]
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    STATSD_EXPORT_FIELD_NUMBER: _ClassVar[int]
    LOGS_REMAP_VRL_FIELD_NUMBER: _ClassVar[int]
    METRICS_REMAP_VRL_FIELD_NUMBER: _ClassVar[int]
    TRACES_REMAP_VRL_FIELD_NUMBER: _ClassVar[int]
    datadog_export: CustomerVectorAggregatorDatadogExportConfig
    replicas: int
    statsd_export: CustomerVectorAggregatorStatsdExportConfig
    logs_remap_vrl: str
    metrics_remap_vrl: str
    traces_remap_vrl: str
    def __init__(
        self,
        datadog_export: _Optional[_Union[CustomerVectorAggregatorDatadogExportConfig, _Mapping]] = ...,
        replicas: _Optional[int] = ...,
        statsd_export: _Optional[_Union[CustomerVectorAggregatorStatsdExportConfig, _Mapping]] = ...,
        logs_remap_vrl: _Optional[str] = ...,
        metrics_remap_vrl: _Optional[str] = ...,
        traces_remap_vrl: _Optional[str] = ...,
    ) -> None: ...

class AggregatorSpec(_message.Message):
    __slots__ = (
        "image_version",
        "request",
        "limit",
        "vector_click_house_sink",
        "export_to_chalk_datadog",
        "vector_victoria_metrics_sink",
        "replicas",
        "metric_aggregation",
    )
    IMAGE_VERSION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLICK_HOUSE_SINK_FIELD_NUMBER: _ClassVar[int]
    EXPORT_TO_CHALK_DATADOG_FIELD_NUMBER: _ClassVar[int]
    VECTOR_VICTORIA_METRICS_SINK_FIELD_NUMBER: _ClassVar[int]
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    METRIC_AGGREGATION_FIELD_NUMBER: _ClassVar[int]
    image_version: str
    request: KubeResourceConfig
    limit: KubeResourceConfig
    vector_click_house_sink: VectorAggregatorClickHouseSinkSpec
    export_to_chalk_datadog: VectorAggregatorChalkDatadogExportSpec
    vector_victoria_metrics_sink: VectorAggregatorVictoriaMetricsSinkSpec
    replicas: int
    metric_aggregation: VectorAggregatorMetricAggregationSpec
    def __init__(
        self,
        image_version: _Optional[str] = ...,
        request: _Optional[_Union[KubeResourceConfig, _Mapping]] = ...,
        limit: _Optional[_Union[KubeResourceConfig, _Mapping]] = ...,
        vector_click_house_sink: _Optional[_Union[VectorAggregatorClickHouseSinkSpec, _Mapping]] = ...,
        export_to_chalk_datadog: _Optional[_Union[VectorAggregatorChalkDatadogExportSpec, _Mapping]] = ...,
        vector_victoria_metrics_sink: _Optional[_Union[VectorAggregatorVictoriaMetricsSinkSpec, _Mapping]] = ...,
        replicas: _Optional[int] = ...,
        metric_aggregation: _Optional[_Union[VectorAggregatorMetricAggregationSpec, _Mapping]] = ...,
    ) -> None: ...

class CustomerCollectorConfig(_message.Message):
    __slots__ = ("config_yaml",)
    CONFIG_YAML_FIELD_NUMBER: _ClassVar[int]
    config_yaml: str
    def __init__(self, config_yaml: _Optional[str] = ...) -> None: ...

class VectorClusterMetricsSpec(_message.Message):
    __slots__ = (
        "collector_scrape_enabled",
        "timescale_sink_enabled",
        "sink_mode",
        "shadow",
        "tables",
        "destination_refresh_interval_seconds",
        "destination_refresh_backoff_seconds",
        "batch_max_events",
        "batch_timeout_seconds",
        "collector_scrape_interval_seconds",
        "collector_scrape_timeout_seconds",
        "api_server_uri",
        "pod_filters",
    )
    COLLECTOR_SCRAPE_ENABLED_FIELD_NUMBER: _ClassVar[int]
    TIMESCALE_SINK_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SINK_MODE_FIELD_NUMBER: _ClassVar[int]
    SHADOW_FIELD_NUMBER: _ClassVar[int]
    TABLES_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_REFRESH_INTERVAL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_REFRESH_BACKOFF_SECONDS_FIELD_NUMBER: _ClassVar[int]
    BATCH_MAX_EVENTS_FIELD_NUMBER: _ClassVar[int]
    BATCH_TIMEOUT_SECONDS_FIELD_NUMBER: _ClassVar[int]
    COLLECTOR_SCRAPE_INTERVAL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    COLLECTOR_SCRAPE_TIMEOUT_SECONDS_FIELD_NUMBER: _ClassVar[int]
    API_SERVER_URI_FIELD_NUMBER: _ClassVar[int]
    POD_FILTERS_FIELD_NUMBER: _ClassVar[int]
    collector_scrape_enabled: bool
    timescale_sink_enabled: bool
    sink_mode: VectorClusterMetricsSinkMode
    shadow: VectorClusterMetricsShadowSpec
    tables: VectorClusterMetricsTablesSpec
    destination_refresh_interval_seconds: int
    destination_refresh_backoff_seconds: int
    batch_max_events: int
    batch_timeout_seconds: int
    collector_scrape_interval_seconds: int
    collector_scrape_timeout_seconds: int
    api_server_uri: str
    pod_filters: _containers.RepeatedCompositeFieldContainer[NodePodMetricsFilter]
    def __init__(
        self,
        collector_scrape_enabled: bool = ...,
        timescale_sink_enabled: bool = ...,
        sink_mode: _Optional[_Union[VectorClusterMetricsSinkMode, str]] = ...,
        shadow: _Optional[_Union[VectorClusterMetricsShadowSpec, _Mapping]] = ...,
        tables: _Optional[_Union[VectorClusterMetricsTablesSpec, _Mapping]] = ...,
        destination_refresh_interval_seconds: _Optional[int] = ...,
        destination_refresh_backoff_seconds: _Optional[int] = ...,
        batch_max_events: _Optional[int] = ...,
        batch_timeout_seconds: _Optional[int] = ...,
        collector_scrape_interval_seconds: _Optional[int] = ...,
        collector_scrape_timeout_seconds: _Optional[int] = ...,
        api_server_uri: _Optional[str] = ...,
        pod_filters: _Optional[_Iterable[_Union[NodePodMetricsFilter, _Mapping]]] = ...,
    ) -> None: ...

class TelemetryIngestMetricsSpec(_message.Message):
    __slots__ = ("enabled", "statsd_endpoint", "image_version", "request")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    STATSD_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    IMAGE_VERSION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    statsd_endpoint: str
    image_version: str
    request: KubeResourceConfig
    def __init__(
        self,
        enabled: bool = ...,
        statsd_endpoint: _Optional[str] = ...,
        image_version: _Optional[str] = ...,
        request: _Optional[_Union[KubeResourceConfig, _Mapping]] = ...,
    ) -> None: ...

class VectorStatsdUdsSpec(_message.Message):
    __slots__ = ("enabled", "socket_path", "socket_file_mode", "peer_credentials")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    SOCKET_PATH_FIELD_NUMBER: _ClassVar[int]
    SOCKET_FILE_MODE_FIELD_NUMBER: _ClassVar[int]
    PEER_CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    socket_path: str
    socket_file_mode: int
    peer_credentials: bool
    def __init__(
        self,
        enabled: bool = ...,
        socket_path: _Optional[str] = ...,
        socket_file_mode: _Optional[int] = ...,
        peer_credentials: bool = ...,
    ) -> None: ...

class VectorStatsdUdpSpec(_message.Message):
    __slots__ = ("enabled", "port", "listen_address")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    LISTEN_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    port: int
    listen_address: str
    def __init__(
        self, enabled: bool = ..., port: _Optional[int] = ..., listen_address: _Optional[str] = ...
    ) -> None: ...

class VectorStatsdSpec(_message.Message):
    __slots__ = ("enabled", "uds", "udp", "pod_label_allowlist")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    UDS_FIELD_NUMBER: _ClassVar[int]
    UDP_FIELD_NUMBER: _ClassVar[int]
    POD_LABEL_ALLOWLIST_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    uds: VectorStatsdUdsSpec
    udp: VectorStatsdUdpSpec
    pod_label_allowlist: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        enabled: bool = ...,
        uds: _Optional[_Union[VectorStatsdUdsSpec, _Mapping]] = ...,
        udp: _Optional[_Union[VectorStatsdUdpSpec, _Mapping]] = ...,
        pod_label_allowlist: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class MetricExportDestination(_message.Message):
    __slots__ = ("name", "format", "endpoint")
    NAME_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    name: str
    format: MetricExportDestinationFormat
    endpoint: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        format: _Optional[_Union[MetricExportDestinationFormat, str]] = ...,
        endpoint: _Optional[str] = ...,
    ) -> None: ...

class MetricExportSpec(_message.Message):
    __slots__ = ("additional_destinations",)
    ADDITIONAL_DESTINATIONS_FIELD_NUMBER: _ClassVar[int]
    additional_destinations: _containers.RepeatedCompositeFieldContainer[MetricExportDestination]
    def __init__(
        self, additional_destinations: _Optional[_Iterable[_Union[MetricExportDestination, _Mapping]]] = ...
    ) -> None: ...

class VectorClusterMetricsShadowSpec(_message.Message):
    __slots__ = ("output", "tables")
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    TABLES_FIELD_NUMBER: _ClassVar[int]
    output: VectorClusterMetricsShadowOutput
    tables: VectorClusterMetricsShadowTables
    def __init__(
        self,
        output: _Optional[_Union[VectorClusterMetricsShadowOutput, str]] = ...,
        tables: _Optional[_Union[VectorClusterMetricsShadowTables, _Mapping]] = ...,
    ) -> None: ...

class VectorClusterMetricsTablesSpec(_message.Message):
    __slots__ = ("cluster_metrics", "metrics1", "metrics4")
    CLUSTER_METRICS_FIELD_NUMBER: _ClassVar[int]
    METRICS1_FIELD_NUMBER: _ClassVar[int]
    METRICS4_FIELD_NUMBER: _ClassVar[int]
    cluster_metrics: str
    metrics1: str
    metrics4: str
    def __init__(
        self, cluster_metrics: _Optional[str] = ..., metrics1: _Optional[str] = ..., metrics4: _Optional[str] = ...
    ) -> None: ...

class VectorClusterMetricsShadowTables(_message.Message):
    __slots__ = ("cluster_metrics", "metrics1", "metrics4")
    CLUSTER_METRICS_FIELD_NUMBER: _ClassVar[int]
    METRICS1_FIELD_NUMBER: _ClassVar[int]
    METRICS4_FIELD_NUMBER: _ClassVar[int]
    cluster_metrics: str
    metrics1: str
    metrics4: str
    def __init__(
        self, cluster_metrics: _Optional[str] = ..., metrics1: _Optional[str] = ..., metrics4: _Optional[str] = ...
    ) -> None: ...

class OtelCollectorSpec(_message.Message):
    __slots__ = (
        "otel_collector_version",
        "request",
        "limit",
        "toleration_mode",
        "otel_collector_image",
        "metric_aggregation",
    )
    OTEL_COLLECTOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    TOLERATION_MODE_FIELD_NUMBER: _ClassVar[int]
    OTEL_COLLECTOR_IMAGE_FIELD_NUMBER: _ClassVar[int]
    METRIC_AGGREGATION_FIELD_NUMBER: _ClassVar[int]
    otel_collector_version: str
    request: KubeResourceConfig
    limit: KubeResourceConfig
    toleration_mode: TelemetryCollectorTolerationMode
    otel_collector_image: OtelCollectorImage
    metric_aggregation: VectorCollectorMetricAggregationSpec
    def __init__(
        self,
        otel_collector_version: _Optional[str] = ...,
        request: _Optional[_Union[KubeResourceConfig, _Mapping]] = ...,
        limit: _Optional[_Union[KubeResourceConfig, _Mapping]] = ...,
        toleration_mode: _Optional[_Union[TelemetryCollectorTolerationMode, str]] = ...,
        otel_collector_image: _Optional[_Union[OtelCollectorImage, str]] = ...,
        metric_aggregation: _Optional[_Union[VectorCollectorMetricAggregationSpec, _Mapping]] = ...,
    ) -> None: ...

class GpuTelemetrySpec(_message.Message):
    __slots__ = (
        "enabled",
        "request",
        "limit",
        "node_selectors",
        "runtime_class_name",
        "host_nvidia_lib_dir",
        "image_override",
    )
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    NODE_SELECTORS_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    HOST_NVIDIA_LIB_DIR_FIELD_NUMBER: _ClassVar[int]
    IMAGE_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    request: KubeResourceConfig
    limit: KubeResourceConfig
    node_selectors: _containers.RepeatedCompositeFieldContainer[KubeNodeSelector]
    runtime_class_name: str
    host_nvidia_lib_dir: str
    image_override: str
    def __init__(
        self,
        enabled: bool = ...,
        request: _Optional[_Union[KubeResourceConfig, _Mapping]] = ...,
        limit: _Optional[_Union[KubeResourceConfig, _Mapping]] = ...,
        node_selectors: _Optional[_Iterable[_Union[KubeNodeSelector, _Mapping]]] = ...,
        runtime_class_name: _Optional[str] = ...,
        host_nvidia_lib_dir: _Optional[str] = ...,
        image_override: _Optional[str] = ...,
    ) -> None: ...

class ClickHouseSpec(_message.Message):
    __slots__ = ("click_house_version", "request", "limit", "storage", "gateway_id", "instance_type", "serve_over_http")
    CLICK_HOUSE_VERSION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    GATEWAY_ID_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SERVE_OVER_HTTP_FIELD_NUMBER: _ClassVar[int]
    click_house_version: str
    request: KubeResourceConfig
    limit: KubeResourceConfig
    storage: KubePersistentVolumeClaim
    gateway_id: str
    instance_type: str
    serve_over_http: bool
    def __init__(
        self,
        click_house_version: _Optional[str] = ...,
        request: _Optional[_Union[KubeResourceConfig, _Mapping]] = ...,
        limit: _Optional[_Union[KubeResourceConfig, _Mapping]] = ...,
        storage: _Optional[_Union[KubePersistentVolumeClaim, _Mapping]] = ...,
        gateway_id: _Optional[str] = ...,
        instance_type: _Optional[str] = ...,
        serve_over_http: bool = ...,
    ) -> None: ...

class VictoriaMetricsSpec(_message.Message):
    __slots__ = (
        "retention_period",
        "storage_size",
        "storage_class",
        "request",
        "cloud_secret_name",
        "instance_type",
        "nodepool",
        "dns_name_override",
    )
    RETENTION_PERIOD_FIELD_NUMBER: _ClassVar[int]
    STORAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    STORAGE_CLASS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    CLOUD_SECRET_NAME_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    DNS_NAME_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    retention_period: str
    storage_size: str
    storage_class: str
    request: KubeResourceConfig
    cloud_secret_name: str
    instance_type: str
    nodepool: str
    dns_name_override: str
    def __init__(
        self,
        retention_period: _Optional[str] = ...,
        storage_size: _Optional[str] = ...,
        storage_class: _Optional[str] = ...,
        request: _Optional[_Union[KubeResourceConfig, _Mapping]] = ...,
        cloud_secret_name: _Optional[str] = ...,
        instance_type: _Optional[str] = ...,
        nodepool: _Optional[str] = ...,
        dns_name_override: _Optional[str] = ...,
    ) -> None: ...

class ZombieKillerSpec(_message.Message):
    __slots__ = ("interval",)
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    interval: int
    def __init__(self, interval: _Optional[int] = ...) -> None: ...

class CoreDumpCollectorSpec(_message.Message):
    __slots__ = (
        "core_dump_bucket_uri",
        "host_directory",
        "core_directory",
        "event_directory",
        "suid_dumpable",
        "vendor",
        "crio_endpoint",
        "deploy_crio_config",
        "include_crio_exe",
        "mount_container_runtime_endpoint",
        "host_container_runtime_endpoint",
        "comp_log_level",
        "comp_ignore_crio",
        "comp_include_proc_info",
        "comp_timeout",
        "comp_compression",
        "comp_core_events",
        "comp_filename_template",
        "comp_pod_selector_label",
        "comp_log_length",
    )
    CORE_DUMP_BUCKET_URI_FIELD_NUMBER: _ClassVar[int]
    HOST_DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    CORE_DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    EVENT_DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    SUID_DUMPABLE_FIELD_NUMBER: _ClassVar[int]
    VENDOR_FIELD_NUMBER: _ClassVar[int]
    CRIO_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    DEPLOY_CRIO_CONFIG_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_CRIO_EXE_FIELD_NUMBER: _ClassVar[int]
    MOUNT_CONTAINER_RUNTIME_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    HOST_CONTAINER_RUNTIME_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    COMP_LOG_LEVEL_FIELD_NUMBER: _ClassVar[int]
    COMP_IGNORE_CRIO_FIELD_NUMBER: _ClassVar[int]
    COMP_INCLUDE_PROC_INFO_FIELD_NUMBER: _ClassVar[int]
    COMP_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    COMP_COMPRESSION_FIELD_NUMBER: _ClassVar[int]
    COMP_CORE_EVENTS_FIELD_NUMBER: _ClassVar[int]
    COMP_FILENAME_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    COMP_POD_SELECTOR_LABEL_FIELD_NUMBER: _ClassVar[int]
    COMP_LOG_LENGTH_FIELD_NUMBER: _ClassVar[int]
    core_dump_bucket_uri: str
    host_directory: str
    core_directory: str
    event_directory: str
    suid_dumpable: int
    vendor: str
    crio_endpoint: str
    deploy_crio_config: bool
    include_crio_exe: bool
    mount_container_runtime_endpoint: bool
    host_container_runtime_endpoint: str
    comp_log_level: str
    comp_ignore_crio: bool
    comp_include_proc_info: bool
    comp_timeout: int
    comp_compression: bool
    comp_core_events: bool
    comp_filename_template: str
    comp_pod_selector_label: str
    comp_log_length: int
    def __init__(
        self,
        core_dump_bucket_uri: _Optional[str] = ...,
        host_directory: _Optional[str] = ...,
        core_directory: _Optional[str] = ...,
        event_directory: _Optional[str] = ...,
        suid_dumpable: _Optional[int] = ...,
        vendor: _Optional[str] = ...,
        crio_endpoint: _Optional[str] = ...,
        deploy_crio_config: bool = ...,
        include_crio_exe: bool = ...,
        mount_container_runtime_endpoint: bool = ...,
        host_container_runtime_endpoint: _Optional[str] = ...,
        comp_log_level: _Optional[str] = ...,
        comp_ignore_crio: bool = ...,
        comp_include_proc_info: bool = ...,
        comp_timeout: _Optional[int] = ...,
        comp_compression: bool = ...,
        comp_core_events: bool = ...,
        comp_filename_template: _Optional[str] = ...,
        comp_pod_selector_label: _Optional[str] = ...,
        comp_log_length: _Optional[int] = ...,
    ) -> None: ...

class PySpyStackTraceCollectorSpec(_message.Message):
    __slots__ = (
        "native",
        "subprocesses",
        "idle",
        "locals",
        "nonblocking",
        "max_retained_runs",
        "interval",
        "introspection_server_uris",
    )
    NATIVE_FIELD_NUMBER: _ClassVar[int]
    SUBPROCESSES_FIELD_NUMBER: _ClassVar[int]
    IDLE_FIELD_NUMBER: _ClassVar[int]
    LOCALS_FIELD_NUMBER: _ClassVar[int]
    NONBLOCKING_FIELD_NUMBER: _ClassVar[int]
    MAX_RETAINED_RUNS_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    INTROSPECTION_SERVER_URIS_FIELD_NUMBER: _ClassVar[int]
    native: bool
    subprocesses: bool
    idle: bool
    locals: bool
    nonblocking: bool
    max_retained_runs: int
    interval: int
    introspection_server_uris: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        native: bool = ...,
        subprocesses: bool = ...,
        idle: bool = ...,
        locals: bool = ...,
        nonblocking: bool = ...,
        max_retained_runs: _Optional[int] = ...,
        interval: _Optional[int] = ...,
        introspection_server_uris: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class PerfCollectorSpec(_message.Message):
    __slots__ = (
        "perf_polling_frequency_hz",
        "call_graph",
        "max_dumps_retained",
        "dump_duration_seconds",
        "export_to",
        "bucket_subdirectory",
    )
    PERF_POLLING_FREQUENCY_HZ_FIELD_NUMBER: _ClassVar[int]
    CALL_GRAPH_FIELD_NUMBER: _ClassVar[int]
    MAX_DUMPS_RETAINED_FIELD_NUMBER: _ClassVar[int]
    DUMP_DURATION_SECONDS_FIELD_NUMBER: _ClassVar[int]
    EXPORT_TO_FIELD_NUMBER: _ClassVar[int]
    BUCKET_SUBDIRECTORY_FIELD_NUMBER: _ClassVar[int]
    perf_polling_frequency_hz: int
    call_graph: bool
    max_dumps_retained: int
    dump_duration_seconds: int
    export_to: str
    bucket_subdirectory: str
    def __init__(
        self,
        perf_polling_frequency_hz: _Optional[int] = ...,
        call_graph: bool = ...,
        max_dumps_retained: _Optional[int] = ...,
        dump_duration_seconds: _Optional[int] = ...,
        export_to: _Optional[str] = ...,
        bucket_subdirectory: _Optional[str] = ...,
    ) -> None: ...

class PerfettoDaemonSpec(_message.Message):
    __slots__ = (
        "config_text",
        "max_retained_runs",
        "interval",
        "trigger_name",
        "export_to",
        "bucket_subdirectory",
        "trigger",
    )
    CONFIG_TEXT_FIELD_NUMBER: _ClassVar[int]
    MAX_RETAINED_RUNS_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_NAME_FIELD_NUMBER: _ClassVar[int]
    EXPORT_TO_FIELD_NUMBER: _ClassVar[int]
    BUCKET_SUBDIRECTORY_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    config_text: str
    max_retained_runs: int
    interval: int
    trigger_name: str
    export_to: str
    bucket_subdirectory: str
    trigger: PerfettoTrigger
    def __init__(
        self,
        config_text: _Optional[str] = ...,
        max_retained_runs: _Optional[int] = ...,
        interval: _Optional[int] = ...,
        trigger_name: _Optional[str] = ...,
        export_to: _Optional[str] = ...,
        bucket_subdirectory: _Optional[str] = ...,
        trigger: _Optional[_Union[PerfettoTrigger, str]] = ...,
    ) -> None: ...

class DirectoryWatcherSpec(_message.Message):
    __slots__ = (
        "watch_directory_subpath",
        "upload_destination_fallback",
        "upload_destination_path_fallback",
        "interval_ms",
        "upload_destination_uri_fallback",
    )
    WATCH_DIRECTORY_SUBPATH_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_DESTINATION_FALLBACK_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_DESTINATION_PATH_FALLBACK_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_MS_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_DESTINATION_URI_FALLBACK_FIELD_NUMBER: _ClassVar[int]
    watch_directory_subpath: str
    upload_destination_fallback: str
    upload_destination_path_fallback: str
    interval_ms: int
    upload_destination_uri_fallback: str
    def __init__(
        self,
        watch_directory_subpath: _Optional[str] = ...,
        upload_destination_fallback: _Optional[str] = ...,
        upload_destination_path_fallback: _Optional[str] = ...,
        interval_ms: _Optional[int] = ...,
        upload_destination_uri_fallback: _Optional[str] = ...,
    ) -> None: ...

class StreamedDirectoryWatcherSpec(_message.Message):
    __slots__ = (
        "watch_directory_subpath",
        "interval_ms",
        "upload_destination_path_fallback",
        "upload_destination_uri_fallback",
        "idle_file_timeout_ms",
    )
    WATCH_DIRECTORY_SUBPATH_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_MS_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_DESTINATION_PATH_FALLBACK_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_DESTINATION_URI_FALLBACK_FIELD_NUMBER: _ClassVar[int]
    IDLE_FILE_TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    watch_directory_subpath: str
    interval_ms: int
    upload_destination_path_fallback: str
    upload_destination_uri_fallback: str
    idle_file_timeout_ms: int
    def __init__(
        self,
        watch_directory_subpath: _Optional[str] = ...,
        interval_ms: _Optional[int] = ...,
        upload_destination_path_fallback: _Optional[str] = ...,
        upload_destination_uri_fallback: _Optional[str] = ...,
        idle_file_timeout_ms: _Optional[int] = ...,
    ) -> None: ...

class NetworkInspectorDaemonSpec(_message.Message):
    __slots__ = (
        "export_to",
        "bucket_subdirectory",
        "interface",
        "filter_expression",
        "snaplen_bytes",
        "trigger",
        "commit_interval_seconds",
    )
    EXPORT_TO_FIELD_NUMBER: _ClassVar[int]
    BUCKET_SUBDIRECTORY_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    FILTER_EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    SNAPLEN_BYTES_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    COMMIT_INTERVAL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    export_to: str
    bucket_subdirectory: str
    interface: str
    filter_expression: str
    snaplen_bytes: int
    trigger: NetworkInspectorTrigger
    commit_interval_seconds: int
    def __init__(
        self,
        export_to: _Optional[str] = ...,
        bucket_subdirectory: _Optional[str] = ...,
        interface: _Optional[str] = ...,
        filter_expression: _Optional[str] = ...,
        snaplen_bytes: _Optional[int] = ...,
        trigger: _Optional[_Union[NetworkInspectorTrigger, str]] = ...,
        commit_interval_seconds: _Optional[int] = ...,
    ) -> None: ...

class ObservabilityDaemonSpec(_message.Message):
    __slots__ = (
        "keep_running_when_suspended",
        "request",
        "limit",
        "image_override",
        "scheduling",
        "zombie_killer",
        "core_dump_collector",
        "py_spy_stack_trace_collector",
        "perf_collector",
        "perfetto_daemon",
        "directory_watcher",
        "streamed_watcher",
        "network_inspector_daemon",
    )
    KEEP_RUNNING_WHEN_SUSPENDED_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    IMAGE_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    SCHEDULING_FIELD_NUMBER: _ClassVar[int]
    ZOMBIE_KILLER_FIELD_NUMBER: _ClassVar[int]
    CORE_DUMP_COLLECTOR_FIELD_NUMBER: _ClassVar[int]
    PY_SPY_STACK_TRACE_COLLECTOR_FIELD_NUMBER: _ClassVar[int]
    PERF_COLLECTOR_FIELD_NUMBER: _ClassVar[int]
    PERFETTO_DAEMON_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_WATCHER_FIELD_NUMBER: _ClassVar[int]
    STREAMED_WATCHER_FIELD_NUMBER: _ClassVar[int]
    NETWORK_INSPECTOR_DAEMON_FIELD_NUMBER: _ClassVar[int]
    keep_running_when_suspended: bool
    request: KubeResourceConfig
    limit: KubeResourceConfig
    image_override: str
    scheduling: ObservabilityDaemonSchedulingSpec
    zombie_killer: ZombieKillerSpec
    core_dump_collector: CoreDumpCollectorSpec
    py_spy_stack_trace_collector: PySpyStackTraceCollectorSpec
    perf_collector: PerfCollectorSpec
    perfetto_daemon: PerfettoDaemonSpec
    directory_watcher: DirectoryWatcherSpec
    streamed_watcher: StreamedDirectoryWatcherSpec
    network_inspector_daemon: NetworkInspectorDaemonSpec
    def __init__(
        self,
        keep_running_when_suspended: bool = ...,
        request: _Optional[_Union[KubeResourceConfig, _Mapping]] = ...,
        limit: _Optional[_Union[KubeResourceConfig, _Mapping]] = ...,
        image_override: _Optional[str] = ...,
        scheduling: _Optional[_Union[ObservabilityDaemonSchedulingSpec, _Mapping]] = ...,
        zombie_killer: _Optional[_Union[ZombieKillerSpec, _Mapping]] = ...,
        core_dump_collector: _Optional[_Union[CoreDumpCollectorSpec, _Mapping]] = ...,
        py_spy_stack_trace_collector: _Optional[_Union[PySpyStackTraceCollectorSpec, _Mapping]] = ...,
        perf_collector: _Optional[_Union[PerfCollectorSpec, _Mapping]] = ...,
        perfetto_daemon: _Optional[_Union[PerfettoDaemonSpec, _Mapping]] = ...,
        directory_watcher: _Optional[_Union[DirectoryWatcherSpec, _Mapping]] = ...,
        streamed_watcher: _Optional[_Union[StreamedDirectoryWatcherSpec, _Mapping]] = ...,
        network_inspector_daemon: _Optional[_Union[NetworkInspectorDaemonSpec, _Mapping]] = ...,
    ) -> None: ...

class ObservabilityDaemonSchedulingSpec(_message.Message):
    __slots__ = ("node_selectors",)
    NODE_SELECTORS_FIELD_NUMBER: _ClassVar[int]
    node_selectors: _containers.RepeatedCompositeFieldContainer[KubeNodeSelector]
    def __init__(self, node_selectors: _Optional[_Iterable[_Union[KubeNodeSelector, _Mapping]]] = ...) -> None: ...

class TelemetryDeploymentSpec(_message.Message):
    __slots__ = (
        "namespace",
        "click_house",
        "otel",
        "node_selectors",
        "dns_name_override",
        "aggregator",
        "observability_daemons",
        "customer_collector",
        "require_infrastructure_nodepool",
        "gpu_telemetry",
        "telemetry_runtime",
        "vector_cluster_metrics",
        "victoria_metrics",
        "ingest_metrics",
        "vector_statsd",
        "metric_exports",
        "customer_vector_aggregator",
        "prometheus_collection_runtime",
    )
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    CLICK_HOUSE_FIELD_NUMBER: _ClassVar[int]
    OTEL_FIELD_NUMBER: _ClassVar[int]
    NODE_SELECTORS_FIELD_NUMBER: _ClassVar[int]
    DNS_NAME_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    AGGREGATOR_FIELD_NUMBER: _ClassVar[int]
    OBSERVABILITY_DAEMONS_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_COLLECTOR_FIELD_NUMBER: _ClassVar[int]
    REQUIRE_INFRASTRUCTURE_NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    GPU_TELEMETRY_FIELD_NUMBER: _ClassVar[int]
    TELEMETRY_RUNTIME_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLUSTER_METRICS_FIELD_NUMBER: _ClassVar[int]
    VICTORIA_METRICS_FIELD_NUMBER: _ClassVar[int]
    INGEST_METRICS_FIELD_NUMBER: _ClassVar[int]
    VECTOR_STATSD_FIELD_NUMBER: _ClassVar[int]
    METRIC_EXPORTS_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_VECTOR_AGGREGATOR_FIELD_NUMBER: _ClassVar[int]
    PROMETHEUS_COLLECTION_RUNTIME_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    click_house: ClickHouseSpec
    otel: OtelCollectorSpec
    node_selectors: _containers.RepeatedCompositeFieldContainer[KubeNodeSelector]
    dns_name_override: str
    aggregator: AggregatorSpec
    observability_daemons: _containers.RepeatedCompositeFieldContainer[ObservabilityDaemonSpec]
    customer_collector: CustomerCollectorConfig
    require_infrastructure_nodepool: bool
    gpu_telemetry: GpuTelemetrySpec
    telemetry_runtime: TelemetryRuntime
    vector_cluster_metrics: VectorClusterMetricsSpec
    victoria_metrics: VictoriaMetricsSpec
    ingest_metrics: TelemetryIngestMetricsSpec
    vector_statsd: VectorStatsdSpec
    metric_exports: MetricExportSpec
    customer_vector_aggregator: CustomerVectorAggregatorConfig
    prometheus_collection_runtime: TelemetryPrometheusCollectionRuntime
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        click_house: _Optional[_Union[ClickHouseSpec, _Mapping]] = ...,
        otel: _Optional[_Union[OtelCollectorSpec, _Mapping]] = ...,
        node_selectors: _Optional[_Iterable[_Union[KubeNodeSelector, _Mapping]]] = ...,
        dns_name_override: _Optional[str] = ...,
        aggregator: _Optional[_Union[AggregatorSpec, _Mapping]] = ...,
        observability_daemons: _Optional[_Iterable[_Union[ObservabilityDaemonSpec, _Mapping]]] = ...,
        customer_collector: _Optional[_Union[CustomerCollectorConfig, _Mapping]] = ...,
        require_infrastructure_nodepool: bool = ...,
        gpu_telemetry: _Optional[_Union[GpuTelemetrySpec, _Mapping]] = ...,
        telemetry_runtime: _Optional[_Union[TelemetryRuntime, str]] = ...,
        vector_cluster_metrics: _Optional[_Union[VectorClusterMetricsSpec, _Mapping]] = ...,
        victoria_metrics: _Optional[_Union[VictoriaMetricsSpec, _Mapping]] = ...,
        ingest_metrics: _Optional[_Union[TelemetryIngestMetricsSpec, _Mapping]] = ...,
        vector_statsd: _Optional[_Union[VectorStatsdSpec, _Mapping]] = ...,
        metric_exports: _Optional[_Union[MetricExportSpec, _Mapping]] = ...,
        customer_vector_aggregator: _Optional[_Union[CustomerVectorAggregatorConfig, _Mapping]] = ...,
        prometheus_collection_runtime: _Optional[_Union[TelemetryPrometheusCollectionRuntime, str]] = ...,
    ) -> None: ...

class TelemetryDeployment(_message.Message):
    __slots__ = ("id", "spec", "created_at", "updated_at", "cluster_id", "suspended_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    SUSPENDED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    spec: TelemetryDeploymentSpec
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    cluster_id: str
    suspended_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        spec: _Optional[_Union[TelemetryDeploymentSpec, _Mapping]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        cluster_id: _Optional[str] = ...,
        suspended_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ClusterIdentifier(_message.Message):
    __slots__ = ("cluster_id", "namespace")
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    namespace: str
    def __init__(self, cluster_id: _Optional[str] = ..., namespace: _Optional[str] = ...) -> None: ...

class GetTelemetryDeploymentRequest(_message.Message):
    __slots__ = ("cluster_id", "namespace", "cluster_identifier", "telemetry_id", "by_environment")
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    TELEMETRY_ID_FIELD_NUMBER: _ClassVar[int]
    BY_ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    namespace: str
    cluster_identifier: ClusterIdentifier
    telemetry_id: str
    by_environment: bool
    def __init__(
        self,
        cluster_id: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        cluster_identifier: _Optional[_Union[ClusterIdentifier, _Mapping]] = ...,
        telemetry_id: _Optional[str] = ...,
        by_environment: bool = ...,
    ) -> None: ...

class GetTelemetryDeploymentResponse(_message.Message):
    __slots__ = ("deployment",)
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    deployment: TelemetryDeployment
    def __init__(self, deployment: _Optional[_Union[TelemetryDeployment, _Mapping]] = ...) -> None: ...

class ListTelemetryDeploymentsRequest(_message.Message):
    __slots__ = ("cluster_id",)
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class ListTelemetryDeploymentsResponse(_message.Message):
    __slots__ = ("deployments",)
    DEPLOYMENTS_FIELD_NUMBER: _ClassVar[int]
    deployments: _containers.RepeatedCompositeFieldContainer[TelemetryDeployment]
    def __init__(self, deployments: _Optional[_Iterable[_Union[TelemetryDeployment, _Mapping]]] = ...) -> None: ...

class CreateTelemetryDeploymentRequest(_message.Message):
    __slots__ = ("cluster_id", "spec", "telemetry_deployment_id")
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    TELEMETRY_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    spec: TelemetryDeploymentSpec
    telemetry_deployment_id: str
    def __init__(
        self,
        cluster_id: _Optional[str] = ...,
        spec: _Optional[_Union[TelemetryDeploymentSpec, _Mapping]] = ...,
        telemetry_deployment_id: _Optional[str] = ...,
    ) -> None: ...

class CreateTelemetryDeploymentResponse(_message.Message):
    __slots__ = ("telemetry_deployment_id",)
    TELEMETRY_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    telemetry_deployment_id: str
    def __init__(self, telemetry_deployment_id: _Optional[str] = ...) -> None: ...

class DeleteTelemetryDeploymentRequest(_message.Message):
    __slots__ = ("cluster_id", "namespace")
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    namespace: str
    def __init__(self, cluster_id: _Optional[str] = ..., namespace: _Optional[str] = ...) -> None: ...

class DeleteTelemetryDeploymentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpdateTelemetryDeploymentRequest(_message.Message):
    __slots__ = ("telemetry_deployment_id", "spec", "suspended", "update_mask")
    TELEMETRY_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    SUSPENDED_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    telemetry_deployment_id: str
    spec: TelemetryDeploymentSpec
    suspended: bool
    update_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        telemetry_deployment_id: _Optional[str] = ...,
        spec: _Optional[_Union[TelemetryDeploymentSpec, _Mapping]] = ...,
        suspended: bool = ...,
        update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class UpdateTelemetryDeploymentResponse(_message.Message):
    __slots__ = ("deployment",)
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    deployment: TelemetryDeployment
    def __init__(self, deployment: _Optional[_Union[TelemetryDeployment, _Mapping]] = ...) -> None: ...

class MigrateTelemetryDeploymentRequest(_message.Message):
    __slots__ = ("telemetry_deployment_id", "migration_image")
    TELEMETRY_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    MIGRATION_IMAGE_FIELD_NUMBER: _ClassVar[int]
    telemetry_deployment_id: str
    migration_image: str
    def __init__(
        self, telemetry_deployment_id: _Optional[str] = ..., migration_image: _Optional[str] = ...
    ) -> None: ...

class MigrateTelemetryDeploymentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetSearchConfigRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetSearchConfigResponse(_message.Message):
    __slots__ = ("team_id", "team_api_key")
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_API_KEY_FIELD_NUMBER: _ClassVar[int]
    team_id: str
    team_api_key: str
    def __init__(self, team_id: _Optional[str] = ..., team_api_key: _Optional[str] = ...) -> None: ...

class UpdateEnvironmentVariablesRequest(_message.Message):
    __slots__ = ("environment_variables",)
    class EnvironmentVariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    ENVIRONMENT_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    environment_variables: _containers.ScalarMap[str, str]
    def __init__(self, environment_variables: _Optional[_Mapping[str, str]] = ...) -> None: ...

class UpdateEnvironmentVariablesResponse(_message.Message):
    __slots__ = ("field_changes",)
    FIELD_CHANGES_FIELD_NUMBER: _ClassVar[int]
    field_changes: _containers.RepeatedCompositeFieldContainer[_field_change_pb2.FieldChange]
    def __init__(
        self, field_changes: _Optional[_Iterable[_Union[_field_change_pb2.FieldChange, _Mapping]]] = ...
    ) -> None: ...

class StartBranchRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StartBranchResponse(_message.Message):
    __slots__ = ("state",)
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: BranchScalingState
    def __init__(self, state: _Optional[_Union[BranchScalingState, str]] = ...) -> None: ...

class ScaleBranchRequest(_message.Message):
    __slots__ = ("replicas",)
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    def __init__(self, replicas: _Optional[int] = ...) -> None: ...

class ScaleBranchResponse(_message.Message):
    __slots__ = ("state",)
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: BranchScalingState
    def __init__(self, state: _Optional[_Union[BranchScalingState, str]] = ...) -> None: ...

class GetBranchProfileRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBranchProfileResponse(_message.Message):
    __slots__ = ("environment_id", "deployment_id", "base_image_sha", "supports_remote_graph_validation")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    BASE_IMAGE_SHA_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_REMOTE_GRAPH_VALIDATION_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    deployment_id: str
    base_image_sha: str
    supports_remote_graph_validation: bool
    def __init__(
        self,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        base_image_sha: _Optional[str] = ...,
        supports_remote_graph_validation: bool = ...,
    ) -> None: ...

class GetBranchServerStatusRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBranchServerStatusResponse(_message.Message):
    __slots__ = ("status", "available_replicas", "ready_replicas", "replicas")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    READY_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    status: BranchServerStatus
    available_replicas: int
    ready_replicas: int
    replicas: int
    def __init__(
        self,
        status: _Optional[_Union[BranchServerStatus, str]] = ...,
        available_replicas: _Optional[int] = ...,
        ready_replicas: _Optional[int] = ...,
        replicas: _Optional[int] = ...,
    ) -> None: ...

class KafkaTopic(_message.Message):
    __slots__ = ("name", "partitions", "replication", "retention_ms")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PARTITIONS_FIELD_NUMBER: _ClassVar[int]
    REPLICATION_FIELD_NUMBER: _ClassVar[int]
    RETENTION_MS_FIELD_NUMBER: _ClassVar[int]
    name: str
    partitions: int
    replication: int
    retention_ms: int
    def __init__(
        self,
        name: _Optional[str] = ...,
        partitions: _Optional[int] = ...,
        replication: _Optional[int] = ...,
        retention_ms: _Optional[int] = ...,
    ) -> None: ...

class CreateKafkaTopicsRequest(_message.Message):
    __slots__ = ("topics",)
    TOPICS_FIELD_NUMBER: _ClassVar[int]
    topics: _containers.RepeatedCompositeFieldContainer[KafkaTopic]
    def __init__(self, topics: _Optional[_Iterable[_Union[KafkaTopic, _Mapping]]] = ...) -> None: ...

class CreateKafkaTopicsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetKafkaTopicsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetKafkaTopicsResponse(_message.Message):
    __slots__ = ("topics",)
    TOPICS_FIELD_NUMBER: _ClassVar[int]
    topics: _containers.RepeatedCompositeFieldContainer[KafkaTopic]
    def __init__(self, topics: _Optional[_Iterable[_Union[KafkaTopic, _Mapping]]] = ...) -> None: ...

class GetNodepoolsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetNodepoolsResponse(_message.Message):
    __slots__ = ("karpenter_nodepools", "gke_nodepools")
    KARPENTER_NODEPOOLS_FIELD_NUMBER: _ClassVar[int]
    GKE_NODEPOOLS_FIELD_NUMBER: _ClassVar[int]
    karpenter_nodepools: _containers.RepeatedCompositeFieldContainer[_karpenter_pb2.KarpenterNodepool]
    gke_nodepools: _containers.RepeatedCompositeFieldContainer[_gke_pb2.GKENodePool]
    def __init__(
        self,
        karpenter_nodepools: _Optional[_Iterable[_Union[_karpenter_pb2.KarpenterNodepool, _Mapping]]] = ...,
        gke_nodepools: _Optional[_Iterable[_Union[_gke_pb2.GKENodePool, _Mapping]]] = ...,
    ) -> None: ...

class ChalkMachineTypeMapping(_message.Message):
    __slots__ = ("cloud", "machine_type", "workload_type", "spilling", "gpu", "instance_type", "cpus", "memory_gb")
    CLOUD_FIELD_NUMBER: _ClassVar[int]
    MACHINE_TYPE_FIELD_NUMBER: _ClassVar[int]
    WORKLOAD_TYPE_FIELD_NUMBER: _ClassVar[int]
    SPILLING_FIELD_NUMBER: _ClassVar[int]
    GPU_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CPUS_FIELD_NUMBER: _ClassVar[int]
    MEMORY_GB_FIELD_NUMBER: _ClassVar[int]
    cloud: _rate_pb2.BillingCloud
    machine_type: str
    workload_type: str
    spilling: bool
    gpu: bool
    instance_type: str
    cpus: float
    memory_gb: float
    def __init__(
        self,
        cloud: _Optional[_Union[_rate_pb2.BillingCloud, str]] = ...,
        machine_type: _Optional[str] = ...,
        workload_type: _Optional[str] = ...,
        spilling: bool = ...,
        gpu: bool = ...,
        instance_type: _Optional[str] = ...,
        cpus: _Optional[float] = ...,
        memory_gb: _Optional[float] = ...,
    ) -> None: ...

class GetAvailableChalkMachineTypesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAvailableChalkMachineTypesResponse(_message.Message):
    __slots__ = ("mappings",)
    MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    mappings: _containers.RepeatedCompositeFieldContainer[ChalkMachineTypeMapping]
    def __init__(self, mappings: _Optional[_Iterable[_Union[ChalkMachineTypeMapping, _Mapping]]] = ...) -> None: ...

class AddNodepoolRequest(_message.Message):
    __slots__ = ("karpenter_nodepool", "gke_nodepool")
    KARPENTER_NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    GKE_NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    karpenter_nodepool: _karpenter_pb2.KarpenterNodepool
    gke_nodepool: _gke_pb2.GKENodePool
    def __init__(
        self,
        karpenter_nodepool: _Optional[_Union[_karpenter_pb2.KarpenterNodepool, _Mapping]] = ...,
        gke_nodepool: _Optional[_Union[_gke_pb2.GKENodePool, _Mapping]] = ...,
    ) -> None: ...

class AddNodepoolResponse(_message.Message):
    __slots__ = ("karpenter_nodepool", "gke_nodepool")
    KARPENTER_NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    GKE_NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    karpenter_nodepool: _karpenter_pb2.KarpenterNodepool
    gke_nodepool: _gke_pb2.GKENodePool
    def __init__(
        self,
        karpenter_nodepool: _Optional[_Union[_karpenter_pb2.KarpenterNodepool, _Mapping]] = ...,
        gke_nodepool: _Optional[_Union[_gke_pb2.GKENodePool, _Mapping]] = ...,
    ) -> None: ...

class UpdateNodepoolRequest(_message.Message):
    __slots__ = ("name", "gke_nodepool", "karpenter_nodepool")
    NAME_FIELD_NUMBER: _ClassVar[int]
    GKE_NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    KARPENTER_NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    name: str
    gke_nodepool: _gke_pb2.GKENodePool
    karpenter_nodepool: _karpenter_pb2.KarpenterNodepool
    def __init__(
        self,
        name: _Optional[str] = ...,
        gke_nodepool: _Optional[_Union[_gke_pb2.GKENodePool, _Mapping]] = ...,
        karpenter_nodepool: _Optional[_Union[_karpenter_pb2.KarpenterNodepool, _Mapping]] = ...,
    ) -> None: ...

class UpdateNodepoolResponse(_message.Message):
    __slots__ = ("karpenter_nodepool", "gke_nodepool")
    KARPENTER_NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    GKE_NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    karpenter_nodepool: _karpenter_pb2.KarpenterNodepool
    gke_nodepool: _gke_pb2.GKENodePool
    def __init__(
        self,
        karpenter_nodepool: _Optional[_Union[_karpenter_pb2.KarpenterNodepool, _Mapping]] = ...,
        gke_nodepool: _Optional[_Union[_gke_pb2.GKENodePool, _Mapping]] = ...,
    ) -> None: ...

class DeleteNodepoolRequest(_message.Message):
    __slots__ = ("name", "cluster")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_FIELD_NUMBER: _ClassVar[int]
    name: str
    cluster: str
    def __init__(self, name: _Optional[str] = ..., cluster: _Optional[str] = ...) -> None: ...

class DeleteNodepoolResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetKarpenterNodepoolsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetKarpenterNodepoolsResponse(_message.Message):
    __slots__ = ("nodepools",)
    NODEPOOLS_FIELD_NUMBER: _ClassVar[int]
    nodepools: _containers.RepeatedCompositeFieldContainer[_karpenter_pb2.KarpenterNodepool]
    def __init__(
        self, nodepools: _Optional[_Iterable[_Union[_karpenter_pb2.KarpenterNodepool, _Mapping]]] = ...
    ) -> None: ...

class AddKarpenterNodepoolRequest(_message.Message):
    __slots__ = ("nodepool",)
    NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    nodepool: _karpenter_pb2.KarpenterNodepool
    def __init__(self, nodepool: _Optional[_Union[_karpenter_pb2.KarpenterNodepool, _Mapping]] = ...) -> None: ...

class AddKarpenterNodepoolResponse(_message.Message):
    __slots__ = ("nodepool",)
    NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    nodepool: _karpenter_pb2.KarpenterNodepool
    def __init__(self, nodepool: _Optional[_Union[_karpenter_pb2.KarpenterNodepool, _Mapping]] = ...) -> None: ...

class UpdateKarpenterNodepoolRequest(_message.Message):
    __slots__ = ("name", "nodepool")
    NAME_FIELD_NUMBER: _ClassVar[int]
    NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    name: str
    nodepool: _karpenter_pb2.KarpenterNodepool
    def __init__(
        self, name: _Optional[str] = ..., nodepool: _Optional[_Union[_karpenter_pb2.KarpenterNodepool, _Mapping]] = ...
    ) -> None: ...

class UpdateKarpenterNodepoolResponse(_message.Message):
    __slots__ = ("nodepool",)
    NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    nodepool: _karpenter_pb2.KarpenterNodepool
    def __init__(self, nodepool: _Optional[_Union[_karpenter_pb2.KarpenterNodepool, _Mapping]] = ...) -> None: ...

class DeleteKarpenterNodepoolRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class DeleteKarpenterNodepoolResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetKarpenterInstallationMetadataRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetKarpenterInstallationMetadataResponse(_message.Message):
    __slots__ = ("deployment_labels",)
    class DeploymentLabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    DEPLOYMENT_LABELS_FIELD_NUMBER: _ClassVar[int]
    deployment_labels: _containers.ScalarMap[str, str]
    def __init__(self, deployment_labels: _Optional[_Mapping[str, str]] = ...) -> None: ...

class CreateEnvironmentCloudResourcesRequest(_message.Message):
    __slots__ = ("environment_id",)
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    def __init__(self, environment_id: _Optional[str] = ...) -> None: ...

class CreateEnvironmentCloudResourcesResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteEnvironmentCloudResourcesRequest(_message.Message):
    __slots__ = ("environment_id",)
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    def __init__(self, environment_id: _Optional[str] = ...) -> None: ...

class DeleteEnvironmentCloudResourcesResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeploymentTag(_message.Message):
    __slots__ = ("tag", "weight", "deployment_id", "mirror_weight")
    TAG_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    MIRROR_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    tag: str
    weight: int
    deployment_id: str
    mirror_weight: int
    def __init__(
        self,
        tag: _Optional[str] = ...,
        weight: _Optional[int] = ...,
        deployment_id: _Optional[str] = ...,
        mirror_weight: _Optional[int] = ...,
    ) -> None: ...

class GetTagWeightsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetTagWeightsResponse(_message.Message):
    __slots__ = ("tags",)
    TAGS_FIELD_NUMBER: _ClassVar[int]
    tags: _containers.RepeatedCompositeFieldContainer[DeploymentTag]
    def __init__(self, tags: _Optional[_Iterable[_Union[DeploymentTag, _Mapping]]] = ...) -> None: ...

class SetTagWeightsRequest(_message.Message):
    __slots__ = ("tags",)
    TAGS_FIELD_NUMBER: _ClassVar[int]
    tags: _containers.RepeatedCompositeFieldContainer[DeploymentTag]
    def __init__(self, tags: _Optional[_Iterable[_Union[DeploymentTag, _Mapping]]] = ...) -> None: ...

class SetTagWeightsResponse(_message.Message):
    __slots__ = ("tags",)
    TAGS_FIELD_NUMBER: _ClassVar[int]
    tags: _containers.RepeatedCompositeFieldContainer[DeploymentTag]
    def __init__(self, tags: _Optional[_Iterable[_Union[DeploymentTag, _Mapping]]] = ...) -> None: ...

class RequirementsFile(_message.Message):
    __slots__ = ("filename", "contents")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    CONTENTS_FIELD_NUMBER: _ClassVar[int]
    filename: str
    contents: str
    def __init__(self, filename: _Optional[str] = ..., contents: _Optional[str] = ...) -> None: ...

class CreateDeploymentRequest(_message.Message):
    __slots__ = (
        "git_branch",
        "git_commit",
        "git_pr",
        "git_author",
        "git_tag",
        "branch",
        "requirements",
        "customer_deployment_tags",
        "project_settings",
        "customer_metadata",
        "display_description",
        "build_options",
    )
    class CustomerMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class BuildOptionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    GIT_BRANCH_FIELD_NUMBER: _ClassVar[int]
    GIT_COMMIT_FIELD_NUMBER: _ClassVar[int]
    GIT_PR_FIELD_NUMBER: _ClassVar[int]
    GIT_AUTHOR_FIELD_NUMBER: _ClassVar[int]
    GIT_TAG_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_DEPLOYMENT_TAGS_FIELD_NUMBER: _ClassVar[int]
    PROJECT_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_METADATA_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    BUILD_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    git_branch: str
    git_commit: str
    git_pr: str
    git_author: str
    git_tag: str
    branch: str
    requirements: _containers.RepeatedCompositeFieldContainer[RequirementsFile]
    customer_deployment_tags: _containers.RepeatedScalarFieldContainer[str]
    project_settings: _export_pb2.ProjectSettings
    customer_metadata: _containers.ScalarMap[str, str]
    display_description: str
    build_options: _containers.ScalarMap[str, str]
    def __init__(
        self,
        git_branch: _Optional[str] = ...,
        git_commit: _Optional[str] = ...,
        git_pr: _Optional[str] = ...,
        git_author: _Optional[str] = ...,
        git_tag: _Optional[str] = ...,
        branch: _Optional[str] = ...,
        requirements: _Optional[_Iterable[_Union[RequirementsFile, _Mapping]]] = ...,
        customer_deployment_tags: _Optional[_Iterable[str]] = ...,
        project_settings: _Optional[_Union[_export_pb2.ProjectSettings, _Mapping]] = ...,
        customer_metadata: _Optional[_Mapping[str, str]] = ...,
        display_description: _Optional[str] = ...,
        build_options: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class CreateDeploymentResponse(_message.Message):
    __slots__ = ("deployment_id",)
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    def __init__(self, deployment_id: _Optional[str] = ...) -> None: ...

class KubernetesCluster(_message.Message):
    __slots__ = ("id", "name", "cloud_credentials", "cluster_gateway", "cluster_background_persistence")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CLOUD_CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_GATEWAY_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_BACKGROUND_PERSISTENCE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    cloud_credentials: _environment_pb2.CloudConfig
    cluster_gateway: EnvoyGatewaySpecs
    cluster_background_persistence: BackgroundPersistenceDeploymentSpecs
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        cloud_credentials: _Optional[_Union[_environment_pb2.CloudConfig, _Mapping]] = ...,
        cluster_gateway: _Optional[_Union[EnvoyGatewaySpecs, _Mapping]] = ...,
        cluster_background_persistence: _Optional[_Union[BackgroundPersistenceDeploymentSpecs, _Mapping]] = ...,
    ) -> None: ...

class GetEnvironmentKubeClustersRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetEnvironmentKubeClustersResponse(_message.Message):
    __slots__ = ("clusters",)
    CLUSTERS_FIELD_NUMBER: _ClassVar[int]
    clusters: _containers.RepeatedCompositeFieldContainer[KubernetesCluster]
    def __init__(self, clusters: _Optional[_Iterable[_Union[KubernetesCluster, _Mapping]]] = ...) -> None: ...

class SuspendEnvironmentRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SuspendEnvironmentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ResumeEnvironmentRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ResumeEnvironmentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SuspendClusterGatewayRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SuspendClusterGatewayResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ResumeClusterGatewayRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ResumeClusterGatewayResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SuspendClusterBackgroundPersistenceRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SuspendClusterBackgroundPersistenceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ResumeClusterBackgroundPersistenceRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ResumeClusterBackgroundPersistenceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteClusterGatewayRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteClusterGatewayResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteClusterBackgroundPersistenceRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteClusterBackgroundPersistenceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StreamingKafkaKedaConfig(_message.Message):
    __slots__ = (
        "resolver_fqn",
        "source_name",
        "integration_id",
        "resource_group",
        "enabled",
        "lag_threshold",
        "min_instances",
        "max_instances",
        "topic",
        "consumer_group",
    )
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    SOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    LAG_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    MIN_INSTANCES_FIELD_NUMBER: _ClassVar[int]
    MAX_INSTANCES_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_GROUP_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    source_name: str
    integration_id: str
    resource_group: str
    enabled: bool
    lag_threshold: int
    min_instances: int
    max_instances: int
    topic: str
    consumer_group: str
    def __init__(
        self,
        resolver_fqn: _Optional[str] = ...,
        source_name: _Optional[str] = ...,
        integration_id: _Optional[str] = ...,
        resource_group: _Optional[str] = ...,
        enabled: bool = ...,
        lag_threshold: _Optional[int] = ...,
        min_instances: _Optional[int] = ...,
        max_instances: _Optional[int] = ...,
        topic: _Optional[str] = ...,
        consumer_group: _Optional[str] = ...,
    ) -> None: ...

class ListStreamingKafkaKedaConfigsRequest(_message.Message):
    __slots__ = ("integration_id", "source_name", "deployment_id", "resolver_fqn")
    INTEGRATION_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    integration_id: str
    source_name: str
    deployment_id: str
    resolver_fqn: str
    def __init__(
        self,
        integration_id: _Optional[str] = ...,
        source_name: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        resolver_fqn: _Optional[str] = ...,
    ) -> None: ...

class ListStreamingKafkaKedaConfigsResponse(_message.Message):
    __slots__ = ("configs",)
    CONFIGS_FIELD_NUMBER: _ClassVar[int]
    configs: _containers.RepeatedCompositeFieldContainer[StreamingKafkaKedaConfig]
    def __init__(self, configs: _Optional[_Iterable[_Union[StreamingKafkaKedaConfig, _Mapping]]] = ...) -> None: ...

class UpdateStreamingKafkaKedaConfigRequest(_message.Message):
    __slots__ = (
        "resolver_fqn",
        "integration_id",
        "source_name",
        "enabled",
        "lag_threshold",
        "min_instances",
        "max_instances",
        "deployment_id",
    )
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    LAG_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    MIN_INSTANCES_FIELD_NUMBER: _ClassVar[int]
    MAX_INSTANCES_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    integration_id: str
    source_name: str
    enabled: bool
    lag_threshold: int
    min_instances: int
    max_instances: int
    deployment_id: str
    def __init__(
        self,
        resolver_fqn: _Optional[str] = ...,
        integration_id: _Optional[str] = ...,
        source_name: _Optional[str] = ...,
        enabled: bool = ...,
        lag_threshold: _Optional[int] = ...,
        min_instances: _Optional[int] = ...,
        max_instances: _Optional[int] = ...,
        deployment_id: _Optional[str] = ...,
    ) -> None: ...

class UpdateStreamingKafkaKedaConfigResponse(_message.Message):
    __slots__ = ("config",)
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: StreamingKafkaKedaConfig
    def __init__(self, config: _Optional[_Union[StreamingKafkaKedaConfig, _Mapping]] = ...) -> None: ...
