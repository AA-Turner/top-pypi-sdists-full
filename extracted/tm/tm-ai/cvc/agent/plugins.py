"""
cvc.agent.plugins — Plugin system for CVC Agent.

Plugin directory structure:
    plugin-name/
    ├── .cvc-plugin/
    │   └── plugin.json    # name, version, description
    ├── commands/           # Slash commands (.md files)
    ├── agents/             # Sub-agent definitions (.md files)
    ├── hooks/              # Hook scripts
    └── README.md

Discovery:
    - .cvc/plugins/ (project-level)
    - ~/.cvc/plugins/ (user-level)
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger("cvc.agent.plugins")


@dataclass
class PluginCommand:
    """A slash command defined by a plugin."""
    name: str
    description: str
    content: str  # Markdown content to inject as system message


@dataclass
class Plugin:
    """A loaded CVC plugin."""
    name: str
    version: str
    description: str
    path: Path
    commands: list[PluginCommand] = field(default_factory=list)
    agent_files: list[Path] = field(default_factory=list)
    hook_files: list[Path] = field(default_factory=list)
    enabled: bool = True


def discover_plugins(workspace: str | Path) -> list[Plugin]:
    """Discover and load plugins from project and user directories."""
    plugins = []
    search_dirs = [
        Path(workspace) / ".cvc" / "plugins",
        Path.home() / ".cvc" / "plugins",
    ]

    for search_dir in search_dirs:
        if not search_dir.is_dir():
            continue
        for plugin_dir in sorted(search_dir.iterdir()):
            if not plugin_dir.is_dir():
                continue
            plugin = _load_plugin(plugin_dir)
            if plugin:
                plugins.append(plugin)

    return plugins


def _load_plugin(plugin_dir: Path) -> Plugin | None:
    """Load a single plugin from its directory."""
    manifest = plugin_dir / ".cvc-plugin" / "plugin.json"
    if not manifest.exists():
        # Also check for a simpler manifest at the root
        manifest = plugin_dir / "plugin.json"
        if not manifest.exists():
            return None

    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except Exception as e:
        logger.warning("Failed to load plugin manifest %s: %s", manifest, e)
        return None

    plugin = Plugin(
        name=data.get("name", plugin_dir.name),
        version=data.get("version", "0.0.0"),
        description=data.get("description", ""),
        path=plugin_dir,
    )

    # Load commands
    commands_dir = plugin_dir / "commands"
    if commands_dir.is_dir():
        for cmd_file in sorted(commands_dir.glob("*.md")):
            content = cmd_file.read_text(encoding="utf-8")
            # Command name is the filename without extension, prefixed with /
            cmd_name = cmd_file.stem
            # First line of the file is treated as description
            lines = content.strip().splitlines()
            desc = lines[0].lstrip("# ").strip() if lines else cmd_name
            plugin.commands.append(PluginCommand(
                name=cmd_name,
                description=desc,
                content=content,
            ))

    # Discover agent files
    agents_dir = plugin_dir / "agents"
    if agents_dir.is_dir():
        plugin.agent_files = list(agents_dir.glob("*.md"))

    # Discover hook files
    hooks_dir = plugin_dir / "hooks"
    if hooks_dir.is_dir():
        plugin.hook_files = list(hooks_dir.glob("*"))

    logger.debug("Loaded plugin: %s v%s (%d commands)", plugin.name, plugin.version, len(plugin.commands))
    return plugin
