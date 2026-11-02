# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from coreweave_evaluations import Client, AsyncClient
from coreweave_evaluations.types.eval_tables.versions.rows import (
    CompareListResponse,
    CompareSearchResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCompare:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Client) -> None:
        compare = client.eval_tables.versions.rows.compare.list(
            evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            compare_to=["string"],
        )
        assert_matches_type(CompareListResponse, compare, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Client) -> None:
        compare = client.eval_tables.versions.rows.compare.list(
            evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            compare_to=["string"],
            cursor="cursor",
            filter="filter",
            limit=1,
            order_by="order_by",
        )
        assert_matches_type(CompareListResponse, compare, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Client) -> None:
        response = client.eval_tables.versions.rows.compare.with_raw_response.list(
            evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            compare_to=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        compare = response.parse()
        assert_matches_type(CompareListResponse, compare, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Client) -> None:
        with client.eval_tables.versions.rows.compare.with_streaming_response.list(
            evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            compare_to=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            compare = response.parse()
            assert_matches_type(CompareListResponse, compare, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Client) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.eval_tables.versions.rows.compare.with_raw_response.list(
                evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
                compare_to=["string"],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            client.eval_tables.versions.rows.compare.with_raw_response.list(
                evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
                compare_to=["string"],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_version_id` but received ''"):
            client.eval_tables.versions.rows.compare.with_raw_response.list(
                evaluation_version_id="",
                namespace="wandb",
                scope_id="scope_id",
                compare_to=["string"],
            )

    @parametrize
    def test_method_search(self, client: Client) -> None:
        compare = client.eval_tables.versions.rows.compare.search(
            evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            compare_to=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
        )
        assert_matches_type(CompareSearchResponse, compare, path=["response"])

    @parametrize
    def test_method_search_with_all_params(self, client: Client) -> None:
        compare = client.eval_tables.versions.rows.compare.search(
            evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            compare_to=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            cursor="cursor",
            filter="filter",
            limit=1,
            order_by="order_by",
        )
        assert_matches_type(CompareSearchResponse, compare, path=["response"])

    @parametrize
    def test_raw_response_search(self, client: Client) -> None:
        response = client.eval_tables.versions.rows.compare.with_raw_response.search(
            evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            compare_to=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        compare = response.parse()
        assert_matches_type(CompareSearchResponse, compare, path=["response"])

    @parametrize
    def test_streaming_response_search(self, client: Client) -> None:
        with client.eval_tables.versions.rows.compare.with_streaming_response.search(
            evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            compare_to=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            compare = response.parse()
            assert_matches_type(CompareSearchResponse, compare, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_search(self, client: Client) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.eval_tables.versions.rows.compare.with_raw_response.search(
                evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
                compare_to=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            client.eval_tables.versions.rows.compare.with_raw_response.search(
                evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
                compare_to=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_version_id` but received ''"):
            client.eval_tables.versions.rows.compare.with_raw_response.search(
                evaluation_version_id="",
                namespace="wandb",
                scope_id="scope_id",
                compare_to=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            )


class TestAsyncCompare:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_list(self, async_client: AsyncClient) -> None:
        compare = await async_client.eval_tables.versions.rows.compare.list(
            evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            compare_to=["string"],
        )
        assert_matches_type(CompareListResponse, compare, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncClient) -> None:
        compare = await async_client.eval_tables.versions.rows.compare.list(
            evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            compare_to=["string"],
            cursor="cursor",
            filter="filter",
            limit=1,
            order_by="order_by",
        )
        assert_matches_type(CompareListResponse, compare, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncClient) -> None:
        response = await async_client.eval_tables.versions.rows.compare.with_raw_response.list(
            evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            compare_to=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        compare = await response.parse()
        assert_matches_type(CompareListResponse, compare, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncClient) -> None:
        async with async_client.eval_tables.versions.rows.compare.with_streaming_response.list(
            evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            compare_to=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            compare = await response.parse()
            assert_matches_type(CompareListResponse, compare, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.eval_tables.versions.rows.compare.with_raw_response.list(
                evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
                compare_to=["string"],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            await async_client.eval_tables.versions.rows.compare.with_raw_response.list(
                evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
                compare_to=["string"],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_version_id` but received ''"):
            await async_client.eval_tables.versions.rows.compare.with_raw_response.list(
                evaluation_version_id="",
                namespace="wandb",
                scope_id="scope_id",
                compare_to=["string"],
            )

    @parametrize
    async def test_method_search(self, async_client: AsyncClient) -> None:
        compare = await async_client.eval_tables.versions.rows.compare.search(
            evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            compare_to=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
        )
        assert_matches_type(CompareSearchResponse, compare, path=["response"])

    @parametrize
    async def test_method_search_with_all_params(self, async_client: AsyncClient) -> None:
        compare = await async_client.eval_tables.versions.rows.compare.search(
            evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            compare_to=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            cursor="cursor",
            filter="filter",
            limit=1,
            order_by="order_by",
        )
        assert_matches_type(CompareSearchResponse, compare, path=["response"])

    @parametrize
    async def test_raw_response_search(self, async_client: AsyncClient) -> None:
        response = await async_client.eval_tables.versions.rows.compare.with_raw_response.search(
            evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            compare_to=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        compare = await response.parse()
        assert_matches_type(CompareSearchResponse, compare, path=["response"])

    @parametrize
    async def test_streaming_response_search(self, async_client: AsyncClient) -> None:
        async with async_client.eval_tables.versions.rows.compare.with_streaming_response.search(
            evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            compare_to=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            compare = await response.parse()
            assert_matches_type(CompareSearchResponse, compare, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_search(self, async_client: AsyncClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.eval_tables.versions.rows.compare.with_raw_response.search(
                evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
                compare_to=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            await async_client.eval_tables.versions.rows.compare.with_raw_response.search(
                evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
                compare_to=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_version_id` but received ''"):
            await async_client.eval_tables.versions.rows.compare.with_raw_response.search(
                evaluation_version_id="",
                namespace="wandb",
                scope_id="scope_id",
                compare_to=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            )
