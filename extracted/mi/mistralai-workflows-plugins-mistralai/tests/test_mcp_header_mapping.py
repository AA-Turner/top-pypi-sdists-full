"""Tests for MCPStreamableHTTPConfig.header_mapping secure credential forwarding.

The critical invariant mirrors env_mapping (WFL-2091): header_mapping lets a
Streamable HTTP MCP caller send secret credentials (e.g. a Notion bot token and
an endpoint bearer) per request while ONLY the mapping names, never the secret
values, are serialized into Temporal activity params and event history. The
secrets are read from the worker's os.environ inside the activity body.

The second invariant is per-call isolation: a Streamable HTTP client is opened
per call (not pooled), so a caller's resolved token only ever reaches its own
client and never bleeds into another caller's session.
"""

import logging
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.core.workflow import workflow
from mistralai.workflows.plugins.mistralai.mcp import (
    CollectMCPToolsParams,
    ExecuteMCPToolParams,
    MCPStreamableHTTPConfig,
    _resolve_headers,
    _resolve_streamable_http_headers,
    collect_mcp_tools,
    collect_tools_streamable_http,
    execute_mcp_tool,
)
from mistralai.workflows.testing import (
    create_capturing_mock_events_client,
    create_test_worker_with_events,
)
from mistralai.workflows.testing.fixtures import (
    clear_dependency_cache,  # noqa: F401
    event_loop,  # noqa: F401
    mock_upsert_search_attributes,  # noqa: F401
    setup_test_config,  # noqa: F401
    temporal_env,  # noqa: F401
)

NOTION_SECRET = "ntn_super_secret_do_not_leak"
AUTH_SECRET = "Bearer gate_super_secret_do_not_leak"
NOTION_WORKER_VAR = "NOTION_TOKEN_BOT_A"
AUTH_WORKER_VAR = "NOTION_MCP_AUTH_BOT_A"
NOTION_HEADER = "Notion-Token"
AUTH_HEADER = "Authorization"

_TOOLS = [{"function": {"name": "search"}}]


def _mock_http_client(constructions: list[dict[str, Any]]) -> Any:
    """Factory replacing MCPClientStreamableHTTP, recording each construction's headers."""

    def make(params: Any, name: str) -> MagicMock:
        constructions.append(
            {
                "url": params.url,
                "headers": params.headers,
                "name": name,
                "trust_env": params.trust_env,
                "follow_redirects": params.follow_redirects,
            }
        )
        instance = MagicMock()
        instance.initialize = AsyncMock()
        instance.get_tools = AsyncMock(return_value=list(_TOOLS))
        instance.execute_tool = AsyncMock(return_value="ok")
        instance.aclose = AsyncMock()
        return instance

    return make


class TestResolveHeaders:
    def test_none_returns_none(self) -> None:
        assert _resolve_headers(None, None) is None

    def test_static_headers_pass_through(self) -> None:
        assert _resolve_headers({"X-Static": "1"}, None) == {"X-Static": "1"}

    def test_mapping_merges_from_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv(NOTION_WORKER_VAR, NOTION_SECRET)
        resolved = _resolve_headers(None, {NOTION_HEADER: NOTION_WORKER_VAR})
        assert resolved == {NOTION_HEADER: NOTION_SECRET}

    def test_static_and_mapping_merge(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv(NOTION_WORKER_VAR, NOTION_SECRET)
        resolved = _resolve_headers({"X-Static": "1"}, {NOTION_HEADER: NOTION_WORKER_VAR})
        assert resolved == {"X-Static": "1", NOTION_HEADER: NOTION_SECRET}

    def test_missing_worker_var_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv(NOTION_WORKER_VAR, raising=False)
        with pytest.raises(RuntimeError, match=NOTION_WORKER_VAR):
            _resolve_headers(None, {NOTION_HEADER: NOTION_WORKER_VAR})

    def test_whitespace_only_worker_var_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # A secret mounted as whitespace-only is treated as unset, mirroring auth_token_env.
        monkeypatch.setenv(NOTION_WORKER_VAR, "   \n")
        with pytest.raises(RuntimeError, match="empty/whitespace"):
            _resolve_headers(None, {NOTION_HEADER: NOTION_WORKER_VAR})

    def test_worker_var_value_is_stripped(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # Trailing newlines from secret mounts must not corrupt the header value.
        monkeypatch.setenv(NOTION_WORKER_VAR, f"{NOTION_SECRET}\n")
        resolved = _resolve_headers(None, {NOTION_HEADER: NOTION_WORKER_VAR})
        assert resolved == {NOTION_HEADER: NOTION_SECRET}

    def test_maps_header_name_not_worker_name(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("SOURCE_VAR", "value-123")
        resolved = _resolve_headers(None, {"Target-Header": "SOURCE_VAR"})
        assert resolved is not None
        assert resolved["Target-Header"] == "value-123"
        # only the wire header name is emitted, never the worker-side var name
        assert "SOURCE_VAR" not in resolved


class TestResolveStreamableHTTPHeaders:
    def test_none_when_nothing_set(self) -> None:
        config = MCPStreamableHTTPConfig(url="http://x/mcp", name="n")
        assert _resolve_streamable_http_headers(config) is None

    def test_auth_token_env_sets_bearer(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # the stored secret is a raw token; the SDK owns the "Bearer " scheme
        monkeypatch.setenv(AUTH_WORKER_VAR, "raw-hex-token")
        config = MCPStreamableHTTPConfig(url="http://x/mcp", name="n", auth_token_env=AUTH_WORKER_VAR)
        assert _resolve_streamable_http_headers(config) == {AUTH_HEADER: "Bearer raw-hex-token"}

    def test_auth_token_env_missing_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv(AUTH_WORKER_VAR, raising=False)
        config = MCPStreamableHTTPConfig(url="http://x/mcp", name="n", auth_token_env=AUTH_WORKER_VAR)
        with pytest.raises(RuntimeError, match=AUTH_WORKER_VAR):
            _resolve_streamable_http_headers(config)

    def test_auth_token_env_combines_with_header_mapping(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv(AUTH_WORKER_VAR, "raw-hex-token")
        monkeypatch.setenv(NOTION_WORKER_VAR, NOTION_SECRET)
        config = MCPStreamableHTTPConfig(
            url="http://x/mcp",
            name="n",
            auth_token_env=AUTH_WORKER_VAR,
            header_mapping={NOTION_HEADER: NOTION_WORKER_VAR},
        )
        assert _resolve_streamable_http_headers(config) == {
            NOTION_HEADER: NOTION_SECRET,
            AUTH_HEADER: "Bearer raw-hex-token",
        }

    def test_auth_token_env_conflicting_with_authorization_header_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # both auth_token_env and an explicit Authorization header would fight over the
        # same header; fail loudly instead of silently dropping one credential
        monkeypatch.setenv(AUTH_WORKER_VAR, "raw-hex-token")
        monkeypatch.setenv("OTHER_AUTH_VAR", "Bearer other")
        config = MCPStreamableHTTPConfig(
            url="http://x/mcp",
            name="n",
            auth_token_env=AUTH_WORKER_VAR,
            header_mapping={AUTH_HEADER: "OTHER_AUTH_VAR"},
        )
        with pytest.raises(RuntimeError, match="only one"):
            _resolve_streamable_http_headers(config)


@workflow.define(name="mcp_header_mapping_workflow")
class MCPHeaderMappingWorkflow:
    @workflow.entrypoint
    async def run(self) -> int:
        config = MCPStreamableHTTPConfig(
            url="http://notion.internal-use-mcps.svc.cluster.local/mcp",
            name="notion_bot_a",
            header_mapping={NOTION_HEADER: NOTION_WORKER_VAR, AUTH_HEADER: AUTH_WORKER_VAR},
        )
        result = await collect_mcp_tools(CollectMCPToolsParams(configs=[config]))
        return len(result.tools)


@pytest.mark.asyncio
async def test_header_mapping_resolves_but_never_leaks_to_temporal(
    temporal_env: WorkflowEnvironment,  # noqa: F811
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The secrets reach the client headers but never the Temporal event payload."""
    monkeypatch.setenv(NOTION_WORKER_VAR, NOTION_SECRET)
    monkeypatch.setenv(AUTH_WORKER_VAR, AUTH_SECRET)

    constructions: list[dict[str, Any]] = []
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    with patch(
        "mistralai.workflows.plugins.mistralai.mcp.MCPClientStreamableHTTP",
        side_effect=_mock_http_client(constructions),
    ):
        async with EventContext(mock_client):
            async with create_test_worker_with_events(
                temporal_env,
                workflows=[MCPHeaderMappingWorkflow],
                activities=[collect_mcp_tools],
            ):
                handle = await temporal_env.client.start_workflow(
                    "mcp_header_mapping_workflow",
                    id="test-mcp-header-mapping",
                    task_queue="test-task-queue",
                )
                tool_count = await handle.result()

    # Temporal returns the workflow result wrapped ({"result": 1}) in this test
    # harness, but a plain int in others; accept both so the assertion is portable.
    assert tool_count in (1, {"result": 1})

    # Resolution happened inside the activity: the real secrets reached the client headers.
    assert constructions, "MCPClientStreamableHTTP was never constructed"
    headers = constructions[0]["headers"]
    assert headers[NOTION_HEADER] == NOTION_SECRET
    assert headers[AUTH_HEADER] == AUTH_SECRET

    started = [
        e
        for e in captured_events
        if e.event_type.value == "ACTIVITY_TASK_STARTED" and e.attributes.activity_name == "collect_mcp_tools"
    ]
    assert started, "collect_mcp_tools ActivityTaskStarted event was not captured"

    serialized_input = str(started[0].attributes.input.value)
    # Mapping names (header + worker var) are safe and expected in serialized params.
    assert NOTION_HEADER in serialized_input
    assert NOTION_WORKER_VAR in serialized_input
    assert AUTH_WORKER_VAR in serialized_input
    # The critical assertion: no secret value ever touches Temporal params / history.
    assert NOTION_SECRET not in serialized_input
    assert AUTH_SECRET not in serialized_input


@pytest.mark.asyncio
async def test_resolved_secret_reaches_headers_but_is_never_logged(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """collect_tools_streamable_http sets the secret headers without logging them."""
    monkeypatch.setenv(NOTION_WORKER_VAR, NOTION_SECRET)
    monkeypatch.setenv(AUTH_WORKER_VAR, AUTH_SECRET)
    constructions: list[dict[str, Any]] = []
    config = MCPStreamableHTTPConfig(
        # unique url so this test's cache entry cannot collide with another test's
        url="http://notion.svc/mcp#not-logged",
        name="notion",
        header_mapping={NOTION_HEADER: NOTION_WORKER_VAR, AUTH_HEADER: AUTH_WORKER_VAR},
    )
    with patch(
        "mistralai.workflows.plugins.mistralai.mcp.MCPClientStreamableHTTP",
        side_effect=_mock_http_client(constructions),
    ):
        with caplog.at_level(logging.DEBUG):
            await collect_tools_streamable_http(config)

    assert constructions[0]["headers"][NOTION_HEADER] == NOTION_SECRET
    assert constructions[0]["headers"][AUTH_HEADER] == AUTH_SECRET
    # Secrets must not appear in structured logs or console output.
    assert NOTION_SECRET not in caplog.text
    assert AUTH_SECRET not in caplog.text
    combined = capsys.readouterr()
    assert NOTION_SECRET not in combined.err
    assert AUTH_SECRET not in combined.err


@pytest.mark.asyncio
async def test_each_call_builds_an_isolated_client_with_only_its_token(monkeypatch: pytest.MonkeyPatch) -> None:
    """Each call opens its own client with only its own resolved token; no bleed.

    Streamable HTTP clients are opened per call (not pooled), so isolation is
    inherent: a caller's token is never present in another caller's client, and no
    session is shared across callers.
    """
    url = "http://notion.svc/mcp#isolation"
    constructions: list[dict[str, Any]] = []

    def config_for(worker_var: str) -> MCPStreamableHTTPConfig:
        return MCPStreamableHTTPConfig(url=url, name="notion", header_mapping={NOTION_HEADER: worker_var})

    monkeypatch.setenv("TOKEN_A", "token-a-value")
    monkeypatch.setenv("TOKEN_B", "token-b-value")

    with patch(
        "mistralai.workflows.plugins.mistralai.mcp.MCPClientStreamableHTTP",
        side_effect=_mock_http_client(constructions),
    ):
        await collect_tools_streamable_http(config_for("TOKEN_A"))
        await collect_tools_streamable_http(config_for("TOKEN_B"))
        await collect_tools_streamable_http(config_for("TOKEN_A"))

    # One fresh client per call, each carrying only its own token (no cross-bleed).
    assert [c["headers"][NOTION_HEADER] for c in constructions] == [
        "token-a-value",
        "token-b-value",
        "token-a-value",
    ]
    for c in constructions:
        assert list(c["headers"].keys()) == [NOTION_HEADER]


@pytest.mark.asyncio
async def test_trust_env_from_config_reaches_client(monkeypatch: pytest.MonkeyPatch) -> None:
    """config.trust_env is forwarded to the client (so an in-cluster MCP can opt
    out of the worker's ambient proxy)."""
    monkeypatch.setenv(NOTION_WORKER_VAR, NOTION_SECRET)
    constructions: list[dict[str, Any]] = []
    config = MCPStreamableHTTPConfig(
        url="http://notion.svc/mcp#trustenv",
        name="notion",
        header_mapping={NOTION_HEADER: NOTION_WORKER_VAR},
        trust_env=False,
    )
    with patch(
        "mistralai.workflows.plugins.mistralai.mcp.MCPClientStreamableHTTP",
        side_effect=_mock_http_client(constructions),
    ):
        await collect_tools_streamable_http(config)

    assert constructions[0]["trust_env"] is False


@pytest.mark.asyncio
async def test_follow_redirects_defaults_false_and_is_configurable(monkeypatch: pytest.MonkeyPatch) -> None:
    """follow_redirects defaults False so secret headers are never resent to a
    redirect target, and is forwarded to the client when explicitly enabled."""
    monkeypatch.setenv(NOTION_WORKER_VAR, NOTION_SECRET)
    constructions: list[dict[str, Any]] = []
    default_config = MCPStreamableHTTPConfig(
        url="http://notion.svc/mcp#redir-default",
        name="notion",
        header_mapping={NOTION_HEADER: NOTION_WORKER_VAR},
    )
    enabled_config = MCPStreamableHTTPConfig(
        url="http://notion.svc/mcp#redir-on",
        name="notion",
        header_mapping={NOTION_HEADER: NOTION_WORKER_VAR},
        follow_redirects=True,
    )
    with patch(
        "mistralai.workflows.plugins.mistralai.mcp.MCPClientStreamableHTTP",
        side_effect=_mock_http_client(constructions),
    ):
        await collect_tools_streamable_http(default_config)
        await collect_tools_streamable_http(enabled_config)

    assert constructions[0]["follow_redirects"] is False
    assert constructions[1]["follow_redirects"] is True


@pytest.mark.asyncio
async def test_execute_mcp_tool_resolves_headers(monkeypatch: pytest.MonkeyPatch) -> None:
    """execute_mcp_tool forwards the resolved secrets to the client headers too."""
    monkeypatch.setenv(NOTION_WORKER_VAR, NOTION_SECRET)
    monkeypatch.setenv(AUTH_WORKER_VAR, AUTH_SECRET)
    constructions: list[dict[str, Any]] = []
    config = MCPStreamableHTTPConfig(
        url="http://notion.svc/mcp#execute",
        name="notion",
        header_mapping={NOTION_HEADER: NOTION_WORKER_VAR, AUTH_HEADER: AUTH_WORKER_VAR},
    )
    params = ExecuteMCPToolParams(
        configs=[config],
        tool_name="notion_search",
        tool_arguments={},
        config_index=0,
    )
    with patch(
        "mistralai.workflows.plugins.mistralai.mcp.MCPClientStreamableHTTP",
        side_effect=_mock_http_client(constructions),
    ):
        result = await execute_mcp_tool(params)

    assert result.result == "ok"
    assert constructions[0]["headers"][NOTION_HEADER] == NOTION_SECRET
    assert constructions[0]["headers"][AUTH_HEADER] == AUTH_SECRET
