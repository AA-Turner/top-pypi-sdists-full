# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from langsmith import Langsmith, AsyncLangsmith
from tests.utils import assert_matches_type
from langsmith.types import Run
from langsmith._utils import parse_datetime
from langsmith.types.public import RunQueryResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRuns:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Langsmith) -> None:
        run = client.public.runs.retrieve(
            run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            share_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            selects=["string"],
            start_time=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(Run, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Langsmith) -> None:
        run = client.public.runs.retrieve(
            run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            share_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            selects=["string"],
            start_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            accept="Accept",
        )
        assert_matches_type(Run, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Langsmith) -> None:

        response = client.public.runs.with_raw_response.retrieve(
            run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            share_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            selects=["string"],
            start_time=parse_datetime("2019-12-27T18:11:19.117Z"),
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = response.parse()
        assert_matches_type(Run, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Langsmith) -> None:
        with client.public.runs.with_streaming_response.retrieve(
            run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            share_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            selects=["string"],
            start_time=parse_datetime("2019-12-27T18:11:19.117Z"),
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = response.parse()
            assert_matches_type(Run, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Langsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `share_token` but received ''"):
            client.public.runs.with_raw_response.retrieve(
                run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                share_token="",
                selects=["string"],
                start_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `run_id` but received ''"):
            client.public.runs.with_raw_response.retrieve(
                run_id="",
                share_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                selects=["string"],
                start_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_query(self, client: Langsmith) -> None:
        run = client.public.runs.query(
            share_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(RunQueryResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_query_with_all_params(self, client: Langsmith) -> None:
        run = client.public.runs.query(
            share_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            selects=[
                "ID",
                "NAME",
                "PROJECT_ID",
                "START_TIME",
                "RUN_TYPE",
                "STATUS",
                "INPUTS_PREVIEW",
                "OUTPUTS_PREVIEW",
                "METADATA",
            ],
            accept="Accept",
        )
        assert_matches_type(RunQueryResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_query(self, client: Langsmith) -> None:

        response = client.public.runs.with_raw_response.query(
            share_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = response.parse()
        assert_matches_type(RunQueryResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_query(self, client: Langsmith) -> None:
        with client.public.runs.with_streaming_response.query(
            share_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = response.parse()
            assert_matches_type(RunQueryResponse, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_query(self, client: Langsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `share_token` but received ''"):
            client.public.runs.with_raw_response.query(
                share_token="",
            )


class TestAsyncRuns:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncLangsmith) -> None:
        run = await async_client.public.runs.retrieve(
            run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            share_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            selects=["string"],
            start_time=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(Run, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncLangsmith) -> None:
        run = await async_client.public.runs.retrieve(
            run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            share_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            selects=["string"],
            start_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            accept="Accept",
        )
        assert_matches_type(Run, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncLangsmith) -> None:

        response = await async_client.public.runs.with_raw_response.retrieve(
            run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            share_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            selects=["string"],
            start_time=parse_datetime("2019-12-27T18:11:19.117Z"),
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = await response.parse()
        assert_matches_type(Run, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncLangsmith) -> None:
        async with async_client.public.runs.with_streaming_response.retrieve(
            run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            share_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            selects=["string"],
            start_time=parse_datetime("2019-12-27T18:11:19.117Z"),
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = await response.parse()
            assert_matches_type(Run, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncLangsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `share_token` but received ''"):
            await async_client.public.runs.with_raw_response.retrieve(
                run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                share_token="",
                selects=["string"],
                start_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `run_id` but received ''"):
            await async_client.public.runs.with_raw_response.retrieve(
                run_id="",
                share_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                selects=["string"],
                start_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_query(self, async_client: AsyncLangsmith) -> None:
        run = await async_client.public.runs.query(
            share_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(RunQueryResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_query_with_all_params(self, async_client: AsyncLangsmith) -> None:
        run = await async_client.public.runs.query(
            share_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            selects=[
                "ID",
                "NAME",
                "PROJECT_ID",
                "START_TIME",
                "RUN_TYPE",
                "STATUS",
                "INPUTS_PREVIEW",
                "OUTPUTS_PREVIEW",
                "METADATA",
            ],
            accept="Accept",
        )
        assert_matches_type(RunQueryResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_query(self, async_client: AsyncLangsmith) -> None:

        response = await async_client.public.runs.with_raw_response.query(
            share_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = await response.parse()
        assert_matches_type(RunQueryResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_query(self, async_client: AsyncLangsmith) -> None:
        async with async_client.public.runs.with_streaming_response.query(
            share_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run = await response.parse()
            assert_matches_type(RunQueryResponse, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_query(self, async_client: AsyncLangsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `share_token` but received ''"):
            await async_client.public.runs.with_raw_response.query(
                share_token="",
            )
