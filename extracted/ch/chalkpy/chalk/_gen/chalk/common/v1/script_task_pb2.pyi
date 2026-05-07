from chalk._gen.chalk.common.v1 import resources_pb2 as _resources_pb2
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

class ScriptTaskStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SCRIPT_TASK_STATUS_UNSPECIFIED: _ClassVar[ScriptTaskStatus]
    SCRIPT_TASK_STATUS_QUEUED: _ClassVar[ScriptTaskStatus]
    SCRIPT_TASK_STATUS_WORKING: _ClassVar[ScriptTaskStatus]
    SCRIPT_TASK_STATUS_COMPLETED: _ClassVar[ScriptTaskStatus]
    SCRIPT_TASK_STATUS_FAILED: _ClassVar[ScriptTaskStatus]
    SCRIPT_TASK_STATUS_CANCELED: _ClassVar[ScriptTaskStatus]

class ScriptTaskKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SCRIPT_TASK_KIND_UNSPECIFIED: _ClassVar[ScriptTaskKind]
    SCRIPT_TASK_KIND_PYTHON_SCRIPT: _ClassVar[ScriptTaskKind]
    SCRIPT_TASK_KIND_TRAINING_RUN: _ClassVar[ScriptTaskKind]
    SCRIPT_TASK_KIND_METAPLAN: _ClassVar[ScriptTaskKind]

SCRIPT_TASK_STATUS_UNSPECIFIED: ScriptTaskStatus
SCRIPT_TASK_STATUS_QUEUED: ScriptTaskStatus
SCRIPT_TASK_STATUS_WORKING: ScriptTaskStatus
SCRIPT_TASK_STATUS_COMPLETED: ScriptTaskStatus
SCRIPT_TASK_STATUS_FAILED: ScriptTaskStatus
SCRIPT_TASK_STATUS_CANCELED: ScriptTaskStatus
SCRIPT_TASK_KIND_UNSPECIFIED: ScriptTaskKind
SCRIPT_TASK_KIND_PYTHON_SCRIPT: ScriptTaskKind
SCRIPT_TASK_KIND_TRAINING_RUN: ScriptTaskKind
SCRIPT_TASK_KIND_METAPLAN: ScriptTaskKind

class TrainingRunArgs(_message.Message):
    __slots__ = ("experiment_name",)
    EXPERIMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    experiment_name: str
    def __init__(self, experiment_name: _Optional[str] = ...) -> None: ...

class ScriptTaskRequest(_message.Message):
    __slots__ = (
        "function_reference_type",
        "function_reference",
        "arguments_json",
        "kind",
        "source_key",
        "branch",
        "resource_group",
        "resource_requests",
        "env_overrides",
        "enable_profiling",
        "max_retries",
        "completion_deadline",
        "training_run",
    )
    class EnvOverridesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    FUNCTION_REFERENCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    ARGUMENTS_JSON_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    SOURCE_KEY_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    ENV_OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    ENABLE_PROFILING_FIELD_NUMBER: _ClassVar[int]
    MAX_RETRIES_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_DEADLINE_FIELD_NUMBER: _ClassVar[int]
    TRAINING_RUN_FIELD_NUMBER: _ClassVar[int]
    function_reference_type: str
    function_reference: str
    arguments_json: str
    kind: ScriptTaskKind
    source_key: str
    branch: str
    resource_group: str
    resource_requests: _resources_pb2.ResourceRequirements
    env_overrides: _containers.ScalarMap[str, str]
    enable_profiling: bool
    max_retries: int
    completion_deadline: str
    training_run: TrainingRunArgs
    def __init__(
        self,
        function_reference_type: _Optional[str] = ...,
        function_reference: _Optional[str] = ...,
        arguments_json: _Optional[str] = ...,
        kind: _Optional[_Union[ScriptTaskKind, str]] = ...,
        source_key: _Optional[str] = ...,
        branch: _Optional[str] = ...,
        resource_group: _Optional[str] = ...,
        resource_requests: _Optional[_Union[_resources_pb2.ResourceRequirements, _Mapping]] = ...,
        env_overrides: _Optional[_Mapping[str, str]] = ...,
        enable_profiling: bool = ...,
        max_retries: _Optional[int] = ...,
        completion_deadline: _Optional[str] = ...,
        training_run: _Optional[_Union[TrainingRunArgs, _Mapping]] = ...,
    ) -> None: ...

class ScriptTaskFilter(_message.Message):
    __slots__ = ("statuses", "kinds", "task_id", "branch_name")
    STATUSES_FIELD_NUMBER: _ClassVar[int]
    KINDS_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    statuses: _containers.RepeatedScalarFieldContainer[ScriptTaskStatus]
    kinds: _containers.RepeatedScalarFieldContainer[ScriptTaskKind]
    task_id: str
    branch_name: str
    def __init__(
        self,
        statuses: _Optional[_Iterable[_Union[ScriptTaskStatus, str]]] = ...,
        kinds: _Optional[_Iterable[_Union[ScriptTaskKind, str]]] = ...,
        task_id: _Optional[str] = ...,
        branch_name: _Optional[str] = ...,
    ) -> None: ...
