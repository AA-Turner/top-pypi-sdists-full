from chalk._gen.buf.validate import validate_pb2 as _validate_pb2
from chalk._gen.chalk.server.v1 import cloud_components_pb2 as _cloud_components_pb2
from google.protobuf import duration_pb2 as _duration_pb2
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

class ClusterHealthCheckName(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLUSTER_HEALTH_CHECK_NAME_UNSPECIFIED: _ClassVar[ClusterHealthCheckName]
    CLUSTER_HEALTH_CHECK_NAME_KUBERNETES_API_ACCESS: _ClassVar[ClusterHealthCheckName]
    CLUSTER_HEALTH_CHECK_NAME_DATAPLANE_API_SERVER_NAMESPACE: _ClassVar[ClusterHealthCheckName]
    CLUSTER_HEALTH_CHECK_NAME_DATAPLANE_CONTROLLER_NAMESPACE: _ClassVar[ClusterHealthCheckName]
    CLUSTER_HEALTH_CHECK_NAME_TELEMETRY_NAMESPACE: _ClassVar[ClusterHealthCheckName]
    CLUSTER_HEALTH_CHECK_NAME_DATAPLANE_API_SERVER_IDENTITY: _ClassVar[ClusterHealthCheckName]
    CLUSTER_HEALTH_CHECK_NAME_ENVOY_GATEWAY: _ClassVar[ClusterHealthCheckName]
    CLUSTER_HEALTH_CHECK_NAME_CERT_MANAGER: _ClassVar[ClusterHealthCheckName]
    CLUSTER_HEALTH_CHECK_NAME_EXTERNAL_DNS: _ClassVar[ClusterHealthCheckName]
    CLUSTER_HEALTH_CHECK_NAME_CLUSTER_ISSUERS: _ClassVar[ClusterHealthCheckName]
    CLUSTER_HEALTH_CHECK_NAME_DNS_ZONES: _ClassVar[ClusterHealthCheckName]
    CLUSTER_HEALTH_CHECK_NAME_KEDA: _ClassVar[ClusterHealthCheckName]
    CLUSTER_HEALTH_CHECK_NAME_VICTORIA_METRICS_OPERATOR: _ClassVar[ClusterHealthCheckName]
    CLUSTER_HEALTH_CHECK_NAME_KUBE_STATE_METRICS: _ClassVar[ClusterHealthCheckName]

class ClusterHealthStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLUSTER_HEALTH_STATUS_UNSPECIFIED: _ClassVar[ClusterHealthStatus]
    CLUSTER_HEALTH_STATUS_OK: _ClassVar[ClusterHealthStatus]
    CLUSTER_HEALTH_STATUS_WARNING: _ClassVar[ClusterHealthStatus]
    CLUSTER_HEALTH_STATUS_FAILING: _ClassVar[ClusterHealthStatus]
    CLUSTER_HEALTH_STATUS_NOT_CONFIGURED: _ClassVar[ClusterHealthStatus]

class ClusterDiagnosticSeverity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLUSTER_DIAGNOSTIC_SEVERITY_UNSPECIFIED: _ClassVar[ClusterDiagnosticSeverity]
    CLUSTER_DIAGNOSTIC_SEVERITY_INFORMATION: _ClassVar[ClusterDiagnosticSeverity]
    CLUSTER_DIAGNOSTIC_SEVERITY_WARNING: _ClassVar[ClusterDiagnosticSeverity]
    CLUSTER_DIAGNOSTIC_SEVERITY_ERROR: _ClassVar[ClusterDiagnosticSeverity]

class ClusterDiagnosticOwner(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLUSTER_DIAGNOSTIC_OWNER_UNSPECIFIED: _ClassVar[ClusterDiagnosticOwner]
    CLUSTER_DIAGNOSTIC_OWNER_CHALK: _ClassVar[ClusterDiagnosticOwner]
    CLUSTER_DIAGNOSTIC_OWNER_CUSTOMER: _ClassVar[ClusterDiagnosticOwner]

class ClusterRequirementKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLUSTER_REQUIREMENT_KIND_UNSPECIFIED: _ClassVar[ClusterRequirementKind]
    CLUSTER_REQUIREMENT_KIND_KUBERNETES_RBAC: _ClassVar[ClusterRequirementKind]
    CLUSTER_REQUIREMENT_KIND_HELM_RELEASE: _ClassVar[ClusterRequirementKind]
    CLUSTER_REQUIREMENT_KIND_KUBERNETES_OBJECT: _ClassVar[ClusterRequirementKind]
    CLUSTER_REQUIREMENT_KIND_WORKLOAD_IDENTITY: _ClassVar[ClusterRequirementKind]
    CLUSTER_REQUIREMENT_KIND_CLOUD_IDENTITY: _ClassVar[ClusterRequirementKind]
    CLUSTER_REQUIREMENT_KIND_DNS_ZONE: _ClassVar[ClusterRequirementKind]

class ClusterRequirementScope(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLUSTER_REQUIREMENT_SCOPE_UNSPECIFIED: _ClassVar[ClusterRequirementScope]
    CLUSTER_REQUIREMENT_SCOPE_CLUSTER: _ClassVar[ClusterRequirementScope]
    CLUSTER_REQUIREMENT_SCOPE_NAMESPACE: _ClassVar[ClusterRequirementScope]
    CLUSTER_REQUIREMENT_SCOPE_AWS_ACCOUNT: _ClassVar[ClusterRequirementScope]
    CLUSTER_REQUIREMENT_SCOPE_GCP_PROJECT: _ClassVar[ClusterRequirementScope]
    CLUSTER_REQUIREMENT_SCOPE_GCP_SERVICE_ACCOUNT: _ClassVar[ClusterRequirementScope]

CLUSTER_HEALTH_CHECK_NAME_UNSPECIFIED: ClusterHealthCheckName
CLUSTER_HEALTH_CHECK_NAME_KUBERNETES_API_ACCESS: ClusterHealthCheckName
CLUSTER_HEALTH_CHECK_NAME_DATAPLANE_API_SERVER_NAMESPACE: ClusterHealthCheckName
CLUSTER_HEALTH_CHECK_NAME_DATAPLANE_CONTROLLER_NAMESPACE: ClusterHealthCheckName
CLUSTER_HEALTH_CHECK_NAME_TELEMETRY_NAMESPACE: ClusterHealthCheckName
CLUSTER_HEALTH_CHECK_NAME_DATAPLANE_API_SERVER_IDENTITY: ClusterHealthCheckName
CLUSTER_HEALTH_CHECK_NAME_ENVOY_GATEWAY: ClusterHealthCheckName
CLUSTER_HEALTH_CHECK_NAME_CERT_MANAGER: ClusterHealthCheckName
CLUSTER_HEALTH_CHECK_NAME_EXTERNAL_DNS: ClusterHealthCheckName
CLUSTER_HEALTH_CHECK_NAME_CLUSTER_ISSUERS: ClusterHealthCheckName
CLUSTER_HEALTH_CHECK_NAME_DNS_ZONES: ClusterHealthCheckName
CLUSTER_HEALTH_CHECK_NAME_KEDA: ClusterHealthCheckName
CLUSTER_HEALTH_CHECK_NAME_VICTORIA_METRICS_OPERATOR: ClusterHealthCheckName
CLUSTER_HEALTH_CHECK_NAME_KUBE_STATE_METRICS: ClusterHealthCheckName
CLUSTER_HEALTH_STATUS_UNSPECIFIED: ClusterHealthStatus
CLUSTER_HEALTH_STATUS_OK: ClusterHealthStatus
CLUSTER_HEALTH_STATUS_WARNING: ClusterHealthStatus
CLUSTER_HEALTH_STATUS_FAILING: ClusterHealthStatus
CLUSTER_HEALTH_STATUS_NOT_CONFIGURED: ClusterHealthStatus
CLUSTER_DIAGNOSTIC_SEVERITY_UNSPECIFIED: ClusterDiagnosticSeverity
CLUSTER_DIAGNOSTIC_SEVERITY_INFORMATION: ClusterDiagnosticSeverity
CLUSTER_DIAGNOSTIC_SEVERITY_WARNING: ClusterDiagnosticSeverity
CLUSTER_DIAGNOSTIC_SEVERITY_ERROR: ClusterDiagnosticSeverity
CLUSTER_DIAGNOSTIC_OWNER_UNSPECIFIED: ClusterDiagnosticOwner
CLUSTER_DIAGNOSTIC_OWNER_CHALK: ClusterDiagnosticOwner
CLUSTER_DIAGNOSTIC_OWNER_CUSTOMER: ClusterDiagnosticOwner
CLUSTER_REQUIREMENT_KIND_UNSPECIFIED: ClusterRequirementKind
CLUSTER_REQUIREMENT_KIND_KUBERNETES_RBAC: ClusterRequirementKind
CLUSTER_REQUIREMENT_KIND_HELM_RELEASE: ClusterRequirementKind
CLUSTER_REQUIREMENT_KIND_KUBERNETES_OBJECT: ClusterRequirementKind
CLUSTER_REQUIREMENT_KIND_WORKLOAD_IDENTITY: ClusterRequirementKind
CLUSTER_REQUIREMENT_KIND_CLOUD_IDENTITY: ClusterRequirementKind
CLUSTER_REQUIREMENT_KIND_DNS_ZONE: ClusterRequirementKind
CLUSTER_REQUIREMENT_SCOPE_UNSPECIFIED: ClusterRequirementScope
CLUSTER_REQUIREMENT_SCOPE_CLUSTER: ClusterRequirementScope
CLUSTER_REQUIREMENT_SCOPE_NAMESPACE: ClusterRequirementScope
CLUSTER_REQUIREMENT_SCOPE_AWS_ACCOUNT: ClusterRequirementScope
CLUSTER_REQUIREMENT_SCOPE_GCP_PROJECT: ClusterRequirementScope
CLUSTER_REQUIREMENT_SCOPE_GCP_SERVICE_ACCOUNT: ClusterRequirementScope

class ClusterRequirement(_message.Message):
    __slots__ = ("kind", "permissions", "resource", "scope", "principal", "resource_kind", "scope_kind")
    KIND_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    PRINCIPAL_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    SCOPE_KIND_FIELD_NUMBER: _ClassVar[int]
    kind: ClusterRequirementKind
    permissions: _containers.RepeatedScalarFieldContainer[str]
    resource: str
    scope: str
    principal: str
    resource_kind: str
    scope_kind: ClusterRequirementScope
    def __init__(
        self,
        kind: _Optional[_Union[ClusterRequirementKind, str]] = ...,
        permissions: _Optional[_Iterable[str]] = ...,
        resource: _Optional[str] = ...,
        scope: _Optional[str] = ...,
        principal: _Optional[str] = ...,
        resource_kind: _Optional[str] = ...,
        scope_kind: _Optional[_Union[ClusterRequirementScope, str]] = ...,
    ) -> None: ...

class ClusterDiagnostic(_message.Message):
    __slots__ = ("severity", "title", "message", "owner", "requirements")
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    severity: ClusterDiagnosticSeverity
    title: str
    message: str
    owner: ClusterDiagnosticOwner
    requirements: _containers.RepeatedCompositeFieldContainer[ClusterRequirement]
    def __init__(
        self,
        severity: _Optional[_Union[ClusterDiagnosticSeverity, str]] = ...,
        title: _Optional[str] = ...,
        message: _Optional[str] = ...,
        owner: _Optional[_Union[ClusterDiagnosticOwner, str]] = ...,
        requirements: _Optional[_Iterable[_Union[ClusterRequirement, _Mapping]]] = ...,
    ) -> None: ...

class ClusterHealthCheckResult(_message.Message):
    __slots__ = ("name", "status", "diagnostics", "latency")
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
    LATENCY_FIELD_NUMBER: _ClassVar[int]
    name: ClusterHealthCheckName
    status: ClusterHealthStatus
    diagnostics: _containers.RepeatedCompositeFieldContainer[ClusterDiagnostic]
    latency: _duration_pb2.Duration
    def __init__(
        self,
        name: _Optional[_Union[ClusterHealthCheckName, str]] = ...,
        status: _Optional[_Union[ClusterHealthStatus, str]] = ...,
        diagnostics: _Optional[_Iterable[_Union[ClusterDiagnostic, _Mapping]]] = ...,
        latency: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
    ) -> None: ...

class ClusterHealthCheckFilters(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: _containers.RepeatedScalarFieldContainer[ClusterHealthCheckName]
    def __init__(self, name: _Optional[_Iterable[_Union[ClusterHealthCheckName, str]]] = ...) -> None: ...

class GetClusterHealthRequest(_message.Message):
    __slots__ = ("candidate", "cluster_id", "filters")
    CANDIDATE_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    candidate: _cloud_components_pb2.CloudComponentClusterRequest
    cluster_id: str
    filters: ClusterHealthCheckFilters
    def __init__(
        self,
        candidate: _Optional[_Union[_cloud_components_pb2.CloudComponentClusterRequest, _Mapping]] = ...,
        cluster_id: _Optional[str] = ...,
        filters: _Optional[_Union[ClusterHealthCheckFilters, _Mapping]] = ...,
    ) -> None: ...

class GetClusterHealthResponse(_message.Message):
    __slots__ = ("cluster_kind", "checks", "status")
    CLUSTER_KIND_FIELD_NUMBER: _ClassVar[int]
    CHECKS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    cluster_kind: str
    checks: _containers.RepeatedCompositeFieldContainer[ClusterHealthCheckResult]
    status: ClusterHealthStatus
    def __init__(
        self,
        cluster_kind: _Optional[str] = ...,
        checks: _Optional[_Iterable[_Union[ClusterHealthCheckResult, _Mapping]]] = ...,
        status: _Optional[_Union[ClusterHealthStatus, str]] = ...,
    ) -> None: ...

class ListClusterDnsZonesRequest(_message.Message):
    __slots__ = ("cloud_credential_id",)
    CLOUD_CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    cloud_credential_id: str
    def __init__(self, cloud_credential_id: _Optional[str] = ...) -> None: ...

class ClusterDnsZone(_message.Message):
    __slots__ = ("id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class ListClusterDnsZonesResponse(_message.Message):
    __slots__ = ("zones",)
    ZONES_FIELD_NUMBER: _ClassVar[int]
    zones: _containers.RepeatedCompositeFieldContainer[ClusterDnsZone]
    def __init__(self, zones: _Optional[_Iterable[_Union[ClusterDnsZone, _Mapping]]] = ...) -> None: ...
