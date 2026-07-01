"""Render inline help content into the conversation view.

Triggered by `?` (empty composer) or `/help`. Writes directly into the
ConversationView — no separate panel widget, no scrolling issues.
"""

from __future__ import annotations

from rich.text import Text

from dreadnode.app.tui.commands import SLASH_COMMANDS
from dreadnode.app.tui.theme import ACCENT, BORDER_LIGHT, FG_MUTED, FG_SUBTLE
from dreadnode.app.tui.widgets.context_bar import PRICING_DOCS_URL

_CMD_LOOKUP = {cmd.name: cmd for cmd in SLASH_COMMANDS}

# Grouped for scannability — most useful first, one section per concern
_INPUT: list[tuple[str, str]] = [
    ("Enter", "send message"),
    ("Shift+Enter", "new line"),
    ("\\ + Enter", "new line"),
    ("/", "commands"),
    ("@", "mention agent"),
    ("!", "shell mode"),
    ("?", "this help"),
]

_NAVIGATION: list[tuple[str, str]] = [
    ("Up/Down", "prompt history"),
    ("j/k", "scroll conversation"),
    ("Ctrl+U/D", "half-page scroll"),
    ("g/G", "top / bottom"),
    ("Tab", "cycle focus"),
    ("Esc", "dismiss / clear / interrupt / rewind"),
]

_AGENT: list[tuple[str, str]] = [
    ("Ctrl+A", "select agent"),
    ("Ctrl+K", "model browser"),
    ("Ctrl+Shift+K", "cycle reasoning effort"),
    ("Ctrl+N", "new session"),
    ("Ctrl+C", "copy selection (drag to select)"),
    ("y", "copy last response"),
    ("Ctrl+Q", "interrupt turn, press twice to quit"),
]

_SCREENS: list[tuple[str, str]] = [
    ("Ctrl+B", "sessions"),
    ("Ctrl+P", "capabilities"),
    ("Ctrl+R", "runtimes"),
    ("Ctrl+T", "traces"),
    ("Ctrl+E", "evaluations"),
    ("F5", "console"),
]

# Inline explanation of the page-status figures. Phrased so a user reading
# `?` after seeing `ctx 53.4k/200k tok · ⚒ 12 · usage $0.34` can identify
# each segment and understand that `usage` cost is in-session-only USD,
# not balance and not account-wide spend — the unit-mismatch resolution.
_STATUS_BAR: list[tuple[str, str]] = [
    ("ctx N/M tok", "prompt size relative to the model's context limit"),
    ("⚒ N", "tool calls this session"),
    ("usage $X.XX", "total inference spend this session"),
]

_COMMAND_GROUPS: list[tuple[str, list[str]]] = [
    (
        "Session",
        ["/new", "/clear", "/sessions", "/rename", "/rewind", "/compact", "/export"],
    ),
    ("Agent", ["/agent", "/agents", "/model", "/models", "/thinking", "/reload"]),
    (
        "Platform",
        ["/login", "/logout", "/whoami", "/profile", "/workspace", "/workspaces", "/projects"],
    ),
    (
        "Screens",
        [
            "/traces",
            "/evaluations",
            "/runtimes",
            "/capabilities",
            "/console",
            "/sandboxes",
            "/secrets",
            "/environments",
        ],
    ),
    ("Tools", ["/skills", "/mcp", "/tools", "/update", "/copy", "/quit"]),
]

# Colors
_HEADING = FG_SUBTLE
_KEY = ACCENT
_DESC = FG_MUTED
_CMD = FG_SUBTLE
_SEP = BORDER_LIGHT


def _section(t: Text, title: str, items: list[tuple[str, str]]) -> None:
    """Append a key/description section."""
    t.append(f"  {title}\n", style=f"bold {_HEADING}")
    for key, desc in items:
        t.append(f"    {key:<14}", style=_KEY)
        t.append(f" {desc}\n", style=_DESC)


def render_help() -> Text:
    """Build the help content as a Rich Text renderable."""
    t = Text()

    _section(t, "Input", _INPUT)
    t.append("\n")
    _section(t, "Navigation", _NAVIGATION)
    t.append("\n")
    _section(t, "Agent", _AGENT)
    t.append("\n")
    _section(t, "Screens", _SCREENS)
    t.append("\n")
    _section(t, "Status", _STATUS_BAR)
    t.append("    Credits and pricing  ", style=_DESC)
    t.append(PRICING_DOCS_URL, style=f"{_CMD} link {PRICING_DOCS_URL}")
    t.append("\n")

    t.append("\n")
    t.append("  Commands\n", style=f"bold {_HEADING}")
    for group, cmd_names in _COMMAND_GROUPS:
        commands = [n for n in cmd_names if n in _CMD_LOOKUP]
        t.append(f"    {group:<12}", style=_DESC)
        t.append(" ".join(commands), style=_CMD)
        t.append("\n")

    return t
