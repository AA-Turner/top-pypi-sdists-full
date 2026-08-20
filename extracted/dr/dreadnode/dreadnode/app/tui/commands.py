"""Slash command registry for the Dreadnode TUI.

Historically this module was a grab-bag of four unrelated concerns: slash
commands, auth helpers, wire-event parsing, and tool display formatting.
Those have been split out:

- wire-event parsing lives in :mod:`dreadnode.app.tui.wire_events`
- auth helpers and in-memory profile state live in
  :mod:`dreadnode.app.tui.auth_flow`
- tool-label formatting and result summarization live in
  :mod:`dreadnode.app.tui.tool_format`

What's left here is just the static slash command registry. The
CommandDispatcher extraction (task #3 in the refactor plan) will eventually
move these definitions alongside the dispatch logic.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SlashCommand:
    """A TUI slash command definition."""

    name: str
    description: str
    hint: str = ""


SLASH_COMMANDS: list[SlashCommand] = [
    SlashCommand("/help", "Show available commands"),
    SlashCommand("/new", "Create a new session"),
    SlashCommand("/clear", "Alias for /new"),
    SlashCommand("/sessions", "List all sessions"),
    SlashCommand("/agents", "List loaded agents"),
    SlashCommand("/agent", "Start agent session", "<name>"),
    SlashCommand("/model", "Get or set model", "[provider/model]"),
    SlashCommand("/reload", "Re-discover capabilities and rebuild registry"),
    SlashCommand(
        "/login", "Authenticate with platform (restarts runtime)", "[api-key] [--server <url>]"
    ),
    SlashCommand("/logout", "Disconnect and revoke credentials"),
    SlashCommand("/whoami", "Show current identity"),
    SlashCommand("/profile", "Switch profile"),
    SlashCommand("/workspace", "View or switch workspace (restarts runtime)", "[key]"),
    SlashCommand("/workspaces", "List workspaces"),
    SlashCommand("/projects", "List projects", "[workspace]"),
    SlashCommand("/models", "Browse models"),
    SlashCommand("/pull", "Pull a Hub artifact into local cache", "<type://[org/]name[@version]>"),
    SlashCommand("/thinking", "Toggle thinking/reasoning effort", "[on|off|low|medium|high|max]"),
    SlashCommand("/runtimes", "View workspace interactive runtimes"),
    SlashCommand("/environments", "Browse available environments"),
    SlashCommand("/capabilities", "Manage runtime capabilities"),
    SlashCommand("/skills", "Browse and load skills"),
    SlashCommand("/mcp", "View background services (MCP servers, workers)"),
    SlashCommand("/workers", "View background services (MCP servers, workers)"),
    SlashCommand("/secrets", "View configured secrets and provider presets"),
    SlashCommand("/compact", "Compact conversation history", "[guidance]"),
    SlashCommand("/rewind", "Rewind to a previous user message"),
    SlashCommand("/auto", "Engage autonomous mode for this session", "[max_steps]"),
    SlashCommand("/interactive", "Restore interactive mode for this session"),
    SlashCommand("/policy", "Swap session policy", "<name> [k=v ...]"),
    SlashCommand("/background", "Launch a task in a new autonomous session", "<task>"),
    SlashCommand("/bg", "Alias for /background", "<task>"),
    SlashCommand("/rename", "Rename current session", "<title>"),
    SlashCommand("/tools", "Set tool details mode", "<compact|expanded>"),
    SlashCommand("/export", "Export session transcript", "[filename]"),
    SlashCommand("/traces", "Browse traces for current project"),
    SlashCommand("/spans", "Browse raw local spans for the active session"),
    SlashCommand("/sandboxes", "Monitor your sandboxes"),
    SlashCommand("/evaluations", "View workspace evaluation jobs"),
    SlashCommand("/console", "View backend logs"),
    SlashCommand("/report-bug", "Create a privacy-reviewed diagnostic report"),
    SlashCommand("/copy", "Copy last assistant message (or press y)"),
    SlashCommand("/version", "Show installed Dreadnode version"),
    SlashCommand("/update", "Update Dreadnode CLI to latest version"),
    SlashCommand("/quit", "Exit the TUI"),
]
