"""Flatten Windsurf/Cascade hook payloads onto the dispatcher's field names.

Cascade sends every event as ``{agent_action_name, trajectory_id, execution_id,
timestamp, model_name, tool_info{...}}`` -- the per-event detail is nested under
``tool_info`` and the session is identified by ``trajectory_id``. The dispatcher
and relay expect the flat Claude-shaped fields (``hook_event_name``,
``session_id``, ``tool_name``, ``tool_input``, ``file_path``, ``command``), so
adapt once at entry instead of teaching every handler the nested shape.

Original keys are preserved: the backend normalizer reads the native Cascade
fields off the forwarded payload.
"""

from __future__ import annotations

from typing import Any

# Canonical MCP tool-name shape shared with every other hook client, synthesized
# from Cascade's separate server/tool fields.
_MCP_TOOL_NAME_TEMPLATE = "mcp__{server}__{tool}"


def _str_field(source: dict[str, Any], key: str) -> str:
    value = source.get(key)
    return value if isinstance(value, str) else ""


def windsurf_mcp_tool_name(server_name: str, tool_name: str) -> str:
    """``mcp__<server>__<tool>``, or empty when either half is missing."""
    if not (server_name and tool_name):
        return ""
    return _MCP_TOOL_NAME_TEMPLATE.format(server=server_name, tool=tool_name)


def adapt_windsurf_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Return *payload* with flat dispatcher fields added.

    Never overwrites a field the payload already carries, so a future Cascade
    release that emits flat names wins over the derived value.
    """
    adapted = dict(payload)
    tool_info = payload.get("tool_info")
    if not isinstance(tool_info, dict):
        tool_info = {}

    event_name = _str_field(payload, "agent_action_name")
    trajectory_id = _str_field(payload, "trajectory_id")

    derived: dict[str, Any] = {}
    if event_name:
        derived["hook_event_name"] = event_name
    if trajectory_id:
        derived["session_id"] = trajectory_id
        derived["conversation_id"] = trajectory_id

    model_name = _str_field(payload, "model_name")
    if model_name:
        derived["model"] = model_name

    mcp_tool = windsurf_mcp_tool_name(
        _str_field(tool_info, "mcp_server_name"),
        _str_field(tool_info, "mcp_tool_name"),
    )
    if mcp_tool:
        derived["tool_name"] = mcp_tool
        derived["mcp_server_name"] = _str_field(tool_info, "mcp_server_name")
        arguments = tool_info.get("mcp_tool_arguments")
        if isinstance(arguments, dict):
            derived["tool_input"] = arguments
        if "mcp_result" in tool_info:
            derived["tool_response"] = tool_info["mcp_result"]

    command_line = _str_field(tool_info, "command_line")
    if command_line:
        derived["command"] = command_line
    if event_name == "pre_run_command":
        derived["tool_name"] = "BeforeShellExecution"
        derived["tool_input"] = {"command": command_line}

    file_path = _str_field(tool_info, "file_path")
    if file_path:
        derived["file_path"] = file_path
    if event_name == "pre_read_code":
        derived["tool_name"] = "BeforeReadFile"
        derived["tool_input"] = {"file_path": file_path}

    user_prompt = _str_field(tool_info, "user_prompt")
    if user_prompt:
        derived["prompt"] = user_prompt

    response = _str_field(tool_info, "response")
    if response:
        derived["response"] = response
        # The Stop normalizer reads ``last_assistant_message``; without this the
        # turn-end event carries no data at all.
        derived["last_assistant_message"] = response

    transcript_path = _str_field(tool_info, "transcript_path")
    if transcript_path:
        derived["transcript_path"] = transcript_path

    cwd = _str_field(tool_info, "cwd")
    if cwd:
        derived["cwd"] = cwd

    for key, value in derived.items():
        adapted.setdefault(key, value)
    return adapted
