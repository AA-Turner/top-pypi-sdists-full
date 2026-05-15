# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._utils import path_template
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.evaluation_metrics import EvaluationMetrics

__all__ = ["EvaluationMetricsResource", "AsyncEvaluationMetricsResource"]


class EvaluationMetricsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EvaluationMetricsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return EvaluationMetricsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EvaluationMetricsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return EvaluationMetricsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        evaluation_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationMetrics:
        """
        Get Evaluation Metrics

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return self._get(
            path_template("/v4/evaluations/{evaluation_id}/evaluation-metrics", evaluation_id=evaluation_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationMetrics,
        )


class AsyncEvaluationMetricsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEvaluationMetricsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEvaluationMetricsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEvaluationMetricsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncEvaluationMetricsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        evaluation_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationMetrics:
        """
        Get Evaluation Metrics

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return await self._get(
            path_template("/v4/evaluations/{evaluation_id}/evaluation-metrics", evaluation_id=evaluation_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationMetrics,
        )


class EvaluationMetricsResourceWithRawResponse:
    def __init__(self, evaluation_metrics: EvaluationMetricsResource) -> None:
        self._evaluation_metrics = evaluation_metrics

        self.retrieve = to_raw_response_wrapper(
            evaluation_metrics.retrieve,
        )


class AsyncEvaluationMetricsResourceWithRawResponse:
    def __init__(self, evaluation_metrics: AsyncEvaluationMetricsResource) -> None:
        self._evaluation_metrics = evaluation_metrics

        self.retrieve = async_to_raw_response_wrapper(
            evaluation_metrics.retrieve,
        )


class EvaluationMetricsResourceWithStreamingResponse:
    def __init__(self, evaluation_metrics: EvaluationMetricsResource) -> None:
        self._evaluation_metrics = evaluation_metrics

        self.retrieve = to_streamed_response_wrapper(
            evaluation_metrics.retrieve,
        )


class AsyncEvaluationMetricsResourceWithStreamingResponse:
    def __init__(self, evaluation_metrics: AsyncEvaluationMetricsResource) -> None:
        self._evaluation_metrics = evaluation_metrics

        self.retrieve = async_to_streamed_response_wrapper(
            evaluation_metrics.retrieve,
        )
