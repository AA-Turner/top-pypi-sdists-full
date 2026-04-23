"""Shared layout utilities for the Anteroom CLI.

Provides prompt prefix styling, input lexer, and input-toolbar helpers.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any, Callable

from prompt_toolkit.lexers import Lexer

if TYPE_CHECKING:
    from prompt_toolkit.formatted_text import StyleAndTextTuples


def _shorten_path(path: str) -> str:
    """Shorten an absolute path using ``~`` for the home directory."""
    import os

    home = os.path.expanduser("~")
    if path.startswith(home):
        return "~" + path[len(home) :]
    return path


# ---------------------------------------------------------------------------
# Input line prefix
# ---------------------------------------------------------------------------


_APPROVAL_PROMPT_STYLES = {
    "auto": "class:prompt.auto",
    "ask_for_dangerous": "class:prompt.safe",
    "ask_for_writes": "class:prompt.caution",
    "ask": "class:prompt.strict",
}

_current_approval_mode: str = ""
_bg_task_count: int = 0


def set_approval_mode(mode: str) -> None:
    """Update the approval mode used for prompt prefix coloring."""
    global _current_approval_mode
    _current_approval_mode = mode


def set_bg_task_count(count: int) -> None:
    """Update the background task count shown in the prompt prefix (#1313)."""
    global _bg_task_count
    _bg_task_count = max(0, count)


def input_line_prefix(line_number: int, wrap_count: int) -> "StyleAndTextTuples":
    """Prompt prefix for the input area: ``> `` on line 0, ``  `` after.

    Color varies by approval mode when set. When background tasks are
    running and the foreground is idle, appends a dim indicator (#1313).
    """
    if line_number == 0:
        style = _APPROVAL_PROMPT_STYLES.get(_current_approval_mode, "class:prompt")
        parts: StyleAndTextTuples = [(style, "> ")]
        if _bg_task_count > 0:
            parts.append(("class:prompt.bg", f"[{_bg_task_count} bg] "))
        return parts
    return [("class:prompt.continuation", ". ")]


def get_editing_mode_badge(
    editing_mode: str,
    *,
    app: Any | None = None,
    show_mode_badge: bool = True,
) -> str | None:
    """Return a compact mode badge for the input toolbar."""
    if not show_mode_badge:
        return None
    mode = (editing_mode or "").strip().lower()
    if mode == "vi":
        vi_state = getattr(app, "vi_state", None)
        input_mode = getattr(vi_state, "input_mode", None)
        input_name = str(input_mode).split(".")[-1].replace("_", " ").upper() if input_mode is not None else ""
        if "NAVIGATION" in input_name:
            return "VI NAV"
        if "REPLACE" in input_name:
            return "VI REPLACE"
        return "VI INSERT"
    if mode == "emacs":
        return "EMACS"
    return None


def get_input_hint(
    *,
    hint_context: str,
    paste_line_count: int = 0,
) -> str | None:
    """Return a context-aware, low-noise hint string for the prompt toolbar."""
    if hint_context == "multiline":
        if paste_line_count > 0:
            return f"{paste_line_count} pasted lines review before Enter"
        return "Multiline Enter sends Alt+Enter newline"
    if hint_context == "idle":
        return "Tab complete Alt+Enter newline Ctrl+D exit"
    return None


def build_input_toolbar_fragments(
    *,
    editing_mode: str,
    app: Any | None = None,
    show_mode_badge: bool = True,
    hint_context: str = "",
    paste_line_count: int = 0,
) -> "StyleAndTextTuples":
    """Format input-specific toolbar fragments appended to the status toolbar."""
    parts: StyleAndTextTuples = []
    badge = get_editing_mode_badge(editing_mode, app=app, show_mode_badge=show_mode_badge)
    hint = get_input_hint(hint_context=hint_context, paste_line_count=paste_line_count)
    if badge:
        parts.append(("class:bottom-toolbar.mode", badge))
    if badge and hint:
        parts.append(("class:bottom-toolbar.sep", " \u00b7 "))
    if hint:
        parts.append(("class:bottom-toolbar.hint", hint))
    return parts


# ---------------------------------------------------------------------------
# Input lexer — highlights /commands and !shell escapes
# ---------------------------------------------------------------------------

_COMMAND_PREFIX_RE = re.compile(r"^([/!]\S*)")


class InputLexer(Lexer):
    """Highlights first-line ``/commands`` and ``!shell`` escapes."""

    def lex_document(self, document: Any) -> Callable[[int], "StyleAndTextTuples"]:
        def get_line(lineno: int) -> "StyleAndTextTuples":
            line = document.lines[lineno] if lineno < len(document.lines) else ""
            m = _COMMAND_PREFIX_RE.match(line) if lineno == 0 else None
            if m:
                cmd_end = m.end()
                return [
                    ("class:input.command", line[:cmd_end]),
                    ("", line[cmd_end:]),
                ]
            return [("", line)]

        return get_line
