# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from patronus_api import PatronusAPI, AsyncPatronusAPI
from patronus_api.types import (
    Project,
    ProjectListResponse,
    ProjectRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestProjects:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: PatronusAPI) -> None:
        project = client.projects.create(
            name="name",
        )
        assert_matches_type(Project, project, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: PatronusAPI) -> None:
        response = client.projects.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = response.parse()
        assert_matches_type(Project, project, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: PatronusAPI) -> None:
        with client.projects.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = response.parse()
            assert_matches_type(Project, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: PatronusAPI) -> None:
        project = client.projects.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ProjectRetrieveResponse, project, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: PatronusAPI) -> None:
        response = client.projects.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = response.parse()
        assert_matches_type(ProjectRetrieveResponse, project, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: PatronusAPI) -> None:
        with client.projects.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = response.parse()
            assert_matches_type(ProjectRetrieveResponse, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: PatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.projects.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: PatronusAPI) -> None:
        project = client.projects.list()
        assert_matches_type(ProjectListResponse, project, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: PatronusAPI) -> None:
        project = client.projects.list(
            limit=1,
            offset=0,
        )
        assert_matches_type(ProjectListResponse, project, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: PatronusAPI) -> None:
        response = client.projects.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = response.parse()
        assert_matches_type(ProjectListResponse, project, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: PatronusAPI) -> None:
        with client.projects.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = response.parse()
            assert_matches_type(ProjectListResponse, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: PatronusAPI) -> None:
        project = client.projects.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert project is None

    @parametrize
    def test_raw_response_delete(self, client: PatronusAPI) -> None:
        response = client.projects.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = response.parse()
        assert project is None

    @parametrize
    def test_streaming_response_delete(self, client: PatronusAPI) -> None:
        with client.projects.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = response.parse()
            assert project is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: PatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.projects.with_raw_response.delete(
                "",
            )


class TestAsyncProjects:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncPatronusAPI) -> None:
        project = await async_client.projects.create(
            name="name",
        )
        assert_matches_type(Project, project, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.projects.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = await response.parse()
        assert_matches_type(Project, project, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.projects.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = await response.parse()
            assert_matches_type(Project, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncPatronusAPI) -> None:
        project = await async_client.projects.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ProjectRetrieveResponse, project, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.projects.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = await response.parse()
        assert_matches_type(ProjectRetrieveResponse, project, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.projects.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = await response.parse()
            assert_matches_type(ProjectRetrieveResponse, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncPatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.projects.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncPatronusAPI) -> None:
        project = await async_client.projects.list()
        assert_matches_type(ProjectListResponse, project, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        project = await async_client.projects.list(
            limit=1,
            offset=0,
        )
        assert_matches_type(ProjectListResponse, project, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.projects.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = await response.parse()
        assert_matches_type(ProjectListResponse, project, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.projects.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = await response.parse()
            assert_matches_type(ProjectListResponse, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncPatronusAPI) -> None:
        project = await async_client.projects.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert project is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.projects.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = await response.parse()
        assert project is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.projects.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = await response.parse()
            assert project is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncPatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.projects.with_raw_response.delete(
                "",
            )
