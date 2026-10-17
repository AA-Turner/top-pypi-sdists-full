# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from langsmith import Langsmith, AsyncLangsmith
from tests.utils import assert_matches_type
from langsmith.types.fleet import ThreadActivateSandboxResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestThreads:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_activate_sandbox(self, client: Langsmith) -> None:
        thread = client.fleet.threads.activate_sandbox(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ThreadActivateSandboxResponse, thread, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_activate_sandbox(self, client: Langsmith) -> None:

        response = client.fleet.threads.with_raw_response.activate_sandbox(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = response.parse()
        assert_matches_type(ThreadActivateSandboxResponse, thread, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_activate_sandbox(self, client: Langsmith) -> None:
        with client.fleet.threads.with_streaming_response.activate_sandbox(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = response.parse()
            assert_matches_type(ThreadActivateSandboxResponse, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_activate_sandbox(self, client: Langsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.fleet.threads.with_raw_response.activate_sandbox(
                "",
            )


class TestAsyncThreads:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_activate_sandbox(self, async_client: AsyncLangsmith) -> None:
        thread = await async_client.fleet.threads.activate_sandbox(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ThreadActivateSandboxResponse, thread, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_activate_sandbox(self, async_client: AsyncLangsmith) -> None:

        response = await async_client.fleet.threads.with_raw_response.activate_sandbox(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = await response.parse()
        assert_matches_type(ThreadActivateSandboxResponse, thread, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_activate_sandbox(self, async_client: AsyncLangsmith) -> None:
        async with async_client.fleet.threads.with_streaming_response.activate_sandbox(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = await response.parse()
            assert_matches_type(ThreadActivateSandboxResponse, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_activate_sandbox(self, async_client: AsyncLangsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.fleet.threads.with_raw_response.activate_sandbox(
                "",
            )
