from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
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

class PromptTemplate(_message.Message):
    __slots__ = ("type", "message")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    type: str
    message: str
    def __init__(self, type: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class ProviderConfig(_message.Message):
    __slots__ = ("provider", "model_name", "parameters", "structured_output")
    class ParametersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    STRUCTURED_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    provider: str
    model_name: str
    parameters: _containers.MessageMap[str, _struct_pb2.Value]
    structured_output: str
    def __init__(
        self,
        provider: _Optional[str] = ...,
        model_name: _Optional[str] = ...,
        parameters: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
        structured_output: _Optional[str] = ...,
    ) -> None: ...

class PromptVariant(_message.Message):
    __slots__ = (
        "id",
        "environment_id",
        "deployment_id",
        "named_prompt_id",
        "evaluation_run_id",
        "commit_hash",
        "templates",
        "variables",
        "provider_config",
        "variant_hash",
        "created_by",
        "created_at",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    NAMED_PROMPT_ID_FIELD_NUMBER: _ClassVar[int]
    EVALUATION_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    COMMIT_HASH_FIELD_NUMBER: _ClassVar[int]
    TEMPLATES_FIELD_NUMBER: _ClassVar[int]
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    VARIANT_HASH_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    environment_id: str
    deployment_id: str
    named_prompt_id: str
    evaluation_run_id: str
    commit_hash: str
    templates: _containers.RepeatedCompositeFieldContainer[PromptTemplate]
    variables: _containers.RepeatedScalarFieldContainer[str]
    provider_config: ProviderConfig
    variant_hash: str
    created_by: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[int] = ...,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        named_prompt_id: _Optional[str] = ...,
        evaluation_run_id: _Optional[str] = ...,
        commit_hash: _Optional[str] = ...,
        templates: _Optional[_Iterable[_Union[PromptTemplate, _Mapping]]] = ...,
        variables: _Optional[_Iterable[str]] = ...,
        provider_config: _Optional[_Union[ProviderConfig, _Mapping]] = ...,
        variant_hash: _Optional[str] = ...,
        created_by: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class NamedPrompt(_message.Message):
    __slots__ = (
        "id",
        "environment_id",
        "deployment_id",
        "name",
        "description",
        "tags",
        "created_by",
        "created_at",
        "updated_at",
        "archived_at",
        "latest_prompt_variant",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    ARCHIVED_AT_FIELD_NUMBER: _ClassVar[int]
    LATEST_PROMPT_VARIANT_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    deployment_id: str
    name: str
    description: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    created_by: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    archived_at: _timestamp_pb2.Timestamp
    latest_prompt_variant: PromptVariant
    def __init__(
        self,
        id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        created_by: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        archived_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        latest_prompt_variant: _Optional[_Union[PromptVariant, _Mapping]] = ...,
    ) -> None: ...

class PromptEvaluationRun(_message.Message):
    __slots__ = (
        "id",
        "environment_id",
        "deployment_id",
        "branch_name",
        "dataset_id",
        "dataset_revision_id",
        "reference_output",
        "evaluators",
        "offline_query_ids",
        "related_named_prompt_ids",
        "related_evaluation_ids",
        "aggregate_metrics",
        "meta_data",
        "created_by",
        "created_at",
        "dataset_name",
        "related_named_prompt_names",
        "prompt_variants",
    )
    class AggregateMetricsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

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
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_REVISION_ID_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    EVALUATORS_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_QUERY_IDS_FIELD_NUMBER: _ClassVar[int]
    RELATED_NAMED_PROMPT_IDS_FIELD_NUMBER: _ClassVar[int]
    RELATED_EVALUATION_IDS_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_METRICS_FIELD_NUMBER: _ClassVar[int]
    META_DATA_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    DATASET_NAME_FIELD_NUMBER: _ClassVar[int]
    RELATED_NAMED_PROMPT_NAMES_FIELD_NUMBER: _ClassVar[int]
    PROMPT_VARIANTS_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    deployment_id: str
    branch_name: str
    dataset_id: str
    dataset_revision_id: str
    reference_output: str
    evaluators: _containers.RepeatedScalarFieldContainer[str]
    offline_query_ids: _containers.RepeatedScalarFieldContainer[str]
    related_named_prompt_ids: _containers.RepeatedScalarFieldContainer[str]
    related_evaluation_ids: _containers.RepeatedScalarFieldContainer[str]
    aggregate_metrics: _containers.MessageMap[str, _struct_pb2.Value]
    meta_data: _containers.MessageMap[str, _struct_pb2.Value]
    created_by: str
    created_at: _timestamp_pb2.Timestamp
    dataset_name: str
    related_named_prompt_names: _containers.RepeatedScalarFieldContainer[str]
    prompt_variants: _containers.RepeatedCompositeFieldContainer[PromptVariant]
    def __init__(
        self,
        id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        branch_name: _Optional[str] = ...,
        dataset_id: _Optional[str] = ...,
        dataset_revision_id: _Optional[str] = ...,
        reference_output: _Optional[str] = ...,
        evaluators: _Optional[_Iterable[str]] = ...,
        offline_query_ids: _Optional[_Iterable[str]] = ...,
        related_named_prompt_ids: _Optional[_Iterable[str]] = ...,
        related_evaluation_ids: _Optional[_Iterable[str]] = ...,
        aggregate_metrics: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
        meta_data: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
        created_by: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        dataset_name: _Optional[str] = ...,
        related_named_prompt_names: _Optional[_Iterable[str]] = ...,
        prompt_variants: _Optional[_Iterable[_Union[PromptVariant, _Mapping]]] = ...,
    ) -> None: ...

class ListNamedPromptsRequest(_message.Message):
    __slots__ = ("cursor", "limit")
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    cursor: str
    limit: int
    def __init__(self, cursor: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...

class ListNamedPromptsResponse(_message.Message):
    __slots__ = ("named_prompts", "next_cursor")
    NAMED_PROMPTS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    named_prompts: _containers.RepeatedCompositeFieldContainer[NamedPrompt]
    next_cursor: str
    def __init__(
        self,
        named_prompts: _Optional[_Iterable[_Union[NamedPrompt, _Mapping]]] = ...,
        next_cursor: _Optional[str] = ...,
    ) -> None: ...

class GetNamedPromptRequest(_message.Message):
    __slots__ = ("named_prompt_id",)
    NAMED_PROMPT_ID_FIELD_NUMBER: _ClassVar[int]
    named_prompt_id: str
    def __init__(self, named_prompt_id: _Optional[str] = ...) -> None: ...

class GetNamedPromptResponse(_message.Message):
    __slots__ = ("named_prompt",)
    NAMED_PROMPT_FIELD_NUMBER: _ClassVar[int]
    named_prompt: NamedPrompt
    def __init__(self, named_prompt: _Optional[_Union[NamedPrompt, _Mapping]] = ...) -> None: ...

class PromptVariantOperation(_message.Message):
    __slots__ = ("templates", "provider_config")
    TEMPLATES_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    templates: _containers.RepeatedCompositeFieldContainer[PromptTemplate]
    provider_config: ProviderConfig
    def __init__(
        self,
        templates: _Optional[_Iterable[_Union[PromptTemplate, _Mapping]]] = ...,
        provider_config: _Optional[_Union[ProviderConfig, _Mapping]] = ...,
    ) -> None: ...

class CreateNamedPromptRequest(_message.Message):
    __slots__ = ("name", "description", "tags", "prompt_variant")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    PROMPT_VARIANT_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    prompt_variant: PromptVariantOperation
    def __init__(
        self,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        prompt_variant: _Optional[_Union[PromptVariantOperation, _Mapping]] = ...,
    ) -> None: ...

class CreateNamedPromptResponse(_message.Message):
    __slots__ = ("named_prompt",)
    NAMED_PROMPT_FIELD_NUMBER: _ClassVar[int]
    named_prompt: NamedPrompt
    def __init__(self, named_prompt: _Optional[_Union[NamedPrompt, _Mapping]] = ...) -> None: ...

class UpdateNamedPromptOperation(_message.Message):
    __slots__ = ("name", "description", "tags", "prompt_variant", "archived_at")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    PROMPT_VARIANT_FIELD_NUMBER: _ClassVar[int]
    ARCHIVED_AT_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    prompt_variant: PromptVariantOperation
    archived_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        prompt_variant: _Optional[_Union[PromptVariantOperation, _Mapping]] = ...,
        archived_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class UpdateNamedPromptRequest(_message.Message):
    __slots__ = ("named_prompt_id", "update", "update_mask")
    NAMED_PROMPT_ID_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    named_prompt_id: str
    update: UpdateNamedPromptOperation
    update_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        named_prompt_id: _Optional[str] = ...,
        update: _Optional[_Union[UpdateNamedPromptOperation, _Mapping]] = ...,
        update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class UpdateNamedPromptResponse(_message.Message):
    __slots__ = ("named_prompt",)
    NAMED_PROMPT_FIELD_NUMBER: _ClassVar[int]
    named_prompt: NamedPrompt
    def __init__(self, named_prompt: _Optional[_Union[NamedPrompt, _Mapping]] = ...) -> None: ...

class ListPromptVariantsRequest(_message.Message):
    __slots__ = ("named_prompt_id", "evaluation_run_id", "cursor", "limit")
    NAMED_PROMPT_ID_FIELD_NUMBER: _ClassVar[int]
    EVALUATION_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    named_prompt_id: str
    evaluation_run_id: str
    cursor: str
    limit: int
    def __init__(
        self,
        named_prompt_id: _Optional[str] = ...,
        evaluation_run_id: _Optional[str] = ...,
        cursor: _Optional[str] = ...,
        limit: _Optional[int] = ...,
    ) -> None: ...

class ListPromptVariantsResponse(_message.Message):
    __slots__ = ("prompt_variants", "next_cursor")
    PROMPT_VARIANTS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    prompt_variants: _containers.RepeatedCompositeFieldContainer[PromptVariant]
    next_cursor: str
    def __init__(
        self,
        prompt_variants: _Optional[_Iterable[_Union[PromptVariant, _Mapping]]] = ...,
        next_cursor: _Optional[str] = ...,
    ) -> None: ...

class ListPromptEvaluationRunsRequest(_message.Message):
    __slots__ = ("cursor", "limit", "named_prompt_id")
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    NAMED_PROMPT_ID_FIELD_NUMBER: _ClassVar[int]
    cursor: str
    limit: int
    named_prompt_id: str
    def __init__(
        self, cursor: _Optional[str] = ..., limit: _Optional[int] = ..., named_prompt_id: _Optional[str] = ...
    ) -> None: ...

class ListPromptEvaluationRunsResponse(_message.Message):
    __slots__ = ("evaluation_runs", "next_cursor")
    EVALUATION_RUNS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    evaluation_runs: _containers.RepeatedCompositeFieldContainer[PromptEvaluationRun]
    next_cursor: str
    def __init__(
        self,
        evaluation_runs: _Optional[_Iterable[_Union[PromptEvaluationRun, _Mapping]]] = ...,
        next_cursor: _Optional[str] = ...,
    ) -> None: ...

class GetPromptEvaluationRunRequest(_message.Message):
    __slots__ = ("evaluation_run_id", "prefill_options")
    class PrefillOptions(_message.Message):
        __slots__ = ("named_prompt_id", "evaluation_run_id")
        NAMED_PROMPT_ID_FIELD_NUMBER: _ClassVar[int]
        EVALUATION_RUN_ID_FIELD_NUMBER: _ClassVar[int]
        named_prompt_id: str
        evaluation_run_id: str
        def __init__(self, named_prompt_id: _Optional[str] = ..., evaluation_run_id: _Optional[str] = ...) -> None: ...

    EVALUATION_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    PREFILL_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    evaluation_run_id: str
    prefill_options: GetPromptEvaluationRunRequest.PrefillOptions
    def __init__(
        self,
        evaluation_run_id: _Optional[str] = ...,
        prefill_options: _Optional[_Union[GetPromptEvaluationRunRequest.PrefillOptions, _Mapping]] = ...,
    ) -> None: ...

class GetPromptEvaluationRunResponse(_message.Message):
    __slots__ = ("evaluation_run",)
    EVALUATION_RUN_FIELD_NUMBER: _ClassVar[int]
    evaluation_run: PromptEvaluationRun
    def __init__(self, evaluation_run: _Optional[_Union[PromptEvaluationRun, _Mapping]] = ...) -> None: ...

class CreatePromptEvaluationRunRequest(_message.Message):
    __slots__ = (
        "branch_name",
        "dataset_id",
        "dataset_revision_id",
        "reference_output",
        "evaluators",
        "related_named_prompt_ids",
        "related_evaluation_ids",
        "meta_data",
        "prompt_variants",
    )
    class MetaDataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_REVISION_ID_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    EVALUATORS_FIELD_NUMBER: _ClassVar[int]
    RELATED_NAMED_PROMPT_IDS_FIELD_NUMBER: _ClassVar[int]
    RELATED_EVALUATION_IDS_FIELD_NUMBER: _ClassVar[int]
    META_DATA_FIELD_NUMBER: _ClassVar[int]
    PROMPT_VARIANTS_FIELD_NUMBER: _ClassVar[int]
    branch_name: str
    dataset_id: str
    dataset_revision_id: str
    reference_output: str
    evaluators: _containers.RepeatedScalarFieldContainer[str]
    related_named_prompt_ids: _containers.RepeatedScalarFieldContainer[str]
    related_evaluation_ids: _containers.RepeatedScalarFieldContainer[str]
    meta_data: _containers.MessageMap[str, _struct_pb2.Value]
    prompt_variants: _containers.RepeatedCompositeFieldContainer[PromptVariantOperation]
    def __init__(
        self,
        branch_name: _Optional[str] = ...,
        dataset_id: _Optional[str] = ...,
        dataset_revision_id: _Optional[str] = ...,
        reference_output: _Optional[str] = ...,
        evaluators: _Optional[_Iterable[str]] = ...,
        related_named_prompt_ids: _Optional[_Iterable[str]] = ...,
        related_evaluation_ids: _Optional[_Iterable[str]] = ...,
        meta_data: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
        prompt_variants: _Optional[_Iterable[_Union[PromptVariantOperation, _Mapping]]] = ...,
    ) -> None: ...

class CreatePromptEvaluationRunResponse(_message.Message):
    __slots__ = ("evaluation_run",)
    EVALUATION_RUN_FIELD_NUMBER: _ClassVar[int]
    evaluation_run: PromptEvaluationRun
    def __init__(self, evaluation_run: _Optional[_Union[PromptEvaluationRun, _Mapping]] = ...) -> None: ...
