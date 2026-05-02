# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from scale_gp_beta import SGPClient, AsyncSGPClient
from scale_gp_beta.types import (
    Credential,
    CredentialSecret,
    CredentialDeleteResponse,
)
from scale_gp_beta.pagination import SyncCursorPage, AsyncCursorPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCredentials:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        credential = client.credentials.create(
            name="x",
            payload="x",
            type="x",
        )
        assert_matches_type(Credential, credential, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        credential = client.credentials.create(
            name="x",
            payload="x",
            type="x",
            credential_metadata={"foo": "bar"},
            description="description",
        )
        assert_matches_type(Credential, credential, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.credentials.with_raw_response.create(
            name="x",
            payload="x",
            type="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = response.parse()
        assert_matches_type(Credential, credential, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.credentials.with_streaming_response.create(
            name="x",
            payload="x",
            type="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = response.parse()
            assert_matches_type(Credential, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        credential = client.credentials.retrieve(
            "credential_id",
        )
        assert_matches_type(Credential, credential, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.credentials.with_raw_response.retrieve(
            "credential_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = response.parse()
        assert_matches_type(Credential, credential, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.credentials.with_streaming_response.retrieve(
            "credential_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = response.parse()
            assert_matches_type(Credential, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_id` but received ''"):
            client.credentials.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        credential = client.credentials.update(
            credential_id="credential_id",
        )
        assert_matches_type(Credential, credential, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGPClient) -> None:
        credential = client.credentials.update(
            credential_id="credential_id",
            credential_metadata={"foo": "bar"},
            description="description",
            name="name",
            payload="payload",
            type="type",
        )
        assert_matches_type(Credential, credential, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.credentials.with_raw_response.update(
            credential_id="credential_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = response.parse()
        assert_matches_type(Credential, credential, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.credentials.with_streaming_response.update(
            credential_id="credential_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = response.parse()
            assert_matches_type(Credential, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_id` but received ''"):
            client.credentials.with_raw_response.update(
                credential_id="",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        credential = client.credentials.list()
        assert_matches_type(SyncCursorPage[Credential], credential, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        credential = client.credentials.list(
            ending_before="ending_before",
            limit=1,
            name="name",
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
        )
        assert_matches_type(SyncCursorPage[Credential], credential, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.credentials.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = response.parse()
        assert_matches_type(SyncCursorPage[Credential], credential, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.credentials.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = response.parse()
            assert_matches_type(SyncCursorPage[Credential], credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        credential = client.credentials.delete(
            "credential_id",
        )
        assert_matches_type(CredentialDeleteResponse, credential, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.credentials.with_raw_response.delete(
            "credential_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = response.parse()
        assert_matches_type(CredentialDeleteResponse, credential, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.credentials.with_streaming_response.delete(
            "credential_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = response.parse()
            assert_matches_type(CredentialDeleteResponse, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_id` but received ''"):
            client.credentials.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_decrypt(self, client: SGPClient) -> None:
        credential = client.credentials.decrypt(
            "credential_id",
        )
        assert_matches_type(CredentialSecret, credential, path=["response"])

    @parametrize
    def test_raw_response_decrypt(self, client: SGPClient) -> None:
        response = client.credentials.with_raw_response.decrypt(
            "credential_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = response.parse()
        assert_matches_type(CredentialSecret, credential, path=["response"])

    @parametrize
    def test_streaming_response_decrypt(self, client: SGPClient) -> None:
        with client.credentials.with_streaming_response.decrypt(
            "credential_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = response.parse()
            assert_matches_type(CredentialSecret, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_decrypt(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_id` but received ''"):
            client.credentials.with_raw_response.decrypt(
                "",
            )

    @parametrize
    def test_method_decrypt_by_name(self, client: SGPClient) -> None:
        credential = client.credentials.decrypt_by_name(
            "credential_name",
        )
        assert_matches_type(CredentialSecret, credential, path=["response"])

    @parametrize
    def test_raw_response_decrypt_by_name(self, client: SGPClient) -> None:
        response = client.credentials.with_raw_response.decrypt_by_name(
            "credential_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = response.parse()
        assert_matches_type(CredentialSecret, credential, path=["response"])

    @parametrize
    def test_streaming_response_decrypt_by_name(self, client: SGPClient) -> None:
        with client.credentials.with_streaming_response.decrypt_by_name(
            "credential_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = response.parse()
            assert_matches_type(CredentialSecret, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_decrypt_by_name(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_name` but received ''"):
            client.credentials.with_raw_response.decrypt_by_name(
                "",
            )

    @parametrize
    def test_method_retrieve_by_name(self, client: SGPClient) -> None:
        credential = client.credentials.retrieve_by_name(
            "credential_name",
        )
        assert_matches_type(Credential, credential, path=["response"])

    @parametrize
    def test_raw_response_retrieve_by_name(self, client: SGPClient) -> None:
        response = client.credentials.with_raw_response.retrieve_by_name(
            "credential_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = response.parse()
        assert_matches_type(Credential, credential, path=["response"])

    @parametrize
    def test_streaming_response_retrieve_by_name(self, client: SGPClient) -> None:
        with client.credentials.with_streaming_response.retrieve_by_name(
            "credential_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = response.parse()
            assert_matches_type(Credential, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve_by_name(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_name` but received ''"):
            client.credentials.with_raw_response.retrieve_by_name(
                "",
            )


class TestAsyncCredentials:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        credential = await async_client.credentials.create(
            name="x",
            payload="x",
            type="x",
        )
        assert_matches_type(Credential, credential, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        credential = await async_client.credentials.create(
            name="x",
            payload="x",
            type="x",
            credential_metadata={"foo": "bar"},
            description="description",
        )
        assert_matches_type(Credential, credential, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.credentials.with_raw_response.create(
            name="x",
            payload="x",
            type="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = await response.parse()
        assert_matches_type(Credential, credential, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.credentials.with_streaming_response.create(
            name="x",
            payload="x",
            type="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = await response.parse()
            assert_matches_type(Credential, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        credential = await async_client.credentials.retrieve(
            "credential_id",
        )
        assert_matches_type(Credential, credential, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.credentials.with_raw_response.retrieve(
            "credential_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = await response.parse()
        assert_matches_type(Credential, credential, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.credentials.with_streaming_response.retrieve(
            "credential_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = await response.parse()
            assert_matches_type(Credential, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_id` but received ''"):
            await async_client.credentials.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        credential = await async_client.credentials.update(
            credential_id="credential_id",
        )
        assert_matches_type(Credential, credential, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        credential = await async_client.credentials.update(
            credential_id="credential_id",
            credential_metadata={"foo": "bar"},
            description="description",
            name="name",
            payload="payload",
            type="type",
        )
        assert_matches_type(Credential, credential, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.credentials.with_raw_response.update(
            credential_id="credential_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = await response.parse()
        assert_matches_type(Credential, credential, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.credentials.with_streaming_response.update(
            credential_id="credential_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = await response.parse()
            assert_matches_type(Credential, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_id` but received ''"):
            await async_client.credentials.with_raw_response.update(
                credential_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        credential = await async_client.credentials.list()
        assert_matches_type(AsyncCursorPage[Credential], credential, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        credential = await async_client.credentials.list(
            ending_before="ending_before",
            limit=1,
            name="name",
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
        )
        assert_matches_type(AsyncCursorPage[Credential], credential, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.credentials.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = await response.parse()
        assert_matches_type(AsyncCursorPage[Credential], credential, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.credentials.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = await response.parse()
            assert_matches_type(AsyncCursorPage[Credential], credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        credential = await async_client.credentials.delete(
            "credential_id",
        )
        assert_matches_type(CredentialDeleteResponse, credential, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.credentials.with_raw_response.delete(
            "credential_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = await response.parse()
        assert_matches_type(CredentialDeleteResponse, credential, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.credentials.with_streaming_response.delete(
            "credential_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = await response.parse()
            assert_matches_type(CredentialDeleteResponse, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_id` but received ''"):
            await async_client.credentials.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_decrypt(self, async_client: AsyncSGPClient) -> None:
        credential = await async_client.credentials.decrypt(
            "credential_id",
        )
        assert_matches_type(CredentialSecret, credential, path=["response"])

    @parametrize
    async def test_raw_response_decrypt(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.credentials.with_raw_response.decrypt(
            "credential_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = await response.parse()
        assert_matches_type(CredentialSecret, credential, path=["response"])

    @parametrize
    async def test_streaming_response_decrypt(self, async_client: AsyncSGPClient) -> None:
        async with async_client.credentials.with_streaming_response.decrypt(
            "credential_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = await response.parse()
            assert_matches_type(CredentialSecret, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_decrypt(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_id` but received ''"):
            await async_client.credentials.with_raw_response.decrypt(
                "",
            )

    @parametrize
    async def test_method_decrypt_by_name(self, async_client: AsyncSGPClient) -> None:
        credential = await async_client.credentials.decrypt_by_name(
            "credential_name",
        )
        assert_matches_type(CredentialSecret, credential, path=["response"])

    @parametrize
    async def test_raw_response_decrypt_by_name(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.credentials.with_raw_response.decrypt_by_name(
            "credential_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = await response.parse()
        assert_matches_type(CredentialSecret, credential, path=["response"])

    @parametrize
    async def test_streaming_response_decrypt_by_name(self, async_client: AsyncSGPClient) -> None:
        async with async_client.credentials.with_streaming_response.decrypt_by_name(
            "credential_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = await response.parse()
            assert_matches_type(CredentialSecret, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_decrypt_by_name(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_name` but received ''"):
            await async_client.credentials.with_raw_response.decrypt_by_name(
                "",
            )

    @parametrize
    async def test_method_retrieve_by_name(self, async_client: AsyncSGPClient) -> None:
        credential = await async_client.credentials.retrieve_by_name(
            "credential_name",
        )
        assert_matches_type(Credential, credential, path=["response"])

    @parametrize
    async def test_raw_response_retrieve_by_name(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.credentials.with_raw_response.retrieve_by_name(
            "credential_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credential = await response.parse()
        assert_matches_type(Credential, credential, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve_by_name(self, async_client: AsyncSGPClient) -> None:
        async with async_client.credentials.with_streaming_response.retrieve_by_name(
            "credential_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credential = await response.parse()
            assert_matches_type(Credential, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve_by_name(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_name` but received ''"):
            await async_client.credentials.with_raw_response.retrieve_by_name(
                "",
            )
