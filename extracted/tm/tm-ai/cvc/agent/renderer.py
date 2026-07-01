"""
cvc.agent.renderer — Rich terminal rendering for the CVC agent.

Handles all visual output: banners, streaming text, tool call displays,
status bars, and the input prompt. Themed with the CVC color palette.

Features:
  - Token-by-token streaming display
  - Cost tracking display
  - Git status integration
  - Tab completion for slash commands
  - Real-time narration, diff previews, permission panels, turn summaries
"""

from __future__ import annotations
from cvc._subprocess_compat import HIDDEN_KW

import asyncio
import difflib
import os
import sys
import time
from typing import TYPE_CHECKING, Any

if sys.platform == "win32":
    # Force UTF-8 codepage in Windows CMD/PowerShell to prevent ASCII block mojibake
    os.system("chcp 65001 >nul 2>&1")
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

if TYPE_CHECKING:
    from cvc.agent.retry import DiagnosisResult

from rich import box
from rich.console import Console, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# ---------------------------------------------------------------------------
# CVC Dark Red Theme — #2C0000 and close colors
# ---------------------------------------------------------------------------

# Rich doesn't support all hex as style names, but we can use them directly
THEME = {
    "primary": "#8B0000",       # Dark red — borders, accents
    "primary_dim": "#5C1010",   # Muted red — secondary borders
    "primary_bright": "#CC3333",  # Bright red — highlights
    "accent": "#FF4444",        # Vivid red — user input, important
    "accent_soft": "#FF6B6B",   # Soft red — prompts
    "text": "#E8D0D0",          # Warm light — readable text
    "text_dim": "#8B7070",      # Dimmed warm text
    "success": "#55AA55",       # Green for success
    "warning": "#CCAA33",       # Yellow for warnings
    "error": "#FF3333",         # Bright red for errors
    "tool_name": "#CC6666",     # Tool name color
    "tool_result": "#AA8888",   # Tool result color
    "branch": "#CC5555",        # Branch name color
    "hash": "#BB8844",          # Commit hash color
    "bg": "#2C0000",            # Deep maroon background ref
}

# Use force_terminal=True on Windows to ensure proper unicode rendering
console = Console(force_terminal=sys.stdout.isatty())


def agent_banner(version: str, provider: str, model: str, branch: str, workspace: str) -> None:
    """Print the CVC Agent startup banner in a split UI."""
    # Fetch user name dynamically
    import json
    from pathlib import Path

    from cvc.agent.tips import get_next_tip
    auth_file = Path.home() / ".cvc" / "auth.json"
    user_name = "Developer"
    short_name = "Dev"
    if auth_file.exists():
        try:
            with open(auth_file, "r") as f:
                auth_data = json.load(f)
                full_name = auth_data.get("display_name")
                if full_name:
                    user_name = full_name
                    # Get first name for the top right badge to save space
                    short_name = "Meena"
        except Exception:
            pass

    # Left Side: Logo + Welcome
    box_width = (console.width or 80) // 2
    # Inner width accounts for borders (2) and padding left/right (4)
    pad_spaces = max(0, (box_width - 6 - 27) // 2)
    pad = " " * pad_spaces

    logo = Text()
    logo.append(f"{pad} ██████╗ ██╗   ██╗  ██████╗\n", style=THEME["primary_bright"])
    logo.append(f"{pad}██╔════╝ ██║   ██║ ██╔════╝\n", style=THEME["primary_bright"])
    logo.append(f"{pad}██║      ██║   ██║ ██║     \n", style=THEME["primary"])
    logo.append(f"{pad}██║      ╚██╗ ██╔╝ ██║     \n", style=THEME["primary"])
    logo.append(f"{pad}╚██████╗  ╚████╔╝  ╚██████╗\n", style=THEME["primary_dim"])
    logo.append(f"{pad} ╚═════╝   ╚═══╝    ╚═════╝\n", style=THEME["primary_dim"])

    welcome_text = Text(justify="center")
    welcome_text.append("\n")
    welcome_text.append("Welcome back! ")
    welcome_text.append(f"— {user_name}\n", style=f"bold {THEME['accent']}")
    welcome_text.append(f"Workspace: {workspace}", style=THEME["text_dim"])

    len_left = len(f" CVC v{version} ")
    len_right = len(f" {short_name} ")
    space_len = max(0, box_width - len_left - len_right - 5)

    title_text = Text()
    title_text.append(f" CVC v{version} ", style=f"bold {THEME['primary_bright']}")
    title_text.append("─" * space_len, style=THEME["primary"])
    title_text.append(f" {short_name} ", style=f"bold {THEME['primary_bright']}")

    left_panel = Panel(
        Group(logo, welcome_text),
        title=title_text,
        title_align="left",
        border_style=THEME["primary"],
        box=box.ROUNDED,
        padding=(1, 2),
        height=14
    )

    # Right Side: Tips
    tip_text = Text()
    tip_text.append_text(Text.from_markup(get_next_tip()))
    tip_text.append("\n\n")
    tip_text.append("Auto-resuming session.\n", style=THEME["text_dim"])
    tip_text.append("Type your request, or use ", style=THEME["text_dim"])
    tip_text.append("/help", style=f"bold {THEME['accent']}")
    tip_text.append(" for commands.\n", style=THEME["text_dim"])
    tip_text.append("Ctrl+C to exit.", style=THEME["text_dim"])

    right_panel = Panel(
        tip_text,
        title=f"[{THEME['text_dim']}]Quick Tips[/{THEME['text_dim']}]",
        title_align="left",
        border_style=THEME["primary"],
        box=box.ROUNDED,
        padding=(1, 2),
        height=14
    )

    # Use a Table to split them 50/50
    layout_table = Table.grid(expand=True)
    layout_table.add_column("left", ratio=1)
    layout_table.add_column("right", ratio=1)
    layout_table.add_row(left_panel, right_panel)

    console.print()
    console.print(layout_table)

    # Config bar
    config_text = Text()
    config_text.append("  Provider  ", style=THEME["text_dim"])
    config_text.append(provider, style=f"bold {THEME['accent']}")
    config_text.append("  │  ", style=THEME["primary_dim"])
    config_text.append("Model  ", style=THEME["text_dim"])
    config_text.append(model, style=f"bold {THEME['accent']}")
    config_text.append("  │  ", style=THEME["primary_dim"])
    config_text.append("Branch  ", style=THEME["text_dim"])
    config_text.append(branch, style=f"bold {THEME['branch']}")

    console.print(
        Panel(
            config_text,
            border_style=THEME["primary_dim"],
            padding=(0, 2),
        )
    )
    console.print()


def print_help() -> None:
    """Show the slash commands help."""
    table = Table(
        box=box.ROUNDED,
        border_style=THEME["primary_dim"],
        show_header=True,
        header_style=f"bold {THEME['primary_bright']}",
    )
    table.add_column("Command", style=f"bold {THEME['accent']}", width=22)
    table.add_column("Description", style=THEME["text"])

    cmds = [
        ("/help", "Show this help message"),
        ("/status", "Show CVC status (branch, HEAD, context)"),
        ("/log", "Show CVC commit history"),
        ("/commit <msg>", "Create a cognitive checkpoint"),
        ("/branch <name>", "Create a new branch (creates & switches)"),
        ("/checkout <name>", "Switch to an existing branch"),
        ("/branches", "List all branches"),
        ("/merge <source>", "Merge source branch into current branch"),
        ("/restore <hash>", "Time-travel to a previous commit"),
        ("/search <query>", "Search commit history for context"),
        ("/smartsearch <q> [flags]", "Staged hybrid search (--branch, --since, --type, etc.)"),
        ("/ingest <path>", "Ingest document into PageIndex Tier 4 (PDF, text, code)"),
        ("/docsearch <query>", "Search ingested documents (--doc <id>, --max N)"),
        ("/documents", "List all PageIndex-indexed documents"),
        ("/files [pattern]", "List files in workspace (optional filter)"),
        ("/summary", "Get codebase structure summary"),
        ("/diff [file]", "Show git diff of uncommitted changes"),
        ("/distill [N]", "Compile recent N commits into a Cog (default: 5)"),
        ("/cogs", "List compiled Cogs and ROI report"),
        ("/continue", "Continue AI response from last point"),
        ("/model", "Switch model interactively (or /model <name>)"),
        ("/provider", "Switch LLM provider interactively"),
        ("/undo", "Undo the last file change"),
        ("/retry [message]", "Auto-retry: diagnose → revert if needed → redo with lessons"),
        ("/web <query>", "Search the web for docs/answers"),
        ("/git", "Show Git status and recent commits"),
        ("/git commit <msg>", "Create a Git commit"),
        ("/sync [remote]", "Fetch + ff-pull + push current branch (--no-push, --rebase)"),
        ("/cost", "Show session cost summary"),
        ("/analytics", "Show detailed session & usage analytics"),
        ("/image <path> [prompt]", "Load image file (+ send prompt inline)"),
        ("/paste [prompt]", "Paste clipboard image (+ send prompt inline)"),
        ("/memory", "Show persistent memory from past sessions"),
        ("/serve", "Start the CVC proxy in a new terminal"),
        ("/init", "Initialize CVC in workspace"),
        ("/init-rules", "Generate CVC.md by analyzing the project"),
        ("/compact", "Summarize and compact the conversation"),
        ("/health", "Context Autopilot health dashboard"),
        ("", ""),  # Separator
        ("/plan", "Toggle plan ↔ agent mode (rerun to switch back)"),
        ("/autopilot [on|off|yolo]", "Toggle autopilot: continuous execution until task is done"),
        ("/mode [default|bypass|autopilot]", "VS Code-style approval mode (synced to dashboard)"),
        ("/think [off|low|med|high]", "Toggle extended thinking (rerun to toggle off/on)"),
        ("/context", "Show context window utilization"),
        ("/copy", "Copy last response to clipboard"),
        ("/export [file]", "Export conversation to markdown"),
        ("/config", "Show current configuration"),
        ("/stats", "Detailed session usage statistics"),
        ("", ""),  # Separator
        ("/permissions [add ...]", "View/add permission rules"),
        ("/allowed-tools", "Show per-tool permission decisions"),
        ("/agents", "List sub-agents (Explore/Plan/Security/AI/UI/Data/Orchestrator)"),
        ("/tasks", "List background tasks"),
        ("/hooks", "List configured hooks"),
        ("", ""),  # Separator
        ("/sessions", "List all sessions for this workspace"),
        ("/fork [name]", "Fork current session into a new one"),
        ("/rename <name>", "Rename current session"),
        ("/rewind [N]", "Rewind conversation by N turns"),
        ("", ""),  # Separator
        ("/plugins", "List installed plugins"),
        ("/skills [name]", "List skills or invoke by name"),
        ("/cd <path>", "Change working directory"),
        ("/add-dir <path>", "Add additional workspace directory"),
        ("/fast [on|off]", "Toggle fast model for current provider"),
        ("/doctor", "Run diagnostics on CVC environment"),
        ("/release-notes", "Show CVC changelog"),
        ("/trust [strict|smart|yolo]", "Toggle trust-all on/off (or set mode)"),
        ("/plan-mode [mode]", "Set plan display: approve, auto, or quiet"),
        ("", ""),  # Separator
        ("/settings [key value]", "View or modify settings"),
        ("/hive [write|read|stats|summary]", "Interact with Hive Memory (The Plüberous)"),
        ("/agent [list|create|create-from-prompt]", "Manage agent templates"),
        ("", ""),  # Separator
        ("/clear, /new", "Clear conversation (start fresh)"),
        ("/exit, /quit", "Exit the agent"),
    ]
    for cmd, desc in cmds:
        table.add_row(cmd, desc)

    console.print(
        Panel(
            table,
            border_style=THEME["primary"],
            title=f"[bold {THEME['accent']}]Commands[/bold {THEME['accent']}]",
            padding=(1, 1),
        )
    )
    console.print()


def _get_box_width() -> int:
    """Get the width for input/narration box borders.

    Returns terminal width minus 1 to prevent corner characters
    (╮, ╯) from wrapping to the next line on terminals that
    auto-wrap when the last column is filled.
    """
    try:
        return max(console.width - 1, 40)
    except Exception:
        return 79


def print_input_prompt(branch: str, turn: int, health_bar: str = "") -> str:
    """Print the C-shaped arrow input prompt (no boxed text area)."""
    health_suffix = f"  {health_bar}" if health_bar else ""
    console.print(
        f"[{THEME['accent']}]╭[/{THEME['accent']}] "
        f"[bold {THEME['primary_bright']}]CVC[/bold {THEME['primary_bright']}]"
        f"[{THEME['text_dim']}]@[/{THEME['text_dim']}]"
        f"[bold {THEME['branch']}]{branch}[/bold {THEME['branch']}]"
        f"[{THEME['text_dim']}] (turn {turn})[/{THEME['text_dim']}]"
        f"{health_suffix}"
    )

    try:
        line = console.input(f"[{THEME['accent']}]╰▶[/{THEME['accent']}] ")
        text = line.strip()
        return text
    except EOFError:
        return "/exit"


def _agent_header_line() -> str:
    """Build a dynamic-width agent response header line."""
    w = _get_box_width()
    label = " Agent "
    # 3 = len("┌─") + trailing space before dashes
    dashes = max(w - 3 - len(label), 0)
    return (
        f"\n[{THEME['primary_dim']}]┌─[/{THEME['primary_dim']}]"
        f"[bold {THEME['primary_bright']}]{label}[/bold {THEME['primary_bright']}]"
        f"[{THEME['primary_dim']}]{'─' * dashes}[/{THEME['primary_dim']}]"
    )


def _agent_footer_line() -> str:
    """Build a dynamic-width agent response footer line."""
    w = _get_box_width()
    return f"[{THEME['primary_dim']}]└{'─' * max(w - 2, 0)}[/{THEME['primary_dim']}]"


def render_streaming_start() -> None:
    """Print the assistant response header."""
    console.print(_agent_header_line())


def render_streaming_text(text: str) -> None:
    """Render a chunk of streaming text."""
    console.print(f"[{THEME['primary_dim']}]│[/{THEME['primary_dim']}] ", end="")
    # Render the accumulated text as markdown
    try:
        md = Markdown(text)
        console.print(md)
    except Exception:
        console.print(text)


def render_response_text(text: str) -> None:
    """Render the full assistant response text."""
    if not text.strip():
        return
    console.print(_agent_header_line())
    # Render as markdown within a bordered area
    for line in text.split("\n"):
        console.print(
            f"[{THEME['primary_dim']}]│[/{THEME['primary_dim']}]  {line}"
        )
    console.print(_agent_footer_line())


def render_markdown_response(text: str) -> None:
    """Render the assistant response as a Rich Markdown panel."""
    if not text.strip():
        return
    display_text = _collapse_large_code_blocks(text.strip())
    try:
        md = Markdown(display_text)
    except Exception:
        md = display_text

    console.print()
    console.print(
        Panel(
            md,
            border_style=THEME["primary_dim"],
            title=f"[bold {THEME['primary_bright']}]Agent[/bold {THEME['primary_bright']}]",
            title_align="left",
            padding=(1, 2),
        )
    )


def render_tool_call_start(tool_name: str, args_summary: str) -> None:
    """Show that a tool is being called — clean, professional, human-readable."""
    label, icon = _tool_display(tool_name)
    # args_summary is already a human-friendly description (built by chat.py)
    desc = args_summary if args_summary else ""
    console.print(
        f"\n  [{THEME['primary_dim']}]⟫[/{THEME['primary_dim']}] "
        f"{icon}  [{THEME['tool_name']}]{label}[/{THEME['tool_name']}]"
        f"{'  ' if desc else ''}"
        f"[{THEME['text_dim']}]{desc}[/{THEME['text_dim']}]",
        end="",
    )


def render_tool_call_result(tool_name: str, result: str, elapsed: float) -> None:
    """Append result info on the SAME line as the tool start — ultra minimal."""
    elapsed_str = f"{elapsed:.1f}s" if elapsed >= 0.1 else f"{elapsed * 1000:.0f}ms"

    # Build a compact inline summary (shown in parentheses)
    summary = _smart_result_summary(tool_name, result)
    suffix = f"  ({summary})" if summary else ""

    console.print(
        f"  [{THEME['success']}]\u2713[/{THEME['success']}] "
        f"[{THEME['text_dim']}]{elapsed_str}{suffix}[/{THEME['text_dim']}]"
    )


def render_tool_error(tool_name: str, error: str) -> None:
    """Show a tool error with professional label."""
    label, _ = _tool_display(tool_name)
    console.print(
        f"  [{THEME['error']}]✗ {label} failed:[/{THEME['error']}] "
        f"[{THEME['text_dim']}]{error[:200]}[/{THEME['text_dim']}]"
    )


def render_tool_dud_warning(tool_calls) -> None:
    """v2.92.10 — Render a single collapsed yellow warning for dud
    tool calls (model emitted empty/missing arguments). Without this,
    the executor's per-call WARNING logs would print once per dud
    call, polluting the terminal with N identical lines. Now we
    dedup in the chat loop and call this function once per turn.

    The format mirrors the dashboard's "list_dir was called 1× with
    no arguments (model emitted dud tool calls)." so the experience
    is consistent across CLI and dashboard.

    Args:
        tool_calls: list of ToolCall-shaped objects (need .name).
                    The function counts occurrences of each tool name.
    """
    if not tool_calls:
        return
    # Tally by tool name. Consecutive duds of the same tool collapse
    # to "name (N×)" so the user sees a single readable line.
    counts: dict[str, int] = {}
    for tc in tool_calls:
        name = getattr(tc, "name", "unknown") or "unknown"
        counts[name] = counts.get(name, 0) + 1
    parts = []
    for name, n in counts.items():
        label, _ = _tool_display(name)
        if n == 1:
            parts.append(label)
        else:
            parts.append(f"{label} {n}\u00d7")
    summary = ", ".join(parts)
    console.print(
        f"  [{THEME['warning']}]\u26a0 {summary} called with no arguments "
        f"(model emitted dud tool calls).[/{THEME['warning']}]"
    )


def render_auto_commit(message: str, commit_hash: str) -> None:
    """Show an auto-commit notification."""
    console.print(
        f"\n  [{THEME['primary_dim']}]⟫[/{THEME['primary_dim']}] "
        f"[{THEME['success']}]Auto-committed:[/{THEME['success']}] "
        f"[{THEME['hash']}]{commit_hash[:12]}[/{THEME['hash']}] "
        f"[{THEME['text_dim']}]{message}[/{THEME['text_dim']}]"
    )


# ---------------------------------------------------------------------------
# Permission Panel — rich permission prompt with multiple options
# ---------------------------------------------------------------------------

def render_permission_panel(
    tool_name: str,
    arguments: dict[str, Any],
    trust_mode: str = "smart",
) -> str:
    """
    Rich permission prompt with full trust options.

    Returns one of: "allow_once", "allow_always", "trust_all", "deny", or
    "deny_feedback:<message>" if the user provides an alternative.
    """
    # Build tool description
    label, icon = _tool_display(tool_name)
    desc_parts = []
    if tool_name == "bash" and "command" in arguments:
        desc_parts.append(f"  [{THEME['accent']}]{arguments['command']}[/{THEME['accent']}]")
    elif tool_name in ("write_file", "edit_file", "patch_file") and "path" in arguments:
        desc_parts.append(f"  [{THEME['accent']}]{arguments['path']}[/{THEME['accent']}]")
    elif tool_name == "agent" and "prompt" in arguments:
        desc_parts.append(f"  [{THEME['text']}]{arguments['prompt'][:80]}[/{THEME['text']}]")

    # Permission panel
    content = Text()
    content.append(f"  {icon}  ", style=THEME["tool_name"])
    content.append(label, style=f"bold {THEME['tool_name']}")
    content.append("\n")
    for part in desc_parts:
        content = None  # We'll use markup instead
        break

    # Use markup-based rendering for proper styling
    markup_lines = [f"  {icon}  [bold {THEME['tool_name']}]{label}[/bold {THEME['tool_name']}]"]
    for part in desc_parts:
        markup_lines.append(part)

    console.print()
    console.print(
        Panel(
            "\n".join(markup_lines),
            title=f"[bold {THEME['warning']}]Permission Required[/bold {THEME['warning']}]",
            border_style=THEME["primary"],
            padding=(0, 2),
        )
    )

    # Arrow-key selection
    from cvc.agent.menus import arrow_confirm, arrow_select

    perm_options: list[tuple[str, str]] = [
        ("Allow this once", "allow_once"),
        (f"Always allow {tool_name} this session", "allow_always"),
        ("Trust ALL commands this session", "trust_all"),
        ("Deny", "deny"),
        ("Deny & suggest alternative", "deny_feedback"),
    ]

    choice = arrow_select("Permission Required", perm_options, default=0)

    if choice is None:
        return "deny"

    if choice == "trust_all":
        console.print(
            f"  [{THEME['warning']}]⚠  All commands will be auto-allowed for this session.[/{THEME['warning']}]"
        )
        if arrow_confirm("Confirm trust-all?", default_yes=False):
            return "trust_all"
        return "deny"
    elif choice == "deny_feedback":
        try:
            feedback = input("  Suggestion > ").strip()
        except (EOFError, KeyboardInterrupt):
            return "deny"
        return f"deny_feedback:{feedback}" if feedback else "deny"
    return choice


# ---------------------------------------------------------------------------
# Code block collapsing — hide ugly raw code dumps from terminal
# ---------------------------------------------------------------------------

_CODE_BLOCK_COLLAPSE_THRESHOLD = 30  # lines — code blocks longer than this get collapsed


def _collapse_large_code_blocks(text: str) -> str:
    """
    Collapse large fenced code blocks (```...```) into short summaries.

    Models like Opus tend to echo entire file contents or generate huge code
    blocks as narration before tool calls.  This keeps the terminal clean by
    replacing blocks longer than the threshold with a one-line summary.
    """
    import re

    def _replace_block(match: re.Match) -> str:
        lang = (match.group(1) or "").strip()
        code = match.group(2)
        lines = code.strip().splitlines()
        if len(lines) <= _CODE_BLOCK_COLLAPSE_THRESHOLD:
            return match.group(0)  # keep small blocks as-is
        lang_label = f" ({lang})" if lang else ""
        # Show first 5 and last 3 lines as a preview
        preview = "\n".join(lines[:5])
        return (
            f"```{lang}\n{preview}\n"
            f"... ({len(lines)} lines total{lang_label} — collapsed for readability)\n```"
        )

    return re.sub(
        r"```(\w*)\n(.*?)```",
        _replace_block,
        text,
        flags=re.DOTALL,
    )


# ---------------------------------------------------------------------------
# Narration — lightweight left-border text between tool calls
# ---------------------------------------------------------------------------

def render_narration(text: str) -> None:
    """
    Show agent narration in a bordered panel.

    Used for intermediate text the agent produces between tool calls,
    visually distinguished from the final Agent response panel.

    Long code blocks (>30 lines) are collapsed to "[Code: N lines]"
    summaries to keep the terminal clean and readable.
    """
    if not text.strip():
        return
    display_text = _collapse_large_code_blocks(text.strip())
    console.print()
    console.print(
        Panel(
            Markdown(display_text),
            border_style=THEME["primary_dim"],
            title=f"[bold {THEME['primary_bright']}]Agent[/bold {THEME['primary_bright']}]",
            title_align="left",
            padding=(0, 2),
        )
    )


# ---------------------------------------------------------------------------
# Plan Display — numbered plan block
# ---------------------------------------------------------------------------

def render_plan_block(plan_text: str, mode: str = "plan-auto") -> None:
    """
    Display the agent's plan before multi-step execution.

    Parameters
    ----------
    plan_text : str
        The plan text (expected to have numbered steps).
    mode : str
        "plan-approve" shows the plan and waits, "plan-auto" shows briefly,
        "plan-quiet" skips display entirely.
    """
    if mode == "plan-quiet" or not plan_text.strip():
        return

    console.print()
    console.print(
        Panel(
            plan_text.strip(),
            title=f"[bold {THEME['primary_bright']}]Plan[/bold {THEME['primary_bright']}]",
            title_align="left",
            border_style=THEME["primary"],
            padding=(0, 2),
        )
    )


def render_plan_approval_prompt() -> bool:
    """Prompt user to approve a plan. Returns True if approved."""
    from cvc.agent.menus import arrow_confirm
    return arrow_confirm("Proceed with this plan?", default_yes=True)


# ---------------------------------------------------------------------------
# Diff Preview — inline diff after file edits
# ---------------------------------------------------------------------------

def render_diff_preview(filepath: str, old_content: str, new_content: str, max_lines: int = 15) -> None:
    """
    Show an inline diff preview after a file edit.

    Small diffs shown inline; large diffs show a summary.
    """
    if old_content is None or old_content == new_content:
        return

    old_lines = old_content.splitlines(keepends=True)
    new_lines = new_content.splitlines(keepends=True)

    diff = list(difflib.unified_diff(old_lines, new_lines, lineterm=""))

    # Skip the --- / +++ headers
    diff_body = [l for l in diff if not l.startswith(("---", "+++"))]
    if not diff_body:
        return

    # Count actual change lines (not @@ headers)
    change_lines = [l for l in diff_body if l.startswith(("+", "-")) and not l.startswith("@@")]

    if len(change_lines) <= max_lines:
        # Show inline diff
        diff_text = Text()
        for line in diff_body[:max_lines + 5]:  # some slack for @@ headers
            line_str = line.rstrip("\n")
            if line_str.startswith("@@"):
                diff_text.append(f"  {line_str}\n", style=THEME["text_dim"])
            elif line_str.startswith("+"):
                diff_text.append(f"  {line_str}\n", style=THEME["success"])
            elif line_str.startswith("-"):
                diff_text.append(f"  {line_str}\n", style=THEME["error"])
            else:
                diff_text.append(f"  {line_str}\n", style=THEME["text_dim"])

        console.print(
            Panel(
                diff_text,
                title=f"[{THEME['text_dim']}]Changes[/{THEME['text_dim']}]",
                title_align="left",
                border_style=THEME["primary_dim"],
                padding=(0, 1),
            )
        )
    else:
        # Summary for large diffs
        added = sum(1 for l in change_lines if l.startswith("+"))
        removed = sum(1 for l in change_lines if l.startswith("-"))
        console.print(
            f"  [{THEME['text_dim']}]Changes:[/{THEME['text_dim']}] "
            f"[{THEME['success']}]+{added}[/{THEME['success']}] "
            f"[{THEME['error']}]-{removed}[/{THEME['error']}] "
            f"[{THEME['text_dim']}]lines ({len(change_lines)} total changes)[/{THEME['text_dim']}]"
        )


# ---------------------------------------------------------------------------
# Command Output Panel — styled output for bash commands
# ---------------------------------------------------------------------------

def render_command_output(command: str, output: str, exit_code: int = 0, max_lines: int = 8) -> None:
    """
    Show bash command output in a styled panel.

    Short output inline; long output truncated with 'N more lines'.
    Error output gets red border.
    """
    if not output.strip():
        return

    lines = output.strip().split("\n")
    is_error = exit_code != 0

    if len(lines) <= max_lines:
        display_text = "\n".join(f"  {line}" for line in lines)
    else:
        display_text = "\n".join(f"  {line}" for line in lines[:max_lines])
        remaining = len(lines) - max_lines
        display_text += f"\n  [{THEME['text_dim']}]... {remaining} more lines[/{THEME['text_dim']}]"

    border = THEME["error"] if is_error else THEME["primary_dim"]
    title_label = "Error Output" if is_error else "Output"

    console.print(
        Panel(
            display_text,
            title=f"[{THEME['text_dim']}]{title_label}[/{THEME['text_dim']}]",
            title_align="left",
            border_style=border,
            padding=(0, 1),
        )
    )


# ---------------------------------------------------------------------------
# Turn Summary — compact summary of all actions taken in a turn
# ---------------------------------------------------------------------------

def render_turn_summary(
    actions: list[dict[str, Any]],
    prompt_tokens: int = 0,
    completion_tokens: int = 0,
    turn_cost: float = 0.0,
    session_cost: float = 0.0,
) -> None:
    """
    Show a compact summary of all actions taken in an agentic turn.

    Parameters
    ----------
    actions : list of dicts with keys: category, description, success
    """
    if not actions:
        return

    # Group by category
    categories: dict[str, list[str]] = {}
    for action in actions:
        cat = action.get("category", "other")
        desc = action.get("description", "")
        success = action.get("success", True)
        icon = "✓" if success else "✗"
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(f"  [{THEME['success'] if success else THEME['error']}]{icon}[/{THEME['success'] if success else THEME['error']}] {desc}")

    summary_lines = []
    for cat, items in categories.items():
        for item in items:
            summary_lines.append(item)

    # Token/cost footer
    if prompt_tokens or completion_tokens:
        summary_lines.append("")
        cost_line = f"  [{THEME['text_dim']}]tokens: {prompt_tokens} in → {completion_tokens} out"
        if session_cost > 0:
            cost_line += f"  │  turn: ${turn_cost:.4f}  │  session: ${session_cost:.4f}"
        cost_line += f"[/{THEME['text_dim']}]"
        summary_lines.append(cost_line)

    console.print()
    console.print(
        Panel(
            "\n".join(summary_lines),
            title=f"[bold {THEME['primary_bright']}]Turn Summary[/bold {THEME['primary_bright']}]",
            title_align="left",
            border_style=THEME["primary_dim"],
            padding=(0, 1),
        )
    )


# ---------------------------------------------------------------------------
# Enhanced tool call with step progress
# ---------------------------------------------------------------------------

def render_tool_call_start_with_step(
    tool_name: str, args_summary: str, step: int = 0, total: int = 0
) -> None:
    """Show tool call start with optional step progress indicator."""
    label, icon = _tool_display(tool_name)
    desc = args_summary if args_summary else ""

    step_prefix = ""
    if step > 0 and total > 0:
        step_prefix = f"[{THEME['text_dim']}]Step {step}/{total}[/{THEME['text_dim']}] [{THEME['primary_dim']}]│[/{THEME['primary_dim']}] "

    console.print(
        f"\n  {step_prefix}"
        f"[{THEME['primary_dim']}]⟫[/{THEME['primary_dim']}] "
        f"{icon}  [{THEME['tool_name']}]{label}[/{THEME['tool_name']}]"
        f"{'  ' if desc else ''}"
        f"[{THEME['text_dim']}]{desc}[/{THEME['text_dim']}]",
        end="",
    )


def render_status(branch: str, head: str, ctx_size: int, provider: str, model: str) -> None:
    """Show CVC status."""
    console.print(
        Panel(
            f"  Branch    [{THEME['branch']}]{branch}[/{THEME['branch']}]\n"
            f"  HEAD      [{THEME['hash']}]{head[:12] if head else '—'}[/{THEME['hash']}]\n"
            f"  Context   [bold]{ctx_size}[/bold] messages\n"
            f"  Provider  [{THEME['text_dim']}]{provider} / {model}[/{THEME['text_dim']}]",
            border_style=THEME["primary_dim"],
            title=f"[bold {THEME['primary_bright']}]CVC Status[/bold {THEME['primary_bright']}]",
            padding=(0, 2),
        )
    )


def render_error(msg: str) -> None:
    """Show an error message."""
    console.print(f"  [{THEME['error']}]✗[/{THEME['error']}] {msg}")


def render_success(msg: str) -> None:
    """Show a success message."""
    console.print(f"  [{THEME['success']}]✓[/{THEME['success']}] {msg}")


def render_info(msg: str) -> None:
    """Show an info message."""
    console.print(f"  [{THEME['text_dim']}]→[/{THEME['text_dim']}] {msg}")


# Track when the last thinking indicator started (for elapsed time display)
_thinking_start_time: float = 0.0
_thinking_model: str = ""


def _print_thinking_line(elapsed: float = 0.0) -> None:
    """Overwrite the current terminal line with the thinking indicator + elapsed time."""
    elapsed_hint = (
        f" [{THEME['warning']}]({elapsed:.0f}s)[/{THEME['warning']}]"
        if elapsed >= 4 else ""
    )
    console.print(
        f"  [{THEME['primary_dim']}]⟫[/{THEME['primary_dim']}] "
        f"[italic {THEME['text_dim']}]Reasoning…[/italic {THEME['text_dim']}]{elapsed_hint}",
        end="\r",
    )


def render_thinking_done() -> None:
    """Finalize the thinking line: clear \\r, print elapsed time, add spacing.

    Idempotent — safe to call multiple times (only renders once).
    """
    global _thinking_start_time
    if _thinking_start_time == 0.0:
        return  # Already finalized or never started
    elapsed = time.time() - _thinking_start_time
    _thinking_start_time = 0.0  # Mark as finalized
    elapsed_str = f"{elapsed:.0f}s" if elapsed >= 1 else f"{elapsed * 1000:.0f}ms"
    # Clear the \r line with spaces, then print final version with newline
    console.print(" " * 80, end="\r")
    console.print(
        f"  [{THEME['primary_dim']}]⟫[/{THEME['primary_dim']}] "
        f"[italic {THEME['text_dim']}]Reasoning…[/italic {THEME['text_dim']}] "
        f"[{THEME['warning']}]({elapsed_str})[/{THEME['warning']}]"
    )


def render_thinking(model: str = "") -> None:
    """Show a polished thinking indicator with model name."""
    global _thinking_start_time, _thinking_model
    _thinking_start_time = time.time()
    _thinking_model = model
    _print_thinking_line(0.0)


async def animate_thinking() -> None:
    """Background task: update the thinking line with live elapsed time every second.

    Start with ``asyncio.create_task(animate_thinking())`` right after
    ``render_thinking()``.  Cancel the task as soon as the first token arrives
    so the elapsed counter disappears cleanly.
    """
    try:
        while True:
            await asyncio.sleep(1.0)
            elapsed = time.time() - _thinking_start_time
            _print_thinking_line(elapsed)
    except asyncio.CancelledError:
        pass


def render_slow_model_warning(model: str) -> None:
    """Display a notice when the user picks an inherently slow thinking model."""
    console.print(
        Panel(
            f"  [{THEME['warning']}]⚠  {model}[/{THEME['warning']}] is a deep-reasoning preview model.\n"
            f"  [bold]Conversational: ~3 – 10 s[/bold] (LOW thinking)\n"
            f"  [bold]Tool iterations: ~5 – 15 s[/bold] (LOW thinking)\n"
            f"  CVC auto-routes thinking level for speed + quality.\n\n"
            f"  [{THEME['text_dim']}]If the model is stuck in deep-think mode (>90 s),[/{THEME['text_dim']}]\n"
            f"  [{THEME['text_dim']}]CVC will auto-fallback to [bold]gemini-3-flash-preview[/bold] for speed.[/{THEME['text_dim']}]\n\n"
            f"  [{THEME['text_dim']}]Faster alternatives:[/{THEME['text_dim']}]\n"
            f"  [{THEME['text_dim']}]  • [bold]cvc agent --model gemini-3-flash-preview[/bold]  ← recommended for daily use[/{THEME['text_dim']}]\n"
            f"  [{THEME['text_dim']}]  • [bold]cvc agent --no-think[/bold]                       ← force minimal thinking always[/{THEME['text_dim']}]",
            border_style=THEME["warning"],
            title=f"[bold {THEME['warning']}] Thinking Model Notice [/bold {THEME['warning']}]",
            padding=(0, 2),
        )
    )
    console.print()


def render_token_usage(
    prompt_tokens: int,
    completion_tokens: int,
    cached: int = 0,
    turn_cost: float = 0.0,
    session_cost: float = 0.0,
) -> None:
    """Show token usage and cost after a response."""
    parts = [f"[{THEME['text_dim']}]tokens: {prompt_tokens} in"]
    if cached > 0:
        pct = (cached / max(prompt_tokens, 1)) * 100
        parts.append(f" ({cached} cached, {pct:.0f}%)")
    parts.append(f" → {completion_tokens} out")
    if session_cost > 0:
        parts.append(f"  │  turn: ${turn_cost:.4f}  │  session: ${session_cost:.4f}")
    parts.append(f"[/{THEME['text_dim']}]")
    console.print(f"  {''.join(parts)}")


def render_goodbye() -> None:
    """Show the goodbye message."""
    console.print()
    console.print(
        Panel(
            f"  [{THEME['text']}]Session ended. Your context is preserved in CVC.[/{THEME['text']}]\n"
            f"  [{THEME['text_dim']}]Run [bold]cvc agent[/bold] to continue where you left off.[/{THEME['text_dim']}]",
            border_style=THEME["primary_dim"],
            title=f"[bold {THEME['primary_bright']}]Goodbye[/bold {THEME['primary_bright']}]",
            padding=(0, 2),
        )
    )
    console.print()


# ---------------------------------------------------------------------------
# Tool Display System — human-readable labels, icons, and smart summaries
# ---------------------------------------------------------------------------

# Maps raw tool function names to (Human Label, Icon)
_TOOL_DISPLAY: dict[str, tuple[str, str]] = {
    # File operations
    "read_file":    ("Reading file",          "📄"),
    "write_file":   ("Writing file",          "✏️"),
    "edit_file":    ("Editing file",           "🔧"),
    "patch_file":   ("Patching file",          "🩹"),
    # Shell
    "bash":         ("Running command",        "⚡"),
    # Search & discovery
    "glob":         ("Finding files",          "📂"),
    "grep":         ("Searching code",         "🔍"),
    "list_dir":     ("Listing directory",      "📁"),
    "web_search":   ("Searching the web",      "🌐"),
    # CVC Time Machine
    "cvc_status":   ("Checking CVC status",    "📊"),
    "cvc_log":      ("Viewing commit history", "📜"),
    "cvc_commit":   ("Saving checkpoint",      "💾"),
    "cvc_branch":   ("Creating branch",        "🌿"),
    "cvc_restore":  ("Time-traveling",         "⏪"),
    "cvc_merge":    ("Merging branches",       "🔀"),
    "cvc_search":   ("Searching history",      "🔮"),
    "cvc_smart_search": ("Smart hybrid search",  "🎯"),
    "cvc_diff":     ("Comparing contexts",     "📐"),
    # Tier 4: PageIndex — Document RAG
    "cvc_ingest_document": ("Indexing document",  "📚"),
    "cvc_document_search": ("Searching documents","📖"),
    "cvc_list_documents":  ("Listing documents",  "📋"),
}


def _tool_display(name: str) -> tuple[str, str]:
    """Return (human_label, icon) for a tool name."""
    return _TOOL_DISPLAY.get(name, (name, "🔧"))


def _tool_icon(name: str) -> str:
    """Get an icon for a tool (legacy helper)."""
    _, icon = _tool_display(name)
    return icon


def _smart_result_summary(tool_name: str, result: str) -> str:
    """
    Build a smart, human-readable result summary based on the tool type.
    Instead of showing raw output, show meaningful context.
    """
    if not result:
        return ""

    lines = [l.strip() for l in result.split("\n") if l.strip()]
    if not lines:
        return ""

    first = lines[0]

    if tool_name == "read_file":
        # Extract file path & line count from typical result
        # Result usually starts with "File: path (N lines)"
        if first.startswith("File:"):
            return first
        # Count lines as fallback
        line_count = len(lines)
        return f"{line_count} lines read"

    elif tool_name == "write_file":
        if "Created" in first or "Wrote" in first:
            return first[:80]
        return "File saved successfully"

    elif tool_name == "edit_file":
        if "Applied" in first or "Edited" in first:
            return first[:80]
        if first.startswith("Error"):
            return first[:80]
        return "Edit applied"

    elif tool_name == "patch_file":
        return first[:80] if first else "Patch applied"

    elif tool_name == "bash":
        # Show first meaningful line of output, skip empties
        output = first[:80]
        if len(lines) > 1:
            output += f"  (+{len(lines) - 1} more lines)"
        return output

    elif tool_name == "glob":
        # Count matches
        match_count = len(lines)
        return f"{match_count} file(s) found"

    elif tool_name == "grep":
        # Result often has "Found N match(es)" or just matching lines
        if "Found" in first and "match" in first:
            return first[:80]
        match_count = len(lines)
        return f"{match_count} match(es) found"

    elif tool_name == "list_dir":
        item_count = len(lines)
        dirs = sum(1 for l in lines if l.endswith("/"))
        files = item_count - dirs
        return f"{files} files, {dirs} directories"

    elif tool_name == "web_search":
        result_count = sum(1 for l in lines if l.startswith("[" ) or l.startswith("1") or l.startswith("• "))
        if result_count:
            return f"{result_count} results — {first[:60]}"
        return first[:80]

    elif tool_name.startswith("cvc_"):
        # CVC tools — show the first line (usually a status or hash)
        return first[:80]

    # Fallback: first meaningful line
    return first[:80]


# ---------------------------------------------------------------------------
# Streaming Response Renderer
# ---------------------------------------------------------------------------

from rich.segment import Segment


class StreamingRenderer:
    """
    Renders streaming LLM responses directly to the console in stable "chunks".

    This completely eliminates all cursor movement bugs, duplication issues, 
    and scrolling corruption while providing 100% PERFECT Markdown rendering 
    and flawless borders.
    
    It works by rendering the Panel internally and only printing the completely
    stable lines that are guaranteed not to be changed by further word wrapping.
    """

    def __init__(self) -> None:
        self._buffer = ""
        self._started = False
        self._printed_lines = 0

    def _get_panel_lines(self, text: str) -> list[list[Segment]]:
        """Render the current text into Rich Segments."""
        try:
            md = Markdown(text)
        except Exception:
            md = text

        panel = Panel(
            md,
            border_style=THEME["primary_dim"],
            title=f"[bold {THEME['primary_bright']}]Agent[/bold {THEME['primary_bright']}]",
            title_align="left",
            padding=(0, 1),
        )
        options = console.options.update(width=console.width)
        return console.render_lines(panel, options)

    def start(self) -> None:
        """Start the streaming display."""
        console.print()
        self._buffer = ""
        self._printed_lines = 0
        self._started = True

    def add_text(self, text: str) -> None:
        """Add streamed text to the display."""
        if not self._started:
            return

        self._buffer += text
        # Strip completion signal so it never appears in the rendered output
        display_buffer = self._buffer.replace("<task_complete/>", "")
        lines = self._get_panel_lines(display_buffer)

        # Buffer the last 2 lines: the bottom border (-1) and the actively wrapping text (-2)
        # We print everything else because it is permanently stable.
        stable_count = max(0, len(lines) - 2)

        if stable_count > self._printed_lines:
            new_stable_lines = lines[self._printed_lines : stable_count]
            for line_segments in new_stable_lines:
                from rich.segment import Segment, Segments
                console.print(Segments(list(line_segments) + [Segment("\n")]), end="")
            self._printed_lines = stable_count

    def finish(self, as_narration: bool = False) -> str:
        """Finish streaming and return the full text."""
        # Strip completion signal before rendering the final panel
        self._buffer = self._buffer.replace("<task_complete/>", "").strip()
        if self._started and self._buffer.strip():
            lines = self._get_panel_lines(self._buffer)
            remaining_lines = lines[self._printed_lines:]
            for line_segments in remaining_lines:
                from rich.segment import Segment, Segments
                console.print(Segments(list(line_segments) + [Segment("\n")]), end="")
        elif self._started:
            # If the buffer was entirely empty but started, just print a small empty box
            lines = self._get_panel_lines("")
            for line_segments in lines:
                from rich.segment import Segment, Segments
                console.print(Segments(list(line_segments) + [Segment("\n")]), end="")

        self._started = False
        result = self._buffer
        self._buffer = ""
        self._printed_lines = 0
        return result

    def is_active(self) -> bool:
        return self._started


def render_cost_summary(summary: str) -> None:
    """Display cost tracking summary."""
    console.print(
        Panel(
            summary,
            border_style=THEME["primary_dim"],
            title=f"[bold {THEME['primary_bright']}]Cost Summary[/bold {THEME['primary_bright']}]",
            padding=(0, 2),
        )
    )


def render_git_status(status_text: str) -> None:
    """Display Git status information."""
    console.print(
        Panel(
            status_text,
            border_style=THEME["primary_dim"],
            title=f"[bold {THEME['primary_bright']}]Git Status[/bold {THEME['primary_bright']}]",
            padding=(0, 2),
        )
    )


def render_memory(memory_text: str) -> None:
    """Display memory from past sessions."""
    if not memory_text.strip():
        render_info("No persistent memory found from previous sessions.")
        return
    try:
        md = Markdown(memory_text)
    except Exception:
        md = memory_text
    console.print(
        Panel(
            md,
            border_style=THEME["primary_dim"],
            title=f"[bold {THEME['primary_bright']}]Session Memory[/bold {THEME['primary_bright']}]",
            padding=(1, 2),
        )
    )


def render_undo_result(message: str) -> None:
    """Display undo result."""
    if message.startswith("Undone"):
        render_success(message)
    else:
        render_info(message)


def render_web_results(results_text: str) -> None:
    """Display web search results."""
    console.print(
        Panel(
            results_text,
            border_style=THEME["primary_dim"],
            title=f"[bold {THEME['primary_bright']}]Web Search[/bold {THEME['primary_bright']}]",
            padding=(0, 2),
        )
    )





def render_git_startup_info(status: dict) -> None:
    """Show Git info on startup."""
    if not status.get("is_git"):
        return

    parts = [f"[{THEME['success']}]●[/{THEME['success']}] Git: {status['branch']}"]

    if not status.get("clean"):
        changes = len(status.get("modified", [])) + len(status.get("staged", []))
        untracked = len(status.get("untracked", []))
        change_parts = []
        if changes:
            change_parts.append(f"{changes} changed")
        if untracked:
            change_parts.append(f"{untracked} untracked")
        parts.append(f"  [{THEME['warning']}]({', '.join(change_parts)})[/{THEME['warning']}]")
    else:
        parts.append(f"  [{THEME['text_dim']}](clean)[/{THEME['text_dim']}]")

    console.print("  " + "".join(parts))


# ---------------------------------------------------------------------------
# Tab Completion for Slash Commands + Ctrl+V Image Paste
# ---------------------------------------------------------------------------

SLASH_COMMANDS = [
    "/add-dir", "/agent", "/agents", "/allowed-tools", "/allowedtools",
    "/analytics", "/auth", "/autopilot", "/branch", "/branches", "/cd", "/checkout",
    "/clear", "/cogs", "/commit", "/compact", "/config", "/context", "/continue",
    "/copy", "/cost", "/diff", "/distill", "/docsearch", "/doctor", "/documents",
    "/effort", "/exit", "/export", "/fast", "/files", "/fork", "/git",
    "/health", "/help", "/hive", "/hooks", "/image", "/ingest", "/init",
    "/init-rules", "/log", "/memory", "/merge", "/mode", "/model", "/new", "/paste",
    "/permissions", "/perms", "/plan", "/plan-mode", "/plugin", "/plugins",
    "/provider", "/q", "/quit", "/release-notes", "/rename", "/restore",
    "/retry", "/rewind", "/search", "/serve", "/sessions", "/settings",
    "/skill", "/skills", "/smartsearch", "/stats", "/status", "/summary",
    "/sync",
    "/tasks", "/think", "/trust", "/undo", "/web",
]

# Module-level list to pass pasted images from the Ctrl+V key binding
# back to the REPL loop.  Each entry is (base64_data, mime_type).
_pending_paste_images: list[tuple[str, str]] = []


def get_pending_paste_images() -> list[tuple[str, str]]:
    """Return and clear any images pasted via Ctrl+V during input."""
    imgs = list(_pending_paste_images)
    _pending_paste_images.clear()
    return imgs


async def get_input_with_completion(branch: str, turn: int, health_bar: str = "") -> str:
    """
    Get user input with tab completion for slash commands.
    Falls back to basic input if prompt_toolkit is not available.
    Uses prompt_async() to avoid nested asyncio.run() errors.

    Ctrl+V is intercepted: if the system clipboard contains an image,
    the image is grabbed and a 📎 marker is inserted into the input
    buffer. The actual image data is stored in _pending_paste_images
    for the REPL loop to consume.  If the clipboard contains text,
    normal paste behaviour is preserved.
    """
    # Clear any stale images from a previous prompt
    _pending_paste_images.clear()

    try:
        from prompt_toolkit import PromptSession
        from prompt_toolkit.completion import WordCompleter
        from prompt_toolkit.formatted_text import HTML
        from prompt_toolkit.key_binding import KeyBindings
        from prompt_toolkit.styles import Style as PTStyle

        completer = WordCompleter(
            SLASH_COMMANDS,
            sentence=True,
        )

        style = PTStyle.from_dict({
            "prompt": "#CC5555",
            "branch": "#CC5555",
            "turn": "#8B7070",
        })

        # ── Custom key bindings ──────────────────────────────────────
        kb = KeyBindings()

        def _paste_image_or_text(event):
            """Intercept paste: if clipboard has an image, grab it;
            otherwise fall through to normal text paste.

            Single binding:
              c-v        — works for CMD, older terminals, and macOS Terminal
            """
            # Lazy-import to avoid circular deps
            from cvc.agent.chat import _grab_clipboard_images

            images = _grab_clipboard_images()
            if images:
                # Store images for the REPL loop; accumulate across multiple pastes
                total_before = len(_pending_paste_images)
                _pending_paste_images.extend(images)
                total_after = len(_pending_paste_images)

                # Insert a visible per-image marker(s) into the text buffer
                buf = event.app.current_buffer
                for i in range(total_before, total_after):
                    label = f"image {i + 1}"
                    buf.insert_text(f" [{label}] ")
                    # Print immediate feedback above input line
                    from rich.console import Console as _RCon
                    _RCon(stderr=True).print(
                        f"[green]  ✓ {label}[/green]"
                    )
            else:
                # No image — paste text from system clipboard
                import sys as _sys
                _text = ""
                if _sys.platform == "win32":
                    try:
                        import ctypes
                        CF_UNICODETEXT = 13
                        u32 = ctypes.windll.user32
                        k32 = ctypes.windll.kernel32
                        if u32.OpenClipboard(0):
                            try:
                                h = u32.GetClipboardData(CF_UNICODETEXT)
                                if h:
                                    k32.GlobalLock.restype = ctypes.c_wchar_p
                                    _text = k32.GlobalLock(h) or ""
                                    k32.GlobalUnlock(h)
                            finally:
                                u32.CloseClipboard()
                    except Exception:
                        pass
                else:
                    # macOS / Linux: try subprocess
                    try:
                        import subprocess
                        if _sys.platform == "darwin":
                            _text = subprocess.run(
                                ["pbpaste"], capture_output=True, text=True, timeout=2,
                                                            **HIDDEN_KW,
                            ).stdout
                        else:
                            _text = subprocess.run(
                                ["xclip", "-selection", "clipboard", "-o"],
                                capture_output=True, text=True, timeout=2,
                                                            **HIDDEN_KW,
                            ).stdout
                    except Exception:
                        pass

                if _text:
                    event.app.current_buffer.insert_text(_text)
                else:
                    # Final fallback: prompt_toolkit's internal clipboard
                    event.app.current_buffer.paste_clipboard_data(
                        event.app.clipboard.get_data(),
                    )

        # eager=True takes priority over terminal default bindings where possible.
        # Note: Windows Terminal intercepts Ctrl+V before the app sees it — use /paste
        # in that case, or configure Windows Terminal to disable its Ctrl+V binding.
        kb.add("c-v", eager=True)(_paste_image_or_text)

        session = PromptSession(
            completer=completer,
            style=style,
            complete_while_typing=True,
            key_bindings=kb,
        )

        # Show the CVC info header with C-shaped arrow
        health_suffix = f"  {health_bar}" if health_bar else ""
        console.print(
            f"[{THEME['accent']}]╭[/{THEME['accent']}] "
            f"[bold {THEME['primary_bright']}]CVC[/bold {THEME['primary_bright']}]"
            f"[{THEME['text_dim']}]@[/{THEME['text_dim']}]"
            f"[bold {THEME['branch']}]{branch}[/bold {THEME['branch']}]"
            f"[{THEME['text_dim']}] (turn {turn})[/{THEME['text_dim']}]"
            f"{health_suffix}"
        )

        prompt_text = HTML(f'<style fg="{THEME["accent"]}">╰▶ </style>')
        line = await session.prompt_async(
            prompt_text,
            placeholder=HTML(f'<style fg="{THEME["text_dim"]}">Type your request here...</style>')
        )
        text = line.strip()
        return text

    except ImportError:
        # Fall back to basic Rich input
        return await asyncio.to_thread(print_input_prompt, branch, turn, health_bar)
    except (EOFError, KeyboardInterrupt):
        return "/exit"


# ---------------------------------------------------------------------------
# Context Autopilot Rendering
# ---------------------------------------------------------------------------

def render_autopilot_action(actions: list[str]) -> None:
    """Show Context Autopilot actions taken during a turn."""
    if not actions:
        return
    console.print()
    console.print(
        f"  [{THEME['primary_dim']}]⟫[/{THEME['primary_dim']}] "
        f"[bold #CC7733]Context Autopilot[/bold #CC7733]"
    )
    for action in actions:
        console.print(f"    [{THEME['text_dim']}]→ {action}[/{THEME['text_dim']}]")


def render_context_health(report) -> None:
    """
    Render a detailed context health dashboard for /health command.
    Accepts a ContextHealthReport object.
    """
    from cvc.agent.context_autopilot import HealthLevel

    color_map = {
        HealthLevel.GREEN: THEME["success"],
        HealthLevel.YELLOW: THEME["warning"],
        HealthLevel.ORANGE: "#CC7733",
        HealthLevel.RED: THEME["error"],
    }
    label_map = {
        HealthLevel.GREEN: "HEALTHY",
        HealthLevel.YELLOW: "THINNING",
        HealthLevel.ORANGE: "COMPACTING",
        HealthLevel.RED: "CRITICAL",
    }
    color = color_map.get(report.health_level, THEME["text"])
    label = label_map.get(report.health_level, "UNKNOWN")

    # Build the health bar
    bar = report.format_bar_rich(width=30)

    content = (
        f"  Status    [{color}]● {label}[/{color}]\n"
        f"  Context   {bar}\n"
        f"  Tokens    [bold]{report.estimated_tokens:,}[/bold] / {report.context_limit:,}\n"
        f"  Remaining [bold]{report.remaining_tokens:,}[/bold] tokens ({report.remaining_pct:.0f}%)\n"
        f"\n"
        f"  [{THEME['text_dim']}]Breakdown:[/{THEME['text_dim']}]\n"
        f"    System     {report.system_tokens:>8,} tokens\n"
        f"    User       {report.user_tokens:>8,} tokens\n"
        f"    Assistant  {report.assistant_tokens:>8,} tokens\n"
        f"    Tool       {report.tool_result_tokens:>8,} tokens "
        f"({report.tool_result_count} results)\n"
        f"\n"
        f"  [{THEME['text_dim']}]Messages: {report.message_count}  │  "
        f"Thinnable: {report.thinning_candidates}  │  "
        f"Compactable: {'Yes' if report.compaction_available else 'No'}[/{THEME['text_dim']}]"
    )

    if report.actions_taken:
        content += f"\n\n  [{THEME['warning']}]Actions taken this turn:[/{THEME['warning']}]"
        for action in report.actions_taken:
            content += f"\n    → {action}"

    console.print(
        Panel(
            content,
            border_style=color,
            title=f"[bold {color}]Context Autopilot — Health Dashboard[/bold {color}]",
            padding=(1, 2),
        )
    )


def render_autopilot_diagnostics(diagnostics: dict) -> None:
    """Render full autopilot diagnostics for /health verbose."""
    content = (
        f"  Enabled     [bold]{diagnostics['enabled']}[/bold]\n"
        f"  Model       {diagnostics['model']}\n"
        f"  Limit       {diagnostics['context_limit']:,} tokens\n"
        f"\n"
        f"  [{THEME['text_dim']}]Thresholds:[/{THEME['text_dim']}]\n"
        f"    Thin       {diagnostics['thresholds']['thin']}\n"
        f"    Compact    {diagnostics['thresholds']['compact']}\n"
        f"    Critical   {diagnostics['thresholds']['critical']}\n"
        f"\n"
        f"  [{THEME['text_dim']}]Session Stats:[/{THEME['text_dim']}]\n"
        f"    Compactions  {diagnostics['session_stats']['compactions_performed']}\n"
        f"    Thinnings    {diagnostics['session_stats']['thinnings_performed']}\n"
        f"    Tokens Saved {diagnostics['session_stats']['tokens_saved']:,}\n"
    )

    actions = diagnostics["session_stats"].get("actions_log", [])
    if actions:
        content += f"\n  [{THEME['text_dim']}]Recent Actions:[/{THEME['text_dim']}]"
        for entry in actions[-5:]:
            for action in entry.get("actions", []):
                content += f"\n    → {action}"

    console.print(
        Panel(
            content,
            border_style=THEME["primary_dim"],
            title=f"[bold {THEME['primary_bright']}]Autopilot Diagnostics[/bold {THEME['primary_bright']}]",
            padding=(1, 2),
        )
    )


def render_autopilot_progress(step: int, total: int, description: str) -> None:
    """Show autopilot plan progress (step X of Y)."""
    if total > 0:
        bar_filled = int((step / total) * 20)
        bar_empty = 20 - bar_filled
        bar = f"[{THEME['success']}]{'█' * bar_filled}[/{THEME['success']}][{THEME['text_dim']}]{'░' * bar_empty}[/{THEME['text_dim']}]"
        console.print(
            f"  [{THEME['primary_dim']}]⟫[/{THEME['primary_dim']}] "
            f"[bold #CC7733]Autopilot[/bold #CC7733] "
            f"Step {step}/{total}  {bar}  "
            f"[{THEME['text_dim']}]{description}[/{THEME['text_dim']}]"
        )
    else:
        console.print(
            f"  [{THEME['primary_dim']}]⟫[/{THEME['primary_dim']}] "
            f"[bold #CC7733]Autopilot[/bold #CC7733] "
            f"[{THEME['text_dim']}]{description}[/{THEME['text_dim']}]"
        )


def render_autopilot_continuation(
    iteration: int,
    remaining_steps: int,
    total_steps: int,
) -> None:
    """Show that autopilot is continuing execution after a premature stop."""
    if total_steps > 0:
        done = total_steps - remaining_steps
        console.print(
            f"\n  [{THEME['warning']}]⟳[/{THEME['warning']}] "
            f"[bold #CC7733]Autopilot[/bold #CC7733] continuing… "
            f"(iteration {iteration}, {done}/{total_steps} steps done)"
        )
    else:
        console.print(
            f"\n  [{THEME['warning']}]⟳[/{THEME['warning']}] "
            f"[bold #CC7733]Autopilot[/bold #CC7733] continuing… "
            f"(iteration {iteration})"
        )


# ---------------------------------------------------------------------------
# Agentic Auto-Retry Rendering
# ---------------------------------------------------------------------------

def render_retry_step(step: int, total: int, message: str) -> None:
    """Show progress through the 3-step retry process."""
    console.print(
        f"  [{THEME['warning']}]⟳ Step {step}/{total}:[/{THEME['warning']}] "
        f"[{THEME['text']}]{message}[/{THEME['text']}]"
    )


def render_diagnosis_panel(diagnosis: DiagnosisResult) -> None:
    """
    Render the diagnosis result as a Rich panel.

    Shows severity, affected files, what went wrong, and lessons learned.
    """
    severity_color = THEME["success"] if diagnosis.severity == "small" else THEME["error"]
    severity_icon = "◉" if diagnosis.severity == "small" else "◈"
    severity_label = "Minor Issue" if diagnosis.severity == "small" else "Major Issue"

    lines = [
        f"  {severity_icon} [{severity_color}][bold]{severity_label}[/bold][/{severity_color}]"
        f"  —  {diagnosis.recommended_action.replace('_', ' ').title()}",
        "",
        f"  [{THEME['text']}]What went wrong:[/{THEME['text']}]",
        f"    [{THEME['accent_soft']}]{diagnosis.what_went_wrong}[/{THEME['accent_soft']}]",
        "",
        f"  [{THEME['text']}]Files affected ({len(diagnosis.files_affected)}):[/{THEME['text']}]",
    ]
    for fp in diagnosis.files_affected[:10]:
        lines.append(f"    [{THEME['text_dim']}]• {fp}[/{THEME['text_dim']}]")
    if len(diagnosis.files_affected) > 10:
        lines.append(f"    [{THEME['text_dim']}]… and {len(diagnosis.files_affected) - 10} more[/{THEME['text_dim']}]")

    if diagnosis.lessons_learned:
        lines.append("")
        lines.append(f"  [{THEME['text']}]Lessons learned:[/{THEME['text']}]")
        for lesson in diagnosis.lessons_learned:
            lines.append(f"    [{THEME['warning']}]→[/{THEME['warning']}] {lesson}")

    console.print()
    console.print(
        Panel(
            "\n".join(lines),
            title=f"[bold {THEME['primary_bright']}]Diagnosis[/bold {THEME['primary_bright']}]",
            border_style=THEME["primary"],
            padding=(1, 1),
        )
    )


def render_revert_header(num_files: int) -> None:
    """Show header for the revert file selection section."""
    console.print()
    console.print(
        Panel(
            f"  [{THEME['text']}]The following {num_files} file(s) were changed in the last task.\n"
            f"  Select which files to revert to their previous version\n"
            f"  before retrying with lessons learned.[/{THEME['text']}]",
            title=f"[bold {THEME['warning']}]Revert Files[/bold {THEME['warning']}]",
            border_style=THEME["primary"],
            padding=(0, 1),
        )
    )


def render_revert_results(results: list[str]) -> None:
    """Show the revert operation results."""
    for result in results:
        if "failed" in result.lower():
            render_error(result)
        else:
            render_success(result)


def render_retry_complete(severity: str) -> None:
    """Show retry completion message."""
    if severity == "small":
        render_success("Retry complete — targeted fixes applied.")
    else:
        render_success("Retry complete — task re-executed with lessons learned.")
