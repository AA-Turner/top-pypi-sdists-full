# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from scale_gp_beta import SGPClient, AsyncSGPClient
from scale_gp_beta.types import (
    AgentexCloudDeploy,
    DeployLogsResponse,
)
from scale_gp_beta._utils import parse_datetime
from scale_gp_beta.pagination import SyncCursorPage, AsyncCursorPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDeploy:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        deploy = client.deploy.create(
            environment_config="environment_config",
            manifest_file="manifest_file",
        )
        assert_matches_type(AgentexCloudDeploy, deploy, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        deploy = client.deploy.create(
            environment_config="environment_config",
            manifest_file="manifest_file",
            build_id="build_id",
            expires_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            image_name="image_name",
            image_tag="image_tag",
            preview=True,
            preview_label="preview_label",
        )
        assert_matches_type(AgentexCloudDeploy, deploy, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.deploy.with_raw_response.create(
            environment_config="environment_config",
            manifest_file="manifest_file",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deploy = response.parse()
        assert_matches_type(AgentexCloudDeploy, deploy, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.deploy.with_streaming_response.create(
            environment_config="environment_config",
            manifest_file="manifest_file",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deploy = response.parse()
            assert_matches_type(AgentexCloudDeploy, deploy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        deploy = client.deploy.retrieve(
            "deployment_id",
        )
        assert_matches_type(AgentexCloudDeploy, deploy, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.deploy.with_raw_response.retrieve(
            "deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deploy = response.parse()
        assert_matches_type(AgentexCloudDeploy, deploy, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.deploy.with_streaming_response.retrieve(
            "deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deploy = response.parse()
            assert_matches_type(AgentexCloudDeploy, deploy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.deploy.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        deploy = client.deploy.list()
        assert_matches_type(SyncCursorPage[AgentexCloudDeploy], deploy, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        deploy = client.deploy.list(
            agent_name="agent_name",
            build_id="build_id",
            ending_before="ending_before",
            limit=1,
            preview_label="preview_label",
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
        )
        assert_matches_type(SyncCursorPage[AgentexCloudDeploy], deploy, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.deploy.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deploy = response.parse()
        assert_matches_type(SyncCursorPage[AgentexCloudDeploy], deploy, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.deploy.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deploy = response.parse()
            assert_matches_type(SyncCursorPage[AgentexCloudDeploy], deploy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        deploy = client.deploy.delete(
            "deployment_id",
        )
        assert_matches_type(AgentexCloudDeploy, deploy, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.deploy.with_raw_response.delete(
            "deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deploy = response.parse()
        assert_matches_type(AgentexCloudDeploy, deploy, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.deploy.with_streaming_response.delete(
            "deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deploy = response.parse()
            assert_matches_type(AgentexCloudDeploy, deploy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.deploy.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_logs(self, client: SGPClient) -> None:
        deploy = client.deploy.logs(
            deployment_id="deployment_id",
        )
        assert_matches_type(DeployLogsResponse, deploy, path=["response"])

    @parametrize
    def test_method_logs_with_all_params(self, client: SGPClient) -> None:
        deploy = client.deploy.logs(
            deployment_id="deployment_id",
            cursor="cursor",
            limit=1,
        )
        assert_matches_type(DeployLogsResponse, deploy, path=["response"])

    @parametrize
    def test_raw_response_logs(self, client: SGPClient) -> None:
        response = client.deploy.with_raw_response.logs(
            deployment_id="deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deploy = response.parse()
        assert_matches_type(DeployLogsResponse, deploy, path=["response"])

    @parametrize
    def test_streaming_response_logs(self, client: SGPClient) -> None:
        with client.deploy.with_streaming_response.logs(
            deployment_id="deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deploy = response.parse()
            assert_matches_type(DeployLogsResponse, deploy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_logs(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.deploy.with_raw_response.logs(
                deployment_id="",
            )


class TestAsyncDeploy:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        deploy = await async_client.deploy.create(
            environment_config="environment_config",
            manifest_file="manifest_file",
        )
        assert_matches_type(AgentexCloudDeploy, deploy, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        deploy = await async_client.deploy.create(
            environment_config="environment_config",
            manifest_file="manifest_file",
            build_id="build_id",
            expires_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            image_name="image_name",
            image_tag="image_tag",
            preview=True,
            preview_label="preview_label",
        )
        assert_matches_type(AgentexCloudDeploy, deploy, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.deploy.with_raw_response.create(
            environment_config="environment_config",
            manifest_file="manifest_file",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deploy = await response.parse()
        assert_matches_type(AgentexCloudDeploy, deploy, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.deploy.with_streaming_response.create(
            environment_config="environment_config",
            manifest_file="manifest_file",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deploy = await response.parse()
            assert_matches_type(AgentexCloudDeploy, deploy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        deploy = await async_client.deploy.retrieve(
            "deployment_id",
        )
        assert_matches_type(AgentexCloudDeploy, deploy, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.deploy.with_raw_response.retrieve(
            "deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deploy = await response.parse()
        assert_matches_type(AgentexCloudDeploy, deploy, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.deploy.with_streaming_response.retrieve(
            "deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deploy = await response.parse()
            assert_matches_type(AgentexCloudDeploy, deploy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.deploy.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        deploy = await async_client.deploy.list()
        assert_matches_type(AsyncCursorPage[AgentexCloudDeploy], deploy, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        deploy = await async_client.deploy.list(
            agent_name="agent_name",
            build_id="build_id",
            ending_before="ending_before",
            limit=1,
            preview_label="preview_label",
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
        )
        assert_matches_type(AsyncCursorPage[AgentexCloudDeploy], deploy, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.deploy.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deploy = await response.parse()
        assert_matches_type(AsyncCursorPage[AgentexCloudDeploy], deploy, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.deploy.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deploy = await response.parse()
            assert_matches_type(AsyncCursorPage[AgentexCloudDeploy], deploy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        deploy = await async_client.deploy.delete(
            "deployment_id",
        )
        assert_matches_type(AgentexCloudDeploy, deploy, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.deploy.with_raw_response.delete(
            "deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deploy = await response.parse()
        assert_matches_type(AgentexCloudDeploy, deploy, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.deploy.with_streaming_response.delete(
            "deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deploy = await response.parse()
            assert_matches_type(AgentexCloudDeploy, deploy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.deploy.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_logs(self, async_client: AsyncSGPClient) -> None:
        deploy = await async_client.deploy.logs(
            deployment_id="deployment_id",
        )
        assert_matches_type(DeployLogsResponse, deploy, path=["response"])

    @parametrize
    async def test_method_logs_with_all_params(self, async_client: AsyncSGPClient) -> None:
        deploy = await async_client.deploy.logs(
            deployment_id="deployment_id",
            cursor="cursor",
            limit=1,
        )
        assert_matches_type(DeployLogsResponse, deploy, path=["response"])

    @parametrize
    async def test_raw_response_logs(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.deploy.with_raw_response.logs(
            deployment_id="deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deploy = await response.parse()
        assert_matches_type(DeployLogsResponse, deploy, path=["response"])

    @parametrize
    async def test_streaming_response_logs(self, async_client: AsyncSGPClient) -> None:
        async with async_client.deploy.with_streaming_response.logs(
            deployment_id="deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deploy = await response.parse()
            assert_matches_type(DeployLogsResponse, deploy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_logs(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.deploy.with_raw_response.logs(
                deployment_id="",
            )
