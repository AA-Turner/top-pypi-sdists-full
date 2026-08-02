"""Generation of the plugin hooks manifest (Claude's ``hooks/hooks.json``).

The Pysae Claude plugin declares its hooks in a ``hooks/hooks.json`` at the plugin root, which
Claude Code auto-discovers while the plugin is enabled. Each hook group is **gated on the embedded
tool that owns it**, so a hook ships only when the user selected that tool — mirroring the per-user
opt-in of the MCP manifest (a plugin firing every hook for everyone would tax each tool call). This
module is the single source of that file.
"""

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from ...config import get_tools_to_install
from ..registry import TOOLS
from .base import SHIM_BINARY

HOOKS_MANIFEST_NAME = "hooks.json"


@dataclass(frozen=True)
class HookGroup:
    """One plugin hook, gated on the embedded tool that owns it.

    ``command`` is the bare ``pysae-ai-tools`` subcommand, resolved on PATH at fire time exactly
    like the MCP shim. ``matcher`` is ``None`` for events that take no matcher (UserPromptSubmit,
    Stop)."""

    tool: str
    event: str
    matcher: str | None
    command: str
    timeout: int


HOOK_GROUPS: tuple[HookGroup, ...] = (
    HookGroup("usage-guard", "PreToolUse", "*", f"{SHIM_BINARY} usage hook", 10),
    HookGroup("usage-guard", "UserPromptSubmit", None, f"{SHIM_BINARY} usage prompt-hook", 10),
    HookGroup("activity-tracker", "PostToolUse", "Bash|Edit|Write|Skill|Agent|Read", f"{SHIM_BINARY} tracker hook", 5),
    HookGroup("activity-tracker", "Stop", None, f"{SHIM_BINARY} tracker stop-hook", 5),
    HookGroup("mcp-cleanup-hook", "SessionEnd", "", f"{SHIM_BINARY} tools mcp-cleanup schedule --delay 30", 5),
)


def gating_tool_names() -> set[str]:
    """Every embedded tool a hook group is gated on."""
    return {g.tool for g in HOOK_GROUPS}


def selected_hook_tool_names() -> set[str]:
    """Hook-owning tools whose hooks should ship in the plugin manifest.

    Those of the gating tools the user selected (saved selection), or — when no selection has been
    saved yet — the default-selected ones. Mirrors :func:`mcp_manifest.selected_mcp_server_names`."""
    saved = get_tools_to_install()
    selected: set[str] | None = set(saved) if saved else None
    gating = gating_tool_names()
    result: set[str] = set()
    for t in TOOLS:
        if t.name not in gating:
            continue
        if selected is None:
            if t.default_selected:
                result.add(t.name)
        elif t.name in selected:
            result.add(t.name)
    return result


def build_plugin_hooks_json(selected_tool_names: Iterable[str]) -> dict[str, Any]:
    """The ``hooks.json`` document declaring the hooks of the selected gating tools.

    Groups sharing an event are collected under it; ``matcher`` is omitted when ``None``."""
    selected = set(selected_tool_names)
    events: dict[str, list[dict[str, Any]]] = {}
    for g in HOOK_GROUPS:
        if g.tool not in selected:
            continue
        entry: dict[str, Any] = {"hooks": [{"type": "command", "command": g.command, "timeout": g.timeout}]}
        group = entry if g.matcher is None else {"matcher": g.matcher, **entry}
        events.setdefault(g.event, []).append(group)
    return {"hooks": events}
