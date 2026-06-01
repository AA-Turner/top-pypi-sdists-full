"""Interactive shell loop. Bridge between prompt_toolkit input and slash dispatch.

The loop:
1. Renders the banner + workspace snapshot on entry.
2. Reads a line via prompt_toolkit (history, tab-completion, key bindings).
3. Parses the line; if not a slash command, prints the hint.
4. Dispatches to the matching handler.
5. Re-prints the snapshot only when state changed (handler returns True).
6. Loops until /exit, /quit, Ctrl+D, or unhandled exception.
"""

from __future__ import annotations

from pathlib import Path

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from rich.console import Console

from efterlev.shell.commands import (
    COMMANDS,
    ShellContext,
    find_command,
    parse_input,
)
from efterlev.shell.layout import (
    render_entry,
    render_status_only,
    render_unknown_command_hint,
)
from efterlev.shell.state import read_snapshot, suggest_next

HISTORY_PATH = Path.home() / ".cache" / "efterlev" / "shell_history"


class _SlashCompleter(Completer):
    """Tab-completes the first token against the slash-command registry.

    Past the first token we hand off to prompt_toolkit's default
    behavior (none) — file-path completion for args is a v1.x follow-up.
    """

    def get_completions(self, document: Document, complete_event):  # type: ignore[no-untyped-def]
        text = document.text_before_cursor
        # Only complete when the cursor is on the first token (no spaces typed yet).
        if " " in text:
            return
        prefix = text
        for command in COMMANDS:
            for name in (command.name, *command.aliases):
                if name.startswith(prefix):
                    yield Completion(
                        name,
                        start_position=-len(prefix),
                        display_meta=command.summary,
                    )


def _prompt_style() -> Style:
    """Visual style for the prompt string itself. Subtle — accent for `>`."""
    return Style.from_dict(
        {
            "prompt.label": "ansicyan",
            "prompt.gt": "bold",
        }
    )


def _prompt_message() -> FormattedText:
    """The `efterlev>` prompt, with the chevron bolded for legibility."""
    return FormattedText(
        [
            ("class:prompt.label", "efterlev"),
            ("class:prompt.gt", "> "),
        ]
    )


def run_shell(root: Path) -> int:
    """Run the interactive shell rooted at `root`. Returns process exit code.

    Exit codes:
      0 — clean exit (/exit, Ctrl+D, /quit)
      130 — interrupted (Ctrl+C twice at the prompt, per convention)
    """
    console = Console()
    # Clear the terminal scrollback so the banner is the first thing the user
    # sees on entry — no install spinner, no pipx noise, no prior session
    # leftovers (v0.1.141 / #346). Skipped when stdout isn't a TTY so test
    # capture and `efterlev shell > log.txt` don't get ANSI escapes mixed in.
    if console.is_terminal:
        console.clear()

    ctx = ShellContext(root=root.resolve(), console=console)

    snapshot = read_snapshot(ctx.root)
    render_entry(console, snapshot, suggest_next(snapshot))

    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)

    session: PromptSession[str] = PromptSession(
        message=_prompt_message(),
        history=FileHistory(str(HISTORY_PATH)),
        auto_suggest=AutoSuggestFromHistory(),
        completer=_SlashCompleter(),
        complete_while_typing=True,  # Surface matches as the user types — more discoverable
        style=_prompt_style(),
        enable_history_search=True,
    )

    while not ctx.should_exit:
        try:
            line = session.prompt()
        except KeyboardInterrupt:
            # First Ctrl+C: clear current input, keep the loop alive.
            continue
        except EOFError:
            # Ctrl+D — clean exit.
            console.print()
            break

        parsed = parse_input(line)
        if parsed is None:
            continue

        raw_cmd, args = parsed
        if not raw_cmd.startswith("/") and raw_cmd != "?":
            render_unknown_command_hint(console, raw_cmd)
            continue

        command = find_command(raw_cmd)
        if command is None:
            render_unknown_command_hint(console, raw_cmd)
            continue

        try:
            state_changed = command.handler(ctx, args)
        except KeyboardInterrupt:
            # Ctrl+C during a running command — let it interrupt the child,
            # then drop back to the prompt cleanly.
            console.print()
            continue
        except Exception as e:
            from efterlev.shell.layout import render_error

            render_error(console, f"{type(e).__name__}: {e}")
            continue

        if state_changed:
            snapshot = read_snapshot(ctx.root)
            render_status_only(console, snapshot, suggest_next(snapshot))

    return 0
