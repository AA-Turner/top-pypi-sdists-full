# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from scale_gp_beta import SGPClient, AsyncSGPClient
from scale_gp_beta.types import (
    DatasetItem,
    DatasetItemArchiveResponse,
    DatasetItemBatchCreateResponse,
)
from scale_gp_beta.pagination import SyncCursorPage, AsyncCursorPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDatasetItems:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        dataset_item = client.dataset_items.retrieve(
            dataset_item_id="dataset_item_id",
        )
        assert_matches_type(DatasetItem, dataset_item, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGPClient) -> None:
        dataset_item = client.dataset_items.retrieve(
            dataset_item_id="dataset_item_id",
            version=0,
        )
        assert_matches_type(DatasetItem, dataset_item, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.dataset_items.with_raw_response.retrieve(
            dataset_item_id="dataset_item_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset_item = response.parse()
        assert_matches_type(DatasetItem, dataset_item, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.dataset_items.with_streaming_response.retrieve(
            dataset_item_id="dataset_item_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset_item = response.parse()
            assert_matches_type(DatasetItem, dataset_item, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_item_id` but received ''"):
            client.dataset_items.with_raw_response.retrieve(
                dataset_item_id="",
            )

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        dataset_item = client.dataset_items.update(
            dataset_item_id="dataset_item_id",
            data={"foo": "bar"},
        )
        assert_matches_type(DatasetItem, dataset_item, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGPClient) -> None:
        dataset_item = client.dataset_items.update(
            dataset_item_id="dataset_item_id",
            data={"foo": "bar"},
            files={"foo": "string"},
        )
        assert_matches_type(DatasetItem, dataset_item, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.dataset_items.with_raw_response.update(
            dataset_item_id="dataset_item_id",
            data={"foo": "bar"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset_item = response.parse()
        assert_matches_type(DatasetItem, dataset_item, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.dataset_items.with_streaming_response.update(
            dataset_item_id="dataset_item_id",
            data={"foo": "bar"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset_item = response.parse()
            assert_matches_type(DatasetItem, dataset_item, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_item_id` but received ''"):
            client.dataset_items.with_raw_response.update(
                dataset_item_id="",
                data={"foo": "bar"},
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        dataset_item = client.dataset_items.list()
        assert_matches_type(SyncCursorPage[DatasetItem], dataset_item, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        dataset_item = client.dataset_items.list(
            dataset_id="dataset_id",
            ending_before="ending_before",
            include_archived=True,
            limit=1,
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
            version=0,
        )
        assert_matches_type(SyncCursorPage[DatasetItem], dataset_item, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.dataset_items.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset_item = response.parse()
        assert_matches_type(SyncCursorPage[DatasetItem], dataset_item, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.dataset_items.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset_item = response.parse()
            assert_matches_type(SyncCursorPage[DatasetItem], dataset_item, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_archive(self, client: SGPClient) -> None:
        dataset_item = client.dataset_items.archive(
            "dataset_item_id",
        )
        assert_matches_type(DatasetItemArchiveResponse, dataset_item, path=["response"])

    @parametrize
    def test_raw_response_archive(self, client: SGPClient) -> None:
        response = client.dataset_items.with_raw_response.archive(
            "dataset_item_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset_item = response.parse()
        assert_matches_type(DatasetItemArchiveResponse, dataset_item, path=["response"])

    @parametrize
    def test_streaming_response_archive(self, client: SGPClient) -> None:
        with client.dataset_items.with_streaming_response.archive(
            "dataset_item_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset_item = response.parse()
            assert_matches_type(DatasetItemArchiveResponse, dataset_item, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_archive(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_item_id` but received ''"):
            client.dataset_items.with_raw_response.archive(
                "",
            )

    @parametrize
    def test_method_batch_create(self, client: SGPClient) -> None:
        dataset_item = client.dataset_items.batch_create(
            data=[{"foo": "bar"}],
            dataset_id="dataset_id",
        )
        assert_matches_type(DatasetItemBatchCreateResponse, dataset_item, path=["response"])

    @parametrize
    def test_method_batch_create_with_all_params(self, client: SGPClient) -> None:
        dataset_item = client.dataset_items.batch_create(
            data=[{"foo": "bar"}],
            dataset_id="dataset_id",
            files=[{"foo": "string"}],
        )
        assert_matches_type(DatasetItemBatchCreateResponse, dataset_item, path=["response"])

    @parametrize
    def test_raw_response_batch_create(self, client: SGPClient) -> None:
        response = client.dataset_items.with_raw_response.batch_create(
            data=[{"foo": "bar"}],
            dataset_id="dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset_item = response.parse()
        assert_matches_type(DatasetItemBatchCreateResponse, dataset_item, path=["response"])

    @parametrize
    def test_streaming_response_batch_create(self, client: SGPClient) -> None:
        with client.dataset_items.with_streaming_response.batch_create(
            data=[{"foo": "bar"}],
            dataset_id="dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset_item = response.parse()
            assert_matches_type(DatasetItemBatchCreateResponse, dataset_item, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDatasetItems:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        dataset_item = await async_client.dataset_items.retrieve(
            dataset_item_id="dataset_item_id",
        )
        assert_matches_type(DatasetItem, dataset_item, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGPClient) -> None:
        dataset_item = await async_client.dataset_items.retrieve(
            dataset_item_id="dataset_item_id",
            version=0,
        )
        assert_matches_type(DatasetItem, dataset_item, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.dataset_items.with_raw_response.retrieve(
            dataset_item_id="dataset_item_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset_item = await response.parse()
        assert_matches_type(DatasetItem, dataset_item, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.dataset_items.with_streaming_response.retrieve(
            dataset_item_id="dataset_item_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset_item = await response.parse()
            assert_matches_type(DatasetItem, dataset_item, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_item_id` but received ''"):
            await async_client.dataset_items.with_raw_response.retrieve(
                dataset_item_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        dataset_item = await async_client.dataset_items.update(
            dataset_item_id="dataset_item_id",
            data={"foo": "bar"},
        )
        assert_matches_type(DatasetItem, dataset_item, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        dataset_item = await async_client.dataset_items.update(
            dataset_item_id="dataset_item_id",
            data={"foo": "bar"},
            files={"foo": "string"},
        )
        assert_matches_type(DatasetItem, dataset_item, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.dataset_items.with_raw_response.update(
            dataset_item_id="dataset_item_id",
            data={"foo": "bar"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset_item = await response.parse()
        assert_matches_type(DatasetItem, dataset_item, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.dataset_items.with_streaming_response.update(
            dataset_item_id="dataset_item_id",
            data={"foo": "bar"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset_item = await response.parse()
            assert_matches_type(DatasetItem, dataset_item, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_item_id` but received ''"):
            await async_client.dataset_items.with_raw_response.update(
                dataset_item_id="",
                data={"foo": "bar"},
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        dataset_item = await async_client.dataset_items.list()
        assert_matches_type(AsyncCursorPage[DatasetItem], dataset_item, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        dataset_item = await async_client.dataset_items.list(
            dataset_id="dataset_id",
            ending_before="ending_before",
            include_archived=True,
            limit=1,
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
            version=0,
        )
        assert_matches_type(AsyncCursorPage[DatasetItem], dataset_item, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.dataset_items.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset_item = await response.parse()
        assert_matches_type(AsyncCursorPage[DatasetItem], dataset_item, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.dataset_items.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset_item = await response.parse()
            assert_matches_type(AsyncCursorPage[DatasetItem], dataset_item, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_archive(self, async_client: AsyncSGPClient) -> None:
        dataset_item = await async_client.dataset_items.archive(
            "dataset_item_id",
        )
        assert_matches_type(DatasetItemArchiveResponse, dataset_item, path=["response"])

    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.dataset_items.with_raw_response.archive(
            "dataset_item_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset_item = await response.parse()
        assert_matches_type(DatasetItemArchiveResponse, dataset_item, path=["response"])

    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncSGPClient) -> None:
        async with async_client.dataset_items.with_streaming_response.archive(
            "dataset_item_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset_item = await response.parse()
            assert_matches_type(DatasetItemArchiveResponse, dataset_item, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_item_id` but received ''"):
            await async_client.dataset_items.with_raw_response.archive(
                "",
            )

    @parametrize
    async def test_method_batch_create(self, async_client: AsyncSGPClient) -> None:
        dataset_item = await async_client.dataset_items.batch_create(
            data=[{"foo": "bar"}],
            dataset_id="dataset_id",
        )
        assert_matches_type(DatasetItemBatchCreateResponse, dataset_item, path=["response"])

    @parametrize
    async def test_method_batch_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        dataset_item = await async_client.dataset_items.batch_create(
            data=[{"foo": "bar"}],
            dataset_id="dataset_id",
            files=[{"foo": "string"}],
        )
        assert_matches_type(DatasetItemBatchCreateResponse, dataset_item, path=["response"])

    @parametrize
    async def test_raw_response_batch_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.dataset_items.with_raw_response.batch_create(
            data=[{"foo": "bar"}],
            dataset_id="dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset_item = await response.parse()
        assert_matches_type(DatasetItemBatchCreateResponse, dataset_item, path=["response"])

    @parametrize
    async def test_streaming_response_batch_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.dataset_items.with_streaming_response.batch_create(
            data=[{"foo": "bar"}],
            dataset_id="dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset_item = await response.parse()
            assert_matches_type(DatasetItemBatchCreateResponse, dataset_item, path=["response"])

        assert cast(Any, response.is_closed) is True
