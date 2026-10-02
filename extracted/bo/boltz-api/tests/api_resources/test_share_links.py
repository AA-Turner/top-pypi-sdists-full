# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from boltz_api import Boltz, AsyncBoltz
from tests.utils import assert_matches_type
from boltz_api.types import (
    ShareLinkReadResponse,
    ShareLinkCreateResponse,
    ShareLinkArchiveResponse,
    ShareLinkRetrieveResponse,
    ShareLinkListPipelineResultsResponse,
)
from boltz_api.pagination import SyncCursorPage, AsyncCursorPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestShareLinks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create(self, client: Boltz) -> None:
        share_link = client.share_links.create(
            expires_at="expires_at",
        )
        assert_matches_type(ShareLinkCreateResponse, share_link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Boltz) -> None:
        share_link = client.share_links.create(
            expires_at="expires_at",
            access_parameters={"access_mode": "public"},
            pipeline_ids=["string"],
            prediction_ids=["string"],
            workspace_id="workspace_id",
        )
        assert_matches_type(ShareLinkCreateResponse, share_link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Boltz) -> None:
        response = client.share_links.with_raw_response.create(
            expires_at="expires_at",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        share_link = response.parse()
        assert_matches_type(ShareLinkCreateResponse, share_link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Boltz) -> None:
        with client.share_links.with_streaming_response.create(
            expires_at="expires_at",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            share_link = response.parse()
            assert_matches_type(ShareLinkCreateResponse, share_link, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Boltz) -> None:
        share_link = client.share_links.retrieve(
            "shr_qoEFr2BlPTBLuM5BinaC8x7iVPP_AwppEOmlxQjJ-eo",
        )
        assert_matches_type(ShareLinkRetrieveResponse, share_link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Boltz) -> None:
        response = client.share_links.with_raw_response.retrieve(
            "shr_qoEFr2BlPTBLuM5BinaC8x7iVPP_AwppEOmlxQjJ-eo",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        share_link = response.parse()
        assert_matches_type(ShareLinkRetrieveResponse, share_link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Boltz) -> None:
        with client.share_links.with_streaming_response.retrieve(
            "shr_qoEFr2BlPTBLuM5BinaC8x7iVPP_AwppEOmlxQjJ-eo",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            share_link = response.parse()
            assert_matches_type(ShareLinkRetrieveResponse, share_link, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.share_links.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_archive(self, client: Boltz) -> None:
        share_link = client.share_links.archive(
            "shr_qoEFr2BlPTBLuM5BinaC8x7iVPP_AwppEOmlxQjJ-eo",
        )
        assert_matches_type(ShareLinkArchiveResponse, share_link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_archive(self, client: Boltz) -> None:
        response = client.share_links.with_raw_response.archive(
            "shr_qoEFr2BlPTBLuM5BinaC8x7iVPP_AwppEOmlxQjJ-eo",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        share_link = response.parse()
        assert_matches_type(ShareLinkArchiveResponse, share_link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_archive(self, client: Boltz) -> None:
        with client.share_links.with_streaming_response.archive(
            "shr_qoEFr2BlPTBLuM5BinaC8x7iVPP_AwppEOmlxQjJ-eo",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            share_link = response.parse()
            assert_matches_type(ShareLinkArchiveResponse, share_link, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_archive(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.share_links.with_raw_response.archive(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_pipeline_results(self, client: Boltz) -> None:
        share_link = client.share_links.list_pipeline_results(
            pipeline_id="pipelineId",
            id="id",
        )
        assert_matches_type(SyncCursorPage[ShareLinkListPipelineResultsResponse], share_link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_pipeline_results_with_all_params(self, client: Boltz) -> None:
        share_link = client.share_links.list_pipeline_results(
            pipeline_id="pipelineId",
            id="id",
            after_id="after_id",
            before_id="before_id",
            ids="ids",
            limit=1,
        )
        assert_matches_type(SyncCursorPage[ShareLinkListPipelineResultsResponse], share_link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list_pipeline_results(self, client: Boltz) -> None:
        response = client.share_links.with_raw_response.list_pipeline_results(
            pipeline_id="pipelineId",
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        share_link = response.parse()
        assert_matches_type(SyncCursorPage[ShareLinkListPipelineResultsResponse], share_link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list_pipeline_results(self, client: Boltz) -> None:
        with client.share_links.with_streaming_response.list_pipeline_results(
            pipeline_id="pipelineId",
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            share_link = response.parse()
            assert_matches_type(SyncCursorPage[ShareLinkListPipelineResultsResponse], share_link, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_list_pipeline_results(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.share_links.with_raw_response.list_pipeline_results(
                pipeline_id="pipelineId",
                id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `pipeline_id` but received ''"):
            client.share_links.with_raw_response.list_pipeline_results(
                pipeline_id="",
                id="id",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_read(self, client: Boltz) -> None:
        share_link = client.share_links.read(
            "shr_qoEFr2BlPTBLuM5BinaC8x7iVPP_AwppEOmlxQjJ-eo",
        )
        assert_matches_type(ShareLinkReadResponse, share_link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_read(self, client: Boltz) -> None:
        response = client.share_links.with_raw_response.read(
            "shr_qoEFr2BlPTBLuM5BinaC8x7iVPP_AwppEOmlxQjJ-eo",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        share_link = response.parse()
        assert_matches_type(ShareLinkReadResponse, share_link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_read(self, client: Boltz) -> None:
        with client.share_links.with_streaming_response.read(
            "shr_qoEFr2BlPTBLuM5BinaC8x7iVPP_AwppEOmlxQjJ-eo",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            share_link = response.parse()
            assert_matches_type(ShareLinkReadResponse, share_link, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_read(self, client: Boltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.share_links.with_raw_response.read(
                "",
            )


class TestAsyncShareLinks:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncBoltz) -> None:
        share_link = await async_client.share_links.create(
            expires_at="expires_at",
        )
        assert_matches_type(ShareLinkCreateResponse, share_link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncBoltz) -> None:
        share_link = await async_client.share_links.create(
            expires_at="expires_at",
            access_parameters={"access_mode": "public"},
            pipeline_ids=["string"],
            prediction_ids=["string"],
            workspace_id="workspace_id",
        )
        assert_matches_type(ShareLinkCreateResponse, share_link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncBoltz) -> None:
        response = await async_client.share_links.with_raw_response.create(
            expires_at="expires_at",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        share_link = await response.parse()
        assert_matches_type(ShareLinkCreateResponse, share_link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncBoltz) -> None:
        async with async_client.share_links.with_streaming_response.create(
            expires_at="expires_at",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            share_link = await response.parse()
            assert_matches_type(ShareLinkCreateResponse, share_link, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncBoltz) -> None:
        share_link = await async_client.share_links.retrieve(
            "shr_qoEFr2BlPTBLuM5BinaC8x7iVPP_AwppEOmlxQjJ-eo",
        )
        assert_matches_type(ShareLinkRetrieveResponse, share_link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncBoltz) -> None:
        response = await async_client.share_links.with_raw_response.retrieve(
            "shr_qoEFr2BlPTBLuM5BinaC8x7iVPP_AwppEOmlxQjJ-eo",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        share_link = await response.parse()
        assert_matches_type(ShareLinkRetrieveResponse, share_link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncBoltz) -> None:
        async with async_client.share_links.with_streaming_response.retrieve(
            "shr_qoEFr2BlPTBLuM5BinaC8x7iVPP_AwppEOmlxQjJ-eo",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            share_link = await response.parse()
            assert_matches_type(ShareLinkRetrieveResponse, share_link, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.share_links.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_archive(self, async_client: AsyncBoltz) -> None:
        share_link = await async_client.share_links.archive(
            "shr_qoEFr2BlPTBLuM5BinaC8x7iVPP_AwppEOmlxQjJ-eo",
        )
        assert_matches_type(ShareLinkArchiveResponse, share_link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncBoltz) -> None:
        response = await async_client.share_links.with_raw_response.archive(
            "shr_qoEFr2BlPTBLuM5BinaC8x7iVPP_AwppEOmlxQjJ-eo",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        share_link = await response.parse()
        assert_matches_type(ShareLinkArchiveResponse, share_link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncBoltz) -> None:
        async with async_client.share_links.with_streaming_response.archive(
            "shr_qoEFr2BlPTBLuM5BinaC8x7iVPP_AwppEOmlxQjJ-eo",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            share_link = await response.parse()
            assert_matches_type(ShareLinkArchiveResponse, share_link, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_archive(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.share_links.with_raw_response.archive(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_pipeline_results(self, async_client: AsyncBoltz) -> None:
        share_link = await async_client.share_links.list_pipeline_results(
            pipeline_id="pipelineId",
            id="id",
        )
        assert_matches_type(AsyncCursorPage[ShareLinkListPipelineResultsResponse], share_link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_pipeline_results_with_all_params(self, async_client: AsyncBoltz) -> None:
        share_link = await async_client.share_links.list_pipeline_results(
            pipeline_id="pipelineId",
            id="id",
            after_id="after_id",
            before_id="before_id",
            ids="ids",
            limit=1,
        )
        assert_matches_type(AsyncCursorPage[ShareLinkListPipelineResultsResponse], share_link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list_pipeline_results(self, async_client: AsyncBoltz) -> None:
        response = await async_client.share_links.with_raw_response.list_pipeline_results(
            pipeline_id="pipelineId",
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        share_link = await response.parse()
        assert_matches_type(AsyncCursorPage[ShareLinkListPipelineResultsResponse], share_link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list_pipeline_results(self, async_client: AsyncBoltz) -> None:
        async with async_client.share_links.with_streaming_response.list_pipeline_results(
            pipeline_id="pipelineId",
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            share_link = await response.parse()
            assert_matches_type(AsyncCursorPage[ShareLinkListPipelineResultsResponse], share_link, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_list_pipeline_results(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.share_links.with_raw_response.list_pipeline_results(
                pipeline_id="pipelineId",
                id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `pipeline_id` but received ''"):
            await async_client.share_links.with_raw_response.list_pipeline_results(
                pipeline_id="",
                id="id",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_read(self, async_client: AsyncBoltz) -> None:
        share_link = await async_client.share_links.read(
            "shr_qoEFr2BlPTBLuM5BinaC8x7iVPP_AwppEOmlxQjJ-eo",
        )
        assert_matches_type(ShareLinkReadResponse, share_link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_read(self, async_client: AsyncBoltz) -> None:
        response = await async_client.share_links.with_raw_response.read(
            "shr_qoEFr2BlPTBLuM5BinaC8x7iVPP_AwppEOmlxQjJ-eo",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        share_link = await response.parse()
        assert_matches_type(ShareLinkReadResponse, share_link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_read(self, async_client: AsyncBoltz) -> None:
        async with async_client.share_links.with_streaming_response.read(
            "shr_qoEFr2BlPTBLuM5BinaC8x7iVPP_AwppEOmlxQjJ-eo",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            share_link = await response.parse()
            assert_matches_type(ShareLinkReadResponse, share_link, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_read(self, async_client: AsyncBoltz) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.share_links.with_raw_response.read(
                "",
            )
