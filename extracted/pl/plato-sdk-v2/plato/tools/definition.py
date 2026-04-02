"""ToolDefinition and workspace resolution for pickled tool handlers."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict

# Module-level workspace path used by world-hosted tool handlers at call time.
_workspace: Path = Path("/workspace")


def get_workspace() -> Path:
    """Get the current workspace path. Call this inside tool handlers instead of
    closing over a path that won't survive pickling across machines."""
    return _workspace


def set_workspace(path: str | Path) -> None:
    """Set the workspace path for this process."""
    global _workspace
    _workspace = Path(path)


class ToolDefinition(BaseModel):
    """A tool that can be pickled and passed from world to agent.

    Handlers should use get_workspace() for filesystem paths instead of
    closing over absolute paths, since paths differ between world and agent.

    Example::

        class ReadOutputInput(BaseModel):
            path: str = Field(description="File path to read")

        tool = ToolDefinition(
            name="read_output",
            description="Read the output file",
            input_model=ReadOutputInput,
            handler=my_handler,  # receives ReadOutputInput instance
        )
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    description: str
    input_schema: dict[str, Any] | None = None
    input_model: type[BaseModel] | None = None
    handler: Callable[..., Any]


def get_tool_input_schema(tool: ToolDefinition) -> dict[str, Any]:
    """Return the JSON schema exposed for a tool.

    Prefer ``input_model`` when present so the schema stays in sync with the
    typed runtime contract. Fall back to legacy ``input_schema`` support for
    pickled tool definitions used by the local stdio MCP bridge.
    """
    if tool.input_model is not None:
        return tool.input_model.model_json_schema()
    if tool.input_schema is not None:
        return tool.input_schema
    raise ValueError(f"Tool {tool.name!r} has neither input_model nor input_schema set")
