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

class BranchWithLatestDeployment(_message.Message):
    __slots__ = (
        "branch",
        "latest_deployment_status",
        "latest_deployment_created",
        "latest_deployment_updated",
        "latest_deployment_id",
    )
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    LATEST_DEPLOYMENT_STATUS_FIELD_NUMBER: _ClassVar[int]
    LATEST_DEPLOYMENT_CREATED_FIELD_NUMBER: _ClassVar[int]
    LATEST_DEPLOYMENT_UPDATED_FIELD_NUMBER: _ClassVar[int]
    LATEST_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    branch: Branch
    latest_deployment_status: _deployment_pb2.DeploymentStatus
    latest_deployment_created: _timestamp_pb2.Timestamp
    latest_deployment_updated: _timestamp_pb2.Timestamp
    latest_deployment_id: str
    def __init__(
        self,
        branch: _Optional[_Union[Branch, _Mapping]] = ...,
        latest_deployment_status: _Optional[_Union[_deployment_pb2.DeploymentStatus, str]] = ...,
        latest_deployment_created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        latest_deployment_updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        latest_deployment_id: _Optional[str] = ...,
    ) -> None: ...

class ListBranchWithLatestDeploymentsRequest(_message.Message):
    __slots__ = ("cursor", "limit")
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    cursor: str
    limit: int
    def __init__(self, cursor: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...

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
