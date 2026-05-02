# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Dict, Union, Iterable, cast
from typing_extensions import Literal

import httpx

from ..types import response_create_params
from .._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.response_create_response import ResponseCreateResponse

__all__ = ["ResponsesResource", "AsyncResponsesResource"]


class ResponsesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ResponsesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return ResponsesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ResponsesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return ResponsesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        input: Union[str, Iterable[response_create_params.InputInputItem]],
        model: str,
        include: SequenceNotStr[str] | Omit = omit,
        instructions: str | Omit = omit,
        max_output_tokens: int | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        parallel_tool_calls: bool | Omit = omit,
        previous_response_id: str | Omit = omit,
        reasoning: Dict[str, object] | Omit = omit,
        store: bool | Omit = omit,
        stream: bool | Omit = omit,
        temperature: float | Omit = omit,
        text: Dict[str, object] | Omit = omit,
        tool_choice: Union[str, Dict[str, object]] | Omit = omit,
        tools: Iterable[Dict[str, object]] | Omit = omit,
        top_p: float | Omit = omit,
        truncation: Literal["auto", "disabled"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ResponseCreateResponse:
        """
        Responses

        Args:
          model: model specified as `model_vendor/model`, for example `openai/gpt-4o`

          include: Which fields to include in the response

          instructions: Instructions for the response generation

          max_output_tokens: Maximum number of output tokens

          metadata: Metadata for the response

          parallel_tool_calls: Whether to enable parallel tool calls

          previous_response_id: ID of the previous response for chaining

          reasoning: Reasoning configuration for the response

          store: Whether to store the response

          stream: Whether to stream the response

          temperature: Sampling temperature for randomness control

          text: Text configuration parameters

          tool_choice: Tool choice configuration

          tools: Tools available for the response

          top_p: Top-p sampling parameter

          truncation: Truncation configuration

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return cast(
            ResponseCreateResponse,
            self._post(
                "/v5/responses",
                body=maybe_transform(
                    {
                        "input": input,
                        "model": model,
                        "include": include,
                        "instructions": instructions,
                        "max_output_tokens": max_output_tokens,
                        "metadata": metadata,
                        "parallel_tool_calls": parallel_tool_calls,
                        "previous_response_id": previous_response_id,
                        "reasoning": reasoning,
                        "store": store,
                        "stream": stream,
                        "temperature": temperature,
                        "text": text,
                        "tool_choice": tool_choice,
                        "tools": tools,
                        "top_p": top_p,
                        "truncation": truncation,
                    },
                    response_create_params.ResponseCreateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, ResponseCreateResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class AsyncResponsesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncResponsesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncResponsesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncResponsesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncResponsesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        input: Union[str, Iterable[response_create_params.InputInputItem]],
        model: str,
        include: SequenceNotStr[str] | Omit = omit,
        instructions: str | Omit = omit,
        max_output_tokens: int | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        parallel_tool_calls: bool | Omit = omit,
        previous_response_id: str | Omit = omit,
        reasoning: Dict[str, object] | Omit = omit,
        store: bool | Omit = omit,
        stream: bool | Omit = omit,
        temperature: float | Omit = omit,
        text: Dict[str, object] | Omit = omit,
        tool_choice: Union[str, Dict[str, object]] | Omit = omit,
        tools: Iterable[Dict[str, object]] | Omit = omit,
        top_p: float | Omit = omit,
        truncation: Literal["auto", "disabled"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ResponseCreateResponse:
        """
        Responses

        Args:
          model: model specified as `model_vendor/model`, for example `openai/gpt-4o`

          include: Which fields to include in the response

          instructions: Instructions for the response generation

          max_output_tokens: Maximum number of output tokens

          metadata: Metadata for the response

          parallel_tool_calls: Whether to enable parallel tool calls

          previous_response_id: ID of the previous response for chaining

          reasoning: Reasoning configuration for the response

          store: Whether to store the response

          stream: Whether to stream the response

          temperature: Sampling temperature for randomness control

          text: Text configuration parameters

          tool_choice: Tool choice configuration

          tools: Tools available for the response

          top_p: Top-p sampling parameter

          truncation: Truncation configuration

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return cast(
            ResponseCreateResponse,
            await self._post(
                "/v5/responses",
                body=await async_maybe_transform(
                    {
                        "input": input,
                        "model": model,
                        "include": include,
                        "instructions": instructions,
                        "max_output_tokens": max_output_tokens,
                        "metadata": metadata,
                        "parallel_tool_calls": parallel_tool_calls,
                        "previous_response_id": previous_response_id,
                        "reasoning": reasoning,
                        "store": store,
                        "stream": stream,
                        "temperature": temperature,
                        "text": text,
                        "tool_choice": tool_choice,
                        "tools": tools,
                        "top_p": top_p,
                        "truncation": truncation,
                    },
                    response_create_params.ResponseCreateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, ResponseCreateResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class ResponsesResourceWithRawResponse:
    def __init__(self, responses: ResponsesResource) -> None:
        self._responses = responses

        self.create = to_raw_response_wrapper(
            responses.create,
        )


class AsyncResponsesResourceWithRawResponse:
    def __init__(self, responses: AsyncResponsesResource) -> None:
        self._responses = responses

        self.create = async_to_raw_response_wrapper(
            responses.create,
        )


class ResponsesResourceWithStreamingResponse:
    def __init__(self, responses: ResponsesResource) -> None:
        self._responses = responses

        self.create = to_streamed_response_wrapper(
            responses.create,
        )


class AsyncResponsesResourceWithStreamingResponse:
    def __init__(self, responses: AsyncResponsesResource) -> None:
        self._responses = responses

        self.create = async_to_streamed_response_wrapper(
            responses.create,
        )
