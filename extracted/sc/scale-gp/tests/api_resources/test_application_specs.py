# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import (
    ApplicationSpecCreateResponse,
    ApplicationSpecUpdateResponse,
    ApplicationSpecRetrieveResponse,
)
from scale_gp.pagination import SyncPageResponse, AsyncPageResponse
from scale_gp.types.shared import GenericDeleteResponse
from scale_gp.types.paginated_application_specs import Item

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestApplicationSpecs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        application_spec = client.application_specs.create(
            account_id="account_id",
            description="description",
            name="name",
        )
        assert_matches_type(ApplicationSpecCreateResponse, application_spec, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        application_spec = client.application_specs.create(
            account_id="account_id",
            description="description",
            name="name",
            run_online_evaluation=True,
            theme_id="theme_id",
        )
        assert_matches_type(ApplicationSpecCreateResponse, application_spec, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.application_specs.with_raw_response.create(
            account_id="account_id",
            description="description",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_spec = response.parse()
        assert_matches_type(ApplicationSpecCreateResponse, application_spec, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.application_specs.with_streaming_response.create(
            account_id="account_id",
            description="description",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_spec = response.parse()
            assert_matches_type(ApplicationSpecCreateResponse, application_spec, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        application_spec = client.application_specs.retrieve(
            "application_spec_id",
        )
        assert_matches_type(ApplicationSpecRetrieveResponse, application_spec, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.application_specs.with_raw_response.retrieve(
            "application_spec_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_spec = response.parse()
        assert_matches_type(ApplicationSpecRetrieveResponse, application_spec, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.application_specs.with_streaming_response.retrieve(
            "application_spec_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_spec = response.parse()
            assert_matches_type(ApplicationSpecRetrieveResponse, application_spec, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `application_spec_id` but received ''"):
            client.application_specs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update_overload_1(self, client: SGPClient) -> None:
        application_spec = client.application_specs.update(
            application_spec_id="application_spec_id",
        )
        assert_matches_type(ApplicationSpecUpdateResponse, application_spec, path=["response"])

    @parametrize
    def test_method_update_with_all_params_overload_1(self, client: SGPClient) -> None:
        application_spec = client.application_specs.update(
            application_spec_id="application_spec_id",
            description="description",
            name="name",
            restore=False,
            run_online_evaluation=True,
            theme_id="theme_id",
        )
        assert_matches_type(ApplicationSpecUpdateResponse, application_spec, path=["response"])

    @parametrize
    def test_raw_response_update_overload_1(self, client: SGPClient) -> None:
        response = client.application_specs.with_raw_response.update(
            application_spec_id="application_spec_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_spec = response.parse()
        assert_matches_type(ApplicationSpecUpdateResponse, application_spec, path=["response"])

    @parametrize
    def test_streaming_response_update_overload_1(self, client: SGPClient) -> None:
        with client.application_specs.with_streaming_response.update(
            application_spec_id="application_spec_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_spec = response.parse()
            assert_matches_type(ApplicationSpecUpdateResponse, application_spec, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update_overload_1(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `application_spec_id` but received ''"):
            client.application_specs.with_raw_response.update(
                application_spec_id="",
            )

    @parametrize
    def test_method_update_overload_2(self, client: SGPClient) -> None:
        application_spec = client.application_specs.update(
            application_spec_id="application_spec_id",
            restore=True,
        )
        assert_matches_type(ApplicationSpecUpdateResponse, application_spec, path=["response"])

    @parametrize
    def test_raw_response_update_overload_2(self, client: SGPClient) -> None:
        response = client.application_specs.with_raw_response.update(
            application_spec_id="application_spec_id",
            restore=True,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_spec = response.parse()
        assert_matches_type(ApplicationSpecUpdateResponse, application_spec, path=["response"])

    @parametrize
    def test_streaming_response_update_overload_2(self, client: SGPClient) -> None:
        with client.application_specs.with_streaming_response.update(
            application_spec_id="application_spec_id",
            restore=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_spec = response.parse()
            assert_matches_type(ApplicationSpecUpdateResponse, application_spec, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update_overload_2(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `application_spec_id` but received ''"):
            client.application_specs.with_raw_response.update(
                application_spec_id="",
                restore=True,
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        application_spec = client.application_specs.list()
        assert_matches_type(SyncPageResponse[Item], application_spec, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        application_spec = client.application_specs.list(
            account_id="account_id",
            include_archived=True,
            limit=1,
            page=1,
        )
        assert_matches_type(SyncPageResponse[Item], application_spec, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.application_specs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_spec = response.parse()
        assert_matches_type(SyncPageResponse[Item], application_spec, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.application_specs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_spec = response.parse()
            assert_matches_type(SyncPageResponse[Item], application_spec, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        application_spec = client.application_specs.delete(
            "application_spec_id",
        )
        assert_matches_type(GenericDeleteResponse, application_spec, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.application_specs.with_raw_response.delete(
            "application_spec_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_spec = response.parse()
        assert_matches_type(GenericDeleteResponse, application_spec, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.application_specs.with_streaming_response.delete(
            "application_spec_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_spec = response.parse()
            assert_matches_type(GenericDeleteResponse, application_spec, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `application_spec_id` but received ''"):
            client.application_specs.with_raw_response.delete(
                "",
            )


class TestAsyncApplicationSpecs:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        application_spec = await async_client.application_specs.create(
            account_id="account_id",
            description="description",
            name="name",
        )
        assert_matches_type(ApplicationSpecCreateResponse, application_spec, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        application_spec = await async_client.application_specs.create(
            account_id="account_id",
            description="description",
            name="name",
            run_online_evaluation=True,
            theme_id="theme_id",
        )
        assert_matches_type(ApplicationSpecCreateResponse, application_spec, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_specs.with_raw_response.create(
            account_id="account_id",
            description="description",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_spec = await response.parse()
        assert_matches_type(ApplicationSpecCreateResponse, application_spec, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_specs.with_streaming_response.create(
            account_id="account_id",
            description="description",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_spec = await response.parse()
            assert_matches_type(ApplicationSpecCreateResponse, application_spec, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        application_spec = await async_client.application_specs.retrieve(
            "application_spec_id",
        )
        assert_matches_type(ApplicationSpecRetrieveResponse, application_spec, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_specs.with_raw_response.retrieve(
            "application_spec_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_spec = await response.parse()
        assert_matches_type(ApplicationSpecRetrieveResponse, application_spec, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_specs.with_streaming_response.retrieve(
            "application_spec_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_spec = await response.parse()
            assert_matches_type(ApplicationSpecRetrieveResponse, application_spec, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `application_spec_id` but received ''"):
            await async_client.application_specs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update_overload_1(self, async_client: AsyncSGPClient) -> None:
        application_spec = await async_client.application_specs.update(
            application_spec_id="application_spec_id",
        )
        assert_matches_type(ApplicationSpecUpdateResponse, application_spec, path=["response"])

    @parametrize
    async def test_method_update_with_all_params_overload_1(self, async_client: AsyncSGPClient) -> None:
        application_spec = await async_client.application_specs.update(
            application_spec_id="application_spec_id",
            description="description",
            name="name",
            restore=False,
            run_online_evaluation=True,
            theme_id="theme_id",
        )
        assert_matches_type(ApplicationSpecUpdateResponse, application_spec, path=["response"])

    @parametrize
    async def test_raw_response_update_overload_1(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_specs.with_raw_response.update(
            application_spec_id="application_spec_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_spec = await response.parse()
        assert_matches_type(ApplicationSpecUpdateResponse, application_spec, path=["response"])

    @parametrize
    async def test_streaming_response_update_overload_1(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_specs.with_streaming_response.update(
            application_spec_id="application_spec_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_spec = await response.parse()
            assert_matches_type(ApplicationSpecUpdateResponse, application_spec, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update_overload_1(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `application_spec_id` but received ''"):
            await async_client.application_specs.with_raw_response.update(
                application_spec_id="",
            )

    @parametrize
    async def test_method_update_overload_2(self, async_client: AsyncSGPClient) -> None:
        application_spec = await async_client.application_specs.update(
            application_spec_id="application_spec_id",
            restore=True,
        )
        assert_matches_type(ApplicationSpecUpdateResponse, application_spec, path=["response"])

    @parametrize
    async def test_raw_response_update_overload_2(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_specs.with_raw_response.update(
            application_spec_id="application_spec_id",
            restore=True,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_spec = await response.parse()
        assert_matches_type(ApplicationSpecUpdateResponse, application_spec, path=["response"])

    @parametrize
    async def test_streaming_response_update_overload_2(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_specs.with_streaming_response.update(
            application_spec_id="application_spec_id",
            restore=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_spec = await response.parse()
            assert_matches_type(ApplicationSpecUpdateResponse, application_spec, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update_overload_2(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `application_spec_id` but received ''"):
            await async_client.application_specs.with_raw_response.update(
                application_spec_id="",
                restore=True,
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        application_spec = await async_client.application_specs.list()
        assert_matches_type(AsyncPageResponse[Item], application_spec, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        application_spec = await async_client.application_specs.list(
            account_id="account_id",
            include_archived=True,
            limit=1,
            page=1,
        )
        assert_matches_type(AsyncPageResponse[Item], application_spec, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_specs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_spec = await response.parse()
        assert_matches_type(AsyncPageResponse[Item], application_spec, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_specs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_spec = await response.parse()
            assert_matches_type(AsyncPageResponse[Item], application_spec, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        application_spec = await async_client.application_specs.delete(
            "application_spec_id",
        )
        assert_matches_type(GenericDeleteResponse, application_spec, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_specs.with_raw_response.delete(
            "application_spec_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_spec = await response.parse()
        assert_matches_type(GenericDeleteResponse, application_spec, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_specs.with_streaming_response.delete(
            "application_spec_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_spec = await response.parse()
            assert_matches_type(GenericDeleteResponse, application_spec, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `application_spec_id` but received ''"):
            await async_client.application_specs.with_raw_response.delete(
                "",
            )
