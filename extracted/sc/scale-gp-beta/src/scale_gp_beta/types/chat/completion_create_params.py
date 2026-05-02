# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._types import SequenceNotStr
from ..._utils import PropertyInfo

__all__ = ["CompletionCreateParamsBase", "CompletionCreateParamsNonStreaming", "CompletionCreateParamsStreaming"]


class CompletionCreateParamsBase(TypedDict, total=False):
    messages: Required[Iterable[Dict[str, object]]]
    """openai standard message format"""

    model: Required[str]
    """model specified as `model_vendor/model`, for example `openai/gpt-4o`"""

    audio: Dict[str, object]
    """Parameters for audio output.

    Required when audio output is requested with modalities: ['audio'].
    """

    frequency_penalty: float
    """Number between -2.0 and 2.0.

    Positive values penalize new tokens based on their existing frequency in the
    text so far.
    """

    function_call: Dict[str, object]
    """Deprecated in favor of tool_choice.

    Controls which function is called by the model.
    """

    functions: Iterable[Dict[str, object]]
    """Deprecated in favor of tools.

    A list of functions the model may generate JSON inputs for.
    """

    logit_bias: Dict[str, int]
    """Modify the likelihood of specified tokens appearing in the completion.

    Maps tokens to bias values from -100 to 100.
    """

    logprobs: bool
    """Whether to return log probabilities of the output tokens or not."""

    max_completion_tokens: int
    """
    An upper bound for the number of tokens that can be generated, including visible
    output tokens and reasoning tokens.
    """

    max_tokens: int
    """Deprecated in favor of max_completion_tokens.

    The maximum number of tokens to generate.
    """

    metadata: Dict[str, str]
    """
    Developer-defined tags and values used for filtering completions in the
    dashboard.
    """

    modalities: SequenceNotStr[str]
    """Output types that you would like the model to generate for this request."""

    n: int
    """How many chat completion choices to generate for each input message."""

    parallel_tool_calls: bool
    """Whether to enable parallel function calling during tool use."""

    prediction: Dict[str, object]
    """
    Static predicted output content, such as the content of a text file being
    regenerated.
    """

    presence_penalty: float
    """Number between -2.0 and 2.0.

    Positive values penalize tokens based on whether they appear in the text so far.
    """

    reasoning_effort: str
    """For o1 models only. Constrains effort on reasoning. Values: low, medium, high."""

    response_format: Dict[str, object]
    """An object specifying the format that the model must output."""

    seed: int
    """
    If specified, system will attempt to sample deterministically for repeated
    requests with same seed.
    """

    stop: Union[str, SequenceNotStr[str]]
    """Up to 4 sequences where the API will stop generating further tokens."""

    store: bool
    """Whether to store the output for use in model distillation or evals products."""

    stream_options: Dict[str, object]
    """Options for streaming response. Only set this when stream is true."""

    temperature: float
    """What sampling temperature to use.

    Higher values make output more random, lower more focused.
    """

    tool_choice: Union[str, Dict[str, object]]
    """Controls which tool is called by the model.

    Values: none, auto, required, or specific tool.
    """

    tools: Iterable[Dict[str, object]]
    """A list of tools the model may call.

    Currently, only functions are supported. Max 128 functions.
    """

    top_k: int
    """Only sample from the top K options for each subsequent token"""

    top_logprobs: int
    """
    Number of most likely tokens to return at each position, with associated log
    probability.
    """

    top_p: float
    """Alternative to temperature.

    Only tokens comprising top_p probability mass are considered.
    """

    x_openai_api_key: Annotated[str, PropertyInfo(alias="x-openai-api-key")]


class CompletionCreateParamsNonStreaming(CompletionCreateParamsBase, total=False):
    stream: Literal[False]
    """If true, partial message deltas will be sent as server-sent events."""


class CompletionCreateParamsStreaming(CompletionCreateParamsBase):
    stream: Required[Literal[True]]
    """If true, partial message deltas will be sent as server-sent events."""


CompletionCreateParams = Union[CompletionCreateParamsNonStreaming, CompletionCreateParamsStreaming]
