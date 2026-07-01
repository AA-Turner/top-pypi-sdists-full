"""Slim top bar with logo and status dot."""

from __future__ import annotations

from rich.text import Text
from textual.reactive import reactive
from textual.widgets import Static

from dreadnode.app.tui.theme import ACCENT, BG, BG_LIGHTER, FG, FG_FAINTEST, FG_SUBTLE


class HeaderBar(Static):
    """Compact header -- logo, status dot, and session label."""

    DEFAULT_CSS = f"""
    HeaderBar {{
        height: 1;
        background: {BG_LIGHTER};
        padding: 0 1;
        content-align: left middle;
    }}
    """

    status_text: reactive[str] = reactive("Booting")
    session_label: reactive[str] = reactive("none")
    busy: reactive[bool] = reactive(False)
    compact: reactive[bool] = reactive(False)

    def render(self) -> Text:
        t = Text()

        if self.compact:
            # Compact mode: just status dot + status text
            if self.busy:
                t.append("\u25cf ", style=ACCENT)
                t.append(self.status_text, style=f"bold {ACCENT}")
            else:
                t.append("\u25cf ", style=ACCENT)
                t.append(self.status_text, style=FG)
            return t

        # Logo
        t.append(" DREADNODE ", style=f"bold {BG} on {ACCENT}")
        t.append("  ", style="")

        # Status dot + text
        if self.busy:
            t.append("\u25cf ", style=ACCENT)
            t.append(self.status_text, style=f"bold {ACCENT}")
        else:
            t.append("\u25cf ", style=ACCENT)
            t.append(self.status_text, style=FG)

        # Session label
        t.append("  \u2502  ", style=FG_FAINTEST)
        t.append(self.session_label, style=FG_SUBTLE)

        return t
