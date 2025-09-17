import datetime

from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal.gen.v1 import error_pb2 as _error_pb2
from nominal.types import types_pb2 as _types_pb2
from nominal.versioning.v1 import versioning_pb2 as _versioning_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SearchProceduresSortField(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SEARCH_PROCEDURES_SORT_FIELD_UNSPECIFIED: _ClassVar[SearchProceduresSortField]
    SEARCH_PROCEDURES_SORT_FIELD_NAME: _ClassVar[SearchProceduresSortField]
    SEARCH_PROCEDURES_SORT_FIELD_CREATED_AT: _ClassVar[SearchProceduresSortField]
    SEARCH_PROCEDURES_SORT_FIELD_UPDATED_AT: _ClassVar[SearchProceduresSortField]

class ProceduresServiceError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PROCEDURES_SERVICE_ERROR_UNSPECIFIED: _ClassVar[ProceduresServiceError]
    PROCEDURES_SERVICE_ERROR_NOT_FOUND: _ClassVar[ProceduresServiceError]
    PROCEDURES_SERVICE_ERROR_COMMIT_NOT_FOUND: _ClassVar[ProceduresServiceError]
    PROCEDURES_SERVICE_ERROR_CANNOT_MERGE_MAIN: _ClassVar[ProceduresServiceError]
    PROCEDURES_SERVICE_ERROR_CANNOT_COMMIT_TO_ARCHIVED_PROCEDURE: _ClassVar[ProceduresServiceError]
    PROCEDURES_SERVICE_ERROR_INVALID_GRAPH: _ClassVar[ProceduresServiceError]
    PROCEDURES_SERVICE_ERROR_INVALID_SEARCH_TOKEN: _ClassVar[ProceduresServiceError]
SEARCH_PROCEDURES_SORT_FIELD_UNSPECIFIED: SearchProceduresSortField
SEARCH_PROCEDURES_SORT_FIELD_NAME: SearchProceduresSortField
SEARCH_PROCEDURES_SORT_FIELD_CREATED_AT: SearchProceduresSortField
SEARCH_PROCEDURES_SORT_FIELD_UPDATED_AT: SearchProceduresSortField
PROCEDURES_SERVICE_ERROR_UNSPECIFIED: ProceduresServiceError
PROCEDURES_SERVICE_ERROR_NOT_FOUND: ProceduresServiceError
PROCEDURES_SERVICE_ERROR_COMMIT_NOT_FOUND: ProceduresServiceError
PROCEDURES_SERVICE_ERROR_CANNOT_MERGE_MAIN: ProceduresServiceError
PROCEDURES_SERVICE_ERROR_CANNOT_COMMIT_TO_ARCHIVED_PROCEDURE: ProceduresServiceError
PROCEDURES_SERVICE_ERROR_INVALID_GRAPH: ProceduresServiceError
PROCEDURES_SERVICE_ERROR_INVALID_SEARCH_TOKEN: ProceduresServiceError

class ProcedureState(_message.Message):
    __slots__ = ("global_fields", "nodes", "section_edges", "step_edges")
    class GlobalFieldsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: FormField
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[FormField, _Mapping]] = ...) -> None: ...
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
    GLOBAL_FIELDS_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    SECTION_EDGES_FIELD_NUMBER: _ClassVar[int]
    STEP_EDGES_FIELD_NUMBER: _ClassVar[int]
    global_fields: _containers.MessageMap[str, FormField]
    nodes: _containers.MessageMap[str, ProcedureNode]
    section_edges: _containers.MessageMap[str, NodeList]
    step_edges: _containers.MessageMap[str, NodeList]
    def __init__(self, global_fields: _Optional[_Mapping[str, FormField]] = ..., nodes: _Optional[_Mapping[str, ProcedureNode]] = ..., section_edges: _Optional[_Mapping[str, NodeList]] = ..., step_edges: _Optional[_Mapping[str, NodeList]] = ...) -> None: ...

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

class NestedProcedure(_message.Message):
    __slots__ = ("title", "description", "steps", "global_fields")
    class GlobalFieldsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: FormField
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[FormField, _Mapping]] = ...) -> None: ...
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STEPS_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_FIELDS_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    steps: _containers.RepeatedCompositeFieldContainer[NestedProcedureNode]
    global_fields: _containers.MessageMap[str, FormField]
    def __init__(self, title: _Optional[str] = ..., description: _Optional[str] = ..., steps: _Optional[_Iterable[_Union[NestedProcedureNode, _Mapping]]] = ..., global_fields: _Optional[_Mapping[str, FormField]] = ...) -> None: ...

class NodeList(_message.Message):
    __slots__ = ("node_ids",)
    NODE_IDS_FIELD_NUMBER: _ClassVar[int]
    node_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, node_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ProcedureNode(_message.Message):
    __slots__ = ("section", "step")
    SECTION_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    section: ProcedureSectionNode
    step: ProcedureStepNode
    def __init__(self, section: _Optional[_Union[ProcedureSectionNode, _Mapping]] = ..., step: _Optional[_Union[ProcedureStepNode, _Mapping]] = ...) -> None: ...

class ProcedureSectionNode(_message.Message):
    __slots__ = ("id", "title", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    description: str
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class ProcedureStepNode(_message.Message):
    __slots__ = ("id", "title", "content", "output_id", "description", "is_required", "auto_start", "initial_auto_proceed_config", "success_condition", "completion_action_configs")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IS_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    AUTO_START_FIELD_NUMBER: _ClassVar[int]
    INITIAL_AUTO_PROCEED_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_CONDITION_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_ACTION_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    content: ProcedureStepContent
    output_id: str
    description: str
    is_required: bool
    auto_start: AutoStartConfig
    initial_auto_proceed_config: AutoProceedConfig
    success_condition: SuccessCondition
    completion_action_configs: _containers.RepeatedCompositeFieldContainer[CompletionActionConfig]
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., content: _Optional[_Union[ProcedureStepContent, _Mapping]] = ..., output_id: _Optional[str] = ..., description: _Optional[str] = ..., is_required: bool = ..., auto_start: _Optional[_Union[AutoStartConfig, _Mapping]] = ..., initial_auto_proceed_config: _Optional[_Union[AutoProceedConfig, _Mapping]] = ..., success_condition: _Optional[_Union[SuccessCondition, _Mapping]] = ..., completion_action_configs: _Optional[_Iterable[_Union[CompletionActionConfig, _Mapping]]] = ...) -> None: ...

class NestedProcedureNode(_message.Message):
    __slots__ = ("id", "title", "description", "steps", "step")
    class NestedStepNode(_message.Message):
        __slots__ = ("output_id", "is_required", "auto_start", "initial_auto_proceed_config", "success_condition", "completion_action_configs", "form", "start_ingest")
        OUTPUT_ID_FIELD_NUMBER: _ClassVar[int]
        IS_REQUIRED_FIELD_NUMBER: _ClassVar[int]
        AUTO_START_FIELD_NUMBER: _ClassVar[int]
        INITIAL_AUTO_PROCEED_CONFIG_FIELD_NUMBER: _ClassVar[int]
        SUCCESS_CONDITION_FIELD_NUMBER: _ClassVar[int]
        COMPLETION_ACTION_CONFIGS_FIELD_NUMBER: _ClassVar[int]
        FORM_FIELD_NUMBER: _ClassVar[int]
        START_INGEST_FIELD_NUMBER: _ClassVar[int]
        output_id: str
        is_required: bool
        auto_start: AutoStartConfig
        initial_auto_proceed_config: AutoProceedConfig
        success_condition: SuccessCondition
        completion_action_configs: _containers.RepeatedCompositeFieldContainer[CompletionActionConfig]
        form: FormStep
        start_ingest: StartIngestStep
        def __init__(self, output_id: _Optional[str] = ..., is_required: bool = ..., auto_start: _Optional[_Union[AutoStartConfig, _Mapping]] = ..., initial_auto_proceed_config: _Optional[_Union[AutoProceedConfig, _Mapping]] = ..., success_condition: _Optional[_Union[SuccessCondition, _Mapping]] = ..., completion_action_configs: _Optional[_Iterable[_Union[CompletionActionConfig, _Mapping]]] = ..., form: _Optional[_Union[FormStep, _Mapping]] = ..., start_ingest: _Optional[_Union[StartIngestStep, _Mapping]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STEPS_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    description: str
    steps: _containers.RepeatedCompositeFieldContainer[NestedProcedureNode]
    step: NestedProcedureNode.NestedStepNode
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., steps: _Optional[_Iterable[_Union[NestedProcedureNode, _Mapping]]] = ..., step: _Optional[_Union[NestedProcedureNode.NestedStepNode, _Mapping]] = ...) -> None: ...

class AutoStartConfig(_message.Message):
    __slots__ = ("all_parents", "disabled")
    class AllParents(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Disabled(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    ALL_PARENTS_FIELD_NUMBER: _ClassVar[int]
    DISABLED_FIELD_NUMBER: _ClassVar[int]
    all_parents: AutoStartConfig.AllParents
    disabled: AutoStartConfig.Disabled
    def __init__(self, all_parents: _Optional[_Union[AutoStartConfig.AllParents, _Mapping]] = ..., disabled: _Optional[_Union[AutoStartConfig.Disabled, _Mapping]] = ...) -> None: ...

class AutoProceedConfig(_message.Message):
    __slots__ = ("disabled", "enabled")
    class Disabled(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Enabled(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    DISABLED_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    disabled: AutoProceedConfig.Disabled
    enabled: AutoProceedConfig.Enabled
    def __init__(self, disabled: _Optional[_Union[AutoProceedConfig.Disabled, _Mapping]] = ..., enabled: _Optional[_Union[AutoProceedConfig.Enabled, _Mapping]] = ...) -> None: ...

class SuccessCondition(_message.Message):
    __slots__ = ("timer",)
    AND_FIELD_NUMBER: _ClassVar[int]
    TIMER_FIELD_NUMBER: _ClassVar[int]
    timer: TimerSuccessCondition
    def __init__(self, timer: _Optional[_Union[TimerSuccessCondition, _Mapping]] = ..., **kwargs) -> None: ...

class AndSuccessCondition(_message.Message):
    __slots__ = ("conditions",)
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    conditions: _containers.RepeatedCompositeFieldContainer[SuccessCondition]
    def __init__(self, conditions: _Optional[_Iterable[_Union[SuccessCondition, _Mapping]]] = ...) -> None: ...

class TimerSuccessCondition(_message.Message):
    __slots__ = ("duration_seconds",)
    DURATION_SECONDS_FIELD_NUMBER: _ClassVar[int]
    duration_seconds: int
    def __init__(self, duration_seconds: _Optional[int] = ...) -> None: ...

class CompletionActionConfig(_message.Message):
    __slots__ = ("create_event",)
    CREATE_EVENT_FIELD_NUMBER: _ClassVar[int]
    create_event: CreateEventConfig
    def __init__(self, create_event: _Optional[_Union[CreateEventConfig, _Mapping]] = ...) -> None: ...

class CreateEventConfig(_message.Message):
    __slots__ = ("name", "description", "labels", "properties", "asset_field_ids")
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
    ASSET_FIELD_IDS_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    labels: _containers.RepeatedScalarFieldContainer[str]
    properties: _containers.ScalarMap[str, str]
    asset_field_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., labels: _Optional[_Iterable[str]] = ..., properties: _Optional[_Mapping[str, str]] = ..., asset_field_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ProcedureStepContent(_message.Message):
    __slots__ = ("form", "start_ingest")
    FORM_FIELD_NUMBER: _ClassVar[int]
    START_INGEST_FIELD_NUMBER: _ClassVar[int]
    form: FormStep
    start_ingest: StartIngestStep
    def __init__(self, form: _Optional[_Union[FormStep, _Mapping]] = ..., start_ingest: _Optional[_Union[StartIngestStep, _Mapping]] = ...) -> None: ...

class FormStep(_message.Message):
    __slots__ = ("fields",)
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    fields: _containers.RepeatedCompositeFieldContainer[FormField]
    def __init__(self, fields: _Optional[_Iterable[_Union[FormField, _Mapping]]] = ...) -> None: ...

class StartIngestStep(_message.Message):
    __slots__ = ("asset", "data_scope", "ingest_type_config", "output_field_id")
    class DataScopeReference(_message.Message):
        __slots__ = ("constant",)
        CONSTANT_FIELD_NUMBER: _ClassVar[int]
        constant: str
        def __init__(self, constant: _Optional[str] = ...) -> None: ...
    class IngestTypeConfig(_message.Message):
        __slots__ = ("containerized_extractor",)
        class ContainerizedExtractorIngestConfig(_message.Message):
            __slots__ = ("rid",)
            RID_FIELD_NUMBER: _ClassVar[int]
            rid: str
            def __init__(self, rid: _Optional[str] = ...) -> None: ...
        CONTAINERIZED_EXTRACTOR_FIELD_NUMBER: _ClassVar[int]
        containerized_extractor: StartIngestStep.IngestTypeConfig.ContainerizedExtractorIngestConfig
        def __init__(self, containerized_extractor: _Optional[_Union[StartIngestStep.IngestTypeConfig.ContainerizedExtractorIngestConfig, _Mapping]] = ...) -> None: ...
    ASSET_FIELD_NUMBER: _ClassVar[int]
    DATA_SCOPE_FIELD_NUMBER: _ClassVar[int]
    INGEST_TYPE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_ID_FIELD_NUMBER: _ClassVar[int]
    asset: AssetReference
    data_scope: StartIngestStep.DataScopeReference
    ingest_type_config: StartIngestStep.IngestTypeConfig
    output_field_id: str
    def __init__(self, asset: _Optional[_Union[AssetReference, _Mapping]] = ..., data_scope: _Optional[_Union[StartIngestStep.DataScopeReference, _Mapping]] = ..., ingest_type_config: _Optional[_Union[StartIngestStep.IngestTypeConfig, _Mapping]] = ..., output_field_id: _Optional[str] = ...) -> None: ...

class FormField(_message.Message):
    __slots__ = ("id", "asset", "checkbox", "text", "int", "double", "single_enum", "multi_enum")
    ID_FIELD_NUMBER: _ClassVar[int]
    ASSET_FIELD_NUMBER: _ClassVar[int]
    CHECKBOX_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    INT_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_FIELD_NUMBER: _ClassVar[int]
    SINGLE_ENUM_FIELD_NUMBER: _ClassVar[int]
    MULTI_ENUM_FIELD_NUMBER: _ClassVar[int]
    id: str
    asset: AssetField
    checkbox: CheckboxField
    text: TextField
    int: IntField
    double: DoubleField
    single_enum: SingleEnumField
    multi_enum: MultiEnumField
    def __init__(self, id: _Optional[str] = ..., asset: _Optional[_Union[AssetField, _Mapping]] = ..., checkbox: _Optional[_Union[CheckboxField, _Mapping]] = ..., text: _Optional[_Union[TextField, _Mapping]] = ..., int: _Optional[_Union[IntField, _Mapping]] = ..., double: _Optional[_Union[DoubleField, _Mapping]] = ..., single_enum: _Optional[_Union[SingleEnumField, _Mapping]] = ..., multi_enum: _Optional[_Union[MultiEnumField, _Mapping]] = ...) -> None: ...

class AssetReference(_message.Message):
    __slots__ = ("rid", "field_id")
    RID_FIELD_NUMBER: _ClassVar[int]
    FIELD_ID_FIELD_NUMBER: _ClassVar[int]
    rid: str
    field_id: str
    def __init__(self, rid: _Optional[str] = ..., field_id: _Optional[str] = ...) -> None: ...

class PresetAssetFieldOptions(_message.Message):
    __slots__ = ("options", "default_option")
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_OPTION_FIELD_NUMBER: _ClassVar[int]
    options: _containers.RepeatedCompositeFieldContainer[AssetReference]
    default_option: AssetReference
    def __init__(self, options: _Optional[_Iterable[_Union[AssetReference, _Mapping]]] = ..., default_option: _Optional[_Union[AssetReference, _Mapping]] = ...) -> None: ...

class AssetField(_message.Message):
    __slots__ = ("label", "is_required", "preset_options")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    IS_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    PRESET_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    label: str
    is_required: bool
    preset_options: PresetAssetFieldOptions
    def __init__(self, label: _Optional[str] = ..., is_required: bool = ..., preset_options: _Optional[_Union[PresetAssetFieldOptions, _Mapping]] = ...) -> None: ...

class CheckboxField(_message.Message):
    __slots__ = ("label", "is_required")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    IS_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    label: str
    is_required: bool
    def __init__(self, label: _Optional[str] = ..., is_required: bool = ...) -> None: ...

class TextFieldSimpleInputType(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TextFieldMarkdownInputType(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TextField(_message.Message):
    __slots__ = ("label", "simple", "markdown", "min_length", "max_length")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    SIMPLE_FIELD_NUMBER: _ClassVar[int]
    MARKDOWN_FIELD_NUMBER: _ClassVar[int]
    MIN_LENGTH_FIELD_NUMBER: _ClassVar[int]
    MAX_LENGTH_FIELD_NUMBER: _ClassVar[int]
    label: str
    simple: TextFieldSimpleInputType
    markdown: TextFieldMarkdownInputType
    min_length: int
    max_length: int
    def __init__(self, label: _Optional[str] = ..., simple: _Optional[_Union[TextFieldSimpleInputType, _Mapping]] = ..., markdown: _Optional[_Union[TextFieldMarkdownInputType, _Mapping]] = ..., min_length: _Optional[int] = ..., max_length: _Optional[int] = ...) -> None: ...

class IntField(_message.Message):
    __slots__ = ("label", "is_required", "gte_value", "lte_value")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    IS_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    GTE_VALUE_FIELD_NUMBER: _ClassVar[int]
    LTE_VALUE_FIELD_NUMBER: _ClassVar[int]
    label: str
    is_required: bool
    gte_value: int
    lte_value: int
    def __init__(self, label: _Optional[str] = ..., is_required: bool = ..., gte_value: _Optional[int] = ..., lte_value: _Optional[int] = ...) -> None: ...

class DoubleField(_message.Message):
    __slots__ = ("label", "is_required", "gt_value", "gte_value", "lt_value", "lte_value")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    IS_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    GT_VALUE_FIELD_NUMBER: _ClassVar[int]
    GTE_VALUE_FIELD_NUMBER: _ClassVar[int]
    LT_VALUE_FIELD_NUMBER: _ClassVar[int]
    LTE_VALUE_FIELD_NUMBER: _ClassVar[int]
    label: str
    is_required: bool
    gt_value: float
    gte_value: float
    lt_value: float
    lte_value: float
    def __init__(self, label: _Optional[str] = ..., is_required: bool = ..., gt_value: _Optional[float] = ..., gte_value: _Optional[float] = ..., lt_value: _Optional[float] = ..., lte_value: _Optional[float] = ...) -> None: ...

class EnumFieldButtonsInputType(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class EnumFieldMenuInputType(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SingleEnumField(_message.Message):
    __slots__ = ("label", "options", "buttons", "dropdown", "allow_custom", "is_required")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    BUTTONS_FIELD_NUMBER: _ClassVar[int]
    DROPDOWN_FIELD_NUMBER: _ClassVar[int]
    ALLOW_CUSTOM_FIELD_NUMBER: _ClassVar[int]
    IS_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    label: str
    options: _containers.RepeatedScalarFieldContainer[str]
    buttons: EnumFieldButtonsInputType
    dropdown: EnumFieldMenuInputType
    allow_custom: bool
    is_required: bool
    def __init__(self, label: _Optional[str] = ..., options: _Optional[_Iterable[str]] = ..., buttons: _Optional[_Union[EnumFieldButtonsInputType, _Mapping]] = ..., dropdown: _Optional[_Union[EnumFieldMenuInputType, _Mapping]] = ..., allow_custom: bool = ..., is_required: bool = ...) -> None: ...

class MultiEnumField(_message.Message):
    __slots__ = ("label", "options", "buttons", "dropdown", "allow_custom", "min_count", "max_count")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    BUTTONS_FIELD_NUMBER: _ClassVar[int]
    DROPDOWN_FIELD_NUMBER: _ClassVar[int]
    ALLOW_CUSTOM_FIELD_NUMBER: _ClassVar[int]
    MIN_COUNT_FIELD_NUMBER: _ClassVar[int]
    MAX_COUNT_FIELD_NUMBER: _ClassVar[int]
    label: str
    options: _containers.RepeatedScalarFieldContainer[str]
    buttons: EnumFieldButtonsInputType
    dropdown: EnumFieldMenuInputType
    allow_custom: bool
    min_count: int
    max_count: int
    def __init__(self, label: _Optional[str] = ..., options: _Optional[_Iterable[str]] = ..., buttons: _Optional[_Union[EnumFieldButtonsInputType, _Mapping]] = ..., dropdown: _Optional[_Union[EnumFieldMenuInputType, _Mapping]] = ..., allow_custom: bool = ..., min_count: _Optional[int] = ..., max_count: _Optional[int] = ...) -> None: ...

class ProcedureMetadata(_message.Message):
    __slots__ = ("rid", "title", "description", "labels", "properties", "is_archived", "is_published", "created_at", "created_by", "updated_at", "updated_by", "workspace")
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
    UPDATED_BY_FIELD_NUMBER: _ClassVar[int]
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
    updated_by: str
    workspace: str
    def __init__(self, rid: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., labels: _Optional[_Iterable[str]] = ..., properties: _Optional[_Mapping[str, str]] = ..., is_archived: bool = ..., is_published: bool = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., created_by: _Optional[str] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_by: _Optional[str] = ..., workspace: _Optional[str] = ...) -> None: ...

class Procedure(_message.Message):
    __slots__ = ("rid", "commit", "metadata", "state")
    RID_FIELD_NUMBER: _ClassVar[int]
    COMMIT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    rid: str
    commit: str
    metadata: ProcedureMetadata
    state: ProcedureState
    def __init__(self, rid: _Optional[str] = ..., commit: _Optional[str] = ..., metadata: _Optional[_Union[ProcedureMetadata, _Mapping]] = ..., state: _Optional[_Union[ProcedureState, _Mapping]] = ...) -> None: ...

class CreateProcedureRequest(_message.Message):
    __slots__ = ("title", "description", "labels", "properties", "state", "is_published", "workspace", "commit_message", "initial_branch_name")
    class PropertiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    IS_PUBLISHED_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    COMMIT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    INITIAL_BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    labels: _containers.RepeatedScalarFieldContainer[str]
    properties: _containers.ScalarMap[str, str]
    state: ProcedureState
    is_published: bool
    workspace: str
    commit_message: str
    initial_branch_name: str
    def __init__(self, title: _Optional[str] = ..., description: _Optional[str] = ..., labels: _Optional[_Iterable[str]] = ..., properties: _Optional[_Mapping[str, str]] = ..., state: _Optional[_Union[ProcedureState, _Mapping]] = ..., is_published: bool = ..., workspace: _Optional[str] = ..., commit_message: _Optional[str] = ..., initial_branch_name: _Optional[str] = ...) -> None: ...

class CreateProcedureResponse(_message.Message):
    __slots__ = ("procedure", "branch_name")
    PROCEDURE_FIELD_NUMBER: _ClassVar[int]
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    procedure: Procedure
    branch_name: str
    def __init__(self, procedure: _Optional[_Union[Procedure, _Mapping]] = ..., branch_name: _Optional[str] = ...) -> None: ...

class GetProcedureRequest(_message.Message):
    __slots__ = ("rid", "branch_or_commit", "include_display_graph")
    RID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_OR_COMMIT_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DISPLAY_GRAPH_FIELD_NUMBER: _ClassVar[int]
    rid: str
    branch_or_commit: _versioning_pb2.BranchOrCommit
    include_display_graph: bool
    def __init__(self, rid: _Optional[str] = ..., branch_or_commit: _Optional[_Union[_versioning_pb2.BranchOrCommit, _Mapping]] = ..., include_display_graph: bool = ...) -> None: ...

class GetProcedureResponse(_message.Message):
    __slots__ = ("procedure", "display_graph")
    PROCEDURE_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_GRAPH_FIELD_NUMBER: _ClassVar[int]
    procedure: Procedure
    display_graph: ProcedureDisplayGraph
    def __init__(self, procedure: _Optional[_Union[Procedure, _Mapping]] = ..., display_graph: _Optional[_Union[ProcedureDisplayGraph, _Mapping]] = ...) -> None: ...

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

class GetProcedureAsNestedRequest(_message.Message):
    __slots__ = ("rid", "branch_or_commit")
    RID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_OR_COMMIT_FIELD_NUMBER: _ClassVar[int]
    rid: str
    branch_or_commit: _versioning_pb2.BranchOrCommit
    def __init__(self, rid: _Optional[str] = ..., branch_or_commit: _Optional[_Union[_versioning_pb2.BranchOrCommit, _Mapping]] = ...) -> None: ...

class GetProcedureAsNestedResponse(_message.Message):
    __slots__ = ("nested_procedure",)
    NESTED_PROCEDURE_FIELD_NUMBER: _ClassVar[int]
    nested_procedure: NestedProcedure
    def __init__(self, nested_procedure: _Optional[_Union[NestedProcedure, _Mapping]] = ...) -> None: ...

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
    __slots__ = ("rid", "branch", "message", "latest_commit_on_branch", "state")
    RID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LATEST_COMMIT_ON_BRANCH_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    rid: str
    branch: str
    message: str
    latest_commit_on_branch: str
    state: ProcedureState
    def __init__(self, rid: _Optional[str] = ..., branch: _Optional[str] = ..., message: _Optional[str] = ..., latest_commit_on_branch: _Optional[str] = ..., state: _Optional[_Union[ProcedureState, _Mapping]] = ...) -> None: ...

class SaveWorkingStateResponse(_message.Message):
    __slots__ = ("procedure",)
    PROCEDURE_FIELD_NUMBER: _ClassVar[int]
    procedure: Procedure
    def __init__(self, procedure: _Optional[_Union[Procedure, _Mapping]] = ...) -> None: ...

class CommitRequest(_message.Message):
    __slots__ = ("rid", "branch", "latest_commit_on_branch", "message", "state")
    RID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    LATEST_COMMIT_ON_BRANCH_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    rid: str
    branch: str
    latest_commit_on_branch: str
    message: str
    state: ProcedureState
    def __init__(self, rid: _Optional[str] = ..., branch: _Optional[str] = ..., latest_commit_on_branch: _Optional[str] = ..., message: _Optional[str] = ..., state: _Optional[_Union[ProcedureState, _Mapping]] = ...) -> None: ...

class CommitResponse(_message.Message):
    __slots__ = ("procedure",)
    PROCEDURE_FIELD_NUMBER: _ClassVar[int]
    procedure: Procedure
    def __init__(self, procedure: _Optional[_Union[Procedure, _Mapping]] = ...) -> None: ...

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

class SearchProceduresSortOptions(_message.Message):
    __slots__ = ("is_descending", "sort_field")
    IS_DESCENDING_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_FIELD_NUMBER: _ClassVar[int]
    is_descending: bool
    sort_field: SearchProceduresSortField
    def __init__(self, is_descending: bool = ..., sort_field: _Optional[_Union[SearchProceduresSortField, str]] = ...) -> None: ...

class SearchProceduresRequest(_message.Message):
    __slots__ = ("query", "sort_options", "page_size", "next_page_token")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    SORT_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    query: ProcedureSearchQuery
    sort_options: SearchProceduresSortOptions
    page_size: int
    next_page_token: str
    def __init__(self, query: _Optional[_Union[ProcedureSearchQuery, _Mapping]] = ..., sort_options: _Optional[_Union[SearchProceduresSortOptions, _Mapping]] = ..., page_size: _Optional[int] = ..., next_page_token: _Optional[str] = ...) -> None: ...

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

class ArchiveProceduresResponse(_message.Message):
    __slots__ = ("procedure_rids",)
    PROCEDURE_RIDS_FIELD_NUMBER: _ClassVar[int]
    procedure_rids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, procedure_rids: _Optional[_Iterable[str]] = ...) -> None: ...

class UnarchiveProceduresRequest(_message.Message):
    __slots__ = ("procedure_rids",)
    PROCEDURE_RIDS_FIELD_NUMBER: _ClassVar[int]
    procedure_rids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, procedure_rids: _Optional[_Iterable[str]] = ...) -> None: ...

class UnarchiveProceduresResponse(_message.Message):
    __slots__ = ("procedure_rids",)
    PROCEDURE_RIDS_FIELD_NUMBER: _ClassVar[int]
    procedure_rids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, procedure_rids: _Optional[_Iterable[str]] = ...) -> None: ...
