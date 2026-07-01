# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import (
    ModelInstance,
    ModelInstanceWithViews,
)
from scale_gp.pagination import SyncPageResponse, AsyncPageResponse
from scale_gp.types.shared import GenericDeleteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestModels:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        model = client.models.create(
            account_id="account_id",
            model_type="COMPLETION",
            name="name",
        )
        assert_matches_type(ModelInstance, model, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        model = client.models.create(
            account_id="account_id",
            model_type="COMPLETION",
            name="name",
            base_model_id="base_model_id",
            base_model_metadata={
                "delivery_date": "delivery_date",
                "model_developer": "model_developer",
                "model_license_url": "model_license_url",
                "model_details": {
                    "alignments": 0,
                    "languages": 0,
                    "number_of_parameters": 0,
                    "token_context_window": 0,
                },
                "ui_model_section_type": "PARTNER",
            },
            description="description",
            display_name="display_name",
            model_card="model_card",
            model_creation_parameters={"foo": "bar"},
            model_group_id="model_group_id",
            model_template_id="model_template_id",
            model_vendor="OPENAI",
            training_data_card="training_data_card",
        )
        assert_matches_type(ModelInstance, model, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.models.with_raw_response.create(
            account_id="account_id",
            model_type="COMPLETION",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert_matches_type(ModelInstance, model, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.models.with_streaming_response.create(
            account_id="account_id",
            model_type="COMPLETION",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert_matches_type(ModelInstance, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        model = client.models.retrieve(
            model_id="model_id",
        )
        assert_matches_type(ModelInstanceWithViews, model, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGPClient) -> None:
        model = client.models.retrieve(
            model_id="model_id",
            view=["Deployments"],
        )
        assert_matches_type(ModelInstanceWithViews, model, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.models.with_raw_response.retrieve(
            model_id="model_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert_matches_type(ModelInstanceWithViews, model, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.models.with_streaming_response.retrieve(
            model_id="model_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert_matches_type(ModelInstanceWithViews, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_id` but received ''"):
            client.models.with_raw_response.retrieve(
                model_id="",
            )

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        model = client.models.update(
            model_id="model_id",
        )
        assert_matches_type(ModelInstance, model, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGPClient) -> None:
        model = client.models.update(
            model_id="model_id",
            base_model_id="base_model_id",
            base_model_metadata={
                "delivery_date": "delivery_date",
                "model_developer": "model_developer",
                "model_license_url": "model_license_url",
                "model_details": {
                    "alignments": 0,
                    "languages": 0,
                    "number_of_parameters": 0,
                    "token_context_window": 0,
                },
                "ui_model_section_type": "PARTNER",
            },
            description="description",
            display_name="display_name",
            model_card="model_card",
            model_creation_parameters={"foo": "bar"},
            model_group_id="model_group_id",
            model_template_id="model_template_id",
            model_type="COMPLETION",
            model_vendor="OPENAI",
            name="name",
            training_data_card="training_data_card",
        )
        assert_matches_type(ModelInstance, model, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.models.with_raw_response.update(
            model_id="model_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert_matches_type(ModelInstance, model, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.models.with_streaming_response.update(
            model_id="model_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert_matches_type(ModelInstance, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_id` but received ''"):
            client.models.with_raw_response.update(
                model_id="",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        model = client.models.list()
        assert_matches_type(SyncPageResponse[ModelInstanceWithViews], model, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        model = client.models.list(
            account_id="account_id",
            limit=1,
            model_group_id=0,
            model_type=0,
            page=1,
            sort_by=["display_name:asc"],
            view=["Deployments"],
        )
        assert_matches_type(SyncPageResponse[ModelInstanceWithViews], model, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.models.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert_matches_type(SyncPageResponse[ModelInstanceWithViews], model, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.models.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert_matches_type(SyncPageResponse[ModelInstanceWithViews], model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        model = client.models.delete(
            "model_id",
        )
        assert_matches_type(GenericDeleteResponse, model, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.models.with_raw_response.delete(
            "model_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert_matches_type(GenericDeleteResponse, model, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.models.with_streaming_response.delete(
            "model_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert_matches_type(GenericDeleteResponse, model, path=["response"])

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
            account_id="account_id",
            model_type="COMPLETION",
            name="name",
        )
        assert_matches_type(ModelInstance, model, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        model = await async_client.models.create(
            account_id="account_id",
            model_type="COMPLETION",
            name="name",
            base_model_id="base_model_id",
            base_model_metadata={
                "delivery_date": "delivery_date",
                "model_developer": "model_developer",
                "model_license_url": "model_license_url",
                "model_details": {
                    "alignments": 0,
                    "languages": 0,
                    "number_of_parameters": 0,
                    "token_context_window": 0,
                },
                "ui_model_section_type": "PARTNER",
            },
            description="description",
            display_name="display_name",
            model_card="model_card",
            model_creation_parameters={"foo": "bar"},
            model_group_id="model_group_id",
            model_template_id="model_template_id",
            model_vendor="OPENAI",
            training_data_card="training_data_card",
        )
        assert_matches_type(ModelInstance, model, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.models.with_raw_response.create(
            account_id="account_id",
            model_type="COMPLETION",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert_matches_type(ModelInstance, model, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.models.with_streaming_response.create(
            account_id="account_id",
            model_type="COMPLETION",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert_matches_type(ModelInstance, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        model = await async_client.models.retrieve(
            model_id="model_id",
        )
        assert_matches_type(ModelInstanceWithViews, model, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGPClient) -> None:
        model = await async_client.models.retrieve(
            model_id="model_id",
            view=["Deployments"],
        )
        assert_matches_type(ModelInstanceWithViews, model, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.models.with_raw_response.retrieve(
            model_id="model_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert_matches_type(ModelInstanceWithViews, model, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.models.with_streaming_response.retrieve(
            model_id="model_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert_matches_type(ModelInstanceWithViews, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_id` but received ''"):
            await async_client.models.with_raw_response.retrieve(
                model_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        model = await async_client.models.update(
            model_id="model_id",
        )
        assert_matches_type(ModelInstance, model, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        model = await async_client.models.update(
            model_id="model_id",
            base_model_id="base_model_id",
            base_model_metadata={
                "delivery_date": "delivery_date",
                "model_developer": "model_developer",
                "model_license_url": "model_license_url",
                "model_details": {
                    "alignments": 0,
                    "languages": 0,
                    "number_of_parameters": 0,
                    "token_context_window": 0,
                },
                "ui_model_section_type": "PARTNER",
            },
            description="description",
            display_name="display_name",
            model_card="model_card",
            model_creation_parameters={"foo": "bar"},
            model_group_id="model_group_id",
            model_template_id="model_template_id",
            model_type="COMPLETION",
            model_vendor="OPENAI",
            name="name",
            training_data_card="training_data_card",
        )
        assert_matches_type(ModelInstance, model, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.models.with_raw_response.update(
            model_id="model_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert_matches_type(ModelInstance, model, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.models.with_streaming_response.update(
            model_id="model_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert_matches_type(ModelInstance, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_id` but received ''"):
            await async_client.models.with_raw_response.update(
                model_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        model = await async_client.models.list()
        assert_matches_type(AsyncPageResponse[ModelInstanceWithViews], model, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        model = await async_client.models.list(
            account_id="account_id",
            limit=1,
            model_group_id=0,
            model_type=0,
            page=1,
            sort_by=["display_name:asc"],
            view=["Deployments"],
        )
        assert_matches_type(AsyncPageResponse[ModelInstanceWithViews], model, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.models.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert_matches_type(AsyncPageResponse[ModelInstanceWithViews], model, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.models.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert_matches_type(AsyncPageResponse[ModelInstanceWithViews], model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        model = await async_client.models.delete(
            "model_id",
        )
        assert_matches_type(GenericDeleteResponse, model, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.models.with_raw_response.delete(
            "model_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert_matches_type(GenericDeleteResponse, model, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.models.with_streaming_response.delete(
            "model_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert_matches_type(GenericDeleteResponse, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_id` but received ''"):
            await async_client.models.with_raw_response.delete(
                "",
            )
