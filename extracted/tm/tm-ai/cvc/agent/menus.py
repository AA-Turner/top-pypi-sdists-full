"""
cvc.agent.menus — Arrow-key interactive selection menus.

Provides reusable components for arrow-key navigation in terminal prompts.
Built on prompt_toolkit (already a CVC dependency). No new packages needed.

Features:
  - arrow_select()  — Pick one option from a list using Up/Down + Enter
  - arrow_confirm() — Binary Yes/No with arrow-key toggle
  - Vim keys (j/k) supported alongside arrows
  - CVC THEME colors for consistent styling
  - Graceful fallback on Esc / Ctrl+C
"""

from __future__ import annotations

import asyncio
import sys
from typing import Any, TypeVar

from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.formatted_text import FormattedText

# ---------------------------------------------------------------------------
# CVC Theme — imported from the canonical source in renderer.py
# ---------------------------------------------------------------------------

try:
    from cvc.agent.renderer import THEME as _THEME
except ImportError:
    # Fallback for standalone usage / testing
    _THEME = {
        "primary": "#8B0000",
        "primary_dim": "#5C1010",
        "primary_bright": "#CC3333",
        "accent": "#FF4444",
        "text": "#E8D0D0",
        "text_dim": "#8B7070",
        "success": "#55AA55",
        "warning": "#CCAA33",
        "error": "#FF3333",
    }

T = TypeVar("T")


# ---------------------------------------------------------------------------
# arrow_select — multi-option interactive menu
# ---------------------------------------------------------------------------

def arrow_select(
    title: str,
    options: list[tuple[str, Any]],
    *,
    descriptions: list[str] | None = None,
    default: int = 0,
) -> Any | None:
    """
    Show an interactive menu with arrow-key navigation.

    Parameters
    ----------
    title : str
        The prompt title shown above the options.
    options : list[tuple[str, value]]
        List of (display_label, return_value) tuples.
    descriptions : list[str] | None
        Optional descriptions shown dim to the right of each option.
    default : int
        Index of the initially selected option (0-based).

    Returns
    -------
    The ``return_value`` from the selected option, or ``None`` if cancelled.
    """
    if not options:
        return None

    selected = [max(0, min(default, len(options) - 1))]
    result: list[Any | None] = [None]

    # ── Key bindings ─────────────────────────────────────────────────────
    kb = KeyBindings()

    @kb.add("up")
    @kb.add("k")  # vim
    def _prev(event: Any) -> None:
        selected[0] = (selected[0] - 1) % len(options)

    @kb.add("down")
    @kb.add("j")  # vim
    def _next(event: Any) -> None:
        selected[0] = (selected[0] + 1) % len(options)

    @kb.add("enter")
    def _accept(event: Any) -> None:
        result[0] = options[selected[0]][1]
        event.app.exit()

    @kb.add("escape")
    @kb.add("c-c")
    def _cancel(event: Any) -> None:
        result[0] = None
        event.app.exit()

    # Allow number keys for quick jump (1-9)
    for digit in range(1, 10):
        @kb.add(str(digit))
        def _jump(event: Any, d: int = digit) -> None:
            idx = d - 1
            if 0 <= idx < len(options):
                selected[0] = idx

    # ── Renderer ─────────────────────────────────────────────────────────
    def _get_text() -> FormattedText:
        fragments: list[tuple[str, str]] = []

        # Title
        fragments.append((_THEME["text"], f"  {title}\n"))
        fragments.append(("", "\n"))

        for i, (label, _val) in enumerate(options):
            is_sel = i == selected[0]

            # Cursor / indent
            if is_sel:
                fragments.append((f"bold {_THEME['primary_bright']}", "  ▸ "))
            else:
                fragments.append((_THEME["text_dim"], "    "))

            # Number
            num_style = f"bold {_THEME['accent']}" if is_sel else _THEME["text_dim"]
            fragments.append((num_style, f"{i + 1} "))

            # Label
            label_style = f"bold {_THEME['text']}" if is_sel else _THEME["text"]
            fragments.append((label_style, label))

            # Optional description
            if descriptions and i < len(descriptions) and descriptions[i]:
                fragments.append((_THEME["text_dim"], f"  — {descriptions[i]}"))

            fragments.append(("", "\n"))

        # Hint
        fragments.append(("", "\n"))
        fragments.append((_THEME["text_dim"], "  ↑↓ navigate  ⏎ select  esc cancel\n"))

        return FormattedText(fragments)

    # ── Application ──────────────────────────────────────────────────────
    control = FormattedTextControl(_get_text)
    layout = Layout(Window(content=control, wrap_lines=True, always_hide_cursor=True))

    app: Application[None] = Application(
        layout=layout,
        key_bindings=kb,
        full_screen=False,
        mouse_support=False,
    )

    try:
        # Detect if we're inside a running event loop (e.g. called from
        # an async function via asyncio.run).  prompt_toolkit's app.run()
        # internally calls asyncio.run() which would raise RuntimeError.
        # In that case, run the app in a worker thread where it can create
        # its own event loop safely.
        try:
            asyncio.get_running_loop()
            _in_async = True
        except RuntimeError:
            _in_async = False

        if _in_async:
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(1) as pool:
                pool.submit(app.run).result()
        else:
            app.run()
    except (EOFError, KeyboardInterrupt):
        return None

    return result[0]


# ---------------------------------------------------------------------------
# arrow_confirm — binary Yes/No selection
# ---------------------------------------------------------------------------

def arrow_confirm(
    prompt: str,
    *,
    default_yes: bool = True,
) -> bool:
    """
    Show a binary Yes/No prompt with arrow-key toggle.

    Parameters
    ----------
    prompt : str
        The question to display.
    default_yes : bool
        If True, "Yes" is pre-selected; otherwise "No".

    Returns
    -------
    True if "Yes" selected, False otherwise (including cancel).
    """
    options: list[tuple[str, bool]] = [
        ("Yes", True),
        ("No", False),
    ]
    default_idx = 0 if default_yes else 1

    result = arrow_select(prompt, options, default=default_idx)
    return result is True
