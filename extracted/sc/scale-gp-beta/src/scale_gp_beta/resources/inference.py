# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Dict, cast

import httpx

from ..types import inference_create_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
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
from ..types.inference_create_response import InferenceCreateResponse
from ..types.launch_inference_configuration_param import LaunchInferenceConfigurationParam

__all__ = ["InferenceResource", "AsyncInferenceResource"]


class InferenceResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> InferenceResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return InferenceResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> InferenceResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return InferenceResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        model: str,
        args: Dict[str, object] | Omit = omit,
        inference_configuration: LaunchInferenceConfigurationParam | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InferenceCreateResponse:
        """
        Runs a model using a free-form, vendor-native request payload rather than a
        fixed OpenAI schema.

        Use this endpoint when the target model does not fit the OpenAI chat, responses,
        or text-completion contracts: the `args` field is an arbitrary dict passed
        straight through to the selected vendor gateway, and the reply is returned
        inside `response` as arbitrary JSON (object, array, string, number, or boolean).
        Prefer /v5/chat/completions, /v5/responses, or /v5/completions when your request
        matches one of those OpenAI-standard shapes, since those return typed OpenAI
        response objects. The model is chosen from the `model` field formatted as
        `vendor/name`, which selects the per-vendor inference gateway. When the request
        enables streaming, the response is sent as server-sent events with each chunk
        wrapped as a `generic_inference.chunk` object; otherwise a single
        `generic_inference` object is returned.

        Args:
          model: model specified as `vendor/name` (ex. openai/gpt-5)

          args: Arguments passed into model

          inference_configuration: Vendor specific configuration

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return cast(
            InferenceCreateResponse,
            self._post(
                "/v5/inference",
                body=maybe_transform(
                    {
                        "model": model,
                        "args": args,
                        "inference_configuration": inference_configuration,
                    },
                    inference_create_params.InferenceCreateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, InferenceCreateResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class AsyncInferenceResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncInferenceResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncInferenceResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncInferenceResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncInferenceResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        model: str,
        args: Dict[str, object] | Omit = omit,
        inference_configuration: LaunchInferenceConfigurationParam | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InferenceCreateResponse:
        """
        Runs a model using a free-form, vendor-native request payload rather than a
        fixed OpenAI schema.

        Use this endpoint when the target model does not fit the OpenAI chat, responses,
        or text-completion contracts: the `args` field is an arbitrary dict passed
        straight through to the selected vendor gateway, and the reply is returned
        inside `response` as arbitrary JSON (object, array, string, number, or boolean).
        Prefer /v5/chat/completions, /v5/responses, or /v5/completions when your request
        matches one of those OpenAI-standard shapes, since those return typed OpenAI
        response objects. The model is chosen from the `model` field formatted as
        `vendor/name`, which selects the per-vendor inference gateway. When the request
        enables streaming, the response is sent as server-sent events with each chunk
        wrapped as a `generic_inference.chunk` object; otherwise a single
        `generic_inference` object is returned.

        Args:
          model: model specified as `vendor/name` (ex. openai/gpt-5)

          args: Arguments passed into model

          inference_configuration: Vendor specific configuration

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return cast(
            InferenceCreateResponse,
            await self._post(
                "/v5/inference",
                body=await async_maybe_transform(
                    {
                        "model": model,
                        "args": args,
                        "inference_configuration": inference_configuration,
                    },
                    inference_create_params.InferenceCreateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, InferenceCreateResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class InferenceResourceWithRawResponse:
    def __init__(self, inference: InferenceResource) -> None:
        self._inference = inference

        self.create = to_raw_response_wrapper(
            inference.create,
        )


class AsyncInferenceResourceWithRawResponse:
    def __init__(self, inference: AsyncInferenceResource) -> None:
        self._inference = inference

        self.create = async_to_raw_response_wrapper(
            inference.create,
        )


class InferenceResourceWithStreamingResponse:
    def __init__(self, inference: InferenceResource) -> None:
        self._inference = inference

        self.create = to_streamed_response_wrapper(
            inference.create,
        )


class AsyncInferenceResourceWithStreamingResponse:
    def __init__(self, inference: AsyncInferenceResource) -> None:
        self._inference = inference

        self.create = async_to_streamed_response_wrapper(
            inference.create,
        )
