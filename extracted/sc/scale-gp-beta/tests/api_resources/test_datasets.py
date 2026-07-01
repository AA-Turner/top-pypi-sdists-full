# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from scale_gp_beta import SGPClient, AsyncSGPClient
from scale_gp_beta.types import (
    Dataset,
    DatasetArchiveResponse,
)
from scale_gp_beta.pagination import SyncCursorPage, AsyncCursorPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDatasets:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        dataset = client.datasets.create(
            data=[{"foo": "bar"}],
            name="name",
        )
        assert_matches_type(Dataset, dataset, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        dataset = client.datasets.create(
            data=[{"foo": "bar"}],
            name="name",
            description="description",
            files=[{"foo": "string"}],
            tags=["string"],
        )
        assert_matches_type(Dataset, dataset, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.datasets.with_raw_response.create(
            data=[{"foo": "bar"}],
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(Dataset, dataset, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.datasets.with_streaming_response.create(
            data=[{"foo": "bar"}],
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(Dataset, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        dataset = client.datasets.retrieve(
            dataset_id="dataset_id",
        )
        assert_matches_type(Dataset, dataset, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGPClient) -> None:
        dataset = client.datasets.retrieve(
            dataset_id="dataset_id",
            include_archived=True,
        )
        assert_matches_type(Dataset, dataset, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.datasets.with_raw_response.retrieve(
            dataset_id="dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(Dataset, dataset, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.datasets.with_streaming_response.retrieve(
            dataset_id="dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(Dataset, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_id` but received ''"):
            client.datasets.with_raw_response.retrieve(
                dataset_id="",
            )

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        dataset = client.datasets.update(
            dataset_id="dataset_id",
            dataset={},
        )
        assert_matches_type(Dataset, dataset, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGPClient) -> None:
        dataset = client.datasets.update(
            dataset_id="dataset_id",
            dataset={
                "description": "description",
                "name": "name",
                "tags": ["string"],
            },
        )
        assert_matches_type(Dataset, dataset, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.datasets.with_raw_response.update(
            dataset_id="dataset_id",
            dataset={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(Dataset, dataset, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.datasets.with_streaming_response.update(
            dataset_id="dataset_id",
            dataset={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(Dataset, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_id` but received ''"):
            client.datasets.with_raw_response.update(
                dataset_id="",
                dataset={},
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        dataset = client.datasets.list()
        assert_matches_type(SyncCursorPage[Dataset], dataset, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        dataset = client.datasets.list(
            ending_before="ending_before",
            include_archived=True,
            limit=1,
            name="name",
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
            tags=["string"],
        )
        assert_matches_type(SyncCursorPage[Dataset], dataset, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.datasets.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(SyncCursorPage[Dataset], dataset, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.datasets.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(SyncCursorPage[Dataset], dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_archive(self, client: SGPClient) -> None:
        dataset = client.datasets.archive(
            "dataset_id",
        )
        assert_matches_type(DatasetArchiveResponse, dataset, path=["response"])

    @parametrize
    def test_raw_response_archive(self, client: SGPClient) -> None:
        response = client.datasets.with_raw_response.archive(
            "dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(DatasetArchiveResponse, dataset, path=["response"])

    @parametrize
    def test_streaming_response_archive(self, client: SGPClient) -> None:
        with client.datasets.with_streaming_response.archive(
            "dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(DatasetArchiveResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_archive(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_id` but received ''"):
            client.datasets.with_raw_response.archive(
                "",
            )


class TestAsyncDatasets:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        dataset = await async_client.datasets.create(
            data=[{"foo": "bar"}],
            name="name",
        )
        assert_matches_type(Dataset, dataset, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        dataset = await async_client.datasets.create(
            data=[{"foo": "bar"}],
            name="name",
            description="description",
            files=[{"foo": "string"}],
            tags=["string"],
        )
        assert_matches_type(Dataset, dataset, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.datasets.with_raw_response.create(
            data=[{"foo": "bar"}],
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(Dataset, dataset, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.datasets.with_streaming_response.create(
            data=[{"foo": "bar"}],
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(Dataset, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        dataset = await async_client.datasets.retrieve(
            dataset_id="dataset_id",
        )
        assert_matches_type(Dataset, dataset, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGPClient) -> None:
        dataset = await async_client.datasets.retrieve(
            dataset_id="dataset_id",
            include_archived=True,
        )
        assert_matches_type(Dataset, dataset, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.datasets.with_raw_response.retrieve(
            dataset_id="dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(Dataset, dataset, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.datasets.with_streaming_response.retrieve(
            dataset_id="dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(Dataset, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_id` but received ''"):
            await async_client.datasets.with_raw_response.retrieve(
                dataset_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        dataset = await async_client.datasets.update(
            dataset_id="dataset_id",
            dataset={},
        )
        assert_matches_type(Dataset, dataset, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        dataset = await async_client.datasets.update(
            dataset_id="dataset_id",
            dataset={
                "description": "description",
                "name": "name",
                "tags": ["string"],
            },
        )
        assert_matches_type(Dataset, dataset, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.datasets.with_raw_response.update(
            dataset_id="dataset_id",
            dataset={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(Dataset, dataset, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.datasets.with_streaming_response.update(
            dataset_id="dataset_id",
            dataset={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(Dataset, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_id` but received ''"):
            await async_client.datasets.with_raw_response.update(
                dataset_id="",
                dataset={},
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        dataset = await async_client.datasets.list()
        assert_matches_type(AsyncCursorPage[Dataset], dataset, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        dataset = await async_client.datasets.list(
            ending_before="ending_before",
            include_archived=True,
            limit=1,
            name="name",
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
            tags=["string"],
        )
        assert_matches_type(AsyncCursorPage[Dataset], dataset, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.datasets.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(AsyncCursorPage[Dataset], dataset, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.datasets.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(AsyncCursorPage[Dataset], dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_archive(self, async_client: AsyncSGPClient) -> None:
        dataset = await async_client.datasets.archive(
            "dataset_id",
        )
        assert_matches_type(DatasetArchiveResponse, dataset, path=["response"])

    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.datasets.with_raw_response.archive(
            "dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(DatasetArchiveResponse, dataset, path=["response"])

    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncSGPClient) -> None:
        async with async_client.datasets.with_streaming_response.archive(
            "dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(DatasetArchiveResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_id` but received ''"):
            await async_client.datasets.with_raw_response.archive(
                "",
            )
