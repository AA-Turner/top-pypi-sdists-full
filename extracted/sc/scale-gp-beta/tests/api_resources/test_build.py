# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from scale_gp_beta import SGPClient, AsyncSGPClient
from scale_gp_beta.types import AgentexCloudBuild, BuildListUndeployedResponse
from scale_gp_beta.pagination import SyncCursorPage, AsyncCursorPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBuild:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        build = client.build.create(
            agent_name="agent_name",
            context_archive=b"Example data",
            image_name="image_name",
        )
        assert_matches_type(AgentexCloudBuild, build, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        build = client.build.create(
            agent_name="agent_name",
            context_archive=b"Example data",
            image_name="image_name",
            build_args="build_args",
            image_tag="image_tag",
        )
        assert_matches_type(AgentexCloudBuild, build, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.build.with_raw_response.create(
            agent_name="agent_name",
            context_archive=b"Example data",
            image_name="image_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        build = response.parse()
        assert_matches_type(AgentexCloudBuild, build, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.build.with_streaming_response.create(
            agent_name="agent_name",
            context_archive=b"Example data",
            image_name="image_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            build = response.parse()
            assert_matches_type(AgentexCloudBuild, build, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        build = client.build.retrieve(
            "build_id",
        )
        assert_matches_type(AgentexCloudBuild, build, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.build.with_raw_response.retrieve(
            "build_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        build = response.parse()
        assert_matches_type(AgentexCloudBuild, build, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.build.with_streaming_response.retrieve(
            "build_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            build = response.parse()
            assert_matches_type(AgentexCloudBuild, build, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `build_id` but received ''"):
            client.build.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        build = client.build.list()
        assert_matches_type(SyncCursorPage[AgentexCloudBuild], build, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        build = client.build.list(
            agent_name="agent_name",
            ending_before="ending_before",
            limit=1,
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
        )
        assert_matches_type(SyncCursorPage[AgentexCloudBuild], build, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.build.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        build = response.parse()
        assert_matches_type(SyncCursorPage[AgentexCloudBuild], build, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.build.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            build = response.parse()
            assert_matches_type(SyncCursorPage[AgentexCloudBuild], build, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_cancel(self, client: SGPClient) -> None:
        build = client.build.cancel(
            "build_id",
        )
        assert_matches_type(AgentexCloudBuild, build, path=["response"])

    @parametrize
    def test_raw_response_cancel(self, client: SGPClient) -> None:
        response = client.build.with_raw_response.cancel(
            "build_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        build = response.parse()
        assert_matches_type(AgentexCloudBuild, build, path=["response"])

    @parametrize
    def test_streaming_response_cancel(self, client: SGPClient) -> None:
        with client.build.with_streaming_response.cancel(
            "build_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            build = response.parse()
            assert_matches_type(AgentexCloudBuild, build, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_cancel(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `build_id` but received ''"):
            client.build.with_raw_response.cancel(
                "",
            )

    @parametrize
    def test_method_list_undeployed(self, client: SGPClient) -> None:
        build = client.build.list_undeployed()
        assert_matches_type(BuildListUndeployedResponse, build, path=["response"])

    @parametrize
    def test_raw_response_list_undeployed(self, client: SGPClient) -> None:
        response = client.build.with_raw_response.list_undeployed()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        build = response.parse()
        assert_matches_type(BuildListUndeployedResponse, build, path=["response"])

    @parametrize
    def test_streaming_response_list_undeployed(self, client: SGPClient) -> None:
        with client.build.with_streaming_response.list_undeployed() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            build = response.parse()
            assert_matches_type(BuildListUndeployedResponse, build, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_logs(self, client: SGPClient) -> None:
        build_stream = client.build.logs(
            "build_id",
        )
        build_stream.response.close()

    @parametrize
    def test_raw_response_logs(self, client: SGPClient) -> None:
        response = client.build.with_raw_response.logs(
            "build_id",
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = response.parse()
        stream.close()

    @parametrize
    def test_streaming_response_logs(self, client: SGPClient) -> None:
        with client.build.with_streaming_response.logs(
            "build_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = response.parse()
            stream.close()

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_logs(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `build_id` but received ''"):
            client.build.with_raw_response.logs(
                "",
            )


class TestAsyncBuild:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        build = await async_client.build.create(
            agent_name="agent_name",
            context_archive=b"Example data",
            image_name="image_name",
        )
        assert_matches_type(AgentexCloudBuild, build, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        build = await async_client.build.create(
            agent_name="agent_name",
            context_archive=b"Example data",
            image_name="image_name",
            build_args="build_args",
            image_tag="image_tag",
        )
        assert_matches_type(AgentexCloudBuild, build, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.build.with_raw_response.create(
            agent_name="agent_name",
            context_archive=b"Example data",
            image_name="image_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        build = await response.parse()
        assert_matches_type(AgentexCloudBuild, build, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.build.with_streaming_response.create(
            agent_name="agent_name",
            context_archive=b"Example data",
            image_name="image_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            build = await response.parse()
            assert_matches_type(AgentexCloudBuild, build, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        build = await async_client.build.retrieve(
            "build_id",
        )
        assert_matches_type(AgentexCloudBuild, build, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.build.with_raw_response.retrieve(
            "build_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        build = await response.parse()
        assert_matches_type(AgentexCloudBuild, build, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.build.with_streaming_response.retrieve(
            "build_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            build = await response.parse()
            assert_matches_type(AgentexCloudBuild, build, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `build_id` but received ''"):
            await async_client.build.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        build = await async_client.build.list()
        assert_matches_type(AsyncCursorPage[AgentexCloudBuild], build, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        build = await async_client.build.list(
            agent_name="agent_name",
            ending_before="ending_before",
            limit=1,
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
        )
        assert_matches_type(AsyncCursorPage[AgentexCloudBuild], build, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.build.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        build = await response.parse()
        assert_matches_type(AsyncCursorPage[AgentexCloudBuild], build, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.build.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            build = await response.parse()
            assert_matches_type(AsyncCursorPage[AgentexCloudBuild], build, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_cancel(self, async_client: AsyncSGPClient) -> None:
        build = await async_client.build.cancel(
            "build_id",
        )
        assert_matches_type(AgentexCloudBuild, build, path=["response"])

    @parametrize
    async def test_raw_response_cancel(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.build.with_raw_response.cancel(
            "build_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        build = await response.parse()
        assert_matches_type(AgentexCloudBuild, build, path=["response"])

    @parametrize
    async def test_streaming_response_cancel(self, async_client: AsyncSGPClient) -> None:
        async with async_client.build.with_streaming_response.cancel(
            "build_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            build = await response.parse()
            assert_matches_type(AgentexCloudBuild, build, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_cancel(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `build_id` but received ''"):
            await async_client.build.with_raw_response.cancel(
                "",
            )

    @parametrize
    async def test_method_list_undeployed(self, async_client: AsyncSGPClient) -> None:
        build = await async_client.build.list_undeployed()
        assert_matches_type(BuildListUndeployedResponse, build, path=["response"])

    @parametrize
    async def test_raw_response_list_undeployed(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.build.with_raw_response.list_undeployed()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        build = await response.parse()
        assert_matches_type(BuildListUndeployedResponse, build, path=["response"])

    @parametrize
    async def test_streaming_response_list_undeployed(self, async_client: AsyncSGPClient) -> None:
        async with async_client.build.with_streaming_response.list_undeployed() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            build = await response.parse()
            assert_matches_type(BuildListUndeployedResponse, build, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_logs(self, async_client: AsyncSGPClient) -> None:
        build_stream = await async_client.build.logs(
            "build_id",
        )
        await build_stream.response.aclose()

    @parametrize
    async def test_raw_response_logs(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.build.with_raw_response.logs(
            "build_id",
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = await response.parse()
        await stream.close()

    @parametrize
    async def test_streaming_response_logs(self, async_client: AsyncSGPClient) -> None:
        async with async_client.build.with_streaming_response.logs(
            "build_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = await response.parse()
            await stream.close()

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_logs(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `build_id` but received ''"):
            await async_client.build.with_raw_response.logs(
                "",
            )
