# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from scale_gp_beta import SGPClient, AsyncSGPClient
from scale_gp_beta.types import (
    SpanAssessment,
    SpanAssessmentDeleteResponse,
)
from scale_gp_beta.pagination import SyncAPIListPage, AsyncAPIListPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSpanAssessments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        span_assessment = client.span_assessments.create(
            assessment_type="comment",
            span_id="span_id",
            trace_id="trace_id",
        )
        assert_matches_type(SpanAssessment, span_assessment, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        span_assessment = client.span_assessments.create(
            assessment_type="comment",
            span_id="span_id",
            trace_id="trace_id",
            approval="approved",
            comment="comment",
            metadata={"foo": "bar"},
            overwrite={"foo": "bar"},
            rating=1,
            rubric={"foo": "string"},
        )
        assert_matches_type(SpanAssessment, span_assessment, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.span_assessments.with_raw_response.create(
            assessment_type="comment",
            span_id="span_id",
            trace_id="trace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span_assessment = response.parse()
        assert_matches_type(SpanAssessment, span_assessment, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.span_assessments.with_streaming_response.create(
            assessment_type="comment",
            span_id="span_id",
            trace_id="trace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span_assessment = response.parse()
            assert_matches_type(SpanAssessment, span_assessment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        span_assessment = client.span_assessments.retrieve(
            "span_assessment_id",
        )
        assert_matches_type(SpanAssessment, span_assessment, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.span_assessments.with_raw_response.retrieve(
            "span_assessment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span_assessment = response.parse()
        assert_matches_type(SpanAssessment, span_assessment, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.span_assessments.with_streaming_response.retrieve(
            "span_assessment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span_assessment = response.parse()
            assert_matches_type(SpanAssessment, span_assessment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `span_assessment_id` but received ''"):
            client.span_assessments.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        span_assessment = client.span_assessments.update(
            span_assessment_id="span_assessment_id",
        )
        assert_matches_type(SpanAssessment, span_assessment, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGPClient) -> None:
        span_assessment = client.span_assessments.update(
            span_assessment_id="span_assessment_id",
            approval="approved",
            assessment_type="comment",
            comment="comment",
            metadata={"foo": "bar"},
            overwrite={"foo": "bar"},
            rating=1,
            rubric={"foo": "string"},
        )
        assert_matches_type(SpanAssessment, span_assessment, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.span_assessments.with_raw_response.update(
            span_assessment_id="span_assessment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span_assessment = response.parse()
        assert_matches_type(SpanAssessment, span_assessment, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.span_assessments.with_streaming_response.update(
            span_assessment_id="span_assessment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span_assessment = response.parse()
            assert_matches_type(SpanAssessment, span_assessment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `span_assessment_id` but received ''"):
            client.span_assessments.with_raw_response.update(
                span_assessment_id="",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        span_assessment = client.span_assessments.list()
        assert_matches_type(SyncAPIListPage[SpanAssessment], span_assessment, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        span_assessment = client.span_assessments.list(
            assessment_type="comment",
            span_id="span_id",
            trace_id="trace_id",
        )
        assert_matches_type(SyncAPIListPage[SpanAssessment], span_assessment, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.span_assessments.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span_assessment = response.parse()
        assert_matches_type(SyncAPIListPage[SpanAssessment], span_assessment, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.span_assessments.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span_assessment = response.parse()
            assert_matches_type(SyncAPIListPage[SpanAssessment], span_assessment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        span_assessment = client.span_assessments.delete(
            "span_assessment_id",
        )
        assert_matches_type(SpanAssessmentDeleteResponse, span_assessment, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.span_assessments.with_raw_response.delete(
            "span_assessment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span_assessment = response.parse()
        assert_matches_type(SpanAssessmentDeleteResponse, span_assessment, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.span_assessments.with_streaming_response.delete(
            "span_assessment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span_assessment = response.parse()
            assert_matches_type(SpanAssessmentDeleteResponse, span_assessment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `span_assessment_id` but received ''"):
            client.span_assessments.with_raw_response.delete(
                "",
            )


class TestAsyncSpanAssessments:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        span_assessment = await async_client.span_assessments.create(
            assessment_type="comment",
            span_id="span_id",
            trace_id="trace_id",
        )
        assert_matches_type(SpanAssessment, span_assessment, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        span_assessment = await async_client.span_assessments.create(
            assessment_type="comment",
            span_id="span_id",
            trace_id="trace_id",
            approval="approved",
            comment="comment",
            metadata={"foo": "bar"},
            overwrite={"foo": "bar"},
            rating=1,
            rubric={"foo": "string"},
        )
        assert_matches_type(SpanAssessment, span_assessment, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.span_assessments.with_raw_response.create(
            assessment_type="comment",
            span_id="span_id",
            trace_id="trace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span_assessment = await response.parse()
        assert_matches_type(SpanAssessment, span_assessment, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.span_assessments.with_streaming_response.create(
            assessment_type="comment",
            span_id="span_id",
            trace_id="trace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span_assessment = await response.parse()
            assert_matches_type(SpanAssessment, span_assessment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        span_assessment = await async_client.span_assessments.retrieve(
            "span_assessment_id",
        )
        assert_matches_type(SpanAssessment, span_assessment, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.span_assessments.with_raw_response.retrieve(
            "span_assessment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span_assessment = await response.parse()
        assert_matches_type(SpanAssessment, span_assessment, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.span_assessments.with_streaming_response.retrieve(
            "span_assessment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span_assessment = await response.parse()
            assert_matches_type(SpanAssessment, span_assessment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `span_assessment_id` but received ''"):
            await async_client.span_assessments.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        span_assessment = await async_client.span_assessments.update(
            span_assessment_id="span_assessment_id",
        )
        assert_matches_type(SpanAssessment, span_assessment, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        span_assessment = await async_client.span_assessments.update(
            span_assessment_id="span_assessment_id",
            approval="approved",
            assessment_type="comment",
            comment="comment",
            metadata={"foo": "bar"},
            overwrite={"foo": "bar"},
            rating=1,
            rubric={"foo": "string"},
        )
        assert_matches_type(SpanAssessment, span_assessment, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.span_assessments.with_raw_response.update(
            span_assessment_id="span_assessment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span_assessment = await response.parse()
        assert_matches_type(SpanAssessment, span_assessment, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.span_assessments.with_streaming_response.update(
            span_assessment_id="span_assessment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span_assessment = await response.parse()
            assert_matches_type(SpanAssessment, span_assessment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `span_assessment_id` but received ''"):
            await async_client.span_assessments.with_raw_response.update(
                span_assessment_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        span_assessment = await async_client.span_assessments.list()
        assert_matches_type(AsyncAPIListPage[SpanAssessment], span_assessment, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        span_assessment = await async_client.span_assessments.list(
            assessment_type="comment",
            span_id="span_id",
            trace_id="trace_id",
        )
        assert_matches_type(AsyncAPIListPage[SpanAssessment], span_assessment, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.span_assessments.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span_assessment = await response.parse()
        assert_matches_type(AsyncAPIListPage[SpanAssessment], span_assessment, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.span_assessments.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span_assessment = await response.parse()
            assert_matches_type(AsyncAPIListPage[SpanAssessment], span_assessment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        span_assessment = await async_client.span_assessments.delete(
            "span_assessment_id",
        )
        assert_matches_type(SpanAssessmentDeleteResponse, span_assessment, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.span_assessments.with_raw_response.delete(
            "span_assessment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span_assessment = await response.parse()
        assert_matches_type(SpanAssessmentDeleteResponse, span_assessment, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.span_assessments.with_streaming_response.delete(
            "span_assessment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span_assessment = await response.parse()
            assert_matches_type(SpanAssessmentDeleteResponse, span_assessment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `span_assessment_id` but received ''"):
            await async_client.span_assessments.with_raw_response.delete(
                "",
            )
