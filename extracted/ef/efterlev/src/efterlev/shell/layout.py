"""Render the snapshot block and banner using rich.

Restrained on purpose: one accent color for `Next` / `✓` / command
names, one muted gray for labels. No boxes, no emojis, no maximalist
panels. Newspaper-restrained, not neon-dashboard.

Colors:
- ACCENT — a muted teal that reads as "important but not loud"
- MUTED  — pale gray for labels and timestamps
- ERROR  — bold red, used only when something failed
- (everything else defaults to the terminal's foreground color, so
  the shell respects the user's theme as much as possible)
"""

from __future__ import annotations

from rich.console import Console
from rich.text import Text

from efterlev import __version__
from efterlev.shell.banner import render_banner
from efterlev.shell.state import (
    NextSuggestion,
    WorkspaceSnapshot,
    format_cost_summary,
    format_status_summary,
)

ACCENT = "color(73)"  # muted teal — palette index, theme-resilient
MUTED = "color(244)"  # mid-gray
ERROR = "bold red"


def render_entry(
    console: Console, snapshot: WorkspaceSnapshot, suggestion: NextSuggestion | None
) -> None:
    """Print the on-entry block: banner + workspace summary + next-step hint.

    Called once per shell session (entry) and again on `/status`.
    """
    console.print()
    console.print(Text(render_banner(), style=ACCENT))
    console.print()
    console.print(
        Text("  efterlev · ", style=MUTED)
        + Text(f"v{__version__}", style="")
        + Text(" · interactive shell", style=MUTED)
    )
    console.print()
    _render_status_block(console, snapshot, suggestion)
    console.print()
    # First-time users: clarify the file-location confusion + surface /tour.
    # (Most common first-run confusion: customers think they have to copy
    # files into .efterlev/. They don't — efterlev scans the cwd directly.)
    if not snapshot.initialized:
        console.print(
            Text(
                "  Efterlev scans the directory it runs from — your IaC files "
                "stay where they are.\n"
                "  The .efterlev/ directory holds workspace metadata only "
                "(config, scan results, reports).",
                style=MUTED,
            )
        )
        console.print()
        console.print(
            Text("  New here? Try ", style=MUTED)
            + Text("/tour", style=ACCENT)
            + Text(" for a guided walkthrough, or ", style=MUTED)
            + Text("/help", style=ACCENT)
            + Text(" for commands.", style=MUTED)
        )
        console.print(
            Text("  ", style=MUTED)
            + Text("Ctrl+D", style=ACCENT)
            + Text(" or ", style=MUTED)
            + Text("/exit", style=ACCENT)
            + Text(" to leave.", style=MUTED)
        )
    else:
        console.print(
            Text("  Type ", style=MUTED)
            + Text("/help", style=ACCENT)
            + Text(" for commands or ", style=MUTED)
            + Text("/tour", style=ACCENT)
            + Text(" for a walkthrough. ", style=MUTED)
            + Text("Ctrl+D", style=ACCENT)
            + Text(" or ", style=MUTED)
            + Text("/exit", style=ACCENT)
            + Text(" to leave.", style=MUTED)
        )
    console.print()


def render_status_only(
    console: Console, snapshot: WorkspaceSnapshot, suggestion: NextSuggestion | None
) -> None:
    """Print just the status block (no banner). Used after state-changing commands."""
    console.print()
    _render_status_block(console, snapshot, suggestion)
    console.print()


def _render_status_block(
    console: Console,
    snapshot: WorkspaceSnapshot,
    suggestion: NextSuggestion | None,
) -> None:
    """The columnar status block: Workspace / Status / Baseline / Cost / Next."""
    rows: list[tuple[str, Text]] = []

    rows.append(("Workspace", Text(str(snapshot.root))))
    rows.append(("Status", Text(format_status_summary(snapshot))))

    if snapshot.baseline:
        rows.append(("Baseline", Text(snapshot.baseline)))

    # v0.1.150 / #355: surface which LLM backend is configured so users
    # can tell at a glance whether their `/agent gap` calls are routing
    # through pay-per-token API, Bedrock, or the subscription path.
    backend_text = _format_backend_line(snapshot)
    if backend_text is not None:
        rows.append(("Backend", backend_text))

    cost_line = format_cost_summary(snapshot)
    if cost_line:
        rows.append(("Cost", Text(cost_line)))

    label_w = max(len(label) for label, _ in rows)
    for label, value in rows:
        console.print(Text("  " + label.ljust(label_w) + "  ", style=MUTED) + value)

    if suggestion is not None:
        console.print()
        console.print(
            Text("  Next  ".ljust(label_w + 4), style=MUTED)
            + Text(suggestion.command, style=ACCENT)
            + Text("  " + suggestion.why, style=MUTED)
        )


def _format_backend_line(snapshot: WorkspaceSnapshot) -> Text | None:
    """Render the Backend banner line: `claude_code · claude-sonnet-4-6 · subscription`.

    Returns None when no backend is configured (early in init flow) so
    the banner doesn't show a confusing empty line. v0.1.150 / #355.
    """
    if snapshot.llm_backend is None:
        return None
    descriptions = {
        "anthropic": ("Anthropic API", "pay-per-token"),
        "bedrock": ("AWS Bedrock", "pay-per-token via Bedrock"),
        "claude_code": ("Claude Code", "Pro/Max subscription, no per-call billing"),
    }
    label, note = descriptions.get(snapshot.llm_backend, (snapshot.llm_backend, ""))
    text = Text(label, style=ACCENT)
    if snapshot.llm_model:
        text = text + Text(f" · {snapshot.llm_model}", style=MUTED)
    if note:
        text = text + Text(f" · {note}", style=MUTED)
    return text


def render_ok(console: Console, message: str) -> None:
    """One-line success confirmation, restrained."""
    console.print(Text("  ✓ ", style=ACCENT) + Text(message))


def render_error(console: Console, message: str, *, hint: str | None = None) -> None:
    """Error line + optional hint on the next line."""
    console.print(Text("  error: ", style=ERROR) + Text(message))
    if hint:
        console.print(Text("  hint: ", style=MUTED) + Text(hint, style=MUTED))


def render_unknown_command_hint(console: Console, raw: str) -> None:
    """The 'commands start with /' nudge for non-slash input."""
    console.print(
        Text("  commands start with ", style=MUTED)
        + Text("/", style=ACCENT)
        + Text(" — try ", style=MUTED)
        + Text("/help", style=ACCENT)
        + Text(f"  ({raw!r} not recognized)", style=MUTED)
    )
