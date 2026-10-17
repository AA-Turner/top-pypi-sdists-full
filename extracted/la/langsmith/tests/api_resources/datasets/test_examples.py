# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from langsmith import Langsmith, AsyncLangsmith

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestExamples:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_delete(self, client: Langsmith) -> None:
        example = client.datasets.examples.delete(
            example_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert example is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: Langsmith) -> None:

        response = client.datasets.examples.with_raw_response.delete(
            example_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        example = response.parse()
        assert example is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: Langsmith) -> None:
        with client.datasets.examples.with_streaming_response.delete(
            example_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            example = response.parse()
            assert example is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: Langsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_id` but received ''"):
            client.datasets.examples.with_raw_response.delete(
                example_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                dataset_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `example_id` but received ''"):
            client.datasets.examples.with_raw_response.delete(
                example_id="",
                dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )


class TestAsyncExamples:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncLangsmith) -> None:
        example = await async_client.datasets.examples.delete(
            example_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert example is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncLangsmith) -> None:

        response = await async_client.datasets.examples.with_raw_response.delete(
            example_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        example = await response.parse()
        assert example is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncLangsmith) -> None:
        async with async_client.datasets.examples.with_streaming_response.delete(
            example_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            example = await response.parse()
            assert example is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncLangsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_id` but received ''"):
            await async_client.datasets.examples.with_raw_response.delete(
                example_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                dataset_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `example_id` but received ''"):
            await async_client.datasets.examples.with_raw_response.delete(
                example_id="",
                dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )
