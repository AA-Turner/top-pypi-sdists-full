# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from pydantic import Field as FieldInfo

from .._utils import PropertyInfo
from .._models import BaseModel
from .item_locator import ItemLocator
from .launch_inference_configuration import LaunchInferenceConfiguration
from .auto_evaluation_agent_task_request_with_item_locator import AutoEvaluationAgentTaskRequestWithItemLocator

__all__ = [
    "EvaluationTask",
    "ChatCompletionEvaluationTask",
    "ChatCompletionEvaluationTaskConfiguration",
    "GenericInferenceEvaluationTask",
    "GenericInferenceEvaluationTaskConfiguration",
    "GenericInferenceEvaluationTaskConfigurationInferenceConfiguration",
    "ApplicationVariantV1EvaluationTask",
    "ApplicationVariantV1EvaluationTaskConfiguration",
    "ApplicationVariantV1EvaluationTaskConfigurationHistoryApplicationRequestResponsePairArray",
    "ApplicationVariantV1EvaluationTaskConfigurationOverrides",
    "ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverrides",
    "ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesInitialState",
    "ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesPartialTrace",
    "AgentexOutputEvaluationTask",
    "AgentexOutputEvaluationTaskConfiguration",
    "MetricEvaluationTask",
    "MetricEvaluationTaskConfiguration",
    "MetricEvaluationTaskConfigurationBleuScorerConfigWithItemLocator",
    "MetricEvaluationTaskConfigurationMeteorScorerConfigWithItemLocator",
    "MetricEvaluationTaskConfigurationCosineSimilarityScorerConfigWithItemLocator",
    "MetricEvaluationTaskConfigurationF1ScorerConfigWithItemLocator",
    "MetricEvaluationTaskConfigurationRougeScorer1ConfigWithItemLocator",
    "MetricEvaluationTaskConfigurationRougeScorer2ConfigWithItemLocator",
    "MetricEvaluationTaskConfigurationRougeScorerLConfigWithItemLocator",
    "AutoEvaluationQuestionTask",
    "AutoEvaluationQuestionTaskConfiguration",
    "AutoEvaluationGuidedDecodingEvaluationTask",
    "AutoEvaluationGuidedDecodingEvaluationTaskConfiguration",
    "AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocator",
    "AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocator",
    "AutoEvaluationAgentEvaluationTask",
    "ContributorEvaluationQuestionTask",
    "ContributorEvaluationQuestionTaskConfiguration",
    "CustomFunctionEvaluationTask",
    "CustomFunctionEvaluationTaskConfiguration",
]


class ChatCompletionEvaluationTaskConfiguration(BaseModel):
    messages: Union[List[Dict[str, object]], ItemLocator]

    model: str

    audio: Union[Dict[str, object], ItemLocator, None] = None

    frequency_penalty: Union[float, ItemLocator, None] = None

    function_call: Union[Dict[str, object], ItemLocator, None] = None

    functions: Union[List[Dict[str, object]], ItemLocator, None] = None

    logit_bias: Union[Dict[str, int], ItemLocator, None] = None

    logprobs: Union[bool, ItemLocator, None] = None

    max_completion_tokens: Union[int, ItemLocator, None] = None

    max_tokens: Union[int, ItemLocator, None] = None

    metadata: Union[Dict[str, str], ItemLocator, None] = None

    modalities: Union[List[str], ItemLocator, None] = None

    n: Union[int, ItemLocator, None] = None

    parallel_tool_calls: Union[bool, ItemLocator, None] = None

    prediction: Union[Dict[str, object], ItemLocator, None] = None

    presence_penalty: Union[float, ItemLocator, None] = None

    reasoning_effort: Optional[str] = None

    response_format: Union[Dict[str, object], ItemLocator, None] = None

    seed: Union[int, ItemLocator, None] = None

    stop: Optional[str] = None

    store: Union[bool, ItemLocator, None] = None

    temperature: Union[float, ItemLocator, None] = None

    tool_choice: Optional[str] = None

    tools: Union[List[Dict[str, object]], ItemLocator, None] = None

    top_k: Union[int, ItemLocator, None] = None

    top_logprobs: Union[int, ItemLocator, None] = None

    top_p: Union[float, ItemLocator, None] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class ChatCompletionEvaluationTask(BaseModel):
    configuration: ChatCompletionEvaluationTaskConfiguration

    alias: Optional[str] = None
    """Alias to title the results column. Defaults to the `chat_completion`"""

    task_type: Optional[Literal["chat_completion"]] = None


GenericInferenceEvaluationTaskConfigurationInferenceConfiguration: TypeAlias = Union[
    LaunchInferenceConfiguration, ItemLocator
]


class GenericInferenceEvaluationTaskConfiguration(BaseModel):
    model: str

    args: Union[Dict[str, object], ItemLocator, None] = None

    inference_configuration: Optional[GenericInferenceEvaluationTaskConfigurationInferenceConfiguration] = None


class GenericInferenceEvaluationTask(BaseModel):
    configuration: GenericInferenceEvaluationTaskConfiguration

    alias: Optional[str] = None
    """Alias to title the results column. Defaults to the `inference`"""

    task_type: Optional[Literal["inference"]] = None


class ApplicationVariantV1EvaluationTaskConfigurationHistoryApplicationRequestResponsePairArray(BaseModel):
    request: str
    """Request inputs"""

    response: str
    """Response outputs"""

    session_data: Optional[Dict[str, object]] = None
    """Session data corresponding to the request response pair"""


class ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesInitialState(BaseModel):
    current_node: str

    state: Dict[str, object]


class ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesPartialTrace(BaseModel):
    duration_ms: int

    node_id: str

    operation_input: str

    operation_output: str

    operation_type: str

    start_timestamp: str

    workflow_id: str

    operation_metadata: Optional[Dict[str, object]] = None


class ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverrides(BaseModel):
    """Execution override options for agentic applications"""

    concurrent: Optional[bool] = None

    initial_state: Optional[
        ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesInitialState
    ] = None

    partial_trace: Optional[
        List[ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesPartialTrace]
    ] = None

    return_span: Optional[bool] = None

    use_channels: Optional[bool] = None


ApplicationVariantV1EvaluationTaskConfigurationOverrides: TypeAlias = Union[
    ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverrides, ItemLocator
]


class ApplicationVariantV1EvaluationTaskConfiguration(BaseModel):
    application_variant_id: str

    inputs: Union[Dict[str, object], ItemLocator]

    history: Union[
        List[ApplicationVariantV1EvaluationTaskConfigurationHistoryApplicationRequestResponsePairArray],
        ItemLocator,
        None,
    ] = None

    operation_metadata: Union[Dict[str, object], ItemLocator, None] = None

    overrides: Optional[ApplicationVariantV1EvaluationTaskConfigurationOverrides] = None
    """Execution override options for agentic applications"""


class ApplicationVariantV1EvaluationTask(BaseModel):
    configuration: ApplicationVariantV1EvaluationTaskConfiguration

    alias: Optional[str] = None
    """Alias to title the results column. Defaults to the `application_variant`"""

    task_type: Optional[Literal["application_variant"]] = None


class AgentexOutputEvaluationTaskConfiguration(BaseModel):
    agentex_agent_id: str

    input_column: Union[str, Dict[str, object], List[object]]

    include_traces: Union[bool, ItemLocator, None] = None

    timeout_seconds: Union[int, ItemLocator, None] = None


class AgentexOutputEvaluationTask(BaseModel):
    configuration: AgentexOutputEvaluationTaskConfiguration

    alias: Optional[str] = None
    """Alias to title the results column. Defaults to the `agentex_output`"""

    task_type: Optional[Literal["agentex_output"]] = None


class MetricEvaluationTaskConfigurationBleuScorerConfigWithItemLocator(BaseModel):
    candidate: str

    reference: str

    type: Literal["bleu"]


class MetricEvaluationTaskConfigurationMeteorScorerConfigWithItemLocator(BaseModel):
    candidate: str

    reference: str

    type: Literal["meteor"]


class MetricEvaluationTaskConfigurationCosineSimilarityScorerConfigWithItemLocator(BaseModel):
    candidate: str

    reference: str

    type: Literal["cosine_similarity"]


class MetricEvaluationTaskConfigurationF1ScorerConfigWithItemLocator(BaseModel):
    candidate: str

    reference: str

    type: Literal["f1"]


class MetricEvaluationTaskConfigurationRougeScorer1ConfigWithItemLocator(BaseModel):
    candidate: str

    reference: str

    type: Literal["rouge1"]


class MetricEvaluationTaskConfigurationRougeScorer2ConfigWithItemLocator(BaseModel):
    candidate: str

    reference: str

    type: Literal["rouge2"]


class MetricEvaluationTaskConfigurationRougeScorerLConfigWithItemLocator(BaseModel):
    candidate: str

    reference: str

    type: Literal["rougeL"]


MetricEvaluationTaskConfiguration: TypeAlias = Annotated[
    Union[
        MetricEvaluationTaskConfigurationBleuScorerConfigWithItemLocator,
        MetricEvaluationTaskConfigurationMeteorScorerConfigWithItemLocator,
        MetricEvaluationTaskConfigurationCosineSimilarityScorerConfigWithItemLocator,
        MetricEvaluationTaskConfigurationF1ScorerConfigWithItemLocator,
        MetricEvaluationTaskConfigurationRougeScorer1ConfigWithItemLocator,
        MetricEvaluationTaskConfigurationRougeScorer2ConfigWithItemLocator,
        MetricEvaluationTaskConfigurationRougeScorerLConfigWithItemLocator,
    ],
    PropertyInfo(discriminator="type"),
]


class MetricEvaluationTask(BaseModel):
    configuration: MetricEvaluationTaskConfiguration

    alias: Optional[str] = None
    """Alias to title the results column.

    Defaults to the metric type specified in the configuration
    """

    task_type: Optional[Literal["metric"]] = None


class AutoEvaluationQuestionTaskConfiguration(BaseModel):
    model: str
    """model specified as `model_vendor/model_name`"""

    prompt: str

    question_id: str
    """question to be evaluated"""


class AutoEvaluationQuestionTask(BaseModel):
    configuration: AutoEvaluationQuestionTaskConfiguration

    alias: Optional[str] = None
    """Alias to title the results column. Defaults to the `auto_evaluation_question`"""

    task_type: Optional[Literal["auto_evaluation.question"]] = None


class AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocator(
    BaseModel
):
    model: str
    """model specified as `model_vendor/model_name`"""

    prompt: str

    response_format: Dict[str, object]
    """JSON schema used for structuring the model response"""

    inference_args: Optional[Dict[str, object]] = None
    """Additional arguments to pass to the inference request"""

    system_prompt: Optional[str] = None


class AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocator(
    BaseModel
):
    choices: List[str]
    """Choices array cannot be empty"""

    model: str
    """model specified as `model_vendor/model_name`"""

    prompt: str

    inference_args: Optional[Dict[str, object]] = None
    """Additional arguments to pass to the inference request"""

    system_prompt: Optional[str] = None


AutoEvaluationGuidedDecodingEvaluationTaskConfiguration: TypeAlias = Union[
    AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocator,
    AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocator,
    AutoEvaluationAgentTaskRequestWithItemLocator,
]


class AutoEvaluationGuidedDecodingEvaluationTask(BaseModel):
    configuration: AutoEvaluationGuidedDecodingEvaluationTaskConfiguration

    alias: Optional[str] = None
    """Alias to title the results column.

    Defaults to the `auto_evaluation_guided_decoding`
    """

    task_type: Optional[Literal["auto_evaluation.guided_decoding"]] = None


class AutoEvaluationAgentEvaluationTask(BaseModel):
    configuration: AutoEvaluationAgentTaskRequestWithItemLocator

    alias: Optional[str] = None
    """Alias to title the results column. Defaults to the `auto_evaluation_agent`"""

    task_type: Optional[Literal["auto_evaluation.agent"]] = None


class ContributorEvaluationQuestionTaskConfiguration(BaseModel):
    layout: "Container"

    question_id: str

    queue_id: Optional[str] = None
    """The contributor annotation queue to include this task in. Defaults to `default`"""

    required: Optional[bool] = None
    """Whether the question is required to be answered"""

    rubric_id: Optional[str] = None
    """ID of the rubric to use for scoring this evaluation question"""


class ContributorEvaluationQuestionTask(BaseModel):
    configuration: ContributorEvaluationQuestionTaskConfiguration

    alias: Optional[str] = None
    """Alias to title the results column.

    Defaults to the `contributor_evaluation_question`
    """

    task_type: Optional[Literal["contributor_evaluation.question"]] = None


class CustomFunctionEvaluationTaskConfiguration(BaseModel):
    """Configuration for a custom Python function evaluation task."""

    function_source: str
    """Python function source code"""

    arg_mapping: Optional[Dict[str, str]] = None
    """Mapping of function parameter names to item locators (e.g.

    item.field). Auto-derived from function signature if not provided.
    """


class CustomFunctionEvaluationTask(BaseModel):
    configuration: CustomFunctionEvaluationTaskConfiguration
    """Configuration for a custom Python function evaluation task."""

    alias: Optional[str] = None
    """Alias to title the results column. Defaults to the function name."""

    task_type: Optional[Literal["custom_function"]] = None


EvaluationTask: TypeAlias = Annotated[
    Union[
        ChatCompletionEvaluationTask,
        GenericInferenceEvaluationTask,
        ApplicationVariantV1EvaluationTask,
        AgentexOutputEvaluationTask,
        MetricEvaluationTask,
        AutoEvaluationQuestionTask,
        AutoEvaluationGuidedDecodingEvaluationTask,
        AutoEvaluationAgentEvaluationTask,
        ContributorEvaluationQuestionTask,
        CustomFunctionEvaluationTask,
    ],
    PropertyInfo(discriminator="task_type"),
]

from .container import Container
