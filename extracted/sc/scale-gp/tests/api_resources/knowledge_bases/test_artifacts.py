# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.pagination import SyncPageResponse, AsyncPageResponse
from scale_gp.types.knowledge_bases import (
    Artifact,
    ArtifactDeleteResponse,
    ArtifactUpdateResponse,
    ArtifactBatchDeleteResponse,
)
from scale_gp.types.knowledge_bases.paginated_artifacts import Item

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestArtifacts:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        artifact = client.knowledge_bases.artifacts.retrieve(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(Artifact, artifact, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGPClient) -> None:
        artifact = client.knowledge_bases.artifacts.retrieve(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
            status_filter="status_filter",
        )
        assert_matches_type(Artifact, artifact, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.knowledge_bases.artifacts.with_raw_response.retrieve(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        artifact = response.parse()
        assert_matches_type(Artifact, artifact, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.knowledge_bases.artifacts.with_streaming_response.retrieve(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            artifact = response.parse()
            assert_matches_type(Artifact, artifact, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.artifacts.with_raw_response.retrieve(
                artifact_id="artifact_id",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `artifact_id` but received ''"):
            client.knowledge_bases.artifacts.with_raw_response.retrieve(
                artifact_id="",
                knowledge_base_id="knowledge_base_id",
            )

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        artifact = client.knowledge_bases.artifacts.update(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(ArtifactUpdateResponse, artifact, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGPClient) -> None:
        artifact = client.knowledge_bases.artifacts.update(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
            tags={"foo": "bar"},
        )
        assert_matches_type(ArtifactUpdateResponse, artifact, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.knowledge_bases.artifacts.with_raw_response.update(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        artifact = response.parse()
        assert_matches_type(ArtifactUpdateResponse, artifact, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.knowledge_bases.artifacts.with_streaming_response.update(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            artifact = response.parse()
            assert_matches_type(ArtifactUpdateResponse, artifact, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.artifacts.with_raw_response.update(
                artifact_id="artifact_id",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `artifact_id` but received ''"):
            client.knowledge_bases.artifacts.with_raw_response.update(
                artifact_id="",
                knowledge_base_id="knowledge_base_id",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        artifact = client.knowledge_bases.artifacts.list(
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(SyncPageResponse[Item], artifact, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        artifact = client.knowledge_bases.artifacts.list(
            knowledge_base_id="knowledge_base_id",
            limit=1,
            page=1,
            status="Pending",
        )
        assert_matches_type(SyncPageResponse[Item], artifact, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.knowledge_bases.artifacts.with_raw_response.list(
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        artifact = response.parse()
        assert_matches_type(SyncPageResponse[Item], artifact, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.knowledge_bases.artifacts.with_streaming_response.list(
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            artifact = response.parse()
            assert_matches_type(SyncPageResponse[Item], artifact, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.artifacts.with_raw_response.list(
                knowledge_base_id="",
            )

    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        artifact = client.knowledge_bases.artifacts.delete(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(ArtifactDeleteResponse, artifact, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.knowledge_bases.artifacts.with_raw_response.delete(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        artifact = response.parse()
        assert_matches_type(ArtifactDeleteResponse, artifact, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.knowledge_bases.artifacts.with_streaming_response.delete(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            artifact = response.parse()
            assert_matches_type(ArtifactDeleteResponse, artifact, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.artifacts.with_raw_response.delete(
                artifact_id="artifact_id",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `artifact_id` but received ''"):
            client.knowledge_bases.artifacts.with_raw_response.delete(
                artifact_id="",
                knowledge_base_id="knowledge_base_id",
            )

    @parametrize
    def test_method_batch_delete(self, client: SGPClient) -> None:
        artifact = client.knowledge_bases.artifacts.batch_delete(
            knowledge_base_id="knowledge_base_id",
            artifact_ids=["string"],
        )
        assert_matches_type(ArtifactBatchDeleteResponse, artifact, path=["response"])

    @parametrize
    def test_raw_response_batch_delete(self, client: SGPClient) -> None:
        response = client.knowledge_bases.artifacts.with_raw_response.batch_delete(
            knowledge_base_id="knowledge_base_id",
            artifact_ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        artifact = response.parse()
        assert_matches_type(ArtifactBatchDeleteResponse, artifact, path=["response"])

    @parametrize
    def test_streaming_response_batch_delete(self, client: SGPClient) -> None:
        with client.knowledge_bases.artifacts.with_streaming_response.batch_delete(
            knowledge_base_id="knowledge_base_id",
            artifact_ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            artifact = response.parse()
            assert_matches_type(ArtifactBatchDeleteResponse, artifact, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_batch_delete(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.artifacts.with_raw_response.batch_delete(
                knowledge_base_id="",
                artifact_ids=["string"],
            )


class TestAsyncArtifacts:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        artifact = await async_client.knowledge_bases.artifacts.retrieve(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(Artifact, artifact, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGPClient) -> None:
        artifact = await async_client.knowledge_bases.artifacts.retrieve(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
            status_filter="status_filter",
        )
        assert_matches_type(Artifact, artifact, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.artifacts.with_raw_response.retrieve(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        artifact = await response.parse()
        assert_matches_type(Artifact, artifact, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.artifacts.with_streaming_response.retrieve(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            artifact = await response.parse()
            assert_matches_type(Artifact, artifact, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.artifacts.with_raw_response.retrieve(
                artifact_id="artifact_id",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `artifact_id` but received ''"):
            await async_client.knowledge_bases.artifacts.with_raw_response.retrieve(
                artifact_id="",
                knowledge_base_id="knowledge_base_id",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        artifact = await async_client.knowledge_bases.artifacts.update(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(ArtifactUpdateResponse, artifact, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        artifact = await async_client.knowledge_bases.artifacts.update(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
            tags={"foo": "bar"},
        )
        assert_matches_type(ArtifactUpdateResponse, artifact, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.artifacts.with_raw_response.update(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        artifact = await response.parse()
        assert_matches_type(ArtifactUpdateResponse, artifact, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.artifacts.with_streaming_response.update(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            artifact = await response.parse()
            assert_matches_type(ArtifactUpdateResponse, artifact, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.artifacts.with_raw_response.update(
                artifact_id="artifact_id",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `artifact_id` but received ''"):
            await async_client.knowledge_bases.artifacts.with_raw_response.update(
                artifact_id="",
                knowledge_base_id="knowledge_base_id",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        artifact = await async_client.knowledge_bases.artifacts.list(
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(AsyncPageResponse[Item], artifact, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        artifact = await async_client.knowledge_bases.artifacts.list(
            knowledge_base_id="knowledge_base_id",
            limit=1,
            page=1,
            status="Pending",
        )
        assert_matches_type(AsyncPageResponse[Item], artifact, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.artifacts.with_raw_response.list(
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        artifact = await response.parse()
        assert_matches_type(AsyncPageResponse[Item], artifact, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.artifacts.with_streaming_response.list(
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            artifact = await response.parse()
            assert_matches_type(AsyncPageResponse[Item], artifact, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.artifacts.with_raw_response.list(
                knowledge_base_id="",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        artifact = await async_client.knowledge_bases.artifacts.delete(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(ArtifactDeleteResponse, artifact, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.artifacts.with_raw_response.delete(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        artifact = await response.parse()
        assert_matches_type(ArtifactDeleteResponse, artifact, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.artifacts.with_streaming_response.delete(
            artifact_id="artifact_id",
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            artifact = await response.parse()
            assert_matches_type(ArtifactDeleteResponse, artifact, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.artifacts.with_raw_response.delete(
                artifact_id="artifact_id",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `artifact_id` but received ''"):
            await async_client.knowledge_bases.artifacts.with_raw_response.delete(
                artifact_id="",
                knowledge_base_id="knowledge_base_id",
            )

    @parametrize
    async def test_method_batch_delete(self, async_client: AsyncSGPClient) -> None:
        artifact = await async_client.knowledge_bases.artifacts.batch_delete(
            knowledge_base_id="knowledge_base_id",
            artifact_ids=["string"],
        )
        assert_matches_type(ArtifactBatchDeleteResponse, artifact, path=["response"])

    @parametrize
    async def test_raw_response_batch_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.artifacts.with_raw_response.batch_delete(
            knowledge_base_id="knowledge_base_id",
            artifact_ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        artifact = await response.parse()
        assert_matches_type(ArtifactBatchDeleteResponse, artifact, path=["response"])

    @parametrize
    async def test_streaming_response_batch_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.artifacts.with_streaming_response.batch_delete(
            knowledge_base_id="knowledge_base_id",
            artifact_ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            artifact = await response.parse()
            assert_matches_type(ArtifactBatchDeleteResponse, artifact, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_batch_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.artifacts.with_raw_response.batch_delete(
                knowledge_base_id="",
                artifact_ids=["string"],
            )
