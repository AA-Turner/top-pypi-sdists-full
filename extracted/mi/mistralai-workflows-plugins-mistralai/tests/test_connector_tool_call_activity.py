from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from mistralai.client.models.connectortoolcallmetadata import ConnectorToolCallMetadata
from mistralai.client.models.connectortoolcallresponse import (
    ConnectorToolCallResponse,
    TextContent,
)
from mistralai.client.models.connectortoolresultmetadata import (
    ConnectorToolResultMetadata,
)
from mistralai.client.models.mcptool import MCPTool
from mistralai.client.models.mcptoolmeta import MCPToolMeta
from mistralai.client.models.mcpuitoolmeta import MCPUIToolMeta

from mistralai.workflows.plugins.mistralai.connectors.activities import (
    connector_tool_call,
)
from mistralai.workflows.plugins.mistralai.connectors.exceptions import ConnectorToolCallError
from mistralai.workflows.plugins.mistralai.connectors.mcp_apps import (
    _collect_declared_mcp_app_uris,
    _get_tool_definition_ui_resource_uri,
    _is_tool_app_visible,
    _trim_mcp_app_tool_result,
    connector_get_mcp_app_resource_uris,
)
from mistralai.workflows.protocol.v1.events import (
    CustomTaskCompleted,
    CustomTaskFailed,
    CustomTaskStarted,
)


def _make_response(
    text: str = "ok",
    is_error: bool = False,
) -> ConnectorToolCallResponse:
    metadata = ConnectorToolCallMetadata(
        mcp_meta=ConnectorToolResultMetadata(is_error=is_error),
    )
    return ConnectorToolCallResponse(
        content=[TextContent(text=text, type="text")],
        metadata=metadata,
    )


class TestConnectorCredentialResolution:
    @pytest.mark.parametrize("on_behalf_of", [True, False])
    @pytest.mark.asyncio
    async def test_tool_call_resolves_executor_credentials_from_obo(self, on_behalf_of: bool) -> None:
        response = _make_response(text="ok", is_error=False)

        with (
            patch("mistralai.workflows.plugins.mistralai.connectors.activities.get_mistral_client") as mock_get_client,
            patch(
                "mistralai.workflows.plugins.mistralai.connectors.activities.should_use_executor_credentials",
                return_value=on_behalf_of,
            ),
        ):
            mock_client = AsyncMock()
            mock_client.beta.connectors.call_tool_async.return_value = response
            mock_get_client.return_value = mock_client

            await connector_tool_call.__wrapped__(
                connector_id_or_name="github",
                tool_name="issue_read",
                arguments={"issue_id": "123"},
            )

        mock_get_client.assert_called_once_with(use_executor_credentials=on_behalf_of)


class TestConnectorToolCallErrorHandling:
    @pytest.mark.asyncio
    async def test_raises_non_retryable_on_mcp_error(self) -> None:
        error_msg = "failed to create issue: POST https://api.github.com/repos/x/y/issues: 404 Not Found []"
        response = _make_response(text=error_msg, is_error=True)

        with patch("mistralai.workflows.plugins.mistralai.connectors.activities.get_mistral_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.beta.connectors.call_tool_async.return_value = response
            mock_get_client.return_value = mock_client

            with pytest.raises(ConnectorToolCallError, match=r"\[github\] connector tool call failed") as exc_info:
                await connector_tool_call.__wrapped__(
                    connector_id_or_name="github",
                    tool_name="issue_write",
                    arguments={"title": "test"},
                )

            assert exc_info.value.non_retryable is True
            assert exc_info.value.type == "ConnectorToolCallError"
            assert exc_info.value.details == (response,)

    @pytest.mark.asyncio
    async def test_raises_with_default_message_when_no_text(self) -> None:
        response = ConnectorToolCallResponse(
            content=[],
            metadata=ConnectorToolCallMetadata(
                mcp_meta=ConnectorToolResultMetadata(is_error=True),
            ),
        )

        with patch("mistralai.workflows.plugins.mistralai.connectors.activities.get_mistral_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.beta.connectors.call_tool_async.return_value = response
            mock_get_client.return_value = mock_client

            with pytest.raises(ConnectorToolCallError, match=r"\[github\] connector tool call failed") as exc_info:
                await connector_tool_call.__wrapped__(
                    connector_id_or_name="github",
                    tool_name="issue_write",
                )

            assert exc_info.value.non_retryable is True

    @pytest.mark.asyncio
    async def test_returns_result_on_success(self) -> None:
        response = _make_response(text="created", is_error=False)

        with patch("mistralai.workflows.plugins.mistralai.connectors.activities.get_mistral_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.beta.connectors.call_tool_async.return_value = response
            mock_get_client.return_value = mock_client

            result = await connector_tool_call.__wrapped__(
                connector_id_or_name="github",
                tool_name="issue_read",
                arguments={"issue_id": "123"},
            )

            assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_logs_mcp_error_response(self) -> None:
        response = _make_response(text="some error detail", is_error=True)

        with (
            patch("mistralai.workflows.plugins.mistralai.connectors.activities.get_mistral_client") as mock_get_client,
            patch("mistralai.workflows.plugins.mistralai.connectors.activities.logger") as mock_logger,
        ):
            mock_client = AsyncMock()
            mock_client.beta.connectors.call_tool_async.return_value = response
            mock_get_client.return_value = mock_client

            with pytest.raises(ConnectorToolCallError):
                await connector_tool_call.__wrapped__(
                    connector_id_or_name="github",
                    tool_name="issue_write",
                )

            mock_logger.error.assert_called_once_with(
                "Connector tool call returned MCP error",
                connector_id_or_name="github",
                tool_name="issue_write",
                response=response.model_dump(),
            )

    @pytest.mark.asyncio
    async def test_returns_result_when_no_metadata(self) -> None:
        response = ConnectorToolCallResponse(
            content=[TextContent(text="ok", type="text")],
        )

        with patch("mistralai.workflows.plugins.mistralai.connectors.activities.get_mistral_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.beta.connectors.call_tool_async.return_value = response
            mock_get_client.return_value = mock_client

            result = await connector_tool_call.__wrapped__(
                connector_id_or_name="github",
                tool_name="issue_read",
            )

            assert isinstance(result, dict)


class TestConnectorToolCallMcpApps:
    @pytest.mark.asyncio
    async def test_get_mcp_app_resource_uris_from_tool_definitions(self) -> None:
        with patch("mistralai.workflows.plugins.mistralai.connectors.mcp_apps.get_mistral_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.beta.connectors.list_tools_async.return_value = [
                {
                    "name": "debug-tool",
                    "_meta": {"ui": {"resourceUri": "ui://debug/app"}},
                },
                {"name": "regular-tool", "_meta": {}},
            ]
            mock_get_client.return_value = mock_client

            assert await connector_get_mcp_app_resource_uris.__wrapped__(
                connector_id_or_name="mcp_apps_test",
                credentials_name="creds",
            ) == {"debug-tool": "ui://debug/app"}

        mock_client.beta.connectors.list_tools_async.assert_awaited_once_with(
            connector_id_or_name="mcp_apps_test",
            credentials_name="creds",
        )

    @pytest.mark.asyncio
    async def test_get_mcp_app_resource_uris_from_sdk_model_metadata(self) -> None:
        with patch("mistralai.workflows.plugins.mistralai.connectors.mcp_apps.get_mistral_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.beta.connectors.list_tools_async.return_value = [
                MCPTool(
                    name="debug-tool",
                    inputSchema={},
                    _meta=MCPToolMeta(
                        ui=MCPUIToolMeta(resourceUri="ui://debug/app"),
                    ),
                )
            ]
            mock_get_client.return_value = mock_client

            assert await connector_get_mcp_app_resource_uris.__wrapped__(
                connector_id_or_name="mcp_apps_test",
            ) == {"debug-tool": "ui://debug/app"}

    @pytest.mark.asyncio
    async def test_get_mcp_app_resource_uris_returns_empty_on_list_failure(self) -> None:
        with patch("mistralai.workflows.plugins.mistralai.connectors.mcp_apps.get_mistral_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.beta.connectors.list_tools_async.side_effect = RuntimeError("expired")
            mock_get_client.return_value = mock_client

            assert (
                await connector_get_mcp_app_resource_uris.__wrapped__(
                    connector_id_or_name="mcp_apps_test",
                )
                == {}
            )

    @pytest.mark.asyncio
    async def test_get_mcp_app_resource_uris_can_raise_on_list_failure(self) -> None:
        with patch("mistralai.workflows.plugins.mistralai.connectors.mcp_apps.get_mistral_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.beta.connectors.list_tools_async.side_effect = RuntimeError("expired")
            mock_get_client.return_value = mock_client

            with pytest.raises(RuntimeError, match="expired"):
                await connector_get_mcp_app_resource_uris.__wrapped__(
                    connector_id_or_name="mcp_apps_test",
                    raise_on_error=True,
                )

    @pytest.mark.asyncio
    async def test_connector_tool_call_emits_mcp_app_from_declared_uri(self) -> None:
        publisher = MagicMock()
        response = _make_response(text="ok", is_error=False)

        with (
            patch("mistralai.workflows.plugins.mistralai.connectors.activities.get_mistral_client") as mock_get_client,
            patch(
                "mistralai.workflows.plugins.mistralai.connectors.mcp_apps.BackgroundEventPublisher.get_current",
                return_value=publisher,
            ),
            patch(
                "temporalio.activity.info",
                return_value=MagicMock(activity_id="activity-id"),
            ),
            patch(
                "mistralai.workflows.plugins.mistralai.connectors.mcp_apps.create_base_event_fields",
                return_value={
                    "event_id": "event-id",
                    "root_workflow_exec_id": "workflow-id",
                    "parent_workflow_exec_id": None,
                    "workflow_exec_id": "workflow-id",
                    "workflow_run_id": "run-id",
                    "workflow_name": "workflow-name",
                },
            ),
        ):
            mock_client = AsyncMock()
            mock_client.beta.connectors.call_tool_async.return_value = response
            mock_get_client.return_value = mock_client

            await connector_tool_call.__wrapped__(
                connector_id_or_name="mcp_apps_test",
                tool_name="debug-tool",
                arguments={"contentType": "text"},
                mcp_ui_resource_uri="ui://debug/app",
            )

        mock_client.beta.connectors.list_tools_async.assert_not_called()
        assert publisher.publish_event_background.call_count == 2

        # The started event is emitted before the tool runs, so it carries no result.
        started_event = publisher.publish_event_background.call_args_list[0].args[0]
        assert isinstance(started_event, CustomTaskStarted)
        assert started_event.attributes.custom_task_type == "mcp_app"
        # The task id is the activity id (stable across retries), so a retried
        # call reconciles onto a single card rather than one card per attempt.
        assert started_event.attributes.custom_task_id == "activity-id"
        assert started_event.attributes.payload.value == {
            "uri": "ui://debug/app",
            "connector_id": "mcp_apps_test",
            "tool_name": "debug-tool",
            "tool_arguments": {"contentType": "text"},
        }

        # The completed event carries the trimmed result (text blocks + metadata).
        completed_event = publisher.publish_event_background.call_args_list[1].args[0]
        assert isinstance(completed_event, CustomTaskCompleted)
        assert completed_event.attributes.custom_task_id == started_event.attributes.custom_task_id
        assert completed_event.attributes.payload.value == {
            "uri": "ui://debug/app",
            "connector_id": "mcp_apps_test",
            "tool_name": "debug-tool",
            "tool_arguments": {"contentType": "text"},
            "tool_result": {
                "content": response.model_dump(serialize_as_any=True)["content"],
                "metadata": response.model_dump(serialize_as_any=True)["metadata"],
            },
        }

    @pytest.mark.asyncio
    async def test_connector_tool_call_emits_failed_on_error(self) -> None:
        publisher = MagicMock()
        response = _make_response(text="boom", is_error=True)

        with (
            patch("mistralai.workflows.plugins.mistralai.connectors.activities.get_mistral_client") as mock_get_client,
            patch(
                "mistralai.workflows.plugins.mistralai.connectors.mcp_apps.BackgroundEventPublisher.get_current",
                return_value=publisher,
            ),
            patch(
                "temporalio.activity.info",
                return_value=MagicMock(activity_id="activity-id"),
            ),
            patch(
                "mistralai.workflows.plugins.mistralai.connectors.mcp_apps.create_base_event_fields",
                return_value={
                    "event_id": "event-id",
                    "root_workflow_exec_id": "workflow-id",
                    "parent_workflow_exec_id": None,
                    "workflow_exec_id": "workflow-id",
                    "workflow_run_id": "run-id",
                    "workflow_name": "workflow-name",
                },
            ),
        ):
            mock_client = AsyncMock()
            mock_client.beta.connectors.call_tool_async.return_value = response
            mock_get_client.return_value = mock_client

            with pytest.raises(ConnectorToolCallError):
                await connector_tool_call.__wrapped__(
                    connector_id_or_name="mcp_apps_test",
                    tool_name="debug-tool",
                    mcp_ui_resource_uri="ui://debug/app",
                )

        # Started (before the call) then Failed (so the panel does not hang on "running").
        assert publisher.publish_event_background.call_count == 2
        started_event = publisher.publish_event_background.call_args_list[0].args[0]
        failed_event = publisher.publish_event_background.call_args_list[1].args[0]
        assert isinstance(started_event, CustomTaskStarted)
        assert isinstance(failed_event, CustomTaskFailed)
        assert failed_event.attributes.custom_task_id == started_event.attributes.custom_task_id
        assert failed_event.attributes.custom_task_type == "mcp_app"


# Mirrors ts/packages/integrations-api-client/src/integrations/mcp/ui-resource.test.ts
# (getToolUiResourceUri / getToolVisibility) — keep the two in sync.
class TestMcpAppUriExtraction:
    def test_modern_resource_uri(self) -> None:
        tool = {"name": "t", "_meta": {"ui": {"resourceUri": "ui://app/component"}}}
        assert _get_tool_definition_ui_resource_uri(tool) == "ui://app/component"

    def test_legacy_resource_uri_key(self) -> None:
        tool = {"name": "t", "_meta": {"ui/resourceUri": "ui://flights/app.html"}}
        assert _get_tool_definition_ui_resource_uri(tool) == "ui://flights/app.html"

    def test_snake_case_resource_uri(self) -> None:
        tool = {"name": "t", "_meta": {"ui": {"resource_uri": "ui://app/snake"}}}
        assert _get_tool_definition_ui_resource_uri(tool) == "ui://app/snake"

    def test_missing_meta_returns_none(self) -> None:
        assert _get_tool_definition_ui_resource_uri({"name": "t"}) is None
        assert _get_tool_definition_ui_resource_uri({"name": "t", "_meta": {}}) is None

    def test_non_ui_scheme_returns_none(self) -> None:
        tool = {"name": "t", "_meta": {"ui": {"resourceUri": "https://example.com/x"}}}
        assert _get_tool_definition_ui_resource_uri(tool) is None

    def test_empty_resource_uri_returns_none(self) -> None:
        tool = {"name": "t", "_meta": {"ui": {"resourceUri": ""}}}
        assert _get_tool_definition_ui_resource_uri(tool) is None


class TestMcpAppVisibility:
    def test_absent_visibility_defaults_to_app_visible(self) -> None:
        assert _is_tool_app_visible({"name": "t"}) is True
        assert _is_tool_app_visible({"name": "t", "_meta": {"ui": {}}}) is True

    def test_visibility_including_app_is_visible(self) -> None:
        tool = {"name": "t", "_meta": {"ui": {"visibility": ["model", "app"]}}}
        assert _is_tool_app_visible(tool) is True

    def test_model_only_visibility_is_not_app_visible(self) -> None:
        tool = {"name": "t", "_meta": {"ui": {"visibility": ["model"]}}}
        assert _is_tool_app_visible(tool) is False

    def test_malformed_visibility_defaults_to_visible(self) -> None:
        tool = {"name": "t", "_meta": {"ui": {"visibility": "model"}}}
        assert _is_tool_app_visible(tool) is True

    def test_collect_skips_model_only_tools(self) -> None:
        tools = [
            {"name": "app-tool", "_meta": {"ui": {"resourceUri": "ui://a/app"}}},
            {
                "name": "model-only",
                "_meta": {"ui": {"resourceUri": "ui://m/app", "visibility": ["model"]}},
            },
        ]
        assert _collect_declared_mcp_app_uris(tools) == {"app-tool": "ui://a/app"}


class TestTrimMcpAppToolResult:
    def test_keeps_text_blocks_and_metadata(self) -> None:
        result = {
            "content": [
                {"type": "text", "text": "hello"},
                {"type": "image", "data": "..."},
                {"type": "resource", "resource": {"uri": "ui://x"}},
            ],
            "metadata": {"isError": False},
        }
        assert _trim_mcp_app_tool_result(result) == {
            "content": [{"type": "text", "text": "hello"}],
            "metadata": {"isError": False},
        }

    def test_handles_missing_or_non_list_content(self) -> None:
        assert _trim_mcp_app_tool_result({}) == {"content": []}
        assert _trim_mcp_app_tool_result({"content": None}) == {"content": []}
