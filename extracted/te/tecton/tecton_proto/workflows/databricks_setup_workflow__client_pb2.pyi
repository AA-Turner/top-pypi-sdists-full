from tecton_proto.data import user_deployment_settings__client_pb2 as _user_deployment_settings__client_pb2
from tecton_proto.workflows import state_machine_workflow__client_pb2 as _state_machine_workflow__client_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DATABRICKS_SETUP_WORKFLOW_CLUSTER_READY: DatabricksSetupWorkflowState
DATABRICKS_SETUP_WORKFLOW_CLUSTER_STARTING: DatabricksSetupWorkflowState
DATABRICKS_SETUP_WORKFLOW_CREATED_SECRET_SCOPE: DatabricksSetupWorkflowState
DATABRICKS_SETUP_WORKFLOW_FOUND_SETTINGS: DatabricksSetupWorkflowState
DATABRICKS_SETUP_WORKFLOW_UNKNOWN: DatabricksSetupWorkflowState
DATABRICKS_SETUP_WORKFLOW_WAITING_FOR_SETTINGS: DatabricksSetupWorkflowState
DESCRIPTOR: _descriptor.FileDescriptor

class DatabricksSetupWorkflow(_message.Message):
    __slots__ = ["created_secret_scope", "error_message", "failed_advances_for_version", "notebook_cluster_id", "state", "user_deployment_settings"]
    CREATED_SECRET_SCOPE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    FAILED_ADVANCES_FOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    NOTEBOOK_CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    USER_DEPLOYMENT_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    created_secret_scope: bool
    error_message: str
    failed_advances_for_version: int
    notebook_cluster_id: str
    state: DatabricksSetupWorkflowState
    user_deployment_settings: _user_deployment_settings__client_pb2.UserDeploymentSettings
    def __init__(self, state: _Optional[_Union[DatabricksSetupWorkflowState, str]] = ..., user_deployment_settings: _Optional[_Union[_user_deployment_settings__client_pb2.UserDeploymentSettings, _Mapping]] = ..., failed_advances_for_version: _Optional[int] = ..., created_secret_scope: bool = ..., notebook_cluster_id: _Optional[str] = ..., error_message: _Optional[str] = ...) -> None: ...

class DatabricksSetupWorkflowState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
