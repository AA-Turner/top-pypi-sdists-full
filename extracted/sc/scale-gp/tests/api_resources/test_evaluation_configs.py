# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import EvaluationConfig
from scale_gp.pagination import SyncPageResponse, AsyncPageResponse
from scale_gp.types.shared import GenericDeleteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEvaluationConfigs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create_overload_1(self, client: SGPClient) -> None:
        evaluation_config = client.evaluation_configs.create(
            account_id="account_id",
            question_set_id="question_set_id",
        )
        assert_matches_type(EvaluationConfig, evaluation_config, path=["response"])

    @parametrize
    def test_method_create_with_all_params_overload_1(self, client: SGPClient) -> None:
        evaluation_config = client.evaluation_configs.create(
            account_id="account_id",
            question_set_id="question_set_id",
            auto_evaluation_model="llama-3-1-70b-instruct",
            auto_evaluation_parameters={
                "batch_size": 1,
                "temperature": 0,
            },
            evaluation_type="llm_auto",
            studio_project_id="studio_project_id",
        )
        assert_matches_type(EvaluationConfig, evaluation_config, path=["response"])

    @parametrize
    def test_raw_response_create_overload_1(self, client: SGPClient) -> None:
        response = client.evaluation_configs.with_raw_response.create(
            account_id="account_id",
            question_set_id="question_set_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_config = response.parse()
        assert_matches_type(EvaluationConfig, evaluation_config, path=["response"])

    @parametrize
    def test_streaming_response_create_overload_1(self, client: SGPClient) -> None:
        with client.evaluation_configs.with_streaming_response.create(
            account_id="account_id",
            question_set_id="question_set_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_config = response.parse()
            assert_matches_type(EvaluationConfig, evaluation_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_create_overload_2(self, client: SGPClient) -> None:
        evaluation_config = client.evaluation_configs.create(
            account_id="account_id",
            question_set_id="question_set_id",
        )
        assert_matches_type(EvaluationConfig, evaluation_config, path=["response"])

    @parametrize
    def test_method_create_with_all_params_overload_2(self, client: SGPClient) -> None:
        evaluation_config = client.evaluation_configs.create(
            account_id="account_id",
            question_set_id="question_set_id",
            auto_evaluation_model=None,
            auto_evaluation_parameters={
                "batch_size": 1,
                "temperature": 0,
            },
            evaluation_type="studio",
            studio_project_id="studio_project_id",
        )
        assert_matches_type(EvaluationConfig, evaluation_config, path=["response"])

    @parametrize
    def test_raw_response_create_overload_2(self, client: SGPClient) -> None:
        response = client.evaluation_configs.with_raw_response.create(
            account_id="account_id",
            question_set_id="question_set_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_config = response.parse()
        assert_matches_type(EvaluationConfig, evaluation_config, path=["response"])

    @parametrize
    def test_streaming_response_create_overload_2(self, client: SGPClient) -> None:
        with client.evaluation_configs.with_streaming_response.create(
            account_id="account_id",
            question_set_id="question_set_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_config = response.parse()
            assert_matches_type(EvaluationConfig, evaluation_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        evaluation_config = client.evaluation_configs.retrieve(
            "evaluation_config_id",
        )
        assert_matches_type(EvaluationConfig, evaluation_config, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.evaluation_configs.with_raw_response.retrieve(
            "evaluation_config_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_config = response.parse()
        assert_matches_type(EvaluationConfig, evaluation_config, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.evaluation_configs.with_streaming_response.retrieve(
            "evaluation_config_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_config = response.parse()
            assert_matches_type(EvaluationConfig, evaluation_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_config_id` but received ''"):
            client.evaluation_configs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        evaluation_config = client.evaluation_configs.list()
        assert_matches_type(SyncPageResponse[EvaluationConfig], evaluation_config, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        evaluation_config = client.evaluation_configs.list(
            account_id="account_id",
            limit=1,
            page=1,
        )
        assert_matches_type(SyncPageResponse[EvaluationConfig], evaluation_config, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.evaluation_configs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_config = response.parse()
        assert_matches_type(SyncPageResponse[EvaluationConfig], evaluation_config, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.evaluation_configs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_config = response.parse()
            assert_matches_type(SyncPageResponse[EvaluationConfig], evaluation_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        evaluation_config = client.evaluation_configs.delete(
            "evaluation_config_id",
        )
        assert_matches_type(GenericDeleteResponse, evaluation_config, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.evaluation_configs.with_raw_response.delete(
            "evaluation_config_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_config = response.parse()
        assert_matches_type(GenericDeleteResponse, evaluation_config, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.evaluation_configs.with_streaming_response.delete(
            "evaluation_config_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_config = response.parse()
            assert_matches_type(GenericDeleteResponse, evaluation_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_config_id` but received ''"):
            client.evaluation_configs.with_raw_response.delete(
                "",
            )


class TestAsyncEvaluationConfigs:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create_overload_1(self, async_client: AsyncSGPClient) -> None:
        evaluation_config = await async_client.evaluation_configs.create(
            account_id="account_id",
            question_set_id="question_set_id",
        )
        assert_matches_type(EvaluationConfig, evaluation_config, path=["response"])

    @parametrize
    async def test_method_create_with_all_params_overload_1(self, async_client: AsyncSGPClient) -> None:
        evaluation_config = await async_client.evaluation_configs.create(
            account_id="account_id",
            question_set_id="question_set_id",
            auto_evaluation_model="llama-3-1-70b-instruct",
            auto_evaluation_parameters={
                "batch_size": 1,
                "temperature": 0,
            },
            evaluation_type="llm_auto",
            studio_project_id="studio_project_id",
        )
        assert_matches_type(EvaluationConfig, evaluation_config, path=["response"])

    @parametrize
    async def test_raw_response_create_overload_1(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_configs.with_raw_response.create(
            account_id="account_id",
            question_set_id="question_set_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_config = await response.parse()
        assert_matches_type(EvaluationConfig, evaluation_config, path=["response"])

    @parametrize
    async def test_streaming_response_create_overload_1(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_configs.with_streaming_response.create(
            account_id="account_id",
            question_set_id="question_set_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_config = await response.parse()
            assert_matches_type(EvaluationConfig, evaluation_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_create_overload_2(self, async_client: AsyncSGPClient) -> None:
        evaluation_config = await async_client.evaluation_configs.create(
            account_id="account_id",
            question_set_id="question_set_id",
        )
        assert_matches_type(EvaluationConfig, evaluation_config, path=["response"])

    @parametrize
    async def test_method_create_with_all_params_overload_2(self, async_client: AsyncSGPClient) -> None:
        evaluation_config = await async_client.evaluation_configs.create(
            account_id="account_id",
            question_set_id="question_set_id",
            auto_evaluation_model=None,
            auto_evaluation_parameters={
                "batch_size": 1,
                "temperature": 0,
            },
            evaluation_type="studio",
            studio_project_id="studio_project_id",
        )
        assert_matches_type(EvaluationConfig, evaluation_config, path=["response"])

    @parametrize
    async def test_raw_response_create_overload_2(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_configs.with_raw_response.create(
            account_id="account_id",
            question_set_id="question_set_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_config = await response.parse()
        assert_matches_type(EvaluationConfig, evaluation_config, path=["response"])

    @parametrize
    async def test_streaming_response_create_overload_2(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_configs.with_streaming_response.create(
            account_id="account_id",
            question_set_id="question_set_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_config = await response.parse()
            assert_matches_type(EvaluationConfig, evaluation_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        evaluation_config = await async_client.evaluation_configs.retrieve(
            "evaluation_config_id",
        )
        assert_matches_type(EvaluationConfig, evaluation_config, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_configs.with_raw_response.retrieve(
            "evaluation_config_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_config = await response.parse()
        assert_matches_type(EvaluationConfig, evaluation_config, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_configs.with_streaming_response.retrieve(
            "evaluation_config_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_config = await response.parse()
            assert_matches_type(EvaluationConfig, evaluation_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_config_id` but received ''"):
            await async_client.evaluation_configs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        evaluation_config = await async_client.evaluation_configs.list()
        assert_matches_type(AsyncPageResponse[EvaluationConfig], evaluation_config, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        evaluation_config = await async_client.evaluation_configs.list(
            account_id="account_id",
            limit=1,
            page=1,
        )
        assert_matches_type(AsyncPageResponse[EvaluationConfig], evaluation_config, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_configs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_config = await response.parse()
        assert_matches_type(AsyncPageResponse[EvaluationConfig], evaluation_config, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_configs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_config = await response.parse()
            assert_matches_type(AsyncPageResponse[EvaluationConfig], evaluation_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        evaluation_config = await async_client.evaluation_configs.delete(
            "evaluation_config_id",
        )
        assert_matches_type(GenericDeleteResponse, evaluation_config, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.evaluation_configs.with_raw_response.delete(
            "evaluation_config_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation_config = await response.parse()
        assert_matches_type(GenericDeleteResponse, evaluation_config, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.evaluation_configs.with_streaming_response.delete(
            "evaluation_config_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation_config = await response.parse()
            assert_matches_type(GenericDeleteResponse, evaluation_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `evaluation_config_id` but received ''"):
            await async_client.evaluation_configs.with_raw_response.delete(
                "",
            )
