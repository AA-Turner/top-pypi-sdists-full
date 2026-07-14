# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from scale_gp_beta import SGPClient, AsyncSGPClient
from scale_gp_beta.types import (
    AgentConfigListResponse,
    AgentConfigCreateResponse,
    AgentConfigDeleteResponse,
    AgentConfigUpdateResponse,
    AgentConfigRetrieveResponse,
    AgentConfigListMcpToolsResponse,
)
from scale_gp_beta.pagination import SyncCursorPage, AsyncCursorPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAgentConfigs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        agent_config = client.agent_configs.create(
            harness="claude-code",
            model="x",
            name="x",
            system_prompt="x",
        )
        assert_matches_type(AgentConfigCreateResponse, agent_config, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        agent_config = client.agent_configs.create(
            harness="claude-code",
            model="x",
            name="x",
            system_prompt="x",
            allowed_tools=["Read"],
            description="description",
        )
        assert_matches_type(AgentConfigCreateResponse, agent_config, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.agent_configs.with_raw_response.create(
            harness="claude-code",
            model="x",
            name="x",
            system_prompt="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent_config = response.parse()
        assert_matches_type(AgentConfigCreateResponse, agent_config, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.agent_configs.with_streaming_response.create(
            harness="claude-code",
            model="x",
            name="x",
            system_prompt="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent_config = response.parse()
            assert_matches_type(AgentConfigCreateResponse, agent_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        agent_config = client.agent_configs.retrieve(
            "agent_config_id",
        )
        assert_matches_type(AgentConfigRetrieveResponse, agent_config, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.agent_configs.with_raw_response.retrieve(
            "agent_config_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent_config = response.parse()
        assert_matches_type(AgentConfigRetrieveResponse, agent_config, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.agent_configs.with_streaming_response.retrieve(
            "agent_config_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent_config = response.parse()
            assert_matches_type(AgentConfigRetrieveResponse, agent_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_config_id` but received ''"):
            client.agent_configs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        agent_config = client.agent_configs.update(
            agent_config_id="agent_config_id",
        )
        assert_matches_type(AgentConfigUpdateResponse, agent_config, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SGPClient) -> None:
        agent_config = client.agent_configs.update(
            agent_config_id="agent_config_id",
            task_id="task_id",
            allowed_tools=["Read"],
            description="description",
            harness="claude-code",
            model="x",
            name="x",
            system_prompt="x",
        )
        assert_matches_type(AgentConfigUpdateResponse, agent_config, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.agent_configs.with_raw_response.update(
            agent_config_id="agent_config_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent_config = response.parse()
        assert_matches_type(AgentConfigUpdateResponse, agent_config, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.agent_configs.with_streaming_response.update(
            agent_config_id="agent_config_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent_config = response.parse()
            assert_matches_type(AgentConfigUpdateResponse, agent_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_config_id` but received ''"):
            client.agent_configs.with_raw_response.update(
                agent_config_id="",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        agent_config = client.agent_configs.list()
        assert_matches_type(SyncCursorPage[AgentConfigListResponse], agent_config, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        agent_config = client.agent_configs.list(
            ending_before="ending_before",
            limit=1,
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
        )
        assert_matches_type(SyncCursorPage[AgentConfigListResponse], agent_config, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.agent_configs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent_config = response.parse()
        assert_matches_type(SyncCursorPage[AgentConfigListResponse], agent_config, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.agent_configs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent_config = response.parse()
            assert_matches_type(SyncCursorPage[AgentConfigListResponse], agent_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        agent_config = client.agent_configs.delete(
            "agent_config_id",
        )
        assert_matches_type(AgentConfigDeleteResponse, agent_config, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.agent_configs.with_raw_response.delete(
            "agent_config_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent_config = response.parse()
        assert_matches_type(AgentConfigDeleteResponse, agent_config, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.agent_configs.with_streaming_response.delete(
            "agent_config_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent_config = response.parse()
            assert_matches_type(AgentConfigDeleteResponse, agent_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_config_id` but received ''"):
            client.agent_configs.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_list_mcp_tools(self, client: SGPClient) -> None:
        agent_config = client.agent_configs.list_mcp_tools()
        assert_matches_type(AgentConfigListMcpToolsResponse, agent_config, path=["response"])

    @parametrize
    def test_raw_response_list_mcp_tools(self, client: SGPClient) -> None:
        response = client.agent_configs.with_raw_response.list_mcp_tools()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent_config = response.parse()
        assert_matches_type(AgentConfigListMcpToolsResponse, agent_config, path=["response"])

    @parametrize
    def test_streaming_response_list_mcp_tools(self, client: SGPClient) -> None:
        with client.agent_configs.with_streaming_response.list_mcp_tools() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent_config = response.parse()
            assert_matches_type(AgentConfigListMcpToolsResponse, agent_config, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAgentConfigs:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        agent_config = await async_client.agent_configs.create(
            harness="claude-code",
            model="x",
            name="x",
            system_prompt="x",
        )
        assert_matches_type(AgentConfigCreateResponse, agent_config, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        agent_config = await async_client.agent_configs.create(
            harness="claude-code",
            model="x",
            name="x",
            system_prompt="x",
            allowed_tools=["Read"],
            description="description",
        )
        assert_matches_type(AgentConfigCreateResponse, agent_config, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.agent_configs.with_raw_response.create(
            harness="claude-code",
            model="x",
            name="x",
            system_prompt="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent_config = await response.parse()
        assert_matches_type(AgentConfigCreateResponse, agent_config, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.agent_configs.with_streaming_response.create(
            harness="claude-code",
            model="x",
            name="x",
            system_prompt="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent_config = await response.parse()
            assert_matches_type(AgentConfigCreateResponse, agent_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        agent_config = await async_client.agent_configs.retrieve(
            "agent_config_id",
        )
        assert_matches_type(AgentConfigRetrieveResponse, agent_config, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.agent_configs.with_raw_response.retrieve(
            "agent_config_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent_config = await response.parse()
        assert_matches_type(AgentConfigRetrieveResponse, agent_config, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.agent_configs.with_streaming_response.retrieve(
            "agent_config_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent_config = await response.parse()
            assert_matches_type(AgentConfigRetrieveResponse, agent_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_config_id` but received ''"):
            await async_client.agent_configs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        agent_config = await async_client.agent_configs.update(
            agent_config_id="agent_config_id",
        )
        assert_matches_type(AgentConfigUpdateResponse, agent_config, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSGPClient) -> None:
        agent_config = await async_client.agent_configs.update(
            agent_config_id="agent_config_id",
            task_id="task_id",
            allowed_tools=["Read"],
            description="description",
            harness="claude-code",
            model="x",
            name="x",
            system_prompt="x",
        )
        assert_matches_type(AgentConfigUpdateResponse, agent_config, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.agent_configs.with_raw_response.update(
            agent_config_id="agent_config_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent_config = await response.parse()
        assert_matches_type(AgentConfigUpdateResponse, agent_config, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.agent_configs.with_streaming_response.update(
            agent_config_id="agent_config_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent_config = await response.parse()
            assert_matches_type(AgentConfigUpdateResponse, agent_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_config_id` but received ''"):
            await async_client.agent_configs.with_raw_response.update(
                agent_config_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        agent_config = await async_client.agent_configs.list()
        assert_matches_type(AsyncCursorPage[AgentConfigListResponse], agent_config, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        agent_config = await async_client.agent_configs.list(
            ending_before="ending_before",
            limit=1,
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
        )
        assert_matches_type(AsyncCursorPage[AgentConfigListResponse], agent_config, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.agent_configs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent_config = await response.parse()
        assert_matches_type(AsyncCursorPage[AgentConfigListResponse], agent_config, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.agent_configs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent_config = await response.parse()
            assert_matches_type(AsyncCursorPage[AgentConfigListResponse], agent_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        agent_config = await async_client.agent_configs.delete(
            "agent_config_id",
        )
        assert_matches_type(AgentConfigDeleteResponse, agent_config, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.agent_configs.with_raw_response.delete(
            "agent_config_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent_config = await response.parse()
        assert_matches_type(AgentConfigDeleteResponse, agent_config, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.agent_configs.with_streaming_response.delete(
            "agent_config_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent_config = await response.parse()
            assert_matches_type(AgentConfigDeleteResponse, agent_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_config_id` but received ''"):
            await async_client.agent_configs.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_list_mcp_tools(self, async_client: AsyncSGPClient) -> None:
        agent_config = await async_client.agent_configs.list_mcp_tools()
        assert_matches_type(AgentConfigListMcpToolsResponse, agent_config, path=["response"])

    @parametrize
    async def test_raw_response_list_mcp_tools(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.agent_configs.with_raw_response.list_mcp_tools()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent_config = await response.parse()
        assert_matches_type(AgentConfigListMcpToolsResponse, agent_config, path=["response"])

    @parametrize
    async def test_streaming_response_list_mcp_tools(self, async_client: AsyncSGPClient) -> None:
        async with async_client.agent_configs.with_streaming_response.list_mcp_tools() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent_config = await response.parse()
            assert_matches_type(AgentConfigListMcpToolsResponse, agent_config, path=["response"])

        assert cast(Any, response.is_closed) is True
