# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal

import httpx

from ..types import (
    trace_insight_list_params,
    trace_insight_list_jobs_params,
    trace_insight_create_job_params,
    trace_insight_search_span_analysis_params,
    trace_insight_search_trace_insights_params,
    trace_insight_get_error_aggregations_params,
)
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
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
from ..types.trace_insight_list_response import TraceInsightListResponse
from ..types.trace_insight_list_jobs_response import TraceInsightListJobsResponse
from ..types.trace_insight_create_job_response import TraceInsightCreateJobResponse
from ..types.trace_insight_search_span_analysis_response import TraceInsightSearchSpanAnalysisResponse
from ..types.trace_insight_search_trace_insights_response import TraceInsightSearchTraceInsightsResponse
from ..types.trace_insight_get_error_aggregations_response import TraceInsightGetErrorAggregationsResponse

__all__ = ["TraceInsightResource", "AsyncTraceInsightResource"]


class TraceInsightResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TraceInsightResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/patronus-ai/patronus-api-python#accessing-raw-response-data-eg-headers
        """
        return TraceInsightResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TraceInsightResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/patronus-ai/patronus-api-python#with_streaming_response
        """
        return TraceInsightResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        app: Optional[str] | NotGiven = NOT_GIVEN,
        experiment_id: Optional[str] | NotGiven = NOT_GIVEN,
        job_id: Optional[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        trace_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TraceInsightListResponse:
        """
        List Insights

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v1/trace-insight",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "app": app,
                        "experiment_id": experiment_id,
                        "job_id": job_id,
                        "limit": limit,
                        "offset": offset,
                        "project_id": project_id,
                        "trace_id": trace_id,
                    },
                    trace_insight_list_params.TraceInsightListParams,
                ),
            ),
            cast_to=TraceInsightListResponse,
        )

    def create_job(
        self,
        *,
        trace_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TraceInsightCreateJobResponse:
        """
        Create Insight Job

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/trace-insight-jobs",
            body=maybe_transform({"trace_id": trace_id}, trace_insight_create_job_params.TraceInsightCreateJobParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TraceInsightCreateJobResponse,
        )

    def get_error_aggregations(
        self,
        *,
        app: Optional[str] | NotGiven = NOT_GIVEN,
        end_time: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        error_types: Optional[List[str]] | NotGiven = NOT_GIVEN,
        experiment_id: Optional[int] | NotGiven = NOT_GIVEN,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        start_time: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TraceInsightGetErrorAggregationsResponse:
        """
        Get Trace Insight Error Aggregations

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/trace-insight/errors",
            body=maybe_transform(
                {
                    "app": app,
                    "end_time": end_time,
                    "error_types": error_types,
                    "experiment_id": experiment_id,
                    "project_id": project_id,
                    "start_time": start_time,
                },
                trace_insight_get_error_aggregations_params.TraceInsightGetErrorAggregationsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TraceInsightGetErrorAggregationsResponse,
        )

    def list_jobs(
        self,
        *,
        app: Optional[str] | NotGiven = NOT_GIVEN,
        experiment_id: Optional[str] | NotGiven = NOT_GIVEN,
        job_id: Optional[str] | NotGiven = NOT_GIVEN,
        job_status: Optional[Literal["pending", "success", "failed", "cancelled"]] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        trace_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TraceInsightListJobsResponse:
        """
        List Insight Jobs

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v1/trace-insight-jobs",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "app": app,
                        "experiment_id": experiment_id,
                        "job_id": job_id,
                        "job_status": job_status,
                        "limit": limit,
                        "offset": offset,
                        "project_id": project_id,
                        "trace_id": trace_id,
                    },
                    trace_insight_list_jobs_params.TraceInsightListJobsParams,
                ),
            ),
            cast_to=TraceInsightListJobsResponse,
        )

    def search_span_analysis(
        self,
        *,
        end_time: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        span_id: Optional[str] | NotGiven = NOT_GIVEN,
        start_time: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        trace_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TraceInsightSearchSpanAnalysisResponse:
        """
        Search Span Analysis

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/span-analysis/search",
            body=maybe_transform(
                {
                    "end_time": end_time,
                    "limit": limit,
                    "offset": offset,
                    "span_id": span_id,
                    "start_time": start_time,
                    "trace_id": trace_id,
                },
                trace_insight_search_span_analysis_params.TraceInsightSearchSpanAnalysisParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TraceInsightSearchSpanAnalysisResponse,
        )

    def search_trace_insights(
        self,
        *,
        app: Optional[str] | NotGiven = NOT_GIVEN,
        end_time: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        error_types: Optional[List[str]] | NotGiven = NOT_GIVEN,
        experiment_id: Optional[int] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        redis_job_id: Optional[str] | NotGiven = NOT_GIVEN,
        start_time: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        trace_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TraceInsightSearchTraceInsightsResponse:
        """
        Search Trace Insights

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/trace-insight/search",
            body=maybe_transform(
                {
                    "app": app,
                    "end_time": end_time,
                    "error_types": error_types,
                    "experiment_id": experiment_id,
                    "limit": limit,
                    "offset": offset,
                    "project_id": project_id,
                    "redis_job_id": redis_job_id,
                    "start_time": start_time,
                    "trace_id": trace_id,
                },
                trace_insight_search_trace_insights_params.TraceInsightSearchTraceInsightsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TraceInsightSearchTraceInsightsResponse,
        )


class AsyncTraceInsightResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTraceInsightResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/patronus-ai/patronus-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTraceInsightResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTraceInsightResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/patronus-ai/patronus-api-python#with_streaming_response
        """
        return AsyncTraceInsightResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        app: Optional[str] | NotGiven = NOT_GIVEN,
        experiment_id: Optional[str] | NotGiven = NOT_GIVEN,
        job_id: Optional[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        trace_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TraceInsightListResponse:
        """
        List Insights

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v1/trace-insight",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "app": app,
                        "experiment_id": experiment_id,
                        "job_id": job_id,
                        "limit": limit,
                        "offset": offset,
                        "project_id": project_id,
                        "trace_id": trace_id,
                    },
                    trace_insight_list_params.TraceInsightListParams,
                ),
            ),
            cast_to=TraceInsightListResponse,
        )

    async def create_job(
        self,
        *,
        trace_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TraceInsightCreateJobResponse:
        """
        Create Insight Job

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/trace-insight-jobs",
            body=await async_maybe_transform(
                {"trace_id": trace_id}, trace_insight_create_job_params.TraceInsightCreateJobParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TraceInsightCreateJobResponse,
        )

    async def get_error_aggregations(
        self,
        *,
        app: Optional[str] | NotGiven = NOT_GIVEN,
        end_time: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        error_types: Optional[List[str]] | NotGiven = NOT_GIVEN,
        experiment_id: Optional[int] | NotGiven = NOT_GIVEN,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        start_time: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TraceInsightGetErrorAggregationsResponse:
        """
        Get Trace Insight Error Aggregations

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/trace-insight/errors",
            body=await async_maybe_transform(
                {
                    "app": app,
                    "end_time": end_time,
                    "error_types": error_types,
                    "experiment_id": experiment_id,
                    "project_id": project_id,
                    "start_time": start_time,
                },
                trace_insight_get_error_aggregations_params.TraceInsightGetErrorAggregationsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TraceInsightGetErrorAggregationsResponse,
        )

    async def list_jobs(
        self,
        *,
        app: Optional[str] | NotGiven = NOT_GIVEN,
        experiment_id: Optional[str] | NotGiven = NOT_GIVEN,
        job_id: Optional[str] | NotGiven = NOT_GIVEN,
        job_status: Optional[Literal["pending", "success", "failed", "cancelled"]] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        trace_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TraceInsightListJobsResponse:
        """
        List Insight Jobs

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v1/trace-insight-jobs",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "app": app,
                        "experiment_id": experiment_id,
                        "job_id": job_id,
                        "job_status": job_status,
                        "limit": limit,
                        "offset": offset,
                        "project_id": project_id,
                        "trace_id": trace_id,
                    },
                    trace_insight_list_jobs_params.TraceInsightListJobsParams,
                ),
            ),
            cast_to=TraceInsightListJobsResponse,
        )

    async def search_span_analysis(
        self,
        *,
        end_time: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        span_id: Optional[str] | NotGiven = NOT_GIVEN,
        start_time: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        trace_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TraceInsightSearchSpanAnalysisResponse:
        """
        Search Span Analysis

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/span-analysis/search",
            body=await async_maybe_transform(
                {
                    "end_time": end_time,
                    "limit": limit,
                    "offset": offset,
                    "span_id": span_id,
                    "start_time": start_time,
                    "trace_id": trace_id,
                },
                trace_insight_search_span_analysis_params.TraceInsightSearchSpanAnalysisParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TraceInsightSearchSpanAnalysisResponse,
        )

    async def search_trace_insights(
        self,
        *,
        app: Optional[str] | NotGiven = NOT_GIVEN,
        end_time: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        error_types: Optional[List[str]] | NotGiven = NOT_GIVEN,
        experiment_id: Optional[int] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        redis_job_id: Optional[str] | NotGiven = NOT_GIVEN,
        start_time: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        trace_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TraceInsightSearchTraceInsightsResponse:
        """
        Search Trace Insights

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/trace-insight/search",
            body=await async_maybe_transform(
                {
                    "app": app,
                    "end_time": end_time,
                    "error_types": error_types,
                    "experiment_id": experiment_id,
                    "limit": limit,
                    "offset": offset,
                    "project_id": project_id,
                    "redis_job_id": redis_job_id,
                    "start_time": start_time,
                    "trace_id": trace_id,
                },
                trace_insight_search_trace_insights_params.TraceInsightSearchTraceInsightsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TraceInsightSearchTraceInsightsResponse,
        )


class TraceInsightResourceWithRawResponse:
    def __init__(self, trace_insight: TraceInsightResource) -> None:
        self._trace_insight = trace_insight

        self.list = to_raw_response_wrapper(
            trace_insight.list,
        )
        self.create_job = to_raw_response_wrapper(
            trace_insight.create_job,
        )
        self.get_error_aggregations = to_raw_response_wrapper(
            trace_insight.get_error_aggregations,
        )
        self.list_jobs = to_raw_response_wrapper(
            trace_insight.list_jobs,
        )
        self.search_span_analysis = to_raw_response_wrapper(
            trace_insight.search_span_analysis,
        )
        self.search_trace_insights = to_raw_response_wrapper(
            trace_insight.search_trace_insights,
        )


class AsyncTraceInsightResourceWithRawResponse:
    def __init__(self, trace_insight: AsyncTraceInsightResource) -> None:
        self._trace_insight = trace_insight

        self.list = async_to_raw_response_wrapper(
            trace_insight.list,
        )
        self.create_job = async_to_raw_response_wrapper(
            trace_insight.create_job,
        )
        self.get_error_aggregations = async_to_raw_response_wrapper(
            trace_insight.get_error_aggregations,
        )
        self.list_jobs = async_to_raw_response_wrapper(
            trace_insight.list_jobs,
        )
        self.search_span_analysis = async_to_raw_response_wrapper(
            trace_insight.search_span_analysis,
        )
        self.search_trace_insights = async_to_raw_response_wrapper(
            trace_insight.search_trace_insights,
        )


class TraceInsightResourceWithStreamingResponse:
    def __init__(self, trace_insight: TraceInsightResource) -> None:
        self._trace_insight = trace_insight

        self.list = to_streamed_response_wrapper(
            trace_insight.list,
        )
        self.create_job = to_streamed_response_wrapper(
            trace_insight.create_job,
        )
        self.get_error_aggregations = to_streamed_response_wrapper(
            trace_insight.get_error_aggregations,
        )
        self.list_jobs = to_streamed_response_wrapper(
            trace_insight.list_jobs,
        )
        self.search_span_analysis = to_streamed_response_wrapper(
            trace_insight.search_span_analysis,
        )
        self.search_trace_insights = to_streamed_response_wrapper(
            trace_insight.search_trace_insights,
        )


class AsyncTraceInsightResourceWithStreamingResponse:
    def __init__(self, trace_insight: AsyncTraceInsightResource) -> None:
        self._trace_insight = trace_insight

        self.list = async_to_streamed_response_wrapper(
            trace_insight.list,
        )
        self.create_job = async_to_streamed_response_wrapper(
            trace_insight.create_job,
        )
        self.get_error_aggregations = async_to_streamed_response_wrapper(
            trace_insight.get_error_aggregations,
        )
        self.list_jobs = async_to_streamed_response_wrapper(
            trace_insight.list_jobs,
        )
        self.search_span_analysis = async_to_streamed_response_wrapper(
            trace_insight.search_span_analysis,
        )
        self.search_trace_insights = async_to_streamed_response_wrapper(
            trace_insight.search_trace_insights,
        )
