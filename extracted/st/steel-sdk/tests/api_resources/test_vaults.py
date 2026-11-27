# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from steel import Steel, AsyncSteel
from steel.types import (
    Vault,
    VaultList,
)
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVaults:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Steel) -> None:
        vault = client.vaults.create(
            name="name",
        )
        assert_matches_type(Vault, vault, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Steel) -> None:
        vault = client.vaults.create(
            name="name",
            description="description",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Vault, vault, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Steel) -> None:
        response = client.vaults.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        vault = response.parse()
        assert_matches_type(Vault, vault, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Steel) -> None:
        with client.vaults.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            vault = response.parse()
            assert_matches_type(Vault, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Steel) -> None:
        vault = client.vaults.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Vault, vault, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Steel) -> None:
        vault = client.vaults.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Vault, vault, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Steel) -> None:
        response = client.vaults.with_raw_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        vault = response.parse()
        assert_matches_type(Vault, vault, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Steel) -> None:
        with client.vaults.with_streaming_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            vault = response.parse()
            assert_matches_type(Vault, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vaults.with_raw_response.retrieve(
                id="",
            )

    @parametrize
    def test_method_update(self, client: Steel) -> None:
        vault = client.vaults.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Vault, vault, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Steel) -> None:
        vault = client.vaults.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            description="description",
            name="name",
        )
        assert_matches_type(Vault, vault, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Steel) -> None:
        response = client.vaults.with_raw_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        vault = response.parse()
        assert_matches_type(Vault, vault, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Steel) -> None:
        with client.vaults.with_streaming_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            vault = response.parse()
            assert_matches_type(Vault, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vaults.with_raw_response.update(
                id="",
            )

    @parametrize
    def test_method_list(self, client: Steel) -> None:
        vault = client.vaults.list()
        assert_matches_type(VaultList, vault, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Steel) -> None:
        vault = client.vaults.list(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(VaultList, vault, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Steel) -> None:
        response = client.vaults.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        vault = response.parse()
        assert_matches_type(VaultList, vault, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Steel) -> None:
        with client.vaults.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            vault = response.parse()
            assert_matches_type(VaultList, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Steel) -> None:
        vault = client.vaults.delete(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert vault is None

    @parametrize
    def test_method_delete_with_all_params(self, client: Steel) -> None:
        vault = client.vaults.delete(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert vault is None

    @parametrize
    def test_raw_response_delete(self, client: Steel) -> None:
        response = client.vaults.with_raw_response.delete(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        vault = response.parse()
        assert vault is None

    @parametrize
    def test_streaming_response_delete(self, client: Steel) -> None:
        with client.vaults.with_streaming_response.delete(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            vault = response.parse()
            assert vault is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vaults.with_raw_response.delete(
                id="",
            )


class TestAsyncVaults:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSteel) -> None:
        vault = await async_client.vaults.create(
            name="name",
        )
        assert_matches_type(Vault, vault, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSteel) -> None:
        vault = await async_client.vaults.create(
            name="name",
            description="description",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Vault, vault, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSteel) -> None:
        response = await async_client.vaults.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        vault = await response.parse()
        assert_matches_type(Vault, vault, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSteel) -> None:
        async with async_client.vaults.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            vault = await response.parse()
            assert_matches_type(Vault, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSteel) -> None:
        vault = await async_client.vaults.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Vault, vault, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSteel) -> None:
        vault = await async_client.vaults.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Vault, vault, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSteel) -> None:
        response = await async_client.vaults.with_raw_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        vault = await response.parse()
        assert_matches_type(Vault, vault, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSteel) -> None:
        async with async_client.vaults.with_streaming_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            vault = await response.parse()
            assert_matches_type(Vault, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vaults.with_raw_response.retrieve(
                id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSteel) -> None:
        vault = await async_client.vaults.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Vault, vault, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSteel) -> None:
        vault = await async_client.vaults.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            description="description",
            name="name",
        )
        assert_matches_type(Vault, vault, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSteel) -> None:
        response = await async_client.vaults.with_raw_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        vault = await response.parse()
        assert_matches_type(Vault, vault, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSteel) -> None:
        async with async_client.vaults.with_streaming_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            vault = await response.parse()
            assert_matches_type(Vault, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vaults.with_raw_response.update(
                id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSteel) -> None:
        vault = await async_client.vaults.list()
        assert_matches_type(VaultList, vault, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSteel) -> None:
        vault = await async_client.vaults.list(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(VaultList, vault, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSteel) -> None:
        response = await async_client.vaults.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        vault = await response.parse()
        assert_matches_type(VaultList, vault, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSteel) -> None:
        async with async_client.vaults.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            vault = await response.parse()
            assert_matches_type(VaultList, vault, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSteel) -> None:
        vault = await async_client.vaults.delete(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert vault is None

    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncSteel) -> None:
        vault = await async_client.vaults.delete(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert vault is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSteel) -> None:
        response = await async_client.vaults.with_raw_response.delete(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        vault = await response.parse()
        assert vault is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSteel) -> None:
        async with async_client.vaults.with_streaming_response.delete(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            vault = await response.parse()
            assert vault is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vaults.with_raw_response.delete(
                id="",
            )
