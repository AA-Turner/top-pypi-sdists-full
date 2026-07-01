# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import (
    GenericModelResponse,
    ModelServerRollbackResponse,
    ModelServerUpdateBackendResponse,
)
from scale_gp.pagination import SyncTopLevelArray, AsyncTopLevelArray
from scale_gp.types.shared import ModelServerInfo

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestModelServers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        model_server = client.model_servers.create(
            model_deployment_id="model_deployment_id",
            name="name",
        )
        assert_matches_type(ModelServerInfo, model_server, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        model_server = client.model_servers.create(
            model_deployment_id="model_deployment_id",
            name="name",
            alias="alias",
        )
        assert_matches_type(ModelServerInfo, model_server, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.model_servers.with_raw_response.create(
            model_deployment_id="model_deployment_id",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_server = response.parse()
        assert_matches_type(ModelServerInfo, model_server, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.model_servers.with_streaming_response.create(
            model_deployment_id="model_deployment_id",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_server = response.parse()
            assert_matches_type(ModelServerInfo, model_server, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        model_server = client.model_servers.retrieve(
            "model_server_id",
        )
        assert_matches_type(ModelServerInfo, model_server, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.model_servers.with_raw_response.retrieve(
            "model_server_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_server = response.parse()
        assert_matches_type(ModelServerInfo, model_server, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.model_servers.with_streaming_response.retrieve(
            "model_server_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_server = response.parse()
            assert_matches_type(ModelServerInfo, model_server, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_server_id` but received ''"):
            client.model_servers.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        model_server = client.model_servers.list()
        assert_matches_type(SyncTopLevelArray[ModelServerInfo], model_server, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.model_servers.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_server = response.parse()
        assert_matches_type(SyncTopLevelArray[ModelServerInfo], model_server, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.model_servers.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_server = response.parse()
            assert_matches_type(SyncTopLevelArray[ModelServerInfo], model_server, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_execute(self, client: SGPClient) -> None:
        model_server = client.model_servers.execute(
            model_server_id="model_server_id",
        )
        assert_matches_type(GenericModelResponse, model_server, path=["response"])

    @parametrize
    def test_method_execute_with_all_params(self, client: SGPClient) -> None:
        model_server = client.model_servers.execute(
            model_server_id="model_server_id",
            stream=True,
        )
        assert_matches_type(GenericModelResponse, model_server, path=["response"])

    @parametrize
    def test_raw_response_execute(self, client: SGPClient) -> None:
        response = client.model_servers.with_raw_response.execute(
            model_server_id="model_server_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_server = response.parse()
        assert_matches_type(GenericModelResponse, model_server, path=["response"])

    @parametrize
    def test_streaming_response_execute(self, client: SGPClient) -> None:
        with client.model_servers.with_streaming_response.execute(
            model_server_id="model_server_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_server = response.parse()
            assert_matches_type(GenericModelResponse, model_server, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_execute(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_server_id` but received ''"):
            client.model_servers.with_raw_response.execute(
                model_server_id="",
            )

    @parametrize
    def test_method_rollback(self, client: SGPClient) -> None:
        model_server = client.model_servers.rollback(
            "model_server_id",
        )
        assert_matches_type(ModelServerRollbackResponse, model_server, path=["response"])

    @parametrize
    def test_raw_response_rollback(self, client: SGPClient) -> None:
        response = client.model_servers.with_raw_response.rollback(
            "model_server_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_server = response.parse()
        assert_matches_type(ModelServerRollbackResponse, model_server, path=["response"])

    @parametrize
    def test_streaming_response_rollback(self, client: SGPClient) -> None:
        with client.model_servers.with_streaming_response.rollback(
            "model_server_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_server = response.parse()
            assert_matches_type(ModelServerRollbackResponse, model_server, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_rollback(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_server_id` but received ''"):
            client.model_servers.with_raw_response.rollback(
                "",
            )

    @parametrize
    def test_method_update_backend(self, client: SGPClient) -> None:
        model_server = client.model_servers.update_backend(
            model_server_id="model_server_id",
            new_model_deployment_id="new_model_deployment_id",
        )
        assert_matches_type(ModelServerUpdateBackendResponse, model_server, path=["response"])

    @parametrize
    def test_raw_response_update_backend(self, client: SGPClient) -> None:
        response = client.model_servers.with_raw_response.update_backend(
            model_server_id="model_server_id",
            new_model_deployment_id="new_model_deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_server = response.parse()
        assert_matches_type(ModelServerUpdateBackendResponse, model_server, path=["response"])

    @parametrize
    def test_streaming_response_update_backend(self, client: SGPClient) -> None:
        with client.model_servers.with_streaming_response.update_backend(
            model_server_id="model_server_id",
            new_model_deployment_id="new_model_deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_server = response.parse()
            assert_matches_type(ModelServerUpdateBackendResponse, model_server, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update_backend(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_server_id` but received ''"):
            client.model_servers.with_raw_response.update_backend(
                model_server_id="",
                new_model_deployment_id="new_model_deployment_id",
            )


class TestAsyncModelServers:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        model_server = await async_client.model_servers.create(
            model_deployment_id="model_deployment_id",
            name="name",
        )
        assert_matches_type(ModelServerInfo, model_server, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        model_server = await async_client.model_servers.create(
            model_deployment_id="model_deployment_id",
            name="name",
            alias="alias",
        )
        assert_matches_type(ModelServerInfo, model_server, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.model_servers.with_raw_response.create(
            model_deployment_id="model_deployment_id",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_server = await response.parse()
        assert_matches_type(ModelServerInfo, model_server, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.model_servers.with_streaming_response.create(
            model_deployment_id="model_deployment_id",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_server = await response.parse()
            assert_matches_type(ModelServerInfo, model_server, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        model_server = await async_client.model_servers.retrieve(
            "model_server_id",
        )
        assert_matches_type(ModelServerInfo, model_server, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.model_servers.with_raw_response.retrieve(
            "model_server_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_server = await response.parse()
        assert_matches_type(ModelServerInfo, model_server, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.model_servers.with_streaming_response.retrieve(
            "model_server_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_server = await response.parse()
            assert_matches_type(ModelServerInfo, model_server, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_server_id` but received ''"):
            await async_client.model_servers.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        model_server = await async_client.model_servers.list()
        assert_matches_type(AsyncTopLevelArray[ModelServerInfo], model_server, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.model_servers.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_server = await response.parse()
        assert_matches_type(AsyncTopLevelArray[ModelServerInfo], model_server, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.model_servers.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_server = await response.parse()
            assert_matches_type(AsyncTopLevelArray[ModelServerInfo], model_server, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_execute(self, async_client: AsyncSGPClient) -> None:
        model_server = await async_client.model_servers.execute(
            model_server_id="model_server_id",
        )
        assert_matches_type(GenericModelResponse, model_server, path=["response"])

    @parametrize
    async def test_method_execute_with_all_params(self, async_client: AsyncSGPClient) -> None:
        model_server = await async_client.model_servers.execute(
            model_server_id="model_server_id",
            stream=True,
        )
        assert_matches_type(GenericModelResponse, model_server, path=["response"])

    @parametrize
    async def test_raw_response_execute(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.model_servers.with_raw_response.execute(
            model_server_id="model_server_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_server = await response.parse()
        assert_matches_type(GenericModelResponse, model_server, path=["response"])

    @parametrize
    async def test_streaming_response_execute(self, async_client: AsyncSGPClient) -> None:
        async with async_client.model_servers.with_streaming_response.execute(
            model_server_id="model_server_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_server = await response.parse()
            assert_matches_type(GenericModelResponse, model_server, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_execute(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_server_id` but received ''"):
            await async_client.model_servers.with_raw_response.execute(
                model_server_id="",
            )

    @parametrize
    async def test_method_rollback(self, async_client: AsyncSGPClient) -> None:
        model_server = await async_client.model_servers.rollback(
            "model_server_id",
        )
        assert_matches_type(ModelServerRollbackResponse, model_server, path=["response"])

    @parametrize
    async def test_raw_response_rollback(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.model_servers.with_raw_response.rollback(
            "model_server_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_server = await response.parse()
        assert_matches_type(ModelServerRollbackResponse, model_server, path=["response"])

    @parametrize
    async def test_streaming_response_rollback(self, async_client: AsyncSGPClient) -> None:
        async with async_client.model_servers.with_streaming_response.rollback(
            "model_server_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_server = await response.parse()
            assert_matches_type(ModelServerRollbackResponse, model_server, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_rollback(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_server_id` but received ''"):
            await async_client.model_servers.with_raw_response.rollback(
                "",
            )

    @parametrize
    async def test_method_update_backend(self, async_client: AsyncSGPClient) -> None:
        model_server = await async_client.model_servers.update_backend(
            model_server_id="model_server_id",
            new_model_deployment_id="new_model_deployment_id",
        )
        assert_matches_type(ModelServerUpdateBackendResponse, model_server, path=["response"])

    @parametrize
    async def test_raw_response_update_backend(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.model_servers.with_raw_response.update_backend(
            model_server_id="model_server_id",
            new_model_deployment_id="new_model_deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_server = await response.parse()
        assert_matches_type(ModelServerUpdateBackendResponse, model_server, path=["response"])

    @parametrize
    async def test_streaming_response_update_backend(self, async_client: AsyncSGPClient) -> None:
        async with async_client.model_servers.with_streaming_response.update_backend(
            model_server_id="model_server_id",
            new_model_deployment_id="new_model_deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_server = await response.parse()
            assert_matches_type(ModelServerUpdateBackendResponse, model_server, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update_backend(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_server_id` but received ''"):
            await async_client.model_servers.with_raw_response.update_backend(
                model_server_id="",
                new_model_deployment_id="new_model_deployment_id",
            )
