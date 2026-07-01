# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.pagination import SyncPageResponse, AsyncPageResponse
from scale_gp.types.knowledge_bases import (
    KnowledgeBaseUpload,
    CancelKnowledgeBaseUploadResponse,
    CreateKnowledgeBaseUploadResponse,
)
from scale_gp.types.paginated_knowledge_base_uploads import Item

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUploads:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create_overload_1(self, client: SGPClient) -> None:
        upload = client.knowledge_bases.uploads.create(
            knowledge_base_id="knowledge_base_id",
            data_source_config={
                "aws_account_id": "aws_account_id",
                "aws_region": "aws_region",
                "s3_bucket": "s3_bucket",
                "source": "S3",
            },
        )
        assert_matches_type(CreateKnowledgeBaseUploadResponse, upload, path=["response"])

    @parametrize
    def test_method_create_with_all_params_overload_1(self, client: SGPClient) -> None:
        upload = client.knowledge_bases.uploads.create(
            knowledge_base_id="knowledge_base_id",
            data_source_config={
                "aws_account_id": "aws_account_id",
                "aws_region": "aws_region",
                "s3_bucket": "s3_bucket",
                "source": "S3",
                "s3_prefix": "s3_prefix",
            },
            chunking_strategy_config={
                "strategy": "character",
                "chunk_overlap": 0,
                "chunk_size": 1,
                "separator": "separator",
            },
            data_source_auth_config={
                "client_secret": "client_secret",
                "source": "SharePoint",
                "encrypted": True,
            },
            force_reupload=True,
            tagging_information={
                "tags_to_apply": {"foo": {"foo": "bar"}},
                "type": "per_file",
            },
        )
        assert_matches_type(CreateKnowledgeBaseUploadResponse, upload, path=["response"])

    @parametrize
    def test_raw_response_create_overload_1(self, client: SGPClient) -> None:
        response = client.knowledge_bases.uploads.with_raw_response.create(
            knowledge_base_id="knowledge_base_id",
            data_source_config={
                "aws_account_id": "aws_account_id",
                "aws_region": "aws_region",
                "s3_bucket": "s3_bucket",
                "source": "S3",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = response.parse()
        assert_matches_type(CreateKnowledgeBaseUploadResponse, upload, path=["response"])

    @parametrize
    def test_streaming_response_create_overload_1(self, client: SGPClient) -> None:
        with client.knowledge_bases.uploads.with_streaming_response.create(
            knowledge_base_id="knowledge_base_id",
            data_source_config={
                "aws_account_id": "aws_account_id",
                "aws_region": "aws_region",
                "s3_bucket": "s3_bucket",
                "source": "S3",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = response.parse()
            assert_matches_type(CreateKnowledgeBaseUploadResponse, upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create_overload_1(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.uploads.with_raw_response.create(
                knowledge_base_id="",
                data_source_config={
                    "aws_account_id": "aws_account_id",
                    "aws_region": "aws_region",
                    "s3_bucket": "s3_bucket",
                    "source": "S3",
                },
            )

    @parametrize
    def test_method_create_overload_2(self, client: SGPClient) -> None:
        upload = client.knowledge_bases.uploads.create(
            knowledge_base_id="knowledge_base_id",
            data_source_config={
                "artifact_name": "artifact_name",
                "artifact_uri": "artifact_uri",
                "source": "LocalChunks",
            },
        )
        assert_matches_type(CreateKnowledgeBaseUploadResponse, upload, path=["response"])

    @parametrize
    def test_method_create_with_all_params_overload_2(self, client: SGPClient) -> None:
        upload = client.knowledge_bases.uploads.create(
            knowledge_base_id="knowledge_base_id",
            data_source_config={
                "artifact_name": "artifact_name",
                "artifact_uri": "artifact_uri",
                "source": "LocalChunks",
                "deduplication_strategy": "Overwrite",
            },
            chunks=[
                {
                    "chunk_position": 0,
                    "text": "text",
                    "metadata": {"foo": "bar"},
                }
            ],
            force_reupload=True,
            tagging_information={
                "tags_to_apply": {"foo": {"foo": "bar"}},
                "type": "per_file",
            },
        )
        assert_matches_type(CreateKnowledgeBaseUploadResponse, upload, path=["response"])

    @parametrize
    def test_raw_response_create_overload_2(self, client: SGPClient) -> None:
        response = client.knowledge_bases.uploads.with_raw_response.create(
            knowledge_base_id="knowledge_base_id",
            data_source_config={
                "artifact_name": "artifact_name",
                "artifact_uri": "artifact_uri",
                "source": "LocalChunks",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = response.parse()
        assert_matches_type(CreateKnowledgeBaseUploadResponse, upload, path=["response"])

    @parametrize
    def test_streaming_response_create_overload_2(self, client: SGPClient) -> None:
        with client.knowledge_bases.uploads.with_streaming_response.create(
            knowledge_base_id="knowledge_base_id",
            data_source_config={
                "artifact_name": "artifact_name",
                "artifact_uri": "artifact_uri",
                "source": "LocalChunks",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = response.parse()
            assert_matches_type(CreateKnowledgeBaseUploadResponse, upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create_overload_2(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.uploads.with_raw_response.create(
                knowledge_base_id="",
                data_source_config={
                    "artifact_name": "artifact_name",
                    "artifact_uri": "artifact_uri",
                    "source": "LocalChunks",
                },
            )

    @parametrize
    def test_method_create_overload_3(self, client: SGPClient) -> None:
        upload = client.knowledge_bases.uploads.create(
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config={"strategy": "character"},
            data_source_id="data_source_id",
        )
        assert_matches_type(CreateKnowledgeBaseUploadResponse, upload, path=["response"])

    @parametrize
    def test_method_create_with_all_params_overload_3(self, client: SGPClient) -> None:
        upload = client.knowledge_bases.uploads.create(
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config={
                "strategy": "character",
                "chunk_overlap": 0,
                "chunk_size": 1,
                "separator": "separator",
            },
            data_source_id="data_source_id",
            force_reupload=True,
            tagging_information={
                "tags_to_apply": {"foo": {"foo": "bar"}},
                "type": "per_file",
            },
        )
        assert_matches_type(CreateKnowledgeBaseUploadResponse, upload, path=["response"])

    @parametrize
    def test_raw_response_create_overload_3(self, client: SGPClient) -> None:
        response = client.knowledge_bases.uploads.with_raw_response.create(
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config={"strategy": "character"},
            data_source_id="data_source_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = response.parse()
        assert_matches_type(CreateKnowledgeBaseUploadResponse, upload, path=["response"])

    @parametrize
    def test_streaming_response_create_overload_3(self, client: SGPClient) -> None:
        with client.knowledge_bases.uploads.with_streaming_response.create(
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config={"strategy": "character"},
            data_source_id="data_source_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = response.parse()
            assert_matches_type(CreateKnowledgeBaseUploadResponse, upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create_overload_3(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.uploads.with_raw_response.create(
                knowledge_base_id="",
                chunking_strategy_config={"strategy": "character"},
                data_source_id="data_source_id",
            )

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        upload = client.knowledge_bases.uploads.retrieve(
            upload_id="upload_id",
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(KnowledgeBaseUpload, upload, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGPClient) -> None:
        upload = client.knowledge_bases.uploads.retrieve(
            upload_id="upload_id",
            knowledge_base_id="knowledge_base_id",
            include_artifact_list=True,
        )
        assert_matches_type(KnowledgeBaseUpload, upload, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.knowledge_bases.uploads.with_raw_response.retrieve(
            upload_id="upload_id",
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = response.parse()
        assert_matches_type(KnowledgeBaseUpload, upload, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.knowledge_bases.uploads.with_streaming_response.retrieve(
            upload_id="upload_id",
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = response.parse()
            assert_matches_type(KnowledgeBaseUpload, upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.uploads.with_raw_response.retrieve(
                upload_id="upload_id",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `upload_id` but received ''"):
            client.knowledge_bases.uploads.with_raw_response.retrieve(
                upload_id="",
                knowledge_base_id="knowledge_base_id",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        upload = client.knowledge_bases.uploads.list(
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(SyncPageResponse[Item], upload, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        upload = client.knowledge_bases.uploads.list(
            knowledge_base_id="knowledge_base_id",
            limit=1,
            page=1,
            status="Running",
        )
        assert_matches_type(SyncPageResponse[Item], upload, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.knowledge_bases.uploads.with_raw_response.list(
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = response.parse()
        assert_matches_type(SyncPageResponse[Item], upload, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.knowledge_bases.uploads.with_streaming_response.list(
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = response.parse()
            assert_matches_type(SyncPageResponse[Item], upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.uploads.with_raw_response.list(
                knowledge_base_id="",
            )

    @parametrize
    def test_method_cancel(self, client: SGPClient) -> None:
        upload = client.knowledge_bases.uploads.cancel(
            upload_id="upload_id",
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(CancelKnowledgeBaseUploadResponse, upload, path=["response"])

    @parametrize
    def test_raw_response_cancel(self, client: SGPClient) -> None:
        response = client.knowledge_bases.uploads.with_raw_response.cancel(
            upload_id="upload_id",
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = response.parse()
        assert_matches_type(CancelKnowledgeBaseUploadResponse, upload, path=["response"])

    @parametrize
    def test_streaming_response_cancel(self, client: SGPClient) -> None:
        with client.knowledge_bases.uploads.with_streaming_response.cancel(
            upload_id="upload_id",
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = response.parse()
            assert_matches_type(CancelKnowledgeBaseUploadResponse, upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_cancel(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            client.knowledge_bases.uploads.with_raw_response.cancel(
                upload_id="upload_id",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `upload_id` but received ''"):
            client.knowledge_bases.uploads.with_raw_response.cancel(
                upload_id="",
                knowledge_base_id="knowledge_base_id",
            )


class TestAsyncUploads:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create_overload_1(self, async_client: AsyncSGPClient) -> None:
        upload = await async_client.knowledge_bases.uploads.create(
            knowledge_base_id="knowledge_base_id",
            data_source_config={
                "aws_account_id": "aws_account_id",
                "aws_region": "aws_region",
                "s3_bucket": "s3_bucket",
                "source": "S3",
            },
        )
        assert_matches_type(CreateKnowledgeBaseUploadResponse, upload, path=["response"])

    @parametrize
    async def test_method_create_with_all_params_overload_1(self, async_client: AsyncSGPClient) -> None:
        upload = await async_client.knowledge_bases.uploads.create(
            knowledge_base_id="knowledge_base_id",
            data_source_config={
                "aws_account_id": "aws_account_id",
                "aws_region": "aws_region",
                "s3_bucket": "s3_bucket",
                "source": "S3",
                "s3_prefix": "s3_prefix",
            },
            chunking_strategy_config={
                "strategy": "character",
                "chunk_overlap": 0,
                "chunk_size": 1,
                "separator": "separator",
            },
            data_source_auth_config={
                "client_secret": "client_secret",
                "source": "SharePoint",
                "encrypted": True,
            },
            force_reupload=True,
            tagging_information={
                "tags_to_apply": {"foo": {"foo": "bar"}},
                "type": "per_file",
            },
        )
        assert_matches_type(CreateKnowledgeBaseUploadResponse, upload, path=["response"])

    @parametrize
    async def test_raw_response_create_overload_1(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.uploads.with_raw_response.create(
            knowledge_base_id="knowledge_base_id",
            data_source_config={
                "aws_account_id": "aws_account_id",
                "aws_region": "aws_region",
                "s3_bucket": "s3_bucket",
                "source": "S3",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = await response.parse()
        assert_matches_type(CreateKnowledgeBaseUploadResponse, upload, path=["response"])

    @parametrize
    async def test_streaming_response_create_overload_1(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.uploads.with_streaming_response.create(
            knowledge_base_id="knowledge_base_id",
            data_source_config={
                "aws_account_id": "aws_account_id",
                "aws_region": "aws_region",
                "s3_bucket": "s3_bucket",
                "source": "S3",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = await response.parse()
            assert_matches_type(CreateKnowledgeBaseUploadResponse, upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create_overload_1(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.uploads.with_raw_response.create(
                knowledge_base_id="",
                data_source_config={
                    "aws_account_id": "aws_account_id",
                    "aws_region": "aws_region",
                    "s3_bucket": "s3_bucket",
                    "source": "S3",
                },
            )

    @parametrize
    async def test_method_create_overload_2(self, async_client: AsyncSGPClient) -> None:
        upload = await async_client.knowledge_bases.uploads.create(
            knowledge_base_id="knowledge_base_id",
            data_source_config={
                "artifact_name": "artifact_name",
                "artifact_uri": "artifact_uri",
                "source": "LocalChunks",
            },
        )
        assert_matches_type(CreateKnowledgeBaseUploadResponse, upload, path=["response"])

    @parametrize
    async def test_method_create_with_all_params_overload_2(self, async_client: AsyncSGPClient) -> None:
        upload = await async_client.knowledge_bases.uploads.create(
            knowledge_base_id="knowledge_base_id",
            data_source_config={
                "artifact_name": "artifact_name",
                "artifact_uri": "artifact_uri",
                "source": "LocalChunks",
                "deduplication_strategy": "Overwrite",
            },
            chunks=[
                {
                    "chunk_position": 0,
                    "text": "text",
                    "metadata": {"foo": "bar"},
                }
            ],
            force_reupload=True,
            tagging_information={
                "tags_to_apply": {"foo": {"foo": "bar"}},
                "type": "per_file",
            },
        )
        assert_matches_type(CreateKnowledgeBaseUploadResponse, upload, path=["response"])

    @parametrize
    async def test_raw_response_create_overload_2(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.uploads.with_raw_response.create(
            knowledge_base_id="knowledge_base_id",
            data_source_config={
                "artifact_name": "artifact_name",
                "artifact_uri": "artifact_uri",
                "source": "LocalChunks",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = await response.parse()
        assert_matches_type(CreateKnowledgeBaseUploadResponse, upload, path=["response"])

    @parametrize
    async def test_streaming_response_create_overload_2(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.uploads.with_streaming_response.create(
            knowledge_base_id="knowledge_base_id",
            data_source_config={
                "artifact_name": "artifact_name",
                "artifact_uri": "artifact_uri",
                "source": "LocalChunks",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = await response.parse()
            assert_matches_type(CreateKnowledgeBaseUploadResponse, upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create_overload_2(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.uploads.with_raw_response.create(
                knowledge_base_id="",
                data_source_config={
                    "artifact_name": "artifact_name",
                    "artifact_uri": "artifact_uri",
                    "source": "LocalChunks",
                },
            )

    @parametrize
    async def test_method_create_overload_3(self, async_client: AsyncSGPClient) -> None:
        upload = await async_client.knowledge_bases.uploads.create(
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config={"strategy": "character"},
            data_source_id="data_source_id",
        )
        assert_matches_type(CreateKnowledgeBaseUploadResponse, upload, path=["response"])

    @parametrize
    async def test_method_create_with_all_params_overload_3(self, async_client: AsyncSGPClient) -> None:
        upload = await async_client.knowledge_bases.uploads.create(
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config={
                "strategy": "character",
                "chunk_overlap": 0,
                "chunk_size": 1,
                "separator": "separator",
            },
            data_source_id="data_source_id",
            force_reupload=True,
            tagging_information={
                "tags_to_apply": {"foo": {"foo": "bar"}},
                "type": "per_file",
            },
        )
        assert_matches_type(CreateKnowledgeBaseUploadResponse, upload, path=["response"])

    @parametrize
    async def test_raw_response_create_overload_3(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.uploads.with_raw_response.create(
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config={"strategy": "character"},
            data_source_id="data_source_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = await response.parse()
        assert_matches_type(CreateKnowledgeBaseUploadResponse, upload, path=["response"])

    @parametrize
    async def test_streaming_response_create_overload_3(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.uploads.with_streaming_response.create(
            knowledge_base_id="knowledge_base_id",
            chunking_strategy_config={"strategy": "character"},
            data_source_id="data_source_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = await response.parse()
            assert_matches_type(CreateKnowledgeBaseUploadResponse, upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create_overload_3(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.uploads.with_raw_response.create(
                knowledge_base_id="",
                chunking_strategy_config={"strategy": "character"},
                data_source_id="data_source_id",
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        upload = await async_client.knowledge_bases.uploads.retrieve(
            upload_id="upload_id",
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(KnowledgeBaseUpload, upload, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGPClient) -> None:
        upload = await async_client.knowledge_bases.uploads.retrieve(
            upload_id="upload_id",
            knowledge_base_id="knowledge_base_id",
            include_artifact_list=True,
        )
        assert_matches_type(KnowledgeBaseUpload, upload, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.uploads.with_raw_response.retrieve(
            upload_id="upload_id",
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = await response.parse()
        assert_matches_type(KnowledgeBaseUpload, upload, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.uploads.with_streaming_response.retrieve(
            upload_id="upload_id",
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = await response.parse()
            assert_matches_type(KnowledgeBaseUpload, upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.uploads.with_raw_response.retrieve(
                upload_id="upload_id",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `upload_id` but received ''"):
            await async_client.knowledge_bases.uploads.with_raw_response.retrieve(
                upload_id="",
                knowledge_base_id="knowledge_base_id",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        upload = await async_client.knowledge_bases.uploads.list(
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(AsyncPageResponse[Item], upload, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        upload = await async_client.knowledge_bases.uploads.list(
            knowledge_base_id="knowledge_base_id",
            limit=1,
            page=1,
            status="Running",
        )
        assert_matches_type(AsyncPageResponse[Item], upload, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.uploads.with_raw_response.list(
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = await response.parse()
        assert_matches_type(AsyncPageResponse[Item], upload, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.uploads.with_streaming_response.list(
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = await response.parse()
            assert_matches_type(AsyncPageResponse[Item], upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.uploads.with_raw_response.list(
                knowledge_base_id="",
            )

    @parametrize
    async def test_method_cancel(self, async_client: AsyncSGPClient) -> None:
        upload = await async_client.knowledge_bases.uploads.cancel(
            upload_id="upload_id",
            knowledge_base_id="knowledge_base_id",
        )
        assert_matches_type(CancelKnowledgeBaseUploadResponse, upload, path=["response"])

    @parametrize
    async def test_raw_response_cancel(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_bases.uploads.with_raw_response.cancel(
            upload_id="upload_id",
            knowledge_base_id="knowledge_base_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = await response.parse()
        assert_matches_type(CancelKnowledgeBaseUploadResponse, upload, path=["response"])

    @parametrize
    async def test_streaming_response_cancel(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_bases.uploads.with_streaming_response.cancel(
            upload_id="upload_id",
            knowledge_base_id="knowledge_base_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = await response.parse()
            assert_matches_type(CancelKnowledgeBaseUploadResponse, upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_cancel(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `knowledge_base_id` but received ''"):
            await async_client.knowledge_bases.uploads.with_raw_response.cancel(
                upload_id="upload_id",
                knowledge_base_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `upload_id` but received ''"):
            await async_client.knowledge_bases.uploads.with_raw_response.cancel(
                upload_id="",
                knowledge_base_id="knowledge_base_id",
            )
