from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.workflows import state_machine_workflow__client_pb2 as _state_machine_workflow__client_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
EMR_VALIDATION_CLUSTER_WORKFLOW_STATE_NO_ACTIVE_CLUSTERS: EMRValidationClusterWorkflowState
EMR_VALIDATION_CLUSTER_WORKFLOW_STATE_RUNNING: EMRValidationClusterWorkflowState
EMR_VALIDATION_CLUSTER_WORKFLOW_STATE_UNKNOWN: EMRValidationClusterWorkflowState
EMR_VALIDATION_CLUSTER_WORKFLOW_STATE_UPGRADING: EMRValidationClusterWorkflowState

class ClusterMetadata(_message.Message):
    __slots__ = ["cluster_id", "emr_release_label", "error_message", "launched_at"]
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    EMR_RELEASE_LABEL_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LAUNCHED_AT_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    emr_release_label: str
    error_message: str
    launched_at: _timestamp_pb2.Timestamp
    def __init__(self, cluster_id: _Optional[str] = ..., emr_release_label: _Optional[str] = ..., error_message: _Optional[str] = ..., launched_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class EMRValidationClusterWorkflowProto(_message.Message):
    __slots__ = ["canonical_cluster", "next_cluster", "state", "state_reported_at"]
    CANONICAL_CLUSTER_FIELD_NUMBER: _ClassVar[int]
    NEXT_CLUSTER_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    STATE_REPORTED_AT_FIELD_NUMBER: _ClassVar[int]
    canonical_cluster: ClusterMetadata
    next_cluster: ClusterMetadata
    state: EMRValidationClusterWorkflowState
    state_reported_at: _timestamp_pb2.Timestamp
    def __init__(self, state: _Optional[_Union[EMRValidationClusterWorkflowState, str]] = ..., canonical_cluster: _Optional[_Union[ClusterMetadata, _Mapping]] = ..., state_reported_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., next_cluster: _Optional[_Union[ClusterMetadata, _Mapping]] = ...) -> None: ...

class EMRValidationClusterWorkflowState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
