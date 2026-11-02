"""Sandbox tool and permission helpers for direct Agent API transport."""

from __future__ import annotations

import json

from .types import _ToolUseData


def _permission_input_for_tool(tool_use: _ToolUseData) -> dict[str, str]:
    lower = _normalize_tool_name(tool_use.name)
    tool_input = tool_use.input
    if lower == "bash":
        return {"action": "execute_command", "resource": str(tool_input.get("command") or "")}
    if lower == "read":
        return {
            "action": "read_file",
            "resource": str(tool_input.get("file_path") or tool_input.get("path") or ""),
        }
    if lower == "write":
        return {
            "action": "write_file",
            "resource": str(tool_input.get("file_path") or tool_input.get("path") or ""),
        }
    if lower == "edit":
        return {
            "action": "edit_file",
            "resource": str(tool_input.get("file_path") or tool_input.get("path") or ""),
        }
    return {"action": "use_tool", "resource": json.dumps(tool_input)}

def _local_tool_execution_error(tool_use: _ToolUseData) -> dict[str, str]:
    return {
        "content": (
            f"Tool {tool_use.name} cannot run locally in API mode. Enable "
            "snowflake_sandbox for server-side tool execution."
        )
    }

def _display_tool_name(name: str) -> str:
    mapping = {
        "bash": "Bash",
        "read": "Read",
        "write": "Write",
        "edit": "Edit",
        "grep": "Grep",
        "glob": "Glob",
    }
    return mapping.get(_normalize_tool_name(name), name)

def _normalize_tool_name(name: str) -> str:
    return name.lower()
