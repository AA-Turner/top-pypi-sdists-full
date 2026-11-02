# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from coreweave_evaluations import Client, AsyncClient
from coreweave_evaluations.types.datasets.versions import CaseListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCases:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Client) -> None:
        case = client.datasets.versions.cases.list(
            dataset_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )
        assert_matches_type(CaseListResponse, case, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Client) -> None:
        case = client.datasets.versions.cases.list(
            dataset_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            cursor="cursor",
            limit=1,
        )
        assert_matches_type(CaseListResponse, case, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Client) -> None:
        response = client.datasets.versions.cases.with_raw_response.list(
            dataset_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        case = response.parse()
        assert_matches_type(CaseListResponse, case, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Client) -> None:
        with client.datasets.versions.cases.with_streaming_response.list(
            dataset_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            case = response.parse()
            assert_matches_type(CaseListResponse, case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Client) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.datasets.versions.cases.with_raw_response.list(
                dataset_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            client.datasets.versions.cases.with_raw_response.list(
                dataset_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_version_id` but received ''"):
            client.datasets.versions.cases.with_raw_response.list(
                dataset_version_id="",
                namespace="wandb",
                scope_id="scope_id",
            )


class TestAsyncCases:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_list(self, async_client: AsyncClient) -> None:
        case = await async_client.datasets.versions.cases.list(
            dataset_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )
        assert_matches_type(CaseListResponse, case, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncClient) -> None:
        case = await async_client.datasets.versions.cases.list(
            dataset_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            cursor="cursor",
            limit=1,
        )
        assert_matches_type(CaseListResponse, case, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncClient) -> None:
        response = await async_client.datasets.versions.cases.with_raw_response.list(
            dataset_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        case = await response.parse()
        assert_matches_type(CaseListResponse, case, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncClient) -> None:
        async with async_client.datasets.versions.cases.with_streaming_response.list(
            dataset_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            case = await response.parse()
            assert_matches_type(CaseListResponse, case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.datasets.versions.cases.with_raw_response.list(
                dataset_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            await async_client.datasets.versions.cases.with_raw_response.list(
                dataset_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_version_id` but received ''"):
            await async_client.datasets.versions.cases.with_raw_response.list(
                dataset_version_id="",
                namespace="wandb",
                scope_id="scope_id",
            )
