# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from coreweave_evaluations import Client, AsyncClient
from coreweave_evaluations.types import (
    EvaluationGetResponse,
    EvaluationListResponse,
    EvaluationCreateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEvaluations:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Client) -> None:
        evaluation = client.evaluations.create(
            namespace="wandb",
            scope_id="scope_id",
            name="x",
            primary_target_kind="case",
            source={
                "dataset_version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "kind": "fixed",
            },
        )
        assert_matches_type(EvaluationCreateResponse, evaluation, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Client) -> None:
        evaluation = client.evaluations.create(
            namespace="wandb",
            scope_id="scope_id",
            name="x",
            primary_target_kind="case",
            source={
                "dataset_version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "kind": "fixed",
            },
            attributes={"foo": "bar"},
        )
        assert_matches_type(EvaluationCreateResponse, evaluation, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Client) -> None:
        response = client.evaluations.with_raw_response.create(
            namespace="wandb",
            scope_id="scope_id",
            name="x",
            primary_target_kind="case",
            source={
                "dataset_version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "kind": "fixed",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(EvaluationCreateResponse, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Client) -> None:
        with client.evaluations.with_streaming_response.create(
            namespace="wandb",
            scope_id="scope_id",
            name="x",
            primary_target_kind="case",
            source={
                "dataset_version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "kind": "fixed",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(EvaluationCreateResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Client) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.evaluations.with_raw_response.create(
                namespace="",
                scope_id="scope_id",
                name="x",
                primary_target_kind="case",
                source={
                    "dataset_version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "kind": "fixed",
                },
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            client.evaluations.with_raw_response.create(
                namespace="wandb",
                scope_id="",
                name="x",
                primary_target_kind="case",
                source={
                    "dataset_version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "kind": "fixed",
                },
            )

    @parametrize
    def test_method_list(self, client: Client) -> None:
        evaluation = client.evaluations.list(
            namespace="wandb",
            scope_id="scope_id",
        )
        assert_matches_type(EvaluationListResponse, evaluation, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Client) -> None:
        evaluation = client.evaluations.list(
            namespace="wandb",
            scope_id="scope_id",
            cursor="cursor",
            limit=1,
            name="x",
        )
        assert_matches_type(EvaluationListResponse, evaluation, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Client) -> None:
        response = client.evaluations.with_raw_response.list(
            namespace="wandb",
            scope_id="scope_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(EvaluationListResponse, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Client) -> None:
        with client.evaluations.with_streaming_response.list(
            namespace="wandb",
            scope_id="scope_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(EvaluationListResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Client) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.evaluations.with_raw_response.list(
                namespace="",
                scope_id="scope_id",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            client.evaluations.with_raw_response.list(
                namespace="wandb",
                scope_id="",
            )

    @parametrize
    def test_method_get(self, client: Client) -> None:
        evaluation = client.evaluations.get(
            evaluation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )
        assert_matches_type(EvaluationGetResponse, evaluation, path=["response"])

    @parametrize
    def test_raw_response_get(self, client: Client) -> None:
        response = client.evaluations.with_raw_response.get(
            evaluation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(EvaluationGetResponse, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_get(self, client: Client) -> None:
        with client.evaluations.with_streaming_response.get(
            evaluation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(EvaluationGetResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_get(self, client: Client) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.evaluations.with_raw_response.get(
                evaluation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            client.evaluations.with_raw_response.get(
                evaluation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            client.evaluations.with_raw_response.get(
                evaluation_id="",
                namespace="wandb",
                scope_id="scope_id",
            )


class TestAsyncEvaluations:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncClient) -> None:
        evaluation = await async_client.evaluations.create(
            namespace="wandb",
            scope_id="scope_id",
            name="x",
            primary_target_kind="case",
            source={
                "dataset_version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "kind": "fixed",
            },
        )
        assert_matches_type(EvaluationCreateResponse, evaluation, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncClient) -> None:
        evaluation = await async_client.evaluations.create(
            namespace="wandb",
            scope_id="scope_id",
            name="x",
            primary_target_kind="case",
            source={
                "dataset_version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "kind": "fixed",
            },
            attributes={"foo": "bar"},
        )
        assert_matches_type(EvaluationCreateResponse, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncClient) -> None:
        response = await async_client.evaluations.with_raw_response.create(
            namespace="wandb",
            scope_id="scope_id",
            name="x",
            primary_target_kind="case",
            source={
                "dataset_version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "kind": "fixed",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(EvaluationCreateResponse, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncClient) -> None:
        async with async_client.evaluations.with_streaming_response.create(
            namespace="wandb",
            scope_id="scope_id",
            name="x",
            primary_target_kind="case",
            source={
                "dataset_version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "kind": "fixed",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(EvaluationCreateResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.evaluations.with_raw_response.create(
                namespace="",
                scope_id="scope_id",
                name="x",
                primary_target_kind="case",
                source={
                    "dataset_version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "kind": "fixed",
                },
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            await async_client.evaluations.with_raw_response.create(
                namespace="wandb",
                scope_id="",
                name="x",
                primary_target_kind="case",
                source={
                    "dataset_version_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "kind": "fixed",
                },
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncClient) -> None:
        evaluation = await async_client.evaluations.list(
            namespace="wandb",
            scope_id="scope_id",
        )
        assert_matches_type(EvaluationListResponse, evaluation, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncClient) -> None:
        evaluation = await async_client.evaluations.list(
            namespace="wandb",
            scope_id="scope_id",
            cursor="cursor",
            limit=1,
            name="x",
        )
        assert_matches_type(EvaluationListResponse, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncClient) -> None:
        response = await async_client.evaluations.with_raw_response.list(
            namespace="wandb",
            scope_id="scope_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(EvaluationListResponse, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncClient) -> None:
        async with async_client.evaluations.with_streaming_response.list(
            namespace="wandb",
            scope_id="scope_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(EvaluationListResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.evaluations.with_raw_response.list(
                namespace="",
                scope_id="scope_id",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            await async_client.evaluations.with_raw_response.list(
                namespace="wandb",
                scope_id="",
            )

    @parametrize
    async def test_method_get(self, async_client: AsyncClient) -> None:
        evaluation = await async_client.evaluations.get(
            evaluation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )
        assert_matches_type(EvaluationGetResponse, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_get(self, async_client: AsyncClient) -> None:
        response = await async_client.evaluations.with_raw_response.get(
            evaluation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(EvaluationGetResponse, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncClient) -> None:
        async with async_client.evaluations.with_streaming_response.get(
            evaluation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(EvaluationGetResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_get(self, async_client: AsyncClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.evaluations.with_raw_response.get(
                evaluation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            await async_client.evaluations.with_raw_response.get(
                evaluation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_id` but received ''"):
            await async_client.evaluations.with_raw_response.get(
                evaluation_id="",
                namespace="wandb",
                scope_id="scope_id",
            )
