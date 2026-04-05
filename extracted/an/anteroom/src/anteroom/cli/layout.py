"""Shared layout utilities for the Anteroom CLI.

Provides prompt prefix styling, input lexer, and path shortening.
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
