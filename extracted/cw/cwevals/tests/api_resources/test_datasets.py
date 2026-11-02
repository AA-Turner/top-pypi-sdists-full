# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from coreweave_evaluations import Client, AsyncClient
from coreweave_evaluations.types import DatasetGetResponse, DatasetCreateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDatasets:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Client) -> None:
        dataset = client.datasets.create(
            namespace="wandb",
            scope_id="scope_id",
            name="x",
        )
        assert_matches_type(DatasetCreateResponse, dataset, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Client) -> None:
        dataset = client.datasets.create(
            namespace="wandb",
            scope_id="scope_id",
            name="x",
            attributes={"foo": "bar"},
            uri="https://example.com",
        )
        assert_matches_type(DatasetCreateResponse, dataset, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Client) -> None:
        response = client.datasets.with_raw_response.create(
            namespace="wandb",
            scope_id="scope_id",
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(DatasetCreateResponse, dataset, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Client) -> None:
        with client.datasets.with_streaming_response.create(
            namespace="wandb",
            scope_id="scope_id",
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(DatasetCreateResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Client) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.datasets.with_raw_response.create(
                namespace="",
                scope_id="scope_id",
                name="x",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            client.datasets.with_raw_response.create(
                namespace="wandb",
                scope_id="",
                name="x",
            )

    @parametrize
    def test_method_get(self, client: Client) -> None:
        dataset = client.datasets.get(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )
        assert_matches_type(DatasetGetResponse, dataset, path=["response"])

    @parametrize
    def test_raw_response_get(self, client: Client) -> None:
        response = client.datasets.with_raw_response.get(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(DatasetGetResponse, dataset, path=["response"])

    @parametrize
    def test_streaming_response_get(self, client: Client) -> None:
        with client.datasets.with_streaming_response.get(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(DatasetGetResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_get(self, client: Client) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.datasets.with_raw_response.get(
                dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            client.datasets.with_raw_response.get(
                dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_id` but received ''"):
            client.datasets.with_raw_response.get(
                dataset_id="",
                namespace="wandb",
                scope_id="scope_id",
            )


class TestAsyncDatasets:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncClient) -> None:
        dataset = await async_client.datasets.create(
            namespace="wandb",
            scope_id="scope_id",
            name="x",
        )
        assert_matches_type(DatasetCreateResponse, dataset, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncClient) -> None:
        dataset = await async_client.datasets.create(
            namespace="wandb",
            scope_id="scope_id",
            name="x",
            attributes={"foo": "bar"},
            uri="https://example.com",
        )
        assert_matches_type(DatasetCreateResponse, dataset, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncClient) -> None:
        response = await async_client.datasets.with_raw_response.create(
            namespace="wandb",
            scope_id="scope_id",
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(DatasetCreateResponse, dataset, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncClient) -> None:
        async with async_client.datasets.with_streaming_response.create(
            namespace="wandb",
            scope_id="scope_id",
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(DatasetCreateResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.datasets.with_raw_response.create(
                namespace="",
                scope_id="scope_id",
                name="x",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            await async_client.datasets.with_raw_response.create(
                namespace="wandb",
                scope_id="",
                name="x",
            )

    @parametrize
    async def test_method_get(self, async_client: AsyncClient) -> None:
        dataset = await async_client.datasets.get(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )
        assert_matches_type(DatasetGetResponse, dataset, path=["response"])

    @parametrize
    async def test_raw_response_get(self, async_client: AsyncClient) -> None:
        response = await async_client.datasets.with_raw_response.get(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(DatasetGetResponse, dataset, path=["response"])

    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncClient) -> None:
        async with async_client.datasets.with_streaming_response.get(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(DatasetGetResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_get(self, async_client: AsyncClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.datasets.with_raw_response.get(
                dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            await async_client.datasets.with_raw_response.get(
                dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_id` but received ''"):
            await async_client.datasets.with_raw_response.get(
                dataset_id="",
                namespace="wandb",
                scope_id="scope_id",
            )
