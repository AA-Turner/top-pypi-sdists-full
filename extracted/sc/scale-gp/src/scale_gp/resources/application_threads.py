# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable

import httpx

from ..types import application_thread_process_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import path_template, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options

__all__ = ["ApplicationThreadsResource", "AsyncApplicationThreadsResource"]


class ApplicationThreadsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ApplicationThreadsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return ApplicationThreadsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ApplicationThreadsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return ApplicationThreadsResourceWithStreamingResponse(self)

    def process(
        self,
        thread_id: str,
        *,
        application_variant_id: str,
        inputs: Dict[str, object],
        history: Iterable[application_thread_process_params.History] | Omit = omit,
        operation_metadata: Dict[str, object] | Omit = omit,
        overrides: application_thread_process_params.Overrides | Omit = omit,
        stream: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Process Deployed Application For Thread

        Args:
          inputs: Input data for the application. For agents service variants, you must provide
              inputs as a mapping from `{input_name: input_value}`. For V0 variants, you must
              specify the node your input should be passed to, structuring your input as
              `{node_id: {input_name: input_value}}`.

          history: History of the application

          operation_metadata: Arbitrary user-defined metadata that can be attached to the process operations
              and will be registered in the interaction.

          overrides: Optional overrides for the application

          stream: Control to have streaming of the endpoint. If the last node before the output is
              a completion node, you can set this to true to get the output as soon as the
              completion node has a token

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_variant_id:
            raise ValueError(
                f"Expected a non-empty value for `application_variant_id` but received {application_variant_id!r}"
            )
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        return self._post(
            path_template(
                "/v4/applications/{application_variant_id}/threads/{thread_id}/process",
                application_variant_id=application_variant_id,
                thread_id=thread_id,
            ),
            body=maybe_transform(
                {
                    "inputs": inputs,
                    "history": history,
                    "operation_metadata": operation_metadata,
                    "overrides": overrides,
                    "stream": stream,
                },
                application_thread_process_params.ApplicationThreadProcessParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncApplicationThreadsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncApplicationThreadsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncApplicationThreadsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncApplicationThreadsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncApplicationThreadsResourceWithStreamingResponse(self)

    async def process(
        self,
        thread_id: str,
        *,
        application_variant_id: str,
        inputs: Dict[str, object],
        history: Iterable[application_thread_process_params.History] | Omit = omit,
        operation_metadata: Dict[str, object] | Omit = omit,
        overrides: application_thread_process_params.Overrides | Omit = omit,
        stream: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Process Deployed Application For Thread

        Args:
          inputs: Input data for the application. For agents service variants, you must provide
              inputs as a mapping from `{input_name: input_value}`. For V0 variants, you must
              specify the node your input should be passed to, structuring your input as
              `{node_id: {input_name: input_value}}`.

          history: History of the application

          operation_metadata: Arbitrary user-defined metadata that can be attached to the process operations
              and will be registered in the interaction.

          overrides: Optional overrides for the application

          stream: Control to have streaming of the endpoint. If the last node before the output is
              a completion node, you can set this to true to get the output as soon as the
              completion node has a token

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_variant_id:
            raise ValueError(
                f"Expected a non-empty value for `application_variant_id` but received {application_variant_id!r}"
            )
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        return await self._post(
            path_template(
                "/v4/applications/{application_variant_id}/threads/{thread_id}/process",
                application_variant_id=application_variant_id,
                thread_id=thread_id,
            ),
            body=await async_maybe_transform(
                {
                    "inputs": inputs,
                    "history": history,
                    "operation_metadata": operation_metadata,
                    "overrides": overrides,
                    "stream": stream,
                },
                application_thread_process_params.ApplicationThreadProcessParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class ApplicationThreadsResourceWithRawResponse:
    def __init__(self, application_threads: ApplicationThreadsResource) -> None:
        self._application_threads = application_threads

        self.process = to_raw_response_wrapper(
            application_threads.process,
        )


class AsyncApplicationThreadsResourceWithRawResponse:
    def __init__(self, application_threads: AsyncApplicationThreadsResource) -> None:
        self._application_threads = application_threads

        self.process = async_to_raw_response_wrapper(
            application_threads.process,
        )


class ApplicationThreadsResourceWithStreamingResponse:
    def __init__(self, application_threads: ApplicationThreadsResource) -> None:
        self._application_threads = application_threads

        self.process = to_streamed_response_wrapper(
            application_threads.process,
        )


class AsyncApplicationThreadsResourceWithStreamingResponse:
    def __init__(self, application_threads: AsyncApplicationThreadsResource) -> None:
        self._application_threads = application_threads

        self.process = async_to_streamed_response_wrapper(
            application_threads.process,
        )
