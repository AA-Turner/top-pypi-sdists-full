# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Literal, Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["CompletionCreateParamsBase", "CompletionCreateParamsNonStreaming", "CompletionCreateParamsStreaming"]


class CompletionCreateParamsBase(TypedDict, total=False):
    model: Required[str]
    """model specified as `model_vendor/model`, for example `openai/gpt-4o`"""

    prompt: Required[Union[str, SequenceNotStr[str]]]
    """The prompt to generate completions for, encoded as a string"""

    best_of: int
    """Generates best_of completions server-side and returns the best one.

    Must be greater than n when used together.
    """

    echo: bool
    """Echo back the prompt in addition to the completion"""

    frequency_penalty: float
    """Number between -2.0 and 2.0.

    Positive values penalize new tokens based on their existing frequency in the
    text.
    """

    logit_bias: Dict[str, int]
    """Modify the likelihood of specified tokens appearing in the completion.

    Maps tokens to bias values from -100 to 100.
    """

    logprobs: int
    """Include log probabilities of the most likely tokens. Maximum value is 5."""

    max_tokens: int
    """The maximum number of tokens that can be generated in the completion."""

    n: int
    """How many completions to generate for each prompt."""

    presence_penalty: float
    """Number between -2.0 and 2.0.

    Positive values penalize new tokens based on their presence in the text so far.
    """

    seed: int
    """If specified, attempts to generate deterministic samples.

    Determinism is not guaranteed.
    """

    stop: Union[str, SequenceNotStr[str]]
    """Up to 4 sequences where the API will stop generating further tokens."""

    stream_options: Dict[str, object]
    """Options for streaming response. Only set this when stream is True."""

    suffix: str
    """The suffix that comes after a completion of inserted text.

    Only supported for gpt-3.5-turbo-instruct.
    """

    temperature: float
    """Sampling temperature between 0 and 2.

    Higher values make output more random, lower more focused.
    """

    top_p: float
    """Alternative to temperature.

    Consider only tokens with top_p probability mass. Range 0-1.
    """

    user: str
    """
    A unique identifier representing your end-user, which can help OpenAI monitor
    and detect abuse.
    """


class CompletionCreateParamsNonStreaming(CompletionCreateParamsBase, total=False):
    stream: Literal[False]
    """Whether to stream back partial progress.

    If set, tokens will be sent as data-only server-sent events.
    """


class CompletionCreateParamsStreaming(CompletionCreateParamsBase):
    stream: Required[Literal[True]]
    """Whether to stream back partial progress.

    If set, tokens will be sent as data-only server-sent events.
    """


CompletionCreateParams = Union[CompletionCreateParamsNonStreaming, CompletionCreateParamsStreaming]
