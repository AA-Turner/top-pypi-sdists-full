from tecton_proto.spark_api import jobs__client_pb2 as _jobs__client_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

BATCH: TaskType
BATCH_JOB: TaskTypeForDisplay
COMPACTION_JOB: TaskTypeForDisplay
DATASET_GENERATION: TaskType
DATASET_GENERATION_JOB: TaskTypeForDisplay
DELETION: TaskType
DELETION_JOB: TaskTypeForDisplay
DELTA_MAINTENANCE: TaskType
DELTA_MAINTENANCE_JOB: TaskTypeForDisplay
DESCRIPTOR: _descriptor.FileDescriptor
ENV_DATABRICKS_NOTEBOOK: SparkExecutionEnvironment
ENV_DATAPROC: SparkExecutionEnvironment
ENV_EMR: SparkExecutionEnvironment
ENV_UNSPECIFIED: SparkExecutionEnvironment
FEATURE_EXPORT: TaskType
FEATURE_EXPORT_JOB: TaskTypeForDisplay
ICEBERG_MAINTENANCE: TaskType
INGEST: TaskType
INGEST_JOB: TaskTypeForDisplay
PLAN_INTEGRATION_TEST_BATCH: TaskType
PLAN_INTEGRATION_TEST_BATCH_JOB: TaskTypeForDisplay
PLAN_INTEGRATION_TEST_STREAM: TaskType
PLAN_INTEGRATION_TEST_STREAM_JOB: TaskTypeForDisplay
STREAMING: TaskType
STREAMING_JOB: TaskTypeForDisplay
UNKNOWN: TaskType
UNKNOWN_JOB: TaskTypeForDisplay

class JobRequestTemplates(_message.Message):
    __slots__ = ["databricks_template", "emr_template"]
    DATABRICKS_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    EMR_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    databricks_template: _jobs__client_pb2.StartJobRequest
    emr_template: _jobs__client_pb2.StartJobRequest
    def __init__(self, databricks_template: _Optional[_Union[_jobs__client_pb2.StartJobRequest, _Mapping]] = ..., emr_template: _Optional[_Union[_jobs__client_pb2.StartJobRequest, _Mapping]] = ...) -> None: ...

class SparkClusterEnvironment(_message.Message):
    __slots__ = ["job_request_templates", "merged_user_deployment_settings_version", "spark_cluster_environment_version"]
    JOB_REQUEST_TEMPLATES_FIELD_NUMBER: _ClassVar[int]
    MERGED_USER_DEPLOYMENT_SETTINGS_VERSION_FIELD_NUMBER: _ClassVar[int]
    SPARK_CLUSTER_ENVIRONMENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    job_request_templates: JobRequestTemplates
    merged_user_deployment_settings_version: int
    spark_cluster_environment_version: int
    def __init__(self, spark_cluster_environment_version: _Optional[int] = ..., job_request_templates: _Optional[_Union[JobRequestTemplates, _Mapping]] = ..., merged_user_deployment_settings_version: _Optional[int] = ...) -> None: ...

class TaskType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class TaskTypeForDisplay(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class SparkExecutionEnvironment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
