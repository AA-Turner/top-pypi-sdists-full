# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from coreweave_evaluations import Client, AsyncClient
from coreweave_evaluations.types import EvalTableCreateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEvalTables:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Client) -> None:
        eval_table = client.eval_tables.create(
            namespace="wandb",
            scope_id="scope_id",
            name="x",
        )
        assert_matches_type(EvalTableCreateResponse, eval_table, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Client) -> None:
        eval_table = client.eval_tables.create(
            namespace="wandb",
            scope_id="scope_id",
            name="x",
            attributes={"foo": "bar"},
            uri="https://example.com",
        )
        assert_matches_type(EvalTableCreateResponse, eval_table, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Client) -> None:
        response = client.eval_tables.with_raw_response.create(
            namespace="wandb",
            scope_id="scope_id",
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        eval_table = response.parse()
        assert_matches_type(EvalTableCreateResponse, eval_table, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Client) -> None:
        with client.eval_tables.with_streaming_response.create(
            namespace="wandb",
            scope_id="scope_id",
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            eval_table = response.parse()
            assert_matches_type(EvalTableCreateResponse, eval_table, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Client) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.eval_tables.with_raw_response.create(
                namespace="",
                scope_id="scope_id",
                name="x",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            client.eval_tables.with_raw_response.create(
                namespace="wandb",
                scope_id="",
                name="x",
            )


class TestAsyncEvalTables:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncClient) -> None:
        eval_table = await async_client.eval_tables.create(
            namespace="wandb",
            scope_id="scope_id",
            name="x",
        )
        assert_matches_type(EvalTableCreateResponse, eval_table, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncClient) -> None:
        eval_table = await async_client.eval_tables.create(
            namespace="wandb",
            scope_id="scope_id",
            name="x",
            attributes={"foo": "bar"},
            uri="https://example.com",
        )
        assert_matches_type(EvalTableCreateResponse, eval_table, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncClient) -> None:
        response = await async_client.eval_tables.with_raw_response.create(
            namespace="wandb",
            scope_id="scope_id",
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        eval_table = await response.parse()
        assert_matches_type(EvalTableCreateResponse, eval_table, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncClient) -> None:
        async with async_client.eval_tables.with_streaming_response.create(
            namespace="wandb",
            scope_id="scope_id",
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            eval_table = await response.parse()
            assert_matches_type(EvalTableCreateResponse, eval_table, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.eval_tables.with_raw_response.create(
                namespace="",
                scope_id="scope_id",
                name="x",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            await async_client.eval_tables.with_raw_response.create(
                namespace="wandb",
                scope_id="",
                name="x",
            )
