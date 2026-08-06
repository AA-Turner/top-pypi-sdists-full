# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias, TypeAliasType

from pydantic import Field as FieldInfo

from .._utils import PropertyInfo
from .._compat import PYDANTIC_V1
from .._models import BaseModel
from .item_locator import ItemLocator
from .eq_evaluation_run_condition import EqEvaluationRunCondition
from .gt_evaluation_run_condition import GtEvaluationRunCondition
from .in_evaluation_run_condition import InEvaluationRunCondition
from .lt_evaluation_run_condition import LtEvaluationRunCondition
from .ne_evaluation_run_condition import NeEvaluationRunCondition
from .or_evaluation_run_condition import OrEvaluationRunCondition
from .and_evaluation_run_condition import AndEvaluationRunCondition
from .gte_evaluation_run_condition import GteEvaluationRunCondition
from .lte_evaluation_run_condition import LteEvaluationRunCondition
from .not_evaluation_run_condition import NotEvaluationRunCondition
from .launch_inference_configuration import LaunchInferenceConfiguration
from .not_in_evaluation_run_condition import NotInEvaluationRunCondition
from .is_null_evaluation_run_condition import IsNullEvaluationRunCondition
from .is_not_null_evaluation_run_condition import IsNotNullEvaluationRunCondition
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
    "ApplicationVariantV1EvaluationTaskConfigurationOverridesUnionMember1ApplicationVariantV1EvaluationTaskConfigurationOverridesUnionMember1Item",
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
    "AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocatorRunCondition",
    "AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocatorRunConditionConstEvaluationRunCondition",
    "AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocatorRunConditionVarEvaluationRunCondition",
    "AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocator",
    "AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocatorRunCondition",
    "AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocatorRunConditionConstEvaluationRunCondition",
    "AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocatorRunConditionVarEvaluationRunCondition",
    "AutoEvaluationAgentEvaluationTask",
    "ContributorEvaluationQuestionTask",
    "ContributorEvaluationQuestionTaskConfiguration",
    "CustomFunctionEvaluationTask",
    "CustomFunctionEvaluationTaskConfiguration",
    "CustomFunctionEvaluationTaskConfigurationOutput",
]


class ChatCompletionEvaluationTaskConfiguration(BaseModel):
    messages: Union[List[Dict[str, object]], ItemLocator]
    """openai standard message format"""

    model: str
    """model specified as `model_vendor/model`, for example `openai/gpt-4o`"""

    audio: Union[Dict[str, object], ItemLocator, None] = None
    """Parameters for audio output.

    Required when audio output is requested with modalities: ['audio'].
    """

    frequency_penalty: Union[float, ItemLocator, None] = None
    """Number between -2.0 and 2.0.

    Positive values penalize new tokens based on their existing frequency in the
    text so far.
    """

    function_call: Union[Dict[str, object], ItemLocator, None] = None
    """Deprecated in favor of tool_choice.

    Controls which function is called by the model.
    """

    functions: Union[List[Dict[str, object]], ItemLocator, None] = None
    """Deprecated in favor of tools.

    A list of functions the model may generate JSON inputs for.
    """

    logit_bias: Union[Dict[str, int], ItemLocator, None] = None
    """Modify the likelihood of specified tokens appearing in the completion.

    Maps tokens to bias values from -100 to 100.
    """

    logprobs: Union[bool, ItemLocator, None] = None
    """Whether to return log probabilities of the output tokens or not."""

    max_completion_tokens: Union[int, ItemLocator, None] = None
    """
    An upper bound for the number of tokens that can be generated, including visible
    output tokens and reasoning tokens.
    """

    max_tokens: Union[int, ItemLocator, None] = None
    """Deprecated in favor of max_completion_tokens.

    The maximum number of tokens to generate.
    """

    metadata: Union[Dict[str, str], ItemLocator, None] = None
    """
    Developer-defined tags and values used for filtering completions in the
    dashboard.
    """

    modalities: Union[List[str], ItemLocator, None] = None
    """Output types that you would like the model to generate for this request."""

    n: Union[int, ItemLocator, None] = None
    """How many chat completion choices to generate for each input message."""

    parallel_tool_calls: Union[bool, ItemLocator, None] = None
    """Whether to enable parallel function calling during tool use."""

    prediction: Union[Dict[str, object], ItemLocator, None] = None
    """
    Static predicted output content, such as the content of a text file being
    regenerated.
    """

    presence_penalty: Union[float, ItemLocator, None] = None
    """Number between -2.0 and 2.0.

    Positive values penalize tokens based on whether they appear in the text so far.
    """

    reasoning_effort: Optional[str] = None
    """For o1 models only. Constrains effort on reasoning. Values: low, medium, high."""

    response_format: Union[Dict[str, object], ItemLocator, None] = None
    """An object specifying the format that the model must output."""

    seed: Union[int, ItemLocator, None] = None
    """
    If specified, system will attempt to sample deterministically for repeated
    requests with same seed.
    """

    stop: Union[str, List[str], None] = None
    """Up to 4 sequences where the API will stop generating further tokens."""

    store: Union[bool, ItemLocator, None] = None
    """Whether to store the output for use in model distillation or evals products."""

    temperature: Union[float, ItemLocator, None] = None
    """What sampling temperature to use.

    Higher values make output more random, lower more focused.
    """

    tool_choice: Union[str, Dict[str, object], None] = None
    """Controls which tool is called by the model.

    Values: none, auto, required, or specific tool.
    """

    tools: Union[List[Dict[str, object]], ItemLocator, None] = None
    """A list of tools the model may call.

    Currently, only functions are supported. Max 128 functions.
    """

    top_k: Union[int, ItemLocator, None] = None
    """Only sample from the top K options for each subsequent token"""

    top_logprobs: Union[int, ItemLocator, None] = None
    """
    Number of most likely tokens to return at each position, with associated log
    probability.
    """

    top_p: Union[float, ItemLocator, None] = None
    """Alternative to temperature.

    Only tokens comprising top_p probability mass are considered.
    """

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
    """model specified as `vendor/name` (ex. openai/gpt-5)"""

    args: Union[Dict[str, object], ItemLocator, None] = None
    """Arguments passed into model"""

    inference_configuration: Optional[GenericInferenceEvaluationTaskConfigurationInferenceConfiguration] = None
    """Vendor specific configuration"""


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


class ApplicationVariantV1EvaluationTaskConfigurationOverridesUnionMember1ApplicationVariantV1EvaluationTaskConfigurationOverridesUnionMember1Item(
    BaseModel
):
    artifact_ids_filter: Optional[List[str]] = None

    artifact_name_regex: Optional[List[str]] = None

    type: Optional[Literal["knowledge_base_schema"]] = None


ApplicationVariantV1EvaluationTaskConfigurationOverrides: TypeAlias = Union[
    ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverrides,
    Dict[
        str,
        ApplicationVariantV1EvaluationTaskConfigurationOverridesUnionMember1ApplicationVariantV1EvaluationTaskConfigurationOverridesUnionMember1Item,
    ],
    ItemLocator,
]


class ApplicationVariantV1EvaluationTaskConfiguration(BaseModel):
    application_variant_id: str

    inputs: Union[Dict[str, object], ItemLocator]
    """Input data for the application.

    For agents service variants, you must provide inputs as a mapping from
    `{input_name: input_value}`. For V0 variants, you must specify the node your
    input should be passed to, structuring your input as
    `{node_id: {input_name: input_value}}`.
    """

    history: Union[
        List[ApplicationVariantV1EvaluationTaskConfigurationHistoryApplicationRequestResponsePairArray],
        ItemLocator,
        None,
    ] = None
    """History of the application"""

    operation_metadata: Union[Dict[str, object], ItemLocator, None] = None
    """
    Arbitrary user-defined metadata that can be attached to the process operations
    and will be registered in the interaction.
    """

    overrides: Optional[ApplicationVariantV1EvaluationTaskConfigurationOverrides] = None
    """Optional overrides for the application"""


class ApplicationVariantV1EvaluationTask(BaseModel):
    configuration: ApplicationVariantV1EvaluationTaskConfiguration

    alias: Optional[str] = None
    """Alias to title the results column. Defaults to the `application_variant`"""

    task_type: Optional[Literal["application_variant"]] = None


class AgentexOutputEvaluationTaskConfiguration(BaseModel):
    agentex_agent_id: str
    """The ID of the Agentex agent to use"""

    input_column: Union[str, Dict[str, object], List[object]]
    """The dataset column to use as input for the agent"""

    deployment_id: Optional[str] = None
    """Optional Agentex deployment ID to pin the eval to a specific deployment.

    When set, RPC traffic routes through
    /agents/{agent_id}/deployments/{deployment_id}/rpc. When unset, traffic uses the
    agent's default RPC endpoint, which resolves through the agent's current routing
    rules on the Agentex side.
    """

    include_traces: Union[bool, ItemLocator, None] = None
    """Whether to include trace data in the evaluation results"""

    timeout_seconds: Union[int, ItemLocator, None] = None
    """Maximum seconds to wait for agent completion per item.

    If not set, the server-side default of 60s applies.
    """


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


class AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocatorRunConditionConstEvaluationRunCondition(
    BaseModel
):
    op: Optional[Literal["const"]] = None

    value: Union[str, float, bool, None] = None


class AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocatorRunConditionVarEvaluationRunCondition(
    BaseModel
):
    path: str

    op: Optional[Literal["var"]] = None


if TYPE_CHECKING or not PYDANTIC_V1:
    AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocatorRunCondition = TypeAliasType(
        "AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocatorRunCondition",
        Annotated[
            Union[
                AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocatorRunConditionConstEvaluationRunCondition,
                AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocatorRunConditionVarEvaluationRunCondition,
                EqEvaluationRunCondition,
                NeEvaluationRunCondition,
                LtEvaluationRunCondition,
                LteEvaluationRunCondition,
                GtEvaluationRunCondition,
                GteEvaluationRunCondition,
                AndEvaluationRunCondition,
                OrEvaluationRunCondition,
                InEvaluationRunCondition,
                NotInEvaluationRunCondition,
                NotEvaluationRunCondition,
                IsNullEvaluationRunCondition,
                IsNotNullEvaluationRunCondition,
            ],
            PropertyInfo(discriminator="op"),
        ],
    )
else:
    AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocatorRunCondition: TypeAlias = Annotated[
        Union[
            AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocatorRunConditionConstEvaluationRunCondition,
            AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocatorRunConditionVarEvaluationRunCondition,
            EqEvaluationRunCondition,
            NeEvaluationRunCondition,
            LtEvaluationRunCondition,
            LteEvaluationRunCondition,
            GtEvaluationRunCondition,
            GteEvaluationRunCondition,
            AndEvaluationRunCondition,
            OrEvaluationRunCondition,
            InEvaluationRunCondition,
            NotInEvaluationRunCondition,
            NotEvaluationRunCondition,
            IsNullEvaluationRunCondition,
            IsNotNullEvaluationRunCondition,
        ],
        PropertyInfo(discriminator="op"),
    ]


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

    run_condition: Optional[
        AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocatorRunCondition
    ] = None

    system_prompt: Optional[str] = None


class AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocatorRunConditionConstEvaluationRunCondition(
    BaseModel
):
    op: Optional[Literal["const"]] = None

    value: Union[str, float, bool, None] = None


class AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocatorRunConditionVarEvaluationRunCondition(
    BaseModel
):
    path: str

    op: Optional[Literal["var"]] = None


if TYPE_CHECKING or not PYDANTIC_V1:
    AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocatorRunCondition = TypeAliasType(
        "AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocatorRunCondition",
        Annotated[
            Union[
                AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocatorRunConditionConstEvaluationRunCondition,
                AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocatorRunConditionVarEvaluationRunCondition,
                EqEvaluationRunCondition,
                NeEvaluationRunCondition,
                LtEvaluationRunCondition,
                LteEvaluationRunCondition,
                GtEvaluationRunCondition,
                GteEvaluationRunCondition,
                AndEvaluationRunCondition,
                OrEvaluationRunCondition,
                InEvaluationRunCondition,
                NotInEvaluationRunCondition,
                NotEvaluationRunCondition,
                IsNullEvaluationRunCondition,
                IsNotNullEvaluationRunCondition,
            ],
            PropertyInfo(discriminator="op"),
        ],
    )
else:
    AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocatorRunCondition: TypeAlias = Annotated[
        Union[
            AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocatorRunConditionConstEvaluationRunCondition,
            AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocatorRunConditionVarEvaluationRunCondition,
            EqEvaluationRunCondition,
            NeEvaluationRunCondition,
            LtEvaluationRunCondition,
            LteEvaluationRunCondition,
            GtEvaluationRunCondition,
            GteEvaluationRunCondition,
            AndEvaluationRunCondition,
            OrEvaluationRunCondition,
            InEvaluationRunCondition,
            NotInEvaluationRunCondition,
            NotEvaluationRunCondition,
            IsNullEvaluationRunCondition,
            IsNotNullEvaluationRunCondition,
        ],
        PropertyInfo(discriminator="op"),
    ]


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

    run_condition: Optional[
        AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocatorRunCondition
    ] = None

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

    prefill_from: Optional[str] = None
    """Dataset column to prefill contributor question task result"""

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


class CustomFunctionEvaluationTaskConfigurationOutput(BaseModel):
    path: str
    """Dot path in the custom function return value to materialize."""

    alias: Optional[str] = None
    """Result column alias. Defaults to path with dots replaced by underscores."""


class CustomFunctionEvaluationTaskConfiguration(BaseModel):
    """Configuration for a custom Python function evaluation task."""

    function_source: str
    """Python function source code"""

    arg_mapping: Optional[Dict[str, str]] = None
    """Mapping of function parameter names to item locators (e.g.

    item.field). Auto-derived from function signature if not provided.
    """

    config_args: Optional[Dict[str, object]] = None
    """Literal argument values for function parameters, such as thresholds or RNG
    seeds.

    Serialized JSON must be at most 10000 characters.
    """

    outputs: Optional[List[CustomFunctionEvaluationTaskConfigurationOutput]] = None
    """Optional output paths to materialize as separate result columns.

    If omitted, the function return value is stored only under the task alias/data
    key.
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
