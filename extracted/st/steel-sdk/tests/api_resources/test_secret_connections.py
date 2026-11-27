# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from steel import Steel, AsyncSteel
from steel.types import (
    SecretConnectionListResponse,
    SecretConnectionCreateResponse,
    SecretConnectionUpdateResponse,
    SecretConnectionRetrieveResponse,
)
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSecretConnections:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Steel) -> None:
        secret_connection = client.secret_connections.create(
            auth={},
            name="x",
            provider="1password",
        )
        assert_matches_type(SecretConnectionCreateResponse, secret_connection, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Steel) -> None:
        secret_connection = client.secret_connections.create(
            auth={
                "token": "x",
                "mount": "x",
                "role_id": "x",
                "secret_id": "x",
                "service_account_token": "x",
                "type": "token",
            },
            name="x",
            provider="1password",
            config={
                "address": "x",
                "ca_pem": "x",
                "namespace": "x",
            },
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            token_budget={
                "burst": 2,
                "refill_per_second": 0.001,
            },
        )
        assert_matches_type(SecretConnectionCreateResponse, secret_connection, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Steel) -> None:
        response = client.secret_connections.with_raw_response.create(
            auth={},
            name="x",
            provider="1password",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        secret_connection = response.parse()
        assert_matches_type(SecretConnectionCreateResponse, secret_connection, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Steel) -> None:
        with client.secret_connections.with_streaming_response.create(
            auth={},
            name="x",
            provider="1password",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            secret_connection = response.parse()
            assert_matches_type(SecretConnectionCreateResponse, secret_connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Steel) -> None:
        secret_connection = client.secret_connections.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SecretConnectionRetrieveResponse, secret_connection, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Steel) -> None:
        secret_connection = client.secret_connections.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SecretConnectionRetrieveResponse, secret_connection, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Steel) -> None:
        response = client.secret_connections.with_raw_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        secret_connection = response.parse()
        assert_matches_type(SecretConnectionRetrieveResponse, secret_connection, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Steel) -> None:
        with client.secret_connections.with_streaming_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            secret_connection = response.parse()
            assert_matches_type(SecretConnectionRetrieveResponse, secret_connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.secret_connections.with_raw_response.retrieve(
                id="",
            )

    @parametrize
    def test_method_update(self, client: Steel) -> None:
        secret_connection = client.secret_connections.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SecretConnectionUpdateResponse, secret_connection, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Steel) -> None:
        secret_connection = client.secret_connections.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            auth={
                "token": "x",
                "mount": "x",
                "role_id": "x",
                "secret_id": "x",
                "service_account_token": "x",
                "type": "token",
            },
            config={
                "address": "x",
                "ca_pem": "x",
                "namespace": "x",
            },
            enabled=True,
            name="x",
            token_budget={
                "burst": 2,
                "refill_per_second": 0.001,
            },
        )
        assert_matches_type(SecretConnectionUpdateResponse, secret_connection, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Steel) -> None:
        response = client.secret_connections.with_raw_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        secret_connection = response.parse()
        assert_matches_type(SecretConnectionUpdateResponse, secret_connection, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Steel) -> None:
        with client.secret_connections.with_streaming_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            secret_connection = response.parse()
            assert_matches_type(SecretConnectionUpdateResponse, secret_connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.secret_connections.with_raw_response.update(
                id="",
            )

    @parametrize
    def test_method_list(self, client: Steel) -> None:
        secret_connection = client.secret_connections.list()
        assert_matches_type(SecretConnectionListResponse, secret_connection, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Steel) -> None:
        secret_connection = client.secret_connections.list(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SecretConnectionListResponse, secret_connection, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Steel) -> None:
        response = client.secret_connections.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        secret_connection = response.parse()
        assert_matches_type(SecretConnectionListResponse, secret_connection, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Steel) -> None:
        with client.secret_connections.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            secret_connection = response.parse()
            assert_matches_type(SecretConnectionListResponse, secret_connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Steel) -> None:
        secret_connection = client.secret_connections.delete(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert secret_connection is None

    @parametrize
    def test_method_delete_with_all_params(self, client: Steel) -> None:
        secret_connection = client.secret_connections.delete(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert secret_connection is None

    @parametrize
    def test_raw_response_delete(self, client: Steel) -> None:
        response = client.secret_connections.with_raw_response.delete(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        secret_connection = response.parse()
        assert secret_connection is None

    @parametrize
    def test_streaming_response_delete(self, client: Steel) -> None:
        with client.secret_connections.with_streaming_response.delete(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            secret_connection = response.parse()
            assert secret_connection is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.secret_connections.with_raw_response.delete(
                id="",
            )

    @parametrize
    def test_method_test(self, client: Steel) -> None:
        secret_connection = client.secret_connections.test(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert secret_connection is None

    @parametrize
    def test_method_test_with_all_params(self, client: Steel) -> None:
        secret_connection = client.secret_connections.test(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert secret_connection is None

    @parametrize
    def test_raw_response_test(self, client: Steel) -> None:
        response = client.secret_connections.with_raw_response.test(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        secret_connection = response.parse()
        assert secret_connection is None

    @parametrize
    def test_streaming_response_test(self, client: Steel) -> None:
        with client.secret_connections.with_streaming_response.test(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            secret_connection = response.parse()
            assert secret_connection is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_test(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.secret_connections.with_raw_response.test(
                id="",
            )


class TestAsyncSecretConnections:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSteel) -> None:
        secret_connection = await async_client.secret_connections.create(
            auth={},
            name="x",
            provider="1password",
        )
        assert_matches_type(SecretConnectionCreateResponse, secret_connection, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSteel) -> None:
        secret_connection = await async_client.secret_connections.create(
            auth={
                "token": "x",
                "mount": "x",
                "role_id": "x",
                "secret_id": "x",
                "service_account_token": "x",
                "type": "token",
            },
            name="x",
            provider="1password",
            config={
                "address": "x",
                "ca_pem": "x",
                "namespace": "x",
            },
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            token_budget={
                "burst": 2,
                "refill_per_second": 0.001,
            },
        )
        assert_matches_type(SecretConnectionCreateResponse, secret_connection, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSteel) -> None:
        response = await async_client.secret_connections.with_raw_response.create(
            auth={},
            name="x",
            provider="1password",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        secret_connection = await response.parse()
        assert_matches_type(SecretConnectionCreateResponse, secret_connection, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSteel) -> None:
        async with async_client.secret_connections.with_streaming_response.create(
            auth={},
            name="x",
            provider="1password",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            secret_connection = await response.parse()
            assert_matches_type(SecretConnectionCreateResponse, secret_connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSteel) -> None:
        secret_connection = await async_client.secret_connections.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SecretConnectionRetrieveResponse, secret_connection, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSteel) -> None:
        secret_connection = await async_client.secret_connections.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SecretConnectionRetrieveResponse, secret_connection, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSteel) -> None:
        response = await async_client.secret_connections.with_raw_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        secret_connection = await response.parse()
        assert_matches_type(SecretConnectionRetrieveResponse, secret_connection, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSteel) -> None:
        async with async_client.secret_connections.with_streaming_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            secret_connection = await response.parse()
            assert_matches_type(SecretConnectionRetrieveResponse, secret_connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.secret_connections.with_raw_response.retrieve(
                id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSteel) -> None:
        secret_connection = await async_client.secret_connections.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SecretConnectionUpdateResponse, secret_connection, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSteel) -> None:
        secret_connection = await async_client.secret_connections.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            auth={
                "token": "x",
                "mount": "x",
                "role_id": "x",
                "secret_id": "x",
                "service_account_token": "x",
                "type": "token",
            },
            config={
                "address": "x",
                "ca_pem": "x",
                "namespace": "x",
            },
            enabled=True,
            name="x",
            token_budget={
                "burst": 2,
                "refill_per_second": 0.001,
            },
        )
        assert_matches_type(SecretConnectionUpdateResponse, secret_connection, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSteel) -> None:
        response = await async_client.secret_connections.with_raw_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        secret_connection = await response.parse()
        assert_matches_type(SecretConnectionUpdateResponse, secret_connection, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSteel) -> None:
        async with async_client.secret_connections.with_streaming_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            secret_connection = await response.parse()
            assert_matches_type(SecretConnectionUpdateResponse, secret_connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.secret_connections.with_raw_response.update(
                id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSteel) -> None:
        secret_connection = await async_client.secret_connections.list()
        assert_matches_type(SecretConnectionListResponse, secret_connection, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSteel) -> None:
        secret_connection = await async_client.secret_connections.list(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SecretConnectionListResponse, secret_connection, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSteel) -> None:
        response = await async_client.secret_connections.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        secret_connection = await response.parse()
        assert_matches_type(SecretConnectionListResponse, secret_connection, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSteel) -> None:
        async with async_client.secret_connections.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            secret_connection = await response.parse()
            assert_matches_type(SecretConnectionListResponse, secret_connection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSteel) -> None:
        secret_connection = await async_client.secret_connections.delete(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert secret_connection is None

    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncSteel) -> None:
        secret_connection = await async_client.secret_connections.delete(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert secret_connection is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSteel) -> None:
        response = await async_client.secret_connections.with_raw_response.delete(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        secret_connection = await response.parse()
        assert secret_connection is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSteel) -> None:
        async with async_client.secret_connections.with_streaming_response.delete(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            secret_connection = await response.parse()
            assert secret_connection is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.secret_connections.with_raw_response.delete(
                id="",
            )

    @parametrize
    async def test_method_test(self, async_client: AsyncSteel) -> None:
        secret_connection = await async_client.secret_connections.test(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert secret_connection is None

    @parametrize
    async def test_method_test_with_all_params(self, async_client: AsyncSteel) -> None:
        secret_connection = await async_client.secret_connections.test(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert secret_connection is None

    @parametrize
    async def test_raw_response_test(self, async_client: AsyncSteel) -> None:
        response = await async_client.secret_connections.with_raw_response.test(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        secret_connection = await response.parse()
        assert secret_connection is None

    @parametrize
    async def test_streaming_response_test(self, async_client: AsyncSteel) -> None:
        async with async_client.secret_connections.with_streaming_response.test(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            secret_connection = await response.parse()
            assert secret_connection is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_test(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.secret_connections.with_raw_response.test(
                id="",
            )
