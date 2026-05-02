# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import (
    KnowledgeBaseDataSource,
)
from scale_gp.pagination import SyncPageResponse, AsyncPageResponse
from scale_gp.types.shared import GenericDeleteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestKnowledgeBaseDataSources:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        knowledge_base_data_source = client.knowledge_base_data_sources.create(
            account_id="account_id",
            data_source_config={
                "aws_account_id": "aws_account_id",
                "aws_region": "aws_region",
                "s3_bucket": "s3_bucket",
                "source": "S3",
            },
            name="name",
        )
        assert_matches_type(KnowledgeBaseDataSource, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        knowledge_base_data_source = client.knowledge_base_data_sources.create(
            account_id="account_id",
            data_source_config={
                "aws_account_id": "aws_account_id",
                "aws_region": "aws_region",
                "s3_bucket": "s3_bucket",
                "source": "S3",
                "s3_prefix": "s3_prefix",
            },
            name="name",
            data_source_auth_config={
                "client_secret": "client_secret",
                "source": "SharePoint",
                "encrypted": True,
            },
            description="description",
            tagging_information={
                "tags_to_apply": {"foo": "bar"},
                "type": "all",
            },
        )
        assert_matches_type(KnowledgeBaseDataSource, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.knowledge_base_data_sources.with_raw_response.create(
            account_id="account_id",
            data_source_config={
                "aws_account_id": "aws_account_id",
                "aws_region": "aws_region",
                "s3_bucket": "s3_bucket",
                "source": "S3",
            },
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base_data_source = response.parse()
        assert_matches_type(KnowledgeBaseDataSource, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.knowledge_base_data_sources.with_streaming_response.create(
            account_id="account_id",
            data_source_config={
                "aws_account_id": "aws_account_id",
                "aws_region": "aws_region",
                "s3_bucket": "s3_bucket",
                "source": "S3",
            },
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base_data_source = response.parse()
            assert_matches_type(KnowledgeBaseDataSource, knowledge_base_data_source, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        knowledge_base_data_source = client.knowledge_base_data_sources.retrieve(
            "knowledge_base_data_source_id",
        )
        assert_matches_type(KnowledgeBaseDataSource, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.knowledge_base_data_sources.with_raw_response.retrieve(
            "knowledge_base_data_source_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base_data_source = response.parse()
        assert_matches_type(KnowledgeBaseDataSource, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.knowledge_base_data_sources.with_streaming_response.retrieve(
            "knowledge_base_data_source_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base_data_source = response.parse()
            assert_matches_type(KnowledgeBaseDataSource, knowledge_base_data_source, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `knowledge_base_data_source_id` but received ''"
        ):
            client.knowledge_base_data_sources.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        knowledge_base_data_source = client.knowledge_base_data_sources.update(
            knowledge_base_data_source_id="knowledge_base_data_source_id",
        )
        assert_matches_type(KnowledgeBaseDataSource, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGPClient) -> None:
        knowledge_base_data_source = client.knowledge_base_data_sources.update(
            knowledge_base_data_source_id="knowledge_base_data_source_id",
            data_source_auth_config={
                "client_secret": "client_secret",
                "source": "SharePoint",
                "encrypted": True,
            },
            description="description",
            name="name",
            tagging_information={
                "tags_to_apply": {"foo": "bar"},
                "type": "all",
            },
        )
        assert_matches_type(KnowledgeBaseDataSource, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.knowledge_base_data_sources.with_raw_response.update(
            knowledge_base_data_source_id="knowledge_base_data_source_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base_data_source = response.parse()
        assert_matches_type(KnowledgeBaseDataSource, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.knowledge_base_data_sources.with_streaming_response.update(
            knowledge_base_data_source_id="knowledge_base_data_source_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base_data_source = response.parse()
            assert_matches_type(KnowledgeBaseDataSource, knowledge_base_data_source, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `knowledge_base_data_source_id` but received ''"
        ):
            client.knowledge_base_data_sources.with_raw_response.update(
                knowledge_base_data_source_id="",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        knowledge_base_data_source = client.knowledge_base_data_sources.list()
        assert_matches_type(SyncPageResponse[KnowledgeBaseDataSource], knowledge_base_data_source, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        knowledge_base_data_source = client.knowledge_base_data_sources.list(
            account_id="account_id",
            limit=1,
            name=0,
            page=1,
        )
        assert_matches_type(SyncPageResponse[KnowledgeBaseDataSource], knowledge_base_data_source, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.knowledge_base_data_sources.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base_data_source = response.parse()
        assert_matches_type(SyncPageResponse[KnowledgeBaseDataSource], knowledge_base_data_source, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.knowledge_base_data_sources.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base_data_source = response.parse()
            assert_matches_type(
                SyncPageResponse[KnowledgeBaseDataSource], knowledge_base_data_source, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        knowledge_base_data_source = client.knowledge_base_data_sources.delete(
            "knowledge_base_data_source_id",
        )
        assert_matches_type(GenericDeleteResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.knowledge_base_data_sources.with_raw_response.delete(
            "knowledge_base_data_source_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base_data_source = response.parse()
        assert_matches_type(GenericDeleteResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.knowledge_base_data_sources.with_streaming_response.delete(
            "knowledge_base_data_source_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base_data_source = response.parse()
            assert_matches_type(GenericDeleteResponse, knowledge_base_data_source, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `knowledge_base_data_source_id` but received ''"
        ):
            client.knowledge_base_data_sources.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_verify(self, client: SGPClient) -> None:
        knowledge_base_data_source = client.knowledge_base_data_sources.verify(
            "knowledge_base_data_source_id",
        )
        assert_matches_type(object, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_raw_response_verify(self, client: SGPClient) -> None:
        response = client.knowledge_base_data_sources.with_raw_response.verify(
            "knowledge_base_data_source_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base_data_source = response.parse()
        assert_matches_type(object, knowledge_base_data_source, path=["response"])

    @parametrize
    def test_streaming_response_verify(self, client: SGPClient) -> None:
        with client.knowledge_base_data_sources.with_streaming_response.verify(
            "knowledge_base_data_source_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base_data_source = response.parse()
            assert_matches_type(object, knowledge_base_data_source, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_verify(self, client: SGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `knowledge_base_data_source_id` but received ''"
        ):
            client.knowledge_base_data_sources.with_raw_response.verify(
                "",
            )


class TestAsyncKnowledgeBaseDataSources:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        knowledge_base_data_source = await async_client.knowledge_base_data_sources.create(
            account_id="account_id",
            data_source_config={
                "aws_account_id": "aws_account_id",
                "aws_region": "aws_region",
                "s3_bucket": "s3_bucket",
                "source": "S3",
            },
            name="name",
        )
        assert_matches_type(KnowledgeBaseDataSource, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        knowledge_base_data_source = await async_client.knowledge_base_data_sources.create(
            account_id="account_id",
            data_source_config={
                "aws_account_id": "aws_account_id",
                "aws_region": "aws_region",
                "s3_bucket": "s3_bucket",
                "source": "S3",
                "s3_prefix": "s3_prefix",
            },
            name="name",
            data_source_auth_config={
                "client_secret": "client_secret",
                "source": "SharePoint",
                "encrypted": True,
            },
            description="description",
            tagging_information={
                "tags_to_apply": {"foo": "bar"},
                "type": "all",
            },
        )
        assert_matches_type(KnowledgeBaseDataSource, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_base_data_sources.with_raw_response.create(
            account_id="account_id",
            data_source_config={
                "aws_account_id": "aws_account_id",
                "aws_region": "aws_region",
                "s3_bucket": "s3_bucket",
                "source": "S3",
            },
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base_data_source = await response.parse()
        assert_matches_type(KnowledgeBaseDataSource, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_base_data_sources.with_streaming_response.create(
            account_id="account_id",
            data_source_config={
                "aws_account_id": "aws_account_id",
                "aws_region": "aws_region",
                "s3_bucket": "s3_bucket",
                "source": "S3",
            },
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base_data_source = await response.parse()
            assert_matches_type(KnowledgeBaseDataSource, knowledge_base_data_source, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        knowledge_base_data_source = await async_client.knowledge_base_data_sources.retrieve(
            "knowledge_base_data_source_id",
        )
        assert_matches_type(KnowledgeBaseDataSource, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_base_data_sources.with_raw_response.retrieve(
            "knowledge_base_data_source_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base_data_source = await response.parse()
        assert_matches_type(KnowledgeBaseDataSource, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_base_data_sources.with_streaming_response.retrieve(
            "knowledge_base_data_source_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base_data_source = await response.parse()
            assert_matches_type(KnowledgeBaseDataSource, knowledge_base_data_source, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `knowledge_base_data_source_id` but received ''"
        ):
            await async_client.knowledge_base_data_sources.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        knowledge_base_data_source = await async_client.knowledge_base_data_sources.update(
            knowledge_base_data_source_id="knowledge_base_data_source_id",
        )
        assert_matches_type(KnowledgeBaseDataSource, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        knowledge_base_data_source = await async_client.knowledge_base_data_sources.update(
            knowledge_base_data_source_id="knowledge_base_data_source_id",
            data_source_auth_config={
                "client_secret": "client_secret",
                "source": "SharePoint",
                "encrypted": True,
            },
            description="description",
            name="name",
            tagging_information={
                "tags_to_apply": {"foo": "bar"},
                "type": "all",
            },
        )
        assert_matches_type(KnowledgeBaseDataSource, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_base_data_sources.with_raw_response.update(
            knowledge_base_data_source_id="knowledge_base_data_source_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base_data_source = await response.parse()
        assert_matches_type(KnowledgeBaseDataSource, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_base_data_sources.with_streaming_response.update(
            knowledge_base_data_source_id="knowledge_base_data_source_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base_data_source = await response.parse()
            assert_matches_type(KnowledgeBaseDataSource, knowledge_base_data_source, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `knowledge_base_data_source_id` but received ''"
        ):
            await async_client.knowledge_base_data_sources.with_raw_response.update(
                knowledge_base_data_source_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        knowledge_base_data_source = await async_client.knowledge_base_data_sources.list()
        assert_matches_type(AsyncPageResponse[KnowledgeBaseDataSource], knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        knowledge_base_data_source = await async_client.knowledge_base_data_sources.list(
            account_id="account_id",
            limit=1,
            name=0,
            page=1,
        )
        assert_matches_type(AsyncPageResponse[KnowledgeBaseDataSource], knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_base_data_sources.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base_data_source = await response.parse()
        assert_matches_type(AsyncPageResponse[KnowledgeBaseDataSource], knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_base_data_sources.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base_data_source = await response.parse()
            assert_matches_type(
                AsyncPageResponse[KnowledgeBaseDataSource], knowledge_base_data_source, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        knowledge_base_data_source = await async_client.knowledge_base_data_sources.delete(
            "knowledge_base_data_source_id",
        )
        assert_matches_type(GenericDeleteResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_base_data_sources.with_raw_response.delete(
            "knowledge_base_data_source_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base_data_source = await response.parse()
        assert_matches_type(GenericDeleteResponse, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_base_data_sources.with_streaming_response.delete(
            "knowledge_base_data_source_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base_data_source = await response.parse()
            assert_matches_type(GenericDeleteResponse, knowledge_base_data_source, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `knowledge_base_data_source_id` but received ''"
        ):
            await async_client.knowledge_base_data_sources.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_verify(self, async_client: AsyncSGPClient) -> None:
        knowledge_base_data_source = await async_client.knowledge_base_data_sources.verify(
            "knowledge_base_data_source_id",
        )
        assert_matches_type(object, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_raw_response_verify(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.knowledge_base_data_sources.with_raw_response.verify(
            "knowledge_base_data_source_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        knowledge_base_data_source = await response.parse()
        assert_matches_type(object, knowledge_base_data_source, path=["response"])

    @parametrize
    async def test_streaming_response_verify(self, async_client: AsyncSGPClient) -> None:
        async with async_client.knowledge_base_data_sources.with_streaming_response.verify(
            "knowledge_base_data_source_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            knowledge_base_data_source = await response.parse()
            assert_matches_type(object, knowledge_base_data_source, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_verify(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `knowledge_base_data_source_id` but received ''"
        ):
            await async_client.knowledge_base_data_sources.with_raw_response.verify(
                "",
            )
