from chalk._gen.chalk.artifacts.v1 import export_pb2 as _export_pb2
from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
from chalk._gen.chalk.graph.v1 import graph_pb2 as _graph_pb2
from chalk._gen.chalk.server.v1 import deployment_pb2 as _deployment_pb2
from google.protobuf import empty_pb2 as _empty_pb2
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

class DeployBranchRequest(_message.Message):
    __slots__ = ("branch_name", "reset_branch", "archive", "is_hot_deploy")
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    RESET_BRANCH_FIELD_NUMBER: _ClassVar[int]
    ARCHIVE_FIELD_NUMBER: _ClassVar[int]
    IS_HOT_DEPLOY_FIELD_NUMBER: _ClassVar[int]
    branch_name: str
    reset_branch: bool
    archive: bytes
    is_hot_deploy: bool
    def __init__(
        self,
        branch_name: _Optional[str] = ...,
        reset_branch: bool = ...,
        archive: _Optional[bytes] = ...,
        is_hot_deploy: bool = ...,
    ) -> None: ...

class DeployBranchResponse(_message.Message):
    __slots__ = ("deployment_id", "graph", "deployment_errors", "export")
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    GRAPH_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ERRORS_FIELD_NUMBER: _ClassVar[int]
    EXPORT_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    graph: _graph_pb2.Graph
    deployment_errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    export: _export_pb2.Export
    def __init__(
        self,
        deployment_id: _Optional[str] = ...,
        graph: _Optional[_Union[_graph_pb2.Graph, _Mapping]] = ...,
        deployment_errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
        export: _Optional[_Union[_export_pb2.Export, _Mapping]] = ...,
    ) -> None: ...

class CreateBranchFromSourceDeploymentRequest(_message.Message):
    __slots__ = ("branch_name", "source_branch_name", "source_deployment_id", "current_mainline_deployment")
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    SOURCE_BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    SOURCE_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CURRENT_MAINLINE_DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    branch_name: str
    source_branch_name: str
    source_deployment_id: str
    current_mainline_deployment: _empty_pb2.Empty
    def __init__(
        self,
        branch_name: _Optional[str] = ...,
        source_branch_name: _Optional[str] = ...,
        source_deployment_id: _Optional[str] = ...,
        current_mainline_deployment: _Optional[_Union[_empty_pb2.Empty, _Mapping]] = ...,
    ) -> None: ...

class CreateBranchFromSourceDeploymentResponse(_message.Message):
    __slots__ = ("deployment_id", "deployment_errors", "export", "branch_already_exists")
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ERRORS_FIELD_NUMBER: _ClassVar[int]
    EXPORT_FIELD_NUMBER: _ClassVar[int]
    BRANCH_ALREADY_EXISTS_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    deployment_errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    export: _export_pb2.Export
    branch_already_exists: bool
    def __init__(
        self,
        deployment_id: _Optional[str] = ...,
        deployment_errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
        export: _Optional[_Union[_export_pb2.Export, _Mapping]] = ...,
        branch_already_exists: bool = ...,
    ) -> None: ...

class GetDeploymentRequest(_message.Message):
    __slots__ = ("deployment_id",)
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    def __init__(self, deployment_id: _Optional[str] = ...) -> None: ...

class GetDeploymentResponse(_message.Message):
    __slots__ = ("deployment",)
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    deployment: _deployment_pb2.Deployment
    def __init__(self, deployment: _Optional[_Union[_deployment_pb2.Deployment, _Mapping]] = ...) -> None: ...

class ListDeploymentsRequest(_message.Message):
    __slots__ = ("cursor", "limit", "include_branch", "branch_name")
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_BRANCH_FIELD_NUMBER: _ClassVar[int]
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    cursor: str
    limit: int
    include_branch: bool
    branch_name: str
    def __init__(
        self,
        cursor: _Optional[str] = ...,
        limit: _Optional[int] = ...,
        include_branch: bool = ...,
        branch_name: _Optional[str] = ...,
    ) -> None: ...

class ListDeploymentsResponse(_message.Message):
    __slots__ = ("deployments", "cursor")
    DEPLOYMENTS_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    deployments: _containers.RepeatedCompositeFieldContainer[_deployment_pb2.Deployment]
    cursor: str
    def __init__(
        self,
        deployments: _Optional[_Iterable[_Union[_deployment_pb2.Deployment, _Mapping]]] = ...,
        cursor: _Optional[str] = ...,
    ) -> None: ...

class SuspendDeploymentRequest(_message.Message):
    __slots__ = ("deployment_id",)
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    def __init__(self, deployment_id: _Optional[str] = ...) -> None: ...

class SuspendDeploymentResponse(_message.Message):
    __slots__ = ("deployment",)
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    deployment: _deployment_pb2.Deployment
    def __init__(self, deployment: _Optional[_Union[_deployment_pb2.Deployment, _Mapping]] = ...) -> None: ...

class ScaleDeploymentRequest(_message.Message):
    __slots__ = ("deployment_id", "sizing")
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    SIZING_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    sizing: _deployment_pb2.InstanceSizing
    def __init__(
        self,
        deployment_id: _Optional[str] = ...,
        sizing: _Optional[_Union[_deployment_pb2.InstanceSizing, _Mapping]] = ...,
    ) -> None: ...

class ScaleDeploymentResponse(_message.Message):
    __slots__ = ("deployment",)
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    deployment: _deployment_pb2.Deployment
    def __init__(self, deployment: _Optional[_Union[_deployment_pb2.Deployment, _Mapping]] = ...) -> None: ...

class TagDeploymentRequest(_message.Message):
    __slots__ = ("deployment_id", "tag", "mirror_weight")
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    MIRROR_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    tag: str
    mirror_weight: int
    def __init__(
        self, deployment_id: _Optional[str] = ..., tag: _Optional[str] = ..., mirror_weight: _Optional[int] = ...
    ) -> None: ...

class TagDeploymentResponse(_message.Message):
    __slots__ = ("deployment", "untagged_deployment_id")
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    UNTAGGED_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    deployment: _deployment_pb2.Deployment
    untagged_deployment_id: str
    def __init__(
        self,
        deployment: _Optional[_Union[_deployment_pb2.Deployment, _Mapping]] = ...,
        untagged_deployment_id: _Optional[str] = ...,
    ) -> None: ...

class GetActiveDeploymentsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetActiveDeploymentsResponse(_message.Message):
    __slots__ = ("deployments",)
    DEPLOYMENTS_FIELD_NUMBER: _ClassVar[int]
    deployments: _containers.RepeatedCompositeFieldContainer[_deployment_pb2.Deployment]
    def __init__(
        self, deployments: _Optional[_Iterable[_Union[_deployment_pb2.Deployment, _Mapping]]] = ...
    ) -> None: ...
