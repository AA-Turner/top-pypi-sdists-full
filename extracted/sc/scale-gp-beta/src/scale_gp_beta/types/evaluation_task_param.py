# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict, TypeAliasType

from .._types import SequenceNotStr
from .._compat import PYDANTIC_V1
from .item_locator import ItemLocator
from .eq_evaluation_run_condition_param import EqEvaluationRunConditionParam
from .gt_evaluation_run_condition_param import GtEvaluationRunConditionParam
from .in_evaluation_run_condition_param import InEvaluationRunConditionParam
from .lt_evaluation_run_condition_param import LtEvaluationRunConditionParam
from .ne_evaluation_run_condition_param import NeEvaluationRunConditionParam
from .or_evaluation_run_condition_param import OrEvaluationRunConditionParam
from .and_evaluation_run_condition_param import AndEvaluationRunConditionParam
from .gte_evaluation_run_condition_param import GteEvaluationRunConditionParam
from .lte_evaluation_run_condition_param import LteEvaluationRunConditionParam
from .not_evaluation_run_condition_param import NotEvaluationRunConditionParam
from .launch_inference_configuration_param import LaunchInferenceConfigurationParam
from .not_in_evaluation_run_condition_param import NotInEvaluationRunConditionParam
from .is_null_evaluation_run_condition_param import IsNullEvaluationRunConditionParam
from .is_not_null_evaluation_run_condition_param import IsNotNullEvaluationRunConditionParam
from .auto_evaluation_agent_task_request_with_item_locator_param import (
    AutoEvaluationAgentTaskRequestWithItemLocatorParam,
)

__all__ = [
    "EvaluationTaskParam",
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


class ChatCompletionEvaluationTaskConfiguration(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    messages: Required[Union[Iterable[Dict[str, object]], ItemLocator]]
    """openai standard message format"""

    model: Required[str]
    """model specified as `model_vendor/model`, for example `openai/gpt-4o`"""

    audio: Union[Dict[str, object], ItemLocator]
    """Parameters for audio output.

    Required when audio output is requested with modalities: ['audio'].
    """

    frequency_penalty: Union[float, ItemLocator]
    """Number between -2.0 and 2.0.

    Positive values penalize new tokens based on their existing frequency in the
    text so far.
    """

    function_call: Union[Dict[str, object], ItemLocator]
    """Deprecated in favor of tool_choice.

    Controls which function is called by the model.
    """

    functions: Union[Iterable[Dict[str, object]], ItemLocator]
    """Deprecated in favor of tools.

    A list of functions the model may generate JSON inputs for.
    """

    logit_bias: Union[Dict[str, int], ItemLocator]
    """Modify the likelihood of specified tokens appearing in the completion.

    Maps tokens to bias values from -100 to 100.
    """

    logprobs: Union[bool, ItemLocator]
    """Whether to return log probabilities of the output tokens or not."""

    max_completion_tokens: Union[int, ItemLocator]
    """
    An upper bound for the number of tokens that can be generated, including visible
    output tokens and reasoning tokens.
    """

    max_tokens: Union[int, ItemLocator]
    """Deprecated in favor of max_completion_tokens.

    The maximum number of tokens to generate.
    """

    metadata: Union[Dict[str, str], ItemLocator]
    """
    Developer-defined tags and values used for filtering completions in the
    dashboard.
    """

    modalities: Union[SequenceNotStr[str], ItemLocator]
    """Output types that you would like the model to generate for this request."""

    n: Union[int, ItemLocator]
    """How many chat completion choices to generate for each input message."""

    parallel_tool_calls: Union[bool, ItemLocator]
    """Whether to enable parallel function calling during tool use."""

    prediction: Union[Dict[str, object], ItemLocator]
    """
    Static predicted output content, such as the content of a text file being
    regenerated.
    """

    presence_penalty: Union[float, ItemLocator]
    """Number between -2.0 and 2.0.

    Positive values penalize tokens based on whether they appear in the text so far.
    """

    reasoning_effort: str
    """For o1 models only. Constrains effort on reasoning. Values: low, medium, high."""

    response_format: Union[Dict[str, object], ItemLocator]
    """An object specifying the format that the model must output."""

    seed: Union[int, ItemLocator]
    """
    If specified, system will attempt to sample deterministically for repeated
    requests with same seed.
    """

    stop: Union[str, SequenceNotStr[str]]
    """Up to 4 sequences where the API will stop generating further tokens."""

    store: Union[bool, ItemLocator]
    """Whether to store the output for use in model distillation or evals products."""

    temperature: Union[float, ItemLocator]
    """What sampling temperature to use.

    Higher values make output more random, lower more focused.
    """

    tool_choice: Union[str, Dict[str, object]]
    """Controls which tool is called by the model.

    Values: none, auto, required, or specific tool.
    """

    tools: Union[Iterable[Dict[str, object]], ItemLocator]
    """A list of tools the model may call.

    Currently, only functions are supported. Max 128 functions.
    """

    top_k: Union[int, ItemLocator]
    """Only sample from the top K options for each subsequent token"""

    top_logprobs: Union[int, ItemLocator]
    """
    Number of most likely tokens to return at each position, with associated log
    probability.
    """

    top_p: Union[float, ItemLocator]
    """Alternative to temperature.

    Only tokens comprising top_p probability mass are considered.
    """


class ChatCompletionEvaluationTask(TypedDict, total=False):
    configuration: Required[ChatCompletionEvaluationTaskConfiguration]

    alias: str
    """Alias to title the results column. Defaults to the `chat_completion`"""

    task_type: Literal["chat_completion"]


GenericInferenceEvaluationTaskConfigurationInferenceConfiguration: TypeAlias = Union[
    LaunchInferenceConfigurationParam, ItemLocator
]


class GenericInferenceEvaluationTaskConfiguration(TypedDict, total=False):
    model: Required[str]
    """model specified as `vendor/name` (ex. openai/gpt-5)"""

    args: Union[Dict[str, object], ItemLocator]
    """Arguments passed into model"""

    inference_configuration: GenericInferenceEvaluationTaskConfigurationInferenceConfiguration
    """Vendor specific configuration"""


class GenericInferenceEvaluationTask(TypedDict, total=False):
    configuration: Required[GenericInferenceEvaluationTaskConfiguration]

    alias: str
    """Alias to title the results column. Defaults to the `inference`"""

    task_type: Literal["inference"]


class ApplicationVariantV1EvaluationTaskConfigurationHistoryApplicationRequestResponsePairArray(TypedDict, total=False):
    request: Required[str]
    """Request inputs"""

    response: Required[str]
    """Response outputs"""

    session_data: Dict[str, object]
    """Session data corresponding to the request response pair"""


class ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesInitialState(
    TypedDict, total=False
):
    current_node: Required[str]

    state: Required[Dict[str, object]]


class ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesPartialTrace(
    TypedDict, total=False
):
    duration_ms: Required[int]

    node_id: Required[str]

    operation_input: Required[str]

    operation_output: Required[str]

    operation_type: Required[str]

    start_timestamp: Required[str]

    workflow_id: Required[str]

    operation_metadata: Dict[str, object]


class ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverrides(TypedDict, total=False):
    """Execution override options for agentic applications"""

    concurrent: bool

    initial_state: ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesInitialState

    partial_trace: Iterable[
        ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesPartialTrace
    ]

    return_span: bool

    use_channels: bool


class ApplicationVariantV1EvaluationTaskConfigurationOverridesUnionMember1ApplicationVariantV1EvaluationTaskConfigurationOverridesUnionMember1Item(
    TypedDict, total=False
):
    artifact_ids_filter: SequenceNotStr[str]

    artifact_name_regex: SequenceNotStr[str]

    type: Literal["knowledge_base_schema"]


ApplicationVariantV1EvaluationTaskConfigurationOverrides: TypeAlias = Union[
    ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverrides,
    Dict[
        str,
        ApplicationVariantV1EvaluationTaskConfigurationOverridesUnionMember1ApplicationVariantV1EvaluationTaskConfigurationOverridesUnionMember1Item,
    ],
    ItemLocator,
]


class ApplicationVariantV1EvaluationTaskConfiguration(TypedDict, total=False):
    application_variant_id: Required[str]

    inputs: Required[Union[Dict[str, object], ItemLocator]]
    """Input data for the application.

    For agents service variants, you must provide inputs as a mapping from
    `{input_name: input_value}`. For V0 variants, you must specify the node your
    input should be passed to, structuring your input as
    `{node_id: {input_name: input_value}}`.
    """

    history: Union[
        Iterable[ApplicationVariantV1EvaluationTaskConfigurationHistoryApplicationRequestResponsePairArray], ItemLocator
    ]
    """History of the application"""

    operation_metadata: Union[Dict[str, object], ItemLocator]
    """
    Arbitrary user-defined metadata that can be attached to the process operations
    and will be registered in the interaction.
    """

    overrides: ApplicationVariantV1EvaluationTaskConfigurationOverrides
    """Optional overrides for the application"""


class ApplicationVariantV1EvaluationTask(TypedDict, total=False):
    configuration: Required[ApplicationVariantV1EvaluationTaskConfiguration]

    alias: str
    """Alias to title the results column. Defaults to the `application_variant`"""

    task_type: Literal["application_variant"]


class AgentexOutputEvaluationTaskConfiguration(TypedDict, total=False):
    agentex_agent_id: Required[str]
    """The ID of the Agentex agent to use"""

    input_column: Required[Union[str, Dict[str, object], Iterable[object]]]
    """The dataset column to use as input for the agent"""

    deployment_id: str
    """Optional Agentex deployment ID to pin the eval to a specific deployment.

    When set, RPC traffic routes through
    /agents/{agent_id}/deployments/{deployment_id}/rpc. When unset, traffic uses the
    agent's default RPC endpoint, which resolves through the agent's current routing
    rules on the Agentex side.
    """

    include_traces: Union[bool, ItemLocator]
    """Whether to include trace data in the evaluation results"""

    timeout_seconds: Union[int, ItemLocator]
    """Maximum seconds to wait for agent completion per item.

    If not set, the server-side default of 60s applies.
    """


class AgentexOutputEvaluationTask(TypedDict, total=False):
    configuration: Required[AgentexOutputEvaluationTaskConfiguration]

    alias: str
    """Alias to title the results column. Defaults to the `agentex_output`"""

    task_type: Literal["agentex_output"]


class MetricEvaluationTaskConfigurationBleuScorerConfigWithItemLocator(TypedDict, total=False):
    candidate: Required[str]

    reference: Required[str]

    type: Required[Literal["bleu"]]


class MetricEvaluationTaskConfigurationMeteorScorerConfigWithItemLocator(TypedDict, total=False):
    candidate: Required[str]

    reference: Required[str]

    type: Required[Literal["meteor"]]


class MetricEvaluationTaskConfigurationCosineSimilarityScorerConfigWithItemLocator(TypedDict, total=False):
    candidate: Required[str]

    reference: Required[str]

    type: Required[Literal["cosine_similarity"]]


class MetricEvaluationTaskConfigurationF1ScorerConfigWithItemLocator(TypedDict, total=False):
    candidate: Required[str]

    reference: Required[str]

    type: Required[Literal["f1"]]


class MetricEvaluationTaskConfigurationRougeScorer1ConfigWithItemLocator(TypedDict, total=False):
    candidate: Required[str]

    reference: Required[str]

    type: Required[Literal["rouge1"]]


class MetricEvaluationTaskConfigurationRougeScorer2ConfigWithItemLocator(TypedDict, total=False):
    candidate: Required[str]

    reference: Required[str]

    type: Required[Literal["rouge2"]]


class MetricEvaluationTaskConfigurationRougeScorerLConfigWithItemLocator(TypedDict, total=False):
    candidate: Required[str]

    reference: Required[str]

    type: Required[Literal["rougeL"]]


MetricEvaluationTaskConfiguration: TypeAlias = Union[
    MetricEvaluationTaskConfigurationBleuScorerConfigWithItemLocator,
    MetricEvaluationTaskConfigurationMeteorScorerConfigWithItemLocator,
    MetricEvaluationTaskConfigurationCosineSimilarityScorerConfigWithItemLocator,
    MetricEvaluationTaskConfigurationF1ScorerConfigWithItemLocator,
    MetricEvaluationTaskConfigurationRougeScorer1ConfigWithItemLocator,
    MetricEvaluationTaskConfigurationRougeScorer2ConfigWithItemLocator,
    MetricEvaluationTaskConfigurationRougeScorerLConfigWithItemLocator,
]


class MetricEvaluationTask(TypedDict, total=False):
    configuration: Required[MetricEvaluationTaskConfiguration]

    alias: str
    """Alias to title the results column.

    Defaults to the metric type specified in the configuration
    """

    task_type: Literal["metric"]


class AutoEvaluationQuestionTaskConfiguration(TypedDict, total=False):
    model: Required[str]
    """model specified as `model_vendor/model_name`"""

    prompt: Required[str]

    question_id: Required[str]
    """question to be evaluated"""


class AutoEvaluationQuestionTask(TypedDict, total=False):
    configuration: Required[AutoEvaluationQuestionTaskConfiguration]

    alias: str
    """Alias to title the results column. Defaults to the `auto_evaluation_question`"""

    task_type: Literal["auto_evaluation.question"]


class AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocatorRunConditionConstEvaluationRunCondition(
    TypedDict, total=False
):
    op: Literal["const"]

    value: Union[str, float, bool]


class AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocatorRunConditionVarEvaluationRunCondition(
    TypedDict, total=False
):
    path: Required[str]

    op: Literal["var"]


if TYPE_CHECKING or not PYDANTIC_V1:
    AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocatorRunCondition = TypeAliasType(
        "AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocatorRunCondition",
        Union[
            AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocatorRunConditionConstEvaluationRunCondition,
            AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocatorRunConditionVarEvaluationRunCondition,
            EqEvaluationRunConditionParam,
            NeEvaluationRunConditionParam,
            LtEvaluationRunConditionParam,
            LteEvaluationRunConditionParam,
            GtEvaluationRunConditionParam,
            GteEvaluationRunConditionParam,
            AndEvaluationRunConditionParam,
            OrEvaluationRunConditionParam,
            InEvaluationRunConditionParam,
            NotInEvaluationRunConditionParam,
            NotEvaluationRunConditionParam,
            IsNullEvaluationRunConditionParam,
            IsNotNullEvaluationRunConditionParam,
        ],
    )
else:
    AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocatorRunCondition: TypeAlias = Union[
        AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocatorRunConditionConstEvaluationRunCondition,
        AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocatorRunConditionVarEvaluationRunCondition,
        EqEvaluationRunConditionParam,
        NeEvaluationRunConditionParam,
        LtEvaluationRunConditionParam,
        LteEvaluationRunConditionParam,
        GtEvaluationRunConditionParam,
        GteEvaluationRunConditionParam,
        AndEvaluationRunConditionParam,
        OrEvaluationRunConditionParam,
        InEvaluationRunConditionParam,
        NotInEvaluationRunConditionParam,
        NotEvaluationRunConditionParam,
        IsNullEvaluationRunConditionParam,
        IsNotNullEvaluationRunConditionParam,
    ]


class AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocator(
    TypedDict, total=False
):
    model: Required[str]
    """model specified as `model_vendor/model_name`"""

    prompt: Required[str]

    response_format: Required[Dict[str, object]]
    """JSON schema used for structuring the model response"""

    inference_args: Dict[str, object]
    """Additional arguments to pass to the inference request"""

    run_condition: AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocatorRunCondition

    system_prompt: str


class AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocatorRunConditionConstEvaluationRunCondition(
    TypedDict, total=False
):
    op: Literal["const"]

    value: Union[str, float, bool]


class AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocatorRunConditionVarEvaluationRunCondition(
    TypedDict, total=False
):
    path: Required[str]

    op: Literal["var"]


if TYPE_CHECKING or not PYDANTIC_V1:
    AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocatorRunCondition = TypeAliasType(
        "AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocatorRunCondition",
        Union[
            AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocatorRunConditionConstEvaluationRunCondition,
            AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocatorRunConditionVarEvaluationRunCondition,
            EqEvaluationRunConditionParam,
            NeEvaluationRunConditionParam,
            LtEvaluationRunConditionParam,
            LteEvaluationRunConditionParam,
            GtEvaluationRunConditionParam,
            GteEvaluationRunConditionParam,
            AndEvaluationRunConditionParam,
            OrEvaluationRunConditionParam,
            InEvaluationRunConditionParam,
            NotInEvaluationRunConditionParam,
            NotEvaluationRunConditionParam,
            IsNullEvaluationRunConditionParam,
            IsNotNullEvaluationRunConditionParam,
        ],
    )
else:
    AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocatorRunCondition: TypeAlias = Union[
        AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocatorRunConditionConstEvaluationRunCondition,
        AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocatorRunConditionVarEvaluationRunCondition,
        EqEvaluationRunConditionParam,
        NeEvaluationRunConditionParam,
        LtEvaluationRunConditionParam,
        LteEvaluationRunConditionParam,
        GtEvaluationRunConditionParam,
        GteEvaluationRunConditionParam,
        AndEvaluationRunConditionParam,
        OrEvaluationRunConditionParam,
        InEvaluationRunConditionParam,
        NotInEvaluationRunConditionParam,
        NotEvaluationRunConditionParam,
        IsNullEvaluationRunConditionParam,
        IsNotNullEvaluationRunConditionParam,
    ]


class AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocator(
    TypedDict, total=False
):
    choices: Required[SequenceNotStr[str]]
    """Choices array cannot be empty"""

    model: Required[str]
    """model specified as `model_vendor/model_name`"""

    prompt: Required[str]

    inference_args: Dict[str, object]
    """Additional arguments to pass to the inference request"""

    run_condition: AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocatorRunCondition

    system_prompt: str


AutoEvaluationGuidedDecodingEvaluationTaskConfiguration: TypeAlias = Union[
    AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationStructuredOutputTaskRequestWithItemLocator,
    AutoEvaluationGuidedDecodingEvaluationTaskConfigurationAutoEvaluationGuidedDecodingTaskRequestWithItemLocator,
    AutoEvaluationAgentTaskRequestWithItemLocatorParam,
]


class AutoEvaluationGuidedDecodingEvaluationTask(TypedDict, total=False):
    configuration: Required[AutoEvaluationGuidedDecodingEvaluationTaskConfiguration]

    alias: str
    """Alias to title the results column.

    Defaults to the `auto_evaluation_guided_decoding`
    """

    task_type: Literal["auto_evaluation.guided_decoding"]


class AutoEvaluationAgentEvaluationTask(TypedDict, total=False):
    configuration: Required[AutoEvaluationAgentTaskRequestWithItemLocatorParam]

    alias: str
    """Alias to title the results column. Defaults to the `auto_evaluation_agent`"""

    task_type: Literal["auto_evaluation.agent"]


class ContributorEvaluationQuestionTaskConfiguration(TypedDict, total=False):
    layout: Required["ContainerParam"]

    question_id: Required[str]

    queue_id: str
    """The contributor annotation queue to include this task in. Defaults to `default`"""

    required: bool
    """Whether the question is required to be answered"""

    rubric_id: str
    """ID of the rubric to use for scoring this evaluation question"""


class ContributorEvaluationQuestionTask(TypedDict, total=False):
    configuration: Required[ContributorEvaluationQuestionTaskConfiguration]

    alias: str
    """Alias to title the results column.

    Defaults to the `contributor_evaluation_question`
    """

    task_type: Literal["contributor_evaluation.question"]


class CustomFunctionEvaluationTaskConfigurationOutput(TypedDict, total=False):
    path: Required[str]
    """Dot path in the custom function return value to materialize."""

    alias: str
    """Result column alias. Defaults to path with dots replaced by underscores."""


class CustomFunctionEvaluationTaskConfiguration(TypedDict, total=False):
    """Configuration for a custom Python function evaluation task."""

    function_source: Required[str]
    """Python function source code"""

    arg_mapping: Dict[str, str]
    """Mapping of function parameter names to item locators (e.g.

    item.field). Auto-derived from function signature if not provided.
    """

    config_args: Dict[str, object]
    """Literal argument values for function parameters, such as thresholds or RNG
    seeds.

    Serialized JSON must be at most 10000 characters.
    """

    outputs: Iterable[CustomFunctionEvaluationTaskConfigurationOutput]
    """Optional output paths to materialize as separate result columns.

    If omitted, the function return value is stored only under the task alias/data
    key.
    """


class CustomFunctionEvaluationTask(TypedDict, total=False):
    configuration: Required[CustomFunctionEvaluationTaskConfiguration]
    """Configuration for a custom Python function evaluation task."""

    alias: str
    """Alias to title the results column. Defaults to the function name."""

    task_type: Literal["custom_function"]


EvaluationTaskParam: TypeAlias = Union[
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
]

from .container_param import ContainerParam
