"""Claude Code's PluginInstaller ledger: installed_plugins.json."""

from __future__ import annotations
import json
import os
from pathlib import Path


def claude_plugin_ledger(env: "dict[str, str] | None" = None) -> Path:
    """Claude Code's install ledger, `installed_plugins.json`: the record its
    `plugin list` reads: `PROBE_INSTALLED_PLUGINS_JSON` first, then Claude
    Code's own plugins folder, which `CLAUDE_CODE_PLUGIN_CACHE_DIR` moves, else
    `CLAUDE_CONFIG_DIR` or `~/.claude`, then `plugins/`. The one answer:
    `versions.py` grades the plugin's version off the same file, and the root
    skills read it (`root_skills.installed_plugin_root`)."""
    values = os.environ if env is None else env
    override = (values.get("PROBE_INSTALLED_PLUGINS_JSON") or "").strip()
    if override:
        return Path(override)
    moved = (values.get("CLAUDE_CODE_PLUGIN_CACHE_DIR") or "").strip()
    if moved:
        return Path(moved).expanduser() / "installed_plugins.json"
    home = (values.get("CLAUDE_CONFIG_DIR") or "").strip()
    return (Path(home).expanduser() if home else Path.home() / ".claude") / "plugins" / "installed_plugins.json"


def _claude_ledger_ids() -> list[str]:
    """Every `<plugin>@<marketplace>` the ledger holds an install for. A missing
    ledger is Claude Code with nothing installed; an unreadable one raises."""
    try:
        raw = json.loads(claude_plugin_ledger().read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    plugins = raw.get("plugins") if isinstance(raw, dict) else None
    if not isinstance(plugins, dict):
        raise ValueError("no `plugins` table")
    return [key for key, entries in plugins.items() if isinstance(key, str) and entries]
