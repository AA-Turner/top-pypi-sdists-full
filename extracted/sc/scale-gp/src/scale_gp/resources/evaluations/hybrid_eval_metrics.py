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
from ...types.hybrid_evaluation_metrics import HybridEvaluationMetrics

__all__ = ["HybridEvalMetricsResource", "AsyncHybridEvalMetricsResource"]


class HybridEvalMetricsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> HybridEvalMetricsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return HybridEvalMetricsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> HybridEvalMetricsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return HybridEvalMetricsResourceWithStreamingResponse(self)

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
    ) -> HybridEvaluationMetrics:
        """
        Get Hybrid Evaluation Metrics

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return self._get(
            path_template("/v4/evaluations/{evaluation_id}/hybrid-eval-metrics", evaluation_id=evaluation_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=HybridEvaluationMetrics,
        )


class AsyncHybridEvalMetricsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncHybridEvalMetricsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncHybridEvalMetricsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncHybridEvalMetricsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncHybridEvalMetricsResourceWithStreamingResponse(self)

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
    ) -> HybridEvaluationMetrics:
        """
        Get Hybrid Evaluation Metrics

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return await self._get(
            path_template("/v4/evaluations/{evaluation_id}/hybrid-eval-metrics", evaluation_id=evaluation_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=HybridEvaluationMetrics,
        )


class HybridEvalMetricsResourceWithRawResponse:
    def __init__(self, hybrid_eval_metrics: HybridEvalMetricsResource) -> None:
        self._hybrid_eval_metrics = hybrid_eval_metrics

        self.retrieve = to_raw_response_wrapper(
            hybrid_eval_metrics.retrieve,
        )


class AsyncHybridEvalMetricsResourceWithRawResponse:
    def __init__(self, hybrid_eval_metrics: AsyncHybridEvalMetricsResource) -> None:
        self._hybrid_eval_metrics = hybrid_eval_metrics

        self.retrieve = async_to_raw_response_wrapper(
            hybrid_eval_metrics.retrieve,
        )


class HybridEvalMetricsResourceWithStreamingResponse:
    def __init__(self, hybrid_eval_metrics: HybridEvalMetricsResource) -> None:
        self._hybrid_eval_metrics = hybrid_eval_metrics

        self.retrieve = to_streamed_response_wrapper(
            hybrid_eval_metrics.retrieve,
        )


class AsyncHybridEvalMetricsResourceWithStreamingResponse:
    def __init__(self, hybrid_eval_metrics: AsyncHybridEvalMetricsResource) -> None:
        self._hybrid_eval_metrics = hybrid_eval_metrics

        self.retrieve = async_to_streamed_response_wrapper(
            hybrid_eval_metrics.retrieve,
        )
