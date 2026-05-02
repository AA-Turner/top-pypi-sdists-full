# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from patronus_api import PatronusAPI, AsyncPatronusAPI
from patronus_api.types import (
    TraceInsightListResponse,
    TraceInsightListJobsResponse,
    TraceInsightCreateJobResponse,
    TraceInsightSearchSpanAnalysisResponse,
    TraceInsightSearchTraceInsightsResponse,
    TraceInsightGetErrorAggregationsResponse,
)
from patronus_api._utils import parse_datetime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTraceInsight:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: PatronusAPI) -> None:
        trace_insight = client.trace_insight.list()
        assert_matches_type(TraceInsightListResponse, trace_insight, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: PatronusAPI) -> None:
        trace_insight = client.trace_insight.list(
            app="app",
            experiment_id="experiment_id",
            job_id="job_id",
            limit=1,
            offset=0,
            project_id="project_id",
            trace_id="trace_id",
        )
        assert_matches_type(TraceInsightListResponse, trace_insight, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: PatronusAPI) -> None:
        response = client.trace_insight.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trace_insight = response.parse()
        assert_matches_type(TraceInsightListResponse, trace_insight, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: PatronusAPI) -> None:
        with client.trace_insight.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trace_insight = response.parse()
            assert_matches_type(TraceInsightListResponse, trace_insight, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_create_job(self, client: PatronusAPI) -> None:
        trace_insight = client.trace_insight.create_job(
            trace_id="trace_id",
        )
        assert_matches_type(TraceInsightCreateJobResponse, trace_insight, path=["response"])

    @parametrize
    def test_raw_response_create_job(self, client: PatronusAPI) -> None:
        response = client.trace_insight.with_raw_response.create_job(
            trace_id="trace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trace_insight = response.parse()
        assert_matches_type(TraceInsightCreateJobResponse, trace_insight, path=["response"])

    @parametrize
    def test_streaming_response_create_job(self, client: PatronusAPI) -> None:
        with client.trace_insight.with_streaming_response.create_job(
            trace_id="trace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trace_insight = response.parse()
            assert_matches_type(TraceInsightCreateJobResponse, trace_insight, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_get_error_aggregations(self, client: PatronusAPI) -> None:
        trace_insight = client.trace_insight.get_error_aggregations()
        assert_matches_type(TraceInsightGetErrorAggregationsResponse, trace_insight, path=["response"])

    @parametrize
    def test_method_get_error_aggregations_with_all_params(self, client: PatronusAPI) -> None:
        trace_insight = client.trace_insight.get_error_aggregations(
            app="app",
            end_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            error_types=["string"],
            experiment_id=0,
            project_id="project_id",
            start_time=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(TraceInsightGetErrorAggregationsResponse, trace_insight, path=["response"])

    @parametrize
    def test_raw_response_get_error_aggregations(self, client: PatronusAPI) -> None:
        response = client.trace_insight.with_raw_response.get_error_aggregations()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trace_insight = response.parse()
        assert_matches_type(TraceInsightGetErrorAggregationsResponse, trace_insight, path=["response"])

    @parametrize
    def test_streaming_response_get_error_aggregations(self, client: PatronusAPI) -> None:
        with client.trace_insight.with_streaming_response.get_error_aggregations() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trace_insight = response.parse()
            assert_matches_type(TraceInsightGetErrorAggregationsResponse, trace_insight, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list_jobs(self, client: PatronusAPI) -> None:
        trace_insight = client.trace_insight.list_jobs()
        assert_matches_type(TraceInsightListJobsResponse, trace_insight, path=["response"])

    @parametrize
    def test_method_list_jobs_with_all_params(self, client: PatronusAPI) -> None:
        trace_insight = client.trace_insight.list_jobs(
            app="app",
            experiment_id="experiment_id",
            job_id="job_id",
            job_status="pending",
            limit=1,
            offset=0,
            project_id="project_id",
            trace_id="trace_id",
        )
        assert_matches_type(TraceInsightListJobsResponse, trace_insight, path=["response"])

    @parametrize
    def test_raw_response_list_jobs(self, client: PatronusAPI) -> None:
        response = client.trace_insight.with_raw_response.list_jobs()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trace_insight = response.parse()
        assert_matches_type(TraceInsightListJobsResponse, trace_insight, path=["response"])

    @parametrize
    def test_streaming_response_list_jobs(self, client: PatronusAPI) -> None:
        with client.trace_insight.with_streaming_response.list_jobs() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trace_insight = response.parse()
            assert_matches_type(TraceInsightListJobsResponse, trace_insight, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_search_span_analysis(self, client: PatronusAPI) -> None:
        trace_insight = client.trace_insight.search_span_analysis()
        assert_matches_type(TraceInsightSearchSpanAnalysisResponse, trace_insight, path=["response"])

    @parametrize
    def test_method_search_span_analysis_with_all_params(self, client: PatronusAPI) -> None:
        trace_insight = client.trace_insight.search_span_analysis(
            end_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            limit=1,
            offset=0,
            span_id="span_id",
            start_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            trace_id="trace_id",
        )
        assert_matches_type(TraceInsightSearchSpanAnalysisResponse, trace_insight, path=["response"])

    @parametrize
    def test_raw_response_search_span_analysis(self, client: PatronusAPI) -> None:
        response = client.trace_insight.with_raw_response.search_span_analysis()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trace_insight = response.parse()
        assert_matches_type(TraceInsightSearchSpanAnalysisResponse, trace_insight, path=["response"])

    @parametrize
    def test_streaming_response_search_span_analysis(self, client: PatronusAPI) -> None:
        with client.trace_insight.with_streaming_response.search_span_analysis() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trace_insight = response.parse()
            assert_matches_type(TraceInsightSearchSpanAnalysisResponse, trace_insight, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_search_trace_insights(self, client: PatronusAPI) -> None:
        trace_insight = client.trace_insight.search_trace_insights()
        assert_matches_type(TraceInsightSearchTraceInsightsResponse, trace_insight, path=["response"])

    @parametrize
    def test_method_search_trace_insights_with_all_params(self, client: PatronusAPI) -> None:
        trace_insight = client.trace_insight.search_trace_insights(
            app="app",
            end_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            error_types=["string"],
            experiment_id=0,
            limit=1,
            offset=0,
            project_id="project_id",
            redis_job_id="redis_job_id",
            start_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            trace_id="trace_id",
        )
        assert_matches_type(TraceInsightSearchTraceInsightsResponse, trace_insight, path=["response"])

    @parametrize
    def test_raw_response_search_trace_insights(self, client: PatronusAPI) -> None:
        response = client.trace_insight.with_raw_response.search_trace_insights()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trace_insight = response.parse()
        assert_matches_type(TraceInsightSearchTraceInsightsResponse, trace_insight, path=["response"])

    @parametrize
    def test_streaming_response_search_trace_insights(self, client: PatronusAPI) -> None:
        with client.trace_insight.with_streaming_response.search_trace_insights() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trace_insight = response.parse()
            assert_matches_type(TraceInsightSearchTraceInsightsResponse, trace_insight, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTraceInsight:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_list(self, async_client: AsyncPatronusAPI) -> None:
        trace_insight = await async_client.trace_insight.list()
        assert_matches_type(TraceInsightListResponse, trace_insight, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        trace_insight = await async_client.trace_insight.list(
            app="app",
            experiment_id="experiment_id",
            job_id="job_id",
            limit=1,
            offset=0,
            project_id="project_id",
            trace_id="trace_id",
        )
        assert_matches_type(TraceInsightListResponse, trace_insight, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.trace_insight.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trace_insight = await response.parse()
        assert_matches_type(TraceInsightListResponse, trace_insight, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.trace_insight.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trace_insight = await response.parse()
            assert_matches_type(TraceInsightListResponse, trace_insight, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_create_job(self, async_client: AsyncPatronusAPI) -> None:
        trace_insight = await async_client.trace_insight.create_job(
            trace_id="trace_id",
        )
        assert_matches_type(TraceInsightCreateJobResponse, trace_insight, path=["response"])

    @parametrize
    async def test_raw_response_create_job(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.trace_insight.with_raw_response.create_job(
            trace_id="trace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trace_insight = await response.parse()
        assert_matches_type(TraceInsightCreateJobResponse, trace_insight, path=["response"])

    @parametrize
    async def test_streaming_response_create_job(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.trace_insight.with_streaming_response.create_job(
            trace_id="trace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trace_insight = await response.parse()
            assert_matches_type(TraceInsightCreateJobResponse, trace_insight, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_get_error_aggregations(self, async_client: AsyncPatronusAPI) -> None:
        trace_insight = await async_client.trace_insight.get_error_aggregations()
        assert_matches_type(TraceInsightGetErrorAggregationsResponse, trace_insight, path=["response"])

    @parametrize
    async def test_method_get_error_aggregations_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        trace_insight = await async_client.trace_insight.get_error_aggregations(
            app="app",
            end_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            error_types=["string"],
            experiment_id=0,
            project_id="project_id",
            start_time=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(TraceInsightGetErrorAggregationsResponse, trace_insight, path=["response"])

    @parametrize
    async def test_raw_response_get_error_aggregations(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.trace_insight.with_raw_response.get_error_aggregations()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trace_insight = await response.parse()
        assert_matches_type(TraceInsightGetErrorAggregationsResponse, trace_insight, path=["response"])

    @parametrize
    async def test_streaming_response_get_error_aggregations(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.trace_insight.with_streaming_response.get_error_aggregations() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trace_insight = await response.parse()
            assert_matches_type(TraceInsightGetErrorAggregationsResponse, trace_insight, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list_jobs(self, async_client: AsyncPatronusAPI) -> None:
        trace_insight = await async_client.trace_insight.list_jobs()
        assert_matches_type(TraceInsightListJobsResponse, trace_insight, path=["response"])

    @parametrize
    async def test_method_list_jobs_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        trace_insight = await async_client.trace_insight.list_jobs(
            app="app",
            experiment_id="experiment_id",
            job_id="job_id",
            job_status="pending",
            limit=1,
            offset=0,
            project_id="project_id",
            trace_id="trace_id",
        )
        assert_matches_type(TraceInsightListJobsResponse, trace_insight, path=["response"])

    @parametrize
    async def test_raw_response_list_jobs(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.trace_insight.with_raw_response.list_jobs()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trace_insight = await response.parse()
        assert_matches_type(TraceInsightListJobsResponse, trace_insight, path=["response"])

    @parametrize
    async def test_streaming_response_list_jobs(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.trace_insight.with_streaming_response.list_jobs() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trace_insight = await response.parse()
            assert_matches_type(TraceInsightListJobsResponse, trace_insight, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_search_span_analysis(self, async_client: AsyncPatronusAPI) -> None:
        trace_insight = await async_client.trace_insight.search_span_analysis()
        assert_matches_type(TraceInsightSearchSpanAnalysisResponse, trace_insight, path=["response"])

    @parametrize
    async def test_method_search_span_analysis_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        trace_insight = await async_client.trace_insight.search_span_analysis(
            end_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            limit=1,
            offset=0,
            span_id="span_id",
            start_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            trace_id="trace_id",
        )
        assert_matches_type(TraceInsightSearchSpanAnalysisResponse, trace_insight, path=["response"])

    @parametrize
    async def test_raw_response_search_span_analysis(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.trace_insight.with_raw_response.search_span_analysis()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trace_insight = await response.parse()
        assert_matches_type(TraceInsightSearchSpanAnalysisResponse, trace_insight, path=["response"])

    @parametrize
    async def test_streaming_response_search_span_analysis(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.trace_insight.with_streaming_response.search_span_analysis() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trace_insight = await response.parse()
            assert_matches_type(TraceInsightSearchSpanAnalysisResponse, trace_insight, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_search_trace_insights(self, async_client: AsyncPatronusAPI) -> None:
        trace_insight = await async_client.trace_insight.search_trace_insights()
        assert_matches_type(TraceInsightSearchTraceInsightsResponse, trace_insight, path=["response"])

    @parametrize
    async def test_method_search_trace_insights_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        trace_insight = await async_client.trace_insight.search_trace_insights(
            app="app",
            end_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            error_types=["string"],
            experiment_id=0,
            limit=1,
            offset=0,
            project_id="project_id",
            redis_job_id="redis_job_id",
            start_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            trace_id="trace_id",
        )
        assert_matches_type(TraceInsightSearchTraceInsightsResponse, trace_insight, path=["response"])

    @parametrize
    async def test_raw_response_search_trace_insights(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.trace_insight.with_raw_response.search_trace_insights()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        trace_insight = await response.parse()
        assert_matches_type(TraceInsightSearchTraceInsightsResponse, trace_insight, path=["response"])

    @parametrize
    async def test_streaming_response_search_trace_insights(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.trace_insight.with_streaming_response.search_trace_insights() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            trace_insight = await response.parse()
            assert_matches_type(TraceInsightSearchTraceInsightsResponse, trace_insight, path=["response"])

        assert cast(Any, response.is_closed) is True
