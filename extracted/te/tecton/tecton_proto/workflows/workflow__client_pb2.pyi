from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.workflows import audit_log_processing_workflow__client_pb2 as _audit_log_processing_workflow__client_pb2
from tecton_proto.workflows import cache_reconcile_workflow__client_pb2 as _cache_reconcile_workflow__client_pb2
from tecton_proto.workflows import canary_workflow__client_pb2 as _canary_workflow__client_pb2
from tecton_proto.workflows import consumption_metrics_exporter_workflow__client_pb2 as _consumption_metrics_exporter_workflow__client_pb2
from tecton_proto.workflows import data_validation_workflow__client_pb2 as _data_validation_workflow__client_pb2
from tecton_proto.workflows import databricks_setup_workflow__client_pb2 as _databricks_setup_workflow__client_pb2
from tecton_proto.workflows import databricks_validation_cluster_workflow__client_pb2 as _databricks_validation_cluster_workflow__client_pb2
from tecton_proto.workflows import dynamo_import_table_workflow__client_pb2 as _dynamo_import_table_workflow__client_pb2
from tecton_proto.workflows import emr_validation_cluster_workflow__client_pb2 as _emr_validation_cluster_workflow__client_pb2
from tecton_proto.workflows import materialization_scheduling_workflow__client_pb2 as _materialization_scheduling_workflow__client_pb2
from tecton_proto.workflows import plan_integration_test_status_workflow__client_pb2 as _plan_integration_test_status_workflow__client_pb2
from tecton_proto.workflows import ray_materialization_workflow__client_pb2 as _ray_materialization_workflow__client_pb2
from tecton_proto.workflows import self_serve_consumption_delivery_workflow__client_pb2 as _self_serve_consumption_delivery_workflow__client_pb2
from tecton_proto.workflows import server_group_reconciliation_workflow__client_pb2 as _server_group_reconciliation_workflow__client_pb2
from tecton_proto.workflows import server_group_state_machine_workflow__client_pb2 as _server_group_state_machine_workflow__client_pb2
from tecton_proto.workflows import spark_execution_workflow__client_pb2 as _spark_execution_workflow__client_pb2
from tecton_proto.workflows import state_machine_workflow__client_pb2 as _state_machine_workflow__client_pb2
from tecton_proto.workflows import test_state_machine_workflow__client_pb2 as _test_state_machine_workflow__client_pb2
from tecton_proto.workflows import test_workflow__client_pb2 as _test_workflow__client_pb2
from tecton_proto.workflows import vm_materialization_workflow__client_pb2 as _vm_materialization_workflow__client_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

AUDIT_LOG_PROCESING_WORKFLOW: WorkflowType
CACHE_RECONCILE_TASK_ATTEMPT_WORKFLOW: WorkflowType
CACHE_RECONCILE_TASK_WORKFLOW: WorkflowType
CANARY_WORKFLOW: WorkflowType
CONSUMPTION_METRICS_EXPORTER_WORKFLOW: WorkflowType
DATABRICKS_SETUP_WORKFLOW: WorkflowType
DATABRICKS_VALIDATION_CLUSTER_WORKFLOW: WorkflowType
DATA_VALIDATION_WORKFLOW: WorkflowType
DESCRIPTOR: _descriptor.FileDescriptor
DYNAMO_IMPORT_TABLE_WORKFLOW: WorkflowType
EMR_VALIDATION_CLUSTER_WORKFLOW: WorkflowType
JOB_EXECUTION_WORKFLOW: WorkflowType
MATERIALIZATION_SCHEDULING_WORKFLOW: WorkflowType
PLAN_INTEGRATION_TEST_STATUS_WORKFLOW: WorkflowType
RAY_MATERIALIZATION_WORKFLOW: WorkflowType
SELF_SERVE_CONSUMPTION_DELIVERY_WORKFLOW: WorkflowType
SERVER_GROUP_RECONCILIATION_WORKFLOW: WorkflowType
SERVER_GROUP_STATE_MACHINE_WORKFLOW: WorkflowType
SPARK_EXECUTION_WORKFLOW: WorkflowType
SPARK_EXECUTION_WORKFLOW_V2: WorkflowType
SUBCONTAINER_FIELD_NUMBER_FIELD_NUMBER: _ClassVar[int]
TEST_STATE_MACHINE_WORKFLOW: WorkflowType
TEST_WORKFLOW: WorkflowType
UNKNOWN_WORKFLOW: WorkflowType
VM_MATERIALIZATION_WORKFLOW: WorkflowType
subcontainer_field_number: _descriptor.FieldDescriptor

class KotlinException(_message.Message):
    __slots__ = ["message", "name", "stack_trace_to_string"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STACK_TRACE_TO_STRING_FIELD_NUMBER: _ClassVar[int]
    message: str
    name: str
    stack_trace_to_string: str
    def __init__(self, name: _Optional[str] = ..., message: _Optional[str] = ..., stack_trace_to_string: _Optional[str] = ...) -> None: ...

class WorkflowHistoryEntry(_message.Message):
    __slots__ = ["event_id", "event_time", "from_state", "reason", "to_state", "workflow_id", "workflow_type"]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_TIME_FIELD_NUMBER: _ClassVar[int]
    FROM_STATE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    TO_STATE_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_TYPE_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    event_time: _timestamp_pb2.Timestamp
    from_state: str
    reason: str
    to_state: str
    workflow_id: _id__client_pb2.Id
    workflow_type: WorkflowType
    def __init__(self, workflow_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., event_id: _Optional[int] = ..., event_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., workflow_type: _Optional[_Union[WorkflowType, str]] = ..., from_state: _Optional[str] = ..., to_state: _Optional[str] = ..., reason: _Optional[str] = ...) -> None: ...

class WorkflowStateContainer(_message.Message):
    __slots__ = ["attempt_index", "audit_log_processing_workflow", "base_state", "cache_reconcile_task_attempt_workflow", "cache_reconcile_task_workflow", "canary_workflow", "cancellation_requested", "completed_at", "consumption_metrics_exporter_workflow", "created_at", "data_validation_workflow", "databricks_setup_workflow", "databricks_validation_cluster_workflow", "dynamo_import_table_workflow", "emr_validation_cluster_workflow", "initial_subcontainer", "is_complete", "last_exception", "materialization_scheduling_workflow", "parent_workflow_id", "plan_integration_test_status_workflow", "ray_materialization_workflow", "self_serve_consumption_delivery_workflow", "server_group_reconciliation_workflow", "server_group_state_machine_workflow", "spark_execution_workflow", "specific_workflow_serial", "termination_code", "test_state_machine_workflow", "test_workflow", "uniqueness_key", "updated_at", "vm_materialization_workflow", "workflow_id", "workflow_type"]
    class BaseState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ACTIVE: WorkflowStateContainer.BaseState
    ATTEMPT_INDEX_FIELD_NUMBER: _ClassVar[int]
    AUDIT_LOG_PROCESSING_WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    BASE_STATE_FIELD_NUMBER: _ClassVar[int]
    BASE_STATE_UNSPECIFIED: WorkflowStateContainer.BaseState
    CACHE_RECONCILE_TASK_ATTEMPT_WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    CACHE_RECONCILE_TASK_WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    CANARY_WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    CANCELLATION_REQUESTED_FIELD_NUMBER: _ClassVar[int]
    CANCELLING: WorkflowStateContainer.BaseState
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    CONSUMPTION_METRICS_EXPORTER_WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    DATABRICKS_SETUP_WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    DATABRICKS_VALIDATION_CLUSTER_WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    DATA_VALIDATION_WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    DYNAMO_IMPORT_TABLE_WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    EMR_VALIDATION_CLUSTER_WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    INITIAL_SUBCONTAINER_FIELD_NUMBER: _ClassVar[int]
    IS_COMPLETE_FIELD_NUMBER: _ClassVar[int]
    LAST_EXCEPTION_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZATION_SCHEDULING_WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    PARENT_WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    PLAN_INTEGRATION_TEST_STATUS_WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    QUEUED: WorkflowStateContainer.BaseState
    RAY_MATERIALIZATION_WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    SELF_SERVE_CONSUMPTION_DELIVERY_WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    SERVER_GROUP_RECONCILIATION_WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    SERVER_GROUP_STATE_MACHINE_WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    SPARK_EXECUTION_WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    SPECIFIC_WORKFLOW_SERIAL_FIELD_NUMBER: _ClassVar[int]
    TERMINATED: WorkflowStateContainer.BaseState
    TERMINATION_CODE_FIELD_NUMBER: _ClassVar[int]
    TEST_STATE_MACHINE_WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    TEST_WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    UNIQUENESS_KEY_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    VM_MATERIALIZATION_WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_TYPE_FIELD_NUMBER: _ClassVar[int]
    attempt_index: int
    audit_log_processing_workflow: _audit_log_processing_workflow__client_pb2.AuditLogProcessingWorkflow
    base_state: WorkflowStateContainer.BaseState
    cache_reconcile_task_attempt_workflow: _cache_reconcile_workflow__client_pb2.CacheReconcileTaskAttemptWorkflow
    cache_reconcile_task_workflow: _cache_reconcile_workflow__client_pb2.CacheReconcileTaskWorkflow
    canary_workflow: _canary_workflow__client_pb2.CanaryWorkflow
    cancellation_requested: bool
    completed_at: _timestamp_pb2.Timestamp
    consumption_metrics_exporter_workflow: _consumption_metrics_exporter_workflow__client_pb2.ConsumptionMetricsExporterWorkflow
    created_at: _timestamp_pb2.Timestamp
    data_validation_workflow: _data_validation_workflow__client_pb2.DataValidationWorkflow
    databricks_setup_workflow: _databricks_setup_workflow__client_pb2.DatabricksSetupWorkflow
    databricks_validation_cluster_workflow: _databricks_validation_cluster_workflow__client_pb2.DatabricksValidationClusterWorkflow
    dynamo_import_table_workflow: _dynamo_import_table_workflow__client_pb2.DynamoImportTableWorkflow
    emr_validation_cluster_workflow: _emr_validation_cluster_workflow__client_pb2.EMRValidationClusterWorkflowProto
    initial_subcontainer: _any_pb2.Any
    is_complete: bool
    last_exception: KotlinException
    materialization_scheduling_workflow: _materialization_scheduling_workflow__client_pb2.MaterializationSchedulingWorkflow
    parent_workflow_id: _id__client_pb2.Id
    plan_integration_test_status_workflow: _plan_integration_test_status_workflow__client_pb2.PlanIntegrationTestStatusWorkflow
    ray_materialization_workflow: _ray_materialization_workflow__client_pb2.RayMaterializationWorkflow
    self_serve_consumption_delivery_workflow: _self_serve_consumption_delivery_workflow__client_pb2.SelfServeConsumptionDeliveryWorkflow
    server_group_reconciliation_workflow: _server_group_reconciliation_workflow__client_pb2.ServerGroupReconciliationWorkflow
    server_group_state_machine_workflow: _server_group_state_machine_workflow__client_pb2.ServerGroupStateMachineWorkflowData
    spark_execution_workflow: _spark_execution_workflow__client_pb2.SparkExecutionWorkflow
    specific_workflow_serial: int
    termination_code: _state_machine_workflow__client_pb2.TerminalStateOptions.WorkflowTerminationCode
    test_state_machine_workflow: _test_state_machine_workflow__client_pb2.TestStateMachineWorkflowData
    test_workflow: _test_workflow__client_pb2.TestWorkflow
    uniqueness_key: str
    updated_at: _timestamp_pb2.Timestamp
    vm_materialization_workflow: _vm_materialization_workflow__client_pb2.VmMaterializationWorkflow
    workflow_id: _id__client_pb2.Id
    workflow_type: WorkflowType
    def __init__(self, workflow_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., parent_workflow_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., workflow_type: _Optional[_Union[WorkflowType, str]] = ..., is_complete: bool = ..., cancellation_requested: bool = ..., base_state: _Optional[_Union[WorkflowStateContainer.BaseState, str]] = ..., termination_code: _Optional[_Union[_state_machine_workflow__client_pb2.TerminalStateOptions.WorkflowTerminationCode, str]] = ..., uniqueness_key: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., completed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., spark_execution_workflow: _Optional[_Union[_spark_execution_workflow__client_pb2.SparkExecutionWorkflow, _Mapping]] = ..., canary_workflow: _Optional[_Union[_canary_workflow__client_pb2.CanaryWorkflow, _Mapping]] = ..., databricks_validation_cluster_workflow: _Optional[_Union[_databricks_validation_cluster_workflow__client_pb2.DatabricksValidationClusterWorkflow, _Mapping]] = ..., databricks_setup_workflow: _Optional[_Union[_databricks_setup_workflow__client_pb2.DatabricksSetupWorkflow, _Mapping]] = ..., materialization_scheduling_workflow: _Optional[_Union[_materialization_scheduling_workflow__client_pb2.MaterializationSchedulingWorkflow, _Mapping]] = ..., data_validation_workflow: _Optional[_Union[_data_validation_workflow__client_pb2.DataValidationWorkflow, _Mapping]] = ..., emr_validation_cluster_workflow: _Optional[_Union[_emr_validation_cluster_workflow__client_pb2.EMRValidationClusterWorkflowProto, _Mapping]] = ..., audit_log_processing_workflow: _Optional[_Union[_audit_log_processing_workflow__client_pb2.AuditLogProcessingWorkflow, _Mapping]] = ..., self_serve_consumption_delivery_workflow: _Optional[_Union[_self_serve_consumption_delivery_workflow__client_pb2.SelfServeConsumptionDeliveryWorkflow, _Mapping]] = ..., dynamo_import_table_workflow: _Optional[_Union[_dynamo_import_table_workflow__client_pb2.DynamoImportTableWorkflow, _Mapping]] = ..., consumption_metrics_exporter_workflow: _Optional[_Union[_consumption_metrics_exporter_workflow__client_pb2.ConsumptionMetricsExporterWorkflow, _Mapping]] = ..., ray_materialization_workflow: _Optional[_Union[_ray_materialization_workflow__client_pb2.RayMaterializationWorkflow, _Mapping]] = ..., vm_materialization_workflow: _Optional[_Union[_vm_materialization_workflow__client_pb2.VmMaterializationWorkflow, _Mapping]] = ..., plan_integration_test_status_workflow: _Optional[_Union[_plan_integration_test_status_workflow__client_pb2.PlanIntegrationTestStatusWorkflow, _Mapping]] = ..., cache_reconcile_task_workflow: _Optional[_Union[_cache_reconcile_workflow__client_pb2.CacheReconcileTaskWorkflow, _Mapping]] = ..., cache_reconcile_task_attempt_workflow: _Optional[_Union[_cache_reconcile_workflow__client_pb2.CacheReconcileTaskAttemptWorkflow, _Mapping]] = ..., test_workflow: _Optional[_Union[_test_workflow__client_pb2.TestWorkflow, _Mapping]] = ..., server_group_reconciliation_workflow: _Optional[_Union[_server_group_reconciliation_workflow__client_pb2.ServerGroupReconciliationWorkflow, _Mapping]] = ..., test_state_machine_workflow: _Optional[_Union[_test_state_machine_workflow__client_pb2.TestStateMachineWorkflowData, _Mapping]] = ..., server_group_state_machine_workflow: _Optional[_Union[_server_group_state_machine_workflow__client_pb2.ServerGroupStateMachineWorkflowData, _Mapping]] = ..., specific_workflow_serial: _Optional[int] = ..., last_exception: _Optional[_Union[KotlinException, _Mapping]] = ..., attempt_index: _Optional[int] = ..., initial_subcontainer: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class WorkflowType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
