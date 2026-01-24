# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from aiinbx import AIInbx, AsyncAIInbx
from tests.utils import assert_matches_type
from aiinbx.types import MetaWebhooksSchemaResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMeta:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_webhooks_schema(self, client: AIInbx) -> None:
        meta = client.meta.webhooks_schema()
        assert_matches_type(MetaWebhooksSchemaResponse, meta, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_webhooks_schema(self, client: AIInbx) -> None:
        response = client.meta.with_raw_response.webhooks_schema()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        meta = response.parse()
        assert_matches_type(MetaWebhooksSchemaResponse, meta, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_webhooks_schema(self, client: AIInbx) -> None:
        with client.meta.with_streaming_response.webhooks_schema() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            meta = response.parse()
            assert_matches_type(MetaWebhooksSchemaResponse, meta, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncMeta:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_webhooks_schema(self, async_client: AsyncAIInbx) -> None:
        meta = await async_client.meta.webhooks_schema()
        assert_matches_type(MetaWebhooksSchemaResponse, meta, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_webhooks_schema(self, async_client: AsyncAIInbx) -> None:
        response = await async_client.meta.with_raw_response.webhooks_schema()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        meta = await response.parse()
        assert_matches_type(MetaWebhooksSchemaResponse, meta, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_webhooks_schema(self, async_client: AsyncAIInbx) -> None:
        async with async_client.meta.with_streaming_response.webhooks_schema() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            meta = await response.parse()
            assert_matches_type(MetaWebhooksSchemaResponse, meta, path=["response"])

        assert cast(Any, response.is_closed) is True
