# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from langsmith import Langsmith, AsyncLangsmith
from tests.utils import assert_matches_type
from langsmith.types import (
    ProductFeedbackCreateResponse,
    ProductFeedbackRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestProductFeedback:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create(self, client: Langsmith) -> None:
        product_feedback = client.product_feedback.create(
            category="BUG",
            message="x",
            source="LANGSMITH_CLI",
        )
        assert_matches_type(ProductFeedbackCreateResponse, product_feedback, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Langsmith) -> None:
        product_feedback = client.product_feedback.create(
            category="BUG",
            message="x",
            source="LANGSMITH_CLI",
            client={
                "architecture": "architecture",
                "os": "os",
                "version": "version",
            },
            idempotency_key="Idempotency-Key",
        )
        assert_matches_type(ProductFeedbackCreateResponse, product_feedback, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Langsmith) -> None:

        response = client.product_feedback.with_raw_response.create(
            category="BUG",
            message="x",
            source="LANGSMITH_CLI",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        product_feedback = response.parse()
        assert_matches_type(ProductFeedbackCreateResponse, product_feedback, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Langsmith) -> None:
        with client.product_feedback.with_streaming_response.create(
            category="BUG",
            message="x",
            source="LANGSMITH_CLI",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            product_feedback = response.parse()
            assert_matches_type(ProductFeedbackCreateResponse, product_feedback, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Langsmith) -> None:
        product_feedback = client.product_feedback.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ProductFeedbackRetrieveResponse, product_feedback, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Langsmith) -> None:

        response = client.product_feedback.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        product_feedback = response.parse()
        assert_matches_type(ProductFeedbackRetrieveResponse, product_feedback, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Langsmith) -> None:
        with client.product_feedback.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            product_feedback = response.parse()
            assert_matches_type(ProductFeedbackRetrieveResponse, product_feedback, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Langsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.product_feedback.with_raw_response.retrieve(
                "",
            )


class TestAsyncProductFeedback:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncLangsmith) -> None:
        product_feedback = await async_client.product_feedback.create(
            category="BUG",
            message="x",
            source="LANGSMITH_CLI",
        )
        assert_matches_type(ProductFeedbackCreateResponse, product_feedback, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncLangsmith) -> None:
        product_feedback = await async_client.product_feedback.create(
            category="BUG",
            message="x",
            source="LANGSMITH_CLI",
            client={
                "architecture": "architecture",
                "os": "os",
                "version": "version",
            },
            idempotency_key="Idempotency-Key",
        )
        assert_matches_type(ProductFeedbackCreateResponse, product_feedback, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncLangsmith) -> None:

        response = await async_client.product_feedback.with_raw_response.create(
            category="BUG",
            message="x",
            source="LANGSMITH_CLI",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        product_feedback = await response.parse()
        assert_matches_type(ProductFeedbackCreateResponse, product_feedback, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncLangsmith) -> None:
        async with async_client.product_feedback.with_streaming_response.create(
            category="BUG",
            message="x",
            source="LANGSMITH_CLI",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            product_feedback = await response.parse()
            assert_matches_type(ProductFeedbackCreateResponse, product_feedback, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncLangsmith) -> None:
        product_feedback = await async_client.product_feedback.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ProductFeedbackRetrieveResponse, product_feedback, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncLangsmith) -> None:

        response = await async_client.product_feedback.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        product_feedback = await response.parse()
        assert_matches_type(ProductFeedbackRetrieveResponse, product_feedback, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncLangsmith) -> None:
        async with async_client.product_feedback.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            product_feedback = await response.parse()
            assert_matches_type(ProductFeedbackRetrieveResponse, product_feedback, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncLangsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.product_feedback.with_raw_response.retrieve(
                "",
            )
