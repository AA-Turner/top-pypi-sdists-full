# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.pagination import SyncPageResponse, AsyncPageResponse
from scale_gp.types.shared import GenericDeleteResponse
from scale_gp.types.evaluation_datasets import TestCase

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestHistory:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        history = client.evaluation_datasets.test_cases.history.retrieve(
            num="num",
            evaluation_dataset_id="evaluation_dataset_id",
            test_case_id="test_case_id",
        )
        assert_matches_type(TestCase, history, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.evaluation_datasets.test_cases.history.with_raw_response.retrieve(
            num="num",
            evaluation_dataset_id="evaluation_dataset_id",
            test_case_id="test_case_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        history = response.parse()
        assert_matches_type(TestCase, history, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.evaluation_datasets.test_cases.history.with_streaming_response.retrieve(
            num="num",
            evaluation_dataset_id="evaluation_dataset_id",
            test_case_id="test_case_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            history = response.parse()
            assert_matches_type(TestCase, history, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.test_cases.history.with_raw_response.retrieve(
                num="num",
                evaluation_dataset_id="",
                test_case_id="test_case_id",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_id` but received ''"):
            client.evaluation_datasets.test_cases.history.with_raw_response.retrieve(
                num="num",
                evaluation_dataset_id="evaluation_dataset_id",
                test_case_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `num` but received ''"):
            client.evaluation_datasets.test_cases.history.with_raw_response.retrieve(
                num="",
                evaluation_dataset_id="evaluation_dataset_id",
                test_case_id="test_case_id",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        history = client.evaluation_datasets.test_cases.history.list(
            num="num",
            evaluation_dataset_id="evaluation_dataset_id",
        )
        assert_matches_type(SyncPageResponse[TestCase], history, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        history = client.evaluation_datasets.test_cases.history.list(
            num="num",
            evaluation_dataset_id="evaluation_dataset_id",
            account_id="account_id",
            limit=1,
            page=1,
        )
        assert_matches_type(SyncPageResponse[TestCase], history, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.evaluation_datasets.test_cases.history.with_raw_response.list(
            num="num",
            evaluation_dataset_id="evaluation_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        history = response.parse()
        assert_matches_type(SyncPageResponse[TestCase], history, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.evaluation_datasets.test_cases.history.with_streaming_response.list(
            num="num",
            evaluation_dataset_id="evaluation_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            history = response.parse()
            assert_matches_type(SyncPageResponse[TestCase], history, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.test_cases.history.with_raw_response.list(
                num="num",
                evaluation_dataset_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `num` but received ''"):
            client.evaluation_datasets.test_cases.history.with_raw_response.list(
                num="",
                evaluation_dataset_id="evaluation_dataset_id",
            )

    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        history = client.evaluation_datasets.test_cases.history.delete(
            test_case_id="test_case_id",
            evaluation_dataset_id="evaluation_dataset_id",
        )
        assert_matches_type(GenericDeleteResponse, history, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.evaluation_datasets.test_cases.history.with_raw_response.delete(
            test_case_id="test_case_id",
            evaluation_dataset_id="evaluation_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        history = response.parse()
        assert_matches_type(GenericDeleteResponse, history, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.evaluation_datasets.test_cases.history.with_streaming_response.delete(
            test_case_id="test_case_id",
            evaluation_dataset_id="evaluation_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            history = response.parse()
            assert_matches_type(GenericDeleteResponse, history, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            client.evaluation_datasets.test_cases.history.with_raw_response.delete(
                test_case_id="test_case_id",
                evaluation_dataset_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_id` but received ''"):
            client.evaluation_datasets.test_cases.history.with_raw_response.delete(
                test_case_id="",
                evaluation_dataset_id="evaluation_dataset_id",
            )


class TestAsyncHistory:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        history = await async_client.evaluation_datasets.test_cases.history.retrieve(
            num="num",
            evaluation_dataset_id="evaluation_dataset_id",
            test_case_id="test_case_id",
        )
        assert_matches_type(TestCase, history, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_datasets.test_cases.history.with_raw_response.retrieve(
            num="num",
            evaluation_dataset_id="evaluation_dataset_id",
            test_case_id="test_case_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        history = await response.parse()
        assert_matches_type(TestCase, history, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_datasets.test_cases.history.with_streaming_response.retrieve(
            num="num",
            evaluation_dataset_id="evaluation_dataset_id",
            test_case_id="test_case_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            history = await response.parse()
            assert_matches_type(TestCase, history, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.test_cases.history.with_raw_response.retrieve(
                num="num",
                evaluation_dataset_id="",
                test_case_id="test_case_id",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_id` but received ''"):
            await async_client.evaluation_datasets.test_cases.history.with_raw_response.retrieve(
                num="num",
                evaluation_dataset_id="evaluation_dataset_id",
                test_case_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `num` but received ''"):
            await async_client.evaluation_datasets.test_cases.history.with_raw_response.retrieve(
                num="",
                evaluation_dataset_id="evaluation_dataset_id",
                test_case_id="test_case_id",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        history = await async_client.evaluation_datasets.test_cases.history.list(
            num="num",
            evaluation_dataset_id="evaluation_dataset_id",
        )
        assert_matches_type(AsyncPageResponse[TestCase], history, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        history = await async_client.evaluation_datasets.test_cases.history.list(
            num="num",
            evaluation_dataset_id="evaluation_dataset_id",
            account_id="account_id",
            limit=1,
            page=1,
        )
        assert_matches_type(AsyncPageResponse[TestCase], history, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_datasets.test_cases.history.with_raw_response.list(
            num="num",
            evaluation_dataset_id="evaluation_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        history = await response.parse()
        assert_matches_type(AsyncPageResponse[TestCase], history, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_datasets.test_cases.history.with_streaming_response.list(
            num="num",
            evaluation_dataset_id="evaluation_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            history = await response.parse()
            assert_matches_type(AsyncPageResponse[TestCase], history, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.test_cases.history.with_raw_response.list(
                num="num",
                evaluation_dataset_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `num` but received ''"):
            await async_client.evaluation_datasets.test_cases.history.with_raw_response.list(
                num="",
                evaluation_dataset_id="evaluation_dataset_id",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        history = await async_client.evaluation_datasets.test_cases.history.delete(
            test_case_id="test_case_id",
            evaluation_dataset_id="evaluation_dataset_id",
        )
        assert_matches_type(GenericDeleteResponse, history, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_datasets.test_cases.history.with_raw_response.delete(
            test_case_id="test_case_id",
            evaluation_dataset_id="evaluation_dataset_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        history = await response.parse()
        assert_matches_type(GenericDeleteResponse, history, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_datasets.test_cases.history.with_streaming_response.delete(
            test_case_id="test_case_id",
            evaluation_dataset_id="evaluation_dataset_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            history = await response.parse()
            assert_matches_type(GenericDeleteResponse, history, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_dataset_id` but received ''"):
            await async_client.evaluation_datasets.test_cases.history.with_raw_response.delete(
                test_case_id="test_case_id",
                evaluation_dataset_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_id` but received ''"):
            await async_client.evaluation_datasets.test_cases.history.with_raw_response.delete(
                test_case_id="",
                evaluation_dataset_id="evaluation_dataset_id",
            )
