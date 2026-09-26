# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cloudflare import Cloudflare, AsyncCloudflare
from tests.utils import assert_matches_type
from cloudflare.types.field_extractors import (
    FieldExtractorGetResponse,
    FieldExtractorUpdateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFieldExtractors:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_update(self, client: Cloudflare) -> None:
        field_extractor = client.field_extractors.update(
            extractor="llm_prompts",
            account_id="123456",
            rules=[
                {
                    "fields": [
                        {
                            "expression": "x",
                            "name": "x",
                        }
                    ],
                    "ref": "x",
                }
            ],
        )
        assert_matches_type(FieldExtractorUpdateResponse, field_extractor, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Cloudflare) -> None:
        response = client.field_extractors.with_raw_response.update(
            extractor="llm_prompts",
            account_id="123456",
            rules=[
                {
                    "fields": [
                        {
                            "expression": "x",
                            "name": "x",
                        }
                    ],
                    "ref": "x",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        field_extractor = response.parse()
        assert_matches_type(FieldExtractorUpdateResponse, field_extractor, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Cloudflare) -> None:
        with client.field_extractors.with_streaming_response.update(
            extractor="llm_prompts",
            account_id="123456",
            rules=[
                {
                    "fields": [
                        {
                            "expression": "x",
                            "name": "x",
                        }
                    ],
                    "ref": "x",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            field_extractor = response.parse()
            assert_matches_type(FieldExtractorUpdateResponse, field_extractor, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.field_extractors.with_raw_response.update(
                extractor="llm_prompts",
                account_id="",
                rules=[
                    {
                        "fields": [
                            {
                                "expression": "x",
                                "name": "x",
                            }
                        ],
                        "ref": "x",
                    }
                ],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `extractor` but received ''"):
            client.field_extractors.with_raw_response.update(
                extractor="",
                account_id="123456",
                rules=[
                    {
                        "fields": [
                            {
                                "expression": "x",
                                "name": "x",
                            }
                        ],
                        "ref": "x",
                    }
                ],
            )

    @parametrize
    def test_method_delete(self, client: Cloudflare) -> None:
        field_extractor = client.field_extractors.delete(
            extractor="llm_prompts",
            account_id="123456",
        )
        assert_matches_type(object, field_extractor, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Cloudflare) -> None:
        response = client.field_extractors.with_raw_response.delete(
            extractor="llm_prompts",
            account_id="123456",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        field_extractor = response.parse()
        assert_matches_type(object, field_extractor, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Cloudflare) -> None:
        with client.field_extractors.with_streaming_response.delete(
            extractor="llm_prompts",
            account_id="123456",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            field_extractor = response.parse()
            assert_matches_type(object, field_extractor, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.field_extractors.with_raw_response.delete(
                extractor="llm_prompts",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `extractor` but received ''"):
            client.field_extractors.with_raw_response.delete(
                extractor="",
                account_id="123456",
            )

    @parametrize
    def test_method_get(self, client: Cloudflare) -> None:
        field_extractor = client.field_extractors.get(
            extractor="llm_prompts",
            account_id="123456",
        )
        assert_matches_type(FieldExtractorGetResponse, field_extractor, path=["response"])

    @parametrize
    def test_raw_response_get(self, client: Cloudflare) -> None:
        response = client.field_extractors.with_raw_response.get(
            extractor="llm_prompts",
            account_id="123456",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        field_extractor = response.parse()
        assert_matches_type(FieldExtractorGetResponse, field_extractor, path=["response"])

    @parametrize
    def test_streaming_response_get(self, client: Cloudflare) -> None:
        with client.field_extractors.with_streaming_response.get(
            extractor="llm_prompts",
            account_id="123456",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            field_extractor = response.parse()
            assert_matches_type(FieldExtractorGetResponse, field_extractor, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_get(self, client: Cloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.field_extractors.with_raw_response.get(
                extractor="llm_prompts",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `extractor` but received ''"):
            client.field_extractors.with_raw_response.get(
                extractor="",
                account_id="123456",
            )


class TestAsyncFieldExtractors:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_update(self, async_client: AsyncCloudflare) -> None:
        field_extractor = await async_client.field_extractors.update(
            extractor="llm_prompts",
            account_id="123456",
            rules=[
                {
                    "fields": [
                        {
                            "expression": "x",
                            "name": "x",
                        }
                    ],
                    "ref": "x",
                }
            ],
        )
        assert_matches_type(FieldExtractorUpdateResponse, field_extractor, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.field_extractors.with_raw_response.update(
            extractor="llm_prompts",
            account_id="123456",
            rules=[
                {
                    "fields": [
                        {
                            "expression": "x",
                            "name": "x",
                        }
                    ],
                    "ref": "x",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        field_extractor = await response.parse()
        assert_matches_type(FieldExtractorUpdateResponse, field_extractor, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncCloudflare) -> None:
        async with async_client.field_extractors.with_streaming_response.update(
            extractor="llm_prompts",
            account_id="123456",
            rules=[
                {
                    "fields": [
                        {
                            "expression": "x",
                            "name": "x",
                        }
                    ],
                    "ref": "x",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            field_extractor = await response.parse()
            assert_matches_type(FieldExtractorUpdateResponse, field_extractor, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.field_extractors.with_raw_response.update(
                extractor="llm_prompts",
                account_id="",
                rules=[
                    {
                        "fields": [
                            {
                                "expression": "x",
                                "name": "x",
                            }
                        ],
                        "ref": "x",
                    }
                ],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `extractor` but received ''"):
            await async_client.field_extractors.with_raw_response.update(
                extractor="",
                account_id="123456",
                rules=[
                    {
                        "fields": [
                            {
                                "expression": "x",
                                "name": "x",
                            }
                        ],
                        "ref": "x",
                    }
                ],
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncCloudflare) -> None:
        field_extractor = await async_client.field_extractors.delete(
            extractor="llm_prompts",
            account_id="123456",
        )
        assert_matches_type(object, field_extractor, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.field_extractors.with_raw_response.delete(
            extractor="llm_prompts",
            account_id="123456",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        field_extractor = await response.parse()
        assert_matches_type(object, field_extractor, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncCloudflare) -> None:
        async with async_client.field_extractors.with_streaming_response.delete(
            extractor="llm_prompts",
            account_id="123456",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            field_extractor = await response.parse()
            assert_matches_type(object, field_extractor, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.field_extractors.with_raw_response.delete(
                extractor="llm_prompts",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `extractor` but received ''"):
            await async_client.field_extractors.with_raw_response.delete(
                extractor="",
                account_id="123456",
            )

    @parametrize
    async def test_method_get(self, async_client: AsyncCloudflare) -> None:
        field_extractor = await async_client.field_extractors.get(
            extractor="llm_prompts",
            account_id="123456",
        )
        assert_matches_type(FieldExtractorGetResponse, field_extractor, path=["response"])

    @parametrize
    async def test_raw_response_get(self, async_client: AsyncCloudflare) -> None:
        response = await async_client.field_extractors.with_raw_response.get(
            extractor="llm_prompts",
            account_id="123456",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        field_extractor = await response.parse()
        assert_matches_type(FieldExtractorGetResponse, field_extractor, path=["response"])

    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncCloudflare) -> None:
        async with async_client.field_extractors.with_streaming_response.get(
            extractor="llm_prompts",
            account_id="123456",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            field_extractor = await response.parse()
            assert_matches_type(FieldExtractorGetResponse, field_extractor, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_get(self, async_client: AsyncCloudflare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.field_extractors.with_raw_response.get(
                extractor="llm_prompts",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `extractor` but received ''"):
            await async_client.field_extractors.with_raw_response.get(
                extractor="",
                account_id="123456",
            )
