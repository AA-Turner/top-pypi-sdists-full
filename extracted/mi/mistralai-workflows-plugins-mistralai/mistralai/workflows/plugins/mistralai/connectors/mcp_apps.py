"""MCP app discovery and event helpers for connector tool calls."""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Any

import structlog
import temporalio.activity

from mistralai.workflows.client import get_mistral_client
from mistralai.workflows.core._events.event_context import BackgroundEventPublisher
from mistralai.workflows.core._events.event_utils import create_base_event_fields
from mistralai.workflows.core.activity import activity
from mistralai.workflows.plugins.mistralai.connectors.run_as import ConnectorRunAs, use_executor_credentials_for
from mistralai.workflows.protocol.v1.events import (
    CustomTaskCompleted,
    CustomTaskCompletedAttributes,
    CustomTaskFailed,
    CustomTaskFailedAttributes,
    CustomTaskStarted,
    CustomTaskStartedAttributes,
    Failure,
    JSONPayload,
)

logger = structlog.get_logger(__name__)

_APP_VISIBILITY = "app"
_MCP_UI_URI_SCHEME = "ui://"
_MCP_APP_TASK_TYPE = "mcp_app"


@dataclass(frozen=True)
class McpAppCallEvents:
    publisher: BackgroundEventPublisher
    task_id: str
    uri: str
    connector_id: str
    tool_name: str
    arguments: dict[str, Any] | None


def _dump_model(value: Any) -> dict[str, Any]:
    dumped = value.model_dump(serialize_as_any=True)
    return dumped if isinstance(dumped, dict) else {}


def _get_tool_meta(tool: dict[str, Any]) -> dict[str, Any] | None:
    meta = tool.get("_meta")
    if meta is None:
        meta = tool.get("meta")
    return meta if isinstance(meta, dict) else None


# Mirror of `getToolUiResourceUri` in
# ts/packages/integrations-api-client/src/integrations/mcp/ui-resource.ts.
# Both must agree on the `_meta.ui.resourceUri` contract (with the legacy
# `_meta["ui/resourceUri"]` fallback and `ui://` scheme validation).
def _get_tool_definition_ui_resource_uri(tool: dict[str, Any]) -> str | None:
    meta = _get_tool_meta(tool)
    if meta is None:
        return None

    ui = meta.get("ui")
    uri = ui.get("resourceUri") if isinstance(ui, dict) else None
    if uri is None:
        uri = ui.get("resource_uri") if isinstance(ui, dict) else None
    if uri is None:
        uri = meta.get("ui/resourceUri")

    if not isinstance(uri, str) or not uri.startswith(_MCP_UI_URI_SCHEME):
        return None

    return uri


# a tool is app-visible unless it declares an explicit `_meta.ui.visibility`
# list that omits "app".
def _is_tool_app_visible(tool: dict[str, Any]) -> bool:
    meta = _get_tool_meta(tool)
    ui = meta.get("ui") if meta else None
    visibility = ui.get("visibility") if isinstance(ui, dict) else None
    if not isinstance(visibility, list):
        return True
    return _APP_VISIBILITY in visibility


def _get_tool_name(tool: dict[str, Any]) -> str | None:
    name = tool.get("name")
    return name if isinstance(name, str) else None


def _collect_declared_mcp_app_uris(tools: Any) -> dict[str, str]:
    output: dict[str, str] = {}
    for tool in tools:
        if hasattr(tool, "model_dump"):
            tool_data = _dump_model(tool)
        elif isinstance(tool, dict):
            tool_data = tool
        else:
            continue

        tool_name = _get_tool_name(tool_data)
        if tool_name is None:
            continue

        uri = _get_tool_definition_ui_resource_uri(tool_data)
        if uri is not None and _is_tool_app_visible(tool_data):
            output[tool_name] = uri

    return output


@activity(
    name="__internal__connector_get_mcp_app_resource_uris",
    start_to_close_timeout=datetime.timedelta(seconds=30),
    _allow_reserved_name=True,
)
async def connector_get_mcp_app_resource_uris(
    connector_id_or_name: str,
    credentials_name: str | None = None,
    raise_on_error: bool = False,
    run_as: ConnectorRunAs = ConnectorRunAs.AUTO,
) -> dict[str, str]:
    """Return tool-name to ``ui://`` URI mappings declared by MCP tool metadata."""
    client = get_mistral_client(use_executor_credentials=use_executor_credentials_for(run_as))
    try:
        response = await client.beta.connectors.list_tools_async(
            connector_id_or_name=connector_id_or_name,
            credentials_name=credentials_name,
        )
    except Exception as e:
        logger.warning(
            "Failed to list connector tools for MCP app metadata",
            connector_id_or_name=connector_id_or_name,
            credentials_name=credentials_name,
            error=str(e),
        )
        if raise_on_error:
            raise
        return {}

    uris = _collect_declared_mcp_app_uris(response or [])
    logger.info(
        "Collected connector MCP app resource URIs",
        connector_id_or_name=connector_id_or_name,
        credentials_name=credentials_name,
        tool_names=list(uris),
        uri_count=len(uris),
    )
    return uris


def _trim_mcp_app_tool_result(result: dict[str, Any]) -> dict[str, Any]:
    """Keep only what the client renders: text content blocks + metadata."""
    content = result.get("content")
    text_blocks = (
        [block for block in content if isinstance(block, dict) and block.get("type") == "text"]
        if isinstance(content, list)
        else []
    )
    tool_result: dict[str, Any] = {"content": text_blocks}
    if isinstance(result.get("metadata"), dict):
        tool_result["metadata"] = result["metadata"]
    return tool_result


def _mcp_app_payload(
    *,
    uri: str,
    connector_id: str,
    tool_name: str,
    arguments: dict[str, Any] | None,
    tool_result: dict[str, Any] | None,
) -> JSONPayload:
    value: dict[str, Any] = {
        "uri": uri,
        "connector_id": connector_id,
        "tool_name": tool_name,
        "tool_arguments": arguments,
    }
    if tool_result is not None:
        value["tool_result"] = tool_result
    return JSONPayload(value=value)


def start_mcp_app_call_events(
    *,
    uri: str | None,
    connector_id: str,
    tool_name: str,
    arguments: dict[str, Any] | None,
) -> McpAppCallEvents | None:
    if not uri:
        return None

    publisher = BackgroundEventPublisher.get_current()
    if publisher is None:
        return None

    call_events = McpAppCallEvents(
        publisher=publisher,
        task_id=temporalio.activity.info().activity_id,
        uri=uri,
        connector_id=connector_id,
        tool_name=tool_name,
        arguments=arguments,
    )
    _emit_mcp_app_started(call_events)
    return call_events


def complete_mcp_app_call_events(call_events: McpAppCallEvents | None, result: Any) -> None:
    if call_events is None:
        return

    call_events.publisher.publish_event_background(
        CustomTaskCompleted(
            **create_base_event_fields(),
            attributes=CustomTaskCompletedAttributes(
                custom_task_id=call_events.task_id,
                custom_task_type=_MCP_APP_TASK_TYPE,
                payload=_mcp_app_payload(
                    uri=call_events.uri,
                    connector_id=call_events.connector_id,
                    tool_name=call_events.tool_name,
                    arguments=call_events.arguments,
                    tool_result=_trim_mcp_app_tool_result(_dump_model(result)),
                ),
            ),
        )
    )


def fail_mcp_app_call_events(call_events: McpAppCallEvents | None, message: str) -> None:
    if call_events is None:
        return

    call_events.publisher.publish_event_background(
        CustomTaskFailed(
            **create_base_event_fields(),
            attributes=CustomTaskFailedAttributes(
                custom_task_id=call_events.task_id,
                custom_task_type=_MCP_APP_TASK_TYPE,
                failure=Failure(message=message),
            ),
        )
    )


def _emit_mcp_app_started(call_events: McpAppCallEvents) -> None:
    call_events.publisher.publish_event_background(
        CustomTaskStarted(
            **create_base_event_fields(),
            attributes=CustomTaskStartedAttributes(
                custom_task_id=call_events.task_id,
                custom_task_type=_MCP_APP_TASK_TYPE,
                payload=_mcp_app_payload(
                    uri=call_events.uri,
                    connector_id=call_events.connector_id,
                    tool_name=call_events.tool_name,
                    arguments=call_events.arguments,
                    tool_result=None,
                ),
            ),
        )
    )
