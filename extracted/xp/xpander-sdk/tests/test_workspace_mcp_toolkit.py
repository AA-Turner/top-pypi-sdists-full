"""Local MCP servers reached through the agent's workspace bridge."""

from typing import Any, Dict, List

import pytest

from xpander_sdk.modules.backend.utils import workspace_mcp
from xpander_sdk.modules.backend.utils.workspace_mcp import WorkspaceMCPTools
from xpander_sdk.modules.tools_repository.sub_modules.mcp_tool_proxy import (
    build_mcp_proxies,
)

pytestmark = pytest.mark.asyncio

LIST_RESPONSE = {
    "server_key": "abc123",
    "tools": [
        {
            "name": "echo",
            "description": "echo text back",
            "input_schema": {
                "type": "object",
                "properties": {"text": {"type": "string"}},
            },
        },
        {"name": "read_token", "description": "", "input_schema": {"type": "object"}},
    ],
}


class _FakeClient:
    """Records bridge calls and replays canned responses."""

    def __init__(self, responses: Dict[str, Any]):
        self.responses = responses
        self.calls: List[Dict[str, Any]] = []

    async def make_request(
        self, path: str, method: str = "GET", payload: Any = None, **_: Any
    ):
        self.calls.append({"path": path, "method": method, "payload": payload})
        tool_name = path.rsplit("/", 1)[-1]
        response = self.responses[tool_name]
        if isinstance(response, Exception):
            raise response
        return response


@pytest.fixture
def bridge(monkeypatch):
    client = _FakeClient(
        {
            "mcp_list_tools": LIST_RESPONSE,
            "mcp_call_tool": {"content": "echo:hi", "is_error": False},
        }
    )
    monkeypatch.setattr(workspace_mcp, "APIClient", lambda configuration=None: client)
    return client


def _toolkit(**kwargs) -> WorkspaceMCPTools:
    return WorkspaceMCPTools(
        agent_id="agent-1", command="npx -y some-mcp", server_name="Some MCP", **kwargs
    )


async def test_connect_registers_one_function_per_tool(bridge):
    toolkit = _toolkit()
    await toolkit.connect()

    assert toolkit.initialized is True
    assert set(toolkit.functions) == {"mcp_tool_echo", "mcp_tool_read_token"}
    echo = toolkit.functions["mcp_tool_echo"]
    assert echo.description == "echo text back"
    assert echo.parameters == LIST_RESPONSE["tools"][0]["input_schema"]


async def test_connect_targets_the_agents_workspace_bridge(bridge):
    await _toolkit().connect()

    call = bridge.calls[0]
    assert call["path"] == "/workspace/agent-1/tools/mcp_list_tools"
    assert call["method"] == "POST"
    assert call["payload"]["command"] == "npx -y some-mcp"


async def test_connect_is_idempotent(bridge):
    toolkit = _toolkit()
    await toolkit.connect()
    await toolkit.connect()
    assert len(bridge.calls) == 1


async def test_allowed_tools_filters_the_registered_set(bridge):
    toolkit = _toolkit(include_tools=["echo"])
    await toolkit.connect()
    assert set(toolkit.functions) == {"mcp_tool_echo"}


async def test_calling_a_tool_posts_to_the_bridge(bridge):
    toolkit = _toolkit()
    await toolkit.connect()

    result = await toolkit.functions["mcp_tool_echo"].entrypoint(text="hi")

    assert result.content == "echo:hi"
    call = bridge.calls[-1]
    assert call["path"] == "/workspace/agent-1/tools/mcp_call_tool"
    assert call["payload"]["tool"] == "echo"
    assert call["payload"]["arguments"] == {"text": "hi"}


async def test_agno_context_kwargs_are_not_sent_as_tool_arguments(bridge):
    toolkit = _toolkit()
    await toolkit.connect()

    await toolkit.functions["mcp_tool_echo"].entrypoint(
        text="hi", run_context=object(), agent=object()
    )

    assert bridge.calls[-1]["payload"]["arguments"] == {"text": "hi"}


async def test_env_var_references_are_forwarded_verbatim(bridge):
    """Expansion happens in the workspace, so no secret value passes through the SDK."""
    toolkit = _toolkit(env_vars={"API_KEY": "${MY_SECRET}"})
    await toolkit.connect()
    await toolkit.functions["mcp_tool_echo"].entrypoint(text="hi")

    for call in bridge.calls:
        assert call["payload"]["env_vars"] == {"API_KEY": "${MY_SECRET}"}


async def test_a_failing_call_is_reported_to_the_model_not_raised(monkeypatch):
    client = _FakeClient(
        {
            "mcp_list_tools": LIST_RESPONSE,
            "mcp_call_tool": RuntimeError("workspace unreachable"),
        }
    )
    monkeypatch.setattr(workspace_mcp, "APIClient", lambda configuration=None: client)
    toolkit = _toolkit()
    await toolkit.connect()

    result = await toolkit.functions["mcp_tool_echo"].entrypoint(text="hi")

    assert "Error from MCP tool 'echo'" in result.content
    assert "workspace unreachable" in result.content


async def test_is_error_results_are_marked_as_errors(monkeypatch):
    client = _FakeClient(
        {
            "mcp_list_tools": LIST_RESPONSE,
            "mcp_call_tool": {"content": "boom", "is_error": True},
        }
    )
    monkeypatch.setattr(workspace_mcp, "APIClient", lambda configuration=None: client)
    toolkit = _toolkit()
    await toolkit.connect()

    result = await toolkit.functions["mcp_tool_echo"].entrypoint(text="hi")
    assert result.content == "Error from MCP tool 'echo': boom"


async def test_close_leaves_the_server_running_in_the_workspace(bridge):
    toolkit = _toolkit()
    await toolkit.connect()
    await toolkit.close()

    assert toolkit.initialized is False
    assert all(call["path"].endswith("mcp_list_tools") for call in bridge.calls)


async def test_tools_collapse_into_dynamic_proxies(bridge):
    """A local server feeds the same dynamic catalog a remote one does."""
    toolkit = _toolkit()
    await toolkit.connect()

    proxies = build_mcp_proxies(toolkit, server_name="Some MCP", server_url=None)

    assert [p.id for p in proxies] == ["mcp_tool_echo", "mcp_tool_read_token"]
    assert all(p.is_mcp_proxy for p in proxies)
    assert proxies[0].server_name == "Some MCP"
    assert proxies[0].server_url is None
    assert proxies[0].raw_json_schema == LIST_RESPONSE["tools"][0]["input_schema"]
    assert (await proxies[0].ainvoke({"text": "hi"})) == "echo:hi"


async def test_a_non_json_call_response_is_reported_not_raised(monkeypatch):
    """A text 200 arrives as a plain string; reading it as a dict would crash the tool."""
    client = _FakeClient(
        {"mcp_list_tools": LIST_RESPONSE, "mcp_call_tool": "upstream said no"}
    )
    monkeypatch.setattr(workspace_mcp, "APIClient", lambda configuration=None: client)
    toolkit = _toolkit()
    await toolkit.connect()

    result = await toolkit.functions["mcp_tool_echo"].entrypoint(text="hi")
    assert result.content == "upstream said no"


async def test_a_non_json_list_response_leaves_no_tools(monkeypatch):
    client = _FakeClient({"mcp_list_tools": "bad gateway"})
    monkeypatch.setattr(workspace_mcp, "APIClient", lambda configuration=None: client)
    toolkit = _toolkit()
    await toolkit.connect()

    assert toolkit.functions == {}


async def test_a_tool_declaring_agent_as_a_parameter_still_receives_it(monkeypatch):
    """Stripping agno's context keys must not eat a tool's own parameter of that name."""
    listing = {
        "server_key": "k",
        "tools": [
            {
                "name": "assign",
                "description": "",
                "input_schema": {
                    "type": "object",
                    "properties": {"agent": {"type": "string"}},
                },
            }
        ],
    }
    client = _FakeClient(
        {
            "mcp_list_tools": listing,
            "mcp_call_tool": {"content": "ok", "is_error": False},
        }
    )
    monkeypatch.setattr(workspace_mcp, "APIClient", lambda configuration=None: client)
    toolkit = _toolkit()
    await toolkit.connect()

    await toolkit.functions["mcp_tool_assign"].entrypoint(
        agent="me", run_context=object()
    )

    assert bridge_args(client) == {"agent": "me"}


def bridge_args(client: _FakeClient) -> dict:
    return client.calls[-1]["payload"]["arguments"]


# ===== start-failure notes carry the workspace's classified reason =====


def test_failure_reason_extracts_http_detail():
    from xpander_sdk.modules.backend.frameworks.agno import (
        _workspace_mcp_failure_reason,
    )

    class _Resp:
        text = ""

        def json(self):
            return {
                "detail": "'x' exited before completing the MCP handshake - the command must be a long-running stdio MCP server, not an installer or one-shot tool"
            }

    err = Exception("502 Bad Gateway")
    err.response = _Resp()
    reason = _workspace_mcp_failure_reason(err)
    assert "exited before completing the MCP handshake" in reason
    assert len(reason) <= 203


def test_failure_reason_empty_for_bare_errors():
    from xpander_sdk.modules.backend.frameworks.agno import (
        _workspace_mcp_failure_reason,
    )

    assert _workspace_mcp_failure_reason(Exception("boom")) == ""


async def test_connect_sends_a_startup_timeout_to_the_bridge(bridge):
    await _toolkit().connect()

    payload = bridge.calls[0]["payload"]
    assert payload["timeout"] == workspace_mcp.STARTUP_TIMEOUT


async def test_a_hung_bridge_times_out_with_a_clear_error(monkeypatch):
    import asyncio

    class _HungClient:
        async def make_request(self, *a, **k):
            await asyncio.sleep(999)

    monkeypatch.setattr(
        workspace_mcp, "APIClient", lambda configuration=None: _HungClient()
    )
    monkeypatch.setattr(workspace_mcp, "STARTUP_TIMEOUT", 0)
    monkeypatch.setattr(workspace_mcp, "STARTUP_GRACE", 0.2)

    with pytest.raises(TimeoutError) as exc:
        await _toolkit().connect()

    assert "did not answer within" in str(exc.value)
    assert "next run" in str(exc.value)
