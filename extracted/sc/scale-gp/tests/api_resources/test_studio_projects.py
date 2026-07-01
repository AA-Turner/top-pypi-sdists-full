# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import (
    StudioProject,
)
from scale_gp.pagination import SyncPageResponse, AsyncPageResponse
from scale_gp.types.shared import GenericDeleteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestStudioProjects:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        studio_project = client.studio_projects.create(
            account_id="account_id",
            description="description",
            name="name",
            studio_api_key="studio_api_key",
        )
        assert_matches_type(StudioProject, studio_project, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.studio_projects.with_raw_response.create(
            account_id="account_id",
            description="description",
            name="name",
            studio_api_key="studio_api_key",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        studio_project = response.parse()
        assert_matches_type(StudioProject, studio_project, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.studio_projects.with_streaming_response.create(
            account_id="account_id",
            description="description",
            name="name",
            studio_api_key="studio_api_key",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            studio_project = response.parse()
            assert_matches_type(StudioProject, studio_project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        studio_project = client.studio_projects.retrieve(
            "studio_project_id",
        )
        assert_matches_type(StudioProject, studio_project, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.studio_projects.with_raw_response.retrieve(
            "studio_project_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        studio_project = response.parse()
        assert_matches_type(StudioProject, studio_project, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.studio_projects.with_streaming_response.retrieve(
            "studio_project_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            studio_project = response.parse()
            assert_matches_type(StudioProject, studio_project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `studio_project_id` but received ''"):
            client.studio_projects.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        studio_project = client.studio_projects.update(
            studio_project_id="studio_project_id",
        )
        assert_matches_type(StudioProject, studio_project, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGPClient) -> None:
        studio_project = client.studio_projects.update(
            studio_project_id="studio_project_id",
            description="description",
            name="name",
            studio_api_key="studio_api_key",
        )
        assert_matches_type(StudioProject, studio_project, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.studio_projects.with_raw_response.update(
            studio_project_id="studio_project_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        studio_project = response.parse()
        assert_matches_type(StudioProject, studio_project, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.studio_projects.with_streaming_response.update(
            studio_project_id="studio_project_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            studio_project = response.parse()
            assert_matches_type(StudioProject, studio_project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `studio_project_id` but received ''"):
            client.studio_projects.with_raw_response.update(
                studio_project_id="",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        studio_project = client.studio_projects.list()
        assert_matches_type(SyncPageResponse[StudioProject], studio_project, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        studio_project = client.studio_projects.list(
            account_id="account_id",
            limit=1,
            page=1,
        )
        assert_matches_type(SyncPageResponse[StudioProject], studio_project, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.studio_projects.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        studio_project = response.parse()
        assert_matches_type(SyncPageResponse[StudioProject], studio_project, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.studio_projects.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            studio_project = response.parse()
            assert_matches_type(SyncPageResponse[StudioProject], studio_project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        studio_project = client.studio_projects.delete(
            "studio_project_id",
        )
        assert_matches_type(GenericDeleteResponse, studio_project, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.studio_projects.with_raw_response.delete(
            "studio_project_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        studio_project = response.parse()
        assert_matches_type(GenericDeleteResponse, studio_project, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.studio_projects.with_streaming_response.delete(
            "studio_project_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            studio_project = response.parse()
            assert_matches_type(GenericDeleteResponse, studio_project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `studio_project_id` but received ''"):
            client.studio_projects.with_raw_response.delete(
                "",
            )


class TestAsyncStudioProjects:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        studio_project = await async_client.studio_projects.create(
            account_id="account_id",
            description="description",
            name="name",
            studio_api_key="studio_api_key",
        )
        assert_matches_type(StudioProject, studio_project, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.studio_projects.with_raw_response.create(
            account_id="account_id",
            description="description",
            name="name",
            studio_api_key="studio_api_key",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        studio_project = await response.parse()
        assert_matches_type(StudioProject, studio_project, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.studio_projects.with_streaming_response.create(
            account_id="account_id",
            description="description",
            name="name",
            studio_api_key="studio_api_key",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            studio_project = await response.parse()
            assert_matches_type(StudioProject, studio_project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        studio_project = await async_client.studio_projects.retrieve(
            "studio_project_id",
        )
        assert_matches_type(StudioProject, studio_project, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.studio_projects.with_raw_response.retrieve(
            "studio_project_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        studio_project = await response.parse()
        assert_matches_type(StudioProject, studio_project, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.studio_projects.with_streaming_response.retrieve(
            "studio_project_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            studio_project = await response.parse()
            assert_matches_type(StudioProject, studio_project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `studio_project_id` but received ''"):
            await async_client.studio_projects.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        studio_project = await async_client.studio_projects.update(
            studio_project_id="studio_project_id",
        )
        assert_matches_type(StudioProject, studio_project, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        studio_project = await async_client.studio_projects.update(
            studio_project_id="studio_project_id",
            description="description",
            name="name",
            studio_api_key="studio_api_key",
        )
        assert_matches_type(StudioProject, studio_project, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.studio_projects.with_raw_response.update(
            studio_project_id="studio_project_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        studio_project = await response.parse()
        assert_matches_type(StudioProject, studio_project, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.studio_projects.with_streaming_response.update(
            studio_project_id="studio_project_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            studio_project = await response.parse()
            assert_matches_type(StudioProject, studio_project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `studio_project_id` but received ''"):
            await async_client.studio_projects.with_raw_response.update(
                studio_project_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        studio_project = await async_client.studio_projects.list()
        assert_matches_type(AsyncPageResponse[StudioProject], studio_project, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        studio_project = await async_client.studio_projects.list(
            account_id="account_id",
            limit=1,
            page=1,
        )
        assert_matches_type(AsyncPageResponse[StudioProject], studio_project, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.studio_projects.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        studio_project = await response.parse()
        assert_matches_type(AsyncPageResponse[StudioProject], studio_project, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.studio_projects.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            studio_project = await response.parse()
            assert_matches_type(AsyncPageResponse[StudioProject], studio_project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        studio_project = await async_client.studio_projects.delete(
            "studio_project_id",
        )
        assert_matches_type(GenericDeleteResponse, studio_project, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.studio_projects.with_raw_response.delete(
            "studio_project_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        studio_project = await response.parse()
        assert_matches_type(GenericDeleteResponse, studio_project, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.studio_projects.with_streaming_response.delete(
            "studio_project_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            studio_project = await response.parse()
            assert_matches_type(GenericDeleteResponse, studio_project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `studio_project_id` but received ''"):
            await async_client.studio_projects.with_raw_response.delete(
                "",
            )
