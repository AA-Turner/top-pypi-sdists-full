"""In-repo Claude plugin catalog for SAGE runtime.

This loader uses a vendored snapshot file committed in the SAGE repo so runtime
capabilities do not require reading ~/.codex/plugins or any external directory.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CLAUDE_PLUGIN_SNAPSHOT_PATH = Path(__file__).with_name("claude_plugins_snapshot.json")


def load_claude_plugin_snapshot() -> dict[str, Any]:
    """Load the vendored Claude plugin snapshot from the repository."""
    if not CLAUDE_PLUGIN_SNAPSHOT_PATH.exists():
        return {"plugins": []}
    try:
        raw = CLAUDE_PLUGIN_SNAPSHOT_PATH.read_text(encoding="utf-8")
        parsed = json.loads(raw)
        if isinstance(parsed, dict) and isinstance(parsed.get("plugins"), list):
            return parsed
    except Exception:
        return {"plugins": []}
    return {"plugins": []}


def iter_claude_plugin_groups() -> list[dict[str, Any]]:
    """Return top-level plugin groups from the vendored snapshot."""
    snapshot = load_claude_plugin_snapshot()
    groups = snapshot.get("plugins", [])
    return [group for group in groups if isinstance(group, dict)]


def iter_claude_skills() -> list[dict[str, Any]]:
    """Flatten snapshot plugin groups into skill records."""
    records: list[dict[str, Any]] = []
    for group in iter_claude_plugin_groups():
        plugin_name = str(group.get("name", "")).strip()
        plugin_description = str(group.get("description", "")).strip()
        skills = group.get("skills", [])
        if not isinstance(skills, list):
            continue
        for skill in skills:
            if not isinstance(skill, dict):
                continue
            record = {
                "plugin_name": plugin_name,
                "plugin_description": plugin_description,
                "skill_name": str(skill.get("skill", "")).strip(),
                "description": str(skill.get("description", "")).strip(),
                "default_prompt": str(skill.get("default_prompt", "")).strip(),
                "instruction_markdown": str(skill.get("instruction_markdown", "")).strip(),
                "source_file": str(skill.get("source_file", "")).strip(),
                "workflow_steps": [
                    str(step).strip()
                    for step in skill.get("workflow_steps", [])
                    if str(step).strip()
                ],
            }
            if record["plugin_name"] and record["skill_name"]:
                records.append(record)
    return records


def iter_claude_capabilities() -> list[dict[str, Any]]:
    """Flatten snapshot plugin groups into capability records.

    Skill names are preserved for backward compatibility.
    Command, agent, and MCP capabilities are prefixed to avoid collisions:
    - command.<name>
    - agent.<name>
    - mcp.<server>
    """
    records: list[dict[str, Any]] = []
    for group in iter_claude_plugin_groups():
        plugin_name = str(group.get("name", "")).strip()
        plugin_description = str(group.get("description", "")).strip()
        if not plugin_name:
            continue

        skills = group.get("skills", [])
        if isinstance(skills, list):
            for skill in skills:
                if not isinstance(skill, dict):
                    continue
                skill_name = str(skill.get("skill", "")).strip()
                if not skill_name:
                    continue
                records.append(
                    {
                        "plugin_name": plugin_name,
                        "plugin_description": plugin_description,
                        "capability_type": "skill",
                        "capability_name": skill_name,
                        "description": str(skill.get("description", "")).strip(),
                        "default_prompt": str(skill.get("default_prompt", "")).strip(),
                        "instruction_markdown": str(skill.get("instruction_markdown", "")).strip(),
                        "source_file": str(skill.get("source_file", "")).strip(),
                        "workflow_steps": [
                            str(step).strip()
                            for step in skill.get("workflow_steps", [])
                            if str(step).strip()
                        ],
                    }
                )

        commands = group.get("commands", [])
        if isinstance(commands, list):
            for command in commands:
                if not isinstance(command, dict):
                    continue
                command_name = str(command.get("command", "")).strip()
                if not command_name:
                    continue
                records.append(
                    {
                        "plugin_name": plugin_name,
                        "plugin_description": plugin_description,
                        "capability_type": "command",
                        "capability_name": f"command.{command_name}",
                        "description": str(command.get("description", "")).strip(),
                        "instruction_markdown": str(
                            command.get("instruction_markdown", "")
                        ).strip(),
                        "source_file": str(command.get("source_file", "")).strip(),
                        "workflow_steps": [
                            str(step).strip()
                            for step in command.get("workflow_steps", [])
                            if str(step).strip()
                        ],
                    }
                )

        agents = group.get("agents", [])
        if isinstance(agents, list):
            for agent in agents:
                if not isinstance(agent, dict):
                    continue
                agent_name = str(agent.get("agent", "")).strip()
                if not agent_name:
                    continue
                records.append(
                    {
                        "plugin_name": plugin_name,
                        "plugin_description": plugin_description,
                        "capability_type": "agent",
                        "capability_name": f"agent.{agent_name}",
                        "description": str(agent.get("description", "")).strip(),
                        "default_prompt": str(agent.get("default_prompt", "")).strip(),
                        "instruction_markdown": str(agent.get("instruction_markdown", "")).strip(),
                        "source_file": str(agent.get("source_file", "")).strip(),
                    }
                )

        mcp_servers = group.get("mcp_servers", [])
        if isinstance(mcp_servers, list):
            for server in mcp_servers:
                if not isinstance(server, dict):
                    continue
                server_name = str(server.get("server", "")).strip()
                if not server_name:
                    continue
                records.append(
                    {
                        "plugin_name": plugin_name,
                        "plugin_description": plugin_description,
                        "capability_type": "mcp",
                        "capability_name": f"mcp.{server_name}",
                        "description": str(server.get("description", "")).strip(),
                        "transport": str(server.get("transport", "")).strip(),
                        "url": str(server.get("url", "")).strip(),
                        "command": str(server.get("command", "")).strip(),
                        "args": [str(arg) for arg in server.get("args", []) if str(arg).strip()],
                    }
                )
    return records


__all__ = [
    "CLAUDE_PLUGIN_SNAPSHOT_PATH",
    "iter_claude_capabilities",
    "iter_claude_plugin_groups",
    "iter_claude_skills",
    "load_claude_plugin_snapshot",
]
