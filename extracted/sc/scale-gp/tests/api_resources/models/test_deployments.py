# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.pagination import SyncPageResponse, AsyncPageResponse
from scale_gp.types.models import (
    ModelDeployment,
)
from scale_gp.types.shared import GenericDeleteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDeployments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        deployment = client.models.deployments.create(
            model_instance_id="model_instance_id",
            name="name",
        )
        assert_matches_type(ModelDeployment, deployment, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        deployment = client.models.deployments.create(
            model_instance_id="model_instance_id",
            name="name",
            account_id="account_id",
            deployment_metadata={"foo": "bar"},
            model_creation_parameters={"foo": "bar"},
            vendor_configuration={
                "max_workers": 0,
                "min_workers": 0,
                "per_worker": 0,
                "vendor": "LAUNCH",
            },
        )
        assert_matches_type(ModelDeployment, deployment, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.models.deployments.with_raw_response.create(
            model_instance_id="model_instance_id",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(ModelDeployment, deployment, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.models.deployments.with_streaming_response.create(
            model_instance_id="model_instance_id",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(ModelDeployment, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            client.models.deployments.with_raw_response.create(
                model_instance_id="",
                name="name",
            )

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        deployment = client.models.deployments.retrieve(
            deployment_id="deployment_id",
            model_instance_id="model_instance_id",
        )
        assert_matches_type(ModelDeployment, deployment, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.models.deployments.with_raw_response.retrieve(
            deployment_id="deployment_id",
            model_instance_id="model_instance_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(ModelDeployment, deployment, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.models.deployments.with_streaming_response.retrieve(
            deployment_id="deployment_id",
            model_instance_id="model_instance_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(ModelDeployment, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            client.models.deployments.with_raw_response.retrieve(
                deployment_id="deployment_id",
                model_instance_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.models.deployments.with_raw_response.retrieve(
                deployment_id="",
                model_instance_id="model_instance_id",
            )

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        deployment = client.models.deployments.update(
            deployment_id="deployment_id",
            model_instance_id="model_instance_id",
        )
        assert_matches_type(ModelDeployment, deployment, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGPClient) -> None:
        deployment = client.models.deployments.update(
            deployment_id="deployment_id",
            model_instance_id="model_instance_id",
            deployment_metadata={"foo": "bar"},
            model_creation_parameters={"foo": "bar"},
            name="name",
            vendor_configuration={
                "max_workers": 0,
                "min_workers": 0,
                "per_worker": 0,
                "vendor": "LAUNCH",
            },
        )
        assert_matches_type(ModelDeployment, deployment, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.models.deployments.with_raw_response.update(
            deployment_id="deployment_id",
            model_instance_id="model_instance_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(ModelDeployment, deployment, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.models.deployments.with_streaming_response.update(
            deployment_id="deployment_id",
            model_instance_id="model_instance_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(ModelDeployment, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            client.models.deployments.with_raw_response.update(
                deployment_id="deployment_id",
                model_instance_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.models.deployments.with_raw_response.update(
                deployment_id="",
                model_instance_id="model_instance_id",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        deployment = client.models.deployments.list(
            model_instance_id="model_instance_id",
        )
        assert_matches_type(SyncPageResponse[ModelDeployment], deployment, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        deployment = client.models.deployments.list(
            model_instance_id="model_instance_id",
            account_id="account_id",
            limit=1,
            page=1,
            sort_by=["model_creation_parameters:asc"],
        )
        assert_matches_type(SyncPageResponse[ModelDeployment], deployment, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.models.deployments.with_raw_response.list(
            model_instance_id="model_instance_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(SyncPageResponse[ModelDeployment], deployment, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.models.deployments.with_streaming_response.list(
            model_instance_id="model_instance_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(SyncPageResponse[ModelDeployment], deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            client.models.deployments.with_raw_response.list(
                model_instance_id="",
            )

    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        deployment = client.models.deployments.delete(
            deployment_id="deployment_id",
            model_instance_id="model_instance_id",
        )
        assert_matches_type(GenericDeleteResponse, deployment, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.models.deployments.with_raw_response.delete(
            deployment_id="deployment_id",
            model_instance_id="model_instance_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(GenericDeleteResponse, deployment, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.models.deployments.with_streaming_response.delete(
            deployment_id="deployment_id",
            model_instance_id="model_instance_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(GenericDeleteResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            client.models.deployments.with_raw_response.delete(
                deployment_id="deployment_id",
                model_instance_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.models.deployments.with_raw_response.delete(
                deployment_id="",
                model_instance_id="model_instance_id",
            )

    @parametrize
    def test_method_execute(self, client: SGPClient) -> None:
        deployment = client.models.deployments.execute(
            model_deployment_id="model_deployment_id",
            model_instance_id="model_instance_id",
        )
        assert_matches_type(object, deployment, path=["response"])

    @parametrize
    def test_method_execute_with_all_params(self, client: SGPClient) -> None:
        deployment = client.models.deployments.execute(
            model_deployment_id="model_deployment_id",
            model_instance_id="model_instance_id",
            stream=True,
        )
        assert_matches_type(object, deployment, path=["response"])

    @parametrize
    def test_raw_response_execute(self, client: SGPClient) -> None:
        response = client.models.deployments.with_raw_response.execute(
            model_deployment_id="model_deployment_id",
            model_instance_id="model_instance_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(object, deployment, path=["response"])

    @parametrize
    def test_streaming_response_execute(self, client: SGPClient) -> None:
        with client.models.deployments.with_streaming_response.execute(
            model_deployment_id="model_deployment_id",
            model_instance_id="model_instance_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(object, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_execute(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            client.models.deployments.with_raw_response.execute(
                model_deployment_id="model_deployment_id",
                model_instance_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_deployment_id` but received ''"):
            client.models.deployments.with_raw_response.execute(
                model_deployment_id="",
                model_instance_id="model_instance_id",
            )

    @parametrize
    def test_method_list_all(self, client: SGPClient) -> None:
        deployment = client.models.deployments.list_all()
        assert_matches_type(SyncPageResponse[ModelDeployment], deployment, path=["response"])

    @parametrize
    def test_method_list_all_with_all_params(self, client: SGPClient) -> None:
        deployment = client.models.deployments.list_all(
            account_id="account_id",
            limit=1,
            page=1,
            sort_by=["model_creation_parameters:asc"],
        )
        assert_matches_type(SyncPageResponse[ModelDeployment], deployment, path=["response"])

    @parametrize
    def test_raw_response_list_all(self, client: SGPClient) -> None:
        response = client.models.deployments.with_raw_response.list_all()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(SyncPageResponse[ModelDeployment], deployment, path=["response"])

    @parametrize
    def test_streaming_response_list_all(self, client: SGPClient) -> None:
        with client.models.deployments.with_streaming_response.list_all() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(SyncPageResponse[ModelDeployment], deployment, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDeployments:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        deployment = await async_client.models.deployments.create(
            model_instance_id="model_instance_id",
            name="name",
        )
        assert_matches_type(ModelDeployment, deployment, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        deployment = await async_client.models.deployments.create(
            model_instance_id="model_instance_id",
            name="name",
            account_id="account_id",
            deployment_metadata={"foo": "bar"},
            model_creation_parameters={"foo": "bar"},
            vendor_configuration={
                "max_workers": 0,
                "min_workers": 0,
                "per_worker": 0,
                "vendor": "LAUNCH",
            },
        )
        assert_matches_type(ModelDeployment, deployment, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.models.deployments.with_raw_response.create(
            model_instance_id="model_instance_id",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(ModelDeployment, deployment, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.models.deployments.with_streaming_response.create(
            model_instance_id="model_instance_id",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(ModelDeployment, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            await async_client.models.deployments.with_raw_response.create(
                model_instance_id="",
                name="name",
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        deployment = await async_client.models.deployments.retrieve(
            deployment_id="deployment_id",
            model_instance_id="model_instance_id",
        )
        assert_matches_type(ModelDeployment, deployment, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.models.deployments.with_raw_response.retrieve(
            deployment_id="deployment_id",
            model_instance_id="model_instance_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(ModelDeployment, deployment, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.models.deployments.with_streaming_response.retrieve(
            deployment_id="deployment_id",
            model_instance_id="model_instance_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(ModelDeployment, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            await async_client.models.deployments.with_raw_response.retrieve(
                deployment_id="deployment_id",
                model_instance_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.models.deployments.with_raw_response.retrieve(
                deployment_id="",
                model_instance_id="model_instance_id",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        deployment = await async_client.models.deployments.update(
            deployment_id="deployment_id",
            model_instance_id="model_instance_id",
        )
        assert_matches_type(ModelDeployment, deployment, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        deployment = await async_client.models.deployments.update(
            deployment_id="deployment_id",
            model_instance_id="model_instance_id",
            deployment_metadata={"foo": "bar"},
            model_creation_parameters={"foo": "bar"},
            name="name",
            vendor_configuration={
                "max_workers": 0,
                "min_workers": 0,
                "per_worker": 0,
                "vendor": "LAUNCH",
            },
        )
        assert_matches_type(ModelDeployment, deployment, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.models.deployments.with_raw_response.update(
            deployment_id="deployment_id",
            model_instance_id="model_instance_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(ModelDeployment, deployment, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.models.deployments.with_streaming_response.update(
            deployment_id="deployment_id",
            model_instance_id="model_instance_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(ModelDeployment, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            await async_client.models.deployments.with_raw_response.update(
                deployment_id="deployment_id",
                model_instance_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.models.deployments.with_raw_response.update(
                deployment_id="",
                model_instance_id="model_instance_id",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        deployment = await async_client.models.deployments.list(
            model_instance_id="model_instance_id",
        )
        assert_matches_type(AsyncPageResponse[ModelDeployment], deployment, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        deployment = await async_client.models.deployments.list(
            model_instance_id="model_instance_id",
            account_id="account_id",
            limit=1,
            page=1,
            sort_by=["model_creation_parameters:asc"],
        )
        assert_matches_type(AsyncPageResponse[ModelDeployment], deployment, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.models.deployments.with_raw_response.list(
            model_instance_id="model_instance_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(AsyncPageResponse[ModelDeployment], deployment, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.models.deployments.with_streaming_response.list(
            model_instance_id="model_instance_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(AsyncPageResponse[ModelDeployment], deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            await async_client.models.deployments.with_raw_response.list(
                model_instance_id="",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        deployment = await async_client.models.deployments.delete(
            deployment_id="deployment_id",
            model_instance_id="model_instance_id",
        )
        assert_matches_type(GenericDeleteResponse, deployment, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.models.deployments.with_raw_response.delete(
            deployment_id="deployment_id",
            model_instance_id="model_instance_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(GenericDeleteResponse, deployment, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.models.deployments.with_streaming_response.delete(
            deployment_id="deployment_id",
            model_instance_id="model_instance_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(GenericDeleteResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            await async_client.models.deployments.with_raw_response.delete(
                deployment_id="deployment_id",
                model_instance_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.models.deployments.with_raw_response.delete(
                deployment_id="",
                model_instance_id="model_instance_id",
            )

    @parametrize
    async def test_method_execute(self, async_client: AsyncSGPClient) -> None:
        deployment = await async_client.models.deployments.execute(
            model_deployment_id="model_deployment_id",
            model_instance_id="model_instance_id",
        )
        assert_matches_type(object, deployment, path=["response"])

    @parametrize
    async def test_method_execute_with_all_params(self, async_client: AsyncSGPClient) -> None:
        deployment = await async_client.models.deployments.execute(
            model_deployment_id="model_deployment_id",
            model_instance_id="model_instance_id",
            stream=True,
        )
        assert_matches_type(object, deployment, path=["response"])

    @parametrize
    async def test_raw_response_execute(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.models.deployments.with_raw_response.execute(
            model_deployment_id="model_deployment_id",
            model_instance_id="model_instance_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(object, deployment, path=["response"])

    @parametrize
    async def test_streaming_response_execute(self, async_client: AsyncSGPClient) -> None:
        async with async_client.models.deployments.with_streaming_response.execute(
            model_deployment_id="model_deployment_id",
            model_instance_id="model_instance_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(object, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_execute(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_instance_id` but received ''"):
            await async_client.models.deployments.with_raw_response.execute(
                model_deployment_id="model_deployment_id",
                model_instance_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_deployment_id` but received ''"):
            await async_client.models.deployments.with_raw_response.execute(
                model_deployment_id="",
                model_instance_id="model_instance_id",
            )

    @parametrize
    async def test_method_list_all(self, async_client: AsyncSGPClient) -> None:
        deployment = await async_client.models.deployments.list_all()
        assert_matches_type(AsyncPageResponse[ModelDeployment], deployment, path=["response"])

    @parametrize
    async def test_method_list_all_with_all_params(self, async_client: AsyncSGPClient) -> None:
        deployment = await async_client.models.deployments.list_all(
            account_id="account_id",
            limit=1,
            page=1,
            sort_by=["model_creation_parameters:asc"],
        )
        assert_matches_type(AsyncPageResponse[ModelDeployment], deployment, path=["response"])

    @parametrize
    async def test_raw_response_list_all(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.models.deployments.with_raw_response.list_all()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(AsyncPageResponse[ModelDeployment], deployment, path=["response"])

    @parametrize
    async def test_streaming_response_list_all(self, async_client: AsyncSGPClient) -> None:
        async with async_client.models.deployments.with_streaming_response.list_all() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(AsyncPageResponse[ModelDeployment], deployment, path=["response"])

        assert cast(Any, response.is_closed) is True
