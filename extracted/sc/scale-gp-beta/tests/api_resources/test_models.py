# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from scale_gp_beta import SGPClient, AsyncSGPClient
from scale_gp_beta.types import (
    InferenceModel,
    ModelDeleteResponse,
)
from scale_gp_beta.pagination import SyncCursorPage, AsyncCursorPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestModels:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        model = client.models.create(
            model={
                "name": "name",
                "vendor_configuration": {
                    "model_image": {
                        "command": ["string"],
                        "registry": "registry",
                        "repository": "repository",
                        "tag": "tag",
                    },
                    "model_infra": {},
                },
                "model_vendor": "launch",
            },
        )
        assert_matches_type(InferenceModel, model, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        model = client.models.create(
            model={
                "name": "name",
                "vendor_configuration": {
                    "model_image": {
                        "command": ["string"],
                        "registry": "registry",
                        "repository": "repository",
                        "tag": "tag",
                        "env_vars": {"foo": "bar"},
                        "healthcheck_route": "healthcheck_route",
                        "predict_route": "predict_route",
                        "readiness_delay": 0,
                        "request_schema": {"foo": "bar"},
                        "response_schema": {"foo": "bar"},
                        "streaming_command": ["string"],
                        "streaming_predict_route": "streaming_predict_route",
                    },
                    "model_infra": {
                        "cpus": "string",
                        "endpoint_type": "async",
                        "gpu_type": "nvidia-tesla-t4",
                        "gpus": 0,
                        "high_priority": True,
                        "labels": {"foo": "string"},
                        "max_workers": 0,
                        "memory": "memory",
                        "min_workers": 0,
                        "per_worker": 0,
                        "public_inference": True,
                        "storage": "storage",
                    },
                },
                "model_metadata": {"foo": "bar"},
                "model_type": "generic",
                "model_vendor": "launch",
                "on_conflict": "error",
            },
        )
        assert_matches_type(InferenceModel, model, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.models.with_raw_response.create(
            model={
                "name": "name",
                "vendor_configuration": {
                    "model_image": {
                        "command": ["string"],
                        "registry": "registry",
                        "repository": "repository",
                        "tag": "tag",
                    },
                    "model_infra": {},
                },
                "model_vendor": "launch",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert_matches_type(InferenceModel, model, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.models.with_streaming_response.create(
            model={
                "name": "name",
                "vendor_configuration": {
                    "model_image": {
                        "command": ["string"],
                        "registry": "registry",
                        "repository": "repository",
                        "tag": "tag",
                    },
                    "model_infra": {},
                },
                "model_vendor": "launch",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert_matches_type(InferenceModel, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        model = client.models.retrieve(
            "model_id",
        )
        assert_matches_type(InferenceModel, model, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.models.with_raw_response.retrieve(
            "model_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert_matches_type(InferenceModel, model, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.models.with_streaming_response.retrieve(
            "model_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert_matches_type(InferenceModel, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_id` but received ''"):
            client.models.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        model = client.models.update(
            model_id="model_id",
            model={},
        )
        assert_matches_type(InferenceModel, model, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGPClient) -> None:
        model = client.models.update(
            model_id="model_id",
            model={"model_metadata": {"foo": "bar"}},
        )
        assert_matches_type(InferenceModel, model, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.models.with_raw_response.update(
            model_id="model_id",
            model={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert_matches_type(InferenceModel, model, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.models.with_streaming_response.update(
            model_id="model_id",
            model={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert_matches_type(InferenceModel, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_id` but received ''"):
            client.models.with_raw_response.update(
                model_id="",
                model={},
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        model = client.models.list()
        assert_matches_type(SyncCursorPage[InferenceModel], model, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        model = client.models.list(
            ending_before="ending_before",
            limit=1,
            model_vendor="openai",
            name="name",
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
        )
        assert_matches_type(SyncCursorPage[InferenceModel], model, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.models.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert_matches_type(SyncCursorPage[InferenceModel], model, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.models.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert_matches_type(SyncCursorPage[InferenceModel], model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        model = client.models.delete(
            "model_id",
        )
        assert_matches_type(ModelDeleteResponse, model, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.models.with_raw_response.delete(
            "model_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert_matches_type(ModelDeleteResponse, model, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.models.with_streaming_response.delete(
            "model_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert_matches_type(ModelDeleteResponse, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_id` but received ''"):
            client.models.with_raw_response.delete(
                "",
            )


class TestAsyncModels:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        model = await async_client.models.create(
            model={
                "name": "name",
                "vendor_configuration": {
                    "model_image": {
                        "command": ["string"],
                        "registry": "registry",
                        "repository": "repository",
                        "tag": "tag",
                    },
                    "model_infra": {},
                },
                "model_vendor": "launch",
            },
        )
        assert_matches_type(InferenceModel, model, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        model = await async_client.models.create(
            model={
                "name": "name",
                "vendor_configuration": {
                    "model_image": {
                        "command": ["string"],
                        "registry": "registry",
                        "repository": "repository",
                        "tag": "tag",
                        "env_vars": {"foo": "bar"},
                        "healthcheck_route": "healthcheck_route",
                        "predict_route": "predict_route",
                        "readiness_delay": 0,
                        "request_schema": {"foo": "bar"},
                        "response_schema": {"foo": "bar"},
                        "streaming_command": ["string"],
                        "streaming_predict_route": "streaming_predict_route",
                    },
                    "model_infra": {
                        "cpus": "string",
                        "endpoint_type": "async",
                        "gpu_type": "nvidia-tesla-t4",
                        "gpus": 0,
                        "high_priority": True,
                        "labels": {"foo": "string"},
                        "max_workers": 0,
                        "memory": "memory",
                        "min_workers": 0,
                        "per_worker": 0,
                        "public_inference": True,
                        "storage": "storage",
                    },
                },
                "model_metadata": {"foo": "bar"},
                "model_type": "generic",
                "model_vendor": "launch",
                "on_conflict": "error",
            },
        )
        assert_matches_type(InferenceModel, model, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.models.with_raw_response.create(
            model={
                "name": "name",
                "vendor_configuration": {
                    "model_image": {
                        "command": ["string"],
                        "registry": "registry",
                        "repository": "repository",
                        "tag": "tag",
                    },
                    "model_infra": {},
                },
                "model_vendor": "launch",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert_matches_type(InferenceModel, model, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.models.with_streaming_response.create(
            model={
                "name": "name",
                "vendor_configuration": {
                    "model_image": {
                        "command": ["string"],
                        "registry": "registry",
                        "repository": "repository",
                        "tag": "tag",
                    },
                    "model_infra": {},
                },
                "model_vendor": "launch",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert_matches_type(InferenceModel, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        model = await async_client.models.retrieve(
            "model_id",
        )
        assert_matches_type(InferenceModel, model, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.models.with_raw_response.retrieve(
            "model_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert_matches_type(InferenceModel, model, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.models.with_streaming_response.retrieve(
            "model_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert_matches_type(InferenceModel, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_id` but received ''"):
            await async_client.models.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        model = await async_client.models.update(
            model_id="model_id",
            model={},
        )
        assert_matches_type(InferenceModel, model, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        model = await async_client.models.update(
            model_id="model_id",
            model={"model_metadata": {"foo": "bar"}},
        )
        assert_matches_type(InferenceModel, model, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.models.with_raw_response.update(
            model_id="model_id",
            model={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert_matches_type(InferenceModel, model, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.models.with_streaming_response.update(
            model_id="model_id",
            model={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert_matches_type(InferenceModel, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_id` but received ''"):
            await async_client.models.with_raw_response.update(
                model_id="",
                model={},
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        model = await async_client.models.list()
        assert_matches_type(AsyncCursorPage[InferenceModel], model, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        model = await async_client.models.list(
            ending_before="ending_before",
            limit=1,
            model_vendor="openai",
            name="name",
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
        )
        assert_matches_type(AsyncCursorPage[InferenceModel], model, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.models.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert_matches_type(AsyncCursorPage[InferenceModel], model, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.models.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert_matches_type(AsyncCursorPage[InferenceModel], model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        model = await async_client.models.delete(
            "model_id",
        )
        assert_matches_type(ModelDeleteResponse, model, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.models.with_raw_response.delete(
            "model_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert_matches_type(ModelDeleteResponse, model, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.models.with_streaming_response.delete(
            "model_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert_matches_type(ModelDeleteResponse, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_id` but received ''"):
            await async_client.models.with_raw_response.delete(
                "",
            )
