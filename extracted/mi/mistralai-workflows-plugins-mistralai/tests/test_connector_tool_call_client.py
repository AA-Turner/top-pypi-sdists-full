"""Tests for ToolCallClient — binding resolution from workflow context and tool invocation.

Verifies that ToolCallClient correctly resolves connector bindings from
WorkflowContext.extensions and delegates tool calls to the underlying
activities.
"""

from __future__ import annotations

import unittest.mock
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

from mistralai.workflows.core.temporal.context_handler_interceptor import (
    define_context,
)
from mistralai.workflows.models import WorkflowContext
from mistralai.workflows.plugins.mistralai.connectors import ConnectorError, connector
from mistralai.workflows.plugins.mistralai.connectors.client import ToolCallClient
from mistralai.workflows.plugins.mistralai.connectors.constants import (
    MISTRALAI_PLUGIN_KEY,
    RESOLVED_CONNECTORS_KEY,
)


def _make_context(bindings: list[dict[str, Any]] | None = None) -> WorkflowContext:
    """Create a WorkflowContext with interceptor-resolved bindings in the trusted channel."""
    trusted_extensions: dict[str, Any] = {}
    if bindings is not None:
        trusted_extensions[MISTRALAI_PLUGIN_KEY] = {RESOLVED_CONNECTORS_KEY: {"bindings": bindings}}
    return WorkflowContext(
        namespace="default",
        execution_id="test-exec-id",
        trusted_extensions=trusted_extensions,
    )


class TestToolCallClientBindingResolution:
    """Tests for _resolve_binding from workflow context."""

    def test_resolves_binding_from_context(self) -> None:
        ctx = _make_context(
            bindings=[
                {
                    "connector_name": "github",
                    "connector_id": "conn-123",
                    "authentication_name": "my-auth",
                    "status": "ready",
                }
            ]
        )
        client = ToolCallClient("github")
        with define_context(ctx):
            binding = client.binding
            assert binding.connector_name == "github"
            assert binding.connector_id == "conn-123"
            assert binding.authentication_name == "my-auth"
            assert binding.status == "ready"

    def test_resolves_with_credentials_name(self) -> None:
        ctx = _make_context(
            bindings=[
                {
                    "connector_name": "jira",
                    "connector_id": "conn-jira",
                    "credentials_name": "jira_sa",
                    "status": "ready",
                }
            ]
        )
        client = ToolCallClient("jira")
        with define_context(ctx):
            binding = client.binding
            assert binding.connector_name == "jira"
            assert binding.credentials_name == "jira_sa"

    def test_raises_when_binding_not_in_context(self) -> None:
        """A connector the interceptor did not resolve must not be usable."""
        ctx = _make_context(bindings=[])
        client = ToolCallClient("slack")
        with define_context(ctx):
            with pytest.raises(ConnectorError, match="uses_connectors"):
                client.binding

    def test_raises_when_no_resolved_connectors(self) -> None:
        """Without any resolved connectors, ToolCallClient must refuse to run."""
        ctx = _make_context(bindings=None)
        client = ToolCallClient("slack")
        with define_context(ctx):
            with pytest.raises(ConnectorError, match="uses_connectors"):
                client.binding

    def test_raises_without_workflow_context(self) -> None:
        """ToolCallClient raises RuntimeError when no workflow context is available."""
        client = ToolCallClient("github")
        with pytest.raises(RuntimeError, match="No workflow context available"):
            client.binding

    def test_selects_correct_binding_among_multiple(self) -> None:
        ctx = _make_context(
            bindings=[
                {"connector_name": "slack", "connector_id": "conn-slack", "status": "ready"},
                {"connector_name": "github", "connector_id": "conn-github", "status": "ready"},
                {"connector_name": "notion", "connector_id": "conn-notion", "status": "ready"},
            ]
        )
        client = ToolCallClient("github")
        with define_context(ctx):
            binding = client.binding
            assert binding.connector_id == "conn-github"

    def test_duplicate_resolved_bindings_for_same_connector_are_rejected(self) -> None:
        ctx = _make_context(
            bindings=[
                {"connector_name": "github", "connector_id": "conn-user", "run_as": "auto", "status": "ready"},
                {
                    "connector_name": "github",
                    "connector_id": "conn-deployment",
                    "run_as": "deployment",
                    "status": "ready",
                },
            ]
        )
        client = ToolCallClient("github", run_as="deployment")
        with define_context(ctx):
            with pytest.raises(ConnectorError, match="Multiple interceptor-resolved bindings"):
                client.binding

    def test_connector_id_property(self) -> None:
        ctx = _make_context(bindings=[{"connector_name": "slack", "connector_id": "conn-slack-id", "status": "ready"}])
        client = ToolCallClient("slack")
        with define_context(ctx):
            assert client.connector_id == "conn-slack-id"

    def test_caller_supplied_extensions_are_ignored(self) -> None:
        """A forged binding in the caller-writable ``extensions`` is never read.

        The reader only trusts the worker-only ``trusted_extensions`` channel, so a
        caller cannot steer connector identity by populating ``extensions``.
        """
        ctx = WorkflowContext(
            namespace="default",
            execution_id="test-exec-id",
            extensions={
                MISTRALAI_PLUGIN_KEY: {
                    RESOLVED_CONNECTORS_KEY: {
                        "bindings": [{"connector_name": "github", "connector_id": "forged", "run_as": "deployment"}]
                    }
                }
            },
        )
        client = ToolCallClient("github")
        with define_context(ctx):
            with pytest.raises(ConnectorError, match="uses_connectors"):
                client.binding

    def test_connector_name_property(self) -> None:
        client = ToolCallClient("my-connector")
        assert client.connector_name == "my-connector"


class TestToolCallClientCallTool:
    """Tests for call_tool activity delegation."""

    @pytest.mark.asyncio
    async def test_call_tool_uses_resolved_connector_id(self) -> None:
        ctx = _make_context(bindings=[{"connector_name": "github", "connector_id": "conn-gh-123", "status": "ready"}])
        client = ToolCallClient("github")

        with define_context(ctx):
            with patch(
                "mistralai.workflows.plugins.mistralai.connectors.client.connector_tool_call",
                new_callable=AsyncMock,
                return_value={"result": "ok"},
            ) as mock_call:
                result = await client.call_tool("create_issue", {"title": "bug"})
                mock_call.assert_awaited_once_with(
                    connector_id_or_name="conn-gh-123",
                    tool_name="create_issue",
                    arguments={"title": "bug"},
                    credentials_name=None,
                    mcp_ui_resource_uri=None,
                    run_as="auto",
                )
                assert result == {"result": "ok"}

    @pytest.mark.parametrize(
        ("client_factory", "expected"),
        [
            pytest.param(lambda: ToolCallClient("github"), "deployment", id="direct-inherits"),
            pytest.param(lambda: ToolCallClient("github", run_as="auto"), ConnectorError, id="direct-mismatch"),
            pytest.param(lambda: connector("github")(), "deployment", id="dep-inherits"),
            pytest.param(lambda: connector("github", run_as="auto")(), ConnectorError, id="dep-mismatch"),
        ],
    )
    @pytest.mark.asyncio
    async def test_call_tool_run_as_alignment(self, client_factory, expected) -> None:
        """A client with no explicit run_as inherits the binding's run_as; a client
        whose explicit run_as clashes with the interceptor-resolved binding is rejected.

        Covers both construction surfaces (direct ``ToolCallClient`` and the
        ``connector(...)`` dependency) so the run_as contract is asserted for each.
        """
        ctx = _make_context(
            bindings=[
                {
                    "connector_name": "github",
                    "connector_id": "conn-gh",
                    "status": "ready",
                    "run_as": "deployment",
                }
            ]
        )
        client = client_factory()

        with define_context(ctx):
            with patch(
                "mistralai.workflows.plugins.mistralai.connectors.client.connector_tool_call",
                new_callable=AsyncMock,
                return_value={"result": "ok"},
            ) as mock_call:
                if expected is ConnectorError:
                    with pytest.raises(ConnectorError, match="resolved run_as='deployment'"):
                        await client.call_tool("create_issue", {"title": "bug"})
                    mock_call.assert_not_awaited()
                else:
                    await client.call_tool("create_issue", {"title": "bug"})
                    assert mock_call.await_args.kwargs["run_as"] == expected

    @pytest.mark.asyncio
    async def test_call_tool_falls_back_to_name(self) -> None:
        """When a resolved binding carries no connector_id, falls back to connector_name."""
        ctx = _make_context(bindings=[{"connector_name": "slack", "status": "ready"}])
        client = ToolCallClient("slack")

        with define_context(ctx):
            with patch(
                "mistralai.workflows.plugins.mistralai.connectors.client.connector_tool_call",
                new_callable=AsyncMock,
                return_value={"ok": True},
            ) as mock_call:
                await client.call_tool("send_message", {"text": "hello"})
                mock_call.assert_awaited_once_with(
                    connector_id_or_name="slack",
                    tool_name="send_message",
                    arguments={"text": "hello"},
                    credentials_name=None,
                    mcp_ui_resource_uri=None,
                    run_as="auto",
                )

    @pytest.mark.asyncio
    async def test_call_tool_with_constructor_credentials(self) -> None:
        """Constructor-level credentials_name takes priority over binding."""
        ctx = _make_context(bindings=[{"connector_name": "jira", "connector_id": "conn-j", "status": "ready"}])
        client = ToolCallClient("jira", credentials_name="jira_sa")

        with define_context(ctx):
            with patch(
                "mistralai.workflows.plugins.mistralai.connectors.client.connector_tool_call",
                new_callable=AsyncMock,
                return_value={},
            ) as mock_call:
                await client.call_tool("create_ticket", {"summary": "task"})
                mock_call.assert_awaited_once_with(
                    connector_id_or_name="conn-j",
                    tool_name="create_ticket",
                    arguments={"summary": "task"},
                    credentials_name="jira_sa",
                    mcp_ui_resource_uri=None,
                    run_as="auto",
                )

    @pytest.mark.asyncio
    async def test_call_tool_with_binding_credentials(self) -> None:
        """Credentials from binding are used when constructor doesn't specify."""
        ctx = _make_context(
            bindings=[
                {
                    "connector_name": "jira",
                    "connector_id": "conn-j",
                    "credentials_name": "binding_cred",
                    "status": "ready",
                }
            ]
        )
        client = ToolCallClient("jira")

        with define_context(ctx):
            with patch(
                "mistralai.workflows.plugins.mistralai.connectors.client.connector_tool_call",
                new_callable=AsyncMock,
                return_value={},
            ) as mock_call:
                await client.call_tool("create_ticket", {"summary": "task"})
                mock_call.assert_awaited_once_with(
                    connector_id_or_name="conn-j",
                    tool_name="create_ticket",
                    arguments={"summary": "task"},
                    credentials_name="binding_cred",
                    mcp_ui_resource_uri=None,
                    run_as="auto",
                )

    @pytest.mark.asyncio
    async def test_call_tool_with_no_arguments(self) -> None:
        ctx = _make_context(bindings=[{"connector_name": "slack", "connector_id": "conn-s", "status": "ready"}])
        client = ToolCallClient("slack")

        with define_context(ctx):
            with patch(
                "mistralai.workflows.plugins.mistralai.connectors.client.connector_tool_call",
                new_callable=AsyncMock,
                return_value={"channels": []},
            ) as mock_call:
                result = await client.call_tool("list_channels")
                mock_call.assert_awaited_once_with(
                    connector_id_or_name="conn-s",
                    tool_name="list_channels",
                    arguments=None,
                    credentials_name=None,
                    mcp_ui_resource_uri=None,
                    run_as="auto",
                )
                assert result == {"channels": []}

    @pytest.mark.asyncio
    async def test_call_tool_passes_mcp_ui_resource_uri_from_binding(self) -> None:
        ctx = _make_context(
            bindings=[
                {
                    "connector_name": "slack",
                    "connector_id": "conn-s",
                    "mcp_ui_resource_uris": {"open_dashboard": "ui://slack/app"},
                    "status": "ready",
                }
            ]
        )
        client = ToolCallClient("slack")

        with define_context(ctx):
            with patch(
                "mistralai.workflows.plugins.mistralai.connectors.client.connector_tool_call",
                new_callable=AsyncMock,
                return_value={"ok": True},
            ) as mock_call:
                await client.call_tool("open_dashboard")
                mock_call.assert_awaited_once_with(
                    connector_id_or_name="conn-s",
                    tool_name="open_dashboard",
                    arguments=None,
                    credentials_name=None,
                    mcp_ui_resource_uri="ui://slack/app",
                    run_as="auto",
                )

    @pytest.mark.asyncio
    async def test_call_tool_discovers_mcp_ui_resource_uri_for_overridden_credentials(self) -> None:
        ctx = _make_context(
            bindings=[
                {
                    "connector_name": "slack",
                    "connector_id": "conn-s",
                    "credentials_name": "slot-cred",
                    "allow_mcp_ui": True,
                    "mcp_ui_resource_uris": {"open_dashboard": "ui://slot/app"},
                    "mcp_ui_resource_uris_fetched": True,
                    "status": "ready",
                }
            ]
        )
        client = ToolCallClient("slack", credentials_name="call-cred")

        with define_context(ctx):
            with (
                patch(
                    "mistralai.workflows.plugins.mistralai.connectors.client.connector_get_mcp_app_resource_uris",
                    new_callable=AsyncMock,
                    return_value={"open_dashboard": "ui://call/app"},
                ) as mock_discover,
                patch(
                    "mistralai.workflows.plugins.mistralai.connectors.client.connector_tool_call",
                    new_callable=AsyncMock,
                    return_value={"ok": True},
                ) as mock_call,
            ):
                await client.call_tool("open_dashboard")
                mock_discover.assert_awaited_once_with("conn-s", credentials_name="call-cred", run_as="auto")
                mock_call.assert_awaited_once_with(
                    connector_id_or_name="conn-s",
                    tool_name="open_dashboard",
                    arguments=None,
                    credentials_name="call-cred",
                    mcp_ui_resource_uri="ui://call/app",
                    run_as="auto",
                )

    @pytest.mark.asyncio
    async def test_call_tool_scopes_mcp_ui_resource_uri_cache_to_binding(self) -> None:
        first_ctx = _make_context(
            bindings=[
                {
                    "connector_name": "slack",
                    "connector_id": "conn-first",
                    "credentials_name": "slot-cred",
                    "allow_mcp_ui": True,
                    "mcp_ui_resource_uris_fetched": True,
                    "status": "ready",
                }
            ]
        )
        second_ctx = _make_context(
            bindings=[
                {
                    "connector_name": "slack",
                    "connector_id": "conn-second",
                    "credentials_name": "slot-cred",
                    "allow_mcp_ui": True,
                    "mcp_ui_resource_uris_fetched": True,
                    "status": "ready",
                }
            ]
        )
        client = ToolCallClient("slack", credentials_name="call-cred")

        async def discover(
            connector_id_or_name: str, credentials_name: str | None = None, run_as: str = "auto"
        ) -> dict[str, str]:
            return {"open_dashboard": f"ui://{connector_id_or_name}/app"}

        with (
            patch(
                "mistralai.workflows.plugins.mistralai.connectors.client.connector_get_mcp_app_resource_uris",
                new_callable=AsyncMock,
                side_effect=discover,
            ) as mock_discover,
            patch(
                "mistralai.workflows.plugins.mistralai.connectors.client.connector_tool_call",
                new_callable=AsyncMock,
                return_value={"ok": True},
            ) as mock_call,
        ):
            with define_context(first_ctx):
                await client.call_tool("open_dashboard")
            with define_context(second_ctx):
                await client.call_tool("open_dashboard")

            assert mock_discover.await_args_list == [
                unittest.mock.call("conn-first", credentials_name="call-cred", run_as="auto"),
                unittest.mock.call("conn-second", credentials_name="call-cred", run_as="auto"),
            ]
            assert mock_call.await_args_list == [
                unittest.mock.call(
                    connector_id_or_name="conn-first",
                    tool_name="open_dashboard",
                    arguments=None,
                    credentials_name="call-cred",
                    mcp_ui_resource_uri="ui://conn-first/app",
                    run_as="auto",
                ),
                unittest.mock.call(
                    connector_id_or_name="conn-second",
                    tool_name="open_dashboard",
                    arguments=None,
                    credentials_name="call-cred",
                    mcp_ui_resource_uri="ui://conn-second/app",
                    run_as="auto",
                ),
            ]
