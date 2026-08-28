from chalk._gen.chalk.artifacts.v1 import export_pb2 as _export_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import deployment_pb2 as _deployment_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
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

class Branch(_message.Message):
    __slots__ = ("id", "name", "created_at", "deployment_count")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_COUNT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    created_at: _timestamp_pb2.Timestamp
    deployment_count: int
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        deployment_count: _Optional[int] = ...,
    ) -> None: ...

class PythonPackage(_message.Message):
    __slots__ = ("package_name", "package_version")
    PACKAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    PACKAGE_VERSION_FIELD_NUMBER: _ClassVar[int]
    package_name: str
    package_version: str
    def __init__(self, package_name: _Optional[str] = ..., package_version: _Optional[str] = ...) -> None: ...

class VenvPackages(_message.Message):
    __slots__ = ("venv_packages",)
    VENV_PACKAGES_FIELD_NUMBER: _ClassVar[int]
    venv_packages: _containers.RepeatedCompositeFieldContainer[PythonPackage]
    def __init__(self, venv_packages: _Optional[_Iterable[_Union[PythonPackage, _Mapping]]] = ...) -> None: ...

class BranchWithLatestDeployment(_message.Message):
    __slots__ = (
        "branch",
        "latest_deployment_status",
        "latest_deployment_created",
        "latest_deployment_updated",
        "latest_deployment_id",
        "latest_deployment_triggered_by",
    )
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    LATEST_DEPLOYMENT_STATUS_FIELD_NUMBER: _ClassVar[int]
    LATEST_DEPLOYMENT_CREATED_FIELD_NUMBER: _ClassVar[int]
    LATEST_DEPLOYMENT_UPDATED_FIELD_NUMBER: _ClassVar[int]
    LATEST_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LATEST_DEPLOYMENT_TRIGGERED_BY_FIELD_NUMBER: _ClassVar[int]
    branch: Branch
    latest_deployment_status: _deployment_pb2.DeploymentStatus
    latest_deployment_created: _timestamp_pb2.Timestamp
    latest_deployment_updated: _timestamp_pb2.Timestamp
    latest_deployment_id: str
    latest_deployment_triggered_by: str
    def __init__(
        self,
        branch: _Optional[_Union[Branch, _Mapping]] = ...,
        latest_deployment_status: _Optional[_Union[_deployment_pb2.DeploymentStatus, str]] = ...,
        latest_deployment_created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        latest_deployment_updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        latest_deployment_id: _Optional[str] = ...,
        latest_deployment_triggered_by: _Optional[str] = ...,
    ) -> None: ...

class GetBranchWithLatestDeploymentRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GetBranchWithLatestDeploymentResponse(_message.Message):
    __slots__ = ("branch_with_latest_deployment",)
    BRANCH_WITH_LATEST_DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    branch_with_latest_deployment: BranchWithLatestDeployment
    def __init__(
        self, branch_with_latest_deployment: _Optional[_Union[BranchWithLatestDeployment, _Mapping]] = ...
    ) -> None: ...

class ListBranchWithLatestDeploymentsRequest(_message.Message):
    __slots__ = ("cursor", "limit", "status", "deployed_by", "sort_ascending")
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DEPLOYED_BY_FIELD_NUMBER: _ClassVar[int]
    SORT_ASCENDING_FIELD_NUMBER: _ClassVar[int]
    cursor: str
    limit: int
    status: _containers.RepeatedScalarFieldContainer[_deployment_pb2.DeploymentStatus]
    deployed_by: _containers.RepeatedScalarFieldContainer[str]
    sort_ascending: bool
    def __init__(
        self,
        cursor: _Optional[str] = ...,
        limit: _Optional[int] = ...,
        status: _Optional[_Iterable[_Union[_deployment_pb2.DeploymentStatus, str]]] = ...,
        deployed_by: _Optional[_Iterable[str]] = ...,
        sort_ascending: bool = ...,
    ) -> None: ...

class ListBranchWithLatestDeploymentsResponse(_message.Message):
    __slots__ = ("branch_with_latest_deployments", "cursor")
    BRANCH_WITH_LATEST_DEPLOYMENTS_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    branch_with_latest_deployments: _containers.RepeatedCompositeFieldContainer[BranchWithLatestDeployment]
    cursor: str
    def __init__(
        self,
        branch_with_latest_deployments: _Optional[_Iterable[_Union[BranchWithLatestDeployment, _Mapping]]] = ...,
        cursor: _Optional[str] = ...,
    ) -> None: ...

class GetBranchVenvInstalledPackagesRequest(_message.Message):
    __slots__ = ("branch_id", "latest_deployment_id")
    BRANCH_ID_FIELD_NUMBER: _ClassVar[int]
    LATEST_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    branch_id: str
    latest_deployment_id: str
    def __init__(self, branch_id: _Optional[str] = ..., latest_deployment_id: _Optional[str] = ...) -> None: ...

class GetBranchVenvInstalledPackagesResponse(_message.Message):
    __slots__ = ("venv_packages_by_name",)
    class VenvPackagesByNameEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: VenvPackages
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[VenvPackages, _Mapping]] = ...
        ) -> None: ...

    VENV_PACKAGES_BY_NAME_FIELD_NUMBER: _ClassVar[int]
    venv_packages_by_name: _containers.MessageMap[str, VenvPackages]
    def __init__(self, venv_packages_by_name: _Optional[_Mapping[str, VenvPackages]] = ...) -> None: ...

class StartBranchDeploymentRequest(_message.Message):
    __slots__ = ("branch_name", "archive")
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    ARCHIVE_FIELD_NUMBER: _ClassVar[int]
    branch_name: str
    archive: bytes
    def __init__(self, branch_name: _Optional[str] = ..., archive: _Optional[bytes] = ...) -> None: ...

class StartBranchDeploymentResponse(_message.Message):
    __slots__ = ("deployment", "deployment_warnings")
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_WARNINGS_FIELD_NUMBER: _ClassVar[int]
    deployment: _deployment_pb2.Deployment
    deployment_warnings: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        deployment: _Optional[_Union[_deployment_pb2.Deployment, _Mapping]] = ...,
        deployment_warnings: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class GetBranchDeploymentStateRequest(_message.Message):
    __slots__ = ("branch_name", "deployment_id")
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    branch_name: str
    deployment_id: str
    def __init__(self, branch_name: _Optional[str] = ..., deployment_id: _Optional[str] = ...) -> None: ...

class GetBranchDeploymentStateResponse(_message.Message):
    __slots__ = ("deployment", "export", "deployment_stage")
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    EXPORT_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_STAGE_FIELD_NUMBER: _ClassVar[int]
    deployment: _deployment_pb2.Deployment
    export: _export_pb2.Export
    deployment_stage: str
    def __init__(
        self,
        deployment: _Optional[_Union[_deployment_pb2.Deployment, _Mapping]] = ...,
        export: _Optional[_Union[_export_pb2.Export, _Mapping]] = ...,
        deployment_stage: _Optional[str] = ...,
    ) -> None: ...
