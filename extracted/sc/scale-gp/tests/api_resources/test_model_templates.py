# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import ModelTemplate
from scale_gp.pagination import SyncPageResponse, AsyncPageResponse
from scale_gp.types.shared import GenericDeleteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestModelTemplates:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        model_template = client.model_templates.create(
            account_id="account_id",
            endpoint_type="SYNC",
            model_type="COMPLETION",
            name="name",
            vendor_configuration={
                "bundle_config": {
                    "image": "image",
                    "registry": "registry",
                    "tag": "tag",
                }
            },
        )
        assert_matches_type(ModelTemplate, model_template, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        model_template = client.model_templates.create(
            account_id="account_id",
            endpoint_type="SYNC",
            model_type="COMPLETION",
            name="name",
            vendor_configuration={
                "bundle_config": {
                    "image": "image",
                    "registry": "registry",
                    "tag": "tag",
                    "command": ["string"],
                    "env": {"foo": "string"},
                    "healthcheck_route": "healthcheck_route",
                    "predict_route": "predict_route",
                    "readiness_initial_delay_seconds": 0,
                    "streaming_command": ["string"],
                    "streaming_predict_route": "streaming_predict_route",
                },
                "endpoint_config": {
                    "cpus": 0,
                    "endpoint_type": "SYNC",
                    "gpu_type": "nvidia-tesla-t4",
                    "gpus": 0,
                    "high_priority": True,
                    "max_workers": 0,
                    "memory": "memory",
                    "min_workers": 0,
                    "per_worker": 0,
                    "storage": "storage",
                },
                "fine_tuning_job_bundle_config": {
                    "image": "image",
                    "registry": "registry",
                    "tag": "tag",
                    "command": ["string"],
                    "env": {"foo": "string"},
                    "mount_location": "mount_location",
                    "resources": {
                        "cpus": 0,
                        "gpu_type": "nvidia-tesla-t4",
                        "gpus": 0,
                        "memory": "memory",
                        "storage": "storage",
                    },
                    "training_dataset_schema_type": "GENERATION",
                },
                "vendor": "LAUNCH",
            },
            endpoint_protocol="SGP",
            model_creation_parameters_schema={
                "parameters": [
                    {
                        "description": "description",
                        "name": "name",
                        "required": True,
                        "type": "str",
                    }
                ]
            },
            model_request_parameters_schema={
                "parameters": [
                    {
                        "description": "description",
                        "name": "name",
                        "required": True,
                        "type": "str",
                    }
                ]
            },
        )
        assert_matches_type(ModelTemplate, model_template, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.model_templates.with_raw_response.create(
            account_id="account_id",
            endpoint_type="SYNC",
            model_type="COMPLETION",
            name="name",
            vendor_configuration={
                "bundle_config": {
                    "image": "image",
                    "registry": "registry",
                    "tag": "tag",
                }
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_template = response.parse()
        assert_matches_type(ModelTemplate, model_template, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.model_templates.with_streaming_response.create(
            account_id="account_id",
            endpoint_type="SYNC",
            model_type="COMPLETION",
            name="name",
            vendor_configuration={
                "bundle_config": {
                    "image": "image",
                    "registry": "registry",
                    "tag": "tag",
                }
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_template = response.parse()
            assert_matches_type(ModelTemplate, model_template, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        model_template = client.model_templates.retrieve(
            "model_template_id",
        )
        assert_matches_type(ModelTemplate, model_template, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.model_templates.with_raw_response.retrieve(
            "model_template_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_template = response.parse()
        assert_matches_type(ModelTemplate, model_template, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.model_templates.with_streaming_response.retrieve(
            "model_template_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_template = response.parse()
            assert_matches_type(ModelTemplate, model_template, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_template_id` but received ''"):
            client.model_templates.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        model_template = client.model_templates.list()
        assert_matches_type(SyncPageResponse[ModelTemplate], model_template, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        model_template = client.model_templates.list(
            account_id="account_id",
            limit=1,
            page=1,
        )
        assert_matches_type(SyncPageResponse[ModelTemplate], model_template, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.model_templates.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_template = response.parse()
        assert_matches_type(SyncPageResponse[ModelTemplate], model_template, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.model_templates.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_template = response.parse()
            assert_matches_type(SyncPageResponse[ModelTemplate], model_template, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        model_template = client.model_templates.delete(
            "model_template_id",
        )
        assert_matches_type(GenericDeleteResponse, model_template, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.model_templates.with_raw_response.delete(
            "model_template_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_template = response.parse()
        assert_matches_type(GenericDeleteResponse, model_template, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.model_templates.with_streaming_response.delete(
            "model_template_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_template = response.parse()
            assert_matches_type(GenericDeleteResponse, model_template, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_template_id` but received ''"):
            client.model_templates.with_raw_response.delete(
                "",
            )


class TestAsyncModelTemplates:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        model_template = await async_client.model_templates.create(
            account_id="account_id",
            endpoint_type="SYNC",
            model_type="COMPLETION",
            name="name",
            vendor_configuration={
                "bundle_config": {
                    "image": "image",
                    "registry": "registry",
                    "tag": "tag",
                }
            },
        )
        assert_matches_type(ModelTemplate, model_template, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        model_template = await async_client.model_templates.create(
            account_id="account_id",
            endpoint_type="SYNC",
            model_type="COMPLETION",
            name="name",
            vendor_configuration={
                "bundle_config": {
                    "image": "image",
                    "registry": "registry",
                    "tag": "tag",
                    "command": ["string"],
                    "env": {"foo": "string"},
                    "healthcheck_route": "healthcheck_route",
                    "predict_route": "predict_route",
                    "readiness_initial_delay_seconds": 0,
                    "streaming_command": ["string"],
                    "streaming_predict_route": "streaming_predict_route",
                },
                "endpoint_config": {
                    "cpus": 0,
                    "endpoint_type": "SYNC",
                    "gpu_type": "nvidia-tesla-t4",
                    "gpus": 0,
                    "high_priority": True,
                    "max_workers": 0,
                    "memory": "memory",
                    "min_workers": 0,
                    "per_worker": 0,
                    "storage": "storage",
                },
                "fine_tuning_job_bundle_config": {
                    "image": "image",
                    "registry": "registry",
                    "tag": "tag",
                    "command": ["string"],
                    "env": {"foo": "string"},
                    "mount_location": "mount_location",
                    "resources": {
                        "cpus": 0,
                        "gpu_type": "nvidia-tesla-t4",
                        "gpus": 0,
                        "memory": "memory",
                        "storage": "storage",
                    },
                    "training_dataset_schema_type": "GENERATION",
                },
                "vendor": "LAUNCH",
            },
            endpoint_protocol="SGP",
            model_creation_parameters_schema={
                "parameters": [
                    {
                        "description": "description",
                        "name": "name",
                        "required": True,
                        "type": "str",
                    }
                ]
            },
            model_request_parameters_schema={
                "parameters": [
                    {
                        "description": "description",
                        "name": "name",
                        "required": True,
                        "type": "str",
                    }
                ]
            },
        )
        assert_matches_type(ModelTemplate, model_template, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.model_templates.with_raw_response.create(
            account_id="account_id",
            endpoint_type="SYNC",
            model_type="COMPLETION",
            name="name",
            vendor_configuration={
                "bundle_config": {
                    "image": "image",
                    "registry": "registry",
                    "tag": "tag",
                }
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_template = await response.parse()
        assert_matches_type(ModelTemplate, model_template, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.model_templates.with_streaming_response.create(
            account_id="account_id",
            endpoint_type="SYNC",
            model_type="COMPLETION",
            name="name",
            vendor_configuration={
                "bundle_config": {
                    "image": "image",
                    "registry": "registry",
                    "tag": "tag",
                }
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_template = await response.parse()
            assert_matches_type(ModelTemplate, model_template, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        model_template = await async_client.model_templates.retrieve(
            "model_template_id",
        )
        assert_matches_type(ModelTemplate, model_template, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.model_templates.with_raw_response.retrieve(
            "model_template_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_template = await response.parse()
        assert_matches_type(ModelTemplate, model_template, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.model_templates.with_streaming_response.retrieve(
            "model_template_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_template = await response.parse()
            assert_matches_type(ModelTemplate, model_template, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_template_id` but received ''"):
            await async_client.model_templates.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        model_template = await async_client.model_templates.list()
        assert_matches_type(AsyncPageResponse[ModelTemplate], model_template, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        model_template = await async_client.model_templates.list(
            account_id="account_id",
            limit=1,
            page=1,
        )
        assert_matches_type(AsyncPageResponse[ModelTemplate], model_template, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.model_templates.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_template = await response.parse()
        assert_matches_type(AsyncPageResponse[ModelTemplate], model_template, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.model_templates.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_template = await response.parse()
            assert_matches_type(AsyncPageResponse[ModelTemplate], model_template, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        model_template = await async_client.model_templates.delete(
            "model_template_id",
        )
        assert_matches_type(GenericDeleteResponse, model_template, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.model_templates.with_raw_response.delete(
            "model_template_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_template = await response.parse()
        assert_matches_type(GenericDeleteResponse, model_template, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.model_templates.with_streaming_response.delete(
            "model_template_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_template = await response.parse()
            assert_matches_type(GenericDeleteResponse, model_template, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_template_id` but received ''"):
            await async_client.model_templates.with_raw_response.delete(
                "",
            )
