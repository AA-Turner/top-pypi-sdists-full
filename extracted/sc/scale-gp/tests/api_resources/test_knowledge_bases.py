# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import (
    KnowledgeBase,
    CreateKnowledgeBaseResponse,
    DeleteKnowledgeBaseResponse,
    KnowledgeBaseUpdateResponse,
    CreateKnowledgeBaseUploadsFromFilesResponse,
)
from scale_gp.pagination import SyncPageResponse, AsyncPageResponse, SyncChunkPagination, AsyncChunkPagination
from scale_gp.types.shared import Chunk

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestKnowledgeBases:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        knowledge_base = client.knowledge_bases.create(
            embedding_config={
                "model_deployment_id": "model_deployment_id",
                "type": "models_api",
            },
            knowledge_base_name="knowledge_base_name",
        )
        assert_matches_type(CreateKnowledgeBaseResponse, knowledge_base, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        knowledge_base = client.knowledge_bases.create(
            embedding_config={
                "model_deployment_id": "model_deployment_id",
                "type": "models_api",
            },
            knowledge_base_name="knowledge_base_name",
            account_id="account_id",
            kb_index_configuration={
                "fields": {
                    "author": "bar",
                    "priority": "bar",
                },
                "max_index_size": 1,
            },
            metadata={"foo": "bar"},
        )
        assert_matches_type(CreateKnowledgeBaseResponse, knowledge_base, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.knowledge_bases.with_raw_response.create(
            embedding_config={
                "model_deployment_id": "model_deployment_id",
                "type": "models_api",
            },
            knowledge_base_name="knowledge_base_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base = response.parse()
        assert_matches_type(CreateKnowledgeBaseResponse, knowledge_base, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.knowledge_bases.with_streaming_response.create(
            embedding_config={
                "model_deployment_id": "model_deployment_id",
                "type": "models_api",
            },
            knowledge_base_name="knowledge_base_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base = response.parse()
            assert_matches_type(CreateKnowledgeBaseResponse, knowledge_base, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        knowledge_base = client.knowledge_bases.retrieve(
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(KnowledgeBase, knowledge_base, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGPClient) -> None:
        knowledge_base = client.knowledge_bases.retrieve(
            knowledge_base_id="knowledge_base_id",
            include_artifacts_status=True,
            view=["Connections"],
        )
        assert_matches_type(KnowledgeBase, knowledge_base, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.knowledge_bases.with_raw_response.retrieve(
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base = response.parse()
        assert_matches_type(KnowledgeBase, knowledge_base, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.knowledge_bases.with_streaming_response.retrieve(
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base = response.parse()
            assert_matches_type(KnowledgeBase, knowledge_base, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.with_raw_response.retrieve(
                knowledge_base_id="",
            )

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        knowledge_base = client.knowledge_bases.update(
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(KnowledgeBaseUpdateResponse, knowledge_base, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGPClient) -> None:
        knowledge_base = client.knowledge_bases.update(
            knowledge_base_id="knowledge_base_id",
            knowledge_base_name="knowledge_base_name",
            metadata={"foo": "bar"},
        )
        assert_matches_type(KnowledgeBaseUpdateResponse, knowledge_base, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.knowledge_bases.with_raw_response.update(
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base = response.parse()
        assert_matches_type(KnowledgeBaseUpdateResponse, knowledge_base, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.knowledge_bases.with_streaming_response.update(
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base = response.parse()
            assert_matches_type(KnowledgeBaseUpdateResponse, knowledge_base, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.with_raw_response.update(
                knowledge_base_id="",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        knowledge_base = client.knowledge_bases.list()
        assert_matches_type(SyncPageResponse[KnowledgeBase], knowledge_base, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        knowledge_base = client.knowledge_bases.list(
            account_id="account_id",
            limit=1,
            name="name",
            page=1,
            view=["Connections"],
        )
        assert_matches_type(SyncPageResponse[KnowledgeBase], knowledge_base, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.knowledge_bases.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base = response.parse()
        assert_matches_type(SyncPageResponse[KnowledgeBase], knowledge_base, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.knowledge_bases.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base = response.parse()
            assert_matches_type(SyncPageResponse[KnowledgeBase], knowledge_base, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        knowledge_base = client.knowledge_bases.delete(
            "knowledge_base_id",
        )
        assert_matches_type(DeleteKnowledgeBaseResponse, knowledge_base, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.knowledge_bases.with_raw_response.delete(
            "knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base = response.parse()
        assert_matches_type(DeleteKnowledgeBaseResponse, knowledge_base, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.knowledge_bases.with_streaming_response.delete(
            "knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base = response.parse()
            assert_matches_type(DeleteKnowledgeBaseResponse, knowledge_base, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_query(self, client: SGPClient) -> None:
        knowledge_base = client.knowledge_bases.query(
            knowledge_base_id="knowledge_base_id",
            query="query",
            top_k=1,
        )
        assert_matches_type(SyncChunkPagination[Chunk], knowledge_base, path=["response"])

    @parametrize
    def test_method_query_with_all_params(self, client: SGPClient) -> None:
        knowledge_base = client.knowledge_bases.query(
            knowledge_base_id="knowledge_base_id",
            query="query",
            top_k=1,
            include_embeddings=True,
            metadata_filters={"foo": "bar"},
            verbose=True,
            wildcard_filters={
                "foo": {
                    "value": "value",
                    "case_insensitive": True,
                }
            },
        )
        assert_matches_type(SyncChunkPagination[Chunk], knowledge_base, path=["response"])

    @parametrize
    def test_raw_response_query(self, client: SGPClient) -> None:
        response = client.knowledge_bases.with_raw_response.query(
            knowledge_base_id="knowledge_base_id",
            query="query",
            top_k=1,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base = response.parse()
        assert_matches_type(SyncChunkPagination[Chunk], knowledge_base, path=["response"])

    @parametrize
    def test_streaming_response_query(self, client: SGPClient) -> None:
        with client.knowledge_bases.with_streaming_response.query(
            knowledge_base_id="knowledge_base_id",
            query="query",
            top_k=1,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base = response.parse()
            assert_matches_type(SyncChunkPagination[Chunk], knowledge_base, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_query(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.with_raw_response.query(
                knowledge_base_id="",
                query="query",
                top_k=1,
            )

    @pytest.mark.skip(reason="prism_binary_unsupported")
    @parametrize
    def test_method_upload_files(self, client: SGPClient) -> None:
        knowledge_base = client.knowledge_bases.upload_files(
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config="chunking_strategy_config",
            data_source_config="data_source_config",
            files=[b"raw file contents"],
            force_reupload=True,
        )
        assert_matches_type(CreateKnowledgeBaseUploadsFromFilesResponse, knowledge_base, path=["response"])

    @pytest.mark.skip(reason="prism_binary_unsupported")
    @parametrize
    def test_method_upload_files_with_all_params(self, client: SGPClient) -> None:
        knowledge_base = client.knowledge_bases.upload_files(
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config="chunking_strategy_config",
            data_source_config="data_source_config",
            files=[b"raw file contents"],
            force_reupload=True,
            tagging_information="tagging_information",
        )
        assert_matches_type(CreateKnowledgeBaseUploadsFromFilesResponse, knowledge_base, path=["response"])

    @pytest.mark.skip(reason="prism_binary_unsupported")
    @parametrize
    def test_raw_response_upload_files(self, client: SGPClient) -> None:
        response = client.knowledge_bases.with_raw_response.upload_files(
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config="chunking_strategy_config",
            data_source_config="data_source_config",
            files=[b"raw file contents"],
            force_reupload=True,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base = response.parse()
        assert_matches_type(CreateKnowledgeBaseUploadsFromFilesResponse, knowledge_base, path=["response"])

    @pytest.mark.skip(reason="prism_binary_unsupported")
    @parametrize
    def test_streaming_response_upload_files(self, client: SGPClient) -> None:
        with client.knowledge_bases.with_streaming_response.upload_files(
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config="chunking_strategy_config",
            data_source_config="data_source_config",
            files=[b"raw file contents"],
            force_reupload=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base = response.parse()
            assert_matches_type(CreateKnowledgeBaseUploadsFromFilesResponse, knowledge_base, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism_binary_unsupported")
    @parametrize
    def test_path_params_upload_files(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.with_raw_response.upload_files(
                knowledge_base_id="",
                chunking_strategy_config="chunking_strategy_config",
                data_source_config="data_source_config",
                files=[b"raw file contents"],
                force_reupload=True,
            )


class TestAsyncKnowledgeBases:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        knowledge_base = await async_client.knowledge_bases.create(
            embedding_config={
                "model_deployment_id": "model_deployment_id",
                "type": "models_api",
            },
            knowledge_base_name="knowledge_base_name",
        )
        assert_matches_type(CreateKnowledgeBaseResponse, knowledge_base, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        knowledge_base = await async_client.knowledge_bases.create(
            embedding_config={
                "model_deployment_id": "model_deployment_id",
                "type": "models_api",
            },
            knowledge_base_name="knowledge_base_name",
            account_id="account_id",
            kb_index_configuration={
                "fields": {
                    "author": "bar",
                    "priority": "bar",
                },
                "max_index_size": 1,
            },
            metadata={"foo": "bar"},
        )
        assert_matches_type(CreateKnowledgeBaseResponse, knowledge_base, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.with_raw_response.create(
            embedding_config={
                "model_deployment_id": "model_deployment_id",
                "type": "models_api",
            },
            knowledge_base_name="knowledge_base_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base = await response.parse()
        assert_matches_type(CreateKnowledgeBaseResponse, knowledge_base, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.with_streaming_response.create(
            embedding_config={
                "model_deployment_id": "model_deployment_id",
                "type": "models_api",
            },
            knowledge_base_name="knowledge_base_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base = await response.parse()
            assert_matches_type(CreateKnowledgeBaseResponse, knowledge_base, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        knowledge_base = await async_client.knowledge_bases.retrieve(
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(KnowledgeBase, knowledge_base, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGPClient) -> None:
        knowledge_base = await async_client.knowledge_bases.retrieve(
            knowledge_base_id="knowledge_base_id",
            include_artifacts_status=True,
            view=["Connections"],
        )
        assert_matches_type(KnowledgeBase, knowledge_base, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.with_raw_response.retrieve(
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base = await response.parse()
        assert_matches_type(KnowledgeBase, knowledge_base, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.with_streaming_response.retrieve(
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base = await response.parse()
            assert_matches_type(KnowledgeBase, knowledge_base, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.with_raw_response.retrieve(
                knowledge_base_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        knowledge_base = await async_client.knowledge_bases.update(
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(KnowledgeBaseUpdateResponse, knowledge_base, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        knowledge_base = await async_client.knowledge_bases.update(
            knowledge_base_id="knowledge_base_id",
            knowledge_base_name="knowledge_base_name",
            metadata={"foo": "bar"},
        )
        assert_matches_type(KnowledgeBaseUpdateResponse, knowledge_base, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.with_raw_response.update(
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base = await response.parse()
        assert_matches_type(KnowledgeBaseUpdateResponse, knowledge_base, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.with_streaming_response.update(
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base = await response.parse()
            assert_matches_type(KnowledgeBaseUpdateResponse, knowledge_base, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.with_raw_response.update(
                knowledge_base_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        knowledge_base = await async_client.knowledge_bases.list()
        assert_matches_type(AsyncPageResponse[KnowledgeBase], knowledge_base, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        knowledge_base = await async_client.knowledge_bases.list(
            account_id="account_id",
            limit=1,
            name="name",
            page=1,
            view=["Connections"],
        )
        assert_matches_type(AsyncPageResponse[KnowledgeBase], knowledge_base, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base = await response.parse()
        assert_matches_type(AsyncPageResponse[KnowledgeBase], knowledge_base, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base = await response.parse()
            assert_matches_type(AsyncPageResponse[KnowledgeBase], knowledge_base, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        knowledge_base = await async_client.knowledge_bases.delete(
            "knowledge_base_id",
        )
        assert_matches_type(DeleteKnowledgeBaseResponse, knowledge_base, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.with_raw_response.delete(
            "knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base = await response.parse()
        assert_matches_type(DeleteKnowledgeBaseResponse, knowledge_base, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.with_streaming_response.delete(
            "knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base = await response.parse()
            assert_matches_type(DeleteKnowledgeBaseResponse, knowledge_base, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_query(self, async_client: AsyncSGPClient) -> None:
        knowledge_base = await async_client.knowledge_bases.query(
            knowledge_base_id="knowledge_base_id",
            query="query",
            top_k=1,
        )
        assert_matches_type(AsyncChunkPagination[Chunk], knowledge_base, path=["response"])

    @parametrize
    async def test_method_query_with_all_params(self, async_client: AsyncSGPClient) -> None:
        knowledge_base = await async_client.knowledge_bases.query(
            knowledge_base_id="knowledge_base_id",
            query="query",
            top_k=1,
            include_embeddings=True,
            metadata_filters={"foo": "bar"},
            verbose=True,
            wildcard_filters={
                "foo": {
                    "value": "value",
                    "case_insensitive": True,
                }
            },
        )
        assert_matches_type(AsyncChunkPagination[Chunk], knowledge_base, path=["response"])

    @parametrize
    async def test_raw_response_query(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.with_raw_response.query(
            knowledge_base_id="knowledge_base_id",
            query="query",
            top_k=1,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base = await response.parse()
        assert_matches_type(AsyncChunkPagination[Chunk], knowledge_base, path=["response"])

    @parametrize
    async def test_streaming_response_query(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.with_streaming_response.query(
            knowledge_base_id="knowledge_base_id",
            query="query",
            top_k=1,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base = await response.parse()
            assert_matches_type(AsyncChunkPagination[Chunk], knowledge_base, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_query(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.with_raw_response.query(
                knowledge_base_id="",
                query="query",
                top_k=1,
            )

    @pytest.mark.skip(reason="prism_binary_unsupported")
    @parametrize
    async def test_method_upload_files(self, async_client: AsyncSGPClient) -> None:
        knowledge_base = await async_client.knowledge_bases.upload_files(
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config="chunking_strategy_config",
            data_source_config="data_source_config",
            files=[b"raw file contents"],
            force_reupload=True,
        )
        assert_matches_type(CreateKnowledgeBaseUploadsFromFilesResponse, knowledge_base, path=["response"])

    @pytest.mark.skip(reason="prism_binary_unsupported")
    @parametrize
    async def test_method_upload_files_with_all_params(self, async_client: AsyncSGPClient) -> None:
        knowledge_base = await async_client.knowledge_bases.upload_files(
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config="chunking_strategy_config",
            data_source_config="data_source_config",
            files=[b"raw file contents"],
            force_reupload=True,
            tagging_information="tagging_information",
        )
        assert_matches_type(CreateKnowledgeBaseUploadsFromFilesResponse, knowledge_base, path=["response"])

    @pytest.mark.skip(reason="prism_binary_unsupported")
    @parametrize
    async def test_raw_response_upload_files(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.with_raw_response.upload_files(
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config="chunking_strategy_config",
            data_source_config="data_source_config",
            files=[b"raw file contents"],
            force_reupload=True,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base = await response.parse()
        assert_matches_type(CreateKnowledgeBaseUploadsFromFilesResponse, knowledge_base, path=["response"])

    @pytest.mark.skip(reason="prism_binary_unsupported")
    @parametrize
    async def test_streaming_response_upload_files(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.with_streaming_response.upload_files(
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config="chunking_strategy_config",
            data_source_config="data_source_config",
            files=[b"raw file contents"],
            force_reupload=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base = await response.parse()
            assert_matches_type(CreateKnowledgeBaseUploadsFromFilesResponse, knowledge_base, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism_binary_unsupported")
    @parametrize
    async def test_path_params_upload_files(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.with_raw_response.upload_files(
                knowledge_base_id="",
                chunking_strategy_config="chunking_strategy_config",
                data_source_config="data_source_config",
                files=[b"raw file contents"],
                force_reupload=True,
            )
