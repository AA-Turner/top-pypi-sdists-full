# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from coreweave_evaluations import Client, AsyncClient
from coreweave_evaluations.types.eval_tables.versions import ColumnGetResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestColumns:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_get(self, client: Client) -> None:
        column = client.eval_tables.versions.columns.get(
            evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )
        assert_matches_type(ColumnGetResponse, column, path=["response"])

    @parametrize
    def test_raw_response_get(self, client: Client) -> None:
        response = client.eval_tables.versions.columns.with_raw_response.get(
            evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        column = response.parse()
        assert_matches_type(ColumnGetResponse, column, path=["response"])

    @parametrize
    def test_streaming_response_get(self, client: Client) -> None:
        with client.eval_tables.versions.columns.with_streaming_response.get(
            evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            column = response.parse()
            assert_matches_type(ColumnGetResponse, column, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_get(self, client: Client) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.eval_tables.versions.columns.with_raw_response.get(
                evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            client.eval_tables.versions.columns.with_raw_response.get(
                evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_version_id` but received ''"):
            client.eval_tables.versions.columns.with_raw_response.get(
                evaluation_version_id="",
                namespace="wandb",
                scope_id="scope_id",
            )


class TestAsyncColumns:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_get(self, async_client: AsyncClient) -> None:
        column = await async_client.eval_tables.versions.columns.get(
            evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )
        assert_matches_type(ColumnGetResponse, column, path=["response"])

    @parametrize
    async def test_raw_response_get(self, async_client: AsyncClient) -> None:
        response = await async_client.eval_tables.versions.columns.with_raw_response.get(
            evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        column = await response.parse()
        assert_matches_type(ColumnGetResponse, column, path=["response"])

    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncClient) -> None:
        async with async_client.eval_tables.versions.columns.with_streaming_response.get(
            evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            column = await response.parse()
            assert_matches_type(ColumnGetResponse, column, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_get(self, async_client: AsyncClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.eval_tables.versions.columns.with_raw_response.get(
                evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            await async_client.eval_tables.versions.columns.with_raw_response.get(
                evaluation_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_version_id` but received ''"):
            await async_client.eval_tables.versions.columns.with_raw_response.get(
                evaluation_version_id="",
                namespace="wandb",
                scope_id="scope_id",
            )
