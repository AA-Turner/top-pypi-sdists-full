# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import TrainingDataset
from scale_gp.pagination import SyncPageResponse, AsyncPageResponse
from scale_gp.types.shared import GenericDeleteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTrainingDatasets:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="prism_binary_unsupported")
    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        training_dataset = client.training_datasets.create(
            account_id="account_id",
            file=b"raw file contents",
            name="name",
            schema_type="GENERATION",
        )
        assert_matches_type(TrainingDataset, training_dataset, path=["response"])

    @pytest.mark.skip(reason="prism_binary_unsupported")
    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.training_datasets.with_raw_response.create(
            account_id="account_id",
            file=b"raw file contents",
            name="name",
            schema_type="GENERATION",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        training_dataset = response.parse()
        assert_matches_type(TrainingDataset, training_dataset, path=["response"])

    @pytest.mark.skip(reason="prism_binary_unsupported")
    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.training_datasets.with_streaming_response.create(
            account_id="account_id",
            file=b"raw file contents",
            name="name",
            schema_type="GENERATION",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            training_dataset = response.parse()
            assert_matches_type(TrainingDataset, training_dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        training_dataset = client.training_datasets.retrieve(
            "training_dataset_id",
        )
        assert_matches_type(TrainingDataset, training_dataset, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.training_datasets.with_raw_response.retrieve(
            "training_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        training_dataset = response.parse()
        assert_matches_type(TrainingDataset, training_dataset, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.training_datasets.with_streaming_response.retrieve(
            "training_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            training_dataset = response.parse()
            assert_matches_type(TrainingDataset, training_dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `training_dataset_id` but received ''"):
            client.training_datasets.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        training_dataset = client.training_datasets.list()
        assert_matches_type(SyncPageResponse[TrainingDataset], training_dataset, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        training_dataset = client.training_datasets.list(
            account_id=0,
            limit=1,
            page=1,
        )
        assert_matches_type(SyncPageResponse[TrainingDataset], training_dataset, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.training_datasets.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        training_dataset = response.parse()
        assert_matches_type(SyncPageResponse[TrainingDataset], training_dataset, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.training_datasets.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            training_dataset = response.parse()
            assert_matches_type(SyncPageResponse[TrainingDataset], training_dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        training_dataset = client.training_datasets.delete(
            "training_dataset_id",
        )
        assert_matches_type(GenericDeleteResponse, training_dataset, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.training_datasets.with_raw_response.delete(
            "training_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        training_dataset = response.parse()
        assert_matches_type(GenericDeleteResponse, training_dataset, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.training_datasets.with_streaming_response.delete(
            "training_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            training_dataset = response.parse()
            assert_matches_type(GenericDeleteResponse, training_dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `training_dataset_id` but received ''"):
            client.training_datasets.with_raw_response.delete(
                "",
            )


class TestAsyncTrainingDatasets:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="prism_binary_unsupported")
    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        training_dataset = await async_client.training_datasets.create(
            account_id="account_id",
            file=b"raw file contents",
            name="name",
            schema_type="GENERATION",
        )
        assert_matches_type(TrainingDataset, training_dataset, path=["response"])

    @pytest.mark.skip(reason="prism_binary_unsupported")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.training_datasets.with_raw_response.create(
            account_id="account_id",
            file=b"raw file contents",
            name="name",
            schema_type="GENERATION",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        training_dataset = await response.parse()
        assert_matches_type(TrainingDataset, training_dataset, path=["response"])

    @pytest.mark.skip(reason="prism_binary_unsupported")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.training_datasets.with_streaming_response.create(
            account_id="account_id",
            file=b"raw file contents",
            name="name",
            schema_type="GENERATION",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            training_dataset = await response.parse()
            assert_matches_type(TrainingDataset, training_dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        training_dataset = await async_client.training_datasets.retrieve(
            "training_dataset_id",
        )
        assert_matches_type(TrainingDataset, training_dataset, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.training_datasets.with_raw_response.retrieve(
            "training_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        training_dataset = await response.parse()
        assert_matches_type(TrainingDataset, training_dataset, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.training_datasets.with_streaming_response.retrieve(
            "training_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            training_dataset = await response.parse()
            assert_matches_type(TrainingDataset, training_dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `training_dataset_id` but received ''"):
            await async_client.training_datasets.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        training_dataset = await async_client.training_datasets.list()
        assert_matches_type(AsyncPageResponse[TrainingDataset], training_dataset, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        training_dataset = await async_client.training_datasets.list(
            account_id=0,
            limit=1,
            page=1,
        )
        assert_matches_type(AsyncPageResponse[TrainingDataset], training_dataset, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.training_datasets.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        training_dataset = await response.parse()
        assert_matches_type(AsyncPageResponse[TrainingDataset], training_dataset, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.training_datasets.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            training_dataset = await response.parse()
            assert_matches_type(AsyncPageResponse[TrainingDataset], training_dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        training_dataset = await async_client.training_datasets.delete(
            "training_dataset_id",
        )
        assert_matches_type(GenericDeleteResponse, training_dataset, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.training_datasets.with_raw_response.delete(
            "training_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        training_dataset = await response.parse()
        assert_matches_type(GenericDeleteResponse, training_dataset, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.training_datasets.with_streaming_response.delete(
            "training_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            training_dataset = await response.parse()
            assert_matches_type(GenericDeleteResponse, training_dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `training_dataset_id` but received ''"):
            await async_client.training_datasets.with_raw_response.delete(
                "",
            )
