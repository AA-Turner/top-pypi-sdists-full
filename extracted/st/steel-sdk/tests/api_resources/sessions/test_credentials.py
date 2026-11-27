# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from steel import Steel, AsyncSteel
from steel.types import SessionCredentials
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCredentials:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Steel) -> None:
        credential = client.sessions.credentials.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SessionCredentials, credential, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Steel) -> None:
        response = client.sessions.credentials.with_raw_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        credential = response.parse()
        assert_matches_type(SessionCredentials, credential, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Steel) -> None:
        with client.sessions.credentials.with_streaming_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            credential = response.parse()
            assert_matches_type(SessionCredentials, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.sessions.credentials.with_raw_response.list(
                "",
            )

    @parametrize
    def test_method_attach(self, client: Steel) -> None:
        credential = client.sessions.credentials.attach(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SessionCredentials, credential, path=["response"])

    @parametrize
    def test_method_attach_with_all_params(self, client: Steel) -> None:
        credential = client.sessions.credentials.attach(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            bindings=["string"],
            credential_ids=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
        )
        assert_matches_type(SessionCredentials, credential, path=["response"])

    @parametrize
    def test_raw_response_attach(self, client: Steel) -> None:
        response = client.sessions.credentials.with_raw_response.attach(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        credential = response.parse()
        assert_matches_type(SessionCredentials, credential, path=["response"])

    @parametrize
    def test_streaming_response_attach(self, client: Steel) -> None:
        with client.sessions.credentials.with_streaming_response.attach(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            credential = response.parse()
            assert_matches_type(SessionCredentials, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_attach(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.sessions.credentials.with_raw_response.attach(
                id="",
            )

    @parametrize
    def test_method_detach(self, client: Steel) -> None:
        credential = client.sessions.credentials.detach(
            credential_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SessionCredentials, credential, path=["response"])

    @parametrize
    def test_raw_response_detach(self, client: Steel) -> None:
        response = client.sessions.credentials.with_raw_response.detach(
            credential_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        credential = response.parse()
        assert_matches_type(SessionCredentials, credential, path=["response"])

    @parametrize
    def test_streaming_response_detach(self, client: Steel) -> None:
        with client.sessions.credentials.with_streaming_response.detach(
            credential_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            credential = response.parse()
            assert_matches_type(SessionCredentials, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_detach(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.sessions.credentials.with_raw_response.detach(
                credential_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_id` but received ''"):
            client.sessions.credentials.with_raw_response.detach(
                credential_id="",
                id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

    @parametrize
    def test_method_detach_binding(self, client: Steel) -> None:
        credential = client.sessions.credentials.detach_binding(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            reference="reference",
        )
        assert_matches_type(SessionCredentials, credential, path=["response"])

    @parametrize
    def test_raw_response_detach_binding(self, client: Steel) -> None:
        response = client.sessions.credentials.with_raw_response.detach_binding(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            reference="reference",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        credential = response.parse()
        assert_matches_type(SessionCredentials, credential, path=["response"])

    @parametrize
    def test_streaming_response_detach_binding(self, client: Steel) -> None:
        with client.sessions.credentials.with_streaming_response.detach_binding(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            reference="reference",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            credential = response.parse()
            assert_matches_type(SessionCredentials, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_detach_binding(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.sessions.credentials.with_raw_response.detach_binding(
                id="",
                reference="reference",
            )

    @parametrize
    def test_method_replace(self, client: Steel) -> None:
        credential = client.sessions.credentials.replace(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SessionCredentials, credential, path=["response"])

    @parametrize
    def test_method_replace_with_all_params(self, client: Steel) -> None:
        credential = client.sessions.credentials.replace(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            bindings=["string"],
            credential_ids=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
        )
        assert_matches_type(SessionCredentials, credential, path=["response"])

    @parametrize
    def test_raw_response_replace(self, client: Steel) -> None:
        response = client.sessions.credentials.with_raw_response.replace(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        credential = response.parse()
        assert_matches_type(SessionCredentials, credential, path=["response"])

    @parametrize
    def test_streaming_response_replace(self, client: Steel) -> None:
        with client.sessions.credentials.with_streaming_response.replace(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            credential = response.parse()
            assert_matches_type(SessionCredentials, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_replace(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.sessions.credentials.with_raw_response.replace(
                id="",
            )


class TestAsyncCredentials:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_list(self, async_client: AsyncSteel) -> None:
        credential = await async_client.sessions.credentials.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SessionCredentials, credential, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.credentials.with_raw_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        credential = await response.parse()
        assert_matches_type(SessionCredentials, credential, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.credentials.with_streaming_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            credential = await response.parse()
            assert_matches_type(SessionCredentials, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.sessions.credentials.with_raw_response.list(
                "",
            )

    @parametrize
    async def test_method_attach(self, async_client: AsyncSteel) -> None:
        credential = await async_client.sessions.credentials.attach(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SessionCredentials, credential, path=["response"])

    @parametrize
    async def test_method_attach_with_all_params(self, async_client: AsyncSteel) -> None:
        credential = await async_client.sessions.credentials.attach(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            bindings=["string"],
            credential_ids=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
        )
        assert_matches_type(SessionCredentials, credential, path=["response"])

    @parametrize
    async def test_raw_response_attach(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.credentials.with_raw_response.attach(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        credential = await response.parse()
        assert_matches_type(SessionCredentials, credential, path=["response"])

    @parametrize
    async def test_streaming_response_attach(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.credentials.with_streaming_response.attach(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            credential = await response.parse()
            assert_matches_type(SessionCredentials, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_attach(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.sessions.credentials.with_raw_response.attach(
                id="",
            )

    @parametrize
    async def test_method_detach(self, async_client: AsyncSteel) -> None:
        credential = await async_client.sessions.credentials.detach(
            credential_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SessionCredentials, credential, path=["response"])

    @parametrize
    async def test_raw_response_detach(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.credentials.with_raw_response.detach(
            credential_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        credential = await response.parse()
        assert_matches_type(SessionCredentials, credential, path=["response"])

    @parametrize
    async def test_streaming_response_detach(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.credentials.with_streaming_response.detach(
            credential_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            credential = await response.parse()
            assert_matches_type(SessionCredentials, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_detach(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.sessions.credentials.with_raw_response.detach(
                credential_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_id` but received ''"):
            await async_client.sessions.credentials.with_raw_response.detach(
                credential_id="",
                id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

    @parametrize
    async def test_method_detach_binding(self, async_client: AsyncSteel) -> None:
        credential = await async_client.sessions.credentials.detach_binding(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            reference="reference",
        )
        assert_matches_type(SessionCredentials, credential, path=["response"])

    @parametrize
    async def test_raw_response_detach_binding(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.credentials.with_raw_response.detach_binding(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            reference="reference",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        credential = await response.parse()
        assert_matches_type(SessionCredentials, credential, path=["response"])

    @parametrize
    async def test_streaming_response_detach_binding(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.credentials.with_streaming_response.detach_binding(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            reference="reference",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            credential = await response.parse()
            assert_matches_type(SessionCredentials, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_detach_binding(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.sessions.credentials.with_raw_response.detach_binding(
                id="",
                reference="reference",
            )

    @parametrize
    async def test_method_replace(self, async_client: AsyncSteel) -> None:
        credential = await async_client.sessions.credentials.replace(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SessionCredentials, credential, path=["response"])

    @parametrize
    async def test_method_replace_with_all_params(self, async_client: AsyncSteel) -> None:
        credential = await async_client.sessions.credentials.replace(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            bindings=["string"],
            credential_ids=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
        )
        assert_matches_type(SessionCredentials, credential, path=["response"])

    @parametrize
    async def test_raw_response_replace(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.credentials.with_raw_response.replace(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        credential = await response.parse()
        assert_matches_type(SessionCredentials, credential, path=["response"])

    @parametrize
    async def test_streaming_response_replace(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.credentials.with_streaming_response.replace(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            credential = await response.parse()
            assert_matches_type(SessionCredentials, credential, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_replace(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.sessions.credentials.with_raw_response.replace(
                id="",
            )
