"""Serialize/deserialize ToolDefinitions via cloudpickle.

Agent-specific integrations (MCP server for Claude Code, OpenHands bridge)
live in their respective agent packages.
"""

from __future__ import annotations

import logging
from pathlib import Path

import cloudpickle

from plato.tools.definition import ToolDefinition, set_workspace

logger = logging.getLogger(__name__)


def save_tools(tools: list[ToolDefinition], path: str | Path) -> Path:
    """Pickle tools to a file.

    Args:
        tools: Tool definitions with handlers to serialize.
        path: Output file path.

    Returns:
        Absolute path to the written file.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "wb") as f:
        cloudpickle.dump(tools, f)
    logger.info("Saved %d tools to %s", len(tools), path)

    return path


def load_tools(path: str | Path, workspace: str | Path = "/workspace") -> list[ToolDefinition]:
    """Load pickled tool definitions.

    Args:
        path: Path to the pickled tools file.
        workspace: Workspace directory path for get_workspace() resolution.

    Returns:
        List of ToolDefinitions with callable handlers.

    Raises:
        FileNotFoundError: If the tools file doesn't exist.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"No tools file found at {path}")

    set_workspace(workspace)

    with open(path, "rb") as f:
        tools = cloudpickle.load(f)

    logger.info("Loaded %d tools from %s (workspace=%s)", len(tools), path, workspace)
    return tools
