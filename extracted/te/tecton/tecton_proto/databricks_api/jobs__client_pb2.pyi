from tecton_proto.spark_common import clusters__client_pb2 as _clusters__client_pb2
from tecton_proto.spark_common import libraries__client_pb2 as _libraries__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AccessControlList(_message.Message):
    __slots__ = ["group_name", "permission_level", "service_principal_name", "user_name"]
    class PermissionLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CAN_MANAGE: AccessControlList.PermissionLevel
    CAN_MANAGE_RUN: AccessControlList.PermissionLevel
    CAN_VIEW: AccessControlList.PermissionLevel
    GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    IS_OWNER: AccessControlList.PermissionLevel
    PERMISSION_LEVEL_FIELD_NUMBER: _ClassVar[int]
    SERVICE_PRINCIPAL_NAME_FIELD_NUMBER: _ClassVar[int]
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    group_name: str
    permission_level: AccessControlList.PermissionLevel
    service_principal_name: str
    user_name: str
    def __init__(self, user_name: _Optional[str] = ..., group_name: _Optional[str] = ..., service_principal_name: _Optional[str] = ..., permission_level: _Optional[_Union[AccessControlList.PermissionLevel, str]] = ...) -> None: ...

class ClusterInstance(_message.Message):
    __slots__ = ["cluster_id"]
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class ClusterSpec(_message.Message):
    __slots__ = ["existing_cluster_id", "libraries", "new_cluster"]
    EXISTING_CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    LIBRARIES_FIELD_NUMBER: _ClassVar[int]
    NEW_CLUSTER_FIELD_NUMBER: _ClassVar[int]
    existing_cluster_id: str
    libraries: _containers.RepeatedCompositeFieldContainer[RemoteLibrary]
    new_cluster: NewCluster
    def __init__(self, new_cluster: _Optional[_Union[NewCluster, _Mapping]] = ..., existing_cluster_id: _Optional[str] = ..., libraries: _Optional[_Iterable[_Union[RemoteLibrary, _Mapping]]] = ...) -> None: ...

class JobsCancelRunRequest(_message.Message):
    __slots__ = ["run_id"]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    run_id: int
    def __init__(self, run_id: _Optional[int] = ...) -> None: ...

class JobsRunsGetRequest(_message.Message):
    __slots__ = ["run_id"]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    run_id: int
    def __init__(self, run_id: _Optional[int] = ...) -> None: ...

class JobsRunsGetResponse(_message.Message):
    __slots__ = ["cluster_instance", "end_time", "execution_duration", "job_id", "run_id", "run_page_url", "setup_duration", "start_time", "state"]
    CLUSTER_INSTANCE_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_DURATION_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_PAGE_URL_FIELD_NUMBER: _ClassVar[int]
    SETUP_DURATION_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    cluster_instance: ClusterInstance
    end_time: int
    execution_duration: int
    job_id: int
    run_id: int
    run_page_url: str
    setup_duration: int
    start_time: int
    state: RunState
    def __init__(self, run_id: _Optional[int] = ..., job_id: _Optional[int] = ..., execution_duration: _Optional[int] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., setup_duration: _Optional[int] = ..., cluster_instance: _Optional[_Union[ClusterInstance, _Mapping]] = ..., run_page_url: _Optional[str] = ..., state: _Optional[_Union[RunState, _Mapping]] = ...) -> None: ...

class JobsRunsListRequest(_message.Message):
    __slots__ = ["active_only", "limit", "offset", "run_type"]
    ACTIVE_ONLY_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    RUN_TYPE_FIELD_NUMBER: _ClassVar[int]
    active_only: bool
    limit: int
    offset: int
    run_type: str
    def __init__(self, offset: _Optional[int] = ..., active_only: bool = ..., run_type: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...

class JobsRunsListResponse(_message.Message):
    __slots__ = ["has_more", "runs"]
    HAS_MORE_FIELD_NUMBER: _ClassVar[int]
    RUNS_FIELD_NUMBER: _ClassVar[int]
    has_more: bool
    runs: _containers.RepeatedCompositeFieldContainer[Run]
    def __init__(self, runs: _Optional[_Iterable[_Union[Run, _Mapping]]] = ..., has_more: bool = ...) -> None: ...

class JobsRunsSubmitRequest(_message.Message):
    __slots__ = ["access_control_list", "idempotency_token", "run_as", "run_name", "tasks", "timeout_seconds"]
    ACCESS_CONTROL_LIST_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_TOKEN_FIELD_NUMBER: _ClassVar[int]
    RUN_AS_FIELD_NUMBER: _ClassVar[int]
    RUN_NAME_FIELD_NUMBER: _ClassVar[int]
    TASKS_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_SECONDS_FIELD_NUMBER: _ClassVar[int]
    access_control_list: _containers.RepeatedCompositeFieldContainer[AccessControlList]
    idempotency_token: str
    run_as: RunAs
    run_name: str
    tasks: _containers.RepeatedCompositeFieldContainer[Task]
    timeout_seconds: int
    def __init__(self, run_name: _Optional[str] = ..., timeout_seconds: _Optional[int] = ..., idempotency_token: _Optional[str] = ..., tasks: _Optional[_Iterable[_Union[Task, _Mapping]]] = ..., access_control_list: _Optional[_Iterable[_Union[AccessControlList, _Mapping]]] = ..., run_as: _Optional[_Union[RunAs, _Mapping]] = ...) -> None: ...

class JobsRunsSubmitResponse(_message.Message):
    __slots__ = ["run_id"]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    run_id: int
    def __init__(self, run_id: _Optional[int] = ...) -> None: ...

class LegacyJobsRunsSubmitRequest(_message.Message):
    __slots__ = ["existing_cluster_id", "libraries", "new_cluster", "notebook_task", "run_name", "tasks", "timeout_seconds"]
    EXISTING_CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    LIBRARIES_FIELD_NUMBER: _ClassVar[int]
    NEW_CLUSTER_FIELD_NUMBER: _ClassVar[int]
    NOTEBOOK_TASK_FIELD_NUMBER: _ClassVar[int]
    RUN_NAME_FIELD_NUMBER: _ClassVar[int]
    TASKS_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_SECONDS_FIELD_NUMBER: _ClassVar[int]
    existing_cluster_id: str
    libraries: _containers.RepeatedCompositeFieldContainer[RemoteLibrary]
    new_cluster: _clusters__client_pb2.NewCluster
    notebook_task: NotebookTask
    run_name: str
    tasks: _containers.RepeatedCompositeFieldContainer[Task]
    timeout_seconds: int
    def __init__(self, new_cluster: _Optional[_Union[_clusters__client_pb2.NewCluster, _Mapping]] = ..., existing_cluster_id: _Optional[str] = ..., notebook_task: _Optional[_Union[NotebookTask, _Mapping]] = ..., run_name: _Optional[str] = ..., libraries: _Optional[_Iterable[_Union[RemoteLibrary, _Mapping]]] = ..., timeout_seconds: _Optional[int] = ..., tasks: _Optional[_Iterable[_Union[Task, _Mapping]]] = ...) -> None: ...

class NewCluster(_message.Message):
    __slots__ = ["custom_tags"]
    class CustomTagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CUSTOM_TAGS_FIELD_NUMBER: _ClassVar[int]
    custom_tags: _containers.ScalarMap[str, str]
    def __init__(self, custom_tags: _Optional[_Mapping[str, str]] = ...) -> None: ...

class NotebookTask(_message.Message):
    __slots__ = ["base_parameters", "notebook_path"]
    class BaseParametersEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    BASE_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    NOTEBOOK_PATH_FIELD_NUMBER: _ClassVar[int]
    base_parameters: _containers.ScalarMap[str, str]
    notebook_path: str
    def __init__(self, notebook_path: _Optional[str] = ..., base_parameters: _Optional[_Mapping[str, str]] = ...) -> None: ...

class RemoteLibrary(_message.Message):
    __slots__ = ["egg", "jar", "maven", "pypi", "whl"]
    EGG_FIELD_NUMBER: _ClassVar[int]
    JAR_FIELD_NUMBER: _ClassVar[int]
    MAVEN_FIELD_NUMBER: _ClassVar[int]
    PYPI_FIELD_NUMBER: _ClassVar[int]
    WHL_FIELD_NUMBER: _ClassVar[int]
    egg: str
    jar: str
    maven: _libraries__client_pb2.MavenLibrary
    pypi: _libraries__client_pb2.PyPiLibrary
    whl: str
    def __init__(self, jar: _Optional[str] = ..., egg: _Optional[str] = ..., whl: _Optional[str] = ..., maven: _Optional[_Union[_libraries__client_pb2.MavenLibrary, _Mapping]] = ..., pypi: _Optional[_Union[_libraries__client_pb2.PyPiLibrary, _Mapping]] = ...) -> None: ...

class Run(_message.Message):
    __slots__ = ["cluster_spec", "job_id", "run_id", "run_page_url", "state"]
    CLUSTER_SPEC_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_PAGE_URL_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    cluster_spec: ClusterSpec
    job_id: int
    run_id: int
    run_page_url: str
    state: RunState
    def __init__(self, job_id: _Optional[int] = ..., run_id: _Optional[int] = ..., state: _Optional[_Union[RunState, _Mapping]] = ..., cluster_spec: _Optional[_Union[ClusterSpec, _Mapping]] = ..., run_page_url: _Optional[str] = ...) -> None: ...

class RunAs(_message.Message):
    __slots__ = ["service_principal_name", "user_name"]
    SERVICE_PRINCIPAL_NAME_FIELD_NUMBER: _ClassVar[int]
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    service_principal_name: str
    user_name: str
    def __init__(self, user_name: _Optional[str] = ..., service_principal_name: _Optional[str] = ...) -> None: ...

class RunState(_message.Message):
    __slots__ = ["life_cycle_state", "result_state", "state_message"]
    class RunLifeCycleState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class RunResultState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CANCELED: RunState.RunResultState
    FAILED: RunState.RunResultState
    INTERNAL_ERROR: RunState.RunLifeCycleState
    LIFE_CYCLE_STATE_FIELD_NUMBER: _ClassVar[int]
    PENDING: RunState.RunLifeCycleState
    RESULT_STATE_FIELD_NUMBER: _ClassVar[int]
    RUNNING: RunState.RunLifeCycleState
    SKIPPED: RunState.RunLifeCycleState
    STATE_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS: RunState.RunResultState
    TERMINATED: RunState.RunLifeCycleState
    TERMINATING: RunState.RunLifeCycleState
    TIMEDOUT: RunState.RunResultState
    UNKNOWN_RUN_LIFE_CYCLE_STATE: RunState.RunLifeCycleState
    UNKNOWN_RUN_RESULT_STATE: RunState.RunResultState
    life_cycle_state: RunState.RunLifeCycleState
    result_state: RunState.RunResultState
    state_message: str
    def __init__(self, life_cycle_state: _Optional[_Union[RunState.RunLifeCycleState, str]] = ..., result_state: _Optional[_Union[RunState.RunResultState, str]] = ..., state_message: _Optional[str] = ...) -> None: ...

class Task(_message.Message):
    __slots__ = ["depends_on", "description", "existing_cluster_id", "libraries", "new_cluster", "notebook_task", "task_key", "timeout_seconds"]
    DEPENDS_ON_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EXISTING_CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    LIBRARIES_FIELD_NUMBER: _ClassVar[int]
    NEW_CLUSTER_FIELD_NUMBER: _ClassVar[int]
    NOTEBOOK_TASK_FIELD_NUMBER: _ClassVar[int]
    TASK_KEY_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_SECONDS_FIELD_NUMBER: _ClassVar[int]
    depends_on: _containers.RepeatedCompositeFieldContainer[Task]
    description: str
    existing_cluster_id: str
    libraries: _containers.RepeatedCompositeFieldContainer[RemoteLibrary]
    new_cluster: _clusters__client_pb2.NewCluster
    notebook_task: NotebookTask
    task_key: str
    timeout_seconds: int
    def __init__(self, task_key: _Optional[str] = ..., description: _Optional[str] = ..., depends_on: _Optional[_Iterable[_Union[Task, _Mapping]]] = ..., new_cluster: _Optional[_Union[_clusters__client_pb2.NewCluster, _Mapping]] = ..., existing_cluster_id: _Optional[str] = ..., notebook_task: _Optional[_Union[NotebookTask, _Mapping]] = ..., libraries: _Optional[_Iterable[_Union[RemoteLibrary, _Mapping]]] = ..., timeout_seconds: _Optional[int] = ...) -> None: ...
