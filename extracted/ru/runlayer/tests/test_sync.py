import datetime
from unittest.mock import MagicMock

import mcp.types as mt
import pytest

from runlayer_cli.sync import sync_local_capabilities


class DummyTool:
    def to_mcp_tool(self, include_fastmcp_meta: bool = True) -> mt.Tool:
        return mt.Tool(
            name="XcodeListWindows",
            description="List Xcode windows",
            inputSchema={"type": "object", "properties": {}},
        )


class DummyResource:
    def to_mcp_resource(self, include_fastmcp_meta: bool = True) -> mt.Resource:
        return mt.Resource(
            name="project",
            uri="file:///project",
        )


class DummyPrompt:
    def to_mcp_prompt(self, include_fastmcp_meta: bool = True) -> mt.Prompt:
        return mt.Prompt(name="prompt")


class ProxyWithResourceFailure:
    async def get_tools(self) -> dict[str, DummyTool]:
        return {"XcodeListWindows": DummyTool()}

    async def get_resources(self) -> dict[str, DummyResource]:
        raise ValueError("invalid resources/list response")

    async def get_prompts(self) -> dict[str, DummyPrompt]:
        return {}


class ProxyWithPromptFailure:
    async def get_tools(self) -> dict[str, DummyTool]:
        return {"XcodeListWindows": DummyTool()}

    async def get_resources(self) -> dict[str, DummyResource]:
        return {}

    async def get_prompts(self) -> dict[str, DummyPrompt]:
        raise ValueError("invalid prompts/list response")


@pytest.mark.asyncio
async def test_sync_local_capabilities_uploads_tools_when_resources_fail():
    client = MagicMock()

    await sync_local_capabilities(
        client, ProxyWithResourceFailure(), "server-123", server_version=7
    )

    client.update_capabilities.assert_called_once()
    _, capabilities = client.update_capabilities.call_args.args
    assert client.update_capabilities.call_args.kwargs == {"server_version": 7}
    assert list(capabilities.tools) == ["XcodeListWindows"]
    assert capabilities.resources == {}
    assert capabilities.prompts == {}
    assert isinstance(capabilities.synced_at, datetime.datetime)


@pytest.mark.asyncio
async def test_sync_local_capabilities_uploads_tools_when_prompts_fail():
    client = MagicMock()

    await sync_local_capabilities(
        client, ProxyWithPromptFailure(), "server-123", server_version=7
    )

    client.update_capabilities.assert_called_once()
    _, capabilities = client.update_capabilities.call_args.args
    assert client.update_capabilities.call_args.kwargs == {"server_version": 7}
    assert list(capabilities.tools) == ["XcodeListWindows"]
    assert capabilities.resources == {}
    assert capabilities.prompts == {}
