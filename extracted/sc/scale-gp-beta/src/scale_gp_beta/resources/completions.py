# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Literal, overload

import httpx

from ..types import completion_create_params
from .._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from .._utils import required_args, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._streaming import Stream, AsyncStream
from .._base_client import make_request_options
from ..types.completion import Completion

__all__ = ["CompletionsResource", "AsyncCompletionsResource"]


class CompletionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CompletionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return CompletionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CompletionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return CompletionsResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        *,
        model: str,
        prompt: Union[str, SequenceNotStr[str]],
        best_of: int | Omit = omit,
        echo: bool | Omit = omit,
        frequency_penalty: float | Omit = omit,
        logit_bias: Dict[str, int] | Omit = omit,
        logprobs: int | Omit = omit,
        max_tokens: int | Omit = omit,
        n: int | Omit = omit,
        presence_penalty: float | Omit = omit,
        seed: int | Omit = omit,
        stop: Union[str, SequenceNotStr[str]] | Omit = omit,
        stream: Literal[False] | Omit = omit,
        stream_options: Dict[str, object] | Omit = omit,
        suffix: str | Omit = omit,
        temperature: float | Omit = omit,
        top_p: float | Omit = omit,
        user: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Completion:
        """
        Completions

        Args:
          model: model specified as `model_vendor/model`, for example `openai/gpt-4o`

          prompt: The prompt to generate completions for, encoded as a string

          best_of: Generates best_of completions server-side and returns the best one. Must be
              greater than n when used together.

          echo: Echo back the prompt in addition to the completion

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text.

          logit_bias: Modify the likelihood of specified tokens appearing in the completion. Maps
              tokens to bias values from -100 to 100.

          logprobs: Include log probabilities of the most likely tokens. Maximum value is 5.

          max_tokens: The maximum number of tokens that can be generated in the completion.

          n: How many completions to generate for each prompt.

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              presence in the text so far.

          seed: If specified, attempts to generate deterministic samples. Determinism is not
              guaranteed.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          stream: Whether to stream back partial progress. If set, tokens will be sent as
              data-only server-sent events.

          stream_options: Options for streaming response. Only set this when stream is True.

          suffix: The suffix that comes after a completion of inserted text. Only supported for
              gpt-3.5-turbo-instruct.

          temperature: Sampling temperature between 0 and 2. Higher values make output more random,
              lower more focused.

          top_p: Alternative to temperature. Consider only tokens with top_p probability mass.
              Range 0-1.

          user: A unique identifier representing your end-user, which can help OpenAI monitor
              and detect abuse.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        *,
        model: str,
        prompt: Union[str, SequenceNotStr[str]],
        stream: Literal[True],
        best_of: int | Omit = omit,
        echo: bool | Omit = omit,
        frequency_penalty: float | Omit = omit,
        logit_bias: Dict[str, int] | Omit = omit,
        logprobs: int | Omit = omit,
        max_tokens: int | Omit = omit,
        n: int | Omit = omit,
        presence_penalty: float | Omit = omit,
        seed: int | Omit = omit,
        stop: Union[str, SequenceNotStr[str]] | Omit = omit,
        stream_options: Dict[str, object] | Omit = omit,
        suffix: str | Omit = omit,
        temperature: float | Omit = omit,
        top_p: float | Omit = omit,
        user: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Stream[Completion]:
        """
        Completions

        Args:
          model: model specified as `model_vendor/model`, for example `openai/gpt-4o`

          prompt: The prompt to generate completions for, encoded as a string

          stream: Whether to stream back partial progress. If set, tokens will be sent as
              data-only server-sent events.

          best_of: Generates best_of completions server-side and returns the best one. Must be
              greater than n when used together.

          echo: Echo back the prompt in addition to the completion

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text.

          logit_bias: Modify the likelihood of specified tokens appearing in the completion. Maps
              tokens to bias values from -100 to 100.

          logprobs: Include log probabilities of the most likely tokens. Maximum value is 5.

          max_tokens: The maximum number of tokens that can be generated in the completion.

          n: How many completions to generate for each prompt.

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              presence in the text so far.

          seed: If specified, attempts to generate deterministic samples. Determinism is not
              guaranteed.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          stream_options: Options for streaming response. Only set this when stream is True.

          suffix: The suffix that comes after a completion of inserted text. Only supported for
              gpt-3.5-turbo-instruct.

          temperature: Sampling temperature between 0 and 2. Higher values make output more random,
              lower more focused.

          top_p: Alternative to temperature. Consider only tokens with top_p probability mass.
              Range 0-1.

          user: A unique identifier representing your end-user, which can help OpenAI monitor
              and detect abuse.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        *,
        model: str,
        prompt: Union[str, SequenceNotStr[str]],
        stream: bool,
        best_of: int | Omit = omit,
        echo: bool | Omit = omit,
        frequency_penalty: float | Omit = omit,
        logit_bias: Dict[str, int] | Omit = omit,
        logprobs: int | Omit = omit,
        max_tokens: int | Omit = omit,
        n: int | Omit = omit,
        presence_penalty: float | Omit = omit,
        seed: int | Omit = omit,
        stop: Union[str, SequenceNotStr[str]] | Omit = omit,
        stream_options: Dict[str, object] | Omit = omit,
        suffix: str | Omit = omit,
        temperature: float | Omit = omit,
        top_p: float | Omit = omit,
        user: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Completion | Stream[Completion]:
        """
        Completions

        Args:
          model: model specified as `model_vendor/model`, for example `openai/gpt-4o`

          prompt: The prompt to generate completions for, encoded as a string

          stream: Whether to stream back partial progress. If set, tokens will be sent as
              data-only server-sent events.

          best_of: Generates best_of completions server-side and returns the best one. Must be
              greater than n when used together.

          echo: Echo back the prompt in addition to the completion

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text.

          logit_bias: Modify the likelihood of specified tokens appearing in the completion. Maps
              tokens to bias values from -100 to 100.

          logprobs: Include log probabilities of the most likely tokens. Maximum value is 5.

          max_tokens: The maximum number of tokens that can be generated in the completion.

          n: How many completions to generate for each prompt.

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              presence in the text so far.

          seed: If specified, attempts to generate deterministic samples. Determinism is not
              guaranteed.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          stream_options: Options for streaming response. Only set this when stream is True.

          suffix: The suffix that comes after a completion of inserted text. Only supported for
              gpt-3.5-turbo-instruct.

          temperature: Sampling temperature between 0 and 2. Higher values make output more random,
              lower more focused.

          top_p: Alternative to temperature. Consider only tokens with top_p probability mass.
              Range 0-1.

          user: A unique identifier representing your end-user, which can help OpenAI monitor
              and detect abuse.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["model", "prompt"], ["model", "prompt", "stream"])
    def create(
        self,
        *,
        model: str,
        prompt: Union[str, SequenceNotStr[str]],
        best_of: int | Omit = omit,
        echo: bool | Omit = omit,
        frequency_penalty: float | Omit = omit,
        logit_bias: Dict[str, int] | Omit = omit,
        logprobs: int | Omit = omit,
        max_tokens: int | Omit = omit,
        n: int | Omit = omit,
        presence_penalty: float | Omit = omit,
        seed: int | Omit = omit,
        stop: Union[str, SequenceNotStr[str]] | Omit = omit,
        stream: Literal[False] | Literal[True] | Omit = omit,
        stream_options: Dict[str, object] | Omit = omit,
        suffix: str | Omit = omit,
        temperature: float | Omit = omit,
        top_p: float | Omit = omit,
        user: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Completion | Stream[Completion]:
        return self._post(
            "/v5/completions",
            body=maybe_transform(
                {
                    "model": model,
                    "prompt": prompt,
                    "best_of": best_of,
                    "echo": echo,
                    "frequency_penalty": frequency_penalty,
                    "logit_bias": logit_bias,
                    "logprobs": logprobs,
                    "max_tokens": max_tokens,
                    "n": n,
                    "presence_penalty": presence_penalty,
                    "seed": seed,
                    "stop": stop,
                    "stream": stream,
                    "stream_options": stream_options,
                    "suffix": suffix,
                    "temperature": temperature,
                    "top_p": top_p,
                    "user": user,
                },
                completion_create_params.CompletionCreateParamsStreaming
                if stream
                else completion_create_params.CompletionCreateParamsNonStreaming,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Completion,
            stream=stream or False,
            stream_cls=Stream[Completion],
        )


class AsyncCompletionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCompletionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncCompletionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCompletionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncCompletionsResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        *,
        model: str,
        prompt: Union[str, SequenceNotStr[str]],
        best_of: int | Omit = omit,
        echo: bool | Omit = omit,
        frequency_penalty: float | Omit = omit,
        logit_bias: Dict[str, int] | Omit = omit,
        logprobs: int | Omit = omit,
        max_tokens: int | Omit = omit,
        n: int | Omit = omit,
        presence_penalty: float | Omit = omit,
        seed: int | Omit = omit,
        stop: Union[str, SequenceNotStr[str]] | Omit = omit,
        stream: Literal[False] | Omit = omit,
        stream_options: Dict[str, object] | Omit = omit,
        suffix: str | Omit = omit,
        temperature: float | Omit = omit,
        top_p: float | Omit = omit,
        user: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Completion:
        """
        Completions

        Args:
          model: model specified as `model_vendor/model`, for example `openai/gpt-4o`

          prompt: The prompt to generate completions for, encoded as a string

          best_of: Generates best_of completions server-side and returns the best one. Must be
              greater than n when used together.

          echo: Echo back the prompt in addition to the completion

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text.

          logit_bias: Modify the likelihood of specified tokens appearing in the completion. Maps
              tokens to bias values from -100 to 100.

          logprobs: Include log probabilities of the most likely tokens. Maximum value is 5.

          max_tokens: The maximum number of tokens that can be generated in the completion.

          n: How many completions to generate for each prompt.

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              presence in the text so far.

          seed: If specified, attempts to generate deterministic samples. Determinism is not
              guaranteed.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          stream: Whether to stream back partial progress. If set, tokens will be sent as
              data-only server-sent events.

          stream_options: Options for streaming response. Only set this when stream is True.

          suffix: The suffix that comes after a completion of inserted text. Only supported for
              gpt-3.5-turbo-instruct.

          temperature: Sampling temperature between 0 and 2. Higher values make output more random,
              lower more focused.

          top_p: Alternative to temperature. Consider only tokens with top_p probability mass.
              Range 0-1.

          user: A unique identifier representing your end-user, which can help OpenAI monitor
              and detect abuse.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        *,
        model: str,
        prompt: Union[str, SequenceNotStr[str]],
        stream: Literal[True],
        best_of: int | Omit = omit,
        echo: bool | Omit = omit,
        frequency_penalty: float | Omit = omit,
        logit_bias: Dict[str, int] | Omit = omit,
        logprobs: int | Omit = omit,
        max_tokens: int | Omit = omit,
        n: int | Omit = omit,
        presence_penalty: float | Omit = omit,
        seed: int | Omit = omit,
        stop: Union[str, SequenceNotStr[str]] | Omit = omit,
        stream_options: Dict[str, object] | Omit = omit,
        suffix: str | Omit = omit,
        temperature: float | Omit = omit,
        top_p: float | Omit = omit,
        user: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncStream[Completion]:
        """
        Completions

        Args:
          model: model specified as `model_vendor/model`, for example `openai/gpt-4o`

          prompt: The prompt to generate completions for, encoded as a string

          stream: Whether to stream back partial progress. If set, tokens will be sent as
              data-only server-sent events.

          best_of: Generates best_of completions server-side and returns the best one. Must be
              greater than n when used together.

          echo: Echo back the prompt in addition to the completion

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text.

          logit_bias: Modify the likelihood of specified tokens appearing in the completion. Maps
              tokens to bias values from -100 to 100.

          logprobs: Include log probabilities of the most likely tokens. Maximum value is 5.

          max_tokens: The maximum number of tokens that can be generated in the completion.

          n: How many completions to generate for each prompt.

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              presence in the text so far.

          seed: If specified, attempts to generate deterministic samples. Determinism is not
              guaranteed.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          stream_options: Options for streaming response. Only set this when stream is True.

          suffix: The suffix that comes after a completion of inserted text. Only supported for
              gpt-3.5-turbo-instruct.

          temperature: Sampling temperature between 0 and 2. Higher values make output more random,
              lower more focused.

          top_p: Alternative to temperature. Consider only tokens with top_p probability mass.
              Range 0-1.

          user: A unique identifier representing your end-user, which can help OpenAI monitor
              and detect abuse.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        *,
        model: str,
        prompt: Union[str, SequenceNotStr[str]],
        stream: bool,
        best_of: int | Omit = omit,
        echo: bool | Omit = omit,
        frequency_penalty: float | Omit = omit,
        logit_bias: Dict[str, int] | Omit = omit,
        logprobs: int | Omit = omit,
        max_tokens: int | Omit = omit,
        n: int | Omit = omit,
        presence_penalty: float | Omit = omit,
        seed: int | Omit = omit,
        stop: Union[str, SequenceNotStr[str]] | Omit = omit,
        stream_options: Dict[str, object] | Omit = omit,
        suffix: str | Omit = omit,
        temperature: float | Omit = omit,
        top_p: float | Omit = omit,
        user: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Completion | AsyncStream[Completion]:
        """
        Completions

        Args:
          model: model specified as `model_vendor/model`, for example `openai/gpt-4o`

          prompt: The prompt to generate completions for, encoded as a string

          stream: Whether to stream back partial progress. If set, tokens will be sent as
              data-only server-sent events.

          best_of: Generates best_of completions server-side and returns the best one. Must be
              greater than n when used together.

          echo: Echo back the prompt in addition to the completion

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text.

          logit_bias: Modify the likelihood of specified tokens appearing in the completion. Maps
              tokens to bias values from -100 to 100.

          logprobs: Include log probabilities of the most likely tokens. Maximum value is 5.

          max_tokens: The maximum number of tokens that can be generated in the completion.

          n: How many completions to generate for each prompt.

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              presence in the text so far.

          seed: If specified, attempts to generate deterministic samples. Determinism is not
              guaranteed.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          stream_options: Options for streaming response. Only set this when stream is True.

          suffix: The suffix that comes after a completion of inserted text. Only supported for
              gpt-3.5-turbo-instruct.

          temperature: Sampling temperature between 0 and 2. Higher values make output more random,
              lower more focused.

          top_p: Alternative to temperature. Consider only tokens with top_p probability mass.
              Range 0-1.

          user: A unique identifier representing your end-user, which can help OpenAI monitor
              and detect abuse.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["model", "prompt"], ["model", "prompt", "stream"])
    async def create(
        self,
        *,
        model: str,
        prompt: Union[str, SequenceNotStr[str]],
        best_of: int | Omit = omit,
        echo: bool | Omit = omit,
        frequency_penalty: float | Omit = omit,
        logit_bias: Dict[str, int] | Omit = omit,
        logprobs: int | Omit = omit,
        max_tokens: int | Omit = omit,
        n: int | Omit = omit,
        presence_penalty: float | Omit = omit,
        seed: int | Omit = omit,
        stop: Union[str, SequenceNotStr[str]] | Omit = omit,
        stream: Literal[False] | Literal[True] | Omit = omit,
        stream_options: Dict[str, object] | Omit = omit,
        suffix: str | Omit = omit,
        temperature: float | Omit = omit,
        top_p: float | Omit = omit,
        user: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Completion | AsyncStream[Completion]:
        return await self._post(
            "/v5/completions",
            body=await async_maybe_transform(
                {
                    "model": model,
                    "prompt": prompt,
                    "best_of": best_of,
                    "echo": echo,
                    "frequency_penalty": frequency_penalty,
                    "logit_bias": logit_bias,
                    "logprobs": logprobs,
                    "max_tokens": max_tokens,
                    "n": n,
                    "presence_penalty": presence_penalty,
                    "seed": seed,
                    "stop": stop,
                    "stream": stream,
                    "stream_options": stream_options,
                    "suffix": suffix,
                    "temperature": temperature,
                    "top_p": top_p,
                    "user": user,
                },
                completion_create_params.CompletionCreateParamsStreaming
                if stream
                else completion_create_params.CompletionCreateParamsNonStreaming,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Completion,
            stream=stream or False,
            stream_cls=AsyncStream[Completion],
        )


class CompletionsResourceWithRawResponse:
    def __init__(self, completions: CompletionsResource) -> None:
        self._completions = completions

        self.create = to_raw_response_wrapper(
            completions.create,
        )


class AsyncCompletionsResourceWithRawResponse:
    def __init__(self, completions: AsyncCompletionsResource) -> None:
        self._completions = completions

        self.create = async_to_raw_response_wrapper(
            completions.create,
        )


class CompletionsResourceWithStreamingResponse:
    def __init__(self, completions: CompletionsResource) -> None:
        self._completions = completions

        self.create = to_streamed_response_wrapper(
            completions.create,
        )


class AsyncCompletionsResourceWithStreamingResponse:
    def __init__(self, completions: AsyncCompletionsResource) -> None:
        self._completions = completions

        self.create = async_to_streamed_response_wrapper(
            completions.create,
        )
