from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.container.v1 import service_pb2 as _service_pb2
from chalk._gen.chalk.server.v1 import model_registry_pb2 as _model_registry_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
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

class TrainingRunStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRAINING_RUN_STATUS_UNSPECIFIED: _ClassVar[TrainingRunStatus]
    TRAINING_RUN_STATUS_QUEUED: _ClassVar[TrainingRunStatus]
    TRAINING_RUN_STATUS_WORKING: _ClassVar[TrainingRunStatus]
    TRAINING_RUN_STATUS_COMPLETED: _ClassVar[TrainingRunStatus]
    TRAINING_RUN_STATUS_FAILED: _ClassVar[TrainingRunStatus]
    TRAINING_RUN_STATUS_CANCELED: _ClassVar[TrainingRunStatus]

TRAINING_RUN_STATUS_UNSPECIFIED: TrainingRunStatus
TRAINING_RUN_STATUS_QUEUED: TrainingRunStatus
TRAINING_RUN_STATUS_WORKING: TrainingRunStatus
TRAINING_RUN_STATUS_COMPLETED: TrainingRunStatus
TRAINING_RUN_STATUS_FAILED: TrainingRunStatus
TRAINING_RUN_STATUS_CANCELED: TrainingRunStatus

class TrainingRunDataSource(_message.Message):
    __slots__ = ("dataset_name", "s3_uri", "input_sql")
    DATASET_NAME_FIELD_NUMBER: _ClassVar[int]
    S3_URI_FIELD_NUMBER: _ClassVar[int]
    INPUT_SQL_FIELD_NUMBER: _ClassVar[int]
    dataset_name: str
    s3_uri: str
    input_sql: str
    def __init__(
        self, dataset_name: _Optional[str] = ..., s3_uri: _Optional[str] = ..., input_sql: _Optional[str] = ...
    ) -> None: ...

class TrainingRun(_message.Message):
    __slots__ = (
        "id",
        "name",
        "status",
        "data",
        "config",
        "resources",
        "image",
        "env",
        "secret_refs",
        "meta_data",
        "error_message",
        "started_at",
        "finalized_at",
        "created_by",
        "created_at",
        "environment_id",
        "deployment_id",
    )
    class EnvEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class MetaDataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    SECRET_REFS_FIELD_NUMBER: _ClassVar[int]
    META_DATA_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    FINALIZED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    status: TrainingRunStatus
    data: TrainingRunDataSource
    config: _struct_pb2.Struct
    resources: _service_pb2.ResourceLimits
    image: str
    env: _containers.ScalarMap[str, str]
    secret_refs: _containers.RepeatedCompositeFieldContainer[_service_pb2.SecretRef]
    meta_data: _containers.MessageMap[str, _struct_pb2.Value]
    error_message: str
    started_at: _timestamp_pb2.Timestamp
    finalized_at: _timestamp_pb2.Timestamp
    created_by: str
    created_at: _timestamp_pb2.Timestamp
    environment_id: str
    deployment_id: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        status: _Optional[_Union[TrainingRunStatus, str]] = ...,
        data: _Optional[_Union[TrainingRunDataSource, _Mapping]] = ...,
        config: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        resources: _Optional[_Union[_service_pb2.ResourceLimits, _Mapping]] = ...,
        image: _Optional[str] = ...,
        env: _Optional[_Mapping[str, str]] = ...,
        secret_refs: _Optional[_Iterable[_Union[_service_pb2.SecretRef, _Mapping]]] = ...,
        meta_data: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
        error_message: _Optional[str] = ...,
        started_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        finalized_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        created_by: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
    ) -> None: ...

class CreateTrainingRunRequest(_message.Message):
    __slots__ = ("name", "data", "config", "resources", "image", "env", "secret_refs", "meta_data")
    class EnvEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class MetaDataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    SECRET_REFS_FIELD_NUMBER: _ClassVar[int]
    META_DATA_FIELD_NUMBER: _ClassVar[int]
    name: str
    data: TrainingRunDataSource
    config: _struct_pb2.Struct
    resources: _service_pb2.ResourceLimits
    image: str
    env: _containers.ScalarMap[str, str]
    secret_refs: _containers.RepeatedCompositeFieldContainer[_service_pb2.SecretRef]
    meta_data: _containers.MessageMap[str, _struct_pb2.Value]
    def __init__(
        self,
        name: _Optional[str] = ...,
        data: _Optional[_Union[TrainingRunDataSource, _Mapping]] = ...,
        config: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        resources: _Optional[_Union[_service_pb2.ResourceLimits, _Mapping]] = ...,
        image: _Optional[str] = ...,
        env: _Optional[_Mapping[str, str]] = ...,
        secret_refs: _Optional[_Iterable[_Union[_service_pb2.SecretRef, _Mapping]]] = ...,
        meta_data: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
    ) -> None: ...

class CreateTrainingRunResponse(_message.Message):
    __slots__ = ("training_run",)
    TRAINING_RUN_FIELD_NUMBER: _ClassVar[int]
    training_run: TrainingRun
    def __init__(self, training_run: _Optional[_Union[TrainingRun, _Mapping]] = ...) -> None: ...

class GetTrainingRunRequest(_message.Message):
    __slots__ = ("training_run_id",)
    TRAINING_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    training_run_id: str
    def __init__(self, training_run_id: _Optional[str] = ...) -> None: ...

class GetTrainingRunResponse(_message.Message):
    __slots__ = ("training_run",)
    TRAINING_RUN_FIELD_NUMBER: _ClassVar[int]
    training_run: TrainingRun
    def __init__(self, training_run: _Optional[_Union[TrainingRun, _Mapping]] = ...) -> None: ...

class ListTrainingRunsRequest(_message.Message):
    __slots__ = ("limit", "cursor", "name")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    limit: int
    cursor: str
    name: str
    def __init__(
        self, limit: _Optional[int] = ..., cursor: _Optional[str] = ..., name: _Optional[str] = ...
    ) -> None: ...

class ListTrainingRunsResponse(_message.Message):
    __slots__ = ("training_runs", "next_cursor")
    TRAINING_RUNS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    training_runs: _containers.RepeatedCompositeFieldContainer[TrainingRun]
    next_cursor: str
    def __init__(
        self,
        training_runs: _Optional[_Iterable[_Union[TrainingRun, _Mapping]]] = ...,
        next_cursor: _Optional[str] = ...,
    ) -> None: ...

class UpdateTrainingRunOperation(_message.Message):
    __slots__ = ("status", "error_message", "meta_data")
    class MetaDataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    META_DATA_FIELD_NUMBER: _ClassVar[int]
    status: TrainingRunStatus
    error_message: str
    meta_data: _containers.MessageMap[str, _struct_pb2.Value]
    def __init__(
        self,
        status: _Optional[_Union[TrainingRunStatus, str]] = ...,
        error_message: _Optional[str] = ...,
        meta_data: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
    ) -> None: ...

class UpdateTrainingRunRequest(_message.Message):
    __slots__ = ("training_run_id", "update", "update_mask")
    TRAINING_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    training_run_id: str
    update: UpdateTrainingRunOperation
    update_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        training_run_id: _Optional[str] = ...,
        update: _Optional[_Union[UpdateTrainingRunOperation, _Mapping]] = ...,
        update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class UpdateTrainingRunResponse(_message.Message):
    __slots__ = ("training_run",)
    TRAINING_RUN_FIELD_NUMBER: _ClassVar[int]
    training_run: TrainingRun
    def __init__(self, training_run: _Optional[_Union[TrainingRun, _Mapping]] = ...) -> None: ...

class CancelTrainingRunRequest(_message.Message):
    __slots__ = ("training_run_id",)
    TRAINING_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    training_run_id: str
    def __init__(self, training_run_id: _Optional[str] = ...) -> None: ...

class CancelTrainingRunResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CheckpointTrainingRunRequest(_message.Message):
    __slots__ = ("training_run_id", "file_names", "artifact_spec")
    TRAINING_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    FILE_NAMES_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_SPEC_FIELD_NUMBER: _ClassVar[int]
    training_run_id: str
    file_names: _containers.RepeatedScalarFieldContainer[str]
    artifact_spec: _struct_pb2.Struct
    def __init__(
        self,
        training_run_id: _Optional[str] = ...,
        file_names: _Optional[_Iterable[str]] = ...,
        artifact_spec: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
    ) -> None: ...

class CheckpointTrainingRunResponse(_message.Message):
    __slots__ = ("model_artifact_id", "upload_urls")
    class UploadUrlsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    MODEL_ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_URLS_FIELD_NUMBER: _ClassVar[int]
    model_artifact_id: str
    upload_urls: _containers.ScalarMap[str, str]
    def __init__(
        self, model_artifact_id: _Optional[str] = ..., upload_urls: _Optional[_Mapping[str, str]] = ...
    ) -> None: ...

class GetLatestCheckpointRequest(_message.Message):
    __slots__ = ("training_run_id",)
    TRAINING_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    training_run_id: str
    def __init__(self, training_run_id: _Optional[str] = ...) -> None: ...

class GetLatestCheckpointResponse(_message.Message):
    __slots__ = ("model_artifact",)
    MODEL_ARTIFACT_FIELD_NUMBER: _ClassVar[int]
    model_artifact: _model_registry_pb2.ModelArtifact
    def __init__(
        self, model_artifact: _Optional[_Union[_model_registry_pb2.ModelArtifact, _Mapping]] = ...
    ) -> None: ...

class ListCheckpointsRequest(_message.Message):
    __slots__ = ("training_run_id", "limit", "cursor")
    TRAINING_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    training_run_id: str
    limit: int
    cursor: str
    def __init__(
        self, training_run_id: _Optional[str] = ..., limit: _Optional[int] = ..., cursor: _Optional[str] = ...
    ) -> None: ...

class ListCheckpointsResponse(_message.Message):
    __slots__ = ("model_artifacts", "next_cursor")
    MODEL_ARTIFACTS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    model_artifacts: _containers.RepeatedCompositeFieldContainer[_model_registry_pb2.ModelArtifact]
    next_cursor: str
    def __init__(
        self,
        model_artifacts: _Optional[_Iterable[_Union[_model_registry_pb2.ModelArtifact, _Mapping]]] = ...,
        next_cursor: _Optional[str] = ...,
    ) -> None: ...

class TrainingMetric(_message.Message):
    __slots__ = ("name", "value", "step", "timestamp")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: float
    step: int
    timestamp: _timestamp_pb2.Timestamp
    def __init__(
        self,
        name: _Optional[str] = ...,
        value: _Optional[float] = ...,
        step: _Optional[int] = ...,
        timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ReportTrainingMetricsRequest(_message.Message):
    __slots__ = ("training_run_id", "metrics")
    TRAINING_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    training_run_id: str
    metrics: _containers.RepeatedCompositeFieldContainer[TrainingMetric]
    def __init__(
        self,
        training_run_id: _Optional[str] = ...,
        metrics: _Optional[_Iterable[_Union[TrainingMetric, _Mapping]]] = ...,
    ) -> None: ...

class ReportTrainingMetricsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
