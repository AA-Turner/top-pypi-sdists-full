# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import ModelGroup
from scale_gp.pagination import SyncPageResponse, AsyncPageResponse
from scale_gp.types.shared import GenericDeleteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestModelGroups:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        model_group = client.model_groups.create(
            account_id="account_id",
            name="name",
        )
        assert_matches_type(ModelGroup, model_group, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        model_group = client.model_groups.create(
            account_id="account_id",
            name="name",
            description="description",
        )
        assert_matches_type(ModelGroup, model_group, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.model_groups.with_raw_response.create(
            account_id="account_id",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_group = response.parse()
        assert_matches_type(ModelGroup, model_group, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.model_groups.with_streaming_response.create(
            account_id="account_id",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_group = response.parse()
            assert_matches_type(ModelGroup, model_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        model_group = client.model_groups.retrieve(
            "model_group_id",
        )
        assert_matches_type(ModelGroup, model_group, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.model_groups.with_raw_response.retrieve(
            "model_group_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_group = response.parse()
        assert_matches_type(ModelGroup, model_group, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.model_groups.with_streaming_response.retrieve(
            "model_group_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_group = response.parse()
            assert_matches_type(ModelGroup, model_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_group_id` but received ''"):
            client.model_groups.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        model_group = client.model_groups.update(
            model_group_id="model_group_id",
        )
        assert_matches_type(ModelGroup, model_group, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGPClient) -> None:
        model_group = client.model_groups.update(
            model_group_id="model_group_id",
            description="description",
            name="name",
        )
        assert_matches_type(ModelGroup, model_group, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.model_groups.with_raw_response.update(
            model_group_id="model_group_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_group = response.parse()
        assert_matches_type(ModelGroup, model_group, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.model_groups.with_streaming_response.update(
            model_group_id="model_group_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_group = response.parse()
            assert_matches_type(ModelGroup, model_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_group_id` but received ''"):
            client.model_groups.with_raw_response.update(
                model_group_id="",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        model_group = client.model_groups.list()
        assert_matches_type(SyncPageResponse[ModelGroup], model_group, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        model_group = client.model_groups.list(
            account_id="account_id",
            limit=1,
            page=1,
        )
        assert_matches_type(SyncPageResponse[ModelGroup], model_group, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.model_groups.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_group = response.parse()
        assert_matches_type(SyncPageResponse[ModelGroup], model_group, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.model_groups.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_group = response.parse()
            assert_matches_type(SyncPageResponse[ModelGroup], model_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        model_group = client.model_groups.delete(
            "model_group_id",
        )
        assert_matches_type(GenericDeleteResponse, model_group, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.model_groups.with_raw_response.delete(
            "model_group_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_group = response.parse()
        assert_matches_type(GenericDeleteResponse, model_group, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.model_groups.with_streaming_response.delete(
            "model_group_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_group = response.parse()
            assert_matches_type(GenericDeleteResponse, model_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_group_id` but received ''"):
            client.model_groups.with_raw_response.delete(
                "",
            )


class TestAsyncModelGroups:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        model_group = await async_client.model_groups.create(
            account_id="account_id",
            name="name",
        )
        assert_matches_type(ModelGroup, model_group, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        model_group = await async_client.model_groups.create(
            account_id="account_id",
            name="name",
            description="description",
        )
        assert_matches_type(ModelGroup, model_group, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.model_groups.with_raw_response.create(
            account_id="account_id",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_group = await response.parse()
        assert_matches_type(ModelGroup, model_group, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.model_groups.with_streaming_response.create(
            account_id="account_id",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_group = await response.parse()
            assert_matches_type(ModelGroup, model_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        model_group = await async_client.model_groups.retrieve(
            "model_group_id",
        )
        assert_matches_type(ModelGroup, model_group, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.model_groups.with_raw_response.retrieve(
            "model_group_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_group = await response.parse()
        assert_matches_type(ModelGroup, model_group, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.model_groups.with_streaming_response.retrieve(
            "model_group_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_group = await response.parse()
            assert_matches_type(ModelGroup, model_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_group_id` but received ''"):
            await async_client.model_groups.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        model_group = await async_client.model_groups.update(
            model_group_id="model_group_id",
        )
        assert_matches_type(ModelGroup, model_group, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        model_group = await async_client.model_groups.update(
            model_group_id="model_group_id",
            description="description",
            name="name",
        )
        assert_matches_type(ModelGroup, model_group, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.model_groups.with_raw_response.update(
            model_group_id="model_group_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_group = await response.parse()
        assert_matches_type(ModelGroup, model_group, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.model_groups.with_streaming_response.update(
            model_group_id="model_group_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_group = await response.parse()
            assert_matches_type(ModelGroup, model_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_group_id` but received ''"):
            await async_client.model_groups.with_raw_response.update(
                model_group_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        model_group = await async_client.model_groups.list()
        assert_matches_type(AsyncPageResponse[ModelGroup], model_group, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        model_group = await async_client.model_groups.list(
            account_id="account_id",
            limit=1,
            page=1,
        )
        assert_matches_type(AsyncPageResponse[ModelGroup], model_group, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.model_groups.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_group = await response.parse()
        assert_matches_type(AsyncPageResponse[ModelGroup], model_group, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.model_groups.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_group = await response.parse()
            assert_matches_type(AsyncPageResponse[ModelGroup], model_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        model_group = await async_client.model_groups.delete(
            "model_group_id",
        )
        assert_matches_type(GenericDeleteResponse, model_group, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.model_groups.with_raw_response.delete(
            "model_group_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model_group = await response.parse()
        assert_matches_type(GenericDeleteResponse, model_group, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.model_groups.with_streaming_response.delete(
            "model_group_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model_group = await response.parse()
            assert_matches_type(GenericDeleteResponse, model_group, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_group_id` but received ''"):
            await async_client.model_groups.with_raw_response.delete(
                "",
            )
