"""MCP App annotation helpers for session workflow task entries."""

from typing import Final, Literal

from pydantic import BaseModel, ConfigDict, JsonValue, field_validator

from mistralai.vibe_agents.session_workflow.annotations import annotations_for
from mistralai.vibe_agents.session_workflow.commands import JsonObject

MCP_APP_ANNOTATION_KEY: Final[Literal["mcp_app"]] = "mcp_app"
MCP_INTEGRATION_ANNOTATION_KEY: Final[Literal["integration"]] = "integration"


class _McpAppModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        validate_by_alias=True,
        validate_by_name=True,
    )


class McpAppToolTextContent(_McpAppModel):
    type: Literal["text"] = "text"
    text: str


class McpAppToolResult(_McpAppModel):
    content: list[McpAppToolTextContent]
    metadata: dict[str, JsonValue] | None = None


class McpAppToolMetadata(_McpAppModel):
    uri: str
    connector_id: str
    tool_result: McpAppToolResult | None = None

    @field_validator("uri")
    @classmethod
    def _validate_ui_uri(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped.startswith("ui://") or len(stripped) == len("ui://"):
            raise ValueError("MCP app uri must start with 'ui://'")
        return stripped

    @field_validator("connector_id")
    @classmethod
    def _validate_connector_id(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("connector_id must be non-empty")
        return stripped


class McpIntegrationMetadata(_McpAppModel):
    id: str
    name: str
    display_name: str | None = None
    icon_url: str | None = None

    @field_validator("id", "name")
    @classmethod
    def _validate_non_empty(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("integration identity fields must be non-empty")
        return stripped


def mcp_app_annotations(
    *,
    uri: str,
    connector_id: str,
    tool_result: McpAppToolResult | JsonObject | None = None,
) -> JsonObject:
    metadata = McpAppToolMetadata(uri=uri, connector_id=connector_id, tool_result=tool_result)
    return annotations_for(MCP_APP_ANNOTATION_KEY, metadata, exclude_none=True)


def mcp_integration_annotations(metadata: McpIntegrationMetadata | None) -> JsonObject:
    if metadata is None:
        return {}
    return annotations_for(MCP_INTEGRATION_ANNOTATION_KEY, metadata, exclude_none=True)


def mcp_app_metadata_from_annotations(annotations: JsonObject | None) -> McpAppToolMetadata | None:
    if annotations is None:
        return None
    raw = annotations.get(MCP_APP_ANNOTATION_KEY)
    if raw is None:
        return None
    return McpAppToolMetadata.model_validate(raw)


__all__ = [
    "MCP_APP_ANNOTATION_KEY",
    "MCP_INTEGRATION_ANNOTATION_KEY",
    "McpAppToolMetadata",
    "McpAppToolResult",
    "McpAppToolTextContent",
    "McpIntegrationMetadata",
    "mcp_app_annotations",
    "mcp_app_metadata_from_annotations",
    "mcp_integration_annotations",
]
