# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp._utils import parse_datetime
from scale_gp.pagination import SyncPageResponse, AsyncPageResponse
from scale_gp.types.shared import GenericDeleteResponse
from scale_gp.types.knowledge_bases import (
    UploadSchedule,
    UploadScheduleWithViews,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUploadSchedules:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        upload_schedule = client.knowledge_bases.upload_schedules.create(
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config={"strategy": "character"},
            interval=0,
            knowledge_base_data_source_id="knowledge_base_data_source_id",
        )
        assert_matches_type(UploadSchedule, upload_schedule, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        upload_schedule = client.knowledge_bases.upload_schedules.create(
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config={
                "strategy": "character",
                "chunk_overlap": 0,
                "chunk_size": 1,
                "separator": "separator",
            },
            interval=0,
            knowledge_base_data_source_id="knowledge_base_data_source_id",
            account_id="account_id",
            next_run_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(UploadSchedule, upload_schedule, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.knowledge_bases.upload_schedules.with_raw_response.create(
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config={"strategy": "character"},
            interval=0,
            knowledge_base_data_source_id="knowledge_base_data_source_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload_schedule = response.parse()
        assert_matches_type(UploadSchedule, upload_schedule, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.knowledge_bases.upload_schedules.with_streaming_response.create(
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config={"strategy": "character"},
            interval=0,
            knowledge_base_data_source_id="knowledge_base_data_source_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload_schedule = response.parse()
            assert_matches_type(UploadSchedule, upload_schedule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.upload_schedules.with_raw_response.create(
                knowledge_base_id="",
                chunking_strategy_config={"strategy": "character"},
                interval=0,
                knowledge_base_data_source_id="knowledge_base_data_source_id",
            )

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        upload_schedule = client.knowledge_bases.upload_schedules.retrieve(
            upload_schedule_id="upload_schedule_id",
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(UploadScheduleWithViews, upload_schedule, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGPClient) -> None:
        upload_schedule = client.knowledge_bases.upload_schedules.retrieve(
            upload_schedule_id="upload_schedule_id",
            knowledge_base_id="knowledge_base_id",
            view=["DataSource"],
        )
        assert_matches_type(UploadScheduleWithViews, upload_schedule, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.knowledge_bases.upload_schedules.with_raw_response.retrieve(
            upload_schedule_id="upload_schedule_id",
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload_schedule = response.parse()
        assert_matches_type(UploadScheduleWithViews, upload_schedule, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.knowledge_bases.upload_schedules.with_streaming_response.retrieve(
            upload_schedule_id="upload_schedule_id",
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload_schedule = response.parse()
            assert_matches_type(UploadScheduleWithViews, upload_schedule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.upload_schedules.with_raw_response.retrieve(
                upload_schedule_id="upload_schedule_id",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `upload_schedule_id` but received ''"):
            client.knowledge_bases.upload_schedules.with_raw_response.retrieve(
                upload_schedule_id="",
                knowledge_base_id="knowledge_base_id",
            )

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        upload_schedule = client.knowledge_bases.upload_schedules.update(
            upload_schedule_id="upload_schedule_id",
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(UploadSchedule, upload_schedule, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGPClient) -> None:
        upload_schedule = client.knowledge_bases.upload_schedules.update(
            upload_schedule_id="upload_schedule_id",
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config={
                "strategy": "character",
                "chunk_overlap": 0,
                "chunk_size": 1,
                "separator": "separator",
            },
            interval=0,
            next_run_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(UploadSchedule, upload_schedule, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.knowledge_bases.upload_schedules.with_raw_response.update(
            upload_schedule_id="upload_schedule_id",
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload_schedule = response.parse()
        assert_matches_type(UploadSchedule, upload_schedule, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.knowledge_bases.upload_schedules.with_streaming_response.update(
            upload_schedule_id="upload_schedule_id",
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload_schedule = response.parse()
            assert_matches_type(UploadSchedule, upload_schedule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.upload_schedules.with_raw_response.update(
                upload_schedule_id="upload_schedule_id",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `upload_schedule_id` but received ''"):
            client.knowledge_bases.upload_schedules.with_raw_response.update(
                upload_schedule_id="",
                knowledge_base_id="knowledge_base_id",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        upload_schedule = client.knowledge_bases.upload_schedules.list(
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(SyncPageResponse[UploadScheduleWithViews], upload_schedule, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        upload_schedule = client.knowledge_bases.upload_schedules.list(
            knowledge_base_id="knowledge_base_id",
            account_id="account_id",
            limit=1,
            page=1,
            view=["DataSource"],
        )
        assert_matches_type(SyncPageResponse[UploadScheduleWithViews], upload_schedule, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.knowledge_bases.upload_schedules.with_raw_response.list(
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload_schedule = response.parse()
        assert_matches_type(SyncPageResponse[UploadScheduleWithViews], upload_schedule, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.knowledge_bases.upload_schedules.with_streaming_response.list(
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload_schedule = response.parse()
            assert_matches_type(SyncPageResponse[UploadScheduleWithViews], upload_schedule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.upload_schedules.with_raw_response.list(
                knowledge_base_id="",
            )

    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        upload_schedule = client.knowledge_bases.upload_schedules.delete(
            upload_schedule_id="upload_schedule_id",
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(GenericDeleteResponse, upload_schedule, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.knowledge_bases.upload_schedules.with_raw_response.delete(
            upload_schedule_id="upload_schedule_id",
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload_schedule = response.parse()
        assert_matches_type(GenericDeleteResponse, upload_schedule, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.knowledge_bases.upload_schedules.with_streaming_response.delete(
            upload_schedule_id="upload_schedule_id",
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload_schedule = response.parse()
            assert_matches_type(GenericDeleteResponse, upload_schedule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.upload_schedules.with_raw_response.delete(
                upload_schedule_id="upload_schedule_id",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `upload_schedule_id` but received ''"):
            client.knowledge_bases.upload_schedules.with_raw_response.delete(
                upload_schedule_id="",
                knowledge_base_id="knowledge_base_id",
            )


class TestAsyncUploadSchedules:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        upload_schedule = await async_client.knowledge_bases.upload_schedules.create(
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config={"strategy": "character"},
            interval=0,
            knowledge_base_data_source_id="knowledge_base_data_source_id",
        )
        assert_matches_type(UploadSchedule, upload_schedule, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        upload_schedule = await async_client.knowledge_bases.upload_schedules.create(
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config={
                "strategy": "character",
                "chunk_overlap": 0,
                "chunk_size": 1,
                "separator": "separator",
            },
            interval=0,
            knowledge_base_data_source_id="knowledge_base_data_source_id",
            account_id="account_id",
            next_run_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(UploadSchedule, upload_schedule, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.upload_schedules.with_raw_response.create(
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config={"strategy": "character"},
            interval=0,
            knowledge_base_data_source_id="knowledge_base_data_source_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload_schedule = await response.parse()
        assert_matches_type(UploadSchedule, upload_schedule, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.upload_schedules.with_streaming_response.create(
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config={"strategy": "character"},
            interval=0,
            knowledge_base_data_source_id="knowledge_base_data_source_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload_schedule = await response.parse()
            assert_matches_type(UploadSchedule, upload_schedule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.upload_schedules.with_raw_response.create(
                knowledge_base_id="",
                chunking_strategy_config={"strategy": "character"},
                interval=0,
                knowledge_base_data_source_id="knowledge_base_data_source_id",
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        upload_schedule = await async_client.knowledge_bases.upload_schedules.retrieve(
            upload_schedule_id="upload_schedule_id",
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(UploadScheduleWithViews, upload_schedule, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGPClient) -> None:
        upload_schedule = await async_client.knowledge_bases.upload_schedules.retrieve(
            upload_schedule_id="upload_schedule_id",
            knowledge_base_id="knowledge_base_id",
            view=["DataSource"],
        )
        assert_matches_type(UploadScheduleWithViews, upload_schedule, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.upload_schedules.with_raw_response.retrieve(
            upload_schedule_id="upload_schedule_id",
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload_schedule = await response.parse()
        assert_matches_type(UploadScheduleWithViews, upload_schedule, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.upload_schedules.with_streaming_response.retrieve(
            upload_schedule_id="upload_schedule_id",
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload_schedule = await response.parse()
            assert_matches_type(UploadScheduleWithViews, upload_schedule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.upload_schedules.with_raw_response.retrieve(
                upload_schedule_id="upload_schedule_id",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `upload_schedule_id` but received ''"):
            await async_client.knowledge_bases.upload_schedules.with_raw_response.retrieve(
                upload_schedule_id="",
                knowledge_base_id="knowledge_base_id",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        upload_schedule = await async_client.knowledge_bases.upload_schedules.update(
            upload_schedule_id="upload_schedule_id",
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(UploadSchedule, upload_schedule, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        upload_schedule = await async_client.knowledge_bases.upload_schedules.update(
            upload_schedule_id="upload_schedule_id",
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config={
                "strategy": "character",
                "chunk_overlap": 0,
                "chunk_size": 1,
                "separator": "separator",
            },
            interval=0,
            next_run_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(UploadSchedule, upload_schedule, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.upload_schedules.with_raw_response.update(
            upload_schedule_id="upload_schedule_id",
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload_schedule = await response.parse()
        assert_matches_type(UploadSchedule, upload_schedule, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.upload_schedules.with_streaming_response.update(
            upload_schedule_id="upload_schedule_id",
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload_schedule = await response.parse()
            assert_matches_type(UploadSchedule, upload_schedule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.upload_schedules.with_raw_response.update(
                upload_schedule_id="upload_schedule_id",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `upload_schedule_id` but received ''"):
            await async_client.knowledge_bases.upload_schedules.with_raw_response.update(
                upload_schedule_id="",
                knowledge_base_id="knowledge_base_id",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        upload_schedule = await async_client.knowledge_bases.upload_schedules.list(
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(AsyncPageResponse[UploadScheduleWithViews], upload_schedule, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        upload_schedule = await async_client.knowledge_bases.upload_schedules.list(
            knowledge_base_id="knowledge_base_id",
            account_id="account_id",
            limit=1,
            page=1,
            view=["DataSource"],
        )
        assert_matches_type(AsyncPageResponse[UploadScheduleWithViews], upload_schedule, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.upload_schedules.with_raw_response.list(
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload_schedule = await response.parse()
        assert_matches_type(AsyncPageResponse[UploadScheduleWithViews], upload_schedule, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.upload_schedules.with_streaming_response.list(
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload_schedule = await response.parse()
            assert_matches_type(AsyncPageResponse[UploadScheduleWithViews], upload_schedule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.upload_schedules.with_raw_response.list(
                knowledge_base_id="",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        upload_schedule = await async_client.knowledge_bases.upload_schedules.delete(
            upload_schedule_id="upload_schedule_id",
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(GenericDeleteResponse, upload_schedule, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.upload_schedules.with_raw_response.delete(
            upload_schedule_id="upload_schedule_id",
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload_schedule = await response.parse()
        assert_matches_type(GenericDeleteResponse, upload_schedule, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.upload_schedules.with_streaming_response.delete(
            upload_schedule_id="upload_schedule_id",
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload_schedule = await response.parse()
            assert_matches_type(GenericDeleteResponse, upload_schedule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.upload_schedules.with_raw_response.delete(
                upload_schedule_id="upload_schedule_id",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `upload_schedule_id` but received ''"):
            await async_client.knowledge_bases.upload_schedules.with_raw_response.delete(
                upload_schedule_id="",
                knowledge_base_id="knowledge_base_id",
            )
