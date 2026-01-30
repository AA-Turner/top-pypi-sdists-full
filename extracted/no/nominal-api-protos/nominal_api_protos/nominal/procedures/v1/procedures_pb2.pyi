import datetime

from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal.gen.v1 import error_pb2 as _error_pb2
from nominal.procedures.v1 import id_format_pb2 as _id_format_pb2
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
    __slots__ = ("global_fields", "new_global_fields", "nodes", "section_edges", "step_edges")
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
    NEW_GLOBAL_FIELDS_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    SECTION_EDGES_FIELD_NUMBER: _ClassVar[int]
    STEP_EDGES_FIELD_NUMBER: _ClassVar[int]
    global_fields: _containers.MessageMap[str, FormField]
    new_global_fields: _containers.RepeatedCompositeFieldContainer[FormField]
    nodes: _containers.MessageMap[str, ProcedureNode]
    section_edges: _containers.MessageMap[str, NodeList]
    step_edges: _containers.MessageMap[str, NodeList]
    def __init__(self, global_fields: _Optional[_Mapping[str, FormField]] = ..., new_global_fields: _Optional[_Iterable[_Union[FormField, _Mapping]]] = ..., nodes: _Optional[_Mapping[str, ProcedureNode]] = ..., section_edges: _Optional[_Mapping[str, NodeList]] = ..., step_edges: _Optional[_Mapping[str, NodeList]] = ...) -> None: ...

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
    __slots__ = ("title", "description", "steps", "global_fields", "new_global_fields")
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
    NEW_GLOBAL_FIELDS_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    steps: _containers.RepeatedCompositeFieldContainer[NestedProcedureNode]
    global_fields: _containers.MessageMap[str, FormField]
    new_global_fields: _containers.RepeatedCompositeFieldContainer[FormField]
    def __init__(self, title: _Optional[str] = ..., description: _Optional[str] = ..., steps: _Optional[_Iterable[_Union[NestedProcedureNode, _Mapping]]] = ..., global_fields: _Optional[_Mapping[str, FormField]] = ..., new_global_fields: _Optional[_Iterable[_Union[FormField, _Mapping]]] = ...) -> None: ...

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
    __slots__ = ("id", "title", "content", "description", "is_required", "auto_start", "initial_auto_proceed_config", "success_condition", "completion_action_configs", "attachments")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IS_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    AUTO_START_FIELD_NUMBER: _ClassVar[int]
    INITIAL_AUTO_PROCEED_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_CONDITION_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_ACTION_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENTS_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    content: ProcedureStepContent
    description: str
    is_required: bool
    auto_start: AutoStartConfig
    initial_auto_proceed_config: AutoProceedConfig
    success_condition: SuccessCondition
    completion_action_configs: _containers.RepeatedCompositeFieldContainer[CompletionActionConfig]
    attachments: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., content: _Optional[_Union[ProcedureStepContent, _Mapping]] = ..., description: _Optional[str] = ..., is_required: bool = ..., auto_start: _Optional[_Union[AutoStartConfig, _Mapping]] = ..., initial_auto_proceed_config: _Optional[_Union[AutoProceedConfig, _Mapping]] = ..., success_condition: _Optional[_Union[SuccessCondition, _Mapping]] = ..., completion_action_configs: _Optional[_Iterable[_Union[CompletionActionConfig, _Mapping]]] = ..., attachments: _Optional[_Iterable[str]] = ...) -> None: ...

class NestedProcedureNode(_message.Message):
    __slots__ = ("id", "title", "description", "steps", "step")
    class NestedStepNode(_message.Message):
        __slots__ = ("is_required", "auto_start", "initial_auto_proceed_config", "success_condition", "completion_action_configs", "form", "start_ingest", "select_or_create_asset", "attachments")
        IS_REQUIRED_FIELD_NUMBER: _ClassVar[int]
        AUTO_START_FIELD_NUMBER: _ClassVar[int]
        INITIAL_AUTO_PROCEED_CONFIG_FIELD_NUMBER: _ClassVar[int]
        SUCCESS_CONDITION_FIELD_NUMBER: _ClassVar[int]
        COMPLETION_ACTION_CONFIGS_FIELD_NUMBER: _ClassVar[int]
        FORM_FIELD_NUMBER: _ClassVar[int]
        START_INGEST_FIELD_NUMBER: _ClassVar[int]
        SELECT_OR_CREATE_ASSET_FIELD_NUMBER: _ClassVar[int]
        ATTACHMENTS_FIELD_NUMBER: _ClassVar[int]
        is_required: bool
        auto_start: AutoStartConfig
        initial_auto_proceed_config: AutoProceedConfig
        success_condition: SuccessCondition
        completion_action_configs: _containers.RepeatedCompositeFieldContainer[CompletionActionConfig]
        form: FormStep
        start_ingest: StartIngestStep
        select_or_create_asset: SelectOrCreateAssetStep
        attachments: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, is_required: bool = ..., auto_start: _Optional[_Union[AutoStartConfig, _Mapping]] = ..., initial_auto_proceed_config: _Optional[_Union[AutoProceedConfig, _Mapping]] = ..., success_condition: _Optional[_Union[SuccessCondition, _Mapping]] = ..., completion_action_configs: _Optional[_Iterable[_Union[CompletionActionConfig, _Mapping]]] = ..., form: _Optional[_Union[FormStep, _Mapping]] = ..., start_ingest: _Optional[_Union[StartIngestStep, _Mapping]] = ..., select_or_create_asset: _Optional[_Union[SelectOrCreateAssetStep, _Mapping]] = ..., attachments: _Optional[_Iterable[str]] = ...) -> None: ...
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
    __slots__ = ("timer", "ingest_job", "channel_validation")
    AND_FIELD_NUMBER: _ClassVar[int]
    TIMER_FIELD_NUMBER: _ClassVar[int]
    INGEST_JOB_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_VALIDATION_FIELD_NUMBER: _ClassVar[int]
    timer: TimerSuccessCondition
    ingest_job: IngestJobSuccessCondition
    channel_validation: ChannelValidationSuccessCondition
    def __init__(self, timer: _Optional[_Union[TimerSuccessCondition, _Mapping]] = ..., ingest_job: _Optional[_Union[IngestJobSuccessCondition, _Mapping]] = ..., channel_validation: _Optional[_Union[ChannelValidationSuccessCondition, _Mapping]] = ..., **kwargs) -> None: ...

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

class IngestJobSuccessCondition(_message.Message):
    __slots__ = ("field_id",)
    FIELD_ID_FIELD_NUMBER: _ClassVar[int]
    field_id: str
    def __init__(self, field_id: _Optional[str] = ...) -> None: ...

class ChannelValidationSuccessCondition(_message.Message):
    __slots__ = ("channel", "comparator", "threshold", "timeout_millis")
    class COMPARATOR(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        COMPARATOR_UNSPECIFIED: _ClassVar[ChannelValidationSuccessCondition.COMPARATOR]
        COMPARATOR_GREATER_THAN: _ClassVar[ChannelValidationSuccessCondition.COMPARATOR]
        COMPARATOR_GREATER_THAN_OR_EQUAL: _ClassVar[ChannelValidationSuccessCondition.COMPARATOR]
        COMPARATOR_LESS_THAN: _ClassVar[ChannelValidationSuccessCondition.COMPARATOR]
        COMPARATOR_LESS_THAN_OR_EQUAL: _ClassVar[ChannelValidationSuccessCondition.COMPARATOR]
        COMPARATOR_EQUAL: _ClassVar[ChannelValidationSuccessCondition.COMPARATOR]
        COMPARATOR_NOT_EQUAL: _ClassVar[ChannelValidationSuccessCondition.COMPARATOR]
    COMPARATOR_UNSPECIFIED: ChannelValidationSuccessCondition.COMPARATOR
    COMPARATOR_GREATER_THAN: ChannelValidationSuccessCondition.COMPARATOR
    COMPARATOR_GREATER_THAN_OR_EQUAL: ChannelValidationSuccessCondition.COMPARATOR
    COMPARATOR_LESS_THAN: ChannelValidationSuccessCondition.COMPARATOR
    COMPARATOR_LESS_THAN_OR_EQUAL: ChannelValidationSuccessCondition.COMPARATOR
    COMPARATOR_EQUAL: ChannelValidationSuccessCondition.COMPARATOR
    COMPARATOR_NOT_EQUAL: ChannelValidationSuccessCondition.COMPARATOR
    class ChannelLocator(_message.Message):
        __slots__ = ("data_source_ref", "channel_name", "tags", "asset", "run")
        class TagsEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
        DATA_SOURCE_REF_FIELD_NUMBER: _ClassVar[int]
        CHANNEL_NAME_FIELD_NUMBER: _ClassVar[int]
        TAGS_FIELD_NUMBER: _ClassVar[int]
        ASSET_FIELD_NUMBER: _ClassVar[int]
        RUN_FIELD_NUMBER: _ClassVar[int]
        data_source_ref: str
        channel_name: str
        tags: _containers.ScalarMap[str, str]
        asset: AssetReference
        run: RunReference
        def __init__(self, data_source_ref: _Optional[str] = ..., channel_name: _Optional[str] = ..., tags: _Optional[_Mapping[str, str]] = ..., asset: _Optional[_Union[AssetReference, _Mapping]] = ..., run: _Optional[_Union[RunReference, _Mapping]] = ...) -> None: ...
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    COMPARATOR_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_MILLIS_FIELD_NUMBER: _ClassVar[int]
    channel: ChannelValidationSuccessCondition.ChannelLocator
    comparator: ChannelValidationSuccessCondition.COMPARATOR
    threshold: float
    timeout_millis: int
    def __init__(self, channel: _Optional[_Union[ChannelValidationSuccessCondition.ChannelLocator, _Mapping]] = ..., comparator: _Optional[_Union[ChannelValidationSuccessCondition.COMPARATOR, str]] = ..., threshold: _Optional[float] = ..., timeout_millis: _Optional[int] = ...) -> None: ...

class CompletionActionConfig(_message.Message):
    __slots__ = ("create_event", "send_notification", "create_run", "apply_workbook_templates", "apply_checklists")
    CREATE_EVENT_FIELD_NUMBER: _ClassVar[int]
    SEND_NOTIFICATION_FIELD_NUMBER: _ClassVar[int]
    CREATE_RUN_FIELD_NUMBER: _ClassVar[int]
    APPLY_WORKBOOK_TEMPLATES_FIELD_NUMBER: _ClassVar[int]
    APPLY_CHECKLISTS_FIELD_NUMBER: _ClassVar[int]
    create_event: CreateEventConfig
    send_notification: SendNotificationConfig
    create_run: CreateRunConfig
    apply_workbook_templates: ApplyWorkbookTemplatesConfig
    apply_checklists: ApplyChecklistsConfig
    def __init__(self, create_event: _Optional[_Union[CreateEventConfig, _Mapping]] = ..., send_notification: _Optional[_Union[SendNotificationConfig, _Mapping]] = ..., create_run: _Optional[_Union[CreateRunConfig, _Mapping]] = ..., apply_workbook_templates: _Optional[_Union[ApplyWorkbookTemplatesConfig, _Mapping]] = ..., apply_checklists: _Optional[_Union[ApplyChecklistsConfig, _Mapping]] = ...) -> None: ...

class CreateEventConfig(_message.Message):
    __slots__ = ("name", "description", "labels", "properties", "asset_field_ids", "asset_references", "property_refs")
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
    ASSET_REFERENCES_FIELD_NUMBER: _ClassVar[int]
    PROPERTY_REFS_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    labels: _containers.RepeatedScalarFieldContainer[str]
    properties: _containers.ScalarMap[str, str]
    asset_field_ids: _containers.RepeatedScalarFieldContainer[str]
    asset_references: _containers.RepeatedCompositeFieldContainer[AssetReference]
    property_refs: _containers.RepeatedCompositeFieldContainer[PropertyReference]
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., labels: _Optional[_Iterable[str]] = ..., properties: _Optional[_Mapping[str, str]] = ..., asset_field_ids: _Optional[_Iterable[str]] = ..., asset_references: _Optional[_Iterable[_Union[AssetReference, _Mapping]]] = ..., property_refs: _Optional[_Iterable[_Union[PropertyReference, _Mapping]]] = ...) -> None: ...

class SendNotificationConfig(_message.Message):
    __slots__ = ("integrations", "title", "message")
    INTEGRATIONS_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    integrations: MultiIntegrationReference
    title: StringReference
    message: StringReference
    def __init__(self, integrations: _Optional[_Union[MultiIntegrationReference, _Mapping]] = ..., title: _Optional[_Union[StringReference, _Mapping]] = ..., message: _Optional[_Union[StringReference, _Mapping]] = ...) -> None: ...

class CreateRunConfig(_message.Message):
    __slots__ = ("run_output_field_id", "assets", "name", "description", "time_range", "labels", "properties")
    class Property(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: StringReference
        value: StringReference
        def __init__(self, key: _Optional[_Union[StringReference, _Mapping]] = ..., value: _Optional[_Union[StringReference, _Mapping]] = ...) -> None: ...
    RUN_OUTPUT_FIELD_ID_FIELD_NUMBER: _ClassVar[int]
    ASSETS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TIME_RANGE_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    run_output_field_id: str
    assets: MultiAssetReference
    name: StringReference
    description: StringReference
    time_range: TimeRangeReference
    labels: MultiStringReference
    properties: _containers.RepeatedCompositeFieldContainer[CreateRunConfig.Property]
    def __init__(self, run_output_field_id: _Optional[str] = ..., assets: _Optional[_Union[MultiAssetReference, _Mapping]] = ..., name: _Optional[_Union[StringReference, _Mapping]] = ..., description: _Optional[_Union[StringReference, _Mapping]] = ..., time_range: _Optional[_Union[TimeRangeReference, _Mapping]] = ..., labels: _Optional[_Union[MultiStringReference, _Mapping]] = ..., properties: _Optional[_Iterable[_Union[CreateRunConfig.Property, _Mapping]]] = ...) -> None: ...

class PropertyReference(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: StringReference
    value: StringReference
    def __init__(self, key: _Optional[_Union[StringReference, _Mapping]] = ..., value: _Optional[_Union[StringReference, _Mapping]] = ...) -> None: ...

class ApplyWorkbookTemplatesConfig(_message.Message):
    __slots__ = ("workbook_templates", "runs")
    WORKBOOK_TEMPLATES_FIELD_NUMBER: _ClassVar[int]
    RUNS_FIELD_NUMBER: _ClassVar[int]
    workbook_templates: MultiWorkbookTemplateReference
    runs: MultiRunReference
    def __init__(self, workbook_templates: _Optional[_Union[MultiWorkbookTemplateReference, _Mapping]] = ..., runs: _Optional[_Union[MultiRunReference, _Mapping]] = ...) -> None: ...

class ApplyChecklistsConfig(_message.Message):
    __slots__ = ("checklists", "runs")
    CHECKLISTS_FIELD_NUMBER: _ClassVar[int]
    RUNS_FIELD_NUMBER: _ClassVar[int]
    checklists: MultiChecklistReference
    runs: MultiRunReference
    def __init__(self, checklists: _Optional[_Union[MultiChecklistReference, _Mapping]] = ..., runs: _Optional[_Union[MultiRunReference, _Mapping]] = ...) -> None: ...

class ProcedureStepContent(_message.Message):
    __slots__ = ("form", "start_ingest", "select_or_create_asset")
    FORM_FIELD_NUMBER: _ClassVar[int]
    START_INGEST_FIELD_NUMBER: _ClassVar[int]
    SELECT_OR_CREATE_ASSET_FIELD_NUMBER: _ClassVar[int]
    form: FormStep
    start_ingest: StartIngestStep
    select_or_create_asset: SelectOrCreateAssetStep
    def __init__(self, form: _Optional[_Union[FormStep, _Mapping]] = ..., start_ingest: _Optional[_Union[StartIngestStep, _Mapping]] = ..., select_or_create_asset: _Optional[_Union[SelectOrCreateAssetStep, _Mapping]] = ...) -> None: ...

class FormStep(_message.Message):
    __slots__ = ("fields",)
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    fields: _containers.RepeatedCompositeFieldContainer[FormField]
    def __init__(self, fields: _Optional[_Iterable[_Union[FormField, _Mapping]]] = ...) -> None: ...

class StartIngestStep(_message.Message):
    __slots__ = ("asset", "ref_name", "ingest_type_config", "ingest_job_output_field_id")
    class IngestTypeConfig(_message.Message):
        __slots__ = ("containerized_extractor", "dataflash", "csv", "parquet")
        class ContainerizedExtractorIngestConfig(_message.Message):
            __slots__ = ("rid", "file_input_bindings")
            RID_FIELD_NUMBER: _ClassVar[int]
            FILE_INPUT_BINDINGS_FIELD_NUMBER: _ClassVar[int]
            rid: str
            file_input_bindings: _containers.RepeatedCompositeFieldContainer[FileInputBinding]
            def __init__(self, rid: _Optional[str] = ..., file_input_bindings: _Optional[_Iterable[_Union[FileInputBinding, _Mapping]]] = ...) -> None: ...
        class DataflashIngestConfig(_message.Message):
            __slots__ = ("file_input",)
            FILE_INPUT_FIELD_NUMBER: _ClassVar[int]
            file_input: FileReference
            def __init__(self, file_input: _Optional[_Union[FileReference, _Mapping]] = ...) -> None: ...
        class CsvIngestConfig(_message.Message):
            __slots__ = ("timestamp_series_name", "timestamp_type", "file_input")
            TIMESTAMP_SERIES_NAME_FIELD_NUMBER: _ClassVar[int]
            TIMESTAMP_TYPE_FIELD_NUMBER: _ClassVar[int]
            FILE_INPUT_FIELD_NUMBER: _ClassVar[int]
            timestamp_series_name: StringReference
            timestamp_type: TimestampTypeParameter
            file_input: FileReference
            def __init__(self, timestamp_series_name: _Optional[_Union[StringReference, _Mapping]] = ..., timestamp_type: _Optional[_Union[TimestampTypeParameter, _Mapping]] = ..., file_input: _Optional[_Union[FileReference, _Mapping]] = ...) -> None: ...
        class ParquetIngestConfig(_message.Message):
            __slots__ = ("timestamp_series_name", "timestamp_type", "file_input")
            TIMESTAMP_SERIES_NAME_FIELD_NUMBER: _ClassVar[int]
            TIMESTAMP_TYPE_FIELD_NUMBER: _ClassVar[int]
            FILE_INPUT_FIELD_NUMBER: _ClassVar[int]
            timestamp_series_name: StringReference
            timestamp_type: TimestampTypeParameter
            file_input: FileReference
            def __init__(self, timestamp_series_name: _Optional[_Union[StringReference, _Mapping]] = ..., timestamp_type: _Optional[_Union[TimestampTypeParameter, _Mapping]] = ..., file_input: _Optional[_Union[FileReference, _Mapping]] = ...) -> None: ...
        CONTAINERIZED_EXTRACTOR_FIELD_NUMBER: _ClassVar[int]
        DATAFLASH_FIELD_NUMBER: _ClassVar[int]
        CSV_FIELD_NUMBER: _ClassVar[int]
        PARQUET_FIELD_NUMBER: _ClassVar[int]
        containerized_extractor: StartIngestStep.IngestTypeConfig.ContainerizedExtractorIngestConfig
        dataflash: StartIngestStep.IngestTypeConfig.DataflashIngestConfig
        csv: StartIngestStep.IngestTypeConfig.CsvIngestConfig
        parquet: StartIngestStep.IngestTypeConfig.ParquetIngestConfig
        def __init__(self, containerized_extractor: _Optional[_Union[StartIngestStep.IngestTypeConfig.ContainerizedExtractorIngestConfig, _Mapping]] = ..., dataflash: _Optional[_Union[StartIngestStep.IngestTypeConfig.DataflashIngestConfig, _Mapping]] = ..., csv: _Optional[_Union[StartIngestStep.IngestTypeConfig.CsvIngestConfig, _Mapping]] = ..., parquet: _Optional[_Union[StartIngestStep.IngestTypeConfig.ParquetIngestConfig, _Mapping]] = ...) -> None: ...
    ASSET_FIELD_NUMBER: _ClassVar[int]
    REF_NAME_FIELD_NUMBER: _ClassVar[int]
    INGEST_TYPE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    INGEST_JOB_OUTPUT_FIELD_ID_FIELD_NUMBER: _ClassVar[int]
    asset: AssetReference
    ref_name: StringReference
    ingest_type_config: StartIngestStep.IngestTypeConfig
    ingest_job_output_field_id: str
    def __init__(self, asset: _Optional[_Union[AssetReference, _Mapping]] = ..., ref_name: _Optional[_Union[StringReference, _Mapping]] = ..., ingest_type_config: _Optional[_Union[StartIngestStep.IngestTypeConfig, _Mapping]] = ..., ingest_job_output_field_id: _Optional[str] = ...) -> None: ...

class FileInputBinding(_message.Message):
    __slots__ = ("environment_variable", "file_reference")
    ENVIRONMENT_VARIABLE_FIELD_NUMBER: _ClassVar[int]
    FILE_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    environment_variable: str
    file_reference: FileReference
    def __init__(self, environment_variable: _Optional[str] = ..., file_reference: _Optional[_Union[FileReference, _Mapping]] = ...) -> None: ...

class FileReference(_message.Message):
    __slots__ = ("field_id",)
    FIELD_ID_FIELD_NUMBER: _ClassVar[int]
    field_id: str
    def __init__(self, field_id: _Optional[str] = ...) -> None: ...

class TimestampTypeParameter(_message.Message):
    __slots__ = ("constant", "user_input")
    class UserInputOptions(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    CONSTANT_FIELD_NUMBER: _ClassVar[int]
    USER_INPUT_FIELD_NUMBER: _ClassVar[int]
    constant: TimestampType
    user_input: TimestampTypeParameter.UserInputOptions
    def __init__(self, constant: _Optional[_Union[TimestampType, _Mapping]] = ..., user_input: _Optional[_Union[TimestampTypeParameter.UserInputOptions, _Mapping]] = ...) -> None: ...

class TimestampType(_message.Message):
    __slots__ = ("relative", "absolute")
    RELATIVE_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_FIELD_NUMBER: _ClassVar[int]
    relative: RelativeTimestamp
    absolute: AbsoluteTimestamp
    def __init__(self, relative: _Optional[_Union[RelativeTimestamp, _Mapping]] = ..., absolute: _Optional[_Union[AbsoluteTimestamp, _Mapping]] = ...) -> None: ...

class RelativeTimestamp(_message.Message):
    __slots__ = ("time_unit", "offset")
    TIME_UNIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    time_unit: str
    offset: _timestamp_pb2.Timestamp
    def __init__(self, time_unit: _Optional[str] = ..., offset: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class AbsoluteTimestamp(_message.Message):
    __slots__ = ("iso8601", "epoch_of_time_unit", "custom_format")
    ISO8601_FIELD_NUMBER: _ClassVar[int]
    EPOCH_OF_TIME_UNIT_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_FORMAT_FIELD_NUMBER: _ClassVar[int]
    iso8601: Iso8601Timestamp
    epoch_of_time_unit: EpochTimestamp
    custom_format: CustomTimestamp
    def __init__(self, iso8601: _Optional[_Union[Iso8601Timestamp, _Mapping]] = ..., epoch_of_time_unit: _Optional[_Union[EpochTimestamp, _Mapping]] = ..., custom_format: _Optional[_Union[CustomTimestamp, _Mapping]] = ...) -> None: ...

class Iso8601Timestamp(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class EpochTimestamp(_message.Message):
    __slots__ = ("time_unit",)
    TIME_UNIT_FIELD_NUMBER: _ClassVar[int]
    time_unit: str
    def __init__(self, time_unit: _Optional[str] = ...) -> None: ...

class CustomTimestamp(_message.Message):
    __slots__ = ("format", "default_year", "default_day_of_year")
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_YEAR_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_DAY_OF_YEAR_FIELD_NUMBER: _ClassVar[int]
    format: str
    default_year: int
    default_day_of_year: int
    def __init__(self, format: _Optional[str] = ..., default_year: _Optional[int] = ..., default_day_of_year: _Optional[int] = ...) -> None: ...

class SelectOrCreateAssetStep(_message.Message):
    __slots__ = ("asset_output_field_id", "create_asset_parameters", "preset_options")
    class CreateAssetParameters(_message.Message):
        __slots__ = ("description", "labels", "properties", "data_scopes")
        class DataScopesEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: SelectOrCreateAssetStep.CreateAssetParameters.DataScopeParameter
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[SelectOrCreateAssetStep.CreateAssetParameters.DataScopeParameter, _Mapping]] = ...) -> None: ...
        class DescriptionParameter(_message.Message):
            __slots__ = ("constant",)
            CONSTANT_FIELD_NUMBER: _ClassVar[int]
            constant: str
            def __init__(self, constant: _Optional[str] = ...) -> None: ...
        class LabelsParameter(_message.Message):
            __slots__ = ("constant", "user_input")
            class UserInputOptions(_message.Message):
                __slots__ = ()
                def __init__(self) -> None: ...
            CONSTANT_FIELD_NUMBER: _ClassVar[int]
            USER_INPUT_FIELD_NUMBER: _ClassVar[int]
            constant: _containers.RepeatedScalarFieldContainer[str]
            user_input: SelectOrCreateAssetStep.CreateAssetParameters.LabelsParameter.UserInputOptions
            def __init__(self, constant: _Optional[_Iterable[str]] = ..., user_input: _Optional[_Union[SelectOrCreateAssetStep.CreateAssetParameters.LabelsParameter.UserInputOptions, _Mapping]] = ...) -> None: ...
        class PropertiesParameter(_message.Message):
            __slots__ = ("constant", "user_input")
            class ConstantEntry(_message.Message):
                __slots__ = ("key", "value")
                KEY_FIELD_NUMBER: _ClassVar[int]
                VALUE_FIELD_NUMBER: _ClassVar[int]
                key: str
                value: str
                def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
            class UserInputOptions(_message.Message):
                __slots__ = ("required_keys", "suggested_keys")
                REQUIRED_KEYS_FIELD_NUMBER: _ClassVar[int]
                SUGGESTED_KEYS_FIELD_NUMBER: _ClassVar[int]
                required_keys: _containers.RepeatedScalarFieldContainer[str]
                suggested_keys: _containers.RepeatedScalarFieldContainer[str]
                def __init__(self, required_keys: _Optional[_Iterable[str]] = ..., suggested_keys: _Optional[_Iterable[str]] = ...) -> None: ...
            CONSTANT_FIELD_NUMBER: _ClassVar[int]
            USER_INPUT_FIELD_NUMBER: _ClassVar[int]
            constant: _containers.ScalarMap[str, str]
            user_input: SelectOrCreateAssetStep.CreateAssetParameters.PropertiesParameter.UserInputOptions
            def __init__(self, constant: _Optional[_Mapping[str, str]] = ..., user_input: _Optional[_Union[SelectOrCreateAssetStep.CreateAssetParameters.PropertiesParameter.UserInputOptions, _Mapping]] = ...) -> None: ...
        class DataScopeParameter(_message.Message):
            __slots__ = ("new_dataset", "existing_dataset", "series_tags")
            class NewDataset(_message.Message):
                __slots__ = ()
                def __init__(self) -> None: ...
            class ExistingDataset(_message.Message):
                __slots__ = ("preset_options",)
                PRESET_OPTIONS_FIELD_NUMBER: _ClassVar[int]
                preset_options: PresetDatasetFieldOptions
                def __init__(self, preset_options: _Optional[_Union[PresetDatasetFieldOptions, _Mapping]] = ...) -> None: ...
            NEW_DATASET_FIELD_NUMBER: _ClassVar[int]
            EXISTING_DATASET_FIELD_NUMBER: _ClassVar[int]
            SERIES_TAGS_FIELD_NUMBER: _ClassVar[int]
            new_dataset: SelectOrCreateAssetStep.CreateAssetParameters.DataScopeParameter.NewDataset
            existing_dataset: SelectOrCreateAssetStep.CreateAssetParameters.DataScopeParameter.ExistingDataset
            series_tags: TagsParameter
            def __init__(self, new_dataset: _Optional[_Union[SelectOrCreateAssetStep.CreateAssetParameters.DataScopeParameter.NewDataset, _Mapping]] = ..., existing_dataset: _Optional[_Union[SelectOrCreateAssetStep.CreateAssetParameters.DataScopeParameter.ExistingDataset, _Mapping]] = ..., series_tags: _Optional[_Union[TagsParameter, _Mapping]] = ...) -> None: ...
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        LABELS_FIELD_NUMBER: _ClassVar[int]
        PROPERTIES_FIELD_NUMBER: _ClassVar[int]
        DATA_SCOPES_FIELD_NUMBER: _ClassVar[int]
        description: SelectOrCreateAssetStep.CreateAssetParameters.DescriptionParameter
        labels: SelectOrCreateAssetStep.CreateAssetParameters.LabelsParameter
        properties: SelectOrCreateAssetStep.CreateAssetParameters.PropertiesParameter
        data_scopes: _containers.MessageMap[str, SelectOrCreateAssetStep.CreateAssetParameters.DataScopeParameter]
        def __init__(self, description: _Optional[_Union[SelectOrCreateAssetStep.CreateAssetParameters.DescriptionParameter, _Mapping]] = ..., labels: _Optional[_Union[SelectOrCreateAssetStep.CreateAssetParameters.LabelsParameter, _Mapping]] = ..., properties: _Optional[_Union[SelectOrCreateAssetStep.CreateAssetParameters.PropertiesParameter, _Mapping]] = ..., data_scopes: _Optional[_Mapping[str, SelectOrCreateAssetStep.CreateAssetParameters.DataScopeParameter]] = ...) -> None: ...
    ASSET_OUTPUT_FIELD_ID_FIELD_NUMBER: _ClassVar[int]
    CREATE_ASSET_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    PRESET_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    asset_output_field_id: str
    create_asset_parameters: SelectOrCreateAssetStep.CreateAssetParameters
    preset_options: PresetAssetFieldOptions
    def __init__(self, asset_output_field_id: _Optional[str] = ..., create_asset_parameters: _Optional[_Union[SelectOrCreateAssetStep.CreateAssetParameters, _Mapping]] = ..., preset_options: _Optional[_Union[PresetAssetFieldOptions, _Mapping]] = ...) -> None: ...

class PresetDatasetFieldOptions(_message.Message):
    __slots__ = ("options", "default_option")
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_OPTION_FIELD_NUMBER: _ClassVar[int]
    options: _containers.RepeatedCompositeFieldContainer[DatasetReference]
    default_option: DatasetReference
    def __init__(self, options: _Optional[_Iterable[_Union[DatasetReference, _Mapping]]] = ..., default_option: _Optional[_Union[DatasetReference, _Mapping]] = ...) -> None: ...

class DatasetReference(_message.Message):
    __slots__ = ("rid", "field_id")
    RID_FIELD_NUMBER: _ClassVar[int]
    FIELD_ID_FIELD_NUMBER: _ClassVar[int]
    rid: str
    field_id: str
    def __init__(self, rid: _Optional[str] = ..., field_id: _Optional[str] = ...) -> None: ...

class TagsParameter(_message.Message):
    __slots__ = ("constant", "user_input")
    class ConstantEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class UserInputOptions(_message.Message):
        __slots__ = ("required_keys", "suggested_keys")
        REQUIRED_KEYS_FIELD_NUMBER: _ClassVar[int]
        SUGGESTED_KEYS_FIELD_NUMBER: _ClassVar[int]
        required_keys: _containers.RepeatedScalarFieldContainer[str]
        suggested_keys: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, required_keys: _Optional[_Iterable[str]] = ..., suggested_keys: _Optional[_Iterable[str]] = ...) -> None: ...
    CONSTANT_FIELD_NUMBER: _ClassVar[int]
    USER_INPUT_FIELD_NUMBER: _ClassVar[int]
    constant: _containers.ScalarMap[str, str]
    user_input: TagsParameter.UserInputOptions
    def __init__(self, constant: _Optional[_Mapping[str, str]] = ..., user_input: _Optional[_Union[TagsParameter.UserInputOptions, _Mapping]] = ...) -> None: ...

class MultiStringReference(_message.Message):
    __slots__ = ("field_id",)
    FIELD_ID_FIELD_NUMBER: _ClassVar[int]
    field_id: str
    def __init__(self, field_id: _Optional[str] = ...) -> None: ...

class StringReference(_message.Message):
    __slots__ = ("constant", "field_id")
    CONSTANT_FIELD_NUMBER: _ClassVar[int]
    FIELD_ID_FIELD_NUMBER: _ClassVar[int]
    constant: str
    field_id: str
    def __init__(self, constant: _Optional[str] = ..., field_id: _Optional[str] = ...) -> None: ...

class MultiAssetReference(_message.Message):
    __slots__ = ("list",)
    class AssetReferenceList(_message.Message):
        __slots__ = ("references",)
        REFERENCES_FIELD_NUMBER: _ClassVar[int]
        references: _containers.RepeatedCompositeFieldContainer[AssetReference]
        def __init__(self, references: _Optional[_Iterable[_Union[AssetReference, _Mapping]]] = ...) -> None: ...
    LIST_FIELD_NUMBER: _ClassVar[int]
    list: MultiAssetReference.AssetReferenceList
    def __init__(self, list: _Optional[_Union[MultiAssetReference.AssetReferenceList, _Mapping]] = ...) -> None: ...

class AssetReference(_message.Message):
    __slots__ = ("rid", "field_id")
    RID_FIELD_NUMBER: _ClassVar[int]
    FIELD_ID_FIELD_NUMBER: _ClassVar[int]
    rid: str
    field_id: str
    def __init__(self, rid: _Optional[str] = ..., field_id: _Optional[str] = ...) -> None: ...

class TimeRangeReference(_message.Message):
    __slots__ = ("from_ingest_jobs",)
    class IngestJobList(_message.Message):
        __slots__ = ("field_ids",)
        FIELD_IDS_FIELD_NUMBER: _ClassVar[int]
        field_ids: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, field_ids: _Optional[_Iterable[str]] = ...) -> None: ...
    FROM_INGEST_JOBS_FIELD_NUMBER: _ClassVar[int]
    from_ingest_jobs: TimeRangeReference.IngestJobList
    def __init__(self, from_ingest_jobs: _Optional[_Union[TimeRangeReference.IngestJobList, _Mapping]] = ...) -> None: ...

class MultiRunReference(_message.Message):
    __slots__ = ("list",)
    class RunReferenceList(_message.Message):
        __slots__ = ("references",)
        REFERENCES_FIELD_NUMBER: _ClassVar[int]
        references: _containers.RepeatedCompositeFieldContainer[RunReference]
        def __init__(self, references: _Optional[_Iterable[_Union[RunReference, _Mapping]]] = ...) -> None: ...
    LIST_FIELD_NUMBER: _ClassVar[int]
    list: MultiRunReference.RunReferenceList
    def __init__(self, list: _Optional[_Union[MultiRunReference.RunReferenceList, _Mapping]] = ...) -> None: ...

class RunReference(_message.Message):
    __slots__ = ("field_id",)
    FIELD_ID_FIELD_NUMBER: _ClassVar[int]
    field_id: str
    def __init__(self, field_id: _Optional[str] = ...) -> None: ...

class MultiWorkbookTemplateReference(_message.Message):
    __slots__ = ("list",)
    class WorkbookTemplateReferenceList(_message.Message):
        __slots__ = ("references",)
        REFERENCES_FIELD_NUMBER: _ClassVar[int]
        references: _containers.RepeatedCompositeFieldContainer[WorkbookTemplateReference]
        def __init__(self, references: _Optional[_Iterable[_Union[WorkbookTemplateReference, _Mapping]]] = ...) -> None: ...
    LIST_FIELD_NUMBER: _ClassVar[int]
    list: MultiWorkbookTemplateReference.WorkbookTemplateReferenceList
    def __init__(self, list: _Optional[_Union[MultiWorkbookTemplateReference.WorkbookTemplateReferenceList, _Mapping]] = ...) -> None: ...

class WorkbookTemplateReference(_message.Message):
    __slots__ = ("rid",)
    RID_FIELD_NUMBER: _ClassVar[int]
    rid: str
    def __init__(self, rid: _Optional[str] = ...) -> None: ...

class MultiChecklistReference(_message.Message):
    __slots__ = ("list",)
    class ChecklistReferenceList(_message.Message):
        __slots__ = ("references",)
        REFERENCES_FIELD_NUMBER: _ClassVar[int]
        references: _containers.RepeatedCompositeFieldContainer[ChecklistReference]
        def __init__(self, references: _Optional[_Iterable[_Union[ChecklistReference, _Mapping]]] = ...) -> None: ...
    LIST_FIELD_NUMBER: _ClassVar[int]
    list: MultiChecklistReference.ChecklistReferenceList
    def __init__(self, list: _Optional[_Union[MultiChecklistReference.ChecklistReferenceList, _Mapping]] = ...) -> None: ...

class ChecklistReference(_message.Message):
    __slots__ = ("rid",)
    RID_FIELD_NUMBER: _ClassVar[int]
    rid: str
    def __init__(self, rid: _Optional[str] = ...) -> None: ...

class MultiIntegrationReference(_message.Message):
    __slots__ = ("list",)
    class IntegrationReferenceList(_message.Message):
        __slots__ = ("references",)
        REFERENCES_FIELD_NUMBER: _ClassVar[int]
        references: _containers.RepeatedCompositeFieldContainer[IntegrationReference]
        def __init__(self, references: _Optional[_Iterable[_Union[IntegrationReference, _Mapping]]] = ...) -> None: ...
    LIST_FIELD_NUMBER: _ClassVar[int]
    list: MultiIntegrationReference.IntegrationReferenceList
    def __init__(self, list: _Optional[_Union[MultiIntegrationReference.IntegrationReferenceList, _Mapping]] = ...) -> None: ...

class IntegrationReference(_message.Message):
    __slots__ = ("rid",)
    RID_FIELD_NUMBER: _ClassVar[int]
    rid: str
    def __init__(self, rid: _Optional[str] = ...) -> None: ...

class FormField(_message.Message):
    __slots__ = ("id", "asset", "checkbox", "text", "int", "double", "single_enum", "multi_enum", "file_upload", "multi_file_upload", "label", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    ASSET_FIELD_NUMBER: _ClassVar[int]
    CHECKBOX_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    INT_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_FIELD_NUMBER: _ClassVar[int]
    SINGLE_ENUM_FIELD_NUMBER: _ClassVar[int]
    MULTI_ENUM_FIELD_NUMBER: _ClassVar[int]
    FILE_UPLOAD_FIELD_NUMBER: _ClassVar[int]
    MULTI_FILE_UPLOAD_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    asset: AssetField
    checkbox: CheckboxField
    text: TextField
    int: IntField
    double: DoubleField
    single_enum: SingleEnumField
    multi_enum: MultiEnumField
    file_upload: FileUploadField
    multi_file_upload: MultiFileUploadField
    label: str
    description: str
    def __init__(self, id: _Optional[str] = ..., asset: _Optional[_Union[AssetField, _Mapping]] = ..., checkbox: _Optional[_Union[CheckboxField, _Mapping]] = ..., text: _Optional[_Union[TextField, _Mapping]] = ..., int: _Optional[_Union[IntField, _Mapping]] = ..., double: _Optional[_Union[DoubleField, _Mapping]] = ..., single_enum: _Optional[_Union[SingleEnumField, _Mapping]] = ..., multi_enum: _Optional[_Union[MultiEnumField, _Mapping]] = ..., file_upload: _Optional[_Union[FileUploadField, _Mapping]] = ..., multi_file_upload: _Optional[_Union[MultiFileUploadField, _Mapping]] = ..., label: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

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

class FileUploadField(_message.Message):
    __slots__ = ("is_required", "suffix_filters")
    IS_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    SUFFIX_FILTERS_FIELD_NUMBER: _ClassVar[int]
    is_required: bool
    suffix_filters: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, is_required: bool = ..., suffix_filters: _Optional[_Iterable[str]] = ...) -> None: ...

class MultiFileUploadField(_message.Message):
    __slots__ = ("min_count", "max_count", "suffix_filters")
    MIN_COUNT_FIELD_NUMBER: _ClassVar[int]
    MAX_COUNT_FIELD_NUMBER: _ClassVar[int]
    SUFFIX_FILTERS_FIELD_NUMBER: _ClassVar[int]
    min_count: int
    max_count: int
    suffix_filters: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, min_count: _Optional[int] = ..., max_count: _Optional[int] = ..., suffix_filters: _Optional[_Iterable[str]] = ...) -> None: ...

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

class BatchGetProcedureMetadataRequest(_message.Message):
    __slots__ = ("procedure_rids",)
    PROCEDURE_RIDS_FIELD_NUMBER: _ClassVar[int]
    procedure_rids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, procedure_rids: _Optional[_Iterable[str]] = ...) -> None: ...

class BatchGetProcedureMetadataResponse(_message.Message):
    __slots__ = ("procedure_metadatas",)
    PROCEDURE_METADATAS_FIELD_NUMBER: _ClassVar[int]
    procedure_metadatas: _containers.RepeatedCompositeFieldContainer[ProcedureMetadata]
    def __init__(self, procedure_metadatas: _Optional[_Iterable[_Union[ProcedureMetadata, _Mapping]]] = ...) -> None: ...

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
