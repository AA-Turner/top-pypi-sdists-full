# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from datetime import datetime
from typing_extensions import Literal

import httpx

from ..types import interaction_create_params
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
from ..types.interaction_create_response import InteractionCreateResponse

__all__ = ["InteractionsResource", "AsyncInteractionsResource"]


class InteractionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> InteractionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return InteractionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> InteractionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return InteractionsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        application_variant_id: str,
        input: interaction_create_params.Input,
        output: interaction_create_params.Output,
        start_timestamp: Union[str, datetime],
        duration_ms: int | Omit = omit,
        operation_metadata: Dict[str, object] | Omit = omit,
        operation_status: Literal["SUCCESS", "ERROR"] | Omit = omit,
        thread_id: str | Omit = omit,
        trace_spans: Iterable[interaction_create_params.TraceSpan] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InteractionCreateResponse:
        """
        Create Application Interaction

        Args:
          application_variant_id: Identifier for the application variant that performed this interaction.

          input: The input data for the interaction.

          output: The output data from the interaction.

          start_timestamp: Timestamp marking the start of the interaction.

          duration_ms: Duration of the interaction in milliseconds.

          operation_metadata: Optional metadata related to the operation, including custom or predefined keys.

          operation_status: The outcome status of the interaction.

          thread_id: Optional UUID identifying the conversation thread associated with the
              interaction.The interaction will be associated with the thread if the id
              represents an existing thread.If the thread with the specified id is not found,
              a new thread will be created.

          trace_spans: List of trace spans associated with the interaction.These spans provide insight
              into the individual steps taken by nodes involved in generating the output.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v4/interactions/",
            body=maybe_transform(
                {
                    "application_variant_id": application_variant_id,
                    "input": input,
                    "output": output,
                    "start_timestamp": start_timestamp,
                    "duration_ms": duration_ms,
                    "operation_metadata": operation_metadata,
                    "operation_status": operation_status,
                    "thread_id": thread_id,
                    "trace_spans": trace_spans,
                },
                interaction_create_params.InteractionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InteractionCreateResponse,
        )


class AsyncInteractionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncInteractionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncInteractionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncInteractionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncInteractionsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        application_variant_id: str,
        input: interaction_create_params.Input,
        output: interaction_create_params.Output,
        start_timestamp: Union[str, datetime],
        duration_ms: int | Omit = omit,
        operation_metadata: Dict[str, object] | Omit = omit,
        operation_status: Literal["SUCCESS", "ERROR"] | Omit = omit,
        thread_id: str | Omit = omit,
        trace_spans: Iterable[interaction_create_params.TraceSpan] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InteractionCreateResponse:
        """
        Create Application Interaction

        Args:
          application_variant_id: Identifier for the application variant that performed this interaction.

          input: The input data for the interaction.

          output: The output data from the interaction.

          start_timestamp: Timestamp marking the start of the interaction.

          duration_ms: Duration of the interaction in milliseconds.

          operation_metadata: Optional metadata related to the operation, including custom or predefined keys.

          operation_status: The outcome status of the interaction.

          thread_id: Optional UUID identifying the conversation thread associated with the
              interaction.The interaction will be associated with the thread if the id
              represents an existing thread.If the thread with the specified id is not found,
              a new thread will be created.

          trace_spans: List of trace spans associated with the interaction.These spans provide insight
              into the individual steps taken by nodes involved in generating the output.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v4/interactions/",
            body=await async_maybe_transform(
                {
                    "application_variant_id": application_variant_id,
                    "input": input,
                    "output": output,
                    "start_timestamp": start_timestamp,
                    "duration_ms": duration_ms,
                    "operation_metadata": operation_metadata,
                    "operation_status": operation_status,
                    "thread_id": thread_id,
                    "trace_spans": trace_spans,
                },
                interaction_create_params.InteractionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InteractionCreateResponse,
        )


class InteractionsResourceWithRawResponse:
    def __init__(self, interactions: InteractionsResource) -> None:
        self._interactions = interactions

        self.create = to_raw_response_wrapper(
            interactions.create,
        )


class AsyncInteractionsResourceWithRawResponse:
    def __init__(self, interactions: AsyncInteractionsResource) -> None:
        self._interactions = interactions

        self.create = async_to_raw_response_wrapper(
            interactions.create,
        )


class InteractionsResourceWithStreamingResponse:
    def __init__(self, interactions: InteractionsResource) -> None:
        self._interactions = interactions

        self.create = to_streamed_response_wrapper(
            interactions.create,
        )


class AsyncInteractionsResourceWithStreamingResponse:
    def __init__(self, interactions: AsyncInteractionsResource) -> None:
        self._interactions = interactions

        self.create = async_to_streamed_response_wrapper(
            interactions.create,
        )
