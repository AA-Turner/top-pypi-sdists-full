# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import ApplicationSchemaRetrieveResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestApplicationSchemas:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="prism response body validation error")
    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        application_schema = client.application_schemas.retrieve(
            version="OFFLINE",
        )
        assert_matches_type(ApplicationSchemaRetrieveResponse, application_schema, path=["response"])

    @pytest.mark.skip(reason="prism response body validation error")
    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.application_schemas.with_raw_response.retrieve(
            version="OFFLINE",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_schema = response.parse()
        assert_matches_type(ApplicationSchemaRetrieveResponse, application_schema, path=["response"])

    @pytest.mark.skip(reason="prism response body validation error")
    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.application_schemas.with_streaming_response.retrieve(
            version="OFFLINE",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_schema = response.parse()
            assert_matches_type(ApplicationSchemaRetrieveResponse, application_schema, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncApplicationSchemas:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="prism response body validation error")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        application_schema = await async_client.application_schemas.retrieve(
            version="OFFLINE",
        )
        assert_matches_type(ApplicationSchemaRetrieveResponse, application_schema, path=["response"])

    @pytest.mark.skip(reason="prism response body validation error")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_schemas.with_raw_response.retrieve(
            version="OFFLINE",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_schema = await response.parse()
        assert_matches_type(ApplicationSchemaRetrieveResponse, application_schema, path=["response"])

    @pytest.mark.skip(reason="prism response body validation error")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_schemas.with_streaming_response.retrieve(
            version="OFFLINE",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_schema = await response.parse()
            assert_matches_type(ApplicationSchemaRetrieveResponse, application_schema, path=["response"])

        assert cast(Any, response.is_closed) is True
