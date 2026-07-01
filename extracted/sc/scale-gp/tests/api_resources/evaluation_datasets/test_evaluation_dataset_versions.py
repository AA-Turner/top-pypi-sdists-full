# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import PublishEvaluationDatasetDraftResponse
from scale_gp._utils import parse_datetime
from scale_gp.pagination import SyncPageResponse, AsyncPageResponse
from scale_gp.types.evaluation_datasets import (
    EvaluationDatasetVersion,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEvaluationDatasetVersions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        evaluation_dataset_version = client.evaluation_datasets.evaluation_dataset_versions.create(
            evaluation_dataset_id="evaluation_dataset_id",
        )
        assert_matches_type(EvaluationDatasetVersion, evaluation_dataset_version, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        evaluation_dataset_version = client.evaluation_datasets.evaluation_dataset_versions.create(
            evaluation_dataset_id="evaluation_dataset_id",
            account_id="account_id",
            draft=True,
            published_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(EvaluationDatasetVersion, evaluation_dataset_version, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.create(
            evaluation_dataset_id="evaluation_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_dataset_version = response.parse()
        assert_matches_type(EvaluationDatasetVersion, evaluation_dataset_version, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.evaluation_datasets.evaluation_dataset_versions.with_streaming_response.create(
            evaluation_dataset_id="evaluation_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_dataset_version = response.parse()
            assert_matches_type(EvaluationDatasetVersion, evaluation_dataset_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.create(
                evaluation_dataset_id="",
            )

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        evaluation_dataset_version = client.evaluation_datasets.evaluation_dataset_versions.retrieve(
            evaluation_dataset_version_id="evaluation_dataset_version_id",
            evaluation_dataset_id="evaluation_dataset_id",
        )
        assert_matches_type(EvaluationDatasetVersion, evaluation_dataset_version, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.retrieve(
            evaluation_dataset_version_id="evaluation_dataset_version_id",
            evaluation_dataset_id="evaluation_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_dataset_version = response.parse()
        assert_matches_type(EvaluationDatasetVersion, evaluation_dataset_version, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.evaluation_datasets.evaluation_dataset_versions.with_streaming_response.retrieve(
            evaluation_dataset_version_id="evaluation_dataset_version_id",
            evaluation_dataset_id="evaluation_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_dataset_version = response.parse()
            assert_matches_type(EvaluationDatasetVersion, evaluation_dataset_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.retrieve(
                evaluation_dataset_version_id="evaluation_dataset_version_id",
                evaluation_dataset_id="",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `evaluation_dataset_version_id` but received ''"
        ):
            client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.retrieve(
                evaluation_dataset_version_id="",
                evaluation_dataset_id="evaluation_dataset_id",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        evaluation_dataset_version = client.evaluation_datasets.evaluation_dataset_versions.list(
            evaluation_dataset_id="evaluation_dataset_id",
        )
        assert_matches_type(SyncPageResponse[EvaluationDatasetVersion], evaluation_dataset_version, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        evaluation_dataset_version = client.evaluation_datasets.evaluation_dataset_versions.list(
            evaluation_dataset_id="evaluation_dataset_id",
            account_id="account_id",
            include_archived=True,
            limit=1,
            page=1,
        )
        assert_matches_type(SyncPageResponse[EvaluationDatasetVersion], evaluation_dataset_version, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.list(
            evaluation_dataset_id="evaluation_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_dataset_version = response.parse()
        assert_matches_type(SyncPageResponse[EvaluationDatasetVersion], evaluation_dataset_version, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.evaluation_datasets.evaluation_dataset_versions.with_streaming_response.list(
            evaluation_dataset_id="evaluation_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_dataset_version = response.parse()
            assert_matches_type(
                SyncPageResponse[EvaluationDatasetVersion], evaluation_dataset_version, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.list(
                evaluation_dataset_id="",
            )

    @parametrize
    def test_method_publish(self, client: SGPClient) -> None:
        evaluation_dataset_version = client.evaluation_datasets.evaluation_dataset_versions.publish(
            evaluation_dataset_version_id="evaluation_dataset_version_id",
            evaluation_dataset_id="evaluation_dataset_id",
        )
        assert_matches_type(PublishEvaluationDatasetDraftResponse, evaluation_dataset_version, path=["response"])

    @parametrize
    def test_method_publish_with_all_params(self, client: SGPClient) -> None:
        evaluation_dataset_version = client.evaluation_datasets.evaluation_dataset_versions.publish(
            evaluation_dataset_version_id="evaluation_dataset_version_id",
            evaluation_dataset_id="evaluation_dataset_id",
            force=True,
        )
        assert_matches_type(PublishEvaluationDatasetDraftResponse, evaluation_dataset_version, path=["response"])

    @parametrize
    def test_raw_response_publish(self, client: SGPClient) -> None:
        response = client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.publish(
            evaluation_dataset_version_id="evaluation_dataset_version_id",
            evaluation_dataset_id="evaluation_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_dataset_version = response.parse()
        assert_matches_type(PublishEvaluationDatasetDraftResponse, evaluation_dataset_version, path=["response"])

    @parametrize
    def test_streaming_response_publish(self, client: SGPClient) -> None:
        with client.evaluation_datasets.evaluation_dataset_versions.with_streaming_response.publish(
            evaluation_dataset_version_id="evaluation_dataset_version_id",
            evaluation_dataset_id="evaluation_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_dataset_version = response.parse()
            assert_matches_type(PublishEvaluationDatasetDraftResponse, evaluation_dataset_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_publish(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.publish(
                evaluation_dataset_version_id="evaluation_dataset_version_id",
                evaluation_dataset_id="",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `evaluation_dataset_version_id` but received ''"
        ):
            client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.publish(
                evaluation_dataset_version_id="",
                evaluation_dataset_id="evaluation_dataset_id",
            )


class TestAsyncEvaluationDatasetVersions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        evaluation_dataset_version = await async_client.evaluation_datasets.evaluation_dataset_versions.create(
            evaluation_dataset_id="evaluation_dataset_id",
        )
        assert_matches_type(EvaluationDatasetVersion, evaluation_dataset_version, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation_dataset_version = await async_client.evaluation_datasets.evaluation_dataset_versions.create(
            evaluation_dataset_id="evaluation_dataset_id",
            account_id="account_id",
            draft=True,
            published_at=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(EvaluationDatasetVersion, evaluation_dataset_version, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.create(
            evaluation_dataset_id="evaluation_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_dataset_version = await response.parse()
        assert_matches_type(EvaluationDatasetVersion, evaluation_dataset_version, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_datasets.evaluation_dataset_versions.with_streaming_response.create(
            evaluation_dataset_id="evaluation_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_dataset_version = await response.parse()
            assert_matches_type(EvaluationDatasetVersion, evaluation_dataset_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.create(
                evaluation_dataset_id="",
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        evaluation_dataset_version = await async_client.evaluation_datasets.evaluation_dataset_versions.retrieve(
            evaluation_dataset_version_id="evaluation_dataset_version_id",
            evaluation_dataset_id="evaluation_dataset_id",
        )
        assert_matches_type(EvaluationDatasetVersion, evaluation_dataset_version, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.retrieve(
            evaluation_dataset_version_id="evaluation_dataset_version_id",
            evaluation_dataset_id="evaluation_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_dataset_version = await response.parse()
        assert_matches_type(EvaluationDatasetVersion, evaluation_dataset_version, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_datasets.evaluation_dataset_versions.with_streaming_response.retrieve(
            evaluation_dataset_version_id="evaluation_dataset_version_id",
            evaluation_dataset_id="evaluation_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_dataset_version = await response.parse()
            assert_matches_type(EvaluationDatasetVersion, evaluation_dataset_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.retrieve(
                evaluation_dataset_version_id="evaluation_dataset_version_id",
                evaluation_dataset_id="",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `evaluation_dataset_version_id` but received ''"
        ):
            await async_client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.retrieve(
                evaluation_dataset_version_id="",
                evaluation_dataset_id="evaluation_dataset_id",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        evaluation_dataset_version = await async_client.evaluation_datasets.evaluation_dataset_versions.list(
            evaluation_dataset_id="evaluation_dataset_id",
        )
        assert_matches_type(AsyncPageResponse[EvaluationDatasetVersion], evaluation_dataset_version, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation_dataset_version = await async_client.evaluation_datasets.evaluation_dataset_versions.list(
            evaluation_dataset_id="evaluation_dataset_id",
            account_id="account_id",
            include_archived=True,
            limit=1,
            page=1,
        )
        assert_matches_type(AsyncPageResponse[EvaluationDatasetVersion], evaluation_dataset_version, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.list(
            evaluation_dataset_id="evaluation_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_dataset_version = await response.parse()
        assert_matches_type(AsyncPageResponse[EvaluationDatasetVersion], evaluation_dataset_version, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_datasets.evaluation_dataset_versions.with_streaming_response.list(
            evaluation_dataset_id="evaluation_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_dataset_version = await response.parse()
            assert_matches_type(
                AsyncPageResponse[EvaluationDatasetVersion], evaluation_dataset_version, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.list(
                evaluation_dataset_id="",
            )

    @parametrize
    async def test_method_publish(self, async_client: AsyncSGPClient) -> None:
        evaluation_dataset_version = await async_client.evaluation_datasets.evaluation_dataset_versions.publish(
            evaluation_dataset_version_id="evaluation_dataset_version_id",
            evaluation_dataset_id="evaluation_dataset_id",
        )
        assert_matches_type(PublishEvaluationDatasetDraftResponse, evaluation_dataset_version, path=["response"])

    @parametrize
    async def test_method_publish_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation_dataset_version = await async_client.evaluation_datasets.evaluation_dataset_versions.publish(
            evaluation_dataset_version_id="evaluation_dataset_version_id",
            evaluation_dataset_id="evaluation_dataset_id",
            force=True,
        )
        assert_matches_type(PublishEvaluationDatasetDraftResponse, evaluation_dataset_version, path=["response"])

    @parametrize
    async def test_raw_response_publish(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.publish(
            evaluation_dataset_version_id="evaluation_dataset_version_id",
            evaluation_dataset_id="evaluation_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_dataset_version = await response.parse()
        assert_matches_type(PublishEvaluationDatasetDraftResponse, evaluation_dataset_version, path=["response"])

    @parametrize
    async def test_streaming_response_publish(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_datasets.evaluation_dataset_versions.with_streaming_response.publish(
            evaluation_dataset_version_id="evaluation_dataset_version_id",
            evaluation_dataset_id="evaluation_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_dataset_version = await response.parse()
            assert_matches_type(PublishEvaluationDatasetDraftResponse, evaluation_dataset_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_publish(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.publish(
                evaluation_dataset_version_id="evaluation_dataset_version_id",
                evaluation_dataset_id="",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `evaluation_dataset_version_id` but received ''"
        ):
            await async_client.evaluation_datasets.evaluation_dataset_versions.with_raw_response.publish(
                evaluation_dataset_version_id="",
                evaluation_dataset_id="evaluation_dataset_id",
            )
