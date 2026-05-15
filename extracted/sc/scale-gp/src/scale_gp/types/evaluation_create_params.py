# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .._types import SequenceNotStr
from .annotation_config_param import AnnotationConfigParam
from .multiturn_annotation_config_param import MultiturnAnnotationConfigParam
from .translation_annotation_config_param import TranslationAnnotationConfigParam
from .summarization_annotation_config_param import SummarizationAnnotationConfigParam
from .shared_params.auto_evaluation_parameters import AutoEvaluationParameters

__all__ = [
    "EvaluationCreateParams",
    "EvaluationBuilderRequest",
    "EvaluationBuilderRequestAnnotationConfig",
    "EvaluationBuilderRequestAnnotationConfigAnnotationConfigRequestBase",
    "EvaluationBuilderRequestAnnotationConfigAnnotationConfigRequestBaseComponent",
    "EvaluationBuilderRequestAnnotationConfigAnnotationConfigRequestBaseLlmPrompt",
    "EvaluationBuilderRequestAnnotationConfigAnnotationConfigRequestBaseLlmPromptVariable",
    "EvaluationBuilderRequestAnnotationConfigAnnotationConfigGenerationRequest",
    "EvaluationBuilderRequestInlineEvaluationConfig",
    "EvaluationBuilderRequestInlineEvaluationConfigAutoEvalEvaluationConfigRequest",
    "EvaluationBuilderRequestInlineEvaluationConfigManualEvaluationConfigRequest",
    "EvaluationBuilderRequestMetricConfig",
    "EvaluationBuilderRequestMetricConfigComponent",
    "DefaultEvaluationRequest",
    "DefaultEvaluationRequestAnnotationConfig",
    "DefaultEvaluationRequestAnnotationConfigAnnotationConfigRequestBase",
    "DefaultEvaluationRequestAnnotationConfigAnnotationConfigRequestBaseComponent",
    "DefaultEvaluationRequestAnnotationConfigAnnotationConfigRequestBaseLlmPrompt",
    "DefaultEvaluationRequestAnnotationConfigAnnotationConfigRequestBaseLlmPromptVariable",
    "DefaultEvaluationRequestAnnotationConfigAnnotationConfigGenerationRequest",
    "DefaultEvaluationRequestMetricConfig",
    "DefaultEvaluationRequestMetricConfigComponent",
]


class EvaluationBuilderRequest(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    application_spec_id: Required[str]

    application_variant_id: Required[str]

    description: Required[str]

    evaluation_dataset_id: Required[str]

    name: Required[str]

    annotation_config: EvaluationBuilderRequestAnnotationConfig
    """Annotation configuration for tasking"""

    application_test_case_output_group_id: str

    evaluation_config: Dict[str, object]

    evaluation_config_id: str
    """The ID of the associated evaluation config."""

    evaluation_dataset_version: int

    inline_evaluation_config: EvaluationBuilderRequestInlineEvaluationConfig
    """Inline evaluation config data to create atomically with the evaluation.

    Provide this OR evaluation_config_id, not both.
    """

    metric_config: EvaluationBuilderRequestMetricConfig
    """Specifies the config for the metrics to be computed."""

    question_id_to_annotation_config: Dict[str, AnnotationConfigParam]
    """Specifies the annotation configuration to use for specific questions."""

    tags: Dict[str, object]

    type: Literal["builder"]
    """
    create standalone evaluation or build evaluation which will auto generate test
    case results
    """


class EvaluationBuilderRequestAnnotationConfigAnnotationConfigRequestBaseComponent(TypedDict, total=False):
    data_loc: Required[SequenceNotStr[str]]

    label: str

    optional: bool


class EvaluationBuilderRequestAnnotationConfigAnnotationConfigRequestBaseLlmPromptVariable(TypedDict, total=False):
    data_loc: Required[SequenceNotStr[str]]

    name: Required[str]

    optional: bool


class EvaluationBuilderRequestAnnotationConfigAnnotationConfigRequestBaseLlmPrompt(TypedDict, total=False):
    template: Required[str]

    variables: Required[Iterable[EvaluationBuilderRequestAnnotationConfigAnnotationConfigRequestBaseLlmPromptVariable]]


class EvaluationBuilderRequestAnnotationConfigAnnotationConfigRequestBase(TypedDict, total=False):
    components: Iterable[Iterable[EvaluationBuilderRequestAnnotationConfigAnnotationConfigRequestBaseComponent]]

    direction: Literal["col", "row"]

    llm_prompt: EvaluationBuilderRequestAnnotationConfigAnnotationConfigRequestBaseLlmPrompt


class EvaluationBuilderRequestAnnotationConfigAnnotationConfigGenerationRequest(TypedDict, total=False):
    llm_prompt_template: Required[str]


EvaluationBuilderRequestAnnotationConfig: TypeAlias = Union[
    EvaluationBuilderRequestAnnotationConfigAnnotationConfigRequestBase,
    EvaluationBuilderRequestAnnotationConfigAnnotationConfigGenerationRequest,
    MultiturnAnnotationConfigParam,
    SummarizationAnnotationConfigParam,
    TranslationAnnotationConfigParam,
]


class EvaluationBuilderRequestInlineEvaluationConfigAutoEvalEvaluationConfigRequest(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    question_set_id: Required[str]

    auto_evaluation_model: Literal[
        "llama-3-1-70b-instruct",
        "gpt-4-turbo-2024-04-09",
        "llama-3-70b-instruct-bedrock",
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4.1",
        "gpt-4.1-mini",
        "gpt-4.1-nano",
        "gpt-5-nano",
        "gpt-5-mini",
        "gpt-5",
        "gpt-5.1",
        "gpt-5.2",
        "o1",
        "o3",
        "o3-mini",
        "o4-mini",
    ]
    """The name of the model to be used for auto-evaluation"""

    auto_evaluation_parameters: AutoEvaluationParameters
    """Execution parameters for auto-evaluation"""

    evaluation_type: Literal["llm_auto", "llm_benchmark"]
    """Evaluation type"""

    studio_project_id: str


class EvaluationBuilderRequestInlineEvaluationConfigManualEvaluationConfigRequest(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    question_set_id: Required[str]

    auto_evaluation_model: None
    """The name of the model to be used for auto-evaluation.

    Not applicable for manual evaluations.
    """

    auto_evaluation_parameters: AutoEvaluationParameters
    """Execution parameters for auto-evaluation"""

    evaluation_type: Literal["studio", "human"]
    """Evaluation type"""

    studio_project_id: str


EvaluationBuilderRequestInlineEvaluationConfig: TypeAlias = Union[
    EvaluationBuilderRequestInlineEvaluationConfigAutoEvalEvaluationConfigRequest,
    EvaluationBuilderRequestInlineEvaluationConfigManualEvaluationConfigRequest,
]


class EvaluationBuilderRequestMetricConfigComponent(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["rouge", "rouge1", "rouge2", "rougeL", "bleu", "meteor", "cosine_similarity", "f1"]]

    mappings: Dict[str, SequenceNotStr[str]]

    params: Dict[str, object]


class EvaluationBuilderRequestMetricConfig(TypedDict, total=False):
    """Specifies the config for the metrics to be computed."""

    components: Required[Iterable[EvaluationBuilderRequestMetricConfigComponent]]


class DefaultEvaluationRequest(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    application_spec_id: Required[str]

    description: Required[str]

    name: Required[str]

    annotation_config: DefaultEvaluationRequestAnnotationConfig
    """Annotation configuration for tasking"""

    application_variant_id: str

    evaluation_config: Dict[str, object]

    evaluation_config_id: str
    """The ID of the associated evaluation config."""

    metric_config: DefaultEvaluationRequestMetricConfig
    """Specifies the config for the metrics to be computed."""

    question_id_to_annotation_config: Dict[str, AnnotationConfigParam]
    """Specifies the annotation configuration to use for specific questions."""

    tags: Dict[str, object]

    type: Literal["default"]
    """
    create standalone evaluation or build evaluation which will auto generate test
    case results
    """


class DefaultEvaluationRequestAnnotationConfigAnnotationConfigRequestBaseComponent(TypedDict, total=False):
    data_loc: Required[SequenceNotStr[str]]

    label: str

    optional: bool


class DefaultEvaluationRequestAnnotationConfigAnnotationConfigRequestBaseLlmPromptVariable(TypedDict, total=False):
    data_loc: Required[SequenceNotStr[str]]

    name: Required[str]

    optional: bool


class DefaultEvaluationRequestAnnotationConfigAnnotationConfigRequestBaseLlmPrompt(TypedDict, total=False):
    template: Required[str]

    variables: Required[Iterable[DefaultEvaluationRequestAnnotationConfigAnnotationConfigRequestBaseLlmPromptVariable]]


class DefaultEvaluationRequestAnnotationConfigAnnotationConfigRequestBase(TypedDict, total=False):
    components: Iterable[Iterable[DefaultEvaluationRequestAnnotationConfigAnnotationConfigRequestBaseComponent]]

    direction: Literal["col", "row"]

    llm_prompt: DefaultEvaluationRequestAnnotationConfigAnnotationConfigRequestBaseLlmPrompt


class DefaultEvaluationRequestAnnotationConfigAnnotationConfigGenerationRequest(TypedDict, total=False):
    llm_prompt_template: Required[str]


DefaultEvaluationRequestAnnotationConfig: TypeAlias = Union[
    DefaultEvaluationRequestAnnotationConfigAnnotationConfigRequestBase,
    DefaultEvaluationRequestAnnotationConfigAnnotationConfigGenerationRequest,
    MultiturnAnnotationConfigParam,
    SummarizationAnnotationConfigParam,
    TranslationAnnotationConfigParam,
]


class DefaultEvaluationRequestMetricConfigComponent(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["rouge", "rouge1", "rouge2", "rougeL", "bleu", "meteor", "cosine_similarity", "f1"]]

    mappings: Dict[str, SequenceNotStr[str]]

    params: Dict[str, object]


class DefaultEvaluationRequestMetricConfig(TypedDict, total=False):
    """Specifies the config for the metrics to be computed."""

    components: Required[Iterable[DefaultEvaluationRequestMetricConfigComponent]]


EvaluationCreateParams: TypeAlias = Union[EvaluationBuilderRequest, DefaultEvaluationRequest]
