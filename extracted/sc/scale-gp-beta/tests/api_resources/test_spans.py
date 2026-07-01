# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from scale_gp_beta import SGPClient, AsyncSGPClient
from scale_gp_beta.types import (
    Span,
    APIListSpan,
)
from scale_gp_beta._utils import parse_datetime
from scale_gp_beta.pagination import SyncCursorPage, AsyncCursorPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSpans:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        span = client.spans.create(
            name="name",
            start_timestamp=parse_datetime("2019-12-27T18:11:19.117Z"),
            trace_id="trace_id",
        )
        assert_matches_type(Span, span, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        span = client.spans.create(
            name="name",
            start_timestamp=parse_datetime("2019-12-27T18:11:19.117Z"),
            trace_id="trace_id",
            id="id",
            application_interaction_id="application_interaction_id",
            application_variant_id="application_variant_id",
            end_timestamp=parse_datetime("2019-12-27T18:11:19.117Z"),
            group_id="group_id",
            input={"foo": "bar"},
            metadata={"foo": "bar"},
            output={"foo": "bar"},
            parent_id="parent_id",
            status="SUCCESS",
            type="TEXT_INPUT",
        )
        assert_matches_type(Span, span, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.spans.with_raw_response.create(
            name="name",
            start_timestamp=parse_datetime("2019-12-27T18:11:19.117Z"),
            trace_id="trace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span = response.parse()
        assert_matches_type(Span, span, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.spans.with_streaming_response.create(
            name="name",
            start_timestamp=parse_datetime("2019-12-27T18:11:19.117Z"),
            trace_id="trace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span = response.parse()
            assert_matches_type(Span, span, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        span = client.spans.retrieve(
            "span_id",
        )
        assert_matches_type(Span, span, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.spans.with_raw_response.retrieve(
            "span_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span = response.parse()
        assert_matches_type(Span, span, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.spans.with_streaming_response.retrieve(
            "span_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span = response.parse()
            assert_matches_type(Span, span, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `span_id` but received ''"):
            client.spans.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        span = client.spans.update(
            span_id="span_id",
        )
        assert_matches_type(Span, span, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGPClient) -> None:
        span = client.spans.update(
            span_id="span_id",
            end_timestamp=parse_datetime("2019-12-27T18:11:19.117Z"),
            metadata={"foo": "bar"},
            name="name",
            output={"foo": "bar"},
            status="SUCCESS",
        )
        assert_matches_type(Span, span, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.spans.with_raw_response.update(
            span_id="span_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span = response.parse()
        assert_matches_type(Span, span, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.spans.with_streaming_response.update(
            span_id="span_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span = response.parse()
            assert_matches_type(Span, span, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `span_id` but received ''"):
            client.spans.with_raw_response.update(
                span_id="",
            )

    @parametrize
    def test_method_batch(self, client: SGPClient) -> None:
        span = client.spans.batch(
            items=[
                {
                    "name": "name",
                    "start_timestamp": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "trace_id": "trace_id",
                }
            ],
        )
        assert_matches_type(APIListSpan, span, path=["response"])

    @parametrize
    def test_raw_response_batch(self, client: SGPClient) -> None:
        response = client.spans.with_raw_response.batch(
            items=[
                {
                    "name": "name",
                    "start_timestamp": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "trace_id": "trace_id",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span = response.parse()
        assert_matches_type(APIListSpan, span, path=["response"])

    @parametrize
    def test_streaming_response_batch(self, client: SGPClient) -> None:
        with client.spans.with_streaming_response.batch(
            items=[
                {
                    "name": "name",
                    "start_timestamp": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "trace_id": "trace_id",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span = response.parse()
            assert_matches_type(APIListSpan, span, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_search(self, client: SGPClient) -> None:
        span = client.spans.search()
        assert_matches_type(SyncCursorPage[Span], span, path=["response"])

    @parametrize
    def test_method_search_with_all_params(self, client: SGPClient) -> None:
        span = client.spans.search(
            ending_before="ending_before",
            from_ts=parse_datetime("2019-12-27T18:11:19.117Z"),
            limit=1,
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
            to_ts=parse_datetime("2019-12-27T18:11:19.117Z"),
            acp_types=["string"],
            agentex_agent_ids=["string"],
            agentex_agent_names=["string"],
            application_variant_ids=["string"],
            assessment_types=["string"],
            excluded_span_ids=["string"],
            excluded_trace_ids=["string"],
            extra_metadata={"foo": "bar"},
            group_id="group_id",
            max_duration_ms=0,
            min_duration_ms=0,
            names=["string"],
            parents_only=True,
            search_texts=["string"],
            span_ids=["string"],
            statuses=["SUCCESS"],
            trace_ids=["string"],
            types=["TEXT_INPUT"],
        )
        assert_matches_type(SyncCursorPage[Span], span, path=["response"])

    @parametrize
    def test_raw_response_search(self, client: SGPClient) -> None:
        response = client.spans.with_raw_response.search()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span = response.parse()
        assert_matches_type(SyncCursorPage[Span], span, path=["response"])

    @parametrize
    def test_streaming_response_search(self, client: SGPClient) -> None:
        with client.spans.with_streaming_response.search() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span = response.parse()
            assert_matches_type(SyncCursorPage[Span], span, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_upsert_batch(self, client: SGPClient) -> None:
        span = client.spans.upsert_batch(
            items=[
                {
                    "name": "name",
                    "start_timestamp": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "trace_id": "trace_id",
                }
            ],
        )
        assert_matches_type(APIListSpan, span, path=["response"])

    @parametrize
    def test_raw_response_upsert_batch(self, client: SGPClient) -> None:
        response = client.spans.with_raw_response.upsert_batch(
            items=[
                {
                    "name": "name",
                    "start_timestamp": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "trace_id": "trace_id",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span = response.parse()
        assert_matches_type(APIListSpan, span, path=["response"])

    @parametrize
    def test_streaming_response_upsert_batch(self, client: SGPClient) -> None:
        with client.spans.with_streaming_response.upsert_batch(
            items=[
                {
                    "name": "name",
                    "start_timestamp": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "trace_id": "trace_id",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span = response.parse()
            assert_matches_type(APIListSpan, span, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSpans:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        span = await async_client.spans.create(
            name="name",
            start_timestamp=parse_datetime("2019-12-27T18:11:19.117Z"),
            trace_id="trace_id",
        )
        assert_matches_type(Span, span, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        span = await async_client.spans.create(
            name="name",
            start_timestamp=parse_datetime("2019-12-27T18:11:19.117Z"),
            trace_id="trace_id",
            id="id",
            application_interaction_id="application_interaction_id",
            application_variant_id="application_variant_id",
            end_timestamp=parse_datetime("2019-12-27T18:11:19.117Z"),
            group_id="group_id",
            input={"foo": "bar"},
            metadata={"foo": "bar"},
            output={"foo": "bar"},
            parent_id="parent_id",
            status="SUCCESS",
            type="TEXT_INPUT",
        )
        assert_matches_type(Span, span, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.spans.with_raw_response.create(
            name="name",
            start_timestamp=parse_datetime("2019-12-27T18:11:19.117Z"),
            trace_id="trace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span = await response.parse()
        assert_matches_type(Span, span, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.spans.with_streaming_response.create(
            name="name",
            start_timestamp=parse_datetime("2019-12-27T18:11:19.117Z"),
            trace_id="trace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span = await response.parse()
            assert_matches_type(Span, span, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        span = await async_client.spans.retrieve(
            "span_id",
        )
        assert_matches_type(Span, span, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.spans.with_raw_response.retrieve(
            "span_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span = await response.parse()
        assert_matches_type(Span, span, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.spans.with_streaming_response.retrieve(
            "span_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span = await response.parse()
            assert_matches_type(Span, span, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `span_id` but received ''"):
            await async_client.spans.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        span = await async_client.spans.update(
            span_id="span_id",
        )
        assert_matches_type(Span, span, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        span = await async_client.spans.update(
            span_id="span_id",
            end_timestamp=parse_datetime("2019-12-27T18:11:19.117Z"),
            metadata={"foo": "bar"},
            name="name",
            output={"foo": "bar"},
            status="SUCCESS",
        )
        assert_matches_type(Span, span, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.spans.with_raw_response.update(
            span_id="span_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span = await response.parse()
        assert_matches_type(Span, span, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.spans.with_streaming_response.update(
            span_id="span_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span = await response.parse()
            assert_matches_type(Span, span, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `span_id` but received ''"):
            await async_client.spans.with_raw_response.update(
                span_id="",
            )

    @parametrize
    async def test_method_batch(self, async_client: AsyncSGPClient) -> None:
        span = await async_client.spans.batch(
            items=[
                {
                    "name": "name",
                    "start_timestamp": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "trace_id": "trace_id",
                }
            ],
        )
        assert_matches_type(APIListSpan, span, path=["response"])

    @parametrize
    async def test_raw_response_batch(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.spans.with_raw_response.batch(
            items=[
                {
                    "name": "name",
                    "start_timestamp": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "trace_id": "trace_id",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span = await response.parse()
        assert_matches_type(APIListSpan, span, path=["response"])

    @parametrize
    async def test_streaming_response_batch(self, async_client: AsyncSGPClient) -> None:
        async with async_client.spans.with_streaming_response.batch(
            items=[
                {
                    "name": "name",
                    "start_timestamp": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "trace_id": "trace_id",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span = await response.parse()
            assert_matches_type(APIListSpan, span, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_search(self, async_client: AsyncSGPClient) -> None:
        span = await async_client.spans.search()
        assert_matches_type(AsyncCursorPage[Span], span, path=["response"])

    @parametrize
    async def test_method_search_with_all_params(self, async_client: AsyncSGPClient) -> None:
        span = await async_client.spans.search(
            ending_before="ending_before",
            from_ts=parse_datetime("2019-12-27T18:11:19.117Z"),
            limit=1,
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
            to_ts=parse_datetime("2019-12-27T18:11:19.117Z"),
            acp_types=["string"],
            agentex_agent_ids=["string"],
            agentex_agent_names=["string"],
            application_variant_ids=["string"],
            assessment_types=["string"],
            excluded_span_ids=["string"],
            excluded_trace_ids=["string"],
            extra_metadata={"foo": "bar"},
            group_id="group_id",
            max_duration_ms=0,
            min_duration_ms=0,
            names=["string"],
            parents_only=True,
            search_texts=["string"],
            span_ids=["string"],
            statuses=["SUCCESS"],
            trace_ids=["string"],
            types=["TEXT_INPUT"],
        )
        assert_matches_type(AsyncCursorPage[Span], span, path=["response"])

    @parametrize
    async def test_raw_response_search(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.spans.with_raw_response.search()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span = await response.parse()
        assert_matches_type(AsyncCursorPage[Span], span, path=["response"])

    @parametrize
    async def test_streaming_response_search(self, async_client: AsyncSGPClient) -> None:
        async with async_client.spans.with_streaming_response.search() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span = await response.parse()
            assert_matches_type(AsyncCursorPage[Span], span, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_upsert_batch(self, async_client: AsyncSGPClient) -> None:
        span = await async_client.spans.upsert_batch(
            items=[
                {
                    "name": "name",
                    "start_timestamp": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "trace_id": "trace_id",
                }
            ],
        )
        assert_matches_type(APIListSpan, span, path=["response"])

    @parametrize
    async def test_raw_response_upsert_batch(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.spans.with_raw_response.upsert_batch(
            items=[
                {
                    "name": "name",
                    "start_timestamp": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "trace_id": "trace_id",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        span = await response.parse()
        assert_matches_type(APIListSpan, span, path=["response"])

    @parametrize
    async def test_streaming_response_upsert_batch(self, async_client: AsyncSGPClient) -> None:
        async with async_client.spans.with_streaming_response.upsert_batch(
            items=[
                {
                    "name": "name",
                    "start_timestamp": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "trace_id": "trace_id",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            span = await response.parse()
            assert_matches_type(APIListSpan, span, path=["response"])

        assert cast(Any, response.is_closed) is True
