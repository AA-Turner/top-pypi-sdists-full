# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import GenericModelResponse
from scale_gp.types.shared import ModelServerInfo

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAlias:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        alias = client.alias.retrieve(
            "alias",
        )
        assert_matches_type(ModelServerInfo, alias, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.alias.with_raw_response.retrieve(
            "alias",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        alias = response.parse()
        assert_matches_type(ModelServerInfo, alias, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.alias.with_streaming_response.retrieve(
            "alias",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            alias = response.parse()
            assert_matches_type(ModelServerInfo, alias, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `alias` but received ''"):
            client.alias.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_execute(self, client: SGPClient) -> None:
        alias = client.alias.execute(
            alias="alias",
        )
        assert_matches_type(GenericModelResponse, alias, path=["response"])

    @parametrize
    def test_method_execute_with_all_params(self, client: SGPClient) -> None:
        alias = client.alias.execute(
            alias="alias",
            stream=True,
        )
        assert_matches_type(GenericModelResponse, alias, path=["response"])

    @parametrize
    def test_raw_response_execute(self, client: SGPClient) -> None:
        response = client.alias.with_raw_response.execute(
            alias="alias",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        alias = response.parse()
        assert_matches_type(GenericModelResponse, alias, path=["response"])

    @parametrize
    def test_streaming_response_execute(self, client: SGPClient) -> None:
        with client.alias.with_streaming_response.execute(
            alias="alias",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            alias = response.parse()
            assert_matches_type(GenericModelResponse, alias, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_execute(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `alias` but received ''"):
            client.alias.with_raw_response.execute(
                alias="",
            )


class TestAsyncAlias:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        alias = await async_client.alias.retrieve(
            "alias",
        )
        assert_matches_type(ModelServerInfo, alias, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.alias.with_raw_response.retrieve(
            "alias",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        alias = await response.parse()
        assert_matches_type(ModelServerInfo, alias, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.alias.with_streaming_response.retrieve(
            "alias",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            alias = await response.parse()
            assert_matches_type(ModelServerInfo, alias, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `alias` but received ''"):
            await async_client.alias.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_execute(self, async_client: AsyncSGPClient) -> None:
        alias = await async_client.alias.execute(
            alias="alias",
        )
        assert_matches_type(GenericModelResponse, alias, path=["response"])

    @parametrize
    async def test_method_execute_with_all_params(self, async_client: AsyncSGPClient) -> None:
        alias = await async_client.alias.execute(
            alias="alias",
            stream=True,
        )
        assert_matches_type(GenericModelResponse, alias, path=["response"])

    @parametrize
    async def test_raw_response_execute(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.alias.with_raw_response.execute(
            alias="alias",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        alias = await response.parse()
        assert_matches_type(GenericModelResponse, alias, path=["response"])

    @parametrize
    async def test_streaming_response_execute(self, async_client: AsyncSGPClient) -> None:
        async with async_client.alias.with_streaming_response.execute(
            alias="alias",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            alias = await response.parse()
            assert_matches_type(GenericModelResponse, alias, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_execute(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `alias` but received ''"):
            await async_client.alias.with_raw_response.execute(
                alias="",
            )
