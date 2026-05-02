# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ...._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.scalar_data import ScalarData
from ....types.applications.metrics import scalar_retrieve_params

__all__ = ["ScalarResource", "AsyncScalarResource"]


class ScalarResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ScalarResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return ScalarResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ScalarResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return ScalarResourceWithStreamingResponse(self)

    def retrieve(
        self,
        metric_id: Literal[
            "total_requests",
            "total_errors",
            "total_tokens",
            "average_latency",
            "p95_latency",
            "error_rate",
            "average_users",
            "aggregated_tokens",
            "feedback",
            "execution_input_response_tokens",
            "execution_average_latency_per_variant",
            "execution_error_rate",
            "execution_latency_percentile",
            "execution_average_latency_per_node",
        ],
        *,
        application_spec_id: str,
        account_id: str | Omit = omit,
        from_ts: int | Omit = omit,
        to_ts: int | Omit = omit,
        variants: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ScalarData:
        """
        Get Scalar Metric

        Args:
          account_id: Account ID used for authorization

          from_ts: The starting (oldest) timestamp window in seconds.

          to_ts: The ending (most recent) timestamp in seconds.

          variants: Which variants to filter on

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_spec_id:
            raise ValueError(
                f"Expected a non-empty value for `application_spec_id` but received {application_spec_id!r}"
            )
        if not metric_id:
            raise ValueError(f"Expected a non-empty value for `metric_id` but received {metric_id!r}")
        return self._get(
            f"/v4/applications/{application_spec_id}/metrics/scalar/{metric_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "from_ts": from_ts,
                        "to_ts": to_ts,
                        "variants": variants,
                    },
                    scalar_retrieve_params.ScalarRetrieveParams,
                ),
            ),
            cast_to=ScalarData,
        )


class AsyncScalarResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncScalarResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncScalarResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncScalarResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncScalarResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        metric_id: Literal[
            "total_requests",
            "total_errors",
            "total_tokens",
            "average_latency",
            "p95_latency",
            "error_rate",
            "average_users",
            "aggregated_tokens",
            "feedback",
            "execution_input_response_tokens",
            "execution_average_latency_per_variant",
            "execution_error_rate",
            "execution_latency_percentile",
            "execution_average_latency_per_node",
        ],
        *,
        application_spec_id: str,
        account_id: str | Omit = omit,
        from_ts: int | Omit = omit,
        to_ts: int | Omit = omit,
        variants: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ScalarData:
        """
        Get Scalar Metric

        Args:
          account_id: Account ID used for authorization

          from_ts: The starting (oldest) timestamp window in seconds.

          to_ts: The ending (most recent) timestamp in seconds.

          variants: Which variants to filter on

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_spec_id:
            raise ValueError(
                f"Expected a non-empty value for `application_spec_id` but received {application_spec_id!r}"
            )
        if not metric_id:
            raise ValueError(f"Expected a non-empty value for `metric_id` but received {metric_id!r}")
        return await self._get(
            f"/v4/applications/{application_spec_id}/metrics/scalar/{metric_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "account_id": account_id,
                        "from_ts": from_ts,
                        "to_ts": to_ts,
                        "variants": variants,
                    },
                    scalar_retrieve_params.ScalarRetrieveParams,
                ),
            ),
            cast_to=ScalarData,
        )


class ScalarResourceWithRawResponse:
    def __init__(self, scalar: ScalarResource) -> None:
        self._scalar = scalar

        self.retrieve = to_raw_response_wrapper(
            scalar.retrieve,
        )


class AsyncScalarResourceWithRawResponse:
    def __init__(self, scalar: AsyncScalarResource) -> None:
        self._scalar = scalar

        self.retrieve = async_to_raw_response_wrapper(
            scalar.retrieve,
        )


class ScalarResourceWithStreamingResponse:
    def __init__(self, scalar: ScalarResource) -> None:
        self._scalar = scalar

        self.retrieve = to_streamed_response_wrapper(
            scalar.retrieve,
        )


class AsyncScalarResourceWithStreamingResponse:
    def __init__(self, scalar: AsyncScalarResource) -> None:
        self._scalar = scalar

        self.retrieve = async_to_streamed_response_wrapper(
            scalar.retrieve,
        )
