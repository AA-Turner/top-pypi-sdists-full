from tecton_proto.workflows import state_machine_workflow__client_pb2 as _state_machine_workflow__client_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DATABRICKS_VALIDATION_CLUSTER_WORKFLOW_ERROR_CREATING_CLUSTER: DatabricksValidationClusterWorkflowError
DATABRICKS_VALIDATION_CLUSTER_WORKFLOW_ERROR_NO_ERROR: DatabricksValidationClusterWorkflowError
DATABRICKS_VALIDATION_CLUSTER_WORKFLOW_STATE_NO_ACTIVE_CLUSTERS: DatabricksValidationClusterWorkflowState
DATABRICKS_VALIDATION_CLUSTER_WORKFLOW_STATE_RUNNING: DatabricksValidationClusterWorkflowState
DATABRICKS_VALIDATION_CLUSTER_WORKFLOW_STATE_UNKNOWN: DatabricksValidationClusterWorkflowState
DATABRICKS_VALIDATION_CLUSTER_WORKFLOW_STATE_UPGRADING: DatabricksValidationClusterWorkflowState
DESCRIPTOR: _descriptor.FileDescriptor

class DatabricksValidationClusterWorkflow(_message.Message):
    __slots__ = ["canonical_cluster_id", "canonical_cluster_user_deployment_settings_version", "error", "error_message", "next_cluster_id", "state"]
    CANONICAL_CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    CANONICAL_CLUSTER_USER_DEPLOYMENT_SETTINGS_VERSION_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    NEXT_CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    canonical_cluster_id: str
    canonical_cluster_user_deployment_settings_version: int
    error: DatabricksValidationClusterWorkflowError
    error_message: str
    next_cluster_id: str
    state: DatabricksValidationClusterWorkflowState
    def __init__(self, state: _Optional[_Union[DatabricksValidationClusterWorkflowState, str]] = ..., canonical_cluster_id: _Optional[str] = ..., canonical_cluster_user_deployment_settings_version: _Optional[int] = ..., error: _Optional[_Union[DatabricksValidationClusterWorkflowError, str]] = ..., error_message: _Optional[str] = ..., next_cluster_id: _Optional[str] = ...) -> None: ...

class DatabricksValidationClusterWorkflowError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class DatabricksValidationClusterWorkflowState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
