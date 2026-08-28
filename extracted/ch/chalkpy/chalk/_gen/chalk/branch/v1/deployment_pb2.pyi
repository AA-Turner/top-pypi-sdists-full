from chalk._gen.chalk.artifacts.v1 import export_pb2 as _export_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import deployment_pb2 as _deployment_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BranchDeployment(_message.Message):
    __slots__ = ("branch_name", "deployment_id", "status", "export")
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    EXPORT_FIELD_NUMBER: _ClassVar[int]
    branch_name: str
    deployment_id: str
    status: _deployment_pb2.DeploymentStatus
    export: _export_pb2.Export
    def __init__(
        self,
        branch_name: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        status: _Optional[_Union[_deployment_pb2.DeploymentStatus, str]] = ...,
        export: _Optional[_Union[_export_pb2.Export, _Mapping]] = ...,
    ) -> None: ...

class StartBranchDeploymentRequest(_message.Message):
    __slots__ = ("branch_name", "deployment_id")
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    branch_name: str
    deployment_id: str
    def __init__(self, branch_name: _Optional[str] = ..., deployment_id: _Optional[str] = ...) -> None: ...

class StartBranchDeploymentResponse(_message.Message):
    __slots__ = ("branch_deployment",)
    BRANCH_DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    branch_deployment: BranchDeployment
    def __init__(self, branch_deployment: _Optional[_Union[BranchDeployment, _Mapping]] = ...) -> None: ...

class GetBranchDeploymentStateRequest(_message.Message):
    __slots__ = ("branch_name", "deployment_id")
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    branch_name: str
    deployment_id: str
    def __init__(self, branch_name: _Optional[str] = ..., deployment_id: _Optional[str] = ...) -> None: ...

class GetBranchDeploymentStateResponse(_message.Message):
    __slots__ = ("branch_deployment", "deployment_stage")
    BRANCH_DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_STAGE_FIELD_NUMBER: _ClassVar[int]
    branch_deployment: BranchDeployment
    deployment_stage: str
    def __init__(
        self,
        branch_deployment: _Optional[_Union[BranchDeployment, _Mapping]] = ...,
        deployment_stage: _Optional[str] = ...,
    ) -> None: ...
