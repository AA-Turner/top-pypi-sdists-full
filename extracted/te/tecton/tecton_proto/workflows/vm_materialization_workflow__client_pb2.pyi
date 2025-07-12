from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.materialization import materialization_states__client_pb2 as _materialization_states__client_pb2
from tecton_proto.materialization import materialization_task__client_pb2 as _materialization_task__client_pb2
from tecton_proto.workflows import spark_execution_workflow__client_pb2 as _spark_execution_workflow__client_pb2
from tecton_proto.workflows import state_machine_workflow__client_pb2 as _state_machine_workflow__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VmMaterializationStateTransition(_message.Message):
    __slots__ = ["state", "state_message", "timestamp"]
    STATE_FIELD_NUMBER: _ClassVar[int]
    STATE_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    state: _materialization_states__client_pb2.MaterializationTaskAttemptState
    state_message: str
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, state: _Optional[_Union[_materialization_states__client_pb2.MaterializationTaskAttemptState, str]] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., state_message: _Optional[str] = ...) -> None: ...

class VmMaterializationWorkflow(_message.Message):
    __slots__ = ["approx_instance_termination_time", "consumption_scrape_watermark", "final_run_details", "import_table_info", "instance_launch_time", "state_transitions", "task", "vm_instance_id", "vm_instance_region", "vm_instance_zone", "workspace_state_id"]
    APPROX_INSTANCE_TERMINATION_TIME_FIELD_NUMBER: _ClassVar[int]
    CONSUMPTION_SCRAPE_WATERMARK_FIELD_NUMBER: _ClassVar[int]
    FINAL_RUN_DETAILS_FIELD_NUMBER: _ClassVar[int]
    IMPORT_TABLE_INFO_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_LAUNCH_TIME_FIELD_NUMBER: _ClassVar[int]
    STATE_TRANSITIONS_FIELD_NUMBER: _ClassVar[int]
    TASK_FIELD_NUMBER: _ClassVar[int]
    VM_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    VM_INSTANCE_REGION_FIELD_NUMBER: _ClassVar[int]
    VM_INSTANCE_ZONE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_STATE_ID_FIELD_NUMBER: _ClassVar[int]
    approx_instance_termination_time: _timestamp_pb2.Timestamp
    consumption_scrape_watermark: _timestamp_pb2.Timestamp
    final_run_details: _spark_execution_workflow__client_pb2.RunResult
    import_table_info: _spark_execution_workflow__client_pb2.ImportTableInfo
    instance_launch_time: _timestamp_pb2.Timestamp
    state_transitions: _containers.RepeatedCompositeFieldContainer[VmMaterializationStateTransition]
    task: _materialization_task__client_pb2.MaterializationTask
    vm_instance_id: str
    vm_instance_region: str
    vm_instance_zone: str
    workspace_state_id: _id__client_pb2.Id
    def __init__(self, task: _Optional[_Union[_materialization_task__client_pb2.MaterializationTask, _Mapping]] = ..., workspace_state_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., vm_instance_id: _Optional[str] = ..., vm_instance_region: _Optional[str] = ..., vm_instance_zone: _Optional[str] = ..., final_run_details: _Optional[_Union[_spark_execution_workflow__client_pb2.RunResult, _Mapping]] = ..., consumption_scrape_watermark: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., state_transitions: _Optional[_Iterable[_Union[VmMaterializationStateTransition, _Mapping]]] = ..., instance_launch_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., approx_instance_termination_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., import_table_info: _Optional[_Union[_spark_execution_workflow__client_pb2.ImportTableInfo, _Mapping]] = ...) -> None: ...
