import datetime

from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal.gen.v1 import error_pb2 as _error_pb2
from nominal.types import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProcedureVariableType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PROCEDURE_VARIABLE_TYPE_UNSPECIFIED: _ClassVar[ProcedureVariableType]
    PROCEDURE_VARIABLE_TYPE_ASSET_RID: _ClassVar[ProcedureVariableType]
    PROCEDURE_VARIABLE_TYPE_STRING: _ClassVar[ProcedureVariableType]
    PROCEDURE_VARIABLE_TYPE_DOUBLE: _ClassVar[ProcedureVariableType]
    PROCEDURE_VARIABLE_TYPE_BOOLEAN: _ClassVar[ProcedureVariableType]

class ProcedureVariableSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PROCEDURE_VARIABLE_SOURCE_UNSPECIFIED: _ClassVar[ProcedureVariableSource]
    PROCEDURE_VARIABLE_SOURCE_GLOBAL: _ClassVar[ProcedureVariableSource]
    PROCEDURE_VARIABLE_SOURCE_STEP: _ClassVar[ProcedureVariableSource]

class ProceduresServiceError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PROCEDURES_SERVICE_ERROR_UNSPECIFIED: _ClassVar[ProceduresServiceError]
    PROCEDURES_SERVICE_ERROR_NOT_FOUND: _ClassVar[ProceduresServiceError]
    PROCEDURES_SERVICE_ERROR_COMMIT_NOT_FOUND: _ClassVar[ProceduresServiceError]
    PROCEDURES_SERVICE_ERROR_CANNOT_MERGE_MAIN: _ClassVar[ProceduresServiceError]
    PROCEDURES_SERVICE_ERROR_CANNOT_COMMIT_TO_ARCHIVED_PROCEDURE: _ClassVar[ProceduresServiceError]
    PROCEDURES_SERVICE_ERROR_INVALID_GRAPH: _ClassVar[ProceduresServiceError]
    PROCEDURES_SERVICE_ERROR_INVALID_SEARCH_TOKEN: _ClassVar[ProceduresServiceError]

class SearchProceduresSortField(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SEARCH_PROCEDURES_SORT_FIELD_UNSPECIFIED: _ClassVar[SearchProceduresSortField]
    SEARCH_PROCEDURES_SORT_FIELD_NAME: _ClassVar[SearchProceduresSortField]
    SEARCH_PROCEDURES_SORT_FIELD_CREATED_AT: _ClassVar[SearchProceduresSortField]
    SEARCH_PROCEDURES_SORT_FIELD_UPDATED_AT: _ClassVar[SearchProceduresSortField]
PROCEDURE_VARIABLE_TYPE_UNSPECIFIED: ProcedureVariableType
PROCEDURE_VARIABLE_TYPE_ASSET_RID: ProcedureVariableType
PROCEDURE_VARIABLE_TYPE_STRING: ProcedureVariableType
PROCEDURE_VARIABLE_TYPE_DOUBLE: ProcedureVariableType
PROCEDURE_VARIABLE_TYPE_BOOLEAN: ProcedureVariableType
PROCEDURE_VARIABLE_SOURCE_UNSPECIFIED: ProcedureVariableSource
PROCEDURE_VARIABLE_SOURCE_GLOBAL: ProcedureVariableSource
PROCEDURE_VARIABLE_SOURCE_STEP: ProcedureVariableSource
PROCEDURES_SERVICE_ERROR_UNSPECIFIED: ProceduresServiceError
PROCEDURES_SERVICE_ERROR_NOT_FOUND: ProceduresServiceError
PROCEDURES_SERVICE_ERROR_COMMIT_NOT_FOUND: ProceduresServiceError
PROCEDURES_SERVICE_ERROR_CANNOT_MERGE_MAIN: ProceduresServiceError
PROCEDURES_SERVICE_ERROR_CANNOT_COMMIT_TO_ARCHIVED_PROCEDURE: ProceduresServiceError
PROCEDURES_SERVICE_ERROR_INVALID_GRAPH: ProceduresServiceError
PROCEDURES_SERVICE_ERROR_INVALID_SEARCH_TOKEN: ProceduresServiceError
SEARCH_PROCEDURES_SORT_FIELD_UNSPECIFIED: SearchProceduresSortField
SEARCH_PROCEDURES_SORT_FIELD_NAME: SearchProceduresSortField
SEARCH_PROCEDURES_SORT_FIELD_CREATED_AT: SearchProceduresSortField
SEARCH_PROCEDURES_SORT_FIELD_UPDATED_AT: SearchProceduresSortField

class ProcedureSectionNode(_message.Message):
    __slots__ = ("id", "title", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    description: str
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class ProcedureEventConfig(_message.Message):
    __slots__ = ("name", "description", "labels", "properties", "asset_variable_names")
    class PropertiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    ASSET_VARIABLE_NAMES_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    labels: _containers.RepeatedScalarFieldContainer[str]
    properties: _containers.ScalarMap[str, str]
    asset_variable_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., labels: _Optional[_Iterable[str]] = ..., properties: _Optional[_Mapping[str, str]] = ..., asset_variable_names: _Optional[_Iterable[str]] = ...) -> None: ...

class ProcedureStepNode(_message.Message):
    __slots__ = ("id", "title", "description", "is_required", "step", "event_config")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IS_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    EVENT_CONFIG_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    description: str
    is_required: bool
    step: TypedProcedureStepNode
    event_config: ProcedureEventConfig
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., is_required: bool = ..., step: _Optional[_Union[TypedProcedureStepNode, _Mapping]] = ..., event_config: _Optional[_Union[ProcedureEventConfig, _Mapping]] = ...) -> None: ...

class AssetFieldType(_message.Message):
    __slots__ = ("rid", "variable_name")
    RID_FIELD_NUMBER: _ClassVar[int]
    VARIABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    rid: str
    variable_name: str
    def __init__(self, rid: _Optional[str] = ..., variable_name: _Optional[str] = ...) -> None: ...

class AssetField(_message.Message):
    __slots__ = ("label", "rid", "variable_name", "variable_to_set", "is_required")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    RID_FIELD_NUMBER: _ClassVar[int]
    VARIABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    VARIABLE_TO_SET_FIELD_NUMBER: _ClassVar[int]
    IS_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    label: str
    rid: str
    variable_name: str
    variable_to_set: str
    is_required: bool
    def __init__(self, label: _Optional[str] = ..., rid: _Optional[str] = ..., variable_name: _Optional[str] = ..., variable_to_set: _Optional[str] = ..., is_required: bool = ...) -> None: ...

class CheckboxField(_message.Message):
    __slots__ = ("label", "is_required")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    IS_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    label: str
    is_required: bool
    def __init__(self, label: _Optional[str] = ..., is_required: bool = ...) -> None: ...

class CheckField(_message.Message):
    __slots__ = ("label", "checklist_rid", "check_rid", "commit_id")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    CHECKLIST_RID_FIELD_NUMBER: _ClassVar[int]
    CHECK_RID_FIELD_NUMBER: _ClassVar[int]
    COMMIT_ID_FIELD_NUMBER: _ClassVar[int]
    label: str
    checklist_rid: str
    check_rid: str
    commit_id: str
    def __init__(self, label: _Optional[str] = ..., checklist_rid: _Optional[str] = ..., check_rid: _Optional[str] = ..., commit_id: _Optional[str] = ...) -> None: ...

class StepField(_message.Message):
    __slots__ = ("asset", "checkbox", "check")
    ASSET_FIELD_NUMBER: _ClassVar[int]
    CHECKBOX_FIELD_NUMBER: _ClassVar[int]
    CHECK_FIELD_NUMBER: _ClassVar[int]
    asset: AssetField
    checkbox: CheckboxField
    check: CheckField
    def __init__(self, asset: _Optional[_Union[AssetField, _Mapping]] = ..., checkbox: _Optional[_Union[CheckboxField, _Mapping]] = ..., check: _Optional[_Union[CheckField, _Mapping]] = ...) -> None: ...

class FormStepNode(_message.Message):
    __slots__ = ("fields",)
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    fields: _containers.RepeatedCompositeFieldContainer[StepField]
    def __init__(self, fields: _Optional[_Iterable[_Union[StepField, _Mapping]]] = ...) -> None: ...

class TypedProcedureStepNode(_message.Message):
    __slots__ = ("form",)
    FORM_FIELD_NUMBER: _ClassVar[int]
    form: FormStepNode
    def __init__(self, form: _Optional[_Union[FormStepNode, _Mapping]] = ...) -> None: ...

class ProcedureNode(_message.Message):
    __slots__ = ("section", "step")
    SECTION_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    section: ProcedureSectionNode
    step: ProcedureStepNode
    def __init__(self, section: _Optional[_Union[ProcedureSectionNode, _Mapping]] = ..., step: _Optional[_Union[ProcedureStepNode, _Mapping]] = ...) -> None: ...

class ProcedureMetadata(_message.Message):
    __slots__ = ("rid", "title", "description", "labels", "properties", "is_archived", "is_published", "created_at", "created_by", "updated_at", "workspace")
    class PropertiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    RID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    IS_ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    IS_PUBLISHED_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    rid: str
    title: str
    description: str
    labels: _containers.RepeatedScalarFieldContainer[str]
    properties: _containers.ScalarMap[str, str]
    is_archived: bool
    is_published: bool
    created_at: _timestamp_pb2.Timestamp
    created_by: str
    updated_at: _timestamp_pb2.Timestamp
    workspace: str
    def __init__(self, rid: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., labels: _Optional[_Iterable[str]] = ..., properties: _Optional[_Mapping[str, str]] = ..., is_archived: bool = ..., is_published: bool = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., created_by: _Optional[str] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., workspace: _Optional[str] = ...) -> None: ...

class NodeList(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, value: _Optional[_Iterable[str]] = ...) -> None: ...

class ProcedureGraph(_message.Message):
    __slots__ = ("nodes", "root_nodes", "section_edges", "step_edges")
    class NodesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ProcedureNode
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ProcedureNode, _Mapping]] = ...) -> None: ...
    class SectionEdgesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: NodeList
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[NodeList, _Mapping]] = ...) -> None: ...
    class StepEdgesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: NodeList
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[NodeList, _Mapping]] = ...) -> None: ...
    NODES_FIELD_NUMBER: _ClassVar[int]
    ROOT_NODES_FIELD_NUMBER: _ClassVar[int]
    SECTION_EDGES_FIELD_NUMBER: _ClassVar[int]
    STEP_EDGES_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.MessageMap[str, ProcedureNode]
    root_nodes: _containers.RepeatedScalarFieldContainer[str]
    section_edges: _containers.MessageMap[str, NodeList]
    step_edges: _containers.MessageMap[str, NodeList]
    def __init__(self, nodes: _Optional[_Mapping[str, ProcedureNode]] = ..., root_nodes: _Optional[_Iterable[str]] = ..., section_edges: _Optional[_Mapping[str, NodeList]] = ..., step_edges: _Optional[_Mapping[str, NodeList]] = ...) -> None: ...

class ProcedureVariable(_message.Message):
    __slots__ = ("type", "source", "name")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    type: ProcedureVariableType
    source: ProcedureVariableSource
    name: str
    def __init__(self, type: _Optional[_Union[ProcedureVariableType, str]] = ..., source: _Optional[_Union[ProcedureVariableSource, str]] = ..., name: _Optional[str] = ...) -> None: ...

class Procedure(_message.Message):
    __slots__ = ("rid", "commit", "metadata", "graph", "variables")
    class VariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ProcedureVariable
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ProcedureVariable, _Mapping]] = ...) -> None: ...
    RID_FIELD_NUMBER: _ClassVar[int]
    COMMIT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    GRAPH_FIELD_NUMBER: _ClassVar[int]
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    rid: str
    commit: str
    metadata: ProcedureMetadata
    graph: ProcedureGraph
    variables: _containers.MessageMap[str, ProcedureVariable]
    def __init__(self, rid: _Optional[str] = ..., commit: _Optional[str] = ..., metadata: _Optional[_Union[ProcedureMetadata, _Mapping]] = ..., graph: _Optional[_Union[ProcedureGraph, _Mapping]] = ..., variables: _Optional[_Mapping[str, ProcedureVariable]] = ...) -> None: ...

class BranchOrCommit(_message.Message):
    __slots__ = ("branch", "commit")
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    COMMIT_FIELD_NUMBER: _ClassVar[int]
    branch: str
    commit: str
    def __init__(self, branch: _Optional[str] = ..., commit: _Optional[str] = ...) -> None: ...

class GetProcedureRequest(_message.Message):
    __slots__ = ("rid", "branch_or_commit", "include_display_graph")
    RID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_OR_COMMIT_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DISPLAY_GRAPH_FIELD_NUMBER: _ClassVar[int]
    rid: str
    branch_or_commit: BranchOrCommit
    include_display_graph: bool
    def __init__(self, rid: _Optional[str] = ..., branch_or_commit: _Optional[_Union[BranchOrCommit, _Mapping]] = ..., include_display_graph: bool = ...) -> None: ...

class ProcedureDisplayGraph(_message.Message):
    __slots__ = ("top_level_nodes", "section_to_sorted_children")
    class SectionToSortedChildrenEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: NodeList
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[NodeList, _Mapping]] = ...) -> None: ...
    TOP_LEVEL_NODES_FIELD_NUMBER: _ClassVar[int]
    SECTION_TO_SORTED_CHILDREN_FIELD_NUMBER: _ClassVar[int]
    top_level_nodes: _containers.RepeatedScalarFieldContainer[str]
    section_to_sorted_children: _containers.MessageMap[str, NodeList]
    def __init__(self, top_level_nodes: _Optional[_Iterable[str]] = ..., section_to_sorted_children: _Optional[_Mapping[str, NodeList]] = ...) -> None: ...

class ProcedureSearchQuery(_message.Message):
    __slots__ = ("search_text", "label", "property", "workspace", "created_by", "is_archived")
    class ProcedureSearchAndQuery(_message.Message):
        __slots__ = ("queries",)
        QUERIES_FIELD_NUMBER: _ClassVar[int]
        queries: _containers.RepeatedCompositeFieldContainer[ProcedureSearchQuery]
        def __init__(self, queries: _Optional[_Iterable[_Union[ProcedureSearchQuery, _Mapping]]] = ...) -> None: ...
    class ProcedureSearchOrQuery(_message.Message):
        __slots__ = ("queries",)
        QUERIES_FIELD_NUMBER: _ClassVar[int]
        queries: _containers.RepeatedCompositeFieldContainer[ProcedureSearchQuery]
        def __init__(self, queries: _Optional[_Iterable[_Union[ProcedureSearchQuery, _Mapping]]] = ...) -> None: ...
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    PROPERTY_FIELD_NUMBER: _ClassVar[int]
    AND_FIELD_NUMBER: _ClassVar[int]
    OR_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    IS_ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    search_text: str
    label: str
    property: _types_pb2.Property
    workspace: str
    created_by: str
    is_archived: bool
    def __init__(self, search_text: _Optional[str] = ..., label: _Optional[str] = ..., property: _Optional[_Union[_types_pb2.Property, _Mapping]] = ..., workspace: _Optional[str] = ..., created_by: _Optional[str] = ..., is_archived: bool = ..., **kwargs) -> None: ...

class GetProcedureResponse(_message.Message):
    __slots__ = ("procedure", "display_graph")
    PROCEDURE_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_GRAPH_FIELD_NUMBER: _ClassVar[int]
    procedure: Procedure
    display_graph: ProcedureDisplayGraph
    def __init__(self, procedure: _Optional[_Union[Procedure, _Mapping]] = ..., display_graph: _Optional[_Union[ProcedureDisplayGraph, _Mapping]] = ...) -> None: ...

class CreateProcedureRequest(_message.Message):
    __slots__ = ("title", "description", "labels", "properties", "graph", "variables", "is_published", "workspace", "commit_message")
    class PropertiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class VariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ProcedureVariable
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ProcedureVariable, _Mapping]] = ...) -> None: ...
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    GRAPH_FIELD_NUMBER: _ClassVar[int]
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    IS_PUBLISHED_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    COMMIT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    labels: _containers.RepeatedScalarFieldContainer[str]
    properties: _containers.ScalarMap[str, str]
    graph: ProcedureGraph
    variables: _containers.MessageMap[str, ProcedureVariable]
    is_published: bool
    workspace: str
    commit_message: str
    def __init__(self, title: _Optional[str] = ..., description: _Optional[str] = ..., labels: _Optional[_Iterable[str]] = ..., properties: _Optional[_Mapping[str, str]] = ..., graph: _Optional[_Union[ProcedureGraph, _Mapping]] = ..., variables: _Optional[_Mapping[str, ProcedureVariable]] = ..., is_published: bool = ..., workspace: _Optional[str] = ..., commit_message: _Optional[str] = ...) -> None: ...

class CreateProcedureResponse(_message.Message):
    __slots__ = ("procedure",)
    PROCEDURE_FIELD_NUMBER: _ClassVar[int]
    procedure: Procedure
    def __init__(self, procedure: _Optional[_Union[Procedure, _Mapping]] = ...) -> None: ...

class UpdateProcedureMetadataRequest(_message.Message):
    __slots__ = ("rid", "title", "description", "labels", "properties", "is_archived", "is_published")
    RID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    IS_ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    IS_PUBLISHED_FIELD_NUMBER: _ClassVar[int]
    rid: str
    title: str
    description: str
    labels: _types_pb2.LabelUpdateWrapper
    properties: _types_pb2.PropertyUpdateWrapper
    is_archived: bool
    is_published: bool
    def __init__(self, rid: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., labels: _Optional[_Union[_types_pb2.LabelUpdateWrapper, _Mapping]] = ..., properties: _Optional[_Union[_types_pb2.PropertyUpdateWrapper, _Mapping]] = ..., is_archived: bool = ..., is_published: bool = ...) -> None: ...

class UpdateProcedureMetadataResponse(_message.Message):
    __slots__ = ("procedure_metadata",)
    PROCEDURE_METADATA_FIELD_NUMBER: _ClassVar[int]
    procedure_metadata: ProcedureMetadata
    def __init__(self, procedure_metadata: _Optional[_Union[ProcedureMetadata, _Mapping]] = ...) -> None: ...

class MergeToMainRequest(_message.Message):
    __slots__ = ("rid", "branch", "latest_commit_on_main", "message")
    RID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    LATEST_COMMIT_ON_MAIN_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    rid: str
    branch: str
    latest_commit_on_main: str
    message: str
    def __init__(self, rid: _Optional[str] = ..., branch: _Optional[str] = ..., latest_commit_on_main: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class MergeToMainResponse(_message.Message):
    __slots__ = ("procedure",)
    PROCEDURE_FIELD_NUMBER: _ClassVar[int]
    procedure: Procedure
    def __init__(self, procedure: _Optional[_Union[Procedure, _Mapping]] = ...) -> None: ...

class SaveWorkingStateRequest(_message.Message):
    __slots__ = ("rid", "branch", "message", "latest_commit_on_branch", "graph", "variables")
    class VariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ProcedureVariable
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ProcedureVariable, _Mapping]] = ...) -> None: ...
    RID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LATEST_COMMIT_ON_BRANCH_FIELD_NUMBER: _ClassVar[int]
    GRAPH_FIELD_NUMBER: _ClassVar[int]
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    rid: str
    branch: str
    message: str
    latest_commit_on_branch: str
    graph: ProcedureGraph
    variables: _containers.MessageMap[str, ProcedureVariable]
    def __init__(self, rid: _Optional[str] = ..., branch: _Optional[str] = ..., message: _Optional[str] = ..., latest_commit_on_branch: _Optional[str] = ..., graph: _Optional[_Union[ProcedureGraph, _Mapping]] = ..., variables: _Optional[_Mapping[str, ProcedureVariable]] = ...) -> None: ...

class SaveWorkingStateResponse(_message.Message):
    __slots__ = ("procedure",)
    PROCEDURE_FIELD_NUMBER: _ClassVar[int]
    procedure: Procedure
    def __init__(self, procedure: _Optional[_Union[Procedure, _Mapping]] = ...) -> None: ...

class CommitRequest(_message.Message):
    __slots__ = ("rid", "branch", "latest_commit_on_branch", "message", "graph", "variables")
    class VariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ProcedureVariable
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ProcedureVariable, _Mapping]] = ...) -> None: ...
    RID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    LATEST_COMMIT_ON_BRANCH_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    GRAPH_FIELD_NUMBER: _ClassVar[int]
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    rid: str
    branch: str
    latest_commit_on_branch: str
    message: str
    graph: ProcedureGraph
    variables: _containers.MessageMap[str, ProcedureVariable]
    def __init__(self, rid: _Optional[str] = ..., branch: _Optional[str] = ..., latest_commit_on_branch: _Optional[str] = ..., message: _Optional[str] = ..., graph: _Optional[_Union[ProcedureGraph, _Mapping]] = ..., variables: _Optional[_Mapping[str, ProcedureVariable]] = ...) -> None: ...

class CommitResponse(_message.Message):
    __slots__ = ("procedure",)
    PROCEDURE_FIELD_NUMBER: _ClassVar[int]
    procedure: Procedure
    def __init__(self, procedure: _Optional[_Union[Procedure, _Mapping]] = ...) -> None: ...

class ParseNestedProcedureRequest(_message.Message):
    __slots__ = ("nested_procedure", "include_display_graph")
    NESTED_PROCEDURE_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DISPLAY_GRAPH_FIELD_NUMBER: _ClassVar[int]
    nested_procedure: NestedProcedure
    include_display_graph: bool
    def __init__(self, nested_procedure: _Optional[_Union[NestedProcedure, _Mapping]] = ..., include_display_graph: bool = ...) -> None: ...

class ParseNestedProcedureResponse(_message.Message):
    __slots__ = ("procedure", "display_graph")
    PROCEDURE_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_GRAPH_FIELD_NUMBER: _ClassVar[int]
    procedure: Procedure
    display_graph: ProcedureDisplayGraph
    def __init__(self, procedure: _Optional[_Union[Procedure, _Mapping]] = ..., display_graph: _Optional[_Union[ProcedureDisplayGraph, _Mapping]] = ...) -> None: ...

class NestedProcedure(_message.Message):
    __slots__ = ("title", "description", "steps", "variables")
    class VariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ProcedureVariable
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ProcedureVariable, _Mapping]] = ...) -> None: ...
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STEPS_FIELD_NUMBER: _ClassVar[int]
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    steps: _containers.RepeatedCompositeFieldContainer[NestedProcedureNode]
    variables: _containers.MessageMap[str, ProcedureVariable]
    def __init__(self, title: _Optional[str] = ..., description: _Optional[str] = ..., steps: _Optional[_Iterable[_Union[NestedProcedureNode, _Mapping]]] = ..., variables: _Optional[_Mapping[str, ProcedureVariable]] = ...) -> None: ...

class NestedProcedureNode(_message.Message):
    __slots__ = ("id", "title", "description", "steps", "fields", "event_config", "is_required")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STEPS_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    EVENT_CONFIG_FIELD_NUMBER: _ClassVar[int]
    IS_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    description: str
    steps: _containers.RepeatedCompositeFieldContainer[NestedProcedureNode]
    fields: _containers.RepeatedCompositeFieldContainer[StepField]
    event_config: ProcedureEventConfig
    is_required: bool
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., steps: _Optional[_Iterable[_Union[NestedProcedureNode, _Mapping]]] = ..., fields: _Optional[_Iterable[_Union[StepField, _Mapping]]] = ..., event_config: _Optional[_Union[ProcedureEventConfig, _Mapping]] = ..., is_required: bool = ...) -> None: ...

class GetProcedureAsNestedRequest(_message.Message):
    __slots__ = ("rid", "branch_or_commit")
    RID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_OR_COMMIT_FIELD_NUMBER: _ClassVar[int]
    rid: str
    branch_or_commit: BranchOrCommit
    def __init__(self, rid: _Optional[str] = ..., branch_or_commit: _Optional[_Union[BranchOrCommit, _Mapping]] = ...) -> None: ...

class GetProcedureAsNestedResponse(_message.Message):
    __slots__ = ("nested_procedure",)
    NESTED_PROCEDURE_FIELD_NUMBER: _ClassVar[int]
    nested_procedure: NestedProcedure
    def __init__(self, nested_procedure: _Optional[_Union[NestedProcedure, _Mapping]] = ...) -> None: ...

class SearchProceduresOptions(_message.Message):
    __slots__ = ("is_descending", "sort_field")
    IS_DESCENDING_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_FIELD_NUMBER: _ClassVar[int]
    is_descending: bool
    sort_field: SearchProceduresSortField
    def __init__(self, is_descending: bool = ..., sort_field: _Optional[_Union[SearchProceduresSortField, str]] = ...) -> None: ...

class SearchProceduresRequest(_message.Message):
    __slots__ = ("query", "search_options", "page_size", "next_page_token")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    SEARCH_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    query: ProcedureSearchQuery
    search_options: SearchProceduresOptions
    page_size: int
    next_page_token: str
    def __init__(self, query: _Optional[_Union[ProcedureSearchQuery, _Mapping]] = ..., search_options: _Optional[_Union[SearchProceduresOptions, _Mapping]] = ..., page_size: _Optional[int] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class SearchProceduresResponse(_message.Message):
    __slots__ = ("procedure_metadata", "next_page_token")
    PROCEDURE_METADATA_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    procedure_metadata: _containers.RepeatedCompositeFieldContainer[ProcedureMetadata]
    next_page_token: str
    def __init__(self, procedure_metadata: _Optional[_Iterable[_Union[ProcedureMetadata, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class ArchiveProceduresRequest(_message.Message):
    __slots__ = ("procedure_rids",)
    PROCEDURE_RIDS_FIELD_NUMBER: _ClassVar[int]
    procedure_rids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, procedure_rids: _Optional[_Iterable[str]] = ...) -> None: ...

class UnarchiveProceduresRequest(_message.Message):
    __slots__ = ("procedure_rids",)
    PROCEDURE_RIDS_FIELD_NUMBER: _ClassVar[int]
    procedure_rids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, procedure_rids: _Optional[_Iterable[str]] = ...) -> None: ...

class ArchiveProceduresResponse(_message.Message):
    __slots__ = ("procedure_rids",)
    PROCEDURE_RIDS_FIELD_NUMBER: _ClassVar[int]
    procedure_rids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, procedure_rids: _Optional[_Iterable[str]] = ...) -> None: ...

class UnarchiveProceduresResponse(_message.Message):
    __slots__ = ("procedure_rids",)
    PROCEDURE_RIDS_FIELD_NUMBER: _ClassVar[int]
    procedure_rids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, procedure_rids: _Optional[_Iterable[str]] = ...) -> None: ...
