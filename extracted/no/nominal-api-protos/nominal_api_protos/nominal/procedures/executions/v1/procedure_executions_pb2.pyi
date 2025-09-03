import datetime

from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal.gen.v1 import error_pb2 as _error_pb2
from nominal.procedures.v1 import procedures_pb2 as _procedures_pb2
from nominal.types import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProcedureExecutionsServiceError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PROCEDURE_EXECUTIONS_SERVICE_ERROR_UNSPECIFIED: _ClassVar[ProcedureExecutionsServiceError]
    PROCEDURE_EXECUTIONS_SERVICE_ERROR_NOT_FOUND: _ClassVar[ProcedureExecutionsServiceError]
    PROCEDURE_EXECUTIONS_SERVICE_ERROR_PROC_NOT_FOUND: _ClassVar[ProcedureExecutionsServiceError]
    PROCEDURE_EXECUTIONS_SERVICE_ERROR_NODE_NOT_FOUND: _ClassVar[ProcedureExecutionsServiceError]
    PROCEDURE_EXECUTIONS_SERVICE_ERROR_INVALID_NODE: _ClassVar[ProcedureExecutionsServiceError]
    PROCEDURE_EXECUTIONS_SERVICE_ERROR_INVALID_GRAPH: _ClassVar[ProcedureExecutionsServiceError]
    PROCEDURE_EXECUTIONS_SERVICE_ERROR_INVALID_STEP_TRANSITION: _ClassVar[ProcedureExecutionsServiceError]
    PROCEDURE_EXECUTIONS_SERVICE_ERROR_INVALID_SEARCH_TOKEN: _ClassVar[ProcedureExecutionsServiceError]

class SearchProcedureExecutionsSortField(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SEARCH_PROCEDURE_EXECUTIONS_SORT_FIELD_UNSPECIFIED: _ClassVar[SearchProcedureExecutionsSortField]
    SEARCH_PROCEDURE_EXECUTIONS_SORT_FIELD_CREATED_AT: _ClassVar[SearchProcedureExecutionsSortField]
    SEARCH_PROCEDURE_EXECUTIONS_SORT_FIELD_STARTED_AT: _ClassVar[SearchProcedureExecutionsSortField]
    SEARCH_PROCEDURE_EXECUTIONS_SORT_FIELD_FINISHED_AT: _ClassVar[SearchProcedureExecutionsSortField]
    SEARCH_PROCEDURE_EXECUTIONS_SORT_FIELD_UPDATED_AT: _ClassVar[SearchProcedureExecutionsSortField]
PROCEDURE_EXECUTIONS_SERVICE_ERROR_UNSPECIFIED: ProcedureExecutionsServiceError
PROCEDURE_EXECUTIONS_SERVICE_ERROR_NOT_FOUND: ProcedureExecutionsServiceError
PROCEDURE_EXECUTIONS_SERVICE_ERROR_PROC_NOT_FOUND: ProcedureExecutionsServiceError
PROCEDURE_EXECUTIONS_SERVICE_ERROR_NODE_NOT_FOUND: ProcedureExecutionsServiceError
PROCEDURE_EXECUTIONS_SERVICE_ERROR_INVALID_NODE: ProcedureExecutionsServiceError
PROCEDURE_EXECUTIONS_SERVICE_ERROR_INVALID_GRAPH: ProcedureExecutionsServiceError
PROCEDURE_EXECUTIONS_SERVICE_ERROR_INVALID_STEP_TRANSITION: ProcedureExecutionsServiceError
PROCEDURE_EXECUTIONS_SERVICE_ERROR_INVALID_SEARCH_TOKEN: ProcedureExecutionsServiceError
SEARCH_PROCEDURE_EXECUTIONS_SORT_FIELD_UNSPECIFIED: SearchProcedureExecutionsSortField
SEARCH_PROCEDURE_EXECUTIONS_SORT_FIELD_CREATED_AT: SearchProcedureExecutionsSortField
SEARCH_PROCEDURE_EXECUTIONS_SORT_FIELD_STARTED_AT: SearchProcedureExecutionsSortField
SEARCH_PROCEDURE_EXECUTIONS_SORT_FIELD_FINISHED_AT: SearchProcedureExecutionsSortField
SEARCH_PROCEDURE_EXECUTIONS_SORT_FIELD_UPDATED_AT: SearchProcedureExecutionsSortField

class ProcedureExecutionMetadata(_message.Message):
    __slots__ = ("rid", "procedure_rid", "procedure_commit_id", "title", "description", "labels", "properties", "created_by", "created_at", "updated_at", "started_at", "finished_at", "is_aborted")
    class PropertiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    RID_FIELD_NUMBER: _ClassVar[int]
    PROCEDURE_RID_FIELD_NUMBER: _ClassVar[int]
    PROCEDURE_COMMIT_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    FINISHED_AT_FIELD_NUMBER: _ClassVar[int]
    IS_ABORTED_FIELD_NUMBER: _ClassVar[int]
    rid: str
    procedure_rid: str
    procedure_commit_id: str
    title: str
    description: str
    labels: _containers.RepeatedScalarFieldContainer[str]
    properties: _containers.ScalarMap[str, str]
    created_by: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    started_at: _timestamp_pb2.Timestamp
    finished_at: _timestamp_pb2.Timestamp
    is_aborted: bool
    def __init__(self, rid: _Optional[str] = ..., procedure_rid: _Optional[str] = ..., procedure_commit_id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., labels: _Optional[_Iterable[str]] = ..., properties: _Optional[_Mapping[str, str]] = ..., created_by: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., started_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., finished_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., is_aborted: bool = ...) -> None: ...

class ProcedureExecutionSectionNode(_message.Message):
    __slots__ = ("id", "node_id", "title", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    node_id: str
    title: str
    description: str
    def __init__(self, id: _Optional[str] = ..., node_id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class ProcedureStepNotStarted(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ProcedureStepInProgress(_message.Message):
    __slots__ = ("started_at", "started_by", "template_commit_id")
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    STARTED_BY_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_COMMIT_ID_FIELD_NUMBER: _ClassVar[int]
    started_at: _timestamp_pb2.Timestamp
    started_by: str
    template_commit_id: str
    def __init__(self, started_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., started_by: _Optional[str] = ..., template_commit_id: _Optional[str] = ...) -> None: ...

class ProcedureStepSkipped(_message.Message):
    __slots__ = ("skipped_at", "skipped_by", "skip_reason", "started_at", "started_by", "template_commit_id")
    SKIPPED_AT_FIELD_NUMBER: _ClassVar[int]
    SKIPPED_BY_FIELD_NUMBER: _ClassVar[int]
    SKIP_REASON_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    STARTED_BY_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_COMMIT_ID_FIELD_NUMBER: _ClassVar[int]
    skipped_at: _timestamp_pb2.Timestamp
    skipped_by: str
    skip_reason: str
    started_at: _timestamp_pb2.Timestamp
    started_by: str
    template_commit_id: str
    def __init__(self, skipped_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., skipped_by: _Optional[str] = ..., skip_reason: _Optional[str] = ..., started_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., started_by: _Optional[str] = ..., template_commit_id: _Optional[str] = ...) -> None: ...

class ProcedureStepCompleted(_message.Message):
    __slots__ = ("started_at", "started_by", "completed_at", "completed_by", "template_commit_id")
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    STARTED_BY_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_BY_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_COMMIT_ID_FIELD_NUMBER: _ClassVar[int]
    started_at: _timestamp_pb2.Timestamp
    started_by: str
    completed_at: _timestamp_pb2.Timestamp
    completed_by: str
    template_commit_id: str
    def __init__(self, started_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., started_by: _Optional[str] = ..., completed_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., completed_by: _Optional[str] = ..., template_commit_id: _Optional[str] = ...) -> None: ...

class ProcedureStepFailed(_message.Message):
    __slots__ = ("started_at", "started_by", "failed_at", "failed_by", "template_commit_id")
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    STARTED_BY_FIELD_NUMBER: _ClassVar[int]
    FAILED_AT_FIELD_NUMBER: _ClassVar[int]
    FAILED_BY_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_COMMIT_ID_FIELD_NUMBER: _ClassVar[int]
    started_at: _timestamp_pb2.Timestamp
    started_by: str
    failed_at: _timestamp_pb2.Timestamp
    failed_by: str
    template_commit_id: str
    def __init__(self, started_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., started_by: _Optional[str] = ..., failed_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., failed_by: _Optional[str] = ..., template_commit_id: _Optional[str] = ...) -> None: ...

class ProcedureStepStatus(_message.Message):
    __slots__ = ("not_started", "in_progress", "skipped", "completed", "failed")
    NOT_STARTED_FIELD_NUMBER: _ClassVar[int]
    IN_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    SKIPPED_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    not_started: ProcedureStepNotStarted
    in_progress: ProcedureStepInProgress
    skipped: ProcedureStepSkipped
    completed: ProcedureStepCompleted
    failed: ProcedureStepFailed
    def __init__(self, not_started: _Optional[_Union[ProcedureStepNotStarted, _Mapping]] = ..., in_progress: _Optional[_Union[ProcedureStepInProgress, _Mapping]] = ..., skipped: _Optional[_Union[ProcedureStepSkipped, _Mapping]] = ..., completed: _Optional[_Union[ProcedureStepCompleted, _Mapping]] = ..., failed: _Optional[_Union[ProcedureStepFailed, _Mapping]] = ...) -> None: ...

class TypedProcedureStepValue(_message.Message):
    __slots__ = ("form",)
    FORM_FIELD_NUMBER: _ClassVar[int]
    form: FormStepNodeValue
    def __init__(self, form: _Optional[_Union[FormStepNodeValue, _Mapping]] = ...) -> None: ...

class FormStepNodeValue(_message.Message):
    __slots__ = ("fields",)
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    fields: _containers.RepeatedCompositeFieldContainer[StepFieldValue]
    def __init__(self, fields: _Optional[_Iterable[_Union[StepFieldValue, _Mapping]]] = ...) -> None: ...

class AssetFieldValue(_message.Message):
    __slots__ = ("rid", "variable_name")
    RID_FIELD_NUMBER: _ClassVar[int]
    VARIABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    rid: str
    variable_name: str
    def __init__(self, rid: _Optional[str] = ..., variable_name: _Optional[str] = ...) -> None: ...

class CheckboxFieldValue(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: bool
    def __init__(self, value: bool = ...) -> None: ...

class CheckFieldValue(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StepFieldValue(_message.Message):
    __slots__ = ("asset", "checkbox", "check")
    ASSET_FIELD_NUMBER: _ClassVar[int]
    CHECKBOX_FIELD_NUMBER: _ClassVar[int]
    CHECK_FIELD_NUMBER: _ClassVar[int]
    asset: AssetFieldValue
    checkbox: CheckboxFieldValue
    check: CheckFieldValue
    def __init__(self, asset: _Optional[_Union[AssetFieldValue, _Mapping]] = ..., checkbox: _Optional[_Union[CheckboxFieldValue, _Mapping]] = ..., check: _Optional[_Union[CheckFieldValue, _Mapping]] = ...) -> None: ...

class ProcedureExecutionStepNode(_message.Message):
    __slots__ = ("id", "node_id", "title", "description", "status", "value", "is_outdated")
    ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    IS_OUTDATED_FIELD_NUMBER: _ClassVar[int]
    id: str
    node_id: str
    title: str
    description: str
    status: ProcedureStepStatus
    value: TypedProcedureStepValue
    is_outdated: bool
    def __init__(self, id: _Optional[str] = ..., node_id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., status: _Optional[_Union[ProcedureStepStatus, _Mapping]] = ..., value: _Optional[_Union[TypedProcedureStepValue, _Mapping]] = ..., is_outdated: bool = ...) -> None: ...

class ProcedureExecutionNode(_message.Message):
    __slots__ = ("section", "step")
    SECTION_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    section: ProcedureExecutionSectionNode
    step: ProcedureExecutionStepNode
    def __init__(self, section: _Optional[_Union[ProcedureExecutionSectionNode, _Mapping]] = ..., step: _Optional[_Union[ProcedureExecutionStepNode, _Mapping]] = ...) -> None: ...

class ProcedureExecutionGraph(_message.Message):
    __slots__ = ("nodes", "root_nodes", "section_edges", "step_edges")
    class NodesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ProcedureExecutionNode
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ProcedureExecutionNode, _Mapping]] = ...) -> None: ...
    class SectionEdgesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _procedures_pb2.NodeList
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_procedures_pb2.NodeList, _Mapping]] = ...) -> None: ...
    class StepEdgesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _procedures_pb2.NodeList
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_procedures_pb2.NodeList, _Mapping]] = ...) -> None: ...
    NODES_FIELD_NUMBER: _ClassVar[int]
    ROOT_NODES_FIELD_NUMBER: _ClassVar[int]
    SECTION_EDGES_FIELD_NUMBER: _ClassVar[int]
    STEP_EDGES_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.MessageMap[str, ProcedureExecutionNode]
    root_nodes: _containers.RepeatedScalarFieldContainer[str]
    section_edges: _containers.MessageMap[str, _procedures_pb2.NodeList]
    step_edges: _containers.MessageMap[str, _procedures_pb2.NodeList]
    def __init__(self, nodes: _Optional[_Mapping[str, ProcedureExecutionNode]] = ..., root_nodes: _Optional[_Iterable[str]] = ..., section_edges: _Optional[_Mapping[str, _procedures_pb2.NodeList]] = ..., step_edges: _Optional[_Mapping[str, _procedures_pb2.NodeList]] = ...) -> None: ...

class ProcedureExecutionVariableValue(_message.Message):
    __slots__ = ("asset_rid", "string_value", "double_value", "boolean_value")
    ASSET_RID_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
    BOOLEAN_VALUE_FIELD_NUMBER: _ClassVar[int]
    asset_rid: str
    string_value: str
    double_value: float
    boolean_value: bool
    def __init__(self, asset_rid: _Optional[str] = ..., string_value: _Optional[str] = ..., double_value: _Optional[float] = ..., boolean_value: bool = ...) -> None: ...

class ProcedureExecution(_message.Message):
    __slots__ = ("rid", "metadata", "graph", "variables")
    class VariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ProcedureExecutionVariableValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ProcedureExecutionVariableValue, _Mapping]] = ...) -> None: ...
    RID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    GRAPH_FIELD_NUMBER: _ClassVar[int]
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    rid: str
    metadata: ProcedureExecutionMetadata
    graph: ProcedureExecutionGraph
    variables: _containers.MessageMap[str, ProcedureExecutionVariableValue]
    def __init__(self, rid: _Optional[str] = ..., metadata: _Optional[_Union[ProcedureExecutionMetadata, _Mapping]] = ..., graph: _Optional[_Union[ProcedureExecutionGraph, _Mapping]] = ..., variables: _Optional[_Mapping[str, ProcedureExecutionVariableValue]] = ...) -> None: ...

class CreateProcedureExecutionRequest(_message.Message):
    __slots__ = ("procedure_rid", "procedure_commit_id", "title", "description")
    PROCEDURE_RID_FIELD_NUMBER: _ClassVar[int]
    PROCEDURE_COMMIT_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    procedure_rid: str
    procedure_commit_id: str
    title: str
    description: str
    def __init__(self, procedure_rid: _Optional[str] = ..., procedure_commit_id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class CreateProcedureExecutionResponse(_message.Message):
    __slots__ = ("procedure_execution",)
    PROCEDURE_EXECUTION_FIELD_NUMBER: _ClassVar[int]
    procedure_execution: ProcedureExecution
    def __init__(self, procedure_execution: _Optional[_Union[ProcedureExecution, _Mapping]] = ...) -> None: ...

class ProcedureExecutionVariablesUpdateWrapper(_message.Message):
    __slots__ = ("variables",)
    class VariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ProcedureExecutionVariableValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ProcedureExecutionVariableValue, _Mapping]] = ...) -> None: ...
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    variables: _containers.MessageMap[str, ProcedureExecutionVariableValue]
    def __init__(self, variables: _Optional[_Mapping[str, ProcedureExecutionVariableValue]] = ...) -> None: ...

class UpdateProcedureExecutionRequest(_message.Message):
    __slots__ = ("procedure_execution_rid", "title", "description", "commit_id", "labels", "properties", "graph", "variables", "is_aborted", "started_at", "finished_at")
    class ProcedureExecutionVariablesUpdateWrapper(_message.Message):
        __slots__ = ("variables",)
        class VariablesEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: ProcedureExecutionVariableValue
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ProcedureExecutionVariableValue, _Mapping]] = ...) -> None: ...
        VARIABLES_FIELD_NUMBER: _ClassVar[int]
        variables: _containers.MessageMap[str, ProcedureExecutionVariableValue]
        def __init__(self, variables: _Optional[_Mapping[str, ProcedureExecutionVariableValue]] = ...) -> None: ...
    PROCEDURE_EXECUTION_RID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    COMMIT_ID_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    GRAPH_FIELD_NUMBER: _ClassVar[int]
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    IS_ABORTED_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    FINISHED_AT_FIELD_NUMBER: _ClassVar[int]
    procedure_execution_rid: str
    title: str
    description: str
    commit_id: str
    labels: _types_pb2.LabelUpdateWrapper
    properties: _types_pb2.PropertyUpdateWrapper
    graph: ProcedureExecutionGraph
    variables: UpdateProcedureExecutionRequest.ProcedureExecutionVariablesUpdateWrapper
    is_aborted: bool
    started_at: _timestamp_pb2.Timestamp
    finished_at: _timestamp_pb2.Timestamp
    def __init__(self, procedure_execution_rid: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., commit_id: _Optional[str] = ..., labels: _Optional[_Union[_types_pb2.LabelUpdateWrapper, _Mapping]] = ..., properties: _Optional[_Union[_types_pb2.PropertyUpdateWrapper, _Mapping]] = ..., graph: _Optional[_Union[ProcedureExecutionGraph, _Mapping]] = ..., variables: _Optional[_Union[UpdateProcedureExecutionRequest.ProcedureExecutionVariablesUpdateWrapper, _Mapping]] = ..., is_aborted: bool = ..., started_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., finished_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class UpdateProcedureExecutionResponse(_message.Message):
    __slots__ = ("procedure_execution",)
    PROCEDURE_EXECUTION_FIELD_NUMBER: _ClassVar[int]
    procedure_execution: ProcedureExecution
    def __init__(self, procedure_execution: _Optional[_Union[ProcedureExecution, _Mapping]] = ...) -> None: ...

class UpdateStepRequest(_message.Message):
    __slots__ = ("procedure_execution_rid", "step_id", "status", "value")
    PROCEDURE_EXECUTION_RID_FIELD_NUMBER: _ClassVar[int]
    STEP_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    procedure_execution_rid: str
    step_id: str
    status: ProcedureStepStatus
    value: TypedProcedureStepValue
    def __init__(self, procedure_execution_rid: _Optional[str] = ..., step_id: _Optional[str] = ..., status: _Optional[_Union[ProcedureStepStatus, _Mapping]] = ..., value: _Optional[_Union[TypedProcedureStepValue, _Mapping]] = ...) -> None: ...

class UpdateStepResponse(_message.Message):
    __slots__ = ("procedure_execution", "event_rid")
    PROCEDURE_EXECUTION_FIELD_NUMBER: _ClassVar[int]
    EVENT_RID_FIELD_NUMBER: _ClassVar[int]
    procedure_execution: ProcedureExecution
    event_rid: str
    def __init__(self, procedure_execution: _Optional[_Union[ProcedureExecution, _Mapping]] = ..., event_rid: _Optional[str] = ...) -> None: ...

class GetProcedureExecutionRequest(_message.Message):
    __slots__ = ("procedure_execution_rid", "include_display_graph")
    PROCEDURE_EXECUTION_RID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DISPLAY_GRAPH_FIELD_NUMBER: _ClassVar[int]
    procedure_execution_rid: str
    include_display_graph: bool
    def __init__(self, procedure_execution_rid: _Optional[str] = ..., include_display_graph: bool = ...) -> None: ...

class GetProcedureExecutionResponse(_message.Message):
    __slots__ = ("procedure_execution", "display_graph")
    PROCEDURE_EXECUTION_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_GRAPH_FIELD_NUMBER: _ClassVar[int]
    procedure_execution: ProcedureExecution
    display_graph: _procedures_pb2.ProcedureDisplayGraph
    def __init__(self, procedure_execution: _Optional[_Union[ProcedureExecution, _Mapping]] = ..., display_graph: _Optional[_Union[_procedures_pb2.ProcedureDisplayGraph, _Mapping]] = ...) -> None: ...

class ProcedureExecutionSearchQuery(_message.Message):
    __slots__ = ("search_text", "label", "property", "workspace", "procedure_rid", "commit_id", "created_by")
    class ProcedureExecutionSearchAndQuery(_message.Message):
        __slots__ = ("queries",)
        QUERIES_FIELD_NUMBER: _ClassVar[int]
        queries: _containers.RepeatedCompositeFieldContainer[ProcedureExecutionSearchQuery]
        def __init__(self, queries: _Optional[_Iterable[_Union[ProcedureExecutionSearchQuery, _Mapping]]] = ...) -> None: ...
    class ProcedureExecutionSearchOrQuery(_message.Message):
        __slots__ = ("queries",)
        QUERIES_FIELD_NUMBER: _ClassVar[int]
        queries: _containers.RepeatedCompositeFieldContainer[ProcedureExecutionSearchQuery]
        def __init__(self, queries: _Optional[_Iterable[_Union[ProcedureExecutionSearchQuery, _Mapping]]] = ...) -> None: ...
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    PROPERTY_FIELD_NUMBER: _ClassVar[int]
    AND_FIELD_NUMBER: _ClassVar[int]
    OR_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    PROCEDURE_RID_FIELD_NUMBER: _ClassVar[int]
    COMMIT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    search_text: str
    label: str
    property: _types_pb2.Property
    workspace: str
    procedure_rid: str
    commit_id: str
    created_by: str
    def __init__(self, search_text: _Optional[str] = ..., label: _Optional[str] = ..., property: _Optional[_Union[_types_pb2.Property, _Mapping]] = ..., workspace: _Optional[str] = ..., procedure_rid: _Optional[str] = ..., commit_id: _Optional[str] = ..., created_by: _Optional[str] = ..., **kwargs) -> None: ...

class SearchProcedureExecutionsOptions(_message.Message):
    __slots__ = ("is_descending", "sort_field")
    IS_DESCENDING_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_FIELD_NUMBER: _ClassVar[int]
    is_descending: bool
    sort_field: SearchProcedureExecutionsSortField
    def __init__(self, is_descending: bool = ..., sort_field: _Optional[_Union[SearchProcedureExecutionsSortField, str]] = ...) -> None: ...

class SearchProcedureExecutionsRequest(_message.Message):
    __slots__ = ("query", "search_options", "page_size", "next_page_token")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    SEARCH_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    query: ProcedureExecutionSearchQuery
    search_options: SearchProcedureExecutionsOptions
    page_size: int
    next_page_token: str
    def __init__(self, query: _Optional[_Union[ProcedureExecutionSearchQuery, _Mapping]] = ..., search_options: _Optional[_Union[SearchProcedureExecutionsOptions, _Mapping]] = ..., page_size: _Optional[int] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class SearchProcedureExecutionsResponse(_message.Message):
    __slots__ = ("procedure_executions", "next_page_token")
    PROCEDURE_EXECUTIONS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    procedure_executions: _containers.RepeatedCompositeFieldContainer[ProcedureExecutionMetadata]
    next_page_token: str
    def __init__(self, procedure_executions: _Optional[_Iterable[_Union[ProcedureExecutionMetadata, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class BatchGetProcedureExecutionMetadataRequest(_message.Message):
    __slots__ = ("procedure_execution_rids",)
    PROCEDURE_EXECUTION_RIDS_FIELD_NUMBER: _ClassVar[int]
    procedure_execution_rids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, procedure_execution_rids: _Optional[_Iterable[str]] = ...) -> None: ...

class BatchGetProcedureExecutionMetadataResponse(_message.Message):
    __slots__ = ("procedure_executions",)
    PROCEDURE_EXECUTIONS_FIELD_NUMBER: _ClassVar[int]
    procedure_executions: _containers.RepeatedCompositeFieldContainer[ProcedureExecutionMetadata]
    def __init__(self, procedure_executions: _Optional[_Iterable[_Union[ProcedureExecutionMetadata, _Mapping]]] = ...) -> None: ...
