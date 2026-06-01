# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from supermemory import Supermemory, AsyncSupermemory
from tests.utils import assert_matches_type
from supermemory.types import (
    ConnectionListResponse,
    ConnectionCreateResponse,
    ConnectionGetByIDResponse,
    ConnectionGetByTagResponse,
    ConnectionConfigureResponse,
    ConnectionResourcesResponse,
    ConnectionDeleteByIDResponse,
    ConnectionListDocumentsResponse,
    ConnectionDeleteByProviderResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestConnections:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create(self, client: Supermemory) -> None:
        connection = client.connections.create(
            provider="notion",
        )
        assert_matches_type(ConnectionCreateResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Supermemory) -> None:
        connection = client.connections.create(
            provider="notion",
            container_tag="containerTag",
            container_tags=["_:_k--W2K_1V"],
            document_limit=1,
            metadata={"foo": "string"},
            redirect_url="redirectUrl",
        )
        assert_matches_type(ConnectionCreateResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Supermemory) -> None:
        response = client.connections.with_raw_response.create(
            provider="notion",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        connection = response.parse()
        assert_matches_type(ConnectionCreateResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Supermemory) -> None:
        with client.connections.with_streaming_response.create(
            provider="notion",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            connection = response.parse()
            assert_matches_type(ConnectionCreateResponse, connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Supermemory) -> None:
        connection = client.connections.list()
        assert_matches_type(ConnectionListResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Supermemory) -> None:
        connection = client.connections.list(
            container_tags=["user_123", "project_123"],
        )
        assert_matches_type(ConnectionListResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Supermemory) -> None:
        response = client.connections.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        connection = response.parse()
        assert_matches_type(ConnectionListResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Supermemory) -> None:
        with client.connections.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            connection = response.parse()
            assert_matches_type(ConnectionListResponse, connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_configure(self, client: Supermemory) -> None:
        connection = client.connections.configure(
            connection_id="connectionId",
            resources=[{"foo": "bar"}],
        )
        assert_matches_type(ConnectionConfigureResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_configure(self, client: Supermemory) -> None:
        response = client.connections.with_raw_response.configure(
            connection_id="connectionId",
            resources=[{"foo": "bar"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        connection = response.parse()
        assert_matches_type(ConnectionConfigureResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_configure(self, client: Supermemory) -> None:
        with client.connections.with_streaming_response.configure(
            connection_id="connectionId",
            resources=[{"foo": "bar"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            connection = response.parse()
            assert_matches_type(ConnectionConfigureResponse, connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_configure(self, client: Supermemory) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `connection_id` but received ''"):
            client.connections.with_raw_response.configure(
                connection_id="",
                resources=[{"foo": "bar"}],
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_delete_by_id(self, client: Supermemory) -> None:
        connection = client.connections.delete_by_id(
            connection_id="connectionId",
        )
        assert_matches_type(ConnectionDeleteByIDResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_delete_by_id_with_all_params(self, client: Supermemory) -> None:
        connection = client.connections.delete_by_id(
            connection_id="connectionId",
            delete_documents="deleteDocuments",
        )
        assert_matches_type(ConnectionDeleteByIDResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_delete_by_id(self, client: Supermemory) -> None:
        response = client.connections.with_raw_response.delete_by_id(
            connection_id="connectionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        connection = response.parse()
        assert_matches_type(ConnectionDeleteByIDResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_delete_by_id(self, client: Supermemory) -> None:
        with client.connections.with_streaming_response.delete_by_id(
            connection_id="connectionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            connection = response.parse()
            assert_matches_type(ConnectionDeleteByIDResponse, connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_delete_by_id(self, client: Supermemory) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `connection_id` but received ''"):
            client.connections.with_raw_response.delete_by_id(
                connection_id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_delete_by_provider(self, client: Supermemory) -> None:
        connection = client.connections.delete_by_provider(
            provider="notion",
            container_tags=["user_123", "project_123"],
        )
        assert_matches_type(ConnectionDeleteByProviderResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_delete_by_provider(self, client: Supermemory) -> None:
        response = client.connections.with_raw_response.delete_by_provider(
            provider="notion",
            container_tags=["user_123", "project_123"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        connection = response.parse()
        assert_matches_type(ConnectionDeleteByProviderResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_delete_by_provider(self, client: Supermemory) -> None:
        with client.connections.with_streaming_response.delete_by_provider(
            provider="notion",
            container_tags=["user_123", "project_123"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            connection = response.parse()
            assert_matches_type(ConnectionDeleteByProviderResponse, connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_get_by_id(self, client: Supermemory) -> None:
        connection = client.connections.get_by_id(
            "connectionId",
        )
        assert_matches_type(ConnectionGetByIDResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_get_by_id(self, client: Supermemory) -> None:
        response = client.connections.with_raw_response.get_by_id(
            "connectionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        connection = response.parse()
        assert_matches_type(ConnectionGetByIDResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_get_by_id(self, client: Supermemory) -> None:
        with client.connections.with_streaming_response.get_by_id(
            "connectionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            connection = response.parse()
            assert_matches_type(ConnectionGetByIDResponse, connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_get_by_id(self, client: Supermemory) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `connection_id` but received ''"):
            client.connections.with_raw_response.get_by_id(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_get_by_tag(self, client: Supermemory) -> None:
        connection = client.connections.get_by_tag(
            provider="notion",
            container_tags=["user_123", "project_123"],
        )
        assert_matches_type(ConnectionGetByTagResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_get_by_tag(self, client: Supermemory) -> None:
        response = client.connections.with_raw_response.get_by_tag(
            provider="notion",
            container_tags=["user_123", "project_123"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        connection = response.parse()
        assert_matches_type(ConnectionGetByTagResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_get_by_tag(self, client: Supermemory) -> None:
        with client.connections.with_streaming_response.get_by_tag(
            provider="notion",
            container_tags=["user_123", "project_123"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            connection = response.parse()
            assert_matches_type(ConnectionGetByTagResponse, connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_import(self, client: Supermemory) -> None:
        connection = client.connections.import_(
            provider="notion",
        )
        assert_matches_type(str, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_import_with_all_params(self, client: Supermemory) -> None:
        connection = client.connections.import_(
            provider="notion",
            container_tags=["user_123", "project_123"],
        )
        assert_matches_type(str, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_import(self, client: Supermemory) -> None:
        response = client.connections.with_raw_response.import_(
            provider="notion",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        connection = response.parse()
        assert_matches_type(str, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_import(self, client: Supermemory) -> None:
        with client.connections.with_streaming_response.import_(
            provider="notion",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            connection = response.parse()
            assert_matches_type(str, connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_documents(self, client: Supermemory) -> None:
        connection = client.connections.list_documents(
            provider="notion",
        )
        assert_matches_type(ConnectionListDocumentsResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_documents_with_all_params(self, client: Supermemory) -> None:
        connection = client.connections.list_documents(
            provider="notion",
            container_tags=["user_123", "project_123"],
        )
        assert_matches_type(ConnectionListDocumentsResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list_documents(self, client: Supermemory) -> None:
        response = client.connections.with_raw_response.list_documents(
            provider="notion",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        connection = response.parse()
        assert_matches_type(ConnectionListDocumentsResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list_documents(self, client: Supermemory) -> None:
        with client.connections.with_streaming_response.list_documents(
            provider="notion",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            connection = response.parse()
            assert_matches_type(ConnectionListDocumentsResponse, connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_resources(self, client: Supermemory) -> None:
        connection = client.connections.resources(
            connection_id="connectionId",
        )
        assert_matches_type(ConnectionResourcesResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_resources_with_all_params(self, client: Supermemory) -> None:
        connection = client.connections.resources(
            connection_id="connectionId",
            page=0,
            parent_id="parent_id",
            per_page=0,
        )
        assert_matches_type(ConnectionResourcesResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_resources(self, client: Supermemory) -> None:
        response = client.connections.with_raw_response.resources(
            connection_id="connectionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        connection = response.parse()
        assert_matches_type(ConnectionResourcesResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_resources(self, client: Supermemory) -> None:
        with client.connections.with_streaming_response.resources(
            connection_id="connectionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            connection = response.parse()
            assert_matches_type(ConnectionResourcesResponse, connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_resources(self, client: Supermemory) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `connection_id` but received ''"):
            client.connections.with_raw_response.resources(
                connection_id="",
            )


class TestAsyncConnections:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncSupermemory) -> None:
        connection = await async_client.connections.create(
            provider="notion",
        )
        assert_matches_type(ConnectionCreateResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSupermemory) -> None:
        connection = await async_client.connections.create(
            provider="notion",
            container_tag="containerTag",
            container_tags=["_:_k--W2K_1V"],
            document_limit=1,
            metadata={"foo": "string"},
            redirect_url="redirectUrl",
        )
        assert_matches_type(ConnectionCreateResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSupermemory) -> None:
        response = await async_client.connections.with_raw_response.create(
            provider="notion",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        connection = await response.parse()
        assert_matches_type(ConnectionCreateResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSupermemory) -> None:
        async with async_client.connections.with_streaming_response.create(
            provider="notion",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            connection = await response.parse()
            assert_matches_type(ConnectionCreateResponse, connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncSupermemory) -> None:
        connection = await async_client.connections.list()
        assert_matches_type(ConnectionListResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSupermemory) -> None:
        connection = await async_client.connections.list(
            container_tags=["user_123", "project_123"],
        )
        assert_matches_type(ConnectionListResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSupermemory) -> None:
        response = await async_client.connections.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        connection = await response.parse()
        assert_matches_type(ConnectionListResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSupermemory) -> None:
        async with async_client.connections.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            connection = await response.parse()
            assert_matches_type(ConnectionListResponse, connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_configure(self, async_client: AsyncSupermemory) -> None:
        connection = await async_client.connections.configure(
            connection_id="connectionId",
            resources=[{"foo": "bar"}],
        )
        assert_matches_type(ConnectionConfigureResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_configure(self, async_client: AsyncSupermemory) -> None:
        response = await async_client.connections.with_raw_response.configure(
            connection_id="connectionId",
            resources=[{"foo": "bar"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        connection = await response.parse()
        assert_matches_type(ConnectionConfigureResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_configure(self, async_client: AsyncSupermemory) -> None:
        async with async_client.connections.with_streaming_response.configure(
            connection_id="connectionId",
            resources=[{"foo": "bar"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            connection = await response.parse()
            assert_matches_type(ConnectionConfigureResponse, connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_configure(self, async_client: AsyncSupermemory) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `connection_id` but received ''"):
            await async_client.connections.with_raw_response.configure(
                connection_id="",
                resources=[{"foo": "bar"}],
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_delete_by_id(self, async_client: AsyncSupermemory) -> None:
        connection = await async_client.connections.delete_by_id(
            connection_id="connectionId",
        )
        assert_matches_type(ConnectionDeleteByIDResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_delete_by_id_with_all_params(self, async_client: AsyncSupermemory) -> None:
        connection = await async_client.connections.delete_by_id(
            connection_id="connectionId",
            delete_documents="deleteDocuments",
        )
        assert_matches_type(ConnectionDeleteByIDResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_delete_by_id(self, async_client: AsyncSupermemory) -> None:
        response = await async_client.connections.with_raw_response.delete_by_id(
            connection_id="connectionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        connection = await response.parse()
        assert_matches_type(ConnectionDeleteByIDResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_delete_by_id(self, async_client: AsyncSupermemory) -> None:
        async with async_client.connections.with_streaming_response.delete_by_id(
            connection_id="connectionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            connection = await response.parse()
            assert_matches_type(ConnectionDeleteByIDResponse, connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_delete_by_id(self, async_client: AsyncSupermemory) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `connection_id` but received ''"):
            await async_client.connections.with_raw_response.delete_by_id(
                connection_id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_delete_by_provider(self, async_client: AsyncSupermemory) -> None:
        connection = await async_client.connections.delete_by_provider(
            provider="notion",
            container_tags=["user_123", "project_123"],
        )
        assert_matches_type(ConnectionDeleteByProviderResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_delete_by_provider(self, async_client: AsyncSupermemory) -> None:
        response = await async_client.connections.with_raw_response.delete_by_provider(
            provider="notion",
            container_tags=["user_123", "project_123"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        connection = await response.parse()
        assert_matches_type(ConnectionDeleteByProviderResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_delete_by_provider(self, async_client: AsyncSupermemory) -> None:
        async with async_client.connections.with_streaming_response.delete_by_provider(
            provider="notion",
            container_tags=["user_123", "project_123"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            connection = await response.parse()
            assert_matches_type(ConnectionDeleteByProviderResponse, connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_get_by_id(self, async_client: AsyncSupermemory) -> None:
        connection = await async_client.connections.get_by_id(
            "connectionId",
        )
        assert_matches_type(ConnectionGetByIDResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_get_by_id(self, async_client: AsyncSupermemory) -> None:
        response = await async_client.connections.with_raw_response.get_by_id(
            "connectionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        connection = await response.parse()
        assert_matches_type(ConnectionGetByIDResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_get_by_id(self, async_client: AsyncSupermemory) -> None:
        async with async_client.connections.with_streaming_response.get_by_id(
            "connectionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            connection = await response.parse()
            assert_matches_type(ConnectionGetByIDResponse, connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_get_by_id(self, async_client: AsyncSupermemory) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `connection_id` but received ''"):
            await async_client.connections.with_raw_response.get_by_id(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_get_by_tag(self, async_client: AsyncSupermemory) -> None:
        connection = await async_client.connections.get_by_tag(
            provider="notion",
            container_tags=["user_123", "project_123"],
        )
        assert_matches_type(ConnectionGetByTagResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_get_by_tag(self, async_client: AsyncSupermemory) -> None:
        response = await async_client.connections.with_raw_response.get_by_tag(
            provider="notion",
            container_tags=["user_123", "project_123"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        connection = await response.parse()
        assert_matches_type(ConnectionGetByTagResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_get_by_tag(self, async_client: AsyncSupermemory) -> None:
        async with async_client.connections.with_streaming_response.get_by_tag(
            provider="notion",
            container_tags=["user_123", "project_123"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            connection = await response.parse()
            assert_matches_type(ConnectionGetByTagResponse, connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_import(self, async_client: AsyncSupermemory) -> None:
        connection = await async_client.connections.import_(
            provider="notion",
        )
        assert_matches_type(str, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_import_with_all_params(self, async_client: AsyncSupermemory) -> None:
        connection = await async_client.connections.import_(
            provider="notion",
            container_tags=["user_123", "project_123"],
        )
        assert_matches_type(str, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_import(self, async_client: AsyncSupermemory) -> None:
        response = await async_client.connections.with_raw_response.import_(
            provider="notion",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        connection = await response.parse()
        assert_matches_type(str, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_import(self, async_client: AsyncSupermemory) -> None:
        async with async_client.connections.with_streaming_response.import_(
            provider="notion",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            connection = await response.parse()
            assert_matches_type(str, connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_documents(self, async_client: AsyncSupermemory) -> None:
        connection = await async_client.connections.list_documents(
            provider="notion",
        )
        assert_matches_type(ConnectionListDocumentsResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_documents_with_all_params(self, async_client: AsyncSupermemory) -> None:
        connection = await async_client.connections.list_documents(
            provider="notion",
            container_tags=["user_123", "project_123"],
        )
        assert_matches_type(ConnectionListDocumentsResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list_documents(self, async_client: AsyncSupermemory) -> None:
        response = await async_client.connections.with_raw_response.list_documents(
            provider="notion",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        connection = await response.parse()
        assert_matches_type(ConnectionListDocumentsResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list_documents(self, async_client: AsyncSupermemory) -> None:
        async with async_client.connections.with_streaming_response.list_documents(
            provider="notion",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            connection = await response.parse()
            assert_matches_type(ConnectionListDocumentsResponse, connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_resources(self, async_client: AsyncSupermemory) -> None:
        connection = await async_client.connections.resources(
            connection_id="connectionId",
        )
        assert_matches_type(ConnectionResourcesResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_resources_with_all_params(self, async_client: AsyncSupermemory) -> None:
        connection = await async_client.connections.resources(
            connection_id="connectionId",
            page=0,
            parent_id="parent_id",
            per_page=0,
        )
        assert_matches_type(ConnectionResourcesResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_resources(self, async_client: AsyncSupermemory) -> None:
        response = await async_client.connections.with_raw_response.resources(
            connection_id="connectionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        connection = await response.parse()
        assert_matches_type(ConnectionResourcesResponse, connection, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_resources(self, async_client: AsyncSupermemory) -> None:
        async with async_client.connections.with_streaming_response.resources(
            connection_id="connectionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            connection = await response.parse()
            assert_matches_type(ConnectionResourcesResponse, connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_resources(self, async_client: AsyncSupermemory) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `connection_id` but received ''"):
            await async_client.connections.with_raw_response.resources(
                connection_id="",
            )
